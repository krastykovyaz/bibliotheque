import re,json
t=open('raw/the-blizzard.wiki',encoding='utf-8').read()
t=t.split('<onlyinclude>',1)[1].split('</onlyinclude>')[0]
t=re.sub(r'<ref[^>]*/>','',t); t=re.sub(r'<ref.*?</ref>','',t,flags=re.S)
# epigraph
m=re.search(r'<poem>(.*?)</poem>',t,re.S)
epi=[l.strip() for l in m.group(1).splitlines() if l.strip() and not l.strip().startswith('{{')]
t=t[:t.index('{{Эпиграф3')]+t[t.index('Автор эпиграфа'):].split('}}',1)[1]
t=re.sub(r'\{\{[^{}]*\}\}','',t)
t=re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]*)\]\]',r'\1',t)
t=re.sub(r'<[^>]+>','',t)
t=t.replace("'''","").replace("''","").replace('\xa0',' ')
paras=[re.sub(r'\s+',' ',p).strip() for p in t.split('\n\n')]
paras=[p for p in paras if p]
json.dump({'epigraph':epi,'paras':paras},open('raw/clean.json','w'),ensure_ascii=False,indent=1)
print(epi)
for i,p in enumerate(paras): print(i,len(p.split()),p)
