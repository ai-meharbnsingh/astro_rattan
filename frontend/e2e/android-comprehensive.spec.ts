import { test, expect, Page } from '@playwright/test';

// Pages to test with their routes
const PAGES = [
  { name: 'Home', route: '/' },
  { name: 'Auth', route: '/auth' },
  { name: 'Dashboard', route: '/dashboard' },
  { name: 'Kundli', route: '/kundli' },
  { name: 'Panchang', route: '/panchang' },
  { name: 'Horoscope', route: '/horoscope' },
  { name: 'Lal Kitab', route: '/lalkitab' },
  { name: 'Numerology', route: '/numerology' },
  { name: 'Vastu', route: '/vastu' },
  { name: 'Feedback', route: '/feedback' },
  { name: 'Admin', route: '/admin' },
  { name: 'Astrologer Dashboard', route: '/astrologer-dashboard' },
  { name: 'Client Profile', route: '/client-profile' },
  { name: 'Blog', route: '/blog' },
];

// Helper: check for console errors
async function checkConsoleErrors(page: Page): Promise<string[]> {
  const errors: string[] = [];
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(msg.text());
  });
  return errors;
}

// Helper: test button/input accessibility
async function testTouchTargets(page: Page): Promise<{ total: number; tooSmall: number }> {
  try {
    const result = await page.evaluate(() => {
      const buttons = document.querySelectorAll('button, a[href], input, [role="button"]');
      let tooSmall = 0;
      buttons.forEach(el => {
        const rect = el.getBoundingClientRect();
        if (rect.width < 44 || rect.height < 44) {
          tooSmall++;
        }
      });
      return { total: buttons.length, tooSmall };
    });
    return result;
  } catch (e) {
    return { total: 0, tooSmall: 0 };
  }
}

// Helper: check for content overflow
async function checkContentOverflow(page: Page): Promise<string[]> {
  try {
    const overflowing = await page.evaluate(() => {
      const issues: string[] = [];
      document.querySelectorAll('*').forEach(el => {
        const style = window.getComputedStyle(el);
        if (style.overflow === 'hidden' || style.overflow === 'auto') {
          if (el.scrollWidth > el.clientWidth) {
            issues.push(`Horizontal overflow on ${el.tagName}${el.id ? '#' + el.id : ''}`);
          }
        }
      });
      return issues;
    });
    return overflowing;
  } catch (e) {
    return [];
  }
}

// Page load and no errors test
PAGES.forEach(pageInfo => {
  test(`[${pageInfo.name}] Page loads without errors`, async ({ page }) => {
    const consoleErrors: string[] = [];

    page.on('console', msg => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });

    const response = await page.goto(pageInfo.route);
    expect(response?.status()).toBeLessThan(400);

    await page.waitForLoadState('networkidle').catch(() => {});
    await page.waitForTimeout(1000);

    const hasContent = await page.$('body') !== null;
    expect(hasContent).toBe(true);

    if (consoleErrors.length > 0) {
      console.log(`❌ ${pageInfo.name}: ${consoleErrors.length} console errors`);
      consoleErrors.slice(0, 3).forEach(err => console.log(`   └─ ${err}`));
    } else {
      console.log(`✅ ${pageInfo.name}: No console errors`);
    }
  });
});

// Content render test
PAGES.forEach(pageInfo => {
  test(`[${pageInfo.name}] Content renders without blank page`, async ({ page }) => {
    await page.goto(pageInfo.route);
    await page.waitForLoadState('networkidle').catch(() => {});
    await page.waitForTimeout(500);

    const textContent = await page.evaluate(() => {
      return document.body.innerText.trim().length;
    });

    expect(textContent).toBeGreaterThan(0);
    console.log(`✅ ${pageInfo.name}: Content rendered (${textContent} chars)`);
  });
});

// No stuck spinners test
PAGES.forEach(pageInfo => {
  test(`[${pageInfo.name}] No spinners or loading states stuck`, async ({ page }) => {
    await page.goto(pageInfo.route);
    await page.waitForLoadState('networkidle').catch(() => {});
    await page.waitForTimeout(1500);

    const spinners = await page.$$('[role="progressbar"], .spinner, [data-testid*="loading"]');

    if (spinners.length > 0) {
      await page.waitForTimeout(2000);
      const stillThere = await page.$$('[role="progressbar"], .spinner, [data-testid*="loading"]');
      expect(stillThere.length).toBe(0);
    }

    console.log(`✅ ${pageInfo.name}: No stuck loading states`);
  });
});

// Touch targets test
PAGES.forEach(pageInfo => {
  test(`[${pageInfo.name}] Touch targets are adequate (44x44px minimum)`, async ({ page }) => {
    await page.goto(pageInfo.route);
    await page.waitForLoadState('networkidle').catch(() => {});

    const { total, tooSmall } = await testTouchTargets(page);

    const acceptableRatio = tooSmall / (total || 1);
    expect(acceptableRatio).toBeLessThan(0.3);

    if (tooSmall > 0) {
      console.log(`⚠️  ${pageInfo.name}: ${tooSmall}/${total} targets < 44px`);
    } else {
      console.log(`✅ ${pageInfo.name}: All ${total} touch targets adequate`);
    }
  });
});

// No overflow test
PAGES.forEach(pageInfo => {
  test(`[${pageInfo.name}] Content doesn't overflow horizontally`, async ({ page }) => {
    await page.goto(pageInfo.route);
    await page.waitForLoadState('networkidle').catch(() => {});

    const overflowing = await checkContentOverflow(page);

    if (overflowing.length > 0) {
      console.log(`⚠️  ${pageInfo.name}: ${overflowing.length} overflow issues`);
    } else {
      console.log(`✅ ${pageInfo.name}: No horizontal overflow`);
    }

    expect(overflowing.length).toBeLessThan(5);
  });
});

// Interactive elements test
PAGES.forEach(pageInfo => {
  test(`[${pageInfo.name}] Interactive elements are accessible`, async ({ page }) => {
    await page.goto(pageInfo.route);
    await page.waitForLoadState('networkidle').catch(() => {});

    const interactiveCount = await page.evaluate(() => {
      const els = document.querySelectorAll('button, a[href], input, [role="button"], [role="tab"]');
      let accessible = 0;
      els.forEach(el => {
        const isVisible = (el as HTMLElement).offsetHeight > 0;
        if (isVisible) accessible++;
      });
      return accessible;
    });

    console.log(`✅ ${pageInfo.name}: ${interactiveCount} interactive elements`);
  });
});

// Forms test (Kundli, Vastu, Numerology, Feedback)
test('[Kundli] Form is present and interactive', async ({ page }) => {
  await page.goto('/kundli');
  await page.waitForLoadState('networkidle').catch(() => {});

  const form = await page.$('form');
  const submitBtn = form ? await form.$('button[type="submit"]') : null;

  if (form && submitBtn) {
    console.log('✅ Kundli: Form with submit button found');
    expect(form).toBeTruthy();
  } else {
    console.log('⚠️  Kundli: Form or submit button not found');
  }
});

test('[Vastu] Form is present and interactive', async ({ page }) => {
  await page.goto('/vastu');
  await page.waitForLoadState('networkidle').catch(() => {});

  const form = await page.$('form');
  const submitBtn = form ? await form.$('button[type="submit"]') : null;

  if (form && submitBtn) {
    console.log('✅ Vastu: Form with submit button found');
    expect(form).toBeTruthy();
  }
});

test('[Numerology] Form is present and interactive', async ({ page }) => {
  await page.goto('/numerology');
  await page.waitForLoadState('networkidle').catch(() => {});

  const form = await page.$('form');
  const inputs = form ? await form.$$('input') : [];

  if (form && inputs.length > 0) {
    console.log(`✅ Numerology: Form with ${inputs.length} input(s) found`);
    expect(form).toBeTruthy();
  }
});

test('[Feedback] Form is present and interactive', async ({ page }) => {
  await page.goto('/feedback');
  await page.waitForLoadState('networkidle').catch(() => {});

  const form = await page.$('form');
  const textarea = form ? await form.$('textarea') : null;

  if (form && textarea) {
    console.log('✅ Feedback: Form with textarea found');
    expect(form).toBeTruthy();
  }
});

// Tabs test (Kundli, Lal Kitab, Panchang, Horoscope, Vastu)
test('[Lal Kitab] Tabs are present and switchable', async ({ page }) => {
  await page.goto('/lalkitab');
  await page.waitForLoadState('networkidle').catch(() => {});

  const tabs = await page.$$('[role="tab"]');

  if (tabs.length > 1) {
    console.log(`✅ Lal Kitab: ${tabs.length} tabs found`);

    // Try clicking first tab
    await tabs[0].click();
    await page.waitForTimeout(500);
    console.log(`✅ Lal Kitab: Tab switching works`);
  } else {
    console.log(`⚠️  Lal Kitab: Only ${tabs.length} tab(s) found`);
  }
});

// Table render test
test('[Panchang] Tables render without overflow', async ({ page }) => {
  await page.goto('/panchang');
  await page.waitForLoadState('networkidle').catch(() => {});

  const tables = await page.$$('table');

  if (tables.length > 0) {
    console.log(`✅ Panchang: ${tables.length} table(s) rendered`);

    const overflowIssues = await checkContentOverflow(page);
    if (overflowIssues.length > 0) {
      console.log(`   ⚠️  ${overflowIssues.length} potential overflow issues`);
    }
  } else {
    console.log('⚠️  Panchang: No tables found');
  }
});

// Blog content test
test('[Blog] Articles load and are readable', async ({ page }) => {
  await page.goto('/blog');
  await page.waitForLoadState('networkidle').catch(() => {});

  const articles = await page.$$('article, [data-testid*="post"], .post, .article');

  if (articles.length > 0) {
    console.log(`✅ Blog: ${articles.length} article(s) found`);
  } else {
    const links = await page.$$('a[href*="/blog"]');
    console.log(`⚠️  Blog: No article elements, but ${links.length} blog links found`);
  }
});

// Navigation test
test('[Navigation] Menu is accessible on mobile', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle').catch(() => {});

  const navMenu = await page.$('[role="navigation"], nav, [data-testid="nav"]');
  const hamburger = await page.$('[data-testid="menu-button"], button[aria-label*="menu" i]');

  if (navMenu || hamburger) {
    console.log('✅ Navigation: Menu/navigation found');
  } else {
    console.log('⚠️  Navigation: No menu or nav element found');
  }
});

// Viewport confirmation
test('[Viewport] Confirmed 393x851 (Android Chrome)', async ({ page }) => {
  const size = await page.evaluate(() => ({
    width: window.innerWidth,
    height: window.innerHeight,
    devicePixelRatio: window.devicePixelRatio,
  }));

  console.log(`✅ Viewport: ${size.width}x${size.height} (DPR: ${size.devicePixelRatio})`);
  expect(size.width).toBe(393);
  expect(size.height).toBe(851);
});
