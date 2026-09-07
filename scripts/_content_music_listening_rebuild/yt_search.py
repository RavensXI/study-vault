# -*- coding: utf-8 -*-
"""Search YouTube for candidate recordings and report the facts that decide
whether a video can be used: real length, uploader, embeddability, age gate.
Usage: python yt_search.py N "query" ["query2" ...]"""
import json, sys, io, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import yt_dlp

N = int(sys.argv[1])
OPTS = {"quiet": True, "no_warnings": True, "skip_download": True, "extract_flat": False,
        "noplaylist": True, "ignoreerrors": True}
rows = []
with yt_dlp.YoutubeDL(OPTS) as y:
    for q in sys.argv[2:]:
        try:
            r = y.extract_info("ytsearch%d:%s" % (N, q), download=False)
        except Exception as e:
            print("SEARCH FAIL", q, e); continue
        print("\n### %s" % q)
        for e in (r.get("entries") or []):
            if not e:
                continue
            row = {"id": e.get("id"), "title": e.get("title"), "ch": e.get("uploader"),
                   "chid": e.get("channel_id"), "dur": e.get("duration"),
                   "emb": e.get("playable_in_embed"), "age": e.get("age_limit"),
                   "views": e.get("view_count"), "date": e.get("upload_date"),
                   "live": e.get("is_live"), "avail": e.get("availability")}
            rows.append(row)
            print(" %-11s %5s s emb=%-5s age=%-2s %-28s %s" % (row["id"], row["dur"], row["emb"],
                  row["age"], (row["ch"] or "")[:28], (row["title"] or "")[:74]))
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ytpick", "last_search.json"), "w",
        encoding="utf-8").write(json.dumps(rows, indent=1, ensure_ascii=False))
