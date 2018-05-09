import logging

from celery import signature, group, uuid
from django.utils.timezone import now

from vigil import tasks
from vigil.models import VigilTaskResult

logger = logging.getLogger(__name__)


def queue_notifications(notifications, alert_channel, alert):
    # we have the message details so we can trigger the notification tasks
    notification_list = []

    for notification_action in notifications:

        if alert.last_notification:
            # if the gap between now and the last notification time is less than the repeat period, we skip
            if (now() - alert.last_notification) < alert_channel.repeat_time:
                logger.warning(
                    'Skipping notification "{}". '
                    'Repeat time not elapsed for {}'.format(
                        notification_action,
                        (alert.last_notification + alert_channel.repeat_time) - now()
                    )
                )
                continue

        notification_task = getattr(tasks, notification_action.task.name)
        task_id = uuid()
        VigilTaskResult.objects.create(
            alert_channel=alert_channel,
            alert_task_object=notification_action,
            task_id=task_id
        )
        data = {
            'title': alert.title,
            'message': alert.message,
            'priority': alert.priority
        }
        data.update(notification_action.data)
        notification_sig = signature(
            notification_task,
            kwargs={
                'data': data
            },
            task_id=task_id,
            immutable=True
        )
        notification_list.append(notification_sig)

    notifications_group = group(notification_list)
    notifications_group.apply_async()

    alert.last_notification = now()
    alert.save()
