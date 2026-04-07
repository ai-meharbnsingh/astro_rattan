"""Navigate from home to kundli"""
from playwright.sync_api import sync_playwright

def test_nav():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        page = browser.new_page(viewport={'width': 1400, 'height': 900})
        
        print("=== Home Page ===")
        page.goto('https://astrovedic-web.vercel.app', timeout=60000)
        page.wait_for_load_state('networkidle')
        page.screenshot(path='./e2e/screenshots/01_home.png')
        
        print("\n=== Click Kundli Generator ===")
        kundli_link = page.locator('a[href="/kundli"]').first
        if kundli_link.is_visible():
            kundli_link.click()
        else:
            page.goto('https://astrovedic-web.vercel.app/kundli')
        
        page.wait_for_timeout(3000)
        page.screenshot(path='./e2e/screenshots/02_kundli_page.png', full_page=True)
        print("✅ Kundli page captured")
        
        # Check if there's a form
        inputs = page.locator('input').all()
        print(f"\nFound {len(inputs)} inputs")
        
        # Get all text on page
        text = page.evaluate('''() => {
            return document.body.innerText.substring(0, 500);
        }''')
        print(f"\nPage text: {text}...")
        
        browser.close()

if __name__ == '__main__':
    test_nav()
