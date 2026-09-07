# -*- coding: utf-8 -*-
"""music-aqa / aos2-popular-music / L3 -- Queen: three set tracks.
Rebuilt as a guided-listening deck: one card per landmark across all three
works, with the element observations from the old thematic cards re-filed under
the moment where each is audible.

LIVE lesson, QA'd by ear, so every pin time is carried over unchanged.
Probe corroboration (3 votes per track, timings.json):
  Bohemian Rhapsody  intro 0/2, ballad 49 vs probe 57 (the probe heard the
    words, the pin marks the piano's entry -- pin kept), solo 156 vs 157,
    opera 183 vs 187, hard rock 247 vs 249, outro 295 vs 296. Length 359 OK.
  Seven Seas of Rhye  5 vs 6, 25 vs 26, 63 vs 63, 84 vs 81, 157 vs 155.
    *** data-dur was 187; YouTube's own metadata says 172. FIXED. ***
  Love of My Life  0, 23 vs 21, 97, 113, 143 vs 139, 188 vs 194; the pins carry
    bar numbers from the score, so they are kept over the probe. Length 217 OK.
"""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck_raw import RawDeck, dfn, patch, build_questions_keep, check_plain, renumber_tail

BACKUP = "music-aqa__aos2-popular-music__L03"
HERE = os.path.dirname(os.path.abspath(__file__))
old = json.load(io.open(os.path.join(HERE, "backups", BACKUP + ".json"), encoding="utf-8"))

d = RawDeck(lesson_id=old["id"], subject="music-aqa", unit="aos2-popular-music", lesson_no=3,
            original_html=old["content_html"], durs={"t2": 172})
TITLE = "Queen: Three Set Tracks — Guided Listening"

d.pins = [
    ("t1", "t1c1", 0,   "Intro",        "A cappella &mdash; voices alone, no instruments. Homorhythmic: every voice moves in the same rhythm."),
    ("t1", "t1c2", 49,  "Ballad",       "Arpeggiated accompaniment &mdash; the piano plays each chord one note at a time, rippling under the voice."),
    ("t1", "t1c3", 156, "Guitar solo",  "Virtuosic &mdash; deliberately difficult, high-register playing that shows off the player."),
    ("t1", "t1c4", 183, "Opera",        "Abrupt modulation &mdash; the key jumps to A major, unrelated to home. Question-and-answer phrases between the voices."),
    ("t1", "t1c5", 247, "Hard rock",    "12/8 compound time &mdash; each beat now splits into threes. Count four strong beats, each carrying a triplet."),
    ("t1", "t1c6", 295, "Outro",        "Ending away from home &mdash; the song closes in F major, not the key it began in."),
    ("t2", "t2c1", 5,   "Piano intro",  "Cross-rhythm arpeggios &mdash; the pianist&rsquo;s right hand ripples against the left in a clashing pattern."),
    ("t2", "t2c2", 25,  "Verse",        "Power chords &mdash; bare root-and-fifth guitar chords with no third: the hard rock sound."),
    ("t2", "t2c3", 63,  "Middle",       "The bridge &mdash; the mode shifts and a new melody breaks the verse pattern, ending on a long held vocal cry."),
    ("t2", "t2c4", 84,  "Guitar solo",  "Instrumental contrast &mdash; the guitar takes the melodic lead between sung verses."),
    ("t2", "t2c5", 157, "Seaside outro", "Music-hall pastiche &mdash; the style flips genre completely for a theatrical ending."),
    ("t3", "t3c1", 0,   "Introduction", "Bars 1&ndash;7. Implies F major, then slips to B flat major in its second phrase."),
    ("t3", "t3c2", 23,  "Verses 1 and 2", "Bars 8&ndash;31. They start in C major and modulate to F major."),
    ("t3", "t3c3", 97,  "Instrumental bridge", "Bars 31&ndash;35, in B flat major &mdash; an echo of the introduction&rsquo;s second phrase."),
    ("t3", "t3c4", 113, "Interlude",    "Bars 36&ndash;44. D minor, the relative minor, passing through G minor."),
    ("t3", "t3c5", 143, "Guitar solo",  "Bars 45&ndash;58. Starts in F major, moves to C major, then B flat major."),
    ("t3", "t3c6", 188, "Coda",         "Bars 59&ndash;67. Begins in D minor and finishes in F major &mdash; home at last."),
]

d.add_cover(
  "Three Queen tracks, equal weight",
  [
    "Your study pieces are <em>Bohemian Rhapsody</em>, <em>Seven Seas of Rhye</em> and <em>Love of My Life</em>. "
    "Questions can ask about any of them, so know all three equally. The band: Freddie Mercury (lead vocals, piano), "
    "Brian May (electric guitar, vocals), John Deacon (bass guitar) and Roger Taylor (drum kit, vocals).",
    "<em>Bohemian Rhapsody</em> and <em>Love of My Life</em> come from <em>A Night at the Opera</em> (1975); "
    "<em>Seven Seas of Rhye</em> from <em>Queen II</em> (1974). The set versions are the 2011 remasters. The spread "
    "is deliberate: one multi-sectional epic, one compact hard rock single, one ballad. Revise them side by side.",
    "Press play and the cards follow the music. Use the track buttons to switch songs, and tap any number to jump.",
  ])

# ---- Bohemian Rhapsody ------------------------------------------------------
d.add_statement(1, "Rhapsody 1 · Intro", "1 &middot; Voices alone",
  "The song opens %s, voices with no instruments at all, moving in %s block chords. %s It is in B flat major, and "
  "the very first chord is a B flat 6, an unusual added-sixth. Watch the metre too: the introduction contains "
  "single bars of 5/4 and 9/8 among the 4/4. Listen for the %s slide on &lsquo;reality&rsquo;."
  % (dfn("a cappella", "Voices alone, without instruments"),
     dfn("homorhythmic", "Every voice moving in the same rhythm at the same time"), d.ref(1),
     dfn("portamento", "A smooth slide between two pitches")),
  "one rhythm shared by every voice. The whole song is %s: no repeating chorus anywhere."
  % dfn("through-composed", "Music that keeps moving forward with no repeated sections"))

d.add_statement(2, "Rhapsody 2 · Ballad", "2 &middot; Piano takes over",
  "The piano enters and the ballad begins, still in B flat major, with %s accompaniment rippling under the voice. "
  "%s The word-setting is almost entirely %s. Mercury had a four-octave range and uses it: soaring falsetto in "
  "places, belted chest voice in others. Listen for the Scotch snap on &lsquo;sympathy&rsquo;."
  % (dfn("arpeggiated", "Chords played one note at a time, in a rippling pattern"), d.ref(2),
     dfn("syllabic", "One note for each syllable of text")),
  "the melody rising at the line about looking up &mdash; %s, the music acting out the words."
  % dfn("word painting", "The music acting out the meaning of the words"))

d.add_statement(3, "Rhapsody 3 · Guitar solo", "3 &middot; May takes a chorus",
  "At the end of the ballad the guitar takes over with a %s solo. %s Name what makes it so: fast %s passages, "
  "slides, bends, vibrato and distortion, played high on the instrument. It is a composed melodic statement in its "
  "own right rather than filler between vocal sections."
  % (dfn("virtuosic", "Deliberately difficult, showing off the performer&rsquo;s skill"), d.ref(3),
     dfn("scalic", "Moving up or down the notes of a scale")),
  "the guitar singing rather than strumming. Name two techniques, not just &lsquo;a guitar solo&rsquo;.")

d.add_statement(4, "Rhapsody 4 · Opera", "4 &middot; The opera section",
  "The key jumps to A major, unrelated to the home key &mdash; an abrupt %s. %s The &lsquo;Galileo&rsquo; motif "
  "uses repeated notes and a rising semitone; &lsquo;Bismillah!&rsquo; works as question and answer, the refusal "
  "landing in %s and the group replying in %s chords. The drums copy the voices&rsquo; rhythms rather than keeping a beat."
  % (dfn("modulation", "A change of key"), d.ref(4),
     dfn("octaves", "The same note doubled eight notes apart"),
     dfn("homophonic", "All parts moving together in chords")),
  "voices panned across the stereo field. The staccato crotchet opening imitates the comic characters of real opera.")

d.add_statement(5, "Rhapsody 5 · Hard rock", "5 &middot; The rock section",
  "Everything changes at once: E flat major, heavy overdubbed electric guitar, and a shift into %s. %s That is a "
  "%s signature, so each of the four beats now splits into three. Dynamics swing to fortissimo interjections here, "
  "the loudest the song gets."
  % (dfn("12/8", "Twelve quavers in a bar, grouped as four beats of three"), d.ref(5),
     dfn("compound time", "A metre where each beat divides into three, giving a rolling feel")),
  "count four strong beats, each carrying a triplet. The rest of the song is almost all 4/4.")

d.add_statement(6, "Rhapsody 6 · Outro", "6 &middot; It ends unfinished",
  "The music falls away to piano for a quiet, reflective close. %s The song ends on an F major chord &mdash; the "
  "%s of B flat major, the key it began in. That is why the ending feels unresolved rather than settled: the harmony "
  "is left pointing home without ever arriving."
  % (d.ref(6), dfn("dominant", "The fifth note or chord of a key, which wants to resolve home rather than finish")),
  "the last chord, and ask which key it belongs to. Ending away from home is the point, not an accident.")

# ---- Seven Seas of Rhye -----------------------------------------------------
d.add_statement(7, "Rhye 1 · Piano intro", "1 &middot; Ten bars of piano",
  "A hard rock song in D major, released in February 1974 &mdash; the single that made Queen&rsquo;s name. %s It "
  "opens with a ten-bar piano introduction: an %s riff in octaves, in semiquavers, with the right hand rippling "
  "against the left in a %s. Power chords are already there underneath."
  % (d.ref(7), dfn("arpeggiated", "Chords played one note at a time"),
     dfn("cross-rhythm", "Two rhythmic patterns pulling against each other at the same time")),
  "the two hands clashing deliberately. Name the cross-rhythm rather than calling it &lsquo;busy&rsquo;.")

d.add_statement(8, "Rhye 2 · Verse", "8 &middot; The verse hits",
  "The band arrives and the verse lands on %s, bare root-and-fifth chords with no third, which is the hard rock "
  "sound. %s Listen for %s colouring the vocal line. There is no chorus anywhere in this song: instead a vocal hook "
  "closes each verse."
  % (dfn("power chords", "Bare two-note guitar chords, root and fifth, with no third"), d.ref(8),
     dfn("blues notes", "Expressively lowered notes, usually the flattened third or seventh")),
  "a chord with no major or minor quality to it. That missing third is what makes a power chord.")

d.add_statement(9, "Rhye 3 · Middle", "9 &middot; The bridge",
  "This is the contrast section. %s The mode shifts, a new melody breaks the verse pattern, and the passage ends "
  "with a long held vocal cry that launches the guitar solo. Listen for %s on the guitar in the first bridge, which "
  "damps the strings for a tighter, drier attack."
  % (d.ref(9), dfn("palm-muting", "Resting the picking hand on the strings to damp them, giving a tight, muffled tone")),
  "the change of mode and the held cry at the end. A bridge is defined by contrast, not by position.")

d.add_statement(10, "Rhye 4 · Guitar solo", "10 &middot; Away and back",
  "The guitar takes the melodic lead between sung verses. %s Track the keys: the solo moves to B flat major before "
  "returning to D, and the second bridge %s to G major. A %s effect closes the solo &mdash; the signal repeated back "
  "at itself a fraction later."
  % (d.ref(10), dfn("modulates", "Changes key"),
     dfn("delay", "An effect that repeats a sound a short time after the original, like a controlled echo")),
  "the key shifting under the solo. Naming B flat major beats saying &lsquo;it changes key&rsquo;.")

d.add_statement(11, "Rhye 5 · Seaside outro", "11 &middot; A different world",
  "The song dissolves into a music-hall singalong of &lsquo;I Do Like to Be Beside the Seaside&rsquo;, played on a "
  "%s. %s Ending a hard rock single on a Victorian seaside tune is deliberate %s: the style flips completely, and "
  "the joke is the point."
  % (dfn("stylophone", "A pocket electronic keyboard played with a stylus"), d.ref(11),
     dfn("pastiche", "Deliberate imitation of another style")),
  "the genre switching in a single bar. Name the borrowed tune and the instrument playing it.")

# ---- Love of My Life --------------------------------------------------------
d.add_statement(12, "Love 1 · Introduction", "12 &middot; Home, almost",
  "The ballad of the three, and the one to choose for a texture or %s question. %s Home is F major, but the harmony "
  "travels constantly, and naming where it goes is where the marks are. The short introduction, bars 1 to 7, implies "
  "F major and then slips to B flat major in its second phrase."
  % (dfn("sonority", "The particular sound quality of voices and instruments; timbre"), d.ref(12)),
  "a key established and immediately left. Give the bar numbers if you can &mdash; this song is examined on detail.")

d.add_statement(13, "Love 2 · Verses 1 and 2", "13 &middot; The verses",
  "Bars 8 to 31. %s The two verses start in C major and %s to F major. Around Mercury, who sings in his %s range "
  "with moments of %s, sit layered backing vocals, harp and arpeggiated piano. The harp is played by Brian May, who "
  "taught himself the instrument for this song."
  % (d.ref(13), dfn("modulate", "Change key"), dfn("tenor", "The higher male voice range"),
     dfn("falsetto", "A male voice pushed above its natural range, light and airy")),
  "an orchestral harp inside a rock band. That is not a normal rock sonority, and it is examinable.")

d.add_statement(14, "Love 3 · Instrumental bridge", "14 &middot; An echo",
  "Bars 31 to 35, in B flat major. %s This passage echoes the second phrase of the introduction, so material you "
  "heard in the first seven bars comes back without the voice. Recognising a returning idea, and saying which "
  "earlier passage it belongs to, is worth more than describing the sound."
  % d.ref(14),
  "a phrase you have already heard, now instrumental and in B flat major.")

d.add_statement(15, "Love 4 · Interlude", "15 &middot; Into the minor",
  "Bars 36 to 44. %s The music turns to D minor, the %s of F major, passing through G minor on the way. This is the "
  "darkest point in the song&rsquo;s harmonic journey, and it is reached by step rather than by a jolt."
  % (d.ref(15), dfn("relative minor", "The minor key sharing a key signature with the major: D minor to F major")),
  "the shift from major to minor colour. Name D minor and the route through G minor, not just &lsquo;it gets sadder&rsquo;.")

d.add_statement(16, "Love 5 · Guitar solo", "16 &middot; Three keys",
  "Bars 45 to 58. %s The guitar solo begins in F major, moves to C major, then B flat major. Three keys in fourteen "
  "bars is the clearest demonstration in the set of how restless this song&rsquo;s harmony is, and every one of "
  "those keys is nameable in an answer."
  % d.ref(16),
  "the ground shifting under the solo three times. Location plus key name is the full mark.")

d.add_statement(17, "Love 6 · Coda", "17 &middot; Home at last",
  "Bars 59 to 67. %s The coda begins in D minor and finishes in F major: the song only settles at home in its last "
  "bars. Set that against <em>Bohemian Rhapsody</em>, which deliberately ends away from home, and you have a "
  "comparison that writes itself."
  % d.ref(17),
  "the final arrival in F major. Two of the three tracks have no chorus; this one has no early resolution either.")

d.add_checklist(
  "Bohemian Rhapsody: through-composed, no chorus; a cappella and ballad in B flat major, opera in A major, rock "
  "section in E flat major and 12/8, ending on F major; roughly 180 vocal overdubs. Seven Seas of Rhye: hard rock "
  "in D major, February 1974; ten-bar piano introduction, power chords, palm-muting, a solo through B flat and a "
  "stylophone seaside pastiche. Love of My Life: F major ballad travelling through C, B flat, D minor and G minor, "
  "with harp, layered backing vocals and arpeggiated piano.",
  "Marks come from three things: name the element, give its exact technical term, and say where in the track it "
  "happens. &ldquo;The harmony is interesting&rdquo; earns nothing. &ldquo;The opera section shifts abruptly to A "
  "major, an unrelated key&rdquo; earns the mark &mdash; element, term, location.")

content = d.content()
exam_tip, conclusion = renumber_tail(d, old["exam_tip_html"], old["conclusion_html"])
description = ("Follow all three Queen set tracks landmark by landmark: Bohemian Rhapsody, Seven Seas of Rhye and "
               "Love of My Life.")

pq, kc, fc = build_questions_keep(BACKUP)
errs, warns = d.verify(content, (exam_tip or "") + (conclusion or ""))
allids = [int(x) for x in __import__("re").findall(r'data-narration-id="n(\d+)"', content + (exam_tip or "") + (conclusion or ""))]
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
io.open(os.path.join(HERE, "html", "aqa_queen.html"), "w", encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
