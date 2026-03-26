"""H-01: Structured Logging Middleware — logs every request with method, path, status, duration, user_id."""
import logging
import time
from typing import Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.auth import decode_token

logger = logging.getLogger("astrovedic.access")

# Configure structured log format
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter(
    "[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
))
if not logger.handlers:
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)


def _extract_user_id(request: Request) -> Optional[str]:
    """Extract user_id from JWT Bearer token if present."""
    auth_header = request.headers.get("authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]
        payload = decode_token(token)
        if payload:
            return payload.get("sub")
    return None


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware that logs every HTTP request with structured fields."""

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        user_id = _extract_user_id(request)

        response: Response = await call_next(request)

        duration_ms = round((time.perf_counter() - start) * 1000, 1)
        logger.info(
            "%s %s → %s (%sms) user=%s",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            user_id or "anon",
        )

        return response
