from __future__ import annotations

from collections import Counter, defaultdict
from threading import Lock
from time import perf_counter

from weather.models import HoraireTempsReel, Quotidienne, Station

_METRICS_LOCK = Lock()
_APP_START = perf_counter()
_REQUEST_COUNTER: Counter[tuple[str, str, str]] = Counter()
_REQUEST_DURATION_SUM: defaultdict[tuple[str, str], float] = defaultdict(float)
_REQUEST_DURATION_COUNT: Counter[tuple[str, str]] = Counter()
_REQUEST_DURATION_BUCKETS: defaultdict[tuple[str, str], Counter[float]] = defaultdict(
    Counter
)
_HISTOGRAM_BUCKETS = (0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0)


def _escape_label_value(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def _labels(**values: str) -> str:
    return ",".join(
        f'{key}="{_escape_label_value(value)}"' for key, value in values.items()
    )


def observe_request(method: str, path: str, status_code: int, duration: float) -> None:
    status = str(status_code)
    request_key = (method, path, status)
    duration_key = (method, path)

    with _METRICS_LOCK:
        _REQUEST_COUNTER[request_key] += 1
        _REQUEST_DURATION_SUM[duration_key] += duration
        _REQUEST_DURATION_COUNT[duration_key] += 1

        for bucket in _HISTOGRAM_BUCKETS:
            if duration <= bucket:
                _REQUEST_DURATION_BUCKETS[duration_key][bucket] += 1


def render_metrics() -> str:
    with _METRICS_LOCK:
        request_counter = dict(_REQUEST_COUNTER)
        request_duration_sum = dict(_REQUEST_DURATION_SUM)
        request_duration_count = dict(_REQUEST_DURATION_COUNT)
        request_duration_buckets = {
            key: dict(bucket_counts)
            for key, bucket_counts in _REQUEST_DURATION_BUCKETS.items()
        }

    stations_total = Station.objects.count()
    hourly_measurements_total = HoraireTempsReel.objects.count()
    daily_measurements_total = Quotidienne.objects.count()
    uptime_seconds = perf_counter() - _APP_START

    lines = [
        "# HELP meteo_observability_uptime_seconds Application uptime in seconds.",
        "# TYPE meteo_observability_uptime_seconds gauge",
        f"meteo_observability_uptime_seconds {uptime_seconds:.6f}",
        "# HELP meteo_stations_total Total weather stations available.",
        "# TYPE meteo_stations_total gauge",
        f"meteo_stations_total {stations_total}",
        "# HELP meteo_hourly_measurements_total Total hourly measurements stored.",
        "# TYPE meteo_hourly_measurements_total gauge",
        f"meteo_hourly_measurements_total {hourly_measurements_total}",
        "# HELP meteo_daily_measurements_total Total daily measurements stored.",
        "# TYPE meteo_daily_measurements_total gauge",
        f"meteo_daily_measurements_total {daily_measurements_total}",
        "# HELP meteo_http_requests_total Total HTTP requests observed by Django.",
        "# TYPE meteo_http_requests_total counter",
    ]

    for (method, path, status), count in sorted(request_counter.items()):
        lines.append(
            f"meteo_http_requests_total{{{_labels(method=method, path=path, status=status)}}} {count}"
        )

    lines.extend(
        [
            "# HELP meteo_http_request_duration_seconds Request duration histogram.",
            "# TYPE meteo_http_request_duration_seconds histogram",
        ]
    )

    for (method, path), count in sorted(request_duration_count.items()):
        bucket_counts = request_duration_buckets.get((method, path), {})

        for bucket in _HISTOGRAM_BUCKETS:
            lines.append(
                "meteo_http_request_duration_seconds_bucket"
                f"{{{_labels(method=method, path=path, le=str(bucket))}}} {bucket_counts.get(bucket, 0)}"
            )

        lines.append(
            "meteo_http_request_duration_seconds_bucket"
            f"{{{_labels(method=method, path=path, le='+Inf')}}} {count}"
        )
        lines.append(
            "meteo_http_request_duration_seconds_sum"
            f"{{{_labels(method=method, path=path)}}} {request_duration_sum[(method, path)]:.6f}"
        )
        lines.append(
            "meteo_http_request_duration_seconds_count"
            f"{{{_labels(method=method, path=path)}}} {count}"
        )

    lines.append("")
    return "\n".join(lines)
