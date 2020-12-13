import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class MessageListenerConsumer(WebsocketConsumer):
    def connect(self):

        self.user = self.scope["user"]
        self.listener_name = 'listener_%s' % self.user.id

        async_to_sync(self.channel_layer.group_add)(
            self.listener_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.listener_name,
            self.channel_name
        )

    def receive(self, text_data):
        pass

    def modal_message(self, event):
        self.send(text_data=event["text"])


class ChatListenerConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_name = self.scope['url_route']['kwargs']['chat_name']
        self.chat_group_name = 'chat_%s' % self.chat_name

        async_to_sync(self.channel_layer.group_add)(
            self.chat_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'message': message
        }))