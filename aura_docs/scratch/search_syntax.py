with open(r"C:\Users\nishu\workspace\wscs_bedrock\aura_docs\frontend\src\components\InteractiveComponents.jsx", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        if "Syntax" in line or "activeTab" in line or "Tab" in line:
            print(f"Line {i}: {line.strip()}")
