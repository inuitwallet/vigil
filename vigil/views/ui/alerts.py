from math import ceil

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.template import Template, Context
from django.views import View
from django.views.generic import ListView

from vigil.models import Alert, AlertChannel


class AlertListView(LoginRequiredMixin, ListView):
    model = Alert
    template_name = 'vigil/alert_channel/historical_alert_list.html'

    def get_context_data(self, **kwargs):
        try:
            alert_channel = AlertChannel.objects.get(pk=self.kwargs.get('pk'))
        except AlertChannel.DoesNotExist:
            alert_channel = None

        return {
            'alert_channel': alert_channel
        }


class AlertDataTablesView(LoginRequiredMixin, View):
    def get(self, request, pk):
        # get the basic parameters
        draw = int(request.GET.get('draw', 0))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 0))

        # handle a search term
        search = request.GET.get('search[value]', '')
        query_set = Alert.objects.filter(alert_channel__pk=pk)
        results_total = query_set.count()

        if search:
            # start with a blank Q object and add a query for every non-relational field attached to the model
            q_objects = Q()

            for field in Alert._meta.fields:
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
                'recordsTotal': results_total,
                'recordsFiltered': query_set.count(),
                'data': [
                    [
                        Template(
                            '{{ alert.alert_created }}'
                        ).render(
                            Context({'alert': alert})
                        ),
                        alert.title,
                        alert.message,
                        Template(
                            '<p class="{{ alert.bootstrap_priority}}">{{ alert.priority }}</p>'
                        ).render(
                            Context({'alert': alert})
                        ),
                        Template(
                            '{% if alert.active %}'
                            '   <p class="text-danger">Active</p>'
                            '{% else %}'
                            '   Acknowledged'
                            '{% endif %}'
                        ).render(
                            Context({'alert': alert})
                        ),
                        Template(
                            '{{ alert.last_updated }}'
                        ).render(
                            Context({'alert': alert})
                        ),
                        Template(
                            '{{ alert.last_notification }}'
                        ).render(
                            Context({'alert': alert})
                        ),
                    ] for alert in page
                ]
            }
        )
