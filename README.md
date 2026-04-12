# 🪐 AstroRattan — Vedic Astrology Platform

> **A comprehensive Vedic Astrology platform with AI-powered insights, e-commerce, consultations, and the unique io-gita semantic gravity engine.**

---

## 🔗 Live Services

| Service | Environment | URL | Status |
|---------|-------------|-----|--------|
| **Platform** | Production | https://astrorattan.com | ✅ Live |
| **API Base** | Production | https://astrorattan.com/api | ✅ Live |
| **Health Check** | — | https://astrorattan.com/api/health | ✅ OK |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           FRONTEND (Hostinger)                          │
│  React 18 + TypeScript + Vite + Tailwind CSS + shadcn/ui + Three.js    │
│  ├─ Observatory Theme (Black + Gold)                                    │
│  ├─ 3D Cosmic Background with Zodiac Symbols                          │
│  └─ Responsive PWA Support                                              │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           BACKEND (Hostinger)                           │
│  FastAPI + Python 3.11 + SQLite (WAL Mode) + Swiss Ephemeris           │
│  ├─ JWT Authentication                                                  │
│  ├─ 73+ API Endpoints                                                   │
│  ├─ WebSocket Support                                                   │
│  └─ AI Integration (Gemini/OpenAI)                                      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            ┌──────────┐    ┌──────────┐    ┌──────────┐
            │  SQLite  │    │ Swiss    │    │  AI      │
            │  (WAL)   │    │Ephemeris │    │ Engines  │
            └──────────┘    └──────────┘    └──────────┘
```

---

## 📊 Project Metrics

| Metric | Value |
|--------|-------|
| **Project** | AstroRattan (P28) |
| **Type** | Hybrid (Web + AI + Astrology + E-commerce + Consultation) |
| **Stack** | FastAPI + SQLite WAL + React + Swiss Ephemeris + io-gita |
| **Backend Routes** | 37 API modules |
| **Frontend Sections** | 25+ React components |
| **API Endpoints** | 73+ REST + 1 WebSocket |
| **Test Coverage** | 219 tests passed |
| **Backend Port** | 8028 |
| **Frontend Port** | 5198 |

---

## 🌟 Key Features

### Core Astrology
- ✅ **Kundli Generator** — Birth chart with planetary positions
- ✅ **Kundli Matching** — Ashtakoota Gun Milan (36 points)
- ✅ **Divisional Charts** — D9, D10, and 16+ varga charts
- ✅ **Dasha Analysis** — Vimshottari Mahadasha/Antardasha
- ✅ **Yoga & Dosha** — Mangal Dosha, Kaal Sarp, Raj Yoga, etc.
- ✅ **Transit Predictions** — Gochara analysis
- ✅ **KP Analysis** — Krishnamurti Paddhati
- ✅ **Ashtakvarga** — Sarvashtakvarga & Bhinnashtakvarga
- ✅ **Shadbala** — Six-fold strength calculation
- ✅ **Avakhada Chakra** — Comprehensive birth summary

### AI-Powered (io-gita Engine)
- ✅ **Semantic Gravity Analysis** — 16 Sanatan atoms × 9 planets
- ✅ **8 Attractor Basins** — Dharma-Yukta, Moksha-Marga, etc.
- ✅ **Personalized Insights** — Based on birth chart

### E-Commerce
- ✅ **Products** — Astrology items, gemstones, yantras
- ✅ **Bundles** — Curated packages
- ✅ **Cart & Checkout** — Razorpay/Stripe integration
- ✅ **Orders** — Order tracking & history

### Consultation
- ✅ **Astrologer Booking** — Schedule consultations
- ✅ **Video/Voice/Chat** — Multiple consultation modes
- ✅ **Wallet System** — Recharge & manage balance

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** (Web framework)
- **Python 3.11** (Language)
- **SQLite (WAL)** (Database)
- **Swiss Ephemeris** (Astronomical calculations)
- **PyJWT** (Authentication)
- **OpenAI/Gemini** (AI integration)

### Frontend
- **React 18** (UI framework)
- **TypeScript** (Type safety)
- **Vite** (Build tool)
- **Tailwind CSS** (Styling)
- **shadcn/ui** (Component library)
- **Three.js** (3D backgrounds)

---

## ⚙️ Configuration

### Environment Variables (.env)
```env
JWT_SECRET=your-secret-key
GEMINI_API_KEY=your-gemini-key
RAZORPAY_KEY_ID=your-razorpay-key
SITE_URL=https://astrorattan.com
```

---

## 📦 Deployment (Hostinger VPS)

### Infrastructure Overview

```
Internet → Nginx (SSL/443) → /app/astro_rattan/frontend/dist  (static files)
                           → http://127.0.0.1:8028             (API proxy)

Backend: Docker container   (Python / FastAPI)
Frontend: Built by Node.js directly on server → frontend/dist
Server:   Hostinger VPS — root@145.223.21.39
Domain:   astrorattan.com (Certbot SSL)
```

---

### Production Deploy — One Command

SSH into the server and run:

```bash
bash /app/astro_rattan/deploy.sh
```

That script does everything automatically:
1. `git fetch && git reset --hard origin/main` — pulls latest code
2. `npm ci && npm run build` — builds frontend into `frontend/dist`
3. `docker compose up -d --build backend` — rebuilds & restarts backend
4. `nginx -s reload` — nginx picks up the new frontend immediately

**No manual steps. No `docker cp`. No container restarts needed for frontend changes.**

---

### SSH Access

```bash
ssh root@145.223.21.39
# Password: see .env → HOSTINGER_SSH_PASSWORD
# Or: sshpass -p 'PASSWORD' ssh root@145.223.21.39
```

---

### First-Time Server Setup

Only needed once on a fresh VPS:

```bash
# 1. Clone repo
git clone https://github.com/ai-meharbnsingh/astro_rattan.git /app/astro_rattan
cd /app/astro_rattan

# 2. Create production .env (copy from .env.example and fill values)
cp .env.example .env
nano .env

# 3. Install Node.js 20+ (required by Vite 7)
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# 4. Install Docker + Docker Compose
apt-get install -y docker.io docker-compose-plugin

# 5. Run deploy
bash deploy.sh

# 6. Configure Nginx (copy nginx.conf then get SSL via Certbot)
cp nginx.conf /etc/nginx/sites-available/astrorattan
ln -s /etc/nginx/sites-available/astrorattan /etc/nginx/sites-enabled/
certbot --nginx -d astrorattan.com -d www.astrorattan.com
```

---

### Useful Server Commands

```bash
# Full redeploy (code + frontend + backend)
bash /app/astro_rattan/deploy.sh

# Backend logs
docker logs astro_rattan-backend-1 -f

# Backend status
docker ps

# Restart backend only (no rebuild)
docker compose restart backend

# Nginx status / reload
systemctl status nginx
nginx -s reload

# Check site is live
curl -I https://astrorattan.com
```

---

### Local Development

```bash
# Backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8028

# Frontend (separate terminal)
cd frontend
npm install
npm run dev    # runs on http://localhost:5198
```

---

## 👨‍💻 Developer
Built with ❤️ by **Meharban Singh**

---

*Last updated: April 12, 2026*
