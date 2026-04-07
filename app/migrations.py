"""H-02: Database Migration System — tracks and applies schema migrations in order."""
import psycopg2
import psycopg2.extras
from typing import List, Tuple, Any

from app.database import DATABASE_URL

# Each migration: (version, description, sql)
MIGRATIONS: List[Tuple[int, str, str]] = [
    (
        1,
        "Add audit_log table",
        """
        CREATE TABLE IF NOT EXISTS audit_log (
            id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
            user_id TEXT,
            action TEXT NOT NULL,
            resource TEXT,
            resource_id TEXT,
            details TEXT,
            ip_address TEXT,
            created_at TEXT NOT NULL DEFAULT to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS')
        );
        CREATE INDEX IF NOT EXISTS idx_audit_log_user ON audit_log(user_id);
        CREATE INDEX IF NOT EXISTS idx_audit_log_action ON audit_log(action);
        """,
    ),
    (
        2,
        "Add date_of_birth, gender, city, is_active columns to users",
        """
        SELECT 1;
        """,
    ),
    (
        3,
        "Add blog_posts table and seed starter editorial content",
        """
        CREATE TABLE IF NOT EXISTS blog_posts (
            id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
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
            published_at TEXT NOT NULL DEFAULT to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS'),
            created_at TEXT NOT NULL DEFAULT to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS'),
            updated_at TEXT NOT NULL DEFAULT to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS')
        );
        CREATE INDEX IF NOT EXISTS idx_blog_posts_slug ON blog_posts(slug);
        CREATE INDEX IF NOT EXISTS idx_blog_posts_published ON blog_posts(is_published, published_at DESC);
        """,
    ),
    (
        4,
        "Add email_verifications table for OTP-based registration",
        """
        CREATE TABLE IF NOT EXISTS email_verifications (
            id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
            email TEXT NOT NULL,
            otp TEXT NOT NULL,
            attempts INTEGER NOT NULL DEFAULT 0,
            expires_at TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS')
        );
        CREATE INDEX IF NOT EXISTS idx_email_verifications_email ON email_verifications(email);
        """,
    ),
]


def _ensure_migration_table(conn):
    """Create the applied_migrations table if it does not exist."""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS applied_migrations (
                version INTEGER PRIMARY KEY,
                description TEXT NOT NULL,
                applied_at TEXT NOT NULL DEFAULT to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS')
            )
        """)
    conn.commit()


def _safe_alter(conn, table: str, column: str, col_def: str):
    """Add a column only if it doesn't already exist."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT column_name FROM information_schema.columns
            WHERE table_name = %s AND column_name = %s
            """,
            (table, column),
        )
        exists = cur.fetchone()
    if not exists:
        with conn.cursor() as cur:
            cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_def}")
        conn.commit()


def run_migrations(db_path: str = None):
    """Check applied_migrations table and run any pending migrations in order.
    db_path parameter is kept for API compatibility but ignored (uses DATABASE_URL)."""
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False

    _ensure_migration_table(conn)

    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT version FROM applied_migrations")
        applied = {row["version"] for row in cur.fetchall()}

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
            # Execute each statement in the SQL block
            stmts = [s.strip() for s in sql.split(';') if s.strip()]
            with conn.cursor() as cur:
                for stmt in stmts:
                    try:
                        cur.execute(stmt)
                    except Exception:
                        conn.rollback()
            conn.commit()
            # Use a PgConnection-like wrapper for seed_blog_posts
            from app.database import PgConnection
            import psycopg2 as pg2
            raw = pg2.connect(DATABASE_URL)
            pg = PgConnection(raw)
            seed_blog_posts(pg)
            raw.commit()
            raw.close()
        else:
            stmts = [s.strip() for s in sql.split(';') if s.strip()]
            with conn.cursor() as cur:
                for stmt in stmts:
                    try:
                        cur.execute(stmt)
                    except Exception:
                        conn.rollback()
            conn.commit()

        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO applied_migrations (version, description) VALUES (%s, %s)",
                (version, description),
            )
        conn.commit()
        print(f"[migration] Applied v{version}: {description}")

    conn.close()
