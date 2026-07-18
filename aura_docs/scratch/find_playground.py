import re

with open(r"C:\Users\nishu\workspace\wscs_bedrock\doc_replica_product_developer\doc_replica_fullstackdeveloper\backend\languages\python.md", "r", encoding="utf-8") as f:
    content = f.read()

for line in content.split('\n'):
    if 'InteractivePlayground' in line or 'InteractiveExample' in line:
        print(line)
