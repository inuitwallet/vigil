from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView

from vigil.models import AlertChannel


class ShowActiveAlertsView(ListView):
    model = AlertChannel
    template_name = 'vigil/alert_channel/list_active.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = []

        for alert_channel in AlertChannel.objects.all():
            for alert in alert_channel.alert_set.filter(active=True):
                context['object_list'].append(alert)

        return context


class ShowAllAlertsView(LoginRequiredMixin, ListView):
    model = AlertChannel
    template_name = 'vigil/alert_channel/list_all.html'


class AlertChannelDetailView(LoginRequiredMixin, DetailView):
    model = AlertChannel
    template_name = 'vigil/alert_channel/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historical_alerts'] = Paginator(self.object.alert_set.all(), 10).page(1)
        return context


class AlertChannelUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AlertChannel
    template_name = 'vigil/alert_channel/update_form.html'
    fields = ['name', 'repeat_time', 'time_to_upgrade', 'auto_acknowledge', 'base_priority',
              'preprocessor_action', 'notification_actions', 'logic_actions']
    success_message = '%(name)s has been updated'

    def get_success_url(self):
        return reverse_lazy('alert_channel_detail', kwargs={'pk': self.object.pk})


class AlertChannelCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = AlertChannel
    template_name = 'vigil/alert_channel/create_form.html'
    fields = ['name', 'repeat_time', 'time_to_upgrade', 'auto_acknowledge', 'base_priority',
              'preprocessor_action', 'notification_actions', 'logic_actions']
    success_message = '%(name)s has been created'

    def get_success_url(self):
        return reverse_lazy('alert_channel_detail', kwargs={'pk': self.object.pk})


class AlertChannelDeleteView(LoginRequiredMixin, DeleteView):
    model = AlertChannel
    template_name = 'vigil/alert_channel/confirm_delete.html'
    success_url = reverse_lazy('all_alert_channel_list')
