# routing.py
from django.urls import path
from monitoring_system import consumers

app_name = 'dashboard'

websocket_urlpatterns = [
    path('ws/data/', consumers.DataConsumer.as_asgi(), name='dashboard'),
]

