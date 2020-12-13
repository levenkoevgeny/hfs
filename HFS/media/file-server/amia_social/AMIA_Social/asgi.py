"""
ASGI config for AMIA_Social project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

# import os
#
# from django.core.asgi import get_asgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AMIA_Social.settings')
#
# application = get_asgi_application()


import os

from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import hr.routing
import messaging.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AMIA_Social.settings')

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            hr.routing.websocket_urlpatterns +
            messaging.routing.websocket_urlpatterns
        )
    ),
})
