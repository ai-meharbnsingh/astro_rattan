# Remedy Reference Map (Narad Puran Layer Audit)

Generated: 2026-04-21

Purpose: Provide a repository-backed map of remedy triggers → remedies → Narad Puran reference availability.

Source of truth:

- Remedy catalog + Narad Puran tradition mapping fields: `app/remedy_sources.py`
- Remedy assembly logic: `app/remedy_engine.py`

Notes:

- If `source_type == "narad_puran"` but no exact chapter/verse is stored, the PDF must label it as `Narad Puran tradition mapping` (no fabricated verse numbers).

---

## Planetary Triggers → Remedies

Source table: `PLANETARY_REMEDIES` (`app/remedy_sources.py`)

For each planet: `trigger = weak/afflicted/combust/debilitated` (as detected by chart logic + Shadbala best-effort).

- Sun
  - Narad Puran reference status: PRESENT (`source_type=narad_puran` appears in remedies list)
  - Remedies (titles with source labels):
    - Surya Gayatri Mantra — `Narad Puran tradition mapping`
    - Sun Donation — `Traditional reference layer`

- Moon
  - Narad Puran reference status: PRESENT
  - Remedies:
    - Chandra Mantra — `Narad Puran tradition mapping`
    - Respecting Mother Figures — `Traditional reference layer`

- Mars
  - Narad Puran reference status: PRESENT
  - Remedies:
    - Mangal Mantra — `Narad Puran tradition mapping`
    - Physical Discipline — `Chart-derived recommendation`

- Mercury
  - Narad Puran reference status: PRESENT
  - Remedies:
    - Budh Mantra — `Narad Puran tradition mapping`

- Jupiter
  - Narad Puran reference status: PRESENT
  - Remedies:
    - Guru Mantra — `Narad Puran tradition mapping`

- Venus
  - Narad Puran reference status: PRESENT
  - Remedies:
    - Shukra Mantra — `Narad Puran tradition mapping`

- Saturn
  - Narad Puran reference status: PRESENT
  - Remedies:
    - Shani Mantra — `Narad Puran tradition mapping`
    - Helping Laborers — `Traditional reference layer`

- Rahu
  - Narad Puran reference status: PRESENT
  - Remedies:
    - Rahu Mantra — `Narad Puran tradition mapping`

- Ketu
  - Narad Puran reference status: PRESENT
  - Remedies:
    - Ketu Mantra — `Narad Puran tradition mapping`

---

## Dosha Triggers → Remedies

Source table: `DOSHA_REMEDIES` (`app/remedy_sources.py`)

- Mangal Dosha
  - Narad Puran reference status: PRESENT
  - Remedies:
    - Hanuman Chalisa — `Narad Puran tradition mapping`

- Kaal Sarp Dosha
  - Narad Puran reference status: PARTIAL (uses traditional mapping; not explicitly Narad Puran-tagged in current data)

- Sade Sati
  - Narad Puran reference status: PRESENT (some entries tagged `narad_puran` in remedy sources)

- Pitra Dosha / Kemdrum Dosha
  - Narad Puran reference status: depends on `app/remedy_sources.py` entries; verify per remedy item (some are traditional).

---

## General Balancing (Never Empty)

Source table: `GENERAL_BALANCING` (`app/remedy_sources.py`)

These ensure the remedies section never renders empty even when no severe affliction is detected.

- Expected output behavior:
  - At least 2 balancing remedies
  - At least 1 spiritual remedy
  - At least 1 behavioral remedy
  - If any Narad Puran-tagged general remedy exists, include it with label `Narad Puran tradition mapping`

