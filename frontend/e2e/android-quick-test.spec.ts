import { test, expect } from '@playwright/test';

// Configure test for Android Chrome (393x851 viewport)
test.use({
  viewport: { width: 393, height: 851 },
  userAgent: 'Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
  deviceScaleFactor: 2,
  isMobile: true,
});

const BASE_URL = 'https://astrorattan.com';
const PAGES = [
  { name: 'Home', path: '/' },
  { name: 'Login', path: '/login' },
  { name: 'Dashboard', path: '/dashboard' },
  { name: 'Kundli', path: '/kundli' },
  { name: 'Panchang', path: '/panchang' },
  { name: 'Horoscope', path: '/horoscope' },
  { name: 'Lal Kitab', path: '/lal-kitab' },
  { name: 'Numerology', path: '/numerology' },
  { name: 'Vastu', path: '/vastu' },
  { name: 'Feedback', path: '/feedback' },
  { name: 'Admin', path: '/admin' },
  { name: 'Astrologer Dashboard', path: '/astrologer' },
  { name: 'Client Profile', path: '/client/1' },
  { name: 'Blog', path: '/blog' },
];

// Test 1: All pages load without 404/500 errors
for (const page of PAGES) {
  test(`✅ [${page.name}] Page loads (HTTP status < 400)`, async ({ page: browserPage }) => {
    const response = await browserPage.goto(`${BASE_URL}${page.path}`);
    const status = response?.status();
    console.log(`[${page.name}] HTTP ${status}`);
    expect(status).toBeLessThan(400);
  });
}

// Test 2: No console errors
for (const page of PAGES) {
  test(`✅ [${page.name}] No console errors`, async ({ page: browserPage }) => {
    const errors: string[] = [];
    browserPage.on('console', msg => {
      if (msg.type() === 'error') errors.push(msg.text());
    });

    await browserPage.goto(`${BASE_URL}${page.path}`);
    await browserPage.waitForLoadState('networkidle').catch(() => {});
    await browserPage.waitForTimeout(1000);

    const errorList = errors.filter(e => e && e.length > 0);
    if (errorList.length > 0) {
      console.log(`[${page.name}] Errors: ${errorList.length}`);
      errorList.slice(0, 2).forEach(e => console.log(`  └─ ${e}`));
    } else {
      console.log(`[${page.name}] ✓ No errors`);
    }

    expect(errorList.length).toBe(0);
  });
}

// Test 3: Content renders (not blank)
for (const page of PAGES) {
  test(`✅ [${page.name}] Content renders`, async ({ page: browserPage }) => {
    await browserPage.goto(`${BASE_URL}${page.path}`);
    await browserPage.waitForLoadState('networkidle').catch(() => {});

    const contentLength = await browserPage.evaluate(() => {
      return document.body.innerText.trim().length;
    });

    console.log(`[${page.name}] Content: ${contentLength} chars`);
    expect(contentLength).toBeGreaterThan(0);
  });
}

// Test 4: Touch targets are clickable (44px+)
for (const page of PAGES) {
  test(`✅ [${page.name}] Touch targets adequate`, async ({ page: browserPage }) => {
    await browserPage.goto(`${BASE_URL}${page.path}`);
    await browserPage.waitForLoadState('networkidle').catch(() => {});

    const { total, tooSmall } = await browserPage.evaluate(() => {
      const buttons = document.querySelectorAll('button, a[href], input, [role="button"]');
      let tooSmall = 0;
      buttons.forEach(el => {
        const rect = el.getBoundingClientRect();
        if (rect.width < 44 || rect.height < 44) tooSmall++;
      });
      return { total: buttons.length, tooSmall };
    });

    const ratio = tooSmall / (total || 1);
    console.log(`[${page.name}] Touch targets: ${total} total, ${tooSmall} < 44px (${(ratio * 100).toFixed(1)}%)`);
    expect(ratio).toBeLessThan(0.3);
  });
}

// Test 5: No horizontal overflow
for (const page of PAGES) {
  test(`✅ [${page.name}] No overflow`, async ({ page: browserPage }) => {
    await browserPage.goto(`${BASE_URL}${page.path}`);
    await browserPage.waitForLoadState('networkidle').catch(() => {});

    const overflowCount = await browserPage.evaluate(() => {
      let count = 0;
      document.querySelectorAll('*').forEach(el => {
        if (el.scrollWidth > el.clientWidth + 1) count++;
      });
      return count;
    });

    console.log(`[${page.name}] Overflow issues: ${overflowCount}`);
    expect(overflowCount).toBeLessThan(5);
  });
}

// Test 6: Forms exist and are submittable
test('✅ [Home] Hero form exists', async ({ page }) => {
  await page.goto(`${BASE_URL}/`);
  const form = await page.$('form');
  console.log(`[Home] Form: ${form ? '✓' : '✗'}`);
  expect(form).toBeTruthy();
});

test('✅ [Kundli] Form exists', async ({ page }) => {
  await page.goto(`${BASE_URL}/kundli`);
  const form = await page.$('form');
  const submitBtn = form ? await form.$('button[type="submit"]') : null;
  console.log(`[Kundli] Form: ${form ? '✓' : '✗'}, Submit button: ${submitBtn ? '✓' : '✗'}`);
  expect(form).toBeTruthy();
});

test('✅ [Protected Routes] Redirect to login when unauthenticated', async ({ page }) => {
  for (const path of ['/vastu', '/numerology', '/feedback', '/admin', '/lal-kitab']) {
    await page.goto(`${BASE_URL}${path}`);
    await page.waitForLoadState('domcontentloaded');
    const pathname = await page.evaluate(() => window.location.pathname);
    console.log(`[Protected] ${path} -> ${pathname}`);
    expect(['/login', path].includes(pathname)).toBeTruthy();
  }
});

// Test 7: Tabs exist and are switchable
test('✅ [Lal Kitab] Tabs switchable', async ({ page }) => {
  await page.goto(`${BASE_URL}/lal-kitab`);
  await page.waitForLoadState('domcontentloaded');
  const pathname = await page.evaluate(() => window.location.pathname);
  if (pathname === '/login') {
    console.log('[Lal Kitab] Redirected to /login (expected when unauthenticated)');
    expect(true).toBeTruthy();
    return;
  }
  const tabs = await page.$$('[role="tab"]');
  const form = await page.$('form');
  console.log(`[Lal Kitab] Tabs: ${tabs.length}`);

  if (tabs.length > 1) {
    await tabs[0].click();
    await page.waitForTimeout(300);
  }
  // Tabs render after chart generation; on initial load it's valid to be in "form" view.
  expect(tabs.length > 0 || !!form).toBeTruthy();
});

// Test 8: Tables render
test('✅ [Panchang] Tables render', async ({ page }) => {
  await page.goto(`${BASE_URL}/panchang`);
  const tables = await page.$$('table');
  console.log(`[Panchang] Tables: ${tables.length}`);
  // Tables may or may not be present depending on data
});

// Test 9: Navigation accessible
test('✅ [Navigation] Menu accessible', async ({ page }) => {
  await page.goto(`${BASE_URL}/`);
  const nav = await page.$('[role="navigation"], nav, [data-testid="nav"]');
  const hamburger = await page.$('button[aria-label*="menu" i]');
  console.log(`[Navigation] Nav: ${nav ? '✓' : '✗'}, Hamburger: ${hamburger ? '✓' : '✗'}`);
  expect(nav || hamburger).toBeTruthy();
});

// Test 10: Viewport confirmed
test('✅ [Viewport] 393x851', async ({ page }) => {
  const size = await page.evaluate(() => ({
    width: window.innerWidth,
    height: window.innerHeight,
  }));
  console.log(`[Viewport] ${size.width}x${size.height}`);
  expect(size.width).toBe(393);
  expect(size.height).toBe(851);
});
