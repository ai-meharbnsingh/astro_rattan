"""
Lal Kitab 1952 remedy classification — P1.11.

Per LK 1952 canon, remedies fall into three tiers:

  1. "trial" (प्रयोग / आजमाइश) — a diagnostic probe. Keep or wear an item
     for a short period (typically 40–43 days, sometimes less) to see if
     the symptom shifts. If positive → continue as a full remedy. If
     negative or neutral → discontinue, try another.

  2. "remedy" (उपाय / टोटका) — the formal long-term upaya. Burying
     objects, throwing them in flowing water, offering specific items on
     specific days. Designed for structural correction.

  3. "good_conduct" (सदाचार / आचरण) — a behavioural rule that does not
     involve any object. Feeding animals daily, respecting specific
     relatives, avoiding specific foods, speech restrictions. These
     follow the LK principle that some afflictions can only be corrected
     by how the native lives, not by what they do once.

This module is deliberately heuristic — it reads the remedy text +
material + urgency and tags each remedy with a classification. The
backend stamps this onto every remedy dict so the frontend can render
a tier badge without any new endpoint.

Source: LK 1952 — chapters 3 (general remedies) and 4 (safety
precautions) distinguish "totka" (remedy) from "achran" (conduct).
"""
from __future__ import annotations

from typing import Any, Dict, Optional

Classification = str  # 'trial' | 'remedy' | 'good_conduct'

# Behavioural keywords — presence in EN text signals a good_conduct rule.
# These are rules about how the native lives, not objects they manipulate.
_CONDUCT_KEYWORDS_EN = (
    "respect", "honour", "honor", "avoid speaking", "don't speak",
    "do not speak", "serve ", "serve your", "feed crows", "feed dogs",
    "feed cows", "feed the", "care for", "never lie", "avoid lying",
    "donate regularly", "abstain", "refrain", "behave", "obey",
    "daily prayer", "visit temple", "touch feet", "seek blessings",
    "share food", "avoid meat", "vegetarian", "truthfulness",
    "anger control", "control anger",
)

# Hindi conduct keywords (broader phrases, since compound words differ)
_CONDUCT_KEYWORDS_HI = (
    "सम्मान", "आदर", "सेवा कर", "सेवा करें", "बोलने से बच",
    "झूठ न बोल", "कौए को खिला", "कुत्ते को खिला", "गाय को",
    "पैर छू", "आशीर्वाद ले", "सच बोल", "क्रोध पर नियंत्रण",
    "दया कर", "नियमित दान",
)

# Trial-signature keywords — short-duration probes, typically wear/carry.
_TRIAL_KEYWORDS_EN = (
    "keep in pocket", "carry with you", "carry in pocket", "wear for",
    "for 3 days", "for 7 days", "for 40 days", "for 41 days",
    "for 43 days", "try wearing", "test by", "observe for",
)

_TRIAL_KEYWORDS_HI = (
    "जेब में रख", "साथ रख", "पहन कर देख", "3 दिन", "7 दिन",
    "40 दिन", "41 दिन", "43 दिन", "परीक्षण", "जांच",
)

# Materials that are almost exclusively "remedy" (permanent object
# manipulation — bury, throw in river, offer, install).
_HEAVY_REMEDY_MATERIALS = {
    "copper square", "silver square", "iron nail", "silver nail",
    "coconut", "rice and milk", "jaggery", "ganga jal", "kesar",
    "tambe ka paisa", "chandi ka chaukor",
}


def _text_contains_any(text: str, needles) -> bool:
    """Lowercase substring match — safe for both EN and HI."""
    if not text:
        return False
    low = text.lower()
    return any(n.lower() in low for n in needles)


def classify_remedy(remedy: Dict[str, Any]) -> Classification:
    """
    Return 'trial' | 'remedy' | 'good_conduct' for a single remedy dict.

    Expected fields on `remedy`:
      - en (str), hi (str) — remedy text
      - material (str) — copper square / wheat / etc.
      - day (str) — Sunday / Monday / etc.
      - urgency (str, optional)

    Falls back to 'remedy' when nothing else matches — this is the safe
    default because most LK remedies are formal upayas.
    """
    if not isinstance(remedy, dict):
        return "remedy"

    en = str(remedy.get("en") or "")
    hi = str(remedy.get("hi") or "")
    material = str(remedy.get("material") or "").lower().strip()

    # 1. Good-conduct signal takes highest precedence — a behavioural rule
    #    stays behavioural even if it mentions an object in passing.
    if _text_contains_any(en, _CONDUCT_KEYWORDS_EN) or _text_contains_any(
        hi, _CONDUCT_KEYWORDS_HI
    ):
        return "good_conduct"

    # 2. Explicit trial markers — "wear for 3 days", "keep in pocket", etc.
    if _text_contains_any(en, _TRIAL_KEYWORDS_EN) or _text_contains_any(
        hi, _TRIAL_KEYWORDS_HI
    ):
        return "trial"

    # 3. Material-based hint — heavy/permanent materials → remedy.
    if material and any(m in material for m in _HEAVY_REMEDY_MATERIALS):
        return "remedy"

    # 4. Empty-material remedies with no object → lean toward good_conduct
    #    (typically "donate", "pray", etc. which are behavioural even
    #    without a conduct keyword match).
    if not material and len(en) < 80:
        # short and object-less — probably a behavioural nudge
        return "good_conduct"

    return "remedy"


def classification_label(classification: Classification, is_hi: bool = False) -> str:
    """Human-readable label for UI badges."""
    if classification == "trial":
        return "आजमाइश" if is_hi else "Trial"
    if classification == "good_conduct":
        return "सदाचार" if is_hi else "Good Conduct"
    return "उपाय" if is_hi else "Remedy"


def classification_description(classification: Classification, is_hi: bool = False) -> str:
    """One-liner explaining what the classification means."""
    if classification == "trial":
        return (
            "छोटी अवधि का परीक्षण — कुछ दिन आज़माकर देखें कि असर होता है या नहीं।"
            if is_hi
            else "Short-duration probe — try for a few days and observe the effect."
        )
    if classification == "good_conduct":
        return (
            "आचरण आधारित — कोई वस्तु नहीं, बस आदत या व्यवहार बदलना है।"
            if is_hi
            else "Behavioural — no object, only a change in daily conduct."
        )
    return (
        "औपचारिक उपाय — वस्तु आधारित दीर्घकालिक क्रिया।"
        if is_hi
        else "Formal upaya — object-based, long-term action."
    )


def stamp_classification(remedy: Dict[str, Any]) -> Dict[str, Any]:
    """In-place: add `classification` + `classification_en` + `classification_hi`
    to a remedy dict. Returns the same dict for chaining."""
    if not isinstance(remedy, dict):
        return remedy
    cls = classify_remedy(remedy)
    remedy["classification"] = cls
    remedy["classification_en"] = classification_label(cls, is_hi=False)
    remedy["classification_hi"] = classification_label(cls, is_hi=True)
    remedy["classification_desc_en"] = classification_description(cls, is_hi=False)
    remedy["classification_desc_hi"] = classification_description(cls, is_hi=True)
    return remedy
