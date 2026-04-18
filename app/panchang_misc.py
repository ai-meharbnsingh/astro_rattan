"""
panchang_misc.py -- Miscellaneous Panchang Calculations
========================================================
Pure calculation functions (no Flask/FastAPI dependencies).
All strings carry both English AND Hindi labels.

Calculations covered:
- Mantri Mandala (planetary cabinet for the Hindu year)
- Kaliyuga & astronomical epoch data (Kali Ahargana, Rata Die, MJD)
- Panchaka Rahita Muhurta (safe/unsafe windows during Panchaka)
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

# ============================================================
# MANTRI MANDALA — Planetary Cabinet (मन्त्री मण्डल)
# ============================================================
# The 10 roles in the Mantri Mandala, assigned cyclically from the
# Raja (King) planet determined by the weekday of Chaitra Shukla
# Pratipada for the given Vikram Samvat year.

MANDALA_ROLES: List[tuple[str, str]] = [
    ("Raja", "राजा"),                    # King
    ("Mantri", "मन्त्री"),              # Minister
    ("Senadhipati", "सेनाधिपति"),       # Commander
    ("Sasyadhipati", "सस्याधिपति"),     # Crops Lord
    ("Dhanyadhipati", "धान्याधिपति"),   # Grain Lord
    ("Dhanadhipati", "धनाधिपति"),       # Wealth Lord
    ("Meghadhipati", "मेघाधिपति"),      # Rain Lord
    ("Rasadhipati", "रसाधिपति"),        # Liquids Lord
    ("Nirasadhipati", "नीरसाधिपति"),    # Minerals Lord
    ("Phaladhipati", "फलाधिपति"),       # Fruits Lord
]

PLANET_NAMES: Dict[str, str] = {
    "Sun": "सूर्य",
    "Moon": "चन्द्र",
    "Mars": "मंगल",
    "Mercury": "बुध",
    "Jupiter": "बृहस्पति",
    "Venus": "शुक्र",
    "Saturn": "शनि",
}

# Classical 7-planet weekday order (Sun=Sunday .. Saturn=Saturday)
GRAHA_ORDER: List[str] = [
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
]

# Raja planet for recent Vikram Samvat years (based on weekday of
# Chaitra Shukla Pratipada).  Extend as needed.
SAMVAT_RAJA: Dict[int, str] = {
    2080: "Mercury",  # 2023-24
    2081: "Jupiter",  # 2024-25
    2082: "Saturn",   # 2025-26
    2083: "Sun",      # 2026-27
    2084: "Moon",     # 2027-28
}

# ============================================================
# MANTRI SIGNIFICANCE — Planet Interpretations per Role
# ============================================================
# Classical meanings when each planet occupies a Mandala role.
# Key: ("Role", "Planet") → (English significance, Hindi significance)

MANTRI_SIGNIFICANCE: Dict[tuple[str, str], tuple[str, str]] = {
    # Raja (King) — Year's overarching theme
    ("Raja", "Sun"): ("Radiant, authoritative year. Leadership, expansion & fame dominate.", "तेजस्वी, प्रभावशाली वर्ष। नेतृत्व, विस्तार और यश प्रमुख।"),
    ("Raja", "Moon"): ("Emotionally complex year. Welfare, benevolence & fluctuations dominate.", "भावनात्मक रूप से जटिल वर्ष। कल्याण, दया और उतार-चढ़ाव प्रमुख।"),
    ("Raja", "Mars"): ("Violent, aggressive year. Conflicts, strife & military action increase.", "हिंसक, आक्रामक वर्ष। संघर्ष, विरोध और युद्ध में वृद्धि।"),
    ("Raja", "Mercury"): ("Intellectual, communicative year. Trade, learning & commerce flourish.", "बौद्धिक, संचारी वर्ष। व्यापार, सीखना और वाणिज्य फलते-फूलते हैं।"),
    ("Raja", "Jupiter"): ("Prosperous, blessed year. Righteousness & dharma expand; abundant gains.", "समृद्ध, आशीर्वादित वर्ष। धर्म का विस्तार; भरपूर लाभ।"),
    ("Raja", "Venus"): ("Pleasure, beauty year. Arts, romance & luxury dominate. Comfort rises.", "सुख, सौंदर्य का वर्ष। कला, प्रेम और विलासिता प्रमुख। आराम बढ़ता है।"),
    ("Raja", "Saturn"): ("Hardship, austere year. Suffering, delays & constraint. Discipline required.", "कठिनाई, तपस्वी वर्ष। पीड़ा, देरी और सीमा। अनुशासन आवश्यक।"),

    # Mantri (Minister) — Counsel & policy
    ("Mantri", "Sun"): ("Wise, principled advice. Clarity in governance & truthfulness in counsel.", "बुद्धिमान, नैतिक सलाह। शासन में स्पष्टता और सत्य।"),
    ("Mantri", "Moon"): ("Compassionate counsel. Public welfare & emotional intelligence guide policy.", "दयालु सलाह। जनकल्याण और भावनात्मक बुद्धिमत्ता नीति निर्देशित करती है।"),
    ("Mantri", "Mars"): ("Aggressive strategy. Bold military moves & forceful implementation of policy.", "आक्रामक रणनीति। साहसी सैन्य कदम और नीति का दृढ़ कार्यान्वयन।"),
    ("Mantri", "Mercury"): ("Clever tactics. Political maneuvering & trade advantages guide counsel.", "चतुर रणनीति। राजनीतिक कौशल और व्यापार लाभ सलाह निर्देशित करते हैं।"),
    ("Mantri", "Jupiter"): ("Righteous policy. Expansion of dharma & beneficial laws dominate counsel.", "धार्मिक नीति। धर्म का विस्तार और लाभकारी कानून प्रमुख।"),
    ("Mantri", "Venus"): ("Pleasure-focused governance. Arts patronage & soft diplomacy guide counsel.", "सुख-केंद्रित शासन। कला संरक्षण और कोमल कूटनीति प्रमुख।"),
    ("Mantri", "Saturn"): ("Conservative, austere counsel. Austerity, restriction & discipline guide policy.", "रूढ़िवादी, तपस्वी सलाह। कठोरता, प्रतिबंध और अनुशासन नीति निर्देशित करते हैं।"),

    # Senadhipati (Commander) — Military & defense
    ("Senadhipati", "Sun"): ("Fierce military commander. Strong defense & heroic victories likely.", "भयानक सेना प्रमुख। मजबूत रक्षा और वीरतापूर्ण जीत संभव।"),
    ("Senadhipati", "Moon"): ("Protective, cautious commander. Naval strength & defense of realm.", "सुरक्षात्मक, सावधान सेना प्रमुख। नौसेना की शक्ति और क्षेत्र की रक्षा।"),
    ("Senadhipati", "Mars"): ("Aggressive warrior. Victories likely; military expansion & conquest.", "आक्रामक योद्धा। जीत संभव; सैन्य विस्तार और विजय।"),
    ("Senadhipati", "Mercury"): ("Strategic, cunning general. Espionage, diplomacy & clever tactics.", "रणनीतिक, चतुर सेनापति। गुप्तचरी, राजनीति और चतुर रणनीति।"),
    ("Senadhipati", "Jupiter"): ("Just, honored commander. Righteous victories & moral military leadership.", "न्यायप्रिय, सम्मानित सेनापति। धार्मिक जीत और नैतिक नेतृत्व।"),
    ("Senadhipati", "Venus"): ("Reluctant warrior. Diplomatic generals; peaceful resolution preferred.", "अनिच्छुक योद्धा। राजनयिक सेनापति; शांतिपूर्ण समाधान पसंद।"),
    ("Senadhipati", "Saturn"): ("Cautious, defensive commander. Prolonged sieges & fortifications prominent.", "सावधान, रक्षात्मक सेनापति। लंबी घेराबंदी और किलेबंदी प्रमुख।"),

    # Sasyadhipati (Crops Lord) — Agriculture & harvests
    ("Sasyadhipati", "Sun"): ("Abundant harvests. Crops flourish; sunshine & growth optimal.", "प्रचुर फसलें। खेती फलती-फूलती है; सूर्य और वृद्धि इष्टतम।"),
    ("Sasyadhipati", "Moon"): ("Variable harvests. Moisture & rainfall fluctuate; irrigation critical.", "परिवर्तनशील फसलें। नमी और वर्षा उतार-चढ़ाव; सिंचाई महत्वपूर्ण।"),
    ("Sasyadhipati", "Mars"): ("Crop damage. Pests, heat & drying winds; losses likely.", "फसल को नुकसान। कीट, गर्मी और सूखी हवाएं; नुकसान संभव।"),
    ("Sasyadhipati", "Mercury"): ("Productive agriculture. Good yields & commerce of crops flourishes.", "उत्पादक कृषि। अच्छी पैदावार और फसलों का वाणिज्य फलता है।"),
    ("Sasyadhipati", "Jupiter"): ("Excellent harvests. Abundance & prosperity in agriculture; bountiful yields.", "उत्कृष्ट फसलें। कृषि में प्रचुरता और समृद्धि; भरपूर पैदावार।"),
    ("Sasyadhipati", "Venus"): ("Pleasant crops. Beautiful harvests; luxury crops flourish.", "सुखद फसलें। सुंदर पैदावार; लक्जरी फसलें फलती-फूलती हैं।"),
    ("Sasyadhipati", "Saturn"): ("Poor harvests. Drought, delay & hardship; crop losses likely.", "खराब फसलें। सूखा, देरी और कठिनाई; फसल का नुकसान संभव।"),

    # Dhanyadhipati (Grain Lord) — Grain stores & supply
    ("Dhanyadhipati", "Sun"): ("Ample grain. Storage & supply excellent; food security high.", "पर्याप्त अनाज। भंडारण और आपूर्ति उत्कृष्ट; खाद्य सुरक्षा अच्छी।"),
    ("Dhanyadhipati", "Moon"): ("Fluctuating grain. Supply varies; careful management needed.", "उतार-चढ़ाव वाला अनाज। आपूर्ति में भिन्नता; सावधान प्रबंधन आवश्यक।"),
    ("Dhanyadhipati", "Mars"): ("Grain shortage. Losses, theft & consumption; scarcity risk.", "अनाज की कमी। नुकसान, चोरी और खपत; कमी का जोखिम।"),
    ("Dhanyadhipati", "Mercury"): ("Good grain trade. Storage & distribution efficient; commerce smooth.", "अनाज का अच्छा व्यापार। भंडारण और वितरण कुशल; व्यापार सुचारु।"),
    ("Dhanyadhipati", "Jupiter"): ("Abundant grain. Reserves plentiful; food security & prosperity.", "प्रचुर अनाज। भंडार भरपूर; खाद्य सुरक्षा और समृद्धि।"),
    ("Dhanyadhipati", "Venus"): ("Quality grain. Excellent storage; grain of high quality.", "गुणवत्तापूर्ण अनाज। उत्कृष्ट भंडारण; उच्च गुणवत्ता वाला अनाज।"),
    ("Dhanyadhipati", "Saturn"): ("Grain shortage. Depreciation, loss & rationing; scarcity increases.", "अनाज की कमी। मूल्य में गिरावट, नुकसान और राशनिंग; कमी बढ़ता है।"),

    # Dhanadhipati (Wealth Lord) — Treasury & finances
    ("Dhanadhipati", "Sun"): ("Ample wealth. Treasury thrives; radiance of prosperity increases.", "प्रचुर धन। कोषागार फलता है; समृद्धि का तेज बढ़ता है।"),
    ("Dhanadhipati", "Moon"): ("Fluctuating wealth. Cash flow varies; careful accounting essential.", "उतार-चढ़ाव वाली संपत्ति। नकद प्रवाह में भिन्नता; सावधान लेखांकन आवश्यक।"),
    ("Dhanadhipati", "Mars"): ("Wealth loss. Theft, expenditure & depletion of treasury likely.", "धन की हानि। चोरी, व्यय और कोषागार की कमी संभव।"),
    ("Dhanadhipati", "Mercury"): ("Good financial trade. Banking & commerce thrive; wealth increases.", "अच्छा वित्तीय व्यापार। बैंकिंग और वाणिज्य फलते-फूलते हैं; धन बढ़ता है।"),
    ("Dhanadhipati", "Jupiter"): ("Prosperity & gain. Treasury flourishes; wealth & riches abound.", "समृद्धि और लाभ। कोषागार फलता है; धन और दौलत प्रचुर।"),
    ("Dhanadhipati", "Venus"): ("Pleasure spending. Treasury used for luxury & comfort; pleasure-focused.", "सुख व्यय। कोषागार विलासिता और आराम के लिए उपयोग; सुख-केंद्रित।"),
    ("Dhanadhipati", "Saturn"): ("Treasury loss. Depletion, depreciation & deficit; scarcity increases.", "कोषागार का नुकसान। कमी, मूल्य में गिरावट और घाटा; कमी बढ़ता है।"),

    # Meghadhipati (Rain Lord) — Rainfall & weather
    ("Meghadhipati", "Sun"): ("Bright skies. Scanty rainfall; dry season dominant.", "उज्ज्वल आसमान। कम वर्षा; शुष्क मौसम प्रभावी।"),
    ("Meghadhipati", "Moon"): ("Good rainfall. Clouds & moisture; normal to abundant rains.", "अच्छी वर्षा। बादल और नमी; सामान्य से प्रचुर वर्षा।"),
    ("Meghadhipati", "Mars"): ("Violent weather. Storms, hail & severe precipitation; flooding risk.", "हिंसक मौसम। तूफान, ओले और तीव्र वर्षा; बाढ़ का जोखिम।"),
    ("Meghadhipati", "Mercury"): ("Variable weather. Irregular rainfall; unpredictable seasons.", "परिवर्तनशील मौसम। अनियमित वर्षा; अप्रत्याशित मौसम।"),
    ("Meghadhipati", "Jupiter"): ("Abundant rainfall. Healthy clouds & moisture; timely, beneficial rains.", "प्रचुर वर्षा। स्वस्थ बादल और नमी; समय पर, लाभकारी वर्षा।"),
    ("Meghadhipati", "Venus"): ("Pleasant weather. Gentle rains & mild climate; comfortable conditions.", "सुखद मौसम। हल्की वर्षा और हल्की जलवायु; आरामदायक परिस्थितियाँ।"),
    ("Meghadhipati", "Saturn"): ("Drought risk. Scanty rainfall; dry conditions & weather extremes.", "सूखे का जोखिम। कम वर्षा; शुष्क परिस्थितियाँ और मौसम की चरम सीमा।"),

    # Rasadhipati (Liquids Lord) — Water, liquids & fluids
    ("Rasadhipati", "Sun"): ("Liquid clarity. Water supply excellent; oils & fluids abundant.", "तरल स्पष्टता। जल आपूर्ति उत्कृष्ट; तेल और तरल प्रचुर।"),
    ("Rasadhipati", "Moon"): ("Fluid flows. Water resources plentiful; aquatic products thrive.", "तरल प्रवाह। जल संसाधन प्रचुर; जलीय उत्पाद फलते-फूलते हैं।"),
    ("Rasadhipati", "Mars"): ("Liquid loss. Water loss, spills & contamination; scarcity risk.", "तरल की हानि। जल हानि, रिसाव और प्रदूषण; कमी का जोखिम।"),
    ("Rasadhipati", "Mercury"): ("Good liquid trade. Oil, wine & beverage commerce flourish.", "अच्छा तरल व्यापार। तेल, शराब और पेय व्यापार फलते-फूलते हैं।"),
    ("Rasadhipati", "Jupiter"): ("Abundant liquids. Water & oil reserves plentiful; prosperity.", "प्रचुर तरल। जल और तेल के भंडार प्रचुर; समृद्धि।"),
    ("Rasadhipati", "Venus"): ("Pleasant liquids. Refined oils, wines & beverages of quality.", "सुखद तरल। परिष्कृत तेल, शराब और उच्च गुणवत्ता वाले पेय।"),
    ("Rasadhipati", "Saturn"): ("Liquid shortage. Water scarcity, contamination & depletion.", "तरल की कमी। जल की कमी, प्रदूषण और कमी।"),

    # Nirasadhipati (Minerals Lord) — Metals, gems & minerals
    ("Nirasadhipati", "Sun"): ("Abundant metals. Gold & precious metals thrive; mining prosperous.", "प्रचुर धातु। सोना और मूल्यवान धातु फलती-फूलती हैं; खनन समृद्ध।"),
    ("Nirasadhipati", "Moon"): ("Variable minerals. Gem & metal yields fluctuate; careful extraction.", "परिवर्तनशील खनिज। रत्न और धातु पैदावार में उतार-चढ़ाव; सावधान निष्कर्षण।"),
    ("Nirasadhipati", "Mars"): ("Mining losses. Ore losses & mining accidents; extraction hazards.", "खनन की हानि। अयस्क हानि और खनन दुर्घटनाएं; निष्कर्षण खतरे।"),
    ("Nirasadhipati", "Mercury"): ("Mineral trade. Gem & metal commerce flourish; trade prosperity.", "खनिज व्यापार। रत्न और धातु व्यापार फलते-फूलते हैं; व्यापार समृद्धि।"),
    ("Nirasadhipati", "Jupiter"): ("Excellent mining. Abundant ores & gems; mining prosperity.", "उत्कृष्ट खनन। प्रचुर अयस्क और रत्न; खनन समृद्धि।"),
    ("Nirasadhipati", "Venus"): ("Quality gems. Fine stones & precious metals of high quality.", "गुणवत्तापूर्ण रत्न। बेहतरीन पत्थर और उच्च गुणवत्ता वाली कीमती धातु।"),
    ("Nirasadhipati", "Saturn"): ("Mineral scarcity. Mining losses & ore depletion; scarcity increases.", "खनिज की कमी। खनन हानि और अयस्क में कमी; कमी बढ़ता है।"),

    # Phaladhipati (Fruits Lord) — Fruits, flowers & produce
    ("Phaladhipati", "Sun"): ("Abundant fruits. Fruit crops flourish; sweet & ripe produce.", "प्रचुर फल। फलों की फसलें फलती-फूलती हैं; मीठे और पके फल।"),
    ("Phaladhipati", "Moon"): ("Variable fruits. Fruit yields fluctuate; moisture affects quality.", "परिवर्तनशील फल। फलों की पैदावार में उतार-चढ़ाव; नमी गुणवत्ता को प्रभावित करती है।"),
    ("Phaladhipati", "Mars"): ("Fruit damage. Pests, rot & loss; fruit crops damaged.", "फल को नुकसान। कीट, सड़न और नुकसान; फलों की फसलें क्षतिग्रस्त।"),
    ("Phaladhipati", "Mercury"): ("Good fruit trade. Fruit commerce & produce markets flourish.", "अच्छा फल व्यापार। फल व्यापार और उपज बाजार फलते-फूलते हैं।"),
    ("Phaladhipati", "Jupiter"): ("Excellent fruits. Abundant harvests & quality produce; prosperity.", "उत्कृष्ट फल। प्रचुर फसलें और गुणवत्तापूर्ण उपज; समृद्धि।"),
    ("Phaladhipati", "Venus"): ("Beautiful fruits. Fine flowers & fragrant produce; beauty & fragrance.", "सुंदर फल। सुंदर फूल और सुगंधित उपज; सौंदर्य और सुगंध।"),
    ("Phaladhipati", "Saturn"): ("Poor fruits. Crop failure, rot & scarcity; losses likely.", "खराब फल। फसल की विफलता, सड़न और कमी; नुकसान संभव।"),
}


def calculate_mantri_mandala(vikram_samvat_year: int) -> List[Dict[str, str]]:
    """
    Return the 10-member planetary cabinet for *vikram_samvat_year*.

    Each entry: {"role", "role_hindi", "planet", "planet_hindi", "significance", "significance_hindi"}.

    The Raja (King) planet is looked up from SAMVAT_RAJA.  If the year
    is unknown, a modulo-7 fallback on GRAHA_ORDER is used so we always
    return a result.
    """
    raja_planet = SAMVAT_RAJA.get(vikram_samvat_year)
    if raja_planet is None:
        # Fallback: cycle through GRAHA_ORDER based on year
        raja_planet = GRAHA_ORDER[vikram_samvat_year % 7]

    raja_idx = GRAHA_ORDER.index(raja_planet)

    result: List[Dict[str, str]] = []
    for i, (role_en, role_hi) in enumerate(MANDALA_ROLES):
        planet = GRAHA_ORDER[(raja_idx + i) % len(GRAHA_ORDER)]
        sig_en, sig_hi = MANTRI_SIGNIFICANCE.get((role_en, planet), ("", ""))
        result.append({
            "role": role_en,
            "role_hindi": role_hi,
            "planet": planet,
            "planet_hindi": PLANET_NAMES[planet],
            "significance": sig_en,
            "significance_hindi": sig_hi,
        })
    return result


# ============================================================
# KALIYUGA & ASTRONOMICAL EPOCH DATA
# ============================================================
# Kaliyuga epoch: 3102 BCE (Feb 17/18), Julian Day 588465.5.
# Kali year = Gregorian year + 3101 (simplified; before April use +3101).

KALI_EPOCH_JD: float = 588465.5  # JD of Kaliyuga start
RATA_DIE_OFFSET: float = 1721424.5
MJD_OFFSET: float = 2400000.5


def calculate_astronomical_data(
    date_str: str,
    jd: Optional[float] = None,
    ayanamsha: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Compute astronomical epoch values for a Gregorian date string (YYYY-MM-DD).

    Returns dict with:
      kaliyuga_year, kali_ahargana, rata_die, julian_day,
      modified_julian_day, ayanamsha — each with English & Hindi labels.
    """
    year, month, day = map(int, date_str.split("-"))

    # Kaliyuga year (simplified)
    kali_year = year + 3101

    # Kali Ahargana: days elapsed since Kaliyuga start
    kali_ahargana = int(jd - KALI_EPOCH_JD) if jd else 0

    # Rata Die: days elapsed since epoch of the proleptic Gregorian calendar
    rata_die = int(jd - RATA_DIE_OFFSET) if jd else 0

    # Modified Julian Day
    mjd = int(jd - MJD_OFFSET) if jd else 0

    return {
        "kaliyuga_year": kali_year,
        "kaliyuga_year_label": f"{kali_year} Years",
        "kaliyuga_year_label_hindi": f"{kali_year} वर्ष",
        "kali_ahargana": kali_ahargana,
        "kali_ahargana_label": f"{kali_ahargana} Days",
        "kali_ahargana_label_hindi": f"{kali_ahargana} दिन",
        "rata_die": rata_die,
        "rata_die_label": f"{rata_die} Days",
        "rata_die_label_hindi": f"{rata_die} दिन",
        "julian_day": round(jd, 1) if jd else 0,
        "julian_day_label": f"JD {round(jd, 1)}" if jd else "",
        "julian_day_label_hindi": f"जूलियन दिन {round(jd, 1)}" if jd else "",
        "modified_julian_day": mjd,
        "modified_julian_day_label": f"MJD {mjd}" if jd else "",
        "modified_julian_day_label_hindi": f"एमजेडी {mjd}" if jd else "",
        "ayanamsha": round(ayanamsha, 6) if ayanamsha else 0,
        "ayanamsha_label": f"Lahiri {round(ayanamsha, 6)}\u00b0" if ayanamsha else "",
        "ayanamsha_label_hindi": f"लाहिरी {round(ayanamsha, 6)}\u00b0" if ayanamsha else "",
    }


# ============================================================
# PANCHAKA RAHITA MUHURTA (पंचक रहित मुहूर्त)
# ============================================================
# Panchaka occurs when Moon transits through the last 5 nakshatras
# (Dhanishta, Shatabhisha, Purva Bhadrapada, Uttara Bhadrapada, Revati).
# Each of those nakshatras maps to a specific Panchaka type.

PANCHAKA_NAKSHATRAS: Dict[str, tuple[str, str, bool]] = {
    "Dhanishta":          ("Mrityu Panchaka",  "मृत्यु पंचक",  False),   # death risk
    "Shatabhisha":        ("Agni Panchaka",    "अग्नि पंचक",   False),   # fire risk
    "Purva Bhadrapada":   ("Raja Panchaka",    "राज पंचक",      True),    # govt ok
    "Uttara Bhadrapada":  ("Chora Panchaka",   "चोर पंचक",      False),   # theft risk
    "Revati":             ("Roga Panchaka",    "रोग पंचक",      False),   # disease risk
}

# Also allow variant spellings commonly seen in panchang data
_NAKSHATRA_ALIASES: Dict[str, str] = {
    "Dhanista":              "Dhanishta",
    "Satabhisha":            "Shatabhisha",
    "Satabisha":             "Shatabhisha",
    "Poorva Bhadrapada":     "Purva Bhadrapada",
    "Uttara Bhadra":         "Uttara Bhadrapada",
    "Uttarabhadrapada":      "Uttara Bhadrapada",
}


def _resolve_nakshatra(name: str) -> str:
    """Normalise common nakshatra spelling variants."""
    stripped = name.strip()
    return _NAKSHATRA_ALIASES.get(stripped, stripped)


def _time_to_minutes(t: str) -> int:
    """Convert 'HH:MM' to minutes since midnight."""
    parts = t.strip().split(":")
    return int(parts[0]) * 60 + int(parts[1])


def _minutes_to_time(m: int) -> str:
    """Convert minutes since midnight to 'HH:MM'."""
    h = m // 60
    mm = m % 60
    return f"{h:02d}:{mm:02d}"


def calculate_panchaka_rahita(
    nakshatra_name: str,
    nakshatra_end_time: str,
    sunrise: str,
    sunset: str,
) -> Optional[Dict[str, Any]]:
    """
    Determine whether Panchaka is active and return safe/unsafe windows.

    Returns ``None`` if the nakshatra does not trigger Panchaka.

    When Panchaka *is* active, returns::

        {
            "active": True,
            "type": "Mrityu Panchaka",
            "type_hindi": "मृत्यु पंचक",
            "safe_for_govt": False,
            "unsafe_window": {"start": "06:10", "end": "14:30"},
            "unsafe_window_label": "06:10 – 14:30",
            "unsafe_window_label_hindi": "06:10 – 14:30 (अशुभ)",
            "safe_window": {"start": "14:30", "end": "18:30"},
            "safe_window_label": "14:30 – 18:30",
            "safe_window_label_hindi": "14:30 – 18:30 (शुभ)",
        }
    """
    resolved = _resolve_nakshatra(nakshatra_name)

    if resolved not in PANCHAKA_NAKSHATRAS:
        return None

    type_en, type_hi, safe_for_govt = PANCHAKA_NAKSHATRAS[resolved]

    sr = _time_to_minutes(sunrise)
    ss = _time_to_minutes(sunset)
    end = _time_to_minutes(nakshatra_end_time)

    # Panchaka is active from sunrise until the nakshatra ends.
    # Safe window is from nakshatra end until sunset (if end < sunset).
    if end <= sr:
        # Nakshatra ends before sunrise — no panchaka during the day
        return None

    unsafe_start = max(sr, sr)  # starts at sunrise
    unsafe_end = min(end, ss)   # until nakshatra ends or sunset

    safe_start = unsafe_end
    safe_end = ss

    # If no safe window remains (nakshatra extends past sunset)
    has_safe = safe_start < safe_end

    result: Dict[str, Any] = {
        "active": True,
        "type": type_en,
        "type_hindi": type_hi,
        "safe_for_govt": safe_for_govt,
        "unsafe_window": {
            "start": _minutes_to_time(unsafe_start),
            "end": _minutes_to_time(unsafe_end),
        },
        "unsafe_window_label": (
            f"{_minutes_to_time(unsafe_start)} – {_minutes_to_time(unsafe_end)}"
        ),
        "unsafe_window_label_hindi": (
            f"{_minutes_to_time(unsafe_start)} – {_minutes_to_time(unsafe_end)} (अशुभ)"
        ),
    }

    if has_safe:
        result["safe_window"] = {
            "start": _minutes_to_time(safe_start),
            "end": _minutes_to_time(safe_end),
        }
        result["safe_window_label"] = (
            f"{_minutes_to_time(safe_start)} – {_minutes_to_time(safe_end)}"
        )
        result["safe_window_label_hindi"] = (
            f"{_minutes_to_time(safe_start)} – {_minutes_to_time(safe_end)} (शुभ)"
        )
    else:
        result["safe_window"] = None
        result["safe_window_label"] = "No safe window / कोई शुभ समय नहीं"
        result["safe_window_label_hindi"] = "कोई शुभ समय नहीं"

    return result


# ============================================================
# CHATURMASA (चातुर्मास)
# ============================================================

_CHATURMASA_FULL_MONTHS = {"Shravana", "Bhadrapada", "Ashwin"}


def calculate_chaturmasa(hindu_month: str, tithi_index: int, paksha: str) -> Dict[str, Any]:
    """
    Determine whether the given Hindu date falls within Chaturmasa.

    Chaturmasa runs from Ashadh Shukla Ekadashi (tithi_index 10 in 0-based)
    to Kartik Shukla Ekadashi.
    """
    active = False
    if hindu_month in _CHATURMASA_FULL_MONTHS:
        active = True
    elif hindu_month == "Ashadh":
        if paksha == "Shukla" and tithi_index >= 10:  # Ekadashi onward
            active = True
    elif hindu_month == "Kartik":
        if paksha == "Krishna":
            active = True
        elif paksha == "Shukla" and tithi_index < 10:  # Before Ekadashi
            active = True

    return {
        "active": active,
        "period": "Chaturmasa",
        "period_hindi": "चातुर्मास",
        "warning": "Major ceremonies prohibited during Chaturmasa",
        "warning_hindi": "चातुर्मास में बड़े संस्कार वर्जित हैं",
        "start_month": "Ashadh",
        "end_month": "Kartik",
    }


# ============================================================
# MASTER FUNCTION
# ============================================================

def calculate_all_misc(
    date_str: str,
    vikram_samvat: int,
    jd: Optional[float] = None,
    ayanamsha: Optional[float] = None,
    nakshatra_name: str = "",
    nakshatra_end_time: str = "",
    sunrise: str = "",
    sunset: str = "",
) -> Dict[str, Any]:
    """
    Aggregate all miscellaneous panchang calculations.

    Returns dict with keys:
      - mantri_mandala  (list of 10 role dicts)
      - astronomical    (epoch data dict)
      - panchaka_rahita (dict or None)
    """
    mantri = calculate_mantri_mandala(vikram_samvat)

    astro = calculate_astronomical_data(date_str, jd=jd, ayanamsha=ayanamsha)

    panchaka: Optional[Dict[str, Any]] = None
    if nakshatra_name and nakshatra_end_time and sunrise and sunset:
        panchaka = calculate_panchaka_rahita(
            nakshatra_name, nakshatra_end_time, sunrise, sunset,
        )

    return {
        "mantri_mandala": mantri,
        "astronomical": astro,
        "panchaka_rahita": panchaka,
    }
