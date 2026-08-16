# -*- coding: utf-8 -*-
"""Apply the music-edexcel fact-check findings (41 findings, 31 HIGH —
the set-work board: every claim checkable against the published guides).

Two layers:
1. GENERIC: each finding's exact `claim` string replaced by its
   `correction` wherever it appears in the lesson's fields (the agents
   quoted exact text). Misses are reported loudly for layer 2.
2. HAND OPS: pervasive term swaps and my own player-pin/credit errors —
   Samba Em Preludio is 2008 (Esperanza), the bass is Pearson's
   "acoustic bass guitar", the opening is a SOLO BASS intro and the
   centrepiece a 34-bar GUITAR solo; Brandenburg entries are
   violin-first; plus KC/flashcard structured rewrites.

Backup: _backup_edexcel_factcheck_2026-08-16.json. Run: [--apply]
"""
import glob
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
BACKUP = os.path.join(HERE, "_backup_edexcel_factcheck_2026-08-16.json")
FIELDS_HTML = ("content_html", "exam_tip_html", "conclusion_html",
               "description")
FIELDS_JSON = ("knowledge_checks", "flashcard_questions", "glossary_terms",
               "practice_questions")

# glossary entries to REMOVE before any text ops run
PRE_DROP_GLOSSARY = {
    ("aos4-fusions", 4): ["String ensemble"],
    ("aos4-fusions", 5): ["String ensemble"],
}

HAND_OPS = {
    ("aos1-instrumental-music", 1): [
        ("The finale is a lively gigue in binary form, built largely from "
         "imitative entries",
         "The finale is a lively gigue in da capo (A&ndash;B&ndash;A) "
         "form, built largely from imitative entries"),
        ("Watching a real performance also shows you something a score "
         "cannot: the physical negotiation between three soloists reading "
         "each other&rsquo;s cues",
         "Listening with a performance in front of you, follow the three "
         "soloists in constant dialogue"),
        ("As you watch a performance, notice the physical intensity "
         "required &mdash; sudden fortissimo chords, rapid scalic and "
         "arpeggio passagework, and the pianist&rsquo;s use of pedal to "
         "sustain the brooding G",
         "As you listen, notice the intensity &mdash; sudden fortissimo "
         "chords, rapid scalic and arpeggio passagework, and pedalled "
         "resonance sustaining the brooding G"),
        ("aimed at concert halls rather than palace chambers",
         "leaving the confined world of the palace chamber behind"),
    ],
    ("aos1-instrumental-music", 2): [
        ("the flute states the theme first, the violin answers with the "
         "same material a little later, and the harpsichord then enters",
         "the violin states the theme first, the flute answers with the "
         "same material a little later, and the harpsichord then enters"),
        ("flute, then violin, then harpsichord",
         "violin, then flute, then harpsichord"),
        ("identifying the fugal imitative entries in order: flute, "
         "violin, harpsichord",
         "identifying the fugal imitative entries in order: violin, "
         "flute, harpsichord"),
        ("flute enters first, answered by the violin",
         "violin enters first, answered by the flute"),
        ("With a fugal exposition where the flute leads",
         "With a fugal exposition where the violin leads"),
    ],
    ("aos1-instrumental-music", 3): [
        ("The movement opens with the harpsichord alone stating a quick, "
         "dancing subject built from running quavers and semiquavers. "
         "This subject is then taken up in turn by violin and flute in "
         "imitation",
         "The movement opens with the violin stating a quick, dancing "
         "subject built from running quavers and semiquavers. This "
         "subject is then taken up in turn by flute and harpsichord in "
         "imitation"),
        ("the relative minor of the dominant area, B minor",
         "the relative minor, B minor"),
        ("noting the harpsichord states the subject first",
         "noting the violin states the subject first"),
    ],
    ("aos1-instrumental-music", 4): [
        ("once bridging the development into the recapitulation, and "
         "once, very briefly, just before the final coda",
         "once at the very start of the development, and once, very "
         "briefly, just before the final coda"),
        ("identifying where it returns (before recapitulation, before "
         "coda)",
         "identifying where it returns (at the start of the development, "
         "and before the coda)"),
    ],
    ("aos2-vocal-music", 3): [
        ("eight-bar", "three-bar"),
        ("roughly thirty-four times", "nine or ten times"),
        ("originally likely a countertenor or alto voice for the stage "
         "production",
         "most usually a tenor today, though the prescribed edition is "
         "notated for soprano"),
    ],
    ("aos2-vocal-music", 4): [
        ("it became Queen&rsquo;s first UK Top 10 hit",
         "it reached No. 2 in the UK &mdash; their biggest hit yet, after "
         "Seven Seas of Rhye had already given them their first Top 10 "
         "entry"),
    ],
    ("aos2-vocal-music", 5): [
        ("Many listeners and analysts describe an underlying swung, "
         "compound-feel groove sitting against the song&rsquo;s notated "
         "simple-time pulse",
         "The song is notated in compound time (12/8), so the rolling, "
         "triplet-based swing IS the written metre"),
        ("There are two main verses, each followed by a chorus",
         "There are three verses and three choruses, each verse leading "
         "into a chorus"),
        ("Between the second chorus and the final section comes a guitar "
         "solo played by Brian May, performed in his signature "
         "multi-tracked, harmonised style rather than as a single melodic "
         "line.",
         "After the second chorus comes Brian May&rsquo;s guitar solo "
         "&mdash; performed in his signature multi-tracked, harmonised "
         "style rather than as a single melodic line &mdash; followed by "
         "a full third verse before the final chorus."),
        ("between the second chorus and the varied final section",
         "after the second chorus, before the third verse and the final "
         "chorus"),
    ],
    ("aos4-fusions", 2): [
        ("A central expressive element of Release is its guest vocal line",
         "A central expressive element of Release is its vocal line"),
        ("associated with singers such as Iarla &Oacute; Lionaird, who "
         "has performed with Afro Celt Sound System.",
         "associated above all with Iarla &Oacute; Lionaird, Afro Celt "
         "Sound System&rsquo;s own singer; on the album track the guest "
         "vocalist Sin&eacute;ad O&rsquo;Connor sings in a similarly "
         "free, keening style."),
    ],
    # (unit, lesson): [(old, new)]
    ("aos4-fusions", 4): [
        ("The recording begins with a stripped-back duet texture: "
         "Spalding&rsquo;s voice paired with her own double bass playing.",
         "The recording begins with the acoustic bass guitar alone; the "
         "voice joins moments later in a stripped-back rubato duet."),
        ("voice, double bass, guitar and strings",
         "voice, acoustic bass guitar and acoustic guitar"),
        ("A large bowed or plucked string instrument providing the lowest "
         "pitched line in jazz ensembles.",
         "An acoustic-bodied bass guitar whose four strings provide the "
         "lowest pitched line in this recording."),
        ("double bass", "acoustic bass guitar"),
        ("Double bass", "Acoustic bass guitar"),
        ("(2010)", "(2008)"),
        ("Voice and bass alone", "Solo bass introduction"),
        ("The duet opening &mdash; rubato, intimate, the double bass as "
         "the only harmony.",
         "Spalding opens ALONE on the acoustic bass guitar &mdash; rubato, "
         "intimate, the bass line as the only harmony before the voice "
         "enters."),
        ("Spalding opens ALONE on the acoustic bass guitar &mdash; rubato, "
         "intimate, the acoustic bass guitar as the only harmony",
         "Spalding opens ALONE on the acoustic bass guitar &mdash; rubato, "
         "intimate, the bass line as the only harmony"),
        ("Bass solo", "Guitar solo"),
        ("The virtuosic centrepiece &mdash; foundation instrument as "
         "soloist.",
         "The extended acoustic guitar solo &mdash; the track's "
         "improvisatory centrepiece."),
        ("string ensemble", "guitar-led texture"),
        ("String ensemble", "Guitar-led texture"),
    ],
    ("aos4-fusions", 5): [
        ("opens in free time, or rubato, with just voice and double bass "
         "moving flexibly",
         "opens in free time, or rubato, with the acoustic bass guitar "
         "alone, the voice joining moments later, both moving flexibly"),
        ("The centrepiece of the recording is an extended, virtuosic "
         "double bass solo, where Spalding improvises",
         "The centrepiece of the recording is an extended, virtuosic "
         "acoustic guitar solo, where the guitar improvises"),
        ("the piece begins as a duet between voice and double bass",
         "the piece begins with solo bass, quickly growing into a duet "
         "between voice and acoustic bass guitar"),
        ("mostly voice and double bass, occasionally joined by light "
         "guitar",
         "mostly voice and acoustic bass guitar, joined by acoustic "
         "guitar"),
        ("double bass", "acoustic bass guitar"),
        ("Double bass", "Acoustic bass guitar"),
        ("(2010)", "(2008)"),
        ("Voice and bass alone", "Solo bass introduction"),
        ("The duet opening &mdash; rubato, intimate, the double bass as "
         "the only harmony.",
         "Spalding opens ALONE on the acoustic bass guitar &mdash; rubato, "
         "intimate, the bass line as the only harmony before the voice "
         "enters."),
        ("The duet opening &mdash; rubato, intimate, the acoustic bass "
         "guitar as the only harmony.",
         "Spalding opens ALONE on the acoustic bass guitar &mdash; rubato, "
         "intimate, the bass line as the only harmony before the voice "
         "enters."),
        ("Bass solo", "Guitar solo"),
        ("The virtuosic centrepiece &mdash; foundation instrument as "
         "soloist.",
         "The extended acoustic guitar solo &mdash; the track's "
         "improvisatory centrepiece."),
        ("string ensemble", "guitar-led texture"),
        ("String ensemble", "Guitar-led texture"),
    ],
    ("aos4-fusions", 1): [
        ("and passages of wordless scat-style vocal improvisation.",
         "and her supple, jazz-inflected vocal phrasing."),
        ("double bass", "acoustic bass guitar"),
        ("Double bass", "Acoustic bass guitar"),
    ],
}


def load_findings():
    out = []
    for path in glob.glob(os.path.join(HERE, "..", "_fact_check",
                                       "_edexcel_aos*_findings.json")):
        out.extend(json.load(io.open(path, encoding="utf-8")))
    return out


def apply_text(text, ops, counter):
    for old, new in ops:
        n = text.count(old)
        if n:
            text = text.replace(old, new)
            counter[old[:60]] = counter.get(old[:60], 0) + n
    return text


def main():
    sb = get_client()
    sub = sb.table("subjects").select("id").eq("slug", "music-edexcel") \
        .execute().data[0]["id"]
    units = {u["slug"]: u["id"] for u in
             sb.table("units").select("id,slug,subject_id").execute().data
             if u["subject_id"] == sub}
    findings = load_findings()
    by_lesson = {}
    for f in findings:
        key = (f["unit"], int(f["lesson"]))
        by_lesson.setdefault(key, []).append(f)
    for key in HAND_OPS:
        by_lesson.setdefault(key, [])

    backup, writes, counter, missed = {}, [], {}, []
    for (uslug, num), fl in sorted(by_lesson.items()):
        row = sb.table("lessons").select(
            "id," + ",".join(FIELDS_HTML + FIELDS_JSON)) \
            .eq("unit_id", units[uslug]).eq("lesson_number", num) \
            .execute().data[0]
        ops = []
        for f in fl:
            claim = f.get("claim") or ""
            corr = f.get("correction") or ""
            if claim and corr and len(claim) > 15:
                ops.append((claim, corr))
            else:
                missed.append("%s L%d: no usable claim/correction (%s)"
                              % (uslug, num, (f.get("problem") or "")[:60]))
        ops += HAND_OPS.get((uslug, num), [])
        ops.sort(key=lambda p: -len(p[0]))  # longest first: no self-shadowing
        upd = {}
        drops = PRE_DROP_GLOSSARY.get((uslug, num))
        if drops:
            gl = [g for g in (row.get("glossary_terms") or [])
                  if g.get("term") not in drops]
            if len(gl) != len(row.get("glossary_terms") or []):
                upd["glossary_terms"] = gl
                row = dict(row)
                row["glossary_terms"] = gl
                print("%s L%d: dropped glossary %s" % (uslug, num, drops))
        found_here = set()
        for fld in FIELDS_HTML:
            t = row.get(fld) or ""
            new = t
            for old, newv in ops:
                if old in new:
                    found_here.add(old)
                    new = new.replace(old, newv)
                    counter[old[:60]] = counter.get(old[:60], 0) + 1
            if new != t:
                upd[fld] = new
        for fld in FIELDS_JSON:
            blob = json.dumps(row.get(fld) or [], ensure_ascii=False)
            new = blob
            for old, newv in ops:
                oldj = json.dumps(old, ensure_ascii=False)[1:-1]
                newj = json.dumps(newv, ensure_ascii=False)[1:-1]
                if oldj in new:
                    found_here.add(old)
                    new = new.replace(oldj, newj)
                    counter[old[:60]] = counter.get(old[:60], 0) + 1
            if new != blob:
                upd[fld] = json.loads(new)
        for old, _ in ops:
            if old not in found_here:
                missed.append("%s L%d NOT FOUND: %s" % (uslug, num, old[:80]))
        if upd:
            backup[row["id"]] = {k: row.get(k) for k in upd}
            writes.append((row["id"], upd))
            print("%s L%d: %d field(s) changed" % (uslug, num, len(upd)))

    print("\nhits: %d distinct ops" % len(counter))
    print("lessons to write: %d" % len(writes))
    if missed:
        print("\n!! %d MISSES (need manual ops):" % len(missed))
        for m in missed:
            print("   ", m)
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
