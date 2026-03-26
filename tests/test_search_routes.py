"""Tests for Global Search routes — FTS5 search across products, content, astrologers.

Covers: GET /api/search?q=, type filtering, empty results, missing query validation.
Seed data provides 12 products and 44 content items for search.
"""
import os
import importlib
import pytest
from fastapi.testclient import TestClient


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def test_db(tmp_path):
    """Create a fresh seeded test database with FTS indexes."""
    db_path = str(tmp_path / "test_search.db")
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

def test_search_ruby(client):
    """GET /api/search?q=ruby -> 200, finds Ruby gemstone."""
    resp = client.get("/api/search?q=ruby")
    assert resp.status_code == 200
    data = resp.json()
    assert "results" in data
    assert "total" in data
    assert data["total"] >= 1
    # Verify Ruby is in results
    titles = [r["title"].lower() for r in data["results"]]
    assert any("ruby" in t for t in titles), f"Ruby not found in: {titles}"


def test_search_gayatri(client):
    """GET /api/search?q=gayatri -> 200, finds Gayatri Mantra."""
    resp = client.get("/api/search?q=gayatri")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1
    titles = [r["title"].lower() for r in data["results"]]
    assert any("gayatri" in t for t in titles), f"Gayatri not found in: {titles}"


def test_search_nonexistent(client):
    """GET /api/search?q=xyznonexistent -> 200, empty results."""
    resp = client.get("/api/search?q=xyznonexistent")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0
    assert len(data["results"]) == 0


def test_search_type_products(client):
    """GET /api/search?q=ruby&type=products -> 200, only product results."""
    resp = client.get("/api/search?q=ruby&type=products")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1
    for r in data["results"]:
        assert r["type"] == "product"


def test_search_type_content(client):
    """GET /api/search?q=gita&type=content -> 200, only content results."""
    resp = client.get("/api/search?q=gita&type=content")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1
    for r in data["results"]:
        assert r["type"] == "content"


def test_search_missing_query(client):
    """GET /api/search without q -> 422 (required query param)."""
    resp = client.get("/api/search")
    assert resp.status_code == 422
