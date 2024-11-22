import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack  # For handling WebSocket authentication
from dashboard.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoring_system.settings')

# Configure the ASGI application
application = ProtocolTypeRouter(
    {
        # Handle HTTP requests
        "http": get_asgi_application(),
        
        # Handle WebSocket connections
        "websocket": AuthMiddlewareStack(  # Add authentication middleware for WebSockets
            URLRouter(
                websocket_urlpatterns  # Include WebSocket routing patterns
            )
        ),
    }
)
