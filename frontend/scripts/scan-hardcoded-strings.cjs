#!/usr/bin/env node
/**
 * scan-hardcoded-strings.cjs — Detect hardcoded user-facing strings in .tsx/.ts files.
 *
 * Scans src/ for English text that should be wrapped in t() or l().
 * Focused on practical detection with low false-positive rate.
 *
 * Usage:
 *   node scripts/scan-hardcoded-strings.cjs          # report issues
 *   node scripts/scan-hardcoded-strings.cjs --fix    # also show suggested t() keys
 *
 * Exit code: 1 if issues found, 0 if clean.
 */
const fs = require('fs');
const path = require('path');

const SRC_DIR = path.resolve(__dirname, '../src');
const FIX_MODE = process.argv.includes('--fix');

// ─── Directories and files to skip ──────────────────────────────────────────
const SKIP_DIRS = new Set([
  'node_modules', 'dist', '.git', 'graphify-out', 'content', 'ui',
]);
const SKIP_FILES = new Set([
  'i18n.ts', 'backend-translations.ts', 'api.ts', 'vite-env.d.ts',
  'puter-ai.ts', 'utils.ts',
]);

// ─── Allowlist patterns — strings matching these are NOT user-facing ────────
// Each entry: regex that matches the raw string value (without surrounding quotes).
const ALLOWLIST = [
  // Technical / format strings
  /^(en|hi|en-IN|hi-IN)$/,
  /^(GET|POST|PUT|DELETE|PATCH|OPTIONS|HEAD)$/,
  /^(application\/json|multipart\/form-data|text\/plain|text\/html)$/,
  /^(utf-8|ascii|base64|hex)$/i,
  /^(YYYY|MM|DD|HH|mm|ss|ISO)/,
  /^\d{4}-\d{2}/,                       // date strings
  /^https?:\/\//,                        // URLs
  /^data:/,                              // data URIs
  /^\//,                                 // absolute paths
  /^\.\//,                               // relative paths
  /^#[0-9a-fA-F]{3,8}$/,                // hex colors
  /^rgb[a]?\(/,
  /^hsl[a]?\(/,
  /^\d+(\.\d+)?(px|em|rem|%|vh|vw|deg|s|ms)?$/, // CSS values
  // CSS property values
  /^(none|auto|inherit|initial|unset|flex|grid|block|inline|inline-block)$/,
  /^(relative|absolute|fixed|sticky|static)$/,
  /^(hidden|visible|scroll|clip)$/,
  /^(center|left|right|top|bottom|start|end|middle|baseline)$/,
  /^(bold|normal|italic|oblique|lighter|bolder)$/,
  /^(solid|dashed|dotted|double|groove|ridge|inset|outset)$/,
  /^(pointer|default|grab|grabbing|text|crosshair|move|not-allowed|wait)$/,
  /^(ease|ease-in|ease-out|ease-in-out|linear|step-start|step-end)$/,
  /^(instant|smooth)$/,
  /^(wrap|nowrap|wrap-reverse)$/,
  /^(contain|cover|fill|scale-down)$/,
  /^(row|column|row-reverse|column-reverse)$/,
  /^(round|square|butt)$/,
  // Font names
  /^(Inter|Segoe|Arial|Helvetica|Verdana|Georgia|Times|Courier|monospace|sans-serif|serif)$/i,
  // File extensions / MIME fragments
  /^(svg|png|jpg|jpeg|gif|webp|pdf|json|csv|xml|html|css|js|ts|tsx)$/,
  // Single characters, empty, pure punctuation/symbols
  /^.?$/,                                // 0 or 1 char
  /^[^a-zA-Z]*$/,                        // no letters at all (pure symbols/numbers)
  // PascalCase identifiers (component/class names)
  /^[A-Z][a-zA-Z0-9]+$/,
  // camelCase identifiers
  /^[a-z][a-zA-Z0-9]+$/,
  // Snake_case or SCREAMING_SNAKE
  /^[a-zA-Z_][a-zA-Z0-9_]+$/,
  // Dot-separated keys (translation keys, config paths)
  /^[a-z][a-zA-Z0-9]*(\.[a-zA-Z0-9_]+)+$/,
  // HTML/SVG tags and attributes
  /^(div|span|p|h[1-6]|a|img|input|button|form|table|tr|td|th|ul|ol|li|section|article|nav|header|footer|main|aside|svg|circle|rect|line|path|g|text|tspan|polygon|polyline|ellipse|defs|use|symbol|mask|clipPath|linearGradient|radialGradient|stop|animate|foreignObject)$/,
  // React/DOM event handlers and props
  /^(onClick|onChange|onSubmit|onBlur|onFocus|onKeyDown|onKeyUp|onMouseEnter|onMouseLeave|onScroll|onLoad|onError|className|htmlFor|tabIndex|aria-|data-)$/,
  // Auth/header tokens
  /^Bearer /,
  /^(Authorization|Content-Type|Accept|X-)$/i,
  // localStorage/sessionStorage keys
  /^(localStorage|sessionStorage|astrorattan-)/,
  // Known technical terms in this astro domain that are NOT translatable
  /^(Rahu|Ketu|Lagna|Navamsa|Dashamsa|Dreshkana|Hora|Saptamsa|Ashtamsa|Dwadasamsa|Shodasamsa|Vimsamsa|Chaturvimsamsa|Saptavimsamsa|Trimsamsa|Khavedamsa|Akshavedamsa|Shashtiamsa)$/,
];

// ─── Props whose values are user-facing ─────────────────────────────────────
const USER_FACING_PROPS = /\b(title|placeholder|label|alt|aria-label|aria-describedby|aria-placeholder)\s*=\s*["']/;

// ─── Line-level skip patterns ───────────────────────────────────────────────
function shouldSkipLine(line) {
  const trimmed = line.trim();
  // Comments
  if (trimmed.startsWith('//') || trimmed.startsWith('*') || trimmed.startsWith('/*')) return true;
  // Imports/exports
  if (trimmed.startsWith('import ') || trimmed.startsWith('export type') || trimmed.startsWith('export interface')) return true;
  // Console statements
  if (/^\s*console\.(log|warn|error|debug|info|trace|assert)\s*\(/.test(trimmed)) return true;
  // Already using t() or l()
  if (/\bt\s*\(/.test(line) || /\bl\s*\(/.test(line)) return true;
  // className prop lines (pure CSS)
  if (/^\s*className\s*=/.test(trimmed)) return true;
  // TypeScript type annotations only
  if (/^\s*(type|interface)\s/.test(trimmed)) return true;
  return false;
}

// ─── Check if a string is on the allowlist ──────────────────────────────────
function isAllowed(str) {
  const s = str.trim();
  if (s.length < 2) return true;
  return ALLOWLIST.some(re => re.test(s));
}

// ─── Generate a suggested t() key from a string ─────────────────────────────
function suggestKey(str) {
  const words = str
    .replace(/[^a-zA-Z0-9\s]/g, '')
    .trim()
    .split(/\s+/)
    .slice(0, 4)
    .map((w, i) => i === 0 ? w.toLowerCase() : w.charAt(0).toUpperCase() + w.slice(1).toLowerCase());
  return 'auto.' + words.join('');
}

// ─── Collect all source files ───────────────────────────────────────────────
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

// ─── Detection logic ────────────────────────────────────────────────────────

/**
 * Category 1: JSX text nodes — English text between > and <
 * Pattern: >Some visible text<
 */
const JSX_TEXT_RE = />\s*([A-Z][a-zA-Z\s,.'!\-?()]{3,80})\s*</g;

/**
 * Category 2: User-facing prop values — title="...", placeholder="...", etc.
 * Pattern: title="Some text" or label='Some text'
 */
const PROP_VALUE_RE = /\b(title|placeholder|label|alt|aria-label)\s*=\s*["']([^"']{2,80})["']/g;

/**
 * Category 3: Object/array literal values that look like UI labels
 * Pattern: { label: "Submit", header: "Results" }
 */
const OBJECT_LABEL_RE = /\b(label|header|title|text|description|message|heading|name|placeholder|tooltip|caption)\s*:\s*['"]([A-Z][a-zA-Z\s,.'!\-?()]{2,80})['"]/g;

function scanFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');
  const relPath = path.relative(SRC_DIR, filePath);
  const findings = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const lineNum = i + 1;

    if (shouldSkipLine(line)) continue;

    // Track what we already found on this line to avoid duplicates
    const foundOnLine = new Set();

    // Category 1: JSX text nodes
    JSX_TEXT_RE.lastIndex = 0;
    let match;
    while ((match = JSX_TEXT_RE.exec(line)) !== null) {
      const text = match[1].trim();
      if (isAllowed(text)) continue;
      // Skip if it contains JSX expressions
      if (text.includes('{') || text.includes('}')) continue;
      const key = `${lineNum}:${text}`;
      if (foundOnLine.has(key)) continue;
      foundOnLine.add(key);
      findings.push({ file: relPath, line: lineNum, text, category: 'JSX_TEXT' });
    }

    // Category 2: User-facing prop values
    PROP_VALUE_RE.lastIndex = 0;
    while ((match = PROP_VALUE_RE.exec(line)) !== null) {
      const text = match[2].trim();
      if (isAllowed(text)) continue;
      const key = `${lineNum}:${text}`;
      if (foundOnLine.has(key)) continue;
      foundOnLine.add(key);
      findings.push({ file: relPath, line: lineNum, text, category: 'PROP_VALUE' });
    }

    // Category 3: Object/array UI labels
    OBJECT_LABEL_RE.lastIndex = 0;
    while ((match = OBJECT_LABEL_RE.exec(line)) !== null) {
      const text = match[2].trim();
      if (isAllowed(text)) continue;
      const key = `${lineNum}:${text}`;
      if (foundOnLine.has(key)) continue;
      foundOnLine.add(key);
      findings.push({ file: relPath, line: lineNum, text, category: 'OBJECT_LABEL' });
    }
  }

  return findings;
}

// ─── Main ───────────────────────────────────────────────────────────────────
const files = getAllFiles(SRC_DIR, ['.tsx', '.ts']);
let allFindings = [];

for (const file of files) {
  allFindings.push(...scanFile(file));
}

// Output
console.log();
console.log('  i18n Hardcoded String Scanner');
console.log('  =============================');
console.log(`  Files scanned:  ${files.length}`);
console.log(`  Issues found:   ${allFindings.length}`);
console.log();

if (allFindings.length === 0) {
  console.log('  All clear — no hardcoded user-facing strings detected.');
  console.log();
  process.exit(0);
}

// Group by file for readable output
const grouped = {};
for (const f of allFindings) {
  if (!grouped[f.file]) grouped[f.file] = [];
  grouped[f.file].push(f);
}

for (const [file, items] of Object.entries(grouped)) {
  console.log(`  ${file}`);
  for (const item of items) {
    let line = `    L${item.line} — "${item.text}" — ${item.category}`;
    if (FIX_MODE) {
      line += `  →  t('${suggestKey(item.text)}')`;
    }
    console.log(line);
  }
  console.log();
}

console.log(`  Total: ${allFindings.length} hardcoded string(s) across ${Object.keys(grouped).length} file(s).`);
if (!FIX_MODE) {
  console.log('  Run with --fix to see suggested t() keys.');
}
console.log();

process.exit(1);
