"""Debug login page structure"""
from playwright.sync_api import sync_playwright

def debug_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        print('Opening app...')
        page.goto('https://astrovedic-web.vercel.app', timeout=60000)
        page.wait_for_load_state('networkidle')
        
        # Click Sign In
        page.locator('a[href="/login"]').first.click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)
        
        print('\n=== Login Page Structure ===')
        
        # Get all buttons
        buttons = page.locator('button').all()
        print(f'\nButtons ({len(buttons)}):')
        for i, btn in enumerate(buttons):
            text = btn.text_content() or ''
            type_attr = btn.get_attribute('type') or 'no-type'
            visible = btn.is_visible()
            print(f'  {i}: "{text[:40]}" type={type_attr} visible={visible}')
        
        # Get all inputs
        inputs = page.locator('input').all()
        print(f'\nInputs ({len(inputs)}):')
        for i, inp in enumerate(inputs):
            type_attr = inp.get_attribute('type') or 'text'
            name = inp.get_attribute('name') or 'no-name'
            placeholder = inp.get_attribute('placeholder') or ''
            print(f'  {i}: type={type_attr} name={name} placeholder={placeholder[:20]}')
        
        # Get all forms
        forms = page.locator('form').all()
        print(f'\nForms: {len(forms)}')
        
        # Get page HTML
        html = page.content()
        with open('./e2e/login_page.html', 'w') as f:
            f.write(html)
        print('\nHTML saved to e2e/login_page.html')
        
        page.screenshot(path='./e2e/screenshots/login_page.png')
        
        browser.close()

if __name__ == '__main__':
    debug_login()
