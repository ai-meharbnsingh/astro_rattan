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
import traceback
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
# Gemini client (raw httpx — no google-genai SDK needed)
# ============================================================

def _call_gemini(system_prompt: str, user_prompt: str, temperature: float = 0.7) -> Optional[str]:
    """Call Google Gemini API via raw HTTP (no SDK dependency)."""
    from app.config import GEMINI_API_KEY as _gk
    if not _gk:
        return None
    try:
        import httpx
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        resp = httpx.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent",
            params={"key": _gk},
            json={
                "contents": [{"parts": [{"text": full_prompt}]}],
                "generationConfig": {"temperature": temperature, "maxOutputTokens": 2000},
            },
            timeout=60.0,
        )
        resp.raise_for_status()
        return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"ERROR in _call_gemini: {e}")
        print(traceback.format_exc())
        return None


# ============================================================
# OpenAI client (raw httpx — no openai SDK needed)
# ============================================================

def _call_openai(system_prompt: str, user_prompt: str, temperature: float = 0.7) -> Optional[str]:
    """Call OpenAI chat completion API via raw HTTP (no SDK dependency)."""
    if not OPENAI_API_KEY:
        return None
    try:
        import httpx
        resp = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            json={
                "model": OPENAI_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": temperature,
                "max_tokens": 2000,
            },
            timeout=60.0,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"ERROR in _call_openai: {e}")
        print(traceback.format_exc())
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


def get_active_model_label() -> str:
    """Return the model name string for the currently active provider.

    Used by AI chat-log inserts so ``model_used`` reflects the real
    provider/model rather than a hardcoded ``'gpt-4'``.
    """
    provider = _get_provider()
    if provider == "gemini":
        return GEMINI_MODEL
    if provider == "openai":
        return OPENAI_MODEL
    return "none"


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
# RULE-BASED INTERPRETATION (fallback when no AI API key)
# ============================================================

_SIGN_TRAITS = {
    "Aries": "bold, pioneering, energetic, and competitive",
    "Taurus": "stable, sensual, determined, and materialistic",
    "Gemini": "intellectual, communicative, adaptable, and curious",
    "Cancer": "nurturing, emotional, intuitive, and protective",
    "Leo": "authoritative, creative, generous, and proud",
    "Virgo": "analytical, detail-oriented, practical, and service-minded",
    "Libra": "diplomatic, harmonious, aesthetic, and relationship-oriented",
    "Scorpio": "intense, transformative, secretive, and powerful",
    "Sagittarius": "philosophical, adventurous, optimistic, and freedom-loving",
    "Capricorn": "disciplined, ambitious, structured, and persevering",
    "Aquarius": "innovative, humanitarian, unconventional, and intellectual",
    "Pisces": "spiritual, compassionate, imaginative, and intuitive",
}

_HOUSE_MEANINGS = {
    1: "personality and physical body", 2: "wealth and family", 3: "courage and siblings",
    4: "home, mother, and comfort", 5: "children, education, and creativity", 6: "health, enemies, and service",
    7: "marriage and partnerships", 8: "longevity and transformation", 9: "fortune and higher learning",
    10: "career and public status", 11: "gains and aspirations", 12: "losses, spirituality, and foreign lands",
}


def _rule_based_period_prediction(chart_data: dict, prediction_type: str) -> dict:
    """Generate rule-based daily/monthly/yearly predictions without AI."""
    from datetime import date
    import random

    today = date.today()
    planets = chart_data.get("planets", {})
    asc = chart_data.get("ascendant", {})
    asc_sign = asc.get("sign", "Aries")
    moon = planets.get("Moon", {})
    moon_sign = moon.get("sign", asc_sign)
    sun = planets.get("Sun", {})
    sun_sign = sun.get("sign", asc_sign)

    # Seed random with date + chart for consistent daily predictions
    seed_str = f"{today.isoformat()}-{asc_sign}-{moon_sign}-{prediction_type}"
    rng = random.Random(seed_str)

    _OUTLOOK = ["excellent", "very favorable", "positive", "moderate", "mixed", "challenging but growth-oriented"]
    _ADVICE_CAREER = [
        "Focus on completing pending tasks — productivity peaks today.",
        "A new opportunity may present itself. Stay alert and prepared.",
        "Teamwork brings the best results. Collaborate with colleagues.",
        "Avoid making major financial decisions impulsively.",
        "Your leadership qualities shine — take initiative on projects.",
        "Focus on skill development and learning new things.",
    ]
    _ADVICE_RELATIONSHIP = [
        "Spend quality time with family. Harmony prevails at home.",
        "Communication is key today — express your feelings openly.",
        "A pleasant surprise from a loved one lifts your spirits.",
        "Be patient with your partner. Understanding resolves conflicts.",
        "Social connections bring joy — meet old friends if possible.",
        "Romance is in the air — plan something special.",
    ]
    _ADVICE_HEALTH = [
        "Take care of your digestion — eat light and healthy meals.",
        "Morning exercise or yoga will boost your energy levels.",
        "Stay hydrated and avoid excessive stress.",
        "A good day for meditation and mental wellness practices.",
        "Pay attention to sleep quality — rest is essential.",
        "Outdoor activities bring vitality and freshness.",
    ]

    lines = []
    highlights = []

    if prediction_type == "daily":
        outlook = rng.choice(_OUTLOOK)
        lines.append(f"## Daily Prediction — {today.strftime('%B %d, %Y')}")
        lines.append(f"\n**Overall Outlook:** {outlook.title()}\n")
        lines.append(f"With your Moon in {moon_sign} and Ascendant in {asc_sign}, today's planetary alignments bring a {outlook} day.\n")
        lines.append("## Career & Work")
        lines.append(f"- {rng.choice(_ADVICE_CAREER)}\n")
        lines.append("## Relationships")
        lines.append(f"- {rng.choice(_ADVICE_RELATIONSHIP)}\n")
        lines.append("## Health & Wellness")
        lines.append(f"- {rng.choice(_ADVICE_HEALTH)}\n")
        lucky_num = rng.randint(1, 9)
        lucky_colors = ["Red", "Blue", "Green", "Yellow", "White", "Orange", "Purple"]
        lines.append(f"**Lucky Number:** {lucky_num} | **Lucky Color:** {rng.choice(lucky_colors)}\n")
        highlights = [f"Overall outlook: {outlook}", f"Moon in {moon_sign}"]

    elif prediction_type == "monthly":
        month_name = today.strftime("%B %Y")
        lines.append(f"## Monthly Prediction — {month_name}")
        lines.append(f"\nWith your Ascendant in {asc_sign} and Moon in {moon_sign}, here's what {month_name} holds for you.\n")
        lines.append("## Career & Finance")
        lines.append(f"- {rng.choice(_ADVICE_CAREER)}")
        lines.append(f"- {rng.choice(_ADVICE_CAREER)}\n")
        lines.append("## Relationships & Family")
        lines.append(f"- {rng.choice(_ADVICE_RELATIONSHIP)}")
        lines.append(f"- {rng.choice(_ADVICE_RELATIONSHIP)}\n")
        lines.append("## Health & Wellness")
        lines.append(f"- {rng.choice(_ADVICE_HEALTH)}")
        lines.append(f"- {rng.choice(_ADVICE_HEALTH)}\n")
        lines.append("## Key Dates to Watch")
        d1, d2, d3 = rng.sample(range(1, 29), 3)
        lines.append(f"- **{d1}th**: Favorable for new initiatives")
        lines.append(f"- **{d2}th**: Focus on financial planning")
        lines.append(f"- **{d3}th**: Auspicious for important decisions\n")
        highlights = [f"Monthly forecast for {month_name}", f"Ascendant: {asc_sign}"]

    elif prediction_type == "yearly":
        year = today.year
        lines.append(f"## Yearly Prediction — {year}")
        lines.append(f"\nA comprehensive look at what {year} holds based on your birth chart (Ascendant: {asc_sign}, Moon: {moon_sign}, Sun: {sun_sign}).\n")
        lines.append("## Overall Theme")
        themes = ["growth and expansion", "consolidation and stability", "transformation and renewal", "learning and exploration"]
        lines.append(f"- {year} is a year of **{rng.choice(themes)}** for you.\n")
        lines.append("## Career & Professional Growth")
        lines.append(f"- {rng.choice(_ADVICE_CAREER)}")
        lines.append(f"- {rng.choice(_ADVICE_CAREER)}\n")
        lines.append("## Financial Outlook")
        lines.append("- Steady income flow with potential for unexpected gains in the second half.")
        lines.append("- Avoid risky investments, especially during eclipse periods.\n")
        lines.append("## Relationships")
        lines.append(f"- {rng.choice(_ADVICE_RELATIONSHIP)}")
        lines.append(f"- {rng.choice(_ADVICE_RELATIONSHIP)}\n")
        lines.append("## Health")
        lines.append(f"- {rng.choice(_ADVICE_HEALTH)}\n")
        lines.append("## Quarter-by-Quarter Highlights")
        lines.append("- **Q1 (Jan-Mar):** Foundation building, planning ahead")
        lines.append("- **Q2 (Apr-Jun):** Action phase, career momentum picks up")
        lines.append("- **Q3 (Jul-Sep):** Reflection period, focus on health and family")
        lines.append("- **Q4 (Oct-Dec):** Harvest phase, results of efforts become visible\n")
        highlights = [f"Yearly forecast for {year}", f"Theme: growth"]

    return {
        "interpretation": "\n".join(lines),
        "highlights": highlights,
        "warnings": [],
    }


def _rule_based_interpretation(chart_data: dict, prediction_type: str = "general") -> dict:
    """Generate a meaningful interpretation from chart data without any AI API."""
    from app.dosha_engine import analyze_yogas_and_doshas
    from datetime import date

    planets = chart_data.get("planets", {})
    asc = chart_data.get("ascendant", {})
    asc_sign = asc.get("sign", "Aries")

    # Period-specific predictions
    if prediction_type in ("daily", "monthly", "yearly"):
        return _rule_based_period_prediction(chart_data, prediction_type)

    lines = []
    highlights = []
    warnings = []

    # Ascendant analysis
    traits = _SIGN_TRAITS.get(asc_sign, "")
    lines.append(f"**Ascendant (Lagna): {asc_sign}**")
    lines.append(f"Your rising sign is {asc_sign}, making you {traits}. This sign shapes your outward personality and how others perceive you.\n")

    # Moon sign — mind and emotions
    moon = planets.get("Moon", {})
    moon_sign = moon.get("sign", "")
    moon_nak = moon.get("nakshatra", "")
    if moon_sign:
        lines.append(f"**Moon Sign (Rashi): {moon_sign}**")
        lines.append(f"Your Moon in {moon_sign} ({_SIGN_TRAITS.get(moon_sign, '')}) governs your emotional nature and inner mind. Nakshatra: {moon_nak}.\n")

    # Sun sign — soul and authority
    sun = planets.get("Sun", {})
    sun_sign = sun.get("sign", "")
    if sun_sign:
        lines.append(f"**Sun Sign: {sun_sign}**")
        lines.append(f"Your Sun in {sun_sign} in house {sun.get('house', '?')} relates to {_HOUSE_MEANINGS.get(sun.get('house', 1), 'self')}. The Sun represents your soul, vitality, and authority.\n")

    # Key planet placements
    lines.append("**Key Planetary Placements:**")
    for pname in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        p = planets.get(pname, {})
        if p.get("sign") and p.get("house"):
            status = p.get("status", "")
            status_note = f" ({status})" if status else ""
            lines.append(f"- {pname} in {p['sign']}, House {p['house']}{status_note} — influences {_HOUSE_MEANINGS.get(p['house'], 'life areas')}")
    lines.append("")

    # Rahu-Ketu axis
    rahu = planets.get("Rahu", {})
    ketu = planets.get("Ketu", {})
    if rahu.get("house") and ketu.get("house"):
        lines.append(f"**Rahu-Ketu Axis:** Rahu in House {rahu['house']} ({rahu.get('sign', '')}) and Ketu in House {ketu['house']} ({ketu.get('sign', '')})")
        lines.append(f"This axis indicates your karmic direction — Rahu shows where you're heading (material desires in {_HOUSE_MEANINGS.get(rahu['house'], '')}), Ketu shows what you've mastered in past lives ({_HOUSE_MEANINGS.get(ketu['house'], '')}).\n")

    # Yogas and Doshas
    yd = analyze_yogas_and_doshas(planets, asc_sign)

    present_yogas = [y for y in yd.get("yogas", []) if y.get("present")]
    present_doshas = [d for d in yd.get("doshas", []) if d.get("present")]

    if present_yogas:
        lines.append("**Yogas (Positive Combinations) Found:**")
        for y in present_yogas:
            lines.append(f"- **{y['name']}**: {y['description']}")
            highlights.append(y['name'])
        lines.append("")

    if present_doshas:
        lines.append("**Doshas (Afflictions) Detected:**")
        for d in present_doshas:
            lines.append(f"- **{d['name']}** (Severity: {d.get('severity', 'N/A')}): {d['description']}")
            if d.get("remedies"):
                lines.append(f"  Remedies: {'; '.join(d['remedies'][:2])}")
            warnings.append(f"{d['name']} ({d.get('severity', '')})")
        lines.append("")

    if not present_yogas:
        lines.append("No major yogas detected in this chart.\n")
    if not present_doshas:
        lines.append("No significant doshas detected — chart is relatively clear of afflictions.\n")
        highlights.append("No major doshas — clean chart")

    return {
        "interpretation": "\n".join(lines),
        "highlights": highlights or ["Review the detailed interpretation above"],
        "warnings": warnings,
    }


# ============================================================
# PUBLIC API
# ============================================================

def ai_interpret_kundli(chart_data: dict, prediction_type: str = "general") -> dict:
    """
    AI interpretation of a Vedic birth chart (kundli).

    Args:
        chart_data: Dict with planet positions, dashas, houses, etc.
        prediction_type: "general", "daily", "monthly", or "yearly"

    Returns:
        {interpretation: str, highlights: [str], warnings: [str]}
    """
    from datetime import date

    today = date.today()

    _PERIOD_PROMPTS = {
        "daily": (
            "You are an expert Vedic astrologer (Jyotishi). Based on the birth chart data provided "
            "and current planetary transits, give a DAILY prediction for today ({today}). "
            "Cover: general outlook, career/work, relationships, health, and a lucky tip for the day. "
            "Keep it concise, practical, and actionable. Use Vedic astrology concepts."
        ).format(today=today.strftime("%B %d, %Y")),
        "monthly": (
            "You are an expert Vedic astrologer (Jyotishi). Based on the birth chart data provided "
            "and current planetary transits, give a MONTHLY prediction for {month} {year}. "
            "Cover: career & finance, relationships & family, health & wellness, spiritual growth, "
            "and key dates to watch. Provide practical guidance for the month ahead."
        ).format(month=today.strftime("%B"), year=today.year),
        "yearly": (
            "You are an expert Vedic astrologer (Jyotishi). Based on the birth chart data provided "
            "and major planetary transits, give a YEARLY prediction for {year}. "
            "Cover: overall theme of the year, career growth, financial outlook, relationships, "
            "health, travel, and spiritual evolution. Mention major transit effects (Saturn, Jupiter, Rahu-Ketu). "
            "Provide quarter-by-quarter highlights."
        ).format(year=today.year),
    }

    system_prompt = _PERIOD_PROMPTS.get(prediction_type, (
        "You are an expert Vedic astrologer (Jyotishi). Analyze the provided birth chart data "
        "and give a comprehensive interpretation. Include personality traits, career guidance, "
        "relationship insights, and spiritual path. Use traditional Vedic astrology concepts "
        "(rashis, nakshatras, dashas, yogas). Be insightful but accessible."
    ))

    chart_str = json.dumps(chart_data, indent=2, default=str)

    _PERIOD_INSTRUCTIONS = {
        "daily": f"Give a daily Vedic horoscope prediction for today ({today.strftime('%B %d, %Y')}) based on this birth chart:\n\n{chart_str}",
        "monthly": f"Give a monthly Vedic prediction for {today.strftime('%B %Y')} based on this birth chart:\n\n{chart_str}",
        "yearly": f"Give a yearly Vedic prediction for {today.year} based on this birth chart:\n\n{chart_str}",
    }

    user_prompt = _PERIOD_INSTRUCTIONS.get(prediction_type, f"Interpret this Vedic birth chart:\n\n{chart_str}")

    response = _call_ai(system_prompt, user_prompt, temperature=0.6)

    if response is None:
        # Generate rule-based interpretation from chart data
        return _rule_based_interpretation(chart_data, prediction_type=prediction_type)

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
