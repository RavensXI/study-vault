# -*- coding: utf-8 -*-
"""music-edexcel / aos2-vocal-music / L2 -- Music for a While, STRUCTURAL walk.
Video sdSA0jcnBNo (Helen Watts), 4:09 = 249 s.
Pin times: 0 ground alone (3/3), 0:18 the voice enters (3/3), 1:33 'Alecto'
(3/3), 2:22 'drop, drop, drop' (3/3), 2:57 the opening words return (3/3),
4:00 the instruments close alone (2/3). The word-cue times run in the order of
the text, which is itself a check that they are right. The last chord (4:03,
2/3) is not pinned: it is three seconds after pin 6."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck import Deck, dfn, patch, build_questions, check_plain

BACKUP = "music-edexcel__aos2-vocal-music__L02"
d = Deck(lesson_id="4628e962-5fbc-4ac0-bc42-d87bfe3fa18b",
         subject="music-edexcel", unit="aos2-vocal-music", lesson_no=2,
         yt="sdSA0jcnBNo", dur=249, track_label="Music for a While",
         credit="Helen Watts, streamed from YouTube &mdash; not hosted by StudyVault. "
                "Purcell: Music for a While.")
TITLE = "Purcell: Music for a While — Guided Listening"

d.pins = [
    ("t1c1", 0,   "The ground alone", "The repeating bass is laid out bare. Learn its shape now and you can track it under everything."),
    ("t1c2", 18,  "The voice enters", "The singer arrives over the ground, and the phrases do not line up with it."),
    ("t1c3", 93,  "The text darkens", "The Furies are named. From here the mood and the harmony tighten."),
    ("t1c4", 142, "Word painting",    "The falling, repeated figure on &lsquo;drop&rsquo; &mdash; the most famous moment in the song."),
    ("t1c5", 177, "The opening returns", "The first words come back, varied rather than copied."),
    ("t1c6", 240, "The ground closes", "The voice has finished. The instruments play the pattern out and stop."),
]

d.add_cover(
  "Purcell: Music for a While",
  [
    "A theatre song of 1692 for solo voice and %s, built over a %s: a short bass pattern repeated from the first bar "
    "to the last. Broadly a %s shape sits on top of that unbroken bass, so two structures run at once."
    % (dfn("basso continuo", "The Baroque accompanying group: a chordal instrument realising harmony over a bass instrument"),
       dfn("ground bass", "A short bass pattern repeated continuously beneath changing music above; also called a basso ostinato"),
       dfn("ternary", "Three-part form, A B A, where the opening returns after a contrasting middle")),
    "Purcell wrote it as %s for a revival of Dryden and Lee&rsquo;s tragedy <em>Oedipus</em>. In the play the song is "
    "sung to raise the spirit of a murdered king, so it has to be beautiful and slightly uncanny at the same time."
    % dfn("incidental music", "Music written to accompany a spoken play, used during or between scenes"),
    "Press play and the cards follow the music. Tap any number to jump to that moment.",
  ])

d.add_statement(1, "The ground alone", "1 &middot; The pattern, on its own",
  "Purcell gives you the ground bass before anything else, unaccompanied by any voice. %s It is a short phrase, "
  "mostly moving by step with a falling shape at its start, and it will now repeat without a break until the song "
  "ends. The %s realises chords above it from a figured bass."
  % (d.ref(1), dfn("continuo", "The accompanying bass line and the chords built on it, played by harpsichord or organ with cello or bass viol")),
  "the shape of the bass. Everything that follows is measured against this one pattern.")

d.add_statement(2, "The voice enters", "2 &middot; Voice over ground",
  "The singer comes in and the texture becomes two layers: one melody over accompanying harmony, which is %s. %s "
  "Notice at once that the vocal phrases do not stop where the bass pattern stops. That deliberate mismatch is called "
  "%s, and it is what stops strict repetition sounding mechanical."
  % (dfn("melody-dominated homophony", "A texture with one clear melody supported by accompanying harmony"), d.ref(2),
     dfn("phrase overlap", "A vocal phrase ending part-way through a repeating bass cycle, hiding the join")),
  "the joins. Try to hear where each bass cycle restarts, and how rarely the voice restarts with it.")

d.add_statement(3, "The text darkens", "3 &middot; The Furies arrive",
  "The words turn from easing pain to Alecto and the dead. %s Purcell answers by letting the ground move out of its "
  "home key for a while, so the fixed pattern is not as fixed as it seemed, and by colouring the harmony with notes "
  "from outside the key. The %s does not change; its key does."
  % (d.ref(3), dfn("ground", "The repeating bass pattern itself")),
  "the same bass shape sounding at a new pitch level. That is the moment to say the ground has changed key.")

d.add_statement(4, "Word painting", "4 &middot; Drop, drop, drop",
  "This is the passage everyone quotes. %s On the word describing the snakes falling, Purcell writes a repeated, "
  "falling figure so that the music does what the word says. That is %s, and it is the single clearest example in the "
  "set work. Elsewhere he uses long %s for words about endlessness."
  % (d.ref(4), dfn("word painting", "Shaping the music so that it reflects the meaning of the words"),
     dfn("melismas", "Several notes sung on a single syllable")),
  "the repeated descent. Name the device and the word together, and say what the effect is.")

d.add_statement(5, "The opening returns", "5 &middot; Back to the beginning",
  "The first words come back and the song rounds itself off. %s This is the return that makes the shape ternary, but "
  "it is not a copy: Purcell varies the vocal line, which is why it is labelled %s rather than a second A. The ground "
  "has been running underneath the whole time, unbroken."
  % (d.ref(5), dfn("A prime", "A returning section that is varied rather than repeated exactly, written A&prime;")),
  "the tune you know, decorated differently. Say &lsquo;varied return&rsquo;, not &lsquo;repeat&rsquo;.")

d.add_statement(6, "The ground closes", "6 &middot; The last cycles",
  "The voice stops and the instruments are left with the pattern. %s Purcell ends the way he began, which frames the "
  "whole song in the ground bass, and the last statements settle on to a closing %s. The stillness is the point: "
  "nothing has changed underneath from first bar to last."
  % (d.ref(6), dfn("cadence", "The chord progression that closes a musical phrase or piece")),
  "the same bass you heard before the singer entered. That symmetry is worth naming in an answer.")

d.add_checklist(
  "Genre: Baroque theatre song, incidental music. Forces: solo voice with basso continuo, a chordal instrument "
  "realising harmony over a bass instrument. Structure: a continuous ground bass beneath a broadly ternary vocal "
  "shape, A B A prime, framed by instrumental statements of the ground. Texture: melody-dominated homophony, two "
  "layers, with phrase overlap disguising the joins. Harmony: mostly diatonic, with suspensions and chromatic "
  "colouring as the text darkens, and one shift of key in the ground. Context: 1692, for a revival of Dryden and "
  "Lee's Oedipus.",
  "Tie the label to the moment. &ldquo;There is a ground bass&rdquo; earns little; &ldquo;the ground is heard alone "
  "before the voice enters and again after it finishes, framing the song&rdquo; earns the mark.")

content = d.content()
exam_tip = ("<p>When a question asks about the ground bass, never stop at the fact that it repeats. Say what Purcell "
            "does with it: he hides the joins by letting vocal phrases end part-way through a cycle, and he shifts "
            "the pattern into another key when the text darkens. Structural detail linked to expressive purpose is "
            "what separates the top band from the middle.</p>")
conclusion = ("<p>You can now follow the song from the bare ground bass, through the entry of the voice, the turn "
              "towards the Furies, the falling figure on the word about dropping, the varied return of the opening "
              "and the closing instrumental cycles. The next lesson takes the same recording apart element by "
              "element &mdash; texture, phrasing, tonality, melody, harmony and ornamentation.</p>")
description = ("Follow Purcell's Music for a While through six landmarks, from the bare ground bass to the closing "
               "instrumental cycles.")

flashcards = [
  {"q": "What is a ground bass?",
   "a": "A short bass pattern that repeats continuously beneath the music, giving a fixed harmonic framework while the melody above develops freely. It is also called a basso ostinato."},
  {"q": "What forces accompany the voice in Music for a While?",
   "a": "Basso continuo: a chordal instrument such as harpsichord or organ realising the harmony, alongside a bass instrument such as cello or bass viol."},
  {"q": "For what occasion was Music for a While written?",
   "a": "As incidental music in 1692 for a revival of Dryden and Lee's tragedy Oedipus, where it is sung to raise the spirit of a murdered king."},
  {"q": "What is word painting, and what is the clearest example in this song?",
   "a": "Shaping the music to reflect the meaning of the words. The clearest example is the repeated falling figure on the word describing the snakes dropping."},
  {"q": "What happens to the ground bass later in Music for a While?",
   "a": "It briefly shifts into a different key to intensify the mood as the text turns to darker, more unsettling imagery."},
  {"q": "How does Purcell frame the song structurally?",
   "a": "The ground bass is played by the instruments alone before the voice enters and again after the voice has finished, so the song opens and closes with the same pattern."},
]

practice = [
  {"text": "Identify the term used to describe a short, continuously repeating bass-line pattern such as the one found in Music for a While.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for ground bass or basso ostinato."},
  {"text": "State the instrumentation typically used to accompany the voice in Music for a While.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for basso continuo, for example harpsichord or organ with cello or bass viol."},
  {"text": "Explain how Purcell uses falling melodic movement as word painting in Music for a While.", "marks": 2, "kind": "Explanation",
   "mark_scheme": "One mark: descending, often repeated, stepwise movement. One mark: it matches the meaning of the words, most obviously on the word describing the snakes dropping."},
  {"text": "Describe the relationship between the ground bass and the vocal line in this piece.", "marks": 2, "kind": "Description",
   "mark_scheme": "One mark: the bass repeats fixed material continuously. One mark: the voice develops freely above it, with phrases that end part-way through a cycle rather than aligning with it."},
  {"text": "Explain how Purcell frames the song with the ground bass, and why the return of the opening material is labelled A prime.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: the instruments state the ground alone before the voice enters and again after it stops. One mark: the opening words return near the end, giving a ternary shape. One mark: that return is varied rather than an exact repeat, so it is labelled A prime."},
  {"text": "Discuss how ornamentation and harmonic changes contribute to the dramatic effect of Music for a While.", "marks": 4, "kind": "Explanation",
   "mark_scheme": "One mark: named ornaments such as trills and appoggiaturas, mostly at cadences. One mark: increased chromatic colouring as the text turns to the Furies. One mark: the ground shifting into another key. One mark: an explanation that these intensify the supernatural, unsettling mood of the scene."},
]

kcs = [
  {"q": "Music for a While was originally written as incidental music for which play?",
   "options": ["Oedipus", "The Tempest", "King Arthur", "Dido and Aeneas"], "correct": 0},
  {"q": "What is a ground bass?",
   "options": ["A single loud bass note held throughout", "A short repeating bass pattern underpinning the harmony", "A bass line played only by the singer", "A bass drum rhythm"], "correct": 1},
  {"q": "What is heard first in the song, before anything else?",
   "options": ["The voice alone", "The ground bass played by the instruments alone", "A full instrumental overture", "A drum roll"], "correct": 1},
  {"q": "What overall shape does the vocal part follow above the continuous ground?",
   "options": ["Strophic form", "Ternary form, A B A prime", "Twelve-bar blues", "Sonata form"], "correct": 1},
  {"q": "A long, flowing run of notes sung on one syllable is called a...",
   "options": ["Trill", "Appoggiatura", "Melisma", "Cadence"], "correct": 2},
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
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", "purcell_l2.html"), "w",
        encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
