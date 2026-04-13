import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';

const BASE = 'http://localhost:5173';
const EMAIL = 'meharbansingh85@gmail.com';
const PASSWORD = 'Misha@2311';
const SHOT_DIR = path.resolve('ui-screenshots/audit');
fs.mkdirSync(SHOT_DIR, { recursive: true });

let shotNum = 0;
async function snap(page, name, fullPage = false) {
  shotNum++;
  const fname = `${String(shotNum).padStart(2, '0')}_${name}.png`;
  try {
    await page.screenshot({ path: path.join(SHOT_DIR, fname), fullPage, timeout: 30000 });
    console.log(`  [${shotNum}] ${fname}`);
  } catch (e) {
    console.log(`  [${shotNum}] ${fname} FAILED: ${e.message.slice(0, 80)}`);
  }
}

async function scrollSnap(page, name) {
  // viewport snap
  await snap(page, name + '_top', false);
  // scroll mid
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight * 0.5));
  await page.waitForTimeout(400);
  await snap(page, name + '_mid', false);
  // scroll bottom
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(400);
  await snap(page, name + '_bottom', false);
  // scroll back to top
  await page.evaluate(() => window.scrollTo(0, 0));
}

(async () => {
  const browser = await chromium.launch({
    executablePath: '/Users/meharban/Library/Caches/ms-playwright/chromium-1217/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing',
    headless: false,
  });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();
  page.setDefaultTimeout(12000);

  // ════════════ HOMEPAGE (unauthenticated) ════════════
  console.log('\n=== HOMEPAGE (logged out) ===');
  await page.goto(BASE, { waitUntil: 'networkidle' });
  await scrollSnap(page, 'homepage');

  // ════════════ AUTH PAGE ════════════
  console.log('\n=== AUTH PAGE ===');
  await page.goto(`${BASE}/login`, { waitUntil: 'networkidle' });
  await snap(page, 'auth_login');

  // Switch to register tab
  try {
    const regTab = page.locator('button:has-text("Sign Up")').first();
    if (await regTab.isVisible({ timeout: 2000 })) {
      await regTab.click();
      await page.waitForTimeout(400);
      await snap(page, 'auth_register');
    }
  } catch {}

  // Switch back to login and authenticate
  try {
    const loginTab = page.locator('button:has-text("Sign In")').first();
    if (await loginTab.isVisible({ timeout: 1000 })) { await loginTab.click(); await page.waitForTimeout(300); }
  } catch {}

  await page.fill('input[type="email"], input[placeholder*="email" i]', EMAIL);
  await page.fill('input[type="password"]', PASSWORD);
  await snap(page, 'auth_filled');
  // Login button uses onClick not type=submit
  const loginBtn = page.locator('button.btn-sacred, button:has-text("Log"), button:has-text("Sign In")').first();
  await loginBtn.click();
  await page.waitForTimeout(4000);
  await snap(page, 'post_login');

  // ════════════ DASHBOARD ════════════
  console.log('\n=== DASHBOARD ===');
  await page.goto(`${BASE}/dashboard`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  await scrollSnap(page, 'dashboard');

  // ════════════ KUNDLI GENERATOR ════════════
  console.log('\n=== KUNDLI GENERATOR ===');
  await page.goto(`${BASE}/kundli`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);
  await snap(page, 'kundli_form');

  // Fill kundli form
  try {
    const nameInput = page.locator('input#name, input[placeholder*="name" i]').first();
    if (await nameInput.isVisible({ timeout: 2000 })) await nameInput.fill('Test User');
    const dateInput = page.locator('input[type="date"]').first();
    if (await dateInput.isVisible({ timeout: 1000 })) await dateInput.fill('1990-01-15');
    const timeInput = page.locator('input[type="time"]').first();
    if (await timeInput.isVisible({ timeout: 1000 })) await timeInput.fill('06:30');
    const placeInput = page.locator('input[placeholder*="place" i], input[placeholder*="city" i]').first();
    if (await placeInput.isVisible({ timeout: 1000 })) {
      await placeInput.fill('New Delhi');
      await page.waitForTimeout(2000);
      const suggestion = page.locator('li, [role="option"]').first();
      if (await suggestion.isVisible({ timeout: 2000 })) await suggestion.click();
      await page.waitForTimeout(500);
    }
    await snap(page, 'kundli_form_filled');

    // Submit
    const submitBtn = page.locator('button[type="submit"], button:has-text("Generate")').first();
    if (await submitBtn.isVisible({ timeout: 1000 })) {
      await submitBtn.click();
      await page.waitForTimeout(8000); // wait for generation
    }
  } catch (e) { console.log('  Form fill:', e.message.slice(0, 60)); }

  await snap(page, 'kundli_result');

  // ════════════ KUNDLI TABS ════════════
  console.log('\n=== KUNDLI TABS ===');
  // Primary tabs
  const primaryTabs = ['Report', 'Planets', 'Dasha', 'Yoga', 'Divisional', 'Aspects'];
  for (const tab of primaryTabs) {
    try {
      const btn = page.locator(`button:has-text("${tab}")`).first();
      if (await btn.isVisible({ timeout: 1500 })) {
        await btn.click();
        await page.waitForTimeout(2000);
        await snap(page, `kundli_${tab.toLowerCase()}`);
      }
    } catch { console.log(`  Skip: ${tab}`); }
  }

  // "More Analysis" dropdown
  try {
    const moreBtn = page.locator('button:has-text("More Analysis"), button:has-text("More")').first();
    if (await moreBtn.isVisible({ timeout: 1500 })) {
      await moreBtn.click();
      await page.waitForTimeout(500);
      await snap(page, 'kundli_more_dropdown');

      // Click through more tabs
      const moreTabs = ['Shadbala', 'Ashtakvarga', 'Transits', 'Varshphal', 'KP', 'Jaimini',
        'Yogini', 'Sade Sati', 'Mundane', 'Iogita', 'Avakhada', 'Milan', 'Birth', 'Lordships',
        'Upagrahas', 'Sodashvarga'];
      for (const tab of moreTabs) {
        try {
          // Open dropdown
          const mb = page.locator('button:has-text("More Analysis"), button:has-text("More")').first();
          if (await mb.isVisible({ timeout: 500 })) await mb.click();
          await page.waitForTimeout(300);
          const tabBtn = page.locator(`button:has-text("${tab}")`).first();
          if (await tabBtn.isVisible({ timeout: 500 })) {
            await tabBtn.click();
            await page.waitForTimeout(2000);
            await snap(page, `kundli_${tab.toLowerCase().replace(/\s+/g, '_')}`);
          }
        } catch { console.log(`  Skip more: ${tab}`); }
      }
    }
  } catch (e) { console.log('  More dropdown:', e.message.slice(0, 60)); }

  // ════════════ PANCHANG ════════════
  console.log('\n=== PANCHANG ===');
  await page.goto(`${BASE}/panchang`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  await scrollSnap(page, 'panchang');

  // ════════════ LAL KITAB ════════════
  console.log('\n=== LAL KITAB ===');
  await page.goto(`${BASE}/lal-kitab`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await snap(page, 'lalkitab_page');

  // Try to load/generate a kundli
  try {
    // Check for existing kundli list or form submit
    const existingBtn = page.locator('button:has-text("Load"), button:has-text("View"), button:has-text("Select")').first();
    if (await existingBtn.isVisible({ timeout: 2000 })) {
      await existingBtn.click();
      await page.waitForTimeout(3000);
    } else {
      // Try filling form and submitting
      const nameInput = page.locator('input[placeholder*="name" i]').first();
      if (await nameInput.isVisible({ timeout: 1000 })) {
        await nameInput.fill('Test User');
        const dateInput = page.locator('input[type="date"]').first();
        if (await dateInput.isVisible()) await dateInput.fill('1990-01-15');
        const timeInput = page.locator('input[type="time"]').first();
        if (await timeInput.isVisible()) await timeInput.fill('06:30');
        const placeInput = page.locator('input[placeholder*="place" i]').first();
        if (await placeInput.isVisible()) {
          await placeInput.fill('New Delhi');
          await page.waitForTimeout(2000);
          const sugg = page.locator('li, [role="option"]').first();
          if (await sugg.isVisible({ timeout: 2000 })) await sugg.click();
        }
        const submit = page.locator('button[type="submit"], button:has-text("Generate")').first();
        if (await submit.isVisible({ timeout: 1000 })) {
          await submit.click();
          await page.waitForTimeout(5000);
        }
      }
    }
  } catch (e) { console.log('  LK load:', e.message.slice(0, 60)); }

  await snap(page, 'lalkitab_result');

  // LK tabs
  const lkTabs = ['Dashboard', 'Chart', 'Analysis', 'Timing', 'Upay', 'Predictions', 'Nishaniyan', 'Advanced'];
  for (const tab of lkTabs) {
    try {
      const btn = page.locator(`button:has-text("${tab}"), [role="tab"]:has-text("${tab}")`).first();
      if (await btn.isVisible({ timeout: 1500 })) {
        await btn.click();
        await page.waitForTimeout(2000);
        await snap(page, `lk_${tab.toLowerCase()}`);
        // Scroll to see more
        await page.evaluate(() => window.scrollTo(0, 600));
        await page.waitForTimeout(400);
        await snap(page, `lk_${tab.toLowerCase()}_scroll`);
        await page.evaluate(() => window.scrollTo(0, 0));
      }
    } catch { console.log(`  Skip LK: ${tab}`); }
  }

  // ════════════ NUMEROLOGY ════════════
  console.log('\n=== NUMEROLOGY ===');
  await page.goto(`${BASE}/numerology`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await scrollSnap(page, 'numerology');

  // ════════════ VASTU SHASTRA ════════════
  console.log('\n=== VASTU SHASTRA ===');
  await page.goto(`${BASE}/vastu`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await scrollSnap(page, 'vastu');

  // ════════════ FEEDBACK ════════════
  console.log('\n=== FEEDBACK ===');
  await page.goto(`${BASE}/feedback`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);
  await snap(page, 'feedback');

  // ════════════════════════════════════
  //          MOBILE VIEWPORT
  // ════════════════════════════════════
  console.log('\n=== MOBILE (375x812) ===');
  await page.setViewportSize({ width: 375, height: 812 });

  await page.goto(BASE, { waitUntil: 'networkidle' });
  await snap(page, 'mobile_home');
  // Open hamburger
  try {
    const hamburger = page.locator('button[aria-label*="menu" i], button:has(svg)').first();
    if (await hamburger.isVisible({ timeout: 2000 })) {
      await hamburger.click();
      await page.waitForTimeout(500);
      await snap(page, 'mobile_menu');
      await page.keyboard.press('Escape');
    }
  } catch {}

  await page.goto(`${BASE}/login`, { waitUntil: 'networkidle' });
  await snap(page, 'mobile_auth');

  await page.goto(`${BASE}/dashboard`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await snap(page, 'mobile_dashboard');

  await page.goto(`${BASE}/kundli`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);
  await snap(page, 'mobile_kundli');

  await page.goto(`${BASE}/panchang`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await snap(page, 'mobile_panchang');

  await page.goto(`${BASE}/lal-kitab`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);
  await snap(page, 'mobile_lalkitab');

  await page.goto(`${BASE}/numerology`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);
  await snap(page, 'mobile_numerology');

  await page.goto(`${BASE}/vastu`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);
  await snap(page, 'mobile_vastu');

  await page.goto(`${BASE}/feedback`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);
  await snap(page, 'mobile_feedback');

  console.log(`\n=== COMPLETE: ${shotNum} screenshots in ${SHOT_DIR} ===`);
  await browser.close();
})();
