# 01 — Problem & Scope

## Problem Statement
Indian astrology platforms (AstroSage, ClickAstro) provide Kundli generation and predictions but lack:
1. **AI-powered interpretation** — users get raw charts with no personalized guidance
2. **io-gita integration** — no platform maps planetary positions to Sanatan philosophical atoms (DHARMA, ATMA, MOKSHA, etc.) to reveal deeper life patterns
3. **Unified experience** — astrology, spiritual content, prashnavali, and astro-products are scattered across separate sites

AstroVedic solves this by combining Swiss Ephemeris-powered calculations with io-gita attractor dynamics and AI interpretation in one platform.

## Target Users
| Persona | Role | Need |
|---------|------|------|
| Spiritual Seeker | Individual exploring Vedic astrology | Kundli generation, AI-guided interpretation, daily Panchang |
| Marriage Planner | Family looking for kundli matching | Compatibility scoring, dosha analysis, muhurat finder |
| Devotee | Daily spiritual practitioner | Mantras, Aarti, Pooja Vidhi, Chalisa, Prashnavali |
| Astro Shopper | Believer in gemstone/rudraksha remedies | Browse products, buy online, track orders |
| Consulting Client | Needs expert astrologer advice | Chat/call/video with professional astrologers |
| Astrologer | Professional providing consultation | Dashboard, schedule, earnings, client management |
| Admin | Platform operator | User management, orders, CMS, AI logs |

## Success Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Kundli generation accuracy | 100% match with Swiss Ephemeris reference | Compare planetary positions with AstroSage for 10 known charts |
| AI response relevance | > 80% user satisfaction (self-rated) | Thumbs up/down on AI responses |
| Panchang accuracy | Tithi/Nakshatra match Drik Panchang | Daily comparison for 30 days |
| API response time (p95) | < 500ms for chart generation | Timing middleware |
| E-commerce conversion | > 2% browse-to-purchase | Analytics |
| Test coverage | > 80% | pytest --cov |

## IN-SCOPE (36 features, 6 waves)

### Wave 1 — Astrology Engine
1. **astro_iogita_engine.py** — Map 9 Vedic planets to 16 io-gita atoms, build atom vectors, identify attractor basins, generate analysis reports. Output to JSON.
2. **Kundli Generation** — Birth chart from date/time/place. 12 houses, 9 planets, 12 signs. Lagna (ascendant), planet positions, house placements.
3. **Horoscope** — Daily/Weekly/Monthly/Yearly text predictions per zodiac sign.
4. **Kundli Matching** — Gun Milan (36-point system), compatibility percentage, mangal dosha check.
5. **Dosha Analysis** — Mangal Dosha detection, Kaal Sarp Dosha, Shani Sade Sati period calculation.
6. **Dasha System** — Vimshottari Dasha calculation (120-year cycle, 9 planets, Mahadasha + Antardasha).
7. **Divisional Charts** — D1 (Rasi), D9 (Navamsa), D10 (Dasamsa) chart generation.
8. **Ashtakvarga** — Bindhu (point) calculation per planet per sign, Sarvashtakvarga totals.
9. **KP System + Lal Kitab** — Krishnamurti Paddhati cuspal chart, Lal Kitab remedies lookup.
10. **Numerology + Tarot + Palmistry** — Numerology from name/DOB, Tarot card draw (78-card deck), palmistry info pages.

### Wave 2 — AI + Panchang
11. **AI Kundli Interpretation** — GPT-4 reads chart data, produces personalized reading.
12. **AI Ask Question** — User asks free-text question, AI interprets against their kundli.
13. **AI Gita** — Q&A powered by Bhagavad Gita text + AI.
14. **AI Remedies** — Personalized remedies (mantras, gemstones, rituals) based on chart analysis.
15. **Daily Panchang** — Tithi, Nakshatra, Yoga, Karana for any date/location.
16. **Rahu Kaal + Choghadiya** — Calculate inauspicious periods based on weekday + sunrise.
17. **Muhurat Finder** — Find auspicious dates/times for Marriage, Griha Pravesh, Business Start, Travel.
18. **Sunrise/Sunset + Festival Calendar** — Location-based astronomical calculations + Hindu festival dates.

### Wave 3 — Spiritual Library + Prashnavali
19. **Bhagavad Gita** — Full 18 chapters, 700 slokas, Sanskrit + English + Hindi. AI commentary per sloka.
20. **Aarti + Mantras** — Collection with text + audio file references.
21. **Pooja Vidhi + Vrat Katha + Chalisa** — Step-by-step ritual guides, fasting stories, devotional hymns (Hanuman Chalisa, Shiv Chalisa, etc.)
22. **Ram Shalaka Prashnavali** — 15x15 grid oracle. User thinks question, picks cell, gets answer.
23. **Hanuman Prashna + Ramcharitmanas + Gita Prashnavali** — Text-based divination from sacred texts.
24. **Yes/No AI Oracle + Tarot AI** — AI-powered divination with context-aware responses.

### Wave 4 — E-Commerce
25. **Product Catalog** — Gemstones (Ruby, Emerald, Blue Sapphire, etc.), Rudraksha (1-14 mukhi), Bracelets, Yantras (Sri Yantra, Navgraha), Vastu products. Categories, images, descriptions, prices.
26. **Cart + Checkout** — Add to cart, quantity management, address form, order summary.
27. **Payment Integration** — COD + Online payment via Razorpay (India) and Stripe (international). Webhook verification.
28. **Order Tracking** — Order status (Placed → Confirmed → Shipped → Delivered), tracking number.

### Wave 5 — Consultation + Admin
29. **Chat with Astrologer** — Real-time WebSocket messaging between client and astrologer. Typing indicators.
30. **Call Booking + Video Consultation** — Schedule appointment slots, initiate video calls (WebRTC or external service link).
31. **Paid Reports** — Detailed PDF report generation (kundli + interpretation). Payment before download.
32. **Admin Panel** — User CRUD, order management, astrologer approval, content CMS, AI usage logs.
33. **Astrologer Dashboard** — Earnings summary, appointment calendar, client list, review management.

### Wave 6 — User Management + Admin Enhancements (added post-audit)
34. **User Profile Management** — update name/phone/DOB/gender/city/avatar, change password, view activity history
35. **Admin Product CRUD** — create/edit/delete products, stock management, activate/deactivate
36. **Admin User Management** — create accounts manually, deactivate/activate users, view user activity

## OUT-OF-SCOPE
1. WhatsApp chatbot integration
2. Affiliate/referral system
3. Multi-language support (Hindi/regional — English only for MVP)
