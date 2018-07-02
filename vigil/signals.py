import json
import logging

from celery.signals import task_postrun
from celery import uuid, signature, group

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.template.loader import render_to_string
from django.utils.timezone import now

from vigil import tasks
from vigil.models import VigilTaskResult, Alert

logger = logging.getLogger(__name__)


@task_postrun.connect
def postrun_handler(sender=None, headers=None, body=None, **kwargs):
    """
    After each task is run we need to update the UI.
    The task result is sent through the websocket to update the list of task results
    on the Alert Action detail page
    """
    task = kwargs.get('task')
    task_id = kwargs.get('task_id')

    try:
        task_result = VigilTaskResult.objects.get(task_id=task_id)
    except VigilTaskResult.DoesNotExist:
        return

    channel_layer = get_channel_layer()
    action_type = task.__class__.action_type

    task_result.alert_task_object.last_triggered = now()
    task_result.alert_task_object.save()

    # update the list of alert action results
    async_to_sync(channel_layer.group_send)(
        '{}_alert_action_detail_{}'.format(action_type, task_result.alert_task_id),
        {
            'type': 'update_action_task_results',
            'html': render_to_string(
                'vigil/fragments/action_task_result.html',
                {
                    'action_task_result': task_result,
                }
            )
        }
    )

    if kwargs.get('state') == 'SUCCESS':
        # Run the following only when a task was successful in running
        if action_type == 'preprocessor':
            # get the alert details (title, message and priority)
            alert_details = json.loads(task_result.result)
            # create the alert object and update the Alert Channel History and Active Alerts list
            # this returns the alert object
            update_preprocessor_tasks(alert_details, task_result.alert_channel, channel_layer)
            # run the logic actions
            # pass the data that triggered this preprocessor as logic tasks will need that
            data = kwargs.get('kwargs', {}).get('data')
            run_logic_actions(data, alert_details, task_result.alert_channel)

        if action_type == 'logic':
            pass

        if action_type == 'notification':
            task_result.alert_task_object.last_success = now()
            task_result.alert_task_object.save()


def update_preprocessor_tasks(alert_details, alert_channel, channel_layer):
    """
    Run only when a Preprocessor task completes successfully
    :param alert_details: dict containing title, message and priority
    :param alert_channel: affected alert channel
    :param channel_layer: channel layer for sending websocket data
    :return:
    """
    # Get or Create the Alert object
    alert, created = Alert.objects.get_or_create(
        alert_channel=alert_channel,
        title=alert_details['title'],
        active=True
    )

    if created:
        # there was no active alert with this title.
        message_type = 'new_alert'
        alert.priority = alert_channel.base_priority
    else:
        # an alert with this title was already active
        message_type = 'update_alert'

    # save the alert object with the necessary data
    alert.message = alert_details['message']
    alert.save()

    # then update the ui
    # update the Active Alert List
    async_to_sync(channel_layer.group_send)(
        'alert_list',
        {
            'type': 'update_alert_list',
            'message_type': message_type,
            'alert': str(alert.pk),
        }
    )

    # Update the Alert Channel History
    async_to_sync(channel_layer.group_send)(
        'alert_detail_{}'.format(alert_channel.pk),
        {
            'type': 'update_historical_alerts',
            'html': render_to_string(
                'vigil/fragments/historical_alert.html',
                {
                    'historical_alert': alert,
                }
            )
        }
    )


def run_logic_actions(data, alert_details, alert_channel):
    """
    Run the Logic actions after the preprocessor has completed successfully.
    Generally they will need the data that is passed to the preprocessor task in addition to their own
    :param data:
    :param alert_details:
    :param alert_channel:
    :return:
    """
    # We then run the Logic actions as a group (in parallel)
    logic_actions = []

    data['title'] = alert_details['title']
    data['message'] = alert_details['message']

    for logic_action in alert_channel.logic_actions.all():
        logic_task = getattr(tasks, logic_action.task.name)
        task_id = uuid()
        VigilTaskResult.objects.create(
            alert_channel=alert_channel,
            alert_task_object=logic_action,
            task_id=task_id
        )
        logic_sig = signature(
            logic_task,
            kwargs={
                'data': data,
                'business_logic_data': logic_action.business_logic_data
            },
            task_id=task_id,
            immutable=True
        )
        logic_actions.append(logic_sig)

    logic_group = group(logic_actions)
    logic_group.apply_async()
