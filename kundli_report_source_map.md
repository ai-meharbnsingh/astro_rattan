# Kundli PDF Report — Source Map (Audit)

Generated: 2026-04-21

This document maps each Kundli PDF report section to:

- Backend engine (file + function)
- Interpretation source (file + key/function)
- Narad Puran remedy reference layer (if applicable)
- API/service layer (endpoint)
- Frontend section/component (where applicable)
- PDF assembler/template block (python)
- Status (per the requested labels)

Legend (Status)

- `WIRED` — engine/data exists and is currently rendered in the PDF
- `ENGINE EXISTS BUT NOT WIRED` — engine/data exists in repo but is not included in the PDF payload or not rendered
- `DATA EXISTS BUT NOT MAPPED` — data exists but the PDF assembler expects a different shape/key
- `INTERPRETATION EXISTS BUT NOT ATTACHED` — interpretation tables exist but PDF does not render them
- `REPORT ASSEMBLER BUG` — payload contains data but PDF prints a missing marker
- `PARTIAL SECTION — USING AVAILABLE EXISTING DATA` — subset exists and should still render

---

## 1) Cover Page

- Backend engine: N/A
- Interpretation: N/A
- API: `GET /api/kundli/{id}/pdf` / `GET /api/kundli/{id}/full-report`
- Frontend: `frontend/src/components/kundli/ConsolidatedReport.tsx` (download action)
- PDF assembler: `app/reports/kundli_report.py:ReportAssembler.render_cover()`
- Status: `WIRED`

## 2) Table of Contents

- Backend engine: N/A
- PDF assembler: `app/reports/kundli_report.py:ReportAssembler.render_toc()`
- Status: `WIRED`

## 3) Executive Summary

- Backend engine: `app/astro_engine.py:calculate_planet_positions` (chart core)
- Interpretation: `app/reports/interpretations.py` (lagna/nakshatra/personality tables)
- PDF assembler: `app/reports/kundli_report.py:ReportAssembler.render_executive_summary()`
- Status: `WIRED` (but quality issues may exist: duplication / overly generic text)

## 4) Birth Particulars

- Backend engine: DB row + core chart (`app/astro_engine.py`)
- API: `POST /api/kundli/generate` creates stored kundli; PDF uses stored birth fields
- Frontend: `frontend/src/components/kundli/BirthDetailsTab.tsx` (birth details tab)
- PDF assembler: `app/reports/kundli_report.py:ReportAssembler.render_birth_particulars()`
- Status: `WIRED`

## 5) Panchang & Avakhada

- Backend engines:
  - `app/panchang_engine.py:calculate_panchang`
  - `app/avakhada_engine.py:calculate_avakhada`
- API:
  - `GET /api/kundli/{id}/panchang`
  - `GET /api/kundli/{id}/avakhada`
- Frontend:
  - `frontend/src/components/kundli/PanchangTab.tsx`
  - `frontend/src/components/kundli/AvakhadaTab.tsx`
- PDF assembler:
  - `app/reports/kundli_report.py:ReportAssembler.render_birth_particulars()` (includes Panchang block)
- Status: `WIRED` if these keys are present in PDF payload (`panchang`, `avakhada`)

## 6) Core Natal Charts (D1, Moon, Bhava)

- Backend engine (raw placements): `app/astro_engine.py:calculate_planet_positions`
- Frontend SVG chart components:
  - `frontend/src/components/KundliChartSVG.tsx` (North Indian SVG)
  - `frontend/src/components/InteractiveKundli.tsx` (interactive SVG)
- PDF assembler:
  - `app/reports/kundli_report.py:ReportAssembler.render_core_charts()`
  - Helper: `app/reports/kundli_report.py:_draw_north_indian_chart_svg(...)`
- Status: `WIRED`
  - Core charts render as vector SVG in the PDF (report-quality scaling; no raster blur).

## 7) Planetary Positions

- Backend engine: `app/astro_engine.py:calculate_planet_positions`
- Interpretation: `app/reports/interpretations.py` (planet/house tables)
- API: `GET /api/kundli/{id}/planetary-positions`
- Frontend: `frontend/src/components/kundli/PlanetsTab.tsx`
- PDF assembler: `app/reports/kundli_report.py:ReportAssembler.render_planetary_positions()`
- Status: `WIRED`

## 8) Bhava Analysis

- Backend engine: `app/bhava_vichara_engine.py` and/or `app/bhava_phala_engine.py` (exists)
- Interpretation: `app/reports/interpretations.py` (house topics, bhavesh)
- API: `GET /api/kundli/{id}/bhava-vichara`, `GET /api/kundli/{id}/bhava-phala`
- Frontend: `frontend/src/components/kundli/BhavaTab.tsx` (tab exists)
- PDF assembler: `app/reports/kundli_report.py:ReportAssembler.render_bhava_analysis()`
- Status: `PARTIAL SECTION — USING AVAILABLE EXISTING DATA`
  - PDF renders house cusps + lordships; deeper bhava engines exist but are not fully mapped into the PDF payload yet.

## 9) Aspects & Conjunctions

- Backend engines:
  - `app/aspects_engine.py:calculate_aspects`
  - `app/conjunction_engine.py:calculate_conjunctions`
- Interpretation source: `app/data/conjunction_effects.json`
- API:
  - `GET /api/kundli/{id}/aspects`
  - `GET /api/kundli/{id}/conjunctions`
- Frontend: `frontend/src/components/kundli/AspectsTab.tsx` / `ConjunctionsTab.tsx` (tabs exist)
- PDF assembler: `app/reports/kundli_report.py:ReportAssembler.render_aspects()`
- Status: `WIRED` (if `aspects`/`conjunctions` included in payload)

## 10) Yogas & Doshas

- Backend engines:
  - `app/dosha_engine.py:analyze_yogas_and_doshas`
  - Rules data: `app/data/yogas.json`
- API: `GET /api/kundli/{id}/yogas-doshas`, `GET /api/kundli/{id}/maha-yogas`, `GET /api/kundli/{id}/raja-yogas`
- Frontend: `frontend/src/components/kundli/YogasDoshasTab.tsx`
- PDF assembler: `app/reports/kundli_report.py:ReportAssembler.render_yogas_doshas()`
- Status: `WIRED` if `yogas_doshas` is present

## 11) Divisional Charts + 12) Shodashvarga Summary

- Backend engines:
  - `app/divisional_charts.py:calculate_divisional_chart_detailed`
  - `app/sodashvarga_engine.py:calculate_sodashvarga`
- API: `GET /api/kundli/{id}/divisional-charts`, `GET /api/kundli/{id}/sodashvarga`
- Frontend: `frontend/src/components/kundli/DivisionalTab.tsx`
- PDF assembler:
  - `app/reports/kundli_report.py:ReportAssembler.render_divisional_charts()`
  - `app/reports/kundli_report.py:ReportAssembler.render_shodashvarga_summary()`
- Status: `WIRED` if `sodashvarga` is present

## 13) Shadbala & 14) Bhava Bala

- Backend engines:
  - `app/shadbala_engine.py:calculate_shadbala`
  - `app/shadbala_engine.py:calculate_bhav_bala`
- API: `GET /api/kundli/{id}/shadbala`
- Frontend: `frontend/src/components/kundli/ShadbalaTab.tsx`
- PDF assembler: `app/reports/kundli_report.py:ReportAssembler.render_shadbala()`
- Status: `WIRED` if `shadbala` is present

## 15) Planetary Friendship / Maitri

- Backend engines:
  - `app/panchadha_maitri_engine.py:calculate_panchadha_maitri`
  - `app/graha_sambandha_engine.py:calculate_graha_sambandha`
- API:
  - `GET /api/kundli/{id}/panchadha-maitri`
  - `GET /api/kundli/{id}/graha-sambandha`
- Frontend: dedicated tabs exist (see `frontend/src/sections/KundliGenerator.tsx`)
- PDF assembler: `app/reports/kundli_report.py:ReportAssembler.render_planetary_friendship()`
- Status: `PARTIAL SECTION — USING AVAILABLE EXISTING DATA`
  - PDF currently uses sign-based friendship; the detailed engines exist but are not fully mapped into the PDF payload yet.

## 16) Avasthas

- Interpretation source: `app/reports/interpretations.py` (`GRAHA_AVASTHAS`)
- PDF assembler: `app/reports/kundli_report.py:ReportAssembler.render_avasthas()`
- Status: `WIRED` (computed from chart data)

## 17) Ashtakavarga + 18) Sarvashtakavarga

- Backend engine: `app/ashtakvarga_engine.py:calculate_ashtakvarga`
- API: `GET /api/kundli/{id}/ashtakavarga`
- Frontend: `frontend/src/components/kundli/AshtakvargaTab.tsx`
- PDF assembler: `app/reports/kundli_report.py:ReportAssembler.render_ashtakavarga()`
- Status: `WIRED` if `ashtakvarga` is present

## 19) Dasha Systems (Vimshottari / Yogini / Kalachakra / etc.)

- Backend engines:
  - `app/dasha_engine.py:calculate_extended_dasha` (Vimshottari with antardasha/pratyantar)
  - `app/yogini_dasha_engine.py:calculate_yogini_dasha`
  - `app/kalachakra_engine.py:calculate_kalachakra_dasha`
  - `app/ashtottari_dasha_engine.py:calculate_ashtottari_dasha`
  - `app/moola_dasha_engine.py:calculate_moola_dasha`
  - `app/tara_dasha_engine.py:calculate_tara_dasha`
- Interpretation:
  - `app/data/dasha_phala.json` + `app/dasha_engine.py:analyze_*_phala`
  - `app/reports/interpretations.py` (`DASHA_INTERPRETATIONS`, `ANTARDASHA_INTERPRETATIONS`)
- API:
  - `GET /api/kundli/{id}/dasha`
  - `GET /api/kundli/{id}/kalachakra-dasha`
- PDF assembler: `app/reports/kundli_report.py:ReportAssembler.render_dashas()`
- Status: `PARTIAL SECTION — USING AVAILABLE EXISTING DATA`
  - Vimshottari/Yogini/Kalachakra engines exist; some are currently not wired into the PDF payload.

## 20) Dasha Effects (Dasha Phala)

- Backend engine: `app/dasha_engine.py:get_current_dasha_phala`
- Source data: `app/data/dasha_phala.json`
- API: `GET /api/kundli/{id}/dasha-phala`
- Frontend: `frontend/src/components/kundli/DashaPhalaTab.tsx`
- PDF assembler: `app/reports/kundli_report.py:ReportAssembler.render_dashas()` (expects `dasha_phala`)
- Status: `WIRED`
  - `dasha_phala` is included in the full-report payload and rendered in the PDF.

## 21) Current Transits & Gochar

- Backend engine: `app/transit_engine.py:calculate_transits` (includes Vedha/Latta enrichment)
- Data: `app/data/gochara_vedhas.json`, `app/data/latta_table.json`
- API:
  - `POST /api/kundli/{id}/transits`
  - `GET /api/kundli/{id}/gochara-vedha`
- Frontend: `frontend/src/components/kundli/TransitsTab.tsx`
- PDF assembler: `app/reports/kundli_report.py:ReportAssembler.render_transits()`
- Status: `WIRED`
  - `transit` is included in the full-report payload and rendered in the PDF (including Vedha/Latta enrichment when available).

## 22) Transit Interpretations

- Interpretation source: `app/transit_interpretations.py:TRANSIT_FRAGMENTS`
- API: `GET /api/kundli/{id}/transit-interpretations`
- Frontend: `frontend/src/components/kundli/TransitsTab.tsx` (interpretation block)
- PDF assembler: `app/reports/kundli_report.py:ReportAssembler.render_transits()`
- Status: `WIRED`

## 23) Lucky Indicators (Transit-based)

- Backend engine: `app/transit_lucky.py:get_all_lucky_metadata`
- API: `GET /api/kundli/{id}/transit-lucky`
- PDF assembler: `app/reports/kundli_report.py:ReportAssembler.render_transits()`
- Status: `WIRED`

## 24) Varshphal

- Backend engine: `app/varshphal_engine.py:calculate_varshphal`
- API: `POST /api/kundli/{id}/varshphal`
- Frontend: `frontend/src/components/kundli/VarshphalTab.tsx`
- PDF assembler: `app/reports/kundli_report.py:ReportAssembler.render_varshphal()`
- Status: `WIRED`

## 25) KP System

- Backend engine: `app/kp_engine.py:calculate_kp_cuspal`
- API: `POST /api/kundli/{id}/kp-analysis`, `GET /api/kundli/{id}/kp-system`
- Frontend: `frontend/src/components/kundli/KPTab.tsx`
- PDF assembler: `app/reports/kundli_report.py:ReportAssembler.render_kp()`
- Status: `WIRED` (when `kp` is included in payload)

## 26) Jaimini / Special Lagnas

- Backend engine: `app/jaimini_engine.py:calculate_jaimini`
- API: `GET /api/kundli/{id}/jaimini`
- Frontend: `frontend/src/components/kundli/JaiminiTab.tsx`
- PDF assembler: `app/reports/kundli_report.py:ReportAssembler.render_jaimini()`
- Status: `WIRED` (when `jaimini` is included in payload)

## 27) Remedies & Upayas (Narad Puran reference layer)

- Backend engine: `app/remedy_engine.py:generate_astrological_remedies`
- Remedy reference layer (Narad Puran mapping):
  - `app/remedy_sources.py` (fields include `source_type`, `source_label`, `scriptural_reference`)
- API: (engine is available for bundling; LK remedies have separate endpoints)
- Frontend: `frontend/src/components/kundli/GeneralRemedies.tsx`
- PDF assembler: `app/reports/kundli_report.py:ReportAssembler.render_remedies()`
- Status: `WIRED`
  - Remedies render in a structured format and preserve Narad Puran source labels without fabricating verse numbers.

## 28) Life Area Interpretations (Synthesis)

- Interpretation source: `app/reports/interpretations.py:LIFE_PREDICTIONS` + house/planet interpretation tables
- Frontend: consolidated report tab sections (various)
- PDF assembler: `app/reports/kundli_report.py:ReportAssembler.render_life_areas()`
- Status: `WIRED`

## 29) Missing / Partial / Audit Appendix + Technical Source Appendix

- PDF assembler:
  - `app/reports/kundli_report.py:ReportAssembler.render_missing_audit()`
- Status: `PARTIAL SECTION — USING AVAILABLE EXISTING DATA`
  - Existing audit is “capability-based”; it does not yet provide the required per-section source+attachment+SVG/Narad status matrix.

---

## Key Files (Entry Points)

- CLI orchestrator: `generate_complete_kundli_report.py`
- API PDF endpoints: `app/routes/kundli.py` (`/pdf` and `/full-report`)
- PDF assembler: `app/reports/kundli_report.py`
- Interpretation DB (static): `app/reports/interpretations.py`
- Narad Puran remedy mapping: `app/remedy_sources.py`
- Transits + interpretations + lucky: `app/transit_engine.py`, `app/transit_interpretations.py`, `app/transit_lucky.py`, `app/gochara_vedha_engine.py`
