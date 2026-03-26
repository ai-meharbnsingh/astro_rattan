"""RED phase: auth tests."""
import pytest


def test_hash_password_returns_hash():
    from app.auth import hash_password
    h = hash_password("secret123")
    assert h != "secret123"
    assert len(h) > 20


def test_verify_password_correct():
    from app.auth import hash_password, verify_password
    h = hash_password("secret123")
    assert verify_password("secret123", h) is True


def test_verify_password_wrong():
    from app.auth import hash_password, verify_password
    h = hash_password("secret123")
    assert verify_password("wrong", h) is False


def test_create_token_returns_string():
    from app.auth import create_token
    token = create_token({"sub": "user123", "role": "user"})
    assert isinstance(token, str)
    assert len(token) > 20


def test_decode_token_roundtrip():
    from app.auth import create_token, decode_token
    token = create_token({"sub": "user123", "role": "admin"})
    payload = decode_token(token)
    assert payload["sub"] == "user123"
    assert payload["role"] == "admin"


def test_decode_token_invalid():
    from app.auth import decode_token
    result = decode_token("invalid.token.here")
    assert result is None


def test_require_role_admin():
    from app.auth import require_role
    checker = require_role("admin")
    assert callable(checker)
