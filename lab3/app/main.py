"""Application entry point and HTTP transport adapter."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from app.internal.config.settings import Settings
from app.internal.controller.health import HealthController
from app.internal.repository.health_repository import InMemoryHealthRepository
from app.internal.service.health_service import HealthService


def build_controller(settings: Settings) -> HealthController:
    """Compose concrete adapters at the application boundary."""
    repository = InMemoryHealthRepository()
    service = HealthService(settings=settings, repository=repository)
    return HealthController(service=service)


def create_handler(controller: HealthController) -> type[BaseHTTPRequestHandler]:
    """Create a request handler that delegates work to the controller."""

    class LibraryRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
            if self.path.split("?", 1)[0] in {"/health", "/api/v1/health"}:
                status, payload = controller.get_health()
                self._send_json(status, payload)
                return
            self._send_json(HTTPStatus.NOT_FOUND, {"code": "NOT_FOUND", "message": "Route not found"})

        def _send_json(self, status: HTTPStatus | int, payload: dict[str, Any]) -> None:
            encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(int(status))
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

        def log_message(self, format: str, *args: Any) -> None:
            print(f"[http] {self.address_string()} - {format % args}")

    return LibraryRequestHandler


def main() -> None:
    settings = Settings.from_environment()
    controller = build_controller(settings)
    server = ThreadingHTTPServer((settings.http_host, settings.http_port), create_handler(controller))
    print(f"{settings.app_name} {settings.app_version} listening on http://{settings.http_host}:{settings.http_port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
