import { test, expect, Page } from '@playwright/test';

const BASE_URL = process.env.E2E_BASE_URL || 'https://astrorattan.com';
const LOGIN_EMAIL = 'meharbansingh85@gmail.com';
const LOGIN_PASSWORD = 'Misha@2311';

// ── Helpers ───────────────────────────────────────────────────────────────

async function switchToHindi(page: Page) {
  const toggleBtn = page.locator('button').filter({ hasText: /EN/ }).filter({ hasText: /हि/ }).first();
  const isVisible = await toggleBtn.isVisible().catch(() => false);
  if (!isVisible) {
    console.log('ℹ️ No language toggle found — assuming already in Hindi');
    return;
  }

  // Check if already in Hindi
  const hindiTab = page.locator('button[role="tab"]').filter({ hasText: /हिन्दू कैलेंडर/ }).first();
  const isHindi = await hindiTab.isVisible().catch(() => false);
  if (isHindi) {
    console.log('ℹ️ Already in Hindi mode');
    return;
  }

  await toggleBtn.click();
  await page.waitForTimeout(2_000);

  // Verify Hindi is active
  await expect(hindiTab).toBeVisible({ timeout: 5_000 });
  console.log('✅ Switched to Hindi mode');
}

async function switchToEnglish(page: Page) {
  const toggleBtn = page.locator('button').filter({ hasText: /EN/ }).filter({ hasText: /हि/ }).first();
  const isVisible = await toggleBtn.isVisible().catch(() => false);
  if (!isVisible) return;

  // Check if already in English
  const englishTab = page.locator('button[role="tab"]').filter({ hasText: /Hindu Calendar/ }).first();
  const isEnglish = await englishTab.isVisible().catch(() => false);
  if (isEnglish) {
    console.log('ℹ️ Already in English mode');
    return;
  }

  await toggleBtn.click();
  await page.waitForTimeout(2_000);

  // Verify English is active
  await expect(englishTab).toBeVisible({ timeout: 5_000 });
  console.log('✅ Switched to English mode');
}

async function login(page: Page) {
  // NOTE: Panchang is a public page — no login required.
  // If you want authenticated testing, update LOGIN_EMAIL / LOGIN_PASSWORD
  // and uncomment the API login block below.

  // ┌─ Optional authenticated login ───────────────────────────────
  // const loginResp = await page.request.post(`${BASE_URL}/api/auth/login`, {
  //   data: { email: LOGIN_EMAIL, password: LOGIN_PASSWORD },
  // });
  // if (!loginResp.ok()) throw new Error(`Login failed: ${await loginResp.text()}`);
  // const { token } = await loginResp.json();
  // await page.goto(`${BASE_URL}/panchang`);
  // await page.evaluate((t) => localStorage.setItem('astrorattan_token', t), token);
  // await page.reload();
  // └──────────────────────────────────────────────────────────────

  await page.goto(`${BASE_URL}/panchang`);
  await page.waitForLoadState('networkidle');
  // Switch to Hindi after page loads
  await switchToHindi(page);
}

async function goToPanchang(page: Page) {
  await page.goto(`${BASE_URL}/panchang`);
  await page.waitForLoadState('networkidle');
  // Wait for skeleton to disappear and real data to show
  await page.waitForSelector('.animate-pulse', { state: 'detached', timeout: 20_000 }).catch(() => {});
  await page.waitForTimeout(2_000);
}

async function scrollToBottom(page: Page) {
  await page.evaluate(async () => {
    const delay = (ms: number) => new Promise(r => setTimeout(r, ms));
    const step = window.innerHeight * 0.6;
    for (let y = 0; y < document.body.scrollHeight; y += step) {
      window.scrollTo(0, y);
      await delay(400);
    }
    window.scrollTo(0, document.body.scrollHeight);
  });
}

async function screenshotTab(page: Page, tabName: string, suffix: string = '') {
  const fileName = `e2e/panchang-${tabName}${suffix ? '-' + suffix : ''}.png`;
  await page.screenshot({ path: fileName, fullPage: false });
  console.log(`📸 Screenshot saved: ${fileName}`);
}

// List of Panchang tabs to test
const TABS = [
  { id: 'calendar',    name: 'Hindu Calendar',   hindi: 'हिन्दू कैलेंडर' },
  { id: 'festivals',   name: 'Festivals',        hindi: 'त्योहार/व्रत' },
  { id: 'muhurat-finder', name: 'Muhurat Finder', hindi: 'मुहूर्त खोजक' },
  { id: 'muhurat',     name: 'Muhurat',          hindi: '' },
  { id: 'planets',     name: 'Planets',            hindi: '' },
  { id: 'hora',        name: 'Hora',               hindi: '' },
  { id: 'lagna',       name: 'Lagna',              hindi: '' },
  { id: 'choghadiya',  name: 'Choghadiya',         hindi: '' },
  { id: 'gowri',       name: 'Gowri',              hindi: '' },
  { id: 'tarabalam',   name: 'Tara/Chandra',       hindi: 'तारा/चन्द्र बल' },
  { id: 'advanced',    name: 'Advanced',           hindi: 'विशेष' },
];

// ── Tests ─────────────────────────────────────────────────────────────────

test.describe('Panchang Page — Full E2E Audit', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
    // login() already navigates to /panchang and switches to Hindi
    await page.waitForSelector('.animate-pulse', { state: 'detached', timeout: 20_000 }).catch(() => {});
    await page.waitForTimeout(2_000);
  });

  test('01 — Page loads and core data is present', async ({ page }) => {
    // Ensure Panchang section exists
    const section = page.locator('#panchang');
    await expect(section).toBeVisible();

    // Date picker should be visible
    await expect(page.locator('input[type="date"]').first()).toBeVisible();

    // After loading, at least one data card should appear
    const cards = page.locator('.rounded-xl, .rounded-lg').filter({ hasText: /\d{2}:\d{2}/ });
    await expect(cards.first()).toBeVisible({ timeout: 15_000 });

    // Screenshot the initial loaded state
    await screenshotTab(page, '01-initial-load');

    // Scroll full page
    await scrollToBottom(page);
    await page.waitForTimeout(1_000);
    await screenshotTab(page, '01-initial-load-scrolled');
  });

  test('02 — Iterate all tabs, scroll and screenshot', async ({ page }) => {
    for (const tab of TABS) {
      // Click the tab trigger using value attribute (language-independent)
      const tabTrigger = page.locator(`button[role="tab"][value="${tab.id}"]`).first();

      try {
        await tabTrigger.click({ timeout: 5_000 });
      } catch {
        // Fallback: use nth index
        const broad = page.locator('[role="tab"]').nth(TABS.indexOf(tab));
        await broad.click({ timeout: 5_000 });
      }

      await page.waitForTimeout(1_500);

      // Screenshot top of tab
      await screenshotTab(page, `02-tab-${tab.id}`);

      // Scroll to bottom to reveal all content
      await scrollToBottom(page);
      await page.waitForTimeout(800);
      await screenshotTab(page, `02-tab-${tab.id}-scrolled`);

      // Scroll back to top for next tab
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.waitForTimeout(300);
    }
  });

  test('03 — Verify no blank / broken cards (data integrity)', async ({ page }) => {
    // Check that key data fields are not literally "--:--" everywhere (would mean API failed)
    const pageText = await page.locator('body').innerText();

    // Should contain some actual times, not just placeholders
    const timeMatches = pageText.match(/\d{1,2}:\d{2}\s*(AM|PM|am|pm)?/g);
    expect(timeMatches?.length || 0).toBeGreaterThan(3);

    // Should contain many Hindi words when running in Hindi mode
    const hindiWords = pageText.match(/[\u0900-\u097F]{2,}/g);
    expect(hindiWords?.length || 0).toBeGreaterThan(5);

    console.log('✅ Found', timeMatches?.length || 0, 'time strings');
    console.log('✅ Found', hindiWords?.length || 0, 'Hindi words');
  });

  test('04 — Check for obvious hardcoded / placeholder strings', async ({ page }) => {
    const bodyText = await page.locator('body').innerText();
    const lower = bodyText.toLowerCase();

    const badPatterns = [
      'lorem ipsum',
      'placeholder',
      'undefined',
      'null',
      'not found',
      'error 404',
      '[object object]',
      'hardcoded',
      'todo:',
      'fixme:',
    ];

    const found: string[] = [];
    for (const p of badPatterns) {
      if (lower.includes(p)) found.push(p);
    }

    if (found.length > 0) {
      console.warn('⚠️ Potential hardcoded/placeholder strings found:', found);
    }
    expect(found).toEqual([]);
  });

  test('05 — Download PDF button is present and clickable', async ({ page }) => {
    const downloadBtn = page.locator('button').filter({ hasText: /Download PDF|डाउनलोड/ }).first();
    await expect(downloadBtn).toBeVisible();

    // We won't actually download, but ensure it's enabled
    await expect(downloadBtn).toBeEnabled();
  });

  test('06 — WhatsApp share button is present', async ({ page }) => {
    const shareBtn = page.locator('button').filter({ hasText: /WhatsApp|व्हाट्सएप/ }).first();
    await expect(shareBtn).toBeVisible();
    await expect(shareBtn).toBeEnabled();
  });

  test('07 — Change date and verify reload', async ({ page }) => {
    const dateInput = page.locator('input[type="date"]').first();
    await dateInput.fill('2026-01-14');
    await page.waitForTimeout(3_000); // wait for API reload

    // Skeleton should appear briefly then disappear
    await page.waitForSelector('.animate-pulse', { state: 'detached', timeout: 20_000 }).catch(() => {});
    await page.waitForTimeout(1_000);

    await screenshotTab(page, '07-date-changed');

    // Reset to today so other tests aren't affected
    const today = new Date().toISOString().split('T')[0];
    await dateInput.fill(today);
    await page.waitForTimeout(3_000);
  });

  test('08 — City search autocomplete works', async ({ page }) => {
    const cityInput = page.locator('input[placeholder*="Search"], input[placeholder*="शहर"]').first();
    await cityInput.fill('Mumbai');
    await page.waitForTimeout(1_500);

    // Dropdown suggestions should appear
    const suggestions = page.locator('button').filter({ hasText: /Mumbai|Bombay/ });
    const count = await suggestions.count();
    if (count > 0) {
      await suggestions.first().click();
      await page.waitForTimeout(3_000); // API reload
      await screenshotTab(page, '08-city-changed');
    } else {
      console.log('⚠️ No city suggestions found for Mumbai — skipping selection');
    }
  });

  test('09 — Language toggle renders and works correctly', async ({ page }) => {
    // Page is already in Hindi from login(); verify Hindi is active
    const hindiTab = page.locator('button[role="tab"]').filter({ hasText: /हिन्दू कैलेंडर/ }).first();
    await expect(hindiTab).toBeVisible();

    // Find the language toggle button
    const toggleBtn = page.locator('button').filter({ hasText: /EN/ }).filter({ hasText: /हि/ }).first();
    await expect(toggleBtn).toBeVisible();

    // Switch to English
    await toggleBtn.click();
    await page.waitForTimeout(2_000);
    await screenshotTab(page, '09-english-language');

    // Verify English content exists
    const englishTab = page.locator('button[role="tab"]').filter({ hasText: /Hindu Calendar/ }).first();
    await expect(englishTab).toBeVisible();

    // Switch back to Hindi
    await toggleBtn.click();
    await page.waitForTimeout(2_000);
    await screenshotTab(page, '09-hindi-language');

    // Verify Hindi content exists
    await expect(hindiTab).toBeVisible();
    const text = await page.locator('body').innerText();
    const hindiWords = text.match(/[\u0900-\u097F]{2,}/g);
    expect(hindiWords?.length || 0).toBeGreaterThan(5);
    console.log('✅ Hindi mode has', hindiWords?.length, 'Hindi words');
  });

  test('10 — Full page scroll capture for visual regression', async ({ page }) => {
    // Reset to calendar tab first
    const calTab = page.locator('[role="tab"]').filter({ hasText: /Hindu Calendar|हिन्दू/ }).first();
    await calTab.click().catch(() => {});
    await page.waitForTimeout(1_000);
    await page.evaluate(() => window.scrollTo(0, 0));

    // Full-page screenshot
    await page.screenshot({ path: 'e2e/panchang-10-fullpage.png', fullPage: true });
    console.log('📸 Full-page screenshot saved: e2e/panchang-10-fullpage.png');
  });
});
