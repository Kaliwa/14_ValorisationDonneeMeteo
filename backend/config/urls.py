"""
Root URL configuration for meteo-api.
"""

from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from weather.observability import render_metrics


def metrics_view(_request):
    return HttpResponse(render_metrics(), content_type="text/plain; version=0.0.4")


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    path("metrics/", metrics_view, name="metrics"),
    # API v1
    path("api/v1/", include("weather.urls")),
    # OpenAPI schema and documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
