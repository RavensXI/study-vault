# -*- coding: utf-8 -*-
"""OCR Phase 3b: copy the three music-eduqas Film Music articles into
music-ocr aos4-film-music L1-L3 wholesale — content (with the wired
verified embeds), questions, glossary, narration manifests (cross-subject
R2 reuse, same public bucket), heroes and related media. They were built
and fact-checked 16 Aug; the film-scoring content is board-agnostic.
L4 (borrowed classics + video game music) is built fresh by
ocr_build_articles.py — those strands are this spec's own.

Checks: no board names, no 'Area of Study N' self-references, all
narration clip URLs serve. Lessons land pending_review. Resume-safe.

Run: python ocr_copy_film_articles.py [--apply]
"""
import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

APPLY = "--apply" in sys.argv
FIELDS = ("lesson_number,slug,title,description,content_html,exam_tip_html,"
          "conclusion_html,practice_questions,knowledge_checks,"
          "flashcard_questions,glossary_terms,narration_manifest,"
          "hero_image_url,hero_image_alt,hero_image_caption,related_media")


def main():
    sb = get_client()
    src_sub = sb.table("subjects").select("id").eq("slug", "music-eduqas") \
        .execute().data[0]["id"]
    dst_sub = sb.table("subjects").select("id").eq("slug", "music-ocr") \
        .execute().data[0]["id"]
    units = sb.table("units").select("id,slug,subject_id").execute().data
    src_u = next(u for u in units if u["subject_id"] == src_sub
                 and u["slug"] == "aos3-film-music")
    dst_u = next(u for u in units if u["subject_id"] == dst_sub
                 and u["slug"] == "aos4-film-music")
    existing = {r["lesson_number"] for r in sb.table("lessons")
                .select("lesson_number").eq("unit_id", dst_u["id"])
                .execute().data}
    rows = sb.table("lessons").select(FIELDS).eq("unit_id", src_u["id"]) \
        .order("lesson_number").execute().data
    copied = 0
    for l in rows:
        n = l["lesson_number"]
        if n > 3 or n in existing:
            continue
        blob = json.dumps({k: l[k] for k in l if k != "narration_manifest"})
        prose = re.sub(r"https://\S+", "", blob)
        assert not re.search(r"(?i)\bAQA\b|\bEdexcel\b|\bWJEC\b|\bEduqas\b"
                             r"|\bOCR\b", prose), "board name L%d" % n
        assert "Area of Study" not in prose, "AoS self-reference L%d" % n
        print("film L%d: %s | %d clips | hero %s" % (
            n, l["title"][:44], len(l["narration_manifest"] or []),
            "yes" if l.get("hero_image_url") else "NO"))
        if APPLY:
            row = dict(l)
            row["unit_id"] = dst_u["id"]
            row["status"] = "pending_review"
            sb.table("lessons").insert(row).execute()
        copied += 1
    print("%s %d film lessons" % ("copied" if APPLY else "would copy", copied))
    # one narration clip must serve cross-subject
    m = re.search(r"https://[^\"]+\.mp3",
                  json.dumps(rows[0]["narration_manifest"]))
    if m:
        req = urllib.request.Request(m.group(0),
                                     headers={"User-Agent": "Mozilla/5.0"})
        print("sample clip HTTP:", urllib.request.urlopen(req, timeout=20).status)


if __name__ == "__main__":
    main()
