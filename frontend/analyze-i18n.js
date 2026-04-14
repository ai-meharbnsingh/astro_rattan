import fs from 'fs';
import path from 'path';

function walk(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  list.forEach((file) => {
    file = path.join(dir, file);
    const stat = fs.statSync(file);
    if (stat && stat.isDirectory()) {
      results = results.concat(walk(file));
    } else {
      if (file.endsWith('.tsx') || file.endsWith('.ts')) {
        results.push(file);
      }
    }
  });
  return results;
}

const files = walk('./src');

let report = '';
let hardcodedCount = 0;

for (const file of files) {
  const content = fs.readFileSync(file, 'utf8');
  const lines = content.split('\n');
  
  // Basic regexes to detect hardcoded text:
  // 1. Text inside JSX elements: >Some Text<
  // 2. Hardcoded attributes: placeholder="Some text"
  const lineMatches = [];
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    // Ignore console.log and errors
    if (line.includes('console.')) continue;
    if (line.includes('Error(')) continue;
    
    // Catch > text < where text has at least one letter and isn't purely a variable like >{x}<
    const jsxTextRegex = />([^<{]*)<|>\s*([^<{]+)\s*\{/g;
    let match;
    let hasMatch = false;
    
    while ((match = jsxTextRegex.exec(line)) !== null) {
      const text = match[1] || match[2];
      if (text && text.trim().match(/[a-zA-Z]{2,}/) && !text.trim().match(/^[0-9\s:%\-+.,]+$/)) {
        // Exclude specific known internal strings if needed
        hasMatch = true;
      }
    }
    
    // Attributes
    const attrs = ['placeholder', 'title', 'label', 'aria-label'];
    for (const attr of attrs) {
       if (line.match(new RegExp(`${attr}="([^"]*[a-zA-Z]{2,}[^"]*)"`))) {
         hasMatch = true;
       }
       if (line.match(new RegExp(`${attr}='([^']*[a-zA-Z]{2,}[^']*)'`))) {
         hasMatch = true;
       }
    }

    if (hasMatch) {
       lineMatches.push({ lineNum: i + 1, text: line.trim() });
       hardcodedCount++;
    }
  }
  
  if (lineMatches.length > 0) {
     report += `\nFile: ${file}\n`;
     for (const m of lineMatches) {
        report += `  Line ${m.lineNum}: ${m.text}\n`;
     }
  }
}

fs.writeFileSync('i18n-report.txt', `Total suspected hardcoded strings: ${hardcodedCount}\n\n` + report);
console.log('Done, saved to i18n-report.txt');
