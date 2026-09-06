# -*- coding: utf-8 -*-
"""music-edexcel / aos1-instrumental-music / L5 -- Pathetique i, ELEMENTS walk.
Same recording as L4 (hcczxDKkYhU, 560 s) and the same verified pin times; the
cards take one element each: dynamics, texture and piano writing, tonality,
harmony, melody, tempo and metre. The exposition-repeat pin (221 s) belongs to
L4's structural walk and is not repeated here."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck import Deck, dfn, patch, build_questions, check_plain

BACKUP = "music-edexcel__aos1-instrumental-music__L05"
d = Deck(lesson_id="2d211a92-34ee-40e7-9ce8-27d39102c7c3",
         subject="music-edexcel", unit="aos1-instrumental-music", lesson_no=5,
         yt="hcczxDKkYhU", dur=560, track_label="Path&eacute;tique i",
         credit="Fabian M&uuml;ller, streamed from YouTube (Deutsche Grammophon) &mdash; not hosted by StudyVault. "
                "Beethoven: Piano Sonata No. 8 &lsquo;Path&eacute;tique&rsquo;, 1st movement.")
TITLE = "Beethoven: Pathétique Sonata, First Movement — The Elements in Close-Up"

d.pins = [
    ("t1c1", 0,   "Dynamics",   "Loud, then instantly quiet. The whole introduction is built from that pairing."),
    ("t1c2", 100, "Texture",    "Melody over tremolo: one pianist making an orchestra&rsquo;s shudder."),
    ("t1c3", 143, "Tonality",   "E flat minor where E flat major was expected. Name the key, not just the change."),
    ("t1c4", 329, "Harmony",    "Diminished sevenths again. The chords with nowhere to go."),
    ("t1c5", 375, "Melody",     "Themes broken into scraps and pushed up and down in sequence."),
    ("t1c6", 505, "Tempo",      "Grave against Allegro one last time, then the abrupt close."),
]

d.add_cover(
  "The same movement, element by element",
  [
    "Beethoven&rsquo;s first movement of 1798, for solo piano: C minor, common time, a %s introduction followed by an "
    "Allegro di molto e con brio in %s, with the Grave returning twice inside the fast music."
    % (dfn("Grave", "A very slow, solemn tempo marking"),
       dfn("sonata form", "A structure in three sections: exposition, development and recapitulation")),
    "The previous lesson followed that shape from end to end. This one stops six times, once for each %s the exam "
    "asks about: dynamics, texture, tonality, harmony, melody, and tempo with metre."
    % dfn("element of music", "The building blocks of music: melody, harmony, tonality, texture, timbre, dynamics, rhythm, metre, tempo and structure"),
    "Press play and the cards follow the music. Tap any number to jump to that moment.",
  ])

d.add_statement(1, "Dynamics", "1 &middot; Loud, then suddenly quiet",
  "The first chord is heavy and the answer to it is hushed. %s That is an %s attack: a strong sound cut off into a "
  "quiet continuation. Beethoven also drops %s accents on to beats you do not expect. There is no gentle swelling "
  "here, only sudden change, and that is the emotional temperature of the piece."
  % (d.ref(1), dfn("fp", "Forte-piano: play loudly, then immediately softly"),
     dfn("sforzando", "A sudden strong accent on a single note or chord")),
  "the size of the drop between the two halves of each gesture. Describe the contrast, not just the volume.")

d.add_statement(2, "Texture", "2 &middot; One pianist, one orchestra",
  "The Allegro is a melody over an accompaniment, but listen to what the accompaniment is doing. %s The left hand "
  "plays a %s &mdash; a note repeated so fast it becomes a shudder &mdash; imitating tremolo strings. Beethoven also "
  "uses %s that span most of the keyboard, so a single player fills an orchestral space."
  % (d.ref(2), dfn("tremolo", "Very rapid repetition of a note, octave or chord"),
     dfn("wide-spaced chords", "Chords whose notes are spread far apart across the keyboard, giving weight and resonance")),
  "the repeated notes underneath rather than the tune on top. Melody over tremolo is the sound of the first subject.")

d.add_statement(3, "Tonality", "3 &middot; The key you did not expect",
  "A second theme arrives, and what matters is its key. %s From C minor the standard move is to E flat major, the %s. "
  "Beethoven writes E flat minor, so the contrast keeps the shadow, and only later opens into E flat major. In the "
  "recapitulation the group appears in F minor first."
  % (d.ref(3), dfn("relative major", "The major key sharing a key signature with a minor key: E flat major for C minor")),
  "a change of theme that is not a change of mood. The mark is for naming the minor, not for hearing a modulation.")

d.add_statement(4, "Harmony", "4 &middot; Chords with nowhere to go",
  "The Grave&rsquo;s harmony comes back with the Grave itself. %s A %s is built entirely from minor thirds, so it "
  "belongs to no single key and can be pushed in several directions at once. Beethoven uses it, with other %s chords, "
  "to keep the ear from ever settling."
  % (d.ref(4), dfn("diminished seventh chord", "A chord of stacked minor thirds, with no strong pull to one key"),
     dfn("chromatic", "Using notes from outside the prevailing key")),
  "harmony that sounds tense without resolving. Say why it is unstable, not just that it is.")

d.add_statement(5, "Melody", "5 &middot; Themes taken apart",
  "The development introduces no new tune at all. %s Beethoven takes short pieces of the first subject and the bridge "
  "and repeats them a step higher or lower, which is %s, tossing them between the hands in %s. Recognising a familiar "
  "theme in fragments is exactly what the exam tests."
  % (d.ref(5), dfn("sequence", "Repeating a short idea immediately at a higher or lower pitch"),
     dfn("imitation", "One hand or part repeating an idea just after the other has played it")),
  "scraps rather than whole themes. If you know the tune but cannot find all of it, you are in the development.")

d.add_statement(6, "Tempo", "6 &middot; Two speeds, one bar length",
  "Grave breaks in one final time before the close. %s Notice what changes and what does not: the tempo swings "
  "between Grave and Allegro di molto e con brio, but the %s stays common time throughout. The %s ends the movement "
  "quickly and abruptly, in C minor."
  % (d.ref(6), dfn("metre", "The pattern of strong and weak beats in a bar"),
     dfn("coda", "A closing passage that rounds off a movement")),
  "a change of tempo, not of time signature. Say &lsquo;the tempo changes to Grave&rsquo;, not &lsquo;the metre changes&rsquo;.")

d.add_checklist(
  "Melody: rising first subject, lyrical second subject, fragmented by sequence and imitation in the development. "
  "Harmony: chromatic, driven by diminished sevenths. Tonality: C minor, second subject in E flat minor turning to E "
  "flat major, F minor in the recapitulation. Texture: homophonic, melody over tremolo, with wide-spaced chords. "
  "Dynamics: sudden fp contrasts and sforzando accents rather than gradual change. Tempo and metre: Grave against "
  "Allegro di molto e con brio, common time throughout. Timbre: the full range and weight of the piano.",
  "Attach every term to a moment. &ldquo;Chromatic harmony&rdquo; earns little; &ldquo;diminished sevenths in the "
  "Grave leave the key uncertain, which is why the opening sounds so unsettled&rdquo; earns the mark.")

content = d.content()
exam_tip = ("<p>Element questions want the technique, then what it does. Do not stop at &lsquo;tremolo&rsquo;: say "
            "that the tremolo bass gives a shuddering, orchestral drive under the first subject. Do not stop at "
            "&lsquo;diminished seventh&rsquo;: say that it is built from minor thirds, so it belongs to no key and "
            "leaves the harmony unstable. The second half of each sentence is where the marks are.</p>")
conclusion = ("<p>You can now name each element of this movement and point to where it is audible: fp contrasts and "
              "sforzando accents, melody over tremolo, the second subject in the unexpected E flat minor, the "
              "diminished sevenths of the Grave, first-subject fragments worked in sequence, and the swing between "
              "Grave and Allegro inside an unchanging common time. Set it beside the Brandenburg finale and the "
              "contrast between Baroque and Classical style will do the rest.</p>")
description = ("Six numbered stops in Beethoven's Pathetique first movement, one for each element: dynamics, texture, "
               "tonality, harmony, melody and tempo.")

flashcards = [
  {"q": "What is unusual about how Beethoven treats the Grave introduction across the movement?",
   "a": "It returns twice more after the opening, at the start of the development and briefly before the coda, rather than being used only once, which ties the slow and fast material together."},
  {"q": "What texture supports the first subject of the Allegro?",
   "a": "A melody in the right hand over a rapid tremolo accompaniment in the left hand, a homophonic texture that imitates orchestral strings."},
  {"q": "In what key does the second subject appear in the exposition, and how does this change in the recapitulation?",
   "a": "E flat minor in the exposition, brightening to E flat major, and F minor in the recapitulation before the music settles in C."},
  {"q": "Why are diminished seventh chords effective in creating tension?",
   "a": "They are built entirely from minor thirds, so they have no strong pull to a single key and can be reinterpreted to move quickly between keys."},
  {"q": "What dynamic marking creates sudden dramatic contrast in the Grave?",
   "a": "The fp, or forte-piano: a loud attack followed immediately by a quiet continuation. Sforzando accents on unexpected beats do similar work."},
  {"q": "Does the metre change when the Grave returns?",
   "a": "No. The tempo changes between Grave and Allegro di molto e con brio, but the movement stays in common time throughout."},
]

practice = [
  {"text": "Identify the tempo marking of the introduction that opens the first movement of the Pathetique.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for Grave."},
  {"text": "Name the key in which the second subject first appears during the exposition.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for E flat minor. Do not credit E flat major."},
  {"text": "Describe the texture used beneath the first subject melody in the Allegro.", "marks": 2, "kind": "Description",
   "mark_scheme": "One mark: a tremolo accompaniment of rapidly repeated notes or octaves in the left hand. One mark: it supports a driving right-hand melody, making the texture homophonic, melody over accompaniment."},
  {"text": "Explain why the return of the Grave material before the coda is considered structurally unusual for its time.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: slow introductions of the period were not normally reused once the fast music began. One mark: Beethoven brings the Grave back to frame and unify the movement. One mark: this integrates the slow and fast material into one argument instead of treating the introduction as disposable."},
  {"text": "Explain how diminished seventh chords contribute to the mood of the Grave introduction.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: a diminished seventh is built from stacked minor thirds. One mark: it has no strong pull to one key, so the harmony sounds unstable. One mark: that instability matches the searching, uncertain character of the opening."},
  {"text": "Discuss how Beethoven uses dynamics across the movement to create dramatic contrast, referring to specific passages.", "marks": 4, "kind": "Explanation",
   "mark_scheme": "One mark: sudden fp attacks in the Grave, loud answered instantly by quiet. One mark: sforzando accents fall on unexpected beats. One mark: abrupt shifts between loud and quiet in the fast sections rather than gradual change. One mark: an explanation of the shock or struggle these contrasts create for the listener."},
]

kcs = [
  {"q": "What is the tempo marking of the slow introduction to the first movement?",
   "options": ["Adagio", "Grave", "Largo", "Andante"], "correct": 1},
  {"q": "In which key does the second subject first appear in the exposition?",
   "options": ["E flat major", "E flat minor", "C major", "G minor"], "correct": 1},
  {"q": "What texture underpins the first subject melody in the Allegro?",
   "options": ["Tremolo accompaniment", "Fugal imitation", "Unaccompanied melody", "Drone bass"], "correct": 0},
  {"q": "How many times is the Grave material heard during the movement, including the opening?",
   "options": ["Once, at the start only", "Twice in total", "Three times in total", "It never returns"], "correct": 2},
  {"q": "What harmonic device does Beethoven frequently use in the Grave to create instability?",
   "options": ["Pedal points", "Diminished seventh chords", "Parallel fifths", "Pentatonic scales"], "correct": 1},
]

pq, kc, fc = build_questions(BACKUP, practice, kcs, flashcards)
errs, warns = d.verify(content, exam_tip + conclusion)
for o, lbl in ((pq, "practice"), (kc, "kc"), (fc, "flashcards")):
    check_plain(o, lbl, errs)
if len(description) > 160:
    errs.append("description %d chars" % len(description))
print("cards", len(d.cards), "| narration ids", d._n, "| chars", len(content), "| desc", len(description))
for w in warns:
    print("WARN", w)
if errs:
    print("ERRORS:")
    for e in errs:
        print("  -", e)
    raise SystemExit(1)
print("verify OK")
payload = {"title": TITLE, "content_html": content, "exam_tip_html": exam_tip, "conclusion_html": conclusion,
           "description": description, "flashcard_questions": fc, "practice_questions": pq,
           "knowledge_checks": kc, "narration_manifest": None}
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", "pathetique_l5.html"), "w",
        encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
