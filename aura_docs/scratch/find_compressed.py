import zlib
import gzip
import io

pb_path = "C:/Users/nishu/.gemini/antigravity/conversations/ac51f2df-f9cd-48af-a743-df4a1e12cf07.pb"

with open(pb_path, "rb") as f:
    data = f.read()

print(f"Scanning for compressed blocks in {len(data)} bytes...")

# Scan for gzip headers
for i in range(len(data) - 2):
    if data[i] == 0x1f and data[i+1] == 0x8b:
        try:
            fileobj = io.BytesIO(data[i:])
            with gzip.GzipFile(fileobj=fileobj) as g:
                dec = g.read()
            if len(dec) > 1000:
                print(f"Gzip block at offset {i} - Decompressed size: {len(dec)}")
                if b"Ecosystem Domination" in dec or b"Python for AI Agents" in dec:
                    print("  FOUND KEYWORD!")
                    with open(f"C:/Users/nishu/workspace/wscs_bedrock/aura_docs/scratch/decompressed_gzip_{i}.txt", "wb") as out:
                        out.write(dec)
        except Exception:
            pass

# Scan for zlib headers
for i in range(len(data) - 2):
    if data[i] == 0x78 and data[i+1] in (0x9c, 0x01, 0x5e):
        try:
            # Using decompressobj handles trailing data automatically
            dobj = zlib.decompressobj()
            dec = dobj.decompress(data[i:])
            if len(dec) > 1000:
                print(f"Zlib block at offset {i} - Decompressed size: {len(dec)}")
                if b"Ecosystem Domination" in dec or b"Python for AI Agents" in dec:
                    print("  FOUND KEYWORD!")
                    with open(f"C:/Users/nishu/workspace/wscs_bedrock/aura_docs/scratch/decompressed_zlib_{i}.txt", "wb") as out:
                        out.write(dec)
        except Exception:
            pass

print("Scan complete.")
