from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from vigil.models import NotificationAlertAction


class ShowNotificationAlertActionsView(LoginRequiredMixin, ListView):
    model = NotificationAlertAction
    template_name = 'vigil/alert_action/notification/list.html'


class NotificationAlertActionDetailView(LoginRequiredMixin, DetailView):
    model = NotificationAlertAction
    template_name = 'vigil/alert_action/notification/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_results'] = Paginator(self.object.task_results.all(), 8).page(1)
        return context


class NotificationAlertActionUpdateView(LoginRequiredMixin, UpdateView):
    model = NotificationAlertAction
    template_name = 'vigil/alert_action/notification/update_form.html'
    fields = ['name', 'description', 'task', 'data']

    def get_success_url(self):
        return reverse_lazy(
            'notification_alert_action_detail', kwargs={'pk': self.object.pk}
        )


class NotificationAlertActionCreateView(
    SuccessMessageMixin,
    LoginRequiredMixin,
    CreateView
):
    model = NotificationAlertAction
    template_name = 'vigil/alert_action/notification/create_form.html'
    fields = ['name', 'description', 'task', 'data']
    success_message = '%(name)s was created. ' \
                      'Check the data field for any required information'

    def get_success_url(self):
        return reverse_lazy(
            'notification_alert_action_update', kwargs={'pk': self.object.pk}
        )


class NotificationAlertActionDeleteView(LoginRequiredMixin, DeleteView):
    model = NotificationAlertAction
    template_name = 'vigil/alert_action/notification/confirm_delete.html'
    success_url = reverse_lazy('notification_alert_actions_list')
