from django.contrib import admin

from vigil.models import AlertChannel, AlertAction, ActionTask


@admin.register(AlertChannel)
class AlertChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'alert_id', 'active']


@admin.register(AlertAction)
class AlertActionAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'last_triggered', 'task']
