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
    from app.astro_engine import _HAS_SWE
    return {
        "status": "ok",
        "version": APP_VERSION,
        "uptime": round(time.time() - _start_time, 2),
        "ai": get_ai_status(),
        "swisseph": _HAS_SWE,
    }


@app.get("/debug/swe-test")
def debug_swe_test():
    """Diagnostic: verify Swiss Ephemeris calculations against known reference."""
    try:
        import swisseph as swe
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        jd = swe.julday(1950, 9, 17, 5.5)  # Sept 17 1950, 05:30 UTC
        ayanamsa = swe.get_ayanamsa(jd)
        sun_pos = swe.calc_ut(jd, swe.SUN)
        sun_trop = sun_pos[0][0]
        sun_sid = (sun_trop - ayanamsa) % 360
        moon_pos = swe.calc_ut(jd, swe.MOON)
        moon_sid = (moon_pos[0][0] - ayanamsa) % 360
        cusps, ascmc = swe.houses(jd, 23.7833, 72.6333, b"P")
        asc_sid = (ascmc[0] - ayanamsa) % 360
        signs = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
        return {
            "engine": "swisseph",
            "version": swe.version,
            "jd": jd,
            "ayanamsa": round(ayanamsa, 6),
            "sun_tropical": round(sun_trop, 4),
            "sun_sidereal": round(sun_sid, 4),
            "sun_sign": signs[int(sun_sid // 30)],
            "sun_degree": round(sun_sid % 30, 4),
            "moon_sidereal": round(moon_sid, 4),
            "moon_sign": signs[int(moon_sid // 30)],
            "ascendant_sidereal": round(asc_sid, 4),
            "ascendant_sign": signs[int(asc_sid // 30)],
            "expected": {"sun": "Virgo 0.59", "moon": "Scorpio 8.81", "asc": "Scorpio 1.25"},
        }
    except Exception as e:
        return {"engine": "error", "detail": str(e)}
