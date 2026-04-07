"""View saved kundli"""
from playwright.sync_api import sync_playwright

def test_view():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        page = browser.new_page(viewport={'width': 1400, 'height': 900})
        
        # Login
        print("=== Login ===")
        page.goto('https://astrovedic-web.vercel.app/login', timeout=60000)
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        page.locator('button:has-text("Sign In")').nth(1).click()
        page.wait_for_timeout(4000)
        
        # Go to kundli page
        print("\n=== Go to My Kundlis ===")
        page.goto('https://astrovedic-web.vercel.app/kundli')
        page.wait_for_timeout(3000)
        page.screenshot(path='./e2e/screenshots/01_list.png')
        
        # Click first kundli
        print("\n=== Click first kundli ===")
        first = page.locator('text=Meharban Singh').first
        first.click()
        page.wait_for_timeout(5000)
        page.screenshot(path='./e2e/screenshots/02_detail.png', full_page=True)
        print("✅ Detail page captured")
        
        # North Indian
        print("\n=== North Indian ===")
        north = page.locator('button:has-text("North Indian")').first
        if north.is_visible():
            north.click()
            page.wait_for_timeout(1000)
            page.screenshot(path='./e2e/screenshots/03_north.png')
            print("✅ North Indian captured")
        
        # South Indian
        print("\n=== South Indian ===")
        south = page.locator('button:has-text("South Indian")').first
        if south.is_visible():
            south.click()
            page.wait_for_timeout(1000)
            page.screenshot(path='./e2e/screenshots/04_south.png')
            print("✅ South Indian captured")
        
        print("\n✅ Done!")
        browser.close()

if __name__ == '__main__':
    test_view()
