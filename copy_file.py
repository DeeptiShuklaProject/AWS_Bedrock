import shutil
import os

src = '/Users/nishantsaxena/Downloads/bedrock-ug.pdf'
dst = '/Users/nishantsaxena/workspace/wscs_bedrock/bedrock-ug.pdf'

try:
    shutil.copy(src, dst)
    print("Success")
except Exception as e:
    print(f"Error: {e}")
