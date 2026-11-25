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


def map_scene_ids(scenes, rows_from, rows_to):
    """Scene starts in book.json ("scenes": [{"id": row id of the English voice script, "art": ...}]) converted to the row ids of another
    voice script (e.g. the Russian one) by part + paragraph. A scene that starts on the first row of its paragraph starts on the first row of
    the same paragraph in the other script; one that starts on a later row (the narrator picks up after a quotation) starts on the first row of
    the same speaker in that paragraph there, or the first row of the paragraph. Returns a new list; nothing is changed in place."""
    by_id = {r["id"]: r for r in rows_from}
    out = []
    for sc in scenes:
        r = by_id[sc["id"]]
        same_par_from = [x for x in rows_from if (x["part"], x["paragraph"]) == (r["part"], r["paragraph"])]
        same_par_to = [x for x in rows_to if (x["part"], x["paragraph"]) == (r["part"], r["paragraph"])]
        if not same_par_to:
            sys.exit(f"scene {sc['id']}: no row for part {r['part']} paragraph {r['paragraph']} in the other voice script")
        pick = same_par_to[0]
        if same_par_from[0]["id"] != r["id"]:
            pick = next((x for x in same_par_to if x["speaker"] == r["speaker"]), pick)
        out.append({**sc, "id": pick["id"]})
    return out
