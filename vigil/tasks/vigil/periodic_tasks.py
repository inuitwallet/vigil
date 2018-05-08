from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils.timezone import now

from vigil.globals import priorities
from vigil.models import AlertChannel
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
            if alert.last_updated + alert_channel.auto_acknowledge <= now():
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
            if (now() - alert.last_updated) > alert_channel.time_to_upgrade:
                index = 0

                for priority in priorities:
                    if priority[0] == alert.priority:
                        chosen_index = index + 1

                        if chosen_index > (len(priorities) - 1):
                            continue

                        print(chosen_index)
                        print(priorities[chosen_index][0])

                        alert.priority = priorities[chosen_index][0]
                        alert.save()

                        upgraded_alerts.append(alert)
                        break

                    index += 1

    return 'Upgraded Priority: {}'.format(upgraded_alerts)