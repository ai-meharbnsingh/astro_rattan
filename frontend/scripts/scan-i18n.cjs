#!/usr/bin/env node
/**
 * scan-i18n.js — Find hardcoded strings NOT wrapped in t() or translation keys
 *
 * Scans all .tsx/.ts files in src/ for suspected hardcoded user-facing strings.
 * Outputs: file path + line number + the hardcoded string
 * Saves report to i18n-report.txt
 *
 * Run: node scripts/scan-i18n.js
 */
const fs = require('fs');
const path = require('path');

const SRC_DIR = path.resolve(__dirname, '../src');
const REPORT_PATH = path.resolve(__dirname, '../i18n-report.txt');

// Patterns to IGNORE (not user-facing)
const IGNORE_PATTERNS = [
  /^['"`]use (strict|client)['"`]/,           // directives
  /^['"`](GET|POST|PUT|DELETE|PATCH)['"`]/,   // HTTP methods
  /^['"`]\//,                                  // paths starting with /
  /^['"`]#/,                                   // hex colors
  /^['"`]\./,                                  // class names, file paths
  /^['"`]https?:/,                             // URLs
  /^['"`]data:/,                               // data URIs
  /^['"`]image\//,                             // MIME types
  /^['"`]application\//,
  /^['"`]text\//,
  /^['"`][a-z]+\/[a-z]/,                       // MIME-like
  /^['"`]\d+['"`]/,                            // pure numbers
  /^['"`]\d+px['"`]/,                          // CSS values
  /^['"`]\d+%['"`]/,
  /^['"`]rgb/,
  /^['"`]hsl/,
  /^['"`]flex/,                                // CSS
  /^['"`]grid/,
  /^['"`]none['"`]/,
  /^['"`]auto['"`]/,
  /^['"`]inherit['"`]/,
  /^['"`]center['"`]/,
  /^['"`]middle['"`]/,
  /^['"`]left['"`]/,
  /^['"`]right['"`]/,
  /^['"`]top['"`]/,
  /^['"`]bottom['"`]/,
  /^['"`]bold['"`]/,
  /^['"`]normal['"`]/,
  /^['"`]solid['"`]/,
  /^['"`]relative['"`]/,
  /^['"`]absolute['"`]/,
  /^['"`]fixed['"`]/,
  /^['"`]hidden['"`]/,
  /^['"`]visible['"`]/,
  /^['"`]scroll['"`]/,
  /^['"`]wrap['"`]/,
  /^['"`]block['"`]/,
  /^['"`]inline/,
  /^['"`]pointer['"`]/,
  /^['"`]default['"`]/,
  /^['"`]smooth['"`]/,
  /^['"`]ease/,
  /^['"`]linear['"`]/,
  /^['"`]instant['"`]/,
  /^['"`]round/,
  /^['"`]square['"`]/,
  /^['"`]butt['"`]/,
  /^['"`]Inter['"`]/,                          // font names
  /^['"`]Segoe/,
  /^['"`]sans-serif['"`]/,
  /^['"`]monospace['"`]/,
  /^['"`]serif['"`]/,
  /^['"`]svg['"`]/,
  /^['"`]png['"`]/,
  /^['"`]jpg['"`]/,
  /^['"`]pdf['"`]/,
  /^['"`]json['"`]/,
  /^['"`]text['"`]/,
  /^['"`]utf-8['"`]/,
  /^['"`]Bearer /,                             // auth
  /^['"`]token/,
  /^['"`]localStorage/,
  /^['"`]Authorization['"`]/,
  /^['"`]Content-Type['"`]/,
  /^['"`]Accept['"`]/,
  /^['"`]application\/json['"`]/,
  /^['"`]multipart/,
  /^['"`]boundary/,
  /^['"`]X-/,                                  // custom headers
  /^['"`]aria-/,                               // accessibility
  /^['"`]data-/,                               // data attributes
  /^['"`]role['"`]/,
  /^['"`]type['"`]/,
  /^['"`]className['"`]/,
  /^['"`]onClick['"`]/,
  /^['"`]onChange['"`]/,
  /^['"`]onSubmit['"`]/,
  /^['"`]placeholder['"`]/,
  /^['"`]disabled['"`]/,
  /^['"`]checked['"`]/,
  /^['"`]value['"`]/,
  /^['"`]key['"`]/,
  /^['"`]id['"`]/,
  /^['"`]name['"`]/,
  /^['"`]ref['"`]/,
  /^['"`]style['"`]/,
  /^['"`]children['"`]/,
  /^['"`]string['"`]/,                         // TypeScript types
  /^['"`]number['"`]/,
  /^['"`]boolean['"`]/,
  /^['"`]object['"`]/,
  /^['"`]function['"`]/,
  /^['"`]undefined['"`]/,
  /^['"`]null['"`]/,
  /^['"`]true['"`]/,
  /^['"`]false['"`]/,
  /^['"`]en['"`]/,                             // language codes
  /^['"`]hi['"`]/,
  /^['"`]en-/,
  /^['"`]hi-/,
  /^['"`]YYYY/,                                // date formats
  /^['"`]MM/,
  /^['"`]DD/,
  /^['"`]HH/,
  /^['"`]mm/,
  /^['"`]ss/,
  /^['"`]T\d/,
  /^['"`][A-Z][a-z]{2,8}['"`]$/,              // single short words (likely keys/enums)
  /^['"`]&/,                                   // HTML entities
  /^['"`]\\u/,                                 // unicode escapes
  /^['"`]☀/,                                   // symbols
  /^['"`]☽/,
  /^['"`]☆/,
  /^['"`]●/,
  /^['"`]▲/,
  /^['"`]🌕/,
  /^['"`]\*/,                                  // retro symbol
  /^['"`]\^/,                                  // combust symbol
  /^['"`]\+/,                                  // vargottama symbol
];

// Files/dirs to skip
const SKIP_DIRS = new Set(['node_modules', 'dist', '.git', 'graphify-out', 'content']);
const SKIP_FILES = new Set(['i18n.ts', 'backend-translations.ts', 'api.ts', 'vite-env.d.ts']);

function getAllFiles(dir, ext) {
  const results = [];
  const items = fs.readdirSync(dir, { withFileTypes: true });
  for (const item of items) {
    if (SKIP_DIRS.has(item.name)) continue;
    const fullPath = path.join(dir, item.name);
    if (item.isDirectory()) {
      results.push(...getAllFiles(fullPath, ext));
    } else if (ext.some(e => item.name.endsWith(e)) && !SKIP_FILES.has(item.name)) {
      results.push(fullPath);
    }
  }
  return results;
}

// Detect suspected hardcoded user-facing strings
// Look for: JSX text content, string props that look like labels
const HARDCODED_REGEX = /(?:>|=\{?)\s*['"`]([A-Z][a-zA-Z\s]{3,60})['"`]/g;
const JSX_TEXT_REGEX = />\s*([A-Z][a-zA-Z\s,.'!?]{4,80})\s*</g;

const files = getAllFiles(SRC_DIR, ['.tsx', '.ts']);
const findings = [];

for (const filePath of files) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');
  const relPath = path.relative(SRC_DIR, filePath);

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const lineNum = i + 1;

    // Skip comments, imports, type definitions
    const trimmed = line.trim();
    if (trimmed.startsWith('//') || trimmed.startsWith('*') || trimmed.startsWith('/*')) continue;
    if (trimmed.startsWith('import ') || trimmed.startsWith('export type') || trimmed.startsWith('export interface')) continue;
    if (trimmed.startsWith('console.')) continue;

    // Skip lines that already use t() or translation
    if (line.includes('t(') || line.includes('t(`') || line.includes("t('")) continue;
    if (line.includes('language ===') || line.includes('isHi ?') || line.includes('l(')) continue;

    // Check for JSX text content (English text between > and <)
    let match;
    JSX_TEXT_REGEX.lastIndex = 0;
    while ((match = JSX_TEXT_REGEX.exec(line)) !== null) {
      const text = match[1].trim();
      if (text.length < 5) continue;
      if (/^[A-Z][a-z]+$/.test(text)) continue; // Single word component name
      if (IGNORE_PATTERNS.some(p => p.test(`'${text}'`))) continue;

      findings.push({
        file: relPath,
        line: lineNum,
        text: text.slice(0, 60),
        type: 'JSX_TEXT',
      });
    }

    // Check for string props that look like labels
    HARDCODED_REGEX.lastIndex = 0;
    while ((match = HARDCODED_REGEX.exec(line)) !== null) {
      const text = match[1].trim();
      if (text.length < 5) continue;
      if (/^[A-Z][a-z]+$/.test(text)) continue;
      if (IGNORE_PATTERNS.some(p => p.test(`'${text}'`))) continue;

      // Avoid duplicates from JSX_TEXT
      if (findings.some(f => f.file === relPath && f.line === lineNum && f.text === text.slice(0, 60))) continue;

      findings.push({
        file: relPath,
        line: lineNum,
        text: text.slice(0, 60),
        type: 'STRING_PROP',
      });
    }
  }
}

// Generate report
const header = `i18n Hardcoded String Scan Report
Generated: ${new Date().toISOString()}
Files scanned: ${files.length}
Suspected hardcoded strings: ${findings.length}
${'='.repeat(70)}\n`;

let report = header;

if (findings.length === 0) {
  report += '\nNo hardcoded strings found. All clear!\n';
} else {
  // Group by file
  const grouped = {};
  for (const f of findings) {
    if (!grouped[f.file]) grouped[f.file] = [];
    grouped[f.file].push(f);
  }

  for (const [file, items] of Object.entries(grouped)) {
    report += `\n${file}\n${'-'.repeat(file.length)}\n`;
    for (const item of items) {
      report += `  L${item.line}: [${item.type}] "${item.text}"\n`;
    }
  }
}

fs.writeFileSync(REPORT_PATH, report);

console.log(`\n  i18n Hardcoded String Scanner`);
console.log(`  ============================`);
console.log(`  Files scanned:  ${files.length}`);
console.log(`  Suspects found: ${findings.length}`);
console.log(`  Report saved:   i18n-report.txt\n`);

if (findings.length > 0) {
  // Show top 10
  const top = findings.slice(0, 10);
  top.forEach(f => console.log(`    ${f.file}:${f.line} → "${f.text}"`));
  if (findings.length > 10) console.log(`    ... and ${findings.length - 10} more`);
  console.log();
}
