# -*- coding: utf-8 -*-
"""Wire the approved YouTube curation (Tom, 16 Aug: "wire it all, vic firth
included").

Sidebar picks -> lessons.youtube_video_id (bare video id per the documented
loader contract). The rest -> related_media, using the live category-grouped
shape {category, items:[{url,title,description}]}.

Every id was oEmbed-verified (exists + embeddable) and channel-checked on
15 Aug. Backup: _backup_youtube_wiring_2026-08-16.json.
Run: python wire_youtube_curation.py [--apply]
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

APPLY = "--apply" in sys.argv
BACKUP = os.path.join(HERE, "_backup_youtube_wiring_2026-08-16.json")

Y = "https://www.youtube.com/watch?v="

SIDEBAR = {
    ("aos2-popular-music", 4): "lDlU08RU7Tk",   # Jurassic Park theme (UMG)
    ("aos4-since-1910", 1): "Q3aUMKrCh8Q",      # Appalachian Spring score video
    ("aos4-since-1910", 2): "DQHa1YZzlDY",      # Hungarian Sketches complete
    ("aos4-since-1910", 3): "5LoUm_r7It8",      # Short Ride, BBC Proms 2014
}

RELATED = {
    ("aos2-popular-music", 4): [{
        "category": "Listen by Era",
        "items": [
            {"url": Y + "Yjyj8qnqkYI",
             "title": "The Beatles — A Hard Day's Night (1964)",
             "description": "1960s rock: live drum kit, jangling electric guitars and "
                            "close vocal harmony with no studio polish — the sound that "
                            "places a track in the sixties."},
            {"url": Y + "C-u5WLJ9Yk4",
             "title": "Britney Spears — …Baby One More Time (1998)",
             "description": "1990s pop: drum machine, synth bass and studio-processed "
                            "vocals. Compare the production with the Beatles track and "
                            "the difference IS the date."},
            {"url": Y + "cuI5ATKPvp0",
             "title": "West Side Story (1961) — key scenes",
             "description": "Mid-century Broadway: full pit orchestra, brassy stabs, "
                            "Latin percussion and trained theatre voices — the sound "
                            "world of the classic musical."},
        ],
    }],
    ("aos4-since-1910", 2): [{
        "category": "Listening Examples",
        "items": [
            {"url": Y + "oY3lGUOvi2A",
             "title": "Bartók — Hungarian Sketches: IV. Slightly Tipsy (Chicago SO)",
             "description": "The unsteady, lurching movement on its own — listen for "
                            "the snap rhythms and the deliberately wrong-footed pulse."},
        ],
    }],
    ("aos4-since-1910", 3): [{
        "category": "Listening Examples",
        "items": [
            {"url": Y + "liYkRarIDfo",
             "title": "Steve Reich — Clapping Music (London Sinfonietta)",
             "description": "Phasing at its barest: two performers, one pattern, one of "
                            "them shifting a quaver at a time. Watch it happen."},
            {"url": Y + "qzmi7Wm10Y0",
             "title": "Terry Riley — In C, live at Millennium Park",
             "description": "The additive process in the wild: dozens of players moving "
                            "through the same 53 cells at their own pace."},
            {"url": Y + "ZXJWO2FQ16c",
             "title": "Steve Reich — Music for 18 Musicians (eighth blackbird, full)",
             "description": "A full hour of interlocking pulse and slowly breathing "
                            "texture — layering on the largest scale on your course."},
        ],
    }],
}


def main():
    sb = get_client()
    subj = [s for s in sb.table("subjects").select("id,slug").execute().data
            if s["slug"] == "music-aqa"][0]["id"]
    units = {u["slug"]: u["id"] for u in sb.table("units").select("id,slug,subject_id")
             .execute().data if u["subject_id"] == subj}

    backup, writes = {}, []
    targets = set(list(SIDEBAR) + list(RELATED))
    for (uslug, num) in sorted(targets):
        row = sb.table("lessons").select("id,youtube_video_id,related_media") \
            .eq("unit_id", units[uslug]).eq("lesson_number", num).execute().data[0]
        backup["%s/%d" % (uslug, num)] = {"id": row["id"],
                                          "youtube_video_id": row["youtube_video_id"],
                                          "related_media": row["related_media"]}
        upd = {}
        if (uslug, num) in SIDEBAR:
            assert not row["youtube_video_id"], "slot not empty: %s L%d" % (uslug, num)
            upd["youtube_video_id"] = SIDEBAR[(uslug, num)]
        if (uslug, num) in RELATED:
            existing = row["related_media"] or []
            assert not existing, "related_media not empty: %s L%d" % (uslug, num)
            upd["related_media"] = RELATED[(uslug, num)]
        writes.append((row["id"], uslug, num, upd))
        print("%s L%d: %s" % (uslug, num, ", ".join(
            ("sidebar=" + v) if k == "youtube_video_id" else
            ("related: %d item(s)" % sum(len(c["items"]) for c in v))
            for k, v in upd.items())))

    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    if not os.path.exists(BACKUP):
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup))
    for lid, uslug, num, upd in writes:
        sb.table("lessons").update(upd).eq("id", lid).execute()
    print("applied. backup:", BACKUP)


if __name__ == "__main__":
    main()
