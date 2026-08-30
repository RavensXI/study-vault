"""Surgical fact-fixes for English Literature lessons.

1. english-literature-edexcel / boys-dont-cry L2,L4,L5,L6,L7
   Swap the two reversed character names. In Malorie Blackman's novel the
   ex-girlfriend is Melanie ("Mel") and the baby daughter is Emma.
   The unit had it backwards. "Bryce" is an unverifiable surname -> dropped.
   L1's three occurrences are already correct and are left untouched.

2. english-literature-eduqas / the-curious-incident L8
   AO4 was labelled "context". Eduqas C720QS: AO4 = vocabulary / sentence
   structure / spelling+punctuation; AO3 = context. Component 2 Section A
   (post-1914 prose/drama, where this play sits) assesses AO1, AO2 and AO4
   only -- AO3 is NOT assessed there.

3. english-literature-ocr / a-christmas-carol L7
   Repair the garbled embedded-quotation example sentence.

Also repairs two pre-existing duplicate data-narration-id collisions
(BDC L6 exam-tip n28, Curious Incident L8 exam-tip n33 + conclusion n34/n35)
which made those blocks share one R2 key and play the wrong audio.

    python scripts/_bdc_apply_fixes.py --dry-run
    python scripts/_bdc_apply_fixes.py
"""
import json
import os
import re
import sys

os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from lib.supabase_client import get_client  # noqa: E402

OUT_DIR = os.path.join(SCRIPT_DIR, "_content_englit-edexcel")
BACKUP = os.path.join(OUT_DIR, "_bdc_nameswap_backup.json")

DRY = "--dry-run" in sys.argv

BDC_UNIT = "8716371d-c1e1-4393-85c7-92cd52dc470a"

TEXT_FIELDS = ["title", "description", "content_html", "conclusion_html", "exam_tip_html"]
JSON_FIELDS = ["practice_questions", "knowledge_checks", "flashcard_questions",
               "glossary_terms", "related_media"]

SENT_SWAP = ""   # placeholder for the ex-girlfriend's name
SENT_KEEP = ""   # placeholder for text that must survive the swap


# ── Name swap ───────────────────────────────────────────────────────────

def swap_names(s):
    """Emma/Emma Bryce (ex-girlfriend) -> Melanie ; Mel (baby) -> Emma."""
    s = s.replace("Emma Bryce", SENT_SWAP)
    s = re.sub(r"\bEmma\b", SENT_SWAP, s)
    s = re.sub(r"\bMel\b", "Emma", s)
    return s.replace(SENT_SWAP, "Melanie")


# Strings that are ALREADY correct under the true naming and must not swap.
# Keyed by lesson_number -> field -> list of literal substrings.
PROTECT = {
    2: {
        "content_html": [
            "Emma's arrival in a pushchair signals she is an older baby, not a newborn.",
        ],
    },
}

# Post-swap literal refinements, keyed by lesson_number -> field -> [(old, new)]
REFINE = {
    2: {
        # post-swap the description reads "Melanie's arrival"; the arrival that
        # collapses the plans is the baby's, so name her explicitly.
        "description": [(
            "A-level results day, Melanie's arrival, and the collapse of Dante's university plans.",
            "A-level results day, baby Emma's arrival, and the collapse of Dante's university plans.",
        )],
        "content_html": [(
            "At the door is Melanie — Dante's ex-girlfriend,",
            "At the door is Melanie, known as Mel — Dante's ex-girlfriend,",
        )],
    },
    6: {
        "content_html": [
            (
                '<p data-narration-id="n27">Melanie is Dante\'s ex-girlfriend and Emma\'s mother.',
                '<p data-narration-id="n27">Melanie, known as Mel, is Dante\'s ex-girlfriend and Emma\'s mother.',
            ),
            # Duplicate narration id: exam-tip n28 collided with content n28.
        ],
    },
}

# Narration-id renumbering to clear duplicate-key collisions.
# lesson key -> field -> [(old_id, new_id)]
RENUMBER = {
    ("bdc", 6): {"exam_tip_html": [("n28", "n34")]},
    ("ci", 8): {"exam_tip_html": [("n33", "n38")],
                "conclusion_html": [("n34", "n39"), ("n35", "n40")]},
}


def apply_bdc(row):
    """Return {field: new_value} for one Boys Don't Cry lesson."""
    n = row["lesson_number"]
    if n in (1, 3):
        return {}
    out = {}
    prot = PROTECT.get(n, {})
    ref = REFINE.get(n, {})

    for f in TEXT_FIELDS + JSON_FIELDS:
        v = row.get(f)
        if v is None:
            continue
        is_json = f in JSON_FIELDS
        s = json.dumps(v, ensure_ascii=False) if is_json else v
        if not re.search(r"\b(Emma|Mel|Melanie|Bryce)\b", s):
            continue

        keeps = prot.get(f, [])
        for i, k in enumerate(keeps):
            assert s.count(k) == 1, f"L{n} {f}: protect string not unique: {k!r}"
            s = s.replace(k, SENT_KEEP + str(i) + SENT_KEEP)

        s = swap_names(s)

        for i, k in enumerate(keeps):
            s = s.replace(SENT_KEEP + str(i) + SENT_KEEP, k)

        for old, new in ref.get(f, []):
            assert s.count(old) == 1, f"L{n} {f}: refine target not unique: {old!r}"
            s = s.replace(old, new)

        for old_id, new_id in RENUMBER.get(("bdc", n), {}).get(f, []):
            tag = f'data-narration-id="{old_id}"'
            assert s.count(tag) == 1, f"L{n} {f}: renumber id not unique: {old_id}"
            s = s.replace(tag, f'data-narration-id="{new_id}"')

        assert "Bryce" not in s, f"L{n} {f}: residual Bryce"
        out[f] = json.loads(s) if is_json else s

    # Renumbering may touch a field with no name hits.
    for f, pairs in RENUMBER.get(("bdc", n), {}).items():
        if f in out:
            continue
        s = row.get(f) or ""
        for old_id, new_id in pairs:
            tag = f'data-narration-id="{old_id}"'
            assert s.count(tag) == 1, f"L{n} {f}: renumber id not unique: {old_id}"
            s = s.replace(tag, f'data-narration-id="{new_id}"')
        out[f] = s
    return out


# ── Curious Incident L8: AO labels ──────────────────────────────────────

CI_EDITS = {
    "content_html": [
        (
            '<p data-narration-id="n15">For AO4 (context), students should engage with '
            'the theatrical and cultural context of the 2012 National Theatre premiere.',
            '<p data-narration-id="n15">Context is AO3 in the assessment objectives. Note '
            'that Component 2 Section A — the post-1914 prose and drama question — is '
            'assessed on AO1, AO2 and AO4 only, so context earns no marks of its own here. '
            'It still sharpens your reading, so engage with the theatrical and cultural '
            'context of the 2012 National Theatre premiere.',
        ),
        (
            "analyse theatrical devices as well as language; embed AO4 context naturally "
            "(2012 National Theatre premiere, the challenge to the deficit model, "
            "Stephens's adaptation of Haddon); range across the whole play; and use "
            "precisely worded quotations from the play-text.",
            "analyse theatrical devices as well as language; use the play's context to "
            "deepen your reading of Stephens's choices (2012 National Theatre premiere, "
            "the challenge to the deficit model, Stephens's adaptation of Haddon); range "
            "across the whole play; and use precisely worded quotations from the "
            "play-text. Protect the five AO4 marks by writing accurately and ambitiously: "
            "varied sentence structures, precise vocabulary, correct spelling and "
            "punctuation.",
        ),
        (
            "<span>AO4 Context: What to Include</span>",
            "<span>Theatrical Context: What to Include</span>",
        ),
        (
            '<p data-narration-id="n28">For AO4, include context about <em>the play</em>, '
            'not just the novel. Useful AO4 points include:',
            '<p data-narration-id="n28">When you draw on context, focus on <em>the play</em>, '
            'not just the novel. Useful points include:',
        ),
        (
            "The novel's Whitbread Award is useful background context, but it is the "
            "play's theatrical context that is directly relevant for AO4 in the Eduqas "
            "exam.",
            "The novel's Whitbread Award is useful background, but it is the play's "
            "theatrical context that is directly relevant in the Eduqas exam.",
        ),
        (
            '<p data-narration-id="n29">Example AO4 sentence:',
            '<p data-narration-id="n29">Example context sentence:',
        ),
    ],
    "exam_tip_html": [
        (
            "When embedding AO4 context, prioritise the 2012 theatrical context "
            "(National Theatre premiere, Frantic Assembly, Olivier/Tony Awards) "
            "alongside the novel's 2003 background.",
            "When you refer to context, prioritise the 2012 theatrical context "
            "(National Theatre premiere, Frantic Assembly, Olivier/Tony Awards) "
            "alongside the novel's 2003 background. Remember that AO4 is the five marks "
            "for accurate, ambitious spelling, punctuation and vocabulary — write "
            "carefully to secure them.",
        ),
    ],
    "conclusion_html": [
        (
            '<li data-narration-id="n37">AO4 context must reference the play:',
            '<li data-narration-id="n37">Context must reference the play:',
        ),
    ],
}

CI_JSON_EDITS = {
    "knowledge_checks": [
        (
            "For AO4 in the Eduqas exam, students should prioritise the _____ context of "
            "Stephens's 2012 play, not just Haddon's 2003 novel.",
            "In the Eduqas exam, students should prioritise the _____ context of "
            "Stephens's 2012 play, not just Haddon's 2003 novel.",
        ),
    ],
    "glossary_terms": [
        (
            "Assessment Objective 4 — showing understanding of the relationships between "
            "texts and the contexts in which they were written, performed, and received. "
            "For this play, AO4 should reference the 2012 theatrical context.",
            "Assessment Objective 4 — using a range of vocabulary and sentence structures "
            "for clarity, purpose and effect, with accurate spelling and punctuation. It "
            "is worth 5 of the 40 marks on this question. Context is AO3, and AO3 is not "
            "assessed on the post-1914 prose and drama question.",
        ),
    ],
    "practice_questions": [
        (
            "AO4: challenges of family under pressure; single parenting of a child with "
            "additional needs.",
            "Context: challenges of family under pressure; single parenting of a child "
            "with additional needs.",
        ),
        (
            "AO4: 2012 theatrical context, neurodiversity discourse.\\nMid-high band "
            "(22-28): Clear analysis with AO4 embedded.",
            "Context: the 2012 theatrical production, neurodiversity discourse.\\nMid-high "
            "band (22-28): Clear analysis with context embedded.",
        ),
    ],
}

ACC_EDITS = {
    "content_html": [
        (
            "reads far weaker than ‘Dickens “flint”-like Scrooge is cold "
            "but capable of sparking change.’",
            "reads far weaker than ‘Dickens’s “flint”-like Scrooge is "
            "cold but capable of sparking change.’",
        ),
    ],
}


def apply_literal(row, text_edits, json_edits, renumber_key=None, tag=""):
    out = {}
    for f, pairs in (text_edits or {}).items():
        s = row.get(f) or ""
        for old, new in pairs:
            assert s.count(old) == 1, f"{tag} {f}: target not unique ({s.count(old)}): {old[:70]!r}"
            s = s.replace(old, new)
        out[f] = s
    for f, pairs in (json_edits or {}).items():
        s = json.dumps(row.get(f), ensure_ascii=False)
        for old, new in pairs:
            assert s.count(old) == 1, f"{tag} {f}: target not unique ({s.count(old)}): {old[:70]!r}"
            s = s.replace(old, new)
        out[f] = json.loads(s)
    if renumber_key:
        for f, pairs in RENUMBER.get(renumber_key, {}).items():
            s = out.get(f, row.get(f) or "")
            for old_id, new_id in pairs:
                t = f'data-narration-id="{old_id}"'
                assert s.count(t) == 1, f"{tag} {f}: renumber id not unique: {old_id}"
                s = s.replace(t, f'data-narration-id="{new_id}"')
            out[f] = s
    return out


# ── Main ────────────────────────────────────────────────────────────────

def main():
    sb = get_client()
    os.makedirs(OUT_DIR, exist_ok=True)

    targets = []  # (label, row, updates)

    bdc = sb.table("lessons").select("*").eq("unit_id", BDC_UNIT).order("lesson_number").execute().data
    for row in bdc:
        upd = apply_bdc(row)
        if upd:
            targets.append((f"boys-dont-cry L{row['lesson_number']}", row, upd))

    for slug, unit, num, te, je, rk in [
        ("english-literature-eduqas", "the-curious-incident", 8, CI_EDITS, CI_JSON_EDITS, ("ci", 8)),
        ("english-literature-ocr", "a-christmas-carol", 7, ACC_EDITS, None, None),
    ]:
        sid = sb.table("subjects").select("id").eq("slug", slug).execute().data[0]["id"]
        uid = sb.table("units").select("id").eq("subject_id", sid).eq("slug", unit).execute().data[0]["id"]
        row = sb.table("lessons").select("*").eq("unit_id", uid).eq("lesson_number", num).execute().data[0]
        label = f"{slug}/{unit} L{num}"
        targets.append((label, row, apply_literal(row, te, je, rk, label)))

    # ── Backup BEFORE the first write ──────────────────────────────────
    backup = {}
    for label, row, upd in targets:
        backup[row["id"]] = {
            "label": label,
            "lesson_number": row["lesson_number"],
            "title": row["title"],
            "fields": {f: row.get(f) for f in upd},
            "narration_manifest": row.get("narration_manifest"),
        }
    with open(BACKUP, "w", encoding="utf-8") as fh:
        json.dump(backup, fh, ensure_ascii=False, indent=1)
    print(f"Backup written: {BACKUP}  ({len(backup)} rows)\n")

    for label, row, upd in targets:
        print(f"── {label}  [{row['id']}]  fields: {', '.join(sorted(upd))}")
        for f in sorted(upd):
            old = row.get(f)
            new = upd[f]
            o = old if isinstance(old, str) else json.dumps(old, ensure_ascii=False)
            n = new if isinstance(new, str) else json.dumps(new, ensure_ascii=False)
            import difflib
            sm = difflib.SequenceMatcher(None, o, n, autojunk=False)
            for tag, i1, i2, j1, j2 in sm.get_opcodes():
                if tag == "equal":
                    continue
                print(f"   [{f}] -{o[max(0,i1-45):i2+45]!r}")
                print(f"   [{f}] +{n[max(0,j1-45):j2+45]!r}")
        print()

    if DRY:
        print("[DRY RUN] no writes.")
        return

    for label, row, upd in targets:
        sb.table("lessons").update(upd).eq("id", row["id"]).execute()
        print(f"[PATCH] {label}  {len(upd)} fields")
    print("\nDone.")


if __name__ == "__main__":
    main()
