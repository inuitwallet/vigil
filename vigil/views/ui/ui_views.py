from itertools import chain

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView


from vigil.models import NotificationAlertAction


class NotificationAlertActionCreateView(
    SuccessMessageMixin,
    LoginRequiredMixin,
    CreateView
):
    model = NotificationAlertAction
    template_name_suffix = '_create_form'
    fields = ['name', 'description', 'task', 'data']
    success_message = '{} was created. Check the data field for any required information'

    def get_success_url(self):
        return reverse_lazy('alert_action_update', kwargs={'pk': self.object.pk})


class AlertActionDeleteView(LoginRequiredMixin, DeleteView):
    model = AlertAction
    success_url = reverse_lazy('all_alert_actions_list')
