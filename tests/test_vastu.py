"""Tests for app.vastu — Vastu Shastra engine calculations."""
import pytest


# ============================================================
# DATA INTEGRITY TESTS
# ============================================================
def test_devtas_count_is_45():
    """45 Devtas must exist in the data set — no more, no less."""
    from app.vastu.data import DEVTAS_45
    assert len(DEVTAS_45) == 45, f"Expected 45 devtas, got {len(DEVTAS_45)}"


def test_devtas_have_unique_ids():
    """Each devta must have a unique id from 1 to 45."""
    from app.vastu.data import DEVTAS_45
    ids = [d["id"] for d in DEVTAS_45]
    assert sorted(ids) == list(range(1, 46))


def test_devtas_have_required_fields():
    """Each devta must have all required fields with non-empty values."""
    from app.vastu.data import DEVTAS_45
    required_fields = [
        "id", "name", "name_hi", "zone", "zone_hi",
        "direction", "direction_hi", "element", "element_hi",
        "nature", "energy_type", "body_part", "body_part_hi",
        "mantra", "desc_en", "desc_hi",
    ]
    for d in DEVTAS_45:
        for field in required_fields:
            assert field in d, f"Devta {d.get('id', '?')} missing field '{field}'"
            assert d[field], f"Devta {d['id']} ({d.get('name', '?')}) has empty '{field}'"


def test_devtas_natures_are_valid():
    """Each devta nature must be one of the allowed values."""
    from app.vastu.data import DEVTAS_45
    allowed = {"supreme", "positive", "neutral", "negative", "fierce"}
    for d in DEVTAS_45:
        assert d["nature"] in allowed, f"Devta {d['name']} has invalid nature '{d['nature']}'"


def test_entrance_padas_count_is_32():
    """32 Entrance Padas must exist — 8 per cardinal direction."""
    from app.vastu.data import ENTRANCE_PADAS
    assert len(ENTRANCE_PADAS) == 32, f"Expected 32 padas, got {len(ENTRANCE_PADAS)}"


def test_entrance_padas_per_direction():
    """Each cardinal direction (N, E, S, W) must have exactly 8 padas."""
    from app.vastu.data import ENTRANCE_PADAS
    for direction in ("N", "E", "S", "W"):
        count = sum(1 for p in ENTRANCE_PADAS if p["direction"] == direction)
        assert count == 8, f"Direction {direction} has {count} padas, expected 8"


def test_entrance_pada_scores_range():
    """Each pada score must be between 1 and 5."""
    from app.vastu.data import ENTRANCE_PADAS
    for p in ENTRANCE_PADAS:
        assert 1 <= p["score"] <= 5, f"Pada {p['pada']} has score {p['score']}, expected 1-5"


def test_entrance_padas_have_bilingual_fields():
    """Each pada must have both English and Hindi name, quality, and effects."""
    from app.vastu.data import ENTRANCE_PADAS
    for p in ENTRANCE_PADAS:
        assert p["name"], f"Pada {p['pada']} has empty name"
        assert p["name_hi"], f"Pada {p['pada']} has empty name_hi"
        assert p["quality"], f"Pada {p['pada']} has empty quality"
        assert p["quality_hi"], f"Pada {p['pada']} has empty quality_hi"
        assert p["effects_en"], f"Pada {p['pada']} has empty effects_en"
        assert p["effects_hi"], f"Pada {p['pada']} has empty effects_hi"


def test_metal_remedies_cover_all_zones():
    """Metal remedies must cover all 8 directions plus Center."""
    from app.vastu.data import METAL_REMEDIES
    expected = {"N", "NE", "E", "SE", "S", "SW", "W", "NW", "Center"}
    assert set(METAL_REMEDIES.keys()) == expected


def test_color_therapy_covers_all_directions():
    """Color therapy must cover all 8 compass directions."""
    from app.vastu.data import COLOR_THERAPY
    expected = {"N", "NE", "E", "SE", "S", "SW", "W", "NW"}
    assert set(COLOR_THERAPY.keys()) == expected


def test_room_placement_has_minimum_rooms():
    """Room placement must cover at least 10 room types."""
    from app.vastu.data import ROOM_PLACEMENT
    assert len(ROOM_PLACEMENT) >= 10, f"Expected >= 10 room types, got {len(ROOM_PLACEMENT)}"


def test_room_placement_has_bilingual_tips():
    """Each room must have tips in both English and Hindi."""
    from app.vastu.data import ROOM_PLACEMENT
    for key, room in ROOM_PLACEMENT.items():
        assert len(room["tips_en"]) > 0, f"Room {key} has no English tips"
        assert len(room["tips_hi"]) > 0, f"Room {key} has no Hindi tips"
        assert len(room["tips_en"]) == len(room["tips_hi"]), \
            f"Room {key}: en has {len(room['tips_en'])} tips, hi has {len(room['tips_hi'])}"


# ============================================================
# MANDALA CALCULATION TESTS
# ============================================================
def test_mandala_residential_uses_8x8():
    """Residential buildings must use Manduka Mandala (8x8 = 64 squares)."""
    from app.vastu.engine import calculate_mandala
    result = calculate_mandala("residential")
    assert result["grid_size"] == 8
    assert result["total_squares"] == 64


def test_mandala_temple_uses_9x9():
    """Temple buildings must use Paramasayika Mandala (9x9 = 81 squares)."""
    from app.vastu.engine import calculate_mandala
    result = calculate_mandala("temple")
    assert result["grid_size"] == 9
    assert result["total_squares"] == 81


def test_mandala_returns_all_10_zones():
    """Mandala must return all 10 zones with devtas."""
    from app.vastu.engine import calculate_mandala
    result = calculate_mandala("residential")
    zones = result["zones"]
    expected_zones = {
        "Central", "Northeast", "East", "Southeast",
        "South", "Southwest", "West", "Northwest", "North", "Special",
    }
    assert set(zones.keys()) == expected_zones


def test_mandala_energy_balance_sums_to_45():
    """Energy balance positive + negative + neutral must equal 45."""
    from app.vastu.engine import calculate_mandala
    result = calculate_mandala("residential")
    eb = result["energy_balance"]
    total = eb["positive"] + eb["negative"] + eb["neutral"]
    assert total == 45, f"Energy balance sums to {total}, expected 45"


def test_mandala_body_mapping_has_9_parts():
    """Body mapping must include head, face, chest, navel, arms, legs, feet."""
    from app.vastu.engine import calculate_mandala
    result = calculate_mandala("residential")
    body = result["body_mapping"]
    expected = {"head", "face", "chest", "navel", "right_arm", "left_arm",
                "right_leg", "left_leg", "feet"}
    assert set(body.keys()) == expected


def test_mandala_positive_exceeds_negative():
    """In a balanced mandala, positive devtas must outnumber negative ones."""
    from app.vastu.engine import calculate_mandala
    result = calculate_mandala("residential")
    eb = result["energy_balance"]
    assert eb["positive"] > eb["negative"], \
        f"Positive ({eb['positive']}) should exceed negative ({eb['negative']})"


# ============================================================
# ENTRANCE ANALYSIS TESTS
# ============================================================
def test_entrance_n5_is_supreme():
    """N5 (Aditi pada) is the supreme entrance — must score 5/5."""
    from app.vastu.engine import analyze_entrance
    result = analyze_entrance("N5")
    assert result["quality"] == "SUPREME"
    assert result["score"] == 5
    assert result["pada_name"] == "Aditi"


def test_entrance_s3_is_challenge():
    """S3 (Yama pada) is most dangerous — must score 1/5 with remedies."""
    from app.vastu.engine import analyze_entrance
    result = analyze_entrance("S3")
    assert result["quality"] == "CHALLENGE"
    assert result["score"] == 1
    assert len(result["remedies"]) > 0  # must suggest remedies


def test_entrance_w8_is_excellent():
    """W8 (Pushpadant pada) is the best West entrance — must score 5/5."""
    from app.vastu.engine import analyze_entrance
    result = analyze_entrance("W8")
    assert result["quality"] == "EXCELLENT"
    assert result["score"] == 5


def test_entrance_returns_all_8_padas_in_direction():
    """Entrance analysis must return all 8 padas for comparison."""
    from app.vastu.engine import analyze_entrance
    result = analyze_entrance("N3")
    assert len(result["all_padas_in_direction"]) == 8


def test_entrance_bad_pada_generates_remedies():
    """Challenging entrance (score <= 2) must generate at least 3 remedies."""
    from app.vastu.engine import analyze_entrance
    result = analyze_entrance("S1")  # Vitatha — score 1
    assert result["score"] <= 2
    assert len(result["remedies"]) >= 3


def test_entrance_good_pada_no_remedies():
    """Good entrance (score >= 4) should not generate remedies."""
    from app.vastu.engine import analyze_entrance
    result = analyze_entrance("N5")  # Aditi — score 5
    assert result["remedies"] == [] or "remedies" not in result or len(result.get("remedies", [])) == 0


def test_entrance_has_ruling_devta():
    """Entrance analysis must include ruling devta with mantra."""
    from app.vastu.engine import analyze_entrance
    result = analyze_entrance("E3")  # Aditya pada (East Dikpala)
    devta = result["ruling_devta"]
    assert devta is not None
    assert devta["name"] == "Aditya"
    assert devta["zone"] == "East"
    assert "Om" in devta["mantra"]


# ============================================================
# REMEDIES TESTS
# ============================================================
def test_remedies_wealth_includes_kubera():
    """Wealth problem must include Kubera mantra in remedies."""
    from app.vastu.engine import suggest_remedies
    result = suggest_remedies(["wealth"])
    devta_names = [m["devta"] for m in result["mantras"]]
    assert "Kubera" in devta_names, f"Kubera not found in mantras: {devta_names}"


def test_remedies_health_includes_metals():
    """Health problem must suggest metal strip remedies."""
    from app.vastu.engine import suggest_remedies
    result = suggest_remedies(["health"])
    assert len(result["metal_strip_remedies"]) > 0


def test_remedies_health_includes_colors():
    """Health problem must suggest color therapy."""
    from app.vastu.engine import suggest_remedies
    result = suggest_remedies(["health"])
    assert len(result["color_therapy"]) > 0


def test_remedies_always_include_universal():
    """Any problem must include universal Vastu remedies (Brahma sthana, diya, etc)."""
    from app.vastu.engine import suggest_remedies
    result = suggest_remedies(["career"])
    universal = [r for r in result["general_remedies"] if r["category"] == "universal"]
    assert len(universal) >= 2


def test_remedies_relationship_includes_room_adjustments():
    """Relationship problem must suggest bedroom and living room adjustments."""
    from app.vastu.engine import suggest_remedies
    result = suggest_remedies(["relationship"])
    room_keys = [r["room"] for r in result["room_adjustments"]]
    assert "master_bedroom" in room_keys
    assert "living_room" in room_keys


def test_remedies_multiple_problems():
    """Multiple problems should produce more remedies than single problem."""
    from app.vastu.engine import suggest_remedies
    single = suggest_remedies(["wealth"])
    multi = suggest_remedies(["wealth", "health", "career"])
    single_total = len(single["metal_strip_remedies"]) + len(single["mantras"])
    multi_total = len(multi["metal_strip_remedies"]) + len(multi["mantras"])
    assert multi_total >= single_total


# ============================================================
# ROOM PLACEMENT TESTS
# ============================================================
def test_room_placement_kitchen_ideal_se():
    """Kitchen ideal direction must be Southeast (Agni zone)."""
    from app.vastu.engine import get_room_placement
    result = get_room_placement("kitchen")
    assert "SE" in result["ideal_directions"]


def test_room_placement_kitchen_avoid_ne():
    """Kitchen must avoid Northeast (spiritual zone — fire pollutes)."""
    from app.vastu.engine import get_room_placement
    result = get_room_placement("kitchen")
    assert "NE" in result["avoid_directions"]


def test_room_placement_master_bedroom_ideal_sw():
    """Master bedroom ideal direction must be Southwest (stability zone)."""
    from app.vastu.engine import get_room_placement
    result = get_room_placement("master_bedroom")
    assert "SW" in result["ideal_directions"]


def test_room_placement_pooja_ideal_ne():
    """Pooja room ideal direction must include Northeast (Ishanya)."""
    from app.vastu.engine import get_room_placement
    result = get_room_placement("pooja")
    assert "NE" in result["ideal_directions"]


def test_room_placement_all_returns_all_rooms():
    """Requesting all rooms must return 10 room types."""
    from app.vastu.engine import get_room_placement
    result = get_room_placement()
    assert result["total_room_types"] >= 10


def test_room_placement_staircase_avoid_ne():
    """Staircase must avoid Northeast (heavy structure blocks divine energy)."""
    from app.vastu.engine import get_room_placement
    result = get_room_placement("staircase")
    assert "NE" in result["avoid_directions"]


# ============================================================
# COMPLETE ANALYSIS TESTS
# ============================================================
def test_complete_analysis_returns_score():
    """Complete analysis must return a Vastu score between 10 and 100."""
    from app.vastu.engine import get_complete_vastu_analysis
    result = get_complete_vastu_analysis("residential", "N5")
    assert 10 <= result["score"] <= 100


def test_complete_analysis_excellent_entrance_high_score():
    """Supreme entrance (N5) with no problems should score >= 80."""
    from app.vastu.engine import get_complete_vastu_analysis
    result = get_complete_vastu_analysis("residential", "N5")
    assert result["score"] >= 80, f"Score {result['score']} should be >= 80 for N5 entrance"


def test_complete_analysis_bad_entrance_lower_score():
    """Challenging entrance (S3) should score lower than excellent entrance."""
    from app.vastu.engine import get_complete_vastu_analysis
    good = get_complete_vastu_analysis("residential", "N5")
    bad = get_complete_vastu_analysis("residential", "S3")
    assert bad["score"] < good["score"], \
        f"Bad entrance score ({bad['score']}) should be < good ({good['score']})"


def test_complete_analysis_includes_all_sections():
    """Complete analysis must include mandala, entrance, rooms, and score."""
    from app.vastu.engine import get_complete_vastu_analysis
    result = get_complete_vastu_analysis("residential", "N3", None, ["wealth"])
    assert "mandala" in result
    assert "entrance_analysis" in result
    assert "room_placement" in result
    assert "remedies" in result
    assert "score" in result
    assert "score_label_en" in result
    assert "score_label_hi" in result


# ============================================================
# DIRECTION HELPER TESTS
# ============================================================
def test_degrees_to_direction_north():
    """0 degrees and 360 degrees must map to North."""
    from app.vastu.engine import _degrees_to_direction
    assert _degrees_to_direction(0) == "N"
    assert _degrees_to_direction(350) == "N"
    assert _degrees_to_direction(10) == "N"


def test_degrees_to_direction_east():
    """90 degrees must map to East."""
    from app.vastu.engine import _degrees_to_direction
    assert _degrees_to_direction(90) == "E"


def test_degrees_to_direction_south():
    """180 degrees must map to South."""
    from app.vastu.engine import _degrees_to_direction
    assert _degrees_to_direction(180) == "S"


def test_degrees_to_direction_west():
    """270 degrees must map to West."""
    from app.vastu.engine import _degrees_to_direction
    assert _degrees_to_direction(270) == "W"


def test_degrees_to_direction_northeast():
    """45 degrees must map to Northeast."""
    from app.vastu.engine import _degrees_to_direction
    assert _degrees_to_direction(45) == "NE"


# ============================================================
# PADA INDEX — degree-based tests (not bypassing _direction_to_pada_index)
# ============================================================
def test_pada_index_due_north_is_n5():
    """0 degrees (due North) must map to N5 — center of the North wall."""
    from app.vastu.engine import _direction_to_pada_index
    idx = _direction_to_pada_index("N", 0.0)
    assert idx == 4, f"0° should be N5 (index 4), got N{idx+1}"


def test_pada_index_nw_corner_is_n1():
    """315 degrees (NW corner) must map to N1 — start of North wall."""
    from app.vastu.engine import _direction_to_pada_index
    idx = _direction_to_pada_index("N", 315.0)
    assert idx == 0, f"315° should be N1 (index 0), got N{idx+1}"


def test_pada_index_due_east_is_e5():
    """90 degrees (due East) must map to E5 — center of East wall."""
    from app.vastu.engine import _direction_to_pada_index
    idx = _direction_to_pada_index("E", 90.0)
    assert idx == 4, f"90° should be E5 (index 4), got E{idx+1}"


def test_pada_index_due_south_is_s5():
    """180 degrees (due South) must map to S5 — center of South wall."""
    from app.vastu.engine import _direction_to_pada_index
    idx = _direction_to_pada_index("S", 180.0)
    assert idx == 4, f"180° should be S5 (index 4), got S{idx+1}"


def test_pada_index_due_west_is_w5():
    """270 degrees (due West) must map to W5 — center of West wall."""
    from app.vastu.engine import _direction_to_pada_index
    idx = _direction_to_pada_index("W", 270.0)
    assert idx == 4, f"270° should be W5 (index 4), got W{idx+1}"


def test_pada_index_sequential_north():
    """North padas N1-N8 must map to sequential 11.25-degree slices from 315 to 45."""
    from app.vastu.engine import _direction_to_pada_index
    expected = [
        (316.0, 0),   # N1
        (327.0, 1),   # N2
        (338.0, 2),   # N3
        (349.0, 3),   # N4
        (5.0,   4),   # N5
        (16.0,  5),   # N6
        (23.0,  6),   # N7
        (34.0,  7),   # N8
    ]
    for deg, exp_idx in expected:
        idx = _direction_to_pada_index("N", deg)
        assert idx == exp_idx, f"{deg}° should be N{exp_idx+1}, got N{idx+1}"


def test_entrance_by_degrees_matches_pada():
    """Passing degrees to analyze_entrance should compute the correct pada."""
    from app.vastu.engine import analyze_entrance
    # 0° = due North = N5 (Aditi pada, supreme)
    result = analyze_entrance("N", 0.0)
    assert result["pada"] == "N5", f"0° North should be N5, got {result['pada']}"
    assert result["quality"] == "SUPREME"


def test_score_can_reach_excellent():
    """Score formula must be able to reach 'Excellent' (>=85) and 100."""
    from app.vastu.engine import get_complete_vastu_analysis
    result = get_complete_vastu_analysis("residential", "N5")
    assert result["score"] >= 85, f"N5 with no problems should score >= 85, got {result['score']}"
    assert result["score"] == 100, f"Best case should be 100, got {result['score']}"


def test_score_worst_case_still_positive():
    """Worst case (bad entrance + many problems) should still be >= 10."""
    from app.vastu.engine import get_complete_vastu_analysis
    result = get_complete_vastu_analysis("residential", "S3", None,
                                         ["wealth", "health", "career", "relationship", "sleep", "conflict"])
    assert result["score"] >= 10


def test_no_duplicate_devta_names():
    """All 45 devta names must be unique for correct pada-devta lookup."""
    from app.vastu.data import DEVTAS_45
    names = [d["name"] for d in DEVTAS_45]
    from collections import Counter
    dupes = {n: c for n, c in Counter(names).items() if c > 1}
    assert not dupes, f"Duplicate devta names found: {dupes}"
