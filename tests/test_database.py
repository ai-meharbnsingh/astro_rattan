"""RED phase: database tests."""
import os
import sqlite3
import pytest


@pytest.fixture
def test_db(tmp_path):
    """Create a temp database for testing."""
    db_path = str(tmp_path / "test.db")
    os.environ["DB_PATH"] = db_path
    from app.database import init_db, get_db
    init_db(db_path)
    yield db_path
    os.environ.pop("DB_PATH", None)


def test_init_db_creates_tables(test_db):
    conn = sqlite3.connect(test_db)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cursor.fetchall()}
    conn.close()
    assert "users" in tables
    assert "kundlis" in tables
    assert "products" in tables
    assert "orders" in tables
    assert "consultations" in tables
    assert "content_library" in tables


def test_init_db_creates_indexes(test_db):
    conn = sqlite3.connect(test_db)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='index'")
    indexes = {row[0] for row in cursor.fetchall()}
    conn.close()
    assert "idx_users_email" in indexes
    assert "idx_kundlis_user" in indexes


def test_get_db_yields_connection(test_db):
    from app.database import get_db
    gen = get_db()
    conn = next(gen)
    assert conn is not None
    assert hasattr(conn, "execute")
    try:
        next(gen)
    except StopIteration:
        pass
