import os
import re

frontend_dir = r"C:\Users\nishu\workspace\wscs_bedrock\aura_docs\frontend"

for root, dirs, files in os.walk(frontend_dir):
    for f in files:
        if f.endswith(('.js', '.jsx', '.ts', '.tsx')):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if 'execute' in content:
                        print(f"Found in {path}")
            except Exception:
                pass
