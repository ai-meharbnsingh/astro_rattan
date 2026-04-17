"""
FULL verbose Lal Kitab output for Jasmine Kaur Khurana — every
engine's complete narrative, nothing truncated. Output goes to
stdout AND to docs/testing/lk_jasmine_verbose.md for easy sharing.

Production engines — ZERO duplicated calculation logic.
"""
from __future__ import annotations

import os, sys, json
from datetime import datetime, date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ─── Subject ──────────────────────────────────────────────────────────
# Using the constant name MEHARBAN is kept only for drop-in
# compatibility with the twin script. Values are Jasmine's chart.
MEHARBAN = {
    "name": "Jasmine Kaur Khurana",
    "birth_date": "1987-11-11",
    "birth_time": "03:00:00",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "tz_offset": 5.5,
    "place": "New Delhi",
}

# ─── Engines ──────────────────────────────────────────────────────────
from app.astro_engine import calculate_planet_positions
from app.routes.kp_lalkitab import _derive_lk_house, _lk_status_string, _SIGN_TO_LK_HOUSE
from app.panchang_engine import _compute_sun_times
from app.lalkitab_advanced import (
    calculate_masnui_planets, calculate_karmic_debts, identify_teva_type,
    calculate_lk_aspects, calculate_sleeping_status, calculate_kayam_grah,
    get_prohibitions, calculate_bunyaad, calculate_takkar,
    calculate_enemy_presence, calculate_karmic_debts_with_hora,
    calculate_dhoka, calculate_achanak_chot, enrich_debts_active_passive,
)
from app.lalkitab_sacrifice import analyze_sacrifice
from app.lalkitab_technical import (
    calculate_chalti_gaadi, calculate_dhur_dhur_aage, calculate_soya_ghar,
    classify_all_planet_statuses, calculate_muththi,
)
from app.lalkitab_dasha import get_saala_grah, get_dasha_timeline
from app.lalkitab_age_activation import get_age_activation
from app.lalkitab_vastu import get_vastu_diagnosis
from app.lalkitab_engine import get_remedies
from app.lalkitab_dosha import detect_lalkitab_doshas
from app.lalkitab_forbidden import get_forbidden_remedies
from app.lalkitab_milestones import get_seven_year_cycle
from app.lalkitab_prediction_studio import build_prediction_studio
from app.lalkitab_interpretations import get_all_interpretations_for_chart
from app.lalkitab_source_tags import source_of

OUT = []
def P(s=""):
    OUT.append(s)
    print(s)

def H(title, level=1, engine=None):
    tag = f"  [{source_of(engine)}]" if engine else ""
    if level == 1:
        P("\n" + "═" * 78); P(f"  {title}{tag}"); P("═" * 78)
    elif level == 2:
        P("\n" + "─" * 78); P(f"  {title}{tag}"); P("─" * 78)
    else:
        P(f"\n— {title}{tag} —")

def pick(v, hi=False):
    if v is None: return ""
    if isinstance(v, (str, int, float)): return str(v)
    if isinstance(v, dict):
        return str(v.get("hi" if hi else "en") or v.get("en") or v.get("hi") or "")
    return str(v)


def main():
    H(f"LAL KITAB VERBOSE REPORT — {MEHARBAN['name']}")
    P(f"DOB       : {MEHARBAN['birth_date']} {MEHARBAN['birth_time']} IST")
    P(f"Place     : {MEHARBAN['place']} (lat {MEHARBAN['latitude']}, lon {MEHARBAN['longitude']})")
    P(f"Generated : {datetime.now().isoformat(timespec='seconds')}")

    # Chart
    chart = calculate_planet_positions(
        birth_date=MEHARBAN["birth_date"], birth_time=MEHARBAN["birth_time"],
        latitude=MEHARBAN["latitude"], longitude=MEHARBAN["longitude"],
        tz_offset=MEHARBAN["tz_offset"],
    )
    pp = [{"planet": n, "house": _derive_lk_house(info), "sign": info["sign"]}
          for n, info in chart["planets"].items()]
    p_map = {x["planet"]: x["house"] for x in pp}

    H("1 · CORE CHART")
    P(f"Ayanamsa (Lahiri) : {chart.get('ayanamsa_value')}°")
    P(f"Ascendant         : {chart['ascendant']['sign']} "
      f"{round(chart['ascendant']['longitude'], 2)}°  "
      f"(Not used in Lal Kitab — shown for reference only)")
    P(f"\n{'Planet':10}{'Sid°':>9}  {'Sign':<12}{'Nak':<15}{'Pada':>5}  "
      f"{'LKH':>4}  {'Status':<40}")
    P("-" * 100)
    for n, info in chart["planets"].items():
        P(f"{n:10}{round(info['longitude'],2):>9}  {info['sign']:<12}"
          f"{info['nakshatra']:<15}{info.get('nakshatra_pada',0):>5}  "
          f"{_derive_lk_house(info):>4}  {_lk_status_string(info)[:40]:<40}")

    # House map
    H("2 · LK HOUSE MAP")
    SIGN_FOR = {v: k for k, v in _SIGN_TO_LK_HOUSE.items()}
    for h in range(1, 13):
        planets = [x["planet"] for x in pp if x["house"] == h] or ["—"]
        P(f"  H{h:<2}  {SIGN_FOR[h]:<14}{', '.join(planets)}")

    # Teva
    H("3 · TEVA TYPOLOGY (full)", engine="identify_teva_type")
    teva = identify_teva_type(pp)
    for t in ("andha", "ratondha", "dharmi", "nabalig", "khali"):
        flag = "★ ACTIVE" if teva.get(f"is_{t}") else "inactive"
        desc_en = pick(teva.get("description", {}).get(t, {}), hi=False)
        desc_hi = pick(teva.get("description", {}).get(t, {}), hi=True)
        P(f"\n• {t.capitalize():<10} [{flag}]")
        P(f"  EN: {desc_en}")
        P(f"  HI: {desc_hi}")

    # Karmic Rin — FULL
    H("4 · KARMIC RIN (full text, all detected debts)", engine="calculate_karmic_debts")
    debts = calculate_karmic_debts(pp)
    if not debts:
        P("No karmic debts detected.")
    for i, d in enumerate(debts, 1):
        P(f"\n[{i}] {pick(d.get('name'))}  ({pick(d.get('type'))})")
        P(f"    Trigger       : {pick(d.get('reason'))}")
        P(f"    Manifestation : {pick(d.get('manifestation'))}")
        P(f"    Remedy        : {pick(d.get('remedy'))}")
        P(f"    (HI remedy)   : {pick(d.get('remedy'), hi=True)}")

    # Hora debt
    H("5 · HORA-BASED 10th DEBT (full)", engine="calculate_karmic_debts_with_hora")
    birth_dt = datetime.combine(
        datetime.strptime(MEHARBAN["birth_date"], "%Y-%m-%d").date(),
        datetime.strptime(MEHARBAN["birth_time"], "%H:%M:%S").time())
    sun_times = _compute_sun_times(MEHARBAN["birth_date"], MEHARBAN["latitude"],
                                    MEHARBAN["longitude"], MEHARBAN["tz_offset"])
    sr_str = sun_times.get("sunrise")
    sr_time = datetime.strptime(sr_str, "%H:%M").time() if sr_str and sr_str != "--:--" else None
    hora_res = calculate_karmic_debts_with_hora(pp, birth_datetime=birth_dt, sunrise_time=sr_time)
    hora = hora_res.get("hora_analysis") or {}
    P(f"Sunrise       : {sr_str}")
    P(f"Day lord      : {hora.get('day_lord')}  ({hora.get('weekday_name')})")
    P(f"Hora lord     : {hora.get('hora_lord')}")
    P(f"Hrs since SR  : {hora.get('hours_elapsed_since_sunrise')}")
    bd = hora.get("base_debt") or {}
    P(f"Base LK debt  : {bd.get('debt')}  |  {bd.get('debt_hi')}")
    desc = bd.get("description", {})
    P(f"  EN meaning  : {desc.get('en','')}")
    P(f"  HI meaning  : {desc.get('hi','')}")
    infl = hora_res.get("hora_influence") or {}
    P(f"Hora influence: added_new_debt={infl.get('added_new_debt')}  "
      f"reason={infl.get('reason','')}")
    for c in (hora_res.get("conflicts_resolved") or []):
        P(f"\nConflict resolved: {c.get('type')}")
        P(f"  from  : {c.get('from')}  →  to: {c.get('to')}")
        P(f"  reason: {pick(c.get('reason'))}")

    # Active/passive enrichment
    H("6 · ACTIVE vs PASSIVE RIN (full urgency)", engine="enrich_debts_active_passive")
    for d in enrich_debts_active_passive(debts, pp):
        P(f"\n{pick(d.get('name')):<20} status={d.get('activation_status')}  "
          f"house={d.get('activation_house')}  "
          f"activating_planet={d.get('activating_planet')}")
        if d.get("activation_urgency"):
            P(f"  urgency (EN)    : {pick(d['activation_urgency'])}")
            P(f"  urgency (HI)    : {pick(d['activation_urgency'], hi=True)}")
        if pick(d.get("activates_during")):
            P(f"  activates_during: {pick(d.get('activates_during'))}")
        if pick(d.get("life_area")):
            P(f"  life_area       : {pick(d.get('life_area'))}")

    # Masnui
    H("7 · MASNUI GRAH (full)", engine="calculate_masnui_planets")
    masnui = calculate_masnui_planets(pp)
    mlist = masnui.get("masnui_planets") or []
    if not mlist:
        empty = masnui.get("empty_interpretation") or {}
        P(f"EN: {empty.get('en', 'No masnui planets formed.')}")
        P(f"HI: {empty.get('hi', '')}")
    for m in mlist:
        P(f"\nHouse {m.get('house')}: {' + '.join(m.get('formed_by') or [])} → "
          f"{m.get('masnui_planet')}  quality={m.get('quality')}")
        P(f"  affected_domain: {pick(m.get('affected_domain'))}")
    prof = masnui.get("psychological_profile") or {}
    if prof:
        P(f"\nPsychological profile:")
        P(f"  Dominant quality : {pick(prof.get('dominant_quality'))}")
        P(f"  Behavior         : {pick(prof.get('behavioral_tendencies'))}")
        P(f"  Relationship     : {pick(prof.get('relationship_approach'))}")
    for n in (masnui.get("predictive_notes") or []):
        P(f"  note: {pick(n.get('note'))}")

    # Prohibitions
    H("8 · PROHIBITIONS (FULL text)", engine="get_prohibitions")
    for p in (get_prohibitions(pp) or []):
        P(f"\n• {p['planet']} in H{p['house']}")
        P(f"    Category      : {pick(p.get('category'))}")
        P(f"    Forbidden     : {pick(p.get('forbidden'))}")
        P(f"    Backlash risk : {pick(p.get('backlash_risk'))}")

    # Forbidden remedies (separate engine)
    H("9 · FORBIDDEN REMEDIES (cross-check engine)", engine="get_forbidden_remedies")
    for fr in (get_forbidden_remedies(pp) or [])[:15]:
        P(f"\n• {fr}")

    # Bunyaad full
    H("10 · BUNYAAD (foundation interpretations)", engine="calculate_bunyaad")
    b = calculate_bunyaad(pp)
    P(f"Afflicted (collapsed) : {b.get('collapsed_planets') or []}")
    P(f"Strong (friends)      : {b.get('strong_foundations') or []}")
    P(f"Neutral               : {b.get('neutral_foundations') or []}")
    P(f"Clear (empty)         : {b.get('clear_foundations') or []}")
    for planet, info in (b.get("planets") or {}).items():
        P(f"\n• {planet}  pakka H{info.get('pakka_ghar')}  "
          f"bunyaad H{info.get('bunyaad_house')}  "
          f"status={info.get('bunyaad_status')}")
        if info.get("friends_in_bunyaad"):
            P(f"   friends in bunyaad : {info.get('friends_in_bunyaad')}")
        if info.get("enemies_in_bunyaad"):
            P(f"   enemies in bunyaad : {info.get('enemies_in_bunyaad')}")
        if info.get("neutrals_in_bunyaad"):
            P(f"   neutrals in bunyaad: {info.get('neutrals_in_bunyaad')}")
        P(f"   EN: {info.get('interpretation_en','')}")
        P(f"   HI: {info.get('interpretation_hi','')}")

    # Takkar full
    H("11 · TAKKAR (collision, full interpretations)", engine="calculate_takkar")
    t = calculate_takkar(pp)
    P(f"Destructive={t.get('destructive_count',0)}  "
      f"Mild={t.get('mild_count',0)}  "
      f"Moderate={t.get('moderate_count',0)}  "
      f"Philosophical={t.get('philosophical_count',0)}")
    P(f"Most vulnerable: {t.get('most_vulnerable_planet')}  "
      f"Safe: {t.get('safe_planets')}")
    sub_vuln = t.get("vulnerability_scores") or {}
    if sub_vuln:
        P("\n— Vulnerability ranking (weighted: base + dusthana + debil + H8) —")
        for rank, name in enumerate(t.get("vulnerability_ranking") or [], 1):
            v = sub_vuln.get(name, {})
            tag = f"[{v.get('vulnerability_reason','?')}]"
            P(f"  {rank}. {name:<10}  {v.get('breakdown','')}  {tag}")
            expl = v.get("vulnerability_explanation")
            if expl and v.get("score", 0) > 0:
                P(f"      → {expl}")
    for c in (t.get("collisions") or []):
        P(f"\n• {c.get('attacker')} → {c.get('receiver')}  axis {c.get('axis')}  "
          f"severity {c.get('severity')}")
        P(f"   EN: {c.get('interpretation_en','')}")
        P(f"   HI: {c.get('interpretation_hi','')}")

    # Enemy siege full
    H("12 · ENEMY PRESENCE / SIEGE (full interpretations)", engine="calculate_enemy_presence")
    ep = calculate_enemy_presence(pp)
    P(f"Most besieged : {ep.get('most_besieged','—')}")
    P(f"Least besieged: {ep.get('least_besieged','—')}")
    for planet, info in (ep.get("planets") or {}).items():
        P(f"\n• {planet}  siege={info.get('enemy_siege_level','—')}  "
          f"enemies={info.get('total_enemies',0)}  "
          f"in_pakka_ghar={info.get('enemies_in_pakka_ghar',0)}")
        P(f"   EN: {info.get('interpretation_en','')}")
        P(f"   HI: {info.get('interpretation_hi','')}")

    # Dhoka / Achanak
    H("13 · RELATIONSHIP PATTERNS (Dhoka + Achanak Chot, full)", engine="calculate_dhoka")
    H("Dhoka (deception)", 2)
    for d in calculate_dhoka(pp) or []:
        P(f"\n• {d.get('dhoka_name')}  H{d.get('source_house')} → H{d.get('target_house')}")
        P(f"   severity={d.get('severity')}  malefics={d.get('malefics_causing')}")
        P(f"   description EN: {pick(d.get('description'))}")
        P(f"   description HI: {pick(d.get('description'), hi=True)}")
        P(f"   remedy      EN: {pick(d.get('remedy'))}")
    H("Achanak Chot (sudden strike)", 2)
    for a in calculate_achanak_chot(pp) or []:
        P(f"\n• {a.get('strike_name')}  striker H{a.get('striker_house')} → victim H{a.get('victim_house')}")
        P(f"   critical={a.get('is_critical')}  malefics={a.get('malefics')}")
        P(f"   description EN: {pick(a.get('description'))}")
        P(f"   warning     EN: {pick(a.get('warning'))}")

    # Sacrifice
    H("14 · BALI KA BAKRA (sacrifice, full messages)", engine="analyze_sacrifice")
    aspects = calculate_lk_aspects(pp) or {}
    sac = analyze_sacrifice(pp, aspects)
    results = sac.get("results") if isinstance(sac, dict) else sac
    if not results:
        P("No sacrifice patterns detected (which itself is good — no planet is consuming another).")
    for r in results or []:
        P(f"\n• Rule {r.get('rule_id')}  {r.get('sacrificer')} sacrifices {r.get('victim')}")
        P(f"   severity={r.get('severity')}  growth={r.get('growth_area')}  cost={r.get('cost_area')}")
        P(f"   message EN: {pick(r.get('message'))}")
        P(f"   message HI: {pick(r.get('message'), hi=True)}")
        P(f"   remedy  EN: {pick(r.get('remedy'))}")

    # Technical
    H("15 · TECHNICAL (Chalti Gaadi · Dhur-dhur-aage · Soya Ghar · Statuses · Muththi)")
    cg = calculate_chalti_gaadi(pp)
    H("Chalti Gaadi", 3, engine="calculate_chalti_gaadi")
    P(f"Engine   : {cg.get('engine')}")
    P(f"Passenger: {cg.get('passenger')}")
    P(f"Brakes   : {cg.get('brakes')}")
    P(f"Status   : {cg.get('train_status')}")
    P(f"EN: {pick(cg.get('interpretation'))}")
    P(f"HI: {pick(cg.get('interpretation'), hi=True)}")
    for rule in cg.get("specific_rules") or []:
        P(f"  • {rule.get('rule')}: {pick(rule.get('note'))}")

    H("Dhur-dhur-aage", 3, engine="calculate_dhur_dhur_aage")
    dd = calculate_dhur_dhur_aage(pp)
    P(f"Most pushful: {dd.get('most_pushful_planet')}")
    P(f"Most pushed : {dd.get('most_pushed_planet')}")
    for push in (dd.get("pushes") or []):
        P(f"  {push.get('pusher')} → {push.get('receiver')}  direction={push.get('direction')}")

    H("Soya Ghar (per-house)", 3, engine="calculate_soya_ghar")
    try:
        soya = calculate_soya_ghar(pp)
        P(f"Awake    : {soya.get('awake_houses')}")
        P(f"Sleeping : {soya.get('sleeping_houses')}")
        for eff in (soya.get("sleeping_house_effects") or []):
            P(f"\n• H{eff.get('house')}")
            P(f"   effect EN: {pick(eff.get('effect'))}")
            P(f"   remedy EN: {pick(eff.get('remedy'))}")
    except Exception as e:
        P(f"(soya skipped: {e})")

    H("Planet statuses (sarkari / pardesi / zakhmi / bhedi / gair_sarkari)", 3, engine="classify_all_planet_statuses")
    for row in classify_all_planet_statuses(pp):
        flags = [k for k in ("sarkari","gair_sarkari","bhedi","zakhmi","pardesi")
                 if row.get(k)]
        P(f"\n{row.get('planet'):<10}  [{', '.join(flags) or 'neutral'}]")
        for k, v in (row.get("details") or {}).items():
            P(f"   {k}: {v}")

    H("Muththi", 3, engine="calculate_muththi")
    P(f"{calculate_muththi(pp)}")

    # Relations / Rules / Doshas
    # Split Lal-Kitab doshas into the main block (LK canon) and a
    # separate "Vedic overlays" block so only pure LK material sits
    # alongside the other LK_CANONICAL sections.
    all_doshas = detect_lalkitab_doshas(pp) or []
    lk_doshas = [d for d in all_doshas if d.get("source") != "vedic_influenced"]
    vedic_doshas = [d for d in all_doshas if d.get("source") == "vedic_influenced"]

    def _print_dosha(d):
        flag = "★ DETECTED" if d.get("detected") else "  not detected"
        src = d.get("source")
        src_tag = f"  source={src}" if src else ""
        P(f"\n• {d.get('name_en')} ({d.get('name_hi')}) — severity {d.get('severity')}  [{flag}]{src_tag}")
        P(f"   EN: {d.get('description_en','')}")
        P(f"   HI: {d.get('description_hi','')}")
        P(f"   remedy EN: {d.get('remedy_hint_en','')}")
        P(f"   remedy HI: {d.get('remedy_hint_hi','')}")
        if d.get("affected_planets"):
            P(f"   affected planets: {d.get('affected_planets')}")

    H("16 · DOSHAS (Lal Kitab canon only)", engine="detect_lalkitab_doshas")
    if not lk_doshas:
        P("\n(No Lal-Kitab-canon doshas to display.)")
    for d in lk_doshas:
        _print_dosha(d)

    # ── 16-B · VEDIC OVERLAYS (reference only — not claimed as LK) ──
    H("16-B · VEDIC OVERLAYS (for reference only — not LK)")
    P("Items below are detected by classical Vedic/Parashari rules but "
      "are NOT part of the Lal Kitab 1952 canon. Shown for cross-")
    P("reference only — do NOT treat as Lal Kitab guidance.")
    if not vedic_doshas:
        P("\n(No Vedic-overlay items active for this chart.)")
    for d in vedic_doshas:
        _print_dosha(d)

    # Vastu
    H("17 · VASTU (full warnings + fixes)", engine="get_vastu_diagnosis")
    v = get_vastu_diagnosis(pp) or {}
    P(f"Critical count: {v.get('critical_count', 0)}")
    for w in (v.get("planet_warnings") or []):
        P(f"\n• {w.get('planet')} in H{w.get('house')}  "
          f"direction {pick(w.get('direction'))}  "
          f"zone {pick(w.get('zone'))}  "
          f"{'★CRITICAL' if w.get('is_critical') else ''}")
        P(f"   warn EN: {pick(w.get('warning'))}")
        P(f"   warn HI: {pick(w.get('warning'), hi=True)}")
        P(f"   fix  EN: {pick(w.get('fix'))}")
        P(f"   fix  HI: {pick(w.get('fix'), hi=True)}")

    # Timing
    H("18 · TIMING (Saala Grah · Dasha · 7-year cycle · Age Activation)", engine="get_dasha_timeline")
    today = date.today().isoformat()
    age_res = get_age_activation(MEHARBAN["birth_date"], today)
    age_years = age_res.get("age_years", 0) if isinstance(age_res, dict) else 0
    P(f"\nAge today: {age_years}")
    active = age_res.get("active") if isinstance(age_res, dict) else None
    if active:
        P(f"Active LK age-period: {active.get('planet')}  "
          f"({active.get('age_start')}–{active.get('age_end')})")
    for p in (age_res.get("periods") or []):
        P(f"  • {p.get('planet'):<10}  ages {p.get('age_start'):>2}–{p.get('age_end'):<2}")

    dasha = get_dasha_timeline(MEHARBAN["birth_date"], today)
    H("Dasha timeline", 2)
    curr = dasha.get("current_saala_grah") or {}
    P(f"\nCurrent saala grah (age {curr.get('age')}, {curr.get('started_year')}–{curr.get('ends_year')}):")
    P(f"  Planet: {curr.get('planet')} ({curr.get('planet_hi')})")
    P(f"  EN: {curr.get('en_desc','')}")
    P(f"  HI: {curr.get('hi_desc','')}")
    nxt = dasha.get("next_saala_grah") or {}
    if nxt:
        P(f"\nNext saala grah (from age {nxt.get('starts_at_age')}, {nxt.get('starts_year')}):")
        P(f"  Planet: {nxt.get('planet')} ({nxt.get('planet_hi')})")
        P(f"  EN: {nxt.get('en_desc','')}")
    P(f"\nLife phase    : {dasha.get('life_phase')}")
    P(f"Years in phase: {dasha.get('years_into_phase')}  remaining: {dasha.get('years_remaining_in_phase')}")
    H("Last 5 past age-periods", 2)
    for p in (dasha.get("past_periods") or [])[-5:]:
        P(f"\n age {p.get('age')} ({p.get('year')}): {p.get('planet')} ({p.get('planet_hi')})")
        P(f"   EN: {p.get('en_desc','')}")
    H("Next 5 age-periods", 2)
    for p in (dasha.get("upcoming_periods") or [])[:5]:
        P(f"\n age {p.get('age')} ({p.get('year')}): {p.get('planet')} ({p.get('planet_hi')})")
        P(f"   EN: {p.get('en_desc','')}")

    H("7-year cycle", 2, engine="get_seven_year_cycle")
    cyc = get_seven_year_cycle(age_years, pp)
    active_c = cyc.get("active_cycle") or {}
    P(f"\nActive cycle   : #{active_c.get('cycle_number')}  ages {active_c.get('age_range')}  ruler {active_c.get('ruler')} (H{active_c.get('ruler_house')})")
    P(f"  domain : {pick(active_c.get('domain'))}")
    P(f"  focus  : {pick(active_c.get('focus'))}")
    P(f"  years into cycle: {active_c.get('years_into_cycle')}  remaining: {active_c.get('years_remaining')}")
    prev_c = cyc.get("previous_cycle") or {}
    P(f"\nPrevious cycle : {pick(prev_c.get('domain'))}  ruler {prev_c.get('ruler')}")
    next_c = cyc.get("next_cycle") or {}
    P(f"Next cycle     : {pick(next_c.get('domain'))}  ruler {next_c.get('ruler')}  starts age {next_c.get('starts_at_age')}")

    # Prediction Studio FULL
    H("19 · PREDICTION STUDIO (FULL — every area, positive/caution/remedy)", engine="build_prediction_studio")
    p_lons = {n: info["longitude"] for n, info in chart["planets"].items()}
    ps = build_prediction_studio(p_map, p_lons)
    for row in (ps.get("areas") or []):
        P(f"\n◆ {row.get('title_en')}  ({row.get('title_hi')})")
        P(f"  {row.get('label','—'):<16}  (raw score {row.get('score')}/100, "
          f"confidence={row.get('confidence')})")
        # 3-part cause structure
        P(f"  PRIMARY  CAUSE     EN: {pick(row.get('primary_cause'))}")
        P(f"  SECONDARY MODIFIER EN: {pick(row.get('secondary_modifier'))}")
        P(f"  SUPPORTING FACTOR  EN: {pick(row.get('supporting_factor'))}")
        P(f"  POSITIVE EN: {row.get('positive_en','')}")
        P(f"  POSITIVE HI: {row.get('positive_hi','')}")
        P(f"  CAUTION  EN: {row.get('caution_en','')}")
        P(f"  CAUTION  HI: {row.get('caution_hi','')}")
        P(f"  REMEDY   EN: {row.get('remedy_en','')}")
        P(f"  REMEDY   HI: {row.get('remedy_hi','')}")
        P(f"  trace: {row.get('trace')}")

    # Per-planet remedies
    H("20 · PER-PLANET REMEDIES (engine-generated, full)", engine="get_remedies")
    rem_by_planet = get_remedies({p["planet"]: p["sign"] for p in pp}, chart)
    for planet, info in (rem_by_planet or {}).items():
        rem = info.get("remedy") or {}
        P(f"\n◆ {planet}  (LK H{info.get('lk_house')})  dignity={info.get('dignity')}  "
          f"strength={info.get('strength')}  has_remedy={info.get('has_remedy')}")
        P(f"  Remedy EN : {rem.get('en','') if isinstance(rem, dict) else rem}")
        P(f"  Remedy HI : {rem.get('hi','') if isinstance(rem, dict) else ''}")
        P(f"  Material  : {rem.get('material','') if isinstance(rem, dict) else ''}")
        P(f"  Day       : {rem.get('day','') if isinstance(rem, dict) else ''}")
        P(f"  Urgency   : {rem.get('urgency','') if isinstance(rem, dict) else ''}")
        if info.get("afflictions"):
            P(f"  Afflictions: {info.get('afflictions')}")

    # Grahfal — FULL per-planet-in-house
    H("21 · GRAHFAL / BHAVFAL (full LK 1952 interpretations, per planet)", engine="get_all_interpretations_for_chart")
    for row in (get_all_interpretations_for_chart(pp) or []):
        P(f"\n◆ {row.get('planet')} in H{row.get('house')}")
        P(f"  EN: {pick(row.get('effect') or row.get('effect_en'))}")
        P(f"  HI: {pick(row.get('effect') or row.get('effect_hi'), hi=True)}")
        cond = row.get('conditions') or row.get('condition')
        if cond:
            P(f"  conditions: {pick(cond)}")
        rem = row.get('remedy') or row.get('remedy_en')
        if rem:
            P(f"  remedy    : {pick(rem)}")

    H("DONE", 1)

    # Dump to markdown file alongside the project's docs.
    out_path = os.path.join(ROOT, "docs", "testing", "lk_jasmine_verbose.md")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write("\n".join(OUT))
    P(f"\n(Full report also saved to {out_path} — "
      f"{sum(len(x) for x in OUT)//1024} KB)")


if __name__ == "__main__":
    main()
