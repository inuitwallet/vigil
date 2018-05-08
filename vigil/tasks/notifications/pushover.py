import requests
from celery import states
from celery.exceptions import Ignore
from celery.task import Task

from vigil.celery import app
from vigil.globals import priorities


class PushoverTask(Task):
    """
    Send Notification to Pushover
    """
    default_data = {
        'token': '',
        'user_token': '',
        'sound': ''
    }

    action_type = 'notification'

    @staticmethod
    def alter_priority(priority):
        if priority is None:
            raise Ignore()

        priors = [p[0] for p in priorities]
        return min(priors.index(priority) - 2, 1)

    def run(self, *args, **kwargs):
        data = kwargs.get('data', {})

        for key in ['token', 'user_token', 'title', 'message', 'priority', 'sound']:
            if key not in data:
                self.update_state(
                    state=states.FAILURE,
                    meta='{} not passed in data'.format(key)
                )
                raise Ignore()

        r = requests.post(
            url='https://api.pushover.net/1/messages.json',
            data={
                'token': data.get('token'),
                'user': data.get('user_token'),
                'title': data.get('title'),
                'message': data.get('message'),
                'priority': self.alter_priority(data.get('priority')),
                'sound': data.get('sound')
            }
        )

        if r.status_code != requests.codes.ok:
            try:
                self.update_state(
                    state=states.FAILURE,
                    meta='bad response from pushover: {}'.format(r.json())
                )
            except ValueError:
                self.update_state(
                    state=states.FAILURE,
                    meta='bad response from pushover: {}'.format(r.status_code)
                )

            raise Ignore()

        try:
            response = r.json()
        except ValueError:
            self.update_state(
                state=states.FAILURE,
                meta='no json from pushover: {}'.format(r.text)
            )
            raise Ignore()

        if response.get('status') != 1:
            self.update_state(
                state=states.FAILURE,
                meta='bad status from pushover: {}'.format(response.get())
            )
            raise Ignore()

        return 'sent pushover notification'


Pushover = app.register_task(PushoverTask())
