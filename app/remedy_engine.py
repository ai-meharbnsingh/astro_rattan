import logging
from typing import Any, Dict, List
from datetime import datetime
from datetime import datetime as _dt
from app.remedy_sources import PLANETARY_REMEDIES, DOSHA_REMEDIES, GENERAL_BALANCING
from app.shadbala_engine import calculate_shadbala, REQUIRED_STRENGTH
from app.dosha_engine import (
    check_mangal_dosha, check_kaal_sarp, check_sade_sati, 
    check_pitra_dosha, check_kemdrum_dosha
)

logger = logging.getLogger(__name__)

def generate_astrological_remedies(chart_data: Dict[str, Any], year: int = None) -> Dict[str, Any]:
    """
    Main engine to generate remedies based on chart logic.
    """
    # Standardize planets extraction
    planets = chart_data.get("planets", {})
    if not planets and "planet_positions" in chart_data:
        planets = chart_data["planet_positions"]
        
    if not planets:
        # Extreme fallback
        return {
            "general_remedies": [{
                "category": "General Balance",
                "problem_detected": "Chart data processing note.",
                "why_it_matters": "Universal spiritual practices support everyone.",
                "remedies": GENERAL_BALANCING
            }],
            "yearly_remedies": [],
            "debug": "No planets found in chart_data"
        }

    # 1. Shadbala Analysis (best-effort)
    shadbala_results = {}
    try:
        shadbala_results = calculate_shadbala(**_prepare_shadbala_params_from_chart(chart_data))
    except Exception as e:
        logger.error(f"Error calculating Shadbala for remedies: {e}")

    # 2. Dosha Detection
    doshas = _detect_all_doshas(chart_data)
    
    general_remedies = []
    
    # 3. Planet-wise Triggers
    for planet_name, info in planets.items():
        if not isinstance(info, dict): continue
        if planet_name not in PLANETARY_REMEDIES:
            continue
            
        triggers = []
        
        # Trigger: Weak in Shadbala
        if shadbala_results and planet_name in REQUIRED_STRENGTH:
            p_shad = shadbala_results.get(planet_name, {})
            total_bala = p_shad.get("total") if isinstance(p_shad, dict) else 0
            if total_bala and total_bala < REQUIRED_STRENGTH[planet_name]:
                triggers.append(f"{planet_name} is weak in Shadbala strength ({total_bala:.2f} < {REQUIRED_STRENGTH[planet_name]})")

        # Trigger: Combustion
        if info.get("is_combust") or info.get("combust"):
            triggers.append(f"{planet_name} is combust (too close to the Sun)")
            
        # Trigger: Debilitation
        dignity = str(info.get("dignity", "")).lower()
        if "debilitated" in dignity or "neecha" in dignity:
             triggers.append(f"{planet_name} is debilitated in the natal chart")
        
        if triggers:
            source_data = PLANETARY_REMEDIES[planet_name]
            general_remedies.append({
                "category": f"{planet_name} Balance",
                "problem_detected": ". ".join(triggers),
                "why_it_matters": source_data["why_it_matters"],
                "remedies": source_data["remedies"]
            })

    # 4. Dosha-wise Triggers
    for dosha_name, is_present in doshas.items():
        if is_present and dosha_name in DOSHA_REMEDIES:
            source_data = DOSHA_REMEDIES[dosha_name]
            general_remedies.append({
                "category": dosha_name,
                "problem_detected": source_data["problem"],
                "why_it_matters": source_data["why_it_matters"],
                "remedies": source_data["remedies"]
            })

    # 5. Fallback: Always ensure meaningful guidance
    if len(general_remedies) < 2:
        general_remedies.append({
            "category": "Universal Balance",
            "problem_detected": "Supporting the latent potential of your birth chart.",
            "why_it_matters": "Even without specific afflictions, regular spiritual hygiene ensures your positive planetary combinations (Yogas) deliver maximum results.",
            "remedies": GENERAL_BALANCING
        })
    else:
        # Always add at least two general balancing tips to the existing list
        general_remedies.append({
            "category": "Vitality Routine",
            "problem_detected": "Aligning your daily energy with cosmic cycles.",
            "why_it_matters": "A disciplined routine creates a strong vessel for planetary energies to manifest through.",
            "remedies": GENERAL_BALANCING[:2]
        })

    return {
        "general_remedies": general_remedies,
        "yearly_remedies": _generate_yearly_remedies(chart_data, year),
    }

def _detect_all_doshas(chart_data: Dict[str, Any]) -> Dict[str, bool]:
    planets = chart_data.get("planets", {})
    planet_houses = {p: info.get("house") for p, info in planets.items()}
    
    results = {}
    
    # Mangal Dosha
    mangal = check_mangal_dosha(planet_houses.get("Mars", 0))
    results["Mangal Dosha"] = mangal.get("present", False)
    
    # Kaal Sarp
    kaal_sarp = check_kaal_sarp(planet_houses.get("Rahu", 0), planet_houses.get("Ketu", 0), planet_houses)
    results["Kaal Sarp Dosha"] = kaal_sarp.get("present", False)
    
    # Sade Sati (Natal condition check)
    moon_sign = planets.get("Moon", {}).get("sign", "")
    saturn_sign = planets.get("Saturn", {}).get("sign", "")
    sade_sati = check_sade_sati(moon_sign, saturn_sign)
    results["Sade Sati"] = sade_sati.get("present", False)
    
    # Pitra Dosha
    pitra = check_pitra_dosha(planets)
    results["Pitra Dosha"] = pitra.get("present", False)
    
    return results

def _generate_yearly_remedies(chart_data: Dict[str, Any], year: int = None) -> List[Dict[str, Any]]:
    """
    Generate yearly remedies based on current dasha and transit influences.
    """
    if not year:
        year = datetime.now().year
        
    yearly = []
    
    # 1. Dasha Influence
    # Attempt to calculate or retrieve the dasha active for the requested year
    dasha_lord = None
    try:
        from app.dasha_engine import calculate_dasha
        birth_nakshatra = chart_data.get("nakshatra")
        birth_date = chart_data.get("birth_date")
        moon_lon = chart_data.get("chart_data", {}).get("planets", {}).get("Moon", {}).get("longitude")
        
        if birth_nakshatra and birth_date:
            dasha_res = calculate_dasha(birth_nakshatra, birth_date, moon_longitude=moon_lon)
            # Find mahadasha active in the middle of the requested year
            target_date = datetime(year, 6, 15)
            for md in dasha_res.get("mahadashas", []):
                start = datetime.strptime(md["start_date"], "%Y-%m-%d")
                end = datetime.strptime(md["end_date"], "%Y-%m-%d")
                if start <= target_date <= end:
                    dasha_lord = md["planet"]
                    break
    except Exception as e:
        logger.warning(f"Could not compute dasha for yearly remedies: {e}")

    if not dasha_lord:
        dasha_lord = chart_data.get("current_dasha", {}).get("mahadasha")
        
    if dasha_lord and dasha_lord in PLANETARY_REMEDIES:
        source_data = PLANETARY_REMEDIES[dasha_lord]
        yearly.append({
            "category": f"{dasha_lord} Mahadasha Influence",
            "based_on": f"Active period in {year}",
            "summary": f"Your year {year} is primarily governed by {dasha_lord}. Aligning with its energy will help you navigate the year with more ease.",
            "remedies": source_data["remedies"][:1] # Focus on the primary mantra
        })

    # 2. Check for Sade Sati (Transit)
    # If the natal Moon is under pressure, the transit of Saturn is a yearly concern.
    doshas = _detect_all_doshas(chart_data)
    if doshas.get("Sade Sati"):
        yearly.append({
            "category": "Saturn Transit (Sade Sati)",
            "based_on": f"Transit cycle for {year}",
            "summary": f"During {year}, the influence of Saturn on your natal Moon continues, requiring disciplined action and emotional resilience.",
            "remedies": DOSHA_REMEDIES["Sade Sati"]["remedies"]
        })

    # 3. Year Lord (Varshphal)
    # The Year Lord from Varshphal engine is the most specific annual indicator.
    year_lord = chart_data.get("year_lord")
    if year_lord and year_lord in PLANETARY_REMEDIES:
        source_data = PLANETARY_REMEDIES[year_lord]
        yearly.append({
            "category": f"Varshesh ({year_lord}) Influence",
            "based_on": f"Solar Return Lord for {year}",
            "summary": f"In your annual solar return chart for {year}, {year_lord} is the designated ruler (Varshesh), defining your major achievements this year.",
            "remedies": source_data["remedies"]
        })

    # 4. Universal Annual Guidance
    if not yearly:
        yearly.append({
            "category": "Annual Vitality",
            "based_on": f"General transit rhythm for {year}",
            "summary": f"A balanced year with no major afflictions. Focus on maintaining your spiritual routine.",
            "remedies": [GENERAL_BALANCING[0]]
        })

    return yearly


def _prepare_shadbala_params_from_chart(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """Build a calculate_shadbala(**params) dict from (possibly partial) chart_data.

    This engine is used in remedies to detect 'weak' planets. It must never
    hard-fail the whole remedies pipeline.
    """
    planets = chart_data.get("planets", {}) if isinstance(chart_data, dict) else {}
    planet_signs: Dict[str, str] = {}
    planet_houses: Dict[str, int] = {}
    planet_longitudes: Dict[str, float] = {}
    planet_speeds: Dict[str, float] = {}
    retrograde_planets = set()

    for pn, pi in (planets or {}).items():
        if not isinstance(pi, dict):
            continue
        planet_signs[pn] = pi.get("sign", "Aries")
        try:
            planet_houses[pn] = int(pi.get("house", 1) or 1)
        except Exception:
            planet_houses[pn] = 1
        if "longitude" in pi:
            try:
                planet_longitudes[pn] = float(pi["longitude"])
            except Exception:
                pass
        if "speed" in pi:
            try:
                planet_speeds[pn] = float(pi["speed"])
            except Exception:
                pass
        if pi.get("retrograde") or "retrograde" in str(pi.get("status", "")).lower():
            retrograde_planets.add(pn)

    # Birth date/time are optional in many payloads; use safe defaults.
    birth_time = str(chart_data.get("birth_time", "12:00:00"))
    try:
        parts = birth_time.split(":")
        birth_hour = int(parts[0]) + int(parts[1]) / 60.0
    except Exception:
        birth_hour = 12.0

    birth_date = str(chart_data.get("birth_date", "2000-01-01"))[:10]
    try:
        bd = _dt.strptime(birth_date, "%Y-%m-%d")
        weekday = bd.weekday()
        birth_year = bd.year
        birth_month = bd.month
    except Exception:
        weekday, birth_year, birth_month = 0, 2000, 1

    sun_lon = planet_longitudes.get("Sun", 0.0)
    moon_lon = planet_longitudes.get("Moon", 0.0)

    return {
        "planet_signs": planet_signs,
        "planet_houses": planet_houses,
        "is_daytime": 6.0 <= birth_hour < 18.0,
        "retrograde_planets": retrograde_planets,
        "planet_longitudes": planet_longitudes if planet_longitudes else None,
        "planet_speeds": planet_speeds if planet_speeds else None,
        "birth_hour": birth_hour,
        "moon_sun_elongation": (moon_lon - sun_lon) % 360.0,
        "weekday": weekday,
        "birth_year": birth_year,
        "birth_month": birth_month,
    }
