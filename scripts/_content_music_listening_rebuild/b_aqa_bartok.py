# -*- coding: utf-8 -*-
"""music-aqa / aos4-since-1910 / L2 -- Bartok, Hungarian Sketches: four movements.
Guided-listening deck, one card per landmark across all four required movements.

LIVE lesson, QA'd by ear: every pin time carried over unchanged.
Probe corroboration (3 votes per movement, timings.json). All four durations are
correct against YouTube's own metadata. The probes hear each section change a
consistent 2-5 s EARLIER than the pins:
    Evening in the Village   B 43.7 vs 46, A1 66 vs 68, length 175 OK
    Bear Dance               B 16 vs 14, A1 33 vs 28, length 89 OK
    Slightly Tipsy           B 39 vs 34, A1 97 vs 92, length 131 OK
    Swineherd's Dance        A1 68 vs 63, length 122 OK
That is a systematic offset, not a contradiction, and consistent with pins set a
beat or two inside each new section. Left alone. One item is flagged for Tom:
all three votes put the first note of Evening in the Village at 0:08, so pin 1
at 0 may sit on a title card rather than on music.

DROPPED: two in-card YouTube embeds, of the complete suite and of Slightly
Tipsy. Both duplicate the four-track dock above them (the second uses the same
video id as track 3), and the deck format carries no in-card embeds.
"""
import io, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck_raw import RawDeck, dfn, patch, build_questions_keep, check_plain, renumber_tail

BACKUP = "music-aqa__aos4-since-1910__L02"
HERE = os.path.dirname(os.path.abspath(__file__))
old = json.load(io.open(os.path.join(HERE, "backups", BACKUP + ".json"), encoding="utf-8"))

d = RawDeck(lesson_id=old["id"], subject="music-aqa", unit="aos4-since-1910", lesson_no=2,
            original_html=old["content_html"])
TITLE = "Bartók: Hungarian Sketches — Guided Listening"

d.pins = [
    ("t1", "t1c1", 0,     "A &mdash; Lento rubato", "A descending legato melody on solo woodwind. Aeolian mode on F sharp, minor pentatonic."),
    ("t1", "t1c2", 43.7,  "B &mdash; Allegretto",   "Staccato, conjunct quavers over short pizzicato &mdash; a busier evening."),
    ("t1", "t1c3", 66,    "A1",                     "The slow music returns, varied."),
    ("t1", "t1c4", 98,    "B1",                     "The quick music returns &mdash; listen for the trills added here."),
    ("t1", "t1c5", 121.1, "A2",                     "The final slow section closes the arch: A B A1 B1 A2."),
    ("t2", "t2c1", 0,     "A &mdash; pedal on D",   "The pedal note sits in cellos, double basses, horns and tuba."),
    ("t2", "t2c2", 16,    "B &mdash; pedal on A flat", "The pedal moves to the second violins. D to A flat is a tritone: the harshest interval."),
    ("t2", "t2c3", 33,    "A1",                     "Back to the D pedal &mdash; and a triangle joins here."),
    ("t2", "t2c4", 52,    "B1",                     "The A flat pedal again; the side drums now play with their snares on."),
    ("t2", "t2c5", 71.7,  "A2",                     "The final D section &mdash; the movement ends on a D major chord."),
    ("t3", "t3c1", 0,     "A section",              "Quaver melody with acciaccaturas on almost every note. Violins col legno, muted at the tip of the bow."),
    ("t3", "t3c2", 39,    "B section",              "Two motifs &mdash; an off-beat accompaniment pattern alternating with a smooth legato melody."),
    ("t3", "t3c3", 97,    "A1 &mdash; developed",   "The A material returns, but significantly developed rather than simply repeated."),
    ("t4", "t4c1", 0,     "Introduction",           "A drone, with fragments of the folk tune before it properly arrives."),
    ("t4", "t4c2", 12,    "A",                      "The first half of the collected folk melody &mdash; bars 1 to 16."),
    ("t4", "t4c3", 32,    "B",                      "The second half, bars 17 to 33. The drone shifts to D before returning to A."),
    ("t4", "t4c4", 68,    "A1",                     "After a four-bar link, the first half of the melody returns."),
    ("t4", "t4c5", 86,    "B2",                     "The second half fragmented and developed &mdash; its last two bars held back for the coda."),
]

d.add_cover(
  "Four pictures of Hungarian village life",
  [
    "<em>Hungarian Sketches</em>, <em>Magyar K&eacute;pek</em>, is an orchestral suite Bart&oacute;k assembled in "
    "1931 from five short piano pieces written about twenty years earlier. Each movement is a small picture of "
    "rural life: a village at dusk, a dance, a drunk stumbling home.",
    "Your exam asks for four of the five: Evening in the Village, Bear Dance, Slightly Tipsy and Swineherd&rsquo;s "
    "Dance. Movement 3, Melody, is not on the specification. From 1906 Bart&oacute;k travelled Hungarian and "
    "Romanian villages with a phonograph, recording peasant song with Zolt&aacute;n Kod&aacute;ly; the %s, short "
    "repeated phrases and dance rhythms he found there are what you hear in all four."
    % dfn("modal scales", "Scales built from a pattern of tones and semitones other than major or minor, often drawn from folk melody"),
    "Press play and the cards follow the music. Use the track buttons to switch movements, and tap any number to jump.",
  ])

# ---- Evening in the Village -------------------------------------------------
d.add_statement(1, "Evening 1 · A", "1 &middot; A sigh at the end of the day",
  "The movement is in %s &mdash; A B A1 B1 A2 &mdash; a symmetry Bart&oacute;k was known for. %s The A sections are "
  "marked Lento rubato, slow and speech-like, and the melody is a mainly descending %s phrase on solo woodwind, "
  "built from the F sharp minor pentatonic scale and the %s on F sharp."
  % (dfn("arch form", "A symmetrical shape that goes out and comes back: A B A1 B1 A2"), d.ref(1),
     dfn("legato", "Smoothly, notes joined together"),
     dfn("Aeolian mode", "The natural minor scale, here starting on F sharp")),
  "one woodwind line over very little else. The scoring here is only woodwind, two horns and strings.")

d.add_statement(2, "Evening 2 · B", "2 &middot; Not everyone's evening is calm",
  "The B section is marked Allegretto, nearly twice the speed. %s Its melody is the opposite of the A melody in "
  "every respect: %s and %s quavers, moving by step, over short pizzicato rather than long held notes. Both "
  "melodies still come from the same F sharp minor pentatonic scale."
  % (d.ref(2), dfn("staccato", "Detached, each note cut short"),
     dfn("conjunct", "Moving by step, without leaps")),
  "the change of articulation. Same scale, opposite character, is the point of the contrast.")

d.add_statement(3, "Evening 3 · A1", "3 &middot; The slow music, varied",
  "The Lento rubato music returns, but varied rather than copied. %s Throughout the movement the texture is melody "
  "and accompaniment, with different woodwind instruments taking the solo line in turn over chordal accompaniment "
  "&mdash; either long held notes or pizzicato crotchets. Dynamics run from ppp to forte."
  % d.ref(3),
  "which woodwind has the tune this time. Bart&oacute;k rotates the solo colour rather than repeating it.")

d.add_statement(4, "Evening 4 · B1", "4 &middot; The quick music, decorated",
  "The Allegretto material comes back, and the giveaway detail is the decoration. %s Trills are added that were not "
  "there the first time. Underneath, Bart&oacute;k avoids traditional cadences and uses non-functional chords, so "
  "however folk-like the tune sounds, the key stays deliberately unclear."
  % d.ref(4),
  "trills on the returning dance tune. Naming what is added on a return earns more than spotting the return.")

d.add_statement(5, "Evening 5 · A2", "5 &middot; Closing the arch",
  "The final slow section completes the shape: A B A1 B1 A2. %s The movement is mostly 4/4, but bars of 3/4 and 2/4 "
  "near the end unsettle the ending, so the arch closes without quite squaring up. That refusal to resolve neatly "
  "is deliberate, and it matches the harmony."
  % d.ref(5),
  "the metre going out of step near the close. Say &lsquo;bars of 3/4 and 2/4&rsquo;, not &lsquo;the rhythm changes&rsquo;.")

# ---- Bear Dance -------------------------------------------------------------
d.add_statement(6, "Bear Dance 1 · A", "6 &middot; Follow the pedal note",
  "Bart&oacute;k described this as the impression of a bear dancing to its leader&rsquo;s song, growling to a drum. "
  "%s It is in %s, and the easiest way to hear the sections is to follow the %s: A sits on a D, held in cellos, "
  "double basses, horns and tuba, and the melody above uses the Aeolian mode on D sharp."
  % (d.ref(6), dfn("varied strophic form", "The same music repeated with variations, verse by verse"),
     dfn("pedal note", "A note held or repeated underneath while the music changes above it")),
  "one low note that will not move. Everything else is measured against it.")

d.add_statement(7, "Bear Dance 2 · B", "7 &middot; A tritone away",
  "The pedal moves to A flat, now in the second violins, and the melody uses the Lydian dominant scale on D. %s D to "
  "A flat is a %s, the most dissonant interval there is, so the shift is deliberately harsh. Phrases stay mostly "
  "four bars long, and the dissonance is what gives the dance its excitement."
  % (d.ref(7), dfn("tritone", "The most dissonant interval: three whole tones apart")),
  "the pedal jumping to a new note in a higher instrument. Name the interval, not just the change.")

d.add_statement(8, "Bear Dance 3 · A1", "8 &middot; Back to D, plus a triangle",
  "The D pedal returns and with it a new colour: a triangle joins here. %s Bart&oacute;k adds two trumpets, two "
  "trombones, tuba, timpani and two side drums to the forces of the first movement, and he is exact about how they "
  "play &mdash; the brass sometimes muted, the strings both bowed and plucked."
  % d.ref(8),
  "the triangle. On a return, an added instrument is the clearest thing you can name.")

d.add_statement(9, "Bear Dance 4 · B1", "9 &middot; Snares on",
  "The A flat pedal comes back, and the side drums, which began without snares, now switch them on. %s The texture "
  "revolves around the pedal notes, which work as a rhythmic drone: repeated quavers in the pedal and the snare "
  "build anticipation while the melody moves mainly in crotchets, harmonised in thirds, sixths and octaves."
  % d.ref(9),
  "the drum changing from a dull thud to a rattle. That is the snares being engaged, and it is examinable.")

d.add_statement(10, "Bear Dance 5 · A2", "10 &middot; The bear stops",
  "The final D section closes the symmetry and the movement ends on a D major chord. %s The crotchet melody carries "
  "the rhythm of the Hungarian %s folk dance. Dynamics run from piano to forte with %s stabs, and there is a great "
  "deal of staccato throughout."
  % (d.ref(10), dfn("kan&aacute;sz", "A Hungarian swineherd&rsquo;s dance, whose rhythm Bart&oacute;k borrows"),
     dfn("sforzando", "A sudden forced accent")),
  "a clear D major chord at the end. After all that tritone dissonance, the ending is unusually plain.")

# ---- Slightly Tipsy ---------------------------------------------------------
d.add_statement(11, "Tipsy 1 · A", "11 &middot; Stumbling, not walking",
  "True to its title, this movement portrays someone stumbling rather than walking straight. %s It is in %s. Almost "
  "every note of the opening melody is decorated with %s, and that single feature does most of the work in creating "
  "the tipsy feel. The melody is built on the interval of a perfect fourth."
  % (d.ref(11), dfn("ternary form", "Three sections: A, a contrasting B, then a return of A"),
     dfn("acciaccaturas", "Crushed grace notes: a very quick note squeezed in before the main one")),
  "the violins %s, muted and at the tip of the bow for a thin, quiet sound."
  % dfn("col legno", "Striking the string with the wood of the bow instead of the hair"))

d.add_statement(12, "Tipsy 2 · B", "12 &middot; Two motifs, one key change",
  "The B section sets two ideas against each other: an off-beat accompaniment pattern alternating with a smooth "
  "legato melody, the second motif descending by step. %s The music begins major and moves to G minor here, with "
  "parallel chords, chromatic harmony and dissonant added-note chords keeping the tonality ambiguous."
  % d.ref(12),
  "the tonality refusing to settle. Name G minor and the added-note chords rather than saying it sounds odd.")

d.add_statement(13, "Tipsy 3 · A1", "13 &middot; The same, but drunker",
  "The A material returns significantly developed rather than simply repeated. %s The marking is Allegretto rubato, "
  "so the music speeds up and slows down; it is mostly 4/4, but a few bars of 2/4 and one bar of 5/4 unsettle the "
  "phrasing, and slur-staccato articulation makes the whole movement sway."
  % d.ref(13),
  "the pulse leaning and recovering. Dynamics swing from pianissimo to forte with sudden changes.")

# ---- Swineherd's Dance ------------------------------------------------------
d.add_statement(14, "Swineherd 1 · Introduction", "14 &middot; The tune arrives in pieces",
  "The suite ends with the only genuine collected folk tune in it: Bart&oacute;k recorded it in Tolna County in "
  "1907. %s The movement opens over a %s, with fragments of the melody appearing before it properly arrives. The "
  "drone sets the tonal centre on A, and the mode is %s on A."
  % (d.ref(14), dfn("drone", "A sustained note held under the music, like a bagpipe"),
     dfn("mixolydian", "A major-sounding mode with a flattened seventh: A major with G natural")),
  "a held note underneath and scraps of tune above it. The drone is doing the work of a key signature.")

d.add_statement(15, "Swineherd 2 · A", "15 &middot; The folk melody",
  "The first half of the collected melody enters, bars 1 to 16. %s It opens with leaps of fourths and fifths and "
  "then moves by step, sitting quite high. The woodwind carry it &mdash; piccolo, flute, oboe and clarinet &mdash; "
  "over strings playing both bowed and pizzicato, muted and unmuted."
  % d.ref(15),
  "the shape: wide leaps first, then stepwise motion. That contour is what Bart&oacute;k collected, not what he invented.")

d.add_statement(16, "Swineherd 3 · B", "16 &middot; The drone moves",
  "The second half of the melody, bars 17 to 33. %s The drone shifts to D before returning to A, and G sharps in "
  "this half lean the music towards G major. The metre is 2/4 throughout and the marking is Allegro molto: quick "
  "and lively, with moments of calm and changes of tempo."
  % d.ref(16),
  "the drone note changing. In a piece with no key signature to speak of, that is the modulation.")

d.add_statement(17, "Swineherd 4 · A1", "17 &middot; Round again",
  "After a reworked second half and a four-bar link, the first half of the melody returns. %s An %s rhythm &mdash; "
  "quaver, crotchet, quaver &mdash; drives many sections, while the horns and trumpets carry %s melodies against "
  "it. This movement has more sections than any other in the suite."
  % (d.ref(17), dfn("ostinato", "A short pattern repeated persistently"),
     dfn("syncopated", "Accented off the main beat")),
  "the three-note rhythm underneath. Count the sections: introduction, A, B, A1, B2 and coda.")

d.add_statement(18, "Swineherd 5 · B2", "18 &middot; Held back for the coda",
  "The second half returns fragmented and developed, and Bart&oacute;k holds back its final two bars. %s The coda "
  "is then built on exactly those two bars, so the tune only completes itself at the very end. Right at the close, "
  "two solo violins play %s."
  % (d.ref(18), dfn("harmonics", "Light, glassy notes made by touching the string rather than pressing it down")),
  "a melody deliberately left unfinished, then finished. Dynamics run from pianissimo to fortissimo throughout.")

d.add_checklist(
  "Evening in the Village: arch form A B A1 B1 A2, Lento rubato against Allegretto, F sharp minor pentatonic and "
  "Aeolian on F sharp, woodwind with two horns and strings. Bear Dance: varied strophic, sections marked by a D "
  "pedal against an A flat pedal a tritone away, ending on D major. Slightly Tipsy: ternary, acciaccaturas on "
  "almost every note, col legno strings, Allegretto rubato with bars of 2/4 and 5/4. Swineherd's Dance: a genuine "
  "folk tune collected in 1907, mixolydian on A over a drone, 2/4 Allegro molto, ending on violin harmonics.",
  "Name the element or technique, give its correct technical term, and say exactly where it happens. "
  "&ldquo;Bart&oacute;k uses folk music&rdquo; is too general. &ldquo;Bart&oacute;k builds the Allegretto dance "
  "tune of Evening in the Village on snap rhythms&rdquo; names the feature, uses the term and locates it &mdash; "
  "and make sure each term is attached to the right movement.")

content = d.content()
exam_tip, conclusion = renumber_tail(d, old["exam_tip_html"], old["conclusion_html"])
description = ("Follow all four required movements of Bartok's Hungarian Sketches landmark by landmark, from the "
               "village at dusk to the swineherd's dance.")

pq, kc, fc = build_questions_keep(BACKUP)
errs, warns = d.verify(content, (exam_tip or "") + (conclusion or ""))
allids = [int(x) for x in re.findall(r'data-narration-id="n(\d+)"', content + (exam_tip or "") + (conclusion or ""))]
if allids != list(range(1, len(allids) + 1)):
    errs.append("narration ids across content+tip+conclusion not contiguous: %s" % allids[-8:])
for o, lbl in ((pq, "practice"), (kc, "kc"), (fc, "flashcards")):
    check_plain(o, lbl, errs)
if len(description) > 160:
    errs.append("description %d chars" % len(description))
print("cards", len(d.cards), "| narration ids", d._n, "| chars", len(content), "| desc", len(description))
print("card words", d.card_words)
for w in warns:
    print("WARN", w)
if errs:
    print("ERRORS:")
    for e in errs:
        print("  -", e)
    raise SystemExit(1)
print("verify OK")
payload = {"title": TITLE, "content_html": content, "exam_tip_html": exam_tip,
           "conclusion_html": conclusion, "description": description,
           "flashcard_questions": fc, "practice_questions": pq, "knowledge_checks": kc,
           "narration_manifest": None}
io.open(os.path.join(HERE, "html", "aqa_bartok.html"), "w", encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
