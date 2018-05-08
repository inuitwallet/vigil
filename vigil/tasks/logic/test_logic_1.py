import requests
from celery import states
from celery.exceptions import Ignore
from celery.task import Task

from vigil.celery import app
from vigil.globals import priorities


class TestLogicTask1(Task):
    """
    Test Notiofication for testing parallel running
    """
    expected_data = {}
    business_logic_data = {}

    action_type = 'logic'

    def run(self, *args, **kwargs):
        print('Test Logic 1')

        return 'test logic'


Test = app.register_task(TestLogicTask1())
