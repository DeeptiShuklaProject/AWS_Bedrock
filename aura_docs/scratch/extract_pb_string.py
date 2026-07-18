import re

pb_path = "C:/Users/nishu/.gemini/antigravity/conversations/ac51f2df-f9cd-48af-a743-df4a1e12cf07.pb"

with open(pb_path, "rb") as f:
    data = f.read()

# Look for "# Python for AI Agents (Beginner to Advanced)" in the bytes
search_str = b"# Python for AI Agents (Beginner to Advanced)"
start_idx = data.find(search_str)

if start_idx != -1:
    print(f"Found search string at index {start_idx}")
    # Let's extract a large chunk of bytes from start_idx
    # We know the size of the section is around 51,000 bytes (from the 51160 bytes truncation message)
    # Let's read 100,000 bytes and then search for the end of the text.
    chunk = data[start_idx:start_idx + 100000]
    
    # Protobuf encodes strings with their length preceding them.
    # The string will run until we hit binary control characters or protobuf tags.
    # Let's decode as much valid UTF-8 as possible.
    # We can try to decode characters one by one.
    text_chars = []
    for b in chunk:
        # Protobuf strings will contain mostly printable ASCII, newlines, and maybe a few other chars.
        # If we see control characters that are not tab, newline, carriage return, let's stop.
        if b < 32 and b not in (9, 10, 13):
            # If we've already collected a lot of text, this is likely the end of the string field.
            if len(text_chars) > 20000:
                break
        text_chars.append(chr(b))
        
    extracted_text = "".join(text_chars)
    # Trim to last printable characters or when we see protobuf delimiters
    print(f"Extracted text length: {len(extracted_text)}")
    
    # Write to file
    with open("C:/Users/nishu/workspace/wscs_bedrock/aura_docs/scratch/recovered_section.md", "w", encoding="utf-8") as out:
        out.write(extracted_text)
    print("Saved recovered section to recovered_section.md!")
else:
    print("Search string not found in protobuf log!")
