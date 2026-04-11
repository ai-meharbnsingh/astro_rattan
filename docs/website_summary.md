# Astro Rattan - Website Summary

## Overview

**Astro Rattan** is a comprehensive Vedic astrology web application that combines traditional Jyotish (Indian astrology) with modern AI-powered interpretations. The platform serves both individual users seeking personal astrological insights and astrologers managing multiple clients.

**Website:** https://astrorattan.com  
**Tech Stack:** React + Vite (Frontend), FastAPI + PostgreSQL (Backend), Docker (Deployment)

---

## Core Features

### 1. Kundli (Birth Chart) Generation
- **North Indian & South Indian** chart styles
- **Interactive chart visualization** with clickable houses and planets
- **Real-time calculations** using Swiss Ephemeris (pyswisseph)
- **Sidereal Lahiri ayanamsa** for accurate Vedic positions
- **Comprehensive birth data:** Planets, signs, houses, nakshatras, degrees

### 2. Lal Kitab System (22 Specialized Tabs)
A unique karma-based astrological system with practical remedies:

| Tab | Purpose |
|-----|---------|
| **Dashboard** | Summary of Lal Kitab chart analysis |
| **Kundli** | Visual chart with house-based placement |
| **Planets** | Individual planet analysis (active/sleeping status) |
| **Dosha** | Karmic defect detection (Pitra, Grahan, Shani, Debt) |
| **Remedies** | Simple upay (totke) based on planetary positions |
| **Houses** | Detailed predictions for all 12 houses |
| **Nishaniyan Matcher** | Match real-life signs with chart indicators |
| **Gochar** | Transit analysis vs natal chart |
| **Prediction Studio** | 8 life area forecasts with confidence scores |
| **Remedy Tracker** | Daily compliance tracking with streaks |
| **Chandra Chalana** | 43-day Moon discipline protocol |
| **Marriage/Career/Health/Wealth** | Specific life area predictions |
| **Saved Predictions** | Bookmark favorite predictions |
| **Teva Type** | Ratandh/Dharmi/Nabalik classification |
| **Varshphal** | Annual predictions |
| **Rin (Debts)** | Karmic debt analysis |

### 3. Advanced Astrological Features
- **Divisional Charts (Varga):** D2 (Hora), D3 (Drekkana), D4, D7, D9 (Navamsa), D10 (Dasamsa), D12, D30
- **Ashtakvarga:** Bindu-based strength analysis with SAV charts
- **Planetary Aspects:** Vedic and Western aspect calculations
- **Dasha System:** Vimshottari Dasha with current period highlighting
- **Shadbala:** Planetary strength analysis with visual charts
- **Mundane Astrology:** World event predictions
- **KP System:** Krishnamurti Paddhati with cusps and sub-lords
- **Jaimini Astrology:** Karaka-based predictions

### 4. AI-Powered Features
- **Chart Interpretation:** AI-generated readings using Gemini/OpenAI
- **Ask Astrologer:** Q&A with chart context
- **Gita Wisdom:** Bhagavad Gita-based life guidance
- **Oracle:** Mystical yes/no answers
- **Remedy Suggestions:** Personalized upay recommendations

### 5. User Management
- **Multi-role system:** Users, Astrologers, Admins
- **Client Management:** Astrologers can manage multiple clients
- **Secure Authentication:** JWT tokens with refresh mechanism
- **Notes Widget:** Per-client chart annotations

### 6. Additional Tools
- **Panchang:** Daily Hindu calendar with tithi, nakshatra, yoga
- **Muhurat Finder:** Auspicious timing calculator
- **Kundli Milan:** Compatibility matching for marriage
- **Numerology:** Name and mobile number analysis
- **Yoga/Dosha Analysis:** Rahu-Ketu, Sade Sati, Manglik checks

---

## Technical Architecture

### Backend (FastAPI)
- **Core Engine:** Python with pyswisseph for astronomical calculations
- **Database:** PostgreSQL with JSON support for chart data
- **AI Integration:** Supports Google Gemini and OpenAI APIs
- **Authentication:** JWT-based with role-based access control
- **Admin Dashboard:** Live user tracking, analytics, feedback management

### Frontend (React + TypeScript)
- **UI Framework:** Tailwind CSS with custom sacred/gold theme
- **Charts:** Interactive SVG-based kundli charts
- **State Management:** React hooks with local storage fallback
- **i18n:** Full Hindi/English bilingual support
- **Responsive:** Mobile-friendly design

### Database Schema Highlights
- **Users & Authentication:** JWT tokens, roles, profiles
- **Kundli Storage:** Birth details + calculated chart data
- **Lal Kitab Tables:** Tracker logs, Chandra protocol, journal entries
- **Predictions:** Saved bookmarks for users
- **Feedback:** User ratings, reviews, word clouds
- **Analytics:** Page views, active users, traffic metrics

---

## Unique Selling Points

1. **Lal Kitab Integration:** One of the few platforms with comprehensive Lal Kitab analysis including the 43-day Chandra Chalana protocol

2. **Bilingual Experience:** Full Hindi interface with proper astrological terminology (no awkward translations)

3. **AI + Traditional:** Combines classical Jyotish calculations with modern AI interpretation

4. **Astrologer-Focused:** Tools for professional astrologers to manage client relationships

5. **Comprehensive:** 22+ tabs of analysis covering every aspect of Vedic astrology

---

## Deployment

- **Server:** Hostinger VPS (Ubuntu + Docker)
- **Domain:** astrorattan.com with SSL
- **Reverse Proxy:** Nginx serving static frontend
- **Containerization:** Docker Compose for easy deployment
- **Updates:** Git-based continuous deployment

---

## Future Roadmap

- Real-time transit tracking (ephemeris-based gochar)
- Push notifications for Chandra Chalana daily tasks
- Mobile app (React Native)
- Advanced AI chatbot with voice
- Multi-language support (Sanskrit, Tamil, Telugu)
- Video consultations integration
