import requests
from celery import Task, states
from celery.exceptions import Ignore

from vigil.celery import app


class LambdaBotTask(Task):
    data = {

    }

    action_type = 'Logic'

    def run(self, *args, **kwargs):
        data = kwargs.get('data', {})


LambdaBot = app.register_task(LambdaBotTask())
