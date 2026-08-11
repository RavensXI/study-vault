# -*- coding: utf-8 -*-
"""Replace the placeholder explanations in listening-skills L1-L3.

Tom, reviewing L1: the wrong-answer feedback was "some very generic feedback...
probably more applicable to maths or science". practice.html was the first
cause — it printed a maths fallback instead of the question's explanation — but
fixing that exposed the second: 28 of these explanations said nothing. They
were shaped

    "Verified answer: minor. This excerpt was composed so that its scale
     content makes the tonality unambiguous — check the method panel."

which states the answer and then sends the student away. A student who cannot
hear the difference is exactly the student reading this, and it does not tell
them what the difference SOUNDS like.

Each replacement names the audible cue that decides the answer and, where the
options invite a specific confusion, contrasts it with the option most likely
to have been chosen.

Two accuracy rules, because these are answer keys:

  * For CONSTRUCTED clips (L1, L3) every claim is a property of the CATEGORY —
    what a minor scale is, what a plagal cadence is — never a claim about what
    happens at a given second of audio, which nobody has verified by ear.
  * For REAL recordings (L2) the work and performer are named, so the answer
    stays auditable by someone who cannot hear the difference: they can check
    that Bach's Cello Suite is played on a cello. That is the same rule the
    tonality rebuild ran on.

    python fix_listening_explanations.py [--dry-run|--restore]
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

BACKUP = os.path.join(HERE, "_listening_explanations_backup.json")

# lesson -> tier -> 1-based question number -> (expected answer, explanation)
# The expected answer is asserted before writing: if a tier is ever reordered,
# this script must fail loudly rather than attach an explanation to the wrong
# question.
NEW = {
    1: {
        "bronze": {
            1: ("major",
                "Major. The note that decides it is the third degree of the scale: in major it sits a "
                "major third above the home note, and that is what gives the bright, settled colour. "
                "Lower that one note by a semitone and the same tune becomes minor."),
            2: ("minor",
                "Minor. A minor scale is a major scale with its third degree flattened by a semitone. "
                "Everything else can be identical, so the third is the note to listen for — it carries "
                "the darker colour on its own."),
            3: ("minor",
                "Minor. Tonality is not about whether music sounds sad; it is about which notes "
                "the scale uses. A flattened third is the test, and it is there whether the music is "
                "slow and mournful or fast and urgent."),
            4: ("pentatonic",
                "Pentatonic. Only five different notes are used in the whole scale, and no two of them "
                "are a semitone apart — the pattern you get from the black keys of a piano. Nothing can "
                "clash, so the sound is open and gapped. Major and minor both use seven notes and both "
                "contain semitone steps."),
        },
        "silver": {
            1: ("major",
                "Major. Seven notes, a major third above the home note, and a clear pull back to that "
                "home note. Pentatonic would use only five notes with no semitones; chromatic would "
                "move by semitone throughout and settle nowhere."),
            2: ("pentatonic",
                "Pentatonic. Five notes to the octave with no semitone steps. Whole-tone also avoids "
                "semitones, so the two are easy to confuse — but whole-tone has six notes and every "
                "step is exactly the same size, which leaves it floating with no home note. Pentatonic "
                "keeps a home note."),
            3: ("chromatic",
                "Chromatic. The line moves by semitone, using notes from outside the key, so no single "
                "key is established — a creeping, sliding effect. Whole-tone moves in steps twice that "
                "size, which sounds open and dreamlike rather than tight and sliding."),
            4: ("minor",
                "Minor. The flattened third gives the dark colour, but the scale is otherwise an "
                "ordinary seven-note scale and the music still settles on a home chord. Chromatic and "
                "whole-tone writing does not settle like that — that is what rules them out."),
        },
    },
    2: {
        "bronze": {
            1: ("woodwind",
                "Woodwind — a flute, playing Mozart's Flute Concerto K.313. Listen for the breath at "
                "the start of each note and the pure, hollow tone: the sound is made by air splitting "
                "across an edge, with no reed and no buzzing lips."),
            2: ("brass",
                "Brass — a solo bugle sounding Taps. Brass players buzz their lips into a mouthpiece, "
                "which gives that hard, ringing attack. A bugle has no valves at all, so it can only "
                "play the notes of one harmonic series — which is why bugle calls are built from leaps "
                "rather than steps."),
            3: ("strings",
                "Strings — a cello, playing the Prélude from Bach's first Cello Suite. The sound is "
                "made by a bow drawn across a string, so a note can begin quietly and swell, and the "
                "player never has to stop for breath."),
            4: ("percussion",
                "Percussion — timpani. The note is struck, so it starts with a thud and then rings on. "
                "Timpani are unusual among drums in having a definite, tunable pitch, which is why an "
                "orchestra can use them to reinforce the bass line rather than just to keep time."),
        },
        "silver": {
            1: ("woodwind",
                "Woodwind — an oboe, in Albinoni's Oboe Concerto Op. 9 No. 2. The oboe uses a double "
                "reed: two thin blades of cane vibrating against each other. That is what gives the "
                "thin, nasal, penetrating tone that carries over a whole string orchestra."),
            2: ("strings",
                "Strings — a full string section (the US Air Force Strings). Several players bow the "
                "same line together, so the sound is smooth and blended and never breaks for breath. "
                "That unbroken continuity is the clue that this is strings and not wind."),
            3: ("brass",
                "Brass — herald trumpets. Listen for the brilliant, cutting attack on every note, and "
                "for the fanfare shape: leaps built from the harmonic series rather than a stepwise "
                "tune."),
            4: ("percussion",
                "Percussion — tuned percussion: xylophone and marimba, wooden bars struck with "
                "mallets. Each note is short and dry with almost no sustain, so a long note has to be "
                "faked with a fast repeated roll. That is the giveaway."),
        },
        "gold": {
            1: ("woodwind",
                "Woodwind — a solo clarinet. A single reed beating against a mouthpiece gives a "
                "warmer, rounder tone than the oboe's double reed. The clarinet also has the widest "
                "range of the woodwinds, and its low register sounds noticeably darker and hollower "
                "than its high one."),
            2: ("strings",
                "Strings — a solo violin, the Adagio from Bach's first Sonata for unaccompanied "
                "violin. Bowed throughout, and you can hear chords made by drawing the bow across more "
                "than one string at once — something no wind instrument can do."),
            3: ("brass",
                "Brass — a solo trumpet sounding Taps. Bright, focused and lip-buzzed, with a clean "
                "attack on each note. Compare it with the flute question in this lesson: there each "
                "note begins with breath, here with a buzz."),
        },
    },
    3: {
        "silver": {
            1: ("simple time, in 2 or 4",
                "Simple time, in 2 or 4. Tap the pulse and the strong beats arrive in twos, and each "
                "beat divides neatly into two equal halves. Compound time (6/8) divides each beat into "
                "three, which produces a swinging lilt — count 'one-and-two-and' against "
                "'one-and-a-two-and-a' and you can hear which fits."),
            2: ("sequence",
                "A sequence. The same short melodic shape returns immediately but starting on a "
                "different note, so the pattern climbs or falls. Imitation would hand the idea to a "
                "different part instead; an ostinato would repeat it at exactly the same pitch."),
            3: ("perfect",
                "Perfect. The last two chords are V–I: the music arrives home and sounds finished, "
                "like a full stop. The test is whether you could stop there and feel settled."),
            4: ("plagal",
                "Plagal. The last two chords are IV–I. It still arrives home, but approaching from "
                "chord IV is gentler and less driven than the V–I of a perfect cadence. It is the "
                "'Amen' sung at the end of a hymn."),
        },
        "gold": {
            1: ("simple triple time, in 3",
                "Simple triple time, in 3. The pulse falls into groups of three — ONE-two-three, "
                "ONE-two-three — and each beat splits into two. Compound 6/8 can feel like it swings "
                "in threes as well, but there the beat splits into three and there are only two main "
                "beats in the bar, not three."),
            2: ("ostinato",
                "An ostinato. A short pattern repeats over and over at the same pitch while the music "
                "above it changes. A sequence would shift the pattern up or down each time; a drone "
                "would hold a single sustained note rather than a pattern."),
            3: ("melody and accompaniment",
                "Melody and accompaniment — a homophonic texture. One line clearly carries the tune "
                "and everything else supports it underneath. Monophonic would be one line with nothing "
                "under it at all; imitative polyphony would have two or more equal lines copying each "
                "other."),
            4: ("imperfect",
                "Imperfect. The music stops ON chord V, so it sounds unfinished — a comma, not a full "
                "stop. A perfect cadence uses the same chord V but carries it home to chord I."),
            5: ("interrupted",
                "Interrupted. Chord V sets the ear up for an ending on chord I, and then the music "
                "turns somewhere else instead — usually chord VI. That thwarted expectation is the "
                "whole effect, and it is why the cadence sounds like a surprise rather than an "
                "ending."),
        },
    },
}


AOS_BACKUP = os.path.join(HERE, "_aos_explanations_backup.json")


def strip_verified_prefix(sb, sub_id, dry):
    """'Verified answer: blue notes — the flattened third and seventh...'

    The five aos-listening explanations that survive the audit above say
    something real; they just open with build-pipeline jargon. "Verified
    answer:" is a note to ourselves about provenance and means nothing to a
    fifteen-year-old. Strip the prefix and keep the sentence.
    """
    unit = [u for u in sb.table("units").select("id,slug").eq("subject_id", sub_id)
            .execute().data if u["slug"] == "aos-listening"]
    if not unit:
        return 0
    rows = sb.table("lessons").select("id,lesson_number,practice_data") \
        .eq("unit_id", unit[0]["id"]).execute().data
    backup, n = {}, 0
    for row in rows:
        pd = json.loads(json.dumps(row["practice_data"]))
        hit = False
        for tier in pd.get("problem_bank", {}):
            for q in pd["problem_bank"][tier]:
                e = (q.get("explanation") or "").strip()
                if not e.startswith("Verified answer:"):
                    continue
                rest = e[len("Verified answer:"):].strip()
                q["explanation"] = rest[:1].upper() + rest[1:]
                hit, n = True, n + 1
        if hit:
            backup[str(row["lesson_number"])] = row["practice_data"]
            if not dry:
                sb.table("lessons").update({"practice_data": pd}).eq("id", row["id"]).execute()
    if backup and not dry and not os.path.exists(AOS_BACKUP):
        json.dump(backup, open(AOS_BACKUP, "w", encoding="utf-8"), indent=1)
    return n


def main():
    dry = "--dry-run" in sys.argv
    sb = get_client()
    sub = [x for x in sb.table("subjects").select("id,slug,school_id")
           .eq("slug", "music-aqa").execute().data if not x["school_id"]][0]
    unit = [u for u in sb.table("units").select("id,slug").eq("subject_id", sub["id"])
            .execute().data if u["slug"] == "listening-skills"][0]["id"]
    rows = {r["lesson_number"]: r for r in sb.table("lessons")
            .select("id,lesson_number,practice_data").eq("unit_id", unit).execute().data}

    if "--restore" in sys.argv:
        for n, pd in json.load(open(BACKUP, encoding="utf-8")).items():
            sb.table("lessons").update({"practice_data": pd}).eq("id", rows[int(n)]["id"]).execute()
        print("restored")
        return

    backup, changed = {}, 0
    for n, tiers in NEW.items():
        row = rows[n]
        backup[str(n)] = row["practice_data"]
        pd = json.loads(json.dumps(row["practice_data"]))
        for tier, items in tiers.items():
            bank = pd["problem_bank"][tier]
            for qno, (answer, text) in items.items():
                q = bank[qno - 1]
                got = q["options"][q["solutions"][0]]
                assert got == answer, "L%s %s q%s: expected answer %r, found %r" % (
                    n, tier, qno, answer, got)
                assert "&" not in text, "plain-text field must not carry HTML entities"
                # practice.html deals the bank in a random order every session,
                # so nothing may refer to what the student saw a moment ago.
                # \b matters: "against each other" contains "again".
                for phrase in ("again", "earlier", "previously", "last question",
                               "the question above", "as before"):
                    assert not re.search(r"\b%s\b" % phrase, text.lower()), \
                        "L%s %s q%s assumes question order: %r" % (n, tier, qno, phrase)
                q["explanation"] = text
                changed += 1
        # nothing may still be pointing the student at the method panel
        left = [q for t in pd["problem_bank"] for q in pd["problem_bank"][t]
                if "check the method panel" in (q.get("explanation") or "")
                or "listen again and focus on it" in (q.get("explanation") or "")]
        assert not left, "L%s still has %d placeholder explanation(s)" % (n, len(left))
        if not dry:
            sb.table("lessons").update({"practice_data": pd}).eq("id", row["id"]).execute()
        print("  L%s — %d explanations rewritten" % (n, sum(len(v) for v in tiers.values())))

    if not dry and not os.path.exists(BACKUP):
        json.dump(backup, open(BACKUP, "w", encoding="utf-8"), indent=1)

    stripped = strip_verified_prefix(sb, sub["id"], dry)
    if stripped:
        print("  aos-listening — %d 'Verified answer:' prefixes stripped" % stripped)
    print(("DRY RUN — " if dry else "") + "%d explanations replaced" % changed)


if __name__ == "__main__":
    main()
