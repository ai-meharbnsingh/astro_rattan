"""Tests for tarot_engine.py — Tarot card deck and spreads."""
import pytest


def test_major_arcana_count():
    """Major Arcana must have exactly 22 cards."""
    from app.tarot_engine import MAJOR_ARCANA
    assert len(MAJOR_ARCANA) == 22


def test_minor_arcana_count():
    """Minor Arcana must have exactly 56 cards (4 suits x 14)."""
    from app.tarot_engine import MINOR_ARCANA
    assert len(MINOR_ARCANA) == 56


def test_full_deck_78():
    """Full deck = 22 Major + 56 Minor = 78 cards."""
    from app.tarot_engine import FULL_DECK
    assert len(FULL_DECK) == 78


def test_major_arcana_structure():
    """Each Major Arcana card has required fields."""
    from app.tarot_engine import MAJOR_ARCANA
    for card in MAJOR_ARCANA:
        assert "name" in card
        assert "number" in card
        assert "meaning_upright" in card
        assert "meaning_reversed" in card
        assert isinstance(card["number"], int)


def test_minor_arcana_suits():
    """Minor Arcana covers all 4 suits with 14 cards each."""
    from app.tarot_engine import MINOR_ARCANA
    suit_counts = {}
    for card in MINOR_ARCANA:
        suit = card["suit"]
        suit_counts[suit] = suit_counts.get(suit, 0) + 1
    assert set(suit_counts.keys()) == {"Wands", "Cups", "Swords", "Pentacles"}
    for suit, count in suit_counts.items():
        assert count == 14, f"{suit} has {count} cards, expected 14"


def test_draw_single_card():
    """Single spread draws exactly 1 card."""
    from app.tarot_engine import draw_cards
    cards = draw_cards("single", seed=42)
    assert len(cards) == 1
    assert cards[0]["position"] == "Guidance"


def test_draw_three_card_spread():
    """Three-card spread draws 3 cards with past/present/future positions."""
    from app.tarot_engine import draw_cards
    cards = draw_cards("three", seed=42)
    assert len(cards) == 3
    positions = [c["position"] for c in cards]
    assert positions == ["Past", "Present", "Future"]


def test_draw_celtic_cross():
    """Celtic Cross spread draws 10 cards."""
    from app.tarot_engine import draw_cards
    cards = draw_cards("celtic_cross", seed=42)
    assert len(cards) == 10


def test_draw_deterministic_with_seed():
    """Same seed produces identical draws."""
    from app.tarot_engine import draw_cards
    draw1 = draw_cards("three", seed=99)
    draw2 = draw_cards("three", seed=99)
    assert [c["name"] for c in draw1] == [c["name"] for c in draw2]
    assert [c["is_reversed"] for c in draw1] == [c["is_reversed"] for c in draw2]


def test_draw_invalid_spread():
    """Invalid spread type raises ValueError."""
    from app.tarot_engine import draw_cards
    with pytest.raises(ValueError):
        draw_cards("invalid_spread")


def test_card_structure():
    """Each drawn card has all required fields."""
    from app.tarot_engine import draw_cards
    cards = draw_cards("three", seed=42)
    for card in cards:
        assert "name" in card
        assert "suit" in card
        assert "number" in card
        assert "is_reversed" in card
        assert "meaning" in card
        assert "position" in card
        assert isinstance(card["is_reversed"], bool)


def test_interpret_spread():
    """interpret_spread returns a non-empty string."""
    from app.tarot_engine import draw_cards, interpret_spread
    cards = draw_cards("three", seed=42)
    interpretation = interpret_spread(cards, question="Will I succeed?")
    assert isinstance(interpretation, str)
    assert "Will I succeed?" in interpretation
    assert len(interpretation) > 50
