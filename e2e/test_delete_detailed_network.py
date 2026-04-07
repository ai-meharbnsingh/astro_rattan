"""Detailed network capture"""
from playwright.sync_api import sync_playwright
import json

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        page = browser.new_page()
        
        # Capture network
        events = []
        
        def on_request(request):
            if 'kundli' in request.url:
                events.append({
                    'type': 'REQUEST',
                    'method': request.method,
                    'url': request.url,
                    'headers': dict(request.headers)
                })
        
        def on_response(response):
            if 'kundli' in response.url:
                events.append({
                    'type': 'RESPONSE',
                    'method': response.request.method,
                    'url': response.url,
                    'status': response.status,
                    'headers': dict(response.headers)
                })
        
        def on_fail(request):
            if 'kundli' in request.url:
                events.append({
                    'type': 'FAIL',
                    'method': request.method,
                    'url': request.url,
                    'error': str(request.failure) if hasattr(request, 'failure') else 'unknown'
                })
        
        page.on('request', on_request)
        page.on('response', on_response)
        page.on('requestfailed', on_fail)
        
        # Console
        page.on('console', lambda m: print(f'[{m.type}] {m.text[:120]}') if 'error' in m.type.lower() or 'cors' in m.text.lower() else None)
        
        # Login
        page.goto('https://astrovedic-web.vercel.app/login', timeout=60000)
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        page.locator('button:has-text("Sign In")').nth(1).click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)
        
        token = page.evaluate('() => localStorage.getItem("astrovedic_token")')
        print(f'Token: {"Yes" if token else "No"}')
        
        # Try DELETE
        print('\nMaking DELETE request...')
        result = page.evaluate('''async (t) => {
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
        
        print(f'Result: {result}')
        
        # Print network events
        print('\n=== Network Events ===')
        for e in events:
            print(f"\n{e['type']}: {e['method']} {e['url'][:70]}...")
            if 'status' in e:
                print(f"  Status: {e['status']}")
                cors = {k: v for k, v in e['headers'].items() if 'access' in k.lower()}
                if cors:
                    print(f"  CORS: {cors}")
            if 'error' in e:
                print(f"  Error: {e['error']}")
            if 'headers' in e and e['type'] == 'REQUEST':
                print(f"  Req Headers: {list(e['headers'].keys())}")
        
        browser.close()

if __name__ == '__main__':
    test()
