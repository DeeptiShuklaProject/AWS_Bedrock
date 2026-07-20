import sys
content = open('doc_uday_advance_notes/17_Chapter_complete_end_to_end_flow.md', encoding='utf-8').read()
parts = content.split('```')
print('PARTS:', len(parts))
for p in parts[1::2]:
    print(repr(p.split('\n')[0]))
