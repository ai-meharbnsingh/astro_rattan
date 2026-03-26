"""Tests for admin dashboard, user management, order management, and product management."""
import pytest
from tests.conftest import (
    _register_user, _auth_header, _make_admin, _make_astrologer,
)
from app.auth import create_token


# ---- Fixtures ---- #

@pytest.fixture(scope="module")
def admin_setup(client, db):
    """Register an admin user + a regular user for tests."""
    # Admin
    admin_user, _ = _register_user(client, "admin_route@test.com", name="Admin Route")
    admin_token = _make_admin(db, admin_user["id"])

    # Regular user
    reg_user, reg_token = _register_user(client, "regular_admin_test@test.com", name="Regular User")

    return {
        "admin_id": admin_user["id"],
        "admin_token": admin_token,
        "reg_id": reg_user["id"],
        "reg_token": reg_token,
    }


# ---- Dashboard ---- #

def test_admin_dashboard_200(client, admin_setup):
    """GET /api/admin/dashboard returns 200 with stats."""
    resp = client.get("/api/admin/dashboard", headers=_auth_header(admin_setup["admin_token"]))
    assert resp.status_code == 200
    data = resp.json()
    assert "stats" in data
    stats = data["stats"]
    assert "users" in stats
    assert "orders" in stats
    assert "revenue" in stats
    assert "pending_orders" in stats


# ---- User Management ---- #

def test_admin_list_users_200(client, admin_setup):
    """GET /api/admin/users returns 200 with user list."""
    resp = client.get("/api/admin/users", headers=_auth_header(admin_setup["admin_token"]))
    assert resp.status_code == 200
    data = resp.json()
    assert "users" in data
    assert isinstance(data["users"], list)
    assert data["total"] >= 1
    assert "is_active" in data["users"][0]


def test_admin_get_user_detail_200(client, admin_setup):
    """GET /api/admin/users/{id} returns 200 with detail + counts."""
    uid = admin_setup["reg_id"]
    resp = client.get(f"/api/admin/users/{uid}", headers=_auth_header(admin_setup["admin_token"]))
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == uid
    assert "kundli_count" in data
    assert "order_count" in data
    assert "consultation_count" in data


def test_admin_create_astrologer_201(client, admin_setup):
    """POST /api/admin/users creates an astrologer user — 201."""
    resp = client.post(
        "/api/admin/users",
        json={
            "email": "new_astro_admin@test.com",
            "password": "password123",
            "name": "New Astrologer",
            "role": "astrologer",
        },
        headers=_auth_header(admin_setup["admin_token"]),
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["role"] == "astrologer"
    assert data["email"] == "new_astro_admin@test.com"


def test_admin_deactivate_user_200(client, db, admin_setup):
    """PATCH /api/admin/users/{id}/deactivate returns 200."""
    uid = admin_setup["reg_id"]
    resp = client.patch(
        f"/api/admin/users/{uid}/deactivate",
        headers=_auth_header(admin_setup["admin_token"]),
    )
    assert resp.status_code == 200
    assert resp.json()["is_active"] == 0


def test_admin_activate_user_200(client, db, admin_setup):
    """PATCH /api/admin/users/{id}/activate returns 200."""
    uid = admin_setup["reg_id"]
    resp = client.patch(
        f"/api/admin/users/{uid}/activate",
        headers=_auth_header(admin_setup["admin_token"]),
    )
    assert resp.status_code == 200
    assert resp.json()["is_active"] == 1


def test_admin_deactivate_self_400(client, admin_setup):
    """Admin cannot deactivate themselves — CHAOS #17."""
    resp = client.patch(
        f"/api/admin/users/{admin_setup['admin_id']}/deactivate",
        headers=_auth_header(admin_setup["admin_token"]),
    )
    assert resp.status_code == 400


def test_deactivated_user_login_403(client, db, admin_setup):
    """Deactivated user login returns 403 — CHAOS #16."""
    # Register a fresh user for this test
    new_user, _ = _register_user(client, "deact_login@test.com", name="Deact User", password="password123")
    # Deactivate
    client.patch(
        f"/api/admin/users/{new_user['id']}/deactivate",
        headers=_auth_header(admin_setup["admin_token"]),
    )
    # Try to login
    resp = client.post("/api/auth/login", json={"email": "deact_login@test.com", "password": "password123"})
    assert resp.status_code == 403


def test_admin_delete_own_account_400(client, db, admin_setup):
    """Admin cannot delete/deactivate own account — CHAOS #11.

    This app uses deactivation (not hard delete). Deactivating self is the closest analog.
    """
    resp = client.patch(
        f"/api/admin/users/{admin_setup['admin_id']}/deactivate",
        headers=_auth_header(admin_setup["admin_token"]),
    )
    assert resp.status_code == 400


# ---- Order Management ---- #

def test_admin_list_orders_200(client, admin_setup):
    """GET /api/admin/orders returns 200."""
    resp = client.get("/api/admin/orders", headers=_auth_header(admin_setup["admin_token"]))
    assert resp.status_code == 200
    data = resp.json()
    assert "orders" in data
    assert isinstance(data["orders"], list)


def test_admin_update_order_200(client, db, admin_setup):
    """PATCH /api/admin/orders/{id} updates status — 200."""
    # Insert a test order directly
    uid = admin_setup["reg_id"]
    db.execute(
        """INSERT INTO orders (user_id, status, total, shipping_address, payment_method, payment_status)
           VALUES (?, 'placed', 500.0, '123 Test Street, Delhi, 110001', 'cod', 'pending')""",
        (uid,),
    )
    db.commit()
    order_row = db.execute("SELECT id FROM orders WHERE user_id = ? ORDER BY rowid DESC LIMIT 1", (uid,)).fetchone()
    order_id = order_row["id"]

    resp = client.patch(
        f"/api/admin/orders/{order_id}",
        json={"status": "confirmed"},
        headers=_auth_header(admin_setup["admin_token"]),
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "confirmed"


# ---- Product Management ---- #

def test_admin_list_products_200(client, admin_setup):
    """GET /api/admin/products returns 200 with seeded products."""
    resp = client.get("/api/admin/products", headers=_auth_header(admin_setup["admin_token"]))
    assert resp.status_code == 200
    data = resp.json()
    assert "products" in data
    assert isinstance(data["products"], list)
    # Seed creates 12 products
    assert data["total"] >= 12


def test_admin_list_content_200(client, admin_setup):
    """GET /api/admin/content returns 200 with content items."""
    resp = client.get("/api/admin/content", headers=_auth_header(admin_setup["admin_token"]))
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert isinstance(data["items"], list)


def test_admin_create_product_201(client, admin_setup):
    """POST /api/admin/products creates a new product — 201."""
    resp = client.post(
        "/api/admin/products",
        json={
            "name": "Test Gemstone",
            "description": "A beautiful test gemstone for testing",
            "category": "gemstone",
            "price": 999.0,
            "stock": 50,
        },
        headers=_auth_header(admin_setup["admin_token"]),
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Test Gemstone"
    assert data["price"] == 999.0


def test_admin_create_content_201(client, admin_setup):
    """POST /api/admin/content creates content — 201."""
    resp = client.post(
        "/api/admin/content",
        json={
            "category": "aarti",
            "title": "Test Aarti",
            "content": "A test content body for admin coverage.",
            "sort_order": 99,
        },
        headers=_auth_header(admin_setup["admin_token"]),
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Test Aarti"
    assert data["category"] == "aarti"


def test_admin_update_stock_200(client, db, admin_setup):
    """PATCH /api/admin/products/{id}/stock updates stock — 200."""
    # Get first product
    prod = db.execute("SELECT id FROM products LIMIT 1").fetchone()
    pid = prod["id"]

    resp = client.patch(
        f"/api/admin/products/{pid}/stock?stock=100",
        headers=_auth_header(admin_setup["admin_token"]),
    )
    assert resp.status_code == 200
    assert resp.json()["stock"] == 100


# ---- Non-admin access ---- #

def test_non_admin_dashboard_403(client, admin_setup):
    """Non-admin accessing admin endpoints returns 403."""
    resp = client.get("/api/admin/dashboard", headers=_auth_header(admin_setup["reg_token"]))
    assert resp.status_code == 403

    resp = client.get("/api/admin/users", headers=_auth_header(admin_setup["reg_token"]))
    assert resp.status_code == 403
