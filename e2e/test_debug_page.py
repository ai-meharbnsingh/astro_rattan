"""Debug what's on the page"""
from playwright.sync_api import sync_playwright

def debug_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        print('Opening app...')
        page.goto('https://astrovedic-web.vercel.app', timeout=60000)
        page.wait_for_load_state('networkidle')
        
        # Take screenshot
        page.screenshot(path='./e2e/screenshots/debug_homepage.png', full_page=True)
        print('Screenshot saved')
        
        # Get page content
        content = page.content()
        with open('./e2e/page_content.html', 'w') as f:
            f.write(content)
        print('HTML saved')
        
        # Find all buttons
        print('\n=== All buttons ===')
        buttons = page.locator('button').all()
        for i, btn in enumerate(buttons):
            text = btn.text_content() or ''
            visible = btn.is_visible()
            print(f'{i}: "{text[:50]}" visible={visible}')
        
        # Find all links
        print('\n=== All links ===')
        links = page.locator('a').all()
        for i, link in enumerate(links[:20]):
            text = link.text_content() or ''
            href = link.get_attribute('href') or ''
            visible = link.is_visible()
            print(f'{i}: "{text[:30]}" href={href[:30]} visible={visible}')
        
        # Check for specific text
        print('\n=== Checking for auth-related elements ===')
        checks = ['Login', 'Sign In', 'Sign Up', 'Register', 'My Account', 'Profile', 'Logout']
        for text in checks:
            locator = page.locator(f'text={text}')
            count = locator.count()
            if count > 0:
                print(f'"{text}": {count} found')
                for i in range(min(count, 3)):
                    el = locator.nth(i)
                    print(f'  {i}: visible={el.is_visible()}')
        
        # Try to find by CSS
        print('\n=== Auth selectors ===')
        selectors = [
            'nav a', 'header a', '[class*="nav"] a', '[class*="header"] a',
            'button[class*="login"]', 'a[class*="login"]',
            '[data-testid]', '[role="button"]'
        ]
        for sel in selectors:
            try:
                count = page.locator(sel).count()
                if count > 0:
                    print(f'{sel}: {count} elements')
            except:
                pass
        
        browser.close()

if __name__ == '__main__':
    debug_page()
