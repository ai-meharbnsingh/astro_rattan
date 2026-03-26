"""Tests for prashnavali_engine.py — Sacred Oracle Engine."""
import pytest


def test_ram_shalaka_grid_dimensions():
    """RAM_SHALAKA_GRID must be 15x15."""
    from app.prashnavali_engine import RAM_SHALAKA_GRID
    assert len(RAM_SHALAKA_GRID) == 15
    for row in RAM_SHALAKA_GRID:
        assert len(row) == 15


def test_hanuman_chaupai_count():
    """HANUMAN_CHAUPAI must have exactly 40 entries."""
    from app.prashnavali_engine import HANUMAN_CHAUPAI
    assert len(HANUMAN_CHAUPAI) == 40


def test_gita_slokas_oracle_count():
    """GITA_SLOKAS_ORACLE must have exactly 50 entries."""
    from app.prashnavali_engine import GITA_SLOKAS_ORACLE
    assert len(GITA_SLOKAS_ORACLE) == 50


def test_ram_shalaka_valid_cell():
    """ram_shalaka returns a valid result for a valid cell."""
    from app.prashnavali_engine import ram_shalaka
    result = ram_shalaka(0, 0)
    assert "syllable" in result
    assert "answer" in result
    assert "verse" in result
    assert "meaning" in result
    assert isinstance(result["answer"], str)
    assert len(result["meaning"]) > 10


def test_ram_shalaka_invalid_cell():
    """ram_shalaka raises ValueError for out-of-range indices."""
    from app.prashnavali_engine import ram_shalaka
    with pytest.raises(ValueError):
        ram_shalaka(15, 0)
    with pytest.raises(ValueError):
        ram_shalaka(0, 15)
    with pytest.raises(ValueError):
        ram_shalaka(-1, 0)


def test_hanuman_prashna_structure():
    """hanuman_prashna returns required keys."""
    from app.prashnavali_engine import hanuman_prashna
    result = hanuman_prashna("Will I get the job?")
    assert "answer" in result
    assert "chaupai" in result
    assert "meaning" in result
    assert isinstance(result["answer"], str)
    assert isinstance(result["chaupai"], str)
    assert len(result["meaning"]) > 10


def test_hanuman_prashna_deterministic():
    """Same question on same day returns same answer."""
    from app.prashnavali_engine import hanuman_prashna
    r1 = hanuman_prashna("Will I pass the exam?")
    r2 = hanuman_prashna("Will I pass the exam?")
    assert r1["chaupai"] == r2["chaupai"]
    assert r1["answer"] == r2["answer"]


def test_ramcharitmanas_prashna_structure():
    """ramcharitmanas_prashna returns required keys."""
    from app.prashnavali_engine import ramcharitmanas_prashna
    result = ramcharitmanas_prashna("Should I travel?")
    assert "answer" in result
    assert "verse" in result
    assert "meaning" in result
    assert isinstance(result["answer"], str)


def test_gita_prashna_structure():
    """gita_prashna returns required keys."""
    from app.prashnavali_engine import gita_prashna
    result = gita_prashna("What is my purpose?")
    assert "answer" in result
    assert "sloka" in result
    assert "meaning" in result
    assert isinstance(result["answer"], str)
    assert len(result["sloka"]) > 5


def test_gita_prashna_deterministic():
    """Same question on same day returns same sloka."""
    from app.prashnavali_engine import gita_prashna
    r1 = gita_prashna("Should I change careers?")
    r2 = gita_prashna("Should I change careers?")
    assert r1["sloka"] == r2["sloka"]
    assert r1["answer"] == r2["answer"]


def test_different_questions_different_answers():
    """Different questions should (very likely) yield different answers."""
    from app.prashnavali_engine import gita_prashna
    r1 = gita_prashna("Should I marry?")
    r2 = gita_prashna("Should I start a business?")
    # Different questions almost certainly select different slokas
    # (hash collision on 50 items is astronomically unlikely for different inputs)
    # We check that at least one field differs
    assert r1["sloka"] != r2["sloka"] or r1["answer"] != r2["answer"]
