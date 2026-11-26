import re, json
t = open('raw/t.wiki', encoding='utf-8').read()
t = t.split('{{F1|', 1)[1].split('\n|1831}}')[0]
t = t.split('\n', 1)[1]                                  # the title line of F1
t = re.sub(r'\{\{Rfloat\|[^}]*\}\}', '', t)
t = re.sub(r'\{\{indent\|2\|([^}]*)\}\}', r'\1', t)
t = t.replace("''", '').replace('&nbsp;', ' ').replace('\xa0', ' ')
lines = [l.strip() for l in t.split('\n')]
blocks, cur = [], []
for l in lines:
    if l: cur.append(l)
    elif cur: blocks.append(cur); cur = []
if cur: blocks.append(cur)
flat = [l for b in blocks for l in b]
bad = [l for l in flat if re.search(r'[{}<>\[\]|]', l)]
print('suspicious lines:', bad)
json.dump({'blocks': blocks, 'lines': flat}, open('raw/clean.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(blocks), len(flat))
n = 0
with open('raw/numbered.txt', 'w', encoding='utf-8') as f:
    for bi, b in enumerate(blocks):
        f.write(f'--- block {bi}\n')
        for l in b:
            f.write(f'{n} {l}\n'); n += 1
