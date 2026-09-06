# -*- coding: utf-8 -*-
"""music-edexcel / aos2-vocal-music / L3 -- Music for a While, ELEMENTS walk.
Same recording as L2 (sdSA0jcnBNo, 249 s). Pin times all 3/3 on the sung text,
and they fall in the order of the words, which is itself corroboration:
0:18 the voice enters, 0:58 'wond'ring', 1:33 'Alecto', 1:52 'eternal bands',
2:43 'the whip from out her hands', 4:00 the instruments close alone."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck import Deck, dfn, patch, build_questions, check_plain

BACKUP = "music-edexcel__aos2-vocal-music__L03"
d = Deck(lesson_id="4125240a-f774-4d0c-8f7e-b9aa510f9a75",
         subject="music-edexcel", unit="aos2-vocal-music", lesson_no=3,
         yt="sdSA0jcnBNo", dur=249, track_label="Music for a While",
         credit="Helen Watts, streamed from YouTube &mdash; not hosted by StudyVault. "
                "Purcell: Music for a While.")
TITLE = "Purcell: Music for a While — The Elements in Close-Up"

d.pins = [
    ("t1c1", 18,  "Texture",       "Two layers only: one voice, one continuo. Nothing can hide."),
    ("t1c2", 58,  "Phrasing",      "The vocal phrase ends part-way through a bass cycle. Listen for the joins that are not there."),
    ("t1c3", 93,  "Tonality",      "The same bass shape, at a new pitch level. The ground is not fixed in key."),
    ("t1c4", 112, "Melody",        "A single syllable stretched across many notes &mdash; a melisma on a word about endlessness."),
    ("t1c5", 163, "Harmony",       "Suspensions and notes from outside the key, at the darkest point of the text."),
    ("t1c6", 240, "Ornamentation", "The continuo alone. Everything decorative in the vocal line was the singer&rsquo;s choice."),
]

d.add_cover(
  "The same song, element by element",
  [
    "Purcell&rsquo;s theatre song of 1692: one voice over a %s, with the bass pattern repeating from the first bar to "
    "the last while the vocal line above changes. The %s realises chords from a figured bass over a cello or bass viol."
    % (dfn("ground bass", "A short bass pattern repeated continuously beneath changing music above; also called a basso ostinato"),
       dfn("continuo", "The Baroque accompanying group: a chordal instrument realising harmony over a bass instrument")),
    "The previous lesson followed the shape from the bare ground to the closing cycles. This one stops six times, "
    "once for each %s the exam sets questions on: texture, phrasing, tonality, melody, harmony and ornamentation."
    % dfn("element of music", "The building blocks of music: melody, harmony, tonality, texture, timbre, dynamics, rhythm, metre, tempo and structure"),
    "Press play and the cards follow the music. Tap any number to jump to that moment.",
  ])
d.add_statement(1, "Texture", "1 &middot; Two layers, nothing hidden",
  "One singer, one accompanying group. %s That is %s: a single melodic line over harmony. Because there are so few "
  "layers, every small gesture in the voice is exposed &mdash; a late entry, a leaning note, a rest. Occasionally the "
  "voice echoes a shape from the bass, which adds a brief %s."
  % (d.ref(1), dfn("melody-dominated homophony", "A texture with one clear melody supported by accompanying harmony"),
     dfn("imitative", "Repeating a melodic idea just after another part has played it")),
  "how little is sounding. Purcell chose that transparency so the word painting can be heard.")

d.add_statement(2, "Phrasing", "2 &middot; Phrases that do not fit",
  "The bass repeats in fixed lengths. The voice refuses to agree with it. %s A vocal phrase ends part-way through a "
  "bass cycle, so the joins between repetitions are covered over. That is %s, and naming it is the quickest way to "
  "show you have heard more than &lsquo;a bass that repeats&rsquo;."
  % (d.ref(2), dfn("phrase overlap", "A melodic phrase ending part-way through a repeating bass cycle, hiding the join")),
  "one bass cycle beginning while the singer is still in the middle of a line.")

d.add_statement(3, "Tonality", "3 &middot; A ground that moves",
  "The pattern in the bass has not changed, but its pitch level has. %s Purcell lifts the whole ground into a "
  "different key as the text turns to the Furies, so the harmony darkens without the bass ever stopping. The music "
  "%s and later works its way home."
  % (d.ref(3), dfn("modulates", "Changes key")),
  "the familiar bass shape sounding higher or lower than before. Say that the ground has changed key, not merely that the mood changes.")

d.add_statement(4, "Melody", "4 &middot; The line above",
  "The vocal writing is mostly %s, moving by step, which gives it its smooth, consoling quality, with occasional "
  "leaps saved for important words. %s Here a single syllable is spread over a run of notes: a %s, used for text "
  "about things that do not end."
  % (dfn("conjunct", "Moving by step, from one note to the next above or below"), d.ref(4),
     dfn("melisma", "Several notes sung on one syllable")),
  "the syllable that will not stop. Name it as a melisma and say which idea in the text it illustrates.")

d.add_statement(5, "Harmony", "5 &middot; Tension and release",
  "The bass is fixed, so Purcell&rsquo;s invention goes into the chords he builds above it. %s Listen for a %s: a "
  "note held over from the previous chord that clashes, then falls by step on to a note that fits. He also colours "
  "the harmony with %s notes at the darkest points of the text."
  % (d.ref(5), dfn("suspension", "A note held over from the previous chord, creating dissonance before resolving down by step"),
     dfn("chromatic", "Using notes from outside the prevailing key")),
  "the clash and its resolution, in that order. A suspension is heard as tension, then release.")

d.add_statement(6, "Ornamentation", "6 &middot; What the singer adds",
  "The voice has finished and the continuo plays the ground out. %s Look back over what the singer did to the line: "
  "%s and %s at cadences and phrase endings. Much of that was not written down. Baroque performers decorated by "
  "convention, so no two performances of this song are identical."
  % (d.ref(6), dfn("trills", "A rapid alternation between a note and the one above it"),
     dfn("appoggiaturas", "An expressive dissonant note that leans on the beat before resolving on to the main note")),
  "how much decoration falls at the ends of phrases. That placement is the convention, not an accident.")

d.add_checklist(
  "Melody: mostly conjunct with expressive leaps and melismas on significant words. Harmony: largely diatonic, "
  "with suspensions and chromatic colouring as the text darkens. Tonality: the ground itself shifts key part-way "
  "through. Texture: melody-dominated homophony, voice and continuo only, with brief imitation of bass shapes. "
  "Rhythm and phrasing: vocal phrases overlap the joins of the repeating bass. Ornamentation: trills and "
  "appoggiaturas at cadences, largely added by the performer.",
  "Every term needs a moment. &ldquo;There are suspensions&rdquo; earns little; &ldquo;a note is held over the "
  "changing bass, clashes, and falls by step on to the new chord&rdquo; earns the mark.")

content = d.content()
exam_tip = ("<p>Do not stop at &lsquo;the bass repeats&rsquo;. The higher marks come from what Purcell does with the "
            "repetition: vocal phrases end part-way through a cycle, so the joins are hidden; the whole ground is "
            "lifted into another key when the words turn dark; and the harmony above it is varied with suspensions "
            "and chromatic notes each time round. Name the device, then say what it does to the sound.</p>")
conclusion = ("<p>You can now describe each element of this song and point to where it is audible: a two-layer "
              "texture, phrases that overlap the bass cycles, a ground that changes key, a conjunct melody with "
              "melismas on significant words, suspensions resolving downwards, and performer-added ornaments at the "
              "cadences. Set it beside Killer Queen and you have the whole Vocal Music area of study in two "
              "contrasting styles.</p>")
description = ("Six numbered stops in Purcell's Music for a While, one for each element: texture, phrasing, tonality, "
               "melody, harmony and ornamentation.")

flashcards = [
  {"q": "What is the ground bass in Music for a While?",
   "a": "A short repeating bass phrase heard continuously throughout the piece, mostly conjunct with a descending shape at its opening."},
  {"q": "How does Purcell disguise the ground bass repetitions?",
   "a": "Through phrase overlap, where vocal phrases end part-way through a cycle, and through occasional rests, so the joins between repetitions are less obvious."},
  {"q": "Describe the vocal melody's character.",
   "a": "Mostly conjunct, moving by step, with occasional expressive leaps on important words and decorative melismas and ornaments."},
  {"q": "What is a suspension and how is it used here?",
   "a": "A note held over from the previous chord that creates dissonance before resolving downwards by step. Purcell uses suspensions to create expressive tension over the fixed bass."},
  {"q": "What happens to the key of the ground bass part-way through the song?",
   "a": "The whole pattern is lifted into a different key as the text turns to darker imagery, so the bass keeps its shape but changes pitch level."},
  {"q": "Which ornaments would a Baroque singer add to this song, and where?",
   "a": "Trills and appoggiaturas, mostly at cadences and phrase endings. Much of the decoration was added by the performer rather than written out, so performances differ."},
]

practice = [
  {"text": "Define the term 'ground bass' as used in Music for a While.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for a repeated bass pattern heard continuously throughout the piece."},
  {"text": "Describe the texture of Music for a While.", "marks": 2, "kind": "Description",
   "mark_scheme": "One mark: melody-dominated homophony. One mark: only two layers, a solo voice over continuo, with brief moments where the voice imitates a shape from the bass."},
  {"text": "Explain how Purcell disguises the repetitions of the ground bass in Music for a While.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: phrase overlap, with vocal phrases ending part-way through a cycle. One mark: rests and changes of texture interrupting the pattern. One mark: an explanation that these hide the joins so the repetition does not sound mechanical."},
  {"text": "Describe two features of the vocal melody in Music for a While.", "marks": 2, "kind": "Description",
   "mark_scheme": "One mark each, up to two, from: mostly conjunct or stepwise movement; occasional expressive leaps on important words; melismas; ornaments such as trills and appoggiaturas."},
  {"text": "Explain what is meant by a suspension and describe its effect in Music for a While.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: a note held over from the previous chord. One mark: it creates dissonance and then resolves downwards by step. One mark: the tension and release colour the harmony above a bass that never changes."},
  {"text": "Explain how Purcell varies the tonality of the piece despite using a fixed repeating bass.", "marks": 4, "kind": "Explanation",
   "mark_scheme": "One mark: the ground keeps its shape throughout. One mark: Purcell transposes the whole pattern into a different key part-way through. One mark: this happens as the text turns to darker imagery. One mark: chromatic notes and changing harmony above the bass add further colour before the music returns home."},
]

kcs = [
  {"q": "What is a ground bass?",
   "options": ["A repeated bass pattern heard throughout a piece", "A single bass note held at the end", "A bass line that only appears once", "A type of ornament in the melody"], "correct": 0},
  {"q": "Which technique does Purcell use to disguise the repetitions of the ground bass?",
   "options": ["Constant modulation", "Phrase overlap", "Removing the bass entirely", "Doubling the tempo"], "correct": 1},
  {"q": "What texture best describes the voice and continuo relationship in this piece?",
   "options": ["Polyphonic", "Melody-dominated homophony", "Monophonic", "Heterophonic"], "correct": 1},
  {"q": "What is a suspension in harmony?",
   "options": ["A note held over creating dissonance before resolving stepwise", "A sudden silence in the music", "A repeated rhythmic pattern", "A change of key"], "correct": 0},
  {"q": "Which ornaments would a Baroque singer typically add at cadences in this song?",
   "options": ["Glissandos and slides", "Trills and appoggiaturas", "Tremolo and pizzicato", "Vibrato only"], "correct": 1},
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
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", "purcell_l3.html"), "w",
        encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
