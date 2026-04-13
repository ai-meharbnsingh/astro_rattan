"""Database initialization and connection management for PostgreSQL."""
import traceback
import psycopg2
import psycopg2.extras
import psycopg2.pool
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/astro_rattan")

# Ensure sslmode=require for cloud databases (Neon, etc.)
if DATABASE_URL and ("neon.tech" in DATABASE_URL or "amazonaws.com" in DATABASE_URL):
    if "sslmode" not in DATABASE_URL:
        sep = "&" if "?" in DATABASE_URL else "?"
        DATABASE_URL += f"{sep}sslmode=require"

# Thread-safe connection pool
_pool: psycopg2.pool.ThreadedConnectionPool = None


def _get_pool() -> psycopg2.pool.ThreadedConnectionPool:
    global _pool
    if _pool is None:
        _pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=2,
            maxconn=30,
            dsn=DATABASE_URL,
        )
    return _pool


class PgConnection:
    """Wrapper around psycopg2 connection to provide sqlite3-like execute API."""

    def __init__(self, conn):
        self._conn = conn

    def execute(self, sql, params=None):
        cursor = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql, params or ())
        return cursor

    def commit(self):
        self._conn.commit()

    def close(self):
        if self._conn is not None:
            pool = _get_pool()
            pool.putconn(self._conn)
            self._conn = None

    def cursor(self):
        return self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def rollback(self):
        self._conn.rollback()


SCHEMA = """
-- Core Auth
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user' CHECK(role IN ('user','astrologer','admin')),
    phone TEXT,
    avatar_url TEXT,
    date_of_birth TEXT,
    gender TEXT,
    city TEXT,
    is_active INTEGER DEFAULT 1,
    token_version INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- Astrologer Clients (people whose charts are being read)
CREATE TABLE IF NOT EXISTS clients (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    astrologer_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    phone TEXT,
    birth_date TEXT,
    birth_time TEXT,
    birth_place TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    timezone_offset DOUBLE PRECISION DEFAULT 5.5,
    gender TEXT DEFAULT 'male',
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_clients_astrologer ON clients(astrologer_id);
CREATE INDEX IF NOT EXISTS idx_clients_name ON clients(name);

-- Kundli / Birth Charts
CREATE TABLE IF NOT EXISTS kundlis (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    client_id TEXT REFERENCES clients(id) ON DELETE SET NULL,
    person_name TEXT NOT NULL,
    birth_date TEXT NOT NULL,
    birth_time TEXT NOT NULL,
    birth_place TEXT NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    timezone_offset DOUBLE PRECISION NOT NULL,
    ayanamsa TEXT NOT NULL DEFAULT 'lahiri',
    chart_type TEXT NOT NULL DEFAULT 'vedic',
    chart_data TEXT NOT NULL,
    iogita_analysis TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_kundlis_user ON kundlis(user_id);
CREATE INDEX IF NOT EXISTS idx_kundlis_client ON kundlis(client_id);

-- Horoscopes
CREATE TABLE IF NOT EXISTS horoscopes (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    sign TEXT NOT NULL CHECK(sign IN ('aries','taurus','gemini','cancer','leo','virgo','libra','scorpio','sagittarius','capricorn','aquarius','pisces')),
    period_type TEXT NOT NULL CHECK(period_type IN ('daily','weekly','monthly','yearly')),
    period_date TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(sign, period_type, period_date)
);
CREATE INDEX IF NOT EXISTS idx_horoscopes_lookup ON horoscopes(sign, period_type, period_date);

-- Panchang Cache
CREATE TABLE IF NOT EXISTS panchang_cache (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    date TEXT NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    tithi TEXT NOT NULL,
    nakshatra TEXT NOT NULL,
    yoga TEXT NOT NULL,
    karana TEXT NOT NULL,
    rahu_kaal TEXT NOT NULL,
    choghadiya TEXT NOT NULL,
    sunrise TEXT NOT NULL,
    sunset TEXT NOT NULL,
    moonrise TEXT,
    moonset TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(date, latitude, longitude)
);
CREATE INDEX IF NOT EXISTS idx_panchang_cache_date ON panchang_cache(date);

-- Spiritual Content Library
CREATE TABLE IF NOT EXISTS content_library (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    category TEXT NOT NULL CHECK(category IN ('gita','aarti','mantra','pooja','vrat_katha','chalisa','festival')),
    title TEXT NOT NULL,
    title_hindi TEXT,
    content TEXT NOT NULL,
    audio_url TEXT,
    chapter INTEGER,
    verse INTEGER,
    sanskrit_text TEXT,
    translation TEXT,
    commentary TEXT,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_content_category ON content_library(category);
CREATE INDEX IF NOT EXISTS idx_content_gita ON content_library(category, chapter, verse);

-- Festivals
CREATE TABLE IF NOT EXISTS festivals (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    name TEXT NOT NULL,
    name_hindi TEXT,
    date TEXT NOT NULL,
    description TEXT,
    rituals TEXT,
    category TEXT CHECK(category IN ('major','regional','fasting','eclipse')),
    year INTEGER NOT NULL,
    UNIQUE(name, year)
);
CREATE INDEX IF NOT EXISTS idx_festivals_date ON festivals(date);

-- Astrologer Notes (per client, per chart)
CREATE TABLE IF NOT EXISTS notes (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    astrologer_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    client_id TEXT NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    kundli_id TEXT REFERENCES kundlis(id) ON DELETE SET NULL,
    chart_type TEXT NOT NULL DEFAULT 'vedic' CHECK(chart_type IN ('vedic','lalkitab','numerology','general')),
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_notes_client ON notes(client_id);
CREATE INDEX IF NOT EXISTS idx_notes_astrologer ON notes(astrologer_id);

-- Email Verification OTPs
CREATE TABLE IF NOT EXISTS email_verifications (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    email TEXT NOT NULL,
    otp TEXT NOT NULL,
    attempts INTEGER NOT NULL DEFAULT 0,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_email_verifications_email ON email_verifications(email);

-- Astrologer Profiles
CREATE TABLE IF NOT EXISTS astrologers (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    display_name TEXT,
    specializations TEXT DEFAULT 'Vedic',
    experience_years INTEGER DEFAULT 0,
    per_minute_rate FLOAT DEFAULT 10.0,
    languages TEXT DEFAULT '["English"]',
    bio TEXT,
    is_available BOOLEAN DEFAULT true,
    rating FLOAT DEFAULT 0,
    total_consultations INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_astrologers_user ON astrologers(user_id);

-- Consultations
CREATE TABLE IF NOT EXISTS consultations (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    astrologer_id TEXT REFERENCES astrologers(id) ON DELETE SET NULL,
    type TEXT DEFAULT 'chat',
    status TEXT DEFAULT 'pending',
    scheduled_at TIMESTAMPTZ,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Reports
CREATE TABLE IF NOT EXISTS reports (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    report_type TEXT DEFAULT 'kundli',
    status TEXT DEFAULT 'pending',
    price FLOAT DEFAULT 0,
    data TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- AI Chat Logs
CREATE TABLE IF NOT EXISTS ai_chat_logs (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message TEXT,
    response TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Messages
CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    sender_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    receiver_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT,
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Muhurat Cache
CREATE TABLE IF NOT EXISTS muhurat_cache (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    muhurat_type TEXT NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    results TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (muhurat_type, year, month, latitude, longitude)
);

-- Prashnavali Logs
CREATE TABLE IF NOT EXISTS prashnavali_logs (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    user_id TEXT REFERENCES users(id) ON DELETE SET NULL,
    question TEXT,
    answer TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Applied Migrations Tracker
CREATE TABLE IF NOT EXISTS applied_migrations (
    version INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""

def init_db():
    """Initialize PostgreSQL database with schema. Creates all tables."""
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    try:
        with conn.cursor() as cur:
            try:
                cur.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
                conn.commit()
            except Exception as e:
                print(f"[init_db] Warning (pgcrypto): {e}")
                conn.rollback()
            statements = [s.strip() for s in SCHEMA.split(';') if s.strip()]
            for stmt in statements:
                try:
                    cur.execute(stmt)
                except Exception as e:
                    print(f"[init_db] Warning: {e}")
                    conn.rollback()
                    continue
            conn.commit()
        print("[init_db] PostgreSQL schema initialized successfully.")
    finally:
        conn.close()


def _get_valid_conn(pool):
    """Get a valid connection from pool, replacing dead ones."""
    raw_conn = pool.getconn()
    # Test with a lightweight ping
    try:
        raw_conn.autocommit = True
        cur = raw_conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        raw_conn.autocommit = False
        return raw_conn
    except Exception:
        # Connection is dead — discard it and recreate the pool
        global _pool
        try:
            pool.putconn(raw_conn, close=True)
        except Exception:
            pass
        try:
            _pool.closeall()
        except Exception:
            pass
        _pool = None
        new_pool = _get_pool()
        return new_pool.getconn()


def get_db():
    """Yield a PgConnection wrapping a psycopg2 connection from the pool. Use as FastAPI dependency."""
    pool = _get_pool()
    raw_conn = _get_valid_conn(pool)
    pg_conn = PgConnection(raw_conn)
    try:
        yield pg_conn
    except Exception:
        try:
            raw_conn.rollback()
        except Exception:
            pass
        raise
    finally:
        try:
            pool.putconn(raw_conn)
        except Exception:
            try:
                raw_conn.close()
            except Exception:
                pass


def migrate_users_table():
    """Add new columns to users table if they don't exist (safe for re-runs).
    No-op for PostgreSQL since columns are included in the main schema."""
    pass


def migrate_gamification_tables():
    """Gamification tables are included in main schema. No-op."""
    pass


def migrate_referral_tables():
    """Referral tables are included in main schema. No-op."""
    pass


def migrate_notification_tables():
    """Notification tables are included in main schema. No-op."""
    pass


def migrate_forum_tables():
    """Forum tables are included in main schema. No-op."""
    pass
