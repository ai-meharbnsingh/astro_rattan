"""Test delete - final version"""
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
        
        # Click first Sign In link
        print('\n=== Clicking Sign In ===')
        page.locator('a[href="/login"]').first.click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)
        
        # Fill form
        print('Filling credentials...')
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        
        # Click submit button (first one in form)
        print('Submitting...')
        page.locator('form button[type="submit"]').first.click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(3000)
        
        # Take screenshot to see what happened
        page.screenshot(path='./e2e/screenshots/after_login.png')
        
        # Check URL - if still on /login, login failed
        current_url = page.url
        print(f'Current URL: {current_url}')
        
        if '/login' in current_url:
            print('Still on login page - checking for error...')
            error = page.locator('text=Invalid, text=Error, text=Failed').first
            if error.is_visible():
                print(f'Error: {error.text_content()}')
            browser.close()
            return
        
        # Check token
        token = page.evaluate('() => localStorage.getItem("astrovedic_token")')
        print(f'Token present: {bool(token)}')
        if token:
            print(f'Token: {token[:50]}...')
        
        # Test DELETE API
        print('\n=== Testing DELETE API ===')
        
        result = page.evaluate('''async () => {
            const token = localStorage.getItem("astrovedic_token");
            if (!token) return { error: "No token found in localStorage" };
            
            console.log("Making DELETE request to /api/kundli/user/all");
            
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
                
                const body = await response.text();
                console.log("Response status:", response.status);
                console.log("Response body:", body);
                
                return {
                    endpoint: "/api/kundli/user/all",
                    status: response.status,
                    statusText: response.statusText,
                    body: body
                };
            } catch (e) {
                console.error("Fetch error:", e);
                return { 
                    error: e.message,
                    name: e.name,
                    stack: e.stack
                };
            }
        }''')
        
        print('\nDELETE /user/all result:')
        print(json.dumps(result, indent=2))
        
        # Test individual delete
        print('\n=== Testing DELETE individual ===')
        result2 = page.evaluate('''async () => {
            const token = localStorage.getItem("astrovedic_token");
            try {
                const response = await fetch(
                    "https://astro-rattan-api.onrender.com/api/kundli/fake-id-12345",
                    {
                        method: "DELETE",
                        headers: {
                            "Authorization": "Bearer " + token,
                            "Content-Type": "application/json"
                        }
                    }
                );
                const body = await response.text();
                return {
                    endpoint: "/api/kundli/{id}",
                    status: response.status,
                    statusText: response.statusText,
                    body: body
                };
            } catch (e) {
                return { error: e.message, name: e.name };
            }
        }''')
        
        print('\nDELETE individual result:')
        print(json.dumps(result2, indent=2))
        
        # Check console for errors
        print('\n=== Console Logs ===')
        errors = [l for l in console_logs if 'error' in l.lower() or 'fail' in l.lower()]
        for log in errors:
            print(log)
        
        browser.close()

if __name__ == '__main__':
    test_delete()
