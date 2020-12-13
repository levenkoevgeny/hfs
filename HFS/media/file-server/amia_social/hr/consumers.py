import json
from channels.generic.websocket import AsyncWebsocketConsumer


class HRConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'hr'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        pass
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        #
        # # Send message to room group
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': message
        #     }
        # )

    # Receive message from room group
    async def hr_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=message)
