import { test, expect } from '@playwright/test';

test('login → load kundli → check all new tabs', async ({ page }) => {
  const errors: string[] = [];
  page.on('console', (msg) => { if (msg.type() === 'error') errors.push(msg.text()); });
  page.on('pageerror', (err) => errors.push(`PAGE_ERROR: ${err.message}`));

  const apiCalls: string[] = [];
  page.on('response', (res) => {
    if (res.url().includes('/api/')) {
      apiCalls.push(`${res.status()} ${res.url().replace(/.*\/api\//, '/api/')}`);
    }
  });

  // 1. Login
  await page.goto('/login', { waitUntil: 'networkidle' });
  await page.waitForSelector('input[type="email"]', { timeout: 15_000 });
  await page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com');
  await page.locator('input[type="password"]').fill('123456');
  await page.locator('button').filter({ hasText: /sign in/i }).last().click();
  await page.waitForURL('**/', { timeout: 15_000 });

  // 2. Go to Kundli
  await page.goto('/kundli', { waitUntil: 'networkidle' });
  await page.waitForTimeout(3_000);

  // 3. Click the first kundli card button (w-full text-left inside the card)
  const kundliButton = page.locator('button.w-full.text-left').first();
  await expect(kundliButton).toBeVisible({ timeout: 10_000 });
  const kundliName = await kundliButton.locator('h4').textContent();
  console.log(`[KUNDLI] Clicking: ${kundliName}`);
  await kundliButton.click();

  // Wait for data to load
  await page.waitForTimeout(12_000);

  console.log('[ERRORS]:', errors.slice(0, 5));
  console.log('[API]:', apiCalls);

  await page.screenshot({ path: 'test-results/debug-02-after-click.png', fullPage: true });

  // Check state
  const tabsVisible = await page.locator('[role="tab"]').first().isVisible().catch(() => false);
  console.log(`[STATE] tabs=${tabsVisible}`);

  if (!tabsVisible) {
    console.log('[CRASH] Page crashed — no tabs visible');
    console.log('[ALL ERRORS]:', errors);
    return;
  }

  // List tabs
  const allTabs = page.locator('[role="tab"]');
  const tabCount = await allTabs.count();
  console.log(`[TABS] ${tabCount} tabs found`);

  // Check each new tab
  const newTabs = ['KP System', 'Yogini Dasha', 'Upagrahas', 'Sodashvarga', 'Aspects', 'Sade Sati'];
  for (const tabName of newTabs) {
    const tab = page.locator('[role="tab"]').filter({ hasText: new RegExp(tabName, 'i') });
    if (!(await tab.isVisible().catch(() => false))) {
      console.log(`[TAB] ${tabName}: NOT FOUND`);
      continue;
    }
    await tab.click();
    await page.waitForTimeout(2_000);
    const content = await page.locator('[role="tabpanel"]:visible').textContent().catch(() => '');
    const hasPlaceholder = content?.includes('Click the') || false;
    const hasTable = await page.locator('[role="tabpanel"]:visible table').isVisible().catch(() => false);
    console.log(`[TAB] ${tabName}: placeholder=${hasPlaceholder}, table=${hasTable}, content="${content?.slice(0, 100)}"`);
    await page.screenshot({ path: `test-results/debug-tab-${tabName.toLowerCase().replace(/\s/g, '-')}.png` });
  }

  console.log('[FINAL ERRORS]:', errors);
});
