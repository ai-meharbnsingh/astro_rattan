"""
Blueprint Contract Tests v2 — Uses conftest.py fixtures
========================================================
This version uses conftest.py fixtures for proper test isolation.
"""
import json
import pytest
from tests.conftest import _register_user, _auth_header, _create_kundli, _make_admin, _make_astrologer


class TestAstroIogitaEngine:
    """REQ-ASTRO-IOGITA-001: astro_iogita_engine.py maps planets to atoms."""

    def test_planet_atom_map_has_9_planets(self):
        from app.astro_iogita_engine import PLANET_ATOM_MAP
        assert len(PLANET_ATOM_MAP) == 9

    def test_planet_strength_exalted(self):
        from app.astro_iogita_engine import get_planet_strength
        assert get_planet_strength("Sun", "Aries") == 0.95

    def test_planet_strength_debilitated(self):
        from app.astro_iogita_engine import get_planet_strength
        assert get_planet_strength("Sun", "Libra") == 0.20

    def test_build_atom_vector_shape(self):
        from app.astro_iogita_engine import build_atom_vector
        import numpy as np
        planet_positions = {"Sun": "Leo", "Moon": "Cancer"}
        vec = build_atom_vector(planet_positions, "Venus")
        assert vec.shape == (16,)

    def test_identify_basin_returns_required_keys(self):
        from app.astro_iogita_engine import identify_basin
        import numpy as np
        vec = np.random.uniform(-1, 1, 16)
        result = identify_basin(vec)
        required = ["basin_name", "basin_hindi", "description", "escape_possible", "escape_trigger", "warning"]
        for key in required:
            assert key in result

    def test_run_astro_analysis_meharban(self):
        from app.astro_iogita_engine import run_astro_analysis
        planet_positions = {
            "Sun": "Leo", "Moon": "Scorpio", "Mars": "Cancer",
            "Mercury": "Cancer", "Jupiter": "Capricorn",
            "Venus": "Cancer", "Saturn": "Libra",
            "Rahu": "Aries", "Ketu": "Libra"
        }
        result = run_astro_analysis(planet_positions, "Venus", "Meharban")
        assert "basin" in result
        assert "atom_activations" in result

    def test_dasha_amplify_modifies_atoms(self):
        from app.astro_iogita_engine import DASHA_AMPLIFY
        assert len(DASHA_AMPLIFY) == 9
        # Check that all values are dicts with atom amplifications
        for planet, atoms in DASHA_AMPLIFY.items():
            assert isinstance(atoms, dict)
            assert len(atoms) > 0


class TestKundliGeneration:
    """REQ-ASTRO-KUNDLI-001: Kundli generation from date/time/place."""

    def test_generate_kundli_creates_record(self, client):
        user, token = _register_user(client, "kundli_test@test.com")
        resp = client.post("/api/kundli/generate", json={
            "person_name": "Test Person",
            "birth_date": "1993-12-05",
            "birth_time": "14:30:00",
            "birth_place": "Delhi",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "timezone_offset": 5.5,
            "ayanamsa": "lahiri"
        }, headers=_auth_header(token))
        assert resp.status_code == 201
        assert "id" in resp.json()

    def test_generate_kundli_returns_planets(self, client):
        user, token = _register_user(client, "kundli_planets@test.com")
        resp = client.post("/api/kundli/generate", json={
            "person_name": "Test",
            "birth_date": "1993-12-05",
            "birth_time": "14:30:00",
            "birth_place": "Delhi",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "timezone_offset": 5.5,
            "ayanamsa": "lahiri"
        }, headers=_auth_header(token))
        data = resp.json()
        assert "chart_data" in data
        assert "planets" in data["chart_data"]


class TestHoroscope:
    """REQ-ASTRO-HORO-001: Horoscope by sign and period."""

    def test_get_daily_horoscope(self, client):
        resp = client.get("/api/horoscope/aries?period=daily")
        assert resp.status_code == 200
        data = resp.json()
        assert data["sign"] == "aries"
        assert data["period"] == "daily"

    def test_horoscope_invalid_sign(self, client):
        resp = client.get("/api/horoscope/invalid_sign")
        assert resp.status_code in [400, 422, 404]


class TestCart:
    """REQ-ECOM-CART-001: Cart CRUD operations."""

    def test_add_to_cart(self, client, db):
        user, token = _register_user(client, "cart_test@test.com")
        # First get a product
        resp = client.get("/api/products")
        products = resp.json()["products"]
        product_id = products[0]["id"]
        
        resp = client.post("/api/cart/add", json={
            "product_id": product_id,
            "quantity": 2
        }, headers=_auth_header(token))
        assert resp.status_code == 201

    def test_add_out_of_stock_rejected(self, client, db):
        user, token = _register_user(client, "cart_stock@test.com")
        resp = client.get("/api/products")
        products = resp.json()["products"]
        product_id = products[0]["id"]
        
        resp = client.post("/api/cart/add", json={
            "product_id": product_id,
            "quantity": 9999
        }, headers=_auth_header(token))
        assert resp.status_code == 400


class TestOrders:
    """REQ-ECOM-ORDER-001: Order creation and management."""

    def test_create_order(self, client, db):
        user, token = _register_user(client, "order_test@test.com")
        # Add to cart first
        resp = client.get("/api/products")
        product_id = resp.json()["products"][0]["id"]
        client.post("/api/cart/add", json={"product_id": product_id, "quantity": 1},
                   headers=_auth_header(token))
        
        # Create order
        resp = client.post("/api/orders", json={
            "shipping_address": "123 Main St, Delhi 110001",
            "payment_method": "cod"
        }, headers=_auth_header(token))
        assert resp.status_code == 201


class TestPayments:
    """REQ-ECOM-PAY-001: Payment initiation and webhooks."""

    def test_initiate_payment(self, client, db):
        user, token = _register_user(client, "payment_test@test.com")
        # Create order first
        resp = client.get("/api/products")
        product_id = resp.json()["products"][0]["id"]
        client.post("/api/cart/add", json={"product_id": product_id, "quantity": 1},
                   headers=_auth_header(token))
        resp = client.post("/api/orders", json={
            "shipping_address": "123 Main St, Delhi",
            "payment_method": "cod"
        }, headers=_auth_header(token))
        order_id = resp.json()["id"]
        
        # Initiate payment
        resp = client.post("/api/payments/initiate", json={
            "order_id": order_id,
            "provider": "cod"
        }, headers=_auth_header(token))
        assert resp.status_code == 200


class TestAdmin:
    """REQ-ADMIN-001: Admin dashboard and management."""

    def test_admin_list_users(self, client, db):
        user, token = _register_user(client, "admin_list@test.com")
        admin_token = _make_admin(db, user["id"])
        resp = client.get("/api/admin/users", headers=_auth_header(admin_token))
        assert resp.status_code == 200

    def test_admin_dashboard_stats(self, client, db):
        user, token = _register_user(client, "admin_dash@test.com")
        admin_token = _make_admin(db, user["id"])
        resp = client.get("/api/admin/dashboard", headers=_auth_header(admin_token))
        assert resp.status_code == 200
        data = resp.json()
        assert "stats" in data
