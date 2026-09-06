# -*- coding: utf-8 -*-
"""music-edexcel / aos3-stage-and-screen / L3 -- Defying Gravity, ELEMENTS walk.
Same recording as L2 (l0Bs_eaXaCo, 352 s). Pin times: 1:16 the accompaniment
turns to a continuous driving rhythm (2/3, and the same second as the 3/3
'Something has changed within me' cue), 1:53 the title phrase (3/3), 3:00 the
word 'Unlimited' first sung (2/3), 3:27 two voices together (2/3), 4:32 the key
lift (2/3), 5:28 the sustained high note (2/3)."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck import Deck, dfn, patch, build_questions, check_plain

BACKUP = "music-edexcel__aos3-stage-and-screen__L03"
d = Deck(lesson_id="e376b794-6f79-4361-8edd-a305ef14b1ca",
         subject="music-edexcel", unit="aos3-stage-and-screen", lesson_no=3,
         yt="l0Bs_eaXaCo", dur=352, track_label="Defying Gravity",
         credit="Original Broadway cast recording, streamed from YouTube &mdash; not hosted by StudyVault. "
                "Schwartz: Defying Gravity (Wicked).")
TITLE = "Schwartz: Defying Gravity — The Elements in Close-Up"

d.pins = [
    ("t1c1", 76,  "Rhythm",   "Free speech-rhythm gives way to continuous quavers. Count the pulse from here."),
    ("t1c2", 113, "Melody",   "The rising hook, with a wide upward leap on the key word."),
    ("t1c3", 180, "Motif",    "The rising &lsquo;Unlimited&rsquo; idea, and the film song hidden inside it."),
    ("t1c4", 207, "Texture",  "Two voices at once above the band. Count the layers."),
    ("t1c5", 272, "Tonality", "The key steps up, and not always to the key you would expect."),
    ("t1c6", 328, "Dynamics", "Everything playing, everything loud, one note held above it."),
]

d.add_cover(
  "The same number, element by element",
  [
    "Stephen Schwartz&rsquo;s act one finale from <em>Wicked</em> (2003), for two solo voices with a %s of strings, "
    "woodwind and brass plus a rock rhythm section of electric guitar, bass, drum kit and keyboards."
    % dfn("pit orchestra", "The instrumental ensemble that plays below or beside the stage in a musical"),
    "The previous lesson followed the number section by section. This one stops six times, once for each %s the exam "
    "sets questions on: rhythm, melody, motif, texture, tonality and dynamics with orchestration."
    % dfn("element of music", "The building blocks of music: melody, harmony, tonality, texture, timbre, dynamics, rhythm, metre, tempo and structure"),
    "Press play and the cards follow the music. Tap any number to jump to that moment.",
  ])

d.add_statement(1, "Rhythm", "1 &middot; A pulse at last",
  "The opening had no steady beat, because the lines followed the rhythm of speech. %s Now the accompaniment settles "
  "into continuous quavers, a repeating rhythmic %s under everything. Against that busy pattern the singer holds long "
  "notes, so the two layers pull in opposite directions: still voice, restless band."
  % (d.ref(1), dfn("ostinato", "A short pattern repeated persistently, often in the accompaniment")),
  "held notes above driving quavers. That contrast is the texture examiners most often ask you to describe here.")

d.add_statement(2, "Melody", "2 &middot; A tune that climbs",
  "The title phrase is set to a rising figure with a wide upward %s on the key word. %s Schwartz also colours several "
  "phrases with the %s, a five-note scale with no semitone steps, which sounds open and unforced even while the "
  "harmony underneath is doing something more complicated."
  % (dfn("leap", "Movement between notes that are not next to each other in the scale"), d.ref(2),
     dfn("pentatonic scale", "A five-note scale that omits the semitone steps of the full major or minor scale")),
  "the shape rising while the accompaniment stays busy. Name the leap and say what it depicts.")

d.add_statement(3, "Motif", "3 &middot; The idea inside the idea",
  "This short rising %s returns through the number, each time a little higher, which is %s. %s Schwartz has said it "
  "nods to the opening interval of the famous rainbow song from <em>The Wizard of Oz</em>, but he changes the rhythm "
  "and where it falls in the bar, so it echoes rather than quotes."
  % (dfn("motif", "A short, recognisable musical idea that recurs and develops through a piece"),
     dfn("sequence", "Repeating an idea at progressively higher or lower pitch levels"), d.ref(3)),
  "the same shape arriving higher each time. Call the film reference a disguised homage, never a direct quotation.")

d.add_statement(4, "Texture", "4 &middot; Layers you can count",
  "Two voices sound together over the full band. %s Count what is there: two vocal lines, sustained string and "
  "keyboard %s, and the rhythm section underneath. Musical theatre builds its textures the way pop does, by adding "
  "layers, and the number of layers is what changes across the song."
  % (d.ref(4), dfn("pads", "Sustained background chords, usually on strings or synthesiser, that fill out the harmony")),
  "how many separate parts you can pick out. Say the number and what each one is doing.")

d.add_statement(5, "Tonality", "5 &middot; Keys that lift",
  "The music steps up into a higher key for the last stretch. %s That is a %s, standard in musical theatre. What is "
  "not standard is that at least one of the shifts moves to a key a third away with a change of mode, a %s, which "
  "shares few chords with the old key and so sounds sudden and slightly magical."
  % (d.ref(5), dfn("step-up modulation", "Moving into a higher key to lift the intensity of a repeated section"),
     dfn("chromatic mediant", "A modulation to a key a third away, usually with a change of mode, giving a striking rather than smooth join")),
  "the whole texture sitting higher. Naming the chromatic mediant is the detail that lifts an answer.")

d.add_statement(6, "Dynamics", "6 &middot; Everything, at once",
  "This is the loudest and thickest point in the number. %s The full pit orchestra doubles the melody, the rock "
  "section drives underneath, and on stage a chorus is added. The soloist %s a sustained note above it all. Nothing "
  "here is marked gently: the volume is built by adding players and pushing the voice."
  % (d.ref(6), dfn("belts", "Sings powerfully in a chest-dominant tone high in the range, a contemporary musical-theatre technique")),
  "the scoring at its fullest under the highest note. Describe the build as a thickening of texture, not just as &lsquo;louder&rsquo;.")

d.add_checklist(
  "Melody: rising shapes with wide upward leaps, pentatonic colouring, and a recurring motif extended by sequence. "
  "Harmony and tonality: minor-tinged uncertainty at the start, step-up modulations including a chromatic mediant, "
  "ending firmly in D flat major. Texture: sparse chords, then held vocal notes over a driving quaver ostinato, then "
  "two voices with full band. Rhythm: free speech rhythm becoming continuous quavers. Orchestration: pit orchestra "
  "with rock rhythm section, thickening throughout. Dynamics: built by adding layers, to a belted climax.",
  "Attach each term to a moment. &ldquo;It uses sequence&rdquo; earns little; &ldquo;the rising motif returns a step "
  "higher each time, so the tune seems to climb as the lyric describes flight&rdquo; earns the mark.")

content = d.content()
exam_tip = ("<p>Two answers lose marks here more than any other. The first is calling the film-song reference a "
            "quotation: Schwartz alters its rhythm and metric placement, so it is a disguised homage. The second is "
            "writing &lsquo;the key changes&rsquo; without naming the type: at least one shift is a chromatic "
            "mediant, a move to a key a third away with a change of mode, which is why it sounds abrupt rather than "
            "smooth.</p>")
conclusion = ("<p>You can now name each element of this number and point to where it is audible: driving quavers "
              "under held vocal notes, a rising hook with a wide leap, the recurring motif and its disguised homage, "
              "two voices layered over the band, step-up and chromatic mediant modulations, and a climax built by "
              "adding everything at once. Set it beside the Star Wars main title and the Stage and Screen area of "
              "study is complete.</p>")
description = ("Six numbered stops in Defying Gravity, one for each element: rhythm, melody, motif, texture, tonality "
               "and dynamics.")

flashcards = [
  {"q": "Who composed Defying Gravity and for which musical?", "a": "Stephen Schwartz, for Wicked (2003)."},
  {"q": "What melodic device makes the rising motif feel like it keeps ascending?",
   "a": "Sequence: the same rising shape is repeated at progressively higher pitch levels."},
  {"q": "What earlier film song does the Unlimited motif echo, and how is the reference disguised?",
   "a": "The rainbow song from The Wizard of Oz. Schwartz keeps the interval shape but alters the rhythm and metric placement, so it is a disguised homage rather than a direct quotation."},
  {"q": "What is distinctive about at least one of the song's key changes?",
   "a": "It is a chromatic mediant modulation, moving to a key a third away with a change of mode rather than to a closely related key, so the join sounds sudden."},
  {"q": "What scale colours some of the melodic phrases, and what does it add?",
   "a": "The pentatonic scale, a five-note scale with no semitone steps. It gives an open, unforced sound above harmony that is more chromatic underneath."},
  {"q": "How does the orchestration change from the opening to the coda?",
   "a": "It thickens from minimal scoring supporting the voice to a full pit orchestra, rock rhythm section and, on stage, chorus voices at maximum dynamic."},
]

practice = [
  {"text": "Identify the term for the free, speech-like vocal section that opens Defying Gravity.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for recitative or recitative-style."},
  {"text": "Describe the melodic device used when the rising motif returns at a higher pitch each time it appears.", "marks": 2, "kind": "Description",
   "mark_scheme": "One mark for sequence. One mark for the detail that each repetition arrives at a higher pitch level, creating a sense of ascent."},
  {"text": "Explain how the modulation scheme in Defying Gravity contributes to the song's dramatic build.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: the key steps up more than once. One mark: at least one shift is a chromatic mediant, to a key a third away with a change of mode. One mark: each lift raises the tension and matches the growing defiance in the words."},
  {"text": "Name the scale type used to give some melodic phrases an open, simple quality.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for pentatonic."},
  {"text": "Describe the relationship between the vocal line and the accompaniment texture in the final section of the song.", "marks": 2, "kind": "Description",
   "mark_scheme": "One mark: sustained, held vocal notes. One mark: a continuous quaver or ostinato accompaniment underneath, so a still vocal line sits over a busy band."},
  {"text": "Explain how orchestration changes across the song support its dramatic structure, referring to specific sections.", "marks": 4, "kind": "Explanation",
   "mark_scheme": "One mark: the recitative-like opening uses only sparse sustained chords. One mark: the rhythm section and orchestra join as the song proper begins. One mark: the final section adds full pit orchestra and, on stage, chorus voices. One mark: the steady thickening of texture carries the dramatic build towards the climax."},
]

kcs = [
  {"q": "What term describes the free, speech-rhythm vocal section at the song's opening?",
   "options": ["Recitative", "Rondo", "Cadenza", "Ostinato"], "correct": 0},
  {"q": "What kind of scale gives some melodic phrases their open, uncomplicated sound?",
   "options": ["Chromatic", "Whole-tone", "Pentatonic", "Octatonic"], "correct": 2},
  {"q": "What is a chromatic mediant modulation?",
   "options": ["A move to a key a third away with a mode change", "A move to the dominant key", "A return to the tonic", "A move by a semitone only"], "correct": 0},
  {"q": "What texture is heard between the vocal line and accompaniment in the song's climax?",
   "options": ["Held vocal notes over a driving quaver ostinato", "Two equal melodic lines in canon", "Unaccompanied solo voice", "Call and response between two singers"], "correct": 0},
  {"q": "How is the reference to the earlier film song treated in the Unlimited motif?",
   "options": ["It is quoted note for note", "The interval shape is kept but the rhythm and metric placement are altered", "It is played backwards", "It appears only in the orchestra"], "correct": 1},
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
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", "defyinggravity_l3.html"), "w",
        encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
