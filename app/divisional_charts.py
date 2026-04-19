"""
divisional_charts.py -- Vedic Divisional Chart Calculator
==========================================================
Calculates divisional (varga) charts used in Vedic astrology.
Supports all 16 standard divisional charts: D1 through D60.

Each divisional chart maps a planet's longitude in the Rasi (D1) chart
to a sign in the divisional chart based on specific mathematical divisions.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

# Sign names in order (0-indexed)
_SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

# Supported divisional chart types with display names
DIVISIONAL_CHARTS: Dict[int, str] = {
    1: "Rashi (D1)",
    2: "Hora (D2)",
    3: "Drekkana (D3)",
    4: "Chaturthamsha (D4)",
    7: "Saptamsha (D7)",
    9: "Navamsha (D9)",
    10: "Dashamsha (D10)",
    12: "Dwadashamsha (D12)",
    16: "Shodashamsha (D16)",
    20: "Vimshamsha (D20)",
    24: "Chaturvimshamsha (D24)",
    27: "Bhamsha (D27)",
    30: "Trimshamsha (D30)",
    40: "Khavedamsha (D40)",
    45: "Akshavedamsha (D45)",
    60: "Shashtiamsha (D60)",
    108: "Ashtottaramsha (D108)",
}

# ============================================================
# D60 SHASHTIAMSA SANSKRIT NAMES & NATURE
# Reference: PDF 1.1.3 (Ancient Vedic Logic)
# ============================================================
D60_NAMES = [
    {"name": "Ghora", "nature": "Malefic", "hi": "घोर", "desc": "Terrible, intense suffering"},
    {"name": "Rakshasa", "nature": "Malefic", "hi": "राक्षस", "desc": "Demonic, cruel tendencies"},
    {"name": "Deva", "nature": "Benefic", "hi": "देव", "desc": "Divine, virtuous, enlightened"},
    {"name": "Kubera", "nature": "Benefic", "hi": "कुबेर", "desc": "Wealthy, lord of riches"},
    {"name": "Yaksha", "nature": "Mixed", "hi": "यक्ष", "desc": "Protector of wealth, mystical"},
    {"name": "Kinnara", "nature": "Benefic", "hi": "किन्नर", "desc": "Artistic, musical, harmonious"},
    {"name": "Bhrashta", "nature": "Malefic", "hi": "भ्रष्ट", "desc": "Fallen, corrupt, loss of status"},
    {"name": "Kulaghna", "nature": "Malefic", "hi": "कुलघ्न", "desc": "Destroyer of lineage"},
    {"name": "Garala", "nature": "Malefic", "hi": "गरल", "desc": "Poisonous, toxic environments"},
    {"name": "Vahni", "nature": "Malefic", "hi": "वह्नि", "desc": "Fire, burning, digestive issues"},
    {"name": "Maya", "nature": "Mixed", "hi": "माया", "desc": "Illusion, deceptive success"},
    {"name": "Purishaka", "nature": "Malefic", "hi": "पुरीषक", "desc": "Impure, difficult circumstances"},
    {"name": "Apampati", "nature": "Benefic", "hi": "अपाम्पति", "desc": "Lord of waters, calm, stable"},
    {"name": "Marutvan", "nature": "Benefic", "hi": "मरुत्वान्", "desc": "Lord of winds, influential"},
    {"name": "Kaala", "nature": "Malefic", "hi": "काल", "desc": "Time, end, restrictive"},
    {"name": "Sarpa", "nature": "Malefic", "hi": "सर्प", "desc": "Serpentine, hidden enemies"},
    {"name": "Amrita", "nature": "Benefic", "hi": "अमृत", "desc": "Nectar, immortality, great health"},
    {"name": "Indu", "nature": "Benefic", "hi": "इन्दु", "desc": "Moon-like, peaceful, nourishing"},
    {"name": "Mridu", "nature": "Benefic", "hi": "मृदु", "desc": "Soft, gentle, kind"},
    {"name": "Komala", "nature": "Benefic", "hi": "कोमल", "desc": "Delicate, refined, aesthetic"},
    {"name": "Heramba", "nature": "Benefic", "hi": "हेरम्ब", "desc": "Ganesha-like, removing obstacles"},
    {"name": "Brahma", "nature": "Benefic", "hi": "ब्रह्मा", "desc": "Creative, knowledge-oriented"},
    {"name": "Vishnu", "nature": "Benefic", "hi": "विष्णु", "desc": "Protective, expansive, lucky"},
    {"name": "Maheshwara", "nature": "Benefic", "hi": "महेश्वर", "desc": "Powerful, transformative, grand"},
    {"name": "Devadeva", "nature": "Benefic", "hi": "देवदेव", "desc": "Lord of lords, supreme status"},
    {"name": "Ardra", "nature": "Mixed", "hi": "आर्द्रा", "desc": "Moist, emotional, sensitive"},
    {"name": "Kalinasa", "nature": "Benefic", "hi": "कलिनाश", "desc": "Destroyer of strife"},
    {"name": "Kshiteeshwara", "nature": "Benefic", "hi": "क्षितीश्वर", "desc": "Ruler of earth, landed property"},
    {"name": "Kamalakara", "nature": "Benefic", "hi": "कमलाकर", "desc": "Lotus-like, purity, beauty"},
    {"name": "Gulika", "nature": "Malefic", "hi": "गुलिका", "desc": "Saturn's son, karmic delays"},
    {"name": "Mrityu", "nature": "Malefic", "hi": "मृत्यु", "desc": "Death-like, end of cycles"},
    {"name": "Kaala", "nature": "Malefic", "hi": "काल", "desc": "Time, finite, ending"},
    {"name": "Davagni", "nature": "Malefic", "hi": "दवाग्नि", "desc": "Forest fire, sudden destruction"},
    {"name": "Ghora", "nature": "Malefic", "hi": "घोर", "desc": "Intense, terrible"},
    {"name": "Adhama", "nature": "Malefic", "hi": "अधम", "desc": "Lowly, degraded results"},
    {"name": "Kantaka", "nature": "Malefic", "hi": "कंटक", "desc": "Thorn, painful obstacles"},
    {"name": "Sudha", "nature": "Benefic", "hi": "सुधा", "desc": "Nectar, pure, satisfying"},
    {"name": "Amrita", "nature": "Benefic", "hi": "अमृत", "desc": "Immortality, nectar"},
    {"name": "Poornachandra", "nature": "Benefic", "hi": "पूर्णचन्द्र", "desc": "Full moon, abundance, fame"},
    {"name": "Vishadagdha", "nature": "Malefic", "hi": "विषदिग्ध", "desc": "Consumed by poison"},
    {"name": "Kulanasa", "nature": "Malefic", "hi": "कुलनाश", "desc": "Linage destroyer"},
    {"name": "Vamshakshaya", "nature": "Malefic", "hi": "वंशक्षय", "desc": "Family decay"},
    {"name": "Utpata", "nature": "Malefic", "hi": "उत्पात", "desc": "Calamity, sudden upheaval"},
    {"name": "Kaala", "nature": "Malefic", "hi": "काल", "desc": "Time constraint"},
    {"name": "Saumya", "nature": "Benefic", "hi": "सौम्य", "desc": "Gentle, benefic results"},
    {"name": "Komala", "nature": "Benefic", "hi": "कोमल", "desc": "Soft, pleasant"},
    {"name": "Sheetala", "nature": "Benefic", "hi": "शीतल", "desc": "Cool, soothing"},
    {"name": "Karaladamshstra", "nature": "Malefic", "hi": "करालदंष्ट्र", "desc": "Fierce teeth, aggressive"},
    {"name": "Chandramukhi", "nature": "Benefic", "hi": "चन्द्रमुखी", "desc": "Moon-faced, attractive"},
    {"name": "Praveena", "nature": "Benefic", "hi": "प्रवीण", "desc": "Skilled, expert"},
    {"name": "Kalapavaka", "nature": "Malefic", "hi": "कालपावक", "desc": "Fire of time"},
    {"name": "Dandayudha", "nature": "Malefic", "hi": "दंडायुध", "desc": "Staff-bearing, punishment"},
    {"name": "Nirmala", "nature": "Benefic", "hi": "निर्मल", "desc": "Pure, stainless"},
    {"name": "Saumya", "nature": "Benefic", "hi": "सौम्य", "desc": "Gentle"},
    {"name": "Kshura", "nature": "Malefic", "hi": "क्षुर", "desc": "Razor-sharp, cutting"},
    {"name": "Atisheetala", "nature": "Benefic", "hi": "अतिशीतल", "desc": "Very cool, highly soothing"},
    {"name": "Amrita", "nature": "Benefic", "hi": "अमृत", "desc": "Nectar"},
    {"name": "Payodhi", "nature": "Benefic", "hi": "पयोधि", "desc": "Ocean, depth, vast wealth"},
    {"name": "Bhramana", "nature": "Mixed", "hi": "भ्रमण", "desc": "Wandering, travel"},
    {"name": "Chandrarekha", "nature": "Benefic", "hi": "चन्द्ररेखा", "desc": "Moon-streak, fame, soft aura"},
]

def calculate_d60_analysis(
    planet_longitudes: Dict[str, float],
    birth_time_uncertainty_seconds: Optional[float] = None
) -> Dict[str, Any]:
    """
    Identifies the D60 Shashtiamsa division for each planet and its meaning.
    Includes comprehensive past-life karma analysis and birth time sensitivity warnings.
    
    Reference: PDF 1.1.3 - D60 Shashtiamsa for Past-Life Karma
    
    Args:
        planet_longitudes: Dict of planet names to sidereal longitudes
        birth_time_uncertainty_seconds: Optional uncertainty in birth time (for warnings)
    
    Returns:
        Dict with planetary_analysis, karmic_summary, birth_time_assessment, and recommendations
    """
    # ============================================================
    # 1. PER-PLANET D60 ANALYSIS
    # ============================================================
    planetary_analysis = {}
    benefic_count = 0
    malefic_count = 0
    mixed_count = 0
    
    # Track karmic themes by planet
    karmic_themes = {
        "punya": [],  # Meritorious karma carriers
        "papa": [],   # Sinful karma carriers
        "mixed": []   # Mixed karma carriers
    }
    
    for planet, lon in planet_longitudes.items():
        # D60 = 30 / 60 = 0.5 degrees per division
        # 1. Degrees within sign
        deg_in_sign = lon % 30.0
        # 2. Shashtiamsa unit (0-59)
        unit = int(deg_in_sign * 2)  # 0.5 deg = 1 unit, so 1 deg = 2 units
        
        # 3. Determine if sign is ODD or EVEN
        sign_idx = int(lon / 30.0) % 12
        is_odd = (sign_idx % 2 == 0)  # 0=Aries (odd), 1=Taurus (even)
        
        # 4. Map to D60 name
        # If ODD: 1 to 60 directly
        # If EVEN: Reverse (60 to 1)
        if is_odd:
            name_idx = unit
        else:
            name_idx = 59 - unit
        
        if 0 <= name_idx < 60:
            info = D60_NAMES[name_idx]
            
            # Count nature types
            if info["nature"] == "Benefic":
                benefic_count += 1
                karmic_themes["punya"].append(planet)
            elif info["nature"] == "Malefic":
                malefic_count += 1
                karmic_themes["papa"].append(planet)
            else:
                mixed_count += 1
                karmic_themes["mixed"].append(planet)
            
            # Planet-specific karmic interpretation
            past_life_interpretation = _get_planet_d60_interpretation(planet, info["name"], info["nature"])
            
            planetary_analysis[planet] = {
                "unit": unit + 1,
                "name": info["name"],
                "name_hi": info["hi"],
                "nature": info["nature"],
                "description": info["desc"],
                "past_life_theme": past_life_interpretation,
                "longitude": round(lon, 4),
                "degree_in_sign": round(deg_in_sign, 2)
            }
    
    # ============================================================
    # 2. KARMIC SUMMARY ANALYSIS
    # ============================================================
    total_planets = len(planetary_analysis)
    punya_score = (benefic_count / total_planets * 100) if total_planets > 0 else 0
    papa_score = (malefic_count / total_planets * 100) if total_planets > 0 else 0
    
    # Overall karmic nature assessment
    if punya_score >= 60:
        overall_nature = "Highly Benefic"
        overall_desc = "Strong accumulated merit from past lives. Protection and grace available."
        overall_desc_hi = "पिछले जन्मों से अर्जित पुण्य अधिक। सुरक्षा और कृपा उपलब्ध।"
    elif punya_score >= 40:
        overall_nature = "Mixed-Benefic"
        overall_desc = "Balanced karmic ledger with slight merit advantage."
        overall_desc_hi = "संतुलित कर्मिक खाता थोड़े पुण्य लाभ के साथ।"
    elif papa_score >= 60:
        overall_nature = "Highly Malefic"
        overall_desc = "Significant karmic burdens requiring remedial attention."
        overall_desc_hi = "उपाय ध्यान देने की आवश्यकता वाले महत्वपूर्ण कर्मिक बोझ।"
    elif papa_score >= 40:
        overall_nature = "Mixed-Malefic"
        overall_desc = "Karmic challenges present but manageable with effort."
        overall_desc_hi = "कर्मिक चुनौतियां मौजूद हैं लेकिन प्रयास से प्रबंधनीय।"
    else:
        overall_nature = "Balanced"
        overall_desc = "Neutral karmic pattern - results depend on current actions."
        overall_desc_hi = "तटस्थ कर्मिक पैटर्न - परिणाम वर्तमान क्रियाओं पर निर्भर।"
    
    # Life purpose derivation
    life_purpose = _derive_life_purpose(karmic_themes, planetary_analysis)
    
    # Karmic debt identification from D60
    karmic_debts = _identify_d60_karmic_debts(planetary_analysis)
    
    # Remedy accessibility assessment
    remedy_accessibility = _assess_remedy_accessibility(punya_score, papa_score)
    
    karmic_summary = {
        "overall_nature": overall_nature,
        "overall_description": {"en": overall_desc, "hi": overall_desc_hi},
        "punya_score": round(punya_score, 1),
        "papa_score": round(papa_score, 1),
        "benefic_planets": karmic_themes["punya"],
        "malefic_planets": karmic_themes["papa"],
        "mixed_planets": karmic_themes["mixed"],
        "life_purpose": life_purpose,
        "karmic_debts": karmic_debts,
        "remedy_accessibility": remedy_accessibility
    }
    
    # ============================================================
    # 3. BIRTH TIME SENSITIVITY ASSESSMENT
    # ============================================================
    # D60 has 0.5 degree = 30 arc-minutes per division
    # Birth time error of ~30 seconds can shift planet to different D60
    # This is because Moon moves ~0.5 degrees in ~1 hour
    # So 30 seconds = ~0.004 degrees (approximate)
    
    sensitivity_warning = {
        "is_critical": True,
        "division_size_degrees": 0.5,
        "division_size_arcminutes": 30,
        "time_sensitivity": {
            "en": "D60 is extremely sensitive to birth time accuracy. Errors as small as 30-60 seconds can alter planetary placements entirely.",
            "hi": "डी60 जन्म समय की सटीकता के प्रति अत्यंत संवेदनशील है। 30-60 सेकंड की छोटी त्रुटि भी ग्रहों की स्थिति पूरी तरह बदल सकती है।"
        },
        "confidence_level": "unknown",
        "recommendations": []
    }
    
    # Assess based on provided uncertainty
    if birth_time_uncertainty_seconds is not None:
        if birth_time_uncertainty_seconds <= 10:
            sensitivity_warning["confidence_level"] = "high"
            sensitivity_warning["assessment"] = {
                "en": "Birth time precision is excellent for D60 analysis.",
                "hi": "डी60 विश्लेषण के लिए जन्म समय की सटीकता उत्कृष्ट है।"
            }
        elif birth_time_uncertainty_seconds <= 30:
            sensitivity_warning["confidence_level"] = "moderate"
            sensitivity_warning["assessment"] = {
                "en": "Birth time acceptable but borderline for D60 precision.",
                "hi": "जन्म समय स्वीकार्य लेकिन डी60 सटीकता के लिए सीमा पर है।"
            }
            sensitivity_warning["recommendations"].append({
                "en": "Consider birth time rectification through life event verification for maximum accuracy.",
                "hi": "अधिकतम सटीकता के लिए जीवन की घटनाओं के माध्यम से जन्म समय सुधार पर विचार करें।"
            })
        elif birth_time_uncertainty_seconds <= 120:
            sensitivity_warning["confidence_level"] = "low"
            sensitivity_warning["assessment"] = {
                "en": "Birth time uncertainty may affect D60 accuracy. Results should be interpreted with caution.",
                "hi": "जन्म समय की अनिश्चितता डी60 की सटीकता को प्रभावित कर सकती है। परिणामों की सावधानी से व्याख्या करनी चाहिए।"
            }
            sensitivity_warning["recommendations"].extend([
                {
                    "en": "Strongly recommend birth time rectification (BTR) before relying on D60 predictions.",
                    "hi": "डी60 भविष्यवाणियों पर भरोसा करने से पहले जन्म समय सुधार (बीटीआर) की दृढ़ता से अनुशंसा करें।"
                },
                {
                    "en": "Cross-verify D60 indications with D1 (Rashi) and D9 (Navamsa) charts.",
                    "hi": "डी60 संकेतों की डी1 (राशि) और डी9 (नवांश) कुंडली के साथ क्रॉस-सत्यापन करें।"
                }
            ])
        else:
            sensitivity_warning["confidence_level"] = "very_low"
            sensitivity_warning["assessment"] = {
                "en": "D60 analysis unreliable with current birth time accuracy. Rectification essential.",
                "hi": "वर्तमान जन्म समय सटीकता के साथ डी60 विश्लेषण अविश्वसनीय। सुधार आवश्यक।"
            }
            sensitivity_warning["recommendations"].extend([
                {
                    "en": "DO NOT rely on D60 predictions without proper birth time rectification.",
                    "hi": "उचित जन्म समय सुधार के बिना डी60 भविष्यवाणियों पर भरोसा न करें।"
                },
                {
                    "en": "Use D1, D9, and D10 charts as primary references instead.",
                    "hi": "इसके बजाय डी1, डी9 और डी10 चार्ट作为主要 संदर्भ के रूप में उपयोग करें।"
                },
                {
                    "en": "Consult a professional astrologer for birth time rectification using life events.",
                    "hi": "जीवन की घटनाओं का उपयोग करके जन्म समय सुधार के लिए एक पेशेवर ज्योतिषी से परामर्श करें।"
                }
            ])
    else:
        # No uncertainty provided - default warning
        sensitivity_warning["confidence_level"] = "unknown"
        sensitivity_warning["assessment"] = {
            "en": "Birth time uncertainty not provided. D60 results should be verified for accuracy.",
            "hi": "जन्म समय की अनिश्चितता प्रदान नहीं की गई। डी60 परिणामों की सटीकता के लिए सत्यापन किया जाना चाहिए।"
        }
        sensitivity_warning["recommendations"].append({
            "en": "Provide birth time accuracy (e.g., from birth certificate) for reliable D60 analysis.",
            "hi": "विश्वसनीय डी60 विश्लेषण के लिए जन्म समय की सटीकता प्रदान करें (जन्म प्रमाण पत्र से)।"
        })
    
    # Add general recommendations
    sensitivity_warning["recommendations"].append({
        "en": "Verify D60 placements with major life events (career peaks, marriage, health crises) for validation.",
        "hi": "सत्यापन के लिए प्रमुख जीवन घटनाओं (करियर चरम, विवाह, स्वास्थ्य संकट) के साथ डी60 स्थितियों की पुष्टि करें।"
    })
    
    # ============================================================
    # 4. FINAL ASSEMBLY
    # ============================================================
    return {
        "planetary_analysis": planetary_analysis,
        "karmic_summary": karmic_summary,
        "birth_time_assessment": sensitivity_warning,
        "metadata": {
            "chart_type": "Shashtiamsa (D60)",
            "chart_type_hi": "षष्ट्यांश (डी60)",
            "purpose": "Past-life karma and accumulated merit/sin analysis",
            "purpose_hi": "पिछले जन्म का कर्म और अर्जित पुण्य/पाप विश्लेषण",
            "authority": "Sage Parashara - highest authority for final judgment",
            "authority_hi": "ऋषि पराशर - अंतिम निर्णय के लिए सर्वोच्च प्राधिकरण"
        }
    }


def _get_planet_d60_interpretation(planet: str, d60_name: str, nature: str) -> Dict[str, Any]:
    """
    Generate planet-specific past-life interpretation based on D60 placement.
    Reference: PDF 1.1.3 - Planetary placements in D60 divisions
    """
    interpretations = {
        "Sun": {
            "benefic": {
                "theme": "Righteous authority and leadership in past lives",
                "theme_hi": "पिछले जन्मों में धार्मिक अधिकार और नेतृत्व",
                "manifestation": "Natural respect from authority figures, government favor"
            },
            "malefic": {
                "theme": "Misuse of authority or ego-driven leadership failures",
                "theme_hi": "अधिकार का दुरुपयोग या अहंकार-प्रेरित नेतृत्व विफलताएं",
                "manifestation": "Struggles with authority, father relationship challenges"
            },
            "mixed": {
                "theme": "Complex relationship with power and responsibility",
                "theme_hi": "शक्ति और जिम्मेदारी के साथ जटिल संबंध",
                "manifestation": "Alternating success and challenges in leadership"
            }
        },
        "Moon": {
            "benefic": {
                "theme": "Nurturing and emotional wisdom accumulated",
                "theme_hi": "पालन-पोषण और भावनात्मक बुद्धि का संचय",
                "manifestation": "Natural emotional security, strong maternal bonds"
            },
            "malefic": {
                "theme": "Emotional trauma or maternal relationship disruptions",
                "theme_hi": "भावनात्मक आघात या मातृ संबंध व्यवधान",
                "manifestation": "Emotional instability, mother-related challenges"
            },
            "mixed": {
                "theme": "Fluctuating emotional patterns across lifetimes",
                "theme_hi": "जीवनकालों में भावनात्मक पैटर्न में उतार-चढ़ाव",
                "manifestation": "Periods of emotional fulfillment and challenges"
            }
        },
        "Mars": {
            "benefic": {
                "theme": "Courageous protection of dharma and righteousness",
                "theme_hi": "धर्म और धार्मिकता की साहसी रक्षा",
                "manifestation": "Natural courage, protection from accidents, strong siblings"
            },
            "malefic": {
                "theme": "Violence, cruelty, or misused strength",
                "theme_hi": "हिंसा, क्रूरता, या दुरुपयोग की गई शक्ति",
                "manifestation": "Accident proneness, sibling conflicts, anger issues"
            },
            "mixed": {
                "theme": "Conflicts between aggression and protection",
                "theme_hi": "आक्रामकता और सुरक्षा के बीच संघर्ष",
                "manifestation": "Courage used sometimes constructively, sometimes destructively"
            }
        },
        "Mercury": {
            "benefic": {
                "theme": "Wisdom sharing and intellectual service",
                "theme_hi": "बुद्धि साझा करना और बौद्धिक सेवा",
                "manifestation": "Natural communication skills, learning ease"
            },
            "malefic": {
                "theme": "Deceptive speech or misused intellect",
                "theme_hi": "भ्रामक भाषण या दुरुपयोग की गई बुद्धि",
                "manifestation": "Communication challenges, nervous system issues"
            },
            "mixed": {
                "theme": "Intellect used for both truth and deception",
                "theme_hi": "बुद्धि का सच और छल दोनों के लिए उपयोग",
                "manifestation": "Skilled but sometimes manipulative communication"
            }
        },
        "Jupiter": {
            "benefic": {
                "theme": "Spiritual teaching and wisdom transmission",
                "theme_hi": "आध्यात्मिक शिक्षण और ज्ञान प्रसारण",
                "manifestation": "Natural wisdom, guru blessings, prosperity"
            },
            "malefic": {
                "theme": "False wisdom or betrayal of teacher's trust",
                "theme_hi": "झूठी बुद्धि या गुरु के विश्वास का विश्वासघात",
                "manifestation": "Challenges with teachers, wisdom misapplication"
            },
            "mixed": {
                "theme": "Alternating between true and false wisdom",
                "theme_hi": "सच्ची और झूठी बुद्धि के बीच बदलाव",
                "manifestation": "Periods of clarity and confusion in beliefs"
            }
        },
        "Venus": {
            "benefic": {
                "theme": "Artistic and relational harmony cultivated",
                "theme_hi": "कलात्मक और संबंधात्मक सामंजस्य का विकास",
                "manifestation": "Natural charm, relationship harmony, artistic talent"
            },
            "malefic": {
                "theme": "Sensual excess or relationship betrayals",
                "theme_hi": "वैभविक अत्यधिकता या संबंध विश्वासघात",
                "manifestation": "Relationship challenges, indulgence issues"
            },
            "mixed": {
                "theme": "Complex relationship patterns across lifetimes",
                "theme_hi": "जीवनकालों में जटिल संबंध पैटर्न",
                "manifestation": "Alternating fulfillment and disappointment in love"
            }
        },
        "Saturn": {
            "benefic": {
                "theme": "Disciplined service and karmic responsibility",
                "theme_hi": "अनुशासित सेवा और कर्मिक जिम्मेदारी",
                "manifestation": "Steady progress, respect for elders, stability"
            },
            "malefic": {
                "theme": "Neglected duties or abuse of power over vulnerable",
                "theme_hi": "उपेक्षित कर्तव्य या कमजोरों पर शक्ति का दुरुपयोग",
                "manifestation": "Delays, chronic challenges, authority conflicts"
            },
            "mixed": {
                "theme": "Inconsistent approach to responsibility",
                "theme_hi": "जिम्मेदारी के प्रति असंगत दृष्टिकोण",
                "manifestation": "Periods of discipline and negligence"
            }
        },
        "Rahu": {
            "benefic": {
                "theme": "Unconventional wisdom and breaking limitations",
                "theme_hi": "अपरंपरागत बुद्धि और सीमाओं को तोड़ना",
                "manifestation": "Innovation, foreign connections, unique insights"
            },
            "malefic": {
                "theme": "Obsessive desires and illusion (Maya)",
                "theme_hi": "व्यामोहजनक desires और माया",
                "manifestation": "Addictions, confusion, unrealistic ambitions"
            },
            "mixed": {
                "theme": "Ambition alternating between constructive and destructive",
                "theme_hi": "रचनात्मक और विनाशकारी के बीच बदलती महत्वाकांक्षा",
                "manifestation": "Unconventional paths with mixed results"
            }
        },
        "Ketu": {
            "benefic": {
                "theme": "Spiritual liberation and detachment cultivated",
                "theme_hi": "आध्यात्मिक मुक्ति और वैराग्य का विकास",
                "manifestation": "Intuitive wisdom, spiritual inclinations, detachment from material"
            },
            "malefic": {
                "theme": "Forced separation or incomplete spiritual growth",
                "theme_hi": "जबरदस्ती अलावा या अधूरी आध्यात्मिक वृद्धि",
                "manifestation": "Losses, isolation, spiritual confusion"
            },
            "mixed": {
                "theme": "Alternating between attachment and detachment",
                "theme_hi": "आसक्ति और वैराग्य के बीच बदलाव",
                "manifestation": "Periods of spiritual growth and material entanglement"
            }
        }
    }
    
    nature_key = nature.lower()
    planet_interp = interpretations.get(planet, {}).get(nature_key, {})
    
    return {
        "planet": planet,
        "d60_division": d60_name,
        "nature": nature,
        "theme": planet_interp.get("theme", "General karmic pattern"),
        "theme_hi": planet_interp.get("theme_hi", "सामान्य कर्मिक पैटर्न"),
        "manifestation": planet_interp.get("manifestation", "Varies by chart context")
    }


def _derive_life_purpose(karmic_themes: Dict, planetary_analysis: Dict) -> Dict[str, Any]:
    """
    Derive current life purpose based on D60 karmic patterns.
    """
    # Analyze which planets carry benefic vs malefic karma
    benefic_planets = karmic_themes["punya"]
    malefic_planets = karmic_themes["papa"]
    
    # Count by planet type
    luminaries_benefic = sum(1 for p in benefic_planets if p in ["Sun", "Moon"])
    luminaries_malefic = sum(1 for p in malefic_planets if p in ["Sun", "Moon"])
    
    # Determine primary life theme
    if luminaries_benefic >= 1 and len(benefic_planets) >= 4:
        purpose = {
            "primary": "Spiritual Leadership and Service",
            "primary_hi": "आध्यात्मिक नेतृत्व और सेवा",
            "description": "Your accumulated merit supports a path of guidance, teaching, and uplifting others.",
            "description_hi": "आपके अर्जित पुण्य मार्गदर्शन, शिक्षण और दूसरों को उठाने के पथ का समर्थन करते हैं।",
            "focus_areas": ["Teaching", "Mentoring", "Spiritual practice", "Community service"]
        }
    elif len(malefic_planets) >= 5:
        purpose = {
            "primary": "Karmic Purification and Transformation",
            "primary_hi": "कर्मिक शुद्धिकरण और परिवर्तन",
            "description": "This life focuses on resolving past burdens through conscious effort and remedial practices.",
            "description_hi": "यह जीवन सचेत प्रयास और उपाय अभ्यास के माध्यम से पिछले बोझ को हल करने पर केंद्रित है।",
            "focus_areas": ["Remedial measures", "Self-discipline", "Service to suffering", "Spiritual practice"]
        }
    elif "Jupiter" in benefic_planets and "Saturn" in benefic_planets:
        purpose = {
            "primary": "Wisdom through Responsibility",
            "primary_hi": "जिम्मेदारी के माध्यम से बुद्धि",
            "description": "Combine practical responsibility with higher learning for meaningful contribution.",
            "description_hi": "अर्थपूर्ण योगदान के लिए व्यावहारिक जिम्मेदारी को उच्च学习 के साथ जोड़ें।",
            "focus_areas": ["Education", "Counseling", "Administration", "Ethical business"]
        }
    elif "Mars" in malefic_planets and "Saturn" in malefic_planets:
        purpose = {
            "primary": "Channeling Energy Constructively",
            "primary_hi": "रचनात्मक रूप से ऊर्जा को चैनल करना",
            "description": "Transform aggressive or restrictive patterns into disciplined action and protection of others.",
            "description_hi": "आक्रामक या प्रतिबंधात्मक पैटर्न को अनुशासित कार्रवाई और दूसरों की सुरक्षा में बदलें।",
            "focus_areas": ["Physical disciplines", "Protective services", "Engineering", "Sports"]
        }
    elif "Venus" in benefic_planets and "Mercury" in benefic_planets:
        purpose = {
            "primary": "Creative Expression and Communication",
            "primary_hi": "रचनात्मक अभिव्यक्ति और संचार",
            "description": "Use artistic and intellectual gifts to inspire and connect with others.",
            "description_hi": "दूसरों को प्रेरित करने और जुड़ने के लिए कलात्मक और बौद्धिक उपहारों का उपयोग करें।",
            "focus_areas": ["Arts", "Writing", "Media", "Design", "Diplomacy"]
        }
    else:
        purpose = {
            "primary": "Balanced Growth through Experience",
            "primary_hi": "अनुभव के माध्यम से संतुलित विकास",
            "description": "Your mixed karmic pattern offers opportunities for growth across multiple life domains.",
            "description_hi": "आपका मिश्रित कर्मिक पैटर्न कई जीवन क्षेत्रों में विकास के अवसर प्रदान करता है।",
            "focus_areas": ["Self-awareness", "Relationship building", "Skill development", "Service"]
        }
    
    return purpose


def _identify_d60_karmic_debts(planetary_analysis: Dict) -> List[Dict[str, Any]]:
    """
    Identify specific karmic debts based on D60 planetary placements.
    """
    debts = []
    
    # Check for specific malefic patterns
    malefic_planets = [p for p, data in planetary_analysis.items() if data.get("nature") == "Malefic"]
    
    # Sun + Saturn both malefic = authority abuse debt
    if "Sun" in malefic_planets and "Saturn" in malefic_planets:
        debts.append({
            "debt_type": "Authority-Power Debt",
            "debt_type_hi": "अधिकार-शक्ति ऋण",
            "planets_involved": ["Sun", "Saturn"],
            "manifestation": "Challenges with authority figures, career blocks, father issues",
            "manifestation_hi": "अधिकारियों के साथ चुनौतियां, करियर में बाधाएं, पिता के मुद्दे",
            "resolution": "Respect elders, serve those in power with integrity, practice humility",
            "resolution_hi": "बड़ों का सम्मान करें, शक्ति में रहने वालों की ईमानदारी से सेवा करें, विनम्रता का अभ्यास करें"
        })
    
    # Moon + Rahu/Ketu malefic = emotional/maternal debt
    if "Moon" in malefic_planets and ("Rahu" in malefic_planets or "Ketu" in malefic_planets):
        debts.append({
            "debt_type": "Emotional-Maternal Debt",
            "debt_type_hi": "भावनात्मक-मातृ ऋण",
            "planets_involved": ["Moon", "Rahu" if "Rahu" in malefic_planets else "Ketu"],
            "manifestation": "Emotional instability, mother relationship challenges, mental confusion",
            "manifestation_hi": "भावनात्मक अस्थिरता, माँ के संबंध में चुनौतियां, मानसिक भ्रम",
            "resolution": "Nurture relationships, practice emotional awareness, honor mother figures",
            "resolution_hi": "संबंधों को पोषित करें, भावनात्मक जागरूकता का अभ्यास करें, मातृ आंकड़ों का सम्मान करें"
        })
    
    # Mars + Mercury malefic = speech-action debt
    if "Mars" in malefic_planets and "Mercury" in malefic_planets:
        debts.append({
            "debt_type": "Speech-Action Debt",
            "debt_type_hi": "वाणी-कर्म ऋण",
            "planets_involved": ["Mars", "Mercury"],
            "manifestation": "Harsh speech leading to conflicts, impulsive decisions, sibling rivalry",
            "manifestation_hi": "संघर्षों का कारण बनने वाली कठोर वाणी, आवेगपूर्ण निर्णय, भाई-बहन प्रतिद्वंद्विता",
            "resolution": "Practice mindful speech, channel aggression constructively, serve siblings",
            "resolution_hi": "सचेत वाणी का अभ्यास करें, आक्रामकता को रचनात्मक रूप से चैनल करें, भाई-बहनों की सेवा करें"
        })
    
    # Venus + Jupiter malefic = wisdom-wealth debt
    if "Venus" in malefic_planets and "Jupiter" in malefic_planets:
        debts.append({
            "debt_type": "Wisdom-Wealth Debt",
            "debt_type_hi": "बुद्धि-धन ऋण",
            "planets_involved": ["Venus", "Jupiter"],
            "manifestation": "Challenges in education, wealth fluctuations, teacher/mentor conflicts",
            "manifestation_hi": "शिक्षा में चुनौतियां, धन में उतार-चढ़ाव, शिक्षक/गुरु संघर्ष",
            "resolution": "Respect teachers, use wealth ethically, share knowledge generously",
            "resolution_hi": "शिक्षकों का सम्मान करें, नैतिक रूप से धन का उपयोग करें, ज्ञान उदारतापूर्वक साझा करें"
        })
    
    # If no specific debt pattern, check general malefic load
    if not debts and len(malefic_planets) >= 3:
        debts.append({
            "debt_type": "General Karmic Purification",
            "debt_type_hi": "सामान्य कर्मिक शुद्धिकरण",
            "planets_involved": malefic_planets,
            "manifestation": "Multiple life areas requiring conscious effort and remedial attention",
            "manifestation_hi": "कई जीवन क्षेत्र जिन्हें सचेत प्रयास और उपाय ध्यान की आवश्यकता है",
            "resolution": "Regular spiritual practice, selfless service, and planetary remedies",
            "resolution_hi": "नियमित आध्यात्मिक अभ्यास, निस्वार्थ सेवा, और ग्रह उपाय"
        })
    
    return debts


def _assess_remedy_accessibility(punya_score: float, papa_score: float) -> Dict[str, Any]:
    """
    Assess how accessible and effective remedies will be based on karmic balance.
    Reference: PDF 1.1.3 - D60 governs remedy effectiveness
    """
    if punya_score >= 60:
        return {
            "level": "High",
            "level_hi": "उच्च",
            "description": "Strong accumulated merit accelerates spiritual practices and remedial results.",
            "description_hi": "मजबूत अर्जित पुण्य आध्यात्मिक अभ्यासों और उपाय परिणामों को तेज करता है।",
            "effectiveness": "Remedies will yield quick and noticeable results",
            "effectiveness_hi": "उपाय त्वरित और स्पष्ट परिणाम देंगे",
            "recommendations": [
                {"en": "Engage in advanced spiritual practices", "hi": "उन्नत आध्यात्मिक अभ्यासों में लगें"},
                {"en": "Take on mentoring roles to share your merit", "hi": "अपने पुण्य को साझा करने के लिए मेंटरिंग की भूमिका निभाएं"}
            ]
        }
    elif punya_score >= 40:
        return {
            "level": "Moderate-High",
            "level_hi": "मध्यम-उच्च",
            "description": "Good karmic foundation supports steady progress with remedies.",
            "description_hi": "अच्छा कर्मिक आधार उपायों के साथ स्थिर प्रगति का समर्थन करता है।",
            "effectiveness": "Remedies will work with consistent practice over time",
            "effectiveness_hi": "उपाय समय के साथ लगातार अभ्यास से काम करेंगे",
            "recommendations": [
                {"en": "Maintain regular remedial practices", "hi": "नियमित उपाय अभ्यास बनाए रखें"},
                {"en": "Combine remedies with selfless service", "hi": "उपायों को निस्वार्थ सेवा के साथ जोड़ें"}
            ]
        }
    elif papa_score >= 60:
        return {
            "level": "Low",
            "level_hi": "कम",
            "description": "Heavy karmic burdens may delay or dilute remedial results. Patience required.",
            "description_hi": "भारी कर्मिक बोझ उपाय परिणामों में देरी या कमी कर सकता है। धैर्य आवश्यक।",
            "effectiveness": "Remedies require sustained effort and may show delayed results",
            "effectiveness_hi": "उपायों को sustained प्रयास की आवश्यकता है और देरी से परिणाम दिख सकते हैं",
            "recommendations": [
                {"en": "Perform intensive remedial measures (fire rituals, charities)", "hi": "गहन उपाय उपाय करें (यज्ञ, दान)"},
                {"en": "Focus on purification practices", "hi": "शुद्धिकरण अभ्यास पर ध्यान केंद्रित करें"},
                {"en": "Seek guidance from experienced practitioners", "hi": "अनुभवी व्यवसायियों से मार्गदर्शन खोजें"}
            ]
        }
    elif papa_score >= 40:
        return {
            "level": "Moderate",
            "level_hi": "मध्यम",
            "description": "Mixed karmic accessibility - remedies work but require dedicated effort.",
            "description_hi": "मिश्रित कर्मिक पहुंच - उपाय काम करते हैं लेकिन समर्पित प्रयास की आवश्यकता होती है।",
            "effectiveness": "Remedies effective with proper guidance and consistency",
            "effectiveness_hi": "उचित मार्गदर्शन और स्थिरता के साथ उपाय प्रभावी",
            "recommendations": [
                {"en": "Follow structured remedial protocols", "hi": "संरचित उपाय प्रोटोकॉल का पालन करें"},
                {"en": "Combine multiple remedial approaches", "hi": "कई उपाय दृष्टिकोणों को जोड़ें"}
            ]
        }
    else:
        return {
            "level": "Moderate",
            "level_hi": "मध्यम",
            "description": "Balanced karmic pattern - standard remedial approaches will yield results.",
            "description_hi": "संतुलित कर्मिक पैटर्न - मानक उपाय दृष्टिकोण परिणाम देंगे।",
            "effectiveness": "Remedies effective with regular practice",
            "effectiveness_hi": "नियमित अभ्यास के साथ उपाय प्रभावी",
            "recommendations": [
                {"en": "Maintain consistent spiritual practice", "hi": "लगातार आध्यात्मिक अभ्यास बनाए रखें"},
                {"en": "Balance material and spiritual pursuits", "hi": "भौतिक और आध्यात्मिक गतिविधियों को संतुलित करें"}
            ]
        }


def _sign_index(sign_name: str) -> int:
    """Return the 0-based index of a zodiac sign."""
    return _SIGN_NAMES.index(sign_name)


# ============================================================
# D2/D3/D30 Lord Significance Helpers (Phaladeepika Adh. 3)
# ============================================================

# Sign lord lookup
_SIGN_LORD: Dict[str, str] = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

# Trimsamsha lord lookup: returns lord planet name given odd/even sign & degree
# Odd signs: Mars 0-5, Saturn 5-10, Jupiter 10-18, Mercury 18-25, Venus 25-30
# Even signs: Venus 0-5, Mercury 5-12, Jupiter 12-20, Saturn 20-25, Mars 25-30
_TRIMSAMSHA_ODD: List[tuple] = [(5, "Mars"), (10, "Saturn"), (18, "Jupiter"), (25, "Mercury"), (30, "Venus")]
_TRIMSAMSHA_EVEN: List[tuple] = [(5, "Venus"), (12, "Mercury"), (20, "Jupiter"), (25, "Saturn"), (30, "Mars")]

# Drekkana type by (sign_element, decanate_part)
# Reference: Phaladeepika Drekkana types
# Elements: Fire(0), Earth(1), Air(2), Water(3)  (sign_index % 4 in sequence: 0,1,2,3)
# But sign element: Aries=Fire=0, Taurus=Earth=1, Gemini=Air=2, Cancer=Water=3 ...
_DREKKANA_TYPES: Dict[tuple, Dict[str, str]] = {
    # Fire signs (Aries=0, Leo=4, Sagittarius=8): 1st=Ayudha, 2nd=Pasa, 3rd=Nagala
    (0, 0): {"type": "Sarpa", "meaning_en": "Serpentine — hidden enemies, transformation", "meaning_hi": "सर्प — छिपे शत्रु, परिवर्तन"},
    (0, 1): {"type": "Ayudha", "meaning_en": "Weapon — courage, conflict, military prowess", "meaning_hi": "आयुध — साहस, संघर्ष, सैन्य पराक्रम"},
    (0, 2): {"type": "Pasa", "meaning_en": "Noose — bondage, legal issues, restrictions", "meaning_hi": "पाश — बंधन, कानूनी मामले, प्रतिबंध"},
    # Earth signs (Taurus=1, Virgo=5, Capricorn=9)
    (1, 0): {"type": "Pasa", "meaning_en": "Noose — bondage, legal issues, restrictions", "meaning_hi": "पाश — बंधन, कानूनी मामले, प्रतिबंध"},
    (1, 1): {"type": "Nagala", "meaning_en": "Chain — karma, imprisonment risk", "meaning_hi": "नागल — कर्म, कारावास का जोखिम"},
    (1, 2): {"type": "Ayudha", "meaning_en": "Weapon — courage, conflict, military prowess", "meaning_hi": "आयुध — साहस, संघर्ष, सैन्य पराक्रम"},
    # Air signs (Gemini=2, Libra=6, Aquarius=10)
    (2, 0): {"type": "Nagala", "meaning_en": "Chain — karma, imprisonment risk", "meaning_hi": "नागल — कर्म, कारावास का जोखिम"},
    (2, 1): {"type": "Sarpa", "meaning_en": "Serpentine — hidden enemies, transformation", "meaning_hi": "सर्प — छिपे शत्रु, परिवर्तन"},
    (2, 2): {"type": "Pasa", "meaning_en": "Noose — bondage, legal issues, restrictions", "meaning_hi": "पाश — बंधन, कानूनी मामले, प्रतिबंध"},
    # Water signs (Cancer=3, Scorpio=7, Pisces=11)
    (3, 0): {"type": "Ayudha", "meaning_en": "Weapon — courage, conflict, military prowess", "meaning_hi": "आयुध — साहस, संघर्ष, सैन्य पराक्रम"},
    (3, 1): {"type": "Pasa", "meaning_en": "Noose — bondage, legal issues, restrictions", "meaning_hi": "पाश — बंधन, कानूनी मामले, प्रतिबंध"},
    (3, 2): {"type": "Nagala", "meaning_en": "Chain — karma, imprisonment risk", "meaning_hi": "नागल — कर्म, कारावास का जोखिम"},
}


def _hora_lord_info(part: int) -> Dict[str, str]:
    """Return hora lord significance dict for D2. part=0→Sun, part=1→Moon."""
    if part == 0:
        return {
            "planet": "Sun",
            "sign": "Leo",
            "meaning_en": "Wealth through own efforts, father's lineage, leadership and authority.",
            "meaning_hi": "स्वयं के प्रयासों से धन, पितृ वंश, नेतृत्व और अधिकार।",
        }
    return {
        "planet": "Moon",
        "sign": "Cancer",
        "meaning_en": "Wealth through mother/family, passive income, emotional security.",
        "meaning_hi": "माता/परिवार से धन, निष्क्रिय आय, भावनात्मक सुरक्षा।",
    }


def _drekkana_lord_info(rasi_index: int, part: int) -> Dict[str, Any]:
    """Return drekkana lord and decanate type for D3."""
    decanate_names = ["1st", "2nd", "3rd"]
    offsets = [0, 4, 8]
    lord_sign_index = (rasi_index + offsets[part]) % 12
    lord_sign = _SIGN_NAMES[lord_sign_index]
    lord = _SIGN_LORD.get(lord_sign, "")
    element = rasi_index % 4  # 0=Fire,1=Earth,2=Air,3=Water
    dtype = _DREKKANA_TYPES.get((element, part), {
        "type": "Mixed",
        "meaning_en": "Indicates mixed results based on chart context.",
        "meaning_hi": "कुंडली के संदर्भ के अनुसार मिश्रित फल।",
    })
    return {
        "lord": lord,
        "decanate": decanate_names[part],
        "type": dtype["type"],
        "meaning_en": dtype["meaning_en"],
        "meaning_hi": dtype["meaning_hi"],
    }


def _trimsamsha_lord_info(rasi_index: int, degree_in_sign: float) -> Dict[str, str]:
    """Return trimsamsha lord for D30."""
    sign_number = rasi_index + 1
    ranges = _TRIMSAMSHA_ODD if sign_number % 2 == 1 else _TRIMSAMSHA_EVEN
    lord = ranges[-1][1]  # default last
    for end, planet in ranges:
        if degree_in_sign < end:
            lord = planet
            break

    _MEANINGS: Dict[str, Dict[str, str]] = {
        "Mars":    {"en": "Energy, courage, conflicts, surgery risk; indicates pitta-type ailments.", "hi": "ऊर्जा, साहस, संघर्ष, शल्य जोखिम; पित्त प्रकार की बीमारियां।"},
        "Saturn":  {"en": "Chronic issues, delays, karma, discipline; indicates vata-type ailments.", "hi": "दीर्घकालिक समस्याएं, देरी, कर्म, अनुशासन; वात प्रकार की बीमारियां।"},
        "Jupiter": {"en": "Wisdom, expansion, liver/fat issues; generally protective if well-placed.", "hi": "बुद्धि, विस्तार, यकृत/वसा समस्याएं; अच्छी स्थिति में सामान्यतः सुरक्षात्मक।"},
        "Mercury": {"en": "Nervous disorders, skin, speech; intelligence and communication challenges.", "hi": "तंत्रिका विकार, त्वचा, वाणी; बुद्धि और संचार चुनौतियां।"},
        "Venus":   {"en": "Reproductive/kidney issues, luxury, hormonal imbalance; sensual excess.", "hi": "प्रजनन/गुर्दे की समस्याएं, विलासिता, हार्मोनल असंतुलन; विषय-भोग की अधिकता।"},
    }
    meaning = _MEANINGS.get(lord, {"en": "", "hi": ""})
    return {
        "lord": lord,
        "meaning_en": meaning["en"],
        "meaning_hi": meaning["hi"],
    }


# ============================================================
# D2 -- Hora
# ============================================================

def _calculate_d2(planet_longitudes: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
    """
    Hora (D2): divide each sign into 2 halves (15 deg each).
    Odd signs: first half -> Leo (Sun), second half -> Cancer (Moon).
    Even signs: first half -> Cancer (Moon), second half -> Leo (Sun).
    """
    result: Dict[str, Dict[str, Any]] = {}
    for planet, lon in planet_longitudes.items():
        lon = lon % 360.0
        rasi_index = int(lon / 30.0)
        degree_in_sign = lon - rasi_index * 30.0
        part = 0 if degree_in_sign < 15.0 else 1
        sign_number = rasi_index + 1  # 1-indexed
        if sign_number % 2 == 1:  # Odd sign
            div_sign_index = 4 if part == 0 else 3  # Leo or Cancer
            hora_part = 0 if part == 0 else 1  # Sun or Moon
        else:  # Even sign
            div_sign_index = 3 if part == 0 else 4  # Cancer or Leo
            hora_part = 1 if part == 0 else 0  # Moon or Sun
        degree_within = (degree_in_sign % 15.0) * 2.0  # Scale to 0-30
        result[planet] = {
            "sign": _SIGN_NAMES[div_sign_index],
            "sign_index": div_sign_index,
            "degree": round(degree_within, 4),
            "hora_lord": _hora_lord_info(hora_part),
        }
    return result


# ============================================================
# D3 -- Drekkana
# ============================================================

def _calculate_d3(planet_longitudes: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
    """
    Drekkana (D3): divide each sign into 3 parts (10 deg each).
    Part 0 -> same sign, Part 1 -> 5th from sign, Part 2 -> 9th from sign.
    """
    result: Dict[str, Dict[str, Any]] = {}
    for planet, lon in planet_longitudes.items():
        lon = lon % 360.0
        rasi_index = int(lon / 30.0)
        degree_in_sign = lon - rasi_index * 30.0
        part = min(int(degree_in_sign / 10.0), 2)
        offsets = [0, 4, 8]  # same, 5th, 9th (0-indexed offsets)
        div_sign_index = (rasi_index + offsets[part]) % 12
        degree_within = (degree_in_sign % 10.0) * 3.0
        result[planet] = {
            "sign": _SIGN_NAMES[div_sign_index],
            "sign_index": div_sign_index,
            "degree": round(degree_within, 4),
            "drekkana_lord": _drekkana_lord_info(rasi_index, part),
        }
    return result


# ============================================================
# D4 -- Chaturthamsha
# ============================================================

def _calculate_d4(planet_longitudes: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
    """
    Chaturthamsha (D4): divide each sign into 4 parts (7.5 deg each).
    Starts from same sign, then advances by 3 signs (quadrants).
    """
    result: Dict[str, Dict[str, Any]] = {}
    part_size = 7.5
    for planet, lon in planet_longitudes.items():
        lon = lon % 360.0
        rasi_index = int(lon / 30.0)
        degree_in_sign = lon - rasi_index * 30.0
        part = min(int(degree_in_sign / part_size), 3)
        div_sign_index = (rasi_index + part * 3) % 12
        degree_within = (degree_in_sign % part_size) * 4.0
        result[planet] = {
            "sign": _SIGN_NAMES[div_sign_index],
            "sign_index": div_sign_index,
            "degree": round(degree_within, 4),
        }
    return result


# ============================================================
# D7 -- Saptamsha
# ============================================================

def _calculate_d7(planet_longitudes: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
    """
    Saptamsha (D7): divide each sign into 7 parts (4deg 17min 8.57sec each).
    Odd signs: start from same sign. Even signs: start from 7th from sign.
    """
    result: Dict[str, Dict[str, Any]] = {}
    part_size = 30.0 / 7.0
    for planet, lon in planet_longitudes.items():
        lon = lon % 360.0
        rasi_index = int(lon / 30.0)
        degree_in_sign = lon - rasi_index * 30.0
        part = min(int(degree_in_sign / part_size), 6)
        sign_number = rasi_index + 1
        if sign_number % 2 == 1:
            start = rasi_index
        else:
            start = (rasi_index + 6) % 12
        div_sign_index = (start + part) % 12
        degree_within = (degree_in_sign % part_size) * 7.0
        result[planet] = {
            "sign": _SIGN_NAMES[div_sign_index],
            "sign_index": div_sign_index,
            "degree": round(degree_within, 4),
        }
    return result


# ============================================================
# D9 -- Navamsa
# ============================================================

def _calculate_d9(planet_longitudes: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
    """
    Navamsa (D9): divide each sign into 9 parts (3deg 20min each).
    Fire signs start from Aries, Earth from Capricorn,
    Air from Libra, Water from Cancer.
    """
    result: Dict[str, Dict[str, Any]] = {}
    part_size = 30.0 / 9.0
    for planet, lon in planet_longitudes.items():
        lon = lon % 360.0
        rasi_index = int(lon / 30.0)
        degree_in_sign = lon - rasi_index * 30.0
        part = min(int(degree_in_sign / part_size), 8)
        element = rasi_index % 4  # 0=Fire, 1=Earth, 2=Air, 3=Water
        start_signs = {0: 0, 1: 9, 2: 6, 3: 3}
        start = start_signs[element]
        div_sign_index = (start + part) % 12
        degree_within = (degree_in_sign % part_size) * 9.0
        degree_within = degree_within % 30.0  # clamp float boundary: 30.0 → 0.0
        result[planet] = {
            "sign": _SIGN_NAMES[div_sign_index],
            "sign_index": div_sign_index,
            "degree": round(degree_within, 4),
        }
    return result


# ============================================================
# D10 -- Dasamsa
# ============================================================

def _calculate_d10(planet_longitudes: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
    """
    Dasamsa (D10): divide each sign into 10 parts (3 deg each).
    Odd signs: start from same sign. Even signs: start from 9th sign.
    """
    result: Dict[str, Dict[str, Any]] = {}
    for planet, lon in planet_longitudes.items():
        lon = lon % 360.0
        rasi_index = int(lon / 30.0)
        degree_in_sign = lon - rasi_index * 30.0
        part = min(int(degree_in_sign / 3.0), 9)
        sign_number = rasi_index + 1
        if sign_number % 2 == 1:
            start = rasi_index
        else:
            start = (rasi_index + 8) % 12  # 9th sign = +8 in 0-indexed
        div_sign_index = (start + part) % 12
        degree_within = (degree_in_sign % 3.0) * 10.0
        degree_within = degree_within % 30.0  # clamp float boundary: 30.0 → 0.0
        result[planet] = {
            "sign": _SIGN_NAMES[div_sign_index],
            "sign_index": div_sign_index,
            "degree": round(degree_within, 4),
        }
    return result


# ============================================================
# D12 -- Dwadashamsha
# ============================================================

def _calculate_d12(planet_longitudes: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
    """
    Dwadashamsha (D12): divide each sign into 12 parts (2.5 deg each).
    Starts from same sign, advances through all 12 signs.
    """
    result: Dict[str, Dict[str, Any]] = {}
    part_size = 2.5
    for planet, lon in planet_longitudes.items():
        lon = lon % 360.0
        rasi_index = int(lon / 30.0)
        degree_in_sign = lon - rasi_index * 30.0
        part = min(int(degree_in_sign / part_size), 11)
        div_sign_index = (rasi_index + part) % 12
        degree_within = (degree_in_sign % part_size) * 12.0
        degree_within = degree_within % 30.0  # clamp float boundary: 30.0 → 0.0
        result[planet] = {
            "sign": _SIGN_NAMES[div_sign_index],
            "sign_index": div_sign_index,
            "degree": round(degree_within, 4),
        }
    return result


# ============================================================
# D30 -- Trimshamsha
# ============================================================

def _calculate_d30(planet_longitudes: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
    """
    Trimshamsha (D30): 1 deg per division.
    Odd signs: 0-5 Mars, 5-10 Saturn, 10-18 Jupiter, 18-25 Mercury, 25-30 Venus.
    Even signs: reversed order.
    """
    # Odd sign boundaries and lords
    odd_ranges = [(5, 4), (10, 6), (18, 5), (25, 2), (30, 3)]   # (end, sign_index for lord)
    even_ranges = [(5, 3), (12, 2), (20, 5), (25, 6), (30, 4)]  # BPHS even: 5,7,8,5,5 degrees
    # Mars=Aries(0)/Scorpio(7), Saturn=Cap(9)/Aqu(10), Jupiter=Sag(8)/Pisces(11),
    # Mercury=Gem(2)/Virgo(5), Venus=Tau(1)/Libra(6)
    odd_signs = [0, 10, 8, 2, 1]   # Mars=Aries, Saturn=Aquarius, Jupiter=Sag, Mercury=Gemini, Venus=Taurus
    even_signs = [6, 5, 11, 9, 7]  # Venus=Libra, Mercury=Virgo, Jupiter=Pisces, Saturn=Cap, Mars=Scorpio

    result: Dict[str, Dict[str, Any]] = {}
    for planet, lon in planet_longitudes.items():
        lon = lon % 360.0
        rasi_index = int(lon / 30.0)
        degree_in_sign = lon - rasi_index * 30.0
        sign_number = rasi_index + 1

        if sign_number % 2 == 1:
            signs_list = odd_signs
            ranges = odd_ranges
        else:
            signs_list = even_signs
            ranges = even_ranges

        div_sign_index = signs_list[0]
        prev_end = 0.0
        for i, (end, _) in enumerate(ranges):
            if degree_in_sign < end:
                div_sign_index = signs_list[i]
                break
            prev_end = end

        degree_within = degree_in_sign  # 1:1 mapping for D30
        result[planet] = {
            "sign": _SIGN_NAMES[div_sign_index],
            "sign_index": div_sign_index,
            "degree": round(degree_within, 4),
            "trimsamsha_lord": _trimsamsha_lord_info(rasi_index, degree_in_sign),
        }
    return result


# ============================================================
# D108 -- Ashtottaramsa
# ============================================================

# Sign classification for D108 (navamsa-like cycling)
_MOVABLE_SIGNS = {0, 3, 6, 9}    # Aries, Cancer, Libra, Capricorn
_FIXED_SIGNS = {1, 4, 7, 10}     # Taurus, Leo, Scorpio, Aquarius
_DUAL_SIGNS = {2, 5, 8, 11}      # Gemini, Virgo, Sagittarius, Pisces

# Exaltation and own-sign data for spiritual strength assessment in D108
_EXALTATION_SIGNS = {
    "Sun": 0, "Moon": 1, "Mars": 9, "Mercury": 5,
    "Jupiter": 3, "Venus": 11, "Saturn": 6,
    "Rahu": 1, "Ketu": 7,
}
_OWN_SIGNS = {
    "Sun": [4], "Moon": [3], "Mars": [0, 7], "Mercury": [2, 5],
    "Jupiter": [8, 11], "Venus": [1, 6], "Saturn": [9, 10],
    "Rahu": [10], "Ketu": [7],
}


def _calculate_d108(planet_longitudes: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
    """
    Ashtottaramsa (D108): divide each sign into 108 parts (16'40" = 0.27778 deg each).
    Uses navamsa-like starting-sign logic:
      - Movable signs (Aries, Cancer, Libra, Capricorn): start from same sign
      - Fixed signs (Taurus, Leo, Scorpio, Aquarius): start from 9th sign (+8)
      - Dual signs (Gemini, Virgo, Sagittarius, Pisces): start from 5th sign (+4)
    Then count part_number signs forward from the starting sign.
    """
    result: Dict[str, Dict[str, Any]] = {}
    part_size = 30.0 / 108.0  # 0.277777... degrees

    for planet, lon in planet_longitudes.items():
        lon = lon % 360.0
        rasi_index = int(lon / 30.0) % 12
        degree_in_sign = lon - (int(lon / 30.0)) * 30.0

        part = min(int(degree_in_sign / part_size), 107)

        # Determine starting sign based on sign type (navamsa-like rule)
        if rasi_index in _MOVABLE_SIGNS:
            start = rasi_index           # same sign
        elif rasi_index in _FIXED_SIGNS:
            start = (rasi_index + 8) % 12  # 9th from sign
        else:  # dual
            start = (rasi_index + 4) % 12  # 5th from sign

        div_sign_index = (start + part) % 12

        degree_within = (degree_in_sign % part_size) * 108.0
        degree_within = degree_within % 30.0  # clamp float boundary

        result[planet] = {
            "sign": _SIGN_NAMES[div_sign_index],
            "sign_index": div_sign_index,
            "degree": round(degree_within, 4),
        }
    return result


def calculate_d108_analysis(
    planet_longitudes: Dict[str, float],
) -> Dict[str, Any]:
    """
    Detailed D108 Ashtottaramsa analysis — deepest karmic chart.

    D108 reveals past-life spiritual progress, moksha indicators, and the
    deepest karmic patterns.  108 is the sacred count of Vedic beads,
    Sri Yantra intersections, and Upanishadic mantras.

    Returns:
        {
          d108_positions, spiritual_indicators, moksha_potential,
          past_life_karma, interpretation
        }
    """
    # 1. Compute D108 positions
    d108_raw = _calculate_d108(planet_longitudes)
    d108_positions: Dict[str, Dict[str, Any]] = {}
    for planet, info in d108_raw.items():
        d108_positions[planet] = {
            "sign": info["sign"],
            "degree": info["degree"],
        }

    # 2. Spiritual indicators — planets in own sign or exalted in D108
    spiritual_indicators: List[Dict[str, Any]] = []
    moksha_factors: List[str] = []
    moksha_score = 0

    for planet, info in d108_raw.items():
        sign_idx = info["sign_index"]
        is_exalted = (_EXALTATION_SIGNS.get(planet) == sign_idx)
        is_own = sign_idx in _OWN_SIGNS.get(planet, [])

        if is_exalted:
            spiritual_indicators.append({
                "planet": planet,
                "condition": "exalted",
                "sign": info["sign"],
                "meaning": f"{planet} exalted in D108 — strong spiritual karma from past lives",
            })
            moksha_score += 15

        if is_own:
            spiritual_indicators.append({
                "planet": planet,
                "condition": "own_sign",
                "sign": info["sign"],
                "meaning": f"{planet} in own sign in D108 — self-earned spiritual merit",
            })
            moksha_score += 10

    # Moksha-karaka planets (Jupiter, Ketu, Moon) in kendra (1,4,7,10)
    # from D108 Ascendant-equivalent (Sun used as proxy)
    sun_d108_sign = d108_raw.get("Sun", {}).get("sign_index", 0)
    moksha_karakas = ["Jupiter", "Ketu", "Moon"]
    for mk in moksha_karakas:
        if mk in d108_raw:
            mk_sign = d108_raw[mk]["sign_index"]
            house_from_sun = (mk_sign - sun_d108_sign) % 12 + 1
            if house_from_sun in (1, 4, 7, 10):
                factor = f"{mk} in kendra (house {house_from_sun}) from D108 Sun — moksha support"
                moksha_factors.append(factor)
                moksha_score += 12

    # Saturn-Ketu conjunction or mutual aspect enhances detachment
    if "Saturn" in d108_raw and "Ketu" in d108_raw:
        if d108_raw["Saturn"]["sign_index"] == d108_raw["Ketu"]["sign_index"]:
            moksha_factors.append("Saturn-Ketu conjunction in D108 — deep vairagya (detachment)")
            moksha_score += 10

    # Jupiter-Ketu conjunction — gnana yoga
    if "Jupiter" in d108_raw and "Ketu" in d108_raw:
        if d108_raw["Jupiter"]["sign_index"] == d108_raw["Ketu"]["sign_index"]:
            moksha_factors.append("Jupiter-Ketu conjunction in D108 — Gnana Yoga (liberation through wisdom)")
            moksha_score += 15

    moksha_score = min(moksha_score, 100)

    # 3. Past-life karma analysis
    past_life_karma: List[Dict[str, str]] = []

    # Rahu-Ketu axis in D108 reveals the karmic direction
    if "Rahu" in d108_raw and "Ketu" in d108_raw:
        rahu_sign = d108_raw["Rahu"]["sign"]
        ketu_sign = d108_raw["Ketu"]["sign"]
        past_life_karma.append({
            "axis": "Rahu-Ketu",
            "rahu_sign": rahu_sign,
            "ketu_sign": ketu_sign,
            "meaning": (
                f"Ketu in {ketu_sign} (D108) — mastered qualities of {ketu_sign} in past lives. "
                f"Rahu in {rahu_sign} — current life soul growth direction."
            ),
        })

    # Saturn in D108 — karmic debts
    if "Saturn" in d108_raw:
        sat_sign = d108_raw["Saturn"]["sign"]
        sat_idx = d108_raw["Saturn"]["sign_index"]
        sat_exalted = (_EXALTATION_SIGNS.get("Saturn") == sat_idx)
        sat_own = sat_idx in _OWN_SIGNS.get("Saturn", [])
        if sat_exalted or sat_own:
            past_life_karma.append({
                "planet": "Saturn",
                "sign": sat_sign,
                "meaning": f"Saturn dignified in D108 ({sat_sign}) — past-life duties fulfilled; lighter karmic load",
            })
        else:
            past_life_karma.append({
                "planet": "Saturn",
                "sign": sat_sign,
                "meaning": f"Saturn in {sat_sign} in D108 — unresolved karmic debts requiring discipline and service",
            })

    # Sun in D108 — soul's past-life identity
    if "Sun" in d108_raw:
        sun_sign = d108_raw["Sun"]["sign"]
        past_life_karma.append({
            "planet": "Sun",
            "sign": sun_sign,
            "meaning": f"Sun in {sun_sign} in D108 — the soul's core identity carried from past incarnations",
        })

    # 4. Build overall interpretation
    if moksha_score >= 70:
        interpretation = (
            "Very strong spiritual chart. Multiple indicators suggest advanced spiritual "
            "progress from past lives. Moksha (liberation) is a realistic pursuit in this "
            "lifetime with dedicated sadhana."
        )
    elif moksha_score >= 40:
        interpretation = (
            "Moderate spiritual potential. Some past-life spiritual merit is present. "
            "Consistent practice and guru guidance can unlock deeper realization. "
            "Focus on the moksha-karaka planets for remedial support."
        )
    elif moksha_score >= 20:
        interpretation = (
            "Developing spiritual chart. Past-life karma is more material than spiritual. "
            "This lifetime offers opportunities to begin serious spiritual work. "
            "Service (seva) and devotion (bhakti) are recommended starting points."
        )
    else:
        interpretation = (
            "Predominantly material karmic pattern in D108. Past lives were focused on "
            "worldly achievement rather than spiritual growth. Current life can plant seeds "
            "of spiritual progress through charity, pilgrimage, and mantra practice."
        )

    return {
        "d108_positions": d108_positions,
        "spiritual_indicators": spiritual_indicators,
        "moksha_potential": {
            "score": moksha_score,
            "max": 100,
            "factors": moksha_factors,
        },
        "past_life_karma": past_life_karma,
        "interpretation": interpretation,
    }


# ============================================================
# GENERIC -- For D16, D20, D24, D27, D40, D45, D60
# ============================================================

def _calculate_generic(
    planet_longitudes: Dict[str, float], division: int,
) -> Dict[str, Dict[str, Any]]:
    """
    Generic divisional chart using cyclic formula.
    part_index = floor(degree_in_sign / (30/division))
    result_sign = (rasi_index * division + part_index) mod 12
    """
    result: Dict[str, Dict[str, Any]] = {}
    part_size = 30.0 / division

    for planet, lon in planet_longitudes.items():
        lon = lon % 360.0
        rasi_index = int(lon / 30.0)
        degree_in_sign = lon - rasi_index * 30.0
        part_index = min(int(degree_in_sign / part_size), division - 1)
        div_sign_index = (rasi_index * division + part_index) % 12
        degree_within = (degree_in_sign % part_size) * division
        degree_within = degree_within % 30.0  # clamp float boundary: 30.0 → 0.0
        result[planet] = {
            "sign": _SIGN_NAMES[div_sign_index],
            "sign_index": div_sign_index,
            "degree": round(degree_within, 4),
        }
    return result


# ============================================================
# PUBLIC API
# ============================================================

def calculate_divisional_chart(
    planet_longitudes: Dict[str, float], division: int,
) -> Dict[str, str]:
    """
    Calculate a divisional chart. Returns simple {planet: sign} mapping.
    Backward-compatible API.
    """
    detailed = calculate_divisional_chart_detailed(planet_longitudes, division)
    return {planet: info["sign"] for planet, info in detailed.items()}


def calculate_divisional_chart_detailed(
    planet_longitudes: Dict[str, float], division: int,
) -> Dict[str, Dict[str, Any]]:
    """
    Calculate a divisional chart with detailed info per planet.

    Returns:
        {planet_name: {sign, sign_index, degree}}
    """
    if division < 1:
        raise ValueError("Division must be >= 1")
    if division == 1:
        # D1 = Rashi chart, just return as-is
        result: Dict[str, Dict[str, Any]] = {}
        for planet, lon in planet_longitudes.items():
            lon = lon % 360.0
            rasi_index = int(lon / 30.0)
            result[planet] = {
                "sign": _SIGN_NAMES[rasi_index],
                "sign_index": rasi_index,
                "degree": round(lon % 30.0, 4),
            }
        return result

    dispatch = {
        2: _calculate_d2,
        3: _calculate_d3,
        4: _calculate_d4,
        7: _calculate_d7,
        9: _calculate_d9,
        10: _calculate_d10,
        12: _calculate_d12,
        30: _calculate_d30,
        108: _calculate_d108,
    }

    if division in dispatch:
        return dispatch[division](planet_longitudes)
    return _calculate_generic(planet_longitudes, division)


def calculate_divisional_ascendant(
    ascendant_longitude: float, division: int,
) -> Dict[str, Any]:
    """
    Calculate the divisional chart ascendant by passing the natal ascendant
    longitude through the same divisional formula used for planets.

    Returns:
        {sign, sign_index, degree}
    """
    detailed = calculate_divisional_chart_detailed(
        {"_Ascendant": ascendant_longitude}, division,
    )
    return detailed["_Ascendant"]


def calculate_divisional_houses(
    ascendant_longitude: float, division: int,
) -> List[Dict[str, Any]]:
    """
    Build the 12-house mapping for a divisional chart, relative to the
    divisional ascendant.

    The divisional ascendant's sign becomes House 1, the next sign
    becomes House 2, and so on through all 12 houses.

    Returns:
        [{number: 1, sign: "Libra"}, {number: 2, sign: "Scorpio"}, ...]
    """
    asc_info = calculate_divisional_ascendant(ascendant_longitude, division)
    asc_sign_index = asc_info["sign_index"]
    return [
        {
            "number": i + 1,
            "sign": _SIGN_NAMES[(asc_sign_index + i) % 12],
        }
        for i in range(12)
    ]
