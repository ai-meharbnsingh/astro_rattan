# Astro App Blueprint (Based on Lalkitaab PDFs + Internet Research)

## 1) What I reviewed

### Local PDFs parsed
1. `Book of Nishaniya 20 (1).pdf` (193 pages)
2. `Nazm E Jyotish 2020 .pdf` (547 pages)
3. `Nishaniya (1).pdf` (555 pages)
4. `Nishaniya hi Nishaniya.pdf` (101 pages)
5. `ग्रहो_की_निशानिया_3rd_Edition_.pdf` (380 pages)

### Key extracted structure from PDFs
- `Book of Nishaniya 20`: clear 9-planet x 12-house structure (Jupiter, Sun, Moon, Venus, Mars, Mercury, Saturn, Rahu, Ketu) + rapid-fire + one-planet nishaniyan.
- `Nishaniya (1)`: repeated pattern per placement: `प्रभाव` (effects), `निशानियां` (observable signs), `उपाय` (remedies).
- `Nishaniya hi Nishaniya`: strong table-style rulebook including one/two/three-planet signs and transit (`गोचर`) cues; extracted numbered entries go up to around **617**.
- `Nishaniya hi Nishaniya`: explicit chapter segments for `Chandra Chalana` and `Gochar Ke Formula`; note says transit table in this book focuses especially on Sun and Mercury formulas.
- `ग्रहो_की_निशानिया_3rd_Edition_`: method philosophy: conjunctions are not always interpreted naively; importance of observed signs over assumption; remedy should target the planet whose signs are actually manifest.
- `Nazm E Jyotish`: mostly poetic/interpretive content and practitioner philosophy; useful for tone and explanatory content, less useful as direct deterministic calculation reference.

---

## 2) Product goal for your app

Build a **Lalkitaab-first predictive assistant** where:
1. User enters birth details + current life observations.
2. App computes chart/transit/varshfal.
3. App matches `निशानियां` from your books.
4. App outputs predictions + confidence + remedies + tracking.

This should not be a generic astrology app. It should be a **structured nishaniyan decision system**.

---

## 3) Recommended app tabs (final information architecture)

## Tab A: Onboarding & Birth Data
**Purpose:** collect required inputs with validation.

**Inputs:**
- Name (optional)
- Date of birth
- Exact time of birth (with confidence: exact/approx/unknown)
- Place of birth (lat/lon + timezone)
- Gender (optional, if needed for legacy rules)
- Current residence (optional for local sunrise calculations)

**Outputs:**
- Stored profile
- Birth-data quality score
- Warning if time uncertain (prediction confidence reduced)

---

## Tab B: Chart Engine (Lagna / Rashi core)
**Purpose:** base computational chart layer.

**Outputs:**
- Planet longitudes (sidereal)
- House placements (1..12)
- Lagna sign/degree
- Retrograde flags
- Combustion flags
- Planet dignity (optional)
- Chart wheel + table view

**Advanced outputs:**
- House lordships
- Planet clusters (same house)
- adjacency influence tags (for shared-wall style logic inspired by your PDF method)

---

## Tab C: Nishaniyan Matcher (Core USP)
**Purpose:** convert chart state -> likely real-world observable signs.

**Inputs:**
- Computed chart state
- Optional user observations checklist (house clues, family events, body markers, behavior, recurring patterns)

**Outputs:**
- Ranked `observed-sign hypotheses`
- Matching rules with references (book + entry id)
- Strength score per rule
- Contradiction flags (rules that conflict)

**Why this tab is critical:** this is where your books become a scalable product.

---

## Tab D: Transit (Gochar) Diagnostics
**Purpose:** short-term event triggers from transit overlays.

**Outputs:**
- Current transit chart and next 30/90 day transit timeline
- Transit-over-natal house mapping
- Rapid daily clues (behavior, events, household signals)
- Alert cards (e.g., “high conflict window”, “health caution window”, “money caution window”)

**PDF alignment:** `Nishaniya hi Nishaniya` includes explicit gochar-style practical cues; integrate as “daily lived markers”.

---

## Tab E: Varshfal (Annual Layer)
**Purpose:** year-specific trend model.

**Outputs:**
- Year chart summary
- Top 5 opportunities
- Top 5 caution areas
- Monthly emphasis heatmap
- Year-vs-natal consistency score

---

## Tab F: Prediction Studio
**Purpose:** user-facing, readable predictions.

**Sections in output:**
- Career/work
- Money/cashflow risk
- Relationship/marriage
- Family/home
- Health caution (non-medical disclaimer)
- Travel/relocation
- Legal/conflict risk
- Spiritual/discipline growth

**Each prediction card must show:**
- `What is likely`
- `Why` (rule trace)
- `When` (window)
- `Confidence` (0-100)
- `What to do` (practical steps/remedy)

---

## Tab G: Remedies Planner (उपाय)
**Purpose:** action scheduling + compliance tracking.

**Outputs:**
- Remedy list tied to active negative signatures
- Start date / duration / frequency
- Contraindications (if remedy conflicts with another)
- Completion tracker
- Effect journal (“before-after”)

**Rules from your PDFs to encode:**
- Use remedy of the planet whose signs are actually visible.
- If multiple planets implicated, rank by evidence score.
- Tag remedies by severity and reversibility.

---

## Tab H: Chandra Chalana Module
**Purpose:** operational protocol from your source text.

**Outputs:**
- 43-day tracker plan
- Day-wise action checklist
- Missed-day restart logic
- Mood/stability journaling

---

## Tab I: Ask-Astrologer AI (Explainer)
**Purpose:** conversational explanation grounded in rule trace.

**Outputs:**
- “Explain this prediction in simple Hindi/English”
- “Which exact rules triggered this?”
- “What changed vs last month?”

**Important:** AI should not invent. Must cite rule IDs from your database.

---

## Tab J: History, Accuracy, and Learning
**Purpose:** make system measurable.

**Outputs:**
- Past predictions log
- User outcome marking (happened / partial / no)
- Rule hit-rate per category
- Confidence calibration chart

This is essential to improve model reliability over time.

---

## 4) Prediction output types you can generate

1. **Static personality baseline** (from natal house-planet map)
2. **Observable household clues** (nishaniyan style)
3. **Near-term transit clues** (1-30 days)
4. **Quarterly risk windows**
5. **Annual trend (varshfal)**
6. **Event likelihood categories** (career move, conflict, health caution, travel)
7. **Remedy urgency bucket** (low/medium/high)
8. **Contradiction-based uncertainty output** (when rules disagree)
9. **Data-quality-aware prediction** (time uncertainty changes precision)

---

## 5) Calculations to implement (technical)

## A. Astronomy and time calculations
1. Gregorian datetime -> Julian Day (UT)
2. Accurate timezone + DST conversion
3. Geolocation to lat/lon
4. Planetary longitudes using ephemeris
5. Sidereal conversion with chosen ayanamsha
6. House cusps and Lagna
7. Transit positions by date range
8. Solar return / annual constructs for varshfal workflows

## B. Astrology rule calculations
1. Planet in house (1..12)
2. Multi-planet conjunction groups
3. Neighbor/adjacent-house influence score (as per your research concept)
4. Benefic/malefic condition flags per your custom rule table
5. One-planet nishaniyan match score
6. Two-planet nishaniyan match score
7. Three-planet nishaniyan match score
8. Gochar-trigger score
9. Varshfal reinforcement score
10. Final weighted confidence score

## C. Evidence scoring formula (recommended)
Use weighted scoring so app is transparent:

`FinalScore = 0.40*NatalRule + 0.25*ObservedNishaniyan + 0.20*TransitSupport + 0.10*VarshfalSupport + 0.05*DataQuality`

Then map score:
- 80-100: High confidence
- 60-79: Moderate
- 40-59: Low
- <40: Speculative

---

## 6) Data model you should create

## Core tables
- `users`
- `birth_profiles`
- `planet_positions`
- `house_positions`
- `transits`
- `varshfal_snapshots`

## Knowledge tables (from PDFs)
- `rules_one_planet`
- `rules_two_planet`
- `rules_three_planet`
- `rules_transit`
- `rules_chandra_chalana`
- `remedies`
- `rule_sources` (book, page, entry)

## Runtime tables
- `rule_matches`
- `predictions`
- `remedy_plans`
- `user_feedback`
- `prediction_outcomes`

---

## 7) Rule ingestion strategy from your PDFs

1. OCR-clean and normalize Hindi text.
2. Split into atomic rule records:
   - Condition (e.g., Sun+Mercury in X)
   - Observable sign
   - Effect/prediction
   - Remedy
   - Context tag (natal/gochar/varshfal)
3. Assign each rule a stable `rule_id`.
4. Add severity tags: `advisory`, `caution`, `high-risk`.
5. Add sensitive-content tags (medical/sexual/legal) for safe display controls.

---

## 8) Safety and policy layer (must-have)

Your source includes strong claims (health, death, pregnancy, legal, sexuality). For production:

1. Add explicit disclaimer: spiritual guidance, not medical/legal diagnosis.
2. For medical flags, show “consult licensed professional”.
3. For severe predictions, avoid deterministic wording (“possible risk”, not certainty).
4. For relationship-sensitive outputs, use privacy-safe UX.
5. Keep remedy actions non-harmful and reversible by default.

---

## 9) UX outputs that users will love

1. **Today card:** 3 short indicators + 1 caution + 1 remedy.
2. **This month card:** opportunities vs caution windows.
3. **Why this result?:** rule trace in plain language.
4. **Home clues checklist:** lets user confirm nishaniyan quickly.
5. **Remedy streak tracker:** daily compliance and improvement graph.
6. **Confidence meter:** avoids overclaiming.

---

## 10) MVP vs Phase-2 scope

## MVP (6-8 weeks)
1. Birth input + chart generation
2. One-planet and two-planet rule engine
3. Basic gochar overlay
4. Predictions tab with confidence
5. Remedies planner
6. Source-cited explanation panel

## Phase 2
1. Three-planet complex rules
2. Full varshfal integration
3. Chandra Chalana guided protocol
4. Outcome feedback learning loop
5. Multi-language (Hindi + English)
6. Practitioner dashboard (if B2B)

---

## 11) Suggested tech stack

- Backend: Python (`FastAPI`) or Node (`NestJS`)
- Astro calculations: Swiss Ephemeris wrapper (`pyswisseph`) and/or PyJHora components
- Database: PostgreSQL
- Search/index for rules: PostgreSQL FTS or OpenSearch
- Frontend: Next.js/React
- Queue: Redis + background workers (for batch predictions)

---

## 12) Internet research notes applied in this blueprint

1. **Swiss Ephemeris / pyswisseph** is widely used for high-precision astrological planetary calculations and broad date-range support; suitable as core calculation engine.
2. **PyJHora** currently exposes many Vedic modules (dasha, chart variants, annual features), useful for faster feature expansion beyond raw ephemeris.
3. **Timezone correctness** should rely on the IANA Time Zone Database (updated periodically; latest release shown on IANA page), otherwise DST/history errors will break charts.
4. **If using free Nominatim geocoding**, enforce strict usage policy (rate limits, identification header, caching) from OSM policy documentation.

---

## 13) Practical implementation order (recommended)

1. Lock calculation conventions:
   - sidereal/tropical choice (default sidereal)
   - ayanamsha default (make configurable)
   - house system default
2. Build chart computation microservice.
3. Build rule database from PDFs with manual QA.
4. Implement scoring + prediction generator.
5. Add remedy scheduling and feedback loop.
6. Add gochar/varshfal layers.
7. Add explainable AI UI with strict citation to rule IDs.

---

## 14) Example output template (for each prediction)

- **Category:** Career
- **Prediction:** Next 30 days may bring authority-related pressure and rapid task switching.
- **Why:** Rules `R-SUN-7-014`, `R-MERCURY-TRANSIT-033` matched; user-confirmed signs: A, C.
- **Time Window:** 2026-04-14 to 2026-05-06
- **Confidence:** 72/100 (Moderate)
- **Suggested Actions:** Communication discipline, avoid impulsive decisions, do remedy `U-047` for 21 days.

---

## 15) What this gives you

If you build with this structure, your app can become:
- Deeply aligned with your Lalkitaab corpus,
- Explainable (not black-box),
- Trackable (prediction accuracy over time),
- Scalable from beginner users to serious practitioners.


---

## 16) Sources (Internet)

1. PyJHora package details and feature list: https://pypi.org/project/pyjhora-astro-suite/
2. pyswisseph (Swiss Ephemeris Python wrapper): https://pypi.org/project/pyswisseph/
3. IANA Time Zone Database reference: https://data.iana.org/time-zones/tz-link.html
4. Nominatim Usage Policy (OSMF): https://operations.osmfoundation.org/policies/nominatim/

