"""Loads the book.json of the book being made. The book folder is BOOK_DIR, or the current folder."""
import json, os, sys

PIPE = os.path.dirname(os.path.abspath(__file__))


def load():
    d = os.path.abspath(os.environ.get("BOOK_DIR") or os.getcwd())
    p = os.path.join(d, "book.json")
    if not os.path.exists(p):
        sys.exit(f"book.json not found in {d}. Run from the book folder or set BOOK_DIR.")
    b = json.load(open(p, encoding="utf-8"))
    # each part uses the picture of the most recent part that has one (parts are grouped under one picture)
    art_for_part, cur = {}, None
    for part in b["parts"]:
        cur = b["art"].get(part, cur)
        art_for_part[part] = cur
    b["art_for_part"] = art_for_part
    return b, d
