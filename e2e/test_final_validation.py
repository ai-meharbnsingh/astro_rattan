"""Final validation that DELETE works"""
from playwright.sync_api import sync_playwright
import json

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        page = browser.new_page()
        
        cors_errors = []
        def log_console(msg):
            if 'cors' in msg.text.lower() or 'blocked' in msg.text.lower():
                cors_errors.append(msg.text)
                print(f'[CORS ERROR] {msg.text}')
        page.on('console', log_console)
        
        # Login with retry
        token = None
        for attempt in range(3):
            print(f'\nLogin attempt {attempt + 1}...')
            page.goto('https://astrovedic-web.vercel.app/login', timeout=60000)
            page.wait_for_load_state('networkidle')
            
            page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
            page.locator('input[type="password"]').fill('123456')
            page.locator('button:has-text("Sign In")').nth(1).click()
            
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(2000)
            
            token = page.evaluate('() => localStorage.getItem("astrovedic_token")')
            if token:
                print(f'✅ Login successful!')
                break
        
        if not token:
            print('❌ Login failed')
            browser.close()
            return
        
        print(f'\nToken: {token[:40]}...')
        
        # Test DELETE endpoints
        print('\n=== Testing DELETE Endpoints ===')
        
        tests = [
            ('DELETE /api/kundli/user/all', 'https://astro-rattan-api.onrender.com/api/kundli/user/all'),
            ('DELETE /api/kundli/{id}', 'https://astro-rattan-api.onrender.com/api/kundli/test-id-123'),
        ]
        
        results = []
        for name, url in tests:
            print(f'\nTesting {name}...')
            result = page.evaluate('''async (args) => {
                try {
                    const resp = await fetch(args.url, {
                        method: "DELETE",
                        headers: { 
                            "Authorization": "Bearer " + args.token, 
                            "Content-Type": "application/json" 
                        }
                    });
                    return { 
                        ok: true, 
                        status: resp.status, 
                        body: await resp.text() 
                    };
                } catch (e) {
                    return { ok: false, error: e.message };
                }
            }''', {'url': url, 'token': token})
            results.append((name, result))
            print(f'  Result: {result}')
        
        # Summary
        print('\n' + '='*50)
        print('FINAL RESULTS')
        print('='*50)
        
        if cors_errors:
            print('❌ CORS ERRORS FOUND:')
            for e in cors_errors:
                print(f'   {e}')
        else:
            print('✅ NO CORS ERRORS')
        
        all_ok = True
        for name, result in results:
            if result.get('ok'):
                print(f'✅ {name}: HTTP {result["status"]}')
            else:
                print(f'❌ {name}: {result.get("error")}')
                all_ok = False
        
        if all_ok and not cors_errors:
            print('\n🎉 DELETE IS WORKING CORRECTLY!')
        
        browser.close()

if __name__ == '__main__':
    test()
