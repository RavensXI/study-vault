# -*- coding: utf-8 -*-
"""Validate and wire the AoS article lessons written by the content agents.

Validation is not a formality here. The agents were told never to invent a
claim about a recording, so the check that matters is the URL whitelist: an
extract we did not verify must not reach a student. Everything else (entity
rules, question shapes, narration ids, no inline styles) is the standard
content contract.

Usage:
    python scripts/music-practice/wire_aos_articles.py --dry-run
    python scripts/music-practice/wire_aos_articles.py
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from lib.supabase_client import get_client

BUILD = r"C:\Users\tshau\.claude\jobs\4059242c\tmp\build"
DRY = "--dry-run" in sys.argv
AUDIO_BASE = "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/"

# every extract a lesson is allowed to embed
ALLOWED = {AUDIO_BASE + "music-aqa/western-classical-1650-1910/" + f for f in
           ("lesson-01.mp3", "lesson-03.mp3", "lesson-04.mp3", "lesson-05.mp3",
            "lesson-06.mp3", "lesson-07.mp3", "lesson-07b.mp3", "lesson-08.mp3",
            "mozart-40-mvt1.mp3")} | {
    AUDIO_BASE + "music-aqa/aos-listening/" + f for f in
    ("aos2_broadway_ballad.mp3", "aos2_film_score.mp3", "aos2_game_music.mp3",
     "aos2_pop_dance.mp3", "aos2_rock_shuffle.mp3", "aos3_blues.mp3",
     "aos3_british_folk.mp3", "aos3_caribbean_fusion.mp3", "aos3_folk_fiddle.mp3",
     "aos3_latin.mp3", "aos3_latin_coro.mp3", "aos4_pastoral_orchestral.mp3",
     "aos4_sacred_static.mp3", "gershwin_rhapsody.mp3", "prokofiev_march.mp3",
     "respighi_catacomb.mp3")}
ALLOWED_LINKS = {"Gjwu4F8pqj0", "_LYv64v6hRY", "oY3lGUOvi2A", "kPDsw98Ax3I",
                 "bekh-sZ0-A8", "1oOmUi4HGt0", "AVfAoNHjTHQ", "NcND9dlwpC4",
                 "YmVZb8BNP38", "OaQkHeK3j8U", "97EX3LLQ33M", "h1SbxDUSJeI",
                 "M5FE2Udxm7o"}
ENTITY = re.compile(r"&(?:[a-zA-Z]+|#\d+);")

UNITS = {
    "aos1-western-classical": {
        "name": "Area of Study 1: Western Classical Tradition 1650\u20131910",
        "subtitle": "The orchestra, the structures and the set study piece \u2014 with "
                    "extracts to hear each one.",
        "accent": "#b45309", "sort_order": 2,
        "lessons": [("aos1_l01", 1), ("aos1_l02", 2), ("aos1_l03", 3)],
    },
    "aos2-popular-music": {
        "name": "Area of Study 2: Popular Music",
        "subtitle": "Rock, pop, and music written for stage, screen and games.",
        "accent": "#be123c", "sort_order": 4,
        "lessons": [("aos2_l01", 1), ("aos2_l02", 2)],
    },
    "aos4-since-1910": {
        "name": "Area of Study 4: Western Classical Tradition since 1910",
        "subtitle": "Twentieth-century colour, the Bart\u00f3k study piece, and minimalism.",
        "accent": "#7c3aed", "sort_order": 6,
        "lessons": [("aos4_l01", 1), ("aos4_l02", 2), ("aos4_l03", 3)],
    },
}
# article units before their drills, foundations first
RESORT = {"listening-skills": 1, "western-classical-1650-1910": 3,
          "aos3-traditional-music": 5, "aos-listening": 7, "score-reading": 8}


def validate(key, d):
    errs = []
    for f in ("title", "description", "content_html", "glossary_terms",
              "knowledge_checks", "practice_questions"):
        if not d.get(f):
            errs.append("missing %s" % f)
    if errs:
        return errs
    html = d["content_html"]

    for url in re.findall(r'<audio[^>]+src="([^"]+)"', html):
        if url not in ALLOWED:
            errs.append("UNVERIFIED AUDIO: %s" % url)
    for href in re.findall(r'href="(https://www\.youtube\.com/watch\?v=([^"&]+))[^"]*"', html):
        if href[1] not in ALLOWED_LINKS:
            errs.append("unverified link: %s" % href[1])
    if re.search(r'\sstyle="', html):
        errs.append("inline style attribute present")
    if "border-left" in html:
        errs.append("left-border stripe present")

    ids = re.findall(r'data-narration-id="n(\d+)"', html)
    if len(ids) != len(set(ids)):
        errs.append("duplicate narration ids")
    if not ids:
        errs.append("no narration ids")

    for fig in re.findall(r'<figure class="sv-listen".*?</figure>', html, re.S):
        if 'class="sv-listen-player"' not in fig or "<audio" not in fig:
            errs.append("malformed sv-listen figure")

    kc = d["knowledge_checks"]
    if len(kc) != 5:
        errs.append("knowledge_checks: %d (want 5)" % len(kc))
    for q in kc:
        if len(q.get("options") or []) != 4:
            errs.append("kc options != 4: %s" % q.get("q", "")[:40])
        if not isinstance(q.get("correct"), int) or not 0 <= q["correct"] < 4:
            errs.append("kc correct index bad: %s" % q.get("q", "")[:40])
        if "answers" in q:
            errs.append("kc uses answers[] - must be correct+options")
    if len(d["practice_questions"]) != 6:
        errs.append("practice_questions: %d (want 6)" % len(d["practice_questions"]))

    # plain-text fields must not carry HTML entities
    plain = [d["description"]]
    plain += [t["term"] for t in d["glossary_terms"]] + \
             [t["definition"] for t in d["glossary_terms"]]
    for q in kc:
        plain += [q["q"]] + list(q["options"])
    for q in d["practice_questions"]:
        plain += [q.get("text", ""), q.get("type", ""), q.get("marks", "")]
    for s in plain:
        if ENTITY.search(s or ""):
            errs.append("HTML entity in plain-text field: %s" % (s or "")[:50])
            break
    return errs


def main():
    docs = {}
    for slug, spec in UNITS.items():
        for key, _n in spec["lessons"]:
            path = os.path.join(BUILD, key + ".json")
            if not os.path.exists(path):
                print("MISSING FILE:", path)
                continue
            docs[key] = json.load(io.open(path, encoding="utf-8"))

    bad = 0
    for key, d in sorted(docs.items()):
        errs = validate(key, d)
        n_audio = d["content_html"].count("<audio")
        n_links = d["content_html"].count("sv-listen-links")
        print("%-10s %-52s audio=%d links=%d  %s"
              % (key, d["title"][:52], n_audio, n_links,
                 "OK" if not errs else "FAIL"))
        for e in errs:
            print("      - %s" % e)
            bad += 1
    if bad:
        sys.exit("\n%d validation problem(s) - nothing written" % bad)
    print("\nall %d lessons valid" % len(docs))
    if DRY:
        print("dry run - nothing written")
        return

    sb = get_client()
    subj = sb.from_("subjects").select("id, settings").eq("slug", "music-aqa") \
             .is_("school_id", "null").execute().data[0]

    for slug, spec in UNITS.items():
        existing = sb.from_("units").select("id").eq("subject_id", subj["id"]) \
                     .eq("slug", slug).execute().data
        if existing:
            unit_id = existing[0]["id"]
            sb.from_("units").update({"sort_order": spec["sort_order"]}) \
              .eq("id", unit_id).execute()
        else:
            unit_id = sb.from_("units").insert({
                "subject_id": subj["id"], "slug": slug, "name": spec["name"],
                "subtitle": spec["subtitle"], "body_class": "unit-music-aqa-" + slug,
                "accent": spec["accent"], "accent_light": spec["accent"] + "22",
                "accent_badge": spec["accent"] + "33",
                "lesson_count": len(spec["lessons"]),
                "sort_order": spec["sort_order"],
            }).execute().data[0]["id"]
            print("unit created:", slug)
        for key, n in spec["lessons"]:
            d = docs[key]
            row = {"unit_id": unit_id, "lesson_number": n, "slug": "lesson-%02d" % n,
                   "title": d["title"], "description": d["description"],
                   "status": "pending_review", "tier": "both",
                   "content_html": d["content_html"],
                   "exam_tip_html": d.get("exam_tip_html"),
                   "conclusion_html": d.get("conclusion_html"),
                   "glossary_terms": d["glossary_terms"],
                   "knowledge_checks": d["knowledge_checks"],
                   "practice_questions": d["practice_questions"]}
            old = sb.from_("lessons").select("id").eq("unit_id", unit_id) \
                    .eq("lesson_number", n).execute().data
            if old:
                sb.from_("lessons").update(row).eq("id", old[0]["id"]).execute()
                print("  updated %s L%02d" % (slug, n))
            else:
                sb.from_("lessons").insert(row).execute()
                print("  inserted %s L%02d" % (slug, n))

    for slug, order in RESORT.items():
        u = sb.from_("units").select("id").eq("subject_id", subj["id"]) \
              .eq("slug", slug).execute().data
        if u:
            sb.from_("units").update({"sort_order": order}).eq("id", u[0]["id"]).execute()
    print("unit order updated: foundations, then each area of study, then drills")


if __name__ == "__main__":
    main()
