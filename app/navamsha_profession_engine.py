"""
navamsha_profession_engine.py — Profession from 10th Navamsha Lord
==================================================================
Implements Phaladeepika Adhyaya 5: the 10th house of the Navamsha (D9) chart
reveals the deeper, dharmic dimension of one's vocation. The lord of D9's 10th
house shows the career's spiritual or vocational nature.

Classical D9 calculation:
  - Divide each zodiac sign into 9 navamshas of 3°20' each.
  - Starting sign by element:
      Fire (Aries, Leo, Sagittarius)    → Aries (index 0)
      Earth (Taurus, Virgo, Capricorn)  → Capricorn (index 9)
      Air (Gemini, Libra, Aquarius)     → Libra (index 6)
      Water (Cancer, Scorpio, Pisces)   → Cancer (index 3)
  - D9 sign = (base_index + part_offset) mod 12

Public API:
  analyze_navamsha_profession(planet_longitudes: dict) -> dict
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

_SIGN_NAMES: List[str] = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

_SIGN_NAMES_HI: List[str] = [
    "मेष", "वृष", "मिथुन", "कर्क", "सिंह", "कन्या",
    "तुला", "वृश्चिक", "धनु", "मकर", "कुम्भ", "मीन",
]

_SIGN_LORD: Dict[str, str] = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

_PLANET_VRITTI: Dict[str, Dict[str, Any]] = {
    "Sun": {
        "type_en": "Governance, medicine, and spiritual authority",
        "type_hi": "शासन, चिकित्सा तथा आध्यात्मिक प्राधिकार",
        "detail_en": (
            "Sun as the 10th Navamsha lord indicates a calling toward leadership roles, "
            "government service, medicine, administration, or positions of authority. "
            "The career carries solar qualities: clarity, responsibility and public recognition."
        ),
        "detail_hi": (
            "सूर्य का दशम नवांश-लॉर्ड होना नेतृत्व, सरकारी सेवा, चिकित्सा, प्रशासन अथवा "
            "अधिकार-पदों की ओर बुलाहट दर्शाता है। जीविका में सौर गुण — स्पष्टता, उत्तरदायित्व "
            "और सार्वजनिक पहचान — झलकते हैं।"
        ),
        "examples_en": [
            "Government officer", "Physician", "Administrator",
            "Priest / temple head", "Goldsmith", "Metallurgist",
        ],
        "examples_hi": [
            "सरकारी अधिकारी", "चिकित्सक", "प्रशासक",
            "पुरोहित / मन्दिर प्रमुख", "स्वर्णकार", "धातुविद्",
        ],
    },
    "Moon": {
        "type_en": "Trade, nurturing professions, and water-related livelihood",
        "type_hi": "व्यापार, पोषण-वृत्ति तथा जल-सम्बन्धी आजीविका",
        "detail_en": (
            "Moon as the 10th Navamsha lord points to careers connected with water, travel, "
            "trade in perishables, textiles or dairy, or nurturing professions such as nursing "
            "and hospitality. There is an emotional and empathetic quality to the dharmic vocation."
        ),
        "detail_hi": (
            "चन्द्रमा का दशम नवांश-लॉर्ड होना जल, यात्रा, नाशवान वस्तुओं के व्यापार, वस्त्र, "
            "डेयरी अथवा परिचर्या और आतिथ्य से जुड़ी वृत्ति दर्शाता है। धार्मिक कार्य में "
            "भावनात्मक और सहानुभूतिपूर्ण गुण रहते हैं।"
        ),
        "examples_en": [
            "Sailor / sea-trader", "Textile merchant", "Farmer",
            "Nurse / midwife", "Hospitality professional", "Pearl dealer",
        ],
        "examples_hi": [
            "नाविक / समुद्री व्यापारी", "वस्त्र व्यापारी", "कृषक",
            "परिचारिका / दाई", "आतिथ्य-कर्मी", "मोती विक्रेता",
        ],
    },
    "Mars": {
        "type_en": "Military, surgery, engineering, and competitive endeavors",
        "type_hi": "सैन्य, शल्य-चिकित्सा, अभियान्त्रिकी तथा प्रतिस्पर्धी क्षेत्र",
        "detail_en": (
            "Mars as the 10th Navamsha lord indicates a career marked by courage, physical "
            "energy, and decisiveness. Military service, surgery, sports, engineering, police "
            "or any field demanding swift action and bold initiative are naturally favored."
        ),
        "detail_hi": (
            "मंगल का दशम नवांश-लॉर्ड होना साहस, शारीरिक ऊर्जा और निर्णायकता से युक्त जीविका "
            "दर्शाता है। सैन्य सेवा, शल्य-चिकित्सा, खेल, अभियान्त्रिकी, पुलिस या किसी भी ऐसे "
            "क्षेत्र में स्वाभाविक योग्यता होती है जहाँ त्वरित कार्य और साहसी पहल अपेक्षित हो।"
        ),
        "examples_en": [
            "Soldier", "Surgeon", "Police officer",
            "Athlete / sportsperson", "Engineer", "Chef", "Blacksmith",
        ],
        "examples_hi": [
            "सैनिक", "शल्य चिकित्सक", "पुलिस अधिकारी",
            "खिलाड़ी", "अभियन्ता", "पाचक / रसोइया", "लुहार",
        ],
    },
    "Mercury": {
        "type_en": "Scholarship, writing, commerce, and communication",
        "type_hi": "विद्वत्ता, लेखन, वाणिज्य तथा संचार",
        "detail_en": (
            "Mercury as the 10th Navamsha lord brings a vocation grounded in intellect, "
            "communication, and commerce. Careers in writing, scholarship, accounting, "
            "teaching, translation, trading or any field requiring mental agility and "
            "skillful speech are classically indicated."
        ),
        "detail_hi": (
            "बुध का दशम नवांश-लॉर्ड होना बुद्धि, संचार और वाणिज्य पर आधारित वृत्ति दर्शाता है। "
            "लेखन, विद्वत्ता, लेखाकर्म, अध्यापन, अनुवाद, व्यापार या किसी भी ऐसे क्षेत्र में "
            "वृत्ति का संकेत होता है जहाँ मानसिक चपलता और कुशल वाक्-कौशल आवश्यक हो।"
        ),
        "examples_en": [
            "Poet / writer", "Scholar", "Accountant / auditor",
            "Teacher", "Translator / interpreter", "Trader / broker", "Editor",
        ],
        "examples_hi": [
            "कवि / लेखक", "विद्वान्", "लेखाकार / लेखापरीक्षक",
            "अध्यापक", "अनुवादक / दुभाषिया", "व्यापारी / दलाल", "सम्पादक",
        ],
    },
    "Jupiter": {
        "type_en": "Priestly service, law, counseling, and teaching of dharma",
        "type_hi": "पौरोहित्य, विधि, परामर्श तथा धर्म-शिक्षा",
        "detail_en": (
            "Jupiter as the 10th Navamsha lord is a powerful indicator of a career in "
            "spiritual, educational or advisory service. Priestly duties, Vedic scholarship, "
            "law, counseling, philosophy, banking, and roles that involve guiding others "
            "according to dharmic principles are strongly favored."
        ),
        "detail_hi": (
            "बृहस्पति का दशम नवांश-लॉर्ड होना आध्यात्मिक, शैक्षणिक या सलाहकार सेवा में वृत्ति "
            "का प्रबल संकेत है। पौरोहित्य, वैदिक विद्वत्ता, विधि, परामर्श, दर्शन, बैंकिंग तथा "
            "धार्मिक सिद्धान्तों के अनुसार दूसरों को मार्गदर्शन देने वाली भूमिकाएँ विशेष अनुकूल होती हैं।"
        ),
        "examples_en": [
            "Purohita / priest", "Vedic scholar", "Judge / lawyer",
            "Counsellor / therapist", "Banker", "Philosopher",
            "Teacher of dharma / ethics",
        ],
        "examples_hi": [
            "पुरोहित", "वैदिक विद्वान्", "न्यायाधीश / अधिवक्ता",
            "परामर्शदाता", "बैंकर", "दार्शनिक", "धर्मोपदेशक / नैतिकता शिक्षक",
        ],
    },
    "Venus": {
        "type_en": "Arts, beauty, luxury goods, music, and creative expression",
        "type_hi": "कला, सौन्दर्य, विलास-वस्तुएँ, संगीत तथा सृजनात्मक अभिव्यक्ति",
        "detail_en": (
            "Venus as the 10th Navamsha lord bestows a vocation infused with beauty, pleasure, "
            "and creative talent. Music, dance, fine arts, fashion, jewellery, silk, cosmetics, "
            "entertainment, and all luxury-oriented trades are indicated. The dharmic career "
            "brings joy and aesthetic refinement."
        ),
        "detail_hi": (
            "शुक्र का दशम नवांश-लॉर्ड होना सौन्दर्य, आनन्द और सृजनात्मक प्रतिभा से युक्त वृत्ति "
            "प्रदान करता है। संगीत, नृत्य, ललित कलाएँ, फैशन, आभूषण, रेशम, प्रसाधन, मनोरंजन तथा "
            "सभी विलास-उन्मुख व्यापारों का संकेत है। धार्मिक वृत्ति में आनन्द और सौन्दर्य-परिष्कार झलकता है।"
        ),
        "examples_en": [
            "Musician / singer", "Dancer / choreographer", "Jeweller",
            "Fashion designer", "Cosmetician / beautician",
            "Actor / entertainer", "Silk / luxury goods merchant",
        ],
        "examples_hi": [
            "संगीतकार / गायक", "नर्तक / कोरियोग्राफर", "आभूषण-निर्माता",
            "फैशन डिज़ाइनर", "प्रसाधनकार",
            "अभिनेता / मनोरंजनकर्ता", "रेशम / विलास-वस्तु व्यापारी",
        ],
    },
    "Saturn": {
        "type_en": "Labor, industry, land, mining, and disciplined service",
        "type_hi": "श्रम, उद्योग, भूमि, खनन तथा अनुशासित सेवा",
        "detail_en": (
            "Saturn as the 10th Navamsha lord brings a career shaped by discipline, hard work, "
            "and service over long durations. Mining, construction, iron and coal trade, oil, "
            "waste management, land administration, or any occupation requiring endurance and "
            "systematic effort are classically indicated. Success comes through persistent, "
            "dutiful labor."
        ),
        "detail_hi": (
            "शनि का दशम नवांश-लॉर्ड होना अनुशासन, परिश्रम और दीर्घकालीन सेवा से गढ़ी वृत्ति "
            "दर्शाता है। खनन, निर्माण, लोहा और कोयले का व्यापार, तेल, अपशिष्ट-प्रबन्धन, भूमि "
            "प्रशासन अथवा किसी भी ऐसे कार्य का संकेत है जिसमें धैर्य और व्यवस्थित प्रयास "
            "अपेक्षित हो। निरन्तर, कर्तव्यनिष्ठ श्रम से सफलता मिलती है।"
        ),
        "examples_en": [
            "Miner / coal worker", "Construction worker", "Iron / steel worker",
            "Oil / fuel dealer", "Land / property administrator",
            "Sanitation / waste management professional", "Low-level civil servant",
        ],
        "examples_hi": [
            "खनिक / कोयला-कर्मी", "निर्माण कर्मी", "लोहा / इस्पात कर्मी",
            "तेल / ईंधन व्यापारी", "भूमि / सम्पत्ति प्रशासक",
            "सफाई / अपशिष्ट-प्रबन्धन कर्मी", "निम्न सरकारी सेवक",
        ],
    },
    "Rahu": {
        "type_en": "Foreign trade, technology, unconventional and boundary-breaking careers",
        "type_hi": "विदेश-व्यापार, प्रौद्योगिकी, अपारम्परिक तथा सीमा-तोड़ने वाली वृत्तियाँ",
        "detail_en": (
            "Rahu as the 10th Navamsha lord indicates a career that defies convention and reaches "
            "beyond familiar boundaries. Technology, foreign commerce, research in hidden or "
            "cutting-edge subjects, aviation, media, and cyber-related fields are strongly "
            "suggested. The dharmic path involves innovation and crossing established limits."
        ),
        "detail_hi": (
            "राहु का दशम नवांश-लॉर्ड होना परम्परा को चुनौती देने और परिचित सीमाओं से परे जाने "
            "वाली वृत्ति का संकेत देता है। प्रौद्योगिकी, विदेश-व्यापार, गुप्त या अत्याधुनिक "
            "विषयों में अनुसन्धान, विमानन, मीडिया और साइबर-क्षेत्र प्रबल संकेत हैं। धार्मिक "
            "मार्ग में नवाचार और स्थापित सीमाओं को पार करना शामिल है।"
        ),
        "examples_en": [
            "Software engineer", "Data scientist", "Foreign trader",
            "Aviator / aerospace", "Cyber-security expert",
            "Media / film professional", "Researcher (fringe sciences)",
        ],
        "examples_hi": [
            "सॉफ्टवेयर अभियन्ता", "डेटा वैज्ञानिक", "विदेश व्यापारी",
            "विमान चालक / एयरोस्पेस", "साइबर सुरक्षा विशेषज्ञ",
            "मीडिया / चलचित्र कर्मी", "अनुसन्धानकर्ता (सीमान्त विज्ञान)",
        ],
    },
    "Ketu": {
        "type_en": "Spiritual teaching, occult research, healing, and renunciation",
        "type_hi": "आध्यात्मिक शिक्षण, रहस्य-विद्या, चिकित्सा तथा वैराग्य",
        "detail_en": (
            "Ketu as the 10th Navamsha lord bestows a career oriented toward liberation and "
            "hidden knowledge. Astrology, spiritual teaching, Ayurvedic or herbal healing, "
            "tantric arts, monastic life, and research into ancient or metaphysical subjects "
            "are indicated. The vocation demands detachment and inward depth."
        ),
        "detail_hi": (
            "केतु का दशम नवांश-लॉर्ड होना मुक्ति और गुप्त ज्ञान की ओर उन्मुख वृत्ति प्रदान "
            "करता है। ज्योतिष, आध्यात्मिक शिक्षण, आयुर्वेद या जड़ी-बूटी चिकित्सा, तान्त्रिक "
            "कलाएँ, मठ-जीवन और प्राचीन या आधिभौतिक विषयों में अनुसन्धान के संकेत हैं। वृत्ति "
            "में वैराग्य और आन्तरिक गहराई अपेक्षित है।"
        ),
        "examples_en": [
            "Astrologer", "Spiritual teacher / guru", "Ayurveda doctor",
            "Tantric practitioner", "Monastic / yogi",
            "Herbalist", "Metaphysical researcher",
        ],
        "examples_hi": [
            "ज्योतिषी", "आध्यात्मिक शिक्षक / गुरु", "आयुर्वेद चिकित्सक",
            "तान्त्रिक साधक", "संन्यासी / योगी",
            "वैद्य / जड़ी-बूटी विशेषज्ञ", "आधिभौतिक अनुसन्धानकर्ता",
        ],
    },
}

_PLANET_IN_SIGN_SUPPORT: Dict[str, str] = {
    "Sun": "Sun in this D9 sign adds solar authority and clarity to the career expression.",
    "Moon": "Moon in this D9 sign brings emotional attunement and adaptability to the vocation.",
    "Mars": "Mars in this D9 sign adds drive, courage, and competitive energy to the profession.",
    "Mercury": "Mercury in this D9 sign enhances intellectual precision and communication in the career.",
    "Jupiter": "Jupiter in this D9 sign expands wisdom, ethics, and prosperity in the vocation.",
    "Venus": "Venus in this D9 sign brings aesthetic refinement and harmonious expression to the career.",
    "Saturn": "Saturn in this D9 sign adds discipline, perseverance, and karmic depth to the work.",
    "Rahu": "Rahu in this D9 sign introduces innovative, unconventional energy to the career.",
    "Ketu": "Ketu in this D9 sign brings spiritual depth and detachment to the professional path.",
}

# D9 element-start mapping: sign index → base D9 index
_D9_BASE: Dict[int, int] = {
    0: 0,   # Aries   (Fire)  → Aries     (0)
    4: 0,   # Leo     (Fire)  → Aries     (0)
    8: 0,   # Sagittarius (Fire) → Aries  (0)
    1: 9,   # Taurus  (Earth) → Capricorn (9)
    5: 9,   # Virgo   (Earth) → Capricorn (9)
    9: 9,   # Capricorn (Earth) → Capricorn (9)
    2: 6,   # Gemini  (Air)   → Libra     (6)
    6: 6,   # Libra   (Air)   → Libra     (6)
    10: 6,  # Aquarius (Air)  → Libra     (6)
    3: 3,   # Cancer  (Water) → Cancer    (3)
    7: 3,   # Scorpio (Water) → Cancer    (3)
    11: 3,  # Pisces  (Water) → Cancer    (3)
}


def _sign_index(sign: str) -> int:
    """Return 0-indexed sign position, -1 if unknown."""
    try:
        return _SIGN_NAMES.index(sign)
    except ValueError:
        return -1


def _navamsha_sign_for_longitude(longitude: float) -> str:
    """Compute the Navamsha (D9) sign for a planet's sidereal longitude.

    Partition sizes:
      Each sign (30°) divided into 9 parts of 3°20' (= 30/9 degrees).
    Starting sign by element of the rasi:
      Fire  (0,4,8  = Aries, Leo, Sagittarius)    → Aries     (index 0)
      Earth (1,5,9  = Taurus, Virgo, Capricorn)   → Capricorn (index 9)
      Air   (2,6,10 = Gemini, Libra, Aquarius)    → Libra     (index 6)
      Water (3,7,11 = Cancer, Scorpio, Pisces)    → Cancer    (index 3)
    """
    lon = float(longitude) % 360.0
    rasi_index = int(lon // 30)
    deg_in_rasi = lon - rasi_index * 30.0
    part_size = 30.0 / 9.0  # 3°20'
    part_offset = int(deg_in_rasi / part_size)
    base = _D9_BASE.get(rasi_index, 0)
    d9_index = (base + part_offset) % 12
    return _SIGN_NAMES[d9_index]


def _d9_sign_for_all(planet_longitudes: Dict[str, float]) -> Dict[str, str]:
    """Compute D9 sign for each planet in the supplied longitude dict."""
    return {
        planet: _navamsha_sign_for_longitude(lon)
        for planet, lon in planet_longitudes.items()
    }


def _d9_tenth_house(d9_lagna: str) -> str:
    """Return the sign of the 10th house in the D9 chart using whole-sign system.
    The 10th house is 9 signs forward from the D9 Lagna (0-indexed offset = 9).
    """
    idx = _sign_index(d9_lagna)
    if idx == -1:
        return d9_lagna
    return _SIGN_NAMES[(idx + 9) % 12]


def _find_planet_in_d9(d9_signs: Dict[str, str], target_sign: str) -> List[str]:
    """Return list of planets whose D9 sign equals target_sign."""
    return [
        p for p, s in d9_signs.items()
        if s == target_sign and p != "Ascendant"
    ]


def analyze_navamsha_profession(planet_longitudes: Dict[str, float]) -> Dict[str, Any]:
    """Profession from the 10th Navamsha lord per Phaladeepika Adh. 5.

    Args:
        planet_longitudes: dict of planet_name -> sidereal longitude (0-360°),
            MUST include 'Ascendant'.
            Standard planet keys: 'Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter',
            'Venus', 'Saturn', 'Rahu', 'Ketu', 'Ascendant'

    Returns:
        {
            "d9_lagna": "...",           # D9 Lagna sign
            "d9_lagna_hi": "...",        # Hindi
            "d9_10th_house_sign": "...", # sign of D9 10th house
            "d9_10th_house_sign_hi": "...",
            "d9_10th_lord": "...",       # lord of that sign
            "d9_10th_lord_sign": "...",  # where that lord sits in D9
            "d9_10th_lord_sign_hi": "...",
            "profession_type_en": "...",
            "profession_type_hi": "...",
            "detailed_interpretation_en": "...",
            "detailed_interpretation_hi": "...",
            "supporting_planets_en": "...",
            "supporting_planets_hi": "...",
            "career_examples_en": [...],
            "career_examples_hi": [...],
            "sloka_ref": "Phaladeepika Adh. 5"
        }
    """
    d9_signs = _d9_sign_for_all(planet_longitudes)

    asc_lon = planet_longitudes.get("Ascendant", planet_longitudes.get("ascendant", 0.0))
    d9_lagna = _navamsha_sign_for_longitude(asc_lon)
    d9_lagna_idx = _sign_index(d9_lagna)
    d9_lagna_hi = _SIGN_NAMES_HI[d9_lagna_idx] if d9_lagna_idx >= 0 else d9_lagna

    d9_10th_sign = _d9_tenth_house(d9_lagna)
    d9_10th_idx = _sign_index(d9_10th_sign)
    d9_10th_sign_hi = _SIGN_NAMES_HI[d9_10th_idx] if d9_10th_idx >= 0 else d9_10th_sign

    d9_10th_lord = _SIGN_LORD.get(d9_10th_sign, "")
    d9_10th_lord_sign = d9_signs.get(d9_10th_lord, "")
    d9_10th_lord_sign_idx = _sign_index(d9_10th_lord_sign)
    d9_10th_lord_sign_hi = (
        _SIGN_NAMES_HI[d9_10th_lord_sign_idx]
        if d9_10th_lord_sign_idx >= 0
        else d9_10th_lord_sign
    )

    vritti = _PLANET_VRITTI.get(d9_10th_lord, {})
    profession_type_en = vritti.get("type_en", "")
    profession_type_hi = vritti.get("type_hi", "")
    career_examples_en = vritti.get("examples_en", [])
    career_examples_hi = vritti.get("examples_hi", [])

    interp_prefix_en = (
        f"The 10th house of your Navamsha (D9) is {d9_10th_sign}, ruled by "
        f"{d9_10th_lord}, placed in {d9_10th_lord_sign} in D9. "
    )
    interp_prefix_hi = (
        f"आपके नवांश (D9) का दशम भाव {d9_10th_sign_hi} है, जिसका स्वामी "
        f"{d9_10th_lord} है, जो D9 में {d9_10th_lord_sign_hi} में स्थित है। "
    )
    detailed_en = interp_prefix_en + vritti.get("detail_en", "")
    detailed_hi = interp_prefix_hi + vritti.get("detail_hi", "")

    # Supporting planets in D9 10th house sign
    co_occupants = _find_planet_in_d9(d9_signs, d9_10th_sign)
    if d9_10th_lord in co_occupants:
        co_occupants.remove(d9_10th_lord)

    support_parts_en: List[str] = []
    support_parts_hi: List[str] = []
    for p in co_occupants:
        support_en = _PLANET_IN_SIGN_SUPPORT.get(
            p, f"{p} in D9 {d9_10th_sign} adds its natural qualities to your career."
        )
        support_hi = f"{p} का D9 के {d9_10th_sign_hi} में स्थित होना आपकी वृत्ति में अपने स्वाभाविक गुण जोड़ता है।"
        support_parts_en.append(support_en)
        support_parts_hi.append(support_hi)

    if support_parts_en:
        supporting_planets_en = " ".join(support_parts_en)
        supporting_planets_hi = " ".join(support_parts_hi)
    else:
        supporting_planets_en = (
            f"No additional planets occupy the D9 10th house ({d9_10th_sign}); "
            f"the {d9_10th_lord}'s indication stands alone."
        )
        supporting_planets_hi = (
            f"D9 के दशम भाव ({d9_10th_sign_hi}) में कोई अन्य ग्रह नहीं; "
            f"{d9_10th_lord} का संकेत अकेला ही प्रभावी है।"
        )

    return {
        "d9_lagna": d9_lagna,
        "d9_lagna_hi": d9_lagna_hi,
        "d9_10th_house_sign": d9_10th_sign,
        "d9_10th_house_sign_hi": d9_10th_sign_hi,
        "d9_10th_lord": d9_10th_lord,
        "d9_10th_lord_sign": d9_10th_lord_sign,
        "d9_10th_lord_sign_hi": d9_10th_lord_sign_hi,
        "profession_type_en": profession_type_en,
        "profession_type_hi": profession_type_hi,
        "detailed_interpretation_en": detailed_en,
        "detailed_interpretation_hi": detailed_hi,
        "supporting_planets_en": supporting_planets_en,
        "supporting_planets_hi": supporting_planets_hi,
        "career_examples_en": career_examples_en,
        "career_examples_hi": career_examples_hi,
        "sloka_ref": "Phaladeepika Adh. 5",
    }
