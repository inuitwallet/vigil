import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string

from vigil.models import AlertChannel


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
        alert_channel = await self.get_alert_channel(event['alert_id'])

        await self.send(text_data=json.dumps({
            'message_type': event['message_type'],
            'alert_id': event['alert_id'],
            'html': render_to_string(
                'vigil/fragments/alert_channel.html',
                {
                    'alert': alert_channel,
                    'user': self.scope['user']
                }
            )
        }))

    @database_sync_to_async
    def get_alert_channel(self, alert_id):
        return AlertChannel.objects.get(alert_id=alert_id)
