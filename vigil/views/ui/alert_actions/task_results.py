from math import ceil

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.template import Template, Context
from django.views import View
from django.views.generic import ListView

from vigil.models import VigilTaskResult, PreProcessorAlertAction, NotificationAlertAction, LogicAlertAction


class TaskResultsListView(LoginRequiredMixin, ListView):
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
            'alert_action': alert_action,
            'alert_type': alert_type
        }


class TaskResultsDataTablesView(LoginRequiredMixin, View):
    def get(self, request, pk, alert_type):
        # get the basic parameters
        draw = int(request.GET.get('draw', 0))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 0))

        # handle a search term
        search = request.GET.get('search[value]', '')

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

        query_set = alert_action.task_results.all()

        if search:
            # start with a blank Q object and add a query for every non-relational field attached to the model
            q_objects = Q()

            for field in VigilTaskResult._meta.fields:
                if field.is_relation:
                    continue
                kwargs = {'{}__icontains'.format(field.name): search}
                q_objects |= Q(**kwargs)

            query_set = query_set.filter(q_objects)

        # handle the ordering
        order_column_index = request.GET.get('order[0][column]')
        order_by = request.GET.get('columns[{}][name]'.format(order_column_index))
        order_direction = request.GET.get('order[0][dir]')

        if order_direction == 'desc':
            order_by = '-{}'.format(order_by)

        if order_by:
            query_set = query_set.order_by(order_by)

        # now we have our completed queryset. we can paginate it
        index = start + 1  # start is 0 based, pages are 1 based
        page = Paginator(
            query_set,
            length
        ).get_page(
            ceil(index/length)
        )

        return JsonResponse(
            {
                'draw': draw,
                'recordsTotal': query_set.count(),
                'recordsFiltered': query_set.count(),
                'data': [
                    [
                        Template(
                            '{{ result.date_done }}'
                        ).render(
                            Context({'result': result})
                        ),
                        result.status,
                        result.result,
                        result.task_id
                    ] for result in page
                ]
            }
        )
