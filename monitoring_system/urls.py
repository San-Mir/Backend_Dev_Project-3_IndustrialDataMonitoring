from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/admin/")),  # Redirect root URL to admin
    path("admin/", admin.site.urls),
    path("dashboard/", include("dashboard.urls")), 
]
