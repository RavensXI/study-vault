# -*- coding: utf-8 -*-
"""Music Eduqas activation (EDUQAS_BUILD_PLAN.md Phase 1): subject row +
eight units with accents/subtitles/body classes + quote ticker +
practice_units. Free tier: school_id NULL, subject live, lessons will land
pending_review. Neutral phrasing: no board name in any student-facing text.
"""
import json
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
     "#b45309", "unit-music-eduqas-listening", True),
    (2, "aos1-forms-and-devices", "Area of Study 1: Musical Forms and Devices",
     "Binary, ternary, rondo and variations — and the devices that build them",
     "#b45309", "unit-music-eduqas-aos1", False),
    (3, "forms-devices-listening", "Area of Study 1: Listening Practice",
     "Real recordings, exam-style questions on forms and devices",
     "#7c3aed", "unit-music-eduqas-aos1-listening", True),
    (4, "aos2-music-for-ensemble", "Area of Study 2: Music for Ensemble",
     "Texture and sonority: jazz, musical theatre and chamber music",
     "#0f766e", "unit-music-eduqas-aos2", False),
    (5, "aos3-film-music", "Area of Study 3: Film Music",
     "How composers score mood, character, time and place",
     "#be123c", "unit-music-eduqas-aos3", False),
    (6, "aos4-popular-music", "Area of Study 4: Popular Music",
     "Pop forms and hooks, bhangra and fusion — and the study track",
     "#7c3aed", "unit-music-eduqas-aos4", False),
    (7, "ensemble-film-pop-listening", "Areas of Study 2–4: Listening Practice",
     "Unfamiliar extracts across ensemble, film and popular music",
     "#7c3aed", "unit-music-eduqas-aos-listening", True),
    (8, "score-reading", "Score Reading",
     "Follow the music on the page while it plays",
     "#0891b2", "unit-music-eduqas-score", True),
]


def main():
    sb = get_client()
    existing = sb.table("subjects").select("id").eq("slug", "music-eduqas").execute().data
    assert not existing, "music-eduqas already exists — aborting"

    aqa = sb.table("subjects").select("settings,color,detail").eq("slug", "music-aqa") \
        .execute().data[0]
    ticker = (aqa.get("settings") or {}).get("quote_ticker_html", "")

    subject = {
        "slug": "music-eduqas", "name": "Music", "exam_board": "Eduqas",
        "spec_code": "C660QS", "school_id": None, "status": "live",
        "is_active": True, "color": aqa.get("color"),
        "detail": "Forms and devices, music for ensemble, film music and "
                  "popular music — with listening practice and score reading "
                  "built for the exam.",
        "settings": {
            "practice_units": ["listening-skills", "score-reading",
                               "forms-devices-listening",
                               "ensemble-film-pop-listening"],
            "quote_ticker_html": ticker,
        },
    }
    print("subject:", subject["slug"], "|", subject["name"], subject["exam_board"])
    for so, slug, name, sub, accent, body, practice in UNITS:
        print("  unit %d %-28s %s %s" % (so, slug, accent, "practice" if practice else "article"))

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
