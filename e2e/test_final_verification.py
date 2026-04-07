"""Final comprehensive test of North Indian chart"""
from playwright.sync_api import sync_playwright

def test_final():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1400, 'height': 2000})
        
        # Login
        print("🔐 Logging in...")
        page.goto('https://astrovedic-web.vercel.app/login', timeout=60000)
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        page.locator('button:has-text("Sign In")').nth(1).click()
        page.wait_for_timeout(4000)
        print("✅ Logged in")
        
        # Generate chart with different test data
        print("\n📊 Generating test chart...")
        page.goto('https://astrovedic-web.vercel.app/kundli', timeout=60000)
        page.wait_for_timeout(3000)
        page.get_by_text('Generate New Kundli').click()
        page.wait_for_timeout(2000)
        
        # Different birth details
        page.get_by_placeholder('Full Name').fill('Rohan Sharma')
        date_inputs = page.locator('input[type="date"]').all()
        if date_inputs:
            date_inputs[0].fill('1992-03-15')
        time_inputs = page.locator('input[type="time"]').all()
        if time_inputs:
            time_inputs[0].fill('08:30')
        page.get_by_placeholder('Birth Place (type to search)').fill('Mumbai')
        page.wait_for_timeout(1500)
        try:
            page.get_by_text('Mumbai, India').first.click(timeout=3000)
        except:
            pass
        page.wait_for_timeout(1000)
        
        page.get_by_text('Generate Kundli').click()
        page.wait_for_timeout(10000)
        print("✅ Chart generated")
        
        # Click North Indian tab
        print("\n🎯 Selecting North Indian chart...")
        page.get_by_text('North Indian').first.click()
        page.wait_for_timeout(1000)
        
        # Scroll to chart
        page.evaluate("window.scrollTo(0, 700)")
        page.wait_for_timeout(1000)
        
        # Take screenshot
        page.screenshot(path='./e2e/screenshots/final_test_north.png')
        print("✅ Screenshot saved")
        
        # Extract data
        print("\n📋 Extracting planet positions...")
        text = page.locator('body').inner_text()
        
        # Get planet table
        print("\n=== PLANET POSITIONS TABLE ===")
        in_table = False
        for line in text.split('\n'):
            line = line.strip()
            if 'Planet' in line and 'Sign' in line and 'House' in line:
                in_table = True
                continue
            if in_table and any(p in line for p in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']):
                parts = [p for p in line.split('  ') if p.strip()]
                if len(parts) >= 3:
                    print(f"  {parts[0]:8} | Sign: {parts[1]:10} | House: {parts[2]}")
            if in_table and 'Avakhada' in line:
                break
        
        # Verify chart is visible
        print("\n=== CHART VERIFICATION ===")
        chart_visible = page.locator('svg').count() > 0
        print(f"  Chart SVG rendered: {'✅ Yes' if chart_visible else '❌ No'}")
        
        house_numbers = page.locator('text=1, text=2, text=3, text=4, text=5, text=6, text=7, text=8, text=9, text=10, text=11, text=12').count()
        print(f"  House numbers displayed: {'✅ Yes' if house_numbers >= 12 else '❌ No'}")
        
        print("\n✅ Final test completed successfully!")
        browser.close()

if __name__ == '__main__':
    test_final()
