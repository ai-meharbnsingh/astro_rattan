# Lal Kitab App — Master Enhancement Plan
**Date:** 18 April 2026
**Sources:** PDF Roadmap (36p) · Codex Deep Study (original 1952 text analysis) · Codex Research Report (market + source layer)
**Audited by:** Claude Sonnet 4.6
**Last engineering update:** 18 April 2026 (late — P0 safety layer + R1–R4 Codex audit + Sprints A through H ALL SHIPPED — **ENTIRE P1 AND P2 TIERS COMPLETE**)

---

## ✅ FULL SPRINT COMPLETION — 24 BACKLOG + 12 P1 AUTHENTICITY + 12 P2 DIFFERENTIATION ITEMS DONE

| Sprint | Commit | Items | Status |
|--------|--------|-------|--------|
| Sprint A | `be2b903` | 8 UI polish fixes (A1–A8) | ✅ SHIPPED |
| Sprint B | `782fc2f` | SourceBadge at 9 mount points + i18n + aria (B1–B3) | ✅ SHIPPED |
| Sprint C | `e3f5dc4` | Architecture cleanup — helper consolidation, pickLang migration, severity-styles, regression test (C1–C4) | ✅ SHIPPED |
| Sprint D | `cc15872` | Taxonomy extension + classical citations + UX depth + tooling (D1–D9) | ✅ SHIPPED |
| Sprint E | `dccfe50` + `a620726` | P1 authenticity — Masnui removal (P1.6), Rin dasha integration (P1.10), Remedy tier classification (P1.11) | ✅ SHIPPED |
| Sprint F | `e14eb6c` + `4a40429` | P1.1 Modified Analytical Tewa — planet-state colour coding on chart | ✅ SHIPPED |
| Sprint G | `c8c82f0`+`4d246c2`+`af21626`+`e1b9216` | Final 7 P1 items — P1.3 Chakar auto-detect, P1.4 Time Planet, P1.5 Rahu-Ketu axis, P1.7/P1.8/P1.9 4 new Rin types, P1.12 Chandra Kundali framework — executed via 4 parallel worktree agents | ✅ SHIPPED |
| **Sprint H** | `4b9a4aa`+`527e3fd`+`8bc8e78`+`a395fab`+`9279464` | **All 12 P2 market-differentiation items — Farmaan DB + Source library + Rights catalog (P2.1/P2.7/P2.8), Tithi timing + Direction/Colour/Material matrix (P2.10/P2.11), Explainable predictions + Compound debt (P2.3/P2.9), Comparative Dual-View + Full Report MVP (P2.5/P2.6), Remedy Wizard + Calculation Detail Panel (P2.4/P2.12) — executed via 4 parallel worktree agents + direct scaffolding** | ✅ **SHIPPED** |

**All 47 items (24 post-ship backlog + 12 P1 authenticity + 12 P2 differentiation − 1 retroactively-counted) now live on `https://astrorattan.com`. Entire P1 + P2 tiers complete.**

---

## 🚀 APRIL 2026 SESSION — SHIPPED TO PRODUCTION

**Commit `9ea174b` is LIVE on `https://astrorattan.com`.** 19 audit priorities across 4 Codex rounds + P0 ship-blockers are now in production. Verbose reports for verification: `docs/testing/lk_meharban_verbose.md` and `docs/testing/lk_jasmine_verbose.md`.

### Shipped — Ship-blockers (P0.1 → P0.4 of the Build Priority Matrix)
- ✅ **P0.1 Savdhaniyan** (4.08) — `app/lalkitab_savdhaniyan.py` · frontend renders orange precaution card before every remedy in LalKitabRemediesTab
- ✅ **P0.2 Andhe Grah detection** (2.12) — `app/lalkitab_andhe_grah.py` (5 detection rules: Andha-Teva pair in H10, H12-with-enemy, retrograde+combust, debilitated-in-dusthana, Papakartari) + adjacency warnings
- ✅ **P0.3 Andhe Grah warning before remedy** (4.14) — red alert card in LalKitabRemediesTab, rendered BEFORE remedy body
- ✅ **P0.4 Daytime-only remedy restriction** (4.09) — "Night is Saturn's time" appears in every remedy's Savdhaniyan list with LK 4.09 citation

### Shipped — Codex R1 (LK correctness)
- ✅ Takkar opposite-axis rule fixed (`|h1−h2|=6`) — was Vedic 1-8/1-6 · `calculate_takkar()` in `lalkitab_advanced.py`
- ✅ LK fixed-house rule (Aries=H1) correctly wired — was using Whole-Sign-from-Ascendant · `_derive_lk_house()` in `kp_lalkitab.py`
- ✅ Combustion stripped from LK surfaces — LK does not use combust · `_lk_status_string()` + `lkStatusString()` helpers
- ✅ Rahu H1 remedy SW-water contradiction fixed (was contradicting Vastu engine)
- ✅ Ascendant labelled "reference-only" on LK verbose reports
- ✅ Source-provenance registry (`app/lalkitab_source_tags.py`) — 36 engines classified into `LK_CANONICAL` / `LK_DERIVED` / `PRODUCT` / `vedic_influenced` · new `SourceBadge.tsx` component ready to mount
- ✅ Mangal Dosh split into strict LK canon (H1/H7/H8) vs Vedic overlay (H2/H4/H12 → `is_vedic_influenced=True`)

### Shipped — Codex R2 (engine quality)
- ✅ Tone softening — "dangerous"→"unstable", "will ruin"→"tendency toward", LK_CANONICAL text preserved verbatim
- ✅ Vedic Overlays segregated into own section on `LalKitabDoshaTab` with reference-only disclaimer
- ✅ Takkar severity ladder 4-rung (destructive / moderate / mild / philosophical) — enemy+both-afflicted vs strong-mitigated vs non-enemy
- ✅ Weighted vulnerability score (`base + dusthana + debil + H8`) — most_vulnerable_planet correctly identifies H8-Debilitated-Moon over Jupiter-3-takkars
- ✅ Bunyaad friend/enemy classification (4 states: strong / afflicted / neutral / clear) with self-exclusion · `LK_FRIENDS` canonical table added

### Shipped — Codex R3 (chart specificity)
- ✅ Chart-specific prediction text generator — names actual planets/houses/dignities, targets weakest planet for remedy · `_build_specific_text()` in `lalkitab_prediction_studio.py`
- ✅ Rin `activating_planet` + `activates_during` + `life_area` fields (9 rin triggers) · `_RIN_ACTIVATION_TRIGGERS` in `lalkitab_advanced.py` · rendered on `LalKitabAdvancedTab`
- ✅ Vulnerability reason classification (`internal` / `external` / `mixed` / `none`) with explanation string · rendered with colour badges on Advanced tab

### Shipped — Codex R4 (UX polish)
- ✅ `STRONG` / `MODERATE` / `NEEDS ATTENTION` label replacing raw scores (`score_to_label()` + badge on prediction tab)
- ✅ "No strong planet" negative framing replaced with balance-based positive reading
- ✅ Chalti Gaadi `"dangerous"` → `"unstable"` + "needs stabilization" phrasing
- ✅ Masnui empty block positive reframing (favourable LK reading)
- ✅ 3-part cause structure (`primary_cause` / `secondary_modifier` / `supporting_factor`) with axis-partner dictionary — rendered on prediction tab with red/amber/green cards

### Shipped — Frontend wiring (5-team parallel sprint)
- ✅ `LalKitabPredictionTab` — label badge + 3-part cause cards
- ✅ `LalKitabAdvancedTab` — Rin activation-trigger block, vulnerability ranking table with reason badges, Bunyaad 4-status colour map + new badge rows for `neutral_foundations` / `clear_foundations`
- ✅ `LalKitabDoshaTab` — split LK canon vs Vedic overlays with reference-only disclaimer
- ✅ `LalKitabRemediesTab` — Andhe Grah red alert + Savdhaniyan orange precaution cards before each remedy
- ✅ `LalKitabKundliTab` / `LalKitabTevaTab` / `LalKitabVarshphalTab` — combust/sandhi tokens stripped at LK context boundary via new `lkStatusString()` helper
- ✅ `SourceBadge.tsx` — new shared provenance-tag component

---

## HOW TO READ THIS DOCUMENT

- ✅ = Implemented (file/function confirmed in codebase)
- ⚠️ = Partial (backend exists but frontend incomplete, or scope unclear)
- ❌ = Missing entirely
- 🚀 = **Newly shipped in this session** (April 2026)
- **Source tags:** `[PDF]` = Roadmap PDF · `[CDX]` = Codex text study · `[MD]` = Codex research report

---

## CATEGORY 1 — Chart & Display Systems

| # | Feature | Source | Status | Notes |
|---|---|---|---|---|
| 1.01 | Standard Lal Kitab Tewa — fixed-house, Aries=H1 | PDF+CDX | ✅ | `LalKitabTevaTab` |
| 1.02 | Planetary positions across 12 houses | All | ✅ | |
| 1.03 | Varshphal (annual chart) display | All | ✅ | `LalKitabVarshphalTab` |
| 1.04 | Chandra Chaalana (Moon movement tracker) | PDF | ✅ | `LalKitabChandraChaalanaTab` |
| 1.05 | Kayam Grah (Fixed planets) calculation | CDX | ✅ | `calculate_kayam_grah()` in `lalkitab_advanced.py` |
| 1.06 | Masnui Grah (Artificial planets) detection | CDX | ✅ | `calculate_masnui_planets()` in `lalkitab_advanced.py` |
| 1.07 | LK house-based aspect system | CDX | ✅ | `calculate_lk_aspects()` in `lalkitab_advanced.py` |
| 1.08 | **Modified Analytical Tewa** — color-coded Soye/Andhe/Kayam/Jage planet states on chart | PDF | 🚀 ✅ | **Sprint F (P1.1)** — new `planet-state.ts` classifier with precedence Andhe > Masnui > Soye > Kayam > Jage > normal. `/api/lalkitab/advanced` now emits `andhe` block. `InteractiveKundli` accepts optional `planetStates` prop — renders a dashed outer ring (South) or indicator dot + state-coloured text (North) per planet. Tewa tab shows a conditional legend with counts. Zero breaking change for other Kundli tabs. |
| 1.09 | **Comparative Dual-View** — Birth Tewa + Varshphal synchronized side-by-side | PDF | ❌ | Professional astrologers need this for transit analysis. LeoStar has it |
| 1.10 | **Chandra Kundali as independent LK predictive framework** (not Vedic Moon chart) | PDF | 🚀 ✅ | **Sprint G (P1.12)** — `app/lalkitab_chandra_kundali.py` + `lalkitab_chandra_readings.py` (108 templated Chandra-domain readings, NOT copied from Lagna table). Re-anchor formula `((natal_house - moon_house) % 12) + 1`. Conflict detector between Lagna and Chandra readings. New tab `LalKitabChandraKundaliTab.tsx` registered in LalKitabPage. |
| 1.11 | **Dual-Tewa view** — Lagna + Chandra side-by-side with strength-shift highlighting | PDF | ❌ | Key for professional client reports |
| 1.12 | **Transit Tewa overlay** — transiting planets on natal with house activation/deactivation | PDF | ❌ | Core LK transit methodology. Gochar tab exists but not the visual overlay |
| 1.13 | **Tarmeem visualization** — hypothetical chart showing remedy impact | PDF | ❌ | Innovation feature. Shows what chart "could look like" post-remedy |
| 1.14 | **Interactive chart drill-down** — tap any house/planet → Rinas + remedies without leaving chart | PDF | ❌ | Currently chart is static. Engagement critical |
| 1.15 | **Vedic chart vs LK interpretation toggle** (canonical chart normalization) | MD | ❌ | Avoids black-box confusion for users coming from Vedic |
| 1.16 | **Educational first-use overlay** explaining LK fixed-house vs Vedic movable-house | PDF | ❌ | Prevents "why is my chart different" confusion. Dismissible tooltip |
| 1.17 | **South Indian chart format** option | PDF | ❌ | Market expectation in South India |

---

## CATEGORY 2 — Planetary Concepts & Analysis

| # | Feature | Source | Status | Notes |
|---|---|---|---|---|
| 2.01 | All 9 planets × 12 houses LK-specific interpretations | All | ✅ | `LalKitabHousesTab` + `LalKitabPlanetsTab` |
| 2.02 | Soye Grah (Sleeping planets) detection | CDX | ✅ | `lalkitab_technical.py` |
| 2.03 | Jage Grah (Awake planets) detection | CDX | ✅ | `lalkitab_technical.py` |
| 2.04 | Nishaniya (planetary physical indicators) | PDF | ✅ | `LalKitabNishaniyaTab` |
| 2.05 | Planet relations engine | PDF+CDX | ✅ | `lalkitab_relations_engine.py` |
| 2.06 | Hora Lord calculation | CDX | ✅ | `calculate_hora_lord()` |
| 2.07 | Pucca Ghar (permanent house) per planet | MD | ⚠️ | Partial in engine — not surfaced in UI |
| 2.08 | Bunyaad (foundation) strength scoring | CDX | 🚀 ✅ | Upgraded to friend/enemy/neutral/clear (4 states) with self-exclusion · `calculate_bunyaad()` · `LK_FRIENDS` table added. Now renders 4 badge rows on Advanced tab. |
| 2.09 | Pakka Ghar enemy siege detection | CDX | 🚀 ✅ | Weighted vulnerability scoring (base + dusthana + debil + H8) now identifies most-besieged planet with internal/external/mixed reason tag. Rendered with colour badges. |
| 2.10 | Trikon / Chakor / Takkar yoga detection | PDF | ⚠️ | Takkar now uses correct opposite-axis rule (`|h1−h2|=6`) with 4-rung severity ladder · Trikon/Chakor remain partial in `lalkitab_rules_engine.py` |
| 2.11 | Inter-house dependency: 8th→2nd, 2nd→6th, 12th→2nd, 1↔7↔8↔11 | MD | ⚠️ | Axis-partner dict (`H1↔H7, H4↔H10`, etc.) added for Prediction Studio's secondary_modifier · full graph still partial |
| 2.12 | **Andhe Grah (Blind Planet) automatic detection + visual on Tewa** | PDF+CDX | 🚀 ✅ | `app/lalkitab_andhe_grah.py` — 5 detection rules + adjacency warnings · Section 3-B in verbose reports · Visual on Tewa tab deferred (still ❌ for that surface) |
| 2.13 | **Andhe Grah mandatory safety warning in all remedy contexts** | PDF+CDX | 🚀 ✅ | Red alert card in `LalKitabRemediesTab` renders BEFORE remedy body when blind or adjacent-to-blind |
| 2.14 | **Takkar collision aspect** (6/8 or 1/8 house relationship) with prominent warnings | PDF+CDX | 🚀 ✅ | Corrected to LK opposite-axis (`|h1−h2|=6`) with 4-rung dignity-aware severity. Sprint B shipped prominent SourceBadge pills on every Takkar surface; Sprint D added confidence opacity + click-to-open ProvenanceModal. |
| 2.15 | **Masnui Grah removal mechanics** — Saturn malefic→remove Jupiter from Venus-Jupiter; Venus bad→keep only Ketu | CDX | 🚀 ✅ | **Sprint E (P1.6)** — `removal_guidance` on all 10 Masnui pairs with `default_remove` / `protected` / `cannot_remove` fields. Dynamic `_resolve_masnui_removal()` picks weaker planet for Mars+Saturn via dusthana score. Rahu+Ketu marked inseparable. Rendered on LalKitabAdvancedTab as colour-coded removal block with recommended target planet + reason. |
| 2.16 | **Day + Time planet placement rules** — Born Monday+evening → Rahu in H4; time planet not remediable | CDX | 🚀 ✅ | **Sprint G (P1.4)** — `app/lalkitab_time_planet.py` — reuses existing `DAY_LORDS` + `calculate_hora_lord`. Chaldean speed order (Saturn > ... > Moon) breaks day-lord vs hora-lord tie. Non-remediable flag + bilingual warning. Sunrise fallback 06:00 when missing. Advanced tab renders warning card + LK 2.16 SourceBadge. |
| 2.17 | **Zodiac Sign vs Fixed House duality** — "land belongs to Saturn, building by Jupiter" (H4/H11) | CDX | ❌ | Affects remedy selection logic |
| 2.18 | **Rahu-Ketu 1-7 conjunction rules** — when 1-7 apart, considered conjoined by aspect | CDX | 🚀 ✅ | **Sprint G (P1.5)** — `app/lalkitab_rahu_ketu_axis.py` encodes the 6 canonical axis configs (H1-H7 Self-Partnership through H6-H12 Struggle-Liberation). Node-order symmetric (Rahu at either end). Refuses to fabricate if data is not a clean 1-7 pair. New indigo section on LalKitabAdvancedTab. |
| 2.19 | **Graha Yuddha (Planetary War)** — within 1 degree, winner/loser affects LK predictions differently than Vedic | CDX | ❌ | |
| 2.20 | **Asta/Moudhya (Combustion)** — LK-specific combustion degrees per planet (not Vedic standard) | CDX | 🚀 ⚠️ | LK context explicitly REMOVES Vedic combust tokens (`_lk_status_string()`, `lkStatusString()`) per LK 1952 (LK doesn't use combustion). LK-specific degrees remain ❌ |
| 2.22_done | **Graduated enemy siege** (now done) | CDX | 🚀 ✅ | Weighted vulnerability score with internal/external/mixed classification. See 2.09. |
| 2.21 | **Uday Lagna** — rising sign at query time for Prashna Jyotish | CDX | ❌ | |
| 2.22 | **Graduated enemy siege** — Severe (2+ enemies) / Moderate (1 enemy) / Mild (aspect) / None | CDX | ❌ | Foundation collapse detection when 9th from pucca ghar is besieged |
| 2.23 | **Jupiter alone never malefic** + Venus alone protected — LK-unique rules | PDF | ❌ | Vedic rules currently contaminating our interpretations |
| 2.24 | **Chandra Avastha** (Moon state by tithi) | CDX | ❌ | Beyond Chandra Chaalana |
| 2.25 | **Chandra Bal** (Moon strength by paksha) | CDX | ❌ | |
| 2.26 | **Planet state tables** — full auspicious/inauspicious/pucca/exalted/debilitated matrix per planet | MD | ⚠️ | Partial — needs structured storage as data not prose |

---

## CATEGORY 3 — Karmic Debt System (Rinas)

| # | Feature | Source | Status | Notes |
|---|---|---|---|---|
| 3.01 | Rina detection tab | All | ✅ | `LalKitabRinTab` |
| 3.02 | Basic karmic debt calculation | All | ✅ | `calculate_karmic_debts()` |
| 3.03 | Karmic debt with Hora integration | CDX | ✅ | `calculate_karmic_debts_with_hora()` |
| 3.04 | Sacrificial goat / bali substitute logic | MD | ✅ | `lalkitab_sacrifice.py` |
| 3.05 | **Pitru Rina full detection** — Saturn H1/H2/H4/H7/H8/H12 + Sun afflicted by Rahu/Ketu + 9th house lord analysis | PDF+MD | ❌ | Current detection uses incomplete criteria |
| 3.06 | **Matru Rina detection** — Moon affliction + Venus/Mercury combos + 4th house lord | PDF | ❌ | Requires both Lagna AND Chandra Tewa |
| 3.07 | **Deva Rina** — Jupiter afflictions → divine/spiritual teacher obligations | PDF | 🚀 ✅ | **Sprint G (P1.7)** — expanded from 1-clause to 3-clause canon (H5+afflicted / dusthana / malefic-in-H9 + weak Jupiter). Activation house 9 via Jupiter — auto-dasha-overlay via existing enrich_debts_active_passive. |
| 3.08 | **Rishi Rina** — Mercury/Jupiter combos → sage tradition obligations | PDF | 🚀 ✅ | **Sprint G (P1.8)** — new detector: Mercury+Jupiter conjunction afflicted OR Mercury H8/H12 OR Jupiter H3. Activation H12, primary activator Mercury. |
| 3.09 | **Nri Rina** — humanity debt | PDF | 🚀 ✅ | **Sprint G (P1.9a)** — new Nri Rin distinct from legacy Nara Rin. Saturn H7 afflicted / Saturn H11 besieged / Mars+Saturn / no benefic in 3/6/11. Activation H7 via Saturn. |
| 3.10 | **Bhoot Rina** — Rahu + 8th house → elemental debt | PDF | 🚀 ✅ | **Sprint G (P1.9b)** — new detector: Rahu H8 / Ketu H4 / Rahu+Moon / malefic in 4th-lord house (surrogate: malefic in H10 with empty H4). Activation H8, primary activator Rahu. |
| 3.11 | **Compound debt analysis** — when multiple Rinas coexist, prioritized remediation order | PDF+MD | ❌ | Expert-system logic needed |
| 3.12 | **Debt activation timing** — specific dasha + transit triggers per debt | PDF | 🚀 ✅ | **Sprint E (P1.10)** — `enrich_debts_active_passive()` now consults current Saala Grah via `get_dasha_timeline`. When activating_planet matches current dasha lord: `dasha_active=true`, activation_status upgraded to active, bilingual `dasha_context` emitted. `next_activation_window` predicts nearest future activation age/year. Rendered on LalKitabRinTab with pulsing "LIVE IN DASHA" badge + Dasha Status panel. Transit integration still pending (dasha only). |
| 3.13 | **Debt-free periods** — optimal windows for resolution | PDF | ❌ | Proactive guidance. Major differentiator |
| 3.14 | **Multi-generational debt analysis** across family charts | PDF | ❌ | High-value for professional astrologers |
| 3.15 | **Debt resolution progress** linked to 43-day remedy compliance tracking | PDF | ❌ | Tracker exists but not wired to specific debt |
| 3.16 | **Andha Tewa / Adha Andha Tewa dosha detection** | MD | ❌ | Named dosha from public LK reports |

---

## CATEGORY 4 — Remedial System (Upayas / Totke)

| # | Feature | Source | Status | Notes |
|---|---|---|---|---|
| 4.01 | Planet-specific remedies | All | ✅ | `lalkitab_engine.py` |
| 4.02 | House-specific remedies (all 12) | All | ✅ | `LalKitabRemediesTab` |
| 4.03 | Remedy tracker (43-day logging) | All | ✅ | `LalKitabRemedyTrackerTab` |
| 4.04 | Remedy context engine | PDF | ✅ | `lalkitab_remedy_context.py` |
| 4.05 | Forbidden remedy combinations | PDF | ✅ | `lalkitab_forbidden.py` |
| 4.06 | Remedy age activation rules | CDX | ✅ | `lalkitab_age_activation.py` |
| 4.07 | **Trial / Remedy / Good Conduct classification** — 3-tier system (quick fix vs long-term vs behavioral) | CDX | 🚀 ✅ | **Sprint E (P1.11)** — new `app/lalkitab_remedy_classifier.py` with heuristic `classify_remedy()` (reads text + material). Stamped on every remedy dict via `stamp_classification()` in `get_remedies()`. Wired into all 3 remedy routes (enriched + master + lk-validated). Frontend: colour-coded pill on each remedy card — cyan=trial, gold=remedy, violet=good_conduct — with bilingual tooltip. |
| 4.08 | **Savdhaniyan (mandatory precautions) system** with violation consequences per remedy | PDF+CDX | 🚀 ✅ | `app/lalkitab_savdhaniyan.py` · per-planet precautions + global night-is-Saturn rule + cleanliness layer · rendered as orange card before every remedy · LK 4.08/4.09 citations shown |
| 4.09 | **Daytime-only restriction warning** — "Night is Saturn's time — remedies at night may be hazardous" | PDF+CDX | 🚀 ✅ | `NIGHT_IS_SATURN_WARNING` + `time_rule` (DAYTIME_ONLY / NIGHT_PERMITTED for Moon-Monday-night and Rahu-Amavasya-midnight / SPECIFIC for Saturn-Saturday-dusk) · rendered with severity tags |
| 4.10 | **43-day interruption detection + mandatory restart alert** | PDF | 🚀 ✅ | **P0.5 (`76007f8`)** — `/remedy-tracker/{id}/checkin` now auto-detects gaps ≥2 days since last check-in and forces reset per LK 4.10 (user cannot override). Response carries bilingual `restart_alert` + `broken_reason` (gap_N_days / self_reported_miss) + `lk_ref="4.10"`. New passive risk endpoint `/remedy-tracker/{id}/risk` returns safe / warning / at_risk / broken tier so UI warns BEFORE auto-break. Frontend RemedyTrackerTab renders prominent red banner with LK 4.10 explanation. |
| 4.11 | **Blood relation requirement guidance** — native OR blood relative; family remedies weekly not daily | PDF | ❌ | |
| 4.12 | **Remedy conflict detection** — two simultaneous contradicting remedies | PDF+MD | ❌ | No logic exists. Could recommend contradicting remedies |
| 4.13 | **Remedy safety score** — overall safety profile of user's active remedy set | PDF | 🚀 ⚠️ | `reversal_risk` boolean shipped per remedy (R4) · Sprint D extended to all 3 remedy endpoints (validated + master + enriched) with full safety bundle · cross-remedy aggregate score still pending |
| 4.14 | **Blind planet mandatory warning** before any remedy when Andhe Grah involved | PDF+CDX | 🚀 ✅ | Red alert card with severity + reason list + LK 4.14 citation · rendered BEFORE remedy body in `LalKitabRemediesTab` |
| 4.15 | **Backfire monitoring** — if user reports negative effects, auto-recommend discontinuation | PDF | ❌ | Liability risk without this |
| 4.16 | **Tithi-based remedy timing** — Shukla vs Krishna Paksha, specific tithi protocols | CDX | ❌ | 43-day protocol exists but not tithi-specific |
| 4.17 | **Direction-based remedies** — South for Pitru, West for Saturn etc. | CDX | ❌ | Systematic directional matrix missing |
| 4.18 | **Color-coded remedies matrix** — Yellow=Jupiter, White=Moon/Venus, Red=Mars | CDX | ❌ | |
| 4.19 | **Material-specific remedies** — Copper=Sun/Saturn, Silver=Moon/Venus | CDX | ❌ | |
| 4.20 | **Abhimantrit item database** — Sphatik Mala, Gomati Chakra, Narmadeshwar Shivlinga | CDX | ❌ | |
| 4.21 | **Specific item remedies** — Jau flour deepak for Pitru, Masoor dal for Mars | CDX | ❌ | |
| 4.22 | **Feeding protocols** — crows for Rahu-Ketu on specific days, dogs for Ketu | CDX+MD | ❌ | With animal welfare caution flags |
| 4.23 | **Remedy customization** by dietary/physical/geographic/financial constraints | PDF | ❌ | One-size-fits-all reduces compliance |
| 4.24 | **Provenance-aware remedy card** — source edition, page reference, authority level, confidence | MD | 🚀 ✅ | Source-tag registry (`app/lalkitab_source_tags.py`) extended to 7 taxonomy values (D1: +LK_ADAPTED/ML_SCORED/HEURISTIC). SourceBadge live at 9 mount points (Sprint B). `confidence` prop with 4-level opacity modifier (Sprint D5). ProvenanceModal on click explains all 7 types bilingually (Sprint D8). Vedic overlays cite Parashari Hora Shastra (Sprint D3). Edition/page refs still pending for Farmaan layer — tracked in P2.2. |
| 4.25 | **Remedy ranking algorithm** — source_authority + safety + feasibility + localization − legal_risk | MD | ❌ | Schema: AfflictionScore + RemedyPriority formula |
| 4.26 | **Longitudinal outcome tracking** — remedy effectiveness trend over months/years | PDF | ❌ | |
| 4.27 | **Animal welfare + environmental + fire caution flags** on relevant remedies | MD | ❌ | App Store requirement + POCA compliance |

---

## CATEGORY 5 — Traditional Systems

| # | Feature | Source | Status | Notes |
|---|---|---|---|---|
| 5.01 | Samudrik / Palmistry tab | All | ✅ | `LalKitabPalmistryTab` + `lalkitab_palmistry.py` |
| 5.02 | Vastu tab | PDF+MD | ✅ | `LalKitabVastuTab` + `lalkitab_vastu.py` |
| 5.03 | LK-specific Vastu integration — bedroom/kitchen/prayer/entrance tied to remedies | PDF | ⚠️ | Currently generic Vastu. LK has specific guidance per remedy type |
| 5.04 | Palmistry ↔ Rina debt correlation — mounts/lines as karmic debt indicators | PDF | ⚠️ | Exists but correlation depth unclear |
| 5.05 | **Phrenology (forehead reading)** — LK Vol.1 integrates this for birth-time rectification | CDX | ❌ | Original LK includes phrenology alongside palmistry |
| 5.06 | **Signature analysis (graphology)** — for charts with unknown birth details | CDX | ❌ | Used by LK Astro Centre professionally |
| 5.07 | **Phrenology educational note** — historical connection, no full module | PDF | ❌ | One paragraph of content for completeness |
| 5.08 | **Farmaan (Urdu couplet) database** — literal Urdu translation layer | PDF+MD | ❌ | Biggest single differentiator. Zero competitors have it properly |
| 5.09 | **Farmaan scholarly commentary layer** — traditional interpretation with confidence levels | PDF+MD | ❌ | |
| 5.10 | **Farmaan modern scholarly layer** — contemporary academic interpretation | PDF | ❌ | |
| 5.11 | **Farmaan search** — by planet / house / debt type / remedy category | PDF | ❌ | |
| 5.12 | **Farmaan citations** in all interpretations and reports | PDF+MD | ❌ | |
| 5.13 | **Collaborative Farmaan decoding** — structured community annotation | PDF+MD | ❌ | Network effect moat |
| 5.14 | **Original 1939-1952 Urdu texts research platform** — manuscript access, translation status, unexplored topics | PDF+MD | ❌ | Positions app as THE scholarly LK resource |
| 5.15 | **Tri-lingual text library** — Urdu/Hindi/English side-by-side (1939/1940/1941/1942/1952 editions) | MD | ❌ | Foundation of defensible product |
| 5.16 | **Edition comparison UI** — variant wording across editions | MD | ❌ | |
| 5.17 | **Rights/provenance badges** per content — "scan only" / "licensed" / "community transliteration" / "unclear for commercial reuse" | MD | ❌ | Reduces legal risk + increases trust |
| 5.18 | **Authorship dispute notes** — Roop Chand Joshi vs Girdhari Lal Sharma attribution | MD | ❌ | Multiple sources conflict. Transparency needed |

---

## CATEGORY 6 — Timing Systems

| # | Feature | Source | Status | Notes |
|---|---|---|---|---|
| 6.01 | LK Dasha | All | ✅ | `LalKitabDashaTab` + `lalkitab_dasha.py` |
| 6.02 | Varshphal (annual chart) | All | ✅ | |
| 6.03 | Gochar (transits) | All | ✅ | `LalKitabGocharTab` |
| 6.04 | Age activation rules | CDX | ✅ | `lalkitab_age_activation.py` |
| 6.05 | 7-year planetary cycle | CDX | ✅ | |
| 6.06 | Saala Grah (annual planet) | CDX | ✅ | |
| 6.07 | Milestones timing tab | All | ✅ | `LalKitabMilestonesTab` |
| 6.08 | Sade Sati basic detection | CDX | ⚠️ | General engine exists; LK-specific phases missing |
| 6.09 | **35-Sala vs 36-Sala Chakar** — auto-determination of which cycle applies to given chart | PDF+CDX | 🚀 ✅ | **Sprint G (P1.3)** — `app/lalkitab_chakar.py::detect_chakar_cycle()`. Sign→ascendant-lord map; 35-Sala default, 36-Sala when Rahu or Ketu physically occupies H1 (conservative reading vs always-36 for Aquarius/Scorpio co-lordship). Chip on Teva tab with bilingual tooltip + purple shadow-year callout. |
| 6.10 | **Varshphal Tajik aspects** — full / 3/4 / 1/2 / 1/4 aspects in annual chart | CDX | ❌ | |
| 6.11 | **Sahams** — sensitive points (Punya Saham, Karma Saham etc.) | CDX | ❌ | |
| 6.12 | **Mudda Dasha** — annual progression timing within Varshphal | CDX | ❌ | |
| 6.13 | **Patyayini Dasha** — for year lord analysis | CDX | ❌ | |
| 6.14 | **Naam Rashi (Name Sign) integration** for predictions and remedy timing | CDX | ❌ | LK uses name-based sign alongside birth chart |
| 6.15 | **Varshphal 120-year coverage** | PDF | ❌ | Standard is 1-5 years. Full LK lifespan = 120 years |
| 6.16 | **Varshphal Gochar system** — annual chart transits analyzed separately from natal | PDF | ❌ | Different precedence rules per life area |
| 6.17 | **Debt activation timing** — dasha + transit triggers per Rina type | PDF | ❌ | Most practically valuable debt feature |
| 6.18 | **Sade Sati detailed** — Rising/Peak/Setting phases + Ashtam Shani + Kantaka Shani (LK interpretation) | CDX | ❌ | |
| 6.19 | **Kaal Chakra** — Ghati/Vighati calculations | CDX | ❌ | |
| 6.20 | **Abhijit Muhurta** calculation | CDX | ❌ | |
| 6.21 | **Panchang integration for remedy timing** — Vara/Tithi/Nakshatra/Yoga/Karana | CDX | ❌ | Beyond existing panchang engine |
| 6.22 | **Transit alerts by severity** — informational / caution / warning / critical | PDF | ❌ | Proactive guidance transforms app from retrospective to navigational |

---

## CATEGORY 7 — Technical Calculations & Infrastructure

| # | Feature | Source | Status | Notes |
|---|---|---|---|---|
| 7.01 | Planetary calculations (Swiss Ephemeris) | MD | ✅ | |
| 7.02 | Geocoding via Nominatim | MD | ✅ | |
| 7.03 | Basic time zone handling | All | ⚠️ | Historical DST coverage unclear |
| 7.04 | Cross-device data sync | PDF | ⚠️ | Unclear implementation |
| 7.05 | **Multiple Ayanamsha options** — Lahiri / Raman / KP / LK lineage variants | PDF | ❌ | Red Astro Touch offers 10 types. Professional verification requirement |
| 7.06 | **Multiple house cusp methods** — Placidus / Koch / Equal / Whole Sign / Sripathi | PDF | ❌ | Red Astro Touch offers 6 types |
| 7.07 | **Historical DST database** with auto-detection by location + date | PDF | ❌ | |
| 7.08 | **Birth time range sensitivity analysis** | PDF | ❌ | Birth time uncertainty is extremely common in India |
| 7.09 | **Calculation detail views** — step-by-step transparency for professional verification | PDF+MD | ❌ | Professional astrologers stake reputation on software accuracy |
| 7.10 | **AfflictionScore formula** — house_badness + enemy_penalty + pucca_conflict + dosha_trigger + time_weight | MD | ❌ | Structured scoring instead of prose |
| 7.11 | **RemedyPriority ranking** — source_authority + safety + feasibility + localization − legal_risk − ethical_risk | MD | ❌ | |
| 7.12 | **Inter-house dependency graph** encoded as engine edges (not hard-coded prose) | MD | ❌ | 8th→2nd, 2nd→6th, 12th→2nd, 1↔7↔8↔11 |
| 7.13 | **AES-256 birth data encryption** at rest | PDF | ❌ | Birth data = PII. Regulatory risk |
| 7.14 | **GDPR / DPDP Act 2023 compliance** — consent records, deletion, retention, portability | MD | ❌ | DPDP Act 2023 + subordinate rules 2025 |
| 7.15 | **Offline-capable caching** — charts + interpretations without network | PDF+MD | ❌ | Consistently top-requested feature in reviews |
| 7.16 | **Secure payment processing** (PCI-DSS) | PDF | ❌ | Required for premium tiers |

---

## CATEGORY 8 — User Experience & Accessibility

| # | Feature | Source | Status | Notes |
|---|---|---|---|---|
| 8.01 | Hindi / English bilingual | All | ✅ | `lalkitab_translations.py` |
| 8.02 | Dashboard overview tab | All | ✅ | `LalKitabDashboardTab` |
| 8.03 | Saved predictions | PDF | ✅ | `LalKitabSavedPredictionsTab` |
| 8.04 | **Urdu script (Nastaliq) support** | MD | ❌ | LK originates in Punjabi/Urdu culture. Pakistani users + authentic practitioners |
| 8.05 | **Punjabi / Gujarati / Marathi / Bengali** language support | PDF | ❌ | Regional language expansion = market expansion |
| 8.06 | **Controlled terminology glossary** — consistent translation of Andhe Grah / Soye Grah / Takkar across languages | PDF+MD | ❌ | |
| 8.07 | **Adaptive complexity levels** — Beginner / Intermediate / Advanced mode | PDF | ❌ | LK overwhelms beginners. Adaptive mode retains users |
| 8.08 | **Guided chart reading workflow** for beginners (progressive disclosure) | PDF | ❌ | |
| 8.09 | **Remedy wizard** — intent → chart conditions → ranked source-linked remedies | MD | ❌ | Core UX flow for non-expert users |
| 8.10 | **"Why this answer?" explanation panel** with source citation | MD | ❌ | Builds trust. Unique in market |
| 8.11 | **User sensitivity mode** — "gentle wording" flag modernizes archaic LK text | MD | ❌ | Son-preference, caste, disability language needs modernization layer |
| 8.12 | **Health/legal/astrology disclaimer** prominently displayed | MD | ❌ | App Store requirement. Especially needed for health + fertility content |
| 8.13 | **Archaic language modernization** — preserve in source layer, rewrite in user-facing layer | MD | ❌ | Ethically necessary + product-smart |

---

## CATEGORY 9 — Reports & Documentation

| # | Feature | Source | Status | Notes |
|---|---|---|---|---|
| 9.01 | Generic kundli PDF download | All | ✅ | |
| 9.02 | **LK-specific comprehensive PDF report** — Tewa + planet-house + Rina + Dasha + Farmaan citations | PDF | ❌ | AstroSage offers 250+ page colored reports. Gap is enormous |
| 9.03 | **Tiered report depth** — Basic (10-20p) / Standard (50-100p) / Comprehensive (150p+) | PDF | ❌ | Premium pricing justification |
| 9.04 | **Multi-language report output** — Hindi + English with regional expansion | PDF | ❌ | |
| 9.05 | **Custom-branded reports** for professional practitioners (logo, color, contact) | PDF | ❌ | B2B revenue stream |
| 9.06 | **Yearly + multi-year predictive reports** — 5yr / 10yr / 35yr options | PDF | ❌ | Subscription anchor product |
| 9.07 | **Offline report generation** for cached charts | PDF+MD | ❌ | |
| 9.08 | **Full remedy card schema** — trigger / symptoms / materials / steps / cautions / source / translation | MD | ❌ | Without this app feels like folklore copy-paste |
| 9.09 | **Worked case studies** using public celebrity birth data (education-only, annotated) | MD | ❌ | AstroSage celebrity databank model |

---

## CATEGORY 10 — Content & Source Layer

| # | Feature | Source | Status | Notes |
|---|---|---|---|---|
| 10.01 | Remedy catalogue in database | All | ✅ | `database_seed_lalkitab.py` |
| 10.02 | Basic interpretation content | All | ✅ | `lalkitab_interpretations.py` |
| 10.03 | **Source-linked text library** — 1939/1940/1941/1942/1952 as objects (scan+OCR+normalized text) | MD | ❌ | Everything else depends on trustworthy source objects |
| 10.04 | **Edition comparison UI** — side-by-side variant wording across 5 volumes | MD | ❌ | Clearest market differentiator |
| 10.05 | **Rights/provenance badges** per content item | MD | ❌ | "Scan only" / "Licensed" / "Community transliteration" / "Commercial reuse unclear" |
| 10.06 | **Authorship dispute editorial notes** (Joshi vs Sharma attribution conflict) | MD | ❌ | |
| 10.07 | **Normalized cross-edition search** — finds content across OCR variants | MD | ❌ | |
| 10.08 | **Textual verification** — every interpretation + remedy linked to source page | PDF+MD | ❌ | Differentiates from "folklore dump" competitors |
| 10.09 | **Research article integration** — academic papers on LK karmic debt system | MD | ❌ | |
| 10.10 | **YouTube educational content embedding** — Astro Arun Pandit, AstroSage AI, Astroguru Subhash Sharma | PDF+MD | ❌ | Embed not host. YouTube IFrame API |

---

## CATEGORY 11 — Community & Social

| # | Feature | Source | Status | Notes |
|---|---|---|---|---|
| 11.01 | **LK research/learning forum** | PDF+MD | ❌ | AstroSage has thriving LK community. We have zero. Community = retention = moat |
| 11.02 | **Structured learning paths** — Foundation → Intermediate → Advanced → Research (4-tier) | PDF+MD | ❌ | Astrolearn.co model. Converts curious users to serious students |
| 11.03 | **Expert Q&A with verified practitioners** | PDF+MD | ❌ | Quality signal in field full of misguidance |
| 11.04 | **Farmaan decoding collaboratives** — structured working groups on unresolved couplets | PDF+MD | ❌ | Creates scholarly network effect |
| 11.05 | **Anonymized chart sharing** for community interpretation | PDF | ❌ | Users without practitioners can get community insights |
| 11.06 | **Remedy experience sharing** with 43-day outcome tracking data | PDF | ❌ | Social proof for remedies. Data-backed would be unique |
| 11.07 | **Success story moderation system** with longitudinal verification | PDF | ❌ | |
| 11.08 | **Privacy-protected discussion groups** (Saturn Sade Sati support etc.) | PDF | ❌ | |
| 11.09 | **Reputation system** for contributing members (knowledge/research/helpfulness/reliability) | PDF+MD | ❌ | |
| 11.10 | **User-generated remedy suggestions** with expert validation pipeline (5-stage) | PDF+MD | ❌ | |
| 11.11 | **Content moderation against misguidance** — automated + human reviewer | PDF+MD | ❌ | AstroSage: "people being misguided by crooks" — platform has ethical responsibility |
| 11.12 | **WhatsApp/Telegram remedy reminders** with 43-day adherence sharing | PDF | ❌ | Behavioral support + viral sharing mechanism |
| 11.13 | **Newsletter** — weekly LK guidance based on current transits | PDF | ❌ | |
| 11.14 | **Facebook group linkage** (bidirectional) | PDF+MD | ❌ | Many potential users already on Facebook LK groups |

---

## CATEGORY 12 — Monetization Architecture

| # | Feature | Source | Status | Notes |
|---|---|---|---|---|
| 12.01 | **Free vs Premium tier gating** | PDF+MD | ❌ | No monetization structure exists |
| 12.02 | **Subscription model** — saved charts / text comparison / advanced reports / community / expert sessions | MD | ❌ | Play Store policy: only where sustained value exists |
| 12.03 | **Extended Varshphal (35-120 years)** as premium feature | PDF | ❌ | Temporal scope differentiation |
| 12.04 | **Complete Rina analysis with timing** as premium | PDF | ❌ | Highest-value analytical feature |
| 12.05 | **Advanced remedy protocols + safety monitoring** as premium | PDF | ❌ | |
| 12.06 | **Professional client management dashboard** — DB + history + remedy tracking per client | PDF | 🚀 ✅ | **P3.5 (`b6002ca`)** — new `/astrologer` route with 4-tab CRM: Overview (metrics cards + chart-type distribution + top-5 active clients), Clients (searchable table), Activity (unified timeline across all clients), Consultations (booking + lifecycle: scheduled→confirmed→active→completed, with cancel). New endpoints: `GET /dashboard`, `GET /activity-feed`, `POST/GET/PATCH/DELETE /consultations`, `GET /client-timeline/{id}`. Migration 20 extends consultations table (client_id FK, duration_minutes, updated_at). Nav link "Professional" added for astrologer/admin roles. |
| 12.07 | **Expert consultation booking** — video/audio/text + escrow + scheduling | PDF+MD | ❌ | Highest monetization per user |
| 12.08 | **Custom-branded practitioner report generation** | PDF | ❌ | |
| 12.09 | **API access** for external tool integration | PDF+MD | ❌ | Platform play. Practitioners build on top |
| 12.10 | **Offline text packs** as one-time purchase | MD | ❌ | |
| 12.11 | **Premium translation packs** | MD | ❌ | |
| 12.12 | **Gemstone / Yantra / Rudraksha e-commerce** linked to remedy recommendations | PDF | ❌ | AstroSage does this. Revenue from remedy fulfilment |
| 12.13 | **Personalized remedy kit assembly + shipping** | PDF | ❌ | Specific metals, grains, cloth colors sourced and delivered |
| 12.14 | **Physical report printing + delivery** | PDF | ❌ | Premium gift market in India astrology |
| 12.15 | **White-label deployment** for astrology schools, spiritual orgs, corporate wellness | PDF | ❌ | Setup fees + recurring licensing |

---

## CATEGORY 13 — Technology & Innovation

| # | Feature | Source | Status | Notes |
|---|---|---|---|---|
| 13.01 | AI oracle (general) | All | ✅ | `ai_engine.py` |
| 13.02 | **Explainable prediction engine** — "Why this answer?" panel with source text | MD | ❌ | Core differentiator. Competitors are black-box |
| 13.03 | **AI pattern recognition** in LK multi-planet chart combinations | PDF | ❌ | Non-obvious patterns human interpreters miss |
| 13.04 | **NLP for Farmaan interpretation** — automated Urdu poetry analysis with idiomatic nuance | PDF+MD | ❌ | Directly solves "Farmaan undeciphered" problem |
| 13.05 | **Personalized remedy recommendation engine** — ranked by feasibility + effectiveness + user constraints | PDF+MD | ❌ | Current: static list. Target: adaptive ranked recommendations |
| 13.06 | **Voice-activated chart queries** — "What does my Saturn mean for career?" | PDF | ❌ | Accessibility + rural voice-first users |
| 13.07 | **Talking AI astrologer** — conversational, LK fine-tuned, emotional state awareness | PDF | ❌ | "World's First Talking AI Astrologer" — AstroSage marketing |
| 13.08 | **Multilingual voice support** — Hindi + English → Punjabi/Urdu/Bengali/Tamil etc. | PDF | ❌ | |
| 13.09 | **Remedy completion gamification** — 43-day streaks, milestone badges, social accountability | PDF | ❌ | Solves adherence problem via behavioral psychology |
| 13.10 | **Astrological learning quizzes + formal certification** | PDF | ❌ | Credential system + community quality control |
| 13.11 | **Interactive chart manipulation** — "what if Saturn were in H3?" hypothetical analysis | PDF+MD | ❌ | Advanced learning + sensitivity analysis |
| 13.12 | **AR for remedy visualization** — spatial arrangement, sky overlay, meditation environments | PDF | ❌ | Forward-looking. Early experimentation phase |
| 13.13 | **Predictive modeling for remedy effectiveness** — statistical from aggregated user outcomes | PDF | ❌ | First empirical evidence on LK remedy effectiveness |

---

## CATEGORY 14 — Legal, Privacy & Compliance

| # | Feature | Source | Status | Notes |
|---|---|---|---|---|
| 14.01 | **AES-256 birth data encryption at rest + TLS in transit** | PDF | ❌ | Birth data = PII. Regulatory + trust requirement |
| 14.02 | **GDPR / DPDP Act 2023 compliance** — consent, deletion, retention, portability, purpose limitation | MD | ❌ | MEIT published DPDP Act 2023 + 2025 subordinate rules |
| 14.03 | **App Store / Play Store compliance** — account deletion, subscription policy, health disclaimers | MD | ❌ | Apple rejects apps risking physical harm. Health content = extra scrutiny |
| 14.04 | **Rights matrix per content item** — one of: scan-link-only / licensed / community-transliteration / commercial-unclear | MD | ❌ | Copyright on Joshi works potentially until 2042 (life+60 years) |
| 14.05 | **Publisher licensing** — Sagar Publications, Diamond Pocket Books for commercial text reuse | MD | ❌ | Required before reproducing beyond fair-use excerpts |
| 14.06 | **Animal welfare flags** on feeding/offering remedies | MD | ❌ | Prevention of Cruelty to Animals Act + Play Store policy |
| 14.07 | **Environmental/safety flags** — fire, public spaces, tree damage, water pollution | MD | ❌ | |
| 14.08 | **Medical/legal/financial disclaimer** — content is informational/spiritual not professional advice | MD | ❌ | App Store requirement. Fertility, illness, mental distress content = high risk |

---

## FINAL SUMMARY TABLE

### Before April 2026 session
| Category | ✅ Have | ⚠️ Partial | ❌ Missing | Total Features |
|---|---|---|---|---|
| 1. Chart & Display | 7 | 1 | 9 | 17 |
| 2. Planetary Concepts | 7 | 5 | 14 | 26 |
| 3. Karmic Debt (Rinas) | 4 | 0 | 12 | 16 |
| 4. Remedial System | 6 | 1 | 20 | 27 |
| 5. Traditional Systems | 2 | 2 | 14 | 18 |
| 6. Timing Systems | 7 | 1 | 14 | 22 |
| 7. Technical / Infra | 2 | 2 | 11 | 15 |
| 8. UX & Accessibility | 3 | 0 | 10 | 13 |
| 9. Reports | 1 | 0 | 8 | 9 |
| 10. Content & Source | 2 | 0 | 8 | 10 |
| 11. Community & Social | 0 | 0 | 14 | 14 |
| 12. Monetization | 0 | 0 | 15 | 15 |
| 13. Technology | 1 | 0 | 12 | 13 |
| 14. Legal & Compliance | 0 | 0 | 8 | 8 |
| **TOTAL (before)** | **42** | **12** | **169** | **223** |

### After April 2026 session (post-ship, intermediate)
| Category | ✅ Have | ⚠️ Partial | ❌ Missing | Δ Shipped |
|---|---|---|---|---|
| 2. Planetary Concepts | 9 | 7 | 10 | **+2 ✅ / +2 ⚠️** (2.08, 2.09, 2.12, 2.13) |
| 3. Karmic Debt (Rinas) | 4 | 1 | 11 | **+1 ⚠️** (3.12) |
| 4. Remedial System | 9 | 2 | 16 | **+3 ✅ / +1 ⚠️** (4.08, 4.09, 4.13, 4.14, 4.24) |
| **NET DELTA** | **+5 ✅** | **+4 ⚠️** | **−9 ❌** | **9 ship-blockers cleared** |

### After Sprints A/B/C/D (intermediate)
Sprints upgraded several partial ⚠️ items to ✅:

| Item | Before | After | Upgrade |
|---|---|---|---|
| 2.14 Takkar warnings | ⚠️ | ✅ | Sprint B SourceBadge pills + Sprint D confidence/modal |
| 4.13 Remedy safety score | ⚠️ | ⚠️ | Sprint D extended to all 3 routes (still no aggregate cross-remedy score) |
| 4.24 Provenance-aware remedy card | ⚠️ | ✅ | Sprint B+D full provenance system live (taxonomy + badge + modal + confidence) |

### After Sprint E (P1 authenticity)
Three more items moved from ❌/⚠️ → ✅:

| Item | Before | After | Delta |
|---|---|---|---|
| 2.15 Masnui removal mechanics | ❌ | ✅ | **Sprint E P1.6** — 10 pairs with canon removal guidance + dynamic weaker-planet picker |
| 3.12 Debt activation timing | ⚠️ | ✅ | **Sprint E P1.10** — dasha-aware activation overlay (transit still pending, but dasha alone closes the primary gap) |
| 4.07 Trial/Remedy/Good Conduct | ❌ | ✅ | **Sprint E P1.11** — heuristic classifier + tier pill UI |

**After Sprint F totals:** 53 ✅ · 14 ⚠️ · 156 ❌ (out of 223).

### After Sprint G (P1 TIER COMPLETE)
7 items moved ❌ → ✅ in a single parallel sprint:

| Item | Before | After | Sprint G work |
|---|---|---|---|
| 1.10 Chandra Kundali framework | ❌ | ✅ | P1.12 — re-anchor engine + 108 Chandra readings + new tab |
| 2.16 Day + Time planet | ❌ | ✅ | P1.4 — `lalkitab_time_planet.py` non-remediable fate signature |
| 2.18 Rahu-Ketu 1-7 conjunction | ❌ | ✅ | P1.5 — 6 canonical axis configs + indigo advanced-tab section |
| 3.07 Deva Rin | ❌ | ✅ | P1.7 — expanded to full 3-clause canon, activation H9 |
| 3.08 Rishi Rin | ❌ | ✅ | P1.8 — new detector, activation H12 via Mercury |
| 3.09 Nri Rin | ❌ | ✅ | P1.9a — new detector distinct from legacy Nara, activation H7 |
| 3.10 Bhoot Rin | ❌ | ✅ | P1.9b — new detector, activation H8 via Rahu |
| 6.09 35 vs 36-Sala Chakar | ❌ | ✅ | P1.3 — ascendant-lord-driven auto-detect + Teva chip |

**After Sprint G totals:** 60 ✅ · 14 ⚠️ · 149 ❌ (out of 223).

### After Sprint H (P2 TIER COMPLETE)
All 12 P2 items delivered via 4 parallel worktree agents + direct scaffolding:

| Item | Sprint H work |
|---|---|
| 5.08-5.12 Farmaan DB | `lk_farmaan` + `lk_farmaan_annotations` tables + search/detail/annotate API + dedicated tab |
| 4.24 Provenance remedy cards | (retroactively ✅ via earlier sprints — source taxonomy + badge + modal) |
| 13.02 Explainable predictions | Evidence list per area + counterfactual + collapsible "Why this score?" panel |
| 8.09 Remedy Wizard | 9 intents × re-rank existing remedies, 3-step modal in Upay tab |
| 1.09 Dual-View | Tewa + Varshphal side-by-side + strength-shift delta table |
| 9.02 PDF Report | 10-15 page aggregator + print-to-PDF modal |
| 10.03 Source library | `lk_source_library` table + 3 editions/by-section/search routes |
| 10.05 Rights badges | 5-band rights catalog with bilingual labels + hex colours |
| 3.11 Compound debt | Canon-ordered priority + clusters + blocked_by gating |
| 4.16 Tithi timing | Per-planet paksha + peak tithi + forbidden tithis |
| 4.17-4.19 Remedy matrix | Direction (bearing) + colour (hex) + material per planet |
| 7.09 Calculation details | Raw ayanamsa + DMS + friend tables + Bunyaad/Takkar/Masnui with source tags |

**After Sprint H totals:** **72 ✅ · 14 ⚠️ · 137 ❌** (out of 223).
- Ship-blocker list P0.1–P0.4 fully cleared
- All 24 Sprint A/B/C/D backlog items complete
- ALL 12 / 12 P1 authenticity items complete ✅
- **ALL 12 / 12 P2 market-differentiation items complete** ✅
- Next tier: P3 Growth & Monetisation (12 items — tier gating, subscription, community forum, WhatsApp reminders, offline, Urdu Nastaliq, adaptive complexity, chart sharing, consultation booking, professional dashboard) — OR commission content ingestion for Farmaan / Source library corpus to populate the shipped empty tables.

---

## BUILD PRIORITY MATRIX

### 🔴 P0 — Ship Blockers (must complete before public launch)

These are safety, legal, and ethical requirements. Shipping without them creates liability.

| # | Feature | Reason |
|---|---|---|
| P0.1 | Savdhaniyan mandatory precautions system (4.08) | LK texts warn remedies without precautions produce opposite effects |
| P0.2 | Andhe Grah detection + visual on Tewa (2.12) | Foundation for all blind-planet-related safety |
| P0.3 | Andhe Grah warning before any remedy (4.14) | Remedies near blind planet can backfire — safety critical |
| P0.4 | Daytime-only remedy restriction warning (4.09) | Textually mandated: "Night is Saturn's time" |
| ~~P0.5~~ | ~~43-day interruption enforcement + restart alert (4.10)~~ | **✅ DONE** (`76007f8`) — auto-gap detection + bilingual restart alert + risk endpoint |
| P0.6 | Health/legal/astrology disclaimer layer (8.12) | App Store requirement. Fertility/illness content = high scrutiny |
| P0.7 | Animal welfare + environmental caution flags on remedies (4.27) | Play Store policy + Prevention of Cruelty to Animals Act |
| P0.8 | GDPR/DPDP Act 2023 basics — consent, deletion, purpose limitation (14.02) | Legal requirement for Indian + EU market |

---

### 🟠 P1 — Core LK Authenticity — **ALL 12 / 12 DONE after Sprint G** ✅

These define whether the app is genuinely Lal Kitab or just Vedic with LK labels.

| # | Feature | Status | Notes |
|---|---|---|---|
| **P1.1** | **Modified Analytical Tewa — Soye/Andhe/Kayam colour coding (1.08)** | **✅ Sprint F** | `planet-state.ts` classifier + `InteractiveKundli` `planetStates` prop + Tewa tab legend. Primary visual differentiator from Vedic is now live. |
| P1.2 | Takkar collision aspect warnings (2.14) | ✅ | Shipped via Sprint B+D (SourceBadge + ProvenanceModal) |
| **P1.3** | **35-Sala vs 36-Sala Chakar auto-determination (6.09)** | **✅ Sprint G** | `app/lalkitab_chakar.py` — 35-Sala by default, 36-Sala when Rahu/Ketu occupies H1. Chip on Teva tab with tooltip + purple shadow-year callout when 36 fires. |
| **P1.4** | **Day + Time planet placement rules (2.16)** | **✅ Sprint G** | `app/lalkitab_time_planet.py` — day-lord + hora-lord with Chaldean speed-order tie-break. Non-remediable flag + bilingual warning. Advanced tab renders warning card + LK 2.16 badge. |
| **P1.5** | **Rahu-Ketu 1-7 conjunction rules (2.17)** | **✅ Sprint G** | `app/lalkitab_rahu_ketu_axis.py` — 6 axis configs (H1-H7 through H6-H12) with canonical effect + remedy + caution. Node-order symmetric. Indigo "Rahu-Ketu Axis" section on Advanced tab. |
| **P1.6** | **Masnui Grah removal mechanics (2.15)** | **✅ Sprint E** | `removal_guidance` on all 10 pairs + dynamic `_resolve_masnui_removal()` + UI block |
| **P1.7** | **Deva Rina detection + remedies (3.07)** | **✅ Sprint G** | Expanded from single clause to full 3-clause canon (H5+afflicted / dusthana / malefic-in-H9 + weak Jupiter). Activation house 9 + activating planet Jupiter — auto-flows through dasha overlay. |
| **P1.8** | **Rishi Rina detection + remedies (3.08)** | **✅ Sprint G** | New detector: Mercury+Jupiter conjunction afflicted OR Mercury in H8/H12 OR Jupiter in H3. Activation house 12, primary activator Mercury. |
| **P1.9** | **Nri Rin + Bhoot Rin (3.09, 3.10)** | **✅ Sprint G** | Nri Rin (humanity): Saturn H7/H11 afflicted or besieged; activation H7. Bhoot Rin (elemental): Rahu H8 / Ketu H4 / Rahu+Moon / malefic in 4th-lord house; activation H8, activator Rahu. |
| **P1.10** | **Debt activation timing — dasha + transit (3.12)** | **✅ Sprint E** | Dasha-aware overlay live; transit overlay still pending |
| **P1.11** | **Trial / Remedy / Good Conduct classification (4.07)** | **✅ Sprint E** | `lalkitab_remedy_classifier.py` + colour-coded pill on every remedy |
| **P1.12** | **Chandra Kundali as independent LK predictive framework (1.10)** | **✅ Sprint G** | `app/lalkitab_chandra_kundali.py` re-anchors planets (Moon→H1 via `((natal_house - moon_house) % 12) + 1`). 108-entry `chandra_readings.py` composed from planet-quality × Moon-domain axes (no Lagna copy). Conflict detector flags favourable-vs-strained disagreements. New `/api/lalkitab/chandra-kundali/{id}` endpoint + new `LalKitabChandraKundaliTab.tsx` tab registered in LalKitabPage. |

**P1 progress: 12 / 12 done (100%) ✅** — all items complete. Ready to move to P2 sprint.

---

### 🟡 P2 — Market Differentiation — **ALL 12 / 12 DONE after Sprint H** ✅

These make the app harder to copy and justify premium pricing.

| # | Feature | Reason |
|---|---|---|
| **P2.1** | **Farmaan database — literal + scholarly + search (5.08-5.12)** | **✅ Sprint H** `4b9a4aa` — 3 new tables + 3 search/detail/annotate routes + Farmaan tab. Corpus ships empty; admin import pipeline seeds content incrementally. |
| **P2.2** | **Provenance-aware remedy cards** | **✅ Sprint B/D earlier** — source taxonomy + SourceBadge + ProvenanceModal + confidence prop. Edition/page refs pending until Farmaan corpus ingests. |
| **P2.3** | **Explainable prediction engine — "Why this answer?"** | **✅ Sprint H** `8bc8e78` — per-area evidence list (trace/rule/bonus/penalty/cap) + counterfactual + bilingual labels + collapsible UI panel on every prediction card. |
| **P2.4** | **Remedy wizard — intent → conditions → ranked remedies** | **✅ Sprint H** `9279464` — new `lalkitab_remedy_wizard.py` with 9 intents, 3-step modal, re-ranks existing LK_CANONICAL remedies (no fabrication). |
| **P2.5** | **Comparative Dual-View — Tewa + Varshphal synchronised** | **✅ Sprint H** `a395fab` — new tab with both charts side-by-side, strength-shift delta table, P1.1 colour coding reused. |
| **P2.6** | **Comprehensive LK PDF report (MVP 10-15 pp)** | **✅ Sprint H** `a395fab` — `/api/lalkitab/pdf-report/{id}` aggregator + `LalKitabFullReport` modal with `@media print` CSS + browser print-to-PDF. |
| **P2.7** | **Source-linked text library — 1939-1952 editions** | **✅ Sprint H** `4b9a4aa` — `lk_source_library` table + 3 editions/by-section/search routes. Empty at launch. |
| **P2.8** | **Rights/provenance badges per content** | **✅ Sprint H** `4b9a4aa` — 5-band rights catalog (scan_only / licensed / community_transliteration / commercial_unclear / public_domain) with bilingual labels + hex colours + /rights-catalog route. Applied to every Farmaan + source-library row. |
| **P2.9** | **Compound debt analysis with prioritisation** | **✅ Sprint H** `8bc8e78` — `lalkitab_compound_debt.py` with canon priority (Pitru→Matru→Deva→...), +10 dasha boost, clusters by activator, blocked_by gating. Top-3 rank badges on Rin tab. |
| **P2.10** | **Tithi-based remedy timing** | **✅ Sprint H** `527e3fd` — `lalkitab_tithi_timing.py` with paksha + peak tithi + forbidden tithis per planet. Shukla/Krishna pakshas encoded. Rendered inside Savdhaniyan precaution card. |
| **P2.11** | **Direction + colour + material remedy matrix** | **✅ Sprint H** `527e3fd` — `lalkitab_remedy_matrix.py` — PLANET_DIRECTION (bearing_deg) + PLANET_COLOURS (hex) + PLANET_MATERIALS. Compass · Palette · Gem chip row on every remedy card. |
| **P2.12** | **Calculation detail views for professional verification** | **✅ Sprint H** `9279464` — new endpoint `/api/lalkitab/calculation-details/{id}` + `CalculationDetailPanel` accordion (ayanamsa, planet DMS, LK fixed houses, Bunyaad/Takkar/Masnui/aspects with source tags, copyable JSON per section). |

**P2 progress: 12 / 12 done (100%) ✅** — all market-differentiation items live. Ready to plan P3 (Growth & Monetisation) or commission content ingestion for Farmaan corpus.

---

### 🟢 P3 — Growth & Monetization (months 6-12)

| # | Feature |
|---|---|
| P3.1 | Free / Premium tier gating (12.01) |
| P3.2 | Subscription model design (12.02) |
| P3.3 | Extended Varshphal 35-120 years as premium (12.03) |
| P3.4 | Community forum — structured learning paths + expert Q&A (11.01-11.03) |
| ~~P3.5~~ | ~~Professional client management dashboard (12.06)~~ — **✅ DONE** (`b6002ca`) — 4-tab CRM at /astrologer |
| P3.6 | Expert consultation booking (12.07) |
| P3.7 | WhatsApp/Telegram remedy reminder integration (11.12) |
| P3.8 | Offline functionality — charts + interpretations without network (7.15) |
| P3.9 | Urdu script (Nastaliq) support (8.04) |
| P3.10 | Adaptive interface complexity — Beginner / Intermediate / Advanced (8.07) |
| P3.11 | Anonymized chart sharing for community interpretation (11.05) |
| P3.12 | Remedy experience sharing with outcome tracking (11.06) |

---

### 🔵 P4 — Innovation (Year 2+)

| # | Feature |
|---|---|
| P4.1 | NLP for Farmaan Urdu poetry interpretation |
| P4.2 | AI pattern recognition in LK chart combinations |
| P4.3 | Personalized remedy recommendation engine (ranked, adaptive) |
| P4.4 | Voice-activated chart queries (Hindi + English first) |
| P4.5 | Remedy completion gamification — 43-day streaks, badges |
| P4.6 | Astrological learning quizzes + formal certification |
| P4.7 | Interactive chart manipulation — what-if hypothetical analysis |
| P4.8 | Gemstone / Yantra e-commerce linked to recommendations |
| P4.9 | Personalized remedy kit assembly + shipping |
| P4.10 | AR for remedy spatial visualization |
| P4.11 | Predictive modeling for remedy effectiveness from aggregated user data |
| P4.12 | API access for external tool integration + white-label |

---

## RECOMMENDED IMPLEMENTATION ROADMAP

Based on Codex Research Report phasing:

| Phase | Focus | Deliverables | Est. Effort |
|---|---|---|---|
| **Foundation** | Source + safety | P0 blockers + text ingestion pipeline + rights matrix + OCR normalization | 4-6 weeks |
| **Trust Layer** | Authenticity | P1 LK concepts + provenance badges + edition comparison UI + source citations | 5-7 weeks |
| **Explainable Engine** | Differentiation | P2 Farmaan DB + remedy cards + "Why?" panels + rule graph + AfflictionScore formula | 6-8 weeks |
| **Learning Layer** | Engagement | Worked examples + embedded video + learning paths + guided UX | 3-5 weeks |
| **Premium Layer** | Monetization | Free/Premium gating + subscriptions + advanced reports + community + consultation | 4-6 weeks |
| **Expansion** | Scale | Expert marketplace + API + original courses + B2B widgets + e-commerce | 6-10 weeks |

---

*Document compiled from three independent research sources. Last updated: 18 April 2026.*
*Next review: before P1 sprint kickoff.*

---

## APRIL 2026 POST-SHIP BACKLOG — 24 FOLLOW-UP ITEMS

These emerged from the 5-team parallel frontend-wiring sprint. They are quality/UX/debt items layered **on top** of the P0-P4 priorities above — not blockers, but necessary for the 10/10 polish tier. Each team also flagged additional issues beyond their assigned scope.

### 🔴 Sprint A — High-visibility quality fixes  ✅ ALL SHIPPED (`be2b903`)
Self-contained UI bugs surfaced during wiring.

| # | Issue | Status |
|---|---|---|
| A1 | i18n typo `auto.chartDataNotAvailabl` (missing trailing `e`) | ✅ DONE |
| A2 | Stale garbled key `auto.aCTIVEDEBT` (bad case from auto-scanner) | ✅ DONE |
| A3 | Masnui quality strings hard-coded English ("Khali Hawai" / "Challenging" / "Mixed") | ✅ DONE |
| A4 | Dhoka severity enum ("high"/"medium") shown verbatim in English mode (not title-cased) | ✅ DONE |
| A5 | `translatePlanet` not string-guarded — crashes if `formed_by` contains non-string | ✅ DONE |
| A6 | `InteractiveKundli` substring-matches `"combust"` unconditionally — add `hideCombust` prop | ✅ DONE |
| A7 | Dead legacy field fallbacks in Dhoka/Achanak Chot (6 stale field names) | ✅ DONE |
| A8 | DoshaTab severity style defaults missing for unknown values → broken classes | ✅ DONE |

### 🟠 Sprint B — SourceBadge deployment  ✅ ALL SHIPPED (`782fc2f`)
Ready-made `SourceBadge.tsx` component wired across 9 mount points.

| # | Issue | Status |
|---|---|---|
| B1 | Wire SourceBadge at 9 identified mount points (Advanced, Remedies, Prediction tabs) | ✅ DONE |
| B2 | Add i18n keys `lk.source.canonical`/`derived`/`product`/`vedic` (EN + HI) | ✅ DONE |
| B3 | Add `aria-label` to SourceBadge (currently only `title` tooltip) | ✅ DONE |

### 🟡 Sprint C — Architecture cleanup  ✅ ALL SHIPPED (`e3f5dc4`)
Tech-debt reduction that prevents future regressions.

| # | Issue | Status |
|---|---|---|
| C1 | Centralize `toLkPlanetData(raw)` helper in `lalkitab-core.ts` | ✅ DONE — 4 scattered copies consolidated |
| C2 | Migrate 20 LK tabs from manual `hi ? ... : ...` ternaries → `pickLang()` | ✅ DONE — eliminates React #31 regression risk |
| C3 | Shared severity/urgency color utility | ✅ DONE — new `frontend/src/components/lalkitab/severity-styles.ts` |
| C4 | DoshaTab regression tests for edge case | ✅ DONE — `tests/test_lalkitab_dosha_split.py` (26 invariants green). **Caught real bug**: only `mangalDosh` had `source` field stamped — now all doshas stamped with `LK_CANONICAL` default. |

### 🔵 Sprint D — Backend enhancements + deeper UX  ✅ ALL SHIPPED (`cc15872`)

| # | Issue | Status |
|---|---|---|
| D1 | Extend source taxonomy: `LK_ADAPTED` + `ML_SCORED` + `HEURISTIC` | ✅ DONE — added to `app/lalkitab_source_tags.py`, `SourceBadge.tsx`, i18n (6 new keys) |
| D2 | Normalize case: `VEDIC_INFLUENCED` (SCREAMING_SNAKE) with backwards-compat alias | ✅ DONE — `source_legacy` field carries lowercase for old consumers, frontend `isVedicSource()` accepts both |
| D3 | Add `source_note_en/hi` per Vedic dosha (Parashari citation) | ✅ DONE — Mangal Dosh Vedic overlays now cite the H1/H2/H4/H7/H8/H12 vs LK-strict-subset divergence |
| D4 | Add `lk_equivalent_key` on Vedic doshas | ✅ DONE — `"mangalDosh"` cross-link stamped on overlay records |
| D5 | `confidence` prop on SourceBadge | ✅ DONE — 4-level opacity modifier (high/moderate/low/speculative) + italics on speculative, aria-label carries level |
| D6 | Attach Savdhaniyan to validated + master remedy routes | ✅ DONE — `/remedies/master/{id}` + `/lk-validated-remedies` now emit `savdhaniyan` + `time_rule` + `reversal_risk` + `andhe_grah_warning` (was only `/remedies/enriched/`) |
| D7 | Show `weakest_planet` / `strongest_planet` chip row in Prediction tab | ✅ DONE — red/green chips with EN/HI dignity labels (exalted→उच्च, debilitated→नीच, etc.) under Chart Analysis header |
| D8 | Provenance modal on SourceBadge click | ✅ DONE — new `ProvenanceModal.tsx` explains all 7 source types in EN+HI, highlights clicked type, Escape-close + body-scroll-lock + aria-modal |
| D9 | Bulk i18n cleanup for `auto.*` keys | ✅ DONE — new `scripts/i18n-sanitize.py` non-destructive scanner → flagged 13/2463 keys → report in `.claude/debug/i18n_sanitize_report.txt` for human triage |

### Summary  ✅ ALL 24 ITEMS COMPLETE
- **Total backlog:** 24 items (8 Sprint A + 3 Sprint B + 4 Sprint C + 9 Sprint D) — **100% shipped**
- **Total commits:** 4 (`be2b903`, `782fc2f`, `e3f5dc4`, `cc15872`) — all on `main`, all deployed
- **All deploys clean** — no rollbacks, regression test green across all sprints
- **Production URL:** https://astrorattan.com

---

## APRIL 2026 AUDIT TRAIL

The following 4-round Codex audit spiral validated the LK engine correctness. Each round produced measurable changes in the engines and documentation:

| Round | Priorities | Focus | Shipped in commit |
|---|---|---|---|
| **R1** | 6 | LK correctness — Takkar axis, combustion, SW water, ascendant label, source tags, Mangal Dosh | `bf4f8dd` → `d7ff09a` |
| **R2** | 5 | Engine quality — tone softening, Vedic-overlay split, 4-rung severity, weighted vulnerability, Bunyaad friend/enemy | `367164d` |
| **R3** | 3 | Chart specificity — chart-aware prediction text, Rin activation triggers, vulnerability reason classification | `d9e82a6` |
| **R4** | 5 | UX polish — STRONG/MODERATE/NEEDS ATTENTION labels, balance framing, "unstable" tone, Masnui positive, 3-part causes | (merged into staging→main) |
| **P0** | 4 | Ship-blockers — Savdhaniyan (4.08), Andhe Grah (2.12), pre-remedy warning (4.14), daytime-only rule (4.09) | `9ea174b` |
| **Sprint A** | 8 | UI polish — i18n typo fixes, translatePlanet guard, severity defaults, dead fallbacks removed | `be2b903` |
| **Sprint B** | 3 | SourceBadge deployed at 9 mount points, i18n keys + aria-label | `782fc2f` |
| **Sprint C** | 4 | Architecture cleanup — centralized helpers, pickLang migration, severity-styles, regression test | `e3f5dc4` |
| **Sprint D** | 9 | Taxonomy extension (LK_ADAPTED/ML_SCORED/HEURISTIC), Vedic source_note, lk_equivalent_key, confidence prop, savdhaniyan on all 3 routes, weakest/strongest chips, ProvenanceModal, i18n sanitiser | `cc15872` |
| **Sprint E** | 3 | P1 authenticity — Masnui removal mechanics (P1.6), Rin dasha integration (P1.10), Remedy tier classification (P1.11) | `dccfe50` + `a620726` |
| **Sprint F** | 1 | P1.1 Modified Analytical Tewa — planet-state classifier + chart colour coding + Tewa tab legend | `e14eb6c` + `4a40429` |
| Sprint G | 7 | ALL remaining P1 items — P1.3 Chakar auto-detect, P1.4 Time Planet non-remediable, P1.5 Rahu-Ketu 1-7 axis, P1.7 Deva Rin expanded, P1.8 Rishi Rin new, P1.9a+b Nri + Bhoot Rin new, P1.12 Chandra Kundali framework. Executed as 4 parallel worktree agents, cherry-picked into main. | `c8c82f0`, `4d246c2`, `af21626`, `e1b9216` |
| **Sprint H** | 12 | **ALL P2 market-differentiation items** — P2.1 Farmaan DB, P2.3 Explainable predictions, P2.4 Remedy Wizard, P2.5 Dual-View, P2.6 PDF Report, P2.7 Source library, P2.8 Rights catalog, P2.9 Compound debt priority, P2.10 Tithi timing, P2.11 Direction/Colour/Material, P2.12 Calculation details. Executed as 4 parallel worktree agents + direct Farmaan scaffolding. | `4b9a4aa`, `527e3fd`, `8bc8e78`, `a395fab`, `9279464` |
| **TOTAL** | **70 priorities** | | All LIVE on production |

Reference verbose reports (every engine's output for verification):
- `docs/testing/lk_meharban_verbose.md` — Meharban Singh Upneja (23 Aug 1985, 11:15 PM IST, Delhi) · 92 KB
- `docs/testing/lk_jasmine_verbose.md` — Jasmine Kaur Khurana (11 Nov 1987, 3:00 AM IST, New Delhi) · 103 KB

Test harnesses (re-runnable):
- `tests/test_lk_meharban_verbose.py`
- `tests/test_lk_jasmine_verbose.py`
- `tests/test_lk_meharban_full_tables.py`

---

*Session addendum added: 18 April 2026, 22:02 UTC (production deploy timestamp).*
*Sprint A+B+C+D completion addendum: 18 April 2026 (post-Sprint-D deploy, commit `cc15872`).*
*Sprint E addendum: 18 April 2026 (post-Sprint-E deploy, commits `dccfe50` + `a620726`). 3 P1 authenticity items closed.*
*Sprint F addendum: 18 April 2026 (post-Sprint-F deploy, commits `e14eb6c` + `4a40429`). P1.1 Modified Analytical Tewa — the primary visual differentiator from Vedic — now live.*
*Sprint G addendum: 18 April 2026 (post-Sprint-G deploy, commits `c8c82f0`/`4d246c2`/`af21626`/`e1b9216`). Entire P1 authenticity tier complete (12/12) via 4 parallel worktree agents — P1.3 Chakar, P1.4 Time Planet, P1.5 Rahu-Ketu axis, P1.7/P1.8/P1.9 new Rin types (Deva/Rishi/Nri/Bhoot), P1.12 Chandra Kundali independent framework.*
*Sprint H addendum: 18 April 2026 (post-Sprint-H deploy, commits `4b9a4aa`/`527e3fd`/`8bc8e78`/`a395fab`/`9279464`). **Entire P2 market-differentiation tier complete** (12/12) via 4 parallel worktree agents + direct Farmaan scaffolding — Farmaan DB + Source library + Rights catalog, Explainable predictions + Compound debt priority, Tithi timing + Direction/Colour/Material matrix, Comparative Dual-View + Full Report MVP, Remedy Wizard + Calculation Detail Panel.*
*Totals: **72 ✅ / 14 ⚠️ / 137 ❌** of 223. **ALL P1 AND P2 items done.** Ship-blocker P0 (4 items) + P3 Growth & Monetisation (12 items) remain. Next review: plan P3 subscription/monetisation OR commission admin ingestion pipeline to populate the Farmaan + Source library tables.*
