# Panchang & Muhurat — Enhancement Plan
**Source:** Muhurt Chintamani (Shriram Daivagya) — Classical Sanskrit muhurta treatise  
**Date:** 18 April 2026  
**Status Codes:** ✅ Complete (BE + API + FE wired) · ⚠️ Partial (simplified/stub) · 🔌 BE Ready / FE Missing · ❌ Not Built

**Update (18 April 2026):** WS-F/WS-G/WS-H/WS-I shipped in backend + API (Vivaha deep rules, Vastu muhurtas, Travel muhurta, Shop opening + business hora guidance) + added P1 activities (Vidyarambha/Shraddha/Antyeshti) + exposed Yoga interpretation fields + added Chandra/Tara Balam per-position interpretation in finder. Added `GET /api/panchang/sankranti` (12 Sankranti ingress times + ±16h restriction window + explicitly-marked heuristic punyakaal; classical prahar-based rules + Amritkaal still pending) + added a Panchang UI tab to view the yearly Sankranti table. Full test suite green (`1825 passed, 1 skipped`) and `frontend npm run build` passes.  

---

## 1. Architecture Summary

| Layer | Files | Status |
|-------|-------|--------|
| Core Engine | `panchang_engine.py` (1,895 lines) | ✅ |
| Muhurat Finder | `muhurat_finder.py` (698 lines) | ✅ |
| Activity Rules DB | `muhurat_rules.py` (543 lines) | ✅ |
| Special Yogas | `panchang_yogas.py` (508 lines) | ✅ |
| Directions | `panchang_directions.py` (252 lines) | ✅ |
| Miscellaneous | `panchang_misc.py` | ✅ |
| Ekadashi | `panchang_ekadashi.py` | ✅ |
| Sankranti Engine | `sankranti_engine.py` | ✅ |
| Panchang API | `routes/panchang.py` (~1,400 lines, 9 endpoints) | ✅ |
| Muhurat API | `routes/muhurat.py` (5 endpoints) | ⚠️ 2 of 5 simplified |
| Frontend Section | `sections/Panchang.tsx` + 14 tab components | ✅ |

---

## 2. Muhurt Chintamani — Chapter Structure

The book has 11 main Prakaranas (chapters):

| # | Prakarana | Topic | Our Status |
|---|-----------|-------|-----------|
| 1 | Shubhashubha | Auspicious/Inauspicious — Tithis, Yogas, Doshas, Hora, Muhurta | ⚠️ Partial |
| 2 | Sankranti | Sun's ingress into 12 signs — timing, restrictions, Amritkaal | ⚠️ Partial (P1 timings + restriction exposed; P2 Amritkaal/type rules pending) |
| 3 | Gochara | Planet transits and their muhurta effects | ⚠️ Partial (Balam scoring + position fruits done) |
| 4 | Samskara | 16 life-cycle ceremonies (Shodasha Samskaras) | ⚠️ 7 of 16 |
| 5 | Vivaha | Marriage muhurta — detailed multi-factor rules | ⚠️ Deep layer partial |
| 6 | Saptamukhya Samskara | 7 main sacrament rules | ❌ Not built |
| 7 | Dwiragamana | Bride's second journey muhurta | ❌ Not built |
| 8 | Vastu | Construction, Griha Pravesh, Bhoomi Puja | ⚠️ Extended P1 layer |
| 9 | Raja Abhisheka | Coronation muhurta | ❌ Skip (N/A) |
| 10 | Yatra | Travel muhurta by direction + nakshatra | ⚠️ Built (P1 core) |
| 11 | Bramhavivaha | Remarriage rules | ❌ Not built |

---

## 3. Fully Implemented ✅ (Backend + API + Frontend all wired)

### 3.1 Core Panchang Elements
| Feature | Backend Function | API Endpoint | Frontend Tab |
|---------|-----------------|-------------|-------------|
| Tithi (30) with end times | `calculate_panchang()` | `GET /api/panchang` | PanchangCoreTab |
| Nakshatra (27) + pada + category | `calculate_panchang()` | `GET /api/panchang` | PanchangCoreTab |
| Yoga (27) + quality | `calculate_panchang()` | `GET /api/panchang` | PanchangCoreTab |
| Karana (11 types) + Vishti flag | `calculate_panchang()` | `GET /api/panchang` | PanchangCoreTab |
| Vara (weekday) + lord | `calculate_panchang()` | `GET /api/panchang` | PanchangCoreTab |
| Sunrise / Sunset | `calculate_panchang()` | `GET /api/panchang` | PanchangCoreTab |
| Moonrise / Moonset | `calculate_panchang()` | `GET /api/panchang` | PanchangCoreTab |
| Hindu Calendar (Samvat, Maas, Paksha, Ritu, Ayana) | `_compute_hindu_calendar()` | `GET /api/panchang` | HinduCalendarTab |
| Planetary Positions (Navgraha) | `calculate_planetary_positions()` | `GET /api/panchang` | PlanetaryPositionsTab |
| Monthly panchang grid | bulk loop | `GET /api/panchang/month` | MonthlyCalendarTab |

### 3.2 Auspicious / Inauspicious Timings
| Feature | Status |
|---------|--------|
| Rahu Kaal, Gulika Kaal, Yamaganda | ✅ |
| Brahma Muhurat | ✅ |
| Abhijit Muhurat | ✅ |
| Pratah Sandhya, Sayahna Sandhya, Nishita Muhurta | ✅ |
| Godhuli Muhurta, Vijaya Muhurta | ✅ |
| Dur Muhurtam, Varjyam | ✅ |

### 3.3 Hora, Choghadiya, Lagna
| Feature | Status |
|---------|--------|
| Hora table (24 planetary hours) | ✅ |
| Choghadiya day + night (48 periods) | ✅ |
| Lagna table (12 ascendant periods) | ✅ |
| Current active period highlighting | ✅ |

### 3.4 Special Yogas
| Yoga | Rule | Status |
|------|------|--------|
| Sarvartha Siddhi Yoga | Tithi+Vara OR Nakshatra+Vara | ✅ |
| Amrit Siddhi Yoga | Nakshatra+Vara | ✅ |
| Dwipushkar Yoga | Dwitiya/Saptami/Dwadashi + Sun/Tue/Sat + Nakshatra | ✅ |
| Tripushkar Yoga | Tritiya/Ashtami/Trayodashi + Sun/Tue/Sat + Nakshatra | ✅ |
| Ganda Moola | Moon in junction nakshatras (6 specific) | ✅ |

### 3.5 Directions & Indicators
| Feature | Status |
|---------|--------|
| Disha Shool (inauspicious direction by weekday) | ✅ |
| Baana (elemental direction by tithi) | ✅ |
| Anandadi Yoga (28 yogas, weekday × nakshatra) | ✅ |
| Lucky color, number, direction per weekday | ✅ |

### 3.6 Panchaka & Ekadashi
| Feature | Status |
|---------|--------|
| Panchaka detection (active/inactive flag) | ✅ |
| Panchaka type (Mrityu/Agni/Raja/Chora/Roga) | ✅ |
| Panchaka Rahita Muhurta window | ✅ |
| Ekadashi Parana timing | ✅ |

### 3.7 Muhurat Finder (Rules-Based)
**Endpoint:** `GET /api/muhurat/finder`  
**13 Activities with full classical rules:**

| Activity | Tithis | Nakshatras | Weekdays | Lagnas | Avoid Conditions |
|----------|--------|-----------|---------|--------|-----------------|
| Marriage | 9 specific | 14 specific | 5 days | 7 lagnas | 11 avoid rules |
| Griha Pravesh | 8 specific | 11 specific | 5 days | 6 lagnas | 9 avoid rules |
| Vehicle Purchase | 7 specific | 12 specific | 4 days | 5 lagnas | 7 avoid rules |
| Property Purchase | 8 specific | 11 specific | 4 days | 5 lagnas | 7 avoid rules |
| Mundan (Haircut) | 7 specific | 12 specific | 5 days | 5 lagnas | 8 avoid rules |
| Annaprashana | 8 specific | 11 specific | 5 days | 5 lagnas | 7 avoid rules |
| Upanayana | 9 specific | 12 specific | 5 days | 6 lagnas | 8 avoid rules |
| Namakarana | 8 specific | 13 specific | 5 days | 5 lagnas | 7 avoid rules |
| Business Start | 7 specific | 11 specific | 4 days | 4 lagnas | 8 avoid rules |
| Shop Opening | 8 specific | 12 specific | 4 days | 6 lagnas | 6 avoid rules |
| Bhoomi Puja | 8 specific | 11 specific | 4 days | 6 lagnas | 8 avoid rules |
| Shilanyas | 8 specific | 9 specific | 3 days | 5 lagnas | 8 avoid rules |
| Vastu Shanti | 8 specific | 8 specific | 4 days | 6 lagnas | 7 avoid rules |

**Hard-block checks in finder (all 15 implemented):**
- Bhadra / Vishti Karana realm check (Earth / Swarga / Patala)
- Dagdha Tithi (burned day per weekday)
- Sankranti (Sun ingress day)
- Guru Asta (Jupiter combustion)
- Shukra Asta (Venus combustion)
- Retrograde Jupiter
- Retrograde Saturn
- Kula Kanthaka Dosha (for marriage)
- Simha Surya (Sun in Leo)
- Panchaka detection
- Ganda Moola
- Krishna Paksha avoidance (per activity)
- Amavasya block
- Chandra Balam scoring (optional, birth Moon rashi)
- Tara Balam scoring (optional, birth nakshatra)

### 3.8 Other Complete Features
| Feature | Status |
|---------|--------|
| Festivals list (year-based) | ✅ |
| PDF generation (bilingual WhatsApp-style) | ✅ |
| Mantri Mandala (10-role planetary cabinet) | ✅ |
| Astronomical data (Kaliyuga, Julian Day, Ayanamsha) | ✅ |
| Gowri Panchangam (8 periods) | ✅ |
| Tara Balam tab (birth nakshatra vs transit nakshatra) | ✅ |
| Do Ghati Muhurta (30 muhurtas in day) | ✅ |
| Panchang PDF download | ✅ |
| Cache management | ✅ |
| Bilingual (Hindi + English) throughout | ✅ |

---

## 4. Partial / Simplified ⚠️ (Exists but not fully classical)

### 4.1 Monthly Muhurat Endpoints — Simplified Logic
**Issue:** `GET /api/muhurat/monthly` and `GET /api/muhurat/find` use simplified logic only:
- Checks: Shukla Paksha + not (Ashtami / Navami / Chaturdashi)
- Does NOT apply the 9-activity classical rule base
- The rules-based finder is at `GET /api/muhurat/finder` (separate endpoint)

**Fix needed:** Replace simplified endpoints with calls to `find_muhurat_dates()` OR deprecate them.  
**FE Impact:** `MuhuratTab.tsx` in the Panchang section may be hitting the simplified endpoint; `MuhuratFinderTab.tsx` correctly uses `/finder`.

### 4.2 Chandrabalam (Moon Strength)
- **Implemented:** Score per rashi (1-12 positions from birth Moon)
- **Missing:** Classical fruit interpretation per position (text for each of 12 positions: "Moon in 1st = indifferent, 2nd = wealth loss, 3rd = gain..." etc.)
- **Book reference:** Prakarana 3 (Gochara) — detailed position-by-position fruit

### 4.3 Sankranti (Solar Ingress)
- **Implemented:** Basic Sankranti avoidance flag in muhurat finder
- **Missing:** Full Sankranti Prakarana (see Section 5.2 below)

### 4.4 Tara Balam
- **Implemented:** Scoring + tab display
- **Missing:** Per-position interpretation (Janma, Sampat, Vipat, Kshema, Pratyari, Sadhaka, Naidhana, Mitra, Parama Mitra) with activity guidance per position

### 4.5 Yoga Quality Explanation
- **Implemented:** "good" / "bad" quality label for 27 yogas
- **Missing:** Individual yoga name + interpretation text (e.g., "Vishkambha — obstacle-causing, avoid new starts")

---

## 5. Missing — Not Built ❌

### 5.1 Prakarana 1: Additional Yogas and Doshas

| Feature | Description | Priority |
|---------|-------------|----------|
| Ravi Yoga | Specific nakshatra + weekday combos | ✅ |
| Siddhi Yoga | Tithi + weekday combination | ✅ |
| Mrityu Yoga | Death yoga — tithi + weekday dosha | ✅ |
| Visha Yoga | Poison yoga — tithi + weekday combo | ✅ |
| Vyatipata Yoga | One of 27 yogas — EXTREMELY inauspicious | ✅ |
| Vaidhriti Yoga | 27th of 27 yogas — EXTREMELY inauspicious | ✅ |
| Marana Yoga | Death association yoga — tithi + weekday | ✅ |
| Dagdha Nakshatra | Per-month "burned nakshatra" | ✅ |
| Kula Yoga | Lineage/family yoga from weekday + nakshatra | ❌ Not built |
| Tithi-Vara Dosha table | Full matrix of bad tithi+weekday combinations | ✅ |
| Ganda Lagna | First 3°20' of any sign = inauspicious | ✅ |
| Sandhi Lagna | Last 3°20' of any sign = avoid | ✅ |
| Chaturmasa period | 4-month period (Ashadh Shukla 11 → Kartik Shukla 11) | ✅ |
| Tithi lord display | Show planet ruling each tithi | P2 |
| Tithi fruit text | Interpretive text per tithi | P2 |
| Panchanga Shuddhi score | Composite day-quality score based on all 5 elements | P1 |

### 5.2 Prakarana 2: Sankranti Chapter

| Feature | Description | Priority |
|---------|-------------|----------|
| 12 Sankranti dates | Compute exact Sun ingress times for all 12 signs for any year | P1 |
| Sankranti Punyakaal | Auspicious window around Sankranti (specific prahars) | P1 |
| Sankranti restriction window | 16 hours before + 16 hours after Sankranti = no ceremonies | P1 |
| Sankranti Amritkaal | Small auspicious window within the restriction (exception) | P2 |
| Sankranti type (8 types) | Day/night × arrival direction × day of week → 8 type names | P2 |
| Uttarayan / Dakshinayana | Summer/Winter solstice Sankranti (Makar and Karka) with significance | P2 |
| Makar Sankranti special rules | Bathing, charity, specific timing rules | P2 |
| Sankranti effects on signs | Which zodiac signs are affected how per Sankranti | P3 |

### 5.3 Prakarana 3: Gochara — Transit Muhurta

| Feature | Description | Priority |
|---------|-------------|----------|
| Jupiter transit muhurta | When Guru changes sign — auspicious for Upanayana, thread ceremony | P2 |
| Chandrabalam per position (text) | Detailed fruit text for each of 12 Moon positions from birth Moon | P1 |
| Tara Balam per position (text) | Interpretation for each of 9 Tara positions (Janma → Parama Mitra) | P1 |
| Saturn transit alert | Saturn entering specific signs creates period restrictions | P3 |

### 5.4 Prakarana 4: Shodasha Samskaras (16 Life Ceremonies) — MAJOR GAP

**Currently implemented:** 7 of 16 Samskaras (mundan, annaprashana, upanayana, namakarana, vidyarambha, shraddha, antyeshti)  
**Missing 9:**

| Samskara # | Name | Description | Priority |
|-----------|------|-------------|----------|
| 1 | Garbha Dhana | Conception ceremony muhurta | P2 |
| 2 | Pumsavana | 3rd lunar month ceremony (son-seeking) | P3 |
| 3 | Simantonnayana | Hair-parting ceremony (4th or 7th month) | P3 |
| 4 | Jatakarma | Birth ceremony (same day as birth) | P2 |
| 5 | Nishkramana | First outdoor outing (4th month) | P2 |
| 9 | Karnavedha | Ear piercing muhurta | P2 |
| 12 | Samavartana | Graduation / study completion | P3 |
| 15 | Chudakarma (extended) | More specific nakshatra rules beyond current basic check | P1 |
| 16 | Shodashopachara Puja | 16-service worship muhurta | P3 |

**Additional Samskara rules missing:**
- Age at which each Samskara should be performed (month-year mapping)
- Which months are forbidden for each Samskara
- Nakshatra + tithi + weekday triple combination per ceremony

### 5.5 Prakarana 5: Vivaha (Marriage) — Deep Rule Layer Missing

Our marriage muhurta has the basic framework but Muhurt Chintamani Vivaha chapter adds 50+ additional rules:

| Feature | Description | Priority | Status |
|---------|-------------|----------|--------|
| Vivaha Panchami rules | 5th day after marriage — ceremony timing | P3 | ❌ |
| Lagnasuddhi score | Lagna purity index (lagna lord, aspect, strength) for marriage | P1 | ✅ |
| Marriage season calendar | Which Hindu months are allowed/forbidden for marriage | P1 | ✅ |
| Guru rashi allowed list | Jupiter in Taurus, Cancer, Virgo, Sagittarius, Pisces = auspicious for marriage | P1 | ✅ |
| Shukra rashi allowed list | Venus not in Aries, Cancer, Virgo, Scorpio for marriage | P1 | ✅ |
| Dwiragamana muhurta | Bride's second journey to in-laws — separate muhurta rules | P2 | ❌ |
| Marriage lagna quality text | Per-lagna interpretation for marriage (Aries = hasty, Taurus = stable, etc.) | P2 | ❌ |
| Muhurta conflict resolution | When nakshatra is good but tithi is bad — precedence rules | P1 | ⚠️ |
| Minimum muhurta quality gate | "Vivaha Paryapta" — minimum acceptable quality, warn user if below | P1 | ✅ |
| Dosha exception rules | Certain doshas cancelled by specific stronger yogas (e.g., Amrit Siddhi cancels Rahu Kaal) | P1 | ❌ |
| Kundali matching integration | Connect muhurta finder to birth chart Ashtakoot (currently separate) | P2 | ❌ |
| Marriage muhurta summary card | One-line reason card with risks | P1 | ✅ |

### 5.6 Prakarana 8: Vastu Muhurtas (beyond basic Griha Pravesh)

| Feature | Description | Priority | Status |
|---------|-------------|----------|--------|
| Bhoomi Puja muhurta | Land worship before construction — specific nakshatra + tithi | P1 | ✅ |
| Shilanyas muhurta | Foundation stone laying — Uttarayan preferred, specific lagnas | P1 | ✅ |
| Kupa / Baoli (Well) muhurta | Water source installation timing | P2 | ❌ |
| Door / Gate installation | Timing and direction for main door installation | P2 | ❌ |
| Vastu Shanti ritual | Peace ceremony after construction — nakshatra + tithi | P1 | ✅ |
| Construction direction rule | Which direction to start construction (East/North preferred) | P2 | ❌ |
| Griha Pravesh extended rules | Uttarayan preference + Pushya/Rohini/Hasta preference | P1 | ⚠️ |
| Month-based construction rules | Which months avoid construction (Ashadh, Bhadrapad, etc.) | P1 | ❌ |

### 5.7 Prakarana 10: Yatra (Travel) Muhurta

| Feature | Description | Priority | Status |
|---------|-------------|----------|--------|
| Travel muhurta finder | Direction → best nakshatra + safety blocks | P1 | ✅ |
| Direction × Nakshatra matrix | Each direction (N/S/E/W/NE etc.) has preferred nakshatras | P1 | ✅ |
| Pushya Nakshatra for travel | Traditional "best nakshatra for travel" with explanation | P1 | ✅ |
| Hora for travel timing | Which planetary hora is best to start journey | P2 | ❌ |
| Journey start lagna | Specific lagna recommendations for departure | P2 | ❌ |
| Return journey muhurta | Timing for return (avoid same dushta yogas) | P3 | ❌ |
| Vehicle purchase extended | Beyond current basic — which nakshatra, Shukra position | P2 | ❌ |

### 5.8 Additional Features from Book

| Feature | Description | Priority | Status |
|---------|-------------|----------|--------|
| Medical treatment muhurta | Which nakshatra/tithi to start treatment, hospital admission | P2 |
| Sowing / harvest muhurta | Agricultural ceremony timing | P3 |
| Shop / business opening | Separate activity + recommended hora windows | P1 | ✅ |
| Loan / debt repayment muhurta | When to repay debts (specific tithi + weekday) | P2 |
| Court case / legal muhurta | Filing case, court hearing timing | P2 |
| Military / confrontation timing | Yudh muhurta (historical — can be reframed as competition) | P3 |
| Puja/Havan muhurta | Specific yajna and puja timing rules | P2 |
| Hora activity guide (detailed) | Hora table includes recommended activities per hora | P1 | ✅ |
| 27 Yoga interpretation text | Individual text for all 27 yogas beyond just "good/bad" | P1 | ✅ |
| 11 Karana interpretation text | Text for all 11 Karanas' significance and use cases | P2 |
| Nakshatra deity + quality text | Each nakshatra's deity, symbol, human quality, best for activity | P2 |

---

## 6. Backend Ready — Frontend Not Connected 🔌

| Feature | Backend Location | Missing Frontend |
|---------|-----------------|-----------------|
| Rules-based `/api/muhurat/finder` fully implemented | `routes/muhurat.py` | MuhuratTab (Panchang) still uses simplified endpoint — should call `/finder` |
| Lagna windows in muhurat response | `find_muhurat_dates()` returns `lagna_windows` | ✅ Displayed in MuhuratFinderTab (safe window + warnings) |
| Score + reasons_good + reasons_bad per muhurat date | `find_muhurat_dates()` | ✅ Expanded in MuhuratFinderTab |
| Panchang data has `panchaka_rahita` | `panchang_misc.py` | Displayed in AdvancedTab but not highlighted when active |
| `do_ghati_muhurta` (30 muhurtas) | `panchang_engine.py` | Not shown in any tab |
| `gowri_panchangam` | `panchang_engine.py` | GowriTab exists but needs validation |
| Anandadi Yoga is calculated | `panchang_directions.py` | Shown in AdvancedTab but no auspicious/inauspicious visual badge |
| Mantri Mandala full 10 roles | `panchang_misc.py` | Shown but no planetary interpretation |

---

## 7. Priority Matrix

### P0 — Safety / Must Fix Before Public Use
| # | Feature | Risk if Missing |
|---|---------|----------------|
| 1 | Vyatipata Yoga block | ✅ |
| 2 | Vaidhriti Yoga block | ✅ |
| 3 | Mrityu Yoga warning | ✅ |
| 4 | Visha Yoga block | ✅ |
| 5 | Sankranti 16-hour restriction | ✅ |
| 6 | Ganda Lagna / Sandhi Lagna warning | ✅ |

### P1 — Core Classical Accuracy (High Business Value)
| # | Feature |
|---|---------|
| 7 | Sankranti Punyakaal + restriction window calculation ⚠️ (restriction + yearly table done; punyakaal heuristic until P2 prahar rules) |
| 8 | Chaturmasa period detection (4 months block) | ✅ |
| 9 | Tithi-Vara dosha full matrix | ✅ |
| 10 | Ravi Yoga + Siddhi Yoga calculation | ✅ |
| 11 | Panchanga Shuddhi composite score | P1 |
| 12 | Chandrabalam per-position interpretation text | ✅ |
| 13 | Tara Balam per-position text (9 positions) | ✅ |
| 14 | Marriage season calendar (allowed/forbidden months) | ✅ |
| 15 | Guru rashi + Shukra rashi filter for marriage | ✅ |
| 16 | Lagnasuddhi score for marriage | ✅ |
| 17 | Muhurta conflict resolution rules (precedence system) | P1 |
| 18 | Vivaha Paryapta minimum quality gate | ✅ |
| 19 | Marriage muhurta summary card | ✅ |
| 20 | Dosha cancellation / exception rules | P1 |
| 21 | Vidyarambha muhurta (school start — high search volume) | ✅ |
| 22 | Shraddha timing (Pitru Paksha — high demand) | ✅ |
| 23 | Antyeshti timing guidance | ✅ |
| 24 | Bhoomi Puja muhurta | ✅ |
| 25 | Shilanyas muhurta | ✅ |
| 26 | Vastu Shanti muhurta | ✅ |
| 27 | Griha Pravesh extended rules (Uttarayan, Pushya/Rohini) | ✅ |
| 28 | Travel muhurta finder (direction × nakshatra matrix) | ✅ |
| 29 | Pushya Nakshatra travel guide | ✅ |
| 30 | Business/shop opening extended rules | ✅ |
| 31 | Hora activity guide (best activity per planetary hora) | ✅ |
| 32 | 27 Yoga interpretation text | ✅ |
| 33 | Dagdha Nakshatra per month | ✅ |
| 34 | Wire MuhuratTab to use `/finder` endpoint (not simplified) | ✅ |
| 35 | Lagna windows display in MuhuratFinderTab | ✅ |

### P2 — Depth Features (Differentiation)
- Dwiragamana muhurta
- Garbha Dhana / Jatakarma / Nishkramana / Karnavedha muhurta
- Sankranti 8-type classification
- Kupa / Door installation muhurta
- Medical treatment muhurta
- Loan/debt repayment muhurta
- Kundali matching ↔ muhurta integration
- Nakshatra deity + quality interpretation
- 11 Karana interpretation text

### P3 — Advanced / Future
- Pumsavana, Simantonnayana, Samavartana muhurta
- Raja Yoga in muhurta context
- Agricultural muhurtas
- Bramhavivaha (remarriage) rules
- Military/competition timing

---

## 8. Implementation Effort Estimates

| Feature Group | Backend Effort | Frontend Effort | Total |
|--------------|---------------|----------------|-------|
| P0 Yoga blocks (Vyatipata, Vaidhriti, Mrityu, Visha) | 1 day | 0.5 day | 1.5 days |
| Sankranti chapter (full) | 2 days | 1 day | 3 days |
| Ganda/Sandhi Lagna warning | 0.5 day | 0.5 day | 1 day |
| Chaturmasa period | 0.5 day | 0.5 day | 1 day |
| Panchanga Shuddhi score | 1 day | 1 day | 2 days |
| Marriage deep rules (P1 batch) | 2 days | 1.5 days | 3.5 days |
| Missing Samskaras P1 (Vidyarambha, Shraddha) | 1 day | 1 day | 2 days |
| Vastu muhurtas P1 | 1 day | 1 day | 2 days |
| Travel muhurta finder | 1.5 days | 1.5 days | 3 days |
| Hora activity guide | 0.5 day | 1 day | 1.5 days |
| Wire MuhuratTab to /finder | 0 days | 0.5 day | 0.5 day |
| Yoga interpretation texts (27) | 1 day | 0.5 day | 1.5 days |
| **P0+P1 Total** | **~12 days BE** | **~10 days FE** | **~22 days** |

---

## 9. Quick Wins (< 1 day each, high impact)

1. **Wire `MuhuratTab` → `/api/muhurat/finder`** — ✅ Done.
2. **Add Vyatipata + Vaidhriti hard blocks to finder** — ✅ Done.
3. **Show Lagna windows in MuhuratFinderTab** — ✅ Done.
4. **Chaturmasa dates** — ✅ Done.
5. **Dagdha Nakshatra** — ✅ Done.
6. **27 Yoga texts** — ✅ Done (exposed in response).

---

## 10. API Endpoint Reference

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/api/panchang` | GET | ✅ Full classical | Main daily panchang |
| `/api/panchang/month` | GET | ✅ | Monthly grid |
| `/api/panchang/choghadiya` | GET | ✅ | 48 periods |
| `/api/panchang/muhurat` | GET | ⚠️ Simplified | Non-rules-based, legacy |
| `/api/panchang/sunrise` | GET | ✅ | Sunrise/sunset only |
| `/api/panchang/sankranti` | GET | ✅ | Year's 12 Sankranti dates + ±16h restriction windows (+ heuristic punyakaal) |
| `/api/festivals` | GET | ✅ | Year-based festivals |
| `/api/panchang/pdf` | GET | ✅ | Bilingual PDF |
| `/api/muhurat/finder` | GET | ✅ | Extended activities (incl. Bhoomi Puja, Shilanyas, Vastu Shanti, Shop Opening) |
| `/api/muhurat/travel` | GET | ✅ | Travel by direction (matrix + Pushya guide) |
| `/api/muhurat/monthly` | GET | ⚠️ Simplified | Replace with finder logic |
| `/api/muhurat/find` | GET | ⚠️ Simplified | Replace with finder logic |
| `/api/muhurat/activities` | GET | ✅ | Activity list |
| `/api/muhurat/vastu` | GET | ❌ | Optional: dedicated Vastu-only endpoint (already covered via `/api/muhurat/finder`) |

---

*Source: Muhurt Chintamani by Shriram Daivagya (Banaras edition) — 11 Prakaranas, ~216 topics*  
*Cross-referenced with: panchang_engine.py, muhurat_finder.py, muhurat_rules.py, panchang_yogas.py, routes/panchang.py, routes/muhurat.py*
