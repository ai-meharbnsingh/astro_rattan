# Mobile Responsive Design Documentation

## Framework and Approach

Astro Rattan uses **Tailwind CSS** with responsive utility classes for mobile-first design. The frontend is built with **React + Vite** and uses **shadcn/ui** components, which are accessible and mobile-responsive by default.

## Responsive Breakpoints (Tailwind Defaults)

| Breakpoint | Min Width | Usage |
|------------|-----------|-------|
| `sm` | 640px | Large phones, landscape |
| `md` | 768px | Tablets |
| `lg` | 1024px | Small laptops |
| `xl` | 1280px | Desktops |
| `2xl` | 1536px | Large screens |

## Mobile Navigation

The navigation component (`frontend/src/sections/Navigation.tsx`) implements a **mobile hamburger menu** using the Sheet pattern:

- **Desktop (lg+):** Horizontal nav bar with inline links and action buttons
- **Mobile (<lg):** Hamburger icon (`Menu`/`X` toggle) that opens a full-screen overlay panel
- The mobile menu includes all navigation links, auth actions (Sign In / Profile), cart, and role-based links (Admin, Astrologer Dashboard)
- Menu closes on link click via `onClick={() => setIsMobileMenuOpen(false)}`
- Overlay uses `backdrop-blur-xl` for a glass-morphism effect

### Mobile Menu Features
- All 7 nav links (Kundli, Horoscope, Panchang, Prashnavali, Numerology, Library, Shop)
- Ask AI Astrologer button (full width)
- Cart and Profile buttons (when authenticated)
- Admin panel link (admin role only)
- Astrologer Dashboard link (astrologer role only)
- Sign In button (when not authenticated)

## Responsive Grid Layouts

All card-based layouts use responsive grid classes:

```
grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3
```

This provides:
- **Mobile:** Single column (full width cards)
- **Tablet:** Two columns
- **Desktop:** Three columns

## Touch Target Compliance

All interactive elements meet the **44px minimum touch target** size:
- Buttons use `size="sm"` or larger (min 36px height with padding)
- Navigation links have `p-3` padding (12px each side = 48px+ touch area)
- Mobile hamburger button has `p-2` padding on a 24px icon (44px+ total)
- Form inputs use default shadcn/ui sizing (40px+ height)

## Scrolled Navigation State

The navigation detects scroll position and transitions to a compact "pill" style:
- **Before scroll (top):** Full width, larger padding (`py-6`)
- **After scroll (>100px):** Compact pill shape with `max-w-4xl`, rounded corners, glass effect, and shadow

## Testing

### Manual Testing
Open browser DevTools and test at these viewport widths:
- 375px (iPhone SE)
- 390px (iPhone 14)
- 768px (iPad)
- 1024px (iPad landscape)
- 1280px (Desktop)

### Automated Testing (Playwright)
When Playwright mobile configuration is added:

```bash
npx playwright test --project=mobile
```

Playwright mobile project config (to be added to `playwright.config.ts`):

```typescript
{
  name: 'mobile',
  use: {
    ...devices['iPhone 14'],
    headless: false,
    slowMo: 500,
  },
}
```

## Key Files

| File | Responsibility |
|------|---------------|
| `frontend/src/sections/Navigation.tsx` | Mobile hamburger menu, scroll state |
| `frontend/tailwind.config.js` | Breakpoint configuration |
| `frontend/src/index.css` | Global responsive styles |
| `frontend/src/components/ui/` | shadcn/ui components (inherently responsive) |
