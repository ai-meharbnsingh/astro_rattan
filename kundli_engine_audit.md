# Kundli Engine Audit Report

**Generated:** 2026-04-21 22:03:08

## Engines Reused
- ✅ astro_engine (core planetary positions)
- ✅ dasha_engine (Vimshottari extended)
- ✅ dasha_engine (dasha phala)
- ✅ ashtottari_dasha_engine
- ✅ tara_dasha_engine
- ✅ moola_dasha_engine
- ✅ avakhada_engine
- ✅ panchang_engine

## Engines Missing / Failed

## Section Coverage Summary
- **Generated:** 18
- **Partial:** 3
- **Missing:** 17

## Front-end Tabs vs Backend Engines
✅ **Cover Page** — GENERATED | Engine computed successfully
✅ **Table of Contents** — GENERATED | Engine computed successfully
✅ **Executive Summary** — GENERATED | Engine computed successfully
✅ **Birth Particulars & Panchang** — GENERATED | Engine computed successfully
✅ **Panchang** — GENERATED | Engine computed successfully
✅ **Avakhada Chakra** — GENERATED | Engine computed successfully
✅ **Core Natal Charts (D1)** — GENERATED | Engine computed successfully
✅ **Core Charts (Moon & Navamsha)** — GENERATED | Engine computed successfully
✅ **Planetary Positions** — GENERATED | Engine computed successfully
✅ **Bhava Analysis** — GENERATED | Engine computed successfully
❌ **Aspects & Conjunctions** — NOT IMPLEMENTED | Engine missing or failed
❌ **Yogas & Doshas** — NOT IMPLEMENTED | Engine missing or failed
❌ **Divisional Charts** — NOT IMPLEMENTED | Engine missing or failed
⚠️ **Shodashvarga Summary** — PARTIALLY GENERATED | Engine computed successfully
❌ **Shadbala & Bhava Bala** — NOT IMPLEMENTED | Engine missing or failed
✅ **Planetary Friendship (Maitri)** — GENERATED | Engine missing or failed
✅ **Planetary Avasthas** — GENERATED | Engine computed successfully
❌ **Ashtakavarga** — NOT IMPLEMENTED | Engine missing or failed
✅ **Dasha Systems** — GENERATED | Engine missing or failed
✅ **Dasha Effects** — GENERATED | Engine computed successfully
❌ **Transits & Gochar** — NOT IMPLEMENTED | Engine missing or failed
❌ **Gochara Vedha** — NOT IMPLEMENTED | Engine missing or failed
⚠️ **Transit Interpretations** — PARTIALLY GENERATED | Engine computed successfully
⚠️ **Transit Lucky** — PARTIALLY GENERATED | Engine computed successfully
❌ **Varshphal (Annual Chart)** — NOT IMPLEMENTED | Engine missing or failed
❌ **KP System** — NOT IMPLEMENTED | Engine missing or failed
❌ **Jaimini Astrology** — NOT IMPLEMENTED | Engine missing or failed
❌ **Nadi Analysis** — NOT IMPLEMENTED | Engine missing or failed
❌ **Disease Analysis (Roga)** — NOT IMPLEMENTED | Engine missing or failed
❌ **Career (Vritti)** — NOT IMPLEMENTED | Engine missing or failed
❌ **Progeny (Apatya)** — NOT IMPLEMENTED | Engine missing or failed
❌ **Longevity Indicators** — NOT IMPLEMENTED | Engine missing or failed
❌ **Lal Kitab Summary** — NOT IMPLEMENTED | Engine missing or failed
✅ **Life Area Interpretations** — GENERATED | Engine computed successfully
❌ **Remedies & Upayas** — NOT IMPLEMENTED | Engine missing or failed
✅ **Lucky Indicators & Practical Guidance** — GENERATED | Engine computed successfully
✅ **Missing / Pending Sections Audit** — GENERATED | Engine computed successfully
✅ **About This Report** — GENERATED | Engine computed successfully

## What is Still Disconnected
The following report sections exist but their backend engines were not successfully invoked or not included:
- Aspects & Conjunctions: Engine missing or failed
- Yogas & Doshas: Engine missing or failed
- Divisional Charts: Engine missing or failed
- Shodashvarga Summary: engine exists but payload missing
- Shadbala & Bhava Bala: Engine missing or failed
- Planetary Friendship (Maitri): Engine missing or failed
- Ashtakavarga: Engine missing or failed
- Dasha Systems: Engine missing or failed
- Transits & Gochar: Engine missing or failed
- Gochara Vedha: Engine missing or failed
- Transit Interpretations: engine exists but payload missing
- Transit Lucky: engine exists but payload missing
- Varshphal (Annual Chart): Engine missing or failed
- KP System: Engine missing or failed
- Jaimini Astrology: Engine missing or failed
- Nadi Analysis: Engine missing or failed
- Disease Analysis (Roga): Engine missing or failed
- Career (Vritti): Engine missing or failed
- Progeny (Apatya): Engine missing or failed
- Longevity Indicators: Engine missing or failed
- Lal Kitab Summary: Engine missing or failed
- Remedies & Upayas: Engine missing or failed

## Action Required
1. Verify all engine modules are importable from the project root.
2. Ensure `swisseph` (pyswisseph) is installed for accurate calculations.
3. Add any missing engine wrappers to the orchestrator in `generate_complete_kundli_report.py`.
4. Run `pytest` to confirm individual engines produce valid output.