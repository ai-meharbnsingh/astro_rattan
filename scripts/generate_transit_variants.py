"""
Generate 4 additional bilingual Jyotish interpretation variants per planet-house-area slot.

Uses qwen3.5:27b via Ollama with 2 parallel workers.
Run: OLLAMA_NUM_PARALLEL=2 python3 scripts/generate_transit_variants.py

Output: app/transit_variants.py  (540 slots × 4 variants each = 2160 new entries)
Progress: .claude/debug/transit_variants_progress.json  (resumable)
"""
import json
import os
import re
import sys
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import urllib.request

# ── Config ──────────────────────────────────────────────────────────────────
MODEL         = "qwen3.5:27b"
OLLAMA_URL    = "http://localhost:11434/api/chat"
VARIANTS_PER_SLOT = 4
MAX_RETRIES   = 3
PROGRESS_FILE = Path(".claude/debug/transit_variants_progress.json")
OUTPUT_FILE   = Path("app/transit_variants.py")
WORKERS       = 2

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
AREAS   = ["general", "love", "career", "finance", "health"]

# Classical Gochara favorability — used in prompt context
GOCHARA_FAV = {
    "Sun":     [3, 6, 10, 11],
    "Moon":    [1, 3, 6, 7, 10, 11],
    "Mars":    [3, 6, 11],
    "Mercury": [2, 4, 6, 8, 10, 11],
    "Jupiter": [2, 5, 7, 9, 11],
    "Venus":   [1, 2, 3, 4, 5, 8, 9, 11, 12],
    "Saturn":  [3, 6, 11],
    "Rahu":    [3, 6, 11],
    "Ketu":    [3, 6, 11],
}

# ── Load existing fragments for reference ───────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent.parent))
from app.transit_interpretations import TRANSIT_FRAGMENTS


def _gochara_tone(planet: str, house: int) -> str:
    fav = house in GOCHARA_FAV.get(planet, [])
    return "FAVORABLE (benefic Gochara house)" if fav else "CHALLENGING (malefic Gochara house)"


def _planet_karakas(planet: str) -> str:
    karakas = {
        "Sun":     "soul, authority, government, father, vitality, ego",
        "Moon":    "mind, emotions, mother, public, fluids, nourishment",
        "Mars":    "energy, courage, siblings, land, accidents, surgery",
        "Mercury": "intellect, communication, trade, education, skin",
        "Jupiter": "wisdom, expansion, wealth, children, guru, dharma",
        "Venus":   "love, beauty, luxury, vehicles, arts, wife/husband",
        "Saturn":  "discipline, karma, delays, servants, longevity, sorrow",
        "Rahu":    "obsession, foreign, technology, unconventional, illusion",
        "Ketu":    "spirituality, detachment, past karma, liberation, mysticism",
    }
    return karakas.get(planet, "")


def _house_significations(house: int) -> str:
    sigs = {
        1:  "self, personality, physique, vitality, beginnings",
        2:  "wealth, family, speech, food, accumulated resources, right eye",
        3:  "courage, siblings, short travel, communication, hands, desires",
        4:  "home, mother, property, vehicles, inner peace, education foundation",
        5:  "intelligence, children, romance, creativity, speculation, merit",
        6:  "enemies, debt, disease, competition, service, daily routine",
        7:  "marriage, partnerships, business deals, open enemies, foreign",
        8:  "transformation, hidden, death, inheritance, occult, chronic illness",
        9:  "dharma, higher learning, father, fortune, long travel, spirituality",
        10: "career, status, fame, government, authority, public reputation",
        11: "gains, income, elder siblings, social networks, fulfillment of desires",
        12: "loss, expenditure, foreign lands, moksha, hospitals, isolation, sleep",
    }
    return sigs.get(house, "")


def _build_prompt(planet: str, house: int) -> str:
    tone = _gochara_tone(planet, house)
    planet_k = _planet_karakas(planet)
    house_sig = _house_significations(house)
    existing = {}
    for area in AREAS:
        try:
            existing[area] = TRANSIT_FRAGMENTS[planet][house][area]["en"]
        except (KeyError, TypeError):
            existing[area] = ""

    existing_block = "\n".join(
        f'  {a}: "{existing[a]}"' for a in AREAS if existing[a]
    )

    return f"""You are a classical Jyotish scholar writing horoscope interpretations.

TRANSIT: {planet} in house {house} from Moon sign (Chandra Lagna)
GOCHARA TONE: {tone}
{planet.upper()} KARAKAS: {planet_k}
HOUSE {house} SIGNIFICATIONS: {house_sig}

EXISTING INTERPRETATIONS (for reference style — do NOT repeat these):
{existing_block}

TASK: Write {VARIANTS_PER_SLOT} NEW bilingual interpretation variants for each of the 5 life areas.
Each variant must:
- Be 2–3 sentences, specific to {planet} + house {house} combination
- Reference the planet's karakas and house significations
- Reflect the {tone.split()[0].lower()} Gochara nature
- Be DIFFERENT from the existing interpretations and from each other
- Include authentic Hindi (not just transliteration)

Output ONLY this JSON structure, nothing else:
{{
  "general": [{{"en": "...", "hi": "..."}}, {{"en": "...", "hi": "..."}}, {{"en": "...", "hi": "..."}}, {{"en": "...", "hi": "..."}}],
  "love":    [{{"en": "...", "hi": "..."}}, {{"en": "...", "hi": "..."}}, {{"en": "...", "hi": "..."}}, {{"en": "...", "hi": "..."}}],
  "career":  [{{"en": "...", "hi": "..."}}, {{"en": "...", "hi": "..."}}, {{"en": "...", "hi": "..."}}, {{"en": "...", "hi": "..."}}],
  "finance": [{{"en": "...", "hi": "..."}}, {{"en": "...", "hi": "..."}}, {{"en": "...", "hi": "..."}}, {{"en": "...", "hi": "..."}}],
  "health":  [{{"en": "...", "hi": "..."}}, {{"en": "...", "hi": "..."}}, {{"en": "...", "hi": "..."}}, {{"en": "...", "hi": "..."}}]
}}"""


def _call_ollama(prompt: str, attempt: int = 0) -> dict | None:
    payload = json.dumps({
        "model": MODEL,
        "stream": False,
        "think": False,
        "options": {
            "num_predict": 2500,
            "temperature": 0.75 + attempt * 0.05,  # slight increase on retry
            "top_p": 0.9,
        },
        "messages": [
            {
                "role": "system",
                "content": "You are a classical Jyotish scholar. Output ONLY valid JSON. No preamble, no explanation.",
            },
            {"role": "user", "content": prompt},
        ],
    }).encode()

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"  [ollama error] {e}")
        return None


def _parse_response(raw: str) -> dict | None:
    # Strip think tags just in case
    clean = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
    # Extract JSON block
    match = re.search(r"\{[\s\S]*\}", clean)
    if not match:
        return None
    try:
        data = json.loads(match.group())
        # Validate structure
        for area in AREAS:
            if area not in data:
                return None
            if not isinstance(data[area], list) or len(data[area]) < VARIANTS_PER_SLOT:
                return None
            for v in data[area]:
                if "en" not in v or "hi" not in v:
                    return None
        return data
    except json.JSONDecodeError:
        return None


def generate_slot(planet: str, house: int, worker_id: int) -> tuple[str, int, dict | None]:
    key = f"{planet}_{house}"
    prompt = _build_prompt(planet, house)

    for attempt in range(MAX_RETRIES):
        t0 = time.time()
        result = _call_ollama(prompt, attempt)
        elapsed = time.time() - t0

        if result is None:
            print(f"  [W{worker_id}] {key} attempt {attempt+1}: ollama error, retrying...")
            time.sleep(2)
            continue

        raw = result.get("message", {}).get("content", "")
        tok_s = round(result.get("eval_count", 0) / max(result.get("eval_duration", 1), 1) * 1e9, 1)
        parsed = _parse_response(raw)

        if parsed:
            print(f"  [W{worker_id}] ✅ {key} — {elapsed:.0f}s — {tok_s} tok/s")
            return planet, house, parsed
        else:
            print(f"  [W{worker_id}] ❌ {key} attempt {attempt+1}: bad JSON, retrying...")
            print(f"     raw[:200]: {raw[:200]}")
            time.sleep(1)

    print(f"  [W{worker_id}] 💀 {key} FAILED after {MAX_RETRIES} attempts")
    return planet, house, None


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {}


def save_progress(progress: dict):
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2, ensure_ascii=False))


def write_output(variants: dict):
    """Write variants dict to app/transit_variants.py."""
    lines = [
        '"""Auto-generated transit interpretation variants.',
        "",
        "Generated by scripts/generate_transit_variants.py using qwen3.5:27b.",
        "Structure: TRANSIT_VARIANTS[planet][house][area] = [{\"en\": ..., \"hi\": ...}, ...]",
        '"""',
        "from typing import Dict, List",
        "",
        "TRANSIT_VARIANTS: Dict[str, Dict[int, Dict[str, List[Dict[str, str]]]]] = {",
    ]

    for planet in PLANETS:
        if planet not in variants:
            continue
        lines.append(f'    "{planet}": {{')
        for house in range(1, 13):
            h_str = str(house)
            if h_str not in variants[planet]:
                continue
            lines.append(f"        {house}: {{")
            for area in AREAS:
                if area not in variants[planet][h_str]:
                    continue
                area_variants = variants[planet][h_str][area]
                lines.append(f'            "{area}": [')
                for v in area_variants:
                    en = v["en"].replace('"', '\\"')
                    hi = v["hi"].replace('"', '\\"')
                    lines.append(f'                {{"en": "{en}", "hi": "{hi}"}},')
                lines.append("            ],")
            lines.append("        },")
        lines.append("    },")

    lines.append("}")
    OUTPUT_FILE.write_text("\n".join(lines) + "\n")
    print(f"\n✅ Written to {OUTPUT_FILE}")


def main():
    # Build full job list
    all_jobs = [(p, h) for p in PLANETS for h in range(1, 13)]
    total = len(all_jobs)  # 108

    # Load progress
    progress = load_progress()
    done_keys = set(progress.keys())
    pending = [(p, h) for p, h in all_jobs if f"{p}_{h}" not in done_keys]

    print(f"Total slots: {total} | Done: {len(done_keys)} | Pending: {len(pending)}")
    print(f"Model: {MODEL} | Workers: {WORKERS} | Variants per slot: {VARIANTS_PER_SLOT}")

    if not pending:
        print("All slots complete. Writing output...")
        write_output(progress)
        return

    # Estimate time
    est_s = len(pending) * 150 / WORKERS
    print(f"Estimated time: {est_s/60:.0f}–{est_s*1.5/60:.0f} minutes\n")

    # Run parallel generation
    completed = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = {
            executor.submit(generate_slot, p, h, i % WORKERS): (p, h)
            for i, (p, h) in enumerate(pending)
        }

        for future in as_completed(futures):
            planet, house, data = future.result()
            completed += 1

            if data:
                key = f"{planet}_{house}"
                progress[key] = data
                save_progress(progress)

            remaining = len(pending) - completed
            print(f"  Progress: {len(done_keys)+completed}/{total} | Remaining: {remaining}")

    # Write final output
    write_output(progress)
    failed = [(p, h) for p, h in all_jobs if f"{p}_{h}" not in progress]
    if failed:
        print(f"\n⚠️  {len(failed)} slots failed: {failed}")
    else:
        print(f"\n🎉 All {total} slots complete!")


if __name__ == "__main__":
    main()
