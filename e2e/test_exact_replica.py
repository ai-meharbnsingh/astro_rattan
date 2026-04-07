"""Test exact replica"""
from playwright.sync_api import sync_playwright

def test_replica():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 4000})
        
        print("🌐 Loading exact replica...")
        page.goto('https://astrovedic-web.vercel.app/', timeout=60000)
        page.wait_for_timeout(5000)
        
        page.screenshot(path='e2e/screenshots/exact_replica_final.png', full_page=True)
        print("✅ Screenshot saved!")
        
        browser.close()

if __name__ == '__main__':
    test_replica()
