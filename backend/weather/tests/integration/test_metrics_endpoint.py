from __future__ import annotations

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from weather.factories.weather import (
    HoraireTempsReelFactory,
    QuotidienneFactory,
    StationFactory,
)

pytestmark = pytest.mark.django_db


def test_metrics_endpoint_exposes_prometheus_text_payload():
    station = StationFactory()
    HoraireTempsReelFactory(station=station)
    QuotidienneFactory(station=station)

    client = APIClient()
    response = client.get(reverse("metrics"))

    assert response.status_code == 200
    assert response["Content-Type"].startswith("text/plain")

    body = response.content.decode()
    assert "meteo_stations_total" in body
    assert "meteo_hourly_measurements_total" in body
    assert "meteo_daily_measurements_total" in body
    assert 'meteo_http_requests_total{method="GET",path="metrics/",status="200"}' in body
