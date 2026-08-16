# -*- coding: utf-8 -*-
"""Apply the music-ocr fact-check findings surgically (16 findings:
aos2 3, aos3 4, aos4 L4 4, aos5 5 — 9 HIGH).

Root fixes:
- Bach was never employed by the Margrave of Brandenburg — the 1721
  dedication was an unsolicited bid for patronage.
- Mozart's D major flute concerto K. 314 is No. 2 (No. 1 = G major
  K. 313); the L4 embed was an amateur upload of the wrong movement —
  replaced with the score video of the full concerto.
- The Israeli hora is a fast DUPLE dance, not triple (content, glossary
  and a KC distractor); dunun sizes ran backwards (kenkeni smallest,
  dundunba largest); stray CJK character removed.
- Halo: chant 4/4 over a compound-time ostinato (not irregular); embed
  honestly labelled as the Mjolnir Mix arrangement; Michael Salvatori
  co-credited. Also sprach: the famous C major/C minor alternation
  restored (not a plain triumphant C major).
- Livin' On A Prayer modulates UP A MINOR THIRD (E minor to G minor),
  not a semitone — fixed in content, mark scheme and flashcard. Dylan's
  1997 backing is piano, upright bass and organ (no harmonica). Kylie
  lyric quotation removed (no-lyrics rule).

Backup: _backup_ocr_factcheck_2026-08-16.json. Run: [--apply]
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

APPLY = "--apply" in sys.argv
BACKUP = os.path.join(HERE, "_backup_ocr_factcheck_2026-08-16.json")

OPS = [
    ("aos2-the-concerto-through-time", 1, [
        ("for aristocratic employers such as the Margrave of Brandenburg, "
         "to whom he dedicated a set of six concertos in 1721",
         "for aristocratic patrons such as Prince Leopold of Anhalt-"
         "K&ouml;then; in 1721 he also sent a set of six concertos to the "
         "Margrave of Brandenburg hoping to win his patronage, though the "
         "Margrave never employed him"),
    ]),
    ("aos2-the-concerto-through-time", 2, [
        ("Mozart - Flute Concerto No. 1 in D major, K. 314",
         "Mozart - Flute Concerto No. 2 in D major, K. 314"),
    ]),
    ("aos2-the-concerto-through-time", 4, [
        # embed replaced below (amateur video, wrong movement); caption
        # corrected to the numbered work with no movement claim — the
        # replacement video is the complete concerto with score
        ("Mozart - Flute Concerto in D major, K. 314, first movement",
         "Mozart - Flute Concerto No. 2 in D major, K. 314"),
        ("embed/ASTSWy1jfwA", "embed/Uy0gH_lPLXs"),
        ('title="Mozart: Flute Concerto in D major K314, 3rd movement '
         '(with my own cadenzas)"',
         'title="Mozart: Flute Concerto No. 2 in D major, K. 314/285d '
         '(with Score)"'),
    ]),
    ("aos3-rhythms-of-the-world", 1, [
        ("and微 microtonal", "and microtonal"),
    ]),
    ("aos3-rhythms-of-the-world", 2, [
        ("The hora is a well-known circle dance, traditionally in a fast "
         "triple metre",
         "The hora is a well-known circle dance, traditionally in a "
         "lively duple metre"),
        ("An Israeli circle dance, traditionally in a fast triple metre.",
         "An Israeli circle dance, traditionally in a lively duple metre."),
        ("An Israeli circle dance in triple metre",
         "An Israeli circle dance"),
        # a fourth echo the agent's list missed — found by the remnant sweep
        ("the hora's circular stepping in fast triple metre",
         "the hora's circular stepping in lively duple metre"),
    ]),
    ("aos3-rhythms-of-the-world", 3, [
        ("the largest and lowest-pitched kenkeni, the middle-sized "
         "sangban, and the largest dundunba",
         "the smallest and highest-pitched kenkeni, the middle-sized "
         "sangban, and the largest, lowest-pitched dundunba"),
    ]),
    ("aos4-film-music", 4, [
        ("set over a simple repeating ostinato figure in an irregular "
         "metre",
         "set over a simple repeating string ostinato in a rolling "
         "compound metre"),
        ("Martin O'Donnell - Halo Theme (Halo: Combat Evolved)",
         "Martin O'Donnell and Michael Salvatori - Halo Theme (Mjolnir "
         "Mix, the Halo 2 arrangement of the series theme)"),
        ("Martin O&rsquo;Donnell&rsquo;s theme for Halo is one of the "
         "most famous examples",
         "Martin O&rsquo;Donnell and Michael Salvatori&rsquo;s theme for "
         "Halo is one of the most famous examples"),
        ("Martin O&rsquo;Donnell (Halo)",
         "Martin O&rsquo;Donnell and Michael Salvatori (Halo)"),
        ("answered by full orchestra and timpani in a triumphant C major "
         "chord",
         "answered by full orchestra and timpani famously alternating "
         "between C major and C minor, so the harmony feels vast but "
         "unsettled"),
    ]),
    ("aos5-conventions-of-pop", 2, [
        ("where the music suddenly shifts up (commonly by a semitone) for "
         "the final chorus",
         "where the music suddenly shifts up &mdash; in this song a "
         "dramatic minor third, from E minor to G minor &mdash; for the "
         "final chorus"),
        ("Award marks for identifying modulation, typically upward by a "
         "semitone, and its effect of raising energy or intensity for the "
         "final chorus.",
         "Award marks for identifying modulation (in this song up a minor "
         "third, from E minor to G minor) and its effect of raising "
         "energy or intensity for the final chorus."),
        ("near the end of the song the music shifts up, typically by a "
         "semitone, to energise the final chorus.",
         "near the end of the song the music shifts up a minor third "
         "(E minor to G minor) to energise the final chorus."),
    ]),
    ("aos5-conventions-of-pop", 3, [
        ("over sparse piano and gentle backing, including harmonica, "
         "characteristic of his raw and understated production style",
         "over sparse piano, upright bass and organ, characteristic of "
         "his raw and understated production style"),
    ]),
    ("aos5-conventions-of-pop", 4, [
        ("The famous &lsquo;la la la&rsquo; vocal hook that opens and "
         "threads through the track",
         "The famous wordless vocal hook that opens and threads through "
         "the track"),
    ]),
]


def apply_ops(text, ops, counter):
    for old, new in ops:
        n = text.count(old)
        if n:
            text = text.replace(old, new)
            counter[old] = counter.get(old, 0) + n
    return text


def main():
    sb = get_client()
    sub = sb.table("subjects").select("id").eq("slug", "music-ocr") \
        .execute().data[0]["id"]
    units = {u["slug"]: u["id"] for u in
             sb.table("units").select("id,slug,subject_id").execute().data
             if u["subject_id"] == sub}
    backup, writes, counter = {}, [], {}
    for uslug, num, ops in OPS:
        row = sb.table("lessons").select(
            "id,content_html,exam_tip_html,conclusion_html,"
            "knowledge_checks,flashcard_questions,glossary_terms,"
            "practice_questions") \
            .eq("unit_id", units[uslug]).eq("lesson_number", num) \
            .execute().data[0]
        upd = {}
        for f in ("content_html", "exam_tip_html", "conclusion_html"):
            new = apply_ops(row.get(f) or "", ops, counter)
            if new != (row.get(f) or ""):
                upd[f] = new
        for f in ("knowledge_checks", "flashcard_questions",
                  "glossary_terms", "practice_questions"):
            blob = json.dumps(row.get(f) or [], ensure_ascii=False)
            new = apply_ops(blob, ops, counter)
            if new != blob:
                upd[f] = json.loads(new)
        if upd:
            backup[row["id"]] = {k: row.get(k) for k in upd}
            writes.append((row["id"], upd))
            print("%s L%d: %d field(s) changed" % (uslug, num, len(upd)))
        else:
            print("%s L%d: !! NO CHANGES — check ops" % (uslug, num))
    print("\nreplacement hits:")
    for k, v in sorted(counter.items(), key=lambda x: -x[1]):
        print("  %2d× %s" % (v, k[:66]))
    missed = [o for _, _, ops in OPS for o, _ in ops if o not in counter]
    for o in missed:
        print("!! NOT FOUND: %s" % o[:70])
    print("lessons to write: %d" % len(writes))
    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    if not os.path.exists(BACKUP):
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup))
    for lid, upd in writes:
        sb.table("lessons").update(upd).eq("id", lid).execute()
    print("applied.")


if __name__ == "__main__":
    main()
