from django.views.generic import ListView

from vigil.models import Alert, AlertChannel


class AlertListView(ListView):
    model = Alert
    template_name = 'vigil/alert_channel/historical_alert_list.html'

    def get_context_data(self, **kwargs):
        try:
            alert_channel = AlertChannel.objects.get(pk=self.kwargs.get('pk'))
        except AlertChannel.DoesNotExist:
            alert_channel = None

        return {
            'object_list': Alert.objects.filter(alert_channel=alert_channel),
            'alert_channel': alert_channel
        }
