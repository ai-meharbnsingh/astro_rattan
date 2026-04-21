import logging
from typing import Any, Dict, List
from datetime import datetime
from app.remedy_sources import PLANETARY_REMEDIES, DOSHA_REMEDIES, GENERAL_BALANCING
from app.shadbala_engine import calculate_shadbala, REQUIRED_STRENGTH
from app.dosha_engine import (
    check_mangal_dosha, check_kaal_sarp, check_sade_sati, 
    check_pitra_dosha, check_kemdrum_dosha
)

logger = logging.getLogger(__name__)

def generate_astrological_remedies(chart_data: Dict[str, Any], year: int = None, language: str = 'en') -> Dict[str, Any]:
    """
    Main engine to generate remedies based on chart logic.
    Supports bilingual output (en/hi).
    """
    is_hi = (language == 'hi')
    
    # Standardize planets extraction
    planets = chart_data.get("planets", {})
    if not planets and "planet_positions" in chart_data:
        planets = chart_data["planet_positions"]
        
    if not planets:
        return {
            "general_remedies": [{
                "category": "Universal Balance" if not is_hi else "सार्वभौमिक संतुलन",
                "problem_detected": "Supporting the latent potential of your birth chart." if not is_hi else "आपकी जन्म कुंडली की अंतर्निहित क्षमता का समर्थन करना।",
                "why_it_matters": "Universal spiritual practices support everyone." if not is_hi else "सार्वभौमिक आध्यात्मिक अभ्यास सभी का समर्थन करते हैं।",
                "remedies": _translate_remedies(GENERAL_BALANCING, is_hi)
            }],
            "yearly_remedies": [],
            "debug": "No planets found in chart_data"
        }

    # 1. Shadbala Analysis
    shadbala_results = {}
    try:
        shadbala_results = calculate_shadbala(chart_data)
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
            
        triggers_en = []
        triggers_hi = []
        
        # Trigger: Weak in Shadbala
        if shadbala_results and planet_name in REQUIRED_STRENGTH:
            p_shad = shadbala_results.get(planet_name, {})
            total_bala = p_shad.get("total") if isinstance(p_shad, dict) else 0
            if total_bala and total_bala < REQUIRED_STRENGTH[planet_name]:
                triggers_en.append(f"{planet_name} is weak in Shadbala strength ({total_bala:.2f} < {REQUIRED_STRENGTH[planet_name]})")
                triggers_hi.append(f"{planet_name} षड्बल शक्ति में कमजोर है ({total_bala:.2f} < {REQUIRED_STRENGTH[planet_name]})")

        # Trigger: Combustion
        if info.get("is_combust") or info.get("combust"):
            triggers_en.append(f"{planet_name} is combust (too close to the Sun)")
            triggers_hi.append(f"{planet_name} अस्त है (सूर्य के बहुत करीब)")
            
        # Trigger: Debilitation
        dignity = str(info.get("dignity", "")).lower()
        if "debilitated" in dignity or "neecha" in dignity:
             triggers_en.append(f"{planet_name} is debilitated in the natal chart")
             triggers_hi.append(f"{planet_name} जन्म कुंडली में नीच का है")
        
        if triggers_en:
            source_data = PLANETARY_REMEDIES[planet_name]
            general_remedies.append({
                "category": f"{planet_name} Balance" if not is_hi else f"{planet_name} संतुलन",
                "problem_detected": ". ".join(triggers_hi if is_hi else triggers_en),
                "why_it_matters": source_data["why_it_matters_hi" if is_hi else "why_it_matters_en"],
                "remedies": _translate_remedies(source_data["remedies"], is_hi)
            })

    # 4. Dosha-wise Triggers
    for dosha_name, is_present in doshas.items():
        if is_present and dosha_name in DOSHA_REMEDIES:
            source_data = DOSHA_REMEDIES[dosha_name]
            general_remedies.append({
                "category": dosha_name if not is_hi else _translate_dosha_name(dosha_name),
                "problem_detected": source_data["problem_hi" if is_hi else "problem_en"],
                "why_it_matters": source_data["why_it_matters_hi" if is_hi else "why_it_matters_en"],
                "remedies": _translate_remedies(source_data["remedies"], is_hi)
            })

    # 5. Fallback: Always ensure meaningful guidance
    if len(general_remedies) < 2:
        general_remedies.append({
            "category": "Universal Balance" if not is_hi else "सार्वभौमिक संतुलन",
            "problem_detected": "Supporting the latent potential of your birth chart." if not is_hi else "आपकी जन्म कुंडली की अंतर्निहित क्षमता का समर्थन करना।",
            "why_it_matters": "Even without specific afflictions, regular spiritual hygiene ensures your positive planetary combinations (Yogas) deliver maximum results." if not is_hi else "विशिष्ट दोषों के बिना भी, नियमित आध्यात्मिक स्वच्छता सुनिश्चित करती है कि आपके सकारात्मक ग्रह योग अधिकतम परिणाम दें।",
            "remedies": _translate_remedies(GENERAL_BALANCING, is_hi)
        })
    else:
        general_remedies.append({
            "category": "Vitality Routine" if not is_hi else "जीवन शक्ति दिनचर्या",
            "problem_detected": "Aligning your daily energy with cosmic cycles." if not is_hi else "अपनी दैनिक ऊर्जा को ब्रह्मांडीय चक्रों के साथ जोड़ना।",
            "why_it_matters": "A disciplined routine creates a strong vessel for planetary energies to manifest through." if not is_hi else "एक अनुशासित दिनचर्या ग्रह ऊर्जाओं के प्रकट होने के लिए एक मजबूत आधार बनाती है।",
            "remedies": _translate_remedies(GENERAL_BALANCING[:2], is_hi)
        })

    return {
        "general_remedies": general_remedies,
        "yearly_remedies": _generate_yearly_remedies(chart_data, year, is_hi),
    }

def _translate_remedies(remedies: List[Dict], is_hi: bool) -> List[Dict]:
    results = []
    for r in remedies:
        results.append({
            "type": r["type"],
            "title": r["title_hi" if is_hi else "title_en"],
            "what_to_do": r["what_to_do_hi" if is_hi else "what_to_do_en"],
            "how_to_do": r["how_to_do_hi" if is_hi else "how_to_do_en"],
            "when_to_do": r.get("when_to_do_hi" if is_hi else "when_to_do_en"),
            "frequency": r.get("frequency_hi" if is_hi else "frequency_en"),
            "expected_benefit": r.get("expected_benefit_hi" if is_hi else "expected_benefit_en"),
            "source_type": r.get("source_type"),
            "source_label": r.get("source_label_hi" if is_hi else "source_label_en"),
            "scriptural_reference": r.get("scriptural_reference")
        })
    return results

def _translate_dosha_name(name: str) -> str:
    mapping = {
        "Mangal Dosha": "मंगल दोष",
        "Kaal Sarp Dosha": "काल सर्प दोष",
        "Sade Sati": "साढ़े साती",
        "Pitra Dosha": "पितृ दोष",
        "Kemadruma Dosha": "केमद्रुम दोष"
    }
    return mapping.get(name, name)

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
    
    # Kemadruma
    kemdrum = check_kemdrum_dosha(planets)
    results["Kemadruma Dosha"] = kemdrum.get("present", False)
    
    return results

def _generate_yearly_remedies(chart_data: Dict[str, Any], year: int = None, is_hi: bool = False) -> List[Dict[str, Any]]:
    if not year:
        year = datetime.now().year
        
    yearly = []
    doshas = _detect_all_doshas(chart_data)
    
    # 1. Dasha Influence
    dasha_lord = None
    try:
        from app.dasha_engine import calculate_dasha
        birth_nakshatra = chart_data.get("nakshatra")
        birth_date = chart_data.get("birth_date")
        moon_lon = chart_data.get("chart_data", {}).get("planets", {}).get("Moon", {}).get("longitude")
        
        if birth_nakshatra and birth_date:
            dasha_res = calculate_dasha(birth_nakshatra, birth_date, moon_longitude=moon_lon)
            target_date = datetime(year, 6, 15)
            for md in dasha_res.get("mahadashas", []):
                start = datetime.strptime(md["start_date"], "%Y-%m-%d")
                end = datetime.strptime(md["end_date"], "%Y-%m-%d")
                if start <= target_date <= end:
                    dasha_lord = md["planet"]
                    break
    except Exception:
        pass

    if not dasha_lord:
        dasha_lord = chart_data.get("current_dasha", {}).get("mahadasha")
        
    if dasha_lord and dasha_lord in PLANETARY_REMEDIES:
        source_data = PLANETARY_REMEDIES[dasha_lord]
        yearly.append({
            "category": f"{dasha_lord} Mahadasha" if not is_hi else f"{dasha_lord} महादशा",
            "based_on": f"Active period in {year}" if not is_hi else f"{year} में सक्रिय अवधि",
            "summary": f"Your year {year} is primarily governed by {dasha_lord}." if not is_hi else f"आपका वर्ष {year} मुख्य रूप से {dasha_lord} द्वारा शासित है।",
            "remedies": _translate_remedies(source_data["remedies"][:1], is_hi)
        })

    # 2. Sade Sati
    if doshas.get("Sade Sati"):
        yearly.append({
            "category": "Sade Sati" if not is_hi else "साढ़े साती",
            "based_on": f"Transit cycle for {year}" if not is_hi else f"{year} के लिए गोचर चक्र",
            "summary": f"During {year}, the influence of Saturn on your natal Moon continues." if not is_hi else f"{year} के दौरान, आपके जन्म के चंद्रमा पर शनि का प्रभाव जारी है।",
            "remedies": _translate_remedies(DOSHA_REMEDIES["Sade Sati"]["remedies"], is_hi)
        })

    if not yearly:
        yearly.append({
            "category": "Annual Vitality" if not is_hi else "वार्षिक जीवन शक्ति",
            "based_on": f"General rhythm for {year}" if not is_hi else f"{year} के लिए सामान्य लय",
            "summary": f"A balanced year ahead." if not is_hi else "आगे एक संतुलित वर्ष है।",
            "remedies": _translate_remedies([GENERAL_BALANCING[0]], is_hi)
        })

    return yearly
