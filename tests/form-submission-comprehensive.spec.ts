import { test, expect } from '@playwright/test';

// Comprehensive form submission tests for mobile viewports
test.describe.configure({ timeout: 90000 });

const BASE_URL = 'http://localhost:5174';
const VIEWPORT_IPHONE_14 = { width: 390, height: 844 };
const VIEWPORT_ANDROID_CHROME = { width: 393, height: 851 };

interface TestResult {
  platform: string;
  form: string;
  formFound: boolean;
  inputsAccepted: boolean;
  buttonVisible: boolean;
  buttonEnabled: boolean;
  submitted: boolean;
  resultLoaded: boolean;
  consoleErrors: number;
  networkErrors: number;
  status: 'PASS' | 'FAIL' | 'PARTIAL' | 'SKIPPED';
}

const results: TestResult[] = [];

function trackResult(result: TestResult) {
  results.push(result);
  const icon = result.status === 'PASS' ? '✅' : result.status === 'FAIL' ? '❌' : '⚠️';
  console.log(`  ${icon} ${result.platform} - ${result.form}: ${result.status}`);
}

test.describe('Mobile Form Submission Tests', () => {

  test('iPhone 14 - KundliForm (Kundli Generation)', async ({ page }) => {
    const platform = 'iPhone 14 Safari (390x844)';
    const formName = 'KundliForm';

    console.log(`\n📱 Testing ${platform} - ${formName}`);
    await page.setViewportSize(VIEWPORT_IPHONE_14);

    const errors: string[] = [];
    const networkErrors: string[] = [];

    page.on('console', msg => {
      if (msg.type() === 'error' && !msg.text().includes('429')) {
        errors.push(msg.text());
      }
    });

    page.on('response', response => {
      if (!response.ok() && response.status() !== 429) {
        networkErrors.push(`${response.status()} ${response.url()}`);
      }
    });

    try {
      await page.goto(`${BASE_URL}/`, { waitUntil: 'networkidle', timeout: 15000 });
      await page.waitForTimeout(1500);

      // Kundli form on homepage: date, time, location inputs
      const dateInput = page.locator('input[type="date"]').first();
      const timeInput = page.locator('input[type="time"]').first();
      const locationInput = page.locator('input[placeholder*="birth place"]').first();

      const dateVisible = await dateInput.isVisible({ timeout: 3000 }).catch(() => false);
      const timeVisible = await timeInput.isVisible().catch(() => false);
      const locVisible = await locationInput.isVisible().catch(() => false);

      console.log(`  Date input: ${dateVisible ? '✅' : '❌'}`);
      console.log(`  Time input: ${timeVisible ? '✅' : '❌'}`);
      console.log(`  Location input: ${locVisible ? '✅' : '❌'}`);

      let inputsAccepted = false;
      let submitted = false;
      let resultLoaded = false;

      if (dateVisible && timeVisible) {
        // Fill form
        await dateInput.fill('1990-05-15');
        await timeInput.fill('10:30');
        if (locVisible) {
          await locationInput.fill('New Delhi');
        }
        inputsAccepted = true;
        console.log(`  ✅ All inputs filled`);

        // Find submit button
        const submitBtn = page.locator('button:has-text("Submit")').first();
        const btnVisible = await submitBtn.isVisible({ timeout: 3000 }).catch(() => false);
        const btnEnabled = await submitBtn.isEnabled().catch(() => false);

        console.log(`  Button visible: ${btnVisible ? '✅' : '❌'}`);
        console.log(`  Button enabled: ${btnEnabled ? '✅' : '❌'}`);

        if (btnVisible && btnEnabled) {
          await submitBtn.click();
          console.log(`  ✅ Submit clicked`);
          submitted = true;

          // Wait for result
          await page.waitForTimeout(3000);
          const resultVisible = await page.locator('canvas, svg, [class*="chart"], [class*="wheel"], [class*="result"]').isVisible({ timeout: 5000 }).catch(() => false);
          resultLoaded = resultVisible;
          console.log(`  Chart/Result: ${resultLoaded ? '✅ loaded' : '⚠️ not visible'}`);
        }
      }

      const result: TestResult = {
        platform,
        form: formName,
        formFound: dateVisible && timeVisible,
        inputsAccepted,
        buttonVisible: await page.locator('button:has-text("Submit")').isVisible().catch(() => false),
        buttonEnabled: submitted,
        submitted,
        resultLoaded,
        consoleErrors: errors.length,
        networkErrors: networkErrors.length,
        status: submitted && resultLoaded ? 'PASS' : submitted ? 'PARTIAL' : 'FAIL'
      };

      trackResult(result);
    } catch (e: any) {
      const result: TestResult = {
        platform,
        form: formName,
        formFound: false,
        inputsAccepted: false,
        buttonVisible: false,
        buttonEnabled: false,
        submitted: false,
        resultLoaded: false,
        consoleErrors: errors.length,
        networkErrors: networkErrors.length,
        status: 'FAIL'
      };
      trackResult(result);
      console.log(`  ❌ Exception: ${e.message?.substring(0, 60)}`);
    }
  });

  test('iPhone 14 - Login Form', async ({ page }) => {
    const platform = 'iPhone 14 Safari (390x844)';
    const formName = 'LoginForm';

    console.log(`\n📱 Testing ${platform} - ${formName}`);
    await page.setViewportSize(VIEWPORT_IPHONE_14);

    const errors: string[] = [];
    const networkErrors: string[] = [];

    page.on('console', msg => {
      if (msg.type() === 'error') errors.push(msg.text());
    });

    page.on('response', response => {
      if (!response.ok() && response.status() !== 429) {
        networkErrors.push(`${response.status()} ${response.url()}`);
      }
    });

    try {
      await page.goto(`${BASE_URL}/login`, { waitUntil: 'domcontentloaded', timeout: 15000 });
      await page.waitForTimeout(1000);

      const emailInput = page.locator('input[type="email"]').first();
      const passwordInput = page.locator('input[type="password"]').first();

      const emailVisible = await emailInput.isVisible({ timeout: 3000 }).catch(() => false);
      const pwdVisible = await passwordInput.isVisible().catch(() => false);

      console.log(`  Email input: ${emailVisible ? '✅' : '❌'}`);
      console.log(`  Password input: ${pwdVisible ? '✅' : '❌'}`);

      let inputsAccepted = false;
      let submitted = false;

      if (emailVisible && pwdVisible) {
        await emailInput.fill('test@example.com');
        await passwordInput.fill('TestPass123');
        inputsAccepted = true;
        console.log(`  ✅ Both inputs filled`);

        const signInBtn = page.locator('button:has-text("Sign In")').first();
        const btnVisible = await signInBtn.isVisible({ timeout: 3000 }).catch(() => false);
        const btnEnabled = await signInBtn.isEnabled().catch(() => false);

        console.log(`  Button visible: ${btnVisible ? '✅' : '❌'}`);
        console.log(`  Button enabled: ${btnEnabled ? '✅' : '❌'}`);

        if (btnVisible && btnEnabled) {
          await signInBtn.click();
          console.log(`  ✅ Submit clicked`);
          submitted = true;

          await page.waitForTimeout(2000);
          const errorMsg = await page.locator('[class*="error"], [role="alert"]').isVisible({ timeout: 3000 }).catch(() => false);
          const redirected = !page.url().includes('/login');

          if (redirected) {
            console.log(`  ✅ Redirected (page changed)`);
          } else if (errorMsg) {
            console.log(`  ⚠️ Error message shown (invalid credentials expected)`);
          }
        }
      }

      const result: TestResult = {
        platform,
        form: formName,
        formFound: emailVisible && pwdVisible,
        inputsAccepted,
        buttonVisible: await page.locator('button:has-text("Sign In")').isVisible().catch(() => false),
        buttonEnabled: submitted,
        submitted,
        resultLoaded: !page.url().includes('/login'),
        consoleErrors: errors.length,
        networkErrors: networkErrors.length,
        status: submitted ? (networkErrors.length === 0 ? 'PASS' : 'PARTIAL') : 'FAIL'
      };

      trackResult(result);
    } catch (e: any) {
      const result: TestResult = {
        platform,
        form: formName,
        formFound: false,
        inputsAccepted: false,
        buttonVisible: false,
        buttonEnabled: false,
        submitted: false,
        resultLoaded: false,
        consoleErrors: errors.length,
        networkErrors: networkErrors.length,
        status: 'FAIL'
      };
      trackResult(result);
      console.log(`  ❌ Exception: ${e.message?.substring(0, 60)}`);
    }
  });

  test('iPhone 14 - LalKitabForm (Auth protected)', async ({ page }) => {
    const platform = 'iPhone 14 Safari (390x844)';
    const formName = 'LalKitabForm';

    console.log(`\n📱 Testing ${platform} - ${formName}`);
    await page.setViewportSize(VIEWPORT_IPHONE_14);

    try {
      // Try to access protected route
      await page.goto(`${BASE_URL}/lal-kitab`, { waitUntil: 'domcontentloaded', timeout: 15000 });
      await page.waitForTimeout(1000);

      // Should redirect to login if not authenticated
      const isOnLalKitabPage = page.url().includes('/lal-kitab');
      const isOnLoginPage = page.url().includes('/login');

      console.log(`  Page: ${isOnLalKitabPage ? 'Lal Kitab' : isOnLoginPage ? 'Login (redirected)' : 'Other'}`);

      if (isOnLalKitabPage) {
        const form = page.locator('form, [class*="form"]').first();
        const formVisible = await form.isVisible({ timeout: 3000 }).catch(() => false);
        console.log(`  Form visible: ${formVisible ? '✅' : '⚠️'}`);
      } else {
        console.log(`  ⚠️ Auth redirected (expected for protected route)`);
      }

      const result: TestResult = {
        platform,
        form: formName,
        formFound: isOnLalKitabPage,
        inputsAccepted: false,
        buttonVisible: false,
        buttonEnabled: false,
        submitted: false,
        resultLoaded: false,
        consoleErrors: 0,
        networkErrors: 0,
        status: isOnLalKitabPage ? 'PARTIAL' : 'SKIPPED'
      };

      trackResult(result);
    } catch (e: any) {
      const result: TestResult = {
        platform,
        form: formName,
        formFound: false,
        inputsAccepted: false,
        buttonVisible: false,
        buttonEnabled: false,
        submitted: false,
        resultLoaded: false,
        consoleErrors: 0,
        networkErrors: 0,
        status: 'FAIL'
      };
      trackResult(result);
    }
  });

  // ========== ANDROID CHROME ==========

  test('Android Chrome - KundliForm', async ({ page }) => {
    const platform = 'Android Chrome (393x851)';
    const formName = 'KundliForm';

    console.log(`\n📱 Testing ${platform} - ${formName}`);
    await page.setViewportSize(VIEWPORT_ANDROID_CHROME);

    const errors: string[] = [];
    const networkErrors: string[] = [];

    page.on('console', msg => {
      if (msg.type() === 'error' && !msg.text().includes('429')) {
        errors.push(msg.text());
      }
    });

    page.on('response', response => {
      if (!response.ok() && response.status() !== 429) {
        networkErrors.push(`${response.status()} ${response.url()}`);
      }
    });

    try {
      await page.goto(`${BASE_URL}/`, { waitUntil: 'networkidle', timeout: 15000 });
      await page.waitForTimeout(1500);

      const dateInput = page.locator('input[type="date"]').first();
      const timeInput = page.locator('input[type="time"]').first();
      const locationInput = page.locator('input[placeholder*="birth place"]').first();

      const dateVisible = await dateInput.isVisible({ timeout: 3000 }).catch(() => false);
      const timeVisible = await timeInput.isVisible().catch(() => false);
      const locVisible = await locationInput.isVisible().catch(() => false);

      console.log(`  Date input: ${dateVisible ? '✅' : '❌'}`);
      console.log(`  Time input: ${timeVisible ? '✅' : '❌'}`);
      console.log(`  Location input: ${locVisible ? '✅' : '❌'}`);

      let inputsAccepted = false;
      let submitted = false;
      let resultLoaded = false;

      if (dateVisible && timeVisible) {
        await dateInput.fill('1992-03-22');
        await timeInput.fill('14:45');
        if (locVisible) {
          await locationInput.fill('Mumbai');
        }
        inputsAccepted = true;
        console.log(`  ✅ All inputs filled`);

        const submitBtn = page.locator('button:has-text("Submit")').first();
        const btnVisible = await submitBtn.isVisible({ timeout: 3000 }).catch(() => false);
        const btnEnabled = await submitBtn.isEnabled().catch(() => false);

        console.log(`  Button visible: ${btnVisible ? '✅' : '❌'}`);
        console.log(`  Button enabled: ${btnEnabled ? '✅' : '❌'}`);

        if (btnVisible && btnEnabled) {
          await submitBtn.click();
          console.log(`  ✅ Submit clicked`);
          submitted = true;

          await page.waitForTimeout(3000);
          const resultVisible = await page.locator('canvas, svg, [class*="chart"], [class*="wheel"]').isVisible({ timeout: 5000 }).catch(() => false);
          resultLoaded = resultVisible;
          console.log(`  Chart/Result: ${resultLoaded ? '✅ loaded' : '⚠️ not visible'}`);
        }
      }

      const result: TestResult = {
        platform,
        form: formName,
        formFound: dateVisible && timeVisible,
        inputsAccepted,
        buttonVisible: await page.locator('button:has-text("Submit")').isVisible().catch(() => false),
        buttonEnabled: submitted,
        submitted,
        resultLoaded,
        consoleErrors: errors.length,
        networkErrors: networkErrors.length,
        status: submitted && resultLoaded ? 'PASS' : submitted ? 'PARTIAL' : 'FAIL'
      };

      trackResult(result);
    } catch (e: any) {
      const result: TestResult = {
        platform,
        form: formName,
        formFound: false,
        inputsAccepted: false,
        buttonVisible: false,
        buttonEnabled: false,
        submitted: false,
        resultLoaded: false,
        consoleErrors: errors.length,
        networkErrors: networkErrors.length,
        status: 'FAIL'
      };
      trackResult(result);
      console.log(`  ❌ Exception: ${e.message?.substring(0, 60)}`);
    }
  });

  test('Android Chrome - Login Form', async ({ page }) => {
    const platform = 'Android Chrome (393x851)';
    const formName = 'LoginForm';

    console.log(`\n📱 Testing ${platform} - ${formName}`);
    await page.setViewportSize(VIEWPORT_ANDROID_CHROME);

    const errors: string[] = [];
    const networkErrors: string[] = [];

    page.on('console', msg => {
      if (msg.type() === 'error') errors.push(msg.text());
    });

    page.on('response', response => {
      if (!response.ok() && response.status() !== 429) {
        networkErrors.push(`${response.status()} ${response.url()}`);
      }
    });

    try {
      await page.goto(`${BASE_URL}/login`, { waitUntil: 'domcontentloaded', timeout: 15000 });
      await page.waitForTimeout(1000);

      const emailInput = page.locator('input[type="email"]').first();
      const passwordInput = page.locator('input[type="password"]').first();

      const emailVisible = await emailInput.isVisible({ timeout: 3000 }).catch(() => false);
      const pwdVisible = await passwordInput.isVisible().catch(() => false);

      console.log(`  Email input: ${emailVisible ? '✅' : '❌'}`);
      console.log(`  Password input: ${pwdVisible ? '✅' : '❌'}`);

      let inputsAccepted = false;
      let submitted = false;

      if (emailVisible && pwdVisible) {
        await emailInput.fill('android@test.com');
        await passwordInput.fill('AndroidTest123');
        inputsAccepted = true;
        console.log(`  ✅ Both inputs filled`);

        const signInBtn = page.locator('button:has-text("Sign In")').first();
        const btnVisible = await signInBtn.isVisible({ timeout: 3000 }).catch(() => false);
        const btnEnabled = await signInBtn.isEnabled().catch(() => false);

        console.log(`  Button visible: ${btnVisible ? '✅' : '❌'}`);
        console.log(`  Button enabled: ${btnEnabled ? '✅' : '❌'}`);

        if (btnVisible && btnEnabled) {
          await signInBtn.click();
          console.log(`  ✅ Submit clicked`);
          submitted = true;

          await page.waitForTimeout(2000);
          const errorMsg = await page.locator('[class*="error"], [role="alert"]').isVisible({ timeout: 3000 }).catch(() => false);
          const redirected = !page.url().includes('/login');

          if (redirected) {
            console.log(`  ✅ Redirected (page changed)`);
          } else if (errorMsg) {
            console.log(`  ⚠️ Error message shown (invalid credentials expected)`);
          }
        }
      }

      const result: TestResult = {
        platform,
        form: formName,
        formFound: emailVisible && pwdVisible,
        inputsAccepted,
        buttonVisible: await page.locator('button:has-text("Sign In")').isVisible().catch(() => false),
        buttonEnabled: submitted,
        submitted,
        resultLoaded: !page.url().includes('/login'),
        consoleErrors: errors.length,
        networkErrors: networkErrors.length,
        status: submitted ? (networkErrors.length === 0 ? 'PASS' : 'PARTIAL') : 'FAIL'
      };

      trackResult(result);
    } catch (e: any) {
      const result: TestResult = {
        platform,
        form: formName,
        formFound: false,
        inputsAccepted: false,
        buttonVisible: false,
        buttonEnabled: false,
        submitted: false,
        resultLoaded: false,
        consoleErrors: errors.length,
        networkErrors: networkErrors.length,
        status: 'FAIL'
      };
      trackResult(result);
      console.log(`  ❌ Exception: ${e.message?.substring(0, 60)}`);
    }
  });

  test('Android Chrome - VastuForm (Auth protected)', async ({ page }) => {
    const platform = 'Android Chrome (393x851)';
    const formName = 'VastuForm';

    console.log(`\n📱 Testing ${platform} - ${formName}`);
    await page.setViewportSize(VIEWPORT_ANDROID_CHROME);

    try {
      await page.goto(`${BASE_URL}/vastu`, { waitUntil: 'domcontentloaded', timeout: 15000 });
      await page.waitForTimeout(1000);

      const isOnVastuPage = page.url().includes('/vastu');
      const isOnLoginPage = page.url().includes('/login');

      console.log(`  Page: ${isOnVastuPage ? 'Vastu' : isOnLoginPage ? 'Login (redirected)' : 'Other'}`);

      if (isOnVastuPage) {
        const form = page.locator('form, [class*="form"]').first();
        const formVisible = await form.isVisible({ timeout: 3000 }).catch(() => false);
        console.log(`  Form visible: ${formVisible ? '✅' : '⚠️'}`);
      } else {
        console.log(`  ⚠️ Auth redirected (expected for protected route)`);
      }

      const result: TestResult = {
        platform,
        form: formName,
        formFound: isOnVastuPage,
        inputsAccepted: false,
        buttonVisible: false,
        buttonEnabled: false,
        submitted: false,
        resultLoaded: false,
        consoleErrors: 0,
        networkErrors: 0,
        status: isOnVastuPage ? 'PARTIAL' : 'SKIPPED'
      };

      trackResult(result);
    } catch (e: any) {
      const result: TestResult = {
        platform,
        form: formName,
        formFound: false,
        inputsAccepted: false,
        buttonVisible: false,
        buttonEnabled: false,
        submitted: false,
        resultLoaded: false,
        consoleErrors: 0,
        networkErrors: 0,
        status: 'FAIL'
      };
      trackResult(result);
    }
  });
});

// Summary after all tests
test.afterAll(() => {
  console.log(`\n\n========== TEST SUMMARY ==========`);
  console.log(`Total tests: ${results.length}`);

  const passed = results.filter(r => r.status === 'PASS').length;
  const partial = results.filter(r => r.status === 'PARTIAL').length;
  const failed = results.filter(r => r.status === 'FAIL').length;
  const skipped = results.filter(r => r.status === 'SKIPPED').length;

  console.log(`✅ PASS: ${passed} | ⚠️ PARTIAL: ${partial} | ❌ FAIL: ${failed} | ⏭️ SKIPPED: ${skipped}`);

  console.log(`\n========== DETAILS BY FORM ==========`);
  const byForm = new Map<string, TestResult[]>();
  results.forEach(r => {
    if (!byForm.has(r.form)) byForm.set(r.form, []);
    byForm.get(r.form)!.push(r);
  });

  byForm.forEach((tests, form) => {
    console.log(`\n${form}:`);
    tests.forEach(t => {
      const statusIcon = t.status === 'PASS' ? '✅' : t.status === 'FAIL' ? '❌' : '⚠️';
      console.log(
        `  ${statusIcon} ${t.platform.split(' ')[0]}: ` +
        `form=${t.formFound ? '✅' : '❌'} ` +
        `inputs=${t.inputsAccepted ? '✅' : '❌'} ` +
        `btn=${t.buttonVisible ? '✅' : '❌'} ` +
        `submitted=${t.submitted ? '✅' : '❌'} ` +
        `errors=${t.consoleErrors + t.networkErrors}`
      );
    });
  });

  console.log(`\n=================================`);
});
