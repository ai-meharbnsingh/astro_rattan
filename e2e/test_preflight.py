"""Test preflight OPTIONS request"""
from playwright.sync_api import sync_playwright
import json

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        page = browser.new_page()
        
        events = []
        
        def on_request(request):
            if 'kundli' in request.url:
                events.append({
                    'type': 'REQ',
                    'method': request.method,
                    'url': request.url
                })
        
        def on_response(response):
            if 'kundli' in response.url:
                events.append({
                    'type': 'RES',
                    'method': response.request.method,
                    'url': response.url,
                    'status': response.status,
                    'cors': {k: v for k, v in response.headers.items() if 'access' in k.lower()}
                })
        
        page.on('request', on_request)
        page.on('response', on_response)
        page.on('console', lambda m: print(f'[CONSOLE] {m.text[:100]}') if 'cors' in m.text.lower() or 'error' in m.type.lower() else None)
        
        # Login
        page.goto('https://astrovedic-web.vercel.app/login', timeout=60000)
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        page.locator('button:has-text("Sign In")').nth(1).click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)
        
        token = page.evaluate('() => localStorage.getItem("astrovedic_token")')
        print(f'Token: {"Yes" if token else "No"}')
        
        # Clear previous events
        events.clear()
        
        # Make DELETE request
        print('\nMaking DELETE request...')
        result = page.evaluate('''async (t) => {
            try {
                const resp = await fetch("https://astro-rattan-api.onrender.com/api/kundli/user/all", {
                    method: "DELETE",
                    headers: { 
                        "Authorization": "Bearer " + t, 
                        "Content-Type": "application/json"
                    }
                });
                return { ok: true, status: resp.status };
            } catch (e) {
                return { ok: false, error: e.message };
            }
        }''', token)
        
        print(f'Result: {result}')
        
        # Print all events
        print('\n=== All Network Events ===')
        for e in events:
            print(f"{e['type']} {e['method']} {e['url'][:60]}...")
            if 'status' in e:
                print(f"  Status: {e['status']}")
                if e['cors']:
                    print(f"  CORS: {e['cors']}")
        
        browser.close()

if __name__ == '__main__':
    test()
