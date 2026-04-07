"""Test 30-03 design"""
from playwright.sync_api import sync_playwright

def test_design():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 4000})
        
        print("🌐 Loading 30-03 design...")
        page.goto('https://mushroomkimandi.in', timeout=60000)
        page.wait_for_timeout(5000)
        
        page.screenshot(path='/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/e2e/screenshots/design_30_03.png', full_page=True)
        print("✅ Screenshot saved!")
        
        browser.close()

if __name__ == '__main__':
    test_design()
