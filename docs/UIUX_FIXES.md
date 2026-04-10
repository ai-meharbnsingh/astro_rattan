# P28 AstroRattan — UI/UX Fix Plan (Kimi Audit 2026-04-10)

## Overall Score: 5.5/10 (C+)

---

## AREA 1: COLOR SYSTEM (Score: 5/10)

### Issues:
| # | File | Issue | Severity |
|---|------|-------|----------|
| 1.1 | AuthPage.tsx | Error messages still use dark-theme red (`bg-red-900`, `text-red-400`) | CRITICAL |
| 1.2 | NumerologyTarot.tsx | Some badge colors still dark-theme remnants | CRITICAL |
| 1.3 | LalKitabPage.tsx | Error state colors not updated | CRITICAL |
| 1.4 | KundliForm.tsx | Validation error colors dark-theme | CRITICAL |
| 1.5 | index.css | CSS variables mix dark and light theme values (`--ink`, `--cosmic-text`, etc.) | MAJOR |
| 1.6 | Multiple files | No consistent design tokens — colors hardcoded everywhere | MAJOR |

### Fix: Global color variable cleanup + remaining dark-theme sweep

---

## AREA 2: MOBILE RESPONSIVENESS (Score: 4/10)

### Issues:
| # | File | Issue | Severity |
|---|------|-------|----------|
| 2.1 | KundliGenerator.tsx:194 | 23 tabs — needs collapsible categories or search/filter | CRITICAL |
| 2.2 | InteractiveKundli.tsx | Diamond chart not fully responsive on <375px | CRITICAL |
| 2.3 | Multiple tables | Tables still need card-based mobile layout (not just horizontal scroll) | MAJOR |
| 2.4 | KundliForm.tsx:174-208 | Place autocomplete dropdown cut off on mobile | MAJOR |
| 2.5 | KundliForm.tsx:214-224 | Phone field appear/disappear causes layout shift | MINOR |
| 2.6 | ConsolidatedReport.tsx:333 | 2 charts side-by-side too small on mobile | MAJOR |

### Fix: Group tabs into categories, card layouts for tables, responsive charts

---

## AREA 3: ACCESSIBILITY (Score: 4/10)

### Issues:
| # | File | Issue | WCAG |
|---|------|-------|------|
| 3.1 | InteractiveKundli.tsx:619-658 | SVG planets have no `aria-label` | 1.1.1 |
| 3.2 | KundliGenerator.tsx:194 | Tabs missing `aria-selected`, `aria-controls` | 4.1.2 |
| 3.3 | Navigation.tsx:86-91 | Mobile menu button no `aria-expanded` | 4.1.2 |
| 3.4 | KundliForm.tsx:163-164 | Gender toggle not marked as `role="radio"` | 4.1.2 |
| 3.5 | All GSAP files | No `prefers-reduced-motion` check | 2.3.3 |
| 3.6 | Multiple | Missing focus-visible states on interactive elements | 2.4.7 |
| 3.7 | Multiple | No keyboard navigation for SVG charts | 2.1.1 |

### Fix: ARIA labels, reduced motion, focus states, keyboard nav

---

## AREA 4: COMPONENT CONSISTENCY (Score: 5/10)

### Issues:
| # | Issue | Severity |
|---|-------|----------|
| 4.1 | Border radius varies: rounded-xl, rounded-2xl, rounded-lg mixed | MAJOR |
| 4.2 | Card styles inconsistent: some `bg-sacred-cream`, some `bg-white`, some `bg-cosmic-card` | MAJOR |
| 4.3 | Button styles vary across pages (size, padding, colors) | MAJOR |
| 4.4 | Badge patterns differ: some rounded-full, some rounded, different sizes | MINOR |
| 4.5 | Section headers not standardized (font size, weight, icon usage varies) | MINOR |

### Fix: Create design tokens, standardize card/button/badge components

---

## AREA 5: ERROR STATES (Score: 5/10)

### Issues:
| # | File | Issue | Severity |
|---|------|-------|----------|
| 5.1 | App.tsx:29 | Global ErrorBoundary shows generic "Something went wrong" | MAJOR |
| 5.2 | Dashboard.tsx | No error handling for API failures | MAJOR |
| 5.3 | KundliGenerator.tsx | Tab data fetch errors silently logged to console | MAJOR |
| 5.4 | Multiple | Network errors show raw error messages to users | MINOR |

### Fix: User-friendly error messages, retry buttons, per-section error handling

---

## AREA 6: NAVIGATION & IA (Score: 6/10)

### Issues:
| # | File | Issue | Severity |
|---|------|-------|----------|
| 6.1 | KundliGenerator.tsx | 23 tabs with no grouping/search — overwhelming | CRITICAL |
| 6.2 | Navigation.tsx:9-14 | Service links only visible when logged in — SEO issue | MAJOR |
| 6.3 | AdminDashboard.tsx:96-103 | Custom tab buttons instead of Tabs component | MINOR |

### Fix: Group kundli tabs into categories (Chart, Analysis, Predictions, Advanced)

---

## AREA 7: VISUAL HIERARCHY (Score: 6/10)

### Issues:
| # | Issue | Severity |
|---|-------|----------|
| 7.1 | Headings not differentiated enough from body text | MAJOR |
| 7.2 | Too many elements competing for attention on kundli page | MAJOR |
| 7.3 | Key data (degrees, nakshatras) same visual weight as labels | MINOR |

### Fix: Stronger heading styles, better information density management

---

## AREA 8: LOADING STATES (Score: 6/10)

### Issues:
| # | Issue | Severity |
|---|-------|----------|
| 8.1 | No skeleton screens — just spinners | MINOR |
| 8.2 | Panchang page flickers between loading and loaded | MINOR |
| 8.3 | Tab content loads individually — page feels "jumpy" | MINOR |

### Fix: Add skeleton placeholders for major components

---

## AREA 9: EMPTY STATES (Score: 6/10)

### Issues:
| # | File | Issue | Severity |
|---|------|-------|----------|
| 9.1 | AdminDashboard.tsx:106-157 | No empty state for zero data | MINOR |
| 9.2 | YogaDoshaTab.tsx:36-37 | "No yogas" message too subtle | MINOR |
| 9.3 | DashaTab.tsx:145 | "Click tab to load" unclear CTA | MINOR |

### Fix: Better empty state designs with illustrations/icons

---

## AREA 10: FORMS & INPUT (Score: 7/10)

### Issues:
| # | File | Issue | Severity |
|---|------|-------|----------|
| 10.1 | AuthPage.tsx:234-247 | OTP paste has no visual feedback | MINOR |
| 10.2 | Panchang.tsx:187-225 | Date/lat/lon inputs not grouped visually | MINOR |

### Fix: Better form grouping, validation feedback

---

## AREA 11: PERFORMANCE (Score: 6/10)

### Issues:
| # | File | Issue | Severity |
|---|------|-------|----------|
| 11.1 | Hero.tsx:10-20 | GSAP animation on every mount, no reduced motion | MAJOR |
| 11.2 | Panchang.tsx:98-106 | Multiple ScrollTrigger instances | MINOR |
| 11.3 | Three.js components | Heavy 3D loading on homepage | MINOR |

### Fix: Reduced motion, lazy load 3D, optimize animations

---

## PRIORITY MATRIX

### P0 — Fix before launch (150 users)
- [ ] 1.1-1.4: Remaining dark-theme error colors
- [ ] 2.1: Kundli tab grouping (categories)
- [ ] 5.1-5.3: User-friendly error messages

### P1 — Fix first week
- [ ] 2.2: Chart responsiveness on small phones
- [ ] 3.1-3.3: Critical ARIA accessibility
- [ ] 4.1-4.3: Design token standardization
- [ ] 6.2: SEO — show nav links to unauthenticated users

### P2 — Fix first month
- [ ] 2.3: Card-based table layouts on mobile
- [ ] 3.5: Reduced motion support
- [ ] 5.4: User-friendly error messages
- [ ] 7.1-7.2: Visual hierarchy improvements
- [ ] 8.1: Skeleton loading screens

### P3 — Backlog
- [ ] 9.1-9.3: Empty state improvements
- [ ] 10.1-10.2: Form UX polish
- [ ] 11.1-11.3: Performance optimizations
- [ ] Chart comparison mode
- [ ] Design system documentation

---

*Source: Real Kimi UI/UX audit, 2026-04-10*
*Score target for launch: 7/10 (B-) — requires P0 + P1 fixes*
