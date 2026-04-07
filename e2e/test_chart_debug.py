"""Debug South Indian chart"""
from playwright.sync_api import sync_playwright

def test_debug():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1400, 'height': 2000})
        
        # Login
        page.goto('https://astrovedic-web.vercel.app/login', timeout=60000)
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        page.locator('button:has-text("Sign In")').nth(1).click()
        page.wait_for_timeout(4000)
        
        # Go to kundli generator and generate new chart
        page.goto('https://astrovedic-web.vercel.app/kundli', timeout=60000)
        page.wait_for_timeout(3000)
        
        # Click "Generate New Kundli"
        page.get_by_text('Generate New Kundli').click()
        page.wait_for_timeout(2000)
        
        # Fill form
        page.get_by_placeholder('Full Name').fill('Test Chart')
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
        
        # Submit
        page.get_by_text('Generate Kundli').click()
        page.wait_for_timeout(10000)
        
        # Click South Indian tab
        page.get_by_text('South Indian').first.click()
        page.wait_for_timeout(2000)
        
        # Scroll to chart section
        page.evaluate("window.scrollTo(0, 800)")
        page.wait_for_timeout(1000)
        
        # Screenshot
        page.screenshot(path='./e2e/screenshots/chart_south.png')
        print("✅ South Indian Chart Screenshot saved")
        
        browser.close()

if __name__ == '__main__':
    test_debug()
