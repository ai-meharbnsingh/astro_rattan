"""Route-level tests for /api/cart/* endpoints.

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
    """Create a fresh test database with schema + seed data + test products."""
    db_path = str(tmp_path_factory.mktemp("cart_db") / "test_cart.db")
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
    """TestClient with rate limiter disabled for tests."""
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
        "email": "cart_test@example.com",
        "password": "testpass123",
        "name": "Cart Tester",
    })
    assert resp.status_code == 201, f"Register failed: {resp.text}"
    return resp.json()["token"]


@pytest.fixture(scope="module")
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture(scope="module")
def product_id(test_db):
    """Get the first active product from the seeded database, or insert one."""
    conn = sqlite3.connect(test_db)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT id, stock FROM products WHERE is_active = 1 AND stock > 0 LIMIT 1").fetchone()
    if row:
        pid = row["id"]
    else:
        # Insert a test product
        conn.execute(
            """INSERT INTO products (id, name, description, category, price, stock, is_active)
               VALUES ('test_prod_001', 'Test Gemstone', 'A test gemstone', 'gemstone', 999.0, 50, 1)"""
        )
        conn.commit()
        pid = "test_prod_001"
    conn.close()
    return pid


@pytest.fixture(scope="module")
def out_of_stock_product_id(test_db):
    """Insert a product with stock=0."""
    conn = sqlite3.connect(test_db)
    conn.execute(
        """INSERT OR IGNORE INTO products (id, name, description, category, price, stock, is_active)
           VALUES ('oos_prod_001', 'Out of Stock Gem', 'No stock', 'gemstone', 500.0, 0, 1)"""
    )
    conn.commit()
    conn.close()
    return "oos_prod_001"


# ── Tests ───────────────────────────────────────────────────

class TestGetCart:

    def test_get_empty_cart(self, client, auth_headers):
        """GET /api/cart (empty) → 200, empty items."""
        resp = client.get("/api/cart", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "items" in data
        assert isinstance(data["items"], list)
        assert "total" in data

    def test_cart_without_auth(self, client):
        """GET /api/cart without auth → 401."""
        resp = client.get("/api/cart")
        assert resp.status_code == 401


class TestAddToCart:

    def test_add_to_cart_success(self, client, auth_headers, product_id):
        """POST /api/cart/add → 201, cart with item."""
        resp = client.post("/api/cart/add", json={
            "product_id": product_id,
            "quantity": 1,
        }, headers=auth_headers)
        assert resp.status_code == 201, f"Expected 201, got {resp.status_code}: {resp.text}"
        data = resp.json()
        assert "items" in data
        assert len(data["items"]) >= 1
        assert data["total"] > 0

    def test_add_duplicate_updates_quantity(self, client, auth_headers, product_id):
        """POST /api/cart/add duplicate → updates quantity (adds to existing)."""
        # Add 1 more of the same product
        resp = client.post("/api/cart/add", json={
            "product_id": product_id,
            "quantity": 1,
        }, headers=auth_headers)
        assert resp.status_code == 201
        data = resp.json()
        # Find the item for our product
        matching = [i for i in data["items"] if i["product_id"] == product_id]
        assert len(matching) == 1
        assert matching[0]["quantity"] >= 2  # Was 1, added 1 more

    def test_add_out_of_stock_product(self, client, auth_headers, out_of_stock_product_id):
        """POST /api/cart/add out-of-stock → 400 (CHAOS #7)."""
        resp = client.post("/api/cart/add", json={
            "product_id": out_of_stock_product_id,
            "quantity": 1,
        }, headers=auth_headers)
        assert resp.status_code == 400
        assert "stock" in resp.json()["detail"].lower() or "insufficient" in resp.json()["detail"].lower()

    def test_add_nonexistent_product(self, client, auth_headers):
        """POST /api/cart/add with nonexistent product → 404."""
        resp = client.post("/api/cart/add", json={
            "product_id": "nonexistent_prod_xyz",
            "quantity": 1,
        }, headers=auth_headers)
        assert resp.status_code == 404

    def test_add_quantity_zero(self, client, auth_headers, product_id):
        """POST /api/cart/add with quantity=0 → 422 (validation: ge=1)."""
        resp = client.post("/api/cart/add", json={
            "product_id": product_id,
            "quantity": 0,
        }, headers=auth_headers)
        assert resp.status_code == 422

    def test_add_without_auth(self, client, product_id):
        """POST /api/cart/add without auth → 401."""
        resp = client.post("/api/cart/add", json={
            "product_id": product_id,
            "quantity": 1,
        })
        assert resp.status_code == 401


class TestUpdateCartItem:

    def test_update_quantity_success(self, client, auth_headers, product_id):
        """PATCH /api/cart/{id} update quantity → 200."""
        # Get cart to find the item ID
        cart_resp = client.get("/api/cart", headers=auth_headers)
        items = cart_resp.json()["items"]
        matching = [i for i in items if i["product_id"] == product_id]
        assert len(matching) >= 1
        item_id = matching[0]["id"]

        resp = client.patch(f"/api/cart/{item_id}", json={"quantity": 3}, headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        updated = [i for i in data["items"] if i["id"] == item_id]
        assert len(updated) == 1
        assert updated[0]["quantity"] == 3

    def test_update_quantity_beyond_stock(self, client, auth_headers, product_id):
        """PATCH /api/cart/{id} beyond stock → 400."""
        cart_resp = client.get("/api/cart", headers=auth_headers)
        items = cart_resp.json()["items"]
        matching = [i for i in items if i["product_id"] == product_id]
        item_id = matching[0]["id"]

        resp = client.patch(f"/api/cart/{item_id}", json={"quantity": 999999}, headers=auth_headers)
        assert resp.status_code == 400


class TestRemoveCartItem:

    def test_remove_cart_item_success(self, client, auth_headers, product_id):
        """DELETE /api/cart/{id} → 200."""
        cart_resp = client.get("/api/cart", headers=auth_headers)
        items = cart_resp.json()["items"]
        matching = [i for i in items if i["product_id"] == product_id]
        assert len(matching) >= 1
        item_id = matching[0]["id"]

        resp = client.delete(f"/api/cart/{item_id}", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        # Item should be gone
        remaining = [i for i in data["items"] if i["id"] == item_id]
        assert len(remaining) == 0

    def test_remove_nonexistent_item(self, client, auth_headers):
        """DELETE /api/cart/{nonexistent} → 404."""
        resp = client.delete("/api/cart/nonexistent_item_xyz", headers=auth_headers)
        assert resp.status_code == 404


class TestCartPersistence:

    def test_cart_preserves_between_requests(self, client, auth_headers, product_id):
        """Cart data persists across separate GET requests."""
        # Add a fresh item
        client.post("/api/cart/add", json={
            "product_id": product_id,
            "quantity": 2,
        }, headers=auth_headers)

        # Fetch cart twice — should be the same
        resp1 = client.get("/api/cart", headers=auth_headers)
        resp2 = client.get("/api/cart", headers=auth_headers)
        assert resp1.json()["total"] == resp2.json()["total"]
        assert len(resp1.json()["items"]) == len(resp2.json()["items"])

    def test_cart_total_correct(self, client, auth_headers):
        """GET /api/cart after operations → has correct total (price * qty sum)."""
        resp = client.get("/api/cart", headers=auth_headers)
        data = resp.json()
        computed_total = sum(item["price"] * item["quantity"] for item in data["items"])
        assert abs(data["total"] - round(computed_total, 2)) < 0.01
