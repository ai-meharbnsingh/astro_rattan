#!/usr/bin/env node
/**
 * check-i18n.js — Verify EN/HI key parity in i18n.ts
 *
 * Exits with code 1 if any key is missing in either language.
 * Run: node scripts/check-i18n.js
 */
const fs = require('fs');
const path = require('path');

const I18N_PATH = path.resolve(__dirname, '../src/lib/i18n.ts');
const content = fs.readFileSync(I18N_PATH, 'utf-8');

// Extract all translation keys from a block like: 'key.name': 'value',
function extractKeys(text, blockStart) {
  const idx = text.indexOf(blockStart);
  if (idx === -1) return new Set();

  // Find the opening { after the block marker
  let braceStart = text.indexOf('{', idx);
  if (braceStart === -1) return new Set();

  // Track brace depth to find the matching }
  let depth = 0;
  let blockEnd = braceStart;
  for (let i = braceStart; i < text.length; i++) {
    if (text[i] === '{') depth++;
    if (text[i] === '}') depth--;
    if (depth === 0) { blockEnd = i; break; }
  }

  const block = text.slice(braceStart, blockEnd + 1);
  const keys = new Set();
  const regex = /['"]([a-zA-Z0-9_.]+)['"]\s*:/g;
  let match;
  while ((match = regex.exec(block)) !== null) {
    keys.add(match[1]);
  }
  return keys;
}

// Find EN and HI blocks — look for the language identifier patterns
const enKeys = extractKeys(content, "en: {");
const hiKeys = extractKeys(content, "hi: {");

// If we couldn't extract properly, try alternative patterns
if (enKeys.size === 0 || hiKeys.size === 0) {
  // Try splitting by the two large objects
  const sections = content.split(/const\s+\w+\s*[:=]/);
  console.error('Could not parse i18n.ts blocks. Trying regex fallback...');

  // Fallback: just find all 'key.name' patterns in EN vs HI sections
  const halfPoint = Math.floor(content.length / 2);
  const firstHalf = content.slice(0, halfPoint);
  const secondHalf = content.slice(halfPoint);

  const keyRegex = /['"]([a-zA-Z][a-zA-Z0-9_.]{2,})['"]\s*:/g;

  if (enKeys.size === 0) {
    let m;
    while ((m = keyRegex.exec(firstHalf)) !== null) enKeys.add(m[1]);
  }
  if (hiKeys.size === 0) {
    let m;
    while ((m = keyRegex.exec(secondHalf)) !== null) hiKeys.add(m[1]);
  }
}

// Compare
const missingInHi = [...enKeys].filter(k => !hiKeys.has(k)).sort();
const missingInEn = [...hiKeys].filter(k => !enKeys.has(k)).sort();

console.log(`\n  i18n Key Parity Check`);
console.log(`  =====================`);
console.log(`  English keys: ${enKeys.size}`);
console.log(`  Hindi keys:   ${hiKeys.size}`);

let failed = false;

if (missingInHi.length > 0) {
  console.log(`\n  MISSING in Hindi (${missingInHi.length}):`);
  missingInHi.forEach(k => console.log(`    - ${k}`));
  failed = true;
}

if (missingInEn.length > 0) {
  console.log(`\n  MISSING in English (${missingInEn.length}):`);
  missingInEn.forEach(k => console.log(`    - ${k}`));
  failed = true;
}

if (failed) {
  console.log(`\n  FAIL — Fix missing keys before building.\n`);
  process.exit(1);
} else {
  console.log(`\n  PASS — Perfect parity. ${enKeys.size} keys matched.\n`);
  process.exit(0);
}
