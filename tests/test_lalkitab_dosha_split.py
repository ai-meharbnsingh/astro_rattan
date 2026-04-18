"""
Regression tests for the Mangal Dosh LK-canon vs Vedic-overlay split
(Codex R1-P6 + R2-P2). Guards against silent regressions like the
frontend Dosha tab merging the two back into one list.

Run: python3 tests/test_lalkitab_dosha_split.py
"""
from __future__ import annotations

import os, sys, traceback

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.lalkitab_dosha import (
    detect_lalkitab_doshas,
    MANGAL_DOSH_LK_HOUSES,
    MANGAL_DOSH_VEDIC_OVERLAY,
)


def _planets(mars_house: int):
    """Minimal chart where only Mars's house matters for Mangal detection."""
    return [
        {"planet": "Sun", "house": 1},
        {"planet": "Moon", "house": 4},
        {"planet": "Mars", "house": mars_house},
        {"planet": "Mercury", "house": 7},
        {"planet": "Jupiter", "house": 9},
        {"planet": "Venus", "house": 3},
        {"planet": "Saturn", "house": 10},
        {"planet": "Rahu", "house": 11},
        {"planet": "Ketu", "house": 5},
    ]


def _mangal(doshas):
    for d in doshas:
        if d.get("key") == "mangalDosh":
            return d
    return None


def ok(label, cond, detail=""):
    mark = "✓" if cond else "✗"
    print(f"  {mark} {label}" + (f" — {detail}" if detail else ""))
    return bool(cond)


def run():
    print("─── Mangal Dosh LK/Vedic split regression ───")
    failures = 0

    # Test 1 — classical LK houses (H1/H7/H8) → LK_CANONICAL
    for h in MANGAL_DOSH_LK_HOUSES:
        d = _mangal(detect_lalkitab_doshas(_planets(h)))
        if not ok(f"Mars H{h} → source=LK_CANONICAL",
                  d and d["source"] == "LK_CANONICAL" and d["is_lk_canonical"],
                  f"got source={d['source']}" if d else "missing"):
            failures += 1

    # Test 2 — Vedic-overlay houses (H2/H4/H12) → source in
    # {"VEDIC_INFLUENCED", "vedic_influenced"} (Codex D2: taxonomy
    # case was normalised; both variants treated as equivalent).
    VEDIC_VALUES = {"VEDIC_INFLUENCED", "vedic_influenced"}
    for h in MANGAL_DOSH_VEDIC_OVERLAY:
        d = _mangal(detect_lalkitab_doshas(_planets(h)))
        if not ok(f"Mars H{h} → source ∈ {{VEDIC_INFLUENCED, vedic_influenced}}",
                  d and d["source"] in VEDIC_VALUES
                  and not d["is_lk_canonical"]
                  and d["is_vedic_influenced"],
                  f"got source={d['source']}, is_lk={d['is_lk_canonical']}" if d else "missing"):
            failures += 1
        # D3: source_note must be non-empty on Vedic-overlay detections
        if not ok(f"Mars H{h} → source_note_en populated",
                  d and bool(d.get("source_note_en")),
                  f"got source_note_en={d.get('source_note_en') if d else None!r}"):
            failures += 1
        # D4: lk_equivalent_key must point to the LK-canon equivalent
        if not ok(f"Mars H{h} → lk_equivalent_key='mangalDosh'",
                  d and d.get("lk_equivalent_key") == "mangalDosh",
                  f"got lk_equivalent_key={d.get('lk_equivalent_key') if d else None!r}"):
            failures += 1

    # Test 3 — Mars H5 (not in either list) → detected=False, source=none
    d = _mangal(detect_lalkitab_doshas(_planets(5)))
    if not ok("Mars H5 → not detected, source=none",
              d and d["detected"] is False and d["source"] == "none",
              f"detected={d['detected']} source={d['source']}" if d else "missing"):
        failures += 1

    # Test 4 — frontend invariant: every dosha record has a 'source' field.
    # This guards against the frontend regressing to mix LK + Vedic.
    doshas = detect_lalkitab_doshas(_planets(4))
    for d in doshas:
        if not ok(f"{d.get('key')}: has source field",
                  "source" in d,
                  f"missing 'source'"):
            failures += 1

    # Test 5 — summary: for Meharban-like chart (Mars H4), the Vedic
    # overlay is detected but is NOT lk_canonical. Frontend will filter
    # this out of main 'Doshas' block into 'Vedic Overlays'.
    d = _mangal(detect_lalkitab_doshas(_planets(4)))
    if not ok("Meharban (Mars H4) scenario: detected AND vedic_influenced AND NOT lk_canonical",
              d and d["detected"] and d["is_vedic_influenced"] and not d["is_lk_canonical"]):
        failures += 1

    # Test 6 — Shani Dosh (unrelated) must still be detected correctly
    # regardless of Mars position (guards against accidental filter
    # removing non-Mangal doshas from the main block).
    doshas = detect_lalkitab_doshas(_planets(4))
    shani = next((x for x in doshas if x.get("key") == "shaniDosh"), None)
    if not ok("Shani Dosh still present when Mars H4 triggers Vedic overlay",
              shani is not None):
        failures += 1

    print()
    if failures == 0:
        print("✓ All Mangal Dosh split invariants hold.")
        return 0
    print(f"✗ {failures} failure(s).")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(run())
    except Exception:
        traceback.print_exc()
        sys.exit(2)
