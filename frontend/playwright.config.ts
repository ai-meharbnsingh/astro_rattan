import { defineConfig, devices } from '@playwright/test';
import path from 'path';

const chromePath = path.join(
  process.env.HOME || '~',
  'Library/Caches/ms-playwright/chromium-1217/chrome-mac-arm64',
  'Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing',
);

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: 1,
  reporter: [['html', { open: 'never' }], ['list']],
  timeout: 60_000,
  use: {
    baseURL: process.env.E2E_BASE_URL || 'https://astrovedic-web.vercel.app',
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
        launchOptions: {
          executablePath: chromePath,
        },
      },
    },
  ],
});
