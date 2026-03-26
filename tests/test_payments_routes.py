"""Route-level tests for /api/payments/* endpoints.

Uses FastAPI TestClient with a fresh temp DB per test session.
Covers happy path, error path, and chaos scenarios.
"""
import os
import sqlite3
import importlib

import pytest
from fastapi.testclient import TestClient


# ── Fixtures ────────────────────────────────────────────────

@pytest.fixture(scope="module")
def test_db(tmp_path_factory):
    """Create a fresh test database with schema + seed data."""
    db_path = str(tmp_path_factory.mktemp("payments_db") / "test_payments.db")
    os.environ["DB_PATH"] = db_path
    import app.config
    importlib.reload(app.config)
    import app.database
    importlib.reload(app.database)

    from app.database import init_db, migrate_users_table
    from app.seed_data import seed_all
    init_db(db_path)
    migrate_users_table(db_path)
    seed_all(db_path)
    return db_path


@pytest.fixture(scope="module")
def client(test_db):
    """TestClient with rate limiter disabled."""
    os.environ["DB_PATH"] = test_db
    import app.config
    importlib.reload(app.config)
    import app.database
    importlib.reload(app.database)

    from app.main import app, limiter
    limiter.enabled = False
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture(scope="module")
def auth_token(client):
    """Register a test user and return JWT token."""
    resp = client.post("/api/auth/register", json={
        "email": "payment_test@example.com",
        "password": "testpass123",
        "name": "Payment Tester",
    })
    assert resp.status_code == 201, f"Register failed: {resp.text}"
    return resp.json()["token"]


@pytest.fixture(scope="module")
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture(scope="module")
def second_user_headers(client):
    """Register a second user and return headers (for cross-user tests)."""
    resp = client.post("/api/auth/register", json={
        "email": "payment_other@example.com",
        "password": "testpass123",
        "name": "Other Payment User",
    })
    assert resp.status_code == 201
    token = resp.json()["token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="module")
def product_id(test_db):
    """Get or create a product with sufficient stock."""
    conn = sqlite3.connect(test_db)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT id FROM products WHERE is_active = 1 AND stock >= 20 LIMIT 1"
    ).fetchone()
    if row:
        pid = row["id"]
    else:
        conn.execute(
            """INSERT INTO products (id, name, description, category, price, stock, is_active)
               VALUES ('pay_test_prod', 'Payment Test Gem', 'For payment tests', 'gemstone', 2000.0, 100, 1)"""
        )
        conn.commit()
        pid = "pay_test_prod"
    conn.close()
    return pid


def _create_order(client, auth_headers, product_id, payment_method="cod"):
    """Helper: add to cart + create order → return order_id."""
    client.post("/api/cart/add", json={
        "product_id": product_id,
        "quantity": 1,
    }, headers=auth_headers)
    resp = client.post("/api/orders", json={
        "shipping_address": "Payment Test Street, Mumbai 400001",
        "payment_method": payment_method,
    }, headers=auth_headers)
    assert resp.status_code == 201, f"Order creation failed: {resp.text}"
    return resp.json()["id"]


# ── Tests ───────────────────────────────────────────────────

class TestInitiatePayment:

    def test_initiate_payment_cod(self, client, auth_headers, product_id):
        """POST /api/payments/initiate → 200, payment_id for COD."""
        order_id = _create_order(client, auth_headers, product_id, payment_method="cod")

        resp = client.post("/api/payments/initiate", json={
            "order_id": order_id,
            "provider": "cod",
        }, headers=auth_headers)
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
        data = resp.json()
        assert "payment_id" in data
        assert data["order_id"] == order_id
        assert data["provider"] == "cod"

    def test_initiate_payment_razorpay(self, client, auth_headers, product_id):
        """Razorpay initiate → has provider_payment_id (test mode)."""
        order_id = _create_order(client, auth_headers, product_id, payment_method="razorpay")

        resp = client.post("/api/payments/initiate", json={
            "order_id": order_id,
            "provider": "razorpay",
        }, headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "payment_id" in data
        assert data["provider"] == "razorpay"
        # In test mode (no RAZORPAY_KEY_ID), provider_payment_id should be a test placeholder
        assert "provider_payment_id" in data

    def test_initiate_payment_stripe(self, client, auth_headers, product_id):
        """Stripe initiate → has provider_payment_id (test mode)."""
        order_id = _create_order(client, auth_headers, product_id, payment_method="stripe")

        resp = client.post("/api/payments/initiate", json={
            "order_id": order_id,
            "provider": "stripe",
        }, headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "payment_id" in data
        assert data["provider"] == "stripe"
        assert "provider_payment_id" in data

    def test_initiate_already_paid(self, client, auth_headers, product_id, test_db):
        """POST /api/payments/initiate for already-paid order → 400."""
        order_id = _create_order(client, auth_headers, product_id)

        # Manually mark the order as paid in the DB
        conn = sqlite3.connect(test_db)
        conn.execute(
            "UPDATE orders SET payment_status = 'paid' WHERE id = ?", (order_id,)
        )
        conn.commit()
        conn.close()

        resp = client.post("/api/payments/initiate", json={
            "order_id": order_id,
            "provider": "cod",
        }, headers=auth_headers)
        assert resp.status_code == 400
        assert "already paid" in resp.json()["detail"].lower()

    def test_initiate_nonexistent_order(self, client, auth_headers):
        """POST /api/payments/initiate nonexistent order → 404."""
        resp = client.post("/api/payments/initiate", json={
            "order_id": "nonexistent_order_xyz",
            "provider": "cod",
        }, headers=auth_headers)
        assert resp.status_code == 404

    def test_initiate_without_auth(self, client, product_id):
        """POST /api/payments/initiate without auth → 401."""
        resp = client.post("/api/payments/initiate", json={
            "order_id": "any_order",
            "provider": "cod",
        })
        assert resp.status_code == 401


class TestIdempotency:

    def test_idempotent_same_order_provider(self, client, auth_headers, product_id):
        """Idempotent: same order + provider → returns existing payment."""
        order_id = _create_order(client, auth_headers, product_id)

        resp1 = client.post("/api/payments/initiate", json={
            "order_id": order_id,
            "provider": "cod",
        }, headers=auth_headers)
        assert resp1.status_code == 200
        payment_id_1 = resp1.json()["payment_id"]

        # Same request again
        resp2 = client.post("/api/payments/initiate", json={
            "order_id": order_id,
            "provider": "cod",
        }, headers=auth_headers)
        assert resp2.status_code == 200
        payment_id_2 = resp2.json()["payment_id"]

        assert payment_id_1 == payment_id_2


class TestCrossUserSecurity:

    def test_payment_for_other_users_order(self, client, auth_headers, second_user_headers, product_id):
        """Payment for other user's order → 404 (order not found for this user)."""
        # Create order as primary user
        order_id = _create_order(client, auth_headers, product_id)

        # Try to initiate payment as second user
        resp = client.post("/api/payments/initiate", json={
            "order_id": order_id,
            "provider": "cod",
        }, headers=second_user_headers)
        assert resp.status_code == 404


class TestPaymentAmounts:

    def test_payment_amount_matches_order(self, client, auth_headers, product_id):
        """Payment amount should match the order total."""
        order_id = _create_order(client, auth_headers, product_id)

        # Get order total
        order_resp = client.get(f"/api/orders/{order_id}", headers=auth_headers)
        order_total = order_resp.json()["total"]

        # Initiate payment
        pay_resp = client.post("/api/payments/initiate", json={
            "order_id": order_id,
            "provider": "cod",
        }, headers=auth_headers)
        assert pay_resp.status_code == 200
        assert abs(pay_resp.json()["amount"] - order_total) < 0.01
