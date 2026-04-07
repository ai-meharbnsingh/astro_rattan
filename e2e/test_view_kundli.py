"""View specific kundli"""
from playwright.sync_api import sync_playwright

def test_view():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        page = browser.new_page(viewport={'width': 1400, 'height': 900})
        
        print("=== Login ===")
        page.goto('https://astrovedic-web.vercel.app/login', timeout=60000)
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        page.locator('button:has-text("Sign In")').nth(1).click()
        page.wait_for_timeout(4000)
        
        # Go directly to kundli
        KUNDLI_ID = "5263f6a11d919dc0b11935f27a8cc591"
        print(f"\n=== Viewing Kundli: {KUNDLI_ID} ===")
        page.goto(f'https://astrovedic-web.vercel.app/kundli/{KUNDLI_ID}')
        page.wait_for_timeout(5000)
        page.screenshot(path='./e2e/screenshots/kundli_view.png', full_page=True)
        print("✅ Kundli view captured")
        
        # Check if chart is visible
        charts = page.locator('svg').all()
        print(f"Found {len(charts)} SVG elements")
        
        # Get chart text content
        chart_text = page.evaluate('''() => {
            const svgs = document.querySelectorAll('svg');
            const results = [];
            svgs.forEach((svg, idx) => {
                const texts = svg.querySelectorAll('text');
                const content = Array.from(texts).map(t => t.textContent).filter(t => t && t.trim());
                if (content.length > 0) {
                    results.push(`SVG ${idx}: ${content.slice(0, 10).join(', ')}`);
                }
            });
            return results;
        }''')
        
        print("\nChart content:")
        for line in chart_text[:5]:
            print(f"  {line}")
        
        # Toggle chart styles
        north = page.locator('button:has-text("North Indian")').first
        if north.is_visible():
            north.click()
            page.wait_for_timeout(1000)
            page.screenshot(path='./e2e/screenshots/north_chart.png')
            print("\n✅ North Indian captured")
        
        south = page.locator('button:has-text("South Indian")').first
        if south.is_visible():
            south.click()
            page.wait_for_timeout(1000)
            page.screenshot(path='./e2e/screenshots/south_chart.png')
            print("✅ South Indian captured")
        
        browser.close()

if __name__ == '__main__':
    test_view()
