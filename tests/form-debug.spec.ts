import { test } from '@playwright/test';

test('Debug: Inspect page structure', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('http://localhost:5174/', { waitUntil: 'networkidle', timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(2000);

  const forms = await page.locator('form').count();
  const inputs = await page.locator('input').count();
  const buttons = await page.locator('button').count();

  console.log(`\n=== HOME PAGE ===`);
  console.log(`Found: ${forms} forms, ${inputs} inputs, ${buttons} buttons`);

  const btnTexts = await page.locator('button').evaluateAll((buttons: any[]) =>
    buttons.slice(0, 15).map(b => b.textContent?.trim()).filter(t => t && t.length > 0)
  );
  console.log(`Button texts: ${btnTexts.join(', ')}`);

  const inputTypes = await page.locator('input').evaluateAll((inputs: any[]) =>
    inputs.slice(0, 10).map(i => `${i.type}${i.placeholder ? `[${i.placeholder}]` : ''}`)
  );
  console.log(`Input types: ${inputTypes.join(', ')}`);

  // Check login page
  await page.goto('http://localhost:5174/login', { waitUntil: 'domcontentloaded', timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(1000);

  const loginForms = await page.locator('form').count();
  const loginInputs = await page.locator('input').count();
  const loginButtons = await page.locator('button').count();

  console.log(`\n=== LOGIN PAGE ===`);
  console.log(`Forms: ${loginForms}, Inputs: ${loginInputs}, Buttons: ${loginButtons}`);

  const loginBtnTexts = await page.locator('button').evaluateAll((buttons: any[]) =>
    buttons.slice(0, 10).map(b => b.textContent?.trim()).filter(t => t)
  );
  console.log(`Buttons: ${loginBtnTexts.join(', ')}`);

  const loginInputTypes = await page.locator('input').evaluateAll((inputs: any[]) =>
    inputs.slice(0, 5).map(i => `${i.type}${i.placeholder ? `[${i.placeholder}]` : ''}${i.name ? `(${i.name})` : ''}`)
  );
  console.log(`Inputs: ${loginInputTypes.join(', ')}`);
});
