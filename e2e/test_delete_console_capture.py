"""Capture exact console error"""
from playwright.sync_api import sync_playwright
import json

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        page = browser.new_page()
        
        # Capture ALL console messages
        all_logs = []
        def log_all(msg):
            all_logs.append(f'[{msg.type}] {msg.text}')
            print(f'[{msg.type}] {msg.text[:150]}')
        page.on('console', log_all)
        
        # Login
        print('=== Logging in ===')
        page.goto('https://astrovedic-web.vercel.app/login', timeout=60000)
        page.wait_for_load_state('networkidle')
        
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        page.locator('button:has-text("Sign In")').nth(1).click()
        
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(3000)
        
        token = page.evaluate('() => localStorage.getItem("astrovedic_token")')
        print(f'\nToken: {"Yes" if token else "No"}')
        
        # Try DELETE
        print('\n=== Making DELETE request ===')
        
        result = page.evaluate('''async (t) => {
            console.log("Starting DELETE request...");
            console.log("Token length:", t.length);
            
            try {
                const controller = new AbortController();
                const timeout = setTimeout(() => controller.abort(), 10000);
                
                const resp = await fetch("https://astro-rattan-api.onrender.com/api/kundli/user/all", {
                    method: "DELETE",
                    headers: { 
                        "Authorization": "Bearer " + t, 
                        "Content-Type": "application/json"
                    },
                    signal: controller.signal
                });
                
                clearTimeout(timeout);
                console.log("Response received:", resp.status);
                return { ok: true, status: resp.status };
                
            } catch (e) {
                console.error("Fetch failed:", e.name, e.message);
                return { ok: false, error: e.message, type: e.name };
            }
        }''', token)
        
        print(f'\nResult: {result}')
        
        # Print all errors
        print('\n=== All Console Errors ===')
        errors = [l for l in all_logs if 'error' in l.lower()]
        for e in errors:
            print(e)
        
        browser.close()

if __name__ == '__main__':
    test()
