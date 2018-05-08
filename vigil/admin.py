from django.contrib.admin import ModelAdmin
from django.contrib import admin

from vigil.models import VigilTaskResult, PreProcessorActionTask, Alert, NotificationActionTask, LogicActionTask


@admin.register(VigilTaskResult)
class VigilTaskResultAdmin(ModelAdmin):
    list_display = ['task_id', 'alert_channel', 'alert_task_object', 'status']
    raw_id_fields = ['alert_channel']


@admin.register(Alert)
class AlertAdmin(ModelAdmin):
    list_display = ['alert_channel', 'title', 'message', 'priority', 'active', 'alert_created', 'last_updated']
    raw_id_fields = ['alert_channel']


@admin.register(PreProcessorActionTask)
class PreProcessorActionTaskAdmin(ModelAdmin):
    list_display = ['name', 'description', 'expected_data']


@admin.register(NotificationActionTask)
class NotificationActionTaskAdmin(ModelAdmin):
    list_display = ['name', 'description', 'default_data']


@admin.register(LogicActionTask)
class LogicActionTaskAdmin(ModelAdmin):
    list_display = ['name', 'description', 'expected_data', 'business_logic_data']
