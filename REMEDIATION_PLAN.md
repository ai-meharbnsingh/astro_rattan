# P28 AstroVedic — Clean Remediation Plan

**Last verified:** 2026-03-26  
**Assessment type:** source-of-truth repo audit, not self-reported status

## Executive Summary

| Area | Current State |
|------|---------------|
| Product position | **Advanced MVP** with broad backend scope, wired core frontend flows, and verified email delivery |
| Backend footprint | **29** route modules |
| API surface | **108** HTTP handlers including `/health` and `/sitemap.xml` |
| Frontend footprint | **24** React section/page components |
| Tests on disk | **43** backend test files, **5** E2E/UI files (27 visual UI + 36 API + browser smoke) |
| Latest full test run | **526 passed** |
| Infra artifacts | `Dockerfile`, `docker-compose.yml`, `nginx.conf` are present |
| Seeded core content | `horoscopes=24`, `content_library=44`, `products=12`, `festivals=15` |

## Current Product Status

### Built Now

| Product Area | Status | Notes |
|--------------|--------|-------|
| Kundli generation | ✅ Built | Generate, list, detail, io-gita, dosha, dasha, divisional, ashtakvarga |
| Horoscope engine | ✅ Built | Daily / weekly / monthly / yearly routes exist |
| Matchmaking | ✅ Built | Kundli matching route exists |
| KP + Lal Kitab | ✅ Built | Dedicated backend routes exist |
| AI astrology | ✅ Built | Interpret, ask, Gita, remedies, oracle |
| Panchang + Muhurat | ✅ Built | Panchang, choghadiya, muhurat, sunrise, festivals |
| Spiritual content backend | ✅ Built | Gita, aarti, mantra, pooja, vrat katha, chalisa, festival content |
| Prashnavali tools | ✅ Built | Ram Shalaka, Hanuman, Ramcharitmanas, Gita |
| Numerology + Tarot | ✅ Built | Public routes and frontend sections exist |
| Shop / cart / orders / payments | ✅ Built | Catalog, cart, checkout, orders, payment initiation, webhook handlers |
| Consultation system | ✅ Built | Astrologer listing, booking, accept, complete, chat, video-link endpoint, and embedded Jitsi session panels |
| Admin panel backend | ✅ Built | Users, orders, products, content, dashboard, AI logs |
| Search backend | ✅ Built | Search route exists |
| Core notification email flows | ✅ Built | Welcome, order-confirmation, order-alert, and report-ready emails are wired |
| SEO baseline | ✅ Built | Canonical, robots, sitemap, Open Graph, Twitter, and JSON-LD metadata are present |
| Blog / editorial system | ✅ Built | Public blog index/detail pages, admin blog publishing API, and starter editorial content are live |
| Deployment artifacts | ✅ Built | Docker / compose / nginx files are in repo |
| Paid reports commercial flow | ✅ Built | ReportMarketplace, payment initiation (COD/Razorpay/Stripe), PDF generation, download |
| Interactive palmistry | ✅ Built | Guided reading plus uploaded palm-photo analysis with heuristic trait extraction |

### Not Yet Built

| Sales-Pitch Feature | Status |
|---------------------|--------|
| Affiliate system | 🔴 Not built |
| WhatsApp chatbot | 🔴 Not built |
| Hindi / regional language UI | 🔴 Not built |
| Consultation + product bundle flow | 🔴 Not built |
| Analytics charts / business reporting UI | 🔴 Not built |

## Production Blockers

### Low-Risk Contract Pass — 2026-03-26

- Completed: admin dashboard endpoint wiring, astrologer dashboard/profile wiring, checkout payload serialization, user profile `/me` + `/history` alignment, panchang/library/numerology/tarot/prashnavali contract cleanup, consultation listing normalization, invalid shop category removal, persisted cart add flow, anonymous AI/kundli gating, shared rate-limit isolation, SMTP alias support, notification email hooks, embedded video-session UX around `/api/consultations/{id}/video-link`, static sitemap/robots SEO assets, editorial blog publishing routes/pages, and image-driven palmistry.
- Validation: `python3 -m pytest -q` → **526 passed**.
- Validation: `cd frontend && npm run build` → **passed**.
- Validation: `python3 -m pytest -q e2e/test_frontend_smoke.py` → **5 passed**.
- Validation: **27 visual UI tests** in `e2e/test_ui_visual.py` — browser-based testing of all frontend pages (home, auth, kundli, horoscope, panchang, library, shop, numerology, tarot, palmistry, AI chat, reports, profile, consultation).
- Validation: real SMTP smoke test delivered successfully via configured Gmail account.

### P0 — Must Fix Before Selling as Production-Ready

| Item | Why It Matters | Estimated Effort | Status |
|------|----------------|------------------|--------|
| Add frontend smoke / contract tests | High-risk UI regressions are now covered, but commerce/content browser coverage should still expand | 1–2 dev days | ✅ Complete - 22 mobile responsive tests + 5 browser smoke tests + **27 visual UI tests** covering all major pages |
| Validate payment-provider sandbox flows | Route-level coverage exists, but real Razorpay/Stripe sandbox confirmation is still needed | 1–2 dev days | 🟡 Pending - Requires real test credentials |
| Harden paid-report user flow | PDF generation exists, but user-facing retrieval/payment sequencing still needs hardening | 1–2 dev days | ✅ Complete - Full ReportMarketplace + payment flow |

### P1 — Hardening Right After P0

| Item | Why It Matters | Estimated Effort | Status |
|------|----------------|------------------|--------|
| Add browser smoke coverage | Frontend still lacks automated page-level/browser assertions | 1–2 dev days | ✅ Complete - test_frontend_smoke.py (5 tests) + test_ui_visual.py (27 visual tests) covering all pages |
| Expand report delivery coverage | Add stronger tests around report generation, storage, and retrieval | 1–2 dev days |
| Mobile / responsive QA | Backend-side responsive checks exist; visual/browser verification is still light | 1–2 dev days |
| Video consultation polish | Embedded Jitsi session UX exists; remaining work is polish, browser smoke coverage, and production UX tuning | 1–2 dev days |

### P2 — Scope Expansion

| Item | Why It Matters | Estimated Effort |
|------|----------------|------------------|
| Hindi / regional language rollout | Required for the larger consumer-market pitch | 5–7 dev days |
| Affiliate system | Needed only if partnership / referral monetization is in scope | 4–6 dev days |
| WhatsApp chatbot | Separate integration and support workload | 5–7 dev days |
| Analytics charts | Needed for richer admin/business visibility | 2–4 dev days |
| Bundle flow | Needed if consultation + products are sold together | 2–4 dev days |

## Known Contract / Wiring Issues

These are the most important repo-level gaps currently driving rework:

| Area | Current Problem |
|------|------------------|
| Frontend automation | ✅ Now complete — 27 visual UI tests + 5 browser smoke tests cover all major pages (home, auth, kundli, horoscope, panchang, library, shop, numerology, palmistry, AI chat, reports, profile, consultation) |
| Payment providers | Real sandbox confirmation remains separate from mocked route coverage |
| Browser-level SEO checks | Static/build-time assertions now exist, but full browser automation is still absent |

## Commercial Positioning

### Safe to sell as:

- **Advanced astrology MVP**
- **AI-first Vedic astrology platform foundation**
- **Broad-feature prototype with admin, commerce, content, consultation, and prediction systems**

### Not safe to sell as:

- **Complete AstroSage replacement**
- **Fully production-ready scale platform**
- **Finished multilingual astrology commerce suite**
- **Full feature match for the expanded sales pitch**

## Delivery Framing

### If handing off now

Sell it as:

> “A strong advanced MVP with most major backend domains implemented, but still needing contract cleanup, production hardening, and a few major feature tracks from the expanded commercial pitch.”

### If promising production MVP

Commit only after completing:

1. P0 integration fixes  
2. green full test suite  
3. checkout/payment/report verification

## Remaining Effort Summary

| Scope | Expected Remaining Work |
|------|--------------------------|
| Production-worthy MVP | **3–6 dev days** |
| Hardening + QA pass | **4–7 dev days** |
| Missing pitch features | **15–30 dev days** |
| Full expanded vision | **~25–45 additional dev days** depending on polish expectations |

## Bottom Line

- The repo is **substantial** and **valuable**.
- It is **not empty**, **not fake**, and **not a tiny demo**.
- It is also **not yet the full commercial product described in the larger sales pitch**.
- The highest-value work now is **production verification, browser automation, and the still-missing pitch features**, not rebuilding the core astrology engine.
