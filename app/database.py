"""Database initialization and connection management for SQLite WAL."""
import sqlite3
import os
from app.config import DB_PATH

SCHEMA = """
-- Core Auth
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user' CHECK(role IN ('user','astrologer','admin')),
    phone TEXT,
    avatar_url TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- Kundli / Birth Charts
CREATE TABLE IF NOT EXISTS kundlis (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT NOT NULL REFERENCES users(id),
    person_name TEXT NOT NULL,
    birth_date TEXT NOT NULL,
    birth_time TEXT NOT NULL,
    birth_place TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    timezone_offset REAL NOT NULL,
    ayanamsa TEXT NOT NULL DEFAULT 'lahiri',
    chart_data TEXT NOT NULL,
    iogita_analysis TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_kundlis_user ON kundlis(user_id);

-- Horoscopes
CREATE TABLE IF NOT EXISTS horoscopes (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    sign TEXT NOT NULL CHECK(sign IN ('aries','taurus','gemini','cancer','leo','virgo','libra','scorpio','sagittarius','capricorn','aquarius','pisces')),
    period_type TEXT NOT NULL CHECK(period_type IN ('daily','weekly','monthly','yearly')),
    period_date TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(sign, period_type, period_date)
);
CREATE INDEX IF NOT EXISTS idx_horoscopes_lookup ON horoscopes(sign, period_type, period_date);

-- Panchang Cache
CREATE TABLE IF NOT EXISTS panchang_cache (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    date TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
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
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(date, latitude, longitude)
);

-- Spiritual Content Library
CREATE TABLE IF NOT EXISTS content_library (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
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
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_content_category ON content_library(category);
CREATE INDEX IF NOT EXISTS idx_content_gita ON content_library(category, chapter, verse);

-- Blog / Editorial Content
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

-- Prashnavali Logs
CREATE TABLE IF NOT EXISTS prashnavali_logs (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT REFERENCES users(id),
    prashnavali_type TEXT NOT NULL CHECK(prashnavali_type IN ('ram_shalaka','hanuman_prashna','ramcharitmanas','gita','yes_no_oracle','tarot')),
    question TEXT,
    result TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- AI Chat Logs
CREATE TABLE IF NOT EXISTS ai_chat_logs (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT NOT NULL REFERENCES users(id),
    chat_type TEXT NOT NULL CHECK(chat_type IN ('kundli_interpretation','ask_question','gita_ai','remedies','oracle')),
    kundli_id TEXT REFERENCES kundlis(id),
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    model_used TEXT NOT NULL DEFAULT 'gpt-4',
    tokens_used INTEGER,
    rating INTEGER CHECK(rating IN (1, -1)),
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_ai_chat_user ON ai_chat_logs(user_id);

-- E-Commerce: Products
CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('gemstone','rudraksha','bracelet','yantra','vastu')),
    price REAL NOT NULL CHECK(price > 0),
    compare_price REAL,
    image_url TEXT,
    images TEXT,
    weight TEXT,
    planet TEXT,
    properties TEXT,
    stock INTEGER NOT NULL DEFAULT 0,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_active ON products(is_active);

-- E-Commerce: Cart
CREATE TABLE IF NOT EXISTS cart_items (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT NOT NULL REFERENCES users(id),
    product_id TEXT NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL DEFAULT 1 CHECK(quantity > 0),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(user_id, product_id)
);
CREATE INDEX IF NOT EXISTS idx_cart_user ON cart_items(user_id);

-- E-Commerce: Orders
CREATE TABLE IF NOT EXISTS orders (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT NOT NULL REFERENCES users(id),
    status TEXT NOT NULL DEFAULT 'placed' CHECK(status IN ('placed','confirmed','shipped','delivered','cancelled')),
    total REAL NOT NULL,
    shipping_address TEXT NOT NULL,
    payment_method TEXT NOT NULL CHECK(payment_method IN ('cod','razorpay','stripe')),
    payment_status TEXT NOT NULL DEFAULT 'pending' CHECK(payment_status IN ('pending','paid','failed','refunded')),
    tracking_number TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);

CREATE TABLE IF NOT EXISTS order_items (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    order_id TEXT NOT NULL REFERENCES orders(id),
    product_id TEXT NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    price REAL NOT NULL,
    product_name TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);

-- Payments
CREATE TABLE IF NOT EXISTS payments (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    order_id TEXT REFERENCES orders(id),
    report_id TEXT,
    consultation_id TEXT,
    provider TEXT NOT NULL CHECK(provider IN ('razorpay','stripe','cod')),
    provider_payment_id TEXT,
    amount REAL NOT NULL,
    currency TEXT NOT NULL DEFAULT 'INR',
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','completed','failed','refunded')),
    metadata TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Consultation: Astrologer Profiles
CREATE TABLE IF NOT EXISTS astrologers (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT UNIQUE NOT NULL REFERENCES users(id),
    display_name TEXT NOT NULL,
    bio TEXT,
    specializations TEXT NOT NULL,
    experience_years INTEGER NOT NULL DEFAULT 0,
    per_minute_rate REAL NOT NULL,
    languages TEXT NOT NULL DEFAULT '["English"]',
    rating REAL DEFAULT 0.0,
    total_consultations INTEGER DEFAULT 0,
    is_available INTEGER NOT NULL DEFAULT 0,
    is_approved INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_astrologers_available ON astrologers(is_available, is_approved);

-- Consultations
CREATE TABLE IF NOT EXISTS consultations (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT NOT NULL REFERENCES users(id),
    astrologer_id TEXT NOT NULL REFERENCES astrologers(id),
    type TEXT NOT NULL CHECK(type IN ('chat','call','video')),
    status TEXT NOT NULL DEFAULT 'requested' CHECK(status IN ('requested','accepted','active','completed','cancelled')),
    scheduled_at TEXT,
    started_at TEXT,
    ended_at TEXT,
    duration_minutes INTEGER,
    total_charge REAL,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_consultations_user ON consultations(user_id);
CREATE INDEX IF NOT EXISTS idx_consultations_astrologer ON consultations(astrologer_id);

-- Messages
CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    consultation_id TEXT NOT NULL REFERENCES consultations(id),
    sender_id TEXT NOT NULL REFERENCES users(id),
    content TEXT NOT NULL,
    message_type TEXT NOT NULL DEFAULT 'text' CHECK(message_type IN ('text','image','file')),
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_messages_consultation ON messages(consultation_id);

-- Paid Reports
CREATE TABLE IF NOT EXISTS reports (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT NOT NULL REFERENCES users(id),
    kundli_id TEXT NOT NULL REFERENCES kundlis(id),
    report_type TEXT NOT NULL CHECK(report_type IN ('full_kundli','marriage','career','health','yearly')),
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','paid','generating','ready','failed')),
    content TEXT,
    pdf_url TEXT,
    price REAL NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_reports_user ON reports(user_id);

-- Muhurat Cache
CREATE TABLE IF NOT EXISTS muhurat_cache (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    muhurat_type TEXT NOT NULL CHECK(muhurat_type IN ('marriage','griha_pravesh','business_start','travel','naming_ceremony','mundan')),
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    results TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Festivals
CREATE TABLE IF NOT EXISTS festivals (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
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
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    name TEXT NOT NULL,
    description TEXT,
    bundle_type TEXT NOT NULL CHECK(bundle_type IN ('consultation_product','multi_product')),
    discount_percent REAL NOT NULL CHECK(discount_percent >= 0 AND discount_percent <= 100),
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_bundles_active ON product_bundles(is_active);

CREATE TABLE IF NOT EXISTS bundle_items (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    bundle_id TEXT NOT NULL REFERENCES product_bundles(id),
    product_id TEXT REFERENCES products(id),
    consultation_type TEXT CHECK(consultation_type IN ('chat','call','video')),
    quantity INTEGER NOT NULL DEFAULT 1 CHECK(quantity > 0)
);
CREATE INDEX IF NOT EXISTS idx_bundle_items_bundle ON bundle_items(bundle_id);

-- H-01: Audit Log
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

-- Referral / Affiliate System
CREATE TABLE IF NOT EXISTS referral_codes (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    code TEXT UNIQUE NOT NULL,
    user_id TEXT UNIQUE NOT NULL REFERENCES users(id),
    discount_percent REAL NOT NULL DEFAULT 5.0,
    commission_percent REAL NOT NULL DEFAULT 10.0,
    uses_count INTEGER NOT NULL DEFAULT 0,
    max_uses INTEGER,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_referral_codes_code ON referral_codes(code);
CREATE INDEX IF NOT EXISTS idx_referral_codes_user ON referral_codes(user_id);

CREATE TABLE IF NOT EXISTS referral_earnings (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    referrer_id TEXT NOT NULL REFERENCES users(id),
    referred_id TEXT NOT NULL REFERENCES users(id),
    order_id TEXT NOT NULL REFERENCES orders(id),
    amount REAL NOT NULL,
    commission REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','paid')),
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_referral_earnings_referrer ON referral_earnings(referrer_id);
CREATE INDEX IF NOT EXISTS idx_referral_earnings_referred ON referral_earnings(referred_id);
"""

# H-11: FTS5 setup — run separately since CREATE VIRTUAL TABLE can't be in executescript with IF NOT EXISTS checks
FTS_SCHEMA = """
CREATE VIRTUAL TABLE IF NOT EXISTS products_fts USING fts5(name, description, category, content=products, content_rowid=rowid);
CREATE VIRTUAL TABLE IF NOT EXISTS content_fts USING fts5(title, content, category, content=content_library, content_rowid=rowid);
"""

FTS_TRIGGERS = """
-- Triggers to keep products_fts in sync
CREATE TRIGGER IF NOT EXISTS products_ai AFTER INSERT ON products BEGIN
    INSERT INTO products_fts(rowid, name, description, category) VALUES (new.rowid, new.name, new.description, new.category);
END;
CREATE TRIGGER IF NOT EXISTS products_ad AFTER DELETE ON products BEGIN
    INSERT INTO products_fts(products_fts, rowid, name, description, category) VALUES('delete', old.rowid, old.name, old.description, old.category);
END;
CREATE TRIGGER IF NOT EXISTS products_au AFTER UPDATE ON products BEGIN
    INSERT INTO products_fts(products_fts, rowid, name, description, category) VALUES('delete', old.rowid, old.name, old.description, old.category);
    INSERT INTO products_fts(rowid, name, description, category) VALUES (new.rowid, new.name, new.description, new.category);
END;

-- Triggers to keep content_fts in sync
CREATE TRIGGER IF NOT EXISTS content_ai AFTER INSERT ON content_library BEGIN
    INSERT INTO content_fts(rowid, title, content, category) VALUES (new.rowid, new.title, new.content, new.category);
END;
CREATE TRIGGER IF NOT EXISTS content_ad AFTER DELETE ON content_library BEGIN
    INSERT INTO content_fts(content_fts, rowid, title, content, category) VALUES('delete', old.rowid, old.title, old.content, old.category);
END;
CREATE TRIGGER IF NOT EXISTS content_au AFTER UPDATE ON content_library BEGIN
    INSERT INTO content_fts(content_fts, rowid, title, content, category) VALUES('delete', old.rowid, old.title, old.content, old.category);
    INSERT INTO content_fts(rowid, title, content, category) VALUES (new.rowid, new.title, new.content, new.category);
END;
"""


def init_db(db_path: str = None):
    """Initialize database with schema. Creates all tables including FTS5."""
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(SCHEMA)
    conn.commit()
    # FTS5 virtual tables — each statement must run individually
    for stmt in FTS_SCHEMA.strip().split(";"):
        stmt = stmt.strip()
        if stmt:
            try:
                conn.execute(stmt)
            except sqlite3.OperationalError:
                pass  # Table may already exist
    conn.commit()
    # FTS sync triggers — use executescript because triggers contain internal semicolons
    try:
        conn.executescript(FTS_TRIGGERS)
    except sqlite3.OperationalError:
        pass  # Triggers may already exist or FTS tables missing
    conn.commit()
    # Rebuild FTS indexes from existing data
    _rebuild_fts(conn)
    conn.close()


def _rebuild_fts(conn: sqlite3.Connection):
    """Rebuild FTS indexes from existing table data."""
    try:
        conn.execute("INSERT INTO products_fts(products_fts) VALUES('rebuild')")
    except sqlite3.OperationalError:
        pass
    try:
        conn.execute("INSERT INTO content_fts(content_fts) VALUES('rebuild')")
    except sqlite3.OperationalError:
        pass
    conn.commit()


def migrate_users_table(db_path: str = None):
    """Add new columns to users table if they don't exist (safe for re-runs)."""
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    existing = [row[1] for row in conn.execute("PRAGMA table_info(users)").fetchall()]
    for col, sql in [
        ("date_of_birth", "ALTER TABLE users ADD COLUMN date_of_birth TEXT"),
        ("gender", "ALTER TABLE users ADD COLUMN gender TEXT"),
        ("city", "ALTER TABLE users ADD COLUMN city TEXT"),
        ("is_active", "ALTER TABLE users ADD COLUMN is_active INTEGER DEFAULT 1"),
    ]:
        if col not in existing:
            conn.execute(sql)
    conn.commit()
    conn.close()


def migrate_gamification_tables(db_path: str = None):
    """Create gamification tables if they don't exist (safe for re-runs)."""
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS user_karma (
            user_id TEXT PRIMARY KEY REFERENCES users(id),
            total_points INTEGER NOT NULL DEFAULT 0,
            current_streak INTEGER NOT NULL DEFAULT 0,
            longest_streak INTEGER NOT NULL DEFAULT 0,
            last_activity_date TEXT,
            level INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS karma_transactions (
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
            user_id TEXT NOT NULL REFERENCES users(id),
            points INTEGER NOT NULL,
            action_type TEXT NOT NULL CHECK(action_type IN (
                'daily_login','kundli_generated','ai_chat','panchang_viewed',
                'shop_purchase','consultation_completed','library_read',
                'prashnavali_used','learning_completed'
            )),
            description TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_karma_transactions_user ON karma_transactions(user_id);
        CREATE INDEX IF NOT EXISTS idx_karma_transactions_created ON karma_transactions(created_at);

        CREATE TABLE IF NOT EXISTS user_badges (
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
            user_id TEXT NOT NULL REFERENCES users(id),
            badge_id TEXT NOT NULL,
            earned_at TEXT NOT NULL DEFAULT (datetime('now')),
            UNIQUE(user_id, badge_id)
        );
        CREATE INDEX IF NOT EXISTS idx_user_badges_user ON user_badges(user_id);

        CREATE TABLE IF NOT EXISTS learning_modules (
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
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
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
            user_id TEXT NOT NULL REFERENCES users(id),
            module_id TEXT NOT NULL REFERENCES learning_modules(id),
            completed_at TEXT NOT NULL DEFAULT (datetime('now')),
            UNIQUE(user_id, module_id)
        );
        CREATE INDEX IF NOT EXISTS idx_learning_progress_user ON learning_progress(user_id);
    """)
    conn.commit()
    conn.close()


def migrate_referral_tables(db_path: str = None):
    """Create referral_codes and referral_earnings tables if they don't exist (safe for re-runs)."""
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS referral_codes (
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
            code TEXT UNIQUE NOT NULL,
            user_id TEXT UNIQUE NOT NULL REFERENCES users(id),
            discount_percent REAL NOT NULL DEFAULT 5.0,
            commission_percent REAL NOT NULL DEFAULT 10.0,
            uses_count INTEGER NOT NULL DEFAULT 0,
            max_uses INTEGER,
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_referral_codes_code ON referral_codes(code);
        CREATE INDEX IF NOT EXISTS idx_referral_codes_user ON referral_codes(user_id);

        CREATE TABLE IF NOT EXISTS referral_earnings (
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
            referrer_id TEXT NOT NULL REFERENCES users(id),
            referred_id TEXT NOT NULL REFERENCES users(id),
            order_id TEXT NOT NULL REFERENCES orders(id),
            amount REAL NOT NULL,
            commission REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','paid')),
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_referral_earnings_referrer ON referral_earnings(referrer_id);
        CREATE INDEX IF NOT EXISTS idx_referral_earnings_referred ON referral_earnings(referred_id);
    """)
    conn.commit()
    conn.close()


def migrate_notification_tables(db_path: str = None):
    """Create notification tables if they don't exist (safe for re-runs)."""
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS user_notifications (
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
            user_id TEXT NOT NULL REFERENCES users(id),
            type TEXT NOT NULL CHECK(type IN ('transit','muhurat','festival','streak','content')),
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            is_read INTEGER NOT NULL DEFAULT 0,
            link TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_user_notifications_user ON user_notifications(user_id, is_read);
        CREATE INDEX IF NOT EXISTS idx_user_notifications_created ON user_notifications(created_at DESC);

        CREATE TABLE IF NOT EXISTS notification_preferences (
            user_id TEXT PRIMARY KEY REFERENCES users(id),
            transit_alerts INTEGER NOT NULL DEFAULT 1,
            muhurat_alerts INTEGER NOT NULL DEFAULT 1,
            festival_alerts INTEGER NOT NULL DEFAULT 1,
            daily_digest INTEGER NOT NULL DEFAULT 1,
            email_notifications INTEGER NOT NULL DEFAULT 0
        );
    """)
    conn.commit()
    conn.close()


def migrate_forum_tables(db_path: str = None):
    """Create forum tables and seed default categories (safe for re-runs)."""
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS forum_categories (
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            icon TEXT,
            order_index INTEGER NOT NULL DEFAULT 0,
            is_active INTEGER NOT NULL DEFAULT 1
        );
        CREATE INDEX IF NOT EXISTS idx_forum_categories_order ON forum_categories(order_index);

        CREATE TABLE IF NOT EXISTS forum_threads (
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
            category_id TEXT NOT NULL REFERENCES forum_categories(id),
            user_id TEXT NOT NULL REFERENCES users(id),
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            is_pinned INTEGER NOT NULL DEFAULT 0,
            is_locked INTEGER NOT NULL DEFAULT 0,
            views_count INTEGER NOT NULL DEFAULT 0,
            replies_count INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_forum_threads_category ON forum_threads(category_id);
        CREATE INDEX IF NOT EXISTS idx_forum_threads_user ON forum_threads(user_id);
        CREATE INDEX IF NOT EXISTS idx_forum_threads_created ON forum_threads(created_at);

        CREATE TABLE IF NOT EXISTS forum_replies (
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
            thread_id TEXT NOT NULL REFERENCES forum_threads(id),
            user_id TEXT NOT NULL REFERENCES users(id),
            content TEXT NOT NULL,
            is_best_answer INTEGER NOT NULL DEFAULT 0,
            likes_count INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_forum_replies_thread ON forum_replies(thread_id);
        CREATE INDEX IF NOT EXISTS idx_forum_replies_user ON forum_replies(user_id);

        CREATE TABLE IF NOT EXISTS forum_likes (
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
            user_id TEXT NOT NULL REFERENCES users(id),
            reply_id TEXT NOT NULL REFERENCES forum_replies(id),
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            UNIQUE(user_id, reply_id)
        );
        CREATE INDEX IF NOT EXISTS idx_forum_likes_reply ON forum_likes(reply_id);
        CREATE INDEX IF NOT EXISTS idx_forum_likes_user ON forum_likes(user_id);
    """)
    conn.commit()

    # Seed default categories
    default_categories = [
        ("General Astrology", "Discuss all things astrology — transits, signs, and celestial events", "🌟", 1),
        ("Kundli Discussions", "Share and analyze birth charts, planetary positions, and dashas", "📜", 2),
        ("Remedies & Doshas", "Explore remedies for Mangal Dosha, Kaal Sarp Dosha, and more", "💎", 3),
        ("Panchang & Muhurat", "Discuss auspicious timings, tithis, nakshatras, and muhurat", "📅", 4),
        ("Spiritual Wisdom", "Vedic philosophy, mantras, meditation, and spiritual growth", "🕉️", 5),
        ("Tarot & Numerology", "Tarot readings, numerology insights, and divination discussions", "🔮", 6),
        ("Astrologer Picks", "Curated discussions and insights from professional astrologers", "⭐", 7),
        ("Beginner Questions", "New to astrology? Ask your questions here — no question is too basic!", "🌱", 8),
    ]
    for name, description, icon, order_index in default_categories:
        try:
            conn.execute(
                "INSERT INTO forum_categories (name, description, icon, order_index) VALUES (?, ?, ?, ?)",
                (name, description, icon, order_index),
            )
        except sqlite3.IntegrityError:
            pass  # Already seeded
    conn.commit()
    conn.close()


def get_db(db_path: str = None):
    """Yield a database connection. Use as dependency in FastAPI."""
    import os
    path = db_path or os.getenv("DB_PATH", DB_PATH)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
    finally:
        conn.close()
