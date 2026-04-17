"""Tests for bilingual translation constants."""
import pytest
from app.lalkitab_translations import (
    PLANET_NAMES_HI, SIGN_NAMES_HI, HOUSE_NAMES_HI, DIGNITY_LABELS_HI
)

def test_planet_names_are_hindi():
    """All planet names must be Devanagari, not English."""
    for en, hi in PLANET_NAMES_HI.items():
        assert hi != en, f"Planet '{en}' Hindi is same as English"
        has_devanagari = any('\u0900' <= c <= '\u097F' for c in hi)
        assert has_devanagari, f"Planet '{en}' Hindi '{hi}' has no Devanagari"

def test_sign_names_are_hindi():
    for en, hi in SIGN_NAMES_HI.items():
        assert hi != en, f"Sign '{en}' Hindi is same as English"
        has_devanagari = any('\u0900' <= c <= '\u097F' for c in hi)
        assert has_devanagari, f"Sign '{en}' Hindi '{hi}' has no Devanagari"

def test_all_9_planets_covered():
    expected = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"}
    assert set(PLANET_NAMES_HI.keys()) == expected

def test_all_12_signs_covered():
    assert len(SIGN_NAMES_HI) == 12

def test_all_12_houses_covered():
    assert set(HOUSE_NAMES_HI.keys()) == set(range(1, 13))

def test_dignity_labels_covered():
    expected = {"Exalted", "Own Sign", "Friendly", "Neutral", "Enemy", "Debilitated"}
    assert set(DIGNITY_LABELS_HI.keys()) == expected

def test_dignity_labels_are_hindi():
    for en, hi in DIGNITY_LABELS_HI.items():
        has_devanagari = any('\u0900' <= c <= '\u097F' for c in hi)
        assert has_devanagari, f"Dignity '{en}' has no Devanagari: '{hi}'"
