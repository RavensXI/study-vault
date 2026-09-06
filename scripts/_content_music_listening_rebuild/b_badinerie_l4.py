# -*- coding: utf-8 -*-
"""music-eduqas / aos1-forms-and-devices / L4 -- Badinerie, ELEMENTS walk.
Same recording as L3 (BsiqjGgwuU8, 101 s) and the same verified pin times, one
card per element: melody, texture, tonality, dynamics, and metre with timbre.
FACT FIXES carried into this deck: the A section ends in F sharp minor, the
DOMINANT minor, which is a closely related key because it differs from B minor
by one sharp -- it is NOT the relative major and does NOT share B minor's key
signature. The old practice question and knowledge check that said so are
replaced. The board is never named.
DROPPED pins: the flute's highest note (votes 0:48 / 0:15, split) and its
longest continuous run (0:45 / 0:53, split); both were judgement calls a
machine ear cannot settle."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck import Deck, dfn, patch, build_questions, check_plain

BACKUP = "music-eduqas__aos1-forms-and-devices__L04"
d = Deck(lesson_id="d9b004d2-4ae8-4f70-817b-7f99d9d89762",
         subject="music-eduqas", unit="aos1-forms-and-devices", lesson_no=4,
         yt="BsiqjGgwuU8", dur=101, track_label="Badinerie", board="eduqas",
         credit="Performance by the Netherlands Bach Society, streamed from YouTube &mdash; not hosted by "
                "StudyVault. Bach: Badinerie, Orchestral Suite No. 2 in B minor, BWV 1067. A title card runs "
                "before the music.")
TITLE = "Bach: Badinerie from Orchestral Suite No. 2 — The Elements in Close-Up"

d.pins = [
    ("t1c1", 7,  "Melody",   "Continuous semiquavers: scales, broken chords, and the same idea moved up or down."),
    ("t1c2", 22, "Texture",  "One line that matters and a supporting cast. Count the layers under the flute."),
    ("t1c3", 37, "Tonality", "Two related keys and the moves between them. Learn to name them, not just hear them."),
    ("t1c4", 61, "Dynamics", "Loud, then suddenly soft. No swelling anywhere in the movement."),
    ("t1c5", 84, "Timbre",   "A wooden flute, gut strings and a harpsichord filling in chords from a bass line."),
]

d.add_cover(
  "The same movement, element by element",
  [
    "Bach&rsquo;s closing movement of the Orchestral Suite No. 2 in B minor, BWV 1067: solo flute with strings and "
    "%s, in B minor, 2/4, fast, and cast in %s."
    % (dfn("continuo", "The continuous bass line and chords of Baroque music, usually cello with harpsichord"),
       dfn("binary form", "A two-part structure, A and B, each usually repeated, giving A A B B")),
    "The previous lesson followed the form from A to the final cadence. This one stops five times, once for each %s "
    "the exam sets questions on here: melody, texture, tonality, dynamics and tone colour."
    % dfn("element of music", "The building blocks of music: melody, harmony, tonality, texture, timbre, dynamics, rhythm, metre, tempo and structure"),
    "Press play and the cards follow the music. Tap any number to jump to that moment.",
  ])

d.add_statement(1, "Melody", "1 &middot; What the flute is made of",
  "Take the line apart and it is three things. %s Rising and falling scales; broken-chord patterns; and short ideas "
  "repeated immediately a step higher or lower, which is %s. All of it in unbroken semiquavers at speed, which is "
  "what makes the part %s and why players need double-tonguing and long breath control."
  % (d.ref(1), dfn("sequence", "A short idea repeated immediately at a higher or lower pitch"),
     dfn("virtuosic", "Written to demand exceptional technical skill")),
  "scale, arpeggio, sequence. Name which one you are hearing rather than calling the part &lsquo;fast&rsquo;.")

d.add_statement(2, "Texture", "2 &middot; One line that matters",
  "Underneath the flute, the strings are doing very little: sustained chords or simple quaver patterns. %s That is "
  "%s, one melody plus accompaniment, and it is deliberate, because the flute must never compete for attention. "
  "Occasionally the violins echo a fragment of the flute&rsquo;s idea, a brief touch of %s."
  % (d.ref(2), dfn("melody-dominated homophony", "A texture with one clear melody supported by accompanying harmony"),
     dfn("imitation", "One part copying material just played by another")),
  "how simple the accompaniment is. Then listen for the violins answering, which is the only counterpoint here.")

d.add_statement(3, "Tonality", "3 &middot; Two keys, and how they relate",
  "The movement uses two main key areas. %s It starts in B minor and the first half closes in F sharp minor, the "
  "%s: a closely related key, one sharp away, not the relative major. The second half sets off from there and "
  "touches D major, which is the %s, before coming home."
  % (d.ref(3), dfn("dominant minor", "The minor key built on the fifth degree of the scale: F sharp minor in B minor"),
     dfn("relative major", "The major key sharing a key signature with a minor key: D major for B minor")),
  "the change of colour at the halfway cadence. Name F sharp minor as the dominant minor and you have the mark.")

d.add_statement(4, "Dynamics", "4 &middot; Steps, not slopes",
  "Volume here changes in blocks. %s A phrase is played loudly and then repeated softly, an echo effect, because "
  "Baroque instruments could not swell gradually the way a modern piano can. That is %s, and it is the only dynamic "
  "device the movement uses."
  % (d.ref(4), dfn("terraced dynamics", "Sudden shifts between loud and soft, without gradual crescendo or diminuendo")),
  "an immediate quiet answer to a loud phrase. If you hear no crescendo at all, that is the correct observation.")

d.add_statement(5, "Timbre", "5 &middot; The sound of the period",
  "This is a period-instrument performance, so the colours are not modern ones. %s The soloist plays a %s, a wooden "
  "flute with a softer, breathier tone than a metal one. Beneath it, the harpsichord %s: it improvises chords from "
  "the written bass line rather than reading them out."
  % (d.ref(5), dfn("traverso", "The Baroque transverse flute, held sideways and blown across a hole"),
     dfn("realises the figured bass", "Improvises chords above a written bass line according to Baroque convention")),
  "the woody flute tone and the plucked harpsichord underneath. Name the continuo instruments, not just &lsquo;the accompaniment&rsquo;.")

d.add_checklist(
  "Melody: continuous semiquavers built from scales, arpeggio figures and sequences, virtuosic throughout. Harmony "
  "and tonality: B minor to F sharp minor, the dominant minor, across A, then through related keys including D major "
  "back to B minor. Texture: melody-dominated homophony with occasional imitation from the violins. Rhythm, metre "
  "and tempo: 2/4, fast, with almost no rests in the solo line. Dynamics: terraced, with echo effects. Timbre: "
  "Baroque transverse flute, strings, and continuo of cello with harpsichord realising the figured bass.",
  "Attach each term to a moment. &ldquo;It uses sequence&rdquo; earns little; &ldquo;the flute repeats a "
  "broken-chord figure a step lower each time, driving the harmony forward&rdquo; earns the mark.")

content = d.content()
exam_tip = ("<p>One key relationship is worth getting exactly right. F sharp minor is the dominant minor of B minor, "
            "the key built on the fifth degree, and the two are closely related because they differ by a single "
            "sharp. It is not the relative major and it does not share B minor's key signature. D major is the "
            "relative major, and it is touched during the second half, not at the end of the first.</p>")
conclusion = ("<p>You can now name each element of this movement and point to where it is audible: scales, arpeggios "
              "and sequences in unbroken semiquavers, a melody-dominated texture with brief imitation, a move from B "
              "minor to F sharp minor and back through D major, terraced dynamics with echo effects, and the woody "
              "tone of a Baroque flute over a realised continuo.</p>")
description = ("Five numbered stops in Bach's Badinerie, one for each element: melody, texture, tonality, dynamics "
               "and tone colour.")

flashcards = [
  {"q": "What binary form pattern does the Badinerie follow?", "a": "A A B B, with the A and B sections each repeated."},
  {"q": "What key relationship links the tonic and the key reached at the end of the A section?",
   "a": "B minor is the tonic and the A section ends in F sharp minor, its dominant minor, the key built on the fifth degree. The two are closely related, differing by one sharp."},
  {"q": "What is terraced dynamics?",
   "a": "Sudden shifts between loud and soft, often making an echo effect, used because Baroque instruments could not produce smooth crescendos."},
  {"q": "What makes the flute writing in the Badinerie virtuosic?",
   "a": "Continuous fast semiquaver runs, scalic and arpeggio patterns and sequences, with demands on breath control and on fast articulation such as double-tonguing."},
  {"q": "What is the role of the continuo in the Badinerie?",
   "a": "The cello, sometimes with double bass, plays the bass line while the harpsichord realises chords above it, giving harmonic and rhythmic support beneath the flute."},
  {"q": "Which major key is touched during the B section, and what is it called in relation to B minor?",
   "a": "D major, the relative major, which shares B minor's key signature of two sharps."},
]

practice = [
  {"text": "Name the overall structure of the Badinerie.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for binary form. Accept A A B B."},
  {"text": "State the tonic key and the key reached by the end of the A section.", "marks": 2, "kind": "Identification",
   "mark_scheme": "One mark for B minor as the tonic. One mark for F sharp minor, the dominant minor, at the end of the A section."},
  {"text": "Explain why F sharp minor counts as a closely related key to B minor.", "marks": 2, "kind": "Explanation",
   "mark_scheme": "One mark: it is the dominant minor, built on the fifth degree of the B minor scale. One mark: its key signature differs from B minor's by only one sharp, so the two share most of their notes and the move sounds smooth. Do not credit any answer calling it the relative major."},
  {"text": "Describe the dynamic technique used in the Badinerie and explain why Baroque composers relied on it.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: terraced dynamics. One mark: sudden loud and soft contrast, often an echo effect where a phrase is repeated quietly. One mark: Baroque instruments, especially the harpsichord, could not produce a gradual crescendo or diminuendo."},
  {"text": "Identify two features of the flute writing that make it virtuosic.", "marks": 2, "kind": "Identification",
   "mark_scheme": "One mark each, up to two, from: continuous semiquaver runs; scalic or arpeggio patterns; sequences; wide leaps; the breath control required; the fast articulation or double-tonguing required."},
  {"text": "Explain the role of the continuo in the Badinerie and how it differs from the flute's role.", "marks": 4, "kind": "Explanation",
   "mark_scheme": "One mark: the continuo is harpsichord with cello, sometimes with double bass. One mark: it supplies the bass line and the harmony, with the harpsichord realising chords from the written bass. One mark: the flute carries a virtuosic melodic line throughout. One mark: the result is a melody-dominated homophonic texture in which the accompaniment never competes with the soloist."},
]

kcs = [
  {"q": "What is the tonic key of the Badinerie?",
   "options": ["D major", "B minor", "F sharp minor", "G major"], "correct": 1},
  {"q": "Which key does the A section reach by its close, and what is its relationship to the tonic?",
   "options": ["D major, the relative major", "F sharp minor, the dominant minor", "E minor, the subdominant minor", "B major, the tonic major"], "correct": 1},
  {"q": "Which term describes a short musical idea repeated immediately at a different pitch?",
   "options": ["Ostinato", "Sequence", "Cadenza", "Ornamentation"], "correct": 1},
  {"q": "Which best describes the dynamics typically used in the Badinerie?",
   "options": ["Gradual crescendo and diminuendo throughout", "Terraced dynamics with sudden loud and soft contrasts", "Constant fortissimo", "No dynamic contrast at all"], "correct": 1},
  {"q": "Which instruments typically make up the continuo in this piece?",
   "options": ["Flute and violin", "Harpsichord and cello or bass", "Oboe and viola", "Trumpet and timpani"], "correct": 1},
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
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", "badinerie_l4.html"), "w",
        encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
