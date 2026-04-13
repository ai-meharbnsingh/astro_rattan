"""
Kundli Full Report PDF Generator
=================================
Generates a 40-60 page professional Vedic astrology report matching
Parashara's Light 9.0 quality.

Usage:
    pdf_bytes = build_full_report(kundli_data)
    # write to file or stream via FastAPI
"""

from __future__ import annotations

import os
import math
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SIGN_ORDER = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

SIGN_SHORT = ["Ari", "Tau", "Gem", "Can", "Leo", "Vir",
              "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis"]

SIGN_LORD = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn",
    "Pisces": "Jupiter",
}

SIGN_INDEX = {s: i for i, s in enumerate(SIGN_ORDER)}

PLANET_LIST_7 = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
PLANET_LIST_9 = PLANET_LIST_7 + ["Rahu", "Ketu"]

NAKSHATRA_LIST = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
    "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
    "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada",
    "Revati",
]

NAKSHATRA_LORD = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
    "Jupiter", "Saturn", "Mercury", "Ketu", "Venus",
    "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn",
    "Mercury", "Ketu", "Venus", "Sun", "Moon",
    "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
]

DASHA_YEARS = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
    "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17,
}

DASHA_SEQUENCE = ["Ketu", "Venus", "Sun", "Moon", "Mars",
                  "Rahu", "Jupiter", "Saturn", "Mercury"]

EXALTATION = {
    "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn",
    "Mercury": "Virgo", "Jupiter": "Cancer", "Venus": "Pisces",
    "Saturn": "Libra", "Rahu": "Gemini", "Ketu": "Sagittarius",
}
DEBILITATION = {
    "Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer",
    "Mercury": "Pisces", "Jupiter": "Capricorn", "Venus": "Virgo",
    "Saturn": "Aries", "Rahu": "Sagittarius", "Ketu": "Gemini",
}
OWN_SIGNS = {
    "Sun": ["Leo"], "Moon": ["Cancer"], "Mars": ["Aries", "Scorpio"],
    "Mercury": ["Gemini", "Virgo"], "Jupiter": ["Sagittarius", "Pisces"],
    "Venus": ["Taurus", "Libra"], "Saturn": ["Capricorn", "Aquarius"],
}
MOOLATRIKONA = {
    "Sun": ("Leo", 0, 20), "Moon": ("Taurus", 4, 20),
    "Mars": ("Aries", 0, 12), "Mercury": ("Virgo", 16, 20),
    "Jupiter": ("Sagittarius", 0, 10), "Venus": ("Libra", 0, 15),
    "Saturn": ("Aquarius", 0, 20),
}

SIGN_ELEMENT = {
    "Aries": "Fire", "Taurus": "Earth", "Gemini": "Air", "Cancer": "Water",
    "Leo": "Fire", "Virgo": "Earth", "Libra": "Air", "Scorpio": "Water",
    "Sagittarius": "Fire", "Capricorn": "Earth", "Aquarius": "Air", "Pisces": "Water",
}
SIGN_MODALITY = {
    "Aries": "Moveable", "Taurus": "Fixed", "Gemini": "Dual",
    "Cancer": "Moveable", "Leo": "Fixed", "Virgo": "Dual",
    "Libra": "Moveable", "Scorpio": "Fixed", "Sagittarius": "Dual",
    "Capricorn": "Moveable", "Aquarius": "Fixed", "Pisces": "Dual",
}
SIGN_GENDER = {
    "Aries": "M", "Taurus": "F", "Gemini": "M", "Cancer": "F",
    "Leo": "M", "Virgo": "F", "Libra": "M", "Scorpio": "F",
    "Sagittarius": "M", "Capricorn": "F", "Aquarius": "M", "Pisces": "F",
}
PLANET_NATURE = {
    "Sun": "Malefic", "Moon": "Benefic", "Mars": "Malefic", "Mercury": "Neutral",
    "Jupiter": "Benefic", "Venus": "Benefic", "Saturn": "Malefic",
    "Rahu": "Malefic", "Ketu": "Malefic",
}
PLANET_ABBR = {
    "Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me",
    "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa",
    "Rahu": "Ra", "Ketu": "Ke", "Ascendant": "As", "Lagna": "As",
}

# Natural friendships (Naisargik Maitri)
NATURAL_FRIENDS: Dict[str, List[str]] = {
    "Sun": ["Moon", "Mars", "Jupiter"],
    "Moon": ["Sun", "Mercury"],
    "Mars": ["Sun", "Moon", "Jupiter"],
    "Mercury": ["Sun", "Venus"],
    "Jupiter": ["Sun", "Moon", "Mars"],
    "Venus": ["Mercury", "Saturn"],
    "Saturn": ["Mercury", "Venus"],
    "Rahu": ["Jupiter", "Venus", "Saturn"],
    "Ketu": ["Mars", "Venus"],
}
NATURAL_ENEMIES: Dict[str, List[str]] = {
    "Sun": ["Venus", "Saturn", "Rahu", "Ketu"],
    "Moon": ["Rahu", "Ketu"],
    "Mars": ["Mercury"],
    "Mercury": ["Moon"],
    "Jupiter": ["Mercury", "Venus"],
    "Venus": ["Sun", "Moon"],
    "Saturn": ["Sun", "Moon", "Mars"],
    "Rahu": ["Sun", "Moon", "Mars", "Ketu"],
    "Ketu": ["Sun", "Moon", "Rahu"],
}

# Yogini Dasha
YOGINI_NAMES = ["Mangala", "Pingala", "Dhanya", "Bhramari",
                "Bhadrika", "Ulka", "Siddha", "Sankata"]
YOGINI_YEARS = [1, 2, 3, 4, 5, 6, 7, 8]
YOGINI_LORDS = ["Moon", "Sun", "Jupiter", "Mars",
                "Mercury", "Saturn", "Venus", "Rahu"]

# Shadbala minimum requirements (in rupas)
SHADBALA_MIN = {
    "Sun": 390, "Moon": 360, "Mars": 300, "Mercury": 420,
    "Jupiter": 390, "Venus": 330, "Saturn": 300,
}

# Divisional chart names
VARGA_NAMES = {
    "D1": "Rashi (Lagna)", "D2": "Hora", "D3": "Dreshkana",
    "D4": "Chaturthamsha", "D7": "Saptamsha", "D9": "Navamsha",
    "D10": "Dashamsha", "D12": "Dwadashamsha", "D16": "Shodashamsha",
    "D20": "Vimshamsha", "D24": "Chaturvimshamsha", "D27": "Saptavimshamsha",
    "D30": "Trimshamsha", "D40": "Khavedamsha", "D45": "Akshavedamsha",
    "D60": "Shashtiamsha",
}

VARGA_PAGE1 = ["D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12"]
VARGA_PAGE2 = ["D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sg(data: Any, *keys, default: Any = "N/A") -> Any:
    """Safe nested get from dicts."""
    cur = data
    for k in keys:
        if isinstance(cur, dict):
            cur = cur.get(k, default)
        else:
            return default
    return cur if cur is not None else default


def _fmt_date(d: str) -> str:
    """Convert YYYY-MM-DD to DD/MM/YYYY."""
    try:
        parts = str(d).split("-")
        if len(parts) == 3:
            return f"{parts[2]}/{parts[1]}/{parts[0]}"
    except Exception:
        pass
    return str(d)


def _fmt_num(v: Any, decimals: int = 2) -> str:
    """Format a numeric value."""
    if v is None or v == "N/A":
        return "N/A"
    try:
        return f"{float(v):.{decimals}f}"
    except (ValueError, TypeError):
        return str(v)


def _sanitize(text: str) -> str:
    """Replace Unicode characters that Helvetica cannot render."""
    return (str(text)
            .replace("\u2014", "-")
            .replace("\u2013", "-")
            .replace("\u2018", "'")
            .replace("\u2019", "'")
            .replace("\u201c", '"')
            .replace("\u201d", '"')
            .replace("\u2022", "*")
            .replace("\u2026", "...")
            .replace("\u00b0", "deg")
            .replace("\u2265", ">=")
            .replace("\u2264", "<="))


def _find_hindi_font() -> Optional[str]:
    """Locate a Devanagari-capable TTF font on disk."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates = [
        os.path.join(base_dir, "fonts", "NotoSansDevanagari-Regular.ttf"),
        "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf",
        "/usr/share/fonts/noto/NotoSansDevanagari-Regular.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def _get_dignity(planet: str, sign: str) -> str:
    """Return dignity status of planet in sign."""
    if sign == EXALTATION.get(planet):
        return "Exalted"
    if sign == DEBILITATION.get(planet):
        return "Debilitated"
    if sign in OWN_SIGNS.get(planet, []):
        return "Own Sign"
    mt = MOOLATRIKONA.get(planet)
    if mt and sign == mt[0]:
        return "Moolatrikona"
    lord = SIGN_LORD.get(sign, "")
    if lord in NATURAL_FRIENDS.get(planet, []):
        return "Friend"
    if lord in NATURAL_ENEMIES.get(planet, []):
        return "Enemy"
    return "Neutral"


def _house_distance(from_sign: str, to_sign: str) -> int:
    """Houses between two signs (1-indexed, from_sign = house 1)."""
    f = SIGN_INDEX.get(from_sign, 0)
    t = SIGN_INDEX.get(to_sign, 0)
    return ((t - f) % 12) + 1


def _natural_relation(p1: str, p2: str) -> str:
    """Natural relationship of p1 towards p2."""
    if p1 == p2:
        return "Self"
    if p2 in NATURAL_FRIENDS.get(p1, []):
        return "Friend"
    if p2 in NATURAL_ENEMIES.get(p1, []):
        return "Enemy"
    return "Neutral"


def _temporal_relation(p1_sign: str, p2_sign: str) -> str:
    """Temporal relationship based on house distance."""
    dist = _house_distance(p1_sign, p2_sign)
    if dist in (2, 3, 4, 10, 11, 12):
        return "Friend"
    return "Enemy"


def _compound_relation(natural: str, temporal: str) -> str:
    """Panchadha (five-fold) compound relationship."""
    combo = (natural, temporal)
    mapping = {
        ("Friend", "Friend"): "Fast Friend",
        ("Friend", "Enemy"): "Neutral",
        ("Neutral", "Friend"): "Friend",
        ("Neutral", "Enemy"): "Enemy",
        ("Enemy", "Friend"): "Neutral",
        ("Enemy", "Enemy"): "Bitter Enemy",
        ("Self", "Friend"): "Self",
        ("Self", "Enemy"): "Self",
    }
    return mapping.get(combo, "Neutral")


# ---------------------------------------------------------------------------
# North Indian chart drawing
# ---------------------------------------------------------------------------

def _draw_north_indian_chart(pdf, x: float, y: float, size: float,
                              planets_in_houses: Dict[int, List[str]],
                              title: str = ""):
    """Draw a North Indian diamond chart on the PDF.

    planets_in_houses: {1: ["Su","Mo"], 2: ["Ma"], ...}  (1-based house numbers)
    """
    pdf.set_draw_color(100, 80, 60)
    pdf.set_line_width(0.4)

    # Outer square
    pdf.rect(x, y, size, size)

    mid = size / 2.0
    cx, cy = x + mid, y + mid

    # Diagonals (corner to corner)
    pdf.line(x, y, x + size, y + size)
    pdf.line(x + size, y, x, y + size)

    # Inner diamond connecting midpoints of sides
    pdf.line(x + mid, y, x + size, y + mid)
    pdf.line(x + size, y + mid, x + mid, y + size)
    pdf.line(x + mid, y + size, x, y + mid)
    pdf.line(x, y + mid, x + mid, y)

    # Title above the chart
    if title:
        pdf.set_font("Helvetica", "B", 7)
        pdf.set_text_color(180, 50, 20)
        tw = pdf.get_string_width(_sanitize(title))
        pdf.text(x + (size - tw) / 2, y - 2, _sanitize(title))
        pdf.set_text_color(40, 40, 40)

    # House centre positions for North Indian chart
    # House 1 = top-centre diamond, then clockwise
    q = size / 4.0
    house_positions = {
        1:  (cx, y + q * 0.8),
        2:  (x + q * 0.7, y + q * 0.7),
        3:  (x + q * 0.6, y + q * 1.6),
        4:  (x + q * 0.8, cy + q * 0.3),
        5:  (x + q * 0.6, y + q * 2.5),
        6:  (x + q * 0.7, y + size - q * 0.7),
        7:  (cx, y + size - q * 0.8),
        8:  (x + size - q * 0.7, y + size - q * 0.7),
        9:  (x + size - q * 0.6, y + q * 2.5),
        10: (x + size - q * 0.8, cy + q * 0.3),
        11: (x + size - q * 0.6, y + q * 1.6),
        12: (x + size - q * 0.7, y + q * 0.7),
    }

    # Planet text in houses
    pdf.set_font("Helvetica", "B", 5.5)
    pdf.set_text_color(40, 40, 40)
    for h_num in range(1, 13):
        plist = planets_in_houses.get(h_num, [])
        if not plist:
            continue
        hx, hy = house_positions[h_num]
        text = " ".join(plist[:4])
        tw = pdf.get_string_width(_sanitize(text))
        pdf.text(hx - tw / 2, hy + 1, _sanitize(text))
        if len(plist) > 4:
            text2 = " ".join(plist[4:])
            tw2 = pdf.get_string_width(_sanitize(text2))
            pdf.text(hx - tw2 / 2, hy + 4, _sanitize(text2))


def _build_planets_in_houses(planets: dict, asc_house: int = 1) -> Dict[int, List[str]]:
    """Build dict {chart_position: [planet_abbrs]}."""
    result: Dict[int, List[str]] = {}
    for pname, pinfo in planets.items():
        if not isinstance(pinfo, dict):
            continue
        house = pinfo.get("house", 1)
        abbr = PLANET_ABBR.get(pname, pname[:2])
        retro = pinfo.get("retrograde", False)
        label = f"{abbr}(R)" if retro else abbr
        chart_pos = ((house - asc_house) % 12) + 1
        result.setdefault(chart_pos, []).append(label)
    return result


# ---------------------------------------------------------------------------
# Planet-in-house interpretation database (concise)
# ---------------------------------------------------------------------------

_PLANET_HOUSE_BRIEF: Dict[str, Dict[int, str]] = {
    "Sun": {
        1: "Strong personality, leadership qualities, self-confidence. May have health issues in early life.",
        2: "Wealth from government or authority figures. Strong speech and family values.",
        3: "Courageous, good communication skills. Younger siblings may prosper.",
        4: "Comfort and property from father. May live away from birthplace.",
        5: "Intelligent, creative, good with children. Authority in education.",
        6: "Victory over enemies, good health. Service-oriented career.",
        7: "Spouse may be dominant. Government connections through partnership.",
        8: "Longevity concerns for father. Interest in occult and research.",
        9: "Blessed by father, religious, fortunate. Pilgrimages and higher learning.",
        10: "Powerful career, authority and recognition. Government connections.",
        11: "Gains from government, influential friends. Elder siblings prosper.",
        12: "Expenses through government. Spiritual inclination, foreign connections.",
    },
    "Moon": {
        1: "Emotional, imaginative, popular. Changeable nature, attractive appearance.",
        2: "Good family life, sweet speech, wealth fluctuations. Love for food.",
        3: "Mentally strong, good communicator. Travel and short journeys.",
        4: "Happy domestic life, emotional comfort. Close to mother, property gains.",
        5: "Romantic, creative, intelligent children. Emotional approach to speculation.",
        6: "Health fluctuations, service orientation. Victory in competitions.",
        7: "Attractive spouse, emotional partnerships. Public relations success.",
        8: "Emotional upheavals, interest in mysteries. Inheritance possible.",
        9: "Religious mother, pilgrimages. Emotional connection to dharma.",
        10: "Public recognition, popularity. Career involves nurturing or public.",
        11: "Gains through women, social circle. Fulfillment of desires.",
        12: "Spiritual inclination, expenditure. Foreign residence possible.",
    },
    "Mars": {
        1: "Energetic, courageous, aggressive. Physical vitality, scars possible.",
        2: "Harsh speech, family conflicts. Wealth through effort and competition.",
        3: "Very courageous, adventurous. Dominant over siblings, technical skills.",
        4: "Property and vehicle gains but domestic unrest. Technical education.",
        5: "Sharp intellect, competitive children. Speculative gains through analysis.",
        6: "Excellent for defeating enemies. Good health, competitive success.",
        7: "Passionate spouse, marital friction. Business in metals or technology.",
        8: "Accident prone, surgery possible. Research ability, occult interest.",
        9: "Active in dharma, pilgrimage to hot places. Father may have conflicts.",
        10: "Powerful career in engineering, military, surgery. Strong ambition.",
        11: "Good gains, influential friends. Elder siblings are ambitious.",
        12: "Hospitalization risk, foreign residence. Spiritual warrior tendencies.",
    },
    "Mercury": {
        1: "Intelligent, good communicator, youthful appearance. Analytical mind.",
        2: "Wealthy through intellect, good speech. Multiple income sources.",
        3: "Excellent communication, writing ability. Good with hands and crafts.",
        4: "Education in home, intellectual mother. Property through cleverness.",
        5: "Highly intelligent, creative writing. Children are bright.",
        6: "Analytical problem-solver, health through intellect. Legal acumen.",
        7: "Business-minded spouse, intellectual partnership. Trade skills.",
        8: "Research ability, interest in hidden knowledge. Insurance gains.",
        9: "Academic higher education, multiple languages. Philosophical writing.",
        10: "Career in communication, commerce, IT. Versatile professional.",
        11: "Gains through intellect, networking skills. Many acquaintances.",
        12: "Foreign education, spiritual writing. Imagination and fantasy.",
    },
    "Jupiter": {
        1: "Wise, generous, optimistic, good health. Natural teacher and guide.",
        2: "Excellent wealth, large family, truthful speech. Financial wisdom.",
        3: "Brave and righteous, religious siblings. Communication with wisdom.",
        4: "Excellent education, comfortable home. Happiness from mother.",
        5: "Very intelligent, good children, spiritual. Past life merit.",
        6: "Victory through righteousness. Good health, minimal enemies.",
        7: "Wise and generous spouse. Successful partnerships and counseling.",
        8: "Long life, interest in philosophy. Inheritance and occult wisdom.",
        9: "Highly fortunate, religious, teacher. Excellent for spiritual growth.",
        10: "Successful career, respected profession. Guidance to others.",
        11: "Excellent gains, powerful friends. Elder siblings are generous.",
        12: "Spiritual liberation, foreign connections. Charitable expenditure.",
    },
    "Venus": {
        1: "Attractive, charming, artistic. Love for luxury and beauty.",
        2: "Wealthy, sweet speech, good food. Family harmony and possessions.",
        3: "Artistic siblings, creative hobbies. Love letters and media.",
        4: "Comfortable home, luxury vehicles. Loving mother, beautiful home.",
        5: "Romantic, creative arts, entertainment. Love affairs and children.",
        6: "Overcomes enemies through charm. Health issues related to overindulgence.",
        7: "Beautiful/handsome spouse, happy marriage. Partnership success.",
        8: "Long-lived spouse, inheritance. Hidden pleasures, occult arts.",
        9: "Religious through beauty, artistic dharma. Fortunate in love.",
        10: "Career in arts, entertainment, luxury goods. Public charm.",
        11: "Gains through women, arts, luxury. Fulfillment of romantic desires.",
        12: "Bed pleasures, foreign luxury. Spiritual love, charitable giving.",
    },
    "Saturn": {
        1: "Hard-working, disciplined, thin build. Delays in early life.",
        2: "Slow wealth accumulation, cautious speech. Family responsibilities.",
        3: "Persistent courage, hard-working siblings. Methodical communication.",
        4: "Delayed property, responsibilities at home. Duty to mother.",
        5: "Delayed children, serious intellect. Conservative in speculation.",
        6: "Excellent for defeating enemies slowly. Service through discipline.",
        7: "Older or mature spouse, delayed marriage. Long-lasting partnerships.",
        8: "Long life, chronic health issues. Deep research and occult.",
        9: "Conservative dharma, religious discipline. Learns through hardship.",
        10: "Excellent career through persistence. Rise after 35, management.",
        11: "Steady gains over time, loyal friends. Elder siblings face delays.",
        12: "Foreign residence, spiritual discipline. Isolated spiritual practice.",
    },
    "Rahu": {
        1: "Unconventional personality, foreign connections. Illusion about self.",
        2: "Sudden wealth or loss, unusual speech. Non-traditional family.",
        3: "Courageous and unconventional. Media, technology communication.",
        4: "Foreign property, unusual home. Mother's unconventional nature.",
        5: "Unusual intellect, speculative gains. Non-traditional children.",
        6: "Victory over enemies through cunning. Unusual health remedies.",
        7: "Foreign spouse, unconventional marriage. Business across borders.",
        8: "Sudden events, transformation. Deep occult ability, research.",
        9: "Unconventional beliefs, foreign guru. Pilgrimage to foreign lands.",
        10: "Career in technology, foreign companies. Sudden rise in career.",
        11: "Large gains, influential network. Fulfillment through innovation.",
        12: "Foreign residence, spiritual illusion. Hospital or asylum connections.",
    },
    "Ketu": {
        1: "Spiritual, detached, psychic abilities. Unusual appearance.",
        2: "Detached from family, unusual speech. Past-life wealth.",
        3: "Spiritual courage, unusual communication. Mystical siblings.",
        4: "Detachment from home, spiritual mother. Past-life property karma.",
        5: "Spiritual intellect, past-life merit. Unusual approach to children.",
        6: "Victory through spiritual means. Unusual health, alternative healing.",
        7: "Spiritual partnerships, detached marriage. Past-life spouse karma.",
        8: "Deep occult ability, kundalini awakening. Transformation through crisis.",
        9: "Past-life spiritual merit, moksha yoga. Unusual religious path.",
        10: "Spiritual career, detached from worldly success. Healing profession.",
        11: "Spiritual gains, detached from material desires. Unusual friends.",
        12: "Excellent for spiritual liberation. Past-life monastery connections.",
    },
}

# ---------------------------------------------------------------------------
# Nakshatra interpretation database (concise)
# ---------------------------------------------------------------------------

_NAKSHATRA_BRIEF: Dict[str, str] = {
    "Ashwini": "Ruled by Ketu. Swift, healers, pioneers. Horse-headed twins of divine physicians. Quick action, medical talent, impatience.",
    "Bharani": "Ruled by Venus. Creative, transformative, bearing responsibilities. Yama's star. Artistic, intense, carries heavy burdens.",
    "Krittika": "Ruled by Sun. Sharp, purifying, critical. Agni's star. Determination, authority, cutting through illusions.",
    "Rohini": "Ruled by Moon. Beautiful, fertile, creative. Brahma's star. Material prosperity, artistic talent, possessiveness.",
    "Mrigashira": "Ruled by Mars. Searching, curious, gentle. Soma's star. Research ability, restlessness, spiritual quest.",
    "Ardra": "Ruled by Rahu. Transformative, stormy, intellectual. Rudra's star. Destruction and renewal, emotional intensity, brilliance after suffering.",
    "Punarvasu": "Ruled by Jupiter. Returning, renewing, prosperous. Aditi's star. Optimism, ability to bounce back, spiritual wisdom.",
    "Pushya": "Ruled by Saturn. Nourishing, protective, religious. Brihaspati's star. Best nakshatra for most activities, charitable, patient.",
    "Ashlesha": "Ruled by Mercury. Serpent energy, mystical, penetrating. Naga's star. Kundalini, hypnotic ability, cunning wisdom.",
    "Magha": "Ruled by Ketu. Royal, ancestral, powerful. Pitris' star. Authority, throne, connection to ancestors, past-life merit.",
    "Purva Phalguni": "Ruled by Venus. Creative, romantic, restful. Bhaga's star. Pleasure, artistic expression, marital bliss, luxury.",
    "Uttara Phalguni": "Ruled by Sun. Generous, helpful, patronizing. Aryaman's star. Contracts, friendships, leadership with grace.",
    "Hasta": "Ruled by Moon. Skillful, crafty, clever. Savitar's star. Manual dexterity, healing hands, resourcefulness.",
    "Chitra": "Ruled by Mars. Brilliant, creative, architectural. Vishwakarma's star. Beautiful creations, artistic, solitary brilliance.",
    "Swati": "Ruled by Rahu. Independent, flexible, scattered. Vayu's star. Business acumen, restless energy, spiritual seeking.",
    "Vishakha": "Ruled by Jupiter. Determined, branching, triumphant. Indragni's star. Goal-oriented, one-pointed focus, marriage challenges.",
    "Anuradha": "Ruled by Saturn. Devoted, friendly, organizational. Mitra's star. Friendship, devotion, success away from birthplace.",
    "Jyeshtha": "Ruled by Mercury. Senior, protective, authoritative. Indra's star. Eldest energy, protective of family, hidden insecurity.",
    "Mula": "Ruled by Ketu. Rooting out, destructive, investigative. Nirriti's star. Getting to the root, destruction of illusions, research.",
    "Purva Ashadha": "Ruled by Venus. Invincible, purifying, spreading. Apas's star. Early victory, philosophical, water purification.",
    "Uttara Ashadha": "Ruled by Sun. Final victory, righteous, universal. Vishvedevas' star. Universal goals, lasting achievement, leadership.",
    "Shravana": "Ruled by Moon. Listening, learning, connecting. Vishnu's star. Knowledge through hearing, media, counseling, travel.",
    "Dhanishta": "Ruled by Mars. Wealthy, rhythmic, musical. Vasus' star. Material abundance, musical talent, group leadership.",
    "Shatabhisha": "Ruled by Rahu. Healing, veiling, scientific. Varuna's star. 100 physicians, alternative healing, secretive, aquatic.",
    "Purva Bhadrapada": "Ruled by Jupiter. Burning, transformative, two-faced. Ajaikapada's star. Fierce spiritual energy, penance, transformation.",
    "Uttara Bhadrapada": "Ruled by Saturn. Depth, stability, wisdom. Ahirbudhnya's star. Deep meditation, kundalini, marital stability.",
    "Revati": "Ruled by Mercury. Nurturing, prosperous, safe travel. Pushan's star. Wealth, protection in journeys, completing cycles.",
}

# ---------------------------------------------------------------------------
# Gemstone database
# ---------------------------------------------------------------------------

_GEMSTONES: Dict[str, Dict[str, str]] = {
    "Sun": {"stone": "Ruby (Manik)", "finger": "Ring finger", "metal": "Gold",
            "weight": "3-6 carats", "day": "Sunday morning",
            "mantra": "Om Hraam Hreem Hroum Sah Suryaya Namah"},
    "Moon": {"stone": "Pearl (Moti)", "finger": "Little finger", "metal": "Silver",
             "weight": "4-6 carats", "day": "Monday morning",
             "mantra": "Om Shraam Shreem Shroum Sah Chandraya Namah"},
    "Mars": {"stone": "Red Coral (Moonga)", "finger": "Ring finger", "metal": "Gold/Copper",
             "weight": "5-9 carats", "day": "Tuesday morning",
             "mantra": "Om Kraam Kreem Kroum Sah Bhaumaya Namah"},
    "Mercury": {"stone": "Emerald (Panna)", "finger": "Little finger", "metal": "Gold",
                "weight": "3-6 carats", "day": "Wednesday morning",
                "mantra": "Om Braam Breem Broum Sah Budhaya Namah"},
    "Jupiter": {"stone": "Yellow Sapphire (Pukhraj)", "finger": "Index finger", "metal": "Gold",
                "weight": "3-5 carats", "day": "Thursday morning",
                "mantra": "Om Graam Greem Groum Sah Gurave Namah"},
    "Venus": {"stone": "Diamond (Heera) / White Sapphire", "finger": "Middle finger",
              "metal": "Platinum/Silver", "weight": "0.5-1 carat (diamond)",
              "day": "Friday morning",
              "mantra": "Om Draam Dreem Droum Sah Shukraya Namah"},
    "Saturn": {"stone": "Blue Sapphire (Neelam)", "finger": "Middle finger",
               "metal": "Silver/Iron", "weight": "3-5 carats",
               "day": "Saturday evening",
               "mantra": "Om Praam Preem Proum Sah Shanaye Namah"},
    "Rahu": {"stone": "Hessonite (Gomed)", "finger": "Middle finger", "metal": "Silver",
             "weight": "5-7 carats", "day": "Saturday evening",
             "mantra": "Om Bhram Bhreem Bhroum Sah Rahave Namah"},
    "Ketu": {"stone": "Cat's Eye (Lehsunia)", "finger": "Little finger", "metal": "Silver",
             "weight": "3-5 carats", "day": "Tuesday/Thursday",
             "mantra": "Om Sraam Sreem Sroum Sah Ketave Namah"},
}

# House topics
_HOUSE_TOPICS = {
    1: ("Self & Personality", "Physical body, appearance, health, temperament, early childhood, general disposition."),
    2: ("Wealth & Family", "Family, speech, food habits, right eye, early education, accumulated wealth, values."),
    3: ("Courage & Siblings", "Younger siblings, courage, short journeys, communication, hands, hobbies, neighbors."),
    4: ("Home & Happiness", "Mother, home, property, vehicles, education, domestic happiness, chest/lungs."),
    5: ("Children & Intelligence", "Children, intellect, creativity, past-life merit, speculation, romance, stomach."),
    6: ("Enemies & Health", "Enemies, diseases, debts, service, competition, maternal uncle, digestive system."),
    7: ("Marriage & Partnership", "Spouse, marriage, business partnerships, foreign travel, public dealing, reproductive organs."),
    8: ("Longevity & Transformation", "Death, longevity, sudden events, inheritance, occult, chronic disease, in-laws."),
    9: ("Fortune & Dharma", "Father, fortune, religion, higher education, long journeys, guru, philosophy, hips/thighs."),
    10: ("Career & Status", "Profession, status, fame, government, authority, karma, knees, public image."),
    11: ("Gains & Aspirations", "Income, gains, elder siblings, friends, social networks, desires fulfilled, ankles."),
    12: ("Loss & Liberation", "Loss, expenditure, foreign land, hospitals, prisons, spiritual liberation, feet, sleep."),
}


# ═══════════════════════════════════════════════════════════════════
# PUBLIC API
# ═══════════════════════════════════════════════════════════════════

def build_full_report(data: dict) -> bytes:
    """Build complete Parashara's Light style Kundli PDF report.
    Returns raw PDF bytes.
    """
    from fpdf import FPDF

    # ── Extract top-level fields ──────────────────────────
    person_name = data.get("person_name", data.get("birth_info", {}).get("person_name", "Native"))
    birth_date = data.get("birth_date", data.get("birth_info", {}).get("birth_date", "2000-01-01"))
    birth_time = data.get("birth_time", data.get("birth_info", {}).get("birth_time", "12:00"))
    birth_place = data.get("birth_place", data.get("birth_info", {}).get("birth_place", "Unknown"))
    latitude = data.get("latitude", data.get("birth_info", {}).get("latitude", 0.0))
    longitude = data.get("longitude", data.get("birth_info", {}).get("longitude", 0.0))
    gender = data.get("gender", data.get("birth_info", {}).get("gender", "Male"))
    ayanamsa_input = data.get("ayanamsa", data.get("birth_info", {}).get("ayanamsa", "Lahiri"))

    chart_data = data.get("chart_data") or {}
    avakhada = data.get("avakhada") or {}
    dasha_data = data.get("dasha") or {}
    yogas_doshas = data.get("yogas_doshas") or {}
    shadbala_data = data.get("shadbala") or {}
    ashtakvarga_data = data.get("ashtakvarga") or {}
    aspects_data = data.get("aspects") or {}
    yogini_data = data.get("yogini_dasha") or {}
    jaimini_data = data.get("jaimini") or {}
    kp_data = data.get("kp") or {}
    sodashvarga_data = data.get("sodashvarga") or {}
    varshphal_data = data.get("varshphal") or {}
    sadesati_data = data.get("sadesati") or {}

    planets = chart_data.get("planets") or {}
    houses = chart_data.get("houses") or {}
    ascendant = chart_data.get("ascendant") or {}
    asc_sign = ascendant.get("sign", "Aries")
    asc_degree = ascendant.get("degree", 0.0)
    ayanamsa_val = chart_data.get("ayanamsa", ayanamsa_input)

    # ── Colours (Parashara's Light style) ─────────────────
    SAFFRON = (180, 50, 20)
    DARK = (40, 40, 40)
    GOLD_LINE = (180, 140, 80)
    ALT_ROW = (245, 240, 235)
    WHITE = (255, 255, 255)
    HEADER_BG = (180, 50, 20)
    GOLD_LIGHT = (245, 235, 210)
    GREEN = (34, 120, 34)
    RED = (178, 34, 34)
    MUTED = (120, 110, 100)

    # ── Hindi font ────────────────────────────────────────
    hindi_font_path = _find_hindi_font()
    has_hindi = hindi_font_path is not None

    # ── Derived values ────────────────────────────────────
    birth_date_display = _fmt_date(birth_date)
    try:
        bd_obj = datetime.strptime(str(birth_date), "%Y-%m-%d")
        day_of_week = bd_obj.strftime("%A")
    except Exception:
        bd_obj = None
        day_of_week = "N/A"

    try:
        bt_parts = str(birth_time).split(":")
        birth_hour = int(bt_parts[0]) + int(bt_parts[1]) / 60.0
    except Exception:
        birth_hour = 12.0
    is_daytime = 6.0 <= birth_hour < 18.0

    # ── Planet lookup helpers ─────────────────────────────
    planet_signs: Dict[str, str] = {}
    planet_houses: Dict[str, int] = {}
    planet_lons: Dict[str, float] = {}
    planet_retro: Dict[str, bool] = {}
    for pn, pi in planets.items():
        if not isinstance(pi, dict):
            continue
        planet_signs[pn] = pi.get("sign", "Aries")
        planet_houses[pn] = pi.get("house", 1)
        planet_lons[pn] = pi.get("longitude", 0.0)
        planet_retro[pn] = pi.get("retrograde", False)

    asc_idx = SIGN_INDEX.get(asc_sign, 0)

    # ══════════════════════════════════════════════════════
    # PDF Class with Parashara's Light styling
    # ══════════════════════════════════════════════════════

    current_section = ["Birth Particulars"]

    class ReportPDF(FPDF):
        def __init__(self):
            super().__init__()
            self._has_hindi = False
            if has_hindi:
                self.add_font("Hindi", "", hindi_font_path, uni=True)
                self._has_hindi = True

        def cell(self, w=0, h=0, txt="", *a, **kw):
            if not self._has_hindi or kw.get("_raw"):
                kw.pop("_raw", None)
                return super().cell(w, h, _sanitize(str(txt)), *a, **kw)
            kw.pop("_raw", None)
            return super().cell(w, h, str(txt), *a, **kw)

        def multi_cell(self, w, h=0, txt="", *a, **kw):
            if not self._has_hindi:
                return super().multi_cell(w, h, _sanitize(str(txt)), *a, **kw)
            return super().multi_cell(w, h, str(txt), *a, **kw)

        def header(self):
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(*SAFFRON)
            super().cell(60, 5, _sanitize(person_name), align="L")
            if self._has_hindi:
                self.set_font("Hindi", "", 12)
                super().cell(70, 5, "\u0950", align="C")
            else:
                self.set_font("Helvetica", "B", 10)
                super().cell(70, 5, "Om", align="C")
            self.set_font("Helvetica", "B", 8)
            super().cell(60, 5, _sanitize(current_section[0]), align="R")
            self.ln(5)
            self.set_draw_color(*GOLD_LINE)
            self.set_line_width(0.5)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(3)
            self.set_draw_color(0, 0, 0)
            self.set_text_color(*DARK)

        def footer(self):
            self.set_y(-12)
            self.set_font("Helvetica", "I", 6.5)
            self.set_text_color(*MUTED)
            super().cell(100, 5, "AstroRattan.com  (c)  Vedic Astrology Report", align="L")
            super().cell(90, 5, f"HP2 * {self.page_no()}", align="R")
            self.set_text_color(*DARK)

        def section_title(self, title: str):
            self.set_font("Helvetica", "B", 10)
            self.set_fill_color(*HEADER_BG)
            self.set_text_color(*WHITE)
            self.cell(0, 7, f"  {title}", fill=True,
                      new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(*DARK)
            self.ln(2)

        def sub_section(self, title: str):
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(*SAFFRON)
            self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(*DARK)
            self.ln(1)

        def gold_line(self):
            self.set_draw_color(*GOLD_LINE)
            self.set_line_width(0.3)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(2)
            self.set_draw_color(0, 0, 0)

        def table_header(self, cols: list, widths: list, font_size: float = 7):
            self.set_font("Helvetica", "B", font_size)
            self.set_fill_color(*GOLD_LIGHT)
            self.set_text_color(*DARK)
            for i, h in enumerate(cols):
                self.cell(widths[i], 5.5, _sanitize(str(h)),
                          border=1, align="C", fill=True)
            self.ln()

        def table_row(self, vals: list, widths: list, row_idx: int = 0,
                      font_size: float = 6.5, aligns: Optional[list] = None):
            self.set_font("Helvetica", "", font_size)
            fill = row_idx % 2 == 1
            if fill:
                self.set_fill_color(*ALT_ROW)
            for i, v in enumerate(vals):
                a = "C" if aligns is None else aligns[i]
                self.cell(widths[i], 5, _sanitize(str(v)),
                          border=1, align=a, fill=fill)
            self.ln()

        def kv_row(self, label: str, value: str, lw: float = 50, vw: float = 45):
            self.set_font("Helvetica", "B", 7)
            self.cell(lw, 4.5, _sanitize(label + ":"))
            self.set_font("Helvetica", "", 7)
            self.cell(vw, 4.5, _sanitize(str(value)))

        def check_space(self, needed: float = 30):
            if self.get_y() + needed > self.h - 15:
                self.add_page()

    # ══════════════════════════════════════════════════════
    # Create PDF
    # ══════════════════════════════════════════════════════

    pdf = ReportPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(10, 10, 10)

    # ==================================================================
    # PAGE 1: BIRTH PARTICULARS + HINDU CALENDAR
    # ==================================================================
    current_section[0] = "Birth Particulars"
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(*SAFFRON)
    pdf.cell(0, 9, person_name, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*DARK)
    pdf.cell(0, 4, "Vedic Birth Chart (Kundli) Report",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.gold_line()

    # Two-column layout
    col_start_y = pdf.get_y()
    left_x = 10
    right_x = 105

    # Left: Birth Particulars
    pdf.set_xy(left_x, col_start_y)
    pdf.sub_section("Birth Particulars")

    birth_items = [
        ("Sex", gender),
        ("Date of Birth", birth_date_display),
        ("Day of Birth", day_of_week),
        ("Time of Birth", birth_time),
        ("Place of Birth", birth_place),
        ("Latitude", _fmt_num(latitude, 4)),
        ("Longitude", _fmt_num(longitude, 4)),
        ("Time Zone", _sg(chart_data, "timezone", default="+05:30")),
        ("GMT at Birth", _sg(chart_data, "gmt_at_birth", default="N/A")),
        ("LMT Correction", _sg(chart_data, "lmt_correction", default="N/A")),
        ("Local Mean Time", _sg(chart_data, "local_mean_time", default="N/A")),
        ("Sidereal Time", _sg(chart_data, "sidereal_time", default="N/A")),
        ("Ayanamsha", str(ayanamsa_val)),
        ("Ascendant (Lagna)", f"{asc_sign} {_fmt_num(asc_degree)}"),
    ]
    for label, val in birth_items:
        pdf.set_x(left_x)
        pdf.kv_row(label, str(val), 42, 50)
        pdf.ln()
    left_end_y = pdf.get_y()

    # Right: Hindu Calendar
    pdf.set_xy(right_x, col_start_y)
    pdf.sub_section("Hindu Calendar")

    hindu_items = [
        ("Vikram Samvat", _sg(avakhada, "vikram_samvat", default="N/A")),
        ("Saka Samvat", _sg(avakhada, "saka_samvat", default="N/A")),
        ("Lunar Month", _sg(avakhada, "lunar_month", default="N/A")),
        ("Sun's Ayana", _sg(avakhada, "ayana", default="N/A")),
        ("Season (Ritu)", _sg(avakhada, "ritu", default="N/A")),
        ("Paksha", _sg(avakhada, "paksha", default="N/A")),
        ("Hindu Weekday", _sg(avakhada, "weekday", default=day_of_week)),
        ("Tithi", _sg(avakhada, "tithi", default="N/A")),
        ("Nakshatra", _sg(avakhada, "nakshatra", default="N/A")),
        ("Yoga", _sg(avakhada, "yoga", default="N/A")),
        ("Karana", _sg(avakhada, "karana", default="N/A")),
        ("Sunrise", _sg(avakhada, "sunrise", default="N/A")),
        ("Sunset", _sg(avakhada, "sunset", default="N/A")),
    ]
    for label, val in hindu_items:
        pdf.set_x(right_x)
        pdf.kv_row(label, str(val), 38, 50)
        pdf.ln()
    right_end_y = pdf.get_y()
    pdf.set_y(max(left_end_y, right_end_y) + 4)

    # Avakhada Chakra table
    pdf.section_title("Avakhada Chakra")
    avk_items = [
        ("Varna", _sg(avakhada, "varna", default="N/A")),
        ("Vashya", _sg(avakhada, "vashya", default="N/A")),
        ("Nakshatra-Pada", f"{_sg(avakhada, 'nakshatra', default='N/A')}-{_sg(avakhada, 'nakshatra_pada', default='N/A')}"),
        ("Yoni", _sg(avakhada, "yoni", default="N/A")),
        ("Rashi", _sg(avakhada, "rashi", default="N/A")),
        ("Gana", _sg(avakhada, "gana", default="N/A")),
        ("Rashi Lord", _sg(avakhada, "rashi_lord", default="N/A")),
        ("Nadi", _sg(avakhada, "nadi", default="N/A")),
        ("Naamakshar", _sg(avakhada, "naamakshar", default="N/A")),
        ("Paya (Rashi)", _sg(avakhada, "paya_rashi", default="N/A")),
        ("Paya (Nak.)", _sg(avakhada, "paya_nakshatra", default="N/A")),
        ("Yunja", _sg(avakhada, "yunja", default="N/A")),
        ("Tatva", _sg(avakhada, "tatva", default="N/A")),
        ("Sun Sign", _sg(avakhada, "sun_sign", default="N/A")),
    ]
    for i in range(0, len(avk_items), 2):
        l1, v1 = avk_items[i]
        pdf.kv_row(l1, v1, 38, 50)
        if i + 1 < len(avk_items):
            l2, v2 = avk_items[i + 1]
            pdf.kv_row(l2, v2, 38, 50)
        pdf.ln()
    pdf.ln(3)

    # Dasha at birth summary
    pdf.sub_section("Dasha at Birth")
    pdf.set_font("Helvetica", "", 7)
    pdf.kv_row("Current Mahadasha", str(_sg(dasha_data, "current_dasha", default="N/A")), 42, 50)
    pdf.ln()
    pdf.kv_row("Balance of Dasha", str(_sg(dasha_data, "balance", default="N/A")), 42, 50)
    pdf.ln(5)

    # ==================================================================
    # PAGE 2: BIRTH CHART + PLANET TABLE
    # ==================================================================
    current_section[0] = "Birth Chart"
    pdf.add_page()

    pih_lagna = _build_planets_in_houses(planets, 1)
    moon_house = planet_houses.get("Moon", 1)
    pih_moon = _build_planets_in_houses(planets, moon_house)

    # Navamsha chart data
    navamsha_planets: Dict[int, List[str]] = {}
    for pn, pi in planets.items():
        if not isinstance(pi, dict):
            continue
        lon = pi.get("longitude", 0.0)
        nav_sign_idx = int((lon % 30) / (30 / 9.0))
        sign_idx = int(lon / 30.0) % 12
        element_start = {"Fire": 0, "Earth": 3, "Air": 6, "Water": 9}
        el = SIGN_ELEMENT.get(SIGN_ORDER[sign_idx], "Fire")
        nav_abs = (element_start.get(el, 0) + nav_sign_idx) % 12
        nav_house = nav_abs + 1
        abbr = PLANET_ABBR.get(pn, pn[:2])
        navamsha_planets.setdefault(nav_house, []).append(abbr)

    chart_size = 55
    chart_y = pdf.get_y()
    _draw_north_indian_chart(pdf, 12, chart_y + 4, chart_size, pih_lagna, "Lagna Chart (D1)")
    _draw_north_indian_chart(pdf, 75, chart_y + 4, chart_size, pih_moon, "Moon Chart (Chandra)")
    _draw_north_indian_chart(pdf, 138, chart_y + 4, chart_size, navamsha_planets, "Navamsha (D9)")
    pdf.set_y(chart_y + chart_size + 10)

    # Planet position table
    pdf.section_title("Planetary Positions")
    p_headers = ["Planet", "R/C", "Sign", "Degree", "Speed", "Nakshatra",
                 "Pada", "RL", "NL", "SL", "Status", "House"]
    p_widths = [16, 8, 19, 14, 13, 21, 9, 10, 10, 10, 18, 10]
    pdf.table_header(p_headers, p_widths)

    for idx, pname in enumerate(PLANET_LIST_9):
        pi = planets.get(pname, {})
        if not isinstance(pi, dict):
            continue
        sign = pi.get("sign", "N/A")
        deg = pi.get("sign_degree", pi.get("degree", "N/A"))
        deg_str = _fmt_num(deg) if deg != "N/A" else "N/A"
        speed = pi.get("speed", "N/A")
        speed_str = _fmt_num(speed, 3) if speed != "N/A" else "N/A"
        nak = pi.get("nakshatra", "N/A")
        pada = pi.get("nakshatra_pada", pi.get("pada", "N/A"))
        retro = "R" if pi.get("retrograde") else ""
        combust = "C" if pi.get("combust") else ""
        rc = retro or combust or ""
        rl = SIGN_LORD.get(sign, "?")
        nak_idx = NAKSHATRA_LIST.index(nak) if nak in NAKSHATRA_LIST else 0
        nl = NAKSHATRA_LORD[nak_idx] if nak_idx < len(NAKSHATRA_LORD) else "?"
        sl = pi.get("sub_lord", "?")
        dignity = _get_dignity(pname, sign)
        house = pi.get("house", "N/A")
        vals = [pname, rc, sign, deg_str, speed_str, nak,
                str(pada), PLANET_ABBR.get(rl, rl[:2]),
                PLANET_ABBR.get(nl, nl[:2]),
                PLANET_ABBR.get(str(sl), str(sl)[:2]),
                dignity, str(house)]
        pdf.table_row(vals, p_widths, idx)

    # Ascendant row
    pdf.set_font("Helvetica", "I", 6.5)
    pdf.set_fill_color(*GOLD_LIGHT)
    asc_nak = ascendant.get("nakshatra", "N/A")
    asc_pada = ascendant.get("nakshatra_pada", "N/A")
    asc_vals = ["Ascendant", "", asc_sign, _fmt_num(asc_degree), "",
                str(asc_nak), str(asc_pada), PLANET_ABBR.get(SIGN_LORD.get(asc_sign, ""), ""),
                "", "", "Lagna", "1"]
    for i, v in enumerate(asc_vals):
        pdf.cell(p_widths[i], 5, str(v), border=1, align="C", fill=True)
    pdf.ln(6)

    # ==================================================================
    # PAGE 3: BHAVA CHART + BHAVA SPASHTA + LORDSHIPS
    # ==================================================================
    current_section[0] = "Bhava Chart"
    pdf.add_page()
    pdf.section_title("Bhava Chart (Sripati)")

    bhava_pih: Dict[int, List[str]] = {}
    for pn, pi in planets.items():
        if not isinstance(pi, dict):
            continue
        h = pi.get("house", 1)
        bhava_pih.setdefault(h, []).append(PLANET_ABBR.get(pn, pn[:2]))

    _draw_north_indian_chart(pdf, 55, pdf.get_y() + 2, 80, bhava_pih, "Bhava (Sripati) Chart")
    pdf.set_y(pdf.get_y() + 88)

    pdf.section_title("Bhava Spashta (House Cusps)")
    bh_headers = ["Bhava", "Arambha (Begin)", "Madhya (Middle)", "Antya (End)", "Sign", "Lord"]
    bh_widths = [15, 35, 35, 35, 25, 25]
    pdf.table_header(bh_headers, bh_widths)

    houses_list = houses if isinstance(houses, list) else []
    for bnum in range(1, 13):
        sign = SIGN_ORDER[(asc_idx + bnum - 1) % 12]
        lord = SIGN_LORD.get(sign, "N/A")
        if bnum <= len(houses_list) and isinstance(houses_list[bnum - 1], dict):
            h_info = houses_list[bnum - 1]
            begin = _fmt_num(h_info.get("begin", h_info.get("start", "N/A")))
            middle = _fmt_num(h_info.get("middle", h_info.get("cusp", "N/A")))
            end = _fmt_num(h_info.get("end", "N/A"))
        else:
            cusp_lon = (asc_idx * 30 + asc_degree + (bnum - 1) * 30) % 360
            begin = _fmt_num(cusp_lon - 15)
            middle = _fmt_num(cusp_lon)
            end = _fmt_num(cusp_lon + 15)
        pdf.table_row([str(bnum), begin, middle, end, sign, lord], bh_widths, bnum)
    pdf.ln(4)

    pdf.section_title("House Lordships")
    lord_headers = ["House", "Sign", "Lord", "Lord In House", "Lord In Sign", "Dignity"]
    lord_widths = [15, 25, 20, 25, 25, 25]
    pdf.table_header(lord_headers, lord_widths)
    for bnum in range(1, 13):
        sign = SIGN_ORDER[(asc_idx + bnum - 1) % 12]
        lord = SIGN_LORD.get(sign, "N/A")
        lord_h = planet_houses.get(lord, "N/A")
        lord_s = planet_signs.get(lord, "N/A")
        lord_d = _get_dignity(lord, lord_s) if lord_s != "N/A" else "N/A"
        pdf.table_row([str(bnum), sign, lord, str(lord_h), lord_s, lord_d], lord_widths, bnum)
    pdf.ln(4)

    # ==================================================================
    # PAGES 4-5: DIVISIONAL CHARTS
    # ==================================================================
    def _draw_varga_page(varga_keys: list, page_title: str):
        current_section[0] = page_title
        pdf.add_page()
        pdf.section_title(page_title)
        chart_w = 42
        gap_x, gap_y = 6, 8
        cols = 4
        start_x, start_y = 10, pdf.get_y() + 2

        for ci, vk in enumerate(varga_keys):
            row_i = ci // cols
            col_i = ci % cols
            cx = start_x + col_i * (chart_w + gap_x)
            cy = start_y + row_i * (chart_w + gap_y + 6)
            if cy + chart_w + 10 > pdf.h - 15:
                pdf.add_page()
                pdf.section_title(page_title + " (cont.)")
                start_y = pdf.get_y() + 2
                cy = start_y

            varga_info = sodashvarga_data.get(vk, {})
            varga_planets: Dict[int, List[str]] = {}
            if isinstance(varga_info, dict):
                vp = varga_info.get("planets", varga_info)
                for vpn, vpd in vp.items():
                    if isinstance(vpd, dict):
                        h = vpd.get("house", vpd.get("sign_num", 1))
                        varga_planets.setdefault(int(h) if isinstance(h, (int, float)) else 1, []).append(
                            PLANET_ABBR.get(vpn, vpn[:2]))
                    elif isinstance(vpd, (int, float)):
                        varga_planets.setdefault(int(vpd), []).append(PLANET_ABBR.get(vpn, vpn[:2]))
            elif vk == "D1":
                varga_planets = _build_planets_in_houses(planets, 1)
            _draw_north_indian_chart(pdf, cx, cy, chart_w, varga_planets,
                                      f"{vk}: {VARGA_NAMES.get(vk, vk)}")

        final_row = (len(varga_keys) - 1) // cols
        pdf.set_y(start_y + (final_row + 1) * (chart_w + gap_y + 6) + 2)

    _draw_varga_page(VARGA_PAGE1, "Divisional Charts (Shodashvarga) I")
    _draw_varga_page(VARGA_PAGE2, "Divisional Charts (Shodashvarga) II")

    # ==================================================================
    # PAGE 6: PLANETARY FRIENDSHIP
    # ==================================================================
    current_section[0] = "Planetary Friendship"
    pdf.add_page()
    pdf.section_title("Planetary Friendship (Maitri Chakra)")
    friendship_planets = PLANET_LIST_9

    # 1. Natural
    pdf.sub_section("1. Naisargik Maitri Chakra (Natural Relationship)")
    nat_headers = ["Planet", "Friends", "Neutral", "Enemies"]
    nat_widths = [22, 55, 50, 55]
    pdf.table_header(nat_headers, nat_widths)
    for idx, p in enumerate(friendship_planets):
        friends = NATURAL_FRIENDS.get(p, [])
        enemies = NATURAL_ENEMIES.get(p, [])
        all_others = [x for x in friendship_planets if x != p]
        neutrals = [x for x in all_others if x not in friends and x not in enemies]
        pdf.table_row([p, ", ".join(friends), ", ".join(neutrals), ", ".join(enemies)], nat_widths, idx)
    pdf.ln(4)

    # 2. Temporal
    pdf.sub_section("2. Tatkalik Maitri Chakra (Temporal Relationship)")
    tw = 18
    tat_headers = ["Planet"] + [PLANET_ABBR.get(p, p[:2]) for p in friendship_planets]
    tat_widths = [22] + [tw] * len(friendship_planets)
    pdf.table_header(tat_headers, tat_widths)
    for idx, p1 in enumerate(friendship_planets):
        row_vals = [p1]
        s1 = planet_signs.get(p1, "Aries")
        for p2 in friendship_planets:
            if p1 == p2:
                row_vals.append("-")
            else:
                row_vals.append("F" if _temporal_relation(s1, planet_signs.get(p2, "Aries")) == "Friend" else "E")
        pdf.table_row(row_vals, tat_widths, idx, font_size=6)
    pdf.ln(4)

    # 3. Compound
    pdf.check_space(60)
    pdf.sub_section("3. Panchadha Maitri Chakra (Compound Relationship)")
    pan_headers = ["Planet"] + [PLANET_ABBR.get(p, p[:2]) for p in friendship_planets]
    pan_widths = [22] + [tw] * len(friendship_planets)
    pdf.table_header(pan_headers, pan_widths)
    compound_abbr = {"Fast Friend": "FF", "Friend": "F", "Neutral": "N",
                     "Enemy": "E", "Bitter Enemy": "BE", "Self": "-"}
    for idx, p1 in enumerate(friendship_planets):
        row_vals = [p1]
        s1 = planet_signs.get(p1, "Aries")
        for p2 in friendship_planets:
            if p1 == p2:
                row_vals.append("-")
            else:
                s2 = planet_signs.get(p2, "Aries")
                comp = _compound_relation(_natural_relation(p1, p2), _temporal_relation(s1, s2))
                row_vals.append(compound_abbr.get(comp, "N"))
        pdf.table_row(row_vals, pan_widths, idx, font_size=6)
    pdf.ln(2)
    pdf.set_font("Helvetica", "I", 6)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 4, "FF=Fast Friend  F=Friend  N=Neutral  E=Enemy  BE=Bitter Enemy",
             new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)
    pdf.ln(3)

    # ==================================================================
    # PAGE 7: SHODASHVARGA SUMMARY
    # ==================================================================
    current_section[0] = "Shodashvarga Summary"
    pdf.add_page()
    pdf.section_title("Shodashvarga Summary")

    # Signs in each varga
    pdf.sub_section("Signs Occupied in 16 Divisional Charts")
    all_vargas = list(VARGA_NAMES.keys())
    sv_cw = 10
    sv_headers = ["Planet"] + [v.replace("D", "") for v in all_vargas]
    sv_widths = [18] + [sv_cw] * len(all_vargas)
    pdf.table_header(sv_headers, sv_widths, font_size=5.5)

    for idx, pname in enumerate(PLANET_LIST_9):
        row_vals = [PLANET_ABBR.get(pname, pname[:2])]
        for vk in all_vargas:
            vdata = sodashvarga_data.get(vk, {})
            if isinstance(vdata, dict):
                vp = vdata.get("planets", vdata)
                pdata = vp.get(pname, {})
                if isinstance(pdata, dict):
                    s = pdata.get("sign", "")
                    row_vals.append(SIGN_SHORT[SIGN_INDEX[s]] if s in SIGN_INDEX else "?")
                elif isinstance(pdata, (int, float)):
                    si = int(pdata) - 1
                    row_vals.append(SIGN_SHORT[si % 12] if 0 <= si < 12 else "?")
                else:
                    row_vals.append("?")
            else:
                row_vals.append("?")
        pdf.table_row(row_vals, sv_widths, idx, font_size=5)
    pdf.ln(4)

    # Dignities
    pdf.sub_section("Dignities in Divisional Charts")
    dig_headers = ["Planet"] + [v.replace("D", "") for v in all_vargas[:8]]
    dig_widths = [22] + [20] * 8
    pdf.table_header(dig_headers, dig_widths, font_size=5.5)
    dig_abbr = {"Exalted": "Ex", "Debilitated": "Db", "Own Sign": "Own",
                "Moolatrikona": "MT", "Friend": "Fr", "Enemy": "En", "Neutral": "Nt"}
    for idx, pname in enumerate(PLANET_LIST_7):
        row_vals = [pname]
        for vk in all_vargas[:8]:
            vdata = sodashvarga_data.get(vk, {})
            if isinstance(vdata, dict):
                vp = vdata.get("planets", vdata)
                pdata = vp.get(pname, {})
                if isinstance(pdata, dict):
                    s = pdata.get("sign", "")
                    d = _get_dignity(pname, s) if s else "?"
                    row_vals.append(dig_abbr.get(d, d[:3]))
                else:
                    row_vals.append("?")
            else:
                row_vals.append("?")
        pdf.table_row(row_vals, dig_widths, idx, font_size=5.5)
    pdf.ln(4)

    # Vimshopaka Bala
    pdf.sub_section("Vimshopaka Bala")
    vim_headers = ["Planet", "Shadavarga", "Saptavarga", "Dashavarga", "Shodashavarga"]
    vim_widths = [30, 38, 38, 38, 38]
    pdf.table_header(vim_headers, vim_widths)
    vimshopaka = sodashvarga_data.get("vimshopaka", {})
    for idx, pname in enumerate(PLANET_LIST_7):
        pv = vimshopaka.get(pname, {})
        if isinstance(pv, dict):
            row = [pname, _fmt_num(pv.get("shadavarga", "N/A")),
                   _fmt_num(pv.get("saptavarga", "N/A")),
                   _fmt_num(pv.get("dashavarga", "N/A")),
                   _fmt_num(pv.get("shodashavarga", "N/A"))]
        else:
            row = [pname, "N/A", "N/A", "N/A", "N/A"]
        pdf.table_row(row, vim_widths, idx)
    pdf.ln(4)

    # ==================================================================
    # PAGE 8: SHAD BALA + BHAVA BALA
    # ==================================================================
    current_section[0] = "Shad Bala"
    pdf.add_page()
    pdf.section_title("Shadbala (Six-fold Planetary Strength)")

    sb_planets = shadbala_data.get("planets", {})
    sb_headers = ["Planet", "Sthana", "Dig", "Kala", "Cheshta", "Naisarg.", "Drik", "Total", "Reqd", "Ratio"]
    sb_widths = [18, 17, 15, 17, 17, 17, 15, 17, 15, 17]
    pdf.table_header(sb_headers, sb_widths)
    for idx, pname in enumerate(PLANET_LIST_7):
        d = sb_planets.get(pname, {})
        if not isinstance(d, dict):
            d = {}
        total = float(d.get("total", 0))
        reqd = SHADBALA_MIN.get(pname, 300)
        ratio = d.get("ratio")
        if not ratio:
            ratio = _fmt_num(total / reqd if reqd else 0, 2) + "x"
        else:
            ratio = f"{ratio}x"
        vals = [pname, _fmt_num(d.get("sthana", 0), 1), _fmt_num(d.get("dig", 0), 1),
                _fmt_num(d.get("kala", 0), 1), _fmt_num(d.get("cheshta", 0), 1),
                _fmt_num(d.get("naisargika", 0), 1), _fmt_num(d.get("drik", 0), 1),
                _fmt_num(total, 1), str(reqd), ratio]
        pdf.table_row(vals, sb_widths, idx)
    pdf.ln(2)

    # Ishta / Kashta Phala
    pdf.sub_section("Ishta Phala / Kashta Phala")
    ik_headers = ["Planet", "Ishta Phala", "Kashta Phala", "Net"]
    ik_widths = [30, 40, 40, 40]
    pdf.table_header(ik_headers, ik_widths)
    for idx, pname in enumerate(PLANET_LIST_7):
        d = sb_planets.get(pname, {})
        if not isinstance(d, dict):
            d = {}
        ishta = d.get("ishta_phala", "N/A")
        kashta = d.get("kashta_phala", "N/A")
        try:
            net = _fmt_num(float(ishta) - float(kashta), 1) if ishta != "N/A" and kashta != "N/A" else "N/A"
        except (ValueError, TypeError):
            net = "N/A"
        pdf.table_row([pname, _fmt_num(ishta), _fmt_num(kashta), net], ik_widths, idx)
    pdf.ln(4)

    # Bhava Bala
    pdf.check_space(60)
    pdf.section_title("Bhava Bala (House Strength)")
    bhava_bala = shadbala_data.get("bhava_bala", shadbala_data.get("bhav_bala", {}))
    bb_headers = ["Bhava", "From Lord", "Dig Bala", "Drishti", "Planets", "Day/Night", "Total"]
    bb_widths = [15, 25, 22, 22, 22, 22, 25]
    pdf.table_header(bb_headers, bb_widths)
    for bnum in range(1, 13):
        bd = bhava_bala.get(str(bnum), bhava_bala.get(bnum, {}))
        if not isinstance(bd, dict):
            bd = {"total": bd} if bd else {}
        pdf.table_row([
            str(bnum),
            _fmt_num(bd.get("from_lord", bd.get("strength", 0)), 1),
            _fmt_num(bd.get("dig_bala", 0), 1),
            _fmt_num(bd.get("drishti_bala", bd.get("drishti", 0)), 1),
            _fmt_num(bd.get("planets_bala", bd.get("planets", 0)), 1),
            _fmt_num(bd.get("day_night", 0), 1),
            _fmt_num(bd.get("total", bd.get("strength", 0)), 1),
        ], bb_widths, bnum)
    pdf.ln(4)

    # ==================================================================
    # PAGE 9: ASPECTS
    # ==================================================================
    current_section[0] = "Aspects"
    pdf.add_page()
    pdf.section_title("Aspects on Planets (Graha Drishti)")

    aspect_planets = aspects_data.get("planet_aspects", aspects_data.get("graha_drishti", {}))
    ap_cw = 17
    ap_headers = ["Aspecting"] + [PLANET_ABBR.get(p, p[:2]) for p in PLANET_LIST_9]
    ap_widths = [22] + [ap_cw] * 9
    pdf.table_header(ap_headers, ap_widths, font_size=6)

    if isinstance(aspect_planets, dict):
        for idx, p1 in enumerate(PLANET_LIST_9):
            row_vals = [PLANET_ABBR.get(p1, p1[:2])]
            p1_asp = aspect_planets.get(p1, {})
            for p2 in PLANET_LIST_9:
                if p1 == p2:
                    row_vals.append("-")
                else:
                    val = p1_asp.get(p2, "")
                    if isinstance(val, dict):
                        val = val.get("aspect_strength", val.get("strength", ""))
                    row_vals.append(_fmt_num(val, 1) if isinstance(val, (int, float)) else str(val)[:4] if val else "")
            pdf.table_row(row_vals, ap_widths, idx, font_size=5.5)
    elif isinstance(aspect_planets, list):
        a_headers = ["Planet", "Aspects On", "Type", "Strength"]
        a_widths = [30, 40, 40, 30]
        pdf.table_header(a_headers, a_widths)
        for idx, asp in enumerate(aspect_planets[:40]):
            if isinstance(asp, dict):
                pdf.table_row([
                    str(asp.get("planet", asp.get("from", "?"))),
                    str(asp.get("aspected", asp.get("to", "?"))),
                    str(asp.get("type", asp.get("aspect_type", ""))),
                    _fmt_num(asp.get("strength", ""), 1),
                ], a_widths, idx)
    pdf.ln(4)

    # Aspects on Bhavas
    pdf.check_space(70)
    pdf.section_title("Aspects on Bhavas (House Aspects)")
    bhava_aspects = aspects_data.get("bhava_aspects", aspects_data.get("house_aspects", {}))
    ba_cw = 13.5
    ba_headers = ["Planet"] + [str(i) for i in range(1, 13)]
    ba_widths = [22] + [ba_cw] * 12
    pdf.table_header(ba_headers, ba_widths, font_size=6)

    if isinstance(bhava_aspects, dict):
        for idx, pname in enumerate(PLANET_LIST_9):
            row_vals = [PLANET_ABBR.get(pname, pname[:2])]
            pa = bhava_aspects.get(pname, {})
            for bnum in range(1, 13):
                val = pa.get(str(bnum), pa.get(bnum, ""))
                if isinstance(val, dict):
                    val = val.get("strength", "")
                row_vals.append(_fmt_num(val, 1) if isinstance(val, (int, float)) else str(val)[:3] if val else "")
            pdf.table_row(row_vals, ba_widths, idx, font_size=5.5)
    elif isinstance(bhava_aspects, list):
        for idx, hasp in enumerate(bhava_aspects[:40]):
            if isinstance(hasp, dict):
                row = [str(hasp.get("planet", "?")), str(hasp.get("house", "?")),
                       str(hasp.get("type", "")), _fmt_num(hasp.get("strength", ""), 1)]
                # pad to 12 columns
                row_padded = [row[0]] + [""] * 12
                pdf.table_row(row_padded, ba_widths, idx, font_size=5.5)
    pdf.ln(4)

    # ==================================================================
    # PAGES 10-11: ASHTAKVARGA (BHINNASHTAKVARGA)
    # ==================================================================
    def _draw_bav_page(planet_list: list, page_title: str):
        current_section[0] = page_title
        pdf.add_page()
        pdf.section_title(page_title)
        bav = ashtakvarga_data.get("planet_bindus", ashtakvarga_data.get("bav", {}))
        contributors = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Lagna"]

        for pi_idx, planet in enumerate(planet_list):
            pdf.check_space(50)
            pdf.sub_section(f"Bhinnashtakvarga: {planet}")
            bav_grid = bav.get(planet, {})
            bav_h = ["Contrib."] + SIGN_SHORT + ["Total"]
            bav_cw = 12
            bav_ws = [17] + [bav_cw] * 12 + [14]
            pdf.table_header(bav_h, bav_ws, font_size=5)

            for ci, contrib in enumerate(contributors):
                row_vals = [PLANET_ABBR.get(contrib, contrib[:2])]
                row_total = 0
                if isinstance(bav_grid, dict):
                    contrib_data = bav_grid.get(contrib, {})
                    if isinstance(contrib_data, dict):
                        for sign in SIGN_ORDER:
                            v = contrib_data.get(sign, 0)
                            row_vals.append(str(v))
                            row_total += int(v) if isinstance(v, (int, float)) else 0
                    else:
                        for sign in SIGN_ORDER:
                            sign_data = bav_grid.get(sign, {})
                            v = sign_data.get(contrib, 0) if isinstance(sign_data, dict) else 0
                            row_vals.append(str(v))
                            row_total += int(v) if isinstance(v, (int, float)) else 0
                else:
                    row_vals += ["0"] * 12
                row_vals.append(str(row_total))
                pdf.table_row(row_vals, bav_ws, ci, font_size=5)

            # Totals row
            pdf.set_font("Helvetica", "B", 5)
            pdf.set_fill_color(*GOLD_LIGHT)
            totals_row = ["Total"]
            grand_total = 0
            if isinstance(bav_grid, dict):
                for sign in SIGN_ORDER:
                    sign_total = 0
                    for contrib in contributors:
                        cd = bav_grid.get(contrib, {})
                        if isinstance(cd, dict):
                            sign_total += int(cd.get(sign, 0))
                        else:
                            sd = bav_grid.get(sign, {})
                            sign_total += int(sd.get(contrib, 0)) if isinstance(sd, dict) else 0
                    totals_row.append(str(sign_total))
                    grand_total += sign_total
            else:
                totals_row += ["0"] * 12
            totals_row.append(str(grand_total))
            for i, v in enumerate(totals_row):
                pdf.cell(bav_ws[i], 5, _sanitize(str(v)), border=1, align="C", fill=True)
            pdf.ln(5)

    _draw_bav_page(["Sun", "Moon", "Mars", "Mercury"], "Bhinnashtakvarga I")
    _draw_bav_page(["Jupiter", "Venus", "Saturn", "Ascendant"], "Bhinnashtakvarga II")

    # ==================================================================
    # PAGE 12: SARVASHTAKVARGA + REDUCTIONS
    # ==================================================================
    current_section[0] = "Sarvashtakvarga"
    pdf.add_page()
    pdf.section_title("Sarvashtakvarga (SAV)")

    sav = ashtakvarga_data.get("sarvashtakvarga", ashtakvarga_data.get("sav", {}))
    sav_cw = 13
    sav_headers = [""] + SIGN_SHORT + ["Total"]
    sav_widths_t = [20] + [sav_cw] * 12 + [16]
    pdf.table_header(sav_headers, sav_widths_t, font_size=5.5)

    bav_all = ashtakvarga_data.get("planet_bindus", ashtakvarga_data.get("bav", {}))
    for idx, contrib in enumerate(PLANET_LIST_7 + ["Lagna"]):
        row_vals = [PLANET_ABBR.get(contrib, contrib[:2])]
        row_total = 0
        bav_c = bav_all.get(contrib, {})
        for sign in SIGN_ORDER:
            if isinstance(bav_c, dict):
                sign_total = 0
                for sub_c in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Lagna"]:
                    sub_d = bav_c.get(sub_c, {})
                    if isinstance(sub_d, dict):
                        sign_total += int(sub_d.get(sign, 0))
                    else:
                        sd2 = bav_c.get(sign, {})
                        sign_total += int(sd2.get(sub_c, 0)) if isinstance(sd2, dict) else 0
                row_vals.append(str(sign_total))
                row_total += sign_total
            else:
                v = sav.get(sign, 0) if isinstance(sav, dict) else 0
                row_vals.append(str(v))
                row_total += int(v) if isinstance(v, (int, float)) else 0
        row_vals.append(str(row_total))
        pdf.table_row(row_vals, sav_widths_t, idx, font_size=5.5)

    # SAV total
    pdf.set_font("Helvetica", "B", 5.5)
    pdf.set_fill_color(*GOLD_LIGHT)
    total_row = ["SAV"]
    grand_total = 0
    for sign in SIGN_ORDER:
        v = sav.get(sign, 0) if isinstance(sav, dict) else 0
        total_row.append(str(v))
        grand_total += int(v) if isinstance(v, (int, float)) else 0
    total_row.append(str(grand_total))
    for i, v in enumerate(total_row):
        pdf.cell(sav_widths_t[i], 5, _sanitize(str(v)), border=1, align="C", fill=True)
    pdf.ln(6)

    # SAV chart
    pdf.sub_section("SAV Distribution Chart")
    sav_chart: Dict[int, List[str]] = {}
    for si, sign in enumerate(SIGN_ORDER):
        v = sav.get(sign, 0) if isinstance(sav, dict) else 0
        sav_chart[si + 1] = [str(v)]
    _draw_north_indian_chart(pdf, 55, pdf.get_y() + 2, 70, sav_chart, "SAV Bindus")
    pdf.set_y(pdf.get_y() + 78)

    # Trikona Shodhana
    pdf.check_space(45)
    pdf.sub_section("Trikona Shodhana")
    trikona = ashtakvarga_data.get("trikona_shodhana", {})
    if trikona and isinstance(trikona, dict):
        tr_headers = ["Planet"] + SIGN_SHORT + ["Pinda"]
        tr_widths = [20] + [sav_cw] * 12 + [16]
        pdf.table_header(tr_headers, tr_widths, font_size=5.5)
        for idx, pname in enumerate(PLANET_LIST_7):
            pd = trikona.get(pname, {})
            row_vals = [PLANET_ABBR.get(pname, pname[:2])]
            pinda = 0
            for sign in SIGN_ORDER:
                v = pd.get(sign, 0) if isinstance(pd, dict) else 0
                row_vals.append(str(v))
                pinda += int(v) if isinstance(v, (int, float)) else 0
            row_vals.append(str(pinda))
            pdf.table_row(row_vals, tr_widths, idx, font_size=5.5)
    else:
        pdf.set_font("Helvetica", "I", 7)
        pdf.cell(0, 5, "Trikona Shodhana data not available.", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Ekadhipatya Shodhana
    pdf.check_space(40)
    pdf.sub_section("Ekadhipatya Shodhana")
    ekadhipatya = ashtakvarga_data.get("ekadhipatya_shodhana", {})
    if ekadhipatya and isinstance(ekadhipatya, dict):
        ek_headers = ["Planet"] + SIGN_SHORT + ["Pinda"]
        ek_widths = [20] + [sav_cw] * 12 + [16]
        pdf.table_header(ek_headers, ek_widths, font_size=5.5)
        for idx, pname in enumerate(PLANET_LIST_7):
            pd = ekadhipatya.get(pname, {})
            row_vals = [PLANET_ABBR.get(pname, pname[:2])]
            pinda = 0
            for sign in SIGN_ORDER:
                v = pd.get(sign, 0) if isinstance(pd, dict) else 0
                row_vals.append(str(v))
                pinda += int(v) if isinstance(v, (int, float)) else 0
            row_vals.append(str(pinda))
            pdf.table_row(row_vals, ek_widths, idx, font_size=5.5)
    else:
        pdf.set_font("Helvetica", "I", 7)
        pdf.cell(0, 5, "Ekadhipatya Shodhana data not available.", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # ==================================================================
    # PAGES 13-17: VIMSHOTTARI DASHA TIMELINE
    # ==================================================================
    current_section[0] = "Vimshottari Dasha"
    pdf.add_page()
    pdf.section_title("Vimshottari Dasha Timeline")

    current_md_name = _sg(dasha_data, "current_dasha", default="N/A")
    current_ad_name = _sg(dasha_data, "current_antardasha", default="N/A")
    dasha_balance = _sg(dasha_data, "balance", default="N/A")

    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(0, 5, f"Current Mahadasha: {current_md_name}  |  Antardasha: {current_ad_name}  |  Balance: {dasha_balance}",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # Mahadasha overview
    pdf.sub_section("Mahadasha Periods")
    md_headers = ["Planet", "Begin", "End", "Years"]
    md_widths = [30, 45, 45, 20]
    pdf.table_header(md_headers, md_widths)
    md_periods = dasha_data.get("mahadasha_periods", [])
    for idx, period in enumerate(md_periods):
        planet = period.get("planet", "?")
        start = _fmt_date(period.get("start_date", "?"))
        end = _fmt_date(period.get("end_date", "?"))
        years = str(period.get("years", DASHA_YEARS.get(planet, "?")))
        marker = " <" if planet == current_md_name else ""
        pdf.table_row([planet + marker, start, end, years], md_widths, idx)
    pdf.ln(4)

    # Antardasha detail pages
    ad_periods = dasha_data.get("antardasha_periods", dasha_data.get("antardasha", dasha_data.get("antardashas", {})))
    md_names = [p.get("planet", "") for p in md_periods] if md_periods else list(DASHA_YEARS.keys())

    # If ad_periods is a list (old format), convert it
    if isinstance(ad_periods, list):
        # Try to find antardashas embedded in mahadasha_periods
        ad_dict: Dict[str, list] = {}
        for md in md_periods:
            mp = md.get("planet", "")
            ads = md.get("antardashas", md.get("antardasha", []))
            if ads:
                ad_dict[mp] = ads
        if not ad_dict and ad_periods:
            ad_dict[current_md_name] = ad_periods
        ad_periods = ad_dict

    if isinstance(ad_periods, dict):
        mds_per_page = 3
        chunks = [md_names[i:i + mds_per_page] for i in range(0, len(md_names), mds_per_page)]
        for ch_idx, chunk in enumerate(chunks):
            if ch_idx > 0 or pdf.get_y() > 180:
                pdf.add_page()
            for md_name in chunk:
                pdf.check_space(35)
                pdf.sub_section(f"Antardasha in {md_name} Mahadasha")
                ad_list = ad_periods.get(md_name, [])
                if isinstance(ad_list, list) and ad_list:
                    ad_h = ["Antar", "Beginning", "Ending"]
                    ad_w = [30, 50, 50]
                    pdf.table_header(ad_h, ad_w)
                    for ai, ad in enumerate(ad_list):
                        if isinstance(ad, dict):
                            pdf.table_row([
                                ad.get("planet", ad.get("antardasha", ad.get("sub_lord", "?"))),
                                _fmt_date(ad.get("start_date", ad.get("begin", "?"))),
                                _fmt_date(ad.get("end_date", ad.get("end", "?"))),
                            ], ad_w, ai)
                    pdf.ln(3)
                else:
                    pdf.set_font("Helvetica", "I", 7)
                    pdf.cell(0, 4, f"No antardasha data for {md_name}.", new_x="LMARGIN", new_y="NEXT")
                    pdf.ln(2)

    # Pratyantar dasha
    pratyantar = dasha_data.get("pratyantar", dasha_data.get("pratyantar_periods", {}))
    if pratyantar and isinstance(pratyantar, dict):
        pdf.add_page()
        current_section[0] = "Pratyantar Dasha"
        pdf.section_title("Pratyantar Dasha (Sub-Sub Periods)")
        for md_key, ad_dict_inner in pratyantar.items():
            if not isinstance(ad_dict_inner, dict):
                continue
            for ad_key, pd_list in ad_dict_inner.items():
                if not isinstance(pd_list, list) or not pd_list:
                    continue
                pdf.check_space(25)
                pdf.sub_section(f"{md_key} - {ad_key}")
                pd_h = ["Pratyantar", "Begin", "End"]
                pd_w = [30, 50, 50]
                pdf.table_header(pd_h, pd_w)
                for pi_idx, pd in enumerate(pd_list[:9]):
                    if isinstance(pd, dict):
                        pdf.table_row([
                            pd.get("planet", "?"),
                            _fmt_date(pd.get("start_date", "?")),
                            _fmt_date(pd.get("end_date", "?")),
                        ], pd_w, pi_idx)
                pdf.ln(2)

    # ==================================================================
    # PAGE 18: YOGINI DASHA
    # ==================================================================
    current_section[0] = "Yogini Dasha"
    pdf.add_page()
    pdf.section_title("Yogini Dasha")

    yogini_current = _sg(yogini_data, "current_yogini", default="N/A")
    yogini_balance = _sg(yogini_data, "balance", default="N/A")
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(0, 5, f"Current Yogini: {yogini_current}  |  Balance: {yogini_balance}",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.sub_section("Yogini Dasha Reference")
    yr_headers = ["Yogini", "Lord", "Years"]
    yr_widths = [35, 30, 20]
    pdf.table_header(yr_headers, yr_widths)
    for idx in range(8):
        pdf.table_row([YOGINI_NAMES[idx], YOGINI_LORDS[idx], str(YOGINI_YEARS[idx])], yr_widths, idx)
    pdf.ln(4)

    pdf.sub_section("Yogini Dasha Periods")
    yogini_periods = yogini_data.get("periods", yogini_data.get("yogini_periods", []))
    if yogini_periods and isinstance(yogini_periods, list):
        yp_headers = ["Yogini", "Lord", "Begin", "End", "Years"]
        yp_widths = [30, 20, 40, 40, 15]
        pdf.table_header(yp_headers, yp_widths)
        for idx, yp in enumerate(yogini_periods):
            if isinstance(yp, dict):
                pdf.table_row([
                    yp.get("yogini", yp.get("name", "?")),
                    yp.get("lord", "?"),
                    _fmt_date(yp.get("start_date", yp.get("begin", "?"))),
                    _fmt_date(yp.get("end_date", yp.get("end", "?"))),
                    str(yp.get("years", "?")),
                ], yp_widths, idx)
        pdf.ln(3)

    yogini_ad = yogini_data.get("antardasha", yogini_data.get("sub_periods", {}))
    if yogini_ad and isinstance(yogini_ad, dict):
        for y_name, sub_list in yogini_ad.items():
            if not isinstance(sub_list, list) or not sub_list:
                continue
            pdf.check_space(30)
            pdf.sub_section(f"Sub-periods in {y_name}")
            ya_h = ["Sub-Yogini", "Begin", "End"]
            ya_w = [35, 45, 45]
            pdf.table_header(ya_h, ya_w)
            for si, sp in enumerate(sub_list):
                if isinstance(sp, dict):
                    pdf.table_row([
                        sp.get("yogini", sp.get("name", "?")),
                        _fmt_date(sp.get("start_date", sp.get("begin", "?"))),
                        _fmt_date(sp.get("end_date", sp.get("end", "?"))),
                    ], ya_w, si)
            pdf.ln(2)

    # ==================================================================
    # PAGE 19: YOGAS & DOSHAS
    # ==================================================================
    current_section[0] = "Yogas & Doshas"
    pdf.add_page()
    pdf.section_title("Yogas Found (Positive Combinations)")

    yogas = yogas_doshas.get("yogas", [])
    if yogas:
        for y in yogas:
            if isinstance(y, dict):
                name = y.get("name", y.get("yoga", "Yoga"))
                present = y.get("present", True)
                desc = y.get("description", y.get("effect", ""))
                strength = y.get("strength", "")
                pdf.check_space(12)
                pdf.set_font("Helvetica", "B", 8)
                if present:
                    pdf.set_text_color(*GREEN)
                    marker = "[+]"
                else:
                    pdf.set_text_color(*MUTED)
                    marker = "[ ]"
                label = f"  {marker} {name}"
                if strength:
                    label += f"  ({strength})"
                pdf.cell(0, 5, label, new_x="LMARGIN", new_y="NEXT")
                pdf.set_text_color(*DARK)
                if desc:
                    pdf.set_font("Helvetica", "", 6.5)
                    pdf.set_x(20)
                    pdf.multi_cell(170, 3.5, str(desc))
                    pdf.ln(1)
            elif isinstance(y, str):
                pdf.set_font("Helvetica", "", 7)
                pdf.cell(0, 5, f"  * {y}", new_x="LMARGIN", new_y="NEXT")
    else:
        pdf.set_font("Helvetica", "I", 7)
        pdf.cell(0, 5, "No yoga data available.", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.section_title("Doshas Found (Afflictions)")
    doshas = yogas_doshas.get("doshas", [])
    if doshas:
        for d in doshas:
            if isinstance(d, dict):
                name = d.get("name", d.get("dosha", "Dosha"))
                present = d.get("present", True)
                desc = d.get("description", d.get("effect", ""))
                severity = d.get("severity", "")
                remedy = d.get("remedy", d.get("remedies", ""))
                pdf.check_space(18)
                pdf.set_font("Helvetica", "B", 8)
                if present:
                    pdf.set_text_color(*RED)
                    marker = "[!]"
                else:
                    pdf.set_text_color(*MUTED)
                    marker = "[ ]"
                label = f"  {marker} {name}"
                if severity:
                    label += f"  [{severity}]"
                pdf.cell(0, 5, label, new_x="LMARGIN", new_y="NEXT")
                pdf.set_text_color(*DARK)
                if desc:
                    pdf.set_font("Helvetica", "", 6.5)
                    pdf.set_x(20)
                    pdf.multi_cell(170, 3.5, str(desc))
                if remedy:
                    pdf.set_font("Helvetica", "I", 6.5)
                    pdf.set_text_color(0, 100, 0)
                    pdf.set_x(20)
                    rt = remedy if isinstance(remedy, str) else "; ".join(remedy) if isinstance(remedy, list) else str(remedy)
                    pdf.multi_cell(170, 3.5, f"Remedy: {rt}")
                    pdf.set_text_color(*DARK)
                pdf.ln(1)
            elif isinstance(d, str):
                pdf.set_font("Helvetica", "", 7)
                pdf.cell(0, 5, f"  * {d}", new_x="LMARGIN", new_y="NEXT")
    else:
        pdf.set_font("Helvetica", "I", 7)
        pdf.cell(0, 5, "No dosha data available.", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # ==================================================================
    # PAGE 20: MANGALA DOSHA
    # ==================================================================
    current_section[0] = "Mangala Dosha"
    pdf.add_page()
    pdf.section_title("Mangala Dosha (Manglik) Consideration")

    mars_house = planet_houses.get("Mars", 0)
    mars_sign = planet_signs.get("Mars", "Aries")
    moon_sign_name = planet_signs.get("Moon", "Aries")

    manglik_houses = {1, 2, 4, 7, 8, 12}
    is_manglik_lagna = mars_house in manglik_houses
    mars_from_moon = _house_distance(moon_sign_name, mars_sign)
    is_manglik_moon = mars_from_moon in manglik_houses

    pdf.sub_section("Mars Position Analysis")
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(0, 5, f"Mars is in House {mars_house} ({mars_sign}) from Lagna",
             new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, f"Mars is in House {mars_from_moon} from Moon ({moon_sign_name})",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    pdf.sub_section("Manglik Status from Lagna")
    pdf.set_font("Helvetica", "B", 9)
    if is_manglik_lagna:
        pdf.set_text_color(*RED)
        pdf.cell(0, 6, "YES - Mangala Dosha is present from Lagna", new_x="LMARGIN", new_y="NEXT")
    else:
        pdf.set_text_color(*GREEN)
        pdf.cell(0, 6, "NO - Mangala Dosha is NOT present from Lagna", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)
    pdf.ln(2)

    pdf.sub_section("Manglik Status from Moon")
    pdf.set_font("Helvetica", "B", 9)
    if is_manglik_moon:
        pdf.set_text_color(*RED)
        pdf.cell(0, 6, "YES - Mangala Dosha is present from Moon", new_x="LMARGIN", new_y="NEXT")
    else:
        pdf.set_text_color(*GREEN)
        pdf.cell(0, 6, "NO - Mangala Dosha is NOT present from Moon", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)
    pdf.ln(4)

    # Classical references
    pdf.sub_section("Classical References on Mangala Dosha")
    classical_texts = [
        ("Brihat Parashara Hora Shastra",
         "If Mars is placed in the 1st, 2nd, 4th, 7th, 8th, or 12th house from the Lagna or Moon, "
         "the native is said to have Mangala Dosha. This dosha causes delays or difficulties in marriage."),
        ("Brihat Jataka (Varahamihira)",
         "Mars in the 7th house from Lagna destroys marital happiness. Mars in the 8th brings "
         "widowhood or loss. In the 1st house, Mars makes the native aggressive."),
        ("Jataka Parijata",
         "When Mars occupies the 1st, 4th, 7th, 8th, or 12th house, the person suffers from "
         "Kuja Dosha. Marriage with a similarly afflicted person neutralizes the dosha."),
        ("Phaladeepika",
         "Mars in the 2nd house causes harsh speech and family discord. In the 12th, it leads "
         "to excessive expenditure and bed pleasures unrelated to spouse."),
        ("Saravali",
         "Kuja Dosha is cancelled if Mars is in its own sign (Aries/Scorpio), exalted (Capricorn), "
         "or in conjunction with / aspected by Jupiter or benefics."),
    ]
    for title, text in classical_texts:
        pdf.check_space(18)
        pdf.set_font("Helvetica", "B", 7.5)
        pdf.set_text_color(*SAFFRON)
        pdf.cell(0, 5, title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(*DARK)
        pdf.set_font("Helvetica", "", 7)
        pdf.multi_cell(0, 3.5, text)
        pdf.ln(2)

    # Cancellation factors
    pdf.check_space(20)
    pdf.sub_section("Dosha Cancellation Factors")
    cancellations = []
    if mars_sign in ("Aries", "Scorpio"):
        cancellations.append("Mars is in own sign - partial cancellation")
    if mars_sign == "Capricorn":
        cancellations.append("Mars is exalted - cancellation possible")
    jup_h = planet_houses.get("Jupiter", 0)
    if jup_h == mars_house or abs(jup_h - mars_house) in (3, 5, 7, 9):
        cancellations.append("Jupiter aspects Mars - significant cancellation")
    if planet_houses.get("Venus", 0) == 7:
        cancellations.append("Venus in 7th house - partial mitigation")
    if cancellations:
        pdf.set_font("Helvetica", "", 7.5)
        for c in cancellations:
            pdf.set_text_color(*GREEN)
            pdf.cell(0, 5, f"  [*] {c}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(*DARK)
    else:
        pdf.set_font("Helvetica", "I", 7)
        pdf.cell(0, 5, "No standard cancellation factors found.", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    pdf.sub_section("Recommended Remedies")
    for r in [
        "Recite Hanuman Chalisa on Tuesdays",
        "Offer red flowers and red cloth to Hanuman Ji on Tuesdays",
        "Fast on Tuesdays (Mangalvar Vrat)",
        "Wear a coral (Moonga) gemstone after consultation with astrologer",
        "Donate red lentils (masoor dal) on Tuesdays",
        "Marriage between two Manglik individuals neutralizes the dosha",
        "Kumbh Vivah (symbolic marriage with pot/tree) before actual marriage",
        "Chant Mangal Beej Mantra: Om Kram Kreem Kroum Sah Bhaumaya Namah",
    ]:
        pdf.set_font("Helvetica", "", 7)
        pdf.cell(0, 4.5, f"  * {r}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # ==================================================================
    # PAGE 21: SADE SATI
    # ==================================================================
    current_section[0] = "Sade Sati"
    pdf.add_page()
    pdf.section_title("Sade Sati of Saturn")

    moon_sign_ss = planet_signs.get("Moon", "Aries")
    saturn_sign = planet_signs.get("Saturn", "Aries")
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(0, 5, f"Moon Sign (Janma Rashi): {moon_sign_ss}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, f"Saturn's Natal Position: {saturn_sign} (House {planet_houses.get('Saturn', 'N/A')})",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    pdf.sub_section("What is Sade Sati?")
    pdf.set_font("Helvetica", "", 7)
    pdf.multi_cell(0, 3.5,
        "Sade Sati is the 7.5-year period when Saturn transits through the 12th, 1st, and "
        "2nd houses from the natal Moon sign. It occurs approximately 2-3 times in a person's "
        "lifetime. The first phase (12th from Moon) brings financial challenges, the second "
        "phase (over Moon, called 'Peak') brings mental stress and health issues, and the "
        "third phase (2nd from Moon) affects family and finances.")
    pdf.ln(3)

    ss_cycles = sadesati_data.get("cycles", sadesati_data.get("periods", []))
    if ss_cycles and isinstance(ss_cycles, list):
        pdf.sub_section("Sade Sati Cycles")
        ss_h = ["Cycle", "Phase", "Start", "End", "Saturn In"]
        ss_w = [15, 30, 35, 35, 30]
        pdf.table_header(ss_h, ss_w)
        for idx, cycle in enumerate(ss_cycles):
            if isinstance(cycle, dict):
                pdf.table_row([
                    str(cycle.get("cycle", idx + 1)),
                    cycle.get("phase", "N/A"),
                    _fmt_date(cycle.get("start", cycle.get("start_date", "N/A"))),
                    _fmt_date(cycle.get("end", cycle.get("end_date", "N/A"))),
                    cycle.get("saturn_sign", cycle.get("sign", "N/A")),
                ], ss_w, idx)
        pdf.ln(3)
    else:
        pdf.sub_section("Sade Sati Phase Reference")
        moon_idx = SIGN_INDEX.get(moon_sign_ss, 0)
        sp_h = ["Phase", "Saturn Transiting", "Effect"]
        sp_w = [40, 35, 80]
        pdf.table_header(sp_h, sp_w)
        phases = [
            ("Phase 1 (Rising)", SIGN_ORDER[(moon_idx - 1) % 12], "Financial pressure, expenses increase"),
            ("Phase 2 (Peak)", moon_sign_ss, "Mental stress, health issues, peak intensity"),
            ("Phase 3 (Setting)", SIGN_ORDER[(moon_idx + 1) % 12], "Family matters, speech, finances affected"),
        ]
        for idx, (ph, sg_name, eff) in enumerate(phases):
            pdf.table_row([ph, sg_name, eff], sp_w, idx)
        pdf.ln(3)

    pdf.check_space(15)
    pdf.sub_section("Current Status")
    ss_active = sadesati_data.get("is_active", sadesati_data.get("active", False))
    ss_phase = sadesati_data.get("current_phase", "N/A")
    pdf.set_font("Helvetica", "B", 9)
    if ss_active:
        pdf.set_text_color(*RED)
        pdf.cell(0, 6, f"Sade Sati is CURRENTLY ACTIVE - {ss_phase}", new_x="LMARGIN", new_y="NEXT")
    else:
        pdf.set_text_color(*GREEN)
        pdf.cell(0, 6, "Sade Sati is NOT currently active.", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)
    pdf.ln(3)

    pdf.sub_section("Sade Sati Remedies")
    pdf.set_font("Helvetica", "", 7)
    for r in [
        "Recite Shani Stotra or Shani Chalisa on Saturdays",
        "Light a sesame oil lamp under a Peepal tree on Saturdays",
        "Donate black cloth, iron items, or mustard oil on Saturdays",
        "Wear a Blue Sapphire (Neelam) only after thorough analysis",
        "Feed crows and black dogs on Saturdays",
        "Chant Shani Beej Mantra: Om Praam Preem Proum Sah Shanaye Namah (23,000 times)",
        "Visit Shani temple on Saturdays and offer mustard oil",
        "Keep fast on Saturdays (Shanivar Vrat)",
    ]:
        pdf.cell(0, 4.5, f"  * {r}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # ==================================================================
    # KP SYSTEM (optional)
    # ==================================================================
    if kp_data and isinstance(kp_data, dict):
        current_section[0] = "KP System"
        pdf.add_page()
        pdf.section_title("Krishnamurti Paddhati (KP) Summary")

        kp_planets = kp_data.get("planets", kp_data.get("significators", {}))
        if kp_planets and isinstance(kp_planets, dict):
            pdf.sub_section("KP Planet Significators")
            kp_h = ["Planet", "Star Lord", "Sub Lord", "Sub-Sub Lord", "Significator Of"]
            kp_w = [22, 25, 25, 25, 60]
            pdf.table_header(kp_h, kp_w)
            for idx, pname in enumerate(PLANET_LIST_9):
                kpd = kp_planets.get(pname, {})
                if isinstance(kpd, dict):
                    pdf.table_row([
                        pname,
                        str(kpd.get("star_lord", kpd.get("nakshatra_lord", "N/A"))),
                        str(kpd.get("sub_lord", "N/A")),
                        str(kpd.get("sub_sub_lord", "N/A")),
                        str(kpd.get("significator_of", kpd.get("houses", "N/A"))),
                    ], kp_w, idx)
            pdf.ln(3)

        kp_cusps = kp_data.get("cusps", kp_data.get("house_cusps", {}))
        if kp_cusps:
            pdf.sub_section("KP House Cusps")
            kc_h = ["Cusp", "Degree", "Sign", "Star Lord", "Sub Lord"]
            kc_w = [15, 25, 25, 30, 30]
            pdf.table_header(kc_h, kc_w)
            if isinstance(kp_cusps, dict):
                for bnum in range(1, 13):
                    cd = kp_cusps.get(str(bnum), kp_cusps.get(bnum, {}))
                    if isinstance(cd, dict):
                        pdf.table_row([str(bnum), _fmt_num(cd.get("degree", "N/A")),
                                      str(cd.get("sign", "N/A")), str(cd.get("star_lord", "N/A")),
                                      str(cd.get("sub_lord", "N/A"))], kc_w, bnum)
            elif isinstance(kp_cusps, list):
                for idx, cusp in enumerate(kp_cusps[:12]):
                    if isinstance(cusp, dict):
                        pdf.table_row([str(cusp.get("cusp", idx + 1)),
                                      _fmt_num(cusp.get("degree", "N/A")),
                                      str(cusp.get("sign", "N/A")),
                                      str(cusp.get("star_lord", "")),
                                      str(cusp.get("sub_lord", ""))], kc_w, idx)
            pdf.ln(3)

    # ==================================================================
    # JAIMINI SYSTEM (optional)
    # ==================================================================
    if jaimini_data and isinstance(jaimini_data, dict):
        current_section[0] = "Jaimini System"
        pdf.add_page()
        pdf.section_title("Jaimini Astrology Summary")

        karakas = jaimini_data.get("chara_karakas", jaimini_data.get("karakas", {}))
        if karakas and isinstance(karakas, dict):
            pdf.sub_section("Chara Karakas (Variable Significators)")
            ck_h = ["Karaka", "Planet", "Degree"]
            ck_w = [50, 35, 35]
            pdf.table_header(ck_h, ck_w)
            karaka_names = ["Atmakaraka", "Amatyakaraka", "Bhratrikaraka",
                          "Matrikaraka", "Putrakaraka", "Gnatikaraka", "Darakaraka"]
            for idx, kn in enumerate(karaka_names):
                kd = karakas.get(kn, karakas.get(kn.lower(), {}))
                if isinstance(kd, dict):
                    pdf.table_row([kn, str(kd.get("planet", "N/A")), _fmt_num(kd.get("degree", "N/A"))], ck_w, idx)
                elif isinstance(kd, str):
                    pdf.table_row([kn, kd, ""], ck_w, idx)
            pdf.ln(3)

        # Special Lagnas
        lagnas = jaimini_data.get("special_lagnas", {})
        if lagnas and isinstance(lagnas, dict):
            pdf.sub_section("Special Lagnas")
            pdf.set_font("Helvetica", "", 8)
            for lname, lval in lagnas.items():
                val_str = str(lval) if not isinstance(lval, dict) else lval.get("sign", str(lval))
                pdf.cell(0, 5, f"  {lname}: {val_str}", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(3)

        jd = jaimini_data.get("dasha", jaimini_data.get("chara_dasha", []))
        if jd and isinstance(jd, list):
            pdf.sub_section("Chara Dasha Periods")
            jd_h = ["Sign", "Begin", "End", "Years"]
            jd_w = [30, 45, 45, 20]
            pdf.table_header(jd_h, jd_w)
            for idx, cd in enumerate(jd[:24]):
                if isinstance(cd, dict):
                    pdf.table_row([str(cd.get("sign", "?")),
                                  _fmt_date(cd.get("start_date", cd.get("start", "?"))),
                                  _fmt_date(cd.get("end_date", cd.get("end", "?"))),
                                  str(cd.get("years", cd.get("duration", "?")))], jd_w, idx)
            pdf.ln(3)

        rashi_asp = jaimini_data.get("rashi_aspects", {})
        if rashi_asp and isinstance(rashi_asp, dict):
            pdf.sub_section("Jaimini Rashi Drishti (Sign Aspects)")
            pdf.set_font("Helvetica", "", 7)
            for sign_name, aspected in rashi_asp.items():
                if isinstance(aspected, list):
                    pdf.cell(0, 4.5, f"  {sign_name} aspects: {', '.join(aspected)}",
                             new_x="LMARGIN", new_y="NEXT")
            pdf.ln(3)

    # ==================================================================
    # VARSHPHAL (SOLAR RETURN) (optional)
    # ==================================================================
    if varshphal_data and isinstance(varshphal_data, dict):
        current_section[0] = "Varshphal"
        pdf.add_page()
        pdf.section_title("Varshphal (Annual Chart / Solar Return)")

        vp_year = _sg(varshphal_data, "year", default="N/A")
        vp_date = _sg(varshphal_data, "solar_return_date", default="N/A")
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(0, 5, f"Year: {vp_year}  |  Solar Return Date: {_fmt_date(str(vp_date))}",
                 new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        vp_planets = varshphal_data.get("planets", {})
        if vp_planets and isinstance(vp_planets, dict):
            pdf.sub_section("Varshphal Planetary Positions")
            vpp_h = ["Planet", "Sign", "Degree", "House", "Nakshatra", "Status"]
            vpp_w = [22, 25, 18, 15, 30, 25]
            pdf.table_header(vpp_h, vpp_w)
            for idx, pname in enumerate(PLANET_LIST_9):
                vpi = vp_planets.get(pname, {})
                if isinstance(vpi, dict):
                    pdf.table_row([pname, str(vpi.get("sign", "N/A")), _fmt_num(vpi.get("degree", "N/A")),
                                  str(vpi.get("house", "N/A")), str(vpi.get("nakshatra", "N/A")),
                                  _get_dignity(pname, vpi.get("sign", ""))], vpp_w, idx)
            pdf.ln(3)

        muntha = varshphal_data.get("muntha", {})
        if muntha and isinstance(muntha, dict):
            pdf.sub_section("Muntha")
            pdf.set_font("Helvetica", "", 7.5)
            pdf.cell(0, 5, f"Muntha Sign: {muntha.get('sign', 'N/A')}  |  "
                          f"Muntha Lord: {muntha.get('lord', 'N/A')}  |  "
                          f"House: {muntha.get('house', 'N/A')}",
                     new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)

        varshesha = varshphal_data.get("varshesha", varshphal_data.get("year_lord", "N/A"))
        if varshesha != "N/A":
            pdf.sub_section("Varshesha (Year Lord)")
            pdf.set_font("Helvetica", "", 7.5)
            if isinstance(varshesha, dict):
                pdf.cell(0, 5, f"Year Lord: {varshesha.get('planet', 'N/A')}  |  "
                              f"Strength: {varshesha.get('strength', 'N/A')}",
                         new_x="LMARGIN", new_y="NEXT")
            else:
                pdf.cell(0, 5, f"Year Lord: {varshesha}", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)

        vp_pih: Dict[int, List[str]] = {}
        for vpn, vpi in vp_planets.items():
            if isinstance(vpi, dict):
                h = vpi.get("house", 1)
                vp_pih.setdefault(int(h) if isinstance(h, (int, float)) else 1, []).append(
                    PLANET_ABBR.get(vpn, vpn[:2]))
        if vp_pih:
            _draw_north_indian_chart(pdf, 55, pdf.get_y() + 2, 70, vp_pih, f"Varshphal Chart ({vp_year})")
            pdf.set_y(pdf.get_y() + 78)

    # ==================================================================
    # PLANETARY PLACEMENT INTERPRETATIONS
    # ==================================================================
    current_section[0] = "Interpretations"
    pdf.add_page()
    pdf.section_title("Planetary Placement Interpretations")

    for pname in PLANET_LIST_9:
        house = planet_houses.get(pname, 0)
        sign = planet_signs.get(pname, "Aries")
        dignity = _get_dignity(pname, sign)
        interp = _PLANET_HOUSE_BRIEF.get(pname, {}).get(house, "")
        if not interp:
            continue
        pdf.check_space(15)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*SAFFRON)
        pdf.cell(0, 5, f"{pname} in House {house} ({sign}) - {dignity}",
                 new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(*DARK)
        pdf.set_font("Helvetica", "", 7)
        pdf.set_x(15)
        pdf.multi_cell(175, 3.5, interp)
        pdf.ln(2)

    # ==================================================================
    # NAKSHATRA ANALYSIS
    # ==================================================================
    current_section[0] = "Nakshatra Analysis"
    pdf.add_page()
    pdf.section_title("Nakshatra Analysis")

    moon_nak = planets.get("Moon", {}).get("nakshatra", "")
    if moon_nak:
        pdf.sub_section(f"Birth Nakshatra (Janma): {moon_nak}")
        interp = _NAKSHATRA_BRIEF.get(moon_nak, "")
        if interp:
            pdf.set_font("Helvetica", "", 7.5)
            pdf.multi_cell(0, 4, interp)
        pdf.ln(3)

    pdf.sub_section("Planets in Nakshatras")
    for pname in PLANET_LIST_9:
        pi = planets.get(pname, {})
        if not isinstance(pi, dict):
            continue
        nak = pi.get("nakshatra", "")
        pada = pi.get("nakshatra_pada", pi.get("pada", ""))
        if not nak:
            continue
        interp = _NAKSHATRA_BRIEF.get(nak, "")
        pdf.check_space(12)
        pdf.set_font("Helvetica", "B", 7)
        pdf.set_text_color(*SAFFRON)
        pada_str = f" (Pada {pada})" if pada else ""
        pdf.cell(0, 5, f"{pname} in {nak}{pada_str}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(*DARK)
        if interp:
            pdf.set_font("Helvetica", "", 6.5)
            pdf.set_x(15)
            pdf.multi_cell(175, 3.5, interp)
            pdf.ln(1)

    # ==================================================================
    # GEMSTONE RECOMMENDATIONS
    # ==================================================================
    current_section[0] = "Gemstone Guide"
    pdf.add_page()
    pdf.section_title("Gemstone Recommendations")

    pdf.set_font("Helvetica", "I", 7)
    pdf.multi_cell(0, 3.5,
        "IMPORTANT: Gemstones should only be worn after thorough analysis by a qualified "
        "astrologer. Wearing the wrong gemstone can amplify negative effects. The following "
        "recommendations are based on planetary positions and should be verified before use.")
    pdf.ln(3)

    asc_lord = SIGN_LORD.get(asc_sign, "")
    recommended = set()
    if asc_lord:
        recommended.add(asc_lord)
    fifth_sign = SIGN_ORDER[(asc_idx + 4) % 12]
    ninth_sign = SIGN_ORDER[(asc_idx + 8) % 12]
    recommended.add(SIGN_LORD.get(fifth_sign, ""))
    recommended.add(SIGN_LORD.get(ninth_sign, ""))
    recommended.discard("")

    for pname in PLANET_LIST_9:
        gem = _GEMSTONES.get(pname, {})
        if not gem:
            continue
        pdf.check_space(22)
        is_rec = pname in recommended
        pdf.set_font("Helvetica", "B", 8)
        if is_rec:
            pdf.set_text_color(*GREEN)
            prefix = "[RECOMMENDED] "
        else:
            pdf.set_text_color(*SAFFRON)
            prefix = ""
        pdf.cell(0, 5, f"{prefix}{pname} - {gem['stone']}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(*DARK)
        pdf.set_font("Helvetica", "", 6.5)
        pdf.set_x(15)
        pdf.cell(0, 4, f"Finger: {gem['finger']}  |  Metal: {gem['metal']}  |  "
                       f"Weight: {gem['weight']}  |  Day: {gem['day']}",
                 new_x="LMARGIN", new_y="NEXT")
        pdf.set_x(15)
        pdf.set_font("Helvetica", "I", 6)
        pdf.cell(0, 4, f"Mantra: {gem['mantra']}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    # ==================================================================
    # GENERAL PREDICTIONS BY HOUSE
    # ==================================================================
    current_section[0] = "House Predictions"
    pdf.add_page()
    pdf.section_title("General Predictions by Bhava (House)")

    for bnum in range(1, 13):
        topic, desc = _HOUSE_TOPICS[bnum]
        sign = SIGN_ORDER[(asc_idx + bnum - 1) % 12]
        lord = SIGN_LORD.get(sign, "N/A")
        lord_h = planet_houses.get(lord, "N/A")
        planets_here = [pn for pn, ph in planet_houses.items() if ph == bnum]

        pdf.check_space(20)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*SAFFRON)
        pdf.cell(0, 5, f"House {bnum}: {topic} ({sign}, Lord: {lord} in House {lord_h})",
                 new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(*DARK)
        pdf.set_font("Helvetica", "", 6.5)
        pdf.set_x(12)
        pdf.multi_cell(178, 3.5, f"Significations: {desc}")
        if planets_here:
            pdf.set_font("Helvetica", "I", 6.5)
            pdf.set_x(12)
            pdf.cell(0, 4, f"Planets here: {', '.join(planets_here)}", new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.set_font("Helvetica", "I", 6.5)
            pdf.set_x(12)
            pdf.cell(0, 4, "No planets in this house.", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    # ==================================================================
    # PLANETARY AVASTHAS
    # ==================================================================
    current_section[0] = "Planetary Avasthas"
    pdf.add_page()
    pdf.section_title("Planetary Avasthas (Planetary States)")

    pdf.set_font("Helvetica", "", 7)
    pdf.multi_cell(0, 3.5,
        "Avasthas indicate the state or mood of a planet, affecting how it delivers results. "
        "The Baladi (age-based) avastha is computed from the planet's position within the sign.")
    pdf.ln(3)

    avastha_names = ["Bala (Infant)", "Kumara (Youth)", "Yuva (Adult)", "Vriddha (Old)", "Mrita (Dead)"]
    avastha_desc = [
        "Quarter strength. Planet gives limited results, like a child.",
        "Half strength. Growing results, potential not fully realized.",
        "Full strength. Planet at peak performance, best results.",
        "Minimal strength. Declining results, exhausted energy.",
        "No strength. Planet unable to deliver results effectively.",
    ]

    av_headers = ["Planet", "Sign", "Degree", "Avastha", "Strength"]
    av_widths = [22, 25, 18, 30, 30]
    pdf.table_header(av_headers, av_widths)

    for idx, pname in enumerate(PLANET_LIST_9):
        sign = planet_signs.get(pname, "Aries")
        pi = planets.get(pname, {})
        deg = pi.get("sign_degree", pi.get("degree", 0)) if isinstance(pi, dict) else 0
        try:
            deg_f = float(deg)
        except (ValueError, TypeError):
            deg_f = 0.0
        sign_num = SIGN_INDEX.get(sign, 0) + 1
        if sign_num % 2 == 1:
            av_idx = min(int(deg_f / 6), 4)
        else:
            av_idx = min(4 - int(deg_f / 6), 4)
            av_idx = max(av_idx, 0)
        avastha = avastha_names[av_idx]
        strength_pct = ["25%", "50%", "100%", "12.5%", "0%"][av_idx]
        pdf.table_row([pname, sign, _fmt_num(deg_f), avastha, strength_pct], av_widths, idx)
    pdf.ln(3)

    pdf.sub_section("Avastha Descriptions (Baladi)")
    for name, desc in zip(avastha_names, avastha_desc):
        pdf.set_font("Helvetica", "B", 7)
        pdf.cell(35, 4, name)
        pdf.set_font("Helvetica", "", 6.5)
        pdf.cell(0, 4, desc, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # Combustion
    pdf.sub_section("Combustion (Asta) Status")
    sun_lon = planet_lons.get("Sun", 0.0)
    combust_orbs = {"Moon": 12, "Mars": 17, "Mercury": 14, "Jupiter": 11, "Venus": 10, "Saturn": 15}
    comb_h = ["Planet", "Distance from Sun", "Combust Orb", "Status"]
    comb_w = [25, 35, 30, 30]
    pdf.table_header(comb_h, comb_w)
    for idx, pname in enumerate(["Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]):
        p_lon = planet_lons.get(pname, 0.0)
        dist = abs(p_lon - sun_lon)
        if dist > 180:
            dist = 360 - dist
        orb = combust_orbs.get(pname, 15)
        status = "COMBUST" if dist < orb else "Not combust"
        pdf.table_row([pname, _fmt_num(dist, 2), f"{orb} deg", status], comb_w, idx)
    pdf.ln(4)

    # Retrograde analysis
    pdf.check_space(40)
    pdf.sub_section("Retrograde Planets Analysis")
    retro_planets = [pn for pn in PLANET_LIST_7 if planet_retro.get(pn, False)]
    retro_effects = {
        "Mercury": "Communication delays, revisiting past decisions, technology issues. Good for research and revision.",
        "Venus": "Revisiting past relationships, reassessing values. Delays in romance and art purchases.",
        "Mars": "Suppressed anger, indirect action. Rethinking strategies. Past conflicts resurface for resolution.",
        "Jupiter": "Inner spiritual growth, reassessing beliefs. Delayed expansion. Wisdom from past experiences.",
        "Saturn": "Reviewing responsibilities, past karma resurfaces. Restructuring commitments. Delayed but lasting results.",
    }
    if retro_planets:
        for pname in retro_planets:
            pdf.set_font("Helvetica", "B", 7.5)
            pdf.set_text_color(*SAFFRON)
            pdf.cell(0, 5, f"{pname} (Retrograde) in {planet_signs.get(pname, 'N/A')}, House {planet_houses.get(pname, 'N/A')}",
                     new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(*DARK)
            pdf.set_font("Helvetica", "", 6.5)
            pdf.set_x(15)
            pdf.multi_cell(175, 3.5, retro_effects.get(pname, "Retrograde planet intensifies inner expression of its significations."))
            pdf.ln(1)
    else:
        pdf.set_font("Helvetica", "I", 7)
        pdf.cell(0, 5, "No retrograde planets in this chart.", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # ==================================================================
    # FINAL PAGE: DISCLAIMER + CREDITS
    # ==================================================================
    current_section[0] = "About This Report"
    pdf.add_page()
    pdf.section_title("About This Report")

    pdf.set_font("Helvetica", "", 8)
    pdf.multi_cell(0, 4,
        "This Vedic astrology report has been generated using Parashara system calculations "
        "with Lahiri (Chitrapaksha) ayanamsha. The computations include planetary positions, "
        "house cusps, divisional charts, Vimshottari and Yogini dasha systems, Shadbala "
        "(six-fold strength), Ashtakvarga, planetary aspects, yogas, and doshas.")
    pdf.ln(3)

    pdf.sub_section("Systems Used")
    for s in [
        "Parashara's Hora Shastra - primary reference",
        "Lahiri Ayanamsha (Chitrapaksha) - standard sidereal correction",
        "Sripati house system - for bhava cusps",
        "Vimshottari Dasha - 120-year planetary period system",
        "Yogini Dasha - 36-year feminine energy period system",
        "Shadbala - six-fold planetary strength analysis",
        "Ashtakvarga - eight-fold transit strength system",
        "Shodashvarga - 16 divisional chart analysis",
        "KP (Krishnamurti Paddhati) - sub lord based analysis",
        "Jaimini - chara karaka and sign-based dasha",
    ]:
        pdf.set_font("Helvetica", "", 7)
        pdf.cell(0, 4.5, f"  * {s}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.sub_section("Disclaimer")
    pdf.set_font("Helvetica", "I", 7)
    pdf.multi_cell(0, 3.5,
        "This report is generated for educational and informational purposes only. "
        "Vedic astrology is a traditional knowledge system and its predictions should not be "
        "considered as definitive or absolute. Important life decisions should be made based on "
        "rational thinking, professional advice, and personal judgment. The accuracy of this "
        "report depends on the accuracy of the birth data provided. Even a difference of a few "
        "minutes in birth time can significantly alter the chart. Please consult a qualified "
        "Vedic astrologer for personalized guidance and interpretation.")
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*SAFFRON)
    pdf.cell(0, 6, "AstroRattan.com", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)
    pdf.set_font("Helvetica", "", 7)
    pdf.cell(0, 4, "Vedic Astrology | Kundli | Panchang | Muhurta",
             align="C", new_x="LMARGIN", new_y="NEXT")

    generated_ts = datetime.now().strftime("%d %b %Y, %I:%M %p")
    pdf.ln(3)
    pdf.set_font("Helvetica", "I", 6)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 4, f"Report generated on {generated_ts}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 4, f"Total pages: {pdf.page_no()}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)

    # ══════════════════════════════════════════════════════
    return pdf.output()
