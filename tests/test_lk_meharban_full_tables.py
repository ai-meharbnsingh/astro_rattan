"""
Full Lal Kitab verification tables for a given chart.

This file is a READ-ONLY probe — every table is produced by calling the
production engines in app/ directly (no duplicated calculation logic here).
Edit the MEHARBAN constant at the top if you want a different chart; the
rest of the file just prints every engine's output.

Run:
    python3 tests/test_lk_meharban_full_tables.py
"""
from __future__ import annotations

import os
import sys
from datetime import datetime, date

# Make sure we can import the app.* modules when running this file directly.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ═══════════════════════════════════════════════════════════════════════
#  SUBJECT — change this block if you want a different chart
# ═══════════════════════════════════════════════════════════════════════
MEHARBAN = {
    "name": "Meharban Singh Upneja",
    "birth_date": "1985-08-23",       # YYYY-MM-DD
    "birth_time": "23:15:00",         # HH:MM:SS (24h)
    "latitude": 28.6139,              # Delhi
    "longitude": 77.2090,
    "tz_offset": 5.5,                 # IST
}

# ═══════════════════════════════════════════════════════════════════════
#  ENGINE IMPORTS — every table below is derived from these production
#  modules. No calculation is duplicated in this file.
# ═══════════════════════════════════════════════════════════════════════
from app.astro_engine import calculate_planet_positions
from app.routes.kp_lalkitab import _derive_lk_house, _SIGN_TO_LK_HOUSE
from app.lalkitab_advanced import (
    calculate_masnui_planets,
    calculate_karmic_debts,
    identify_teva_type,
    calculate_lk_aspects,
    calculate_sleeping_status,
    calculate_kayam_grah,
    get_prohibitions,
    calculate_bunyaad,
    calculate_takkar,
    calculate_enemy_presence,
    calculate_karmic_debts_with_hora,
    calculate_dhoka,
    calculate_achanak_chot,
    enrich_debts_active_passive,
)
from app.lalkitab_sacrifice import analyze_sacrifice
from app.lalkitab_technical import (
    calculate_chalti_gaadi,
    calculate_dhur_dhur_aage,
    calculate_soya_ghar,
    classify_all_planet_statuses,
    calculate_muththi,
)
from app.lalkitab_dasha import get_saala_grah, get_dasha_timeline
from app.lalkitab_age_activation import get_age_activation
from app.lalkitab_vastu import get_vastu_diagnosis
from app.lalkitab_engine import get_remedies, get_planet_strength_detailed
from app.lalkitab_dosha import detect_lalkitab_doshas
from app.lalkitab_relations_engine import build_relations
from app.lalkitab_rules_engine import build_rules
from app.lalkitab_forbidden import get_forbidden_remedies
from app.lalkitab_milestones import calculate_age_milestones, get_seven_year_cycle
from app.lalkitab_palmistry import get_palm_zones
from app.lalkitab_prediction_studio import build_prediction_studio
from app.lalkitab_interpretations import get_all_interpretations_for_chart

# ─────────────────────────────────────────────────────────────────────
#  Helpers (print formatting only — no astrology logic)
# ─────────────────────────────────────────────────────────────────────
def hr(title: str, char: str = "═") -> None:
    print()
    print(char * 78)
    print(f"  {title}")
    print(char * 78)


def sub(title: str) -> None:
    print()
    print(f"── {title} " + "─" * max(3, 73 - len(title)))


def pick(val, isHi=False):
    """Safe-render for bilingual {en, hi} objects."""
    if val is None:
        return ""
    if isinstance(val, (str, int, float)):
        return str(val)
    if isinstance(val, dict):
        return str(val.get("hi" if isHi else "en") or val.get("en") or val.get("hi") or "")
    return str(val)


# ─────────────────────────────────────────────────────────────────────
#  1) CORE CHART — Swiss Ephemeris + LK fixed-house rule
# ─────────────────────────────────────────────────────────────────────
def table_core_chart(chart, planet_positions_lk):
    hr("1 · CORE CHART (Swiss Ephemeris + LK fixed-house rule)")
    print(f"Subject      : {MEHARBAN['name']}")
    print(f"DOB          : {MEHARBAN['birth_date']} {MEHARBAN['birth_time']} "
          f"(TZ +{MEHARBAN['tz_offset']})")
    print(f"Location     : lat {MEHARBAN['latitude']}, lon {MEHARBAN['longitude']}")
    print(f"Ayanamsa     : {chart.get('ayanamsa_system', 'lahiri')} "
          f"= {chart.get('ayanamsa_value', '—')}°")
    print(f"Ascendant    : {chart['ascendant']['sign']} "
          f"{round(chart['ascendant']['longitude'], 2)}°  "
          f"(Not used in Lal Kitab — shown for reference only)")

    sub("Planet table (sidereal Lahiri)")
    print(f"{'Planet':10} {'Sid°':>8}  {'Sign':<12}{'Nak':<16}{'WSH':>4}  {'LK':>4}  Retro")
    print("-" * 78)
    for p, info in chart["planets"].items():
        lk = _derive_lk_house(info)            # <-- production function
        retro = "R" if info.get("retrograde") else ""
        print(f"{p:10} {round(info['longitude'], 2):>8}  "
              f"{info['sign']:<12}{info['nakshatra']:<16}"
              f"{info['house']:>4}  {lk:>4}    {retro}")
    print()
    print("WSH = Whole-Sign house from Ascendant (for KP / Parashari).")
    print("LK  = Lal Kitab fixed house (Aries=1 … Pisces=12).")


# ─────────────────────────────────────────────────────────────────────
#  2) LK HOUSE MAP — which planets sit in which LK house
# ─────────────────────────────────────────────────────────────────────
def table_house_map(planet_positions_lk):
    hr("2 · LK HOUSE MAP (Aries=H1 … Pisces=H12)")
    house_to_planets: dict[int, list[str]] = {h: [] for h in range(1, 13)}
    SIGN_FOR = {v: k for k, v in _SIGN_TO_LK_HOUSE.items()}
    for p in planet_positions_lk:
        house_to_planets[p["house"]].append(p["planet"])
    print(f"{'House':<6}{'Sign':<14}Planets")
    print("-" * 60)
    for h in range(1, 13):
        planets = ", ".join(house_to_planets[h]) or "—"
        print(f"H{h:<5}{SIGN_FOR[h]:<14}{planets}")


# ─────────────────────────────────────────────────────────────────────
#  3) PLANET STATUS (dignity, combust, vargottama, sandhi)
# ─────────────────────────────────────────────────────────────────────
def table_planet_status(chart):
    hr("3 · PLANET STATUS (from astro_engine)")
    print(f"{'Planet':10}{'Status':<42}{'Combust':<9}{'Varg':<6}{'Sandhi':<7}")
    print("-" * 78)
    for p, info in chart["planets"].items():
        status = info.get("status", "")
        c = "Y" if info.get("is_combust") else ""
        v = "Y" if info.get("is_vargottama") else ""
        s = "Y" if info.get("is_sandhi") else ""
        print(f"{p:10}{status[:41]:<42}{c:<9}{v:<6}{s:<7}")


# ─────────────────────────────────────────────────────────────────────
#  4) TEVA TYPE — Andha/Ratondha/Dharmi/Nabalig/Khali
# ─────────────────────────────────────────────────────────────────────
def table_teva(planet_positions_lk):
    hr("4 · TEVA TYPOLOGY")
    teva = identify_teva_type(planet_positions_lk)
    for tname in ("andha", "ratondha", "dharmi", "nabalig", "khali"):
        active = teva.get(f"is_{tname}")
        desc = pick(teva.get("description", {}).get(tname, {}))
        flag = "★ ACTIVE" if active else "  inactive"
        print(f"{tname.capitalize():<10}{flag:<12} {desc}")
    print(f"\nActive types: {teva.get('active_types') or ['—']}")


# ─────────────────────────────────────────────────────────────────────
#  5) 9 KARMIC RIN
# ─────────────────────────────────────────────────────────────────────
def table_karmic_debts(planet_positions_lk):
    hr("5 · KARMIC RIN (9-debt engine)")
    debts = calculate_karmic_debts(planet_positions_lk)
    if not debts:
        print("No active karmic debts.")
        return
    for d in debts:
        print(f"• {pick(d['name']):<20} {pick(d['type']):<30}  "
              f"trigger: {pick(d['reason'])[:70]}")


# ─────────────────────────────────────────────────────────────────────
#  6) HORA-BASED DEBT (10th karmic debt via planetary hour)
# ─────────────────────────────────────────────────────────────────────
def table_hora_debt(planet_positions_lk):
    hr("6 · HORA-BASED DEBT (planetary-hour 10th debt)")
    birth_dt = datetime.combine(
        datetime.strptime(MEHARBAN["birth_date"], "%Y-%m-%d").date(),
        datetime.strptime(MEHARBAN["birth_time"], "%H:%M:%S").time(),
    )

    # Compute real sunrise for the birth date+location so the Hora lord
    # can actually be derived. Without this the engine correctly skips.
    sunrise_time = None
    try:
        from app.panchang_engine import _compute_sun_times
        sun_times = _compute_sun_times(
            MEHARBAN["birth_date"],
            MEHARBAN["latitude"],
            MEHARBAN["longitude"],
            MEHARBAN["tz_offset"],
        )
        sr_str = sun_times.get("sunrise")
        if sr_str and sr_str != "--:--":
            sunrise_time = datetime.strptime(sr_str, "%H:%M").time()
            print(f"Real sunrise : {sr_str} (from panchang_engine)")
    except Exception as e:
        print(f"(sunrise computation failed: {e} — hora will be skipped)")

    try:
        result = calculate_karmic_debts_with_hora(
            planet_positions_lk,
            birth_datetime=birth_dt,
            sunrise_time=sunrise_time,
        )
    except Exception as e:
        print(f"Hora calc skipped: {e}")
        return

    hora = result.get("hora_analysis") or {}
    if hora.get("_skipped"):
        print(f"(Hora skipped — reason: {hora.get('reason', 'no sunrise')})")
        return
    print(f"Day lord     : {hora.get('day_lord')}")
    print(f"Hora lord    : {hora.get('hora_lord')}")
    print(f"Weekday      : {hora.get('weekday_name')}")
    print(f"Hrs after SR : {hora.get('hours_elapsed_since_sunrise')}")
    base_debt = (hora.get("base_debt") or {})
    print(f"Base debt    : {base_debt.get('debt')}  |  {base_debt.get('debt_hi')}")
    desc = base_debt.get("description", {}) or {}
    if desc:
        print(f"  meaning    : {desc.get('en', '')[:90]}")
    conflicts = result.get("conflicts_resolved") or []
    if conflicts:
        print("Conflicts    :")
        for c in conflicts:
            print(f"   - {c.get('type')}: {c.get('trigger')}  →  {pick(c.get('reason'))[:80]}")
    infl = result.get("hora_influence") or {}
    if infl:
        print(f"Hora influence: {'new debt added' if infl.get('added_new_debt') else 'already covered'}"
              f"  ({infl.get('debt_name') or infl.get('reason','')})")


# ─────────────────────────────────────────────────────────────────────
#  7) ACTIVE vs PASSIVE RIN
# ─────────────────────────────────────────────────────────────────────
def table_active_passive_rin(planet_positions_lk):
    hr("7 · ACTIVE vs PASSIVE RIN (enrichment)")
    debts = calculate_karmic_debts(planet_positions_lk)
    enriched = enrich_debts_active_passive(debts, planet_positions_lk)
    print(f"{'Rin':<22}{'Status':<12}{'Activ. house':<14}Urgency")
    print("-" * 78)
    for d in enriched:
        urgency = pick(d.get("activation_urgency"))[:40]
        print(f"{pick(d['name']):<22}{d.get('activation_status','—'):<12}"
              f"{str(d.get('activation_house','—')):<14}{urgency}")


# ─────────────────────────────────────────────────────────────────────
#  8) MASNUI GRAH (artificial planets)
# ─────────────────────────────────────────────────────────────────────
def table_masnui(planet_positions_lk):
    hr("8 · MASNUI GRAH (artificial planets)")
    res = calculate_masnui_planets(planet_positions_lk)
    masnui_list = res.get("masnui_planets") or []
    if not masnui_list:
        print("No masnui planets formed.")
    else:
        print(f"{'House':<7}{'Formed by':<28}{'→ Masnui':<16}{'Quality':<12}")
        print("-" * 78)
        for m in masnui_list:
            formed = " + ".join(m.get("formed_by") or [])
            print(f"H{m.get('house'):<6}{formed:<28}{m.get('masnui_planet',''):<16}"
                  f"{m.get('quality','—'):<12}")
    prof = res.get("psychological_profile") or {}
    if prof:
        sub("Psychological profile")
        print(f"Dominant quality   : {pick(prof.get('dominant_quality'))}")
        print(f"Behaviour          : {pick(prof.get('behavioral_tendencies'))}")
        print(f"Relationship style : {pick(prof.get('relationship_approach'))}")


# ─────────────────────────────────────────────────────────────────────
#  9) LK ASPECTS (classical drishti)
# ─────────────────────────────────────────────────────────────────────
def table_aspects(planet_positions_lk):
    hr("9 · LK ASPECTS (scriptural drishti)")
    aspects = calculate_lk_aspects(planet_positions_lk)
    for aspecting, targets in (aspects or {}).items():
        if not targets:
            continue
        ts = ", ".join(f"{t.get('aspects_to')} (H{t.get('house')}, "
                       f"str {t.get('strength')})" for t in targets)
        print(f"  {aspecting:<10} → {ts}")


# ─────────────────────────────────────────────────────────────────────
# 10) SLEEPING STATUS + KAYAM GRAH + MUTHTHI
# ─────────────────────────────────────────────────────────────────────
def table_sleeping_kayam(planet_positions_lk):
    hr("10 · SLEEPING STATUS / KAYAM / MUTHTHI")
    sleep = calculate_sleeping_status(planet_positions_lk)
    aspects = calculate_lk_aspects(planet_positions_lk)
    kayam = calculate_kayam_grah(planet_positions_lk, aspects)
    muth = calculate_muththi(planet_positions_lk)

    sub("Sleeping / Awake")
    for p, flag in sleep.items():
        print(f"  {p:<10} : {flag}")
    sub("Kayam (stable) planets")
    print("  " + (", ".join(kayam) or "—"))
    sub("Muththi (fist / kendra grip)")
    print(f"  Kendra strength score : {muth.get('strength_score', '—')}")
    print(f"  Detail                : {muth.get('detail', '—')}")


# ─────────────────────────────────────────────────────────────────────
# 11) PROHIBITIONS + FORBIDDEN REMEDIES
# ─────────────────────────────────────────────────────────────────────
def table_prohibitions(planet_positions_lk):
    hr("11 · PROHIBITIONS & FORBIDDEN REMEDIES")
    prohib = get_prohibitions(planet_positions_lk) or []
    if prohib:
        for p in prohib:
            print(f"• {p['planet']} in H{p['house']}  forbidden: "
                  f"{pick(p.get('forbidden'))}")
            print(f"   backlash → {pick(p.get('backlash_risk'))}")
    else:
        print("No prohibitions triggered.")

    sub("Forbidden-remedy engine (cross-check)")
    for row in (get_forbidden_remedies(planet_positions_lk) or [])[:10]:
        print(f"• {row.get('planet')} H{row.get('house')}  "
              f"{pick(row.get('forbidden_action'))[:80]}")


# ─────────────────────────────────────────────────────────────────────
# 12) BUNYAAD (foundation)
# ─────────────────────────────────────────────────────────────────────
def table_bunyaad(planet_positions_lk):
    hr("12 · BUNYAAD (foundation)")
    b = calculate_bunyaad(planet_positions_lk)
    print(f"Collapsed foundations : {b.get('collapsed_planets') or '—'}")
    print(f"Strong foundations    : {b.get('strong_foundations') or '—'}")
    sub("Per-planet")
    for planet, info in (b.get("planets") or {}).items():
        print(f"  {planet:<10} pakka H{info.get('pakka_ghar')}  "
              f"bunyaad H{info.get('bunyaad_house')}  "
              f"status: {info.get('bunyaad_status')}  "
              f"enemies: {info.get('enemies_in_bunyaad') or '—'}")


# ─────────────────────────────────────────────────────────────────────
# 13) TAKKAR (collision 1-6 / 1-8 axis)
# ─────────────────────────────────────────────────────────────────────
def table_takkar(planet_positions_lk):
    hr("13 · TAKKAR (collision)")
    t = calculate_takkar(planet_positions_lk)
    print(f"Destructive: {t.get('destructive_count', 0)}  "
          f"Mild: {t.get('mild_count', 0)}  "
          f"Most attacked: {t.get('most_attacked_planet', '—')}  "
          f"Safe: {t.get('safe_planets') or '—'}")
    for c in (t.get("collisions") or []):
        print(f"  • {c.get('attacker')} → {c.get('receiver')}  "
              f"axis {c.get('axis')}  sev {c.get('severity')}")


# ─────────────────────────────────────────────────────────────────────
# 14) ENEMY PRESENCE / SIEGE
# ─────────────────────────────────────────────────────────────────────
def table_enemy_presence(planet_positions_lk):
    hr("14 · ENEMY PRESENCE / SIEGE")
    e = calculate_enemy_presence(planet_positions_lk)
    print(f"Most besieged : {e.get('most_besieged', '—')}  |  "
          f"Least besieged: {e.get('least_besieged', '—')}")
    for planet, info in (e.get("planets") or {}).items():
        print(f"  {planet:<10} siege {info.get('enemy_siege_level','—'):<9}  "
              f"enemies: {info.get('total_enemies',0)}  "
              f"in pakka: {info.get('enemies_in_pakka_ghar',0)}")


# ─────────────────────────────────────────────────────────────────────
# 15) DHOKA + ACHANAK CHOT
# ─────────────────────────────────────────────────────────────────────
def table_relationship_patterns(planet_positions_lk):
    hr("15 · RELATIONSHIP PATTERNS (Dhoka · Achanak Chot)")
    sub("Dhoka (deception)")
    for d in calculate_dhoka(planet_positions_lk) or []:
        print(f"  {d.get('dhoka_name'):<28} H{d.get('source_house')} → "
              f"H{d.get('target_house')}  severity {d.get('severity')}")
    sub("Achanak Chot (sudden strike)")
    for a in calculate_achanak_chot(planet_positions_lk) or []:
        print(f"  {a.get('strike_name'):<28} striker H{a.get('striker_house')} → "
              f"victim H{a.get('victim_house')}  crit {a.get('is_critical')}")


# ─────────────────────────────────────────────────────────────────────
# 16) BALI KA BAKRA (sacrifice)
# ─────────────────────────────────────────────────────────────────────
def table_sacrifice(planet_positions_lk):
    hr("16 · BALI KA BAKRA (sacrifice patterns)")
    # analyze_sacrifice expects List[Dict[planet, house]] + aspects mapping
    aspects = calculate_lk_aspects(planet_positions_lk) or {}
    try:
        res = analyze_sacrifice(planet_positions_lk, aspects)
    except Exception as e:
        print(f"Sacrifice calc skipped: {e}")
        return
    results = res.get("results") if isinstance(res, dict) else res
    if not results:
        print("No sacrifice patterns detected.")
        return
    for r in results:
        print(f"  {r.get('sacrificer')} sacrifices {r.get('victim')}  "
              f"severity {r.get('severity')}  rule {r.get('rule_id')}")
        print(f"    {pick(r.get('message'))[:120]}")


# ─────────────────────────────────────────────────────────────────────
# 17) TECHNICAL (Chalti Gaadi · Dhur-dhur-aage · Soya Ghar · Statuses)
# ─────────────────────────────────────────────────────────────────────
def table_technical(planet_positions_lk):
    hr("17 · TECHNICAL METRICS")
    sub("Chalti Gaadi (moving vehicle)")
    cg = calculate_chalti_gaadi(planet_positions_lk)
    print(f"  {cg}")
    sub("Dhur-dhur-aage (push/pull)")
    dd = calculate_dhur_dhur_aage(planet_positions_lk)
    print(f"  Most pushful: {dd.get('most_pushful_planet','—')}   "
          f"Most pushed: {dd.get('most_pushed_planet','—')}")
    for push in (dd.get("pushes") or [])[:6]:
        print(f"    {push.get('pusher')} → {push.get('receiver')}  "
              f"direction {push.get('direction')}")
    sub("Soya Ghar (sleeping houses)")
    try:
        soya = calculate_soya_ghar(planet_positions_lk)
        print(f"  {soya}")
    except TypeError:
        print("  (soya needs extra args — skipped)")
    sub("Planet statuses (LK-level)")
    for row in classify_all_planet_statuses(planet_positions_lk):
        print(f"  {row.get('planet'):<10}  status: {row.get('status','—')}")


# ─────────────────────────────────────────────────────────────────────
# 18) RELATIONS + RULES + DOSHAS
# ─────────────────────────────────────────────────────────────────────
def table_relations_rules_doshas(planet_positions_lk):
    hr("18 · RELATIONS · RULES · DOSHAS")
    pos_map = {p["planet"]: p["house"] for p in planet_positions_lk}
    sub("Relations — Conjunctions")
    rel = build_relations(pos_map)
    for c in (rel.get("conjunctions") or [])[:10]:
        print(f"  • {c}")
    sub("Relations — Aspects")
    for a in (rel.get("aspects") or [])[:10]:
        print(f"  • {a}")
    sub("Rules — Mirror axis")
    r = build_rules(pos_map)
    for rule in (r.get("mirror_axis") or [])[:10]:
        print(f"  • {rule}")
    sub("Rules — Cross effects")
    for rule in (r.get("cross_effects") or [])[:10]:
        print(f"  • {rule}")
    sub("Doshas")
    for d in detect_lalkitab_doshas(planet_positions_lk) or []:
        flag = "★" if d.get("detected") else " "
        print(f"  {flag} {d.get('name_en','?'):<22} severity {d.get('severity','—'):<8} "
              f"detected={d.get('detected', False)}")


# ─────────────────────────────────────────────────────────────────────
# 19) VASTU
# ─────────────────────────────────────────────────────────────────────
def table_vastu(planet_positions_lk):
    hr("19 · VASTU")
    v = get_vastu_diagnosis(planet_positions_lk) or {}
    print(f"Critical count: {v.get('critical_count', 0)}")
    for w in (v.get("planet_warnings") or [])[:10]:
        crit = "★CRITICAL" if w.get("is_critical") else ""
        print(f"  • {w.get('planet'):<10} H{w.get('house')}  "
              f"{pick(w.get('direction')):<14} {crit}")
        print(f"    warn: {pick(w.get('warning'))[:90]}")
        print(f"    fix : {pick(w.get('fix'))[:90]}")


# ─────────────────────────────────────────────────────────────────────
# 20) DASHA / SAALA GRAH / AGE ACTIVATION
# ─────────────────────────────────────────────────────────────────────
def table_timing():
    hr("20 · TIMING (Dasha · Saala Grah · Age Activation · 7-year cycle)")
    today = date.today().isoformat()
    age = get_age_activation(MEHARBAN["birth_date"], today)
    print(f"Age activation today : {age}")

    saala = get_saala_grah(age.get("current_age", 0) if isinstance(age, dict) else 0)
    print(f"Saala Grah (year-lord): {saala}")

    dasha = get_dasha_timeline(MEHARBAN["birth_date"], today)
    print(f"Current saala grah   : {dasha.get('current_saala_grah')}")
    print(f"Next saala grah      : {dasha.get('next_saala_grah')}")
    print(f"Life phase           : {dasha.get('life_phase')}")
    print(f"Years in phase       : {dasha.get('years_into_phase')} / "
          f"{dasha.get('years_remaining_in_phase')} left")
    sub("Past age-periods (last 3)")
    for p in (dasha.get("past_periods") or [])[-3:]:
        print(f"  {p}")
    sub("Upcoming age-periods (next 3)")
    for p in (dasha.get("upcoming_periods") or [])[:3]:
        print(f"  {p}")


def table_milestones_and_cycle(planet_positions_lk):
    hr("21 · AGE MILESTONES + 7-YEAR CYCLE")
    birth_year = int(MEHARBAN["birth_date"][:4])
    current_age = datetime.now().year - birth_year
    try:
        # calculate_age_milestones signature: (birth_date, planet_positions, as_of=None)
        ms = calculate_age_milestones(MEHARBAN["birth_date"], planet_positions_lk)
        if isinstance(ms, dict):
            for m in (ms.get("past") or [])[:5]:
                print(f"  past : {m}")
            for m in (ms.get("upcoming") or [])[:5]:
                print(f"  upcm : {m}")
        elif isinstance(ms, list):
            for m in ms[:8]:
                print(f"  • {m}")
    except Exception as e:
        print(f"  (milestones skipped: {e})")
    sub("7-year cycle")
    try:
        cyc = get_seven_year_cycle(current_age, planet_positions_lk)
        print(f"  {cyc}")
    except Exception as e:
        print(f"  (cycle skipped: {e})")


# ─────────────────────────────────────────────────────────────────────
# 22) PREDICTION STUDIO
# ─────────────────────────────────────────────────────────────────────
def table_prediction_studio(chart, planet_positions_lk):
    hr("22 · PREDICTION STUDIO (marriage · career · health · wealth)")
    # build_prediction_studio(planet_positions: Dict[str,int], planet_longitudes?)
    p_map = {p["planet"]: p["house"] for p in planet_positions_lk}
    p_lons = {n: info["longitude"] for n, info in chart["planets"].items()}
    try:
        ps = build_prediction_studio(p_map, p_lons)
    except Exception as e:
        print(f"Studio skipped: {e}")
        return
    rows = ps if isinstance(ps, list) else (ps.get("areas") or ps.get("predictions") or [])
    if isinstance(rows, dict):
        rows = [{"area": k, **(v if isinstance(v, dict) else {"value": v})}
                for k, v in rows.items()]
    print(f"{'Area':<22}{'Score':>6} {'Confidence':<11}{'Tone':<5}Headline")
    print("-" * 78)
    for row in rows:
        area = row.get("title_en") or row.get("area") or row.get("key") or "—"
        conf = row.get("confidence") or "—"
        score = row.get("score", "—")
        pos = row.get("is_positive")
        tone = "✓" if pos else "✗" if pos is False else " "
        head = row.get("positive_en") if pos else (row.get("caution_en") or row.get("positive_en") or "")
        print(f"{str(area)[:21]:<22}{score:>6} {conf:<11}{tone:<5}{str(head)[:60]}")


# ─────────────────────────────────────────────────────────────────────
# 23) REMEDIES (engine-generated)
# ─────────────────────────────────────────────────────────────────────
def table_remedies(chart, planet_positions_lk):
    hr("23 · REMEDIES (engine-generated per planet)")
    # get_remedies expects {planet: sign_name}
    planet_signs = {p["planet"]: p["sign"] for p in planet_positions_lk}
    try:
        rem = get_remedies(planet_signs, chart)
    except TypeError:
        rem = get_remedies(planet_signs)
    print(f"{'Planet':<10}{'LK H':<6}{'Dignity':<14}{'Strength':<10}{'Remedy (EN)':<40}")
    print("-" * 78)
    for planet, info in (rem or {}).items():
        r = info.get("remedy") or {}
        text = (r.get("en") or "—") if isinstance(r, dict) else str(r)
        print(f"{planet:<10}H{info.get('lk_house','?'):<5}"
              f"{info.get('dignity','—'):<14}{info.get('strength','—'):<10}"
              f"{text[:40]:<40}")


# ─────────────────────────────────────────────────────────────────────
# 24) PLANET-IN-HOUSE INTERPRETATIONS (Grahfal/Bhavfal per LK 1952)
# ─────────────────────────────────────────────────────────────────────
def table_grahfal(planet_positions_lk):
    hr("24 · GRAHFAL / BHAVFAL (planet-in-house per LK 1952)")
    # get_all_interpretations_for_chart expects the raw list-of-dicts
    interps = get_all_interpretations_for_chart(planet_positions_lk)
    rows = interps if isinstance(interps, list) else interps.get("interpretations", [])
    for row in rows[:9]:
        print(f"  {row.get('planet'):<10} H{row.get('house'):<3} — "
              f"{pick(row.get('effect') or row.get('effect_en'))[:100]}")
        cond = row.get("conditions") or row.get("condition")
        if cond:
            print(f"             ↳ {pick(cond)[:100]}")


# ─────────────────────────────────────────────────────────────────────
# 25) PALM ZONES (reference table)
# ─────────────────────────────────────────────────────────────────────
def table_palm_zones():
    hr("25 · PALM ZONES (Samudrik — reference only)")
    for z in get_palm_zones():
        print(f"  {z['zone_id']:<16} {z['planet']:<10}  "
              f"H{z['lk_house']:<3} ({z['svg_cx']}, {z['svg_cy']})")


# ═══════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════
def main():
    chart = calculate_planet_positions(**{
        k: MEHARBAN[k] for k in
        ("birth_date", "birth_time", "latitude", "longitude", "tz_offset")
    })

    # Build the planet list that every LK engine accepts:
    # [{"planet": "Sun", "house": <LK house from sign>}, ...]
    planet_positions_lk = [
        {"planet": name, "house": _derive_lk_house(info), "sign": info["sign"]}
        for name, info in chart["planets"].items()
    ]

    table_core_chart(chart, planet_positions_lk)
    table_house_map(planet_positions_lk)
    table_planet_status(chart)
    table_teva(planet_positions_lk)
    table_karmic_debts(planet_positions_lk)
    table_hora_debt(planet_positions_lk)
    table_active_passive_rin(planet_positions_lk)
    table_masnui(planet_positions_lk)
    table_aspects(planet_positions_lk)
    table_sleeping_kayam(planet_positions_lk)
    table_prohibitions(planet_positions_lk)
    table_bunyaad(planet_positions_lk)
    table_takkar(planet_positions_lk)
    table_enemy_presence(planet_positions_lk)
    table_relationship_patterns(planet_positions_lk)
    table_sacrifice(planet_positions_lk)
    table_technical(planet_positions_lk)
    table_relations_rules_doshas(planet_positions_lk)
    table_vastu(planet_positions_lk)
    table_timing()
    table_milestones_and_cycle(planet_positions_lk)
    table_prediction_studio(chart, planet_positions_lk)
    table_remedies(chart, planet_positions_lk)
    table_grahfal(planet_positions_lk)
    table_palm_zones()

    hr("DONE", char="═")


if __name__ == "__main__":
    main()
