"""Test delete with actual browser network inspection"""
from playwright.sync_api import sync_playwright
import json

def test_delete_network():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # Capture all network activity
        network_logs = []
        
        def log_request(request):
            if 'api' in request.url:
                network_logs.append({
                    'type': 'request',
                    'method': request.method,
                    'url': request.url,
                    'headers': dict(request.headers)
                })
        
        def log_response(response):
            if 'api' in response.url:
                req = response.request
                network_logs.append({
                    'type': 'response',
                    'method': req.method,
                    'url': response.url,
                    'status': response.status,
                    'headers': dict(response.headers)
                })
        
        def log_failure(request):
            if 'api' in request.url:
                network_logs.append({
                    'type': 'failure',
                    'method': request.method,
                    'url': request.url,
                    'error': request.failure if hasattr(request, 'failure') else 'Unknown'
                })
        
        page.on('request', log_request)
        page.on('response', log_response)
        page.on('requestfailed', log_failure)
        
        # Capture console errors
        console_errors = []
        def log_console(msg):
            if msg.type == 'error':
                console_errors.append(msg.text)
                print(f'[CONSOLE ERROR] {msg.text}')
        
        page.on('console', log_console)
        
        try:
            print('Opening app...')
            page.goto('https://astrovedic-web.vercel.app', timeout=60000)
            page.wait_for_load_state('networkidle')
            
            # Check localStorage for token
            token = page.evaluate('() => localStorage.getItem("astrovedic_token")')
            print(f'Token in localStorage: {token[:50]}...' if token and len(token) > 50 else f'Token: {token}')
            
            # Look for login/my kundlis
            if page.locator('text=Login').first.is_visible():
                print('User NOT logged in - clicking Login')
                page.locator('text=Login').first.click()
                page.wait_for_load_state('networkidle')
                
                # Try to login with test account
                page.locator('input[type="email"]').fill('test@example.com')
                page.locator('input[type="password"]').fill('test123')
                page.locator('button:has-text("Sign In"), button:has-text("Login")').click()
                
                page.wait_for_load_state('networkidle')
                page.wait_for_timeout(2000)
                
                # Check if login succeeded
                error_msg = page.locator('text=Invalid, text=error').first
                if error_msg.is_visible():
                    print(f'Login failed: {error_msg.text_content()}')
                    
                    # Try registration
                    page.locator('text=Sign Up, text=Register').first.click()
                    page.locator('input[name="name"], input[placeholder*="name"]').fill('Test User')
                    page.locator('input[type="email"]').fill('test@example.com')
                    page.locator('input[type="password"]').fill('test123')
                    page.locator('button:has-text("Sign Up"), button:has-text("Register")').click()
                    page.wait_for_timeout(2000)
            
            # Now check token again
            token = page.evaluate('() => localStorage.getItem("astrovedic_token")')
            print(f'Token after auth: {"Yes" if token else "No"}')
            
            # Navigate to kundli section
            print('\nNavigating to kundli...')
            
            # Look for kundli link
            kundli_links = [
                'text=Kundli',
                'text=My Kundlis',
                'text=Birth Chart',
                'a[href*="kundli"]'
            ]
            
            for selector in kundli_links:
                try:
                    if page.locator(selector).first.is_visible():
                        print(f'Found: {selector}')
                        page.locator(selector).first.click()
                        page.wait_for_load_state('networkidle')
                        break
                except:
                    continue
            
            page.wait_for_timeout(2000)
            page.screenshot(path='./e2e/screenshots/kundli_page.png')
            
            # Look for any delete button
            print('\nLooking for delete buttons...')
            delete_selectors = [
                'button svg[data-lucide="trash-2"]',
                'button:has-text("Delete")',
                '[title="Delete"]',
                'button svg[name="trash"]',
                'button:has(svg)'
            ]
            
            for selector in delete_selectors:
                elements = page.locator(selector).all()
                print(f'{selector}: {len(elements)} found')
                if elements:
                    for i, el in enumerate(elements[:3]):
                        print(f'  {i}: {el.text_content()[:50] if el.text_content() else "no text"}')
            
            # Check if there's a "Delete All" button
            delete_all = page.locator('text=Delete All').first
            if delete_all.is_visible():
                print('\nFound Delete All button!')
                
                # Set up dialog handler
                page.on('dialog', lambda dialog: (print(f'Dialog: {dialog.message}'), dialog.accept()))
                
                # Click delete all
                delete_all.click()
                page.wait_for_timeout(3000)
                
                # Check for error
                error = page.locator('text=Failed to delete').first
                if error.is_visible():
                    print(f'Error shown: {error.text_content()}')
            
            # Print network logs
            print('\n=== Network Logs ===')
            for log in network_logs[-20:]:  # Last 20
                print(f"{log['type'].upper()}: {log['method']} {log['url'][:80]}...")
                if 'status' in log:
                    print(f"  Status: {log['status']}")
                if 'error' in log:
                    print(f"  Error: {log['error']}")
            
            # Print console errors
            if console_errors:
                print('\n=== Console Errors ===')
                for err in console_errors:
                    print(err)
            
            # Try making a delete request manually from browser
            print('\n=== Testing DELETE from browser console ===')
            result = page.evaluate('''async () => {
                const token = localStorage.getItem("astrovedic_token");
                if (!token) return { error: "No token" };
                
                try {
                    const response = await fetch(
                        "https://astro-rattan-api.onrender.com/api/kundli/test-id",
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
                        headers: Object.fromEntries(response.headers.entries())
                    };
                } catch (e) {
                    return { error: e.message, type: e.name };
                }
            }''')
            print(f'Browser fetch result: {json.dumps(result, indent=2)}')
            
        finally:
            page.screenshot(path='./e2e/screenshots/final_state.png')
            context.close()
            browser.close()

if __name__ == '__main__':
    test_delete_network()
