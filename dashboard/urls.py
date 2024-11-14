from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),  # Add a path for the dashboard view
]
