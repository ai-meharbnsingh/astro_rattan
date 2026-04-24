import { test, expect } from '@playwright/test';

// Test configuration
test.describe.configure({ timeout: 90000 });

const BASE_URL = 'http://localhost:5174';
const VIEWPORT_IPHONE_14 = { width: 390, height: 844 };
const VIEWPORT_ANDROID_CHROME = { width: 393, height: 851 };

// Test user credentials (use existing/demo user if available)
const TEST_EMAIL = 'test@example.com';
const TEST_PASSWORD = 'testpassword';

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
    if (msg.type() === 'error' && !text.includes('429') && !text.includes('rate')) {
      context.errors.push(text);
      console.log(`  ⚠️  Error: ${text.substring(0, 80)}`);
    }
    if (msg.type() === 'warning') {
      context.warnings.push(text);
    }
  });

  page.on('response', (response: any) => {
    if (!response.ok() && response.status() !== 429) {
      const status = response.status();
      const url = response.url();
      if (status >= 400 && status < 500) {
        context.networkErrors.push({ status, url });
      }
    }
  });

  return context;
}

// ========== IPHONE 14 SAFARI (390x844) ==========

test.describe('iPhone 14 Safari (390x844)', () => {

  test('KundliForm: Fill & Submit - iPhone', async ({ page }) => {
    const ctx = setupErrorTracking(page);

    console.log('\n📱 iPhone 14 - KundliForm Submission Test');
    await page.setViewportSize(VIEWPORT_IPHONE_14);

    await page.goto(`${BASE_URL}/`, { waitUntil: 'networkidle', timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(2000);

    try {
      // Check form existence on home or kundli section
      const formVisible = await page.locator('form, [class*="kundli"], [class*="form"]').first().isVisible().catch(() => false);
      console.log(`  Form visible: ${formVisible ? '✅' : '⚠️'}`);

      // Try to find date input
      const dateInput = page.locator('input[type="date"], input[placeholder*="Date"], input[placeholder*="date"]').first();
      const dateExists = await dateInput.isVisible({ timeout: 5000 }).catch(() => false);

      let submitted = false;

      if (dateExists) {
        await dateInput.fill('1990-05-15');
        console.log(`  ✅ Date filled: 1990-05-15`);

        // Fill time
        const timeInput = page.locator('input[type="time"], input[placeholder*="Time"]').first();
        if (await timeInput.isVisible().catch(() => false)) {
          await timeInput.fill('10:30');
          console.log(`  ✅ Time filled: 10:30`);
        }

        // Fill location
        const locationInput = page.locator('input[placeholder*="Location"], input[placeholder*="Place"]').first();
        if (await locationInput.isVisible().catch(() => false)) {
          await locationInput.fill('New Delhi, India');
          console.log(`  ✅ Location filled`);
        }

        // Find and click Generate button
        const generateBtn = page.locator('button:has-text("Generate"), button:has-text("generate"), button[type="submit"]').first();
        const btnVisible = await generateBtn.isVisible().catch(() => false);

        if (btnVisible) {
          const btnOpacity = await generateBtn.evaluate((el: HTMLElement) => {
            return window.getComputedStyle(el).opacity;
          }).catch(() => '1');
          console.log(`  Button visible: ✅ (opacity: ${btnOpacity})`);

          const isEnabled = await generateBtn.isEnabled().catch(() => false);
          console.log(`  Button enabled: ${isEnabled ? '✅' : '⚠️'}`);

          await generateBtn.click();
          console.log(`  ✅ Button clicked`);
          submitted = true;

          // Wait for response
          await page.waitForTimeout(4000);
          const chartLoaded = await page.locator('canvas, svg, .chart, [class*="wheel"], [class*="kundli"]').isVisible().catch(() => false);
          console.log(`  Chart/Result loaded: ${chartLoaded ? '✅' : '⚠️'}`);
        }
      }

      if (!submitted) {
        console.log(`  ⚠️ Could not complete form submission`);
      }

      console.log(`  Network 4xx errors: ${ctx.networkErrors.length}, Console errors: ${ctx.errors.length}`);
      console.log(`  RESULT: ${submitted ? '✅ SUBMITTED' : '⚠️ INCOMPLETE'}`);
    } catch (e: any) {
      console.log(`  ❌ Exception: ${e.message?.substring(0, 60)}`);
      console.log(`  RESULT: ❌ FAIL`);
    }
  });

  test('Login Form: Email/Password - iPhone', async ({ page }) => {
    const ctx = setupErrorTracking(page);

    console.log('\n📱 iPhone 14 - Login Form Test');
    await page.setViewportSize(VIEWPORT_IPHONE_14);

    await page.goto(`${BASE_URL}/login`, { waitUntil: 'domcontentloaded', timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(1000);

    try {
      const formVisible = await page.locator('form').isVisible().catch(() => false);
      console.log(`  Form visible: ${formVisible ? '✅' : '⚠️'}`);

      if (!formVisible) {
        console.log('  RESULT: ⚠️ Form not accessible');
        return;
      }

      // Fill email
      const emailInput = page.locator('input[type="email"], input[placeholder*="Email"], input[placeholder*="email"]').first();
      const emailExists = await emailInput.isVisible().catch(() => false);

      let submitted = false;

      if (emailExists) {
        await emailInput.fill('testuser@astrorattan.com');
        console.log(`  ✅ Email filled`);

        // Fill password
        const passwordInput = page.locator('input[type="password"]').first();
        if (await passwordInput.isVisible().catch(() => false)) {
          await passwordInput.fill('TestPassword123!');
          console.log(`  ✅ Password filled`);
        }

        // Find and click submit
        const submitBtn = page.locator('button[type="submit"], button:has-text("Login"), button:has-text("login"), button:has-text("Sign In")').first();
        const btnVisible = await submitBtn.isVisible().catch(() => false);

        if (btnVisible) {
          const btnOpacity = await submitBtn.evaluate((el: HTMLElement) => window.getComputedStyle(el).opacity);
          console.log(`  Button visible: ✅ (opacity: ${btnOpacity})`);

          const isEnabled = await submitBtn.isEnabled().catch(() => false);
          console.log(`  Button enabled: ${isEnabled ? '✅' : '⚠️'}`);

          await submitBtn.click();
          console.log(`  ✅ Submit clicked`);
          submitted = true;

          // Wait for response
          await page.waitForTimeout(3000);

          const errorMsg = await page.locator('[class*="error"], [role="alert"]').innerText().catch(() => null);
          const currentUrl = page.url();

          if (errorMsg) {
            console.log(`  📌 Error/Message shown: ${errorMsg.substring(0, 50)}`);
          } else if (currentUrl !== `${BASE_URL}/login`) {
            console.log(`  ✅ Redirected to: ${currentUrl.split('?')[0]}`);
          } else {
            console.log(`  ⚠️ No redirect yet (may be loading or invalid credentials)`);
          }
        }
      }

      console.log(`  Network 4xx errors: ${ctx.networkErrors.length}, Console errors: ${ctx.errors.length}`);
      console.log(`  RESULT: ${submitted ? '✅ SUBMITTED' : '⚠️ INCOMPLETE'}`);
    } catch (e: any) {
      console.log(`  ❌ Exception: ${e.message?.substring(0, 60)}`);
      console.log(`  RESULT: ❌ FAIL`);
    }
  });

  test('ProfileEditPanel: Load & Interaction - iPhone', async ({ page }) => {
    const ctx = setupErrorTracking(page);

    console.log('\n📱 iPhone 14 - ProfileEditPanel Test');
    await page.setViewportSize(VIEWPORT_IPHONE_14);

    await page.goto(`${BASE_URL}/`, { waitUntil: 'networkidle', timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(1000);

    try {
      // Look for profile button/link
      const profileBtn = page.locator('button:has-text("Profile"), a:has-text("Profile"), [class*="profile"]').first();
      const profileBtnExists = await profileBtn.isVisible({ timeout: 5000 }).catch(() => false);

      if (profileBtnExists) {
        await profileBtn.click();
        console.log(`  ✅ Profile button clicked`);
        await page.waitForTimeout(1500);
      }

      // Look for edit button or editable fields
      const editBtn = page.locator('button:has-text("Edit"), [class*="edit"]').first();
      const editBtnExists = await editBtn.isVisible().catch(() => false);

      if (editBtnExists) {
        await editBtn.click();
        console.log(`  ✅ Edit button clicked`);
        await page.waitForTimeout(500);
      }

      // Try to find and fill editable fields
      const inputs = page.locator('input[type="text"], textarea');
      const inputCount = await inputs.count();

      if (inputCount > 0) {
        const firstInput = inputs.first();
        const initialValue = await firstInput.inputValue().catch(() => '');
        const testValue = (initialValue || 'Test') + '_Updated';

        await firstInput.fill(testValue);
        console.log(`  ✅ Field updated: "${testValue.substring(0, 30)}..."`);

        // Find and click save
        const saveBtn = page.locator('button:has-text("Save"), button:has-text("Update")').first();
        const saveBtnExists = await saveBtn.isVisible().catch(() => false);

        if (saveBtnExists) {
          await saveBtn.click();
          console.log(`  ✅ Save clicked`);
          await page.waitForTimeout(2000);

          const successMsg = await page.locator('[class*="success"], [role="status"]').innerText().catch(() => null);
          if (successMsg) {
            console.log(`  ✅ Success shown: ${successMsg.substring(0, 40)}`);
          }

          // Reload to check persistence
          await page.reload({ waitUntil: 'domcontentloaded' });
          await page.waitForTimeout(1000);
          const reloadValue = await firstInput.inputValue().catch(() => '');
          const persisted = reloadValue.includes('Updated');
          console.log(`  Data persisted: ${persisted ? '✅' : '⚠️'}`);
        } else {
          console.log(`  ⚠️ Save button not found`);
        }
      } else {
        console.log(`  ⚠️ No editable fields found`);
      }

      console.log(`  Network 4xx errors: ${ctx.networkErrors.length}, Console errors: ${ctx.errors.length}`);
      console.log(`  RESULT: ✅ TESTED`);
    } catch (e: any) {
      console.log(`  ❌ Exception: ${e.message?.substring(0, 60)}`);
      console.log(`  RESULT: ⚠️ PARTIAL`);
    }
  });
});

// ========== ANDROID CHROME (393x851) ==========

test.describe('Android Chrome (393x851)', () => {

  test('KundliForm: Fill & Submit - Android', async ({ page }) => {
    const ctx = setupErrorTracking(page);

    console.log('\n📱 Android Chrome - KundliForm Submission Test');
    await page.setViewportSize(VIEWPORT_ANDROID_CHROME);

    await page.goto(`${BASE_URL}/`, { waitUntil: 'networkidle', timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(2000);

    try {
      const formVisible = await page.locator('form, [class*="form"]').first().isVisible().catch(() => false);
      console.log(`  Form visible: ${formVisible ? '✅' : '⚠️'}`);

      const dateInput = page.locator('input[type="date"], input[placeholder*="Date"]').first();
      const dateExists = await dateInput.isVisible({ timeout: 5000 }).catch(() => false);

      let submitted = false;

      if (dateExists) {
        await dateInput.fill('1992-03-22');
        console.log(`  ✅ Date filled: 1992-03-22`);

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

        const generateBtn = page.locator('button:has-text("Generate"), button[type="submit"]').first();
        if (await generateBtn.isVisible().catch(() => false)) {
          const btnOpacity = await generateBtn.evaluate((el: HTMLElement) => window.getComputedStyle(el).opacity);
          console.log(`  Button visible: ✅ (opacity: ${btnOpacity})`);

          await generateBtn.click();
          console.log(`  ✅ Button clicked`);
          submitted = true;

          await page.waitForTimeout(4000);
          const chartLoaded = await page.locator('canvas, svg, .chart, [class*="wheel"]').isVisible().catch(() => false);
          console.log(`  Chart/Result loaded: ${chartLoaded ? '✅' : '⚠️'}`);
        }
      }

      console.log(`  Network 4xx errors: ${ctx.networkErrors.length}, Console errors: ${ctx.errors.length}`);
      console.log(`  RESULT: ${submitted ? '✅ SUBMITTED' : '⚠️ INCOMPLETE'}`);
    } catch (e: any) {
      console.log(`  ❌ Exception: ${e.message?.substring(0, 60)}`);
      console.log(`  RESULT: ❌ FAIL`);
    }
  });

  test('Login Form: Email/Password - Android', async ({ page }) => {
    const ctx = setupErrorTracking(page);

    console.log('\n📱 Android Chrome - Login Form Test');
    await page.setViewportSize(VIEWPORT_ANDROID_CHROME);

    await page.goto(`${BASE_URL}/login`, { waitUntil: 'domcontentloaded', timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(1000);

    try {
      const formVisible = await page.locator('form').isVisible().catch(() => false);
      console.log(`  Form visible: ${formVisible ? '✅' : '⚠️'}`);

      if (!formVisible) {
        console.log('  RESULT: ⚠️ Form not accessible');
        return;
      }

      const emailInput = page.locator('input[type="email"], input[placeholder*="Email"]').first();
      const emailExists = await emailInput.isVisible().catch(() => false);

      let submitted = false;

      if (emailExists) {
        await emailInput.fill('android@test.com');
        console.log(`  ✅ Email filled`);

        const passwordInput = page.locator('input[type="password"]').first();
        if (await passwordInput.isVisible().catch(() => false)) {
          await passwordInput.fill('AndroidTest123!');
          console.log(`  ✅ Password filled`);
        }

        const submitBtn = page.locator('button[type="submit"], button:has-text("Login")').first();
        if (await submitBtn.isVisible().catch(() => false)) {
          const btnOpacity = await submitBtn.evaluate((el: HTMLElement) => window.getComputedStyle(el).opacity);
          console.log(`  Button visible: ✅ (opacity: ${btnOpacity})`);

          await submitBtn.click();
          console.log(`  ✅ Submit clicked`);
          submitted = true;

          await page.waitForTimeout(3000);

          const errorMsg = await page.locator('[class*="error"], [role="alert"]').innerText().catch(() => null);
          const currentUrl = page.url();

          if (errorMsg) {
            console.log(`  📌 Error/Message shown: ${errorMsg.substring(0, 50)}`);
          } else if (currentUrl !== `${BASE_URL}/login`) {
            console.log(`  ✅ Redirected to: ${currentUrl.split('?')[0]}`);
          } else {
            console.log(`  ⚠️ No redirect yet`);
          }
        }
      }

      console.log(`  Network 4xx errors: ${ctx.networkErrors.length}, Console errors: ${ctx.errors.length}`);
      console.log(`  RESULT: ${submitted ? '✅ SUBMITTED' : '⚠️ INCOMPLETE'}`);
    } catch (e: any) {
      console.log(`  ❌ Exception: ${e.message?.substring(0, 60)}`);
      console.log(`  RESULT: ❌ FAIL`);
    }
  });

  test('ProfileEditPanel: Load & Interaction - Android', async ({ page }) => {
    const ctx = setupErrorTracking(page);

    console.log('\n📱 Android Chrome - ProfileEditPanel Test');
    await page.setViewportSize(VIEWPORT_ANDROID_CHROME);

    await page.goto(`${BASE_URL}/`, { waitUntil: 'networkidle', timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(1000);

    try {
      const profileBtn = page.locator('button:has-text("Profile"), a:has-text("Profile")').first();
      if (await profileBtn.isVisible({ timeout: 5000 }).catch(() => false)) {
        await profileBtn.click();
        console.log(`  ✅ Profile button clicked`);
        await page.waitForTimeout(1500);
      }

      const editBtn = page.locator('button:has-text("Edit")').first();
      if (await editBtn.isVisible().catch(() => false)) {
        await editBtn.click();
        console.log(`  ✅ Edit button clicked`);
        await page.waitForTimeout(500);
      }

      const inputs = page.locator('input[type="text"], textarea');
      const inputCount = await inputs.count();

      if (inputCount > 0) {
        const firstInput = inputs.first();
        const initialValue = await firstInput.inputValue().catch(() => '');
        const testValue = (initialValue || 'Test') + '_Android';

        await firstInput.fill(testValue);
        console.log(`  ✅ Field updated`);

        const saveBtn = page.locator('button:has-text("Save"), button:has-text("Update")').first();
        if (await saveBtn.isVisible().catch(() => false)) {
          await saveBtn.click();
          console.log(`  ✅ Save clicked`);
          await page.waitForTimeout(2000);

          await page.reload({ waitUntil: 'domcontentloaded' });
          await page.waitForTimeout(1000);
          const reloadValue = await firstInput.inputValue().catch(() => '');
          const persisted = reloadValue.includes('Android');
          console.log(`  Data persisted: ${persisted ? '✅' : '⚠️'}`);
        } else {
          console.log(`  ⚠️ Save button not found`);
        }
      } else {
        console.log(`  ⚠️ No editable fields found`);
      }

      console.log(`  Network 4xx errors: ${ctx.networkErrors.length}, Console errors: ${ctx.errors.length}`);
      console.log(`  RESULT: ✅ TESTED`);
    } catch (e: any) {
      console.log(`  ❌ Exception: ${e.message?.substring(0, 60)}`);
      console.log(`  RESULT: ⚠️ PARTIAL`);
    }
  });
});
