# -*- coding: utf-8 -*-
"""Music Edexcel activation (EDEXCEL_BUILD_PLAN.md Phase 1): subject row + eight
units with accents/subtitles/body classes + quote ticker + practice_units.
Free tier: school_id NULL, subject live, lessons land pending_review.
No board names in any student-facing text.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

APPLY = "--apply" in sys.argv

UNITS = [
    (1, "listening-skills", "Listening Skills",
     "Train your ear: tonality, metre, texture, devices and cadences",
     "#b45309", "unit-music-edexcel-listening", True),
    (2, "aos1-instrumental-music", "Area of Study 1: Instrumental Music 1700–1820",
     "Bach's Brandenburg No. 5 and Beethoven's 'Pathétique' — two set works in close-up",
     "#0f766e", "unit-music-edexcel-aos1", False),
    (3, "aos2-vocal-music", "Area of Study 2: Vocal Music",
     "Purcell's Music for a While and Queen's Killer Queen",
     "#be123c", "unit-music-edexcel-aos2", False),
    (4, "aos3-stage-and-screen", "Area of Study 3: Music for Stage and Screen",
     "Defying Gravity and the Star Wars Main Title",
     "#7c3aed", "unit-music-edexcel-aos3", False),
    (5, "aos4-fusions", "Area of Study 4: Fusions",
     "Afro Celt Sound System's Release and Esperanza Spalding's Samba Em Preludio",
     "#b45309", "unit-music-edexcel-aos4", False),
    (6, "unfamiliar-listening", "Unfamiliar Listening Practice",
     "Real recordings and exam-style questions — the comparison-question muscle",
     "#7c3aed", "unit-music-edexcel-unfamiliar", True),
    (7, "score-reading", "Score Reading",
     "Follow the music on the page while it plays",
     "#0891b2", "unit-music-edexcel-score", True),
]


def main():
    sb = get_client()
    existing = sb.table("subjects").select("id").eq("slug", "music-edexcel").execute().data
    assert not existing, "music-edexcel already exists — aborting"

    aqa = sb.table("subjects").select("settings,color,detail").eq("slug", "music-aqa") \
        .execute().data[0]
    ticker = (aqa.get("settings") or {}).get("quote_ticker_html", "")

    subject = {
        "slug": "music-edexcel", "name": "Music", "exam_board": "Edexcel",
        "spec_code": "1MU0", "school_id": None, "status": "live",
        "is_active": True, "color": aqa.get("color"),
        "detail": "The concerto through time, rhythms of the world, film "
                  "music and conventions of pop — with listening practice "
                  "and score reading built for the exam.",
        "settings": {
            "practice_units": ["listening-skills", "score-reading",
                               "unfamiliar-listening"],
            "quote_ticker_html": ticker,
        },
    }
    print("subject:", subject["slug"], "|", subject["name"], subject["exam_board"])
    for so, slug, name, sub, accent, body, practice in UNITS:
        print("  unit %d %-30s %s %s" % (so, slug, accent,
                                         "practice" if practice else "article"))

    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    r = sb.table("subjects").insert(subject).execute()
    sid = r.data[0]["id"]
    for so, slug, name, sub, accent, body, practice in UNITS:
        sb.table("units").insert({
            "subject_id": sid, "slug": slug, "name": name, "subtitle": sub,
            "sort_order": so, "accent": accent, "accent_light": accent + "22",
            "accent_badge": accent + "33", "body_class": body,
        }).execute()
    chk = sb.table("units").select("slug").eq("subject_id", sid).execute().data
    print("created subject %s with %d units" % (sid, len(chk)))


if __name__ == "__main__":
    main()
