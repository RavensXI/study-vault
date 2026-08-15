# -*- coding: utf-8 -*-
"""AOS1-4: ear-vs-fact classifier (Tom's review, agreed 14 Aug).

The principle Tom signed off: a question with an audio excerpt attached must
be answerable BY EAR (instrument/family, texture, metre, tonality as
major/minor, cadence, device, dynamics, tempo character, period by style).
A fact only study can supply — key NAMES, opus/K numbers, dates, movement
numbers, work titles, composer names — must not masquerade as listening.

This is ANSWER-based, not audio-presence-based: it reads the correct answer
(and question) of every problem in the music practice units and flags
excerpt-attached problems whose answers are unhearable facts.

Output: EAR_VS_FACT_WORKLIST_2026-08-15.md — a desk file with drafted
rewrites for Tom. NOTHING is applied to the database.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

OUT = os.path.join(HERE, "EAR_VS_FACT_WORKLIST_2026-08-15.md")
UNITS = ["western-classical-1650-1910", "score-reading", "listening-skills",
         "aos-listening"]

KEY_NAME = re.compile(r"\b[A-G](\s?(flat|sharp|&#9837;|&#9839;|b|#))?\s+(major|minor)\b", re.I)
CATALOGUE = re.compile(r"\b(K\.?\s?\d+|[Oo]p(us|\.)\s?\d+|BWV\s?\d+|Hob\.)", )
YEAR = re.compile(r"\b(1[5-9]\d\d|20[0-2]\d)\b")
MOVEMENT = re.compile(r"\b(first|second|third|fourth|1st|2nd|3rd|4th)\s+movement\b", re.I)
COMPOSERS = re.compile(r"\b(Mozart|Beethoven|Haydn|Handel|Bach|Chopin|Schumann|Verdi|"
                       r"Purcell|Vivaldi|Brahms|Tchaikovsky|Elgar|Schubert)\b")

HEARABLE_HINT = re.compile(r"\b(instrument|family|texture|metre|meter|cadence|tonality|"
                           r"major or minor|tempo|dynamic|device|ostinato|drone|sequence|"
                           r"syncopat|staccato|legato|conjunct|disjunct|period|era|style)\b", re.I)


def txt(x):
    return re.sub(r"<[^>]+>", " ", str(x or ""))


def classify(question, answer):
    """Returns (verdict, reason). verdict: 'fact' | 'review' | 'ear'."""
    q, a = txt(question), txt(answer)
    if CATALOGUE.search(a) or CATALOGUE.search(q) and CATALOGUE.search(a):
        return "fact", "catalogue number in the answer"
    if YEAR.search(a):
        return "fact", "specific year as the answer"
    if KEY_NAME.search(a):
        # major/minor alone is hearable; a NAMED key is not (no perfect pitch)
        if re.fullmatch(r"\s*(major|minor)\s*", a, re.I):
            return "ear", ""
        return "fact", "named key as the answer (students cannot hear absolute key)"
    if COMPOSERS.search(a):
        return "fact", "composer name as the answer"
    if MOVEMENT.search(a) or MOVEMENT.search(q) and not HEARABLE_HINT.search(q):
        return "review", "movement number involved — check the ear can answer it"
    if CATALOGUE.search(q) or YEAR.search(q):
        return "review", "question cites catalogue/date facts — check what the answer needs"
    return "ear", ""


def draft(question, answer, reason, has_audio):
    """A rewrite suggestion for the desk file."""
    if not has_audio:
        return ("Keep as a fact/recall question (no excerpt attached) — no change "
                "needed unless it reads as listening.")
    if "catalogue" in reason or "year" in reason:
        return ("Detach the excerpt and keep this as a recall question, OR keep the "
                "excerpt and ask a hearable property of it instead (instrument "
                "family, texture, metre, major/minor, cadence at the end).")
    if "named key" in reason:
        return ("Ask 'major or minor?' of the excerpt (hearable), or show the score "
                "and ask the student to READ the key signature (score-reading skill). "
                "Naming a key purely by ear is not a GCSE skill.")
    if "composer" in reason:
        return ("Rewrite to period/style-by-features ('Which period does this belong "
                "to? What features tell you?'), which IS hearable, or detach the audio.")
    return "Check by ear; rewrite to a hearable property if it fails."


def main():
    sb = get_client()
    subj = [s for s in sb.table("subjects").select("id,slug").execute().data
            if s["slug"] == "music-aqa"][0]["id"]
    units = {u["slug"]: u["id"] for u in sb.table("units").select("id,slug")
             .eq("subject_id", subj).execute().data}

    rows = []
    counts = {"ear": 0, "fact": 0, "review": 0}
    for uslug in UNITS:
        if uslug not in units:
            continue
        for l in sb.table("lessons").select("lesson_number,practice_data") \
                .eq("unit_id", units[uslug]).order("lesson_number").execute().data:
            pd = l.get("practice_data") or {}
            for tier in ("bronze", "silver", "gold"):
                for i, p in enumerate((pd.get("problem_bank") or {}).get(tier) or []):
                    q = p.get("question") or ""
                    sol = p.get("solutions", [None])[0]
                    opts = p.get("options") or []
                    ans = opts[sol] if (opts and isinstance(sol, int) and sol < len(opts)) \
                        else (p.get("answer") or "")
                    verdict, reason = classify(q, ans)
                    counts[verdict] += 1
                    if verdict != "ear":
                        rows.append({
                            "unit": uslug, "lesson": l["lesson_number"],
                            "tier": tier, "idx": i, "verdict": verdict,
                            "reason": reason, "has_audio": bool(p.get("passage_id")),
                            "passage": p.get("passage_id") or "",
                            "q": txt(q).strip()[:180], "a": txt(ans).strip()[:80],
                        })

    md = io.StringIO()
    md.write("# Ear-vs-fact worklist — music-aqa practice (15 Aug 2026)\n\n")
    md.write("Principle (agreed 14 Aug): an excerpt-attached question must be "
             "answerable by ear. Facts (key names, opus numbers, dates, composers) "
             "must not masquerade as listening.\n\n")
    md.write("**Nothing here has been applied — every rewrite is a draft for your "
             "call.**\n\n")
    md.write("Scanned every problem in %s.\nVerdicts: %d hearable, %d fact-as-"
             "listening, %d needs-review.\n\n" % (", ".join(UNITS), counts["ear"],
                                                  counts["fact"], counts["review"]))
    for verdict in ("fact", "review"):
        hits = [r for r in rows if r["verdict"] == verdict]
        md.write("\n## %s (%d)\n\n" % ("Fact answers on listening questions"
                                       if verdict == "fact" else "Borderline — needs your ear",
                                       len(hits)))
        for r in hits:
            md.write("### %s L%d %s[%d]%s\n" % (r["unit"], r["lesson"], r["tier"],
                                                r["idx"],
                                                " — 🔊 excerpt attached: `%s`" % r["passage"]
                                                if r["has_audio"] else " — no excerpt"))
            md.write("- **Q:** %s\n- **Answer:** %s\n- **Why flagged:** %s\n"
                     % (r["q"], r["a"], r["reason"]))
            md.write("- **Draft:** %s\n\n" % draft(r["q"], r["a"], r["reason"],
                                                   r["has_audio"]))
    io.open(OUT, "w", encoding="utf-8").write(md.getvalue())
    print("verdicts:", counts)
    print("flagged with audio:", sum(1 for r in rows if r["has_audio"]))
    print("flagged without audio:", sum(1 for r in rows if not r["has_audio"]))
    print("worklist ->", OUT)


if __name__ == "__main__":
    main()
