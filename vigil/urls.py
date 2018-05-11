"""vigil URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from vigil import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),

    ######
    # Alerts API

    path(
        'alert/<uuid:alert_channel_uuid>',
        views.AlertVigil.as_view(),
        name='alert'
    ),
    path(
        'alerts/acknowledge',
        views.AlertsAcknowledge.as_view(),
        name='acknowledge'
    ),

    ######
    # Alerts UI

    # Alert Channels

    path(
        '',
        views.ShowActiveAlertsView.as_view(),
        name='active_alert_channel_list'
    ),
    path(
        'alert_channels',
        views.ShowAllAlertsView.as_view(),
        name='all_alert_channel_list'
    ),
    path(
        'alert_channel/<int:pk>',
        views.AlertChannelDetailView.as_view(),
        name='alert_channel_detail'
    ),
    path(
        'alert_channel/create',
        views.AlertChannelCreateView.as_view(),
        name='alert_channel_create'
    ),
    path(
        'alert_channel/<int:pk>/edit',
        views.AlertChannelUpdateView.as_view(),
        name='alert_channel_update'
    ),
    path(
        'alert_channel/<int:pk>/delete',
        views.AlertChannelDeleteView.as_view(),
        name='alert_channel_delete'
    ),

    path(
        'alert_channel/<int:pk>/historical_alerts',
        views.AlertListView.as_view(),
        name='historical_alerts'
    ),

    path(
        'alert_channel/<int:pk>/historical_alerts/datatable',
        views.AlertDataTablesView.as_view(),
        name='historical_alerts_datatable'
    ),

    # Preprocessor Alert Actions

    path(
        'preprocessor_alert_actions',
        views.ShowPreProcessorAlertActionsView.as_view(),
        name='preprocessor_alert_actions_list'
    ),
    path(
        'preprocessor_alert_action/<int:pk>',
        views.PreProcessorAlertActionDetailView.as_view(),
        name='preprocessor_alert_action_detail'
    ),
    path(
        'preprocessor_alert_action/create',
        views.PreProcessorAlertActionCreateView.as_view(),
        name='preprocessor_alert_action_create'
    ),
    path(
        'preprocessor_alert_action/<int:pk>/edit',
        views.PreProcessorAlertActionUpdateView.as_view(),
        name='preprocessor_alert_action_update'
    ),
    path(
        'preprocessor_alert_action/<int:pk>/delete',
        views.PreProcessorAlertActionDeleteView.as_view(),
        name='preprocessor_alert_action_delete'
    ),

    # Logic Alert Actions

    path(
        'logic_alert_actions',
        views.ShowLogicAlertActionsView.as_view(),
        name='logic_alert_actions_list'
    ),
    path(
        'logic_alert_action/<int:pk>',
        views.LogicAlertActionDetailView.as_view(),
        name='logic_alert_action_detail'
    ),
    path(
        'logic_alert_action/create',
        views.LogicAlertActionCreateView.as_view(),
        name='logic_alert_action_create'
    ),
    path(
        'logic_alert_action/<int:pk>/edit',
        views.LogicAlertActionUpdateView.as_view(),
        name='logic_alert_action_update'
    ),
    path(
        'logic_alert_action/<int:pk>/delete',
        views.LogicAlertActionDeleteView.as_view(),
        name='logic_alert_action_delete'
    ),

    # Notification Alert Actions

    path(
        'notification_alert_actions',
        views.ShowNotificationAlertActionsView.as_view(),
        name='notification_alert_actions_list'
    ),
    path(
        'notification_alert_action/<int:pk>',
        views.NotificationAlertActionDetailView.as_view(),
        name='notification_alert_action_detail'
    ),
    path(
        'notification_alert_action/create',
        views.NotificationAlertActionCreateView.as_view(),
        name='notification_alert_action_create'
    ),
    path(
        'notification_alert_action/<int:pk>/edit',
        views.NotificationAlertActionUpdateView.as_view(),
        name='notification_alert_action_update'
    ),
    path(
        'notification_alert_action/<int:pk>/delete',
        views.NotificationAlertActionDeleteView.as_view(),
        name='notification_alert_action_delete'
    ),

    # Task Results
    path(
        'alert_action/<str:alert_type>/<int:pk>/results',
        views.TaskResultsListView.as_view(),
        name='task_results'
    ),
]
