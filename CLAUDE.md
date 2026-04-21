## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Only read graphify artifacts when you explicitly need repo-level structure (architecture, “where is X implemented?”, dependency map).
- Prefer `graphify-out/GRAPH_REPORT.md` or `graphify-out/wiki/index.md` (if it exists); avoid loading `graphify-out/graph.json` or anything under `graphify-out/cache/` (too large).
- After modifying code files in this session, run `python3 -c "from graphify.watch import _rebuild_code; from pathlib import Path; _rebuild_code(Path('.'))"` to keep the graph current.
