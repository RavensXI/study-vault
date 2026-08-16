# -*- coding: utf-8 -*-
"""OCR Phase 3c: wire the <!-- EMBED: key --> markers the article builder
left in music-ocr lessons. The embeds map (key -> work name) lives in the
_ocr_drafts/*.json the builder saved. Discovery + gates reuse the proven
pipeline from eduqas_wire_listen_embeds: real YouTube search, then oEmbed
(alive + embeddable), title keyword match, plausible-channel check, ban
list. A marker with no verified video is REMOVED (with a loud note) —
never shipped dead.

Run: python ocr_wire_embeds.py [--apply]
Backup: _backup_ocr_embeds_2026-08-16.json
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
from eduqas_wire_listen_embeds import (yt_search, oembed, vid_of,  # noqa
                                       BAN, OFFICIALISH)

APPLY = "--apply" in sys.argv
BACKUP = os.path.join(HERE, "_backup_ocr_embeds_2026-08-16.json")
STOP = {"the", "and", "with", "from", "for", "concerto", "major", "minor",
        "no", "movement", "music", "theme", "official"}

# hand-verified picks where automated search failed or chose badly
# (all oEmbed-verified again at apply time)
KNOWN_BY_KEY = {
    "halo-theme": "bwikj_lQLT0",            # Martin O'Donnell - Topic
    "zelda-theme": "xuXHrHRZzLk",           # Nintendo of America concert
    "west-african-ensemble": "pT242MrDkls", # Mamady Keita & Sewa Kan live
    "call-response": "HTVmwaaXfLo",         # Famoudou Konate, field recs
    "samba-bateria": "VikKxRiAMrM",         # Mangueira bateria (4K)
}


def keywords(work):
    toks = [t.lower() for t in re.findall(r"[A-Za-z']{3,}", work)
            if t.lower() not in STOP]
    return toks or [work.lower()]


def pick(work):
    kws = keywords(work)
    for vid, title, owner in yt_search(work + " official", 8):
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


def embed_html(vid, title, work):
    cap = "Listen &mdash; %s" % work.replace("&", "&amp;")
    return ('<figure class="sv-embed"><div class="sv-embed-frame">'
            '<iframe src="https://www.youtube.com/embed/%s" title="%s" '
            'loading="lazy" allow="fullscreen" allowfullscreen></iframe>'
            '</div><figcaption class="sv-embed-cap">%s</figcaption></figure>'
            % (vid, title.replace('"', "&quot;"), cap))


def main():
    sb = get_client()
    sub = sb.table("subjects").select("id").eq("slug", "music-ocr") \
        .execute().data[0]["id"]
    units = {u["slug"]: u["id"] for u in
             sb.table("units").select("id,slug,subject_id").execute().data
             if u["subject_id"] == sub}
    backup, writes = {}, []
    wired = removed = 0
    cache = {}
    for path in sorted(glob.glob(os.path.join(HERE, "_ocr_drafts",
                                              "*_L*.json"))):
        base = os.path.basename(path)[:-5]
        uslug, num = base.rsplit("_L", 1)
        d = json.load(io.open(path, encoding="utf-8"))
        emb = d.get("embeds") or {}
        if not emb:
            continue
        row = sb.table("lessons").select("id,content_html") \
            .eq("unit_id", units[uslug]).eq("lesson_number", int(num)) \
            .execute().data
        if not row:
            print("%s L%s: not in DB — skipped" % (uslug, num))
            continue
        row = row[0]
        ch = row["content_html"]
        if "<!-- EMBED:" not in ch:
            print("%s L%s: no markers left — skipped" % (uslug, num))
            continue
        changed = False
        for key, work in emb.items():
            marker = "<!-- EMBED: %s -->" % key
            if marker not in ch:
                continue
            if key in KNOWN_BY_KEY:
                t2, a2 = oembed(KNOWN_BY_KEY[key])
                cache[work] = ({"vid": KNOWN_BY_KEY[key], "title": t2,
                                "author": a2} if t2 else None)
            elif work not in cache:
                try:
                    cache[work] = pick(work)
                except Exception as e:
                    print("  ! search error for %r: %s" % (work, e))
                    cache[work] = None
            p = cache[work]
            if p:
                ch = ch.replace(marker, embed_html(p["vid"], p["title"], work))
                wired += 1
                print("%s L%s: %s -> %s | %s | %s"
                      % (uslug, num, key, p["vid"], p["title"][:40],
                         p["author"][:28]))
            else:
                ch = ch.replace("<p>%s</p>" % marker, "")
                ch = ch.replace(marker, "")
                removed += 1
                print("%s L%s: %s (%r) — NO VERIFIED VIDEO, marker removed"
                      % (uslug, num, key, work[:40]))
            changed = True
        if changed:
            backup[row["id"]] = row["content_html"]
            writes.append((row["id"], ch))
    print("\nwired %d | removed %d | lessons %d" % (wired, removed,
                                                    len(writes)))
    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    if not os.path.exists(BACKUP):
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup))
    for lid, ch in writes:
        sb.table("lessons").update({"content_html": ch}).eq("id", lid) \
            .execute()
    print("applied. backup:", BACKUP)


if __name__ == "__main__":
    main()
