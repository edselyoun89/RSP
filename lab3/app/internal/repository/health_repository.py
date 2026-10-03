"""Repository abstraction for technical service state."""

from __future__ import annotations

from typing import Protocol


class HealthRepository(Protocol):
    def is_alive(self) -> bool:
        """Return whether the application process is able to serve requests."""


class InMemoryHealthRepository:
    """Local adapter used by this bootstrap project."""

    def is_alive(self) -> bool:
        return True
