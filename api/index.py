"""Vercel serverless entry point — exposes the FastAPI app."""
import traceback

try:
    from app.main import app  # noqa: F401
except Exception:
    # If the main app fails to load, serve a diagnostic app so we can see the error
    from fastapi import FastAPI
    app = FastAPI()

    _error = traceback.format_exc()

    @app.get("/{path:path}")
    def diagnostic(path: str = ""):
        return {"error": "App failed to start", "traceback": _error}
