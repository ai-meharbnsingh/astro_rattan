"""Panchang routes — daily panchang, choghadiya, muhurat, sunrise, festivals, monthly view, and PDF download."""
import io
import json
import os
import calendar
from typing import Any
from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse

from app.database import get_db
from app.panchang_engine import (
    calculate_panchang,
    calculate_rahu_kaal,
    calculate_choghadiya,
)
from app.festival_engine import detect_festivals


# ============================================================
# Hindi translation mappings for bilingual PDF
# ============================================================

HINDI_DAYS = {
    'Sunday': 'रविवार', 'Monday': 'सोमवार', 'Tuesday': 'मंगलवार',
    'Wednesday': 'बुधवार', 'Thursday': 'गुरुवार', 'Friday': 'शुक्रवार',
    'Saturday': 'शनिवार',
}

HINDI_MONTHS_ENG = {
    1: 'जनवरी', 2: 'फरवरी', 3: 'मार्च', 4: 'अप्रैल', 5: 'मई', 6: 'जून',
    7: 'जुलाई', 8: 'अगस्त', 9: 'सितंबर', 10: 'अक्टूबर', 11: 'नवंबर', 12: 'दिसंबर',
}

HINDI_NAKSHATRAS = {
    'Ashwini': 'अश्विनी', 'Bharani': 'भरणी', 'Krittika': 'कृत्तिका',
    'Rohini': 'रोहिणी', 'Mrigashira': 'मृगशिरा', 'Ardra': 'आर्द्रा',
    'Punarvasu': 'पुनर्वसु', 'Pushya': 'पुष्य', 'Ashlesha': 'अश्लेषा',
    'Magha': 'मघा', 'Purva Phalguni': 'पूर्व फाल्गुनी', 'Uttara Phalguni': 'उत्तर फाल्गुनी',
    'Hasta': 'हस्त', 'Chitra': 'चित्रा', 'Swati': 'स्वाति',
    'Vishakha': 'विशाखा', 'Anuradha': 'अनुराधा', 'Jyeshtha': 'ज्येष्ठा',
    'Mula': 'मूल', 'Purva Ashadha': 'पूर्व आषाढ़ा', 'Uttara Ashadha': 'उत्तर आषाढ़ा',
    'Shravana': 'श्रवण', 'Dhanishta': 'धनिष्ठा', 'Shatabhisha': 'शतभिषा',
    'Purva Bhadrapada': 'पूर्व भाद्रपद', 'Uttara Bhadrapada': 'उत्तर भाद्रपद', 'Revati': 'रेवती',
}

HINDI_MAAS = {
    'Chaitra': 'चैत्र', 'Vaishakha': 'वैशाख', 'Jyeshtha': 'ज्येष्ठ',
    'Ashadha': 'आषाढ़', 'Shravana': 'श्रावण', 'Bhadrapada': 'भाद्रपद',
    'Ashwin': 'आश्विन', 'Kartik': 'कार्तिक', 'Margashirsha': 'मार्गशीर्ष',
    'Pausha': 'पौष', 'Magha': 'माघ', 'Phalguna': 'फाल्गुन',
}

HINDI_TITHIS = {
    'Pratipada': 'प्रतिपदा', 'Dwitiya': 'द्वितीया', 'Tritiya': 'तृतीया',
    'Chaturthi': 'चतुर्थी', 'Panchami': 'पंचमी', 'Shashthi': 'षष्ठी',
    'Saptami': 'सप्तमी', 'Ashtami': 'अष्टमी', 'Navami': 'नवमी',
    'Dashami': 'दशमी', 'Ekadashi': 'एकादशी', 'Dwadashi': 'द्वादशी',
    'Trayodashi': 'त्रयोदशी', 'Chaturdashi': 'चतुर्दशी',
    'Purnima': 'पूर्णिमा', 'Amavasya': 'अमावस्या',
}

HINDI_PAKSHA = {'Shukla': 'शुक्ल', 'Krishna': 'कृष्ण'}
HINDI_AYANA = {'Uttarayana': 'उत्तरायण', 'Dakshinayana': 'दक्षिणायन'}
HINDI_RITU = {
    'Vasanta': 'वसंत', 'Grishma': 'ग्रीष्म', 'Varsha': 'वर्षा',
    'Sharad': 'शरद', 'Hemanta': 'हेमंत', 'Shishira': 'शिशिर',
}

HINDI_RASHIS = {
    'Aries': 'मेष', 'Taurus': 'वृषभ', 'Gemini': 'मिथुन', 'Cancer': 'कर्क',
    'Leo': 'सिंह', 'Virgo': 'कन्या', 'Libra': 'तुला', 'Scorpio': 'वृश्चिक',
    'Sagittarius': 'धनु', 'Capricorn': 'मकर', 'Aquarius': 'कुम्भ', 'Pisces': 'मीन',
}

HINDI_YOGAS = {
    'Vishkumbha': 'विष्कम्भ', 'Priti': 'प्रीति', 'Ayushman': 'आयुष्मान',
    'Saubhagya': 'सौभाग्य', 'Shobhana': 'शोभन', 'Atiganda': 'अतिगण्ड',
    'Sukarma': 'सुकर्मा', 'Dhriti': 'धृति', 'Shula': 'शूल',
    'Ganda': 'गण्ड', 'Vriddhi': 'वृद्धि', 'Dhruva': 'ध्रुव',
    'Vyaghata': 'व्याघात', 'Harshana': 'हर्षण', 'Vajra': 'वज्र',
    'Siddhi': 'सिद्धि', 'Vyatipata': 'व्यतिपात', 'Variyan': 'वरीयान',
    'Parigha': 'परिघ', 'Shiva': 'शिव', 'Siddha': 'सिद्ध',
    'Sadhya': 'साध्य', 'Shubha': 'शुभ', 'Shukla': 'शुक्ल',
    'Brahma': 'ब्रह्म', 'Indra': 'इन्द्र', 'Vaidhriti': 'वैधृति',
}

HINDI_PLANETS = {
    'Sun': 'सूर्य', 'Moon': 'चन्द्र', 'Mars': 'मंगल', 'Mercury': 'बुध',
    'Jupiter': 'गुरु', 'Venus': 'शुक्र', 'Saturn': 'शनि',
    'Rahu': 'राहु', 'Ketu': 'केतु',
}

HINDI_CHOGHADIYA_QUALITY = {
    'Amrit': 'अमृत', 'Shubh': 'शुभ', 'Labh': 'लाभ', 'Char': 'चर',
    'Rog': 'रोग', 'Kaal': 'काल', 'Udveg': 'उद्वेग',
}

router = APIRouter(tags=["panchang"])


def _today() -> str:
    return date.today().isoformat()


def _parse_date(date_str: str) -> datetime:
    """Parse a date string, raising HTTPException on invalid format."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format: '{date_str}'. Expected YYYY-MM-DD.",
        )


# ============================================================
# GET /api/panchang -- Full daily panchang (enhanced)
# ============================================================

@router.get("/api/panchang", status_code=status.HTTP_200_OK)
def get_panchang(
    date_str: str = Query(default=None, alias="date"),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
    db: Any = Depends(get_db),
):
    """Calculate complete Panchang for a given date and location."""
    target_date = date_str or _today()
    _parse_date(target_date)

    # Check cache first
    cached = db.execute(
        "SELECT * FROM panchang_cache WHERE date = %s AND latitude = %s AND longitude = %s",
        (target_date, latitude, longitude),
    ).fetchone()

    # Serve from cache only if it has extended data (new engine format)
    raw_ext_check = cached.get("choghadiya", "") if cached else ""
    cache_has_extended = cached and raw_ext_check and raw_ext_check not in ("", "[]")

    if cache_has_extended:
        tithi = cached["tithi"]
        if isinstance(tithi, str):
            tithi = json.loads(tithi)
        nakshatra = cached["nakshatra"]
        if isinstance(nakshatra, str):
            nakshatra = json.loads(nakshatra)
        yoga = cached["yoga"]
        if isinstance(yoga, str):
            yoga = json.loads(yoga)
        karana = cached["karana"]
        if isinstance(karana, str):
            karana = json.loads(karana)
        rahu_kaal = cached["rahu_kaal"]
        if isinstance(rahu_kaal, str):
            rahu_kaal = json.loads(rahu_kaal)

        # Try to load extended data from choghadiya column (stores full JSON now)
        extended = {}
        raw_ext = cached.get("choghadiya", "")
        if raw_ext and raw_ext != "[]":
            try:
                extended = json.loads(raw_ext) if isinstance(raw_ext, str) else raw_ext
            except (json.JSONDecodeError, TypeError):
                extended = {}

        result = {
            "date": cached["date"],
            "latitude": cached["latitude"],
            "longitude": cached["longitude"],
            "tithi": tithi,
            "nakshatra": nakshatra,
            "yoga": yoga,
            "karana": karana,
            "rahu_kaal": rahu_kaal,
            "sunrise": cached["sunrise"],
            "sunset": cached["sunset"],
            "moonrise": cached.get("moonrise", "--:--"),
            "moonset": cached.get("moonset", "--:--"),
        }
        # Merge extended data if present
        if isinstance(extended, dict):
            result.update(extended)
        return result

    # Calculate fresh
    panchang = calculate_panchang(target_date, latitude, longitude)

    # Detect festivals
    festivals = detect_festivals(
        tithi_name=panchang["tithi"]["name"],
        paksha=panchang["tithi"]["paksha"],
        nakshatra_name=panchang["nakshatra"]["name"],
        maas=panchang.get("hindu_calendar", {}).get("maas", ""),
    )
    panchang["festivals"] = festivals

    # Build extended data for cache (everything beyond core fields)
    _CORE_KEYS = {"date", "tithi", "nakshatra", "yoga", "karana", "rahu_kaal",
                  "sunrise", "sunset", "moonrise", "moonset", "latitude", "longitude"}
    extended_data = {k: v for k, v in panchang.items() if k not in _CORE_KEYS}
    extended_data["festivals"] = festivals

    # Cache the result
    tithi_str = json.dumps(panchang["tithi"])
    nak_str = json.dumps(panchang["nakshatra"])
    yoga_str = json.dumps(panchang["yoga"])
    karana_str = json.dumps(panchang["karana"])
    rahu_str = json.dumps(panchang.get("rahu_kaal", {}))
    extended_str = json.dumps(extended_data, default=str)

    db.execute(
        """INSERT INTO panchang_cache
           (date, latitude, longitude, tithi, nakshatra, yoga, karana,
            rahu_kaal, choghadiya, sunrise, sunset, moonrise, moonset)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
           ON CONFLICT (date, latitude, longitude) DO NOTHING""",
        (
            target_date, latitude, longitude,
            tithi_str, nak_str, yoga_str, karana_str,
            rahu_str, extended_str,
            panchang["sunrise"], panchang["sunset"],
            panchang.get("moonrise", "--:--"),
            panchang.get("moonset", "--:--"),
        ),
    )
    db.commit()

    # Build full response
    return {
        "date": target_date,
        "latitude": latitude,
        "longitude": longitude,
        **panchang,
        "festivals": festivals,
    }


# ============================================================
# GET /api/panchang/month -- Monthly panchang overview
# ============================================================

@router.get("/api/panchang/month", status_code=status.HTTP_200_OK)
def get_monthly_panchang(
    month: int = Query(default=None),
    year: int = Query(default=None),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
    db: Any = Depends(get_db),
):
    """Get panchang summary for each day of a month."""
    today = date.today()
    target_year = year or today.year
    target_month = month or today.month

    if not (1 <= target_month <= 12):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid month: {target_month}. Must be 1-12.",
        )

    days_in_month = calendar.monthrange(target_year, target_month)[1]
    start_date = date(target_year, target_month, 1).isoformat()
    end_date = date(target_year, target_month, days_in_month).isoformat()

    # Batch-query all cached days for this month in ONE query
    cached_rows = db.execute(
        "SELECT date, tithi, nakshatra, yoga, sunrise, sunset FROM panchang_cache WHERE date >= %s AND date <= %s AND latitude = %s AND longitude = %s",
        (start_date, end_date, latitude, longitude),
    ).fetchall()
    cached_dates = {row["date"]: row for row in cached_rows}

    days = []

    for day in range(1, days_in_month + 1):
        d = date(target_year, target_month, day)
        d_str = d.isoformat()

        cached = cached_dates.get(d_str)

        if cached:
            tithi = json.loads(cached["tithi"]) if isinstance(cached["tithi"], str) else cached["tithi"]
            nak = json.loads(cached["nakshatra"]) if isinstance(cached["nakshatra"], str) else cached["nakshatra"]
            yoga = json.loads(cached["yoga"]) if isinstance(cached["yoga"], str) else cached["yoga"]
            days.append({
                "date": d_str,
                "weekday": d.strftime("%A"),
                "tithi": tithi.get("name", "") if isinstance(tithi, dict) else str(tithi),
                "paksha": tithi.get("paksha", "") if isinstance(tithi, dict) else "",
                "nakshatra": nak.get("name", "") if isinstance(nak, dict) else str(nak),
                "yoga": yoga.get("name", "") if isinstance(yoga, dict) else str(yoga),
                "sunrise": cached["sunrise"],
                "sunset": cached["sunset"],
                "festivals": [],
            })
            continue

        panchang = calculate_panchang(d_str, latitude, longitude)
        festivals = detect_festivals(
            tithi_name=panchang["tithi"]["name"],
            paksha=panchang["tithi"]["paksha"],
            nakshatra_name=panchang["nakshatra"]["name"],
            maas=panchang.get("hindu_calendar", {}).get("maas", ""),
        )
        days.append({
            "date": d_str,
            "weekday": d.strftime("%A"),
            "tithi": panchang["tithi"]["name"],
            "paksha": panchang["tithi"]["paksha"],
            "nakshatra": panchang["nakshatra"]["name"],
            "yoga": panchang["yoga"]["name"],
            "sunrise": panchang["sunrise"],
            "sunset": panchang["sunset"],
            "festivals": [f["name"] for f in festivals],
        })

    return {
        "month": target_month,
        "year": target_year,
        "latitude": latitude,
        "longitude": longitude,
        "days": days,
    }


# ============================================================
# GET /api/panchang/choghadiya
# ============================================================

@router.get("/api/panchang/choghadiya", status_code=status.HTTP_200_OK)
def get_choghadiya(
    date_str: str = Query(default=None, alias="date"),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
):
    """Calculate Choghadiya (auspicious time periods) for the day."""
    target_date = date_str or _today()
    dt = _parse_date(target_date)
    weekday = dt.weekday()

    panchang = calculate_panchang(target_date, latitude, longitude)
    periods = calculate_choghadiya(weekday, panchang["sunrise"], panchang["sunset"])

    return {
        "date": target_date,
        "sunrise": panchang["sunrise"],
        "sunset": panchang["sunset"],
        "periods": periods,
    }


# ============================================================
# GET /api/panchang/muhurat -- Monthly muhurat
# ============================================================

@router.get("/api/panchang/muhurat", status_code=status.HTTP_200_OK)
def get_muhurat(
    muhurat_type: str = Query(default="marriage"),
    year: int = Query(default=None),
    month: int = Query(default=None),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
    db: Any = Depends(get_db),
):
    """Get auspicious muhurat dates for a given type and period."""
    today = date.today()
    target_year = year or today.year
    target_month = month or today.month

    # Check cache
    cached = db.execute(
        "SELECT results FROM muhurat_cache WHERE muhurat_type = %s AND year = %s AND month = %s AND latitude = %s AND longitude = %s",
        (muhurat_type, target_year, target_month, latitude, longitude),
    ).fetchone()

    if cached:
        raw_results = json.loads(cached["results"])
        dates = [
            {
                "date": r.get("date", ""),
                "time_range": f"Sunrise to Sunset ({r.get('tithi', 'Shukla')} {r.get('nakshatra', '')})",
                "quality": r.get("quality", "auspicious"),
            }
            for r in raw_results
        ]
        return {"dates": dates}

    days_in_month = calendar.monthrange(target_year, target_month)[1]
    auspicious_dates = []

    for day in range(1, days_in_month + 1):
        d = date(target_year, target_month, day)
        d_str = d.isoformat()
        panchang = calculate_panchang(d_str, latitude, longitude)
        tithi = panchang["tithi"]

        if tithi["paksha"] == "Shukla" and tithi["name"] not in ("Ashtami", "Navami", "Chaturdashi"):
            auspicious_dates.append({
                "date": d_str,
                "tithi": tithi["name"],
                "nakshatra": panchang["nakshatra"]["name"],
                "quality": "auspicious",
            })

    results_json = json.dumps(auspicious_dates)
    db.execute(
        """INSERT INTO muhurat_cache
           (muhurat_type, year, month, latitude, longitude, results)
           VALUES (%s, %s, %s, %s, %s, %s)
           ON CONFLICT (muhurat_type, year, month, latitude, longitude) DO NOTHING""",
        (muhurat_type, target_year, target_month, latitude, longitude, results_json),
    )
    db.commit()

    dates = [
        {
            "date": r["date"],
            "time_range": f"Sunrise to Sunset ({r['tithi']} {r['nakshatra']})",
            "quality": r["quality"],
        }
        for r in auspicious_dates
    ]
    return {"dates": dates}


# ============================================================
# Sunrise & Festivals
# ============================================================

@router.get("/api/panchang/sunrise", status_code=status.HTTP_200_OK)
def get_sunrise(
    date_str: str = Query(default=None, alias="date"),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
):
    """Get sunrise, sunset, moonrise, moonset for a given date and location."""
    target_date = date_str or _today()
    _parse_date(target_date)

    panchang = calculate_panchang(target_date, latitude, longitude)

    return {
        "sunrise": panchang["sunrise"],
        "sunset": panchang["sunset"],
        "moonrise": panchang.get("moonrise", "--:--"),
        "moonset": panchang.get("moonset", "--:--"),
    }


@router.get("/api/festivals", status_code=status.HTTP_200_OK)
def list_festivals(
    year: int = Query(default=None),
    category: str = Query(default=None),
    db: Any = Depends(get_db),
):
    """List festivals for a given year, optionally filtered by category."""
    target_year = year or date.today().year

    if category:
        rows = db.execute(
            "SELECT * FROM festivals WHERE year = %s AND category = %s ORDER BY date",
            (target_year, category),
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT * FROM festivals WHERE year = %s ORDER BY date",
            (target_year,),
        ).fetchall()

    return [
        {
            "name": r["name"],
            "date": r["date"],
            "description": r["description"],
            "rituals": r["rituals"],
        }
        for r in rows
    ]


# ============================================================
# GET /api/panchang/pdf -- Download Panchang as PDF
# ============================================================

def _find_hindi_font():
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


def _build_panchang_pdf(panchang: dict, date_str: str) -> bytes:
    """Build a bilingual Hindi+English Panchang PDF and return raw bytes."""
    from fpdf import FPDF

    # -- Colours ------------------------------------------------
    SAFFRON = (255, 153, 51)       # #FF9933
    SAFFRON_LIGHT = (255, 230, 204)
    CREAM = (250, 247, 242)        # #FAF7F2
    DARK_TEXT = (51, 51, 51)
    WHITE = (255, 255, 255)
    ALT_ROW = (255, 245, 235)

    # -- Font setup ---------------------------------------------
    hindi_font_path = _find_hindi_font()
    has_hindi = hindi_font_path is not None

    generated_ts = datetime.now().strftime("%d %b %Y, %I:%M %p")
    footer_text = f"Generated by AstroRattan.com | {generated_ts}"

    # -- Parse date for display ---------------------------------
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    day_name_en = dt.strftime("%A")
    day_name_hi = HINDI_DAYS.get(day_name_en, day_name_en)
    month_hi = HINDI_MONTHS_ENG.get(dt.month, "")
    date_hi = f"{dt.day} {month_hi} {dt.year}"
    date_en = dt.strftime("%d %B %Y")

    # -- Extract panchang fields --------------------------------
    tithi = panchang.get("tithi", {})
    nakshatra = panchang.get("nakshatra", {})
    yoga = panchang.get("yoga", {})
    karana = panchang.get("karana", {})
    hindu_cal = panchang.get("hindu_calendar", {})
    rahu_kaal = panchang.get("rahu_kaal", {})
    gulika_kaal = panchang.get("gulika_kaal", {})
    yamaganda = panchang.get("yamaganda", {})
    brahma_muhurat = panchang.get("brahma_muhurat", {})
    abhijit = panchang.get("abhijit_muhurat", {})
    nishita = panchang.get("nishita_muhurta", panchang.get("nishita_muhurat", {}))
    choghadiya = panchang.get("choghadiya", [])
    planets = panchang.get("planetary_positions", [])
    festivals = panchang.get("festivals", [])

    # -- Helper: safe Hindi lookup ------------------------------
    def _hi(mapping, key):
        return mapping.get(key, key) if has_hindi else key

    # ============================================================
    # PDF class
    # ============================================================
    class PanchangPDF(FPDF):
        def __init__(self):
            super().__init__()
            self._hindi_ok = False
            if has_hindi:
                self.add_font("Hindi", "", hindi_font_path, uni=True)
                self._hindi_ok = True

        def header(self):
            # Saffron header bar
            self.set_fill_color(*SAFFRON)
            self.rect(0, 0, 210, 28, "F")

            if self._hindi_ok:
                self.set_font("Hindi", "", 18)
            else:
                self.set_font("Helvetica", "B", 18)
            self.set_text_color(*WHITE)
            self.set_y(4)
            title = "\u0935\u0948\u0926\u093f\u0915 \u092a\u0902\u091a\u093e\u0902\u0917  /  Hindu Panchang" if self._hindi_ok else "Hindu Panchang"
            self.cell(0, 10, title, align="C", new_x="LMARGIN", new_y="NEXT")
            self.set_font("Helvetica", "", 9)
            self.set_text_color(255, 240, 220)
            self.cell(0, 6, f"{date_en}  |  {day_name_en}", align="C", new_x="LMARGIN", new_y="NEXT")
            self.set_y(30)
            self.set_text_color(*DARK_TEXT)

        def footer(self):
            self.set_y(-12)
            self.set_font("Helvetica", "I", 7)
            self.set_text_color(150, 150, 150)
            self.cell(0, 8, f"Page {self.page_no()}  |  {footer_text}", align="C")
            self.set_text_color(*DARK_TEXT)

        def section_title(self, title_hi: str, title_en: str):
            """Draw a saffron section header with Hindi + English."""
            self.ln(3)
            self.set_fill_color(*SAFFRON)
            self.set_text_color(*WHITE)
            if self._hindi_ok:
                self.set_font("Hindi", "", 11)
                label = f"  {title_hi}  /  {title_en}"
            else:
                self.set_font("Helvetica", "B", 11)
                label = f"  {title_en}"
            self.cell(0, 7, label, fill=True, new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(*DARK_TEXT)
            self.ln(2)

        def _thin_line(self):
            """Draw a thin saffron separator."""
            y = self.get_y()
            self.set_draw_color(*SAFFRON)
            self.set_line_width(0.3)
            self.line(10, y, 200, y)
            self.ln(2)

        def bilingual_row(self, label_hi: str, label_en: str, value_hi: str, value_en: str, fill: bool = False):
            """Print a bilingual label-value row."""
            if fill:
                self.set_fill_color(*ALT_ROW)
            lw = 72  # label column width
            vw = 118  # value column width

            if self._hindi_ok:
                self.set_font("Hindi", "", 9)
                label_text = f"{label_hi} / {label_en}"
                value_text = f"{value_hi} / {value_en}" if value_hi != value_en else value_en
            else:
                self.set_font("Helvetica", "B", 9)
                label_text = label_en
                self.set_font("Helvetica", "", 9)
                value_text = value_en

            if self._hindi_ok:
                self.set_font("Hindi", "", 9)
            else:
                self.set_font("Helvetica", "B", 9)
            self.cell(lw, 6, label_text, border=0, fill=fill)
            if self._hindi_ok:
                self.set_font("Hindi", "", 9)
            else:
                self.set_font("Helvetica", "", 9)
            self.cell(vw, 6, value_text, border=0, fill=fill, new_x="LMARGIN", new_y="NEXT")

        def table_header(self, cols: list, widths: list):
            self.set_fill_color(*SAFFRON_LIGHT)
            if self._hindi_ok:
                self.set_font("Hindi", "", 8)
            else:
                self.set_font("Helvetica", "B", 8)
            for i, h in enumerate(cols):
                self.cell(widths[i], 6, h, border=1, align="C", fill=True)
            self.ln()

        def table_row(self, vals: list, widths: list, row_idx: int = 0):
            if self._hindi_ok:
                self.set_font("Hindi", "", 8)
            else:
                self.set_font("Helvetica", "", 8)
            if row_idx % 2 == 1:
                self.set_fill_color(*ALT_ROW)
                fill = True
            else:
                fill = False
            for i, v in enumerate(vals):
                self.cell(widths[i], 5.5, str(v), border=1, align="C", fill=fill)
            self.ln()

    # ============================================================
    # Build the PDF
    # ============================================================
    pdf = PanchangPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # ---- PAGE 1: Main Panchang --------------------------------
    pdf.add_page()

    # --- Date & Day Section ---
    pdf.section_title("\u0926\u093f\u0928\u093e\u0902\u0915 \u0935 \u0935\u093e\u0930", "Date & Day")
    pdf.bilingual_row(
        "\u0926\u093f\u0928\u093e\u0902\u0915", "Date",
        date_hi, date_en, fill=True,
    )
    pdf.bilingual_row(
        "\u0926\u093f\u0928", "Day",
        day_name_hi, day_name_en,
    )

    # --- Hindu Calendar Section ---
    maas_en = hindu_cal.get("maas", "")
    paksha_en = hindu_cal.get("paksha", tithi.get("paksha", ""))
    ritu_en = hindu_cal.get("ritu", "")
    ayana_en = hindu_cal.get("ayana", "")
    vikram = hindu_cal.get("vikram_samvat", "")
    shaka = hindu_cal.get("shaka_samvat", "")

    pdf.section_title("\u0939\u093f\u0928\u094d\u0926\u0942 \u092a\u0902\u091a\u093e\u0902\u0917", "Hindu Calendar")
    pdf.bilingual_row(
        "\u0935\u093f\u0915\u094d\u0930\u092e \u0938\u0902\u0935\u0924\u094d", "Vikram Samvat",
        str(vikram), str(vikram), fill=True,
    )
    pdf.bilingual_row(
        "\u0936\u0915 \u0938\u0902\u0935\u0924\u094d", "Shaka Samvat",
        str(shaka), str(shaka),
    )
    pdf.bilingual_row(
        "\u0905\u092f\u0928", "Ayana",
        _hi(HINDI_AYANA, ayana_en), ayana_en, fill=True,
    )
    pdf.bilingual_row(
        "\u090b\u0924\u0941", "Ritu",
        _hi(HINDI_RITU, ritu_en), f"{ritu_en} ({hindu_cal.get('ritu_english', '')})",
    )
    pdf.bilingual_row(
        "\u092e\u093e\u0938", "Month",
        _hi(HINDI_MAAS, maas_en), maas_en, fill=True,
    )
    pdf.bilingual_row(
        "\u092a\u0915\u094d\u0937", "Paksha",
        _hi(HINDI_PAKSHA, paksha_en), paksha_en,
    )

    # --- Tithi / Nakshatra / Yoga / Karana ---
    pdf.section_title("\u092a\u0902\u091a\u093e\u0902\u0917 \u0935\u093f\u0935\u0930\u0923", "Panchang Details")

    # Tithi
    tithi_name = tithi.get("name", "")
    tithi_end = tithi.get("end_time", "")
    tithi_next = tithi.get("next", "")
    tithi_val_en = f"{tithi_name} until {tithi_end}"
    if tithi_next:
        tithi_val_en += f", then {tithi_next}"
    tithi_val_hi = f"{_hi(HINDI_TITHIS, tithi_name)} {tithi_end} \u0924\u0915"
    if tithi_next:
        tithi_val_hi += f", \u092b\u093f\u0930 {_hi(HINDI_TITHIS, tithi_next)}"
    pdf.bilingual_row(
        "\u0924\u093f\u0925\u093f", "Tithi",
        tithi_val_hi, tithi_val_en, fill=True,
    )

    # Nakshatra
    nak_name = nakshatra.get("name", "")
    nak_pada = nakshatra.get("pada", "")
    nak_end = nakshatra.get("end_time", "")
    nak_next = nakshatra.get("next", "")
    nak_val_en = f"{nak_name} (Pada {nak_pada}) until {nak_end}"
    if nak_next:
        nak_val_en += f", then {nak_next}"
    nak_val_hi = f"{_hi(HINDI_NAKSHATRAS, nak_name)} (\u092a\u0926 {nak_pada}) {nak_end} \u0924\u0915"
    if nak_next:
        nak_val_hi += f", \u092b\u093f\u0930 {_hi(HINDI_NAKSHATRAS, nak_next)}"
    pdf.bilingual_row(
        "\u0928\u0915\u094d\u0937\u0924\u094d\u0930", "Nakshatra",
        nak_val_hi, nak_val_en,
    )

    # Yoga
    yoga_name = yoga.get("name", "")
    yoga_end = yoga.get("end_time", "")
    yoga_next = yoga.get("next", "")
    yoga_val_en = f"{yoga_name} until {yoga_end}"
    if yoga_next:
        yoga_val_en += f", then {yoga_next}"
    yoga_val_hi = f"{_hi(HINDI_YOGAS, yoga_name)} {yoga_end} \u0924\u0915"
    if yoga_next:
        yoga_val_hi += f", \u092b\u093f\u0930 {_hi(HINDI_YOGAS, yoga_next)}"
    pdf.bilingual_row(
        "\u092f\u094b\u0917", "Yoga",
        yoga_val_hi, yoga_val_en, fill=True,
    )

    # Karana
    karana_name = karana.get("name", "")
    karana_end = karana.get("end_time", "")
    karana_second = karana.get("second_karana", "")
    karana_val_en = f"{karana_name} until {karana_end}"
    if karana_second:
        karana_val_en += f", then {karana_second}"
    karana_val_hi = f"{karana_name} {karana_end} \u0924\u0915"
    if karana_second:
        karana_val_hi += f", \u092b\u093f\u0930 {karana_second}"
    pdf.bilingual_row(
        "\u0915\u0930\u0923", "Karana",
        karana_val_hi, karana_val_en,
    )

    # --- Timings Section ---
    pdf.section_title("\u0938\u092e\u092f", "Timings")
    pdf.bilingual_row(
        "\u0938\u0942\u0930\u094d\u092f\u094b\u0926\u092f", "Sunrise",
        panchang.get("sunrise", "--:--"), panchang.get("sunrise", "--:--"), fill=True,
    )
    pdf.bilingual_row(
        "\u0938\u0942\u0930\u094d\u092f\u093e\u0938\u094d\u0924", "Sunset",
        panchang.get("sunset", "--:--"), panchang.get("sunset", "--:--"),
    )
    pdf.bilingual_row(
        "\u091a\u0928\u094d\u0926\u094d\u0930\u094b\u0926\u092f", "Moonrise",
        panchang.get("moonrise", "--:--"), panchang.get("moonrise", "--:--"), fill=True,
    )
    pdf.bilingual_row(
        "\u091a\u0928\u094d\u0926\u094d\u0930\u093e\u0938\u094d\u0924", "Moonset",
        panchang.get("moonset", "--:--"), panchang.get("moonset", "--:--"),
    )
    pdf.bilingual_row(
        "\u0926\u093f\u0928\u092e\u093e\u0928", "Day Duration",
        panchang.get("dinamana", "--"), panchang.get("dinamana", "--"), fill=True,
    )
    pdf.bilingual_row(
        "\u0930\u093e\u0924\u094d\u0930\u093f\u092e\u093e\u0928", "Night Duration",
        panchang.get("ratrimana", "--"), panchang.get("ratrimana", "--"),
    )

    # --- Muhurat Section ---
    pdf.section_title("\u092e\u0941\u0939\u0942\u0930\u094d\u0924", "Muhurat & Inauspicious Periods")

    def _muhurat_str(m):
        if isinstance(m, dict):
            return f"{m.get('start', '--:--')} - {m.get('end', '--:--')}"
        return str(m) if m else "--"

    pdf.bilingual_row(
        "\u0930\u093e\u0939\u0941\u0915\u093e\u0932", "Rahu Kaal",
        _muhurat_str(rahu_kaal), _muhurat_str(rahu_kaal), fill=True,
    )
    pdf.bilingual_row(
        "\u0917\u0941\u0932\u093f\u0915 \u0915\u093e\u0932", "Gulika Kaal",
        _muhurat_str(gulika_kaal), _muhurat_str(gulika_kaal),
    )
    pdf.bilingual_row(
        "\u092f\u092e\u0917\u0923\u094d\u0921", "Yamaganda",
        _muhurat_str(yamaganda), _muhurat_str(yamaganda), fill=True,
    )
    pdf.bilingual_row(
        "\u092c\u094d\u0930\u0939\u094d\u092e\u092e\u0941\u0939\u0942\u0930\u094d\u0924", "Brahma Muhurat",
        _muhurat_str(brahma_muhurat), _muhurat_str(brahma_muhurat),
    )
    pdf.bilingual_row(
        "\u0905\u092d\u093f\u091c\u0940\u0924 \u092e\u0941\u0939\u0942\u0930\u094d\u0924", "Abhijit Muhurat",
        _muhurat_str(abhijit), _muhurat_str(abhijit), fill=True,
    )
    pdf.bilingual_row(
        "\u0928\u093f\u0936\u093f\u0924\u093e \u092e\u0941\u0939\u0942\u0930\u094d\u0924", "Nishita Muhurat",
        _muhurat_str(nishita), _muhurat_str(nishita),
    )

    # --- Sun / Moon Sign ---
    pdf.section_title("\u0917\u094d\u0930\u0939 \u0938\u094d\u0925\u093f\u0924\u093f", "Sun & Moon Position")
    sun_sign = panchang.get("sun_sign", "")
    moon_sign = panchang.get("moon_sign", "")
    pdf.bilingual_row(
        "\u0938\u0942\u0930\u094d\u092f \u0930\u093e\u0936\u093f", "Sun Sign",
        _hi(HINDI_RASHIS, sun_sign), sun_sign, fill=True,
    )
    pdf.bilingual_row(
        "\u091a\u0928\u094d\u0926\u094d\u0930 \u0930\u093e\u0936\u093f", "Moon Sign",
        _hi(HINDI_RASHIS, moon_sign), moon_sign,
    )

    # --- Festivals ---
    if festivals:
        pdf.section_title("\u0935\u094d\u0930\u0924/\u092a\u0930\u094d\u0935", "Festivals & Observances")
        if pdf._hindi_ok:
            pdf.set_font("Hindi", "", 9)
        else:
            pdf.set_font("Helvetica", "", 9)
        for f in festivals:
            fname = f.get("name", f) if isinstance(f, dict) else str(f)
            fname_hi = f.get("hindi_name", fname) if isinstance(f, dict) else fname
            if pdf._hindi_ok and fname_hi != fname:
                pdf.cell(0, 6, f"  - {fname_hi} / {fname}", new_x="LMARGIN", new_y="NEXT")
            else:
                pdf.cell(0, 6, f"  - {fname}", new_x="LMARGIN", new_y="NEXT")

    # ---- PAGE 2: Choghadiya + Planetary Positions -------------
    pdf.add_page()

    # --- Choghadiya Table ---
    if choghadiya:
        pdf.section_title("\u091a\u094c\u0918\u0921\u093f\u092f\u093e", "Choghadiya (Day Periods)")
        if pdf._hindi_ok:
            chog_headers = ["\u0915\u094d\u0930\u092e / #", "\u0928\u093e\u092e / Name", "\u0917\u0941\u0923\u0935\u0924\u094d\u0924\u093e / Quality", "\u0936\u0941\u0930\u0942 / Start", "\u0938\u092e\u093e\u092a\u094d\u0924 / End"]
        else:
            chog_headers = ["#", "Name", "Quality", "Start", "End"]
        chog_widths = [18, 42, 50, 40, 40]
        pdf.table_header(chog_headers, chog_widths)

        for idx, period in enumerate(choghadiya):
            name = period.get("name", "")
            quality = period.get("quality", "")
            start = period.get("start", "")
            end = period.get("end", "")
            if pdf._hindi_ok:
                name_display = f"{HINDI_CHOGHADIYA_QUALITY.get(name, name)} / {name}"
            else:
                name_display = name
            pdf.table_row([str(idx + 1), name_display, quality, start, end], chog_widths, idx)
        pdf.ln(4)

    # --- Planetary Positions Table ---
    if planets:
        pdf.section_title("\u0917\u094d\u0930\u0939 \u0938\u094d\u0925\u093f\u0924\u093f", "Planetary Positions (Navagraha)")
        if pdf._hindi_ok:
            planet_headers = [
                "\u0917\u094d\u0930\u0939 / Planet",
                "\u0905\u0902\u0936 / Degree",
                "\u0930\u093e\u0936\u093f / Rashi",
            ]
        else:
            planet_headers = ["Planet", "Degree", "Rashi"]
        planet_widths = [60, 50, 80]
        pdf.table_header(planet_headers, planet_widths)

        for idx, planet in enumerate(planets):
            name_en = planet.get("name", "")
            degree = planet.get("degree", 0)
            rashi_en = planet.get("rashi", "")
            if pdf._hindi_ok:
                name_display = f"{HINDI_PLANETS.get(name_en, name_en)} / {name_en}"
                rashi_display = f"{_hi(HINDI_RASHIS, rashi_en)} / {rashi_en}"
            else:
                name_display = name_en
                rashi_display = rashi_en
            pdf.table_row(
                [name_display, f"{degree:.2f}", rashi_display],
                planet_widths, idx,
            )

    return pdf.output()


@router.get("/api/panchang/pdf", status_code=status.HTTP_200_OK)
async def download_panchang_pdf(
    date_str: str = Query(..., alias="date"),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
):
    """Generate and download a bilingual Hindi+English Panchang PDF report."""
    target_date = date_str
    _parse_date(target_date)

    # Calculate full panchang
    panchang = calculate_panchang(target_date, latitude, longitude)

    # Detect festivals
    festivals = detect_festivals(
        tithi_name=panchang["tithi"]["name"],
        paksha=panchang["tithi"]["paksha"],
        nakshatra_name=panchang["nakshatra"]["name"],
        maas=panchang.get("hindu_calendar", {}).get("maas", ""),
    )
    panchang["festivals"] = festivals

    # Build PDF
    pdf_bytes = _build_panchang_pdf(panchang, target_date)

    filename = f"Panchang_{target_date}.pdf"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
