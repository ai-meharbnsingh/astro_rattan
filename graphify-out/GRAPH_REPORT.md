# Graph Report - .  (2026-04-14)

## Corpus Check
- 240 files · ~2,780,406 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2161 nodes · 3290 edges · 76 communities detected
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 307 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `KundliRequest` - 40 edges
2. `KundliMatchRequest` - 40 edges
3. `DivisionalChartRequest` - 40 edges
4. `analyze_yogas_and_doshas()` - 36 edges
5. `_fetch_kundli()` - 29 edges
6. `_h()` - 25 edges
7. `_chart_data()` - 24 edges
8. `calculate_panchang()` - 23 edges
9. `SendOtpRequest` - 18 edges
10. `VerifyOtpRequest` - 18 edges

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
Cohesion: 0.02
Nodes (27): apiFetch(), fetchWithRetry(), friendlyError(), tryRefreshToken(), detectDoshas(), generateLalKitabChart(), getHouseStrength(), markDayDone() (+19 more)

### Community 1 - "Community 1"
Cohesion: 0.03
Nodes (125): get_live_dashboard(), get_stats(), get_user_detail(), list_all_kundlis(), list_users(), Admin routes — user management, stats, kundli overview, live traffic panel., Change a user's role (user/astrologer/admin)., Activate or deactivate a user account. (+117 more)

### Community 2 - "Community 2"
Cohesion: 0.01
Nodes (141): Tests for app.vastu — Vastu Shastra engine calculations., Residential buildings must use Manduka Mandala (8x8 = 64 squares)., Temple buildings must use Paramasayika Mandala (9x9 = 81 squares)., Mandala must return all 10 zones with devtas., Energy balance positive + negative + neutral must equal 45., Body mapping must include head, face, chest, navel, arms, legs, feet., Each devta must have a unique id from 1 to 45., In a balanced mandala, positive devtas must outnumber negative ones. (+133 more)

### Community 3 - "Community 3"
Cohesion: 0.02
Nodes (25): rotateByLagna(), SAVKundliChart(), compactAsciiKey(), escapeRegExp(), normalizeIdLike(), normalizeKey(), resolveTranslationId(), translateBackend() (+17 more)

### Community 4 - "Community 4"
Cohesion: 0.03
Nodes (39): isInTimeRange(), toMinutes(), getTypeBucket(), isInTimeRange(), renderRow(), toMinutes(), isDayStart(), isInTimeRange() (+31 more)

### Community 5 - "Community 5"
Cohesion: 0.03
Nodes (5): handleOtpKeyDown(), handleResendOtp(), handleSendOtp(), handleVerifyOtp(), startCountdown()

### Community 6 - "Community 6"
Cohesion: 0.07
Nodes (80): _build_kundli_pdf(), _chart_data(), check_doshas(), _compute_dasha(), delete_all_my_kundlis(), delete_kundli(), download_full_report(), download_kundli_pdf() (+72 more)

### Community 7 - "Community 7"
Cohesion: 0.05
Nodes (81): analyze_yogas_and_doshas(), check_adhi_yoga(), check_amala_yoga(), check_anapha_yoga(), check_angarak_dosha(), check_budhaditya_yoga(), check_chandra_mangal_yoga(), check_danda_yoga() (+73 more)

### Community 8 - "Community 8"
Cohesion: 0.03
Nodes (45): auth_headers(), auth_token(), client(), Route-level tests for /api/kundli/* endpoints.  Uses FastAPI TestClient with a f, POST /api/kundli/generate → 201, returns chart_data with 9 planets., POST /api/kundli/generate with invalid date → 422 or 500., POST /api/kundli/generate without auth → 401., POST /api/kundli/generate with missing required fields → 422. (+37 more)

### Community 9 - "Community 9"
Cohesion: 0.06
Nodes (61): _approx_sunrise_sunset(), calculate_abhijit_muhurat(), calculate_brahma_muhurat(), calculate_choghadiya(), calculate_gulika_kaal(), calculate_night_choghadiya(), calculate_panchang(), calculate_planetary_positions() (+53 more)

### Community 10 - "Community 10"
Cohesion: 0.05
Nodes (53): _abda_bala(), _angular_distance(), _aspect_strength(), _ayana_bala(), calculate_bhav_bala(), calculate_shadbala(), _cheshta_bala(), _dig_bala() (+45 more)

### Community 11 - "Community 11"
Cohesion: 0.07
Nodes (51): analyze_name_numerology(), _build_number_affinities(), _build_pair_combination_table(), _calculate_house_compatibility(), calculate_house_numerology(), calculate_mobile_numerology(), calculate_numerology(), calculate_vehicle_numerology() (+43 more)

### Community 12 - "Community 12"
Cohesion: 0.06
Nodes (39): build_full_report(), _build_planets_in_houses(), _compound_relation(), _display(), _draw_north_indian_chart(), _find_hindi_font(), _fmt_date(), _fmt_num() (+31 more)

### Community 13 - "Community 13"
Cohesion: 0.07
Nodes (37): get_db(), _get_pool(), _get_valid_conn(), init_db(), migrate_forum_tables(), migrate_gamification_tables(), migrate_notification_tables(), migrate_referral_tables() (+29 more)

### Community 14 - "Community 14"
Cohesion: 0.05
Nodes (45): add_chandra_journal(), add_tracker_journal(), delete_saved_prediction(), get_chandra_state(), get_gochar_transits(), get_lalkitab_advanced(), get_nishaniyan(), _get_planet_positions() (+37 more)

### Community 15 - "Community 15"
Cohesion: 0.06
Nodes (43): _assess_remedy_accessibility(), _calculate_d10(), calculate_d10_dasamsa(), _calculate_d12(), _calculate_d2(), _calculate_d3(), _calculate_d30(), _calculate_d4() (+35 more)

### Community 16 - "Community 16"
Cohesion: 0.05
Nodes (15): Tests for app.panchang_engine -- Vedic Panchang Calculator., Test Rahu Kaal calculation., Monday Rahu Kaal: slot 2 of 8 (equal day)., Sunday Rahu Kaal: slot 8 of 8., Validate TITHIS constant data., Rahu Kaal must be between sunrise and sunset., Test Choghadiya calculation., First period starts at sunrise, last ends at sunset. (+7 more)

### Community 17 - "Community 17"
Cohesion: 0.05
Nodes (11): Smoke tests for critical engine modules: varshphal, transit, astro_iogita, dasha, Smoke tests for transit_engine.py., Smoke tests for astro_iogita_engine.py., Smoke tests for dasha_engine.py., Design change: dasha now covers 2 full 120-year cycles = 240 years total., When moon_longitude is given, first dasha balance is partial.          Design ch, Smoke tests for varshphal_engine.py., TestAstroIogitaEngine (+3 more)

### Community 18 - "Community 18"
Cohesion: 0.08
Nodes (37): _analyze_houses(), _angular_distance(), _build_summary(), calculate_eclipses(), calculate_ingress(), calculate_mundane_analysis(), _conflict_indicators(), _current_transits_in_country_chart() (+29 more)

### Community 19 - "Community 19"
Cohesion: 0.05
Nodes (16): Tests for app.kp_engine -- Krishnamurti Paddhati Engine., Validate Vimshottari Dasha constants., Validate the pre-built KP sub-lord table., Must have 27 nakshatras * 9 subs = 243 entries., First entry starts at 0, last entry ends at ~360., Each entry's end should equal the next entry's start., First nakshatra (Ashwini) lord is Ketu., Ashwini's first sub = its own lord (Ketu). (+8 more)

### Community 20 - "Community 20"
Cohesion: 0.1
Nodes (35): _approx_ascendant(), _approx_ayanamsa(), _approx_moon_longitude(), _approx_planet_longitude(), _approx_rahu_longitude(), _approx_sun_longitude(), _build_status(), _calculate_fallback() (+27 more)

### Community 21 - "Community 21"
Cohesion: 0.09
Nodes (35): analyze_entrance(), analyze_home_layout(), _build_entrance_result(), _build_room_remedies(), calculate_mandala(), _calculate_vastu_score(), _degrees_to_direction(), _direction_to_pada_index() (+27 more)

### Community 22 - "Community 22"
Cohesion: 0.09
Nodes (31): ai_ask_question(), ai_gita_answer(), ai_interpret_kundli(), ai_oracle(), ai_remedies(), _call_ai(), _call_gemini(), _call_openai() (+23 more)

### Community 23 - "Community 23"
Cohesion: 0.07
Nodes (31): analyze_masnui_transits(), calculate_hora_lord(), calculate_karmic_debts(), calculate_karmic_debts_with_hora(), calculate_kayam_grah(), calculate_lk_aspects(), calculate_masnui_planets(), _calculate_masnui_psychological_profile() (+23 more)

### Community 24 - "Community 24"
Cohesion: 0.13
Nodes (30): calculate_argala(), calculate_chara_dasha(), calculate_chara_karakas(), calculate_indu_lagna(), calculate_jaimini(), calculate_jaimini_drishti(), calculate_jaimini_yogas(), calculate_longevity() (+22 more)

### Community 25 - "Community 25"
Cohesion: 0.09
Nodes (22): calculate_gun_milan(), _normalize_nakshatra(), _rashi_lord(), matching_engine.py — Kundli Gun Milan (Ashtakoota) Matching Engine =============, Varna koot: groom's varna should be >= bride's. Max 1 point., Vasya koot: mutual influence/attraction based on Moon rashi. Max 2 points., Tara koot: based on nakshatra distance (bidirectional). Max 3 points.     Standa, Yoni koot: sexual/physical compatibility. Max 4 points.     Same=4, Friendly=3, (+14 more)

### Community 26 - "Community 26"
Cohesion: 0.14
Nodes (19): _atom(), build_atom_vector(), _generate_iogita_insight(), _generate_normal_insights(), _get_dignity_label(), get_planet_strength(), identify_basin(), _print_report() (+11 more)

### Community 27 - "Community 27"
Cohesion: 0.14
Nodes (19): _build_kp_sub_lords(), calculate_kp_cuspal(), _find_house_for_planet(), _find_vimshottari_index(), _get_houses_owned(), get_star_lord_of_sub_lord(), get_sub_lord(), get_sub_sub_lord() (+11 more)

### Community 28 - "Community 28"
Cohesion: 0.12
Nodes (19): _build_ai_horoscope_prompt(), generate_ai_horoscope(), generate_daily_horoscopes(), _generate_template_horoscope(), _get_current_transits(), _parse_ai_sections(), H-09: Horoscope Content Generation Pipeline — seeds daily & weekly horoscopes., Calculate today's planetary positions (signs) for horoscope weighting. (+11 more)

### Community 29 - "Community 29"
Cohesion: 0.13
Nodes (15): BaseHTTPMiddleware, _extract_user_id(), get_traffic_snapshot(), H-01: Structured Logging Middleware — logs every request with method, path, stat, Extract user_id from JWT Bearer token if present., Middleware that logs every HTTP request and records to the live traffic buffer., Return a snapshot of recent traffic for the live admin dashboard.     Thread-saf, RequestLoggingMiddleware (+7 more)

### Community 30 - "Community 30"
Cohesion: 0.16
Nodes (17): cleanup_old_uploads(), ensure_upload_dir(), map_room_placements(), _optimize_image(), pixel_to_direction(), vastu/floorplan.py — Floor Plan Upload & Pixel-to-Direction Mapper =============, Resize large images and compress to JPEG for storage efficiency.     Returns opt, Validate, optimize, and save uploaded floor plan image.      Returns:         di (+9 more)

### Community 31 - "Community 31"
Cohesion: 0.2
Nodes (12): enrichDayFestivals(), fetchMonthly(), generateObservances(), getDayMarkers(), getFestivalTone(), getLocalDateString(), hasKeyword(), mergeMonthlyFestivalDetails() (+4 more)

### Community 32 - "Community 32"
Cohesion: 0.11
Nodes (17): Tests for numerology_engine.py — Pythagorean numerology calculations., Verify master number 11 is preserved (not reduced to 2)., Destiny number (formerly expression) uses all letters of the name., Soul urge uses only vowels (A, E, I, O, U)., Personality uses only consonants., Verify all required keys are present in the output dict., Life path for 1990-01-15: 1+9+9+0=19->10->1 + 0+1=1 + 1+5=6 => 1+1+6=8., Master numbers 11, 22, 33 should not be reduced further. (+9 more)

### Community 33 - "Community 33"
Cohesion: 0.17
Nodes (15): calculate_mudda_dasha(), calculate_muntha(), calculate_varshphal(), calculate_year_lord(), find_solar_return_jd(), _jd_to_datetime(), varshphal_engine.py — Vedic Varshphal (Solar Return / Tajaka) Engine ===========, Muntha advances one sign per year from natal ascendant.     Returns: {sign, sign (+7 more)

### Community 34 - "Community 34"
Cohesion: 0.2
Nodes (15): _build_antardasha_periods(), _build_pratyantar_periods(), calculate_dasha(), _calculate_dasha_balance(), calculate_extended_dasha(), _get_dasha_sequence(), _parse_date(), dasha_engine.py — Vimshottari Dasha Calculation Engine ========================= (+7 more)

### Community 35 - "Community 35"
Cohesion: 0.13
Nodes (13): _bootstrap_db(), client(), _create_kundli(), db(), _make_admin(), _make_astrologer(), Shared test fixtures — temp DB, TestClient, auth helpers.  Every test module get, Insert a minimal kundli record and return its id. (+5 more)

### Community 36 - "Community 36"
Cohesion: 0.21
Nodes (13): _binary_search_station(), calculate_retrograde_stations(), _get_longitude(), _get_speed(), _jd_to_date(), _jd_to_datetime(), retrograde_engine.py — Planetary Retrograde Station Calculator =================, Convert Julian Day to YYYY-MM-DD string. (+5 more)

### Community 37 - "Community 37"
Cohesion: 0.2
Nodes (13): calculate_avakhada(), _get_gana(), _get_nadi(), _get_nakshatra_index(), _get_pada(), _get_western_sign(), avakhada_engine.py — Avakhada Chakra Calculation Engine ========================, Get nakshatra index (0-26) from sidereal longitude. (+5 more)

### Community 38 - "Community 38"
Cohesion: 0.2
Nodes (13): auto_detect_rooms(), _detect_ocr_labels(), _detect_opencv(), _detect_yolo(), _match_room(), _preprocess_for_ocr(), vastu/auto_detect.py — AI Room Detection for Floor Plans =======================, Preprocess floor plan for OCR: grayscale → upscale 2x → sharpen → binarize. (+5 more)

### Community 39 - "Community 39"
Cohesion: 0.22
Nodes (13): get_all_signs_horoscope(), get_daily_horoscope(), get_transit_insights(), get_weekly_horoscope(), _parse_content_to_sections(), Horoscope routes — daily, weekly, all-signs, and transit-aware horoscopes., Get weekly horoscope for a specific sign., Get horoscopes for all 12 signs at once. (+5 more)

### Community 40 - "Community 40"
Cohesion: 0.14
Nodes (13): Tests for lalkitab_engine.py — Lal Kitab remedies engine., Each planet should have 5-8 remedies., A debilitated planet (strength < 0.5) should receive remedies., An exalted planet (strength >= 0.5) should NOT receive remedies., A planet in enemy sign (strength 0.35 < 0.5) should receive remedies., Verify the output dict structure for each planet., REMEDIES dict must cover all 9 Vedic planets., test_enemy_planet_gets_remedies() (+5 more)

### Community 41 - "Community 41"
Cohesion: 0.18
Nodes (12): calculate_aspects(), calculate_cusp_aspects(), calculate_western_aspects(), _get_aspected_houses(), _match_western_aspect(), aspects_engine.py -- Vedic Planetary Aspects Calculator ========================, Calculate degree-based Western aspects between all planet pairs.      Returns a, Find the Western aspect matching a given degree difference, if any. (+4 more)

### Community 42 - "Community 42"
Cohesion: 0.23
Nodes (11): _apply_ekadhipatya_shodhana(), _apply_trikona_shodhana(), calculate_ashtakvarga(), _calculate_shodhya_pinda(), ashtakvarga_engine.py -- Ashtakvarga Calculation Engine ========================, Convert sign name to 0-based index., Calculate the Ashtakvarga system for a given chart.     Includes Trikona Shodhan, Reduces bindus in trine signs.     Trines: (0,4,8), (1,5,9), (2,6,10), (3,7,11) (+3 more)

### Community 43 - "Community 43"
Cohesion: 0.23
Nodes (11): calculate_baladi(), calculate_deeptadi(), calculate_jagradadi(), calculate_shyanadi(), get_all_avasthas(), interpretations.py -- Static Text Databases for Kundli Report ==================, Jagradadi Avastha (3 states):     - Jagrad (Awake): planet in own sign or exalte, Baladi Avastha (5 states based on degree within sign):     Odd signs: Bala(0-6), (+3 more)

### Community 44 - "Community 44"
Cohesion: 0.27
Nodes (9): calculate_transit_forecast(), calculate_transits(), _check_sade_sati(), _house_from_moon(), transit_engine.py -- Gochara (Transit) Prediction Engine =======================, Calculate planetary transits and their Gochara effects on a natal chart., Calculate transit intensity scores for the next N days., Return the house number (1-12) of transit_sign counted from moon_sign.     House (+1 more)

### Community 45 - "Community 45"
Cohesion: 0.2
Nodes (9): get_eclipses(), get_ingress(), get_mundane_analysis(), list_countries(), Mundane Astrology routes — country charts, national analysis, eclipses, ingress., Return the dates when the Sun enters each of the 12 sidereal signs     (Sankrant, Return the list of available country charts for mundane analysis., Full mundane astrology analysis for a country: birth chart, current transits, (+1 more)

### Community 46 - "Community 46"
Cohesion: 0.22
Nodes (1): RED phase: auth tests.

### Community 47 - "Community 47"
Cohesion: 0.36
Nodes (7): _is_auspicious_day(), _monthly_days(), muhurat_find(), muhurat_monthly(), Compatibility muhurat routes used by frontend widgets., Monthly calendar-style muhurat compatibility endpoint., Daily window compatibility endpoint for a selected date.

### Community 48 - "Community 48"
Cohesion: 0.57
Nodes (7): createClientsViaAPI(), fillBirthForm(), injectAuth(), main(), screenshot(), sleep(), waitForChart()

### Community 49 - "Community 49"
Cohesion: 0.29
Nodes (6): get_analytics(), HitPayload, Analytics routes — lightweight page-view tracking and admin reporting., Record a single page view from the frontend SPA.     No auth required — called c, Aggregated traffic analytics for the admin panel., record_hit()

### Community 50 - "Community 50"
Cohesion: 0.4
Nodes (5): _get_dignity_label(), get_remedies(), lalkitab_engine.py — Lal Kitab Remedies Engine =================================, Determine dignity label for a planet in a sign., Get Lal Kitab remedies for weak or afflicted planets.      Args:         planet_

### Community 51 - "Community 51"
Cohesion: 0.4
Nodes (5): calculate_sodashvarga(), _get_dignity(), sodashvarga_engine.py -- Sodashvarga (16 Divisional Charts) Summary & Vimshopak, Determine the dignity of a planet in a given sign., Calculate Sodashvarga for all planets.      Args:         planet_longitudes: {pl

### Community 52 - "Community 52"
Cohesion: 0.47
Nodes (5): ai_interpret(), _compose_interpretation(), _normalize_period(), AI interpretation routes for kundli predictions., Return AI-style period prediction for a saved kundli.

### Community 53 - "Community 53"
Cohesion: 0.4
Nodes (3): _env_first(), Application configuration — loaded from environment variables with defaults., Return the first non-empty environment variable from the given names.

### Community 54 - "Community 54"
Cohesion: 0.5
Nodes (3): calculate_nadi_insights(), nadi_engine.py -- Nadi Astrology Interpretive Engine ===========================, Identify Nadi shlokas / yogas based on planet placements in the same house.

### Community 55 - "Community 55"
Cohesion: 0.5
Nodes (3): detect_festivals(), festival_engine.py -- Rule-Based Hindu Festival & Vrat Detection Engine ========, Detect festivals and vrats for given panchang elements.      Checks all three so

### Community 56 - "Community 56"
Cohesion: 0.67
Nodes (3): calculate_yogini_dasha(), get_starting_yogini(), Calculate Yogini Dasha periods. Returns periods for up to 108 years (3 cycles).

### Community 57 - "Community 57"
Cohesion: 0.5
Nodes (3): Shared rate-limit helpers., Scope rate limits to the active test DB and client address., request_rate_limit_key()

### Community 58 - "Community 58"
Cohesion: 0.67
Nodes (2): calculate_lifelong_sade_sati(), Calculate lifelong Sade Sati, Dhaiya (Ashtamesh/Kantak), and Panauti phases.

### Community 59 - "Community 59"
Cohesion: 0.67
Nodes (2): calculate_upagrahas(), Calculate Upagrahas (sub-planets) including Aprakasha Grahas and Kala Velas.

### Community 60 - "Community 60"
Cohesion: 1.0
Nodes (1): Vercel serverless entry point — exposes the FastAPI app.

### Community 61 - "Community 61"
Cohesion: 1.0
Nodes (1): Route registry — import all routers for inclusion in the FastAPI app.

### Community 62 - "Community 62"
Cohesion: 1.0
Nodes (1): vastu/data.py — Complete Vastu Shastra Reference Data ==========================

### Community 63 - "Community 63"
Cohesion: 1.0
Nodes (0): 

### Community 64 - "Community 64"
Cohesion: 1.0
Nodes (0): 

### Community 65 - "Community 65"
Cohesion: 1.0
Nodes (0): 

### Community 66 - "Community 66"
Cohesion: 1.0
Nodes (0): 

### Community 67 - "Community 67"
Cohesion: 1.0
Nodes (0): 

### Community 68 - "Community 68"
Cohesion: 1.0
Nodes (0): 

### Community 69 - "Community 69"
Cohesion: 1.0
Nodes (0): 

### Community 70 - "Community 70"
Cohesion: 1.0
Nodes (0): 

### Community 71 - "Community 71"
Cohesion: 1.0
Nodes (0): 

### Community 72 - "Community 72"
Cohesion: 1.0
Nodes (0): 

### Community 73 - "Community 73"
Cohesion: 1.0
Nodes (0): 

### Community 74 - "Community 74"
Cohesion: 1.0
Nodes (0): 

### Community 75 - "Community 75"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **645 isolated node(s):** `ai_engine.py — AI-Powered Vedic Astrology Interpretation Engine ================`, `Detect which AI provider to use. Priority: explicit > gemini > openai.`, `Lazy provider detection — re-reads config each time until a provider is found.`, `Call Google Gemini API via raw HTTP (no SDK dependency).`, `Call OpenAI chat completion API via raw HTTP (no SDK dependency).` (+640 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 60`** (2 nodes): `index.ts`, `Vercel serverless entry point — exposes the FastAPI app.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 61`** (2 nodes): `__init__.py`, `Route registry — import all routers for inclusion in the FastAPI app.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 62`** (2 nodes): `data.py`, `vastu/data.py — Complete Vastu Shastra Reference Data ==========================`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 63`** (2 nodes): `analyze-i18n.js`, `walk()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 64`** (2 nodes): `connection.js`, `testConnection()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 65`** (2 nodes): `predictions.js`, `auth()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 66`** (2 nodes): `remedies.js`, `auth()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 67`** (2 nodes): `KundliChart.jsx`, `KundliChart()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 68`** (1 nodes): `stress_test.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 69`** (1 nodes): `ui-test.spec.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 70`** (1 nodes): `tailwind.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 71`** (1 nodes): `playwright.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 72`** (1 nodes): `vite.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 73`** (1 nodes): `postcss.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 74`** (1 nodes): `server.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 75`** (1 nodes): `aspect-ratio.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `KundliRequest` connect `Community 6` to `Community 1`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Why does `KundliMatchRequest` connect `Community 6` to `Community 1`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Why does `DivisionalChartRequest` connect `Community 6` to `Community 1`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `KundliRequest` (e.g. with `Kundli routes — generate, retrieve, list, iogita analysis, match, dosha, dasha,` and `Geocode a place name using the free Nominatim OpenStreetMap API.`) actually correct?**
  _`KundliRequest` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 38 inferred relationships involving `KundliMatchRequest` (e.g. with `Kundli routes — generate, retrieve, list, iogita analysis, match, dosha, dasha,` and `Geocode a place name using the free Nominatim OpenStreetMap API.`) actually correct?**
  _`KundliMatchRequest` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 38 inferred relationships involving `DivisionalChartRequest` (e.g. with `Kundli routes — generate, retrieve, list, iogita analysis, match, dosha, dasha,` and `Geocode a place name using the free Nominatim OpenStreetMap API.`) actually correct?**
  _`DivisionalChartRequest` has 38 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ai_engine.py — AI-Powered Vedic Astrology Interpretation Engine ================`, `Detect which AI provider to use. Priority: explicit > gemini > openai.`, `Lazy provider detection — re-reads config each time until a provider is found.` to the rest of the system?**
  _645 weakly-connected nodes found - possible documentation gaps or missing edges._