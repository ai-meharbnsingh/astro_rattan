"""
yoga_search_engine.py — Yoga Search Across Kundli Database
============================================================
Searches stored kundlis for specific yoga combinations.
Pro astrologer research tool.

Reuses the canonical yoga detection from dosha_engine.analyze_yogas_and_doshas()
so results are always consistent with individual kundli yoga analysis.
"""
from __future__ import annotations
from typing import Dict, List, Any, Optional
import json
import logging

from app.dosha_engine import analyze_yogas_and_doshas
from app.yoga_rule_engine import detect_all_yogas as _detect_declarative_yogas, load_yoga_rules

logger = logging.getLogger(__name__)

# ── All yoga keys that analyze_yogas_and_doshas can detect ───────────────────
# Names here match the "name" field returned by each check_* function.
# Callers can search by any substring/prefix; we normalise for matching.
YOGA_TYPES = [
    # Panch Mahapurusha (5)
    "Ruchaka Yoga",
    "Bhadra Yoga",
    "Hamsa Yoga",
    "Malavya Yoga",
    "Shasha Yoga",
    # Moon-based
    "Gajakesari Yoga",
    "Sunapha Yoga",
    "Anapha Yoga",
    "Durudhara Yoga",
    "Shakata Yoga",
    "Adhi Yoga",
    "Amala Yoga",
    "Chandra-Mangal Yoga",
    # Sun-based
    "Budhaditya Yoga",
    "Vesi Yoga",
    "Vasi Yoga",
    "Ubhayachari Yoga",
    "Surya in Swa Rashi (Sun in Own Sign)",
    "Shani Uchcha (Saturn Exalted)",
    # Raja Yogas
    "Neecha Bhanga Raj Yoga",
    "Harsha Viparita Raja Yoga",
    "Sarala Viparita Raja Yoga",
    "Vimala Viparita Raja Yoga",
    "Parashari Raja Yoga",
    "Lakshmi Yoga",
    "Dhana Yoga",
    # Special
    "Saraswati Yoga",
    "Danda Yoga",
]

# Extend with all declarative yoga names so search resolves them too
try:
    for _y in load_yoga_rules():
        _name = _y.get("name_en", "")
        if _name and _name not in YOGA_TYPES:
            YOGA_TYPES.append(_name)
except Exception:
    pass  # don't break existing behavior if JSON load fails

# Lowercase lookup set for quick matching
_YOGA_LOWER = {y.lower() for y in YOGA_TYPES}

# Normalised key -> display name for fuzzy search
_YOGA_SLUG_MAP: Dict[str, str] = {}
for _y in YOGA_TYPES:
    _slug = _y.lower().replace("-", " ").replace("(", "").replace(")", "").strip()
    _YOGA_SLUG_MAP[_slug] = _y
    # Also index without " yoga" suffix
    if _slug.endswith(" yoga"):
        _YOGA_SLUG_MAP[_slug[:-5].strip()] = _y


def _normalise_query(q: str) -> str:
    """Lowercase and strip common suffixes for flexible matching."""
    return q.lower().replace("-", " ").replace("_", " ").strip()


def resolve_yoga_name(query: str) -> Optional[str]:
    """Resolve a user query to an exact yoga display name.

    Supports partial matching: "gajakesari", "Gajakesari Yoga", "ruchaka", etc.
    Returns None if no match.
    """
    norm = _normalise_query(query)
    # Exact hit
    if norm in _YOGA_SLUG_MAP:
        return _YOGA_SLUG_MAP[norm]
    # Substring search
    for slug, display in _YOGA_SLUG_MAP.items():
        if norm in slug or slug in norm:
            return display
    return None


def detect_yogas_in_chart(chart_data: dict) -> List[Dict[str, Any]]:
    """
    Run full yoga detection on a parsed chart_data dict.

    Merges legacy dosha_engine yoga detection (~34 yogas) with declarative
    yoga_rule_engine detection (~50 additional yogas from JSON).

    Returns list of *present* yogas, each as
    ``{name, description, planets_involved, category, sloka_ref, nature}``.
    """
    planets = chart_data.get("planets", {})
    asc_sign = chart_data.get("ascendant", {}).get("sign", "")

    result = analyze_yogas_and_doshas(planets, asc_sign)
    present: List[Dict[str, Any]] = []
    seen_keys: set = set()
    for y in result.get("yogas", []):
        if y.get("present"):
            key = (y["name"] or "").strip().lower()
            if key in seen_keys:
                continue
            seen_keys.add(key)
            present.append({
                "name": y["name"],
                "description": y.get("description", ""),
                "planets_involved": y.get("planets_involved", []),
                "category": y.get("category", "classical"),
                "sloka_ref": y.get("sloka_ref", ""),
                "nature": y.get("nature", "mixed"),
            })

    # Merge declarative (data-driven) yogas
    for d in _detect_declarative_yogas(chart_data):
        key = (d.get("name_en") or "").strip().lower()
        if key in seen_keys:
            continue
        seen_keys.add(key)
        present.append({
            "name": d.get("name_en", ""),
            "name_hi": d.get("name_hi", ""),
            "description": d.get("effect_en", ""),
            "description_hi": d.get("effect_hi", ""),
            "planets_involved": [],
            "category": d.get("category", ""),
            "category_label_en": d.get("category_label_en", ""),
            "category_label_hi": d.get("category_label_hi", ""),
            "sloka_ref": d.get("sloka_ref", ""),
            "nature": d.get("nature", "mixed"),
        })

    return present


def search_yogas_in_chart(chart_data: dict) -> List[str]:
    """
    Given chart_data (planets dict from DB), detect which yogas are present.
    Uses the canonical dosha_engine logic. Returns just the yoga names.
    """
    return [y["name"] for y in detect_yogas_in_chart(chart_data)]


# ─── Database search functions ───────────────────────────────────────────────

def search_kundlis_for_yoga(
    db,
    yoga_name: str,
    user_id: str,
    limit: int = 50,
    offset: int = 0,
) -> Dict[str, Any]:
    """
    Search all kundlis owned by *user_id* for a specific yoga.

    Args:
        db: PgConnection from get_db().
        yoga_name: The yoga to search for (flexible: "gajakesari", "Ruchaka Yoga", etc.).
        user_id: Owner of the kundlis (auth-scoped).
        limit: Max results to return.
        offset: Pagination offset.

    Returns:
        {yoga: str, total_scanned: int, total_matches: int, matches: [...]}
    """
    resolved = resolve_yoga_name(yoga_name)
    if resolved is None:
        return {
            "yoga": yoga_name,
            "resolved_yoga": None,
            "total_scanned": 0,
            "total_matches": 0,
            "matches": [],
            "error": f"Unknown yoga '{yoga_name}'. Use GET /api/yoga-search/types for valid names.",
        }

    # Fetch all kundlis for this user
    rows = db.execute(
        "SELECT id, person_name, birth_date, birth_time, birth_place, chart_data "
        "FROM kundlis WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()

    matches = []
    for row in rows:
        row = dict(row)
        try:
            chart_data = json.loads(row["chart_data"])
        except (json.JSONDecodeError, TypeError):
            continue

        present_yogas = detect_yogas_in_chart(chart_data)
        # Check if the searched yoga is among present ones
        matched_yoga = None
        for y in present_yogas:
            if y["name"] == resolved:
                matched_yoga = y
                break

        if matched_yoga:
            matches.append({
                "kundli_id": row["id"],
                "person_name": row["person_name"],
                "birth_date": row.get("birth_date", ""),
                "birth_time": row.get("birth_time", ""),
                "birth_place": row.get("birth_place", ""),
                "yoga": matched_yoga,
                "all_yogas": [y["name"] for y in present_yogas],
            })

    total_matches = len(matches)
    # Apply pagination
    paginated = matches[offset: offset + limit]

    return {
        "yoga": resolved,
        "total_scanned": len(rows),
        "total_matches": total_matches,
        "offset": offset,
        "limit": limit,
        "matches": paginated,
    }


def get_yoga_statistics(
    db,
    user_id: str,
) -> Dict[str, Any]:
    """
    Get statistics on yoga prevalence across all stored kundlis for a user.

    Returns count and percentage for each yoga type.
    """
    rows = db.execute(
        "SELECT id, person_name, chart_data FROM kundlis WHERE user_id = %s",
        (user_id,),
    ).fetchall()

    total = len(rows)
    if total == 0:
        return {
            "total_kundlis": 0,
            "yoga_counts": {},
            "yoga_percentages": {},
            "most_common": [],
            "rarest": [],
        }

    # Count occurrences of each yoga
    yoga_counts: Dict[str, int] = {}
    for row in rows:
        row = dict(row)
        try:
            chart_data = json.loads(row["chart_data"])
        except (json.JSONDecodeError, TypeError):
            continue

        present_names = search_yogas_in_chart(chart_data)
        for name in present_names:
            yoga_counts[name] = yoga_counts.get(name, 0) + 1

    # Calculate percentages
    yoga_percentages = {
        name: round(count / total * 100, 1)
        for name, count in yoga_counts.items()
    }

    # Sort by count descending
    sorted_yogas = sorted(yoga_counts.items(), key=lambda x: x[1], reverse=True)
    most_common = [
        {"yoga": name, "count": count, "percentage": yoga_percentages[name]}
        for name, count in sorted_yogas[:10]
    ]
    rarest = [
        {"yoga": name, "count": count, "percentage": yoga_percentages[name]}
        for name, count in sorted_yogas[-5:]
    ] if len(sorted_yogas) > 5 else []

    return {
        "total_kundlis": total,
        "yoga_counts": yoga_counts,
        "yoga_percentages": yoga_percentages,
        "most_common": most_common,
        "rarest": rarest,
    }


def get_kundli_yoga_profile(
    db,
    kundli_id: str,
    user_id: str,
) -> Dict[str, Any]:
    """
    Get full yoga profile for a single kundli. Useful as a detail view
    after finding a match via search.
    """
    row = db.execute(
        "SELECT id, person_name, birth_date, birth_time, birth_place, chart_data "
        "FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user_id),
    ).fetchone()

    if not row:
        return {"error": "Kundli not found"}

    row = dict(row)
    try:
        chart_data = json.loads(row["chart_data"])
    except (json.JSONDecodeError, TypeError):
        return {"error": "Invalid chart data"}

    present_yogas = detect_yogas_in_chart(chart_data)
    return {
        "kundli_id": row["id"],
        "person_name": row["person_name"],
        "birth_date": row.get("birth_date", ""),
        "birth_time": row.get("birth_time", ""),
        "birth_place": row.get("birth_place", ""),
        "total_yogas": len(present_yogas),
        "yogas": present_yogas,
    }
