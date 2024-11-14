from django.urls import path
from monitoring_system import consumers  
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/monitor/", consumers.YourConsumer.as_asgi()),  # Replace `YourConsumer` with the actual consumer class name
        ])
    ),
})
