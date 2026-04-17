"""Tests for numerology_forecast_engine.py — Personal Year/Month/Day forecasts."""
import pytest
from datetime import date


# ── Unit tests: _reduce_to_single (imported from existing engine) ──

def test_reduce_basic():
    from app.numerology_engine import _reduce_to_single
    assert _reduce_to_single(10) == 1
    assert _reduce_to_single(28) == 1  # 2+8=10->1
    assert _reduce_to_single(7) == 7


def test_reduce_master_numbers():
    from app.numerology_engine import _reduce_to_single
    assert _reduce_to_single(11) == 11
    assert _reduce_to_single(22) == 22
    assert _reduce_to_single(33) == 33


# ── Personal Year ──

def test_personal_year_known_dob():
    """DOB May 15 + year 2026: 5 + 1+5 + 2+0+2+6 = 5+6+10=21 -> 3."""
    from app.numerology_forecast_engine import calculate_personal_year
    result = calculate_personal_year(birth_month=5, birth_day=15, year=2026)
    # 5 + (1+5) + (2+0+2+6) = 5 + 6 + 10 = 21 -> 2+1 = 3
    assert result == 3


def test_personal_year_another_dob():
    """DOB Jan 1 + year 2026: 1 + 1 + 10 = 12 -> 3."""
    from app.numerology_forecast_engine import calculate_personal_year
    result = calculate_personal_year(birth_month=1, birth_day=1, year=2026)
    # 1 + 1 + (2+0+2+6) = 1 + 1 + 10 = 12 -> 1+2 = 3
    assert result == 3


def test_personal_year_master_number_in_sum():
    """DOB Nov 9 + year 2009: 1+1 + 9 + 2+0+0+9 = 2+9+11 = 22 (master)."""
    from app.numerology_forecast_engine import calculate_personal_year
    result = calculate_personal_year(birth_month=11, birth_day=9, year=2009)
    # month digits: 1+1=2, day digits: 9, year digits: 2+0+0+9=11
    # sum: 2 + 9 + 11 = 22 (master number, preserved)
    assert result == 22


# ── Personal Month ──

def test_personal_month_basic():
    """PY=3, month=4 (April): 3 + 4 = 7."""
    from app.numerology_forecast_engine import calculate_personal_month
    result = calculate_personal_month(personal_year=3, month=4)
    assert result == 7


def test_personal_month_reduce():
    """PY=8, month=7: 8 + 7 = 15 -> 6."""
    from app.numerology_forecast_engine import calculate_personal_month
    result = calculate_personal_month(personal_year=8, month=7)
    assert result == 6


def test_personal_month_december():
    """PY=1, month=12: 1 + 1+2 = 4."""
    from app.numerology_forecast_engine import calculate_personal_month
    result = calculate_personal_month(personal_year=1, month=12)
    # 1 + (1+2) = 1 + 3 = 4
    assert result == 4


# ── Personal Day ──

def test_personal_day_basic():
    """PM=7, day=17: 7 + 1+7 = 15 -> 6."""
    from app.numerology_forecast_engine import calculate_personal_day
    result = calculate_personal_day(personal_month=7, day=17)
    # 7 + (1+7) = 7 + 8 = 15 -> 1+5 = 6
    assert result == 6


def test_personal_day_single_digit_day():
    """PM=4, day=5: 4 + 5 = 9."""
    from app.numerology_forecast_engine import calculate_personal_day
    result = calculate_personal_day(personal_month=4, day=5)
    assert result == 9


# ── Universal Year ──

def test_universal_year_2026():
    """2026: 2+0+2+6 = 10 -> 1."""
    from app.numerology_forecast_engine import calculate_universal_year
    assert calculate_universal_year(2026) == 1


def test_universal_year_2025():
    """2025: 2+0+2+5 = 9."""
    from app.numerology_forecast_engine import calculate_universal_year
    assert calculate_universal_year(2025) == 9


def test_universal_year_2018():
    """2018: 2+0+1+8 = 11 (master number preserved)."""
    from app.numerology_forecast_engine import calculate_universal_year
    assert calculate_universal_year(2018) == 11


# ── Universal Month ──

def test_universal_month():
    """UY=1 (2026), month=4 (April): 1 + 4 = 5."""
    from app.numerology_forecast_engine import calculate_universal_month
    assert calculate_universal_month(universal_year=1, month=4) == 5


# ── Universal Day ──

def test_universal_day():
    """UY=1, month=4, day=17: universal_month=5, 5+(1+7)=13->4."""
    from app.numerology_forecast_engine import calculate_universal_day
    result = calculate_universal_day(universal_year=1, month=4, day=17)
    # universal_month = reduce(1+4) = 5
    # 5 + (1+7) = 5 + 8 = 13 -> 1+3 = 4
    assert result == 4


# ── Main forecast function ──

def test_forecast_returns_all_fields():
    """calculate_forecast must return all personal + universal numbers and predictions."""
    from app.numerology_forecast_engine import calculate_forecast
    result = calculate_forecast("1990-05-15", "2026-04-17")
    required_keys = [
        "personal_year", "personal_month", "personal_day",
        "universal_year", "universal_month", "universal_day",
        "predictions",
    ]
    for key in required_keys:
        assert key in result, f"Missing key: {key}"
    # All numbers must be ints
    for key in required_keys[:-1]:
        assert isinstance(result[key], int), f"{key} must be int"


def test_forecast_predictions_structure():
    """Each prediction group has bilingual keys."""
    from app.numerology_forecast_engine import calculate_forecast
    result = calculate_forecast("1990-05-15", "2026-04-17")
    preds = result["predictions"]
    for section in ("personal_year", "personal_month", "personal_day"):
        assert section in preds, f"predictions missing {section}"
        pred = preds[section]
        for field in ("theme", "theme_hi", "description", "description_hi"):
            assert field in pred, f"predictions.{section} missing {field}"
            assert isinstance(pred[field], str)
            assert len(pred[field]) > 0


def test_forecast_personal_year_prediction_full_keys():
    """Personal year prediction must include all detailed keys."""
    from app.numerology_forecast_engine import calculate_forecast
    result = calculate_forecast("1990-05-15", "2026-04-17")
    py_pred = result["predictions"]["personal_year"]
    for field in ("theme", "theme_hi", "description", "description_hi",
                  "focus_areas", "focus_areas_hi", "advice", "advice_hi",
                  "lucky_months"):
        assert field in py_pred, f"personal_year prediction missing {field}"
    assert isinstance(py_pred["lucky_months"], list)
    assert len(py_pred["lucky_months"]) > 0


def test_forecast_default_target_date():
    """When target_date is None, it should use today's date."""
    from app.numerology_forecast_engine import calculate_forecast
    result = calculate_forecast("1990-05-15")
    today = date.today()
    assert result["universal_year"] == calculate_universal_year_from_module(today.year)
    assert isinstance(result["personal_year"], int)


def calculate_universal_year_from_module(year):
    """Helper to verify default date behavior."""
    from app.numerology_forecast_engine import calculate_universal_year
    return calculate_universal_year(year)


def test_forecast_values_correct():
    """Verify actual computed values for known inputs."""
    from app.numerology_forecast_engine import calculate_forecast
    result = calculate_forecast("1990-05-15", "2026-04-17")
    # PY: 5 + (1+5) + (2+0+2+6) = 5+6+10 = 21 -> 3
    assert result["personal_year"] == 3
    # PM: 3 + 4 = 7
    assert result["personal_month"] == 7
    # PD: 7 + (1+7) = 15 -> 6
    assert result["personal_day"] == 6
    # UY: 2+0+2+6 = 10 -> 1
    assert result["universal_year"] == 1
    # UM: 1 + 4 = 5
    assert result["universal_month"] == 5
    # UD: 5 + (1+7) = 13 -> 4
    assert result["universal_day"] == 4


# ── Prediction data completeness ──

def test_personal_year_predictions_all_numbers():
    """PERSONAL_YEAR_PREDICTIONS has entries for 1-9, 11, 22, 33."""
    from app.numerology_forecast_engine import PERSONAL_YEAR_PREDICTIONS
    expected_keys = {1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33}
    assert set(PERSONAL_YEAR_PREDICTIONS.keys()) == expected_keys


def test_personal_month_predictions_all_numbers():
    """PERSONAL_MONTH_PREDICTIONS has entries for 1-9."""
    from app.numerology_forecast_engine import PERSONAL_MONTH_PREDICTIONS
    expected_keys = {1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33}
    assert expected_keys.issubset(set(PERSONAL_MONTH_PREDICTIONS.keys()))


def test_personal_day_predictions_all_numbers():
    """PERSONAL_DAY_PREDICTIONS has entries for 1-9."""
    from app.numerology_forecast_engine import PERSONAL_DAY_PREDICTIONS
    expected_keys = {1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33}
    assert expected_keys.issubset(set(PERSONAL_DAY_PREDICTIONS.keys()))


def test_all_year_predictions_bilingual():
    """Every personal year prediction entry has bilingual keys."""
    from app.numerology_forecast_engine import PERSONAL_YEAR_PREDICTIONS
    required = {"theme", "theme_hi", "description", "description_hi",
                "focus_areas", "focus_areas_hi", "advice", "advice_hi",
                "lucky_months"}
    for num, pred in PERSONAL_YEAR_PREDICTIONS.items():
        for field in required:
            assert field in pred, f"Year {num} missing {field}"


def test_all_month_predictions_bilingual():
    """Every personal month prediction entry has bilingual keys."""
    from app.numerology_forecast_engine import PERSONAL_MONTH_PREDICTIONS
    required = {"theme", "theme_hi", "description", "description_hi"}
    for num, pred in PERSONAL_MONTH_PREDICTIONS.items():
        for field in required:
            assert field in pred, f"Month {num} missing {field}"


def test_all_day_predictions_bilingual():
    """Every personal day prediction entry has bilingual keys."""
    from app.numerology_forecast_engine import PERSONAL_DAY_PREDICTIONS
    required = {"theme", "theme_hi", "description", "description_hi"}
    for num, pred in PERSONAL_DAY_PREDICTIONS.items():
        for field in required:
            assert field in pred, f"Day {num} missing {field}"


# ── API route tests (lightweight — no DB required for forecast) ──

@pytest.fixture(scope="module")
def forecast_client():
    """Minimal TestClient using only the numerology router (no DB bootstrap)."""
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from app.routes.numerology import router
    app = FastAPI()
    app.include_router(router)
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


def test_forecast_api_success(forecast_client):
    """POST /api/numerology/forecast with valid data returns 200."""
    resp = forecast_client.post("/api/numerology/forecast", json={
        "birth_date": "1990-05-15",
        "target_date": "2026-04-17",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "personal_year" in data
    assert "predictions" in data


def test_forecast_api_no_target_date(forecast_client):
    """POST /api/numerology/forecast without target_date uses today."""
    resp = forecast_client.post("/api/numerology/forecast", json={
        "birth_date": "1990-05-15",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data["personal_year"], int)


def test_forecast_api_invalid_date(forecast_client):
    """POST /api/numerology/forecast with invalid birth_date returns 400."""
    resp = forecast_client.post("/api/numerology/forecast", json={
        "birth_date": "not-a-date",
    })
    assert resp.status_code == 400


def test_forecast_api_missing_birth_date(forecast_client):
    """POST /api/numerology/forecast without birth_date returns 422."""
    resp = forecast_client.post("/api/numerology/forecast", json={})
    assert resp.status_code == 422
