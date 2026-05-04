"""Copy heroes + related_media from PE AQA to PE OCR for transferred lessons.

For each OCR lesson with content_transfer.transfer_score in (high, medium, low),
look up the AQA lesson by source_unit_slug + source_lesson_number, and copy
hero/media fields onto the OCR row. Fresh transfers are skipped.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

scripts = Path(__file__).resolve().parent
plan = json.loads(
    (scripts / "_plan_physical-education-ocr.json").read_text(encoding="utf-8")
)
sb = get_client()

ASSET_FIELDS = [
    "hero_image_url", "hero_image_caption", "hero_image_alt",
    "hero_image_position", "related_media", "youtube_video_id",
]


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[‘’′]", "", s)
    s = re.sub(r"[–—]", "-", s)
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80]


def get_subject_lessons_by_unit_and_num(slug):
    """Return {(unit_slug, lesson_number): row} for lessons under subject slug."""
    res = sb.table("subjects").select("id").eq("slug", slug).is_("school_id", "null").execute()
    sid = res.data[0]["id"]
    units = sb.table("units").select("id, slug").eq("subject_id", sid).execute().data
    out = {}
    for u in units:
        rows = (
            sb.table("lessons")
            .select("id, slug, lesson_number, " + ", ".join(ASSET_FIELDS))
            .eq("unit_id", u["id"])
            .execute()
            .data
        )
        for r in rows:
            out[(u["slug"], r["lesson_number"])] = r
    return out


print("Loading source (PE AQA) and target (PE OCR) lesson maps...")
aqa = get_subject_lessons_by_unit_and_num("physical-education-aqa")
ocr = get_subject_lessons_by_unit_and_num("physical-education-ocr")
print(f"  AQA lessons: {len(aqa)}")
print(f"  OCR lessons: {len(ocr)}")

print("\n--- Copying assets per content_transfer plan ---")
copied = 0
fresh = 0
missing = 0
for unit in plan["article_units"]:
    ocr_unit_slug = unit["slug"]
    for L in unit["lessons"]:
        ct = L.get("content_transfer", {}) or {}
        score = ct.get("transfer_score")
        src_unit = ct.get("source_unit_slug")
        src_num = ct.get("source_lesson_number")

        ocr_row = ocr.get((ocr_unit_slug, L["number"]))
        title_short = L["title"][:46]

        if score == "fresh" or not src_unit or not src_num:
            print(f"  L{L['number']:2d} {title_short:46s}  FRESH (skip)")
            fresh += 1
            continue

        src_row = aqa.get((src_unit, src_num))
        if not src_row:
            print(f"  L{L['number']:2d} {title_short:46s}  MISS source ({src_unit} #{src_num})")
            missing += 1
            continue

        if not ocr_row:
            print(f"  L{L['number']:2d} {title_short:46s}  MISS OCR target ({ocr_unit_slug} #{L['number']})")
            missing += 1
            continue

        payload = {f: src_row.get(f) for f in ASSET_FIELDS if src_row.get(f) is not None}
        if not payload:
            print(f"  L{L['number']:2d} {title_short:46s}  src has no assets")
            missing += 1
            continue

        sb.table("lessons").update(payload).eq("id", ocr_row["id"]).execute()
        fields = ", ".join(sorted(k.replace("_image_", "_").replace("_", "")[:6] for k in payload))
        print(f"  L{L['number']:2d} {title_short:46s} <- AQA {src_unit[:18]:18s}#{src_num:2d}  [{fields}]")
        copied += 1

print(f"\n  Copied: {copied}, fresh-skipped: {fresh}, missing: {missing}")
