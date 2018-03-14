from celery.signals import task_postrun

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.template.loader import render_to_string

from vigil.models import VigilTaskResult


@task_postrun.connect
def update_alert_action_result_list(sender=None, headers=None, body=None, **kwargs):
    try:
        action_task_result = VigilTaskResult.objects.get(task_id=kwargs.get('task_id'))
    except VigilTaskResult.DoesNotExist:
        return

    print(action_task_result.alert_action_id)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'alert_action_detail_{}'.format(action_task_result.alert_action_id),
        {
            'type': 'update_action_task_results',
            'html': render_to_string(
                'vigil/fragments/action_task_result.html',
                {
                    'action_task_result': action_task_result,
                }
            )
        }
    )
