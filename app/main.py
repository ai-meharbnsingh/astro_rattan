"""AstroVedic — FastAPI application entry point."""
import os
import time
from contextlib import asynccontextmanager

# Sentry — initialize before FastAPI if DSN is set
_sentry_dsn = os.getenv("SENTRY_DSN", "")
if _sentry_dsn:
    import sentry_sdk
    sentry_sdk.init(dsn=_sentry_dsn, traces_sample_rate=0.1, profiles_sample_rate=0.1)

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import APP_NAME, APP_VERSION, CORS_ORIGINS, CORS_ORIGIN_REGEX, RATE_LIMIT_PER_MINUTE
from app.database import init_db
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
    """Initialize database and run migrations on startup. Heavy seeding runs in background."""
    import threading
    init_db()
    run_migrations()
    # Heavy work in background so health check passes quickly
    def _background_init():
        try:
            seed_all()
            generate_daily_horoscopes()
            seed_weekly_horoscopes()
        except Exception as e:
            print(f"[startup] Background init error: {e}")
    threading.Thread(target=_background_init, daemon=True).start()
    yield
    # Graceful shutdown — close connection pool
    from app.database import _get_pool
    try:
        _get_pool().closeall()
    except Exception:
        pass


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
    allow_origin_regex=CORS_ORIGIN_REGEX,
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
    """Health check endpoint with DB verification."""
    from app.astro_engine import _HAS_SWE
    from app.config import AI_PROVIDER, GEMINI_API_KEY, OPENAI_API_KEY
    ai_status = "configured" if (GEMINI_API_KEY or OPENAI_API_KEY) else "not_configured"
    db_ok = False
    try:
        from app.database import _get_pool
        pool = _get_pool()
        conn = pool.getconn()
        conn.cursor().execute("SELECT 1")
        pool.putconn(conn)
        db_ok = True
    except Exception:
        pass
    return {
        "status": "ok" if db_ok else "degraded",
        "version": APP_VERSION,
        "uptime": round(time.time() - _start_time, 2),
        "database": "connected" if db_ok else "unreachable",
        "ai": {"provider": AI_PROVIDER, "status": ai_status},
        "swisseph": _HAS_SWE,
    }




# Debug endpoints removed — security risk in production (Gemini audit finding #1)
