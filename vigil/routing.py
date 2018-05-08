from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from vigil import consumers

websocket_urlpatterns = [
    url(
        r'^alert_list/$',
        consumers.AlertListConsumer
    ),
    url(
        r'^alert_detail/(?P<alert_channel_pk>[^/]+)/$',
        consumers.AlertDetailConsumer
    ),
    url(
        r'^preprocessor_alert_action_detail/(?P<alert_action_pk>[^/]+)/$',
        consumers.PreProcessorAlertActionDetailConsumer
    ),
    url(
        r'^notification_alert_action_detail/(?P<alert_action_pk>[^/]+)/$',
        consumers.NotificationAlertActionDetailConsumer
    ),
    url(
        r'^logic_alert_action_detail/(?P<alert_action_pk>[^/]+)/$',
        consumers.LogicAlertActionDetailConsumer
    ),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
