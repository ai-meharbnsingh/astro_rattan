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
