import os
from django.urls import path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from dashboard.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoring_system.settings')

application = ProtocolTypeRouter(
        {
            "http": get_asgi_application(),
            "websocket": URLRouter(websocket_urlpatterns)
        }
)
