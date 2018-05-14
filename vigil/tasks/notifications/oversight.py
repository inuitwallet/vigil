import hashlib
import hmac
import time
import uuid

import requests
from celery import states
from celery.task import Task
from celery.exceptions import Ignore

from vigil.celery import app


class OversightTask(Task):
    """
    Report the given error to oversight
    """
    default_data = {
        'name': '',
        'exchange': '',
        'api_secret': ''
    }

    action_type = 'notification'

    def check_data(self, data):
        for key in self.expected_data:
            if key not in data:
                self.update_state(
                    state=states.FAILURE,
                    meta='A value for \'{}\' was not present in the passed data'.format(key)
                )
                return False
        return True

    @staticmethod
    def generate_hash(api_secret, name, exchange):
        nonce = int(time.time() * 1000)
        # calculate the hash from supplied data
        return nonce, hmac.new(
            uuid.UUID(api_secret).bytes,
            '{}{}{}'.format(
                name.lower(),
                exchange.lower(),
                nonce
            ).encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def handle_response(self, r):
        if r.status_code != requests.codes.ok:
            self.update_state(
                state=states.FAILURE,
                meta='oversight gave a bad response code: {}'.format(r.status_code)
            )
            return False

        try:
            response = r.json()
        except ValueError:
            self.update_state(
                state=states.FAILURE,
                meta='oversight did not return valid JSON: {}'.format(r.text)
            )
            return False

        if not response.get('success', True):
            self.update_state(
                state=states.FAILURE,
                meta='oversight reported a failure: {}'.format(response)
            )
            return False

        return response

    def run(self, *args, **kwargs):
        data = kwargs.get('data', {})

        if not self.check_data(data):
            raise Ignore()

        name = data.get('name')
        exchange = data.get('exchange')

        nonce, generated_hash = self.generate_hash(
            data.get('api_secret'),
            name,
            exchange,
        )

        response = self.handle_response(
            requests.post(
                url='https://oversight.crypto-daio.co.uk/bot/report_error',
                data={
                    'name': name,
                    'exchange': exchange,
                    'n': nonce,
                    'h': generated_hash,
                    'title': data.get('text'),
                    'message': data.get('message')
                }
            )
        )

        if not response:
            return False

        return response


Oversight = app.register_task(OversightTask())
