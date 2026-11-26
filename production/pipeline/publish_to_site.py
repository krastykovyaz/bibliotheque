#!/usr/bin/env python3
"""Adds a finished book to the site: cover, PDFs, full text for the reading pages and the entry in data/books.json.
Then validates the build, commits, pushes and deploys to the main server.

  production/pipeline/.venv/bin/python production/pipeline/publish_to_site.py <slug> --youtube <public video link> [--no-deploy]

Run it only when the YouTube video is Public or Unlisted: the book page plays it and links to it."""
import argparse, json, os, shutil, subprocess, sys
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def sh(cmd, **kw):
    r = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, **kw)
    if r.returncode != 0:
        sys.exit(f"failed: {' '.join(cmd)}\n{(r.stdout + r.stderr)[-800:]}")
    return r.stdout


ap = argparse.ArgumentParser()
ap.add_argument("slug")
ap.add_argument("--youtube", default="https://www.youtube.com/watch?v=PLACEHOLDER", help="the video link; without it the page says the video is coming soon")
ap.add_argument("--lang", default=None, help="en (default, the translation) or ru (the Russian original, text and PDFs only)")
ap.add_argument("--part", action="append", default=[], help='one per part, in order: "Part 1: Title|https://www.youtube.com/watch?v=ID" (a series)')
ap.add_argument("--playlist", default=None, help="the series playlist link")
ap.add_argument("--no-deploy", action="store_true")
a = ap.parse_args()

bdir = os.path.join(ROOT, "production", a.slug)
B = json.load(open(os.path.join(bdir, "book.json"), encoding="utf-8"))
lang, slug, prefix = a.lang or B.get("lang", "en"), a.slug, B["prefix"]
RU = lang == "ru"
R = B.get("ru", {}) if RU else {}
sfx = "_ru" if RU else ""
A5, A4 = f"{prefix}_A5_reading{sfx}.pdf", f"{prefix}_A4_booklet{sfx}.pdf"
NOBOOK = bool(B.get("no_booklet"))
for need in ((A5,) if NOBOOK else (A5, A4)) + ("art/png/cover.png", "source_clean.json" if RU else "translation_en.json"):
    if not os.path.exists(os.path.join(bdir, need)):
        sys.exit(f"missing {need} in {bdir}; run the earlier stages first")

# cover, PDFs
if not RU or not os.path.exists(os.path.join(ROOT, "public/covers", f"{slug}.webp")):
    Image.open(os.path.join(bdir, "art/png/cover.png")).convert("RGB").resize((1000, 1000), Image.LANCZOS).save(os.path.join(ROOT, "public/covers", f"{slug}.webp"), quality=88)

# full text for the reading pages: "## I · Name" starts a part, blank lines separate paragraphs
if RU:
    T = {x["part"]: x["paragraphs"] for x in json.load(open(os.path.join(bdir, "source_clean.json"), encoding="utf-8"))}
    NAMES = R["names"]
else:
    T = json.load(open(os.path.join(bdir, "translation_en.json"), encoding="utf-8"))
    NAMES = B["names"]
os.makedirs(os.path.join(ROOT, "data/texts"), exist_ok=True)
with open(os.path.join(ROOT, "data/texts", f"{slug}-{lang}.txt"), "w", encoding="utf-8") as f:
    for part in B["parts"]:
        f.write(f"## {part} · {NAMES[part]}\n\n" + "\n\n".join(x[2:] if x.startswith("§ ") else x for x in T[part]) + "\n\n")

# the Russian cover for the Russian pages
RUCOVER = os.path.join(bdir, "art/png/cover_ru.png")
if RU and os.path.exists(RUCOVER):
    Image.open(RUCOVER).convert("RGB").resize((1000, 1000), Image.LANCZOS).save(os.path.join(ROOT, "public/covers", f"{slug}-ru.webp"), quality=88)

# the book entry
bp = os.path.join(ROOT, "data/books.json")
books = json.load(open(bp, encoding="utf-8"))
entry_lang = {"title": R.get("title", B["title"]), "description": R.get("description", B["site_description"]), "youtube": a.youtube,
              "pdf": f"/pdf/{slug}-{lang}.pdf", "text": f"texts/{slug}-{lang}.txt"}
if a.part:
    entry_lang["parts"] = [dict(zip(("title", "youtube"), x.split("|", 1))) for x in a.part]
    entry_lang["youtube"] = entry_lang["parts"][0]["youtube"]
if a.playlist:
    entry_lang["playlist"] = a.playlist
if not NOBOOK:
    entry_lang["booklet"] = f"/pdf/{slug}-{lang}-booklet.pdf"
    entry_lang["bookletDuplex"] = f"/pdf/{slug}-{lang}-booklet-duplex.pdf"
if B.get("text_note") and not RU:
    entry_lang["textNote"] = B["text_note"]
existing = next((b for b in books if b["id"] == slug), None)
if existing:
    existing["languages"][lang] = entry_lang
    if RU and os.path.exists(RUCOVER): existing["coverRu"] = f"/covers/{slug}-ru.webp"
else:
    books.append({"id": slug, "author": {"en": B["author"], "ru": B.get("author_ru", B["author"])}, "year": B["year"],
                  "cover": f"/covers/{slug}.webp", "languages": {lang: entry_lang}})
    if RU and os.path.exists(RUCOVER): books[-1]["coverRu"] = f"/covers/{slug}-ru.webp"
json.dump(books, open(bp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(bp, "a").write("\n")

# the book is no longer "next on the shelf"
qp = os.path.join(ROOT, "data/queue.json")
q = json.load(open(qp, encoding="utf-8"))
if any(i["title_en"].strip().lower() == B["title"].strip().lower() and i.get("kids") for i in q["items"]):
    for b_ in books:                      # a children's book: it is also listed on the Children page
        if b_["id"] == slug: b_["kids"] = True
    json.dump(books, open(bp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(bp, "a").write("\n")
n = len(q["items"])
q["items"] = [i for i in q["items"] if i["title_en"].strip().lower() != B["title"].strip().lower()]
if len(q["items"]) != n:
    json.dump(q, open(qp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(qp, "a").write("\n")

# rebuild the PDFs now: the last page carries the QR code of the video and of the book page, which are known only now
PIPE = os.path.dirname(os.path.abspath(__file__))
env = dict(os.environ, BOOK_DIR=bdir, **({"BOOK_LANG": "ru"} if RU else {}))
# a verse book keeps its own build_pdf_verse.py (it keeps the line breaks of the Russian text)
BUILDER = os.path.join(bdir, "build_pdf_verse.py") if os.path.exists(os.path.join(bdir, "build_pdf_verse.py")) else os.path.join(PIPE, "build_pdf.py")
subprocess.run([sys.executable, "-W", "ignore", BUILDER], cwd=bdir, env=env, check=True, capture_output=True)
if not NOBOOK:
    subprocess.run([sys.executable, os.path.join(PIPE, "make_booklet.py"), os.path.join(bdir, A5), os.path.join(bdir, A4)], check=True, capture_output=True)
    subprocess.run([sys.executable, os.path.join(PIPE, "make_booklet.py"), os.path.join(bdir, A5), os.path.join(bdir, A4.replace("_A4_booklet", "_A4_booklet_duplex")), "--fold"], check=True, capture_output=True)
shutil.copy(os.path.join(bdir, A5), os.path.join(ROOT, "public/pdf", f"{slug}-{lang}.pdf"))
if not NOBOOK:
    shutil.copy(os.path.join(bdir, A4), os.path.join(ROOT, "public/pdf", f"{slug}-{lang}-booklet.pdf"))
    shutil.copy(os.path.join(bdir, A4.replace("_A4_booklet", "_A4_booklet_duplex")), os.path.join(ROOT, "public/pdf", f"{slug}-{lang}-booklet-duplex.pdf"))

print("validating the site build ...")
out = sh(["npm", "run", "build"])
if "Complete!" not in out:
    sys.exit("the site build did not complete:\n" + out[-600:])
print("build ok")

sh(["git", "add", "data/books.json", "data/queue.json", f"data/texts/{slug}-{lang}.txt", f"public/covers/{slug}.webp", f"public/pdf/{slug}-{lang}.pdf"] + ([] if NOBOOK else [f"public/pdf/{slug}-{lang}-booklet.pdf", f"public/pdf/{slug}-{lang}-booklet-duplex.pdf"]) + ([f"public/covers/{slug}-ru.webp"] if RU and os.path.exists(RUCOVER) else []))
sh(["git", "commit", "-q", "-m", f"Add {B['title']} by {B['author']} to the shelf\n\nCover, reading text, PDFs and the YouTube video, made with the book pipeline.\n\nCo-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>"])
env = dict(os.environ)
env.pop("GH_TOKEN", None)
env.pop("GITHUB_TOKEN", None)
subprocess.run(["git", "-c", "credential.helper=", "-c", "credential.helper=!gh auth git-credential", "push", "-q", "origin", "main"], cwd=ROOT, env=env, check=True)
print("committed and pushed")
if not a.no_deploy:
    print(sh(["scripts/deploy-site.sh"]).strip())
    print(f"live: https://biblio.unilu.space/book/{slug}/")
