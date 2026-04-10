# P28 AstroRattan — Complete Audit Report (2026-04-10)

## Auditors
- **Kimi** (real CLI) — Integration point audit
- **Gemini** (real CLI) — Calculation standards audit
- **Codex** (real CLI) — Code execution verification
- **Claude agents** — Architecture, Deployment, Mobile scans

---

## 1. INTEGRATION ISSUES (Kimi — real)

### CRITICAL (1)
| Tab | Issue |
|-----|-------|
| KP System | `nakshatra_lord` vs `star_lord` field mismatch + `house_significations` not in API response |

### MODERATE (7)
| Tab | Issue |
|-----|-------|
| Shadbala | `sthana_detail`/`kala_detail` sub-components ignored by frontend |
| Dosha | Gemstone recommendations calculated but never displayed |
| Varshphal | `current_mudda` vs `current_mudda_dasha` field mismatch |
| LK Varshphal | Hardcoded client-side annual calc instead of API |
| LK Planets | Static Pakka Ghar lookup, not dynamic |
| Divisional | Diamond chart shows hardcoded Aries-Pisces houses |
| Shadbala | Rahu/Ketu excluded (correct per BPHS) |

### MINOR (7)
Sandhi edge case, SAV visualization, date format, transit colors, age timeline, Yogini field names, etc.

---

## 2. DEPLOYMENT ISSUES (Claude agent)

### CRITICAL (1)
| Issue | Impact |
|-------|--------|
| ASGI lifespan never triggers on Vercel | init_db(), run_migrations(), seed_all() never execute |

### HIGH (4)
| Issue | Impact |
|-------|--------|
| Missing env vars: GEMINI_API_KEY, RESEND_API_KEY, SENTRY_DSN | AI features fail, OTP silent-fail |
| JWT_SECRET guard doesn't check VERCEL env | Random secret per cold start if removed |
| Connection pool minconn=2, maxconn=10 | 500 connections under load (Neon limit ~100) |
| Docker port mismatch: 8080 vs 8028 | docker-compose broken |

### MEDIUM (3)
Rate limiter useless on serverless, Vite proxy wrong port, static audio excluded

---

## 3. MOBILE ISSUES (Claude agent)

### CRITICAL (5)
| Component | Issue |
|-----------|-------|
| KundliGenerator.tsx:194 | 23 tabs in grid-cols-12, no scroll/wrap — UNUSABLE |
| KundliGenerator.tsx:194 | Tab touch targets ~31px (below 44px min) |
| KundliGenerator.tsx:121-189 | Header buttons overflow with long names |
| Panchang.tsx:312-361 | 4 tables with no overflow-x-auto |
| AshtakvargaTab.tsx:198 | Fixed 280x280 SVG ignores container width |

### MODERATE (13)
Tables without overflow-x-auto (VarshphalTab, SadesatiTab, DashaTab, TransitsTab), 14-column matrix compression, min-width forced scroll, grid-cols-4 without breakpoints, long text wrapping, etc.

### MINOR (10)
Font sizes at minimum, small touch targets, tight grid layouts, etc.

---

## 4. CALCULATION FIXES APPLIED (this session)

| Fix | Source | Commit |
|-----|--------|--------|
| KP Placidus cusps key | Kimi | 97eafce |
| KP ayanamsa (Krishnamurti) | Codex+Gemini | 674f7ea |
| Shadbala full BPHS rewrite | All 3 | 674f7ea |
| Dasha 240yr cycling | Codex | 674f7ea |
| True node option | Gemini | 674f7ea |
| D-10 even-sign offset | Gemini | 97eafce |
| D-30 sign mappings + ranges | Gemini+Codex | a1743a1 |
| Panchang TZ (IST) | Codex | a1743a1 |
| Panchang nakshatra index | Kimi | 97eafce |
| Panchang karana half-tithi | Codex (real) | 4e8e014 |
| Panchang tz passthrough | Codex (real) | 4e8e014 |
| Divisional 30.0° boundary | Codex (real) | 4e8e014 |
| Dasha moon normalization | Codex (real) | 4e8e014 |
| Shadbala Drik Bala off-by-one | Codex (real) | 4e8e014 |
| Amala Yoga Moon check | Codex (real) | 4e8e014 |
| Neecha Bhanga Lagna check | Codex (real) | 4e8e014 |

---

## 4b. ARCHITECTURE ISSUES (Claude agent)

### CRITICAL (3)
| Issue | File | Impact |
|-------|------|--------|
| Monthly panchang N+1: 31 sequential DB queries + calcs | panchang.py:187-231 | Extremely slow on cold cache |
| Connection pool leak: `_get_valid_conn` creates non-pool connections | database.py:260-263 | Pool permanently loses slots under DB flakiness |
| JWT_SECRET guard doesn't check VERCEL env | config.py:25-29 | Silent auth failure if env var removed |

### MODERATE (12)
| Issue | File |
|-------|------|
| 30+ dead Pydantic models in models.py | models.py |
| 3 dead React sections (Testimonials, About, CTA) | sections/*.tsx |
| 640KB wasted memory: iogita V dict never read | astro_iogita_engine.py:40 |
| Single error boundary — one crash kills entire app | App.tsx:29 |
| Pool leak in health check on cursor.execute failure | main.py:132-135 |
| Pool leak in get_current_user on DB error | auth.py:65-70 |
| OTP logged to console if RESEND_API_KEY missing | auth.py:44,551 |
| Inconsistent API shapes (profile vs login response) | auth.py:414 |
| Admin role update uses untyped `body: dict` | admin.py:108 |
| Missing date format validation on birth_date/birth_time | models.py:132 |
| KP/LalKitab routes use raw `dict` bodies | kp_lalkitab.py:17,89 |
| Unvalidated transit_date/varshphal year | kundli.py:1398,1501 |

### MINOR (13)
Dead imports (6), dead components (4), unused npm packages (3), deprecated .dict() Pydantic v2

---

## 5. PRIORITY FIX ORDER (remaining)

### P0 — Fix immediately (10 CRITICAL)
1. KundliGenerator tab bar — 23 tabs unusable on mobile
2. KundliGenerator header — buttons overflow on mobile
3. ASGI lifespan trigger — DB init/migrations never run on Vercel
4. Connection pool sizing — minconn=2 exhausts Neon under load
5. Connection pool leak — _get_valid_conn creates non-pool connections
6. Monthly panchang N+1 — 31 sequential queries, extremely slow
7. Panchang tables — 4 tables no overflow-x-auto (mobile)
8. Ashtakvarga SVG — fixed 280px, no responsive scaling
9. KP field name mismatch — nakshatra_lord vs star_lord
10. JWT_SECRET guard — doesn't detect Vercel environment

### P1 — Fix this week (HIGH + MODERATE)
11. Missing Vercel env vars (GEMINI_API_KEY, RESEND_API_KEY, SENTRY_DSN)
12. Pool leak in health check + get_current_user
13. OTP logged to console without RESEND_API_KEY
14. Shadbala sub-component display in frontend
15. Dosha gemstone recommendations display
16. Varshphal field name mismatch
17. Divisional chart hardcoded houses in frontend
18. Table overflow-x-auto (Varshphal, Sadesati, Dasha, Transits)
19. Single error boundary → per-tab boundaries
20. Dead Pydantic models cleanup (30+)

### P2 — Fix soon (MINOR)
21. Dead React components (Testimonials, About, CTA, ZodiacScene)
22. Dead imports in routes
23. Unused npm packages
24. Docker port consistency
25. Vite dev proxy port
26. iogita V dict memory waste
27. Date format validation
28. Admin untyped body
29. Deprecated .dict() → .model_dump()
30. Rate limiter for serverless
