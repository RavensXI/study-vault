"""Audit lessons' related_media for mojibake (UTF-8 bytes mis-encoded as
cp1252/Latin-1 then re-encoded as UTF-8). Symptoms: visible sequences
like `â€™` `â€œ` `Ã©` etc. instead of the proper unicode characters.

Also checks practice_questions, knowledge_checks, flashcard_questions,
glossary_terms, description, exam_tip_html, conclusion_html, content_html
in case the same fault is present elsewhere.

Output: scripts/_audit_mojibake_findings.json with per-lesson counts +
sample snippets, plus a console summary by subject.
"""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from lib.supabase_client import get_client


# Common mojibake patterns (UTF-8 → cp1252/Latin-1 → UTF-8). Each entry is
# (regex_pattern, what_it_should_be, severity_weight).
# Most are 2-3 byte sequences starting with â or Ã.
MOJIBAKE_PATTERNS = [
    ("â€™", "'", "right single quote / apostrophe"),
    ("â€˜", "'", "left single quote"),
    ("â€œ", '"', "left double quote"),
    ("â€\x9d", '"', "right double quote"),
    ("â€", '"', "right double quote (variant)"),
    ("â€¦", "…", "ellipsis"),
    ("â€“", "–", "en dash"),
    ("â€”", "—", "em dash"),
    ("â€¢", "•", "bullet"),
    ("Ã©", "é", "e-acute"),
    ("Ã¨", "è", "e-grave"),
    ("Ã ", "à", "a-grave"),
    ("Ã¡", "á", "a-acute"),
    ("Ã­", "í", "i-acute"),
    ("Ã³", "ó", "o-acute"),
    ("Ãº", "ú", "u-acute"),
    ("Ã±", "ñ", "n-tilde"),
    ("Ã¶", "ö", "o-umlaut"),
    ("Ã¼", "ü", "u-umlaut"),
    ("Ã¤", "ä", "a-umlaut"),
    ("Ã"   "œ", "Œ", "OE ligature"),  # split to avoid encoding issues
    # Catch-all signal: any standalone â followed by 1-2 chars is suspicious.
    # We score these lower since some legitimate words (rare) might trip.
]

# Broad detection regex — at minimum flag any of these sequences existing.
DETECT_RE = re.compile(r"â€.|Ã[©¨¡¢£¤¥¦§¨©ª«¬­®¯°± ¡¢£©¨\xa0-\xff]")


def walk_text(obj, hits, path):
    """Recursively walk JSON-like structure and accumulate mojibake hits."""
    if isinstance(obj, str):
        for m in DETECT_RE.finditer(obj):
            start = max(0, m.start() - 25)
            end = min(len(obj), m.end() + 25)
            snippet = obj[start:end].replace("\n", " ")
            hits.append({
                "path": path,
                "match": m.group(),
                "context": snippet,
            })
    elif isinstance(obj, dict):
        for k, v in obj.items():
            walk_text(v, hits, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk_text(v, hits, f"{path}[{i}]")


def main():
    sb = get_client()
    # Paginate to bypass 1000-row default
    lessons = []
    offset = 0
    page_size = 1000
    while True:
        page = sb.table("lessons").select(
            "id, lesson_number, title, unit_id, related_media, "
            "practice_questions, knowledge_checks, flashcard_questions, "
            "glossary_terms, description, content_html, exam_tip_html, conclusion_html"
        ).range(offset, offset + page_size - 1).execute().data
        if not page:
            break
        lessons.extend(page)
        if len(page) < page_size:
            break
        offset += page_size

    print(f"Scanning {len(lessons)} lessons...")

    units = {u["id"]: u for u in sb.table("units").select("id, slug, subject_id").execute().data}
    subjects = {s["id"]: s for s in sb.table("subjects").select("id, slug, school_id").execute().data}

    findings_by_lesson = []
    for L in lessons:
        hits = []
        for field in ("related_media", "practice_questions", "knowledge_checks",
                      "flashcard_questions", "glossary_terms", "description",
                      "content_html", "exam_tip_html", "conclusion_html"):
            v = L.get(field)
            if v is None:
                continue
            walk_text(v, hits, field)
        if hits:
            u = units.get(L["unit_id"])
            s = subjects.get(u["subject_id"]) if u else None
            findings_by_lesson.append({
                "lesson_id": L["id"],
                "subject_slug": s["slug"] if s else "?",
                "scope": "unity" if s and s.get("school_id") else "generic",
                "unit_slug": u["slug"] if u else "?",
                "lesson_number": L["lesson_number"],
                "title": L["title"],
                "hit_count": len(hits),
                "samples": hits[:5],
            })

    findings_by_lesson.sort(key=lambda f: -f["hit_count"])

    # Summary by subject
    by_subject = {}
    for f in findings_by_lesson:
        key = f["subject_slug"] + (" (unity)" if f["scope"] == "unity" else "")
        by_subject.setdefault(key, {"lessons": 0, "hits": 0})
        by_subject[key]["lessons"] += 1
        by_subject[key]["hits"] += f["hit_count"]

    print()
    print(f"Lessons with mojibake: {len(findings_by_lesson)}")
    print(f"Total hits: {sum(f['hit_count'] for f in findings_by_lesson)}")
    print()
    print("By subject (sorted by hit count):")
    for slug in sorted(by_subject.keys(), key=lambda k: -by_subject[k]["hits"]):
        v = by_subject[slug]
        print(f"  {slug:<45} {v['lessons']:>4} lessons, {v['hits']:>5} hits")
    print()
    if findings_by_lesson:
        print("Worst 10 lessons:")
        for f in findings_by_lesson[:10]:
            print(f"  {f['subject_slug']:<35} {f['unit_slug']:<35} L{f['lesson_number']:>2} ({f['hit_count']} hits) — {f['title'][:50]}")
            if f["samples"]:
                ex = f["samples"][0]
                print(f"      path={ex['path']} match={ex['match']!r}")
                print(f"      ...{ex['context']}...")

    out_path = "scripts/_audit_mojibake_findings.json"
    with open(out_path, "w", encoding="utf-8") as fp:
        json.dump(findings_by_lesson, fp, indent=2, ensure_ascii=False)
    print()
    print(f"Findings written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
