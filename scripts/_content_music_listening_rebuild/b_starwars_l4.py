# -*- coding: utf-8 -*-
"""music-edexcel / aos3-stage-and-screen / L4 -- Star Wars Main Title, STRUCTURAL walk.
Video 54hoKbTWon4 (John Williams and the Wiener Philharmoniker, Deutsche
Grammophon, live), 6:42 = 402 s. The music ends at 6:14 and applause follows.
Pin times: 0:01 fanfare (3/3), 0:08 main theme (2/3 in the first round and again
in the targeted round), 0:52 the lyrical string theme (0:52 and 0:53 in the
targeted round plus 0:52 in the first round), 1:52 the main theme returns (3/3
in the targeted round), 3:30 the loud title music gives way to quiet music (3/3,
and all three votes described the music after it as quieter film music), 6:14
the last chord (3/3). DROPPED: a separate 'C section' pin, votes 1:14 / 0:43 /
1:49, split; and the 3:18 climax pin, which sits only 12 s before pin 5."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck import Deck, dfn, patch, build_questions, check_plain

BACKUP = "music-edexcel__aos3-stage-and-screen__L04"
d = Deck(lesson_id="a8ec22eb-8db7-4692-8fc2-02803b7c4682",
         subject="music-edexcel", unit="aos3-stage-and-screen", lesson_no=4,
         yt="54hoKbTWon4", dur=402, track_label="Star Wars Main Title",
         credit="John Williams and the Wiener Philharmoniker, streamed from YouTube (Deutsche Grammophon) &mdash; "
                "not hosted by StudyVault. Williams: Main Title from Star Wars Episode IV. Applause follows the "
                "last chord.")
TITLE = "Williams: Main Title from Star Wars — Guided Listening"

d.pins = [
    ("t1c1", 1,   "Fanfare",      "Brass hurl out rising fourths and fifths with triplet upbeats. An announcement, not a tune."),
    ("t1c2", 8,   "Main theme",   "The heroic A theme: triadic, wide-leaping, carried by horns and trumpets."),
    ("t1c3", 52,  "B section",    "Strings take a gentler, smoother idea. The vastness of space rather than the charge."),
    ("t1c4", 112, "A returns",    "The main theme comes back in the brass, restating the heroic idea."),
    ("t1c5", 210, "Into the film", "The crawl ends. The loud title music gives way to quiet, and the underscore takes over."),
    ("t1c6", 374, "Last chord",   "The chase music reaches its finish. Applause follows on this recording."),
]

d.add_cover(
  "Williams: Main Title from Star Wars",
  [
    "The opening cue of <em>Star Wars Episode IV: A New Hope</em> (1977), for %s in a bright B flat major. It has two "
    "connected halves: a concert-style opening of fanfare, main theme, contrasting idea and return, then %s for the "
    "chase between the rebel ship and the Imperial Star Destroyer."
    % (dfn("full symphony orchestra", "A large ensemble of strings, woodwind, brass and percussion"),
       dfn("action underscore", "Instrumental music played beneath on-screen action to support the drama")),
    "In 1977 film scoring had drifted towards pop songs and electronics. George Lucas asked for something grand and "
    "melodic instead, and Williams answered with recurring themes for a full orchestra. The film recording was made "
    "by the London Symphony Orchestra; this performance is by the Vienna Philharmonic.",
    "Press play and the cards follow the music. Tap any number to jump to that moment.",
  ])

d.add_statement(1, "Fanfare", "1 &middot; The curtain-raiser",
  "Before any theme, a short brass gesture. %s Horns and trumpets leap upward through fourths and fifths, wide open "
  "intervals that project brightly, launched by %s upbeats. A %s is not a melody; its job is to seize attention and "
  "fix the key, and it does both within four seconds."
  % (d.ref(1), dfn("triplet", "Three equal notes played in the time normally taken by two"),
     dfn("fanfare", "A short, bold flourish, usually for brass, announcing something important")),
  "the direction of the leaps. Rising fourths and fifths, not steps: that is what makes it sound heroic.")

d.add_statement(2, "Main theme", "2 &middot; The A theme",
  "The fanfare runs straight into the theme everyone knows. %s Horns and trumpets stride upward through the notes of "
  "the chord, and this idea will return across the whole saga as a %s for heroism and the Rebellion, a technique "
  "Wagner developed in opera and film composers borrowed wholesale."
  % (d.ref(2), dfn("leitmotif", "A recurring musical theme tied to a character, place or idea")),
  "how the tune climbs. The theme is the film's engine, not just its title music.")

d.add_statement(3, "B section", "3 &middot; The contrast",
  "The texture changes and the strings take over with a gentler idea. %s It moves by smaller intervals, at a softer "
  "dynamic and a slower pace, so it gives the ear a rest from fanfare energy. In the film this is the crawl still "
  "moving away into deep space: scale and mystery rather than action."
  % d.ref(3),
  "strings replacing brass. Naming the family that carries each theme is the quickest structure mark in this cue.")

d.add_statement(4, "A returns", "4 &middot; The theme comes back",
  "The brass reclaim the main theme. %s That gives the opening half a clear shape &mdash; fanfare, A, B, A &mdash; "
  "which is why this part of the cue works as concert music as well as film music. What follows is not a repeat but "
  "a %s: the music will change function rather than stop."
  % (d.ref(4), dfn("transition", "A passage that leads from one section to the next, usually changing key or character")),
  "the return of a theme you already know, in the instruments that first played it.")

d.add_statement(5, "Into the film", "5 &middot; The music changes job",
  "The loud title music falls away and something quiet and uneasy takes its place. %s The crawl has finished and the "
  "camera has found the planet. The music does not stop and restart: tension builds in the strings with brass "
  "interjections until the chase is under way and the cue has become %s."
  % (d.ref(5), dfn("underscore", "Music played beneath action or dialogue rather than as the focus of attention")),
  "the join. Recognising where concert music becomes underscore is exactly the structural detail examiners reward.")

d.add_statement(6, "Last chord", "6 &middot; The finish",
  "The chase music drives to its close. %s Across the whole cue Williams has done three jobs at once: set the heroic "
  "tone of the saga, introduce a theme that will return for hours of film, and glue the written crawl to the first "
  "on-screen action. On this recording the audience answers immediately."
  % d.ref(6),
  "how far the music has travelled from the opening fanfare without ever leaving its key for long.")

d.add_checklist(
  "Genre: symphonic film score, main title cue. Forces: full symphony orchestra, brass-led. Key: B flat major. "
  "Metre and tempo: firm regular metre with a march-like drive. Structure: fanfare, A theme, lyrical B section, "
  "return of A, transition, action underscore. Texture: mostly homophonic, melody doubled in octaves over "
  "accompaniment. Harmony: functional and major, with quartal touches. Context: 1977, written at George Lucas's "
  "request in a style reviving Korngold's Hollywood scoring and Holst's orchestral power, using Wagner's leitmotif "
  "technique.",
  "Say which family plays what, and where. &ldquo;It uses a fanfare&rdquo; earns little; &ldquo;horns and trumpets "
  "open with rising fourths and fifths before the strings take the contrasting theme&rdquo; earns the mark.")

content = d.content()
exam_tip = ("<p>Answer with the pattern feature, cause, effect. Do not write &lsquo;it uses a fanfare&rsquo;; write "
            "that the rising fourths and fifths sit high in the natural range of horns and trumpets, so the sound "
            "projects brightly and reads instantly as heroism. Examiners reward the causal chain between the "
            "technical detail and its dramatic effect, not the label on its own.</p>")
conclusion = ("<p>You can now follow the cue from the brass fanfare, through the main theme, the lyrical string "
              "contrast and the return, to the moment the title music becomes action underscore and on to the final "
              "chord. The next lesson takes the same recording element by element &mdash; rhythm, melody, "
              "orchestration, harmony, dynamics and timbre.</p>")
description = ("Follow the Star Wars Main Title through six landmarks, from the brass fanfare to the moment the title "
               "music becomes action underscore.")

flashcards = [
  {"q": "In what year was Star Wars Episode IV released, and who wrote the score?",
   "a": "1977, with the score by John Williams. The film recording was made by the London Symphony Orchestra."},
  {"q": "What are the sections of the Main Title cue in order?",
   "a": "Brass fanfare, A theme (the main heroic theme), a lyrical B section for strings, a return of the A theme, then a transition into the action underscore for the blockade runner chase."},
  {"q": "What is a leitmotif, and how does Williams use one here?",
   "a": "A recurring musical theme tied to a character, place or idea, developed by Wagner in opera. The main theme returns across the whole saga to signal heroism and the Rebellion."},
  {"q": "Which two earlier composers shaped the style of this score?",
   "a": "Erich Wolfgang Korngold, whose lush 1930s and 1940s Hollywood scores established the symphonic film style, and Gustav Holst, whose driving rhythms and quintal harmony in The Planets influenced Williams's darker cues."},
  {"q": "In what key is the Main Title written, and why does that key suit it?",
   "a": "B flat major. It sits comfortably in the natural range of trumpets and horns, so the brass can play with a full, ringing, resonant tone."},
  {"q": "What happens to the music after the main theme returns?",
   "a": "It does not stop. The loud title music gives way to quiet, uneasy music as the crawl ends, then builds through string tension and brass interjections into the chase underscore."},
]

practice = [
  {"text": "Identify the key of the Star Wars Main Title.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for B flat major."},
  {"text": "Name the sections of the Main Title cue in the order you hear them.", "marks": 3, "kind": "Identification",
   "mark_scheme": "One mark: fanfare first, then the A theme. One mark: a contrasting lyrical B section, then the A theme returning. One mark: a transition into the action underscore for the blockade runner chase."},
  {"text": "Explain how the opening fanfare creates an impression of heroism.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: it rises through wide fourths and fifths. One mark: those intervals sit high in the natural range of horns and trumpets, so the sound projects brightly. One mark: triplet upbeats add forward energy, and the whole gesture announces the film before any image has registered."},
  {"text": "Explain what a leitmotif is and how Williams uses the technique in this score.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: a recurring theme attached to a character, place or idea. One mark: the technique was developed by Wagner in opera. One mark: the main theme returns throughout the film and the wider saga whenever heroism or the Rebellion is on screen, unifying hours of music."},
  {"text": "Describe how the music moves from concert-style title music into film underscore.", "marks": 3, "kind": "Description",
   "mark_scheme": "One mark: after the A theme returns, the loud title music falls away to a quiet, uneasy passage. One mark: tension builds in the strings with brass interjections. One mark: the cue does not stop and restart, so by the time the chase appears the music has already become agitated action underscore."},
  {"text": "Explain why Star Wars is described as reviving an older style of film scoring.", "marks": 4, "kind": "Explanation",
   "mark_scheme": "One mark: by 1977 mainstream scoring favoured pop songs, jazz and electronics. One mark: Lucas asked for grand, heroic, melodic music instead. One mark: Williams drew on Korngold's late-Romantic Hollywood style and Holst's driving orchestral writing. One mark: the full orchestra and Wagnerian leitmotif technique together restored the symphonic score as the blockbuster norm."},
]

kcs = [
  {"q": "What opens the Main Title cue before the A theme is heard?",
   "options": ["A lyrical string melody", "A brass fanfare", "A percussion solo", "A vocal introduction"], "correct": 1},
  {"q": "In which key is the Main Title written?",
   "options": ["C major", "B flat major", "D minor", "E flat minor"], "correct": 1},
  {"q": "Which instrumental family primarily carries the lyrical B section?",
   "options": ["Brass", "Woodwind", "Strings", "Percussion"], "correct": 2},
  {"q": "What is a leitmotif?",
   "options": ["A recurring theme tied to a character, place or idea", "A repeated bass pattern", "A brass flourish at the start of a piece", "A change of key at a climax"], "correct": 0},
  {"q": "What happens after the main theme returns for the second time?",
   "options": ["The cue ends immediately", "The music transitions into quiet, then agitated action underscore", "A vocal chorus enters", "The fanfare is repeated three more times"], "correct": 1},
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
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", "starwars_l4.html"), "w",
        encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
