import os
import re

notes_dir = r"c:\Users\nishu\workspace\wscs_bedrock\Uday_AWS_Services_notes"
files = sorted([f for f in os.listdir(notes_dir) if f.endswith('.md')])
mermaid_block_regex = re.compile(r"```mermaid\s*\n([\s\S]*?)```", re.IGNORECASE)

for filename in files:
    filepath = os.path.join(notes_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    matches = list(mermaid_block_regex.finditer(content))
    if matches:
        print(f"=== {filename} ({len(matches)} diagrams) ===")
        for idx, m in enumerate(matches, 1):
            line_num = content[:m.start()].count('\n') + 1
            print(f"--- Diagram {idx} (Line {line_num}) ---")
            print(m.group(1).strip())
            print()
