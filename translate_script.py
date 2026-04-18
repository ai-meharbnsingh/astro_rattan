import os
import sys
import pprint

# Make sure we can import from app
sys.path.insert(0, os.path.abspath('.'))

from app.reports.interpretations import (
    DASHA_INTERPRETATIONS,
    ANTARDASHA_INTERPRETATIONS,
    MANGALA_DOSHA_TEXT,
    LIFE_PREDICTIONS
)
from deep_translator import GoogleTranslator
translator = GoogleTranslator(source='en', target='hi')

def bulk_translate(texts):
    if not texts: return []
    # Deep translator handles strings one by one effectively, or we can just loop
    # Let's just loop
    res = []
    for t in texts:
        try:
            res.append(translator.translate(t))
        except Exception as e:
            res.append(t)  # fallback
    return res

def process_dict(d):
    if isinstance(d, dict):
        new_d = {}
        for k, v in d.items():
            if isinstance(k, tuple):
                # keep tuple keys
                new_d[k] = process_dict(v)
            else:
                new_d[k] = process_dict(v)
        return new_d
    elif isinstance(d, list):
        if len(d) > 0 and isinstance(d[0], str):
            # Translate strings
            hi_strings = bulk_translate(d)
            # We must map each string to bilingual if expected
            # Wait, if it's a list of strings, the frontend expects a list of bilingual dicts?
            # Or in some places it expects just a list of strings.
            # If we wrap it: [{"en": x, "hi": y}, ...]
            return [{"en": en_s, "hi": hi_s} for en_s, hi_s in zip(d, hi_strings)]
        else:
            return [process_dict(x) for x in d]
    elif isinstance(d, str):
        hi_str = ""
        try:
            hi_str = translator.translate(d)
        except:
            hi_str = d
        return {"en": d, "hi": hi_str}
    else:
        return d

print("Processing DASHA...")
NEW_DASHA = process_dict(DASHA_INTERPRETATIONS)
print("Processing ANTARDASHA...")
NEW_ANTARDASHA = process_dict(ANTARDASHA_INTERPRETATIONS)
print("Processing MANGALA_DOSHA...")
# For MANGALA_DOSHA we only want to process certain keys to avoid breaking structure
NEW_MANGALA = process_dict(MANGALA_DOSHA_TEXT)
print("Processing LIFE...")
NEW_LIFE = process_dict(LIFE_PREDICTIONS)

# Generate Python code
code = f"""
from typing import Dict, Any, Tuple

DASHA_INTERPRETATIONS: Dict[str, Dict[str, Any]] = {pprint.pformat(NEW_DASHA, sort_dicts=False)}

ANTARDASHA_INTERPRETATIONS: Dict[Tuple[str, str], Any] = {pprint.pformat(NEW_ANTARDASHA, sort_dicts=False)}

MANGALA_DOSHA_TEXT: Dict[str, Any] = {pprint.pformat(NEW_MANGALA, sort_dicts=False)}

LIFE_PREDICTIONS: Dict[str, Dict[str, Any]] = {pprint.pformat(NEW_LIFE, sort_dicts=False)}
"""

with open("translated_blocks.py", "w") as f:
    f.write(code)

print("Done. Wrote to translated_blocks.py")
