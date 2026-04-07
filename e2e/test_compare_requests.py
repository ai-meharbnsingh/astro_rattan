"""Compare curl vs browser request"""
from playwright.sync_api import sync_playwright
import subprocess
import json

def test_compare():
    # First test with curl
    print('=== CURL Test ===')
    result = subprocess.run([
        'curl', '-s', '-X', 'DELETE',
        '-H', 'Origin: https://astrovedic-web.vercel.app',
        '-H', 'Authorization: Bearer test_token_123',
        '-H', 'Content-Type: application/json',
        '-w', '\nHTTP:%{http_code}\n',
        'https://astro-rattan-api.onrender.com/api/kundli/user/all'
    ], capture_output=True, text=True)
    print(f'Curl output: {result.stdout[:200]}...')
    print(f'Curl stderr: {result.stderr[:200]}...')
    
    # Now test with browser
    print('\n=== Browser Test ===')
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to vercel app first (to set origin)
        page.goto('https://astrovedic-web.vercel.app', timeout=60000)
        
        # Set token manually
        page.evaluate('() => localStorage.setItem("astrovedic_token", "test_token_123")')
        
        # Try fetch
        result = page.evaluate('''async () => {
            try {
                const resp = await fetch("https://astro-rattan-api.onrender.com/api/kundli/user/all", {
                    method: "DELETE",
                    headers: {
                        "Authorization": "Bearer test_token_123",
                        "Content-Type": "application/json"
                    }
                });
                return { status: resp.status, ok: true };
            } catch (e) {
                return { error: e.message, name: e.name, ok: false };
            }
        }''')
        
        print(f'Browser result: {json.dumps(result)}')
        
        # Check console for CORS errors
        console_errors = []
        page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)
        
        page.wait_for_timeout(1000)
        
        print(f'Console errors: {console_errors}')
        
        browser.close()

if __name__ == '__main__':
    test_compare()
