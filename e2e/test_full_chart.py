"""Full test with chart generation"""
from playwright.sync_api import sync_playwright

def test_full():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=150)
        page = browser.new_page(viewport={'width': 1400, 'height': 900})
        
        # Step 1: Login
        print("=== Step 1: Login ===")
        page.goto('https://astrovedic-web.vercel.app/login', timeout=60000)
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        page.locator('button:has-text("Sign In")').nth(1).click()
        page.wait_for_timeout(4000)
        
        # Check login
        token = page.evaluate('() => localStorage.getItem("astrovedic_token")')
        if not token:
            print("❌ Login failed")
            browser.close()
            return
        print("✅ Logged in")
        
        # Step 2: Go to Kundli page
        print("\n=== Step 2: Go to Kundli Generator ===")
        page.goto('https://astrovedic-web.vercel.app/kundli')
        page.wait_for_timeout(2000)
        page.screenshot(path='./e2e/screenshots/01_form.png')
        
        # Step 3: Fill form
        print("\n=== Step 3: Fill Form ===")
        page.locator('input[placeholder="Full Name"]').fill('Meharban Singh')
        page.locator('input[type="date"]').fill('1985-08-23')
        page.locator('input[type="time"]').fill('23:15')
        page.locator('input[placeholder*="Birth Place"]').fill('Delhi')
        page.wait_for_timeout(1000)
        
        # Select Delhi from dropdown if it appears
        delhi_option = page.locator('text=Delhi, India').first
        if delhi_option.is_visible():
            delhi_option.click()
            page.wait_for_timeout(500)
        
        page.screenshot(path='./e2e/screenshots/02_filled.png')
        
        # Step 4: Generate
        print("\n=== Step 4: Generate Kundli ===")
        page.locator('button:has-text("Generate Kundli")').click()
        page.wait_for_timeout(5000)
        page.screenshot(path='./e2e/screenshots/03_result.png', full_page=True)
        print("✅ Chart generated")
        
        # Step 5: Check North Indian
        print("\n=== Step 5: North Indian Chart ===")
        north = page.locator('button:has-text("North Indian")').first
        if north.is_visible():
            north.click()
            page.wait_for_timeout(1000)
            page.screenshot(path='./e2e/screenshots/04_north.png')
            print("✅ North Indian captured")
        
        # Step 6: Check South Indian
        print("\n=== Step 6: South Indian Chart ===")
        south = page.locator('button:has-text("South Indian")').first
        if south.is_visible():
            south.click()
            page.wait_for_timeout(1000)
            page.screenshot(path='./e2e/screenshots/05_south.png')
            print("✅ South Indian captured")
        
        # Get chart numbers
        print("\n=== Chart House Numbers ===")
        numbers = page.evaluate('''() => {
            const svgs = document.querySelectorAll('svg');
            for (let svg of svgs) {
                const texts = svg.querySelectorAll('text');
                const nums = Array.from(texts)
                    .map(t => t.textContent)
                    .filter(t => /^[0-9]+$/.test(t) && parseInt(t) >= 1 && parseInt(t) <= 12)
                    .slice(0, 12);
                if (nums.length >= 12) return nums;
            }
            return [];
        }''')
        print(f"Found house numbers: {numbers}")
        
        print("\n✅ All screenshots saved!")
        browser.close()

if __name__ == '__main__':
    test_full()
