"""
jaimini_engine.py — Jaimini Astrology Calculator
==================================================
Implements key Jaimini system components:
  1. Chara Karakas (7 variable significators by degree)
  2. Special Lagnas (Arudha, Upapada, Karakamsha)
  3. Jaimini Drishti (sign-based aspects)
  4. Chara Dasha (sign-based timing)
  5. Indu Lagna (wealth indicator)
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

ZODIAC = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

SIGN_LORD = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

# Sign modality
CARDINAL = {"Aries", "Cancer", "Libra", "Capricorn"}
FIXED = {"Taurus", "Leo", "Scorpio", "Aquarius"}
DUAL = {"Gemini", "Virgo", "Sagittarius", "Pisces"}

# Kaksha values for Indu Lagna
KAKSHA_VALUES = {
    "Sun": 30, "Moon": 16, "Mars": 6, "Mercury": 8,
    "Jupiter": 10, "Venus": 12, "Saturn": 1,
}

KARAKA_NAMES = ["AK", "AmK", "BK", "MK", "PiK", "GnK", "DK"]
KARAKA_FULL = {
    "AK": ("Atmakaraka", "आत्मकारक", "Soul / Self"),
    "AmK": ("Amatyakaraka", "अमात्यकारक", "Career / Minister"),
    "BK": ("Bhratrikaraka", "भ्रातृकारक", "Siblings"),
    "MK": ("Matrikaraka", "मातृकारक", "Mother"),
    "PiK": ("Pitrikaraka", "पितृकारक", "Father"),
    "GnK": ("Gnatikaraka", "ज्ञातिकारक", "Relatives / Enemies"),
    "DK": ("Darakaraka", "दारकारक", "Spouse"),
}


def _sign_index(sign: str) -> int:
    try:
        return ZODIAC.index(sign)
    except ValueError:
        return 0


def _sign_distance(from_sign: str, to_sign: str) -> int:
    """Count houses from from_sign to to_sign (1-indexed)."""
    return ((_sign_index(to_sign) - _sign_index(from_sign)) % 12) + 1


def _sign_at_offset(sign: str, offset: int) -> str:
    """Get sign at N houses from given sign (1-indexed offset)."""
    return ZODIAC[(_sign_index(sign) + offset - 1) % 12]


def _get_planet_sign(planets: Dict, planet_name: str) -> str:
    return planets.get(planet_name, {}).get("sign", "Aries")


def _get_planet_degree(planets: Dict, planet_name: str) -> float:
    p = planets.get(planet_name, {})
    return float(p.get("sign_degree", p.get("longitude", 0.0) % 30.0))


# ============================================================
# 1. CHARA KARAKAS
# ============================================================

def calculate_chara_karakas(planets: Dict) -> List[Dict]:
    """
    Sort 7 planets (Sun through Saturn) by sign_degree descending.
    Highest degree = Atmakaraka, lowest = Darakaraka.
    """
    karaka_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    entries = []
    for name in karaka_planets:
        deg = _get_planet_degree(planets, name)
        entries.append({"planet": name, "degree": round(deg, 2)})

    entries.sort(key=lambda x: x["degree"], reverse=True)

    result = []
    for i, entry in enumerate(entries):
        karaka = KARAKA_NAMES[i] if i < len(KARAKA_NAMES) else f"K{i+1}"
        full = KARAKA_FULL.get(karaka, (karaka, karaka, ""))
        result.append({
            "planet": entry["planet"],
            "degree": entry["degree"],
            "karaka": karaka,
            "name_en": full[0],
            "name_hi": full[1],
            "significance": full[2],
        })

    return result


# ============================================================
# 2. SPECIAL LAGNAS
# ============================================================

def calculate_special_lagnas(planets: Dict, ascendant: Dict, d9_planets: Optional[Dict] = None) -> Dict:
    """
    Arudha Lagna (AL), Upapada Lagna (UL), Karakamsha.
    """
    asc_sign = ascendant.get("sign", "Aries") if ascendant else "Aries"
    asc_idx = _sign_index(asc_sign)

    # --- Arudha Lagna ---
    asc_lord = SIGN_LORD[asc_sign]
    lord_sign = _get_planet_sign(planets, asc_lord)
    dist = _sign_distance(asc_sign, lord_sign)

    # Exception: if lord in 1st or 7th from ascendant, use 10th or 4th instead
    if dist == 1:
        al_sign = _sign_at_offset(asc_sign, 10)
    elif dist == 7:
        al_sign = _sign_at_offset(asc_sign, 4)
    else:
        al_sign = _sign_at_offset(lord_sign, dist)

    # --- Upapada Lagna (from 12th house) ---
    twelfth_sign = _sign_at_offset(asc_sign, 12)
    twelfth_lord = SIGN_LORD[twelfth_sign]
    twelfth_lord_sign = _get_planet_sign(planets, twelfth_lord)
    dist12 = _sign_distance(twelfth_sign, twelfth_lord_sign)

    if dist12 == 1:
        ul_sign = _sign_at_offset(twelfth_sign, 10)
    elif dist12 == 7:
        ul_sign = _sign_at_offset(twelfth_sign, 4)
    else:
        ul_sign = _sign_at_offset(twelfth_lord_sign, dist12)

    # --- Karakamsha (D9 sign of Atmakaraka) ---
    karakas = calculate_chara_karakas(planets)
    ak_planet = karakas[0]["planet"] if karakas else "Sun"

    karakamsha_sign = "Unknown"
    if d9_planets:
        karakamsha_sign = _get_planet_sign(d9_planets, ak_planet)
    else:
        # Approximate: use sign degree to compute Navamsha sign
        ak_lon = planets.get(ak_planet, {}).get("longitude", 0.0)
        d9_index = int((float(ak_lon) % 360.0) / (360.0 / 108.0)) % 12
        karakamsha_sign = ZODIAC[d9_index]

    # --- Hora Lagna ---
    # Based on Sun's longitude: each hora = 15° of Sun movement from sunrise
    # Approximate: Sun longitude / 15 → sign offset from ascendant
    sun_lon = float(planets.get("Sun", {}).get("longitude", 0.0))
    hora_offset = int((sun_lon % 360.0) / 15.0) % 12
    hora_sign = ZODIAC[(asc_idx + hora_offset) % 12]

    # --- Ghatika Lagna ---
    # Based on Sun's position relative to sunrise (sunrise = lagna)
    # Approximate: each ghatika = 24 minutes. Use Sun's house position.
    sun_house = int(planets.get("Sun", {}).get("house", 1))
    ghatika_offset = (sun_house - 1 + 5) % 12  # 5th from Sun's house
    ghatika_sign = ZODIAC[(asc_idx + ghatika_offset) % 12]

    # --- Varnada Lagna ---
    # If lagna is odd sign: Varnada = Aries + (lagna_idx + hora_offset)
    # If lagna is even sign: Varnada = Pisces - (lagna_idx + hora_offset)
    if asc_idx % 2 == 0:  # odd sign (Aries, Gemini, etc.)
        varnada_idx = (asc_idx + hora_offset) % 12
    else:  # even sign
        varnada_idx = (11 - asc_idx + hora_offset) % 12  # 11 = Pisces index
    varnada_sign = ZODIAC[varnada_idx]

    return {
        "arudha_lagna": {
            "sign": al_sign,
            "house": _sign_distance(asc_sign, al_sign),
            "description_en": "How the world perceives you",
            "description_hi": "संसार आपको कैसे देखता है",
        },
        "upapada_lagna": {
            "sign": ul_sign,
            "house": _sign_distance(asc_sign, ul_sign),
            "description_en": "Marriage & spouse indicator",
            "description_hi": "विवाह और जीवनसाथी सूचक",
        },
        "karakamsha": {
            "sign": karakamsha_sign,
            "atmakaraka": ak_planet,
            "house": _sign_distance(asc_sign, karakamsha_sign),
            "description_en": "Soul's journey (AK in Navamsha D9)",
            "description_hi": "आत्मा की यात्रा (AK नवांश में)",
        },
        "hora_lagna": {
            "sign": hora_sign,
            "house": _sign_distance(asc_sign, hora_sign),
            "description_en": "Wealth & financial status",
            "description_hi": "धन और आर्थिक स्थिति",
        },
        "ghatika_lagna": {
            "sign": ghatika_sign,
            "house": _sign_distance(asc_sign, ghatika_sign),
            "description_en": "Power, authority & social status",
            "description_hi": "शक्ति, अधिकार और सामाजिक स्थिति",
        },
        "varnada_lagna": {
            "sign": varnada_sign,
            "house": _sign_distance(asc_sign, varnada_sign),
            "description_en": "Purpose & dharmic calling",
            "description_hi": "उद्देश्य और धार्मिक कर्तव्य",
        },
    }


# ============================================================
# 3. JAIMINI DRISHTI (Sign-based aspects)
# ============================================================

def calculate_jaimini_drishti() -> Dict:
    """
    Cardinal signs aspect Fixed signs (except adjacent).
    Fixed signs aspect Cardinal signs (except adjacent).
    Dual signs aspect all other Dual signs.
    """
    aspects: Dict[str, List[str]] = {}

    for sign in ZODIAC:
        idx = _sign_index(sign)
        aspected = []

        if sign in CARDINAL:
            for target in FIXED:
                t_idx = _sign_index(target)
                if abs(idx - t_idx) != 1 and abs(idx - t_idx) != 11:
                    aspected.append(target)
        elif sign in FIXED:
            for target in CARDINAL:
                t_idx = _sign_index(target)
                if abs(idx - t_idx) != 1 and abs(idx - t_idx) != 11:
                    aspected.append(target)
        else:  # DUAL
            for target in DUAL:
                if target != sign:
                    aspected.append(target)

        aspects[sign] = aspected

    return {"sign_aspects": aspects}


# ============================================================
# 4. CHARA DASHA (Sign-based timing)
# ============================================================

def calculate_chara_dasha(planets: Dict, ascendant: Dict, birth_date: str) -> Dict:
    """
    Chara Dasha periods based on sign distances.
    Each sign gets a period = distance from sign to its lord's sign.
    """
    asc_sign = ascendant.get("sign", "Aries") if ascendant else "Aries"
    asc_idx = _sign_index(asc_sign)

    # Determine order: odd sign = forward, even sign = backward
    is_odd = asc_idx % 2 == 0  # Aries=0 (odd sign), Taurus=1 (even sign)

    if is_odd:
        sign_order = [ZODIAC[(asc_idx + i) % 12] for i in range(12)]
    else:
        sign_order = [ZODIAC[(asc_idx - i) % 12] for i in range(12)]

    # Calculate period for each sign
    periods = []
    try:
        start = datetime.strptime(str(birth_date).split("T")[0].split(" ")[0], "%Y-%m-%d")
    except Exception:
        start = datetime(2000, 1, 1)

    for sign in sign_order:
        lord = SIGN_LORD[sign]
        lord_sign = _get_planet_sign(planets, lord)
        dist = _sign_distance(sign, lord_sign)

        # For even signs, adjust: years = 12 - dist
        s_idx = _sign_index(sign)
        if s_idx % 2 == 1:  # even sign
            years = 12 - dist
        else:
            years = dist - 1  # 0-indexed

        years = max(1, min(years, 12))  # clamp 1-12

        end = start + timedelta(days=years * 365.25)
        periods.append({
            "sign": sign,
            "lord": lord,
            "years": years,
            "start_date": start.strftime("%Y-%m-%d"),
            "end_date": end.strftime("%Y-%m-%d"),
        })
        start = end

    # Mark current period
    now = datetime.now()
    current_idx = -1
    for i, p in enumerate(periods):
        s = datetime.strptime(p["start_date"], "%Y-%m-%d")
        e = datetime.strptime(p["end_date"], "%Y-%m-%d")
        if s <= now <= e:
            current_idx = i
            break

    return {
        "periods": periods,
        "current_period_index": current_idx,
        "total_years": sum(p["years"] for p in periods),
    }


# ============================================================
# 5. INDU LAGNA (Wealth indicator)
# ============================================================

def calculate_indu_lagna(planets: Dict, ascendant: Dict) -> Dict:
    """
    Indu Lagna calculation:
    1. Find 9th lord from Lagna
    2. Find 9th lord from Moon
    3. Add Kaksha values of both lords
    4. Remainder when divided by 12 → count from Moon sign
    """
    asc_sign = ascendant.get("sign", "Aries") if ascendant else "Aries"
    moon_sign = _get_planet_sign(planets, "Moon")

    # 9th house from Lagna
    ninth_from_lagna = _sign_at_offset(asc_sign, 9)
    ninth_lord_lagna = SIGN_LORD[ninth_from_lagna]

    # 9th house from Moon
    ninth_from_moon = _sign_at_offset(moon_sign, 9)
    ninth_lord_moon = SIGN_LORD[ninth_from_moon]

    kaksha_1 = KAKSHA_VALUES.get(ninth_lord_lagna, 1)
    kaksha_2 = KAKSHA_VALUES.get(ninth_lord_moon, 1)
    total = kaksha_1 + kaksha_2
    remainder = total % 12

    # Count remainder from TAURUS (not Moon) — standard Jaimini rule
    indu_sign = _sign_at_offset("Taurus", remainder)  # remainder houses from Taurus

    return {
        "indu_lagna_sign": indu_sign,
        "indu_lagna_house": _sign_distance(asc_sign, indu_sign),
        "ninth_lord_lagna": ninth_lord_lagna,
        "ninth_lord_moon": ninth_lord_moon,
        "kaksha_sum": total,
        "remainder": remainder,
    }


# ============================================================
# 6. ARGALA (Planetary Intervention)
# ============================================================

def calculate_argala(planets: Dict, ascendant: Dict) -> Dict:
    """
    Argala = planetary influence from specific houses.
    Argala houses: 2nd, 4th, 11th, 5th from any house → promote results.
    Virodha Argala (obstruction): 12th (blocks 2nd), 10th (blocks 4th),
      3rd (blocks 11th), 9th (blocks 5th).
    Argala holds if promoting planets > obstructing planets.
    """
    asc_sign = ascendant.get("sign", "Aries") if ascendant else "Aries"

    # Build planet-to-house mapping
    planet_houses: Dict[str, int] = {}
    for name, data in planets.items():
        if isinstance(data, dict):
            planet_houses[name] = int(data.get("house", 1))

    # Planets in each house
    houses_planets: Dict[int, List[str]] = {h: [] for h in range(1, 13)}
    for name, house in planet_houses.items():
        if 1 <= house <= 12:
            houses_planets[house].append(name)

    ARGALA_PAIRS = [
        (2, 12, "Secondary Argala (2nd house) — wealth, speech"),
        (4, 10, "Secondary Argala (4th house) — happiness, property"),
        (11, 3, "Primary Argala (11th house) — gains, desires"),
        (5, 9, "Primary Argala (5th house) — children, merit"),
    ]

    result = []
    for house_num in range(1, 13):
        house_argala = []
        for argala_offset, virodha_offset, desc in ARGALA_PAIRS:
            argala_house = ((house_num - 1 + argala_offset) % 12) + 1
            virodha_house = ((house_num - 1 + virodha_offset) % 12) + 1

            argala_planets = houses_planets.get(argala_house, [])
            virodha_planets = houses_planets.get(virodha_house, [])

            if argala_planets:
                blocked = len(virodha_planets) >= len(argala_planets)
                house_argala.append({
                    "type": desc,
                    "from_house": argala_house,
                    "planets": argala_planets,
                    "virodha_house": virodha_house,
                    "virodha_planets": virodha_planets,
                    "blocked": blocked,
                    "status": "Blocked" if blocked else "Active",
                })

        if house_argala:
            result.append({"house": house_num, "argalas": house_argala})

    return {"house_argalas": result}


# ============================================================
# 7. JAIMINI YOGAS
# ============================================================

def calculate_jaimini_yogas(planets: Dict, ascendant: Dict) -> List[Dict]:
    """
    Key Jaimini Yogas based on Karaka relationships and Arudha Padas.
    """
    asc_sign = ascendant.get("sign", "Aries") if ascendant else "Aries"
    karakas = calculate_chara_karakas(planets)
    karaka_map = {k["karaka"]: k for k in karakas}

    yogas = []

    # Get special lagnas for Arudha-based yogas
    lagnas = calculate_special_lagnas(planets, ascendant)
    al_house = lagnas["arudha_lagna"]["house"]

    # 1. Jaimini Raja Yoga: AK and AmK in kendras (1,4,7,10) from each other
    ak = karaka_map.get("AK", {})
    amk = karaka_map.get("AmK", {})
    if ak and amk:
        ak_house = int(planets.get(ak["planet"], {}).get("house", 1))
        amk_house = int(planets.get(amk["planet"], {}).get("house", 1))
        dist = abs(ak_house - amk_house) % 12
        if dist in [0, 3, 6, 9]:  # kendra positions
            yogas.append({
                "name_en": "Jaimini Raja Yoga",
                "name_hi": "जैमिनी राज योग",
                "present": True,
                "description_en": f"AK ({ak['planet']}) and AmK ({amk['planet']}) in kendra — leadership & authority",
                "description_hi": f"AK ({ak['planet']}) और AmK ({amk['planet']}) केंद्र में — नेतृत्व और अधिकार",
                "strength": "Strong" if dist == 0 else "Moderate",
            })

    # 2. Dhana Yoga: Planets in 2nd or 11th from Arudha Lagna
    second_from_al = ((al_house - 1 + 1) % 12) + 1
    eleventh_from_al = ((al_house - 1 + 10) % 12) + 1
    wealth_planets = []
    for name, data in planets.items():
        if isinstance(data, dict):
            h = int(data.get("house", 0))
            if h == second_from_al or h == eleventh_from_al:
                wealth_planets.append(name)
    if wealth_planets:
        yogas.append({
            "name_en": "Dhana Yoga (from Arudha)",
            "name_hi": "धन योग (आरूढ़ से)",
            "present": True,
            "description_en": f"Planets in 2nd/11th from AL: {', '.join(wealth_planets)} — wealth accumulation",
            "description_hi": f"AL से 2/11 भाव में ग्रह: {', '.join(wealth_planets)} — धन संचय",
            "strength": "Strong" if len(wealth_planets) >= 2 else "Moderate",
        })

    # 3. AK-DK Yoga: Connection between Atmakaraka and Darakaraka
    dk = karaka_map.get("DK", {})
    if ak and dk:
        ak_house = int(planets.get(ak["planet"], {}).get("house", 1))
        dk_house = int(planets.get(dk["planet"], {}).get("house", 1))
        dist = abs(ak_house - dk_house) % 12
        if dist in [0, 3, 6, 9]:  # kendra
            yogas.append({
                "name_en": "AK-DK Kendra Yoga",
                "name_hi": "AK-DK केंद्र योग",
                "present": True,
                "description_en": f"Atmakaraka ({ak['planet']}) and Darakaraka ({dk['planet']}) in kendra — strong marital bond",
                "description_hi": f"आत्मकारक ({ak['planet']}) और दारकारक ({dk['planet']}) केंद्र में — मजबूत वैवाहिक बंधन",
                "strength": "Strong",
            })

    # 4. Mahabhagya Yoga (gender-based): check Sun/Moon/Lagna in odd/even signs
    sun_sign = _get_planet_sign(planets, "Sun")
    moon_sign = _get_planet_sign(planets, "Moon")
    sun_odd = _sign_index(sun_sign) % 2 == 0
    moon_odd = _sign_index(moon_sign) % 2 == 0
    asc_odd = _sign_index(asc_sign) % 2 == 0
    if sun_odd and moon_odd and asc_odd:
        yogas.append({
            "name_en": "Mahabhagya Yoga (Male)",
            "name_hi": "महाभाग्य योग (पुरुष)",
            "present": True,
            "description_en": "Sun, Moon, and Lagna all in odd signs — great fortune",
            "description_hi": "सूर्य, चंद्र, और लग्न सभी विषम राशि में — महान भाग्य",
            "strength": "Strong",
        })
    elif not sun_odd and not moon_odd and not asc_odd:
        yogas.append({
            "name_en": "Mahabhagya Yoga (Female)",
            "name_hi": "महाभाग्य योग (स्त्री)",
            "present": True,
            "description_en": "Sun, Moon, and Lagna all in even signs — great fortune",
            "description_hi": "सूर्य, चंद्र, और लग्न सभी सम राशि में — महान भाग्य",
            "strength": "Strong",
        })

    return yogas


# ============================================================
# 8. LONGEVITY CALCULATION
# ============================================================

def calculate_longevity(planets: Dict, ascendant: Dict) -> Dict:
    """
    Jaimini longevity calculation based on 1st and 8th house lords.
    Divides life into: Alpa (short, 0-32), Madhyama (medium, 32-64),
    Purna (long, 64-100), based on sign modality of Lagna & 8th lord.
    """
    asc_sign = ascendant.get("sign", "Aries") if ascendant else "Aries"

    # 8th house sign
    eighth_sign = _sign_at_offset(asc_sign, 8)
    eighth_lord = SIGN_LORD[eighth_sign]
    eighth_lord_sign = _get_planet_sign(planets, eighth_lord)

    # Classify signs by modality
    def _modality(sign: str) -> str:
        if sign in CARDINAL:
            return "Cardinal"
        elif sign in FIXED:
            return "Fixed"
        return "Dual"

    lagna_mod = _modality(asc_sign)
    eighth_mod = _modality(eighth_lord_sign)

    # Jaimini longevity matrix:
    # Cardinal + Cardinal = Purna (Long)
    # Fixed + Fixed = Alpa (Short)
    # Dual + Dual = Madhyama (Medium)
    # Cardinal + Fixed = Madhyama
    # Cardinal + Dual = Alpa
    # Fixed + Dual = Purna
    LONGEVITY_MATRIX = {
        ("Cardinal", "Cardinal"): ("Purna", "Long Life (64-100 years)", "दीर्घ आयु (64-100 वर्ष)"),
        ("Fixed", "Fixed"): ("Alpa", "Short Life (0-32 years)", "अल्प आयु (0-32 वर्ष)"),
        ("Dual", "Dual"): ("Madhyama", "Medium Life (32-64 years)", "मध्यम आयु (32-64 वर्ष)"),
        ("Cardinal", "Fixed"): ("Madhyama", "Medium Life (32-64 years)", "मध्यम आयु (32-64 वर्ष)"),
        ("Fixed", "Cardinal"): ("Madhyama", "Medium Life (32-64 years)", "मध्यम आयु (32-64 वर्ष)"),
        ("Cardinal", "Dual"): ("Alpa", "Short Life (0-32 years)", "अल्प आयु (0-32 वर्ष)"),
        ("Dual", "Cardinal"): ("Alpa", "Short Life (0-32 years)", "अल्प आयु (0-32 वर्ष)"),
        ("Fixed", "Dual"): ("Purna", "Long Life (64-100 years)", "दीर्घ आयु (64-100 वर्ष)"),
        ("Dual", "Fixed"): ("Purna", "Long Life (64-100 years)", "दीर्घ आयु (64-100 वर्ष)"),
    }

    key = (lagna_mod, eighth_mod)
    category, desc_en, desc_hi = LONGEVITY_MATRIX.get(key, ("Madhyama", "Medium Life", "मध्यम आयु"))

    return {
        "category": category,
        "description_en": desc_en,
        "description_hi": desc_hi,
        "lagna_sign": asc_sign,
        "lagna_modality": lagna_mod,
        "eighth_lord": eighth_lord,
        "eighth_lord_sign": eighth_lord_sign,
        "eighth_modality": eighth_mod,
        "note_en": "This is an indicative calculation. Multiple factors including Saturn, 8th house occupants, and dasha periods should be considered.",
        "note_hi": "यह एक सांकेतिक गणना है। शनि, अष्टम भाव के ग्रह, और दशा काल सहित कई कारकों पर विचार करना चाहिए।",
    }


# ============================================================
# MASTER FUNCTION
# ============================================================

def calculate_jaimini(chart_data: Dict, birth_date: str = "") -> Dict:
    """Calculate all Jaimini components from chart data."""
    planets = chart_data.get("planets", {})
    ascendant = chart_data.get("ascendant", {})

    return {
        "chara_karakas": calculate_chara_karakas(planets),
        "special_lagnas": calculate_special_lagnas(planets, ascendant),
        "jaimini_drishti": calculate_jaimini_drishti(),
        "chara_dasha": calculate_chara_dasha(planets, ascendant, birth_date),
        "indu_lagna": calculate_indu_lagna(planets, ascendant),
        "argala": calculate_argala(planets, ascendant),
        "jaimini_yogas": calculate_jaimini_yogas(planets, ascendant),
        "longevity": calculate_longevity(planets, ascendant),
    }
