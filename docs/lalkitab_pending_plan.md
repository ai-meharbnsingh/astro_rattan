# Lal Kitab — Pending Build Plan
**Date:** 2026-04-17  
**Status:** Active  
**Goal:** Make astrorattan.com the authoritative "Digital Guru" Lal Kitab platform — no fake data, no English-as-Hindi, all backend routes wired to real frontend, all remedies from LK sources.

---

## INVARIANTS (non-negotiable)

- **NO fake tests** — every test must hit real logic with real assertions
- **NO English inside Hindi** — `remedy_hi` must contain actual Hindi text, never a copy of `remedy_en`
- **NO hardcoded UI data** — every tab must call its API route; no static fallback arrays shown as "real" chart data
- **ALL remedies from LK sources** — `lalkitab_engine.py` must have house-based remedies (planet × house = 108 entries) sourced from the books in `docs/lalkitab_audio/laalkitaab/`
- **swisseph must be confirmed running on VPS** — never show `_engine: "fallback"` silently

---

## AUDIT FINDINGS

### A. Built But Not Bridged (backend exists, frontend ignores it)

| Route | Frontend File | Gap |
|---|---|---|
| `GET /api/lalkitab/seven-year-cycle/{id}` | `LalKitabMilestonesTab.tsx` | No card renders the cycle |
| `GET /api/lalkitab/relationship-engine/{id}` | `LalKitabAdvancedTab.tsx` | Dhoka + Achanak Chot computed, never shown |
| `GET /api/lalkitab/rin-active/{id}` | `LalKitabRinTab.tsx` | Still calls old `/rin/` route, misses activation_status |
| `GET /api/lalkitab/vastu/{id}` | `LalKitabVastuTab.tsx` | SVG renders hardcoded warnings — real API never called |
| `_debug_ayanamsa` in chart response | `LalKitabKundliTab.tsx` | Calculation chain never displayed |

### B. Fake / Hardcoded

| Location | Issue |
|---|---|
| `kp_lalkitab.py:182` | `remedy_hi = r_text` — Hindi is English |
| `LalKitabVastuTab.tsx` | Hardcoded SVG warnings unconnected to user's chart |
| `astro_engine.py` fallback | If swisseph missing on VPS, pure math runs silently |
| Career/Health/Wealth/Marriage predictions | Simple dict lookups, not real LK house-combination rules |
| `nishaniyan_master` DB table | Returns empty if unseeded — no user-visible error |
| `lal_kitab_debts` DB table | Returns empty if unseeded |
| `lk_interpretations` DB table | Returns empty if unseeded |
| `lalkitab_engine.py REMEDIES` | Planet-only, no house context — LK remedies MUST be planet×house specific |
| Old `LalKitabRemediesTrackerTab.tsx` | Duplicate tracker component — old toggle-based one still exists |

### C. Not Built At All

| Feature | Priority |
|---|---|
| 35-Year LK Dasha system | Critical — primary LK timing engine |
| Cross-waking Family narrative | High |
| Kayam Grah section in TechnicalTab | Medium |
| Calc chain display in KundliTab | Medium |
| Edition toggle (1939/41/42/52) | Low — defer |
| Vastu camera overlay | Deferred — mobile native API |

---

## EXECUTION PLAN

### WAVE 1 — Pure Backend (4 agents in parallel, no shared files)

**Agent W1-A: Remedies Engine**  
Files: `app/lalkitab_engine.py` only  
Task:
- Read all extracted LK book texts from `docs/lalkitab_audio/laalkitaab/extracted_txt/`
- Build `REMEDIES_BY_HOUSE` dict: 9 planets × 12 houses = 108 entries
- Each entry: `{en: str, hi: str, material: str, day: str, timing: str}`
- Hindi must be actual Hindi (from source books), not translated English
- Update `get_remedies()` to accept planet×house and return house-specific remedy
- Tests: `tests/test_lalkitab_remedies.py` — assert each of 108 entries has non-empty hi field, hi != en

**Agent W1-B: Translations Fix**  
Files: `app/lalkitab_translations.py` (NEW), `app/routes/kp_lalkitab.py`  
Task:
- Create `app/lalkitab_translations.py` with:
  - `PLANET_NAMES_HI: dict` (Sun→सूर्य, Moon→चंद्र, Mars→मंगल, etc.)
  - `SIGN_NAMES_HI: dict` (Aries→मेष, Taurus→वृषभ, etc.)
  - `HOUSE_NAMES_HI: dict` (1→प्रथम भाव, etc.)
  - `DIGNITY_LABELS_HI: dict`
- Replace every `planet_hi: planet` (English) in `kp_lalkitab.py` with `PLANET_NAMES_HI.get(planet, planet)`
- Fix `remedy_hi = r_text` at line 182 — must use actual Hindi remedy text
- Tests: assert `PLANET_NAMES_HI["Sun"] != "Sun"` and is valid Hindi string

**Agent W1-C: 35-Year LK Dasha Engine**  
Files: `app/lalkitab_dasha.py` (NEW), `tests/test_lalkitab_dasha.py` (NEW)  
Task:
- Build LK Dasha: fixed planet sequence Sun(6yrs)→Moon(6)→Jupiter(16)→Rahu(7)→Saturn(19)→Mercury(17)→Ketu(7)→Venus(20)→Mars(7) = 105 yr Vimshottari-equivalent adapted for LK
- Actually LK uses its own dasha: implement the LK 35-year cycle where each year has a ruling planet based on birth year number modulo cycle
- Alternative simpler LK approach: age-based planet periods matching LK milestones
- `get_lk_dasha_periods(birth_date, current_date)` → returns: current_period{planet, started, ends, years_remaining}, all_periods list
- Route `GET /api/lalkitab/dasha/{kundli_id}` added to `app/routes/kp_lalkitab.py`
- Tests: assert current_period has planet, started < current_date < ends

**Agent W1-D: DB Seeding Audit**  
Files: `app/database_seed_lalkitab.py` (NEW), `app/database.py`  
Task:
- Read `docs/lalkitab_audio/laalkitaab/extracted_txt/` books
- Build seed data for `nishaniyan_master` table: at minimum 9 planets × 12 houses = 108 nishaniyan rows with real Hindi + English text
- Audit `lal_kitab_debts` table seed — 7 types: Pitru/Matru/Stri/Dev/Bhai/Shatru/Pitamah Rin
- Create `seed_lalkitab_tables()` function that's idempotent (uses INSERT ... ON CONFLICT DO NOTHING)
- Call from `init_db()` in `database.py`
- Tests: assert after seeding, `nishaniyan_master` has >= 108 rows, `lal_kitab_debts` has >= 7 rows

---

### WAVE 2 — Frontend Bridge (3 agents in parallel, different frontend files)

**Agent W2-A: Vastu Bridge + Calc Chain**  
Files: `frontend/src/components/lalkitab/LalKitabVastuTab.tsx`, `frontend/src/components/lalkitab/LalKitabKundliTab.tsx`  
Task:
- Rewrite `LalKitabVastuTab.tsx` to call `GET /api/lalkitab/vastu/{kundliId}` 
- Display real `planet_warnings`, `priority_fixes`, `directional_map`, `vastu_score` from API
- Keep the SVG compass as visual but populate it from API `directional_map` data
- Add "Calculation Chain" card in `LalKitabKundliTab.tsx`: show `_debug_ayanamsa` value, `ayanamsa_system`, `_engine` (swisseph/fallback), tropical→sidereal chain

**Agent W2-B: Orphaned Routes Bridge**  
Files: `frontend/src/components/lalkitab/LalKitabMilestonesTab.tsx`, `frontend/src/components/lalkitab/LalKitabAdvancedTab.tsx`, `frontend/src/components/lalkitab/LalKitabRinTab.tsx`  
Task:
- `LalKitabMilestonesTab.tsx`: add "7-Year Cycle" section at bottom — calls `/api/lalkitab/seven-year-cycle/{id}`, shows active cycle card with years_into/remaining
- `LalKitabAdvancedTab.tsx`: add "Relationship Patterns" section — calls `/api/lalkitab/relationship-engine/{id}`, renders Dhoka and Achanak Chot pattern cards
- `LalKitabRinTab.tsx`: switch to `/api/lalkitab/rin-active/{id}`, add ACTIVE/LATENT badge + urgency indicator per debt

**Agent W2-C: Family Cross-Waking + Kayam Ghar**  
Files: `app/lalkitab_family.py`, `frontend/src/components/lalkitab/LalKitabFamilyTab.tsx`, `frontend/src/components/lalkitab/LalKitabTechnicalTab.tsx`  
Task:
- Extend `calculate_family_harmony()` to return `cross_waking_narrative` list: text like "Jasmine's Jupiter in H2 is waking up your Soya House 9 — expect wisdom flow from partner"
- Add cross-waking section to `LalKitabFamilyTab.tsx`
- Add "Kayam Grah (Established Planets)" section in `LalKitabTechnicalTab.tsx` — data already in advanced route response

---

### WAVE 3 — Cleanup (sequential, after Wave 1+2)

- Delete `frontend/src/components/lalkitab/LalKitabRemediesTrackerTab.tsx` (old toggle-based tracker)
- Add 35-year Dasha frontend card in Timing tab
- Verify swisseph on VPS: `docker exec <container> python3 -c "import swisseph; print(swisseph.__version__)"`

---

## TDD CHECKLIST (per agent)

```
RED:   write test that fails with current code
GREEN: implement minimum code to pass
CHECK: no test expectations changed — only source code fixed
FINAL: run full test suite, assert 0 failed
```

Tests must:
- Assert specific values (not `is not None`)
- Test Hindi field contains actual Hindi characters (check `\u0900-\u097F` range)
- Test hi != en for all bilingual fields
- Test DB seed produces correct row counts
- Test API routes return expected schema

---

## SOURCE MATERIAL

| Source | Location | Use For |
|---|---|---|
| Nishaniya hi Nishaniya | `docs/lalkitab_audio/laalkitaab/extracted_txt/Nishaniya hi Nishaniya.txt` | Nishaniyan seed data |
| Book of Nishaniya 20 | `docs/lalkitab_audio/laalkitaab/extracted_txt/Book of Nishaniya 20 (1).txt` | Signs + remedies |
| Graho Ki Nishaniya 3rd Ed | `docs/lalkitab_audio/laalkitaab/extracted_txt/ग्रहो_की_निशानिया_3rd_Edition_.txt` | Planet-house signs |
| Nazm E Jyotish 2020 | `docs/lalkitab_audio/laalkitaab/extracted_txt/Nazm E Jyotish 2020 .txt` | Remedies + rules |
| Audio transcripts | `docs/lalkitab_audio/extracted/Advance/00X*/` | Planet-specific insights (noisy — use cautiously) |

---

## SUCCESS CRITERIA

- [ ] `python3 -c "import swisseph"` succeeds on VPS container
- [ ] All 108 remedy entries (planet×house) have non-empty Hindi text where `hi != en`
- [ ] All API routes called by their frontend tabs (zero orphaned routes)
- [ ] `nishaniyan_master` has >= 108 seeded rows
- [ ] `lal_kitab_debts` has >= 7 seeded rows
- [ ] Old `LalKitabRemediesTrackerTab.tsx` deleted
- [ ] Calc chain visible in KundliTab (shows ayanamsa value + engine type)
- [ ] 35-year LK Dasha route + frontend card exists
- [ ] Test suite: 0 failed, 0 skipped
