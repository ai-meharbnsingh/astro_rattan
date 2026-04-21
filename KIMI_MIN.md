# KIMI (Minimal) — Low-Token QC Prompt

Use this instead of `KIMI.md` when you want Kimi/QC behavior without burning a large context budget.

## Rules
- Only load the minimum repo files needed for the task at hand.
- Do not read `docs/`, `reports/`, `_trash/`, `.claude/`, or `.git/`.
- Do not load graph artifacts unless explicitly needed; if needed, read only `graphify-out/GRAPH_REPORT.md` (avoid `graphify-out/graph.json` and `graphify-out/cache/`).

## QC Output (required)
```
✓ Done: [what reviewed + what checks ran]
→ Decision: [ACCEPT/CHANGE/REJECT + why]
⚠ Review: [only what must be verified]
```

## When to use full `KIMI.md`
- Only when running the full “QC Director & TDD Parallel Agent Standards” process.
