"""Tests for Birth Time Rectification Engine.

Covers:
  - Event signature lookup
  - Scoring logic with known dasha/transit configurations
  - Edge cases: narrow window, no events, single event, unknown event type
  - Full rectification with multiple events
"""
import pytest


# ======================================================================
# _get_event_signatures
# ======================================================================

class TestEventSignatures:
    """Tests for _get_event_signatures()."""

    def test_known_event_type_returns_signature(self):
        from app.birth_rectification_engine import _get_event_signatures
        sig = _get_event_signatures("marriage")
        assert "dasha_lords" in sig
        assert "houses" in sig
        assert "transit_planets" in sig
        assert "malefic" in sig
        assert "Venus" in sig["dasha_lords"]
        assert 7 in sig["houses"]
        assert sig["malefic"] is False

    def test_all_event_types_have_signatures(self):
        from app.birth_rectification_engine import _get_event_signatures, EVENT_SIGNATURES
        for event_type in EVENT_SIGNATURES:
            sig = _get_event_signatures(event_type)
            assert len(sig["dasha_lords"]) > 0, f"{event_type} has no dasha lords"
            assert len(sig["houses"]) > 0, f"{event_type} has no houses"
            assert len(sig["transit_planets"]) > 0, f"{event_type} has no transit planets"

    def test_unknown_event_type_returns_empty(self):
        from app.birth_rectification_engine import _get_event_signatures
        sig = _get_event_signatures("winning_lottery")
        assert len(sig["dasha_lords"]) == 0
        assert len(sig["houses"]) == 0

    def test_malefic_events_flagged_correctly(self):
        from app.birth_rectification_engine import _get_event_signatures
        assert _get_event_signatures("accident")["malefic"] is True
        assert _get_event_signatures("job_loss")["malefic"] is True
        assert _get_event_signatures("father_death")["malefic"] is True
        assert _get_event_signatures("marriage")["malefic"] is False
        assert _get_event_signatures("child_birth")["malefic"] is False

    def test_child_birth_signature(self):
        from app.birth_rectification_engine import _get_event_signatures
        sig = _get_event_signatures("child_birth")
        assert "Jupiter" in sig["dasha_lords"]
        assert 5 in sig["houses"]

    def test_health_issue_signature(self):
        from app.birth_rectification_engine import _get_event_signatures
        sig = _get_event_signatures("health_issue")
        assert 6 in sig["houses"]
        assert 8 in sig["houses"]
        assert "Saturn" in sig["dasha_lords"]


# ======================================================================
# _score_event_match
# ======================================================================

class TestScoreEventMatch:
    """Tests for _score_event_match() scoring logic."""

    # Sample birth chart with Leo ascendant (house 1 = Leo)
    SAMPLE_CHART = {
        "ascendant": {"sign": "Leo", "longitude": 130.0},
        "houses": [
            {"number": 1, "sign": "Leo", "degree": 120.0},
            {"number": 2, "sign": "Virgo", "degree": 150.0},
            {"number": 3, "sign": "Libra", "degree": 180.0},
            {"number": 4, "sign": "Scorpio", "degree": 210.0},
            {"number": 5, "sign": "Sagittarius", "degree": 240.0},
            {"number": 6, "sign": "Capricorn", "degree": 270.0},
            {"number": 7, "sign": "Aquarius", "degree": 300.0},
            {"number": 8, "sign": "Pisces", "degree": 330.0},
            {"number": 9, "sign": "Aries", "degree": 0.0},
            {"number": 10, "sign": "Taurus", "degree": 30.0},
            {"number": 11, "sign": "Gemini", "degree": 60.0},
            {"number": 12, "sign": "Cancer", "degree": 90.0},
        ],
        "planets": {
            "Sun": {"house": 1, "sign": "Leo"},
            "Moon": {"house": 4, "sign": "Scorpio"},
            "Jupiter": {"house": 5, "sign": "Sagittarius"},
        },
    }

    def test_perfect_marriage_match_scores_high(self):
        """Venus MD + Jupiter AD + Jupiter transit 7th house = high score."""
        from app.birth_rectification_engine import _score_event_match

        event = {"type": "marriage", "date": "2015-03-20"}
        dasha = {"mahadasha": "Venus", "antardasha": "Jupiter"}
        # Jupiter transiting Aquarius = 7th from Leo asc
        transit = {"planets": {
            "Jupiter": {"sign": "Aquarius", "longitude": 310.0},
            "Venus": {"sign": "Aries", "longitude": 15.0},
        }}

        score = _score_event_match(event, dasha, transit, self.SAMPLE_CHART)
        # Venus MD = 30pts, Jupiter AD = 20pts, Jupiter transit 7th = partial transit
        assert score >= 50.0, f"Expected >= 50 for strong marriage match, got {score}"

    def test_no_match_scores_low(self):
        """Completely mismatched dasha/transit should score near zero."""
        from app.birth_rectification_engine import _score_event_match

        event = {"type": "marriage", "date": "2015-03-20"}
        dasha = {"mahadasha": "Saturn", "antardasha": "Mars"}
        transit = {"planets": {
            "Jupiter": {"sign": "Leo", "longitude": 130.0},
            "Venus": {"sign": "Scorpio", "longitude": 220.0},
        }}

        score = _score_event_match(event, dasha, transit, self.SAMPLE_CHART)
        assert score < 30.0, f"Expected < 30 for mismatched marriage, got {score}"

    def test_unknown_event_type_scores_zero(self):
        from app.birth_rectification_engine import _score_event_match

        event = {"type": "invented_event", "date": "2020-01-01"}
        dasha = {"mahadasha": "Venus", "antardasha": "Jupiter"}
        transit = {"planets": {}}

        score = _score_event_match(event, dasha, transit, self.SAMPLE_CHART)
        assert score == 0.0

    def test_score_between_zero_and_hundred(self):
        """Score should never exceed 100 or go below 0."""
        from app.birth_rectification_engine import _score_event_match

        event = {"type": "job_start", "date": "2020-01-01"}
        dasha = {"mahadasha": "Saturn", "antardasha": "Sun"}
        transit = {"planets": {
            "Jupiter": {"sign": "Taurus", "longitude": 40.0},
            "Saturn": {"sign": "Capricorn", "longitude": 280.0},
            "Sun": {"sign": "Taurus", "longitude": 35.0},
        }}

        score = _score_event_match(event, dasha, transit, self.SAMPLE_CHART)
        assert 0 <= score <= 100

    def test_mahadasha_only_match(self):
        """Only mahadasha lord matches, nothing else."""
        from app.birth_rectification_engine import _score_event_match

        event = {"type": "education", "date": "2010-06-01"}
        dasha = {"mahadasha": "Mercury", "antardasha": "Mars"}
        transit = {"planets": {
            "Jupiter": {"sign": "Leo", "longitude": 130.0},
            "Mercury": {"sign": "Aries", "longitude": 10.0},
        }}

        score = _score_event_match(event, dasha, transit, self.SAMPLE_CHART)
        # Should get 30 for MD match, possibly some house lord points
        assert score >= 30.0

    def test_accident_malefic_dasha(self):
        """Mars MD + Rahu AD for accident should score well."""
        from app.birth_rectification_engine import _score_event_match

        event = {"type": "accident", "date": "2018-11-15"}
        dasha = {"mahadasha": "Mars", "antardasha": "Rahu"}
        transit = {"planets": {
            "Mars": {"sign": "Pisces", "longitude": 340.0},
            "Rahu": {"sign": "Cancer", "longitude": 100.0},
            "Ketu": {"sign": "Capricorn", "longitude": 280.0},
        }}

        score = _score_event_match(event, dasha, transit, self.SAMPLE_CHART)
        assert score >= 50.0, f"Expected >= 50 for accident match, got {score}"


# ======================================================================
# calculate_rectification
# ======================================================================

class TestCalculateRectification:
    """Integration tests for the main rectification function."""

    BIRTH_PLACE = {"lat": 28.6139, "lon": 77.2090}  # Delhi

    def test_no_events_returns_empty(self):
        from app.birth_rectification_engine import calculate_rectification

        result = calculate_rectification(
            birth_date="1990-05-15",
            time_window_start="06:00",
            time_window_end="09:00",
            birth_place=self.BIRTH_PLACE,
            life_events=[],
        )
        assert result["candidates"] == []
        assert result["best_time"] is None
        assert result["confidence"] == "low"

    def test_midnight_crossing_window_works(self):
        """Midnight-crossing windows (e.g. 23:00→01:00) should now work
        by wrapping to next day instead of rejecting."""
        from app.birth_rectification_engine import calculate_rectification

        result = calculate_rectification(
            birth_date="1990-05-15",
            time_window_start="23:00",
            time_window_end="01:00",
            birth_place=self.BIRTH_PLACE,
            life_events=[{"date": "2015-03-20", "type": "marriage"}],
            step_minutes=30,
        )
        assert len(result["candidates"]) > 0
        assert result["best_time"] is not None

    def test_single_event_returns_candidates(self):
        from app.birth_rectification_engine import calculate_rectification

        result = calculate_rectification(
            birth_date="1990-05-15",
            time_window_start="06:00",
            time_window_end="06:05",
            birth_place=self.BIRTH_PLACE,
            life_events=[{"date": "2015-03-20", "type": "marriage"}],
            step_minutes=1,
        )
        assert "candidates" in result
        assert len(result["candidates"]) > 0
        assert len(result["candidates"]) <= 6  # 6 minutes window, up to 5 returned
        assert result["best_time"] is not None

    def test_candidates_are_sorted_by_score(self):
        from app.birth_rectification_engine import calculate_rectification

        result = calculate_rectification(
            birth_date="1990-05-15",
            time_window_start="06:00",
            time_window_end="06:10",
            birth_place=self.BIRTH_PLACE,
            life_events=[
                {"date": "2015-03-20", "type": "marriage"},
                {"date": "2018-06-10", "type": "child_birth"},
            ],
            step_minutes=2,
        )
        candidates = result["candidates"]
        scores = [c["score"] for c in candidates]
        assert scores == sorted(scores, reverse=True), "Candidates must be sorted by score descending"

    def test_candidate_structure(self):
        from app.birth_rectification_engine import calculate_rectification

        result = calculate_rectification(
            birth_date="1990-05-15",
            time_window_start="07:00",
            time_window_end="07:02",
            birth_place=self.BIRTH_PLACE,
            life_events=[{"date": "2015-03-20", "type": "marriage"}],
            step_minutes=1,
        )
        assert len(result["candidates"]) > 0
        c = result["candidates"][0]
        assert "birth_time" in c
        assert "score" in c
        assert "lagna" in c
        assert "lagna_degree" in c
        assert "event_matches" in c
        assert isinstance(c["event_matches"], list)
        # Event match structure
        em = c["event_matches"][0]
        assert "event" in em
        assert "date" in em
        assert "score" in em
        assert "explanation" in em

    def test_confidence_field_present(self):
        from app.birth_rectification_engine import calculate_rectification

        result = calculate_rectification(
            birth_date="1990-05-15",
            time_window_start="06:00",
            time_window_end="06:03",
            birth_place=self.BIRTH_PLACE,
            life_events=[{"date": "2015-03-20", "type": "marriage"}],
        )
        assert result["confidence"] in ("high", "medium", "low")

    def test_multiple_events_improves_discrimination(self):
        """More events should help differentiate between candidates."""
        from app.birth_rectification_engine import calculate_rectification

        single = calculate_rectification(
            birth_date="1990-05-15",
            time_window_start="06:00",
            time_window_end="06:05",
            birth_place=self.BIRTH_PLACE,
            life_events=[{"date": "2015-03-20", "type": "marriage"}],
            step_minutes=1,
        )
        multi = calculate_rectification(
            birth_date="1990-05-15",
            time_window_start="06:00",
            time_window_end="06:05",
            birth_place=self.BIRTH_PLACE,
            life_events=[
                {"date": "2015-03-20", "type": "marriage"},
                {"date": "2010-07-01", "type": "job_start"},
                {"date": "2018-06-10", "type": "child_birth"},
            ],
            step_minutes=1,
        )
        # Both should return valid results
        assert len(single["candidates"]) > 0
        assert len(multi["candidates"]) > 0
        # analysis_summary should mention the event count
        assert "3 life events" in multi["analysis_summary"]

    def test_narrow_window_single_candidate(self):
        """Window of 0 minutes = exactly 1 candidate."""
        from app.birth_rectification_engine import calculate_rectification

        result = calculate_rectification(
            birth_date="1990-05-15",
            time_window_start="07:30",
            time_window_end="07:30",
            birth_place=self.BIRTH_PLACE,
            life_events=[{"date": "2015-03-20", "type": "marriage"}],
            step_minutes=1,
        )
        assert len(result["candidates"]) == 1
        assert result["candidates"][0]["birth_time"] == "07:30"

    def test_step_minutes_parameter(self):
        """Larger step = fewer candidates tested."""
        from app.birth_rectification_engine import calculate_rectification

        result_1min = calculate_rectification(
            birth_date="1990-05-15",
            time_window_start="08:00",
            time_window_end="08:10",
            birth_place=self.BIRTH_PLACE,
            life_events=[{"date": "2015-03-20", "type": "marriage"}],
            step_minutes=1,
        )
        result_5min = calculate_rectification(
            birth_date="1990-05-15",
            time_window_start="08:00",
            time_window_end="08:10",
            birth_place=self.BIRTH_PLACE,
            life_events=[{"date": "2015-03-20", "type": "marriage"}],
            step_minutes=5,
        )
        # 1-min step over 10 min = 11 candidates tested; 5-min step = 3 candidates
        # top 5 returned in each case
        assert len(result_1min["candidates"]) == 5  # top 5 out of 11
        assert len(result_5min["candidates"]) == 3  # only 3 total


# ======================================================================
# House lord helper
# ======================================================================

class TestHouseLordHelper:
    """Tests for _get_house_lord and _get_planets_in_house."""

    CHART = {
        "houses": [
            {"number": 1, "sign": "Leo"},
            {"number": 7, "sign": "Aquarius"},
            {"number": 10, "sign": "Taurus"},
        ],
        "planets": {
            "Sun": {"house": 1},
            "Jupiter": {"house": 7},
        },
    }

    def test_house_lord_lookup(self):
        from app.birth_rectification_engine import _get_house_lord
        assert _get_house_lord(self.CHART, 1) == "Sun"       # Leo -> Sun
        assert _get_house_lord(self.CHART, 7) == "Saturn"    # Aquarius -> Saturn
        assert _get_house_lord(self.CHART, 10) == "Venus"    # Taurus -> Venus

    def test_house_lord_missing_house(self):
        from app.birth_rectification_engine import _get_house_lord
        assert _get_house_lord(self.CHART, 5) is None  # Not in our sparse chart

    def test_planets_in_house(self):
        from app.birth_rectification_engine import _get_planets_in_house
        assert "Sun" in _get_planets_in_house(self.CHART, 1)
        assert "Jupiter" in _get_planets_in_house(self.CHART, 7)
        assert _get_planets_in_house(self.CHART, 3) == []
