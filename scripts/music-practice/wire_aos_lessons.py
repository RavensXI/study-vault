# -*- coding: utf-8 -*-
"""Wire the AoS2-4 listening drills into music-aqa as an 'aos-listening' unit.

Three lessons, one per area of study, in the same practice shape as the existing
listening-skills unit (passages / problem_bank / worked_examples / method_card /
exam_context). Idempotent: re-running updates in place.

Sources, and how each earns its place:
  batch 1+2 generated clips  - three-pass validated, then ruled on by ear
  public-domain recordings   - real US Marine Band / US Army Band performances,
                               identity true by provenance, features 3-vote
                               verified

Every lesson also links the official recordings for its strand, so a student can
hear the real repertoire the exam board names. We link those rather than host
them: the works themselves are still in copyright.

Usage: python scripts/music-practice/wire_aos_lessons.py [--dry-run]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from lib.supabase_client import get_client
from lib.r2 import get_r2_client, upload_bytes_to_r2, AUDIO_BUCKET, AUDIO_PUBLIC_URL
import batch1_bank
import batch2_bank
import pd_bank

DRY = "--dry-run" in sys.argv
UNIT_SLUG = "aos-listening"

LESSONS = {
    "aos2": {
        "n": 1, "slug": "lesson-01",
        "title": "Area of Study 2: Popular Music — Unfamiliar Listening",
        "desc": "Drill the styles AQA sets for popular music: rock and pop, music for "
                "stage and screen, and music for media.",
        "links": [
            ("Britten — The Young Person's Guide to the Orchestra (LSO)",
             "https://www.youtube.com/watch?v=M5FE2Udxm7o",
             "Not popular music, but the clearest demonstration of orchestral timbre "
             "you will find — useful before any listening paper."),
        ],
        "context": "Section A of the listening exam plays short unfamiliar extracts and asks "
                   "you to describe what you hear. These drills use the same question types.",
    },
    "aos3": {
        "n": 2, "slug": "lesson-02",
        "title": "Area of Study 3: Traditional Music — Unfamiliar Listening",
        "desc": "Blues, fusion taking in African and Caribbean influences, contemporary "
                "Latin music, and contemporary folk of the British Isles.",
        "links": [],
        "context": "AQA names four traditional styles for unfamiliar listening: blues from "
                   "1920–1950, fusion incorporating African and/or Caribbean music, "
                   "contemporary Latin music, and contemporary folk music of the British "
                   "Isles. Every extract here belongs to one of them.",
    },
    "aos4": {
        "n": 3, "slug": "lesson-03",
        "title": "Area of Study 4: Western Classical Tradition since 1910 — Unfamiliar Listening",
        "desc": "Twentieth-century orchestral and choral writing: instrumental colour, "
                "dynamics that build across a whole extract, and styles that borrow from jazz.",
        "links": [
            ("Bartók — Hungarian Sketches I: An Evening in the Village (Boulez / Chicago SO)",
             "https://www.youtube.com/watch?v=Gjwu4F8pqj0", "Set study piece, movement 1."),
            ("Bartók — Hungarian Sketches II: Bear Dance",
             "https://www.youtube.com/watch?v=_LYv64v6hRY", "Set study piece, movement 2."),
            ("Bartók — Hungarian Sketches IV: Slightly Tipsy",
             "https://www.youtube.com/watch?v=oY3lGUOvi2A", "Set study piece, movement 4."),
            ("Bartók — Hungarian Sketches V: Swineherd's Dance",
             "https://www.youtube.com/watch?v=kPDsw98Ax3I", "Set study piece, movement 5. "
             "Movement 3 is not on your specification."),
            ("Copland — Fanfare for the Common Man (Gewandhausorchester)",
             "https://www.youtube.com/watch?v=NcND9dlwpC4", "Copland strand."),
            ("Arnold — Peterloo Overture (BBC Concert Orchestra)",
             "https://www.youtube.com/watch?v=YmVZb8BNP38", "British strand."),
            ("Tavener — Song for Athene (Choir of St John's College, Cambridge)",
             "https://www.youtube.com/watch?v=OaQkHeK3j8U", "British strand."),
            ("Maxwell Davies — An Orkney Wedding, with Sunrise",
             "https://www.youtube.com/watch?v=97EX3LLQ33M", "British strand."),
            ("Kodály — Dances of Galánta, finale (LSO)",
             "https://www.youtube.com/watch?v=h1SbxDUSJeI", "Kodály strand."),
            ("Adams — Short Ride in a Fast Machine (Berliner Philharmoniker)",
             "https://www.youtube.com/watch?v=bekh-sZ0-A8", "Minimalism strand."),
            ("Reich — Music for 18 Musicians",
             "https://www.youtube.com/watch?v=1oOmUi4HGt0",
             "Minimalism strand. Long — listen to any five minutes and notice how little, "
             "and how gradually, it changes."),
            ("Riley — In C (Bang on a Can All-Stars)",
             "https://www.youtube.com/watch?v=AVfAoNHjTHQ", "Minimalism strand."),
        ],
        "context": "AQA names four strands here: the orchestral music of Copland, British "
                   "music of Arnold, Britten, Maxwell-Davies and Tavener, the orchestral "
                   "music of Kodály and Bartók, and minimalist music of Adams, Reich and "
                   "Riley. The extracts below drill the listening skills; the links take you "
                   "to the repertoire itself.",
    },
}

METHOD = {"title": "How to answer a listening question", "steps": [
    "Play the extract once without looking at the options — form your own impression first",
    "Read the question and decide which element it asks about: timbre, dynamics, rhythm, "
    "texture, tempo or melody",
    "Play it again listening ONLY for that element",
    "Cross off any option that contradicts what you heard, then choose",
    "Play it a final time to confirm your answer still fits"]}

TIERS = ["bronze", "silver", "gold"]


def passage_html(url, credit=None):
    block = ('<div style="text-align: center;">'
             '<p style="font-family: Inter, sans-serif; font-size: 0.95rem; '
             'color: var(--text-primary); margin-bottom: 1rem;">Listen to the extract, '
             'then answer.</p>'
             '<audio controls preload="metadata" src="%s" '
             'style="width: 100%%; max-width: 480px; margin: 0.5rem auto;"></audio>' % url)
    if credit:
        block += ('<p style="font-family: Inter, sans-serif; font-size: 0.8rem; '
                  'color: var(--text-secondary); margin-top: 0.75rem;">%s</p>' % credit)
    return block + "</div>"


def links_html(links):
    if not links:
        return ""
    items = "".join(
        '<li style="margin-bottom:0.5rem;"><a href="%s" target="_blank" rel="noopener">%s</a>'
        '%s</li>' % (url, title, (" — " + why) if why else "")
        for title, url, why in links)
    return ('<h3>Listen to the real repertoire</h3>'
            '<p>These are official recordings on the performers\' and labels\' own channels. '
            'They open in a new tab.</p><ul>%s</ul>' % items)


def main():
    bank = batch1_bank.build_bank() + batch2_bank.build_bank() + pd_bank.build_bank()
    by_aos = {}
    for rec in bank:
        by_aos.setdefault(rec["aos"], []).append(rec)
    print("bank: %d questions | %s" % (len(bank), {k: len(v) for k, v in sorted(by_aos.items())}))

    sb = get_client()
    subj = sb.from_("subjects").select("id, settings").eq("slug", "music-aqa") \
             .is_("school_id", "null").execute().data[0]

    # upload any clip not already on R2 (the PD ones; generated clips are up)
    if not DRY:
        r2 = get_r2_client()
        for rec in bank:
            if not rec.get("path"):
                continue
            with open(rec["path"], "rb") as f:
                upload_bytes_to_r2(r2, AUDIO_BUCKET, rec["r2_key"], f.read(), "audio/mpeg")
        print("uploaded public-domain excerpts")

    existing = sb.from_("units").select("id").eq("subject_id", subj["id"]) \
                 .eq("slug", UNIT_SLUG).execute().data
    if existing:
        unit_id = existing[0]["id"]
        print("unit exists:", unit_id)
    elif DRY:
        unit_id = "(dry-run)"
    else:
        unit_id = sb.from_("units").insert({
            "subject_id": subj["id"], "slug": UNIT_SLUG,
            "name": "Areas of Study: Listening",
            "subtitle": "Unfamiliar-listening drills for Areas of Study 2, 3 and 4, on "
                        "verified extracts.",
            "body_class": "unit-music-aqa-aos", "accent": "#7c3aed",
            "accent_light": "#7c3aed22", "accent_badge": "#7c3aed33",
            "lesson_count": len(LESSONS), "sort_order": 4,
        }).execute().data[0]["id"]
        print("unit created:", unit_id)

    for aos, spec in sorted(LESSONS.items(), key=lambda kv: kv[1]["n"]):
        recs = by_aos.get(aos, [])
        if not recs:
            print("SKIP %s - no questions" % aos)
            continue
        passages, seen = [], {}
        for rec in recs:
            if rec["clip"] not in seen:
                seen[rec["clip"]] = True
                passages.append({"id": rec["clip"],
                                 "text": passage_html(rec["url"] if "url" in rec else
                                                      "%s/%s" % (AUDIO_PUBLIC_URL, rec["r2_key"]),
                                                      rec.get("credit"))})
        # worked example = first question, shown fully worked
        wq = recs[0]
        worked = [{
            "question": passage_html("%s/%s" % (AUDIO_PUBLIC_URL, wq["r2_key"]),
                                     wq.get("credit"))
                        + "Listen to the extract. " + wq["question"],
            "difficulty": "bronze",
            "steps": [
                {"label": "Step 1 — listen once, no options",
                 "content": "Play the whole extract before you read the choices. Decide for "
                            "yourself what stands out."},
                {"label": "Step 2 — name the element",
                 "content": "This question asks about a single musical element. Work out which "
                            "one, then play the extract again listening only for it."},
                {"label": "Step 3 — eliminate, then commit",
                 "content": "Rule out every option that contradicts what you heard. "
                            "Answer: <strong>%s</strong>." % wq["answer"]},
            ]}]
        bankq = {"bronze": [], "silver": [], "gold": []}
        for i, rec in enumerate(recs[1:]):
            bankq[TIERS[i % 3]].append({
                "input_type": "multiple_choice",
                "passage_id": rec["clip"],
                "question": rec["question"],
                "options": rec["options"],
                "solutions": [rec["correct"]],
                "explanation": "Answer: %s. Play the extract once more and listen for just "
                               "that feature." % rec["answer"],
            })
        pd_ = {"passages": passages, "problem_bank": bankq, "method_card": METHOD,
               "exam_context": spec["context"], "worked_examples": worked}
        row = {"unit_id": unit_id, "lesson_number": spec["n"], "slug": spec["slug"],
               "title": spec["title"], "description": spec["desc"],
               "status": "pending_review", "tier": "both", "practice_data": pd_,
               "content_html": links_html(spec["links"])}
        print("  L%02d %-58s %2d questions / %d extracts"
              % (spec["n"], spec["title"][:58], len(recs), len(passages)))
        if DRY:
            continue
        old = sb.from_("lessons").select("id").eq("unit_id", unit_id) \
                .eq("lesson_number", spec["n"]).execute().data
        if old:
            sb.from_("lessons").update(row).eq("id", old[0]["id"]).execute()
        else:
            sb.from_("lessons").insert(row).execute()

    if not DRY:
        settings = subj.get("settings") or {}
        pu = settings.get("practice_units") or []
        if UNIT_SLUG not in pu:
            pu.append(UNIT_SLUG)
            settings["practice_units"] = pu
            sb.from_("subjects").update({"settings": settings}).eq("id", subj["id"]).execute()
            print("practice_units updated:", pu)
    print("DONE" + (" (dry run)" if DRY else ""))


if __name__ == "__main__":
    main()
