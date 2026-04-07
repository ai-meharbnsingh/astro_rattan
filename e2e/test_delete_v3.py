"""Test delete - fixed selectors"""
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
        
        # Click Sign In link
        print('\n=== Clicking Sign In ===')
        page.locator('a[href="/login"]').click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)
        
        # Fill form
        print('Filling credentials...')
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        
        # Click the submit button (not the tab)
        print('Submitting...')
        page.locator('form button[type="submit"]').click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)
        
        # Check for error
        error = page.locator('text=Invalid, text=Error, text=Failed, text=incorrect').first
        if error.is_visible():
            print(f'Login error: {error.text_content()}')
            browser.close()
            return
        
        # Check token
        token = page.evaluate('() => localStorage.getItem("astrovedic_token")')
        print(f'\nToken present: {bool(token)}')
        
        # Go to kundli page
        print('\n=== Going to Kundli ===')
        page.goto('https://astrovedic-web.vercel.app/kundli')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)
        page.screenshot(path='./e2e/screenshots/kundli_page.png')
        
        # Look for "My Kundlis" button
        my_kundlis = page.locator('text=My Kundlis').first
        if my_kundlis.is_visible():
            print('Clicking My Kundlis...')
            my_kundlis.click()
            page.wait_for_timeout(2000)
            page.screenshot(path='./e2e/screenshots/my_kundlis.png')
        
        # Test DELETE API
        print('\n=== Testing DELETE API ===')
        
        result = page.evaluate('''async () => {
            const token = localStorage.getItem("astrovedic_token");
            if (!token) return { error: "No token" };
            
            // Test DELETE /user/all
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
                    endpoint: "/api/kundli/user/all",
                    status: response.status,
                    statusText: response.statusText,
                    body: await response.text()
                };
            } catch (e) {
                return { error: e.message, name: e.name };
            }
        }''')
        
        print('\nDELETE /user/all:')
        print(json.dumps(result, indent=2))
        
        # Test individual delete
        result2 = page.evaluate('''async () => {
            const token = localStorage.getItem("astrovedic_token");
            try {
                const response = await fetch(
                    "https://astro-rattan-api.onrender.com/api/kundli/fake-id",
                    {
                        method: "DELETE",
                        headers: {
                            "Authorization": "Bearer " + token,
                            "Content-Type": "application/json"
                        }
                    }
                );
                return {
                    endpoint: "/api/kundli/{id}",
                    status: response.status,
                    statusText: response.statusText,
                    body: await response.text()
                };
            } catch (e) {
                return { error: e.message, name: e.name };
            }
        }''')
        
        print('\nDELETE /{kundli_id}:')
        print(json.dumps(result2, indent=2))
        
        # Look for console errors
        print('\n=== Console Logs ===')
        for log in console_logs:
            print(log)
        
        browser.close()

if __name__ == '__main__':
    test_delete()
