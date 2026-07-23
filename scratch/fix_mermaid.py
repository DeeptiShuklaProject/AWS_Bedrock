import os
import re

notes_dir = r"c:\Users\nishu\workspace\wscs_bedrock\Uday_AWS_Services_notes"

for filename in os.listdir(notes_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(notes_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Clean up core labels like "04 Amazon API Gateway" -> "Amazon API Gateway"
        cleaned_content = re.sub(r'core\["\d+[\s_]+([^"]+)"\]', r'core["\1"]', content)
        if cleaned_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(cleaned_content)
            print(f"Cleaned {filename}")
