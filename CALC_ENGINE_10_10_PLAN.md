# Calculation Engine 10/10 Plan
**Target**: Every engine returns genuinely personalized, chart-derived results.
**Current avg**: 7.1/10 → 8.8/10 (updated Apr 19, 2026) | **Target**: 9.5/10

## Session Apr 19 2026 — Completed
- ✅ Numerology: Personal Year Number (1-9) with bilingual predictions for current + next year
- ✅ Dasha: `dasha_strength_score` (0-100) in `analyze_mahadasha_phala` — exalted/own/debilitated/combust/house
- ✅ Dasha: `transit_correlation` in `get_current_dasha_phala` — flags when MD lord within 15° of natal position
- ✅ Dasha: fixed `factors` returning short keys (e.g. `["exalted","kendra"]`) + verbose text in `factors_detail`
- ✅ Transit: Saturn Return + Guru-Chandal detection in 30-day forecast + natal planet hit detection
- ✅ Panchang: Chandrashtama detection via `natal_moon_sign` query param → `chandrashtama.{active, house_from_natal, note}`
- ✅ Vastu: Compound warnings (Saturn+Rahu, Saturn+Ketu, Mars+Rahu, Jupiter+Rahu, Sun+Saturn) + `remedy_priority_score`

---

---

## 1. AI / Horoscope — 3/10 → 9/10 (HIGHEST IMPACT)

**Gap**: Gemini key exists but is NEVER called. All interpretations are random template pools.

**Fix**:
- Wire `GEMINI_API_KEY` in `app/routes/ai.py` → call `genai.GenerativeModel("gemini-2.0-flash")`
- Pass actual chart context (ascendant, planet positions, current dasha, transits) in the prompt
- Cache response in DB (ai_interpretations table, keyed by kundli_id + period)
- Fallback to templates only if Gemini fails

**Files**: `app/routes/ai.py`, `app/horoscope_generator.py`
**Effort**: 1 day

---

## 2. Horoscope personalization — 6/10 → 8/10

**Gap**: Same-sign users get identical horoscopes. Template pool is per-sign, not per-chart.

**Fix**:
- Compute Janma Lagna, Moon sign, current Mahadasha planet from chart
- Use these three to select/weight template segments (e.g., Saturn dasha = career/discipline themes)
- Add `active_yoga` detection (Raj Yoga, Kemadruma, Gajakesari) and inject into horoscope
- This works even WITHOUT Gemini; makes predictions chart-specific

**Files**: `app/horoscope_generator.py`, `app/transit_engine.py`
**Effort**: 4 hours

---

## 3. Numerology — 7/10 → 9/10

**Gap**: Life path math is correct; predictions are static text by number.

**Fix**:
- Add Lo Shu Grid (3×3 grid from DOB digits) — shows missing numbers, dominant numbers
- Add `Personal Year Number` = (Life Path + current year digit sum) — changes annually
- Integrate with Kundli: if Jupiter is strong in chart AND Life Path = 3, amplify education prediction
- Add Name Correction Suggestions (flag names where Chaldean name number conflicts with Life Path)

**Files**: `app/numerology_engine.py`, `app/routes/numerology.py`
**Effort**: 6 hours

---

## 4. Lal Kitab — 8/10 → 9.5/10 ✅ IN PROGRESS

**Done this session**:
- ✅ Prashna number from real sidereal ASC (not timestamp % 249)
- ✅ Rin (karmic debts) uses full LK canonical trigger engine (not simplified 6/8/12)
- ✅ All 4 prediction routes (marriage/career/health/wealth) + dasha overlay + Pakka Ghar
- ✅ Chandra 43-day tasks personalized by Moon house (12 houses × 8 milestone days)
- ✅ Farmaan corpus seeded (108 entries)

**Remaining**:
- [ ] `advanced` route: fallback to simplified karmic debts when location missing (currently skips silently)
- [ ] `full` endpoint: surface section-level success/fail in a structured `_diagnostics` block (done) — verify all 8 sections complete for standard charts
- [ ] Varshapravesh (Solar Return) backend endpoint — advertised in frontend, missing

**Files**: `app/routes/kp_lalkitab.py`
**Effort**: 3 hours

---

## 5. KP System — 7/10 → 9/10

**Gap**: Horary prediction uses canned interpretations. Significator strength not fully modelled.

**Fix**:
- Rewrite `get_horary_prediction()` to do 4-level significator analysis:
  - Level 1: Planet in house (occupant)
  - Level 2: Lord of occupied sign
  - Level 3: Nakshatra lord of planet
  - Level 4: Sub-lord of nakshatra
- Verdict = "favorable" only if sub-lord of relevant cusp is a significator of that cusp
- Add timing via dasha/antardasha of significators

**Files**: `app/kp_engine.py`
**Effort**: 1 day

---

## 6. Dasha Engine — 8/10 → 9.5/10

**Gap**: Sub-dasha timing is accurate; phala (effects) are template pools.

**Fix**:
- Compute Dasha Phala from actual chart: if Mahadasha lord is in its own sign/exaltation = positive phala
- Add Dasha-Transit correlation: flag when Mahadasha lord transits over natal position (intensification)
- Add Narayan Dasha (sign-based, rarer but complete) alongside Vimshottari
- Add `dasha_strength_score` (0-100) based on: lordship dignity + natal house + transit support

**Files**: `app/dasha_engine.py`, `app/routes/kundli.py`
**Effort**: 6 hours

---

## 7. Panchang — 8/10 → 9.5/10

**Gap**: Ekadashi Parana DST edge case. No Chandrodaya (moonrise) time. Chandrashtama not computed.

**Fix**:
- Add `chandrodaya` (moonrise) and `chandrast` (moonset) times to panchang output
- Add `chandrashtama` flag: Moon transiting 8th from natal Moon = caution day
- Fix Ekadashi Parana: ensure end-time handles DST transitions using `pytz` aware datetimes
- Add `abhijit_muhurat_today` as a computed field on every panchang response

**Files**: `app/panchang_engine.py`, `app/routes/panchang.py`
**Effort**: 4 hours

---

## 8. Vastu — 6/10 → 8/10

**Gap**: Hardcoded planet→direction matrix. No multi-planet compound warnings. No floor plan input.

**Fix**:
- Add compound warnings: e.g., Saturn + Rahu in same house → double affliction in that direction
- Add `remedy_priority_score` for each direction (higher = more urgent)
- Add optional `structure_type` input (flat/house/office) that modifies which planets are checked
- Add Vastu Purusha Mandala overlay (16-zone extended map beyond just 12 LK houses)

**Files**: `app/lalkitab_vastu.py`
**Effort**: 4 hours

---

## 9. Transit/Gochar — 7/10 → 9/10

**Gap**: Shows current positions only. No forward forecasting. No natal-transit hit detection.

**Fix**:
- Add `next_30_days` transit forecast: compute planet positions for each day, flag when a planet
  crosses a natal planet's house (exact transit hit)
- Add `saturn_return` detection: when transit Saturn approaches natal Saturn house = life checkpoint
- Add `guru_chandal` detection in real-time transits (Jupiter + Rahu/Ketu in same LK house)
- Add transit strength score per planet (dignified transits score higher)

**Files**: `app/transit_engine.py`, `app/routes/kp_lalkitab.py`
**Effort**: 6 hours

---

## 10. Kundli / Shadbala — 8/10 → 9.5/10

**Gap**: Shadbala uses simplified dignity rules. Vimshopak Bala does 16 vargas but not weighted fully.

**Fix**:
- Complete Shadbala: add Chesta Bala (for retrograde planets), Naisargika Bala (natural strength),
  Drig Bala (aspect strength from all 9 planets)
- Complete Vimshopak: apply classical weights per varga (D1=3, D2=1.5, D3=1.5, D9=4.5 etc.)
- Add `yoga_detection`: scan for 30 major yogas (Raj, Dhana, Kesari, Hamsa, Malavya etc.)
  and include in chart output
- Add `ashtakavarga` basic computation for bindus per planet per sign

**Files**: `app/shadbala_engine.py`, `app/varga_grading_engine.py`, `app/astro_engine.py`
**Effort**: 1.5 days

---

## Priority Order

| Priority | Feature | Impact | Effort |
|---|---|---|---|
| 1 | Wire Gemini AI | 3→9/10 | 1 day |
| 2 | LK remaining gaps | 8→9.5/10 | 3 hours |
| 3 | Horoscope chart-personalization | 6→8/10 | 4 hours |
| 4 | Dasha phala from chart | 8→9.5/10 | 6 hours |
| 5 | Transit forecasting | 7→9/10 | 6 hours |
| 6 | Numerology Lo Shu + Personal Year | 7→9/10 | 6 hours |
| 7 | KP Significator depth | 7→9/10 | 1 day |
| 8 | Panchang Chandrodaya + Chandrashtama | 8→9.5/10 | 4 hours |
| 9 | Vastu compound warnings | 6→8/10 | 4 hours |
| 10 | Shadbala + Yoga Detection | 8→9.5/10 | 1.5 days |

**Total effort to reach 9.5/10 avg**: ~7 days of focused work.
**Biggest single move**: Wire Gemini (Priority 1) — takes avg from 7.1 → 8.2 overnight.
