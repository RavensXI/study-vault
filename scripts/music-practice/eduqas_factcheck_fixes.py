# -*- coding: utf-8 -*-
"""Apply the music-eduqas fact-check findings surgically (20 findings:
11 HIGH aos1, 3 aos2, 6 aos4 incl. 1 HIGH).

Root fixes:
- Badinerie key scheme was REVERSED (A ends in F sharp minor, the dominant
  minor — not D major) — corrected across content, tip, KCs, flashcards
  and mark schemes in aos1 L3+L4.
- The ternary listening example (Eine kleine Nachtmusik 2nd mvt) is a
  rondo — replaced with Chopin's 'Raindrop' Prelude.
- Africa's groove is a half-time FEEL (straight sixteenths), not a
  half-time shuffle (that is Rosanna) — corrected across aos4 L3+L4.
- Kalimba intro = layered Yamaha GS-1 synth + real marimba; solo synth is
  the CS-80 (not GX-1). Dhol dagga/tilli name the STICKS, not the heads.
- So What call is bass answered by piano+horns; Sweeney Todd menace is
  dissonant strings/organ/whistle, not synths; A Little Priest is a shared
  scheme, not an argument.

Backup: _backup_factcheck_fixes_2026-08-16.json. Run: [--apply]
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
BACKUP = os.path.join(HERE, "_backup_factcheck_fixes_2026-08-16.json")

# (unit, lesson, [(old, new)]) applied to content_html + exam_tip_html AND
# the JSON of the four question fields (fragments avoid quotes so the JSON
# string form matches too)
OPS = [
    ("aos2-music-for-ensemble", 2, [
        ("walking bass moves steadily under the famous piano-and-bass call",
         "bass states the famous opening call, answered by piano and horns together"),
    ]),
    ("aos2-music-for-ensemble", 3, [
        ("synthesised or distorted timbres for menace, as in",
         "dissonant strings, a tolling organ and a shrieking factory whistle for menace, as in"),
        ("dramatise an argument or two different points of view being expressed at once, as in",
         "let two characters spin ideas together at once, each with their own line, as in"),
    ]),
    ("aos4-popular-music", 2, [
        ("The bass side (called the dagga) is struck with a thick wooden stick",
         "The bass side is struck with a thick, curved wooden stick called the dagga"),
        ("The treble side (called the tilli) is struck with a thin, curved cane stick",
         "The treble side is struck with a thin, straight cane stick called the tilli"),
        ("the bass side (dagga) struck with a thick stick",
         "the bass side struck with the thick dagga stick"),
        ("the treble side (tilli) struck with a thin cane",
         "the treble side struck with the thin tilli cane stick"),
    ]),
    ("aos4-popular-music", 3, [
        ("Half-Time Shuffle", "Half-Time Groove"),
        ("combining a shuffle feel (a swung, triplet-based subdivision) with a "
         "half-time backbeat, where the snare drum falls less often",
         "building a half-time feel: the snare backbeat lands on beat 3 rather "
         "than beats 2 and 4, over steady sixteenth notes on the hi-hat, so the "
         "snare falls less often"),
        ("This combination of a half-time backbeat under a shuffled subdivision "
         "is what musicians mean by a half-time shuffle",
         "This half-time backbeat under a steady sixteenth-note subdivision is "
         "what musicians mean by a half-time feel"),
        ("identify the half-time shuffle groove and explain how the backbeat "
         "and shuffle feel combine",
         "identify the half-time groove and explain where the backbeat falls"),
        ("without naming the shuffle feel or the half-time backbeat",
         "without naming the half-time backbeat"),
        ("combining a swung, shuffle subdivision with a half-time backbeat",
         "placing the snare backbeat on beat 3 over a steady sixteenth-note subdivision"),
        ("What is a half-time shuffle groove?", "What is a half-time groove?"),
        # the generic replace below turned the woven embed caption into
        # "groove groove" on the first pass — this repairs it on re-runs
        ("half-time groove groove", "half-time drum groove"),
        ("This is not an acoustic instrument at all &mdash; it is created using "
         "a digital synthesizer programmed to sound percussive and metallic",
         "The pattern is a layered sound: a Yamaha GS-1 digital synthesizer "
         "programmed to sound percussive and metallic, doubled by a real "
         "acoustic marimba"),
        ("half-time shuffle", "half-time groove"),
        ("Half-time shuffle", "Half-time groove"),
    ]),
    ("aos4-popular-music", 4, [
        ("opens with a marimba and kalimba (thumb piano) ostinato",
         "opens with a layered ostinato &mdash; a Yamaha GS-1 synthesizer "
         "programmed to imitate a kalimba (thumb piano), doubled by a real marimba"),
        ("the opening marimba/kalimba ostinato", "the opening synth-and-marimba ostinato"),
        ("GX-1", "CS-80"),
        ("half-time shuffle groove", "half-time drum groove"),
    ]),
    ("aos1-forms-and-devices", 4, [
        ("arriving at a perfect cadence that confirms D major by the end of the section",
         "arriving at a perfect cadence that confirms F sharp minor by the end of the section"),
        ("The B section begins in the D major established",
         "The B section begins in the F sharp minor established"),
        ("B minor (tonic) moves to D major, its relative major, sharing the same key signature.",
         "B minor (tonic) moves to F sharp minor, its dominant minor."),
        ("One mark for B minor (tonic), one mark for D major (relative major/reached by end of A).",
         "One mark for B minor (tonic), one mark for F sharp minor (dominant minor, reached by the end of A)."),
        ("the modulation from B minor to D major sounds smooth",
         "the modulation from B minor to F sharp minor sounds smooth"),
        ("to the relative major, D major", "to F sharp minor, the dominant minor"),
        ("relative major D major", "F sharp minor (dominant minor)"),
        ("the relative major (D major)", "the dominant minor (F sharp minor)"),
    ]),
    ("aos1-forms-and-devices", 3, [
        ("modulates during its course to the relative major, D major, ending there",
         "modulates during its course to F sharp minor, the dominant minor, ending there"),
        ("from the tonic B minor to the relative major, D major, before Section B returns",
         "from the tonic B minor to F sharp minor, the dominant minor, before Section B works its way back"),
        ("Section A moves from the tonic B minor to the relative major D major; "
         "Section B returns from D major/related keys back to B minor",
         "Section A moves from the tonic B minor to F sharp minor (dominant "
         "minor); Section B begins in F sharp minor and returns via related "
         "keys, including D major, back to B minor"),
        ("Section A moving from B minor to relative major D major",
         "Section A moving from B minor to F sharp minor (dominant minor)"),
        ("Section B returning from D major/related keys",
         "Section B beginning in F sharp minor and returning via related keys"),
        ("to the relative major, D major", "to F sharp minor, the dominant minor"),
        ("relative major D major", "F sharp minor (dominant minor)"),
        ("try to spot the point where the music seems to settle into a "
         "brighter, major-key sound before the first section ends &mdash; "
         "this is the shift from B minor towards its relative major, D major.",
         "try to spot the point where the music moves away from its home key "
         "before the first section ends &mdash; this is the shift from B "
         "minor to F sharp minor, its dominant minor."),
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
    sub = sb.table("subjects").select("id").eq("slug", "music-eduqas").execute().data[0]["id"]
    units = {u["slug"]: u["id"] for u in sb.table("units").select("id,slug,subject_id")
             .execute().data if u["subject_id"] == sub}
    backup, writes = {}, []
    counter = {}
    for uslug, num, ops in OPS:
        row = sb.table("lessons").select(
            "id,content_html,exam_tip_html,conclusion_html,knowledge_checks,"
            "flashcard_questions,glossary_terms,practice_questions") \
            .eq("unit_id", units[uslug]).eq("lesson_number", num).execute().data[0]
        upd = {}
        for f in ("content_html", "exam_tip_html", "conclusion_html"):
            new = apply_ops(row.get(f) or "", ops, counter)
            if new != (row.get(f) or ""):
                upd[f] = new
        for f in ("knowledge_checks", "flashcard_questions", "glossary_terms",
                  "practice_questions"):
            blob = json.dumps(row.get(f) or [], ensure_ascii=False)
            new = apply_ops(blob, ops, counter)
            if new != blob:
                upd[f] = json.loads(new)
        # L1 ternary example + L4 KC handled specially below
        if upd:
            backup[row["id"]] = {k: row.get(k) for k in upd}
            writes.append((row["id"], upd, "%s L%d" % (uslug, num)))
            print("%s L%d: %d field(s) changed" % (uslug, num, len(upd)))

    # aos1 L1: swap the mis-labelled ternary example (whole figure + PQ text)
    l1 = sb.table("lessons").select(
        "id,content_html,practice_questions") \
        .eq("unit_id", units["aos1-forms-and-devices"]).eq("lesson_number", 1) \
        .execute().data[0]
    ch = l1["content_html"]
    figm = re.search(r'<figure class="sv-listen"[^>]*>(?:(?!</figure>).)*'
                     r'Eine kleine Nachtmusik(?:(?!</figure>).)*</figure>', ch, re.S)
    pq = json.dumps(l1["practice_questions"], ensure_ascii=False)
    if figm:
        nid = re.search(r'data-narration-id="([^"]+)"', figm.group(0))
        newfig = ('<figure class="sv-listen"%s><figcaption class="sv-listen-label">'
                  "Listen &mdash; Chopin, &lsquo;Raindrop&rsquo; Prelude, Op. 28 "
                  "No. 15: the calm opening idea (A), the stormy minor-key middle "
                  "(B), and the return of the opening (A)</figcaption></figure>"
                  % ((' data-narration-id="%s"' % nid.group(1)) if nid else ""))
        ch2 = ch.replace(figm.group(0), newfig)
        pq2 = re.sub(r"the Romance from[^\"]*Eine kleine Nachtmusik[^\"]*?(?=[\".,)])",
                     "Chopin's 'Raindrop' Prelude", pq)
        pq2 = pq2.replace("Eine kleine Nachtmusik", "Chopin's 'Raindrop' Prelude")
        upd = {"content_html": ch2}
        if pq2 != pq:
            upd["practice_questions"] = json.loads(pq2)
        backup[l1["id"]] = {"content_html": ch, "practice_questions": l1["practice_questions"]}
        writes.append((l1["id"], upd, "aos1 L1 ternary example"))
        print("aos1 L1: ternary example swapped to Raindrop Prelude "
              "(narration id preserved: %s)" % (nid.group(1) if nid else "none"))
    else:
        print("aos1 L1: !! Eine kleine figure NOT FOUND — check manually")

    # aos1 L4 KC: 'modulate to by its close' — correct answer becomes dominant minor
    l4 = sb.table("lessons").select("id,knowledge_checks") \
        .eq("unit_id", units["aos1-forms-and-devices"]).eq("lesson_number", 4) \
        .execute().data[0]
    kcs = l4["knowledge_checks"]
    changed = False
    for k in kcs:
        if "modulate to by its close" in k.get("q", ""):
            k["options"][k["correct"]] = "The dominant minor (F sharp minor)"
            changed = True
            print("aos1 L4 KC: correct option rewritten -> dominant minor")
    if changed:
        backup.setdefault(l4["id"], {})["knowledge_checks"] = \
            json.loads(json.dumps(l4["knowledge_checks"]))
        writes.append((l4["id"], {"knowledge_checks": kcs}, "aos1 L4 KC"))

    print("\nreplacement hits:")
    for k, v in sorted(counter.items(), key=lambda x: -x[1])[:12]:
        print("  %2d× %s" % (v, k[:70]))
    print("lessons to write: %d" % len(writes))
    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    if not os.path.exists(BACKUP):
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup))
    for lid, upd, label in writes:
        sb.table("lessons").update(upd).eq("id", lid).execute()
    print("applied.")


if __name__ == "__main__":
    main()
