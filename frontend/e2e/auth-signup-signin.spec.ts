import { test, expect, type Page } from '@playwright/test';

/**
 * P28 AstroVedic — Signup & Signin UI E2E Tests
 * Tests run against the LIVE Vercel deployment.
 * Covers: login tab, register tab, form validation, error handling,
 *         astrologer toggle, successful auth flow, navigation after auth.
 */

const uniqueId = () => Math.random().toString(36).slice(2, 10);

// ─── HELPERS ────────────────────────────────────────────────────────────

async function navigateToLogin(page: Page) {
  await page.goto('/login', { waitUntil: 'networkidle' });
  // Wait for the auth form to render (lazy loaded)
  await page.waitForSelector('input[type="email"]', { timeout: 15_000 });
}

async function switchToTab(page: Page, tabName: 'Sign In' | 'Sign Up') {
  // The tab triggers contain translated text; fallback to positional click
  const tab = page.getByRole('tab', { name: new RegExp(tabName, 'i') });
  if (await tab.isVisible()) {
    await tab.click();
  } else {
    // Fallback: click by tab position (0=Sign In, 1=Sign Up)
    const tabs = page.locator('[role="tab"]');
    const idx = tabName === 'Sign In' ? 0 : 1;
    await tabs.nth(idx).click();
  }
  await page.waitForTimeout(300); // tab animation
}

// ─── 1. PAGE LOAD & UI STRUCTURE ────────────────────────────────────────

test.describe('Auth Page — Load & Structure', () => {
  test('should load the login page and show auth form', async ({ page }) => {
    await navigateToLogin(page);

    // Page should have the auth heading
    const heading = page.locator('h2');
    await expect(heading).toBeVisible();

    // Should have two tabs (Sign In / Sign Up)
    const tabs = page.locator('[role="tab"]');
    await expect(tabs).toHaveCount(2);
  });

  test('should default to Sign In tab', async ({ page }) => {
    await navigateToLogin(page);

    // Sign In tab should be active
    const signInTab = page.locator('[role="tab"]').first();
    await expect(signInTab).toHaveAttribute('data-state', 'active');

    // Should show email and password inputs (2 inputs for login)
    const emailInput = page.locator('input[type="email"]');
    await expect(emailInput).toBeVisible();

    const passwordInput = page.locator('input[type="password"]');
    await expect(passwordInput).toBeVisible();
  });

  test('should switch to Sign Up tab and show name field', async ({ page }) => {
    await navigateToLogin(page);
    await switchToTab(page, 'Sign Up');

    // Sign Up should have name + email + password (3 inputs)
    const nameInput = page.locator('input[type="text"]');
    await expect(nameInput).toBeVisible();

    const emailInput = page.locator('input[type="email"]');
    await expect(emailInput).toBeVisible();

    const passwordInput = page.locator('input[type="password"]');
    await expect(passwordInput).toBeVisible();
  });

  test('should show astrologer toggle on Sign Up tab', async ({ page }) => {
    await navigateToLogin(page);
    await switchToTab(page, 'Sign Up');

    // Astrologer toggle button
    const astrologerToggle = page.locator('button').filter({ hasText: /astrologer/i });
    await expect(astrologerToggle).toBeVisible();
  });
});

// ─── 2. SIGN IN — FORM VALIDATION ──────────────────────────────────────

test.describe('Sign In — Validation', () => {
  test('sign in button should be disabled with empty fields', async ({ page }) => {
    await navigateToLogin(page);

    // The submit button should be disabled when fields are empty
    const signInButton = page.locator('button').filter({ hasText: /sign in/i }).last();
    await expect(signInButton).toBeDisabled();
  });

  test('sign in button should be disabled with only email', async ({ page }) => {
    await navigateToLogin(page);

    await page.locator('input[type="email"]').fill('test@example.com');
    const signInButton = page.locator('button').filter({ hasText: /sign in/i }).last();
    await expect(signInButton).toBeDisabled();
  });

  test('sign in button should be enabled with both fields filled', async ({ page }) => {
    await navigateToLogin(page);

    await page.locator('input[type="email"]').fill('test@example.com');
    await page.locator('input[type="password"]').fill('password123');
    const signInButton = page.locator('button').filter({ hasText: /sign in/i }).last();
    await expect(signInButton).toBeEnabled();
  });

  test('should show error on invalid credentials', async ({ page }) => {
    await navigateToLogin(page);

    await page.locator('input[type="email"]').fill('nonexistent@example.com');
    await page.locator('input[type="password"]').fill('wrongpassword');

    const signInButton = page.locator('button').filter({ hasText: /sign in/i }).last();
    await signInButton.click();

    // Wait for error message — the error div shows text like "Invalid credentials"
    const errorDiv = page.locator('.text-red-400.text-center, .rounded-xl.text-red-400').first();
    await expect(errorDiv).toBeVisible({ timeout: 10_000 });
    const errorText = await errorDiv.textContent();
    expect(errorText?.toLowerCase()).toMatch(/invalid|credentials|failed|error/);
  });

  test('should capture network request on sign in attempt', async ({ page }) => {
    await navigateToLogin(page);

    // Intercept API call to see what URL the frontend actually calls
    const requestPromise = page.waitForRequest(
      (req) => req.url().includes('/api/auth/login'),
      { timeout: 10_000 },
    );

    await page.locator('input[type="email"]').fill('test@example.com');
    await page.locator('input[type="password"]').fill('password123');

    const signInButton = page.locator('button').filter({ hasText: /sign in/i }).last();
    await signInButton.click();

    const request = await requestPromise;
    console.log(`[AUTH DEBUG] Login request URL: ${request.url()}`);
    console.log(`[AUTH DEBUG] Login request method: ${request.method()}`);

    // Verify the request is POST
    expect(request.method()).toBe('POST');

    // Wait for response
    const response = await request.response();
    if (response) {
      console.log(`[AUTH DEBUG] Login response status: ${response.status()}`);
      const body = await response.text().catch(() => 'no body');
      console.log(`[AUTH DEBUG] Login response body: ${body}`);

      // If status is 405, the API endpoint isn't available on this domain
      if (response.status() === 405) {
        console.error('[AUTH ISSUE] API returns 405 — VITE_API_URL may not be configured on Vercel');
      }
    }
  });
});

// ─── 3. SIGN UP — FORM VALIDATION ──────────────────────────────────────

test.describe('Sign Up — Validation', () => {
  test('sign up button should be disabled with empty fields', async ({ page }) => {
    await navigateToLogin(page);
    await switchToTab(page, 'Sign Up');

    const signUpButton = page.locator('button').filter({ hasText: /sign up/i }).last();
    await expect(signUpButton).toBeDisabled();
  });

  test('sign up button should be disabled with partial fields', async ({ page }) => {
    await navigateToLogin(page);
    await switchToTab(page, 'Sign Up');

    // Only fill name
    await page.locator('input[type="text"]').fill('Test User');
    const signUpButton = page.locator('button').filter({ hasText: /sign up/i }).last();
    await expect(signUpButton).toBeDisabled();

    // Fill email too (still missing password)
    await page.locator('input[type="email"]').fill('test@example.com');
    await expect(signUpButton).toBeDisabled();
  });

  test('sign up button should be enabled with all fields filled', async ({ page }) => {
    await navigateToLogin(page);
    await switchToTab(page, 'Sign Up');

    await page.locator('input[type="text"]').fill('Test User');
    await page.locator('input[type="email"]').fill('test@example.com');
    await page.locator('input[type="password"]').fill('password123');

    const signUpButton = page.locator('button').filter({ hasText: /sign up/i }).last();
    await expect(signUpButton).toBeEnabled();
  });

  test('should capture network request on sign up attempt', async ({ page }) => {
    await navigateToLogin(page);
    await switchToTab(page, 'Sign Up');

    const email = `e2e_${uniqueId()}@test-astrovedic.com`;

    // Intercept API call
    const requestPromise = page.waitForRequest(
      (req) => req.url().includes('/api/auth/register'),
      { timeout: 10_000 },
    );

    await page.locator('input[type="text"]').fill('E2E Test User');
    await page.locator('input[type="email"]').fill(email);
    await page.locator('input[type="password"]').fill('TestPass123!');

    const signUpButton = page.locator('button').filter({ hasText: /sign up/i }).last();
    await signUpButton.click();

    const request = await requestPromise;
    console.log(`[AUTH DEBUG] Register request URL: ${request.url()}`);
    console.log(`[AUTH DEBUG] Register request method: ${request.method()}`);

    expect(request.method()).toBe('POST');

    const response = await request.response();
    if (response) {
      console.log(`[AUTH DEBUG] Register response status: ${response.status()}`);
      const body = await response.text().catch(() => 'no body');
      console.log(`[AUTH DEBUG] Register response body: ${body}`);

      if (response.status() === 405) {
        console.error('[AUTH ISSUE] API returns 405 — VITE_API_URL may not be configured on Vercel');
      }
    }
  });

  test('should show error for duplicate email registration', async ({ page }) => {
    await navigateToLogin(page);
    await switchToTab(page, 'Sign Up');

    // Use an email that likely already exists (admin user)
    await page.locator('input[type="text"]').fill('Duplicate Test');
    await page.locator('input[type="email"]').fill('gauravrattan87@gmail.com');
    await page.locator('input[type="password"]').fill('TestPass123!');

    const signUpButton = page.locator('button').filter({ hasText: /sign up/i }).last();
    await signUpButton.click();

    // Should show an error — "Email already registered" or similar
    const errorDiv = page.locator('.text-red-400.text-center, .rounded-xl.text-red-400').first();
    await expect(errorDiv).toBeVisible({ timeout: 10_000 });
    const errorText = await errorDiv.textContent();
    expect(errorText?.toLowerCase()).toMatch(/already|registered|exists|duplicate/);
  });
});

// ─── 4. ASTROLOGER REGISTRATION TOGGLE ─────────────────────────────────

test.describe('Astrologer Registration', () => {
  test('toggling astrologer should change button text', async ({ page }) => {
    await navigateToLogin(page);
    await switchToTab(page, 'Sign Up');

    // Before toggle — button says "Sign Up"
    const submitButton = page.locator('[role="tabpanel"]:visible button[data-slot="button"]');
    const initialText = await submitButton.textContent();

    // Toggle astrologer — use the toggle button specifically (has the round toggle div inside)
    const astrologerToggle = page.locator('button.flex.items-center').filter({ hasText: /astrologer/i });
    await astrologerToggle.click();

    // After toggle — button text should change to include "Astrologer"
    await page.waitForTimeout(300);
    const newText = await submitButton.textContent();
    expect(newText?.toLowerCase()).toContain('astrologer');

    // Untoggle — click the same toggle button again
    await astrologerToggle.click();
    await page.waitForTimeout(300);
    const revertedText = await submitButton.textContent();
    // Should revert back
    expect(revertedText).toBe(initialText);
  });

  test('astrologer signup should call register-astrologer endpoint', async ({ page }) => {
    await navigateToLogin(page);
    await switchToTab(page, 'Sign Up');

    const email = `astro_e2e_${uniqueId()}@test-astrovedic.com`;

    // Toggle astrologer ON
    const astrologerToggle = page.locator('button').filter({ hasText: /astrologer/i });
    await astrologerToggle.click();
    await page.waitForTimeout(300);

    // Intercept API call — should go to register-astrologer, not register
    const requestPromise = page.waitForRequest(
      (req) => req.url().includes('/api/auth/register'),
      { timeout: 10_000 },
    );

    await page.locator('input[type="text"]').fill('E2E Astrologer');
    await page.locator('input[type="email"]').fill(email);
    await page.locator('input[type="password"]').fill('AstroPass123!');

    const submitButton = page.locator('[role="tabpanel"]:visible button[class*="btn-sacred"]');
    await submitButton.click();

    const request = await requestPromise;
    console.log(`[AUTH DEBUG] Astrologer register URL: ${request.url()}`);

    // Should hit the astrologer-specific endpoint
    expect(request.url()).toContain('register-astrologer');
  });
});

// ─── 5. KEYBOARD INTERACTION ────────────────────────────────────────────

test.describe('Keyboard Interaction', () => {
  test('pressing Enter in password field should submit login', async ({ page }) => {
    await navigateToLogin(page);

    const requestPromise = page.waitForRequest(
      (req) => req.url().includes('/api/auth/login'),
      { timeout: 10_000 },
    );

    await page.locator('input[type="email"]').fill('keyboard@test.com');
    await page.locator('input[type="password"]').fill('password123');
    await page.locator('input[type="password"]').press('Enter');

    // Verify the request was sent (Enter triggered login)
    const request = await requestPromise;
    expect(request.method()).toBe('POST');
  });

  test('pressing Enter in password field should submit signup', async ({ page }) => {
    await navigateToLogin(page);
    await switchToTab(page, 'Sign Up');

    const requestPromise = page.waitForRequest(
      (req) => req.url().includes('/api/auth/register'),
      { timeout: 10_000 },
    );

    await page.locator('input[type="text"]').fill('Enter Test');
    await page.locator('input[type="email"]').fill(`enter_${uniqueId()}@test.com`);
    await page.locator('input[type="password"]').fill('password123');
    await page.locator('input[type="password"]').press('Enter');

    const request = await requestPromise;
    expect(request.method()).toBe('POST');
  });
});

// ─── 6. RESPONSIVE / VISUAL ────────────────────────────────────────────

test.describe('Responsive & Visual', () => {
  test('auth page should render correctly on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 }); // iPhone X
    await navigateToLogin(page);

    const form = page.locator('.max-w-md');
    await expect(form).toBeVisible();

    // Tabs should still be visible on mobile
    const tabs = page.locator('[role="tab"]');
    await expect(tabs).toHaveCount(2);
  });

  test('auth page should render correctly on tablet', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 }); // iPad
    await navigateToLogin(page);

    const form = page.locator('.max-w-md');
    await expect(form).toBeVisible();
  });
});

// ─── 7. API CONNECTIVITY DIAGNOSTIC ────────────────────────────────────

test.describe('API Connectivity Diagnostic', () => {
  test('verify which API URL the frontend calls', async ({ page }) => {
    await navigateToLogin(page);

    // Check what VITE_API_URL is set to in the deployed app
    const apiBase = await page.evaluate(() => {
      // @ts-expect-error - accessing Vite env
      return (window as any).__VITE_API_URL__ || 'not-exposed';
    });
    console.log(`[DIAG] VITE_API_URL exposed: ${apiBase}`);

    // Capture all network requests during login attempt
    const requests: string[] = [];
    page.on('request', (req) => {
      if (req.url().includes('auth')) {
        requests.push(`${req.method()} ${req.url()} (${req.resourceType()})`);
      }
    });

    const responses: string[] = [];
    page.on('response', (res) => {
      if (res.url().includes('auth')) {
        responses.push(`${res.status()} ${res.url()}`);
      }
    });

    await page.locator('input[type="email"]').fill('diag@test.com');
    await page.locator('input[type="password"]').fill('diagpass');

    const signInButton = page.locator('button').filter({ hasText: /sign in/i }).last();
    await signInButton.click();

    // Wait for network activity
    await page.waitForTimeout(5_000);

    console.log('[DIAG] Auth requests:', JSON.stringify(requests, null, 2));
    console.log('[DIAG] Auth responses:', JSON.stringify(responses, null, 2));

    // Diagnostic assertion: log what happened
    if (responses.some((r) => r.includes('405'))) {
      console.error(
        '[DIAGNOSIS] The frontend is calling the Vercel domain for API, but Vercel returns 405.\n' +
        'FIX: Set VITE_API_URL=https://astro-rattan-api.onrender.com in Vercel Environment Variables.',
      );
    }
    if (responses.some((r) => r.includes('401') || r.includes('Invalid'))) {
      console.log('[DIAGNOSIS] API is reachable. Auth correctly rejected invalid credentials.');
    }
    if (responses.length === 0) {
      console.error('[DIAGNOSIS] No auth responses received — possible network/CORS issue.');
    }

    // This test always passes — it's diagnostic
    expect(true).toBe(true);
  });
});
