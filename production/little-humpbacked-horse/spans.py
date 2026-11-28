import json, re
def load():
    c = json.load(open('raw/clean.json', encoding='utf-8'))
    d, bl = [], {}
    for k, blocks in c.items():
        bl[k] = []
        for b in blocks:
            bl[k].append((len(d), len(d) + len(b) - 1)); d.extend(b)
    return d, bl
def spans(d):
    out, i = [], 0
    state = 0; start = None
    for i, l in enumerate(d):
        o, c = l.count('«'), l.count('»')
        if state == 0 and o:
            first = bool(re.match(r'^(— )?«', l))
            start = i if first else i + 1
            state = o - c
            if state <= 0:
                state = 0
                if first: out.append((i, i))
                # single-line mid quote: keep narrator
            elif not first and False: pass
            if state > 0 and not first: start = i + 1
        elif state > 0:
            state += o - c
            if state <= 0:
                state = 0; out.append((start, i))
    return out
if __name__ == '__main__':
    d, bl = load(); sp = spans(d)
    for n, (a, b) in enumerate(sp): print(n, a, b, '|', d[a][:50], '|', d[a-1][:40] if a else '')
    print(len(sp))
