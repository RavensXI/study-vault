# -*- coding: utf-8 -*-
"""Site-wide YouTube link audit (Tom, 16 Aug: "do we have a test that
systematically checks all the youtube links are alive and go to the right
place?").

Enumerates every YouTube reference in the database:
  - lessons.youtube_video_id (bare ids and youtube URLs; drive/R2 skipped)
  - lessons.related_media[].items[].url
  - <iframe src=".../embed/ID"> inside lessons.content_html
  - the same inside guide_pages content

Each id is checked once via oEmbed — which proves the video EXISTS and is
EMBEDDABLE, and returns its real title + channel. Where we stored a label
(related-media titles, embed captions), the real title is compared by word
overlap: zero shared meaningful words = flagged as possibly the wrong video.
Where a label credits a channel ("Channel — Title") the prefix is compared with
oEmbed's author_name, which catches an on-topic video by the wrong channel.
Ids in DENY (build-time placeholders) are always reported dead.

Mismatch pairs a human has already cleared live in scripts/_yt_audit_accepted.json
and are not flagged again; dead-link checking ignores that file.

Output: scripts/_yt_audit_report.md (+ .json). Exit 1 if any DEAD links.
Intended cadence: weekly scheduled + on demand; scripts/tests/live/ has a
sampling wrapper for suite runs.

Usage: python scripts/audit_youtube_links.py [--limit N]
"""
import difflib
import io
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

LIMIT = None
if "--limit" in sys.argv:
    LIMIT = int(sys.argv[sys.argv.index("--limit") + 1])

YT_ID = re.compile(r"(?:youtube\.com/(?:watch\?v=|embed/|shorts/)|youtu\.be/)([\w-]{11})")
BARE = re.compile(r"^[\w-]{11}$")
STOP = set("the a an of and in on for with to from by at is are music gcse "
           "lesson official video full hd".split())

# Placeholder ids the generic build left behind. They are dead-level whatever
# the title overlap says: the video is alive, so oEmbed can never catch one, and
# one of them hid for days behind a label that shared the word "you".
DENY = {"dQw4w9WgXcQ": "known placeholder (Rick Astley) — never a real reference"}

# (id, stored label) pairs already checked by hand: a curator's label can read
# nothing like the real title while still pointing at the right video.
ACCEPTED = set()
try:
    for a in json.load(io.open(os.path.join(HERE, "_yt_audit_accepted.json"),
                               encoding="utf-8"))["accepted"]:
        ACCEPTED.add((a["id"], a["stored"]))
except Exception:
    pass


def words(s):
    return set(w for w in re.findall(r"[a-z0-9']+", (s or "").lower())
               if len(w) > 2 and w not in STOP)


CHANNEL_SPLIT = re.compile(r"^(.{2,40}?)\s+[—–-]\s+")


def norm(s):
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def wrong_credit(label, title, channel):
    """Stored labels usually read "Channel — Title". Title word overlap never
    notices an on-topic video that is somebody else's, so compare the credited
    channel with oEmbed's author_name too. Only a clear disagreement counts:
    case and punctuation are ignored, a part name matches the whole
    ("Kurzgesagt" vs "Kurzgesagt – In a Nutshell"), a channel credited anywhere
    else in the label is fine, and a prefix that reads as a topic (it turns up
    in the real title) is not a credit at all."""
    m = CHANNEL_SPLIT.match(label or "")
    if not m or not channel or not title:
        return None
    claimed = m.group(1).strip()
    a, b, lab = norm(claimed), norm(channel), norm(label)
    if not a or len(claimed.split()) > 4:
        return None
    if a in b or b in a or a in norm(title) or (words(claimed) & words(title)):
        return None
    first = re.split(r"[^A-Za-z0-9]+", channel)[0]
    if b in lab or (len(first) > 3 and norm(first) in lab):
        return None
    ct, at = set(claimed.lower().split()), set(channel.lower().split())
    if ct <= at or at <= ct:
        return None
    if difflib.SequenceMatcher(None, a, b).ratio() >= 0.6:  # "Mr Cloake"/"MrClokeHistory"
        return None
    return claimed


def oembed(vid):
    url = ("https://www.youtube.com/oembed?format=json&url="
           "https://www.youtube.com/watch?v=" + vid)
    try:
        d = json.loads(urllib.request.urlopen(url, timeout=15).read().decode("utf-8"))
        return {"ok": True, "title": d.get("title", ""), "channel": d.get("author_name", "")}
    except Exception as e:
        return {"ok": False, "err": str(e)[:60]}


def refs_from_lesson(l, subj, unit):
    where = "%s/%s/L%s" % (subj, unit, l["lesson_number"])
    out = []
    v = l.get("youtube_video_id") or ""
    if v:
        m = YT_ID.search(v)
        if m:
            out.append((m.group(1), where + " [video slot]", None))
        elif BARE.match(v.strip()):
            out.append((v.strip(), where + " [video slot]", None))
    for cat in l.get("related_media") or []:
        for it in cat.get("items", []):
            m = YT_ID.search(it.get("url") or "")
            if m:
                out.append((m.group(1), where + " [related media]", it.get("title")))
    for m in YT_ID.finditer(l.get("content_html") or ""):
        out.append((m.group(1), where + " [in-body embed]", None))
    return out


def main():
    sb = get_client()
    subs = {s["id"]: s["slug"] for s in
            sb.table("subjects").select("id,slug").execute().data}
    units = {u["id"]: (subs.get(u["subject_id"], "?"), u["slug"]) for u in
             sb.table("units").select("id,slug,subject_id").execute().data}

    refs = []
    start = 0
    while True:
        rows = sb.table("lessons") \
            .select("lesson_number,unit_id,youtube_video_id,related_media,content_html") \
            .range(start, start + 199).execute().data
        if not rows:
            break
        for l in rows:
            subj, unit = units.get(l["unit_id"], ("?", "?"))
            refs.extend(refs_from_lesson(l, subj, unit))
        start += 200
    try:
        for g in sb.table("guide_pages").select("slug,content_html").execute().data:
            for m in YT_ID.finditer(g.get("content_html") or ""):
                refs.append((m.group(1), "guide/" + str(g.get("slug")), None))
    except Exception:
        pass

    # one check per distinct id; remember every place it appears
    by_id = {}
    for vid, where, label in refs:
        by_id.setdefault(vid, {"where": [], "labels": []})
        by_id[vid]["where"].append(where)
        if label:
            by_id[vid]["labels"].append(label)
    ids = list(by_id)
    if LIMIT:
        ids = ids[:LIMIT]
    print("references: %d | distinct videos: %d%s"
          % (len(refs), len(by_id), " (checking %d)" % len(ids) if LIMIT else ""))

    dead, mismatched, ok = [], [], 0
    for i, vid in enumerate(ids):
        r = {"ok": False, "err": DENY[vid]} if vid in DENY else oembed(vid)
        info = by_id[vid]
        if not r["ok"]:
            dead.append((vid, info, r["err"]))
            print("DEAD  %s  %s  (%s)" % (vid, info["where"][0], r["err"]))
        else:
            ok += 1
            for label in info["labels"]:
                if (vid, label) in ACCEPTED:
                    continue
                claimed = wrong_credit(label, r["title"], r["channel"])
                if claimed:
                    mismatched.append((vid, label, "%s [%s]" % (r["title"], r["channel"]),
                                       info["where"][0]))
                    print("WRONG CREDIT %s stored %r but plays %r by %r  %s"
                          % (vid, label[:40], r["title"][:40], r["channel"], info["where"][0]))
                elif words(label) and not (words(label) & words(r["title"] + " " + r["channel"])):
                    mismatched.append((vid, label, r["title"], info["where"][0]))
                    print("MISMATCH? %s stored %r but plays %r  %s"
                          % (vid, label[:40], r["title"][:40], info["where"][0]))
        if i % 50 == 49:
            print("  ...%d/%d checked" % (i + 1, len(ids)), flush=True)
        time.sleep(0.15)

    lines = ["# YouTube link audit — %s" % time.strftime("%d %b %Y %H:%M"),
             "", "%d references, %d distinct videos checked: %d alive, %d DEAD, "
             "%d title mismatches flagged" % (len(refs), len(ids), ok, len(dead),
                                              len(mismatched)), ""]
    if dead:
        lines.append("## Dead (fix these)")
        for vid, info, err in dead:
            lines.append("- `%s` — %s — %s" % (vid, "; ".join(info["where"][:4]), err))
    if mismatched:
        lines.append("\n## Possible wrong video (title shares no words with our label)")
        for vid, label, title, where in mismatched:
            lines.append("- `%s` at %s — stored %r, actually plays %r"
                         % (vid, where, label, title))
    io.open(os.path.join(HERE, "_yt_audit_report.md"), "w", encoding="utf-8") \
        .write("\n".join(lines))
    io.open(os.path.join(HERE, "_yt_audit_report.json"), "w", encoding="utf-8") \
        .write(json.dumps({"dead": [[v, i["where"]] for v, i, _ in dead],
                           "mismatched": mismatched}))
    print("\n%d alive, %d dead, %d mismatch-flagged — report: scripts/_yt_audit_report.md"
          % (ok, len(dead), len(mismatched)))
    sys.exit(1 if dead else 0)


if __name__ == "__main__":
    main()
