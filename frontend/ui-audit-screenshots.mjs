import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';

const BASE = 'http://localhost:5173';
const EMAIL = 'meharbansingh85@gmail.com';
const PASSWORD = 'Misha@2311';
const SHOT_DIR = path.resolve('ui-screenshots/audit');

fs.mkdirSync(SHOT_DIR, { recursive: true });

let shotNum = 0;
async function snap(page, name, fullPage = true) {
  shotNum++;
  const fname = `${String(shotNum).padStart(2, '0')}_${name}.png`;
  await page.screenshot({ path: path.join(SHOT_DIR, fname), fullPage });
  console.log(`  [${shotNum}] ${fname}`);
}

(async () => {
  const browser = await chromium.launch({
    executablePath: '/Users/meharban/Library/Caches/ms-playwright/chromium-1217/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing',
    headless: false,
  });

  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();
  page.setDefaultTimeout(15000);

  // ──────────── HOMEPAGE (unauthenticated) ────────────
  console.log('\n=== HOMEPAGE (logged out) ===');
  await page.goto(BASE, { waitUntil: 'networkidle' });
  await snap(page, 'homepage_hero');

  // Scroll to features
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight * 0.5));
  await page.waitForTimeout(500);
  await snap(page, 'homepage_features', false);

  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(500);
  await snap(page, 'homepage_footer', false);

  // ──────────── PUBLIC KUNDLI PAGE (no auth) ────────────
  console.log('\n=== KUNDLI PAGE (public) ===');
  await page.goto(`${BASE}/kundli`, { waitUntil: 'networkidle' });
  await snap(page, 'kundli_public');

  // ──────────── PUBLIC PANCHANG PAGE (no auth) ────────────
  console.log('\n=== PANCHANG PAGE (public) ===');
  await page.goto(`${BASE}/panchang`, { waitUntil: 'networkidle' });
  await snap(page, 'panchang_public');

  // ──────────── AUTH PAGE ────────────
  console.log('\n=== AUTH PAGE ===');
  await page.goto(`${BASE}/login`, { waitUntil: 'networkidle' });
  await snap(page, 'auth_login_form');

  // Click register tab if exists
  try {
    const registerTab = page.locator('button:has-text("Register"), button:has-text("Sign Up"), [role="tab"]:has-text("Register")').first();
    if (await registerTab.isVisible({ timeout: 2000 })) {
      await registerTab.click();
      await page.waitForTimeout(500);
      await snap(page, 'auth_register_form');
    }
  } catch { /* no register tab visible */ }

  // ──────────── LOGIN ────────────
  console.log('\n=== LOGGING IN ===');
  // Go back to login tab
  try {
    const loginTab = page.locator('button:has-text("Login"), button:has-text("Sign In"), [role="tab"]:has-text("Login")').first();
    if (await loginTab.isVisible({ timeout: 2000 })) {
      await loginTab.click();
      await page.waitForTimeout(300);
    }
  } catch { /* already on login */ }

  await page.fill('input[type="email"], input[placeholder*="email" i], input[name="email"]', EMAIL);
  await page.fill('input[type="password"]', PASSWORD);
  await snap(page, 'auth_filled');

  // Submit
  await page.click('button[type="submit"], button:has-text("Login"), button:has-text("Sign In")');
  await page.waitForTimeout(3000);
  await snap(page, 'post_login');

  // ──────────── DASHBOARD ────────────
  console.log('\n=== DASHBOARD ===');
  await page.goto(`${BASE}/dashboard`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await snap(page, 'dashboard_main');
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(500);
  await snap(page, 'dashboard_bottom', false);

  // ──────────── KUNDLI GENERATOR (authenticated) ────────────
  console.log('\n=== KUNDLI GENERATOR ===');
  await page.goto(`${BASE}/kundli`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);
  await snap(page, 'kundli_form');

  // Try to generate a kundli - fill the form
  try {
    // Fill name
    const nameInput = page.locator('input[placeholder*="name" i], input#name, input[name="name"]').first();
    if (await nameInput.isVisible({ timeout: 2000 })) {
      await nameInput.fill('Test User');
    }

    // Fill date
    const dateInput = page.locator('input[type="date"]').first();
    if (await dateInput.isVisible({ timeout: 1000 })) {
      await dateInput.fill('1990-01-15');
    }

    // Fill time
    const timeInput = page.locator('input[type="time"]').first();
    if (await timeInput.isVisible({ timeout: 1000 })) {
      await timeInput.fill('06:30');
    }

    // Fill place
    const placeInput = page.locator('input[placeholder*="place" i], input[placeholder*="city" i], input[placeholder*="birth place" i]').first();
    if (await placeInput.isVisible({ timeout: 1000 })) {
      await placeInput.fill('New Delhi');
      await page.waitForTimeout(1500);
      // Click first suggestion
      const suggestion = page.locator('[role="option"], .suggestion, li:has-text("Delhi")').first();
      if (await suggestion.isVisible({ timeout: 2000 })) {
        await suggestion.click();
        await page.waitForTimeout(500);
      }
    }

    await snap(page, 'kundli_form_filled');

    // Submit
    const submitBtn = page.locator('button[type="submit"], button:has-text("Generate")').first();
    if (await submitBtn.isVisible({ timeout: 1000 })) {
      await submitBtn.click();
      await page.waitForTimeout(5000); // Wait for kundli generation
      await snap(page, 'kundli_generated');
    }
  } catch (e) {
    console.log('  Kundli form fill skipped:', e.message);
  }

  // ──────────── KUNDLI TABS (if kundli was generated or existing) ────────────
  console.log('\n=== KUNDLI TABS ===');
  const tabNames = ['Report', 'Planets', 'Dasha', 'Yoga', 'Dosha', 'Divisional', 'Aspects',
    'Shadbala', 'Ashtakvarga', 'Transits', 'Varshphal', 'KP', 'Jaimini', 'Mundane',
    'Yogini', 'Sade Sati', 'Birth', 'Lordships', 'Upagrahas', 'Sodashvarga', 'Iogita',
    'Avakhada', 'Milan'];

  for (const tab of tabNames) {
    try {
      // Try clicking the tab
      const tabBtn = page.locator(`button:has-text("${tab}"), [role="tab"]:has-text("${tab}")`).first();
      if (await tabBtn.isVisible({ timeout: 1000 })) {
        await tabBtn.click();
        await page.waitForTimeout(1500);
        await snap(page, `kundli_tab_${tab.toLowerCase().replace(/\s+/g, '_')}`, false);
      } else {
        // Maybe it's in the "More" dropdown
        const moreBtn = page.locator('button:has-text("More"), button:has-text("More Analysis")').first();
        if (await moreBtn.isVisible({ timeout: 500 })) {
          await moreBtn.click();
          await page.waitForTimeout(300);
          const moreTabBtn = page.locator(`button:has-text("${tab}")`).first();
          if (await moreTabBtn.isVisible({ timeout: 500 })) {
            await moreTabBtn.click();
            await page.waitForTimeout(1500);
            await snap(page, `kundli_tab_${tab.toLowerCase().replace(/\s+/g, '_')}`, false);
          }
        }
      }
    } catch {
      console.log(`  Skipped tab: ${tab}`);
    }
  }

  // ──────────── PANCHANG (authenticated) ────────────
  console.log('\n=== PANCHANG ===');
  await page.goto(`${BASE}/panchang`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  await snap(page, 'panchang_main');
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(500);
  await snap(page, 'panchang_bottom');

  // ──────────── LAL KITAB ────────────
  console.log('\n=== LAL KITAB ===');
  await page.goto(`${BASE}/lal-kitab`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await snap(page, 'lalkitab_form');

  // Check if there's a kundli to load, or fill form
  try {
    // Look for existing kundli list or form
    const existingKundli = page.locator('button:has-text("Load"), button:has-text("View"), [data-kundli]').first();
    if (await existingKundli.isVisible({ timeout: 2000 })) {
      await existingKundli.click();
      await page.waitForTimeout(3000);
    }
  } catch { /* */ }

  // Screenshot Lal Kitab tabs
  const lkTabs = ['Dashboard', 'Chart', 'Analysis', 'Timing', 'Upay', 'Predictions', 'Nishaniyan', 'Advanced'];
  for (const tab of lkTabs) {
    try {
      const tabBtn = page.locator(`button:has-text("${tab}"), [role="tab"]:has-text("${tab}")`).first();
      if (await tabBtn.isVisible({ timeout: 1000 })) {
        await tabBtn.click();
        await page.waitForTimeout(1500);
        await snap(page, `lalkitab_tab_${tab.toLowerCase()}`, false);

        // Scroll down to see more content
        await page.evaluate(() => window.scrollTo(0, 800));
        await page.waitForTimeout(300);
        await snap(page, `lalkitab_tab_${tab.toLowerCase()}_scrolled`, false);
      }
    } catch {
      console.log(`  Skipped LK tab: ${tab}`);
    }
  }

  // ──────────── NUMEROLOGY ────────────
  console.log('\n=== NUMEROLOGY ===');
  await page.goto(`${BASE}/numerology`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await snap(page, 'numerology_main');
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(500);
  await snap(page, 'numerology_bottom');

  // ──────────── VASTU SHASTRA ────────────
  console.log('\n=== VASTU SHASTRA ===');
  await page.goto(`${BASE}/vastu`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await snap(page, 'vastu_form');
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(500);
  await snap(page, 'vastu_form_bottom');

  // ──────────── FEEDBACK ────────────
  console.log('\n=== FEEDBACK ===');
  await page.goto(`${BASE}/feedback`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);
  await snap(page, 'feedback_page');

  // ──────────── MOBILE VIEWPORT ────────────
  console.log('\n=== MOBILE VIEWPORT (375x812) ===');
  await page.setViewportSize({ width: 375, height: 812 });

  await page.goto(BASE, { waitUntil: 'networkidle' });
  await snap(page, 'mobile_homepage');

  // Open mobile menu
  try {
    const hamburger = page.locator('button[aria-label*="menu" i], button:has(svg.lucide-menu), .hamburger, button:has-text("Menu")').first();
    if (await hamburger.isVisible({ timeout: 2000 })) {
      await hamburger.click();
      await page.waitForTimeout(500);
      await snap(page, 'mobile_menu_open', false);
      await hamburger.click(); // close
    }
  } catch { /* */ }

  await page.goto(`${BASE}/kundli`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);
  await snap(page, 'mobile_kundli');

  await page.goto(`${BASE}/login`, { waitUntil: 'networkidle' });
  await snap(page, 'mobile_auth');

  await page.goto(`${BASE}/dashboard`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await snap(page, 'mobile_dashboard');

  await page.goto(`${BASE}/lal-kitab`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);
  await snap(page, 'mobile_lalkitab');

  await page.goto(`${BASE}/vastu`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);
  await snap(page, 'mobile_vastu');

  await page.goto(`${BASE}/panchang`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);
  await snap(page, 'mobile_panchang');

  await page.goto(`${BASE}/numerology`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);
  await snap(page, 'mobile_numerology');

  // ──────────── DONE ────────────
  console.log(`\n=== COMPLETE: ${shotNum} screenshots saved to ${SHOT_DIR} ===`);

  await browser.close();
})();
