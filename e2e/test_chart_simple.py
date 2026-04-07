"""Simple visual test for kundli chart"""
from playwright.sync_api import sync_playwright

def test_chart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page(viewport={'width': 1400, 'height': 900})
        
        print("=== Opening app ===")
        page.goto('https://astrovedic-web.vercel.app/login', timeout=60000)
        page.wait_for_load_state('networkidle')
        page.screenshot(path='./e2e/screenshots/01_login.png')
        
        # Login
        print("\n=== Logging in ===")
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        page.locator('button:has-text("Sign In")').nth(1).click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)
        page.screenshot(path='./e2e/screenshots/02_after_login.png')
        
        # Navigate to Kundli Generator
        print("\n=== Going to Kundli Generator ===")
        page.goto('https://astrovedic-web.vercel.app/kundli')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)
        page.screenshot(path='./e2e/screenshots/03_kundli_page.png', full_page=True)
        
        # Check what's on the page
        print("\n=== Page content ===")
        inputs = page.locator('input').all()
        print(f"Found {len(inputs)} inputs:")
        for i, inp in enumerate(inputs[:5]):
            type_attr = inp.get_attribute('type') or 'text'
            placeholder = inp.get_attribute('placeholder') or ''
            print(f"  {i}: type={type_attr}, placeholder={placeholder[:30]}")
        
        buttons = page.locator('button').all()
        print(f"\nFound {len(buttons)} buttons:")
        for i, btn in enumerate(buttons[:10]):
            text = btn.text_content() or ''
            print(f"  {i}: {text[:40]}")
        
        browser.close()

if __name__ == '__main__':
    test_chart()
