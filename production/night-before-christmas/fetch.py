import urllib.request, urllib.parse, time, sys
t="Ночь перед Рождеством (Гоголь)"
url="https://ru.wikisource.org/w/index.php?title="+urllib.parse.quote(t.replace(" ","_"))+"&action=raw"
for i in range(6):
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"bibliotheque-book-pipeline/1.0"})
        d=urllib.request.urlopen(req,timeout=60).read().decode("utf-8")
        open("raw/night.wiki","w",encoding="utf-8").write(d); print(len(d)); break
    except urllib.error.HTTPError as e:
        print(e.code); time.sleep(5*2**i)
