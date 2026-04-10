# P28 AstroRattan — Development & Production Deployment Process

## Environments

| Environment | Branch | URL | Hosting | Database |
|-------------|--------|-----|---------|----------|
| **Development** | `main` | test.astrorattan.com / Vercel preview | Vercel (free) | Neon PostgreSQL |
| **Production** | `production` | astrorattan.com | Hostinger KVM2 VPS | Local PostgreSQL |

---

## Daily Development Workflow

### Step 1: Code & Push
```
# Work on main branch (always)
git add -A && git commit -m "your message" && git push origin main
```

### Step 2: Auto-deploys to Vercel
- GitHub push triggers CI → tests run → Vercel auto-deploys
- Test at: `test.astrorattan.com` or Vercel preview URL
- No manual action needed

### Step 3: Test with Partner
- Both test on Vercel (dev environment)
- Use your own emails for signup (not client emails)
- Dev OTPs may log to console (no real emails if RESEND_API_KEY removed from Vercel)

### Step 4: Ready for Production
- Say **"deploy to production"** to Claude
- OR manually: `git checkout production && git merge main && git push origin production`
- GitHub CI auto-deploys to Hostinger VPS
- Live at: `astrorattan.com`

---

## What Happens on Each Push

### Push to `main`:
```
GitHub → CI runs tests → Vercel auto-deploys → test.astrorattan.com updated
```
Hostinger NOT touched. Production safe.

### Push/merge to `production`:
```
GitHub → CI runs tests → SSH into Hostinger VPS → git pull → Docker rebuild → nginx reload → astrorattan.com updated
```

---

## Checklist Before Going Live

### One-time Setup (before first 150 users):
- [ ] Verify `astrorattan.com` domain in Resend (email deliverability)
- [ ] Test full signup flow on Hostinger (OTP email arrives in inbox, not spam)
- [ ] Test kundli generation end-to-end on Hostinger
- [ ] Test all tabs: Planets, KP, Dasha, Ashtakvarga, Shadbala, Panchang, Doshas, Divisional, Lal Kitab
- [ ] Test on mobile (scrollable tabs, readable text)
- [ ] Confirm Gaurav's (partner) account works

### Before Each Production Deploy:
- [ ] All changes tested on Vercel (dev)
- [ ] No "Something went wrong" errors on dev
- [ ] Say "deploy to production" or merge main → production
- [ ] After deploy: check `https://astrorattan.com/health` shows `status: ok`
- [ ] Quick test: login → generate one kundli → verify chart loads

---

## Emergency Rollback

If production breaks after deploy:
```
# Option 1: Tell Claude
"rollback production to previous version"

# Option 2: Manual
git checkout production
git revert HEAD
git push origin production
# CI auto-deploys the reverted version
```

---

## Environment Variables

### Same code, different env vars:

| Variable | Vercel (dev) | Hostinger (prod) |
|----------|-------------|-----------------|
| `DATABASE_URL` | `postgresql://...@neon.tech/...` | `postgresql://...@localhost/...` |
| `JWT_SECRET` | Same or different | Same or different |
| `CORS_ORIGINS` | Auto-includes astrorattan.com | Auto-includes astrorattan.com |
| `RESEND_API_KEY` | Remove (dev = no real emails) | Real key (prod = real emails) |
| `VITE_API_URL` | `''` (empty = same origin) | `''` (empty = same origin) |

---

## Key Rules

1. **Never push directly to `production` branch** — always merge from `main`
2. **Never test with real client emails on Vercel** — use your own
3. **Always check `/health` after production deploy**
4. **Same code works on both** — only `.env` differs
5. **When in doubt, test on Vercel first**

---

## Quick Reference Commands

```bash
# Deploy to dev (automatic — just push)
git push origin main

# Deploy to production
git checkout production && git merge main && git push origin production

# Check production health
curl -s https://astrorattan.com/health

# Check VPS status
ssh root@145.223.21.39 "docker logs astrorattan-backend --tail 10"

# Emergency: restart backend on VPS
ssh root@145.223.21.39 "docker restart astrorattan-backend"
```
