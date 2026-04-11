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

## 📦 Deployment (Hostinger)

The application is deployed on Hostinger using Nginx as a reverse proxy.

### Backend Setup
1. Clone the repository to the VPS.
2. Initialize the virtual environment: `python -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run using Gunicorn/Uvicorn: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app`

### Frontend Setup
1. Build the production bundle: `cd frontend && npm install && npm run build`
2. Serve the `dist` folder via Nginx.

---

## 👨‍💻 Developer
Built with ❤️ by **Meharban Singh**

---

*Last updated: April 12, 2026*
