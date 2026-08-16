# -*- coding: utf-8 -*-
"""Music OCR activation (OCR_BUILD_PLAN.md Phase 1): subject row + eight
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
     "#b45309", "unit-music-ocr-listening", True),
    (2, "aos2-the-concerto-through-time",
     "Area of Study 2: The Concerto Through Time",
     "The concerto from 1650 to 1910: Baroque, Classical and Romantic",
     "#0f766e", "unit-music-ocr-aos2", False),
    (3, "aos2-concerto-listening", "Area of Study 2: Listening Practice",
     "Real recordings from the concerto's era, exam-style questions",
     "#7c3aed", "unit-music-ocr-aos2-listening", True),
    (4, "aos3-rhythms-of-the-world", "Area of Study 3: Rhythms of the World",
     "Traditional rhythms of India and Punjab, the Eastern Mediterranean, "
     "Africa and the Americas",
     "#b45309", "unit-music-ocr-aos3", False),
    (5, "aos4-film-music", "Area of Study 4: Film Music",
     "Scoring mood, character and action — for screen and video games",
     "#be123c", "unit-music-ocr-aos4", False),
    (6, "aos5-conventions-of-pop", "Area of Study 5: Conventions of Pop",
     "Rock 'n' roll to solo artists: pop conventions from the 1950s to now",
     "#7c3aed", "unit-music-ocr-aos5", False),
    (7, "aos45-unfamiliar-listening", "Areas of Study 4–5: Listening Practice",
     "Unfamiliar extracts: film colours, band textures and pop",
     "#7c3aed", "unit-music-ocr-aos45-listening", True),
    (8, "score-reading", "Score Reading",
     "Follow the music on the page while it plays",
     "#0891b2", "unit-music-ocr-score", True),
]


def main():
    sb = get_client()
    existing = sb.table("subjects").select("id").eq("slug", "music-ocr").execute().data
    assert not existing, "music-ocr already exists — aborting"

    aqa = sb.table("subjects").select("settings,color,detail").eq("slug", "music-aqa") \
        .execute().data[0]
    ticker = (aqa.get("settings") or {}).get("quote_ticker_html", "")

    subject = {
        "slug": "music-ocr", "name": "Music", "exam_board": "OCR",
        "spec_code": "J536", "school_id": None, "status": "live",
        "is_active": True, "color": aqa.get("color"),
        "detail": "The concerto through time, rhythms of the world, film "
                  "music and conventions of pop — with listening practice "
                  "and score reading built for the exam.",
        "settings": {
            "practice_units": ["listening-skills", "score-reading",
                               "aos2-concerto-listening",
                               "aos45-unfamiliar-listening"],
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
