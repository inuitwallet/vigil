from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from vigil.globals import priorities
from vigil.models import AlertChannel, HistoricalAlert


class AlertsAcknowledge(View):
    @staticmethod
    def post(request):
        for alert_id in request.POST.getlist('acknowledge_alerts'):
            try:
                alert = AlertChannel.objects.get(alert_id=alert_id)
                alert.active = False
                alert.save()
            except AlertChannel.DoesNotExist:
                continue
        return redirect('alert_list')


class AlertVigil(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(AlertVigil, self).dispatch(request, *args, **kwargs)

    @staticmethod
    def post(request, alert_channel_uuid):
        """
        Main endpoint for activating or updating an existing alert channel
        :param request: Django request
        :param alert_channel_uuid: first section of the UUID
        :param title: String - Title to set the alert to
        :param message: String - Alert Message
        :param priority: Int -
            0 = LOW
            1 = MEDIUM (default)
            2 = HIGH
            3 = URGENT
            4 = EMERGENCY - rarely if ever used
        :return:
        """
        alert_channel = get_object_or_404(
            AlertChannel,
            alert_id=alert_channel_uuid
        )

        message_type = 'update_alert'

        if not alert_channel.active:
            alert_channel.active = True
            alert_channel.set_active = now()
            message_type = 'new_alert'

        alert_channel.title = request.POST.get('title')
        alert_channel.message = request.POST.get('message')

        priority = request.POST.get('priority', 1)

        try:
            priority = int(priority)
        except ValueError:
            priority = 1

        if priority < 0 or priority > len(priorities):
            priority = 1

        # set the priority based on the list from globals
        alert_channel.priority = priorities[priority][0]
        alert_channel.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'alert_list',
            {
                'type': 'update_alert_list',
                'message_type': message_type,
                'alert_id': str(alert_channel.alert_id),
            }
        )

        # create a history point
        historical_alert = HistoricalAlert.objects.create(
            alert_channel=alert_channel,
            title=alert_channel.title,
            message=alert_channel.message,
            priority=alert_channel.priority,
            updated=(message_type == 'update_alert')
        )
        async_to_sync(channel_layer.group_send)(
            'alert_detail_{}'.format(alert_channel.pk),
            {
                'type': 'update_historical_alerts',
                'html': render_to_string(
                    'vigil/fragments/historical_alert.html',
                    {
                        'historical_alert': historical_alert,
                    }
                )
            }
        )

        return JsonResponse({'success': True})
