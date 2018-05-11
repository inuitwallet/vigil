from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from vigil.models import LogicAlertAction


class ShowLogicAlertActionsView(LoginRequiredMixin, ListView):
    model = LogicAlertAction
    template_name = 'vigil/alert_action/logic/list.html'


class LogicAlertActionDetailView(LoginRequiredMixin, DetailView):
    model = LogicAlertAction
    template_name = 'vigil/alert_action/logic/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_results'] = Paginator(self.object.task_results.all(), 8).page(1)
        return context


class LogicAlertActionUpdateView(LoginRequiredMixin, UpdateView):
    model = LogicAlertAction
    template_name = 'vigil/alert_action/logic/update_form.html'
    fields = ['name', 'description', 'task', 'expected_data', 'business_logic_data',
              'notification_actions']

    def get_success_url(self):
        return reverse_lazy('logic_alert_action_detail', kwargs={'pk': self.object.pk})


class LogicAlertActionCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = LogicAlertAction
    template_name = 'vigil/alert_action/logic/create_form.html'
    fields = ['name', 'description', 'task', 'expected_data', 'business_logic_data',
              'notification_actions']
    success_message = '%(name)s was created. ' \
                      'Check the data fields for any required information'

    def get_success_url(self):
        return reverse_lazy('logic_alert_action_update', kwargs={'pk': self.object.pk})


class LogicAlertActionDeleteView(LoginRequiredMixin, DeleteView):
    model = LogicAlertAction
    template_name = 'vigil/alert_action/logic/confirm_delete.html'
    success_url = reverse_lazy('logic_alert_actions_list')
