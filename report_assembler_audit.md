# Kundli PDF Report Assembler — Audit (Wiring + False “Missing” Fixes)

Generated: 2026-04-21

## What I audited (evidence-first)

- PDF assembler / renderer: `app/reports/kundli_report.py`
- CLI orchestration: `generate_complete_kundli_report.py`
- API full report payload builder: `app/routes/kundli.py` (`GET /api/kundli/{id}/full-report`)
- Existing interpretation stores:
  - Transit fragments: `app/transit_interpretations.py`
  - Lucky metadata: `app/transit_lucky.py`
  - Dasha phala: `app/dasha_engine.py` + `app/data/dasha_phala.json`
  - Remedies + Narad Puran tradition mapping: `app/remedy_sources.py`, `app/remedy_engine.py`
- Existing classical modifiers for transits:
  - Vedha/Latta: `app/gochara_vedha_engine.py` + `app/data/gochara_vedhas.json`, `app/data/latta_table.json`

## False “MISSING / NOT IMPLEMENTED” labels found

These sections were previously printed with:
`SECTION STATUS: NOT IMPLEMENTED | BACKEND STATUS: MISSING`
even though engines / sources exist in the repo.

- Dasha Effects (Dasha Phala)
  - Engine exists: `app.dasha_engine.get_current_dasha_phala`
  - Fix: wired `dasha_phala` into payload (API + CLI) and rendered in PDF.
- Current Transits + Gochar
  - Engine exists: `app.transit_engine.calculate_transits`
  - Fix: wired `transit` into full-report payload; PDF now renders proper fields (`current_sign`, `sign_degree`, `natal_house_from_moon`, etc.).
- Gochara Vedha
  - Engine/data exists: `app.gochara_vedha_engine.enrich_transits` + JSON tables
  - Fix: PDF now renders Vedha/Latta fields from enriched transit payload (already integrated into `calculate_transits`).
- Transit Interpretations
  - Data exists: `app.transit_interpretations.TRANSIT_FRAGMENTS`
  - Fix: wired `transit_interpretations` into payload and PDF; also added on-the-fly fallback computation in renderer.
- Lucky Indicators (Transit Lucky)
  - Engine exists: `app.transit_lucky.get_all_lucky_metadata`
  - Fix: wired `transit_lucky` into payload and rendered in PDF (with fallback computation if missing).
- Remedies reference structure (Narad Puran)
  - Data exists: `app.remedy_sources.py` includes `source_type`, `source_label`, `scriptural_reference`
  - Fix: PDF remedies section now renders structured remedies using `app.remedy_engine.generate_astrological_remedies` and preserves Narad Puran mapping labels without fabricating verse numbers.
- Varshphal
  - Engine exists: `app.varshphal_engine.calculate_varshphal`
  - Fix: wired `varshphal` into full-report payload so PDF no longer prints it as missing when the engine can run.

## What was wired (payload + renderer)

### API full-report payload (`app/routes/kundli.py`)

Added to `kundli_data` before calling `build_full_report(...)`:

- `transit`, `transit_interpretations`, `transit_lucky`
- `dasha_phala`
- `varshphal`
- `aspects`, `conjunctions`
- `yogini_dasha`, `kalachakra`
- `ashtottari_dasha`, `tara_dasha`, `moola_dasha` (fixed Moola signature)
- `remedies` (with birth_date/time injected into chart payload for better Shadbala-driven triggers)
- `jaimini`
- Specialized engines wired into the full-report payload (previously omitted):
  - `nadi` (`app/nadi_engine.py:calculate_nadi_insights`)
  - `roga` (`app/roga_engine.py:analyze_diseases`)
  - `vritti` (`app/vritti_engine.py:analyze_vritti`)
  - `apatya` (`app/apatya_engine.py:analyze_apatya`)
  - `longevity` (`app/ayurdaya_engine.py:calculate_lifespan`)
  - `lal_kitab` (`app/lalkitab_engine.py:get_remedies`)
  - `sade_sati` (`app/lifelong_sade_sati.py:calculate_lifelong_sade_sati`)

### CLI orchestration (`generate_complete_kundli_report.py`)

Fixed multiple signature/shape mismatches that were causing silent “missing”:

- Vimshottari: now calls `calculate_extended_dasha(moon_nakshatra, birth_date, moon_longitude=...)`
- Dasha Phala: now calls `get_current_dasha_phala(chart_data, birth_date, as_of_date, ...)`
- Shadbala: now uses correct `calculate_shadbala(**params)` shape + correct Bhava Bala call
- Ashtakavarga: now calls `calculate_ashtakvarga(planet_signs_map)`
- Varshphal: now calls `calculate_varshphal(natal_chart_data, target_year, birth_date, ...)`
- KP: now computes a KP chart and calls `calculate_kp_cuspal(planet_longitudes, cusps, ...)`
- Transits: now calls `calculate_transits(natal_chart_data, ...)` and wires interpretation + lucky payloads
- Remedies: now injects birth_date/time into chart payload for remedies Shadbala triggers
- Writes `report_debug_payload.json` (assembled inputs passed into PDF builder)
- Specialized sections adapters (these engines existed, but the CLI was calling non-existent function names):
  - Nadi: now calls `calculate_nadi_insights(chart_data)` and wraps as `{"results": [...]}` for the PDF renderer
  - Roga: now calls `analyze_diseases(chart_data)`
  - Vritti: now calls `analyze_vritti(chart_data)`
  - Apatya: now calls `analyze_apatya(chart_data)`
  - Longevity: now calls `calculate_lifespan(chart_data)`
  - Lal Kitab: now calls `get_remedies(planet_signs_map, chart_data)` and wraps as `{"results": {...}}`

### PDF renderer (`app/reports/kundli_report.py`)

- Replaced hardcoded missing boxes in Transits with real renderers:
  - Vedha/Latta summary table
  - Transit interpretation paragraphs per planet/house
  - Transit lucky KV + do/don’t lists
- Rebuilt Remedies output to required structured format:
  - Trigger → Remedy → Method → Timing → Benefit → Caution → Source Type/Reference
  - Uses Narad Puran “tradition mapping” label where present; does not fabricate verse numbers
- Added “Life Area Interpretations” section driven by existing `app/reports/interpretations.py:LIFE_PREDICTIONS`
- Fixed “premium layout” regressions:
  - Cover page no longer triggers an auto page-break (removes the blank first page)
  - Table of Contents is now finalized after all sections render (TOC is no longer empty)
  - SVG chart viewport scaling corrected (charts were rendering too small due to mm/points mismatch)

## Remaining gaps (actual)

These are not marked as “backend missing” unless the repo truly has no usable engine/data.

- Some advanced sections are still not added to the full-report payload (yet), even though engines exist (example: Graha Sambandha / Panchadha Maitri detailed engines are present but not displayed by PDF).
- Section audit appendix is still capability-based; it does not yet output the full per-section matrix requested (source used + interpretation attached + Narad/SVG flags) in the PDF itself.

## Next verification action

- Regenerate a full report via API (`/api/kundli/{id}/full-report`) and confirm:
  - TOC is populated
  - Core charts (D1/Moon/D9) are readable and correctly scaled
  - Specialized sections (Nadi/Roga/Vritti/Apatya/Longevity/Lal Kitab) render when engines succeed
