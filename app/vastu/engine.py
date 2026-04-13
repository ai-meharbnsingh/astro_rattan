"""
vastu/engine.py — Vastu Shastra Calculation Engine
====================================================
Core calculations for Vastu Purusha Mandala (45 Devtas),
32 Entrance Padas analysis, and Remedial system.
All calculations based on ancient Vastu Shastra principles.
"""
import math
from typing import Optional

from app.vastu.data import (
    DEVTAS_45,
    DIRECTIONS,
    ENTRANCE_PADAS,
    METAL_REMEDIES,
    COLOR_THERAPY,
    ROOM_PLACEMENT,
    BUILDING_TYPES,
    VASTU_PURUSHA_BODY,
)


# ============================================================
# DIRECTION HELPERS
# ============================================================
def _normalize_degrees(deg: float) -> float:
    """Normalize angle to 0-360 range."""
    return deg % 360


def _degrees_to_direction(degrees: float) -> str:
    """Convert compass degrees to 8-direction code (N, NE, E, etc.)."""
    deg = _normalize_degrees(degrees)
    # 8 sectors of 45 degrees each, starting from N at 0/360
    sectors = [
        (337.5, 360.0, "N"), (0.0, 22.5, "N"),
        (22.5, 67.5, "NE"),
        (67.5, 112.5, "E"),
        (112.5, 157.5, "SE"),
        (157.5, 202.5, "S"),
        (202.5, 247.5, "SW"),
        (247.5, 292.5, "W"),
        (292.5, 337.5, "NW"),
    ]
    for lo, hi, d in sectors:
        if lo <= deg < hi:
            return d
    return "N"


def _direction_to_pada_index(direction: str, degrees: float) -> int:
    """
    Within a direction (N/E/S/W), compute which pada (1-8) the entrance falls in.
    Each direction spans 90 degrees, divided into 8 padas of 11.25 degrees each.

    Ancient method: the 90-degree arc of each cardinal direction is divided
    into 8 equal padas (sub-divisions) of 11.25 degrees each.
    """
    # Each cardinal direction spans 90° of the compass, centered on its axis.
    # N: 315°→45°, E: 45°→135°, S: 135°→225°, W: 225°→315°
    # Pada 1 starts at the counter-clockwise boundary.
    dir_base = {
        "N": 315.0,   # N wall spans 315° (NW corner) → 45° (NE corner)
        "E": 45.0,    # E wall spans 45° → 135°
        "S": 135.0,   # S wall spans 135° → 225°
        "W": 225.0,   # W wall spans 225° → 315°
    }

    if direction not in dir_base:
        return 0

    base = dir_base[direction]
    deg = _normalize_degrees(degrees)

    # Handle N wrapping around 360/0
    if direction == "N":
        if deg >= 315.0:
            offset = deg - 315.0
        else:
            offset = deg + 45.0  # wrap: 0° → offset 45 → N5 (center)
    else:
        offset = deg - base

    if offset < 0:
        offset += 360

    pada_index = int(offset / 11.25)
    return min(pada_index, 7)  # clamp to 0-7


# ============================================================
# MANDALA CALCULATION
# ============================================================
def calculate_mandala(
    building_type: str = "residential",
    entrance_direction: Optional[str] = None,
    entrance_degrees: Optional[float] = None,
) -> dict:
    """
    Calculate the Vastu Purusha Mandala analysis for a building.

    Args:
        building_type: "residential", "commercial", or "temple"
        entrance_direction: optional 2-letter direction code (N, NE, E, etc.)
        entrance_degrees: optional compass degrees of entrance (0-360)

    Returns:
        dict with mandala grid, devtas by zone, body mapping, and energy analysis
    """
    bt = BUILDING_TYPES.get(building_type, BUILDING_TYPES["residential"])
    grid_size = bt["grid_size"]

    # Group devtas by zone
    zones = {}
    for d in DEVTAS_45:
        zone = d["zone"]
        if zone not in zones:
            zones[zone] = {
                "zone_en": zone,
                "zone_hi": d["zone_hi"],
                "devtas": [],
                "positive_count": 0,
                "negative_count": 0,
                "neutral_count": 0,
            }
        zones[zone]["devtas"].append({
            "id": d["id"],
            "name": d["name"],
            "name_hi": d["name_hi"],
            "direction": d["direction"],
            "direction_hi": d["direction_hi"],
            "element": d["element"],
            "element_hi": d["element_hi"],
            "nature": d["nature"],
            "energy_type": d["energy_type"],
            "body_part": d["body_part"],
            "body_part_hi": d["body_part_hi"],
            "mantra": d["mantra"],
            "description_en": d["desc_en"],
            "description_hi": d["desc_hi"],
        })
        if d["nature"] in ("positive", "supreme"):
            zones[zone]["positive_count"] += 1
        elif d["nature"] in ("negative", "fierce"):
            zones[zone]["negative_count"] += 1
        else:
            zones[zone]["neutral_count"] += 1

    # Calculate overall energy balance
    total_positive = sum(z["positive_count"] for z in zones.values())
    total_negative = sum(z["negative_count"] for z in zones.values())
    total_neutral = sum(z["neutral_count"] for z in zones.values())

    # Body mapping
    body_map = {}
    for part, info in VASTU_PURUSHA_BODY.items():
        body_map[part] = {
            "direction": info["direction"],
            "direction_hi": info["direction_hi"],
            "significance_en": info["significance_en"],
            "significance_hi": info["significance_hi"],
        }

    # Entrance analysis if provided
    entrance_info = None
    if entrance_direction or entrance_degrees is not None:
        if entrance_degrees is not None:
            direction = _degrees_to_direction(entrance_degrees)
        else:
            direction = entrance_direction
        entrance_info = analyze_entrance(direction, entrance_degrees)

    return {
        "grid_type": bt["name_en"],
        "grid_type_hi": bt["name_hi"],
        "grid_size": grid_size,
        "total_squares": grid_size * grid_size,
        "building_type": building_type,
        "description_en": bt["desc_en"],
        "description_hi": bt["desc_hi"],
        "zones": zones,
        "body_mapping": body_map,
        "energy_balance": {
            "positive": total_positive,
            "negative": total_negative,
            "neutral": total_neutral,
            "total": len(DEVTAS_45),
            "balance_ratio": round(total_positive / max(total_negative, 1), 2),
            "assessment_en": _energy_assessment(total_positive, total_negative),
            "assessment_hi": _energy_assessment_hi(total_positive, total_negative),
        },
        "entrance_analysis": entrance_info,
    }


def _energy_assessment(positive: int, negative: int) -> str:
    ratio = positive / max(negative, 1)
    if ratio >= 3:
        return "Excellent — strong positive energy dominates the mandala"
    elif ratio >= 2:
        return "Good — positive energy is significantly stronger than negative"
    elif ratio >= 1.5:
        return "Moderate — positive energy leads but remedies recommended for weak zones"
    else:
        return "Needs attention — negative zones require immediate remedial measures"


def _energy_assessment_hi(positive: int, negative: int) -> str:
    ratio = positive / max(negative, 1)
    if ratio >= 3:
        return "उत्कृष्ट — मंडल में मजबूत सकारात्मक ऊर्जा का प्रभुत्व"
    elif ratio >= 2:
        return "अच्छा — सकारात्मक ऊर्जा नकारात्मक से काफी मजबूत"
    elif ratio >= 1.5:
        return "मध्यम — सकारात्मक ऊर्जा आगे है लेकिन कमजोर क्षेत्रों के लिए उपाय आवश्यक"
    else:
        return "ध्यान आवश्यक — नकारात्मक क्षेत्रों के लिए तुरंत उपायों की आवश्यकता"


# ============================================================
# ENTRANCE ANALYSIS
# ============================================================
def analyze_entrance(
    direction: str,
    degrees: Optional[float] = None,
) -> dict:
    """
    Analyze entrance direction against the 32 pada system.

    Args:
        direction: compass direction code — N, NE, E, SE, S, SW, W, NW,
                   or specific pada like "N3", "E5"
        degrees:   optional precise compass degrees (0-360)

    Returns:
        dict with pada details, quality score, effects, and recommendations
    """
    # If user provides a pada code directly (e.g. "N3")
    if len(direction) >= 2 and direction[0] in "NESW" and direction[-1].isdigit():
        pada_code = direction.upper()
        matching = [p for p in ENTRANCE_PADAS if p["pada"] == pada_code]
        if matching:
            pada = matching[0]
            return _build_entrance_result(pada, degrees)

    # Map direction to cardinal (only N/E/S/W have padas)
    cardinal = direction[0] if direction in ("NE", "NW", "SE", "SW") else direction
    if cardinal not in ("N", "E", "S", "W"):
        # For intercardinals, pick the nearest cardinal
        mapping = {"NE": "N", "NW": "N", "SE": "E", "SW": "S"}
        cardinal = mapping.get(direction, "N")

    # Find pada index from degrees
    if degrees is not None:
        idx = _direction_to_pada_index(cardinal, degrees)
    else:
        idx = 0  # default to first pada

    pada_code = f"{cardinal}{idx + 1}"
    matching = [p for p in ENTRANCE_PADAS if p["pada"] == pada_code]
    if not matching:
        # Fallback: get all padas for the direction, pick first
        matching = [p for p in ENTRANCE_PADAS if p["direction"] == cardinal]
        if matching:
            pada = matching[0]
        else:
            return {"error": f"No pada data for direction {direction}"}
    else:
        pada = matching[0]

    return _build_entrance_result(pada, degrees)


def _build_entrance_result(pada: dict, degrees: Optional[float]) -> dict:
    """Build the full entrance analysis result from a pada record."""
    # Find the ruling devta details
    ruling_devta = None
    for d in DEVTAS_45:
        if d["name"] == pada["devta"]:
            ruling_devta = {
                "name": d["name"],
                "name_hi": d["name_hi"],
                "zone": d["zone"],
                "zone_hi": d["zone_hi"],
                "energy_type": d["energy_type"],
                "mantra": d["mantra"],
                "description_en": d["desc_en"],
                "description_hi": d["desc_hi"],
            }
            break

    # Get all padas for this direction for comparison
    dir_padas = [p for p in ENTRANCE_PADAS if p["direction"] == pada["direction"]]
    best_pada = max(dir_padas, key=lambda x: x["score"])
    worst_pada = min(dir_padas, key=lambda x: x["score"])

    # Generate remedies if entrance is challenging
    entrance_remedies = []
    if pada["score"] <= 2:
        entrance_remedies = _generate_entrance_remedies(pada)

    return {
        "pada": pada["pada"],
        "pada_name": pada["name"],
        "pada_name_hi": pada["name_hi"],
        "direction": pada["direction"],
        "direction_info": DIRECTIONS.get(pada["direction"], {}),
        "quality": pada["quality"],
        "quality_hi": pada["quality_hi"],
        "score": pada["score"],
        "score_max": 5,
        "degrees": degrees,
        "effects_en": pada["effects_en"],
        "effects_hi": pada["effects_hi"],
        "suitable_for": pada["suitable"],
        "avoid_for": pada["avoid"],
        "ruling_devta": ruling_devta,
        "best_pada_in_direction": {
            "pada": best_pada["pada"],
            "name": best_pada["name"],
            "name_hi": best_pada["name_hi"],
            "score": best_pada["score"],
        },
        "worst_pada_in_direction": {
            "pada": worst_pada["pada"],
            "name": worst_pada["name"],
            "name_hi": worst_pada["name_hi"],
            "score": worst_pada["score"],
        },
        "all_padas_in_direction": [
            {"pada": p["pada"], "name": p["name"], "name_hi": p["name_hi"],
             "quality": p["quality"], "quality_hi": p["quality_hi"], "score": p["score"]}
            for p in dir_padas
        ],
        "remedies": entrance_remedies,
    }


def _generate_entrance_remedies(pada: dict) -> list:
    """Generate remedies for a challenging entrance pada."""
    remedies = []
    direction = pada["direction"]

    # Metal strip remedy
    metal = METAL_REMEDIES.get(direction)
    if metal:
        remedies.append({
            "type": "metal_strip",
            "type_hi": "धातु पट्टी",
            "remedy_en": f"Place a {metal['metal']} strip at the entrance threshold to neutralize negative energy",
            "remedy_hi": f"नकारात्मक ऊर्जा को निष्प्रभावित करने के लिए प्रवेश द्वार की दहलीज पर {metal['metal_hi']} की पट्टी रखें",
            "metal": metal["metal"],
            "metal_hi": metal["metal_hi"],
        })

    # Color remedy
    colors = COLOR_THERAPY.get(direction)
    if colors:
        color_str = ", ".join(colors["colors"])
        color_str_hi = ", ".join(colors["colors_hi"])
        remedies.append({
            "type": "color_therapy",
            "type_hi": "रंग चिकित्सा",
            "remedy_en": f"Paint the entrance area in {color_str} colors to harmonize the energy",
            "remedy_hi": f"ऊर्जा को सामंजस्यपूर्ण बनाने के लिए प्रवेश क्षेत्र को {color_str_hi} रंगों में रंगें",
            "colors": colors["colors"],
            "colors_hi": colors["colors_hi"],
        })

    # Mantra remedy based on devta
    for d in DEVTAS_45:
        if d["name"] == pada["devta"]:
            remedies.append({
                "type": "mantra",
                "type_hi": "मंत्र",
                "remedy_en": f"Chant '{d['mantra']}' 108 times daily at the entrance to appease {d['name']}",
                "remedy_hi": f"प्रवेश द्वार पर प्रतिदिन '{d['mantra']}' का 108 बार जाप करें",
                "mantra": d["mantra"],
                "devta": d["name"],
                "devta_hi": d["name_hi"],
            })
            break

    # Universal entrance remedies for bad padas
    remedies.extend([
        {
            "type": "yantra",
            "type_hi": "यंत्र",
            "remedy_en": "Install a Vastu Dosh Nivaran Yantra at the entrance to deflect negative energy",
            "remedy_hi": "नकारात्मक ऊर्जा को विचलित करने के लिए प्रवेश द्वार पर वास्तु दोष निवारण यंत्र स्थापित करें",
        },
        {
            "type": "salt_water",
            "type_hi": "नमक-जल",
            "remedy_en": "Keep a bowl of rock salt dissolved in water near the entrance, change weekly",
            "remedy_hi": "प्रवेश द्वार के पास पानी में सेंधा नमक घोलकर एक कटोरा रखें, साप्ताहिक बदलें",
        },
    ])

    return remedies


# ============================================================
# REMEDIES CALCULATOR
# ============================================================
def suggest_remedies(
    problems: list[str],
    building_type: str = "residential",
    entrance_direction: Optional[str] = None,
) -> dict:
    """
    Suggest Vastu remedies based on reported problems.

    Args:
        problems: list of problem keywords — "wealth", "health", "relationship",
                  "career", "education", "legal", "sleep", "conflict"
        building_type: "residential", "commercial", or "temple"
        entrance_direction: optional entrance direction for entrance-specific remedies

    Returns:
        dict with metal_strips, color_therapy, room_adjustments, mantras, and general remedies
    """
    result = {
        "problems_analyzed": problems,
        "building_type": building_type,
        "metal_strip_remedies": [],
        "color_therapy": [],
        "room_adjustments": [],
        "mantras": [],
        "general_remedies": [],
    }

    # Problem → direction mapping (which zone to fix)
    problem_zones = {
        "wealth":       ["N", "NE"],
        "health":       ["NE", "E", "Center"],
        "relationship": ["SW", "NW"],
        "career":       ["N", "E"],
        "education":    ["NE", "E", "NW"],
        "legal":        ["S", "W"],
        "sleep":        ["SW", "S"],
        "conflict":     ["SE", "SW"],
        "fertility":    ["NE", "N"],
        "depression":   ["NE", "E"],
        "debt":         ["N", "NW", "SE"],
        "accident":     ["S", "SW"],
    }

    # Problem → devta mapping (which devta to appease)
    problem_devtas = {
        "wealth":       ["Kubera", "Aditi"],
        "health":       ["Surya", "Brahma", "Agni"],
        "relationship": ["Mitra", "Soma", "Gandharva"],
        "career":       ["Indra", "Mukhya", "Jayant"],
        "education":    ["Aditi", "Savita", "Jayant"],
        "legal":        ["Yama", "Satya", "Varuna"],
        "sleep":        ["Soma", "Rudra"],
        "conflict":     ["Mitra", "Aryama", "Brahma"],
        "fertility":    ["Parjanya", "Aditi", "Pushan"],
        "depression":   ["Surya", "Savita", "Shikhi"],
        "debt":         ["Kubera", "Naga", "Agni"],
        "accident":     ["Yama", "Rudra", "Dauvarika"],
    }

    zones_to_fix = set()
    devtas_to_appease = set()

    for prob in problems:
        prob_lower = prob.lower().strip()
        if prob_lower in problem_zones:
            zones_to_fix.update(problem_zones[prob_lower])
        if prob_lower in problem_devtas:
            devtas_to_appease.update(problem_devtas[prob_lower])

    # If no recognized problems, suggest general audit
    if not zones_to_fix:
        zones_to_fix = {"N", "NE", "E", "SE", "S", "SW", "W", "NW"}

    # Metal strip remedies for affected zones
    for zone in sorted(zones_to_fix):
        metal = METAL_REMEDIES.get(zone)
        if metal:
            result["metal_strip_remedies"].append({
                "direction": zone,
                "direction_en": DIRECTIONS[zone]["en"] if zone in DIRECTIONS else zone,
                "direction_hi": DIRECTIONS[zone]["hi"] if zone in DIRECTIONS else zone,
                "metal": metal["metal"],
                "metal_hi": metal["metal_hi"],
                "purpose_en": metal["purpose_en"],
                "purpose_hi": metal["purpose_hi"],
                "placement_en": metal["placement"],
                "placement_hi": metal["placement_hi"],
            })

    # Color therapy for affected zones
    for zone in sorted(zones_to_fix):
        colors = COLOR_THERAPY.get(zone)
        if colors:
            result["color_therapy"].append({
                "direction": zone,
                "direction_en": DIRECTIONS[zone]["en"] if zone in DIRECTIONS else zone,
                "direction_hi": DIRECTIONS[zone]["hi"] if zone in DIRECTIONS else zone,
                "colors": colors["colors"],
                "colors_hi": colors["colors_hi"],
                "element": colors["element"],
                "reasoning_en": colors["reasoning_en"],
                "reasoning_hi": colors["reasoning_hi"],
            })

    # Room adjustments based on problems
    room_recs = _room_recommendations_for_problems(problems)
    result["room_adjustments"] = room_recs

    # Mantras for specific devtas
    for devta_name in sorted(devtas_to_appease):
        for d in DEVTAS_45:
            if d["name"] == devta_name:
                result["mantras"].append({
                    "devta": d["name"],
                    "devta_hi": d["name_hi"],
                    "mantra": d["mantra"],
                    "zone": d["zone"],
                    "zone_hi": d["zone_hi"],
                    "purpose_en": f"Appease {d['name']} — {d['energy_type']} energy for resolving related issues",
                    "purpose_hi": f"{d['name_hi']} को प्रसन्न करें — संबंधित समस्याओं के समाधान के लिए {d['energy_type']} ऊर्जा",
                    "method_en": f"Chant '{d['mantra']}' 108 times daily, facing {d['direction']}",
                    "method_hi": f"प्रतिदिन '{d['mantra']}' का 108 बार जाप करें, {d['direction_hi']} की ओर मुख करके",
                })
                break  # one entry per devta

    # General remedies
    result["general_remedies"] = _general_remedies_for_problems(problems)

    # Entrance-specific remedies
    if entrance_direction:
        entrance_analysis = analyze_entrance(entrance_direction)
        if entrance_analysis.get("remedies"):
            result["entrance_remedies"] = entrance_analysis["remedies"]

    return result


def _room_recommendations_for_problems(problems: list[str]) -> list:
    """Map problems to room placement adjustments."""
    recs = []
    problem_room_map = {
        "health":       ["pooja", "kitchen", "master_bedroom"],
        "wealth":       ["pooja", "study_room"],
        "relationship": ["master_bedroom", "living_room"],
        "career":       ["study_room"],
        "education":    ["study_room", "children_bedroom"],
        "sleep":        ["master_bedroom", "children_bedroom"],
        "conflict":     ["living_room", "kitchen"],
        "fertility":    ["master_bedroom", "pooja"],
    }

    seen_rooms = set()
    for prob in problems:
        prob_lower = prob.lower().strip()
        rooms = problem_room_map.get(prob_lower, [])
        for room_key in rooms:
            if room_key in seen_rooms:
                continue
            seen_rooms.add(room_key)
            room = ROOM_PLACEMENT.get(room_key)
            if room:
                ideal_str = ", ".join(room["ideal"])
                ideal_str_hi = ", ".join(room["ideal_hi"])
                avoid_str = ", ".join(room["avoid"]) if room["avoid"] else "None"
                avoid_str_hi = ", ".join(room["avoid_hi"]) if room["avoid_hi"] else "कोई नहीं"
                recs.append({
                    "room": room_key,
                    "room_name_en": room["name_en"],
                    "room_name_hi": room["name_hi"],
                    "ideal_directions": room["ideal"],
                    "ideal_directions_hi": room["ideal_hi"],
                    "avoid_directions": room["avoid"],
                    "avoid_directions_hi": room["avoid_hi"],
                    "reason_en": room["reason_en"],
                    "reason_hi": room["reason_hi"],
                    "tips_en": room["tips_en"],
                    "tips_hi": room["tips_hi"],
                    "recommendation_en": f"Place {room['name_en']} in {ideal_str} direction. Avoid: {avoid_str}.",
                    "recommendation_hi": f"{room['name_hi']} को {ideal_str_hi} दिशा में रखें। बचें: {avoid_str_hi}।",
                })
    return recs


def _general_remedies_for_problems(problems: list[str]) -> list:
    """Return universal Vastu remedies applicable to reported problems."""
    remedies = []

    for prob in problems:
        p = prob.lower().strip()
        if p == "wealth":
            remedies.extend([
                {"remedy_en": "Place a Kuber Yantra in the North zone of the house", "remedy_hi": "घर के उत्तर क्षेत्र में कुबेर यंत्र रखें", "category": "yantra"},
                {"remedy_en": "Keep cash locker in North wall, opening towards North", "remedy_hi": "तिजोरी उत्तर दीवार पर रखें, उत्तर की ओर खुलने वाली", "category": "placement"},
                {"remedy_en": "Place a fountain or aquarium in North or Northeast", "remedy_hi": "उत्तर या ईशान में फव्वारा या एक्वेरियम रखें", "category": "water_element"},
                {"remedy_en": "Ensure Northeast corner is lowest, cleanest, and most open", "remedy_hi": "सुनिश्चित करें कि ईशान कोना सबसे नीचा, स्वच्छ और खुला हो", "category": "structural"},
            ])
        elif p == "health":
            remedies.extend([
                {"remedy_en": "Ensure morning sunlight enters from the East windows", "remedy_hi": "सुनिश्चित करें कि प्रातःकालीन सूर्य प्रकाश पूर्वी खिड़कियों से प्रवेश करे", "category": "light"},
                {"remedy_en": "Remove clutter from Northeast zone — blocked NE causes health issues", "remedy_hi": "ईशान क्षेत्र से अव्यवस्था हटाएँ — अवरुद्ध ईशान स्वास्थ्य समस्याएँ उत्पन्न करता है", "category": "declutter"},
                {"remedy_en": "Place a copper vessel with water in the East zone", "remedy_hi": "पूर्व क्षेत्र में पानी भरा ताँबे का बर्तन रखें", "category": "metal"},
                {"remedy_en": "Kitchen must be in Southeast — fire element in wrong zone disturbs digestion", "remedy_hi": "रसोई आग्नेय में होनी चाहिए — गलत क्षेत्र में अग्नि तत्व पाचन बिगाड़ता है", "category": "placement"},
            ])
        elif p == "relationship":
            remedies.extend([
                {"remedy_en": "Place paired items (paired candles, paired figurines) in Southwest bedroom", "remedy_hi": "नैऋत्य शयनकक्ष में जोड़ीदार वस्तुएँ (जोड़ी मोमबत्ती, जोड़ी मूर्तियाँ) रखें", "category": "symbolic"},
                {"remedy_en": "Remove cacti, thorny plants, and single-person artwork from bedroom", "remedy_hi": "शयनकक्ष से कैक्टस, काँटेदार पौधे और एकल-व्यक्ति कलाकृति हटाएँ", "category": "declutter"},
                {"remedy_en": "Use rose quartz or pink/cream colors in Southwest zone", "remedy_hi": "नैऋत्य क्षेत्र में गुलाबी क्वार्ट्ज़ या गुलाबी/क्रीम रंग उपयोग करें", "category": "color"},
                {"remedy_en": "Ensure no toilet or kitchen wall is shared with master bedroom", "remedy_hi": "सुनिश्चित करें कि मुख्य शयनकक्ष की दीवार शौचालय या रसोई से साझा न हो", "category": "structural"},
            ])
        elif p == "career":
            remedies.extend([
                {"remedy_en": "Sit facing North or East while working — aligns with Kubera and Indra energy", "remedy_hi": "काम करते समय उत्तर या पूर्व की ओर मुख करके बैठें — कुबेर और इन्द्र ऊर्जा से संरेखित", "category": "placement"},
                {"remedy_en": "Place a brass pyramid in the North zone of your workspace", "remedy_hi": "अपने कार्यक्षेत्र के उत्तर क्षेत्र में पीतल का पिरामिड रखें", "category": "yantra"},
                {"remedy_en": "Keep the entrance well-lit and clutter-free", "remedy_hi": "प्रवेश द्वार को अच्छी तरह प्रकाशित और साफ रखें", "category": "light"},
            ])
        elif p == "education":
            remedies.extend([
                {"remedy_en": "Study room should be in Northeast or East — face East while studying", "remedy_hi": "अध्ययन कक्ष ईशान या पूर्व में हो — अध्ययन करते समय पूर्व की ओर मुख करें", "category": "placement"},
                {"remedy_en": "Place a Saraswati Yantra on the study desk", "remedy_hi": "अध्ययन डेस्क पर सरस्वती यंत्र रखें", "category": "yantra"},
                {"remedy_en": "Use green or cream colors in the study area", "remedy_hi": "अध्ययन क्षेत्र में हरा या क्रीम रंग उपयोग करें", "category": "color"},
            ])

    # Universal remedies applicable to all
    remedies.extend([
        {"remedy_en": "Keep the Brahma Sthana (center of house) open and clutter-free", "remedy_hi": "ब्रह्म स्थान (घर का केंद्र) खुला और साफ रखें", "category": "universal"},
        {"remedy_en": "Light a diya (oil lamp) in the Northeast corner every evening", "remedy_hi": "प्रत्येक संध्या ईशान कोने में दीपक जलाएँ", "category": "universal"},
        {"remedy_en": "Ensure Southwest is the heaviest zone — no empty SW corners", "remedy_hi": "सुनिश्चित करें कि नैऋत्य सबसे भारी क्षेत्र हो — खाली नैऋत्य कोने नहीं", "category": "universal"},
    ])

    return remedies


# ============================================================
# ROOM PLACEMENT GUIDE
# ============================================================
def get_room_placement(room_type: Optional[str] = None) -> dict:
    """
    Get Vastu-compliant room placement recommendations.

    Args:
        room_type: specific room key (e.g. "kitchen", "master_bedroom") or None for all

    Returns:
        dict with room placement data including ideal/avoid directions and tips
    """
    if room_type and room_type in ROOM_PLACEMENT:
        room = ROOM_PLACEMENT[room_type]
        return {
            "room_type": room_type,
            "room_name_en": room["name_en"],
            "room_name_hi": room["name_hi"],
            "ideal_directions": room["ideal"],
            "ideal_directions_hi": room["ideal_hi"],
            "acceptable_directions": room["acceptable"],
            "acceptable_directions_hi": room["acceptable_hi"],
            "avoid_directions": room["avoid"],
            "avoid_directions_hi": room["avoid_hi"],
            "reason_en": room["reason_en"],
            "reason_hi": room["reason_hi"],
            "tips_en": room["tips_en"],
            "tips_hi": room["tips_hi"],
            "direction_details": {
                d: DIRECTIONS[d] for d in room["ideal"] if d in DIRECTIONS
            },
        }

    # Return all rooms
    all_rooms = {}
    for key, room in ROOM_PLACEMENT.items():
        all_rooms[key] = {
            "room_name_en": room["name_en"],
            "room_name_hi": room["name_hi"],
            "ideal_directions": room["ideal"],
            "ideal_directions_hi": room["ideal_hi"],
            "acceptable_directions": room["acceptable"],
            "acceptable_directions_hi": room["acceptable_hi"],
            "avoid_directions": room["avoid"],
            "avoid_directions_hi": room["avoid_hi"],
            "reason_en": room["reason_en"],
            "reason_hi": room["reason_hi"],
            "tips_en": room["tips_en"],
            "tips_hi": room["tips_hi"],
        }

    return {
        "total_room_types": len(all_rooms),
        "rooms": all_rooms,
        "directions": DIRECTIONS,
    }


# ============================================================
# COMPLETE ANALYSIS — combines everything
# ============================================================
def get_complete_vastu_analysis(
    building_type: str = "residential",
    entrance_direction: Optional[str] = None,
    entrance_degrees: Optional[float] = None,
    problems: Optional[list[str]] = None,
) -> dict:
    """
    Full Vastu analysis combining mandala, entrance, room placement, and remedies.

    Args:
        building_type: "residential", "commercial", or "temple"
        entrance_direction: compass direction code or pada code
        entrance_degrees: precise compass degrees (0-360)
        problems: list of problem keywords for remedy suggestions

    Returns:
        Complete dict with all Vastu analysis sections
    """
    mandala = calculate_mandala(building_type, entrance_direction, entrance_degrees)

    entrance = None
    if entrance_direction or entrance_degrees is not None:
        direction = entrance_direction
        if not direction and entrance_degrees is not None:
            direction = _degrees_to_direction(entrance_degrees)
        entrance = analyze_entrance(direction, entrance_degrees)

    rooms = get_room_placement()

    remedies = None
    if problems:
        remedies = suggest_remedies(problems, building_type, entrance_direction)

    # Overall Vastu score (1-100)
    score = _calculate_vastu_score(entrance, problems)

    return {
        "score": score,
        "score_label_en": _score_label(score),
        "score_label_hi": _score_label_hi(score),
        "building_type": building_type,
        "mandala": mandala,
        "entrance_analysis": entrance,
        "room_placement": rooms,
        "remedies": remedies,
        "metal_remedies": METAL_REMEDIES,
        "color_therapy": COLOR_THERAPY,
    }


def _calculate_vastu_score(entrance: Optional[dict], problems: Optional[list]) -> int:
    """
    Calculate an overall Vastu compliance score (10-100).

    Formula:
      base 50  +  entrance bonus (0-30)  +  no-problem bonus (0-20)  -  problem penalty
      Max: 50 + 30 + 20 = 100   Min: 50 + 0 + 0 - 36 = 14 (clamped to 10)

    Entrance contribution: pada_score (1-5) * 6 = 6 to 30
    No-problem bonus: +20 when problems list is empty/None
    Problem penalty: -3 per problem (max 12 problems = -36)
    """
    score = 50

    if entrance:
        pada_score = entrance.get("score", 3)
        score += pada_score * 6  # 1→6, 3→18, 5→30

    if not problems or len(problems) == 0:
        score += 20  # no-problem bonus
    else:
        score -= len(problems) * 3

    return max(10, min(100, score))


def _score_label(score: int) -> str:
    if score >= 85:
        return "Excellent Vastu Compliance"
    elif score >= 70:
        return "Good — Minor Corrections Needed"
    elif score >= 50:
        return "Moderate — Multiple Remedies Recommended"
    else:
        return "Needs Significant Vastu Correction"


def _score_label_hi(score: int) -> str:
    if score >= 85:
        return "उत्कृष्ट वास्तु अनुपालन"
    elif score >= 70:
        return "अच्छा — मामूली सुधार आवश्यक"
    elif score >= 50:
        return "मध्यम — कई उपाय अनुशंसित"
    else:
        return "महत्वपूर्ण वास्तु सुधार आवश्यक"
