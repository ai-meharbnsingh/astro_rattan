# 🪐 AstroVedic — Vedic Astrology Platform

> **A comprehensive Vedic Astrology platform with AI-powered insights, e-commerce, consultations, and the unique io-gita semantic gravity engine.**

---

## 🔗 Live Services

| Service | Environment | URL | Status |
|---------|-------------|-----|--------|
| **Frontend** | Production | https://astrovedic-web.vercel.app | ✅ Live |
| **Backend API** | Production | https://astro-rattan-api.onrender.com | ✅ Live |
| **Health Check** | — | https://astro-rattan-api.onrender.com/health | ✅ OK |

### Latest Deployments
| Deployment | URL | Age |
|------------|-----|-----|
| Frontend (Latest) | https://astrovedic-71n53jseg-ai-meharbnsinghs-projects.vercel.app | 20m |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           FRONTEND (Vercel)                             │
│  React 18 + TypeScript + Vite + Tailwind CSS + shadcn/ui + Three.js    │
│  ├─ Observatory Theme (Black + Gold)                                    │
│  ├─ 3D Cosmic Background with Zodiac Symbols                          │
│  └─ Responsive PWA Support                                              │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           BACKEND (Render)                              │
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
| **Project** | AstroVedic (P28) |
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

### Community
- ✅ **Forum** — Discussion threads & replies
- ✅ **Blog** — Astrology articles
- ✅ **Comments & Likes** — Engagement features
- ✅ **Prashnavali** — Ask questions, get answers

### Additional Features
- ✅ **Daily Horoscope** — Zodiac predictions
- ✅ **Panchang** — Daily almanac
- ✅ **Numerology** — Name/number analysis
- ✅ **Tarot Reading** — Card predictions
- ✅ **Palmistry** — Hand analysis
- ✅ **Cosmic Calendar** — Auspicious dates
- ✅ **Library** — PDF/eBook access
- ✅ **Gamification** — Badges, points, levels
- ✅ **Referral System** — Invite & earn
- ✅ **Notifications** — In-app & email
- ✅ **WhatsApp Integration** — Message notifications
- ✅ **Admin Dashboard** — Full CMS

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | Web framework |
| **Python 3.11** | Language |
| **SQLite (WAL)** | Database |
| **Swiss Ephemeris** | Astronomical calculations |
| **PyJWT** | Authentication |
| **Passlib** | Password hashing |
| **FPDF2** | PDF generation |
| **OpenAI/Gemini** | AI integration |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 18** | UI framework |
| **TypeScript** | Type safety |
| **Vite** | Build tool |
| **Tailwind CSS** | Styling |
| **shadcn/ui** | Component library |
| **Three.js** | 3D backgrounds |
| **React Context + useState** | State management |

---

## 📁 Project Structure

```
astrovedic/
├── app/                          # Backend FastAPI
│   ├── routes/                   # 37 API route modules
│   │   ├── kundli.py            # Kundli CRUD + analysis
│   │   ├── auth.py              # JWT authentication
│   │   ├── payments.py          # Razorpay/Stripe
│   │   ├── consultation.py      # Booking system
│   │   ├── forum.py             # Community forum
│   │   ├── ai.py                # AI chat & analysis
│   │   └── ... (30+ more)
│   ├── engines/                 # Astrology calculation engines
│   │   ├── astro_engine.py      # Core calculations
│   │   ├── dasha_engine.py      # Dasha periods
│   │   ├── matching_engine.py   # Kundli matching
│   │   ├── dosha_engine.py      # Yoga/dosha analysis
│   │   └── ... (14+ more)
│   ├── models.py                # Pydantic models
│   ├── auth.py                  # JWT utilities
│   ├── config.py                # App configuration
│   └── main.py                  # App entry point
├── frontend/                     # React Frontend
│   ├── src/
│   │   ├── sections/            # Page sections (25+)
│   │   ├── components/          # Reusable components
│   │   ├── lib/                 # Utilities & API
│   │   └── App.tsx              # Main app
│   └── package.json
├── tests/                        # Test suite (219 tests)
├── static/                       # Static assets
├── Dockerfile                    # Container config
├── render.yaml                   # Render deployment
└── docker-compose.yml           # Local development
```

---

## 🚀 API Endpoints Overview

### Core Modules (73+ endpoints)

| Module | Endpoints | Description |
|--------|-----------|-------------|
| `/api/auth` | 8 | Login, register, JWT, password reset |
| `/api/kundli` | 18 | Generate, match, dasha, divisional, PDF |
| `/api/payments` | 6 | Orders, transactions, webhooks |
| `/api/consultation` | 10 | Booking, slots, reviews |
| `/api/astrologer` | 8 | Profiles, availability, earnings |
| `/api/forum` | 10 | Threads, replies, likes, search |
| `/api/blog` | 6 | Articles, comments |
| `/api/products` | 8 | Catalog, cart, bundles |
| `/api/horoscope` | 4 | Daily predictions |
| `/api/admin/*` | 15 | Dashboard, users, orders, content |
| `/api/ai` | 5 | Chat, analysis, recommendations |
| `/ws/notifications` | 1 | WebSocket real-time updates |
| ... | ... | 20+ more modules |

---

## ⚙️ Configuration

### Environment Variables

#### Backend (.env)
```env
DATABASE_URL=sqlite:///astrovedic.db
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=24
CORS_ORIGINS=https://astrovedic-web.vercel.app,http://localhost:5198
GEMINI_API_KEY=your-gemini-key
OPENAI_API_KEY=your-openai-key
RAZORPAY_KEY_ID=your-razorpay-key
RAZORPAY_KEY_SECRET=your-razorpay-secret
```

#### Frontend (.env)
```env
VITE_API_URL=https://astro-rattan-api.onrender.com
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app

# E2E tests
cd e2e && npm test
```

**Current Status:** 219 tests passed ✅

---

## 📦 Deployment

### Backend (Render)
```bash
# Auto-deploy on git push
git push origin main

# Manual deploy
render deploys create srv-d73mcuogjchc73apnnl0 --confirm
```

### Frontend (Vercel)
```bash
# Deploy
cd frontend && vercel --prod

# Environment variables
vercel env add VITE_API_URL production
```

---

## 🎨 UI/UX Design

- **Theme:** Observatory (Black #000000 + Gold #d4af37)
- **Background:** 3D floating zodiac symbols with Three.js
- **Typography:** Traditional Indian aesthetics
- **Icons:** Lucide React
- **Components:** shadcn/ui with custom theming

---

## 🔐 Security

- JWT-based authentication
- Password hashing (bcrypt)
- CORS protection
- Rate limiting (60 req/min)
- SQL injection protection (parameterized queries)

---

## 📄 License

Private — All rights reserved.

---

## 👨‍💻 Developer

Built with ❤️ by **Meharban Singh**

---

## 🔗 Quick Links

| Resource | Link |
|----------|------|
| 🌐 Live App | https://astrovedic-web.vercel.app |
| 🔌 API Base | https://astro-rattan-api.onrender.com |
| 💓 Health | https://astro-rattan-api.onrender.com/health |
| 📚 API Docs | https://astro-rattan-api.onrender.com/docs |
| 🧪 Redoc | https://astro-rattan-api.onrender.com/redoc |

---

*Last updated: March 29, 2026*
