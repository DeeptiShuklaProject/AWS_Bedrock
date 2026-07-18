import re

with open("C:/Users/nishu/workspace/wscs_bedrock/doc_replica_product_developer/doc_replica_fullstackdeveloper/backend/languages/python.md", "r", encoding="utf-8") as f:
    content = f.read()

parts = content.split("# Python for AI Agents (Beginner to Advanced)")
header = parts[0]
ai_section = parts[1]

# Split into subsections
subsections = re.split(r'\n(###\s+[^\n]+)', ai_section)
print(f"Total parts: {len(subsections)}")

for i in range(1, len(subsections), 2):
    title = subsections[i].strip()
    body = subsections[i+1] if i+1 < len(subsections) else ""
    headers = re.findall(r'####\s+(\d+\.\s+[^\n]+)', body)
    print(f"{title}: {headers}")
