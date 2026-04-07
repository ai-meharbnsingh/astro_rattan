"""Final test for delete functionality with correct selectors"""
from playwright.sync_api import sync_playwright
import json

def test_delete():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()
        
        # Capture console logs
        console_logs = []
        page.on('console', lambda msg: console_logs.append(f'[{msg.type}] {msg.text}'))
        
        # Capture network
        api_calls = []
        page.on('response', lambda r: api_calls.append({
            'method': r.request.method,
            'url': r.url,
            'status': r.status
        }) if 'api' in r.url else None)
        
        print('=== Opening app ===')
        page.goto('https://astrovedic-web.vercel.app', timeout=60000)
        page.wait_for_load_state('networkidle')
        page.screenshot(path='./e2e/screenshots/01_home.png')
        
        # Click Sign In
        print('\n=== Clicking Sign In ===')
        page.locator('text=Sign In').first.click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)
        page.screenshot(path='./e2e/screenshots/02_login_form.png')
        
        # Fill login form
        print('Filling credentials...')
        page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
        page.locator('input[type="password"]').fill('123456')
        page.screenshot(path='./e2e/screenshots/03_filled.png')
        
        # Click Sign In button
        print('Submitting...')
        page.locator('button:has-text("Sign In")').click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)
        page.screenshot(path='./e2e/screenshots/04_after_submit.png')
        
        # Check for error
        error = page.locator('text=Invalid, text=Error, text=Failed').first
        if error.is_visible():
            print(f'Login error: {error.text_content()}')
            browser.close()
            return
        
        # Check token
        token = page.evaluate('() => localStorage.getItem("astrovedic_token")')
        print(f'\nToken present: {bool(token)}')
        
        # Navigate to Kundli
        print('\n=== Going to Kundli page ===')
        page.locator('a[href="/kundli"]').first.click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)
        page.screenshot(path='./e2e/screenshots/05_kundli_page.png')
        
        # Look for "My Kundlis" or saved section
        print('Looking for saved kundlis...')
        
        my_kundlis = page.locator('text=My Kundlis').first
        if my_kundlis.is_visible():
            print('Found My Kundlis - clicking')
            my_kundlis.click()
            page.wait_for_timeout(2000)
            page.screenshot(path='./e2e/screenshots/06_my_kundlis.png')
        
        # Look for delete buttons
        print('\n=== Looking for delete buttons ===')
        
        # Check all buttons on page
        all_buttons = page.locator('button').all()
        print(f'Total buttons: {len(all_buttons)}')
        
        delete_btns = []
        for i, btn in enumerate(all_buttons):
            text = btn.text_content() or ''
            title = btn.get_attribute('title') or ''
            if 'delete' in text.lower() or 'trash' in text.lower() or 'delete' in title.lower():
                print(f'Found delete button: "{text}" title="{title}"')
                delete_btns.append(btn)
        
        if not delete_btns:
            print('No delete buttons with text found, checking for trash icons...')
            # Look inside kundli items
            kundli_items = page.locator('.group, [class*="kundli-item"]').all()
            print(f'Kundli items found: {len(kundli_items)}')
            
            if kundli_items:
                for i, item in enumerate(kundli_items[:3]):
                    text = item.text_content() or ''
                    print(f'\nItem {i}: {text[:80]}...')
                    
                    # Look for any button inside
                    item_btns = item.locator('button').all()
                    for j, btn in enumerate(item_btns):
                        btn_text = btn.text_content() or ''
                        print(f'  Button {j}: "{btn_text[:30]}"')
                        btn.screenshot(path=f'./e2e/screenshots/item_{i}_btn_{j}.png')
        
        # Now test DELETE API from browser
        print('\n=== Testing DELETE API from browser ===')
        
        result = page.evaluate('''async () => {
            const token = localStorage.getItem("astrovedic_token");
            if (!token) return { error: "No token" };
            
            console.log("Testing DELETE /api/kundli/user/all");
            
            try {
                const response = await fetch(
                    "https://astro-rattan-api.onrender.com/api/kundli/user/all",
                    {
                        method: "DELETE",
                        headers: {
                            "Authorization": "Bearer " + token,
                            "Content-Type": "application/json"
                        }
                    }
                );
                
                const body = await response.text();
                
                return {
                    status: response.status,
                    statusText: response.statusText,
                    body: body
                };
            } catch (e) {
                return { 
                    error: e.message,
                    name: e.name,
                    stack: e.stack
                };
            }
        }''')
        
        print('\nDELETE /user/all result:')
        print(json.dumps(result, indent=2))
        
        # Test individual delete
        print('\n=== Testing DELETE individual ===')
        result2 = page.evaluate('''async () => {
            const token = localStorage.getItem("astrovedic_token");
            
            try {
                const response = await fetch(
                    "https://astro-rattan-api.onrender.com/api/kundli/test-id-123",
                    {
                        method: "DELETE",
                        headers: {
                            "Authorization": "Bearer " + token,
                            "Content-Type": "application/json"
                        }
                    }
                );
                
                return {
                    status: response.status,
                    statusText: response.statusText,
                    body: await response.text()
                };
            } catch (e) {
                return { error: e.message, name: e.name };
            }
        }''')
        
        print('\nDELETE individual result:')
        print(json.dumps(result2, indent=2))
        
        # Print console logs
        print('\n=== Console Logs ===')
        for log in console_logs:
            print(log)
        
        browser.close()

if __name__ == '__main__':
    test_delete()
