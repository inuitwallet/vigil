import requests
from celery import states
from celery.exceptions import Ignore
from celery.task import Task

from vigil.celery import app
from vigil.globals import priorities


class TestNotificationTask(Task):
    """
    Test Notiofication for testing parallel running
    """
    default_data = {}

    action_type = 'notification'

    def run(self, *args, **kwargs):
        print('Test Notification')

        return 'sent pushover notification'


Test = app.register_task(TestNotificationTask())
