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

    # Alerts UI
    # Show
    path(
        '',
        views.ShowActiveAlertsView.as_view(),
        name='alert_list'
    ),
    path(
        'all_alerts',
        views.ShowAllAlertsView.as_view(),
        name='all_alert_list'
    ),
    path(
        'alert_actions',
        views.ShowAllAlertActionsView.as_view(),
        name='all_alert_actions_list'
    ),

    # Create

    # Edit
    path(
        'alert/<int:pk>/edit',
        views.AlertChannelUpdateView.as_view(),
        name='alert_update'
    ),
    path(
        'alert_action/<int:pk>/edit',
        views.AlertActionUpdateView.as_view(),
        name='alert_action_update'
    )
]
