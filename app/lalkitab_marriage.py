"""
lalkitab_marriage.py — Lal Kitab Marriage & Relationship Analysis
=================================================================
All predictions derived from actual chart planet positions.
Reference: Lal Kitab 1952 (Pt. Roop Chand Joshi).

In LK's fixed-house system: H7 = Libra = natural house of Venus and marriage.
"""
from __future__ import annotations
from typing import Any, Dict, List


# ── Planet effects when placed in H7 ─────────────────────────────────────────
# Derived from LK 1952 canonical rules for H7 placements.
_H7_PLANET_EFFECTS: Dict[str, Dict[str, Any]] = {
    "Sun": {
        "timing": "possible_but_ego_delays",
        "marriage_strength": 45,
        "partner_nature": {
            "en": "authoritative, career-driven, possibly dominating",
            "hi": "प्रभावशाली, करियर-केंद्रित, संभवतः प्रभुत्वशाली",
        },
        "challenge": {
            "en": "ego clashes and power struggles within marriage",
            "hi": "विवाह में अहंकार-टकराव और शक्ति-संघर्ष",
        },
        "advice": {
            "en": "avoid control; give partner space and recognition; do Sun remedies on Sunday",
            "hi": "नियंत्रण से बचें; साथी को स्थान और मान दें; रविवार को सूर्य उपाय करें",
        },
    },
    "Moon": {
        "timing": "timely_emotional",
        "marriage_strength": 70,
        "partner_nature": {
            "en": "emotional, intuitive, caring, possibly moody",
            "hi": "भावनात्मक, सहज-ज्ञानी, देखभाल करने वाला, संभवतः मूडी",
        },
        "challenge": {
            "en": "emotional dependency and mood swings can strain the bond",
            "hi": "भावनात्मक निर्भरता और मनोदशा उतार-चढ़ाव बंधन में तनाव ला सकते हैं",
        },
        "advice": {
            "en": "nurture emotional stability; offer water on Monday; keep communication open",
            "hi": "भावनात्मक स्थिरता पोषित करें; सोमवार को जल अर्पित करें; संवाद खुला रखें",
        },
    },
    "Mars": {
        "timing": "early_but_turbulent",
        "marriage_strength": 40,
        "partner_nature": {
            "en": "energetic, independent, possibly aggressive",
            "hi": "ऊर्जावान, स्वतंत्र, संभवतः आक्रामक",
        },
        "challenge": {
            "en": "frequent arguments, property disputes, risk of separation if Mars is debilitated",
            "hi": "बार-बार विवाद, संपत्ति विवाद; मंगल नीच हो तो अलगाव का जोखिम",
        },
        "advice": {
            "en": "channel Mars energy into shared goals; avoid confrontation; do Mars remedies on Tuesday",
            "hi": "मंगल ऊर्जा को साझा लक्ष्यों में लगाएँ; टकराव से बचें; मंगलवार को मंगल उपाय करें",
        },
    },
    "Mercury": {
        "timing": "timely_intellectual",
        "marriage_strength": 65,
        "partner_nature": {
            "en": "intelligent, communicative, witty, business-minded",
            "hi": "बुद्धिमान, संवादी, विनोदी, व्यापार-केंद्रित",
        },
        "challenge": {
            "en": "over-analysis and indecisiveness can delay commitment",
            "hi": "अति-विश्लेषण और अनिर्णय प्रतिबद्धता में देरी कर सकते हैं",
        },
        "advice": {
            "en": "keep agreements in writing; build intellectual bonds; Mercury favors early communication",
            "hi": "समझौते लिखित में करें; बौद्धिक बंधन बनाएँ; बुध शुरुआती संवाद का पक्षधर है",
        },
    },
    "Jupiter": {
        "timing": "auspicious_blessed",
        "marriage_strength": 85,
        "partner_nature": {
            "en": "wise, educated, religious, prosperous background",
            "hi": "बुद्धिमान, शिक्षित, धार्मिक, समृद्ध पृष्ठभूमि",
        },
        "challenge": {
            "en": "partner may be overly philosophical or expansive in spending",
            "hi": "साथी अत्यधिक दार्शनिक या खर्चीला हो सकता है",
        },
        "advice": {
            "en": "Jupiter blesses marriage in H7; seek a partner of good values; respect in-laws",
            "hi": "H7 में गुरु विवाह को आशीर्वाद देता है; अच्छे मूल्यों वाला साथी खोजें; ससुराल का सम्मान करें",
        },
    },
    "Venus": {
        "timing": "very_auspicious_pakka_ghar",
        "marriage_strength": 92,
        "partner_nature": {
            "en": "beautiful, artistic, loving, refined taste",
            "hi": "सुंदर, कलात्मक, प्रेमी, परिष्कृत रुचि",
        },
        "challenge": {
            "en": "over-indulgence or unrealistic expectations in romance",
            "hi": "अति-भोग या रोमांस में अवास्तविक अपेक्षाएँ",
        },
        "advice": {
            "en": "Venus in H7 is Pakka Ghar — strongest placement for marriage; maintain devotion and beauty in the relationship",
            "hi": "H7 में शुक्र पक्का घर है — विवाह के लिए सबसे बलशाली स्थान; संबंध में भक्ति और सौंदर्य बनाए रखें",
        },
    },
    "Saturn": {
        "timing": "delayed_after_28_or_30",
        "marriage_strength": 38,
        "partner_nature": {
            "en": "mature, serious, disciplined, hardworking, possibly older",
            "hi": "परिपक्व, गंभीर, अनुशासित, परिश्रमी, संभवतः उम्रदराज़",
        },
        "challenge": {
            "en": "delayed marriage (typically after 28–30); karmic dues must be settled first",
            "hi": "विलंबित विवाह (सामान्यतः 28-30 के बाद); पहले कर्मिक ऋण चुकाने होंगे",
        },
        "advice": {
            "en": "do not rush marriage; Saturn in H7 demands patience and karmic readiness; do Saturday remedies",
            "hi": "विवाह में जल्दबाज़ी न करें; H7 में शनि धैर्य और कर्मिक तत्परता माँगता है; शनिवार उपाय करें",
        },
    },
    "Rahu": {
        "timing": "unconventional_or_foreign",
        "marriage_strength": 42,
        "partner_nature": {
            "en": "unconventional, possibly foreign or different background, ambitious",
            "hi": "अपरंपरागत, संभवतः विदेशी या अलग पृष्ठभूमि, महत्वाकांक्षी",
        },
        "challenge": {
            "en": "confusion or illusions in marriage; verify partner thoroughly before commitment",
            "hi": "विवाह में भ्रम या मायाजाल का खतरा; प्रतिबद्धता से पहले साथी की अच्छी तरह जाँच करें",
        },
        "advice": {
            "en": "Rahu in H7 gives unusual partnerships; stay grounded and clear-headed in love matters",
            "hi": "H7 में राहु असाधारण साझेदारी देता है; प्रेम मामलों में यथार्थवादी और स्पष्ट-बुद्धि रहें",
        },
    },
    "Ketu": {
        "timing": "spiritually_oriented_or_detached",
        "marriage_strength": 48,
        "partner_nature": {
            "en": "spiritually inclined, detached, philosophical, karmic connection",
            "hi": "आध्यात्मिक रूप से झुका हुआ, अनासक्त, दार्शनिक, कर्मिक संबंध",
        },
        "challenge": {
            "en": "emotional detachment; partner may seem distant or unworldly",
            "hi": "भावनात्मक अनासक्ति; साथी दूर या अव्यावहारिक लग सकता है",
        },
        "advice": {
            "en": "Ketu in H7 indicates a spiritually karmic relationship; honour the spiritual dimension of the bond",
            "hi": "H7 में केतु आध्यात्मिक कर्मिक संबंध दर्शाता है; बंधन के आध्यात्मिक आयाम का सम्मान करें",
        },
    },
}

# ── Venus dignity → marriage strength modifier ───────────────────────────────
_VENUS_DIGNITY_MODIFIER: Dict[str, int] = {
    "exalted": 25, "own": 20, "friend": 10,
    "neutral": 0, "enemy": -10, "debilitated": -20,
}

# ── Saturn house → delay description ─────────────────────────────────────────
_SATURN_DELAY: Dict[int, Dict[str, str]] = {
    1:  {"en": "Saturn in H1 delays self-confidence in marriage decisions",
         "hi": "H1 में शनि विवाह निर णयों में आत्मविश्वास को विलंबित करता है"},
    2:  {"en": "Saturn in H2 restricts family support for marriage",
         "hi": "H2 में शनि विवाह के लिए पारिवारिक सहयोग को सीमित करता है"},
    4:  {"en": "Saturn in H4 creates domestic tension impacting marriage harmony",
         "hi": "H4 में शनि घरेलू तनाव उत्पन्न करता है जो वैवाहिक सामंजस्य को प्रभावित करता है"},
    7:  {"en": "Saturn in H7 directly delays marriage — patience and Saturn remedies are essential",
         "hi": "H7 में शनि सीधे विवाह में देरी करता है — धैर्य और शनि उपाय आवश्यक हैं"},
    8:  {"en": "Saturn in H8 affects longevity and depth of the marital bond",
         "hi": "H8 में शनि वैवाहिक बंधन की दीर्घायु और गहराई को प्रभावित करता है"},
    12: {"en": "Saturn in H12 creates hidden obstacles or a foreign-based marriage",
         "hi": "H12 में शनि छिपी बाधाएँ या विदेश-आधारित विवाह उत्पन्न करता है"},
}


def analyze_marriage(positions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze marriage prospects from Lal Kitab chart positions.

    Args:
        positions: list of dicts, each with keys:
            planet   (str)
            house    (int)   — LK house (1-12)
            sign     (str, optional)
            dignity  (str, optional)  — exalted/own/friend/neutral/enemy/debilitated
            strength (float, optional) — 0-100

    Returns:
        h7_planets        — planets in H7 with LK effect data
        h7_planet_count   — int
        venus_analysis    — Venus house/dignity/marriage score
        moon_analysis     — Moon emotional readiness
        saturn_influence  — Saturn delay/karma assessment
        overall_marriage_score — 0-100 composite
        timing_outlook    — {en, hi}
        top_advice        — list of {en, hi} action items derived from chart
    """
    pos_map: Dict[str, Dict[str, Any]] = {
        p["planet"]: p for p in positions if isinstance(p, dict) and "planet" in p
    }

    # ── H7 planets ───────────────────────────────────────────────────────────
    h7_planets = [p for p in positions if isinstance(p, dict) and p.get("house") == 7]
    h7_effects: List[Dict[str, Any]] = []
    h7_scores: List[int] = []
    for entry in h7_planets:
        planet = entry.get("planet", "")
        effect = _H7_PLANET_EFFECTS.get(planet)
        if effect:
            h7_effects.append({
                "planet": planet,
                "timing": effect["timing"],
                "marriage_strength": effect["marriage_strength"],
                "partner_nature": effect["partner_nature"],
                "challenge": effect["challenge"],
                "advice": effect["advice"],
            })
            h7_scores.append(effect["marriage_strength"])

    # ── Venus ────────────────────────────────────────────────────────────────
    venus = pos_map.get("Venus", {})
    venus_house = venus.get("house", 0)
    venus_dignity = (venus.get("dignity") or "neutral").lower()
    venus_strength = venus.get("strength", 50)
    venus_modifier = _VENUS_DIGNITY_MODIFIER.get(venus_dignity, 0)
    venus_base = 55 + venus_modifier + (10 if venus_house == 7 else 0)
    venus_score = min(100, max(0, venus_base))
    venus_h7_effect = _H7_PLANET_EFFECTS.get("Venus") if venus_house == 7 else None

    if venus_h7_effect:
        venus_note_en = venus_h7_effect["advice"]["en"]
        venus_note_hi = venus_h7_effect["advice"]["hi"]
    elif venus_score >= 65:
        venus_note_en = f"Venus in H{venus_house} ({venus_dignity}) is well-placed — marriage karaka is strong."
        venus_note_hi = f"H{venus_house} में शुक्र ({venus_dignity}) अच्छी स्थिति में — विवाह कारक बलशाली।"
    elif venus_score >= 45:
        venus_note_en = f"Venus in H{venus_house} ({venus_dignity}) is moderately placed — consistent remedies will strengthen marriage prospects."
        venus_note_hi = f"H{venus_house} में शुक्र ({venus_dignity}) मध्यम स्थिति — नियमित उपाय से विवाह संभावनाएँ मजबूत होंगी।"
    else:
        venus_note_en = f"Venus in H{venus_house} ({venus_dignity}) is challenged — marriage karaka needs strengthening via Friday remedies."
        venus_note_hi = f"H{venus_house} में शुक्र ({venus_dignity}) चुनौतीपूर्ण — शुक्रवार उपाय से विवाह कारक को मजबूत करें।"

    venus_analysis = {
        "house": venus_house,
        "dignity": venus.get("dignity", "neutral"),
        "strength": venus_strength,
        "marriage_score": venus_score,
        "is_pakka": venus_house == 7,
        "note_en": venus_note_en,
        "note_hi": venus_note_hi,
    }

    # ── Moon ─────────────────────────────────────────────────────────────────
    moon = pos_map.get("Moon", {})
    moon_house = moon.get("house", 0)
    moon_dignity = (moon.get("dignity") or "neutral").lower()
    moon_strength = moon.get("strength", 50)
    if moon_dignity in {"exalted", "own"}:
        moon_score = 80
    elif moon_dignity in {"debilitated", "enemy"}:
        moon_score = 30
    else:
        moon_score = 55

    if moon_score >= 70:
        moon_readiness = "strong emotional stability"
        moon_readiness_hi = "मजबूत भावनात्मक स्थिरता"
    elif moon_score >= 45:
        moon_readiness = "moderate emotional groundedness"
        moon_readiness_hi = "मध्यम भावनात्मक दृढ़ता"
    else:
        moon_readiness = "emotional vulnerability"
        moon_readiness_hi = "भावनात्मक कमज़ोरी"

    moon_analysis = {
        "house": moon_house,
        "dignity": moon.get("dignity", "neutral"),
        "strength": moon_strength,
        "emotional_readiness_score": moon_score,
        "in_h7": moon_house == 7,
        "note_en": f"Moon in H{moon_house} ({moon.get('dignity','neutral')}) indicates {moon_readiness} in relationships.",
        "note_hi": f"H{moon_house} में चंद्र ({moon.get('dignity','neutral')}) संबंधों में {moon_readiness_hi} दर्शाता है।",
    }

    # ── Saturn ───────────────────────────────────────────────────────────────
    saturn = pos_map.get("Saturn", {})
    saturn_house = saturn.get("house", 0)
    saturn_note = _SATURN_DELAY.get(saturn_house, {
        "en": f"Saturn in H{saturn_house} has indirect influence on marriage timing.",
        "hi": f"H{saturn_house} में शनि का विवाह समय पर अप्रत्यक्ष प्रभाव है।",
    })

    saturn_influence = {
        "house": saturn_house,
        "causes_delay": saturn_house in _SATURN_DELAY,
        "direct_h7": saturn_house == 7,
        "note_en": saturn_note.get("en", ""),
        "note_hi": saturn_note.get("hi", ""),
    }

    # ── Composite score ───────────────────────────────────────────────────────
    score_inputs = [venus_score, moon_score]
    if h7_scores:
        score_inputs.extend(h7_scores)
    if saturn_house == 7:
        score_inputs.append(30)
    overall = int(sum(score_inputs) / len(score_inputs))

    # ── Timing outlook ────────────────────────────────────────────────────────
    if saturn_house == 7:
        timing_en = "Delayed — Saturn directly in H7; marriage typically after age 28-30. Patience and Saturn remedies are essential."
        timing_hi = "विलंबित — H7 में सीधे शनि; विवाह सामान्यतः 28-30 की आयु के बाद। धैर्य और शनि उपाय आवश्यक हैं।"
    elif overall >= 75:
        timing_en = "Favorable — marriage likely within normal age range with active effort."
        timing_hi = "अनुकूल — सामान्य आयु सीमा में सक्रिय प्रयास से विवाह संभव।"
    elif overall >= 55:
        timing_en = "Moderate — some delays possible; consistent Venus and Moon remedies will help."
        timing_hi = "मध्यम — कुछ देरी संभव; नियमित शुक्र और चंद्र उपाय सहायक होंगे।"
    else:
        timing_en = "Challenging — significant delays expected; planetary influence (Saturn/Rahu/Mars) requires careful and consistent remedy work."
        timing_hi = "चुनौतीपूर्ण — उल्लेखनीय देरी अपेक्षित; शनि/राहु/मंगल प्रभाव के लिए सावधानीपूर्वक और नियमित उपाय आवश्यक।"

    # ── Top advice (from actual H7/Venus data) ────────────────────────────────
    advice: List[Dict[str, str]] = []
    for effect in h7_effects[:2]:
        a = effect.get("advice", {})
        if a.get("en"):
            advice.append({"en": a["en"], "hi": a.get("hi", "")})
    if not any(e.get("en", "").startswith("Venus") for e in advice):
        advice.append({"en": venus_note_en, "hi": venus_note_hi})
    if saturn_house in _SATURN_DELAY and not any("Saturn" in e.get("en", "") for e in advice):
        advice.append({"en": saturn_note.get("en", ""), "hi": saturn_note.get("hi", "")})

    return {
        "h7_planets": h7_effects,
        "h7_planet_count": len(h7_planets),
        "venus_analysis": venus_analysis,
        "moon_analysis": moon_analysis,
        "saturn_influence": saturn_influence,
        "overall_marriage_score": overall,
        "timing_outlook": {"en": timing_en, "hi": timing_hi},
        "top_advice": advice[:3],
    }
