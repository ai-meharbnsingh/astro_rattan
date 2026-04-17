"""
Lal Kitab age activation (backend)

The UI shows age-bucket activation periods (Sun 1-6, Moon 7-12, ...).
This used to be computed on the frontend; we provide it as backend data so
no mock/static timing logic is needed client-side.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List, Optional


AGE_PLANET_ACTIVATION: List[Dict[str, Any]] = [
    {"planet": "Sun", "age_start": 1, "age_end": 6},
    {"planet": "Moon", "age_start": 7, "age_end": 12},
    {"planet": "Mars", "age_start": 13, "age_end": 18},
    {"planet": "Mercury", "age_start": 19, "age_end": 24},
    {"planet": "Jupiter", "age_start": 25, "age_end": 36},
    {"planet": "Venus", "age_start": 37, "age_end": 48},
    {"planet": "Saturn", "age_start": 49, "age_end": 60},
    {"planet": "Rahu", "age_start": 61, "age_end": 72},
    {"planet": "Ketu", "age_start": 73, "age_end": 84},
]


def _age_years(birth_date: str, as_of: Optional[str] = None) -> Optional[int]:
    try:
        bd = datetime.strptime(birth_date, "%Y-%m-%d").date()
    except Exception:
        return None
    if as_of:
        try:
            ad = datetime.strptime(as_of, "%Y-%m-%d").date()
        except Exception:
            ad = date.today()
    else:
        ad = date.today()
    if bd > ad:
        return None
    years = ad.year - bd.year - ((ad.month, ad.day) < (bd.month, bd.day))
    return max(0, int(years))


def get_age_activation(birth_date: str, as_of: Optional[str] = None) -> Dict[str, Any]:
    years = _age_years(birth_date, as_of=as_of)
    active = None
    if years is not None:
        for p in AGE_PLANET_ACTIVATION:
            if years >= p["age_start"] and years <= p["age_end"]:
                active = p
                break
        if active is None and years > AGE_PLANET_ACTIVATION[-1]["age_end"]:
            active = AGE_PLANET_ACTIVATION[-1]
    return {
        "birth_date": birth_date,
        "as_of": as_of or date.today().isoformat(),
        "age_years": years,
        "periods": AGE_PLANET_ACTIVATION,
        "active": active,
    }

