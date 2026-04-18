#!/usr/bin/env python3
"""
i18n-sanitize.py — Codex D9 follow-up.

Scans frontend/src/lib/i18n.ts and flags translation entries that likely
leaked from the auto-scanner and shouldn't be in the bilingual dict:

  - CSS class strings as values (e.g. "text-muted-foreground", "bg-red-500")
  - Locale codes / tokens (e.g. "en-IN")
  - Pure punctuation / numbers / whitespace
  - Truncated keys (auto.*) whose EN value is a single-word CSS-like token
  - Keys where EN and HI are identical (HI not translated)
  - Empty or near-empty values

Output: .claude/debug/i18n_sanitize_report.txt

NON-DESTRUCTIVE — human reviews report, then chooses what to remove.
This script never edits i18n.ts.

Usage:
    python3 scripts/i18n-sanitize.py
    python3 scripts/i18n-sanitize.py --csv          # also emit CSV
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent
I18N_FILE = ROOT / "frontend/src/lib/i18n.ts"
OUT_DIR = ROOT / ".claude/debug"
OUT_FILE = OUT_DIR / "i18n_sanitize_report.txt"
OUT_CSV = OUT_DIR / "i18n_sanitize_report.csv"

# Patterns that indicate a value leaked into translations
CSS_LEAK_RE = re.compile(
    r"^(text-|bg-|border-|flex|grid|p-\d|m-\d|px-|py-|pt-|pb-|w-|h-|rounded|gap-|"
    r"font-|items-|justify-|space-|absolute|relative|fixed|hidden|inline|block|"
    r"overflow-|shadow-|opacity-|ring-|cursor-|transition|duration-|ease-)"
)
LOCALE_CODE_RE = re.compile(r"^[a-z]{2}-[A-Z]{2}$")
PUNCT_ONLY_RE = re.compile(r"^[\s\W\d]*$")
ENTRY_RE = re.compile(r"^\s*(['\"])([^'\"]+)\1\s*:\s*(['\"])(.*?)\3\s*,?\s*$")

def parse_block(lines: List[str], start_idx: int) -> Tuple[Dict[str, str], int]:
    """
    Parse an object-literal block starting at `start_idx` where the next line
    opens with {. Returns (dict, end_idx_of_matching_brace).
    """
    entries: Dict[str, str] = {}
    depth = 0
    for i in range(start_idx, len(lines)):
        line = lines[i]
        if "{" in line:
            depth += line.count("{")
        if "}" in line:
            depth -= line.count("}")
        m = ENTRY_RE.match(line)
        if m:
            entries[m.group(2)] = m.group(4)
        if depth == 0 and i > start_idx:
            return entries, i
    return entries, len(lines) - 1

def find_block_starts(lines: List[str]) -> List[Tuple[str, int]]:
    """Locate EN and HI translation block opening lines by heuristic."""
    starts: List[Tuple[str, int]] = []
    for idx, line in enumerate(lines):
        stripped = line.strip()
        # Looks for `en:` or `hi:` object openings at top-level of the translations map
        if re.match(r"^(en|hi)\s*:\s*\{", stripped):
            lang = stripped.split(":", 1)[0].strip()
            starts.append((lang, idx))
    return starts

def classify(key: str, val_en: str, val_hi: str | None) -> List[str]:
    issues: List[str] = []
    v = val_en.strip()
    if not v:
        issues.append("empty_en")
    if CSS_LEAK_RE.match(v):
        issues.append("css_class_leak")
    if LOCALE_CODE_RE.match(v):
        issues.append("locale_code_leak")
    if v and PUNCT_ONLY_RE.match(v):
        issues.append("punct_or_digits_only")
    if val_hi is not None and val_hi.strip() == v.strip() and v:
        # English and Hindi identical — HI not translated (ignore if value is
        # intentionally universal like proper nouns, but flag anyway for review)
        if not re.fullmatch(r"[A-Za-z0-9 \-./]+", v):
            pass  # likely symbol/emoji; skip
        else:
            issues.append("hi_same_as_en")
    # Truncated auto.* keys — flag only if value is a single lowercase token
    if key.startswith("auto.") and re.fullmatch(r"[a-z][a-zA-Z0-9_-]*", v):
        issues.append("suspicious_token_value")
    return issues

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", action="store_true", help="Also emit CSV report.")
    args = ap.parse_args()

    if not I18N_FILE.exists():
        print(f"✗ Not found: {I18N_FILE}", file=sys.stderr)
        return 2

    text = I18N_FILE.read_text(encoding="utf-8")
    lines = text.splitlines()
    blocks = find_block_starts(lines)

    en: Dict[str, str] = {}
    hi: Dict[str, str] = {}
    for lang, idx in blocks:
        entries, _ = parse_block(lines, idx)
        if lang == "en" and not en:
            en = entries
        elif lang == "hi" and not hi:
            hi = entries

    print(f"Parsed {len(en)} EN keys, {len(hi)} HI keys from {I18N_FILE.name}")

    findings: List[Tuple[str, str, str, List[str]]] = []
    for key, val_en in en.items():
        val_hi = hi.get(key)
        issues = classify(key, val_en, val_hi)
        if issues:
            findings.append((key, val_en, val_hi or "", issues))

    # Summary by issue
    summary: Dict[str, int] = {}
    for _, _, _, iss in findings:
        for i in iss:
            summary[i] = summary.get(i, 0) + 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with OUT_FILE.open("w", encoding="utf-8") as f:
        f.write("i18n sanitize report\n")
        f.write(f"Source: {I18N_FILE}\n")
        f.write(f"EN keys: {len(en)}   HI keys: {len(hi)}\n")
        f.write(f"Flagged: {len(findings)}\n\n")
        f.write("Issue summary:\n")
        for k, c in sorted(summary.items(), key=lambda kv: -kv[1]):
            f.write(f"  {k:<28}  {c}\n")
        f.write("\n" + "-" * 80 + "\n\n")
        for key, val_en, val_hi, iss in findings:
            f.write(f"[{','.join(iss)}]\n")
            f.write(f"  key  : {key}\n")
            f.write(f"  en   : {val_en!r}\n")
            f.write(f"  hi   : {val_hi!r}\n\n")

    print(f"✓ Wrote report: {OUT_FILE}")
    print(f"  Flagged {len(findings)} / {len(en)} keys")
    for k, c in sorted(summary.items(), key=lambda kv: -kv[1]):
        print(f"    {k:<28}  {c}")

    if args.csv:
        with OUT_CSV.open("w", encoding="utf-8") as f:
            f.write("key,issues,en,hi\n")
            for key, val_en, val_hi, iss in findings:
                # basic CSV escaping
                esc = lambda s: '"' + s.replace('"', '""') + '"'
                f.write(f"{esc(key)},{esc(';'.join(iss))},{esc(val_en)},{esc(val_hi)}\n")
        print(f"✓ Wrote CSV: {OUT_CSV}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
