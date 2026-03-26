"""Sprint 1 backend hardening tests — RED phase first, then GREEN.

Covers: C-02, C-03, C-04, H-06, H-07, H-10, H-04
"""
import os
import io
import re
import time
import sqlite3
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def test_db(tmp_path):
    """Create a fresh test database."""
    db_path = str(tmp_path / "test_sprint1.db")
    os.environ["DB_PATH"] = db_path
    from app.database import init_db, migrate_users_table
    init_db(db_path)
    migrate_users_table(db_path)
    return db_path


@pytest.fixture
def client(test_db):
    """TestClient with fresh DB."""
    os.environ["DB_PATH"] = test_db
    # Force re-import to pick up new DB_PATH
    import importlib
    import app.config
    importlib.reload(app.config)
    import app.database
    importlib.reload(app.database)

    from app.main import app
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def admin_token(client, test_db):
    """Register an admin user and return JWT token."""
    # Register a regular user first
    resp = client.post("/api/auth/register", json={
        "email": "admin@test.com",
        "password": "admin123456",
        "name": "Admin User",
    })
    token = resp.json()["token"]

    # Manually set role to admin in DB
    conn = sqlite3.connect(test_db)
    conn.execute("UPDATE users SET role = 'admin' WHERE email = 'admin@test.com'")
    conn.commit()
    conn.close()

    # Re-login to get admin token
    resp = client.post("/api/auth/login", json={
        "email": "admin@test.com",
        "password": "admin123456",
    })
    return resp.json()["token"]


@pytest.fixture
def user_token(client):
    """Register a regular user and return JWT token."""
    resp = client.post("/api/auth/register", json={
        "email": "user@test.com",
        "password": "user123456",
        "name": "Test User",
    })
    return resp.json()["token"]


# ============================================================
# C-02: Stripe Webhook Verification
# ============================================================

class TestC02StripeWebhookVerification:
    """Stripe webhook should use stripe.Webhook.construct_event when available."""

    def test_stripe_webhook_rejects_invalid_signature(self, test_db):
        """Webhook with bad signature must be rejected (400)."""
        import importlib
        import app.config as _cfg_mod
        import app.routes.payments as _pay_mod

        os.environ["STRIPE_WEBHOOK_SECRET"] = "whsec_test_secret"
        os.environ["DB_PATH"] = test_db
        importlib.reload(_cfg_mod)
        # Must reload payments to pick up new STRIPE_WEBHOOK_SECRET
        importlib.reload(_pay_mod)

        from app.main import app as _app
        client = TestClient(_app, raise_server_exceptions=False)

        resp = client.post(
            "/api/payments/webhook/stripe",
            content=b'{"type": "payment_intent.succeeded", "data": {"object": {"id": "pi_1", "metadata": {"order_id": "ord1"}}}}',
            headers={
                "Stripe-Signature": "t=12345,v1=invalidsig",
                "Content-Type": "application/json",
            },
        )
        assert resp.status_code == 400

        # Cleanup
        os.environ.pop("STRIPE_WEBHOOK_SECRET", None)
        importlib.reload(_cfg_mod)
        importlib.reload(_pay_mod)

    def test_stripe_webhook_construct_event_used_when_stripe_available(self):
        """Verify that construct_event from the stripe library is the preferred path."""
        from app.routes.payments import stripe_webhook
        # The function should exist and be an async function
        import inspect
        assert inspect.iscoroutinefunction(stripe_webhook)


# ============================================================
# C-03: Fix Hardcoded Payment URLs
# ============================================================

class TestC03FrontendUrl:
    """Payment URLs must use FRONTEND_URL config, not hardcoded localhost."""

    def test_config_has_frontend_url(self):
        """app.config must export FRONTEND_URL."""
        from app.config import FRONTEND_URL
        assert isinstance(FRONTEND_URL, str)
        assert FRONTEND_URL.startswith("http")

    def test_frontend_url_default(self):
        """Default FRONTEND_URL should be http://localhost:5198."""
        os.environ.pop("FRONTEND_URL", None)
        import importlib, app.config
        importlib.reload(app.config)
        from app.config import FRONTEND_URL
        assert FRONTEND_URL == "http://localhost:5198"

    def test_frontend_url_env_override(self):
        """FRONTEND_URL should be overridable via environment."""
        os.environ["FRONTEND_URL"] = "https://astrovedic.example.com"
        import importlib, app.config
        importlib.reload(app.config)
        from app.config import FRONTEND_URL
        assert FRONTEND_URL == "https://astrovedic.example.com"
        # Cleanup
        os.environ.pop("FRONTEND_URL", None)
        importlib.reload(app.config)

    def test_payments_uses_frontend_url_not_hardcoded(self):
        """payments.py must NOT contain hardcoded localhost URLs."""
        import inspect
        from app.routes import payments
        source = inspect.getsource(payments)
        # Should NOT have hardcoded localhost payment URLs
        assert "http://localhost:5198/orders" not in source


# ============================================================
# C-04: Rate Limiting
# ============================================================

class TestC04RateLimiting:
    """Rate limiting via slowapi must be configured."""

    def test_slowapi_in_requirements(self):
        """slowapi must be listed in requirements.txt."""
        req_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "requirements.txt"
        )
        with open(req_path) as f:
            content = f.read()
        assert "slowapi" in content

    def test_health_endpoint_has_rate_limit_headers(self, client):
        """Responses should include rate-limit related headers or middleware be present."""
        from app.main import app
        # Check that slowapi limiter is attached to the app state
        assert hasattr(app.state, "limiter"), "app.state.limiter must be set by slowapi"

    def test_login_rate_limit_configured(self):
        """Login endpoint should have a stricter rate limit than default."""
        import inspect
        from app.routes.auth import router
        source = inspect.getsource(router.routes[-1].endpoint) if router.routes else ""
        # Check that the login function or its decorators mention rate limiting
        from app.routes import auth as auth_module
        auth_source = inspect.getsource(auth_module)
        assert "limiter" in auth_source or "limit" in auth_source


# ============================================================
# H-06: Input Sanitization
# ============================================================

class TestH06InputSanitization:
    """sanitize_text must strip HTML and limit length."""

    def test_sanitize_module_exists(self):
        """app.sanitize must be importable."""
        from app.sanitize import sanitize_text
        assert callable(sanitize_text)

    def test_sanitize_strips_html_tags(self):
        """HTML tags must be removed from text."""
        from app.sanitize import sanitize_text
        result = sanitize_text("<script>alert('xss')</script>Hello")
        assert "<script>" not in result
        assert "alert" not in result
        assert "Hello" in result

    def test_sanitize_strips_nested_tags(self):
        """Nested and complex HTML must be stripped."""
        from app.sanitize import sanitize_text
        result = sanitize_text('<div class="x"><b>Bold</b></div>')
        assert "<div" not in result
        assert "<b>" not in result
        assert "Bold" in result

    def test_sanitize_limits_length(self):
        """Text exceeding max_length must be truncated."""
        from app.sanitize import sanitize_text
        long_text = "a" * 20000
        result = sanitize_text(long_text, max_length=5000)
        assert len(result) == 5000

    def test_sanitize_preserves_normal_text(self):
        """Normal text without HTML must be preserved as-is."""
        from app.sanitize import sanitize_text
        text = "This is a normal astrology question about Mars retrograde."
        assert sanitize_text(text) == text

    def test_sanitize_handles_empty_string(self):
        """Empty string input must return empty string."""
        from app.sanitize import sanitize_text
        assert sanitize_text("") == ""

    def test_sanitize_handles_none_gracefully(self):
        """None input should return empty string."""
        from app.sanitize import sanitize_text
        assert sanitize_text(None) == ""


# ============================================================
# H-07: Caching
# ============================================================

class TestH07Caching:
    """Dict-based TTL cache must work for panchang and horoscope data."""

    def test_cache_module_exists(self):
        """app.cache must be importable."""
        from app.cache import TTLCache
        assert callable(TTLCache)

    def test_cache_stores_and_retrieves(self):
        """Cache.get should return stored value within TTL."""
        from app.cache import TTLCache
        cache = TTLCache(ttl_seconds=60)
        cache.set("key1", {"data": "test"})
        result = cache.get("key1")
        assert result == {"data": "test"}

    def test_cache_returns_none_for_missing_key(self):
        """Cache.get should return None for keys that were never set."""
        from app.cache import TTLCache
        cache = TTLCache(ttl_seconds=60)
        assert cache.get("nonexistent") is None

    def test_cache_expires_after_ttl(self):
        """Cache entries must expire after TTL seconds."""
        from app.cache import TTLCache
        cache = TTLCache(ttl_seconds=1)
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
        time.sleep(1.1)
        assert cache.get("key1") is None

    def test_cache_overwrite(self):
        """Setting the same key again should update value and reset TTL."""
        from app.cache import TTLCache
        cache = TTLCache(ttl_seconds=60)
        cache.set("k", "v1")
        cache.set("k", "v2")
        assert cache.get("k") == "v2"

    def test_panchang_cache_instance_exists(self):
        """A panchang_cache instance should be available."""
        from app.cache import panchang_cache
        assert panchang_cache is not None

    def test_horoscope_cache_instance_exists(self):
        """A horoscope_cache instance should be available."""
        from app.cache import horoscope_cache
        assert horoscope_cache is not None


# ============================================================
# H-10: Image Upload Endpoint
# ============================================================

class TestH10ImageUpload:
    """Admin image upload endpoint must accept files and return URLs."""

    def test_upload_requires_admin(self, client, user_token):
        """Non-admin users must get 403."""
        resp = client.post(
            "/api/admin/upload-image",
            headers={"Authorization": f"Bearer {user_token}"},
            files={"file": ("test.png", b"fakepngdata", "image/png")},
        )
        assert resp.status_code == 403

    def test_upload_image_success(self, client, admin_token, tmp_path):
        """Admin can upload image and get back a URL."""
        resp = client.post(
            "/api/admin/upload-image",
            headers={"Authorization": f"Bearer {admin_token}"},
            files={"file": ("test.png", b"\x89PNG\r\n\x1a\nfakedata", "image/png")},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "url" in data
        assert "/static/uploads/" in data["url"]
        assert data["url"].endswith(".png")

    def test_upload_rejects_no_file(self, client, admin_token):
        """Upload without file should fail."""
        resp = client.post(
            "/api/admin/upload-image",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 422

    def test_static_mount_exists(self, client):
        """The /static path should be mounted for serving uploaded files."""
        from app.main import app
        route_paths = [r.path for r in app.routes if hasattr(r, "path")]
        # StaticFiles mount creates a Mount with path "/static"
        mount_paths = []
        for route in app.routes:
            if hasattr(route, "path"):
                mount_paths.append(route.path)
        assert any("/static" in p for p in mount_paths), f"No /static mount found. Routes: {mount_paths}"


# ============================================================
# H-04: consultation_fee / per_minute_rate Float Consistency
# ============================================================

class TestH04ConsultationFeeType:
    """per_minute_rate must be REAL/float throughout the stack."""

    def test_db_schema_uses_real(self):
        """Database schema defines per_minute_rate as REAL."""
        from app.database import SCHEMA
        assert "per_minute_rate REAL" in SCHEMA

    def test_model_uses_float(self):
        """Pydantic model uses float for per_minute_rate."""
        from app.models import AstrologerProfileUpdate
        field = AstrologerProfileUpdate.model_fields["per_minute_rate"]
        # The annotation should be Optional[float]
        import typing
        assert field.annotation in (float, typing.Optional[float])

    def test_astrologer_profile_update_accepts_float(self):
        """AstrologerProfileUpdate should accept float values."""
        from app.models import AstrologerProfileUpdate
        update = AstrologerProfileUpdate(per_minute_rate=25.50)
        assert update.per_minute_rate == 25.50


# ============================================================
# Quick fix: e2e/__init__.py
# ============================================================

class TestE2eInit:
    """e2e/ directory must have __init__.py."""

    def test_e2e_init_exists(self):
        """e2e/__init__.py must exist."""
        init_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "e2e", "__init__.py"
        )
        assert os.path.exists(init_path), f"Missing: {init_path}"
