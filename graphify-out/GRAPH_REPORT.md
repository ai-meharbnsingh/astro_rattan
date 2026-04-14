# Graph Report - .  (2026-04-14)

## Corpus Check
- 305 files · ~5,653,504 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3574 nodes · 7396 edges · 127 communities detected
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 307 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `M()` - 74 edges
2. `o()` - 56 edges
3. `F()` - 48 edges
4. `Am()` - 48 edges
5. `KundliRequest` - 40 edges
6. `KundliMatchRequest` - 40 edges
7. `DivisionalChartRequest` - 40 edges
8. `analyze_yogas_and_doshas()` - 36 edges
9. `ar()` - 33 edges
10. `rb()` - 32 edges

## Surprising Connections (you probably didn't know these)
- `Admin routes — user management, stats, kundli overview, live traffic panel.` --uses--> `AdminUserUpdate`  [INFERRED]
  app/routes/admin.py → app/models.py
- `Dashboard stats — user count, kundli count, recent activity.` --uses--> `AdminUserUpdate`  [INFERRED]
  app/routes/admin.py → app/models.py
- `List all users with pagination.` --uses--> `AdminUserUpdate`  [INFERRED]
  app/routes/admin.py → app/models.py
- `Get detailed user info + their kundlis.` --uses--> `AdminUserUpdate`  [INFERRED]
  app/routes/admin.py → app/models.py
- `Change a user's role (user/astrologer/admin).` --uses--> `AdminUserUpdate`  [INFERRED]
  app/routes/admin.py → app/models.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.01
Nodes (491): a(), aA(), Ab(), ac(), ad(), ag(), ah(), ai() (+483 more)

### Community 1 - "Community 1"
Cohesion: 0.01
Nodes (67): apiFetch(), fetchWithRetry(), friendlyError(), tryRefreshToken(), rotateByLagna(), SAVKundliChart(), handleOtpKeyDown(), handleResendOtp() (+59 more)

### Community 2 - "Community 2"
Cohesion: 0.02
Nodes (114): ie(), w(), be(), ve(), ac(), ae(), ai(), Ar() (+106 more)

### Community 3 - "Community 3"
Cohesion: 0.05
Nodes (163): _a(), aa(), ac(), Ae(), af(), ao(), ar(), at() (+155 more)

### Community 4 - "Community 4"
Cohesion: 0.03
Nodes (131): get_live_dashboard(), get_stats(), get_user_detail(), list_all_kundlis(), list_users(), Admin routes — user management, stats, kundli overview, live traffic panel., Change a user's role (user/astrologer/admin)., Activate or deactivate a user account. (+123 more)

### Community 5 - "Community 5"
Cohesion: 0.01
Nodes (141): Tests for app.vastu — Vastu Shastra engine calculations., Residential buildings must use Manduka Mandala (8x8 = 64 squares)., Temple buildings must use Paramasayika Mandala (9x9 = 81 squares)., Mandala must return all 10 zones with devtas., Energy balance positive + negative + neutral must equal 45., Body mapping must include head, face, chest, navel, arms, legs, feet., Each devta must have a unique id from 1 to 45., In a balanced mandala, positive devtas must outnumber negative ones. (+133 more)

### Community 6 - "Community 6"
Cohesion: 0.04
Nodes (73): _2(), A_(), a0(), A2(), aT(), b0(), _c(), C2() (+65 more)

### Community 7 - "Community 7"
Cohesion: 0.07
Nodes (80): _build_kundli_pdf(), _chart_data(), check_doshas(), _compute_dasha(), delete_all_my_kundlis(), delete_kundli(), download_full_report(), download_kundli_pdf() (+72 more)

### Community 8 - "Community 8"
Cohesion: 0.05
Nodes (81): analyze_yogas_and_doshas(), check_adhi_yoga(), check_amala_yoga(), check_anapha_yoga(), check_angarak_dosha(), check_budhaditya_yoga(), check_chandra_mangal_yoga(), check_danda_yoga() (+73 more)

### Community 9 - "Community 9"
Cohesion: 0.07
Nodes (68): Ae(), ar(), at(), Be(), br(), Ce(), cr(), De() (+60 more)

### Community 10 - "Community 10"
Cohesion: 0.04
Nodes (51): isInTimeRange(), toMinutes(), getTypeBucket(), isInTimeRange(), renderRow(), toMinutes(), isDayStart(), isInTimeRange() (+43 more)

### Community 11 - "Community 11"
Cohesion: 0.03
Nodes (45): auth_headers(), auth_token(), client(), Route-level tests for /api/kundli/* endpoints.  Uses FastAPI TestClient with a f, POST /api/kundli/generate → 201, returns chart_data with 9 planets., POST /api/kundli/generate with invalid date → 422 or 500., POST /api/kundli/generate without auth → 401., POST /api/kundli/generate with missing required fields → 422. (+37 more)

### Community 12 - "Community 12"
Cohesion: 0.06
Nodes (61): _approx_sunrise_sunset(), calculate_abhijit_muhurat(), calculate_brahma_muhurat(), calculate_choghadiya(), calculate_gulika_kaal(), calculate_night_choghadiya(), calculate_panchang(), calculate_planetary_positions() (+53 more)

### Community 13 - "Community 13"
Cohesion: 0.04
Nodes (16): Ar(), Er(), fa(), Fr(), hl(), Hr(), is(), Nn() (+8 more)

### Community 14 - "Community 14"
Cohesion: 0.05
Nodes (53): _abda_bala(), _angular_distance(), _aspect_strength(), _ayana_bala(), calculate_bhav_bala(), calculate_shadbala(), _cheshta_bala(), _dig_bala() (+45 more)

### Community 15 - "Community 15"
Cohesion: 0.07
Nodes (51): analyze_name_numerology(), _build_number_affinities(), _build_pair_combination_table(), _calculate_house_compatibility(), calculate_house_numerology(), calculate_mobile_numerology(), calculate_numerology(), calculate_vehicle_numerology() (+43 more)

### Community 16 - "Community 16"
Cohesion: 0.05
Nodes (13): ba(), fa(), Ht(), Ia(), ja(), Ke(), Mt(), Oa() (+5 more)

### Community 17 - "Community 17"
Cohesion: 0.06
Nodes (39): build_full_report(), _build_planets_in_houses(), _compound_relation(), _display(), _draw_north_indian_chart(), _find_hindi_font(), _fmt_date(), _fmt_num() (+31 more)

### Community 18 - "Community 18"
Cohesion: 0.07
Nodes (37): get_db(), _get_pool(), _get_valid_conn(), init_db(), migrate_forum_tables(), migrate_gamification_tables(), migrate_notification_tables(), migrate_referral_tables() (+29 more)

### Community 19 - "Community 19"
Cohesion: 0.05
Nodes (45): add_chandra_journal(), add_tracker_journal(), delete_saved_prediction(), get_chandra_state(), get_gochar_transits(), get_lalkitab_advanced(), get_nishaniyan(), _get_planet_positions() (+37 more)

### Community 20 - "Community 20"
Cohesion: 0.06
Nodes (43): _assess_remedy_accessibility(), _calculate_d10(), calculate_d10_dasamsa(), _calculate_d12(), _calculate_d2(), _calculate_d3(), _calculate_d30(), _calculate_d4() (+35 more)

### Community 21 - "Community 21"
Cohesion: 0.05
Nodes (15): Tests for app.panchang_engine -- Vedic Panchang Calculator., Test Rahu Kaal calculation., Monday Rahu Kaal: slot 2 of 8 (equal day)., Sunday Rahu Kaal: slot 8 of 8., Validate TITHIS constant data., Rahu Kaal must be between sunrise and sunset., Test Choghadiya calculation., First period starts at sunrise, last ends at sunset. (+7 more)

### Community 22 - "Community 22"
Cohesion: 0.05
Nodes (11): Smoke tests for critical engine modules: varshphal, transit, astro_iogita, dasha, Smoke tests for transit_engine.py., Smoke tests for astro_iogita_engine.py., Smoke tests for dasha_engine.py., Design change: dasha now covers 2 full 120-year cycles = 240 years total., When moon_longitude is given, first dasha balance is partial.          Design ch, Smoke tests for varshphal_engine.py., TestAstroIogitaEngine (+3 more)

### Community 23 - "Community 23"
Cohesion: 0.08
Nodes (37): _analyze_houses(), _angular_distance(), _build_summary(), calculate_eclipses(), calculate_ingress(), calculate_mundane_analysis(), _conflict_indicators(), _current_transits_in_country_chart() (+29 more)

### Community 24 - "Community 24"
Cohesion: 0.05
Nodes (16): Tests for app.kp_engine -- Krishnamurti Paddhati Engine., Validate Vimshottari Dasha constants., Validate the pre-built KP sub-lord table., Must have 27 nakshatras * 9 subs = 243 entries., First entry starts at 0, last entry ends at ~360., Each entry's end should equal the next entry's start., First nakshatra (Ashwini) lord is Ketu., Ashwini's first sub = its own lord (Ketu). (+8 more)

### Community 25 - "Community 25"
Cohesion: 0.1
Nodes (35): _approx_ascendant(), _approx_ayanamsa(), _approx_moon_longitude(), _approx_planet_longitude(), _approx_rahu_longitude(), _approx_sun_longitude(), _build_status(), _calculate_fallback() (+27 more)

### Community 26 - "Community 26"
Cohesion: 0.09
Nodes (35): analyze_entrance(), analyze_home_layout(), _build_entrance_result(), _build_room_remedies(), calculate_mandala(), _calculate_vastu_score(), _degrees_to_direction(), _direction_to_pada_index() (+27 more)

### Community 27 - "Community 27"
Cohesion: 0.09
Nodes (31): ai_ask_question(), ai_gita_answer(), ai_interpret_kundli(), ai_oracle(), ai_remedies(), _call_ai(), _call_gemini(), _call_openai() (+23 more)

### Community 28 - "Community 28"
Cohesion: 0.07
Nodes (31): analyze_masnui_transits(), calculate_hora_lord(), calculate_karmic_debts(), calculate_karmic_debts_with_hora(), calculate_kayam_grah(), calculate_lk_aspects(), calculate_masnui_planets(), _calculate_masnui_psychological_profile() (+23 more)

### Community 29 - "Community 29"
Cohesion: 0.13
Nodes (30): calculate_argala(), calculate_chara_dasha(), calculate_chara_karakas(), calculate_indu_lagna(), calculate_jaimini(), calculate_jaimini_drishti(), calculate_jaimini_yogas(), calculate_longevity() (+22 more)

### Community 30 - "Community 30"
Cohesion: 0.12
Nodes (12): be(), da(), E(), ie(), ma(), oa(), oe(), pe() (+4 more)

### Community 31 - "Community 31"
Cohesion: 0.09
Nodes (22): calculate_gun_milan(), _normalize_nakshatra(), _rashi_lord(), matching_engine.py — Kundli Gun Milan (Ashtakoota) Matching Engine =============, Varna koot: groom's varna should be >= bride's. Max 1 point., Vasya koot: mutual influence/attraction based on Moon rashi. Max 2 points., Tara koot: based on nakshatra distance (bidirectional). Max 3 points.     Standa, Yoni koot: sexual/physical compatibility. Max 4 points.     Same=4, Friendly=3, (+14 more)

### Community 32 - "Community 32"
Cohesion: 0.09
Nodes (4): kt(), Me(), _t(), V()

### Community 33 - "Community 33"
Cohesion: 0.18
Nodes (18): a(), at(), be(), e(), Ee(), Fe(), Le(), o() (+10 more)

### Community 34 - "Community 34"
Cohesion: 0.14
Nodes (19): _atom(), build_atom_vector(), _generate_iogita_insight(), _generate_normal_insights(), _get_dignity_label(), get_planet_strength(), identify_basin(), _print_report() (+11 more)

### Community 35 - "Community 35"
Cohesion: 0.14
Nodes (19): _build_kp_sub_lords(), calculate_kp_cuspal(), _find_house_for_planet(), _find_vimshottari_index(), _get_houses_owned(), get_star_lord_of_sub_lord(), get_sub_lord(), get_sub_sub_lord() (+11 more)

### Community 36 - "Community 36"
Cohesion: 0.12
Nodes (19): _build_ai_horoscope_prompt(), generate_ai_horoscope(), generate_daily_horoscopes(), _generate_template_horoscope(), _get_current_transits(), _parse_ai_sections(), H-09: Horoscope Content Generation Pipeline — seeds daily & weekly horoscopes., Calculate today's planetary positions (signs) for horoscope weighting. (+11 more)

### Community 37 - "Community 37"
Cohesion: 0.13
Nodes (15): BaseHTTPMiddleware, _extract_user_id(), get_traffic_snapshot(), H-01: Structured Logging Middleware — logs every request with method, path, stat, Extract user_id from JWT Bearer token if present., Middleware that logs every HTTP request and records to the live traffic buffer., Return a snapshot of recent traffic for the live admin dashboard.     Thread-saf, RequestLoggingMiddleware (+7 more)

### Community 38 - "Community 38"
Cohesion: 0.16
Nodes (17): cleanup_old_uploads(), ensure_upload_dir(), map_room_placements(), _optimize_image(), pixel_to_direction(), vastu/floorplan.py — Floor Plan Upload & Pixel-to-Direction Mapper =============, Resize large images and compress to JPEG for storage efficiency.     Returns opt, Validate, optimize, and save uploaded floor plan image.      Returns:         di (+9 more)

### Community 39 - "Community 39"
Cohesion: 0.11
Nodes (17): Tests for numerology_engine.py — Pythagorean numerology calculations., Verify master number 11 is preserved (not reduced to 2)., Destiny number (formerly expression) uses all letters of the name., Soul urge uses only vowels (A, E, I, O, U)., Personality uses only consonants., Verify all required keys are present in the output dict., Life path for 1990-01-15: 1+9+9+0=19->10->1 + 0+1=1 + 1+5=6 => 1+1+6=8., Master numbers 11, 22, 33 should not be reduced further. (+9 more)

### Community 40 - "Community 40"
Cohesion: 0.17
Nodes (15): calculate_mudda_dasha(), calculate_muntha(), calculate_varshphal(), calculate_year_lord(), find_solar_return_jd(), _jd_to_datetime(), varshphal_engine.py — Vedic Varshphal (Solar Return / Tajaka) Engine ===========, Muntha advances one sign per year from natal ascendant.     Returns: {sign, sign (+7 more)

### Community 41 - "Community 41"
Cohesion: 0.2
Nodes (15): _build_antardasha_periods(), _build_pratyantar_periods(), calculate_dasha(), _calculate_dasha_balance(), calculate_extended_dasha(), _get_dasha_sequence(), _parse_date(), dasha_engine.py — Vimshottari Dasha Calculation Engine ========================= (+7 more)

### Community 42 - "Community 42"
Cohesion: 0.13
Nodes (13): _bootstrap_db(), client(), _create_kundli(), db(), _make_admin(), _make_astrologer(), Shared test fixtures — temp DB, TestClient, auth helpers.  Every test module get, Insert a minimal kundli record and return its id. (+5 more)

### Community 43 - "Community 43"
Cohesion: 0.29
Nodes (11): aa(), c(), d(), ea(), h(), J(), L(), Q() (+3 more)

### Community 44 - "Community 44"
Cohesion: 0.21
Nodes (13): _binary_search_station(), calculate_retrograde_stations(), _get_longitude(), _get_speed(), _jd_to_date(), _jd_to_datetime(), retrograde_engine.py — Planetary Retrograde Station Calculator =================, Convert Julian Day to YYYY-MM-DD string. (+5 more)

### Community 45 - "Community 45"
Cohesion: 0.2
Nodes (13): calculate_avakhada(), _get_gana(), _get_nadi(), _get_nakshatra_index(), _get_pada(), _get_western_sign(), avakhada_engine.py — Avakhada Chakra Calculation Engine ========================, Get nakshatra index (0-26) from sidereal longitude. (+5 more)

### Community 46 - "Community 46"
Cohesion: 0.2
Nodes (13): auto_detect_rooms(), _detect_ocr_labels(), _detect_opencv(), _detect_yolo(), _match_room(), _preprocess_for_ocr(), vastu/auto_detect.py — AI Room Detection for Floor Plans =======================, Preprocess floor plan for OCR: grayscale → upscale 2x → sharpen → binarize. (+5 more)

### Community 47 - "Community 47"
Cohesion: 0.22
Nodes (13): get_all_signs_horoscope(), get_daily_horoscope(), get_transit_insights(), get_weekly_horoscope(), _parse_content_to_sections(), Horoscope routes — daily, weekly, all-signs, and transit-aware horoscopes., Get weekly horoscope for a specific sign., Get horoscopes for all 12 signs at once. (+5 more)

### Community 48 - "Community 48"
Cohesion: 0.2
Nodes (6): be(), j(), m(), pe(), ss(), ts()

### Community 49 - "Community 49"
Cohesion: 0.14
Nodes (13): Tests for lalkitab_engine.py — Lal Kitab remedies engine., Each planet should have 5-8 remedies., A debilitated planet (strength < 0.5) should receive remedies., An exalted planet (strength >= 0.5) should NOT receive remedies., A planet in enemy sign (strength 0.35 < 0.5) should receive remedies., Verify the output dict structure for each planet., REMEDIES dict must cover all 9 Vedic planets., test_enemy_planet_gets_remedies() (+5 more)

### Community 50 - "Community 50"
Cohesion: 0.18
Nodes (12): calculate_aspects(), calculate_cusp_aspects(), calculate_western_aspects(), _get_aspected_houses(), _match_western_aspect(), aspects_engine.py -- Vedic Planetary Aspects Calculator ========================, Calculate degree-based Western aspects between all planet pairs.      Returns a, Find the Western aspect matching a given degree difference, if any. (+4 more)

### Community 51 - "Community 51"
Cohesion: 0.22
Nodes (6): assert(), initNECaptchaWithFallback(), isInteger(), loadResource(), normalizeFallbackConfig(), ObjectAssign()

### Community 52 - "Community 52"
Cohesion: 0.23
Nodes (11): _apply_ekadhipatya_shodhana(), _apply_trikona_shodhana(), calculate_ashtakvarga(), _calculate_shodhya_pinda(), ashtakvarga_engine.py -- Ashtakvarga Calculation Engine ========================, Convert sign name to 0-based index., Calculate the Ashtakvarga system for a given chart.     Includes Trikona Shodhan, Reduces bindus in trine signs.     Trines: (0,4,8), (1,5,9), (2,6,10), (3,7,11) (+3 more)

### Community 53 - "Community 53"
Cohesion: 0.23
Nodes (11): calculate_baladi(), calculate_deeptadi(), calculate_jagradadi(), calculate_shyanadi(), get_all_avasthas(), interpretations.py -- Static Text Databases for Kundli Report ==================, Jagradadi Avastha (3 states):     - Jagrad (Awake): planet in own sign or exalte, Baladi Avastha (5 states based on degree within sign):     Odd signs: Bala(0-6), (+3 more)

### Community 54 - "Community 54"
Cohesion: 0.27
Nodes (5): C(), k(), M(), P(), V()

### Community 55 - "Community 55"
Cohesion: 0.22
Nodes (4): createDebouncedFn(), createHead(), setVhUnit(), vhUnitFix()

### Community 56 - "Community 56"
Cohesion: 0.27
Nodes (9): calculate_transit_forecast(), calculate_transits(), _check_sade_sati(), _house_from_moon(), transit_engine.py -- Gochara (Transit) Prediction Engine =======================, Calculate planetary transits and their Gochara effects on a natal chart., Calculate transit intensity scores for the next N days., Return the house number (1-12) of transit_sign counted from moon_sign.     House (+1 more)

### Community 57 - "Community 57"
Cohesion: 0.2
Nodes (9): get_eclipses(), get_ingress(), get_mundane_analysis(), list_countries(), Mundane Astrology routes — country charts, national analysis, eclipses, ingress., Return the dates when the Sun enters each of the 12 sidereal signs     (Sankrant, Return the list of available country charts for mundane analysis., Full mundane astrology analysis for a country: birth chart, current transits, (+1 more)

### Community 58 - "Community 58"
Cohesion: 0.22
Nodes (2): bs(), Qe()

### Community 59 - "Community 59"
Cohesion: 0.29
Nodes (6): D(), N(), O(), R(), w(), x()

### Community 60 - "Community 60"
Cohesion: 0.22
Nodes (1): RED phase: auth tests.

### Community 61 - "Community 61"
Cohesion: 0.36
Nodes (7): _is_auspicious_day(), _monthly_days(), muhurat_find(), muhurat_monthly(), Compatibility muhurat routes used by frontend widgets., Monthly calendar-style muhurat compatibility endpoint., Daily window compatibility endpoint for a selected date.

### Community 62 - "Community 62"
Cohesion: 0.57
Nodes (7): createClientsViaAPI(), fillBirthForm(), injectAuth(), main(), screenshot(), sleep(), waitForChart()

### Community 63 - "Community 63"
Cohesion: 0.52
Nodes (6): G(), J(), se(), U(), X(), y()

### Community 64 - "Community 64"
Cohesion: 0.4
Nodes (5): _get_dignity_label(), get_remedies(), lalkitab_engine.py — Lal Kitab Remedies Engine =================================, Determine dignity label for a planet in a sign., Get Lal Kitab remedies for weak or afflicted planets.      Args:         planet_

### Community 65 - "Community 65"
Cohesion: 0.4
Nodes (5): calculate_sodashvarga(), _get_dignity(), sodashvarga_engine.py -- Sodashvarga (16 Divisional Charts) Summary & Vimshopak, Determine the dignity of a planet in a given sign., Calculate Sodashvarga for all planets.      Args:         planet_longitudes: {pl

### Community 66 - "Community 66"
Cohesion: 0.47
Nodes (5): ai_interpret(), _compose_interpretation(), _normalize_period(), AI interpretation routes for kundli predictions., Return AI-style period prediction for a saved kundli.

### Community 67 - "Community 67"
Cohesion: 0.4
Nodes (3): _env_first(), Application configuration — loaded from environment variables with defaults., Return the first non-empty environment variable from the given names.

### Community 68 - "Community 68"
Cohesion: 0.6
Nodes (3): a(), b(), k()

### Community 69 - "Community 69"
Cohesion: 0.5
Nodes (3): calculate_nadi_insights(), nadi_engine.py -- Nadi Astrology Interpretive Engine ===========================, Identify Nadi shlokas / yogas based on planet placements in the same house.

### Community 70 - "Community 70"
Cohesion: 0.5
Nodes (3): detect_festivals(), festival_engine.py -- Rule-Based Hindu Festival & Vrat Detection Engine ========, Detect festivals and vrats for given panchang elements.      Checks all three so

### Community 71 - "Community 71"
Cohesion: 0.67
Nodes (3): calculate_yogini_dasha(), get_starting_yogini(), Calculate Yogini Dasha periods. Returns periods for up to 108 years (3 cycles).

### Community 72 - "Community 72"
Cohesion: 0.5
Nodes (3): Shared rate-limit helpers., Scope rate limits to the active test DB and client address., request_rate_limit_key()

### Community 73 - "Community 73"
Cohesion: 0.67
Nodes (2): calculate_lifelong_sade_sati(), Calculate lifelong Sade Sati, Dhaiya (Ashtamesh/Kantak), and Panauti phases.

### Community 74 - "Community 74"
Cohesion: 0.67
Nodes (2): calculate_upagrahas(), Calculate Upagrahas (sub-planets) including Aprakasha Grahas and Kala Velas.

### Community 75 - "Community 75"
Cohesion: 0.67
Nodes (0): 

### Community 76 - "Community 76"
Cohesion: 1.0
Nodes (1): Vercel serverless entry point — exposes the FastAPI app.

### Community 77 - "Community 77"
Cohesion: 1.0
Nodes (1): Route registry — import all routers for inclusion in the FastAPI app.

### Community 78 - "Community 78"
Cohesion: 1.0
Nodes (1): vastu/data.py — Complete Vastu Shastra Reference Data ==========================

### Community 79 - "Community 79"
Cohesion: 1.0
Nodes (0): 

### Community 80 - "Community 80"
Cohesion: 1.0
Nodes (0): 

### Community 81 - "Community 81"
Cohesion: 1.0
Nodes (0): 

### Community 82 - "Community 82"
Cohesion: 1.0
Nodes (0): 

### Community 83 - "Community 83"
Cohesion: 1.0
Nodes (0): 

### Community 84 - "Community 84"
Cohesion: 1.0
Nodes (0): 

### Community 85 - "Community 85"
Cohesion: 1.0
Nodes (0): 

### Community 86 - "Community 86"
Cohesion: 1.0
Nodes (0): 

### Community 87 - "Community 87"
Cohesion: 1.0
Nodes (0): 

### Community 88 - "Community 88"
Cohesion: 1.0
Nodes (0): 

### Community 89 - "Community 89"
Cohesion: 1.0
Nodes (0): 

### Community 90 - "Community 90"
Cohesion: 1.0
Nodes (0): 

### Community 91 - "Community 91"
Cohesion: 1.0
Nodes (0): 

### Community 92 - "Community 92"
Cohesion: 1.0
Nodes (0): 

### Community 93 - "Community 93"
Cohesion: 1.0
Nodes (0): 

### Community 94 - "Community 94"
Cohesion: 1.0
Nodes (0): 

### Community 95 - "Community 95"
Cohesion: 1.0
Nodes (0): 

### Community 96 - "Community 96"
Cohesion: 1.0
Nodes (0): 

### Community 97 - "Community 97"
Cohesion: 1.0
Nodes (0): 

### Community 98 - "Community 98"
Cohesion: 1.0
Nodes (0): 

### Community 99 - "Community 99"
Cohesion: 1.0
Nodes (0): 

### Community 100 - "Community 100"
Cohesion: 1.0
Nodes (0): 

### Community 101 - "Community 101"
Cohesion: 1.0
Nodes (0): 

### Community 102 - "Community 102"
Cohesion: 1.0
Nodes (0): 

### Community 103 - "Community 103"
Cohesion: 1.0
Nodes (0): 

### Community 104 - "Community 104"
Cohesion: 1.0
Nodes (0): 

### Community 105 - "Community 105"
Cohesion: 1.0
Nodes (0): 

### Community 106 - "Community 106"
Cohesion: 1.0
Nodes (0): 

### Community 107 - "Community 107"
Cohesion: 1.0
Nodes (0): 

### Community 108 - "Community 108"
Cohesion: 1.0
Nodes (0): 

### Community 109 - "Community 109"
Cohesion: 1.0
Nodes (0): 

### Community 110 - "Community 110"
Cohesion: 1.0
Nodes (0): 

### Community 111 - "Community 111"
Cohesion: 1.0
Nodes (0): 

### Community 112 - "Community 112"
Cohesion: 1.0
Nodes (0): 

### Community 113 - "Community 113"
Cohesion: 1.0
Nodes (0): 

### Community 114 - "Community 114"
Cohesion: 1.0
Nodes (0): 

### Community 115 - "Community 115"
Cohesion: 1.0
Nodes (0): 

### Community 116 - "Community 116"
Cohesion: 1.0
Nodes (0): 

### Community 117 - "Community 117"
Cohesion: 1.0
Nodes (0): 

### Community 118 - "Community 118"
Cohesion: 1.0
Nodes (0): 

### Community 119 - "Community 119"
Cohesion: 1.0
Nodes (0): 

### Community 120 - "Community 120"
Cohesion: 1.0
Nodes (0): 

### Community 121 - "Community 121"
Cohesion: 1.0
Nodes (0): 

### Community 122 - "Community 122"
Cohesion: 1.0
Nodes (0): 

### Community 123 - "Community 123"
Cohesion: 1.0
Nodes (0): 

### Community 124 - "Community 124"
Cohesion: 1.0
Nodes (0): 

### Community 125 - "Community 125"
Cohesion: 1.0
Nodes (0): 

### Community 126 - "Community 126"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **645 isolated node(s):** `ai_engine.py — AI-Powered Vedic Astrology Interpretation Engine ================`, `Detect which AI provider to use. Priority: explicit > gemini > openai.`, `Lazy provider detection — re-reads config each time until a provider is found.`, `Call Google Gemini API via raw HTTP (no SDK dependency).`, `Call OpenAI chat completion API via raw HTTP (no SDK dependency).` (+640 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 76`** (2 nodes): `index.ts`, `Vercel serverless entry point — exposes the FastAPI app.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 77`** (2 nodes): `__init__.py`, `Route registry — import all routers for inclusion in the FastAPI app.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 78`** (2 nodes): `data.py`, `vastu/data.py — Complete Vastu Shastra Reference Data ==========================`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 79`** (2 nodes): `analyze-i18n.js`, `walk()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 80`** (2 nodes): `connection.js`, `testConnection()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 81`** (2 nodes): `predictions.js`, `auth()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 82`** (2 nodes): `remedies.js`, `auth()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 83`** (2 nodes): `KundliChart.jsx`, `KundliChart()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 84`** (1 nodes): `stress_test.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 85`** (1 nodes): `ui-test.spec.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 86`** (1 nodes): `tailwind.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 87`** (1 nodes): `playwright.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 88`** (1 nodes): `vite.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 89`** (1 nodes): `postcss.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 90`** (1 nodes): `palette-CXiXSgC5.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 91`** (1 nodes): `house-DtiC-4UK.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 92`** (1 nodes): `hash-CicP2k4H.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 93`** (1 nodes): `sun-BzBhZV-E.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 94`** (1 nodes): `zap-CAEtoi2h.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 95`** (1 nodes): `circle-alert-C7OzIryt.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 96`** (1 nodes): `circle-check-big-C2G1rGUt.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 97`** (1 nodes): `plus-0BNEFBy0.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 98`** (1 nodes): `activity-X4r3g2MZ.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 99`** (1 nodes): `info-CrU8AAHX.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 100`** (1 nodes): `chevron-left-De_SGD7e.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 101`** (1 nodes): `search-B7V9CMzU.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 102`** (1 nodes): `chevron-up-oUmfnrAD.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 103`** (1 nodes): `navigation-KikWBpYy.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 104`** (1 nodes): `arrow-left-B1R7J2oO.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 105`** (1 nodes): `save-CurQzcRD.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 106`** (1 nodes): `circle-check-CgXHvHNa.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 107`** (1 nodes): `calendar-BAWu2H0T.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 108`** (1 nodes): `eye-CP953dOK.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 109`** (1 nodes): `map-pin-4ZjEbj4U.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 110`** (1 nodes): `orbit-BJqvfdpJ.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 111`** (1 nodes): `briefcase-CKH9P3l8.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 112`** (1 nodes): `rotate-ccw-DKeW6YZS.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 113`** (1 nodes): `clock-BmMvehyB.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 114`** (1 nodes): `chevron-right-BX36YS4o.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 115`** (1 nodes): `send-DBV8maWO.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 116`** (1 nodes): `trending-up-D6lZAkWG.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 117`** (1 nodes): `triangle-alert-Djnuq5R0.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 118`** (1 nodes): `book-open-DsqoyRev.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 119`** (1 nodes): `loader-circle-DHqOI4NW.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 120`** (1 nodes): `wallet-Wc7AxNdH.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 121`** (1 nodes): `shield-check-CeboXS6O.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 122`** (1 nodes): `sticky-note-Dh-n4DfT.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 123`** (1 nodes): `arrow-right-Dg-Z4lpq.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 124`** (1 nodes): `wxLogin.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 125`** (1 nodes): `server.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 126`** (1 nodes): `aspect-ratio.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `js()` connect `Community 2` to `Community 32`, `Community 6`, `Community 13`, `Community 16`, `Community 48`, `Community 58`, `Community 59`, `Community 30`, `Community 63`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Why does `KundliRequest` connect `Community 7` to `Community 4`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Why does `KundliMatchRequest` connect `Community 7` to `Community 4`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `KundliRequest` (e.g. with `Kundli routes — generate, retrieve, list, iogita analysis, match, dosha, dasha,` and `Geocode a place name using the free Nominatim OpenStreetMap API.`) actually correct?**
  _`KundliRequest` has 38 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ai_engine.py — AI-Powered Vedic Astrology Interpretation Engine ================`, `Detect which AI provider to use. Priority: explicit > gemini > openai.`, `Lazy provider detection — re-reads config each time until a provider is found.` to the rest of the system?**
  _645 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.01 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.01 - nodes in this community are weakly interconnected._