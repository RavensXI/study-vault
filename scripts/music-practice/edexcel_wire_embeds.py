# -*- coding: utf-8 -*-
"""Edexcel Phase 4: wire the <!-- EMBED: key --> markers in music-edexcel
lessons. RETRO APPLIED from the OCR build: --curate searches + verifies
ONCE and saves every pick to _edexcel_embed_map.json; --apply reads ONLY
the map (yt search ordering is unstable between runs — never re-search
at apply time).

Discovery/gates reuse the proven pipeline (yt search -> oEmbed -> title
keywords -> channel plausibility -> ban list). A marker with no verified
pick is removed at apply with a loud note.

Run: python edexcel_wire_embeds.py --curate   (writes the map — review it)
     python edexcel_wire_embeds.py [--apply]  (wires from the map)
Backup: _backup_edexcel_embeds_2026-08-16.json
"""
import glob
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client
from eduqas_wire_listen_embeds import yt_search, oembed, BAN, OFFICIALISH
from ocr_wire_embeds import keywords, embed_html

MAP_PATH = os.path.join(HERE, "_edexcel_embed_map.json")
BACKUP = os.path.join(HERE, "_backup_edexcel_embeds_2026-08-16.json")
MODE = ("curate" if "--curate" in sys.argv else
        "apply" if "--apply" in sys.argv else "dry")


def pick(work):
    kws = keywords(work)
    for q in (work + " official", work):
        for vid, title, owner in yt_search(q, 8):
            tl, ol = title.lower(), (owner or "").lower()
            if not any(k in tl for k in kws):
                continue
            if any(b in tl for b in BAN):
                continue
            if not (any(k in ol for k in kws) or any(o in ol for o in OFFICIALISH)
                    or ("official" in tl and any(k in tl for k in kws))):
                continue
            t2, a2 = oembed(vid)
            if t2 is None:
                continue
            return {"vid": vid, "title": t2, "author": a2}
    return None


def drafts():
    for path in sorted(glob.glob(os.path.join(HERE, "_edexcel_drafts",
                                              "*_L*.json"))):
        base = os.path.basename(path)[:-5]
        uslug, num = base.rsplit("_L", 1)
        d = json.load(io.open(path, encoding="utf-8"))
        yield uslug, int(num), d.get("embeds") or {}


def curate():
    result = json.load(io.open(MAP_PATH, encoding="utf-8")) \
        if os.path.exists(MAP_PATH) else {}
    for uslug, num, emb in drafts():
        for key, work in emb.items():
            if work in result:
                continue
            try:
                p = pick(work)
            except Exception as e:
                print("  ! search error %r: %s" % (work, e))
                p = None
            result[work] = p
            print("%s %-46s -> %s" % ("OK " if p else "DEL", work[:46],
                                      "%s | %s | %s" % (p["vid"], p["title"][:40],
                                                        p["author"][:26]) if p else "none"))
    io.open(MAP_PATH, "w", encoding="utf-8").write(
        json.dumps(result, indent=1, ensure_ascii=False))
    ok = sum(1 for v in result.values() if v)
    print("\nmap: %d works, %d verified -> %s" % (len(result), ok, MAP_PATH))


def apply():
    emap = json.load(io.open(MAP_PATH, encoding="utf-8"))
    sb = get_client()
    sub = sb.table("subjects").select("id").eq("slug", "music-edexcel") \
        .execute().data[0]["id"]
    units = {u["slug"]: u["id"] for u in
             sb.table("units").select("id,slug,subject_id").execute().data
             if u["subject_id"] == sub}
    backup, writes = {}, []
    wired = removed = 0
    for uslug, num, emb in drafts():
        if not emb:
            continue
        row = sb.table("lessons").select("id,content_html") \
            .eq("unit_id", units[uslug]).eq("lesson_number", num) \
            .execute().data
        if not row:
            print("%s L%d: not in DB — skipped" % (uslug, num))
            continue
        row = row[0]
        ch = row["content_html"]
        if "<!-- EMBED:" not in ch:
            continue
        changed = False
        for key, work in emb.items():
            marker = "<!-- EMBED: %s -->" % key
            if marker not in ch:
                continue
            p = emap.get(work)
            if p:
                ch = ch.replace(marker, embed_html(p["vid"], p["title"], work))
                wired += 1
            else:
                ch = ch.replace("<p>%s</p>" % marker, "")
                ch = ch.replace(marker, "")
                removed += 1
                print("%s L%d: %r NO VERIFIED VIDEO — marker removed"
                      % (uslug, num, work[:40]))
            changed = True
        if changed:
            backup[row["id"]] = row["content_html"]
            writes.append((row["id"], ch))
    print("wired %d | removed %d | lessons %d" % (wired, removed, len(writes)))
    if MODE != "apply":
        print("DRY RUN — re-run with --apply")
        return
    if not os.path.exists(BACKUP):
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup))
    for lid, ch in writes:
        sb.table("lessons").update({"content_html": ch}).eq("id", lid) \
            .execute()
    print("applied. backup:", BACKUP)


if __name__ == "__main__":
    if MODE == "curate":
        curate()
    else:
        apply()
