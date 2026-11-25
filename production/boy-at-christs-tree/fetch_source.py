import urllib.request, urllib.parse, time, json, sys
def get(url):
    for i in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "bibliotheque-book-pipeline/1.0"})
            return urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(5 * (i + 1)); continue
            raise
title = "Мальчик у Христа на ёлке (Достоевский)"
url = "https://ru.wikisource.org/w/index.php?title=" + urllib.parse.quote(title.replace(" ", "_")) + "&action=raw"
t = get(url); open("raw/boy.wiki", "w", encoding="utf-8").write(t); print(len(t))
