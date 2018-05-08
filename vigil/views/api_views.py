from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from vigil.models import AlertChannel, Alert
from celery import uuid, signature, group, chord, chain

from vigil import tasks
from vigil.models import VigilTaskResult


class AlertsAcknowledge(View):
    @staticmethod
    def post(request):
        for alert_pk in request.POST.getlist('acknowledge_alerts'):
            try:
                alert = Alert.objects.get(pk=alert_pk)
                alert.active = False
                alert.save()
            except Alert.DoesNotExist:
                continue
        return redirect('active_alert_channel_list')


class AlertVigil(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(AlertVigil, self).dispatch(request, *args, **kwargs)

    @staticmethod
    def post(request, alert_channel_uuid):
        """
        Main endpoint for activating or updating an alert on an existing alert channel
        """
        alert_channel = get_object_or_404(
            AlertChannel,
            alert_id=alert_channel_uuid
        )

        # First we run the preprocessor task
        preprocessor_task = getattr(tasks, alert_channel.preprocessor_action.task.name)
        task_id = uuid()
        VigilTaskResult.objects.create(
            alert_channel=alert_channel,
            alert_task_object=alert_channel.preprocessor_action,
            task_id=task_id
        )
        # build the preprocessor signature
        preprocessor_sig = signature(
            preprocessor_task,
            kwargs={
                'data': request.POST
            },
            task_id=task_id,
            immutable=True
        )
        # run the preprocessor async.
        # when this has finished, the notifications tasks will run.
        # This is handled by the signals
        preprocessor_sig.apply_async()

        # We then run the Logic actions as a group (in parallel)
        logic_actions = []

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
                    'data': request.POST
                },
                task_id=task_id,
                immutable=True
            )
            logic_actions.append(logic_sig)

        logic_group = group(logic_actions)
        logic_group.apply_async()

        return JsonResponse({'success': True})
