# Styles Audit Report - Hardcoded Colors & Fonts

## Summary
Found **385** inline style declarations and **228** hardcoded hex colors across the frontend codebase.

---

## Critical Issues Found

### 1. Frontend - Hardcoded Colors in Tailwind Classes (69 instances)

**Files with most violations:**
- `KundliGenerator.tsx` - 25+ instances
- `ConsolidatedReport.tsx` - Multiple instances  
- `KundliSummaryModal.tsx` - Background colors
- `Hero.tsx`, `Features.tsx`, `CTA.tsx` - Brand colors

**Common hardcoded patterns:**
```tsx
// Gold colors
bg-[#d4af37]          // Should use: bg-sacred-gold or var(--aged-gold)
text-[#d4af37]        // Should use: text-sacred-gold
border-[#B8860B]/30   // Should use: border-sacred-gold/30

// Red/Maroon colors  
bg-[#8B2332]/10       // Should use: bg-wax-red/10 or var(--wax-red-deep)
text-[#8B2332]        // Should use: text-wax-red-deep
text-[#ff6b6b]        // Should use: text-red-400

// Background colors
bg-[#1a1a2e]          // Should use: CSS variable
bg-[#FDF8F0]          // Should use: bg-parchment or var(--parchment)
bg-[#0a0a0a]          // Should use: CSS variable
```

### 2. Frontend - Inline Styles (385 instances)

**Common patterns in KundliGenerator.tsx:**
```tsx
// Hardcoded rgba values
style={{ background: 'rgba(184,134,11,0.1)' }}
style={{ background: 'rgba(34,34,58,0.8)' }}
style={{ background: 'rgba(196,62,78,0.08)' }}

// Hardcoded hex colors
style={{ color: '#f87171' }}
style={{ color: '#059669' }}
style={{ color: '#b8b0a4' }}

// Using CSS variables (GOOD - keep these)
style={{ color: 'var(--ink)' }}
style={{ color: 'var(--aged-gold)' }}
style={{ color: 'var(--ink-light)' }}
```

### 3. CSS File Issues (index.css)

**Hardcoded colors that should be variables:**
```css
/* Line 117-118 */
background: #FAFAFA;     /* Should use: var(--parchment) */
color: #1e293b;          /* Should use: var(--ink) */

/* Line 137-139 */
background: rgba(255, 153, 51, 0.2);  /* Should use variable */
color: #1e293b;                       /* Should use variable */

/* Line 149, 155, 156 */
color: #1e293b;          /* var(--ink) */
color: #B45309;          /* var(--aged-gold-dim) */

/* Lines 223-227 - Gradient definitions */
background: linear-gradient(135deg, #FAFAFA 0%, #F8FAFC 50%, #FAFAFA 100%);
background: linear-gradient(135deg, #FFD700 0%, #FF9933 50%, #B45309 100%);

/* Line 253-256 */
background: linear-gradient(90deg, transparent 0%, #B8860B 20%, #D4A052 50%, ...);

/* Lines 286-291 */
border: 2px solid #B8860B;

/* Lines 318, 324, 334 */
color: rgba(139, 69, 19, 0.03);
box-shadow: inset 0 0 60px rgba(139, 69, 19, 0.1);
background: radial-gradient(circle, rgba(139, 69, 19, 0.05) 0%, ...);

/* Lines 348-355 - Scrollbar colors */
background: #f1f5f9;     /* var(--parchment-dark) */
background: #cbd5e1;     /* Should use variable */
background: #94a3b8;     /* var(--text-muted) */
```

### 4. Backend - PDF Generation (app/routes/kundli.py)

**Hardcoded RGB tuples (acceptable for PDFs but could be centralized):**
```python
GOLD = (184, 134, 11)       # #B8860B
GOLD_LIGHT = (245, 235, 210)
ALT_ROW = (252, 248, 240)
GREEN_MARK = (34, 139, 34)
RED_MARK = (178, 34, 34)
```

---

## Recommended Fixes

### 1. Add Missing CSS Variables to index.css

```css
:root {
  /* Missing opacity variants */
  --aged-gold-5: rgba(184, 134, 11, 0.05);
  --aged-gold-10: rgba(184, 134, 11, 0.1);
  --aged-gold-12: rgba(184, 134, 11, 0.12);
  --aged-gold-15: rgba(184, 134, 11, 0.15);
  --aged-gold-20: rgba(184, 134, 11, 0.2);
  --aged-gold-30: rgba(184, 134, 11, 0.3);
  
  /* Dark theme backgrounds */
  --dark-bg: #1a1a2e;
  --dark-bg-secondary: #16213e;
  --dark-card: rgba(34, 34, 58, 0.8);
  
  /* Semantic colors */
  --success: #059669;
  --success-light: #34d399;
  --error: #dc2626;
  --error-light: #f87171;
  --warning: #f59e0b;
  --warning-light: #fbbf24;
  
  /* Text colors */
  --text-cream: #e8e0d4;
  --text-warm: #b8b0a4;
}
```

### 2. Create Utility Classes for Common Patterns

```css
/* Background opacity utilities */
.bg-gold-5 { background-color: var(--aged-gold-5); }
.bg-gold-10 { background-color: var(--aged-gold-10); }
.bg-gold-20 { background-color: var(--aged-gold-20); }

/* Dark theme cards */
.bg-dark-card { background-color: var(--dark-card); }
.bg-dark-bg { background-color: var(--dark-bg); }

/* Semantic colors */
.text-success { color: var(--success); }
.text-error { color: var(--error); }
.bg-error-5 { background-color: rgba(220, 38, 38, 0.05); }
.bg-error-8 { background-color: rgba(196, 62, 78, 0.08); }
```

### 3. Replace Hardcoded Values Priority List

**HIGH PRIORITY:**
1. `KundliGenerator.tsx` - Lines 798, 813, 826 (core UI colors)
2. `index.css` - Body background and text colors (affects entire app)
3. All `text-[#8B2332]` → `text-wax-red-deep`
4. All `bg-[#d4af37]` → `bg-sacred-gold`

**MEDIUM PRIORITY:**
1. Inline rgba backgrounds in KundliGenerator
2. Dark theme colors (`#1a1a2e`, `#16213e`)
3. Status colors (`#059669`, `#f87171`)

**LOW PRIORITY:**
1. Decorative gradients
2. Scrollbar colors
3. PDF generation colors (backend)

---

## Files Requiring Updates

### Frontend
1. `frontend/src/index.css` - Add variables, fix hardcoded values
2. `frontend/src/sections/KundliGenerator.tsx` - Major refactoring needed
3. `frontend/src/components/KundliSummaryModal.tsx`
4. `frontend/src/components/kundli/ConsolidatedReport.tsx`
5. `frontend/src/sections/Hero.tsx`
6. `frontend/src/sections/Features.tsx`
7. `frontend/src/sections/CTA.tsx`
8. `frontend/src/sections/Footer.tsx`
9. `frontend/src/sections/SpiritualLibrary.tsx`

### Backend
1. `app/routes/kundli.py` - Optional: Centralize PDF colors

---

## Quick Wins (Safe to Replace)

### Replace in KundliGenerator.tsx:
```diff
- className="bg-[#d4af37] text-black"
+ className="bg-sacred-gold text-black"

- className="text-[#8B2332]"
+ className="text-wax-red-deep"

- style={{ background: 'rgba(184,134,11,0.1)' }}
+ className="bg-sacred-gold/10"

- style={{ color: '#059669' }}
+ className="text-emerald-600"
```

### Replace in index.css:
```diff
- background: #FAFAFA;
+ background: var(--parchment);

- color: #1e293b;
+ color: var(--ink);
```
