import json
import os
import ast
from pathlib import Path

# Provide API key directly
API_KEY = "AIzaSyDVSB9yerOZ2Vyf4A76GUje09BzZKSYeoI"

print("Checking generativeai...", end="")
try:
    import google.generativeai as genai
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash") # Use 1.5-flash or 2.0-flash
    response = model.generate_content("Translate 'Hello World' to Hindi. Only return the translated text.")
    print("Success. Translation:", response.text.strip())
except Exception as e:
    print("Failed to use Gemini API:", e)

