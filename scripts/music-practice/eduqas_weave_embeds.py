# -*- coding: utf-8 -*-
"""Replace the study lessons' <!-- EMBED: key --> markers with the
oEmbed-verified official performance figures (same sv-embed markup as the
AoS4 in-body embeds).

  badinerie -> Netherlands Bach Society, BsiqjGgwuU8
  africa    -> TotoVEVO official video, FTQbiNvZqaY

Run: python eduqas_weave_embeds.py [--apply]
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

APPLY = "--apply" in sys.argv

EMBEDS = {
    "badinerie": ("BsiqjGgwuU8", "Bach — Badinerie (Netherlands Bach Society)",
                  "Watch: the Badinerie performed on Baroque instruments &mdash; "
                  "flute leading, strings and harpsichord continuo behind."),
    "africa": ("FTQbiNvZqaY", "Toto — Africa (Official HD Video)",
               "Watch: the official video. Listen for the layered keyboards, "
               "the half-time drum groove and the lifted chorus harmony."),
}


def fig(vid, title, cap):
    return ('<figure class="sv-embed"><div class="sv-embed-frame">'
            '<iframe src="https://www.youtube.com/embed/%s" title="%s" '
            'loading="lazy" allow="fullscreen" allowfullscreen></iframe></div>'
            '<figcaption class="sv-embed-cap">%s</figcaption></figure>' % (vid, title, cap))


def main():
    sb = get_client()
    sub = sb.table("subjects").select("id").eq("slug", "music-eduqas").execute().data[0]["id"]
    units = [u for u in sb.table("units").select("id,slug,subject_id").execute().data
             if u["subject_id"] == sub]
    woven = 0
    for u in units:
        rows = sb.table("lessons").select("id,lesson_number,content_html") \
            .eq("unit_id", u["id"]).execute().data
        for l in rows:
            ch = l.get("content_html") or ""
            if "<!-- EMBED:" not in ch:
                continue
            new = ch
            for key, (vid, title, cap) in EMBEDS.items():
                new = re.sub(r"<!--\s*EMBED:\s*%s\s*-->" % key, fig(vid, title, cap), new)
            leftover = re.findall(r"<!--\s*EMBED:[^>]*-->", new)
            print("%s L%d: woven%s" % (u["slug"], l["lesson_number"],
                                       " | UNKNOWN MARKERS: %s" % leftover if leftover else ""))
            if APPLY and new != ch and not leftover:
                sb.table("lessons").update({"content_html": new}).eq("id", l["id"]).execute()
                woven += 1
    print("%s %d lesson(s)" % ("wove" if APPLY else "would weave", woven))


if __name__ == "__main__":
    main()
