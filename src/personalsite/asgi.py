import django
from django.core.handlers.asgi import ASGIHandler
from channels.routing import ProtocolTypeRouter, URLRouter

import os
from newsreader.urls import urlpatterns
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "personalsite.settings")

from channels.routing import ProtocolTypeRouter
# from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
     "websocket": 
        URLRouter(
            urlpatterns)
})