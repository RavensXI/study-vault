# -*- coding: utf-8 -*-
"""Add the Eduqas AoS1 form-discrimination questions to the eight
forms-devices-listening drills (the Phase-3 TODO).

The copied AQA banks already name the obvious forms (rondo L3, variations
L4, ternary L7) — what the Eduqas spec needs on top is the vocabulary AQA
never drilled (minuet and trio, strophic, through-composed) and the
"prove the label" discrimination asks. 12 questions, slotted per tier.

Run: python eduqas_forms_questions.py [--apply]
Backup: _backup_forms_questions_2026-08-16.json
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

APPLY = "--apply" in sys.argv
BACKUP = os.path.join(HERE, "_backup_forms_questions_2026-08-16.json")


def q(passage_id, question, options, correct, explanation, miscons):
    return {"question": question, "options": options, "solutions": [correct],
            "input_type": "multiple_choice", "passage_id": passage_id,
            "explanation": explanation,
            "misconceptions": [{"id": mid, "expect": exp, "message": msg}
                               for mid, exp, msg in miscons]}


ADDITIONS = {
    1: [  # Beethoven Symphony No.1, mvt 1
        ("bronze", q("beethoven-sym1-mvt1",
            "The movement moves from a slow, searching introduction into a fast, confident Allegro. Which structural device is Beethoven using at this moment?",
            ["Contrast — placing two very different characters side by side",
             "Imitation — one part copying another",
             "Ostinato — a short pattern repeated over and over",
             "Drone — a long held note underneath the music"],
            0,
            "Contrast is one of the most basic structural devices: the hesitant, slow introduction makes the arrival of the quick Allegro feel like a burst of energy. Composers place contrasting sections side by side so each one sharpens the effect of the other.",
            [("confuse-contrast-imitation", 1,
              "You chose imitation, but imitation means one part copying another part's melody shortly after it. Here nothing is being copied — two whole sections with different speeds and moods are being set against each other, which is contrast."),
             ("confuse-contrast-ostinato", 2,
              "You chose ostinato, but an ostinato is a short musical pattern repeated many times. The slow-then-fast opening is about two contrasting characters, not a repeating pattern.")])),
        ("gold", q("beethoven-sym1-mvt1",
            "A Classical symphony's third movement is traditionally a minuet and trio. What shape does a minuet and trio make?",
            ["A large ternary shape: minuet, contrasting trio, then the minuet played once more",
             "A set of variations on the minuet melody",
             "A rondo in which the minuet keeps returning between many different episodes",
             "Two repeated halves with no return of the opening"],
            0,
            "A minuet and trio is a dance-based movement in a large A-B-A (ternary) shape: the minuet is played, a contrasting central section called the trio follows, and then the minuet returns. It is one of the named forms you can be asked to recognise, and this symphony's own third movement is one.",
            [("minuet-trio-not-rondo", 2,
              "You chose rondo, but a rondo's theme returns several times between different episodes. In a minuet and trio there is only ONE contrasting section — the trio — so the overall shape is ternary, A-B-A, not A-B-A-C-A."),
             ("minuet-trio-not-binary", 3,
              "You chose two repeated halves with no return, which describes binary form. The defining feature of a minuet and trio is that the opening minuet DOES return after the trio, making the large shape ternary.")])),
    ],
    2: [  # Mozart Symphony No. 40, mvt 1
        ("bronze", q("mozart-40-mvt1",
            "The famous opening melody is built from a short three-note sighing figure heard over and over, then carried to different pitches. Which pair of devices is Mozart using?",
            ["Repetition and sequence",
             "Drone and syncopation",
             "Imitation and pedal",
             "Ostinato and glissando"],
            0,
            "The urgent opening grows from one tiny three-note cell: Mozart repeats it insistently, then moves it to new pitch levels — that pitch-shifted repetition is called a sequence. Building long melodies from a repeated and sequenced motif is a core device to name in a listening answer.",
            [("sequence-not-ostinato", 3,
              "You chose ostinato, but an ostinato stays fixed while other music changes around it. Mozart's sighing figure MOVES — it is restated at different pitch levels, and repetition at changing pitch levels is a sequence.")])),
        ("silver", q("mozart-40-mvt1",
            "The agitated opening melody returns near the end of the movement, back in the home key. Which structural principle does this departure and return show?",
            ["The ternary principle: opening material departs and later returns to round the music off",
             "Strophic form: the same music repeats for each new verse",
             "Theme and variations: the melody is decorated differently at each appearance",
             "Binary form: two halves, with the opening never coming back"],
            0,
            "Statement, departure and return is the ternary principle, and it governs this movement: the opening material sets out, the music travels through new keys and development, and the theme comes home at the end. (The full Classical structure is called sonata form — beyond what you need — but hearing departure-and-return is exactly the skill the exam rewards.)",
            [("return-not-strophic", 1,
              "You chose strophic, but strophic form means the SAME music repeated straight through for each verse of a text, as in a hymn. Here the return frames a long contrasting journey in between — that framing shape is the ternary principle."),
             ("return-not-binary", 3,
              "You chose binary, but binary form's defining feature is that the opening material does NOT return at the end. You can hear the opening theme come back in the home key, which rules binary out.")])),
    ],
    3: [  # Mozart Clarinet Concerto, mvt 3
        ("gold", q("mozart-k622-mvt3",
            "A friend hears this movement and says it is ternary. You say rondo. Which single piece of listening evidence settles it in your favour?",
            ["The main theme returns more than twice, with a DIFFERENT contrasting episode before each return",
             "The movement is fast and in a major key",
             "There is a solo instrument accompanied by an orchestra",
             "The opening theme is repeated immediately after it is first played"],
            0,
            "Ternary is A-B-A: one contrasting section, one return. A rondo is A-B-A-C-A (or longer): the refrain keeps returning and each episode between returns is NEW. Counting the returns of the theme — and noticing the episodes differ from each other — is the evidence that proves rondo over ternary.",
            [("rondo-evidence-not-tempo", 1,
              "You chose the speed and key, but tempo and tonality do not identify a form — ternary movements can be fast and major too. Form labels rest on the ORDER and RETURN of sections: several returns with different episodes between them means rondo."),
             ("rondo-evidence-not-scoring", 2,
              "You chose the solo-plus-orchestra layout, but that describes the GENRE (a concerto), not the form. A concerto movement could be ternary, variations or rondo — only the pattern of returning sections tells you which.")])),
    ],
    4: [  # Haydn Symphony No.94, mvt 2
        ("gold", q("haydn-sym94-mvt2",
            "Variations form and rondo form both bring the main idea back several times. What is the crucial difference you listen for?",
            ["In variations the theme itself is transformed at each return; in a rondo the refrain returns largely unchanged with contrasting episodes between",
             "Variations are always quiet, while rondos are always loud",
             "A rondo transforms its theme at each return; variations keep it identical",
             "Variations use the full orchestra, while rondos use soloists"],
            0,
            "Both forms rely on return, so the test is WHAT returns. In this movement the theme is never left behind — each section IS the theme, re-dressed with new decoration, accompaniment or mode. In a rondo you instead hear the same refrain come back essentially intact, separated by episodes made of new material.",
            [("variations-rondo-swapped", 2,
              "You have the two forms swapped round: it is the VARIATIONS that transform the theme at every appearance, while a rondo's refrain returns essentially as it was. Listen for whether the returning music is re-dressed (variations) or intact (rondo)."),
             ("form-not-dynamics", 1,
              "You chose a dynamics rule, but no form has a fixed volume — this very movement contains both a whispered theme and the famous fortissimo crash. Forms are identified by the pattern of repetition and contrast, never by loudness.")])),
    ],
    5: [  # Handel, Zadok the Priest
        ("silver", q("handel-zadok",
            "The anthem sets three different portions of text, each with its own music, sung continuously. Why is this NOT strophic form?",
            ["Strophic form repeats the SAME music for each verse of text — here every section has new music",
             "Strophic form is only used in pop songs, never in choral music",
             "Strophic form requires a solo singer rather than a choir",
             "Strophic form must be in a minor key"],
            0,
            "Strophic means verse form: one block of music repeated for verse after verse, as in a hymn or folk song. Handel instead writes fresh music for each section of the coronation text, so the anthem is through-composed in three linked sections. Being able to reject a label for the right reason earns marks as surely as choosing one.",
            [("strophic-not-genre-bound", 1,
              "You tied strophic form to pop music, but hymns, folk songs and plenty of choral pieces are strophic too. The label is about REPEATED MUSIC FOR EACH VERSE, in any style — and it fails here because each text section gets new music."),
             ("strophic-not-forces", 2,
              "You linked strophic form to a solo singer, but form labels do not depend on who performs. A choir can sing a strophic hymn; what disqualifies Zadok is that its three sections each have different music rather than one repeated verse.")])),
    ],
    6: [  # Chopin, Nocturne Op.9 No.2
        ("bronze", q("chopin-nocturne-op9-no2",
            "After the final return of the melody, Chopin adds a closing passage with a new idea and a sparkling cadenza-like flourish before the quiet last bars. What is a closing section like this called?",
            ["A coda", "An episode", "A refrain", "An introduction"],
            0,
            "A coda (Italian for 'tail') is music added after the main structure is complete, to wind the piece down or provide a final flourish. Here it brings a new closing idea and a brilliant run before settling onto the final quiet chords.",
            [("coda-not-episode", 1,
              "You chose episode, but an episode is a contrasting section INSIDE a rondo, between returns of the refrain. Music added at the END, after the last return, is a coda — a tailpiece that closes the whole structure.")])),
        ("silver", q("chopin-nocturne-op9-no2",
            "Each time the main melody returns, Chopin decorates it more elaborately with runs, turns and extra notes. Which structural principle is this?",
            ["Ornamented (varied) repetition — the same melody returns, more decorated each time",
             "Through-composed form — new music continuously, with nothing returning",
             "Strophic form — identical music repeated exactly for each verse",
             "Imitation — a second voice copying the melody in another part"],
            0,
            "The Nocturne's structure works by RETURN plus DECORATION: the melody comes back recognisably, but never plainly — each reprise carries more ornamentation. Naming this as ornamented or varied repetition shows an examiner you hear both the return and the transformation.",
            [("varied-return-not-through-composed", 1,
              "You chose through-composed, but that means nothing returns at all. You can clearly recognise the same nocturne melody coming back — what changes is the decoration on top of it, which makes this varied repetition."),
             ("varied-return-not-strophic", 2,
              "You chose strophic, but strophic repetition is EXACT — the same music for each verse. Chopin never repeats the tune exactly: every return is more embellished, so the right label is ornamented (varied) repetition.")])),
    ],
    7: [  # Schumann, Kinderszenen
        ("silver", q("schumann-traumerei",
            "In Träumerei, the gentle rising opening figure is heard, then restated starting on higher notes as the phrase unfolds. Which device is this?",
            ["Sequence — the same figure repeated at a different pitch level",
             "Pedal — a sustained note held beneath changing harmony",
             "Ostinato — an unchanging pattern repeated throughout the piece",
             "Syncopation — accents placed off the main beat"],
            0,
            "When a melodic figure is immediately restated higher or lower, that is a sequence — one of the named devices you should spot and label. Schumann uses it to make Träumerei's dreamy opening reach upwards step by step, each restatement lifting the phrase further.",
            [("sequence-not-pedal", 1,
              "You chose pedal, but a pedal is a note SUSTAINED underneath while harmonies change above it. What you hear in Träumerei is the melodic figure itself being restated at new pitch levels — that restatement is a sequence."),
             ("sequence-not-ostinato", 2,
              "You chose ostinato, but an ostinato repeats at the SAME pitch, unchanged, usually as an accompaniment layer. Träumerei's figure climbs — repetition at changing pitch levels is a sequence, not an ostinato.")])),
    ],
    8: [  # Verdi, Dies irae
        ("bronze", q("verdi-dies-irae",
            "The Dies Irae does not fit binary, ternary or rondo form: the music surges continuously onward, shaped by the words rather than by repeating sections. What is music like this called?",
            ["Through-composed", "Strophic", "Theme and variations", "Minuet and trio"],
            0,
            "When music follows its text continuously without a repeating sectional plan, it is through-composed. Verdi lets the terrifying Day of Judgement text drive the structure, so the movement is organised by drama rather than by a returning refrain or repeated verse.",
            [("through-composed-not-strophic", 1,
              "You chose strophic, but strophic music repeats the same block of music for every verse. Verdi gives each new line of the text new music — continuous, text-driven writing like this is through-composed.")])),
        ("gold", q("verdi-dies-irae",
            "The terrifying Dies Irae music erupts back later in the Requiem — within the long Judgement sequence and once more in the final movement. What structural job do these returns do?",
            ["They act like a refrain: recurrence binds the huge work together and re-ignites its terror at key moments",
             "They are exact strophic verses, restating the same words each time",
             "They turn the whole Requiem into a rondo with regular episodes",
             "They are codas, formally closing each movement they appear in"],
            0,
            "Across a ninety-minute work, Verdi uses recurrence as architecture: bringing the Dies Irae music back stamps the fear of judgement over everything between its appearances. It behaves like a refrain — return as a unifying device — without the regular alternation that would make a true rondo.",
            [("refrain-not-rondo", 2,
              "You chose rondo, but a rondo alternates refrain and episode in a regular pattern within ONE movement. Verdi's returns are irregular and dramatic, striking across a huge multi-movement work — recurrence as a unifying refrain, not a rondo scheme."),
             ("refrain-not-coda", 3,
              "You chose coda, but a coda is closing music added after a structure is complete. These returns ERUPT MID-STRUCTURE to revive the terror of the opening — their job is unification and dramatic recall, not formal closure.")])),
    ],
}


def main():
    sb = get_client()
    sub = sb.table("subjects").select("id").eq("slug", "music-eduqas").execute().data[0]["id"]
    unit = [u for u in sb.table("units").select("id,slug,subject_id").execute().data
            if u["subject_id"] == sub and u["slug"] == "forms-devices-listening"][0]
    backup, writes, added = {}, [], 0
    for num, items in sorted(ADDITIONS.items()):
        row = sb.table("lessons").select("id,title,practice_data") \
            .eq("unit_id", unit["id"]).eq("lesson_number", num).execute().data[0]
        pd = row["practice_data"]
        existing = {p["question"] for t in pd["problem_bank"].values() for p in t}
        pids = {p["id"] for p in pd["passages"]}
        n = 0
        for tier, prob in items:
            assert prob["passage_id"] in pids, \
                "L%d: unknown passage %s" % (num, prob["passage_id"])
            if prob["question"] in existing:
                print("L%d [%s]: already present, skipped" % (num, tier))
                continue
            pd["problem_bank"][tier].append(prob)
            n += 1
        if n:
            backup[row["id"]] = None  # full pd too big; backup file holds it
            writes.append((row["id"], pd, num, n))
            added += n
        sizes = {t: len(v) for t, v in pd["problem_bank"].items()}
        print("L%d: +%d -> %s" % (num, n, sizes))
    print("\nquestions to add: %d across %d lessons" % (added, len(writes)))
    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    if not os.path.exists(BACKUP):
        # back up the pre-change practice_data of every touched lesson
        pre = {}
        for lid, _, num, _ in writes:
            cur = sb.table("lessons").select("practice_data").eq("id", lid) \
                .execute().data[0]["practice_data"]
            pre[lid] = cur
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(pre))
    for lid, pd, num, n in writes:
        sb.table("lessons").update({"practice_data": pd}).eq("id", lid).execute()
    print("applied. backup:", BACKUP)


if __name__ == "__main__":
    main()
