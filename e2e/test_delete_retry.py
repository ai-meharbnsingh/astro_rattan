"""Test with retry logic"""
from playwright.sync_api import sync_playwright
import json
import time

def test_with_retry():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        page = browser.new_page()
        
        # Try login up to 3 times
        token = None
        for attempt in range(3):
            print(f'\n=== Login attempt {attempt + 1} ===')
            
            page.goto('https://astrovedic-web.vercel.app/login', timeout=60000)
            page.wait_for_load_state('networkidle')
            time.sleep(1)
            
            # Clear and fill
            page.locator('input[type="email"]').fill('')
            page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
            page.locator('input[type="password"]').fill('')
            page.locator('input[type="password"]').fill('123456')
            
            # Click sign in
            page.locator('button:has-text("Sign In")').nth(1).click()
            
            # Wait
            page.wait_for_load_state('networkidle')
            time.sleep(3)
            
            # Check token
            token = page.evaluate('() => localStorage.getItem("astrovedic_token")')
            if token:
                print(f'✅ Login successful!')
                break
            else:
                print(f'❌ No token, current URL: {page.url}')
        
        if not token:
            print('Failed to login after 3 attempts')
            browser.close()
            return
        
        print(f'\nToken: {token[:40]}...')
        
        # Now test DELETE
        print('\n=== Testing DELETE ===')
        
        results = []
        
        # Test DELETE all
        print('Testing DELETE /user/all...')
        r1 = page.evaluate('''async (t) => {
            try {
                const resp = await fetch("https://astro-rattan-api.onrender.com/api/kundli/user/all", {
                    method: "DELETE",
                    headers: { "Authorization": "Bearer " + t, "Content-Type": "application/json" }
                });
                return { ok: true, status: resp.status };
            } catch (e) {
                return { ok: false, error: e.message };
            }
        }''', token)
        results.append(('DELETE /user/all', r1))
        print(f'  Result: {r1}')
        
        # Test DELETE one
        print('Testing DELETE /{id}...')
        r2 = page.evaluate('''async (t) => {
            try {
                const resp = await fetch("https://astro-rattan-api.onrender.com/api/kundli/test-id", {
                    method: "DELETE",
                    headers: { "Authorization": "Bearer " + t, "Content-Type": "application/json" }
                });
                return { ok: true, status: resp.status };
            } catch (e) {
                return { ok: false, error: e.message };
            }
        }''', token)
        results.append(('DELETE /{id}', r2))
        print(f'  Result: {r2}')
        
        # Summary
        print('\n=== RESULTS ===')
        for name, result in results:
            if result.get('ok'):
                print(f'✅ {name}: HTTP {result["status"]}')
            else:
                print(f'❌ {name}: {result.get("error")}')
        
        browser.close()

if __name__ == '__main__':
    test_with_retry()
