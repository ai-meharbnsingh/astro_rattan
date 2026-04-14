const fs = require('fs');
const path = require('path');

let enKeys = {};
let hiKeys = {};

function toCamelCase(str) {
  return str.replace(/(?:^\w|[A-Z]|\b\w)/g, (word, index) => {
    return index === 0 ? word.toLowerCase() : word.toUpperCase();
  }).replace(/\s+/g, '').replace(/[^a-zA-Z0-9]/g, '').slice(0, 20);
}

function processComponent(filePath) {
  let content = fs.readFileSync(filePath, 'utf8');
  let changed = false;

  // Regex for `isHi ? 'Hindi' : 'English'` or `language === 'hi' ? "Hindi" : "English"`
  // Handle both single and double quotes
  const regex = /(isHi|language\s*===\s*'hi'|lang\s*===\s*'hi'|language\s*===\s*"hi"|lang\s*===\s*"hi")\s*\?\s*(['"`])([^'"`]+)\2\s*:\s*(['"`])([^'"`]+)\4/g;

  content = content.replace(regex, (match, condition, q1, hiStr, q2, enStr) => {
    // Generate key based on enStr
    const baseKey = toCamelCase(enStr);
    const key = `auto.${baseKey}`;
    
    enKeys[key] = enStr;
    hiKeys[key] = hiStr;
    
    changed = true;
    return `t('${key}')`;
  });

  // Also catch `{isHi ? 'A' : 'B'}` and replace with `{t('auto.B')}` if matched inside JSX
  // The above regex already does the replacement, so `{isHi ? 'A' : 'B'}` becomes `{t('auto.B')}` which is valid JSX!
  
  if (changed) {
    // Need to make sure `t` is available.
    // If it's not, we might break the file. We assume `t` is available or `useTranslation()` is used if it used `language` or `isHi`!
    if (!content.includes('const {') || !content.includes('t')) {
       // if `t` is missing, inject it. But wait, `language` was used, so `useTranslation` must be there.
       if (!content.includes(' t ') && !content.includes(', t') && !content.includes('t,')) {
         content = content.replace(/const\s*{\s*([^}]+)\s*}\s*=\s*useTranslation\(\)/, "const { $1, t } = useTranslation()");
       }
    }
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`Updated ${filePath}`);
  }
}

function walk(dir) {
  fs.readdirSync(dir).forEach(file => {
    const p = path.join(dir, file);
    if (fs.statSync(p).isDirectory()) walk(p);
    else if (p.endsWith('.tsx') || p.endsWith('.ts')) processComponent(p);
  });
}

walk('src/components');
walk('src/sections');

// Now update i18n.ts
if (Object.keys(enKeys).length > 0) {
  let i18n = fs.readFileSync('src/lib/i18n.ts', 'utf8');
  
  let enInsert = '';
  for (const [k, v] of Object.entries(enKeys)) {
    enInsert += `    '${k}': '${v.replace(/'/g, "\\'")}',\n`;
  }
  
  let hiInsert = '';
  for (const [k, v] of Object.entries(hiKeys)) {
    hiInsert += `    '${k}': '${v.replace(/'/g, "\\'")}',\n`;
  }
  
  i18n = i18n.replace(/en: \{/, `en: {\n${enInsert}`);
  i18n = i18n.replace(/hi: \{/, `hi: {\n${hiInsert}`);
  
  fs.writeFileSync('src/lib/i18n.ts', i18n, 'utf8');
  console.log(`Added ${Object.keys(enKeys).length} auto keys to i18n.ts`);
}

