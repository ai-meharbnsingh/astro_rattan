"""Final delete test with working login"""
from playwright.sync_api import sync_playwright
import json

def test_delete():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        
        cors_errors = []
        def log_console(msg):
            text = msg.text.lower()
            if 'cors' in text or 'blocked' in text or 'failed to fetch' in text:
                cors_errors.append(msg.text)
                print(f'[CORS ERROR] {msg.text}')
        page.on('console', log_console)
        
        # Login
        print('=== Logging in ===')
        page.goto('https://astrovedic-web.vercel.app/login', timeout=60000)
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        page.locator('button:has-text("Sign In")').nth(1).click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)
        
        token = page.evaluate('() => localStorage.getItem("astrovedic_token")')
        print(f'Token: {"Yes" if token else "No"}')
        
        # Test DELETE /user/all
        print('\n=== DELETE /api/kundli/user/all ===')
        result = page.evaluate('''async (token) => {
            try {
                const resp = await fetch("https://astro-rattan-api.onrender.com/api/kundli/user/all", {
                    method: "DELETE",
                    headers: {
                        "Authorization": "Bearer " + token,
                        "Content-Type": "application/json"
                    }
                });
                const body = await resp.text();
                return { 
                    status: resp.status, 
                    statusText: resp.statusText,
                    body: body,
                    success: true
                };
            } catch (e) {
                return { 
                    error: e.message, 
                    name: e.name,
                    success: false
                };
            }
        }''', token)
        
        print(f'Result: {json.dumps(result, indent=2)}')
        print(f'CORS errors: {cors_errors}')
        
        # Test DELETE individual
        print('\n=== DELETE /api/kundli/{id} ===')
        cors_errors.clear()
        
        result2 = page.evaluate('''async (token) => {
            try {
                const resp = await fetch("https://astro-rattan-api.onrender.com/api/kundli/test-id-12345", {
                    method: "DELETE",
                    headers: {
                        "Authorization": "Bearer " + token,
                        "Content-Type": "application/json"
                    }
                });
                const body = await resp.text();
                return { 
                    status: resp.status, 
                    body: body,
                    success: true
                };
            } catch (e) {
                return { 
                    error: e.message,
                    success: false
                };
            }
        }''', token)
        
        print(f'Result: {json.dumps(result2, indent=2)}')
        print(f'CORS errors: {cors_errors}')
        
        browser.close()
        
        # Summary
        print('\n=== SUMMARY ===')
        if result.get('success') and result2.get('success'):
            print('✅ Both DELETE endpoints working!')
            print(f'   /user/all: {result["status"]}')
            print(f'   /{{id}}: {result2["status"]}')
        else:
            print('❌ DELETE not working')
            if not result.get('success'):
                print(f'   /user/all error: {result.get("error")}')
            if not result2.get('success'):
                print(f'   /{{id}} error: {result2.get("error")}')

if __name__ == '__main__':
    test_delete()
