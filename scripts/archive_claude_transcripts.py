#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class MovePlan:
    src: Path
    dst: Path


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")


def _iter_projects_dir(projects_root: Path) -> list[Path]:
    return sorted([p for p in projects_root.iterdir() if p.is_dir()])


def _sort_by_mtime_desc(paths: list[Path]) -> list[Path]:
    return sorted(paths, key=lambda p: p.stat().st_mtime, reverse=True)


def _rel_under(path: Path, root: Path) -> Path:
    return Path(path.as_posix().replace(root.as_posix().rstrip("/") + "/", "", 1))


def build_move_plans(
    projects_root: Path,
    archive_root: Path,
    keep_top_level_jsonl: int,
    keep_subagent_jsonl: int,
    move_tool_results: bool,
) -> list[MovePlan]:
    plans: list[MovePlan] = []

    for proj_dir in _iter_projects_dir(projects_root):
        # 1) Top-level conversation transcripts (*.jsonl in project dir)
        top_jsonl = _sort_by_mtime_desc(list(proj_dir.glob("*.jsonl")))
        for p in top_jsonl[keep_top_level_jsonl:]:
            rel = _rel_under(p, projects_root)
            dst = archive_root / rel
            plans.append(MovePlan(src=p, dst=dst))

        # 2) Subagent transcripts (often huge) under any nested "subagents/" directory
        for subagents_dir in proj_dir.glob("**/subagents"):
            if not subagents_dir.is_dir():
                continue
            sub_jsonl = _sort_by_mtime_desc(list(subagents_dir.glob("*.jsonl")))
            for p in sub_jsonl[keep_subagent_jsonl:]:
                rel = _rel_under(p, projects_root)
                dst = archive_root / rel
                plans.append(MovePlan(src=p, dst=dst))

        # 3) Tool results dumps (stdout captures)
        if move_tool_results:
            for tool_results_dir in proj_dir.glob("**/tool-results"):
                if not tool_results_dir.is_dir():
                    continue
                for p in tool_results_dir.rglob("*"):
                    if not p.is_file():
                        continue
                    # Never touch memory files (these are meant to be loaded)
                    if "/memory/" in p.as_posix().replace("\\", "/"):
                        continue
                    rel = _rel_under(p, projects_root)
                    dst = archive_root / rel
                    plans.append(MovePlan(src=p, dst=dst))

    # De-dupe (can happen if globbing overlaps)
    unique: dict[str, MovePlan] = {}
    for plan in plans:
        unique[plan.src.as_posix()] = plan
    return list(unique.values())


def _bytes(path: Path) -> int:
    try:
        return path.stat().st_size
    except OSError:
        return 0


def apply_move_plans(plans: list[MovePlan]) -> tuple[int, int]:
    moved_files = 0
    moved_bytes = 0
    for plan in plans:
        if not plan.src.exists():
            continue
        plan.dst.parent.mkdir(parents=True, exist_ok=True)
        moved_bytes += _bytes(plan.src)
        shutil.move(str(plan.src), str(plan.dst))
        moved_files += 1
    return moved_files, moved_bytes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Archive Claude Code transcripts/tool-results to reduce accidental context bloat.",
    )
    parser.add_argument(
        "--projects-root",
        type=Path,
        default=Path.home() / ".claude" / "projects",
        help="Claude projects directory (default: ~/.claude/projects)",
    )
    parser.add_argument(
        "--archive-root",
        type=Path,
        default=None,
        help="Archive destination root (default: ~/.claude/_trash/projects_archive_<UTCSTAMP>)",
    )
    parser.add_argument(
        "--keep-top-level-jsonl",
        type=int,
        default=3,
        help="Keep newest N top-level *.jsonl per project (default: 3)",
    )
    parser.add_argument(
        "--keep-subagent-jsonl",
        type=int,
        default=1,
        help="Keep newest N subagent *.jsonl per subagents/ folder (default: 1)",
    )
    parser.add_argument(
        "--no-tool-results",
        action="store_true",
        help="Do not move tool-results/ dumps",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would move; make no changes",
    )
    args = parser.parse_args()

    projects_root: Path = args.projects_root.expanduser().resolve()
    if not projects_root.exists():
        raise SystemExit(f"projects root not found: {projects_root}")

    archive_root = args.archive_root
    if archive_root is None:
        archive_root = Path.home() / ".claude" / "_trash" / f"projects_archive_{_utc_stamp()}"
    archive_root = archive_root.expanduser().resolve()

    plans = build_move_plans(
        projects_root=projects_root,
        archive_root=archive_root,
        keep_top_level_jsonl=max(0, args.keep_top_level_jsonl),
        keep_subagent_jsonl=max(0, args.keep_subagent_jsonl),
        move_tool_results=not args.no_tool_results,
    )

    plans = sorted(plans, key=lambda p: p.src.as_posix())
    total_bytes = sum(_bytes(p.src) for p in plans if p.src.exists())
    print(f"projects_root: {projects_root}")
    print(f"archive_root:  {archive_root}")
    print(f"planned_moves: {len(plans)} files, ~{total_bytes/1024/1024:.1f} MB")
    for plan in plans[:200]:
        print(f"MOVE {plan.src} -> {plan.dst}")
    if len(plans) > 200:
        print(f"... ({len(plans)-200} more)")

    if args.dry_run:
        print("dry-run: no changes made")
        return 0

    moved_files, moved_bytes = apply_move_plans(plans)
    print(f"moved: {moved_files} files, {moved_bytes/1024/1024:.1f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

