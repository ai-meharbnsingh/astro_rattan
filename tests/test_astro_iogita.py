"""Tests for astro_iogita_engine.py — the KEY deliverable."""
import numpy as np
import pytest


def test_planet_atom_map_has_9_planets():
    from app.astro_iogita_engine import PLANET_ATOM_MAP
    assert len(PLANET_ATOM_MAP) == 9
    expected = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"}
    assert set(PLANET_ATOM_MAP.keys()) == expected


def test_planet_atom_map_weights_in_range():
    from app.astro_iogita_engine import PLANET_ATOM_MAP
    for planet, atoms in PLANET_ATOM_MAP.items():
        for atom, weight in atoms.items():
            assert -1.0 <= weight <= 1.0, f"{planet}.{atom} = {weight} out of range"


def test_planet_strength_exalted():
    from app.astro_iogita_engine import get_planet_strength
    assert get_planet_strength("Sun", "Aries") == 0.95
    assert get_planet_strength("Moon", "Taurus") == 0.95
    assert get_planet_strength("Saturn", "Libra") == 0.95


def test_planet_strength_debilitated():
    from app.astro_iogita_engine import get_planet_strength
    assert get_planet_strength("Sun", "Libra") == 0.20
    assert get_planet_strength("Moon", "Scorpio") == 0.20
    assert get_planet_strength("Jupiter", "Capricorn") == 0.20


def test_planet_strength_own_sign():
    from app.astro_iogita_engine import get_planet_strength
    assert get_planet_strength("Sun", "Leo") == 0.85
    assert get_planet_strength("Mars", "Aries") == 0.85


def test_planet_strength_neutral():
    from app.astro_iogita_engine import get_planet_strength
    assert get_planet_strength("Rahu", "Aries") == 0.50


def test_dasha_amplify_has_9_planets():
    from app.astro_iogita_engine import DASHA_AMPLIFY
    assert len(DASHA_AMPLIFY) == 9


def test_dasha_amplify_range():
    from app.astro_iogita_engine import DASHA_AMPLIFY
    for planet, amps in DASHA_AMPLIFY.items():
        for atom, mult in amps.items():
            assert 1.3 <= mult <= 1.8, f"{planet}.{atom} amplify = {mult}"


def test_build_atom_vector_shape():
    from app.astro_iogita_engine import build_atom_vector
    positions = {"Sun": "Leo", "Moon": "Cancer", "Mars": "Aries"}
    vec = build_atom_vector(positions, "Sun")
    assert isinstance(vec, np.ndarray)
    assert vec.shape == (16,)


def test_build_atom_vector_normalized():
    from app.astro_iogita_engine import build_atom_vector
    positions = {
        "Sun": "Leo", "Moon": "Scorpio", "Mercury": "Cancer",
        "Venus": "Cancer", "Mars": "Cancer", "Jupiter": "Capricorn",
        "Saturn": "Libra", "Rahu": "Aries", "Ketu": "Libra"
    }
    vec = build_atom_vector(positions, "Venus")
    assert np.max(np.abs(vec)) <= 1.0 + 1e-10


def test_identify_basin_returns_required_keys():
    from app.astro_iogita_engine import build_atom_vector, identify_basin
    positions = {"Sun": "Leo", "Moon": "Cancer"}
    vec = build_atom_vector(positions, "Sun")
    basin = identify_basin(vec)
    required_keys = {"basin_name", "basin_hindi", "description", "escape_possible", "escape_trigger", "warning", "trajectory_steps"}
    assert required_keys.issubset(set(basin.keys()))


def test_identify_basin_trajectory_in_range():
    from app.astro_iogita_engine import build_atom_vector, identify_basin
    positions = {"Sun": "Leo", "Moon": "Cancer", "Jupiter": "Sagittarius"}
    vec = build_atom_vector(positions, "Jupiter")
    basin = identify_basin(vec)
    assert 20 <= basin["trajectory_steps"] <= 80


def test_run_astro_analysis_meharban():
    from app.astro_iogita_engine import run_astro_analysis
    positions = {
        "Sun": "Leo", "Moon": "Scorpio", "Mercury": "Cancer",
        "Venus": "Cancer", "Mars": "Cancer", "Jupiter": "Capricorn",
        "Saturn": "Libra", "Rahu": "Aries", "Ketu": "Libra"
    }
    result = run_astro_analysis(positions, "Venus", "Meharban Singh")
    assert result["person_name"] == "Meharban Singh"
    assert result["version"] == "2.0"
    assert "basin" in result
    assert result["basin"]["name"] in [
        "Dharma-Yukta", "Moksha-Marga", "Shakti-Krodha", "Kama-Moha",
        "Bhakti-Kula", "Rajya-Niti", "Ahankar-Trap", "Nyaya-Satya"
    ]
    assert len(result["atom_activations"]) == 16
    assert len(result["normal_astrology"]) == 4


def test_all_16_atoms_present():
    from app.astro_iogita_engine import ALL_ATOM_NAMES, V
    assert len(ALL_ATOM_NAMES) == 16
    assert len(V) == 16
    for name in ALL_ATOM_NAMES:
        assert name in V
        assert V[name].shape == (10_000,)
