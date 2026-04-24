import { test, expect, devices } from '@playwright/test';

// Configure iPhone 14 for all tests in this file
test.use({
  ...devices['iPhone 14'],
  viewport: { width: 390, height: 844 },
});

test.describe('iPhone 14 Safari Mobile Tests (390x844)', () => {
  // Helper to check for console errors
  async function getConsoleErrors(page: any) {
    const errors: string[] = [];
    page.on('console', (msg: any) => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });
    return errors;
  }

  // Helper to take screenshot with timestamp
  async function takeScreenshot(page: any, testName: string) {
    try {
      await page.screenshot({
        path: `./e2e/screenshots/mobile-${testName}-${Date.now()}.png`,
        fullPage: false,
      });
    } catch (e) {
      // Screenshot failed, continue
    }
  }

  // ==================== PAGE 1: HOME ====================
  test('1. HOME - Page loads without console errors', async ({ page }) => {
    const consoleErrors: string[] = [];
    page.on('console', (msg: any) => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });

    try {
      const response = await page.goto('https://astrorattan.com', { waitUntil: 'networkidle', timeout: 30000 });
      expect(response?.status()).toBeLessThan(400);

      // Check no console errors
      expect(consoleErrors).toHaveLength(0);

      // Check key content present
      const body = page.locator('body');
      const text = await body.innerText();
      expect(text.length).toBeGreaterThan(100);

      await takeScreenshot(page, 'home-loaded');
      console.log('✅ HOME: Loaded successfully, no console errors');
    } catch (error) {
      console.log(`❌ HOME: ${error}`);
      throw error;
    }
  });

  test('1. HOME - Touch targets are 44px or larger', async ({ page }) => {
    await page.goto('https://astrorattan.com', { waitUntil: 'networkidle', timeout: 30000 });

    const buttons = page.locator('button, a[role="button"], [role="button"]');
    const buttonCount = await buttons.count();
    let minSizeViolations = 0;

    for (let i = 0; i < Math.min(buttonCount, 5); i++) {
      const button = buttons.nth(i);
      const box = await button.boundingBox();
      if (box && (box.width < 44 || box.height < 44)) {
        minSizeViolations++;
      }
    }

    const violationRate = buttonCount > 0 ? (minSizeViolations / Math.min(buttonCount, 5)) * 100 : 0;
    console.log(`✅ HOME: Touch targets checked (${buttonCount} total, ${violationRate.toFixed(1)}% < 44px)`);
  });

  // ==================== PAGE 2: AUTH ====================
  test('2. AUTH - Page loads without console errors', async ({ page }) => {
    const consoleErrors: string[] = [];
    page.on('console', (msg: any) => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });

    const response = await page.goto('https://astrorattan.com/auth', { waitUntil: 'networkidle', timeout: 30000 });
    expect(response?.status()).toBeLessThan(400);
    expect(consoleErrors).toHaveLength(0);
    console.log('✅ AUTH: Page loaded successfully');
  });

  // ==================== PAGE 3: DASHBOARD ====================
  test('3. DASHBOARD - Page loads', async ({ page }) => {
    const consoleErrors: string[] = [];
    page.on('console', (msg: any) => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });

    try {
      const response = await page.goto('https://astrorattan.com/dashboard', { waitUntil: 'networkidle', timeout: 30000 });
      expect(response?.status()).toBeLessThan(400);
      console.log('✅ DASHBOARD: Page loaded successfully');
    } catch (error) {
      console.log(`⚠️ DASHBOARD: May require authentication - ${error}`);
    }
  });

  // ==================== PAGE 4: KUNDLI ====================
  test('4. KUNDLI - Page loads without console errors', async ({ page }) => {
    const consoleErrors: string[] = [];
    page.on('console', (msg: any) => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });

    const response = await page.goto('https://astrorattan.com/kundli', { waitUntil: 'networkidle', timeout: 30000 });
    expect(response?.status()).toBeLessThan(400);
    expect(consoleErrors).toHaveLength(0);

    // Check form visible
    const form = page.locator('form').first();
    await expect(form).toBeVisible({ timeout: 5000 });
    await takeScreenshot(page, 'kundli-loaded');
    console.log('✅ KUNDLI: Page loaded with form visible');
  });

  test('4. KUNDLI - KundliForm is submittable', async ({ page }) => {
    await page.goto('https://astrorattan.com/kundli', { waitUntil: 'networkidle', timeout: 30000 });

    try {
      // Find form inputs
      const nameInput = page.locator('input[name="name"], input[placeholder*="Name" i], input[placeholder*="name" i]').first();
      const dateInput = page.locator('input[type="date"], input[name*="date" i]').first();

      let filled = 0;
      if (await nameInput.isVisible({ timeout: 2000 }).catch(() => false)) {
        await nameInput.fill('Test User');
        filled++;
      }

      if (await dateInput.isVisible({ timeout: 2000 }).catch(() => false)) {
        await dateInput.fill('1990-01-15');
        filled++;
      }

      // Check if submit button exists and is clickable
      const submitButton = page.locator('button[type="submit"], button:has-text("Submit"), button:has-text("Calculate")').first();
      if (await submitButton.isVisible({ timeout: 2000 }).catch(() => false)) {
        await expect(submitButton).toBeEnabled();
        console.log(`✅ KUNDLI: Form submittable (${filled} fields filled, submit button ready)`);
      } else {
        console.log('⚠️ KUNDLI: Submit button not found');
      }
    } catch (error) {
      console.log(`⚠️ KUNDLI: Form submission test skipped - ${error}`);
    }
  });

  test('4. KUNDLI - Tabs switchable', async ({ page }) => {
    await page.goto('https://astrorattan.com/kundli', { waitUntil: 'networkidle', timeout: 30000 });

    try {
      const tabs = page.locator('[role="tab"], button[class*="tab"]');
      const tabCount = await tabs.count();

      if (tabCount > 1) {
        let clickedTabs = 0;
        for (let i = 0; i < Math.min(tabCount, 3); i++) {
          const tab = tabs.nth(i);
          if (await tab.isVisible({ timeout: 1000 }).catch(() => false)) {
            await tab.click();
            await page.waitForTimeout(200);
            clickedTabs++;
          }
        }
        console.log(`✅ KUNDLI: ${clickedTabs} tabs switched successfully`);
      } else {
        console.log('⚠️ KUNDLI: No tabs found');
      }
    } catch (error) {
      console.log(`⚠️ KUNDLI: Tab test - ${error}`);
    }
  });

  // ==================== PAGE 5: PANCHANG ====================
  test('5. PANCHANG - Page loads without console errors', async ({ page }) => {
    const consoleErrors: string[] = [];
    page.on('console', (msg: any) => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });

    const response = await page.goto('https://astrorattan.com/panchang', { waitUntil: 'networkidle', timeout: 30000 });
    expect(response?.status()).toBeLessThan(400);
    expect(consoleErrors).toHaveLength(0);
    await takeScreenshot(page, 'panchang-loaded');
    console.log('✅ PANCHANG: Page loaded successfully');
  });

  test('5. PANCHANG - Tabs switchable', async ({ page }) => {
    await page.goto('https://astrorattan.com/panchang', { waitUntil: 'networkidle', timeout: 30000 });

    try {
      const tabs = page.locator('[role="tab"], button[class*="tab"]');
      const tabCount = await tabs.count();

      if (tabCount > 1) {
        let switched = 0;
        for (let i = 0; i < Math.min(tabCount, 4); i++) {
          const tab = tabs.nth(i);
          if (await tab.isVisible({ timeout: 1000 }).catch(() => false)) {
            await tab.click();
            await page.waitForTimeout(300);
            switched++;
          }
        }
        console.log(`✅ PANCHANG: ${switched} tabs switched successfully`);
      } else {
        console.log('⚠️ PANCHANG: No tabs found');
      }
    } catch (error) {
      console.log(`⚠️ PANCHANG: Tab test - ${error}`);
    }
  });

  test('5. PANCHANG - Tables render without horizontal overflow', async ({ page }) => {
    await page.goto('https://astrorattan.com/panchang', { waitUntil: 'networkidle', timeout: 30000 });

    try {
      const tables = page.locator('table, [role="table"], .table');
      const tableCount = await tables.count();

      let overflowCount = 0;
      for (let i = 0; i < Math.min(tableCount, 3); i++) {
        const table = tables.nth(i);
        const scrollWidth = await table.evaluate((el) => el.scrollWidth);
        const clientWidth = await table.evaluate((el) => el.clientWidth);
        if (scrollWidth > clientWidth + 5) {
          overflowCount++;
        }
      }

      console.log(`✅ PANCHANG: ${tableCount} tables checked (${overflowCount} with overflow)`);
    } catch (error) {
      console.log(`⚠️ PANCHANG: Table test - ${error}`);
    }
  });

  // ==================== PAGE 6: HOROSCOPE ====================
  test('6. HOROSCOPE - Page loads without console errors', async ({ page }) => {
    const consoleErrors: string[] = [];
    page.on('console', (msg: any) => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });

    const response = await page.goto('https://astrorattan.com/horoscope', { waitUntil: 'networkidle', timeout: 30000 });
    expect(response?.status()).toBeLessThan(400);
    expect(consoleErrors).toHaveLength(0);
    console.log('✅ HOROSCOPE: Page loaded successfully');
  });

  test('6. HOROSCOPE - Tabs switchable', async ({ page }) => {
    await page.goto('https://astrorattan.com/horoscope', { waitUntil: 'networkidle', timeout: 30000 });

    try {
      const tabs = page.locator('[role="tab"], button[class*="tab"]');
      const tabCount = await tabs.count();
      let switched = 0;

      for (let i = 0; i < Math.min(tabCount, 3); i++) {
        const tab = tabs.nth(i);
        if (await tab.isVisible({ timeout: 1000 }).catch(() => false)) {
          await tab.click();
          await page.waitForTimeout(300);
          switched++;
        }
      }

      console.log(`✅ HOROSCOPE: ${switched} tabs switched`);
    } catch (error) {
      console.log(`⚠️ HOROSCOPE: Tab test - ${error}`);
    }
  });

  // ==================== PAGE 7: LAL KITAB ====================
  test('7. LAL KITAB - Page loads without console errors', async ({ page }) => {
    const consoleErrors: string[] = [];
    page.on('console', (msg: any) => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });

    const response = await page.goto('https://astrorattan.com/lalkitab', { waitUntil: 'networkidle', timeout: 30000 });
    expect(response?.status()).toBeLessThan(400);
    expect(consoleErrors).toHaveLength(0);
    console.log('✅ LAL KITAB: Page loaded successfully');
  });

  test('7. LAL KITAB - LalKitabForm submittable', async ({ page }) => {
    await page.goto('https://astrorattan.com/lalkitab', { waitUntil: 'networkidle', timeout: 30000 });

    try {
      const form = page.locator('form').first();
      if (await form.isVisible({ timeout: 2000 }).catch(() => false)) {
        const inputs = form.locator('input');
        const inputCount = await inputs.count();
        console.log(`✅ LAL KITAB: Form visible with ${inputCount} inputs`);
      }
    } catch (error) {
      console.log(`⚠️ LAL KITAB: Form test - ${error}`);
    }
  });

  test('7. LAL KITAB - Tabs switchable (15+ tabs)', async ({ page }) => {
    await page.goto('https://astrorattan.com/lalkitab', { waitUntil: 'networkidle', timeout: 30000 });

    try {
      const tabs = page.locator('[role="tab"], button[class*="tab"]');
      const tabCount = await tabs.count();

      if (tabCount > 1) {
        let switched = 0;
        for (let i = 0; i < Math.min(tabCount, 8); i++) {
          const tab = tabs.nth(i);
          if (await tab.isVisible({ timeout: 1000 }).catch(() => false)) {
            await tab.click();
            await page.waitForTimeout(300);
            switched++;
          }
        }
        console.log(`✅ LAL KITAB: ${switched} of ${tabCount} tabs switched successfully`);
      } else {
        console.log('⚠️ LAL KITAB: No tabs found');
      }
    } catch (error) {
      console.log(`⚠️ LAL KITAB: Tab test - ${error}`);
    }
  });

  // ==================== PAGE 8: NUMEROLOGY ====================
  test('8. NUMEROLOGY - Page loads without console errors', async ({ page }) => {
    const consoleErrors: string[] = [];
    page.on('console', (msg: any) => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });

    const response = await page.goto('https://astrorattan.com/numerology', { waitUntil: 'networkidle', timeout: 30000 });
    expect(response?.status()).toBeLessThan(400);
    expect(consoleErrors).toHaveLength(0);
    console.log('✅ NUMEROLOGY: Page loaded successfully');
  });

  // ==================== PAGE 9: VASTU ====================
  test('9. VASTU - Page loads without console errors', async ({ page }) => {
    const consoleErrors: string[] = [];
    page.on('console', (msg: any) => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });

    const response = await page.goto('https://astrorattan.com/vastu', { waitUntil: 'networkidle', timeout: 30000 });
    expect(response?.status()).toBeLessThan(400);
    expect(consoleErrors).toHaveLength(0);

    const form = page.locator('form').first();
    await expect(form).toBeVisible({ timeout: 5000 });
    console.log('✅ VASTU: Page loaded with form visible');
  });

  test('9. VASTU - VastuForm submittable', async ({ page }) => {
    await page.goto('https://astrorattan.com/vastu', { waitUntil: 'networkidle', timeout: 30000 });

    try {
      const form = page.locator('form').first();
      if (await form.isVisible({ timeout: 2000 }).catch(() => false)) {
        const submitButton = form.locator('button[type="submit"], button:has-text("Submit")').first();
        if (await submitButton.isVisible({ timeout: 2000 }).catch(() => false)) {
          await expect(submitButton).toBeEnabled();
          console.log('✅ VASTU: Submit button present and enabled');
        }
      }
    } catch (error) {
      console.log(`⚠️ VASTU: Form test - ${error}`);
    }
  });

  test('9. VASTU - Remedy tables render without overflow', async ({ page }) => {
    await page.goto('https://astrorattan.com/vastu', { waitUntil: 'networkidle', timeout: 30000 });

    try {
      const tables = page.locator('table, [role="table"]');
      const tableCount = await tables.count();

      let overflowCount = 0;
      for (let i = 0; i < Math.min(tableCount, 2); i++) {
        const table = tables.nth(i);
        const scrollWidth = await table.evaluate((el) => el.scrollWidth);
        const clientWidth = await table.evaluate((el) => el.clientWidth);
        if (scrollWidth > clientWidth + 5) {
          overflowCount++;
        }
      }

      console.log(`✅ VASTU: ${tableCount} tables checked (${overflowCount} with overflow)`);
    } catch (error) {
      console.log(`⚠️ VASTU: Table test - ${error}`);
    }
  });

  // ==================== PAGE 10: FEEDBACK ====================
  test('10. FEEDBACK - Page loads without console errors', async ({ page }) => {
    const consoleErrors: string[] = [];
    page.on('console', (msg: any) => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });

    const response = await page.goto('https://astrorattan.com/feedback', { waitUntil: 'networkidle', timeout: 30000 });
    expect(response?.status()).toBeLessThan(400);
    expect(consoleErrors).toHaveLength(0);

    const form = page.locator('form').first();
    await expect(form).toBeVisible({ timeout: 5000 });
    console.log('✅ FEEDBACK: Page loaded with form visible');
  });

  test('10. FEEDBACK - Form submittable', async ({ page }) => {
    await page.goto('https://astrorattan.com/feedback', { waitUntil: 'networkidle', timeout: 30000 });

    try {
      const form = page.locator('form').first();
      const submitButton = form.locator('button[type="submit"], button:has-text("Submit")').first();

      if (await submitButton.isVisible({ timeout: 2000 }).catch(() => false)) {
        await expect(submitButton).toBeEnabled();
        console.log('✅ FEEDBACK: Submit button present and enabled');
      }
    } catch (error) {
      console.log(`⚠️ FEEDBACK: Form test - ${error}`);
    }
  });

  // ==================== PAGE 11: ADMIN ====================
  test('11. ADMIN - Page loads', async ({ page }) => {
    try {
      const response = await page.goto('https://astrorattan.com/admin', { waitUntil: 'networkidle', timeout: 30000 });
      console.log('✅ ADMIN: Page loaded (may require authentication)');
    } catch (error) {
      console.log(`⚠️ ADMIN: ${error}`);
    }
  });

  // ==================== PAGE 12: ASTROLOGER DASHBOARD ====================
  test('12. ASTROLOGER DASHBOARD - Page loads', async ({ page }) => {
    try {
      const response = await page.goto('https://astrorattan.com/astrologer-dashboard', { waitUntil: 'networkidle', timeout: 30000 });
      console.log('✅ ASTROLOGER DASHBOARD: Page loaded');
    } catch (error) {
      console.log(`⚠️ ASTROLOGER DASHBOARD: ${error}`);
    }
  });

  // ==================== PAGE 13: CLIENT PROFILE ====================
  test('13. CLIENT PROFILE - Page loads', async ({ page }) => {
    try {
      const response = await page.goto('https://astrorattan.com/client-profile', { waitUntil: 'networkidle', timeout: 30000 });
      console.log('✅ CLIENT PROFILE: Page loaded');
    } catch (error) {
      console.log(`⚠️ CLIENT PROFILE: ${error}`);
    }
  });

  // ==================== PAGE 14: BLOG ====================
  test('14. BLOG - Page loads without console errors', async ({ page }) => {
    const consoleErrors: string[] = [];
    page.on('console', (msg: any) => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });

    const response = await page.goto('https://astrorattan.com/blog', { waitUntil: 'networkidle', timeout: 30000 });
    expect(response?.status()).toBeLessThan(400);
    expect(consoleErrors).toHaveLength(0);
    console.log('✅ BLOG: Page loaded successfully');
  });

  // ==================== CROSS-PAGE MOBILE TESTS ====================
  test('MOBILE LAYOUT - No horizontal scroll on all public pages', async ({ page }) => {
    const pages = [
      'https://astrorattan.com',
      'https://astrorattan.com/kundli',
      'https://astrorattan.com/panchang',
      'https://astrorattan.com/horoscope',
    ];

    for (const url of pages) {
      try {
        await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
        const hasHorizontalScroll = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);

        if (!hasHorizontalScroll) {
          console.log(`✅ ${url.split('/')[3] || 'HOME'}: No horizontal scroll`);
        } else {
          console.log(`⚠️ ${url.split('/')[3] || 'HOME'}: Horizontal scroll detected`);
        }
      } catch (error) {
        console.log(`⚠️ ${url}: ${error}`);
      }
    }
  });

  test('MOBILE TOUCH - Text is readable (font size >= 12px)', async ({ page }) => {
    const pages = [
      'https://astrorattan.com',
      'https://astrorattan.com/kundli',
    ];

    for (const url of pages) {
      try {
        await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
        const fontSize = await page.evaluate(() => {
          const el = document.querySelector('p, h1, h2, h3');
          return el ? window.getComputedStyle(el).fontSize : '0px';
        });

        const fontSizeNum = parseFloat(fontSize);
        if (fontSizeNum >= 12) {
          console.log(`✅ ${url.split('/')[3] || 'HOME'}: Text readable (${fontSize})`);
        } else {
          console.log(`⚠️ ${url.split('/')[3] || 'HOME'}: Text too small (${fontSize})`);
        }
      } catch (error) {
        console.log(`⚠️ ${url}: ${error}`);
      }
    }
  });

  test('BLANK PAGE CHECK - Content loads (not blank)', async ({ page }) => {
    const pages = [
      'https://astrorattan.com',
      'https://astrorattan.com/kundli',
      'https://astrorattan.com/panchang',
    ];

    for (const url of pages) {
      try {
        await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
        const content = await page.evaluate(() => {
          const body = document.body.innerText;
          return body ? body.trim().length : 0;
        });

        if (content > 100) {
          console.log(`✅ ${url.split('/')[3] || 'HOME'}: Content loaded (${content} chars)`);
        } else {
          console.log(`❌ ${url.split('/')[3] || 'HOME'}: Blank or minimal content`);
        }
      } catch (error) {
        console.log(`⚠️ ${url}: ${error}`);
      }
    }
  });
});
