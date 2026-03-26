"""Tests for Product catalog routes and Palmistry guide.

Covers: GET /api/products, /api/products?category=, /api/products?page=&limit=,
        /api/products/{id}, /api/palmistry/guide.
Seed data: 12 products (3 gemstone, 3 rudraksha, 3 bracelet, 2 yantra, 1 vastu).
"""
import os
import sqlite3
import importlib
import pytest
from fastapi.testclient import TestClient


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def test_db(tmp_path):
    """Create a fresh seeded test database."""
    db_path = str(tmp_path / "test_products.db")
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


@pytest.fixture
def client(test_db):
    """TestClient with fresh seeded DB."""
    os.environ["DB_PATH"] = test_db
    import app.config
    importlib.reload(app.config)
    import app.database
    importlib.reload(app.database)

    from app.main import app
    return TestClient(app, raise_server_exceptions=False)


# ============================================================
# Tests
# ============================================================

def test_products_list_all(client):
    """GET /api/products -> 200, has products list (12 seeded)."""
    resp = client.get("/api/products")
    assert resp.status_code == 200
    data = resp.json()
    assert "products" in data
    assert "total" in data
    assert "page" in data
    assert data["total"] == 12
    assert len(data["products"]) == 12
    assert data["page"] == 1


def test_products_filter_gemstone(client):
    """GET /api/products?category=gemstone -> 200, filtered (3 gemstones)."""
    resp = client.get("/api/products?category=gemstone")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 3
    assert len(data["products"]) == 3
    # All should be gemstone category
    for p in data["products"]:
        assert p["category"] == "gemstone"


def test_products_filter_rudraksha(client):
    """GET /api/products?category=rudraksha -> 200 (3 items)."""
    resp = client.get("/api/products?category=rudraksha")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 3
    assert len(data["products"]) == 3
    for p in data["products"]:
        assert p["category"] == "rudraksha"


def test_products_pagination(client):
    """GET /api/products?page=1&limit=5 -> 200, pagination works."""
    resp = client.get("/api/products?page=1&limit=5")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 12  # Total unchanged
    assert len(data["products"]) == 5  # Only 5 per page
    assert data["page"] == 1

    # Page 2 should have another 5
    resp2 = client.get("/api/products?page=2&limit=5")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert len(data2["products"]) == 5
    assert data2["page"] == 2

    # Page 3 should have remaining 2
    resp3 = client.get("/api/products?page=3&limit=5")
    assert resp3.status_code == 200
    data3 = resp3.json()
    assert len(data3["products"]) == 2


def test_product_by_id(client, test_db):
    """GET /api/products/{id} -> 200, full detail."""
    # Get an actual product ID from the DB
    conn = sqlite3.connect(test_db)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT id, name FROM products LIMIT 1").fetchone()
    conn.close()
    product_id = row["id"]

    resp = client.get(f"/api/products/{product_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == product_id
    assert "name" in data
    assert "description" in data
    assert "category" in data
    assert "price" in data
    assert data["price"] > 0


def test_product_nonexistent(client):
    """GET /api/products/{nonexistent} -> 404."""
    resp = client.get("/api/products/nonexistent_product_id_99999")
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()


def test_palmistry_guide(client):
    """GET /api/palmistry/guide -> 200, has lines, mounts, shapes."""
    resp = client.get("/api/palmistry/guide")
    assert resp.status_code == 200
    data = resp.json()
    assert "lines" in data
    assert "mounts" in data
    assert "shapes" in data
    assert isinstance(data["lines"], list)
    assert len(data["lines"]) >= 4  # At least Heart, Head, Life, Fate
    assert isinstance(data["mounts"], list)
    assert len(data["mounts"]) >= 6  # Jupiter, Saturn, Apollo, Mercury, Venus, Moon, Mars
    assert isinstance(data["shapes"], list)
    assert len(data["shapes"]) == 4  # Earth, Air, Water, Fire
