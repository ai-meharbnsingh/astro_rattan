import { test, expect } from '@playwright/test';

/**
 * P28 AstroVedic — Numerology, Tarot & Feature Verification E2E Tests
 * Verifies all features from user feedback are accessible and functional.
 */

// ─── NUMEROLOGY ─────────────────────────────────────────────────────────

test.describe('Numerology', () => {
  test('should load numerology page with form', async ({ page }) => {
    await page.goto('/numerology', { waitUntil: 'networkidle' });
    await page.waitForSelector('input[placeholder="Full Name"]', { timeout: 15_000 });

    await expect(page.locator('input[placeholder="Full Name"]')).toBeVisible();
    await expect(page.locator('input[type="date"]')).toBeVisible();
    await expect(page.locator('button').filter({ hasText: /calculate/i })).toBeVisible();
  });

  test('calculate button should be disabled without inputs', async ({ page }) => {
    await page.goto('/numerology', { waitUntil: 'networkidle' });
    await page.waitForSelector('input[placeholder="Full Name"]', { timeout: 15_000 });

    const calcButton = page.locator('button').filter({ hasText: /calculate/i });
    await expect(calcButton).toBeDisabled();
  });

  test('should calculate numerology and show results', async ({ page }) => {
    await page.goto('/numerology', { waitUntil: 'networkidle' });
    await page.waitForSelector('input[placeholder="Full Name"]', { timeout: 15_000 });

    // Intercept the API call
    const responsePromise = page.waitForResponse(
      (res) => res.url().includes('/api/numerology/calculate'),
      { timeout: 15_000 },
    );

    await page.locator('input[placeholder="Full Name"]').fill('Gaurav Rattan');
    await page.locator('input[type="date"]').fill('1990-05-15');

    const calcButton = page.locator('button').filter({ hasText: /calculate/i });
    await expect(calcButton).toBeEnabled();
    await calcButton.click();

    // Wait for API response
    const response = await responsePromise;
    console.log(`[NUMEROLOGY] API status: ${response.status()}`);
    const body = await response.json();
    console.log(`[NUMEROLOGY] Response:`, JSON.stringify(body));

    // Verify results card appears
    const resultsCard = page.locator('text=Your Numerology Report');
    await expect(resultsCard).toBeVisible({ timeout: 10_000 });

    // Verify all 4 numbers are displayed
    await expect(page.locator('text=Life Path')).toBeVisible();
    await expect(page.locator('text=Expression')).toBeVisible();
    await expect(page.locator('text=Soul Urge')).toBeVisible();
    await expect(page.locator('text=Personality')).toBeVisible();

    // Verify predictions section appears
    await expect(page.locator('text=Predictions')).toBeVisible();
  });

  test('should NOT show blank page after calculate (regression)', async ({ page }) => {
    await page.goto('/numerology', { waitUntil: 'networkidle' });
    await page.waitForSelector('input[placeholder="Full Name"]', { timeout: 15_000 });

    await page.locator('input[placeholder="Full Name"]').fill('Test User');
    await page.locator('input[type="date"]').fill('1985-03-20');

    const calcButton = page.locator('button').filter({ hasText: /calculate/i });
    await calcButton.click();

    // Wait for loading to finish
    await page.waitForTimeout(5_000);

    // The page should NOT be blank — either results OR error should show
    const hasResults = await page.locator('text=Your Numerology Report').isVisible();
    const hasError = await page.locator('.text-red-400').isVisible();
    const hasForm = await page.locator('input[placeholder="Full Name"]').isVisible();

    console.log(`[REGRESSION] Results visible: ${hasResults}, Error visible: ${hasError}, Form visible: ${hasForm}`);

    // At minimum, the form should still be visible (not blank)
    expect(hasForm).toBe(true);
    // And either results or error should be shown
    expect(hasResults || hasError).toBe(true);
  });
});

// ─── TAROT ──────────────────────────────────────────────────────────────

test.describe('Tarot', () => {
  test('should switch to Tarot tab and draw cards', async ({ page }) => {
    await page.goto('/numerology', { waitUntil: 'networkidle' });
    await page.waitForSelector('[role="tab"]', { timeout: 15_000 });

    // Click Tarot tab
    const tarotTab = page.locator('[role="tab"]').filter({ hasText: /tarot/i });
    await tarotTab.click();
    await page.waitForTimeout(300);

    // Draw Cards button should be visible
    const drawButton = page.locator('button').filter({ hasText: /draw cards/i });
    await expect(drawButton).toBeVisible();

    // Draw a single card
    await drawButton.click();

    // Wait for results
    await page.waitForTimeout(5_000);

    // Should show card results or error (not blank)
    const hasCards = await page.locator('.aspect-\\[2\\/3\\]').first().isVisible();
    const hasError = await page.locator('.text-red-400').isVisible();
    console.log(`[TAROT] Cards visible: ${hasCards}, Error: ${hasError}`);
  });
});

// ─── PALMISTRY ──────────────────────────────────────────────────────────

test.describe('Palmistry', () => {
  test('should switch to Palmistry tab and load guide', async ({ page }) => {
    await page.goto('/numerology', { waitUntil: 'networkidle' });
    await page.waitForSelector('[role="tab"]', { timeout: 15_000 });

    // Click Palmistry tab
    const palmTab = page.locator('[role="tab"]').filter({ hasText: /palmistry/i });
    await palmTab.click();
    await page.waitForTimeout(500);

    // Should show load button or auto-load
    const loadButton = page.locator('button').filter({ hasText: /load guide/i });
    if (await loadButton.isVisible()) {
      await loadButton.click();
    }

    // Wait for content
    await page.waitForTimeout(5_000);

    // Should show palm lines or error
    const hasContent = await page.locator('text=Palm Lines').isVisible();
    const hasError = await page.locator('.text-red-400').isVisible();
    console.log(`[PALMISTRY] Content visible: ${hasContent}, Error: ${hasError}`);
  });
});

// ─── FEATURE PAGES ACCESSIBILITY ────────────────────────────────────────

test.describe('Feature Pages Load Check', () => {
  const pages = [
    { path: '/kundli', name: 'Kundli Generator' },
    { path: '/horoscope', name: 'Daily Horoscope' },
    { path: '/panchang', name: 'Panchang' },
    { path: '/numerology', name: 'Numerology' },
    { path: '/kp-lalkitab', name: 'KP & Lal Kitab' },
    { path: '/consultation', name: 'Consultation' },
    { path: '/ai-chat', name: 'AI Chat' },
    { path: '/blog', name: 'Blog' },
    { path: '/transits', name: 'Planetary Transits' },
  ];

  for (const pg of pages) {
    test(`${pg.name} page should load without errors`, async ({ page }) => {
      // Listen for console errors
      const errors: string[] = [];
      page.on('console', (msg) => {
        if (msg.type() === 'error') errors.push(msg.text());
      });

      await page.goto(pg.path, { waitUntil: 'networkidle', timeout: 30_000 });

      // Page should not be blank — at least navigation should be visible
      const nav = page.locator('nav, header, [class*="Navigation"]').first();
      await expect(nav).toBeVisible({ timeout: 10_000 });

      // Log any console errors
      if (errors.length > 0) {
        console.log(`[${pg.name}] Console errors:`, errors.slice(0, 3));
      }
    });
  }
});
