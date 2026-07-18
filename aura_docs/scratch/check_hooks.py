with open(r"C:\Users\nishu\workspace\wscs_bedrock\aura_docs\frontend\src\components\InteractiveComponents.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# We can find all component declarations and see what hooks they define.
# Let's search for functions and check their bodies.
import re
components = re.split(r'export const ', content)
for comp in components[1:]:
    lines = comp.split('\n')
    name = lines[0].split('=')[0].strip()
    # Find all setSuccess calls in this component
    has_set_success = any('setSuccess' in l for l in lines)
    defines_success = any('useState' in l and 'success' in l for l in lines)
    if has_set_success and not defines_success:
        print(f"Component '{name}' uses setSuccess but does NOT define success state!")
