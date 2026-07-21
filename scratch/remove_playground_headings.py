import os
import glob
import re

bedrock_dir = r"c:\Users\nishu\workspace\wscs_bedrock\doc_uday_bedrock_notes"

chapter_files = glob.glob(os.path.join(bedrock_dir, "Chapter_*.md"))
print(f"Found {len(chapter_files)} chapter files to process...")

for filepath in sorted(chapter_files):
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove heading lines matching '### Hands-on Code Playground...' or '### Interactive Python Playground...'
    content = re.sub(r'###\s+Hands-on\s+Code\s+Playground\s+#\d+\s*\n*', '', content)
    content = re.sub(r'###\s+Interactive\s+Python\s+Playground\s*\n*', '', content)

    # Clean up any triply-repeated blank lines
    content = re.sub(r'\n{4,}', '\n\n', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Cleaned playground heading lines from {filename}")

print("Removal complete! Playground headings removed while preserving all interactive playground components and quizzes.")
