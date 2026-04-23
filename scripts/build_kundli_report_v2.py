#!/usr/bin/env python3
"""Build the new professional kundli_report.py in one clean pass."""
import os

OUT = "app/reports/kundli_report.py"

# We'll write the file in parts using a list
P = []

def add(s):
    P.append(s)

# ========================================================================
# PART 1: Header, imports, constants, helpers
# ========================================================================
add(r'''"""
Kundli Full Report PDF Generator - Professional Edition
=======================================================
Generates a premium, production-grade Vedic astrology report covering
all website tabs with structured layout and comprehensive section coverage.

Usage:
    pdf_bytes = build_full_report(kundli_data)
"""
from __future__ import annotations

import os
import math
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import importlib.util

from fpdf import FPDF

# ------------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------------
SIGN_ORDER = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]
SIGN_SHORT = ["Ari", "Tau", "Gem", "Can", "Leo", "Vir",
              "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis"]
SIGN_LORD = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}
SIGN_ELEMENT = {
    "Aries": "Fire", "Taurus": "Earth", "Gemini": "Air", "Cancer": "Water",
    "Leo": "Fire", "Virgo": "Earth", "Libra": "Air", "Scorpio": "Water",
    "Sagittarius": "Fire", "Capricorn": "Earth", "Aquarius": "Air", "Pisces": "Water",
}
SIGN_MODALITY = {
    "Aries": "Cardinal", "Taurus": "Fixed", "Gemini": "Mutable",
    "Cancer": "Cardinal", "Leo": "Fixed", "Virgo": "Mutable",
    "Libra": "Cardinal", "Scorpio": "Fixed", "Sagittarius": "Mutable",
    "Capricorn": "Cardinal", "Aquarius": "Fixed", "Pisces": "Mutable",
}
SIGN_INDEX = {s: i for i, s in enumerate(SIGN_ORDER)}
PLANET_LIST_7 = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
PLANET_LIST_9 = PLANET_LIST_7 + ["Rahu", "Ketu"]
PLANET_ABBR = {
    "Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me",
    "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa", "Rahu": "Ra", "Ketu": "Ke",
    "Ascendant": "As", "Lagna": "As",
}
NAKSHATRA_LIST = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
    "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
    "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]
NAKSHATRA_LORD = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
]
DASHA_YEARS = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
    "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17,
}
DASHA_SEQUENCE = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
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
NATURAL_FRIENDS = {
    "Sun": ["Moon", "Mars", "Jupiter"], "Moon": ["Sun", "Mercury"],
    "Mars": ["Sun", "Moon", "Jupiter"], "Mercury": ["Sun", "Venus"],
    "Jupiter": ["Sun", "Moon", "Mars"], "Venus": ["Mercury", "Saturn"],
    "Saturn": ["Mercury", "Venus"], "Rahu": ["Mercury", "Saturn", "Venus"],
    "Ketu": ["Mercury", "Saturn", "Venus"],
}
NATURAL_ENEMIES = {
    "Sun": ["Saturn", "Venus"], "Moon": [], "Mars": ["Mercury"],
    "Mercury": ["Moon"], "Jupiter": ["Mercury", "Venus"],
    "Venus": ["Sun", "Moon"], "Saturn": ["Sun", "Moon", "Mars"],
    "Rahu": ["Sun", "Moon", "Mars"], "Ketu": ["Sun", "Moon", "Mars"],
}
SHADBALA_MIN = {"Sun": 390, "Moon": 360, "Mars": 300, "Mercury": 420,
                "Jupiter": 390, "Venus": 330, "Saturn": 300}
VARGA_NAMES = {
    "D1": "Rashi (Lagna)", "D2": "Hora", "D3": "Drekkana", "D4": "Chaturthamsha",
    "D7": "Saptamsha", "D9": "Navamsha", "D10": "Dashamsha", "D12": "Dwadashamsha",
    "D16": "Shodashamsha", "D20": "Vimshamsha", "D24": "Chaturvimshamsha",
    "D27": "Saptavimshamsha", "D30": "Trimshamsha", "D40": "Khavedamsha",
    "D45": "Akshavedamsha", "D60": "Shashtiamsha",
}
GEMSTONE_DATA = {
    "Sun": {"stone": "Ruby (Manik)", "finger": "Ring", "metal": "Gold", "weight": "3-6 carats", "day": "Sunday", "mantra": "Om Hram Hrim Hroum Sah Suryaya Namah"},
    "Moon": {"stone": "Pearl (Moti)", "finger": "Little", "metal": "Silver", "weight": "2-5 carats", "day": "Monday", "mantra": "Om Shram Shrim Shroum Sah Chandraya Namah"},
    "Mars": {"stone": "Red Coral (Moonga)", "finger": "Ring", "metal": "Gold/Copper", "weight": "3-6 carats", "day": "Tuesday", "mantra": "Om Kram Kreem Kroum Sah Bhaumaya Namah"},
    "Mercury": {"stone": "Emerald (Panna)", "finger": "Little", "metal": "Gold", "weight": "3-5 carats", "day": "Wednesday", "mantra": "Om Bram Brim Broum Sah Budhaya Namah"},
    "Jupiter": {"stone": "Yellow Sapphire (Pukhraj)", "finger": "Index", "metal": "Gold", "weight": "3-6 carats", "day": "Thursday", "mantra": "Om Gram Grim Groum Sah Guruve Namah"},
    "Venus": {"stone": "Diamond (Heera)", "finger": "Middle", "metal": "Gold", "weight": "0.5-1 carat", "day": "Friday", "mantra": "Om Dram Drim Droum Sah Shukraya Namah"},
    "Saturn": {"stone": "Blue Sapphire (Neelam)", "finger": "Middle", "metal": "Silver", "weight": "3-5 carats", "day": "Saturday", "mantra": "Om Pram Preem Proum Sah Shanaye Namah"},
    "Rahu": {"stone": "Hessonite (Gomed)", "finger": "Middle", "metal": "Silver", "weight": "3-6 carats", "day": "Saturday", "mantra": "Om Bhram Bhreem Bhroum Sah Rahave Namah"},
    "Ketu": {"stone": "Cat's Eye (Lehsunia)", "finger": "Little", "metal": "Silver", "weight": "3-5 carats", "day": "Tuesday", "mantra": "Om Stram Streem Stroum Sah Ketave Namah"},
}
HOUSE_TOPICS = {
    1: ("Personality & Body", "Physical appearance, temperament, health, longevity, self-identity"),
    2: ("Wealth & Family", "Family lineage, accumulated wealth, speech, food habits, early education"),
    3: ("Courage & Siblings", "Younger siblings, courage, communication, short travels, skills"),
    4: ("Home & Mother", "Domestic happiness, vehicles, mother, land, education, heart"),
    5: ("Children & Intelligence", "Progeny, intelligence, speculation, mantras, past merit"),
    6: ("Disease & Enemies", "Health issues, enemies, debts, service, competition, maternal uncle"),
    7: ("Marriage & Partnerships", "Spouse, business partnerships, foreign lands, open enemies"),
    8: ("Longevity & Occult", "Longevity, sudden events, inheritance, occult, transformation"),
    9: ("Fortune & Father", "Luck, father, higher learning, pilgrimage, dharma, guru"),
    10: ("Career & Status", "Profession, honour, government, authority, public image"),
    11: ("Gains & Friends", "Elder siblings, gains, ambitions, social networks, fulfilment"),
    12: ("Expenses & Liberation", "Expenditure, losses, foreign settlement, spirituality, bed pleasures"),
}


# ------------------------------------------------------------------
# DATA HELPERS
# ------------------------------------------------------------------
def _sg(data: Any, *keys, default: Any = "N/A") -> Any:
    for k in keys:
        if isinstance(data, dict):
            data = data.get(k, default)
        else:
            return default
    return data if data is not None else default


def _fmt_date(d: str) -> str:
    if not d or d in ("N/A", "?"):
        return "N/A"
    try:
        dt = datetime.strptime(str(d)[:10], "%Y-%m-%d")
        return dt.strftime("%d %b %Y")
    except Exception:
        try:
            dt = datetime.strptime(str(d)[:10], "%d-%m-%Y")
            return dt.strftime("%d %b %Y")
        except Exception:
            return str(d)


def _fmt_num(v: Any, decimals: int = 2) -> str:
    if v is None or v == "N/A":
        return "N/A"
    try:
        return f"{float(v):.{decimals}f}"
    except (ValueError, TypeError):
        return str(v)


def _display(v: Any) -> str:
    if v is None:
        return "N/A"
    if isinstance(v, bool):
        return "Yes" if v else "No"
    if isinstance(v, float):
        return f"{v:.2f}"
    return str(v)


def _sanitize(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)
    repl = {
        '\u2014': '-', '\u2013': '-', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2026': '...', '\u2212': '-',
        '\u00b0': 'deg', '\u00d7': 'x', '\u00f7': '/', '\u2264': '<=',
        '\u2265': '>=', '\u2022': '*', '\u25cf': '*',
    }
    for ch, rep in repl.items():
        text = text.replace(ch, rep)
    try:
        text.encode('latin-1')
    except UnicodeEncodeError:
        text = text.encode('ascii', 'ignore').decode('ascii')
    return text


def _has_meaningful(v: Any) -> bool:
    if v is None:
        return False
    if isinstance(v, str):
        return v.strip() not in ("", "N/A", "n/a", "None", "null", "?", "-")
    if isinstance(v, (list, dict)):
        return len(v) > 0
    return True


def _get_dignity(planet: str, sign: str) -> str:
    if not sign or not planet:
        return "Neutral"
    if EXALTATION.get(planet) == sign:
        return "Exalted"
    if DEBILITATION.get(planet) == sign:
        return "Debilitated"
    if sign in OWN_SIGNS.get(planet, []):
        return "Own Sign"
    mt = MOOLATRIKONA.get(planet)
    if mt and mt[0] == sign:
        return "Moolatrikona"
    sl = SIGN_LORD.get(sign, "")
    if sl:
        if planet in NATURAL_FRIENDS.get(sl, []):
            return "Friendly"
        if planet in NATURAL_ENEMIES.get(sl, []):
            return "Enemy"
    return "Neutral"


def _house_distance(from_sign: str, to_sign: str) -> int:
    return ((SIGN_INDEX.get(to_sign, 0) - SIGN_INDEX.get(from_sign, 0)) % 12) + 1


def _natural_relation(p1: str, p2: str) -> str:
    if p1 == p2:
        return "Self"
    if p2 in NATURAL_FRIENDS.get(p1, []):
        return "Friend"
    if p2 in NATURAL_ENEMIES.get(p1, []):
        return "Enemy"
    return "Neutral"


def _temporal_relation(p1_sign: str, p2_sign: str) -> str:
    d = _house_distance(p1_sign, p2_sign)
    if d in {1, 5, 6, 7, 8, 9}:
        return "Enemy"
    return "Friend"


def _compound_relation(natural: str, temporal: str) -> str:
    mapping = {
        ("Friend", "Friend"): "Fast Friend", ("Friend", "Neutral"): "Friend",
        ("Friend", "Enemy"): "Neutral", ("Neutral", "Friend"): "Friend",
        ("Neutral", "Neutral"): "Neutral", ("Neutral", "Enemy"): "Enemy",
        ("Enemy", "Friend"): "Neutral", ("Enemy", "Neutral"): "Enemy",
        ("Enemy", "Enemy"): "Bitter Enemy",
    }
    return mapping.get((natural, temporal), "Neutral")


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


def _build_planets_in_houses(planets: dict, asc_house: int = 1) -> Dict[int, List[str]]:
    pih: Dict[int, List[str]] = {}
    for pn, pi in planets.items():
        if not isinstance(pi, dict):
            continue
        h = pi.get("house", 1)
        if h is None:
            continue
        rel_h = ((int(h) - asc_house) % 12) + 1
        pih.setdefault(rel_h, []).append(PLANET_ABBR.get(pn, pn[:2]))
    return pih
''')

# ========================================================================
# PART 2: Chart drawing + ProfessionalPDF class
# ========================================================================
add(r'''
# ------------------------------------------------------------------
# CHART DRAWING - North Indian Style
# ------------------------------------------------------------------
def _draw_north_indian_chart(
    pdf: FPDF, x: float, y: float, size: float,
    planets_in_houses: Dict[int, List[str]], title: str = "", show_title: bool = True,
) -> float:
    cx, cy = x + size / 2.0, y + size / 2.0
    half = size / 2.0
    quarter = size / 4.0
    diamond = [(cx, cy - half), (cx + half, cy), (cx, cy + half), (cx - half, cy)]
    pdf.set_fill_color(253, 248, 240)
    pdf.set_draw_color(180, 140, 80)
    pdf.set_line_width(0.4)
    pdf.polygon(diamond, style="DF")
    pdf.set_draw_color(180, 140, 80)
    pdf.set_line_width(0.25)
    pdf.line(cx - half, cy, cx + half, cy)
    pdf.line(cx, cy - half, cx, cy + half)
    pdf.line(cx + half, cy - half, cx - half, cy + half)
    pdf.line(cx - half, cy - half, cx + half, cy + half)
    c_diamond = [(cx, cy - quarter), (cx + quarter, cy), (cx, cy + quarter), (cx - quarter, cy)]
    pdf.set_fill_color(255, 252, 245)
    pdf.polygon(c_diamond, style="DF")
    pdf.set_font("Helvetica", "", 5.5)
    pdf.set_text_color(160, 120, 70)
    hn_pos = {
        1: (cx - quarter + 2, cy - 2), 2: (cx + 2, cy - half + 4),
        3: (cx + half - 8, cy - half + 4), 4: (cx + half - 8, cy - 2),
        5: (cx + half - 8, cy + half - 4), 6: (cx + 2, cy + half - 4),
        7: (cx - quarter + 2, cy + half - 4), 8: (cx - half + 2, cy + half - 4),
        9: (cx - half + 2, cy + 2), 10: (cx - half + 2, cy - half + 4),
        11: (cx - quarter - 2, cy - half + 4), 12: (cx - quarter + 2, cy - 2),
    }
    for hnum, (hx, hy) in hn_pos.items():
        pdf.set_xy(hx, hy)
        pdf.cell(4, 3, str(hnum), align="C")
    pdf.set_font("Helvetica", "B", 6.0)
    pdf.set_text_color(45, 45, 45)
    def _wrap_tokens(tokens, max_w, max_lines):
        lines = []
        cur = ""
        for t in tokens:
            test = cur + (", " if cur else "") + t
            if pdf.get_string_width(test) > max_w and cur:
                lines.append(cur)
                cur = t
                if len(lines) >= max_lines:
                    break
            else:
                cur = test
        if cur and len(lines) < max_lines:
            lines.append(cur)
        return lines
    lp = {
        1: (cx - quarter * 0.7, cy - quarter * 0.7), 2: (cx + quarter * 0.5, cy - half * 0.75),
        3: (cx + half * 0.75, cy - quarter * 0.5), 4: (cx + quarter * 0.7, cy + quarter * 0.7),
        5: (cx + half * 0.75, cy + quarter * 0.5), 6: (cx + quarter * 0.5, cy + half * 0.75),
        7: (cx + quarter * 0.7, cy + quarter * 0.7), 8: (cx - quarter * 0.5, cy + half * 0.75),
        9: (cx - half * 0.75, cy + quarter * 0.5), 10: (cx - quarter * 0.7, cy - quarter * 0.7),
        11: (cx - half * 0.75, cy - quarter * 0.5), 12: (cx - quarter * 0.5, cy - half * 0.75),
    }
    max_tw = size * 0.28
    lh = size * 0.045
    for hnum in range(1, 13):
        tokens = planets_in_houses.get(hnum, [])
        if not tokens:
            continue
        lx, ly = lp.get(hnum, (cx, cy))
        wrapped = _wrap_tokens(tokens, max_tw, 3)
        bh = len(wrapped) * lh
        sy = ly - bh / 2
        for li, lt in enumerate(wrapped):
            tw = pdf.get_string_width(lt)
            pdf.set_xy(lx - tw / 2, sy + li * lh)
            pdf.cell(tw, lh, lt, align="C")
    if show_title and title:
        pdf.set_font("Helvetica", "B", 7.5)
        pdf.set_text_color(184, 72, 20)
        tw = pdf.get_string_width(title)
        pdf.set_xy(cx - tw / 2, y - 6)
        pdf.cell(tw, 5, title, align="C")
    pdf.set_text_color(45, 45, 45)
    pdf.set_line_width(0.2)
    return y + size + 4


# ------------------------------------------------------------------
# PROFESSIONAL PDF CLASS
# ------------------------------------------------------------------
class ProfessionalPDF(FPDF):
    SAFFRON = (184, 72, 20)
    DARK = (45, 45, 45)
    GOLD = (200, 138, 56)
    GOLD_LIGHT = (245, 235, 210)
    CREAM = (253, 248, 240)
    WHITE = (255, 255, 255)
    GREEN = (46, 125, 50)
    RED = (198, 40, 40)
    MUTED = (141, 127, 114)
    BLUE = (25, 103, 210)
    HEADER_BG = (184, 72, 20)
    INFO_BOX_BG = (245, 248, 255)
    WARNING_BG = (255, 248, 235)
    SUCCESS_BG = (240, 250, 240)

    def __init__(self, unit="mm", format="A4"):
        super().__init__(unit=unit, format=format)
        self.set_auto_page_break(auto=True, margin=15)
        self._section_stack = []
        self._toc_entries = []
        self._bookmarks = []
        self._layout_warnings = []
        self._current_section = ""

    def header(self):
        if self.page_no() == 1:
            return
        self.set_draw_color(*self.GOLD)
        self.set_line_width(0.5)
        self.line(self.l_margin, 10, self.w - self.r_margin, 10)
        if self._current_section:
            self.set_font("Helvetica", "I", 7)
            self.set_text_color(*self.MUTED)
            self.set_xy(self.l_margin, 5)
            self.cell(0, 4, self._current_section, align="L")
            self.set_text_color(*self.DARK)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-12)
        self.set_draw_color(*self.GOLD)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*self.MUTED)
        self.cell(0, 5, f"Page {self.page_no()}", align="C")

    def cell(self, w=0, h=0, txt="", border=0, align="", fill=False, link="", center=False, new_x="RIGHT", new_y="TOP"):
        return super().cell(w, h, _sanitize(txt), border=border, align=align, fill=fill, link=link, center=center, new_x=new_x, new_y=new_y)

    def multi_cell(self, w, h=0, txt="", border=0, align="", fill=False, link="", split_only=False, padding=0, new_x="LMARGIN", new_y="NEXT"):
        return super().multi_cell(w, h, _sanitize(txt), border=border, align=align, fill=fill, link=link, split_only=split_only, padding=padding, new_x=new_x, new_y=new_y)

    def section_title(self, title: str, level: int = 0):
        self._current_section = title
        self._section_stack = [title]
        self._toc_entries.append((title, level, self.page_no()))
        self._bookmarks.append((title, level, self.page_no()))
        self.check_space(18)
        bar_h = 10
        self.set_fill_color(*self.HEADER_BG)
        self.set_draw_color(*self.HEADER_BG)
        self.rect(self.l_margin, self.get_y(), self.w - self.l_margin - self.r_margin, bar_h, style="F")
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*self.WHITE)
        self.set_xy(self.l_margin + 3, self.get_y() + 2.5)
        self.cell(0, 5, title)
        self.set_text_color(*self.DARK)
        self.ln(bar_h + 3)

    def sub_section(self, title: str):
        self.check_space(10)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*self.SAFFRON)
        self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.GOLD)
        self.set_line_width(0.5)
        y = self.get_y()
        self.line(self.l_margin, y, self.l_margin + min(80, self.get_string_width(title) + 10), y)
        self.set_text_color(*self.DARK)
        self.ln(2)

    def minor_heading(self, text: str):
        self.check_space(7)
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(*self.DARK)
        self.cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(0.5)

    def body_text(self, text: str, indent: float = 0):
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.DARK)
        if indent:
            self.set_x(self.l_margin + indent)
        self.multi_cell(self.w - self.l_margin - self.r_margin - indent, 4.2, text)
        self.ln(1)

    def italic_note(self, text: str):
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*self.MUTED)
        self.multi_cell(0, 3.8, text)
        self.set_text_color(*self.DARK)
        self.ln(1)

    def info_box(self, title: str, text: str, box_type: str = "info"):
        colors = {
            "info": (self.INFO_BOX_BG, self.BLUE),
            "warning": (self.WARNING_BG, self.GOLD),
            "success": (self.SUCCESS_BG, self.GREEN),
            "danger": ((255, 240, 240), self.RED),
        }
        bg, border = colors.get(box_type, colors["info"])
        self.check_space(22)
        pad = 3
        x = self.l_margin
        w = self.w - self.l_margin - self.r_margin
        start_y = self.get_y()
        self.set_font("Helvetica", "", 7.5)
        self.set_xy(x + pad, start_y + pad)
        content = text
        if title:
            content = text
        self.multi_cell(w - pad * 2, 3.8, content)
        box_h = self.get_y() - start_y + pad
        self.set_fill_color(*bg)
        self.set_draw_color(*border)
        self.set_line_width(0.4)
        self.rect(x, start_y, w, box_h, style="FD")
        self.set_fill_color(*border)
        self.rect(x, start_y, 1.5, box_h, style="F")
        if title:
            self.set_font("Helvetica", "B", 7.5)
            self.set_text_color(*border)
            self.set_xy(x + pad + 2, start_y + pad)
            self.cell(0, 4, title)
            self.ln(4.5)
            self.set_xy(x + pad + 2, self.get_y())
            self.set_font("Helvetica", "", 7.5)
            self.set_text_color(*self.DARK)
            self.multi_cell(w - pad * 2 - 2, 3.8, content)
        else:
            self.set_xy(x + pad + 2, start_y + pad)
            self.set_font("Helvetica", "", 7.5)
            self.set_text_color(*self.DARK)
            self.multi_cell(w - pad * 2 - 2, 3.8, content)
        self.set_text_color(*self.DARK)
        self.set_xy(self.l_margin, start_y + box_h + 2)

    def key_observation(self, label: str, value: str, observation: str = ""):
        self.check_space(16)
        x = self.l_margin
        w = self.w - self.l_margin - self.r_margin
        start_y = self.get_y()
        self.set_fill_color(255, 252, 245)
        self.set_draw_color(*self.GOLD)
        self.set_line_width(0.3)
        self.rect(x, start_y, w, 12, style="FD")
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.SAFFRON)
        self.set_xy(x + 3, start_y + 2.5)
        self.cell(0, 4, f"{label}:  ")
        self.set_text_color(*self.DARK)
        self.set_font("Helvetica", "B", 8)
        self.cell(0, 4, value)
        if observation:
            self.set_xy(x + 3, start_y + 7)
            self.set_font("Helvetica", "I", 6.5)
            self.set_text_color(*self.MUTED)
            self.cell(0, 4, observation)
        self.set_text_color(*self.DARK)
        self.set_xy(self.l_margin, start_y + 14)

    def table_header(self, cols, widths, font_size=7):
        self.set_font("Helvetica", "B", font_size)
        self.set_fill_color(*self.HEADER_BG)
        self.set_text_color(*self.WHITE)
        self.set_draw_color(160, 110, 60)
        self.set_line_width(0.25)
        for col, w in zip(cols, widths):
            self.cell(w, 5.5, str(col), border=1, align="C", fill=True)
        self.ln()
        self.set_text_color(*self.DARK)

    def table_row(self, vals, widths, row_idx=0, font_size=6.8, aligns=None):
        if aligns is None:
            aligns = ["C"] * len(vals)
        self.set_font("Helvetica", "", font_size)
        if row_idx % 2 == 1:
            self.set_fill_color(250, 246, 240)
        else:
            self.set_fill_color(*self.WHITE)
        self.set_draw_color(210, 200, 188)
        for val, w, align in zip(vals, widths, aligns):
            self.cell(w, 4.5, str(val), border=1, align=align, fill=True)
        self.ln()
        self.set_fill_color(*self.WHITE)

    def kv_table(self, rows, col_widths=(55, 125)):
        lw, vw = col_widths
        for i, (label, value) in enumerate(rows):
            if not _has_meaningful(value):
                continue
            self.set_font("Helvetica", "B", 7.5)
            self.set_fill_color(250, 246, 240)
            self.set_draw_color(210, 200, 188)
            self.cell(lw, 5, str(label), border="LR", align="L", fill=True)
            self.set_font("Helvetica", "", 7.5)
            self.cell(vw, 5, str(value), border="LR", align="L", fill=True)
            self.ln()
        self.set_draw_color(210, 200, 188)
        self.cell(lw + vw, 0.3, "", border="T")
        self.ln(1)

    def data_table(self, headers, rows, widths, font_size=6.8, aligns=None):
        if not rows:
            self.italic_note("No data available for this table.")
            return
        self.table_header(headers, widths, font_size)
        for ri, row in enumerate(rows):
            str_row = [str(c) for c in row]
            self.table_row(str_row, widths, ri, font_size, aligns)
        self.ln(2)

    def two_column_kv(self, left_items, right_items, label_w=40, value_w=48):
        max_rows = max(len(left_items), len(right_items))
        start_y = self.get_y()
        left_x = self.l_margin
        right_x = self.l_margin + label_w + value_w + 8
        for i in range(max_rows):
            row_y = start_y + i * 6.5
            if row_y > self.h - 20:
                self.add_page()
                start_y = self.get_y()
                row_y = start_y
            if i < len(left_items):
                label, value = left_items[i]
                if _has_meaningful(value):
                    self.set_xy(left_x, row_y)
                    self.set_font("Helvetica", "B", 7.5)
                    self.set_text_color(*self.MUTED)
                    self.cell(label_w, 5, label)
                    self.set_text_color(*self.DARK)
                    self.set_font("Helvetica", "", 7.5)
                    self.cell(value_w, 5, str(value))
            if i < len(right_items):
                label, value = right_items[i]
                if _has_meaningful(value):
                    self.set_xy(right_x, row_y)
                    self.set_font("Helvetica", "B", 7.5)
                    self.set_text_color(*self.MUTED)
                    self.cell(label_w, 5, label)
                    self.set_text_color(*self.DARK)
                    self.set_font("Helvetica", "", 7.5)
                    self.cell(value_w, 5, str(value))
        self.set_y(start_y + max_rows * 6.5 + 2)

    def check_space(self, needed=25):
        if self.get_y() + needed > self.h - 15:
            self.add_page()

    def render_toc(self, title="Table of Contents"):
        self.add_page()
        self.section_title(title)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*self.DARK)
        for entry_title, level, page in self._toc_entries:
            indent = level * 5
            self.set_x(self.l_margin + indent)
            self.set_font("Helvetica", "B" if level == 0 else "", 9 if level == 0 else 8)
            title_w = self.get_string_width(entry_title)
            dots_w = self.w - self.l_margin - self.r_margin - indent - title_w - 15
            dots = "." * int(dots_w / 1.8)
            self.cell(title_w + 2, 6, entry_title)
            self.set_font("Helvetica", "", 8)
            self.set_text_color(*self.MUTED)
            self.cell(dots_w, 6, dots)
            self.set_text_color(*self.DARK)
            self.cell(10, 6, str(page), align="R")
            self.ln()
        self.ln(4)
''')

print("Part 2 done")
