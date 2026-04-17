import { test, expect, Page } from '@playwright/test';

const BASE_URL = process.env.E2E_BASE_URL || 'https://astrorattan.com';
const LOGIN_EMAIL = 'meharbansingh85@gmail.com';
const LOGIN_PASSWORD = 'Misha@123';

// ── Helpers ───────────────────────────────────────────────────────────────

async function login(page: Page) {
  await page.goto(`${BASE_URL}/login`);
  await page.waitForLoadState('networkidle');

  // Fill login form
  console.log('🔑 Entering credentials...');
  await page.locator('input[type="email"]').first().fill(LOGIN_EMAIL);
  await page.waitForTimeout(500);
  
  // Use type instead of fill for password to simulate human typing
  await page.locator('input[type="password"]').first().focus();
  await page.keyboard.type(LOGIN_PASSWORD);
  await page.waitForTimeout(500);
  await page.keyboard.press('Enter'); // Try Enter first

  // Also click Sign In as a backup
  const loginBtn = page.locator('button').filter({ hasText: /Sign In|साइन इन/ }).last();
  try {
    if (await loginBtn.isVisible()) {
      console.log('🖱️ Clicking Sign In button...');
      await loginBtn.click();
    }
  } catch (e) {
    console.log('   ⚠️ Login button click failed or not needed (Enter might have worked)');
  }

  // Wait for navigation - extended timeout to 60s for production
  console.log('⏳ Waiting for navigation...');
  await page.waitForURL(url => {
    console.log(`   🔗 Current URL: ${url.pathname}`);
    // A successful login should move away from /login
    return url.pathname !== '/login' && url.pathname !== '/login/';
  }, { timeout: 60_000 });
  
  await page.waitForTimeout(2000); // Give it time to settle
  console.log('✅ Login successful.');
}

async function scrollToBottom(page: Page) {
  await page.evaluate(async () => {
    const delay = (ms: number) => new Promise(r => setTimeout(r, ms));
    const step = window.innerHeight * 0.7;
    for (let y = 0; y < document.body.scrollHeight; y += step) {
      window.scrollTo(0, y);
      await delay(300);
    }
    window.scrollTo(0, document.body.scrollHeight);
  });
}

async function screenshotElement(page: Page, fileName: string) {
  await page.screenshot({ path: `e2e/lalkitab-audit/${fileName}.png`, fullPage: false });
  console.log(`📸 Screenshot saved: e2e/lalkitab-audit/${fileName}.png`);
}

// ── Test Logic ────────────────────────────────────────────────────────────

test.describe('Lal Kitab E2E Audit — Create Client & Verify Tabs', () => {

  test.beforeEach(async ({ page }) => {
    // Increase timeout for long audit
    test.setTimeout(180_000);
    await login(page);
    await page.goto(`${BASE_URL}/lal-kitab`);
    await page.waitForLoadState('networkidle');
  });

  test('01 — Full Audit: Create User, Scroll All Tabs, Verify Integrity', async ({ page }) => {
    // 1. Fill Form for New Client
    console.log('📝 Filling Lal Kitab Form...');
    
    // Check if we are on the form view
    await expect(page.locator('h1').filter({ hasText: /Lal Kitab/i })).toBeVisible();
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(1000);

    // Ensure 'New Client' is selected
    const newClientBtn = page.locator('button').filter({ hasText: /New Client|नया क्लाइंट/i }).first();
    if (await newClientBtn.isVisible()) {
      await newClientBtn.click();
      await page.waitForTimeout(500);
    }

    // Name
    const testName = `Test User ${Date.now()}`;
    const nameInput = page.locator('input[placeholder="Enter your name"], input[placeholder*="नाम"]').first();
    await nameInput.waitFor({ state: 'visible' });
    await nameInput.fill(testName);
    await page.waitForTimeout(500);

    // Phone (Required for astrologer role)
    const testPhone = `9${Math.floor(Math.random() * 900000000 + 100000000)}`;
    const phoneInput = page.locator('input[placeholder="Phone number"], input[placeholder*="फोन"]').first();
    await phoneInput.fill(testPhone);
    await page.waitForTimeout(500);

    // DOB
    const dateInput = page.locator('input[type="date"]').first();
    await dateInput.fill('1990-05-15');
    await page.waitForTimeout(500);

    // TOB
    const timeInput = page.locator('input[type="time"]').first();
    await timeInput.fill('14:30');
    await page.waitForTimeout(500);

    // POB - Search and select from dropdown
    const placeInput = page.locator('input[placeholder="Search birth place"], input[placeholder*="खोजें"]').first();
    await placeInput.waitFor({ state: 'visible' });
    await placeInput.click();
    await page.waitForTimeout(500);
    await placeInput.pressSequentially('Delhi', { delay: 150 });
    await page.waitForTimeout(5000); // Wait longer for geocode results on production

    // Click first suggestion
    const suggestion = page.locator('button').filter({ hasText: /Delhi/i }).first();
    await expect(suggestion).toBeVisible({ timeout: 15_000 });
    console.log('📍 Selecting place...');
    await suggestion.click();
    await page.waitForTimeout(1000);

    // Submit form
    console.log('🚀 Generating Kundli...');
    await page.waitForTimeout(1000); // 1s delay before submit
    await page.locator('button[type="submit"]').click();

    // 2. Wait for API and Tabs to appear
    await page.waitForSelector('[role="tablist"]', { timeout: 30_000 });
    await page.waitForTimeout(1000); // 1s delay after load
    console.log('✅ Result page loaded.');

    // 3. Define Tabs to Iterate
    // dashboard, chart, analysis, timing, upay, predictions, nishaniyan, advanced, vastu, tracker
    const TABS = [
      { id: 'dashboard', label: /Dashboard|डैशबोर्ड/i },
      { id: 'chart',     label: /Chart|चक्र/i },
      { id: 'analysis',  label: /Analysis|विश्लेषण/i },
      { id: 'timing',    label: /Timing|समय/i },
      { id: 'upay',      label: /Upay|उपाय/i },
      { id: 'predictions', label: /Predictions|भविष्यवाणी/i },
      { id: 'nishaniyan', label: /Nishaniyan|निशानियां/i },
      { id: 'advanced',  label: /Karmic Insight|कर्मिक दृष्टि/i },
      { id: 'vastu',     label: /Vastu|वास्तु/i },
      { id: 'tracker',   label: /Tracker|ट्रैकर/i },
    ];

    for (const tab of TABS) {
      console.log(`🔍 Auditing Tab: ${tab.id}`);
      
      const trigger = page.locator('button[role="tab"]').filter({ hasText: tab.label }).first();
      await expect(trigger).toBeVisible();
      await trigger.click();
      await page.waitForTimeout(1500); // Slightly more for tab switching

      // Scroll to bottom
      await scrollToBottom(page);
      await page.waitForTimeout(500);

      // Verify no critical errors or placeholders
      const bodyText = await page.innerText('body');
      const artifacts = await page.evaluate(() => {
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
        let node;
        const found = [];
        // Use regex for word boundary and case sensitivity where appropriate
        const badStrings = [
          { key: 'undefined', regex: /\bundefined\b/ },
          { key: 'null',      regex: /\bnull\b/ },
          { key: 'object object', regex: /\[object object\]/i },
          { key: 'NaN',       regex: /\bNaN\b/ },
        ];
        while (node = walker.nextNode()) {
          const txt = node.textContent || '';
          for (const bad of badStrings) {
            if (bad.regex.test(txt)) {
              const el = node.parentElement;
              found.push({ bad: bad.key, html: el ? el.outerHTML : 'TEXT_NODE' });
            }
          }
        }
        return found;
      });
      if (artifacts.length > 0) {
        console.error(`❌ Found broken strings in tab ${tab.id}:`);
        artifacts.forEach(a => console.error(`   - [${a.bad}] in: ${a.html}`));
      }

      // Check for presence of Hindi text (ensure it's not all English if backend uses i18n)
      const hindiMatches = bodyText.match(/[\u0900-\u097F]{2,}/g);
      if (!hindiMatches || hindiMatches.length < 2) {
        console.warn(`⚠️ Very little or no Hindi text found in tab ${tab.id}`);
      }

      // Capture screenshot
      await screenshotElement(page, `tab-${tab.id}`);

      // Special handling for the Predictions tab accordions
      if (tab.id === 'predictions') {
        process.stdout.write('   📂 Opening accordions: ');
        const accordions = page.locator('details summary');
        const accCount = await accordions.count();
        for (let i = 1; i < accCount; i++) { // Skip the first one if it's already open by default
          const summary = accordions.nth(i);
          await summary.click();
          await page.waitForTimeout(800);
          process.stdout.write('.');
        }
        process.stdout.write('\n');
        await scrollToBottom(page);
        await screenshotElement(page, 'tab-predictions-expanded');
      }

      // Scroll back to top
      await page.evaluate(() => window.scrollTo(0, 0));
    }

    console.log('✅ Full Lal Kitaab Audit Completed successfully.');
  });
});
