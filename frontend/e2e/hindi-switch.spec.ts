import { test, expect } from '@playwright/test';

test('language switch EN → Hindi → verify UI changes', async ({ page }) => {
  await page.goto('/', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2_000);

  // Check English is default
  const nav = page.locator('nav');
  await expect(nav).toContainText('Kundli');
  await page.screenshot({ path: 'test-results/lang-01-english.png' });

  // Find and click the language switcher (EN/हिं button)
  const switcher = page.locator('button').filter({ hasText: /EN.*हिं|हिं.*EN/ }).first();
  await expect(switcher).toBeVisible({ timeout: 5_000 });
  console.log('[LANG] Switcher found, clicking...');
  await switcher.click();
  await page.waitForTimeout(1_000);

  // Verify Hindi text appears in navigation
  await expect(nav).toContainText('कुंडली');
  console.log('[LANG] Nav shows Hindi: कुंडली');

  await page.screenshot({ path: 'test-results/lang-02-hindi.png' });

  // Navigate to login page — should show Hindi
  await page.goto('/login', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1_000);
  const heading = page.locator('h2');
  const headingText = await heading.textContent();
  console.log(`[LANG] Login heading: ${headingText}`);
  await page.screenshot({ path: 'test-results/lang-03-hindi-login.png' });

  // Switch back to English
  const switcher2 = page.locator('button').filter({ hasText: /EN.*हिं|हिं.*EN/ }).first();
  await switcher2.click();
  await page.waitForTimeout(1_000);

  await expect(nav).toContainText('Kundli');
  console.log('[LANG] Switched back to English');
  await page.screenshot({ path: 'test-results/lang-04-back-english.png' });
});

test('Hindi persists across page navigation', async ({ page }) => {
  // Set Hindi first
  await page.goto('/', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1_000);
  const switcher = page.locator('button').filter({ hasText: /EN.*हिं|हिं.*EN/ }).first();
  await switcher.click();
  await page.waitForTimeout(500);

  // Navigate to /kundli
  await page.goto('/kundli', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2_000);

  // Nav should still be Hindi
  const nav = page.locator('nav');
  await expect(nav).toContainText('कुंडली');
  console.log('[PERSIST] Hindi persists on /kundli');

  await page.screenshot({ path: 'test-results/lang-05-hindi-kundli.png' });
});
