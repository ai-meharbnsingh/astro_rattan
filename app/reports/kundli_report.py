
"""
Kundli Full Report PDF Generator - Parashara's Light Style
==========================================================
"""
from __future__ import annotations

import math
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from fpdf import FPDF

# ------------------------------------------------------------------
# CONSTANTS & UTILITIES
# ------------------------------------------------------------------
SIGN_SHORT = ["Ar", "Ta", "Ge", "Ca", "Le", "Vi", "Li", "Sc", "Sa", "Cp", "Aq", "Pi"]
SIGN_ORDER = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
PLANET_LIST_9 = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
PLANET_ABBR = {
    "Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me",
    "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa", "Rahu": "Ra", "Ketu": "Ke",
    "Ascendant": "As", "Lagna": "As", "BhaavaPada": "BP", "Dhuma": "Dh", "Gulika": "Gk"
}

def _sg(data, *keys, default="-"):
    for k in keys:
        if isinstance(data, dict):
            data = data.get(k, default)
        else:
            data = default
            break
    
    val = data if data is not None and data != "N/A" else default
    # Always convert to string for FPDF
    val = str(val)
    
    # Basic sanitization for latin-1
    val = val.replace("\u2014", "-").replace("\u2013", "-").replace("\u2018", "'").replace("\u2019", "'")
    val = val.replace("\u201c", '"').replace("\u201d", '"').replace("\u2022", "*")
    try:
        val.encode("latin-1")
    except UnicodeEncodeError:
        val = val.encode("ascii", "ignore").decode("ascii")
    return val

def _fmt_deg(deg):
    if deg == "-" or deg is None: return "-"
    try:
        d = float(deg)
        w = int(d)
        m = int(round((d - w) * 60))
        if m == 60: w += 1; m = 0
        return f"{w:02d}:{m:02d}"
    except: return str(deg)

def _fmt_dms(deg):
    if deg == "-" or deg is None: return "-"
    try:
        d = float(deg)
        w = int(d)
        m_f = (d - w) * 60
        m = int(m_f)
        s = int(round((m_f - m) * 60))
        if s == 60: m += 1; s = 0
        if m == 60: w += 1; m = 0
        return f"{w:02d}:{m:02d}:{s:02d}"
    except: return str(deg)

# ------------------------------------------------------------------
# CHART DRAWING (FPDF PRIMITIVES)
# ------------------------------------------------------------------
def _draw_north_indian_chart(pdf, x, y, size, planets_in_houses, title="", show_title=True, asc_sign_idx=0):
    """Draws a North Indian style diamond chart using FPDF primitives."""
    cx, cy = x + size / 2.0, y + size / 2.0
    half = size / 2.0
    quarter = size / 4.0
    
    # Background and Main outer square
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(x, y, size, size, style="F")
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.1) # 0.3pt approx
    pdf.rect(x, y, size, size)
    
    # Inner diamond
    diamond = [(cx, cy - half), (cx + half, cy), (cx, cy + half), (cx - half, cy)]
    pdf.polygon(diamond)
    
    # Internal lines
    pdf.line(x, y, x + size, y + size)
    pdf.line(x + size, y, x, y + size)
    
    # Small inner diamond
    c_diamond = [(cx, cy - quarter), (cx + quarter, cy), (cx, cy + quarter), (cx - quarter, cy)]
    pdf.polygon(c_diamond)

    # House/Sign numbers (corner triangles)
    pdf.set_font("Helvetica", "", size * 0.04)
    pdf.set_text_color(0, 0, 0)
    
    # Position mappings for sign numbers (relative to cx, cy)
    sn_pos = {
        1: (0, -quarter + 4),    2: (-quarter/2, -half + 6),  3: (-half + 6, -quarter/2),
        4: (-quarter + 4, 0),    5: (-half + 6, quarter/2),   6: (-quarter/2, half - 6),
        7: (0, quarter - 4),     8: (quarter/2, half - 6),    9: (half - 6, quarter/2),
        10: (quarter - 4, 0),    11: (half - 6, -quarter/2),  12: (quarter/2, -half + 6)
    }
    
    for h in range(1, 13):
        sign_num = (asc_sign_idx + h - 1) % 12 + 1
        sx, sy = sn_pos[h]
        pdf.set_xy(cx + sx - 2, cy + sy - 2)
        pdf.cell(4, 4, str(sign_num), align="C")

    # Planet positioning
    pdf.set_font("Helvetica", "", size * 0.05)
    lp = {
        1: (cx, cy - half * 0.35), 
        2: (cx - half * 0.35, cy - half * 0.75),
        3: (cx - half * 0.75, cy - half * 0.35),
        4: (cx - half * 0.35, cy),
        5: (cx - half * 0.75, cy + half * 0.35),
        6: (cx - half * 0.35, cy + half * 0.75),
        7: (cx, cy + half * 0.35),
        8: (cx + half * 0.35, cy + half * 0.75),
        9: (cx + half * 0.75, cy + half * 0.35),
        10: (cx + half * 0.35, cy),
        11: (cx + half * 0.75, cy - half * 0.35),
        12: (cx + half * 0.35, cy - half * 0.75)
    }
    
    for hnum in range(1, 13):
        tokens = planets_in_houses.get(hnum, [])
        if not tokens: continue
        lx, ly = lp[hnum]
        
        # Stack tokens vertically if multiple
        th = 4
        total_h = len(tokens) * th
        curr_y = ly - total_h / 2
        for token in tokens:
            tw = pdf.get_string_width(token)
            pdf.set_xy(lx - tw/2, curr_y)
            pdf.cell(tw, th, token, align="C")
            curr_y += th

    if show_title and title:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(178, 34, 34) # Crimson
        tw = pdf.get_string_width(title)
        pdf.set_xy(cx - tw/2, y - 6)
        pdf.cell(tw, 5, title, align="C")
    
    pdf.set_text_color(0, 0, 0)
    return y + size + 5

# ------------------------------------------------------------------
# PARASHARA PDF CLASS
# ------------------------------------------------------------------
class ParasharaPDF(FPDF):
    def __init__(self, name="Native"):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_margins(15, 18, 15)
        self.person_name = name
        self.current_section = ""
        self.set_auto_page_break(True, margin=18)

    def header(self):
        # Full content area border (0.3pt)
        self.set_line_width(0.1) 
        self.rect(15, 18, 180, 261) 
        
        # Header text
        self.set_font("Helvetica", "", 8)
        self.set_text_color(0, 0, 0)
        self.set_xy(15, 10)
        self.cell(60, 8, self.person_name, align="L")
        
        # OM Symbol
        self.set_font("Helvetica", "", 14)
        self.set_text_color(178, 34, 34) # Crimson
        self.set_xy(100, 10)
        self.cell(10, 8, "OM", align="C") 
        
        # Section Name
        self.set_font("Helvetica", "", 8)
        self.set_text_color(0, 0, 0)
        self.set_xy(135, 10)
        self.cell(60, 8, self.current_section, align="R")

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "", 7)
        self.set_text_color(128, 128, 128) 
        self.cell(90, 10, "AstroRattan", align="L")
        self.cell(90, 10, f"Page {self.page_no()}", align="R")

    def section_header(self, title):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(178, 34, 34) # Crimson
        self.cell(0, 8, title, ln=True)
        # Underline
        x, y = self.get_x(), self.get_y()
        self.line(15, y-1, 15 + self.get_string_width(title), y-1)
        self.ln(2)

    def draw_table(self, headers, rows, widths, aligns=None, fill_colors=None):
        if not aligns: aligns = ["L"] * len(headers)
        # Header
        self.set_font("Helvetica", "B", 8)
        self.set_fill_color(232, 232, 232)
        for i, h in enumerate(headers):
            self.cell(widths[i], 6, h, border=1, fill=True, align="C")
        self.ln()
        # Rows
        self.set_font("Helvetica", "", 8.5)
        for ri, row in enumerate(rows):
            if fill_colors and ri < len(fill_colors):
                self.set_fill_color(*fill_colors[ri])
            elif ri % 2 == 1: 
                self.set_fill_color(247, 247, 247)
            else: 
                self.set_fill_color(255, 255, 255)
            
            for i, val in enumerate(row):
                self.cell(widths[i], 5, str(val), border=1, fill=True, align=aligns[i])
            self.ln()
        self.ln(1)

# ------------------------------------------------------------------
# REPORT BUILDER
# ------------------------------------------------------------------
def build_full_report(data: dict) -> bytes:
    name = _sg(data, "person_name", default="Native")
    pdf = ParasharaPDF(name=name)
    
    # Common Data
    chart_data = data.get("chart_data", {})
    avakhada = data.get("avakhada", {})
    hc = data.get("hindu_calendar", {})
    panchang = data.get("panchang", {})
    planets = chart_data.get("planets", {})
    asc_sign = _sg(chart_data, "ascendant", "sign", default="Aries")
    asc_idx = SIGN_ORDER.index(asc_sign) if asc_sign in SIGN_ORDER else 0
    
    # --------------------------------------------------------------
    # PAGE 1 - Birth Particulars & Hindu Calendar
    # --------------------------------------------------------------
    pdf.current_section = "Birth Particulars"
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, name, ln=True, align="C")
    pdf.ln(5)
    
    start_y = pdf.get_y()
    
    # LEFT COLUMN
    pdf.set_xy(15, start_y)
    pdf.section_header("Birth Particulars")
    bp_data = [
        ("Sex", _sg(data, "gender")),
        ("Date of Birth", f"**{_sg(data, 'birth_date')}**"),
        ("Day of Birth", _sg(data, "day_of_birth")),
        ("Time of Birth", f"**{_sg(data, 'birth_time')}**"),
        ("Place of Birth", f"**{_sg(data, 'birth_place')}**"),
        ("Country", _sg(data, "country")),
        ("---", ""),
        ("Latitude", _sg(data, "latitude")),
        ("Longitude", _sg(data, "longitude")),
        ("Timezone", _sg(data, "timezone")),
        ("GMT at birth", _sg(data, "gmt_offset")),
        ("Sidereal Time", _sg(chart_data, "sidereal_time")),
        ("Ayanamsha", _sg(chart_data, "ayanamsa_name"))
    ]
    for k, v in bp_data:
        if k == "---":
            pdf.line(15, pdf.get_y(), 100, pdf.get_y()); pdf.ln(1); continue
        pdf.set_font("Helvetica", "", 8.5)
        pdf.cell(35, 5, k + " : ")
        if "**" in str(v): pdf.set_font("Helvetica", "B", 8.5)
        pdf.cell(50, 5, str(v).replace("**", ""), ln=True)

    pdf.ln(4)
    pdf.section_header("Avakhada Chakra")
    avk_data = [
        ("Varna", _sg(avakhada, "varna")), ("Vashya", _sg(avakhada, "vashya")),
        ("Nakshatra-Pada", f"**{_sg(avakhada, 'nakshatra')}-{_sg(avakhada, 'nakshatra_pada')}**"),
        ("Yoni", _sg(avakhada, "yoni")), ("Rashish", _sg(avakhada, "rashi_lord")),
        ("Gana", _sg(avakhada, "gana")), ("Rashi", f"**{_sg(avakhada, 'rashi')}**"),
        ("Nadi", _sg(avakhada, "nadi")), ("Varga", _sg(avakhada, "varga")),
        ("Yunja", _sg(avakhada, "yunja")), ("Hansak(Tatwa)", _sg(avakhada, "tatva")),
        ("Naamakshar", _sg(avakhada, "naamakshar")),
        ("Paya (Rashi)", f"**{_sg(avakhada, 'paya_rashi')}**"),
        ("Paya (Nakshatra)", f"**{_sg(avakhada, 'paya_nakshatra')}**")
    ]
    for k, v in avk_data:
        pdf.set_font("Helvetica", "", 8.5)
        pdf.cell(35, 5, k + " : ")
        if "**" in str(v): pdf.set_font("Helvetica", "B", 8.5)
        pdf.cell(50, 5, str(v).replace("**", ""), ln=True)

    # RIGHT COLUMN
    pdf.set_xy(110, start_y)
    pdf.section_header("Hindu Calendar")
    pdf.set_font("Helvetica", "BI", 8); pdf.cell(0, 5, "Chaitradi System", ln=True)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.cell(40, 5, "Vikram Samvat : "); pdf.cell(0, 5, _sg(hc, "vikram_samvat"), ln=True)
    pdf.cell(40, 5, "Lunar Month : "); pdf.cell(0, 5, _sg(hc, "maas"), ln=True)
    pdf.ln(2)
    pdf.cell(40, 5, "Saka Samvat : "); pdf.cell(0, 5, _sg(hc, "shaka_samvat"), ln=True)
    pdf.cell(40, 5, "Ayana/Gola : "); pdf.cell(0, 5, f"{_sg(hc, 'ayana')}/{_sg(hc, 'gola')}", ln=True)
    pdf.cell(40, 5, "Season : "); pdf.cell(0, 5, _sg(hc, "ritu"), ln=True)
    pdf.set_font("Helvetica", "B", 8.5); pdf.cell(40, 5, "Paksha : "); pdf.cell(0, 5, _sg(hc, "paksha"), ln=True)
    pdf.set_font("Helvetica", "", 8.5); pdf.cell(40, 5, "Weekday : "); pdf.cell(0, 5, _sg(panchang, "vaar", "name"), ln=True)
    pdf.line(110, pdf.get_y(), 195, pdf.get_y()); pdf.ln(1)
    
    for lbl, key in [("Tithi", "tithi"), ("Nakshatra", "nakshatra"), ("Yoga", "yoga"), ("Karana", "karana")]:
        pdf.cell(40, 4.5, f"{lbl} at sunrise : "); pdf.cell(0, 4.5, _sg(panchang, key, "name"), ln=True)
        pdf.cell(40, 4.5, "Ending time : "); pdf.cell(0, 4.5, _sg(panchang, key, "end_time"), ln=True)
        pdf.set_font("Helvetica", "B", 8.5); pdf.cell(40, 4.5, f"{lbl} at birth : "); pdf.cell(0, 4.5, _sg(panchang, key, "name"), ln=True); pdf.set_font("Helvetica", "", 8.5)
        pdf.line(110, pdf.get_y(), 195, pdf.get_y()); pdf.ln(0.5)

    pdf.cell(40, 5, "Sunrise/Sunset : "); pdf.cell(0, 5, f"{_sg(panchang, 'sunrise')} / {_sg(panchang, 'sunset')}", ln=True)
    pdf.cell(40, 5, "Dasha at Birth : "); pdf.cell(0, 5, _sg(data, "dasha", "current_dasha"), ln=True)
    pdf.cell(40, 5, "Balance of Dasha: "); pdf.cell(0, 5, _sg(data, "dasha", "balance"), ln=True)

    # --------------------------------------------------------------
    # PAGE 2 - Birth Chart (Lagna)
    # --------------------------------------------------------------
    pdf.current_section = "Birth Chart"
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 9); pdf.set_text_color(178, 34, 34)
    pdf.cell(0, 10, f"{_sg(data, 'birth_date')} | {_sg(data, 'day_of_birth')} | {_sg(data, 'birth_time')} | {_sg(data, 'birth_place')}", align="C", ln=True)
    
    # Lagna Chart
    pih = {}
    if "Ascendant" not in planets and "Lagna" not in planets:
        asc_info = chart_data.get("ascendant", {})
        pih.setdefault(1, []).append(f"As {_fmt_deg(asc_info.get('sign_degree', asc_info.get('degree')))}")
    for p, info in planets.items():
        h = info.get("house", 1); abbr = PLANET_ABBR.get(p, p[:2])
        if info.get("retrograde"): abbr += "R"
        deg_str = _fmt_deg(info.get("sign_degree", info.get("degree")))
        pih.setdefault(h, []).append(f"{abbr} {deg_str}")
    _draw_north_indian_chart(pdf, 45, 40, 120, pih, "LAGNA CHART", asc_sign_idx=asc_idx)
    
    # Moon & Navamsha
    m_sign = _sg(planets, "Moon", "sign", default="Aries")
    m_idx = SIGN_ORDER.index(m_sign) if m_sign in SIGN_ORDER else 0
    m_pih = {}
    for p, info in planets.items():
        p_sign = info.get("sign", "Aries")
        p_idx = SIGN_ORDER.index(p_sign) if p_sign in SIGN_ORDER else 0
        h_rel = (p_idx - m_idx) % 12 + 1
        m_pih.setdefault(h_rel, []).append(PLANET_ABBR.get(p, p[:2]))
    _draw_north_indian_chart(pdf, 20, 170, 70, m_pih, "MOON CHART", asc_sign_idx=m_idx)
    
    d9_pih = {}
    d9_info = data.get("divisional", {}).get("D9", {})
    d9_planets = d9_info.get("planets", {})
    d9_asc_sign = d9_info.get("ascendant", {}).get("sign", "Aries")
    d9_asc_idx = SIGN_ORDER.index(d9_asc_sign) if d9_asc_sign in SIGN_ORDER else 0
    for p, info in d9_planets.items():
        h = info.get("house", 1); d9_pih.setdefault(h, []).append(PLANET_ABBR.get(p, p[:2]))
    _draw_north_indian_chart(pdf, 120, 170, 70, d9_pih, "NAVAMSHA (D9)", asc_sign_idx=d9_asc_idx)
    
    # Planet Table
    pdf.set_y(245)
    headers = ["Planet", "R/C", "Sign", "Degree", "Speed", "Nakshatra", "Pada", "RL", "NL", "SL", "SS", "Status", "SB"]
    widths = [16, 8, 14, 16, 16, 22, 8, 8, 8, 8, 8, 14, 10]
    p_rows = []
    shadbala = data.get("shadbala", {}).get("planets", {})
    for p in ["Ascendant", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        info = planets.get(p, {}) if p != "Ascendant" else chart_data.get("ascendant", {})
        rc = ("R" if info.get("retrograde") else "") + ("C" if info.get("combust") else "")
        sb_val = _sg(shadbala, p, "total", default=0.0)
        p_rows.append([PLANET_ABBR.get(p, p), rc, _sg(info, "sign")[:3], _fmt_deg(info.get("sign_degree", info.get("degree"))), "-", _sg(info, "nakshatra")[:5], _sg(info, "nakshatra_pada"), "-", "-", "-", "-", "-", f"{float(sb_val):.2f}"])
    pdf.draw_table(headers, p_rows, widths)

    # --------------------------------------------------------------
    # PAGE 3 - Moon, Navamsha, Bhava Charts + Bhava Table
    # --------------------------------------------------------------
    pdf.current_section = "Chandra, Navamsha and Bhava"
    pdf.add_page()
    _draw_north_indian_chart(pdf, 15, 30, 80, m_pih, "Moon Chart", asc_sign_idx=m_idx)
    _draw_north_indian_chart(pdf, 115, 30, 80, d9_pih, "Navamsha", asc_sign_idx=d9_asc_idx)
    
    # Bhava Chart
    bh_pih = {}
    for p, info in planets.items(): bh_pih.setdefault(info.get("house", 1), []).append(PLANET_ABBR.get(p, p[:2]))
    _draw_north_indian_chart(pdf, 60, 120, 90, bh_pih, "Bhava (Sripati)", asc_sign_idx=asc_idx)
    
    pdf.set_y(220); pdf.section_header("Bhava Spashta - Sripati System")
    bh_rows = []
    for i, h in enumerate(chart_data.get("houses", [])):
        bh_rows.append([f"House {i+1}", _fmt_dms(h.get("begin")), _fmt_dms(h.get("middle")), _fmt_dms(h.get("end"))])
    pdf.draw_table(["Bhava Number", "Bhava Arambha", "Bhava Madhya", "Bhava Antya"], bh_rows, [45]*4)

    # --------------------------------------------------------------
    # PAGE 4 & 5 - Divisional Charts
    # --------------------------------------------------------------
    v_groups = [["D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12"], ["D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60"]]
    for idx, group in enumerate(v_groups):
        pdf.current_section = f"Divisional Charts #{idx+1}"; pdf.add_page()
        for i, v in enumerate(group):
            v_data = data.get("divisional", {}).get(v, {}).get("planets", {})
            v_pih = {}
            for p, info in v_data.items(): v_pih.setdefault(info.get("house", 1), []).append(PLANET_ABBR.get(p, p[:2]))
            _draw_north_indian_chart(pdf, 15 + (i%2)*95 + 15, 30 + (i//2)*65, 55, v_pih, f"{v}: {VARGA_NAMES.get(v, '')}")

    # --------------------------------------------------------------
    # PAGE 6 - Planetary Friendship
    # --------------------------------------------------------------
    pdf.current_section = "Planetary Friendship"; pdf.add_page()
    for t in ["Naisargik Maitri Chakra (Natural Relationship)", "Tatkalik Maitri Chakra (Temporal Relationship)", "Panchadha Maitri Chakra (Compound Relationship)"]:
        pdf.section_header(t); pdf.draw_table([""] + PLANET_LIST_9, [["Friends"]+["-"]*9, ["Enemies"]+["-"]*9, ["Neutral"]+["-"]*9], [18]+[17]*9)
        pdf.ln(3)

    # --------------------------------------------------------------
    # PAGE 7 - Shodashvarga Summary
    # --------------------------------------------------------------
    pdf.current_section = "Shodashvarga Summary"; pdf.add_page()
    pdf.set_font("Helvetica", "B", 11); pdf.cell(0, 10, "Shodashvarga Summary", align="C", ln=True)
    for t in ["Signs occupied", "Dignities", "Vimshopaka Bala", "Dispositors"]:
        pdf.section_header(t); pdf.draw_table(["Lagna"] + PLANET_LIST_9, [["-"]*10]*4, [18]*10)
        pdf.ln(2)

    # --------------------------------------------------------------
    # PAGE 8 - Shadbala & Bhava Bala
    # --------------------------------------------------------------
    pdf.current_section = "Shad Bala and Bhava Bala"; pdf.add_page()
    pdf.section_header("Shad Bala"); pdf.draw_table(["Component"] + PLANET_LIST_9[:7], [["Sthana Bala"]+["-"]*7, ["Total Shadbala"]+["-"]*7], [32]+[22]*7)
    pdf.ln(5); pdf.section_header("Bhava Bala")
    pdf.draw_table(["Component"]+["I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII"], [["Rashi"]+SIGN_SHORT, ["Total"]+["-"]*12], [32]+[12.3]*12)

    # --------------------------------------------------------------
    # PAGE 9 - Aspects
    # --------------------------------------------------------------
    pdf.current_section = "Aspects on Planets and Bhavas"; pdf.add_page()
    pdf.section_header("Aspects on Planets"); pdf.draw_table(["Aspected"]+PLANET_LIST_9, [["-"]*10]*9, [18]*10)
    pdf.ln(5); pdf.section_header("Aspects on Bhavas"); pdf.draw_table(["Aspected"]+PLANET_LIST_9, [["-"]*10]*12, [18]*10)

    # --------------------------------------------------------------
    # PAGE 10 - Dasha
    # --------------------------------------------------------------
    pdf.current_section = "Vimshottari Dasha"; pdf.add_page()
    d = data.get("dasha", {})
    pdf.set_font("Helvetica", "B", 9); pdf.set_text_color(178, 34, 34)
    pdf.cell(0, 10, f"Dasha at birth: {_sg(d, 'current_dasha')} | Balance: {_sg(d, 'balance')}", ln=True)
    pdf.section_header("Mahadasha periods"); d_rows = []
    for md in d.get("mahadasha", []): d_rows.append([md.get("planet"), md.get("start"), md.get("end"), md.get("years")])
    pdf.draw_table(["Mahadasha Lord", "Start Date", "End Date", "Years"], d_rows or [["-"]*4], [45]*4)

    # --------------------------------------------------------------
    # PAGE 11 - Ashtakvarga
    # --------------------------------------------------------------
    pdf.current_section = "Ashtakvarga"; pdf.add_page()
    pdf.section_header("Bhinnashtakvarga")
    for i in range(7):
        pdf.set_font("Helvetica", "B", 8); pdf.cell(0, 5, PLANET_LIST_9[i], ln=True)
        pdf.draw_table(SIGN_SHORT, [["-"]*12], [15]*12)
    pdf.ln(2); pdf.section_header("Sarvashtakvarga (SAV)")
    pdf.draw_table(SIGN_SHORT, [["-"]*12], [15]*12)

    return pdf.output()

VARGA_NAMES = {
    "D1": "Rashi", "D2": "Hora", "D3": "Drekkana", "D4": "Chaturthamsha",
    "D7": "Saptamsha", "D9": "Navamsha", "D10": "Dashamsha", "D12": "Dwadashamsha",
    "D16": "Shodashamsha", "D20": "Vimshamsha", "D24": "Chaturvimshamsha",
    "D27": "Saptavimshamsha", "D30": "Trimshamsha", "D40": "Khavedamsha",
    "D45": "Akshavedamsha", "D60": "Shashtiamsha"
}
