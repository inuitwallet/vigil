import json
from channels.generic.websocket import AsyncWebsocketConsumer


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
        await self.send(text_data=json.dumps({
            'html': event['html']
        }))
