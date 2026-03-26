# 03 — Data Contracts

## Data Model (SQLite)

```sql
-- Core Auth
CREATE TABLE users (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user' CHECK(role IN ('user','astrologer','admin')),
    phone TEXT,
    avatar_url TEXT,
    date_of_birth TEXT,
    gender TEXT CHECK(gender IN ('male','female','other')),
    city TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- Kundli / Birth Charts
CREATE TABLE kundlis (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT NOT NULL REFERENCES users(id),
    person_name TEXT NOT NULL,
    birth_date TEXT NOT NULL,        -- ISO date
    birth_time TEXT NOT NULL,        -- HH:MM:SS
    birth_place TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    timezone_offset REAL NOT NULL,   -- hours from UTC
    ayanamsa TEXT NOT NULL DEFAULT 'lahiri',
    chart_data TEXT NOT NULL,        -- JSON: planets, houses, signs, aspects
    iogita_analysis TEXT,            -- JSON: atom_vector, basin, trajectory
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_kundlis_user ON kundlis(user_id);

-- Horoscopes
CREATE TABLE horoscopes (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    sign TEXT NOT NULL CHECK(sign IN ('aries','taurus','gemini','cancer','leo','virgo','libra','scorpio','sagittarius','capricorn','aquarius','pisces')),
    period_type TEXT NOT NULL CHECK(period_type IN ('daily','weekly','monthly','yearly')),
    period_date TEXT NOT NULL,       -- date or date range start
    content TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(sign, period_type, period_date)
);
CREATE INDEX idx_horoscopes_lookup ON horoscopes(sign, period_type, period_date);

-- Panchang Cache
CREATE TABLE panchang_cache (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    date TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    tithi TEXT NOT NULL,              -- JSON: {name, start, end, number}
    nakshatra TEXT NOT NULL,          -- JSON: {name, start, end, pada}
    yoga TEXT NOT NULL,               -- JSON: {name, start, end}
    karana TEXT NOT NULL,             -- JSON: {name, start, end}
    rahu_kaal TEXT NOT NULL,          -- JSON: {start, end}
    choghadiya TEXT NOT NULL,         -- JSON: [{name, start, end, quality}]
    sunrise TEXT NOT NULL,
    sunset TEXT NOT NULL,
    moonrise TEXT,
    moonset TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(date, latitude, longitude)
);

-- Spiritual Content Library
CREATE TABLE content_library (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    category TEXT NOT NULL CHECK(category IN ('gita','aarti','mantra','pooja','vrat_katha','chalisa','festival')),
    title TEXT NOT NULL,
    title_hindi TEXT,
    content TEXT NOT NULL,            -- Main text
    audio_url TEXT,                   -- For mantras/aarti with audio
    chapter INTEGER,                  -- For Gita: chapter number
    verse INTEGER,                    -- For Gita: verse number
    sanskrit_text TEXT,               -- Original Sanskrit
    translation TEXT,                 -- English translation
    commentary TEXT,                  -- AI or traditional commentary
    sort_order INTEGER DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_content_category ON content_library(category);
CREATE INDEX idx_content_gita ON content_library(category, chapter, verse);

-- Prashnavali Logs
CREATE TABLE prashnavali_logs (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT REFERENCES users(id),
    prashnavali_type TEXT NOT NULL CHECK(prashnavali_type IN ('ram_shalaka','hanuman_prashna','ramcharitmanas','gita','yes_no_oracle','tarot')),
    question TEXT,
    result TEXT NOT NULL,             -- JSON: the oracle answer
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- AI Chat Logs
CREATE TABLE ai_chat_logs (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT NOT NULL REFERENCES users(id),
    chat_type TEXT NOT NULL CHECK(chat_type IN ('kundli_interpretation','ask_question','gita_ai','remedies','oracle')),
    kundli_id TEXT REFERENCES kundlis(id),
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    model_used TEXT NOT NULL DEFAULT 'gpt-4',
    tokens_used INTEGER,
    rating INTEGER CHECK(rating IN (1, -1)),  -- thumbs up/down
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_ai_chat_user ON ai_chat_logs(user_id);

-- E-Commerce: Products
CREATE TABLE products (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('gemstone','rudraksha','bracelet','yantra','vastu')),
    price REAL NOT NULL CHECK(price > 0),
    compare_price REAL,              -- Original price for showing discount
    image_url TEXT,
    images TEXT,                      -- JSON array of image URLs
    weight TEXT,                      -- e.g. "3.5 carat", "50g"
    planet TEXT,                      -- Associated planet
    properties TEXT,                  -- JSON: {benefits, who_should_wear, etc.}
    stock INTEGER NOT NULL DEFAULT 0,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_active ON products(is_active);

-- E-Commerce: Cart
CREATE TABLE cart_items (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT NOT NULL REFERENCES users(id),
    product_id TEXT NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL DEFAULT 1 CHECK(quantity > 0),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(user_id, product_id)
);
CREATE INDEX idx_cart_user ON cart_items(user_id);

-- E-Commerce: Orders
CREATE TABLE orders (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT NOT NULL REFERENCES users(id),
    status TEXT NOT NULL DEFAULT 'placed' CHECK(status IN ('placed','confirmed','shipped','delivered','cancelled')),
    total REAL NOT NULL,
    shipping_address TEXT NOT NULL,    -- JSON
    payment_method TEXT NOT NULL CHECK(payment_method IN ('cod','razorpay','stripe')),
    payment_status TEXT NOT NULL DEFAULT 'pending' CHECK(payment_status IN ('pending','paid','failed','refunded')),
    tracking_number TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);

CREATE TABLE order_items (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    order_id TEXT NOT NULL REFERENCES orders(id),
    product_id TEXT NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    price REAL NOT NULL,
    product_name TEXT NOT NULL
);
CREATE INDEX idx_order_items_order ON order_items(order_id);

-- Payments
CREATE TABLE payments (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    order_id TEXT REFERENCES orders(id),
    report_id TEXT REFERENCES reports(id),
    consultation_id TEXT REFERENCES consultations(id),
    provider TEXT NOT NULL CHECK(provider IN ('razorpay','stripe','cod')),
    provider_payment_id TEXT,
    amount REAL NOT NULL,
    currency TEXT NOT NULL DEFAULT 'INR',
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','completed','failed','refunded')),
    metadata TEXT,                     -- JSON: provider-specific data
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Consultation: Astrologer Profiles
CREATE TABLE astrologers (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT UNIQUE NOT NULL REFERENCES users(id),
    display_name TEXT NOT NULL,
    bio TEXT,
    specializations TEXT NOT NULL,    -- JSON array: ["Vedic","KP","Lal Kitab"]
    experience_years INTEGER NOT NULL DEFAULT 0,
    per_minute_rate REAL NOT NULL,
    languages TEXT NOT NULL DEFAULT '["English"]',  -- JSON array
    rating REAL DEFAULT 0.0,
    total_consultations INTEGER DEFAULT 0,
    is_available INTEGER NOT NULL DEFAULT 0,
    is_approved INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_astrologers_available ON astrologers(is_available, is_approved);

-- Consultation: Appointments
CREATE TABLE consultations (
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
CREATE INDEX idx_consultations_user ON consultations(user_id);
CREATE INDEX idx_consultations_astrologer ON consultations(astrologer_id);
CREATE INDEX idx_consultations_status ON consultations(status);

-- Consultation: Chat Messages
CREATE TABLE messages (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    consultation_id TEXT NOT NULL REFERENCES consultations(id),
    sender_id TEXT NOT NULL REFERENCES users(id),
    content TEXT NOT NULL,
    message_type TEXT NOT NULL DEFAULT 'text' CHECK(message_type IN ('text','image','file')),
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_messages_consultation ON messages(consultation_id);

-- Paid Reports
CREATE TABLE reports (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT NOT NULL REFERENCES users(id),
    kundli_id TEXT NOT NULL REFERENCES kundlis(id),
    report_type TEXT NOT NULL CHECK(report_type IN ('full_kundli','marriage','career','health','yearly')),
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','paid','generating','ready','failed')),
    content TEXT,                      -- Generated report content (HTML/Markdown)
    pdf_url TEXT,
    price REAL NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_reports_user ON reports(user_id);

-- Muhurat requests
CREATE TABLE muhurat_cache (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    muhurat_type TEXT NOT NULL CHECK(muhurat_type IN ('marriage','griha_pravesh','business_start','travel','naming_ceremony','mundan')),
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    results TEXT NOT NULL,             -- JSON array of auspicious dates/times
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Festival Calendar
CREATE TABLE festivals (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    name TEXT NOT NULL,
    name_hindi TEXT,
    date TEXT NOT NULL,
    description TEXT,
    rituals TEXT,                      -- JSON: steps for celebration
    category TEXT CHECK(category IN ('major','regional','fasting','eclipse')),
    year INTEGER NOT NULL,
    UNIQUE(name, year)
);
CREATE INDEX idx_festivals_date ON festivals(date);
```

## API Contract

### Health & Auth
| Method | Endpoint | Auth | Request | Response | Status |
|--------|----------|------|---------|----------|--------|
| GET | /health | None | — | `{status, version, uptime}` | 200 |
| POST | /api/auth/register | None | `{email, password, name, phone?}` | `{user, token}` | 201 |
| POST | /api/auth/login | None | `{email, password}` | `{user, token}` | 200 |
| GET | /api/auth/me | JWT | — | `{user}` | 200 |
| PATCH | /api/auth/profile | JWT | `{name?, phone?, date_of_birth?, gender?, city?, avatar_url?}` | `{user profile}` | 200 |
| POST | /api/auth/change-password | JWT | `{current_password, new_password}` | `{message}` | 200 |
| GET | /api/auth/history | JWT | — | `{kundlis, orders, consultations, ai_chats, reports}` | 200 |

### Kundli & Astrology
| Method | Endpoint | Auth | Request | Response | Status |
|--------|----------|------|---------|----------|--------|
| POST | /api/kundli/generate | JWT | `{person_name, birth_date, birth_time, birth_place, lat, lng, tz_offset}` | `{kundli_id, planets, houses, signs, aspects}` | 201 |
| GET | /api/kundli/{id} | JWT | — | `{kundli with chart_data}` | 200 |
| GET | /api/kundli/list | JWT | — | `[kundli summaries]` | 200 |
| POST | /api/kundli/{id}/iogita | JWT | — | `{atom_vector, basin, analysis}` | 200 |
| POST | /api/kundli/match | JWT | `{kundli_id_1, kundli_id_2}` | `{gun_milan_score, compatibility, doshas}` | 200 |
| POST | /api/kundli/{id}/dosha | JWT | — | `{mangal_dosha, kaal_sarp, sade_sati}` | 200 |
| POST | /api/kundli/{id}/dasha | JWT | — | `{mahadasha_periods, current_dasha, antardasha}` | 200 |
| POST | /api/kundli/{id}/divisional | JWT | `{chart_type: "D9"|"D10"|...}` | `{chart_data}` | 200 |
| POST | /api/kundli/{id}/ashtakvarga | JWT | — | `{planet_bindus, sarvashtakvarga}` | 200 |
| GET | /api/horoscope/{sign} | None | `?period=daily|weekly|monthly|yearly` | `{sign, period, content, date}` | 200 |

### KP System + Lal Kitab + Numerology + Tarot
| Method | Endpoint | Auth | Request | Response | Status |
|--------|----------|------|---------|----------|--------|
| POST | /api/kp/cuspal | JWT | `{kundli_id}` | `{cuspal_chart, significators}` | 200 |
| POST | /api/lalkitab/remedies | JWT | `{kundli_id}` | `{remedies_by_planet}` | 200 |
| POST | /api/numerology/calculate | None | `{name, birth_date}` | `{life_path, expression, soul_urge, personality, predictions}` | 200 |
| POST | /api/tarot/draw | JWT? | `{spread: "single"|"three"|"celtic_cross", question?}` | `{cards, interpretation}` | 200 |
| GET | /api/palmistry/guide | None | — | `{lines, mounts, shapes, meanings}` | 200 |

### AI
| Method | Endpoint | Auth | Request | Response | Status |
|--------|----------|------|---------|----------|--------|
| POST | /api/ai/interpret | JWT | `{kundli_id}` | `{interpretation, highlights, warnings}` | 200 |
| POST | /api/ai/ask | JWT | `{question, kundli_id?}` | `{answer, reasoning}` | 200 |
| POST | /api/ai/gita | None | `{question}` | `{answer, relevant_slokas}` | 200 |
| POST | /api/ai/remedies | JWT | `{kundli_id}` | `{remedies: [{type, description, planet}]}` | 200 |
| POST | /api/ai/oracle | JWT? | `{question, mode: "yes_no"|"tarot"}` | `{answer, cards?, reasoning}` | 200 |
| GET | /api/ai/history | JWT | `?page=1&limit=20` | `{chats, total}` | 200 |

### Panchang
| Method | Endpoint | Auth | Request | Response | Status |
|--------|----------|------|---------|----------|--------|
| GET | /api/panchang | None | `?date=YYYY-MM-DD&lat=X&lng=Y` | `{tithi, nakshatra, yoga, karana, rahu_kaal, ...}` | 200 |
| GET | /api/panchang/choghadiya | None | `?date=YYYY-MM-DD&lat=X&lng=Y` | `{periods: [{name, start, end, quality}]}` | 200 |
| GET | /api/panchang/muhurat | None | `?type=marriage&year=2026&month=4&lat=X&lng=Y` | `{dates: [{date, time_range, quality}]}` | 200 |
| GET | /api/panchang/sunrise | None | `?date=YYYY-MM-DD&lat=X&lng=Y` | `{sunrise, sunset, moonrise, moonset}` | 200 |
| GET | /api/festivals | None | `?year=2026&month=4?` | `[{name, date, description, rituals}]` | 200 |

### Spiritual Library
| Method | Endpoint | Auth | Request | Response | Status |
|--------|----------|------|---------|----------|--------|
| GET | /api/gita/chapters | None | — | `[{chapter, title, verses_count, summary}]` | 200 |
| GET | /api/gita/chapter/{ch} | None | — | `{chapter, title, verses}` | 200 |
| GET | /api/gita/verse/{ch}/{v} | None | — | `{sanskrit, translation, commentary}` | 200 |
| GET | /api/library/{category} | None | — | `[{id, title, content_preview}]` | 200 |
| GET | /api/library/item/{id} | None | — | `{full content}` | 200 |

### Prashnavali
| Method | Endpoint | Auth | Request | Response | Status |
|--------|----------|------|---------|----------|--------|
| POST | /api/prashnavali/ram-shalaka | JWT? | `{row, col}` (grid position) | `{answer, verse, meaning}` | 200 |
| POST | /api/prashnavali/hanuman | JWT? | `{question}` | `{answer, chaupai, meaning}` | 200 |
| POST | /api/prashnavali/ramcharitmanas | JWT? | `{question}` | `{answer, verse, meaning}` | 200 |
| POST | /api/prashnavali/gita | JWT? | `{question}` | `{answer, sloka, meaning}` | 200 |

### E-Commerce
| Method | Endpoint | Auth | Request | Response | Status |
|--------|----------|------|---------|----------|--------|
| GET | /api/products | None | `?category=gemstone&page=1&limit=20` | `{products, total, page}` | 200 |
| GET | /api/products/{id} | None | — | `{product detail}` | 200 |
| GET | /api/cart | JWT | — | `{items, total}` | 200 |
| POST | /api/cart/add | JWT | `{product_id, quantity}` | `{cart}` | 200 |
| PATCH | /api/cart/{item_id} | JWT | `{quantity}` | `{cart}` | 200 |
| DELETE | /api/cart/{item_id} | JWT | — | `{cart}` | 200 |
| POST | /api/orders | JWT | `{shipping_address, payment_method}` | `{order}` | 201 |
| GET | /api/orders | JWT | — | `[orders]` | 200 |
| GET | /api/orders/{id} | JWT | — | `{order with items}` | 200 |
| POST | /api/payments/initiate | JWT | `{order_id, provider}` | `{payment_url or payment_id}` | 200 |
| POST | /api/payments/webhook/razorpay | Signature | Razorpay webhook | `{status}` | 200 |
| POST | /api/payments/webhook/stripe | Signature | Stripe webhook | `{status}` | 200 |

### Consultation
| Method | Endpoint | Auth | Request | Response | Status |
|--------|----------|------|---------|----------|--------|
| GET | /api/astrologers | None | `?specialization=Vedic&available=true` | `[astrologer profiles]` | 200 |
| GET | /api/astrologers/{id} | None | — | `{astrologer detail}` | 200 |
| POST | /api/consultations/book | JWT | `{astrologer_id, type, scheduled_at?}` | `{consultation}` | 201 |
| GET | /api/consultations | JWT | — | `[user's consultations]` | 200 |
| PATCH | /api/consultations/{id}/accept | JWT(astrologer) | — | `{consultation}` | 200 |
| PATCH | /api/consultations/{id}/complete | JWT(astrologer) | `{notes?}` | `{consultation}` | 200 |
| WS | /ws/consultation/{id} | JWT | — | Real-time chat messages | — |
| POST | /api/reports/request | JWT | `{kundli_id, report_type}` | `{report, payment_required}` | 201 |
| GET | /api/reports/{id} | JWT | — | `{report with content}` | 200 |
| GET | /api/reports | JWT | — | `[reports]` | 200 |

### Admin
| Method | Endpoint | Auth | Request | Response | Status |
|--------|----------|------|---------|----------|--------|
| GET | /api/admin/users | JWT(admin) | `?page=1&role=user` | `{users, total}` | 200 |
| PATCH | /api/admin/users/{id} | JWT(admin) | `{role?, is_active?}` | `{user}` | 200 |
| GET | /api/admin/orders | JWT(admin) | `?status=placed&page=1` | `{orders, total}` | 200 |
| PATCH | /api/admin/orders/{id} | JWT(admin) | `{status, tracking_number?}` | `{order}` | 200 |
| PATCH | /api/admin/astrologers/{id}/approve | JWT(admin) | — | `{astrologer}` | 200 |
| GET | /api/admin/ai-logs | JWT(admin) | `?page=1&type=ask_question` | `{logs, total}` | 200 |
| POST | /api/admin/content | JWT(admin) | `{category, title, content, ...}` | `{content_item}` | 201 |
| PATCH | /api/admin/content/{id} | JWT(admin) | `{updates}` | `{content_item}` | 200 |
| GET | /api/admin/dashboard | JWT(admin) | — | `{stats: users, orders, revenue, ai_usage}` | 200 |
| DELETE | /api/admin/content/{id} | JWT(admin) | — | — | 204 |

### Admin Product CRUD (v2.0)
| Method | Endpoint | Auth | Request | Response | Status |
|--------|----------|------|---------|----------|--------|
| GET | /api/admin/products | JWT(admin) | `?category=&page=1&limit=20` | `{products, total, page}` | 200 |
| POST | /api/admin/products | JWT(admin) | `{name, description, category, price, stock, ...}` | `{product}` | 201 |
| PUT | /api/admin/products/{id} | JWT(admin) | `{full ProductCreate body}` | `{product}` | 200 |
| PATCH | /api/admin/products/{id}/stock | JWT(admin) | `?stock=N` | `{product_id, stock}` | 200 |
| PATCH | /api/admin/products/{id}/toggle | JWT(admin) | — | `{product_id, is_active}` | 200 |

### Admin User Management (v2.0)
| Method | Endpoint | Auth | Request | Response | Status |
|--------|----------|------|---------|----------|--------|
| POST | /api/admin/users | JWT(admin) | `{email, password, name, role, phone?}` | `{user}` | 201 |
| GET | /api/admin/users/{id} | JWT(admin) | — | `{user + activity counts}` | 200 |
| PATCH | /api/admin/users/{id}/deactivate | JWT(admin) | — | `{user}` | 200 |
| PATCH | /api/admin/users/{id}/activate | JWT(admin) | — | `{user}` | 200 |
| GET | /api/admin/users/{id}/activity | JWT(admin) | — | `{kundlis, orders, consultations, ai_chats, reports}` | 200 |

### Astrologer Dashboard
| Method | Endpoint | Auth | Request | Response | Status |
|--------|----------|------|---------|----------|--------|
| GET | /api/astrologer/dashboard | JWT(astrologer) | — | `{earnings, consultations, rating, upcoming}` | 200 |
| GET | /api/astrologer/consultations | JWT(astrologer) | `?status=requested` | `[consultations]` | 200 |
| PATCH | /api/astrologer/profile | JWT(astrologer) | `{bio, specializations, rate, ...}` | `{profile}` | 200 |
| PATCH | /api/astrologer/availability | JWT(astrologer) | `{is_available}` | `{profile}` | 200 |

## Contract Alignment Notes (v2.0)

All API responses follow these rules — no exceptions:

### Response Shape Rules
1. **NO `{"status", "data"}` wrappers** — all endpoints return data directly (e.g., `{user}` not `{"status": "ok", "data": {user}}`)
2. **Horoscope** — response field is `date` not `period_date`
3. **Library chapters** — field is `verses_count` (not `verse_count`), includes `summary` and `content_preview`
4. **Products list** — returns `{products, total, page}` directly (not wrapped)
5. **Palmistry guide** — returns `{lines, mounts, shapes, meanings}` directly
6. **AI interpret** — accepts `{kundli_id}` (not `{question}`)
7. **AI ask** — accepts `{question, kundli_id?}` with optional kundli context
