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
        self._initialized = False

    async def __call__(self, scope, receive, send):
        if self._real is None:
            import importlib
            mod = importlib.import_module("app.main")
            self._real = mod.app
        if not self._initialized:
            from app.database import init_db
            from app.migrations import run_migrations
            try:
                init_db()
                run_migrations()
            except Exception as e:
                print(f"[LazyApp] DB init error: {e}")
            self._initialized = True
        await self._real(scope, receive, send)


app = _LazyApp()
