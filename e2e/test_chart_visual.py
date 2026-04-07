"""Visual test for kundli chart"""
from playwright.sync_api import sync_playwright

def test_chart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        page = browser.new_page(viewport={'width': 1400, 'height': 900})
        
        print("=== Opening app ===")
        page.goto('https://astrovedic-web.vercel.app', timeout=60000)
        page.wait_for_load_state('networkidle')
        page.screenshot(path='./e2e/screenshots/01_home.png')
        
        # Login
        print("\n=== Logging in ===")
        page.locator('a[href="/login"]').first.click()
        page.wait_for_load_state('networkidle')
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        page.locator('button:has-text("Sign In")').nth(1).click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)
        
        # Navigate to Kundli Generator
        print("\n=== Going to Kundli Generator ===")
        page.goto('https://astrovedic-web.vercel.app/kundli')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)
        page.screenshot(path='./e2e/screenshots/02_kundli_page.png')
        
        # Fill form and generate
        print("\n=== Generating Kundli ===")
        page.locator('input[name="name"], input[placeholder*="name"]').fill('Test Chart')
        page.locator('input[type="date"]').fill('1985-08-23')
        page.locator('input[type="time"]').fill('23:15')
        page.locator('input[name="place"]').fill('Delhi, India')
        page.screenshot(path='./e2e/screenshots/03_form_filled.png')
        
        # Click generate
        page.locator('button:has-text("Generate"), button:has-text("Submit")').click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(3000)
        page.screenshot(path='./e2e/screenshots/04_chart_generated.png', full_page=True)
        
        # Take screenshot of just the chart area
        print("\n=== Capturing charts ===")
        
        # Find and screenshot North Indian chart
        north_chart = page.locator('text=North Indian').first
        if north_chart.is_visible():
            print("North Indian chart found")
            # Click to ensure it's selected
            north_chart.click()
            page.wait_for_timeout(500)
            page.screenshot(path='./e2e/screenshots/05_north_indian.png', full_page=True)
        
        # Find and click South Indian
        south_chart = page.locator('text=South Indian').first
        if south_chart.is_visible():
            print("South Indian chart found")
            south_chart.click()
            page.wait_for_timeout(500)
            page.screenshot(path='./e2e/screenshots/06_south_indian.png', full_page=True)
        
        # Get chart data
        print("\n=== Chart Analysis ===")
        chart_text = page.evaluate('''() => {
            const svg = document.querySelector('svg');
            if (!svg) return 'No SVG found';
            const texts = svg.querySelectorAll('text');
            return Array.from(texts).slice(0, 20).map(t => t.textContent).join(', ');
        }''')
        print(f"Chart text content: {chart_text}")
        
        print("\n✅ Screenshots saved in ./e2e/screenshots/")
        browser.close()

if __name__ == '__main__':
    test_chart()
