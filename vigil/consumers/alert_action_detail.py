import json
from channels.generic.websocket import AsyncWebsocketConsumer


class PreProcessorAlertActionDetailConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join group
        self.group_name = 'preprocessor_alert_action_detail_{}'.format(
            self.scope['url_route']['kwargs']['alert_action_pk']
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
    async def update_action_task_results(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'html': event['html']
        }))


class NotificationAlertActionDetailConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join group
        self.group_name = 'notification_alert_action_detail_{}'.format(
            self.scope['url_route']['kwargs']['alert_action_pk']
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
    async def update_action_task_results(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'html': event['html']
        }))


class LogicAlertActionDetailConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join group
        self.group_name = 'logic_alert_action_detail_{}'.format(
            self.scope['url_route']['kwargs']['alert_action_pk']
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
    async def update_action_task_results(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'html': event['html']
        }))