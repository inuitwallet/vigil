import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string

from vigil.models import AlertChannel, Alert


class AlertListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join group
        await self.channel_layer.group_add(
            'alert_list',
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'alert_list',
            self.channel_name
        )

    # Receive message from room group
    async def update_alert_list(self, event):
        # Send message to WebSocket
        alert = await self.get_alert(event['alert'])

        # html needs to be rendered here in order to
        # correctly determine if the viewing user is authenticated
        await self.send(text_data=json.dumps({
            'message_type': event['message_type'],
            'alert': event['alert'],
            'html': render_to_string(
                'vigil/fragments/alert.html',
                {
                    'alert': alert,
                    'user': self.scope['user']
                }
            )
        }))

    @database_sync_to_async
    def get_alert(self, alert_pk):
        return Alert.objects.get(pk=alert_pk)
