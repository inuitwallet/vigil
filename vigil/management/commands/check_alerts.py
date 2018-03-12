import logging
from copy import copy
from django.core.management import BaseCommand
from django.utils.timezone import now

import vigil.tasks as tasks
from vigil.globals import priorities
from vigil.models import AlertChannel


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        active_channels = AlertChannel.objects.filter(active=True)
        logger.info('Got {} Active Channels'.format(active_channels.count()))

        for alert_channel in active_channels:
            # check if we need to set the priority to urgent
            if alert_channel.set_active + alert_channel.time_to_urgent < now():
                if alert_channel.priority != priorities[3][0]:
                    logger.warning('Setting Alert channel to URGENT')
                    alert_channel.priority = priorities[3][0]
                    alert_channel.save()

            for alert_action in alert_channel.actions.all():
                logger.info(
                    'Checking {}:{}...'.format(
                        alert_channel.name,
                        alert_action.task.name
                    )
                )

                if alert_action.last_triggered:
                    trigger_time = alert_action.last_triggered + alert_channel.repeat_time

                    if trigger_time > now():
                        logger.warning(
                            'Not yet reached trigger time. Wait another {}'.format(
                                trigger_time - now()
                            )
                        )
                        continue

                task = getattr(tasks, alert_action.task.name)

                task_data = copy(alert_action.data)
                task_data['title'] = alert_channel.title
                task_data['message'] = alert_channel.message
                task_data['priority'] = alert_channel.priority

                task.delay(data=task_data)

                alert_action.last_triggered = now()
                alert_action.save()
                logger.info('Alert sent')

