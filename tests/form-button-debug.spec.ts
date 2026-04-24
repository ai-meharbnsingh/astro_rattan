import { test } from '@playwright/test';

test('Debug: Kundli button state', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('http://localhost:5174/', { waitUntil: 'networkidle', timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(1500);

  const submitBtn = page.locator('button:has-text("Submit")').first();

  const isVisible = await submitBtn.isVisible().catch(() => false);
  const isEnabled = await submitBtn.isEnabled().catch(() => false);
  const isDisabled = await submitBtn.isDisabled().catch(() => false);

  const textContent = await submitBtn.textContent();
  const ariaDisabled = await submitBtn.getAttribute('aria-disabled');
  const disabled = await submitBtn.getAttribute('disabled');

  const classList = await submitBtn.evaluate((el: HTMLElement) => {
    return {
      classList: Array.from(el.classList),
      style: el.getAttribute('style'),
      opacity: window.getComputedStyle(el).opacity,
      pointerEvents: window.getComputedStyle(el).pointerEvents,
      cursor: window.getComputedStyle(el).cursor
    };
  });

  console.log(`\n=== BUTTON STATE DEBUG ===`);
  console.log(`Text: "${textContent}"`);
  console.log(`isVisible: ${isVisible}`);
  console.log(`isEnabled: ${isEnabled}`);
  console.log(`isDisabled: ${isDisabled}`);
  console.log(`disabled attr: ${disabled}`);
  console.log(`aria-disabled: ${ariaDisabled}`);
  console.log(`classList: ${classList.classList.join(' ')}`);
  console.log(`opacity: ${classList.opacity}`);
  console.log(`pointer-events: ${classList.pointerEvents}`);
  console.log(`cursor: ${classList.cursor}`);
});
