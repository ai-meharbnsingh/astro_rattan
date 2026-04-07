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
from app.database import init_db, migrate_users_table, migrate_referral_tables, migrate_forum_tables, migrate_gamification_tables, migrate_notification_tables
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
    migrate_referral_tables()
    migrate_forum_tables()
    migrate_gamification_tables()
    migrate_notification_tables()
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

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    if not request.url.path.startswith("/debug"):
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# H-01: Structured request logging middleware (after CORS)
from app.logging_middleware import RequestLoggingMiddleware  # noqa: E402
app.add_middleware(RequestLoggingMiddleware)

# Include all routers
for router in all_routers:
    app.include_router(router)

# Static file serving for uploaded images
from app.config import STATIC_DIR
os.makedirs(os.path.join(STATIC_DIR, "uploads"), exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def root():
    """Root endpoint — API welcome."""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    """Health check endpoint."""
    from app.ai_engine import get_ai_status
    from app.astro_engine import _HAS_SWE
    return {
        "status": "ok",
        "version": APP_VERSION,
        "uptime": round(time.time() - _start_time, 2),
        "ai": get_ai_status(),
        "swisseph": _HAS_SWE,
    }




# Debug endpoints removed — security risk in production (Gemini audit finding #1)
