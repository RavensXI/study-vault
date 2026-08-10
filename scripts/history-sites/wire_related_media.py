# -*- coding: utf-8 -*-
"""Related media for the five site lessons. Every URL in this file was
live-verified (HTTP 200) on 2026-08-06 before insert; the podcast entry is
added later by the podcast pipeline as usual."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

SITE = "&#127963;"  # classical building

MEDIA = {
    ("history-aqa", "Norman England", 13): [
        {"emoji": SITE, "category": "Explore the Site", "items": [
            {"url": "https://www.english-heritage.org.uk/visit/places/1066-battle-of-hastings-abbey-and-battlefield/",
             "title": "English Heritage &mdash; 1066 Battle of Hastings, Abbey and Battlefield",
             "description": "The site itself: visit information, battlefield walks and the abbey built on the spot where Harold fell."},
            {"url": "https://www.english-heritage.org.uk/visit/places/1066-battle-of-hastings-abbey-and-battlefield/history-and-stories/what-happened-battle-hastings/",
             "title": "English Heritage &mdash; What Happened at the Battle of Hastings",
             "description": "The battle told by the site&rsquo;s custodians, with the ridge, the charges and the feigned retreats mapped to the ground."},
            {"url": "https://www.bayeuxmuseum.com/en/the-bayeux-tapestry/",
             "title": "Bayeux Museum &mdash; The Bayeux Tapestry",
             "description": "The tapestry online &mdash; the nearest thing to a contemporary picture of the battle your exam is about."},
        ]},
    ],
    ("history-aqa", "Medieval England", 12): [
        {"emoji": SITE, "category": "Explore the Site", "items": [
            {"url": "https://www.nationalwallacemonument.com/",
             "title": "The National Wallace Monument",
             "description": "Stands on Abbey Craig, the crag from which Wallace and Moray watched the English crossing."},
            {"url": "http://portal.historicenvironment.scot/designation/BTL20",
             "title": "Historic Environment Scotland &mdash; Battle of Stirling Bridge",
             "description": "The official battlefield inventory record: the designated site, its landscape and what survives."},
        ]},
    ],
    ("history-aqa", "Elizabethan England", 13): [
        {"emoji": SITE, "category": "Explore the Site", "items": [
            {"url": "https://www.rmg.co.uk/stories/royal-history/elizabeth-i-spanish-armada",
             "title": "Royal Museums Greenwich &mdash; Elizabeth I and the Spanish Armada",
             "description": "The campaign from the museum that holds the Armada Portrait &mdash; commanders, fleets and the fireships."},
            {"url": "https://www.rmg.co.uk/collections/objects/rmgc-object-11755",
             "title": "RMG &mdash; Launch of Fireships against the Spanish Armada painting",
             "description": "A near-contemporary painting of the night attack at Calais &mdash; the moment this lesson turns on."},
        ]},
    ],
    ("history-aqa", "Restoration England", 13): [
        {"emoji": SITE, "category": "Explore the Site", "items": [
            {"url": "https://www.english-heritage.org.uk/visit/places/upnor-castle/",
             "title": "English Heritage &mdash; Upnor Castle",
             "description": "The Elizabethan gun fort that put up the raid&rsquo;s stiffest resistance &mdash; still facing the Medway moorings."},
            {"url": "https://www.rijksmuseum.nl/en/collection/NG-MC-239",
             "title": "Rijksmuseum &mdash; Stern of the Royal Charles",
             "description": "The captured flagship&rsquo;s carved stern in Amsterdam &mdash; the raid&rsquo;s most famous relic."},
            {"url": "https://thedockyard.co.uk/",
             "title": "The Historic Dockyard Chatham",
             "description": "The dockyard the chain was protecting &mdash; England&rsquo;s premier naval arsenal in 1667, open to visit today."},
        ]},
    ],
    ("history", "Elizabethan England", 16): [
        {"emoji": SITE, "category": "Explore the Site", "items": [
            {"url": "https://www.rmg.co.uk/stories/royal-history/queen-elizabeth-speech-troops-tilbury",
             "title": "Royal Museums Greenwich &mdash; Elizabeth&rsquo;s Speech at Tilbury",
             "description": "The famous speech in context &mdash; delivered while the Armada was already limping north."},
            {"url": "https://www.rmg.co.uk/collections/objects/rmgc-object-11755",
             "title": "RMG &mdash; Launch of Fireships against the Spanish Armada painting",
             "description": "Your hero image in full &mdash; the night at Calais that broke the crescent."},
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
    n = sum(len(g["items"]) for g in media)
    print("wired %s L%d: %d links" % (slug, num, n))
print("done")
