"""Debug login in detail"""
from playwright.sync_api import sync_playwright

def debug_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()
        
        # Capture network
        api_calls = []
        def log_response(response):
            if 'api' in response.url:
                api_calls.append({
                    'url': response.url,
                    'status': response.status,
                    'method': response.request.method
                })
        page.on('response', log_response)
        
        # Capture console
        page.on('console', lambda msg: print(f'[CONSOLE] {msg.type}: {msg.text}'))
        
        print('Opening login page...')
        page.goto('https://astrovedic-web.vercel.app/login', timeout=60000)
        page.wait_for_load_state('networkidle')
        page.screenshot(path='./e2e/screenshots/login_page.png')
        
        print('Filling credentials...')
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        page.screenshot(path='./e2e/screenshots/login_filled.png')
        
        print('Clicking Sign In...')
        page.locator('button:has-text("Sign In")').nth(1).click()
        
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(3000)
        
        print(f'Current URL: {page.url}')
        page.screenshot(path='./e2e/screenshots/after_login.png')
        
        # Check for errors
        error_selectors = [
            'text=Invalid',
            'text=Error',
            'text=Failed',
            'text=incorrect',
            'text=wrong'
        ]
        
        for sel in error_selectors:
            el = page.locator(sel).first
            if el.is_visible():
                print(f'Error found: {el.text_content()}')
        
        # Check localStorage
        token = page.evaluate('() => localStorage.getItem("astrovedic_token")')
        print(f'Token: {token}')
        
        # Print API calls
        print(f'\nAPI calls:')
        for call in api_calls:
            print(f"  {call['method']} {call['status']} {call['url']}")
        
        browser.close()

if __name__ == '__main__':
    debug_login()
