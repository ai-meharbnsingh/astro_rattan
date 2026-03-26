"""RED phase: Pydantic model validation tests."""
import pytest
from pydantic import ValidationError


def test_user_register_valid():
    from app.models import UserRegister
    u = UserRegister(email="test@test.com", password="secret123", name="Test User")
    assert u.email == "test@test.com"


def test_user_register_invalid_email():
    from app.models import UserRegister
    with pytest.raises(ValidationError):
        UserRegister(email="not-an-email", password="secret123", name="Test")


def test_kundli_request_valid():
    from app.models import KundliRequest
    k = KundliRequest(
        person_name="Test", birth_date="2000-01-01", birth_time="12:00:00",
        birth_place="Delhi", latitude=28.6139, longitude=77.2090, timezone_offset=5.5
    )
    assert k.latitude == 28.6139


def test_product_create_valid():
    from app.models import ProductCreate
    p = ProductCreate(name="Ruby", description="Natural ruby", category="gemstone", price=5000.0, stock=10)
    assert p.price == 5000.0


def test_product_create_invalid_price():
    from app.models import ProductCreate
    with pytest.raises(ValidationError):
        ProductCreate(name="Ruby", description="Test", category="gemstone", price=-100, stock=10)


def test_login_request():
    from app.models import LoginRequest
    lr = LoginRequest(email="test@test.com", password="secret")
    assert lr.email == "test@test.com"
