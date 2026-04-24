from app.astro_engine import calculate_planet_positions
import sys

# Mock swisseph missing by removing it from sys.modules if it exists
if 'swisseph' in sys.modules:
    del sys.modules['swisseph']

try:
    res = calculate_planet_positions("2023-10-27", "12:00", 20.59, 78.96, 5.5)
    print("Success")
except Exception as e:
    print(f"Error: {e}")
