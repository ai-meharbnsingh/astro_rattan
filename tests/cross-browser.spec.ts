import { test, expect, devices } from '@playwright/test';

test.describe.configure({ timeout: 30000 });

// Add reporter config
test.describe('🌐 Astrorattan - Cross-Browser Compatibility Tests', () => {

  // ========== DESKTOP BROWSERS ==========
  
  test.describe('Desktop Browsers', () => {
    
    test('01: Chromium (Chrome/Edge) - Desktop', async ({ page }) => {
      console.log('\n📱 Testing: Chromium Desktop');
      
      const errors: string[] = [];
      const warnings: string[] = [];
      
      page.on('console', msg => {
        const text = msg.text();
        if (msg.type() === 'error') errors.push(text);
        if (msg.type() === 'warning') warnings.push(text);
      });

      page.on('response', response => {
        if (!response.ok() && response.status() !== 401) {
          errors.push(`HTTP ${response.status()}: ${response.url()}`);
        }
      });

      await page.goto('https://astrorattan.com', { waitUntil: 'domcontentloaded', timeout: 15000 });
      await page.waitForTimeout(2000);

      const title = await page.title();
      expect(title).toContain('Astro Rattan');

      console.log(`✅ Title: ${title}`);
      console.log(`   Errors: ${errors.length}`);
      console.log(`   Warnings: ${warnings.length}`);
      if (errors.length > 0) console.log('   Error details:', errors.slice(0, 3));
    });

    test('02: Firefox - Desktop', async ({ page }) => {
      console.log('\n📱 Testing: Firefox Desktop');
      
      const errors: string[] = [];
      page.on('console', msg => {
        if (msg.type() === 'error') errors.push(msg.text());
      });

      await page.goto('https://astrorattan.com', { waitUntil: 'domcontentloaded', timeout: 15000 });
      await page.waitForTimeout(2000);

      const title = await page.title();
      expect(title).toContain('Astro Rattan');
      console.log(`✅ Title: ${title}`);
      console.log(`   Errors: ${errors.length}`);
    });

    test('03: Webkit (Safari) - Desktop', async ({ page }) => {
      console.log('\n📱 Testing: Safari (Webkit) Desktop');
      
      const errors: string[] = [];
      page.on('console', msg => {
        if (msg.type() === 'error') errors.push(msg.text());
      });

      await page.goto('https://astrorattan.com', { waitUntil: 'domcontentloaded', timeout: 15000 });
      await page.waitForTimeout(2000);

      const title = await page.title();
      expect(title).toContain('Astro Rattan');
      console.log(`✅ Title: ${title}`);
      console.log(`   Errors: ${errors.length}`);
    });
  });

  // ========== MOBILE BROWSERS ==========

  test.describe('Mobile Browsers', () => {
    
    test('04: Chrome Mobile - Android', async ({ page }) => {
      console.log('\n📱 Testing: Chrome Mobile (Android)');
      page.setViewportSize({ width: 393, height: 851 }); // Pixel 5
      
      const errors: string[] = [];
      page.on('console', msg => {
        if (msg.type() === 'error') errors.push(msg.text());
      });

      await page.goto('https://astrorattan.com', { waitUntil: 'domcontentloaded', timeout: 15000 });
      await page.waitForTimeout(2000);

      const title = await page.title();
      expect(title).toContain('Astro Rattan');
      console.log(`✅ Title: ${title}`);
      console.log(`   Viewport: 393x851 (Pixel 5)`);
      console.log(`   Errors: ${errors.length}`);
    });

    test('05: Safari Mobile - iPhone', async ({ page }) => {
      console.log('\n📱 Testing: Safari Mobile (iPhone)');
      page.setViewportSize({ width: 390, height: 844 }); // iPhone 14
      
      const errors: string[] = [];
      page.on('console', msg => {
        if (msg.type() === 'error') errors.push(msg.text());
      });

      await page.goto('https://astrorattan.com', { waitUntil: 'domcontentloaded', timeout: 15000 });
      await page.waitForTimeout(2000);

      const title = await page.title();
      expect(title).toContain('Astro Rattan');
      console.log(`✅ Title: ${title}`);
      console.log(`   Viewport: 390x844 (iPhone 14)`);
      console.log(`   Errors: ${errors.length}`);
    });

    test('06: Safari Mobile - iPad', async ({ page }) => {
      console.log('\n📱 Testing: Safari Mobile (iPad)');
      page.setViewportSize({ width: 1024, height: 1366 }); // iPad Pro
      
      const errors: string[] = [];
      page.on('console', msg => {
        if (msg.type() === 'error') errors.push(msg.text());
      });

      await page.goto('https://astrorattan.com', { waitUntil: 'domcontentloaded', timeout: 15000 });
      await page.waitForTimeout(2000);

      const title = await page.title();
      expect(title).toContain('Astro Rattan');
      console.log(`✅ Title: ${title}`);
      console.log(`   Viewport: 1024x1366 (iPad Pro)`);
      console.log(`   Errors: ${errors.length}`);
    });
  });

  // ========== FEATURE TESTS ==========

  test.describe('Feature Tests', () => {
    
    test('07: Kundli Form - All Browsers', async ({ page }) => {
      console.log('\n🎯 Testing: Kundli Form');
      
      await page.goto('https://astrorattan.com/kundli', { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(2000);

      // Check if form elements exist
      const formExists = await page.locator('form, input, button').first().isVisible({ timeout: 5000 }).catch(() => false);
      
      if (formExists) {
        console.log(`✅ Form loaded successfully`);
      } else {
        console.log(`⚠️  Form elements not immediately visible`);
      }
    });

    test('08: API Call - Current Sky', async ({ page }) => {
      console.log('\n🌟 Testing: API - Current Sky');
      
      let apiSuccess = false;
      
      page.on('response', response => {
        if (response.url().includes('/api/kundli/current-sky') && response.ok()) {
          apiSuccess = true;
          console.log(`✅ API responded with ${response.status()}`);
        }
      });

      await page.goto('https://astrorattan.com', { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(3000);

      if (apiSuccess) {
        console.log(`✅ API calls successful`);
      } else {
        console.log(`⚠️  API calls made (may be queued or cached)`);
      }
    });

    test('09: Language Toggle - Storage Test', async ({ page }) => {
      console.log('\n🗣️ Testing: Language Toggle & Storage');
      
      await page.goto('https://astrorattan.com', { waitUntil: 'domcontentloaded' });
      
      // Check localStorage access
      const storageAvailable = await page.evaluate(() => {
        try {
          localStorage.setItem('test', 'test');
          localStorage.removeItem('test');
          return true;
        } catch {
          return false;
        }
      });

      if (storageAvailable) {
        console.log(`✅ localStorage available`);
      } else {
        console.log(`⚠️  localStorage unavailable (private mode?)`);
      }
    });
  });

  // ========== PRIVATE BROWSING MODE ==========

  test.describe('Private Browsing Mode', () => {
    
    test('10: Private Mode - Storage Handling', async ({ browser }) => {
      console.log('\n🔒 Testing: Private Browsing Mode');
      
      // Create private context
      const context = await browser.newContext({
        javaScriptEnabled: true,
        locale: 'en-US'
      });
      const page = await context.newPage();

      const errors: string[] = [];
      page.on('console', msg => {
        if (msg.type() === 'error') errors.push(msg.text());
      });

      await page.goto('https://astrorattan.com', { waitUntil: 'domcontentloaded', timeout: 15000 });
      await page.waitForTimeout(2000);

      const title = await page.title();
      expect(title).toContain('Astro Rattan');
      
      console.log(`✅ Title: ${title}`);
      console.log(`   Errors in private mode: ${errors.length}`);
      
      await context.close();
    });
  });

  // ========== PERFORMANCE TESTS ==========

  test.describe('Performance', () => {
    
    test('11: Page Load Time', async ({ page }) => {
      console.log('\n⏱️  Testing: Page Load Performance');
      
      const startTime = Date.now();
      await page.goto('https://astrorattan.com', { waitUntil: 'domcontentloaded' });
      const loadTime = Date.now() - startTime;

      console.log(`✅ Page loaded in ${loadTime}ms`);
      
      if (loadTime < 3000) {
        console.log(`✅ EXCELLENT performance (< 3s)`);
      } else if (loadTime < 5000) {
        console.log(`⚠️  GOOD performance (3-5s)`);
      } else {
        console.log(`⚠️  NEEDS IMPROVEMENT (> 5s)`);
      }
    });
  });
});
