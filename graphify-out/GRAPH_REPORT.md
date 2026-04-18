# Graph Report - .  (2026-04-18)

## Corpus Check
- 507 files · ~5,171,977 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 7776 nodes · 13498 edges · 266 communities detected
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 777 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `KundliRequest` - 74 edges
2. `KundliMatchRequest` - 74 edges
3. `DivisionalChartRequest` - 74 edges
4. `BirthRectificationRequest` - 74 edges
5. `SarvatobhadraRequest` - 74 edges
6. `D108AnalysisRequest` - 74 edges
7. `M()` - 74 edges
8. `KPHoraryRequest` - 67 edges
9. `KPHoraryPredictRequest` - 67 edges
10. `o()` - 56 edges

## Surprising Connections (you probably didn't know these)
- `Calculate Ekadashi Parana time.      Parana is done the morning after Ekadashi,` --rationale_for--> `calculate_ekadashi_parana()`  [EXTRACTED]
  _trash/panchang_ekadashi.py → app/panchang_ekadashi.py
- `Convert 'HH:MM' to minutes from midnight.` --rationale_for--> `_time_to_minutes()`  [EXTRACTED]
  _trash/panchang_ekadashi.py → app/panchang_ekadashi.py
- `Convert minutes from midnight to 'HH:MM'.` --rationale_for--> `_minutes_to_time()`  [EXTRACTED]
  _trash/panchang_ekadashi.py → app/panchang_ekadashi.py
- `Admin routes — user management, stats, kundli overview, live traffic panel.` --uses--> `AdminUserUpdate`  [INFERRED]
  app/routes/admin.py → app/models.py
- `Dashboard stats — user count, kundli count, recent activity.` --uses--> `AdminUserUpdate`  [INFERRED]
  app/routes/admin.py → app/models.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.01
Nodes (125): apiFetch(), fetchWithRetry(), friendlyError(), tryRefreshToken(), rotateByLagna(), SAVKundliChart(), handleOtpKeyDown(), handleResendOtp() (+117 more)

### Community 1 - "Community 1"
Cohesion: 0.01
Nodes (491): a(), aA(), Ab(), ac(), ad(), ag(), ah(), ai() (+483 more)

### Community 2 - "Community 2"
Cohesion: 0.02
Nodes (168): get_live_dashboard(), get_stats(), get_user_detail(), list_all_kundlis(), list_users(), Admin routes — user management, stats, kundli overview, live traffic panel., Change a user's role (user/astrologer/admin)., Activate or deactivate a user account. (+160 more)

### Community 3 - "Community 3"
Cohesion: 0.01
Nodes (54): bs(), Qe(), D(), N(), O(), R(), w(), x() (+46 more)

### Community 4 - "Community 4"
Cohesion: 0.05
Nodes (163): _a(), aa(), ac(), Ae(), af(), ao(), ar(), at() (+155 more)

### Community 5 - "Community 5"
Cohesion: 0.06
Nodes (152): birth_rectification(), _build_kundli_pdf(), _chart_data(), check_doshas(), _compute_dasha(), create_download_token(), d108_analysis(), delete_all_my_kundlis() (+144 more)

### Community 6 - "Community 6"
Cohesion: 0.03
Nodes (109): ac(), ae(), ai(), Ar(), as(), At(), bc(), Be() (+101 more)

### Community 7 - "Community 7"
Cohesion: 0.01
Nodes (141): Tests for app.vastu — Vastu Shastra engine calculations., Residential buildings must use Manduka Mandala (8x8 = 64 squares)., Temple buildings must use Paramasayika Mandala (9x9 = 81 squares)., Mandala must return all 10 zones with devtas., Energy balance positive + negative + neutral must equal 45., Body mapping must include head, face, chest, navel, arms, legs, feet., Each devta must have a unique id from 1 to 45., In a balanced mandala, positive devtas must outnumber negative ones. (+133 more)

### Community 8 - "Community 8"
Cohesion: 0.03
Nodes (129): add_chandra_journal(), add_family_link(), checkin_remedy_tracker(), correlate_palm_marks(), create_remedy_tracker(), _degrees_to_dms(), delete_remedy_tracker(), delete_saved_prediction() (+121 more)

### Community 9 - "Community 9"
Cohesion: 0.02
Nodes (36): _has_hindi(), Tests for app.panchang_nivas -- Nivas, Homahuti & Kumbha Chakra Calculations ===, Krishna Paksha tithis 16-20 cycle back to Prithvi., Validate Rahu Vasa (Rahu residence) calculations., Weekday 7 should wrap to 0 (Sunday = South)., Validate Shivavasa (Shiva residence) calculations., Krishna Paksha: 16-20 back to Gowri., Validate Homahuti (homa planet) calculations. (+28 more)

### Community 10 - "Community 10"
Cohesion: 0.02
Nodes (51): Tests for Phaladeepika Adhyaya 3 (Vargadhyaya) varga-strength grading.  Verifies, 0° Aries (odd) -> part 0 -> Aries., 0° Taurus (even) -> part 0 -> 7th from Taurus = Scorpio., 0° Aries (fire) -> part 0 starts from Aries -> Aries., 29.99° Aries -> part 8 starts from Aries -> Sagittarius (9th)., 270° = 0° Capricorn (earth) -> part 0 from Capricorn -> Capricorn., 3° Aries (2.5-5.0 range = part 1) -> Taurus., 29.99° Aries (part 11) -> Pisces (Aries + 11). (+43 more)

### Community 11 - "Community 11"
Cohesion: 0.02
Nodes (37): test_sarvatobhadra_chakra.py -- Tests for Sarvatobhadra Chakra Engine ==========, Verify specific cells match the canonical SBC layout., All 7 weekdays must appear at least once in the grid., The grid should contain nakshatras in the NAKSHATRA_CELL lookup., 12 zodiac signs should be on the grid (some appear in multiple spots)., Test nakshatra and sign lookup from sidereal longitude., Test that vedha reflections are computed correctly., Center cell (4,4) reflects to itself — no vedha targets. (+29 more)

### Community 12 - "Community 12"
Cohesion: 0.04
Nodes (73): _2(), A_(), a0(), A2(), aT(), b0(), _c(), C2() (+65 more)

### Community 13 - "Community 13"
Cohesion: 0.02
Nodes (54): Tests for lalkitab_interpretations.py — Lal Kitab house-by-house planet interpre, Test the get_lk_house_interpretation() public function., Jupiter in House 1 should return raja_or_fakir nature., Jupiter in House 4 should mention exalted/uchcha., Jupiter in House 10 should mention debilitated., Mars in House 12 should be its strongest position., Mars in House 8 should mention blood disease., Moon in House 4 should be exalted. (+46 more)

### Community 14 - "Community 14"
Cohesion: 0.02
Nodes (40): Tests for app.panchang_yogas -- Special Yoga Calculations ======================, Sunday + Rohini → inactive (needs Hasta)., Monday + Hasta → inactive (Monday needs Rohini)., Sunday (0) + Dwitiya (2) + Chitra → active., Tuesday (2) + Saptami (7) + Mrigashira → active., Saturday (6) + Dwadashi (12) + Vishakha → active., Monday (1) + Dwitiya (2) + Chitra → inactive (Monday not valid)., Sunday (0) + Tritiya (3) + Chitra → inactive (wrong tithi). (+32 more)

### Community 15 - "Community 15"
Cohesion: 0.02
Nodes (37): Tests for KP Horary (Prashna) 1-249 system in app.kp_engine., Every sub_lord must be one of the 9 Vimshottari planets., Every entry's degree range must lie within its stated sign., Splitting the 243 subs at sign boundaries must produce 249 = 243 + 6., Every entry must have a positive degree span., Test the get_horary_entry() lookup function., DMS strings should contain degree symbol., Test the _degree_to_dms helper. (+29 more)

### Community 16 - "Community 16"
Cohesion: 0.02
Nodes (47): Tests for app.panchang_samvat -- Samvat Systems & Pushkara Navamsha., Result should include the samvatsara name for the Gujarati year., All 7 months before Kartik should give VS - 1., Months from Kartik onward should give same VS., Validate Amant/Purnimant conversions., In Shukla paksha, both systems show the same month., In Krishna paksha, Purnimant system shifts to next month., Ashwin Krishna → Purnimant = Kartik. (+39 more)

### Community 17 - "Community 17"
Cohesion: 0.02
Nodes (49): Tests for Lo Shu Grid interpretation — arrows, planes, missing numbers, repeated, When ALL 3 numbers of an arrow are present in DOB digits -> strength arrow., If at least 1 number of an arrow is present, it's NOT a weakness., Weakness arrows must include a missing_meaning field., Mental (3,6,9), Emotional (2,5,8), Practical (1,4,7) plane scoring., DOB 1995-05-19 has digits 1,9,9,5,0,5,1,9 -> non-zero {1,5,9} all present., DOB heavy on 3, 6, 9 -> mental plane dominant., DOB heavy on 2, 5, 8 -> emotional plane dominant. (+41 more)

### Community 18 - "Community 18"
Cohesion: 0.02
Nodes (46): _expected_d108_sign(), Tests for D108 (Ashtottaramsa) divisional chart calculation. Verifies:   - Calcu, Fixed signs start counting from the 9th sign (rasi + 8)., 0 deg Taurus (lon 30) -> part 0 -> start = (1+8)%12 = 9 = Capricorn, 0 deg Leo (lon 120) -> part 0 -> start = (4+8)%12 = 0 = Aries, 0 deg Scorpio (lon 210) -> part 0 -> start = (7+8)%12 = 3 = Cancer, 0 deg Aquarius (lon 300) -> part 0 -> start = (10+8)%12 = 6 = Libra, Part 3 in Taurus -> start(9)+3 = 12 mod 12 = 0 = Aries (+38 more)

### Community 19 - "Community 19"
Cohesion: 0.05
Nodes (81): analyze_yogas_and_doshas(), check_adhi_yoga(), check_amala_yoga(), check_anapha_yoga(), check_angarak_dosha(), check_budhaditya_yoga(), check_chandra_mangal_yoga(), check_danda_yoga() (+73 more)

### Community 20 - "Community 20"
Cohesion: 0.02
Nodes (31): Tests for 6 new core numerology calculations: Birthday Number, Maturity Number,, Born on the 13th — karmic debt 13 from birthday., Born on the 14th — karmic debt 14 from birthday., Born on the 16th — karmic debt 16 from birthday., Born on the 19th — karmic debt 19 from birthday., Born on the 15th — no birthday karmic debt (15 is not 13/14/16/19)., Birthday Number = birth day reduced to single digit or master number., Hidden Passion = most frequently occurring Pythagorean number in name. (+23 more)

### Community 21 - "Community 21"
Cohesion: 0.05
Nodes (79): analyze_loshu_arrows(), analyze_loshu_planes(), analyze_missing_numbers(), analyze_name_numerology(), analyze_repeated_numbers(), _birthday_number(), _build_number_affinities(), _build_pair_combination_table() (+71 more)

### Community 22 - "Community 22"
Cohesion: 0.03
Nodes (27): Tests for app.panchang_tamil -- Tamil Yoga, Jeevanama & Netrama., Thursday (4) should have same Siddha pattern as Sunday (0)., Saturday (6) should have same Siddha pattern as Tuesday (2)., Test calculate_jeevanama() for each tithi range., Validate the Tamil Yoga lookup tables., Test calculate_netrama() for each pada., Netrama depends on pada, not nakshatra identity., Test the master calculate_all_tamil() function. (+19 more)

### Community 23 - "Community 23"
Cohesion: 0.07
Nodes (68): Ae(), ar(), at(), Be(), br(), Ce(), cr(), De() (+60 more)

### Community 24 - "Community 24"
Cohesion: 0.03
Nodes (47): auth_headers(), auth_token(), client(), Route-level tests for /api/kundli/* endpoints.  Uses FastAPI TestClient with a f, POST /api/kundli/generate → 201, returns chart_data with 9 planets., POST /api/kundli/generate with invalid date → 422 or 500., POST /api/kundli/generate without auth → 401., POST /api/kundli/generate with missing required fields → 422. (+39 more)

### Community 25 - "Community 25"
Cohesion: 0.05
Nodes (73): _approx_sunrise_sunset(), calculate_abhijit_muhurat(), calculate_brahma_muhurat(), calculate_choghadiya(), calculate_gulika_kaal(), calculate_night_choghadiya(), calculate_panchang(), calculate_planetary_positions() (+65 more)

### Community 26 - "Community 26"
Cohesion: 0.03
Nodes (32): app_client(), Route-level tests for the 7 new API endpoints.  Tests are split into two parts:, Verify KP Horary engine via route handler arguments., Verify KP Horary prediction engine via route handler arguments., Verify Birth Rectification engine via route handler arguments., Verify Sarvatobhadra Chakra engine via route handler arguments., Verify D108 analysis engine via route handler arguments., Verify Ashtottari Dasha engine via route handler arguments. (+24 more)

### Community 27 - "Community 27"
Cohesion: 0.03
Nodes (43): afflicted_bunyaad_positions(), all_in_one_house(), empty_houses_positions(), Tests for Lal Kitab Bunyaad, Takkar, and Enemy Presence analysis., Result should have an entry for every planet in the input., Jupiter's bunyaad (house 10) has Saturn and Rahu — should be afflicted., Mars bunyaad is house 11 — Venus is there but not an enemy of Mars., With only 2 planets, most bunyaad houses will be empty. (+35 more)

### Community 28 - "Community 28"
Cohesion: 0.03
Nodes (39): chart(), list_positions(), Golden-path E2E tests for the Lal Kitab pipeline.  Uses a fixed reference birth, Validate core ephemeris gives stable, correct positions for ref birth., Reference tests require real Swiss Ephemeris, not the fallback., Ref birth at 6:30 AM Delhi -> Lagna in Sagittarius (sidereal/Lahiri)., Jan 15 1990: Mercury, Jupiter, Venus known retrograde. Stable check., Remedy pipeline must correctly identify weak/afflicted planets. (+31 more)

### Community 29 - "Community 29"
Cohesion: 0.03
Nodes (23): Tests for app.panchang_directions -- Directional & Anandadi Calculations., Tithi 6 should cycle back to Agni (same as tithi 1)., Purnima (tithi 15) = Akasha., Amavasya (tithi 30) = Akasha., Validate Anandadi Yoga calculations., Sunday (0) + Ashwini (0) => (0*7+0)%28 = 0 => Ananda., Monday (1) + Ashwini (0) => (1*7+0)%28 = 7 => Mitra., Sunday (0) + Bharani (1) => (0*7+1)%28 = 1 => Kaldanda. (+15 more)

### Community 30 - "Community 30"
Cohesion: 0.03
Nodes (59): calculate_universal_year_from_module(), forecast_client(), Tests for numerology_forecast_engine.py — Personal Year/Month/Day forecasts., 2018: 2+0+1+8 = 11 (master number preserved)., UY=1 (2026), month=4 (April): 1 + 4 = 5., UY=1, month=4, day=17: universal_month=5, 5+(1+7)=13->4., calculate_forecast must return all personal + universal numbers and predictions., Each prediction group has bilingual keys. (+51 more)

### Community 31 - "Community 31"
Cohesion: 0.05
Nodes (52): assemble_section(), calculate_transit_forecast(), calculate_transit_houses(), calculate_transits(), _check_sade_sati(), compute_scores(), _default_section_text(), _detect_sign_changes() (+44 more)

### Community 32 - "Community 32"
Cohesion: 0.04
Nodes (16): Ar(), Er(), fa(), Fr(), hl(), Hr(), is(), Nn() (+8 more)

### Community 33 - "Community 33"
Cohesion: 0.05
Nodes (53): _abda_bala(), _angular_distance(), _aspect_strength(), _ayana_bala(), calculate_bhav_bala(), calculate_shadbala(), _cheshta_bala(), _dig_bala() (+45 more)

### Community 34 - "Community 34"
Cohesion: 0.04
Nodes (8): Tests for app.panchang_misc -- Miscellaneous Panchang Calculations =============, Year not in SAMVAT_RAJA should still return 10 roles., Planets should follow GRAHA_ORDER starting from the Raja planet., TestAstronomicalData, TestCalculateAllMisc, TestHelpers, TestMantriMandala, TestPanchakaRahita

### Community 35 - "Community 35"
Cohesion: 0.04
Nodes (18): Tests for Ashtottari Dasha Engine, Test the main calculation function., Ardra is ruled by Sun in Ashtottari. First dasha should be Sun., Shatabhisha is ruled by Rahu in Ashtottari., Revati is ruled by Venus in Ashtottari., Each period's end should be the next period's start., First 8 periods should cover the first cycle., With no balance offset (moon_longitude=None), first 8 periods ~ 108 years. (+10 more)

### Community 36 - "Community 36"
Cohesion: 0.04
Nodes (13): Tests for Tara Dasha Engine, Test balance calculation., Test the main calculation function., With no balance offset, first 9 periods should total ~120 years., Verify Tara Dasha constants are correct., Test various nakshatras for robustness., Revati (last nakshatra) should wrap groups correctly., Test Tara group construction from birth nakshatra. (+5 more)

### Community 37 - "Community 37"
Cohesion: 0.06
Nodes (9): Tests for Phaladeepika Adhyaya 20 (Mahadasha-phala) + Adhyaya 21 (Antardashadhya, analyze_antardasha_phala severity and content., End-to-end: get MD + AD narrative for a real birth date., Verify dasha_phala.json is well-formed and complete., analyze_mahadasha_phala strength rules., TestAntardashaPhala, TestDataIntegrity, TestGetCurrentDashaPhala (+1 more)

### Community 38 - "Community 38"
Cohesion: 0.04
Nodes (13): Tests for Moola (Jaimini) Dasha Engine, Test sign strength calculation., Test the main calculation function., Each period should use the correct base years for its sign., Test with various lagna signs to ensure robustness., Verify Moola Dasha constants are correct., Test odd/even sign classification., Test sign sequence generation. (+5 more)

### Community 39 - "Community 39"
Cohesion: 0.09
Nodes (45): analyze_diseases(), _aspects_house(), _aspects_planet(), _detect_accidents_wounds(), _detect_blindness(), _detect_cancer_tumor(), _detect_diabetes(), _detect_epilepsy() (+37 more)

### Community 40 - "Community 40"
Cohesion: 0.09
Nodes (46): analyze_apatya(), _aspects_house(), _assess_prospect(), _build_fifth_house_analysis(), _detect_aputra_yoga(), _detect_bahu_putra_yoga(), _detect_dattaka_yoga(), _detect_delayed_progeny_yoga() (+38 more)

### Community 41 - "Community 41"
Cohesion: 0.06
Nodes (26): _chart_full(), Tests for Ashtakavarga-phala — Phaladeepika Adhyaya 24.  Covers applied predicti, achieved flag must agree with total_bindus vs threshold., Sanity — Cancer-lagna chart yields a different score than Aries., A complete 7-classical-planet chart with Ascendant., Planet strength must use the planet's own BAV bindus in its transit sign., test_analyze_has_12_house_entries(), test_analyze_has_7_classical_planets_no_rahu_ketu() (+18 more)

### Community 42 - "Community 42"
Cohesion: 0.06
Nodes (38): build_full_report(), _build_planets_in_houses(), _compound_relation(), _display(), _draw_north_indian_chart(), _find_hindi_font(), _fmt_date(), _fmt_num() (+30 more)

### Community 43 - "Community 43"
Cohesion: 0.05
Nodes (15): _has_devanagari(), Tests for LK DB seeding — validates data integrity of seed constants.  RED → imp, Each row must be a 6-tuple: (planet, house, nishani_hi, nishani_en, category, se, First 10 rows must have Devanagari in nishani_text., All rows must have Devanagari in nishani_text., nishani_text (Hindi) must not equal nishani_text_en (English)., Return True if text contains at least one Devanagari character (U+0900–U+097F)., interpretation_hi must contain Devanagari characters. (+7 more)

### Community 44 - "Community 44"
Cohesion: 0.05
Nodes (43): _assess_remedy_accessibility(), _calculate_d10(), _calculate_d108(), calculate_d108_analysis(), _calculate_d12(), _calculate_d2(), _calculate_d3(), _calculate_d30() (+35 more)

### Community 45 - "Community 45"
Cohesion: 0.12
Nodes (43): amsayu(), apply_haranas(), _aspects_house(), _aspects_planet(), calculate_lifespan(), check_balarishta(), classify_ayu(), _house_of() (+35 more)

### Community 46 - "Community 46"
Cohesion: 0.05
Nodes (15): Tests for app.panchang_engine -- Vedic Panchang Calculator., Test Rahu Kaal calculation., Monday Rahu Kaal: slot 2 of 8 (equal day)., Validate TITHIS constant data., Sunday Rahu Kaal: slot 8 of 8., Rahu Kaal must be between sunrise and sunset., Test Choghadiya calculation., First period starts at sunrise, last ends at sunset. (+7 more)

### Community 47 - "Community 47"
Cohesion: 0.05
Nodes (18): Tests for Birth Time Rectification Engine.  Covers:   - Event signature lookup, Completely mismatched dasha/transit should score near zero., Score should never exceed 100 or go below 0., Only mahadasha lord matches, nothing else., Mars MD + Rahu AD for accident should score well., Tests for _get_event_signatures()., Integration tests for the main rectification function., Midnight-crossing windows (e.g. 23:00→01:00) should now work         by wrapping (+10 more)

### Community 48 - "Community 48"
Cohesion: 0.05
Nodes (15): Tests for Pinnacle Numbers, Challenge Numbers, and Life Cycles in numerology_eng, When month and day reduce to same digit, c1 = 0., Pinnacle number calculation for DOB 1990-05-15.      month = reduce(5)  = 5, Life cycles for DOB 1990-05-15.      month_cycle = reduce(5)  = 5  (Early Life), Age ~36 in 2026 → Middle Life cycle., Each pinnacle in the result should have its prediction attached., For DOB 1990-05-15, in 2026 age ~35/36 → second pinnacle (33-42)., Pinnacle 1 for 1990-05-15 should be 11 (not reduced to 2). (+7 more)

### Community 49 - "Community 49"
Cohesion: 0.05
Nodes (11): Smoke tests for critical engine modules: varshphal, transit, astro_iogita, dasha, Smoke tests for transit_engine.py., Smoke tests for astro_iogita_engine.py., Smoke tests for dasha_engine.py., Design change: dasha now covers 2 full 120-year cycles = 240 years total., When moon_longitude is given, first dasha balance is partial.          Design ch, Smoke tests for varshphal_engine.py., TestAstroIogitaEngine (+3 more)

### Community 50 - "Community 50"
Cohesion: 0.13
Nodes (38): analyze_stri_jataka(), _ascendant_sign(), _aspects_house(), _aspects_planet(), _detect_bhartri_sukha(), _detect_pativrata(), _detect_punarbhu(), _detect_putravati() (+30 more)

### Community 51 - "Community 51"
Cohesion: 0.08
Nodes (32): _p(), Tests for expanded yoga library — Phaladeepika Adh. 6-7.  Covers declarative rul, detect_yogas_in_chart should merge legacy + declarative detections., Combined legacy + declarative yoga names should exceed 60., Search engine should have resolved all declarative yoga names., test_amala_benefic_in_10(), test_category_filter(), test_existing_yoga_detection_still_works() (+24 more)

### Community 52 - "Community 52"
Cohesion: 0.05
Nodes (9): Tests for Lagna profile + Moon-Nakshatra predictions — Phaladeepika Adh. 9 + 10., Within Ashwini (0..13.333°), padas 1→4 step every 3.333°., When only sign + sign_degree are present, reconstruct longitude., EN and HI must both be non-empty and differ (basic bilingual check)., EN/HI list lengths must match for lists; strengths/vulns/career non-empty., test_analyze_moon_nakshatra_pada_progression(), test_analyze_moon_nakshatra_reconstruct_from_sign_and_sign_degree(), test_every_lagna_entry_is_bilingual() (+1 more)

### Community 53 - "Community 53"
Cohesion: 0.09
Nodes (37): _aspects_house(), _aspects_planet(), _detect_bhrugukachcha(), _detect_charaka(), _detect_paramahamsa(), detect_pravrajya(), _detect_sannyasi(), _detect_tridandi() (+29 more)

### Community 54 - "Community 54"
Cohesion: 0.08
Nodes (37): _analyze_houses(), _angular_distance(), _build_summary(), calculate_eclipses(), calculate_ingress(), calculate_mundane_analysis(), _conflict_indicators(), _current_transits_in_country_chart() (+29 more)

### Community 55 - "Community 55"
Cohesion: 0.09
Nodes (37): analyze_antardasha_phala(), analyze_mahadasha_phala(), _assess_planet_strength(), _build_antardasha_periods(), _build_prana_periods(), _build_pratyantar_periods(), _build_sookshma_periods(), calculate_dasha() (+29 more)

### Community 56 - "Community 56"
Cohesion: 0.09
Nodes (37): _approx_ascendant(), _approx_ayanamsa(), _approx_moon_longitude(), _approx_planet_longitude(), _approx_rahu_longitude(), _approx_sun_longitude(), _build_status(), _calculate_fallback() (+29 more)

### Community 57 - "Community 57"
Cohesion: 0.09
Nodes (28): _natal(), Tests for Gochara Vedhas + Lattas — Phaladeepika Adh. 26., For each (planet, good_house, vedha_house) entry, verify cancellation fires., Sun and Moon don't vedha each other (Adh. 26 sloka 33)., Moon and Saturn don't vedha each other., If transit is not in a good house, vedha doesn't apply (no cancellation)., Multiple planets in the vedha house — still just one cancellation (first found)., Sun's prishta distance = 12. If natal Moon in Ashwini (1st nak) and Sun transits (+20 more)

### Community 58 - "Community 58"
Cohesion: 0.06
Nodes (36): calculate_achanak_chot(), calculate_bunyaad(), calculate_dhoka(), calculate_enemy_presence(), calculate_hora_lord(), calculate_karmic_debts(), calculate_karmic_debts_with_hora(), calculate_kayam_grah() (+28 more)

### Community 59 - "Community 59"
Cohesion: 0.08
Nodes (20): calcLifePath(), calcPersonalDay(), formatTime12(), formatTime24(), generateObservancesFromDay(), getLocalDateString(), handleNumeroSubmit(), hasMeaningfulSections() (+12 more)

### Community 60 - "Community 60"
Cohesion: 0.05
Nodes (16): Tests for app.kp_engine -- Krishnamurti Paddhati Engine., Validate Vimshottari Dasha constants., Validate the pre-built KP sub-lord table., Must have 27 nakshatras * 9 subs = 243 entries., First entry starts at 0, last entry ends at ~360., Each entry's end should equal the next entry's start., First nakshatra (Ashwini) lord is Ketu., Ashwini's first sub = its own lord (Ketu). (+8 more)

### Community 61 - "Community 61"
Cohesion: 0.08
Nodes (35): analyze_ashtakvarga_phala(), analyze_horasara_phala(), _apply_ekadhipatya_shodhana(), _apply_trikona_shodhana(), _bav_bindu_level(), calculate_ashtakvarga(), _calculate_shodhya_pinda(), _combo_effect() (+27 more)

### Community 62 - "Community 62"
Cohesion: 0.1
Nodes (27): get_db(), _get_pool(), _get_valid_conn(), init_db(), PgConnection, Database initialization and connection management for PostgreSQL., Wrapper around psycopg2 connection to provide sqlite3-like execute API., Initialize PostgreSQL database with schema. Creates all tables. (+19 more)

### Community 63 - "Community 63"
Cohesion: 0.09
Nodes (35): analyze_entrance(), analyze_home_layout(), _build_entrance_result(), _build_room_remedies(), calculate_mandala(), _calculate_vastu_score(), _degrees_to_direction(), _direction_to_pada_index() (+27 more)

### Community 64 - "Community 64"
Cohesion: 0.07
Nodes (19): _p(), Tests for Vritti (Livelihood / Career) — Phaladeepika Adhyaya 5., Aries ascendant → 10th sign = Capricorn → lord Saturn., Leo ascendant → 10th sign = Taurus → lord Venus., Sun exalted in Aries (1st), Moon debilitated in Scorpio (8th)., Aries ascendant → 10th sign Capricorn → 10th lord Saturn.     Put Saturn at a lo, Leo ascendant → 10th sign Taurus → 10th lord Venus.     Place Venus in the 9th h, test_all_primary_vocation_fields_present() (+11 more)

### Community 65 - "Community 65"
Cohesion: 0.12
Nodes (34): analyze_bhava_vichara(), _analyze_karaka_as_lagna(), _asc_sign(), _aspects_on_house(), _assess_bhava(), _bhava_karakas(), _house_lord(), _house_sign() (+26 more)

### Community 66 - "Community 66"
Cohesion: 0.08
Nodes (33): _approximate_placidus_cusps(), _build_kp_horary_table(), _build_kp_sub_lords(), calculate_kp_cuspal(), calculate_kp_horary(), _degree_to_dms(), _find_house_for_planet(), _find_vimshottari_index() (+25 more)

### Community 67 - "Community 67"
Cohesion: 0.07
Nodes (13): _planet_by_name(), planets(), test_planetary_enhanced.py -- Tests for enhanced planetary position fields =====, Ensure the enhancement did not break existing fields., Calculate planetary positions once for all tests., Get a planet dict by name., TestAllPlanetsPresent, TestCombustion (+5 more)

### Community 68 - "Community 68"
Cohesion: 0.08
Nodes (19): _handcrafted_chart(), _p(), Tests for Bhava Phala + Bhava-misra-phala — Phaladeepika Adh. 8 + 16., Aries Lagna; Jupiter in 5th (Leo) aspects Lagna (9th aspect); Lagna lord     Mar, 4th house weak: Saturn (malefic) in 4th, Moon (Lagna-lord-ish context)     with, Empty 11th house, Jupiter (Aquarius→lord Saturn) in neutral position., Tanu, Dhana, Sahaja, Sukha, Putra, Ari, Yuvati, Randhra, Bhagya, Karma, Labha, V, A full chart for testing: Aries ascendant, standard planet placements. (+11 more)

### Community 69 - "Community 69"
Cohesion: 0.11
Nodes (25): _aries_chart(), _p(), Tests for Bhava-phala-vichara — Phaladeepika Adhyaya 15., Aries Lagna: 4th=Cancer → Moon. Place Moon in 6th → lord in dusthana → destructi, Malefics Sun + Saturn + Mars aspecting the same house with no benefic support., Karaka of 9th = Jupiter. Place Jupiter combust (within 10° of Sun) AND afflicted, Aries Lagna; lord Mars exalted (Capricorn) in 10th (Kendra) → Lagna flourishes., Jupiter in 5th (own-ish territory); 5th lord absent. Benefic occupant → flourish (+17 more)

### Community 70 - "Community 70"
Cohesion: 0.13
Nodes (29): _all_narrative_text(), _aries_chart(), _p(), Tests for Nidhana-phala — Phaladeepika Adhyaya 17.  Important: Adh. 17 is about, Ensures narrative uses philosophical language and disclaimers., Empty chart with no ascendant → neither strong nor weak indicators., test_disclaimer_phrase_in_hi_narrative(), test_eighth_house_analysis_fields() (+21 more)

### Community 71 - "Community 71"
Cohesion: 0.09
Nodes (31): calculate_ascendant_for_location(), calculate_astro_map(), calculate_houses_for_location(), _degree_in_sign(), _detect_planetary_lines(), _dusthana_label(), get_planet_house(), _gmst_hours() (+23 more)

### Community 72 - "Community 72"
Cohesion: 0.2
Nodes (31): hr(), main(), pick(), Full Lal Kitab verification tables for a given chart.  This file is a READ-ONLY, Safe-render for bilingual {en, hi} objects., sub(), table_active_passive_rin(), table_aspects() (+23 more)

### Community 73 - "Community 73"
Cohesion: 0.13
Nodes (30): calculate_argala(), calculate_chara_dasha(), calculate_chara_karakas(), calculate_indu_lagna(), calculate_jaimini(), calculate_jaimini_drishti(), calculate_jaimini_yogas(), calculate_longevity() (+22 more)

### Community 74 - "Community 74"
Cohesion: 0.11
Nodes (30): analyze_vritti(), _ascendant_sign(), _build_geographic_affinities(), _dignity_score(), _empty_result(), _house_score(), load_vritti_data(), _lord_of_tenth() (+22 more)

### Community 75 - "Community 75"
Cohesion: 0.11
Nodes (24): _mkplanet(), Tests for Stri-Jataka (women's horoscope) analysis — Phaladeepika Adh. 11., test_bhartri_sukha_detected(), test_gender_male_returns_not_applicable(), test_minimal_chart_no_crash(), test_pativrata_detected(), test_pativrata_rejected_malefic_in_7th(), test_prospect_favorable_with_positive_yogas() (+16 more)

### Community 76 - "Community 76"
Cohesion: 0.14
Nodes (29): analyze_longevity_indicators(), _asc_sign(), _eighth_house_section(), _int_house(), _is_debilitated(), _is_exalted(), _is_own(), _karmic_transitions_narrative() (+21 more)

### Community 77 - "Community 77"
Cohesion: 0.09
Nodes (29): _build_cell_lookup(), _build_sbc_grid(), _build_summary(), calculate_sarvatobhadra(), get_empty_grid(), get_nakshatra_positions(), get_sign_positions(), get_vedha_targets() (+21 more)

### Community 78 - "Community 78"
Cohesion: 0.07
Nodes (11): Tests for Lal Kitab house-based remedies engine., Old code expects 'remedies' key (list) — must still work., Strong planet: remedies list empty (backward compat), has_remedy False., Sun in H1 (Aries) vs Sun in H7 (Libra) should have different en remedies., Verify Aries=H1, Cancer=H4, Libra=H7, Capricorn=H10., Hindi text must contain Devanagari characters (U+0900-U+097F)., Must have at least 9 planets × 12 houses = 108 entries., Each returned planet entry must have lk_house, remedy dict, has_remedy. (+3 more)

### Community 79 - "Community 79"
Cohesion: 0.11
Nodes (19): _p(), Tests for 45 two-planet conjunctions — Phaladeepika Adh. 18., 9 base planets + Lagna → C(9,2)=36 planet-planet + 9 planet-Lagna = 45., test_all_major_pairs_recognizable(), test_conjunct_planets_within_orb(), test_conjunction_picks_up_budhaditya_special_yoga(), test_custom_orb(), test_data_includes_all_planet_planet_pairs() (+11 more)

### Community 80 - "Community 80"
Cohesion: 0.07
Nodes (11): Tests for P0 safety blocks in muhurat_finder.  P0 items tested:   1. Vyatipata Y, P0-3 / P0-4: Mrityu Yoga and Visha Yoga blocks., P0-6: Ganda Lagna / Sandhi Lagna warning., Integration tests for the full finder with P0 blocks active., P0-5: Sankranti 16-hour restriction., P0-1 / P0-2: Vyatipata (#17) and Vaidhriti (#27) hard blocks., TestMuhuratFinderIntegration, TestP0LagnaWarnings (+3 more)

### Community 81 - "Community 81"
Cohesion: 0.14
Nodes (26): add_fruition_timing(), _all_in(), _asc_sign(), detect_all_yogas(), detect_yogas_with_timing(), evaluate_rule(), _extract_yoga_planets(), _house_of() (+18 more)

### Community 82 - "Community 82"
Cohesion: 0.07
Nodes (6): Tests for muhurat_rules.py, TestActivityMetadata, TestCheckDayFavorable, TestHelpers, TestNormalizeTithi, TestRules

### Community 83 - "Community 83"
Cohesion: 0.13
Nodes (19): _mkplanet(), Tests for Apatya (progeny) analysis — Phaladeepika Adhyaya 12., test_aputra_yoga_detected(), test_bahu_putra_yoga_detected(), test_bilingual_fields_present(), test_dattaka_yoga_detected(), test_delayed_progeny_yoga_lord_in_saturn_sign(), test_delayed_progeny_yoga_saturn_in_5() (+11 more)

### Community 84 - "Community 84"
Cohesion: 0.14
Nodes (19): _p(), Tests for Classical Roga (disease) Phalam — Phaladeepika Adh. 14., test_blindness_cancelled_by_jupiter(), test_blindness_detected(), test_body_parts_populated(), test_diabetes_jupiter_in_6(), test_diabetes_venus_saturn_in_6(), test_epilepsy_detected() (+11 more)

### Community 85 - "Community 85"
Cohesion: 0.13
Nodes (18): _p(), Tests for 3-method Ayurdaya — Phaladeepika Adh. 22., test_amsayu_returns_contract(), test_apply_haranas_no_reduction_when_clean(), test_astangata_harana_for_combust(), test_calculate_lifespan_full_chart(), test_calculate_lifespan_gandhi_range(), test_haranas_floor_at_zero() (+10 more)

### Community 86 - "Community 86"
Cohesion: 0.12
Nodes (23): _add_years(), _assign_deha_jeeva(), _build_sign_sequence(), _calculate_balance(), calculate_kalachakra_dasha(), _enrich_period(), _find_deha_jeeva_rashis(), _is_savya() (+15 more)

### Community 87 - "Community 87"
Cohesion: 0.13
Nodes (23): calculate_all_special_yogas(), calculate_amrit_siddhi(), calculate_dagdha_nakshatra(), calculate_dwipushkar(), calculate_ganda_moola(), calculate_ravi_yoga(), calculate_sarvartha_siddhi(), calculate_siddhi_yoga() (+15 more)

### Community 88 - "Community 88"
Cohesion: 0.12
Nodes (23): _classify_house(), derive_compatible_sign(), derive_donts(), derive_dos(), derive_gemstone(), derive_lucky_color(), derive_lucky_number(), derive_lucky_time() (+15 more)

### Community 89 - "Community 89"
Cohesion: 0.09
Nodes (22): calculate_gun_milan(), _normalize_nakshatra(), _rashi_lord(), matching_engine.py — Kundli Gun Milan (Ashtakoota) Matching Engine =============, Varna koot: groom's varna should be >= bride's. Max 1 point., Vasya koot: mutual influence/attraction based on Moon rashi. Max 2 points., Tara koot: based on nakshatra distance (bidirectional). Max 3 points.     Standa, Yoni koot: sexual/physical compatibility. Max 4 points.     Same=4, Friendly=3, (+14 more)

### Community 90 - "Community 90"
Cohesion: 0.09
Nodes (22): calculate_baladi(), calculate_deeptadi(), calculate_jagradadi(), calculate_shyanadi(), _fetch_chart(), get_dasha_interpretation(), get_full_interpretations(), get_lagna_interpretation() (+14 more)

### Community 91 - "Community 91"
Cohesion: 0.11
Nodes (21): _build_ai_horoscope_prompt(), generate_ai_horoscope(), generate_daily_horoscopes(), _generate_template_horoscope(), _get_current_transits(), _get_current_transits_full(), _parse_ai_sections(), H-09: Horoscope Content Generation Pipeline — seeds daily & weekly horoscopes. (+13 more)

### Community 92 - "Community 92"
Cohesion: 0.18
Nodes (18): a(), at(), be(), e(), Ee(), Fe(), Le(), o() (+10 more)

### Community 93 - "Community 93"
Cohesion: 0.16
Nodes (16): _mkplanet(), Tests for Pravrajya (ascetic) yogas — Phaladeepika Adh. 27., test_bhrugukachcha_detected(), test_bhrugukachcha_rejected_when_one_not_in_kendra(), test_charaka_detected(), test_missing_ascendant(), test_missing_planets(), test_normal_chart_no_yogas() (+8 more)

### Community 94 - "Community 94"
Cohesion: 0.1
Nodes (10): Tests for Ekadashi Parana calculation., When next tithi is Dwadashi and it ends before window closes, note it., Parana window must start at or after sunrise., If Dwadashi starts after sunrise, parana waits for Dwadashi., Parana end must be within ~4 hours of sunrise., Core behaviour: returns dict for Ekadashi, None otherwise., All required fields must be present and correct., TestEkadashiParanaBasic (+2 more)

### Community 95 - "Community 95"
Cohesion: 0.15
Nodes (18): build_prediction_studio(), _build_specific_text(), compute_area_score(), compute_area_score_with_evidence(), _dignity_phrase(), _dignity_phrase_hi(), _house_strength(), _navamsa_dignity_adjustment() (+10 more)

### Community 96 - "Community 96"
Cohesion: 0.15
Nodes (19): _build_explanation(), calculate_rectification(), _get_dasha_at_date(), _get_event_signatures(), _get_house_lord(), _get_planets_in_house(), _get_transit_at_date(), _ordinal() (+11 more)

### Community 97 - "Community 97"
Cohesion: 0.14
Nodes (19): _atom(), build_atom_vector(), _generate_iogita_insight(), _generate_normal_insights(), _get_dignity_label(), get_planet_strength(), identify_basin(), _print_report() (+11 more)

### Community 98 - "Community 98"
Cohesion: 0.14
Nodes (19): calculate_avakhada(), _calculate_ghatak(), _compute_good_years(), _get_gana(), _get_nadi(), _get_nakshatra_index(), _get_nakshatra_lord(), _get_pada() (+11 more)

### Community 99 - "Community 99"
Cohesion: 0.15
Nodes (19): analyze_janma_predictions(), analyze_lagna_profile(), analyze_moon_nakshatra(), _combined_narrative_en(), _combined_narrative_hi(), _extract_moon_longitude(), get_nakshatra_index(), get_pada() (+11 more)

### Community 100 - "Community 100"
Cohesion: 0.18
Nodes (19): get_all_signs_horoscope(), get_daily_horoscope(), get_monthly_horoscope(), get_transit_insights(), get_weekly_horoscope(), get_yearly_horoscope(), _has_meaningful_sections(), _parse_content_to_sections() (+11 more)

### Community 101 - "Community 101"
Cohesion: 0.13
Nodes (9): backendToDrikNum(), enrichDayFestivals(), fetchMonthly(), generateObservances(), getLocalDateString(), getTithiNumber(), normalizeFestivalDetail(), normalizeFestivalName() (+1 more)

### Community 102 - "Community 102"
Cohesion: 0.17
Nodes (18): analyze_family_timing(), _build_indicator(), _house_lord(), _house_sign(), _house_sign_hi(), _make_summary(), _natal_sign(), family_timing_engine.py — Cross-Chart Family Timing Analysis =================== (+10 more)

### Community 103 - "Community 103"
Cohesion: 0.13
Nodes (15): BaseHTTPMiddleware, _extract_user_id(), get_traffic_snapshot(), H-01: Structured Logging Middleware — logs every request with method, path, stat, Extract user_id from JWT Bearer token if present., Middleware that logs every HTTP request and records to the live traffic buffer., Return a snapshot of recent traffic for the live admin dashboard.     Thread-saf, RequestLoggingMiddleware (+7 more)

### Community 104 - "Community 104"
Cohesion: 0.11
Nodes (9): Tests for enhanced Choghadiya — Vaar Vela, Kaal Vela, Kaal Ratri flags., Ensure Vaar Vela / Kaal Vela / Kaal Ratri additions don't break existing fields., Exactly ONE day period must have vaar_vela=True for each weekday., Exactly ONE day period must have kaal_vela=True for each weekday., Exactly ONE night period must have kaal_ratri=True for each weekday., TestExistingFieldsPreserved, TestKaalRatri, TestKaalVela (+1 more)

### Community 105 - "Community 105"
Cohesion: 0.16
Nodes (17): apply_lattas(), apply_vedhas(), enrich_transits(), _house_from_moon(), _is_exception_pair(), load_latta_table(), load_vedha_table(), _nakshatra_distance() (+9 more)

### Community 106 - "Community 106"
Cohesion: 0.2
Nodes (17): calculate_forecast(), calculate_personal_day(), calculate_personal_month(), calculate_personal_year(), calculate_universal_day(), calculate_universal_month(), calculate_universal_year(), _digit_sum() (+9 more)

### Community 107 - "Community 107"
Cohesion: 0.15
Nodes (17): calculate_all_misc(), calculate_astronomical_data(), calculate_chaturmasa(), calculate_mantri_mandala(), calculate_panchaka_rahita(), _minutes_to_time(), panchang_misc.py -- Miscellaneous Panchang Calculations ========================, Compute astronomical epoch values for a Gregorian date string (YYYY-MM-DD). (+9 more)

### Community 108 - "Community 108"
Cohesion: 0.16
Nodes (17): cleanup_old_uploads(), ensure_upload_dir(), map_room_placements(), _optimize_image(), pixel_to_direction(), vastu/floorplan.py — Floor Plan Upload & Pixel-to-Direction Mapper =============, Resize large images and compress to JPEG for storage efficiency.     Returns opt, Validate, optimize, and save uploaded floor plan image.      Returns:         di (+9 more)

### Community 109 - "Community 109"
Cohesion: 0.11
Nodes (17): farmaan_annotate(), farmaan_detail(), farmaan_search(), Lal Kitab Farmaan routes — P2.1 + P2.7 + P2.8 (MVP).  Implements the thin API la, Contribute a transliteration / translation / commentary / dispute., List every edition present in the corpus with row counts., P2 edition comparison: return all editions' versions of the same section., Search the raw source library across editions / languages / rights bands. (+9 more)

### Community 110 - "Community 110"
Cohesion: 0.11
Nodes (17): Tests for numerology_engine.py — Pythagorean numerology calculations., Verify master number 11 is preserved (not reduced to 2)., Destiny number (formerly expression) uses all letters of the name., Soul urge uses only vowels (A, E, I, O, U)., Personality uses only consonants., Verify all required keys are present in the output dict., Life path for 1990-01-15: 1+9+9+0=19->10->1 + 0+1=1 + 1+5=6 => 1+1+6=8., Master numbers 11, 22, 33 should not be reduced further. (+9 more)

### Community 111 - "Community 111"
Cohesion: 0.17
Nodes (15): detect_yogas_in_chart(), get_kundli_yoga_profile(), get_yoga_statistics(), _normalise_query(), yoga_search_engine.py — Yoga Search Across Kundli Database =====================, Run full yoga detection on a parsed chart_data dict.      Merges legacy dosha_en, Given chart_data (planets dict from DB), detect which yogas are present.     Use, Search all kundlis owned by *user_id* for a specific yoga.      Args:         db (+7 more)

### Community 112 - "Community 112"
Cohesion: 0.17
Nodes (15): calculate_agnivasa(), calculate_all_nivas(), calculate_chandra_vasa(), calculate_homahuti(), calculate_kumbha_chakra(), calculate_rahu_vasa(), calculate_shivavasa(), panchang_nivas.py -- Nivas, Shool, Homahuti & Kumbha Chakra Calculations ======= (+7 more)

### Community 113 - "Community 113"
Cohesion: 0.17
Nodes (15): calculate_mudda_dasha(), calculate_muntha(), calculate_varshphal(), calculate_year_lord(), find_solar_return_jd(), _jd_to_datetime(), varshphal_engine.py — Vedic Varshphal (Solar Return / Tajaka) Engine ===========, Muntha advances one sign per year from natal ascendant.     Returns: {sign, sign (+7 more)

### Community 114 - "Community 114"
Cohesion: 0.2
Nodes (15): analyze_bhava_phala(), _house(), _house_strength(), _is_strong_planet(), _is_weak_planet(), load_bhava_phala_data(), _planet_aspects_house(), bhava_phala_engine.py — Classical Bhava Phala + Bhava-misra-phala ============== (+7 more)

### Community 115 - "Community 115"
Cohesion: 0.19
Nodes (15): _build_sub_periods(), calculate_moola_dasha(), _get_dasha_sign_sequence(), _get_effective_years(), _is_odd_sign(), _parse_date(), moola_dasha_engine.py — Moola (Jaimini) Dasha Calculation Engine ===============, Get the 12-sign sequence for Moola Dasha starting from the given sign.      For (+7 more)

### Community 116 - "Community 116"
Cohesion: 0.13
Nodes (13): _bootstrap_db(), client(), _create_kundli(), db(), _make_admin(), _make_astrologer(), Shared test fixtures — temp DB, TestClient, auth helpers.  Every test module get, Insert a minimal kundli record and return its id. (+5 more)

### Community 117 - "Community 117"
Cohesion: 0.21
Nodes (12): _p(), Tests for Balarishta & Ayu classification — Phaladeepika Adh. 13., test_alpayu_malefic_lagna_no_benefic(), test_ayu_return_contract(), test_balarishta_cancelled_by_strong_jupiter(), test_balarishta_moon_in_dusthana_aspected_by_mars(), test_balarishta_return_contract(), test_balarishta_sun_in_8th_moon_in_6th() (+4 more)

### Community 118 - "Community 118"
Cohesion: 0.2
Nodes (14): _add_lagna_warnings(), find_muhurat_dates(), _find_sankranti_times(), find_travel_muhurat(), _is_sankranti_restricted(), _normalize_direction(), Muhurat Finder Engine — finds auspicious dates for specific activities.  Classic, Find auspicious dates for an activity in a given month.      Optional birth_moon (+6 more)

### Community 119 - "Community 119"
Cohesion: 0.19
Nodes (14): calculate_chalti_gaadi(), calculate_dhur_dhur_aage(), calculate_muththi(), calculate_soya_ghar(), classify_all_planet_statuses(), _get_strongest_planet(), lalkitab_technical.py — Advanced Lal Kitab Technical Logic =====================, Planet in house N-1 pushes planet in house N.     House 12 pushes house 1 (circu (+6 more)

### Community 120 - "Community 120"
Cohesion: 0.29
Nodes (11): aa(), c(), d(), ea(), h(), J(), L(), Q() (+3 more)

### Community 121 - "Community 121"
Cohesion: 0.13
Nodes (3): TDD tests for LK Saala Grah Dasha engine., TestDashaTimeline, TestSaalaGrah

### Community 122 - "Community 122"
Cohesion: 0.21
Nodes (13): _build_antardasha_periods(), _build_pratyantar_periods(), calculate_ashtottari_dasha(), _calculate_balance(), _get_dasha_sequence(), _parse_date(), ashtottari_dasha_engine.py — Ashtottari Dasha Calculation Engine ===============, Return the 8-planet dasha sequence starting from a given lord. (+5 more)

### Community 123 - "Community 123"
Cohesion: 0.22
Nodes (13): analyze_navamsha_profession(), _d9_sign_for_all(), _d9_tenth_house(), _find_planet_in_d9(), _navamsha_sign_for_longitude(), navamsha_profession_engine.py — Profession from 10th Navamsha Lord =============, Return 0-indexed sign position, -1 if unknown., Compute the Navamsha (D9) sign for a planet's sidereal longitude.      Partition (+5 more)

### Community 124 - "Community 124"
Cohesion: 0.21
Nodes (13): analyze_panchadha_maitri(), _build_effect(), _house_distance(), _natural_relation(), _panchadha(), panchadha_maitri_engine.py — Panchadha Maitri (5-fold Planetary Friendship) ====, Return (panchadha_en, panchadha_hi) for a given natural+temporary pair., Build English and Hindi effect strings for the pair. (+5 more)

### Community 125 - "Community 125"
Cohesion: 0.2
Nodes (13): calculate_all_samvat(), check_lagna_pushkara(), get_brihaspati_samvatsara(), get_gujarati_samvat(), get_month_systems(), is_pushkara_navamsha(), panchang_samvat.py -- Samvat Systems & Pushkara Navamsha =======================, Return both Purnimant and Amant month names for the given lunar month and paksha (+5 more)

### Community 126 - "Community 126"
Cohesion: 0.18
Nodes (13): _is_auspicious_day(), list_activities(), _monthly_days(), muhurat_find(), muhurat_finder(), muhurat_monthly(), Muhurat Finder API — activity-specific auspicious date finder + compatibility ro, Find auspicious dates for a specific activity in a given month.      Uses tradit (+5 more)

### Community 127 - "Community 127"
Cohesion: 0.21
Nodes (13): _binary_search_station(), calculate_retrograde_stations(), _get_longitude(), _get_speed(), _jd_to_date(), _jd_to_datetime(), retrograde_engine.py — Planetary Retrograde Station Calculator =================, Convert Julian Day to YYYY-MM-DD string. (+5 more)

### Community 128 - "Community 128"
Cohesion: 0.2
Nodes (13): auto_detect_rooms(), _detect_ocr_labels(), _detect_opencv(), _detect_yolo(), _match_room(), _preprocess_for_ocr(), vastu/auto_detect.py — AI Room Detection for Floor Plans =======================, Preprocess floor plan for OCR: grayscale → upscale 2x → sharpen → binarize. (+5 more)

### Community 129 - "Community 129"
Cohesion: 0.14
Nodes (13): Tests for lalkitab_engine.py — Lal Kitab remedies engine., Each planet should have 5-8 remedies., A debilitated planet (strength < 0.5) should receive remedies., An exalted planet (strength >= 0.5) should NOT receive remedies., A planet in enemy sign (strength 0.35 < 0.5) should receive remedies., Verify the output dict structure for each planet., REMEDIES dict must cover all 9 Vedic planets., test_enemy_planet_gets_remedies() (+5 more)

### Community 130 - "Community 130"
Cohesion: 0.14
Nodes (13): Correctness smoke tests for Lal Kitab — validate that real calculations produce, When chart_data is provided, the per-planet result must include afflictions., Sun in Aries should be Exalted, not something else., A planet in its own sign but combust should score lower than non-combust., Even an exalted planet in 8th house should have affliction noted., calculate_age_milestones must raise on empty / malformed birth_date., After fix, remedy.hi should be real Devanagari Hindi (not duplicated English)., test_detailed_strength_penalizes_combustion() (+5 more)

### Community 131 - "Community 131"
Cohesion: 0.18
Nodes (12): calculate_aspects(), calculate_cusp_aspects(), calculate_western_aspects(), _get_aspected_houses(), _match_western_aspect(), aspects_engine.py -- Vedic Planetary Aspects Calculator ========================, Calculate degree-based Western aspects between all planet pairs.      Returns a, Find the Western aspect matching a given degree difference, if any. (+4 more)

### Community 132 - "Community 132"
Cohesion: 0.23
Nodes (12): _build_pair_index(), _degree_separation(), detect_conjunctions(), _house(), load_conjunction_data(), _longitude(), conjunction_engine.py — Pair-wise Planetary Conjunctions =======================, Return list of detected conjunctions.      Each entry:     {         "planets": (+4 more)

### Community 133 - "Community 133"
Cohesion: 0.17
Nodes (12): check_day_favorable(), get_activity_info(), get_activity_rules(), get_all_activities(), normalize_tithi_for_rules(), Muhurat rules database for 9 activity-specific muhurats.  Each activity defines, # NOTE: These lists use Python weekday numbering: Monday=0 … Sunday=6., Get activity name, Hindi name, icon, description. (+4 more)

### Community 134 - "Community 134"
Cohesion: 0.22
Nodes (6): assert(), initNECaptchaWithFallback(), isInteger(), loadResource(), normalizeFallbackConfig(), ObjectAssign()

### Community 135 - "Community 135"
Cohesion: 0.26
Nodes (11): add_import(), process_file(), Convert raw <table> elements to use Table primitives.     This is a best-effort, Replace simple caption/label spans with Text component where safe.     Very cons, Add an import line near the top if not already present., Replace simple h3/h4 headings with Heading component where appropriate., remove_font_classes(), replace_colors() (+3 more)

### Community 136 - "Community 136"
Cohesion: 0.23
Nodes (11): calculate_all_directions(), calculate_anandadi_yoga(), calculate_baana(), calculate_disha_shool(), calculate_lucky_indicators(), panchang_directions.py -- Directional & Anandadi Calculations ==================, Return the inauspicious direction (Disha Shool) for a weekday.      Parameters, Return the Baana (elemental arrow direction) for a tithi.      Parameters     -- (+3 more)

### Community 137 - "Community 137"
Cohesion: 0.23
Nodes (11): calculate_varga_strength(), _classify_hold(), _has_dignity_hold(), varga_grading_engine.py -- Phaladeepika Adhyaya 3 (Vargadhyaya) Varga-Strength T, Return (sign_name, sign_index) for a planet at given ecliptic longitude     in t, Return True if the planet is in its own / exalted / moolatrikona /     friendly, Classify the varga-hold category for reporting:     exalted / moolatrikona / own, Return the classical tier definition for a given hold-count (0..7). (+3 more)

### Community 138 - "Community 138"
Cohesion: 0.23
Nodes (11): classification_description(), classification_label(), classify_remedy(), Lal Kitab 1952 remedy classification — P1.11.  Per LK 1952 canon, remedies fall, Human-readable label for UI badges., One-liner explaining what the classification means., In-place: add `classification` + `classification_en` + `classification_hi`     t, Lowercase substring match — safe for both EN and HI. (+3 more)

### Community 139 - "Community 139"
Cohesion: 0.23
Nodes (11): _build_sub_periods(), _build_tara_nakshatras(), _calculate_balance(), calculate_tara_dasha(), _parse_date(), tara_dasha_engine.py — Tara Dasha Calculation Engine ===========================, Build the 9 Tara groups starting from the birth nakshatra.      Each group conta, Build sub-periods (antardasha equivalent) within a Tara main period.      Sub-pe (+3 more)

### Community 140 - "Community 140"
Cohesion: 0.24
Nodes (11): calculate_pindayu(), _compute_modifier(), _is_combust(), _is_debilitated(), _is_exalted(), _is_retrograde(), ashtakavarga_lifespan_engine.py — Pindayu (Ashtakavarga-based Lifespan) ========, Return True if planet is within _COMBUST_ORB degrees of Sun.      Moon is never (+3 more)

### Community 141 - "Community 141"
Cohesion: 0.17
Nodes (11): kundli_yoga_profile(), list_yoga_categories(), list_yoga_types(), Yoga Search routes — search across kundli database for specific yoga combination, Get full yoga profile for a single kundli.      Returns all detected yogas with, Return all searchable yoga types.      No auth required — informational endpoint, Return available categories from the declarative yoga database., Search all stored kundlis for a specific yoga.      Scans every kundli owned by (+3 more)

### Community 142 - "Community 142"
Cohesion: 0.27
Nodes (5): C(), k(), M(), P(), V()

### Community 143 - "Community 143"
Cohesion: 0.22
Nodes (4): createDebouncedFn(), createHead(), setVhUnit(), vhUnitFix()

### Community 144 - "Community 144"
Cohesion: 0.22
Nodes (2): saveJournal(), saveJournalEntry()

### Community 145 - "Community 145"
Cohesion: 0.29
Nodes (9): build_sankranti_payload(), find_sankranti_times(), Sankranti engine — compute Sun ingress times into sidereal rashis.  This module, Build API-friendly sankranti payload with local times + windows., Return sidereal Sun rashi index (0=Mesha…11=Meena) at UTC datetime., Find 12 sankranti ingress instants for the given year (UTC), ordered from Mesha., SankrantiEvent, _sun_rashi_index_sidereal() (+1 more)

### Community 146 - "Community 146"
Cohesion: 0.29
Nodes (8): calculate_family_harmony(), generate_cross_waking_narrative(), get_family_dominant_planet(), lalkitab_family.py — Grah-Gasti: Family Chart Linking ==========================, Cross-chart harmony analysis between two Lal Kitab charts.      Returns: {harmon, Most frequent planet across all family charts — the family's ruling planet., Generate cross-waking narrative between two charts.      A planet in House N wak, _safe_p_map()

### Community 147 - "Community 147"
Cohesion: 0.31
Nodes (9): _canonical_name(), _count_malefics_in_house(), _name_for_cluster(), rank_compound_debts(), Lal Kitab — P2.9 Compound Debt Analysis with Prioritisation ====================, Extract the canonical EN name used for priority lookup.      Debt `name` may be, Match debt to a canon tier. Substring match covers     'Pitru Rin (Father's Debt, Rank a list of enriched karmic debts by LK compound-remedy canon.      Parameter (+1 more)

### Community 148 - "Community 148"
Cohesion: 0.27
Nodes (9): calculate_all_tamil(), calculate_jeevanama(), calculate_netrama(), calculate_tamil_yoga(), panchang_tamil.py -- Tamil Yoga, Jeevanama & Netrama Calculations ==============, Calculate Jeevanama (Moon's life status) based on tithi.      Args:         tith, Calculate Netrama (eye status) based on nakshatra pada.      Args:         naksh, Calculate all Tamil panchang elements at once.      Args:         weekday: 0=Sun (+1 more)

### Community 149 - "Community 149"
Cohesion: 0.27
Nodes (9): database_seed_lalkitab.py — Idempotent seed data for Lal Kitab DB tables.  Table, Idempotent seed of all three Lal Kitab DB tables.     Uses ON CONFLICT DO NOTHIN, Seed nishaniyan_master. Handles both 5-column and 6-column (with nishani_text_en, Seed lal_kitab_debts. DB columns: debt_type, planet, description, indication, re, Seed lk_interpretations table (created by migration if not yet present)., _seed_debts(), seed_lalkitab_tables(), _seed_lk_interpretations() (+1 more)

### Community 150 - "Community 150"
Cohesion: 0.29
Nodes (9): _calc_age(), get_dasha_timeline(), get_saala_grah(), _planet_at_age(), lalkitab_dasha.py — Lal Kitab Saala Grah & 35-Year Dasha System ================, Return the Saala Grah planet name for a given age (1-based)., Return completed years of age (integer floor)., Get the ruling planet (Saala Grah) for a given age.      Args:         current_a (+1 more)

### Community 151 - "Community 151"
Cohesion: 0.2
Nodes (9): get_eclipses(), get_ingress(), get_mundane_analysis(), list_countries(), Mundane Astrology routes — country charts, national analysis, eclipses, ingress., Return the dates when the Sun enters each of the 12 sidereal signs     (Sankrant, Return the list of available country charts for mundane analysis., Full mundane astrology analysis for a country: birth chart, current transits, (+1 more)

### Community 152 - "Community 152"
Cohesion: 0.2
Nodes (3): Tests for bilingual translation constants., All planet names must be Devanagari, not English., test_planet_names_are_hindi()

### Community 153 - "Community 153"
Cohesion: 0.28
Nodes (8): calculate_ekadashi_parana(), _minutes_to_time(), Ekadashi Parana (एकादशी पारण) calculation., Convert 'HH:MM' to minutes from midnight., Calculate Ekadashi Parana (fast-breaking) time.      Parana is done the morning, Convert minutes from midnight to 'HH:MM'., Calculate Ekadashi Parana time.      Parana is done the morning after Ekadashi,, _time_to_minutes()

### Community 154 - "Community 154"
Cohesion: 0.42
Nodes (8): add_import(), cleanup_classnames(), process_file(), remove_font_classes(), replace_colors(), transform_heading(), transform_table(), transform_text_component()

### Community 155 - "Community 155"
Cohesion: 0.31
Nodes (8): _compute_baladi_avastha(), get_lagna_rising_analysis(), get_planet_properties(), _load_data(), planet_properties_engine.py — Phaladeepika Adh. 1–2 Planet Properties ==========, Returns stage-of-life, Baladi Avastha, and guna for each planet in the chart., Returns Shirodaya / Prusthodaya / Ubhaodaya analysis for the Lagna sign.      Ar, Determine Baladi Avastha for a planet at `sign_degree` degrees (0-30)     within

### Community 156 - "Community 156"
Cohesion: 0.22
Nodes (1): RED phase: auth tests.

### Community 157 - "Community 157"
Cohesion: 0.29
Nodes (7): get_all_interpretations_for_chart(), get_lk_house_interpretation(), get_lk_validated_remedies(), lalkitab_interpretations.py — Lal Kitab House-by-House Planet Interpretations ==, Return the full interpretation for a planet in a specific house.      Args:, Return all house interpretations for a given chart's planet positions.      Args, Return all applicable validated remedies based on planet positions.      Args:

### Community 158 - "Community 158"
Cohesion: 0.36
Nodes (7): _get_dignity_label(), get_planet_strength_detailed(), get_remedies(), lalkitab_engine.py — Lal Kitab Remedies Engine =================================, Determine dignity label for a planet in a sign.      NOTE: This is a simplified, Enriched Lal Kitab strength model — accounts for dignity, house,     retrograde,, Get Lal Kitab remedies based on planet × house placement.      Args:         pla

### Community 159 - "Community 159"
Cohesion: 0.29
Nodes (7): list_intents(), _match_reason(), app/lalkitab_remedy_wizard.py  P2.4 — Intent-driven Remedy Wizard.  Transforms a, Public helper — return all intent cards for the first wizard step., Explain WHY this remedy ranks for the intent, in EN + HI, and return     a relev, Main wizard entry point.      Args:         intent:            one of INTENT_PRO, recommend_remedies()

### Community 160 - "Community 160"
Cohesion: 0.32
Nodes (7): compute_chandra_kundali(), detect_chandra_lagna_conflicts(), lalkitab_chandra_kundali.py — Chandra Kundali as an INDEPENDENT LK framework ===, Compare each planet's Chandra reading against its Lagna interpretation and     r, Re-anchor a natal house so Moon's natal house becomes H1., Build the Chandra Kundali as an independent LK predictive framework.      Args:, _shift_to_chandra_house()

### Community 161 - "Community 161"
Cohesion: 0.57
Nodes (7): createClientsViaAPI(), fillBirthForm(), injectAuth(), main(), screenshot(), sleep(), waitForChart()

### Community 162 - "Community 162"
Cohesion: 0.33
Nodes (6): calculate_palm_correlations(), _get_default_interp(), get_palm_zones(), lalkitab_palmistry.py — Samudrik Shastra / Palmistry Integration ===============, Return all palm zones normalized to frontend-expected shape., Correlates palm marks with LK chart placements.      planet_positions: [{"planet

### Community 163 - "Community 163"
Cohesion: 0.43
Nodes (6): are_enemies(), are_friends(), build_relations(), _norm_house(), Lal Kitab Relations Engine (backend)  Purpose: - Compute conjunctions (yuti), as, planet_positions: {"Sun": 1..12, ...}      Returns:       {         "conjunction

### Community 164 - "Community 164"
Cohesion: 0.38
Nodes (6): detect_time_planet(), _dominance(), _pick_time_planet(), lalkitab_time_planet.py — Day + Time (Hora) planet: the non-remediable fate plan, Compute the Day-Lord, Hora-Lord and resulting Time Planet.      Args:         bi, Decide which of {day_lord, hora_lord} is the "Time Planet".      Rules (LK 2.16)

### Community 165 - "Community 165"
Cohesion: 0.38
Nodes (6): _build_interpretation(), calculate_upagrahas(), _compute_house(), Calculate Upagrahas (sub-planets) including Aprakasha Grahas and Kala Velas., Whole-sign house from ecliptic longitude and ascendant longitude., Return (en, hi) interpretation for an upagraha in a given house.

### Community 166 - "Community 166"
Cohesion: 0.38
Nodes (6): detect_chakar_cycle(), _normalize_planet(), _normalize_sign(), lalkitab_chakar.py — 35-Sala vs 36-Sala Chakar auto-determination ==============, Decide whether the native follows the 35-Sala or 36-Sala Chakar.      Args:, Capitalise first letter so 'aries', 'ARIES' and 'Aries' all map.

### Community 167 - "Community 167"
Cohesion: 0.33
Nodes (2): login(), switchToHindi()

### Community 168 - "Community 168"
Cohesion: 0.43
Nodes (6): _mangal(), ok(), _planets(), Regression tests for the Mangal Dosh LK-canon vs Vedic-overlay split (Codex R1-P, Minimal chart where only Mars's house matters for Mangal detection., run()

### Community 169 - "Community 169"
Cohesion: 0.43
Nodes (6): classify(), find_block_starts(), main(), parse_block(), Parse an object-literal block starting at `start_idx` where the next line     op, Locate EN and HI translation block opening lines by heuristic.

### Community 170 - "Community 170"
Cohesion: 0.33
Nodes (5): calculate_age_milestones(), get_seven_year_cycle(), lalkitab_milestones.py — Safar-e-Zindagi (Age Milestone Triggers) ==============, birth_date: "YYYY-MM-DD"     planet_positions: [{"planet": "Saturn", "house": 8}, Returns the active 7-year sub-cycle, adjacent cycles, and ruler quality for curr

### Community 171 - "Community 171"
Cohesion: 0.4
Nodes (5): detect_rahu_ketu_axis(), _find_node_house(), lalkitab_rahu_ketu_axis.py — Rahu-Ketu 1-7 Axis (Shadow Axis) Canonical Rules ==, Find the house of Rahu or Ketu in the planet_positions list.      Matching is ca, Detect the 1-7 Rahu-Ketu axis configuration and emit the canonical     combined

### Community 172 - "Community 172"
Cohesion: 0.33
Nodes (5): _compose_reading(), get_chandra_reading(), lalkitab_chandra_readings.py — Chandra Kundali (Moon-chart) LK interpretations =, Compose a compact Chandra-domain reading from:         planet-emotion-quality  ×, Return the LK Chandra-context reading for a planet in a given Chandra-chart

### Community 173 - "Community 173"
Cohesion: 0.4
Nodes (5): calculate_sodashvarga(), _get_dignity(), sodashvarga_engine.py -- Sodashvarga (16 Divisional Charts) Summary & Vimshopak, Determine the dignity of a planet in a given sign., Calculate Sodashvarga for all planets.      Args:         planet_longitudes: {pl

### Community 174 - "Community 174"
Cohesion: 0.33
Nodes (5): get_vastu_diagnosis(), get_vastu_house_for_direction(), lalkitab_vastu.py — Makaan (Vastu) Directional Mapping =========================, Generate Vastu home layout diagnosis from Lal Kitab planet positions.      Retur, Reverse lookup: direction string → house number.

### Community 175 - "Community 175"
Cohesion: 0.33
Nodes (5): get_remedy_matrix(), list_supported_planets(), app/lalkitab_remedy_matrix.py  P2.11 — Direction + Colour + Material remedy matr, Return the frozen direction/colour/material matrix for a planet.      Args:, Convenience: enumerate planets with a full matrix entry.

### Community 176 - "Community 176"
Cohesion: 0.47
Nodes (5): ai_interpret(), _compose_interpretation(), _normalize_period(), AI interpretation routes for kundli predictions., Return AI-style period prediction for a saved kundli.

### Community 177 - "Community 177"
Cohesion: 0.6
Nodes (5): H(), main(), P(), pick(), FULL verbose Lal Kitab output for Meharban Singh Upneja — every engine's complet

### Community 178 - "Community 178"
Cohesion: 0.6
Nodes (5): H(), main(), P(), pick(), FULL verbose Lal Kitab output for Jasmine Kaur Khurana — every engine's complete

### Community 179 - "Community 179"
Cohesion: 0.4
Nodes (3): _env_first(), Application configuration — loaded from environment variables with defaults., Return the first non-empty environment variable from the given names.

### Community 180 - "Community 180"
Cohesion: 0.4
Nodes (4): get_tithi_remedy_timing(), app/lalkitab_tithi_timing.py  P2.10 — Tithi-based remedy timing.  Lal Kitab 1952, # NOTE: for Jupiter we encode Amavasya as forbidden by returning, Return the tithi-timing bundle for a given planet's remedy.      Args:         p

### Community 181 - "Community 181"
Cohesion: 0.6
Nodes (3): a(), b(), k()

### Community 182 - "Community 182"
Cohesion: 0.5
Nodes (3): detect_lalkitab_doshas(), Lal Kitab Dosha Detection Engine.  Detects classical Lal Kitab doshas from plane, Detect Lal Kitab doshas from planet positions.      Args:         planet_positio

### Community 183 - "Community 183"
Cohesion: 0.5
Nodes (3): calculate_nadi_insights(), nadi_engine.py -- Nadi Astrology Interpretive Engine ===========================, Identify Nadi shlokas / yogas based on planet placements in the same house.

### Community 184 - "Community 184"
Cohesion: 0.5
Nodes (3): analyze_sacrifice(), lalkitab_sacrifice.py — Bali Ka Bakra (Sacrificial Lamb Logic) =================, Analyzes the chart for Bali Ka Bakra (sacrificial lamb) patterns.      planet_po

### Community 185 - "Community 185"
Cohesion: 0.5
Nodes (3): get_remedy_precautions(), app/lalkitab_savdhaniyan.py  Savdhaniyan (सावधानियाँ) — mandatory precautions th, Return the full Savdhaniyan bundle for a given planet's remedy.      Args:

### Community 186 - "Community 186"
Cohesion: 0.5
Nodes (3): get_forbidden_remedies(), lalkitab_forbidden.py — Dynamic Forbidden Actions List =========================, Returns forbidden actions specific to this chart's planet placements.      plane

### Community 187 - "Community 187"
Cohesion: 0.5
Nodes (3): detect_festivals(), festival_engine.py -- Rule-Based Hindu Festival & Vrat Detection Engine ========, Detect festivals and vrats for given panchang elements.      Checks all three so

### Community 188 - "Community 188"
Cohesion: 0.67
Nodes (3): calculate_yogini_dasha(), get_starting_yogini(), Calculate Yogini Dasha periods. Returns periods for up to 108 years (3 cycles).

### Community 189 - "Community 189"
Cohesion: 0.5
Nodes (3): detect_andhe_grah(), app/lalkitab_andhe_grah.py  Andhe Grah (अंधे ग्रह) — Blind Planet detection.  So, Return per-planet blind-status plus a list of blind planets.      Args:

### Community 190 - "Community 190"
Cohesion: 0.5
Nodes (3): app/lalkitab_source_tags.py  Single source of truth for the provenance tag on ev, Return the source tag for a given engine function name.      Unknown engines fal, source_of()

### Community 191 - "Community 191"
Cohesion: 0.5
Nodes (3): Shared rate-limit helpers., Scope rate limits to the active test DB and client address., request_rate_limit_key()

### Community 192 - "Community 192"
Cohesion: 0.67
Nodes (3): _age_years(), get_age_activation(), Lal Kitab age activation (backend)  The UI shows age-bucket activation periods (

### Community 193 - "Community 193"
Cohesion: 0.5
Nodes (0): 

### Community 194 - "Community 194"
Cohesion: 0.5
Nodes (0): 

### Community 195 - "Community 195"
Cohesion: 0.67
Nodes (1): Lal Kitab Rules Engine (backend)  Purpose: - Provide rule-driven structures used

### Community 196 - "Community 196"
Cohesion: 0.67
Nodes (2): calculate_lifelong_sade_sati(), Calculate lifelong Sade Sati, Dhaiya (Ashtamesh/Kantak), and Panauti phases.

### Community 197 - "Community 197"
Cohesion: 0.67
Nodes (0): 

### Community 198 - "Community 198"
Cohesion: 1.0
Nodes (1): Lal Kitab remedy context — Sun, Moon, Mars (36 entries)

### Community 199 - "Community 199"
Cohesion: 1.0
Nodes (1): Lal Kitab remedy context — Saturn, Rahu, Ketu (36 entries)

### Community 200 - "Community 200"
Cohesion: 1.0
Nodes (1): Lal Kitab remedy context — Mercury, Jupiter, Venus (36 entries)

### Community 201 - "Community 201"
Cohesion: 1.0
Nodes (0): 

### Community 202 - "Community 202"
Cohesion: 1.0
Nodes (0): 

### Community 203 - "Community 203"
Cohesion: 1.0
Nodes (1): Route registry — import all routers for inclusion in the FastAPI app.

### Community 204 - "Community 204"
Cohesion: 1.0
Nodes (1): lalkitab_translations.py — Lal Kitab bilingual constants =======================

### Community 205 - "Community 205"
Cohesion: 1.0
Nodes (1): Chandra Chalana 43-day protocol tasks (backend).  The protocol itself is tracked

### Community 206 - "Community 206"
Cohesion: 1.0
Nodes (1): Lal Kitab 1952 — Remedy Context: problem / reason / how_it_works Source: Pt. Roo

### Community 207 - "Community 207"
Cohesion: 1.0
Nodes (1): Transit interpretation fragments — 9 planets x 12 houses x 5 areas, bilingual.

### Community 208 - "Community 208"
Cohesion: 1.0
Nodes (1): vastu/data.py — Complete Vastu Shastra Reference Data ==========================

### Community 209 - "Community 209"
Cohesion: 1.0
Nodes (0): 

### Community 210 - "Community 210"
Cohesion: 1.0
Nodes (0): 

### Community 211 - "Community 211"
Cohesion: 1.0
Nodes (0): 

### Community 212 - "Community 212"
Cohesion: 1.0
Nodes (0): 

### Community 213 - "Community 213"
Cohesion: 1.0
Nodes (0): 

### Community 214 - "Community 214"
Cohesion: 1.0
Nodes (0): 

### Community 215 - "Community 215"
Cohesion: 1.0
Nodes (0): 

### Community 216 - "Community 216"
Cohesion: 1.0
Nodes (0): 

### Community 217 - "Community 217"
Cohesion: 1.0
Nodes (0): 

### Community 218 - "Community 218"
Cohesion: 1.0
Nodes (1): Krishna Pratipada to Panchami (16-20) normalise to 1-5 → Full Life.

### Community 219 - "Community 219"
Cohesion: 1.0
Nodes (1): Krishna Shashthi to Dashami (21-25) normalise to 6-10 → Half Life.

### Community 220 - "Community 220"
Cohesion: 1.0
Nodes (1): Krishna Ekadashi to Chaturdashi (26-29) normalise to 11-14 → Weak Life.

### Community 221 - "Community 221"
Cohesion: 1.0
Nodes (0): 

### Community 222 - "Community 222"
Cohesion: 1.0
Nodes (0): 

### Community 223 - "Community 223"
Cohesion: 1.0
Nodes (0): 

### Community 224 - "Community 224"
Cohesion: 1.0
Nodes (0): 

### Community 225 - "Community 225"
Cohesion: 1.0
Nodes (0): 

### Community 226 - "Community 226"
Cohesion: 1.0
Nodes (0): 

### Community 227 - "Community 227"
Cohesion: 1.0
Nodes (0): 

### Community 228 - "Community 228"
Cohesion: 1.0
Nodes (0): 

### Community 229 - "Community 229"
Cohesion: 1.0
Nodes (0): 

### Community 230 - "Community 230"
Cohesion: 1.0
Nodes (0): 

### Community 231 - "Community 231"
Cohesion: 1.0
Nodes (0): 

### Community 232 - "Community 232"
Cohesion: 1.0
Nodes (0): 

### Community 233 - "Community 233"
Cohesion: 1.0
Nodes (0): 

### Community 234 - "Community 234"
Cohesion: 1.0
Nodes (0): 

### Community 235 - "Community 235"
Cohesion: 1.0
Nodes (0): 

### Community 236 - "Community 236"
Cohesion: 1.0
Nodes (0): 

### Community 237 - "Community 237"
Cohesion: 1.0
Nodes (0): 

### Community 238 - "Community 238"
Cohesion: 1.0
Nodes (0): 

### Community 239 - "Community 239"
Cohesion: 1.0
Nodes (0): 

### Community 240 - "Community 240"
Cohesion: 1.0
Nodes (0): 

### Community 241 - "Community 241"
Cohesion: 1.0
Nodes (0): 

### Community 242 - "Community 242"
Cohesion: 1.0
Nodes (0): 

### Community 243 - "Community 243"
Cohesion: 1.0
Nodes (0): 

### Community 244 - "Community 244"
Cohesion: 1.0
Nodes (0): 

### Community 245 - "Community 245"
Cohesion: 1.0
Nodes (0): 

### Community 246 - "Community 246"
Cohesion: 1.0
Nodes (0): 

### Community 247 - "Community 247"
Cohesion: 1.0
Nodes (0): 

### Community 248 - "Community 248"
Cohesion: 1.0
Nodes (0): 

### Community 249 - "Community 249"
Cohesion: 1.0
Nodes (0): 

### Community 250 - "Community 250"
Cohesion: 1.0
Nodes (0): 

### Community 251 - "Community 251"
Cohesion: 1.0
Nodes (0): 

### Community 252 - "Community 252"
Cohesion: 1.0
Nodes (0): 

### Community 253 - "Community 253"
Cohesion: 1.0
Nodes (0): 

### Community 254 - "Community 254"
Cohesion: 1.0
Nodes (0): 

### Community 255 - "Community 255"
Cohesion: 1.0
Nodes (0): 

### Community 256 - "Community 256"
Cohesion: 1.0
Nodes (0): 

### Community 257 - "Community 257"
Cohesion: 1.0
Nodes (0): 

### Community 258 - "Community 258"
Cohesion: 1.0
Nodes (0): 

### Community 259 - "Community 259"
Cohesion: 1.0
Nodes (0): 

### Community 260 - "Community 260"
Cohesion: 1.0
Nodes (0): 

### Community 261 - "Community 261"
Cohesion: 1.0
Nodes (1): Sample parts 0..107 for each sign and confirm all 12 target signs appear.

### Community 262 - "Community 262"
Cohesion: 1.0
Nodes (1): Each planet must be in the exact sign+house from the ref snapshot.

### Community 263 - "Community 263"
Cohesion: 1.0
Nodes (0): 

### Community 264 - "Community 264"
Cohesion: 1.0
Nodes (0): 

### Community 265 - "Community 265"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **1874 isolated node(s):** `Lal Kitab remedy context — Sun, Moon, Mars (36 entries)`, `Tests for enhanced Choghadiya — Vaar Vela, Kaal Vela, Kaal Ratri flags.`, `Exactly ONE day period must have vaar_vela=True for each weekday.`, `Exactly ONE day period must have kaal_vela=True for each weekday.`, `Exactly ONE night period must have kaal_ratri=True for each weekday.` (+1869 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 198`** (2 nodes): `lk_ctx_a.py`, `Lal Kitab remedy context — Sun, Moon, Mars (36 entries)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 199`** (2 nodes): `lk_ctx_c.py`, `Lal Kitab remedy context — Saturn, Rahu, Ketu (36 entries)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 200`** (2 nodes): `lk_ctx_b.py`, `Lal Kitab remedy context — Mercury, Jupiter, Venus (36 entries)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 201`** (2 nodes): `test_fest_engine.py`, `test_festivals()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 202`** (2 nodes): `test_flags.py`, `test_sunrise_flags()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 203`** (2 nodes): `__init__.py`, `Route registry — import all routers for inclusion in the FastAPI app.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 204`** (2 nodes): `lalkitab_translations.py`, `lalkitab_translations.py — Lal Kitab bilingual constants =======================`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 205`** (2 nodes): `lalkitab_chandra_tasks.py`, `Chandra Chalana 43-day protocol tasks (backend).  The protocol itself is tracked`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 206`** (2 nodes): `lalkitab_remedy_context.py`, `Lal Kitab 1952 — Remedy Context: problem / reason / how_it_works Source: Pt. Roo`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 207`** (2 nodes): `transit_interpretations.py`, `Transit interpretation fragments — 9 planets x 12 houses x 5 areas, bilingual.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 208`** (2 nodes): `data.py`, `vastu/data.py — Complete Vastu Shastra Reference Data ==========================`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 209`** (2 nodes): `analyze-i18n.js`, `walk()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 210`** (2 nodes): `test_transit_interpretations_completeness.py`, `test_transit_fragments_include_9_planets_and_full_matrix()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 211`** (2 nodes): `test_panchang_sankranti_route.py`, `test_panchang_sankranti_route_returns_12()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 212`** (2 nodes): `connection.js`, `testConnection()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 213`** (2 nodes): `predictions.js`, `auth()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 214`** (2 nodes): `remedies.js`, `auth()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 215`** (2 nodes): `KundliChart.jsx`, `KundliChart()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 216`** (1 nodes): `check_swe_help.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 217`** (1 nodes): `stress_test.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 218`** (1 nodes): `Krishna Pratipada to Panchami (16-20) normalise to 1-5 → Full Life.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 219`** (1 nodes): `Krishna Shashthi to Dashami (21-25) normalise to 6-10 → Half Life.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 220`** (1 nodes): `Krishna Ekadashi to Chaturdashi (26-29) normalise to 11-14 → Weak Life.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 221`** (1 nodes): `ui-test.spec.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 222`** (1 nodes): `tailwind.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 223`** (1 nodes): `playwright.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 224`** (1 nodes): `vite.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 225`** (1 nodes): `postcss.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 226`** (1 nodes): `palette-CXiXSgC5.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 227`** (1 nodes): `house-DtiC-4UK.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 228`** (1 nodes): `hash-CicP2k4H.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 229`** (1 nodes): `sun-BzBhZV-E.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 230`** (1 nodes): `zap-CAEtoi2h.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 231`** (1 nodes): `circle-alert-C7OzIryt.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 232`** (1 nodes): `circle-check-big-C2G1rGUt.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 233`** (1 nodes): `plus-0BNEFBy0.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 234`** (1 nodes): `activity-X4r3g2MZ.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 235`** (1 nodes): `info-CrU8AAHX.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 236`** (1 nodes): `chevron-left-De_SGD7e.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 237`** (1 nodes): `search-B7V9CMzU.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 238`** (1 nodes): `chevron-up-oUmfnrAD.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 239`** (1 nodes): `navigation-KikWBpYy.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 240`** (1 nodes): `arrow-left-B1R7J2oO.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 241`** (1 nodes): `save-CurQzcRD.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 242`** (1 nodes): `circle-check-CgXHvHNa.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 243`** (1 nodes): `calendar-BAWu2H0T.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 244`** (1 nodes): `eye-CP953dOK.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 245`** (1 nodes): `map-pin-4ZjEbj4U.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 246`** (1 nodes): `orbit-BJqvfdpJ.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 247`** (1 nodes): `briefcase-CKH9P3l8.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 248`** (1 nodes): `rotate-ccw-DKeW6YZS.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 249`** (1 nodes): `clock-BmMvehyB.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 250`** (1 nodes): `chevron-right-BX36YS4o.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 251`** (1 nodes): `send-DBV8maWO.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 252`** (1 nodes): `trending-up-D6lZAkWG.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 253`** (1 nodes): `triangle-alert-Djnuq5R0.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 254`** (1 nodes): `book-open-DsqoyRev.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 255`** (1 nodes): `loader-circle-DHqOI4NW.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 256`** (1 nodes): `wallet-Wc7AxNdH.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 257`** (1 nodes): `shield-check-CeboXS6O.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 258`** (1 nodes): `sticky-note-Dh-n4DfT.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 259`** (1 nodes): `arrow-right-Dg-Z4lpq.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 260`** (1 nodes): `index.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 261`** (1 nodes): `Sample parts 0..107 for each sign and confirm all 12 target signs appear.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 262`** (1 nodes): `Each planet must be in the exact sign+house from the ref snapshot.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 263`** (1 nodes): `wxLogin.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 264`** (1 nodes): `server.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 265`** (1 nodes): `aspect-ratio.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `js()` connect `Community 3` to `Community 32`, `Community 12`, `Community 6`?**
  _High betweenness centrality (0.003) - this node is a cross-community bridge._
- **Why does `KPHoraryRequest` connect `Community 8` to `Community 2`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Why does `KPHoraryPredictRequest` connect `Community 8` to `Community 2`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Are the 72 inferred relationships involving `KundliRequest` (e.g. with `FreePreviewRequest` and `Kundli routes — generate, retrieve, list, iogita analysis, match, dosha, dasha,`) actually correct?**
  _`KundliRequest` has 72 INFERRED edges - model-reasoned connections that need verification._
- **Are the 72 inferred relationships involving `KundliMatchRequest` (e.g. with `FreePreviewRequest` and `Kundli routes — generate, retrieve, list, iogita analysis, match, dosha, dasha,`) actually correct?**
  _`KundliMatchRequest` has 72 INFERRED edges - model-reasoned connections that need verification._
- **Are the 72 inferred relationships involving `DivisionalChartRequest` (e.g. with `FreePreviewRequest` and `Kundli routes — generate, retrieve, list, iogita analysis, match, dosha, dasha,`) actually correct?**
  _`DivisionalChartRequest` has 72 INFERRED edges - model-reasoned connections that need verification._
- **Are the 72 inferred relationships involving `BirthRectificationRequest` (e.g. with `FreePreviewRequest` and `Kundli routes — generate, retrieve, list, iogita analysis, match, dosha, dasha,`) actually correct?**
  _`BirthRectificationRequest` has 72 INFERRED edges - model-reasoned connections that need verification._