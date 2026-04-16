"""Tests for KP Horary (Prashna) 1-249 system in app.kp_engine."""
import pytest
from app.kp_engine import (
    KP_HORARY_TABLE,
    KP_SUB_LORDS,
    HORARY_QUESTION_HOUSES,
    SIGN_LORD_MAP,
    VIMSHOTTARI_SEQUENCE,
    get_horary_entry,
    calculate_kp_horary,
    get_horary_prediction,
    _degree_to_dms,
)


# ============================================================
# KP_HORARY_TABLE integrity tests
# ============================================================

class TestKPHoraryTable:
    """Validate the 249-entry KP Horary lookup table."""

    def test_table_has_249_entries(self):
        """The table must have exactly 249 entries (243 subs + 6 sign splits)."""
        assert len(KP_HORARY_TABLE) == 249

    def test_numbers_are_sequential_1_to_249(self):
        """Numbers must run 1, 2, 3, ... 249 without gaps."""
        for i, entry in enumerate(KP_HORARY_TABLE):
            assert entry["number"] == i + 1, (
                f"Entry {i} has number {entry['number']}, expected {i + 1}"
            )

    def test_first_entry(self):
        """Number 1 = start of Aries, Ketu star, Ketu sub."""
        e = KP_HORARY_TABLE[0]
        assert e["number"] == 1
        assert e["degree_start"] == 0.0
        assert e["sign"] == "Aries"
        assert e["star_lord"] == "Ketu"
        assert e["sub_lord"] == "Ketu"

    def test_last_entry(self):
        """Number 249 = ends at 360° in Pisces, Mercury star, Saturn sub.

        Revati nakshatra (lord=Mercury) sub sequence starts at Mercury and
        follows Vimshottari order: Mercury, Ketu, Venus, Sun, Moon, Mars,
        Rahu, Jupiter, Saturn. The 9th (last) sub is Saturn.
        """
        e = KP_HORARY_TABLE[-1]
        assert e["number"] == 249
        assert abs(e["degree_end"] - 360.0) < 0.01
        assert e["sign"] == "Pisces"
        assert e["star_lord"] == "Mercury"
        assert e["sub_lord"] == "Saturn"

    def test_entries_are_continuous(self):
        """No gaps: each entry's end must equal the next entry's start."""
        for i in range(len(KP_HORARY_TABLE) - 1):
            end = KP_HORARY_TABLE[i]["degree_end"]
            start_next = KP_HORARY_TABLE[i + 1]["degree_start"]
            assert abs(end - start_next) < 0.001, (
                f"Gap between entries {i+1} and {i+2}: "
                f"{end} != {start_next}"
            )

    def test_no_overlaps(self):
        """No entry should overlap with another."""
        for i in range(len(KP_HORARY_TABLE) - 1):
            assert KP_HORARY_TABLE[i]["degree_end"] <= KP_HORARY_TABLE[i + 1]["degree_start"] + 0.001

    def test_covers_full_zodiac(self):
        """First entry starts at 0°, last entry ends at 360°."""
        assert KP_HORARY_TABLE[0]["degree_start"] == 0.0
        assert abs(KP_HORARY_TABLE[-1]["degree_end"] - 360.0) < 0.01

    def test_all_12_signs_present(self):
        """All 12 zodiac signs must appear in the table."""
        signs_in_table = {e["sign"] for e in KP_HORARY_TABLE}
        expected_signs = {
            "Aries", "Taurus", "Gemini", "Cancer",
            "Leo", "Virgo", "Libra", "Scorpio",
            "Sagittarius", "Capricorn", "Aquarius", "Pisces",
        }
        assert signs_in_table == expected_signs

    def test_sign_lord_matches_sign(self):
        """Each entry's sign_lord must match the standard rulership."""
        for e in KP_HORARY_TABLE:
            expected_lord = SIGN_LORD_MAP[e["sign"]]
            assert e["sign_lord"] == expected_lord, (
                f"Number {e['number']}: sign={e['sign']} "
                f"expected lord={expected_lord}, got {e['sign_lord']}"
            )

    def test_star_lord_is_valid_planet(self):
        """Every star_lord must be one of the 9 Vimshottari planets."""
        valid = {name for name, _ in VIMSHOTTARI_SEQUENCE}
        for e in KP_HORARY_TABLE:
            assert e["star_lord"] in valid, (
                f"Number {e['number']}: invalid star_lord '{e['star_lord']}'"
            )

    def test_sub_lord_is_valid_planet(self):
        """Every sub_lord must be one of the 9 Vimshottari planets."""
        valid = {name for name, _ in VIMSHOTTARI_SEQUENCE}
        for e in KP_HORARY_TABLE:
            assert e["sub_lord"] in valid, (
                f"Number {e['number']}: invalid sub_lord '{e['sub_lord']}'"
            )

    def test_entries_within_correct_sign(self):
        """Every entry's degree range must lie within its stated sign."""
        for e in KP_HORARY_TABLE:
            sign_idx = [
                "Aries", "Taurus", "Gemini", "Cancer",
                "Leo", "Virgo", "Libra", "Scorpio",
                "Sagittarius", "Capricorn", "Aquarius", "Pisces",
            ].index(e["sign"])
            sign_start = sign_idx * 30.0
            sign_end = (sign_idx + 1) * 30.0
            assert e["degree_start"] >= sign_start - 0.001, (
                f"Number {e['number']}: starts at {e['degree_start']} "
                f"before sign {e['sign']} ({sign_start}°)"
            )
            assert e["degree_end"] <= sign_end + 0.001, (
                f"Number {e['number']}: ends at {e['degree_end']} "
                f"after sign {e['sign']} ({sign_end}°)"
            )

    def test_exactly_6_splits(self):
        """Splitting the 243 subs at sign boundaries must produce 249 = 243 + 6."""
        # This is more of a sanity check: 249 - 243 = 6 extra entries
        assert len(KP_HORARY_TABLE) - len(KP_SUB_LORDS) == 6

    def test_positive_spans(self):
        """Every entry must have a positive degree span."""
        for e in KP_HORARY_TABLE:
            span = e["degree_end"] - e["degree_start"]
            assert span > 0.0, (
                f"Number {e['number']}: zero or negative span "
                f"({e['degree_start']} to {e['degree_end']})"
            )


# ============================================================
# get_horary_entry tests
# ============================================================

class TestGetHoraryEntry:
    """Test the get_horary_entry() lookup function."""

    def test_valid_number_1(self):
        result = get_horary_entry(1)
        assert result["number"] == 1
        assert result["sign"] == "Aries"
        assert "degree_start_dms" in result
        assert "degree_end_dms" in result

    def test_valid_number_249(self):
        result = get_horary_entry(249)
        assert result["number"] == 249
        assert result["sign"] == "Pisces"

    def test_valid_number_mid(self):
        result = get_horary_entry(125)
        assert result["number"] == 125
        assert result["sign"] in {
            "Aries", "Taurus", "Gemini", "Cancer",
            "Leo", "Virgo", "Libra", "Scorpio",
            "Sagittarius", "Capricorn", "Aquarius", "Pisces",
        }

    def test_invalid_number_zero(self):
        with pytest.raises(ValueError, match="1-249"):
            get_horary_entry(0)

    def test_invalid_number_250(self):
        with pytest.raises(ValueError, match="1-249"):
            get_horary_entry(250)

    def test_invalid_number_negative(self):
        with pytest.raises(ValueError, match="1-249"):
            get_horary_entry(-5)

    def test_dms_format(self):
        """DMS strings should contain degree symbol."""
        result = get_horary_entry(42)
        assert "\u00b0" in result["degree_start_dms"]
        assert "'" in result["degree_start_dms"]


# ============================================================
# Degree-to-DMS utility tests
# ============================================================

class TestDegreeToDMS:
    """Test the _degree_to_dms helper."""

    def test_zero_degrees(self):
        assert _degree_to_dms(0.0) == "0\u00b000'00\""

    def test_integer_degrees(self):
        assert _degree_to_dms(90.0) == "90\u00b000'00\""

    def test_fractional_degrees(self):
        # 45.5 = 45° 30' 00"
        result = _degree_to_dms(45.5)
        assert result.startswith("45\u00b030'")

    def test_complex_degrees(self):
        # 123.456 deg = 123° 27' ~21.6"
        result = _degree_to_dms(123.456)
        assert result.startswith("123\u00b027'")


# ============================================================
# calculate_kp_horary tests
# ============================================================

class TestCalculateKPHorary:
    """Test the main horary chart calculation."""

    def test_returns_required_keys(self):
        result = calculate_kp_horary(42, "2024-06-15 10:30:00")
        required_keys = [
            "horary_number", "degree_range", "sign", "star_lord",
            "sub_lord", "ascendant", "house_cusps", "planets",
            "significators", "ruling_planets",
        ]
        for key in required_keys:
            assert key in result, f"Missing key: {key}"

    def test_horary_number_preserved(self):
        result = calculate_kp_horary(100, "2024-06-15")
        assert result["horary_number"] == 100

    def test_ascendant_within_degree_range(self):
        """Ascendant should be at the midpoint of the number's range."""
        result = calculate_kp_horary(42, "2024-06-15 10:30:00")
        deg_start = result["degree_range"]["start"]
        deg_end = result["degree_range"]["end"]
        expected_asc = (deg_start + deg_end) / 2.0
        assert abs(result["ascendant"] - expected_asc) < 0.01

    def test_house_cusps_has_12(self):
        result = calculate_kp_horary(1, "2024-01-01")
        assert len(result["house_cusps"]) == 12
        for h in range(1, 13):
            assert h in result["house_cusps"]
            assert 0 <= result["house_cusps"][h] < 360.0

    def test_planets_present(self):
        result = calculate_kp_horary(200, "2024-06-15 10:30:00")
        # At minimum Sun and Moon should be in the result
        assert "Sun" in result["planets"]
        assert "Moon" in result["planets"]

    def test_significators_present(self):
        result = calculate_kp_horary(150, "2024-06-15")
        assert "significators" in result
        assert len(result["significators"]) > 0

    def test_invalid_number(self):
        with pytest.raises(ValueError):
            calculate_kp_horary(0, "2024-01-01")
        with pytest.raises(ValueError):
            calculate_kp_horary(250, "2024-01-01")

    def test_degree_range_has_dms(self):
        result = calculate_kp_horary(42, "2024-06-15")
        assert "start_dms" in result["degree_range"]
        assert "end_dms" in result["degree_range"]

    def test_with_query_place(self):
        """Should not crash when query_place is provided."""
        place = {"latitude": 19.076, "longitude": 72.8777, "tz_offset": 5.5}
        result = calculate_kp_horary(42, "2024-06-15 10:30:00", query_place=place)
        assert result["horary_number"] == 42

    def test_different_numbers_give_different_ascendants(self):
        r1 = calculate_kp_horary(1, "2024-06-15")
        r2 = calculate_kp_horary(100, "2024-06-15")
        r3 = calculate_kp_horary(249, "2024-06-15")
        assert r1["ascendant"] != r2["ascendant"]
        assert r2["ascendant"] != r3["ascendant"]


# ============================================================
# get_horary_prediction tests
# ============================================================

class TestGetHoraryPrediction:
    """Test the prediction engine for various question types."""

    def test_returns_prediction_key(self):
        result = get_horary_prediction(42, "marriage", "2024-06-15 10:30:00")
        assert "prediction" in result

    def test_prediction_has_required_fields(self):
        result = get_horary_prediction(42, "marriage", "2024-06-15 10:30:00")
        pred = result["prediction"]
        required = [
            "question_type", "relevant_houses", "cusp_checked",
            "sub_lord_of_cusp", "verdict", "verdict_detail", "timing",
        ]
        for field in required:
            assert field in pred, f"Missing prediction field: {field}"

    def test_marriage_checks_7th_cusp(self):
        result = get_horary_prediction(42, "marriage", "2024-06-15")
        assert result["prediction"]["cusp_checked"] == 7
        assert result["prediction"]["relevant_houses"] == [2, 7, 11]

    def test_job_checks_10th_cusp(self):
        result = get_horary_prediction(100, "job", "2024-06-15")
        assert result["prediction"]["cusp_checked"] == 10

    def test_travel_checks_9th_cusp(self):
        result = get_horary_prediction(200, "travel", "2024-06-15")
        assert result["prediction"]["cusp_checked"] == 9

    def test_health_checks_1st_cusp(self):
        result = get_horary_prediction(50, "health", "2024-06-15")
        assert result["prediction"]["cusp_checked"] == 1

    def test_finance_checks_2nd_cusp(self):
        result = get_horary_prediction(75, "finance", "2024-06-15")
        assert result["prediction"]["cusp_checked"] == 2

    def test_legal_checks_6th_cusp(self):
        result = get_horary_prediction(130, "legal", "2024-06-15")
        assert result["prediction"]["cusp_checked"] == 6

    def test_education_checks_4th_cusp(self):
        result = get_horary_prediction(180, "education", "2024-06-15")
        assert result["prediction"]["cusp_checked"] == 4

    def test_property_checks_4th_cusp(self):
        result = get_horary_prediction(220, "property", "2024-06-15")
        assert result["prediction"]["cusp_checked"] == 4

    def test_verdict_is_valid(self):
        result = get_horary_prediction(42, "marriage", "2024-06-15")
        assert result["prediction"]["verdict"] in {
            "favorable", "unfavorable", "mixed", "neutral"
        }

    def test_sub_lord_of_cusp_is_valid_planet(self):
        valid_planets = {name for name, _ in VIMSHOTTARI_SEQUENCE}
        result = get_horary_prediction(42, "job", "2024-06-15")
        assert result["prediction"]["sub_lord_of_cusp"] in valid_planets

    def test_invalid_question_type(self):
        with pytest.raises(ValueError, match="Unknown question type"):
            get_horary_prediction(42, "lottery", "2024-06-15")

    def test_case_insensitive_question_type(self):
        """Question type should work regardless of case."""
        result = get_horary_prediction(42, "MARRIAGE", "2024-06-15")
        assert result["prediction"]["question_type"] == "marriage"

    def test_all_question_types_work(self):
        """Every supported question type should produce a valid result."""
        for qtype in HORARY_QUESTION_HOUSES:
            result = get_horary_prediction(42, qtype, "2024-06-15")
            assert "prediction" in result
            assert result["prediction"]["question_type"] == qtype


# ============================================================
# Mathematical accuracy tests
# ============================================================

class TestMathematicalAccuracy:
    """Verify the mathematical correctness of the 249 subdivisions."""

    def test_aries_entries_within_0_to_30(self):
        """All Aries entries must have degrees within [0, 30]."""
        aries_entries = [e for e in KP_HORARY_TABLE if e["sign"] == "Aries"]
        assert len(aries_entries) > 0
        for e in aries_entries:
            assert 0.0 <= e["degree_start"] < 30.0 + 0.001
            assert 0.0 < e["degree_end"] <= 30.0 + 0.001

    def test_pisces_entries_within_330_to_360(self):
        """All Pisces entries must have degrees within [330, 360]."""
        pisces_entries = [e for e in KP_HORARY_TABLE if e["sign"] == "Pisces"]
        assert len(pisces_entries) > 0
        for e in pisces_entries:
            assert 330.0 - 0.001 <= e["degree_start"]
            assert e["degree_end"] <= 360.0 + 0.001

    def test_total_span_is_360(self):
        """Sum of all entry spans must equal 360 degrees."""
        total = sum(
            e["degree_end"] - e["degree_start"]
            for e in KP_HORARY_TABLE
        )
        assert abs(total - 360.0) < 0.01, f"Total span = {total}, expected 360"

    def test_sign_boundary_splits(self):
        """Entries sharing the same star_lord+sub_lord that span a sign
        boundary should appear as two consecutive entries in different signs."""
        split_count = 0
        for i in range(len(KP_HORARY_TABLE) - 1):
            curr = KP_HORARY_TABLE[i]
            nxt = KP_HORARY_TABLE[i + 1]
            if (
                curr["star_lord"] == nxt["star_lord"]
                and curr["sub_lord"] == nxt["sub_lord"]
                and curr["sign"] != nxt["sign"]
            ):
                split_count += 1
                # Verify the boundary is at a sign cusp (multiple of 30)
                boundary = curr["degree_end"]
                assert abs(boundary % 30.0) < 0.001, (
                    f"Split at {boundary}° is not at a sign boundary"
                )
        assert split_count == 6, (
            f"Expected 6 sign-boundary splits, found {split_count}"
        )

    def test_each_sign_has_entries(self):
        """Count entries per sign — each sign should have ~20-21 entries."""
        from collections import Counter
        counts = Counter(e["sign"] for e in KP_HORARY_TABLE)
        for sign, count in counts.items():
            assert 18 <= count <= 23, (
                f"{sign} has {count} entries (expected 18-23)"
            )
