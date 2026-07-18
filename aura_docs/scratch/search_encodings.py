pb_path = "C:/Users/nishu/.gemini/antigravity/conversations/ac51f2df-f9cd-48af-a743-df4a1e12cf07.pb"

with open(pb_path, "rb") as f:
    data = f.read()

# Search for UTF-16 Little Endian and Big Endian
target = "Python for AI Agents"
target_le = target.encode("utf-16le")
target_be = target.encode("utf-16be")

print("UTF-16 LE match:", data.find(target_le))
print("UTF-16 BE match:", data.find(target_be))

# Let's search for ASCII/UTF-8 lowercase or part of it
target_utf8 = target.encode("utf-8")
print("UTF-8 match:", data.find(target_utf8))

# Let's search for "Ecosystem" in UTF-8
print("Ecosystem UTF-8 match:", data.find(b"Ecosystem"))
