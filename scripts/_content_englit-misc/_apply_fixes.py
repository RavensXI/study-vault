"""Apply the EngLit surgical content fixes.

Every edit is an exact-substring replacement, so the script fails loudly if
the stored text has drifted from what was reviewed. PATCHes one row at a
time by id. Run _backup_before_fixes.py first.

    python scripts/_content_englit-misc/_apply_fixes.py --dry-run
    python scripts/_content_englit-misc/_apply_fixes.py --only 1 2 4
"""
import argparse, json, os, sys
os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRIPT_DIR)
from lib.supabase_client import get_client

OUT = os.path.dirname(os.path.abspath(__file__))
BACKUP = os.path.join(OUT, "_final_fixes_backup.json")

FRANK_L6 = "0581f441-6e06-475c-b1b3-36d8184b8673"
LT_L2 = "e832b6dd-6e34-4e53-b71b-78c8ece8e905"
LT_L3 = "4038c672-d9f6-4924-9195-71745f273f3c"
LT_L5 = "dfc930cd-8246-46cc-9d9b-4fc16885d08e"
BDC_L6 = "c81cefe5-ecc1-4cc0-a8c6-1e30dbb7aee5"

# (fix_no, lesson_id, field, old_exact, new, note)
EDITS = [
    # ── FIX 1 — Frankenstein L6: Walton DOES turn back; ambiguity is the
    # Creature's fate. Curly apostrophes to match this lesson's convention.
    (1, FRANK_L6, "content_html",
     "Walton must decide whether to continue his dangerous quest or heed "
     "Victor’s warning. Shelley leaves this choice ambiguous, returning "
     "the moral question to the reader. Will humanity learn from "
     "Victor’s mistake? Will ambition be tempered by responsibility? The "
     "open ending suggests Shelley was not optimistic — the desire to "
     "push beyond limits is part of human nature. The novel is a warning, but "
     "it is uncertain whether the warning will be heard.",
     "Walton yields to them: he abandons the quest and turns the ship for "
     "home, heeding the warning Victor gave but could not follow himself. "
     "What Shelley leaves ambiguous is not Walton’s choice but the "
     "Creature’s ending. It is borne away into darkness and distance, and "
     "we never see it die. The moral question returns to the reader. Will "
     "humanity learn from Victor’s mistake? Will ambition be tempered by "
     "responsibility? Walton’s retreat suggests the warning can be heard, "
     "but the Creature’s unwitnessed fate leaves the novel’s final "
     "question open.",
     "n13 — Walton yields and turns back; ambiguity moved to the Creature"),

    # ── FIX 2 — Leave Taking titles: the unit teaches (L1 n8, L6 n2, L8 n15)
    # that the play is eight scenes and that 'Act 1'/'Act 2' is a marked exam
    # error. Scene ranges come from each lesson's own exam_tip canonical title.
    (2, LT_L2, "title",
     "Act 1: Enid, Viv & the Obeah Woman",
     "Scenes 1–3: Enid, Del & the Obeah Woman",
     "title — Act 1 -> Scenes 1-3; Viv -> Del per this lesson's own exam tip"),
    (2, LT_L3, "title",
     "Act 2: Generational Conflict",
     "Scenes 4–7: Generational Conflict",
     "title — Act 2 -> Scenes 4-7 (lesson states 'In Scenes 4-7')"),

    # ── FIX 4 — Boys Don't Cry is a NOVEL by Malorie Blackman.
    (4, BDC_L6, "content_html",
     "explaining its effect on the audience and then connecting it to a wider "
     "theme. For example: state what the playwright does,",
     "explaining its effect on the reader and then connecting it to a wider "
     "theme. For example: state what the novelist does,",
     "n28 — audience -> reader, playwright -> novelist"),
]

# FIX 3 is appended by _fix3_enid.py once the textual ruling is settled.
try:
    from _fix3_enid import EDITS3
    EDITS += EDITS3
except ImportError:
    pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", nargs="*", type=int, default=None)
    args = ap.parse_args()

    if not os.path.exists(BACKUP):
        print("REFUSING: backup missing. Run _backup_before_fixes.py first.")
        sys.exit(1)

    sb = get_client()
    # Group edits per lesson+field so one PATCH carries all its changes.
    todo = [e for e in EDITS if args.only is None or e[0] in args.only]
    by_row = {}
    for fix, lid, field, old, new, note in todo:
        by_row.setdefault((lid, field), []).append((fix, old, new, note))

    changed = 0
    for (lid, field), edits in by_row.items():
        row = sb.table("lessons").select(f"id,lesson_number,title,{field}").eq(
            "id", lid).single().execute().data
        val = row[field]
        for fix, old, new, note in edits:
            if new in val and old not in val:
                print(f"  [SKIP already applied] fix{fix} {lid[:8]} {field}: {note}")
                continue
            n = val.count(old)
            if n != 1:
                print(f"  [FAIL] fix{fix} {lid[:8]} {field}: old text found {n}x "
                      f"(expected 1). NOT written.")
                print(f"         looking for: {old[:110]!r}")
                sys.exit(2)
            val = val.replace(old, new)
            print(f"\n  [fix{fix}] {lid[:8]} L{row['lesson_number']} {field} — {note}")
            print(f"    BEFORE: {old}")
            print(f"    AFTER : {new}")
        if val == row[field]:
            continue
        if args.dry_run:
            print(f"    (dry-run — no write)")
        else:
            sb.table("lessons").update({field: val}).eq("id", lid).execute()
            print(f"    PATCHED {field} on {lid}")
        changed += 1

    print(f"\n{changed} row-fields {'would be' if args.dry_run else ''} updated.")


if __name__ == "__main__":
    main()
