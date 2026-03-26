# AstroVedic UI Test Suite

Comprehensive browser-based UI testing using Playwright.

## 🎯 What These Tests Do

These tests **ACTUALLY OPEN A BROWSER** and:
- Navigate to each page of your website
- Click buttons and fill forms
- Take screenshots for visual verification
- Verify all UI elements are visible and working

## 📁 Test Files

| File | Tests | Coverage |
|------|-------|----------|
| `e2e/test_ui_visual.py` | **27 tests** | All frontend pages with visual verification |
| `e2e/test_frontend_smoke.py` | **5 tests** | Critical flows (blog, palmistry, admin, astrologer, profile) |
| `e2e/test_astrovedic_e2e.py` | **36 tests** | API-level E2E tests |
| `tests/test_mobile_responsive.py` | **22 tests** | Responsive design verification |

## 🚀 Running the Tests

### Prerequisites
Make sure both servers are running:

```bash
# Terminal 1: Start Backend
cd /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app
python -m app.main

# Terminal 2: Start Frontend
cd /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app/frontend
npm run dev
```

### Run All UI Tests (with visible browser)

```bash
cd /Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app
./run_ui_tests.sh
```

Or manually:

```bash
# Run all UI tests with visible browser
python3 -m pytest e2e/test_ui_visual.py -v --headed --slowmo=300

# Run specific test class
python3 -m pytest e2e/test_ui_visual.py::TestHomePage -v --headed --slowmo=300

# Run specific test
python3 -m pytest e2e/test_ui_visual.py::TestAuthUI::test_login_page_loads -v --headed --slowmo=300

# Run in headless mode (faster, no visible browser)
python3 -m pytest e2e/test_ui_visual.py -v
```

## 📸 Screenshots

Screenshots are saved to `screenshots/ui_tests/` with timestamps:
- `01_homepage_complete_1234567890.png`
- `04_login_page_1234567890.png`
- `09_kundli_form_1234567890.png`
- etc.

## 🧪 Test Coverage

### TestHomePage (3 tests)
- ✅ Homepage loads completely
- ✅ Navigation menu items visible
- ✅ Hero CTA buttons work

### TestAuthUI (3 tests)
- ✅ Login page loads with form
- ✅ Register new user through UI
- ✅ Login with credentials

### TestKundliUI (3 tests)
- ✅ Kundli form page loads
- ✅ Generate kundli through UI
- ✅ Report purchase buttons visible

### TestHoroscopeUI (2 tests)
- ✅ Horoscope page loads with zodiac signs
- ✅ Select zodiac sign displays reading

### TestPanchangUI (1 test)
- ✅ Panchang page loads with daily data

### TestLibraryUI (2 tests)
- ✅ Library page loads with tabs
- ✅ Gita chapters display

### TestShopUI (2 tests)
- ✅ Shop page loads with products
- ✅ Category filters work

### TestDivinationUI (2 tests)
- ✅ Numerology calculator works
- ✅ Prashnavali page loads

### TestAIChatUI (1 test)
- ✅ AI chat interface works

### TestReportsUI (1 test)
- ✅ Reports marketplace loads with pricing

### TestPalmistryUI (2 tests)
- ✅ Palmistry page loads
- ✅ Guide tab displays

### TestProfileUI (1 test)
- ✅ User profile page loads

### TestConsultationUI (1 test)
- ✅ Consultation page loads

### TestNavigationFlow (1 test)
- ✅ All nav links work correctly

### TestMobileResponsive (2 tests)
- ✅ Homepage on mobile viewport
- ✅ Kundli form on mobile

## 🔧 Configuration

Set environment variables to customize:

```bash
export FRONTEND_URL=http://localhost:5173  # Your frontend URL
export API_URL=http://localhost:8028        # Your backend URL
```

## 📊 Test Results

When tests complete, you'll see:
```
========================= 27 passed in 180.50s =========================
```

Screenshots will be in `screenshots/ui_tests/` for visual verification.

## 🐛 Troubleshooting

### Tests failing to start
- Make sure both frontend and backend servers are running
- Check that ports 5173 (frontend) and 8028 (backend) are available

### Browser not visible
- Add `--headed` flag to see the browser
- Remove `--headed` for headless (faster) execution

### Screenshots not saving
- Check that `screenshots/ui_tests/` directory exists and is writable
- Check the test output for error messages

### Tests timing out
- Increase `--slowmo` value (in milliseconds) to slow down execution
- Check if the frontend/backend are responding slowly

## 📝 Example Output

```
e2e/test_ui_visual.py::TestHomePage::test_homepage_loads_completely 
🌐 Navigating to http://localhost:5173
✓ Checking logo...
✓ Checking hero section...
✓ Checking CTA buttons...
✓ Checking navigation...
✓ Checking footer...
📸 Screenshot saved: screenshots/ui_tests/01_homepage_complete_1234567890.png
✅ Homepage loaded successfully!
PASSED
```

## 🎥 Video Recording

To record videos of tests, modify the browser launch in `conftest.py`:

```python
context = browser.new_context(
    viewport={"width": 1400, "height": 900},
    record_video_dir="screenshots/ui_tests/videos"
)
```
