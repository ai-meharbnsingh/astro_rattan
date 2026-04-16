"""Ekadashi Parana (एकादशी पारण) calculation."""
from typing import Any, Dict, Optional


def _time_to_minutes(time_str: str) -> float:
    parts = time_str.split(":")
    return int(parts[0]) * 60 + int(parts[1])


def _minutes_to_time(minutes: float) -> str:
    minutes = minutes % 1440
    h = int(minutes // 60)
    m = int(minutes % 60)
    return f"{h:02d}:{m:02d}"


def calculate_ekadashi_parana(
    tithi_name: str,
    tithi_end_time: str = "",
    next_sunrise: str = "05:54",
    next_tithi_name: str = "",
) -> Optional[Dict[str, Any]]:
    """
    Calculate Ekadashi Parana (fast-breaking) time.

    Parana is done the morning after Ekadashi, between sunrise and
    the first 1/3 of daytime (~4 hours after sunrise).

    Returns None if not an Ekadashi day.
    """
    if "ekadashi" not in tithi_name.lower():
        return None

    sunrise_mins = _time_to_minutes(next_sunrise)
    parana_end_mins = sunrise_mins + 240  # ~4 hours (1/3 of 12h day)

    # Parana starts at sunrise by default
    parana_start_mins = sunrise_mins

    # If Dwadashi hasn't started at sunrise (tithi_end_time is after sunrise),
    # parana must wait for Dwadashi to begin
    note = ""
    note_hindi = ""
    if tithi_end_time:
        tithi_end_mins = _time_to_minutes(tithi_end_time)
        if tithi_end_mins > sunrise_mins:
            parana_start_mins = tithi_end_mins
            note = f"Wait for Dwadashi to begin at {tithi_end_time}"
            note_hindi = f"द्वादशी प्रारम्भ {tithi_end_time} तक प्रतीक्षा करें"

        # If Dwadashi ends before parana window closes, note it
        if tithi_end_mins < parana_end_mins and tithi_end_mins > sunrise_mins:
            if not note:
                note = f"Dwadashi ends at {tithi_end_time}"
                note_hindi = f"द्वादशी {tithi_end_time} पर समाप्त"

    return {
        "name": "Ekadashi Parana",
        "name_hindi": "एकादशी पारण",
        "start": _minutes_to_time(parana_start_mins),
        "end": _minutes_to_time(parana_end_mins),
        "note": note,
        "note_hindi": note_hindi,
    }
