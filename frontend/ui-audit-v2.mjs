import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';

const BASE = 'http://localhost:5173';
const EMAIL = 'meharbansingh85@gmail.com';
const PASSWORD = 'Misha@2311';
const SHOT_DIR = path.resolve('ui-screenshots/audit-v2');
fs.mkdirSync(SHOT_DIR, { recursive: true });

let shotNum = 0;
async function snap(page, name) {
  shotNum++;
  const fname = `${String(shotNum).padStart(2, '0')}_${name}.png`;
  try {
    // Clip to viewport only - never full page (avoids font timeout)
    await page.screenshot({ path: path.join(SHOT_DIR, fname), fullPage: false, timeout: 10000 });
    console.log(`  [${shotNum}] ${fname}`);
  } catch (e) {
    console.log(`  [${shotNum}] ${fname} FAILED: ${e.message.split('\n')[0].slice(0, 80)}`);
  }
}

(async () => {
  const browser = await chromium.launch({
    executablePath: '/Users/meharban/Library/Caches/ms-playwright/chromium-1217/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing',
    headless: true,
  });
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  page.setDefaultTimeout(10000);

  // ═══ HOMEPAGE ═══
  console.log('\n=== HOMEPAGE ===');
  await page.goto(BASE, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);
  await snap(page, 'home_hero');
  await page.evaluate(() => window.scrollBy(0, 900));
  await page.waitForTimeout(500);
  await snap(page, 'home_features');
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(500);
  await snap(page, 'home_footer');

  // ═══ AUTH ═══
  console.log('\n=== AUTH ===');
  await page.goto(`${BASE}/login`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1500);
  await snap(page, 'auth_login');
  try {
    await page.click('button:has-text("Sign Up")', { timeout: 2000 });
    await page.waitForTimeout(400);
    await snap(page, 'auth_register');
    await page.click('button:has-text("Sign In")', { timeout: 1000 });
    await page.waitForTimeout(300);
  } catch {}

  // Login
  await page.fill('input[type="email"]', EMAIL);
  await page.fill('input[type="password"]', PASSWORD);
  await snap(page, 'auth_filled');
  await page.click('button.btn-sacred');
  await page.waitForTimeout(4000);
  await snap(page, 'post_login');

  // ═══ DASHBOARD ═══
  console.log('\n=== DASHBOARD ===');
  await page.goto(`${BASE}/dashboard`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2500);
  await snap(page, 'dashboard');
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(400);
  await snap(page, 'dashboard_bottom');

  // ═══ KUNDLI ═══
  console.log('\n=== KUNDLI ===');
  await page.goto(`${BASE}/kundli`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1500);
  await snap(page, 'kundli_form');

  // Fill form
  try {
    await page.fill('input#name', 'Test User');
    await page.fill('input[type="date"]', '1990-01-15');
    await page.fill('input[type="time"]', '06:30');
    const place = page.locator('input[placeholder*="place" i], input[placeholder*="city" i], input[placeholder*="birth" i]').first();
    await place.fill('New Delhi');
    await page.waitForTimeout(2000);
    const sugg = page.locator('li').first();
    if (await sugg.isVisible({ timeout: 2000 })) await sugg.click();
    await page.waitForTimeout(500);
    await snap(page, 'kundli_filled');

    await page.click('button:has-text("Generate")');
    await page.waitForTimeout(8000);
    await snap(page, 'kundli_result');
  } catch (e) { console.log('  Fill error:', e.message.split('\n')[0].slice(0, 60)); }

  // Kundli primary tabs
  console.log('\n=== KUNDLI TABS ===');
  for (const tab of ['Report', 'Planets', 'Dasha', 'Yoga', 'Divisional', 'Aspects']) {
    try {
      await page.click(`button:has-text("${tab}")`, { timeout: 2000 });
      await page.waitForTimeout(2000);
      await snap(page, `kundli_${tab.toLowerCase()}`);
    } catch { console.log(`  Skip: ${tab}`); }
  }

  // More Analysis dropdown
  try {
    const more = page.locator('button:has-text("More Analysis")').first();
    if (await more.isVisible({ timeout: 1500 })) {
      await more.click();
      await page.waitForTimeout(500);
      await snap(page, 'kundli_more_open');
      for (const t of ['Shadbala', 'Ashtakvarga', 'Transits', 'KP', 'Jaimini', 'Varshphal', 'Yogini', 'Sade', 'Avakhada', 'Milan', 'Birth', 'Mundane']) {
        try {
          const mb = page.locator('button:has-text("More Analysis")').first();
          if (await mb.isVisible({ timeout: 500 })) await mb.click();
          await page.waitForTimeout(300);
          await page.click(`button:has-text("${t}")`, { timeout: 1000 });
          await page.waitForTimeout(2000);
          await snap(page, `kundli_${t.toLowerCase()}`);
        } catch { console.log(`  Skip more: ${t}`); }
      }
    }
  } catch {}

  // ═══ PANCHANG ═══
  console.log('\n=== PANCHANG ===');
  await page.goto(`${BASE}/panchang`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(3000);
  await snap(page, 'panchang');
  await page.evaluate(() => window.scrollBy(0, 800));
  await page.waitForTimeout(400);
  await snap(page, 'panchang_scroll');

  // ═══ LAL KITAB ═══
  console.log('\n=== LAL KITAB ===');
  await page.goto(`${BASE}/lal-kitab`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);
  await snap(page, 'lalkitab_form');

  // Generate/load kundli for LK
  try {
    await page.fill('input#name, input[placeholder*="name" i]', 'Test User');
    await page.fill('input[type="date"]', '1990-01-15');
    await page.fill('input[type="time"]', '06:30');
    const place = page.locator('input[placeholder*="place" i], input[placeholder*="city" i]').first();
    await place.fill('New Delhi');
    await page.waitForTimeout(2000);
    const sugg = page.locator('li').first();
    if (await sugg.isVisible({ timeout: 2000 })) await sugg.click();
    await page.waitForTimeout(500);
    await page.click('button:has-text("Generate")');
    await page.waitForTimeout(6000);
    await snap(page, 'lalkitab_result');
  } catch (e) { console.log('  LK fill:', e.message.split('\n')[0].slice(0, 60)); }

  // LK tabs
  for (const tab of ['Dashboard', 'Chart', 'Analysis', 'Timing', 'Upay', 'Predictions', 'Nishaniyan', 'Advanced']) {
    try {
      await page.click(`button:has-text("${tab}"), [role="tab"]:has-text("${tab}")`, { timeout: 1500 });
      await page.waitForTimeout(2000);
      await snap(page, `lk_${tab.toLowerCase()}`);
      await page.evaluate(() => window.scrollBy(0, 600));
      await page.waitForTimeout(300);
      await snap(page, `lk_${tab.toLowerCase()}_more`);
      await page.evaluate(() => window.scrollTo(0, 0));
    } catch { console.log(`  Skip LK: ${tab}`); }
  }

  // ═══ NUMEROLOGY ═══
  console.log('\n=== NUMEROLOGY ===');
  await page.goto(`${BASE}/numerology`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);
  await snap(page, 'numerology');
  await page.evaluate(() => window.scrollBy(0, 800));
  await page.waitForTimeout(400);
  await snap(page, 'numerology_more');

  // ═══ VASTU ═══
  console.log('\n=== VASTU ===');
  await page.goto(`${BASE}/vastu`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);
  await snap(page, 'vastu');
  await page.evaluate(() => window.scrollBy(0, 800));
  await page.waitForTimeout(400);
  await snap(page, 'vastu_more');

  // ═══ FEEDBACK ═══
  console.log('\n=== FEEDBACK ===');
  await page.goto(`${BASE}/feedback`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1500);
  await snap(page, 'feedback');

  // ═══════════════════════
  //      MOBILE (375x812)
  // ═══════════════════════
  console.log('\n=== MOBILE ===');
  await page.setViewportSize({ width: 375, height: 812 });

  for (const [route, name] of [
    ['/', 'mob_home'],
    ['/login', 'mob_auth'],
    ['/dashboard', 'mob_dashboard'],
    ['/kundli', 'mob_kundli'],
    ['/panchang', 'mob_panchang'],
    ['/lal-kitab', 'mob_lalkitab'],
    ['/numerology', 'mob_numerology'],
    ['/vastu', 'mob_vastu'],
    ['/feedback', 'mob_feedback'],
  ]) {
    await page.goto(`${BASE}${route}`, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);
    await snap(page, name);
  }

  // Mobile hamburger
  try {
    await page.goto(BASE, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1000);
    const ham = page.locator('button').filter({ has: page.locator('svg.lucide-menu') }).first();
    if (await ham.isVisible({ timeout: 2000 })) {
      await ham.click();
      await page.waitForTimeout(500);
      await snap(page, 'mob_menu_open');
    }
  } catch {}

  console.log(`\n=== DONE: ${shotNum} screenshots in ${SHOT_DIR} ===`);
  await browser.close();
})();
