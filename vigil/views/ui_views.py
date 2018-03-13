from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView

from vigil.models import AlertChannel, AlertAction

# Alert Channels


class ShowActiveAlertsView(ListView):
    model = AlertChannel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = AlertChannel.objects.filter(active=True)
        return context


class ShowAllAlertsView(ListView):
    model = AlertChannel
    template_name_suffix = '_list_all'


class AlertChannelDetailView(DetailView):
    model = AlertChannel


class AlertChannelUpdateView(UpdateView):
    model = AlertChannel
    template_name_suffix = '_update_form'
    fields = ['name', 'actions', 'repeat_time', 'time_to_urgent']
    success_url = reverse_lazy('all_alert_list')


class AlertChannelCreateView(CreateView):
    model = AlertChannel
    template_name_suffix = '_create_form'
    fields = ['name', 'actions', 'repeat_time', 'time_to_urgent']
    success_url = reverse_lazy('all_alert_list')


class AlertChannelDeleteView(DeleteView):
    model = AlertChannel
    success_url = reverse_lazy('all_alert_list')


# Alert Actions


class ShowAllAlertActionsView(ListView):
    model = AlertAction


class AlertActionUpdateView(UpdateView):
    model = AlertAction
    template_name_suffix = '_update_form'
    fields = ['name', 'description', 'data', 'task']
    success_url = reverse_lazy('all_alert_actions_list')


class AlertActionCreateView(CreateView):
    model = AlertAction
    template_name_suffix = '_create_form'
    fields = ['name', 'description', 'data', 'task']
    success_url = reverse_lazy('all_alert_actions_list')


class AlertActionDeleteView(DeleteView):
    model = AlertAction
    success_url = reverse_lazy('all_alert_actions_list')
