"""Health-check use case independent from HTTP and JSON."""

from __future__ import annotations

from app.internal.config.settings import Settings
from app.internal.domain.models import HealthStatus
from app.internal.repository.health_repository import HealthRepository


class HealthService:
    def __init__(self, settings: Settings, repository: HealthRepository) -> None:
        self._settings = settings
        self._repository = repository

    def get_health(self) -> HealthStatus:
        status = "pass" if self._repository.is_alive() else "fail"
        return HealthStatus(
            status=status,
            app_name=self._settings.app_name,
            version=self._settings.app_version,
            environment=self._settings.app_env,
        )
