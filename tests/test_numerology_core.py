"""
Numerology engine core number tests — 5 manually verified numbers.
DOB: 1985-08-23 | Name: Meharban Singh
"""
import pytest
from app.numerology_engine import calculate_numerology, _life_path, _name_to_number, _vowels_number, _consonants_number, _maturity_number


DOB = "1985-08-23"
NAME = "Meharban Singh"


def test_life_path():
    # day=23→5, month=8→8, year=1+9+8+5=23→5, total=18→9
    assert _life_path(DOB) == 9


def test_destiny():
    # Pythagorean sum of MEHARBAN SINGH = 65 → master 11 preserved
    assert _name_to_number(NAME) == 11


def test_soul_urge():
    # Vowels E(5)+A(1)+A(1)+I(9) = 16, karmic debt 16 → 7
    assert _vowels_number(NAME) == 7


def test_personality():
    # Consonants M(4)+H(8)+R(9)+B(2)+N(5)+S(1)+N(5)+G(7)+H(8) = 49 → 13 → 4
    assert _consonants_number(NAME) == 4


def test_maturity():
    lp = _life_path(DOB)
    destiny = _name_to_number(NAME)
    # 9 + 11 = 20 → 2
    assert _maturity_number(lp, destiny) == 2


def test_master_11_preserved_in_destiny():
    # Destiny 11 must NOT be reduced to 2
    result = calculate_numerology(NAME, DOB)
    assert result["destiny"] == 11


def test_all_core_numbers_in_result():
    result = calculate_numerology(NAME, DOB)
    assert result["life_path"] == 9
    assert result["destiny"] == 11
    assert result["soul_urge"] == 7
    assert result["personality"] == 4
    assert result["maturity_number"] == 2


def test_focus_areas_are_lists():
    result = calculate_numerology(NAME, DOB)
    for key in ("life_path", "destiny", "soul_urge", "personality"):
        pred = result["predictions"].get(key, {})
        fa = pred.get("focus_areas")
        if fa is not None:
            assert isinstance(fa, list), f"{key}.focus_areas should be a list, got {type(fa)}"


def test_karmic_debts_present():
    result = calculate_numerology(NAME, DOB)
    debts = result["karmic_debts"]
    assert isinstance(debts, list)
    debt_numbers = {d["number"] for d in debts}
    assert 16 in debt_numbers, "Karmic debt 16 expected from soul_urge intermediary"
    assert 13 in debt_numbers, "Karmic debt 13 expected from personality intermediary"


def test_loshu_planes_have_interpretation():
    result = calculate_numerology(NAME, DOB)
    planes = result["loshu_planes"]
    for plane_key in ("mental", "emotional", "practical"):
        assert plane_key in planes
        assert "interpretation" in planes[plane_key], f"{plane_key} missing interpretation"


def test_personal_year_prediction_present():
    result = calculate_numerology(NAME, DOB)
    assert "personal_year" in result
    assert "personal_year_prediction" in result
    pred = result["personal_year_prediction"]
    assert isinstance(pred, dict)
    assert "theme" in pred
