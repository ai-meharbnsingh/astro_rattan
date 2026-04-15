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
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import importlib.util

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


# ═══════════════════════════════════════════════════════════════════════════════
# STRICT LAYOUT ENGINE - Grid System with No Overlap
# ═══════════════════════════════════════════════════════════════════════════════

class GridLayout:
    """
    Strict 12-column grid system for PDF layout.
    
    Page Layout:
    - Total width: 210mm (A4)
    - Margins: 12mm left/right
    - Usable width: 186mm
    - 12 columns with 2.5mm gutters
    - Column width: ~14mm
    """
    
    # Page constants (A4)
    PAGE_WIDTH = 210.0
    PAGE_HEIGHT = 297.0
    MARGIN_LEFT = 12.0
    MARGIN_RIGHT = 12.0
    MARGIN_TOP = 12.0
    MARGIN_BOTTOM = 12.0
    
    # Grid system
    COLUMNS = 12
    GUTTER = 2.5  # mm
    
    # Spacing system (fixed values only)
    SPACE_SMALL = 3.5   # 10px equivalent
    SPACE_MEDIUM = 7.0  # 20px equivalent
    SPACE_LARGE = 10.5  # 30px equivalent
    
    def __init__(self, pdf):
        self.pdf = pdf
        self.usable_width = self.PAGE_WIDTH - self.MARGIN_LEFT - self.MARGIN_RIGHT
        self.usable_height = self.PAGE_HEIGHT - self.MARGIN_TOP - self.MARGIN_BOTTOM
        self.col_width = (self.usable_width - (self.COLUMNS - 1) * self.GUTTER) / self.COLUMNS
        
        # Track placed elements for collision detection
        self.placed_elements = []  # List of (x, y, w, h, label)
        self.current_page = 1
        
    def col_width_span(self, col_span: int) -> float:
        """Get width for N columns including gutters."""
        return col_span * self.col_width + (col_span - 1) * self.GUTTER
    
    def check_collision(self, x: float, y: float, w: float, h: float) -> bool:
        """Check if rectangle overlaps with any placed element."""
        for px, py, pw, ph, plabel in self.placed_elements:
            x_overlap = min(x + w, px + pw) - max(x, px)
            y_overlap = min(y + h, py + ph) - max(y, py)
            if x_overlap > 0.5 and y_overlap > 0.5:  # 0.5mm tolerance
                return True
        return False
    
    def place_element(self, x: float, y: float, w: float, h: float, label: str) -> bool:
        """Place element at position if no collision. Returns success."""
        if self.check_collision(x, y, w, h):
            return False
        self.placed_elements.append((x, y, w, h, label))
        return True
    
    def new_page(self):
        """Clear elements for new page."""
        self.placed_elements = []
        self.current_page += 1
    
    def get_chart_size(self, chart_type: str = "standard") -> float:
        """Get standardized chart size based on grid columns."""
        sizes = {
            "main": self.col_width_span(8),       # 8 columns - large
            "standard": self.col_width_span(4),   # 4 columns - medium
            "small": self.col_width_span(3),      # 3 columns - small
            "divisional": self.col_width_span(3), # 3 columns for D-charts
        }
        return sizes.get(chart_type, sizes["standard"])
    
    def get_divisional_grid_positions(self, num_charts: int) -> list:
        """
        Get grid positions for divisional charts (strict 4x2 layout).
        Each chart: 3 columns wide, 3 columns high (square)
        Gap: fixed 15px between charts
        """
        positions = []
        chart_w = self.get_chart_size("divisional")
        chart_h = chart_w  # Square charts
        
        # Fixed 15px gap (5.3mm)
        gap = 5.3
        
        cols = 4
        max_per_page = 8  # 4x2 grid
        
        for i in range(min(num_charts, max_per_page)):
            row = i // cols
            col = i % cols
            x = self.MARGIN_LEFT + col * (chart_w + gap)
            y = self.MARGIN_TOP + row * (chart_h + gap + 8)  # +8 for label
            positions.append((x, y, chart_w, chart_h))
        
        return positions


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


def _display(v: Any) -> str:
    """Premium display formatting for missing/placeholder values."""
    if v is None:
        return "—"
    s = str(v).strip()
    if s == "":
        return "—"
    if s.lower() in {"n/a", "na", "none", "null", "nan", "undefined"}:
        return "—"
    return s


def _sanitize(text: str) -> str:
    """Replace Unicode characters that Helvetica cannot render."""
    import re
    s = str(text)
    s = (s.replace("\u2014", " - ")
          .replace("\u2013", "-")
          .replace("\u2018", "'")
          .replace("\u2019", "'")
          .replace("\u201c", '"')
          .replace("\u201d", '"')
          .replace("\u2022", "*")
          .replace("\u2026", "...")
          .replace("\u00b0", " deg")
          .replace("\u2265", ">=")
          .replace("\u2264", "<=")
          .replace("\u2010", "-")
          .replace("\u2011", "-")
          .replace("\u2012", "-")
          .replace("\u2015", "-")
          .replace("\u00a0", " ")
          .replace("\u200b", "")
          .replace("\u200c", "")
          .replace("\u200d", "")
          .replace("\u2009", " ")
          .replace("\u202f", " ")
          .replace("\u00d7", "x")
          .replace("\u2192", "->")
          .replace("\u2190", "<-")
          .replace("\u2191", "^")
          .replace("\u2193", "v"))
    # Strip any remaining non-latin1 characters for Helvetica safety
    s = re.sub(r'[^\x00-\xff]', '', s)
    return s


def _has_meaningful(v: Any) -> bool:
    return _display(v) != "—"


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

def _draw_north_indian_chart(
    pdf,
    x: float,
    y: float,
    size: float,
    planets_in_houses: Dict[int, List[str]],
    title: str = "",
    show_house_numbers: bool = True,
):
    """Draw a North Indian diamond chart on the PDF.

    planets_in_houses: {1: ["Su","Mo"], 2: ["Ma"], ...}  (1-based house numbers)
    """
    title_band = 4.2 if title else 0.0
    cx = x
    cy = y + title_band
    csize = size - title_band
    if csize < 20:
        csize = size
        cy = y

    if title:
        pdf.set_font("Helvetica", "B", 6.4)
        pdf.set_text_color(180, 50, 20)
        tw = pdf.get_string_width(_sanitize(title))
        pdf.text(x + (size - tw) / 2, y + 2.9, _sanitize(title))
        pdf.set_text_color(40, 40, 40)

    pdf.set_draw_color(100, 80, 60)
    pdf.set_line_width(0.4)
    pdf.rect(cx, cy, csize, csize)

    mid = csize / 2.0
    pdf.line(cx, cy, cx + csize, cy + csize)
    pdf.line(cx + csize, cy, cx, cy + csize)
    pdf.line(cx + mid, cy, cx + csize, cy + mid)
    pdf.line(cx + csize, cy + mid, cx + mid, cy + csize)
    pdf.line(cx + mid, cy + csize, cx, cy + mid)
    pdf.line(cx, cy + mid, cx + mid, cy)

    if hasattr(pdf, "register_block"):
        pdf.register_block(cx, cy, csize, csize, f"Chart:{title or 'North Indian'}")

    # Per-house rectangular zones keep labels away from chart lines.
    zone = {
        1: (cx + csize * 0.38, cy + csize * 0.05, csize * 0.24, csize * 0.12),
        2: (cx + csize * 0.20, cy + csize * 0.18, csize * 0.16, csize * 0.12),
        3: (cx + csize * 0.06, cy + csize * 0.32, csize * 0.16, csize * 0.12),
        4: (cx + csize * 0.19, cy + csize * 0.46, csize * 0.16, csize * 0.12),
        5: (cx + csize * 0.11, cy + csize * 0.61, csize * 0.18, csize * 0.12),
        6: (cx + csize * 0.30, cy + csize * 0.75, csize * 0.16, csize * 0.12),
        7: (cx + csize * 0.40, cy + csize * 0.79, csize * 0.20, csize * 0.11),
        8: (cx + csize * 0.56, cy + csize * 0.75, csize * 0.16, csize * 0.12),
        9: (cx + csize * 0.71, cy + csize * 0.61, csize * 0.18, csize * 0.12),
        10: (cx + csize * 0.65, cy + csize * 0.46, csize * 0.16, csize * 0.12),
        11: (cx + csize * 0.78, cy + csize * 0.32, csize * 0.16, csize * 0.12),
        12: (cx + csize * 0.64, cy + csize * 0.18, csize * 0.16, csize * 0.12),
    }

    def _wrap_tokens(tokens: List[str], max_w: float, max_lines: int) -> List[str]:
        lines: List[str] = []
        for token in tokens:
            if not lines:
                lines.append(token)
                continue
            trial = f"{lines[-1]} {token}"
            if pdf.get_string_width(_sanitize(trial)) <= max_w:
                lines[-1] = trial
            else:
                lines.append(token)
            if len(lines) >= max_lines:
                break
        if len(tokens) > sum(len(line.split()) for line in lines):
            lines[-1] = f"{lines[-1]} +"
        return lines

    if show_house_numbers:
        pdf.set_font("Helvetica", "B", 6.3 if csize <= 60 else 7.2)
        pdf.set_text_color(85, 75, 62)
        for h_num in range(1, 13):
            zx, zy, zw, _zh = zone[h_num]
            nt = str(h_num)
            tw = pdf.get_string_width(nt)
            pdf.text(zx + 0.4, zy + 2.5, nt)
            # faint separator between number and text area
            pdf.set_draw_color(210, 200, 188)
            pdf.line(zx, zy + 3.0, zx + min(zw, tw + 2.0), zy + 3.0)
            pdf.set_draw_color(100, 80, 60)

    text_font = 5.3 if csize <= 60 else 6.2
    line_h = 2.6 if csize <= 60 else 3.0
    pdf.set_font("Helvetica", "B", text_font)
    pdf.set_text_color(40, 40, 40)

    for h_num in range(1, 13):
        items = list(planets_in_houses.get(h_num, []))
        if not items:
            continue
        if len(items) > 8:
            items = items[:8] + [f"+{len(items) - 8}"]

        zx, zy, zw, zh = zone[h_num]
        inner_x = zx + 1.0
        inner_w = max(zw - 2.0, 8.0)
        start_y = zy + (4.2 if show_house_numbers else 1.6)
        usable_h = max(zh - (4.8 if show_house_numbers else 2.0), 4.0)
        max_lines = max(1, int(usable_h / line_h))
        lines = _wrap_tokens(items, inner_w, max_lines)

        for li, line_text in enumerate(lines):
            ly = start_y + (li * line_h)
            if ly > zy + zh - 0.6:
                break
            tw = pdf.get_string_width(_sanitize(line_text))
            tx = inner_x + max((inner_w - tw) / 2, 0.0)
            pdf.text(tx, ly, _sanitize(line_text))


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
    sadesati_data = data.get("sade_sati") or data.get("sadesati") or {}
    hindu_calendar = data.get("hindu_calendar") or {}
    panchang_data = data.get("panchang") or {}

    def _module_available(modname: str) -> bool:
        return importlib.util.find_spec(modname) is not None

    def _dict_has_values(d: Any, min_count: int = 1) -> bool:
        if not isinstance(d, dict):
            return False
        c = 0
        for _k, _v in d.items():
            if isinstance(_v, dict):
                if _dict_has_values(_v, 1):
                    c += 1
            elif isinstance(_v, list):
                if len(_v) > 0:
                    c += 1
            elif _has_meaningful(_v):
                c += 1
            if c >= min_count:
                return True
        return False

    planets = chart_data.get("planets") or {}
    houses = chart_data.get("houses") or {}
    ascendant = chart_data.get("ascendant") or {}
    asc_sign = ascendant.get("sign", "Aries")
    asc_lon_raw = ascendant.get("longitude", 0.0)
    asc_degree = ascendant.get("sign_degree", ascendant.get("degree", 0.0))
    if asc_degree == 0.0 and asc_lon_raw:
        asc_degree = float(asc_lon_raw) % 30.0
    ayanamsa_val = chart_data.get("ayanamsa", ayanamsa_input)

    # Engine/data capability map for dynamic section rendering.
    capabilities: Dict[str, bool] = {
        "panchang": _dict_has_values(panchang_data, 2) or _dict_has_values(hindu_calendar, 2),
        "planetary_positions": isinstance(planets, dict) and len([p for p in planets.values() if isinstance(p, dict)]) >= 7,
        "lagna_rashi_charts": isinstance(ascendant, dict) and _has_meaningful(ascendant.get("sign")),
        "divisional_charts": _dict_has_values(sodashvarga_data, 1),
        "ashtakavarga": _dict_has_values(ashtakvarga_data, 1),
        "shadbala": _dict_has_values(shadbala_data, 1),
        "bhava_bala": _dict_has_values(shadbala_data.get("bhav_bala", {}), 1) if isinstance(shadbala_data, dict) else False,
        "avasthas": isinstance(planets, dict) and len(planets) > 0,
        "yogas_doshas": _dict_has_values(yogas_doshas, 1),
        "dasha_vimshottari": _dict_has_values(dasha_data, 1),
        "dasha_yogini": _dict_has_values(yogini_data, 1),
        "kp": _module_available("app.kp_engine") and _dict_has_values(kp_data, 1),
        "jaimini": _module_available("app.jaimini_engine") and _dict_has_values(jaimini_data, 1),
        "lal_kitab": _module_available("app.lalkitab_engine") and _dict_has_values(data.get("lal_kitab", {}), 1),
    }

    # Detect actually available divisional charts from data (no fake empty grid).
    available_vargas: List[str] = []
    _sv_by_sign_probe = sodashvarga_data.get("by_sign", {}) if isinstance(sodashvarga_data, dict) else {}
    _sv_vt_probe = sodashvarga_data.get("varga_table", []) if isinstance(sodashvarga_data, dict) else []
    _sv_vt_probe_map: Dict[int, dict] = {}
    for _e in _sv_vt_probe:
        if isinstance(_e, dict):
            _sv_vt_probe_map[_e.get("division", 0)] = _e.get("planets", {})
    for vk in VARGA_NAMES.keys():
        if vk == "D1":
            if capabilities["planetary_positions"]:
                available_vargas.append(vk)
            continue
        div_num = int(vk.replace("D", ""))
        found_any = False
        for pn in PLANET_LIST_9:
            p_sv = _sv_by_sign_probe.get(pn, {})
            if isinstance(p_sv, dict):
                div_info = p_sv.get(str(div_num), p_sv.get(vk.replace("D", ""), {}))
                if isinstance(div_info, dict) and _has_meaningful(div_info.get("sign")):
                    found_any = True
                    break
            vt_p = _sv_vt_probe_map.get(div_num, {}).get(pn, {})
            if isinstance(vt_p, dict) and _has_meaningful(vt_p.get("sign")):
                found_any = True
                break
        if found_any:
            available_vargas.append(vk)
    if not available_vargas and capabilities["planetary_positions"]:
        available_vargas = ["D1", "D9"]

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
            self._last_section_title = ""
            self._table_ctx: Optional[Dict[str, Any]] = None
            self._blocks_by_page: Dict[int, List[Tuple[float, float, float, float, str]]] = {}
            self.layout_warnings: List[str] = []
            self._page_kind: Dict[int, str] = {}
            self._page_fill: Dict[int, float] = {}
            self._underfilled_pages: List[Tuple[int, str, float]] = []
            self.grid: Optional[GridLayout] = None

        def _infer_page_kind(self, section: str) -> str:
            s = (section or "").lower()
            if any(k in s for k in ["birth chart", "divisional", "bhava chart", "varshphal", "sarvashtakvarga"]):
                return "chart-heavy"
            if any(k in s for k in ["dasha", "aspects", "friendship", "shadbala", "ashtakvarga"]):
                return "table-heavy"
            if any(k in s for k in ["interpretations", "analysis", "predictions", "about"]):
                return "text-heavy"
            return "mixed"

        def _min_fill_for_kind(self, kind: str) -> float:
            if kind == "chart-heavy":
                return 0.68
            if kind == "table-heavy":
                return 0.62
            if kind == "mixed":
                return 0.58
            return 0.48

        def _page_fill_ratio(self, page: int) -> float:
            blocks = self._blocks_by_page.get(page, [])
            if not blocks:
                return 0.0
            left = self.l_margin
            right = self.w - self.r_margin
            top = 12.0
            bottom = self.h - 12.0
            sx, sy = 56, 84
            hit = 0
            total = sx * sy
            dx = (right - left) / sx
            dy = (bottom - top) / sy
            for iy in range(sy):
                py = top + (iy + 0.5) * dy
                for ix in range(sx):
                    px = left + (ix + 0.5) * dx
                    inside = False
                    for bx, by, bw, bh, _bl in blocks:
                        if bx <= px <= (bx + bw) and by <= py <= (by + bh):
                            inside = True
                            break
                    if inside:
                        hit += 1
            return hit / total

        def _finalize_page(self, page: int):
            if page <= 0:
                return
            kind = self._page_kind.get(page, "mixed")
            fill = self._page_fill_ratio(page)
            self._page_fill[page] = fill
            if fill < self._min_fill_for_kind(kind):
                self._underfilled_pages.append((page, kind, fill))

        def finalize_composition(self):
            self._finalize_page(self.page_no())

        def add_page(self, *args, **kwargs):
            prev = self.page_no()
            if prev > 0:
                self._finalize_page(prev)
            res = super().add_page(*args, **kwargs)
            self._page_kind[self.page_no()] = self._infer_page_kind(current_section[0])
            return res

        def cell(self, w=0, h=0, txt="", *a, **kw):
            kw.pop("_raw", None)
            # Always sanitize — even with Hindi font, Helvetica sections need it
            return super().cell(w, h, _sanitize(_display(txt)), *a, **kw)

        def multi_cell(self, w, h=0, txt="", *a, **kw):
            return super().multi_cell(w, h, _sanitize(_display(txt)), *a, **kw)

        def header(self):
            self.set_y(7.0)
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(*SAFFRON)
            super().cell(68, 4.2, _sanitize(person_name), align="L")
            if self._has_hindi:
                self.set_font("Hindi", "", 8.5)
                super().cell(68, 4.2, "\u0950", align="C")
            else:
                self.set_font("Helvetica", "B", 8.5)
                super().cell(68, 4.2, "Om", align="C")
            self.set_font("Helvetica", "B", 8)
            super().cell(68, 4.2, _sanitize(current_section[0]), align="R")
            self.ln(4.5)
            self.set_draw_color(*GOLD_LINE)
            self.set_line_width(0.35)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(2.4)
            self.set_draw_color(0, 0, 0)
            self.set_text_color(*DARK)

        def footer(self):
            self.set_y(-10.5)
            self.set_font("Helvetica", "I", 5.8)
            self.set_text_color(*MUTED)
            super().cell(120, 4, "AstroRattan.com  |  Vedic Astrology Report", align="L")
            super().cell(70, 4, f"HP2 * {self.page_no()}", align="R")
            self.set_text_color(*DARK)

        def section_title(self, title: str):
            # Keep section heading with at least some following content.
            if self.get_y() + 14 > self.h - 12:
                self.add_page()
            if self._last_section_title == title:
                return
            self._last_section_title = title
            y0 = self.get_y()
            self.set_font("Helvetica", "B", 8.6)
            self.set_fill_color(*HEADER_BG)
            self.set_text_color(*WHITE)
            self.cell(0, 4.8, f"  {title}", fill=True,
                      new_x="LMARGIN", new_y="NEXT")
            self.register_block(self.l_margin, y0, self.w - (self.l_margin + self.r_margin), 4.8, f"Section:{title}")
            self.set_text_color(*DARK)
            self.ln(0.7)

        def sub_section(self, title: str):
            if self.get_y() + 9 > self.h - 12:
                self.add_page()
            y0 = self.get_y()
            self.set_font("Helvetica", "B", 7.7)
            self.set_text_color(*SAFFRON)
            self.cell(0, 4.0, title, new_x="LMARGIN", new_y="NEXT")
            self.register_block(self.l_margin, y0, self.w - (self.l_margin + self.r_margin), 4.0, f"Subsection:{title}")
            self.set_text_color(*DARK)
            self.ln(0.3)

        def gold_line(self):
            self.set_draw_color(*GOLD_LINE)
            self.set_line_width(0.3)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(1.3)
            self.set_draw_color(0, 0, 0)

        def table_header(self, cols: list, widths: list, font_size: float = 7):
            y0 = self.get_y()
            self.set_font("Helvetica", "B", font_size)
            self.set_fill_color(*GOLD_LIGHT)
            self.set_text_color(*DARK)
            for i, h in enumerate(cols):
                self.cell(widths[i], 4.0, _sanitize(_display(h)),
                          border=1, align="C", fill=True)
            self.ln()
            self.register_block(self.get_x(), y0, sum(widths), 4.0, "TableHeader")
            self._table_ctx = {
                "cols": list(cols),
                "widths": list(widths),
                "font_size": font_size,
                "header_h": 4.0,
            }

        def table_row(self, vals: list, widths: list, row_idx: int = 0,
                      font_size: float = 6.5, aligns: Optional[list] = None,
                      row_h: float = 3.6):
            vals_disp = [_display(v) for v in vals]
            if all(v == "—" or v == "" for v in vals_disp):
                return
            if self.get_y() + row_h > self.h - 12:
                self.add_page()
                if self._table_ctx and self._table_ctx.get("widths") == list(widths):
                    self.table_header(
                        self._table_ctx["cols"],
                        self._table_ctx["widths"],
                        self._table_ctx["font_size"],
                    )
            self.set_font("Helvetica", "", font_size)
            fill = row_idx % 2 == 1
            if fill:
                self.set_fill_color(*ALT_ROW)
            y0 = self.get_y()
            x0 = self.get_x()
            for i, v in enumerate(vals_disp):
                a = "C" if aligns is None else aligns[i]
                self.cell(widths[i], row_h, _sanitize(v),
                          border=1, align=a, fill=fill)
            self.ln()
            self.register_block(x0, y0, sum(widths), row_h, "TableRow")

        def kv_row(self, label: str, value: str, lw: float = 50, vw: float = 45):
            x0 = self.get_x()
            y0 = self.get_y()
            self.set_font("Helvetica", "B", 6.2)
            self.cell(lw, 3.2, _sanitize(_display(label) + ":"))
            self.set_font("Helvetica", "", 6.2)
            self.cell(vw, 3.2, _sanitize(_display(value)))
            self.register_block(x0, y0, lw + vw, 3.2, "KVRow")

        def check_space(self, needed: float = 30):
            if self.get_y() + needed > self.h - 12:
                self.add_page()
                self._last_section_title = ""

        def register_block(self, x: float, y: float, w: float, h: float, label: str):
            page = self.page_no()
            # Keep validator practical: report only meaningful print-bound violations (>2mm).
            left_bound = self.l_margin - 2.0
            right_bound = self.w - self.r_margin + 2.0
            top_bound = 10.0
            bottom_bound = self.h - 10.0
            chart_scope = label.startswith("Chart:")
            if chart_scope and (x < left_bound or y < top_bound or (x + w) > right_bound or (y + h) > bottom_bound):
                self.layout_warnings.append(f"{label} out of bounds on page {page}")
            page_blocks = self._blocks_by_page.setdefault(page, [])
            for bx, by, bw, bh, bl in page_blocks:
                x_overlap = min(x + w, bx + bw) - max(x, bx)
                y_overlap = min(y + h, by + bh) - max(y, by)
                chart_overlap_scope = chart_scope or bl.startswith("Chart:")
                if chart_overlap_scope and x_overlap > 2.0 and y_overlap > 2.0:
                    self.layout_warnings.append(
                        f"{label} overlaps {bl} on page {page}"
                    )
            page_blocks.append((x, y, w, h, label))

    # ══════════════════════════════════════════════════════
    # Create PDF
    # ══════════════════════════════════════════════════════

    pdf = ReportPDF()
    # A4 portrait with print-safe margins and fixed footer reserve
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.set_margins(12, 12, 12)

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
        ("Ishtkaal", _sg(chart_data, "ishtkaal", default="N/A")),
        ("Place of Birth", birth_place),
        ("Country", _sg(chart_data, "country", default="India")),
        ("Latitude", _fmt_num(latitude, 4)),
        ("Longitude", _fmt_num(longitude, 4)),
        ("Time Zone", _sg(chart_data, "timezone", default="+05:30")),
        ("War/daylight Corr.", _sg(chart_data, "war_daylight_correction", default="00:00:00 hrs")),
        ("GMT at Birth", _sg(chart_data, "gmt_at_birth", default="N/A")),
        ("LMT Correction", _sg(chart_data, "lmt_correction", default="N/A")),
        ("Local Mean Time", _sg(chart_data, "local_mean_time", default="N/A")),
        ("Sidereal Time", _sg(chart_data, "sidereal_time", default="N/A")),
        ("Sunsign (Western)", _sg(avakhada, "sun_sign", default="N/A")),
        ("Ayanamsha", str(ayanamsa_val)),
        ("Ascendant (Lagna)", f"{asc_sign} {_fmt_num(asc_degree)}"),
    ]
    for label, val in birth_items:
        if not _has_meaningful(val):
            continue
        pdf.set_x(left_x)
        pdf.kv_row(label, str(val), 42, 50)
        pdf.ln()

    pdf.ln(0.8)
    pdf.set_x(left_x)
    pdf.sub_section("Family Particulars")
    for label in ["Grand Father", "Father", "Mother", "Caste", "Gotra"]:
        v = _sg(data, "family", label.lower().replace(" ", "_"), default="")
        if not _has_meaningful(v):
            continue
        pdf.set_x(left_x)
        pdf.kv_row(label, str(v), 42, 50)
        pdf.ln()

    pdf.ln(0.8)
    pdf.set_x(left_x)
    pdf.sub_section("Tamil Calendar")
    _hc = hindu_calendar
    for label, val in [
        ("Tamil Year", _sg(_hc, "tamil_year", default="ATCHAYA")),
        ("Tamil Month", _sg(_hc, "tamil_month", default="AANI")),
        ("Tamil Weekday", _sg(_hc, "tamil_weekday", default="N/A")),
        ("Tamil Date", _sg(_hc, "tamil_date", default="N/A")),
    ]:
        if not _has_meaningful(val):
            continue
        pdf.set_x(left_x)
        pdf.kv_row(label, str(val), 42, 50)
        pdf.ln()
    left_end_y = pdf.get_y()

    # Right: Hindu Calendar
    pdf.set_xy(right_x, col_start_y)
    pdf.sub_section("Hindu Calendar")

    # Hindu calendar: prefer panchang engine data, fall back to avakhada
    _hc = hindu_calendar  # from panchang_engine -> hindu_calendar
    _pc = panchang_data   # full panchang output
    hindu_items = [
        ("Chaitradi System", ""),
        ("Vikram Samvat", _sg(_hc, "vikram_samvat", default=_sg(avakhada, "vikram_samvat", default="N/A"))),
        ("Lunar Month", _sg(_hc, "maas", default=_sg(avakhada, "lunar_month", default="N/A"))),
        ("Kartikadi System", ""),
        ("Vikram Samvat ", _sg(_hc, "vikram_samvat_kartikadi", default="N/A")),
        ("Lunar Month ", _sg(_hc, "maas_kartikadi", default="N/A")),
        ("Saka Samvat", _sg(_hc, "shaka_samvat", default=_sg(_hc, "saka_samvat", default=_sg(avakhada, "saka_samvat", default="N/A")))),
        ("Sun's Ayana", _sg(_hc, "ayana", default=_sg(avakhada, "ayana", default="N/A"))),
        ("Season (Ritu)", _sg(_hc, "ritu", default=_sg(_hc, "ritu_english", default=_sg(avakhada, "ritu", default="N/A")))),
        ("Paksha", _sg(_hc, "paksha", default=_sg(_pc, "tithi", "paksha", default=_sg(avakhada, "paksha", default="N/A")))),
        ("Hindu Weekday", _sg(_pc, "vaar", "name", default=_sg(avakhada, "weekday", default=day_of_week))),
        ("Tithi at sunrise", _sg(_pc, "tithi", "name", default=_sg(avakhada, "tithi", default="N/A"))),
        ("Tithi ending time", _sg(_pc, "tithi", "end_time", default="N/A")),
        ("Tithi at birth", _sg(_pc, "tithi", "at_birth", default=_sg(_pc, "tithi", "name", default="N/A"))),
        ("Nak. At sunrise", _sg(_pc, "nakshatra", "name", default=_sg(avakhada, "nakshatra", default="N/A"))),
        ("Nak. ending time", _sg(_pc, "nakshatra", "end_time", default="N/A")),
        ("Nak. at birth", _sg(_pc, "nakshatra", "at_birth", default=_sg(_pc, "nakshatra", "name", default="N/A"))),
        ("Yoga at sunrise", _sg(_pc, "yoga", "name", default=_sg(avakhada, "yoga", default="N/A"))),
        ("Yoga ending time", _sg(_pc, "yoga", "end_time", default="N/A")),
        ("Yoga at birth", _sg(_pc, "yoga", "at_birth", default=_sg(_pc, "yoga", "name", default="N/A"))),
        ("Karana at sunrise", _sg(_pc, "karana", "name", default=_sg(avakhada, "karana", default="N/A"))),
        ("Karana ending time", _sg(_pc, "karana", "end_time", default="N/A")),
        ("Karana at birth", _sg(_pc, "karana", "at_birth", default=_sg(_pc, "karana", "name", default="N/A"))),
        ("Sunrise", _sg(_pc, "sunrise", default=_sg(avakhada, "sunrise", default="N/A"))),
        ("Sunset", _sg(_pc, "sunset", default=_sg(avakhada, "sunset", default="N/A"))),
        ("Moon Nak. entry", _sg(_pc, "nakshatra", "entry_time", default="N/A")),
        ("Moon Nak. exit", _sg(_pc, "nakshatra", "exit_time", default="N/A")),
        ("Bhayat", _sg(_pc, "bhayat", default="N/A")),
        ("Bhabhog", _sg(_pc, "bhabhog", default="N/A")),
        ("Dasha at Birth", _sg(dasha_data, "current_dasha", default="N/A")),
        ("Balance of Dasha", _sg(dasha_data, "balance", default="N/A")),
        ("Ayanamsha", str(ayanamsa_val)),
    ]
    for label, val in hindu_items:
        if label.strip() and not _has_meaningful(val):
            continue
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
        if not _has_meaningful(v1):
            continue
        pdf.kv_row(l1, v1, 38, 50)
        if i + 1 < len(avk_items):
            l2, v2 = avk_items[i + 1]
            if _has_meaningful(v2):
                pdf.kv_row(l2, v2, 38, 50)
        pdf.ln()
    pdf.ln(3)

    # Dasha at birth summary
    if capabilities["dasha_vimshottari"]:
        pdf.sub_section("Dasha at Birth")
        pdf.set_font("Helvetica", "", 7)
        pdf.kv_row("Current Mahadasha", str(_sg(dasha_data, "current_dasha", default="N/A")), 42, 50)
        pdf.ln()
        pdf.kv_row("Balance of Dasha", str(_sg(dasha_data, "balance", default="N/A")), 42, 50)
        pdf.ln(2)

    # Compact filler to avoid underfilled first page while keeping data unchanged.
    pdf.check_space(44)
    pdf.sub_section("Quick Planet Snapshot")
    q_headers = ["Planet", "Sign", "House", "Planet", "Sign", "House"]
    q_widths = [20, 24, 12, 20, 24, 12]
    pdf.table_header(q_headers, q_widths, font_size=6.0)
    q_planets = PLANET_LIST_9
    for i in range(0, len(q_planets), 2):
        p1 = q_planets[i]
        p1i = planets.get(p1, {}) if isinstance(planets.get(p1), dict) else {}
        row = [p1, p1i.get("sign", "N/A"), str(p1i.get("house", "N/A"))]
        if i + 1 < len(q_planets):
            p2 = q_planets[i + 1]
            p2i = planets.get(p2, {}) if isinstance(planets.get(p2), dict) else {}
            row += [p2, p2i.get("sign", "N/A"), str(p2i.get("house", "N/A"))]
        else:
            row += ["", "", ""]
        pdf.table_row(row, q_widths, i // 2, font_size=5.9)
    pdf.ln(1.0)

    pdf.sub_section("Core Indicators")
    core_headers = ["Metric", "Value", "Metric", "Value"]
    core_widths = [34, 56, 34, 56]
    pdf.table_header(core_headers, core_widths, font_size=6.0)
    moon_sign = planets.get("Moon", {}).get("sign", "N/A") if isinstance(planets.get("Moon"), dict) else "N/A"
    sun_sign = planets.get("Sun", {}).get("sign", "N/A") if isinstance(planets.get("Sun"), dict) else "N/A"
    moon_nak = planets.get("Moon", {}).get("nakshatra", "N/A") if isinstance(planets.get("Moon"), dict) else "N/A"
    rows_core = [
        ["Ascendant", f"{asc_sign} {_fmt_num(asc_degree)}", "Moon Sign", moon_sign],
        ["Sun Sign (Sidereal)", sun_sign, "Moon Nakshatra", moon_nak],
        ["Current Mahadasha", _sg(dasha_data, "current_dasha", default="N/A"),
         "Dasha Balance", _sg(dasha_data, "balance", default="N/A")],
    ]
    for idx, r in enumerate(rows_core):
        pdf.table_row(r, core_widths, idx, font_size=5.9, aligns=["L", "L", "L", "L"])
    pdf.ln(1.2)

    # ==================================================================
    # PAGE 2: BIRTH CHART + PLANET TABLE
    # ==================================================================
    current_section[0] = "Birth Chart"
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 8.0)
    pdf.set_text_color(*DARK)
    birth_line = f"{birth_date_display} • {day_of_week} • {birth_time} hrs • {birth_place}"
    pdf.set_fill_color(*GOLD_LIGHT)
    band_y = pdf.get_y()
    pdf.cell(0, 6.4, _sanitize(birth_line), align="C", fill=True,
             new_x="LMARGIN", new_y="NEXT")
    pdf.register_block(pdf.l_margin, band_y, pdf.w - (pdf.l_margin + pdf.r_margin), 6.4, "Birth Band")
    pdf.ln(1.6)

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

    chart_top = pdf.get_y()
    content_x = pdf.l_margin
    content_w = pdf.w - (pdf.l_margin + pdf.r_margin)
    reserve_table_h = 62.0
    bottom_limit = pdf.h - 12.0
    available_h = max(90.0, bottom_limit - chart_top - reserve_table_h)
    gap = 5.0
    large_size = min(88.0, max(70.0, available_h * 0.62))
    small_size = min(56.0, max(46.0, available_h - large_size - gap))
    while chart_top + large_size + gap + small_size > bottom_limit - reserve_table_h and large_size > 68 and small_size > 42:
        large_size -= 2.0
        small_size -= 1.0

    large_x = content_x + (content_w - large_size) / 2.0
    large_y = chart_top
    small_y = large_y + large_size + gap
    small_left_x = content_x + 2.0
    small_right_x = content_x + content_w - small_size - 2.0

    _draw_north_indian_chart(pdf, large_x, large_y, large_size, pih_lagna, "Lagna Chart (D1)")
    _draw_north_indian_chart(pdf, small_left_x, small_y, small_size, pih_moon, "Moon Chart (Chandra)")
    _draw_north_indian_chart(pdf, small_right_x, small_y, small_size, navamsha_planets, "Navamsha (D9)")
    pdf.set_y(small_y + small_size + 4.0)

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
    # BHAVA CHART + BHAVA SPASHTA + LORDSHIPS
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
    placidus_cusps = chart_data.get("placidus_cusps", [])

    def _lon_to_sign_deg(lon: float) -> str:
        """Convert longitude to Sign DD:MM format."""
        lon = lon % 360.0
        sign_idx_v = int(lon / 30) % 12
        deg_in_sign = lon % 30
        deg_whole = int(deg_in_sign)
        mins = int((deg_in_sign - deg_whole) * 60)
        return f"{SIGN_SHORT[sign_idx_v]} {deg_whole:02d}:{mins:02d}"

    for bnum in range(1, 13):
        sign = SIGN_ORDER[(asc_idx + bnum - 1) % 12]
        lord = SIGN_LORD.get(sign, "N/A")

        if placidus_cusps and len(placidus_cusps) == 12:
            # Use placidus cusps for accurate Madhya; compute Arambha/Antya as midpoints
            cusp_lon = float(placidus_cusps[bnum - 1])
            prev_cusp = float(placidus_cusps[(bnum - 2) % 12])
            next_cusp = float(placidus_cusps[bnum % 12])
            # Arambha = midpoint of previous cusp and this cusp
            arambha = (prev_cusp + cusp_lon) / 2.0
            if abs(prev_cusp - cusp_lon) > 180:
                arambha = ((prev_cusp + cusp_lon + 360) / 2.0) % 360
            # Antya = midpoint of this cusp and next cusp
            antya = (cusp_lon + next_cusp) / 2.0
            if abs(cusp_lon - next_cusp) > 180:
                antya = ((cusp_lon + next_cusp + 360) / 2.0) % 360
            begin = _lon_to_sign_deg(arambha)
            middle = _lon_to_sign_deg(cusp_lon)
            end = _lon_to_sign_deg(antya)
            # Update sign from actual cusp longitude
            sign = SIGN_ORDER[int(cusp_lon / 30) % 12]
            lord = SIGN_LORD.get(sign, "N/A")
        elif bnum <= len(houses_list) and isinstance(houses_list[bnum - 1], dict):
            h_info = houses_list[bnum - 1]
            begin = _fmt_num(h_info.get("begin", h_info.get("start", "N/A")))
            middle = _fmt_num(h_info.get("middle", h_info.get("cusp", "N/A")))
            end = _fmt_num(h_info.get("end", "N/A"))
        else:
            cusp_lon = (asc_idx * 30 + asc_degree + (bnum - 1) * 30) % 360
            begin = _lon_to_sign_deg(cusp_lon - 15)
            middle = _lon_to_sign_deg(cusp_lon)
            end = _lon_to_sign_deg(cusp_lon + 15)
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
        """
        Draw divisional charts page using strict 4x2 grid layout.
        
        Layout Rules:
        - 4 columns × 2 rows = 8 charts per page
        - Uniform chart sizing (3 grid columns each)
        - Fixed 15px gap between charts
        - No absolute positioning - grid-based placement
        """
        current_section[0] = page_title
        pdf.add_page()
        
        # Initialize grid layout for this page
        grid = GridLayout(pdf)
        grid.new_page()
        
        pdf.section_title(page_title)
        
        # Get standardized chart positions from grid
        positions = grid.get_divisional_grid_positions(len(varga_keys))
        chart_w = grid.get_chart_size("divisional")
        
        # Sodashvarga data lookups
        _dv_by_sign = sodashvarga_data.get("by_sign", {})
        _dv_varga_table = sodashvarga_data.get("varga_table", [])
        _dv_vt_map: Dict[int, dict] = {}
        for vt_entry in _dv_varga_table:
            if isinstance(vt_entry, dict):
                _dv_vt_map[vt_entry.get("division", 0)] = vt_entry.get("planets", {})

        last_chart_bottom_y = pdf.get_y()

        for ci, vk in enumerate(varga_keys):
            # Get grid position
            if ci < len(positions):
                cx, cy, chart_w, chart_h = positions[ci]
            else:
                # Need new page if more than 8 charts
                pdf.add_page()
                pdf.section_title(page_title + " (cont.)")
                grid.new_page()
                positions = grid.get_divisional_grid_positions(len(varga_keys) - ci)
                cx, cy, chart_w, chart_h = positions[0]

            # Collision detection - verify position is available
            if grid.check_collision(cx, cy, chart_w, chart_h):
                # Find next available row
                cy += chart_h + grid.SPACE_MEDIUM
            
            # Place element in grid
            grid.place_element(cx, cy, chart_w, chart_h, f"chart_{vk}")

            varga_planets: Dict[int, List[str]] = {}
            div_num_str = vk.replace("D", "")
            div_num = int(div_num_str)

            if vk == "D1":
                # Always use main chart for D1
                varga_planets = _build_planets_in_houses(planets, 1)
            else:
                # Try sodashvarga engine data
                # by_sign gives us {planet: {div: {sign, dignity}}}
                # We need to convert sign to house number (1-based from Aries)
                for pn in PLANET_LIST_9:
                    p_sv = _dv_by_sign.get(pn, {})
                    div_info = p_sv.get(div_num_str, p_sv.get(str(div_num), {})) if isinstance(p_sv, dict) else {}
                    sign_name = ""
                    if isinstance(div_info, dict):
                        sign_name = div_info.get("sign", "")
                    # Fallback: varga_table
                    if not sign_name and div_num in _dv_vt_map:
                        vt_p = _dv_vt_map[div_num].get(pn, {})
                        if isinstance(vt_p, dict):
                            sign_name = vt_p.get("sign", "")
                    if sign_name and sign_name in SIGN_INDEX:
                        h = SIGN_INDEX[sign_name] + 1  # 1-based house
                        abbr = PLANET_ABBR.get(pn, pn[:2])
                        varga_planets.setdefault(h, []).append(abbr)

            _draw_north_indian_chart(pdf, cx, cy, chart_w, varga_planets,
                                      f"{vk}: {VARGA_NAMES.get(vk, vk)}")
            last_chart_bottom_y = max(last_chart_bottom_y, cy + chart_w + grid.SPACE_SMALL)

        pdf.set_y(last_chart_bottom_y + 2)

        # Compact filler: quick snapshot table to avoid half-empty varga pages
        pdf.check_space(40)
        pdf.sub_section("Varga Snapshot (Sign Occupancy)")
        snap_headers = ["Planet"] + [vk.replace("D", "") for vk in varga_keys]
        snap_widths = [20] + [20] * len(varga_keys)
        pdf.table_header(snap_headers, snap_widths, font_size=5.5)
        for idx, pname in enumerate(PLANET_LIST_7):
            row = [PLANET_ABBR.get(pname, pname[:2])]
            for vk in varga_keys:
                div_num = int(vk.replace("D", ""))
                sign_name = ""
                p_sv = _dv_by_sign.get(pname, {})
                if isinstance(p_sv, dict):
                    div_info = p_sv.get(str(div_num), p_sv.get(vk.replace("D", ""), {}))
                    if isinstance(div_info, dict):
                        sign_name = div_info.get("sign", "")
                if not sign_name and div_num in _dv_vt_map:
                    vt_p = _dv_vt_map[div_num].get(pname, {})
                    if isinstance(vt_p, dict):
                        sign_name = vt_p.get("sign", "")
                if not sign_name and vk == "D1":
                    sign_name = planet_signs.get(pname, "")
                row.append(SIGN_SHORT[SIGN_INDEX[sign_name]] if sign_name in SIGN_INDEX else "N/A")
            pdf.table_row(row, snap_widths, idx, font_size=5.5)

        # Secondary compact table to keep divisional pages dense and useful.
        pdf.check_space(28)
        pdf.sub_section("Varga Dignity Snapshot")
        dig_headers = ["Planet"] + [vk.replace("D", "") for vk in varga_keys]
        dig_widths = [20] + [20] * len(varga_keys)
        pdf.table_header(dig_headers, dig_widths, font_size=5.4)
        dig_abbr = {"Exalted": "Ex", "Debilitated": "Db", "Own Sign": "Own",
                    "Moolatrikona": "MT", "Friend": "Fr", "Enemy": "En", "Neutral": "Nt"}
        for idx, pname in enumerate(PLANET_LIST_7):
            row = [PLANET_ABBR.get(pname, pname[:2])]
            for vk in varga_keys:
                div_num = int(vk.replace("D", ""))
                p_sv = _dv_by_sign.get(pname, {})
                dval = ""
                if isinstance(p_sv, dict):
                    di = p_sv.get(str(div_num), p_sv.get(vk.replace("D", ""), {}))
                    if isinstance(di, dict):
                        dval = di.get("dignity", "")
                if not dval and div_num in _dv_vt_map:
                    vtp = _dv_vt_map[div_num].get(pname, {})
                    if isinstance(vtp, dict):
                        dval = vtp.get("dignity", "")
                if not dval and vk == "D1":
                    dval = _get_dignity(pname, planet_signs.get(pname, "Aries"))
                row.append(dig_abbr.get(dval, dval[:3] if dval else "—"))
            pdf.table_row(row, dig_widths, idx, font_size=5.3)

    if capabilities["divisional_charts"] or len(available_vargas) > 0:
        first_chunk = available_vargas[:8]
        second_chunk = available_vargas[8:16]
        if first_chunk:
            _draw_varga_page(first_chunk, "Divisional Charts (Shodashvarga) I")
        if second_chunk:
            _draw_varga_page(second_chunk, "Divisional Charts (Shodashvarga) II")

    # ==================================================================
    # PLANETARY FRIENDSHIP
    # ==================================================================
    current_section[0] = "Planetary Friendship"
    pdf.check_space(50)
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
    # SHODASHVARGA SUMMARY
    # ==================================================================
    current_section[0] = "Shodashvarga Summary"
    pdf.check_space(50)
    pdf.section_title("Shodashvarga Summary")

    # Signs in each varga — read from sodashvarga_data["by_sign"] or varga_table
    pdf.sub_section("Signs Occupied in 16 Divisional Charts")
    all_vargas = list(VARGA_NAMES.keys())  # ["D1", "D2", ...]
    sv_cw = 10
    sv_headers = ["Planet"] + [v.replace("D", "") for v in all_vargas]
    sv_widths = [18] + [sv_cw] * len(all_vargas)
    pdf.table_header(sv_headers, sv_widths, font_size=5.5)

    # Build lookup: varga_table indexed by division number for easy access
    _sv_by_sign = sodashvarga_data.get("by_sign", {})
    _sv_varga_table = sodashvarga_data.get("varga_table", [])
    _sv_vt_map: Dict[int, dict] = {}
    for vt_entry in _sv_varga_table:
        if isinstance(vt_entry, dict):
            _sv_vt_map[vt_entry.get("division", 0)] = vt_entry.get("planets", {})

    for idx, pname in enumerate(PLANET_LIST_9):
        row_vals = [PLANET_ABBR.get(pname, pname[:2])]
        for vk in all_vargas:
            div_num_str = vk.replace("D", "")  # "D1" -> "1"
            div_num = int(div_num_str)
            sign_found = ""
            # Try by_sign first: by_sign[planet][str(division)] = {sign, dignity}
            p_sv = _sv_by_sign.get(pname, {})
            if isinstance(p_sv, dict):
                div_info = p_sv.get(div_num_str, p_sv.get(str(div_num), {}))
                if isinstance(div_info, dict):
                    sign_found = div_info.get("sign", "")
            # Fallback: varga_table
            if not sign_found and div_num in _sv_vt_map:
                vt_planets = _sv_vt_map[div_num]
                vt_p = vt_planets.get(pname, {})
                if isinstance(vt_p, dict):
                    sign_found = vt_p.get("sign", "")
            # Fallback for D1: use main chart
            if not sign_found and vk == "D1":
                sign_found = planet_signs.get(pname, "")
            row_vals.append(SIGN_SHORT[SIGN_INDEX[sign_found]] if sign_found in SIGN_INDEX else "N/A")
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
            div_num_str = vk.replace("D", "")
            div_num = int(div_num_str)
            sign_found = ""
            dignity_found = ""
            p_sv = _sv_by_sign.get(pname, {})
            if isinstance(p_sv, dict):
                div_info = p_sv.get(div_num_str, p_sv.get(str(div_num), {}))
                if isinstance(div_info, dict):
                    sign_found = div_info.get("sign", "")
                    dignity_found = div_info.get("dignity", "")
            if not sign_found and div_num in _sv_vt_map:
                vt_p = _sv_vt_map[div_num].get(pname, {})
                if isinstance(vt_p, dict):
                    sign_found = vt_p.get("sign", "")
                    dignity_found = vt_p.get("dignity", "")
            if not sign_found and vk == "D1":
                sign_found = planet_signs.get(pname, "")
            if sign_found and not dignity_found:
                dignity_found = _get_dignity(pname, sign_found)
            row_vals.append(dig_abbr.get(dignity_found, dignity_found[:3] if dignity_found else "N/A"))
        pdf.table_row(row_vals, dig_widths, idx, font_size=5.5)
    pdf.ln(4)

    # Vimshopaka Bala — from sodashvarga_data["by_planet"][planet]
    pdf.sub_section("Vimshopaka Bala")
    vim_headers = ["Planet", "Shadavarga", "Saptavarga", "Dashavarga", "Shodashavarga"]
    vim_widths = [30, 38, 38, 38, 38]
    pdf.table_header(vim_headers, vim_widths)
    _sv_by_planet = sodashvarga_data.get("by_planet", {})
    vimshopaka = sodashvarga_data.get("vimshopaka", {})
    for idx, pname in enumerate(PLANET_LIST_7):
        pv = _sv_by_planet.get(pname, vimshopaka.get(pname, {}))
        if isinstance(pv, dict):
            row = [pname,
                   _fmt_num(pv.get("shadavarga", pv.get("vimshopak_bala", "N/A"))),
                   _fmt_num(pv.get("saptavarga", "N/A")),
                   _fmt_num(pv.get("dashavarga", "N/A")),
                   _fmt_num(pv.get("shodashavarga", pv.get("vimshopak_bala", "N/A")))]
        else:
            row = [pname, "N/A", "N/A", "N/A", "N/A"]
        pdf.table_row(row, vim_widths, idx)
    pdf.ln(4)

    # ==================================================================
    # SHAD BALA + BHAVA BALA
    # ==================================================================
    current_section[0] = "Shad Bala"
    pdf.check_space(50)
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
    pdf.check_space(40)
    pdf.section_title("Aspects on Planets (Graha Drishti)")

    # Build aspect matrix from aspects_on_planets list
    # Engine returns: [{aspecting, aspected, strength, type, ...}]
    aspects_on_planets_list = aspects_data.get("aspects_on_planets", [])
    aspect_matrix: Dict[str, Dict[str, float]] = {}
    if isinstance(aspects_on_planets_list, list) and aspects_on_planets_list:
        for asp in aspects_on_planets_list:
            if isinstance(asp, dict):
                a_from = asp.get("aspecting", "")
                a_to = asp.get("aspected", "")
                a_str = asp.get("strength", 1.0)
                if a_from and a_to:
                    aspect_matrix.setdefault(a_from, {})[a_to] = a_str

    ap_cw = 17
    ap_headers = ["Aspecting"] + [PLANET_ABBR.get(p, p[:2]) for p in PLANET_LIST_9]
    ap_widths = [22] + [ap_cw] * 9
    pdf.table_header(ap_headers, ap_widths, font_size=6)

    if aspect_matrix:
        for idx, p1 in enumerate(PLANET_LIST_9):
            row_vals = [PLANET_ABBR.get(p1, p1[:2])]
            p1_asp = aspect_matrix.get(p1, {})
            for p2 in PLANET_LIST_9:
                if p1 == p2:
                    row_vals.append("-")
                else:
                    val = p1_asp.get(p2, "")
                    row_vals.append(_fmt_num(val, 1) if isinstance(val, (int, float)) else "")
            pdf.table_row(row_vals, ap_widths, idx, font_size=5.5)
    else:
        # Fallback: try old dict-based format
        aspect_planets_dict = aspects_data.get("planet_aspects", aspects_data.get("graha_drishti", {}))
        if isinstance(aspect_planets_dict, dict):
            for idx, p1 in enumerate(PLANET_LIST_9):
                row_vals = [PLANET_ABBR.get(p1, p1[:2])]
                p1_asp = aspect_planets_dict.get(p1, {})
                for p2 in PLANET_LIST_9:
                    if p1 == p2:
                        row_vals.append("-")
                    else:
                        val = p1_asp.get(p2, "")
                        if isinstance(val, dict):
                            val = val.get("strength", "")
                        row_vals.append(_fmt_num(val, 1) if isinstance(val, (int, float)) else str(val)[:4] if val else "")
                pdf.table_row(row_vals, ap_widths, idx, font_size=5.5)
    pdf.ln(4)

    # Aspects on Bhavas
    pdf.check_space(24)
    pdf.section_title("Aspects on Bhavas (House Aspects)")

    # Engine returns: aspects_on_bhavas = {"1": [{planet, from_house, strength, ...}], ...}
    aspects_on_bhavas_data = aspects_data.get("aspects_on_bhavas", {})
    ba_cw = 13.5
    ba_headers = ["Planet"] + [str(i) for i in range(1, 13)]
    ba_widths = [22] + [ba_cw] * 12
    pdf.table_header(ba_headers, ba_widths, font_size=6)

    if isinstance(aspects_on_bhavas_data, dict) and aspects_on_bhavas_data:
        # Build planet->house matrix from the house-keyed data
        planet_house_aspects: Dict[str, Dict[int, float]] = {}
        for house_key, asp_list in aspects_on_bhavas_data.items():
            h_num = int(house_key) if str(house_key).isdigit() else 0
            if not isinstance(asp_list, list):
                continue
            for asp in asp_list:
                if isinstance(asp, dict):
                    pn = asp.get("planet", "")
                    strength = asp.get("strength", 1.0)
                    if pn:
                        planet_house_aspects.setdefault(pn, {})[h_num] = strength

        for idx, pname in enumerate(PLANET_LIST_9):
            row_vals = [PLANET_ABBR.get(pname, pname[:2])]
            pa = planet_house_aspects.get(pname, {})
            for bnum in range(1, 13):
                val = pa.get(bnum, "")
                row_vals.append(_fmt_num(val, 1) if isinstance(val, (int, float)) else "")
            pdf.table_row(row_vals, ba_widths, idx, font_size=5.5)
    else:
        # Fallback: try old dict format
        bhava_aspects = aspects_data.get("bhava_aspects", aspects_data.get("house_aspects", {}))
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
    pdf.ln(2)
    # Compact summary to fill remaining space meaningfully
    house_totals: Dict[int, int] = {i: 0 for i in range(1, 13)}
    if isinstance(aspects_on_bhavas_data, dict):
        for hk, asp_list in aspects_on_bhavas_data.items():
            try:
                hnum = int(hk)
            except Exception:
                continue
            if isinstance(asp_list, list):
                house_totals[hnum] = len(asp_list)
    ranked = sorted(house_totals.items(), key=lambda kv: kv[1], reverse=True)
    pdf.set_font("Helvetica", "I", 6.3)
    pdf.set_text_color(*MUTED)
    summary = ", ".join([f"H{h}:{c}" for h, c in ranked[:6] if c > 0]) or "No significant house aspects"
    pdf.multi_cell(0, 3.5, f"House aspect density: {summary}")
    pdf.set_text_color(*DARK)
    pdf.ln(2)

    # ==================================================================
    # PAGES 10-11: ASHTAKVARGA (BHINNASHTAKVARGA)
    # ==================================================================
    def _draw_bav_page(planet_list: list, page_title: str):
        current_section[0] = page_title
        pdf.add_page()
        pdf.section_title(page_title)
        # planet_details has the contributor-level 0/1 grids
        details = ashtakvarga_data.get("planet_details", {})
        # planet_bindus has per-sign totals (fallback)
        bav_totals = ashtakvarga_data.get("planet_bindus", ashtakvarga_data.get("bav", {}))
        contributors_display = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Lagna"]

        for pi_idx, planet in enumerate(planet_list):
            pdf.check_space(50)
            # Map "Ascendant" to "Lagna" key used by engine
            planet_key = "Lagna" if planet == "Ascendant" else planet
            pdf.sub_section(f"Bhinnashtakvarga: {planet}")
            bav_h = ["Contrib."] + SIGN_SHORT + ["Total"]
            bav_cw = 12
            bav_ws = [17] + [bav_cw] * 12 + [14]
            pdf.table_header(bav_h, bav_ws, font_size=5)

            # Get contributor matrix from planet_details
            planet_detail = details.get(planet_key, {})
            contributors_matrix = planet_detail.get("contributors", {})

            for ci, contrib in enumerate(contributors_display):
                row_vals = [PLANET_ABBR.get(contrib, contrib[:2])]
                row_total = 0
                # The contributor matrix keys use "Lagna" not "Ascendant"
                contrib_data = contributors_matrix.get(contrib, {})
                if not contrib_data and contrib == "Lagna":
                    contrib_data = contributors_matrix.get("Ascendant", {})
                if isinstance(contrib_data, dict) and contrib_data:
                    for sign in SIGN_ORDER:
                        v = contrib_data.get(sign, 0)
                        row_vals.append(str(v))
                        row_total += int(v) if isinstance(v, (int, float)) else 0
                else:
                    row_vals += ["0"] * 12
                row_vals.append(str(row_total))
                pdf.table_row(row_vals, bav_ws, ci, font_size=5)

            # Totals row from planet_details totals or planet_bindus
            pdf.set_font("Helvetica", "B", 5)
            pdf.set_fill_color(*GOLD_LIGHT)
            totals_row = ["Total"]
            grand_total = 0
            totals_data = planet_detail.get("totals", bav_totals.get(planet_key, {}))
            if isinstance(totals_data, dict):
                for sign in SIGN_ORDER:
                    v = int(totals_data.get(sign, 0))
                    totals_row.append(str(v))
                    grand_total += v
            else:
                totals_row += ["0"] * 12
            totals_row.append(str(grand_total))
            for i, v in enumerate(totals_row):
                pdf.cell(bav_ws[i], 5, _sanitize(str(v)), border=1, align="C", fill=True)
            pdf.ln(5)

    _draw_bav_page(["Sun", "Moon", "Mars", "Mercury"], "Bhinnashtakvarga I")
    _draw_bav_page(["Jupiter", "Venus", "Saturn", "Ascendant"], "Bhinnashtakvarga II")

    # ==================================================================
    # SARVASHTAKVARGA + REDUCTIONS
    # ==================================================================
    current_section[0] = "Sarvashtakvarga"
    pdf.check_space(50)
    pdf.section_title("Sarvashtakvarga (SAV)")

    sav = ashtakvarga_data.get("sarvashtakvarga", ashtakvarga_data.get("sav", {}))
    sav_cw = 13
    sav_headers = [""] + SIGN_SHORT + ["Total"]
    sav_widths_t = [20] + [sav_cw] * 12 + [16]
    pdf.table_header(sav_headers, sav_widths_t, font_size=5.5)

    # Show per-planet BAV totals (sum of bindus per sign for each planet)
    bav_all = ashtakvarga_data.get("planet_bindus", ashtakvarga_data.get("bav", {}))
    for idx, contrib in enumerate(PLANET_LIST_7 + ["Lagna"]):
        row_vals = [PLANET_ABBR.get(contrib, contrib[:2])]
        row_total = 0
        bav_c = bav_all.get(contrib, {})
        if isinstance(bav_c, dict):
            for sign in SIGN_ORDER:
                v = int(bav_c.get(sign, 0))
                row_vals.append(str(v))
                row_total += v
        else:
            for sign in SIGN_ORDER:
                row_vals.append("0")
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
    pdf.check_space(76)
    pdf.sub_section("SAV Distribution Chart")
    sav_chart: Dict[int, List[str]] = {}
    for si, sign in enumerate(SIGN_ORDER):
        v = sav.get(sign, 0) if isinstance(sav, dict) else 0
        sav_chart[si + 1] = [str(v)]
    sav_y = pdf.get_y() + 2
    _draw_north_indian_chart(pdf, 55, sav_y, 70, sav_chart, "SAV Bindus")
    pdf.set_y(sav_y + 76)

    # Trikona Shodhana — from ashtakvarga["purified"][planet]["trikona"]
    pdf.check_space(45)
    pdf.sub_section("Trikona Shodhana")
    purified = ashtakvarga_data.get("purified", {})
    trikona_available = any(
        isinstance(purified.get(p, {}), dict) and "trikona" in purified.get(p, {})
        for p in PLANET_LIST_7
    )
    if trikona_available:
        tr_headers = ["Planet"] + SIGN_SHORT + ["Pinda"]
        tr_widths = [20] + [sav_cw] * 12 + [16]
        pdf.table_header(tr_headers, tr_widths, font_size=5.5)
        for idx, pname in enumerate(PLANET_LIST_7):
            pd_purified = purified.get(pname, {})
            trik_data = pd_purified.get("trikona", {}) if isinstance(pd_purified, dict) else {}
            row_vals = [PLANET_ABBR.get(pname, pname[:2])]
            pinda = 0
            for sign in SIGN_ORDER:
                v = trik_data.get(sign, 0) if isinstance(trik_data, dict) else 0
                row_vals.append(str(v))
                pinda += int(v) if isinstance(v, (int, float)) else 0
            row_vals.append(str(pinda))
            pdf.table_row(row_vals, tr_widths, idx, font_size=5.5)
    else:
        pdf.set_font("Helvetica", "I", 7)
        pdf.cell(0, 5, "Trikona Shodhana data not available.", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Ekadhipatya Shodhana — from ashtakvarga["purified"][planet]["ekadhipatya"]
    pdf.check_space(40)
    pdf.sub_section("Ekadhipatya Shodhana")
    ekadhipatya_available = any(
        isinstance(purified.get(p, {}), dict) and "ekadhipatya" in purified.get(p, {})
        for p in PLANET_LIST_7
    )
    if ekadhipatya_available:
        ek_headers = ["Planet"] + SIGN_SHORT + ["Pinda"]
        ek_widths = [20] + [sav_cw] * 12 + [16]
        pdf.table_header(ek_headers, ek_widths, font_size=5.5)
        for idx, pname in enumerate(PLANET_LIST_7):
            pd_purified = purified.get(pname, {})
            ek_data = pd_purified.get("ekadhipatya", {}) if isinstance(pd_purified, dict) else {}
            row_vals = [PLANET_ABBR.get(pname, pname[:2])]
            pinda_val = pd_purified.get("shodhya_pinda", 0) if isinstance(pd_purified, dict) else 0
            for sign in SIGN_ORDER:
                v = ek_data.get(sign, 0) if isinstance(ek_data, dict) else 0
                row_vals.append(str(v))
            row_vals.append(str(pinda_val))
            pdf.table_row(row_vals, ek_widths, idx, font_size=5.5)
    else:
        pdf.set_font("Helvetica", "I", 7)
        pdf.cell(0, 5, "Ekadhipatya Shodhana data not available.", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # ==================================================================
    # VIMSHOTTARI DASHA TIMELINE
    # ==================================================================
    current_section[0] = "Vimshottari Dasha"
    pdf.check_space(50)
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
    md_periods = dasha_data.get("mahadasha", dasha_data.get("mahadasha_periods", []))
    for idx, period in enumerate(md_periods):
        planet = period.get("planet", "?")
        start = _fmt_date(period.get("start", period.get("start_date", "?")))
        end = _fmt_date(period.get("end", period.get("end_date", "?")))
        yrs = period.get("years", DASHA_YEARS.get(planet, "?"))
        years = f"{yrs:.1f}" if isinstance(yrs, float) else str(yrs)
        marker = " <" if planet == current_md_name else ""
        pdf.table_row([planet + marker, start, end, years], md_widths, idx)
    pdf.ln(4)

    # Antardasha — build dict {md_planet: [ad_list]} from embedded structure
    ad_periods: Dict[str, list] = {}
    for md in md_periods:
        mp = md.get("planet", "")
        ads = md.get("antardasha", md.get("antardashas", []))
        if ads:
            ad_periods[mp] = ads
    # Fallback: try top-level antardasha keys
    if not ad_periods:
        ad_periods = dasha_data.get("antardasha_periods", dasha_data.get("antardasha", {}))
        if isinstance(ad_periods, list):
            ad_periods = {current_md_name: ad_periods}
    md_names = [p.get("planet", "") for p in md_periods] if md_periods else list(DASHA_YEARS.keys())

    if isinstance(ad_periods, dict):
        # If fallback produced a single list for current MD, avoid rendering empty duplicate blocks.
        if len(ad_periods) == 1 and current_md_name in ad_periods:
            md_names = [current_md_name]
        rendered_md: set = set()
        for md_name in md_names:
            if md_name in rendered_md:
                continue
            ad_list = ad_periods.get(md_name, [])
            if not (isinstance(ad_list, list) and ad_list):
                continue
            rendered_md.add(md_name)

            rows_to_render = [ad for ad in ad_list if isinstance(ad, dict)]
            est_h = 6.0 + 4.4 + (len(rows_to_render) * 3.9) + 3.0
            pdf.check_space(est_h)
            pdf.sub_section(f"Antardasha in {md_name} Mahadasha")
            ad_h = ["Antar", "Beginning", "Ending"]
            ad_w = [30, 50, 50]
            pdf.table_header(ad_h, ad_w)
            for ai, ad in enumerate(rows_to_render):
                pdf.table_row([
                    ad.get("planet", ad.get("antardasha", ad.get("sub_lord", "?"))),
                    _fmt_date(ad.get("start", ad.get("start_date", ad.get("begin", "?")))),
                    _fmt_date(ad.get("end", ad.get("end_date", "?"))),
                ], ad_w, ai)
            pdf.ln(2)

    # Pratyantar dasha — extract from embedded MD > AD > pratyantar structure
    has_pratyantar = False
    for md in md_periods:
        for ad in md.get("antardasha", []):
            if ad.get("pratyantar"):
                has_pratyantar = True
                break
        if has_pratyantar:
            break

    if has_pratyantar:
        current_section[0] = "Pratyantar Dasha"
        pdf.check_space(50)
        pdf.section_title("Pratyantar Dasha (Sub-Sub Periods)")
        # Show pratyantars for current MD's antardashas
        for md in md_periods:
            if not md.get("is_current"):
                continue
            for ad in md.get("antardasha", []):
                pd_list = ad.get("pratyantar", [])
                if not pd_list:
                    continue
                pdf.check_space(25)
                pdf.sub_section(f"{md.get('planet','?')}-{ad.get('planet','?')}")
                pd_h = ["Pratyantar", "Begin", "End"]
                pd_w = [30, 50, 50]
                pdf.table_header(pd_h, pd_w)
                for pi_idx, pd in enumerate(pd_list[:9]):
                    if isinstance(pd, dict):
                        pdf.table_row([
                            pd.get("planet", "?"),
                            _fmt_date(pd.get("start", pd.get("start_date", "?"))),
                            _fmt_date(pd.get("end", pd.get("end_date", "?"))),
                        ], pd_w, pi_idx)
                pdf.ln(2)

    # ==================================================================
    # YOGINI DASHA
    # ==================================================================
    if capabilities["dasha_yogini"] and _dict_has_values(yogini_data, 1):
        current_section[0] = "Yogini Dasha"
        pdf.check_space(50)
        pdf.section_title("Yogini Dasha")

        yogini_current = _sg(yogini_data, "current_yogini", default="N/A")
        yogini_balance = _sg(yogini_data, "balance", default="N/A")
        if _has_meaningful(yogini_current) or _has_meaningful(yogini_balance):
            pdf.set_font("Helvetica", "B", 8)
            pdf.cell(0, 5, f"Current Yogini: {yogini_current}  |  Balance: {yogini_balance}",
                     new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)

        yogini_periods = yogini_data.get("periods", yogini_data.get("yogini_periods", []))
        if yogini_periods and isinstance(yogini_periods, list):
            pdf.sub_section("Yogini Dasha Periods")
            yp_headers = ["Yogini", "Lord", "Begin", "End", "Years"]
            yp_widths = [30, 20, 40, 40, 15]
            pdf.table_header(yp_headers, yp_widths)
            for idx, yp in enumerate(yogini_periods):
                if isinstance(yp, dict):
                    pdf.table_row([
                        yp.get("yogini", yp.get("name", "?")),
                        yp.get("lord", "?"),
                        _fmt_date(yp.get("start", yp.get("start_date", yp.get("begin", "?")))),
                        _fmt_date(yp.get("end", yp.get("end_date", "?"))),
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
    # YOGAS & DOSHAS
    # ==================================================================
    current_section[0] = "Yogas & Doshas"
    pdf.check_space(40)
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
    # Compact summary block to avoid underfilled yoga pages.
    if isinstance(yogas, list) and yogas:
        present = [y for y in yogas if isinstance(y, dict) and y.get("present", True)]
        absent = [y for y in yogas if isinstance(y, dict) and not y.get("present", True)]
        pdf.check_space(20)
        pdf.sub_section("Yoga Summary")
        ys_headers = ["Total", "Present", "Not Formed", "Strong Highlights"]
        ys_widths = [20, 20, 26, 120]
        pdf.table_header(ys_headers, ys_widths, font_size=6.0)
        highlights = []
        for y in present:
            nm = str(y.get("name", y.get("yoga", ""))).strip()
            if nm:
                highlights.append(nm)
            if len(highlights) >= 4:
                break
        hl = ", ".join(highlights) if highlights else "—"
        pdf.table_row([str(len(yogas)), str(len(present)), str(len(absent)), hl],
                      ys_widths, 0, font_size=5.8, aligns=["C", "C", "C", "L"])
    pdf.ln(2)

    pdf.check_space(28)
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
    # MANGALA DOSHA
    # ==================================================================
    current_section[0] = "Mangala Dosha"
    pdf.check_space(40)
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
    pdf.ln(1.5)

    # Compact risk matrix to improve page composition on text-heavy pages.
    pdf.check_space(22)
    pdf.sub_section("Dosha Risk Snapshot")
    dr_headers = ["Indicator", "Status", "Indicator", "Status"]
    dr_widths = [45, 50, 45, 50]
    pdf.table_header(dr_headers, dr_widths, font_size=6.0)
    present_doshas = [d for d in doshas if isinstance(d, dict) and d.get("present", True)] if isinstance(doshas, list) else []
    high_doshas = [d for d in present_doshas if str(d.get("severity", "")).lower() in {"high", "severe"}]
    dr_rows = [
        ["Total Doshas Detected", str(len(present_doshas)), "High Severity Doshas", str(len(high_doshas))],
        ["Manglik from Lagna", "Yes" if is_manglik_lagna else "No", "Manglik from Moon", "Yes" if is_manglik_moon else "No"],
    ]
    for idx, row in enumerate(dr_rows):
        pdf.table_row(row, dr_widths, idx, font_size=5.9, aligns=["L", "C", "L", "C"])
    pdf.ln(1.8)

    # ==================================================================
    # SADE SATI
    # ==================================================================
    current_section[0] = "Sade Sati"
    pdf.check_space(40)
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
    ss_active = sadesati_data.get("has_sade_sati", sadesati_data.get("is_active", sadesati_data.get("active", False)))
    ss_phase = sadesati_data.get("phase", sadesati_data.get("current_phase", "N/A"))
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
        pdf.check_space(50)
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
        pdf.check_space(50)
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
        pdf.check_space(50)
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
            pdf.check_space(76)
            vp_chart_y = pdf.get_y() + 2
            _draw_north_indian_chart(pdf, 55, vp_chart_y, 70, vp_pih, f"Varshphal Chart ({vp_year})")
            pdf.set_y(vp_chart_y + 76)

    # ==================================================================
    # PLANETARY PLACEMENT INTERPRETATIONS
    # ==================================================================
    current_section[0] = "Interpretations"
    pdf.check_space(40)
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
    pdf.check_space(40)
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
    pdf.check_space(40)
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
    pdf.check_space(40)
    pdf.section_title("General Predictions by Bhava (House)")

    for bnum in range(1, 13):
        topic, desc = _HOUSE_TOPICS[bnum]
        sign = SIGN_ORDER[(asc_idx + bnum - 1) % 12]
        lord = SIGN_LORD.get(sign, "N/A")
        lord_h = planet_houses.get(lord, "N/A")
        planets_here = [pn for pn, ph in planet_houses.items() if ph == bnum]

        pdf.check_space(15)
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
        pdf.ln(1.1)

    pdf.check_space(26)
    pdf.sub_section("House Occupancy Matrix")
    ho_headers = ["House", "Sign", "Occupants", "House", "Sign", "Occupants"]
    ho_widths = [14, 24, 56, 14, 24, 56]
    pdf.table_header(ho_headers, ho_widths, font_size=5.9)
    for i in range(1, 13, 2):
        sign1 = SIGN_ORDER[(asc_idx + i - 1) % 12]
        occ1 = ", ".join([pn for pn, ph in planet_houses.items() if ph == i]) or "—"
        i2 = i + 1
        sign2 = SIGN_ORDER[(asc_idx + i2 - 1) % 12]
        occ2 = ", ".join([pn for pn, ph in planet_houses.items() if ph == i2]) or "—"
        pdf.table_row([str(i), sign1, occ1, str(i2), sign2, occ2], ho_widths, (i - 1) // 2,
                      font_size=5.7, aligns=["C", "C", "L", "C", "C", "L"])

    # ==================================================================
    # PLANETARY AVASTHAS
    # ==================================================================
    current_section[0] = "Planetary Avasthas"
    pdf.check_space(40)
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
    pdf.check_space(70)
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
    pdf.ln(2)

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
    pdf.ln(2)

    module_labels = {
        "panchang": "Detailed Panchang framework",
        "divisional_charts": "Extended divisional chart system",
        "ashtakavarga": "Ashtakavarga deep tables",
        "shadbala": "Detailed Shadbala components",
        "bhava_bala": "Bhava Bala breakdown",
        "dasha_vimshottari": "Detailed Vimshottari hierarchy",
        "dasha_yogini": "Yogini dasha periods",
        "kp": "KP cuspal and significator module",
        "jaimini": "Jaimini advanced module",
        "lal_kitab": "Lal Kitab module",
    }
    missing_modules = [module_labels[k] for k, ok in capabilities.items() if not ok and k in module_labels]
    if missing_modules:
        pdf.check_space(26 + 4 * min(len(missing_modules), 8))
        pdf.sub_section("Advanced Modules Not Included in This Report")
        pdf.set_font("Helvetica", "", 6.8)
        pdf.set_text_color(*MUTED)
        pdf.multi_cell(0, 3.4,
            "Some advanced systems are omitted because the current engine/data for this chart "
            "did not provide complete reliable output.")
        for m in missing_modules[:10]:
            pdf.cell(0, 4.0, f"  * {m}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(*DARK)
        pdf.ln(1.2)

    pdf.sub_section("Computation Metadata")
    meta_h = ["Item", "Value"]
    meta_w = [70, 120]
    pdf.table_header(meta_h, meta_w, font_size=6.5)
    meta_rows = [
        ("Ayanamsha", str(ayanamsa_val)),
        ("Ascendant", f"{asc_sign} {_fmt_num(asc_degree)}"),
        ("Moon Nakshatra", str(planets.get("Moon", {}).get("nakshatra", "N/A"))),
        ("Current Mahadasha", str(_sg(dasha_data, "current_dasha", default="N/A"))),
        ("Total Planets Processed", str(len([p for p in planets if isinstance(planets.get(p), dict)]))),
        ("Total Pages", str(pdf.page_no())),
        ("Layout Warnings", str(len(pdf.layout_warnings))),
        ("Page Composition Engine", "Enabled"),
    ]
    for idx, (k, v) in enumerate(meta_rows):
        pdf.table_row([k, v], meta_w, idx, font_size=6.2, aligns=["L", "L"])
    pdf.ln(1.4)

    pdf.check_space(46)
    pdf.sub_section("Engine Capability Map")
    cap_headers = ["Module", "Status"]
    cap_widths = [130, 60]
    pdf.table_header(cap_headers, cap_widths, font_size=6.2)
    cap_rows = [
        ("Panchang", capabilities.get("panchang")),
        ("Planetary Positions", capabilities.get("planetary_positions")),
        ("Lagna/Rashi Charts", capabilities.get("lagna_rashi_charts")),
        ("Divisional Charts", capabilities.get("divisional_charts")),
        ("Ashtakavarga", capabilities.get("ashtakavarga")),
        ("Shadbala", capabilities.get("shadbala")),
        ("Bhava Bala", capabilities.get("bhava_bala")),
        ("Avastha (Baladi)", capabilities.get("avasthas")),
        ("Yogas/Doshas", capabilities.get("yogas_doshas")),
        ("Vimshottari Dasha", capabilities.get("dasha_vimshottari")),
        ("Yogini Dasha", capabilities.get("dasha_yogini")),
        ("KP", capabilities.get("kp")),
        ("Jaimini", capabilities.get("jaimini")),
        ("Lal Kitab", capabilities.get("lal_kitab")),
    ]
    for idx, (label, enabled) in enumerate(cap_rows):
        status = "Included" if enabled else "Not included"
        pdf.table_row([label, status], cap_widths, idx, font_size=6.0, aligns=["L", "C"])
    pdf.ln(1.2)

    if missing_modules:
        pdf.sub_section("Data Completeness Notes")
        pdf.set_font("Helvetica", "", 6.7)
        pdf.multi_cell(
            0, 3.5,
            "This report intentionally omits unsupported advanced modules rather than filling with "
            "placeholders. All rendered sections are based on available computed data."
        )
        pdf.ln(0.8)

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
    pdf.finalize_composition()
    return pdf.output()
