"""Shared rate-limit helpers."""
import os

from fastapi import Request
from slowapi.util import get_remote_address


def request_rate_limit_key(request: Request) -> str:
    """Scope rate limits to the active test DB and client address."""
    db_scope = os.getenv("DB_PATH", "default")
    client_ip = get_remote_address(request) or "unknown"
    return f"{db_scope}:{client_ip}"
