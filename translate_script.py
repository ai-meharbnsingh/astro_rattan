import re
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Use my own provided key if not found
    api_key = "AIzaSyDVSB9yerOZ2Vyf4A76GUje09BzZKSYeoI"
genai.configure(api_key=api_key)

print("Testing Gemini API...")
try:
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content("Translate 'Hello World' to Hindi.")
    print("Response:", response.text)
except Exception as e:
    print("Failed to use Gemini API:", e)
