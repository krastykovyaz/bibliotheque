import urllib.request, urllib.parse, json, time, sys
def get(url):
    for i in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "bibliotheque-book-pipeline/1.0"})
            return urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(10 * (i + 1)); continue
            raise
def api(**p):
    p["format"] = "json"; r = get("https://ru.wikisource.org/w/api.php?" + urllib.parse.urlencode(p)); time.sleep(3); return json.loads(r)
if __name__ == "__main__":
    if sys.argv[1] == "search":
        for t in api(action="query", list="search", srsearch=sys.argv[2], srlimit=20)["query"]["search"]: print(t["title"], t["size"], t["wordcount"])
    else:
        d = api(action="query", prop="revisions", rvprop="content", rvslots="main", titles=sys.argv[1])
        for p in d["query"]["pages"].values():
            txt = p["revisions"][0]["slots"]["main"]["*"]; print(len(txt)); open(sys.argv[2], "w").write(txt)
