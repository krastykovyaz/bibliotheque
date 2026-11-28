#!/usr/bin/env python3
"""Cleans the Wikisource wikitext of Konyok-Gorbunok (Yershov), edition 1868 (the 7th, last in the author's lifetime) into raw/clean.json.
The author's text only; the part epigraphs are kept as the first block of each part. Nothing is reworded."""
import re, json
t = open('raw/t1868.wiki', encoding='utf-8').read()
body = t.split('{{poem-on|Конёк-горбунок}}', 1)[1].split('{{poem-off}}')[0]
parts = re.split(r'\n== Часть (I+) ==\n', '\n' + body)
parts = dict(zip(parts[1::2], parts[2::2]))
def clean(s):
    s = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]*)\]\]', r'\1', s)
    s = re.sub(r'\{\{right\|<small>(.*?)</small>\}\}', r'\1', s)
    s = re.sub(r'\{\{Poemx1\|\|<small>(.*?)</small>\}\}', r'\1', s, flags=re.S)
    s = s.replace('<poem>', '\n').replace('</poem>', '\n').replace('&nbsp;', ' ').replace('\xa0', ' ')
    s = s.replace("''", '')
    return s
out, flat = {}, []
for k, s in parts.items():
    s = clean(s)
    blocks, cur = [], []
    for l in [l.strip() for l in s.split('\n')]:
        if l: cur.append(l)
        elif cur: blocks.append(cur); cur = []
    if cur: blocks.append(cur)
    out[k] = blocks
bad = [l for b in out.values() for bl in b for l in bl if re.search(r'[{}<>\[\]|=]', l)]
print('suspicious:', bad)
json.dump(out, open('raw/clean.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
n = 0
with open('raw/numbered.txt', 'w', encoding='utf-8') as f:
    for k, bl in out.items():
        f.write(f'=== PART {k}\n')
        for bi, b in enumerate(bl):
            f.write(f'--- block {bi}\n')
            for l in b: f.write(f'{n} {l}\n'); n += 1
print({k: (len(v), sum(len(b) for b in v)) for k, v in out.items()}, n, sum(len(l.split()) for v in out.values() for b in v for l in b))
