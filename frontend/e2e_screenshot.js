const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('http://localhost:5199/login');
  await page.screenshot({ path: 'login-debug.png' });
  await browser.close();
})();
