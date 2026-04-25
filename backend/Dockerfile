FROM dhi.io/python:3.12-dev AS build

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_NO_DEV=1

COPY --from=ghcr.io/astral-sh/uv:0.10.0 /uv /uvx /bin/

COPY . .
RUN uv sync --locked

FROM dhi.io/python:3.12

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --from=build /app /app

EXPOSE 8000
CMD ["/app/.venv/bin/python", "container_entrypoint.py"]
