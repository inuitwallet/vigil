from celery import states
from celery.task import Task
from celery.exceptions import Ignore

from vigil.celery import app


class LambdaBotInsufficientFundsTask(Task):
    """
    Pre-process data from Lambda Bot when reporting
    insufficient funds to place total walls
    """
    expected_data = {
        'exchange': '',
        'pair': '',
        'currency': '',
        'target_amount': '',
        'amount_available': '',
        'amount_on_order': ''
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
            'title': 'Refill {} on {} {}'.format(data['currency'], data['exchange'], data['pair']),
            'message': (
                'There are not enough {} to place orders on the {} {} pair.\n'
                'Require {:.4f} to reach the target of {:.4f} but there are only {:.4f} available.\n'
                'There are currently {:.4f} on order.'.format(
                    data['currency'],
                    data['exchange'],
                    data['pair'],
                    float(data['target_amount']) - float(data['amount_available']),
                    float(data['target_amount']),
                    float(data['amount_available']),
                    float(data['amount_on_order'])
                )
            )
        }


LambdaBotInsufficientFunds = app.register_task(LambdaBotInsufficientFundsTask())
