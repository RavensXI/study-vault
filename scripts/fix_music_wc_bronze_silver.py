# -*- coding: utf-8 -*-
"""Bring bronze and silver to 4 on the eight AoS1 listening-practice lessons.

Same reasoning as the gold pass: 75% of 3 is 3/3, so a single slip failed the
tier. Analysis and context questions only — nothing that asks the student to
identify something new by ear, because the audio cannot be verified from here.

    python scripts/fix_music_wc_bronze_silver.py [--dry-run|--restore]
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

BACKUP = os.path.join(HERE, "_music_wc_bs_backup.json")
UNIT = "western-classical-1650-1910"

# lesson -> {tier: [(question, options, correct_index, explanation)]}
ADD = {
1: {"bronze": [("In which musical period was Beethoven's Symphony No.1 written?",
    ["Baroque", "Classical, at the point where it begins to look towards Romanticism",
     "Early Romantic, after Beethoven's deafness", "Twentieth century"], 1,
    "It dates from 1800. The scoring and structure are Classical, but the harmonic risk-taking "
    "already points towards the Romantic era Beethoven helped open.")],
    "silver": [("What is the function of a slow introduction before a fast sonata-form Allegro?",
    ["To let the players tune up",
     "To build expectation and delay the arrival of the home key and main tempo",
     "To state the second subject in advance", "To repeat the previous movement"], 1,
    "A slow introduction creates anticipation. Beethoven goes further by withholding a clear C major "
    "as well, so both the tempo and the key arrive together when the Allegro begins.")]},
2: {"bronze": [("Symphony No. 40 is in G minor. What is its relative major?",
    ["G major", "B flat major", "E flat major", "D minor"], 1,
    "A minor key shares its key signature with the major a minor third above: G minor and B flat "
    "major both have two flats. That is the key the second subject appears in."),
    ("Which period does Mozart's Symphony No. 40 belong to?",
     ["Baroque", "Classical", "Romantic", "Modern"], 1,
     "Written in 1788, it is a central Classical symphony: balanced phrasing, clear "
     "melody-and-accompaniment textures and a standard Classical orchestra.")],
    "silver": [("What does 'Molto allegro' tell the performers?",
     ["Very slow", "Very fast", "Moderately loud", "Gradually quicker"], 1,
     "Allegro is fast and molto means very, so molto allegro is very fast. It is a tempo marking, "
     "not a dynamic — dynamics are the letters p and f."),
    ("Why does a minor-key sonata-form exposition usually move to the relative major?",
     ["Because minor keys cannot be sustained",
      "Because it shares the key signature, so the shift sounds like a natural brightening rather "
      "than a jolt",
      "Because the relative major is always louder", "To avoid using accidentals"], 1,
     "The relative major is the closest related key, sharing every note of the scale. Moving there "
     "gives contrast without dislocation, and the return to the tonic in the recapitulation then "
     "feels like a resolution.")]},
3: {"bronze": [("What is the solo instrument in Mozart's K.622?",
    ["Flute", "Clarinet", "Oboe", "Bassoon"], 1,
    "It is the Clarinet Concerto in A major, written in 1791 for the clarinettist Anton Stadler.")],
    "silver": [("In a concerto, what is the relationship between soloist and orchestra?",
    ["The orchestra plays only when the soloist rests",
     "The soloist is contrasted with and accompanied by the orchestra, often alternating and "
     "combining with it",
     "They always play the same music together", "The soloist conducts the orchestra"], 1,
    "Concerto form is built on that contrast — a single voice set against the mass of the orchestra, "
    "sometimes answered by it, sometimes supported by it.")]},
4: {"bronze": [("Haydn's Symphony No. 94 has a nickname. What is it?",
    ["The Clock", "The Surprise", "The Military", "The Drumroll"], 1,
    "The nickname comes from the sudden fortissimo chord in the second movement. Haydn wrote "
    "several nicknamed symphonies, so the label is worth knowing precisely.")],
    "silver": [("Why is Haydn often called the 'father of the symphony'?",
    ["He wrote the first piece of orchestral music ever",
     "He wrote over a hundred symphonies and did much to establish the four-movement Classical form",
     "He invented the orchestra", "He was the first composer to use a minor key"], 1,
    "Haydn did not invent the symphony, but his output and consistency shaped what the Classical "
    "symphony became — including the standard four-movement plan.")]},
5: {"bronze": [("Which type of ensemble performs Zadok the Priest?",
    ["Solo organ", "Orchestra and choir", "String quartet", "Unaccompanied voices"], 1,
    "Handel scores it for choir with orchestra, including trumpets and timpani for ceremonial "
    "brilliance.")],
    "silver": [("Handel wrote Zadok the Priest in 1727. Which period is that?",
    ["Renaissance", "Baroque", "Classical", "Romantic"], 1,
    "1727 is late Baroque. The continuo, the terraced dynamics of the era and the ceremonial "
    "trumpet writing are all Baroque traits, even though the long crescendo here is unusual.")]},
6: {"bronze": [("What is a nocturne?",
    ["A dance in triple time", "A short lyrical piano piece evoking night",
     "A movement for full orchestra", "A song with words"], 1,
    "The nocturne is a Romantic character piece for piano, associated with night and reverie. "
    "Chopin wrote twenty-one of them.")],
    "silver": [("Which period does Chopin's Op. 9 No. 2 belong to, and how can you tell?",
    ["Baroque — it uses a continuo",
     "Romantic — expressive rubato, rich pedalled harmony and a highly ornamented singing melody",
     "Classical — it uses sonata form", "Modern — it avoids a key centre"], 1,
    "Everything about it is Romantic: the expressive freedom, the sustaining pedal blurring the "
    "harmony, and a melody decorated as a singer might decorate a repeated verse.")]},
7: {"bronze": [("What does the title Kinderszenen mean?",
    ["Night pieces", "Scenes from childhood", "Studies", "Dances"], 1,
    "Kinderszenen is German for 'Scenes from Childhood'. Schumann wrote them as an adult looking "
    "back, not as music for children to play.")],
    "silver": [("What is a character piece?",
    ["A piece written for a stage character",
     "A short instrumental work capturing a single mood or idea",
     "A piece with a repeating refrain", "A work in four movements"], 1,
    "The character piece is a Romantic genre: brief, self-contained, and aiming at one atmosphere "
    "rather than a large argument. Träumerei is a model example.")]},
8: {"bronze": [("What is a Requiem?",
    ["A dance suite", "A Mass for the dead", "A solo song cycle", "A type of overture"], 1,
    "A Requiem is the Roman Catholic Mass for the dead. The Dies Irae — 'day of wrath' — is its most "
    "dramatic section, describing the Day of Judgement.")],
    "silver": [("Which period does Verdi's Requiem belong to?",
    ["Baroque", "Classical", "Romantic", "Twentieth century"], 2,
    "It dates from 1874. The huge forces, extremes of dynamics and vividly dramatic text setting are "
    "all Romantic traits, and Verdi's operatic background shows throughout.")]},
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
    for num, tiers in sorted(ADD.items()):
        row = sb.table("lessons").select("id,practice_data").eq("unit_id", unit) \
            .eq("lesson_number", num).single().execute().data
        pd = json.loads(json.dumps(row["practice_data"]))
        # anchor on the lesson's own first passage so the audio stays available
        pid = (pd.get("passages") or [{}])[0].get("id")
        assert pid, num
        before = {t: len(pd["problem_bank"][t]) for t in ("bronze", "silver", "gold")}
        for tier, items in tiers.items():
            for text, opts, correct, expl in items:
                if any(g.get("question") == text for g in pd["problem_bank"][tier]):
                    continue
                assert 0 <= correct < len(opts) and len(set(opts)) == len(opts)
                pd["problem_bank"][tier].append({
                    "input_type": "multiple_choice", "passage_id": pid, "question": text,
                    "options": opts, "solutions": [correct], "explanation": expl})
        after = {t: len(pd["problem_bank"][t]) for t in ("bronze", "silver", "gold")}
        assert all(after[t] >= 4 for t in after), (num, after)
        saved[row["id"]] = row["practice_data"]
        if not dry:
            sb.table("lessons").update({"practice_data": pd}).eq("id", row["id"]).execute()
        print("  L%-2d b %d->%d  s %d->%d  g=%d" % (num, before["bronze"], after["bronze"],
                                                    before["silver"], after["silver"], after["gold"]))
    if not dry and saved and not os.path.exists(BACKUP):
        with open(BACKUP, "w", encoding="utf-8") as f:
            json.dump(saved, f)
        print("backup ->", BACKUP)
    print(("DRY RUN — " if dry else "") + "lessons updated: %d" % len(ADD))


if __name__ == "__main__":
    main()
