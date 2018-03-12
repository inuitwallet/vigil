import json

from channels.generic.websocket import AsyncWebsocketConsumer


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
        await self.send(text_data=json.dumps({
            'message_type': event['message_type'],
            'alert_id': event['alert_id'],
            'html': event['html']
        }))
