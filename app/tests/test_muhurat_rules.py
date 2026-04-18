"""Tests for muhurat_rules.py"""
import pytest
from app.muhurat_rules import (
    MUHURAT_ACTIVITIES, MUHURAT_RULES, get_activity_info,
    get_activity_rules, get_all_activities, normalize_tithi_for_rules,
    check_day_favorable,
)

ALL_ACTIVITIES = list(MUHURAT_ACTIVITIES.keys())


class TestActivityMetadata:
    def test_nine_activities(self):
        # P1 extends activities beyond the original 9.
        assert len(MUHURAT_ACTIVITIES) >= 9

    def test_all_have_hindi_name(self):
        for key, info in MUHURAT_ACTIVITIES.items():
            assert info.get("name_hindi"), f"{key} missing name_hindi"

    def test_all_have_icon(self):
        for key, info in MUHURAT_ACTIVITIES.items():
            assert info.get("icon"), f"{key} missing icon"

    def test_all_have_description_hindi(self):
        for key, info in MUHURAT_ACTIVITIES.items():
            assert info.get("description_hindi"), f"{key} missing description_hindi"


class TestRules:
    @pytest.mark.parametrize("activity", ALL_ACTIVITIES)
    def test_has_rules(self, activity):
        assert activity in MUHURAT_RULES

    @pytest.mark.parametrize("activity", ALL_ACTIVITIES)
    def test_rules_have_required_keys(self, activity):
        rules = MUHURAT_RULES[activity]
        for key in ["favorable_tithis", "favorable_nakshatras", "favorable_weekdays",
                     "favorable_lagnas", "avoid_krishna_paksha", "avoid_conditions"]:
            assert key in rules, f"{activity} missing {key}"

    @pytest.mark.parametrize("activity", ALL_ACTIVITIES)
    def test_favorable_tithis_nonempty(self, activity):
        assert len(MUHURAT_RULES[activity]["favorable_tithis"]) > 0

    @pytest.mark.parametrize("activity", ALL_ACTIVITIES)
    def test_favorable_nakshatras_nonempty(self, activity):
        assert len(MUHURAT_RULES[activity]["favorable_nakshatras"]) > 0

    @pytest.mark.parametrize("activity", ALL_ACTIVITIES)
    def test_favorable_weekdays_nonempty(self, activity):
        assert len(MUHURAT_RULES[activity]["favorable_weekdays"]) > 0


class TestHelpers:
    def test_get_activity_info(self):
        info = get_activity_info("marriage")
        assert info["name"] == "Vivah Muhurat"
        assert "विवाह" in info["name_hindi"]

    def test_get_activity_rules(self):
        rules = get_activity_rules("marriage")
        assert "favorable_tithis" in rules

    def test_get_all_activities(self):
        activities = get_all_activities()
        assert len(activities) == len(MUHURAT_ACTIVITIES)
        assert all("key" in a for a in activities)


class TestNormalizeTithi:
    def test_shukla_unchanged(self):
        assert normalize_tithi_for_rules(5) == 5

    def test_purnima(self):
        assert normalize_tithi_for_rules(15) == 15

    def test_krishna_normalized(self):
        assert normalize_tithi_for_rules(16) == 1  # Krishna Pratipada
        assert normalize_tithi_for_rules(22) == 7  # Krishna Saptami

    def test_amavasya(self):
        assert normalize_tithi_for_rules(30) == 30


class TestCheckDayFavorable:
    def test_marriage_good_day(self):
        result = check_day_favorable("marriage", 2, "Shukla", "Rohini", 0, "Magha")
        assert result["favorable"] is True
        assert result["score"] > 50

    def test_marriage_bad_weekday(self):
        result = check_day_favorable("marriage", 2, "Shukla", "Rohini", 5)  # Saturday
        assert "Unfavorable weekday" in result["reasons_bad"]

    def test_mundan_krishna_avoided(self):
        result = check_day_favorable("mundan", 16, "Krishna", "Hasta", 0)
        assert "Krishna Paksha avoided" in result["reasons_bad"]

    def test_unknown_activity(self):
        result = check_day_favorable("nonexistent", 1, "Shukla", "Ashwini", 0)
        assert result["favorable"] is False
