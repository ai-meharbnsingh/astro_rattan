import { chromium } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';

const BASE_URL = process.env.FONT_VERIFY_BASE_URL || 'http://127.0.0.1:5173';
const OUT_DIR = path.resolve('font-verification');
fs.mkdirSync(OUT_DIR, { recursive: true });

const pages = [
  { path: '/', key: 'home' },
  { path: '/kundli', key: 'kundli' },
  { path: '/panchang', key: 'panchang' },
  { path: '/lal-kitab', key: 'lal-kitab' },
  { path: '/numerology', key: 'numerology' },
  { path: '/dashboard', key: 'dashboard' },
  { path: '/admin', key: 'admin' },
];

const viewports = [
  { key: 'desktop', viewport: { width: 1280, height: 800 } },
  { key: 'mobile', viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 },
];

function includesAny(v, needles) {
  const lc = (v || '').toLowerCase();
  return needles.some((n) => lc.includes(n.toLowerCase()));
}

async function collectFonts(page) {
  return page.evaluate(() => {
    const get = (sel) => document.querySelector(sel);
    const fontOf = (el) => (el ? window.getComputedStyle(el).fontFamily : 'N/A');
    const styleOf = (el) => (el ? el.style.fontFamily || '' : '');

    const bodyEl = document.body;
    const headingEl = get('h1') || get('h2');
    const pEl = get('p');
    const btnEl = get('button');
    const inputEl = get('input');
    const tdEl = get('td');

    const walker = document.createTreeWalker(document.body || document.documentElement, NodeFilter.SHOW_TEXT);
    let devanagariNode = null;
    while (walker.nextNode()) {
      const text = (walker.currentNode.nodeValue || '').trim();
      if (/[\u0900-\u097F]/.test(text)) {
        devanagariNode = walker.currentNode.parentElement;
        break;
      }
    }

    return {
      url: window.location.pathname,
      bodyFont: fontOf(bodyEl),
      headingFont: fontOf(headingEl),
      pFont: fontOf(pEl),
      buttonFont: fontOf(btnEl),
      inputFont: fontOf(inputEl),
      tdFont: fontOf(tdEl),
      hindiFont: fontOf(devanagariNode),
      rawStyle: {
        body: styleOf(bodyEl),
        heading: styleOf(headingEl),
        p: styleOf(pEl),
      },
    };
  });
}

function statusFor(row) {
  const bodyOk = includesAny(row.bodyFont, ['inter']);
  const headingOk = row.headingFont === 'N/A' || includesAny(row.headingFont, ['cormorant garamond']);
  const hindiOk = row.hindiFont === 'N/A' || includesAny(row.hindiFont, ['hind', 'noto sans devanagari']);
  const uiOk = [row.pFont, row.buttonFont, row.inputFont, row.tdFont]
    .filter((v) => v && v !== 'N/A')
    .every((v) => includesAny(v, ['inter']) && !includesAny(v, ['cormorant garamond']));

  return {
    bodyOk,
    headingOk,
    hindiOk,
    uiOk,
    pass: bodyOk && headingOk && hindiOk && uiOk,
  };
}

const browser = await chromium.launch({ headless: true });
const allRows = [];

for (const vp of viewports) {
  const context = await browser.newContext({
    viewport: vp.viewport,
    isMobile: vp.isMobile || false,
    hasTouch: vp.hasTouch || false,
    deviceScaleFactor: vp.deviceScaleFactor || 1,
  });

  for (const p of pages) {
    const page = await context.newPage();
    const target = `${BASE_URL}${p.path}`;

    await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(() => {});
    await page.waitForTimeout(1200);

    // Ensure English baseline for body/UI checks
    await page.evaluate(() => localStorage.setItem('astrorattan-language', 'en')).catch(() => {});
    await page.reload({ waitUntil: 'domcontentloaded' }).catch(() => {});
    await page.waitForTimeout(900);

    const en = await collectFonts(page);
    await page.screenshot({ path: path.join(OUT_DIR, `verify-fonts-${p.key}-${vp.key}.png`), fullPage: true });

    // Hindi pass
    await page.evaluate(() => localStorage.setItem('astrorattan-language', 'hi')).catch(() => {});
    await page.reload({ waitUntil: 'domcontentloaded' }).catch(() => {});
    await page.waitForTimeout(1200);
    const hi = await collectFonts(page);

    const check = statusFor({ ...en, hindiFont: hi.hindiFont });
    allRows.push({
      page: p.path,
      viewport: vp.key,
      finalUrl: en.url,
      bodyFont: en.bodyFont,
      headingFont: en.headingFont,
      hindiFont: hi.hindiFont,
      pFont: en.pFont,
      buttonFont: en.buttonFont,
      inputFont: en.inputFont,
      tdFont: en.tdFont,
      rawBodyStyle: en.rawStyle.body,
      rawHeadingStyle: en.rawStyle.heading,
      rawPStyle: en.rawStyle.p,
      ...check,
    });

    await page.close();
  }

  await context.close();
}

await browser.close();

const reportPath = path.join(OUT_DIR, 'font-report.json');
fs.writeFileSync(reportPath, JSON.stringify(allRows, null, 2));

const header = ['Page', 'Viewport', 'Body Font', 'H1/H2 Font', 'Hindi Font', 'Status'];
const lines = [header.join(' | ')];
for (const row of allRows) {
  lines.push([
    row.page,
    row.viewport,
    row.bodyFont,
    row.headingFont,
    row.hindiFont,
    row.pass ? 'PASS' : 'FAIL',
  ].join(' | '));
}

const textReport = lines.join('\n');
fs.writeFileSync(path.join(OUT_DIR, 'font-report.txt'), textReport);
console.log(textReport);
