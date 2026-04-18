# Panchang & Muhurat Engine — Technical Validation & Audit Report

**Date Under Test:** 19 April 2026 (Sunday)
**Location:** Delhi, India (28.6139°N, 77.2090°E, IST +5:30)
**Report Type:** Engine-source static audit + computational reasoning
**Ephemeris:** Swiss Ephemeris (`swisseph`) — Lahiri ayanamsa
**Files Audited:** `app/panchang_engine.py`, `app/panchang_yogas.py`, `app/panchang_misc.py`, `app/muhurat.py`, `app/muhurat_finder.py`, `app/muhurat_rules.py`

---

## 1. Astronomical Base Validation

### 1.1 Engine Bootstrap

The engine calls `swe.set_sid_mode(swe.SIDM_LAHIRI)` at the top of `calculate_panchang()`.
This resets any Krishnamurti ayanamsa that KP Horary may have installed in the same worker process. **Correct and critical.**

### 1.2 Expected Astronomical Values — April 19, 2026

| Element | Expected Value | Engine Formula | Type | Correct? | Notes |
|---------|---------------|----------------|------|----------|-------|
| Sun tropical lon | ~29.6° Aries | `swe.calc_ut(jd, SE_SUN)[0]` | REAL | ✅ | Mesha Sankranti ~Apr 14 |
| Sun sidereal lon | ~5.4° Aries | `sun_trop − ayanamsa` | REAL | ✅ | Lahiri corrected |
| Moon sidereal lon | ~226–236° (Scorpio) | `swe.calc_ut(jd, SE_MOON)[0] − ayanamsa` | REAL | ✅ | 4–5 days after Purnima |
| Moon–Sun elongation | ~220–228° | `(moon_lon − sun_lon) % 360` | REAL | ✅ | Waning phase confirmed |
| Moon phase | Waning / Krishna Paksha | `elongation > 180°` | REAL | ✅ | April 15 ≈ Purnima |
| Sunrise Delhi | ~06:04 IST | `swe.rise_trans(CALC_RISE | BIT_DISC_CENTER)` | REAL | ✅ | Upper limb + refraction |
| Sunset Delhi | ~18:43 IST | `swe.rise_trans(CALC_SET | BIT_DISC_CENTER)` | REAL | ✅ | Upper limb |
| Ayanamsa | ~24.14° | `swe.get_ayanamsa(jd)` | REAL | ✅ | Lahiri standard |
| Timezone | IST +5:30 | `if 68 ≤ lon ≤ 97.5: tz_offset = 5.5` | RULE | ✅ | Hardcoded for India band |

### 1.3 Tithi Calculation Logic

- Formula: `elongation = (moon_trop − sun_trop) % 360`; `tithi_index = int(elongation / 12.0)`
- Each tithi spans 12° of Moon–Sun elongation. **Correct per classical definition.**
- April 19 elongation ~224° → index 18 → **Tithi #19 = Krishna Chaturthi** (or Krishna Panchami depending on exact elongation at sunrise)

### 1.4 Nakshatra Calculation Logic

- Formula: `moon_sid / (360/27)` = `moon_sid / 13.3333`
- Moon at ~228° sidereal → index = 17 → **Jyeshtha** (226.66°–240°)
- **Correct per classical definition.**

### 1.5 Yoga Calculation Logic

- Formula: `(sun_sid + moon_sid) % 360 / (360/27)`
- Sun ~5.4°, Moon ~228° → sum ~233.4° → yoga_index = 17 → **Vyatipata (#18)**
- Vyatipata is marked `_BAD_YOGA_NUMBERS` in the engine. **Correct.**

### 1.6 Karana Calculation Logic

- Formula: `int(elongation / 6.0)` using actual elongation (not tithi-based approximation)
- Each karana = 6° of elongation. 60 karanas per lunar month. **Correct.**
- The engine correctly distinguishes first and second half of each tithi.

---

## 2. Panchang Core Output Audit

### 2.1 Tithi

| Field | Computation | Status | Issue |
|-------|-------------|--------|-------|
| Name & Number | `int(elongation / 12.0)` via SWE | ✅ REAL | — |
| Paksha | `"Shukla" if index < 15 else "Krishna"` | ✅ REAL | — |
| End time | Binary search (`_find_boundary_time`) on elongation | ✅ REAL | ±0.5 min tolerance |
| Lord | Lookup table `TITHI_LORD[number]` | RULE-BASED | — |
| Phala text | Static dict `TITHI_PHALA` | RULE-BASED | Static text only |
| Type (Nanda/Bhadra/Jaya) | **NOT EXPORTED** | ❌ GAP | Not in API response |

### 2.2 Nakshatra

| Field | Computation | Status | Issue |
|-------|-------------|--------|-------|
| Name & Index | `moon_sid / 13.333` via SWE | ✅ REAL | — |
| Pada | `int((lon % 13.333) / (13.333 / 4)) + 1` | ✅ REAL | — |
| End time | Binary search on Moon sidereal longitude | ✅ REAL | — |
| Lord | Lookup table | RULE-BASED | — |
| Category (Sthira/Chara/etc.) | `NAKSHATRA_CATEGORY` dict | RULE-BASED | Correct classical mapping |
| Deity | `NAKSHATRA_DEITY` dict | RULE-BASED | — |

**Note:** For April 19 — Nakshatra = **Jyeshtha** → Category = **Tikshna** (sharp/fierce). Deity = Indra.

### 2.3 Yoga & Karana

| Field | Computation | Status | Issue |
|-------|-------------|--------|-------|
| Yoga name | `(sun_sid + moon_sid) % 360 / (360/27)` | ✅ REAL | — |
| Yoga end time | Binary search on yoga angle | ✅ REAL | — |
| Yoga auspicious flag | `yoga_number not in {1,8,17,24,27}` | RULE-BASED | Set is inconsistent — `_BAD_YOGA_NUMBERS = {1,8,17,24,27}` but comment says Shoola is #9 not #8 |
| Karana name | `int(elongation / 6.0)` via SWE | ✅ REAL | — |
| Karana end time | Binary search on elongation (6° span) | ✅ REAL | — |
| Second karana end | Returns tithi end time — same as first boundary | ⚠️ WRONG | `_compute_second_karana_end` is identical to tithi end, not a true second karana end |

### 2.4 Sun/Moon Timings

| Element | Formula | Status | Issue |
|---------|---------|--------|-------|
| Sunrise | `swe.rise_trans(CALC_RISE | BIT_DISC_CENTER)` | ✅ REAL | — |
| Sunset | `swe.rise_trans(CALC_SET | BIT_DISC_CENTER)` | ✅ REAL | — |
| Moonrise | `swe.rise_trans(jd, MOON, CALC_RISE)` | ✅ REAL | — |
| Moonset | `swe.rise_trans(jd, MOON, CALC_SET)` | ✅ REAL | — |
| Moonrise (fallback) | `sunrise + 50 min` | ❌ WRONG | Completely arbitrary; off by hours when SWE unavailable |
| Moonset (fallback) | `sunset + 50 min` | ❌ WRONG | Same issue |

**Expected for Apr 19, 2026, Delhi:** Moonrise ~22:30–23:00 IST (waning gibbous, rising late), Moonset ~11:00–11:30 IST.

### 2.5 Derived Metrics

| Metric | Formula | Status |
|--------|---------|--------|
| Dinamana (day duration) | `sunset_mins − sunrise_mins` | ✅ REAL |
| Ratrimana (night duration) | `1440 − dinamana` | ✅ REAL |
| Madhyahna | `sunrise + dinamana / 2` | ✅ CORRECT |
| Weekday lord | `VARA_LORDS[weekday + 1]` | RULE-BASED |
| Vaar name | `_VAAR_NAMES[weekday]` | RULE-BASED |

### 2.6 Panchanga Shuddhi Score

**Formula:** Scores 5 limbs (0–20 each) → total 0–100.

| Limb | Rule | Max Score |
|------|------|-----------|
| Tithi | Good set {2,3,5,7,10,11,12,13} = 20; Bad {4,6,8,9,14} = 0 | 20 |
| Vara | Wed/Thu = 20; Sun/Mon/Fri = 15; Sat = 5; Tue = 0 | 20 |
| Nakshatra | Good set = 20; Bad set = 0; else 10 | 20 |
| Yoga | Vyatipata/Vaidhriti = 0; Excellent set = 20 | 20 |
| Karana | Bad set (Vishti etc.) = 0; Kimstughna = 5; else 20 | 20 |

**Assessment for Apr 19 (Sunday, Jyeshtha, Vyatipata likely):**
- Vara (Sunday) = 15
- Nakshatra (Jyeshtha) ∈ `_BAD_NAKSHATRAS` = **0**
- Yoga (Vyatipata) = **0**
- Tithi (Krishna Chaturthi/Panchami) = 0 or 20 depending on exact tithi
- **Estimated score: 20–35 → Label: "Weak" or "Inauspicious"**

**Verdict:** DYNAMIC — computes correctly from real data. Not static/hardcoded. ✅

---

## 3. Muhurat Engine Audit

### 3.1 Inauspicious Periods

#### Rahu Kaal

| Weekday | Slot | Formula | Apr 19 (Sunday) | Status |
|---------|------|---------|-----------------|--------|
| Slot map | `_RAHU_KAAL_SLOT = {6: 8}` (Sunday = slot 8) | `day / 8 × slot` | Last 1/8 of day | ✅ RULE-BASED |
| Day = ~12h 39min | 8 equal slots = ~94.9 min each | Slot 8 = ~18:28–19:53 IST | Dynamic from sunrise/sunset | ✅ CORRECT |

**Traditional rule:** Sunday Rahu Kaal = 4:30–6:00 PM (older fixed tables). Engine uses dynamic sunrise-relative calculation which is the preferred method. Acceptable.

#### Yamaganda

| Weekday | Slot | Status |
|---------|------|--------|
| Sunday (`weekday=6`) | `_YAMAGANDA_SLOT[6] = 8` | Wait — this is the same slot as Rahu Kaal for Sunday |

**BUG FOUND:** `_YAMAGANDA_SLOT = {6: 8}` — Sunday Yamaganda is assigned slot 8, same as Rahu Kaal Sunday. Traditional tables: Sunday Yamaganda = slot 5 (different from Rahu Kaal). This produces an **incorrect overlap**.

| Period | Traditional Sunday | Engine Sunday | Match? |
|--------|-------------------|---------------|--------|
| Rahu Kaal | Slot 8 | Slot 8 | ✅ |
| Yamaganda | Slot 5 | Slot 8 | ❌ WRONG |
| Gulika | Slot 7 | `_GULIKA_KAAL_SLOT[6] = 7` | ✅ |

#### Gulika Kaal

`_GULIKA_KAAL_SLOT = {0:6, 1:5, 2:4, 3:3, 4:2, 5:1, 6:7}` — Standard rule is **Saturday = slot 1** (Sun rises Gulika active from sunrise). Sunday = slot 7 matches tradition. ✅

#### Dur Muhurtam

```python
dur_start = sunrise_mins + muhurta_duration * 7  # always 8th muhurta
```

**SIMPLIFIED / INCORRECT:** Classical Dur Muhurtam varies by weekday:
- Not a fixed 8th muhurta — it's 2 specific muhurtas per day that differ by weekday.
- E.g., Sunday: muhurtas 5 and 8 are Dur Muhurtas; Monday: 6 and 7; etc.
- Engine uses a single fixed 8th muhurta regardless of day.

**Status: STATIC APPROXIMATION — not classically correct.**

#### Varjyam

```python
nak_num = nakshatra.get("index", 0) % 9
varjyam_offset = (nak_num * 2 + 1) * 60
varjyam_start = sunrise_mins + varjyam_offset % (dinamana_mins * 0.8)
varjyam = {"start": ..., "end": ... + 90}  # fixed 90 min window
```

**FAKE / APPROXIMATION:** Real Varjyam is derived from the 8th ghati (each ghati = 24 min) of each nakshatra's duration, counted from nakshatra start time. The engine instead uses a modulo formula on the nakshatra index — producing a number that correlates loosely but is not the actual classical calculation.

**Status: RULE-BASED APPROXIMATION — NOT the real Varjyam.**

### 3.2 Auspicious Periods

| Period | Formula | Status | Issue |
|--------|---------|--------|-------|
| Brahma Muhurat | `sunrise − 2×(ratrimana/15)` | ✅ CORRECT | Dynamic per sunrise |
| Abhijit Muhurat | `Day / 15 × 7` to `× 8` (8th muhurta) | ✅ CORRECT | Classical definition |
| Vijaya Muhurta | `sunrise + muhurta_duration × 6` | ✅ CORRECT | 7th muhurta |
| Godhuli Muhurta | `sunset − 24` to `sunset` | ⚠️ SIMPLIFIED | Traditional = 30 min, not 24 |
| Nishita Muhurta | `midnight ± 24 min` | ✅ CORRECT | — |
| Pratah Sandhya | `sunrise − 48` to `sunrise` | ✅ APPROXIMATELY CORRECT | — |
| Sayahna Sandhya | `sunset` to `sunset + 48` | ✅ APPROXIMATELY CORRECT | — |

**None of the above are hardcoded — all computed dynamically from sunrise/sunset.** ✅

### 3.3 Special Yogas (panchang_yogas.py)

| Yoga | Condition Logic | Type | Status |
|------|----------------|------|--------|
| Sarvartha Siddhi | Tithi + Nakshatra + Weekday table | RULE-BASED | ✅ Correct logic |
| Amrit Siddhi | Weekday + Nakshatra (1 nakshatra per day) | RULE-BASED | ✅ Correct |
| Dwipushkar | Tithi (2,7,12) + Weekday (Sun/Tue/Sat) + Nakshatra | RULE-BASED | ✅ |
| Tripushkar | Tithi (3,8,13) + Weekday (Sun/Tue/Sat) + Nakshatra | RULE-BASED | ✅ |
| Ravi Yoga | Sunday + Sun-ruled nakshatra | RULE-BASED | ✅ |
| Ganda Moola | 6 junction nakshatras (Ashwini, Ashlesha, Magha, Jyeshtha, Moola, Revati) | RULE-BASED | ✅ |
| Siddhi Yoga | Tithi category + Weekday | RULE-BASED | ✅ |
| Dagdha Tithi | Weekday→Tithi table (`DAGDHA_TITHIS`) | RULE-BASED | ✅ |
| Dagdha Nakshatra | Hindu month → nakshatra list | RULE-BASED | ✅ |
| Kula Yoga | `(tithi + vara + nak) % 9 == 0` | RULE-BASED | ✅ |
| Tithi-Vara Dosha | Dagdha/Visha/Hutasana/Krakacha/Samvartaka | RULE-BASED | ✅ Extended only |

**Weekday convention fix:** Engine correctly converts `dt.weekday()` (Mon=0) to Sun=0 convention via:
```python
weekday_sun = (weekday + 1) % 7
```
This is applied to `calculate_all_special_yogas` and `calculate_all_directions`. ✅

**Special Yoga for Apr 19 (Sunday, Jyeshtha):**
- Ravi Yoga: Sunday + Krittika/Uttara Phalguni/Uttara Ashadha → Jyeshtha NOT in list → **INACTIVE**
- Sarvartha Siddhi (Sunday): needs nakshatra in {Pushya, Hasta, Ashwini} → Jyeshtha → **INACTIVE**
- Amrit Siddhi (Sunday): needs Hasta → Jyeshtha → **INACTIVE**
- Ganda Moola: Jyeshtha IS in the list → **ACTIVE** (junction nakshatra Jyeshtha/Scorpio-Sagittarius boundary)

### 3.4 Panchaka

```python
panchaka_nakshatras = [22, 23, 24, 25, 26]  # Dhanishta to Revati
is_panchaka = moon_nak_idx in panchaka_nakshatras
panchaka = {"active": is_panchaka, "rahita": not is_panchaka}
```

**Issue:** The panchaka dict returned by the engine only has `{"active": bool, "rahita": bool}`. The Panchaka **type** (Mrityu/Agni/Raja/Chora/Roga) is computed in `panchang_misc.py:calculate_panchaka_rahita()` but stored separately under `misc.panchaka_rahita`, not merged into the top-level `panchaka` key.

**For Apr 19:** Jyeshtha (index 17) is NOT in panchaka indices [22-26] → **Panchaka INACTIVE**. ✅

---

## 4. Muhurat Finder Audit

### 4.1 Activity-Based Muhurat

The finder iterates all days in a month calling `calculate_panchang()` per day, then applies:

1. `check_day_favorable()` — Tithi/Nakshatra/Weekday/Month filter (hard gate)
2. Bhadra realm check (Moon rashi-aware)
3. Dagdha Tithi hard block
4. Sankranti window (±16 hours) block
5. Vyatipata/Vaidhriti Yoga (#17, #27) hard block
6. Visha Yoga hard block
7. Mrityu Yoga soft warning (−40 pts)
8. Activity-specific checks (Guru Asta, Shukra Asta, Kula Kanthaka, Simha Surya for marriage; Retrograde Jupiter/Saturn for samskaras)

**Status:** All rules are dynamically evaluated using real panchang data. ✅ **Not static.**

| Rule | Source Data | Type | Status |
|------|------------|------|--------|
| Rahu Kaal block | Dynamic from sunrise/sunset | REAL | ✅ |
| Bhadra realm | Moon rashi_index from SWE | REAL | ✅ |
| Guru Asta | Jupiter combusted flag from SWE | REAL | ✅ |
| Shukra Asta | Venus combusted flag from SWE | REAL | ✅ |
| Retrograde detection | Daily SWE longitude delta | REAL | ✅ |
| Simha Surya | Sun rashi_index from SWE | REAL | ✅ |
| Sankranti window | `find_sankranti_times(year)` | REAL | ✅ |
| Kula Kanthaka | Mars house from Moon (both from SWE) | REAL | ✅ |

### 4.2 Lagna Windows

- Engine samples ascendant every **5 minutes for 24 hours** (289 samples).
- Uses proper GMST formula: `gmst = 280.46061837 + 360.98564736629 × (JD − 2451545.0)`
- Applies ayanamsa correction for sidereal zodiac.
- Detects sign boundaries by scanning for sign index changes.
- Annotates Ganda (first 3°20') and Sandhi (last 3°20').
- Adds safe sub-windows trimming 14 minutes from each end.

**Status:** REAL astronomical calculation. ✅ Not hardcoded.

**Issue:** 5-minute sampling gives ±5 min precision at sign boundaries. For a ~2h lagna window this is acceptable (~4% error).

### 4.3 Chandra Balam

```python
house = ((current_moon_ridx − birth_moon_rashi) % 12) + 1
favorable = house in {1, 3, 6, 7, 10, 11}
```

- Current moon rashi from real SWE position. ✅
- Classical favorable houses: 1, 3, 6, 7, 10, 11. ✅ (matches traditional Muhurta Chintamani)
- Interpretation text from `_CHANDRA_BALAM_FRUITS` — correct per house.

**Status:** REAL (current moon) + RULE-BASED (favorable house list). ✅

### 4.4 Tara Balam

```python
tara = ((nak_index − birth_nakshatra) % 9) + 1
```

- 9-tara cycle: Janma(1), Sampat(2), Vipat(3), Kshema(4), Pratyari(5), Sadhaka(6), Vadha(7), Mitra(8), Ati-Mitra(9)
- Favorable: {2, 4, 6, 8, 9} ✅ matches classical definition.
- Current nakshatra from real SWE. ✅

**Status:** REAL + RULE-BASED. ✅

### 4.5 Scoring Logic

```python
# Positive factors
favorable_tithi   → +20
favorable_vara    → +15
favorable_nakshatra → +25
auspicious yoga   → +10
non-Vishti karana → +5
Sarvartha Siddhi  → +20
Amrit Siddhi      → +20

# Negative factors
rahu_kaal_active  → −30
avoid_tithi       → −25
avoid_vara        → −20
avoid_nakshatra   → −25
```

**Flaw in Rahu Kaal flag:** The scorer marks `rahu_kaal_active = True` if rahu_kaal dict has start/end keys (it always does). This means **Rahu Kaal is always considered "active" in the scoring function**, deducting 30 points from every day. The intent was to check if the proposed muhurat time falls within Rahu Kaal, but there's no time comparison — it always penalises.

**Status: SCORING BUG — Rahu Kaal penalty applied to every date regardless of time.**

### 4.6 Rule Engine (Avoidance Conditions)

| Condition | Implemented? | Method |
|-----------|-------------|--------|
| Rahu Kaal exclusion | ✅ | Dynamic sunrise-relative |
| Bhadra exclusion | ✅ | Moon rashi-aware realm check |
| Panchaka exclusion | ✅ | Nakshatra index check |
| Ganda Moola | ✅ | 6-nakshatra list |
| Sankranti (±16h) | ✅ | `find_sankranti_times()` |
| Guru/Shukra Asta | ✅ | SWE combustion check |
| Dagdha Tithi | ✅ | Weekday→Tithi table |
| Retrograde Jupiter | ✅ | SWE daily delta |
| Retrograde Saturn | ✅ | SWE daily delta |
| Simha Surya | ✅ | SWE sun rashi |
| Vyatipata/Vaidhriti | ✅ | Yoga number check |
| Visha Yoga | ✅ | Tithi+Weekday table |
| Mrityu Yoga | ✅ (soft) | Tithi+Weekday table |
| Kula Kanthaka | ✅ | Mars/Moon rashi from SWE |
| Chaturmasa | ❌ MISSING | Not checked in finder |
| Guru Rashi filter | ✅ (marriage only) | SWE rashi check |
| Shukra Rashi filter | ✅ (marriage only) | SWE rashi check |

---

## 5. Dynamic vs Static Detection — Complete Classification

| Module | Output | Classification | Evidence |
|--------|--------|----------------|---------|
| Sunrise / Sunset | HH:MM | ✅ REAL (SWE) | `swe.rise_trans` |
| Moonrise / Moonset | HH:MM | ✅ REAL (SWE) or ❌ WRONG (fallback) | SWE good; fallback += 50min |
| Tithi name+number | string | ✅ REAL | `int(elongation / 12)` |
| Tithi end time | HH:MM | ✅ REAL | Binary search |
| Tithi lord | string | RULE-BASED | Static table |
| Nakshatra name+pada | string | ✅ REAL | SWE moon_sid / 13.333 |
| Nakshatra end time | HH:MM | ✅ REAL | Binary search |
| Yoga name | string | ✅ REAL | SWE (sun+moon)/360×27 |
| Yoga end time | HH:MM | ✅ REAL | Binary search |
| Karana name | string | ✅ REAL | elongation/6 |
| Second karana end | HH:MM | ⚠️ BUG | Returns tithi end, not karana boundary |
| Rahu Kaal | HH:MM–HH:MM | RULE-BASED (dynamic) | Day/8 × weekday slot |
| Yamaganda | HH:MM–HH:MM | ⚠️ WRONG SLOT (Sunday) | Slot 8 = same as Rahu Kaal |
| Gulika Kaal | HH:MM–HH:MM | RULE-BASED (dynamic) | Day/8 × weekday slot |
| Abhijit Muhurat | HH:MM–HH:MM | ✅ CORRECT | Day/15, 8th muhurta |
| Brahma Muhurat | HH:MM–HH:MM | ✅ CORRECT | Dynamic ratrimana |
| Dur Muhurtam | HH:MM–HH:MM | ❌ SIMPLIFIED | Fixed 8th muhurta, not weekday-specific |
| Varjyam | HH:MM–HH:MM | ❌ APPROXIMATION | Index-based formula, not classical |
| Vijaya Muhurta | HH:MM–HH:MM | ✅ CORRECT | 7th muhurta |
| Godhuli Muhurta | HH:MM–HH:MM | ⚠️ OFF BY 6 MIN | 24 min before sunset, should be 30 |
| Nishita Muhurta | HH:MM–HH:MM | ✅ CORRECT | Midnight ± 24 min |
| Planetary positions | longitude/rashi | ✅ REAL | SWE calc_ut |
| Retrograde detection | bool | ✅ REAL | Daily SWE delta |
| Combustion detection | bool | ✅ REAL | Orb table vs SWE angle |
| Sarvartha Siddhi | active/inactive | RULE-BASED | Tithi+Nak+Weekday tables |
| Amrit Siddhi | active/inactive | RULE-BASED | Weekday+Nakshatra |
| Dwipushkar | active/inactive | RULE-BASED | 3-condition check |
| Tripushkar | active/inactive | RULE-BASED | 3-condition check |
| Ganda Moola | active/inactive | RULE-BASED | 6-nakshatra list |
| Ravi Yoga | active/inactive | RULE-BASED | Sunday+3 nakshatras |
| Dagdha Tithi | active/inactive | RULE-BASED | Weekday→Tithi table |
| Panchaka | active/inactive | REAL | SWE moon nakshatra index |
| Panchaka type | string | ✅ REAL | `panchang_misc.py` (separate key) |
| Lagna table | sign+time windows | ✅ REAL | GMST+ASC formula, 5-min sampling |
| Ganda/Sandhi lagna | flag | ✅ REAL | Degree check < 3.333° or > 26.667° |
| Chandra Balam | house+label | REAL+RULE | SWE moon + classical houses |
| Tara Balam | tara+label | REAL+RULE | SWE nak + (idx−birth)%9 |
| Panchanga Shuddhi | 0–100 score | REAL+RULE | Dynamic from real elements |
| Hindu Calendar (Samvat) | year string | RULE-BASED | `year + 57 / − 78` |
| Hora table | 24 entries | RULE-BASED (dynamic) | Weekday lord rotation |
| Choghadiya (day) | 8 periods | RULE-BASED (dynamic) | Weekday sequence table |
| Choghadiya (night) | 8 periods | RULE-BASED (dynamic) | Weekday sequence table |
| Gowri Panchang | 16 periods | RULE-BASED (dynamic) | Fixed name lists |
| Do Ghati Muhurta | 30 periods | RULE-BASED | Static name list |

---

## 6. Engine Health Dashboard

| Module | Status | Real Output? | Critical Issue |
|--------|--------|-------------|----------------|
| Tithi engine | 🟢 HEALTHY | Yes (SWE) | None |
| Nakshatra engine | 🟢 HEALTHY | Yes (SWE) | None |
| Yoga engine | 🟢 HEALTHY | Yes (SWE) | Bad yoga set has minor inconsistency (#8) |
| Karana engine | 🟢 HEALTHY | Yes (SWE) | Second karana end time returns tithi end |
| Sunrise/Sunset | 🟢 HEALTHY | Yes (SWE) | None |
| Moonrise/Moonset | 🟡 PARTIAL | Yes (SWE) / Wrong (fallback) | Fallback completely wrong |
| Rahu Kaal | 🟢 HEALTHY | Dynamic | None |
| Gulika Kaal | 🟢 HEALTHY | Dynamic | None |
| Yamaganda | 🔴 BUG | Dynamic | Sunday slot = 8, should be 5 |
| Abhijit Muhurat | 🟢 HEALTHY | Derived | None |
| Brahma Muhurat | 🟢 HEALTHY | Derived | None |
| Dur Muhurtam | 🟡 SIMPLIFIED | No — fixed 8th | Not weekday-specific |
| Varjyam | 🔴 FAKE | No — index formula | Not the classical calculation |
| Godhuli | 🟡 MINOR | Derived | 24 min window vs 30 min classical |
| Planetary positions | 🟢 HEALTHY | Yes (SWE) | None |
| Combustion check | 🟢 HEALTHY | Yes (SWE) | None |
| Special Yogas | 🟢 HEALTHY | Rule-based | Weekday convention correctly converted |
| Panchaka | 🟡 PARTIAL | Yes (active flag) | Type (Mrityu/Agni etc.) in separate dict |
| Lagna table | 🟢 HEALTHY | Yes (GMST formula) | ±5 min precision |
| Chandra/Tara Balam | 🟢 HEALTHY | Real+Rule | None |
| Panchanga Shuddhi | 🟢 HEALTHY | Derived | None |
| Muhurat Finder | 🟡 MINOR BUG | Mostly real | Rahu Kaal scoring flag always true |
| Choghadiya | 🟢 HEALTHY | Dynamic | None |
| Hora table | 🟢 HEALTHY | Dynamic | None |

---

## 7. Critical Bugs & Gaps

### BUG-01: Yamaganda Sunday Slot Incorrect
**File:** `app/panchang_engine.py` line ~480
**Code:** `_YAMAGANDA_SLOT = {6: 8}`
**Issue:** Sunday Yamaganda mapped to slot 8, same as Sunday Rahu Kaal. Traditional: Sunday Yamaganda = slot 5.
**Impact:** Yamaganda and Rahu Kaal display identical times on Sundays.
**Fix:** `_YAMAGANDA_SLOT[6] = 5`

### BUG-02: Varjyam Is Not Real
**File:** `app/panchang_engine.py` lines ~1633–1638
**Code:**
```python
nak_num = nakshatra.get("index", 0) % 9
varjyam_offset = (nak_num * 2 + 1) * 60
varjyam_start = sunrise_mins + varjyam_offset % (dinamana_mins * 0.8)
```
**Issue:** This is an invented formula, not classical Varjyam. Real Varjyam = 8th ghati of nakshatra duration, counted from nakshatra start time.
**Impact:** Varjyam times are always wrong. This is **UI DECORATIVE** data, not classical.
**Fix:** Compute from nakshatra start time and duration. Varjyam window = nakshatra_start + 7×(nak_duration/9) for 24 min duration.

### BUG-03: Rahu Kaal Scoring Flag Always True
**File:** `app/muhurat_finder.py` line ~496–498
**Code:**
```python
rahu_kaal_dict = panchang.get("rahu_kaal", {}) or {}
rahu_kaal_active_flag = bool(rahu_kaal_dict.get("start") and rahu_kaal_dict.get("end"))
```
**Issue:** `rahu_kaal` always has start/end keys → flag is always `True` → always deducts 30 pts.
**Impact:** Every date loses 30 points in muhurat scoring regardless of what time the muhurat falls in. Scores are systematically suppressed.
**Fix:** Compare proposed muhurat time against Rahu Kaal window, or remove the penalty from day-level scoring.

### BUG-04: Second Karana End Time Incorrect
**File:** `app/panchang_engine.py` function `_compute_second_karana_end`
**Code:** Returns tithi boundary (same as tithi end), not the actual second karana boundary.
**Issue:** Second karana end = midpoint between first karana end and tithi end. The function calls `_find_boundary_time` with same parameters as tithi, so returns identical value.
**Impact:** Second karana start/end times are wrong; first karana end = second karana end = tithi end.

### BUG-05: Moonrise/Moonset Fallback Is Meaningless
**File:** `app/panchang_engine.py` lines ~703–710
**Code:**
```python
"moonrise": _minutes_to_time(sr_min + 50),
"moonset": _minutes_to_time(_time_to_minutes(ss) + 50),
```
**Issue:** When SWE not available, moonrise = sunrise + 50 min. Real moonrise for waning gibbous on Apr 19 ≈ 22:30. This is off by ~16 hours.
**Impact:** Only when SWE is unavailable; production with SWE installed is fine.

### BUG-06: Dur Muhurtam Is Not Weekday-Specific
**File:** `app/panchang_engine.py` line ~1630
**Code:** `dur_start = sunrise_mins + muhurta_duration * 7`
**Issue:** Classical Dur Muhurtam differs by weekday (2 specific muhurtas per day, day-dependent). Engine always uses the 8th muhurta.
**Impact:** Incorrect Dur Muhurtam window. Displays plausible-looking but wrong times.
**Status:** UI DECORATIVE for now.

### GAP-01: Chaturmasa Not Checked in Muhurat Finder
**File:** `app/muhurat_finder.py`
**Issue:** `calculate_chaturmasa()` exists in `panchang_misc.py` but muhurat finder never calls it. Chaturmasa (Ashadh Shukla 11 to Kartik Shukla 11) prohibits major samskaras.
**Impact:** Marriage, Griha Pravesh etc. may be suggested during Chaturmasa months.

### GAP-02: Tithi Type Not Exported
**Issue:** Nanda/Bhadra/Jaya/Rikta/Purna classification not in API response for panchang. Only available implicitly via tithi number.

### GAP-03: Panchaka Type Not in Top-Level Dict
**Issue:** `panchang["panchaka"]` only has `{"active": bool, "rahita": bool}`. The type (Mrityu/Agni/Raja/Chora/Roga) is in `panchang["misc"]["panchaka_rahita"]` — split across two locations.

### GAP-04: Active-Now Logic for Inauspicious Periods
**Issue:** No endpoint or flag indicates whether the current time falls within Rahu Kaal, Varjyam, etc. The "active now" display on the frontend cannot be dynamically correct without a time parameter in the API.

---

## 8. Accuracy Verdict

| Dimension | Score | Reasoning |
|-----------|-------|-----------|
| **Astronomical Accuracy** | 8.5/10 | SWE-powered; Lahiri ayanamsa; correct formulas for tithi/nakshatra/yoga/karana. Deductions: wrong second karana end, Yamaganda Sunday slot error. |
| **Panchang Reliability** | 7.5/10 | Core 5 limbs are real. End times via binary search are solid. Gaps: Dur Muhurtam fake, Varjyam fake, tithi type not exported. |
| **Muhurat Reliability** | 7/10 | Hard avoidance rules are comprehensive and real-data-driven. Scoring has Rahu Kaal flag bug. Chaturmasa gap. |
| **Production Readiness** | 72% | Suitable for informational use. Not yet reliable for scheduling critical samskaras (marriage, upanayana) without fixing BUG-01, BUG-03, and GAP-01. |

---

## 9. Final Verdict

### Is the Panchang engine real or fake?
**REAL** — The core five limbs (Tithi, Nakshatra, Yoga, Karana, Vara) are computed from Swiss Ephemeris using correct classical formulas. Sunrise/Sunset/Moonrise/Moonset are SWE-powered. Planetary positions use true sidereal longitudes with Lahiri ayanamsa. End times use binary search on actual ephemeris data. The engine is **not fake** and not hardcoded.

### Is the Muhurat engine rule-based or static?
**RULE-BASED with real-data inputs** — Muhurat finder evaluates 15+ avoidance conditions dynamically using real panchang data per day. It is not static. The activity rules (favorable tithis, nakshatras, weekdays) are hardcoded tables, which is correct per classical Jyotish texts (Muhurta Chintamani). These rules are not "fake" — they are the textual rules themselves.

### Can it be trusted for real-world usage?
**Yes for informational display.** With caveats:
- ✅ Trust: Tithi, Nakshatra, Yoga, Karana, Sunrise/Sunset, Planetary positions, Abhijit, Brahma Muhurat, Choghadiya, Hora table, Lagna windows, Chandra/Tara Balam
- ⚠️ Use with caution: Rahu Kaal (correct formula, Sunday Yamaganda wrong), Muhurat scoring (Rahu Kaal flag bug)
- ❌ Do not trust: Varjyam, Dur Muhurtam (not classical calculations)

### What must be fixed before production-grade trust?

**Priority 1 (Critical):**
1. Fix Yamaganda Sunday slot: `_YAMAGANDA_SLOT[6] = 5`
2. Fix Varjyam to use classical ghati-based calculation from nakshatra start time
3. Fix Rahu Kaal scoring flag in muhurat finder

**Priority 2 (High):**
4. Add Chaturmasa check in muhurat finder
5. Fix second karana end time computation
6. Fix Dur Muhurtam to be weekday-specific

**Priority 3 (Medium):**
7. Export tithi type (Nanda/Bhadra/Jaya/Rikta/Purna) in panchang response
8. Merge panchaka type into top-level panchaka dict
9. Add time-aware "active now" flag for inauspicious periods
10. Extend Godhuli window to 30 min (traditional) instead of 24 min

---

*Report generated: 2026-04-19 | Engine version: production branch | Auditor: Claude Sonnet 4.6*
