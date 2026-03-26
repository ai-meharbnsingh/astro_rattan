"""Tests for dasha_engine.py — Vimshottari Dasha calculations."""
import pytest
from datetime import datetime


def test_dasha_years_sum_to_120():
    """Vimshottari total must be exactly 120 years."""
    from app.dasha_engine import DASHA_YEARS
    assert sum(DASHA_YEARS.values()) == 120


def test_dasha_order_has_9_planets():
    """Dasha order must contain exactly 9 planets in correct sequence."""
    from app.dasha_engine import DASHA_ORDER
    assert len(DASHA_ORDER) == 9
    assert DASHA_ORDER == [
        "Ketu", "Venus", "Sun", "Moon", "Mars",
        "Rahu", "Jupiter", "Saturn", "Mercury",
    ]


def test_nakshatra_lord_has_27_entries():
    """All 27 nakshatras must be mapped to their ruling planet."""
    from app.dasha_engine import NAKSHATRA_LORD, DASHA_YEARS
    assert len(NAKSHATRA_LORD) == 27
    # Every lord must be a valid planet in DASHA_YEARS
    for nak, lord in NAKSHATRA_LORD.items():
        assert lord in DASHA_YEARS, f"{nak} has invalid lord: {lord}"


def test_nakshatra_lords_cycle_three_times():
    """Each planet rules exactly 3 nakshatras (27 / 9 = 3)."""
    from app.dasha_engine import NAKSHATRA_LORD
    from collections import Counter
    lord_counts = Counter(NAKSHATRA_LORD.values())
    for planet, count in lord_counts.items():
        assert count == 3, f"{planet} rules {count} nakshatras, expected 3"


def test_calculate_dasha_returns_9_periods():
    """Mahadasha should return exactly 9 periods covering 120 years."""
    from app.dasha_engine import calculate_dasha
    result = calculate_dasha("Ashwini", "1990-01-15")
    assert "mahadasha_periods" in result
    assert len(result["mahadasha_periods"]) == 9
    total_years = sum(p["years"] for p in result["mahadasha_periods"])
    assert total_years == 120


def test_calculate_dasha_starts_from_nakshatra_lord():
    """First mahadasha must be the nakshatra lord."""
    from app.dasha_engine import calculate_dasha, NAKSHATRA_LORD
    # Ashwini is ruled by Ketu
    result = calculate_dasha("Ashwini", "1990-01-15")
    assert result["mahadasha_periods"][0]["planet"] == "Ketu"
    assert result["mahadasha_periods"][0]["years"] == 7

    # Rohini is ruled by Moon
    result2 = calculate_dasha("Rohini", "1990-01-15")
    assert result2["mahadasha_periods"][0]["planet"] == "Moon"
    assert result2["mahadasha_periods"][0]["years"] == 10


def test_calculate_dasha_current_dasha_is_valid():
    """Current dasha must be one of the 9 planets (not Unknown for recent births)."""
    from app.dasha_engine import calculate_dasha, DASHA_YEARS
    result = calculate_dasha("Pushya", "1995-06-20")
    assert result["current_dasha"] in DASHA_YEARS


def test_calculate_dasha_current_antardasha_is_valid():
    """Current antardasha must be one of the 9 planets."""
    from app.dasha_engine import calculate_dasha, DASHA_YEARS
    result = calculate_dasha("Hasta", "2000-03-10")
    # For a 2000 birth, we're 26 years in — well within 120 years
    assert result["current_antardasha"] in DASHA_YEARS


def test_calculate_dasha_unknown_nakshatra():
    """Unknown nakshatra should return error response."""
    from app.dasha_engine import calculate_dasha
    result = calculate_dasha("FakeNakshatra", "1990-01-01")
    assert "error" in result
    assert result["current_dasha"] == "Unknown"


def test_calculate_dasha_date_ordering():
    """Each period's end_date must be after its start_date, and periods must be contiguous."""
    from app.dasha_engine import calculate_dasha
    result = calculate_dasha("Mrigashira", "1985-11-30")
    periods = result["mahadasha_periods"]

    for i, period in enumerate(periods):
        start = datetime.strptime(period["start_date"], "%Y-%m-%d")
        end = datetime.strptime(period["end_date"], "%Y-%m-%d")
        assert end > start, f"Period {i} ({period['planet']}): end <= start"

        # Check contiguity with next period
        if i < len(periods) - 1:
            next_start = datetime.strptime(periods[i + 1]["start_date"], "%Y-%m-%d")
            assert abs((end - next_start).days) <= 1, (
                f"Gap between period {i} and {i+1}"
            )
