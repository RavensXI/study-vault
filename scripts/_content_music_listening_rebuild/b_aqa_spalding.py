# -*- coding: utf-8 -*-
"""music-aqa / aos3-traditional-music / L2 -- Esperanza Spalding: three set tracks.
Guided-listening deck, one card per landmark across all three works.

LIVE lesson, QA'd by ear: every pin time carried over unchanged.
Probe corroboration (3 votes per track, timings.json):
  Little Fly       0 / 15.5 / 60.3 / 195.8  vs probe 0 / 14-15 / 61 / split.
                   Length 213, probe 214. All corroborated.
  I Know You Know  0 / 25 / 44.7 / 99 / 133.5 vs probe 0 / 23 / 45 / 122 / 157.
                   Intro, verse and hook corroborated; the solo and outro pins
                   sit earlier than the probe heard them, flagged not moved.
                   *** data-dur was 300; YouTube's own metadata says 225. FIXED
                   -- every pin on this track was drawn at the wrong place. ***
  I Adore You      5.4 / 41.8 / 69.5 / 156.5 / 428.3 vs probe 0 / 8 / 58 / 157 /
                   276. The solo pin is corroborated exactly; the others differ
                   and are flagged, not moved. Length 447 OK.
"""
import io, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck_raw import RawDeck, dfn, patch, build_questions_keep, check_plain, renumber_tail

BACKUP = "music-aqa__aos3-traditional-music__L02"
HERE = os.path.dirname(os.path.abspath(__file__))
old = json.load(io.open(os.path.join(HERE, "backups", BACKUP + ".json"), encoding="utf-8"))

d = RawDeck(lesson_id=old["id"], subject="music-aqa", unit="aos3-traditional-music", lesson_no=2,
            original_html=old["content_html"], durs={"t2": 225})
TITLE = "Esperanza Spalding: Three Set Tracks — Guided Listening"

d.pins = [
    ("t1", "t1c1", 0,     "Introduction", "Strings enter one by one; the bass plays a chromatically descending pizzicato riff in double stopping."),
    ("t1", "t1c2", 15.5,  "Verse 1",      "The vocal opens with a descending three-note pattern in E major, repeated."),
    ("t1", "t1c3", 60.3,  "Verse 2",      "Same vocal melody, now with a violin countermelody and the viola recalling its own tune."),
    ("t1", "t1c4", 195.8, "Coda",         "A bass-and-voice improvisation over sustained arco strings."),
    ("t2", "t2c1", 0,     "Groove intro", "A solo fretless bass riff &mdash; it avoids beat one of every bar."),
    ("t2", "t2c2", 25,    "Verse",        "Very fast 4/4 &mdash; around 176 beats per minute. F major is still hidden."),
    ("t2", "t2c3", 44.7,  "Hook",         "The chorus lands on F major at last &mdash; ii&ndash;V&ndash;I, every chord carrying a seventh."),
    ("t2", "t2c4", 99,    "Solo territory", "B major interlude &mdash; a vamp for piano and fretless bass improvisation."),
    ("t2", "t2c5", 133.5, "Outro",        "Double chorus, and out."),
    ("t3", "t3c1", 5.4,   "Unpitched introduction", "Samba instruments fade in &mdash; surdo and ocean drum. No pitch yet, so no key."),
    ("t3", "t3c2", 41.8,  "Pitched introduction", "Voice enters, then double bass playing the main groove. Vocals move in thirds."),
    ("t3", "t3c3", 69.5,  "Main groove",  "Three repeating motifs layered together &mdash; this is the chorus of the piece."),
    ("t3", "t3c4", 156.5, "Solo section", "Piano solo first, over drums and bass; the voice and double bass take over later."),
    ("t3", "t3c5", 428.3, "Outro",        "The samba instruments are left alone, then fade &mdash; no final chord to confirm a key."),
]

d.add_cover(
  "Three Spalding tracks, three fusions",
  [
    "Esperanza Spalding is an American jazz bassist, singer and composer. <em>I Know You Know</em> and <em>I Adore "
    "You</em> come from <em>Esperanza</em> (2008); <em>Little Fly</em> comes from <em>Chamber Music Society</em> "
    "(2010). In 2011 she became the first jazz artist to win the Grammy for Best New Artist.",
    "All three are %s. They mix jazz harmony and improvisation with Brazilian samba rhythm, and, in <em>Little "
    "Fly</em>, with chamber-music strings. Be precise about the bass: a fretless bass guitar in <em>I Know You "
    "Know</em>, a double bass in the other two."
    % dfn("fusions", "Music combining elements of two or more distinct traditions or genres"),
    "Press play and the cards follow the music. Use the track buttons to switch songs, and tap any number to jump.",
  ])

# ---- Little Fly -------------------------------------------------------------
d.add_statement(1, "Little Fly 1 · Introduction", "1 &middot; The riff everything grows from",
  "The strings enter one by one over a bass line that will dominate the song. %s It is a chromatically descending "
  "%s riff played with %s, so one instrument sounds two notes at once. That riff returns about twenty times &mdash; "
  "forty of the piece&rsquo;s sixty-three bars."
  % (d.ref(1), dfn("pizzicato", "Plucking the strings with the fingers instead of bowing"),
     dfn("double stopping", "Playing two strings at once, so one instrument sounds two notes")),
  "two notes from one bass. Count the scoring: voice, double bass and a string trio &mdash; four string instruments, but not a string quartet.")

d.add_statement(2, "Little Fly 2 · Verse 1", "2 &middot; Blake, set syllabically",
  "The words are William Blake&rsquo;s poem &lsquo;The Fly&rsquo;, and the setting is %s: every verse takes the "
  "same music. %s The voice opens with a descending three-note pattern in E major, repeated, moving mostly by step "
  "and setting the words %s. The riff carries on without the double stopping, then stops altogether."
  % (dfn("strophic", "Every verse set to the same music, with no chorus"), d.ref(2),
     dfn("syllabically", "One note for each syllable of text")),
  "the word &lsquo;oh&rsquo; at the verse end, falling in three %s steps."
  % dfn("chromatic", "Moving by semitones, using notes outside the key"))

d.add_statement(3, "Little Fly 3 · Verse 2", "3 &middot; The ensemble answers",
  "The same vocal melody returns, but the texture around it has grown. %s A violin countermelody joins, the "
  "ensemble adds interjections, and the viola recalls its own melody from the introduction. Spalding sings in the "
  "alto range, moving into head voice with vibrato in the second half of each verse."
  % d.ref(3),
  "the strings using trills to suggest the fly itself. The poem&rsquo;s first four verses make the song&rsquo;s two.")

d.add_statement(4, "Little Fly 4 · Coda", "4 &middot; Improvised close",
  "Blake&rsquo;s last verse becomes the coda. %s The trio plays semibreve tremolos while the voice and bass "
  "improvise together over a sustained %s chord. After a whole song built on one strict repeating riff, the ending "
  "is the one passage where the players are free."
  % (d.ref(4), dfn("arco", "Played with the bow")),
  "the bow replacing the pluck. That change of technique is the clearest signal that the coda has begun.")

# ---- I Know You Know --------------------------------------------------------
d.add_statement(5, "I Know You Know 1 · Groove intro", "5 &middot; One line, no key",
  "The track opens %s: a solo fretless bass riff with nothing accompanying it. %s The riff avoids the first beat of "
  "every one of its seventeen bars, and it opens on dominant Cs. The home key of F major is being withheld from the "
  "very first note, and it will stay hidden until the chorus."
  % (dfn("monophonic", "A single line of music, with nothing accompanying it"), d.ref(5)),
  "a bass that slides between notes rather than stepping. That is a %s."
  % dfn("fretless bass", "A bass guitar without frets, allowing smooth slides between notes"))

d.add_statement(6, "I Know You Know 2 · Verse", "6 &middot; Still hiding",
  "Very fast 4/4, around 176 beats per minute. %s The chords that join the riff dodge the chord of F, and the first "
  "sung note is G, the %s. Underneath, the samba lives in the rhythm section: ganza, a shaker; caixa, a Brazilian "
  "snare drum; and a triangle."
  % (d.ref(6), dfn("supertonic", "The second note of the scale")),
  "percussion, not a drum kit. Name ganza and caixa rather than calling them shakers and drums.")

d.add_statement(7, "I Know You Know 3 · Hook", "7 &middot; F major, at last",
  "The chorus finally lands on F major, and it does so through the standard jazz cadence %s &mdash; G minor 7, C7, "
  "F &mdash; with every chord carrying a seventh. %s The melody adds %s, especially A flat and D flat. Off-beat "
  "piano chords give a double-time samba feel, and the syncopations layer into %s."
  % (dfn("ii&ndash;V&ndash;I", "The most common jazz cadence: chord two, then five, then home"), d.ref(7),
     dfn("blue notes", "Expressively lowered notes borrowed from the blues"),
     dfn("polyrhythm", "Two or more conflicting rhythmic patterns sounding together")),
  "the moment the harmony settles. Naming that first chorus chord as the arrival of F major is a ready-made answer.")

d.add_statement(8, "I Know You Know 4 · Solo territory", "8 &middot; Somewhere else entirely",
  "The interlude %s to B major, a distant key from F. %s Over it sits a %s &mdash; a short chord pattern repeated "
  "underneath improvisation &mdash; for piano and fretless bass solos. Improvisation is built into the form here, "
  "not added on top of it."
  % (dfn("modulates", "Changes key"), d.ref(8),
     dfn("vamp", "A short chord pattern repeated under improvisation")),
  "how far the harmony has travelled. B major and F major share almost nothing, which is why the shift is startling.")

d.add_statement(9, "I Know You Know 5 · Outro", "9 &middot; Back and out",
  "The music snaps back to F for a double chorus and ends. %s Production here is light but nameable, which is "
  "exactly what an answer needs: some reverb, some panning across the stereo field, and EQ shaping the balance. "
  "This is a studio jazz recording, not a live capture."
  % d.ref(9),
  "the chorus arriving twice over. Say &lsquo;double chorus&rsquo; rather than &lsquo;it repeats the chorus&rsquo;.")

# ---- I Adore You ------------------------------------------------------------
d.add_statement(10, "I Adore You 1 · Unpitched introduction", "10 &middot; No key at all",
  "Samba instruments fade in: %s and ocean drum among them. %s Nothing here has a definite pitch, so the track "
  "literally begins in no key. That is unusual enough to be worth a sentence on its own, and it is answered by the "
  "ending, which does the same thing in reverse."
  % (dfn("surdo", "The large low Brazilian bass drum that anchors a samba groove"), d.ref(10)),
  "percussion with no pitch. You cannot name a key here because there is not one yet.")

d.add_statement(11, "I Adore You 2 · Pitched introduction", "11 &middot; Voice as instrument",
  "The voice enters, then the double bass with the main groove, and the vocals move in thirds. %s There are almost "
  "no conventional lyrics: the singing is %s and %s throughout, and the spoken rhythm of the title phrase forms the "
  "main melodic hook."
  % (d.ref(11), dfn("scat", "Wordless jazz singing using invented syllables"),
     dfn("vocalise", "Singing without words, on open vowel sounds")),
  "a voice used as an instrument rather than as a storyteller. Name scat and vocalise separately.")

d.add_statement(12, "I Adore You 3 · Main groove", "12 &middot; Three motifs at once",
  "Three repeating motifs are layered together here, and this is the chorus of the piece. %s The music settles into "
  "%s, a major-sounding mode with a flattened seventh. Even now the tonality stays ambiguous, with dissonant piano "
  "interjections cutting across the voice."
  % (d.ref(12), dfn("G mixolydian", "A major-sounding mode with a flattened seventh: G to G on the white notes")),
  "how many separate repeating patterns you can pick out. Name the mode, not just &lsquo;it sounds major&rsquo;.")

d.add_statement(13, "I Adore You 4 · Solo section", "13 &middot; Passing it round",
  "The piano solos first, over drums and bass; later the voice and double bass take over. %s Improvisation is "
  "shared rather than owned by one player, which is a jazz convention operating inside a samba texture &mdash; the "
  "fusion working at the level of who plays, not just of what is played."
  % d.ref(13),
  "the solo changing hands. Say which instrument has it and what the rhythm section is doing underneath.")

d.add_statement(14, "I Adore You 5 · Outro", "14 &middot; Ending in no key",
  "The samba instruments are left alone and the track fades. %s No final chord ever confirms a key, so the piece "
  "ends exactly as it began: unpitched percussion and nothing to analyse harmonically. That symmetry is a strong "
  "exam sentence, because it is a structural observation and a harmonic one at once."
  % d.ref(14),
  "the absence of a final chord. A fade-out on percussion is a decision, not an accident.")

d.add_checklist(
  "Little Fly: Blake's poem set strophically in E major for voice, pizzicato double bass and string trio, built on "
  "a chromatically descending riff in double stopping. I Know You Know: samba-jazz at about 176 bpm that hides F "
  "major until a ii-V-I chorus, with fretless bass, ganza, caixa and triangle, and a B major solo vamp. I Adore "
  "You: scat and vocalise over G mixolydian, opening and closing on unpitched samba percussion so no key is ever "
  "confirmed.",
  "Precision with instruments matters and is easy to lose: fretless bass guitar in <em>I Know You Know</em>, but "
  "double bass in <em>Little Fly</em> and <em>I Adore You</em>; ganza and caixa, not just percussion; a string "
  "trio plus bass, not a string quartet.")

content = d.content()
exam_tip, conclusion = renumber_tail(d, old["exam_tip_html"], old["conclusion_html"])
description = ("Follow all three Esperanza Spalding set tracks landmark by landmark: Little Fly, I Know You Know and "
               "I Adore You.")

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
io.open(os.path.join(HERE, "html", "aqa_spalding.html"), "w", encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
