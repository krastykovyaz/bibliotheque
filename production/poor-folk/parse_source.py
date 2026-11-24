import re,json,glob,html
def clean(t):
    t=re.sub(r'<ref[^>]*?/>|<ref[^>]*>.*?</ref>','',t,flags=re.S)
    t=re.sub(r'<section[^>]*/>','',t)
    t=re.sub(r'\{\{(?:poem1|поэма)\|\|?([^}|]*)\|?\}\}',r'\1',t)
    t=re.sub(r'\{\{right\|([^}]*)\}\}',r'\1',t)
    t=re.sub(r'\{\{эпиграф2?\|([^}]*)\}\}',r'\1',t)
    t=re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]*)\]\]',r'\1',t)
    t=re.sub(r"'{2,}","",t)
    t=re.sub(r'<[^>]+>','',t)
    t=html.unescape(t.replace('&nbsp;',' '))
    t=re.sub(r'\{\{[^}]*\}\}','',t)
    return re.sub(r'[ \t]+',' ',t).strip()
letters=[]
for f in sorted(glob.glob('raw/*.wiki')):
    if f.endswith('19.wiki'): continue
    txt=open(f,encoding='utf-8').read()
    body=txt.split('__NOTOC__',1)[1]
    for chunk in re.split(r'\n==[^=\n]*==\n',body)[1:]:
        lines=[clean(l) for l in chunk.split('\n')]
        lines=[l for l in lines if l]
        if not lines: continue
        date=lines[0]
        letters.append({'src':f,'date':date,'paras':lines[1:]})
print(len(letters))
for i,l in enumerate(letters): print(i+1,l['src'][-7:-5],l['date'][:30],len(l['paras']),sum(len(p.split()) for p in l['paras']),'|',l['paras'][0][:40] if l['paras'] else '')
json.dump(letters,open('letters_raw.json','w'),ensure_ascii=False,indent=1)
