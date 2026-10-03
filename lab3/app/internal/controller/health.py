"""Transport-facing controller for health checks."""

from __future__ import annotations

from http import HTTPStatus

from app.internal.service.health_service import HealthService


class HealthController:
    def __init__(self, service: HealthService) -> None:
        self._service = service

    def get_health(self) -> tuple[HTTPStatus, dict[str, str]]:
        """Translate a domain health model into a JSON-ready HTTP response."""
        health = self._service.get_health()
        return HTTPStatus.OK, {
            "status": health.status,
            "app_name": health.app_name,
            "version": health.version,
            "environment": health.environment,
        }
