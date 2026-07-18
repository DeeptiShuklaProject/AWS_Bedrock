import re

with open(r"C:\Users\nishu\workspace\wscs_bedrock\doc_replica_product_developer\doc_replica_fullstackdeveloper\backend\languages\python.md", "r", encoding="utf-8") as f:
    content = f.read()

matches = re.findall(r"<InterviewQuestion[^>]*>", content)
for m in matches:
    print(m)
