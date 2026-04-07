"""Test delete with actual credentials"""
from playwright.sync_api import sync_playwright
import json

def test_delete_with_real_user():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context()
        page = context.new_page()
        
        network_logs = []
        
        def log_response(response):
            req = response.request
            if 'api' in response.url:
                network_logs.append({
                    'method': req.method,
                    'url': response.url,
                    'status': response.status
                })
                print(f'[API] {req.method} {response.status} {response.url[:60]}...')
        
        def log_failure(request):
            if 'api' in request.url:
                failure = request.failure
                print(f'[FAILED] {request.method} {request.url}')
                print(f'  Error: {failure}')
        
        page.on('response', log_response)
        page.on('requestfailed', log_failure)
        
        # Capture alerts
        def handle_dialog(dialog):
            print(f'[DIALOG] {dialog.type}: {dialog.message}')
            dialog.accept()
        
        page.on('dialog', handle_dialog)
        
        try:
            print('=== Opening app ===')
            page.goto('https://astrovedic-web.vercel.app', timeout=60000)
            page.wait_for_load_state('networkidle')
            
            # Click Login
            print('\n=== Clicking Login ===')
            page.locator('text=Login').first.click()
            page.wait_for_load_state('networkidle')
            
            # Fill credentials
            print('Filling credentials...')
            page.locator('input[type="email"]').fill('ai.meharbansingh@gmail.com')
            page.locator('input[type="password"]').fill('123456')
            
            # Click Sign In
            page.locator('button:has-text("Sign In")').click()
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(2000)
            
            # Check if logged in
            token = page.evaluate('() => localStorage.getItem("astrovedic_token")')
            print(f'Token present: {bool(token)}')
            if token:
                print(f'Token preview: {token[:50]}...')
            
            page.screenshot(path='./e2e/screenshots/01_after_login.png')
            
            # Navigate to Kundli Generator
            print('\n=== Navigating to Kundli Generator ===')
            page.locator('text=Kundli Generator').first.click()
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(2000)
            
            page.screenshot(path='./e2e/screenshots/02_kundli_generator.png')
            
            # Check for "My Kundlis" button/link
            print('\n=== Looking for My Kundlis ===')
            my_kundlis = page.locator('text=My Kundlis').first
            if my_kundlis.is_visible():
                print('Found My Kundlis - clicking')
                my_kundlis.click()
                page.wait_for_load_state('networkidle')
                page.wait_for_timeout(2000)
            else:
                # Try to find saved kundlis section
                print('Looking for saved kundlis section...')
                saved_section = page.locator('text=Saved, text=My Charts').first
                if saved_section.is_visible():
                    saved_section.click()
            
            page.screenshot(path='./e2e/screenshots/03_kundli_list.png')
            
            # Look for delete buttons
            print('\n=== Looking for delete buttons ===')
            
            # Multiple selectors to try
            selectors = [
                'button:has(svg)',
                '[class*="delete"]',
                '[class*="trash"]',
                'button[class*="icon"]'
            ]
            
            all_buttons = page.locator('button').all()
            print(f'Total buttons on page: {len(all_buttons)}')
            
            for i, btn in enumerate(all_buttons[:10]):
                text = btn.text_content() or ''
                title = btn.get_attribute('title') or ''
                if 'delete' in text.lower() or 'trash' in text.lower() or 'delete' in title.lower():
                    print(f'Found delete button {i}: text="{text}" title="{title}"')
                    btn.screenshot(path=f'./e2e/screenshots/delete_btn_{i}.png')
            
            # Check for trash icon
            trash_buttons = page.locator('svg').all()
            print(f'SVG elements: {len(trash_buttons)}')
            
            # Now check the actual KundliList component
            print('\n=== Checking KundliList component ===')
            
            # Look for kundli items
            kundli_items = page.locator('[class*="kundli"], [class*="chart"], .group').all()
            print(f'Kundli items found: {len(kundli_items)}')
            
            if len(kundli_items) > 0:
                for i, item in enumerate(kundli_items[:3]):
                    print(f'\nItem {i}:')
                    print(f'  Text: {item.text_content()[:100]}...')
                    
                    # Look for delete button inside this item
                    delete_btn = item.locator('button').first
                    if delete_btn.is_visible():
                        print('  Has button - clicking to see what happens')
                        delete_btn.click()
                        page.wait_for_timeout(1000)
                        
                        # Check for confirm dialog
                        confirm = page.locator('text=Are you sure, text=Confirm').first
                        if confirm.is_visible():
                            print('  Confirmation dialog appeared!')
                            page.screenshot(path=f'./e2e/screenshots/04_confirm_dialog.png')
                            
                            # Click OK/Yes
                            ok_btn = page.locator('button:has-text("OK"), button:has-text("Yes"), button:has-text("Delete")').first
                            if ok_btn.is_visible():
                                ok_btn.click()
                                page.wait_for_timeout(3000)
                                page.screenshot(path='./e2e/screenshots/05_after_delete.png')
                        break
            
            # Test the DELETE API directly from browser console
            print('\n=== Testing DELETE API from browser ===')
            result = page.evaluate('''async () => {
                const token = localStorage.getItem("astrovedic_token");
                if (!token) return { error: "No token found" };
                
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
                        url: "https://astro-rattan-api.onrender.com/api/kundli/user/all",
                        method: "DELETE",
                        status: response.status,
                        statusText: response.statusText,
                        body: body,
                        headers: Object.fromEntries(response.headers.entries())
                    };
                } catch (e) {
                    console.error("Fetch error:", e);
                    return { 
                        error: e.message, 
                        type: e.name,
                        stack: e.stack
                    };
                }
            }''')
            
            print(f'\nDELETE /user/all result:')
            print(json.dumps(result, indent=2))
            
            # Also test individual delete with a fake ID
            print('\n=== Testing DELETE individual kundli ===')
            result2 = page.evaluate('''async () => {
                const token = localStorage.getItem("astrovedic_token");
                
                try {
                    const response = await fetch(
                        "https://astro-rattan-api.onrender.com/api/kundli/nonexistent-id-123",
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
                    return { error: e.message, type: e.name };
                }
            }''')
            
            print(f'\nDELETE /{kundli_id} result:')
            print(json.dumps(result2, indent=2))
            
            # Print all network logs
            print('\n=== All API Calls ===')
            for log in network_logs:
                print(f"{log['method']} {log['status']} {log['url'][:70]}...")
            
        except Exception as e:
            print(f'ERROR: {e}')
            import traceback
            traceback.print_exc()
            page.screenshot(path='./e2e/screenshots/error.png')
        finally:
            browser.close()

if __name__ == '__main__':
    test_delete_with_real_user()
