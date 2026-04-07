"""Verify North Indian chart planet positions"""
from playwright.sync_api import sync_playwright

def test_north_chart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1400, 'height': 2000})
        
        # Login
        page.goto('https://astrovedic-web.vercel.app/login', timeout=60000)
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        page.locator('button:has-text("Sign In")').nth(1).click()
        page.wait_for_timeout(4000)
        
        # Generate new chart
        page.goto('https://astrovedic-web.vercel.app/kundli', timeout=60000)
        page.wait_for_timeout(3000)
        page.get_by_text('Generate New Kundli').click()
        page.wait_for_timeout(2000)
        
        # Fill form with test data
        page.get_by_placeholder('Full Name').fill('Test User')
        page.get_by_placeholder('Full Name').blur()
        date_inputs = page.locator('input[type="date"]').all()
        if date_inputs:
            date_inputs[0].fill('1985-08-23')
        time_inputs = page.locator('input[type="time"]').all()
        if time_inputs:
            time_inputs[0].fill('23:15')
        page.get_by_placeholder('Birth Place (type to search)').fill('Delhi')
        page.wait_for_timeout(1000)
        try:
            page.get_by_text('Delhi, India').first.click(timeout=3000)
        except:
            pass
        page.wait_for_timeout(1000)
        
        # Generate
        page.get_by_text('Generate Kundli').click()
        page.wait_for_timeout(10000)
        
        # Ensure North Indian is selected
        page.get_by_text('North Indian').first.click()
        page.wait_for_timeout(1000)
        
        # Scroll to chart
        page.evaluate("window.scrollTo(0, 800)")
        page.wait_for_timeout(1000)
        
        # Screenshot
        page.screenshot(path='./e2e/screenshots/north_chart_final.png')
        print("✅ North Indian Chart Screenshot saved")
        
        # Get data for verification
        text = page.locator('body').inner_text()
        print("\n=== Planet Positions (from table) ===")
        for line in text.split('\n'):
            line = line.strip()
            if any(p in line for p in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']) and 'House' in line:
                parts = line.split()
                if len(parts) >= 3:
                    print(f"{parts[0]:10} | Sign: {parts[1]:12} | House: {parts[2]}")
        
        browser.close()

if __name__ == '__main__':
    test_north_chart()
