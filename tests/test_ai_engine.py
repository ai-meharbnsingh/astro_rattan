"""Tests for ai_engine.py — AI interpretation with OpenAI mocking + fallback tests."""
import pytest
from unittest.mock import patch, MagicMock
import os


# ============================================================
# Fallback Tests (no API key)
# ============================================================

def test_interpret_kundli_fallback_no_key():
    """When OPENAI_API_KEY is empty, should return fallback response."""
    with patch("app.ai_engine.OPENAI_API_KEY", ""):
        # Reset the cached client
        import app.ai_engine as ai
        ai._openai_client = None

        result = ai.ai_interpret_kundli({"Sun": "Leo", "Moon": "Scorpio"})
        assert "interpretation" in result
        assert "unavailable" in result["interpretation"].lower() or "api key" in result["interpretation"].lower()
        assert len(result["highlights"]) > 0
        assert len(result["warnings"]) > 0


def test_ask_question_fallback_no_key():
    """ai_ask_question should return fallback when no API key."""
    with patch("app.ai_engine.OPENAI_API_KEY", ""):
        import app.ai_engine as ai
        ai._openai_client = None

        result = ai.ai_ask_question("Will I get a promotion?")
        assert "answer" in result
        assert "reasoning" in result
        assert "fallback" in result["reasoning"].lower() or "unavailable" in result["answer"].lower()


def test_gita_answer_fallback_no_key():
    """ai_gita_answer should return default sloka when no API key."""
    with patch("app.ai_engine.OPENAI_API_KEY", ""):
        import app.ai_engine as ai
        ai._openai_client = None

        result = ai.ai_gita_answer("What is my duty?")
        assert "answer" in result
        assert "relevant_slokas" in result
        assert len(result["relevant_slokas"]) > 0
        # Should contain the default Chapter 2, Verse 47 sloka
        assert any("Chapter 2" in s for s in result["relevant_slokas"])


def test_remedies_fallback_no_key():
    """ai_remedies should return generic remedies when no API key."""
    with patch("app.ai_engine.OPENAI_API_KEY", ""):
        import app.ai_engine as ai
        ai._openai_client = None

        result = ai.ai_remedies({"Sun": "Leo"})
        assert "remedies" in result
        assert len(result["remedies"]) >= 3
        # Each remedy should have type, description, planet
        for remedy in result["remedies"]:
            assert "type" in remedy
            assert "description" in remedy
            assert "planet" in remedy


def test_oracle_fallback_no_key():
    """ai_oracle should return deterministic fallback when no API key."""
    with patch("app.ai_engine.OPENAI_API_KEY", ""):
        import app.ai_engine as ai
        ai._openai_client = None

        result = ai.ai_oracle("Will it rain tomorrow?", mode="yes_no")
        assert "answer" in result
        assert "reasoning" in result
        # The answer should be deterministic (based on question hash)
        answer1 = result["answer"]
        result2 = ai.ai_oracle("Will it rain tomorrow?", mode="yes_no")
        assert result2["answer"] == answer1  # Same question = same answer


# ============================================================
# Mocked OpenAI Tests
# ============================================================

def _mock_openai_response(content: str):
    """Create a mock OpenAI chat completion response."""
    mock_choice = MagicMock()
    mock_choice.message.content = content
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    return mock_response


def test_interpret_kundli_with_mocked_openai():
    """ai_interpret_kundli should parse OpenAI response correctly."""
    import app.ai_engine as ai

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = _mock_openai_response(
        "Your Sun in Leo shows strong leadership.\n"
        "HIGHLIGHT: Natural authority and charisma\n"
        "WARNING: Tendency toward ego conflicts\n"
        "Overall positive chart."
    )

    with patch("app.ai_engine.OPENAI_API_KEY", "test-key-123"):
        ai._openai_client = mock_client
        result = ai.ai_interpret_kundli({"Sun": "Leo", "Moon": "Cancer"})
        assert "Your Sun in Leo" in result["interpretation"]
        ai._openai_client = None  # cleanup


def test_oracle_yes_no_with_mocked_openai():
    """ai_oracle in yes_no mode should extract yes/no from response."""
    import app.ai_engine as ai

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = _mock_openai_response(
        "Yes, the stars favor this endeavor.\nJupiter's transit supports new beginnings."
    )

    with patch("app.ai_engine.OPENAI_API_KEY", "test-key-123"):
        ai._openai_client = mock_client
        result = ai.ai_oracle("Should I start a business?", mode="yes_no")
        assert "answer" in result
        assert "yes" in result["answer"].lower()
        ai._openai_client = None


def test_gita_answer_with_mocked_openai():
    """ai_gita_answer should extract slokas from response."""
    import app.ai_engine as ai

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = _mock_openai_response(
        "The Gita teaches us about duty and detachment.\n"
        "Chapter 2, Verse 47: Karmanye vadhikaraste — Focus on action, not results.\n"
        "Chapter 3, Verse 35: Shreyan svadharmo vigunah — Better is one's own dharma.\n"
        "Follow your dharma with dedication."
    )

    with patch("app.ai_engine.OPENAI_API_KEY", "test-key-123"):
        ai._openai_client = mock_client
        result = ai.ai_gita_answer("What should I focus on?")
        assert "answer" in result
        assert len(result["relevant_slokas"]) >= 2
        assert any("Chapter 2" in s for s in result["relevant_slokas"])
        ai._openai_client = None
