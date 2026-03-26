"""RED phase: config tests — must FAIL before config.py exists."""
import os
import importlib
import pytest


def test_config_has_db_path():
    from app.config import DB_PATH
    assert isinstance(DB_PATH, str)
    assert DB_PATH.endswith(".db")


def test_config_has_jwt_secret():
    from app.config import JWT_SECRET
    assert isinstance(JWT_SECRET, str)
    assert len(JWT_SECRET) > 10


def test_config_has_ports():
    from app.config import BACKEND_PORT, FRONTEND_PORT
    assert BACKEND_PORT == 8028
    assert FRONTEND_PORT == 5198


def test_config_has_openai_key_field():
    from app.config import OPENAI_API_KEY
    assert isinstance(OPENAI_API_KEY, str)


def test_config_has_app_version():
    from app.config import APP_VERSION
    assert APP_VERSION == "1.0.0"


def test_config_supports_email_aliases(monkeypatch):
    monkeypatch.setenv("EMAIL_SMTP_HOST", "smtp.gmail.com")
    monkeypatch.setenv("EMAIL_SMTP_PORT", "587")
    monkeypatch.setenv("EMAIL_USERNAME", "sender@example.com")
    monkeypatch.setenv("EMAIL_PASSWORD", "secret")
    monkeypatch.setenv("EMAIL_FROM", "sender@example.com")
    monkeypatch.setenv("EMAIL_TO", "ops@example.com")

    import app.config
    importlib.reload(app.config)

    assert app.config.SMTP_HOST == "smtp.gmail.com"
    assert app.config.SMTP_PORT == 587
    assert app.config.SMTP_USER == "sender@example.com"
    assert app.config.SMTP_PASSWORD == "secret"
    assert app.config.FROM_EMAIL == "sender@example.com"
    assert app.config.EMAIL_TO == "ops@example.com"
