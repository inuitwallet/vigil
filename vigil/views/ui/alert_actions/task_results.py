from django.views.generic import ListView

from vigil.models import VigilTaskResult, PreProcessorAlertAction, NotificationAlertAction, LogicAlertAction


class TaskResultsListView(ListView):
    model = VigilTaskResult
    template_name = 'vigil/alert_action/task_results.html'

    def get_context_data(self, **kwargs):
        alert_type = self.kwargs.get('alert_type')
        pk = self.kwargs.get('pk')
        alert_action = None

        if alert_type == 'preprocessor':
            try:
                alert_action = PreProcessorAlertAction.objects.get(pk=pk)
            except PreProcessorAlertAction.DoesNotExist:
                pass

        if alert_type == 'notification':
            try:
                alert_action = NotificationAlertAction.objects.get(pk=pk)
            except PreProcessorAlertAction.DoesNotExist:
                pass

        if alert_type == 'logic':
            try:
                alert_action = LogicAlertAction.objects.get(pk=pk)
            except PreProcessorAlertAction.DoesNotExist:
                pass

        return {
            'object_list': alert_action.task_results.all() if alert_action else [],
            'alert_action': alert_action
        }
