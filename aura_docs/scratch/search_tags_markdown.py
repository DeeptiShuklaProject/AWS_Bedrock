with open(r"C:\Users\nishu\workspace\wscs_bedrock\doc_replica_product_developer\doc_replica_fullstackdeveloper\backend\languages\python.md", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        if "SyntaxTabs" in line or "<Tabs" in line or "<Tab" in line:
            print(f"Line {i}: {line.strip()}")
