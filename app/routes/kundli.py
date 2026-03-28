"""Kundli routes — generate, retrieve, list, iogita analysis, match, dosha, dasha, divisional, ashtakvarga, avakhada, yogas, geocode, pdf."""
import io
import json
from typing import Any

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse

from app.auth import get_current_user
from app.database import get_db
from app.models import KundliRequest, KundliMatchRequest, DivisionalChartRequest
from app.astro_engine import calculate_planet_positions
from app.astro_iogita_engine import run_astro_analysis
from app.matching_engine import calculate_gun_milan
from app.dosha_engine import check_mangal_dosha, check_kaal_sarp, check_sade_sati, analyze_yogas_and_doshas
from app.dasha_engine import calculate_dasha, calculate_extended_dasha
from app.divisional_charts import (
    calculate_divisional_chart,
    calculate_divisional_chart_detailed,
    calculate_divisional_houses,
    DIVISIONAL_CHARTS,
)
from app.ashtakvarga_engine import calculate_ashtakvarga
from app.shadbala_engine import calculate_shadbala
from app.avakhada_engine import calculate_avakhada
from app.transit_engine import calculate_transits
from app.kp_engine import calculate_kp_cuspal

router = APIRouter(prefix="/api/kundli", tags=["kundli"])


# ── geocode ─────────────────────────────────────────────────

@router.get("/geocode", status_code=status.HTTP_200_OK)
async def geocode_place(query: str = Query(..., min_length=2, description="Place name to geocode")):
    """Geocode a place name using the free Nominatim OpenStreetMap API."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                "https://nominatim.openstreetmap.org/search",
                params={"q": query, "format": "json", "limit": 5},
                headers={"User-Agent": "AstroRattan/1.0"},
            )
            resp.raise_for_status()
            results = resp.json()
            return [
                {"name": r["display_name"], "lat": float(r["lat"]), "lon": float(r["lon"])}
                for r in results
            ]
    except httpx.HTTPError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Geocoding service unavailable. Please enter coordinates manually.",
        )


# ── helpers ──────────────────────────────────────────────────
def _fetch_kundli(db: Any, kundli_id: str, user_id: str) -> dict:
    """Fetch a kundli row or raise 404. Returns dict(row)."""
    row = db.execute(
        "SELECT * FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user_id),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kundli not found")
    return dict(row)


def _chart_data(row: dict) -> dict:
    """Parse the JSON chart_data column from a kundli row."""
    return json.loads(row["chart_data"])


# ── routes ───────────────────────────────────────────────────

@router.post("/generate", status_code=status.HTTP_201_CREATED)
def generate_kundli(
    body: KundliRequest,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Generate a new Vedic birth chart (kundli) and store it."""
    chart_data = calculate_planet_positions(
        birth_date=body.birth_date,
        birth_time=body.birth_time,
        latitude=body.latitude,
        longitude=body.longitude,
        tz_offset=body.timezone_offset,
    )
    chart_json = json.dumps(chart_data, default=str)

    db.execute(
        """INSERT INTO kundlis
           (user_id, person_name, birth_date, birth_time, birth_place,
            latitude, longitude, timezone_offset, ayanamsa, chart_data)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (
            current_user["sub"],
            body.person_name,
            body.birth_date,
            body.birth_time,
            body.birth_place,
            body.latitude,
            body.longitude,
            body.timezone_offset,
            body.ayanamsa,
            chart_json,
        ),
    )
    db.commit()

    row = db.execute(
        "SELECT * FROM kundlis WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
        (current_user["sub"],),
    ).fetchone()

    return {
        "id": row["id"],
        "person_name": row["person_name"],
        "birth_date": row["birth_date"],
        "birth_time": row["birth_time"],
        "birth_place": row["birth_place"],
        "chart_data": json.loads(row["chart_data"]),
        "created_at": row["created_at"],
    }


@router.get("/list", status_code=status.HTTP_200_OK)
def list_kundlis(
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """List all kundlis for the current user."""
    rows = db.execute(
        "SELECT id, person_name, birth_date, birth_time, birth_place, created_at "
        "FROM kundlis WHERE user_id = %s ORDER BY created_at DESC",
        (current_user["sub"],),
    ).fetchall()

    return [
        {
            "id": r["id"],
            "person_name": r["person_name"],
            "birth_date": r["birth_date"],
            "birth_time": r["birth_time"],
            "birth_place": r["birth_place"],
            "created_at": r["created_at"],
        }
        for r in rows
    ]


@router.get("/{kundli_id}", status_code=status.HTTP_200_OK)
def get_kundli(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Retrieve a single kundli by ID."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    return {
        "id": row["id"],
        "person_name": row["person_name"],
        "birth_date": row["birth_date"],
        "birth_time": row["birth_time"],
        "birth_place": row["birth_place"],
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "timezone_offset": row["timezone_offset"],
        "ayanamsa": row["ayanamsa"],
        "chart_data": json.loads(row["chart_data"]),
        "iogita_analysis": json.loads(row["iogita_analysis"]) if row["iogita_analysis"] else None,
        "created_at": row["created_at"],
    }


@router.post("/{kundli_id}/iogita", status_code=status.HTTP_200_OK)
def run_iogita_analysis(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Run io-gita atom engine analysis on a kundli."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)

    # Build planet_positions as {planet: sign}
    planet_positions = {}
    for planet_name, info in chart.get("planets", {}).items():
        planet_positions[planet_name] = info["sign"]

    # Need dasha to determine current mahadasha lord
    moon_info = chart.get("planets", {}).get("Moon", {})
    moon_nakshatra = moon_info.get("nakshatra", "Ashwini")
    dasha_result = calculate_dasha(moon_nakshatra, row["birth_date"])
    current_dasha = dasha_result.get("current_dasha", "Venus")

    analysis = run_astro_analysis(planet_positions, current_dasha, row["person_name"])

    # Store analysis on the kundli row
    analysis_json = json.dumps(analysis, default=str)
    db.execute(
        "UPDATE kundlis SET iogita_analysis = %s WHERE id = %s",
        (analysis_json, kundli_id),
    )
    db.commit()

    return analysis


@router.post("/match", status_code=status.HTTP_200_OK)
def match_kundlis(
    body: KundliMatchRequest,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Ashtakoota Gun Milan — match two kundlis for compatibility."""
    row1 = _fetch_kundli(db, body.kundli_id_1, current_user["sub"])
    row2 = _fetch_kundli(db, body.kundli_id_2, current_user["sub"])

    chart1 = _chart_data(row1)
    chart2 = _chart_data(row2)

    moon1 = chart1.get("planets", {}).get("Moon", {}).get("nakshatra", "Ashwini")
    moon2 = chart2.get("planets", {}).get("Moon", {}).get("nakshatra", "Ashwini")

    result = calculate_gun_milan(moon1, moon2)
    result["person1"] = row1["person_name"]
    result["person2"] = row2["person_name"]
    return result


@router.post("/{kundli_id}/dosha", status_code=status.HTTP_200_OK)
def check_doshas(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Check Mangal Dosha, Kaal Sarp Dosha, and Sade Sati."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)
    planets = chart.get("planets", {})

    # Mangal Dosha
    mars_house = planets.get("Mars", {}).get("house", 1)
    mangal = check_mangal_dosha(mars_house)

    # Kaal Sarp Dosha
    rahu_house = planets.get("Rahu", {}).get("house", 1)
    ketu_house = planets.get("Ketu", {}).get("house", 7)
    planet_houses = {}
    for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        if p in planets:
            planet_houses[p] = planets[p].get("house", 1)
    kaal_sarp = check_kaal_sarp(rahu_house, ketu_house, planet_houses)

    # Sade Sati (use Moon sign + Saturn sign from chart)
    moon_sign = planets.get("Moon", {}).get("sign", "Aries")
    saturn_sign = planets.get("Saturn", {}).get("sign", "Capricorn")
    sade_sati = check_sade_sati(moon_sign, saturn_sign)

    return {
        "kundli_id": kundli_id,
        "person_name": row["person_name"],
        "mangal_dosha": mangal,
        "kaal_sarp_dosha": kaal_sarp,
        "sade_sati": sade_sati,
    }


@router.post("/{kundli_id}/dasha", status_code=status.HTTP_200_OK)
def get_dasha(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Calculate Vimshottari Dasha periods for a kundli."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)

    moon_nakshatra = chart.get("planets", {}).get("Moon", {}).get("nakshatra", "Ashwini")
    result = calculate_dasha(moon_nakshatra, row["birth_date"])
    result["kundli_id"] = kundli_id
    result["person_name"] = row["person_name"]
    return result


@router.get("/{kundli_id}/divisional-charts", status_code=status.HTTP_200_OK)
def list_divisional_charts(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """List available divisional chart types."""
    _fetch_kundli(db, kundli_id, current_user["sub"])  # Validate access
    return {
        "kundli_id": kundli_id,
        "charts": [
            {"division": d, "name": name, "code": f"D{d}"}
            for d, name in DIVISIONAL_CHARTS.items()
        ],
    }


@router.post("/{kundli_id}/divisional", status_code=status.HTTP_200_OK)
def get_divisional_chart(
    kundli_id: str,
    body: DivisionalChartRequest,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Calculate a divisional (varga) chart for a kundli."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)

    # Extract planet longitudes
    planet_longitudes = {}
    for planet_name, info in chart.get("planets", {}).items():
        planet_longitudes[planet_name] = info["longitude"]

    # Parse division number from chart_type string (e.g. "D9" -> 9)
    chart_type = body.chart_type.upper()
    try:
        division = int(chart_type.replace("D", ""))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid chart type: {body.chart_type}. Use format 'D9', 'D10', etc.",
        )

    # Get detailed result with degree info
    detailed = calculate_divisional_chart_detailed(planet_longitudes, division)

    # Calculate divisional houses relative to divisional ascendant
    asc_longitude = chart.get("ascendant", {}).get("longitude", 0.0)
    houses = calculate_divisional_houses(asc_longitude, division)

    # Build a lookup: sign -> house number (for mapping planets to houses)
    sign_to_house = {h["sign"]: h["number"] for h in houses}

    # Build planet data suitable for InteractiveKundli component
    planet_positions = []
    for planet_name, info in detailed.items():
        sign_index = info["sign_index"]
        # House is relative to divisional ascendant, not absolute sign index
        house_num = sign_to_house.get(info["sign"], sign_index + 1)
        planet_positions.append({
            "planet": planet_name,
            "sign": info["sign"],
            "sign_degree": info["degree"],
            "house": house_num,
            "nakshatra": "",
            "longitude": sign_index * 30.0 + info["degree"],
        })

    # Simple sign mapping for backward compat
    planet_signs = {planet: info["sign"] for planet, info in detailed.items()}

    chart_name = DIVISIONAL_CHARTS.get(division, f"D{division}")

    return {
        "kundli_id": kundli_id,
        "person_name": row["person_name"],
        "chart_type": chart_type,
        "chart_name": chart_name,
        "division": division,
        "planet_signs": planet_signs,
        "planet_positions": planet_positions,
        "houses": houses,
    }


@router.post("/{kundli_id}/ashtakvarga", status_code=status.HTTP_200_OK)
def get_ashtakvarga(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Calculate Ashtakvarga point system for a kundli."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)

    # Build planet_signs: {planet: sign, Ascendant: sign}
    planet_signs = {}
    for planet_name, info in chart.get("planets", {}).items():
        planet_signs[planet_name] = info["sign"]

    ascendant_sign = chart.get("ascendant", {}).get("sign")
    if ascendant_sign:
        planet_signs["Ascendant"] = ascendant_sign

    result = calculate_ashtakvarga(planet_signs)
    result["kundli_id"] = kundli_id
    result["person_name"] = row["person_name"]
    return result


@router.post("/{kundli_id}/shadbala", status_code=status.HTTP_200_OK)
def get_shadbala(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Calculate Shadbala (six-fold strength) for a kundli."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)
    planets = chart.get("planets", {})

    # Build planet_signs and planet_houses
    planet_signs = {}
    planet_houses = {}
    for planet_name, info in planets.items():
        planet_signs[planet_name] = info.get("sign", "Aries")
        planet_houses[planet_name] = info.get("house", 1)

    # Determine if daytime birth (simplified: hour 6-18 = day)
    birth_time = row.get("birth_time", "12:00:00")
    try:
        hour = int(birth_time.split(":")[0])
    except (ValueError, IndexError):
        hour = 12
    is_daytime = 6 <= hour < 18

    result = calculate_shadbala(
        planet_signs=planet_signs,
        planet_houses=planet_houses,
        is_daytime=is_daytime,
    )
    result["kundli_id"] = kundli_id
    result["person_name"] = row["person_name"]
    return result


@router.get("/{kundli_id}/avakhada", status_code=status.HTTP_200_OK)
def get_avakhada(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Calculate Avakhada Chakra — comprehensive birth summary table."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)
    result = calculate_avakhada(chart)
    result["kundli_id"] = kundli_id
    result["person_name"] = row["person_name"]
    return result


@router.post("/{kundli_id}/extended-dasha", status_code=status.HTTP_200_OK)
def get_extended_dasha(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Calculate extended Vimshottari Dasha with Mahadasha -> Antardasha -> Pratyantar."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)
    moon_nakshatra = chart.get("planets", {}).get("Moon", {}).get("nakshatra", "Ashwini")
    result = calculate_extended_dasha(moon_nakshatra, row["birth_date"])
    result["kundli_id"] = kundli_id
    result["person_name"] = row["person_name"]
    return result


@router.post("/{kundli_id}/yogas-doshas", status_code=status.HTTP_200_OK)
def get_yogas_and_doshas(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Comprehensive Yoga & Dosha analysis — positive yogas and negative doshas."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)
    planets = chart.get("planets", {})
    result = analyze_yogas_and_doshas(planets)
    result["kundli_id"] = kundli_id
    result["person_name"] = row["person_name"]
    return result


# ── PDF Download ────────────────────────────────────────────

# Sign → Lord mapping used for house lordships table
_SIGN_LORD = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

_SIGN_ORDER = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]


def _build_kundli_pdf(row: dict, chart: dict) -> bytes:
    """Build an in-memory Kundli PDF report and return the raw bytes."""
    from fpdf import FPDF

    class KundliPDF(FPDF):
        def header(self):
            self.set_font("Helvetica", "B", 16)
            self.cell(0, 10, "Astro Rattan - Vedic Birth Chart Report", align="C", new_x="LMARGIN", new_y="NEXT")
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.cell(0, 10, f"Page {self.page_no()} | Powered by Semantic Gravity", align="C")

    pdf = KundliPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # ── Birth Details ───────────────────────────────────────
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, f"{row['person_name']}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.set_font("Helvetica", "", 11)
    birth_date = row.get("birth_date", "N/A")
    birth_time = row.get("birth_time", "N/A")
    birth_place = row.get("birth_place", "N/A")
    pdf.cell(0, 7, f"Date of Birth: {birth_date}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"Time of Birth: {birth_time}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"Place of Birth: {birth_place}", align="C", new_x="LMARGIN", new_y="NEXT")
    ayanamsa = row.get("ayanamsa", "lahiri")
    pdf.cell(0, 7, f"Ayanamsa: {ayanamsa.title() if isinstance(ayanamsa, str) else ayanamsa}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    # Ascendant info
    ascendant = chart.get("ascendant", {})
    if ascendant:
        asc_sign = ascendant.get("sign", "N/A")
        asc_deg = ascendant.get("degree", "")
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, f"Ascendant (Lagna): {asc_sign} {asc_deg}\u00b0" if asc_deg else f"Ascendant (Lagna): {asc_sign}", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(6)

    # ── Planet Positions Table ──────────────────────────────
    planets = chart.get("planets", {})
    if planets:
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 10, "Planet Positions", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        # Table header
        col_widths = [30, 32, 22, 38, 38, 30]
        headers = ["Planet", "Sign", "House", "Degree", "Nakshatra", "Retro"]
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_fill_color(245, 235, 210)
        for i, h in enumerate(headers):
            pdf.cell(col_widths[i], 7, h, border=1, align="C", fill=True)
        pdf.ln()

        # Table rows
        pdf.set_font("Helvetica", "", 9)
        for planet_name, info in planets.items():
            if not isinstance(info, dict):
                continue
            sign = info.get("sign", "N/A")
            house = str(info.get("house", "N/A"))
            degree = f"{info.get('degree', 'N/A')}\u00b0" if info.get("degree") is not None else "N/A"
            nakshatra = info.get("nakshatra", "N/A")
            retro = "R" if info.get("retrograde") else ""
            vals = [planet_name, sign, house, degree, nakshatra, retro]
            for i, v in enumerate(vals):
                pdf.cell(col_widths[i], 6, str(v), border=1, align="C")
            pdf.ln()
        pdf.ln(8)

    # ── House Lordships ─────────────────────────────────────
    asc_sign = chart.get("ascendant", {}).get("sign")
    if asc_sign and asc_sign in _SIGN_ORDER:
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 10, "House Lordships", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        pdf.set_font("Helvetica", "B", 9)
        pdf.set_fill_color(245, 235, 210)
        lord_cols = [25, 40, 35]
        for i, h in enumerate(["House", "Sign", "Lord"]):
            pdf.cell(lord_cols[i], 7, h, border=1, align="C", fill=True)
        pdf.ln()

        pdf.set_font("Helvetica", "", 9)
        asc_idx = _SIGN_ORDER.index(asc_sign)
        for house_num in range(1, 13):
            sign = _SIGN_ORDER[(asc_idx + house_num - 1) % 12]
            lord = _SIGN_LORD.get(sign, "N/A")
            pdf.cell(lord_cols[0], 6, str(house_num), border=1, align="C")
            pdf.cell(lord_cols[1], 6, sign, border=1, align="C")
            pdf.cell(lord_cols[2], 6, lord, border=1, align="C")
            pdf.ln()
        pdf.ln(8)

    # ── Yoga / Dosha Summary ────────────────────────────────
    if planets:
        yoga_dosha = analyze_yogas_and_doshas(planets)

        yogas = yoga_dosha.get("yogas", [])
        if yogas:
            pdf.set_font("Helvetica", "B", 13)
            pdf.cell(0, 10, "Yogas (Positive Combinations)", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
            pdf.set_font("Helvetica", "", 9)
            for y in yogas:
                if isinstance(y, dict):
                    name = y.get("name", y.get("yoga", "Yoga"))
                    desc = y.get("description", y.get("effect", ""))
                    pdf.set_font("Helvetica", "B", 9)
                    pdf.cell(0, 6, f"  {name}", new_x="LMARGIN", new_y="NEXT")
                    if desc:
                        pdf.set_font("Helvetica", "", 9)
                        pdf.multi_cell(0, 5, f"    {desc}")
                else:
                    pdf.cell(0, 6, f"  {y}", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(6)

        doshas = yoga_dosha.get("doshas", [])
        if doshas:
            pdf.set_font("Helvetica", "B", 13)
            pdf.cell(0, 10, "Doshas (Afflictions)", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
            pdf.set_font("Helvetica", "", 9)
            for d in doshas:
                if isinstance(d, dict):
                    name = d.get("name", d.get("dosha", "Dosha"))
                    severity = d.get("severity", "")
                    desc = d.get("description", d.get("effect", ""))
                    label = f"  {name}"
                    if severity:
                        label += f" [{severity}]"
                    pdf.set_font("Helvetica", "B", 9)
                    pdf.cell(0, 6, label, new_x="LMARGIN", new_y="NEXT")
                    if desc:
                        pdf.set_font("Helvetica", "", 9)
                        pdf.multi_cell(0, 5, f"    {desc}")
                else:
                    pdf.cell(0, 6, f"  {d}", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(6)

    # ── io-gita Analysis (if stored) ────────────────────────
    iogita_raw = row.get("iogita_analysis")
    if iogita_raw:
        try:
            iogita = json.loads(iogita_raw) if isinstance(iogita_raw, str) else iogita_raw
        except (json.JSONDecodeError, TypeError):
            iogita = None
        if iogita and isinstance(iogita, dict):
            pdf.set_font("Helvetica", "B", 13)
            pdf.cell(0, 10, "io-gita Semantic Gravity Analysis", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
            pdf.set_font("Helvetica", "", 9)
            for key, val in iogita.items():
                text = f"{key}: {val}"
                pdf.multi_cell(0, 5, text)
            pdf.ln(6)

    # Return raw bytes
    return pdf.output()


@router.get("/{kundli_id}/pdf", status_code=status.HTTP_200_OK)
def download_kundli_pdf(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Generate and stream a Kundli PDF report for download."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)

    try:
        pdf_bytes = _build_kundli_pdf(row, chart)
    except ImportError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="PDF generation unavailable — fpdf2 not installed",
        )

    safe_name = (row.get("person_name") or "kundli").replace(" ", "_")
    filename = f"kundli-{safe_name}.pdf"

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/{kundli_id}/transits", status_code=status.HTTP_200_OK)
def get_transits(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Calculate current Gochara (transit) predictions for a kundli."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)
    result = calculate_transits(chart)
    result["kundli_id"] = kundli_id
    result["person_name"] = row["person_name"]
    return result


@router.post("/{kundli_id}/kp-analysis", status_code=status.HTTP_200_OK)
def get_kp_analysis(
    kundli_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """KP (Krishnamurti Paddhati) analysis — sign lord, star lord, sub lord for planets and cusps."""
    row = _fetch_kundli(db, kundli_id, current_user["sub"])
    chart = _chart_data(row)

    # Extract planet longitudes
    planet_longitudes = {}
    for planet_name, info in chart.get("planets", {}).items():
        planet_longitudes[planet_name] = info.get("longitude", 0.0)

    if not planet_longitudes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chart data has no planet longitudes",
        )

    # Extract house cusps (Placidus from swisseph) or fallback to equal houses
    house_cusps = chart.get("house_cusps", [])
    if not house_cusps or len(house_cusps) != 12:
        asc_lon = chart.get("ascendant", {}).get("longitude", 0.0)
        house_cusps = [(asc_lon + i * 30.0) % 360.0 for i in range(12)]

    try:
        kp = calculate_kp_cuspal(planet_longitudes, house_cusps)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"KP calculation error: {str(exc)}",
        )

    # Shape response: planets as list, cusps as list
    planets_list = []
    for pname, pinfo in kp.get("planets", {}).items():
        planets_list.append({
            "planet": pname,
            "sign": pinfo.get("sign", ""),
            "sign_lord": pinfo.get("sign_lord", ""),
            "star_lord": pinfo.get("star_lord", ""),
            "sub_lord": pinfo.get("sub_lord", ""),
            "degree": pinfo.get("longitude", 0.0),
        })

    return {
        "kundli_id": kundli_id,
        "person_name": row["person_name"],
        "planets": planets_list,
        "cusps": kp.get("cusps", []),
        "significators": kp.get("significators", {}),
    }
