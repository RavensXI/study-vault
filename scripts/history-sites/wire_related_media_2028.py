# -*- coding: utf-8 -*-
"""Related media for the five 2028 site lessons. Every URL live-verified
(HTTP 200) on 2026-08-06. HRP's White Tower page 403s all automated fetchers,
so it is deliberately absent — never ship a URL we could not verify."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

SITE = "&#127963;"

MEDIA = {
    ("history-aqa", "Norman England", 14): [
        {"emoji": SITE, "category": "Explore the Site", "items": [
            {"url": "https://www.britannica.com/place/White-Tower-London",
             "title": "Britannica &mdash; The White Tower",
             "description": "The keep's construction, dimensions and history in brief &mdash; solid reference for dates and features."},
        ]},
    ],
    ("history-aqa", "Medieval England", 13): [
        {"emoji": SITE, "category": "Explore the Site", "items": [
            {"url": "https://www.english-heritage.org.uk/visit/places/acton-burnell-castle/",
             "title": "English Heritage &mdash; Acton Burnell Castle",
             "description": "The site itself: the red sandstone shell, its history and the parliament tradition, from its custodians."},
        ]},
    ],
    ("history-aqa", "Elizabethan England", 14): [
        {"emoji": SITE, "category": "Explore the Site", "items": [
            {"url": "https://www.english-heritage.org.uk/visit/places/kenilworth-castle/",
             "title": "English Heritage &mdash; Kenilworth Castle",
             "description": "The castle today: Leicester's Building, the gatehouse, the keep and the recreated garden."},
            {"url": "https://www.english-heritage.org.uk/visit/places/kenilworth-castle/history-and-stories/history/",
             "title": "English Heritage &mdash; History of Kenilworth Castle",
             "description": "The full story from Norman keep to slighting &mdash; with the 1575 visit at its centre."},
        ]},
    ],
    ("history-aqa", "Restoration England", 14): [
        {"emoji": SITE, "category": "Explore the Site", "items": [
            {"url": "https://www.stpauls.co.uk/history-collections",
             "title": "St Paul&rsquo;s Cathedral &mdash; History and Collections",
             "description": "The cathedral&rsquo;s own account of the Fire, Wren&rsquo;s rebuilding and the Great Model."},
        ]},
    ],
    ("history", "Elizabethan England", 17): [
        {"emoji": SITE, "category": "Explore the Site", "items": [
            {"url": "https://www.english-heritage.org.uk/visit/places/kenilworth-castle/elizabethan-garden/",
             "title": "English Heritage &mdash; The Elizabethan Garden",
             "description": "The garden rebuilt in 2009 from the Langham letter &mdash; your hero image, explained by its makers."},
            {"url": "https://www.english-heritage.org.uk/visit/places/kenilworth-castle/history-and-stories/elizabeth-and-dudley/",
             "title": "English Heritage &mdash; Elizabeth and Dudley",
             "description": "The courtship behind the nineteen days, told by the site&rsquo;s custodians."},
        ]},
    ],
}

sb = get_client()
for (slug, frag, num), media in MEDIA.items():
    generic = slug == "history-aqa"
    subs = sb.table("subjects").select("id,school_id").eq("slug", slug).execute().data
    sub = [s for s in subs if (s["school_id"] is None) == generic][0]
    unit = [u for u in sb.table("units").select("id,name").eq(
        "subject_id", sub["id"]).execute().data if frag in u["name"]][0]
    lesson = sb.table("lessons").select("id,related_media").eq(
        "unit_id", unit["id"]).eq("lesson_number", num).single().execute().data
    if lesson.get("related_media"):
        print("SKIP %s L%d: related_media already set" % (slug, num))
        continue
    sb.table("lessons").update({"related_media": media}).eq("id", lesson["id"]).execute()
    print("wired %s L%d: %d links" % (slug, num,
                                      sum(len(g["items"]) for g in media)))
print("done")
