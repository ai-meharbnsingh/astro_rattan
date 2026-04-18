"""
Lal Kitab Dosha Detection Engine.

Detects classical Lal Kitab doshas from planet x house positions.
Bilingual output (English + Hindi).

Ported from frontend/src/components/lalkitab/lalkitab-data.ts detectDoshas()
to provide authoritative backend detection.
"""
from typing import Dict, List, Any


# ── Constants (mirrored from frontend lalkitab-data.ts) ──

PITRA_DOSH_HOUSE = 9

SHANI_DOSH_HOUSES = [1, 4, 7, 8, 10]
SHANI_DOSH_HIGH_SEVERITY_HOUSE = 8

DUSTHANA_HOUSES = [6, 8, 12]

KARMIC_DEBT_MIN_MALEFICS = 2
KARMIC_DEBT_HIGH_MALEFICS = 3

# ─── Mangal Dosh — LK 1952 vs Vedic variants ────────────────────────
# Strict Lal Kitab rule: Mars in H1, H7, or H8 only.
# The Vedic/Parashari overlay additionally flags H2, H4, and H12 but
# those are NOT part of the LK 1952 canon (per Codex audit).
MANGAL_DOSH_LK_HOUSES        = [1, 7, 8]          # LK 1952 canon
MANGAL_DOSH_VEDIC_OVERLAY    = [2, 4, 12]         # flagged but tagged source="vedic_influenced"
MANGAL_DOSH_HIGH_HOUSES      = [7, 8]
# Backwards-compat alias (still referenced by older callers/tests).
MANGAL_DOSH_HOUSES = MANGAL_DOSH_LK_HOUSES + MANGAL_DOSH_VEDIC_OVERLAY


def detect_lalkitab_doshas(planet_positions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Detect Lal Kitab doshas from planet positions.

    Args:
        planet_positions: [{"planet": "Sun", "house": 1}, {"planet": "Moon", "house": 4}, ...]

    Returns:
        List of detected doshas, each with:
        {
            "key": str,
            "name_en": str,
            "name_hi": str,
            "detected": bool,
            "severity": "high" | "medium" | "low",
            "description_en": str,
            "description_hi": str,
            "affected_planets": list[str],
            "affected_houses": list[int],
            "remedy_hint_en": str,
            "remedy_hint_hi": str,
        }
    """
    # Build planet -> house lookup
    pos: Dict[str, int] = {}
    for entry in planet_positions:
        planet = entry.get("planet", "")
        house = entry.get("house", 0)
        if isinstance(house, int) and house > 0:
            pos[planet] = house

    sun_h = pos.get("Sun", 0)
    moon_h = pos.get("Moon", 0)
    mars_h = pos.get("Mars", 0)
    sat_h = pos.get("Saturn", 0)
    rahu_h = pos.get("Rahu", 0)
    ketu_h = pos.get("Ketu", 0)

    results: List[Dict[str, Any]] = []

    # ── 1. Pitra Dosh ──
    # Sun in 9th house with Saturn or Rahu
    pitra_detected = (
        sun_h == PITRA_DOSH_HOUSE
        and (sat_h == PITRA_DOSH_HOUSE or rahu_h == PITRA_DOSH_HOUSE)
    )
    pitra_affected_planets = []
    pitra_affected_houses = []
    if pitra_detected:
        pitra_affected_planets.append("Sun")
        pitra_affected_houses.append(PITRA_DOSH_HOUSE)
        if sat_h == PITRA_DOSH_HOUSE:
            pitra_affected_planets.append("Saturn")
        if rahu_h == PITRA_DOSH_HOUSE:
            pitra_affected_planets.append("Rahu")

    results.append({
        "key": "pitraDosh",
        "name_en": "Pitra Dosh",
        "name_hi": "\u092a\u093f\u0924\u0943 \u0926\u094b\u0937",
        "detected": pitra_detected,
        "severity": "high" if pitra_detected else "low",
        "description_en": (
            "Ancestors' unfulfilled karmas causing obstacles in life. "
            "Issues with father figures and authority."
        ),
        "description_hi": (
            "\u092a\u0942\u0930\u094d\u0935\u091c\u094b\u0902 \u0915\u0947 \u0905\u0927\u0942\u0930\u0947 \u0915\u0930\u094d\u092e \u091c\u0940\u0935\u0928 \u092e\u0947\u0902 \u092c\u093e\u0927\u093e\u090f\u0902 \u0921\u093e\u0932 \u0930\u0939\u0947 \u0939\u0948\u0902\u0964 "
            "\u092a\u093f\u0924\u093e \u0914\u0930 \u0905\u0927\u093f\u0915\u093e\u0930\u093f\u092f\u094b\u0902 \u0938\u0947 \u0938\u092e\u0938\u094d\u092f\u093e\u0964"
        ),
        "affected_planets": pitra_affected_planets,
        "affected_houses": pitra_affected_houses,
        "remedy_hint_en": (
            "Feed crows with sweet chapati every Saturday. "
            "Donate food to Brahmins on Amavasya."
        ),
        "remedy_hint_hi": (
            "\u0939\u0930 \u0936\u0928\u093f\u0935\u093e\u0930 \u0915\u094c\u0913\u0902 \u0915\u094b \u092e\u0940\u0920\u0940 \u0930\u094b\u091f\u0940 \u0916\u093f\u0932\u093e\u090f\u0902\u0964 "
            "\u0905\u092e\u093e\u0935\u0938\u094d\u092f\u093e \u092a\u0930 \u092c\u094d\u0930\u093e\u0939\u094d\u092e\u0923\u094b\u0902 \u0915\u094b \u092d\u094b\u091c\u0928 \u0926\u093e\u0928 \u0915\u0930\u0947\u0902\u0964"
        ),
    })

    # ── 2. Grahan Dosh ──
    # Sun or Moon conjunct with Rahu or Ketu (same house)
    grahan_detected = (
        (sun_h > 0 and (sun_h == rahu_h or sun_h == ketu_h))
        or (moon_h > 0 and (moon_h == rahu_h or moon_h == ketu_h))
    )
    grahan_affected_planets = []
    grahan_affected_houses = set()
    if grahan_detected:
        if sun_h > 0 and sun_h == rahu_h:
            grahan_affected_planets.extend(["Sun", "Rahu"])
            grahan_affected_houses.add(sun_h)
        if sun_h > 0 and sun_h == ketu_h:
            grahan_affected_planets.extend(["Sun", "Ketu"])
            grahan_affected_houses.add(sun_h)
        if moon_h > 0 and moon_h == rahu_h:
            grahan_affected_planets.extend(["Moon", "Rahu"])
            grahan_affected_houses.add(moon_h)
        if moon_h > 0 and moon_h == ketu_h:
            grahan_affected_planets.extend(["Moon", "Ketu"])
            grahan_affected_houses.add(moon_h)
        # deduplicate
        grahan_affected_planets = list(dict.fromkeys(grahan_affected_planets))

    results.append({
        "key": "grahanDosh",
        "name_en": "Grahan Dosh",
        "name_hi": "\u0917\u094d\u0930\u0939\u0923 \u0926\u094b\u0937",
        "detected": grahan_detected,
        "severity": "high" if grahan_detected else "low",
        "description_en": (
            "Eclipse-like effect on luminaries. "
            "Mental confusion, health issues, and delayed success."
        ),
        "description_hi": (
            "\u0917\u094d\u0930\u0939\u094b\u0902 \u092a\u0930 \u0917\u094d\u0930\u0939\u0923 \u091c\u0948\u0938\u093e \u092a\u094d\u0930\u092d\u093e\u0935\u0964 "
            "\u092e\u093e\u0928\u0938\u093f\u0915 \u092d\u094d\u0930\u092e, \u0938\u094d\u0935\u093e\u0938\u094d\u0925\u094d\u092f \u0938\u092e\u0938\u094d\u092f\u093e \u0914\u0930 \u0935\u093f\u0932\u0902\u092c\u093f\u0924 \u0938\u092b\u0932\u0924\u093e\u0964"
        ),
        "affected_planets": grahan_affected_planets,
        "affected_houses": sorted(grahan_affected_houses),
        "remedy_hint_en": (
            "Float coconut in flowing water. "
            "Donate black and white sesame seeds."
        ),
        "remedy_hint_hi": (
            "\u092c\u0939\u0924\u0947 \u092a\u093e\u0928\u0940 \u092e\u0947\u0902 \u0928\u093e\u0930\u093f\u092f\u0932 \u092c\u0939\u093e\u090f\u0902\u0964 "
            "\u0915\u093e\u0932\u0947 \u0914\u0930 \u0938\u092b\u0947\u0926 \u0924\u093f\u0932 \u0926\u093e\u0928 \u0915\u0930\u0947\u0902\u0964"
        ),
    })

    # ── 3. Mangal Dosh ──
    # Strict LK 1952 rule: Mars in H1, H7, or H8. Vedic-influenced
    # overlay (H2/H4/H12) is still surfaced but tagged so callers can
    # filter it out of Lal Kitab output. Codex audit: H4 Mars alone is
    # NOT standard LK Mangal Dosh.
    is_lk_mangal     = mars_h in MANGAL_DOSH_LK_HOUSES
    is_vedic_mangal  = mars_h in MANGAL_DOSH_VEDIC_OVERLAY
    mangal_detected  = is_lk_mangal or is_vedic_mangal
    # Codex D2 audit: use SCREAMING_SNAKE for taxonomy consistency.
    # Lower-case alias "vedic_influenced" is still emitted in the
    # record below for backward-compat with frontend filters.
    mangal_source    = (
        "LK_CANONICAL"     if is_lk_mangal
        else "VEDIC_INFLUENCED" if is_vedic_mangal
        else "none"
    )
    results.append({
        "key": "mangalDosh",
        "name_en": "Mangal Dosh",
        "name_hi": "\u092e\u0902\u0917\u0932 \u0926\u094b\u0937",
        "detected": mangal_detected,
        "is_lk_canonical": is_lk_mangal,
        "is_vedic_influenced": is_vedic_mangal,
        "source": mangal_source,
        # Codex D2 audit — backwards-compatible lowercase alias so
        # frontend filters using the old string (`vedic_influenced`)
        # don't silently break when taxonomy case is normalised.
        "source_legacy": mangal_source.lower() if is_vedic_mangal else mangal_source,
        # Codex D3 audit — classical citation for the Vedic overlay branch.
        "source_note_en": (
            "Parashari Hora Shastra — Mangal Dosh from H1/H2/H4/H7/H8/H12. "
            "Lal Kitab 1952 adopts a stricter subset (H1/H7/H8 only), so this "
            "is flagged as Vedic overlay for cross-reference." if is_vedic_mangal
            else (
                "Lal Kitab 1952 canonical — Mars in angular or 8th house."
                if is_lk_mangal else ""
            )
        ),
        "source_note_hi": (
            "पाराशरी होरा शास्त्र — मंगल दोष H1/H2/H4/H7/H8/H12 से। "
            "लाल किताब 1952 में सख्त नियम (केवल H1/H7/H8), इसलिए वैदिक परत "
            "के रूप में संदर्भ हेतु।" if is_vedic_mangal
            else (
                "लाल किताब 1952 मूल — केंद्र या 8वें भाव में मंगल।"
                if is_lk_mangal else ""
            )
        ),
        # Codex D4 audit — cross-link to the nearest LK-canon equivalent
        # so the frontend can render a "see also" pointer from the
        # Vedic block to the canonical block.
        "lk_equivalent_key": "mangalDosh" if is_vedic_mangal else None,
        "severity": (
            "high" if mangal_detected and mars_h in MANGAL_DOSH_HIGH_HOUSES
            else ("medium" if is_lk_mangal
                  else ("low" if is_vedic_mangal else "low"))
        ),
        "description_en": (
            "Mars in a sensitive house creates aggression in relationships, "
            "delays in marriage, and conflicts with spouse. "
            "Impacts domestic harmony and partnership stability."
        ),
        "description_hi": (
            "\u092e\u0902\u0917\u0932 \u0938\u0902\u0935\u0947\u0926\u0928\u0936\u0940\u0932 \u092d\u093e\u0935 \u092e\u0947\u0902 \u0939\u094b\u0928\u0947 \u0938\u0947 \u0930\u093f\u0936\u094d\u0924\u094b\u0902 \u092e\u0947\u0902 \u0906\u0915\u094d\u0930\u093e\u092e\u0915\u0924\u093e, "
            "\u0935\u093f\u0935\u093e\u0939 \u092e\u0947\u0902 \u0926\u0947\u0930\u0940 \u0914\u0930 \u091c\u0940\u0935\u0928\u0938\u093e\u0925\u0940 \u0938\u0947 \u0935\u093f\u0935\u093e\u0926\u0964 "
            "\u0918\u0930\u0947\u0932\u0942 \u0938\u093e\u092e\u0902\u091c\u0938\u094d\u092f \u0914\u0930 \u0938\u093e\u091d\u0947\u0926\u093e\u0930\u0940 \u092a\u094d\u0930\u092d\u093e\u0935\u093f\u0924\u0964"
        ),
        "affected_planets": ["Mars"] if mangal_detected else [],
        "affected_houses": [mars_h] if mangal_detected else [],
        "remedy_hint_en": (
            "Donate red lentils (masoor dal) on Tuesdays. "
            "Keep a silver square piece in your pocket."
        ),
        "remedy_hint_hi": (
            "\u092e\u0902\u0917\u0932\u0935\u093e\u0930 \u0915\u094b \u0932\u093e\u0932 \u092e\u0938\u0942\u0930 \u0926\u093e\u0932 \u0926\u093e\u0928 \u0915\u0930\u0947\u0902\u0964 "
            "\u091a\u093e\u0902\u0926\u0940 \u0915\u093e \u091a\u094c\u0915\u094b\u0930 \u091f\u0941\u0915\u0921\u093c\u093e \u091c\u0947\u092c \u092e\u0947\u0902 \u0930\u0916\u0947\u0902\u0964"
        ),
    })

    # ── 4. Shani Dosh ──
    # Saturn in houses 1, 4, 7, 8, or 10
    shani_detected = sat_h in SHANI_DOSH_HOUSES
    results.append({
        "key": "shaniDosh",
        "name_en": "Shani Dosh",
        "name_hi": "\u0936\u0928\u093f \u0926\u094b\u0937",
        "detected": shani_detected,
        "severity": (
            "high" if shani_detected and sat_h == SHANI_DOSH_HIGH_SEVERITY_HOUSE
            else ("medium" if shani_detected else "low")
        ),
        "description_en": (
            "Saturn creating delays, hard work without reward, "
            "and karmic lessons in life."
        ),
        "description_hi": (
            "\u0936\u0928\u093f \u0926\u0947\u0930\u0940, \u092c\u093f\u0928\u093e \u092b\u0932 \u0915\u0947 \u0915\u0920\u093f\u0928 \u092a\u0930\u093f\u0936\u094d\u0930\u092e "
            "\u0914\u0930 \u0915\u093e\u0930\u094d\u092e\u093f\u0915 \u0938\u092c\u0915 \u0926\u0947 \u0930\u0939\u093e \u0939\u0948\u0964"
        ),
        "affected_planets": ["Saturn"] if shani_detected else [],
        "affected_houses": [sat_h] if shani_detected else [],
        "remedy_hint_en": (
            "Feed crows and black dogs. "
            "Donate iron and mustard oil on Saturdays."
        ),
        "remedy_hint_hi": (
            "\u0915\u094c\u0913\u0902 \u0914\u0930 \u0915\u093e\u0932\u0947 \u0915\u0941\u0924\u094d\u0924\u094b\u0902 \u0915\u094b \u0916\u093f\u0932\u093e\u090f\u0902\u0964 "
            "\u0936\u0928\u093f\u0935\u093e\u0930 \u0915\u094b \u0932\u094b\u0939\u093e \u0914\u0930 \u0938\u0930\u0938\u094b\u0902 \u0915\u093e \u0924\u0947\u0932 \u0926\u093e\u0928 \u0915\u0930\u0947\u0902\u0964"
        ),
    })

    # ── 5. Kaal Sarp Dosh ──
    # All 7 planets (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn)
    # fall between the Rahu-Ketu axis
    kaal_sarp_detected = False
    kaal_sarp_planets: List[str] = []
    if rahu_h > 0 and ketu_h > 0 and rahu_h != ketu_h:
        seven_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
        seven_houses = [pos.get(p, 0) for p in seven_planets]

        # Check if all 7 planets fall in the arc from Rahu to Ketu (going forward)
        # or from Ketu to Rahu. We check both arcs.
        def _all_in_arc(start_h: int, end_h: int, houses: List[int]) -> bool:
            """Check if all non-zero houses fall in the arc from start to end (clockwise)."""
            if start_h == end_h:
                return False
            for h in houses:
                if h <= 0:
                    continue  # skip unknown positions
                if start_h < end_h:
                    if not (start_h <= h <= end_h):
                        return False
                else:
                    # Wrap around: e.g., start=10, end=3 means 10,11,12,1,2,3
                    if not (h >= start_h or h <= end_h):
                        return False
            return True

        valid_houses = [h for h in seven_houses if h > 0]
        if len(valid_houses) >= 5:  # need at least 5 of 7 planets with valid positions
            arc1 = _all_in_arc(rahu_h, ketu_h, valid_houses)
            arc2 = _all_in_arc(ketu_h, rahu_h, valid_houses)
            kaal_sarp_detected = arc1 or arc2
            if kaal_sarp_detected:
                kaal_sarp_planets = [
                    p for p, h in zip(seven_planets, seven_houses) if h > 0
                ]

    results.append({
        "key": "kaalSarpDosh",
        "name_en": "Kaal Sarp Dosh",
        "name_hi": "\u0915\u093e\u0932 \u0938\u0930\u094d\u092a \u0926\u094b\u0937",
        "detected": kaal_sarp_detected,
        "severity": "high" if kaal_sarp_detected else "low",
        "description_en": (
            "All planets hemmed between Rahu and Ketu axis. "
            "Creates sudden setbacks, fear, anxiety, and obstacles in major life events. "
            "One of the most impactful doshas in Lal Kitab."
        ),
        "description_hi": (
            "\u0938\u092d\u0940 \u0917\u094d\u0930\u0939 \u0930\u093e\u0939\u0941 \u0914\u0930 \u0915\u0947\u0924\u0941 \u0915\u0947 \u092c\u0940\u091a \u0918\u093f\u0930\u0947 \u0939\u0941\u090f\u0964 "
            "\u0905\u091a\u093e\u0928\u0915 \u0935\u093f\u092a\u0924\u094d\u0924\u093f\u092f\u093e\u0902, \u092d\u092f, \u091a\u093f\u0902\u0924\u093e \u0914\u0930 \u092e\u0939\u0924\u094d\u0935\u092a\u0942\u0930\u094d\u0923 \u091c\u0940\u0935\u0928 \u0918\u091f\u0928\u093e\u0913\u0902 \u092e\u0947\u0902 \u092c\u093e\u0927\u093e\u090f\u0902\u0964 "
            "\u0932\u093e\u0932 \u0915\u093f\u0924\u093e\u092c \u0915\u0947 \u0938\u092c\u0938\u0947 \u092a\u094d\u0930\u092d\u093e\u0935\u0936\u093e\u0932\u0940 \u0926\u094b\u0937\u094b\u0902 \u092e\u0947\u0902 \u0938\u0947 \u090f\u0915\u0964"
        ),
        "affected_planets": kaal_sarp_planets + ["Rahu", "Ketu"] if kaal_sarp_detected else [],
        "affected_houses": sorted({rahu_h, ketu_h}) if kaal_sarp_detected else [],
        "remedy_hint_en": (
            "Worship Lord Shiva on Mondays. "
            "Float a pair of silver snakes in flowing water."
        ),
        "remedy_hint_hi": (
            "\u0938\u094b\u092e\u0935\u093e\u0930 \u0915\u094b \u092d\u0917\u0935\u093e\u0928 \u0936\u093f\u0935 \u0915\u0940 \u092a\u0942\u091c\u093e \u0915\u0930\u0947\u0902\u0964 "
            "\u091a\u093e\u0902\u0926\u0940 \u0915\u0947 \u0926\u094b \u0938\u093e\u0902\u092a \u092c\u0939\u0924\u0947 \u092a\u093e\u0928\u0940 \u092e\u0947\u0902 \u092c\u0939\u093e\u090f\u0902\u0964"
        ),
    })

    # ── 6. Karmic Debts (Rini Dosh) ──
    # 2+ malefics (Saturn, Mars, Rahu, Ketu) in dusthana houses (6, 8, 12)
    malefic_houses = [sat_h, mars_h, rahu_h, ketu_h]
    malefics_in_dusthana = [h for h in malefic_houses if h in DUSTHANA_HOUSES]
    malefic_count = len(malefics_in_dusthana)
    karmic_detected = malefic_count >= KARMIC_DEBT_MIN_MALEFICS
    karmic_affected_planets = []
    if karmic_detected:
        if sat_h in DUSTHANA_HOUSES:
            karmic_affected_planets.append("Saturn")
        if mars_h in DUSTHANA_HOUSES:
            karmic_affected_planets.append("Mars")
        if rahu_h in DUSTHANA_HOUSES:
            karmic_affected_planets.append("Rahu")
        if ketu_h in DUSTHANA_HOUSES:
            karmic_affected_planets.append("Ketu")

    results.append({
        "key": "debtKarma",
        "name_en": "Karmic Debts (Rini Dosh)",
        "name_hi": "\u0915\u093e\u0930\u094d\u092e\u093f\u0915 \u090b\u0923 (\u090b\u0923\u0940 \u0926\u094b\u0937)",
        "detected": karmic_detected,
        "severity": (
            "high" if karmic_detected and malefic_count >= KARMIC_DEBT_HIGH_MALEFICS
            else ("medium" if karmic_detected else "low")
        ),
        "description_en": (
            "Past-life debts manifesting as recurring obstacles, "
            "financial issues, or relationship problems."
        ),
        "description_hi": (
            "\u092a\u0942\u0930\u094d\u0935 \u091c\u0928\u094d\u092e \u0915\u0947 \u090b\u0923 \u092c\u093e\u0930-\u092c\u093e\u0930 \u092c\u093e\u0927\u093e\u0913\u0902, "
            "\u0935\u093f\u0924\u094d\u0924\u0940\u092f \u0938\u092e\u0938\u094d\u092f\u093e\u0913\u0902 \u092f\u093e \u0938\u0902\u092c\u0902\u0927 \u0938\u092e\u0938\u094d\u092f\u093e\u0913\u0902 \u0915\u0947 \u0930\u0942\u092a \u092e\u0947\u0902 \u092a\u094d\u0930\u0915\u091f \u0939\u094b \u0930\u0939\u0947 \u0939\u0948\u0902\u0964"
        ),
        "affected_planets": karmic_affected_planets,
        "affected_houses": sorted(set(malefics_in_dusthana)),
        "remedy_hint_en": (
            "Donate food and clothes to the needy. "
            "Serve elders and parents sincerely."
        ),
        "remedy_hint_hi": (
            "\u091c\u0930\u0942\u0930\u0924\u092e\u0902\u0926\u094b\u0902 \u0915\u094b \u092d\u094b\u091c\u0928 \u0914\u0930 \u0915\u092a\u0921\u093c\u0947 \u0926\u093e\u0928 \u0915\u0930\u0947\u0902\u0964 "
            "\u092c\u0921\u093c\u094b\u0902 \u0914\u0930 \u092e\u093e\u0924\u093e-\u092a\u093f\u0924\u093e \u0915\u0940 \u0938\u091a\u094d\u091a\u0940 \u0938\u0947\u0935\u093e \u0915\u0930\u0947\u0902\u0964"
        ),
    })

    # Stamp every dosha record with a `source` tag so the frontend's
    # LK-canon vs Vedic-overlay split (Codex R2-P2) can filter reliably.
    # Mangal Dosh already stamps its own source (LK_CANONICAL / vedic_influenced
    # / none) based on Mars house; the remaining doshas are classical LK canon.
    for d in results:
        d.setdefault("source", "LK_CANONICAL")
    return results
