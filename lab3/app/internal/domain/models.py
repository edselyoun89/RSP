"""Transport-independent domain data structures."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HealthStatus:
    status: str
    app_name: str
    version: str
    environment: str
