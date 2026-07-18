with open(r"C:\Users\nishu\workspace\wscs_bedrock\aura_docs\frontend\src\components\DocReader.jsx", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        if "execute" in line or "/api" in line:
            print(f"Line {i}: {line.strip()}")
