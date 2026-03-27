"""Generate local Library audio files and map audio_url in content_library.

Usage:
  python3 -m app.generate_library_audio
  python3 -m app.generate_library_audio --force --voice Samantha --limit 20
"""
from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path

import psycopg2
import psycopg2.extras

from app.database import DATABASE_URL


def _speech_text(row: dict) -> str:
    chapter = row.get("chapter")
    verse = row.get("verse")
    title = (row.get("title") or "").strip()
    translation = (row.get("translation") or "").strip()
    content = (row.get("content") or "").strip()

    if chapter and verse:
        prefix = f"Bhagavad Gita. Chapter {chapter}, Verse {verse}."
    elif chapter:
        prefix = f"Bhagavad Gita. Chapter {chapter}."
    else:
        prefix = "Spiritual Library."

    core = translation or content or title or "Audio content."
    core = core.replace("\n", " ").strip()
    # Keep snippets short so generation is fast and deterministic.
    snippet = core[:320]
    return f"{prefix} {title}. {snippet}".strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate local audio files for library content.")
    parser.add_argument("--voice", default="Samantha", help="macOS `say` voice")
    parser.add_argument("--limit", type=int, default=0, help="Max items to process (0 = all)")
    parser.add_argument("--force", action="store_true", help="Regenerate even if audio_url already exists")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    out_dir = project_root / "static" / "audio" / "library"
    out_dir.mkdir(parents=True, exist_ok=True)

    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            where = "category IN ('gita','mantra','aarti','chalisa')"
            if not args.force:
                where += " AND (audio_url IS NULL OR audio_url = '')"
            cur.execute(
                f"""
                SELECT id, category, chapter, verse, title, content, translation, audio_url
                FROM content_library
                WHERE {where}
                ORDER BY category, chapter NULLS FIRST, verse NULLS FIRST, title
                """
            )
            rows = cur.fetchall()

            if args.limit > 0:
                rows = rows[: args.limit]

            created = 0
            updated = 0
            skipped = 0

            for row in rows:
                item_id = row["id"]
                rel_path = f"/static/audio/library/{item_id}.m4a"
                out_path = out_dir / f"{item_id}.m4a"

                if out_path.exists() and not args.force:
                    # Ensure DB points to existing file.
                    cur.execute("UPDATE content_library SET audio_url = %s WHERE id = %s", (rel_path, item_id))
                    updated += 1
                    continue

                text = _speech_text(row)
                try:
                    subprocess.run(
                        ["say", "-v", args.voice, text, "-o", str(out_path)],
                        check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )
                    created += 1
                    cur.execute("UPDATE content_library SET audio_url = %s WHERE id = %s", (rel_path, item_id))
                    updated += 1
                except Exception:
                    skipped += 1

            conn.commit()
            print(f"Processed={len(rows)} created={created} updated={updated} skipped={skipped}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
