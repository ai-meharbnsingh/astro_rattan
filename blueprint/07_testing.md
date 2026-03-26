# 07 — Testing (Master Document)

> **Project**: AstroVedic (Vedic Astrology Platform + io-gita Engine)
> **Stack**: FastAPI (Python) + React 19 (TypeScript) + SQLite WAL
> **Total Endpoints**: 108 | **Tables**: 20 | **Frontend Pages**: 19
> **Test Types**: Unit, Integration, API, E2E (Playwright), WebSocket, Security, Performance
> **Last Updated**: 2026-03-26 — verified against actual codebase

---

## PART A: STATUS & TRACKING

### Current Verification Snapshot

| Check | Current State | Notes |
|------|---------------|-------|
| Backend test files on disk | **43** | Route, engine, security, performance, hardening, contract, email/config, blog/SEO |
| E2E test files on disk | **2** | `e2e/test_astrovedic_e2e.py`, `e2e/test_frontend_smoke.py` |
| Latest full suite run (`pytest -q`) | **526 passed** | Full suite is green, including the new browser smoke tests |
| Focused validation | **GREEN** | `e2e/test_frontend_smoke.py` 5/5; `tests/test_palmistry_routes.py` + `tests/test_blog_routes.py` + `tests/test_seo_assets.py` 16/16 |
| Frontend build | **GREEN** | `cd frontend && npm run build` passes |

> **Inference from the current run:** backend contract/isolation issues that were red earlier are now resolved; the remaining test gaps are mostly **frontend/browser automation depth** and **end-to-end provider validations**.

---

### Coverage Already Present

| Layer | Current Coverage | Status |
|------|------------------|--------|
| Engine / model tests | Astro, io-gita, dasha, dosha, divisional, KP, Lal Kitab, numerology, tarot, prashnavali, models, config, DB | ✅ Strong |
| Route-level backend tests | Admin, AI, astrologer, cart, consultation, horoscope, kundli, library, orders, payments, products, reports, search, user profile | ✅ Present |
| Contract tests | `tests/test_blueprint_contract.py` with blueprint-level assertions | ✅ Green in the full suite |
| Payment verification | `tests/test_payment_webhooks.py` + `tests/test_payments_routes.py` | ✅ Present |
| Security | `tests/test_security.py` with **21** OWASP-style cases | ✅ Present |
| Performance | `tests/test_performance.py` with **11** timing / concurrency cases | ✅ Present |
| Hardening | `tests/test_sprint1_hardening.py` with **32** checks | ✅ Present |
| E2E flow coverage | Auth, kundli, panchang, numerology, tarot, prashnavali, AI, commerce | 🟡 Present on disk; browser run not re-verified in this pass |

---

### Pending Tests — Actual Gaps After Code Audit

These are the **remaining test gaps that matter now**. This list intentionally excludes speculative future features and stays inside the current planned product.

| Area | Priority | Pending Test Cases |
|------|----------|--------------------|
| **Frontend ↔ backend browser contracts** | 🟡 HIGH | Extend page/API smoke beyond current coverage for Cart Checkout, Consultation Page, Panchang, Spiritual Library, Numerology/Tarot, Prashnavali, and Shop |
| **Frontend smoke coverage** | 🟡 HIGH | Current browser smoke now covers Blog, Palmistry, Admin Dashboard, Astrologer Dashboard, and User Profile; broaden to remaining public/commerce flows |
| **Payment-provider sandbox coverage** | 🔴 HIGH | Run Razorpay/Stripe sandbox confirmation flows beyond mocked/unit route coverage |
| **Paid-report lifecycle coverage** | 🔴 HIGH | Assert payment gating, background generation, storage, and user retrieval work together cleanly |
| **Email delivery route coverage** | 🟡 HIGH | Add route-level assertions for welcome, order, and report-ready notification triggers beyond current service-hook tests |

---

### QC Findings — Endpoint Connections and Input Contracts

### Resolved in Current Repo — 2026-03-26

| Finding | Status | Validation |
|--------|--------|------------|
| Admin dashboard endpoint usage and content payload mapping | ✅ Fixed | Targeted admin route tests now pass; frontend build passes |
| Astrologer dashboard profile route, accept/complete actions, and response-key mapping | ✅ Fixed | Targeted astrologer route tests now pass; frontend build passes |
| Cart checkout `shipping_address` serialization and payment-initiation payload | ✅ Fixed | Frontend build passes; checkout payload now matches backend request models |
| Consultation page astrologer field normalization | ✅ Fixed | Frontend build passes |
| User profile `/api/auth/me` and `/api/auth/history` shape mismatch | ✅ Fixed | Targeted user profile tests now pass; frontend build passes |
| Panchang query params and Choghadiya response handling | ✅ Fixed | Frontend build passes |
| Spiritual library chapter/item response mapping | ✅ Fixed | Backend now returns `title_hindi`; frontend normalizers updated |
| Numerology / tarot / palmistry request-response mapping | ✅ Fixed | Frontend build passes |
| Ram Shalaka 0-based grid coordinates | ✅ Fixed | Frontend build passes |
| Invalid `idol` shop category | ✅ Fixed | Frontend build passes |
| Orders API `order_number` field | ✅ Fixed | Backend now maps `id` to `order_number` for frontend compatibility |
| Reports API `title` and `type` fields | ✅ Fixed | Backend now returns mapped `title` and `type` from `report_type` |
| Persisted shop add-to-cart flow | ✅ Fixed | Frontend now uses `/api/cart/add` for authenticated users |
| Anonymous AI chat auth gating | ✅ Fixed | Frontend now blocks protected AI calls until sign-in |
| Anonymous kundli auth gating | ✅ Fixed | Frontend now blocks protected kundli generation until sign-in |
| SMTP alias config + notification wiring | ✅ Fixed | Config accepts provided SMTP variable names; service-hook tests pass |
| Embedded video consultation session UX | ✅ Fixed | Client and astrologer dashboards now open the Jitsi room inline via `/api/consultations/{id}/video-link` |
| Static sitemap / robots SEO assets | ✅ Fixed | `frontend/public/sitemap.xml` and `frontend/public/robots.txt` added |
| Image-driven palmistry | ✅ Fixed | `/api/palmistry/analyze-image` plus dedicated `/palmistry` photo-reading UX are live |
| Blog / editorial growth system | ✅ Fixed | Public `/blog`, admin publishing routes, seeded posts, and sitemap coverage now exist |
| Browser smoke for key fixed pages | ✅ Fixed | `e2e/test_frontend_smoke.py` covers blog, palmistry, admin, astrologer, and profile routes |

### Still Pending

| Finding | Severity | Why It Matters | Tests To Add |
|--------|----------|----------------|--------------|
| No dedicated frontend test runner | 🟡 | Current UI verification is build-level plus backend-side contracts | Browser smoke + page/API contract tests |
| No provider-backed payment smoke | 🟡 | Mocked route coverage is not the same as live sandbox confirmation | Razorpay/Stripe sandbox smoke |
| No browser-level SEO regression check | 🟡 | Canonical/OG/sitemap changes can drift silently | Production-build SEO asset check |

---

### Current Test-Infra Risk

| Risk | Current Evidence | Pending QC Action |
|------|------------------|------------------|
| Frontend automated harness is still thin | Browser smoke now exists in pytest, but there is still no dedicated frontend unit/component runner | Keep expanding page-level smoke/contract checks before deeper E2E |
| Payment verification is still mock-heavy | Backend tests cover routes/webhooks, not live provider confirmation | Add sandbox confirmation steps before production |
| Browser-rendered SEO drift can go unnoticed | Static head/sitemap assertions now exist in `tests/test_seo_assets.py`, but no browser-level crawl smoke exists | Add browser smoke for canonical/OG on `/blog` and key landing pages |

---

### Updated Execution Order

| Order | What To Lock Next | Reason |
|------|--------------------|--------|
| 1 | Frontend browser smoke + contract tests | The backend is green; UI-page/API drift is now the highest automation gap |
| 2 | Payment sandbox verification | Needed to move from mocked confidence to provider confidence |
| 3 | Paid-report and video-link integration tests | These are the most stateful remaining product flows |
| 4 | Browser-level SEO regression checks | Static metadata is covered; browser assertions should verify final rendered pages |
| 5 | Expand E2E only after those contracts are stable | Avoid slow browser tests masking simpler regressions |

---

## PART B: COMPLETE TEST CASE DEFINITIONS (~530 Cases)

### Test Environment Setup

**Prerequisites**
```
Backend:  Python 3.11+, pip install -r requirements.txt
Frontend: Node 20+, cd frontend && npm install
E2E:      npx playwright install chromium
Database: Fresh astrovedic_test.db (auto-created)
```

**Environment Variables (`.env.test`)**
```
DB_PATH=astrovedic_test.db
JWT_SECRET=test-secret-key-for-testing
BACKEND_PORT=8028
FRONTEND_PORT=5198
OPENAI_API_KEY=sk-test-mock-key
OPENAI_MODEL=gpt-4
RAZORPAY_KEY_ID=rzp_test_xxxx
RAZORPAY_KEY_SECRET=test_secret
STRIPE_SECRET_KEY=sk_test_xxxx
STRIPE_WEBHOOK_SECRET=whsec_test
CORS_ORIGINS=http://localhost:5198
RATE_LIMIT_PER_MINUTE=1000
```

**Test Fixtures (Reused Across All Suites)**

| Fixture | Description |
|---------|-------------|
| `test_user` | `{email: "test@astro.com", password: "test123456", name: "Test User"}` |
| `test_admin` | `{email: "admin@astro.com", password: "admin123456", name: "Admin", role: "admin"}` |
| `test_astrologer` | `{email: "astrologer@astro.com", password: "astro123456", name: "Pandit Ji", role: "astrologer"}` |
| `test_kundli_data` | `{person_name: "Meharban Singh", birth_date: "1998-03-15", birth_time: "06:30:00", birth_place: "Delhi", latitude: 28.6139, longitude: 77.2090, timezone_offset: 5.5, ayanamsa: "lahiri"}` |
| `test_product` | `{name: "Yellow Sapphire", description: "Natural Pukhraj", category: "gemstone", price: 5999.0, stock: 10}` |
| `auth_header(token)` | `{"Authorization": f"Bearer {token}"}` |

---

### 1. Backend Unit Tests — Astrology Engines

#### 1.1 Astro Engine (`app/engines/astro_engine.py`)

| # | Test Case | Input | Expected | Priority |
|---|-----------|-------|----------|----------|
| U-AE-001 | Calculate Sun position for known date | `2024-01-01, 12:00, lat=28.6, lon=77.2` | Sun longitude within 1° of known value (~279° Sagittarius) | HIGH |
| U-AE-002 | Calculate Moon position | Same date | Moon longitude within 2° of known value | HIGH |
| U-AE-003 | Calculate all 9 planets | Same date | All 9 returned: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu | HIGH |
| U-AE-004 | Rahu and Ketu 180° apart | Any date | `abs(rahu - ketu) ≈ 180 ± 1°` | HIGH |
| U-AE-005 | Zodiac sign assignment | Sun at 279° | Sagittarius (270°-300°) | HIGH |
| U-AE-006 | Nakshatra assignment | Moon at specific degree | Correct nakshatra (1-27) | HIGH |
| U-AE-007 | House calculation (Placidus) | Birth data | 12 house cusps, Ascendant = House 1 | HIGH |
| U-AE-008 | Lahiri ayanamsa applied | Any date | Tropical - Sidereal offset ≈ 24.1° (for 2024) | MEDIUM |
| U-AE-009 | Meeus fallback when swisseph unavailable | Mock swisseph import fail | Uses Meeus, results within ~1° | HIGH |
| U-AE-010 | Negative longitude (Western hemisphere) | `lat=40.7, lon=-74.0` (NYC) | Valid positions returned | MEDIUM |
| U-AE-011 | Extreme latitude (Arctic) | `lat=70.0, lon=25.0` | No crash, valid results | LOW |
| U-AE-012 | Date at epoch boundary | `1900-01-01` | Valid, no overflow | LOW |
| U-AE-013 | Future date (2050) | `2050-06-15` | Valid calculation | LOW |
| U-AE-014 | Timezone offset applied correctly | `tz=5.5` (IST) | UTC conversion correct | HIGH |
| U-AE-015 | Aspect calculation | Two planet positions | Conjunction/Opposition/Trine/Square identified | MEDIUM |

#### 1.2 io-gita Engine (`app/engines/astro_iogita_engine.py`)

| # | Test Case | Input | Expected | Priority |
|---|-----------|-------|----------|----------|
| U-IG-001 | All 16 atoms in output | Valid chart_data | DHARMA, SATYA, TYAGA, AHANKAR, ATMA, MOKSHA, KULA, RAJYA, NYAYA, KRODHA, NITI, SHAKTI, BHAKTI, KAAM, LOBH, MOH | HIGH |
| U-IG-002 | Atom values normalized | Valid chart | All in [-1.0, 1.0] | HIGH |
| U-IG-003 | Exalted = 0.95 | Sun in Aries | strength = 0.95 | HIGH |
| U-IG-004 | Debilitated = 0.20 | Sun in Libra | strength = 0.20 | HIGH |
| U-IG-005 | Own sign = 0.80 | Sun in Leo | strength = 0.80 | MEDIUM |
| U-IG-006 | Mool trikona = 0.75 | Verified combo | strength = 0.75 | MEDIUM |
| U-IG-007 | Basin: Dharma-Yukta | ATMA, DHARMA dominant | basin = "Dharma-Yukta" | HIGH |
| U-IG-008 | Basin: Kama-Moha | KAAM, LOBH dominant | basin = "Kama-Moha" | HIGH |
| U-IG-009 | All 8 basins identified | 8 configs | Each maps to correct basin | HIGH |
| U-IG-010 | Meharban Singh known chart | Known birth data | Matches astro_meharban_result.json | HIGH |
| U-IG-011 | Dasha amplification | Active Jupiter Mahadasha | DHARMA, MOKSHA boosted | MEDIUM |
| U-IG-012 | Escape trajectory present | Any basin | Non-empty string | MEDIUM |
| U-IG-013 | Warnings for negative basins | Kama-Moha | Non-empty warnings list | MEDIUM |
| U-IG-014 | Empty chart_data handled | `{}` | Graceful error, no crash | HIGH |
| U-IG-015 | Missing planets handled | Only 5 planets | Partial analysis, no crash | MEDIUM |

#### 1.3 Panchang Engine (`app/engines/panchang_engine.py`)

| # | Test Case | Input | Expected | Priority |
|---|-----------|-------|----------|----------|
| U-PA-001 | Tithi for known date | `2024-01-15, Delhi` | Correct tithi (1-30) | HIGH |
| U-PA-002 | Nakshatra calculation | Same date | Correct nakshatra (1-27) | HIGH |
| U-PA-003 | Yoga calculation | Same date | Correct yoga (1-27) | HIGH |
| U-PA-004 | Karana calculation | Same date | Correct karana (1-11 repeating) | MEDIUM |
| U-PA-005 | Sunrise/Sunset Delhi | `2024-06-21, 28.6, 77.2` | Sunrise ~05:22 IST ± 5min | HIGH |
| U-PA-006 | Sunrise varies by longitude | Delhi vs Mumbai | Mumbai ~10min later | MEDIUM |
| U-PA-007 | Rahu Kaal Monday | `weekday=0` | 07:30-09:00 relative to sunrise | HIGH |
| U-PA-008 | Rahu Kaal all 7 days | Days 0-6 | Unique 1.5hr windows, no overlap | HIGH |
| U-PA-009 | Choghadiya returns 8 | Any date+location | 8 periods with name, start, end, quality | MEDIUM |
| U-PA-010 | Purnima detection | `2024-01-25` | Tithi = 15 | HIGH |
| U-PA-011 | Amavasya detection | `2024-01-11` | Tithi = 30 | HIGH |
| U-PA-012 | Southern hemisphere | `lat=-33.8, lon=151.2` (Sydney) | Valid results | LOW |

#### 1.4 Dasha Engine (`app/engines/dasha_engine.py`)

| # | Test Case | Input | Expected | Priority |
|---|-----------|-------|----------|----------|
| U-DA-001 | Vimshottari sequence | Any nakshatra | Ketu→Venus→Sun→Moon→Mars→Rahu→Jupiter→Saturn→Mercury | HIGH |
| U-DA-002 | Periods sum to 120 years | Full dasha | 7+20+6+10+7+18+16+19+17 = 120 | HIGH |
| U-DA-003 | Start from birth nakshatra | Ashwini (Ketu) | First Mahadasha = Ketu | HIGH |
| U-DA-004 | Remaining balance calculated | Moon at 5° in Ashwini | Ketu balance = 7*(1-5/13.33) years | HIGH |
| U-DA-005 | Antardasha subdivisions | Ketu Mahadasha | 9 Antardashas, proportional | HIGH |
| U-DA-006 | Current dasha for date | Birth + 25 years | Correct active Mahadasha/Antardasha | MEDIUM |
| U-DA-007 | Dates in ISO format | Any dasha | All YYYY-MM-DD | MEDIUM |

#### 1.5 Dosha Engine (`app/engines/dosha_engine.py`)

| # | Test Case | Input | Expected | Priority |
|---|-----------|-------|----------|----------|
| U-DO-001 | Mangal: Mars in 7th | house=7 | `mangal_dosha: true, severity: High` | HIGH |
| U-DO-002 | Mangal: Mars in 1st | house=1 | `mangal_dosha: true` | HIGH |
| U-DO-003 | Mangal: Mars in 5th (safe) | house=5 | `mangal_dosha: false` | HIGH |
| U-DO-004 | Mangal cancelled by Jupiter | house=7, Jupiter aspecting | `false` or `Low` | MEDIUM |
| U-DO-005 | Kaal Sarp: all between Rahu-Ketu | Specific layout | `kaal_sarp: true` | HIGH |
| U-DO-006 | Kaal Sarp: scattered | Scattered planets | `kaal_sarp: false` | HIGH |
| U-DO-007 | Sade Sati: Saturn in 12th from Moon | Moon=Aries, Saturn=Pisces | `active: true, phase: "Rising"` | HIGH |
| U-DO-008 | Sade Sati: Saturn in 1st from Moon | Moon=Aries, Saturn=Aries | `active: true, phase: "Peak"` | HIGH |
| U-DO-009 | Sade Sati: Saturn in 2nd from Moon | Moon=Aries, Saturn=Taurus | `active: true, phase: "Setting"` | HIGH |
| U-DO-010 | Sade Sati: Saturn in 5th from Moon | | `active: false` | HIGH |

#### 1.6 Matching Engine (`app/engines/matching_engine.py`)

| # | Test Case | Input | Expected | Priority |
|---|-----------|-------|----------|----------|
| U-MA-001 | Gun Milan total out of 36 | Two charts | Score 0-36 | HIGH |
| U-MA-002 | Varna matching (1 pt) | Same varna | varna_score = 1 | MEDIUM |
| U-MA-003 | Nadi match (8 pts) | Different nadi | nadi_score = 8 | HIGH |
| U-MA-004 | Nadi mismatch (0 pts) | Same nadi | nadi_score = 0, nadi_dosha = true | HIGH |
| U-MA-005 | Perfect match (36/36) | Ideal combo | total=36, "Excellent" | MEDIUM |
| U-MA-006 | Poor match (<18/36) | Bad combo | total<18, "Not recommended" | MEDIUM |
| U-MA-007 | All 8 categories scored | Any pair | varna, vasya, tara, yoni, graha_maitri, gana, bhakoot, nadi | HIGH |
| U-MA-008 | Compatibility percentage | Score=27 | 75% | MEDIUM |

#### 1.7 Other Engines

| # | Test Case | Engine | Expected | Priority |
|---|-----------|--------|----------|----------|
| U-DC-001 | D9 Navamsa division | divisional_charts | Correct sign from degree | HIGH |
| U-DC-002 | D10 Dasamsa | divisional_charts | Correct D10 sign | MEDIUM |
| U-AK-001 | Ashtakvarga total = 337 | ashtakvarga | Total bindhu = 337 | HIGH |
| U-AK-002 | Per-planet bindhu 0-8 | ashtakvarga | Each value 0-8 | HIGH |
| U-KP-001 | 12 cusps with star_lord + sub_lord | kp_engine | 12 cusps | HIGH |
| U-KP-002 | Sub-lord precision | kp_engine | Correct sub-lord | MEDIUM |
| U-LK-001 | Remedies per planet | lalkitab | Non-empty remedies for each of 9 planets | HIGH |
| U-NM-001 | Life Path from DOB | numerology | `1998-03-15` → 1+9+9+8+0+3+1+5=36→9 | HIGH |
| U-NM-002 | Name number | numerology | Correct alphabetic sum → single digit | MEDIUM |
| U-TR-001 | Single card draw | tarot | 1 card from 78 | HIGH |
| U-TR-002 | Three-card spread | tarot | 3 unique cards | HIGH |
| U-TR-003 | Celtic Cross | tarot | 10 unique cards | HIGH |
| U-TR-004 | No duplicates | tarot | All unique within spread | HIGH |
| U-PR-001 | Ram Shalaka valid | prashnavali | row=1,col=1 → non-empty answer | HIGH |
| U-PR-002 | Ram Shalaka boundary | prashnavali | row=15,col=15 → valid | MEDIUM |
| U-PR-003 | Hanuman Prashna | prashnavali | Non-empty oracle | HIGH |
| U-PR-004 | Gita Prashnavali | prashnavali | Response with verse reference | HIGH |

#### 1.8 AI Engine (`app/engines/ai_engine.py`)

| # | Test Case | Input | Expected | Priority |
|---|-----------|-------|----------|----------|
| U-AI-001 | Kundli interpretation (mocked) | chart_data | Non-empty astrological content | HIGH |
| U-AI-002 | Free Q&A (mocked) | "Will I get married?" | Non-empty answer | HIGH |
| U-AI-003 | Gita AI (mocked) | "What is dharma?" | Response with verse refs | HIGH |
| U-AI-004 | Remedies (mocked) | chart_data + question | Mantras/gemstones | HIGH |
| U-AI-005 | Oracle yes/no (mocked) | "Will I pass?" | yes/no with explanation | HIGH |
| U-AI-006 | Fallback when no API key | OPENAI_API_KEY="" | Fallback response, no crash | HIGH |
| U-AI-007 | Token counting | Mocked response | tokens_used > 0 | MEDIUM |
| U-AI-008 | Temperature is 0.7 | Inspect call args | temperature=0.7 | LOW |

---

### 2. Backend Unit Tests — Auth & Security

| # | Test Case | Input | Expected | Priority |
|---|-----------|-------|----------|----------|
| U-AU-001 | Password hashing (bcrypt) | "test123456" | Hashed != plaintext, starts with `$2b$` | HIGH |
| U-AU-002 | Password verification pass | hash + "test123456" | True | HIGH |
| U-AU-003 | Password verification fail | hash + "wrong" | False | HIGH |
| U-AU-004 | JWT generation | `{sub, email, role}` | Valid JWT, 3 parts | HIGH |
| U-AU-005 | JWT decode | Valid token | Correct sub, email, role | HIGH |
| U-AU-006 | JWT expired | exp = past | 401 | HIGH |
| U-AU-007 | JWT tampered | Modified payload | 401 | HIGH |
| U-AU-008 | JWT wrong secret | Different key | 401 | HIGH |
| U-AU-009 | require_role("admin") with user | role="user" | 403 | HIGH |
| U-AU-010 | require_role("admin") with admin | role="admin" | Pass | HIGH |
| U-AU-011 | require_role("user","admin") | role="user" | Pass | MEDIUM |
| U-AU-012 | Missing Authorization header | No header | 401 | HIGH |
| U-AU-013 | Malformed Bearer token | "Bearer garbage" | 401 | HIGH |

---

### 3. Backend API Tests — Auth Routes

| # | Test Case | Method + Path | Expected | Priority |
|---|-----------|---------------|----------|----------|
| A-AU-001 | Register new user | POST `/api/auth/register` | 201, `{user, token}` | HIGH |
| A-AU-002 | Register duplicate email | POST same email | 409, "Email already registered" | HIGH |
| A-AU-003 | Register missing email | `{password, name}` | 422 | HIGH |
| A-AU-004 | Register short password | password="12345" | 422 (min 6) | HIGH |
| A-AU-005 | Register empty name | name="" | 422 (min 1) | HIGH |
| A-AU-006 | Register invalid email | "notanemail" | 422 | HIGH |
| A-AU-007 | Register with optional fields | phone, dob, gender, city | 201, all saved | MEDIUM |
| A-AU-008 | Token valid after register | Decode response token | sub = user id | HIGH |
| A-AU-010 | Login valid | POST `/api/auth/login` | 200, `{user, token}` | HIGH |
| A-AU-011 | Login wrong password | | 401 | HIGH |
| A-AU-012 | Login non-existent email | | 401 | HIGH |
| A-AU-013 | Login deactivated user | is_active=0 | 403 | HIGH |
| A-AU-020 | Get profile | GET `/api/auth/me` | 200, `{id, email, name, role}` | HIGH |
| A-AU-021 | Get profile no token | | 401 | HIGH |
| A-AU-022 | Update profile name | PATCH `/api/auth/profile` | 200, name updated | HIGH |
| A-AU-023 | Update all fields | name, phone, dob, gender, city, avatar_url | 200 | MEDIUM |
| A-AU-024 | Invalid gender | gender="xyz" | 400 | MEDIUM |
| A-AU-025 | Empty body | `{}` | 400 | MEDIUM |
| A-AU-026 | Change password success | POST `/api/auth/change-password` | 200 | HIGH |
| A-AU-027 | Change password wrong current | | 400 | HIGH |

---

### 4. Backend API Tests — Kundli Routes

| # | Test Case | Method + Path | Expected | Priority |
|---|-----------|---------------|----------|----------|
| A-KU-001 | Generate kundli | POST `/api/kundli/generate` | 201, `{id, chart_data: {planets[9], houses[12]}}` | HIGH |
| A-KU-002 | chart_data has 9 planets | | Sun thru Ketu | HIGH |
| A-KU-003 | chart_data has 12 houses | | 12 house objects | HIGH |
| A-KU-004 | Invalid latitude (95) | | 422 | HIGH |
| A-KU-005 | Invalid longitude (200) | | 422 | HIGH |
| A-KU-006 | Invalid timezone (15) | | 422 | MEDIUM |
| A-KU-007 | No auth | | 401 | HIGH |
| A-KU-008 | List kundlis | GET `/api/kundli/list` | 200, user's array | HIGH |
| A-KU-009 | Only own kundlis | Login as user B | Empty array | HIGH |
| A-KU-010 | Get by ID | GET `/api/kundli/{id}` | 200, full + parsed JSON | HIGH |
| A-KU-011 | Not found | Invalid id | 404 | HIGH |
| A-KU-012 | Not own kundli | User B → A's kundli | 404 | HIGH |
| A-KU-013 | io-gita analysis | POST `/{id}/iogita` | 200, `{atoms, basin, escape_trajectory}` | HIGH |
| A-KU-014 | 16 atoms present | | All 16 keys | HIGH |
| A-KU-015 | Basin is valid | | One of 8 basins | HIGH |
| A-KU-016 | Matching | POST `/api/kundli/match` | 200, `{total_score: 0-36, categories, percentage}` | HIGH |
| A-KU-017 | Self-match | Same kundli twice | 200 (should work) | MEDIUM |
| A-KU-018 | Dosha analysis | POST `/{id}/dosha` | 200, `{mangal, kaal_sarp, sade_sati}` | HIGH |
| A-KU-019 | Dasha analysis | POST `/{id}/dasha` | 200, `{mahadasha, current_dasha}` | HIGH |
| A-KU-020 | Divisional D9 | POST `/{id}/divisional` | 200, D9 chart | HIGH |
| A-KU-021 | Divisional D10 | | 200, D10 | MEDIUM |
| A-KU-022 | Invalid chart type D99 | | 400 | MEDIUM |
| A-KU-023 | Ashtakvarga | POST `/{id}/ashtakvarga` | 200, bindhu results | HIGH |

---

### 5. Backend API Tests — Horoscope Routes

| # | Test Case | Expected | Priority |
|---|-----------|----------|----------|
| A-HO-001 | GET `/api/horoscope/aries?period=daily` | 200, `{sign, period, content}` | HIGH |
| A-HO-002 | Weekly horoscope | 200 | HIGH |
| A-HO-003 | Monthly | 200 | MEDIUM |
| A-HO-004 | Yearly | 200 | MEDIUM |
| A-HO-005 | Invalid sign | 422 | HIGH |
| A-HO-006 | All 12 signs return data | 200 each | MEDIUM |
| A-HO-007 | No auth required | 200 | HIGH |
| A-HO-008 | Default period = daily | 200 | MEDIUM |

---

### 6. Backend API Tests — Panchang Routes

| # | Test Case | Expected | Priority |
|---|-----------|----------|----------|
| A-PC-001 | GET `/api/panchang?lat=28.6&lon=77.2` | 200, `{tithi, nakshatra, yoga, karana, sunrise, sunset}` | HIGH |
| A-PC-002 | Specific date | 200 | HIGH |
| A-PC-003 | Invalid date format | 400 | HIGH |
| A-PC-004 | Default location | 200, uses Delhi | MEDIUM |
| A-PC-005 | Tithi structure | `{number, name, paksha}` | HIGH |
| A-PC-006 | Nakshatra structure | `{number, name, pada}` | HIGH |
| A-PC-007 | Rahu Kaal | 200, `{start, end}` | HIGH |
| A-PC-008 | Choghadiya | 200, 8 periods | HIGH |
| A-PC-009 | Muhurat (marriage) | 200, auspicious dates | HIGH |
| A-PC-010 | Festivals | 200, 15+ items | HIGH |
| A-PC-011 | Festivals by year | 200, filtered | MEDIUM |
| A-PC-012 | Sunrise < sunset | Always | HIGH |
| A-PC-013 | Caching works | Second call uses cache | MEDIUM |
| A-PC-014 | No auth required | 200 | HIGH |

---

### 7. Backend API Tests — AI Routes

| # | Test Case | Expected | Priority |
|---|-----------|----------|----------|
| A-AI-001 | POST `/api/ai/interpret` `{kundli_id}` | 200, non-empty interpretation | HIGH |
| A-AI-002 | Invalid kundli_id | 404 | HIGH |
| A-AI-003 | POST `/api/ai/ask` | 200, non-empty answer | HIGH |
| A-AI-004 | Ask with kundli context | 200, references chart | HIGH |
| A-AI-005 | Empty question | 422 | HIGH |
| A-AI-006 | POST `/api/ai/gita` | 200, Gita references | HIGH |
| A-AI-007 | Gita: no auth | 200 (public) | HIGH |
| A-AI-008 | POST `/api/ai/remedies` | 200, mantras/gemstones | HIGH |
| A-AI-009 | Remedies: no kundli_id | 400 | HIGH |
| A-AI-010 | Oracle yes/no | 200 | HIGH |
| A-AI-011 | Oracle tarot | 200 | HIGH |
| A-AI-012 | GET `/api/ai/history` | 200, `{chats, total}` | HIGH |
| A-AI-013 | History pagination | Different results page 1 vs 2 | MEDIUM |
| A-AI-014 | Chat logged in DB | Row exists in ai_chat_logs | HIGH |
| A-AI-015 | Fallback no API key | 200, fallback response | HIGH |
| A-AI-016 | Auth required (interpret/ask/remedies) | 401 without token | HIGH |

---

### 8. Backend API Tests — Prashnavali Routes

| # | Test Case | Expected | Priority |
|---|-----------|----------|----------|
| A-PV-001 | Ram Shalaka `{row:7, col:7}` | 200, `{answer, meaning}` | HIGH |
| A-PV-002 | Row out of range (16) | 422 | HIGH |
| A-PV-003 | Col out of range (0) | 422 | HIGH |
| A-PV-004 | Hanuman Prashna | 200, oracle response | HIGH |
| A-PV-005 | Ramcharitmanas | 200, oracle response | HIGH |
| A-PV-006 | Gita Prashnavali | 200, verse oracle | HIGH |
| A-PV-007 | Logged in DB | Row in prashnavali_logs | MEDIUM |
| A-PV-008 | No auth required | 200 | HIGH |

---

### 9. Backend API Tests — Library & Gita Routes

| # | Test Case | Expected | Priority |
|---|-----------|----------|----------|
| A-LB-001 | GET `/api/gita/chapters` | 200, 18 chapters | HIGH |
| A-LB-002 | GET `/api/gita/chapter/1` | 200, Arjuna Vishada Yoga | HIGH |
| A-LB-003 | GET `/api/gita/chapter/18` | 200, Moksha Sannyasa | HIGH |
| A-LB-004 | Chapter 0 (invalid) | 400 | HIGH |
| A-LB-005 | Chapter 19 (invalid) | 400 | HIGH |
| A-LB-006 | Library: aarti | 200, array | HIGH |
| A-LB-007 | Library: mantra | 200, array | HIGH |
| A-LB-008 | Library: pooja | 200, array | HIGH |
| A-LB-009 | Library: chalisa | 200, array | MEDIUM |
| A-LB-010 | Library: vrat_katha | 200, array | MEDIUM |
| A-LB-011 | Invalid category | 400 | HIGH |
| A-LB-012 | Item by ID | 200, full content | HIGH |
| A-LB-013 | Item not found | 404 | HIGH |
| A-LB-014 | Content has title + content | Non-empty | HIGH |
| A-LB-015 | Gita items have sanskrit | Present | MEDIUM |
| A-LB-016 | No auth required | 200 | HIGH |

---

### 10. Backend API Tests — Numerology, Tarot, Palmistry

| # | Test Case | Expected | Priority |
|---|-----------|----------|----------|
| A-NM-001 | Numerology calculate | 200, `{life_path, expression, soul_urge}` | HIGH |
| A-NM-002 | Life path 1-9 (or 11/22/33) | Valid | HIGH |
| A-NM-003 | Empty name | 422 | HIGH |
| A-NM-004 | Invalid date | 400/422 | HIGH |
| A-NM-005 | Tarot single | 200, 1 card | HIGH |
| A-NM-006 | Tarot three | 200, 3 cards | HIGH |
| A-NM-007 | Tarot celtic cross | 200, 10 cards | HIGH |
| A-NM-008 | Card has name, meaning | `{name, suit, arcana, meaning_upright}` | HIGH |
| A-NM-009 | No duplicate cards | All unique | HIGH |
| A-NM-010 | Palmistry guide | 200, `{lines, mounts, shapes}` | HIGH |
| A-NM-011 | Has Heart/Head/Life lines | Present | HIGH |
| A-NM-012 | No auth required | 200 | HIGH |

---

### 11. Backend API Tests — KP & Lal Kitab

| # | Test Case | Expected | Priority |
|---|-----------|----------|----------|
| A-KP-001 | KP cuspal chart | 200, cusps with star_lord + sub_lord | HIGH |
| A-KP-002 | 12 cusps present | length = 12 | HIGH |
| A-KP-003 | Missing kundli_id | 400 | HIGH |
| A-KP-004 | Invalid kundli | 404 | HIGH |
| A-KP-005 | Lal Kitab remedies | 200, `{remedies_by_planet}` | HIGH |
| A-KP-006 | Remedy has mantra, gemstone | Non-empty list | HIGH |
| A-KP-007 | Auth required | 401 | HIGH |

---

### 12. Backend API Tests — Products

| # | Test Case | Expected | Priority |
|---|-----------|----------|----------|
| A-PR-001 | List all | 200, `{products, total >= 12}` | HIGH |
| A-PR-002 | Filter: gemstone | All category="gemstone" | HIGH |
| A-PR-003 | Filter: rudraksha | Only rudraksha | MEDIUM |
| A-PR-004 | Pagination limit=5 | Max 5 | HIGH |
| A-PR-005 | Page 2 | Different from page 1 | HIGH |
| A-PR-006 | Single product | 200, `{id, name, price, stock}` | HIGH |
| A-PR-007 | Not found | 404 | HIGH |
| A-PR-008 | Price > 0 | Always | HIGH |
| A-PR-009 | Stock >= 0 | Always | HIGH |
| A-PR-010 | No auth for listing | 200 | HIGH |
| A-PR-011 | Inactive hidden | Not in public list | MEDIUM |

---

### 13. Backend API Tests — Cart

| # | Test Case | Expected | Priority |
|---|-----------|----------|----------|
| A-CA-001 | Empty cart | 200, `{items: [], total: 0}` | HIGH |
| A-CA-002 | Add product | 201, `{items, total}` | HIGH |
| A-CA-003 | Add same again | Quantity incremented | HIGH |
| A-CA-004 | Insufficient stock | 400 | HIGH |
| A-CA-005 | Inactive product | 404 | HIGH |
| A-CA-006 | Invalid product_id | 404 | HIGH |
| A-CA-007 | Update quantity | 200, updated total | HIGH |
| A-CA-008 | Quantity 0 | 422 | HIGH |
| A-CA-009 | Exceed stock | 400 | HIGH |
| A-CA-010 | Remove item | 200, updated | HIGH |
| A-CA-011 | Remove non-existent | 404 | HIGH |
| A-CA-012 | Total = sum(price*qty) | Correct | HIGH |
| A-CA-013 | Items have product details | name, price, image_url, stock | HIGH |
| A-CA-014 | Auth required all routes | 401 | HIGH |
| A-CA-015 | Cart isolated per user | Each sees own | HIGH |

---

### 14. Backend API Tests — Orders

| # | Test Case | Expected | Priority |
|---|-----------|----------|----------|
| A-OR-001 | Create from cart (COD) | 201, `{id, status:"placed"}` | HIGH |
| A-OR-002 | Empty cart | 400 | HIGH |
| A-OR-003 | Short address (<10) | 422 | HIGH |
| A-OR-004 | Clears cart | GET cart → empty | HIGH |
| A-OR-005 | Reduces stock | Product stock decreased | HIGH |
| A-OR-006 | Race: stock=0 before order | 400 | HIGH |
| A-OR-007 | Items match cart | Same products/quantities | HIGH |
| A-OR-008 | Total matches | Order total = cart total | HIGH |
| A-OR-009 | List orders | 200, user's array | HIGH |
| A-OR-010 | Get by ID | 200, with items | HIGH |
| A-OR-011 | Not found | 404 | HIGH |
| A-OR-012 | Not mine | 404 (ownership) | HIGH |
| A-OR-013 | Razorpay method | 201, payment_status="pending" | HIGH |
| A-OR-014 | Stripe method | 201, payment_status="pending" | HIGH |
| A-OR-015 | Auth required | 401 | HIGH |

---

### 15. Backend API Tests — Payments

| # | Test Case | Expected | Priority |
|---|-----------|----------|----------|
| A-PY-001 | Initiate COD | 200, `{payment_id, status:"pending"}` | HIGH |
| A-PY-002 | Initiate Razorpay | 200, `{razorpay_key_id, provider_payment_id}` | HIGH |
| A-PY-003 | Initiate Stripe | 200, `{payment_url}` | HIGH |
| A-PY-004 | Order not found | 404 | HIGH |
| A-PY-005 | Already paid | 400 | HIGH |
| A-PY-006 | Idempotent initiate | Same pending payment returned | HIGH |
| A-PY-007 | Razorpay webhook success | 200, payment→"completed" | HIGH |
| A-PY-008 | Razorpay: invalid signature | 400 | HIGH |
| A-PY-009 | Stripe webhook success | 200, payment→"completed" | HIGH |
| A-PY-010 | Stripe: invalid signature | 400 | HIGH |
| A-PY-011 | Webhook updates order | payment_status="paid", status="confirmed" | HIGH |
| A-PY-012 | Failed payment webhook | payment_status→"failed" | HIGH |
| A-PY-013 | Auth for initiate | 401 | HIGH |
| A-PY-014 | Webhooks: no bearer (external) | 200 with signature | HIGH |
| A-PY-015 | Webhook replay idempotency | No duplicate confirmation | CRITICAL |
| A-PY-016 | State consistency after paid | payment="paid", order="confirmed" | HIGH |

---

### 16. Backend API Tests — Consultation

| # | Test Case | Expected | Priority |
|---|-----------|----------|----------|
| A-CO-001 | List astrologers | 200, array | HIGH |
| A-CO-002 | Only approved | Unapproved excluded | HIGH |
| A-CO-003 | Get by ID | 200, profile | HIGH |
| A-CO-004 | Not found | 404 | HIGH |
| A-CO-005 | Book: chat | 201, `{status:"requested"}` | HIGH |
| A-CO-006 | Book: call | 201 | HIGH |
| A-CO-007 | Book: video | 201 | MEDIUM |
| A-CO-008 | Not found astrologer | 404 | HIGH |
| A-CO-009 | Not approved | 400 | HIGH |
| A-CO-010 | Unavailable | 400 | HIGH |
| A-CO-011 | With scheduled_at | 201, saved | MEDIUM |
| A-CO-012 | List my consultations | 200, with astrologer_name | HIGH |
| A-CO-013 | Auth required | 401 | HIGH |
| A-CO-014 | Listing is public | 200 without token | HIGH |
| A-CO-015 | Video session URL (Jitsi) | 200, valid URL | HIGH |
| A-CO-016 | Access before accept | 403 | HIGH |
| A-CO-018 | Regional language JSON | 200, array stored | HIGH |

---

### 17. Backend API Tests — Messages & WebSocket

| # | Test Case | Expected | Priority |
|---|-----------|----------|----------|
| A-WS-001 | Connect with valid token | Connection accepted | HIGH |
| A-WS-002 | No token | Close 4001 "Missing token" | HIGH |
| A-WS-003 | Invalid token | Close 4001 "Invalid token" | HIGH |
| A-WS-004 | Consultation not found | Close 4004 | HIGH |
| A-WS-005 | Not a participant | Close 4003 | HIGH |
| A-WS-006 | Not accepted status | Close 4002 | HIGH |
| A-WS-010 | Send text | Broadcast to all | HIGH |
| A-WS-011 | Receive broadcast | User B gets A's message | HIGH |
| A-WS-012 | Message persisted | Row in messages table | HIGH |
| A-WS-013 | Connection activates consultation | status→"active", started_at set | HIGH |
| A-WS-014 | Empty content | Error or ignored | MEDIUM |

---

### 18. Backend API Tests — Reports

| # | Test Case | Expected | Priority |
|---|-----------|----------|----------|
| A-RP-001 | Request full_kundli report | 201, `{price: 999, status:"pending"}` | HIGH |
| A-RP-002 | Marriage = 799 | price = 799 | HIGH |
| A-RP-003 | Career = 799 | price = 799 | HIGH |
| A-RP-004 | Health = 699 | price = 699 | HIGH |
| A-RP-005 | Yearly = 599 | price = 599 | HIGH |
| A-RP-006 | Invalid kundli | 404 | HIGH |
| A-RP-007 | List reports | 200, `{reports}` | HIGH |
| A-RP-008 | Get by ID | 200 | HIGH |
| A-RP-009 | Not found | 404 | HIGH |
| A-RP-010 | Auth required | 401 | HIGH |

---

### 19. Backend API Tests — Astrologer Routes

| # | Test Case | Expected | Priority |
|---|-----------|----------|----------|
| A-AS-001 | Dashboard | 200, `{earnings, consultations, rating}` | HIGH |
| A-AS-002 | Not astrologer | 403 | HIGH |
| A-AS-003 | List consultations | 200, this astrologer only | HIGH |
| A-AS-004 | Update profile | 200 | HIGH |
| A-AS-005 | No fields | 400 | MEDIUM |
| A-AS-006 | Set available | 200, is_available=true | HIGH |
| A-AS-007 | Set unavailable | 200, is_available=false | HIGH |
| A-AS-008 | Accept consultation | 200, status→"accepted" | HIGH |
| A-AS-009 | Not my consultation | 403 | HIGH |
| A-AS-010 | Complete consultation | 200, status→"completed" | HIGH |
| A-AS-011 | Increments total | total_consultations += 1 | MEDIUM |
| A-AS-012 | Role required | 401/403 | HIGH |

---

### 20. Backend API Tests — Admin Routes

| # | Test Case | Expected | Priority |
|---|-----------|----------|----------|
| A-AD-001 | List users | 200, `{users, total}` | HIGH |
| A-AD-002 | Pagination | Max 10 | MEDIUM |
| A-AD-003 | User detail | 200, + activity counts | HIGH |
| A-AD-004 | Not found | 404 | HIGH |
| A-AD-005 | Create user | 201 | HIGH |
| A-AD-006 | Create admin | 201, role="admin" | HIGH |
| A-AD-007 | Duplicate email | 409 | HIGH |
| A-AD-008 | Deactivate user | 200, is_active=0 | HIGH |
| A-AD-009 | Deactivate self | 400 | HIGH |
| A-AD-010 | Activate user | 200, is_active=1 | HIGH |
| A-AD-011 | User activity | 200, `{kundlis, orders, consultations}` | MEDIUM |
| A-AD-012 | Update role | 200, role changed | HIGH |
| A-AD-013 | List orders | 200, with user_name | HIGH |
| A-AD-014 | Filter by status | All match filter | MEDIUM |
| A-AD-015 | Update order status + tracking | 200 | HIGH |
| A-AD-016 | Approve astrologer | 200, is_approved=1 | HIGH |
| A-AD-017 | AI logs | 200, with user_name | MEDIUM |
| A-AD-018 | Create content | 201 | HIGH |
| A-AD-019 | Update content | 200 | HIGH |
| A-AD-020 | Delete content | 204 | HIGH |
| A-AD-021 | Dashboard stats | 200, `{users, orders, revenue}` | HIGH |
| A-AD-022 | Create product | 201 | HIGH |
| A-AD-023 | Update product | 200 | HIGH |
| A-AD-024 | Update stock | 200, stock=50 | HIGH |
| A-AD-025 | Toggle active | 200, toggled | HIGH |
| A-AD-026 | User role → 403 | 403 | HIGH |
| A-AD-027 | No token → 401 | 401 | HIGH |
| A-AD-028 | Dashboard aggregate stats | Correct counts | HIGH |

---

### 21. Database Tests

| # | Test Case | Expected | Priority |
|---|-----------|----------|----------|
| D-DB-001 | Fresh DB: 18 tables | All created | HIGH |
| D-DB-002 | WAL mode | PRAGMA = "wal" | HIGH |
| D-DB-003 | Foreign keys ON | PRAGMA = 1 | HIGH |
| D-DB-004 | 30+ indexes | Check sqlite_master | HIGH |
| D-DB-005 | Seed: content_library 44+ rows | After seed_all() | HIGH |
| D-DB-006 | Seed: products 12 rows | | HIGH |
| D-DB-007 | Seed: festivals 15 rows | | HIGH |
| D-DB-008 | Unique email constraint | IntegrityError on duplicate | HIGH |
| D-DB-009 | FK cascade: user→kundli | Constraint prevents orphan | HIGH |
| D-DB-010 | CHECK: role enum | "hacker" → violation | HIGH |
| D-DB-011 | CHECK: price > 0 | -1 → violation | HIGH |
| D-DB-012 | CHECK: order status | "invalid" → violation | HIGH |
| D-DB-013 | UNIQUE cart (user, product) | Duplicate fails/updates | HIGH |
| D-DB-014 | Concurrent WAL reads | Both succeed | MEDIUM |
| D-DB-015 | Migration adds columns | dob, gender, city, is_active exist | HIGH |

---

### 22. Playwright E2E — Navigation & Layout

Config: `headless: false, slowMo: 500`, Base: `http://localhost:5198`

| # | Test Case | Expected | Screenshot |
|---|-----------|----------|------------|
| E-NV-001 | Home loads | No errors, Hero visible | `home--loaded.png` |
| E-NV-002 | Navbar visible | Logo + all links | `home--navbar.png` |
| E-NV-003 | Click Kundli | Navigates to /kundli | `nav--kundli.png` |
| E-NV-004 | Click Horoscope | /horoscope | `nav--horoscope.png` |
| E-NV-005 | Click Panchang | /panchang | `nav--panchang.png` |
| E-NV-006 | Click AI Chat | /ai-chat | `nav--aichat.png` |
| E-NV-007 | Click Library | /library | `nav--library.png` |
| E-NV-008 | Click Shop | /shop | `nav--shop.png` |
| E-NV-009 | Click Login | /login | `nav--login.png` |
| E-NV-010 | Footer on all pages | Visible on scroll | `home--footer.png` |
| E-NV-011 | No 404 for nav routes | All render content | — |
| E-NV-012 | Back button works | Returns to previous | — |
| E-NV-013 | Direct URL access | Page renders | — |
| E-NV-014 | Hero section | Heading, CTA visible | `home--hero.png` |
| E-NV-015 | Features section | Feature cards | `home--features.png` |
| E-NV-016 | About section | Text visible | `home--about.png` |
| E-NV-017 | Testimonials | Quotes visible | `home--testimonials.png` |
| E-NV-018 | CTA section | Button visible | `home--cta.png` |

---

### 23. Playwright E2E — Auth Flow

| # | Test Case | Expected | Screenshot |
|---|-----------|----------|------------|
| E-AU-001 | Login page renders | Email, Password, Login btn | `auth--login.png` |
| E-AU-002 | Switch to Register | Name field appears | `auth--register.png` |
| E-AU-003 | Register new user | Redirect, nav shows name | `auth--register-ok.png` |
| E-AU-004 | Empty fields submit | Validation errors | `auth--empty.png` |
| E-AU-005 | Duplicate email | Error shown | `auth--duplicate.png` |
| E-AU-006 | Short password | Error shown | `auth--short-pw.png` |
| E-AU-007 | Logout | Nav shows Login link | `auth--logout.png` |
| E-AU-008 | Login success | Logged in, nav updated | `auth--login-ok.png` |
| E-AU-009 | Wrong password | Error shown | `auth--wrong-pw.png` |
| E-AU-010 | Non-existent email | Error shown | `auth--no-user.png` |
| E-AU-011 | Token persists on reload | Still logged in | `auth--persist.png` |
| E-AU-012 | Protected route redirect | → /login | `auth--protected.png` |

---

### 24. Playwright E2E — Kundli Generator

| # | Test Case | Expected | Screenshot |
|---|-----------|----------|------------|
| E-KU-001 | Page renders | Form: Name, Date, Time, Place | `kundli--form.png` |
| E-KU-002 | Fill valid data | All fields populated | `kundli--filled.png` |
| E-KU-003 | Submit | Loading → Results | `kundli--results.png` |
| E-KU-004 | Planets table | 9 planets with Sign, Degree, House | `kundli--planets.png` |
| E-KU-005 | Ascendant shown | Sign + degree | `kundli--ascendant.png` |
| E-KU-006 | Moon sign shown | Prominently displayed | — |
| E-KU-007 | Empty name | Validation error | `kundli--empty-name.png` |
| E-KU-008 | No date | Validation error | `kundli--no-date.png` |
| E-KU-009 | No time | Validation error | — |
| E-KU-010 | No auth | Error or redirect | `kundli--no-auth.png` |
| E-KU-011 | Multiple kundlis | Both created | — |
| E-KU-012 | View saved | Full chart displayed | `kundli--saved.png` |

---

### 25. Playwright E2E — Horoscope

| # | Test Case | Expected | Screenshot |
|---|-----------|----------|------------|
| E-HO-001 | Page renders | 12 sign selectors | `horoscope--page.png` |
| E-HO-002 | Select Aries | Daily content loads | `horoscope--aries.png` |
| E-HO-003 | Switch to weekly | Weekly content | `horoscope--weekly.png` |
| E-HO-004-006 | Monthly, Yearly, All signs | Content updates | `horoscope--all.png` |
| E-HO-007 | No auth | Works | — |
| E-HO-008 | Empty content | "Coming soon" message | `horoscope--empty.png` |

---

### 26. Playwright E2E — Panchang

| # | Test Case | Expected | Screenshot |
|---|-----------|----------|------------|
| E-PC-001 | Page renders | Today's panchang | `panchang--today.png` |
| E-PC-002-005 | Tithi, Nakshatra, Yoga, Karana | All displayed | `panchang--details.png` |
| E-PC-006 | Sunrise/Sunset | HH:MM format | `panchang--times.png` |
| E-PC-007 | Change date | Updates | `panchang--custom.png` |
| E-PC-008 | Change location | Recalculates | `panchang--mumbai.png` |
| E-PC-009 | Rahu Kaal | Time range shown | `panchang--rahu.png` |
| E-PC-010 | No auth | Works | — |

---

### 27. Playwright E2E — AI Chat

| # | Test Case | Expected | Screenshot |
|---|-----------|----------|------------|
| E-AI-001 | Page renders | Input, send button | `aichat--page.png` |
| E-AI-002 | Send question | AI response appears | `aichat--response.png` |
| E-AI-003 | Response non-empty | Visible text | — |
| E-AI-004 | Multiple messages | All Q&A visible | `aichat--multi.png` |
| E-AI-005 | Empty prevented | Button disabled | `aichat--empty.png` |
| E-AI-006 | Long question | Accepted | — |
| E-AI-007 | Auth required | Redirect | `aichat--no-auth.png` |
| E-AI-008 | Loading state | Spinner shown | `aichat--loading.png` |

---

### 28. Playwright E2E — Spiritual Library

| # | Test Case | Expected | Screenshot |
|---|-----------|----------|------------|
| E-LB-001 | Page renders | Category tabs | `library--page.png` |
| E-LB-002 | Gita: 18 chapters | All listed | `library--gita.png` |
| E-LB-003 | Chapter 1 | Content, Sanskrit | `library--ch1.png` |
| E-LB-004 | Chapter 18 | Last chapter | `library--ch18.png` |
| E-LB-005-007 | Aarti, Mantra, Pooja | Lists shown | `library--content.png` |
| E-LB-008 | Click item | Full content page | `library--detail.png` |
| E-LB-009 | No auth | Works | — |
| E-LB-010 | Empty category | "No items" message | `library--empty.png` |

---

### 29. Playwright E2E — Shop & E-Commerce

#### Product Browsing

| # | Test Case | Expected | Screenshot |
|---|-----------|----------|------------|
| E-SH-001 | Shop renders | Product grid | `shop--page.png` |
| E-SH-002 | Cards: image, name, price | All present | `shop--cards.png` |
| E-SH-003-006 | Filter: gemstone/rudraksha/bracelet/all | Filtered correctly | `shop--filter.png` |
| E-SH-007 | Product click | Detail view | `shop--detail.png` |
| E-SH-008 | No auth for browsing | Works | — |

#### Cart Flow

| # | Test Case | Expected | Screenshot |
|---|-----------|----------|------------|
| E-SH-010 | Add to cart | Badge increments | `shop--add.png` |
| E-SH-011 | Add without auth | Login prompt | `shop--add-no-auth.png` |
| E-SH-012 | Badge count | Shows "2" | `shop--badge.png` |
| E-SH-013 | View cart | Items, quantities, total | `shop--cart.png` |
| E-SH-014 | Update quantity | Total recalculates | `shop--cart-qty.png` |
| E-SH-015 | Remove item | Removed, recalculated | `shop--cart-remove.png` |
| E-SH-016 | Empty cart | "Empty" message | `shop--cart-empty.png` |

#### Checkout Flow

| # | Test Case | Expected | Screenshot |
|---|-----------|----------|------------|
| E-SH-020 | Checkout form | Address, payment method | `shop--checkout.png` |
| E-SH-021 | Fill address | Populated | `shop--address.png` |
| E-SH-022 | Select COD | Selected | `shop--cod.png` |
| E-SH-023 | Place order | Confirmation with order ID | `shop--confirm.png` |
| E-SH-024 | Cart cleared | Empty | — |
| E-SH-025 | Order in history | Visible, status "placed" | `shop--history.png` |
| E-SH-026 | Order detail | Items, total, address | `shop--order.png` |
| E-SH-027 | Empty cart checkout | "Cart empty" error | `shop--checkout-empty.png` |
| E-SH-028 | Short address | Validation error | `shop--short-addr.png` |

#### Full Purchase E2E

| # | Test Case | Steps | Screenshot |
|---|-----------|-------|------------|
| E-SH-030 | Complete flow | Login→Browse→Add×2→Cart→Update qty→Checkout COD→Confirm→History | All intermediate |

---

### 30. Playwright E2E — Responsive & Mobile

Viewport: `375×812` (iPhone X)

| # | Test Case | Expected | Screenshot |
|---|-----------|----------|------------|
| E-MO-001 | Hamburger menu | Icon visible | `mobile--hamburger.png` |
| E-MO-002 | Menu opens | Side panel with links | `mobile--menu.png` |
| E-MO-003 | Nav links work | Navigates, closes | `mobile--nav.png` |
| E-MO-004 | Kundli form | Stacks vertically | `mobile--kundli.png` |
| E-MO-005 | Shop cards | 1-2 column grid | `mobile--shop.png` |
| E-MO-006 | AI Chat | Input bottom, scrollable | `mobile--aichat.png` |
| E-MO-007 | No horizontal scroll | No overflow | — |
| E-MO-008 | Tablet (768×1024) | 2-3 column grid | `tablet--home.png` |

---

### 31. Cross-Cutting Concerns

| # | Category | Test Case | Expected | Priority |
|---|----------|-----------|----------|----------|
| X-CO-001 | CORS | Frontend origin allowed | Requests succeed | HIGH |
| X-CO-002 | CORS | Random origin blocked | Blocked | MEDIUM |
| X-CO-003 | CORS | Preflight OPTIONS | Correct headers | HIGH |
| X-RL-001 | Rate Limit | Under 60/min | All 200 | HIGH |
| X-RL-002 | Rate Limit | Over 60/min | 429 | HIGH |
| X-RL-003 | Rate Limit | Resets after 60s | Succeed again | MEDIUM |
| X-HC-001 | Health | GET /health | 200, `{status, version}` | HIGH |
| X-HC-002 | Health | No auth | 200 | HIGH |
| X-ER-001 | Errors | Unknown route | 404 | HIGH |
| X-ER-002 | Errors | Malformed JSON | 422 | HIGH |
| X-ER-003 | Errors | Wrong method | 405 | MEDIUM |
| X-ER-004 | Errors | Format: `{detail}` | Consistent | HIGH |
| X-RF-001 | Format | Content-Type JSON | All responses | HIGH |
| X-RF-002 | Format | Dates ISO | YYYY-MM-DD | HIGH |
| X-RF-003 | Format | IDs are hex strings | 32-char | MEDIUM |

---

### 32. Performance Tests

| # | Test Case | Threshold | Priority |
|---|-----------|-----------|----------|
| P-PF-001 | Home page load | < 3s | HIGH |
| P-PF-002 | Health check | < 100ms | HIGH |
| P-PF-003 | Kundli generation | < 5s | HIGH |
| P-PF-004 | Panchang calculation | < 2s | HIGH |
| P-PF-005 | Product listing | < 500ms | HIGH |
| P-PF-006 | Cart operations | < 300ms | HIGH |
| P-PF-007 | io-gita analysis | < 3s | MEDIUM |
| P-PF-008 | AI response (mocked) | < 1s mocked, <10s real | HIGH |
| P-PF-009 | 10 concurrent users | All < 5s | MEDIUM |
| P-PF-010 | 1000 kundlis query | List < 500ms | MEDIUM |
| P-PF-011 | Frontend bundle | < 500KB gzipped | MEDIUM |

---

### 33. Security Tests

| # | Test Case | Expected | Priority |
|---|-----------|----------|----------|
| S-SE-001 | SQL injection in email | 422 or safe query | CRITICAL |
| S-SE-002 | SQL injection in kundli name | Parameterized, no injection | CRITICAL |
| S-SE-003 | SQL injection in search params | Safe | CRITICAL |
| S-SE-004 | XSS in user name | React escapes on render | HIGH |
| S-SE-005 | XSS in product description | React escapes | HIGH |
| S-SE-006 | JWT not in URL | Header only (except WS) | HIGH |
| S-SE-007 | Password not in response | No password_hash | CRITICAL |
| S-SE-008 | Password hashed in DB | Starts with `$2b$` | CRITICAL |
| S-SE-009 | Expired JWT rejected | 401 | HIGH |
| S-SE-010 | User A can't access B's data | 404 | HIGH |
| S-SE-011 | Non-admin can't access admin | 403 | HIGH |
| S-SE-012 | Non-astrologer can't accept | 403 | HIGH |
| S-SE-013 | Razorpay signature verified | 400 on invalid | HIGH |
| S-SE-014 | Stripe signature verified | 400 on invalid | HIGH |
| S-SE-015 | Rate limit prevents brute force | 429 after threshold | HIGH |
| S-SE-016 | No secrets in response | No keys/hashes | CRITICAL |
| S-SE-017 | CORS restrictive | Not `*` | HIGH |
| S-SE-018 | No directory traversal | 400/404 | HIGH |
| S-SE-019 | Large payload rejected | 413 or graceful | MEDIUM |
| S-SE-020 | JWT_SECRET not default in prod | Not dev secret | CRITICAL |

---

### 34. Data Integrity & Edge Cases

| # | Test Case | Expected | Priority |
|---|-----------|----------|----------|
| I-DI-001 | Future birth date (2050) | Accepted | MEDIUM |
| I-DI-002 | Very old date (1900) | Valid calc | MEDIUM |
| I-DI-003 | Panchang date 1800 | Graceful error | LOW |
| I-DI-004 | Product deactivated after cart add | Checkout fails gracefully | HIGH |
| I-DI-005 | Stock reduced externally | "Insufficient stock" | HIGH |
| I-DI-006 | Double submit order | Only 1 created | HIGH |
| I-DI-007 | Webhook replay | Idempotent | HIGH |
| I-DI-008 | 5 concurrent kundli generations | All created, no mixing | MEDIUM |
| I-DI-009 | Unicode in names | "मेहरबान सिंह" → stored/returned correctly | HIGH |
| I-DI-010 | Hindi in AI questions | Handled correctly | MEDIUM |
| I-DI-011 | 5000-char AI question | Accepted or truncated | MEDIUM |
| I-DI-012 | Emoji in messages | "🙏 Namaste" stored/displayed | LOW |
| I-DI-013 | Null vs empty string | Consistent | MEDIUM |
| I-DI-014 | UTC+14 timezone | Valid kundli | LOW |
| I-DI-015 | UTC-12 timezone | Valid kundli | LOW |
| I-DI-016 | Equator (lat=0) | Valid panchang | LOW |
| I-DI-017 | Date line (lon=180) | Valid panchang | LOW |
| I-DI-018 | Book consultation with self | Prevented or allowed (check rule) | MEDIUM |

---

## PART C: PRODUCTION GATES

### Pass/Fail Criteria

- **GREEN (Ship)**: All HIGH pass, >90% MEDIUM pass, no CRITICAL security fail
- **YELLOW (Fix Required)**: Any HIGH fails, or >3 MEDIUM failures
- **RED (Block Release)**: Any CRITICAL security fail, >5 HIGH failures, E2E purchase flow broken

### Production Checklist

- [x] Unit tests for all 13 engines (219 tests)
- [ ] Route tests for all 88 endpoints (missing: kundli, payments, cart, ai, orders)
- [ ] Payment webhook tests (CRITICAL)
- [ ] Chaos scenarios (12/17 missing)
- [ ] Contract tests GREEN (75 stubs → real tests)
- [ ] Performance tests (p95 < 500ms)
- [ ] Security tests (OWASP Top 10)
- [ ] E2E tests for all user flows
- [ ] Load testing (100 concurrent users)
- [ ] Failover testing (DB disconnect, API timeout)

### Production Release Gate

- [ ] Payment Integrity: 100% webhook tests pass
- [ ] Data Security: No PII leakage in AI/Chat logs
- [ ] Core Logic: All 13 engines verified
- [ ] Uptime: WebSocket resilience tested 1hr

---

## Test Summary Matrix

| Category | Tests | HIGH | MEDIUM | LOW |
|----------|-------|------|--------|-----|
| Unit: Astrology Engines | 78 | 52 | 20 | 6 |
| Unit: Auth & Security | 13 | 11 | 2 | 0 |
| API: Auth | 19 | 15 | 4 | 0 |
| API: Kundli | 23 | 19 | 4 | 0 |
| API: Horoscope | 8 | 4 | 4 | 0 |
| API: Panchang | 14 | 10 | 4 | 0 |
| API: AI | 16 | 13 | 3 | 0 |
| API: Prashnavali | 8 | 7 | 1 | 0 |
| API: Library | 16 | 12 | 4 | 0 |
| API: Numerology/Tarot/Palm | 12 | 9 | 3 | 0 |
| API: KP & Lal Kitab | 7 | 6 | 1 | 0 |
| API: Products | 11 | 8 | 3 | 0 |
| API: Cart | 15 | 13 | 2 | 0 |
| API: Orders | 15 | 13 | 2 | 0 |
| API: Payments | 16 | 14 | 2 | 0 |
| API: Consultation | 17 | 13 | 4 | 0 |
| API: WebSocket | 11 | 9 | 2 | 0 |
| API: Reports | 10 | 8 | 2 | 0 |
| API: Astrologer | 12 | 9 | 3 | 0 |
| API: Admin | 28 | 21 | 7 | 0 |
| Database | 15 | 12 | 3 | 0 |
| E2E: Navigation | 18 | 12 | 6 | 0 |
| E2E: Auth | 12 | 10 | 2 | 0 |
| E2E: Kundli | 12 | 8 | 4 | 0 |
| E2E: Horoscope | 8 | 4 | 4 | 0 |
| E2E: Panchang | 10 | 6 | 4 | 0 |
| E2E: AI Chat | 8 | 6 | 2 | 0 |
| E2E: Library | 10 | 7 | 3 | 0 |
| E2E: Shop & Commerce | 31 | 24 | 7 | 0 |
| E2E: Responsive | 8 | 4 | 4 | 0 |
| Cross-Cutting | 15 | 10 | 5 | 0 |
| Performance | 11 | 6 | 5 | 0 |
| Security | 20 | 14 | 6 | 0 |
| Data Integrity | 18 | 6 | 8 | 4 |
| **TOTAL** | **~530** | **~355** | **~145** | **~10** |

---

*Master Document | Merged from testing.md + blueprint/07_testing.md*
*Last Updated: 2026-03-26 | Verified against actual codebase*
*Total: ~530 test cases | 88 endpoints | 18 tables | 8 pages | 13 engines*
