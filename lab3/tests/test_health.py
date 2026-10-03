from __future__ import annotations

import json
import threading
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path

from app.internal.config.settings import Settings
from app.internal.controller.health import HealthController
from app.internal.repository.health_repository import InMemoryHealthRepository
from app.internal.service.health_service import HealthService
from app.main import create_handler


class HealthTestCase(unittest.TestCase):
    def setUp(self) -> None:
        settings = Settings(
            app_name="Test Library API",
            app_version="9.9.9",
            app_env="test",
            http_host="127.0.0.1",
            http_port=0,
        )
        service = HealthService(settings, InMemoryHealthRepository())
        self.controller = HealthController(service)

    def test_settings_are_loaded_from_dotenv(self) -> None:
        path = Path(self.id().replace(".", "_") + ".env")
        path.write_text("APP_NAME=From file\nHTTP_PORT=9090\n", encoding="utf-8")
        try:
            settings = Settings.from_environment(path)
            self.assertEqual(settings.app_name, "From file")
            self.assertEqual(settings.http_port, 9090)
        finally:
            path.unlink(missing_ok=True)

    def test_service_returns_domain_status(self) -> None:
        status, payload = self.controller.get_health()
        self.assertEqual(status, 200)
        self.assertEqual(payload["status"], "pass")
        self.assertEqual(payload["app_name"], "Test Library API")

    def test_http_endpoint_returns_json(self) -> None:
        server = ThreadingHTTPServer(("127.0.0.1", 0), create_handler(self.controller))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            connection = HTTPConnection("127.0.0.1", server.server_port, timeout=2)
            connection.request("GET", "/api/v1/health")
            response = connection.getresponse()
            payload = json.loads(response.read())
            self.assertEqual(response.status, 200)
            self.assertEqual(response.getheader("Content-Type"), "application/json; charset=utf-8")
            self.assertEqual(payload["environment"], "test")
            connection.close()
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
