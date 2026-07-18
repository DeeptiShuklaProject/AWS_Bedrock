import json

with open("C:/Users/nishu/workspace/wscs_bedrock/aura_docs/scratch/extracted_content.json", "r", encoding="utf-8") as f:
    args = json.load(f)

path = "C:/Users/nishu/workspace/wscs_bedrock/doc_replica_product_developer/doc_replica_fullstackdeveloper/backend/languages/python.md"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

target = args["TargetContent"]
replacement = args["ReplacementContent"]

# If it starts with quote and ends with quote, parse as JSON string
if target.startswith('"') and target.endswith('"'):
    target = json.loads(target)
else:
    # It might still be JSON serialized if it has escaped characters
    try:
        target = json.loads('"' + target + '"')
    except Exception:
        pass

if replacement.startswith('"') and replacement.endswith('"'):
    replacement = json.loads(replacement)
else:
    try:
        replacement = json.loads('"' + replacement + '"')
    except Exception:
        pass

# Normalize newlines
target = target.replace("\r\n", "\n")
replacement = replacement.replace("\r\n", "\n")
content = content.replace("\r\n", "\n")

if target in content:
    new_content = content.replace(target, replacement)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_content)
    print("Successfully restored the appended section to python.md!")
else:
    print("Error: TargetContent not found in python.md!")
    print("TargetContent:", repr(target))
    # Let's print the last 200 chars of content
    print("Last 200 chars of python.md:", repr(content[-200:]))
