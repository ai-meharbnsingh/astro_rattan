"""
Lal Kitab — P2.9 Compound Debt Analysis with Prioritisation
===========================================================

Purpose
-------
When multiple Rins (karmic debts) coexist in a chart, Lal Kitab canon says
they should be remediated in a SPECIFIC order — not random, not all at
once. `enrich_debts_active_passive()` emits all detected Rins but leaves
them UN-ranked. This module adds the ranking layer.

Canon prioritisation (from PDF 2.3.1 "Rina-Shodhan Krama"):
    1. Pitru Rin (Father's debt)      — foundational. Unblocks all others.
    2. Matru Rin (Mother's debt)      — second after paternal line cleared.
    3. Deva / Guru Rin                — spiritual teacher / 9th house after parents.
    4. Stri / Bhratri / Bhagini Rin   — partnerships and siblings.
    5. Everything else                — Pitamah, Prapitamah, Shatru, Nara,
                                        Nri, Bhoot, Prakriti, Rishi, Sva.

Additional adjustments
----------------------
  • `dasha_active` Rins get +10 priority boost (currently live in Saala Grah).
  • Activation-house besieged by 2+ malefics   → +5 boost.
  • Rins sharing the same `activating_planet`  → treated as a single cluster
    (summed priority), so family of Mars-triggered debts surface together.
  • Pitru + Deva both present + both active    → explicit blocker:
    Deva Rin cannot be touched until Pitru Rin is in-progress.

Output shape (contract for route merge)
---------------------------------------
    {
      "ranked":                 [ debt, ... ]   # each gets priority_score + priority_rank
      "clusters":               [ {activator, debts, combined_score} ]
      "blocked_relationships":  [ {blocker, blocks, reason_en, reason_hi} ]
      "recommended_order_en":   str             # prose paragraph
      "recommended_order_hi":   str             # prose paragraph
      "source":                 "LK_DERIVED"
    }

This module is pure (no DB / FastAPI imports) so it can be called from
route code after `enrich_debts_active_passive()` without side-effects.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple


# ─────────────────────────────────────────────────────────────
# Canon priority tiers
# ─────────────────────────────────────────────────────────────
# Higher base score = higher priority. Gaps of 20 leave room for the
# +10 dasha boost and +5 besieged-house boost without tier bleed.

_CANON_PRIORITY: Dict[str, int] = {
    # Tier 1 — foundational, blocks everything
    "Pitru Rin":     100,
    # Tier 2 — maternal after paternal
    "Matru Rin":      80,
    # Tier 3 — Deva / Guru (9th house spiritual)
    "Deva Rin":       60,
    "Dev Rin":        60,   # legacy spelling
    "Guru Rin":       60,   # alternate canonical name
    # Tier 4 — partnerships, siblings
    "Stri Rin":       40,
    "Stree Rin":      40,
    "Bhratri Rin":    40,
    "Bhratu Rin":     40,   # DB variant
    "Bhagini Rin":    40,
    # Tier 5 — everything else
    "Pitamah Rin":    20,
    "Prapitamah Rin": 20,
    "Shatru Rin":     20,
    "Nara Rin":       20,
    "Nri Rin":        20,
    "Bhoot Rin":      20,
    "Prakriti Rin":   20,
    "Rishi Rin":      20,
    "Sva Rin":        20,
    "Nag Rin":        20,
}


# Explicit canon-stated blocking relationships. Key = Rin that must be
# cleared first. Value = list of Rins that cannot be worked on until the
# key Rin is at least "in progress".
_CANON_BLOCKS: Dict[str, List[str]] = {
    "Pitru Rin": ["Deva Rin", "Dev Rin", "Guru Rin"],
}


_MALEFIC_SET = {"Saturn", "Mars", "Rahu", "Ketu", "Sun"}


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def _canonical_name(debt: Dict[str, Any]) -> str:
    """Extract the canonical EN name used for priority lookup.

    Debt `name` may be a dict `{"en": "Pitru Rin", "hi": "..."}` or a
    plain string (legacy). `debt_type` is also possible. Tolerate all.
    """
    name = debt.get("name")
    if isinstance(name, dict):
        en = name.get("en") or ""
    else:
        en = name or ""
    if not en:
        dt = debt.get("debt_type")
        if isinstance(dt, dict):
            en = dt.get("en") or ""
        elif isinstance(dt, str):
            en = dt
    return str(en).strip()


def _resolve_priority(en_name: str) -> int:
    """Match debt to a canon tier. Substring match covers
    'Pitru Rin (Father's Debt)' → 'Pitru Rin'."""
    if not en_name:
        return 10
    for key, score in _CANON_PRIORITY.items():
        if key in en_name:
            return score
    return 10  # truly unknown — lowest tier


def _count_malefics_in_house(
    house: Optional[int],
    planet_positions: Optional[List[Dict[str, Any]]],
) -> int:
    if not house or not planet_positions:
        return 0
    return sum(
        1 for p in planet_positions
        if p.get("house") == house and p.get("planet") in _MALEFIC_SET
    )


def _name_for_cluster(debts: List[Dict[str, Any]]) -> List[str]:
    return [_canonical_name(d) for d in debts]


# ─────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────

def rank_compound_debts(
    enriched_debts: List[Dict[str, Any]],
    planet_positions: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Rank a list of enriched karmic debts by LK compound-remedy canon.

    Parameters
    ----------
    enriched_debts : output of `enrich_debts_active_passive()` — each
        debt must carry (at least) `name` and ideally `activating_planet`,
        `activation_house`, `activation_status`, `dasha_active`.
    planet_positions : optional. If supplied, used to detect besieged
        activation houses (2+ malefics) for the +5 priority boost.

    Returns
    -------
    dict with keys: ranked, clusters, blocked_relationships,
    recommended_order_en, recommended_order_hi, source.
    """
    if not enriched_debts:
        return {
            "ranked": [],
            "clusters": [],
            "blocked_relationships": [],
            "recommended_order_en": "No karmic debts detected — no prioritisation needed.",
            "recommended_order_hi": "कोई कर्म ऋण नहीं मिला — प्राथमिकता की आवश्यकता नहीं।",
            "source": "LK_DERIVED",
        }

    # 1. Compute priority_score per debt ────────────────────────
    scored: List[Dict[str, Any]] = []
    for debt in enriched_debts:
        # Work on a shallow copy so we don't mutate the caller's dicts
        # if they're re-used elsewhere in the response.
        d = dict(debt)
        en = _canonical_name(d)
        base = _resolve_priority(en)
        boosts: List[Dict[str, Any]] = []

        # Dasha active → +10
        if d.get("dasha_active"):
            base += 10
            boosts.append({
                "kind": "dasha_active",
                "delta": 10,
                "reason_en": "Currently live in Saala Grah — this year is the remedy window.",
                "reason_hi": "वर्तमान साला ग्रह में सक्रिय — इस वर्ष उपाय का सबसे बड़ा अवसर।",
            })

        # Activation house besieged by 2+ malefics → +5
        act_house = d.get("activation_house")
        malefic_count = _count_malefics_in_house(act_house, planet_positions)
        if malefic_count >= 2:
            base += 5
            boosts.append({
                "kind": "besieged_house",
                "delta": 5,
                "house": act_house,
                "malefic_count": malefic_count,
                "reason_en": (
                    f"Activation house H{act_house} besieged by {malefic_count} malefics — "
                    f"pressure is structural, not transient."
                ),
                "reason_hi": (
                    f"सक्रियण भाव H{act_house} में {malefic_count} पाप ग्रह — "
                    f"दबाव संरचनात्मक है, क्षणिक नहीं।"
                ),
            })

        d["priority_score"] = base
        d["priority_boosts"] = boosts
        d["canon_name"] = en
        scored.append(d)

    # 2. Cluster by activating_planet (same planet → combined) ───
    by_activator: Dict[str, List[Dict[str, Any]]] = {}
    for d in scored:
        ap = d.get("activating_planet")
        if ap:
            by_activator.setdefault(ap, []).append(d)

    clusters: List[Dict[str, Any]] = []
    for activator, members in by_activator.items():
        if len(members) < 2:
            continue  # single-member group is not a "cluster"
        combined = sum(m["priority_score"] for m in members)
        clusters.append({
            "activator": activator,
            "debts": _name_for_cluster(members),
            "member_count": len(members),
            "combined_score": combined,
            "note_en": (
                f"{len(members)} debts share {activator} as activating planet — "
                f"they compound. Remedying {activator} directly reduces all of them."
            ),
            "note_hi": (
                f"{len(members)} ऋणों का सक्रियक ग्रह {activator} है — वे संयोजित होते हैं। "
                f"{activator} का सीधा उपाय सभी को कम करता है।"
            ),
        })
        # Attach cluster_id to each member so frontend can group them.
        for m in members:
            m["cluster_activator"] = activator
            m["cluster_size"] = len(members)

    # Sort clusters by combined_score descending
    clusters.sort(key=lambda c: c["combined_score"], reverse=True)

    # 3. Detect blocked relationships ───────────────────────────
    present_names = {d["canon_name"] for d in scored}
    blocked: List[Dict[str, Any]] = []

    for blocker_name, blocked_names in _CANON_BLOCKS.items():
        if not any(blocker_name in n for n in present_names):
            continue
        # blocker exists — check each potential blocked Rin
        actually_blocked = [
            b for b in blocked_names
            if any(b in n for n in present_names)
        ]
        if not actually_blocked:
            continue

        # Canon only enforces the block when blocker is ACTIVE. If it's
        # dormant, the blocked Rins are free to be worked.
        blocker_debt = next(
            (d for d in scored if blocker_name in d["canon_name"]),
            None,
        )
        is_blocker_active = bool(
            blocker_debt
            and (
                blocker_debt.get("activation_status") == "active"
                or blocker_debt.get("dasha_active")
            )
        )
        if not is_blocker_active:
            continue

        blocked.append({
            "blocker": blocker_name,
            "blocks": actually_blocked,
            "reason_en": (
                f"Canon (PDF 2.3.1): {blocker_name} is foundational. "
                f"{', '.join(actually_blocked)} cannot be remediated until "
                f"{blocker_name} remedy is in progress — doing so invites no result."
            ),
            "reason_hi": (
                f"कैनन (PDF 2.3.1): {blocker_name} आधारभूत है। "
                f"{', '.join(actually_blocked)} का उपाय तब तक फलदायी नहीं जब तक "
                f"{blocker_name} का उपाय प्रगति पर न हो।"
            ),
        })

        # Mark the blocked debts so UI can gate them.
        for d in scored:
            if any(b in d["canon_name"] for b in actually_blocked):
                d["blocked_by"] = blocker_name
                d["blocked_reason"] = {
                    "en": f"Clear {blocker_name} first — canon requires foundational order.",
                    "hi": f"पहले {blocker_name} का उपाय — कैनन आधारभूत क्रम माँगता है।",
                }

    # 4. Rank: higher priority_score first. Tie-breaker: active > passive > latent.
    _status_rank = {"active": 2, "passive": 1, "latent": 0}
    scored.sort(
        key=lambda d: (
            d["priority_score"],
            _status_rank.get(d.get("activation_status", ""), 0),
        ),
        reverse=True,
    )
    for i, d in enumerate(scored, start=1):
        d["priority_rank"] = i

    # 5. Recommended-order prose ────────────────────────────────
    top = scored[: min(3, len(scored))]
    top_names_en = [d["canon_name"] or "(unnamed)" for d in top]

    rec_en_parts: List[str] = []
    rec_hi_parts: List[str] = []

    if top:
        rec_en_parts.append(
            "Remediate in this order: "
            + " → ".join(f"{i+1}. {n}" for i, n in enumerate(top_names_en))
            + "."
        )
        rec_hi_parts.append(
            "इस क्रम में उपाय करें: "
            + " → ".join(f"{i+1}. {n}" for i, n in enumerate(top_names_en))
            + "।"
        )

    if blocked:
        blocker_summary = "; ".join(
            f"{b['blocker']} before {', '.join(b['blocks'])}" for b in blocked
        )
        rec_en_parts.append(
            f"Hard canon blocks: {blocker_summary}. Working the blocked Rin "
            f"first gives NO result — it is canon-banned until the blocker is active."
        )
        rec_hi_parts.append(
            f"कठोर कैनन अवरोध: {blocker_summary}। अवरुद्ध ऋण पर पहले कार्य "
            f"करने से कोई फल नहीं — अवरोधक के सक्रिय होने तक कैनन-निषिद्ध।"
        )

    if clusters:
        top_cluster = clusters[0]
        rec_en_parts.append(
            f"Note: {top_cluster['member_count']} debts compound on "
            f"{top_cluster['activator']} — a single {top_cluster['activator']} "
            f"remedy simultaneously addresses "
            f"{', '.join(top_cluster['debts'])}."
        )
        rec_hi_parts.append(
            f"टिप्पणी: {top_cluster['member_count']} ऋण {top_cluster['activator']} "
            f"पर संयोजित हैं — एक ही {top_cluster['activator']} उपाय से "
            f"{', '.join(top_cluster['debts'])} सभी का समाधान होता है।"
        )

    recommended_order_en = " ".join(rec_en_parts) or "No compound analysis available."
    recommended_order_hi = " ".join(rec_hi_parts) or "कोई यौगिक विश्लेषण उपलब्ध नहीं।"

    return {
        "ranked": scored,
        "clusters": clusters,
        "blocked_relationships": blocked,
        "recommended_order_en": recommended_order_en,
        "recommended_order_hi": recommended_order_hi,
        "source": "LK_DERIVED",
    }
