# Phaladeepika Completeness — Copy-Paste Prompts

7 self-contained prompts, one per feature. Each includes full context so you can hand it to any CLI (Kimi / Gemini / Codex / fresh Claude session) without prior chat history.

Execute in order: **1 → 2 → 3 → 4 → 5 → 6 → 7**.

Between prompts, run: `pytest -q && cd frontend && npm run build` to verify nothing regressed.

---

## 📋 Prompt 1 — Pravrajya (Ascetic) Yogas

```
TASK: Implement Adhyaya 27 of Phaladeepika — Pravrajya (ascetic / renunciation) yogas — in the Astro Rattan repo at /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app.

CONTEXT:
- FastAPI + Python backend, React + TypeScript frontend.
- Existing engines follow this pattern: app/<name>_engine.py + app/routes/kundli.py endpoint + frontend tab component.
- Chart data structure (input): {'planets': {'Sun': {'sign': 'Aries', 'house': 1, 'longitude': 12.3, 'sign_degree': 12.3, ...}, ...}, 'ascendant': {'sign': 'Aries', 'longitude': 0}, 'houses': [...]}.
- Bilingual: every user-facing string must have *_en and *_hi fields.
- Testing framework: pytest (1167 tests currently pass).
- i18n: add new keys to frontend/src/lib/i18n.ts in both translations (EN + HI parity enforced by scripts/check-i18n.cjs).
- Deployment: user runs SSH deploy; you only commit + push to staging branch.

SCOPE — 7 CLASSICAL PRAVRAJYA YOGAS (Phaladeepika Adh. 27, slokas 1–7):

1. PARAMAHAMSA: 4 or more planets (excluding Moon) in ONE sign, AND Jupiter is one of them, AND that sign is in a Kendra (1, 4, 7, 10).
2. SANNYASI: Saturn aspects Moon; Moon is in Saturn's drekkana (decan) of a sign (2nd or 3rd drekkana of Saturn-ruled signs: Capricorn/Aquarius).
3. TRIDANDI: Jupiter in Lagna, aspected by Saturn.
4. BHRUGUKACHCHA: Sun + Mars + Saturn all occupy either Kendras (1,4,7,10) or Trikonas (1,5,9).
5. VANAPRASTHA: 4+ planets of equal strength in Lagna (1st house).
6. VRIDDHASRAVAKA: Moon and Mars together in same house, aspected by Saturn.
7. CHARAKA: Moon is weak (debilitated / in 6,8,12 / aspected by malefics) AND Ketu in Lagna.

For each detected yoga, compute effect strength (1-10): count how many supporting factors (exaltation, Kendra placement, benefic aspect) are present.

DELIVERABLES:

1. CREATE app/pravrajya_engine.py with:
   - def detect_pravrajya(chart_data: dict) -> dict
   - Returns: {"yogas_found": [{"key": "paramahamsa", "name_en": "Paramahamsa", "name_hi": "परमहंस", "strength": 8, "effect_en": "...", "effect_hi": "...", "sloka_ref": "Adh. 27 sloka 1", "supporting_factors": [...]}], "count": N, "has_ascetic_tendency": bool}
   - Helper: _planets_in_sign(planets, sign) -> list
   - Helper: _is_drekkana(planet_longitude: float, drekkana_num: int, sign: str) -> bool

2. ADD endpoint to app/routes/kundli.py:
   - @router.get("/{kundli_id}/pravrajya")
   - Fetches kundli, parses chart_data, calls detect_pravrajya, returns dict.

3. CREATE frontend/src/components/kundli/PravrajyaTab.tsx:
   - Props: { kundliId: string; language: string; t: (key: string) => string }
   - Fetches /api/kundli/{id}/pravrajya on mount
   - Renders list of yogas as cards with: name (bilingual), strength bar (1-10), effect, sloka ref
   - Empty state: "No Pravrajya yogas detected" (bilingual)

4. REGISTER new tab in frontend/src/sections/KundliGenerator.tsx inside the "More Analysis" dropdown.

5. ADD i18n keys to frontend/src/lib/i18n.ts (EN + HI both):
   auto.pravrajyaYogas, auto.asceticTendency, auto.yogaStrength, auto.slokaRef, auto.noPravrajyaFound, + 7 yoga names

6. CREATE tests/test_pravrajya.py:
   - One test per yoga with a handcrafted chart fixture that SHOULD trigger it
   - One test verifying a "normal" chart triggers ZERO pravrajya yogas
   - Test that detect_pravrajya handles missing planets gracefully

VERIFICATION CHECKLIST (run before committing):
- pytest tests/test_pravrajya.py -v  → all pass
- pytest -q  → still 1167+ passing (no regressions)
- cd frontend && npm run build  → build clean (i18n gate passes)
- Manually test on Meharban Singh's saved kundli (ask user for kundli_id)

COMMIT MESSAGE:
"feat: Pravrajya yogas (Phaladeepika Adh. 27) — 7 ascetic yogas with bilingual output

Co-Authored-By: <your-model-name>"

After commit: push to staging branch. User will handle merge to main + deploy.
```

---

## 📋 Prompt 2 — Balarishta & Ayu Classification

```
TASK: Implement Adhyaya 13 of Phaladeepika — Balarishta (infant mortality risk) + Ayu classification (Alpayu/Madhyayu/Dirghayu/Purnayu) — in the Astro Rattan repo at /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app.

CONTEXT:
- Same codebase as Prompt 1 (FastAPI + React, bilingual, pytest).
- This is the PREREQUISITE for 3-method Ayurdaya (Prompt 3) — do this first.
- Chart input format: same as Prompt 1.

SCOPE — CLASSICAL RULES (Phaladeepika Adh. 13, slokas 1–8):

BALARISHTA (infant mortality, death before age 12):
- Moon in 6/8/12 aspected by malefic (Mars/Saturn/Rahu/Ketu) without benefic aspect
- Weak Moon in Lagna + weak Lagna lord
- Malefic in Lagna + Moon in 7th/8th aspected by malefic
- Sun in 7th/8th + Moon in 6th/12th

AYU CATEGORIES (total lifespan):
- ALPAYU (short, up to 32y): Malefic in Lagna, no benefic aspect; Lagna lord in 6/8/12; Moon+Saturn+Mars in Lagna
- MADHYAYU (middle, 32–64y): Mixed influences; 8th lord in Kendra; benefics + malefics in roughly equal strength
- DIRGHAYU (long, 64–108y): Strong Jupiter in Kendra/Trikona; Lagna lord strong + benefic aspect; 8th lord in own/exaltation
- PURNAYU (100+y): Dirghayu conditions + exalted Lagna lord + Jupiter in Lagna/5/9/10

For each category, generate "reasoning" text explaining WHICH rule matched.

DELIVERABLES:

1. CREATE app/ayurdaya_engine.py with:
   - def check_balarishta(chart_data: dict) -> dict
     Returns: {"has_risk": bool, "risk_level": "low|moderate|high|severe", "factors": [...], "remedies_recommended": bool, "sloka_ref": "..."}
   - def classify_ayu(chart_data: dict) -> dict
     Returns: {"category": "Dirghayu", "years_range": "64-108", "reasoning_en": "...", "reasoning_hi": "...", "matched_rules": [...], "sloka_ref": "..."}
   - def is_balarishta_cancelled(chart_data: dict) -> bool  (benefic aspect can cancel balarishta per sloka 21)

2. ADD endpoint to app/routes/kundli.py:
   - @router.get("/{kundli_id}/ayu-classification")
   - Returns: {"balarishta": {...}, "ayu_class": {...}}

3. CREATE frontend/src/components/kundli/LifespanTab.tsx (reused in Prompt 3):
   - Fetches /api/kundli/{id}/ayu-classification
   - Shows: Category badge (Dirghayu etc.), year range, reasoning bullet points
   - Balarishta risk card (only if has_risk=true): risk level, factors, remedy note

4. REGISTER "Lifespan" tab in KundliGenerator "More Analysis" dropdown.

5. ADD i18n keys:
   auto.lifespan, auto.alpayu, auto.madhyayu, auto.dirghayu, auto.purnayu, auto.balarishtaRisk, auto.riskLevel, auto.yearsRange, auto.reasoningFactors

6. CREATE tests/test_balarishta.py:
   - Test balarishta detection with Moon-in-6th + Mars aspect chart
   - Test each Ayu category (Alpayu/Madhya/Dirgha/Purna) with canonical example charts
   - Test balarishta cancellation when Jupiter aspects Moon

HISTORICAL TEST FIXTURES (verify your implementation gives expected results):
- Ramana Maharshi (1879-12-30, 01:00, Tiruchuli, TN) → Dirghayu
- Adi Shankara (traditionally aged 32) → Alpayu classical prediction
- M.K. Gandhi (1869-10-02, 07:12, Porbandar) → Madhyayu (died 78)

VERIFICATION: pytest tests/test_balarishta.py -v && pytest -q && cd frontend && npm run build

COMMIT: "feat: Balarishta + Ayu classification (Phaladeepika Adh. 13)"

Push to staging.
```

---

## 📋 Prompt 3 — Three-Method Ayurdaya

```
TASK: Implement Adhyaya 22 of Phaladeepika — three classical lifespan calculation methods (Pindayu, Nisargayu, Amsayu) + 6 Haranas (reductions) — in Astro Rattan repo at /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app.

CONTEXT:
- Extends app/ayurdaya_engine.py created in Prompt 2.
- Frontend reuses LifespanTab.tsx — just adds new sections.

SCOPE — THREE LIFESPAN CALCULATORS (Phaladeepika Adh. 22):

1. PINDAYU (Satyacharya method, Sun-based):
   - Each planet contributes years based on its position & strength in its saptavarga
   - Max planet years: Sun 19, Moon 25, Mars 15, Mercury 12, Jupiter 15, Venus 21, Saturn 20
   - Contributions scaled by (planet's vimshopaka bala / max_possible)
   - Sum planet contributions → raw pindayu
   - Reduce by Haranas (see below)

2. NISARGAYU (Jivasarman method, Moon-based):
   - Natural life assigned by Moon's placement:
     - Moon in own/exalt in Kendra → 80-100 years
     - Moon in benefic house + benefic aspect → 70-90 years
     - Moon in 6/8/12 → 40-60 years
     - Weak Moon + malefic aspect → < 40 years
   - Adjusted by other planetary influences on Moon

3. AMSAYU (Parashara method, Navamsa-based):
   - Each planet contributes 1/108 × 100 years × (navamsa_position_strength)
   - Planets in own navamsa → full contribution
   - Planets in enemy navamsa → half
   - Planets in debilitation navamsa → quarter

6 HARANAS (reductions — Adh. 22 slokas 17–22):
- RAJA-HARANA: if Lagna lord severely afflicted → reduce by 1/3
- BHUPA-HARANA: if 10th lord weak → reduce by 1/4
- AYANA-HARANA: if Sun/Moon in southern ayana unfavorably → reduce by 1/6
- ASTANGATA-HARANA: for each combust planet → reduce by 1/8 per planet
- DUSHTA-HARANA: planets in 6/8/12 → reduce by 1/10 per planet
- CHAKRAPATA-HARANA: special astronomical alignment → reduce by 1/12 (use approximation)

SELECTOR RULE (Adh. 22 sloka 27):
- If SUN strongest among Sun/Moon/Lagna → use PINDAYU
- If MOON strongest → use NISARGAYU
- If LAGNA strongest (or equal) → use AMSAYU
- If any method gives <5 years → cross-check with Kalachakra dasha (fallback)

Final lifespan CAPPED at 108 years (human limit).

DELIVERABLES:

1. EXTEND app/ayurdaya_engine.py with:
   - def pindayu(chart_data: dict) -> dict (raw years, after haranas, breakdown)
   - def nisargayu(chart_data: dict) -> dict
   - def amsayu(chart_data: dict) -> dict
   - def apply_haranas(raw_years: float, chart_data: dict) -> dict (returns {final_years, haranas_applied: [...]})
   - def calculate_lifespan(chart_data: dict) -> dict
     Returns:
     {
       "pindayu": {"raw": 78.4, "after_haranas": 72.1, "haranas": [...]},
       "nisargayu": {"raw": 82.0, "after_haranas": 75.3, "haranas": [...]},
       "amsayu": {"raw": 79.5, "after_haranas": 73.2, "haranas": [...]},
       "selected_method": "amsayu",
       "selection_reason_en": "Lagna strongest among Sun/Moon/Lagna",
       "selection_reason_hi": "...",
       "final_years": 73.2,
       "classification": "Dirghayu",  // from Prompt 2's classify_ayu
       "sloka_ref": "Adh. 22 sloka 27"
     }

2. ADD endpoint: @router.get("/{kundli_id}/lifespan") in app/routes/kundli.py
   - Returns combined output of calculate_lifespan + classify_ayu + check_balarishta

3. UPDATE frontend/src/components/kundli/LifespanTab.tsx:
   - Show all 3 methods side-by-side in a table
   - Highlight selected method
   - Show haranas breakdown (expandable)
   - Final lifespan in large number display with classification badge

4. ADD i18n keys:
   auto.pindayu, auto.nisargayu, auto.amsayu, auto.rawYears, auto.afterHaranas, auto.selectedMethod, auto.finalLifespan, auto.rajaHarana, auto.bhupaHarana, auto.ayanaHarana, auto.astangataHarana, auto.dushtaHarana, auto.chakrapataHarana

5. CREATE tests/test_ayurdaya.py:
   - Unit tests for each of 3 methods with mock charts
   - Unit tests for each of 6 haranas (apply separately, verify math)
   - Integration test: full calculate_lifespan on historical chart
   - Test cap at 108 years
   - Test selector: Sun-strongest → pindayu, Moon-strongest → nisargayu, Lagna-strongest → amsayu

HISTORICAL TEST FIXTURES:
- Gandhi: died 78.4 years actual. All 3 methods should land within 60-85 range
- Ramana Maharshi: died at 70. Similar range

VERIFICATION: pytest tests/test_ayurdaya.py -v (all pass) && pytest -q (1167+ still pass) && cd frontend && npm run build

COMMIT: "feat: Three-method Ayurdaya (Phaladeepika Adh. 22) — Pindayu/Nisargayu/Amsayu + 6 Haranas"

Push to staging.
```

---

## 📋 Prompt 4 — 45 Two-Planet Conjunction Phalam

```
TASK: Implement Adhyaya 18 of Phaladeepika — pair-wise conjunction effects for all 45 planet combinations (C(10,2) including Rahu/Ketu) — in Astro Rattan repo at /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app.

CONTEXT:
- Detection: two planets within 8° orb in the SAME sign → conjunction
- Effects are house-modified (Kendra vs Dusthana) but base phalam is planet-pair
- Bilingual required

SCOPE:
10 planets: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu, Lagna-lord
→ C(9,2) = 36 planet-planet pairs + 9 planet-with-Lagna = 45 total pairings

BASE EFFECTS per pair (from Adh. 18 slokas 3-48) — condensed:

Sun-Moon: Harsh temperament, mother-father conflict
Sun-Mars: Valor, military, fiery disposition, surgical aptitude
Sun-Mercury: Budhaditya yoga — intelligence, eloquence
Sun-Jupiter: Royal favor, religious authority, fortune
Sun-Venus: Vision issues, wife's ill-health, artistic bent
Sun-Saturn: Father-son conflict, bone issues, servant-like status
Sun-Rahu: Eclipses — ego distortion, political failure
Sun-Ketu: Spiritual pride, loss of authority

Moon-Mars: Chandra-Mangal yoga — wealth through business
Moon-Mercury: Merchant, well-spoken, charming
Moon-Jupiter: Gaja-Kesari (if in Kendra) — prosperity
Moon-Venus: Handsome, poetic, many women
Moon-Saturn: Mental stress, mother's ill-health, melancholy
Moon-Rahu: Mental disturbance, addictions
Moon-Ketu: Spiritual insights, unstable mind

Mars-Mercury: Debater, sharp tongue, argumentative
Mars-Jupiter: Guru-Mangal yoga — successful advocate, commander
Mars-Venus: Passionate, artistic, strong sexual energy
Mars-Saturn: Accidents, legal issues, chronic anger
Mars-Rahu: Violent tendencies, engineering aptitude
Mars-Ketu: Sudden accidents, martial arts, surgery

Mercury-Jupiter: Scholar, literary genius, wealth through intellect
Mercury-Venus: Business, diplomacy, luxury trade
Mercury-Saturn: Cautious, analytical, late success
Mercury-Rahu: Computer skills, foreign trade
Mercury-Ketu: Investigative mind, research

Jupiter-Venus: Wealth, religious teachers, happy marriage
Jupiter-Saturn: Karma yogi, patient accumulator, late-life success
Jupiter-Rahu: Guru-Chandal yoga — corrupted teacher
Jupiter-Ketu: Genuine spiritual teacher

Venus-Saturn: Delayed marriage, older spouse, service orientation
Venus-Rahu: Sensuality, unconventional relationships
Venus-Ketu: Tantric practices, artistic detachment

Saturn-Rahu: Shrapit yoga — delays, obstacles, hard work
Saturn-Ketu: Spiritual discipline, ascetic tendencies

Rahu-Ketu: Kaal Sarp (handled elsewhere — reference)

Plus 9 Planet-with-Lagna effects (planet conjunct ascendant):
Sun-Lagna: Bold, commanding, authoritative appearance
Moon-Lagna: Peaceful, attractive, emotional
Mars-Lagna: Fiery, combative, scarred/injured face
Mercury-Lagna: Youthful, articulate, quick-witted
Jupiter-Lagna: Dignified, respected, religious
Venus-Lagna: Beautiful, charming, artistic
Saturn-Lagna: Serious, slow, thin/dark complexion
Rahu-Lagna: Unconventional appearance, foreign look
Ketu-Lagna: Spiritual aura, deep-set eyes

DELIVERABLES:

1. CREATE app/data/conjunction_effects.json with 45 entries, each:
   {
     "key": "sun_moon",
     "planets": ["Sun", "Moon"],
     "name_en": "Sun-Moon Conjunction",
     "name_hi": "सूर्य-चंद्र युति",
     "nature": "mixed|benefic|malefic",
     "effect_en": "...",
     "effect_hi": "...",
     "enhanced_en": "If in Kendra: stronger parental conflict",
     "enhanced_hi": "...",
     "weakened_en": "If aspected by Jupiter: softened",
     "weakened_hi": "...",
     "sloka_ref": "Adh. 18 sloka 3",
     "special_yoga": "Budhaditya" | null
   }

2. CREATE app/conjunction_engine.py with:
   - def detect_conjunctions(chart_data: dict, orb_degrees: float = 8.0) -> list
   - Returns list of {"planets": [...], "house": int, "sign": str, "orb": float, "effect_en": ..., "effect_hi": ..., "enhanced": bool, "weakened": bool, "special_yoga": ..., "sloka_ref": ...}
   - Iterates all pairs, checks sign match + longitude difference < orb

3. ADD endpoint: @router.get("/{kundli_id}/conjunctions") in app/routes/kundli.py

4. INTEGRATE into existing Kundli chart component (frontend/src/components/InteractiveKundli.tsx):
   - When a house has 2+ planets, show a small "🔗 N" badge
   - Click → popover with conjunction effects list

5. ALSO create new section in ReportTab.tsx showing all detected conjunctions as cards.

6. i18n keys: auto.conjunctions, auto.enhancedInKendra, auto.weakenedByBenefic, auto.specialYoga (+ 45 pair names)

7. CREATE tests/test_conjunctions.py:
   - Verify JSON data file has exactly 45 entries with unique keys
   - Test orb detection: planets 0° apart = conjunct, 9° apart = NOT conjunct (above 8° orb)
   - Test each of 10 base pairs triggers correctly
   - Test Lagna-planet conjunctions

VERIFICATION: pytest tests/test_conjunctions.py -v && pytest -q && cd frontend && npm run build

COMMIT: "feat: 45 two-planet conjunction effects (Phaladeepika Adh. 18)"

Push to staging.
```

---

## 📋 Prompt 5 — Classical Roga (Disease) Phalam

```
TASK: Implement Adhyaya 14 of Phaladeepika — classical disease prediction (Roga Phalam) — in Astro Rattan repo at /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app.

CONTEXT:
- Augments existing dosha_engine.py (which handles Mangal/Kaal Sarp/Sade Sati)
- Different from dosha: Roga predicts SPECIFIC DISEASES based on planets in 6/8/12 and their aspects
- Integrates into existing Health tab

SCOPE — PLANET→DISEASE MAPPING (Adh. 14 slokas 2-8):

PLANET DISEASE-SIGNATURES:
- SUN: heart, bile (pitta), head pain, eye issues (right eye for men), fevers, vitamin deficiency, spine
- MOON: blood, phlegm (kapha), mental disorders, water-borne diseases, mother-related ailments, left eye for men, lung issues
- MARS: wounds, accidents, blood pressure, pitta excess, surgery, burns, muscle injuries, inflammations
- MERCURY: skin diseases, allergies, nervous system, speech defects, digestive issues
- JUPITER: liver, diabetes (JUPITER in 8th classic indicator), obesity, ear issues, pancreas
- VENUS: reproductive organs, urinary tract, venereal disease, throat, diabetes (female), kidney
- SATURN: chronic diseases, bones, arthritis, paralysis, depression, legs, teeth, rheumatism
- RAHU: undiagnosed / mysterious diseases, psychological, foreign diseases, poisons, sudden onset
- KETU: sudden onset, spiritual-cause, accidents, undiagnosed, parasitic, viral

TRIGGERING RULES:
- Planet in 6th house → disease of that planet's type will appear
- Planet in 8th → chronic/death-causing potential
- Planet in 12th → hospitalization, hidden disease
- 6th lord + planet nature → specific body area
- Malefic aspect on Lagna/Moon → mental/physical weakness
- Benefic in 6/8/12 can cancel (slight)

SPECIAL DISEASE YOGAS (Adh. 14 sloka 11-12):
- LEPROSY: Moon + Rahu in Lagna without Jupiter aspect
- EPILEPSY: Saturn + Moon in Lagna, afflicted
- DIABETES: Jupiter in 6th OR Venus + Saturn in 6th
- JAUNDICE: Sun + Mars in 6th
- TUBERCULOSIS: Moon in 8th afflicted + weak Lagna
- INSANITY: Moon + Saturn + Rahu conjoint in dusthana
- BLINDNESS: Sun+Moon both debilitated with no benefic aspect

TIMING (when will disease manifest):
- During mahadasha of the afflicting planet
- During antardasha of 6th/8th lord
- During transit of Saturn over natal Moon (Sade Sati)

DELIVERABLES:

1. CREATE app/data/roga_rules.json with:
   - "planet_diseases": {...} (each planet → disease list, en + hi)
   - "special_yogas": [...] (7 special disease yogas with trigger conditions + disease name + remedy suggestion)
   - "body_part_by_house": {...} (house 1=head, house 2=face, ... standard mapping)

2. CREATE app/roga_engine.py with:
   - def analyze_diseases(chart_data: dict) -> dict
     Returns: {
       "general_tendencies": [...],  (from planets in 6/8/12)
       "special_yogas_detected": [...],  (matched from 7 special yogas)
       "timing_indicators": [...],  (which dashas/transits to watch)
       "body_parts_affected": [...],
       "remedy_suggestions": [...],
       "sloka_ref": "Adh. 14"
     }

3. ADD endpoint: @router.get("/{kundli_id}/roga-analysis") in app/routes/kundli.py

4. INTEGRATE into existing health section:
   - If there's a HealthTab, add "Classical Disease Analysis" section
   - If not, create frontend/src/components/kundli/RogaTab.tsx
   - Show: disease tendencies cards, special yogas (with warning for severe ones), timing, remedies

5. i18n keys: auto.rogaAnalysis, auto.diseaseTendencies, auto.specialDiseaseYogas, auto.timingIndicators, auto.bodyPartsAffected, auto.remedySuggestions, + disease names (leprosy, diabetes, etc. in HI/EN)

6. CREATE tests/test_roga.py:
   - Test each planet triggers its disease set when in 6/8/12
   - Test each of 7 special yogas with handcrafted chart
   - Test benefic cancellation reduces severity
   - Integration test on historical chart

VERIFICATION: pytest tests/test_roga.py -v && pytest -q && cd frontend && npm run build

COMMIT: "feat: Classical Roga (disease) phalam (Phaladeepika Adh. 14)"

Push to staging.
```

---

## 📋 Prompt 6 — Yoga Library Expansion (10 → 80+)

```
TASK: Expand the yoga detection library in Astro Rattan from ~10 yogas to 80+ covering Phaladeepika Adh. 6 & 7 comprehensively. Repo: /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app.

CONTEXT:
- Existing file: app/yoga_search_engine.py — ~10 yogas hardcoded
- Target: REFACTOR to data-driven architecture, then ADD 70+ new yogas
- Endpoint: /api/yoga-search exists — extend, don't break

ARCHITECTURE CHANGE — DECLARATIVE YOGA RULES:

Instead of hardcoded Python if-else per yoga, use JSON rules + generic evaluator.

Rule types:
- planet_in_house(planet, houses[])
- planet_in_own_or_exaltation(planet)
- planet_aspects_planet(source, target)
- planet_aspects_house(source, house)
- lord_of_house_in_house(lord_of, in_house)
- planets_conjunct(planet1, planet2, max_orb)
- count_planets_in_houses(planets[], houses[], operator: ">=", count: N)
- planet_in_kendra(planet)
- planet_in_trikona(planet)
- planet_strong(planet, min_strength)
- no_planet_in(houses[])
- AND, OR, NOT combinators

YOGA CATEGORIES TO IMPLEMENT (from Phaladeepika Adh. 6-7):

A. PANCHA MAHAPURUSHA (5 — verify existing):
   Ruchaka (Mars in own/exalt in Kendra)
   Bhadra (Mercury —)
   Hamsa (Jupiter —)
   Malavya (Venus —)
   Sasa (Saturn —)

B. MOON-BASED (6):
   Sunapha (planets in 2nd from Moon, not Sun)
   Anapha (planets in 12th from Moon)
   Durudhara (planets in both 2nd and 12th from Moon)
   Kemadruma (NO planets in 2nd, 12th, or Kendra from Moon — POVERTY yoga)
   Adhi Yoga (benefics in 6/7/8 from Moon)
   Vasumati (benefics in Upachayas from Moon)

C. KENDRA-MALEFIC/BENEFIC (8):
   Subhakartari (benefics in 2nd AND 12th from a planet/Lagna)
   Papakartari (malefics —)
   Subha-Mala (3+ benefics in Kendra)
   Papa-Mala (3+ malefics —)
   Subha-Vasi, Papa-Vasi (benefic/malefic in 12th from Sun)
   Subha-Ubhayachari, Papa-Ubhayachari (both sides of Sun)

D. DHANA (Wealth, 12):
   Lakshmi (9th lord strong + benefic in 9th)
   Saraswati (Mercury+Jupiter+Venus in Kendra/Trikona/2nd)
   Parvata (Lagna+12th lord in Kendra with benefics)
   Kahala (4th + 9th lord in Kendra together)
   Chamara (Lagna lord exalted in Kendra aspected by Jupiter)
   Dhenu (2nd lord + 11th lord in Kendra)
   Jaladhi (3rd lord with Venus, aspected by Jupiter)
   Bharati (2nd/5th/11th lords in Kendra)
   Ama (Mercury exalted + Jupiter aspect)
   Pushya (Jupiter in 4th from Moon, with benefic aspect)
   Srikantha (Lagna/Moon/5th lord connected via own/exalt/friend sign)
   Srinatha (7th + 10th lords connected; Venus involved)

E. FAME/PROSPERITY (10):
   Vamsi, Amala, Goar, Pushkala, Hathi-Mangsh, Samanya, Samudraja, Sankha, Bheri, Mridanga

F. NABHASA (classical 32 — Adh. 7):
   Rajju (3 sub-types), Musala (3), Nala, Mala, Sarpa (3 types by movement),
   Gada, Sakata, Vihaga, Sringataka, Hala, Vajra, Yava, Kamala, Vapi, Yupa,
   Sara, Sakti, Danda, Naukaa, Koota, Chathra, Chapa, Ardhachandra, Samudra,
   Chakra, Samputa, Iravata, Dhwaja

G. RAJA-YOGAS (8):
   Neechabhanga (debilitation cancellation — specific rules)
   Sun-Caused (strong exalt Sun + 9th/10th aspect)
   Moon-Caused (similar for Moon)
   Mars-Caused
   Venus-Lagna (Venus in Lagna with 9/10 lords)
   Kendra-Trikona Connection (lord of Kendra + lord of Trikona conjunct)
   Vipareeta (lord of 6/8/12 in another dusthana)
   Dharma-Karmadhipati (9th + 10th lords in mutual Kendra/Trikona)

H. GAJA-KESARI special (Adh. 6 sloka 14): Already have — verify
I. BUDHADITYA special: Already covered in Prompt 4

DELIVERABLES:

1. CREATE app/data/yogas.json with ~80 yoga definitions, each:
   {
     "key": "lakshmi",
     "name_en": "Lakshmi Yoga",
     "name_hi": "लक्ष्मी योग",
     "category": "dhana",
     "rules": {"type": "AND", "conditions": [
       {"type": "lord_in_house", "lord_of": 9, "in_houses": [1,5,9,10]},
       {"type": "planet_strong", "planet": "Venus", "min_strength": 0.5}
     ]},
     "effect_en": "Bestows abundant wealth, lovable spouse, and fame.",
     "effect_hi": "...",
     "category_label_en": "Dhana Yoga",
     "category_label_hi": "धन योग",
     "sloka_ref": "Adh. 6 sloka 35"
   }

2. CREATE app/yoga_rule_engine.py:
   - def evaluate_rule(rule: dict, chart_data: dict) -> bool  (recursive, handles AND/OR/NOT)
   - def detect_all_yogas(chart_data: dict, category_filter: str = None) -> list
   - Returns list of matched yogas with full metadata

3. REFACTOR app/yoga_search_engine.py:
   - Keep existing API signature
   - Internally delegate to yoga_rule_engine
   - Remove hardcoded per-yoga logic

4. EXTEND app/routes/ route handling yoga search:
   - Add ?category= query param (raja|dhana|nabhasa|mahapurusha|moon|kendra|fame)

5. UPDATE YogaSearchTab.tsx (frontend):
   - Add category filter chips at top
   - Group results by category
   - Each yoga card: name, sloka ref, effect, category badge, strength indicator

6. ADD i18n keys for all 80 yoga names (EN+HI) + category labels.

7. CREATE tests/test_yogas_expanded.py:
   - Verify count >= 80 yogas loaded from JSON
   - One test per MAJOR yoga (at least 30 spot-checks) with handcrafted charts
   - Test rule_engine evaluator for each rule type (unit tests)
   - Test AND/OR/NOT combinator logic
   - Regression: verify existing 10 yogas still detected with same API

VERIFICATION: pytest tests/test_yogas_expanded.py -v && pytest -q (no regressions in existing yoga tests) && cd frontend && npm run build

COMMIT: "feat: Yoga library expansion ~10→80 (Phaladeepika Adh. 6-7) — data-driven rule engine"

Push to staging.
```

---

## 📋 Prompt 7 — Gochara Vedhas + Lattas (FINAL — most complex)

```
TASK: Implement Adhyaya 26 of Phaladeepika — Gochara Vedha (transit obstruction cancellation) + Lattas (kicks) rules — in Astro Rattan repo at /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app.

CONTEXT:
- MOST CRITICAL ACCURACY FIX — touches live transit engine
- Existing: app/transit_engine.py has basic good/bad house transit mapping
- PROBLEM: no Vedha cancellation means ~30% of daily horoscope predictions are WRONG per classical rules
- Ship ONLY AFTER Prompts 1-6 pass QA

BACKGROUND:
Classical rule: a good transit can be CANCELLED by another planet sitting in a specific "Vedha" (obstruction) house from the Moon. Same for bad transits being cancelled. Vedha tables are fixed per-planet.

SCOPE — VEDHA TABLES (Adh. 26 slokas 29-33):

SUN:
  Good transits (3,6,10,11 from Moon) → Vedha by another planet in houses (9,12,4,5) respectively
  i.e. Sun's good in 3 is cancelled by planet in 9; good in 6 cancelled by 12; etc.

MOON (varies by day/night half):
  Good (1,3,6,7,10,11) → Vedha by planet in (5,9,12,2,4,8)

MARS:
  Good (3,6,11) → Vedha by planet in (12,9,5)

MERCURY:
  Good (2,4,6,8,10,11) → Vedha by planet in (5,3,9,1,8,12)

JUPITER:
  Good (2,5,7,9,11) → Vedha by planet in (12,4,3,10,8)

VENUS:
  Good (1,2,3,4,5,8,9,11,12) → Vedha by planet in (8,7,1,10,9,5,11,6,3)

SATURN:
  Good (3,6,11) → Vedha by planet in (12,9,5)

RAHU/KETU: Same rules as Saturn/Mars respectively.

EXCEPTION: Moon-Saturn don't vedha each other. Sun-Moon don't vedha each other. (Adh. 26 sloka 33)

LATTAS (Kicks) — secondary modifier (Adh. 26 slokas 36-40):
- Each planet has a "Pratyak Latta" (back-kick) nakshatra distance and "Prishta Latta" (front-kick)
- When a transit planet reaches a specific nakshatra count from natal Moon's nakshatra → latta effect
- Modifiers: +25% strength if Prishta (front), -25% if Pratyak (back)

Planet latta-distances (count from natal nakshatra):
- Sun: 12 (Prishta), 16 (Pratyak)
- Moon: 22, 5
- Mars: 3, 1
- Mercury: 7, 9
- Jupiter: 6, 8
- Venus: 5, 7
- Saturn: 8, 2

DELIVERABLES:

1. CREATE app/data/gochara_vedhas.json:
   {
     "Sun": {"good": [3,6,10,11], "vedhas": {"3":9, "6":12, "10":4, "11":5}},
     ... (all 7 planets + Rahu/Ketu)
     "exceptions": [["Sun","Moon"], ["Moon","Saturn"]]
   }

2. CREATE app/data/latta_table.json:
   {
     "Sun": {"prishta": 12, "pratyak": 16},
     ... (all 7)
   }

3. MODIFY app/transit_engine.py:
   - Add def apply_vedhas(transits: list, natal_chart: dict) -> list
     For each transit entry, check if any planet occupies the vedha house from natal Moon
     If yes: mark cancellation, add vedha_by: "Mars in 9th cancels Sun's transit in 3rd"
   - Add def apply_lattas(transits: list, natal_chart: dict) -> list
     For each transit, compute nakshatra distance from natal Moon nakshatra
     If distance matches Prishta/Pratyak → apply ±25% strength modifier
   - Modify main transit output function to call these in sequence

4. UPDATE /api/horoscope/transits response schema:
   Each transit entry now includes:
   {
     "planet": "Sun",
     "transit_house": 3,
     "effect_base": "favorable",
     "effect_final": "cancelled",  // after vedha+latta
     "vedha_active": true,
     "vedha_by": {"planet": "Mars", "house": 9, "description_en": "...", "description_hi": "..."},
     "latta_modifier": 0.75,
     "latta_type": "pratyak",
     "sloka_ref": "Adh. 26 sloka 29"
   }

5. UPDATE frontend/src/components/horoscope/TransitInsightsTab.tsx:
   - Show Vedha status next to each transit row:
     "✓ Active" (green) or "⊘ Cancelled by Mars in 8th" (red with strikethrough on effect text)
   - Show Latta modifier as pill: "+25% (Prishta)" or "-25% (Pratyak)"
   - Add legend: "⊘ = Vedha obstruction | Pratyak/Prishta = Latta kicks"

6. i18n keys:
   auto.vedhaActive, auto.vedhaCancelled, auto.cancelledBy, auto.pratyakLatta, auto.prishtaLatta, auto.transitStrengthened, auto.transitWeakened, auto.vedhaLegend, auto.lattaLegend

7. CREATE tests/test_gochara_vedha.py:
   - Table-driven test: for each (transiting_planet, good_house, vedha_planet, vedha_house) combo, verify cancellation fires
   - Test Sun-Moon exception (no vedha between them)
   - Test Moon-Saturn exception
   - Test multiple vedhas on same transit (should still cancel)
   - Test Latta calculation: with natal Moon in Ashwini (1st nak), transit Sun in 12th nak → Prishta Latta (12 naks = Sun's prishta distance) → +25%
   - Integration test: full daily horoscope with all modifiers applied

VERIFICATION (EXTRA CAREFUL — this touches live prod feature):
- pytest tests/test_gochara_vedha.py -v (comprehensive)
- pytest -q (MUST STILL BE 1167+)
- cd frontend && npm run build
- Manual test: load daily horoscope on production staging — compare against manual classical calculation for a known date
- Test dates to verify: today (2026-04-17) for all 12 signs — cross-reference against Drik Panchang if possible

COMMIT: "feat: Gochara Vedhas + Lattas (Phaladeepika Adh. 26) — transit prediction completeness"

Push to staging. This is a HIGH-IMPACT change — request manual QA before merge to main.
```

---

## 🎯 After All 7 Ship

Run these verification steps:
```bash
cd /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app
pytest -q  # expect 1167 + ~180 new = ~1350 tests passing
cd frontend && npm run build  # i18n gate + TS build pass
```

Then external audit prompt:
```
Audit the last 7 commits in this repo (all feat: Phaladeepika ...). Verify:
1. Classical rules from Phaladeepika Adh. 6,7,13,14,18,22,26,27 are correctly implemented
2. Bilingual (EN+HI) parity maintained
3. No regressions in existing 1167 tests
4. Every user-facing output has sloka_ref field
5. Historical chart fixtures (Gandhi, Ramana Maharshi, Adi Shankara) produce classically-expected results
Score each feature 0-10. Report gaps.
```

---

## 📝 Notes for Your Delegate CLI

- All prompts are self-contained — paste each as-is. No prior conversation context needed.
- Each prompt ends with "Push to staging." — you (Meharban) handle merge to main + SSH deploy.
- If the CLI gets stuck, tell it to read `docs/PHALADEEPIKA_SUMMARY.md` in the repo for the classical source.
- Between prompts: run `git log --oneline -5` to confirm the prior commit landed before starting next.
