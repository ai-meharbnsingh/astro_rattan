"""Debug CORS issue in detail"""
from playwright.sync_api import sync_playwright
import json

def test_cors():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        
        # Capture ALL network activity
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
                    'type': 'FAILED',
                    'method': request.method,
                    'url': request.url,
                    'error': str(request.failure)
                })
        
        page.on('request', on_request)
        page.on('response', on_response)
        page.on('requestfailed', on_fail)
        
        # Console logging
        page.on('console', lambda msg: print(f'[CONSOLE] {msg.type}: {msg.text}'))
        
        print('Opening app and logging in...')
        page.goto('https://astrovedic-web.vercel.app/login', timeout=60000)
        page.wait_for_load_state('networkidle')
        
        # Login
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        page.locator('button:has-text("Sign In")').nth(1).click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)
        
        # Test fetch with detailed error
        print('\n=== Testing DELETE with detailed capture ===')
        
        result = page.evaluate('''async () => {
            const token = localStorage.getItem("astrovedic_token");
            
            // First test a working GET endpoint
            console.log("Testing GET /api/kundli/list...");
            try {
                const getResp = await fetch("https://astro-rattan-api.onrender.com/api/kundli/list", {
                    headers: { "Authorization": "Bearer " + token }
                });
                console.log("GET status:", getResp.status);
            } catch (e) {
                console.error("GET error:", e.message);
            }
            
            // Now test DELETE
            console.log("Testing DELETE /api/kundli/user/all...");
            try {
                const deleteResp = await fetch("https://astro-rattan-api.onrender.com/api/kundli/user/all", {
                    method: "DELETE",
                    headers: {
                        "Authorization": "Bearer " + token,
                        "Content-Type": "application/json"
                    }
                });
                console.log("DELETE status:", deleteResp.status);
                return { success: true, status: deleteResp.status };
            } catch (e) {
                console.error("DELETE error:", e.message, e.name);
                return { 
                    success: false, 
                    error: e.message, 
                    name: e.name,
                    toString: e.toString()
                };
            }
        }''')
        
        print(f'\nResult: {json.dumps(result, indent=2)}')
        
        # Print all network events
        print('\n=== Network Events ===')
        for e in events:
            print(f"\n{e['type']}: {e['method']} {e['url'][:60]}...")
            if 'status' in e:
                print(f"  Status: {e['status']}")
                cors_headers = {k: v for k, v in e['headers'].items() if 'access-control' in k.lower()}
                if cors_headers:
                    print(f"  CORS Headers: {cors_headers}")
            if 'error' in e:
                print(f"  Error: {e['error']}")
        
        browser.close()

if __name__ == '__main__':
    test_cors()
