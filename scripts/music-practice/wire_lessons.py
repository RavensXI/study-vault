# -*- coding: utf-8 -*-
"""Wire the double-locked (construction + machine-ear) listening questions
into music-aqa as a new 'listening-skills' practice unit.

Only questions with status=verified ship. Uploads excerpt MP3s to R2, creates
unit + lessons at pending_review, writes practice_data in the same
passages/problem_bank shape as the existing works-based lessons.

Usage: python scripts/music-practice/wire_lessons.py
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from lib.supabase_client import get_client
from lib.r2 import get_r2_client, upload_bytes_to_r2, AUDIO_BUCKET, AUDIO_PUBLIC_URL

BANK = r"C:\Users\tshau\.claude\jobs\4059242c\tmp\music_bank"

LESSONS = [
    {"n": 1, "slug": "lesson-01", "title": "Hearing Tonality: Major, Minor and Beyond",
     "facts": ["tonality"],
     "desc": "Train your ear to tell major from minor, and to spot pentatonic and chromatic colour."},
    {"n": 2, "slug": "lesson-02", "title": "Hearing Instruments and Families",
     "facts": ["instrument_family"],
     "desc": "Identify which instrument family carries the melody across strings, woodwind and brass."},
    {"n": 3, "slug": "lesson-03", "title": "Texture, Devices and Cadences: First Steps",
     "facts": ["texture", "device", "cadence", "metre", "bass_rhythm"],
     "desc": "Spot textures, melodic devices and cadences in short focused excerpts."},
]

TIER_ORDER = ["bronze", "silver", "gold"]


def main():
    qs = [q for q in json.load(io.open(os.path.join(BANK, "questions.json"), encoding="utf-8"))
          if q["status"] == "verified"]
    print("verified questions:", len(qs))
    sb = get_client()
    r2 = get_r2_client()

    subj = sb.from_("subjects").select("id, settings").eq("slug", "music-aqa").is_("school_id", "null").execute().data[0]

    # unit (idempotent)
    existing = sb.from_("units").select("id").eq("subject_id", subj["id"]).eq("slug", "listening-skills").execute().data
    if existing:
        unit_id = existing[0]["id"]
        print("unit exists:", unit_id)
    else:
        unit = sb.from_("units").insert({
            "subject_id": subj["id"], "slug": "listening-skills", "name": "Listening Skills",
            "subtitle": "Ear-training drills on short verified excerpts — tonality, instruments, texture and cadences.",
            "body_class": "unit-music-aqa-listening", "accent": "#b45309",
            "accent_light": "#b4530922", "accent_badge": "#b4530933",
            "lesson_count": len(LESSONS), "sort_order": 3,
        }).execute().data[0]
        unit_id = unit["id"]
        print("unit created:", unit_id)

    # upload the excerpts that verified questions reference
    needed = sorted({q["excerpt"] for q in qs})
    urls = {}
    for ex in needed:
        key = "music-aqa/listening-skills/%s.mp3" % ex
        with open(os.path.join(BANK, ex + ".mp3"), "rb") as f:
            upload_bytes_to_r2(r2, AUDIO_BUCKET, key, f.read(), "audio/mpeg")
        urls[ex] = AUDIO_PUBLIC_URL + "/" + key
    print("uploaded %d excerpts to R2" % len(needed))

    for spec in LESSONS:
        lq = [q for q in qs if q["fact"] in spec["facts"]]
        if not lq:
            print("SKIP", spec["slug"], "- no verified questions")
            continue
        passages, bank = [], {"bronze": [], "silver": [], "gold": []}
        for i, q in enumerate(lq):
            pid = q["excerpt"]
            if pid not in [p["id"] for p in passages]:
                passages.append({"id": pid, "text":
                    '<div style="text-align: center;"><p style="font-family: Inter, sans-serif; '
                    'font-size: 0.95rem; color: var(--text-primary); margin-bottom: 1rem;">'
                    'Listen to the excerpt, then answer.</p>'
                    '<audio controls preload="metadata" src="%s" '
                    'style="width: 100%%; max-width: 480px; margin: 0.5rem auto;"></audio></div>' % urls[pid]})
            tier = TIER_ORDER[i % 3]
            bank[tier].append({
                "input_type": "multiple_choice", "passage_id": pid,
                "question": q["question"], "options": q["options"],
                "solutions": [q["correct"]],
                "explanation": "Verified answer: %s. This excerpt was composed so that this feature is "
                               "unambiguous — listen again and focus on it." % q["truth"],
            })
        pd = {"passages": passages, "problem_bank": bank,
              "method_card": {"title": "Ear-training method", "steps": [
                  "Listen to the whole excerpt once without answering",
                  "Listen again focusing only on the feature the question asks about",
                  "Eliminate options that clearly contradict what you hear",
                  "Answer, then listen one final time to confirm"]},
              "exam_context": "Component 1: Understanding Music — the listening exam plays short "
                              "excerpts and asks you to identify musical elements exactly like these drills.",
              "worked_examples": []}
        existing_l = sb.from_("lessons").select("id").eq("unit_id", unit_id).eq("lesson_number", spec["n"]).execute().data
        row = {"unit_id": unit_id, "lesson_number": spec["n"], "slug": spec["slug"],
               "title": spec["title"], "description": spec["desc"],
               "status": "pending_review", "tier": "both", "practice_data": pd}
        if existing_l:
            sb.from_("lessons").update(row).eq("id", existing_l[0]["id"]).execute()
        else:
            sb.from_("lessons").insert(row).execute()
        print("lesson %d '%s': %d questions (b%d/s%d/g%d) across %d excerpts" % (
            spec["n"], spec["title"], len(lq), len(bank["bronze"]), len(bank["silver"]),
            len(bank["gold"]), len(passages)))

    settings = subj.get("settings") or {}
    pu = settings.get("practice_units") or []
    if "listening-skills" not in pu:
        pu.append("listening-skills")
        settings["practice_units"] = pu
        sb.from_("subjects").update({"settings": settings}).eq("id", subj["id"]).execute()
        print("practice_units updated:", pu)
    print("DONE")


if __name__ == "__main__":
    main()
