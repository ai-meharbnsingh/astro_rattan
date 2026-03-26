"""Route-level tests for /api/orders/* endpoints.

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
    db_path = str(tmp_path_factory.mktemp("orders_db") / "test_orders.db")
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
        "email": "orders_test@example.com",
        "password": "testpass123",
        "name": "Orders Tester",
    })
    assert resp.status_code == 201, f"Register failed: {resp.text}"
    return resp.json()["token"]


@pytest.fixture(scope="module")
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture(scope="module")
def product_id(test_db):
    """Get or create a product with sufficient stock."""
    conn = sqlite3.connect(test_db)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT id FROM products WHERE is_active = 1 AND stock >= 10 LIMIT 1"
    ).fetchone()
    if row:
        pid = row["id"]
    else:
        conn.execute(
            """INSERT INTO products (id, name, description, category, price, stock, is_active)
               VALUES ('order_test_prod', 'Order Test Gem', 'For order tests', 'gemstone', 1500.0, 100, 1)"""
        )
        conn.commit()
        pid = "order_test_prod"
    conn.close()
    return pid


def _add_item_to_cart(client, auth_headers, product_id, quantity=2):
    """Helper: add a product to the cart."""
    resp = client.post("/api/cart/add", json={
        "product_id": product_id,
        "quantity": quantity,
    }, headers=auth_headers)
    return resp


def _get_product_stock(test_db, product_id):
    """Helper: get current stock for a product."""
    conn = sqlite3.connect(test_db)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT stock FROM products WHERE id = ?", (product_id,)).fetchone()
    conn.close()
    return row["stock"] if row else 0


# ── Tests ───────────────────────────────────────────────────

class TestCreateOrder:

    def test_create_order_success(self, client, auth_headers, product_id, test_db):
        """POST /api/orders (with items in cart) → 201."""
        # First add items to cart
        _add_item_to_cart(client, auth_headers, product_id, quantity=2)

        stock_before = _get_product_stock(test_db, product_id)

        resp = client.post("/api/orders", json={
            "shipping_address": "123 Test Street, Mumbai, Maharashtra 400001",
            "payment_method": "cod",
        }, headers=auth_headers)
        assert resp.status_code == 201, f"Expected 201, got {resp.status_code}: {resp.text}"
        data = resp.json()
        assert "id" in data
        assert data["status"] == "placed"
        assert data["payment_method"] == "cod"
        assert data["total"] > 0

    def test_create_order_empty_cart(self, client, auth_headers):
        """POST /api/orders (empty cart) → 400."""
        # Cart should be empty after previous order creation
        resp = client.post("/api/orders", json={
            "shipping_address": "123 Test Street, Mumbai, Maharashtra 400001",
            "payment_method": "cod",
        }, headers=auth_headers)
        assert resp.status_code == 400
        assert "empty" in resp.json()["detail"].lower()

    def test_create_order_reduces_stock(self, client, auth_headers, product_id, test_db):
        """POST /api/orders reduces product stock."""
        stock_before = _get_product_stock(test_db, product_id)
        qty = 1

        _add_item_to_cart(client, auth_headers, product_id, quantity=qty)
        client.post("/api/orders", json={
            "shipping_address": "456 Stock Test Lane, Delhi 110001",
            "payment_method": "cod",
        }, headers=auth_headers)

        stock_after = _get_product_stock(test_db, product_id)
        assert stock_after == stock_before - qty

    def test_order_clears_cart(self, client, auth_headers, product_id):
        """Order clears cart after creation."""
        _add_item_to_cart(client, auth_headers, product_id, quantity=1)
        client.post("/api/orders", json={
            "shipping_address": "789 Clear Cart Road, Kolkata 700001",
            "payment_method": "cod",
        }, headers=auth_headers)

        cart_resp = client.get("/api/cart", headers=auth_headers)
        assert cart_resp.status_code == 200
        assert len(cart_resp.json()["items"]) == 0

    def test_order_without_auth(self, client):
        """POST /api/orders without auth → 401."""
        resp = client.post("/api/orders", json={
            "shipping_address": "123 No Auth Street, Test 100001",
            "payment_method": "cod",
        })
        assert resp.status_code == 401

    def test_cod_order_payment_pending(self, client, auth_headers, product_id):
        """COD order → payment_status=pending."""
        _add_item_to_cart(client, auth_headers, product_id, quantity=1)
        resp = client.post("/api/orders", json={
            "shipping_address": "321 COD Street, Chennai 600001",
            "payment_method": "cod",
        }, headers=auth_headers)
        assert resp.status_code == 201
        assert resp.json()["payment_status"] == "pending"

    def test_invalid_payment_method(self, client, auth_headers, product_id):
        """Invalid payment_method → 422."""
        _add_item_to_cart(client, auth_headers, product_id, quantity=1)
        resp = client.post("/api/orders", json={
            "shipping_address": "999 Invalid Pay Road, Test 100001",
            "payment_method": "bitcoin",
        }, headers=auth_headers)
        assert resp.status_code == 422

    def test_short_shipping_address(self, client, auth_headers, product_id):
        """Shipping address too short → 422 (min_length=10)."""
        _add_item_to_cart(client, auth_headers, product_id, quantity=1)
        resp = client.post("/api/orders", json={
            "shipping_address": "short",
            "payment_method": "cod",
        }, headers=auth_headers)
        assert resp.status_code == 422


class TestListOrders:

    def test_list_orders_success(self, client, auth_headers):
        """GET /api/orders → 200, list of orders."""
        resp = client.get("/api/orders", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1  # We created orders above

    def test_list_orders_no_auth(self, client):
        """GET /api/orders without auth → 401."""
        resp = client.get("/api/orders")
        assert resp.status_code == 401


class TestGetOrder:

    def test_get_order_success(self, client, auth_headers):
        """GET /api/orders/{id} → 200 with items."""
        # Get list first
        list_resp = client.get("/api/orders", headers=auth_headers)
        orders = list_resp.json()
        assert len(orders) >= 1
        order_id = orders[0]["id"]

        resp = client.get(f"/api/orders/{order_id}", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == order_id
        assert "items" in data
        assert isinstance(data["items"], list)

    def test_get_order_nonexistent(self, client, auth_headers):
        """GET /api/orders/{nonexistent} → 404."""
        resp = client.get("/api/orders/nonexistent_order_xyz", headers=auth_headers)
        assert resp.status_code == 404


class TestOrderIntegrity:

    def test_multiple_orders_all_tracked(self, client, auth_headers, product_id):
        """Multiple orders → all tracked in list."""
        # Count existing orders
        before_resp = client.get("/api/orders", headers=auth_headers)
        count_before = len(before_resp.json())

        # Create 2 more orders
        for _ in range(2):
            _add_item_to_cart(client, auth_headers, product_id, quantity=1)
            client.post("/api/orders", json={
                "shipping_address": "Multi Order Test Street, Pune 411001",
                "payment_method": "cod",
            }, headers=auth_headers)

        after_resp = client.get("/api/orders", headers=auth_headers)
        count_after = len(after_resp.json())
        assert count_after == count_before + 2

    def test_order_total_matches_cart_total(self, client, auth_headers, product_id):
        """Order total matches what was in the cart."""
        _add_item_to_cart(client, auth_headers, product_id, quantity=3)
        cart_resp = client.get("/api/cart", headers=auth_headers)
        cart_total = cart_resp.json()["total"]
        assert cart_total > 0

        order_resp = client.post("/api/orders", json={
            "shipping_address": "Total Match Road, Bangalore 560001",
            "payment_method": "cod",
        }, headers=auth_headers)
        assert order_resp.status_code == 201
        assert abs(order_resp.json()["total"] - cart_total) < 0.01
