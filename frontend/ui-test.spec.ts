import { test } from '@playwright/test';

const BASE_URL = 'http://localhost:5173';

// Test Home Page sections
test('Home Page - Full Screenshot', async ({ page }) => {
  await page.goto(BASE_URL);
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(2000);
  
  // Hero section
  await page.screenshot({ 
    path: 'ui-screenshots/home-hero.png', 
    fullPage: false,
    clip: { x: 0, y: 0, width: 1280, height: 800 }
  });
  
  // Full page scroll
  await page.screenshot({ 
    path: 'ui-screenshots/home-full.png', 
    fullPage: true 
  });
});

test('Home Page - Our Story Section', async ({ page }) => {
  await page.goto(BASE_URL + '#about');
  await page.waitForTimeout(1000);
  
  const about = await page.locator('#about');
  await about.screenshot({ path: 'ui-screenshots/section-our-story.png' });
});

test('Home Page - Features Section', async ({ page }) => {
  await page.goto(BASE_URL);
  await page.waitForTimeout(1000);
  
  await page.evaluate(() => {
    const features = document.querySelector('#features');
    if (features) features.scrollIntoView();
  });
  await page.waitForTimeout(1000);
  
  await page.screenshot({ 
    path: 'ui-screenshots/section-features.png',
    clip: { x: 0, y: 400, width: 1280, height: 800 }
  });
});

test('Home Page - CTA Section', async ({ page }) => {
  await page.goto(BASE_URL);
  await page.waitForTimeout(1000);
  
  await page.evaluate(() => {
    const cta = document.querySelector('#cta');
    if (cta) cta.scrollIntoView();
  });
  await page.waitForTimeout(1000);
  
  await page.screenshot({ 
    path: 'ui-screenshots/section-cta.png',
    clip: { x: 0, y: 400, width: 1280, height: 800 }
  });
});

// Test Navigation Pages
test('Navigation - Kundli Generator', async ({ page }) => {
  await page.goto(BASE_URL + '/kundli');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/page-kundli.png' });
});

test('Navigation - Kundli 3D Demo', async ({ page }) => {
  await page.goto(BASE_URL + '/kundli-3d');
  await page.waitForTimeout(3000); // Wait for 3D scene to load
  await page.screenshot({ path: 'ui-screenshots/page-kundli-3d.png' });
});

test('Navigation - Daily Horoscope', async ({ page }) => {
  await page.goto(BASE_URL + '/horoscope');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/page-horoscope.png' });
});

test('Navigation - Panchang', async ({ page }) => {
  await page.goto(BASE_URL + '/panchang');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/page-panchang.png' });
});

test('Navigation - Shop', async ({ page }) => {
  await page.goto(BASE_URL + '/shop');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/page-shop.png' });
});

test('Navigation - Spiritual Library', async ({ page }) => {
  await page.goto(BASE_URL + '/library');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/page-library.png' });
  
  // Click on "View 47 Verses" button to see verses display
  await page.click('button:has-text("View 47 Verses")');
  await page.waitForTimeout(1500);
  // Scroll down to see verses
  await page.evaluate(() => window.scrollTo(0, 800));
  await page.waitForTimeout(500);
  await page.screenshot({ path: 'ui-screenshots/page-library-verses.png' });
});

test('Navigation - Consultation', async ({ page }) => {
  await page.goto(BASE_URL + '/consultation');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/page-consultation.png' });
});

test('Navigation - Cosmic Calendar', async ({ page }) => {
  await page.goto(BASE_URL + '/calendar');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/page-calendar.png' });
});

test('Navigation - Blog', async ({ page }) => {
  await page.goto(BASE_URL + '/blog');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/page-blog.png' });
});

test('Navigation - Community', async ({ page }) => {
  await page.goto(BASE_URL + '/community');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/page-community.png' });
});

// Test Auth Pages
test('Auth - Login Page', async ({ page }) => {
  await page.goto(BASE_URL + '/auth?mode=login');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/auth-login.png' });
});

test('Auth - Register Page', async ({ page }) => {
  await page.goto(BASE_URL + '/auth?mode=register');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/auth-register.png' });
});

// Test Dashboard
test('Dashboard - User Dashboard', async ({ page }) => {
  await page.goto(BASE_URL + '/dashboard');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/dashboard-user.png' });
});

test('Dashboard - Astrologer Dashboard', async ({ page }) => {
  await page.goto(BASE_URL + '/astrologer-dashboard');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/dashboard-astrologer.png' });
});

// Test Special Pages
test('Special - Numerology & Tarot', async ({ page }) => {
  await page.goto(BASE_URL + '/numerology-tarot');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/page-numerology.png' });
});

test('Special - Palmistry', async ({ page }) => {
  await page.goto(BASE_URL + '/palmistry');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/page-palmistry.png' });
});

test('Special - Prashnavali', async ({ page }) => {
  await page.goto(BASE_URL + '/prashnavali');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/page-prashnavali.png' });
});

test('Special - Planetary Transits', async ({ page }) => {
  await page.goto(BASE_URL + '/transits');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/page-transits.png' });
});

test('Special - KP & Lalkitab', async ({ page }) => {
  await page.goto(BASE_URL + '/kp-lalkitab');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/page-kp-lalkitab.png' });
});

test('Special - Report Marketplace', async ({ page }) => {
  await page.goto(BASE_URL + '/reports');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/page-reports.png' });
});

test('Special - Cart & Checkout', async ({ page }) => {
  await page.goto(BASE_URL + '/cart');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/page-cart.png' });
});

test('Special - AI Chat', async ({ page }) => {
  await page.goto(BASE_URL + '/ai-chat');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/page-ai-chat.png' });
});

test('Special - Gamification', async ({ page }) => {
  await page.goto(BASE_URL + '/gamification');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/page-gamification.png' });
});

// ─── Lal Kitab Section Tests ──────────────────────────────────────────────────

test('LK - Page loads with tab navigation', async ({ page }) => {
  await page.goto(BASE_URL + '/kp-lalkitab');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'ui-screenshots/lk-page-full.png', fullPage: true });
});

test('LK - Farmaan tab renders and shows search or empty state', async ({ page }) => {
  await page.goto(BASE_URL + '/kp-lalkitab');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1500);

  // Find and click the Farmaan tab — try both English and Hindi label variants
  const farmaanTab = page.locator('button, [role="tab"]').filter({ hasText: /farmaan|फरमान/i }).first();
  const tabExists = await farmaanTab.count();
  if (tabExists > 0) {
    await farmaanTab.click();
    await page.waitForTimeout(1500);
  }

  await page.screenshot({ path: 'ui-screenshots/lk-farmaan-tab.png', fullPage: true });
});

test('LK - Nishaniyan tab renders signs/symbols', async ({ page }) => {
  await page.goto(BASE_URL + '/kp-lalkitab');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1500);

  const nishaanTab = page.locator('button, [role="tab"]').filter({ hasText: /nishaniyan|निशानियां/i }).first();
  const tabExists = await nishaanTab.count();
  if (tabExists > 0) {
    await nishaanTab.click();
    await page.waitForTimeout(1500);
  }

  await page.screenshot({ path: 'ui-screenshots/lk-nishaniyan-tab.png', fullPage: true });
});

test('LK - Chandra Chalana tab shows task list or start prompt', async ({ page }) => {
  await page.goto(BASE_URL + '/kp-lalkitab');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1500);

  const chandraTab = page.locator('button, [role="tab"]').filter({ hasText: /chandra|चंद्र/i }).first();
  const tabExists = await chandraTab.count();
  if (tabExists > 0) {
    await chandraTab.click();
    await page.waitForTimeout(2000);
  }

  await page.screenshot({ path: 'ui-screenshots/lk-chandra-tab.png', fullPage: true });
});

test('LK - Vastu tab renders house diagram or placeholder', async ({ page }) => {
  await page.goto(BASE_URL + '/kp-lalkitab');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1500);

  const vastuTab = page.locator('button, [role="tab"]').filter({ hasText: /vastu|वास्तु/i }).first();
  const tabExists = await vastuTab.count();
  if (tabExists > 0) {
    await vastuTab.click();
    await page.waitForTimeout(2000);
  }

  await page.screenshot({ path: 'ui-screenshots/lk-vastu-tab.png', fullPage: true });
});

test('LK - Remedies tab renders remedy cards', async ({ page }) => {
  await page.goto(BASE_URL + '/kp-lalkitab');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1500);

  const remedyTab = page.locator('button, [role="tab"]').filter({ hasText: /remd|remedy|उपाय/i }).first();
  const tabExists = await remedyTab.count();
  if (tabExists > 0) {
    await remedyTab.click();
    await page.waitForTimeout(2000);
  }

  await page.screenshot({ path: 'ui-screenshots/lk-remedies-tab.png', fullPage: true });
});

test('LK - Milestones tab renders countdown or milestone list', async ({ page }) => {
  await page.goto(BASE_URL + '/kp-lalkitab');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1500);

  const msTab = page.locator('button, [role="tab"]').filter({ hasText: /milestone|मील/i }).first();
  const tabExists = await msTab.count();
  if (tabExists > 0) {
    await msTab.click();
    await page.waitForTimeout(2000);
  }

  await page.screenshot({ path: 'ui-screenshots/lk-milestones-tab.png', fullPage: true });
});

test('LK - Doshas tab renders dosha analysis cards', async ({ page }) => {
  await page.goto(BASE_URL + '/kp-lalkitab');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1500);

  const doshaTab = page.locator('button, [role="tab"]').filter({ hasText: /dosha|दोष/i }).first();
  const tabExists = await doshaTab.count();
  if (tabExists > 0) {
    await doshaTab.click();
    await page.waitForTimeout(2000);
  }

  await page.screenshot({ path: 'ui-screenshots/lk-doshas-tab.png', fullPage: true });
});
