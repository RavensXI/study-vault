# -*- coding: utf-8 -*-
"""Move the curated performances INTO the lesson copy (Tom, 16 Aug).

The first wiring put them in the sidebar video slot — but that slot is
reserved for the NotebookLM explainer when it is generated. What Tom wants:
each performance embedded in the flow of the lesson, at the section that
discusses it.

This script:
  1. Reverts the sidebar youtube_video_id and related_media writes on the
     four lessons (back to empty, as they were).
  2. Inserts a responsive <figure class="sv-embed"> YouTube iframe after the
     matching section heading in content_html (or before, for the one
     end-of-section placement).

Embeds are interactive media, not prose, so narration needs no change.
Backup: _backup_body_embeds_2026-08-16.json (content_html + the two
reverted fields). Run: python embed_videos_in_body.py [--apply]
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

APPLY = "--apply" in sys.argv
BACKUP = os.path.join(HERE, "_backup_body_embeds_2026-08-16.json")


def fig(vid, title, cap):
    return ('<figure class="sv-embed"><div class="sv-embed-frame">'
            '<iframe src="https://www.youtube.com/embed/%s" title="%s" '
            'loading="lazy" allow="fullscreen" allowfullscreen></iframe></div>'
            '<figcaption class="sv-embed-cap">%s</figcaption></figure>' % (vid, title, cap))


# (unit, lesson) -> list of (heading-text-to-match, position, embed html)
EMBEDS = {
    ("aos4-since-1910", 1): [
        ("Open Space versus Dense Texture", "after",
         fig("Q3aUMKrCh8Q", "Copland — Appalachian Spring (score video)",
             "Watch with the score: Copland &mdash; <em>Appalachian Spring</em>. "
             "Hear how much air sits between the parts.")),
    ],
    ("aos4-since-1910", 2): [
        ("The four movements you need", "after",
         fig("DQHa1YZzlDY", "Bartók — Hungarian Sketches (complete)",
             "Listen: Bart&oacute;k &mdash; <em>Hungarian Sketches</em>, complete. "
             "Follow the movements as you read about each one.")),
        ("Slightly Tipsy (Movement 4)", "after",
         fig("oY3lGUOvi2A", "Bartók — Slightly Tipsy (Chicago Symphony Orchestra)",
             "Listen: &lsquo;Slightly Tipsy&rsquo; on its own &mdash; snap rhythms "
             "and a deliberately unsteady pulse.")),
    ],
    ("aos4-since-1910", 3): [
        ("The additive process, and how In C differs &mdash; Terry Riley", "after",
         fig("qzmi7Wm10Y0", "Terry Riley — In C, live at Millennium Park",
             "Watch: Riley &mdash; <em>In C</em>. Dozens of players move through "
             "the same 53 cells at their own pace.")),
        ("Phasing and gradual change &mdash; Steve Reich", "after",
         fig("liYkRarIDfo", "Steve Reich — Clapping Music (London Sinfonietta)",
             "Watch: Reich &mdash; <em>Clapping Music</em>. Two performers, one "
             "pattern, one of them shifting a quaver at a time.")),
        ("Layering and texture &mdash; John Adams", "after",
         fig("5LoUm_r7It8", "John Adams — Short Ride in a Fast Machine (BBC Proms)",
             "Watch: Adams &mdash; <em>Short Ride in a Fast Machine</em>. Four and "
             "a half minutes of layered, pulsing orchestra.")),
        ("Why this matters in the exam", "before",
         fig("ZXJWO2FQ16c", "Steve Reich — Music for 18 Musicians (full performance)",
             "Go deeper: Reich &mdash; <em>Music for 18 Musicians</em>, a full hour "
             "of interlocking pulse and slowly breathing texture.")),
    ],
    ("aos2-popular-music", 4): [
        ("Rock of the 1960s and 1970s", "after",
         fig("Yjyj8qnqkYI", "The Beatles — A Hard Day's Night",
             "Listen: The Beatles &mdash; <em>A Hard Day&rsquo;s Night</em> (1964). "
             "Live kit, jangling guitars, close vocal harmony &mdash; the sixties "
             "sound.")),
        ("Pop from the 1990s to now", "after",
         fig("C-u5WLJ9Yk4", "Britney Spears — …Baby One More Time",
             "Listen: Britney Spears &mdash; <em>&hellip;Baby One More Time</em> "
             "(1998). Drum machine, synth bass, studio-processed vocals &mdash; "
             "the production IS the date.")),
        ("Broadway from the 1950s to the 1990s", "after",
         fig("cuI5ATKPvp0", "West Side Story (1961) — key scenes",
             "Watch: <em>West Side Story</em> (1961). Full pit orchestra, brassy "
             "stabs, Latin percussion, trained theatre voices.")),
        ("Film and gaming music from the 1990s", "after",
         fig("lDlU08RU7Tk", "Theme From Jurassic Park",
             "Listen: John Williams &mdash; <em>Jurassic Park</em> (1993). A full "
             "orchestra scoring wonder &mdash; the sound of the modern blockbuster.")),
    ],
}


def main():
    sb = get_client()
    subj = [s for s in sb.table("subjects").select("id,slug").execute().data
            if s["slug"] == "music-aqa"][0]["id"]
    units = {u["slug"]: u["id"] for u in sb.table("units").select("id,slug,subject_id")
             .execute().data if u["subject_id"] == subj}

    backup, writes = {}, []
    for (uslug, num), inserts in EMBEDS.items():
        row = sb.table("lessons").select("id,content_html,youtube_video_id,related_media") \
            .eq("unit_id", units[uslug]).eq("lesson_number", num).execute().data[0]
        backup["%s/%d" % (uslug, num)] = {
            "id": row["id"], "content_html": row["content_html"],
            "youtube_video_id": row["youtube_video_id"],
            "related_media": row["related_media"]}
        html = row["content_html"]
        assert "sv-embed" not in html, "%s L%d already has embeds" % (uslug, num)
        for head, pos, embed in inserts:
            m = re.search(r"<h[23][^>]*>\s*%s\s*</h[23]>" % re.escape(head), html)
            assert m, "heading not found: %s L%d %r" % (uslug, num, head)
            at = m.start() if pos == "before" else m.end()
            html = html[:at] + embed + html[at:]
            print("%s L%d: embed %s %r" % (uslug, num, pos, head[:45]))
        writes.append((row["id"], {"content_html": html,
                                   "youtube_video_id": None,
                                   "related_media": []}))
    print("lessons touched: %d, embeds: %d"
          % (len(writes), sum(len(v) for v in EMBEDS.values())))

    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    if not os.path.exists(BACKUP):
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup))
    for lid, upd in writes:
        sb.table("lessons").update(upd).eq("id", lid).execute()
    print("applied. backup:", BACKUP)


if __name__ == "__main__":
    main()
