import { defineConfig, devices } from '@playwright/test';
import fs from 'fs';
import path from 'path';

// Auto-detect installed Chromium version
const playwrightCache = path.join(process.env.HOME || '~', 'Library/Caches/ms-playwright');
let chromePath: string | undefined;
try {
  const dirs = fs.readdirSync(playwrightCache).filter(d => d.startsWith('chromium-')).sort().reverse();
  if (dirs.length > 0) {
    chromePath = path.join(
      playwrightCache, dirs[0], 'chrome-mac-arm64',
      'Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing',
    );
    if (!fs.existsSync(chromePath)) chromePath = undefined;
  }
} catch { /* fallback to Playwright default */ }

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: 1,
  reporter: [['html', { open: 'never' }], ['list']],
  timeout: 60_000,
  use: {
    baseURL: process.env.E2E_BASE_URL || 'https://astrorattan.com',
    trace: 'on-first-retry',
    screenshot: 'on',
    video: 'on-first-retry',
    actionTimeout: 15_000,
  },
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        ...(chromePath ? { launchOptions: { executablePath: chromePath } } : {}),
      },
    },
    {
      name: 'chrome-beta',
      use: {
        ...devices['Desktop Chrome'],
        channel: 'chrome-beta',
      },
    },
  ],
});
