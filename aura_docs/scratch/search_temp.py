import os

temp_dir = "C:/Users/nishu/AppData/Local/Temp"

if os.path.exists(temp_dir):
    print("Searching Temp directory...")
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Check files that are reasonably sized and modified recently
                size = os.path.getsize(file_path)
                if 50000 <= size <= 200000:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if "# Python for AI Agents" in content:
                            print(f"FOUND in Temp: {file_path} (size: {size})")
            except Exception:
                pass
else:
    print("Temp directory does not exist!")
