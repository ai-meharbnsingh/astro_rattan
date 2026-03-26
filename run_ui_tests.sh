#!/bin/bash
# AstroVedic UI Test Runner
# This script runs the visual UI tests with a visible browser

echo "=================================="
echo "AstroVedic UI Visual Test Runner"
echo "=================================="
echo ""
echo "Make sure your servers are running:"
echo "  1. Backend: python -m app.main"
echo "  2. Frontend: cd frontend && npm run dev"
echo ""
echo "Press Ctrl+C to cancel, or wait 3 seconds to continue..."
sleep 3

# Create screenshots directory
mkdir -p screenshots/ui_tests

# Run the UI tests
echo ""
echo "Running UI tests with visible browser..."
echo ""

python3 -m pytest e2e/test_ui_visual.py -v \
    --headed \
    --slowmo=300 \
    -k "$1" 2>&1 | tee ui_test_output.log

echo ""
echo "=================================="
echo "UI Tests Complete!"
echo "=================================="
echo "Screenshots saved to: screenshots/ui_tests/"
echo "Test output saved to: ui_test_output.log"
