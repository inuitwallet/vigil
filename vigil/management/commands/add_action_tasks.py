import logging

from django.core.management import BaseCommand

from vigil.models import ActionTask
import vigil.tasks as tasks

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        for task in tasks.__all__:
            task_object, created = ActionTask.objects.get_or_create(
                name=task,
            )
            if created:
                logger.info('created new provider {}'.format(task))
            else:
                logger.info('{} already exists'.format(task))

            task_class = getattr(tasks, task)
            task_object.default_data = task_class.data
            task_object.action_type = task_class.action_type
            task_object.save()
            logger.info('updated default data and action type for {}'.format(task))
