/**
 * capture_screenshots.js — v2
 * Captures 6 showcase screenshots for astrorattan.com
 * Run: node scripts/capture_screenshots.js
 *
 * Key fixes vs v1:
 *  - Creates dummy clients via API (not UI automation)
 *  - Correct place autocomplete selector: div.absolute button[type="button"]
 *  - Fills phone number (required for astrologer new-client mode)
 *  - Uses [role="tab"] to click Chart / Upay tabs in LalKitab
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const BASE_URL = 'https://astrorattan.com';
const TOKEN = process.env.ASTRORATTAN_TOKEN || '';
const OUT_DIR = path.join(__dirname, '../frontend/public/images/showcase');
const VIEWPORT = { width: 1280, height: 800 };

const ARJUN = {
  name: 'Arjun Sharma',
  date: '1990-03-15',
  time: '06:30',
  place: 'New Delhi',
  lat: 28.6139,
  lon: 77.2090,
  phone: '9999999999',
};

const DUMMY_CLIENTS = [
  { name: 'Priya Mehta',   gender: 'female', birth_date: '1985-08-22', birth_place: 'Mumbai',  phone: '9876543210' },
  { name: 'Rohit Verma',   gender: 'male',   birth_date: '1992-01-07', birth_place: 'Jaipur',  phone: '9876543211' },
  { name: 'Sunita Kapoor', gender: 'female', birth_date: '1978-11-14', birth_place: 'Lucknow', phone: '9876543212' },
];

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function injectAuth(page) {
  await page.evaluate((token) => localStorage.setItem('astrorattan_token', token), TOKEN);
  await page.reload({ waitUntil: 'networkidle' });
  await sleep(500);
}

async function screenshot(page, filename) {
  const outPath = path.join(OUT_DIR, filename);
  await page.screenshot({ path: outPath, fullPage: false });
  console.log(`  ✓ saved ${filename}`);
}

// ── Create clients via REST API (no UI automation needed) ────────────────────
async function createClientsViaAPI(page) {
  console.log('\n[API] Creating dummy clients...');
  for (const client of DUMMY_CLIENTS) {
    const result = await page.evaluate(async ({ client, token }) => {
      try {
        const resp = await fetch('/api/clients', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
          body: JSON.stringify(client),
        });
        const data = await resp.json();
        return { status: resp.status, data };
      } catch (e) {
        return { error: e.message };
      }
    }, { client, token: TOKEN });
    if (result.status === 201) {
      console.log(`  ✓ Created ${client.name} (id: ${result.data.id || '?'})`);
    } else if (result.error) {
      console.log(`  ⚠ ${client.name}: ${result.error}`);
    } else {
      console.log(`  ⚠ ${client.name}: HTTP ${result.status} — ${JSON.stringify(result.data).slice(0, 80)}`);
    }
  }
}

// ── Fill the shared kundli / lalkitab form ───────────────────────────────────
async function fillBirthForm(page) {
  // Name — KundliForm uses "Full Name", LalKitabForm uses "Enter your name"
  const nameField = page.locator(
    'input[placeholder*="Full Name" i], input[placeholder*="पूरा नाम"], input[placeholder*="Enter your name" i], input[placeholder*="अपना नाम"]'
  ).first();
  if (await nameField.count() > 0) {
    await nameField.click();
    await nameField.fill(ARJUN.name);
  } else {
    console.log('  ⚠ name field not found');
  }

  // Date
  const dateField = page.locator('input[type="date"]').first();
  if (await dateField.count() > 0) await dateField.fill(ARJUN.date);

  // Time
  const timeField = page.locator('input[type="time"]').first();
  if (await timeField.count() > 0) await timeField.fill(ARJUN.time);

  // Place (triggers geocode autocomplete debounced at ~400ms)
  const placeField = page.locator('input[placeholder*="Birth Place" i], input[placeholder*="जन्म स्थान"]').first();
  if (await placeField.count() > 0) {
    await placeField.click();
    await placeField.fill('');
    // Type slowly so the onChange fires and debounce triggers
    await placeField.type(ARJUN.place, { delay: 80 });
    await sleep(2000); // Wait for debounced API call + render

    // Suggestions render as: div.absolute > button[type="button"]
    const suggestion = page.locator('div[class*="absolute"] button[type="button"]').first();
    if (await suggestion.count() > 0) {
      await suggestion.click();
      console.log('  ✓ Autocomplete suggestion clicked');
      await sleep(300);
    } else {
      // Fallback: no dropdown appeared — lat/lon will be 0,0. Try pressing Enter.
      console.log('  ⚠ No autocomplete suggestion visible');
    }
  }

  // Phone (shown for astrologers in New Client mode)
  const phoneField = page.locator('input[placeholder*="phone" i], input[placeholder*="फ़ोन"]').first();
  if (await phoneField.count() > 0) {
    await phoneField.fill(ARJUN.phone);
  }
}

// ── Wait for any chart / result content to appear ───────────────────────────
async function waitForChart(page, timeout = 20000) {
  try {
    await page.waitForSelector(
      'svg, canvas, [role="tab"], [class*="chart"], [class*="planet"], table',
      { timeout }
    );
    await sleep(2500);
  } catch {
    console.log('  ⚠ Chart selector timeout — proceeding');
    await sleep(2500);
  }
}

async function main() {
  if (!TOKEN) {
    console.error('Fatal: ASTRORATTAN_TOKEN environment variable is required');
    process.exit(1);
  }
  fs.mkdirSync(OUT_DIR, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: VIEWPORT });
  const page = await context.newPage();

  // ── Auth ─────────────────────────────────────────────────────
  console.log('\n[Auth] Injecting token...');
  await page.goto(BASE_URL, { waitUntil: 'domcontentloaded' });
  await injectAuth(page);

  // ── Create dummy clients ──────────────────────────────────────
  await createClientsViaAPI(page);

  // ── SCREENSHOT 1: Kundli Engine ──────────────────────────────
  console.log('\n[1/6] Kundli Engine...');
  await page.goto(`${BASE_URL}/kundli`, { waitUntil: 'networkidle' });
  await sleep(1500);

  await fillBirthForm(page);

  const kundliBtn = page.locator('button').filter({ hasText: /Generate Kundli|कुंडली बनाएं/i }).first();
  if (await kundliBtn.count() > 0) {
    await kundliBtn.click();
    console.log('  Generating Kundli...');
    await waitForChart(page, 25000);
  } else {
    console.log('  ⚠ Generate Kundli button not found');
  }
  await screenshot(page, 'showcase-kundli.png');

  // ── SCREENSHOT 2: Lal Kitab (Chart tab) ──────────────────────
  console.log('\n[2/6] Lal Kitab...');
  await page.goto(`${BASE_URL}/lal-kitab`, { waitUntil: 'networkidle' });
  await sleep(1500);

  await fillBirthForm(page);

  const lkBtn = page.locator('button').filter({ hasText: /Generate|Analyse|Generate Chart|चार्ट बनाएं/i }).first();
  if (await lkBtn.count() > 0) {
    await lkBtn.click();
    console.log('  Generating LalKitab chart...');
    await waitForChart(page, 25000);
  }

  // Click "Chart" tab for the visual wheel
  const chartTab = page.locator('[role="tab"]').filter({ hasText: /^Chart$/ }).first();
  if (await chartTab.count() > 0) {
    await chartTab.click();
    await sleep(1500);
    console.log('  ✓ Switched to Chart tab');
  }
  await screenshot(page, 'showcase-lalkitab.png');

  // ── SCREENSHOT 3: Panchang ────────────────────────────────────
  console.log('\n[3/6] Panchang...');
  await page.goto(`${BASE_URL}/panchang`, { waitUntil: 'networkidle' });
  await sleep(3000);
  await screenshot(page, 'showcase-panchang.png');

  // ── SCREENSHOT 4: Numerology ──────────────────────────────────
  console.log('\n[4/6] Numerology...');
  await page.goto(`${BASE_URL}/numerology`, { waitUntil: 'networkidle' });
  await sleep(1000);

  const numName = page.locator('input[placeholder*="name" i]').first();
  if (await numName.count() > 0) {
    await numName.fill(ARJUN.name);
    const numDate = page.locator('input[type="date"]').first();
    if (await numDate.count() > 0) await numDate.fill(ARJUN.date);

    const calcBtn = page.locator('button').filter({ hasText: /calculate|generate|analyse/i }).first();
    if (await calcBtn.count() > 0) {
      await calcBtn.click();
      try {
        await page.waitForSelector('[class*="number"], [class*="grid"], table, [class*="result"]', { timeout: 8000 });
      } catch { /* continue */ }
      await sleep(2000);
      // Scroll down to show actual numerology numbers grid
      await page.evaluate(() => window.scrollBy(0, 350));
      await sleep(500);
    }
  }
  await screenshot(page, 'showcase-numerology.png');

  // ── SCREENSHOT 5: Client Manager ─────────────────────────────
  console.log('\n[5/6] Client Manager...');
  await page.goto(`${BASE_URL}/dashboard`, { waitUntil: 'networkidle' });
  await sleep(3000);
  await screenshot(page, 'showcase-clients.png');

  // ── SCREENSHOT 6: Chandra Chalana (Lal Kitab → Upay tab) ─────
  console.log('\n[6/6] Chandra Chalana...');
  await page.goto(`${BASE_URL}/lal-kitab`, { waitUntil: 'networkidle' });
  await sleep(1500);

  await fillBirthForm(page);

  const lkBtn2 = page.locator('button').filter({ hasText: /Generate|Analyse|Generate Chart|चार्ट बनाएं/i }).first();
  if (await lkBtn2.count() > 0) {
    await lkBtn2.click();
    console.log('  Generating LalKitab chart...');
    await waitForChart(page, 25000);
  }

  // Click "Upay" tab — contains LalKitabChandraChaalanaTab (3rd component, below Remedies)
  const upayTab = page.locator('[role="tab"]').filter({ hasText: /^Upay$/ }).first();
  if (await upayTab.count() > 0) {
    await upayTab.click();
    console.log('  ✓ Switched to Upay tab (contains Chandra Chalana)');
    await sleep(2500);
    // Chandra Chalana is the 3rd section in Upay — scroll past Remedies & Tracker
    await page.evaluate(() => {
      const el = document.querySelector('[class*="chandra"], [class*="Chandra"], h2, h3');
      const sections = Array.from(document.querySelectorAll('section, [class*="card"], [class*="Card"]'));
      // Try to scroll to element with "Chandra" text
      const chandraEl = Array.from(document.querySelectorAll('*')).find(
        e => e.children.length === 0 && /chandra/i.test(e.textContent || '')
      );
      if (chandraEl) chandraEl.scrollIntoView({ block: 'start' });
      else window.scrollBy(0, 900);
    });
    await sleep(800);
  } else {
    console.log('  ⚠ Upay tab not found');
  }
  await screenshot(page, 'showcase-chandra.png');

  await browser.close();
  console.log('\n✅ All 6 screenshots captured →', OUT_DIR);
}

main().catch(e => { console.error('Fatal:', e.message); process.exit(1); });
