# 02 — Architecture

## System Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Vite)                   │
│  Port 5198 | shadcn/ui + Tailwind | Kimi Template v2        │
│  Pages: Home, Kundli, Horoscope, Panchang, AI Chat,         │
│         Prashnavali, Gita, Library, Shop, Consultation,      │
│         Admin, Astrologer Dashboard                          │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP + WebSocket
┌──────────────────────────▼──────────────────────────────────┐
│                  BACKEND (FastAPI)                            │
│  Port 8028 | Uvicorn | CORS | JWT Auth                       │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Astrology    │  │ AI Engine    │  │ Panchang     │       │
│  │ Engine       │  │ (OpenAI)     │  │ Engine       │       │
│  │ - Kundli     │  │ - Chat       │  │ - Tithi      │       │
│  │ - Dasha      │  │ - Interpret  │  │ - Nakshatra  │       │
│  │ - Dosha      │  │ - Gita AI   │  │ - Muhurat    │       │
│  │ - Matching   │  │ - Remedies   │  │ - Rahu Kaal  │       │
│  │ - Charts     │  │ - Oracle     │  │ - Festivals  │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                 │                │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐       │
│  │ Swiss        │  │ OpenAI API   │  │ Astronomical │       │
│  │ Ephemeris    │  │ (GPT-4)      │  │ Calculations │       │
│  │ (swisseph)   │  │              │  │ (ephem math) │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ io-gita      │  │ E-Commerce   │  │ Consultation │       │
│  │ Engine       │  │ Engine       │  │ Engine       │       │
│  │ - Atom Map   │  │ - Products   │  │ - Chat (WS)  │       │
│  │ - Basin ID   │  │ - Cart       │  │ - Booking    │       │
│  │ - Analysis   │  │ - Payment    │  │ - Reports    │       │
│  │ (numpy)      │  │ - Orders     │  │ - Video      │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Spiritual    │  │ Prashnavali  │  │ Auth + Admin │       │
│  │ Library      │  │ Engine       │  │ Engine       │       │
│  │ - Gita text  │  │ - Ram Shalaka│  │ - JWT Auth   │       │
│  │ - Mantras    │  │ - Hanuman    │  │ - RBAC       │       │
│  │ - Aarti      │  │ - Tarot AI   │  │ - Admin CRUD │       │
│  │ - Pooja      │  │ - Yes/No     │  │ - Astrologer │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                  DATABASE (SQLite WAL)                        │
│  Tables: users, kundlis, horoscopes, panchang_cache,         │
│          products, cart_items, orders, order_items,           │
│          payments, consultations, messages, appointments,     │
│          astrologers, reports, content_library,               │
│          prashnavali_logs, ai_chat_logs                       │
└─────────────────────────────────────────────────────────────┘
```

## Architecture Notes (v2.0)

- **Total API routes:** 88 (increased from 73 after Wave 6 additions)
- **app/seed_data.py** — Seeds spiritual content (Gita, Mantras, Festivals, Products) and demo data on first startup
- **migrate_users_table()** — Database migration adds `date_of_birth`, `gender`, `city`, `is_active` columns to existing users table

## Data Flow

### Kundli Generation Flow
```
User enters DOB/Time/Place → Frontend sends POST /api/kundli/generate
→ Backend calls swisseph.calc_ut() for each planet
→ Calculates house cusps via swisseph.houses()
→ Maps planets to houses and signs
→ Optionally calls astro_iogita_engine.build_atom_vector()
→ Returns JSON {planets, houses, signs, aspects, iogita_analysis}
```

### AI Chat Flow
```
User asks question → Frontend sends POST /api/ai/ask
→ Backend loads user's kundli data
→ Constructs prompt: system(astrology expert) + kundli context + question
→ Calls OpenAI GPT-4 API
→ Returns AI response with astrological reasoning
```

### E-Commerce Flow
```
User browses products → GET /api/products?category=gemstones
→ Adds to cart → POST /api/cart/add
→ Checkout → POST /api/orders/create (validates cart, calculates total)
→ Payment → POST /api/payments/initiate (Razorpay/Stripe)
→ Webhook confirms → POST /api/payments/webhook
→ Order status updated → GET /api/orders/{id}
```

### User Profile Management Flow
```
User edits profile → Frontend sends PATCH /api/auth/profile
→ Backend validates fields (name, phone, DOB, gender, city, avatar_url)
→ Sanitizes text inputs via bleach
→ Updates users table
→ Returns updated user profile
```

### User Activity History Flow
```
User views activity → Frontend sends GET /api/auth/history
→ Backend queries kundlis, orders, consultations, ai_chat_logs, reports for user_id
→ Returns {kundlis, orders, consultations, ai_chats, reports} with counts and summaries
```

### Admin Product CRUD Flow
```
Admin creates product → POST /api/admin/products
→ Validates all fields (name, description, category, price, stock, images)
→ Inserts into products table → Returns product
Admin updates stock → PATCH /api/admin/products/{id}/stock?stock=N
→ Updates stock column → Returns {product_id, stock}
Admin toggles active → PATCH /api/admin/products/{id}/toggle
→ Flips is_active flag → Returns {product_id, is_active}
```

### Admin User Management Flow
```
Admin creates user → POST /api/admin/users
→ Validates email uniqueness, hashes password
→ Inserts into users table → Returns user
Admin deactivates user → PATCH /api/admin/users/{id}/deactivate
→ Sets is_active=0 → Deactivated user cannot login (403)
Admin views user activity → GET /api/admin/users/{id}/activity
→ Same as user history but for any user_id
```

### Consultation Flow
```
User books appointment → POST /api/consultations/book
→ Astrologer accepts → PATCH /api/consultations/{id}/accept
→ Chat opens → WebSocket /ws/consultation/{id}
→ Messages exchanged in real-time
→ Session ends → consultation marked complete
```

## Tech Stack Justification
| Choice | Why | Alternative Considered | Why Not |
|--------|-----|----------------------|---------|
| FastAPI | Python required (swisseph, numpy, OpenAI). Expert DNA (16 projects) | PHP (user's initial suggestion) | Zero experience, no numpy/swisseph bindings |
| SQLite WAL | MVP prototype. 15 project DNA. Sufficient for single-server | PostgreSQL | Overkill for MVP. Upgrade path clear. |
| React + Vite | Interactive charts, real-time updates. Kimi template ready | Vanilla JS | Too limited for complex dashboard |
| Swiss Ephemeris | Gold standard for astronomical calculations. Used by AstroSage | Astronomical Algorithms (Meeus) | Less accurate, more code |
| OpenAI GPT-4 | Best for nuanced astrological interpretation | Local LLM | Accuracy too low for astrology domain |
| shadcn/ui | 40+ components ready from Kimi template | Material UI | Heavier, less customizable |
