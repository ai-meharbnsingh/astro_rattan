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
from app.auth import get_current_user, require_role
from app.panchang_engine import (
    calculate_panchang,
    calculate_choghadiya,
)
from app.festival_engine import detect_festivals
from app.sankranti_engine import build_sankranti_payload


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
HINDI_RASHI = {
    'Mesha': 'मेष', 'Vrishabha': 'वृषभ', 'Mithuna': 'मिथुन',
    'Karka': 'कर्क', 'Simha': 'सिंह', 'Kanya': 'कन्या',
    'Tula': 'तुला', 'Vrishchika': 'वृश्चिक', 'Dhanu': 'धनु',
    'Makara': 'मकर', 'Kumbha': 'कुम्भ', 'Meena': 'मीन',
}
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
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        if dt.year < 1900 or dt.year > 2100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Year out of range: {dt.year}. Must be 1900-2100.",
            )
        return dt
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format: '{date_str}'. Expected YYYY-MM-DD.",
        )


def _validate_coords(latitude: float, longitude: float) -> None:
    """Validate latitude and longitude ranges."""
    if not (-90.0 <= latitude <= 90.0):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid latitude: {latitude}. Must be -90 to 90.",
        )
    if not (-180.0 <= longitude <= 180.0):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid longitude: {longitude}. Must be -180 to 180.",
        )


# ============================================================
# GET /api/panchang -- Full daily panchang (enhanced)
# ============================================================

@router.get("/api/panchang", status_code=status.HTTP_200_OK)
def get_panchang(
    date_str: str = Query(default=None, alias="date"),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
    lang: str = Query(default="en"),
    db: Any = Depends(get_db),
):
    """Calculate complete Panchang for a given date and location."""
    _validate_coords(latitude, longitude)
    target_date = date_str or _today()
    _parse_date(target_date)

    # Check cache first (with TTL - 7 days)
    cached = db.execute(
        """SELECT * FROM panchang_cache 
           WHERE date = %s AND latitude = %s AND longitude = %s 
           AND created_at > NOW() - INTERVAL '7 days'""",
        (target_date, latitude, longitude),
    ).fetchone()

    # Serve from cache only if it has extended data (new engine format)
    raw_ext_check = cached.get("choghadiya", "") if cached else ""
    cache_has_extended = cached and raw_ext_check and raw_ext_check not in ("", "[]", "{}")
    # Also verify cache has the newer misc data; otherwise treat as stale
    if cache_has_extended:
        try:
            ext_parsed = json.loads(raw_ext_check) if isinstance(raw_ext_check, str) else raw_ext_check
            cache_has_extended = isinstance(ext_parsed, dict) and "misc" in ext_parsed
        except (json.JSONDecodeError, TypeError):
            cache_has_extended = False

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
        
        # Inject Hindi names if missing in cache (for backward compatibility or new lang support)
        _inject_hindi_fields(result)
        return result

    # Calculate fresh
    panchang = calculate_panchang(target_date, latitude, longitude)

    # Detect festivals
    festivals = detect_festivals(
        tithi_name=panchang["tithi"]["name"],
        paksha=panchang["tithi"]["paksha"],
        nakshatra_name=panchang["nakshatra"]["name"],
        maas=panchang.get("hindu_calendar", {}).get("maas", ""),
        gregorian_date=target_date,
    )
    panchang["festivals"] = festivals

    # Inject Hindi names before caching
    _inject_hindi_fields(panchang)

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
           ON CONFLICT (date, latitude, longitude) DO UPDATE SET
               tithi = EXCLUDED.tithi, nakshatra = EXCLUDED.nakshatra,
               yoga = EXCLUDED.yoga, karana = EXCLUDED.karana,
               rahu_kaal = EXCLUDED.rahu_kaal, choghadiya = EXCLUDED.choghadiya,
               sunrise = EXCLUDED.sunrise, sunset = EXCLUDED.sunset,
               moonrise = EXCLUDED.moonrise, moonset = EXCLUDED.moonset,
               created_at = NOW()""",
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

def _inject_hindi_fields(panchang: dict):
    """Deep-inject Hindi names into panchang dict based on English keys."""
    if "tithi" in panchang:
        t = panchang["tithi"]
        t["name_hindi"] = HINDI_TITHIS.get(t.get("name"), t.get("name"))
        t["paksha_hindi"] = HINDI_PAKSHA.get(t.get("paksha"), t.get("paksha"))
        if "next" in t:
            t["next_hindi"] = HINDI_TITHIS.get(t["next"], t["next"])
            
    if "nakshatra" in panchang:
        n = panchang["nakshatra"]
        if "name_hindi" not in n:
            # Look for it elsewhere if possible, but we don't have a direct dict here
            # Engine usually provides it, so we just ensure it's there
            pass
            
    if "yoga" in panchang:
        y = panchang["yoga"]
        y["name_hindi"] = HINDI_YOGAS.get(y.get("name"), y.get("name"))
        if "next" in y:
            y["next_hindi"] = HINDI_YOGAS.get(y["next"], y["next"])
            
    if "karana" in panchang:
        k = panchang["karana"]
        k["name_hindi"] = HINDI_TITHIS.get(k.get("name"), k.get("name")) # Karana names often reuse tithi-like names or need separate dict
        # Actually Karanas have their own names: Bava, Balava...
        # Let's add HINDI_KARANAS if needed.
        if "second_karana" in k:
             k["second_karana_hindi"] = k.get("second_karana")

    if "vaar" in panchang:
        v = panchang["vaar"]
        # HINDI_PLANETS can map Sun -> Surya etc.
        v["name_hindi"] = v.get("name") 

    if "hindu_calendar" in panchang:
        hc = panchang["hindu_calendar"]
        hc["maas_hindi"] = HINDI_MAAS.get(hc.get("maas"), hc.get("maas"))
        hc["paksha_hindi"] = HINDI_PAKSHA.get(hc.get("paksha"), hc.get("paksha"))
        hc["ritu_hindi"] = HINDI_RITU.get(hc.get("ritu"), hc.get("ritu"))
        hc["ayana_hindi"] = HINDI_AYANA.get(hc.get("ayana"), hc.get("ayana"))

    if "sun_sign" in panchang:
        panchang["sun_sign_hindi"] = HINDI_RASHIS.get(panchang["sun_sign"], panchang["sun_sign"])
    if "moon_sign" in panchang:
        panchang["moon_sign_hindi"] = HINDI_RASHIS.get(panchang["moon_sign"], panchang["moon_sign"])
         
    # Choghadiya
    for group in ["choghadiya", "night_choghadiya"]:
        if group in panchang and isinstance(panchang[group], list):
            for c in panchang[group]:
                c["name_hindi"] = HINDI_CHOGHADIYA_QUALITY.get(c.get("name"), c.get("name"))
                c["quality_hindi"] = HINDI_CHOGHADIYA_QUALITY.get(c.get("quality"), c.get("quality"))
                
    # Hora
    if "hora_table" in panchang and isinstance(panchang["hora_table"], list):
        for h in panchang["hora_table"]:
            h["lord_hindi"] = HINDI_PLANETS.get(h.get("lord"), h.get("lord"))
            
    # Gowri
    if "gowri_panchang" in panchang and isinstance(panchang["gowri_panchang"], list):
        for g in panchang["gowri_panchang"]:
             g["name_hindi"] = g.get("name") # Logic for Gowri names needed if they differ


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
    _validate_coords(latitude, longitude)
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

    # Batch-query all cached days for this month in ONE query (with TTL - 7 days)
    cached_rows = db.execute(
        """SELECT date, tithi, nakshatra, yoga, sunrise, sunset, moonrise, moonset
           FROM panchang_cache
           WHERE date >= %s AND date <= %s AND latitude = %s AND longitude = %s
           AND created_at > NOW() - INTERVAL '7 days'""",
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
            t_name = tithi.get("name", "") if isinstance(tithi, dict) else str(tithi)
            t_paksha = tithi.get("paksha", "") if isinstance(tithi, dict) else ""
            t_number = tithi.get("number", 0) if isinstance(tithi, dict) else 0
            n_name = nak.get("name", "") if isinstance(nak, dict) else str(nak)
            # Run festival detection even for cached data
            cached_festivals = detect_festivals(
                tithi_name=t_name,
                paksha=t_paksha,
                nakshatra_name=n_name,
                maas="",  # maas not stored in cache; tithi+solar still match
                gregorian_date=d_str,
            )
            # Derive moon_sign from extended cache data if available
            _ext_raw = cached.get("choghadiya", "")
            _ext = {}
            if _ext_raw and _ext_raw not in ("", "[]", "{}"):
                try:
                    _ext = json.loads(_ext_raw) if isinstance(_ext_raw, str) else _ext_raw
                except (json.JSONDecodeError, TypeError):
                    _ext = {}
            _moon_sign = _ext.get("moon_sign", "") if isinstance(_ext, dict) else ""
            days.append({
                "date": d_str,
                "weekday": d.strftime("%A"),
                "tithi": t_name,
                "tithi_number": t_number,
                "tithi_hindi": HINDI_TITHIS.get(t_name, ""),
                "paksha": t_paksha,
                "paksha_hindi": HINDI_PAKSHA.get(t_paksha, ""),
                "nakshatra": n_name,
                "nakshatra_hindi": HINDI_NAKSHATRAS.get(n_name, ""),
                "yoga": yoga.get("name", "") if isinstance(yoga, dict) else str(yoga),
                "sunrise": cached["sunrise"],
                "sunset": cached["sunset"],
                "moonrise": cached.get("moonrise", "--:--"),
                "moonset": cached.get("moonset", "--:--"),
                "moon_sign": _moon_sign,
                "moon_sign_hindi": HINDI_RASHI.get(_moon_sign, ""),
                "festivals": [f["name"] for f in cached_festivals],
            })
            continue

        panchang = calculate_panchang(d_str, latitude, longitude)
        festivals = detect_festivals(
            tithi_name=panchang["tithi"]["name"],
            paksha=panchang["tithi"]["paksha"],
            nakshatra_name=panchang["nakshatra"]["name"],
            maas=panchang.get("hindu_calendar", {}).get("maas", ""),
            gregorian_date=d_str,
        )
        # Cache the freshly calculated day for future requests
        db.execute(
            """INSERT INTO panchang_cache
               (date, latitude, longitude, tithi, nakshatra, yoga, karana,
                rahu_kaal, choghadiya, sunrise, sunset, moonrise, moonset)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (date, latitude, longitude) DO NOTHING""",
            (
                d_str, latitude, longitude,
                json.dumps(panchang["tithi"]), json.dumps(panchang["nakshatra"]),
                json.dumps(panchang["yoga"]), json.dumps(panchang.get("karana", {})),
                json.dumps(panchang.get("rahu_kaal", {})), "{}",
                panchang["sunrise"], panchang["sunset"],
                panchang.get("moonrise", "--:--"), panchang.get("moonset", "--:--"),
            ),
        )
        db.commit()
        _t_name = panchang["tithi"]["name"]
        _t_paksha = panchang["tithi"]["paksha"]
        _n_name = panchang["nakshatra"]["name"]
        _m_sign = panchang.get("moon_sign", "")
        days.append({
            "date": d_str,
            "weekday": d.strftime("%A"),
            "tithi": _t_name,
            "tithi_number": panchang["tithi"].get("number", 0),
            "tithi_hindi": HINDI_TITHIS.get(_t_name, ""),
            "paksha": _t_paksha,
            "paksha_hindi": HINDI_PAKSHA.get(_t_paksha, ""),
            "nakshatra": _n_name,
            "nakshatra_hindi": HINDI_NAKSHATRAS.get(_n_name, ""),
            "yoga": panchang["yoga"]["name"],
            "sunrise": panchang["sunrise"],
            "sunset": panchang["sunset"],
            "moonrise": panchang.get("moonrise", "--:--"),
            "moonset": panchang.get("moonset", "--:--"),
            "moon_sign": _m_sign,
            "moon_sign_hindi": HINDI_RASHI.get(_m_sign, ""),
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


@router.get("/api/panchang/sankranti", status_code=status.HTTP_200_OK)
def get_sankranti(
    year: int = Query(default=None, ge=1900, le=2100),
    latitude: float = Query(default=28.6139),
    longitude: float = Query(default=77.2090),
):
    """Return 12 Sankranti (Sun ingress) times + restriction windows for a year."""
    _validate_coords(latitude, longitude)
    target_year = year or date.today().year
    return build_sankranti_payload(target_year, longitude)


@router.get("/api/festivals", status_code=status.HTTP_200_OK)
def list_festivals(
    year: int = Query(default=None),
    month: int = Query(default=None),
    category: str = Query(default=None),
    lang: str = Query(default="en"),
    db: Any = Depends(get_db),
):
    """List festivals for a given year and optionally month, filtered by category."""
    target_year = year or date.today().year

    # Build query with month filter if provided
    if month and category:
        rows = db.execute(
            "SELECT * FROM festivals WHERE year = %s AND MONTH(date) = %s AND category = %s ORDER BY date",
            (target_year, month, category),
        ).fetchall()
    elif month:
        rows = db.execute(
            "SELECT * FROM festivals WHERE year = %s AND MONTH(date) = %s ORDER BY date",
            (target_year, month),
        ).fetchall()
    elif category:
        rows = db.execute(
            "SELECT * FROM festivals WHERE year = %s AND category = %s ORDER BY date",
            (target_year, category),
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT * FROM festivals WHERE year = %s ORDER BY date",
            (target_year,),
        ).fetchall()

    # Format response with bilingual support
    festivals_list = []
    for r in rows:
        festival = {
            "name": r.get("name", ""),
            "name_hindi": r.get("name_hindi", r.get("name", "")),
            "date": r.get("date"),
            "description": r.get("description", ""),
            "description_hindi": r.get("description_hindi", r.get("description", "")),
            "type": r.get("category", "Festival"),
            "type_hindi": r.get("category_hindi", r.get("category", "त्योहार")),
            "rituals": r.get("rituals", ""),
            "rituals_hindi": r.get("rituals_hindi", r.get("rituals", "")),
        }
        festivals_list.append(festival)

    return {"festivals": festivals_list}


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
    """Build a clean single-page Panchang summary PDF (like WhatsApp text style)."""
    from fpdf import FPDF

    SAFFRON = (255, 153, 51)
    DARK = (51, 51, 51)
    WHITE = (255, 255, 255)
    MUTED = (120, 100, 80)

    hindi_font_path = _find_hindi_font()
    has_hindi = hindi_font_path is not None

    dt = datetime.strptime(date_str, "%Y-%m-%d")
    day_en = dt.strftime("%A")
    day_hi = HINDI_DAYS.get(day_en, day_en)
    month_hi = HINDI_MONTHS_ENG.get(dt.month, "")
    date_hi = f"{dt.day} {month_hi} {dt.year}"
    date_en = dt.strftime("%d %B %Y")

    tithi = panchang.get("tithi", {})
    nakshatra = panchang.get("nakshatra", {})
    yoga = panchang.get("yoga", {})
    karana = panchang.get("karana", {})
    hc = panchang.get("hindu_calendar", {})
    rahu = panchang.get("rahu_kaal", {})
    gulika = panchang.get("gulika_kaal", {})
    yamag = panchang.get("yamaganda", {})
    brahma = panchang.get("brahma_muhurat", {})
    abhijit = panchang.get("abhijit_muhurat", {})
    nishita = panchang.get("nishita_muhurta", panchang.get("nishita_muhurat", {}))
    festivals = panchang.get("festivals", [])
    choghadiya = panchang.get("choghadiya", [])
    planets = panchang.get("planetary_positions", [])

    def _hi(m, k):
        return m.get(k, k) if has_hindi else k

    def _period(m):
        if isinstance(m, dict):
            return f"{m.get('start', '')} - {m.get('end', '')}"
        return str(m) if m else "--"

    # Build tithi string
    t_name = tithi.get("name", "")
    t_hi = _hi(HINDI_TITHIS, t_name)
    t_str_hi = f"{t_hi} {tithi.get('end_time', '')} तक"
    t_str_en = f"{t_name} until {tithi.get('end_time', '')}"
    if tithi.get("next"):
        t_str_hi += f" तत्पश्चात् {_hi(HINDI_TITHIS, tithi['next'])}"
        t_str_en += f", then {tithi['next']}"

    # Nakshatra string
    n_name = nakshatra.get("name", "")
    n_hi = _hi(HINDI_NAKSHATRAS, n_name)
    n_str_hi = f"{n_hi} (पद {nakshatra.get('pada', '')}) {nakshatra.get('end_time', '')} तक"
    n_str_en = f"{n_name} (Pada {nakshatra.get('pada', '')}) until {nakshatra.get('end_time', '')}"
    if nakshatra.get("next"):
        n_str_hi += f" तत्पश्चात् {_hi(HINDI_NAKSHATRAS, nakshatra['next'])}"
        n_str_en += f", then {nakshatra['next']}"

    # Yoga string
    y_name = yoga.get("name", "")
    y_hi = _hi(HINDI_YOGAS, y_name)
    y_str_hi = f"{y_hi} {yoga.get('end_time', '')} तक"
    y_str_en = f"{y_name} until {yoga.get('end_time', '')}"
    if yoga.get("next"):
        y_str_hi += f" तत्पश्चात् {_hi(HINDI_YOGAS, yoga['next'])}"
        y_str_en += f", then {yoga['next']}"

    # Karana string
    k_name = karana.get("name", "")
    k_str_en = f"{k_name} until {karana.get('end_time', '')}"
    k_str_hi = f"{k_name} {karana.get('end_time', '')} तक"
    if karana.get("second_karana"):
        k_str_en += f", then {karana['second_karana']}"
        k_str_hi += f" तत्पश्चात् {karana['second_karana']}"

    # ── PDF ──────────────────────────────────────────────────────
    class SummaryPDF(FPDF):
        def __init__(self):
            super().__init__()
            self._h = False
            if has_hindi:
                self.add_font("Hi", "", hindi_font_path, uni=True)
                self._h = True

        def footer(self):
            self.set_y(-10)
            self.set_font("Helvetica", "I", 7)
            self.set_text_color(*MUTED)
            self.cell(0, 6, f"Generated by AstroRattan.com  |  {datetime.now().strftime('%d %b %Y, %I:%M %p')}", align="C")

        def _use_font(self, sz=10):
            if self._h:
                self.set_font("Hi", "", sz)
            else:
                self.set_font("Helvetica", "", sz)

        def line_item(self, label_hi, label_en, val_hi, val_en):
            """Print one summary line: Hindi label — Hindi value / English label — English value"""
            self._use_font(10)
            self.set_text_color(*DARK)
            if self._h:
                self.cell(0, 6.5, f"  {label_hi} — {val_hi}", new_x="LMARGIN", new_y="NEXT")
                self.set_text_color(*MUTED)
                self._use_font(8)
                self.cell(0, 5, f"     {label_en} — {val_en}", new_x="LMARGIN", new_y="NEXT")
            else:
                self.cell(0, 6.5, f"  {label_en} — {val_en}", new_x="LMARGIN", new_y="NEXT")
            self.ln(1)

        def section_sep(self, title_hi, title_en):
            self.ln(2)
            self.set_fill_color(*SAFFRON)
            self.set_text_color(*WHITE)
            self._use_font(11)
            lbl = f"  {title_hi}  |  {title_en}" if self._h else f"  {title_en}"
            self.cell(0, 7, lbl, fill=True, new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(*DARK)
            self.ln(3)

    pdf = SummaryPDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()

    # ── Header ───────────────────────────────────────────────────
    pdf.set_fill_color(*SAFFRON)
    pdf.rect(0, 0, 210, 30, "F")
    pdf.set_text_color(*WHITE)
    pdf._use_font(20)
    pdf.set_y(5)
    title = "卐  हिन्दू पंचांग  卐" if pdf._h else "Hindu Panchang"
    pdf.cell(0, 10, title, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf._use_font(10)
    pdf.cell(0, 7, f"{date_hi}  |  {date_en}  |  {day_hi} / {day_en}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(33)
    pdf.set_text_color(*DARK)

    # ── Hindu Calendar ───────────────────────────────────────────
    pdf.section_sep("हिन्दू पंचांग", "Hindu Calendar")
    pdf.line_item("विक्रम संवत्", "Vikram Samvat", str(hc.get("vikram_samvat", "")), str(hc.get("vikram_samvat", "")))
    pdf.line_item("शक संवत्", "Shaka Samvat", str(hc.get("shaka_samvat", "")), str(hc.get("shaka_samvat", "")))
    pdf.line_item("अयन", "Ayana", _hi(HINDI_AYANA, hc.get("ayana", "")), hc.get("ayana", ""))
    pdf.line_item("ऋतु", "Ritu", _hi(HINDI_RITU, hc.get("ritu", "")), f"{hc.get('ritu', '')} ({hc.get('ritu_english', '')})")
    pdf.line_item("मास", "Month", _hi(HINDI_MAAS, hc.get("maas", "")), hc.get("maas", ""))
    pdf.line_item("पक्ष", "Paksha", _hi(HINDI_PAKSHA, hc.get("paksha", "")), hc.get("paksha", ""))

    # ── Panchang Details ─────────────────────────────────────────
    pdf.section_sep("पंचांग विवरण", "Panchang Details")
    pdf.line_item("तिथि", "Tithi", t_str_hi, t_str_en)
    pdf.line_item("नक्षत्र", "Nakshatra", n_str_hi, n_str_en)
    pdf.line_item("योग", "Yoga", y_str_hi, y_str_en)
    pdf.line_item("करण", "Karana", k_str_hi, k_str_en)

    # ── Timings ──────────────────────────────────────────────────
    pdf.section_sep("समय", "Timings")
    pdf.line_item("सूर्योदय", "Sunrise", panchang.get("sunrise", "--"), panchang.get("sunrise", "--"))
    pdf.line_item("सूर्यास्त", "Sunset", panchang.get("sunset", "--"), panchang.get("sunset", "--"))
    pdf.line_item("चन्द्रोदय", "Moonrise", panchang.get("moonrise", "--"), panchang.get("moonrise", "--"))
    pdf.line_item("चन्द्रास्त", "Moonset", panchang.get("moonset", "--"), panchang.get("moonset", "--"))
    pdf.line_item("दिनमान", "Day Duration", panchang.get("dinamana", "--"), panchang.get("dinamana", "--"))
    pdf.line_item("रात्रिमान", "Night Duration", panchang.get("ratrimana", "--"), panchang.get("ratrimana", "--"))

    # ── Muhurat ──────────────────────────────────────────────────
    pdf.section_sep("मुहूर्त", "Muhurat & Inauspicious Periods")
    pdf.line_item("राहुकाल", "Rahu Kaal", _period(rahu), _period(rahu))
    pdf.line_item("गुलिक काल", "Gulika Kaal", _period(gulika), _period(gulika))
    pdf.line_item("यमगण्ड", "Yamaganda", _period(yamag), _period(yamag))
    pdf.line_item("ब्रह्ममुहूर्त", "Brahma Muhurat", _period(brahma), _period(brahma))
    pdf.line_item("अभिजीत मुहूर्त", "Abhijit Muhurat", _period(abhijit), _period(abhijit))
    pdf.line_item("निशिता मुहूर्त", "Nishita Muhurat", _period(nishita), _period(nishita))

    # ── Sun & Moon ───────────────────────────────────────────────
    sun_s = panchang.get("sun_sign", "")
    moon_s = panchang.get("moon_sign", "")
    pdf.section_sep("ग्रह स्थिति", "Sun & Moon")
    pdf.line_item("सूर्य राशि", "Sun Sign", f"{_hi(HINDI_RASHIS, sun_s)}", sun_s)
    pdf.line_item("चन्द्र राशि", "Moon Sign", f"{_hi(HINDI_RASHIS, moon_s)}", moon_s)

    # ── Festivals ────────────────────────────────────────────────
    if festivals:
        pdf.section_sep("व्रत / पर्व", "Festivals & Observances")
        for f in festivals:
            fname = f.get("name", f) if isinstance(f, dict) else str(f)
            fname_hi = f.get("name_hindi", f.get("hindi_name", fname)) if isinstance(f, dict) else fname
            pdf._use_font(10)
            pdf.set_text_color(*DARK)
            if pdf._h and fname_hi != fname:
                pdf.cell(0, 6, f"  • {fname_hi} / {fname}", new_x="LMARGIN", new_y="NEXT")
            else:
                pdf.cell(0, 6, f"  • {fname}", new_x="LMARGIN", new_y="NEXT")

    # ── Choghadiya (compact) ─────────────────────────────────────
    if choghadiya:
        pdf.section_sep("चौघडिया", "Choghadiya")
        pdf._use_font(9)
        for i, c in enumerate(choghadiya):
            name = c.get("name", "")
            q = c.get("quality", "")
            hi_name = HINDI_CHOGHADIYA_QUALITY.get(name, name) if has_hindi else name
            line = f"  {i+1}. {hi_name} / {name}  ({q})  {c.get('start', '')} - {c.get('end', '')}"
            pdf.cell(0, 5.5, line, new_x="LMARGIN", new_y="NEXT")

    # ── Planetary Positions (compact) ────────────────────────────
    if planets:
        pdf.section_sep("नवग्रह स्थिति", "Planetary Positions")
        pdf._use_font(9)
        for p in planets:
            n = p.get("name", "")
            hi_n = HINDI_PLANETS.get(n, n) if has_hindi else n
            r = p.get("rashi", "")
            hi_r = _hi(HINDI_RASHIS, r)
            d = p.get("degree", 0)
            line = f"  {hi_n} / {n}  —  {d:.1f}°  {hi_r} / {r}"
            pdf.cell(0, 5.5, line, new_x="LMARGIN", new_y="NEXT")

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
        gregorian_date=target_date,
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


@router.post("/api/admin/panchang/cleanup-cache", status_code=status.HTTP_200_OK)
def cleanup_panchang_cache(
    max_age_days: int = Query(default=7, ge=1),
    db: Any = Depends(get_db),
    current_user: dict = Depends(require_role("admin")),
):
    """
    Remove panchang cache entries older than max_age_days.
    Requires admin privileges.
    """
    result = db.execute(
        "DELETE FROM panchang_cache WHERE created_at < NOW() - INTERVAL '%s days'",
        (max_age_days,)
    )
    db.commit()
    return {
        "message": f"Cleaned up {result.rowcount} old cache entries",
        "deleted_count": result.rowcount,
        "max_age_days": max_age_days,
    }
