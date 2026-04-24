# Tier 1 Fixes — Deployment Guide

**Date**: 2026-04-24  
**Status**: Ready to Deploy  
**Fixes Applied**: 3 critical issues addressed  

---

## FIXES APPLIED

### ✅ Fix 1: Added Missing `/register` Route
**File**: `frontend/src/App.tsx`  
**Change**: Added route for `/register` that loads the AuthPage component  
**Line**: 215 added `<Route path="/register" element={<AuthPage />} />`  
**Effect**: New users can now sign up at `/register`  

### ✅ Fix 2: Updated nginx.conf for Proper Static File Serving
**File**: `nginx.conf` (both production and staging servers)  
**Changes**:
- Added explicit `/assets/` location block BEFORE catch-all `/` location
- Fixed `try_files` to use `@fallback` named location instead of direct `/index.html`
- Ensures JS chunks return 404 (not HTML) if missing
- Prevents MIME type errors on lazy-loaded JavaScript files

**Effect**: Pages like Numerology, Vastu, Client Profile will now load correctly  

### ✅ Fix 3: Rebuilt Frontend with Correct Environment Variable
**Command**: `VITE_API_URL= npm run build`  
**Effect**: Frontend now uses relative URLs (`/api/...`) instead of hardcoded `localhost:5198`  
**Build Output**: 
```
✓ 2007 modules transformed
✓ built in 2.87s
```

**New JS chunks generated**:
- All chunk hashes updated (e.g., `index-D8ttrwbD.css` instead of old hashes)
- This is normal and expected after a rebuild

---

## DEPLOYMENT STEPS

### Step 1: Deploy Updated nginx.conf

```bash
# Copy updated nginx.conf to production server
scp /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/nginx.conf \
  root@145.223.21.39:/etc/nginx/sites-available/astrorattan

# SSH into server
ssh root@145.223.21.39

# Test nginx syntax
nginx -t
# Expected output: nginx: the configuration file /etc/nginx/nginx.conf syntax is ok

# Reload nginx (graceful restart, no downtime)
systemctl reload nginx

# Verify nginx is running
systemctl status nginx
```

### Step 2: Deploy Updated Frontend Build

```bash
# Copy new dist files to production
scp -r /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/frontend/dist/* \
  root@145.223.21.39:/var/www/astrorattan/dist/

# Verify files were copied
ssh root@145.223.21.39 "ls -la /var/www/astrorattan/dist/assets/ | head -20"
```

### Step 3: Verify Deployment

After deploying, test each fix:

```bash
# Test 1: Check /register route loads signup form
curl -I https://astrorattan.com/register
# Expected: HTTP 200 (not 404)

# Test 2: Check Numerology page loads (tests JS chunk serving)
curl -I https://astrorattan.com/numerology
# Expected: HTTP 200 (not 404)

# Test 3: Check a JS asset returns correct MIME type
curl -I https://astrorattan.com/assets/vendor-react-*.js | grep Content-Type
# Expected: Content-Type: application/javascript (not text/html)

# Test 4: Check API calls go to correct endpoint
curl -I https://astrorattan.com/api/kundli/current-sky
# Expected: HTTP 200 or 401 (not 500 or connection refused)
```

### Step 4: Manual Testing in Browser

1. **Register Page**:
   - Visit https://astrorattan.com/register
   - Form should load with email, name, password fields
   - Should be able to fill form (don't submit yet)

2. **Numerology Page**:
   - Visit https://astrorattan.com/numerology
   - Should load form (not blank spinner)
   - Tab buttons should be clickable

3. **Vastu Page**:
   - Visit https://astrorattan.com/vastu
   - Should load form (not blank)

4. **Dashboard Tabs**:
   - Login with test account
   - Visit /astrologer
   - Click tabs (Overview, Clients, Activity, Consultations)
   - Content should change when clicking tabs

5. **Lal Kitab Form Submit**:
   - Visit /lal-kitab
   - Fill form with test data
   - Click "Generate Lal Kitab"
   - After generation, tabs should appear (not blank main area)

6. **Mobile Testing**:
   - Test on iPhone 14 Safari (390×844)
   - Test on Android Chrome (393×851)
   - Check:
     - Forms fillable
     - Buttons tappable (44px minimum)
     - Tables readable

---

## ROLLBACK PLAN

If deployment causes issues, rollback is simple:

```bash
# Revert nginx.conf to previous version (from git)
git checkout HEAD~1 -- nginx.conf
scp nginx.conf root@145.223.21.39:/etc/nginx/sites-available/astrorattan
ssh root@145.223.21.39 "nginx -s reload"

# Revert frontend to previous build
# Note: The old dist/ is in git (or you have a backup)
git checkout HEAD~1 -- frontend/dist
# Then re-deploy old dist:
scp -r frontend/dist/* root@145.223.21.39:/var/www/astrorattan/dist/
```

---

## WHAT'S NEXT

After Tier 1 deployment succeeds:

### Phase 2: Continue Testing (Phases 2-5)
- Form submission testing (all 4 forms)
- Table column alignment checking
- Tab switching validation
- Responsive design verification

### Known Remaining Issues (NOT blocking)
These are low-priority and can be addressed after Phase 2:
- Panchang calendar text size (8px on mobile, should be 14px+)
- Mobile touch targets <44px (Language toggle, buttons, etc.)
- Analytics rate limit (429 Too Many Requests)
- One-off issues (blog route instability, etc.)

---

## DEPLOYMENT CHECKLIST

- [ ] Nginx syntax tested (`nginx -t` returns ok)
- [ ] nginx reloaded successfully
- [ ] Frontend dist files copied to server
- [ ] Register page loads (test in browser)
- [ ] Numerology page loads (test in browser)
- [ ] Vastu page loads (test in browser)
- [ ] Dashboard tabs switch correctly (test logged in)
- [ ] Lal Kitab form generates report (test form submission)
- [ ] Mobile layout works (test iPhone and Android viewports)
- [ ] API calls to `/api/...` succeed (check console, not localhost:5198)

---

## FILES MODIFIED

- ✅ `frontend/src/App.tsx` — Added `/register` route (1 line added)
- ✅ `nginx.conf` — Updated production and staging server configs (20+ lines modified)
- ✅ `frontend/dist/` — Rebuilt all assets with correct env var

## ESTIMATED IMPACT

- **Downtime**: 0 seconds (nginx reload is graceful)
- **Performance**: No change (same build optimizations)
- **User Impact**: Fixes access to 3+ pages that were previously broken
- **Rollback Risk**: Very low (simple file replacements)

---

## SUCCESS CRITERIA

After deployment:
- ✅ All 14 pages accessible without redirect loops
- ✅ All JS chunks load with correct MIME type
- ✅ API calls use relative URLs (not localhost)
- ✅ Forms render and are submittable
- ✅ Tabs switch content correctly
- ✅ Mobile layout readable on iPhone and Android

---

**Next Step**: Execute deployment steps above, then run Phase 2-5 testing with all 14 agents in parallel.
