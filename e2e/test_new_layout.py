"""Test new homepage layout"""
from playwright.sync_api import sync_playwright

def test_layout():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1400, 'height': 3000})
        
        print("🌐 Opening new layout...")
        page.goto('https://astrovedic-web.vercel.app/', timeout=60000)
        page.wait_for_timeout(5000)
        
        # Take full page screenshot
        page.screenshot(path='./e2e/screenshots/new_layout_home.png', full_page=True)
        print("✅ Homepage screenshot saved")
        
        # Get page title
        title = page.title()
        print(f"\n📄 Page Title: {title}")
        
        # Check for key elements
        text = page.locator('body').inner_text()
        
        checks = [
            ('Kundli Generation', 'Service Card'),
            ('500,000+', 'Stats Bar'),
            ('Daily Insights', 'Daily Section'),
            ('AI Astrology Assistant', 'AI Section'),
            ('Recommended For You', 'Recommended Section'),
            ('Shop Astrovedic', 'Shop Section'),
        ]
        
        print("\n✅ Layout Elements Check:")
        for keyword, label in checks:
            found = keyword in text
            print(f"  {'✅' if found else '❌'} {label}: {keyword}")
        
        browser.close()
        print("\n🎉 New layout test complete!")

if __name__ == '__main__':
    test_layout()
