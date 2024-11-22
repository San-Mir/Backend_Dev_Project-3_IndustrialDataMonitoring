from django.urls import path
from .views import KafkaDataView

urlpatterns = [
    path('', KafkaDataView.as_view(), name='kafka_messages'),
]
