import os

src_dir = r"C:\Users\nishu\workspace\wscs_bedrock\aura_docs\frontend\src"

for root, dirs, files in os.walk(src_dir):
    for f in files:
        if f.endswith(('.js', '.jsx', '.ts', '.tsx')):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if 'Interactive Playground' in content:
                        print(f"Found in {path}")
                        # Print some lines around it
                        lines = content.split('\n')
                        for idx, l in enumerate(lines):
                            if 'Interactive Playground' in l:
                                start = max(0, idx - 10)
                                end = min(len(lines), idx + 10)
                                print(f"--- lines {start} to {end} in {f} ---")
                                for i in range(start, end):
                                    print(f"{i}: {lines[i]}")
            except Exception as e:
                print(e)
