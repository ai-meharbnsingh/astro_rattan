"""H-02: Database Migration System — tracks and applies schema migrations in order."""
import traceback
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
    (
        5,
        "Add ON DELETE CASCADE to all foreign key constraints",
        # SQL is not used — handled via special Python logic in run_migrations
        "SELECT 1;",
    ),
    (
        6,
        "Convert date/time columns from TEXT to TIMESTAMPTZ",
        # SQL is not used — handled via special Python logic in run_migrations
        "SELECT 1;",
    ),
]


# ---- Migration 5 helper: re-create all FK constraints with ON DELETE CASCADE ----

# (child_table, fk_column(s), parent_table, parent_column(s))
_FK_CASCADE_SPEC = [
    ("kundlis", ["user_id"], "users", ["id"]),
    ("prashnavali_logs", ["user_id"], "users", ["id"]),
    ("ai_chat_logs", ["user_id"], "users", ["id"]),
    ("ai_chat_logs", ["kundli_id"], "kundlis", ["id"]),
    ("cart_items", ["user_id"], "users", ["id"]),
    ("cart_items", ["product_id"], "products", ["id"]),
    ("orders", ["user_id"], "users", ["id"]),
    ("order_items", ["order_id"], "orders", ["id"]),
    ("order_items", ["product_id"], "products", ["id"]),
    ("payments", ["order_id"], "orders", ["id"]),
    ("astrologers", ["user_id"], "users", ["id"]),
    ("consultations", ["user_id"], "users", ["id"]),
    ("consultations", ["astrologer_id"], "astrologers", ["id"]),
    ("messages", ["consultation_id"], "consultations", ["id"]),
    ("messages", ["sender_id"], "users", ["id"]),
    ("reports", ["user_id"], "users", ["id"]),
    ("reports", ["kundli_id"], "kundlis", ["id"]),
    ("bundle_items", ["bundle_id"], "product_bundles", ["id"]),
    ("bundle_items", ["product_id"], "products", ["id"]),
    ("referral_codes", ["user_id"], "users", ["id"]),
    ("referral_earnings", ["referrer_id"], "users", ["id"]),
    ("referral_earnings", ["referred_id"], "users", ["id"]),
    ("referral_earnings", ["order_id"], "orders", ["id"]),
    ("user_karma", ["user_id"], "users", ["id"]),
    ("karma_transactions", ["user_id"], "users", ["id"]),
    ("user_badges", ["user_id"], "users", ["id"]),
    ("learning_progress", ["user_id"], "users", ["id"]),
    ("learning_progress", ["module_id"], "learning_modules", ["id"]),
    ("user_notifications", ["user_id"], "users", ["id"]),
    ("notification_preferences", ["user_id"], "users", ["id"]),
    ("forum_threads", ["category_id"], "forum_categories", ["id"]),
    ("forum_threads", ["user_id"], "users", ["id"]),
    ("forum_replies", ["thread_id"], "forum_threads", ["id"]),
    ("forum_replies", ["user_id"], "users", ["id"]),
    ("forum_likes", ["user_id"], "users", ["id"]),
    ("forum_likes", ["reply_id"], "forum_replies", ["id"]),
    ("astrologer_clients", ["astrologer_user_id"], "users", ["id"]),
    ("astrologer_clients", ["kundli_id"], "kundlis", ["id"]),
]


def _apply_cascade_migration(conn):
    """Drop and recreate every FK constraint with ON DELETE CASCADE.

    Looks up the auto-generated constraint name from pg_constraint,
    drops it, and adds a new one with CASCADE.  Idempotent — skips
    any FK that already has CASCADE or whose constraint is missing
    (e.g. table not yet created).
    """
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        for child_table, fk_cols, parent_table, parent_cols in _FK_CASCADE_SPEC:
            # Find the constraint name for this FK
            cur.execute("""
                SELECT con.conname, con.confdeltype
                FROM pg_constraint con
                JOIN pg_class rel ON rel.oid = con.conrelid
                JOIN pg_namespace nsp ON nsp.oid = rel.relnamespace
                WHERE rel.relname = %s
                  AND nsp.nspname = 'public'
                  AND con.contype = 'f'
                  AND EXISTS (
                      SELECT 1
                      FROM unnest(con.conkey) WITH ORDINALITY AS ck(attnum, ord)
                      JOIN pg_attribute a ON a.attrelid = con.conrelid AND a.attnum = ck.attnum
                      WHERE a.attname = %s
                  )
            """, (child_table, fk_cols[0]))
            rows = cur.fetchall()
            if not rows:
                # Table or FK doesn't exist yet — skip
                continue
            for row in rows:
                if row["confdeltype"] == "c":
                    # Already CASCADE — nothing to do
                    continue
                constraint_name = row["conname"]
                fk_col_list = ", ".join(fk_cols)
                parent_col_list = ", ".join(parent_cols)
                new_constraint = f"fk_{child_table}_{'_'.join(fk_cols)}_cascade"
                try:
                    cur.execute(
                        f"ALTER TABLE {child_table} DROP CONSTRAINT {constraint_name}"
                    )
                    cur.execute(
                        f"ALTER TABLE {child_table} ADD CONSTRAINT {new_constraint} "
                        f"FOREIGN KEY ({fk_col_list}) REFERENCES {parent_table}({parent_col_list}) "
                        f"ON DELETE CASCADE"
                    )
                except Exception as e:
                    print(f"[migration] Warning: cascade for {child_table}.{fk_col_list}: {e}")
                    conn.rollback()
    conn.commit()


_TIMESTAMPTZ_COLUMNS = [
    # (table, column, has_default)
    ("users", "created_at", True),
    ("users", "updated_at", True),
    ("kundlis", "created_at", True),
    ("horoscopes", "created_at", True),
    ("panchang_cache", "created_at", True),
    ("content_library", "created_at", True),
    ("blog_posts", "published_at", True),
    ("blog_posts", "created_at", True),
    ("blog_posts", "updated_at", True),
    ("prashnavali_logs", "created_at", True),
    ("ai_chat_logs", "created_at", True),
    ("products", "created_at", True),
    ("products", "updated_at", True),
    ("cart_items", "created_at", True),
    ("orders", "created_at", True),
    ("orders", "updated_at", True),
    ("payments", "created_at", True),
    ("astrologers", "created_at", True),
    ("consultations", "scheduled_at", False),
    ("consultations", "started_at", False),
    ("consultations", "ended_at", False),
    ("consultations", "created_at", True),
    ("messages", "created_at", True),
    ("reports", "created_at", True),
    ("muhurat_cache", "created_at", True),
    ("product_bundles", "created_at", True),
    ("audit_log", "created_at", True),
    ("referral_codes", "created_at", True),
    ("referral_codes", "updated_at", True),
    ("referral_earnings", "created_at", True),
    ("user_karma", "last_activity_date", False),
    ("user_karma", "created_at", True),
    ("karma_transactions", "created_at", True),
    ("user_badges", "earned_at", True),
    ("learning_progress", "completed_at", True),
    ("user_notifications", "created_at", True),
    ("forum_threads", "created_at", True),
    ("forum_threads", "updated_at", True),
    ("forum_replies", "created_at", True),
    ("forum_replies", "updated_at", True),
    ("forum_likes", "created_at", True),
    ("astrologer_clients", "created_at", True),
    ("astrologer_clients", "updated_at", True),
    ("email_verifications", "expires_at", False),
    ("email_verifications", "created_at", True),
    ("applied_migrations", "applied_at", True),
]


def _apply_timestamptz_migration(conn):
    """Convert TEXT date/time columns to TIMESTAMPTZ.

    Uses USING column::timestamptz to cast existing ISO-8601 text values.
    Skips columns that are already TIMESTAMPTZ (idempotent).
    """
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        for table, column, has_default in _TIMESTAMPTZ_COLUMNS:
            # Check if table and column exist and what the current type is
            cur.execute("""
                SELECT data_type FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = %s
                  AND column_name = %s
            """, (table, column))
            row = cur.fetchone()
            if not row:
                # Table or column doesn't exist yet — skip
                continue
            if row["data_type"] in (
                "timestamp with time zone",
                "timestamp without time zone",
            ):
                # Already a timestamp type — skip
                continue
            try:
                cur.execute(
                    f"ALTER TABLE {table} ALTER COLUMN {column} "
                    f"TYPE TIMESTAMPTZ USING {column}::timestamptz"
                )
                if has_default:
                    cur.execute(
                        f"ALTER TABLE {table} ALTER COLUMN {column} "
                        f"SET DEFAULT NOW()"
                    )
                print(f"[migration] Converted {table}.{column} to TIMESTAMPTZ")
            except Exception as e:
                print(f"[migration] Warning: {table}.{column}: {e}")
                conn.rollback()
    conn.commit()


def _ensure_migration_table(conn):
    """Create the applied_migrations table if it does not exist."""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS applied_migrations (
                version INTEGER PRIMARY KEY,
                description TEXT NOT NULL,
                applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
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

        # Special handling for specific migrations
        if version == 6:
            _apply_timestamptz_migration(conn)
        elif version == 5:
            _apply_cascade_migration(conn)
        elif version == 2:
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
                    except Exception as e:
                        print(f"[migration] Warning in v{version} statement: {e}")
                        print(traceback.format_exc())
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
                    except Exception as e:
                        print(f"[migration] Warning in v{version} statement: {e}")
                        print(traceback.format_exc())
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
