from __future__ import annotations

import os
import subprocess
import sys


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def main() -> None:
    venv_bin = "/app/.venv/bin"
    python_bin = f"{venv_bin}/python"
    gunicorn_bin = f"{venv_bin}/gunicorn"

    print("Applying database migrations...", flush=True)
    run([python_bin, "manage.py", "migrate", "--noinput"])

    print("Collecting static files...", flush=True)
    run([python_bin, "manage.py", "collectstatic", "--noinput"])

    os.execv(
        gunicorn_bin,
        [
            gunicorn_bin,
            "config.wsgi:application",
            "--bind",
            "0.0.0.0:8000",
        ],
    )


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
