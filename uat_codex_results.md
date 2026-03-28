OpenAI Codex v0.116.0 (research preview)
--------
workdir: /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app
model: gpt-5.3-codex
provider: openai
approval: never
sandbox: read-only
reasoning effort: medium
reasoning summaries: none
session id: 019d33ad-6629-7992-be3c-7b4939c065d1
--------
user
You are a BRUTAL astrology calculation verifier. Read these backend engine files and verify every calculation is mathematically correct: app/astro_engine.py, app/dasha_engine.py, app/ashtakvarga_engine.py, app/shadbala_engine.py, app/avakhada_engine.py, app/divisional_charts.py, app/transit_engine.py, app/kp_engine.py, app/dosha_engine.py. For each file rate CORRECT/INCORRECT/PARTIALLY CORRECT with specific errors and line numbers. Give final verdict on production readiness.
mcp startup: no servers
codex
I’m going to do a strict code-level verification of each listed engine file, checking formulas and edge-case math line by line, then I’ll return per-file verdicts with exact line references and a production-readiness conclusion. I’ll start by loading all nine files with line numbers.
exec
/bin/zsh -lc "nl -ba app/astro_engine.py | sed -n '1,260p'" in /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app succeeded in 0ms:
     1	"""
     2	astro_engine.py -- Vedic Astrology Planetary Calculation Engine
     3	===============================================================
     4	Wrapper around Swiss Ephemeris (swisseph). Falls back to pure-math
     5	approximations when swisseph is not installed.
     6	
     7	Provides:
     8	  - ZODIAC_SIGNS, PLANETS, NAKSHATRAS data tables
     9	  - calculate_planet_positions(birth_date, birth_time, lat, lon, tz_offset)
    10	  - get_sign_from_longitude(longitude)
    11	  - get_nakshatra_from_longitude(longitude)
    12	"""
    13	from __future__ import annotations
    14	
    15	import math
    16	from datetime import datetime, timedelta, timezone
    17	from typing import Any, Dict, List, Optional, Tuple
    18	
    19	# ---------- Try to import Swiss Ephemeris ----------
    20	try:
exec
/bin/zsh -lc "nl -ba app/dasha_engine.py | sed -n '1,260p'" in /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_appexec
/bin/zsh -lc "nl -ba app/ashtakvarga_engine.py | sed -n '1,260p'" in /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app succeeded in 0ms:
     1	"""
     2	dasha_engine.py — Vimshottari Dasha Calculation Engine
     3	=======================================================
     4	Computes Mahadasha, Antardasha, and Pratyantar Dasha periods based on
     5	birth nakshatra. Vimshottari total = 120 years. Order starts from birth
     6	nakshatra lord.
     7	"""
     8	from datetime import datetime, timedelta
     9	
    10	
    11	# ============================================================
    12	# CONSTANTS
    13	# ============================================================
    14	
    15	# Planet -> years in Vimshottari Dasha system (total = 120)
    16	DASHA_YEARS = {
    17	    "Ketu": 7,
    18	    "Venus": 20,
    19	    "Sun": 6,
    20	    "Moon": 10,
 succeeded in 0ms:
     1	"""
     2	ashtakvarga_engine.py -- Ashtakvarga Calculation Engine
     3	========================================================
     4	Calculates the Ashtakvarga point system used in Vedic astrology for
     5	transit predictions. Each planet gets 0 or 1 point (bindu) from each
     6	of the 7 contributing planets + Ascendant for each of the 12 signs.
     7	
     8	The Sarvashtakvarga is the sum of all individual planet ashtakvargas.
     9	"""
    10	from __future__ import annotations
    11	
    12	from typing import Any, Dict, List, Set
    13	
    14	# Sign names
    15	_SIGN_NAMES = [
    16	    "Aries", "Taurus", "Gemini", "Cancer",
    17	    "Leo", "Virgo", "Libra", "Scorpio",
    18	    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
    19	]
    20	
codex
I’ve loaded the first three files and now I’m pulling the remaining sections plus the other six engines so I can validate full formulas, not just top-level APIs.
exec
/bin/zsh -lc "nl -ba app/dasha_engine.py | sed -n '261,520p'" in /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_appexec
/bin/zsh -lc "nl -ba app/shadbala_engine.py | sed -n '1,320p'" in /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_appexec
/bin/zsh -lc "nl -ba app/astro_engine.py | sed -n '261,520p'" in /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app succeeded in 0ms:
   261	    birth_dt = _parse_date(birth_date)
   262	    now = datetime.now()
   263	
   264	    mahadasha_list = []
   265	    current_start = birth_dt
   266	    current_dasha = "Unknown"
   267	    current_antardasha = "Unknown"
   268	    current_pratyantar = "Unknown"
   269	
   270	    for planet in sequence:
   271	        years = DASHA_YEARS[planet]
   272	        end_dt = current_start + timedelta(days=years * 365.25)
   273	        is_current = (current_start <= now <= end_dt)
   274	
   275	        if is_current:
   276	            current_dasha = planet
   277	
   278	        # Build antardasha for every mahadasha (but pratyantar only for current)
   279	        antardasha = _build_antardasha_periods(
   280	            planet, years, current_start, now
 succeeded in 0ms:
     1	"""
     2	shadbala_engine.py -- Shadbala (Six-fold Strength) Calculator
     3	=============================================================
     4	Calculates the six components of planetary strength in Vedic astrology:
     5	  1. Sthana Bala (Positional Strength)
     6	  2. Dig Bala (Directional Strength)
     7	  3. Kala Bala (Temporal Strength)
     8	  4. Cheshta Bala (Motional Strength)
     9	  5. Naisargika Bala (Natural Strength)
    10	  6. Drik Bala (Aspectual Strength)
    11	
    12	Total Shadbala = sum of all six. Compared against minimum required (Rupas).
    13	"""
    14	from __future__ import annotations
    15	
    16	from typing import Any, Dict
    17	
    18	# Sign names
    19	_SIGN_NAMES = [
    20	    "Aries", "Taurus", "Gemini", "Cancer",
 succeeded in 0ms:
   261	        house = _find_house(sid_lon, [h["degree"] for h in houses])
   262	
   263	        # Retrograde: negative daily speed means the planet appears to move backward
   264	        # Rahu (mean node) is always retrograde by nature
   265	        is_retrograde = daily_speed < 0 or pname == "Rahu"
   266	
   267	        planets_result[pname] = {
   268	            "longitude": round(sid_lon, 4),
   269	            "sign": sign,
   270	            "sign_degree": round(sign_deg, 4),
   271	            "nakshatra": nak["name"],
   272	            "nakshatra_pada": nak["pada"],
   273	            "house": house,
   274	            "retrograde": is_retrograde,
   275	            "status": _build_status(pname, sign, is_retrograde),
   276	        }
   277	
   278	    # Ketu = Rahu + 180  (Ketu is always retrograde)
   279	    rahu_lon = planets_result["Rahu"]["longitude"]
   280	    ketu_lon = (rahu_lon + 180.0) % 360.0
codex
Next I’m checking the remaining engines and the tail of `astro_engine.py` for helper math (`_find_house`, status/exaltation logic), because those often hide boundary bugs.
exec
/bin/zsh -lc "nl -ba app/astro_engine.py | sed -n '520,760p'" in /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app succeeded in 0ms:
   520	# ============================================================
   521	# INTERNAL: Planetary dignity & status
   522	# ============================================================
   523	
   524	# Exaltation signs for each planet
   525	_EXALTATION_SIGN: Dict[str, str] = {
   526	    "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn",
   527	    "Mercury": "Virgo", "Jupiter": "Cancer", "Venus": "Pisces",
   528	    "Saturn": "Libra", "Rahu": "Gemini", "Ketu": "Sagittarius",
   529	}
   530	
   531	# Debilitation signs (opposite of exaltation)
   532	_DEBILITATION_SIGN: Dict[str, str] = {
   533	    "Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer",
   534	    "Mercury": "Pisces", "Jupiter": "Capricorn", "Venus": "Virgo",
   535	    "Saturn": "Aries", "Rahu": "Sagittarius", "Ketu": "Gemini",
   536	}
   537	
   538	# Own signs (Moolatrikona / Swakshetra)
   539	_OWN_SIGN: Dict[str, List[str]] = {
exec
/bin/zsh -lc "nl -ba app/avakhada_engine.py | sed -n '1,320p'" in /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app succeeded in 0ms:
     1	"""
     2	avakhada_engine.py — Avakhada Chakra Calculation Engine
     3	========================================================
     4	Computes the comprehensive birth summary table (Avakhada Chakra)
     5	from chart data: ascendant, Moon position, Sun position, and planet data.
     6	"""
     7	import math
     8	from typing import Any, Dict, List, Optional
     9	
    10	# ============================================================
    11	# CONSTANTS
    12	# ============================================================
    13	
    14	ZODIAC_SIGNS = [
    15	    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    16	    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
    17	]
    18	
    19	# Sign lords (traditional Vedic rulerships)
    20	SIGN_LORD = {
exec
/bin/zsh -lc "nl -ba app/divisional_charts.py | sed -n '1,360p'" in /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app succeeded in 0ms:
     1	"""
     2	divisional_charts.py -- Vedic Divisional Chart Calculator
     3	==========================================================
     4	Calculates divisional (varga) charts used in Vedic astrology.
     5	Supports all 16 standard divisional charts: D1 through D60.
     6	
     7	Each divisional chart maps a planet's longitude in the Rasi (D1) chart
     8	to a sign in the divisional chart based on specific mathematical divisions.
     9	"""
    10	from __future__ import annotations
    11	
    12	from typing import Any, Dict, List
    13	
    14	# Sign names in order (0-indexed)
    15	_SIGN_NAMES = [
    16	    "Aries", "Taurus", "Gemini", "Cancer",
    17	    "Leo", "Virgo", "Libra", "Scorpio",
    18	    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
    19	]
    20	
exec
/bin/zsh -lc "nl -ba app/divisional_charts.py | sed -n '360,520p'" in /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app succeeded in 0ms:
   360	                "sign": _SIGN_NAMES[rasi_index],
   361	                "sign_index": rasi_index,
   362	                "degree": round(lon % 30.0, 4),
   363	            }
   364	        return result
   365	
   366	    dispatch = {
   367	        2: _calculate_d2,
   368	        3: _calculate_d3,
   369	        4: _calculate_d4,
   370	        7: _calculate_d7,
   371	        9: _calculate_d9,
   372	        10: _calculate_d10,
   373	        12: _calculate_d12,
   374	        30: _calculate_d30,
   375	    }
   376	
   377	    if division in dispatch:
   378	        return dispatch[division](planet_longitudes)
   379	    return _calculate_generic(planet_longitudes, division)
codex
I have enough context to start identifying concrete mathematical defects; I’m now loading `transit_engine.py`, `kp_engine.py`, and `dosha_engine.py` to complete the full verification set.
exec
/bin/zsh -lc "nl -ba app/dosha_engine.py | sed -n '1,360p'" in /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_appexec
/bin/zsh -lc "nl -ba app/kp_engine.py | sed -n '1,380p'" in /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_appexec
/bin/zsh -lc "nl -ba app/transit_engine.py | sed -n '1,360p'" in /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app succeeded in 0ms:
     1	"""
     2	dosha_engine.py — Vedic Dosha & Yoga Detection Engine
     3	======================================================
     4	Detects Mangal Dosha, Kaal Sarp Dosha, Sade Sati, Pitra Dosha, Kemdrum Dosha.
     5	Also detects positive Yogas: Gajakesari, Budhaditya, Chandra-Mangal,
     6	and Panch Mahapurusha Yogas.
     7	"""
     8	
     9	# Zodiac signs in order (0-indexed for arithmetic)
    10	ZODIAC_SIGNS = [
    11	    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    12	    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
    13	]
    14	
    15	ZODIAC_INDEX = {sign: i for i, sign in enumerate(ZODIAC_SIGNS)}
    16	
    17	# Houses where Mars causes Mangal Dosha
    18	MANGAL_DOSHA_HOUSES = {1, 2, 4, 7, 8, 12}
    19	
    20	# Kendra houses (angular houses)
 succeeded in 0ms:
     1	"""
     2	kp_engine.py -- Krishnamurti Paddhati (KP) Astrology Engine
     3	=============================================================
     4	Implements the KP system of astrology, which uses the Vimshottari Dasha
     5	sub-lord system to determine significators for each house cusp.
     6	
     7	Key concepts:
     8	  - Star Lord: the Nakshatra lord of the cusp/planet position
     9	  - Sub Lord: finer Vimshottari subdivision within the Nakshatra
    10	  - Significators: planets that signify (influence) particular houses
    11	"""
    12	from __future__ import annotations
    13	
    14	from typing import Any, Dict, List, Tuple
    15	
    16	from app.astro_engine import NAKSHATRAS, NAKSHATRA_SPAN, get_nakshatra_from_longitude
    17	
    18	# ============================================================
    19	# VIMSHOTTARI DASHA SEQUENCE & YEARS
    20	# ============================================================
 succeeded in 0ms:
     1	"""
     2	transit_engine.py -- Gochara (Transit) Prediction Engine
     3	========================================================
     4	Calculates current planetary transits and evaluates their effects
     5	on a natal chart using classical Vedic Gochara rules (transit of
     6	planets counted from the natal Moon sign).
     7	
     8	Provides:
     9	  - calculate_transits(natal_chart_data) -> transit results + Sade Sati status
    10	"""
    11	from __future__ import annotations
    12	
    13	from datetime import datetime, timezone
    14	from typing import Any, Dict, List
    15	
    16	from app.astro_engine import calculate_planet_positions, _SIGN_NAMES
    17	
    18	
    19	# ── Zodiac helpers ─────────────────────────────────────────────
    20	
exec
/bin/zsh -lc "nl -ba app/dosha_engine.py | sed -n '360,760p'" in /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app succeeded in 0ms:
   360	    moon_house = moon.get("house", 0)
   361	    if moon_house == 0:
   362	        return {
   363	            "has_dosha": False,
   364	            "severity": "none",
   365	            "description": "Moon house data not available.",
   366	            "remedies": [],
   367	        }
   368	
   369	    # Houses 2nd and 12th from Moon
   370	    house_2nd = ((moon_house - 1 + 1) % 12) + 1  # moon_house + 1, wrapped
   371	    house_12th = ((moon_house - 1 - 1) % 12) + 1  # moon_house - 1, wrapped
   372	
   373	    # Check if any planet (excluding Rahu/Ketu) is in those houses
   374	    check_planets = ["Sun", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
   375	    planets_in_2nd = [p for p in check_planets if planets.get(p, {}).get("house") == house_2nd]
   376	    planets_in_12th = [p for p in check_planets if planets.get(p, {}).get("house") == house_12th]
   377	
   378	    has_dosha = len(planets_in_2nd) == 0 and len(planets_in_12th) == 0
   379	
exec
/bin/zsh -lc "python -c \"import random;from app.ashtakvarga_engine import calculate_ashtakvarga;signs=['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
for k in range(5):
 ps={p:random.choice(signs) for p in ['Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn','Ascendant']};r=calculate_ashtakvarga(ps);totals={p:sum(d.values()) for p,d in r['planet_bindus'].items()};sav=sum(r['sarvashtakvarga'].values());print(totals,sav)\"" in /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app exited 127 in 0ms:
zsh:1: command not found: python
exec
/bin/zsh -lc "python3 -c \"import random;from app.ashtakvarga_engine import calculate_ashtakvarga;signs=['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
for k in range(5):
 ps={p:random.choice(signs) for p in ['Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn','Ascendant']};r=calculate_ashtakvarga(ps);totals={p:sum(d.values()) for p,d in r['planet_bindus'].items()};sav=sum(r['sarvashtakvarga'].values());print(totals,sav)\"" in /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app succeeded in 0ms:
{'Sun': 48, 'Moon': 49, 'Mars': 39, 'Mercury': 54, 'Jupiter': 56, 'Venus': 52, 'Saturn': 39} 337
{'Sun': 48, 'Moon': 49, 'Mars': 39, 'Mercury': 54, 'Jupiter': 56, 'Venus': 52, 'Saturn': 39} 337
{'Sun': 48, 'Moon': 49, 'Mars': 39, 'Mercury': 54, 'Jupiter': 56, 'Venus': 52, 'Saturn': 39} 337
{'Sun': 48, 'Moon': 49, 'Mars': 39, 'Mercury': 54, 'Jupiter': 56, 'Venus': 52, 'Saturn': 39} 337
{'Sun': 48, 'Moon': 49, 'Mars': 39, 'Mercury': 54, 'Jupiter': 56, 'Venus': 52, 'Saturn': 39} 337
codex
I’m doing quick numerical sanity checks now (table invariants and boundary coverage) to avoid subjective-only judgments on these formula engines.
exec
/bin/zsh -lc "python3 -c \"from app.kp_engine import KP_SUB_LORDS;print(len(KP_SUB_LORDS),KP_SUB_LORDS[0]['start_degree'],KP_SUB_LORDS[-1]['end_degree']);
mx=0;gaps=[]
for i in range(len(KP_SUB_LORDS)-1):
 a=KP_SUB_LORDS[i]['end_degree'];b=KP_SUB_LORDS[i+1]['start_degree'];d=round(b-a,8)
 if d"'!=0:gaps.append((i,d,a,b))
print('"'gaps',len(gaps),gaps[:5])\"" in /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app succeeded in 0ms:
243 0.0 360.0
gaps 0 []
codex
**Findings (critical first)**

1. **Infinite loop risk in Kaal Sarp check**  
   - In [`dosha_engine.py:127`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/dosha_engine.py:127), `_houses_in_arc()` increments `h` with `(h % 12) + 1`.  
   - If `start=0` or `end=0`, loop never terminates.  
   - Caller passes defaults `0` in [`dosha_engine.py:589`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/dosha_engine.py:589)-[`595`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/dosha_engine.py:595).  
   - Result: potential hang in production.

2. **Vimshottari Dasha start is mathematically wrong**  
   - Code starts full Mahadasha of nakshatra lord from birth date in [`dasha_engine.py:170`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/dasha_engine.py:170)-[`181`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/dasha_engine.py:181) and [`270`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/dasha_engine.py:270)-[`273`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/dasha_engine.py:273).  
   - True Vimshottari requires **balance at birth** from Moon’s exact nakshatra position.

3. **“Cycle back” logic is incorrect**  
   - Comment says cycle, but logic sets last period instead in [`dasha_engine.py:203`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/dasha_engine.py:203)-[`207`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/dasha_engine.py:207).

4. **Divisional chart engine is not mathematically valid for all claimed charts**  
   - Claims all 16 standard vargas, but uses generic formula for many in [`divisional_charts.py:295`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/divisional_charts.py:295)-[`316`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/divisional_charts.py:316), dispatched via [`379`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/divisional_charts.py:379).  
   - D16/D20/D24/D27/D40/D45/D60 are not generally computed by this single cyclic formula.

5. **D30 implementation has wrong boundaries/degree handling**  
   - Even-sign boundaries in [`divisional_charts.py:258`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/divisional_charts.py:258) are non-standard for classical Trimshamsha.  
   - Degree output uses raw sign degree in [`divisional_charts.py:286`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/divisional_charts.py:286)-[`291`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/divisional_charts.py:291), not normalized within selected Trimshamsha segment.

6. **Avakhada western sign and karana calculations are wrong**  
   - Western Sun sign uses sidereal longitude directly in [`avakhada_engine.py:164`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/avakhada_engine.py:164)-[`166`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/avakhada_engine.py:166), [`241`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/avakhada_engine.py:241).  
   - Karana is reduced to `int(diff/6)%11` in [`avakhada_engine.py:216`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/avakhada_engine.py:216)-[`219`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/avakhada_engine.py:219), which is not the real karana sequence logic.

7. **Fallback astro math is intentionally low-precision, not production-grade**  
   - Explicitly approximate with multi-degree error in [`astro_engine.py:352`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/astro_engine.py:352)-[`357`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/astro_engine.py:357).  
   - Inner-planet “0.8 factor” in [`astro_engine.py:396`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/astro_engine.py:396)-[`397`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/astro_engine.py:397) is heuristic, not rigorous astronomy.

---

**Per-file verdict**

- [`app/astro_engine.py`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/astro_engine.py): **PARTIALLY CORRECT**  
- [`app/dasha_engine.py`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/dasha_engine.py): **INCORRECT**  
- [`app/ashtakvarga_engine.py`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/ashtakvarga_engine.py): **PARTIALLY CORRECT** (core bindu arithmetic is internally consistent; but defaulting Ascendant to Aries in [`137`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/ashtakvarga_engine.py:137)-[`139`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/ashtakvarga_engine.py:139) can silently produce wrong chart-level results)  
- [`app/shadbala_engine.py`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/shadbala_engine.py): **INCORRECT** (major simplifications + ordering bug in [`90`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/shadbala_engine.py:90)-[`93`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/shadbala_engine.py:93))  
- [`app/avakhada_engine.py`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/avakhada_engine.py): **INCORRECT**  
- [`app/divisional_charts.py`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/divisional_charts.py): **INCORRECT**  
- [`app/transit_engine.py`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/transit_engine.py): **PARTIALLY CORRECT** (sign/house logic okay, but precision depends on upstream engine quality)  
- [`app/kp_engine.py`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/kp_engine.py): **PARTIALLY CORRECT** (sub-lord segmentation math mostly consistent, but significator model in [`221`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/kp_engine.py:221)-[`253`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/kp_engine.py:253) is not full KP-grade)  
- [`app/dosha_engine.py`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/dosha_engine.py): **INCORRECT**

**Final production-readiness verdict:** **NOT PRODUCTION READY**.  
Too many core mathematical inaccuracies and at least one hard reliability bug (possible infinite loop).
tokens used
76,742
**Findings (critical first)**

1. **Infinite loop risk in Kaal Sarp check**  
   - In [`dosha_engine.py:127`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/dosha_engine.py:127), `_houses_in_arc()` increments `h` with `(h % 12) + 1`.  
   - If `start=0` or `end=0`, loop never terminates.  
   - Caller passes defaults `0` in [`dosha_engine.py:589`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/dosha_engine.py:589)-[`595`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/dosha_engine.py:595).  
   - Result: potential hang in production.

2. **Vimshottari Dasha start is mathematically wrong**  
   - Code starts full Mahadasha of nakshatra lord from birth date in [`dasha_engine.py:170`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/dasha_engine.py:170)-[`181`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/dasha_engine.py:181) and [`270`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/dasha_engine.py:270)-[`273`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/dasha_engine.py:273).  
   - True Vimshottari requires **balance at birth** from Moon’s exact nakshatra position.

3. **“Cycle back” logic is incorrect**  
   - Comment says cycle, but logic sets last period instead in [`dasha_engine.py:203`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/dasha_engine.py:203)-[`207`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/dasha_engine.py:207).

4. **Divisional chart engine is not mathematically valid for all claimed charts**  
   - Claims all 16 standard vargas, but uses generic formula for many in [`divisional_charts.py:295`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/divisional_charts.py:295)-[`316`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/divisional_charts.py:316), dispatched via [`379`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/divisional_charts.py:379).  
   - D16/D20/D24/D27/D40/D45/D60 are not generally computed by this single cyclic formula.

5. **D30 implementation has wrong boundaries/degree handling**  
   - Even-sign boundaries in [`divisional_charts.py:258`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/divisional_charts.py:258) are non-standard for classical Trimshamsha.  
   - Degree output uses raw sign degree in [`divisional_charts.py:286`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/divisional_charts.py:286)-[`291`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/divisional_charts.py:291), not normalized within selected Trimshamsha segment.

6. **Avakhada western sign and karana calculations are wrong**  
   - Western Sun sign uses sidereal longitude directly in [`avakhada_engine.py:164`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/avakhada_engine.py:164)-[`166`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/avakhada_engine.py:166), [`241`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/avakhada_engine.py:241).  
   - Karana is reduced to `int(diff/6)%11` in [`avakhada_engine.py:216`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/avakhada_engine.py:216)-[`219`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/avakhada_engine.py:219), which is not the real karana sequence logic.

7. **Fallback astro math is intentionally low-precision, not production-grade**  
   - Explicitly approximate with multi-degree error in [`astro_engine.py:352`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/astro_engine.py:352)-[`357`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/astro_engine.py:357).  
   - Inner-planet “0.8 factor” in [`astro_engine.py:396`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/astro_engine.py:396)-[`397`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/astro_engine.py:397) is heuristic, not rigorous astronomy.

---

**Per-file verdict**

- [`app/astro_engine.py`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/astro_engine.py): **PARTIALLY CORRECT**  
- [`app/dasha_engine.py`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/dasha_engine.py): **INCORRECT**  
- [`app/ashtakvarga_engine.py`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/ashtakvarga_engine.py): **PARTIALLY CORRECT** (core bindu arithmetic is internally consistent; but defaulting Ascendant to Aries in [`137`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/ashtakvarga_engine.py:137)-[`139`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/ashtakvarga_engine.py:139) can silently produce wrong chart-level results)  
- [`app/shadbala_engine.py`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/shadbala_engine.py): **INCORRECT** (major simplifications + ordering bug in [`90`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/shadbala_engine.py:90)-[`93`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/shadbala_engine.py:93))  
- [`app/avakhada_engine.py`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/avakhada_engine.py): **INCORRECT**  
- [`app/divisional_charts.py`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/divisional_charts.py): **INCORRECT**  
- [`app/transit_engine.py`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/transit_engine.py): **PARTIALLY CORRECT** (sign/house logic okay, but precision depends on upstream engine quality)  
- [`app/kp_engine.py`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/kp_engine.py): **PARTIALLY CORRECT** (sub-lord segmentation math mostly consistent, but significator model in [`221`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/kp_engine.py:221)-[`253`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/kp_engine.py:253) is not full KP-grade)  
- [`app/dosha_engine.py`](/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/app/dosha_engine.py): **INCORRECT**

**Final production-readiness verdict:** **NOT PRODUCTION READY**.  
Too many core mathematical inaccuracies and at least one hard reliability bug (possible infinite loop).
