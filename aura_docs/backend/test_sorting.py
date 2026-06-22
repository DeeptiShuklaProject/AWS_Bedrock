import os
import json
import shutil
import tempfile
import sys

# Set tempdir inside the workspace to ensure sandbox compatibility
tempfile.tempdir = os.path.dirname(os.path.abspath(__file__))

import app

def test_sorting():
    with tempfile.TemporaryDirectory(dir=tempfile.tempdir) as temp_dir:
        # Create some files
        files = ["Welcome.md", "02_Architecture.md", "About.md", "Z_Last.md"]
        for f in files:
            with open(os.path.join(temp_dir, f), "w") as fp:
                fp.write("dummy")
                
        # 1. Test current behavior (without order.json) -> should sort alphabetically
        nav = app.build_nav_from_fs(temp_dir, temp_dir)
        titles = [item["title"] for item in nav]
        print("Default behavior:", titles)
        assert titles == ["Architecture", "About", "Welcome", "Z Last"], f"Expected Architecture, About, Welcome, Z Last but got {titles}"
        
        # 2. Test with order.json using raw file names
        order_raw = ["Welcome.md", "02_Architecture.md"]
        with open(os.path.join(temp_dir, "order.json"), "w") as fp:
            json.dump(order_raw, fp)
            
        nav = app.build_nav_from_fs(temp_dir, temp_dir)
        titles = [item["title"] for item in nav]
        print("With order.json (raw filenames):", titles)
        assert titles == ["Welcome", "Architecture", "About", "Z Last"], f"Expected Welcome, Architecture, About, Z Last but got {titles}"
        
        # 3. Test with order.json using clean title/names (e.g. "Architecture", "Welcome")
        order_clean = ["Welcome", "Architecture"]
        with open(os.path.join(temp_dir, "order.json"), "w") as fp:
            json.dump(order_clean, fp)
            
        nav = app.build_nav_from_fs(temp_dir, temp_dir)
        titles = [item["title"] for item in nav]
        print("With order.json (clean titles/names without 02_ prefix):", titles)
        assert titles == ["Welcome", "Architecture", "About", "Z Last"], f"Expected Welcome, Architecture, About, Z Last but got {titles}"

        # 4. Test case insensitivity (e.g. "architecture", "welcome")
        order_case = ["welcome", "architecture"]
        with open(os.path.join(temp_dir, "order.json"), "w") as fp:
            json.dump(order_case, fp)
            
        nav = app.build_nav_from_fs(temp_dir, temp_dir)
        titles = [item["title"] for item in nav]
        print("With order.json (case-insensitive):", titles)
        assert titles == ["Welcome", "Architecture", "About", "Z Last"], f"Expected Welcome, Architecture, About, Z Last but got {titles}"

    print("ALL TESTS PASSED!")

if __name__ == "__main__":
    test_sorting()
