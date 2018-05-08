import logging

from django.core.management import BaseCommand

from vigil.models import PreProcessorActionTask, LogicActionTask, NotificationActionTask
from vigil.tasks import preprocessors, logic, notifications

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info('Scanning Pre-processor tasks')

        # TODO - get all alert actions that use these tasks and save them to force updating of their data attributes  # noqa

        for task in preprocessors.__all__:
            task_object, created = PreProcessorActionTask.objects.get_or_create(
                name=task
            )
            task_class = getattr(preprocessors, task)

            if task_class.__doc__:
                task_object.description = ' '.join(task_class.__doc__.split())

            task_object.expected_data = task_class.expected_data

            task_object.save()

            if created:
                logger.info('created new PreProcessor Action Task {}'.format(task_object.name))
            else:
                logger.info('{} already existed. Data updated'.format(task_object.name))

            logger.info('Updating Alert Actions for {}'.format(task_object.name))

            for alert_action in task_object.action_tasks.all():
                alert_action.save()
                logger.info('>> Updated {}'.format(alert_action))

        logger.info('Scanning Logic tasks')

        for task in logic.__all__:
            task_object, created = LogicActionTask.objects.get_or_create(
                name=task
            )
            task_class = getattr(logic, task)

            if task_class.__doc__:
                task_object.description = ' '.join(task_class.__doc__.split())

            task_object.expected_data = task_class.expected_data
            task_object.business_logic_data = task_class.business_logic_data

            task_object.save()

            if created:
                logger.info('created new PreProcessor Action Task {}'.format(task_object.name))
            else:
                logger.info('{} already existed. Data updated'.format(task_object.name))

            logger.info('Updating Alert Actions for {}'.format(task_object.name))

            for alert_action in task_object.action_tasks.all():
                alert_action.save()
                logger.info('>> Updated {}'.format(alert_action))

        logger.info('Scanning Notification tasks')

        for task in notifications.__all__:
            task_object, created = NotificationActionTask.objects.get_or_create(
                name=task
            )
            task_class = getattr(notifications, task)

            if task_class.__doc__:
                task_object.description = ' '.join(task_class.__doc__.split())

            task_object.default_data = task_class.default_data

            task_object.save()

            if created:
                logger.info('created new PreProcessor Action Task {}'.format(task_object.name))
            else:
                logger.info('{} already existed. Data updated'.format(task_object.name))

            logger.info('Updating Alert Actions for {}'.format(task_object.name))

            for alert_action in task_object.action_tasks.all():
                alert_action.save()
                logger.info('>> Updated {}'.format(alert_action))
