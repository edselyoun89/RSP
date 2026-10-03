"""Typed application configuration loaded from .env and the process environment."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _read_dotenv(path: Path) -> dict[str, str]:
    """Read a small dotenv subset without exposing values or requiring a package."""
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def _value(name: str, dotenv: dict[str, str], default: str) -> str:
    return os.environ.get(name, dotenv.get(name, default))


@dataclass(frozen=True, slots=True)
class Settings:
    app_name: str
    app_version: str
    app_env: str
    http_host: str
    http_port: int

    @classmethod
    def from_environment(cls, dotenv_path: Path | None = None) -> "Settings":
        dotenv = _read_dotenv(dotenv_path or Path.cwd() / ".env")
        raw_port = _value("HTTP_PORT", dotenv, "8080")
        try:
            port = int(raw_port)
        except ValueError as exc:
            raise ValueError("HTTP_PORT must be an integer") from exc
        if not 1 <= port <= 65535:
            raise ValueError("HTTP_PORT must be between 1 and 65535")
        return cls(
            app_name=_value("APP_NAME", dotenv, "Library API"),
            app_version=_value("APP_VERSION", dotenv, "1.0.0"),
            app_env=_value("APP_ENV", dotenv, "development"),
            http_host=_value("HTTP_HOST", dotenv, "127.0.0.1"),
            http_port=port,
        )
