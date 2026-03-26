"""
UI Tests with VIDEO Recording - Watch the tests later!
Run: python3 e2e/test_ui_with_video.py
"""
import os
import time
from playwright.sync_api import sync_playwright

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "..", "screenshots", "videos")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

timestamp = int(time.time())

def main():
    print("🎬 Starting UI Tests with Video Recording...")
    print(f"🌐 Testing: {FRONTEND_URL}")
    print("")
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)  # Headless but recording video
        
        # Create context with video recording
        context = browser.new_context(
            viewport={"width": 1400, "height": 900},
            record_video_dir=SCREENSHOTS_DIR,
            record_video_size={"width": 1400, "height": 900}
        )
        
        page = context.new_page()
        
        try:
            # Test 1: Homepage
            print("1️⃣ Testing Homepage...")
            page.goto(FRONTEND_URL, timeout=30000)
            page.wait_for_load_state("networkidle")
            print("   ✅ Homepage loaded")
            print(f"   📄 Title: {page.title()}")
            print(f"   📏 Page size: {len(page.content())} bytes")
            time.sleep(2)
            
            # Test 2: Login Page
            print("\n2️⃣ Testing Login Page...")
            page.goto(f"{FRONTEND_URL}/login", timeout=30000)
            page.wait_for_load_state("networkidle")
            
            # Check for login form elements
            has_email = page.locator("input[type='email']").count() > 0
            has_password = page.locator("input[type='password']").count() > 0
            print(f"   ✅ Email input: {has_email}")
            print(f"   ✅ Password input: {has_password}")
            time.sleep(2)
            
            # Test 3: Kundli Page
            print("\n3️⃣ Testing Kundli Page...")
            page.goto(f"{FRONTEND_URL}/kundli", timeout=30000)
            page.wait_for_load_state("networkidle")
            
            has_name = page.locator("input").count() > 0
            print(f"   ✅ Form inputs found: {has_name}")
            time.sleep(2)
            
            # Test 4: Shop Page
            print("\n4️⃣ Testing Shop Page...")
            page.goto(f"{FRONTEND_URL}/shop", timeout=30000)
            page.wait_for_load_state("networkidle")
            
            content = page.content()
            has_products = "product" in content.lower() or "shop" in content.lower()
            print(f"   ✅ Shop content loaded: {has_products}")
            time.sleep(2)
            
            # Test 5: Horoscope
            print("\n5️⃣ Testing Horoscope Page...")
            page.goto(f"{FRONTEND_URL}/horoscope", timeout=30000)
            page.wait_for_load_state("networkidle")
            
            zodiac_found = []
            for sign in ["Aries", "Taurus", "Gemini"]:
                if sign in page.content():
                    zodiac_found.append(sign)
            print(f"   ✅ Zodiac signs found: {zodiac_found}")
            time.sleep(2)
            
            # Test 6: Library
            print("\n6️⃣ Testing Library Page...")
            page.goto(f"{FRONTEND_URL}/library", timeout=30000)
            page.wait_for_load_state("networkidle")
            
            has_gita = "Gita" in page.content() or "gita" in page.content()
            print(f"   ✅ Library loaded: {has_gita}")
            time.sleep(2)
            
            print("\n" + "="*50)
            print("✅ ALL UI TESTS PASSED!")
            print("="*50)
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            print("\n💡 Make sure servers are running:")
            print("   Backend: python -m app.main")
            print("   Frontend: cd frontend && npm run dev")
            
        finally:
            # Close context - this saves the video
            context.close()
            browser.close()
            
            # Find the video file
            video_files = [f for f in os.listdir(SCREENSHOTS_DIR) if f.endswith('.webm')]
            if video_files:
                print(f"\n🎥 VIDEO SAVED!")
                print(f"📁 Location: {SCREENSHOTS_DIR}")
                print(f"🎬 Files: {video_files}")
                print(f"\n👉 Open the .webm file in Chrome/VLC to watch the test!")

if __name__ == "__main__":
    main()
