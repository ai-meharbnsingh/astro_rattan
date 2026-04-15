from datetime import datetime, timedelta, timezone

YOGINI_YEARS = {
    "Mangala": 1,
    "Pingala": 2,
    "Dhanya": 3,
    "Bhramari": 4,
    "Bhadrika": 5,
    "Ulka": 6,
    "Siddha": 7,
    "Sankata": 8
}

YOGINI_ORDER = [
    "Mangala",
    "Pingala",
    "Dhanya",
    "Bhramari",
    "Bhadrika",
    "Ulka",
    "Siddha",
    "Sankata"
]

NAKSHATRA_ORDER = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
    "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

YOGINI_TOTAL = 36 # Years

def get_starting_yogini(nakshatra_name: str) -> str:
    try:
        nak_num = NAKSHATRA_ORDER.index(nakshatra_name) + 1
    except ValueError:
        return "Mangala"
    
    idx = (nak_num + 3) % 8
    # If 0, it means the 8th item (Sankata), so we use idx=8 conceptually, but array is 0-indexed
    # Let's map remainder to 0-7 index in YOGINI_ORDER.
    # Remainder 1 = Mangala (index 0)
    # Remainder 2 = Pingala (index 1)
    # ...
    # Remainder 0 = Sankata (index 7)
    if idx == 0:
        return "Sankata"
    
    return YOGINI_ORDER[idx - 1]

def calculate_yogini_dasha(birth_nakshatra: str, birth_date: str, moon_longitude: float) -> dict:
    """
    Calculate Yogini Dasha periods. Returns periods for up to 108 years (3 cycles).
    """
    start_yogini = get_starting_yogini(birth_nakshatra)
    start_idx = YOGINI_ORDER.index(start_yogini)
    
    nak_index = NAKSHATRA_ORDER.index(birth_nakshatra)
    nak_start = nak_index * (13 + 20.0 / 60.0)
    traversed = moon_longitude - nak_start
    if traversed < 0:
        traversed += 360.0
    sp = 13 + 20.0 / 60.0
    if traversed > sp:
        traversed = sp
    
    remaining_fraction = (sp - traversed) / sp
    balance = max(0.0, min(1.0, remaining_fraction))

    birth_dt = datetime.strptime(birth_date, "%Y-%m-%d")
    now = datetime.utcnow()
    
    periods = []
    
    current_start = birth_dt
    
    # Generate 3 cycles (~108 years)
    for cycle in range(3):
        for i in range(8):
            curr_idx = (start_idx + i) % 8
            planet = YOGINI_ORDER[curr_idx]
            full_years = YOGINI_YEARS[planet]
            
            if cycle == 0 and i == 0:
                effective_years = full_years * balance
            else:
                effective_years = full_years
                
            end_dt = current_start + timedelta(days=effective_years * 365.25)
            
            is_current = current_start <= now <= end_dt
            
            periods.append({
                "planet": planet,
                "start": current_start.strftime("%Y-%m-%d"),
                "end": end_dt.strftime("%Y-%m-%d"),
                "years": round(effective_years, 2),
                "is_current": is_current
            })
            
            current_start = end_dt
            
    current_dasha = "Unknown"
    for p in periods:
        if p["is_current"]:
            current_dasha = p["planet"]
            break
            
    return {
        "periods": periods,
        "current_dasha": current_dasha
    }
