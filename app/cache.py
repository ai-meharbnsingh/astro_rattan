"""Simple dict-based TTL cache for expensive calculations.

No external dependencies needed — uses plain dict + time.time().
"""
import time
import threading
from typing import Any, Optional


class TTLCache:
    """Thread-safe dict-based cache with per-entry TTL expiration.

    Args:
        ttl_seconds: Time-to-live for cache entries in seconds.
    """

    def __init__(self, ttl_seconds: int = 3600):
        self._ttl = ttl_seconds
        self._store: dict[str, tuple[float, Any]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        """Return cached value if present and not expired, else None."""
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            expires_at, value = entry
            if time.time() > expires_at:
                del self._store[key]
                return None
            return value

    def set(self, key: str, value: Any) -> None:
        """Store a value with TTL starting from now."""
        with self._lock:
            self._store[key] = (time.time() + self._ttl, value)

    def clear(self) -> None:
        """Remove all entries."""
        with self._lock:
            self._store.clear()


# Pre-configured cache instances
# Panchang: 1 hour TTL (calculations are date+location dependent)
panchang_cache = TTLCache(ttl_seconds=3600)

# Horoscope: 6 hours TTL (sign+period dependent)
horoscope_cache = TTLCache(ttl_seconds=21600)
