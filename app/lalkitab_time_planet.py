"""
lalkitab_time_planet.py — Day + Time (Hora) planet: the non-remediable fate planet
===================================================================================
Reference: Lal Kitab 1952 (Pandit Roop Chand Joshi), Ch. 2.16.

Canon:
  • Every native has a Day-Lord (ruler of the weekday of birth) and a
    Hora-Lord (ruler of the hour of birth, per Chaldean order).
  • Together they form the native's "Time Planet" — a signature of
    TIME itself, not of karma. The Time Planet encodes destiny that
    LK considers FATE rather than karma.
  • Therefore remedies applied to the Time Planet are BANNED by canon.
    LK 1952 is explicit: remedies to the Time Planet backfire — the
    native is trying to edit the clock that pre-existed them.
  • This is what creates the LK distinction between "Sign Effect"
    (Vedic, karmic, remediable) and "Planetary Effect" (LK, fated,
    non-remediable).

This engine REUSES `app.lalkitab_advanced.calculate_hora_lord()` and
`app.lalkitab_advanced.DAY_LORDS` so that the day + hora semantics
stay consistent with karmic-debt calculation.

If the real sunrise is not available and no explicit fallback is
provided the caller receives a best-effort 6:00 AM local fallback
result marked `sunrise_assumed=True` — this is naive but safe for UI
display (front-end surfaces the assumption). The fallback can be
disabled by passing `allow_sunrise_fallback=False`.
"""
from __future__ import annotations

from datetime import datetime, time
from typing import Any, Dict, Optional


# Reuse the single source of truth for day-lord + hora-lord maths.
from app.lalkitab_advanced import (
    DAY_LORDS,
    calculate_hora_lord,
)


_PLANET_HI: Dict[str, str] = {
    "Sun":     "सूर्य",
    "Moon":    "चन्द्र",
    "Mars":    "मंगल",
    "Mercury": "बुध",
    "Jupiter": "गुरु",
    "Venus":   "शुक्र",
    "Saturn":  "शनि",
    "Rahu":    "राहु",
    "Ketu":    "केतु",
}

# LK canon ranks visible planets by "weight" (luminaries > malefics > benefics)
# for breaking ties between day-lord and hora-lord. Higher index = more dominant.
# Matches the Chaldean speed order used elsewhere — slowest planet wins because
# slower planets have stronger "time signature" per LK.
_DOMINANCE_ORDER = [
    "Moon",    # fastest
    "Mercury",
    "Venus",
    "Sun",
    "Mars",
    "Jupiter",
    "Saturn",  # slowest — most fate-heavy
]


def _dominance(planet: str) -> int:
    try:
        return _DOMINANCE_ORDER.index(planet)
    except ValueError:
        return -1


def _pick_time_planet(day_lord: str, hora_lord: Optional[str]) -> Dict[str, Any]:
    """
    Decide which of {day_lord, hora_lord} is the "Time Planet".

    Rules (LK 2.16):
      1. If day_lord == hora_lord, that planet is the sole Time Planet
         and is treated as especially potent (fate signature doubles).
      2. If hora_lord is unknown (no sunrise), fall back to day_lord
         alone.
      3. Otherwise both are emitted with `dual=True` — frontend should
         warn that remedies to EITHER are banned — but the dominant one
         (slower planet, higher Chaldean weight) is flagged as primary.
    """
    if not hora_lord or hora_lord == day_lord:
        return {
            "time_planet": day_lord,
            "dual": False,
            "doubled": hora_lord == day_lord,
            "both": [day_lord] if not hora_lord else [day_lord, day_lord],
        }

    # Different planets — both are "Time Planets", pick primary by dominance.
    d_day = _dominance(day_lord)
    d_hora = _dominance(hora_lord)
    if d_hora > d_day:
        primary = hora_lord
    elif d_day > d_hora:
        primary = day_lord
    else:
        # Equal dominance (shouldn't happen among visible planets) — prefer hora.
        primary = hora_lord

    return {
        "time_planet": primary,
        "dual": True,
        "doubled": False,
        "both": [day_lord, hora_lord],
    }


def detect_time_planet(
    birth_date_iso: str,
    birth_time_hms: str,
    sunrise_hms: Optional[str] = None,
    allow_sunrise_fallback: bool = True,
) -> Dict[str, Any]:
    """
    Compute the Day-Lord, Hora-Lord and resulting Time Planet.

    Args:
        birth_date_iso:   "YYYY-MM-DD"
        birth_time_hms:   "HH:MM" or "HH:MM:SS"
        sunrise_hms:      optional "HH:MM" / "HH:MM:SS" sunrise for the
                          birth date + location. If absent and
                          allow_sunrise_fallback=True we assume 06:00
                          local sunrise and mark `sunrise_assumed=True`.
        allow_sunrise_fallback:
                          when False and sunrise_hms is None we skip the
                          Hora calculation entirely and the result flags
                          `hora_lord=None, hora_skipped=True`.

    Returns (LK_CANONICAL shape):
        {
          day_lord:         str,
          day_lord_hi:      str,
          weekday_name:     str,
          hora_lord:        str | None,
          hora_lord_hi:     str | None,
          hora_skipped:     bool,
          sunrise_assumed:  bool,
          time_planet:      str,          # dominant planet (or day-lord if dual=False)
          time_planet_hi:   str,
          both_planets:     [str, ...],   # [day_lord, hora_lord] (or just day_lord)
          dual:             bool,         # True ⇔ day_lord != hora_lord
          doubled:          bool,         # True ⇔ day_lord == hora_lord (amplifies fate)
          is_remediable:    False,        # always False per LK canon
          warning_en:       str,
          warning_hi:       str,
          source:           "LK_CANONICAL",
          lk_ref:           "2.16",
        }
    """
    # ── Parse birth datetime (accept HH:MM or HH:MM:SS) ──────────
    t_parts = (birth_time_hms or "").split(":")
    if len(t_parts) == 2:
        t_parts = [t_parts[0], t_parts[1], "00"]
    if len(t_parts) != 3:
        raise ValueError(f"birth_time_hms must be HH:MM or HH:MM:SS, got {birth_time_hms!r}")
    try:
        hh, mm, ss = (int(t_parts[0]), int(t_parts[1]), int(t_parts[2]))
        birth_dt = datetime.fromisoformat(birth_date_iso).replace(
            hour=hh, minute=mm, second=ss, microsecond=0,
        )
    except (ValueError, TypeError) as exc:
        raise ValueError(
            f"cannot parse birth date/time ({birth_date_iso!r} {birth_time_hms!r}): {exc}"
        ) from exc

    # ── Parse sunrise (real or fallback) ─────────────────────────
    sunrise_assumed = False
    sunrise_time: Optional[time] = None
    if sunrise_hms:
        sr_parts = sunrise_hms.split(":")
        if len(sr_parts) == 2:
            sr_parts = [sr_parts[0], sr_parts[1], "00"]
        try:
            sunrise_time = time(int(sr_parts[0]), int(sr_parts[1]), int(sr_parts[2]))
        except (ValueError, TypeError):
            sunrise_time = None
    if sunrise_time is None and allow_sunrise_fallback:
        # Naive but safe fallback: 06:00 local time. Surfaced via
        # sunrise_assumed=True so UI can caveat the result.
        sunrise_time = time(6, 0, 0)
        sunrise_assumed = True

    # ── Day lord (always computable from date alone) ─────────────
    day_lord = DAY_LORDS[birth_dt.weekday()]
    weekday_name = birth_dt.strftime("%A")

    # ── Hora lord (needs sunrise; may skip) ──────────────────────
    hora_lord: Optional[str] = None
    hora_skipped = True
    if sunrise_time is not None:
        hora_info = calculate_hora_lord(birth_dt, sunrise_time=sunrise_time)
        if not hora_info.get("_skipped"):
            hora_lord = hora_info.get("hora_lord")
            hora_skipped = False

    # ── Derive Time Planet ───────────────────────────────────────
    pick = _pick_time_planet(day_lord, hora_lord)
    tp = pick["time_planet"]
    tp_hi = _PLANET_HI.get(tp, tp)

    both = [day_lord]
    if hora_lord and hora_lord != day_lord:
        both = [day_lord, hora_lord]
    elif hora_lord == day_lord:
        both = [day_lord]

    # ── Bilingual warnings ───────────────────────────────────────
    if pick["doubled"]:
        warning_en = (
            f"The Day-Lord and Hora-Lord of your birth are both {tp}. "
            f"This makes {tp} your Time Planet with doubled fate-weight. "
            f"Per Lal Kitab canon (LK 2.16) do NOT apply any remedy to {tp} — "
            f"remedies to the Time Planet backfire because it encodes fate, "
            f"not karma."
        )
        warning_hi = (
            f"आपके जन्म का वार-स्वामी और होरा-स्वामी दोनों {tp_hi} हैं। "
            f"इससे {tp_hi} आपका समय-ग्रह बन जाता है जिसका भाग्य-भार दोगुना है। "
            f"लाल किताब अनुसार (लाल किताब 2.16) {tp_hi} पर कोई भी उपाय न करें — "
            f"समय-ग्रह पर किए गए उपाय उल्टे पड़ते हैं क्योंकि यह भाग्य है, "
            f"कर्म नहीं।"
        )
    elif pick["dual"] and hora_lord:
        hora_hi = _PLANET_HI.get(hora_lord, hora_lord)
        day_hi = _PLANET_HI.get(day_lord, day_lord)
        warning_en = (
            f"Your Day-Lord is {day_lord} and your Hora-Lord is {hora_lord}. "
            f"Both function as Time Planets (LK 2.16) — {tp} is dominant "
            f"but remedies to EITHER {day_lord} OR {hora_lord} are banned. "
            f"These planets encode the clock of your birth, not actions you "
            f"can edit through remedy."
        )
        warning_hi = (
            f"आपका वार-स्वामी {day_hi} और होरा-स्वामी {hora_hi} है। "
            f"दोनों समय-ग्रह की तरह कार्य करते हैं (लाल किताब 2.16) — {tp_hi} "
            f"प्रमुख है परंतु {day_hi} अथवा {hora_hi} — किसी पर भी उपाय वर्जित है। "
            f"ये ग्रह आपके जन्म-काल की घड़ी दर्शाते हैं, न कि ऐसे कर्म जिन्हें "
            f"उपाय से बदला जा सके।"
        )
    else:
        # Hora unknown — emit day-lord only warning.
        warning_en = (
            f"Your Day-Lord is {day_lord}. Per Lal Kitab canon (LK 2.16) this "
            f"is your Time Planet and remedies applied to {day_lord} will "
            f"backfire — it encodes fate, not karma. "
            f"(Hora-Lord could not be computed because sunrise was unavailable.)"
        )
        warning_hi = (
            f"आपका वार-स्वामी {tp_hi} है। लाल किताब अनुसार (लाल किताब 2.16) "
            f"यही आपका समय-ग्रह है और {tp_hi} पर किए गए उपाय उल्टे पड़ते हैं — "
            f"यह भाग्य है, कर्म नहीं। "
            f"(सूर्योदय उपलब्ध न होने से होरा-स्वामी की गणना नहीं हो सकी।)"
        )

    return {
        "day_lord": day_lord,
        "day_lord_hi": _PLANET_HI.get(day_lord, day_lord),
        "weekday_name": weekday_name,
        "hora_lord": hora_lord,
        "hora_lord_hi": _PLANET_HI.get(hora_lord, hora_lord) if hora_lord else None,
        "hora_skipped": hora_skipped,
        "sunrise_assumed": sunrise_assumed,
        "time_planet": tp,
        "time_planet_hi": tp_hi,
        "both_planets": both,
        "dual": bool(pick["dual"]),
        "doubled": bool(pick["doubled"]),
        "is_remediable": False,  # LK 2.16 — always False
        "warning_en": warning_en,
        "warning_hi": warning_hi,
        "source": "LK_CANONICAL",
        "lk_ref": "2.16",
    }
