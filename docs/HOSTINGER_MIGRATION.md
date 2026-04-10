# Hostinger KVM2 VPS — Migration Plan for AstroRattan

## Decision: Moving from Vercel to Hostinger KVM2 VPS
**Date:** 2026-04-10
**Reason:** Eliminate cold starts for 150+ users launching next week
**Status:** PURCHASING — no migration work until confirmed

---

## Hostinger Access

- **API Token:** Available (stored in env, used via REST API)
- **API Base:** https://developers.hostinger.com/api
- **DNS Zone:** astrorattan.com managed via Hostinger DNS API
- **Existing hosting IP:** 82.112.232.116 (shared hosting — test.astrorattan.com lives here)
- **VPS:** Not yet purchased — API returns empty list
- **MCP Server:** `hostinger-api-mcp` installed globally on Mac

### Hostinger API endpoints we'll use:
```
GET  /api/vps/v1/virtual-machines          — list VPS instances
POST /api/vps/v1/virtual-machines          — provision new VPS
GET  /api/dns/v1/zones/astrorattan.com     — DNS records
PUT  /api/dns/v1/zones/astrorattan.com     — update DNS
GET  /api/billing/v1/subscriptions         — active subscriptions
```

---

## Why move

| Problem on Vercel | Solved on VPS |
|---|---|
| 5-8 sec cold starts (Python + Neon) | Always running, 0 cold start |
| 10 sec function timeout (Hobby) | No timeout limit |
| "Something went wrong" errors | Stable, persistent process |
| Neon DB suspends after 5 min | Local PostgreSQL, always on |
| No background jobs | Cron for horoscopes, seeding |
| $39/mo (Vercel Pro + Neon paid) | $10-15/mo all inclusive |

## Hostinger KVM2 Specs

- 2 vCPU, 8GB RAM, 100GB NVMe, 8TB bandwidth
- ~$10-15/month
- Full root SSH access
- Manage from Mac terminal via `ssh root@vps-ip`

## What we'll deploy

- **Backend:** Docker (Dockerfile already exists) — uvicorn with 2-4 workers
- **Frontend:** Static build served by nginx
- **Database:** PostgreSQL installed on same VPS (zero network latency)
- **SSL:** Certbot + Let's Encrypt (auto-renew)
- **Reverse proxy:** nginx → uvicorn backend + static frontend
- **Domain:** Point astrorattan.com DNS to VPS IP

## Existing files ready

- `Dockerfile` — Python 3.12 + pyswisseph + all deps (port fixed to 8028)
- `docker-compose.yml` — backend + frontend services
- `railway.json` — can reference for health check config
- `requirements.txt` — all Python deps
- `frontend/` — Vite build → static dist/

## One-time setup (~30 min)

1. SSH key setup
2. Install Docker + docker-compose
3. Install nginx + certbot
4. Clone repo + create .env
5. docker-compose up -d
6. Configure nginx reverse proxy
7. SSL certificate
8. DNS update

## Ongoing deploys (from Mac)

```bash
ssh root@vps-ip "cd /app/astro_rattan && git pull && docker-compose up -d --build"
```

Or Claude can do it when asked "deploy to hostinger".

## What stays on Vercel (for now)

- Frontend at astrorattan.com (until DNS switches)
- Can keep as fallback during migration

---

**Next step:** Purchase KVM2, share the VPS IP, then we build everything.
