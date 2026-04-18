"""
app/lalkitab_source_tags.py

Single source of truth for the provenance tag on every Lal Kitab engine.
Each output carries a `source` field so the UI / auditor can distinguish:

  LK_CANONICAL  — text or rule comes directly from Lal Kitab 1952
                  (Pt. Roop Chand Joshi's original canon). Includes
                  classical planet-in-house interpretations, the 9 Rin
                  triggers, Teva types, Masnui rules, Takkar axis,
                  Hora debts, Prohibitions, per-planet remedies.

  LK_DERIVED    — logical inference from canonical LK principles but
                  NOT quoted verbatim from the 1952 text. Bunyaad,
                  Dhoka, Achanak Chot, Vastu overlay, Soya Ghar,
                  Sacrifice rules, Enemy Siege scoring, 7-year cycle.

  PRODUCT       — UX feature or composite score we have built on top
                  of the above. Not claimed as Lal Kitab canon:
                  Chalti Gaadi narrative, Prediction Studio scores,
                  Dhur-dhur-aage visual, Karmic Confidence meter.

Rule: every top-level engine function MUST stamp its output with one
of these constants, so the frontend can label the section accordingly.
"""

LK_CANONICAL = "LK_CANONICAL"
LK_DERIVED = "LK_DERIVED"
LK_ADAPTED = "LK_ADAPTED"       # Rule applied to a scenario LK 1952 didn't explicitly cover
PRODUCT = "PRODUCT"
ML_SCORED = "ML_SCORED"         # Score produced by a learned/heuristic model
HEURISTIC = "HEURISTIC"         # Heuristic scoring / empirical weighting (not ML)

# Vedic overlay — used for dosha engine and future cross-system tags.
# Case-normalised upper-case variant is canonical; lower-case alias kept
# for backward compatibility with existing payloads (Codex D2 audit).
VEDIC_INFLUENCED = "VEDIC_INFLUENCED"
VEDIC_INFLUENCED_LEGACY = "vedic_influenced"

# Per-engine classification. Key = function name. Value = source tag.
# This lets callers (frontend, tests, audits) query the tag without
# having to inspect every engine file.
ENGINE_SOURCE = {
    # ─── LK_CANONICAL (direct from 1952 text) ────────────────────────
    # Note: the 9 Rin NAMES / manifestations are canonical, but the
    # detection rules (planet-in-house triggers) are a codified
    # inference layer — Codex audit classifies Rin DETECTION as
    # LK_DERIVED.
    "calculate_karmic_debts":              LK_DERIVED,     # Rin detection rules
    "calculate_karmic_debts_with_hora":    LK_CANONICAL,   # Hora 10th debt
    "calculate_hora_lord":                 LK_CANONICAL,
    "identify_teva_type":                  LK_CANONICAL,   # Andha/Ratondha/etc
    "calculate_masnui_planets":            LK_CANONICAL,   # Artificial planets
    "calculate_lk_aspects":                LK_CANONICAL,   # Classical drishti
    "get_prohibitions":                    LK_CANONICAL,   # 11 forbidden rules
    "get_forbidden_remedies":              LK_CANONICAL,
    "get_remedies":                        LK_CANONICAL,   # Per-planet LK remedy
    "get_remedy_precautions":              LK_CANONICAL,   # Savdhaniyan (LK 4.08 + 4.09)
    "detect_andhe_grah":                   LK_CANONICAL,   # Blind planets (LK 2.12 + 4.14)
    "get_lk_house_interpretation":         LK_CANONICAL,   # Grahfal/Bhavfal
    "get_all_interpretations_for_chart":   LK_CANONICAL,
    "get_lk_validated_remedies":           LK_CANONICAL,
    "calculate_takkar":                    LK_CANONICAL,   # Opposite-axis rule
    "detect_lalkitab_doshas":              LK_CANONICAL,
    "classify_all_planet_statuses":        LK_CANONICAL,   # sarkari/pardesi/…
    "get_saala_grah":                      LK_CANONICAL,
    "get_dasha_timeline":                  LK_CANONICAL,
    "get_age_activation":                  LK_CANONICAL,

    # ─── LK_DERIVED (inference from canon, not verbatim) ─────────────
    "calculate_bunyaad":                   LK_DERIVED,
    "calculate_enemy_presence":            LK_DERIVED,
    "calculate_dhoka":                     LK_DERIVED,
    "calculate_achanak_chot":              LK_DERIVED,
    "analyze_sacrifice":                   LK_DERIVED,
    "calculate_sleeping_status":           LK_DERIVED,
    "calculate_kayam_grah":                LK_DERIVED,
    "calculate_soya_ghar":                 LK_DERIVED,
    "calculate_muththi":                   LK_DERIVED,
    "enrich_debts_active_passive":         LK_DERIVED,
    "get_vastu_diagnosis":                 LK_DERIVED,
    "get_seven_year_cycle":                LK_DERIVED,
    "calculate_age_milestones":            LK_DERIVED,
    "build_relations":                     LK_DERIVED,
    "build_rules":                         LK_DERIVED,
    "calculate_dhur_dhur_aage":            LK_DERIVED,

    # ─── PRODUCT (UX layer, not claimed as LK) ───────────────────────
    "calculate_chalti_gaadi":              PRODUCT,
    "build_prediction_studio":             PRODUCT,
    "calculate_palm_correlations":         PRODUCT,  # Samudrik overlay
    "calculate_family_harmony":            PRODUCT,
    "generate_cross_waking_narrative":     PRODUCT,
}


def source_of(engine_name: str) -> str:
    """Return the source tag for a given engine function name.

    Unknown engines fall back to `PRODUCT` — never `LK_CANONICAL` — so
    unclassified features never accidentally masquerade as canon.
    """
    return ENGINE_SOURCE.get(engine_name, PRODUCT)
