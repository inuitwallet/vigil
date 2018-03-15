from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView
from extra_views import UpdateWithInlinesView, InlineFormSet, NamedFormsetsMixin

from vigil.models import AlertChannel, AlertAction, ChannelAction


# Alert Channels


class ShowActiveAlertsView(ListView):
    model = AlertChannel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = AlertChannel.objects.filter(active=True)
        return context


class ShowAllAlertsView(LoginRequiredMixin, ListView):
    model = AlertChannel
    template_name_suffix = '_list_all'


class AlertChannelDetailView(LoginRequiredMixin, DetailView):
    model = AlertChannel


class ChannelActionInline(InlineFormSet):
    model = ChannelAction
    fields = ['alert_action', 'priority']
    extra = 2
    max_num = 10


class AlertChannelUpdateView(LoginRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):  # noqa
    model = AlertChannel
    template_name_suffix = '_update_form'
    fields = ['name', 'repeat_time', 'time_to_urgent']
    inlines = [ChannelActionInline]
    inlines_names = ['channel_actions']

    def get_success_url(self):
        return reverse_lazy('alert_detail', kwargs={'pk': self.object.pk})


class AlertChannelCreateView(LoginRequiredMixin, CreateView):
    model = AlertChannel
    template_name_suffix = '_create_form'
    fields = ['name', 'alert_actions', 'repeat_time', 'time_to_urgent']

    def get_success_url(self):
        return reverse_lazy('alert_detail', kwargs={'pk': self.object.pk})


class AlertChannelDeleteView(LoginRequiredMixin, DeleteView):
    model = AlertChannel
    success_url = reverse_lazy('all_alert_list')


# Alert Actions


class ShowAllAlertActionsView(LoginRequiredMixin, ListView):
    model = AlertAction


class AlertActionDetailView(LoginRequiredMixin, DetailView):
    model = AlertAction


class AlertActionUpdateView(LoginRequiredMixin, UpdateView):
    model = AlertAction
    template_name_suffix = '_update_form'
    fields = ['name', 'description', 'task', 'data']

    def get_success_url(self):
        return reverse_lazy('alert_action_detail', kwargs={'pk': self.object.pk})


class AlertActionCreateView(LoginRequiredMixin, CreateView):
    model = AlertAction
    template_name_suffix = '_create_form'
    fields = ['name', 'description', 'task', 'data']

    def get_success_url(self):
        return reverse_lazy('alert_action_detail', kwargs={'pk': self.object.pk})


class AlertActionDeleteView(LoginRequiredMixin, DeleteView):
    model = AlertAction
    success_url = reverse_lazy('all_alert_actions_list')
