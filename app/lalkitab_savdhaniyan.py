"""
app/lalkitab_savdhaniyan.py

Savdhaniyan (सावधानियाँ) — mandatory precautions that MUST be
observed when a Lal Kitab remedy is performed.

Source: Lal Kitab 1952 (Pt. Roop Chand Joshi), chapter 4.08 + 4.09.

The 1952 text is explicit: a remedy performed without its
precaution does NOT merely fail — it produces the OPPOSITE effect
(the "ulta asar" clause). This makes Savdhaniyan a safety-critical
layer — the app must surface them BEFORE any remedy instruction.

Categories
----------
  TIMING        - must/must-not do at certain times of day/week
  DIETARY       - food / alcohol / tobacco abstentions required
  CONSISTENCY   - consecutive days, non-missable (miss one → restart)
  NON_REVERSE   - actions that cannot be undone if wrongly performed
  WITNESSES     - remedies that must be secret, or witnessed
  SUBSTITUTES   - what NOT to substitute (e.g. imitation silver)
  FAMILY        - only by / with specific family members
  REVERSAL_RISK - most severe: remedy backfires if precaution missed

Each rule stamps its source so the UI can colour-code severity.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


# ─────────────────────────────────────────────────────────────
# GLOBAL / DEFAULT PRECAUTIONS — apply to EVERY Lal Kitab remedy
# unless a specific remedy overrides them.
# ─────────────────────────────────────────────────────────────
# LK 4.09 — "Night is Saturn's time"
# Remedies performed between sunset and sunrise shift under Saturn's
# dominion; most non-Saturn remedies silently invert. Only explicitly
# night-suitable remedies (Moon Monday-night, Saturn Saturday-dusk,
# Rahu Amavasya-midnight) are exempt.
NIGHT_IS_SATURN_WARNING: Dict[str, str] = {
    "en": (
        "Perform this remedy between sunrise and sunset. Lal Kitab 4.09: "
        "'Night belongs to Saturn' — remedies performed after dark are "
        "silently converted into Saturn's energy and can invert the "
        "intended result. Exceptions are explicitly night-suitable "
        "remedies (Moon on Monday night, Saturn on Saturday dusk, "
        "Rahu on Amavasya midnight) — this rule does NOT apply to those."
    ),
    "hi": (
        "यह उपाय सूर्योदय से सूर्यास्त के बीच ही करें। लाल किताब 4.09: "
        "'रात शनि की है' — रात के समय किया गया उपाय चुपचाप शनि की ऊर्जा "
        "में बदल जाता है और परिणाम उल्टा हो सकता है। अपवाद वे उपाय हैं जो "
        "स्पष्ट रूप से रात के लिए निर्देशित हैं (सोमवार रात चंद्र, शनिवार "
        "संध्या शनि, अमावस्या आधी रात राहु) — उन पर यह नियम लागू नहीं।"
    ),
    "severity": "high",
    "lk_ref": "4.09",
    "category": "TIMING",
}

# LK 4.08 — remedy action that reverses LK's 'cleanliness' principle
# fails silently; performer must be clean (bathed, fresh clothes,
# no tobacco/alcohol in last 12 hours) or the remedy reverses.
GENERIC_PRE_REMEDY_CLEANLINESS: Dict[str, str] = {
    "en": (
        "Before performing any Lal Kitab remedy: bathe, wear clean clothes, "
        "and abstain from tobacco / alcohol / meat for 12 hours prior. "
        "LK 4.08 states an unclean performer causes the remedy to silently "
        "reverse."
    ),
    "hi": (
        "कोई भी लाल किताब उपाय करने से पहले: स्नान करें, स्वच्छ वस्त्र "
        "पहनें, और 12 घंटे पहले से तम्बाकू / शराब / मांस का त्याग करें। "
        "लाल किताब 4.08 के अनुसार अशुद्ध कर्ता का उपाय चुपचाप उल्टा पड़ता है।"
    ),
    "severity": "high",
    "lk_ref": "4.08",
    "category": "DIETARY",
}


# ─────────────────────────────────────────────────────────────
# PLANET-SPECIFIC SAVDHANIYAN — overrides / additions to the default
# set, keyed on the planet the remedy targets.
# ─────────────────────────────────────────────────────────────
PLANET_SAVDHANIYAN: Dict[str, List[Dict[str, Any]]] = {
    "Sun": [
        {
            "en": "Sun remedies are done facing EAST at sunrise only. Facing the wrong direction silently inverts the remedy.",
            "hi": "सूर्य उपाय सूर्योदय के समय पूर्व दिशा की ओर मुँह करके ही करें। गलत दिशा में उपाय उल्टा पड़ता है।",
            "severity": "high", "lk_ref": "4.08", "category": "TIMING",
        },
        {
            "en": "Never perform Sun remedies when angry or having quarrelled with father. LK 4.08 — 'Surya raag ke samay nahin'.",
            "hi": "क्रोध की स्थिति में या पिता से विवाद के तुरंत बाद सूर्य उपाय न करें। 'सूर्य राग के समय नहीं'।",
            "severity": "high", "lk_ref": "4.08", "category": "NON_REVERSE",
        },
    ],
    "Moon": [
        {
            "en": "Moon remedies may be performed on Monday night (one of the few night-permitted remedies — LK 4.09 exception). All other days, follow sunrise-to-sunset rule.",
            "hi": "चंद्र उपाय सोमवार रात को किया जा सकता है (लाल किताब 4.09 का अपवाद)। अन्य दिनों में सूर्योदय-सूर्यास्त का नियम लागू।",
            "severity": "medium", "lk_ref": "4.09", "category": "TIMING",
        },
        {
            "en": "Moon remedies fail if performed while grieving a female family member. Wait 40 days after such loss.",
            "hi": "परिवार की किसी महिला के शोक काल में चंद्र उपाय विफल होते हैं। ऐसी हानि के बाद 40 दिन प्रतीक्षा करें।",
            "severity": "high", "lk_ref": "4.08", "category": "FAMILY",
        },
    ],
    "Mars": [
        {
            "en": "Mars remedies are DAYTIME ONLY (Tuesday morning preferred). Night-performed Mars remedy activates Saturn inversion per LK 4.09.",
            "hi": "मंगल उपाय केवल दिन में (मंगलवार सुबह श्रेष्ठ)। रात में किया गया मंगल उपाय लाल किताब 4.09 के अनुसार शनि में बदल जाता है।",
            "severity": "high", "lk_ref": "4.09", "category": "TIMING",
        },
        {
            "en": "Never donate red items (cloth/lentils) on a lunar eclipse day — causes blood-related reversal.",
            "hi": "चंद्र-ग्रहण के दिन लाल वस्तुएं (कपड़ा/दाल) दान न करें — रक्त-संबंधी उल्टा प्रभाव।",
            "severity": "high", "lk_ref": "4.08", "category": "NON_REVERSE",
        },
    ],
    "Mercury": [
        {
            "en": "Mercury remedies are performed on Wednesday. Feed green fodder to cows with your own hand — using an agent reverses the remedy.",
            "hi": "बुध उपाय बुधवार को करें। गायों को अपने हाथ से हरा चारा खिलाएं — दूसरे से कराने पर उपाय उल्टा पड़ता है।",
            "severity": "medium", "lk_ref": "4.08", "category": "NON_REVERSE",
        },
    ],
    "Jupiter": [
        {
            "en": "Jupiter remedies must NEVER be performed with display or pride. LK 4.08 — showing off the remedy makes it act like poison (specifically flagged for Jupiter in H10).",
            "hi": "गुरु उपाय कभी दिखावे या अहंकार के साथ न करें। लाल किताब 4.08 — दिखावटी उपाय विष की तरह कार्य करता है (विशेष रूप से 10वें में गुरु के लिए)।",
            "severity": "high", "lk_ref": "4.08", "category": "NON_REVERSE",
        },
        {
            "en": "Jupiter remedies are best at sunrise Thursday. Never on Amavasya (moonless night) — Jupiter's light is masked.",
            "hi": "गुरु उपाय गुरुवार सूर्योदय पर सर्वश्रेष्ठ। अमावस्या पर नहीं — गुरु की रोशनी ढक जाती है।",
            "severity": "medium", "lk_ref": "4.09", "category": "TIMING",
        },
    ],
    "Venus": [
        {
            "en": "Venus remedies are performed Friday morning. Never by the performer if they have cheated on their spouse — causes immediate reversal.",
            "hi": "शुक्र उपाय शुक्रवार सुबह करें। यदि कर्ता ने जीवनसाथी से बेवफाई की हो तो उपाय तुरंत उल्टा पड़ता है।",
            "severity": "high", "lk_ref": "4.08", "category": "NON_REVERSE",
        },
    ],
    "Saturn": [
        {
            "en": "Saturn remedies are the exception to LK 4.09 — Saturday evening/twilight is the preferred time. Daytime Saturn remedies are weaker.",
            "hi": "शनि उपाय लाल किताब 4.09 का अपवाद है — शनिवार संध्या/गोधूलि श्रेष्ठ समय। दिन के समय शनि उपाय कमज़ोर रहते हैं।",
            "severity": "medium", "lk_ref": "4.09", "category": "TIMING",
        },
        {
            "en": "Saturn donation (oil/iron) MUST be given without revealing identity — secret donation. Named/public Saturn donation reverses.",
            "hi": "शनि दान (तेल/लोहा) गुप्त रूप से दें — पहचान प्रकट न करें। नाम सहित/सार्वजनिक शनि दान उल्टा पड़ता है।",
            "severity": "high", "lk_ref": "4.08", "category": "WITNESSES",
        },
    ],
    "Rahu": [
        {
            "en": "Rahu remedies are acceptable on Amavasya midnight (LK 4.09 exception). Keep remedy fully secret — disclosed Rahu remedy backfires through deceit.",
            "hi": "राहु उपाय अमावस्या आधी रात को स्वीकार्य (लाल किताब 4.09 अपवाद)। उपाय पूर्णतः गुप्त रखें — प्रकट राहु उपाय धोखे से उल्टा पड़ता है।",
            "severity": "high", "lk_ref": "4.09", "category": "WITNESSES",
        },
    ],
    "Ketu": [
        {
            "en": "Ketu remedies are performed on Tuesday sunrise. Never feed stray dogs already fed by someone else on the same day — competing remedies cancel.",
            "hi": "केतु उपाय मंगलवार सूर्योदय पर। उसी दिन किसी और के द्वारा खिलाए गए आवारा कुत्तों को दोबारा न खिलाएं — परस्पर उपाय रद्द हो जाते हैं।",
            "severity": "medium", "lk_ref": "4.08", "category": "NON_REVERSE",
        },
    ],
}


def get_remedy_precautions(
    planet: str,
    house: Optional[int] = None,
    remedy_material: str = "",
) -> Dict[str, Any]:
    """
    Return the full Savdhaniyan bundle for a given planet's remedy.

    Args:
        planet: target planet ("Sun", "Mars", ...)
        house: (optional) the Lal Kitab house of the planet — used
            to emit house-specific warnings (e.g. Jupiter H10 pride rule).
        remedy_material: (optional) hint for matching a material-specific
            warning (e.g. "silver" / "iron" / "copper").

    Returns:
        {
            "precautions": List[{en, hi, severity, lk_ref, category}],
            "time_rule": str,   # "DAYTIME_ONLY" | "NIGHT_PERMITTED" | "SPECIFIC"
            "reversal_risk": bool,
            "source": "LK_CANONICAL",
        }
    """
    precautions: List[Dict[str, Any]] = []

    # 1. Always-applicable defaults
    precautions.append(dict(NIGHT_IS_SATURN_WARNING))
    precautions.append(dict(GENERIC_PRE_REMEDY_CLEANLINESS))

    # 2. Planet-specific layer
    for rule in PLANET_SAVDHANIYAN.get(planet, []):
        precautions.append(dict(rule))

    # 3. House-specific overlays (a few important LK 1952 cases)
    if planet == "Jupiter" and house == 10:
        precautions.append({
            "en": (
                "LK 1952 specifically flags Jupiter in H10: feeding with "
                "emotional display / pity is forbidden — causes career "
                "collapse ('poison effect'). Perform any Jupiter charity "
                "silently, without witnesses, without pity-photography."
            ),
            "hi": (
                "लाल किताब 1952 गुरु 10वें भाव के लिए स्पष्ट कहती है: "
                "भावनात्मक प्रदर्शन / दया के साथ भोजन कराना वर्जित है — "
                "करियर विनाश होता है ('विष प्रभाव')। गुरु से जुड़ा दान "
                "गुप्त रूप से, बिना गवाह, बिना फोटो करें।"
            ),
            "severity": "high", "lk_ref": "4.08", "category": "NON_REVERSE",
        })
    if planet == "Saturn" and house == 10:
        precautions.append({
            "en": "Saturn in H10 — do NOT build/buy property before age 48. This is the strongest 'non_reverse' precaution in LK 1952.",
            "hi": "शनि 10वें — 48 वर्ष की आयु से पहले निर्माण/संपत्ति-खरीद न करें। लाल किताब 1952 का सबसे सख्त 'अपरिवर्तनीय' सावधान।",
            "severity": "high", "lk_ref": "4.08", "category": "NON_REVERSE",
        })

    # 4. Derive time rule — explicit table instead of text-matching.
    #    Only planets with a *planet-specific* night exception clause
    #    in their rule list get NIGHT_PERMITTED / SPECIFIC status.
    NIGHT_PERMITTED_PLANETS = {"Moon", "Rahu"}   # Monday-night / Amavasya-midnight
    if planet == "Saturn":
        time_rule = "SPECIFIC"              # Saturday dusk
    elif planet in NIGHT_PERMITTED_PLANETS:
        time_rule = "NIGHT_PERMITTED"
    else:
        time_rule = "DAYTIME_ONLY"

    reversal_risk = any(
        p.get("category") == "NON_REVERSE" or p.get("severity") == "high"
        for p in precautions
    )

    return {
        "precautions": precautions,
        "time_rule": time_rule,
        "reversal_risk": reversal_risk,
        "lk_refs": sorted({p.get("lk_ref") for p in precautions if p.get("lk_ref")}),
        "source": "LK_CANONICAL",
    }
