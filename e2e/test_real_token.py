"""Test with real token step by step"""
from playwright.sync_api import sync_playwright
import json

def test_step_by_step():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        
        # Login
        print('Logging in...')
        page.goto('https://astrovedic-web.vercel.app/login', timeout=60000)
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        page.locator('button:has-text("Sign In")').nth(1).click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)
        
        # Get token
        token = page.evaluate('() => localStorage.getItem("astrovedic_token")')
        print(f'Token: {token[:60]}...' if token else 'No token!')
        
        if not token:
            print('Login failed!')
            browser.close()
            return
        
        # Test 1: GET request
        print('\n=== Test 1: GET /api/kundli/list ===')
        result1 = page.evaluate('''async (token) => {
            try {
                const resp = await fetch("https://astro-rattan-api.onrender.com/api/kundli/list", {
                    headers: { "Authorization": "Bearer " + token }
                });
                return { status: resp.status, ok: true };
            } catch (e) {
                return { error: e.message, ok: false };
            }
        }''', token)
        print(f'GET result: {result1}')
        
        # Test 2: DELETE with real token
        print('\n=== Test 2: DELETE /api/kundli/user/all ===')
        
        # Set up console error capture
        cors_errors = []
        def capture_error(msg):
            if 'cors' in msg.text.lower() or 'blocked' in msg.text.lower():
                cors_errors.append(msg.text)
        page.on('console', capture_error)
        
        result2 = page.evaluate('''async (token) => {
            console.log("Making DELETE request...");
            console.log("Token:", token.substring(0, 20) + "...");
            try {
                const resp = await fetch("https://astro-rattan-api.onrender.com/api/kundli/user/all", {
                    method: "DELETE",
                    headers: {
                        "Authorization": "Bearer " + token,
                        "Content-Type": "application/json"
                    }
                });
                console.log("DELETE success, status:", resp.status);
                return { status: resp.status, ok: true };
            } catch (e) {
                console.error("DELETE failed:", e.message);
                return { error: e.message, name: e.name, ok: false };
            }
        }''', token)
        
        print(f'DELETE result: {result2}')
        print(f'CORS errors: {cors_errors}')
        
        # Test 3: DELETE individual kundli
        print('\n=== Test 3: DELETE /api/kundli/{id} ===')
        result3 = page.evaluate('''async (token) => {
            try {
                const resp = await fetch("https://astro-rattan-api.onrender.com/api/kundli/test-id-123", {
                    method: "DELETE",
                    headers: {
                        "Authorization": "Bearer " + token,
                        "Content-Type": "application/json"
                    }
                });
                return { status: resp.status, ok: true };
            } catch (e) {
                return { error: e.message, ok: false };
            }
        }''', token)
        print(f'DELETE individual result: {result3}')
        
        browser.close()

if __name__ == '__main__':
    test_step_by_step()
