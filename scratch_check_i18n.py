import ast
import os
import glob

def check_file(path):
    with open(path, 'r') as f:
        content = f.read()
    
    issues = []
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            # Check dictionary keys
            if isinstance(node, ast.Dict):
                keys = []
                has_en_hi = False
                for k in node.keys:
                    if isinstance(k, ast.Constant) and isinstance(k.value, str):
                        keys.append(k.value)
                if "en" in keys and "hi" not in keys:
                    issues.append(f"Line {node.lineno}: found 'en' key without 'hi'")
                if "hi" in keys and "en" not in keys:
                    issues.append(f"Line {node.lineno}: found 'hi' key without 'en'")
                
                # Check for bare strings in common text keys
                text_keys = {'title', 'name', 'reason', 'description', 'message', 'note', 'guidance', 'text', 'warning'}
                for k, v in zip(node.keys, node.values):
                    if isinstance(k, ast.Constant) and isinstance(k.value, str):
                        if k.value in text_keys:
                            if isinstance(v, ast.Constant) and isinstance(v.value, str):
                                issues.append(f"Line {node.lineno}: key '{k.value}' has a bare string instead of bilingual dict")
    except SyntaxError:
        pass
    return issues

for f in glob.glob("app/lalkitab_*.py"):
    res = check_file(f)
    if res:
        print(f"--- {f} ---")
        for r in res:
            print(r)
