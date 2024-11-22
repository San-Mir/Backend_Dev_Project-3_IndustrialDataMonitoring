import json
from django.shortcuts import render

from django.views.generic import TemplateView
from .kafka_service import fetch_kafka_messages

class KafkaDataView(TemplateView):
    template_name = "dashboard/dashboard.html"  # Define the template to render

    def get_context_data(self, **kwargs):
        # Fetch context data for the template
        context = super().get_context_data(**kwargs)
        context['messages'] = json.dumps(fetch_kafka_messages(limit=16))  # Fetch Kafka messages
        print(context['messages'])
        return context


