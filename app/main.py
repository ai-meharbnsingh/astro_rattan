"""AstroVedic — FastAPI application entry point."""
import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import APP_NAME, APP_VERSION, CORS_ORIGINS, RATE_LIMIT_PER_MINUTE
from app.database import init_db, migrate_users_table
from app.migrations import run_migrations
from app.rate_limit import request_rate_limit_key
from app.seed_data import seed_all
from app.horoscope_generator import generate_daily_horoscopes, seed_weekly_horoscopes
from app.routes import all_routers

_start_time = time.time()

# Rate limiter — keyed by client IP
limiter = Limiter(
    key_func=request_rate_limit_key,
    default_limits=[f"{RATE_LIMIT_PER_MINUTE}/minute"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database, run migrations, seed data, and generate horoscopes on startup."""
    init_db()
    migrate_users_table()
    run_migrations()
    seed_all()
    generate_daily_horoscopes()
    seed_weekly_horoscopes()
    yield


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    lifespan=lifespan,
)

# Attach limiter to app state (required by slowapi)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# H-01: Structured request logging middleware (after CORS)
from app.logging_middleware import RequestLoggingMiddleware  # noqa: E402
app.add_middleware(RequestLoggingMiddleware)

# Include all routers
for router in all_routers:
    app.include_router(router)

# Static file serving for uploaded images
_static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
os.makedirs(os.path.join(_static_dir, "uploads"), exist_ok=True)
app.mount("/static", StaticFiles(directory=_static_dir), name="static")


@app.get("/health")
def health():
    """Health check endpoint."""
    from app.ai_engine import get_ai_status
    return {
        "status": "ok",
        "version": APP_VERSION,
        "uptime": round(time.time() - _start_time, 2),
        "ai": get_ai_status(),
    }
