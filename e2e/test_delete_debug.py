"""Debug test for delete kundli functionality"""
import pytest
from playwright.sync_api import sync_playwright, expect


def test_delete_kundli_debug():
    """Debug the delete kundli API issue"""
    
    with sync_playwright() as p:
        # Launch browser with devtools to see network
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            record_video_dir='./e2e/videos/'
        )
        
        # Enable console and network logging
        page = context.new_page()
        
        # Listen to console logs
        page.on('console', lambda msg: print(f'[CONSOLE {msg.type}]: {msg.text}'))
        
        # Listen to network requests
        def handle_route(route, request):
            print(f'[NETWORK] {request.method} {request.url}')
            route.continue_()
        
        # Listen to network responses
        page.on('response', lambda response: 
            print(f'[RESPONSE] {response.status} {response.request.method} {response.url}') 
            if 'api' in response.url else None
        )
        
        page.on('requestfailed', lambda request: 
            print(f'[REQUEST FAILED] {request.method} {request.url} - {request.failure}')
        )
        
        try:
            # Go to the app
            print('\n=== Opening app ===')
            page.goto('https://astrovedic-web.vercel.app', timeout=60000)
            page.wait_for_load_state('networkidle')
            
            # Take screenshot of homepage
            page.screenshot(path='./e2e/screenshots/01_homepage.png')
            print('Screenshot: homepage saved')
            
            # Check if we need to login
            print('\n=== Checking auth state ===')
            
            # Look for login button or my kundlis link
            login_btn = page.locator('text=Login').first
            my_kundlis_link = page.locator('text=My Kundlis').first
            
            if my_kundlis_link.is_visible():
                print('Found My Kundlis link - clicking')
                my_kundlis_link.click()
                page.wait_for_load_state('networkidle')
            elif login_btn.is_visible():
                print('Need to login first')
                login_btn.click()
                
                # Fill login form
                page.locator('input[type="email"]').fill('test@example.com')
                page.locator('input[type="password"]').fill('test123')
                page.locator('button:has-text("Login")').click()
                
                page.wait_for_load_state('networkidle')
                page.wait_for_timeout(2000)
            
            page.screenshot(path='./e2e/screenshots/02_after_login.png')
            
            # Now navigate to kundli list
            print('\n=== Navigating to Kundli List ===')
            
            # Look for kundli list or try to find saved kundlis
            kundli_section = page.locator('text=My Kundlis, text=Saved Kundlis, text=Your Kundlis').first
            
            if kundli_section.is_visible():
                kundli_section.click()
                page.wait_for_load_state('networkidle')
            
            page.screenshot(path='./e2e/screenshots/03_kundli_list.png')
            
            # Look for delete buttons
            print('\n=== Looking for delete buttons ===')
            
            delete_buttons = page.locator('button:has([name="trash"]), button:has-text("Delete"), [title="Delete"]').all()
            print(f'Found {len(delete_buttons)} delete buttons')
            
            if len(delete_buttons) > 0:
                print('Clicking first delete button...')
                
                # Set up dialog handler for confirm
                page.on('dialog', lambda dialog: 
                    (print(f'[DIALOG] {dialog.type}: {dialog.message}'), dialog.accept())
                )
                
                # Click delete
                delete_buttons[0].click()
                
                # Wait a bit for the request
                page.wait_for_timeout(3000)
                
                page.screenshot(path='./e2e/screenshots/04_after_delete_click.png')
                
                # Check for alert/error
                alert_text = page.locator('text=Failed to delete').first
                if alert_text.is_visible():
                    print(f'ERROR VISIBLE: {alert_text.text_content()}')
            else:
                print('No delete buttons found - checking if any kundlis exist')
                
                # Check for "No saved kundlis" message
                no_kundlis = page.locator('text=No saved kundlis').first
                if no_kundlis.is_visible():
                    print('No kundlis found - need to create one first')
                    
                    # Try to create a test kundli
                    new_kundli_btn = page.locator('text=Generate New Kundli').first
                    if new_kundli_btn.is_visible():
                        new_kundli_btn.click()
                        page.wait_for_load_state('networkidle')
                        
                        # Fill form
                        page.locator('input[name="name"], input[placeholder*="name"]').fill('Test Person')
                        page.locator('input[name="date"], input[type="date"]').fill('1990-01-01')
                        page.locator('input[name="time"], input[type="time"]').fill('12:00')
                        page.locator('input[name="place"], input[placeholder*="place"]').fill('Delhi, India')
                        
                        # Submit
                        page.locator('button:has-text("Generate"), button:has-text("Submit")').click()
                        page.wait_for_load_state('networkidle')
                        page.wait_for_timeout(3000)
                        
                        page.screenshot(path='./e2e/screenshots/05_after_create.png')
                        
                        # Now go back to list
                        page.goto('https://astrovedic-web.vercel.app/kundli/list')
                        page.wait_for_load_state('networkidle')
                        
                        # Look for delete button again
                        delete_buttons = page.locator('button:has([name="trash"]), button:has-text("Delete"), [title="Delete"]').all()
                        print(f'After creating, found {len(delete_buttons)} delete buttons')
            
            # Get all console logs
            print('\n=== All Console Logs ===')
            logs = page.evaluate('() => window.console_logs || []')
            print(logs)
            
        except Exception as e:
            print(f'ERROR: {e}')
            page.screenshot(path='./e2e/screenshots/error.png')
            raise
        finally:
            page.screenshot(path='./e2e/screenshots/final.png')
            context.close()
            browser.close()


def test_api_directly():
    """Test the delete API directly to see the error"""
    import requests
    
    base_url = 'https://astro-rattan-api.onrender.com'
    frontend_url = 'https://astrovedic-web.vercel.app'
    
    print('\n=== Testing CORS preflight ===')
    
    # Test OPTIONS request
    response = requests.options(
        f'{base_url}/api/kundli/test-id',
        headers={
            'Origin': frontend_url,
            'Access-Control-Request-Method': 'DELETE',
            'Access-Control-Request-Headers': 'Authorization,Content-Type'
        }
    )
    print(f'OPTIONS Status: {response.status_code}')
    print(f'CORS Headers: {dict(response.headers)}')
    
    print('\n=== Testing DELETE with invalid token ===')
    
    # Test DELETE request
    response = requests.delete(
        f'{base_url}/api/kundli/test-id',
        headers={
            'Origin': frontend_url,
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
    )
    print(f'DELETE Status: {response.status_code}')
    print(f'Response: {response.text}')
    
    print('\n=== Testing DELETE /user/all ===')
    
    response = requests.delete(
        f'{base_url}/api/kundli/user/all',
        headers={
            'Origin': frontend_url,
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
    )
    print(f'DELETE /user/all Status: {response.status_code}')
    print(f'Response: {response.text}')


if __name__ == '__main__':
    print('Running API tests...')
    test_api_directly()
    
    print('\n\nRunning UI tests...')
    test_delete_kundli_debug()
