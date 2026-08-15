# -*- coding: utf-8 -*-
"""Act on the YouTube audit (Tom, 16 Aug: "we need to do something about the
88 dead and 188 suspicious links").

Phase 1 — dead: every dead reference lives in related_media; the item is
removed (a category that empties is removed with it).

Phase 2 — mismatches: each flagged item plays a REAL video that isn't what
our label promised. A model triages with the lesson path for context:
  RELABEL — the actual video plausibly serves this lesson: keep the url,
            replace title with the real title, rewrite the description.
  DROP    — off-topic/junk for this lesson: remove the item.
Verdicts print for spot-checking; --apply writes with per-lesson backups in
scripts/_yt_cleanup_backup.json.

Run: python scripts/yt_link_cleanup.py [--apply]
"""
import io
import json
import os
import re
import sys

import anthropic

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

APPLY = "--apply" in sys.argv
BACKUP = os.path.join(HERE, "_yt_cleanup_backup.json")
MODEL = "claude-sonnet-5"
YT_ID = re.compile(r"(?:youtube\.com/(?:watch\?v=|embed/|shorts/)|youtu\.be/)([\w-]{11})")

SYSTEM = """You triage revision-site sidebar links. Each item was stored with
a label, but its YouTube id actually plays a different real video (title
given). Decide per item, using the lesson path for topical context:
- "relabel" if the ACTUAL video plausibly helps a GCSE student on that
  lesson's topic: give a corrected title (the real title, tidied) and a one
  sentence description of what it is and why it helps.
- "drop" if the actual video is off-topic for the lesson (trailers for the
  wrong purpose, unrelated songs, clickbait).
Return ONLY a JSON array, same order as input:
[{"n": 1, "verdict": "relabel", "title": "...", "description": "..."}, ...]
British English. When unsure, drop — a wrong link is worse than none."""


def main():
    sb = get_client()
    report = json.load(io.open(os.path.join(HERE, "_yt_audit_report.json"),
                               encoding="utf-8"))
    dead_ids = {v for v, _ in report["dead"]}
    mm = report["mismatched"]          # [vid, stored_label, actual_title, where]

    # triage the mismatches in batches of 20
    cl = anthropic.Anthropic()
    verdicts = {}                      # (vid, where) -> verdict dict
    for i in range(0, len(mm), 20):
        batch = mm[i:i + 20]
        lines = []
        for n, (vid, label, title, where) in enumerate(batch, 1):
            lines.append("%d. lesson: %s | stored label: %r | actually plays: %r"
                         % (n, where.split(" [")[0], label[:80], title[:80]))
        r = cl.messages.create(model=MODEL, max_tokens=3000, system=SYSTEM,
                               messages=[{"role": "user", "content": "\n".join(lines)}])
        text = re.sub(r"```(?:json)?", "",
                      "".join(getattr(b, "text", "") or "" for b in r.content))
        m = re.search(r"\[[\s\S]*\]", text)
        arr = json.loads(m.group(0)) if m else []
        for n, (vid, label, title, where) in enumerate(batch, 1):
            v = next((x for x in arr if x.get("n") == n), {"verdict": "drop"})
            verdicts[(vid, where)] = v
    n_re = sum(1 for v in verdicts.values() if v["verdict"] == "relabel")
    print("triage: %d relabel, %d drop" % (n_re, len(verdicts) - n_re))
    for (vid, where), v in list(verdicts.items())[:10]:
        print("  %-7s %s %s" % (v["verdict"], vid, (v.get("title") or "")[:60]))

    # sweep every lesson's related media once, applying dead-drops + verdicts
    units = {u["id"]: u for u in sb.table("units").select("id,slug,subject_id").execute().data}
    subs = {s["id"]: s["slug"] for s in sb.table("subjects").select("id,slug").execute().data}
    backup, writes = {}, []
    removed = relabelled = 0
    start = 0
    while True:
        rows = sb.table("lessons").select("id,lesson_number,unit_id,related_media") \
            .range(start, start + 199).execute().data
        if not rows:
            break
        for l in rows:
            rm = l.get("related_media")
            if not rm:
                continue
            u = units.get(l["unit_id"], {})
            where = "%s/%s/L%s [related media]" % (subs.get(u.get("subject_id"), "?"),
                                                   u.get("slug", "?"), l["lesson_number"])
            changed = False
            new_rm = []
            for cat in rm:
                items = []
                for it in cat.get("items", []):
                    mvid = YT_ID.search(it.get("url") or "")
                    vid = mvid.group(1) if mvid else None
                    if vid and vid in dead_ids:
                        removed += 1
                        changed = True
                        continue
                    v = verdicts.get((vid, where)) if vid else None
                    if v:
                        if v["verdict"] == "drop":
                            removed += 1
                            changed = True
                            continue
                        it = dict(it, title=v.get("title") or it.get("title"),
                                  description=v.get("description") or it.get("description"))
                        relabelled += 1
                        changed = True
                    items.append(it)
                if items:
                    new_rm.append(dict(cat, items=items))
                elif cat.get("items"):
                    changed = True
            if changed:
                backup[l["id"]] = l.get("related_media")
                writes.append((l["id"], new_rm))
        start += 200

    print("lessons touched: %d | items removed: %d | relabelled: %d"
          % (len(writes), removed, relabelled))
    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    if not os.path.exists(BACKUP):
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup))
    for lid, rm in writes:
        sb.table("lessons").update({"related_media": rm}).eq("id", lid).execute()
    print("applied. backup:", BACKUP)


if __name__ == "__main__":
    main()
