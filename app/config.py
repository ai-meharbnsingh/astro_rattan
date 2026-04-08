"""Application configuration — loaded from environment variables with defaults."""
import os

# Load .env file if present (development convenience)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed — rely on OS env vars


def _env_first(*names: str, default: str = "") -> str:
    """Return the first non-empty environment variable from the given names."""
    for name in names:
        value = os.getenv(name, "")
        if value:
            return value
    return default

# Database
DB_PATH = os.getenv("DB_PATH", "astrovedic.db")

# Auth
JWT_SECRET = os.getenv("JWT_SECRET", "")
if not JWT_SECRET:
    if os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RENDER") or os.getenv("FLY_APP_NAME"):
        raise RuntimeError("FATAL: JWT_SECRET env var is required in production. Set it and redeploy.")
    import secrets
    JWT_SECRET = secrets.token_hex(32)
    print("[WARNING] JWT_SECRET not set — using random secret (dev only).")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24

# Ports
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8028"))
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "5198"))

# AI Provider: "gemini" or "openai" (auto-detects from which key is set)
AI_PROVIDER = os.getenv("AI_PROVIDER", "auto")  # auto | gemini | openai

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

# Google Gemini (free tier available)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")


# Frontend URL (used in payment redirect URLs)
FRONTEND_URL = os.getenv("FRONTEND_URL", f"http://localhost:{FRONTEND_PORT}")
SITE_URL = _env_first("SITE_URL", default="https://astrorattan.com")

# Static files directory
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")

# App
APP_VERSION = "1.0.0"
APP_NAME = "AstroVedic"
TESTING = _env_first("TESTING", default="").lower() in {"1", "true", "yes", "on"}

# CORS - Explicit domains only (no wildcards — security hardening)
_default_cors = f"http://localhost:{FRONTEND_PORT},https://astrorattan.com,https://www.astrorattan.com"
_env_cors = os.getenv("CORS_ORIGINS", _default_cors)
CORS_ORIGINS = _env_cors.split(",")

# Always ensure production URLs are included
_production_urls = [
    "https://astrorattan.com",
    "https://www.astrorattan.com",
    "https://astrorattan-web.vercel.app",
    f"http://localhost:{FRONTEND_PORT}",
]
for url in _production_urls:
    if url not in CORS_ORIGINS:
        CORS_ORIGINS.append(url)
# Allow Vercel preview deployments (*.vercel.app)
CORS_ORIGIN_REGEX = r"https://astrorattan-.*\.vercel\.app"

# Swiss Ephemeris
EPHE_PATH = os.getenv("EPHE_PATH", "")  # Path to ephemeris data files

# SMTP / Email (graceful degradation — if not set, emails are logged and skipped)
SMTP_HOST = _env_first("SMTP_HOST", "EMAIL_SMTP_HOST")
SMTP_PORT = int(_env_first("SMTP_PORT", "EMAIL_SMTP_PORT", default="587"))
SMTP_USER = _env_first("SMTP_USER", "EMAIL_USERNAME")
SMTP_PASSWORD = _env_first("SMTP_PASSWORD", "EMAIL_PASSWORD")
FROM_EMAIL = _env_first("FROM_EMAIL", "EMAIL_FROM")
EMAIL_TO = _env_first("EMAIL_TO", "NOTIFICATION_EMAIL_TO")

# Rate limiting
RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
LOGIN_RATE_LIMIT = _env_first("LOGIN_RATE_LIMIT", default="5/minute")
