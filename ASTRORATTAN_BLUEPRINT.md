# ASTRORATTAN — Complete Platform Blueprint

> **astrorattan.com** · Production · April 2026
>
> A comprehensive Vedic astrology platform delivering four major feature systems:
> **Kundli** · **Lal Kitaab** · **Numerology** · **Vastu Shastra**
>
> This document is derived exclusively from the implemented codebase — frontend components,
> backend engines, and API routes. Every feature listed exists in production code.

---

## Table of Contents

1. [Platform Overview](#platform-overview)
2. [KUNDLI — Birth Chart System](#1-kundli--birth-chart-system)
3. [LAL KITAAB — Red Book System](#2-lal-kitaab--red-book-system)
4. [NUMEROLOGY — Numbers System](#3-numerology--numbers-system)
5. [VASTU SHASTRA — Sacred Architecture System](#4-vastu-shastra--sacred-architecture-system)
6. [Cross-Feature Infrastructure](#5-cross-feature-infrastructure)

---

## Platform Overview

Astrorattan is a full-stack astrology platform built on **FastAPI** (Python backend) + **React/TypeScript** (frontend). It uses **Swiss Ephemeris** for planetary calculations, **PostgreSQL** for persistence, and delivers results bilingually in **English and Hindi (Devanagari)**.

| Dimension | Scale |
|---|---|
| Backend engines | 90+ Python modules |
| API endpoints | 150+ routes |
| Frontend components | 120+ React/TypeScript files |
| Bilingual coverage | English + Hindi throughout |
| Calculation core | Swiss Ephemeris, Lahiri ayanamsa |
| Auth | JWT with role-based access (user / astrologer / admin) |

---

## 1. KUNDLI — Birth Chart System

### What It Is

Kundli is the core Vedic birth chart module. It generates a complete natal horoscope from birth date, time, and place using Swiss Ephemeris and the Lahiri ayanamsa (sidereal zodiac). The system encompasses 35+ analysis modules spanning classical Parashari, Jaimini, KP, and modern predictive techniques. All outputs are bilingual.

**Entry point:** `frontend/src/components/kundli/KundliForm.tsx`  
**Primary backend:** `app/routes/kundli.py`, `app/astro_engine.py`

---

### 1.1 Chart Generation & Birth Data

**Frontend:** `KundliForm.tsx`, `BirthDetailsTab.tsx`  
**Backend:** `astro_engine.py:calculate_planet_positions()`

**Inputs:**
- Name, date of birth, time of birth (optional), place of birth, timezone

**Chart Output — 9 Planets (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu):**
- Longitude (degrees, minutes, seconds)
- Zodiac sign & sign-degree
- Nakshatra (lunar mansion) & pada (quarter)
- House placement (1–12)
- Retrograde status
- Dignity: exalted / own sign / moolatrikona / friend / neutral / enemy / debilitated
- Combustion status
- Jaimini Chara Karakas (AK, AmK, BK, MK, PK, PiK, GK)

**Ascendant Details:**
- Lagna sign, degree, nakshatra, lord
- Chandra Lagna (Moon ascendant)
- Surya Lagna (Sun ascendant)

**BirthDetailsTab columns:** Planet · Sign · Sign-Degree (with sandhi flag) · Nakshatra & Pada · House · Dignity (color-coded) · Sign type · Element · Nature · Retrograde indicator · Jaimini Karaka

---

### 1.2 Planet Properties (Phaladeepika Adhyaya 2)

**Frontend:** `PlanetsTab.tsx`  
**Backend:** `app/planet_properties_engine.py`

- Day/Night chart classification (6 AM–6 PM = day chart)
- Father indicator (Sun in day charts, Saturn in night charts)
- Mother indicator (complementary parent significator)
- Mercury gender state (male / female / hermaphrodite based on conjunction context)
- Lagna sign triad: Deva / Manava / Rakshasa classification
  - Deva: Aries, Gemini, Leo, Libra, Sagittarius, Aquarius
  - Manava: Taurus, Cancer, Virgo, Scorpio, Capricorn
  - Rakshasa: Pisces (mixed)
- Sloka references from Phaladeepika

---

### 1.3 Vimshottari Dasha System

**Frontend:** `DashaTab.tsx`  
**Backend:** `app/dasha_engine.py`

**Vimshottari (120-year cycle) — order:** Ketu → Venus → Sun → Moon → Mars → Rahu → Jupiter → Saturn → Mercury

**Current Period Panel:**
- Active Mahadasha lord & date range
- Active Antardasha lord & date range
- Active Pratyantar Dasha lord & date range

**Full Timeline Table:**
- All 9 Mahadashas with nested Antardashas and Pratyantar Dashas
- Expandable/collapsible at each level
- Start/end dates + duration; current period highlighted

**Sookshma-Prana Sub-dashas:**
- Sookshma Dasha (sub-AD) lord & date range
- Prana Dasha (sub-sub-AD) lord & date range

**Dasha Phala (Effects):** `DashaPhalaTab.tsx`
- Mahadasha effects based on lord's placement, dignity, conjunctions
- Antardasha refined effects with yoga/dosha multipliers
- Pratyantar Phala for finest-grain interpretation

---

### 1.4 Dosha Analysis

**Frontend:** `DoshaTab.tsx`  
**Backend:** `app/dosha_engine.py`

#### Mangal Dosha (Mars Defect)
- Detected when Mars occupies houses 1, 2, 4, 7, 8, or 12
- Severity levels: Mild / Moderate / Severe
- Cancellation rules applied automatically
- Effects description & remedy list

#### Kaal Sarp Dosha (Serpent Defect)
- Rahu–Ketu axis enclosing all planets
- Presence indicator + description + remedies

#### Sade Sati (7.5-Year Saturn Transit)
- Three phases: Purvardha / Madhya / Uttarardha
- Ashtam Shani escalation (Saturn in 8th from Moon = most severe)
- Effect description per phase
- Up to 4 specific remedies per phase

---

### 1.5 Yogas & Combinations

**Frontend:** `YogaDoshaTab.tsx`  
**Backend:** `app/yoga_rule_engine.py`, `app/maha_yoga_engine.py`, `app/raja_yoga_engine.py`

**Yoga Categories:**
- **Raja Yogas** — Leadership & authority combinations (5+ sub-types)
- **Dhana Yogas** — Wealth-giving combinations
- **Pancha Mahapurusha** — 5 exaltation/own-sign yogas:
  - Ruchaka (Mars), Bhadra (Mercury), Hamsa (Jupiter), Malavya (Venus), Shasha (Saturn)
- **Nabhasa Yogas** — Positional patterns (Aashraya, Dala, Akriti, Sankhya)
- **Chandra Yogas** — Moon-based combinations
- **Surya Yogas** — Sun-based combinations
- **Arishta Yogas** — Affliction combinations

**Per Yoga Output:** Presence indicator · Nature (benefic/malefic/mixed) · Strength level · Description · Remedies

**Maha Yogas:** `GET /api/kundli/{id}/maha-yogas`  
**Raja Yogas:** `GET /api/kundli/{id}/raja-yogas`

---

### 1.6 Divisional Charts (Vargas)

**Frontend:** `DivisionalTab.tsx`  
**Backend:** `app/divisional_charts.py`

16 Vargas available via chart selector:

| Chart | Division | Domain |
|---|---|---|
| D1 (Rashi) | 1 | Physical self, general life |
| D2 (Hora) | 2 | Wealth |
| D3 (Drekkana) | 3 | Siblings, courage |
| D4 (Chaturthamsa) | 4 | Property, fortune |
| D5 (Panchamsa) | 5 | Power, authority |
| D7 (Saptamsa) | 7 | Children |
| D9 (Navamsa) | 9 | Spouse, dharma, inner self |
| D10 (Dasamsa) | 10 | Career, profession |
| D12 (Dwadasamsa) | 12 | Parents |
| D16 (Shodasamsa) | 16 | Vehicles, comforts |
| D20 (Vimsamsa) | 20 | Spiritual practices |
| D24 (Chaturvimsamsa) | 24 | Education |
| D27 (Saptavimsamsa) | 27 | Strength, vitality |
| D30 (Triamsamsa) | 30 | Misfortunes, health |
| D40 (Chatvarimsamsa) | 40 | Maternal ancestry |
| D60 (Shashtyamsa) | 60 | Past-life karma |

Each chart renders: North Indian Diamond SVG · Planetary positions table (planet, sign, degree, nakshatra, pada, house) · Lord significance cards for D2, D3, D30

---

### 1.7 Ashtakvarga — Strength Grid

**Frontend:** `AshtakvargaTab.tsx`, `AshtakvargaPhalaTab.tsx`  
**Backend:** `app/ashtakvarga_engine.py`

**Planet-wise Ashtakvarga:**
- 8 separate tables (Sun through Saturn)
- Bindus (0–8) per sign for each planet
- SAV (Sarva Ashtakvarga) — total bindus per sign
- Color coding: ≥ 28 bindus = strong (green), < 28 = weak (red)
- North Indian Diamond chart with SAV bindus per house

**Ashtakvarga Phala (Predictive Benefits):**
- House strengths with SAV thresholds
- Planet transit favorability by sign
- Special combinations (houses 5+6+7 ≥ 28 → marital happiness, etc.)
- Transit recommendations for beneficial timing
- Horasara Phala special rules

---

### 1.8 Shadbala — Six-fold Planetary Strength

**Frontend:** `ShadbalaTab.tsx`  
**Backend:** `app/shadbala_engine.py`

Six strength components per planet (Sun through Saturn):

| Bala | Component | Measures |
|---|---|---|
| Sthana Bala | Positional | Exaltation, saptavarga, kendra position |
| Kala Bala | Temporal | Day/night, paksha, hora, ayana |
| Chesta Bala | Motional | Retrograde speed |
| Naisargika Bala | Natural | Innate planet strength |
| Drig Bala | Directional | Aspect strength received |
| Bhava Bala | House | House placement quality |

Display: Bar chart per planet · Minimum required strength threshold (dashed line) · Star indicator if ratio > 1.2 · Expandable sub-component breakdown

---

### 1.9 Bhava Analysis (House Effects)

**Frontend:** `BhavaPhalaTab.tsx`, `BhavaVicharaTab.tsx`  
**Backend:** `app/bhava_phala_engine.py`, `app/bhava_vichara_engine.py`

**Bhava Phala (House-by-house predictions):**
- House lord placement & strength
- Planets in house + aspects received
- Timing indicators (dasha/transit)
- Predictions: general / personal / familial / health / financial

**Bhava Vichara (House examination):**
- House characteristics (nature, ruled topics)
- Strength assessment
- Functional benefic/malefic classification
- Occupant planet analysis

---

### 1.10 Kundli Milan — Compatibility Matching

**Frontend:** `KundliMilanTab.tsx`  
**Backend:** `app/matching_engine.py:calculate_kundli_match()`

**8-Koot Matching System:**

| Koot | Maximum Points | What It Measures |
|---|---|---|
| Nadi | 8 | Physiological compatibility |
| Bhakoot | 7 | Sign pairing (emotional bond) |
| Gana | 6 | Nature harmony (Deva/Manava/Rakshasa) |
| Maitri | 5 | Planetary friendship |
| Yoni | 4 | Animal nature (sexual/instinctive) |
| Tara | 3 | Star harmony |
| Varna | 1 | Caste/class alignment |
| Vashya | 2 | Dominance/control |

**Output:** Total score / 36 · Compatibility % · Per-koot scoring · Dosha alerts (Nadi Dosha, Bhakoot Dosha, Gana Dosha) · Cancellation rules applied · Recommendation (Excellent / Good / Average / Poor) · Dosha remedies

---

### 1.11 Transits & Gochar

**Frontend:** `TransitsTab.tsx`  
**Backend:** `app/transit_engine.py`, `app/family_timing_engine.py`, `app/retrograde_engine.py`

**Current Transit Positions:**
- 9 planets' current signs & houses (relative to natal Lagna and Moon)
- House shift controls (0–12 for alternate ascendants)
- Date/time selector for any target date

**30-Day Transit Heatmap:**
- Calendar grid with intensity scores (0–100%)
- Green ≥ 70% · Amber 40–70% · Red < 40%
- Hover tooltip: date, intensity %, daily summary

**Family Timing Indicators:**
- Father / Mother / Siblings / Spouse life-event timing
- Favorable/unfavorable markers with transit reasoning

**Retrograde Stations:**
- Station date (when retrograde begins)
- Direct date (when direct motion resumes)
- Duration, sign range, effect interpretation

---

### 1.12 Sade Sati Lifelong Analysis

**Frontend:** `SadesatiTab.tsx`  
**Backend:** `app/lifelong_sade_sati.py`

- All 3 Sade Sati cycles across the lifetime
- Each cycle: phases (Purvardha/Madhya/Uttarardha), transit sign, date range, severity
- Dhayya (2.5-year sub-cycles) table per cycle
- Remedies per cycle

---

### 1.13 Longevity & Ayurdaya

**Frontend:** `LongevityTab.tsx`  
**Backend:** `app/ayurdaya_engine.py`, `app/ashtakavarga_lifespan_engine.py`

**Lifespan Methods:**
- Amsa method (Tajaka)
- Ashtottari Dasha extension
- Saturn transit cycle analysis
- 8th house strength assessment

**Death Indicators:**
- Saturn transit to 8th from Moon (high / moderate / low severity)
- Dasha–Gochara convergence analysis
- Mahadasha lord in 8th/12th alignment
- Maraka planet activation windows

---

### 1.14 Roga — Disease Predisposition

**Frontend:** `RogaTab.tsx`  
**Backend:** `app/roga_engine.py`

- General disease tendencies (planet–house combinations)
- Body part mapping (house → anatomical regions)
- Special disease yogas (cancer, diabetes, etc.)
- Severity levels: low / moderate / severe / chronic
- Timing indicators (dasha periods prone to onset)
- Afflicted planet disease profile
- 6th house sign vulnerability areas

---

### 1.15 Aspects (Vedic & Western)

**Frontend:** `AspectsTab.tsx`  
**Backend:** `app/aspects_engine.py`

**Vedic (Graha Dristi) — special aspects:**
- Sun/Moon/Mercury/Venus: 7th house
- Mars: 4th & 8th (special)
- Jupiter: 5th, 7th & 9th (special)
- Saturn: 3rd, 7th & 10th (special)

Per planet: Aspected-By table (benefic = green, malefic = red) · Aspects-To list · Strength multipliers

**Western Aspects (Ptolemaic):** `GET /api/kundli/{id}/western-aspects`
- Geocentric, configurable orbs
- Conjunction, sextile, square, trine, opposition, quincunx

---

### 1.16 Conjunctions

**Frontend:** `ConjunctionsTab.tsx`  
**Backend:** `app/conjunction_engine.py`

Per conjunction: Planets involved · House & sign · Orb · Name (bilingual) · Nature (benefic/malefic/mixed) · Full effect description · Enhancement/weakening factors · Special yoga triggered · Effect strength (full/partial/reversed) · D12 amplification note · Sloka reference

---

### 1.17 Jaimini Astrology

**Frontend:** `JaiminiTab.tsx`  
**Backend:** `app/jaimini_engine.py`

**7 Chara Karakas (Movable Significators):**

| Karaka | Signifies |
|---|---|
| Atma Karaka (AK) | Soul, life purpose |
| Amatya Karaka (AmK) | Profession, minister |
| Bhratri Karaka (BK) | Siblings |
| Matri Karaka (MK) | Mother |
| Pitri Karaka (PiK) | Father |
| Putra Karaka (PK) | Children |
| Gnatri Karaka (GK) | General relations |

**4 Special Lagnas:**
- Arudha Lagna (AL) — world's perception of you
- Upapada Lagna (UL) — marriage & spouse
- Karakamsha — soul's journey (AK in D9)
- Hora Lagna — wealth & finances

**Jaimini Dasha Systems:**
- Chara Dasha (8-sign system)
- Sthira Dasha (fixed sign system)
- Navamsha Dasha (harmonic divisional)

---

### 1.18 KP Astrology (Krishnamurti Paddhati)

**Frontend:** `KPTab.tsx`  
**Backend:** `app/kp_engine.py`

**Planet Reference Table:** Planet · R/C status · Sign · DMS degree · Nakshatra · Pada · Rashi Lord (RL) · Nakshatra Lord (NL) · Sub Lord (SL) · Sub-Sub Lord (SSL) · Star Lord of Sub Lord (SSSL)

**Two Chart Views:**
- Birth Chart (Rashi-based houses — North Indian Diamond SVG)
- Cuspal Chart (cusp-degree-based house placement)

**House Significations:** 249 sub-divisions table — House · Rashi lord · Star lord · Sub lord · Signification

**KP Horary (Prashna):** Question number (0–249) → sign/sub mapping → significator analysis → verdict (Favorable / Unfavorable / Mixed) with bilingual summary

---

### 1.19 Upagrahas (Sub-Planets)

**Frontend:** `UpagrahasTab.tsx`  
**Backend:** `app/upagraha_engine.py`

11 Upagrahas: Gulika · Mandi · Yamakantaka · Ardhaprahara · Kala · Mrityu · Dhuma · Vyatipata · Parivesha · Indrachapa · Upaketu

Per upagraha: Name (EN/HI) · House · Sign · Degree DMS · Nakshatra · Nature badge · Interpretation · Sloka reference

**Critical Alert:** Gulika or Mandi in Lagna (House 1) → severe red warning (Phaladeepika Adh. 25)

---

### 1.20 Sodashvarga — 16-Varga Strength Grading

**Frontend:** `SodashvargaTab.tsx`  
**Backend:** `app/varga_grading_engine.py`

**6 Strength Tiers per Planet:**

| Tier | Name | Description |
|---|---|---|
| 1 (Worst) | Bhedaka | Afflicted in most vargas |
| 2 | Parijatamsa | Mostly afflicted |
| 3 | Uttamamsa | Mixed |
| 4 | Gopuramsa | Mostly well-placed |
| 5 | Simhasanamsa | Exalted/own in most |
| 6 (Best) | Parvatamsa | Strongest across all 16 |

Per planet: Progress bar (0–16 vargas) · Tier badge · Sign in each varga · Dignity in each varga · Summary %

---

### 1.21 Varshphal — Annual Charts

**Frontend:** `VarshphalTab.tsx`  
**Backend:** `app/varshphal_engine.py`

- Year selector (current ± 10)
- Solar return date & time (Sun returns to natal degree)
- Year lord calculation
- Planet positions in solar return chart
- North Indian Diamond visualization
- Muntha (annual ascendant): sign, house, lord, interpretation
- Annual predictions: Muntha lord strength, transit effects, dasha alignment

---

### 1.22 Avakhada — Nadi Astrology

**Frontend:** `AvakhadaTab.tsx`  
**Backend:** `app/avakhada_engine.py`

- Gana: Deva / Manushya / Rakshasa
- Nadi: Aadi / Madhya / Antya (used in compatibility matching)
- Varna: Brahmin / Kshatriya / Vaishya / Shudra
- Yoni: 14 animal types (Horse, Elephant, Goat, Serpent, Dog, Cat, Rat, Cow, Buffalo, Tiger, Deer, Monkey, Mongoose, Lion)
- Paya: Gold / Silver / Copper / Iron (financial strength indicator)
- Name matching: birth nakshatra pada syllable table, suggested auspicious starting letters

---

### 1.23 Yogini Dasha

**Frontend:** `YoginiTab.tsx`  
**Backend:** `app/yogini_dasha_engine.py`

60-year cycle with 8 Yoginis: Mangala · Pingala · Dhanya · Bhramari · Bhairavy · Chulika · Mrityu · Shanti

Per yogini: Ruling planet · Period start/end dates · Duration in years · Current period highlighted

---

### 1.24 D108 Analysis — Ashtottaramsa

**Frontend:** `D108Analysis.tsx`  
**Backend:** `app/divisional_charts.py:calculate_d108_analysis()`

- 108-part divisional chart (each sub-division = 0.277°)
- Moksha potential score (0–100): High ≥ 70 · Moderate 40–70 · Low < 40
- Spiritual indicator: name, description, strength
- Past-life karma analysis: title, description, associated planet/house
- D108 North Indian Diamond chart

---

### 1.25 Sarvatobhadra Chakra

**Frontend:** `sarvatobhadra/SarvatobhadraChakra.tsx`  
**Backend:** `app/sarvatobhadra_chakra_engine.py`

9×9 grid chakra showing: Nakshatras · Zodiac signs · Sanskrit vowels (phonetic) · Days (Vara)

Cell color types: Saffron (nakshatras) · Green (signs) · Blue (vowels) · Purple (vara) · Gray (empty)

Natal & transit planets displayed in respective cells. Vedha lines (mutual affliction): green = auspicious · red = inauspicious · toggleable display

---

### 1.26 Specialized Analyses

| Tab | Backend Engine | What It Produces |
|---|---|---|
| Stri Jataka | `stri_jataka_engine.py` | Marriage yogas for female charts, 7th house analysis, marital prospect |
| Apatya | `apatya_engine.py` | Children yogas, 5th house analysis, count estimate, gender indicators, timing |
| Pravrajya | `pravrajya_engine.py` | Renunciation/monastic yoga detection |
| Iogita | `astro_iogita_engine.py` | 16-basin personality archetype (Dharma/Atma/Shakti/Kaam/Moh etc.) |
| Birth Rectification | `birth_rectification_engine.py` | Corrected birth time from life events, confidence score |
| Mundane | `mundane_engine.py` | National/collective astrology indicators |

---

### 1.27 New Tabs — 10 Engines Wired to Frontend

10 new tab components added to `frontend/src/sections/KundliGenerator.tsx` (lines 57–66 imports, lines 765–802 TabsContent renders, lines 102–137 TAB_DEFS). Grouped by category:

#### Timing Category (4 tabs)

**KalachakraTab** (`kalachakra-dasha` · `kalachakra_engine.py`)
- `GET /api/kundli/{id}/kalachakra-dasha`
- 360-year dasha cycle; `periods[]` with start/end dates; nested `antardashas[]` per period; planet colors + Hindi names

**GochaVedhaTab** (`gochara-vedha` · `gochara_vedha_engine.py`)
- `GET /api/kundli/{id}/gochara-vedha`
- `transits[]` rows: each transit planet with active Vedha obstructions — which natal planets it is blocked by and the blocking house

**TransitInterpretationsTab** (`transit-interp` · `transit_interpretations.py`)
- `GET /api/kundli/{id}/transit-interpretations`
- Per-planet interpretations across 5 life-area categories: `general` · `love` · `career` · `finance` (+ additional)
- Each category: `InterpretationCategory` with bilingual title + fragment text; expandable per planet

**TransitLuckyTab** (`transit-lucky` · `transit_lucky.py`)
- `GET /api/kundli/{id}/transit-lucky`
- `lucky_color` (EN/HI) · `compatible_sign` (EN/HI) · `mood` (EN/HI)
- `dos[]` + `donts[]` — bilingual do's and don'ts for current transit period
- `gemstones[]` — recommended stones with color swatches

#### Analysis Category (4 tabs)

**NavamshaCareerTab** (`navamsha-career` · `navamsha_profession_engine.py`)
- `GET /api/kundli/{id}/navamsha-profession`
- `primary_vocation` — career archetype from D9 placements
- `tenth_lord_info` — 10th lord in D9: sign, house, dignity
- `luminary_strength` — Sun/Moon comparative strength, career direction

**GrahaSambandhaTab** (`graha-sambandha` · `graha_sambandha_engine.py`)
- `GET /api/kundli/{id}/graha-sambandha`
- `relationships[]` — every planet pair with relationship type (conjunction/aspect/sign-exchange) and strength badge: Strong (emerald) / Moderate (amber) / Weak (red)
- Relationship type color-coding by aspect/conjunction/exchange category

**PanchadhaMaitriTab** (`panchadha-maitri` · `panchadha_maitri_engine.py`)
- `GET /api/kundli/{id}/panchadha-maitri`
- `friendships[]` — full 9×9 planet-pair matrix; each entry: natural friendship + temporary friendship → combined result (Friend / Neutral / Enemy)
- Combined result row styling: green (friend) / gray (neutral) / red (enemy)

**NadiAnalysisTab** (`nadi-analysis` · `nadi_engine.py`)
- `GET /api/kundli/{id}/nadi-analysis`
- `insights[]` — Nadi Shastra delineations per planet/house; each with `title_en` / `title_hi`, `description_en` / `description_hi`
- House labels (EN/HI) + planet color coding

#### Advanced Category (2 tabs)

**FamilyDemiseTab** (`family-demise` · `family_demise_engine.py`)
- `GET /api/kundli/{id}/family-demise-timing`
- Label in UI: "Family Longevity" / "परिवार आयु विचार"
- `overall_risk`: high / moderate / low (card border: amber / blue / green)
- `members[]` — per family member (Father/Mother/Spouse/Sibling): longevity indicators, risk level, timing notes
- `indicators[]` — supporting health/longevity indicators per planet

**AstroMapTab** (`astro-map` · `astro_mapping_engine.py`)
- `POST /api/astro-map` with kundli data payload
- `city_analysis[]` — scored cities by planetary line proximity
- `best_cities_by_area` — top cities for `career` / `love` / `health` life areas
- `planetary_lines[]` — raw planetary line data
- Life area tabs: Career (briefcase icon) · Love (heart icon) · Health (activity icon), each with score bar 0–100

---

---

## 2. LAL KITAAB — Red Book System

### What It Is

Lal Kitab (Red Book) is an ancient Hindi astrological tradition using a fixed-sign-to-house mapping where Aries always = House 1 regardless of the ascendant. It emphasizes karmic debts (Rin), practical remedies (Upay), and house-based life predictions. The Astrorattan implementation delivers **33 frontend tabs**, **58 API endpoints**, and **21+ backend Python modules**.

**Fixed House Mapping:**
```
Aries=H1  Taurus=H2  Gemini=H3  Cancer=H4  Leo=H5  Virgo=H6
Libra=H7  Scorpio=H8  Sagittarius=H9  Capricorn=H10  Aquarius=H11  Pisces=H12
```

**Entry point:** `frontend/src/components/lalkitab/`  
**Primary backend:** `app/routes/lalkitab.py`, 21 engine modules

---

### 2.1 Dashboard & Entry

**LalKitabDashboardTab.tsx**
- Planet count & empty houses count
- Current age & active Saala Grah (age-activation planet)
- Dosha count (detected vs. total) + high severity count
- Top 6 urgent remedies with urgency badges
- Navigation shortcuts to dosha and remedy detail tabs

**LalKitabForm.tsx**
- Name, DOB, TOB, Place, Gender
- Client selector for astrologer users (new vs. existing toggle)
- Real-time geolocation autocomplete (lat/lng/timezone)

**LalKitabFullReport.tsx — 10–15 Page PDF Report:**
1. Cover page (details + timestamp)
2. Table of contents
3. Tewa Chart & identification
4. Per-planet table (9 planets × 6 fields)
5. Detected doshas
6. Karmic debts (active/passive)
7. Prediction Studio scores
8. Remedies (full list with savdhaniyan)
9. Varshphal (solar return, muntha, mudda dasha)
10. Sources & references (tagged bibliography)

---

### 2.2 Tewa (Chart Classification)

**Frontend:** `LalKitabTevaTab.tsx`  
**Backend:** `lalkitab_advanced.py:identify_teva_type()`

Tewa types detected: Andha (blind) · Ratondha (night-blind) · Dharmi (righteous) · Nabalig (immature) · Khali (empty)

Color indicators: Red (Andha/Ratondha) · Green (Dharmi) · Orange (Nabalig) · Amber (Khali)

Planet state legend with visual indicators via `planet-state.ts`

---

### 2.3 Birth Chart

**Frontend:** `LalKitabKundliTab.tsx`, `InteractiveKundli.tsx`  
**Backend:** Fixed-house normalization (combust status stripped for LK)

Interactive Kundli visualization with LK fixed-house planet placement. Empty house count & incomplete chart warnings.

---

### 2.4 Planet & House Interpretations

**Frontend:** `LalKitabPlanetsTab.tsx`  
**Backend:** `lalkitab_interpretations.py:get_lk_house_interpretation()`

Per planet card (9 planets):
- Planet name & LK house position
- Remedy urgency (high/medium/low, auto-expanded for high)
- Remedy text (problem description, remedy action, how to perform)
- Kayam Grah (established/rooted planet) indicator
- House interpretation (all 9 × 12 = 108 combinations)
- Source tags (LK_CANONICAL / LK_DERIVED / VEDIC_INFLUENCED)

---

### 2.5 Dosha Detection

**Frontend:** `LalKitabDoshaTab.tsx`  
**Backend:** `lalkitab_dosha.py:detect_lalkitab_doshas()`

Doshas detected and classified: Lal Kitab Canonical doshas vs. Vedic Overlay doshas (split view)

Per dosha: Name (EN/HI) · Detected status · Severity (high/medium/low, color-coded) · Description · Remedy hint · Source badge

Detected doshas sorted first; clean-chart doshas shown separately.

---

### 2.6 Karmic Debts (Rin)

**Frontend:** `LalKitabRinTab.tsx`  
**Backend:** `lalkitab_advanced.py:calculate_karmic_debts()`, `lalkitab_compound_debt.py:rank_compound_debts()`

**11 Debt Types:**
पितृ ऋण (Father) · मातृ ऋण (Mother) · भ्रातृ ऋण (Sibling) · देव ऋण (God) · स्त्री ऋण (Female) · शत्रु ऋण (Enemy) · पितामह ऋण (Grandfather) · प्रपितामह ऋण (Great-grandfather) · ऋषि ऋण (Sage) · नृ ऋण (Human) · भूत ऋण (Past being)

Per debt: Associated planet · Description & indication · Active flag (planet in 6/8/12 houses) · Remedy text

**Compound Debt Analysis (P2.9):**
- Priority rank & score
- Cluster membership (activator, member count, combined score)
- Blocked-by relationships (debt A must resolve before debt B)
- Dasha-aware activation window
- Recommended resolution order (EN/HI)

---

### 2.7 Remedies (Upay)

**Frontend:** `LalKitabRemediesTab.tsx`  
**Backend:** `lalkitab_remedy_context.py`, `lalkitab_remedy_matrix.py`, `lalkitab_remedy_classifier.py`, `lalkitab_savdhaniyan.py`, `lalkitab_tithi_timing.py`

Per remedy card:
- Planet & house position
- Problem description (why needed)
- Remedy action (specific instruction)
- Method (how to perform)
- Material & day (e.g., copper, Sunday)
- Urgency badge (high/medium/low)
- Classification tier: Trial / Remedy / Good Conduct (LK 1952 system)
- Savdhaniyan (precautions) with severity levels (amber box)
- Remedy matrix: direction, color, material variants
- Tithi timing rules: preferred paksha, forbidden tithis, peak tithi
- Andhe Grah warning (if applicable)

**Remedy Wizard (Intent-Based):**  `LalKitabRemedyWizardModal.tsx` → `POST /api/lalkitab/remedy-wizard`
- User selects intent/goal
- Returns top 3–5 ranked remedies with confidence score & explanation
- Quick-start checklist + "Add to Tracker" button

---

### 2.8 Advanced Analysis (Bunyaad, Takkar, Enemy)

**Frontend:** `LalKitabAdvancedTab.tsx`, `LalKitabDiagnosticChart.tsx`  
**Backend:** `lalkitab_advanced.py`

| Concept | Description |
|---|---|
| **Bunyaad** (Foundation) | Base strength & stability of the chart; strongest house & planet |
| **Takkar** (Clash) | Planetary conflicts — conflicting pairs, clash severity |
| **Enemy Presence** | Planetary enmities — enemy combinations, threat level |
| **Dhoka** (Betrayal) | Relationship breakdown indicators |
| **Achanak Chot** (Sudden Blow) | Unexpected calamity indicators |
| **Chakar Cycle** | Planetary repetition pattern — same planet returning to same sign |
| **Andhe Grah** (Blind Planet) | Planets rendered blind by conjunction with afflicted neighbours |

Tabbed navigation (Bunyaad · Takkar · Enemy · Relationships) with animated SVG diagnostic chart.

**Chakar Cycle section** (`lalkitab_chakar.py:detect_chakar_cycle()`):
- Cycle length: 35 or 36 years (displayed prominently)
- Ascendant lord (sign → ruling planet mapping, all 12 signs)
- Trigger badge: green (active) / amber (approaching) / gray (dormant)
- Bilingual reason describing the cycle's karmic significance
- Shadow-year amber box shown when within 1 year of cycle peak

**Andhe Grah (Blind Planet) section** (`lalkitab_andhe_grah.py:detect_andhe_grah()`):
- "All clear" green card when no blind planets detected
- Per-planet warning cards when affliction found:
  - Planet name + house
  - Severity badge (high / medium / low)
  - Reasons list (Andha Teva, H12 placement, Papakartari, debilitated in dusthana)
  - Adjacency cautions (planets in neighbouring houses affected)
- 4 detection paths: Andha Teva chart type · H12 occupation · Papakartari squeeze · Debilitated in 6/8/12

---

### 2.9 Relations & Aspects

**Frontend:** `LalKitabRelationsTab.tsx`  
**Backend:** `lalkitab_relations_engine.py:build_relations()`

**Conjunctions (Yuti) per house:**
- Planets present, clashes array, friendships array
- Color-coded: clashes = red, friendships = blue

**Aspects (Drishti):** Aspecting planet · From house · List of aspected houses

---

### 2.10 Rules & House Principles

**Frontend:** `LalKitabRulesTab.tsx`  
**Backend:** `lalkitab_rules_engine.py:build_rules()`

**Mirror House Axis:** H1↔H7 · H2↔H8 · H3↔H9 · H4↔H10 · H5↔H11 · H6↔H12

Per axis: Planets in each house, mutual presence indicator

**Cross Effects:** From house → To house · Trigger planets · Has-trigger flag

---

### 2.11 Prediction Studio

**Frontend:** `LalKitabPredictionTab.tsx`  
**Backend:** `lalkitab_prediction_studio.py:build_prediction_studio()`

**5–7 Life Area Scores:**

| Area | Output |
|---|---|
| Marriage | Score 0–100 · Manglik · Spouse description |
| Career | Score · Job vs. business suitability |
| Health | Score · Vulnerabilities · Preventive measures |
| Wealth | Score · Method (job/business/inheritance/luck) |
| Spirituality | Score · Spiritual indicators |

**Per Area — Full Breakdown:**
- Confidence level: high / moderate / low / speculative
- Positive outcome description (EN/HI)
- Caution/challenge description (EN/HI)
- Remedy suggestion (EN/HI)
- Trace: planets & houses contributing

**3-Part Cause Structure (P4-R4):**
1. Primary cause
2. Secondary modifier
3. Supporting factor

**Explainable Evidence (P5):**
- Evidence rows: kind (trace/rule/penalty/bonus/cap) · planet · house · contribution · rule reference · label (EN/HI)
- Counterfactual: what would change the prediction

**Feedback loop:** Users can rate prediction accuracy; data informs future versions.

---

### 2.12 Saala Grah — Annual Planet Dasha

**Frontend:** `LalKitabDashaTab.tsx`  
**Backend:** `lalkitab_dasha.py:get_saala_grah()`, `get_dasha_timeline()`

- Current age & active Saala Grah (9-planet annual rotation)
- Current planet's sequence position, cycle year, description (EN/HI)
- Next Saala Grah & life phase indicators
- Years remaining in current phase
- Upcoming 5–7 planets with age ranges
- Past periods (historical)
- Timeline visualization with planet colors

---

### 2.13 Varshphal (Annual Chart)

**Frontend:** `LalKitabVarshphalTab.tsx`  
**Backend:** Shared `varshphal_engine.py`

- Year selector (current ± 5)
- Solar return chart visualization (Interactive Kundli)
- Solar return date & time
- Muntha (annual ascendant): house, favorable/caution indicator
- Year Lord (ruling planet)
- Mudda Dasha (intra-year sub-periods): planet · start date · end date · duration in days

---

### 2.14 Gochar — Live Transits

**Frontend:** `LalKitabGocharTab.tsx`  
**Backend:** `GET /api/lalkitab/gochar` (real-time ephemeris)

Per planet: Current sign · Sign degree · Nakshatra · Retrograde status (R indicator) · LK house (fixed mapping) · Speed note (slow/medium/fast — color-coded purple/orange/blue)

---

### 2.15 Chandra Kundali (Moon Chart)

**Frontend:** `LalKitabChandraKundaliTab.tsx`  
**Backend:** `lalkitab_chandra_kundali.py`, `lalkitab_chandra_readings.py`

- Moon-centered chart with house positions shifted by Moon's natal house
- Chandra Lagna conflict detection (if Moon house ≠ Ascendant house)
- Per-planet Chandra readings (interpretation from Moon-chart perspective)
- Dual chart comparison (Natal vs. Chandra)

---

### 2.16 Chandra Chaalana — 43-Day Moon Protocol

**Frontend:** `LalKitabChandraChaalanaTab.tsx`  
**Backend:** `lalkitab_chandra_tasks.py` (CHANDRA_CHAALANA_TASKS)

- 43-day structured spiritual/remedial practice
- Protocol start/restart functionality
- Daily task checklist (from predefined task library)
- Day mark-done with progress tracking
- Journal entries (date + note)

---

### 2.17 Technical Concepts

**Frontend:** `LalKitabTechnicalTab.tsx`  
**Backend:** `lalkitab_technical.py:classify_all_planet_statuses()`

| Concept | Description |
|---|---|
| Kayam Grah | Established/rooted planets — stable, fixed influence |
| Chalti Gaadi | Mobile influencer — fastest-moving planet affecting chart |
| Dhur Dhur Aage | Far-distance placement — planets at extreme degrees |
| Soya Ghar | Sleeping houses — unoccupied 6th/8th/12th |
| Muththi | Fist/grasp — dominant planet grouping |

---

### 2.18 Specialized Features

| Tab | Backend Module | Output |
|---|---|---|
| Forbidden Remedies | `lalkitab_forbidden.py` | Contraindicated remedies per chart with alternatives |
| Nishaniyan (Omens) | via routes | Planet-based daily omens (category: animal/color/food/dream), severity |
| Farmaan (Decrees) | via routes | Direct LK text instructions with source references |
| Family Harmony | `lalkitab_family.py` | Harmony score 0–100, dominant planet, cross-waking narrative, member linking |
| Vastu Correlation | `lalkitab_vastu.py` | Vastu recommendations by direction (NE/E/SE/S/SW/W/NW/N) |
| Milestones | `lalkitab_milestones.py` | 7-year cycles, life milestone events, activated house themes |
| Palmistry | `lalkitab_palmistry.py` | SVG palm diagram, zone-to-planet mapping, expected mark predictions |
| Sacrifice (Daan) | `lalkitab_sacrifice.py` | Donation recommendations: type, planet, day, recipient, timing |
| Relations | `lalkitab_relations_engine.py` | Conjunction yuti, clash/friendship classification |
| Saved Predictions | via routes | Prediction archive, feedback submission, accuracy rating |

---

### 2.19 Remedy Tracker

**Frontend:** `LalKitabRemedyTrackerTab.tsx`  
**Backend:** `app/models.py` (RemedyTracker model), routes

Per tracked remedy:
- Remedy ID, planet & house, start date, frequency (daily/weekly/monthly)
- Check-in history with adherence %
- Days since last check-in
- Calendar view of completed days

**Reversal Risk Assessment:** `GET /api/lalkitab/remedy-tracker/{id}/risk`
- Risk level: low / medium / high
- Risk reason (inconsistency, conflicting remedies, wrong timing)
- Mitigation steps

---

---

## 3. NUMEROLOGY — Numbers System

### What It Is

Astrorattan's Numerology module provides five complete calculators covering **Life Path**, **Mobile Number**, **Name**, **Vehicle**, and **House** numerology. Calculations draw from Pythagorean, Chaldean, and Vedic (Lo Shu) systems. All results are bilingual with master number (11, 22, 33) support throughout.

**Entry point:** `frontend/src/components/numerology/NumerologyTabs.tsx`  
**Primary backend:** `app/numerology_engine.py`, `app/numerology_forecast_engine.py`  
**API routes:** `app/routes/numerology.py`

---

### 3.1 Life Path Calculator

**Frontend:** `NumerologyTabs.tsx`  
**Backend:** `numerology_engine.py`  
**Endpoint:** `POST /api/numerology/calculate`

**Inputs:** Full name · Date of birth

#### Core Numbers

| Number | Source | Meaning |
|---|---|---|
| Life Path | Full birth date reduction | Life direction & soul purpose |
| Destiny (Expression) | Full name — Pythagorean | Natural talents & potential |
| Soul Urge | Vowels in name | Inner emotional desires |
| Personality | Consonants in name | How others perceive you |
| Birthday Number | Day of birth (01–31) | Key talent for this lifetime — 31 unique entries (each compound day 10–31 has distinct title/talent + Hindi); `birthday_reduced` fallback for lookup |
| Maturity Number | Life Path + Destiny | Evolved self (manifests after 40–50) — fields: title, title_hi, theme, theme_hi, description, description_hi, advice, advice_hi |

Master numbers 11, 22, 33 supported across all calculations.

#### Karmic Features

| Feature | Output |
|---|---|
| Karmic Debts | Number, source (life_path/destiny), title (EN/HI), meaning (EN/HI) |
| Hidden Passion | Most frequent Pythagorean number in name + meaning |
| Subconscious Self | Derived from present/absent numbers + missing_numbers array |
| Karmic Lessons | Missing digit interpretations with remedy, color, gemstone |

#### Predictions (per core number)
Each core number generates: theme · description · focus_areas · advice · lucky_months — all bilingual

#### Timing & Cycles

| System | Output |
|---|---|
| Pinnacles (4 periods) | Number, age range (period), prediction title (EN/HI) — each card shows green opportunity row (✦) + amber lesson row |
| Challenges (4 periods) | Number, age range, challenge nature (EN/HI) — each card shows green opportunity row + amber lesson row |
| Life Cycles (3 × 27 years) | Number, age range, cycle theme (EN/HI) |

---

### 3.2 Lo Shu Grid Analysis

**Frontend:** `NumerologyTabs.tsx` (grid section)  
**Backend:** `numerology_engine.py:_compute_loshu_grid()`, `analyze_loshu_arrows()`, `analyze_loshu_planes()`

**3×3 Magic Square:**
- Digit occurrence counts from DOB mapped to 1–9 grid positions
- Color coding: Green (strength arrows) · Red (weakness arrows) · Grey (absent) · Light gold (present)

**Arrows of Strength** (complete 3-digit patterns): Key · Name (EN/HI) · Meaning (EN/HI) · Digit trio

**Arrows of Weakness** (missing digit patterns): Key · Name (EN/HI) · Missing_meaning (EN/HI) · Digit trio

**Three Planes:**

| Plane | Digits | Measures |
|---|---|---|
| Mental | 3, 6, 9 | Intellectual strength |
| Emotional | 2, 5, 8 | Emotional depth |
| Practical | 1, 4, 7 | Material/physical grounding |

Per plane: score (0–3) · percentage · interpretation (EN/HI)

**Missing Numbers (enriched):** Number · meaning (EN/HI) · remedy (EN/HI) · color (EN/HI) · gemstone (EN/HI)

**Repeated Numbers:** Number · count · meaning (EN/HI)

---

### 3.3 Forecast Calculator

**Frontend:** `NumerologyTabs.tsx` (forecast section)  
**Backend:** `numerology_forecast_engine.py`  
**Endpoint:** `POST /api/numerology/forecast`

**Personal Forecast:**
- Personal Year (life-path + calendar year) — rendered fields: theme (EN/HI) · description (EN/HI) · focus_areas (EN/HI) · advice (EN/HI) · lucky_months (chips, e.g. Jan/Mar/Oct)
- Personal Month (personal year + calendar month) — theme + description displayed
- Personal Day (personal month + calendar day) — description displayed

**Universal Forecast:**
- Universal Year (sum of calendar year digits)
- Universal Month · Universal Day

**Lucky Month Chips:** Personal year `lucky_months` array rendered as month-name chips in the forecast card (fully wired)

---

### 3.4 Mobile Number Numerology

**Frontend:** `NumerologyTabs.tsx` (mobile section)  
**Backend:** `numerology_engine.py:calculate_mobile_numerology()`  
**Endpoint:** `POST /api/numerology/mobile`

**Inputs:** Phone number (with country code) · Name (optional) · DOB (optional) · Areas of struggle (Health/Relationship/Career/Money/Job checkboxes)

**Core Outputs:**
- Compound Number (raw digit sum)
- Mobile Total (reduced to 1–9, 11, 22, 33)
- Recommendation status: Highly Recommended / Not Recommended / Acceptable
- Good/Caution status badge (based on malefic digit pair detection)

**If DOB provided:**
- Life Path Number
- Recommended Totals (3–4 harmonizing numbers)
- Is-Recommended flag

**Prediction Profile:**
- Lucky Qualities (5 traits) · Challenges (3 weaknesses) · Best For · Compatibility Numbers

**Lucky & Unlucky Analysis:**
- Lucky Numbers (planetary friends) · Unlucky Numbers (planetary enemies) · Neutral Numbers
- Lucky Colors (3–4) · Unlucky Colors (2–3)

**Pair Combination Table:**
- Each consecutive digit pair classified: Benefic / Neutral / Malefic
- Summary: benefic_count, malefic_count, has_malefic

**Grids (if DOB provided):**
- Lo Shu Grid (3×3) with strength/weakness/absent indicators
- Vedic Grid (3×3, different layout from Lo Shu)
- Missing Numbers (enriched with remedy/color/gemstone)
- Repeated Numbers

**Affirmations (if areas of struggle provided):**
- Per area (health/relationship/career/money/job): 4–6 sentence empowerment statement

---

### 3.5 Name Numerology

**Frontend:** `numerology/NameNumerology.tsx`  
**Backend:** `numerology_engine.py:analyze_name_numerology()`  
**Endpoint:** `POST /api/numerology/name`

**Inputs:** Full name · Name type (full_name / first_name / last_name / business_name) · DOB (optional)

**Core Name Numbers (Pythagorean & Chaldean):**
- Pythagorean number (A=1…Z=8 repeating)
- Chaldean number (alternative ancient values)
- Soul Urge (vowels) · Personality (consonants)

**Primary Prediction Profile:**
- Title & ruling planet · Key Traits (5) · Career Guidance · Relationship insights · Health notes · Lucky Colors (3–4) · Lucky Days (2–3) · Spiritual Advice

**Name Parts Analysis:**
- First Name: extracted number + traits (up to 5)
- Last Name: extracted number + surname significance

**Life Path Compatibility (if DOB):**
- name_number + life_path + is_compatible + compatibility_note

**Letter Breakdown Table:**
- Per letter: Pythagorean value · Chaldean value · Type (Vowel/Consonant badge)

---

### 3.6 Vehicle Number Numerology

**Frontend:** `numerology/VehicleNumerology.tsx`  
**Backend:** `numerology_engine.py:calculate_vehicle_numerology()`  
**Endpoint:** `POST /api/numerology/vehicle`

**Inputs:** License plate number · Owner name (optional) · DOB (optional)

**Vibration Calculation:**
- Digits & letters extracted separately
- Vibration Number (reduced 1–9, 11, 22, 33)
- Letter value (A=1, B=2, etc.)

**Prediction Profile (fully bilingual via `pick()` helper — EN↔HI on language toggle):**
- energy / energy_hi · prediction / prediction_hi · driving_style / driving_style_hi
- best_for / best_for_hi · caution / caution_hi · lucky_directions / lucky_directions_hi

**Lucky Elements (bilingual):** vehicle_color / vehicle_color_hi (3–4 colors) · lucky_directions / lucky_directions_hi (compass)

**Digit Analysis:** Per digit in plate number → position + meaning

**Special Combinations:** Detected patterns: master_number / repeated_digit / ascending_sequence / descending_sequence + meaning

**Owner Compatibility (if DOB):** owner_life_path + vehicle_number + is_favorable + recommendation

---

### 3.7 House Number Numerology

**Frontend:** `numerology/HouseNumerology.tsx`  
**Backend:** `numerology_engine.py:calculate_house_numerology()`  
**Endpoint:** `POST /api/numerology/house`

**Inputs:** Full address · DOB (optional)

**House Energy Profile (per number 1–9, fully bilingual via `pick()` helper — EN↔HI on language toggle):**
- energy · prediction · best_for · family_life · career_impact · relationships · health · vastu_tip · lucky_colors — all fields have `*_hi` variants rendered

**Life Areas Impact (4 cards):** Family Life · Career Impact · Relationships · Health

**Street Name Analysis:** Name → numerology number → street influence

**Resident Compatibility (if DOB):** resident_life_path + house_number + is_ideal + compatibility_score (Excellent/Moderate/etc.) + recommendation

**Remedies & Enhancement:** 3–5 remedies + 3–5 enhancement tips (bilingual)

---

---

## 4. VASTU SHASTRA — Sacred Architecture System

### What It Is

Vastu Shastra is the ancient Indian science of architecture and spatial harmony. The Astrorattan implementation provides a complete analysis suite covering the 45-Devta Purusha Mandala, 32 entrance Pada quality ratings, room placement guidance for 10+ room types, a full remedial system (metals, colors, mantras), and an AI-powered floorplan analysis tool.

**Entry point:** `frontend/src/sections/VastuShastraPage.tsx`  
**Three modes:** Vastu Analysis (form-based) · My Home Grid (3×3 manual) · Floor Plan Upload (visual)  
**Primary backend:** `app/vastu/engine.py`, `app/vastu/data.py`, `app/vastu/floorplan.py`, `app/vastu/auto_detect.py`

---

### 4.1 Vastu Purusha Mandala — 45 Devtas

**Frontend:** `VastuMandalaTab.tsx`, `VastuMandalaGrid.tsx`  
**Backend:** `app/vastu/engine.py:calculate_mandala()`, `app/vastu/data.py:DEVTAS_45`

**Two Grid Types:**
- Residential/Commercial: Manduka Mandala (8×8 = 64 squares)
- Temple: Paramasayika Mandala (9×9 = 81 squares)

**45 Devtas across 10 Zones:**

| Zone | Direction |
|---|---|
| Central | Center (Brahma Sthana) |
| Northeast | NE |
| East | E |
| Southeast | SE |
| South | S |
| Southwest | SW |
| West | W |
| Northwest | NW |
| North | N |
| Special | Multiple positions |

**Per Devta Record (45 entries):**
- `id` (1–45, unique) · name (EN/HI) · zone (EN/HI) · direction (EN/HI)
- `element` (EN/HI): Ether / Water / Fire / Air / Earth
- `nature`: supreme / positive / neutral / negative / fierce
- `energy_type`: creative / ancestral / solar / harmonious / etc.
- `body_part` (EN/HI): anatomical correspondence
- `mantra`: Sanskrit activation mantra
- `desc_en` / `desc_hi`: detailed description
- `grid_positions`: list of (row, col) positions

**Interactive SVG Grid:**
- 9×9 cells, all 45 devtas color-coded by nature:
  - Supreme = amber · Positive = emerald · Neutral = blue · Negative = red · Fierce = orange
- Clickable cells show devta popup: name, description, element, direction, body part, mantra
- Dashed border highlights Brahma Sthana (center 3×3 zone)

**Energy Balance Output:**
- Positive / negative / neutral count
- Balance ratio & assessment (EN/HI)

**Vastu Purusha Body Mapping (9 body parts → directions):**
head → NE · face → E · chest → SE · navel → Center · arms → N/S · legs → SW/NW · feet → W

---

### 4.2 32 Entrance Padas

**Frontend:** `VastuEntranceTab.tsx`, `VastuCompass.tsx`  
**Backend:** `app/vastu/engine.py:analyze_entrance()`, `app/vastu/data.py:ENTRANCE_PADAS`

32 padas = 8 per cardinal direction (N, E, S, W), each spanning 11.25°

**Quality Scale:**

| Score | Quality | Meaning |
|---|---|---|
| 5/5 | SUPREME | Unlimited prosperity — ideal for all |
| 4/5 | EXCELLENT | Highly auspicious |
| 3/5 | GOOD | Favorable |
| 2/5 | NEUTRAL | Tolerable |
| 1/5 | CHALLENGE | Requires immediate remedies |

**Notable Padas:** N5 (Aditi) = SUPREME · S3 (Yama) = CHALLENGE · W8 = EXCELLENT

**Per Pada Record:**
- `pada` (code, e.g., "N5") · name (EN/HI) · direction · score (1–5)
- quality (EN/HI) · effects_en / effects_hi
- `suitable` (professions/activities list) · `avoid` list
- `devta` (ruling deity linking to DEVTAS_45)

**Interactive SVG Compass:**
- 8-point cardinal/intercardinal outer ring
- 32-pada inner ring (colored by score: 5=gold, 4=green, 3=blue, 2=orange, 1=red)
- Hoverable tooltips + clickable selection

**Pada Analysis Output:**
- Pada code & name · Quality badge · Score bar
- Effects description · Ruling Devta (name, mantra, description)
- All 8 padas in direction (grid view)
- Best & Worst pada in direction

**Entrance Remedies (score ≤ 2):**
- Metal strip · Color therapy · Mantra (ruling devta, 108× daily) · Yantra · Salt water

---

### 4.3 Room Placement Guidance

**Frontend:** `VastuRoomPlacementTab.tsx`  
**Backend:** `app/vastu/engine.py:get_room_placement()`, `app/vastu/data.py:ROOM_PLACEMENT`

**10 Room Types with ideal/acceptable/avoid direction mappings:**

| Room | Ideal Directions |
|---|---|
| Pooja Room | NE, N |
| Kitchen | SE |
| Master Bedroom | SW |
| Living Room | N, NE, E |
| Bathroom | NW, W |
| Staircase | S, SW, NW |
| Underground Water Tank | NE, N |
| Overhead Water Tank | SW, W |
| Study Room | NE, N, E |
| Children's Bedroom | NW, W |

Per room display: Room name (EN/HI) with emoji · Ideal directions (emerald) · Acceptable (blue) · Avoid (red) · Reason (EN/HI) · Tips (3+ per room, EN/HI)

---

### 4.4 Remedial System

**Frontend:** `VastuRemediesTab.tsx`  
**Backend:** `app/vastu/engine.py:suggest_remedies()`, `app/vastu/data.py`

**12 Recognized Problems:**
wealth · health · relationship · career · education · legal · sleep · conflict · fertility · depression · debt · accident

Each problem maps to 2–4 directional zones to strengthen and 2–3 devtas to appease.

#### A. Metal Strip Remedies
9 entries (N, NE, E, SE, S, SW, W, NW, Center):
- Metal name (EN/HI) · Purpose (EN/HI) · Placement instructions (EN/HI)
- Metals used: Copper, Silver, Iron, Gold, Bronze, Lead

#### B. Color Therapy
8 entries (8 cardinal/intercardinal directions):
- Colors list (EN/HI) · Element correspondence · Reasoning (EN/HI)

#### C. Mantras
Per devta: Devta name (EN/HI) · Mantra (Sanskrit) · Zone direction · Method (EN/HI) · Purpose (EN/HI)

#### D. Room Adjustments
Per problem → room-specific fix: Room name · Recommendation (relocate/redesign/reorient) · Reason (EN/HI) · Tips (3+, EN/HI)

#### E. General Vastu Remedies
Universal recommendations: Keep Brahma Sthana open · North-facing main door · Avoid round/oval rooms · Natural light/ventilation · North water feature

---

### 4.5 Home Layout Analysis

#### Grid Mode (3×3 Manual Assignment)
**Frontend:** `VastuHomeMapperTab.tsx`, `HomeGrid.tsx`

- 3×3 grid of 9 zones (NW/N/NE · W/Center/E · SW/S/SE)
- Click each zone to add/remove rooms (max 3 per zone)
- Compliance dots per room: ideal (green) / acceptable (blue) / avoid (red) / blocked (dark red)
- Center = Brahma Sthana — must remain empty or minimal
- LocalStorage persistence

#### Floorplan Mode (AI-Powered)
**Frontend:** `FloorplanUploader.tsx`, `FloorplanMapper.tsx`  
**Backend:** `app/vastu/floorplan.py`, `app/vastu/auto_detect.py`

**4-step flow:**
1. **Upload**: PNG/JPG/WebP, max 5MB → validation + optimization (JPEG 85% quality)
2. **North Rotation**: Set bearing (0–360°) for compass alignment
3. **Mark Rooms**: Click to place room markers (main_entrance, pooja, kitchen, bedrooms 1–6, bathrooms 1–3, study, staircase, tanks)
4. **Analyze**: Pixel coordinates → direction → compliance report

**Pixel-to-Direction Conversion:** `pixel_to_direction(x, y, width, height, north_rotation)`
- Normalize to center (0.0–1.0)
- Apply north rotation
- Map to 9-zone grid → returns N/NE/E/SE/S/SW/W/NW/Center

**AI Auto-Detection:** `auto_detect.py:auto_detect_rooms()`
- OCR (pytesseract): Extract room text labels
- YOLOv8 (if installed): Detect room bounding boxes
- OpenCV Contours: Find large rectangular regions
- Graceful degradation if models unavailable
- Output: detected_rooms with room_type, confidence, bbox_or_center

---

### 4.6 Home Compliance Report

**Frontend:** `HomeComplianceReport.tsx`  
**Backend:** `app/vastu/engine.py:analyze_home_layout()`

**Overall Score (0–100):**
- Base 70 + entrance bonus (0–5) − problem penalty (3 per issue)
- Bands: 80+ Excellent · 60–79 Good · 40–59 Moderate · < 40 Needs Work

**Report Structure:**
```
overall_score, overall_label (EN/HI)
total_rooms, ideal_count, acceptable_count, neutral_count, avoid_count
center_status: {is_open, rooms, assessment (EN/HI)}
room_results[]: {
  room_type, room_name (EN/HI), assigned_direction (EN/HI)
  compliance: ideal/acceptable/neutral/avoid/blocked
  score_contribution, ideal_directions, reason (EN/HI), tips (EN/HI)
  remedies (if non-compliant), zone_devtas[]
}
missing_critical_rooms[], duplicate_warnings[], direction_summary{}
```

**Brahma Sthana Hard Rules:**
- Kitchen / Bathroom / Staircase in Center = blocked (hard error)
- Other rooms in Center = soft caution

---

### 4.7 Complete Vastu Analysis

**Frontend:** `VastuShastraPage.tsx` → 5 result tabs  
**Backend:** `app/vastu/engine.py:get_complete_vastu_analysis()`

Five result tabs:
1. **My Home** — `VastuHomeMapperTab` (grid mode)
2. **45 Devtas** — `VastuMandalaTab` (mandala + energy balance + body mapping)
3. **Entrance** — `VastuEntranceTab` (pada analysis + compass + ruling devta)
4. **Remedies** — `VastuRemediesTab` (metal + color + mantras + room adjustments)
5. **Rooms** — `VastuRoomPlacementTab` (placement guide for all 10 room types)

---

### 4.8 Vastu API Summary

| Endpoint | Auth | Purpose |
|---|---|---|
| `GET /api/vastu/mandala` | ✗ | Mandala analysis, 45 devtas, energy balance |
| `GET /api/vastu/entrance` | ✗ | 32-pada entrance analysis |
| `GET /api/vastu/room-placement` | ✗ | Room placement guidance (all or specific) |
| `POST /api/vastu/analyze` | ✓ | Complete vastu analysis (all sub-analyses) |
| `POST /api/vastu/remedies` | ✓ | Remedy suggestions for problem list |
| `POST /api/vastu/home-layout` | ✓ | Home layout compliance from grid assignments |
| `POST /api/vastu/upload-floorplan` | ✓ | Floorplan image upload, validation, storage |
| `POST /api/vastu/analyze-floorplan` | ✓ | Floorplan room analysis, pixel-to-direction |
| `POST /api/vastu/auto-detect` | ✓ | AI room detection (OCR/YOLOv8/OpenCV) |

---

---

## 5. Cross-Feature Infrastructure

### Bilingual System
All four features deliver content in **English and Hindi** via:
- Backend fields named `*_en` / `*_hi` or plain + `*_hi` suffix pattern
- Frontend `useTranslation()` hook with language context (`en` / `hi`)
- Devanagari script throughout Hindi output

### Authentication & Roles
- JWT-based authentication
- Three roles: user · astrologer · admin
- Astrologers: access client management, extended analytics, dashboard
- Admin: user management, stats, live traffic panel

### Chart Visualization
- `KundliChartSVG.tsx` — SVG North Indian Diamond chart (reused across Kundli, LK, KP)
- `InteractiveKundli.tsx` — Interactive clickable chart (used in LK, KP, Varshphal)
- `VastuMandalaGrid.tsx` — 9×9 SVG devta grid (Vastu)
- `VastuCompass.tsx` — 32-pada SVG compass (Vastu)

### Swiss Ephemeris Integration
- Lahiri ayanamsa (sidereal zodiac) for all Vedic calculations
- Geocoding via Nominatim OpenStreetMap API
- Full historical DST & timezone support
- Accurate to arc-seconds for planetary positions

### Data Architecture
- **PostgreSQL** — kundlis, users, predictions, remedy trackers, journal entries
- **PDF Generation** — browser print-to-PDF (A4, serif typography)
- **Image Storage** — `/static/uploads/vastu/` for floorplan files
- **AI Models** — YOLOv8n.pt for room detection in floorplan mode

---

## 6. PANCHANG (Hindu Almanac)

**File:** `frontend/src/sections/Panchang.tsx` (main section, tab navigation, GSAP animations, location + date selectors)  
**Backend routes:** `app/routes/panchang.py`, `app/routes/muhurat.py`  
**Backend engines:** 13 specialized Python modules (see §6.3)

### 6.1 Daily Panchang Core (PanchangCoreTab)
**API:** `GET /api/panchang?date&latitude&longitude&lang`  
**File:** `frontend/src/components/panchang/PanchangCoreTab.tsx`

| Output | Detail |
|--------|--------|
| **Tithi** | Name, Number (1-30), Paksha (Shukla/Krishna), End Time, Type badge (Nanda/Bhadra/Jaya/Rikta/Poorna), Lord, Phala |
| **Nakshatra** | Name, Pada (1-4), Lord, End Time, Category badge (Sthira/Chara/Ugra/Mishra/Laghu/Mridu/Tikshna), Deity |
| **Yoga** | Name, Number (1-27), End Time, Quality badge (Shubha / Yoga Dosha) |
| **Karana** | Name, Number (1-60), End Time, Type badge (Sthira/Chara/Vishti) |
| **Sun & Moon** | Sunrise, Sunset, Moonrise, Moonset |
| **Day/Night duration** | Dinamana, Ratrimana, Madhyahna (mid-day) |
| **Weekday** | Vaar name, Graha Swami (planet lord) |
| **Special banners** | Dagdha Tithi warning, Kula Yoga indicator, Best Hora for Travel |
| **Panchanga Shuddhi Score** | Percentage + Grade (Shubha / Madhyama / Ashubha) |

### 6.2 Muhurat Tab (MuhuratTab)
**File:** `frontend/src/components/panchang/MuhuratTab.tsx`

| Output | Detail |
|--------|--------|
| **Hard block banners** | Vyatipata / Vaidhriti Yoga (all-activity-blocked), Chaturmasa warning |
| **Prominent Yoga banners** | Amrit Siddhi, Sarvartha Siddhi, Dwipushkar, Tripushkar, Ganda Moola active status |
| **Auspicious periods** | Brahma Muhurat, Abhijit Muhurat, Vijaya Muhurta, Godhuli Muhurta, Nishita Muhurta |
| **Inauspicious periods** | Rahu Kaal (live "Active Now" + minutes remaining), Gulika Kaal, Yamaganda, Dur Muhurtam, Varjyam |
| **Special Yogas** | Ravi Yoga, Amrit Siddhi, Sarvartha Siddhi, Tripushkar, Dwipushkar |
| **Sandhya Times** | Pratah Sandhya, Sayahna Sandhya (for Gayatri recitation) |
| **4-column grid** | Anandadi Yoga, Disha Shool + travel warning, Lucky Color/Number/Direction, Ekadashi Parana window |
| **Panchaka Rahita** | Type (Mrityu/Agni/Chora/Roga/Raja), severity, safe/unsafe windows |
| **Tamil Yoga** | Tamil Yoga name + auspicious flag, Jeevanama, Netrama |
| **Nivas & Vasa** | Chandra Vasa, Rahu Vasa + caution, Shivavasa, Agnivasa, Homahuti, Kumbha Chakra |
| **Vrats & Fasting** | Filtered list with type, name, description |
| **Festivals Today** | Non-fasting festival tags with icons |

### 6.3 Muhurat Finder (MuhuratFinderTab)
**API:** `GET /api/muhurat/activities`, `GET /api/muhurat/finder`, `GET /api/muhurat/travel`  
**File:** `frontend/src/components/panchang/MuhuratFinderTab.tsx`

- **20+ activities:** Marriage, Griha Pravesh, Vehicle Purchase, Business Start, Shop Opening, Thread Ceremony, Naming Ceremony, Education Start, etc.
- **Month picker** with previous/next navigation
- **Personal Muhurat** collapsible toggle: birth nakshatra (27 options) + birth moon rashi (12 options) for Chandra Balam / Tara Balam scoring
- **Per-date output:** Muhurat Score (0-100), Tithi/Nakshatra/Paksha tags, Sunrise/Sunset/Rahu Kaal, Lagna Windows (sign, time, Ganda/Sandhi warnings, safe sub-window), Chandra Balam (house + favorable), Tara Balam (tara name + favorable), Reasons good/bad (bulleted)
- **Marriage-specific:** Best Lagna + Lord, Lagna Quality Score, Vivaha Quality (0-100), Marriage Season Calendar (allowed months green / forbidden months red)
- **Business-specific:** Recommended Hora Windows (planet lord + time range)
- **Activity rules:** Tithi, Nakshatra, Weekday, Lagna preferences; avoidance of Rahu Kaal, Bhadra, Panchaka, Ganda Moola, Sankranti, Guru/Shukra Asta, Dagdha Tithi

### 6.4 Sankranti Tab (SankrantiTab)
**API:** `GET /api/panchang/sankranti?year&latitude&longitude`  
**File:** `frontend/src/components/panchang/SankrantiTab.tsx`  
**Engine:** `app/sankranti_engine.py:build_sankranti_payload()`

- **Annual Sun Ingress Calendar:** 12 rashi ingress times (local + UTC), restriction window (±16 hours), Amritkaal window (minutes), Ayana (Uttarayana/Dakshinayana), Makar special (Magha Mela context), sign effects interpretation
- **Year navigation:** 1900–2100 range

### 6.5 Planetary Positions Tab (PlanetaryPositionsTab)
**File:** `frontend/src/components/panchang/PlanetaryPositionsTab.tsx`

- 9-planet table: Sign (Rashi) + Hindi, Nakshatra + Pada, Degree, Longitude, Retrograde flag (R in red), Combusted flag (🔥)
- Row tinting: retrograde = red-tinted, combusted = orange-tinted

### 6.6 Hora Tab (HoraTab)
**File:** `frontend/src/components/panchang/HoraTab.tsx`

- Current Hora banner (planet lord, time window, quality badge)
- Day/Night Hora tables (24 periods): planet ruler, best-for guidance, time window, result quality
- Live status: current hora highlighted

### 6.7 Lagna Tab (LagnaTab)
**File:** `frontend/src/components/panchang/LagnaTab.tsx`

- 24-hour lagna cycle table: rising sign, degree, start/end time, Ganda/Sandhi badges
- Current lagna highlight card: Pushkara Navamsha badge if applicable
- Ganda/Sandhi warning banner if present

### 6.8 Choghadiya Tab (ChoghadiyaTab)
**File:** `frontend/src/components/panchang/ChoghadiyaTab.tsx`

- Day + Night tables: 7 period types (Amrit/Shubh/Labh/Char/Udveg/Kaal/Rog), quality color-coding, time windows
- Vaar Vela / Kaal Vela / Kaal Ratri sub-period indicators
- Color-coded legend + Vela legends

### 6.9 Tara & Chandra Balam Tab (TarabalamTab)
**File:** `frontend/src/components/panchang/TarabalamTab.tsx`

- **Tarabalam table:** Nakshatra, Tara number, interpretation, Good/Bad badge
- **Chandrabalam table:** Rashi, Ashtama house warning badge, strength indicator, Good/Bad badge

### 6.10 Hindu Calendar Tab (CalendarTab + HinduCalendarTab)
**API:** `GET /api/panchang/month`, `GET /api/festivals`  
**Files:** `CalendarTab.tsx` (overview cards), `HinduCalendarTab.tsx` (full monthly grid)

- **Overview cards:** Vikram Samvat, Shaka Samvat, Maas (month + deity), Paksha, Ritu (season), Ayana
- **Full monthly calendar (Drik Panchang style):**
  - 7-column weekday grid, cells 130–150px
  - Per-cell: Tithi + Paksha, moon phase emoji, date number, sunrise/sunset, moonrise/moonset, festival name (red), vrat name (purple), nakshatra
  - Left detail panel: all panchang elements, inauspicious/auspicious periods, special yogas, lucky indicators
  - Click lightbox: expandable sections for Sun/Moon, Hindu Calendar, Panchang Elements, Signs, Muhurat, Festivals
- **Festivals grid:** 3-column with date, festival name, weekday

### 6.11 Gowri Panchang Tab (GowriTab)
**File:** `frontend/src/components/panchang/GowriTab.tsx`

- Day + Night tables: 8 period types (Amruta/Labha/Shubha/Kaal/Udvega/Chara/Dhanada), quality badges, time windows
- Current Gowri banner with live status

### 6.12 Advanced Tab (AdvancedTab)
**File:** `frontend/src/components/panchang/AdvancedTab.tsx`

- **Mantri Mandala:** 9 planetary cabinet roles (PM/Minister/General/Treasurer/etc.) with significance
- **Astronomical epoch data:** Kaliyuga year, Kali Ahargana, Julian Day, Modified Julian Day, Rata Die, Ayanamsha (Lahiri °)
- **Do-Ghati Muhurtas:** 30 daily muhurtas (3-column grid): name, time window, quality badge

### 6.13 Festivals Tab (FestivalsTab)
**File:** `frontend/src/components/panchang/FestivalsTab.tsx`

- Today's festivals/vrats with icon (🔥 fast, 🪔 festival, 🪴 observance), type badge, description, rituals
- Panchak status (Active/Inactive) + Ganda Moola status cards

### 6.14 Today's Insights Component (TodaysInsights)
**File:** `frontend/src/components/panchang/TodaysInsights.tsx`

- Insight cards: Festival 🎊, Auspicious Muhurat ✨, Time to Avoid ⚠️, Special Yoga 🔥, Ganda Moola alert ⚡
- Transitions timeline: Next Tithi/Nakshatra/Yoga end with countdown
- CTA to kundli/prediction integration

### 6.15 Backend Engines

| Engine | File | Key Functions |
|--------|------|--------------|
| **Core Panchang** | `panchang_engine.py` | `calculate_panchang()` — tithi, nakshatra, yoga, karana, sunrise/sunset, rahu kaal, abhijit, brahma muhurat, planetary positions, choghadiya |
| **Muhurat Rules** | `muhurat_rules.py` | `get_all_activities()` — 20+ activity definitions with favorable/unfavorable rule sets |
| **Muhurat Finder** | `muhurat_finder.py` | `find_muhurat_dates()`, `find_travel_muhurat()` — date ranking by Chandra/Tara Balam, lagna windows |
| **Sankranti** | `sankranti_engine.py` | `build_sankranti_payload()` — 12 sun ingress times + restriction windows + amritkaal |
| **Festival** | `festival_engine.py` | `detect_festivals()` — tithi-based, nakshatra-based, maas-based, Gregorian fixed |
| **Special Yogas** | `panchang_yogas.py` | Sarvartha Siddhi, Amrit Siddhi, Dwipushkar/Tripushkar, Ganda Moola, Kula Yoga |
| **Directions** | `panchang_directions.py` | Disha Shool, Anandadi Yoga, Lucky Color/Number/Direction |
| **Ekadashi** | `panchang_ekadashi.py` | Ekadashi Parana window + fasting end time |
| **Nivas** | `panchang_nivas.py` | Chandra Vasa, Rahu Vasa, Shivavasa, Agnivasa, Homahuti, Kumbha Chakra |
| **Tamil Yoga** | `panchang_tamil.py` | Tamil Yoga, Jeevanama, Netrama |
| **Samvat** | `panchang_samvat.py` | Vikram/Shaka/Brihaspati/Gujarati Samvat, Purnimant/Amant, Pushkara Navamsha |
| **Miscellaneous** | `panchang_misc.py` | Mantri Mandala, astronomical epochs, Panchaka Rahita, Chaturmasa, Dagdha Nakshatra |

### 6.16 API Endpoints

| Endpoint | Method | Key Params | Purpose |
|----------|--------|-----------|---------|
| `/api/panchang` | GET | `date`, `latitude`, `longitude`, `lang` | Full daily panchang calculation |
| `/api/panchang/sankranti` | GET | `year`, `latitude`, `longitude` | Annual sun ingress calendar |
| `/api/panchang/month` | GET | `month`, `year`, `latitude`, `longitude`, `lang` | Monthly panchang summaries for calendar grid |
| `/api/festivals` | GET | `year`, `month`, `lang` | Festival list for calendar enrichment |
| `/api/muhurat/activities` | GET | `lang` | Activity list for muhurat finder |
| `/api/muhurat/finder` | GET | `activity`, `month`, `year`, `latitude`, `longitude`, `limit`, `birth_moon_rashi`, `birth_nakshatra` | Ranked auspicious dates for activity |
| `/api/muhurat/travel` | GET | `direction`, `month`, `year`, `latitude`, `longitude`, `limit` | Travel-specific muhurat dates |

### 6.17 Real-Time Features
- Rahu Kaal live status ("Active Now" + minutes remaining)
- Current Hora / Lagna / Choghadiya / Gowri period highlighted dynamically (per-minute tick)
- Tithi/Nakshatra/Yoga transition countdown timers

---

## 7. HOROSCOPE (Sun-Sign Predictions)

**File:** `frontend/src/sections/HoroscopePage.tsx` (main page, tab orchestration, sign selector, date picker, live clock)  
**Backend routes:** `app/routes/horoscope.py` (7 endpoints)  
**Backend engines:** `app/transit_engine.py`, `app/transit_lucky.py`, `app/transit_interpretations.py`, `app/horoscope_generator.py`

### 7.1 Tabs & Time Horizons

| Tab | Component | API | Extra Sections |
|-----|-----------|-----|---------------|
| **Daily** | `DailyTab.tsx` | `GET /api/horoscope/daily?sign&date&lang` | — |
| **Tomorrow** | `DailyTab.tsx` (reused) | `GET /api/horoscope/tomorrow?sign&lang` | — |
| **Weekly** | `WeeklyTab.tsx` | `GET /api/horoscope/weekly?sign&lang` | Week date range |
| **Monthly** | `MonthlyTab.tsx` | `GET /api/horoscope/monthly?sign&lang` | Phase Breakdown (3 cards) + Key Dates (sign changes) |
| **Yearly** | `YearlyTab.tsx` | `GET /api/horoscope/yearly?sign&lang` | Annual Theme banner + Quarter Breakdown (4 cards) + Best Months grid |
| **All Signs** | `AllSignsTab.tsx` | `GET /api/horoscope/all?period&date` | 12-sign summary grid |
| **Transit Insights** | `TransitInsightsTab.tsx` | `GET /api/horoscope/transits` | Planet positions + sign-wise dignity table |

### 7.2 Per-Prediction Output (Daily/Weekly/Monthly/Yearly)

| Section | Detail |
|---------|--------|
| **Sign Metadata Card** | Sign name (EN + HI), emoji, date range, ruling planet, element |
| **Score Card** | 5 horizontal bars (1-10): Overall, Love, Career, Finance, Health |
| **Active Dasha Period** | Shown when birth data provided — displays active Mahadasha / Antardasha (bilingual: "Sun Mahadasha / Moon Antardasha") |
| **Mood Indicator** | Bilingual (Challenging / Balanced / Optimistic) |
| **Lucky Metadata** | Lucky Number, Color, Time, Compatible Sign, Gemstone (metal/finger/day), Mantra |
| **5 Prediction Sections** | General Outlook, Love, Career, Finance, Health — grid layout, bilingual text |
| **Dos & Don'ts** | 2-column panel: green Dos list + red Don'ts list (2-5 items each) |

**Monthly extras:** Phase Breakdown (1st–10th, 11th–20th, 21st–end with scores), Key Dates (planet sign-change events with date + bilingual description)  
**Yearly extras:** Annual Theme banner, Quarter Breakdown (Q1–Q4 with theme, best_area, score), Best Months grid (Love/Career/Finance/Health × 2 months)

### 7.3 All Signs Tab (AllSignsTab)
- 12-sign clickable card grid (3 cols mobile → 12 cols desktop)
- Per card: zodiac image, sign name (EN+HI), date range, element badge (Fire/Earth/Air/Water), 160-char general preview
- On click: switches to Daily tab for full reading

### 7.4 Transit Insights Tab (TransitInsightsTab)
**API:** `GET /api/horoscope/transits`

- **Left panel:** 9-planet current positions table (Planet → Current Sign, bilingual)
- **Right panel:** 12-sign effects table (Sign, Ruler, Ruler In, Dignity, Strength badge: very_strong/strong/moderate/weak)

### 7.5 Shared UI Components

| Component | File | Purpose |
|-----------|------|---------|
| `ScoreBar` | `ScoreBar.tsx` | Label + filled progress bar (0-100%) + "N/10" text |
| `LuckyMetadataCard` | `LuckyMetadataCard.tsx` | 6-item icon grid: number/color/time/compatible/gemstone/mantra |
| `DosAndDonts` | `DosAndDonts.tsx` | Two-column green/red cards with check/X icons |

### 7.6 Zodiac Sign Support (All 12)

| Sign | Hindi | Dates | Ruling Planet | Element |
|------|-------|-------|---------------|---------|
| Aries ♈ | मेष | Mar 21–Apr 19 | Mars | Fire |
| Taurus ♉ | वृषभ | Apr 20–May 20 | Venus | Earth |
| Gemini ♊ | मिथुन | May 21–Jun 20 | Mercury | Air |
| Cancer ♋ | कर्क | Jun 21–Jul 22 | Moon | Water |
| Leo ♌ | सिंह | Jul 23–Aug 22 | Sun | Fire |
| Virgo ♍ | कन्या | Aug 23–Sep 22 | Mercury | Earth |
| Libra ♎ | तुला | Sep 23–Oct 22 | Venus | Air |
| Scorpio ♏ | वृश्चिक | Oct 23–Nov 21 | Mars | Water |
| Sagittarius ♐ | धनु | Nov 22–Dec 21 | Jupiter | Fire |
| Capricorn ♑ | मकर | Dec 22–Jan 19 | Saturn | Earth |
| Aquarius ♒ | कुंभ | Jan 20–Feb 18 | Saturn | Air |
| Pisces ♓ | मीन | Feb 19–Mar 20 | Jupiter | Water |

### 7.7 Backend Engines

#### Transit Engine (`app/transit_engine.py` — 1394 lines)
Primary horoscope generator using real Swiss Ephemeris data.

| Function | Purpose |
|----------|---------|
| `get_full_transits(date)` | Planetary positions at Delhi 12:00 IST via ephemeris |
| `calculate_transit_houses(sign, planet_data)` | Maps 9 planets to houses 1-12 from native sign |
| `get_planet_dignity(planet, info)` | Classifies: exalted / debilitated / own_sign / retrograde / combust / neutral |
| `assemble_section(sign, area, houses, data, period, lang, fragment_offset, dasha_lord)` | Combines fragments from TRANSIT_FRAGMENTS matrix; `dasha_lord` doubles that planet's weight |
| `compute_scores(sign, houses, data)` | Generates 1-10 scores for overall + 4 areas (weighted house + dignity + planet nature) |
| `generate_transit_horoscope(sign, period, date, native_lagna, dasha_lord)` | **Master function** — orchestrates full horoscope dict; dasha-aware when `dasha_lord` set |
| `generate_monthly_extras(sign, date)` | 3-phase breakdown + key planet sign-change dates |
| `generate_yearly_extras(sign, year)` | Quarters + best months + annual theme via quarterly sampling |

**Key constants:** `EXALTED_SIGNS`, `DEBILITATED_SIGNS`, `OWN_SIGNS`, `PERIOD_WEIGHTS` (Moon 5× for daily), `FRAGMENT_COUNTS` (Daily=3, Weekly=3, Monthly=4, Yearly=5)

**Route helpers (`app/routes/horoscope.py`):**
- `_resolve_birth_nakshatra(birth_date, birth_time, birth_lat, birth_lon, birth_tz)` — computes natal Moon nakshatra from ephemeris (required for Dasha calculation)
- `_resolve_active_dasha(birth_nakshatra, birth_date)` — returns `{mahadasha, antardasha}` for today; returns `None` if birth data incomplete

**Dasha-aware personalization:** When birth data is provided, all 5 route handlers (daily/tomorrow/weekly/monthly/yearly) compute the active Mahadasha lord and pass it as `dasha_lord` to `generate_transit_horoscope()`. This doubles the active lord's fragment weight in `assemble_section()`, so two users with the same Moon sign but different birth years receive different readings (different dasha periods).

**Variant generation scripts:**
- `scripts/generate_transit_variants.py` — generates 4 variant fragments per slot (9 planets × 12 houses = 108 slots; 4 variants × 5 areas × 2 langs = 4320 fragments total) via qwen3.5:27b on Ollama; outputs `app/transit_variants.py`; single-worker, fully resumable via `.claude/debug/transit_variants_progress.json`
- `scripts/watch_variants.py` — terminal monitor for generation progress; per-planet grid (■=done ·=pending), overall progress bar with ETA, recent activity log; refreshes every 10s
- `app/transit_variants.py` — generated output; `_lookup_fragment()` in transit_engine uses this first (random variant selection) with fallback to `TRANSIT_FRAGMENTS`

**Scoring algorithm:**
1. Per planet: `house_score` (benefic 1/5/9/10/11 = +2/+3/+3/+2/+3; malefic 6/8/12 = -1/-2/-2) + `planet_nature` (Jupiter=+1.5 … Saturn=-1.0, Rahu/Ketu=-0.7) + `dignity_bonus` (exalted=+2, own=+1, debil=-2, combust=-1)
2. Sum across 9 planets → normalize to 1-10 scale

#### Lucky Metadata Module (`app/transit_lucky.py`)

| Derivation | Source |
|-----------|--------|
| Lucky Number | Moon nakshatra index mod 9 |
| Lucky Color | Sign element + moon pada (4-color palette per element) |
| Lucky Time | 12-slot cycle keyed to sign index |
| Compatible Sign | Trine (same element) or strongest dignified planet's sign |
| Gemstone | Ruling planet lookup (Ruby/Pearl/Red Coral/Emerald/Yellow Sapphire/Diamond/Blue Sapphire/Hessonite/Cat's Eye) |
| Mantra | Sanskrit planetary mantra per ruling planet |
| Mood | Overall score: 1-3=Challenging, 4-6=Balanced, 7-10=Optimistic |
| Dos | Benefic houses (1,5,9,10,11) + strong planet guidance |
| Don'ts | Malefic houses (6,8,12) + weak planet cautions |

#### Interpretation Matrix (`app/transit_interpretations.py` — >500KB)
`TRANSIT_FRAGMENTS[planet][house][area][language]` + `DIGNITY_MODIFIERS[dignity]` — fragment library consumed by `assemble_section()`.

#### Horoscope Generator / Fallback (`app/horoscope_generator.py`)
- `generate_ai_horoscope()`: tries transit_engine → falls back to DB → falls back to template pools
- `generate_daily_horoscopes()`: batch cron for all 12 signs
- `seed_weekly_horoscopes()`: seeded at application startup
- Template pools: `_CAREER`, `_LOVE`, `_HEALTH`, `_SPIRITUAL`, `_CHALLENGES` (6 templates each)

### 7.8 API Endpoints

| Endpoint | Method | Key Params | Returns |
|----------|--------|-----------|---------|
| `/api/horoscope/daily` | GET | `sign*`, `date`, `lang` | sections, scores, mood, lucky, dos/donts, active_dasha |
| `/api/horoscope/tomorrow` | GET | `sign*`, `lang` | same shape as daily, date = today+1 |
| `/api/horoscope/weekly` | GET | `sign*`, `lang` | + week_start, week_end |
| `/api/horoscope/monthly` | GET | `sign*`, `lang` | + phases[], key_dates[] |
| `/api/horoscope/yearly` | GET | `sign*`, `lang` | + quarters[], best_months{}, annual_theme{} |
| `/api/horoscope/all` | GET | `period*`, `date` | 12-sign summary list |
| `/api/horoscope/transits` | GET | — | transits[] (9 planets) + sign_effects[] (12 signs) |

### 7.9 Data Flow
```
HoroscopePage → /api/horoscope/{period}?sign=...&birth_date=...&birth_lat=...
  → horoscope.py route handler
      → _resolve_birth_nakshatra()  [if birth data present]
      → _resolve_active_dasha()     [if nakshatra resolved]
      → transit_engine.generate_transit_horoscope(sign, period, date,
                                                   native_lagna, dasha_lord)
          → get_full_transits() [Swiss Ephemeris @ Delhi]
          → calculate_transit_houses()
          → assemble_section() × 5
              → _lookup_fragment()  [tries TRANSIT_VARIANTS first, falls back to TRANSIT_FRAGMENTS]
              → dasha_lord weight × 2 if active dasha set
          → compute_scores()
          → get_all_lucky_metadata() [transit_lucky.py]
  → response includes: active_dasha {mahadasha, antardasha}
  → fallback: horoscopes DB table
  → fallback: horoscope_generator.generate_ai_horoscope() [templates]
```

### 7.10 Bilingual Support
- All section text stored as `{"en": "...", "hi": "..."}` — assembled by transit engine
- All metadata fields (color, time, compatible sign, gemstone, mood) have EN + HI variants
- Frontend: `useTranslation()` hook + `txt()` helper for language switching per tab
- Backend: `lang` query param (defaults to `"en"`)

---

*Blueprint generated from codebase implementation — April 19, 2026.*  
*Every feature listed exists in production code at `project_28_astro_app/`.*
