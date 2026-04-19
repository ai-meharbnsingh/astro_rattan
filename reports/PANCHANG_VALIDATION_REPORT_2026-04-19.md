
# Astrorattan Panchang & Muhurat Validation Report

**Generated**: 2026-04-19 13:55:21 IST

**Subject**: Meharban Singh

**Target Date**: 2026-04-19

**Location**: Delhi, India (Lat: 28.6139, Lon: 77.209, TZ: +5.5)

**Engine API**: http://localhost:8000

**Report Type**: Technical Audit — NOT user-facing

**Validation Method**: Direct engine calls + API layer verification + cross-calculation


---


# 1. Astronomical Base Validation

**Data Source**: Swiss Ephemeris (libswe) + Lahiri Ayanamsa

**Ayanamsa (Lahiri)**: 24.2244° (Valid range: 23.0°–25.5° for 2000-2050)

**Sun Longitude (engine)**: 4.7459°

**Moon Longitude (engine)**: 25.8572°

**Sun Longitude (swe direct)**: 4.7513°  — independent cross-check

**Moon Longitude (swe direct)**: 25.9402°  — independent cross-check

**Ayanamsa (swe direct)**: 24.2244°  — independent cross-check


| Element | Engine Output | Independent Computation | Method | Consistent? | Notes |
| --- | --- | --- | --- | --- | --- |
| Sunrise | 05:52 | 05:54 (solar geometry) | Swiss Ephemeris (SWE) | ✅ YES | Diff: 2.5min (tolerance ±15min) |
| Sunset | 18:48 | 18:49 (solar geometry) | Swiss Ephemeris (SWE) | ✅ YES | Diff: 1.3min (tolerance ±15min) |
| Moonrise | 06:49 | Computed from SWE (varies by date) | Swiss Ephemeris | ✅ COMPUTED |  |
| Moonset | 21:11 | Computed from SWE (varies by date) | Swiss Ephemeris | ✅ COMPUTED |  |
| Ayanamsa | 24.2244 | 24.2244° (swe direct) | Lahiri SIDM_LAHIRI mode | ✅ YES | Diff: 0.0° |
| Sun Longitude | 4.7459 | 4.7513° (swe direct) | SWE calc_ut | ✅ YES | Diff within 1° (engine uses sunrise JD, swe direct uses 6AM) |
| Moon Longitude | 25.8572 | 25.9402° (swe direct) | SWE calc_ut | ✅ YES | Diff within 3° (moon moves fast; engine uses sunrise JD) |
| Moon Phase (independent) | Waxing (Shukla) — elongation 21.2° | Engine tithi paksha: Shukla | swe direct elongation (swe direct (INDEPENDENT)) | ✅ YES | Mismatch = engine tithi paksha wrong |
| Tithi (from longitudes) | Dwitiya (Shukla) | Engine reports: Dwitiya | elongation/12 → tithi index | ✅ YES | Cross-check: independent vs engine |
| Nakshatra (from moon_lon) | Bharani | Engine reports: Bharani | moon_lon / (360/27) | ✅ YES | Note: engine uses sunrise-moment moon |
| Yoga (from sun+moon) | Ayushman | Engine reports: Ayushman | (sun+moon) / (360/27) | ✅ YES | Cross-check |


---


# 2. Panchang Core Output Audit


## 2.1 Tithi

| Field | Value | Correct? | Notes |
| --- | --- | --- | --- |
| Name | Dwitiya | ✅ YES |  |
| Number (1-30) | 2 | ✅ YES |  |
| Paksha | Shukla | ✅ YES |  |
| End Time | 10:49 | ✅ YES | Binary-search boundary |
| Lord | Mars | ✅ YES | From TITHI_LORD table |
| Type (Nanda/Bhadra/...) | Bhadra | ✅ YES | Expected: Bhadra — 5-cycle pattern |
| Consistent with elongation? | Dwitiya Shukla | ✅ YES | Cross-check: computed=Dwitiya (Shukla) |

**Calculation Method**: elongation = (Moon_sid - Sun_sid) % 360; tithi_index = int(elongation / 12); boundary via binary search on JD.


## 2.2 Nakshatra

| Field | Value | Correct? | Notes |
| --- | --- | --- | --- |
| Name | Bharani | ✅ YES |  |
| Pada (1-4) | 4 | ✅ YES |  |
| Lord (Ruling Planet) | Venus | ✅ YES |  |
| Category | ugra | ✅ YES | Dhruva/Chara/Ugra/etc. |
| End Time | 07:10 | ✅ YES | Binary-search on Moon longitude |
| Consistent with moon_lon? | Bharani | ✅ YES | Cross-check: computed=Bharani |

**Calculation Method**: Moon sidereal longitude / (360/27) = nakshatra index; pada = sub-division within 13°20' span.


## 2.3 Yoga

| Field | Value | Correct? | Notes |
| --- | --- | --- | --- |
| Name | Ayushman | ✅ YES |  |
| Number (1-27) | 3 | ✅ YES |  |
| End Time | 20:01 | ✅ YES | Binary-search |
| Quality Field | good | ✅ YES | Must be 'bad' for Vyatipata/Vaidhriti etc. |
| Auspicious Flag | True | ✅ YES | Expected: True |

**Calculation Method**: yoga_sum = (Sun_sid + Moon_sid) % 360; yoga_index = int(yoga_sum / 13.333...)


## 2.4 Karana

| Field | Value | Correct? | Notes |
| --- | --- | --- | --- |
| Name | Kaulava | ✅ YES |  |
| Number (1-60) | 4 | ✅ YES |  |
| End Time | 10:49 | ✅ YES | Half-tithi boundary |
| Is Vishti | False | N/A (check if Vishti) | Inauspicious karana |
| Type (chara/sthira) | chara | ✅ YES | Expected: chara |
| Second Karana | Taitila | ✅ YES | Second half-tithi |

**Calculation Method**: elongation % 12 → first vs second half of tithi → maps to 60-karana cycle (7 chara repeating + 4 sthira fixed).


## 2.5 Sun/Moon Timings

| Timing | Reported | Formula Expected (±15min) | Diff (min) | Correct? |
| --- | --- | --- | --- | --- |
| Sunrise | 05:52 | 05:54 | 2.5 | ✅ YES |
| Sunset | 18:48 | 18:49 | 1.3 | ✅ YES |
| Moonrise | 06:49 | Computed (SWE) | N/A | ✅ REAL |
| Moonset | 21:11 | Computed (SWE) | N/A | ✅ REAL |


## 2.6 Derived Metrics

| Metric | Reported | Computed | Correct? |
| --- | --- | --- | --- |
| Dinamana (Day duration) | 12 Hours 56 Mins | ~12h 56m | ✅ REAL |
| Ratrimana (Night duration) | 11 Hours 4 Mins | ~11h 4m | ✅ REAL |
| Madhyahna (Solar noon) | 12:20 | 12:20 | ✅ REAL |
| Weekday | Sunday | Sunday | ✅ YES |
| Weekday Lord | Sun | Derived from weekday | ✅ RULE-BASED |


## 2.7 Hindu Calendar

| Field | Value | Present? |
| --- | --- | --- |
| Vikram Samvat | 2083 | ✅ YES |
| Hindu Month (Maas) | Vaishakha | ✅ YES |
| Paksha | Shukla | ✅ YES |
| Shaka Samvat | 1948 | ✅ YES |
| Ritu (Season) | Vasanta | ✅ YES |
| Ayana | Uttarayana | ✅ YES |


## 2.8 Panchanga Shuddhi Score

| Component | Score (0-20) | Rules Applied |
| --- | --- | --- |
| Tithi | 20 | Nanda/Jaya/Purna=20, Rikta=0, Ashtami/Navami=0 |
| Vara (Weekday) | 15 | Mon/Wed/Thu/Fri=20, Sun=15, Tue=10, Sat=5 |
| Nakshatra | 0 | Good nakshatras=20, Bad=0, Others=10 |
| Yoga | 15 | Vyatipata/Vaidhriti=0, Bad=5, Excellent=20, Others=15 |
| Karana | 20 | Vishti/Bhadra=0, Kimstughna=5, Others=20 |
| **TOTAL** | **70/100** | Label: Good |

| Check | Result |
| --- | --- |
| Score = sum of breakdown? | ✅ YES |
| Label matches threshold? | ✅ YES |
| Is dynamic (date-dependent)? | ✅ YES — depends on Tithi/Vara/Nak/Yoga/Karana |


---


# 3. Muhurat Engine Audit


## 3.1 Inauspicious Periods


### 3.1.1 Rahu Kaal

| Field | Value |
| --- | --- |
| Day (Weekday) | Sunday (slot 8/8) |
| Reported Start | 17:11 |
| Reported End | 18:48 |
| Expected Start (manual) | 17:11 |
| Expected End (manual) | 18:48 |
| Start Diff (min) | 0.0 |
| End Diff (min) | 0.0 |
| Start Correct? | ✅ YES |
| End Correct? | ✅ YES |
| Has active_now flag? | ✅ YES |
| Slot Duration (min) | 97.0 |

**Formula**: day = sunrise→sunset / 8 equal slots; Sunday = slot 8


### 3.1.2 Yamaganda

| Field | Value |
| --- | --- |
| Slot | 5/8 |
| Reported | 12:20 – 13:57 |
| Expected | 12:20 – 13:57 |
| Diff (min) | 0.0 / 0.0 |
| Correct? | ✅ YES |
| active_now? | ✅ YES |


### 3.1.3 Gulika Kaal

| Field | Value |
| --- | --- |
| Slot | 7/8 |
| Reported | 15:34 – 17:11 |
| Expected | 15:34 – 17:11 |
| Diff (min) | 0.0 / 0.0 |
| Correct? | ✅ YES |


### 3.1.4 Dur Muhurtam

| Field | Value |
| --- | --- |
| Weekday | Sunday |
| Slot Index (0-based) | 13 |
| Muhurta Duration (min) | 51.7 |
| Reported | 17:04 – 17:56 |
| Expected | 17:04 – 17:56 |
| Diff (min) | 0.5 / 0.3 |
| Correct? | ✅ YES |
| Has Second Slot? | ❌ NO |


### 3.1.5 Varjyam

| Field | Value |
| --- | --- |
| Reported Start | 17:52 |
| Reported End | 19:18 |
| Is Computed (not --:--)? | ✅ YES |
| Method | Tyajya ghati formula per nakshatra (verified against Drik Panchang) |

**Formula**: varjyam_start = nak_start + ((tyajya_ghati-1)/60) × nak_duration; duration = (4/60) × nak_duration. Tyajya ghati is nakshatra-specific (27 values).


## 3.2 Auspicious Periods


### 3.2.1 Brahma Muhurat

| Field | Value |
| --- | --- |
| Reported | 04:23 – 05:07 |
| Expected (dynamic formula) | 04:23 – 05:07 |
| Night Muhurta Duration (min) | 44.27 |
| Start Diff (min) | 0.5 |
| End Diff (min) | 0.7 |
| Correct? | ✅ YES |
| active_now? | ✅ YES |
| Formula | Dynamic formula: ratrimana/15 per muhurta (Drik Panchang standard) |


### 3.2.2 Abhijit Muhurat

| Field | Value |
| --- | --- |
| Reported | 11:54 – 12:45 |
| Expected (8th muhurta of 15) | 11:54 – 12:45 |
| Start Diff (min) | 0.1 |
| Correct? | ✅ YES |
| active_now? | ✅ YES |

**Formula**: 8th muhurta = sunrise + 7 × (dayduration/15); skipped on Wednesday (classical rule).


### 3.2.3 Vijaya Muhurta

| Field | Value |
| --- | --- |
| Reported Start | 11:02 |
| Reported End | 11:54 |
| Formula | 7th muhurta = sunrise + 6 × (dayduration/15) |
| Present? | ✅ YES |


### 3.2.4 Godhuli Muhurta

| Field | Value |
| --- | --- |
| Reported | 18:18 – 18:48 |
| Expected | 18:18 – 18:48 |
| Start Diff (min) | 0 |
| Correct? | ✅ YES |

**Formula**: 30 minutes before sunset (classical: dust of cattle hooves).


### 3.2.5 Nishita Muhurta

| Field | Value |
| --- | --- |
| Midnight Computed | 00:20 |
| Reported | 23:56 – 00:44 |
| Expected | 23:56 – 00:44 |
| Start Diff (min) | 0.0 |
| Correct? | ✅ YES |


## 3.3 Special Yogas

| Yoga | Active? | Method | Condition Verified? |
| --- | --- | --- | --- |
| Sarvartha Siddhi | ❌ NO | RULE-BASED: Nakshatra+Tithi+Weekday combo (Muhurta Chintamani) | ✅ YES |
| Amrit Siddhi | ❌ NO | RULE-BASED: Specific nakshatra for each weekday | ✅ YES |
| Dwipushkar | ❌ NO | RULE-BASED: 3-way condition (weekday+tithi+nakshatra) | N/A (3-way logic) |
| Tripushkar | ✅ YES | RULE-BASED: 3-way condition (weekday+tithi+nakshatra) | N/A (3-way logic) |
| Ganda Moola | ❌ NO | RULE-BASED: Specific nakshatras (Ashwini,Magha,Mula,Jyeshtha,Revati,Ashlesha) | N/A |
| Ravi Yoga | ❌ NO | Sunday + Sun-ruled Nakshatra (Krittika/UttPhalguni/UttAshadha) | ✅ YES |


## 3.4 Panchaka

| Field | Value |
| --- | --- |
| Nakshatra | Bharani |
| Is Panchaka Nakshatra? | ❌ NO |
| Expected Type | None |
| Reported Active? | ❌ NO |
| Reported Type | None |
| Logic Correct? | ✅ YES |
| Method | RULE-BASED: Last 5 nakshatras of the zodiac |


---


# 4. Muhurat Finder Audit


## 4.1 Activity-Based Muhurat (API: /api/panchang/muhurat)


### 4.1.1 Marriage

| Field | Value |
| --- | --- |
| API Reachable? | ✅ YES |
| Dates Returned | 11 |
| Sample Date | 2026-04-02 |
| Sample Time Range | Sunrise to Sunset (Purnima Hasta) |
| Sample Quality | auspicious |
| Filtering Logic | Shukla paksha tithis, excludes Ashtami/Navami/Chaturdashi |
| Is Dynamic? | ✅ YES — computed month-by-month from panchang |


### 4.1.2 Business Start

| Field | Value |
| --- | --- |
| API Reachable? | ✅ YES |
| Dates Returned | 11 |
| Sample Date | 2026-04-02 |
| Sample Time Range | Sunrise to Sunset (Purnima Hasta) |
| Sample Quality | auspicious |
| Filtering Logic | Shukla paksha tithis, excludes Ashtami/Navami/Chaturdashi |
| Is Dynamic? | ✅ YES — computed month-by-month from panchang |


### 4.1.3 Griha Pravesh

| Field | Value |
| --- | --- |
| API Reachable? | ✅ YES |
| Dates Returned | 11 |
| Sample Date | 2026-04-02 |
| Sample Time Range | Sunrise to Sunset (Purnima Hasta) |
| Sample Quality | auspicious |
| Filtering Logic | Shukla paksha tithis, excludes Ashtami/Navami/Chaturdashi |
| Is Dynamic? | ✅ YES — computed month-by-month from panchang |


## 4.2 Lagna Windows

| Field | Value |
| --- | --- |
| Present? | ✅ YES |
| Entry Count | 13 |
| Unique Signs | 12 |
| Avg Duration (min) | 110.8 |
| Ganda/Sandhi Detected | 1 |
| Method | REAL: Ascendant computed from sidereal time + LST formula |
| Count OK (10-14 for 24h)? | ✅ YES |

**Sample Lagna Entries**:

| Lagna (Sign) | Start | End | Duration (min) | Status |
| --- | --- | --- | --- | --- |
| Mesha | 05:52 | 07:17 | 85 | ✅ Safe |
| Vrishabha | 07:17 | 09:17 | 120 | ✅ Safe |
| Mithuna | 09:17 | 11:32 | 135 | ✅ Safe |
| Karka | 11:32 | 13:52 | 140 | ✅ Safe |
| Simha | 13:52 | 16:07 | 135 | ✅ Safe |
| Kanya | 16:07 | 18:22 | 135 | ✅ Safe |


## 4.3 Chandra Balam

| Field | Value |
| --- | --- |
| Present? | ✅ YES |
| Birth Rashi | Mesha |
| Transit Moon | Mesha |
| House from Moon | 1 |
| Favorable? | True |
| Method | RULE-BASED: Transit moon house from natal moon rashi (all 12 rashis returned) |
| Has Favorable Flag? | ✅ YES |


## 4.4 Tara Balam

| Field | Value |
| --- | --- |
| Present? | ✅ YES |
| Tara Name | Ati-Mitra |
| Tara Number (1-9) | 9 |
| Favorable? | True |
| Birth Nakshatra | Ashwini |
| Method | RULE-BASED: Count from birth nakshatra to transit nakshatra mod 9 |
| OK? | ✅ YES |


## 4.5 Choghadiya

| Check | Value |
| --- | --- |
| Day Choghadiya count | 8 |
| Night Choghadiya count | 8 |
| Expected per period | 8 |
| Day count OK? | ✅ YES |
| Night count OK? | ✅ YES |
| Method | RULE-BASED: 8 slots × weekday-specific quality pattern |

**Day Choghadiya entries**:

| Slot # | Name | Quality | Start | End |
| --- | --- | --- | --- | --- |
| 1 | Udveg | Inauspicious | 05:52 | 07:29 |
| 2 | Char | Neutral | 07:29 | 09:06 |
| 3 | Labh | Good | 09:06 | 10:43 |
| 4 | Amrit | Best | 10:43 | 12:20 |
| 5 | Kaal | Inauspicious | 12:20 | 13:57 |
| 6 | Shubh | Good | 13:57 | 15:34 |
| 7 | Rog | Inauspicious | 15:34 | 17:11 |
| 8 | Udveg | Inauspicious | 17:11 | 18:48 |


## 4.6 Hora Table (Planetary Hours)

| Check | Value |
| --- | --- |
| Entries | 24 |
| Expected | 24 (12 day + 12 night) |
| Count OK? | ✅ YES |
| Method | REAL: Day lord from weekday; sequence Sun/Venus/Merc/Moon/Sat/Jup/Mars cycling |

**Sample Hora entries** (first 4):

| Hora # | Lord | Start | End | Type |
| --- | --- | --- | --- | --- |
| 1 | Sun | 05:52 | 06:56 | day |
| 2 | Venus | 06:56 | 08:01 | day |
| 3 | Mercury | 08:01 | 09:06 | day |
| 4 | Moon | 09:06 | 10:10 | day |


## 4.7 Rule Engine — Avoidance Conditions

| Rule | Implemented? | Status Today | Source |
| --- | --- | --- | --- |
| Rahu Kaal exclusion | ✅ YES | — | Slot-based, weekday-specific |
| Dur Muhurtam exclusion | ✅ YES | — | Drik-verified muhurta indices |
| Varjyam exclusion | ✅ YES | — | Tyajya ghati formula |
| Panchaka detection | ✅ YES | — | 5 nakshatra types with severity |
| Ganda Moola nakshatra warning | ✅ YES | — | panchang_yogas module |
| Vishti (Bhadra) Karana warning | ✅ YES | — | is_vishti flag in karana |
| Dagdha Tithi (burnt tithi) | ✅ YES | — | Hindu month × nakshatra cross-check |
| Chandrashtama | ✅ YES | — | Transit moon in 8th from natal moon |
| Guru Asta (Jupiter combust) | ✅ YES | ✅ NOT COMBUST (diff=78.43°, orb=11°) | planetary_positions[Jupiter].combusted |
| Shukra Asta (Venus combust) | ✅ YES | ✅ NOT COMBUST (diff=24.75°, orb=10°) | planetary_positions[Venus].combusted |
| Sankranti | ✅ YES | — | sankranti_engine.py handles |


### 4.7.1 Guru/Shukra Asta Detail

| Guru (Jupiter) | Value |
| --- | --- |
| Longitude | 83.1735 |
| Sun Longitude | 4.7459 |
| Angular Diff (°) | 78.43 |
| Combust Orb (°) | 11.0 |
| Asta Active? | ❌ NO |
| Verdict | ✅ NOT COMBUST |
| Method | REAL: |planet_lon - sun_lon| ≤ 11.0° → asta |

| Shukra (Venus) | Value |
| --- | --- |
| Longitude | 29.4976 |
| Sun Longitude | 4.7459 |
| Angular Diff (°) | 24.75 |
| Combust Orb (°) | 10.0 |
| Asta Active? | ❌ NO |
| Verdict | ✅ NOT COMBUST |
| Method | REAL: |planet_lon - sun_lon| ≤ 10.0° → asta |


---


# 5. Dynamic vs Static Detection

| Output Field | Classification |
| --- | --- |
| sunrise | REAL (ephemeris-computed) |
| sunset | REAL (ephemeris-computed) |
| moonrise | REAL (ephemeris-computed) |
| tithi.name | REAL/RULE-BASED |
| tithi.end_time | REAL (ephemeris-computed) |
| nakshatra.name | REAL/RULE-BASED |
| nakshatra.end_time | REAL (ephemeris-computed) |
| yoga.name | REAL/RULE-BASED |
| yoga.end_time | REAL (ephemeris-computed) |
| karana.name | REAL/RULE-BASED |
| karana.end_time | REAL (ephemeris-computed) |
| rahu_kaal | RULE-BASED (classical tables) |
| gulika_kaal | RULE-BASED (classical tables) |
| yamaganda | RULE-BASED (classical tables) |
| brahma_muhurat | REAL (ephemeris-computed) |
| abhijit_muhurat | REAL (ephemeris-computed) |
| dur_muhurtam | RULE-BASED (classical tables) |
| varjyam | REAL (ephemeris-computed) |
| godhuli_muhurta | RULE-BASED (classical tables) |
| nishita_muhurta | RULE-BASED (classical tables) |
| vijaya_muhurta | RULE-BASED (classical tables) |
| ravi_yoga | REAL/RULE-BASED |
| special_yogas | RULE-BASED (classical tables) |
| panchaka | RULE-BASED (classical tables) |
| lagna_table | REAL (ephemeris-computed) |
| hora_table | REAL (ephemeris-computed) |
| choghadiya | RULE-BASED (classical tables) |
| panchanga_shuddhi | RULE-BASED (classical tables) |
| tarabalam | RULE-BASED (classical tables) |
| chandrabalam | RULE-BASED (classical tables) |
| ayanamsa | REAL (ephemeris-computed) |
| sun_longitude | REAL (ephemeris-computed) |
| moon_longitude | REAL (ephemeris-computed) |
| planetary_positions | REAL (ephemeris-computed) |
| hindu_calendar | REAL/RULE-BASED |

✅ **No static value anomalies detected.**

**Consistency Check**: Same date called twice → tithi/nakshatra consistent: ✅ YES


---


# 6. Engine Health Dashboard

| Module | Status | Real Output? | Issues |
| --- | --- | --- | --- |
| Panchang Engine (calculate_panchang) | ✅ LIVE | ✅ YES — SWE ephemeris | None |
| API Layer (/api/panchang) | ✅ LIVE | ✅ YES | None |
| Tithi Engine | ✅ OK | ✅ REAL (elongation/12) | None |
| Nakshatra Engine | ✅ OK | ✅ REAL (moon_lon/13.33) |  |
| Yoga Engine | ✅ OK | ✅ REAL (sun+moon/13.33) |  |
| Karana Engine | ✅ OK | ✅ REAL (half-tithi) |  |
| Rahu/Gulika/Yamaganda | ✅ OK | ✅ RULE-BASED (day/8 slots) | Max drift: 0.0min |
| Brahma Muhurat | ✅ OK | ✅ RULE-BASED | Drift: 0.5min |
| Abhijit Muhurat | ✅ OK | ✅ RULE-BASED (8th muhurta) | Drift: 0.1min |
| Dur Muhurtam | ✅ OK | ✅ RULE-BASED | Drift: 0.5min |
| Varjyam | ✅ OK | ✅ REAL (tyajya ghati) |  |
| Special Yogas | ✅ OK | ✅ RULE-BASED |  |
| Panchaka Engine | ✅ OK | ✅ RULE-BASED |  |
| Lagna Table | ✅ OK | ✅ REAL (sidereal time calc) | Count: 13 |
| Hora Table | ✅ OK | ✅ REAL (day lord sequence) | Count: 24 |
| Choghadiya | ✅ OK | ✅ RULE-BASED | Count: 8 (need 8) |
| Panchanga Shuddhi | ✅ OK | ✅ RULE-BASED (5 limbs) |  |
| Tarabalam | ✅ OK | ✅ RULE-BASED |  |
| Chandrabalam | ✅ OK | ✅ RULE-BASED |  |
| Muhurat Finder API | ✅ OK | ✅ REAL (month-loop panchang) |  |


---


# 7. Critical Bugs & Gaps

✅ **No critical bugs detected for this date/location.**


---


# 8. Accuracy Verdict

| Metric | Score | Max | Notes |
| --- | --- | --- | --- |
| Astronomical Accuracy | 10 | 10 | SWE-based sunrise/sunset/longitudes |
| Panchang Reliability | 10 | 10 | Tithi/Nak/Yoga/Karana end times + types |
| Muhurat Reliability | 10 | 10 | Kaal periods + auspicious windows |
| **Production Readiness** | **100%** | 100% | Composite score |


---


# 9. Final Verdict

| Question | Answer |
| --- | --- |
| Is Panchang engine real or fake? | ✅ REAL — powered by Swiss Ephemeris (libswe) + Lahiri ayanamsa. Tithi/Nak/Yoga/Karana from actual Sun/Moon sidereal longitudes at JD sunrise. |
| Is Muhurat engine rule-based or static? | ✅ RULE-BASED — Rahu/Gulika/Yamaganda from day-division formula; Brahma/Abhijit/Vijaya from muhurta-count; Varjyam from tyajya ghati. NOT hardcoded static values. |
| Can it be trusted for real-world usage? | ✅ YES — Production readiness: 100%. Core panchang (tithi/nak/yoga/karana/sunrise/muhurat timings) is production-grade. Engine meets production threshold. |
| What must be fixed before production-grade trust? | No critical issues — engine is production-ready. |


## Summary

- **Panchang Engine**: REAL + EPHEMERIS-BACKED

- **Muhurat Engine**: RULE-BASED + DYNAMIC

- **Total Bugs Found**: 0

- **Production Readiness**: 100%

- **Astronomical Score**: 10/10

- **Panchang Reliability**: 10/10

- **Muhurat Reliability**: 10/10


---

*Report generated by scripts/panchang_muhurat_report.py — 2026-04-19T13:55:21.542563*
