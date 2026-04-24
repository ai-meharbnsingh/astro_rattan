# Tier 1 Critical Fixes Guide

## Priority 1: Fix localhost:5198 API Calls in Production

**Problem**: Frontend is calling `http://localhost:5198/api/...` instead of relative `/api/...` URLs. This causes 30+ 500 errors per session across all browsers.

**Root Cause**: The production build used the wrong VITE_API_URL environment variable during build.

**Fix**:
1. Rebuild frontend with correct environment:
```bash
cd frontend
rm -rf dist
VITE_API_URL= npm run build  # Empty string = use relative URLs
cd ..
```

2. Verify the built code uses relative URLs:
```bash
grep -r "http://localhost" frontend/dist/assets/ 2>/dev/null || echo "✅ No localhost URLs in built code"
```

3. Deploy the new dist:
```bash
# Copy to production
scp -r frontend/dist/* root@astrorattan.com:/var/www/astrorattan/dist/
```

---

## Priority 2: Fix Nginx Static File Serving for JS Chunks

**Problem**: Lazy-loaded JavaScript chunks fail to load with MIME type error. Pages like Numerology, Vastu, and Client Profile show blank screens.

**Root Cause**: Nginx `try_files $uri $uri/ /index.html` falls back to serving index.html for any non-existent path, including missing JS files. This returns HTML with text/html MIME type instead of application/javascript.

**Fix**: Update nginx.conf to properly handle asset requests:

```nginx
# Location block 1: Static assets (must come BEFORE the catch-all)
location ~ ^/assets/.*\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot|map)$ {
    root /var/www/astrorattan/dist;
    expires 1y;
    add_header Cache-Control "public, immutable";
    # If file doesn't exist, return 404 (not index.html)
    error_page 404 /404.html;
}

# Location block 2: SPA catch-all (routes to index.html)
location / {
    root /var/www/astrorattan/dist;
    # For actual SPA routes, fall back to index.html
    # But NOT for asset files (handled above)
    if (!-e $request_filename) {
        rewrite ^.*$ /index.html break;
    }
}
```

**Alternative simpler fix** (if the above is complex):
```nginx
location / {
    root /var/www/astrorattan/dist;
    try_files $uri $uri/ @fallback;
}

location @fallback {
    rewrite ^.*$ /index.html break;
}
```

**Test after fix**:
```bash
# SSH to server
ssh root@145.223.21.39

# Test nginx syntax
nginx -t

# Reload nginx
systemctl reload nginx

# Verify a JS chunk loads with correct MIME type
curl -I https://astrorattan.com/assets/vendor-react-*.js | grep Content-Type  # Should be application/javascript
```

---

## Priority 3: Fix Broken SPA Routes (6 routes redirecting wrong)

**Problem**: 6 core routes redirect to wrong pages:
- `/` → `/astrologer` (should be landing page or stay home)
- `/dashboard` → `/panchang` or `/astrologer` (inconsistent)
- `/horoscope` → `/panchang` (redirects away)
- `/vastu` → `/horoscope` (redirects away)
- `/admin` → `/numerology` (access guard broken)
- `/astrologer` → `/lal-kitab` on iOS (inaccessible)

**Root Cause**: Route guards or redirect middleware in App.tsx or a router config file is misconfigured.

**Fix**: Open `frontend/src/App.tsx` and find the Routes section. Look for:
1. Any `Navigate` components with incorrect `to` props
2. Any `useEffect` hooks that call `navigate()` with hardcoded paths
3. Any route guards checking user role and redirecting

Expected behavior:
- `/` → Should load Home or redirect only if not authenticated
- `/dashboard` → Should load Dashboard (not redirect)
- `/horoscope` → Should load Horoscope page
- `/vastu` → Should load Vastu page
- `/admin` → Should load Admin OR redirect to `/` if not admin role (with error message)
- `/astrologer` → Should load Astrologer dashboard

**Search for redirect issues**:
```bash
grep -n "navigate\|Navigate\|to=" frontend/src/App.tsx | head -20
```

**After fixing**: 
```bash
npm run build
# Test each route in browser
```

---

## Priority 4: Add Missing `/register` Route

**Problem**: New user signup is impossible. `/register` returns 404.

**Root Cause**: The `/register` route is missing from the SPA router.

**Fix**: Open `frontend/src/App.tsx` and find the Routes section. Add:

```tsx
<Route path="/register" element={<AuthPage initialTab="register" />} />
```

(or whatever the correct component/prop is for the registration form)

**Find the auth component**:
```bash
grep -r "register\|Register" frontend/src/sections/ --include="*.tsx" | grep -i "function\|export" | head -5
```

**Verify**: After building and deploying, test that `/register` shows the signup form.

---

## Priority 5: Fix Astrologer Dashboard Tab Switching (Firefox)

**Problem**: Clicking tabs (Overview/Clients/Activity/Consultations) doesn't update the main content area.

**Root Cause**: Tab switch event handler not updating state OR content components not re-rendering.

**Fix**: Open `frontend/src/sections/AstrologerDashboard.tsx` and check:

1. Is there a `useState` for `activeTab`?
2. Are the tab buttons calling `setActiveTab(tabName)` on click?
3. Are the tab content components keyed properly or conditionally rendered based on `activeTab`?

**Example fix**:
```tsx
const [activeTab, setActiveTab] = useState('overview');

return (
  <>
    <div className="tab-buttons">
      {['overview', 'clients', 'activity', 'consultations'].map(tab => (
        <button key={tab} onClick={() => setActiveTab(tab)} className={activeTab === tab ? 'active' : ''}>
          {tab.charAt(0).toUpperCase() + tab.slice(1)}
        </button>
      ))}
    </div>
    
    {activeTab === 'overview' && <OverviewContent />}
    {activeTab === 'clients' && <ClientsContent />}
    {activeTab === 'activity' && <ActivityContent />}
    {activeTab === 'consultations' && <ConsultationsContent />}
  </>
);
```

---

## Priority 6: Fix Lal Kitab Report Not Rendering After Form Submit

**Problem**: Click "Generate Lal Kitab Kundli" → form submits → main content area goes blank. Expected: Report tabs should appear.

**Root Cause**: Either:
1. API call fails and error isn't handled
2. API response doesn't match expected shape
3. Component doesn't update state with API response
4. Conditional rendering logic is broken

**Fix**: Open `frontend/src/sections/LalKitabPage.tsx` and check:

1. Check the `generate` or `submit` button's click handler:
```tsx
// Should call API like:
const res = await api.post('/api/lalkitab/generate', { name, dob, ... });
setReport(res);  // Save response to state
```

2. Check the render logic:
```tsx
{report ? (
  <LalKitabReportTabs report={report} />
) : (
  <LalKitabForm onSubmit={handleGenerateKundli} />
)}
```

3. Check if API errors are being swallowed:
```tsx
// Find the submit handler and add error logging
const handleGenerateKundli = async (data) => {
  try {
    const res = await api.post('/api/lalkitab/generate', data);
    setReport(res);  // Should update state
  } catch (err) {
    console.error('Lal Kitab error:', err);  // Should log error
    // Show error to user
  }
};
```

---

## Implementation Order

Execute in this sequence:

1. **Rebuild frontend** (Priority 1) — takes ~2 min
2. **Fix nginx config** (Priority 2) — takes ~5 min
3. **Reload nginx and test static files** — takes ~3 min
4. **Fix SPA routes** (Priority 3) — takes ~15-20 min (need to locate and fix redirect logic)
5. **Add /register route** (Priority 4) — takes ~5 min
6. **Fix Astrologer Dashboard tabs** (Priority 5) — takes ~10 min (search, understand, fix)
7. **Fix Lal Kitab report** (Priority 6) — takes ~10 min (similar process)

After each fix:
- Run `npm run build` in frontend
- Test locally (if possible) or deploy and test on production
- Verify the specific page/functionality works

**Total estimated time**: 60-90 minutes

---

## Deployment Process

```bash
# After all fixes are made locally:

# 1. Build frontend with correct env
cd frontend
VITE_API_URL= npm run build
cd ..

# 2. Update nginx config on server
scp nginx.conf root@145.223.21.39:/etc/nginx/sites-available/astrorattan

# 3. Test nginx syntax
ssh root@145.223.21.39 'nginx -t'

# 4. Reload nginx
ssh root@145.223.21.39 'systemctl reload nginx'

# 5. Deploy new frontend
scp -r frontend/dist/* root@145.223.21.39:/var/www/astrorattan/dist/

# 6. Verify with browser
# - Visit https://astrorattan.com/numerology (should load, not blank)
# - Visit https://astrorattan.com/register (should load signup)
# - Visit https://astrorattan.com/horoscope (should work, not redirect)
# - Click dashboard tabs (should switch content)
# - Test Lal Kitab form (should show report after submit)
```
