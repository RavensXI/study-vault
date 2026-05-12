"""Fix UTF-8-as-cp1252 mojibake across all lessons' content fields.

Reads scripts/_audit_mojibake_findings.json (produced by
_audit_mojibake.py) and applies targeted unicode replacements. Order
matters — longer/more-specific sequences first.

After running, re-run _audit_mojibake.py to confirm zero hits.
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


# Ordered list of mojibake → correct character. Apply LONGEST patterns
# FIRST so we don't accidentally double-replace.
REPLACEMENTS = [
    # 3-byte UTF-8 chars that became 6-byte sequences when mis-encoded
    ("â€™", "’"),   # right single quotation mark '
    ("â€˜", "‘"),   # left single quotation mark '
    ("â€œ", "“"),   # left double quotation mark "
    ("â€\x9d", "”"), # right double quotation mark "
    ("â€¦", "…"),   # horizontal ellipsis …
    ("â€“", "–"),   # en dash –
    ("â€”", "—"),   # em dash —
    ("â€¢", "•"),   # bullet •
    # 2-byte UTF-8 chars that became 4-byte sequences
    ("Ã©", "é"),    # é
    ("Ã¨", "è"),    # è
    ("Ãª", "ê"),    # ê
    ("Ã«", "ë"),    # ë
    ("Ã¡", "á"),    # á
    ("Ã ", "à"),    # à  (NB trailing space matters)
    ("Ã¢", "â"),    # â
    ("Ã¤", "ä"),    # ä
    ("Ã­", "í"),    # í
    ("Ã¬", "ì"),    # ì
    ("Ã®", "î"),    # î
    ("Ã¯", "ï"),    # ï
    ("Ã³", "ó"),    # ó
    ("Ã²", "ò"),    # ò
    ("Ã´", "ô"),    # ô
    ("Ã¶", "ö"),    # ö
    ("Ãº", "ú"),    # ú
    ("Ã¹", "ù"),    # ù
    ("Ã»", "û"),    # û
    ("Ã¼", "ü"),    # ü
    ("Ã±", "ñ"),    # ñ
    ("Ã§", "ç"),    # ç
    ("Ã‰", "É"),    # É
    ("Ãœ", "Ü"),    # Ü
    # Catch-all: stray  often appears next to other mojibake — strip
    # only after the patterns above have run, so we don't break legit Â.
    # Leave it: re-audit will flag any residual.
]


FIELDS = [
    "related_media", "practice_questions", "knowledge_checks",
    "flashcard_questions", "glossary_terms", "description",
    "content_html", "exam_tip_html", "conclusion_html",
]


def fix_str(s):
    if not isinstance(s, str):
        return s, 0
    fixed = 0
    for bad, good in REPLACEMENTS:
        if bad in s:
            count = s.count(bad)
            s = s.replace(bad, good)
            fixed += count
    return s, fixed


def fix_obj(obj):
    """Recursively fix strings inside dict/list/string. Returns (new_obj, fix_count)."""
    if isinstance(obj, str):
        return fix_str(obj)
    elif isinstance(obj, dict):
        new = {}
        total = 0
        for k, v in obj.items():
            nv, c = fix_obj(v)
            new[k] = nv
            total += c
        return new, total
    elif isinstance(obj, list):
        new = []
        total = 0
        for v in obj:
            nv, c = fix_obj(v)
            new.append(nv)
            total += c
        return new, total
    else:
        return obj, 0


def main():
    findings = json.loads(open("scripts/_audit_mojibake_findings.json", encoding="utf-8").read())
    lesson_ids = [f["lesson_id"] for f in findings]
    print(f"Processing {len(lesson_ids)} affected lessons...")

    sb = get_client()
    total_fixes = 0
    lessons_updated = 0
    for lid in lesson_ids:
        row = sb.table("lessons").select("id," + ",".join(FIELDS)).eq("id", lid).execute().data
        if not row:
            continue
        row = row[0]
        update = {}
        per_lesson_fixes = 0
        for field in FIELDS:
            if row.get(field) is None:
                continue
            new_val, c = fix_obj(row[field])
            if c > 0:
                update[field] = new_val
                per_lesson_fixes += c
        if update:
            sb.table("lessons").update(update).eq("id", lid).execute()
            total_fixes += per_lesson_fixes
            lessons_updated += 1
            print(f"  {lid[:8]} — {per_lesson_fixes} fixes in {', '.join(update.keys())}")

    print()
    print(f"Updated {lessons_updated} lessons, {total_fixes} total fixes applied.")
    print("Re-run scripts/_audit_mojibake.py to confirm zero hits.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
