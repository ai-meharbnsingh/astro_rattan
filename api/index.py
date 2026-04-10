"""Vercel serverless entry point — ASGI proxy to the real FastAPI app.

Top-level `from app.main import app` crashes the Vercel Python scanner
(conflicts with the `app/` package directory). This class-based ASGI
wrapper lazy-loads the real app on first request and delegates fully,
preserving all middleware (CORS, security headers, rate limiting).
"""


class _LazyApp:
    """ASGI application that lazy-loads the real FastAPI app."""

    def __init__(self):
        self._real = None

    async def __call__(self, scope, receive, send):
        if self._real is None:
            import importlib
            mod = importlib.import_module("app.main")
            self._real = mod.app
        await self._real(scope, receive, send)


app = _LazyApp()
