from celery import states
from celery.task import Task
from celery.exceptions import Ignore

from vigil.celery import app


class LambdaBotErrorTask(Task):
    """
    Pre-process data from Lambda Bot when reporting
    insufficient funds to place total walls
    """
    expected_data = {
        'exchange': '',
        'bot_name': '',
        'action': '',
        'error': '',
    }

    action_type = 'preprocessor'

    def check_data(self, data):
        for key in self.expected_data:
            if key not in data:
                self.update_state(
                    state=states.FAILURE,
                    meta='A value for \'{}\' was not present in the passed data'.format(key)
                )
                return False
        return True

    def run(self, *args, **kwargs):
        data = kwargs.get('data', {})

        if not self.check_data(data):
            raise Ignore()

        return {
            'title': 'An Error occurred on {} {}'.format(data['exchange'], data['pair']),
            'message': (
                'The bot was attempting to {} when the following error occurred: {}'.format(
                    data['action'],
                    data['error']
                )
            )
        }


LambdaBotError = app.register_task(LambdaBotErrorTask())
