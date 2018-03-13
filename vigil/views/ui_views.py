from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from vigil.models import AlertChannel, AlertAction


class ShowActiveAlertsView(ListView):
    model = AlertChannel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = AlertChannel.objects.filter(active=True)
        return context


class ShowAllAlertsView(ListView):
    model = AlertChannel
    template_name_suffix = '_list_all'


class ShowAllAlertActionsView(ListView):
    model = AlertAction


class AlertChannelUpdateView(UpdateView):
    model = AlertChannel
    fields = ['name', 'actions', 'repeat_time', 'time_to_urgent']
    success_url = reverse_lazy('alert_list')


class AlertActionUpdateView(UpdateView):
    model = AlertAction
    fields = ['name', 'description', 'data', 'task']
    success_url = reverse_lazy('all_alert_actions_list')
