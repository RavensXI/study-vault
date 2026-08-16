# -*- coding: utf-8 -*-
"""Give every music key-fact box a SPECIFIC revision task (Tom's review
find, 16 Aug): the music article pipeline never emitted
data-revision-tip, so the lightbulbs fell back to the generic 'Cover
this box...' text. Every other subject family is fully tipped — the gap
is music-only (music-aqa, -eduqas, -ocr, -edexcel; music-technology
already has 37/37).

One model call per lesson: each box's own content becomes one concrete,
actionable retrieval task (<=22 words, plain text). Injected as
data-revision-tip on the box's opening tag — main.js line ~2491 prefers
it over the generic fallback. Attributes are not narrated, so manifests
are untouched.

Run: python music_revision_tips.py [--apply]
Backup: _backup_music_revision_tips_2026-08-16.json
"""
import io
import json
import os
import re
import sys

import anthropic

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

APPLY = "--apply" in sys.argv
BACKUP = os.path.join(HERE, "_backup_music_revision_tips_2026-08-16.json")
SUBJECTS = ["music-aqa", "music-eduqas", "music-ocr", "music-edexcel"]
MODEL = "claude-sonnet-5"

PROMPT = """For each numbered key-fact box below (from the GCSE Music
lesson '{title}'), write ONE specific, actionable revision task a
student can do right now with THAT box's content. Retrieval-practice
flavoured: cover-and-recall, list-from-memory, write-out, sketch,
count, hum-and-name. Reference the box's actual content (names, numbers,
terms) so the task could not be attached to any other box. Maximum 22
words each. Plain text, no quotation marks of any kind, no lyrics.

Return ONLY a JSON array of strings, one per box, in order.

{boxes}"""


def main():
    sb = get_client()
    cl = anthropic.Anthropic()
    subs = {s["slug"]: s["id"] for s in
            sb.table("subjects").select("id,slug,school_id").execute().data
            if not s["school_id"] and s["slug"] in SUBJECTS}
    units = sb.table("units").select("id,slug,subject_id").execute().data
    backup, writes = {}, []
    total = done = 0
    for slug in SUBJECTS:
        for u in [x for x in units if x["subject_id"] == subs[slug]]:
            rows = sb.table("lessons").select(
                "id,lesson_number,title,content_html") \
                .eq("unit_id", u["id"]).order("lesson_number").execute().data
            for l in rows:
                ch = l.get("content_html") or ""
                boxes = re.findall(r'(<div class="key-fact"[^>]*>)(.*?)(</div>)',
                                   ch, re.S)
                todo = [(i, b) for i, b in enumerate(boxes)
                        if "data-revision-tip" not in b[0]]
                if not todo:
                    continue
                total += len(todo)
                listing = "\n".join(
                    "%d. %s" % (i + 1,
                                re.sub(r"\s+", " ",
                                       re.sub(r"<[^>]+>", " ", b[1]))[:400])
                    for i, b in todo)
                if not APPLY:
                    print("%s %s L%d: %d box(es) need tips"
                          % (slug, u["slug"], l["lesson_number"], len(todo)))
                    continue
                tips = None
                for attempt in range(3):
                    r = cl.messages.create(
                        model=MODEL, max_tokens=1500,
                        messages=[{"role": "user", "content":
                                   PROMPT.format(title=l["title"],
                                                 boxes=listing)}])
                    text = re.sub(r"```(?:json)?", "",
                                  "".join(getattr(b, "text", "") or ""
                                          for b in r.content))
                    m = re.search(r"\[[\s\S]*\]", text)
                    if not m:
                        continue
                    try:
                        cand = json.loads(m.group(0))
                    except ValueError:
                        continue
                    if len(cand) == len(todo) and all(
                            isinstance(t, str) and 0 < len(t) <= 180
                            and '"' not in t for t in cand):
                        tips = cand
                        break
                if tips is None:
                    print("%s %s L%d: FAILED tip generation"
                          % (slug, u["slug"], l["lesson_number"]))
                    continue
                new_ch = ch
                for (i, b), tip in zip(todo, tips):
                    old_open = b[0]
                    new_open = old_open[:-1] + \
                        ' data-revision-tip="%s">' % tip.replace("&", "&amp;")
                    new_ch = new_ch.replace(old_open + b[1] + b[2],
                                            new_open + b[1] + b[2], 1)
                backup[l["id"]] = ch
                sb.table("lessons").update({"content_html": new_ch}) \
                    .eq("id", l["id"]).execute()
                done += len(todo)
                print("%s %s L%d: %d tip(s) injected"
                      % (slug, u["slug"], l["lesson_number"], len(todo)))
    if APPLY and backup and not os.path.exists(BACKUP):
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup))
    print("\n%s: %d boxes%s" % ("injected" if APPLY else "would inject",
                                done if APPLY else total,
                                "" if APPLY else " need tips"))


if __name__ == "__main__":
    main()
