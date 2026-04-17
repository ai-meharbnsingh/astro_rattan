#!/usr/bin/env node
/**
 * validate-i18n-keys.cjs — Validate translation key completeness.
 *
 * 1. Parses src/lib/i18n.ts to extract all defined keys for 'en' and 'hi'.
 * 2. Scans all .tsx/.ts files for t('...') calls to find all USED keys.
 * 3. Reports:
 *    - Keys used in code but MISSING from i18n.ts (broken translations)
 *    - Keys defined in 'en' but missing from 'hi' (incomplete Hindi)
 *    - Keys defined in 'hi' but missing from 'en' (incomplete English)
 *    - Keys defined but never used (orphans) — warning only
 *
 * Exit code: 1 if any MISSING keys found, 0 if all keys present.
 */
const fs = require('fs');
const path = require('path');

const SRC_DIR = path.resolve(__dirname, '../src');
const I18N_PATH = path.resolve(__dirname, '../src/lib/i18n.ts');

// ─── Directories/files to skip when scanning for usage ──────────────────────
const SKIP_DIRS = new Set(['node_modules', 'dist', '.git', 'graphify-out', 'content']);
const SKIP_FILES = new Set(['i18n.ts', 'vite-env.d.ts']);

// ─── Step 1: Extract defined keys from i18n.ts ─────────────────────────────

function extractKeysFromBlock(content, blockMarker) {
  const idx = content.indexOf(blockMarker);
  if (idx === -1) return new Set();

  // Find the opening { after the block marker
  let braceStart = content.indexOf('{', idx);
  if (braceStart === -1) return new Set();

  // Track brace depth to find the matching closing }
  let depth = 0;
  let blockEnd = braceStart;
  for (let i = braceStart; i < content.length; i++) {
    if (content[i] === '{') depth++;
    if (content[i] === '}') depth--;
    if (depth === 0) { blockEnd = i; break; }
  }

  const block = content.slice(braceStart, blockEnd + 1);
  const keys = new Set();
  // Match keys like 'auto.keyName': or "blog.title":
  const regex = /['"]([a-zA-Z][a-zA-Z0-9_.]+)['"]\s*:/g;
  let match;
  while ((match = regex.exec(block)) !== null) {
    keys.add(match[1]);
  }
  return keys;
}

const i18nContent = fs.readFileSync(I18N_PATH, 'utf-8');

const enKeys = extractKeysFromBlock(i18nContent, 'en: {');
const hiKeys = extractKeysFromBlock(i18nContent, 'hi: {');

if (enKeys.size === 0) {
  console.error('  ERROR: Could not parse EN block from i18n.ts');
  process.exit(1);
}
if (hiKeys.size === 0) {
  console.error('  ERROR: Could not parse HI block from i18n.ts');
  process.exit(1);
}

// All defined keys (union of en and hi)
const allDefinedKeys = new Set([...enKeys, ...hiKeys]);

// ─── Step 2: Scan source files for t('...') usage ──────────────────────────

function getAllFiles(dir, extensions) {
  const results = [];
  let items;
  try { items = fs.readdirSync(dir, { withFileTypes: true }); } catch { return results; }
  for (const item of items) {
    if (SKIP_DIRS.has(item.name)) continue;
    const fullPath = path.join(dir, item.name);
    if (item.isDirectory()) {
      results.push(...getAllFiles(fullPath, extensions));
    } else if (extensions.some(e => item.name.endsWith(e)) && !SKIP_FILES.has(item.name)) {
      results.push(fullPath);
    }
  }
  return results;
}

// Collect all t('key') usages with file locations
const usedKeys = new Map(); // key -> [{ file, line }]

// Match t('key'), t("key"), t(`key`)
const T_CALL_RE = /\bt\s*\(\s*['"`]([a-zA-Z][a-zA-Z0-9_.]+)['"`]\s*\)/g;

const files = getAllFiles(SRC_DIR, ['.tsx', '.ts']);

for (const filePath of files) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');
  const relPath = path.relative(SRC_DIR, filePath);

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    T_CALL_RE.lastIndex = 0;
    let match;
    while ((match = T_CALL_RE.exec(line)) !== null) {
      const key = match[1];
      if (!usedKeys.has(key)) usedKeys.set(key, []);
      usedKeys.get(key).push({ file: relPath, line: i + 1 });
    }
  }
}

// ─── Step 3: Compute differences ────────────────────────────────────────────

// 3a. Keys used in code but MISSING from i18n.ts
const missingFromI18n = [];
for (const [key, locations] of usedKeys) {
  if (!allDefinedKeys.has(key)) {
    missingFromI18n.push({ key, locations });
  }
}
missingFromI18n.sort((a, b) => a.key.localeCompare(b.key));

// 3b. Keys in EN but missing from HI
const missingInHi = [...enKeys].filter(k => !hiKeys.has(k)).sort();

// 3c. Keys in HI but missing from EN
const missingInEn = [...hiKeys].filter(k => !enKeys.has(k)).sort();

// 3d. Keys defined but never used (orphans) — warning only
const orphanKeys = [...allDefinedKeys].filter(k => !usedKeys.has(k)).sort();

// ─── Step 4: Output report ──────────────────────────────────────────────────

console.log();
console.log('  i18n Key Validator');
console.log('  ==================');
console.log(`  English keys defined: ${enKeys.size}`);
console.log(`  Hindi keys defined:   ${hiKeys.size}`);
console.log(`  Keys used in code:    ${usedKeys.size}`);
console.log(`  Source files scanned: ${files.length}`);
console.log();

let hasErrors = false;

// Missing from i18n.ts entirely (broken translations)
if (missingFromI18n.length > 0) {
  hasErrors = true;
  console.log(`  MISSING from i18n.ts (${missingFromI18n.length}) — these t() calls will show raw keys:`);
  for (const { key, locations } of missingFromI18n) {
    const loc = locations.map(l => `${l.file}:${l.line}`).join(', ');
    console.log(`    - "${key}"  used in: ${loc}`);
  }
  console.log();
}

// Missing in Hindi
if (missingInHi.length > 0) {
  hasErrors = true;
  console.log(`  MISSING in Hindi (${missingInHi.length}) — defined in EN but not HI:`);
  for (const k of missingInHi) {
    console.log(`    - ${k}`);
  }
  console.log();
}

// Missing in English
if (missingInEn.length > 0) {
  hasErrors = true;
  console.log(`  MISSING in English (${missingInEn.length}) — defined in HI but not EN:`);
  for (const k of missingInEn) {
    console.log(`    - ${k}`);
  }
  console.log();
}

// Orphan keys (warning only, does not cause failure)
if (orphanKeys.length > 0) {
  console.log(`  ORPHANS (${orphanKeys.length}) — defined but never used via t() (warning only):`);
  // Show first 20 to avoid noise
  const shown = orphanKeys.slice(0, 20);
  for (const k of shown) {
    console.log(`    - ${k}`);
  }
  if (orphanKeys.length > 20) {
    console.log(`    ... and ${orphanKeys.length - 20} more`);
  }
  console.log();
}

// Final verdict
if (hasErrors) {
  console.log('  FAIL — Fix missing translation keys before proceeding.');
  console.log();
  process.exit(1);
} else {
  console.log('  PASS — All translation keys are complete and matched.');
  console.log();
  process.exit(0);
}
