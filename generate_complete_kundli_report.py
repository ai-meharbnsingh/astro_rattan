#!/usr/bin/env python3
"""
Kundli Complete Report Generator — CLI Orchestrator
=====================================================
Generates a full production-grade Kundli PDF report plus audit/debug files.

Usage:
    python generate_complete_kundli_report.py \
        --name "Rahul Sharma" \
        --gender Male \
        --date 1990-06-15 \
        --time "14:30" \
        --place "Delhi, India" \
        --lat 28.6139 \
        --lon 77.2090 \
        --tz 5.5 \
        --ayanamsa lahiri \
        --depth detailed

Outputs:
    kundli_full_report.pdf
    kundli_full_report_debug.json
    kundli_section_coverage.json
    kundli_engine_audit.md
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# Ensure app modules are importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.astro_engine import calculate_planet_positions
from app.reports.kundli_report import build_full_report, _dict_has_values, _has_meaningful


def safe_call(func, *args, **kwargs) -> Tuple[Any, str]:
    """Call a function safely, returning (result, error_or_empty)."""
    try:
        return func(*args, **kwargs), ""
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:120]}"


def run_all_engines(birth_data: dict) -> Tuple[dict, dict, dict]:
    """
    Run all available Kundli engines and return:
      - assembled_data: dict for PDF builder
      - debug: dict with all computed outputs
      - audit: dict with engine status info
    """
    bd = birth_data
    only_first_page = bool(bd.get("only_first_page"))
    person_name = bd["person_name"]
    birth_date = bd["birth_date"]
    birth_time = bd["birth_time"]
    latitude = bd["latitude"]
    longitude = bd["longitude"]
    tz_offset = bd["tz_offset"]
    gender = bd["gender"]
    ayanamsa = bd.get("ayanamsa", "lahiri")

    debug: Dict[str, Any] = {"birth_data": bd, "engines": {}}
    audit: Dict[str, Any] = {"reused": [], "missing": [], "stubbed": [], "disconnected": []}
    assembled: Dict[str, Any] = {"birth_info": bd, "chart_data": {}, "language": bd.get("language", "en"), "report_depth": bd.get("report_depth", "detailed")}

    # ── CORE: Planetary Positions ──
    chart_data, err = safe_call(
        calculate_planet_positions,
        birth_date, birth_time, latitude, longitude, tz_offset, ayanamsa
    )
    if chart_data:
        assembled["chart_data"] = chart_data
        debug["engines"]["astro_engine"] = chart_data
        audit["reused"].append("astro_engine (core planetary positions)")
    else:
        audit["missing"].append(f"astro_engine: {err}")
        print(f"FATAL: Core chart calculation failed: {err}")
        sys.exit(1)

    planets = chart_data.get("planets", {})
    ascendant = chart_data.get("ascendant", {})
    asc_sign = ascendant.get("sign", "Aries")
    moon_sign = planets.get("Moon", {}).get("sign", "Aries") if isinstance(planets.get("Moon"), dict) else "Aries"

    # Helper to extract planet houses/signs for engines that need them
    planet_houses = {p: info.get("house", 1) for p, info in planets.items() if isinstance(info, dict)}
    planet_signs = {p: info.get("sign", "Aries") for p, info in planets.items() if isinstance(info, dict)}

    # ── DASHA (Vimshottari) ──
    try:
        from app.dasha_engine import calculate_extended_dasha, get_current_dasha_phala
        moon_info = planets.get("Moon", {}) if isinstance(planets, dict) else {}
        moon_nakshatra = moon_info.get("nakshatra", "Ashwini")
        moon_longitude = moon_info.get("longitude", None)

        ext_dasha, err = safe_call(calculate_extended_dasha, moon_nakshatra, birth_date, moon_longitude=moon_longitude)
        if ext_dasha:
            assembled["dasha"] = ext_dasha
            debug["engines"]["dasha_engine"] = ext_dasha
            audit["reused"].append("dasha_engine (Vimshottari extended)")
        else:
            audit["missing"].append(f"dasha_engine: {err}")

        today = datetime.now().strftime("%Y-%m-%d")
        phala, err = safe_call(
            get_current_dasha_phala,
            chart_data,
            birth_date,
            today,
            latitude,
            longitude,
            tz_offset,
        )
        if phala:
            assembled["dasha_phala"] = phala
            debug["engines"]["dasha_phala"] = phala
            audit["reused"].append("dasha_engine (dasha phala)")
    except ImportError as e:
        audit["missing"].append(f"dasha_engine: {e}")

    # ── OTHER DASHAS (Ashtottari / Tara / Moola) ──
    try:
        moon_info = planets.get("Moon", {}) if isinstance(planets, dict) else {}
        moon_nakshatra = moon_info.get("nakshatra", "Ashwini")
        moon_longitude = moon_info.get("longitude", None)
        from app.ashtottari_dasha_engine import calculate_ashtottari_dasha
        ad, err = safe_call(calculate_ashtottari_dasha, moon_nakshatra, birth_date, moon_longitude=moon_longitude)
        if ad:
            assembled["ashtottari_dasha"] = ad
            debug["engines"]["ashtottari_dasha_engine"] = ad
            audit["reused"].append("ashtottari_dasha_engine")
    except Exception as e:
        audit["missing"].append(f"ashtottari_dasha_engine: {e}")
    try:
        moon_info = planets.get("Moon", {}) if isinstance(planets, dict) else {}
        moon_nakshatra = moon_info.get("nakshatra", "Ashwini")
        moon_longitude = moon_info.get("longitude", None)
        from app.tara_dasha_engine import calculate_tara_dasha
        td, err = safe_call(calculate_tara_dasha, moon_nakshatra, birth_date, moon_longitude=moon_longitude)
        if td:
            assembled["tara_dasha"] = td
            debug["engines"]["tara_dasha_engine"] = td
            audit["reused"].append("tara_dasha_engine")
    except Exception as e:
        audit["missing"].append(f"tara_dasha_engine: {e}")
    try:
        from app.moola_dasha_engine import calculate_moola_dasha
        planet_signs_map = {p: info.get("sign", "") for p, info in planets.items() if isinstance(info, dict)}
        _SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
        _idx = _SIGNS.index(asc_sign) if asc_sign in _SIGNS else 0
        seventh_sign = _SIGNS[(_idx + 6) % 12]
        md, err = safe_call(calculate_moola_dasha, asc_sign, seventh_sign, planet_signs_map, birth_date)
        if md:
            assembled["moola_dasha"] = md
            debug["engines"]["moola_dasha_engine"] = md
            audit["reused"].append("moola_dasha_engine")
    except Exception as e:
        audit["missing"].append(f"moola_dasha_engine: {e}")

    # ── AVAKHADA ──
    try:
        from app.avakhada_engine import calculate_avakhada
        avk, err = safe_call(calculate_avakhada, chart_data, birth_date=birth_date)
        if avk:
            assembled["avakhada"] = avk
            debug["engines"]["avakhada_engine"] = avk
            audit["reused"].append("avakhada_engine")
        else:
            audit["missing"].append(f"avakhada_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"avakhada_engine: {e}")

    # ── PANCHANG ──
    try:
        from app.panchang_engine import calculate_panchang
        pc, err = safe_call(calculate_panchang, birth_date, latitude, longitude, tz_offset)
        if pc:
            assembled["panchang"] = pc
            debug["engines"]["panchang_engine"] = pc
            audit["reused"].append("panchang_engine")
        else:
            audit["missing"].append(f"panchang_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"panchang_engine: {e}")
    except Exception as e:
        audit["missing"].append(f"panchang_engine: {e}")

    if only_first_page:
        # First-page preview only needs core chart + panchang/avakhada.
        return assembled, debug, audit

    # ── YOGAS & DOSHAS ──
    try:
        from app.dosha_engine import analyze_yogas_and_doshas
        yd, err = safe_call(analyze_yogas_and_doshas, planets, asc_sign)
        if yd:
            assembled["yogas_doshas"] = yd
            debug["engines"]["dosha_engine"] = yd
            audit["reused"].append("dosha_engine (yogas & doshas)")
        else:
            audit["missing"].append(f"dosha_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"dosha_engine: {e}")

    # ── SHADBALA ──
    try:
        from app.shadbala_engine import calculate_shadbala, calculate_bhav_bala
        sb_params = _prepare_shadbala_params(planets, bd)
        sb, err = safe_call(calculate_shadbala, **sb_params)
        if sb:
            assembled["shadbala"] = sb
            debug["engines"]["shadbala_engine"] = sb
            audit["reused"].append("shadbala_engine")
        else:
            audit["missing"].append(f"shadbala_engine: {err}")

        # Bhava bala requires house_signs + planets_result
        house_signs = {}
        houses_raw = chart_data.get("houses", [])
        if isinstance(houses_raw, list):
            for h in houses_raw:
                if isinstance(h, dict):
                    num = h.get("number") or h.get("house")
                    sign = h.get("sign", "Aries")
                    if num:
                        house_signs[int(num)] = sign
        if sb and isinstance(sb, dict) and isinstance(sb.get("planets"), dict):
            bb, err = safe_call(
                calculate_bhav_bala,
                house_signs=house_signs,
                planet_houses=sb_params.get("planet_houses", {}),
                planets_result=sb.get("planets", {}),
            )
            if bb:
                sb["bhav_bala"] = bb
                debug["engines"]["bhav_bala"] = bb
    except ImportError as e:
        audit["missing"].append(f"shadbala_engine: {e}")

    # ── ASHTAKAVARGA ──
    try:
        from app.ashtakvarga_engine import calculate_ashtakvarga
        planet_signs_map = {p: info.get("sign", "") for p, info in planets.items() if isinstance(info, dict)}
        av, err = safe_call(calculate_ashtakvarga, planet_signs_map)
        if av:
            assembled["ashtakvarga"] = av
            debug["engines"]["ashtakvarga_engine"] = av
            audit["reused"].append("ashtakvarga_engine")
        else:
            audit["missing"].append(f"ashtakvarga_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"ashtakvarga_engine: {e}")

    # ── ASPECTS ──
    try:
        from app.aspects_engine import calculate_aspects
        asp, err = safe_call(calculate_aspects, planets, chart_data.get("houses"))
        if asp:
            assembled["aspects"] = asp
            debug["engines"]["aspects_engine"] = asp
            audit["reused"].append("aspects_engine")
        else:
            audit["missing"].append(f"aspects_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"aspects_engine: {e}")

    # ── CONJUNCTIONS ──
    try:
        from app.conjunction_engine import detect_conjunctions
        conj, err = safe_call(detect_conjunctions, chart_data)
        if conj is not None:
            assembled["conjunctions"] = {"conjunctions": conj, "count": len(conj) if isinstance(conj, list) else None}
            debug["engines"]["conjunction_engine"] = assembled["conjunctions"]
            audit["reused"].append("conjunction_engine")
        else:
            audit["missing"].append(f"conjunction_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"conjunction_engine: {e}")

    # ── DIVISIONAL / SODASHVARGA ──
    try:
        from app.divisional_charts import calculate_divisional_chart_detailed
        from app.sodashvarga_engine import calculate_sodashvarga
        div, err = safe_call(calculate_divisional_chart_detailed, planets)
        if div:
            debug["engines"]["divisional_charts"] = div
        longs = {pn: pi.get("longitude", 0.0) for pn, pi in planets.items() if isinstance(pi, dict) and "longitude" in pi}
        sv, err = safe_call(calculate_sodashvarga, longs)
        if sv:
            assembled["sodashvarga"] = sv
            debug["engines"]["sodashvarga_engine"] = sv
            audit["reused"].append("sodashvarga_engine")
        else:
            audit["missing"].append(f"sodashvarga_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"divisional/sodashvarga: {e}")

    # ── TRANSITS (includes Vedha/Latta enrichment) ──
    try:
        from app.transit_engine import calculate_transits
        today = datetime.now().strftime("%Y-%m-%d")
        tr, err = safe_call(calculate_transits, chart_data, latitude, longitude, today)
        if tr:
            assembled["transit"] = tr
            debug["engines"]["transit_engine"] = tr
            audit["reused"].append("transit_engine")
            # Transit interpretations (planet-house fragments)
            try:
                from app.transit_interpretations import TRANSIT_FRAGMENTS
                _AREAS = ["general", "love", "career", "finance", "health"]
                interpretations = []
                for t in tr.get("transits", []) if isinstance(tr, dict) else []:
                    if not isinstance(t, dict):
                        continue
                    planet = t.get("planet", "")
                    house = t.get("natal_house_from_moon") or t.get("house_from_moon") or t.get("house")
                    if not planet or not house:
                        continue
                    if planet not in TRANSIT_FRAGMENTS:
                        continue
                    house_int = int(house)
                    planet_frags = TRANSIT_FRAGMENTS.get(planet, {})
                    if house_int not in planet_frags:
                        continue
                    house_frags = planet_frags[house_int]
                    interpretations.append({
                        "planet": planet,
                        "house": house_int,
                        "interpretation": {a: house_frags.get(a, {}) for a in _AREAS},
                    })
                assembled["transit_interpretations"] = {"interpretations": interpretations}
                debug["engines"]["transit_interpretations"] = assembled["transit_interpretations"]
                audit["reused"].append("transit_interpretations (TRANSIT_FRAGMENTS)")
            except Exception as e:
                audit["missing"].append(f"transit_interpretations: {e}")

            # Transit lucky metadata (deterministic)
            try:
                from app.transit_lucky import get_all_lucky_metadata
                moon_info = (chart_data.get("planets", {}) or {}).get("Moon", {}) if isinstance(chart_data, dict) else {}
                sign = str(moon_info.get("sign", "Aries")).lower()
                moon_nakshatra_index = moon_info.get("nakshatra_index", 0) or 0
                if not moon_nakshatra_index:
                    moon_lon = moon_info.get("longitude", 0.0) or 0.0
                    moon_nakshatra_index = int(moon_lon / (360.0 / 27)) % 27
                moon_pada = moon_info.get("pada", 1) or 1
                planet_houses = {}
                planet_dignities = {}
                transit_dignities = {}
                for t in tr.get("transits", []) if isinstance(tr, dict) else []:
                    if not isinstance(t, dict):
                        continue
                    pnm = t.get("planet", "")
                    if not pnm:
                        continue
                    planet_houses[pnm] = t.get("natal_house_from_moon") or t.get("house_from_moon") or t.get("house") or 1
                    planet_dignities[pnm] = t.get("dignity", "") or t.get("effect", "")
                    transit_dignities[pnm] = t.get("current_sign", "") or t.get("sign", "")
                overall_score = max(1, min(10, int((tr.get("daily_score", 50) or 50) / 10)))
                assembled["transit_lucky"] = get_all_lucky_metadata(
                    sign=sign,
                    moon_nakshatra_index=moon_nakshatra_index,
                    moon_pada=moon_pada,
                    date_str=tr.get("transit_date", today),
                    overall_score=overall_score,
                    planet_houses=planet_houses,
                    planet_dignities=planet_dignities,
                    transit_dignities=transit_dignities,
                )
                debug["engines"]["transit_lucky"] = assembled["transit_lucky"]
                audit["reused"].append("transit_lucky")
            except Exception as e:
                audit["missing"].append(f"transit_lucky: {e}")
    except ImportError as e:
        audit["missing"].append(f"transit_engine: {e}")

    # ── SADE SATI ──
    try:
        from app.dosha_engine import check_sade_sati
        from app.lifelong_sade_sati import calculate_lifelong_sade_sati
        ss, err = safe_call(check_sade_sati, moon_sign, planet_signs.get("Saturn", "Aries"))
        if ss:
            debug["engines"]["sade_sati_check"] = ss
        # lifelong_sade_sati expects birth datetime + Moon sign index
        try:
            bt = str(birth_time)
            if len(bt.split(":")) == 2:
                bt = bt + ":00"
            birth_dt = datetime.strptime(f"{birth_date} {bt}", "%Y-%m-%d %H:%M:%S")
        except Exception:
            birth_dt = datetime.strptime(str(birth_date), "%Y-%m-%d")
        sign_order = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
        moon_idx = sign_order.index(moon_sign) if moon_sign in sign_order else 0
        lss, err = safe_call(calculate_lifelong_sade_sati, birth_dt, moon_idx, moon_sign)
        if lss:
            payload = lss if isinstance(lss, dict) else {"results": lss}
            if ss and isinstance(ss, dict):
                payload.setdefault("current_check", ss)
            assembled["sade_sati"] = payload
            debug["engines"]["lifelong_sade_sati"] = payload
            audit["reused"].append("lifelong_sade_sati")
        else:
            audit["missing"].append(f"lifelong_sade_sati: {err}")
    except ImportError as e:
        audit["missing"].append(f"sade_sati engines: {e}")

    # ── VARSHPHAL ──
    try:
        from app.varshphal_engine import calculate_varshphal
        year = datetime.now().year
        vp, err = safe_call(calculate_varshphal, chart_data, year, birth_date, latitude, longitude, tz_offset)
        if vp:
            assembled["varshphal"] = vp
            debug["engines"]["varshphal_engine"] = vp
            audit["reused"].append("varshphal_engine")
        else:
            audit["missing"].append(f"varshphal_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"varshphal_engine: {e}")

    # ── YOGINI DASHA ──
    try:
        from app.yogini_dasha_engine import calculate_yogini_dasha
        moon_info = planets.get("Moon", {}) if isinstance(planets, dict) else {}
        moon_nakshatra = moon_info.get("nakshatra", "Ashwini")
        moon_longitude = moon_info.get("longitude", None)
        yd, err = safe_call(calculate_yogini_dasha, moon_nakshatra, birth_date, moon_longitude or 0.0)
        if yd:
            assembled["yogini_dasha"] = yd
            debug["engines"]["yogini_dasha_engine"] = yd
            audit["reused"].append("yogini_dasha_engine")
        else:
            audit["missing"].append(f"yogini_dasha_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"yogini_dasha_engine: {e}")

    # ── KALACHAKRA DASHA ──
    try:
        from app.kalachakra_engine import calculate_kalachakra_dasha
        moon_info = planets.get("Moon", {}) if isinstance(planets, dict) else {}
        moon_longitude = moon_info.get("longitude", None)
        kd, err = safe_call(calculate_kalachakra_dasha, float(moon_longitude or 0.0), birth_date, birth_time)
        if kd:
            assembled["kalachakra"] = kd
            debug["engines"]["kalachakra_engine"] = kd
            audit["reused"].append("kalachakra_engine")
        else:
            audit["missing"].append(f"kalachakra_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"kalachakra_engine: {e}")

    # ── KP ──
    try:
        from app.kp_engine import calculate_kp_cuspal
        kp_chart = calculate_planet_positions(
            birth_date=birth_date,
            birth_time=birth_time,
            latitude=latitude,
            longitude=longitude,
            tz_offset=tz_offset,
            ayanamsa="kp",
        )
        kp_longs = {pn: pi.get("longitude", 0.0) for pn, pi in (kp_chart.get("planets", {}) or {}).items() if isinstance(pi, dict)}
        kp_cusps = kp_chart.get("placidus_cusps", kp_chart.get("house_cusps", []))
        if not kp_cusps or len(kp_cusps) != 12:
            asc_lon = kp_chart.get("ascendant", {}).get("longitude", 0.0)
            kp_cusps = [(asc_lon + i * 30.0) % 360.0 for i in range(12)]
        kp, err = safe_call(calculate_kp_cuspal, kp_longs, kp_cusps, kp_chart, birth_date)
        if kp:
            assembled["kp"] = kp
            debug["engines"]["kp_engine"] = kp
            audit["reused"].append("kp_engine")
        else:
            audit["missing"].append(f"kp_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"kp_engine: {e}")

    # ── JAIMINI ──
    try:
        from app.jaimini_engine import calculate_jaimini
        jm, err = safe_call(calculate_jaimini, planets, ascendant)
        if jm:
            assembled["jaimini"] = jm
            debug["engines"]["jaimini_engine"] = jm
            audit["reused"].append("jaimini_engine")
        else:
            audit["missing"].append(f"jaimini_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"jaimini_engine: {e}")

    # ── NADI ──
    try:
        from app.nadi_engine import calculate_nadi_insights
        nd, err = safe_call(calculate_nadi_insights, chart_data)
        if nd:
            assembled["nadi"] = {"results": nd}
            debug["engines"]["nadi_engine"] = {"results": nd}
            audit["reused"].append("nadi_engine")
        else:
            audit["missing"].append(f"nadi_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"nadi_engine: {e}")

    # ── ROGA ──
    try:
        from app.roga_engine import analyze_diseases
        rg, err = safe_call(analyze_diseases, chart_data)
        if rg:
            assembled["roga"] = rg
            debug["engines"]["roga_engine"] = rg
            audit["reused"].append("roga_engine")
        else:
            audit["missing"].append(f"roga_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"roga_engine: {e}")

    # ── VRITTI (Career) ──
    try:
        from app.vritti_engine import analyze_vritti
        vt, err = safe_call(analyze_vritti, chart_data)
        if vt:
            assembled["vritti"] = vt
            debug["engines"]["vritti_engine"] = vt
            audit["reused"].append("vritti_engine")
        else:
            audit["missing"].append(f"vritti_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"vritti_engine: {e}")

    # ── APATYA (Progeny) ──
    try:
        from app.apatya_engine import analyze_apatya
        ap, err = safe_call(analyze_apatya, chart_data)
        if ap:
            assembled["apatya"] = ap
            debug["engines"]["apatya_engine"] = ap
            audit["reused"].append("apatya_engine")
        else:
            audit["missing"].append(f"apatya_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"apatya_engine: {e}")

    # ── UPAGRAHAS ──
    try:
        from app.upagraha_engine import calculate_upagrahas
        ug, err = safe_call(calculate_upagrahas, birth_date, birth_time, latitude, longitude, tz_offset)
        if ug:
            assembled["upagrahas"] = ug
            debug["engines"]["upagraha_engine"] = ug
            audit["reused"].append("upagraha_engine")
        else:
            audit["missing"].append(f"upagraha_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"upagraha_engine: {e}")

    # ── PANCHADHA MAITRI ──
    try:
        from app.panchadha_maitri_engine import calculate_panchadha_maitri
        pm, err = safe_call(calculate_panchadha_maitri, planet_signs)
        if pm:
            assembled["panchadha_maitri"] = pm
            debug["engines"]["panchadha_maitri_engine"] = pm
            audit["reused"].append("panchadha_maitri_engine")
        else:
            audit["missing"].append(f"panchadha_maitri_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"panchadha_maitri_engine: {e}")

    # ── GRAHA SAMBANDHA ──
    try:
        from app.graha_sambandha_engine import calculate_graha_sambandha
        gs, err = safe_call(calculate_graha_sambandha, planets)
        if gs:
            assembled["graha_sambandha"] = gs
            debug["engines"]["graha_sambandha_engine"] = gs
            audit["reused"].append("graha_sambandha_engine")
        else:
            audit["missing"].append(f"graha_sambandha_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"graha_sambandha_engine: {e}")

    # ── SARVATOBHADRA ──
    try:
        from app.sarvatobhadra_chakra_engine import calculate_sarvatobhadra
        sb, err = safe_call(calculate_sarvatobhadra, birth_date, birth_time, latitude, longitude, tz_offset)
        if sb:
            assembled["sarvatobhadra"] = sb
            debug["engines"]["sarvatobhadra_chakra_engine"] = sb
            audit["reused"].append("sarvatobhadra_chakra_engine")
        else:
            audit["missing"].append(f"sarvatobhadra_chakra_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"sarvatobhadra_chakra_engine: {e}")

    # ── LONGEVITY ──
    try:
        from app.ayurdaya_engine import calculate_lifespan
        ay, err = safe_call(calculate_lifespan, chart_data)
        if ay:
            assembled["longevity"] = ay
            debug["engines"]["ayurdaya_engine"] = ay
            audit["reused"].append("ayurdaya_engine")
        else:
            audit["missing"].append(f"ayurdaya_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"ayurdaya_engine: {e}")

    # ── BIRTH RECTIFICATION ──
    try:
        from app.birth_rectification_engine import calculate_rectification
        br, err = safe_call(calculate_rectification, birth_date, birth_time, latitude, longitude, tz_offset)
        if br:
            assembled["birth_rectification"] = br
            debug["engines"]["birth_rectification_engine"] = br
            audit["reused"].append("birth_rectification_engine")
        else:
            audit["missing"].append(f"birth_rectification_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"birth_rectification_engine: {e}")

    # ── LAL KITAB ──
    try:
        from app.lalkitab_engine import get_remedies
        planet_signs_map = {}
        for pn, pi in planets.items():
            if isinstance(pi, dict) and pi.get("sign"):
                planet_signs_map[pn] = pi.get("sign")
        lk, err = safe_call(get_remedies, planet_signs_map, chart_data)
        if lk:
            assembled["lal_kitab"] = {"results": lk}
            debug["engines"]["lalkitab_engine"] = {"results": lk}
            audit["reused"].append("lalkitab_engine")
        else:
            audit["missing"].append(f"lalkitab_engine: {err}")
    except ImportError as e:
        audit["missing"].append(f"lalkitab_engine: {e}")

    # ── REMEDIES (Narad Puran reference layer) ──
    try:
        from app.remedy_engine import generate_astrological_remedies
        chart_for_remedies = dict(chart_data) if isinstance(chart_data, dict) else {}
        chart_for_remedies.setdefault("birth_date", birth_date)
        chart_for_remedies.setdefault("birth_time", birth_time)
        rem, err = safe_call(generate_astrological_remedies, chart_for_remedies, datetime.now().year)
        if rem:
            assembled["remedies"] = rem
            debug["engines"]["remedy_engine"] = rem
            audit["reused"].append("remedy_engine")
    except ImportError as e:
        audit["missing"].append(f"remedy_engine: {e}")

    return assembled, debug, audit


def _prepare_shadbala_params(planets: dict, row: dict) -> dict:
    """Match the helper in `app/routes/kundli.py` (calculate_shadbala signature)."""
    planet_signs = {}
    planet_houses = {}
    planet_longitudes = {}
    planet_speeds = {}
    retrograde_planets = set()
    for pn, pi in planets.items():
        if not isinstance(pi, dict):
            continue
        planet_signs[pn] = pi.get("sign", "Aries")
        planet_houses[pn] = pi.get("house", 1)
        if "longitude" in pi:
            planet_longitudes[pn] = pi["longitude"]
        if "speed" in pi:
            planet_speeds[pn] = pi["speed"]
        if pi.get("retrograde") or "Retrograde" in pi.get("status", ""):
            retrograde_planets.add(pn)

    birth_time = row.get("birth_time", "12:00:00")
    try:
        parts = str(birth_time).split(":")
        birth_hour = int(parts[0]) + int(parts[1]) / 60.0
    except (ValueError, IndexError):
        birth_hour = 12.0

    sun_lon = planet_longitudes.get("Sun", 0.0)
    moon_lon = planet_longitudes.get("Moon", 0.0)

    try:
        bd = datetime.strptime(str(row.get("birth_date", "2000-01-01")), "%Y-%m-%d")
        weekday = bd.weekday()
        birth_year = bd.year
        birth_month = bd.month
    except (ValueError, TypeError):
        weekday, birth_year, birth_month = 0, 2000, 1

    return {
        "planet_signs": planet_signs,
        "planet_houses": planet_houses,
        "is_daytime": 6.0 <= birth_hour < 18.0,
        "retrograde_planets": retrograde_planets,
        "planet_longitudes": planet_longitudes,
        "planet_speeds": planet_speeds if planet_speeds else None,
        "birth_hour": birth_hour,
        "moon_sun_elongation": (moon_lon - sun_lon) % 360.0,
        "weekday": weekday,
        "birth_year": birth_year,
        "birth_month": birth_month,
    }


def build_section_coverage(assembled: dict, audit: dict, birth_data: dict) -> dict:
    """Build kundli_section_coverage.json content."""
    coverage = {
        "report_metadata": {
            "generated_at": datetime.now().isoformat(),
            "native_name": birth_data["person_name"],
            "birth_date": birth_data["birth_date"],
            "report_depth": birth_data.get("report_depth", "detailed"),
        },
        "sections": [],
    }

    def has(key: str) -> bool:
        return key in assembled and _has_meaningful(assembled.get(key))

    transit_list = []
    if isinstance(assembled.get("transit"), dict):
        raw = assembled["transit"].get("transits", [])
        if isinstance(raw, list):
            transit_list = [t for t in raw if isinstance(t, dict)]
    has_vedha = any(("vedha_active" in t) or ("effect_final" in t) for t in transit_list)

    # Section list is aligned with the PDF order in `app/reports/kundli_report.py:ReportAssembler.assemble()`.
    # For each section: (name, backend_engine_found, included_in_payload)
    section_map = [
        ("Cover Page", True, True),
        ("Table of Contents", True, True),
        ("Executive Summary", True, True),
        ("Birth Particulars & Panchang", True, True),
        ("Panchang", "panchang_engine" in audit.get("reused", []), has("panchang")),
        ("Avakhada Chakra", "avakhada_engine" in audit.get("reused", []), has("avakhada")),
        ("Core Natal Charts (D1)", True, has("chart_data")),
        ("Core Charts (Moon & Navamsha)", True, has("chart_data")),
        ("Planetary Positions", True, has("chart_data")),
        ("Bhava Analysis", True, has("chart_data")),
        ("Aspects & Conjunctions", ("aspects_engine" in audit.get("reused", [])) or ("conjunction_engine" in audit.get("reused", [])), has("aspects") or has("conjunctions")),
        ("Yogas & Doshas", "dosha_engine" in audit.get("reused", []), has("yogas_doshas")),
        ("Divisional Charts", "sodashvarga_engine" in audit.get("reused", []), has("sodashvarga")),
        ("Shodashvarga Summary", True, has("sodashvarga")),
        ("Shadbala & Bhava Bala", "shadbala_engine" in audit.get("reused", []), has("shadbala")),
        ("Planetary Friendship (Maitri)", ("panchadha_maitri_engine" in audit.get("reused", [])) or ("graha_sambandha_engine" in audit.get("reused", [])), has("panchadha_maitri") or has("graha_sambandha") or has("chart_data")),
        ("Planetary Avasthas", True, has("chart_data")),
        ("Ashtakavarga", "ashtakvarga_engine" in audit.get("reused", []), has("ashtakvarga")),
        ("Dasha Systems", "dasha_engine" in audit.get("reused", []), has("dasha") or has("yogini_dasha") or has("kalachakra") or has("ashtottari_dasha") or has("moola_dasha") or has("tara_dasha")),
        ("Dasha Effects", "dasha_engine (dasha phala)" in audit.get("reused", []), has("dasha_phala")),
        ("Transits & Gochar", "transit_engine" in audit.get("reused", []), has("transit")),
        ("Gochara Vedha", has_vedha, has("transit") and has_vedha),
        ("Transit Interpretations", True, has("transit_interpretations")),
        ("Transit Lucky", True, has("transit_lucky")),
        ("Varshphal (Annual Chart)", "varshphal_engine" in audit.get("reused", []), has("varshphal")),
        ("KP System", "kp_engine" in audit.get("reused", []), has("kp")),
        ("Jaimini Astrology", "jaimini_engine" in audit.get("reused", []), has("jaimini")),
        ("Nadi Analysis", "nadi_engine" in audit.get("reused", []), has("nadi")),
        ("Disease Analysis (Roga)", "roga_engine" in audit.get("reused", []), has("roga")),
        ("Career (Vritti)", "vritti_engine" in audit.get("reused", []), has("vritti")),
        ("Progeny (Apatya)", "apatya_engine" in audit.get("reused", []), has("apatya")),
        ("Longevity Indicators", "ayurdaya_engine" in audit.get("reused", []), has("longevity")),
        ("Lal Kitab Summary", "lalkitab_engine" in audit.get("reused", []), has("lal_kitab")),
        ("Life Area Interpretations", True, True),
        ("Remedies & Upayas", "remedy_engine" in audit.get("reused", []), has("remedies")),
        ("Lucky Indicators & Practical Guidance", True, True),
        ("Missing / Pending Sections Audit", True, True),
        ("About This Report", True, True),
    ]

    for section_name, backend, included in section_map:
        status = "GENERATED" if included else ("PARTIALLY GENERATED" if backend else "NOT IMPLEMENTED")
        coverage["sections"].append({
            "section_name": section_name,
            "backend_engine_found": bool(backend),
            "included_in_payload": bool(included),
            "included_in_pdf": bool(included),
            "status": status,
            "notes": "Engine computed successfully" if backend else "Engine missing or failed",
        })

    return coverage


def build_engine_audit_md(audit: dict, coverage: dict) -> str:
    lines = []
    lines.append("# Kundli Engine Audit Report")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("## Engines Reused")
    for e in audit.get("reused", []):
        lines.append(f"- ✅ {e}")
    lines.append("")
    lines.append("## Engines Missing / Failed")
    for e in audit.get("missing", []):
        lines.append(f"- ❌ {e}")
    lines.append("")
    lines.append("## Section Coverage Summary")
    generated = [s for s in coverage["sections"] if s["status"] == "GENERATED"]
    partial = [s for s in coverage["sections"] if s["status"] == "PARTIALLY GENERATED"]
    missing = [s for s in coverage["sections"] if s["status"] == "NOT IMPLEMENTED"]
    lines.append(f"- **Generated:** {len(generated)}")
    lines.append(f"- **Partial:** {len(partial)}")
    lines.append(f"- **Missing:** {len(missing)}")
    lines.append("")
    lines.append("## Front-end Tabs vs Backend Engines")
    for s in coverage["sections"]:
        status_icon = "✅" if s["included_in_pdf"] else "⚠️" if s["backend_engine_found"] else "❌"
        lines.append(f"{status_icon} **{s['section_name']}** — {s['status']} | {s['notes']}")
    lines.append("")
    lines.append("## What is Still Disconnected")
    lines.append("The following report sections exist but their backend engines were not successfully invoked or not included:")
    for s in coverage["sections"]:
        if not s["backend_engine_found"] or not s.get("included_in_payload", False):
            if not s.get("included_in_payload", False) and s["backend_engine_found"]:
                lines.append(f"- {s['section_name']}: engine exists but payload missing")
            elif not s["backend_engine_found"]:
                lines.append(f"- {s['section_name']}: {s['notes']}")
    lines.append("")
    lines.append("## Action Required")
    lines.append("1. Verify all engine modules are importable from the project root.")
    lines.append("2. Ensure `swisseph` (pyswisseph) is installed for accurate calculations.")
    lines.append("3. Add any missing engine wrappers to the orchestrator in `generate_complete_kundli_report.py`.")
    lines.append("4. Run `pytest` to confirm individual engines produce valid output.")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Complete Kundli Report")
    parser.add_argument("--name", default="Sample Native", help="Full name")
    parser.add_argument("--gender", default="Male", choices=["Male", "Female", "Other"])
    parser.add_argument("--date", default="1990-06-15", help="YYYY-MM-DD")
    parser.add_argument("--time", default="14:30", help="HH:MM")
    parser.add_argument("--place", default="Delhi, India", help="Place of birth")
    parser.add_argument("--lat", type=float, default=28.6139, help="Latitude")
    parser.add_argument("--lon", type=float, default=77.2090, help="Longitude")
    parser.add_argument("--tz", type=float, default=5.5, help="Timezone offset from UTC")
    parser.add_argument("--ayanamsa", default="lahiri", help="Ayanamsa setting")
    parser.add_argument("--language", default="en", help="Language code")
    parser.add_argument("--depth", default="detailed", choices=["basic", "standard", "detailed", "exhaustive"])
    parser.add_argument("--only-first-page", action="store_true", help="Generate only the first page (Kanika-style reference layout)")
    parser.add_argument("--output-dir", default=".", help="Output directory")
    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    birth_data = {
        "person_name": args.name,
        "gender": args.gender,
        "birth_date": args.date,
        "birth_time": args.time,
        "birth_place": args.place,
        "latitude": args.lat,
        "longitude": args.lon,
        "tz_offset": args.tz,
        "ayanamsa": args.ayanamsa,
        "language": args.language,
        "report_depth": args.depth,
        "only_first_page": bool(args.only_first_page),
    }

    print("=" * 60)
    print("KUNDLI COMPLETE REPORT GENERATOR")
    print("=" * 60)
    print(f"Native: {args.name}")
    print(f"DOB: {args.date} {args.time}")
    print(f"Place: {args.place} ({args.lat}, {args.lon})")
    print("-" * 60)

    print("[1/4] Running all backend engines...")
    assembled, debug, audit = run_all_engines(birth_data)
    if args.only_first_page:
        assembled["output_mode"] = "first_page"
    print(f"      Engines reused: {len(audit['reused'])}")
    print(f"      Engines missing/failed: {len(audit['missing'])}")

    print("[2/4] Building section coverage...")
    coverage = build_section_coverage(assembled, audit, birth_data)

    print("[3/4] Generating PDF report...")
    pdf_bytes = build_full_report(assembled)
    pdf_filename = "kundli_first_page.pdf" if args.only_first_page else "kundli_full_report.pdf"
    pdf_path = os.path.join(args.output_dir, pdf_filename)
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)
    print(f"      PDF saved: {pdf_path} ({len(pdf_bytes)} bytes, ~{len(pdf_bytes)//1024} KB)")

    print("[4/4] Saving debug & audit files...")
    payload_path = os.path.join(args.output_dir, "report_debug_payload.json")
    with open(payload_path, "w", encoding="utf-8") as f:
        json.dump(assembled, f, indent=2, default=str, ensure_ascii=False)
    print(f"      Report payload JSON: {payload_path}")

    debug_path = os.path.join(args.output_dir, "kundli_full_report_debug.json")
    with open(debug_path, "w", encoding="utf-8") as f:
        json.dump(debug, f, indent=2, default=str, ensure_ascii=False)
    print(f"      Debug JSON: {debug_path}")

    coverage_path = os.path.join(args.output_dir, "kundli_section_coverage.json")
    with open(coverage_path, "w", encoding="utf-8") as f:
        json.dump(coverage, f, indent=2, default=str, ensure_ascii=False)
    print(f"      Coverage JSON: {coverage_path}")

    audit_md = build_engine_audit_md(audit, coverage)
    audit_path = os.path.join(args.output_dir, "kundli_engine_audit.md")
    with open(audit_path, "w", encoding="utf-8") as f:
        f.write(audit_md)
    print(f"      Audit MD: {audit_path}")

    print("=" * 60)
    print("DONE. All files generated successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
