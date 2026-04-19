#!/usr/bin/env python3
"""
Watch transit variants generation progress.
Run from project root: python3 scripts/watch_variants.py
"""
import json
import os
import sys
import time
from pathlib import Path

PROGRESS_FILE = Path(".claude/debug/transit_variants_progress.json")
LOG_FILE      = Path(".claude/debug/transit_variants_run.log")

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
TOTAL   = 108  # 9 planets × 12 houses

PLANET_COLORS = {
    "Sun":     "\033[93m",   # yellow
    "Moon":    "\033[97m",   # white
    "Mars":    "\033[91m",   # red
    "Mercury": "\033[92m",   # green
    "Jupiter": "\033[94m",   # blue
    "Venus":   "\033[95m",   # magenta
    "Saturn":  "\033[90m",   # dark grey
    "Rahu":    "\033[96m",   # cyan
    "Ketu":    "\033[35m",   # purple
}

RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
GREY   = "\033[90m"


def clear():
    os.system("clear")


def bar(done: int, total: int, width: int = 30) -> str:
    pct = done / total if total else 0
    filled = int(width * pct)
    b = "█" * filled + "░" * (width - filled)
    return f"[{b}] {done}/{total} ({pct*100:.0f}%)"


def eta_str(done: int, total: int, elapsed_s: float) -> str:
    if done == 0:
        return "calculating..."
    remaining = total - done
    rate = done / elapsed_s  # slots per second
    secs = int(remaining / rate)
    h, m = divmod(secs, 3600)
    m, s = divmod(m, 60)
    if h:
        return f"~{h}h {m}m"
    return f"~{m}m {s}s"


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        try:
            return json.loads(PROGRESS_FILE.read_text())
        except Exception:
            return {}
    return {}


def tail_log(n: int = 5) -> list[str]:
    if not LOG_FILE.exists():
        return []
    try:
        lines = LOG_FILE.read_text().splitlines()
        return [l for l in lines[-n:] if l.strip()]
    except Exception:
        return []


def planet_grid(progress: dict) -> str:
    lines = []
    for planet in PLANETS:
        color = PLANET_COLORS.get(planet, "")
        done_houses = [h for h in range(1, 13) if f"{planet}_{h}" in progress]
        cells = ""
        for h in range(1, 13):
            key = f"{planet}_{h}"
            if key in progress:
                cells += f"{GREEN}■{RESET}"
            else:
                cells += f"{GREY}·{RESET}"
        pct = len(done_houses) / 12 * 100
        b = bar(len(done_houses), 12, width=12)
        lines.append(f"  {color}{planet:<9}{RESET}  {cells}  {b}")
    return "\n".join(lines)


def main():
    start_time = None
    first_done = 0

    print(f"{CYAN}{BOLD}Transit Variants Monitor{RESET} — Ctrl+C to exit\n")

    try:
        while True:
            progress = load_progress()
            done = len(progress)

            if done > 0 and start_time is None:
                start_time = time.time()
                first_done = done

            elapsed = time.time() - start_time if start_time else 0
            done_since_start = done - first_done

            clear()

            # Header
            print(f"{CYAN}{BOLD}━━━  Transit Variants Generator  ━━━{RESET}")
            print(f"  Model : qwen3.5:27b  |  1 worker  |  4 variants/slot")
            print()

            # Overall bar
            overall_bar = bar(done, TOTAL, width=40)
            status_color = GREEN if done == TOTAL else YELLOW
            print(f"  {BOLD}Overall{RESET}  {status_color}{overall_bar}{RESET}")

            if done == TOTAL:
                print(f"\n  {GREEN}{BOLD}✅ ALL DONE! Run write_output to finalize.{RESET}\n")
            else:
                eta = eta_str(done_since_start, TOTAL - first_done, elapsed) if done_since_start > 0 else "..."
                rate = f"{done_since_start / elapsed * 60:.1f} slots/min" if elapsed > 0 and done_since_start > 0 else "..."
                print(f"  ETA    : {YELLOW}{eta}{RESET}   Rate: {DIM}{rate}{RESET}")

            print()

            # Per-planet grid
            print(f"  {BOLD}Per-planet  (■=done  ·=pending){RESET}  Houses 1→12")
            print()
            print(planet_grid(progress))
            print()

            # Recent log
            recent = tail_log(6)
            if recent:
                print(f"  {BOLD}Recent activity{RESET}")
                for line in recent:
                    if "✅" in line:
                        print(f"  {GREEN}{line}{RESET}")
                    elif "❌" in line or "💀" in line:
                        print(f"  {RED}{line}{RESET}")
                    elif "ollama error" in line.lower():
                        print(f"  {YELLOW}{line}{RESET}")
                    else:
                        print(f"  {DIM}{line}{RESET}")

            print()
            print(f"  {GREY}Refreshing every 10s  |  Progress: {PROGRESS_FILE}{RESET}")

            if done == TOTAL:
                print(f"\n  {CYAN}Output will be written to app/transit_variants.py{RESET}")
                break

            time.sleep(10)

    except KeyboardInterrupt:
        print(f"\n{GREY}Exited monitor. Generation continues in background.{RESET}\n")


if __name__ == "__main__":
    main()
