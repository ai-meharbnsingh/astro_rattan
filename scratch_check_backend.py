import ast
import os
import glob

def check_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            # Check dictionary keys for bilingual pairs
            if isinstance(node, ast.Dict):
                keys = []
                for k in node.keys:
                    if isinstance(k, ast.Constant) and isinstance(k.value, str):
                        keys.append(k.value)
                
                # Check 1: Missing EN/HI counterparts
                if "en" in keys and "hi" not in keys:
                    issues.append(f"Line {node.lineno}: Dictionary has 'en' key but missing 'hi'")
                if "hi" in keys and "en" not in keys:
                    issues.append(f"Line {node.lineno}: Dictionary has 'hi' key but missing 'en'")
                
                # Check 2: Strings in typical text fields meant for UI
                text_keys = {'title', 'name', 'reason', 'description', 'message', 'note', 'guidance', 'text', 'warning', 'symptoms', 'alert'}
                for k, v in zip(node.keys, node.values):
                    if isinstance(k, ast.Constant) and isinstance(k.value, str):
                        if k.value in text_keys:
                            if isinstance(v, ast.Constant) and isinstance(v.value, str):
                                # It's a bare string instead of a dictionary.
                                # Check if the bare string contains alphabets and is not a known enum.
                                val = v.value.strip()
                                # Ignore small keys / enums (e.g. "active", "trial_remedy")
                                if val and len(val) > 10 and any(c.isalpha() for c in val):
                                    issues.append(f"Line {node.lineno}: Key '{k.value}' has a hardcoded string ('{val[:30]}...') instead of a bilingual dictionary.")

            # Check 3: Simple assignments or returns of text strings in certain functions
            # Too complex with AST, sticking to dict checks which is where 99% of LK payloads are defined.

    except SyntaxError:
        pass
    except Exception as e:
        print(f"Error parsing {path}: {e}")
        pass
        
    return issues

print("Backend Hardcoded English Scan Report\n" + "="*40)
for f in glob.glob("app/**/*.py", recursive=True):
    res = check_file(f)
    if res:
        print(f"\n📁 File: {f}")
        for r in res:
            print(f"  - {r}")
