import zlib
import gzip
import bz2
import lzma

pb_path = "C:/Users/nishu/.gemini/antigravity/conversations/ac51f2df-f9cd-48af-a743-df4a1e12cf07.pb"

with open(pb_path, "rb") as f:
    data = f.read()

print("File size:", len(data))

# Try zlib
try:
    dec = zlib.decompress(data)
    print("zlib successful, decompressed size:", len(dec))
except Exception as e:
    print("zlib failed:", e)

# Try zlib with wbits (raw DEFLATE or gzip/zlib header auto-detect)
try:
    dec = zlib.decompress(data, zlib.MAX_WBITS | 32)
    print("zlib auto-detect successful, decompressed size:", len(dec))
except Exception as e:
    print("zlib auto-detect failed:", e)

# Try gzip
try:
    dec = gzip.decompress(data)
    print("gzip successful, decompressed size:", len(dec))
except Exception as e:
    print("gzip failed:", e)

# Try bz2
try:
    dec = bz2.decompress(data)
    print("bz2 successful, decompressed size:", len(dec))
except Exception as e:
    print("bz2 failed:", e)

# Try lzma
try:
    dec = lzma.decompress(data)
    print("lzma successful, decompressed size:", len(dec))
except Exception as e:
    print("lzma failed:", e)
