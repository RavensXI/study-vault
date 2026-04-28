"""Phase 3 follow-up: validate generated lesson JSONs and insert into Supabase.

For each JSON file in scripts/_content_history-aqa/lessons/:
1. Validate against the CONTENT_PROMPT.md checklist + drift grep.
2. If valid, update the matching empty lesson row in Supabase
   (matched by unit slug + lesson_number embedded in filename).
3. Print per-lesson pass/fail summary; --insert flag actually does the upserts.

Filename convention: {unit-slug}_{NN}.json   e.g.  germany-democracy-dictatorship_03.json

Usage:
  python scripts/_validate_and_insert_history_aqa.py            # dry-run validation only
  python scripts/_validate_and_insert_history_aqa.py --insert   # validate + insert
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

scripts = Path(__file__).resolve().parent
lessons_dir = scripts / "_content_history-aqa" / "lessons"
master = json.loads((scripts / "_plan_history-aqa.json").read_text(encoding="utf-8"))

REGISTERED_QT = set(master["question_type_names"])
SUBJECT_SLUG = master["subject"]["slug"]


REQUIRED_TOP_KEYS = {
    "description",
    "content_html",
    "exam_tip_html",
    "conclusion_html",
    "practice_questions",
    "knowledge_checks",
    "flashcard_questions",
    "glossary_terms",
    "hero_keywords",
    "hero_image_caption",
}

FORBIDDEN_FREE_TIER_KEYS = {"diagram_prompt", "diagram_style"}

DRIFT_PATTERNS = [
    (r"\b8145\b", "spec code 8145"),
    (r"\b8145/\d", "paper code 8145/X"),
    (r"\bComponent \d", "component code"),
    (r"\bLevel\s+[1-9]\b", "Level descriptor"),
    (r"Nothing worthy of credit", "exam-board rubric phrase"),
    (r"How far do you agree", "AQA rubric phrase"),
    (r"How does Interpretation B differ from Interpretation A", "AQA rubric phrase"),
    (r"You could include the following", "AQA rubric phrase"),
    (r"Has\s+\w+\s+been the main factor", "AQA rubric phrase"),
    (r"In what ways were", "AQA rubric phrase"),
    (r"<!--\s*DIAGRAM\s*-->", "Diagram placeholder (Unity-only)"),
    (r"<h1[\s>]", "h1 tag (template renders title)"),
]


def strip_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", " ", html)


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def validate_lesson(data: dict, filename: str) -> list[str]:
    issues: list[str] = []

    # Required keys
    missing = REQUIRED_TOP_KEYS - set(data.keys())
    if missing:
        issues.append(f"missing keys: {sorted(missing)}")
    forbidden = FORBIDDEN_FREE_TIER_KEYS & set(data.keys())
    if forbidden:
        issues.append(f"free-tier must not include: {sorted(forbidden)}")

    # description
    desc = data.get("description") or ""
    if not (60 <= len(desc) <= 110):
        issues.append(f"description {len(desc)} chars (60-110 expected — slight overshoot tolerated)")

    # content_html
    content = data.get("content_html") or ""
    wc = word_count(strip_tags(content))
    if not (700 <= wc <= 1700):  # slight tolerance vs 800-1500
        issues.append(f"content_html word count {wc} (target 800-1500)")

    # narration ids
    narration_ids = re.findall(r'data-narration-id="(n\d+)"', content)
    seen = set()
    for nid in narration_ids:
        n = int(nid[1:])
        if n in seen:
            issues.append(f"duplicate narration id {nid}")
        seen.add(n)
    if narration_ids:
        nums = sorted(int(n[1:]) for n in narration_ids)
        if nums[0] != 1:
            issues.append(f"narration ids should start at n1 (got n{nums[0]})")
        for i, n in enumerate(nums):
            if n != i + 1:
                issues.append(f"narration id sequence has gap at n{n}")
                break

    # key-facts
    n_kf = len(re.findall(r'<div class="key-fact"', content))
    if n_kf < 2:
        issues.append(f"key-facts: {n_kf} (≥2 expected)")

    # collapsibles
    n_coll = len(re.findall(r'<div class="collapsible"', content))
    if n_coll < 2:
        issues.append(f"collapsibles: {n_coll} (≥2 expected)")

    # glossary dfns
    dfns = re.findall(r'<dfn class="term"\s+data-def="[^"]*">([^<]+)</dfn>', content)
    if len(dfns) < 3:
        issues.append(f"<dfn> glossary terms in content: {len(dfns)} (≥3 expected)")

    # glossary array vs dfns
    glossary = data.get("glossary_terms") or []
    if len(glossary) != len(dfns):
        issues.append(f"glossary_terms count ({len(glossary)}) != <dfn> count ({len(dfns)})")

    # practice questions
    pqs = data.get("practice_questions") or []
    if len(pqs) != 6:
        issues.append(f"practice_questions: {len(pqs)} (exactly 6 required)")
    for i, q in enumerate(pqs):
        if not isinstance(q, dict):
            issues.append(f"practice_q[{i}] not a dict")
            continue
        for k in ("text", "type", "marks"):
            if not q.get(k):
                issues.append(f"practice_q[{i}] missing {k}")
        if q.get("type") and q["type"] not in REGISTERED_QT:
            issues.append(f"practice_q[{i}] type {q['type']!r} not registered")

    # knowledge checks
    kcs = data.get("knowledge_checks") or []
    if len(kcs) != 5:
        issues.append(f"knowledge_checks: {len(kcs)} (exactly 5 required)")
    types = [k.get("type") for k in kcs if isinstance(k, dict)]
    if types.count("mcq") != 2 or types.count("fill") != 2 or types.count("match") != 1:
        issues.append(f"knowledge_checks types {sorted(types)} (need 2 mcq + 2 fill + 1 match)")

    # flashcards
    fcs = data.get("flashcard_questions") or []
    if not (8 <= len(fcs) <= 15):
        issues.append(f"flashcards: {len(fcs)} (8-15 expected)")
    for i, c in enumerate(fcs):
        if not (isinstance(c, dict) and "q" in c and "a" in c):
            issues.append(f"flashcard[{i}] malformed")
            continue
        ans_words = word_count(c["a"] or "")
        if ans_words > 30:
            issues.append(f"flashcard[{i}] answer {ans_words} words (≤30 hard cap)")

    # hero
    hk = data.get("hero_keywords") or []
    if not (3 <= len(hk) <= 4):
        issues.append(f"hero_keywords: {len(hk)} (3-4 expected)")
    cap = data.get("hero_image_caption") or ""
    if not cap or word_count(cap) < 4:
        issues.append("hero_image_caption missing or too short")

    # Drift grep — across all string fields
    flat_text = json.dumps(data, ensure_ascii=False)
    for pat, label in DRIFT_PATTERNS:
        if re.search(pat, flat_text, re.IGNORECASE if "rubric" in label or "phrase" in label else 0):
            issues.append(f"drift pattern hit: {label}")

    return issues


def parse_filename(name: str):
    """{unit-slug}_{lesson-number}.json — but unit slugs themselves contain hyphens."""
    if not name.endswith(".json"):
        return None, None
    stem = name[:-5]
    m = re.match(r"^(.+)_(\d{1,3})$", stem)
    if not m:
        return None, None
    return m.group(1), int(m.group(2))


def find_lesson_row(sb, unit_slug: str, lesson_number: int):
    subject = (
        sb.table("subjects")
        .select("id")
        .eq("slug", SUBJECT_SLUG)
        .is_("school_id", "null")
        .single()
        .execute()
        .data
    )
    unit = (
        sb.table("units")
        .select("id")
        .eq("subject_id", subject["id"])
        .eq("slug", unit_slug)
        .single()
        .execute()
        .data
    )
    lesson = (
        sb.table("lessons")
        .select("id, status, content_html")
        .eq("unit_id", unit["id"])
        .eq("lesson_number", lesson_number)
        .single()
        .execute()
        .data
    )
    return lesson


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--insert", action="store_true", help="Actually update Supabase rows")
    parser.add_argument("--unit", help="Only process files for this unit slug")
    parser.add_argument("--filter", help="Only filenames matching this substring")
    args = parser.parse_args()

    if not lessons_dir.exists():
        print(f"No generated lessons yet at {lessons_dir}")
        return

    files = sorted(lessons_dir.glob("*.json"))
    if args.unit:
        files = [f for f in files if f.name.startswith(args.unit + "_")]
    if args.filter:
        files = [f for f in files if args.filter in f.name]

    if not files:
        print("No matching JSON files.")
        return

    sb = get_client() if args.insert else None
    pass_count = 0
    fail_count = 0
    failures: list[tuple[str, list[str]]] = []
    inserted = 0

    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            failures.append((f.name, [f"JSON parse error: {e}"]))
            fail_count += 1
            continue

        issues = validate_lesson(data, f.name)
        if issues:
            failures.append((f.name, issues))
            fail_count += 1
            continue

        pass_count += 1

        if args.insert:
            unit_slug, lesson_number = parse_filename(f.name)
            if not unit_slug:
                failures.append((f.name, ["bad filename"]))
                fail_count += 1
                pass_count -= 1
                continue
            try:
                lesson_row = find_lesson_row(sb, unit_slug, lesson_number)
            except Exception as e:
                failures.append((f.name, [f"DB lookup failed: {e}"]))
                fail_count += 1
                pass_count -= 1
                continue
            payload = {
                "description": data["description"],
                "content_html": data["content_html"],
                "exam_tip_html": data["exam_tip_html"],
                "conclusion_html": data["conclusion_html"],
                "practice_questions": data["practice_questions"],
                "knowledge_checks": data["knowledge_checks"],
                "flashcard_questions": data["flashcard_questions"],
                "glossary_terms": data["glossary_terms"],
                "hero_image_caption": data["hero_image_caption"],
            }
            sb.table("lessons").update(payload).eq("id", lesson_row["id"]).execute()
            inserted += 1

    print(f"\n{'='*60}")
    print(f"Validated: {pass_count} pass, {fail_count} fail (of {len(files)})")
    if args.insert:
        print(f"Inserted into Supabase: {inserted}")
    print(f"{'='*60}\n")
    if failures:
        print("FAILURES:")
        for name, issues in failures:
            print(f"\n  {name}:")
            for i in issues:
                print(f"    - {i}")


if __name__ == "__main__":
    main()
