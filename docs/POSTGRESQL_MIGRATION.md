# PostgreSQL Migration Guide

## Current State

Astro Rattan uses **SQLite with WAL mode** (Write-Ahead Logging). This provides:
- Single-writer concurrency (readers never block)
- Zero-config setup (no server process)
- Excellent read performance for MVP scale
- File-based — easy backups and portability

## When to Migrate

Migrate to PostgreSQL when **any** of these thresholds are hit:
- **>50 concurrent users** sustained
- **>10 concurrent write operations** per second
- **Multi-server deployment** required (SQLite is single-file, can't share across servers)
- **Advanced queries** needed (window functions, CTEs with MATERIALIZED, JSONB operators)

## Migration Steps

### 1. Install Dependencies

```bash
pip install asyncpg databases[postgresql] alembic
```

Replace `python-jose` and `passlib` stays as-is (auth layer unchanged).

### 2. Convert SQL Placeholders

SQLite uses `?` positional placeholders. PostgreSQL uses `$1, $2, ...` numbered style.

| SQLite | PostgreSQL |
|--------|------------|
| `WHERE id = ?` | `WHERE id = $1` |
| `VALUES (?, ?, ?)` | `VALUES ($1, $2, $3)` |
| `LIMIT ? OFFSET ?` | `LIMIT $1 OFFSET $2` |

**Affected files:** All files in `app/routes/` and `app/database.py`.

### 3. Replace Connection Layer

Replace `sqlite3.connect()` with `asyncpg` connection pool:

```python
# Before (SQLite)
import sqlite3
conn = sqlite3.connect("astrorattan.db")
conn.row_factory = sqlite3.Row

# After (PostgreSQL)
import asyncpg
pool = await asyncpg.create_pool(
    dsn="postgresql://user:pass@localhost:5432/astrorattan",
    min_size=5,
    max_size=20,
)
async with pool.acquire() as conn:
    row = await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
```

Update `app/database.py`:
- Replace `get_db()` generator with async pool-based dependency
- Remove `init_db()` SQLite schema execution — use Alembic migrations instead
- Remove WAL pragma (PostgreSQL handles this natively)

### 4. Convert Primary Keys

```sql
-- SQLite
id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16))))

-- PostgreSQL
id UUID PRIMARY KEY DEFAULT gen_random_uuid()
```

All `TEXT` ID columns become `UUID` type. Foreign keys referencing them also become `UUID`.

### 5. Convert Date/Time Functions

| SQLite | PostgreSQL |
|--------|------------|
| `datetime('now')` | `NOW()` |
| `date('now')` | `CURRENT_DATE` |
| `datetime('now', '+1 hour')` | `NOW() + INTERVAL '1 hour'` |

### 6. Convert Boolean Columns

```sql
-- SQLite (uses INTEGER 0/1)
is_active INTEGER NOT NULL DEFAULT 1
is_approved INTEGER NOT NULL DEFAULT 0

-- PostgreSQL (native BOOLEAN)
is_active BOOLEAN NOT NULL DEFAULT TRUE
is_approved BOOLEAN NOT NULL DEFAULT FALSE
```

Update Python code: replace `if row["is_active"]` checks (these still work, but be explicit with `True`/`False` in queries).

### 7. Convert Full-Text Search (FTS5 to tsvector)

```sql
-- SQLite FTS5
CREATE VIRTUAL TABLE products_fts USING fts5(name, description, category);
SELECT * FROM products_fts WHERE products_fts MATCH 'gemstone';

-- PostgreSQL Full-Text Search
ALTER TABLE products ADD COLUMN search_vector tsvector;
CREATE INDEX idx_products_search ON products USING GIN(search_vector);

UPDATE products SET search_vector =
    to_tsvector('english', coalesce(name, '') || ' ' || coalesce(description, '') || ' ' || coalesce(category, ''));

-- Query
SELECT * FROM products WHERE search_vector @@ to_tsquery('english', 'gemstone');
```

Remove FTS5 virtual tables, triggers, and `_rebuild_fts()` function. Replace with PostgreSQL triggers that update `search_vector` on INSERT/UPDATE.

### 8. Data Migration

```bash
# Export from SQLite
sqlite3 astrorattan.db .dump > astrorattan_dump.sql

# Manual conversion needed for:
# - hex(randomblob(16)) → gen_random_uuid()
# - INTEGER booleans → TRUE/FALSE
# - datetime('now') → NOW()

# Or use pgloader (automated):
pgloader astrorattan.db postgresql://user:pass@localhost/astrorattan
```

For a clean migration, use a Python script that reads from SQLite and inserts into PostgreSQL, handling type conversions programmatically.

## Configuration Changes

Update `app/config.py`:

```python
# Before
DB_PATH = os.getenv("DB_PATH", "astrorattan.db")

# After
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost:5432/astrorattan")
DB_POOL_MIN = int(os.getenv("DB_POOL_MIN", "5"))
DB_POOL_MAX = int(os.getenv("DB_POOL_MAX", "20"))
```

## Estimated Effort

- **Core migration (database.py + all routes):** 4-6 hours
- **FTS conversion:** 1-2 hours
- **Testing + data migration:** 1-2 hours
- **Total:** 6-10 hours

## No Code Changes Needed Now

This document is for **future reference only**. SQLite WAL mode is sufficient for the current MVP scale. Migrate only when the thresholds above are reached.
