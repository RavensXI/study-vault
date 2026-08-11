# -*- coding: utf-8 -*-
"""Bring the gold tier to 4 on the eight AoS1 listening-practice lessons.

Gold sat at 1-2, so a 4-streak was impossible and 75% demanded every question.

These are all ANALYSIS questions grounded in what the lesson already documents
or in established fact about the work — form, key, scoring, historical context,
cross-piece comparison. None asks the student to identify something new by ear,
because the audio cannot be verified from here and a wrong key in an ear
question is unfixable by reading. The existing ear questions are untouched.

    python scripts/fix_music_wc_gold.py --dry-run
    python scripts/fix_music_wc_gold.py
    python scripts/fix_music_wc_gold.py --restore
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

BACKUP = os.path.join(HERE, "_music_wc_gold_backup.json")
UNIT = "western-classical-1650-1910"


def q(pid, text, opts, correct, expl):
    return {"input_type": "multiple_choice", "passage_id": pid, "question": text,
            "options": opts, "solutions": [correct], "explanation": expl}


GOLD = {
1: ("beethoven-sym1-mvt1", [
    ("Beethoven's First Symphony is scored for a Classical orchestra. Which combination best "
     "describes the forces he uses?",
     ["Strings and continuo only",
      "Strings, pairs of woodwind, horns, trumpets and timpani",
      "Strings, harp, tuba and a large percussion section",
      "A solo instrument with orchestral accompaniment"], 1,
     "This is the standard late-Classical orchestra: strings with woodwind in pairs, plus horns, "
     "trumpets and timpani. The continuo had gone by 1800, and tuba, harp and expanded percussion "
     "belong to the Romantic orchestra that came later."),
    ("Why is the opening chord of the symphony considered daring for 1800?",
     ["It is played by the timpani alone",
      "It is a dominant seventh belonging to a different key from the home key",
      "It is played fortissimo without warning",
      "It uses an instrument not normally found in an orchestra"], 1,
     "The symphony is in C major, but the first chord is a dominant seventh pulling towards F major. "
     "Beethoven delays confirming the home key, so the listener is briefly unsure where the music "
     "stands — harmonic unease used deliberately, which points towards the Romantic era.")]),
2: ("mozart-40-mvt1", [
    ("Symphony No. 40 is one of only two Mozart symphonies in a minor key. What effect does the "
     "minor tonality have on its character?",
     ["It makes the music sound triumphant and ceremonial",
      "It contributes to the restless, agitated mood the work is known for",
      "It means the piece has no clear home key",
      "It requires a smaller orchestra"], 1,
     "G minor gives the movement its urgent, unsettled quality. Minor-key symphonies were unusual "
     "for Mozart, and this one is often linked with the Sturm und Drang style — storm and stress."),
    ("The first movement is in sonata form. What happens to the second subject between the "
     "exposition and the recapitulation?",
     ["It disappears entirely",
      "It returns in the tonic key rather than the contrasting key",
      "It is played by a different instrument family",
      "It is heard twice as fast"], 1,
     "In a minor-key movement the second subject appears in the relative major during the "
     "exposition, then returns in the tonic in the recapitulation. That resolution of the key "
     "conflict is what gives sonata form its shape."),
    ("Mozart later revised the symphony to add clarinets. What does this tell you about the "
     "orchestra of the late Classical period?",
     ["Clarinets had only just been invented",
      "The clarinet was still being absorbed into the standard orchestra",
      "Mozart disliked oboes", "Clarinets replaced the string section"], 1,
     "The clarinet was the newest of the standard woodwind and was still becoming a fixture in the "
     "1780s. Mozart rewrote some oboe material to accommodate it, which is why two versions of the "
     "symphony exist.")]),
3: ("mozart-k622-mvt3", [
    ("The movement is a rondo. Why does that structure suit a concerto finale?",
     ["It allows the soloist to stop playing halfway through",
      "The returning theme gives the movement a memorable, lively character and frames contrasting "
      "episodes that display the soloist",
      "It is the shortest possible structure",
      "It avoids the need for an orchestra"], 1,
     "A recurring refrain makes a finale feel buoyant and easy to follow, while the episodes between "
     "returns give the soloist room to show range and agility. That is why rondo finales are so "
     "common in Classical concertos."),
    ("The clarinet's wide range is central to this movement. Which feature of the writing shows it "
     "most clearly?",
     ["The clarinet plays only in its highest register",
      "The line moves between low, warm notes and bright, high ones, often within a single phrase",
      "The clarinet doubles the violins throughout",
      "The clarinet plays only when the orchestra rests"], 1,
     "Mozart exploits the clarinet's contrasting registers — the dark chalumeau at the bottom and "
     "the brighter clarino above — often in the same phrase. Writing that shows off an instrument's "
     "range is characteristic of a concerto.")]),
4: ("haydn-sym94-mvt2", [
    ("Why does the famous fortissimo chord work as a surprise, in structural terms?",
     ["It is the loudest chord in the whole symphony",
      "It arrives at the end of a quiet, repeated phrase where the listener expects nothing new",
      "It is played in a different key from the rest",
      "It is played by an instrument heard nowhere else"], 1,
     "The theme's opening phrase is played quietly and then repeated even more quietly. The chord "
     "lands at the end of that repeat, exactly where the ear has settled into predictable calm — "
     "the joke depends on the structure, not just the volume."),
    ("Across the variations, which techniques does Haydn use to vary the theme?",
     ["He changes the time signature in every variation",
      "He alters the instrumentation, dynamics, ornamentation and harmony while keeping the theme's "
      "phrase structure recognisable",
      "He replaces the theme with a completely new melody each time",
      "He transposes the theme up a semitone each time"], 1,
     "Theme and variations keeps the underlying shape audible while changing its clothing. Recognising "
     "that the phrase structure survives is what lets you identify the form by ear."),
    ("This movement is in theme and variations form. How does that differ from rondo form?",
     ["Variations have no repeats; rondos do",
      "In variations one idea keeps returning transformed; in a rondo one idea returns unchanged "
      "between contrasting episodes",
      "Variations are always slow and rondos always fast",
      "Rondos have no main theme"], 1,
     "Both rely on return, but differently: variations reshape the same material each time, while a "
     "rondo brings its refrain back largely intact and puts the contrast in the episodes.")]),
5: ("handel-zadok", [
    ("Zadok the Priest has been sung at every British coronation since 1727. Which musical features "
     "make it suited to a ceremonial occasion?",
     ["A solo voice with quiet accompaniment throughout",
      "A long orchestral build to a sudden full-choir entry, with sustained homophonic writing and "
      "bright trumpets and timpani",
      "Constant changes of key and metre",
      "A small chamber ensemble with harpsichord only"], 1,
     "The gradual crescendo delays gratification, then the choir enters in a solid block of sound. "
     "Homophonic writing keeps the words clear, and trumpets and drums supply ceremonial brilliance."),
    ("The orchestral prelude builds tension without changing the harmony much. What technique "
     "achieves this?",
     ["Rapid modulation through distant keys",
      "Rippling arpeggiated string figuration over sustained harmony, growing steadily louder",
      "A solo trumpet fanfare",
      "Silence broken by sudden accents"], 1,
     "The strings keep the same harmonies turning over in broken chords while the dynamic swells. "
     "Nothing dramatic happens harmonically — the tension comes from texture and dynamics alone.")]),
6: ("chopin-nocturne-op9-no2", [
    ("The Nocturne's texture is melody with accompaniment. How does Chopin keep the accompaniment "
     "from sounding mechanical?",
     ["The left hand plays the same chord throughout",
      "The left hand plays flowing broken chords with a wide span, sustained by the pedal, under a "
      "freely ornamented melody",
      "The left hand doubles the melody an octave lower",
      "The accompaniment stops whenever the melody moves"], 1,
     "The arpeggiated left hand covers a wide range and is blurred by the pedal into continuous "
     "harmony, while the right hand decorates the tune differently on each return. Together they "
     "avoid any sense of a rigid pattern."),
    ("Chopin marks the piece with rubato. What does a performer do?",
     ["Play strictly in time with a metronome",
      "Stretch and relax the tempo expressively, so the melody moves flexibly against the pulse",
      "Play everything twice as slowly",
      "Repeat each phrase immediately"], 1,
     "Rubato means 'robbed' time — the melody borrows and repays time against a steadier "
     "accompaniment. It is central to Romantic piano style and is why two performances of this "
     "Nocturne can sound quite different.")]),
7: ("schumann-traumerei", [
    ("Kinderszenen means 'Scenes from Childhood'. What does the very short length of these pieces "
     "tell you about Romantic piano music?",
     ["Romantic composers could not sustain long works",
      "The Romantic character piece aimed to capture a single mood or image concisely, often for "
      "domestic performance",
      "They were written for beginners only",
      "They were unfinished sketches"], 1,
     "The character piece is a Romantic genre in its own right: a short, self-contained work "
     "evoking one mood, and ideal for playing at home on the piano that was becoming common in "
     "middle-class houses."),
    ("Träumerei is in ternary form. What must a listener hear for that label to be correct?",
     ["Two sections, each repeated",
      "An opening idea, a contrasting middle, then a return of the opening",
      "A main theme returning between several different episodes",
      "One idea repeated with changes each time"], 1,
     "Ternary is ABA. The return of A after a contrasting B is the deciding evidence — without that "
     "return you have binary, and with several different episodes you have rondo.")]),
8: ("verdi-dies-irae", [
    ("Verdi's Requiem is often called operatic. Which features justify that description?",
     ["It uses only unaccompanied voices",
      "Large orchestral forces, extremes of dynamics, vivid word-painting and dramatic vocal "
      "writing more usually found on the stage",
      "It is written in binary form",
      "It avoids the chorus entirely"], 1,
     "Verdi wrote for the theatre, and the Requiem carries that instinct into sacred music: huge "
     "contrasts, dramatic orchestration and text setting that paints the words. Some contemporaries "
     "thought it too theatrical for church."),
    ("Compare the choral entry in the Dies Irae with the one in Handel's Zadok the Priest. What is "
     "the main difference in approach?",
     ["Both build gradually to the entry",
      "Handel builds a long crescendo before the choir enters; Verdi strikes suddenly with the "
      "chorus and full orchestra almost immediately",
      "Verdi uses a solo voice and Handel a chorus",
      "Neither uses an orchestra"], 1,
     "Handel delays and prepares; Verdi shocks. Both produce a powerful entry, but one works by "
     "anticipation and the other by immediate impact — a useful contrast to have ready for a "
     "comparison question.")]),
}


def main():
    dry = "--dry-run" in sys.argv
    sb = get_client()
    sub = [x for x in sb.table("subjects").select("id,slug,school_id")
           .eq("slug", "music-aqa").execute().data if not x["school_id"]][0]
    unit = [u for u in sb.table("units").select("id,slug").eq("subject_id", sub["id"])
            .execute().data if u["slug"] == UNIT][0]["id"]

    if "--restore" in sys.argv:
        with open(BACKUP, "r", encoding="utf-8") as f:
            for lid, pd in json.load(f).items():
                sb.table("lessons").update({"practice_data": pd}).eq("id", lid).execute()
        print("restored")
        return

    saved = {}
    for num, (pid, items) in sorted(GOLD.items()):
        row = sb.table("lessons").select("id,practice_data").eq("unit_id", unit) \
            .eq("lesson_number", num).single().execute().data
        pd = json.loads(json.dumps(row["practice_data"]))
        ids = {p.get("id") for p in pd.get("passages") or []}
        assert pid in ids, (num, pid, ids)
        gold = pd["problem_bank"]["gold"]
        before = len(gold)
        for text, opts, correct, expl in items:
            if any(g.get("question") == text for g in gold):
                continue
            assert 0 <= correct < len(opts)
            assert len(set(opts)) == len(opts)
            gold.append(q(pid, text, opts, correct, expl))
        assert len(gold) >= 4, (num, len(gold))
        saved[row["id"]] = row["practice_data"]
        if not dry:
            sb.table("lessons").update({"practice_data": pd}).eq("id", row["id"]).execute()
        print("  L%-2d gold %d -> %d" % (num, before, len(gold)))

    if not dry and saved and not os.path.exists(BACKUP):
        with open(BACKUP, "w", encoding="utf-8") as f:
            json.dump(saved, f)
        print("backup ->", BACKUP)
    print(("DRY RUN — " if dry else "") + "lessons updated: %d" % len(GOLD))


if __name__ == "__main__":
    main()
