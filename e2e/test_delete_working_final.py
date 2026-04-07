"""Final working delete test"""
from playwright.sync_api import sync_playwright
import json

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()
        
        print('=== Step 1: Login ===')
        page.goto('https://astrovedic-web.vercel.app/login', timeout=60000)
        page.wait_for_load_state('networkidle')
        
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        page.locator('button:has-text("Sign In")').nth(1).click()
        
        # Wait for navigation
        page.wait_for_url('https://astrovedic-web.vercel.app/**', timeout=10000)
        page.wait_for_timeout(2000)
        
        # Verify token
        token = page.evaluate('() => localStorage.getItem("astrovedic_token")')
        if not token:
            print('❌ Login failed - no token')
            browser.close()
            return
        print(f'✅ Token acquired: {token[:30]}...')
        
        print('\n=== Step 2: Test DELETE ===')
        
        # Capture console errors
        errors = []
        page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
        
        # Test 1: GET list (should work)
        print('Testing GET /api/kundli/list...')
        get_result = page.evaluate('''async (t) => {
            const r = await fetch("https://astro-rattan-api.onrender.com/api/kundli/list", {
                headers: { "Authorization": "Bearer " + t }
            });
            return r.status;
        }''', token)
        print(f'GET status: {get_result}')
        
        # Test 2: DELETE all
        print('Testing DELETE /api/kundli/user/all...')
        delete_all_result = page.evaluate('''async (t) => {
            try {
                const r = await fetch("https://astro-rattan-api.onrender.com/api/kundli/user/all", {
                    method: "DELETE",
                    headers: { "Authorization": "Bearer " + t, "Content-Type": "application/json" }
                });
                return { ok: true, status: r.status, body: await r.text() };
            } catch (e) {
                return { ok: false, error: e.message };
            }
        }''', token)
        print(f'DELETE all result: {json.dumps(delete_all_result)}')
        
        # Test 3: DELETE individual
        print('Testing DELETE /api/kundli/{id}...')
        delete_one_result = page.evaluate('''async (t) => {
            try {
                const r = await fetch("https://astro-rattan-api.onrender.com/api/kundli/fake-id", {
                    method: "DELETE",
                    headers: { "Authorization": "Bearer " + t, "Content-Type": "application/json" }
                });
                return { ok: true, status: r.status, body: await r.text() };
            } catch (e) {
                return { ok: false, error: e.message };
            }
        }''', token)
        print(f'DELETE one result: {json.dumps(delete_one_result)}')
        
        # Summary
        print('\n=== SUMMARY ===')
        cors_errors = [e for e in errors if 'cors' in e.lower()]
        
        if cors_errors:
            print('❌ CORS errors found:')
            for e in cors_errors:
                print(f'   {e}')
        else:
            print('✅ No CORS errors')
            
        if delete_all_result.get('ok') and delete_one_result.get('ok'):
            print('✅ DELETE requests working')
            print(f'   /user/all: HTTP {delete_all_result["status"]}')
            print(f'   /{{id}}: HTTP {delete_one_result["status"]}')
        else:
            print('❌ DELETE failed')
            if not delete_all_result.get('ok'):
                print(f'   /user/all: {delete_all_result.get("error")}')
            if not delete_one_result.get('ok'):
                print(f'   /{{id}}: {delete_one_result.get("error")}')
        
        browser.close()

if __name__ == '__main__':
    test()
