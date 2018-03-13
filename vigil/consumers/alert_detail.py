import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string

from vigil.models import AlertChannel, HistoricalAlert


class AlertDetailConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join group
        self.group_name = 'alert_detail_{}'.format(
                self.scope['url_route']['kwargs']['alert_channel_pk']
            )
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from room group
    async def update_historical_alerts(self, event):
        # Send message to WebSocket
        historical_alert = await self.get_historical_alert(event['historical_alert_pk'])

        await self.send(text_data=json.dumps({
            'html': render_to_string(
                'vigil/fragments/historical_alert.html',
                {
                    'historical_alert': historical_alert,
                }
            )
        }))

    @database_sync_to_async
    def get_historical_alert(self, pk):
        return HistoricalAlert.objects.get(pk=pk)
