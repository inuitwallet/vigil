from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from vigil.models import PreProcessorAlertAction


class ShowPreProcessorAlertActionsView(LoginRequiredMixin, ListView):
    model = PreProcessorAlertAction
    template_name = 'vigil/alert_action/preprocessor/list.html'


class PreProcessorAlertActionDetailView(LoginRequiredMixin, DetailView):
    model = PreProcessorAlertAction
    template_name = 'vigil/alert_action/preprocessor/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_results'] = Paginator(self.object.task_results.all(), 8).page(1)
        return context


class PreProcessorAlertActionUpdateView(LoginRequiredMixin, UpdateView):
    model = PreProcessorAlertAction
    template_name = 'vigil/alert_action/preprocessor/update_form.html'
    fields = ['name', 'description', 'task', 'expected_data']

    def get_success_url(self):
        return reverse_lazy(
            'preprocessor_alert_action_detail', kwargs={'pk': self.object.pk}
        )


class PreProcessorAlertActionCreateView(
    SuccessMessageMixin,
    LoginRequiredMixin,
    CreateView
):
    model = PreProcessorAlertAction
    template_name = 'vigil/alert_action/preprocessor/create_form.html'
    fields = ['name', 'description', 'task', 'expected_data']
    success_message = '%(name)s was created. ' \
                      'Check the data fields for any required information'

    def get_success_url(self):
        return reverse_lazy(
            'preprocessor_alert_action_update', kwargs={'pk': self.object.pk}
        )


class PreProcessorAlertActionDeleteView(LoginRequiredMixin, DeleteView):
    model = PreProcessorAlertAction
    template_name = 'vigil/alert_action/preprocessor/confirm_delete.html'
    success_url = reverse_lazy('preprocessor_alert_actions_list')
