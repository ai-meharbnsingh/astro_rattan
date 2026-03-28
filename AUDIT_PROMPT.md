# P28 AstroVedic — External Audit Prompt

## Project Overview
Full-stack Vedic Astrology platform live at:
- **Frontend:** https://astrovedic-web.vercel.app (React 19 + Vite + Tailwind)
- **Backend:** https://astro-rattan-api.onrender.com (FastAPI + PostgreSQL/Neon)
- **Repo:** https://github.com/ai-meharbnsingh/astro_rattan

## Audit Scope
Review the ENTIRE codebase and live deployment. Score each category 0-10.

### 1. ASTROLOGY ACCURACY (most important)
- Are planetary positions correct? Compare a sample kundli against a known tool (Jagannatha Hora, Astrosage).
- Test: Generate kundli for DOB=1985-08-23, Time=23:15, Place=Delhi (28.6139, 77.2090)
  - Verify Ascendant, Moon sign, Sun sign, planetary houses
- Are Nakshatra calculations correct?
- Is Ayanamsa (Lahiri) applied correctly?
- Are divisional charts (especially D9 Navamsha) computed correctly?
- Are Vimshottari Dasha periods mathematically correct?
- Are Ashtakvarga points following Parashari tables?
- Are Yoga/Dosha detections accurate?

### 2. CODE QUALITY
- Dead code? Unused imports/functions?
- Error handling — do API endpoints handle edge cases?
- SQL injection risks? (psycopg2 parameterized queries?)
- JWT security — is the secret strong? Token expiry reasonable?
- CORS — is it properly restricted?
- Rate limiting — effective?
- Password hashing — bcrypt rounds sufficient?

### 3. FRONTEND QUALITY
- Is the io-gita parchment theme consistent across ALL pages?
- Any remaining dark theme artifacts?
- Hindi translation complete? Any English-only text remaining?
- Mobile responsiveness?
- Accessibility (a11y)?
- Loading states for all async operations?
- Error states shown to users?

### 4. API DESIGN
- RESTful conventions followed?
- Consistent response shapes?
- Pagination on list endpoints?
- Proper HTTP status codes?
- Input validation on all endpoints?

### 5. PERFORMANCE
- Frontend bundle size (currently ~1.8MB) — too large?
- Database queries efficient? Indexes present?
- Connection pooling configured correctly?
- Any N+1 query patterns?

### 6. DEPLOYMENT
- Render free tier cold start — acceptable?
- Vercel SPA routing — working?
- Environment variables secure?
- HTTPS everywhere?

### 7. MISSING FEATURES / BUGS
- What critical features are missing for a production astrology platform?
- Any visible bugs in the UI?
- What would a real user complain about?

## Deliverable
Provide:
1. Score per category (0-10)
2. Overall score (weighted average, astrology accuracy = 3x weight)
3. Top 5 critical issues to fix
4. Top 5 nice-to-have improvements
5. One-paragraph verdict: "Is this production-ready?"
