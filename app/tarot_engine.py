"""
tarot_engine.py — Tarot Card Engine
=====================================
Full 78-card deck: 22 Major Arcana + 56 Minor Arcana (4 suits x 14 cards).
Supports single, three-card, and Celtic Cross spreads.
"""
import hashlib
import random

# ============================================================
# MAJOR ARCANA — 22 cards
# ============================================================
MAJOR_ARCANA = [
    {"name": "The Fool", "number": 0,
     "meaning_upright": "New beginnings, innocence, spontaneity, free spirit",
     "meaning_reversed": "Recklessness, taken advantage of, inconsideration"},
    {"name": "The Magician", "number": 1,
     "meaning_upright": "Manifestation, resourcefulness, power, inspired action",
     "meaning_reversed": "Manipulation, poor planning, untapped talents"},
    {"name": "The High Priestess", "number": 2,
     "meaning_upright": "Intuition, sacred knowledge, divine feminine, the subconscious mind",
     "meaning_reversed": "Secrets, disconnected from intuition, withdrawal and silence"},
    {"name": "The Empress", "number": 3,
     "meaning_upright": "Femininity, beauty, nature, nurturing, abundance",
     "meaning_reversed": "Creative block, dependence on others, emptiness"},
    {"name": "The Emperor", "number": 4,
     "meaning_upright": "Authority, establishment, structure, father figure",
     "meaning_reversed": "Domination, excessive control, lack of discipline, inflexibility"},
    {"name": "The Hierophant", "number": 5,
     "meaning_upright": "Spiritual wisdom, religious beliefs, conformity, tradition",
     "meaning_reversed": "Personal beliefs, freedom, challenging the status quo"},
    {"name": "The Lovers", "number": 6,
     "meaning_upright": "Love, harmony, relationships, values alignment, choices",
     "meaning_reversed": "Self-love, disharmony, imbalance, misalignment of values"},
    {"name": "The Chariot", "number": 7,
     "meaning_upright": "Control, willpower, success, action, determination",
     "meaning_reversed": "Self-discipline, opposition, lack of direction"},
    {"name": "Strength", "number": 8,
     "meaning_upright": "Strength, courage, persuasion, influence, compassion",
     "meaning_reversed": "Inner strength, self-doubt, low energy, raw emotion"},
    {"name": "The Hermit", "number": 9,
     "meaning_upright": "Soul-searching, introspection, being alone, inner guidance",
     "meaning_reversed": "Isolation, loneliness, withdrawal"},
    {"name": "Wheel of Fortune", "number": 10,
     "meaning_upright": "Good luck, karma, life cycles, destiny, turning point",
     "meaning_reversed": "Bad luck, resistance to change, breaking cycles"},
    {"name": "Justice", "number": 11,
     "meaning_upright": "Justice, fairness, truth, cause and effect, law",
     "meaning_reversed": "Unfairness, lack of accountability, dishonesty"},
    {"name": "The Hanged Man", "number": 12,
     "meaning_upright": "Pause, surrender, letting go, new perspectives",
     "meaning_reversed": "Delays, resistance, stalling, indecision"},
    {"name": "Death", "number": 13,
     "meaning_upright": "Endings, change, transformation, transition",
     "meaning_reversed": "Resistance to change, personal transformation, inner purging"},
    {"name": "Temperance", "number": 14,
     "meaning_upright": "Balance, moderation, patience, purpose",
     "meaning_reversed": "Imbalance, excess, self-healing, re-alignment"},
    {"name": "The Devil", "number": 15,
     "meaning_upright": "Shadow self, attachment, addiction, restriction, sexuality",
     "meaning_reversed": "Releasing limiting beliefs, exploring dark thoughts, detachment"},
    {"name": "The Tower", "number": 16,
     "meaning_upright": "Sudden change, upheaval, chaos, revelation, awakening",
     "meaning_reversed": "Personal transformation, fear of change, averting disaster"},
    {"name": "The Star", "number": 17,
     "meaning_upright": "Hope, faith, purpose, renewal, spirituality",
     "meaning_reversed": "Lack of faith, despair, self-trust, disconnection"},
    {"name": "The Moon", "number": 18,
     "meaning_upright": "Illusion, fear, anxiety, subconscious, intuition",
     "meaning_reversed": "Release of fear, repressed emotion, inner confusion"},
    {"name": "The Sun", "number": 19,
     "meaning_upright": "Positivity, fun, warmth, success, vitality",
     "meaning_reversed": "Inner child, feeling down, overly optimistic"},
    {"name": "Judgement", "number": 20,
     "meaning_upright": "Judgement, rebirth, inner calling, absolution",
     "meaning_reversed": "Self-doubt, inner critic, ignoring the call"},
    {"name": "The World", "number": 21,
     "meaning_upright": "Completion, integration, accomplishment, travel",
     "meaning_reversed": "Seeking personal closure, short-cuts, delays"},
]

# ============================================================
# MINOR ARCANA — 56 cards (4 suits x 14)
# ============================================================
SUITS = ["Wands", "Cups", "Swords", "Pentacles"]
SUIT_ELEMENTS = {
    "Wands": "Fire", "Cups": "Water", "Swords": "Air", "Pentacles": "Earth",
}
RANK_NAMES = [
    "Ace", "Two", "Three", "Four", "Five", "Six", "Seven",
    "Eight", "Nine", "Ten", "Page", "Knight", "Queen", "King",
]

# Brief upright meanings per rank (applied across suits with suit flavor)
_RANK_MEANINGS_UPRIGHT = {
    "Ace": "new beginnings and raw potential",
    "Two": "balance, partnership, and early decisions",
    "Three": "growth, creativity, and collaboration",
    "Four": "stability, structure, and contemplation",
    "Five": "conflict, loss, and challenge",
    "Six": "harmony, generosity, and resolution",
    "Seven": "reflection, assessment, and perseverance",
    "Eight": "movement, speed, and mastery",
    "Nine": "culmination, attainment, and near-completion",
    "Ten": "completion, fulfillment, and endings",
    "Page": "curiosity, new messages, and youthful energy",
    "Knight": "action, adventure, and charged energy",
    "Queen": "nurturing mastery, intuition, and inner authority",
    "King": "leadership, command, and mature wisdom",
}

_RANK_MEANINGS_REVERSED = {
    "Ace": "missed opportunity, delays in new ventures",
    "Two": "indecision, disharmony, and withdrawal",
    "Three": "overextension, lack of teamwork, scattered efforts",
    "Four": "restlessness, instability, and stagnation",
    "Five": "recovery from conflict, compromise, and acceptance",
    "Six": "selfishness, imbalance, and unfairness",
    "Seven": "lack of purpose, distractions, and deception",
    "Eight": "slowness, frustration, and lack of progress",
    "Nine": "incompletion, disappointment, and suffering",
    "Ten": "burden, resistance to closure, and excess",
    "Page": "immaturity, lack of direction, and bad news",
    "Knight": "recklessness, haste, and scattered energy",
    "Queen": "insecurity, dependence, and smothering",
    "King": "tyranny, rigidity, and abuse of authority",
}

_SUIT_THEMES = {
    "Wands": "in the realm of passion, ambition, and willpower",
    "Cups": "in the realm of emotions, love, and relationships",
    "Swords": "in the realm of intellect, truth, and conflict",
    "Pentacles": "in the realm of material wealth, health, and work",
}


def _build_minor_arcana() -> list:
    """Build the 56 minor arcana cards."""
    cards = []
    for suit in SUITS:
        for i, rank in enumerate(RANK_NAMES):
            number = i + 1  # Ace=1, Two=2, ... King=14
            upright = f"{_RANK_MEANINGS_UPRIGHT[rank]} {_SUIT_THEMES[suit]}"
            reversed_m = f"{_RANK_MEANINGS_REVERSED[rank]} {_SUIT_THEMES[suit]}"
            cards.append({
                "name": f"{rank} of {suit}",
                "number": number,
                "suit": suit,
                "element": SUIT_ELEMENTS[suit],
                "meaning_upright": upright,
                "meaning_reversed": reversed_m,
            })
    return cards


MINOR_ARCANA = _build_minor_arcana()

# Full deck
FULL_DECK = MAJOR_ARCANA + MINOR_ARCANA

# Spread sizes
SPREAD_SIZES = {
    "single": 1,
    "three": 3,
    "celtic_cross": 10,
}

# Position names for each spread
SPREAD_POSITIONS = {
    "single": ["Guidance"],
    "three": ["Past", "Present", "Future"],
    "celtic_cross": [
        "Present", "Challenge", "Foundation", "Recent Past",
        "Crown", "Near Future", "Self", "Environment",
        "Hopes and Fears", "Outcome",
    ],
}


def draw_cards(spread: str, seed: int = None) -> list:
    """
    Draw cards for a given spread type.

    Args:
        spread: One of "single", "three", "celtic_cross"
        seed: Optional random seed for reproducibility

    Returns:
        List of card dicts with name, suit, number, is_reversed, meaning, position
    """
    if spread not in SPREAD_SIZES:
        raise ValueError(f"Unknown spread: {spread}. Choose from: {list(SPREAD_SIZES.keys())}")

    count = SPREAD_SIZES[spread]
    positions = SPREAD_POSITIONS[spread]

    rng = random.Random(seed)

    # Shuffle a copy of the full deck
    deck = list(FULL_DECK)
    rng.shuffle(deck)

    drawn = []
    for i in range(count):
        card = deck[i]
        is_reversed = rng.random() < 0.3  # 30% chance of reversal

        suit = card.get("suit", "Major Arcana")
        meaning = card["meaning_reversed"] if is_reversed else card["meaning_upright"]

        drawn.append({
            "name": card["name"],
            "suit": suit,
            "number": card["number"],
            "is_reversed": is_reversed,
            "meaning": meaning,
            "position": positions[i],
        })

    return drawn


def interpret_spread(cards: list, question: str = None) -> str:
    """
    Generate a textual interpretation of a drawn spread.

    Args:
        cards: List of card dicts from draw_cards()
        question: Optional question the querent is asking

    Returns:
        String interpretation of the spread
    """
    lines = []
    if question:
        lines.append(f"Question: {question}")
        lines.append("")

    lines.append(f"=== Tarot Reading ({len(cards)} card{'s' if len(cards) > 1 else ''}) ===")
    lines.append("")

    for card in cards:
        orientation = "Reversed" if card["is_reversed"] else "Upright"
        lines.append(f"[{card['position']}] {card['name']} ({orientation})")
        lines.append(f"  Suit: {card['suit']} | Number: {card['number']}")
        lines.append(f"  Meaning: {card['meaning']}")
        lines.append("")

    # Summary
    reversed_count = sum(1 for c in cards if c["is_reversed"])
    total = len(cards)

    if reversed_count > total / 2:
        energy = "The predominance of reversed cards suggests internal work, delays, or the need for reflection."
    elif reversed_count == 0:
        energy = "All cards are upright, indicating clear forward momentum and aligned energy."
    else:
        energy = "A balanced mix of upright and reversed cards points to a nuanced situation with both progress and challenges."

    lines.append(f"Overall Energy: {energy}")

    if question:
        lines.append(f"In answer to your question, the cards suggest looking at the interplay between "
                      f"{cards[0]['name']} and {cards[-1]['name']} for your primary guidance.")

    return "\n".join(lines)
