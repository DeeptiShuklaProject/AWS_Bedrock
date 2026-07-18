import os
import time

history_path = "C:/Users/nishu/AppData/Roaming/Code/User/History"

if not os.path.exists(history_path):
    print("VS Code History path does not exist!")
else:
    print("Searching files modified in the last 2 hours...")
    now = time.time()
    two_hours_ago = now - 2 * 3600
    
    found_files = []
    for root, dirs, files in os.walk(history_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                mtime = os.path.getmtime(file_path)
                if mtime >= two_hours_ago:
                    size = os.path.getsize(file_path)
                    print(f"File: {file_path} (size: {size} bytes, mtime: {time.ctime(mtime)})")
                    # Read first line or check if it contains python/md content
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read(500)
                        print("  Snippet:", repr(content[:150]))
            except Exception as e:
                pass
