from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/message_listener/', consumers.MessageListenerConsumer.as_asgi()),
    re_path(r'ws/chat_listener/(?P<chat_name>\w+)/$', consumers.ChatListenerConsumer.as_asgi()),
]