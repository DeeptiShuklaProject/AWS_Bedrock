import os

def normalize_code(code_str):
    lines = code_str.splitlines()
    clean_lines = []
    for line in lines:
        line_stripped = line.strip()
        if line_stripped.startswith('#'):
            continue
        if '#' in line_stripped:
            line_stripped = line_stripped.split('#', 1)[0].strip()
        if line_stripped:
            clean_lines.append(line_stripped)
    return ''.join(clean_lines).replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '')

def test_matching():
    path = 'doc_replica_aws-bedrock/doc_uday_advance_notes/02_Chapter_prerequisites.md'
    if not os.path.exists(path):
        print("Path does not exist:", path)
        return
        
    lines = open(path, encoding='utf-8').read().splitlines()
    explanations = {}
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith('```') and len(stripped) > 3 and not stripped.endswith('```'):
            lang = stripped[3:].strip()
            if lang.lower() == 'mermaid':
                i += 1
                continue
            code_lines = []
            i += 1
            found_close = False
            while i < len(lines):
                if lines[i].strip() == '```':
                    found_close = True
                    break
                code_lines.append(lines[i])
                i += 1
            
            if found_close:
                code_str = '\n'.join(code_lines).strip()
                explanation_lines = []
                j = i + 1
                found_explanation = False
                while j < len(lines):
                    j_line = lines[j].strip()
                    if j_line.startswith('### What This Code Does') or j_line.startswith('### What this code does'):
                        found_explanation = True
                        break
                    if j_line.startswith('## ') or j_line.startswith('```') or (j_line.startswith('# ') and not j_line.startswith('###')):
                        break
                    j += 1
                
                if found_explanation:
                    while j < len(lines):
                        j_line = lines[j]
                        j_line_stripped = j_line.strip()
                        if j_line_stripped.startswith('## ') or j_line_stripped.startswith('```') or j_line_stripped == '---':
                            break
                        explanation_lines.append(j_line)
                        j += 1
                    explanation_str = '\n'.join(explanation_lines).strip()
                    norm = normalize_code(code_str)
                    explanations[norm] = (code_str, explanation_str)
        i += 1
    
    print(f'Matching count: {len(explanations)}')
    for norm, (orig, exp) in list(explanations.items())[:3]:
        print(f'- Code: {repr(orig[:30])} => Exp starts with: {repr(exp[:100])}')

if __name__ == "__main__":
    test_matching()
