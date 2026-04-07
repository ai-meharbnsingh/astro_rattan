"""Test with existing saved kundli"""
from playwright.sync_api import sync_playwright

def test_existing():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        page = browser.new_page(viewport={'width': 1400, 'height': 900})
        
        print("=== Login ===")
        page.goto('https://astrovedic-web.vercel.app/login', timeout=60000)
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        page.locator('button:has-text("Sign In")').nth(1).click()
        
        # Wait longer for login
        page.wait_for_timeout(4000)
        page.screenshot(path='./e2e/screenshots/login_result.png')
        
        # Check if logged in
        token = page.evaluate('() => localStorage.getItem("astrovedic_token")')
        print(f"Token present: {bool(token)}")
        
        if token:
            print("\n=== Go to My Kundlis ===")
            page.goto('https://astrovedic-web.vercel.app/kundli/list')
            page.wait_for_timeout(3000)
            page.screenshot(path='./e2e/screenshots/my_kundlis.png', full_page=True)
            
            # Click first kundli
            kundli_items = page.locator('text=Meharban').all()
            print(f"Found {len(kundli_items)} kundli items")
            
            if len(kundli_items) > 0:
                kundli_items[0].click()
                page.wait_for_timeout(3000)
                page.screenshot(path='./e2e/screenshots/kundli_detail.png', full_page=True)
                
                # Click North Indian
                north = page.locator('button:has-text("North Indian")').first
                if north.is_visible():
                    north.click()
                    page.wait_for_timeout(1000)
                    page.screenshot(path='./e2e/screenshots/north_indian.png')
                    print("✅ North Indian captured")
                
                # Click South Indian
                south = page.locator('button:has-text("South Indian")').first
                if south.is_visible():
                    south.click()
                    page.wait_for_timeout(1000)
                    page.screenshot(path='./e2e/screenshots/south_indian.png')
                    print("✅ South Indian captured")
        
        browser.close()

if __name__ == '__main__':
    test_existing()
