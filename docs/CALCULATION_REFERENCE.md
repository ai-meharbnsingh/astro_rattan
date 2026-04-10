# Calculation Reference -- AstroRattan Vedic Astrology Engine

**Purpose:** Comprehensive reference for astrologers to verify that every calculation in AstroRattan matches classical texts.

**Engine:** Swiss Ephemeris (swisseph) primary; pure-math fallback when swisseph is unavailable.

---

## Table of Contents

1. [Planetary Positions (astro_engine)](#1-planetary-positions)
2. [KP System (kp_engine)](#2-kp-system)
3. [Vimshottari Dasha (dasha_engine)](#3-vimshottari-dasha)
4. [Ashtakvarga (ashtakvarga_engine)](#4-ashtakvarga)
5. [Shadbala (shadbala_engine)](#5-shadbala)
6. [Panchang (panchang_engine)](#6-panchang)
7. [Divisional Charts (divisional_charts)](#7-divisional-charts)
8. [Doshas and Yogas (dosha_engine)](#8-doshas-and-yogas)
9. [Kundli Matching (matching_engine)](#9-kundli-matching)
10. [Numerology (numerology_engine)](#10-numerology)
11. [Lal Kitab (lalkitab_engine)](#11-lal-kitab)
12. [Transits (transit_engine)](#12-transits)
13. [Varshphal (varshphal_engine)](#13-varshphal)

---

## 1. Planetary Positions

**Source:** `app/astro_engine.py`
**Classical References:** Surya Siddhanta, Lahiri Ayanamsa tables, BPHS (Brihat Parashara Hora Shastra)
**Tab:** Birth Chart, all tabs relying on planet positions

### 1.1 Julian Day Number

| Item | Detail |
|------|--------|
| **Method** | `_datetime_to_jd(dt_utc)` |
| **Formula** | Meeus algorithm: `JD = int(365.25 * (Y + 4716)) + int(30.6001 * (M + 1)) + D + B - 1524.5` where B = `2 - int(Y/100) + int(int(Y/100)/4)`, and if M <= 2 then Y -= 1, M += 12 |
| **Input** | UTC datetime |
| **Output** | Julian Day Number (float) |
| **Reference** | Jean Meeus, "Astronomical Algorithms" |

### 1.2 Ayanamsa

| Item | Detail |
|------|--------|
| **Method** | `swe.get_ayanamsa(jd)` or `_approx_ayanamsa(jd)` |
| **Primary (swisseph)** | Lahiri: `swe.SIDM_LAHIRI`; KP: `swe.SIDM_KRISHNAMURTI` |
| **Fallback formula** | `Ayanamsa = 23.856 + (50.2788 / 3600) * years_from_J2000` where `years_from_J2000 = (JD - 2451545.0) / 365.25` |
| **Input** | Julian Day |
| **Output** | Ayanamsa in degrees |
| **Reference** | Lahiri Ayanamsa: Indian Astronomical Ephemeris. KP Ayanamsa: Krishnamurti Paddhati. Precession rate: IAU standard (~50.2788 arcsec/year) |

### 1.3 Sidereal Longitude

| Item | Detail |
|------|--------|
| **Formula** | `sidereal_longitude = (tropical_longitude - ayanamsa) mod 360` |
| **Input** | Tropical longitude from Swiss Ephemeris, Ayanamsa |
| **Output** | Sidereal longitude (0-360 degrees) |
| **Reference** | Standard Vedic conversion (Nirayana system) |

### 1.4 Ascendant (Lagna)

| Item | Detail |
|------|--------|
| **Method (swisseph)** | `swe.houses(jd, lat, lon, b"P")` returns Placidus cusps; ascendant = `ascmc[0]`, then converted to sidereal |
| **Fallback formula** | GMST = `(280.46061837 + 360.98564736629 * d) mod 360`; LST = `(GMST + lon) mod 360`; Ascendant = `atan2(-cos(LST), sin(eps)*tan(lat) + cos(eps)*sin(LST))` where eps = obliquity of ecliptic |
| **Input** | JD, latitude, longitude |
| **Output** | Sidereal ascendant longitude |
| **Reference** | Surya Siddhanta (concept), Meeus (modern formula) |

### 1.5 House System

| Item | Detail |
|------|--------|
| **Primary** | Whole Sign Houses (Vedic standard) |
| **Formula** | House 1 = sign of Ascendant. Houses 2-12 follow in sequential signs. `house_number = ((planet_sign_index - asc_sign_index) mod 12) + 1` |
| **Secondary** | Placidus cusps stored separately for KP system |
| **Reference** | BPHS, standard Vedic practice |

### 1.6 Zodiac Sign

| Item | Detail |
|------|--------|
| **Formula** | `sign_index = int(longitude / 30)` |
| **Output** | Sign name (Aries through Pisces, each 30 degrees) |

### 1.7 Nakshatra

| Item | Detail |
|------|--------|
| **Formula** | `nakshatra_index = int(longitude / 13.3333)` |
| **Span** | 360 / 27 = 13 deg 20 min per nakshatra |
| **Pada** | `pada = int(offset_in_nakshatra / 3.3333) + 1` (4 padas per nakshatra, each 3 deg 20 min) |
| **Lords** | Ashwini=Ketu, Bharani=Venus, Krittika=Sun, Rohini=Moon, Mrigashira=Mars, Ardra=Rahu, Punarvasu=Jupiter, Pushya=Saturn, Ashlesha=Mercury (repeats 3x for 27 nakshatras) |
| **Reference** | BPHS, Surya Siddhanta |

### 1.8 Planetary Dignity

| Planet | Exaltation | Debilitation | Own Signs | Moolatrikona |
|--------|-----------|-------------|-----------|-------------|
| Sun | Aries | Libra | Leo | Leo |
| Moon | Taurus | Scorpio | Cancer | Taurus |
| Mars | Capricorn | Cancer | Aries, Scorpio | Aries |
| Mercury | Virgo | Pisces | Gemini, Virgo | Virgo |
| Jupiter | Cancer | Capricorn | Sagittarius, Pisces | Sagittarius |
| Venus | Pisces | Virgo | Taurus, Libra | Libra |
| Saturn | Libra | Aries | Capricorn, Aquarius | Aquarius |
| Rahu | Gemini | Sagittarius | -- | -- |
| Ketu | Sagittarius | Gemini | -- | -- |

**Reference:** BPHS Chapter 3

### 1.9 Combustion (Asta)

| Planet | Direct Orb | Retrograde Orb |
|--------|-----------|---------------|
| Moon | 12 deg | 12 deg |
| Mars | 17 deg | 17 deg |
| Mercury | 14 deg | 12 deg |
| Jupiter | 11 deg | 11 deg |
| Venus | 10 deg | 8 deg |
| Saturn | 15 deg | 15 deg |

| Item | Detail |
|------|--------|
| **Formula** | `angular_distance = min(abs(planet - sun), 360 - abs(planet - sun))`; combust if `distance <= orb` |
| **Reference** | BPHS Chapter 6, Surya Siddhanta |
| **Tab** | Birth Chart (status column) |

### 1.10 Vargottama

| Item | Detail |
|------|--------|
| **Formula** | Planet is Vargottama when its D1 sign index equals its D9 (Navamsa) sign index: `int(lon/30) == d9_sign_index` |
| **Reference** | BPHS -- a planet in the same sign in Rasi and Navamsa gains special strength |
| **Tab** | Birth Chart (status column) |

### 1.11 Sandhi

| Item | Detail |
|------|--------|
| **Formula** | `sandhi = (degree_in_sign < 1.0) or (degree_in_sign > 29.0)` |
| **Meaning** | Planet at the junction of two signs; considered weak |
| **Reference** | Classical Jyotish texts |

### 1.12 Retrograde

| Item | Detail |
|------|--------|
| **Formula** | `retrograde = (daily_speed < 0)` or planet is Rahu/Ketu (always retrograde) |
| **Source** | Swiss Ephemeris speed data (pos[3]) |

### 1.13 Fallback Planetary Approximations

Used only when swisseph is not installed:

| Planet | Method | Accuracy |
|--------|--------|----------|
| Sun | Mean longitude + single-harmonic equation of center: `L = 280.46646 + 0.9856474*d`, center = `1.9146*sin(M) + 0.02*sin(2M)` | ~0.5 deg |
| Moon | Mean longitude + 5-term correction (principal evection, variation, annual equation, parallactic inequality, reduction) | ~2-5 deg |
| Mercury-Saturn | Mean orbital elements at J2000 + single-harmonic equation of center + heliocentric-to-geocentric conversion | ~2-5 deg |
| Rahu | Mean ascending node: `125.044 - 0.0529539 * d` | ~1 deg |
| Ketu | `Rahu + 180` | Same as Rahu |

**Reference:** Meeus "Astronomical Algorithms", simplified

---

## 2. KP System

**Source:** `app/kp_engine.py`
**Classical Reference:** Krishnamurti Paddhati (KP Reader volumes by Prof. K.S. Krishnamurti)
**Tab:** KP tab

### 2.1 Star Lord (Nakshatra Lord)

| Item | Detail |
|------|--------|
| **Formula** | Standard nakshatra lord from the 27-nakshatra scheme (same as 1.7 above) |
| **Reference** | KP Reader Vol. 1 |

### 2.2 Sub Lord

| Item | Detail |
|------|--------|
| **Formula** | Each nakshatra (13 deg 20 min) is divided into 9 unequal sub-parts proportional to Vimshottari Dasha years. Sub-lord sequence starts from the nakshatra lord and follows Vimshottari order. |
| **Sub-span** | `sub_span = (planet_years / 120) * 13.3333 degrees` |
| **Vimshottari proportions** | Ketu=7/120, Venus=20/120, Sun=6/120, Moon=10/120, Mars=7/120, Rahu=18/120, Jupiter=16/120, Saturn=19/120, Mercury=17/120 |
| **Input** | Sidereal longitude (0-360) |
| **Output** | Star lord + Sub lord planet names |
| **Reference** | KP Reader Vol. 2 |

### 2.3 Sub-Sub Lord

| Item | Detail |
|------|--------|
| **Formula** | Each sub-lord span is further divided into 9 sub-sub parts using the same Vimshottari proportions. Sequence starts from the sub lord. `ss_span = (ss_years / 120) * sub_span` |
| **Reference** | KP Reader Vol. 2 |

### 2.4 Significators (House-Planet Connection)

| Level | Rule |
|-------|------|
| **Occupation** | Planet physically present in a house signifies that house |
| **Ownership** | Planet ruling the sign on a house cusp signifies that house |
| **Star Lord Connection** | If a cusp's star lord is a planet, that planet signifies the house |

### 2.5 Significator Strength (4 Levels)

| Level | Name | Rule |
|-------|------|------|
| 1 | Very Strong | Planet is an occupant of the house |
| 2 | Strong | Planet's nakshatra lord is an occupant of the house |
| 3 | Normal | Planet's nakshatra lord is the cusp sign lord of the house |
| 4 | Weak | Planet IS the cusp sign lord but not an occupant |

**Reference:** KP Reader Vol. 3 -- "Significators and their relative strengths"

### 2.6 Ruling Planets

| Ruling Planet | Source |
|--------------|--------|
| Day Lord | Lord of the weekday (Sun=Sunday, Moon=Monday, etc.) |
| Lagna Lord | Sign lord of the ascendant sign |
| Lagna Nakshatra Lord | Nakshatra lord of the ascendant degree |
| Lagna Sub Lord | Sub lord of the ascendant degree |
| Moon Rashi Lord | Sign lord of Moon's sign |
| Moon Nakshatra Lord | Nakshatra lord of Moon's degree |
| Moon Sub Lord | Sub lord of Moon's degree |

**Reference:** KP Reader Vol. 6 -- Ruling Planets for timing events

### 2.7 Sign Lord Map

Standard Parashari rulership used throughout KP:

| Sign | Lord | Sign | Lord |
|------|------|------|------|
| Aries | Mars | Libra | Venus |
| Taurus | Venus | Scorpio | Mars |
| Gemini | Mercury | Sagittarius | Jupiter |
| Cancer | Moon | Capricorn | Saturn |
| Leo | Sun | Aquarius | Saturn |
| Virgo | Mercury | Pisces | Jupiter |

---

## 3. Vimshottari Dasha

**Source:** `app/dasha_engine.py`
**Classical Reference:** BPHS Chapter 46
**Tab:** Dasha tab

### 3.1 Dasha Periods

| Planet | Years | Planet | Years |
|--------|-------|--------|-------|
| Ketu | 7 | Rahu | 18 |
| Venus | 20 | Jupiter | 16 |
| Sun | 6 | Saturn | 19 |
| Moon | 10 | Mercury | 17 |
| Mars | 7 | **Total** | **120** |

### 3.2 Dasha Balance at Birth

| Item | Detail |
|------|--------|
| **Formula** | `traversed = moon_longitude - nakshatra_start_degree`; `remaining_fraction = (13.3333 - traversed) / 13.3333`; `first_dasha_years = full_years * remaining_fraction` |
| **Meaning** | If Moon is at the START of its nakshatra, full dasha remains. If at the END, almost none remains. |
| **Input** | Birth nakshatra, Moon sidereal longitude |
| **Output** | Fraction (0.0 to 1.0) representing remaining first dasha |
| **Reference** | BPHS Chapter 46 -- "The balance of Dasha at birth" |

### 3.3 Starting Lord

| Item | Detail |
|------|--------|
| **Rule** | First Mahadasha lord = nakshatra lord of Moon's birth nakshatra |
| **Sequence** | Follows Vimshottari order starting from the birth lord: Ketu -> Venus -> Sun -> Moon -> Mars -> Rahu -> Jupiter -> Saturn -> Mercury |

### 3.4 Antardasha (Bhukti)

| Item | Detail |
|------|--------|
| **Formula** | `antardasha_duration = (mahadasha_years * sub_planet_years / 120) * 365.25 days` |
| **Sequence** | Starts from the Mahadasha lord, follows Vimshottari order |
| **Reference** | BPHS Chapter 46 |

### 3.5 Pratyantar Dasha

| Item | Detail |
|------|--------|
| **Formula** | `pratyantar_duration = antardasha_duration_days * p_years / 120` |
| **Sequence** | Starts from the Antardasha lord, follows Vimshottari order |
| **Reference** | BPHS Chapter 46 |

---

## 4. Ashtakvarga

**Source:** `app/ashtakvarga_engine.py`
**Classical Reference:** BPHS Chapters 66-72, Brihaj Jataka
**Tab:** Ashtakvarga tab

### 4.1 Bindu (Point) System

| Item | Detail |
|------|--------|
| **Receiving planets** | Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn + Lagna |
| **Contributing bodies** | Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn + Ascendant (8 contributors) |
| **Bindu value** | 0 or 1 per sign per contributor |
| **Formula** | For each receiving planet, each contributor has a fixed set of "benefic houses" (counted from the contributor's position). If house N is benefic, the sign at `(contributor_sign + N - 1) mod 12` gets 1 bindu. |
| **Reference** | BPHS Chapter 66 |

### 4.2 Benefic Points Table (select examples)

**Sun's Ashtakvarga benefic houses from each contributor:**

| Contributor | Benefic Houses |
|------------|---------------|
| Sun | 1, 2, 4, 7, 8, 9, 10, 11 |
| Moon | 3, 6, 10, 11 |
| Mars | 1, 2, 4, 7, 8, 9, 10, 11 |
| Mercury | 3, 5, 6, 9, 10, 11, 12 |
| Jupiter | 5, 6, 9, 11 |
| Venus | 6, 7, 12 |
| Saturn | 1, 2, 4, 7, 8, 9, 10, 11 |
| Ascendant | 3, 4, 6, 10, 11, 12 |

Full benefic house tables are defined for all 8 receiving planets as per BPHS.

### 4.3 Sarvashtakvarga (SAV)

| Item | Detail |
|------|--------|
| **Formula** | SAV for each sign = sum of bindus across all 7 planets (Lagna excluded from SAV) |
| **Range** | 0 to 56 per sign (7 planets x 8 contributors, max 1 each) |
| **Interpretation** | Signs with SAV >= 28 are strong for transits; < 28 are weak |
| **Reference** | BPHS Chapter 70 |

---

## 5. Shadbala

**Source:** `app/shadbala_engine.py`
**Classical Reference:** BPHS Chapter 27 -- "Shadbala (Six Sources of Strength)"
**Tab:** Shadbala tab
**Unit:** Virupas (1 Rupa = 60 Virupas)

### 5.1 Minimum Required Strength

| Planet | Required (Virupas) |
|--------|-------------------|
| Sun | 390 |
| Moon | 360 |
| Mars | 300 |
| Mercury | 420 |
| Jupiter | 390 |
| Venus | 330 |
| Saturn | 300 |

### 5.2 Component 1: Sthana Bala (Positional Strength)

5 sub-components:

#### 5.2a Uchcha Bala (Exaltation Strength)

| Item | Detail |
|------|--------|
| **Formula** | `uchcha_bala = (180 - angular_distance(planet_lon, exaltation_degree)) / 3` clamped to [0, 60] |
| **Max** | 60 Virupas at exact exaltation degree |
| **Min** | 0 Virupas at debilitation point (180 deg away) |

**Exaltation degrees:**

| Planet | Degree | Planet | Degree |
|--------|--------|--------|--------|
| Sun | 10 deg Aries | Jupiter | 5 deg Cancer |
| Moon | 3 deg Taurus | Venus | 27 deg Pisces |
| Mars | 28 deg Capricorn | Saturn | 20 deg Libra |
| Mercury | 15 deg Virgo | | |

#### 5.2b Saptavargaja Bala (Dignity in 7 Vargas)

| Item | Detail |
|------|--------|
| **Charts assessed** | D1, D2, D3, D7, D9, D12, D30 |
| **Scoring per chart** | Moolatrikona=45, Own=30, Great Friend=22.5, Friend=15, Neutral=7.5, Enemy=3.75, Great Enemy=1.875 |
| **Total** | Sum across 7 charts |
| **Reference** | BPHS Chapter 27 |

#### 5.2c Ojhayugma Bala (Odd/Even Strength)

| Item | Detail |
|------|--------|
| **Formula** | Moon and Venus get 15 Virupas in even signs + 15 in even houses. All other planets get 15 in odd signs + 15 in odd houses. |
| **Max** | 30 Virupas |

#### 5.2d Kendra Bala

| House Type | Houses | Virupas |
|-----------|--------|---------|
| Kendra | 1, 4, 7, 10 | 60 |
| Panaphara | 2, 5, 8, 11 | 30 |
| Apoklima | 3, 6, 9, 12 | 15 |

#### 5.2e Drekkana Bala

| Category | Planets | Strong Drekkana | Virupas |
|----------|---------|----------------|---------|
| Male | Sun, Mars, Jupiter | 1st (0-10 deg) | 15 |
| Female | Moon, Venus | 3rd (20-30 deg) | 15 |
| Neutral | Mercury, Saturn | 2nd (10-20 deg) | 15 |

### 5.3 Component 2: Dig Bala (Directional Strength)

| Item | Detail |
|------|--------|
| **Formula** | `dig_bala = 60 * (1 - house_distance / 6)` where house_distance is the shortest arc on the 12-house circle from the planet's house to its strong house |
| **Max** | 60 Virupas at strongest house |

| Planet | Strongest House |
|--------|----------------|
| Sun | 10th |
| Moon | 4th |
| Mars | 10th |
| Mercury | 1st |
| Jupiter | 1st |
| Venus | 4th |
| Saturn | 7th |

**Reference:** BPHS Chapter 27

### 5.4 Component 3: Kala Bala (Temporal Strength)

8 sub-components:

#### 5.4a Nathonnatha Bala (Diurnal/Nocturnal)

| Category | Planets | Rule |
|----------|---------|------|
| Diurnal | Sun, Jupiter, Venus | Max 60 at noon, 0 at midnight. Formula: `60 * (1 - dist_from_noon/12)` |
| Nocturnal | Moon, Mars, Saturn | Max 60 at midnight, 0 at noon. Formula: `60 - diurnal_strength` |
| Ubhaya | Mercury | Always 60 |

#### 5.4b Paksha Bala (Lunar Phase Strength)

| Item | Detail |
|------|--------|
| **Formula** | Shukla Paksha (0-180 deg elongation): `benefic_val = elongation / 3`; Krishna Paksha (180-360): `benefic_val = (360 - elongation) / 3` |
| **Benefics** | Jupiter, Venus, Moon, Mercury get `benefic_val` |
| **Malefics** | Sun, Mars, Saturn get `60 - benefic_val` |

#### 5.4c Tribhaga Bala

| Period | 1st Third | 2nd Third | 3rd Third |
|--------|-----------|-----------|-----------|
| Day | Mercury=60 | Sun=60 | Saturn=60 |
| Night | Moon=60 | Venus=60 | Mars=60 |
| Always | Jupiter=60 at all times |

#### 5.4d-f Abda, Masa, Vara Bala

| Type | Lord gets | Formula |
|------|----------|---------|
| Abda (Year) | 15 Virupas | Year lord = planet at index `(year mod 7)` in cycle |
| Masa (Month) | 30 Virupas | Month lord = planet at index `(month-1) mod 7` in cycle |
| Vara (Day) | 45 Virupas | Day lord from standard weekday mapping |

#### 5.4g Hora Bala

| Item | Detail |
|------|--------|
| **Formula** | Planetary hours follow Chaldean order (Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon). First hour of each day ruled by day lord. `hora_lord_index = (day_start_index + hour_number) mod 7`. Lord of birth hour gets 60 Virupas. |

#### 5.4h Ayana Bala (Declination Strength)

| Item | Detail |
|------|--------|
| **Formula** | `tropical = sidereal + ayanamsa`; `declination = arcsin(sin(23.44) * sin(tropical))`; `benefic_val = 60 * (declination + 23.44) / (2 * 23.44)` |
| **Benefics** | Jupiter, Venus, Moon, Mercury get `benefic_val` |
| **Malefics** | Sun, Mars, Saturn get `60 - benefic_val` |

### 5.5 Component 4: Cheshta Bala (Motional Strength)

| Condition | Virupas |
|-----------|---------|
| Retrograde | 60 |
| Stationary (speed < 10% of avg) | 45 |
| Normal direct motion | 30 |
| Fast (speed > 150% of avg) | 15 |
| Sun / Moon (no Cheshta Bala) | 0 |

Average daily speeds: Mars=0.524, Mercury=1.383, Jupiter=0.083, Venus=1.2, Saturn=0.034 deg/day.

### 5.6 Component 5: Naisargika Bala (Natural Strength)

Fixed values per BPHS:

| Planet | Virupas |
|--------|---------|
| Sun | 60.00 |
| Moon | 51.43 |
| Venus | 42.86 |
| Jupiter | 34.29 |
| Mercury | 25.71 |
| Mars | 17.14 |
| Saturn | 8.57 |

### 5.7 Component 6: Drik Bala (Aspectual Strength)

| Item | Detail |
|------|--------|
| **Formula** | For each aspecting planet: compute aspect strength from house distance, then add (if aspecting planet is benefic) or subtract (if malefic). Total clamped to [-60, 60]. |
| **Full aspect (60 Virupas)** | 7th house for all planets |
| **Special aspects (45 Virupas)** | Mars: 4th, 8th; Jupiter: 5th, 9th; Saturn: 3rd, 10th |
| **Benefics** | Jupiter, Venus, Moon, Mercury |
| **Malefics** | Sun, Mars, Saturn |
| **Reference** | BPHS Chapter 27-28 |

### 5.8 Total Shadbala

`Total = Sthana + Dig + Kala + Cheshta + Naisargika + Drik`

Ishta/Kashta Phala and Shadbala Ratio are derived from these totals.

---

## 6. Panchang

**Source:** `app/panchang_engine.py`
**Classical Reference:** Surya Siddhanta, BPHS, various Panchangam traditions
**Tab:** Panchang tab

### 6.1 Tithi (Lunar Day)

| Item | Detail |
|------|--------|
| **Formula** | `tithi_index = int(elongation / 12)` where `elongation = (Moon_tropical - Sun_tropical) mod 360` |
| **Span** | 12 degrees of elongation per tithi |
| **Count** | 30 tithis: Shukla Pratipada (1) through Purnima (15), then Krishna Pratipada (16) through Amavasya (30) |
| **End time** | Binary search for next 12-degree boundary crossing |
| **Reference** | Surya Siddhanta |

### 6.2 Nakshatra (Lunar Mansion)

| Item | Detail |
|------|--------|
| **Formula** | `nakshatra_index = int(moon_sidereal_longitude / 13.3333)` |
| **End time** | Binary search for Moon crossing next 13.3333-degree boundary |
| **Reference** | Surya Siddhanta, BPHS |

### 6.3 Yoga (Sun-Moon Combination)

| Item | Detail |
|------|--------|
| **Formula** | `yoga_angle = (sun_sidereal + moon_sidereal) mod 360`; `yoga_index = int(yoga_angle / 13.3333)` |
| **Count** | 27 yogas: Vishkambha, Priti, Ayushman, Saubhagya, Shobhana, Atiganda, Sukarma, Dhriti, Shoola, Ganda, Vriddhi, Dhruva, Vyaghata, Harshana, Vajra, Siddhi, Vyatipata, Variyan, Parigha, Shiva, Siddha, Sadhya, Shubha, Shukla, Brahma, Indra, Vaidhriti |
| **End time** | Binary search for sum crossing next 13.3333-degree boundary |
| **Reference** | Surya Siddhanta |

### 6.4 Karana (Half-Tithi)

| Item | Detail |
|------|--------|
| **Formula** | `karana_index = int(elongation / 6)` (each karana = 6 degrees of elongation) |
| **Count** | 60 karanas per lunar month: 7 repeating (Bava, Balava, Kaulava, Taitila, Garaja, Vanija, Vishti) cycling through positions 1-56, plus 4 fixed (Kimstughna at 0, Shakuni at 57, Chatushpada at 58, Naga at 59) |
| **Reference** | Surya Siddhanta |

### 6.5 Sunrise / Sunset

| Item | Detail |
|------|--------|
| **Primary (swisseph)** | `swe.rise_trans()` with `CALC_RISE/CALC_SET` and `BIT_DISC_CENTER` flags |
| **Fallback (NOAA)** | Declination = `23.45 * sin(360/365 * (DOY - 81))`; Hour Angle = `acos(-tan(lat) * tan(dec))`; Sunrise/Sunset from solar noon +/- hour angle; EoT correction: `9.87*sin(2B) - 7.53*cos(B) - 1.5*sin(B)` |
| **Reference** | NOAA Solar Calculator |

### 6.6 Rahu Kaal, Gulika Kaal, Yamaganda Kaal

| Item | Detail |
|------|--------|
| **Formula** | Divide daytime (sunrise to sunset) into 8 equal slots. Each weekday has a fixed slot number for each kaal. `slot_duration = day_duration / 8`; `start = sunrise + (slot - 1) * slot_duration` |
| **Reference** | Traditional Panchangam |

**Rahu Kaal slot by weekday:**

| Day | Mon | Tue | Wed | Thu | Fri | Sat | Sun |
|-----|-----|-----|-----|-----|-----|-----|-----|
| Slot | 2 | 7 | 5 | 6 | 4 | 3 | 8 |

### 6.7 Abhijit Muhurat

| Item | Detail |
|------|--------|
| **Formula** | Divide daytime into 15 muhurats. Abhijit = the 8th muhurat (midday). `muhurat_duration = day_duration / 15`; `start = sunrise + 7 * muhurat_duration` |
| **Reference** | Muhurta Chintamani |

### 6.8 Brahma Muhurat

| Item | Detail |
|------|--------|
| **Formula** | 96 to 48 minutes before sunrise. One Vedic muhurat = 48 minutes. Brahma Muhurat = 2 muhurats before sunrise. |
| **Reference** | Dharmashastra texts |

### 6.9 Choghadiya

| Item | Detail |
|------|--------|
| **Formula** | Divide daytime into 8 equal periods. Each weekday has a fixed sequence of 8 named periods. |
| **Qualities** | Amrit=Best, Shubh=Good, Labh=Good, Char=Neutral, Rog=Inauspicious, Kaal=Inauspicious, Udveg=Inauspicious |
| **Reference** | Gujarat/Rajasthan Panchangam tradition |

### 6.10 Hindu Calendar

| Element | Formula |
|---------|---------|
| Vikram Samvat | `Gregorian year + 57` (adjusted -1 before April) |
| Shaka Samvat | `Gregorian year - 78` (adjusted -1 before April) |
| Maas (Month) | From Sun sidereal longitude: `solar_month_index = int(sun_sid / 30)` mapped to Chaitra through Phalguna |
| Paksha | Shukla if tithi_index < 15, else Krishna |
| Ritu (Season) | 6 seasons, 2 months each: Vasanta, Grishma, Varsha, Sharad, Hemanta, Shishira |
| Ayana | Uttarayana (solar months 9-2), Dakshinayana (3-8) |

---

## 7. Divisional Charts

**Source:** `app/divisional_charts.py`
**Classical Reference:** BPHS Chapters 6-7
**Tab:** Divisional Charts tab

### 7.1 Supported Charts

| Chart | Name | Division | Signification |
|-------|------|----------|---------------|
| D1 | Rashi | 1 | Main birth chart |
| D2 | Hora | 2 | Wealth |
| D3 | Drekkana | 3 | Siblings/courage |
| D4 | Chaturthamsha | 4 | Property/fortune |
| D7 | Saptamsha | 7 | Children/progeny |
| D9 | Navamsha | 9 | Marriage/dharma |
| D10 | Dasamsha | 10 | Career/profession |
| D12 | Dwadashamsha | 12 | Parents |
| D16 | Shodashamsha | 16 | Vehicles/happiness |
| D20 | Vimshamsha | 20 | Spiritual progress |
| D24 | Chaturvimshamsha | 24 | Education |
| D27 | Bhamsha | 27 | Strength/weakness |
| D30 | Trimshamsha | 30 | Evils/misfortunes |
| D40 | Khavedamsha | 40 | Auspicious effects |
| D45 | Akshavedamsha | 45 | General indications |
| D60 | Shashtiamsha | 60 | Past life karma |

### 7.2 Formulas

#### D2 (Hora)

| Sign Type | 0-15 deg | 15-30 deg |
|-----------|----------|-----------|
| Odd sign | Leo (Sun) | Cancer (Moon) |
| Even sign | Cancer (Moon) | Leo (Sun) |

#### D3 (Drekkana)

| Segment | Degrees | Maps to |
|---------|---------|---------|
| 1st | 0-10 | Same sign |
| 2nd | 10-20 | 5th sign from rashi |
| 3rd | 20-30 | 9th sign from rashi |

#### D4 (Chaturthamsha)

Each 7.5-degree segment advances by 3 signs (quadrants) from rashi sign.

#### D7 (Saptamsha)

| Sign Type | Start |
|-----------|-------|
| Odd sign | Same sign, advance 1 per 4.2857-deg segment |
| Even sign | 7th from sign, advance 1 per segment |

#### D9 (Navamsha)

Each 3 deg 20 min segment. Starting sign depends on element:

| Element | Signs | Start From |
|---------|-------|-----------|
| Fire | Aries, Leo, Sagittarius | Aries |
| Earth | Taurus, Virgo, Capricorn | Capricorn |
| Air | Gemini, Libra, Aquarius | Libra |
| Water | Cancer, Scorpio, Pisces | Cancer |

#### D10 (Dasamsha)

Each 3-degree segment. Odd signs start from same sign; even signs start from 9th sign.

#### D12 (Dwadashamsha)

Each 2.5-degree segment. Starts from same sign, advances through all 12 signs.

#### D30 (Trimshamsha)

Unequal divisions per BPHS:

| **Odd signs** | Degrees | Lord (Sign) |
|--------------|---------|-------------|
| 0-5 | Mars (Aries) |
| 5-10 | Saturn (Aquarius) |
| 10-18 | Jupiter (Sagittarius) |
| 18-25 | Mercury (Gemini) |
| 25-30 | Venus (Taurus) |

| **Even signs** | Degrees | Lord (Sign) |
|---------------|---------|-------------|
| 0-5 | Venus (Libra) |
| 5-12 | Mercury (Virgo) |
| 12-20 | Jupiter (Pisces) |
| 20-25 | Saturn (Capricorn) |
| 25-30 | Mars (Scorpio) |

#### Generic Formula (D16, D20, D24, D27, D40, D45, D60)

`part_index = floor(degree_in_sign / (30 / division))`
`result_sign = (rashi_index * division + part_index) mod 12`

---

## 8. Doshas and Yogas

**Source:** `app/dosha_engine.py`
**Classical Reference:** BPHS, Phaladeepika, Jataka Parijata
**Tab:** Doshas tab

### 8.1 Mangal Dosha (Kuja Dosha)

| Item | Detail |
|------|--------|
| **Rule** | Mars in houses {1, 2, 4, 7, 8, 12} from Lagna causes Mangal Dosha |
| **Severity** | High: houses 7, 8; Medium: houses 1, 4; Mild: houses 2, 12 |
| **Reference** | BPHS, Lal Kitab |

### 8.2 Kaal Sarp Dosha

| Item | Detail |
|------|--------|
| **Rule** | All 7 planets (Sun through Saturn) hemmed between the Rahu-Ketu axis (all on one side) |
| **Types** | Ascending (Rahu leading) or Descending (Ketu leading) |
| **Named types** | Based on Rahu's house: 1=Anant, 2=Kulik, 3=Vasuki, 4=Shankhpal, 5=Padma, 6=Mahapadma, 7=Takshak, 8=Karkotak, 9=Shankhachur, 10=Ghatak, 11=Vishdhar, 12=Sheshnag |
| **Reference** | Lal Kitab, modern Jyotish texts |

### 8.3 Sade Sati

| Item | Detail |
|------|--------|
| **Rule** | Saturn transiting 12th from Moon (Rising), same sign as Moon (Peak), or 2nd from Moon (Setting) |
| **Formula** | `moon_idx = ZODIAC_INDEX[moon_sign]`; check if Saturn is at `(moon_idx - 1) mod 12`, `moon_idx`, or `(moon_idx + 1) mod 12` |
| **Duration** | ~7.5 years total (2.5 years per phase) |
| **Reference** | Classical transit texts, Phaladeepika |

### 8.4 Pitra Dosha

| Item | Detail |
|------|--------|
| **Rule** | (1) Sun conjunct Rahu or Ketu (same house), OR (2) Sun in 9th house with a malefic (Mars, Saturn, Rahu, Ketu) |
| **Reference** | BPHS, Pitra Dosha chapters |

### 8.5 Kemdrum Dosha

| Item | Detail |
|------|--------|
| **Rule** | No planets (excluding Rahu/Ketu) in the 2nd or 12th house from Moon |
| **Checked planets** | Sun, Mars, Mercury, Jupiter, Venus, Saturn |
| **Reference** | Phaladeepika, BPHS |

### 8.6 Gajakesari Yoga

| Item | Detail |
|------|--------|
| **Rule** | Jupiter in a Kendra (houses 1, 4, 7, 10) from Moon |
| **Reference** | Phaladeepika Chapter 6 |

### 8.7 Budhaditya Yoga

| Item | Detail |
|------|--------|
| **Rule** | Sun and Mercury in the same house |
| **Reference** | BPHS |

### 8.8 Chandra-Mangal Yoga

| Item | Detail |
|------|--------|
| **Rule** | Moon and Mars in the same house |
| **Reference** | Classical Jyotish texts |

### 8.9 Panch Mahapurusha Yogas

| Yoga | Planet | Condition |
|------|--------|-----------|
| Ruchaka | Mars | In own sign (Aries/Scorpio) or exaltation (Capricorn) AND in Kendra (1,4,7,10) |
| Bhadra | Mercury | In own sign (Gemini/Virgo) or exaltation (Virgo) AND in Kendra |
| Hamsa | Jupiter | In own sign (Sagittarius/Pisces) or exaltation (Cancer) AND in Kendra |
| Malavya | Venus | In own sign (Taurus/Libra) or exaltation (Pisces) AND in Kendra |
| Sasa | Saturn | In own sign (Capricorn/Aquarius) or exaltation (Libra) AND in Kendra |

**Reference:** BPHS Chapter 75, Phaladeepika Chapter 15

---

## 9. Kundli Matching

**Source:** `app/matching_engine.py`
**Classical Reference:** Muhurta Chintamani, BPHS matching chapters, North Indian tradition
**Tab:** Matching tab

### 9.1 Ashta Koota (8 Matching Factors)

| Koota | Max Points | Basis | Formula |
|-------|-----------|-------|---------|
| **Varna** | 1 | Spiritual rank | Groom's varna >= Bride's varna. Ranks: Brahmin=4, Kshatriya=3, Vaishya=2, Shudra=1 |
| **Vasya** | 2 | Mutual attraction | Based on Moon rashi mapped to Vasya groups: Chatushpada, Manava, Jalchar, Vanchar, Keeta. Same=2, compatible=1, Keeta conflict=0 |
| **Tara** | 3 | Birth star compatibility | `D = (bride_nak - groom_nak) mod 27`; `R = D mod 9`; Favorable if R in {1,3,5,7,8} -> 3 pts, else 0 |
| **Yoni** | 4 | Physical compatibility | Each nakshatra has an animal. Same=4, Friendly pair=3, Neutral=2, Enemy pair=0 |
| **Graha Maitri** | 5 | Mental compatibility | Based on nakshatra lords' friendship. Same lord or mutual friends=5, friend+neutral=4, both neutral=3, friend+enemy=1, mutual enemies=0 |
| **Gana** | 6 | Temperament | 3 ganas: Deva, Manushya, Rakshasa. Same=6, Deva-Manushya=5, Deva-Rakshasa=1, Manushya-Rakshasa=0 |
| **Bhakoot** | 7 | Emotional/financial | Rashi distance ratios. Unfavorable: 2/12, 5/9, 6/8 -> 0 pts; all others -> 7 pts |
| **Nadi** | 8 | Health/genetic | 3 nadis: Aadi, Madhya, Antya. Same nadi=0 (Nadi Dosha!), different=8 |

**Total: 36 points**

### 9.2 Compatibility Rating

| Score | Rating |
|-------|--------|
| 30+ | Exceptional match |
| 24-29 | Excellent match |
| 18-23 | Good match |
| < 18 | Not recommended |

### 9.3 Dosha Cancellation Rules

**Nadi Dosha cancellation (any of):**
- Both persons have the same rashi
- Both persons have the same nakshatra
- Nakshatra lords are friends

**Bhakoot Dosha cancellation (any of):**
- Same rashi lord for both signs
- Rashi lords are mutual friends
- Nadi koot scored full 8

### 9.4 Yoni Enemy Pairs

Horse-Buffalo, Elephant-Lion, Dog-Deer, Serpent-Mongoose, Cat-Rat, Monkey-Goat, Tiger-Cow

---

## 10. Numerology

**Source:** `app/numerology_engine.py`
**Classical Reference:** Pythagorean Numerology, Cheiro, Sephariyal, J.C. Chaudhry (mobile numerology per Batraa method)
**Tab:** Numerology tab

### 10.1 Pythagorean Number Map

```
A=1 B=2 C=3 D=4 E=5 F=6 G=7 H=8 I=9
J=1 K=2 L=3 M=4 N=5 O=6 P=7 Q=8 R=9
S=1 T=2 U=3 V=4 W=5 X=6 Y=7 Z=8
```

### 10.2 Core Numbers

| Number | Derivation | Formula |
|--------|-----------|---------|
| **Life Path** | Birth date | Sum all digits of YYYY-MM-DD, reduce to single digit or master number |
| **Expression (Destiny)** | Full name | Sum Pythagorean values of ALL letters, reduce |
| **Soul Urge** | Name vowels | Sum values of vowels (A, E, I, O, U) only, reduce |
| **Personality** | Name consonants | Sum values of consonants only, reduce |

### 10.3 Reduction Rule

Sum digits repeatedly until a single digit (1-9) or master number (11, 22, 33) is reached. Master numbers are NOT reduced further.

### 10.4 Mobile Numerology (Batraa Method)

| Item | Detail |
|------|--------|
| **Mobile Total** | Sum all digits of mobile number, reduce to single digit or master number |
| **Digit-Pair Analysis** | Each consecutive pair of digits classified as Benefic, Neutral, or Malefic based on planetary friendship |
| **Planetary mapping** | 1=Sun, 2=Moon, 3=Jupiter, 4=Rahu, 5=Mercury, 6=Venus, 7=Ketu, 8=Saturn, 9=Mars |
| **Pair rules** | Mutual friends -> Benefic; Either enemy -> Malefic; Otherwise -> Neutral; 0 pairs always Neutral |
| **Loshu Grid** | Standard 3x3: `[4,9,2 / 3,5,7 / 8,1,6]` -- digits present/missing analyzed |

---

## 11. Lal Kitab

**Source:** `app/lalkitab_engine.py`
**Classical Reference:** Lal Kitab (original Urdu text by Pt. Roop Chand Joshi, 1939-1952)
**Tab:** Lal Kitab tab

### 11.1 Remedy Trigger

| Item | Detail |
|------|--------|
| **Rule** | Remedies prescribed only when `planet_strength < 0.5` (enemy or debilitated placement) |
| **Strength source** | `get_planet_strength(planet, sign)` from dignity tables |
| **Dignity hierarchy** | Exalted > Own Sign > Friendly > Neutral > Enemy > Debilitated |

### 11.2 Remedies Per Planet

5-8 classical Lal Kitab remedies per planet covering: gemstone, donation items, day of week, specific rituals, behavioral prescriptions. All 9 Vedic planets covered (Sun through Ketu).

---

## 12. Transits

**Source:** `app/transit_engine.py`
**Classical Reference:** Phaladeepika Chapter 26 (Gochara), BPHS transit rules
**Tab:** Transit tab

### 12.1 Gochara (Transit) Effect

| Item | Detail |
|------|--------|
| **Formula** | `house_from_moon = ((transit_sign_index - natal_moon_sign_index) mod 12) + 1` |
| **Effect** | Favorable if house is in planet's favorable set, unfavorable otherwise |

### 12.2 Favorable Houses (from Natal Moon)

| Planet | Favorable Houses |
|--------|-----------------|
| Jupiter | 2, 5, 7, 9, 11 |
| Saturn | 3, 6, 11 |
| Rahu | 3, 6, 11 |
| Ketu | 3, 6, 11 |
| Mars | 3, 6, 11 |
| Venus | 1, 2, 3, 4, 5, 8, 9, 11, 12 |
| Sun | 3, 6, 10, 11 |
| Mercury | 2, 4, 6, 8, 10, 11 |
| Moon | 1, 3, 6, 7, 10, 11 |

**Reference:** Phaladeepika Chapter 26, Brihat Samhita

### 12.3 Sade Sati (Transit-Based)

Same logic as Section 8.3, applied to current Saturn transit position vs natal Moon sign.

---

## 13. Varshphal (Solar Return / Tajaka)

**Source:** `app/varshphal_engine.py`
**Classical Reference:** Tajaka Neelakanthi, Varshphal Paddhati
**Tab:** Varshphal tab

### 13.1 Solar Return Moment

| Item | Detail |
|------|--------|
| **Method** | Newton-Raphson iteration on Swiss Ephemeris |
| **Goal** | Find exact JD when Sun's sidereal longitude equals natal Sun's sidereal longitude in the target year |
| **Formula** | `delta = current_sun_lon - natal_sun_lon` (normalized to [-180, 180]); `jd -= delta / 0.9856` (Sun's avg speed); iterate until `abs(delta) < 0.0001 deg` (~0.36 arcsec accuracy) |
| **Reference** | Tajaka Neelakanthi |

### 13.2 Muntha (Annual Progressed Ascendant)

| Item | Detail |
|------|--------|
| **Formula** | `muntha_sign_index = (natal_asc_sign_index + completed_years) mod 12` |
| **Meaning** | Muntha advances one sign per year from natal ascendant |
| **Favorable houses** | 1, 2, 3, 4, 5, 9, 10, 11 in Varshphal chart |
| **Reference** | Tajaka Neelakanthi Chapter 3 |

### 13.3 Year Lord (Varsheshwar)

| Item | Detail |
|------|--------|
| **Formula** | Lord of the weekday on which the Solar Return falls. `day_of_week = int(sr_jd + 0.5) mod 7` |
| **Day lords** | Mon=Moon, Tue=Mars, Wed=Mercury, Thu=Jupiter, Fri=Venus, Sat=Saturn, Sun=Sun |
| **Reference** | Tajaka Neelakanthi |

### 13.4 Mudda Dasha (Annual Planetary Periods)

| Planet | Days |
|--------|------|
| Sun | 110 |
| Moon | 60 |
| Mars | 32 |
| Mercury | 40 |
| Jupiter | 48 |
| Venus | 56 |
| Saturn | 4 |
| **Total** | **350** |

| Item | Detail |
|------|--------|
| **Sequence** | Tajaka cycle: Sun -> Venus -> Mercury -> Moon -> Saturn -> Jupiter -> Mars, starting from the Year Lord |
| **Reference** | Tajaka Neelakanthi Chapter 5 |

---

## Appendix A: Natural Planetary Friendships (BPHS)

Used across multiple engines (Shadbala, Matching, KP):

| Planet | Friends | Enemies | Neutral |
|--------|---------|---------|---------|
| Sun | Moon, Mars, Jupiter | Venus, Saturn | Mercury |
| Moon | Sun, Mercury | (none) | Mars, Jupiter, Venus, Saturn |
| Mars | Sun, Moon, Jupiter | Mercury | Venus, Saturn |
| Mercury | Sun, Venus | Moon | Mars, Jupiter, Saturn |
| Jupiter | Sun, Moon, Mars | Mercury, Venus | Saturn |
| Venus | Mercury, Saturn | Sun, Moon | Mars, Jupiter |
| Saturn | Mercury, Venus | Sun, Moon, Mars | Jupiter |

**Reference:** BPHS Chapter 3

---

## Appendix B: Node Types

| Setting | Constant | Description |
|---------|----------|-------------|
| Mean Node | SE_MEAN_NODE (10) | Average position of lunar node; used by most Vedic astrologers |
| True Node | SE_TRUE_NODE (11) | Osculating (actual) node position; used by some KP practitioners |
| Ketu | Rahu + 180 deg | Always derived; never computed independently |

---

## Appendix C: Computation Pipeline

```
User Input (date, time, lat, lon, tz)
  |
  v
[1] Parse datetime -> UTC -> Julian Day
  |
  v
[2] Swiss Ephemeris -> Tropical longitudes + daily speeds
  |
  v
[3] Apply Ayanamsa -> Sidereal longitudes
  |
  v
[4] Compute Ascendant + Houses (Whole Sign)
  |
  v
[5] Derive: sign, nakshatra, pada, house, dignity,
     combust, vargottama, sandhi, retrograde
  |
  v
[6] Feed into downstream engines:
     KP -> Dasha -> Ashtakvarga -> Shadbala ->
     Panchang -> Divisional -> Dosha -> Matching ->
     Transit -> Varshphal
```

---

*Generated from source code analysis of AstroRattan engine files, April 2026.*
