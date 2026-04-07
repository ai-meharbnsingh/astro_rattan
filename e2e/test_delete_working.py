"""Working test for delete"""
from playwright.sync_api import sync_playwright
import json

def test_delete():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()
        
        console_logs = []
        page.on('console', lambda msg: console_logs.append(f'[{msg.type}] {msg.text}'))
        
        print('=== Opening app ===')
        page.goto('https://astrovedic-web.vercel.app', timeout=60000)
        page.wait_for_load_state('networkidle')
        
        # Click Sign In
        print('\n=== Clicking Sign In ===')
        page.locator('a[href="/login"]').first.click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)
        
        # Fill credentials
        print('Filling credentials...')
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        
        # Click the Sign In button (the one at index 7 based on debug)
        print('Clicking Sign In button...')
        page.locator('button:has-text("Sign In")').nth(1).click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(3000)
        
        current_url = page.url
        print(f'Current URL: {current_url}')
        page.screenshot(path='./e2e/screenshots/after_login.png')
        
        if '/login' in current_url:
            print('Still on login page - login failed!')
            browser.close()
            return
        
        # Check token
        token = page.evaluate('() => localStorage.getItem("astrovedic_token")')
        print(f'\nToken present: {bool(token)}')
        
        # Test DELETE /user/all
        print('\n=== Testing DELETE /api/kundli/user/all ===')
        
        result = page.evaluate('''async () => {
            const token = localStorage.getItem("astrovedic_token");
            if (!token) return { error: "No token" };
            
            try {
                const response = await fetch(
                    "https://astro-rattan-api.onrender.com/api/kundli/user/all",
                    {
                        method: "DELETE",
                        headers: {
                            "Authorization": "Bearer " + token,
                            "Content-Type": "application/json"
                        }
                    }
                );
                
                return {
                    status: response.status,
                    statusText: response.statusText,
                    body: await response.text()
                };
            } catch (e) {
                return { 
                    error: e.message,
                    name: e.name,
                    stack: e.stack
                };
            }
        }''')
        
        print(f'\nResult: {json.dumps(result, indent=2)}')
        
        # Test DELETE individual
        print('\n=== Testing DELETE /api/kundli/{id} ===')
        
        result2 = page.evaluate('''async () => {
            const token = localStorage.getItem("astrovedic_token");
            try {
                const response = await fetch(
                    "https://astro-rattan-api.onrender.com/api/kundli/nonexistent-id",
                    {
                        method: "DELETE",
                        headers: {
                            "Authorization": "Bearer " + token,
                            "Content-Type": "application/json"
                        }
                    }
                );
                
                return {
                    status: response.status,
                    statusText: response.statusText,
                    body: await response.text()
                };
            } catch (e) {
                return { error: e.message, name: e.name };
            }
        }''')
        
        print(f'\nResult: {json.dumps(result2, indent=2)}')
        
        # Print console errors
        print('\n=== Console Errors ===')
        errors = [l for l in console_logs if 'error' in l.lower()]
        for e in errors:
            print(e)
        
        browser.close()

if __name__ == '__main__':
    test_delete()
