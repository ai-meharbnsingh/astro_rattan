"""
ai_engine.py — AI-Powered Vedic Astrology Interpretation Engine
================================================================
Supports TWO AI providers:
  1. Google Gemini (FREE tier — recommended for testing)
  2. OpenAI GPT-4 (paid — production quality)

Auto-detects: if GEMINI_API_KEY is set → uses Gemini. If OPENAI_API_KEY → uses OpenAI.
Set AI_PROVIDER=gemini|openai to force a specific provider.
"""
import os
import json
from typing import Optional

try:
    from app.config import (
        AI_PROVIDER, OPENAI_API_KEY, OPENAI_MODEL,
        GEMINI_API_KEY, GEMINI_MODEL,
    )
except ImportError:
    AI_PROVIDER = os.getenv("AI_PROVIDER", "auto")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")


# ============================================================
# Provider detection
# ============================================================
def _detect_provider() -> str:
    """Detect which AI provider to use. Priority: explicit > gemini > openai."""
    if AI_PROVIDER in ("gemini", "openai"):
        return AI_PROVIDER
    # Auto-detect: prefer Gemini (free) over OpenAI (paid)
    if GEMINI_API_KEY:
        return "gemini"
    if OPENAI_API_KEY:
        return "openai"
    return "none"


def _get_provider() -> str:
    """Lazy provider detection — re-reads config each time until a provider is found."""
    # Re-import to pick up .env changes
    from app.config import AI_PROVIDER as _ap, GEMINI_API_KEY as _gk, OPENAI_API_KEY as _ok
    if _ap in ("gemini", "openai"):
        return _ap
    if _gk:
        return "gemini"
    if _ok:
        return "openai"
    return "none"

# ============================================================
# Gemini client
# ============================================================
_gemini_model = None


_gemini_client = None


def _get_gemini():
    """Get or create the Gemini client. Returns None if no key."""
    global _gemini_client
    from app.config import GEMINI_API_KEY as _gk
    if not _gk:
        return None
    if _gemini_client is None:
        try:
            from google import genai
            _gemini_client = genai.Client(api_key=_gk)
        except Exception:
            return None
    return _gemini_client


def _call_gemini(system_prompt: str, user_prompt: str, temperature: float = 0.7) -> Optional[str]:
    """Call Google Gemini API using the new google-genai package."""
    client = _get_gemini()
    if client is None:
        return None
    try:
        from google.genai import types
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=full_prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=2000,
            ),
        )
        return response.text
    except Exception as e:
        return None


# ============================================================
# OpenAI client
# ============================================================
_openai_client = None


def _get_openai():
    """Get or create the OpenAI client. Returns None if no API key."""
    global _openai_client
    if not OPENAI_API_KEY:
        return None
    if _openai_client is None:
        try:
            import openai
            _openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
        except Exception:
            return None
    return _openai_client


def _call_openai(system_prompt: str, user_prompt: str, temperature: float = 0.7) -> Optional[str]:
    """Call OpenAI chat completion API."""
    client = _get_openai()
    if client is None:
        return None
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except Exception:
        return None


# ============================================================
# Unified AI caller — routes to active provider
# ============================================================
def _call_ai(system_prompt: str, user_prompt: str, temperature: float = 0.7) -> Optional[str]:
    """
    Call the active AI provider. Tries primary, falls back to secondary.
    Gemini (free) → OpenAI (paid) → None (fallback response).
    """
    provider = _get_provider()

    if provider == "gemini":
        result = _call_gemini(system_prompt, user_prompt, temperature)
        if result:
            return result
        # Fallback to OpenAI if Gemini fails
        return _call_openai(system_prompt, user_prompt, temperature)

    elif provider == "openai":
        result = _call_openai(system_prompt, user_prompt, temperature)
        if result:
            return result
        # Fallback to Gemini if OpenAI fails
        return _call_gemini(system_prompt, user_prompt, temperature)

    return None  # No provider available


def _fallback_response(context: str) -> str:
    """Generate a fallback response when no AI provider is available."""
    return (
        f"AI interpretation is currently unavailable (no API key configured). "
        f"Context: {context}. "
        "Please configure GEMINI_API_KEY (free) or OPENAI_API_KEY in your environment."
    )


def get_ai_status() -> dict:
    """Return current AI provider status — useful for health check / admin."""
    return {
        "provider": _get_provider(),
        "gemini_configured": bool(GEMINI_API_KEY),
        "openai_configured": bool(OPENAI_API_KEY),
        "gemini_model": GEMINI_MODEL if GEMINI_API_KEY else None,
        "openai_model": OPENAI_MODEL if OPENAI_API_KEY else None,
    }


# ============================================================
# PUBLIC API
# ============================================================

def ai_interpret_kundli(chart_data: dict) -> dict:
    """
    AI interpretation of a Vedic birth chart (kundli).

    Args:
        chart_data: Dict with planet positions, dashas, houses, etc.

    Returns:
        {interpretation: str, highlights: [str], warnings: [str]}
    """
    system_prompt = (
        "You are an expert Vedic astrologer (Jyotishi). Analyze the provided birth chart data "
        "and give a comprehensive interpretation. Include personality traits, career guidance, "
        "relationship insights, and spiritual path. Use traditional Vedic astrology concepts "
        "(rashis, nakshatras, dashas, yogas). Be insightful but accessible."
    )

    chart_str = json.dumps(chart_data, indent=2, default=str)
    user_prompt = f"Interpret this Vedic birth chart:\n\n{chart_str}"

    response = _call_ai(system_prompt, user_prompt, temperature=0.6)

    if response is None:
        return {
            "interpretation": _fallback_response("kundli interpretation"),
            "highlights": ["AI features require OPENAI_API_KEY configuration"],
            "warnings": ["No API key configured — using fallback response"],
        }

    # Parse highlights and warnings from response
    highlights = []
    warnings = []
    lines = response.split("\n")
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("HIGHLIGHT:") or stripped.startswith("- Strength:"):
            highlights.append(stripped.replace("HIGHLIGHT:", "").strip())
        elif stripped.startswith("WARNING:") or stripped.startswith("- Caution:"):
            warnings.append(stripped.replace("WARNING:", "").strip())

    if not highlights:
        highlights = ["Full interpretation provided — review the text for details."]
    if not warnings:
        warnings = []

    return {
        "interpretation": response,
        "highlights": highlights,
        "warnings": warnings,
    }


def ai_ask_question(question: str, chart_data: dict = None) -> dict:
    """
    Ask any astrology-related question, optionally with chart context.

    Args:
        question: The user's question.
        chart_data: Optional chart data for personalized answer.

    Returns:
        {answer: str, reasoning: str}
    """
    system_prompt = (
        "You are an expert Vedic astrologer. Answer the question using Vedic astrology principles. "
        "Provide clear reasoning based on planetary positions, dashas, and yogas where applicable. "
        "If chart data is provided, personalize your answer to that chart."
    )

    if chart_data:
        chart_str = json.dumps(chart_data, indent=2, default=str)
        user_prompt = f"Chart data:\n{chart_str}\n\nQuestion: {question}"
    else:
        user_prompt = f"Question: {question}"

    response = _call_ai(system_prompt, user_prompt)

    if response is None:
        return {
            "answer": _fallback_response(f"question: {question}"),
            "reasoning": "Fallback — AI unavailable. Configure OPENAI_API_KEY.",
        }

    return {
        "answer": response,
        "reasoning": "Based on Vedic astrology principles and planetary analysis.",
    }


def ai_gita_answer(question: str) -> dict:
    """
    Answer a life question using Bhagavad Gita wisdom.

    Args:
        question: A life question or dilemma.

    Returns:
        {answer: str, relevant_slokas: [str]}
    """
    system_prompt = (
        "You are a scholar of the Bhagavad Gita. Answer the user's question using wisdom from "
        "the Gita. Reference specific chapters and verses (slokas) where relevant. "
        "Provide the Sanskrit transliteration and English meaning. "
        "Format slokas as: 'Chapter X, Verse Y: [Sanskrit transliteration] — [English meaning]'"
    )

    user_prompt = f"Life question: {question}"

    response = _call_ai(system_prompt, user_prompt, temperature=0.5)

    if response is None:
        return {
            "answer": _fallback_response(f"Gita question: {question}"),
            "relevant_slokas": [
                "Chapter 2, Verse 47: Karmanye vadhikaraste ma phaleshu kadachana — "
                "You have the right to perform your duty, but not to the fruits of action. (Default sloka)"
            ],
        }

    # Extract slokas from response
    slokas = []
    for line in response.split("\n"):
        stripped = line.strip()
        if "Chapter" in stripped and "Verse" in stripped:
            slokas.append(stripped.lstrip("- ").lstrip("* "))

    if not slokas:
        slokas = ["See the full answer for referenced slokas."]

    return {
        "answer": response,
        "relevant_slokas": slokas,
    }


def ai_remedies(chart_data: dict) -> dict:
    """
    Get personalized Vedic remedies based on chart analysis.

    Args:
        chart_data: Dict with planet positions, doshas, weak planets, etc.

    Returns:
        {remedies: [{type, description, planet}]}
    """
    system_prompt = (
        "You are a Vedic astrologer specializing in remedies (upayas). Based on the chart data, "
        "suggest specific remedies for weak or afflicted planets. Include: gemstones, mantras, "
        "charity/donation, fasting, temple visits, and lifestyle changes. "
        "Format each remedy as JSON: {\"type\": \"...\", \"description\": \"...\", \"planet\": \"...\"}"
    )

    chart_str = json.dumps(chart_data, indent=2, default=str)
    user_prompt = f"Suggest Vedic remedies for this chart:\n\n{chart_str}"

    response = _call_ai(system_prompt, user_prompt, temperature=0.5)

    if response is None:
        # Return generic remedies as fallback
        return {
            "remedies": [
                {"type": "mantra", "description": "Recite Gayatri Mantra daily at sunrise for general spiritual upliftment.", "planet": "Sun"},
                {"type": "charity", "description": "Donate food on Saturdays to appease Saturn.", "planet": "Saturn"},
                {"type": "gemstone", "description": "Consult an astrologer for personalized gemstone recommendation.", "planet": "General"},
                {"type": "lifestyle", "description": "Practice meditation and pranayama for mental clarity.", "planet": "Moon"},
            ],
        }

    # Try to parse structured remedies from response
    remedies = []
    try:
        # Look for JSON arrays in the response
        start = response.find("[")
        end = response.rfind("]") + 1
        if start >= 0 and end > start:
            parsed = json.loads(response[start:end])
            if isinstance(parsed, list):
                for item in parsed:
                    if isinstance(item, dict) and "type" in item and "description" in item:
                        remedies.append({
                            "type": item.get("type", "general"),
                            "description": item.get("description", ""),
                            "planet": item.get("planet", "General"),
                        })
    except (json.JSONDecodeError, TypeError):
        pass

    if not remedies:
        # Parse line by line if JSON parsing failed
        remedies = [{
            "type": "interpretation",
            "description": response,
            "planet": "General",
        }]

    return {"remedies": remedies}


def ai_oracle(question: str, mode: str = "yes_no") -> dict:
    """
    AI Oracle — mystical answers to yes/no or open-ended questions.

    Args:
        question: The user's question.
        mode: "yes_no" for binary answer, "open" for detailed guidance.

    Returns:
        {answer: str, reasoning: str}
    """
    if mode == "yes_no":
        system_prompt = (
            "You are a Vedic oracle (Prashna Jyotish practitioner). Answer the question with "
            "YES or NO first, then provide brief astrological reasoning based on current planetary "
            "transits and cosmic energy. Keep the answer mystical but grounded in Jyotish."
        )
    else:
        system_prompt = (
            "You are a Vedic oracle and spiritual guide. Provide deep, insightful guidance on "
            "the question using a blend of Vedic astrology, Gita wisdom, and karmic understanding. "
            "Be mystical, poetic, and wise."
        )

    user_prompt = f"Oracle question ({mode} mode): {question}"

    response = _call_ai(system_prompt, user_prompt, temperature=0.8)

    if response is None:
        if mode == "yes_no":
            # Deterministic fallback based on question hash
            q_hash = sum(ord(c) for c in question) % 2
            answer = "Yes — the cosmic energies align in your favor." if q_hash == 0 else "No — the stars suggest patience and reflection."
        else:
            answer = _fallback_response(f"oracle question: {question}")

        return {
            "answer": answer,
            "reasoning": "Fallback oracle — AI unavailable. Based on cosmic numerology of your question.",
        }

    # Extract yes/no if in yes_no mode
    if mode == "yes_no":
        first_line = response.strip().split("\n")[0].lower()
        if "yes" in first_line:
            reasoning = "The oracle says YES. " + response
        elif "no" in first_line:
            reasoning = "The oracle says NO. " + response
        else:
            reasoning = response
    else:
        reasoning = response

    return {
        "answer": response,
        "reasoning": reasoning,
    }
