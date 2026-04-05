"""Vercel serverless entry point — exposes the FastAPI app."""
import traceback
from fastapi import FastAPI

app = None
_startup_error = None

try:
    from app.main import app as _real_app
    app = _real_app
except Exception:
    _startup_error = traceback.format_exc()

if app is None:
    app = FastAPI()

    @app.get("/{path:path}")
    def diagnostic(path: str = ""):
        return {"error": "App failed to start", "traceback": _startup_error}
