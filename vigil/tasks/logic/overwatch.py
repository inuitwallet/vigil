import hashlib
import hmac
import time
import uuid

import requests
from celery import states
from celery.task import Task
from celery.exceptions import Ignore

from vigil.celery import app


class OverwatchTask(Task):
    """
    Report the given error to overwatch
    """
    expected_data = {
        'bot_name': '',
        'exchange': '',
        'title': '',
        'message': ''
    }

    business_logic_data = {
        'api_user': '',
        'api_secret': ''
    }

    action_type = 'logic'

    def check_data(self, data):
        for key in self.expected_data:
            if key not in data:
                self.update_state(
                    state=states.FAILURE,
                    meta='A value for \'{}\' was not present in the passed data'.format(key)
                )
                return False
        return True

    def check_business_logic_data(self, data):
        for key in self.business_logic_data:
            if key not in data:
                self.update_state(
                    state=states.FAILURE,
                    meta='A value for \'{}\' was not present in the saved business logic data'.format(key)
                )
                return False
        return True

    @staticmethod
    def generate_hash(api_user, api_secret):
        nonce = int(time.time() * 1000)
        # calculate the hash from supplied data
        return nonce, hmac.new(
            uuid.UUID(api_secret).bytes,
            '{}{}'.format(
                uuid.UUID(api_user).hex.lower(),
                nonce
            ).encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def handle_response(self, r):
        if r.status_code != requests.codes.ok:
            self.update_state(
                state=states.FAILURE,
                meta='overwatch gave a bad response code: {} {}'.format(r.status_code, r.text)
            )
            return False

        try:
            response = r.json()
        except ValueError:
            self.update_state(
                state=states.FAILURE,
                meta='overwatch did not return valid JSON: {}'.format(r.text)
            )
            return False

        if not response.get('success', True):
            self.update_state(
                state=states.FAILURE,
                meta='overwatch reported a failure: {}'.format(response)
            )
            return False

        return response

    def run(self, *args, **kwargs):
        data = kwargs.get('data', {})

        if not self.check_data(data):
            raise Ignore()

        business_logic_data = kwargs.get('business_logic_data', 'Nope')

        if not self.check_business_logic_data(business_logic_data):
            raise Ignore()

        api_user = business_logic_data.get('api_user')
        api_secret =  business_logic_data.get('api_secret')

        nonce, generated_hash = self.generate_hash(
            api_user,
            api_secret
        )

        name = data.get('bot_name')
        exchange = data.get('exchange')

        response = self.handle_response(
            requests.post(
                url='https://overwatch.crypto-daio.co.uk/bot/report_error',
                data={
                    'name': name,
                    'exchange': exchange,
                    'api_user': api_user,
                    'n': nonce,
                    'h': generated_hash,
                    'title': data.get('title'),
                    'message': data.get('message')
                }
            )
        )

        if not response:
            raise Ignore()

        return response


Overwatch = app.register_task(OverwatchTask())
