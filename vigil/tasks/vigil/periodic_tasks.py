from asgiref.sync import async_to_sync
from celery import signature, group, uuid
from channels.layers import get_channel_layer
from django.utils.timezone import now

from vigil import tasks
from vigil.globals import priorities
from vigil.models import AlertChannel, VigilTaskResult
from vigil.celery import app


@app.task
def refresh_ui():
    """
    Update the Active Alerts list to keep the times up to date
    """
    updated_alerts = []

    for alert_channel in AlertChannel.objects.all():
        for alert in alert_channel.active_alerts:
            updated_alerts.append(alert)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'alert_list',
                {
                    'type': 'update_alert_list',
                    'message_type': 'update_alert_inplace',
                    'alert': str(alert.pk),
                }
            )

    return 'Refreshed: {}'.format(updated_alerts)


@app.task
def auto_acknowledge():
    """
    Scan all active alerts and acknowledge those that have auto_acknowledge set
    """
    acknowledged_alerts = []

    for alert_channel in AlertChannel.objects.all():
        for alert in alert_channel.active_alerts:
            # if the period between the last update and now is bigger than the auto-acknowledge period
            if (now() - alert.last_updated) >= alert_channel.auto_acknowledge:
                alert.active = False
                alert.save()

                acknowledged_alerts.append(alert)

                # update the ui
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'alert_list',
                    {
                        'type': 'update_alert_list',
                        'message_type': 'remove_alert',
                        'alert': str(alert.pk),
                    }
                )

    return 'Auto Acknowledged: {}'.format(acknowledged_alerts)


@app.task
def upgrade_priority():
    """
    For each active alert, determine if the priority should be raised
    """
    upgraded_alerts = []

    for alert_channel in AlertChannel.objects.all():
        for alert in alert_channel.active_alerts:
            # if the period between the last priority upgrade and now is greater than the time_to_uipgrade
            if (now() - alert.last_priority_change) > alert_channel.time_to_upgrade:
                index = 0

                for priority in priorities:
                    if priority[0] == alert.priority:
                        chosen_index = index + 1

                        if chosen_index > (len(priorities) - 1):
                            continue

                        alert.priority = priorities[chosen_index][0]
                        alert.save()

                        upgraded_alerts.append(alert)
                        break

                    index += 1

    return 'Upgraded Priority: {}'.format(upgraded_alerts)


@app.task
def send_notifications():
    """
    for each active alert. determine if notifications should be sent
    :return:
    """
    for alert_channel in AlertChannel.objects.all():
        # get the required notifications
        notifications = alert_channel.notification_actions.all()

        for alert in alert_channel.active_alerts:
            if alert.last_notification:
                # if the gap between now and the last notification time is less than the repeat period, we skip
                if (now() - alert.last_notification) < alert_channel.repeat_time:
                    print(
                        'Skipping notifications for {}. '
                        'Repeat time not elapsed for {}'.format(
                            alert,
                            (alert.last_notification + alert_channel.repeat_time) - now()
                        )
                    )
                    continue

            # we have the message details so we can trigger the notification tasks
            notification_list = []

            for notification_action in notifications:
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
