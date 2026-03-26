"""H-02: Database Migration System — tracks and applies schema migrations in order."""
import sqlite3
from typing import List, Tuple

from app.config import DB_PATH

# Each migration: (version, description, sql)
MIGRATIONS: List[Tuple[int, str, str]] = [
    (
        1,
        "Add audit_log table",
        """
        CREATE TABLE IF NOT EXISTS audit_log (
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
            user_id TEXT,
            action TEXT NOT NULL,
            resource TEXT,
            resource_id TEXT,
            details TEXT,
            ip_address TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_audit_log_user ON audit_log(user_id);
        CREATE INDEX IF NOT EXISTS idx_audit_log_action ON audit_log(action);
        """,
    ),
    (
        2,
        "Add date_of_birth, gender, city, is_active columns to users",
        """
        -- These columns may already exist from migrate_users_table; ALTER TABLE is idempotent
        -- via the safe_alter helper below. This migration is a no-op if columns exist.
        SELECT 1;
        """,
    ),
    (
        3,
        "Add blog_posts table and seed starter editorial content",
        """
        CREATE TABLE IF NOT EXISTS blog_posts (
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
            slug TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            excerpt TEXT NOT NULL,
            content TEXT NOT NULL,
            cover_image_url TEXT,
            tags TEXT NOT NULL DEFAULT '[]',
            author_name TEXT NOT NULL DEFAULT 'AstroVedic Editorial',
            seo_title TEXT,
            seo_description TEXT,
            is_published INTEGER NOT NULL DEFAULT 1,
            published_at TEXT NOT NULL DEFAULT (datetime('now')),
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_blog_posts_slug ON blog_posts(slug);
        CREATE INDEX IF NOT EXISTS idx_blog_posts_published ON blog_posts(is_published, published_at DESC);
        """,
    ),
]


def _ensure_migration_table(conn: sqlite3.Connection):
    """Create the applied_migrations table if it does not exist."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS applied_migrations (
            version INTEGER PRIMARY KEY,
            description TEXT NOT NULL,
            applied_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    conn.commit()


def _safe_alter(conn: sqlite3.Connection, table: str, column: str, col_def: str):
    """Add a column only if it doesn't already exist."""
    existing = [row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()]
    if column not in existing:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_def}")


def run_migrations(db_path: str = None):
    """Check applied_migrations table and run any pending migrations in order."""
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys=ON")

    _ensure_migration_table(conn)

    applied = {
        row[0]
        for row in conn.execute("SELECT version FROM applied_migrations").fetchall()
    }

    for version, description, sql in MIGRATIONS:
        if version in applied:
            continue

        # Special handling for migration 2: safe column adds
        if version == 2:
            _safe_alter(conn, "users", "date_of_birth", "TEXT")
            _safe_alter(conn, "users", "gender", "TEXT")
            _safe_alter(conn, "users", "city", "TEXT")
            _safe_alter(conn, "users", "is_active", "INTEGER DEFAULT 1")
        elif version == 3:
            from app.blog_seed import seed_blog_posts

            conn.executescript(sql)
            seed_blog_posts(conn)
        else:
            conn.executescript(sql)

        conn.execute(
            "INSERT INTO applied_migrations (version, description) VALUES (?, ?)",
            (version, description),
        )
        conn.commit()
        print(f"[migration] Applied v{version}: {description}")

    conn.close()
