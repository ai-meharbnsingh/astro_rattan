"""Test with fresh login to get valid token"""
from playwright.sync_api import sync_playwright
import json

def test_with_fresh_token():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()
        
        print('=== Fresh Login Test ===')
        
        # Clear storage
        page.context.clear_cookies()
        
        # Go to login
        page.goto('https://astrovedic-web.vercel.app/login', timeout=60000)
        page.wait_for_load_state('networkidle')
        
        # Fill and submit
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        page.locator('button:has-text("Sign In")').nth(1).click()
        
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(3000)
        
        # Check if login succeeded
        token = page.evaluate('() => localStorage.getItem("astrovedic_token")')
        print(f'Token present: {bool(token)}')
        
        if not token:
            print('Login failed - no token!')
            page.screenshot(path='./e2e/screenshots/login_failed.png')
            browser.close()
            return
        
        # Decode token to check
        import base64
        try:
            payload = token.split('.')[1]
            decoded = base64.b64decode(payload + '==')
            print(f'Token payload: {decoded.decode()}')
        except Exception as e:
            print(f'Token decode error: {e}')
        
        # Test DELETE
        print('\n=== Testing DELETE ===')
        
        result = page.evaluate('''async () => {
            const token = localStorage.getItem("astrovedic_token");
            
            // Test 1: List kundlis first
            console.log("1. GET /api/kundli/list");
            const listResp = await fetch("https://astro-rattan-api.onrender.com/api/kundli/list", {
                headers: { "Authorization": "Bearer " + token }
            });
            console.log("List status:", listResp.status);
            const listData = await listResp.json().catch(() => []);
            console.log("Kundlis count:", listData.length || 0);
            
            // Test 2: Delete all
            console.log("2. DELETE /api/kundli/user/all");
            const deleteResp = await fetch("https://astro-rattan-api.onrender.com/api/kundli/user/all", {
                method: "DELETE",
                headers: {
                    "Authorization": "Bearer " + token,
                    "Content-Type": "application/json"
                }
            });
            console.log("Delete status:", deleteResp.status);
            const deleteData = await deleteResp.json().catch(() => ({}));
            
            return {
                listStatus: listResp.status,
                kundlisCount: listData.length || 0,
                deleteStatus: deleteResp.status,
                deleteResponse: deleteData
            };
        }''')
        
        print(f'\nResult: {json.dumps(result, indent=2)}')
        
        # Take final screenshot
        page.screenshot(path='./e2e/screenshots/final_result.png')
        
        browser.close()

if __name__ == '__main__':
    test_with_fresh_token()
