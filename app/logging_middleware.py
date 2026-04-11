"""H-01: Structured Logging Middleware — logs every request with method, path, status, duration, user_id.
Also maintains an in-memory circular buffer for the live admin dashboard panel.
"""
import logging
import time
import threading
from collections import deque, Counter
from typing import Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.auth import decode_token

logger = logging.getLogger("astrorattan.access")

# Configure structured log format
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter(
    "[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
))
if not logger.handlers:
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)

# ── In-memory traffic store (per worker process) ─────────────────────────────
_lock = threading.Lock()
_recent_requests: deque = deque(maxlen=500)      # last 500 requests
_active_users: dict = {}                          # user_id → {last_seen, last_path}
_server_start: float = time.time()               # process start time

# Paths to exclude from the live activity feed (too noisy)
_SKIP_PATHS = {"/health", "/", "/api/admin/live", "/favicon.ico"}


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
    """Middleware that logs every HTTP request and records to the live traffic buffer."""

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        user_id = _extract_user_id(request)

        response: Response = await call_next(request)

        duration_ms = round((time.perf_counter() - start) * 1000, 1)
        path = request.url.path

        logger.info(
            "%s %s → %s (%sms) user=%s",
            request.method,
            path,
            response.status_code,
            duration_ms,
            user_id or "anon",
        )

        # Record to live traffic buffer (skip noisy internal paths)
        if path not in _SKIP_PATHS and not path.startswith("/static"):
            entry = {
                "ts": time.time(),
                "method": request.method,
                "path": path,
                "status": response.status_code,
                "duration_ms": duration_ms,
                "user_id": user_id,
                "is_error": response.status_code >= 400,
            }
            with _lock:
                _recent_requests.append(entry)
                if user_id:
                    _active_users[user_id] = {
                        "last_seen": time.time(),
                        "last_path": path,
                    }

        return response


def get_traffic_snapshot() -> dict:
    """Return a snapshot of recent traffic for the live admin dashboard.
    Thread-safe — copies data under lock before processing."""
    now = time.time()

    with _lock:
        reqs = list(_recent_requests)
        # Only keep users seen in the last 5 minutes
        active = {
            uid: dict(v)
            for uid, v in _active_users.items()
            if now - v["last_seen"] < 300
        }

    one_min_ago = now - 60
    five_min_ago = now - 300

    reqs_1m = [r for r in reqs if r["ts"] >= one_min_ago]
    reqs_5m = [r for r in reqs if r["ts"] >= five_min_ago]
    errors_1m = [r for r in reqs_1m if r["is_error"]]

    # Top endpoints by hit count in the last 5 minutes
    endpoint_counts = Counter(r["path"] for r in reqs_5m)
    endpoint_durations: dict = {}
    for r in reqs_5m:
        endpoint_durations.setdefault(r["path"], []).append(r["duration_ms"])

    top_endpoints = [
        {
            "path": path,
            "count": count,
            "avg_ms": round(sum(endpoint_durations[path]) / len(endpoint_durations[path]), 1),
        }
        for path, count in endpoint_counts.most_common(10)
    ]

    # Most recent 50 requests for the activity feed
    recent_50 = list(reversed(reqs))[:50]

    error_rate = round(len(errors_1m) / max(len(reqs_1m), 1) * 100, 1)

    return {
        "active_user_ids": list(active.keys()),
        "active_user_details": active,
        "requests_1m": len(reqs_1m),
        "requests_5m": len(reqs_5m),
        "error_rate_1m": error_rate,
        "top_endpoints": top_endpoints,
        "recent_activity": recent_50,
        "uptime_seconds": int(now - _server_start),
    }
