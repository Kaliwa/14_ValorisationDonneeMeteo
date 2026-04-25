from __future__ import annotations

from time import perf_counter

from weather.observability import observe_request


class PrometheusMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = perf_counter()
        response = self.get_response(request)
        duration = perf_counter() - start

        route = getattr(getattr(request, "resolver_match", None), "route", None)
        path = route or request.path_info
        observe_request(
            method=request.method,
            path=path,
            status_code=response.status_code,
            duration=duration,
        )
        return response
