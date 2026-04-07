"""Final visual test for kundli chart"""
from playwright.sync_api import sync_playwright

def test_chart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=150)
        page = browser.new_page(viewport={'width': 1400, 'height': 900})
        
        print("=== Step 1: Login ===")
        page.goto('https://astrovedic-web.vercel.app/login', timeout=60000)
        page.wait_for_load_state('networkidle')
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        page.locator('button:has-text("Sign In")').nth(1).click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)
        
        print("\n=== Step 2: Go to Kundli Generator ===")
        page.goto('https://astrovedic-web.vercel.app/kundli')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)
        page.screenshot(path='./e2e/screenshots/01_kundli_form.png')
        
        print("\n=== Step 3: Fill Form ===")
        page.locator('input[placeholder="Full Name"]').fill('Meharban Singh')
        page.locator('input[type="date"]').fill('1985-08-23')
        page.locator('input[type="time"]').fill('23:15')
        page.locator('input[placeholder*="Birth Place"]').fill('Delhi')
        page.wait_for_timeout(1000)
        page.screenshot(path='./e2e/screenshots/02_form_filled.png')
        
        print("\n=== Step 4: Generate Kundli ===")
        page.locator('button:has-text("Generate Kundli")').click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(4000)
        page.screenshot(path='./e2e/screenshots/03_chart_generated.png', full_page=True)
        
        print("\n=== Step 5: Check North Indian Chart ===")
        # Click North Indian button
        north_btn = page.locator('button:has-text("North Indian")').first
        if north_btn.is_visible():
            north_btn.click()
            page.wait_for_timeout(1000)
            page.screenshot(path='./e2e/screenshots/04_north_indian.png', full_page=True)
            print("✅ North Indian chart captured")
        
        print("\n=== Step 6: Check South Indian Chart ===")
        south_btn = page.locator('button:has-text("South Indian")').first
        if south_btn.is_visible():
            south_btn.click()
            page.wait_for_timeout(1000)
            page.screenshot(path='./e2e/screenshots/05_south_indian.png', full_page=True)
            print("✅ South Indian chart captured")
        
        # Get chart numbers
        print("\n=== Chart Numbers ===")
        chart_numbers = page.evaluate('''() => {
            const svgs = document.querySelectorAll('svg');
            const results = [];
            svgs.forEach((svg, idx) => {
                const texts = svg.querySelectorAll('text');
                const numbers = Array.from(texts)
                    .map(t => t.textContent)
                    .filter(t => /^[0-9]+$/.test(t))
                    .slice(0, 15);
                if (numbers.length > 0) {
                    results.push(`SVG ${idx}: ${numbers.join(', ')}`);
                }
            });
            return results;
        }''')
        
        for line in chart_numbers:
            print(line)
        
        print("\n✅ All screenshots saved in ./e2e/screenshots/")
        browser.close()

if __name__ == '__main__':
    test_chart()
