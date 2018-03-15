from django.contrib import admin

from vigil.models import AlertChannel, AlertAction, ChannelAction


@admin.register(AlertChannel)
class AlertChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'alert_id', 'active']


@admin.register(AlertAction)
class AlertActionAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'last_triggered', 'task']


@admin.register(ChannelAction)
class ChannelActionAdmin(admin.ModelAdmin):
    list_display = ['priority', 'alert_channel', 'alert_action']
