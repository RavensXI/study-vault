# -*- coding: utf-8 -*-
"""Related media for the 12 music article lessons (WC-1 — the one catalogue
item the fix programme missed; Tom caught it mid-review, 16 Aug).

Per docs/RELATED_MEDIA_PIPELINE.md: curated external links per lesson in the
live category-grouped shape, then EVERY url audited before writing — YouTube
via oEmbed (also proves embeddability), everything else by HTTP status.
Items that fail the audit are dropped; a lesson keeps a category only if at
least one item survives. Lesson Podcast entries are NOT fabricated — the
podcast batch weaves those in when Tom runs it post-approval.

Run: python build_related_media.py [--apply]   (~12 calls, ~$0.30)
Backup: _backup_related_media_2026-08-16.json
"""
import io
import json
import os
import re
import sys
import urllib.request

import anthropic

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

APPLY = "--apply" in sys.argv
MODEL = "claude-sonnet-5"


def arg(flag, default):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


SUBJECT = arg("--subject", "music-aqa")
UNITS = arg("--units", "aos1-western-classical,aos2-popular-music,"
            "aos3-traditional-music,aos4-since-1910").split(",")
BACKUP = os.path.join(HERE, "_backup_related_media_%s.json" % SUBJECT)

SYSTEM = """You curate external media for GCSE Music (age 15-16) revision
lessons. Suggest genuinely good, REAL, currently-available resources a UK
student can open free of charge.

Prefer sources that stay up: BBC (Bitesize, Radio 3, Ten Pieces, iPlayer/
Sounds series pages), official orchestra and label YouTube channels,
long-running podcasts (series page rather than one episode where possible),
major institutions (Royal Opera House, Philharmonia, Classic FM).

Return ONLY JSON: an array of 2-3 categories, each
{"category": "Videos & Channels" | "Podcasts" | "Listening & Documentaries"
  | "Study Tools",
 "items": [{"url": "...", "title": "...", "description": "one sentence on
            what it is AND why it helps this lesson"}]}
4-7 items total per lesson. Only real URLs you are confident exist — a
plausible-looking dead link is worse than fewer items. British English.
Never invent a URL pattern; use canonical homepages/channel/series URLs when
unsure of a deep link."""


def audit(url):
    try:
        if "youtube.com" in url or "youtu.be" in url:
            m = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", url)
            if m:
                probe = ("https://www.youtube.com/oembed?format=json&url="
                         "https://www.youtube.com/watch?v=" + m.group(1))
                urllib.request.urlopen(probe, timeout=15).read()
                return True
            # channel / playlist urls: plain fetch
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        r = urllib.request.urlopen(req, timeout=15)
        return r.status < 400
    except Exception:
        return False


def main():
    sb = get_client()
    cl = anthropic.Anthropic()
    subj = [s for s in sb.table("subjects").select("id,slug").execute().data
            if s["slug"] == SUBJECT][0]["id"]
    units = {u["slug"]: u["id"] for u in sb.table("units").select("id,slug,subject_id")
             .execute().data if u["subject_id"] == subj}

    backup, writes = {}, []
    for uslug in UNITS:
        rows = sb.table("lessons").select("id,lesson_number,title,description,content_html,related_media") \
            .eq("unit_id", units[uslug]).order("lesson_number").execute().data
        for l in rows:
            if l.get("related_media"):
                continue
            heads = re.findall(r"<h[23][^>]*>(.*?)</h[23]>", l["content_html"] or "")
            brief = ("LESSON: %s\nUNIT: %s\nDESCRIPTION: %s\nSECTIONS: %s"
                     % (l["title"], uslug, l.get("description") or "",
                        " | ".join(re.sub(r"<[^>]+>", "", h) for h in heads[:10])))
            cats = None
            for attempt in range(2):
                r = cl.messages.create(model=MODEL, max_tokens=2500, system=SYSTEM,
                                       messages=[{"role": "user", "content": brief}])
                text = "".join(getattr(b, "text", "") or "" for b in r.content)
                text = re.sub(r"```(?:json)?", "", text)
                m = re.search(r"\[[\s\S]*\]", text)
                if m:
                    try:
                        cats = json.loads(m.group(0))
                        break
                    except ValueError:
                        pass
                print("%s L%d: bad output (attempt %d)" % (uslug, l["lesson_number"],
                                                           attempt + 1))
            if cats is None:
                continue
            kept, dropped = [], 0
            for c in cats:
                items = []
                for it in c.get("items", []):
                    if it.get("url") and audit(it["url"]):
                        items.append({"url": it["url"], "title": it.get("title", ""),
                                      "description": it.get("description", "")})
                    else:
                        dropped += 1
                if items:
                    kept.append({"category": c.get("category", "Related"),
                                 "items": items})
            n = sum(len(c["items"]) for c in kept)
            print("%s L%d: %d live item(s) in %d categor%s, %d dead dropped"
                  % (uslug, l["lesson_number"], n, len(kept),
                     "y" if len(kept) == 1 else "ies", dropped))
            if n < 2:
                print("   too thin — skipped (will need a manual pass)")
                continue
            backup["%s/%d" % (uslug, l["lesson_number"])] = {
                "id": l["id"], "related_media": l.get("related_media")}
            writes.append((l["id"], kept))

    print("\nlessons to write: %d" % len(writes))
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
