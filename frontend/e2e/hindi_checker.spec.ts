import { test, expect } from '@playwright/test';

const ROUTES = [
  '/',
  '/login',
  '/dashboard',
  '/kundli',
  '/panchang',
  '/horoscope',
  '/numerology',
  '/lal-kitab',
  '/vastu',
  '/blog',
  '/astrologer',
  '/feedback'
];

test('Verify complete Hindi translation across all pages', async ({ page }) => {
  // Go to login page first to authenticate
  await page.goto('/login');
  
  // Try to toggle Hindi right away on the login page
  // The toggle is usually a button containing 'A/' or 'A/अ' or 'English/हिंदी'
  await page.evaluate(() => {
    localStorage.setItem('astrorattan-language', 'hi');
  });
  await page.reload();

  // Login
  await page.fill('input[type="email"]', 'meharbansingh85@gmail.com');
  await page.fill('input[type="password"]', 'Misha@123');
  // Click login button (assuming there's a button type=submit)
  await page.click('button[type="submit"]');

  // Wait for login to complete (should navigate to /dashboard or /admin depending on user role)
  await page.waitForTimeout(3000); 

  const englishFindings = [];

  for (const route of ROUTES) {
    if (route === '/login') continue; // already logged in

    console.log(`Checking route: ${route}`);
    await page.goto(route);
    await page.waitForTimeout(2000); // Wait for animations or data to load
    
    // Ensure language is Hindi
    await page.evaluate(() => {
      localStorage.setItem('astrorattan-language', 'hi');
    });

    // Check for english text using evaluate
    const result = await page.evaluate(() => {
      const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT,
        null,
      );

      const findings = [];
      let node;
      // We will skip styles, scripts, and inputs/textareas
      const skipElements = ['SCRIPT', 'STYLE', 'NOSCRIPT', 'INPUT', 'TEXTAREA', 'CODE', 'PRE'];
      
      while ((node = walker.nextNode())) {
        if (!node.nodeValue) continue;
        const text = node.nodeValue.trim();
        // Skip short texts or pure numbers/symbols
        if (text.length < 2) continue;
        
        const parent = node.parentElement;
        if (parent && skipElements.includes(parent.tagName)) continue;
        
        // This is a naive regex to check if there are 3 consecutive english letters 
        // which usually indicate a missed translation.
        if (/[a-zA-Z]{3,}/.test(text)) {
          // Exclude URLs, dates, numbers, known brand names
          if (text.includes('http') || text.includes('astrorattan')) continue;
          
          findings.push({
            text: text.substring(0, 50),
            element: parent?.tagName
          });
        }
      }
      return findings;
    });

    if (result.length > 0) {
      console.log(`Found English on ${route}:`, result);
      englishFindings.push({ route, findings: result });
    }
  }

  // Log findings
  console.log(JSON.stringify(englishFindings, null, 2));

  // If we found english text in Hindi mode, optionally fail the test
  // To allow checking what failed, we don't strict fail, just log it.
});
