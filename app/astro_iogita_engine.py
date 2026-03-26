"""
astro_iogita_engine.py — Vedic Astrology × io-gita Atom Engine
================================================================
Maps 9 Vedic planets to 16 io-gita atoms from full_sanatan_system.py.
Same seed=42, D=10000 — atom vectors are identical to the original system.

Pipeline:
  planet_positions + current_dasha
  → build_atom_vector (PLANET_ATOM_MAP × PLANET_STRENGTH × DASHA_AMPLIFY)
  → identify_basin (top 3 positive, top negative, escape analysis)
  → run_astro_analysis (formatted report + JSON output)
"""
import numpy as np
import json
import os
from datetime import datetime

# ============================================================
# CONSTANTS — same as full_sanatan_system.py
# ============================================================
D = 10_000
BETA = 4.0
DT = 0.05
T_MAX = 500

rng = np.random.default_rng(42)

def _atom():
    """Generate a bipolar random vector, identical to full_sanatan_system.py atom()."""
    return rng.choice([-1, 1], size=D).astype(np.float64)

# 16 atoms — EXACT same order and seed as full_sanatan_system.py
ALL_ATOM_NAMES = [
    "DHARMA", "SATYA", "TYAGA", "AHANKAR",   # Shared moral forces
    "ATMA", "MOKSHA",                          # Gita (inner path)
    "KULA", "RAJYA",                           # Ramayana (outer society)
    "NYAYA", "KRODHA", "NITI", "SHAKTI", "BHAKTI",  # Mahabharata
    "KAAM", "LOBH", "MOH",                    # Panch Vikar (negative)
]
V = {name: _atom() for name in ALL_ATOM_NAMES}

# ============================================================
# 1. PLANET_ATOM_MAP — 9 Vedic planets to atom weights (-1.0 to +1.0)
# ============================================================
PLANET_ATOM_MAP = {
    "Sun": {
        "DHARMA": 0.9, "SATYA": 0.7, "ATMA": 0.95, "SHAKTI": 0.6,
        "AHANKAR": 0.5, "RAJYA": 0.4, "TYAGA": 0.2,
        "KAAM": -0.3, "LOBH": -0.4, "MOH": -0.5,
    },
    "Moon": {
        "MOH": 0.6, "BHAKTI": 0.8, "KULA": 0.7, "KAAM": 0.3,
        "ATMA": 0.4, "SATYA": 0.3,
        "KRODHA": -0.5, "AHANKAR": -0.3, "SHAKTI": -0.2,
    },
    "Mars": {
        "SHAKTI": 0.9, "KRODHA": 0.7, "NYAYA": 0.5, "DHARMA": 0.3,
        "NITI": 0.4, "AHANKAR": 0.4,
        "TYAGA": -0.5, "MOH": -0.3, "BHAKTI": -0.4,
    },
    "Mercury": {
        "NITI": 0.8, "SATYA": 0.6, "NYAYA": 0.7, "RAJYA": 0.3,
        "ATMA": 0.3, "DHARMA": 0.2,
        "KRODHA": -0.5, "MOH": -0.4, "AHANKAR": -0.2,
    },
    "Jupiter": {
        "DHARMA": 0.95, "MOKSHA": 0.8, "SATYA": 0.7, "NYAYA": 0.6,
        "BHAKTI": 0.7, "TYAGA": 0.5, "ATMA": 0.6,
        "KAAM": -0.6, "LOBH": -0.7, "AHANKAR": -0.4,
    },
    "Venus": {
        "KAAM": 0.7, "BHAKTI": 0.6, "MOH": 0.5, "KULA": 0.4,
        "LOBH": 0.3, "SHAKTI": 0.3,
        "TYAGA": -0.6, "MOKSHA": -0.4, "DHARMA": -0.2,
    },
    "Saturn": {
        "TYAGA": 0.8, "NYAYA": 0.7, "DHARMA": 0.5, "NITI": 0.6,
        "KRODHA": 0.3, "MOKSHA": 0.4,
        "KAAM": -0.7, "LOBH": -0.6, "AHANKAR": -0.5, "SHAKTI": -0.3,
    },
    "Rahu": {
        "MOH": 0.9, "LOBH": 0.8, "KAAM": 0.6, "AHANKAR": 0.7,
        "SHAKTI": 0.4, "RAJYA": 0.3,
        "DHARMA": -0.6, "SATYA": -0.7, "MOKSHA": -0.5, "TYAGA": -0.4,
    },
    "Ketu": {
        "MOKSHA": 0.9, "TYAGA": 0.8, "ATMA": 0.7, "DHARMA": 0.4,
        "SATYA": 0.3,
        "KAAM": -0.8, "MOH": -0.7, "LOBH": -0.6, "KULA": -0.4, "RAJYA": -0.3,
    },
}

# ============================================================
# 2. PLANET_STRENGTH — planet + sign → strength (0.0 to 1.0)
# ============================================================

# Zodiac signs
SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Exaltation signs
EXALTED = {
    "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn",
    "Mercury": "Virgo", "Jupiter": "Cancer", "Venus": "Pisces",
    "Saturn": "Libra", "Rahu": "Gemini", "Ketu": "Sagittarius",
}

# Debilitation signs (opposite of exalted)
DEBILITATED = {
    "Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer",
    "Mercury": "Pisces", "Jupiter": "Capricorn", "Venus": "Virgo",
    "Saturn": "Aries", "Rahu": "Sagittarius", "Ketu": "Gemini",
}

# Own signs
OWN_SIGNS = {
    "Sun": ["Leo"],
    "Moon": ["Cancer"],
    "Mars": ["Aries", "Scorpio"],
    "Mercury": ["Gemini", "Virgo"],
    "Jupiter": ["Sagittarius", "Pisces"],
    "Venus": ["Taurus", "Libra"],
    "Saturn": ["Capricorn", "Aquarius"],
    "Rahu": ["Aquarius"],
    "Ketu": ["Scorpio"],
}

# Friend signs (simplified — major friendships)
FRIEND_SIGNS = {
    "Sun": ["Aries", "Scorpio", "Sagittarius", "Pisces", "Cancer"],
    "Moon": ["Taurus", "Gemini", "Virgo", "Sagittarius", "Pisces"],
    "Mars": ["Leo", "Sagittarius", "Pisces", "Cancer"],
    "Mercury": ["Taurus", "Leo", "Libra", "Capricorn", "Aquarius"],
    "Jupiter": ["Aries", "Leo", "Scorpio", "Cancer"],
    "Venus": ["Gemini", "Virgo", "Capricorn", "Aquarius", "Pisces"],
    "Saturn": ["Taurus", "Gemini", "Virgo", "Libra"],
    "Rahu": ["Gemini", "Virgo", "Sagittarius", "Pisces"],
    "Ketu": ["Aries", "Sagittarius", "Pisces"],
}

# Enemy signs
ENEMY_SIGNS = {
    "Sun": ["Taurus", "Libra", "Capricorn", "Aquarius"],
    "Moon": ["Capricorn", "Aquarius"],
    "Mars": ["Gemini", "Virgo"],
    "Mercury": ["Cancer", "Scorpio"],
    "Jupiter": ["Taurus", "Libra", "Gemini", "Virgo"],
    "Venus": ["Cancer", "Leo"],
    "Saturn": ["Aries", "Leo", "Cancer", "Scorpio"],
    "Rahu": ["Leo", "Cancer"],
    "Ketu": ["Gemini", "Virgo"],
}


def get_planet_strength(planet: str, sign: str) -> float:
    """
    Return strength float 0.0 to 1.0 based on planet dignity in sign.
    Rules: Exalted=0.95, Own=0.85, Friend=0.65, Neutral=0.50, Enemy=0.35, Debilitated=0.20
    """
    if sign == EXALTED.get(planet):
        return 0.95
    if sign == DEBILITATED.get(planet):
        return 0.20
    if sign in OWN_SIGNS.get(planet, []):
        return 0.85
    if sign in FRIEND_SIGNS.get(planet, []):
        return 0.65
    if sign in ENEMY_SIGNS.get(planet, []):
        return 0.35
    return 0.50  # neutral


# ============================================================
# 3. DASHA_AMPLIFY — current mahadasha lord → atom amplification
# ============================================================
DASHA_AMPLIFY = {
    "Sun": {
        "ATMA": 1.8, "DHARMA": 1.6, "SATYA": 1.5, "SHAKTI": 1.4,
        "AHANKAR": 1.3,
    },
    "Moon": {
        "BHAKTI": 1.7, "MOH": 1.5, "KULA": 1.6, "KAAM": 1.3,
    },
    "Mars": {
        "SHAKTI": 1.8, "KRODHA": 1.6, "NYAYA": 1.4, "NITI": 1.3,
    },
    "Mercury": {
        "NITI": 1.7, "SATYA": 1.5, "NYAYA": 1.6, "RAJYA": 1.3,
    },
    "Jupiter": {
        "DHARMA": 1.8, "MOKSHA": 1.7, "BHAKTI": 1.6, "SATYA": 1.5,
        "TYAGA": 1.4,
    },
    "Venus": {
        "KAAM": 1.7, "BHAKTI": 1.5, "MOH": 1.4, "KULA": 1.3,
        "LOBH": 1.3,
    },
    "Saturn": {
        "TYAGA": 1.8, "NYAYA": 1.6, "DHARMA": 1.4, "NITI": 1.5,
        "MOKSHA": 1.3,
    },
    "Rahu": {
        "MOH": 1.8, "LOBH": 1.7, "AHANKAR": 1.6, "KAAM": 1.5,
        "SHAKTI": 1.3,
    },
    "Ketu": {
        "MOKSHA": 1.8, "TYAGA": 1.7, "ATMA": 1.6, "DHARMA": 1.4,
    },
}


# ============================================================
# 4. build_atom_vector(planet_positions, current_dasha) → np.array(16,)
# ============================================================
def build_atom_vector(planet_positions: dict, current_dasha: str) -> np.ndarray:
    """
    Build a 16-element atom activation vector.

    Input:
        planet_positions: dict of {planet_name: sign_name}
        current_dasha: string name of current Mahadasha lord

    Output:
        numpy array of shape (16,) with atom weights

    Logic: PLANET_ATOM_MAP × PLANET_STRENGTH × DASHA_AMPLIFY
    """
    atom_weights = np.zeros(16, dtype=np.float64)
    atom_index = {name: i for i, name in enumerate(ALL_ATOM_NAMES)}

    # Step 1: Accumulate planet contributions weighted by dignity
    for planet, sign in planet_positions.items():
        if planet not in PLANET_ATOM_MAP:
            continue
        strength = get_planet_strength(planet, sign)
        atom_map = PLANET_ATOM_MAP[planet]

        for atom_name, weight in atom_map.items():
            idx = atom_index[atom_name]
            atom_weights[idx] += weight * strength

    # Step 2: Apply Dasha amplification
    dasha_amps = DASHA_AMPLIFY.get(current_dasha, {})
    for atom_name, multiplier in dasha_amps.items():
        idx = atom_index[atom_name]
        atom_weights[idx] *= multiplier

    # Step 3: Normalize to [-1, 1] range
    max_abs = np.max(np.abs(atom_weights))
    if max_abs > 0:
        atom_weights = atom_weights / max_abs

    return atom_weights


# ============================================================
# 5. identify_basin(atom_vector) → dict
# ============================================================

# Basin definitions — named attractor patterns
BASIN_DEFINITIONS = {
    "Dharma-Yukta": {
        "dominant": ["DHARMA", "SATYA", "NYAYA"],
        "hindi": "धर्म-युक्त",
        "description": "A life aligned with cosmic order. Strong moral compass, truthful conduct, and justice-seeking nature.",
        "escape_trigger": "When AHANKAR (ego) overwhelms DHARMA through unchecked power or praise.",
        "warning": "Risk of rigidity — dharma without compassion becomes tyranny.",
    },
    "Moksha-Marga": {
        "dominant": ["MOKSHA", "ATMA", "TYAGA"],
        "hindi": "मोक्ष-मार्ग",
        "description": "The liberation path. Deep self-knowledge, renunciation of attachments, spiritual seeking.",
        "escape_trigger": "When worldly KAAM or MOH pulls the seeker back into material engagement.",
        "warning": "Risk of withdrawal — detachment without engagement becomes escapism.",
    },
    "Shakti-Krodha": {
        "dominant": ["SHAKTI", "KRODHA", "NITI"],
        "hindi": "शक्ति-क्रोध",
        "description": "Warrior energy. Power combined with righteous anger and strategic thinking. Arjuna before the battle.",
        "escape_trigger": "When BHAKTI (devotion) or TYAGA (sacrifice) softens the war stance.",
        "warning": "Risk of destruction — unchecked KRODHA without DHARMA becomes violence.",
    },
    "Kama-Moha": {
        "dominant": ["KAAM", "MOH", "LOBH"],
        "hindi": "काम-मोह",
        "description": "Trapped in desire and attachment. Material pursuit dominates spiritual growth. The Panch Vikar basin.",
        "escape_trigger": "A shock (Saturn transit, loss) that awakens TYAGA and ATMA awareness.",
        "warning": "This is the most common human basin. Escape requires conscious effort.",
    },
    "Bhakti-Kula": {
        "dominant": ["BHAKTI", "KULA", "DHARMA"],
        "hindi": "भक्ति-कुल",
        "description": "Devotional family path. Strong bonds, religious observance, community-oriented dharma.",
        "escape_trigger": "When MOKSHA seeking or RAJYA ambition pulls beyond family boundaries.",
        "warning": "Risk of insularity — family dharma can become tribal exclusion.",
    },
    "Rajya-Niti": {
        "dominant": ["RAJYA", "NITI", "SHAKTI"],
        "hindi": "राज्य-नीति",
        "description": "Governance and statecraft. Strategic leadership, institutional power, administrative wisdom.",
        "escape_trigger": "When LOBH (greed for power) erodes NYAYA (justice) in governance.",
        "warning": "Risk of Machiavellian drift — NITI without DHARMA becomes cunning.",
    },
    "Ahankar-Trap": {
        "dominant": ["AHANKAR", "SHAKTI", "RAJYA"],
        "hindi": "अहंकार-जाल",
        "description": "Ego dominance. Self-importance, pride, attachment to status and identity.",
        "escape_trigger": "Humbling experience that reconnects with ATMA and TYAGA.",
        "warning": "Most difficult to escape — ego doesn't recognize its own trap.",
    },
    "Nyaya-Satya": {
        "dominant": ["NYAYA", "SATYA", "NITI"],
        "hindi": "न्याय-सत्य",
        "description": "Truth and justice path. Intellectual honesty, fair dealing, ethical reasoning.",
        "escape_trigger": "When emotional forces (BHAKTI, KRODHA) override logical assessment.",
        "warning": "Risk of cold calculation — justice without mercy becomes cruelty.",
    },
}


def identify_basin(atom_vector: np.ndarray) -> dict:
    """
    Identify the attractor basin from atom activation vector.

    Input: atom_vector numpy array of shape (16,)
    Logic: find top 3 positive atoms, find top negative atom
    Output: dict with basin_name, basin_hindi, description, escape info
    """
    atom_activations = {name: atom_vector[i] for i, name in enumerate(ALL_ATOM_NAMES)}

    # Sort by activation (descending)
    sorted_atoms = sorted(atom_activations.items(), key=lambda x: x[1], reverse=True)
    top_3_positive = [(name, val) for name, val in sorted_atoms[:3]]

    # Top negative atom
    sorted_negative = sorted(atom_activations.items(), key=lambda x: x[1])
    top_negative = sorted_negative[0] if sorted_negative[0][1] < 0 else ("NONE", 0.0)

    # Match to basin — find best overlap with top 3 dominant atoms
    top_3_names = [name for name, _ in top_3_positive]
    best_basin = None
    best_overlap = 0

    for basin_name, basin_def in BASIN_DEFINITIONS.items():
        overlap = len(set(top_3_names) & set(basin_def["dominant"]))
        if overlap > best_overlap:
            best_overlap = overlap
            best_basin = basin_name

    # Default basin if no match
    if best_basin is None or best_overlap == 0:
        # Use the strongest atom to determine basin
        strongest = top_3_names[0]
        basin_map = {
            "DHARMA": "Dharma-Yukta", "SATYA": "Nyaya-Satya", "TYAGA": "Moksha-Marga",
            "AHANKAR": "Ahankar-Trap", "ATMA": "Moksha-Marga", "MOKSHA": "Moksha-Marga",
            "KULA": "Bhakti-Kula", "RAJYA": "Rajya-Niti", "NYAYA": "Nyaya-Satya",
            "KRODHA": "Shakti-Krodha", "NITI": "Rajya-Niti", "SHAKTI": "Shakti-Krodha",
            "BHAKTI": "Bhakti-Kula", "KAAM": "Kama-Moha", "LOBH": "Kama-Moha",
            "MOH": "Kama-Moha",
        }
        best_basin = basin_map.get(strongest, "Kama-Moha")

    basin_def = BASIN_DEFINITIONS[best_basin]

    # Escape analysis
    negative_strength = abs(top_negative[1])
    positive_strength = sum(val for _, val in top_3_positive)
    escape_possible = bool(negative_strength > 0.3 and positive_strength < 2.5)

    # Trajectory steps estimate: stronger basin = more steps to escape
    trajectory_steps = int(20 + (float(positive_strength) / 3.0) * 60)
    trajectory_steps = max(20, min(80, trajectory_steps))

    # Convert numpy types to native Python for JSON serialization
    top_3_positive = [(name, float(val)) for name, val in top_3_positive]
    top_negative = (top_negative[0], float(top_negative[1]))

    return {
        "basin_name": best_basin,
        "basin_hindi": basin_def["hindi"],
        "description": basin_def["description"],
        "escape_possible": escape_possible,
        "escape_trigger": basin_def["escape_trigger"],
        "warning": basin_def["warning"],
        "trajectory_steps": trajectory_steps,
        "top_3_atoms": top_3_positive,
        "top_negative": top_negative,
        "overlap_score": best_overlap,
    }


# ============================================================
# 6. run_astro_analysis(planet_positions, current_dasha, person_name)
# ============================================================
def run_astro_analysis(planet_positions: dict, current_dasha: str, person_name: str) -> dict:
    """
    Full astro-iogita analysis pipeline.
    Calls build_atom_vector → identify_basin → formatted report.
    Returns dict with all analysis data.
    """
    # Build atom vector
    atom_vector = build_atom_vector(planet_positions, current_dasha)

    # Identify basin
    basin = identify_basin(atom_vector)

    # Atom activation table
    activations = {}
    for i, name in enumerate(ALL_ATOM_NAMES):
        activations[name] = round(float(atom_vector[i]), 4)

    # Planet strengths
    planet_strengths = {}
    for planet, sign in planet_positions.items():
        planet_strengths[planet] = {
            "sign": sign,
            "strength": get_planet_strength(planet, sign),
            "dignity": _get_dignity_label(planet, sign),
        }

    # Normal astrology insights (4 bullet points)
    normal_insights = _generate_normal_insights(planet_positions, planet_strengths, current_dasha)

    # io-gita combined insight
    iogita_insight = _generate_iogita_insight(basin, activations, current_dasha)

    # Print formatted report
    _print_report(person_name, activations, planet_strengths, basin, normal_insights, iogita_insight, current_dasha)

    # Return full analysis dict
    return {
        "person_name": person_name,
        "planet_positions": planet_positions,
        "current_dasha": current_dasha,
        "planet_strengths": planet_strengths,
        "atom_activations": activations,
        "atom_vector": atom_vector.tolist(),
        "basin": {
            "name": basin["basin_name"],
            "hindi": basin["basin_hindi"],
            "description": basin["description"],
            "escape_possible": basin["escape_possible"],
            "escape_trigger": basin["escape_trigger"],
            "warning": basin["warning"],
            "trajectory_steps": basin["trajectory_steps"],
            "top_3_atoms": [(n, round(v, 4)) for n, v in basin["top_3_atoms"]],
            "top_negative": (basin["top_negative"][0], round(basin["top_negative"][1], 4)),
        },
        "normal_astrology": normal_insights,
        "iogita_insight": iogita_insight,
        "engine_params": {"D": D, "BETA": BETA, "DT": DT, "T_MAX": T_MAX, "seed": 42, "atoms": 16},
        "timestamp": datetime.now(tz=__import__('datetime').timezone.utc).isoformat(),
        "version": "2.0",
    }


def _get_dignity_label(planet: str, sign: str) -> str:
    """Return human-readable dignity label."""
    if sign == EXALTED.get(planet):
        return "Exalted"
    if sign == DEBILITATED.get(planet):
        return "Debilitated"
    if sign in OWN_SIGNS.get(planet, []):
        return "Own Sign"
    if sign in FRIEND_SIGNS.get(planet, []):
        return "Friendly"
    if sign in ENEMY_SIGNS.get(planet, []):
        return "Enemy"
    return "Neutral"


def _generate_normal_insights(positions: dict, strengths: dict, dasha: str) -> list:
    """Generate 4 bullet points of normal astrology interpretation."""
    insights = []

    # 1. Sun sign personality
    sun_sign = positions.get("Sun", "Unknown")
    insights.append(
        f"Sun in {sun_sign} ({strengths.get('Sun', {}).get('dignity', 'Unknown')}): "
        f"Core identity is shaped by {sun_sign} energy — "
        f"{'leadership and authority' if sun_sign in ['Leo', 'Aries'] else 'analytical and service-oriented' if sun_sign in ['Virgo'] else 'emotional depth and transformation' if sun_sign in ['Scorpio'] else 'adaptability and communication' if sun_sign in ['Gemini'] else 'stability and determination'}."
    )

    # 2. Moon sign emotional nature
    moon_sign = positions.get("Moon", "Unknown")
    insights.append(
        f"Moon in {moon_sign} ({strengths.get('Moon', {}).get('dignity', 'Unknown')}): "
        f"Emotional world is {'intense and secretive' if moon_sign == 'Scorpio' else 'nurturing and family-oriented' if moon_sign == 'Cancer' else 'stable and comfort-seeking' if moon_sign == 'Taurus' else 'restless and curious' if moon_sign == 'Gemini' else 'idealistic and philosophical' if moon_sign == 'Sagittarius' else 'emotionally adaptive'}."
    )

    # 3. Current Dasha influence
    dasha_strength = strengths.get(dasha, {}).get("strength", 0.5)
    insights.append(
        f"{dasha} Mahadasha (strength {dasha_strength:.2f}): "
        f"{'Highly favorable period — planet is dignified' if dasha_strength >= 0.8 else 'Challenging period — planet is weakened' if dasha_strength <= 0.3 else 'Mixed results — planet has moderate influence'}. "
        f"Focus on {dasha}-ruled matters."
    )

    # 4. Key strength/weakness
    strongest = max(strengths.items(), key=lambda x: x[1]["strength"])
    weakest = min(strengths.items(), key=lambda x: x[1]["strength"])
    insights.append(
        f"Strongest placement: {strongest[0]} in {strongest[1]['sign']} ({strongest[1]['dignity']}, {strongest[1]['strength']:.2f}). "
        f"Weakest: {weakest[0]} in {weakest[1]['sign']} ({weakest[1]['dignity']}, {weakest[1]['strength']:.2f})."
    )

    return insights


def _generate_iogita_insight(basin: dict, activations: dict, dasha: str) -> str:
    """Generate combined io-gita insight."""
    top_atoms = ", ".join(f"{n} ({v:.3f})" for n, v in basin["top_3_atoms"])
    neg_name, neg_val = basin["top_negative"]

    return (
        f"io-gita attractor analysis places you in the {basin['basin_name']} ({basin['basin_hindi']}) basin. "
        f"Your dominant atoms are {top_atoms}, with {neg_name} ({neg_val:.3f}) as the strongest suppressed force. "
        f"Under {dasha} Mahadasha, the {basin['basin_name']} pattern is "
        f"{'reinforced — expect deepening of this life theme' if not basin['escape_possible'] else 'potentially unstable — conditions exist for a life phase transition'}. "
        f"Normal astrology sees planets in signs. io-gita sees the COMBINED gravitational field — "
        f"where all 9 planets pull your consciousness toward {basin['basin_name']}. "
        f"Estimated trajectory: {basin['trajectory_steps']} computational steps in this basin. "
        f"{basin['warning']}"
    )


def _print_report(name, activations, strengths, basin, normal, iogita, dasha):
    """Print formatted analysis report to stdout."""
    print("\n" + "=" * 70)
    print(f"  ASTRO-IOGITA ANALYSIS: {name}")
    print(f"  Current Dasha: {dasha} Mahadasha")
    print("=" * 70)

    # Planet strengths table
    print("\n--- PLANET DIGNITIES ---")
    print(f"  {'Planet':<10} {'Sign':<14} {'Dignity':<14} {'Strength':>8}")
    print("  " + "-" * 48)
    for planet, info in strengths.items():
        print(f"  {planet:<10} {info['sign']:<14} {info['dignity']:<14} {info['strength']:>8.2f}")

    # Atom activation table with bar chart
    print("\n--- ATOM ACTIVATIONS (io-gita D=10000, seed=42) ---")
    print(f"  {'Atom':<12} {'Weight':>8}  Bar")
    print("  " + "-" * 50)
    for name in ALL_ATOM_NAMES:
        val = activations[name]
        bar_len = int(abs(val) * 20)
        if val >= 0:
            bar = "+" * bar_len
        else:
            bar = "-" * bar_len
        print(f"  {name:<12} {val:>8.4f}  {bar}")

    # Basin identification
    print(f"\n--- BASIN IDENTIFICATION ---")
    print(f"  Basin: {basin['basin_name']} ({basin['basin_hindi']})")
    print(f"  {basin['description']}")
    print(f"  Escape possible: {'YES' if basin['escape_possible'] else 'NO'}")
    print(f"  Escape trigger: {basin['escape_trigger']}")
    print(f"  Warning: {basin['warning']}")
    print(f"  Trajectory steps: {basin['trajectory_steps']}")

    # Normal astrology
    print(f"\n--- NORMAL ASTROLOGY SAYS ---")
    for i, insight in enumerate(normal, 1):
        print(f"  {i}. {insight}")

    # io-gita combined
    print(f"\n--- IO-GITA SAYS (combined picture) ---")
    print(f"  {iogita}")

    print("\n" + "=" * 70)


# ============================================================
# 7. TEST — Meharban Singh's Chart
# ============================================================
if __name__ == "__main__":
    planet_positions = {
        "Sun": "Leo",
        "Moon": "Scorpio",
        "Mercury": "Cancer",
        "Venus": "Cancer",
        "Mars": "Cancer",
        "Jupiter": "Capricorn",
        "Saturn": "Libra",
        "Rahu": "Aries",
        "Ketu": "Libra",
    }
    current_dasha = "Venus"
    person_name = "Meharban Singh"

    # Run analysis
    result = run_astro_analysis(planet_positions, current_dasha, person_name)

    # Save to JSON
    output_path = os.path.join(os.path.dirname(__file__), "..", "astro_meharban_result.json")
    output_path = os.path.abspath(output_path)

    # Make JSON-serializable (convert tuples to lists)
    json_result = json.loads(json.dumps(result, default=str))

    with open(output_path, "w") as f:
        json.dump(json_result, f, indent=2)

    print(f"\n  Result saved to: {output_path}")
    print(f"  Version: {result['version']}")
