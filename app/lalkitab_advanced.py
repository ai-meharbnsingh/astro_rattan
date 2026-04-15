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

    return debts

def identify_teva_type(planet_positions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Detects if the chart is an Andha Teva (Blind), Ratondha (Half-Blind), or Dharmi Teva (Religious).
    Reference: PDF 2.1.1, 2.1.2
    """
    p_map = {p["planet"]: p["house"] for p in planet_positions}
    
    # 1. Andha Teva (Blind Chart)
    # Trigger: Two or more enemy planets in 10th house
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

    # 2. Ratondha Teva (Half-Blind Chart)
    # Trigger: Sun in 4th and Saturn in 7th (Classical example)
    is_ratondha = (p_map.get("Sun") == 4 and p_map.get("Saturn") == 7)

    # 3. Dharmi Teva (Religious Chart)
    is_dharmi = False
    # Path A: Jupiter + Saturn mutual association (conjunction or 1/7 aspect)
    if p_map.get("Jupiter") == p_map.get("Saturn") and p_map.get("Jupiter") is not None:
        is_dharmi = True
    elif (p_map.get("Jupiter") == 1 and p_map.get("Saturn") == 7) or (p_map.get("Jupiter") == 7 and p_map.get("Saturn") == 1):
        is_dharmi = True
    elif (p_map.get("Jupiter") == 4 and p_map.get("Saturn") == 10) or (p_map.get("Jupiter") == 10 and p_map.get("Saturn") == 4):
        is_dharmi = True
    # Path B: Specific auspicious placements
    elif p_map.get("Jupiter") in {6, 9, 11} or p_map.get("Saturn") in {9, 11}:
        is_dharmi = True

    return {
        "is_andha": is_andha,
        "is_ratondha": is_ratondha,
        "is_dharmi": is_dharmi,
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
            }
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
        sunrise_time: Optional sunrise time (defaults to 6:00 AM)
        longitude: Optional longitude for precise sunrise calculation
        latitude: Optional latitude for precise sunrise calculation
        
    Returns:
        Dict with hora_lord, day_lord, hours_elapsed, conflict_info
    """
    from datetime import datetime, time
    
    # Get day of week and day lord
    weekday = birth_datetime.weekday()  # 0=Monday
    day_lord = DAY_LORDS[weekday]
    
    # Determine sunrise (simplified: 6:00 AM, or calculate if location provided)
    if sunrise_time is None:
        # Simplified: use 6:00 AM local time
        sunrise = datetime.combine(birth_datetime.date(), time(6, 0))
    else:
        sunrise = datetime.combine(birth_datetime.date(), sunrise_time)
    
    # Calculate hours elapsed since sunrise
    # Handle case where birth is before sunrise (previous day's cycle)
    if birth_datetime < sunrise:
        # Use previous day's cycle - find yesterday's sunrise
        from datetime import timedelta
        yesterday = birth_datetime - timedelta(days=1)
        sunrise = datetime.combine(yesterday.date(), time(6, 0))
    
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


