# 09 — Implementation

## Phase Breakdown

### Wave 1: Foundation (no cross-deps — parallel)
| File | Purpose | Complexity | Who |
|------|---------|-----------|-----|
| app/config.py | Settings, env vars, paths | 1 | Qwen |
| app/models.py | Pydantic request/response models | 2 | Qwen |
| app/database.py | SQLite init, get_db, migrations | 2 | Qwen |
| app/auth.py | JWT create/verify, password hash, get_current_user | 3 | Claude |
| requirements.txt | All dependencies | 1 | Qwen |

### Wave 2: Core Engines (depend on Wave 1 — parallel within wave)
| File | Purpose | Complexity | Who |
|------|---------|-----------|-----|
| app/astro_engine.py | Swiss Ephemeris wrapper: planet positions, houses, signs, aspects | 5 | Claude |
| app/astro_iogita_engine.py | **KEY FILE**: Planet→Atom mapping, basin identification, analysis | 5 | Claude |
| app/panchang_engine.py | Tithi, Nakshatra, Yoga, Karana, Rahu Kaal, Choghadiya | 4 | Claude |
| app/dasha_engine.py | Vimshottari Dasha calculation (120-year cycle) | 4 | Claude |
| app/dosha_engine.py | Mangal Dosha, Kaal Sarp, Sade Sati detection | 3 | Claude |
| app/matching_engine.py | Gun Milan (36 points), compatibility scoring | 4 | Claude |
| app/divisional_charts.py | D1, D9, D10 chart calculations | 4 | Claude |
| app/ashtakvarga_engine.py | Bindhu calculation per planet per sign | 3 | Claude |
| app/kp_engine.py | KP System cuspal chart, significators | 3 | Claude |
| app/lalkitab_engine.py | Lal Kitab remedies lookup | 2 | Qwen |
| app/numerology_engine.py | Life path, expression, soul urge from name/DOB | 2 | Qwen |
| app/tarot_engine.py | 78-card deck, spreads, card meanings | 2 | Qwen |
| app/prashnavali_engine.py | Ram Shalaka grid, Hanuman Prashna, Gita oracle | 3 | Claude |
| app/ai_engine.py | OpenAI integration: interpret, ask, gita, remedies, oracle | 4 | Claude |

### Wave 3: Routes (depend on Wave 2 — parallel within wave)
| File | Purpose | Complexity | Who |
|------|---------|-----------|-----|
| app/routes/__init__.py | Router registry | 1 | Qwen |
| app/routes/auth.py | Register, login, me | 3 | Claude |
| app/routes/kundli.py | Kundli CRUD, io-gita, match, dosha, dasha, divisional, ashtakvarga | 4 | Claude |
| app/routes/horoscope.py | Horoscope by sign and period | 2 | Qwen |
| app/routes/panchang.py | Panchang, Choghadiya, Muhurat, Sunrise, Festivals | 3 | Claude |
| app/routes/ai.py | AI interpret, ask, gita, remedies, oracle | 3 | Claude |
| app/routes/prashnavali.py | All oracle endpoints | 2 | Qwen |
| app/routes/library.py | Gita chapters/verses, content by category | 2 | Qwen |
| app/routes/kp_lalkitab.py | KP cuspal, Lal Kitab remedies | 2 | Qwen |
| app/routes/numerology.py | Numerology calculation endpoint | 2 | Qwen |
| app/routes/tarot.py | Tarot draw endpoint | 2 | Qwen |
| app/routes/palmistry.py | Palmistry guide (static content) | 1 | Qwen |
| app/routes/products.py | Product catalog, filtering, pagination | 3 | Claude |
| app/routes/cart.py | Cart CRUD, stock validation | 3 | Claude |
| app/routes/orders.py | Order creation, status, tracking | 3 | Claude |
| app/routes/payments.py | Payment initiation, webhooks | 4 | Claude |
| app/routes/consultation.py | Booking, accept, complete | 3 | Claude |
| app/routes/messages.py | WebSocket chat | 4 | Claude |
| app/routes/reports.py | Report request, generation | 3 | Claude |
| app/routes/admin.py | Admin CRUD, dashboard, content CMS | 3 | Claude |
| app/routes/astrologer.py | Astrologer dashboard, profile, availability | 3 | Claude |

### Wave 4: Integration (depends on Wave 3)
| File | Purpose | Complexity | Who |
|------|---------|-----------|-----|
| app/main.py | FastAPI app, CORS, include all routers, lifespan | 3 | Claude |
| app/seed_data.py | Seed spiritual content (Gita, Mantras, Festivals, Products) | 2 | Qwen |

### Wave 5: Frontend (depends on Wave 4)
| File | Purpose | Complexity | Who |
|------|---------|-----------|-----|
| frontend/ | React app from Kimi template v2 | 4 | Claude |
| — src/pages/ | All page components | 4 | Claude |
| — src/hooks/ | API hooks, WebSocket hook | 3 | Claude |
| — src/types/ | TypeScript types matching backend models | 2 | Qwen |

### Wave 6: User Management + Admin Enhancements (v2.0 — added post-audit)
| File | Purpose | Complexity | Who |
|------|---------|-----------|-----|
| app/seed_data.py | Seed spiritual content + demo data + migrate_users_table | 2 | Qwen |
| app/routes/auth.py (update) | Add PATCH /profile, POST /change-password, GET /history | 3 | Claude |
| app/routes/admin.py (update) | Add product CRUD, user management endpoints | 3 | Claude |
| app/routes/ai.py (update) | Add GET /history endpoint | 2 | Qwen |
| app/routes/reports.py (update) | Add GET /reports list endpoint | 2 | Qwen |
| Database migration | migrate_users_table() — adds date_of_birth, gender, city, is_active | 2 | Claude |

### Wave 7: E2E + Deployment
| File | Purpose | Complexity | Who |
|------|---------|-----------|-----|
| e2e/test_astrovedic_e2e.py | Full Playwright E2E walkthrough | 4 | Claude |
| .env.example | Environment variable template | 1 | Qwen |
| .gitignore | Git exclusions | 1 | Qwen |
| pytest.ini | Pytest configuration | 1 | Qwen |

## File Count Summary
- **app/ source files:** 45 (increased from 40 — Wave 6 additions + seed_data.py)
- **test files:** 29 (26 original + 3 new: test_user_profile, test_admin_products, test_admin_users)
- **frontend files:** ~20 key files (pages, hooks, types)
- **config/deploy files:** 4
- **Total:** ~98 files
- **Total API routes:** 88 (increased from 73 — Wave 6 adds 15 new endpoints)

## Build Order Rules
1. Wave N+1 is BLOCKED until Wave N passes full pytest
2. Within a wave, files with no cross-deps build in parallel
3. Every file: test FIRST (RED), then code (GREEN)
4. Full pytest after each wave
5. Complexity <= 2 → Qwen Coder first, Claude fallback
6. Complexity >= 3 → Claude only
