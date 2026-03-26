"""Tests for Library routes — Gita chapters/verses and spiritual content library.

Covers: GET /api/gita/chapters, /api/gita/chapter/{ch}, /api/gita/verse/{ch}/{v},
        /api/library/{category}, /api/library/item/{id}.
Seed data: 18 gita chapters + 10 gita verses + 8 mantras + 5 aartis + 3 chalisas = 44 content.
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
    db_path = str(tmp_path / "test_library.db")
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
# Gita Chapter Tests
# ============================================================

def test_gita_chapters_list(client):
    """GET /api/gita/chapters -> 200, 18 chapters (from seed data)."""
    resp = client.get("/api/gita/chapters")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 18
    # Verify chapter structure
    first = data[0]
    assert "chapter" in first
    assert "title" in first
    assert "verses_count" in first


def test_gita_chapter_1(client):
    """GET /api/gita/chapter/1 -> 200, has title."""
    resp = client.get("/api/gita/chapter/1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["chapter"] == 1
    assert "title" in data
    assert len(data["title"]) > 0
    assert "verses" in data


def test_gita_chapter_19_not_found(client):
    """GET /api/gita/chapter/19 -> 400 (only 18 chapters)."""
    resp = client.get("/api/gita/chapter/19")
    assert resp.status_code == 400
    assert "between 1 and 18" in resp.json()["detail"]


def test_gita_verse_2_47(client):
    """GET /api/gita/verse/2/47 -> 200, has sanskrit, translation."""
    resp = client.get("/api/gita/verse/2/47")
    assert resp.status_code == 200
    data = resp.json()
    assert "sanskrit" in data
    assert "translation" in data
    assert "karmanye" in data["sanskrit"].lower()
    assert len(data["translation"]) > 0


def test_gita_verse_nonexistent(client):
    """GET /api/gita/verse/99/99 -> 404."""
    resp = client.get("/api/gita/verse/99/99")
    assert resp.status_code == 404


# ============================================================
# Spiritual Content Library Tests
# ============================================================

def test_library_mantra(client):
    """GET /api/library/mantra -> 200, has items (from seed)."""
    resp = client.get("/api/library/mantra")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 8  # 8 mantras seeded
    # Verify structure
    item = data[0]
    assert "id" in item
    assert "title" in item
    assert "content_preview" in item


def test_library_aarti(client):
    """GET /api/library/aarti -> 200."""
    resp = client.get("/api/library/aarti")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 5  # 5 aartis seeded


def test_library_chalisa(client):
    """GET /api/library/chalisa -> 200."""
    resp = client.get("/api/library/chalisa")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 3  # 3 chalisas seeded


def test_library_invalid_category(client):
    """GET /api/library/invalid_category -> 400."""
    resp = client.get("/api/library/invalid_category")
    assert resp.status_code == 400
    assert "Invalid category" in resp.json()["detail"]


def test_library_item_by_id(client, test_db):
    """GET /api/library/item/{id} -> 200."""
    # Get an actual item ID from the DB
    conn = sqlite3.connect(test_db)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT id FROM content_library WHERE category = 'mantra' LIMIT 1").fetchone()
    conn.close()
    item_id = row["id"]

    resp = client.get(f"/api/library/item/{item_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == item_id
    assert data["category"] == "mantra"
    assert "title" in data
    assert "content" in data


def test_library_item_nonexistent(client):
    """GET /api/library/item/{nonexistent} -> 404."""
    resp = client.get("/api/library/item/nonexistent_id_99999")
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()
