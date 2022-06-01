"""
ASGI config for Connect project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from users import consumers

from django.urls import re_path, path

# import stories.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [path('stories/notification_testing/', consumers.NotificationConsumer.as_asgi())]
        ))

})

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Connect.settings')

# application = get_asgi_application()
