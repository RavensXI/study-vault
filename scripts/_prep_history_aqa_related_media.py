"""Phase 4 prep — build per-batch input JSONs for related media curation agents.

53 batches × 4 lessons each = 210 lessons total. Smaller batches than Phase 3
content gen because each lesson involves web search + URL verification, and
larger batches lead to lazy agents inserting hallucinated links.

Outputs:
  scripts/_content_history-aqa/related_media/_batch_{NN}.json — per-batch input
  scripts/_content_history-aqa/related_media/_manifest.json — list of batch IDs
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from lib.supabase_client import get_client

OUT_DIR = ROOT / "scripts" / "_content_history-aqa" / "related_media"
OUT_DIR.mkdir(exist_ok=True)
(OUT_DIR / "lessons").mkdir(exist_ok=True)

LESSONS_PER_BATCH = 4


def main():
    sb = get_client()
    sub = (
        sb.table("subjects")
        .select("id, name, exam_board")
        .eq("slug", "history-aqa")
        .is_("school_id", "null")
        .single()
        .execute()
        .data
    )
    units = (
        sb.table("units")
        .select("id, slug, name, subtitle, sort_order")
        .eq("subject_id", sub["id"])
        .order("sort_order")
        .execute()
        .data
    )

    # Build flat ordered list of (unit, lesson) tuples
    flat = []
    for unit in units:
        lessons = (
            sb.table("lessons")
            .select("id, slug, lesson_number, title, description")
            .eq("unit_id", unit["id"])
            .order("lesson_number")
            .execute()
            .data
        )
        for L in lessons:
            flat.append((unit, L))

    print(f"Found {len(flat)} lessons across {len(units)} units")

    # Chunk into batches of 4, preferring lessons from the same unit per batch
    # (gives the agent topical coherence — easier to research a coherent set).
    by_unit = {}
    for unit, L in flat:
        by_unit.setdefault(unit["slug"], []).append((unit, L))

    batches = []
    for unit_slug, items in by_unit.items():
        for i in range(0, len(items), LESSONS_PER_BATCH):
            chunk = items[i : i + LESSONS_PER_BATCH]
            batches.append(chunk)

    print(f"Built {len(batches)} batches (target {LESSONS_PER_BATCH} lessons each, last batches per unit may be smaller)")

    manifest = []
    for n, chunk in enumerate(batches, start=1):
        batch_id = f"{n:02d}"
        # All lessons in a batch share the same unit by construction
        unit = chunk[0][0]
        payload = {
            "batch_id": batch_id,
            "subject": {
                "name": sub["name"],
                "slug": "history-aqa",
                "exam_board": sub["exam_board"],
                "target_audience": "free-tier (15-16 year old GCSE students)",
            },
            "unit": {
                "name": unit["name"],
                "slug": unit["slug"],
                "subtitle": unit["subtitle"],
            },
            "lessons_in_batch": [
                {
                    "lesson_id": L["id"],
                    "lesson_number": L["lesson_number"],
                    "lesson_slug": L["slug"],
                    "title": L["title"],
                    "description": L["description"],
                }
                for (_, L) in chunk
            ],
            "output_dir": "scripts/_content_history-aqa/related_media/lessons",
        }
        out = OUT_DIR / f"_batch_{batch_id}.json"
        out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        manifest.append({"batch_id": batch_id, "unit": unit["slug"], "n_lessons": len(chunk)})

    (OUT_DIR / "_manifest.json").write_text(
        json.dumps({"total_batches": len(batches), "total_lessons": len(flat), "batches": manifest}, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {len(batches)} batch input files to {OUT_DIR}")


if __name__ == "__main__":
    main()
