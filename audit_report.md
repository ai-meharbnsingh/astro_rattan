# AstroRattan Technical Audit Report
**Date:** April 12, 2026
**Status:** Completed

## 1. Executive Summary
AstroRattan is a production-grade Vedic Astrology platform built on a modern stack (FastAPI, React, PostgreSQL). The core strength lies in its modular calculation engines and precise astronomical wrappers. However, the internationalization (i18n) strategy and certain middleware patterns present scalability and maintenance risks.

---

## 2. Architectural Analysis

### 2.1 Backend (FastAPI)
- **Engine Modularity:** Calculation logic is excellently decoupled into domain-specific engines (`panchang_engine.py`, `dasha_engine.py`, `lalkitab_engine.py`).
- **Precision:** Uses `swisseph` (Swiss Ephemeris) for high-accuracy calculations with a custom pure-math fallback system if the library is missing.
- **Database Layer:** Uses `psycopg2.pool.ThreadedConnectionPool`.
    - **Risk:** The `PgConnection` wrapper in `database.py` recreates the entire pool on a single connection failure. This could cause "connection stampedes" during transient network issues.

### 2.2 Frontend (React + Vite)
- **Component Design:** Rich, state-of-the-art UI utilizing modern patterns like glassmorphism and smooth transitions.
- **State Management:** Functional hooks-based data fetching.

---

## 3. Security & Authentication

- **Hashing:** Correctly uses `bcrypt` via `passlib`.
- **JWT Implementation:** Features a robust two-token system (Access + Refresh) with `token_version` tracking for immediate revocation.
- **Role-Based Access (RBAC):** Clean implementation via FastAPI dependencies.
- **Risk:** `app/auth.py` hits the database on *every* request to check `token_version`. This introduces significant latency (~10-50ms per request) and database overhead.

---

## 4. Internationalization (i18n) Audit

- **The "Brute-Force" Translation Problem:** 
    - Engines return hardcoded English strings (e.g., `"Ashwini"`, `"Gajakesari Yoga"`).
    - The frontend (`src/lib/backend-translations.ts`) maintainers a massive mapping of English phrases to Hindi.
- **Critical Risk:** This approach is extremely brittle. A single typo change in the backend (e.g., `"Gajakesari Yoga"` -> `"Gaj Kesari Yoga"`) will cause the Hindi translation to fail silently for that entry.
- **Recommendation:** Move to a Key/ID based system (e.g., `YOGA_GAJAKESARI`) where both languages map to a stable identifier.

---

## 5. Performance Bottlenecks

1. **Auth Latency:** As mentioned, per-request DB checks for user state.
2. **Background Seeding:** `app/main.py` starts background threads for heavy AI seeding on every startup. This should be monitored for memory usage on Hostinger VPS.
3. **Database Pooling:** The `maxconn=30` limit in `database.py` may be too low for high-traffic peaks given the platform's complexity.

---

## 6. Recommendations

| Priority | Issue | Recommended Action |
| :--- | :--- | :--- |
| **High** | Brittle i18n | Implement a localization key system or move translations to the backend. |
| **High** | Auth Middleware | Cache `token_version` in Redis or check only for critical operations. |
| **Medium** | Pool Re-init | Refactor `PgConnection` to replace individual dead connections rather than the whole pool. |
| **Medium** | Background Tasks | Move heavy seeding/AI generation to a proper worker queue (e.g., Celery or Vercel Cron). |

---

**Auditor:** Antigravity (Google DeepMind)
