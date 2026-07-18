import re

pb_path = "C:/Users/nishu/.gemini/antigravity/conversations/ac51f2df-f9cd-48af-a743-df4a1e12cf07.pb"

with open(pb_path, "rb") as f:
    data = f.read()

# Let's decode the entire file using utf-8 with 'ignore' or 'replace'
text = data.decode("utf-8", errors="ignore")

# Find all occurrences of "# Python for AI Agents"
matches = [m.start() for m in re.finditer("# Python for AI Agents", text)]

print(f"Matches found: {len(matches)}")
for idx, m_start in enumerate(matches):
    print(f"Match {idx} at index {m_start}")
    # Print the first 200 chars of the match
    print(repr(text[m_start:m_start+200]))
    
    # Save the full block of text starting here
    # A typical model response containing the full section is around 80,000 characters
    block = text[m_start:m_start+100000]
    
    # Let's find where the block ends. In our markdown, the last section is "26. Package Structure"
    # or "ep12_semantic_memory.py". Let's search for "ep12_semantic_memory.py" in this block.
    end_marker = "ep12_semantic_memory.py"
    end_idx = block.find(end_marker)
    if end_idx != -1:
        # Include some characters after the end marker
        full_text = block[:end_idx + len(end_marker) + 500]
        with open(f"C:/Users/nishu/workspace/wscs_bedrock/aura_docs/scratch/recovered_{idx}.md", "w", encoding="utf-8") as out:
            out.write(full_text)
        print(f"Saved recovered_{idx}.md of length {len(full_text)}")
