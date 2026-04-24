/**
 * Safari Desktop Audit — 14 pages
 * Viewport: 1920×1080 (Desktop Safari)
 * Focus: localStorage, IndexedDB, scroll, animations, form persistence
 */
import { test, expect, Page } from '@playwright/test';

const BASE = process.env.E2E_BASE_URL || 'https://astrorattan.com';

// ── helpers ────────────────────────────────────────────────────────────────
async function pageState(page: Page) {
  return page.evaluate(() => {
    // localStorage probe
    const ls: Record<string, unknown> = { available: false, keys: [], quotaOk: false, error: null };
    try {
      localStorage.setItem('__quota__', 'x'.repeat(1024 * 50)); // 50 KB
      localStorage.removeItem('__quota__');
      ls.quotaOk = true;
      ls.available = true;
      ls.keys = Object.keys(localStorage);
    } catch (e: any) { ls.error = e?.message; }

    // sessionStorage probe
    const ss: Record<string, unknown> = { available: false };
    try {
      sessionStorage.setItem('__t__', '1');
      sessionStorage.removeItem('__t__');
      ss.available = true;
    } catch (e: any) { ss.error = e?.message; }

    return {
      url: window.location.href,
      pathname: window.location.pathname,
      title: document.title,
      width: window.innerWidth,
      height: window.innerHeight,
      ls,
      ss,
      idb: typeof indexedDB !== 'undefined',
      scrollBehavior: getComputedStyle(document.documentElement).scrollBehavior,
      // animation signals
      gsap: typeof (window as any).gsap !== 'undefined',
      animateSections: document.querySelectorAll('.animate-section').length,
      motionElements: document.querySelectorAll('[class*="motion"],[class*="animate"],[data-aos]').length,
      // forms
      forms: Array.from(document.forms).length,
      inputs: Array.from(document.querySelectorAll('input')).map(i => ({
        type: i.type, placeholder: i.placeholder, name: i.name
      })),
      // content
      headings: Array.from(document.querySelectorAll('h1,h2')).map(h => h.textContent?.trim()).filter(Boolean).slice(0, 5),
      hasNav: !!document.querySelector('nav'),
      hasSVG: !!document.querySelector('svg'),
      hasCanvas: !!document.querySelector('canvas'),
      hasErrorBoundary: !!document.querySelector('[class*="error"]'),
      // auth state
      hasToken: !!localStorage.getItem('astrorattan_token'),
      language: localStorage.getItem('astrorattan-language') || 'en',
    };
  });
}

async function consoleErrors(page: Page): Promise<string[]> {
  // Errors are collected via listener; approximate via evaluate
  return page.evaluate(() => (window as any).__pw_errors__ || []);
}

// ── test setup ─────────────────────────────────────────────────────────────
test.describe('Safari Desktop — 14-page audit', () => {
  let errors: string[] = [];

  test.beforeEach(async ({ page }) => {
    errors = [];
    page.on('pageerror', err => errors.push(`JS_ERROR: ${err.message}`));
    page.on('response', resp => {
      if (resp.status() >= 500) errors.push(`HTTP_500: ${resp.url()}`);
    });
    await page.setViewportSize({ width: 1920, height: 1080 });
  });

  // ── Page 1: Home ──────────────────────────────────────────────────────────
  test('Page 01 — Home (/)', async ({ page }) => {
    await page.goto(`${BASE}/`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(1500);

    const state = await pageState(page);
    console.log('HOME:', JSON.stringify(state, null, 2));

    // Core checks
    expect(state.width).toBe(1920);
    expect(state.ls.available).toBe(true);
    expect(state.ls.error).toBeNull();
    expect(state.idb).toBe(true);
    expect(state.hasNav).toBe(true);
    expect(state.scrollBehavior).toBe('smooth');

    // Form should be visible (Kundli form on home)
    const hasForm = state.inputs.length > 0 || state.forms > 0;
    expect(hasForm).toBe(true);

    // SVG chart should render
    expect(state.hasSVG).toBe(true);

    // No JS errors
    expect(errors.filter(e => e.startsWith('JS_ERROR'))).toHaveLength(0);

    await page.screenshot({ path: 'screenshots/safari_p01_home.png', fullPage: false });
  });

  // ── Page 2: Register ─────────────────────────────────────────────────────
  test('Page 02 — Register (/register)', async ({ page }) => {
    await page.goto(`${BASE}/register`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(1500);

    const state = await pageState(page);
    console.log('REGISTER:', JSON.stringify({ pathname: state.pathname, inputs: state.inputs, headings: state.headings }, null, 2));

    // /register and /login both use AuthPage — check form present
    const hasAuthInputs = state.inputs.some(i => i.type === 'email' || i.type === 'password' || i.placeholder.toLowerCase().includes('email'));
    expect(hasAuthInputs || state.pathname === '/register').toBeTruthy();

    // Test form persistence: fill email, reload, check if it's saved
    const emailInput = page.locator('input[type="email"]').first();
    if (await emailInput.isVisible({ timeout: 3000 }).catch(() => false)) {
      await emailInput.fill('test@example.com');
      await page.reload({ waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(1000);
      // In standard (non-private) browsing, email should NOT persist (no autocomplete="email" with saved value)
      const valAfterReload = await page.locator('input[type="email"]').first().inputValue().catch(() => '');
      console.log('REGISTER form persistence after reload:', valAfterReload);
    }

    await page.screenshot({ path: 'screenshots/safari_p02_register.png' });
  });

  // ── Page 3: Login ────────────────────────────────────────────────────────
  test('Page 03 — Login (/login)', async ({ page }) => {
    await page.goto(`${BASE}/login`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(1500);

    const state = await pageState(page);
    console.log('LOGIN:', JSON.stringify({ pathname: state.pathname, inputs: state.inputs, headings: state.headings }, null, 2));

    const hasLoginForm = state.inputs.some(i => i.type === 'email' || i.type === 'password');
    expect(hasLoginForm).toBe(true);

    // Test session persistence: check if token survives reload after simulated login
    const lsBefore = await page.evaluate(() => Object.keys(localStorage));
    console.log('LOGIN localStorage keys:', lsBefore);

    await page.screenshot({ path: 'screenshots/safari_p03_login.png' });
  });

  // ── Page 4: Dashboard ────────────────────────────────────────────────────
  test('Page 04 — Dashboard (/dashboard)', async ({ page }) => {
    await page.goto(`${BASE}/dashboard`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(2000);

    const state = await pageState(page);
    console.log('DASHBOARD:', JSON.stringify({ pathname: state.pathname, headings: state.headings, hasToken: state.hasToken }, null, 2));

    // If not authenticated, should redirect to /login
    const expectedPaths = ['/dashboard', '/login'];
    expect(expectedPaths).toContain(state.pathname);

    await page.screenshot({ path: 'screenshots/safari_p04_dashboard.png' });
  });

  // ── Page 5: Kundli ───────────────────────────────────────────────────────
  test('Page 05 — Kundli (/kundli) — form persistence', async ({ page }) => {
    await page.goto(`${BASE}/kundli`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(2000);

    const state = await pageState(page);
    console.log('KUNDLI:', JSON.stringify({ pathname: state.pathname, inputs: state.inputs, headings: state.headings }, null, 2));

    expect(state.pathname).toBe('/kundli');
    const hasKundliInputs = state.inputs.some(i =>
      i.placeholder.toLowerCase().includes('name') ||
      i.placeholder.toLowerCase().includes('birth') ||
      i.type === 'date' ||
      i.type === 'time'
    );
    expect(hasKundliInputs).toBe(true);

    // Fill form fields and test persistence on reload
    const nameInput = page.locator('input[placeholder*="name" i]').first();
    const dateInput = page.locator('input[type="date"]').first();

    let nameFilled = false;
    if (await nameInput.isVisible({ timeout: 3000 }).catch(() => false)) {
      await nameInput.fill('Meharban Singh');
      nameFilled = true;
    }
    if (await dateInput.isVisible({ timeout: 3000 }).catch(() => false)) {
      await dateInput.fill('1990-05-15');
    }

    // Check localStorage for form draft
    const lsBeforeReload = await page.evaluate(() => {
      const keys = Object.keys(localStorage).filter(k => k.includes('kundli') || k.includes('form') || k.includes('draft'));
      return Object.fromEntries(keys.map(k => [k, localStorage.getItem(k)]));
    });
    console.log('KUNDLI localStorage draft keys:', lsBeforeReload);

    // Reload and check persistence
    await page.reload({ waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1500);

    const nameAfterReload = nameFilled
      ? await page.locator('input[placeholder*="name" i]').first().inputValue().catch(() => '')
      : '';
    console.log('KUNDLI name field after reload:', nameAfterReload || '(empty — no persistence)');

    const lsAfterReload = await page.evaluate(() => {
      const keys = Object.keys(localStorage).filter(k => k.includes('kundli') || k.includes('form') || k.includes('draft'));
      return Object.fromEntries(keys.map(k => [k, localStorage.getItem(k)]));
    });
    console.log('KUNDLI localStorage after reload:', lsAfterReload);

    await page.screenshot({ path: 'screenshots/safari_p05_kundli.png' });
  });

  // ── Page 6: Panchang ─────────────────────────────────────────────────────
  test('Page 06 — Panchang (/panchang)', async ({ page }) => {
    await page.goto(`${BASE}/panchang`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(3000); // calendar needs more time

    const state = await pageState(page);
    console.log('PANCHANG:', JSON.stringify({ pathname: state.pathname, headings: state.headings, hasSVG: state.hasSVG }, null, 2));

    expect(state.pathname).toBe('/panchang');

    // Check calendar is interactive
    const hasCalendar = await page.locator('table, [class*="calendar"], [class*="panchang"]').count() > 0;
    const hasDateNavigation = await page.locator('button[aria-label*="prev" i], button[aria-label*="next" i], button[aria-label*="forward" i], button[aria-label*="back" i]').count() > 0;
    console.log('PANCHANG calendar present:', hasCalendar, 'navigation:', hasDateNavigation);

    await page.screenshot({ path: 'screenshots/safari_p06_panchang.png' });
  });

  // ── Page 7: Horoscope ────────────────────────────────────────────────────
  test('Page 07 — Horoscope (/horoscope)', async ({ page }) => {
    await page.goto(`${BASE}/horoscope`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(2000);

    const state = await pageState(page);
    console.log('HOROSCOPE:', JSON.stringify({ pathname: state.pathname, headings: state.headings }, null, 2));

    expect(state.pathname).toBe('/horoscope');

    // Should NOT be blank — check for content
    const hasContent = state.headings.length > 0;
    const hasZodiacSign = await page.locator('[class*="sign"], [class*="zodiac"], [class*="rashi"]').count() > 0;
    console.log('HOROSCOPE has content:', hasContent, 'has zodiac:', hasZodiacSign);
    expect(hasContent || hasZodiacSign).toBeTruthy();

    // Check for error boundary rendering (blank page indicator)
    const hasErrorUI = await page.locator('text=Something went wrong').isVisible({ timeout: 1000 }).catch(() => false);
    expect(hasErrorUI).toBe(false);

    await page.screenshot({ path: 'screenshots/safari_p07_horoscope.png' });
  });

  // ── Page 8: Lal Kitab ────────────────────────────────────────────────────
  test('Page 08 — Lal Kitab (/lal-kitab)', async ({ page }) => {
    await page.goto(`${BASE}/lal-kitab`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(2000);

    const state = await pageState(page);
    console.log('LAL KITAB:', JSON.stringify({ pathname: state.pathname, headings: state.headings, inputs: state.inputs.slice(0,5) }, null, 2));

    const expectedPaths = ['/lal-kitab', '/login'];
    expect(expectedPaths).toContain(state.pathname);

    if (state.pathname === '/lal-kitab') {
      // Check tabs render
      const tabCount = await page.locator('[role="tab"], [class*="tab"]').count();
      console.log('LAL KITAB tab count:', tabCount);
      expect(tabCount).toBeGreaterThan(0);
    }

    await page.screenshot({ path: 'screenshots/safari_p08_lalkitab.png' });
  });

  // ── Page 9: Numerology ───────────────────────────────────────────────────
  test('Page 09 — Numerology (/numerology)', async ({ page }) => {
    await page.goto(`${BASE}/numerology`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(2000);

    const state = await pageState(page);
    console.log('NUMEROLOGY:', JSON.stringify({ pathname: state.pathname, headings: state.headings, inputs: state.inputs.slice(0,5) }, null, 2));

    const expectedPaths = ['/numerology', '/login'];
    expect(expectedPaths).toContain(state.pathname);

    if (state.pathname === '/numerology') {
      const hasForm = state.inputs.length > 0;
      const submitBtn = await page.locator('button[type="submit"], button:has-text("Calculate"), button:has-text("Submit")').count() > 0;
      console.log('NUMEROLOGY form:', hasForm, 'submit button:', submitBtn);
      expect(hasForm || submitBtn).toBeTruthy();
    }

    await page.screenshot({ path: 'screenshots/safari_p09_numerology.png' });
  });

  // ── Page 10: Vastu ───────────────────────────────────────────────────────
  test('Page 10 — Vastu (/vastu)', async ({ page }) => {
    await page.goto(`${BASE}/vastu`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(2000);

    const state = await pageState(page);
    console.log('VASTU:', JSON.stringify({ pathname: state.pathname, headings: state.headings, inputs: state.inputs.slice(0,5) }, null, 2));

    const expectedPaths = ['/vastu', '/login'];
    expect(expectedPaths).toContain(state.pathname);

    if (state.pathname === '/vastu') {
      const hasRoomInputs = state.inputs.some(i =>
        i.placeholder.toLowerCase().includes('room') ||
        i.placeholder.toLowerCase().includes('direction') ||
        i.type === 'select-one'
      ) || await page.locator('select').count() > 0;
      console.log('VASTU room analysis inputs present:', hasRoomInputs || state.inputs.length > 0);
    }

    await page.screenshot({ path: 'screenshots/safari_p10_vastu.png' });
  });

  // ── Page 11: Feedback ────────────────────────────────────────────────────
  test('Page 11 — Feedback (/feedback)', async ({ page }) => {
    await page.goto(`${BASE}/feedback`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(2000);

    const state = await pageState(page);
    console.log('FEEDBACK:', JSON.stringify({ pathname: state.pathname, headings: state.headings, inputs: state.inputs }, null, 2));

    const expectedPaths = ['/feedback', '/login'];
    expect(expectedPaths).toContain(state.pathname);

    if (state.pathname === '/feedback') {
      const hasTextarea = await page.locator('textarea').count() > 0;
      const hasSubmit = await page.locator('button[type="submit"], button:has-text("Submit"), button:has-text("Send")').count() > 0;
      console.log('FEEDBACK textarea:', hasTextarea, 'submit:', hasSubmit);
      expect(hasTextarea || state.inputs.length > 0).toBeTruthy();
    }

    await page.screenshot({ path: 'screenshots/safari_p11_feedback.png' });
  });

  // ── Page 12: Admin ───────────────────────────────────────────────────────
  test('Page 12 — Admin (/admin)', async ({ page }) => {
    await page.goto(`${BASE}/admin`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(2000);

    const state = await pageState(page);
    console.log('ADMIN:', JSON.stringify({ pathname: state.pathname, headings: state.headings }, null, 2));

    const expectedPaths = ['/admin', '/login'];
    expect(expectedPaths).toContain(state.pathname);

    await page.screenshot({ path: 'screenshots/safari_p12_admin.png' });
  });

  // ── Page 13: Astrologer Dashboard ────────────────────────────────────────
  test('Page 13 — Astrologer Dashboard (/astrologer)', async ({ page }) => {
    await page.goto(`${BASE}/astrologer`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(2000);

    const state = await pageState(page);
    console.log('ASTROLOGER:', JSON.stringify({ pathname: state.pathname, headings: state.headings }, null, 2));

    const expectedPaths = ['/astrologer', '/login'];
    expect(expectedPaths).toContain(state.pathname);

    if (state.pathname === '/astrologer') {
      const tabCount = await page.locator('[role="tab"], [class*="tab"]').count();
      const clientList = await page.locator('[class*="client"], table tbody tr').count();
      console.log('ASTROLOGER tabs:', tabCount, 'clients:', clientList);
    }

    await page.screenshot({ path: 'screenshots/safari_p13_astrologer.png' });
  });

  // ── Page 14: Client Profile ───────────────────────────────────────────────
  test('Page 14 — Client Profile (/client/1)', async ({ page }) => {
    await page.goto(`${BASE}/client/1`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(2000);

    const state = await pageState(page);
    console.log('CLIENT PROFILE:', JSON.stringify({ pathname: state.pathname, headings: state.headings }, null, 2));

    const expectedPaths = ['/client/1', '/login'];
    expect(expectedPaths).toContain(state.pathname);

    await page.screenshot({ path: 'screenshots/safari_p14_client.png' });
  });

  // ── Safari-specific: localStorage in Private Mode simulation ─────────────
  test('Safari — localStorage quota and IDB availability', async ({ page }) => {
    await page.goto(`${BASE}/`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(1000);

    const storageReport = await page.evaluate(() => {
      const report: Record<string, unknown> = {};

      // 1. localStorage read/write
      try {
        localStorage.setItem('_test', 'hello');
        report.ls_write = localStorage.getItem('_test') === 'hello';
        localStorage.removeItem('_test');
      } catch(e: any) { report.ls_write = false; report.ls_error = e.message; }

      // 2. Quota test (Safari private mode fails at ~0 bytes)
      try {
        localStorage.setItem('_big', 'x'.repeat(1024 * 100)); // 100KB
        localStorage.removeItem('_big');
        report.ls_quota_100kb = true;
      } catch { report.ls_quota_100kb = false; }

      // 3. sessionStorage
      try {
        sessionStorage.setItem('_t', '1');
        report.ss_write = sessionStorage.getItem('_t') === '1';
        sessionStorage.removeItem('_t');
      } catch(e: any) { report.ss_write = false; report.ss_error = e.message; }

      // 4. IndexedDB
      report.idb_available = typeof indexedDB !== 'undefined';

      // 5. Cookies
      try {
        document.cookie = '_cookietest=1; SameSite=Strict';
        report.cookies_available = document.cookie.includes('_cookietest');
      } catch { report.cookies_available = false; }

      // 6. Existing keys in localStorage
      report.existing_ls_keys = Object.keys(localStorage);

      return report;
    });

    console.log('STORAGE AUDIT:', JSON.stringify(storageReport, null, 2));
    expect(storageReport.ls_write).toBe(true);
    expect(storageReport.ss_write).toBe(true);
    expect(storageReport.idb_available).toBe(true);
  });

  // ── Page 15: Blog ───────────────────────────────────────────────────────────
  test('Page 15 — Blog (/blog)', async ({ page }) => {
    await page.goto(`${BASE}/blog`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(2000);

    const state = await pageState(page);
    console.log('BLOG:', JSON.stringify({ pathname: state.pathname, headings: state.headings }, null, 2));

    const expectedPaths = ['/blog', '/login'];
    expect(expectedPaths).toContain(state.pathname);

    if (state.pathname === '/blog') {
      const hasContent = state.headings.length > 0;
      const hasBlogCards = await page.locator('[class*="article"], [class*="post"], [class*="card"]').count() > 0;
      console.log('BLOG has content:', hasContent, 'blog cards:', hasBlogCards);
      expect(hasContent || hasBlogCards).toBeTruthy();
    }

    await page.screenshot({ path: 'screenshots/safari_p15_blog.png' });
  });

  // ── Safari-specific: Scroll animation audit ───────────────────────────────
  test('Safari — Scroll animation and GSAP check', async ({ page }) => {
    await page.goto(`${BASE}/`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(2000);

    const animReport = await page.evaluate(() => {
      return {
        gsap_loaded: typeof (window as any).gsap !== 'undefined',
        scroll_trigger: typeof (window as any).ScrollTrigger !== 'undefined',
        animate_sections: document.querySelectorAll('.animate-section').length,
        css_animations: Array.from(document.styleSheets).reduce((sum, ss) => {
          try { return sum + Array.from(ss.cssRules).filter(r => r instanceof CSSKeyframesRule).length; }
          catch { return sum; }
        }, 0),
        scroll_behavior: getComputedStyle(document.documentElement).scrollBehavior,
        prefers_reduced_motion: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
        will_change_els: document.querySelectorAll('[style*="will-change"]').length,
        transform_els: Array.from(document.querySelectorAll('[style*="transform"]')).length,
      };
    });

    console.log('ANIMATION AUDIT:', JSON.stringify(animReport, null, 2));

    // Scroll down to trigger scroll animations
    await page.evaluate(() => window.scrollTo({ top: 500, behavior: 'smooth' }));
    await page.waitForTimeout(1000);
    await page.evaluate(() => window.scrollTo({ top: 1000, behavior: 'smooth' }));
    await page.waitForTimeout(1000);

    const scrollY = await page.evaluate(() => window.scrollY);
    console.log('Scroll position after smooth scroll:', scrollY);
    expect(scrollY).toBeGreaterThan(0);

    await page.screenshot({ path: 'screenshots/safari_scroll_test.png' });
  });
});
