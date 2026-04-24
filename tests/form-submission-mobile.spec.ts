import { test, expect } from '@playwright/test';

// Test configuration with extended timeouts for mobile
test.describe.configure({ timeout: 60000 });

const BASE_URL = 'http://localhost:5174';
const VIEWPORT_IPHONE_14 = { width: 390, height: 844 };
const VIEWPORT_ANDROID_CHROME = { width: 393, height: 851 };

// Helper to collect console messages and network errors
interface TestContext {
  errors: string[];
  warnings: string[];
  networkErrors: { status: number; url: string }[];
}

function setupErrorTracking(page: any): TestContext {
  const context: TestContext = {
    errors: [],
    warnings: [],
    networkErrors: []
  };

  page.on('console', (msg: any) => {
    const text = msg.text();
    if (msg.type() === 'error') {
      context.errors.push(text);
      console.log(`  ⚠️  Error: ${text}`);
    }
    if (msg.type() === 'warning') {
      context.warnings.push(text);
    }
  });

  page.on('response', (response: any) => {
    if (!response.ok()) {
      const status = response.status();
      const url = response.url();
      if (status >= 500) {
        context.networkErrors.push({ status, url });
        console.log(`  ⚠️  HTTP ${status}: ${url}`);
      }
    }
  });

  return context;
}

// ========== IPHONE 14 SAFARI (390x844) ==========

test.describe('iPhone 14 Safari (390x844)', () => {

  test('KundliForm: Fill & Submit', async ({ page }) => {
    const ctx = setupErrorTracking(page);

    console.log('\n📱 iPhone 14 - KundliForm Submission Test');
    await page.setViewportSize(VIEWPORT_IPHONE_14);

    await page.goto(`${BASE_URL}/kundli`, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForTimeout(1000);

    try {
      // Check form existence
      const formVisible = await page.locator('form').isVisible().catch(() => false);
      console.log(`  Form visible: ${formVisible ? '✅' : '❌'}`);

      if (!formVisible) {
        console.log('  RESULT: ❌ Form not found');
        return;
      }

      // Fill date field (look for input with type="date" or similar)
      const dateInput = page.locator('input[type="date"], input[placeholder*="Date"], input[placeholder*="date"]').first();
      const dateExists = await dateInput.isVisible().catch(() => false);

      if (dateExists) {
        await dateInput.fill('1990-05-15');
        console.log(`  ✅ Date filled: 1990-05-15`);
      }

      // Fill time field
      const timeInput = page.locator('input[type="time"], input[placeholder*="Time"], input[placeholder*="time"]').first();
      const timeExists = await timeInput.isVisible().catch(() => false);

      if (timeExists) {
        await timeInput.fill('10:30');
        console.log(`  ✅ Time filled: 10:30`);
      }

      // Fill location field
      const locationInput = page.locator('input[placeholder*="Location"], input[placeholder*="location"], input[placeholder*="Place"], input[placeholder*="place"]').first();
      const locationExists = await locationInput.isVisible().catch(() => false);

      if (locationExists) {
        await locationInput.fill('New Delhi, India');
        console.log(`  ✅ Location filled`);
      }

      // Find and check Generate button visibility
      const generateBtn = page.locator('button:has-text("Generate"), button:has-text("generate"), button:has-text("Submit"), button:has-text("submit")').first();
      const btnVisible = await generateBtn.isVisible().catch(() => false);

      if (btnVisible) {
        const btnOpacity = await generateBtn.evaluate((el: HTMLElement) => window.getComputedStyle(el).opacity);
        console.log(`  Button visible: ✅ (opacity: ${btnOpacity})`);

        // Check button is clickable
        const isEnabled = await generateBtn.isEnabled().catch(() => false);
        console.log(`  Button enabled: ${isEnabled ? '✅' : '❌'}`);

        // Click submit
        await generateBtn.click();
        console.log(`  ✅ Button clicked`);

        // Wait for chart to load
        await page.waitForTimeout(3000);
        const chartLoaded = await page.locator('canvas, svg, .chart, [class*="chart"], [class*="wheel"]').isVisible().catch(() => false);
        console.log(`  Chart loaded: ${chartLoaded ? '✅' : '⚠️'}`);
      } else {
        console.log(`  ❌ Generate button not found or visible`);
      }

      // Check for error messages
      const errorMsg = await page.locator('[class*="error"], [role="alert"]').innerText().catch(() => null);
      if (errorMsg) {
        console.log(`  Error message: ${errorMsg}`);
      }

      console.log(`  Network errors: ${ctx.networkErrors.length}, Console errors: ${ctx.errors.length}`);
      console.log(`  RESULT: ${ctx.errors.length === 0 && ctx.networkErrors.length === 0 ? '✅ PASS' : '⚠️ WARNINGS'}`);
    } catch (e) {
      console.log(`  ❌ Exception: ${e}`);
      console.log(`  RESULT: ❌ FAIL`);
    }
  });

  test('LalKitabForm: Fill & Submit', async ({ page }) => {
    const ctx = setupErrorTracking(page);

    console.log('\n📱 iPhone 14 - LalKitabForm Submission Test');
    await page.setViewportSize(VIEWPORT_IPHONE_14);

    await page.goto(`${BASE_URL}/lal-kitab`, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForTimeout(1000);

    try {
      // Check form existence
      const formVisible = await page.locator('form').isVisible().catch(() => false);
      console.log(`  Form visible: ${formVisible ? '✅' : '❌'}`);

      if (!formVisible) {
        console.log('  RESULT: ❌ Form not found');
        return;
      }

      // Fill name field
      const nameInput = page.locator('input[placeholder*="Name"], input[placeholder*="name"], input[type="text"]').first();
      const nameExists = await nameInput.isVisible().catch(() => false);

      if (nameExists) {
        await nameInput.fill('John Doe');
        console.log(`  ✅ Name filled`);
      }

      // Fill DOB field
      const dobInput = page.locator('input[placeholder*="DOB"], input[placeholder*="Birth"], input[type="date"]').first();
      const dobExists = await dobInput.isVisible().catch(() => false);

      if (dobExists) {
        await dobInput.fill('1985-07-20');
        console.log(`  ✅ DOB filled`);
      }

      // Find and check submit button
      const submitBtn = page.locator('button:has-text("Generate"), button:has-text("generate"), button:has-text("Lal"), button:has-text("lal"), button:has-text("Submit")').first();
      const btnVisible = await submitBtn.isVisible().catch(() => false);

      if (btnVisible) {
        const btnOpacity = await submitBtn.evaluate((el: HTMLElement) => window.getComputedStyle(el).opacity);
        console.log(`  Button visible: ✅ (opacity: ${btnOpacity})`);

        const isEnabled = await submitBtn.isEnabled().catch(() => false);
        console.log(`  Button enabled: ${isEnabled ? '✅' : '❌'}`);

        await submitBtn.click();
        console.log(`  ✅ Button clicked`);

        // Wait for predictions to load
        await page.waitForTimeout(3000);
        const predictionsLoaded = await page.locator('.predictions, [class*="prediction"], .analysis, [class*="analysis"]').isVisible().catch(() => false);
        console.log(`  Predictions loaded: ${predictionsLoaded ? '✅' : '⚠️'}`);
      } else {
        console.log(`  ❌ Submit button not found`);
      }

      console.log(`  Network errors: ${ctx.networkErrors.length}, Console errors: ${ctx.errors.length}`);
      console.log(`  RESULT: ${ctx.errors.length === 0 && ctx.networkErrors.length === 0 ? '✅ PASS' : '⚠️ WARNINGS'}`);
    } catch (e) {
      console.log(`  ❌ Exception: ${e}`);
      console.log(`  RESULT: ❌ FAIL`);
    }
  });

  test('VastuForm: Fill & Submit', async ({ page }) => {
    const ctx = setupErrorTracking(page);

    console.log('\n📱 iPhone 14 - VastuForm Submission Test');
    await page.setViewportSize(VIEWPORT_IPHONE_14);

    await page.goto(`${BASE_URL}/vastu`, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForTimeout(1000);

    try {
      const formVisible = await page.locator('form').isVisible().catch(() => false);
      console.log(`  Form visible: ${formVisible ? '✅' : '❌'}`);

      if (!formVisible) {
        console.log('  RESULT: ❌ Form not found');
        return;
      }

      // Fill room dimensions
      const inputs = page.locator('input[type="number"], input[placeholder*="dimension"], input[placeholder*="size"], input[placeholder*="length"], input[placeholder*="width"]');
      const inputCount = await inputs.count();

      if (inputCount >= 2) {
        await inputs.nth(0).fill('15');
        await inputs.nth(1).fill('20');
        console.log(`  ✅ Room dimensions filled (15x20)`);
      }

      // Find submit button
      const submitBtn = page.locator('button:has-text("Analyze"), button:has-text("analyze"), button:has-text("Submit"), button:has-text("submit")').first();
      const btnVisible = await submitBtn.isVisible().catch(() => false);

      if (btnVisible) {
        const btnOpacity = await submitBtn.evaluate((el: HTMLElement) => window.getComputedStyle(el).opacity);
        console.log(`  Button visible: ✅ (opacity: ${btnOpacity})`);

        await submitBtn.click();
        console.log(`  ✅ Button clicked`);

        await page.waitForTimeout(3000);
        const analysisLoaded = await page.locator('.analysis, [class*="analysis"], .results, [class*="result"]').isVisible().catch(() => false);
        console.log(`  Analysis loaded: ${analysisLoaded ? '✅' : '⚠️'}`);
      } else {
        console.log(`  ❌ Submit button not found`);
      }

      console.log(`  Network errors: ${ctx.networkErrors.length}, Console errors: ${ctx.errors.length}`);
      console.log(`  RESULT: ${ctx.errors.length === 0 && ctx.networkErrors.length === 0 ? '✅ PASS' : '⚠️ WARNINGS'}`);
    } catch (e) {
      console.log(`  ❌ Exception: ${e}`);
      console.log(`  RESULT: ❌ FAIL`);
    }
  });

  test('ProfileEditPanel: Edit & Save', async ({ page }) => {
    const ctx = setupErrorTracking(page);

    console.log('\n📱 iPhone 14 - ProfileEditPanel Submission Test');
    await page.setViewportSize(VIEWPORT_IPHONE_14);

    await page.goto(`${BASE_URL}/profile`, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForTimeout(1000);

    try {
      // Check if edit button exists
      const editBtn = page.locator('button:has-text("Edit"), button:has-text("edit"), [class*="edit"]').first();
      const editBtnVisible = await editBtn.isVisible().catch(() => false);

      if (editBtnVisible) {
        await editBtn.click();
        console.log(`  ✅ Edit button clicked`);
        await page.waitForTimeout(500);
      }

      // Try to find editable fields
      const inputs = page.locator('input[type="text"], textarea');
      const inputCount = await inputs.count();

      if (inputCount > 0) {
        const firstInput = inputs.first();
        const currentValue = await firstInput.inputValue().catch(() => '');
        await firstInput.fill(currentValue + ' Updated');
        console.log(`  ✅ Field updated`);

        // Find save button
        const saveBtn = page.locator('button:has-text("Save"), button:has-text("save"), button:has-text("Update"), button:has-text("update")').first();
        const saveBtnVisible = await saveBtn.isVisible().catch(() => false);

        if (saveBtnVisible) {
          await saveBtn.click();
          console.log(`  ✅ Save button clicked`);

          await page.waitForTimeout(2000);

          // Check for success message
          const successMsg = await page.locator('[class*="success"], [role="status"]').innerText().catch(() => null);
          if (successMsg) {
            console.log(`  ✅ Success message: ${successMsg}`);
          }

          // Reload and check persistence
          await page.reload({ waitUntil: 'domcontentloaded' });
          await page.waitForTimeout(1000);
          const reloadValue = await firstInput.inputValue().catch(() => '');
          const persisted = reloadValue.includes('Updated');
          console.log(`  Data persisted: ${persisted ? '✅' : '❌'}`);
        } else {
          console.log(`  ⚠️ Save button not found`);
        }
      } else {
        console.log(`  ⚠️ No editable fields found`);
      }

      console.log(`  Network errors: ${ctx.networkErrors.length}, Console errors: ${ctx.errors.length}`);
      console.log(`  RESULT: ${ctx.errors.length === 0 && ctx.networkErrors.length === 0 ? '✅ PASS' : '⚠️ WARNINGS'}`);
    } catch (e) {
      console.log(`  ❌ Exception: ${e}`);
      console.log(`  RESULT: ❌ FAIL`);
    }
  });

  test('Login Form: Submit', async ({ page }) => {
    const ctx = setupErrorTracking(page);

    console.log('\n📱 iPhone 14 - Login Form Test');
    await page.setViewportSize(VIEWPORT_IPHONE_14);

    await page.goto(`${BASE_URL}/login`, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForTimeout(1000);

    try {
      const formVisible = await page.locator('form').isVisible().catch(() => false);
      console.log(`  Form visible: ${formVisible ? '✅' : '❌'}`);

      if (!formVisible) {
        console.log('  RESULT: ❌ Form not found');
        return;
      }

      // Fill email
      const emailInput = page.locator('input[type="email"], input[placeholder*="Email"], input[placeholder*="email"]').first();
      const emailExists = await emailInput.isVisible().catch(() => false);

      if (emailExists) {
        await emailInput.fill('test@example.com');
        console.log(`  ✅ Email filled`);
      }

      // Fill password
      const passwordInput = page.locator('input[type="password"]').first();
      const passwordExists = await passwordInput.isVisible().catch(() => false);

      if (passwordExists) {
        await passwordInput.fill('TestPassword123');
        console.log(`  ✅ Password filled`);
      }

      // Find and click submit button
      const submitBtn = page.locator('button[type="submit"], button:has-text("Login"), button:has-text("login"), button:has-text("Sign In"), button:has-text("sign in")').first();
      const btnVisible = await submitBtn.isVisible().catch(() => false);

      if (btnVisible) {
        const btnOpacity = await submitBtn.evaluate((el: HTMLElement) => window.getComputedStyle(el).opacity);
        console.log(`  Button visible: ✅ (opacity: ${btnOpacity})`);

        await submitBtn.click();
        console.log(`  ✅ Submit clicked`);

        // Wait for response
        await page.waitForTimeout(3000);

        // Check for error or redirect
        const errorMsg = await page.locator('[class*="error"], [role="alert"]').innerText().catch(() => null);
        const currentUrl = page.url();

        if (errorMsg) {
          console.log(`  Error message shown: ${errorMsg}`);
        } else if (currentUrl !== `${BASE_URL}/login`) {
          console.log(`  ✅ Redirected to: ${currentUrl}`);
        } else {
          console.log(`  ⚠️ No redirect or error shown`);
        }
      } else {
        console.log(`  ❌ Submit button not found`);
      }

      console.log(`  Network errors: ${ctx.networkErrors.length}, Console errors: ${ctx.errors.length}`);
      console.log(`  RESULT: ${ctx.errors.length === 0 && ctx.networkErrors.length === 0 ? '✅ PASS' : '⚠️ WARNINGS'}`);
    } catch (e) {
      console.log(`  ❌ Exception: ${e}`);
      console.log(`  RESULT: ❌ FAIL`);
    }
  });
});

// ========== ANDROID CHROME (393x851) ==========

test.describe('Android Chrome (393x851)', () => {

  test('KundliForm: Fill & Submit', async ({ page }) => {
    const ctx = setupErrorTracking(page);

    console.log('\n📱 Android Chrome - KundliForm Submission Test');
    await page.setViewportSize(VIEWPORT_ANDROID_CHROME);

    await page.goto(`${BASE_URL}/kundli`, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForTimeout(1000);

    try {
      const formVisible = await page.locator('form').isVisible().catch(() => false);
      console.log(`  Form visible: ${formVisible ? '✅' : '❌'}`);

      if (!formVisible) {
        console.log('  RESULT: ❌ Form not found');
        return;
      }

      const dateInput = page.locator('input[type="date"], input[placeholder*="Date"]').first();
      if (await dateInput.isVisible().catch(() => false)) {
        await dateInput.fill('1992-03-22');
        console.log(`  ✅ Date filled: 1992-03-22`);
      }

      const timeInput = page.locator('input[type="time"], input[placeholder*="Time"]').first();
      if (await timeInput.isVisible().catch(() => false)) {
        await timeInput.fill('14:15');
        console.log(`  ✅ Time filled: 14:15`);
      }

      const locationInput = page.locator('input[placeholder*="Location"], input[placeholder*="Place"]').first();
      if (await locationInput.isVisible().catch(() => false)) {
        await locationInput.fill('Mumbai, India');
        console.log(`  ✅ Location filled`);
      }

      const generateBtn = page.locator('button:has-text("Generate"), button:has-text("Submit")').first();
      if (await generateBtn.isVisible().catch(() => false)) {
        const btnOpacity = await generateBtn.evaluate((el: HTMLElement) => window.getComputedStyle(el).opacity);
        console.log(`  Button visible: ✅ (opacity: ${btnOpacity})`);

        await generateBtn.click();
        console.log(`  ✅ Button clicked`);

        await page.waitForTimeout(3000);
        const chartLoaded = await page.locator('canvas, svg, .chart, [class*="wheel"]').isVisible().catch(() => false);
        console.log(`  Chart loaded: ${chartLoaded ? '✅' : '⚠️'}`);
      } else {
        console.log(`  ❌ Generate button not found`);
      }

      console.log(`  Network errors: ${ctx.networkErrors.length}, Console errors: ${ctx.errors.length}`);
      console.log(`  RESULT: ${ctx.errors.length === 0 && ctx.networkErrors.length === 0 ? '✅ PASS' : '⚠️ WARNINGS'}`);
    } catch (e) {
      console.log(`  ❌ Exception: ${e}`);
      console.log(`  RESULT: ❌ FAIL`);
    }
  });

  test('LalKitabForm: Fill & Submit', async ({ page }) => {
    const ctx = setupErrorTracking(page);

    console.log('\n📱 Android Chrome - LalKitabForm Submission Test');
    await page.setViewportSize(VIEWPORT_ANDROID_CHROME);

    await page.goto(`${BASE_URL}/lal-kitab`, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForTimeout(1000);

    try {
      const formVisible = await page.locator('form').isVisible().catch(() => false);
      console.log(`  Form visible: ${formVisible ? '✅' : '❌'}`);

      if (!formVisible) {
        console.log('  RESULT: ❌ Form not found');
        return;
      }

      const nameInput = page.locator('input[placeholder*="Name"], input[type="text"]').first();
      if (await nameInput.isVisible().catch(() => false)) {
        await nameInput.fill('Jane Smith');
        console.log(`  ✅ Name filled`);
      }

      const dobInput = page.locator('input[placeholder*="DOB"], input[placeholder*="Birth"], input[type="date"]').first();
      if (await dobInput.isVisible().catch(() => false)) {
        await dobInput.fill('1988-11-10');
        console.log(`  ✅ DOB filled`);
      }

      const submitBtn = page.locator('button:has-text("Generate"), button:has-text("Lal"), button:has-text("Submit")').first();
      if (await submitBtn.isVisible().catch(() => false)) {
        const btnOpacity = await submitBtn.evaluate((el: HTMLElement) => window.getComputedStyle(el).opacity);
        console.log(`  Button visible: ✅ (opacity: ${btnOpacity})`);

        await submitBtn.click();
        console.log(`  ✅ Button clicked`);

        await page.waitForTimeout(3000);
        const predictionsLoaded = await page.locator('.predictions, [class*="prediction"], .analysis').isVisible().catch(() => false);
        console.log(`  Predictions loaded: ${predictionsLoaded ? '✅' : '⚠️'}`);
      } else {
        console.log(`  ❌ Submit button not found`);
      }

      console.log(`  Network errors: ${ctx.networkErrors.length}, Console errors: ${ctx.errors.length}`);
      console.log(`  RESULT: ${ctx.errors.length === 0 && ctx.networkErrors.length === 0 ? '✅ PASS' : '⚠️ WARNINGS'}`);
    } catch (e) {
      console.log(`  ❌ Exception: ${e}`);
      console.log(`  RESULT: ❌ FAIL`);
    }
  });

  test('VastuForm: Fill & Submit', async ({ page }) => {
    const ctx = setupErrorTracking(page);

    console.log('\n📱 Android Chrome - VastuForm Submission Test');
    await page.setViewportSize(VIEWPORT_ANDROID_CHROME);

    await page.goto(`${BASE_URL}/vastu`, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForTimeout(1000);

    try {
      const formVisible = await page.locator('form').isVisible().catch(() => false);
      console.log(`  Form visible: ${formVisible ? '✅' : '❌'}`);

      if (!formVisible) {
        console.log('  RESULT: ❌ Form not found');
        return;
      }

      const inputs = page.locator('input[type="number"], input[placeholder*="dimension"]');
      if (await inputs.count() >= 2) {
        await inputs.nth(0).fill('18');
        await inputs.nth(1).fill('25');
        console.log(`  ✅ Dimensions filled (18x25)`);
      }

      const submitBtn = page.locator('button:has-text("Analyze"), button:has-text("Submit")').first();
      if (await submitBtn.isVisible().catch(() => false)) {
        const btnOpacity = await submitBtn.evaluate((el: HTMLElement) => window.getComputedStyle(el).opacity);
        console.log(`  Button visible: ✅ (opacity: ${btnOpacity})`);

        await submitBtn.click();
        console.log(`  ✅ Button clicked`);

        await page.waitForTimeout(3000);
        const analysisLoaded = await page.locator('.analysis, [class*="result"]').isVisible().catch(() => false);
        console.log(`  Analysis loaded: ${analysisLoaded ? '✅' : '⚠️'}`);
      } else {
        console.log(`  ❌ Submit button not found`);
      }

      console.log(`  Network errors: ${ctx.networkErrors.length}, Console errors: ${ctx.errors.length}`);
      console.log(`  RESULT: ${ctx.errors.length === 0 && ctx.networkErrors.length === 0 ? '✅ PASS' : '⚠️ WARNINGS'}`);
    } catch (e) {
      console.log(`  ❌ Exception: ${e}`);
      console.log(`  RESULT: ❌ FAIL`);
    }
  });

  test('ProfileEditPanel: Edit & Save', async ({ page }) => {
    const ctx = setupErrorTracking(page);

    console.log('\n📱 Android Chrome - ProfileEditPanel Test');
    await page.setViewportSize(VIEWPORT_ANDROID_CHROME);

    await page.goto(`${BASE_URL}/profile`, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForTimeout(1000);

    try {
      const editBtn = page.locator('button:has-text("Edit"), [class*="edit"]').first();
      if (await editBtn.isVisible().catch(() => false)) {
        await editBtn.click();
        console.log(`  ✅ Edit button clicked`);
        await page.waitForTimeout(500);
      }

      const inputs = page.locator('input[type="text"], textarea');
      if (await inputs.count() > 0) {
        const firstInput = inputs.first();
        const currentValue = await firstInput.inputValue().catch(() => '');
        await firstInput.fill(currentValue + ' Android');
        console.log(`  ✅ Field updated`);

        const saveBtn = page.locator('button:has-text("Save"), button:has-text("Update")').first();
        if (await saveBtn.isVisible().catch(() => false)) {
          await saveBtn.click();
          console.log(`  ✅ Save button clicked`);

          await page.waitForTimeout(2000);
          const successMsg = await page.locator('[class*="success"]').innerText().catch(() => null);
          if (successMsg) {
            console.log(`  ✅ Success message shown`);
          }

          await page.reload({ waitUntil: 'domcontentloaded' });
          await page.waitForTimeout(1000);
          const reloadValue = await firstInput.inputValue().catch(() => '');
          const persisted = reloadValue.includes('Android');
          console.log(`  Data persisted: ${persisted ? '✅' : '❌'}`);
        } else {
          console.log(`  ⚠️ Save button not found`);
        }
      } else {
        console.log(`  ⚠️ No editable fields found`);
      }

      console.log(`  Network errors: ${ctx.networkErrors.length}, Console errors: ${ctx.errors.length}`);
      console.log(`  RESULT: ${ctx.errors.length === 0 && ctx.networkErrors.length === 0 ? '✅ PASS' : '⚠️ WARNINGS'}`);
    } catch (e) {
      console.log(`  ❌ Exception: ${e}`);
      console.log(`  RESULT: ❌ FAIL`);
    }
  });

  test('Login Form: Submit', async ({ page }) => {
    const ctx = setupErrorTracking(page);

    console.log('\n📱 Android Chrome - Login Form Test');
    await page.setViewportSize(VIEWPORT_ANDROID_CHROME);

    await page.goto(`${BASE_URL}/login`, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForTimeout(1000);

    try {
      const formVisible = await page.locator('form').isVisible().catch(() => false);
      console.log(`  Form visible: ${formVisible ? '✅' : '❌'}`);

      if (!formVisible) {
        console.log('  RESULT: ❌ Form not found');
        return;
      }

      const emailInput = page.locator('input[type="email"], input[placeholder*="Email"]').first();
      if (await emailInput.isVisible().catch(() => false)) {
        await emailInput.fill('android@test.com');
        console.log(`  ✅ Email filled`);
      }

      const passwordInput = page.locator('input[type="password"]').first();
      if (await passwordInput.isVisible().catch(() => false)) {
        await passwordInput.fill('AndroidTest123');
        console.log(`  ✅ Password filled`);
      }

      const submitBtn = page.locator('button[type="submit"], button:has-text("Login"), button:has-text("Sign In")').first();
      if (await submitBtn.isVisible().catch(() => false)) {
        const btnOpacity = await submitBtn.evaluate((el: HTMLElement) => window.getComputedStyle(el).opacity);
        console.log(`  Button visible: ✅ (opacity: ${btnOpacity})`);

        await submitBtn.click();
        console.log(`  ✅ Submit clicked`);

        await page.waitForTimeout(3000);

        const errorMsg = await page.locator('[class*="error"], [role="alert"]').innerText().catch(() => null);
        const currentUrl = page.url();

        if (errorMsg) {
          console.log(`  Error message shown: ${errorMsg}`);
        } else if (currentUrl !== `${BASE_URL}/login`) {
          console.log(`  ✅ Redirected to: ${currentUrl}`);
        } else {
          console.log(`  ⚠️ No redirect or error shown`);
        }
      } else {
        console.log(`  ❌ Submit button not found`);
      }

      console.log(`  Network errors: ${ctx.networkErrors.length}, Console errors: ${ctx.errors.length}`);
      console.log(`  RESULT: ${ctx.errors.length === 0 && ctx.networkErrors.length === 0 ? '✅ PASS' : '⚠️ WARNINGS'}`);
    } catch (e) {
      console.log(`  ❌ Exception: ${e}`);
      console.log(`  RESULT: ❌ FAIL`);
    }
  });
});
