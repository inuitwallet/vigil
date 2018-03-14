import requests
from celery import Task, states
from celery.exceptions import Ignore

from vigil.celery import app
from vigil.globals import priorities


class PushoverTask(Task):
    data = {
        'token': '',
        'user_token': '',
        'sound': ''
    }

    action_type = 'Notification'

    @staticmethod
    def alter_priority(priority):
        priors = [p[0] for p in priorities]
        return min(priors.index(priority) - 2, 1)

    def run(self, *args, **kwargs):
        data = kwargs.get('data', {})

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

        if response.get('status', 0) != 1:
            self.update_state(
                state=states.FAILURE,
                meta='bad status from pushover: {}'.format(response.get('errors'))
            )
            raise Ignore()

        return 'sent pushover notification'


Pushover = app.register_task(PushoverTask())
