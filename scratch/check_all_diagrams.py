import os
import re

notes_dir = r"c:\Users\nishu\workspace\wscs_bedrock\Uday_AWS_Services_notes"

files = sorted([f for f in os.listdir(notes_dir) if f.endswith('.md')])

mermaid_block_regex = re.compile(r"```mermaid\s*\n([\s\S]*?)```", re.IGNORECASE)

total_blocks = 0
all_blocks = []

for filename in files:
    filepath = os.path.join(notes_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    matches = list(mermaid_block_regex.finditer(content))
    for m in matches:
        total_blocks += 1
        block_text = m.group(1).strip()
        first_line = block_text.split('\n')[0] if block_text else ""
        # Get line number
        line_num = content[:m.start()].count('\n') + 1
        all_blocks.append({
            'file': filename,
            'line': line_num,
            'first_line': first_line,
            'text': block_text
        })

print(f"Found {total_blocks} mermaid blocks across {len(files)} files.\n")
for idx, b in enumerate(all_blocks, 1):
    print(f"[{idx}] {b['file']}:L{b['line']} -> {b['first_line']}")
