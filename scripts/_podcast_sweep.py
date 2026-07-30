# -*- coding: utf-8 -*-
"""Which LIVE free-tier article lessons still lack our Lesson Podcast?

The eyes of the nightly NLM dispatcher (daily_shorts_build.ps1): podcasts
take priority over shorts whenever this reports a backlog. A subject enters
this list the day its lessons flip to live — no one has to remember.

    python scripts/_podcast_sweep.py            # human-readable per subject
    python scripts/_podcast_sweep.py --total    # single integer, for the wrapper
    python scripts/_podcast_sweep.py --json     # {"subjects":[{"slug","pending"}],"total"}
"""
import json
import os
import sys
import urllib.request

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

SB_URL = os.environ["SUPABASE_URL"]
SB_KEY = os.environ["SUPABASE_SERVICE_KEY"]
MIN_CONTENT = 800  # chars of content_html below which a lesson can't sustain a podcast


def sq(path):
    r = urllib.request.Request(SB_URL + "/rest/v1/" + path,
                               headers={"apikey": SB_KEY, "Authorization": "Bearer " + SB_KEY})
    return json.load(urllib.request.urlopen(r))


def has_podcast(media):
    for cat in (media or []):
        if (cat.get("category") or "").lower() in ("podcasts", "podcast"):
            for item in cat.get("items", []):
                if item.get("title") == "Lesson Podcast" and item.get("url") and item["url"] != "#":
                    return True
    return False


def main():
    subs = {s["id"]: s["slug"] for s in
            sq("subjects?select=id,slug,status&school_id=is.null&status=eq.live&limit=500")}
    units = sq("units?select=id,subject_id&limit=2000")
    usub = {u["id"]: subs.get(u["subject_id"]) for u in units}

    counts = {}
    off = 0
    while True:
        page = sq("lessons?select=unit_id,status,related_media,content_html"
                  f"&status=eq.live&order=id&limit=500&offset={off}")
        for l in page:
            slug = usub.get(l["unit_id"])
            if not slug:
                continue
            if len(l.get("content_html") or "") < MIN_CONTENT:
                continue  # practice-format or stub — no podcast by design
            if has_podcast(l.get("related_media")):
                continue
            counts[slug] = counts.get(slug, 0) + 1
        if len(page) < 500:
            break
        off += 500

    ordered = sorted(counts.items(), key=lambda kv: kv[1])  # smallest first: finish subjects atomically
    total = sum(counts.values())
    if "--total" in sys.argv:
        print(total)
    elif "--json" in sys.argv:
        print(json.dumps({"subjects": [{"slug": s, "pending": n} for s, n in ordered],
                          "total": total}))
    else:
        for s, n in ordered:
            print(f"{n:>5}  {s}")
        print(f"{total:>5}  TOTAL")


if __name__ == "__main__":
    main()
