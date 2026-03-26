# 00 — Manifest

## Project Identity
- **Name:** AstroVedic — Vedic Astrology Platform + io-gita Engine
- **Number:** Project 28
- **Mode:** CREATE
- **Complexity:** HIGH
- **Domain:** Vedic Astrology + AI + E-commerce + Spiritual Content
- **Ports:** Backend 8028 | Frontend 5198

## Blueprint Files
| File | Tag | Status |
|------|-----|--------|
| 00_manifest.md | CORE | Active |
| 01_problem_and_scope.md | CORE | Active |
| 02_architecture.md | CORE | Active |
| 03_data_contracts.md | CORE | Active |
| 05_security.md | PROJECT | Active |
| 07_testing.md | PROJECT | Active |
| 09_implementation.md | CORE | Active |
| 10_benchmarks.md | CORE | Active |

## Tech Stack
- Backend: FastAPI (Python 3.12)
- Frontend: React 18 + Tailwind CSS + Vite + shadcn/ui (Kimi template v2)
- Database: SQLite WAL (aiosqlite)
- Astrology Engine: Swiss Ephemeris (swisseph)
- io-gita Engine: numpy (D=10000, seed=42, 16 atoms)
- AI: OpenAI API (gpt-4)
- Payment: Razorpay + Stripe
- Testing: pytest + httpx + Playwright
- Deployment: Docker + Uvicorn

## Version
- Blueprint v2.0 — 2026-03-26
- v2.0 — Post-audit remediation: user management, admin product CRUD, contract alignment, security hardening
