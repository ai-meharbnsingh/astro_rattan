"""
lalkitab_advanced.py -- Advanced Lal Kitab Logic Engine
========================================================
Implements "Pundit-level" logic including:
1. Masnui Grah (Artificial Planets)
2. Lal Kitab Rin (Karmic Debts)
3. Teva Typology (Andha/Dharmi Teva)
4. Prohibited Remedies (Precautions)
5. Lal Kitab Aspects (Drishti)
6. Sleeping Planets & Houses (Soya Grah / Ghar)
7. Kayam Grah (Established Planets)
"""

from typing import Dict, List, Any

# ============================================================
# 1. MASNUI GRAH (ARTIFICIAL PLANETS)
# Reference: PDF 2.2.1
# ============================================================

MASNUI_MAPPING = [
    {
        "planets": {"Saturn", "Venus"}, 
        "result": "Jupiter", 
        "domain": {"en": "Children, wisdom, prosperity", "hi": "संतान, बुद्धि, समृद्धि"},
        "quality": "Khali Hawai",  # Empty air - philosophical pretension without foundation
        "house_override": None,  # No specific house override
        "psychological_profile": {
            "en": "Espouses spiritual ideals while remaining materially attached",
            "hi": "भौतिक रूप से आसक्त रहते हुए आध्यात्मिक आदर्शों का समर्थन करना"
        }
    },
    {
        "planets": {"Jupiter", "Venus"}, 
        "result": "Saturn", 
        "domain": {"en": "Delays, structure, maturity", "hi": "विलंब, संरचना, परिपक्वता"},
        "quality": "Khali Hawai",
        "house_override": 2,  # 1941 text p380 - affects 2nd house (wealth, family speech)
        "house_effects": {
            "en": "Restricted expansion, disciplined pleasure - affects wealth accumulation and family speech patterns",
            "hi": "प्रतिबंधित विस्तार, अनुशासित सुख - धन संचय और पारिवारिक वाणी पैटर्न को प्रभावित करता है"
        },
        "psychological_profile": {
            "en": "Pursues pleasure compulsively without genuine enjoyment",
            "hi": "वास्तविक आनंद के बिना अनिवार्य रूप से सुख का पीछा करना"
        }
    },
    {
        "planets": {"Sun", "Mercury"}, 
        "result": "Mars", 
        "domain": {"en": "Courage, siblings, property", "hi": "साहस, भाई-बहन, संपत्ति"},
        "quality": "Good",
        "house_override": None,
        "psychological_profile": {
            "en": "Positive aggression and intellectual protection",
            "hi": "सकारात्मक आक्रामकता और बौद्धिक सुरक्षा"
        }
    },
    {
        "planets": {"Sun", "Mars"}, 
        "result": "Mercury", 
        "domain": {"en": "Intellect, commerce, health", "hi": "बुद्धि, वाणिज्य, स्वास्थ्य"},
        "quality": "Good",
        "house_override": None,
        "psychological_profile": {
            "en": "Rapid decision making with impulsive communication",
            "hi": "आवेगपूर्ण संचार के साथ त्वरित निर्णय लेना"
        }
    },
    {
        "planets": {"Saturn", "Mercury"}, 
        "result": "Venus", 
        "domain": {"en": "Partnerships, arts, wealth", "hi": "साझेदारी, कला, धन"},
        "quality": "Good",
        "house_override": 7,  # 1941 text p380 - affects 7th house (marriage, partnerships)
        "house_effects": {
            "en": "Calculated relationships, business romance - directly impacts marriage and business partnerships",
            "hi": "गणितीय संबंध, व्यावसायिक रोमांस - सीधे विवाह और व्यावसायिक साझेदारी को प्रभावित करता है"
        },
        "psychological_profile": {
            "en": "Approaches relationships with calculated precision",
            "hi": "गणितीय सटीकता के साथ संबंधों को देखना"
        }
    },
    {
        "planets": {"Moon", "Jupiter"}, 
        "result": "Sun", 
        "domain": {"en": "Vitality, career, father", "hi": "जीवन शक्ति, करियर, पिता"},
        "quality": "Good",
        "house_override": None,
        "psychological_profile": {
            "en": "Emotional authority with nurturing leadership",
            "hi": "पालन-पोषण नेतृत्व के साथ भावनात्मक अधिकार"
        }
    },
    {
        "planets": {"Sun", "Jupiter"}, 
        "result": "Moon", 
        "domain": {"en": "Emotions, mother, public", "hi": "भावनाएं, माता, जनता"},
        "quality": "Good",
        "house_override": 5,  # 1941 text p380 - affects 5th house (children, intelligence)
        "house_effects": {
            "en": "Optimistic emotions, expansive imagination - impacts children, education, and intelligence",
            "hi": "आशावादी भावनाएं, विस्तृत कल्पना - संतान, शिक्षा और बुद्धि को प्रभावित करता है"
        },
        "psychological_profile": {
            "en": "Expansive emotional imagination with optimism",
            "hi": "आशावाद के साथ विस्तृत भावनात्मक कल्पना"
        }
    },
    {
        "planets": {"Rahu", "Ketu"}, 
        "result": "Venus", 
        "domain": {"en": "Relationships, pleasures, addictions", "hi": "संबंध, सुख, व्यसन"},
        "quality": "Mixed",
        "house_override": None,
        "psychological_profile": {
            "en": "Sensual/obsessive desires in relationships",
            "hi": "संबंधों में कामुक/व्यामोहजनक इच्छाएं"
        }
    },
    {
        "planets": {"Mars", "Saturn"}, 
        "result": "Rahu", 
        "domain": {"en": "Foreign, accidents, upheaval", "hi": "विदेश, दुर्घटनाएं, उथल-पुथल"},
        "quality": "Challenging",
        "house_override": None,
        "psychological_profile": {
            "en": "Intensified ambition with sudden disruptions",
            "hi": "अचानक व्यवधानों के साथ तीव्र महत्वाकांक्षा"
        }
    },
    {
        "planets": {"Moon", "Saturn"}, 
        "result": "Ketu", 
        "domain": {"en": "Liberation, loss, meditation", "hi": "मुक्ति, हानि, ध्यान"},
        "quality": "Challenging",
        "house_override": 8,  # Mars+Saturn+Moon combination affects 8th house
        "house_effects": {
            "en": "Depressive detachment, spiritual isolation - impacts longevity, obstacles, inheritance",
            "hi": "अवसादपूर्ण वैराग्य, आध्यात्मिक एकांत - आयु, बाधाओं, विरासत को प्रभावित करता है"
        },
        "psychological_profile": {
            "en": "Depressive detachment with spiritual isolation tendencies",
            "hi": "आध्यात्मिक एकांत की प्रवृत्तियों के साथ अवसादपूर्ण वैराग्य"
        }
    },
]

# ============================================================
# HOUSE OVERRIDE MAPPING (Reference: Lal Kitab 1941, p380)
# ============================================================
# These combinations affect specific houses regardless of actual placement
MASNUI_HOUSE_OVERRIDES = {
    # Jupiter + Venus → 2nd house effects
    ("Jupiter", "Venus"): {
        "house": 2,
        "house_name": {"en": "Wealth/Family", "hi": "धन/परिवार"},
        "effects": {
            "en": "Restricts wealth accumulation, affects family speech patterns, creates delays in financial matters",
            "hi": "धन संचय को प्रतिबंधित करता है, पारिवारिक वाणी पैटर्न को प्रभावित करता है, वित्तीय मामलों में देरी"
        },
        "predictive_note": {
            "en": "May experience marriage delay despite favorable Venus condition, or wealth obstacles despite Jupiter's beneficence",
            "hi": "अनुकूल शुक्र स्थिति के बावजूद विवाह में देरी, या गुरु की शुभता के बावजूद धन बाधाएं अनुभव हो सकती हैं"
        }
    },
    # Saturn + Mercury → 7th house effects
    ("Saturn", "Mercury"): {
        "house": 7,
        "house_name": {"en": "Marriage/Partnerships", "hi": "विवाह/साझेदारी"},
        "effects": {
            "en": "Calculative approach to relationships, business-like marital arrangements, intellectual compatibility over romance",
            "hi": "संबंधों में गणनात्मक दृष्टिकोण, व्यावसायिक विवाह व्यवस्था, रोमांस पर बौद्धिक अनुकूलता"
        },
        "predictive_note": {
            "en": "Partnerships characterized by contractual discussions; avoid intellectualizing emotional matters during Mercury periods",
            "hi": "अनुबंधित चर्चाओं से चिह्नित साझेदारी; बुध की अवधि के दौरान भावनात्मक मामलों को बौद्धिक बनाने से बचें"
        }
    },
    # Sun + Jupiter → 5th house effects
    ("Sun", "Jupiter"): {
        "house": 5,
        "house_name": {"en": "Children/Intelligence", "hi": "संतान/बुद्धि"},
        "effects": {
            "en": "Impacts progeny matters, educational success, and creative intelligence",
            "hi": "संतान के मामलों, शैक्षिक सफलता और रचनात्मक बुद्धि को प्रभावित करता है"
        },
        "predictive_note": {
            "en": "Children's success may follow unconventional paths; education may involve sudden changes",
            "hi": "बच्चों की सफलता अपरंपरागत रास्तों पर अनुसरण कर सकती है; शिक्षा में अचानक परिवर्तन शामिल हो सकते हैं"
        }
    },
    # Mars + Mercury → 3rd house effects
    ("Mars", "Mercury"): {
        "house": 3,
        "house_name": {"en": "Siblings/Courage", "hi": "भाई-बहन/साहस"},
        "effects": {
            "en": "Affects sibling relationships, courage in communication, short-distance travel success",
            "hi": "भाई-बहन संबंधों, संचार में साहस, लघु-दूरी यात्रा सफलता को प्रभावित करता है"
        },
        "predictive_note": {
            "en": "Aggressive communication with siblings; courageous writing or media pursuits",
            "hi": "भाई-बहनों के साथ आक्रामक संचार; साहसी लेखन या मीडिया प्रयास"
        }
    },
    # Moon + Saturn (+ Mars if present) → 8th house effects
    ("Moon", "Saturn"): {
        "house": 8,
        "house_name": {"en": "Longevity/Obstacles", "hi": "आयु/बाधाएं"},
        "effects": {
            "en": "Transforms 8th house effects including longevity concerns, sudden obstacles, inheritance issues",
            "hi": "आयु संबंधी चिंताओं, अचानक बाधाओं, विरासत के मुद्दों सहित 8वें भाव के प्रभावों को बदलता है"
        },
        "predictive_note": {
            "en": "Depressive tendencies may manifest as health challenges; meditation recommended during difficult periods",
            "hi": "अवसादग्रस्त प्रवृत्तियां स्वास्थ्य चुनौतियों के रूप में प्रकट हो सकती हैं; कठिन अवधि के दौरान ध्यान की सलाह दी जाती है"
        }
    },
}

def calculate_masnui_planets(planet_positions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Identifies artificial planets formed by conjunctions in the same house.
    Includes house-override principles from Lal Kitab 1941 (p380).
    
    Returns:
        {
            "masnui_planets": [...],  # List of identified artificial planets
            "house_overrides": {...},  # House-specific effects
            "psychological_profile": {...},
            "predictive_notes": [...]
        }
    """
    # Group planets by house
    house_map: Dict[int, set] = {}
    for p in planet_positions:
        h = p.get("house")
        if h:
            if h not in house_map:
                house_map[h] = set()
            house_map[h].add(p["planet"])

    results = []
    house_overrides = {}
    all_affected_houses = set()
    
    for house, planets in house_map.items():
        if len(planets) < 2:
            continue
            
        for rule in MASNUI_MAPPING:
            # Check if all required planets for the rule are in this house
            if rule["planets"].issubset(planets):
                masnui_result = {
                    "house": house,
                    "formed_by": sorted(list(rule["planets"])),
                    "masnui_planet": rule["result"],
                    "affected_domain": rule["domain"],
                    "quality": rule.get("quality", "Good"),
                    "psychological_profile": rule.get("psychological_profile", {})
                }
                
                # Add house override information if applicable
                if rule.get("house_override"):
                    override_house = rule["house_override"]
                    masnui_result["house_override"] = override_house
                    masnui_result["house_effects"] = rule.get("house_effects", {})
                    all_affected_houses.add(override_house)
                    
                    # Track this override
                    planet_pair = tuple(sorted(rule["planets"]))
                    if planet_pair in MASNUI_HOUSE_OVERRIDES:
                        house_overrides[str(override_house)] = {
                            "formed_by": sorted(list(rule["planets"])),
                            "masnui_planet": rule["result"],
                            **MASNUI_HOUSE_OVERRIDES[planet_pair]
                        }
                
                results.append(masnui_result)
    
    # Generate predictive notes based on house overrides
    predictive_notes = []
    for house_num, override_data in house_overrides.items():
        predictive_notes.append({
            "house": int(house_num),
            "note": override_data.get("predictive_note", {}),
            "affected_area": override_data.get("house_name", {})
        })
    
    # Calculate overall psychological profile
    psychological_profile = _calculate_masnui_psychological_profile(results)
    
    return {
        "masnui_planets": results,
        "house_overrides": house_overrides,
        "affected_houses": sorted(list(all_affected_houses)),
        "psychological_profile": psychological_profile,
        "predictive_notes": predictive_notes,
        "total_masnui": len(results)
    }


def _calculate_masnui_psychological_profile(masnui_results: List[Dict]) -> Dict[str, Any]:
    """
    Calculate overall psychological profile based on Masnui planets present.
    """
    if not masnui_results:
        return {
            "dominant_themes": [],
            "behavioral_tendencies": {"en": "Standard planetary influences", "hi": "मानक ग्रहीय प्रभाव"},
            "relationship_approach": {"en": "Based on natural planetary positions", "hi": "प्राकृतिक ग्रहीय स्थितियों पर आधारित"}
        }
    
    # Collect all qualities and themes
    qualities = [r.get("quality", "Good") for r in masnui_results]
    domains = [r.get("affected_domain", {}) for r in masnui_results]
    
    # Determine dominant quality
    khali_count = qualities.count("Khali Hawai")
    challenging_count = qualities.count("Challenging")
    mixed_count = qualities.count("Mixed")
    
    if khali_count >= 2:
        dominant_quality = {
            "en": "Khali Hawai (Empty Air) - Philosophical pretension without foundation",
            "hi": "खाली हवाई - बिना नींव के दार्शनिक दंभ"
        }
        behavioral = {
            "en": "Tendency to espouse high ideals while remaining materially attached. Thoughts without substance.",
            "hi": "भौतिक रूप से आसक्त रहते हुए उच्च आदर्शों का प्रचार करने की प्रवृत्ति। पदार्थ के बिना विचार।"
        }
    elif challenging_count >= 2:
        dominant_quality = {
            "en": "Intensified challenges requiring conscious integration",
            "hi": "सचेत एकीकरण की आवश्यकता वाली तीव्र चुनौतियां"
        }
        behavioral = {
            "en": "Sudden disruptions and intense ambition may create instability. Need for grounding practices.",
            "hi": "अचानक व्यवधान और तीव्र महत्वाकांक्षा अस्थिरता पैदा कर सकती है। भूमिका अभ्यास की आवश्यकता।"
        }
    elif mixed_count >= 1:
        dominant_quality = {
            "en": "Mixed influences requiring discernment",
            "hi": "विवेक की आवश्यकता वाले मिश्रित प्रभाव"
        }
        behavioral = {
            "en": "Both constructive and destructive potentials present. Context determines outcomes.",
            "hi": "रचनात्मक और विनाशकारी दोनों क्षमताएं मौजूद हैं। संदर्भ परिणाम निर्धारित करता है।"
        }
    else:
        dominant_quality = {
            "en": "Generally supportive artificial influences",
            "hi": "सामान्य रूप से सहायक कृत्रिम प्रभाव"
        }
        behavioral = {
            "en": "Enhanced capabilities in specific domains. Positive synergies active.",
            "hi": "विशिष्ट डोमेन में बढ़ी हुई क्षमताएं। सकारात्मक synergies सक्रिय।"
        }
    
    # Relationship approach based on house overrides
    has_7th_override = any(r.get("house_override") == 7 for r in masnui_results)
    has_2nd_override = any(r.get("house_override") == 2 for r in masnui_results)
    
    if has_7th_override:
        relationship = {
            "en": "Calculative approach to partnerships. Business-like arrangements may replace romance. Mercury periods trigger intellectualized relationship dynamics.",
            "hi": "साझेदारी के प्रति गणनात्मक दृष्टिकोण। व्यावसायिक व्यवस्थाएं रोमांस की जगह ले सकती हैं। बुध की अवधि बौद्धिकृत संबंध गतिशीलता को ट्रिगर करती है।"
        }
    elif has_2nd_override:
        relationship = {
            "en": "Restricted expansion in family matters. Speech patterns affected. Material desires without satisfaction capacity.",
            "hi": "पारिवारिक मामलों में प्रतिबंधित विस्तार। भाषण पैटर्न प्रभावित। संतुष्टि क्षमता के बिना भौतिक इच्छाएं।"
        }
    else:
        relationship = {
            "en": "Standard relationship dynamics modified by artificial planet qualities",
            "hi": "कृत्रिम ग्रह गुणों द्वारा संशोधित मानक संबंध गतिशीलता"
        }
    
    # Collect dominant themes
    dominant_themes = []
    for domain in domains:
        if domain:
            dominant_themes.append(domain)
    
    return {
        "dominant_themes": dominant_themes,
        "dominant_quality": dominant_quality,
        "behavioral_tendencies": behavioral,
        "relationship_approach": relationship,
        "masnui_count": len(masnui_results)
    }

def calculate_karmic_debts(planet_positions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Identifies the 9 types of Karmic Debts based on planetary triggers.
    Reference: PDF 2.3.1
    """
    # Helper to get planet's house
    p_map = {p["planet"]: p["house"] for p in planet_positions}
    
    # Helper to check if any of the planets are in a set of houses
    def in_houses(planets: List[str], houses: set) -> bool:
        return any(p_map.get(p) in houses for p in planets)

    debts = []

    # 1. Pitru Rin (Father's Debt)
    if in_houses(["Venus", "Mercury", "Rahu", "Ketu"], {2, 5, 9, 12}):
        debts.append({
            "name": {"hi": "पितृ ऋण", "en": "Pitru Rin"},
            "type": {"hi": "पिता / पूर्वज का ऋण", "en": "Father's / Forefather's Debt"},
            "reason": {"hi": "२, ५, ९, या १२वें भाव में शुक्र, बुध, राहु, या केतु", "en": "Venus, Mercury, Rahu, or Ketu in 2, 5, 9, or 12th house"},
            "manifestation": {"hi": "पारिवारिक इतिहास में मंदिर का विनाश, पीपल के पेड़ को नुकसान, पैतृक वंश में बाधाएं।", "en": "Temple destruction in family history, peepal tree damage, paternal lineage disruptions."},
            "remedy": {"hi": "पूरे परिवार से बराबर धन इकट्ठा करें और उसे एक ही दिन में किसी मंदिर में दान करें।", "en": "Collect equal money from all family members and donate it to a temple on the same day."}
        })

    # 2. Matru Rin (Mother's Debt)
    if p_map.get("Ketu") == 4:
        debts.append({
            "name": {"hi": "मातृ ऋण", "en": "Matru Rin"},
            "type": {"hi": "माता / मातृ ऋण", "en": "Mother's / Maternal Debt"},
            "reason": {"hi": "चौथे भाव में केतु", "en": "Ketu in 4th house"},
            "manifestation": {"hi": "मातृ उपेक्षा पैटर्न, माँ-बच्चे के संबंधों में कठिनाइयाँ, भावनात्मक सुरक्षा की कमी।", "en": "Maternal neglect patterns, mother-child relationship difficulties, emotional security deficits."},
            "remedy": {"hi": "पूरे परिवार से बराबर मात्रा में चांदी (या सिक्के) इकट्ठा करें और उसे बहते पानी में प्रवाहित करें।", "en": "Collect equal amounts of silver (or coins) from all family members and immerse it in flowing water."}
        })

    # 3. Sva Rin (Self Debt)
    if in_houses(["Venus", "Saturn", "Rahu"], {5}):
        debts.append({
            "name": {"hi": "स्व ऋण", "en": "Sva Rin"},
            "type": {"hi": "स्वयं का ऋण", "en": "Self Debt"},
            "reason": {"hi": "५वें भाव में शुक्र, शनि, या राहु", "en": "Venus, Saturn, or Rahu in 5th house"},
            "manifestation": {"hi": "नास्तिक प्रवृत्तियाँ, हृदय रोग, निर्दोष होने के बावजूद कानूनी दंड।", "en": "Atheistic tendencies, heart disease, legal penalties despite innocence."},
            "remedy": {"hi": "परिजनों से समान धन राशि एकत्र कर यज्ञ या सामूहिक पूजन कराएं।", "en": "Collect equal money from family members and perform a Yajna or community prayer."}
        })

    # 4. Bhratri Rin (Brother's Debt)
    if p_map.get("Mars") in {3, 6, 8, 12} and p_map.get("Saturn") in {3, 6, 8, 12}:
        debts.append({
            "name": {"hi": "भ्रातृ ऋण", "en": "Bhratri Rin"},
            "type": {"hi": "भाई / मित्र का ऋण", "en": "Brother's / Friend's Debt"},
            "reason": {"hi": "३, ६, ८, या १२वें भाव में मंगल और शनि", "en": "Mars and Saturn in 3, 6, 8, or 12th house"},
            "manifestation": {"hi": "बड़े भाई की अकाल मृत्यु, दोस्तों द्वारा विश्वासघात, भाई-बहनों द्वारा संपत्ति पर कब्जा।", "en": "Elder brother's early death, betrayal by friends, property seizure by siblings."},
            "remedy": {"hi": "परिजनों से समान मात्रा में तांबा या गुड़ एकत्र कर किसी धार्मिक स्थान पर दान करें।", "en": "Collect equal amounts of copper or jaggery from family members and donate to a religious place."}
        })

    # 5. Bhagini Rin (Sister's Debt)
    if p_map.get("Moon") in {3, 6} or (p_map.get("Rahu") in {3, 4, 6} and p_map.get("Mercury") in {3, 4, 6}):
        debts.append({
            "name": {"hi": "भगिनी ऋण", "en": "Bhagini Rin"},
            "type": {"hi": "बहन / पुत्री का ऋण", "en": "Sister's / Daughter's Debt"},
            "reason": {"hi": "३/६ में चंद्रमा या ३, ४, ६ में राहु-बुध की युति", "en": "Moon in 3/6 or Rahu-Mercury conjunction in 3, 4, 6"},
            "manifestation": {"hi": "बालिकाओं का शोषण, बहन के जन्म पर अशुभ घटनाएँ।", "en": "Exploitation of female children, inauspicious events at sister's birth."},
            "remedy": {"hi": "परिजनों से बराबर मात्रा में पीले रंग की कौड़ियाँ इकट्ठा करें, उन्हें जलाकर राख करें और उसी दिन बहते पानी में बहा दें।", "en": "Collect equal yellow sea shells (Kaudis) from family, burn them to ash, and immerse in flowing water on the same day."}
        })

    # 6. Deva Rin (Divine Debt)
    if p_map.get("Jupiter") in {6, 8, 12}:
        debts.append({
            "name": {"hi": "देव ऋण", "en": "Deva Rin"},
            "type": {"hi": "दिव्य / शिक्षक का ऋण", "en": "Divine / Teacher's Debt"},
            "reason": {"hi": "६, ८, या १२वें भाव में गुरु", "en": "Jupiter in 6, 8, or 12th house"},
            "manifestation": {"hi": "गुरु का विश्वासघात, पुजारी का अनादर, पवित्र वृक्ष का विनाश, गौ हत्या।", "en": "Guru betrayal, priest disrespect, sacred tree destruction, cow killing."},
            "remedy": {"hi": "परिजनों से बराबर मात्रा में हल्दी की गांठें या चने की दाल एकत्र कर किसी पुराने मंदिर में दान करें।", "en": "Collect equal pieces of turmeric or chana dal from family and donate to an old temple."}
        })

    # 7. Stree Rin (Women's Debt)
    if in_houses(["Sun", "Moon", "Rahu"], {2, 7}):
        debts.append({
            "name": {"hi": "स्त्री ऋण", "en": "Stree Rin"},
            "type": {"hi": "स्त्री ऋण", "en": "Women's Debt"},
            "reason": {"hi": "दूसरे या ७वें भाव में सूर्य, चंद्रमा, या राहु", "en": "Sun, Moon, or Rahu in 2nd or 7th house"},
            "manifestation": {"hi": "संबंधों में संघर्ष, विवाह में बाधाएं, महिलाओं के शोषण के पैटर्न।", "en": "Relationship conflicts, marriage obstacles, female exploitation patterns."},
            "remedy": {"hi": "परिजनों से बराबर धन एकत्र कर १०० सफेद गायों को एक समय का भोजन खिलाएं।", "en": "Collect equal money from family and feed 100 white cows once."}
        })

    # 8. Nara Rin (Humanity Debt)
    if p_map.get("Saturn") in {1, 2, 4, 7, 8, 12}:
        debts.append({
            "name": {"hi": "नरा ऋण", "en": "Nara Rin"},
            "type": {"hi": "मानवता का ऋण", "en": "Humanity Debt"},
            "reason": {"hi": "केंद्र या दुस्थान भावों में शनि", "en": "Saturn in angular or dusthana houses"},
            "manifestation": {"hi": "सामान्यीकृत जीवन बाधाएं, पुराना कष्ट, शापित होने की भावना।", "en": "Generalized life obstacles, chronic suffering, feeling of being cursed."},
            "remedy": {"hi": "परिजनों से बराबर राशि एकत्र कर अनाथालय या कोढ़ी आश्रम में दान करें।", "en": "Collect equal money from family and donate to an orphanage or leprosy center."}
        })

    # 9. Prakriti Rin (Nature Debt)
    if (p_map.get("Mercury") in {3, 6, 10, 12}) and (p_map.get("Rahu") in {3, 6, 10, 12} or p_map.get("Ketu") in {3, 6, 10, 12}):
        debts.append({
            "name": {"hi": "प्रकृति ऋण", "en": "Prakriti Rin"},
            "type": {"hi": "प्रकृति का ऋण", "en": "Nature Debt"},
            "reason": {"hi": "३, ६, १०, १२ में राहु/केतु के साथ पीड़ित बुध", "en": "Afflicted Mercury with Rahu/Ketu in 3, 6, 10, 12"},
            "manifestation": {"hi": "पिछले जन्मों में पर्यावरण का विनाश, पशु क्रूरता, प्राकृतिक आपदा की संवेदनशीलता।", "en": "Environmental destruction in past lives, animal cruelty, natural disaster vulnerability."},
            "remedy": {"hi": "परिजनों से बराबर धन एकत्र कर ४३ दिनों तक १०० कुत्तों को दूध और ब्रेड खिलाएं।", "en": "Collect equal money from family and feed 100 dogs milk and bread for 43 days."}
        })

    # Stamp every detected debt with its provenance tag. Rin triggers
    # are direct from the LK 1952 text → LK_CANONICAL.
    from app.lalkitab_source_tags import source_of
    src = source_of("calculate_karmic_debts")
    for d in debts:
        d.setdefault("source", src)
    return debts

def identify_teva_type(planet_positions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Detects Teva (chart typology): Andha, Ratondha, Dharmi, Nabalig, Khali.
    Reference: PDF 2.1.1, 2.1.2
    """
    p_map = {p["planet"]: p["house"] for p in planet_positions}
    CENTER_HOUSES = {1, 4, 7, 10}   # Kendra
    BENEFICS = {"Jupiter", "Venus", "Moon", "Mercury"}
    MALEFICS = {"Saturn", "Mars", "Rahu", "Ketu", "Sun"}

    # 1. Andha Teva (Blind Chart)
    ENEMY_PAIRS = [
        {"Sun", "Saturn"}, {"Sun", "Venus"}, {"Moon", "Rahu"},
        {"Mars", "Mercury"}, {"Mars", "Rahu"}, {"Jupiter", "Mercury"},
        {"Jupiter", "Venus"}, {"Saturn", "Moon"}
    ]
    planets_in_10 = {p["planet"] for p in planet_positions if p["house"] == 10}
    is_andha = False
    if len(planets_in_10) >= 2:
        for pair in ENEMY_PAIRS:
            if pair.issubset(planets_in_10):
                is_andha = True
                break

    # 2. Ratondha Teva (Half-Blind) — Sun in 4th + Saturn in 7th
    is_ratondha = (p_map.get("Sun") == 4 and p_map.get("Saturn") == 7)

    # 3. Dharmi Teva (Religious / Protected)
    is_dharmi = False
    if p_map.get("Jupiter") == p_map.get("Saturn") and p_map.get("Jupiter") is not None:
        is_dharmi = True
    elif (p_map.get("Jupiter") == 1 and p_map.get("Saturn") == 7) or (p_map.get("Jupiter") == 7 and p_map.get("Saturn") == 1):
        is_dharmi = True
    elif (p_map.get("Jupiter") == 4 and p_map.get("Saturn") == 10) or (p_map.get("Jupiter") == 10 and p_map.get("Saturn") == 4):
        is_dharmi = True
    elif p_map.get("Jupiter") in {6, 9, 11} or p_map.get("Saturn") in {9, 11}:
        is_dharmi = True

    # 4. Nabalig Teva (Underage/Immature Chart)
    # Trigger: 3 or more empty houses among 1,4,7,10 AND Jupiter/Moon not in kendra
    occupied_houses = {p["house"] for p in planet_positions}
    empty_kendra = CENTER_HOUSES - occupied_houses
    jup_moon_in_kendra = (p_map.get("Jupiter") in CENTER_HOUSES) or (p_map.get("Moon") in CENTER_HOUSES)
    is_nabalig = len(empty_kendra) >= 3 and not jup_moon_in_kendra

    # 5. Khali Teva (Empty Chart) — all 4 kendra empty
    is_khali = CENTER_HOUSES.issubset(set(range(1, 13)) - occupied_houses)

    # Active types list
    active_types = []
    if is_andha:    active_types.append("andha")
    if is_ratondha: active_types.append("ratondha")
    if is_dharmi:   active_types.append("dharmi")
    if is_nabalig:  active_types.append("nabalig")
    if is_khali:    active_types.append("khali")

    return {
        "is_andha":    is_andha,
        "is_ratondha": is_ratondha,
        "is_dharmi":   is_dharmi,
        "is_nabalig":  is_nabalig,
        "is_khali":    is_khali,
        "active_types": active_types,
        "description": {
            "andha": {
                "hi": "करियर और सार्वजनिक छवि में मौलिक बाधा। सफलता के लिए गहन शनिवार के उपायों की आवश्यकता है।" if is_andha else "सामान्य कुंडली दृष्टि।",
                "en": "Fundamental obstruction in career and public image. Success requires intensive Saturday remedies." if is_andha else "Normal chart vision."
            },
            "ratondha": {
                "hi": "रात में काम करने या अनैतिक कार्यों से भाग्य की हानि। दिन के समय की गतिविधियाँ ही फलदायी होंगी।" if is_ratondha else "सामान्य समय-चक्र प्रभाव।",
                "en": "Loss of fortune through night-work or unethical deeds. Daytime activities will be fruitful." if is_ratondha else "Standard time-cycle influence."
            },
            "dharmi": {
                "hi": "पूर्व जन्म के पुण्यों से जन्मजात सुरक्षा। यहाँ तक कि पापी ग्रह भी 'धर्मी ग्रह' (सुरक्षात्मक) के रूप में कार्य करते हैं।" if is_dharmi else "मानक कर्मिक प्रतिक्रिया।",
                "en": "Innate protection from past merit. Even malefic planets act as 'Dharmi Grah' (protective)." if is_dharmi else "Standard karmic responsiveness."
            },
            "nabalig": {
                "hi": "अपरिपक्व कुंडली — प्रमुख क्षेत्रों (1,4,7,10) में अनुभव और गुरु का मार्गदर्शन आवश्यक। बड़ों का सहयोग सफलता लाएगा।" if is_nabalig else "परिपक्व केंद्र बल।",
                "en": "Immature chart — guidance from elders and Jupiter's grace needed in core life areas. Avoid solo decisions on major life matters." if is_nabalig else "Mature kendra strength."
            },
            "khali": {
                "hi": "खाली केंद्र — जीवन के मुख्य चार क्षेत्रों (स्वयं, घर, साझेदारी, करियर) में ग्रह बल की कमी। आध्यात्मिक साधना से रिक्तता भरें।" if is_khali else "केंद्र में ग्रह बल उपस्थित।",
                "en": "Empty chart — the four pillars of life (self, home, partnerships, career) have no direct planetary occupancy. Fill this void through spiritual practice and service." if is_khali else "Kendra has planetary occupancy."
            },
        }
    }

# ============================================================
# 5. LAL KITAB ASPECTS (DRISHTI)
# One-way fixed house aspects. Reference: PDF structural
# ============================================================

LK_ASPECTS = {
    1:  {7: 1.0},
    4:  {10: 1.0},
    7:  {1: 1.0},
    10: {4: 1.0},
    3:  {9: 0.5, 11: 0.5},
    5:  {9: 0.5},
    2:  {6: 0.25},
    6:  {12: 0.25},
    8:  {12: 0.25},
}

def calculate_lk_aspects(planet_positions: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Calculates one-way Lal Kitab aspects between planets.
    """
    house_to_planets = {}
    for p in planet_positions:
        h = p["house"]
        if h not in house_to_planets: house_to_planets[h] = []
        house_to_planets[h].append(p["planet"])

    aspects = {p["planet"]: [] for p in planet_positions}

    for p in planet_positions:
        source_h = p["house"]
        if source_h in LK_ASPECTS:
            for target_h, strength in LK_ASPECTS[source_h].items():
                target_planets = house_to_planets.get(target_h, [])
                for tp in target_planets:
                    aspects[p["planet"]].append({
                        "aspects_to": tp,
                        "house": target_h,
                        "strength": strength
                    })
    
    return aspects

# ============================================================
# 6. SLEEPING PLANETS & HOUSES (SOYA GRAH / GHAR)
# ============================================================

def calculate_sleeping_status(planet_positions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Identifies which houses and planets are 'sleeping' (inactive).
    """
    occupied_houses = {p["house"] for p in planet_positions}
    
    # 1. Sleeping Houses
    sleeping_houses = []
    for h in range(1, 13):
        if h not in occupied_houses:
            # Special activation rules
            is_sleeping = True
            if h == 1 and 7 in occupied_houses: is_sleeping = False
            if h == 2 and 8 in occupied_houses: is_sleeping = False
            if h == 3 and 9 in occupied_houses: is_sleeping = False
            if h == 4 and 10 in occupied_houses: is_sleeping = False
            
            if is_sleeping:
                sleeping_houses.append(h)

    # 2. Sleeping Planets (Soya Grah)
    ACTIVATION_HOUSE = {1: 7, 2: 8, 3: 9, 4: 10, 5: 11, 6: 12, 7: 1, 8: 2, 9: 3, 10: 4, 11: 5, 12: 6}
    
    sleeping_planets = []
    for p in planet_positions:
        name = p["planet"]
        h = p["house"]
        activation_h = ACTIVATION_HOUSE.get(h)
        
        if activation_h not in occupied_houses:
            sleeping_planets.append({
                "planet": name,
                "reason": {
                    "en": f"No planet in activation house {activation_h}",
                    "hi": f"सक्रियण भाव {activation_h} में कोई ग्रह नहीं है"
                },
                "trigger": {
                    "en": f"Wakes up when a planet enters house {activation_h}",
                    "hi": f"भाव {activation_h} में किसी ग्रह के प्रवेश करने पर सक्रिय होगा"
                }
            })

    return {
        "sleeping_houses": sleeping_houses,
        "sleeping_planets": sleeping_planets
    }

# ============================================================
# 7. KAYAM GRAH (ESTABLISHED PLANETS)
# ============================================================

def calculate_kayam_grah(planet_positions: List[Dict[str, Any]], lk_aspects: Dict[str, List[Dict[str, Any]]]) -> List[str]:
    """
    A planet is Kayam if it is not aspected by any enemy planet.
    """
    ENEMIES = {
        "Sun": {"Saturn", "Venus", "Rahu", "Ketu"},
        "Moon": {"Rahu", "Ketu"},
        "Mars": {"Mercury", "Ketu"},
        "Mercury": {"Moon"},
        "Jupiter": {"Mercury", "Venus"},
        "Venus": {"Sun", "Moon", "Rahu"},
        "Saturn": {"Sun", "Moon", "Mars"},
        "Rahu": {"Sun", "Moon", "Jupiter"},
        "Ketu": {"Moon", "Mars"},
    }
    
    kayam = []
    for p in planet_positions:
        name = p["planet"]
        aspected_by_enemies = False
        
        for source_p, targets in lk_aspects.items():
            for t in targets:
                if t["aspects_to"] == name:
                    if source_p in ENEMIES.get(name, set()):
                        aspected_by_enemies = True
                        break
            if aspected_by_enemies: break
            
        if not aspected_by_enemies:
            kayam.append(name)
            
    return kayam

def get_prohibitions(planet_positions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Returns a list of forbidden actions/remedies based on house placements.
    Reference: PDF 2.4.1
    """
    p_map = {p["planet"]: p["house"] for p in planet_positions}
    prohibitions = []

    rules = [
        {
            "planet": "Moon", "house": {12}, "category": {"en": "Religious charity", "hi": "धार्मिक दान"}, 
            "item": {"en": "Donations to saints, temple construction", "hi": "साधु-संतों को दान, मंदिर निर्माण"}, 
            "risk": {"en": "Mental health crisis, poverty", "hi": "मानसिक स्वास्थ्य संकट, गरीबी"}
        },
        {
            "planet": "Jupiter", "house": {7}, "category": {"en": "Clothing charity", "hi": "वस्त्र दान"}, 
            "item": {"en": "Any clothing donation", "hi": "किसी भी प्रकार का वस्त्र दान"}, 
            "risk": {"en": "Financial loss, partnership destruction", "hi": "आर्थिक हानि, साझेदारी का विनाश"}
        },
        {
            "planet": "Sun", "house": {7, 8}, "category": {"en": "Timed donations", "hi": "समयबद्ध दान"}, 
            "item": {"en": "Morning/Evening donations specifically", "hi": "विशेष रूप से सुबह/शाम का दान"}, 
            "risk": {"en": "Authority loss, health crisis", "hi": "अधिकार की हानि, स्वास्थ्य संकट"}
        },
        {
            "planet": "Venus", "house": {9}, "category": {"en": "Female-targeted charity", "hi": "स्त्री-केंद्रित दान"}, 
            "item": {"en": "Financial aid to widows/poor girls", "hi": "विधवाओं/गरीब लड़कियों को वित्तीय सहायता"}, 
            "risk": {"en": "Progeny obstruction, marital conflict", "hi": "संतान प्राप्ति में बाधा, वैवाहिक कलह"}
        },
        {
            "planet": "Saturn", "house": {4}, "category": {"en": "Oil/Alcohol", "hi": "तेल/शराब"}, 
            "item": {"en": "Oil donations, serving liquor", "hi": "तेल का दान, शराब परोसना"}, 
            "risk": {"en": "Mother's health, property loss", "hi": "माता का स्वास्थ्य, संपत्ति की हानि"}
        },
        {
            "planet": "Mars", "house": {8}, "category": {"en": "Red/Copper", "hi": "लाल वस्तुएं/तांबा"}, 
            "item": {"en": "Red cloth, copper vessels", "hi": "लाल कपड़ा, तांबे के बर्तन"}, 
            "risk": {"en": "Accident proneness, blood diseases", "hi": "दुर्घटना की संभावना, रक्त रोग"}
        },
        {
            "planet": "Rahu", "house": {6}, "category": {"en": "Dark items", "hi": "काली वस्तुएं"}, 
            "item": {"en": "Blue/Black cloth, gemstone gifts", "hi": "नीला/काला कपड़ा, रत्न उपहार में देना"}, 
            "risk": {"en": "Legal entanglement, chronic disease", "hi": "कानूनी उलझन, पुरानी बीमारी"}
        },
        {
            "planet": "Ketu", "house": {12}, "category": {"en": "Warmth charity", "hi": "गर्मी/ऊनी दान"}, 
            "item": {"en": "Blankets, heating equipment", "hi": "कंबल, हीटिंग उपकरण"}, 
            "risk": {"en": "Sleep disorders, spiritual confusion", "hi": "नींद में खलल, आध्यात्मिक भ्रम"}
        },
        {
            "planet": "Mercury", "house": {3, 8, 9, 12}, "category": {"en": "Green items", "hi": "हरी वस्तुएं"}, 
            "item": {"en": "Money plant, green cloth, emerald", "hi": "मनी प्लांट, हरा कपड़ा, पन्ना"}, 
            "risk": {"en": "Sibling conflict, travel accidents", "hi": "भाई-बैनों से विवाद, यात्रा दुर्घटनाएं"}
        },
        {
            "planet": "Saturn", "house": {10}, "category": {"en": "Construction", "hi": "निर्माण"}, 
            "item": {"en": "House construction before age 48", "hi": "४८ वर्ष की आयु से पहले घर का निर्माण"}, 
            "risk": {"en": "Complete wealth destruction", "hi": "धन का पूर्ण विनाश"}
        },
        {
            "planet": "Jupiter", "house": {10}, "category": {"en": "Sympathetic feeding", "hi": "सह सहानुभूति भोजन"}, 
            "item": {"en": "Feeding others with emotional display", "hi": "भावनात्मक प्रदर्शन के साथ दूसरों को खिलाना"}, 
            "risk": {"en": "Severe suffering (Acts like poison)", "hi": "गंभीर कष्ट (जहर की तरह काम करता है)"}
        },
    ]

    for rule in rules:
        h = p_map.get(rule["planet"])
        if h in rule["house"]:
            prohibitions.append({
                "planet": rule["planet"],
                "house": h,
                "forbidden": rule["item"],
                "category": rule["category"],
                "backlash_risk": rule["risk"]
            })

    return prohibitions




# ============================================================
# PLANETARY HOURS (HORA) KARMIC DEBT CALCULATION
# Reference: PDF 2.3.2
# ============================================================

# Chaldean order of planets by speed (slowest to fastest)
CHALDEAN_ORDER = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]

# Day of week → Day Lord mapping (0=Monday)
DAY_LORDS = {
    0: "Moon",    # Monday
    1: "Mars",    # Tuesday
    2: "Mercury", # Wednesday
    3: "Jupiter", # Thursday
    4: "Venus",   # Friday
    5: "Saturn",  # Saturday
    6: "Sun"      # Sunday
}

# Base Hora lord → Debt association mapping
HORA_DEBT_MAPPING = {
    "Saturn": {
        "debt": "Nara Rin",
        "debt_hi": "नरा ऋण",
        "description": {
            "en": "Base Humanity Debt - chronic suffering, feeling cursed",
            "hi": "आधार मानवता ऋण - पुराना कष्ट, शापित महसूस होना"
        }
    },
    "Jupiter": {
        "debt": "Pitru Rin",
        "debt_hi": "पितृ ऋण",
        "description": {
            "en": "Base Father's Debt - ancestral karmic obligations",
            "hi": "आधार पितृ ऋण - पैतृक कर्मिक दायित्व"
        }
    },
    "Mars": {
        "debt": "Bhratri Rin",
        "debt_hi": "भ्रातृ ऋण",
        "description": {
            "en": "Base Brother's Debt - sibling/friendship betrayal patterns",
            "hi": "आधार भ्रातृ ऋण - भाई-बहन/मित्रता विश्वासघात पैटर्न"
        }
    },
    "Sun": {
        "debt": "Sva Rin",
        "debt_hi": "स्व ऋण",
        "description": {
            "en": "Base Self Debt - misuse of authority/ego in past lives",
            "hi": "आधार स्व ऋण - पिछले जन्मों में अधिकार/अहंकार का दुरुपयोग"
        }
    },
    "Venus": {
        "debt": "Stree Rin",
        "debt_hi": "स्त्री ऋण",
        "description": {
            "en": "Base Women's Debt - exploitation of feminine energy",
            "hi": "आधार स्त्री ऋण - स्त्री ऊर्जा का शोषण"
        }
    },
    "Mercury": {
        "debt": "Bhagini Rin",
        "debt_hi": "भगिनी ऋण",
        "description": {
            "en": "Base Sister's Debt - exploitation of female relatives",
            "hi": "आधार भगिनी ऋण - महिला रिश्तेदारों का शोषण"
        }
    },
    "Moon": {
        "debt": "Matru Rin",
        "debt_hi": "मातृ ऋण",
        "description": {
            "en": "Base Mother's Debt - maternal relationship disruptions",
            "hi": "आधार मातृ ऋण - मातृ संबंध व्यवधान"
        }
    }
}

# Conflict modification rules: (Day Lord, Hora Lord) → Modified Debt
CONFLICT_MODIFICATIONS = {
    # Mars day + Saturn Hora OR Saturn day + Mars Hora → Rahu (Shadow Debt)
    ("Mars", "Saturn"): {
        "modified_debt": "Ketu Rin / Shadow Debt",
        "modified_debt_hi": "केतु ऋण / छाया ऋण",
        "reason": {
            "en": "Day Mars + Hora Saturn explosive friction creates unpredictable karmic pattern",
            "hi": "मंगल वार + शनि होरा विस्फोटक घर्षण अप्रत्याशित कर्मिक पैटर्न बनाता है"
        },
        "manifestation": {
            "en": "Sudden upheavals, hidden enemies, spiritual confusion requiring detachment practices",
            "hi": "अचानक उथल-पुथल, छिपे शत्रु, वैराग्य अभ्यास की आवश्यकता वाला आध्यात्मिक भ्रम"
        }
    },
    ("Saturn", "Mars"): {
        "modified_debt": "Ketu Rin / Shadow Debt",
        "modified_debt_hi": "केतु ऋण / छाया ऋण",
        "reason": {
            "en": "Day Saturn + Hora Mars creates explosive, unpredictable karmic friction",
            "hi": "शनि वार + मंगल होरा विस्फोटक, अप्रत्याशित कर्मिक घर्षण पैदा करता है"
        },
        "manifestation": {
            "en": "Restriction followed by sudden release, authority conflicts, need for spiritual surrender",
            "hi": "अचानक मुक्ति के बाद प्रतिबंध, अधिकार संघर्ष, आध्यात्मिक समर्पण की आवश्यकता"
        }
    },
    # Mars day + Mercury Hora → Ketu (Divine/Spiritual Debt)
    ("Mars", "Mercury"): {
        "modified_debt": "Deva Rin / Divine Debt",
        "modified_debt_hi": "देव ऋण / दिव्य ऋण",
        "reason": {
            "en": "Mars day + Mercury Hora triggers spiritual lesson through communication/intellectual conflict",
            "hi": "मंगल वार + बुध होरा संचार/बौद्धिक संघर्ष के माध्यम से आध्यात्मिक सबक को ट्रिगर करता है"
        },
        "manifestation": {
            "en": "Guru betrayal patterns, learning difficulties, need for humility in knowledge",
            "hi": "गुरु विश्वासघात पैटर्न, सीखने में कठिनाइयां, ज्ञान में विनम्रता की आवश्यकता"
        }
    },
    # Enhanced effects (not full modification but intensity changes)
    ("Friday", "Venus"): {
        "enhancement": True,
        "effect": {
            "en": "Stree Rin intensity increased - Friday birth with Venus Hora amplifies feminine debt",
            "hi": "स्त्री ऋण तीव्रता बढ़ी - शुक्रवार जन्म शुक्र होरा के साथ स्त्री ऋण को बढ़ाता है"
        }
    },
    ("Monday", "Moon"): {
        "enhancement": True,
        "effect": {
            "en": "Matru Rin intensity increased - Monday birth with Moon Hora amplifies maternal debt",
            "hi": "मातृ ऋण तीव्रता बढ़ी - सोमवार जन्म चंद्रमा होरा के साथ मातृ ऋण को बढ़ाता है"
        }
    }
}


def calculate_hora_lord(
    birth_datetime,
    sunrise_time=None,
    longitude=None,
    latitude=None
) -> Dict[str, Any]:
    """
    Calculate the Hora (Planetary Hour) lord at birth time.
    
    The Chaldean order cycles through the day starting from the day lord.
    Each hour is approximately 60 minutes (varies by daylight length).
    
    Args:
        birth_datetime: Python datetime object
        sunrise_time: REQUIRED real sunrise time for the birth date + location
                      (datetime.time object). If None, Hora debt is not computed —
                      the function returns {"hora_lord": None, "_skipped": True, ...}
                      so callers can surface "hora_debt_available: False" to the UI.
        longitude: Optional longitude (informational only — caller must compute
                   sunrise and pass it in via sunrise_time).
        latitude: Optional latitude (informational only — see longitude).

    Returns:
        Dict with hora_lord, day_lord, hours_elapsed, conflict_info.
        When sunrise_time is None, returns {"hora_lord": None, "_skipped": True,
        "reason": "sunrise not provided"} instead of silently falling back.
    """
    from datetime import datetime, time

    # Get day of week and day lord (still valid without sunrise)
    weekday = birth_datetime.weekday()  # 0=Monday
    day_lord = DAY_LORDS[weekday]

    # Honest guard: without a real sunrise we cannot compute the Hora cycle.
    # Returning a skip sentinel here lets callers mark
    # hora_debt_available=False instead of presenting a 06:00-fallback lie.
    if sunrise_time is None:
        return {
            "hora_lord": None,
            "day_lord": day_lord,
            "weekday": weekday,
            "weekday_name": birth_datetime.strftime("%A"),
            "hours_elapsed_since_sunrise": None,
            "minutes_into_hour": None,
            "boundary_warning": None,
            "conflict_modification": None,
            "base_debt": {},
            "_skipped": True,
            "reason": {
                "en": "Hora debt not computed — real sunrise (date + lat/lon) was not provided.",
                "hi": "होरा ऋण की गणना नहीं की गई — वास्तविक सूर्योदय (तिथि + अक्षांश/देशांतर) उपलब्ध नहीं था।",
            },
        }

    sunrise = datetime.combine(birth_datetime.date(), sunrise_time)

    # Calculate hours elapsed since sunrise
    # Handle case where birth is before sunrise (previous day's cycle)
    if birth_datetime < sunrise:
        # Use previous day's cycle - approximate yesterday's sunrise with the
        # same sunrise_time (adequate within minutes for a 1-day delta).
        from datetime import timedelta
        yesterday = birth_datetime - timedelta(days=1)
        sunrise = datetime.combine(yesterday.date(), sunrise_time)
    
    elapsed = birth_datetime - sunrise
    hours_elapsed = elapsed.total_seconds() / 3600.0
    
    # Find starting position in Chaldean order based on day lord
    day_lord_index = CHALDEAN_ORDER.index(day_lord)
    
    # Calculate which planet rules the current hour
    # The sequence starts from day lord and cycles through Chaldean order
    hora_index = (day_lord_index + int(hours_elapsed)) % 7
    hora_lord = CHALDEAN_ORDER[hora_index]
    
    # Check for Hora boundary (within 10 minutes = warning)
    minutes_into_hour = (hours_elapsed % 1) * 60
    boundary_warning = None
    if minutes_into_hour < 10:
        boundary_warning = {
            "type": "approaching_transition",
            "message": {
                "en": f"Birth occurred {minutes_into_hour:.1f} minutes into {hora_lord} Hora. "
                      f"If birth time uncertainty exceeds {(10-minutes_into_hour):.1f} minutes, "
                      f"previous Hora lord ({CHALDEAN_ORDER[(hora_index-1)%7]}) should be considered.",
                "hi": f"जन्म {hora_lord} होरा में {minutes_into_hour:.1f} मिनट बाद हुआ। "
                      f"यदि जन्म समय की अनिश्चितता {(10-minutes_into_hour):.1f} मिनट से अधिक है, "
                      f"पिछले होरा स्वामी ({CHALDEAN_ORDER[(hora_index-1)%7]}) पर विचार करना चाहिए।"
            },
            "uncertainty_threshold_minutes": 10 - minutes_into_hour
        }
    elif minutes_into_hour > 50:
        next_lord = CHALDEAN_ORDER[(hora_index + 1) % 7]
        boundary_warning = {
            "type": "approaching_next",
            "message": {
                "en": f"Birth occurred {minutes_into_hour:.1f} minutes into {hora_lord} Hora. "
                      f"If birth time uncertainty exceeds {(60-minutes_into_hour):.1f} minutes, "
                      f"next Hora lord ({next_lord}) should be considered.",
                "hi": f"जन्म {hora_lord} होरा में {minutes_into_hour:.1f} मिनट बाद हुआ। "
                      f"यदि जन्म समय की अनिश्चितता {(60-minutes_into_hour):.1f} मिनट से अधिक है, "
                      f"अगले होरा स्वामी ({next_lord}) पर विचार करना चाहिए।"
            },
            "uncertainty_threshold_minutes": 60 - minutes_into_hour
        }
    
    # Check for conflict modifications
    conflict_info = None
    conflict_key = (day_lord, hora_lord)
    if conflict_key in CONFLICT_MODIFICATIONS:
        conflict_info = CONFLICT_MODIFICATIONS[conflict_key]
        conflict_info["trigger"] = f"{day_lord} day + {hora_lord} Hora"
    
    return {
        "hora_lord": hora_lord,
        "day_lord": day_lord,
        "weekday": weekday,
        "weekday_name": birth_datetime.strftime("%A"),
        "hours_elapsed_since_sunrise": round(hours_elapsed, 2),
        "minutes_into_hour": round(minutes_into_hour, 1),
        "boundary_warning": boundary_warning,
        "conflict_modification": conflict_info,
        "base_debt": HORA_DEBT_MAPPING.get(hora_lord, {})
    }


# ============================================================
# BUNYAAD (FOUNDATION HOUSE) ANALYSIS
# ============================================================

# Pakka Ghar (Permanent House) for each planet in Lal Kitab
PAKKA_GHAR = {
    "Sun": 1,
    "Moon": 4,
    "Mars": 3,
    "Mercury": 7,
    "Jupiter": 2,
    "Venus": 7,
    "Saturn": 8,
    "Rahu": 12,
    "Ketu": 6,
}

# Lal Kitab enemy relationships (used across bunyaad, takkar, enemy presence)
LK_ENEMIES = {
    "Sun": {"Saturn", "Rahu", "Ketu"},
    "Moon": {"Rahu", "Ketu"},
    "Mars": {"Mercury", "Ketu"},
    "Mercury": {"Moon", "Ketu"},
    "Jupiter": {"Mercury", "Venus", "Rahu", "Ketu", "Saturn"},
    "Venus": {"Sun", "Moon", "Rahu"},
    "Saturn": {"Sun", "Moon", "Mars"},
    "Rahu": {"Sun", "Moon", "Jupiter"},
    "Ketu": {"Moon", "Mars"},
}

# Canonical LK friendship table per Codex R2-P5 audit.
# Used by bunyaad to decide truly-strong foundations (friendly planets
# present) vs merely-not-hostile (neutrals).
LK_FRIENDS = {
    "Sun":     {"Moon", "Mars", "Jupiter"},
    "Moon":    {"Sun", "Mercury"},
    "Mars":    {"Sun", "Moon", "Jupiter"},
    "Mercury": {"Sun", "Venus"},
    "Jupiter": {"Sun", "Moon", "Mars"},
    "Venus":   {"Mercury", "Saturn"},
    "Saturn":  {"Mercury", "Venus", "Rahu"},
    # Rahu/Ketu are not explicitly classified in Codex's list;
    # we take the reciprocal of Saturn's entry and leave Ketu empty.
    "Rahu":    {"Saturn"},
    "Ketu":    set(),
}

# Bunyaad house = 9th from pakka ghar (precomputed)
BUNYAAD_HOUSE = {planet: ((ghar - 1 + 8) % 12) + 1 for planet, ghar in PAKKA_GHAR.items()}


def calculate_bunyaad(planet_positions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    For each planet, calculate its bunyaad (foundation house) and check if it's afflicted.

    Bunyaad house = 9th house from the planet's pakka ghar (permanent house).

    Returns a dict with per-planet bunyaad analysis, collapsed planets, and strong foundations.
    """
    # Build house → planets map
    house_map: Dict[int, List[str]] = {}
    for p in planet_positions:
        h = p.get("house")
        name = p.get("planet", "")
        if h and name:
            house_map.setdefault(h, []).append(name)

    planets_result: Dict[str, Dict[str, Any]] = {}
    collapsed_planets: List[str] = []
    strong_foundations: List[str] = []

    all_planet_names = [p["planet"] for p in planet_positions if p.get("planet") in PAKKA_GHAR]

    neutral_foundations: List[str] = []
    clear_foundations: List[str] = []

    for planet_name in all_planet_names:
        pakka = PAKKA_GHAR[planet_name]
        bunyaad_h = BUNYAAD_HOUSE[planet_name]
        # A planet standing in its own bunyaad does NOT support itself —
        # exclude self-presence from the foundation check.
        planets_in_bunyaad = [
            p for p in house_map.get(bunyaad_h, []) if p != planet_name
        ]
        enemies = LK_ENEMIES.get(planet_name, set())
        friends = LK_FRIENDS.get(planet_name, set())
        enemies_in_bunyaad = [p for p in planets_in_bunyaad if p in enemies]
        friends_in_bunyaad = [p for p in planets_in_bunyaad if p in friends]
        neutrals_in_bunyaad = [
            p for p in planets_in_bunyaad
            if p not in enemies and p not in friends
        ]

        # Codex R2-P5 rule:
        #   enemies present  → afflicted
        #   friends present  → strong  (truly reinforces the foundation)
        #   only neutrals    → neutral (workable, not reinforcing)
        #   empty            → clear   (default safe, no interference)
        if enemies_in_bunyaad:
            bunyaad_status = "afflicted"
            collapsed_planets.append(planet_name)
            en_list = ", ".join(enemies_in_bunyaad)
            hi_list = ", ".join(enemies_in_bunyaad)
            interpretation_en = (
                f"{planet_name}'s foundation (House {bunyaad_h}) is afflicted by {en_list}. "
                f"Despite its own placement, {planet_name}'s results collapse under enemy pressure."
            )
            interpretation_hi = (
                f"{planet_name} की बुनियाद (भाव {bunyaad_h}) पर दुश्मन {hi_list} का कब्ज़ा है। "
                f"अपनी जगह अच्छी होने के बावजूद {planet_name} के फल नष्ट होंगे।"
            )
        elif friends_in_bunyaad:
            bunyaad_status = "strong"
            strong_foundations.append(planet_name)
            fr_list = ", ".join(friends_in_bunyaad)
            interpretation_en = (
                f"{planet_name}'s foundation (House {bunyaad_h}) is reinforced by friendly "
                f"planet(s) {fr_list}. Foundation is genuinely strong — {planet_name}'s "
                f"results are actively supported."
            )
            interpretation_hi = (
                f"{planet_name} की बुनियाद (भाव {bunyaad_h}) में मित्र ग्रह {fr_list} हैं। "
                f"बुनियाद वास्तव में मज़बूत है — {planet_name} के फल सक्रिय रूप से समर्थित।"
            )
        elif neutrals_in_bunyaad:
            bunyaad_status = "neutral"
            neutral_foundations.append(planet_name)
            ne_list = ", ".join(neutrals_in_bunyaad)
            interpretation_en = (
                f"{planet_name}'s foundation (House {bunyaad_h}) has only neutral planet(s) "
                f"{ne_list} — no enemy pressure, but no active reinforcement either. "
                f"Foundation is workable, not uplifting."
            )
            interpretation_hi = (
                f"{planet_name} की बुनियाद (भाव {bunyaad_h}) में केवल तटस्थ ग्रह {ne_list} हैं — "
                f"शत्रुता नहीं, पर सक्रिय समर्थन भी नहीं। बुनियाद टिकाऊ है, पर उत्थानशील नहीं।"
            )
        else:
            bunyaad_status = "clear"
            clear_foundations.append(planet_name)
            interpretation_en = (
                f"{planet_name}'s foundation (House {bunyaad_h}) is empty. "
                f"No enemy interference — foundation is clear by default."
            )
            interpretation_hi = (
                f"{planet_name} की बुनियाद (भाव {bunyaad_h}) खाली है। "
                f"कोई दुश्मन नहीं — बुनियाद सुरक्षित है।"
            )

        planets_result[planet_name] = {
            "pakka_ghar": pakka,
            "bunyaad_house": bunyaad_h,
            "bunyaad_status": bunyaad_status,
            "planets_in_bunyaad": planets_in_bunyaad,
            "friends_in_bunyaad": friends_in_bunyaad,
            "enemies_in_bunyaad": enemies_in_bunyaad,
            "neutrals_in_bunyaad": neutrals_in_bunyaad,
            "interpretation_en": interpretation_en,
            "interpretation_hi": interpretation_hi,
        }

    return {
        "planets": planets_result,
        "collapsed_planets": collapsed_planets,
        "strong_foundations": strong_foundations,
        "neutral_foundations": neutral_foundations,
        "clear_foundations": clear_foundations,
    }


# ============================================================
# TAKKAR (COLLISION) ANALYSIS — LAL KITAB OPPOSITE-AXIS RULE
# ============================================================
#
# Lal Kitab Takkar is strictly across OPPOSITE (7th-from) houses:
#   H1 ↔ H7   H2 ↔ H8   H3 ↔ H9
#   H4 ↔ H10  H5 ↔ H11  H6 ↔ H12
#
# A takkar is flagged only when two planets sit on the SAME axis —
# i.e. when |house_a - house_b| == 6.  The "1-8 / 1-6 axis" rule used
# previously was Vedic-influenced and produced false positives (e.g.
# Moon H8 vs Rahu H1, which are on DIFFERENT axes).  Severity is
# determined by the standard LK enemy matrix:
#   enemies → destructive   friends/neutrals → mild

def calculate_takkar(planet_positions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Detect opposite-axis takkar between planets (LK rule).

    Rule: planet A in house H and planet B in house (H+6 mod 12) are on
    the same LK axis and form a takkar. Each axis pair is reported once.

    Severity is conditional on both the enemy relationship AND the
    dignity of each planet (Codex audit R2-P3):
      - enemies + BOTH afflicted (debilitated / in enemy sign)
                                         → "destructive"
      - enemies but AT LEAST ONE strong  → "mild friction"
                                           (Exalted / Own / Friendly)
      - not LK enemies                   → "philosophical conflict"
                                           (axis tension, no harm)
    """
    from app.lalkitab_engine import _get_dignity_label  # local import to avoid cycle

    # Classify a planet as afflicted / strong from its sign.
    def _affliction_state(planet: str, sign: str) -> str:
        dignity = _get_dignity_label(planet, sign) if sign else "Neutral"
        if dignity in ("Debilitated", "Enemy"):
            return "afflicted"
        if dignity in ("Exalted", "Own Sign", "Friendly"):
            return "strong"
        return "neutral"

    collisions: List[Dict[str, Any]] = []
    attack_count: Dict[str, int] = {}

    all_planets = [p for p in planet_positions if p.get("planet") in LK_ENEMIES]

    # Initialize attack count
    for p in all_planets:
        attack_count[p["planet"]] = 0

    # Check unordered pairs; each pair is emitted once with a symmetric axis label.
    for i, pa in enumerate(all_planets):
        for j in range(i + 1, len(all_planets)):
            pb = all_planets[j]
            ha, hb = pa.get("house"), pb.get("house")
            if not isinstance(ha, int) or not isinstance(hb, int):
                continue

            # Opposite-axis rule: houses exactly 6 positions apart.
            if abs(ha - hb) != 6:
                continue

            a_name, b_name = pa["planet"], pb["planet"]
            are_enemies = (
                b_name in LK_ENEMIES.get(a_name, set())
                or a_name in LK_ENEMIES.get(b_name, set())
            )

            # Dignity-aware severity ladder
            state_a = _affliction_state(a_name, pa.get("sign", ""))
            state_b = _affliction_state(b_name, pb.get("sign", ""))
            both_afflicted = state_a == "afflicted" and state_b == "afflicted"
            any_strong = state_a == "strong" or state_b == "strong"

            if are_enemies and both_afflicted:
                severity = "destructive"
            elif are_enemies and any_strong:
                severity = "mild friction"
            elif are_enemies:
                # enemies + both neutral → between destructive & mild
                severity = "moderate friction"
            else:
                severity = "philosophical conflict"

            # Axis label is always the lower-numbered house first.
            low, high = (ha, hb) if ha < hb else (hb, ha)
            axis_label = f"{low}-{high}"

            if severity == "destructive":
                interp_en = (
                    f"{a_name} (H{ha}, {state_a}) and {b_name} (H{hb}, {state_b}) are on the "
                    f"{axis_label} axis. Both planets are LK enemies AND afflicted — their "
                    f"significations will actively undermine each other across this axis."
                )
                interp_hi = (
                    f"{a_name} (भाव {ha}, {state_a}) और {b_name} (भाव {hb}, {state_b}) "
                    f"{axis_label} अक्ष पर शत्रु हैं और दोनों पीड़ित — एक-दूसरे के फलों को "
                    f"सक्रिय रूप से कमज़ोर करेंगे।"
                )
            elif severity == "mild friction":
                interp_en = (
                    f"{a_name} (H{ha}, {state_a}) and {b_name} (H{hb}, {state_b}) are LK "
                    f"enemies on the {axis_label} axis, but at least one is strong — the "
                    f"strong side largely contains the damage, expect mild friction only."
                )
                interp_hi = (
                    f"{a_name} (भाव {ha}, {state_a}) और {b_name} (भाव {hb}, {state_b}) "
                    f"{axis_label} अक्ष पर शत्रु हैं, पर एक बली है — बली पक्ष क्षति को "
                    f"सीमित करता है, केवल हल्का घर्षण अपेक्षित।"
                )
            elif severity == "moderate friction":
                interp_en = (
                    f"{a_name} (H{ha}) and {b_name} (H{hb}) are LK enemies on the {axis_label} "
                    f"axis, both in neutral dignity — workable friction, not destructive."
                )
                interp_hi = (
                    f"{a_name} (भाव {ha}) और {b_name} (भाव {hb}) {axis_label} अक्ष पर "
                    f"शत्रु हैं, दोनों तटस्थ — प्रबंधनीय घर्षण, विनाशकारी नहीं।"
                )
            else:  # philosophical conflict (not LK enemies)
                interp_en = (
                    f"{a_name} (H{ha}) and {b_name} (H{hb}) share the {axis_label} axis "
                    f"but are not LK enemies — a philosophical conflict of themes, not "
                    f"a harmful clash. The axis is workable."
                )
                interp_hi = (
                    f"{a_name} (भाव {ha}) और {b_name} (भाव {hb}) {axis_label} अक्ष पर हैं "
                    f"पर शत्रु नहीं — विषयों का दार्शनिक मतभेद, हानिकारक टकराव नहीं। "
                    f"अक्ष टिकाऊ है।"
                )

            collisions.append({
                "planet_a": a_name,
                "planet_a_house": ha,
                "planet_b": b_name,
                "planet_b_house": hb,
                # Backwards-compatible aliases for the frontend UI
                # (which read `attacker` / `receiver`). Takkar is mutual,
                # so either side can be called attacker; we pick the
                # lower-house planet for stability.
                "attacker": a_name if ha < hb else b_name,
                "attacker_house": low,
                "receiver": b_name if ha < hb else a_name,
                "receiver_house": high,
                "axis": axis_label,
                "are_enemies": are_enemies,
                "severity": severity,
                "state_a": state_a,
                "state_b": state_b,
                "interpretation_en": interp_en,
                "interpretation_hi": interp_hi,
                "source": "LK_CANONICAL",
            })
            attack_count[a_name] = attack_count.get(a_name, 0) + 1
            attack_count[b_name] = attack_count.get(b_name, 0) + 1

    # Severity counts under the new dignity-aware ladder
    destructive_count = sum(1 for c in collisions if c["severity"] == "destructive")
    moderate_count    = sum(1 for c in collisions if c["severity"] == "moderate friction")
    mild_count        = sum(1 for c in collisions if c["severity"] == "mild friction")
    philosophical_count = sum(1 for c in collisions if c["severity"] == "philosophical conflict")

    # ── WEIGHTED VULNERABILITY SCORE (Codex R2-P4) ────────────────
    # Pure takkar count under-ranks Moon H8 Debilitated because Moon
    # has no axis partner — yet LK places H8 Moon as the single most
    # vulnerable position. Codex weighting:
    #   base = # takkar attacks
    #   dusthana house (H6/H8/H12)   +2
    #   debilitated dignity           +2
    #   H8 specifically              +1   (H8 is the ultimate dusthana)
    #
    # Tie-breaker order (per LK severity intuition):
    #   1. higher weighted score
    #   2. planet in H8 > any other dusthana > non-dusthana
    #   3. debilitated > non-debilitated
    #   4. alphabetical (deterministic)
    DUSTHANA = {6, 8, 12}
    vulnerability: Dict[str, Dict[str, Any]] = {}
    sign_by_planet = {p["planet"]: p.get("sign", "") for p in planet_positions}
    for p in all_planets:
        pname = p["planet"]
        phouse = p.get("house")
        sign = sign_by_planet.get(pname, "")
        dignity = _get_dignity_label(pname, sign) if sign else "Neutral"
        is_debilitated = dignity == "Debilitated"
        base = attack_count.get(pname, 0)
        dust_bonus = 2 if phouse in DUSTHANA else 0
        debil_bonus = 2 if is_debilitated else 0
        h8_bonus = 1 if phouse == 8 else 0
        score = base + dust_bonus + debil_bonus + h8_bonus

        # Classify WHERE the vulnerability comes from (Codex R3 fix).
        has_internal = dust_bonus + debil_bonus + h8_bonus > 0
        has_external = base > 0
        if has_internal and has_external:
            reason = "mixed"
        elif has_internal:
            reason = "internal"
        elif has_external:
            reason = "external"
        else:
            reason = "none"

        # Build human-readable explanation of WHY this planet is vulnerable.
        intrinsic_bits = []
        if is_debilitated:
            intrinsic_bits.append(f"debilitated in H{phouse}")
        elif phouse == 8:
            intrinsic_bits.append("placed in H8 (ultimate dusthana)")
        elif phouse in DUSTHANA:
            intrinsic_bits.append(f"placed in dusthana H{phouse}")
        external_bit = (
            f"attacked by {base} axis-enemy planet{'s' if base != 1 else ''}"
            if base > 0 else ""
        )

        if reason == "internal":
            explanation = (
                f"Internal — weakness is intrinsic ("
                f"{', '.join(intrinsic_bits)}), not from external enemy attack."
            )
        elif reason == "external":
            explanation = (
                f"External — {external_bit} across the opposite axis; "
                f"the planet itself is in a workable sign/house."
            )
        elif reason == "mixed":
            explanation = (
                f"Both — intrinsic weakness ({', '.join(intrinsic_bits)}) "
                f"AMPLIFIED by {external_bit}."
            )
        else:
            explanation = "None — no vulnerability factors detected."

        vulnerability[pname] = {
            "takkar_attacks": base,
            "in_dusthana": phouse in DUSTHANA,
            "in_h8": phouse == 8,
            "debilitated": is_debilitated,
            "score": score,
            "breakdown": (
                f"base({base}) + dusthana({dust_bonus}) + "
                f"debil({debil_bonus}) + h8({h8_bonus}) = {score}"
            ),
            "vulnerability_reason": reason,       # internal | external | mixed | none
            "vulnerability_explanation": explanation,
        }

    def _rank_key(item):
        name, v = item
        return (
            -v["score"],                # higher score first
            0 if v["in_h8"] else 1,     # H8 beats non-H8
            0 if v["in_dusthana"] else 1,
            0 if v["debilitated"] else 1,
            name,                       # alphabetical tie-break
        )
    ranked = sorted(vulnerability.items(), key=_rank_key)
    most_vulnerable = ranked[0][0] if ranked and ranked[0][1]["score"] > 0 else None

    # Keep backwards-compatible alias so the frontend doesn't break
    # but repoint it to the weighted winner (Codex: "Recalculate
    # 'most attacked' with this weight").
    most_attacked = most_vulnerable

    # Safe planets (zero takkar attacks received AND no vulnerability factors)
    safe_planets = [
        name for name, v in vulnerability.items() if v["score"] == 0
    ]

    from app.lalkitab_source_tags import source_of
    return {
        "collisions": collisions,
        "destructive_count": destructive_count,
        "moderate_count": moderate_count,
        "mild_count": mild_count,
        "philosophical_count": philosophical_count,
        "most_attacked_planet": most_attacked,       # legacy alias, now weighted
        "most_vulnerable_planet": most_vulnerable,   # new explicit name
        "vulnerability_scores": vulnerability,
        "vulnerability_ranking": [name for name, _ in ranked],
        "safe_planets": safe_planets,
        "source": source_of("calculate_takkar"),
    }


# ============================================================
# ENEMY PRESENCE DETECTION IN KEY HOUSES
# ============================================================

def calculate_enemy_presence(planet_positions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    For each planet, count how many of its enemies are present in:
    1. Its pakka ghar (permanent house)
    2. The house it currently sits in
    3. Houses that it aspects (LK aspects)

    Returns per-planet enemy siege analysis, most/least besieged planets.
    """
    # Build house → planets map
    house_map: Dict[int, List[str]] = {}
    planet_house: Dict[str, int] = {}
    for p in planet_positions:
        h = p.get("house")
        name = p.get("planet", "")
        if h and name:
            house_map.setdefault(h, []).append(name)
            planet_house[name] = h

    # Get LK aspects for aspected houses
    lk_aspects = calculate_lk_aspects(planet_positions)

    planets_result: Dict[str, Dict[str, Any]] = {}
    all_planet_names = [p["planet"] for p in planet_positions if p.get("planet") in PAKKA_GHAR]

    for planet_name in all_planet_names:
        enemies = LK_ENEMIES.get(planet_name, set())
        pakka = PAKKA_GHAR[planet_name]
        current_h = planet_house.get(planet_name)

        # 1. Enemies in pakka ghar
        enemies_in_pakka = [p for p in house_map.get(pakka, []) if p in enemies and p != planet_name]

        # 2. Enemies in current house
        enemies_in_current = [p for p in house_map.get(current_h, []) if p in enemies and p != planet_name] if current_h else []

        # 3. Enemies in aspected houses
        aspected_houses = set()
        for asp in lk_aspects.get(planet_name, []):
            aspected_houses.add(asp["house"])

        enemies_in_aspected = []
        for ah in aspected_houses:
            for p in house_map.get(ah, []):
                if p in enemies and p != planet_name and p not in enemies_in_aspected:
                    enemies_in_aspected.append(p)

        total_enemies = len(set(enemies_in_pakka + enemies_in_current + enemies_in_aspected))

        if total_enemies >= 3:
            siege_level = "severe"
        elif total_enemies == 2:
            siege_level = "moderate"
        elif total_enemies == 1:
            siege_level = "mild"
        else:
            siege_level = "none"

        if total_enemies > 0:
            all_enemy_names = sorted(set(enemies_in_pakka + enemies_in_current + enemies_in_aspected))
            interp_en = (
                f"{planet_name} faces {total_enemies} enem{'y' if total_enemies == 1 else 'ies'} "
                f"({', '.join(all_enemy_names)}) across its key houses. "
                f"Siege level: {siege_level}."
            )
            interp_hi = (
                f"{planet_name} के प्रमुख भावों में {total_enemies} दुश्मन "
                f"({', '.join(all_enemy_names)}) मौजूद हैं। "
                f"घेराबंदी स्तर: {'गंभीर' if siege_level == 'severe' else 'मध्यम' if siege_level == 'moderate' else 'हल्का'}।"
            )
        else:
            interp_en = f"{planet_name} has no enemies in its key houses. It operates freely."
            interp_hi = f"{planet_name} के प्रमुख भावों में कोई दुश्मन नहीं। यह स्वतंत्र रूप से कार्य करता है।"

        planets_result[planet_name] = {
            "total_enemies": total_enemies,
            "enemies_in_pakka_ghar": enemies_in_pakka,
            "enemies_in_current_house": enemies_in_current,
            "enemies_in_aspected_houses": enemies_in_aspected,
            "enemy_siege_level": siege_level,
            "interpretation_en": interp_en,
            "interpretation_hi": interp_hi,
        }

    # Determine most/least besieged
    if planets_result:
        most_besieged = max(planets_result, key=lambda k: planets_result[k]["total_enemies"])
        least_besieged = min(planets_result, key=lambda k: planets_result[k]["total_enemies"])
    else:
        most_besieged = None
        least_besieged = None

    return {
        "planets": planets_result,
        "most_besieged": most_besieged,
        "least_besieged": least_besieged,
    }


def calculate_karmic_debts_with_hora(
    planet_positions: List[Dict[str, Any]],
    birth_datetime=None,
    sunrise_time=None
) -> Dict[str, Any]:
    """
    Calculate karmic debts including Hora-based debt analysis.
    
    Combines standard planetary-position based debts with Hora-based calculations.
    
    Args:
        planet_positions: List of planet position dicts
        birth_datetime: Optional datetime for Hora calculation
        sunrise_time: Optional sunrise time
        
    Returns:
        Dict with standard_debts, hora_debt, combined_analysis
    """
    # Get standard planetary-based debts
    standard_debts = calculate_karmic_debts(planet_positions)
    
    result = {
        "standard_debts": standard_debts,
        "hora_analysis": None,
        "final_debts": standard_debts.copy() if standard_debts else [],
        "conflicts_resolved": [],
        "hora_influence": {}
    }
    
    if birth_datetime is None:
        result["hora_analysis"] = {
            "error": {
                "en": "Birth datetime not provided. Hora-based debt calculation skipped.",
                "hi": "जन्म दिनांक/समय प्रदान नहीं किया गया। होरा-आधारित ऋण गणना छोड़ दी गई।"
            }
        }
        return result
    
    # Calculate Hora lord and associated debt
    hora_info = calculate_hora_lord(birth_datetime, sunrise_time)
    result["hora_analysis"] = hora_info

    # Honest skip: if Hora was not computed (no real sunrise), do not
    # manufacture a debt entry. Surface the skip reason to callers.
    if hora_info.get("_skipped"):
        result["hora_influence"] = {
            "added_new_debt": False,
            "reason": "Hora debt skipped — real sunrise not available",
        }
        return result

    # Determine effective debt based on Hora
    base_debt_info = hora_info.get("base_debt", {})
    effective_debt = base_debt_info.get("debt")
    effective_debt_hi = base_debt_info.get("debt_hi")
    
    # Check for conflict modification
    conflict = hora_info.get("conflict_modification")
    if conflict:
        # Conflict modification applies - override base debt
        if not conflict.get("enhancement", False):
            effective_debt = conflict.get("modified_debt")
            effective_debt_hi = conflict.get("modified_debt_hi")
            result["conflicts_resolved"].append({
                "type": "modification",
                "trigger": conflict.get("trigger"),
                "from": base_debt_info.get("debt"),
                "to": effective_debt,
                "reason": conflict.get("reason", {})
            })
        else:
            # Enhancement rather than full modification
            result["conflicts_resolved"].append({
                "type": "enhancement",
                "trigger": conflict.get("trigger"),
                "effect": conflict.get("effect", {})
            })
    
    # Add Hora-based debt if not already present in standard debts
    hora_debt_entry = {
        "name": {"hi": effective_debt_hi, "en": effective_debt},
        "type": {"hi": effective_debt_hi, "en": effective_debt},
        "source": {
            "en": f"Planetary Hour (Hora) calculation - {hora_info['hora_lord']} Hora on {hora_info['weekday_name']}",
            "hi": f"ग्रहीय घंटा (होरा) गणना - {hora_info['weekday_name']} को {hora_info['hora_lord']} होरा"
        },
        "hora_lord": hora_info["hora_lord"],
        "day_lord": hora_info["day_lord"],
        "reason": {
            "en": f"Hora lord {hora_info['hora_lord']} at birth indicates this karmic debt pattern",
            "hi": f"जन्म के समय होरा स्वामी {hora_info['hora_lord']} यह कर्मिक ऋण पैटर्न इंगित करता है"
        },
        "manifestation": base_debt_info.get("description", {}) if not conflict else conflict.get("manifestation", base_debt_info.get("description", {})),
        "is_hora_based": True,
        "is_modified": conflict is not None and not conflict.get("enhancement", False)
    }
    
    # Check if this debt type is already identified
    debt_types = [d.get("name", {}).get("en", "") for d in standard_debts]
    
    # Extract base debt name without "Rin"
    hora_base_name = effective_debt.replace(" Rin", "").replace(" / Shadow Debt", "").replace(" / Divine Debt", "") if effective_debt else ""
    
    already_present = any(hora_base_name in dt or dt in hora_base_name for dt in debt_types if dt)
    
    if not already_present and effective_debt:
        result["final_debts"].append(hora_debt_entry)
        result["hora_influence"] = {
            "added_new_debt": True,
            "debt_name": effective_debt
        }
    else:
        result["hora_influence"] = {
            "added_new_debt": False,
            "reason": "Debt already identified through planetary positions" if already_present else "No effective debt determined",
            "hora_debt_would_be": effective_debt
        }
    
    # Add boundary warning if applicable
    if hora_info.get("boundary_warning"):
        result["time_sensitivity_warning"] = hora_info["boundary_warning"]
    
    return result




# ============================================================
# DHOKA (DECEPTION) — 10th house deceives 4th
# ============================================================

_MALEFIC_SET = {"Saturn", "Mars", "Rahu", "Ketu", "Sun"}
_BENEFIC_SET = {"Jupiter", "Venus", "Moon", "Mercury"}

_DHOKA_MATRIX: List[Dict] = [
    # (source_house, target_house, name, description_en, description_hi)
    (10, 4,  "Career-Home Dhoka",
     "10th house Saturn/Rahu casts deception over 4th house domestic peace. Career ambition erodes family stability.",
     "10वें भाव का ग्रह 4थे भाव में भ्रम फैलाता है — करियर की महत्वाकांक्षा पारिवारिक शांति को नष्ट करती है।"),
    (7,  1,  "Partnership-Self Dhoka",
     "7th house malefic deceives the 1st house self — you may give more than you receive in partnerships.",
     "7वें भाव का ग्रह लग्न को धोखा देता है — साझेदारी में आप देते अधिक हैं, पाते कम हैं।"),
    (12, 6,  "Loss-Conflict Dhoka",
     "12th house loss creates illusion of victory in 6th house conflicts. Secret enemies use apparent defeats.",
     "12वें भाव की हानि 6ठे भाव के संघर्षों में विजय का भ्रम देती है।"),
    (5,  9,  "Intelligence-Fortune Dhoka",
     "5th house cleverness can deceive 9th house fortune — overthinking blocks blessings.",
     "5वें भाव की चालाकी 9वें भाव के भाग्य को धोखा देती है — अति सोच आशीर्वाद रोकती है।"),
    (8,  2,  "Transformation-Wealth Dhoka",
     "8th house sudden changes create deception in 2nd house accumulated wealth. Inherited resources may vanish.",
     "8वें भाव के अचानक परिवर्तन 2रे भाव के संचित धन को छलते हैं।"),
]

def calculate_dhoka(planet_positions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Detect Dhoka (Deception) patterns — when malefic planets in source houses
    cast their shadow over target houses, creating false signals and instability.
    """
    p_map: Dict[str, int] = {}
    for p in planet_positions:
        name = p.get("planet")
        house = p.get("house")
        if name and isinstance(house, int):
            p_map[name] = house

    # Build house→planet map
    house_to_planets: Dict[int, List[str]] = {}
    for planet, house in p_map.items():
        house_to_planets.setdefault(house, []).append(planet)

    results = []
    for src_h, tgt_h, dhoka_name, desc_en, desc_hi in _DHOKA_MATRIX:
        src_planets = house_to_planets.get(src_h, [])
        tgt_planets = house_to_planets.get(tgt_h, [])
        malefics_in_src = [p for p in src_planets if p in _MALEFIC_SET]
        if not malefics_in_src:
            continue
        tgt_empty = len(tgt_planets) == 0
        tgt_vulnerable = tgt_empty or any(p in _MALEFIC_SET for p in tgt_planets)
        severity = "high" if tgt_vulnerable else "moderate"
        results.append({
            "dhoka_name": dhoka_name,
            "source_house": src_h,
            "target_house": tgt_h,
            "malefics_causing": malefics_in_src,
            "target_planets": tgt_planets,
            "target_empty": tgt_empty,
            "severity": severity,
            "description": {"en": desc_en, "hi": desc_hi},
            "remedy": {
                "en": f"Strengthen {'4th' if tgt_h == 4 else str(tgt_h)+'th'} house by daily moon/milk water ritual. Avoid decisions driven by {', '.join(malefics_in_src)} themes.",
                "hi": f"{tgt_h}वें भाव को मजबूत करें — जल और दूध का दान, {', '.join(malefics_in_src)} से संबंधित निर्णय टालें।"
            }
        })
    return results


# ============================================================
# ACHANAK CHOT (SUDDEN STRIKE)
# ============================================================

_STRIKE_RULES: List[Dict] = [
    # 6th house strikes 2nd (service/conflict destroys accumulated wealth)
    {"striker_house": 6, "victim_house": 2,
     "name": "Service-Wealth Strike",
     "en": "6th house enemies/service unexpectedly drains 2nd house savings and family resources. Legal disputes, medical bills.",
     "hi": "6ठे भाव के शत्रु 2रे भाव के धन को अचानक नष्ट करते हैं — कानूनी विवाद, चिकित्सा खर्च।"},
    # 3rd house strikes 9th
    {"striker_house": 3, "victim_house": 9,
     "name": "Effort-Fortune Strike",
     "en": "3rd house impulsive actions or sibling conflicts suddenly undermine 9th house fortune and long-term blessings.",
     "hi": "3रे भाव की आवेगशील कार्रवाइयां 9वें भाव के भाग्य को अचानक नुकसान पहुंचाती हैं।"},
    # 11th house strikes 5th
    {"striker_house": 11, "victim_house": 5,
     "name": "Network-Creativity Strike",
     "en": "11th house social circle or false friends suddenly disrupts 5th house children/creativity/speculation.",
     "hi": "11वें भाव के मित्र या नेटवर्क 5वें भाव की रचनात्मकता/संतान को अचानक झटका देते हैं।"},
    # 12th house strikes 1st
    {"striker_house": 12, "victim_house": 1,
     "name": "Loss-Self Strike",
     "en": "Hidden 12th house enemies or foreign elements suddenly attack personal health and identity.",
     "hi": "12वें भाव के छिपे दुश्मन व्यक्तित्व और स्वास्थ्य पर अचानक प्रहार करते हैं।"},
]

def calculate_achanak_chot(planet_positions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Calculate Achanak Chot (Sudden Strike) — malefics in striker houses
    targeting victim houses, creating abrupt life disruptions.
    """
    house_to_planets: Dict[int, List[str]] = {}
    for p in planet_positions:
        name = p.get("planet")
        house = p.get("house")
        if name and isinstance(house, int):
            house_to_planets.setdefault(house, []).append(name)

    results = []
    for rule in _STRIKE_RULES:
        striker_h = rule["striker_house"]
        victim_h = rule["victim_house"]
        malefics_in_striker = [
            p for p in house_to_planets.get(striker_h, []) if p in _MALEFIC_SET
        ]
        if not malefics_in_striker:
            continue
        victim_planets = house_to_planets.get(victim_h, [])
        is_critical = any(p in _MALEFIC_SET for p in victim_planets) or len(victim_planets) == 0
        results.append({
            "strike_name": rule["name"],
            "striker_house": striker_h,
            "victim_house": victim_h,
            "malefics": malefics_in_striker,
            "victim_planets": victim_planets,
            "is_critical": is_critical,
            "description": {"en": rule["en"], "hi": rule["hi"]},
            "warning": {
                "en": f"Watch for sudden disruptions when {', '.join(malefics_in_striker)} transits activate house {striker_h}.",
                "hi": f"सावधान रहें जब {', '.join(malefics_in_striker)} भाव {striker_h} को सक्रिय करें।"
            }
        })
    return results


# ============================================================
# ACTIVE vs PASSIVE RIN (Karmic Debt Activation)
# ============================================================

# Map each rin type to its "home house" — if a malefic occupies this house, rin is active
_RIN_ACTIVATION_HOUSE: Dict[str, int] = {
    "Pitru Rin":    9,   # Father/ancestor house
    "Matru Rin":    4,   # Mother house
    "Sva Rin":      1,   # Self house
    "Bhratri Rin":  3,   # Siblings house
    "Bhagini Rin":  3,   # Sister house
    "Stri Rin":     7,   # Spouse house (legacy key)
    "Stree Rin":    7,   # Spouse house
    "Guru Rin":     9,   # Teacher/fortune house
    "Dev Rin":      5,   # Piety / past merit house
    "Deva Rin":     5,   # Alternate spelling
    "Rishi Rin":    12,  # Liberation / spirituality house
    "Nag Rin":      8,   # Hidden/serpent house
    "Nara Rin":     7,   # Humanity/service/partnership house
    "Prakriti Rin": 10,  # Work/public-service house
}

# Per-Rin activation triggers (Codex R3 fix): when the debt is
# expected to SURFACE in life, and what life-area it dominates.
# Used by enrich_debts_active_passive() to emit:
#   activates_during: Saturn saala grah (age 41) OR H7 Saturn transit...
#   life_area:       Career delays, chronic partnership obstacles...
_RIN_ACTIVATION_TRIGGERS: Dict[str, Dict[str, str]] = {
    "Pitru Rin": {
        "planet": "Rahu",
        "activates_during_en": (
            "Rahu/Ketu saala grah or dasha, during pitra-paksha (September), "
            "or when a major father-figure/authority event occurs."
        ),
        "activates_during_hi": (
            "राहु/केतु की साला ग्रह या दशा, पितृ-पक्ष (सितंबर), "
            "अथवा पिता-तुल्य/अधिकारी घटना के समय।"
        ),
        "life_area_en": (
            "Paternal line issues, authority blocks, 9th-house fortune "
            "stagnation, ancestral-property disputes."
        ),
        "life_area_hi": (
            "पैतृक पक्ष की समस्याएं, अधिकार में बाधा, 9वें भाव का "
            "भाग्य रुकावट, पैतृक-संपत्ति विवाद।"
        ),
    },
    "Matru Rin": {
        "planet": "Moon",
        "activates_during_en": (
            "Moon saala grah, Monday pradoshas, or whenever mother/home-life "
            "crises surface."
        ),
        "activates_during_hi": (
            "चंद्र साला ग्रह, सोमवार प्रदोष, अथवा माता/घर से जुड़े संकट।"
        ),
        "life_area_en": (
            "Mother's health, emotional security, home-property stability, "
            "sleep disturbances."
        ),
        "life_area_hi": (
            "माता का स्वास्थ्य, भावनात्मक सुरक्षा, घर-संपत्ति स्थिरता, "
            "नींद में विघ्न।"
        ),
    },
    "Sva Rin": {
        "planet": "Rahu",
        "activates_during_en": (
            "Rahu saala grah, or during periods of ego-conflict / legal "
            "trouble / 5th-house creative ventures."
        ),
        "activates_during_hi": (
            "राहु साला ग्रह, अथवा अहंकार-विवाद, कानूनी समस्या, 5वें भाव के "
            "रचनात्मक उपक्रमों के समय।"
        ),
        "life_area_en": (
            "Self-worth, children's welfare, legal penalties despite innocence, "
            "heart issues, atheistic drift."
        ),
        "life_area_hi": (
            "आत्म-सम्मान, संतान कल्याण, निर्दोष होकर भी कानूनी दंड, "
            "हृदय रोग, नास्तिकता की ओर झुकाव।"
        ),
    },
    "Bhratri Rin": {
        "planet": "Mars",
        "activates_during_en": (
            "Mars saala grah, during disputes with siblings/friends, or on "
            "property-partition / blood-injury events."
        ),
        "activates_during_hi": (
            "मंगल साला ग्रह, भाई/मित्र विवाद, या संपत्ति-बंटवारा/रक्त-चोट की घटनाओं पर।"
        ),
        "life_area_en": (
            "Sibling relationships, friendship betrayal, property disputes, "
            "courage and initiative."
        ),
        "life_area_hi": (
            "भाई-बहन के रिश्ते, मित्रता का विश्वासघात, संपत्ति विवाद, "
            "साहस और पहल।"
        ),
    },
    "Bhagini Rin": {
        "planet": "Mercury",
        "activates_during_en": (
            "Mercury saala grah or around the birth of a daughter/female "
            "relative; 3rd/6th house transits."
        ),
        "activates_during_hi": (
            "बुध साला ग्रह, कन्या/महिला संबंधी के जन्म पर, 3रे/6ठे भाव के गोचर में।"
        ),
        "life_area_en": (
            "Welfare of female children and sisters, exploitation patterns, "
            "inauspicious events at female births."
        ),
        "life_area_hi": (
            "कन्याओं/बहनों का कल्याण, शोषण पैटर्न, स्त्री-जन्म पर अशुभ घटनाएं।"
        ),
    },
    "Deva Rin": {
        "planet": "Jupiter",
        "activates_during_en": (
            "Jupiter saala grah, guru-disrespect events, or periods of "
            "temple / spiritual-teacher conflict."
        ),
        "activates_during_hi": (
            "गुरु साला ग्रह, गुरु-अनादर की घटनाएं, या मंदिर/आध्यात्मिक-गुरु विवाद के समय।"
        ),
        "life_area_en": (
            "Spiritual progress, guru connection, respect for teachers and "
            "priests, sacred-place/tree maintenance."
        ),
        "life_area_hi": (
            "आध्यात्मिक प्रगति, गुरु से संबंध, शिक्षकों/पुजारियों का सम्मान, "
            "पवित्र स्थल/वृक्ष की देखभाल।"
        ),
    },
    "Stree Rin": {
        "planet": "Venus",
        "activates_during_en": (
            "Venus saala grah, marriage-related transits, or when H2/H7 "
            "houses are activated by Sun/Moon/Rahu."
        ),
        "activates_during_hi": (
            "शुक्र साला ग्रह, विवाह-संबंधी गोचर, अथवा 2रे/7वें भाव पर "
            "सूर्य/चंद्र/राहु की सक्रियता।"
        ),
        "life_area_en": (
            "Marriage stability, relationship harmony, treatment of women "
            "in family, female-exploitation patterns."
        ),
        "life_area_hi": (
            "विवाह-स्थिरता, संबंधों में सामंजस्य, परिवार में स्त्रियों का "
            "व्यवहार, स्त्री-शोषण पैटर्न।"
        ),
    },
    "Nara Rin": {
        "planet": "Saturn",
        "activates_during_en": (
            "Saturn saala grah (any Saturn year) OR any Saturn transit of "
            "H1/H7/H10 OR when partnership/service/labour disputes arise."
        ),
        "activates_during_hi": (
            "शनि साला ग्रह (शनि का कोई भी वर्ष) अथवा शनि का 1/7/10 भाव में "
            "गोचर, या साझेदारी/सेवा/मजदूर विवाद के समय।"
        ),
        "life_area_en": (
            "Career delays, chronic obstacles in partnerships and service, "
            "generalised feeling of being cursed, humanitarian debt."
        ),
        "life_area_hi": (
            "करियर में देरी, साझेदारी और सेवा में पुरानी बाधाएं, "
            "सामान्य शापित होने की भावना, मानवता का ऋण।"
        ),
    },
    "Prakriti Rin": {
        "planet": "Mercury",
        "activates_during_en": (
            "Mercury saala grah, natural-disaster-prone periods, Rahu/Ketu "
            "ingress, or when environmental/animal-welfare events trigger."
        ),
        "activates_during_hi": (
            "बुध साला ग्रह, प्राकृतिक आपदा की अवधि, राहु/केतु का प्रवेश, "
            "या पर्यावरण/पशु-कल्याण की घटनाओं पर।"
        ),
        "life_area_en": (
            "Environmental issues, natural-disaster vulnerability, treatment "
            "of animals, past-life ecological debts."
        ),
        "life_area_hi": (
            "पर्यावरणीय समस्याएं, प्राकृतिक आपदा की संवेदनशीलता, पशुओं का "
            "व्यवहार, पूर्व जन्म के पारिस्थितिकीय ऋण।"
        ),
    },
}

def enrich_debts_active_passive(
    debts: List[Dict[str, Any]],
    planet_positions: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Takes raw karmic debts and adds 'activation_status': 'active' | 'passive' | 'latent'.
    Active = house related to debt has a malefic planet in the natal chart.
    Passive = debt exists but house is occupied by benefic or empty.
    Latent = debt not triggered yet.
    """
    house_to_planets: Dict[int, List[str]] = {}
    for p in planet_positions:
        name = p.get("planet")
        house = p.get("house")
        if name and isinstance(house, int):
            house_to_planets.setdefault(house, []).append(name)

    enriched = []
    for debt in debts:
        debt_name_en = debt.get("name", {}).get("en", "")
        # Find the matching trigger key (supports variants like Stri / Stree / Dev / Deva).
        trigger_key = next(
            (k for k in _RIN_ACTIVATION_HOUSE
             if k in debt_name_en or debt_name_en in k),
            None
        )
        activation_house = _RIN_ACTIVATION_HOUSE.get(trigger_key) if trigger_key else None
        trigger_info = _RIN_ACTIVATION_TRIGGERS.get(trigger_key) if trigger_key else None

        # Resolve activation status ────────────────────────────────
        if activation_house is None:
            debt["activation_status"] = "latent"
            debt["activation_house"] = None
        else:
            house_planets = house_to_planets.get(activation_house, [])
            has_malefic = any(p in _MALEFIC_SET for p in house_planets)
            has_benefic = any(p in _BENEFIC_SET for p in house_planets)
            if has_malefic:
                status = "active"
                urgency_en = "URGENT — this debt is actively manifesting. Remedy immediately."
                urgency_hi = "तत्काल — यह ऋण सक्रिय रूप से प्रकट हो रहा है। तुरंत उपाय करें।"
            elif has_benefic or house_planets:
                status = "passive"
                urgency_en = "Latent — this debt exists but is not acutely activated. Preventive remedy advised."
                urgency_hi = "सुप्त — यह ऋण मौजूद है लेकिन तीव्र नहीं। निवारक उपाय करें।"
            else:
                status = "passive"
                urgency_en = "House empty — debt is dormant. May activate during relevant dashas/transits."
                urgency_hi = "भाव खाली — ऋण सुप्त है। संबंधित दशा/गोचर में सक्रिय हो सकता है।"
            debt["activation_status"] = status
            debt["activation_house"] = activation_house
            debt["activation_urgency"] = {"en": urgency_en, "hi": urgency_hi}

        # ── Per-Rin activation trigger + life-area (Codex R3 fix) ──
        # Always populate these — even for "latent" Rins we describe
        # WHEN they would activate and WHICH life area they touch.
        if trigger_info:
            debt["activating_planet"] = trigger_info.get("planet")
            debt["activates_during"] = {
                "en": trigger_info.get("activates_during_en", ""),
                "hi": trigger_info.get("activates_during_hi", ""),
            }
            debt["life_area"] = {
                "en": trigger_info.get("life_area_en", ""),
                "hi": trigger_info.get("life_area_hi", ""),
            }
        else:
            debt["activating_planet"] = None
            debt["activates_during"] = {"en": "", "hi": ""}
            debt["life_area"] = {"en": "", "hi": ""}

        enriched.append(debt)
    return enriched
