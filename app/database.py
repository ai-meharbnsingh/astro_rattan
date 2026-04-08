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
            minconn=1,
            maxconn=20,
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
        pool = _get_pool()
        pool.putconn(self._conn)

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
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- Kundli / Birth Charts
CREATE TABLE IF NOT EXISTS kundlis (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    person_name TEXT NOT NULL,
    birth_date TEXT NOT NULL,
    birth_time TEXT NOT NULL,
    birth_place TEXT NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    timezone_offset DOUBLE PRECISION NOT NULL,
    ayanamsa TEXT NOT NULL DEFAULT 'lahiri',
    chart_data TEXT NOT NULL,
    iogita_analysis TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_kundlis_user ON kundlis(user_id);

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

-- Blog / Editorial Content
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
    published_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_blog_posts_slug ON blog_posts(slug);
CREATE INDEX IF NOT EXISTS idx_blog_posts_published ON blog_posts(is_published, published_at DESC);

-- Prashnavali Logs
CREATE TABLE IF NOT EXISTS prashnavali_logs (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    prashnavali_type TEXT NOT NULL CHECK(prashnavali_type IN ('ram_shalaka','hanuman_prashna','ramcharitmanas','gita','yes_no_oracle','tarot')),
    question TEXT,
    result TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- AI Chat Logs
CREATE TABLE IF NOT EXISTS ai_chat_logs (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    chat_type TEXT NOT NULL CHECK(chat_type IN ('kundli_interpretation','ask_question','gita_ai','remedies','oracle')),
    kundli_id TEXT REFERENCES kundlis(id) ON DELETE CASCADE,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    model_used TEXT NOT NULL DEFAULT 'gpt-4',
    tokens_used INTEGER,
    rating INTEGER CHECK(rating IN (1, -1)),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_ai_chat_user ON ai_chat_logs(user_id);

-- E-Commerce: Products
CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('gemstone','rudraksha','bracelet','yantra','vastu')),
    price DOUBLE PRECISION NOT NULL CHECK(price > 0),
    compare_price DOUBLE PRECISION,
    image_url TEXT,
    images TEXT,
    weight TEXT,
    planet TEXT,
    properties TEXT,
    stock INTEGER NOT NULL DEFAULT 0,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_active ON products(is_active);

-- E-Commerce: Cart
CREATE TABLE IF NOT EXISTS cart_items (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    product_id TEXT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 1 CHECK(quantity > 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, product_id)
);
CREATE INDEX IF NOT EXISTS idx_cart_user ON cart_items(user_id);

-- E-Commerce: Orders
CREATE TABLE IF NOT EXISTS orders (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status TEXT NOT NULL DEFAULT 'placed' CHECK(status IN ('placed','confirmed','shipped','delivered','cancelled')),
    total DOUBLE PRECISION NOT NULL,
    shipping_address TEXT NOT NULL,
    payment_method TEXT NOT NULL CHECK(payment_method IN ('cod','razorpay','stripe')),
    payment_status TEXT NOT NULL DEFAULT 'pending' CHECK(payment_status IN ('pending','paid','failed','refunded')),
    tracking_number TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);

CREATE TABLE IF NOT EXISTS order_items (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    order_id TEXT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id TEXT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    price DOUBLE PRECISION NOT NULL,
    product_name TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);

-- Payments
CREATE TABLE IF NOT EXISTS payments (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    order_id TEXT REFERENCES orders(id) ON DELETE CASCADE,
    report_id TEXT,
    consultation_id TEXT,
    provider TEXT NOT NULL CHECK(provider IN ('razorpay','stripe','cod')),
    provider_payment_id TEXT,
    amount DOUBLE PRECISION NOT NULL,
    currency TEXT NOT NULL DEFAULT 'INR',
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','completed','failed','refunded')),
    metadata TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Consultation: Astrologer Profiles
CREATE TABLE IF NOT EXISTS astrologers (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    user_id TEXT UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    display_name TEXT NOT NULL,
    bio TEXT,
    specializations TEXT NOT NULL,
    experience_years INTEGER NOT NULL DEFAULT 0,
    per_minute_rate DOUBLE PRECISION NOT NULL,
    languages TEXT NOT NULL DEFAULT '["English"]',
    rating DOUBLE PRECISION DEFAULT 0.0,
    total_consultations INTEGER DEFAULT 0,
    is_available INTEGER NOT NULL DEFAULT 0,
    is_approved INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_astrologers_available ON astrologers(is_available, is_approved);

-- Consultations
CREATE TABLE IF NOT EXISTS consultations (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    astrologer_id TEXT NOT NULL REFERENCES astrologers(id) ON DELETE CASCADE,
    type TEXT NOT NULL CHECK(type IN ('chat','call','video')),
    status TEXT NOT NULL DEFAULT 'requested' CHECK(status IN ('requested','accepted','active','completed','cancelled')),
    scheduled_at TIMESTAMPTZ,
    started_at TIMESTAMPTZ,
    ended_at TIMESTAMPTZ,
    duration_minutes INTEGER,
    total_charge DOUBLE PRECISION,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_consultations_user ON consultations(user_id);
CREATE INDEX IF NOT EXISTS idx_consultations_astrologer ON consultations(astrologer_id);

-- Messages
CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    consultation_id TEXT NOT NULL REFERENCES consultations(id) ON DELETE CASCADE,
    sender_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    message_type TEXT NOT NULL DEFAULT 'text' CHECK(message_type IN ('text','image','file')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_messages_consultation ON messages(consultation_id);

-- Paid Reports
CREATE TABLE IF NOT EXISTS reports (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    kundli_id TEXT NOT NULL REFERENCES kundlis(id) ON DELETE CASCADE,
    report_type TEXT NOT NULL CHECK(report_type IN ('full_kundli','marriage','career','health','yearly')),
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','paid','generating','ready','failed')),
    content TEXT,
    pdf_url TEXT,
    price DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_reports_user ON reports(user_id);

-- Muhurat Cache
CREATE TABLE IF NOT EXISTS muhurat_cache (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    muhurat_type TEXT NOT NULL CHECK(muhurat_type IN ('marriage','griha_pravesh','business_start','travel','naming_ceremony','mundan')),
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    results TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(muhurat_type, year, month, latitude, longitude)
);

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

-- Product Bundles
CREATE TABLE IF NOT EXISTS product_bundles (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    name TEXT NOT NULL,
    description TEXT,
    bundle_type TEXT NOT NULL CHECK(bundle_type IN ('consultation_product','multi_product')),
    discount_percent DOUBLE PRECISION NOT NULL CHECK(discount_percent >= 0 AND discount_percent <= 100),
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_bundles_active ON product_bundles(is_active);

CREATE TABLE IF NOT EXISTS bundle_items (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    bundle_id TEXT NOT NULL REFERENCES product_bundles(id) ON DELETE CASCADE,
    product_id TEXT REFERENCES products(id) ON DELETE CASCADE,
    consultation_type TEXT CHECK(consultation_type IN ('chat','call','video')),
    quantity INTEGER NOT NULL DEFAULT 1 CHECK(quantity > 0)
);
CREATE INDEX IF NOT EXISTS idx_bundle_items_bundle ON bundle_items(bundle_id);

-- H-01: Audit Log
CREATE TABLE IF NOT EXISTS audit_log (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    user_id TEXT,
    action TEXT NOT NULL,
    resource TEXT,
    resource_id TEXT,
    details TEXT,
    ip_address TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_audit_log_user ON audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_action ON audit_log(action);

-- Referral / Affiliate System
CREATE TABLE IF NOT EXISTS referral_codes (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    code TEXT UNIQUE NOT NULL,
    user_id TEXT UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    discount_percent DOUBLE PRECISION NOT NULL DEFAULT 5.0,
    commission_percent DOUBLE PRECISION NOT NULL DEFAULT 10.0,
    uses_count INTEGER NOT NULL DEFAULT 0,
    max_uses INTEGER,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_referral_codes_code ON referral_codes(code);
CREATE INDEX IF NOT EXISTS idx_referral_codes_user ON referral_codes(user_id);

CREATE TABLE IF NOT EXISTS referral_earnings (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    referrer_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    referred_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    order_id TEXT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    amount DOUBLE PRECISION NOT NULL,
    commission DOUBLE PRECISION NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','paid')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_referral_earnings_referrer ON referral_earnings(referrer_id);
CREATE INDEX IF NOT EXISTS idx_referral_earnings_referred ON referral_earnings(referred_id);

-- Gamification: User Karma
CREATE TABLE IF NOT EXISTS user_karma (
    user_id TEXT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    total_points INTEGER NOT NULL DEFAULT 0,
    current_streak INTEGER NOT NULL DEFAULT 0,
    longest_streak INTEGER NOT NULL DEFAULT 0,
    last_activity_date TIMESTAMPTZ,
    level INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS karma_transactions (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    points INTEGER NOT NULL,
    action_type TEXT NOT NULL CHECK(action_type IN (
        'daily_login','kundli_generated','ai_chat','panchang_viewed',
        'shop_purchase','consultation_completed','library_read',
        'prashnavali_used','learning_completed'
    )),
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_karma_transactions_user ON karma_transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_karma_transactions_created ON karma_transactions(created_at);

CREATE TABLE IF NOT EXISTS user_badges (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    badge_id TEXT NOT NULL,
    earned_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, badge_id)
);
CREATE INDEX IF NOT EXISTS idx_user_badges_user ON user_badges(user_id);

CREATE TABLE IF NOT EXISTS learning_modules (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    title TEXT NOT NULL,
    description TEXT,
    category TEXT NOT NULL CHECK(category IN (
        'basics','kundli','panchang','doshas','remedies','advanced'
    )),
    order_index INTEGER NOT NULL DEFAULT 0,
    content_json TEXT NOT NULL DEFAULT '{}',
    points_reward INTEGER NOT NULL DEFAULT 50
);
CREATE INDEX IF NOT EXISTS idx_learning_modules_category ON learning_modules(category);
CREATE INDEX IF NOT EXISTS idx_learning_modules_order ON learning_modules(order_index);

CREATE TABLE IF NOT EXISTS learning_progress (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    module_id TEXT NOT NULL REFERENCES learning_modules(id) ON DELETE CASCADE,
    completed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, module_id)
);
CREATE INDEX IF NOT EXISTS idx_learning_progress_user ON learning_progress(user_id);

-- Notifications
CREATE TABLE IF NOT EXISTS user_notifications (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type TEXT NOT NULL CHECK(type IN ('transit','muhurat','festival','streak','content')),
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    is_read INTEGER NOT NULL DEFAULT 0,
    link TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_user_notifications_user ON user_notifications(user_id, is_read);
CREATE INDEX IF NOT EXISTS idx_user_notifications_created ON user_notifications(created_at DESC);

CREATE TABLE IF NOT EXISTS notification_preferences (
    user_id TEXT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    transit_alerts INTEGER NOT NULL DEFAULT 1,
    muhurat_alerts INTEGER NOT NULL DEFAULT 1,
    festival_alerts INTEGER NOT NULL DEFAULT 1,
    daily_digest INTEGER NOT NULL DEFAULT 1,
    email_notifications INTEGER NOT NULL DEFAULT 0
);

-- Forum / Community
CREATE TABLE IF NOT EXISTS forum_categories (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    icon TEXT,
    order_index INTEGER NOT NULL DEFAULT 0,
    is_active INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_forum_categories_order ON forum_categories(order_index);

CREATE TABLE IF NOT EXISTS forum_threads (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    category_id TEXT NOT NULL REFERENCES forum_categories(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    is_pinned INTEGER NOT NULL DEFAULT 0,
    is_locked INTEGER NOT NULL DEFAULT 0,
    views_count INTEGER NOT NULL DEFAULT 0,
    replies_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_forum_threads_category ON forum_threads(category_id);
CREATE INDEX IF NOT EXISTS idx_forum_threads_user ON forum_threads(user_id);
CREATE INDEX IF NOT EXISTS idx_forum_threads_created ON forum_threads(created_at);

CREATE TABLE IF NOT EXISTS forum_replies (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    thread_id TEXT NOT NULL REFERENCES forum_threads(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    is_best_answer INTEGER NOT NULL DEFAULT 0,
    likes_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_forum_replies_thread ON forum_replies(thread_id);
CREATE INDEX IF NOT EXISTS idx_forum_replies_user ON forum_replies(user_id);

CREATE TABLE IF NOT EXISTS forum_likes (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reply_id TEXT NOT NULL REFERENCES forum_replies(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, reply_id)
);
CREATE INDEX IF NOT EXISTS idx_forum_likes_reply ON forum_likes(reply_id);
CREATE INDEX IF NOT EXISTS idx_forum_likes_user ON forum_likes(user_id);

-- Astrologer Client Management
CREATE TABLE IF NOT EXISTS astrologer_clients (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    astrologer_user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    client_name TEXT NOT NULL,
    client_phone TEXT,
    client_email TEXT,
    birth_date TEXT,
    birth_time TEXT,
    birth_place TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    timezone_offset DOUBLE PRECISION DEFAULT 5.5,
    gender TEXT DEFAULT 'male',
    notes TEXT,
    kundli_id TEXT REFERENCES kundlis(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_astrologer_clients_astrologer ON astrologer_clients(astrologer_user_id);
CREATE INDEX IF NOT EXISTS idx_astrologer_clients_name ON astrologer_clients(client_name);

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

-- Applied Migrations Tracker
CREATE TABLE IF NOT EXISTS applied_migrations (
    version INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""

# Forum default categories seed data
FORUM_DEFAULT_CATEGORIES = [
    ("General Astrology", "Discuss all things astrology — transits, signs, and celestial events", "🌟", 1),
    ("Kundli Discussions", "Share and analyze birth charts, planetary positions, and dashas", "📜", 2),
    ("Remedies & Doshas", "Explore remedies for Mangal Dosha, Kaal Sarp Dosha, and more", "💎", 3),
    ("Panchang & Muhurat", "Discuss auspicious timings, tithis, nakshatras, and muhurat", "📅", 4),
    ("Spiritual Wisdom", "Vedic philosophy, mantras, meditation, and spiritual growth", "🕉️", 5),
    ("Tarot & Numerology", "Tarot readings, numerology insights, and divination discussions", "🔮", 6),
    ("Astrologer Picks", "Curated discussions and insights from professional astrologers", "⭐", 7),
    ("Beginner Questions", "New to astrology? Ask your questions here — no question is too basic!", "🌱", 8),
]


def init_db():
    """Initialize PostgreSQL database with schema. Creates all tables."""
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    try:
        with conn.cursor() as cur:
            # Ensure pgcrypto extension is available for gen_random_bytes
            try:
                cur.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
                conn.commit()
            except Exception as e:
                print(f"[init_db] Warning (pgcrypto): {e}")
                print(traceback.format_exc())
                conn.rollback()
            # Split and execute each statement individually
            statements = [s.strip() for s in SCHEMA.split(';') if s.strip()]
            for stmt in statements:
                try:
                    cur.execute(stmt)
                except Exception as e:
                    # Log but continue — some may already exist
                    print(f"[init_db] Warning: {e}")
                    conn.rollback()
                    continue
            conn.commit()

        # Seed forum categories
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            for name, description, icon, order_index in FORUM_DEFAULT_CATEGORIES:
                try:
                    cur.execute(
                        "INSERT INTO forum_categories (name, description, icon, order_index) VALUES (%s, %s, %s, %s) ON CONFLICT (name) DO NOTHING",
                        (name, description, icon, order_index),
                    )
                except Exception as e:
                    print(f"[init_db] Warning (forum seed): {e}")
                    print(traceback.format_exc())
                    conn.rollback()
                    continue
            conn.commit()

        print("[init_db] PostgreSQL schema initialized successfully.")
    finally:
        conn.close()


def get_db():
    """Yield a PgConnection wrapping a psycopg2 connection from the pool. Use as FastAPI dependency."""
    pool = _get_pool()
    raw_conn = pool.getconn()
    # Set autocommit off to use explicit transactions
    raw_conn.autocommit = False
    pg_conn = PgConnection(raw_conn)
    try:
        yield pg_conn
    except Exception:
        raw_conn.rollback()
        raise
    finally:
        pool.putconn(raw_conn)


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
