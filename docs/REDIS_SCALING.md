# Redis WebSocket Scaling Guide

## Current Architecture

AstroVedic uses an **in-memory connection dictionary** in `app/routes/messages.py` to manage WebSocket connections for consultation chat:

```python
_active_connections: dict[str, set[WebSocket]] = {}
```

Each consultation ID maps to a set of connected WebSocket clients. Messages are broadcast to all connections in the set.

### Current Limitations
- **Single server only** — the dict lives in one Python process
- **No persistence of connection state** — server restart loses all active connections
- **No horizontal scaling** — a second server instance has its own separate dict
- Works well for **<100 concurrent WebSocket connections** on a single server

## When to Scale

Migrate to Redis pub/sub when **any** of these apply:
- **>100 concurrent WebSocket connections** sustained
- **>1 server instance** deployed (load-balanced)
- **Cross-server message delivery** needed (user A on server 1, astrologer on server 2)
- **Connection state must survive restarts**

## Target Architecture

```
Client A ──WebSocket──► Server 1 ──publish──► Redis Pub/Sub
                                                    │
Client B ──WebSocket──► Server 2 ◄──subscribe───────┘
```

1. Each server subscribes to Redis channels for its active consultations
2. When a message arrives via WebSocket, it is published to Redis
3. Redis fans out to all subscribed servers
4. Each server delivers to its local WebSocket connections

## Implementation Steps

### 1. Install Dependencies

```bash
pip install redis aioredis
```

### 2. Create Redis Client Module

```python
# app/redis_client.py
import os
import redis.asyncio as aioredis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

_pool: aioredis.Redis | None = None

async def get_redis() -> aioredis.Redis:
    global _pool
    if _pool is None:
        _pool = aioredis.from_url(REDIS_URL, decode_responses=True)
    return _pool

async def close_redis():
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
```

### 3. Replace In-Memory Dict with Redis Pub/Sub

```python
# app/routes/messages.py (updated)
import json
from app.redis_client import get_redis

# Local connections (this server only)
_local_connections: dict[str, set[WebSocket]] = {}

async def publish_message(consultation_id: str, message: dict):
    """Publish a message to Redis channel for fan-out."""
    r = await get_redis()
    await r.publish(f"consultation:{consultation_id}", json.dumps(message))

async def subscribe_consultation(consultation_id: str, websocket: WebSocket):
    """Subscribe to Redis channel and forward messages to WebSocket."""
    r = await get_redis()
    pubsub = r.pubsub()
    await pubsub.subscribe(f"consultation:{consultation_id}")
    try:
        async for msg in pubsub.listen():
            if msg["type"] == "message":
                await websocket.send_text(msg["data"])
    finally:
        await pubsub.unsubscribe(f"consultation:{consultation_id}")
        await pubsub.close()
```

### 4. Connection Registry in Redis

Track which consultations have active connections across all servers:

```python
async def register_connection(consultation_id: str, server_id: str):
    """Register this server as having active connections for a consultation."""
    r = await get_redis()
    await r.sadd(f"consultation:{consultation_id}:servers", server_id)
    await r.expire(f"consultation:{consultation_id}:servers", 3600)

async def unregister_connection(consultation_id: str, server_id: str):
    """Remove this server from the consultation's connection registry."""
    r = await get_redis()
    await r.srem(f"consultation:{consultation_id}:servers", server_id)
```

### 5. Update Lifespan

```python
# app/main.py
from app.redis_client import close_redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    # ... existing startup
    yield
    await close_redis()
```

## Configuration

Add to `app/config.py`:

```python
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
SERVER_ID = os.getenv("SERVER_ID", "server-1")
```

Add to `docker-compose.yml`:

```yaml
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

## Estimated Effort

- **Redis client module:** 30 minutes
- **Pub/sub integration in messages.py:** 2 hours
- **Connection registry:** 30 minutes
- **Testing (multi-server simulation):** 1 hour
- **Total:** ~4 hours

## No Code Changes Needed Now

This document is for **future reference only**. The in-memory connection dict works correctly for single-server deployment and the current user base. Migrate only when the thresholds above are reached.
