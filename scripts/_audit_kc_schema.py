"""Audit every lesson's knowledge_checks for the bug pattern that breaks
the Quick Quiz Next button.

Player schema (per js/main.js renderMCQ/renderFill/renderMatch):
- All KCs need a `type` field with value 'mcq', 'fill', or 'match'
- `type: 'mcq'`   needs q.q, q.options (array), q.correct (int index)
- `type: 'fill'`  needs q.q (with '_____'), q.options (array), q.correct (int)
- `type: 'match'` needs q.q, q.left (array), q.right (array)

Common bugs found in earlier audits:
- `answers: ["text"]` instead of `correct: <int>` + `options`
- Wrong type values like 'multiple_choice', 'fill_blank', 'match-up'
- Missing `correct` field — JS reads undefined, throws when indexing
- options/left/right arrays not arrays
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from lib.supabase_client import get_client


VALID_TYPES = {"mcq", "fill", "match"}


def validate_kc(kc, idx):
    """Return list of error strings, or [] if KC is valid."""
    errors = []
    if not isinstance(kc, dict):
        return [f"kc[{idx}] is not a dict ({type(kc).__name__})"]

    t = kc.get("type")
    if t not in VALID_TYPES:
        errors.append(f"kc[{idx}].type = {t!r} (must be one of {sorted(VALID_TYPES)})")

    if not kc.get("q"):
        errors.append(f"kc[{idx}] missing 'q' field")

    if t in ("mcq", "fill"):
        opts = kc.get("options")
        if not isinstance(opts, list):
            errors.append(f"kc[{idx}].options = {type(opts).__name__} (must be list)")
        elif len(opts) < 2:
            errors.append(f"kc[{idx}].options has {len(opts)} items (need >=2)")

        # Check for the canonical 'correct' int OR the broken 'answers' shape
        if "correct" not in kc:
            if "answers" in kc:
                errors.append(f"kc[{idx}] uses 'answers' field instead of 'correct' (BROKEN — Next button will fail)")
            else:
                errors.append(f"kc[{idx}] missing 'correct' field")
        else:
            c = kc["correct"]
            if not isinstance(c, int):
                errors.append(f"kc[{idx}].correct = {c!r} (must be int)")
            elif isinstance(opts, list) and (c < 0 or c >= len(opts)):
                errors.append(f"kc[{idx}].correct = {c} out of range for {len(opts)} options")

        if t == "fill" and kc.get("q") and "_____" not in kc["q"]:
            errors.append(f"kc[{idx}].q is type 'fill' but has no '_____' placeholder")

    if t == "match":
        left = kc.get("left")
        right = kc.get("right")
        if not isinstance(left, list):
            errors.append(f"kc[{idx}].left = {type(left).__name__} (must be list)")
        if not isinstance(right, list):
            errors.append(f"kc[{idx}].right = {type(right).__name__} (must be list)")
        if isinstance(left, list) and isinstance(right, list) and len(left) != len(right):
            errors.append(f"kc[{idx}] left/right length mismatch ({len(left)} vs {len(right)})")
        if "pairs" in kc and "left" not in kc:
            errors.append(f"kc[{idx}] uses 'pairs' (practice-format shape) instead of 'left'+'right' (BROKEN)")

    return errors


def main():
    sb = get_client()
    print("Querying all subjects + lessons with knowledge_checks ...")

    # Pull all subjects so we can group findings by subject
    subjects = sb.table("subjects").select("id, slug, name, school_id").execute().data
    subjects_by_id = {s["id"]: s for s in subjects}

    # Pull all units so we can group findings by unit
    units = sb.table("units").select("id, slug, name, subject_id").execute().data
    units_by_id = {u["id"]: u for u in units}

    # Pull all lessons — paginate to bypass Supabase's default 1000-row cap.
    lessons = []
    offset = 0
    page_size = 1000
    while True:
        page = sb.table("lessons").select("id, lesson_number, title, unit_id, status, knowledge_checks").range(offset, offset + page_size - 1).execute().data
        if not page:
            break
        lessons.extend(page)
        if len(page) < page_size:
            break
        offset += page_size
    print(f"  {len(lessons)} lesson rows total")
    print()

    broken_by_subject = {}
    total_lessons_with_kc = 0
    total_broken = 0

    for l in lessons:
        kcs = l.get("knowledge_checks")
        if not kcs:
            continue
        total_lessons_with_kc += 1

        # Sometimes stored as JSON string
        if isinstance(kcs, str):
            try:
                kcs = json.loads(kcs)
            except Exception:
                continue
        if not isinstance(kcs, list):
            continue

        errors = []
        for i, kc in enumerate(kcs):
            errors.extend(validate_kc(kc, i))

        if errors:
            total_broken += 1
            u = units_by_id.get(l["unit_id"])
            s = subjects_by_id.get(u["subject_id"]) if u else None
            subj_slug = s["slug"] if s else "?"
            scope = " (Unity)" if s and s.get("school_id") else ""
            key = subj_slug + scope
            broken_by_subject.setdefault(key, []).append({
                "lesson_id": l["id"],
                "unit_slug": u["slug"] if u else "?",
                "unit_name": u["name"] if u else "?",
                "lesson_number": l["lesson_number"],
                "title": l["title"],
                "status": l.get("status"),
                "errors": errors,
            })

    print(f"Lessons with KCs: {total_lessons_with_kc}")
    print(f"Lessons with broken KC schema: {total_broken}")
    print()

    if not broken_by_subject:
        print("All KCs valid. No bugs found.")
        return 0

    # Sort subjects by broken count
    for subj in sorted(broken_by_subject.keys(), key=lambda k: -len(broken_by_subject[k])):
        items = broken_by_subject[subj]
        print(f"=== {subj}: {len(items)} broken lessons ===")
        for it in items[:8]:  # cap output per subject for readability
            print(f"  L{it['lesson_number']:>2} {it['unit_slug']:<28} | {it['title'][:55]} | {it['status']}")
            for e in it["errors"][:3]:
                print(f"      {e}")
        if len(items) > 8:
            print(f"  ... and {len(items) - 8} more")
        print()

    out_path = "scripts/_audit_kc_findings.json"
    import json as J
    with open(out_path, "w", encoding="utf-8") as f:
        J.dump(broken_by_subject, f, indent=2, ensure_ascii=False)
    print(f"Full findings written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
