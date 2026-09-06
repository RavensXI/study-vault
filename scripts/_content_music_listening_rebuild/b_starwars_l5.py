# -*- coding: utf-8 -*-
"""music-edexcel / aos3-stage-and-screen / L5 -- Star Wars Main Title, ELEMENTS walk.
Same recording as L4 (54hoKbTWon4, 402 s), same verified pin times, one card per
element: rhythm and metre, melody, orchestration, harmony and tonality,
dynamics, and timbre in the action music."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck import Deck, dfn, patch, build_questions, check_plain

BACKUP = "music-edexcel__aos3-stage-and-screen__L05"
d = Deck(lesson_id="4e094f48-ac47-4a51-8c39-80c198ec4684",
         subject="music-edexcel", unit="aos3-stage-and-screen", lesson_no=5,
         yt="54hoKbTWon4", dur=402, track_label="Star Wars Main Title",
         credit="John Williams and the Wiener Philharmoniker, streamed from YouTube (Deutsche Grammophon) &mdash; "
                "not hosted by StudyVault. Williams: Main Title from Star Wars Episode IV. Applause follows the "
                "last chord.")
TITLE = "Williams: Main Title from Star Wars — The Elements in Close-Up"

d.pins = [
    ("t1c1", 1,   "Rhythm",        "Triplet upbeats and dotted rhythms. The cue marches before it sings."),
    ("t1c2", 8,   "Melody",        "Triadic shapes and a wide upward leap. A bugle call, not a song."),
    ("t1c3", 52,  "Orchestration", "Strings take over from brass. Same orchestra, different job."),
    ("t1c4", 112, "Harmony",       "Solid major triads, with the odd chord stacked in fourths for colour."),
    ("t1c5", 210, "Dynamics",      "The largest drop in the cue: full orchestra to almost nothing."),
    ("t1c6", 374, "Action timbre", "Tremolo strings, syncopated brass stabs, timpani. Tension made of tone colour."),
]

d.add_cover(
  "The same cue, element by element",
  [
    "John Williams&rsquo;s opening cue for <em>Star Wars Episode IV</em> (1977), for full symphony orchestra in B "
    "flat major: fanfare, main theme, lyrical contrast, return, then %s for the chase."
    % dfn("action underscore", "Instrumental music played beneath on-screen action to support the drama"),
    "The previous lesson followed the cue section by section. This one stops six times, once for each %s the exam "
    "sets questions on: rhythm and metre, melody, orchestration, harmony and tonality, dynamics and timbre."
    % dfn("element of music", "The building blocks of music: melody, harmony, tonality, texture, timbre, dynamics, rhythm, metre, tempo and structure"),
    "Press play and the cards follow the music. Tap any number to jump to that moment.",
  ])

d.add_statement(1, "Rhythm", "1 &middot; It marches",
  "Listen to the rhythm before you listen to the tune. %s Phrases are launched by %s upbeats, three quick notes "
  "springing into the strong beat, and the theme itself carries %s that give it a crisp, military edge. The metre is "
  "firm and regular, which is why the cue feels like advancing rather than dancing."
  % (d.ref(1), dfn("triplet", "Three equal notes played in the time normally taken by two"),
     dfn("dotted rhythms", "A long dotted note followed by a short one, giving a crisp, uneven feel")),
  "the three-note run into each phrase. Name it as a triplet upbeat, not just &lsquo;a fast bit&rsquo;.")

d.add_statement(2, "Melody", "2 &middot; Built from a chord",
  "The main theme does not wander by step; it outlines the notes of the chord, which makes it %s. %s There is a wide "
  "upward %s near the start of the phrase, so the tune reaches rather than creeps. The effect is close to a bugle "
  "call: confident, open and instantly memorable."
  % (dfn("triadic", "Built mainly from the notes of a chord rather than moving by step"), d.ref(2),
     dfn("leap", "Movement between notes that are not next to each other in the scale")),
  "the gaps between notes. Triadic outline plus a wide leap is the answer to almost any melody question here.")

d.add_statement(3, "Orchestration", "3 &middot; Who plays what",
  "The brass step back and the strings take the lyrical theme. %s That division of labour runs through the whole "
  "cue: brass carry fanfare and heroism, strings carry lyricism and later tension, and %s punctuates the structure. "
  "The same family will do a completely different job later on."
  % (d.ref(3), dfn("percussion", "Instruments struck or shaken, here mainly timpani, used to mark and reinforce key moments")),
  "which family has the tune. Naming the family and its dramatic role together is the fastest mark in this set work.")

d.add_statement(4, "Harmony", "4 &middot; Secure, with one strange colour",
  "The theme returns over harmony that leaves no doubt about the key: strong %s in a bright major. %s But Williams "
  "also slips in chords and fragments built from stacked fourths rather than thirds, which is %s. It sounds slightly "
  "modern and unsettled, hinting at scale and mystery without loosening the key."
  % (dfn("triads", "Three-note chords built from stacked thirds"), d.ref(4),
     dfn("quartal harmony", "Harmony built from chords stacked in fourths rather than thirds")),
  "a chord that sounds hollow rather than warm. Spotting and naming quartal harmony separates a strong answer from an average one.")

d.add_statement(5, "Dynamics", "5 &middot; The biggest drop",
  "The loudest and the quietest points of the cue are seconds apart. %s The full orchestra falls away to almost "
  "nothing as the crawl ends, and Williams then rebuilds from that silence rather than staying loud. Dynamics here "
  "are structural: the drop is what tells you the music has changed job."
  % d.ref(5),
  "how far the volume falls, and how quickly. Describe the contrast and what it signals, not just the loud part.")

d.add_statement(6, "Action timbre", "6 &middot; Tension made of tone colour",
  "By the close the same orchestra sounds nothing like the fanfare. %s Strings play %s and rapid figuration, brass "
  "throw in %s stabs off the beat, and timpani punch the accents. No new theme is needed: the tension is built "
  "entirely from tone colour, rhythm and register."
  % (d.ref(6), dfn("tremolo", "Very rapid repetition of a note, giving a shimmering, unsettled sound"),
     dfn("syncopated", "Accented off the main beat, against the expected pulse")),
  "short accented chords landing between the beats. That is the sound of the underscore, not of the title music.")

d.add_checklist(
  "Melody: triadic, with wide leaps and triplet upbeats; smoother and narrower in the B section. Harmony and "
  "tonality: confident B flat major with strong triadic harmony, coloured by quartal chords. Texture: mostly "
  "homophonic, with the melody doubled in octaves. Rhythm and metre: firm regular metre, march-like, with dotted "
  "rhythms and later syncopated stabs. Orchestration: brass for fanfare and heroism, strings for lyricism and "
  "tension, percussion for punctuation. Dynamics: extremes, including a sudden fall as the title music ends.",
  "Name the device, then what it does. &ldquo;Quartal harmony&rdquo; earns little; &ldquo;chords stacked in fourths "
  "give a hollow, modern colour that suggests the vastness of space&rdquo; earns the mark.")

content = d.content()
exam_tip = ("<p>Orchestration questions on this cue are quick marks if you learn one sentence: brass equals fanfare "
            "and heroism, strings equal lyricism and later tension, percussion equals punctuation. Then add where you "
            "heard it. The same rule applies to every element here &mdash; name the feature, name the instrument or "
            "moment, name the dramatic effect.</p>")
conclusion = ("<p>You can now name each element of the cue and point to where it is audible: triplet upbeats and "
              "dotted rhythms, a triadic theme with a wide leap, brass and strings trading roles, secure major "
              "harmony with quartal colouring, an enormous dynamic drop, and tension built from tremolo, stabs and "
              "timpani. That completes the Stage and Screen area of study alongside Defying Gravity.</p>")
description = ("Six numbered stops in the Star Wars Main Title, one for each element: rhythm, melody, orchestration, "
               "harmony, dynamics and timbre.")

flashcards = [
  {"q": "What two melodic features define the A theme of the Main Title?",
   "a": "A triadic shape, outlining the notes of a chord rather than moving by step, combined with wide leaps including a prominent upward leap."},
  {"q": "What rhythmic features give the main theme its march-like character?",
   "a": "Triplet upbeats launching the phrases, dotted rhythms within the theme, and a firm, regular metre."},
  {"q": "How does the B section contrast with the A theme?",
   "a": "It is lyrical and string-led, moving mostly by smaller intervals at a softer dynamic, against the brass-led, leaping, fanfare-like A theme."},
  {"q": "How does harmony in the Main Title balance stability and colour?",
   "a": "It is mostly a confident major key with simple triadic harmony, but includes quartal touches, chords built from stacked fourths, which add unusual colour without undermining the key."},
  {"q": "What rhythmic device creates the tension during the chase underscore?",
   "a": "Syncopated stabs: short accented chords placed off the main beat in the brass and lower strings, reinforced by timpani."},
  {"q": "Summarise how Williams divides the orchestra by dramatic role.",
   "a": "Brass carry the fanfares and heroic theme, strings carry the lyrical contrast and later the tremolo tension of the chase, and percussion punctuates key structural moments."},
]

practice = [
  {"text": "Identify the instrumental family that plays the opening fanfare of Main Title.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for brass, or for horns and trumpets."},
  {"text": "Describe the contrast between the A theme and the B section in Main Title.", "marks": 2, "kind": "Description",
   "mark_scheme": "One mark: the A theme is heroic, brass-led, triadic and leaping. One mark: the B section is lyrical, string-led, smoother and quieter, moving by smaller intervals."},
  {"text": "Explain how rhythm contributes to the march-like character of the main theme.", "marks": 2, "kind": "Explanation",
   "mark_scheme": "One mark: dotted rhythms and triplet upbeats give a crisp, springing feel. One mark: a firm, regular metre suggests marching or advancing, matching the heroic mood."},
  {"text": "Name and briefly explain one harmonic feature that adds unusual colour within the otherwise major-key tonality of Main Title.", "marks": 2, "kind": "Explanation",
   "mark_scheme": "One mark for quartal harmony, chords or fragments built from stacked fourths. One mark for the explanation that it adds a modern, hollow or unsettled colour without disturbing the overall tonal stability."},
  {"text": "Explain how dynamics are used structurally in this cue.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: the fanfare and theme are loud and full from the first bar. One mark: the volume falls away almost to nothing as the title music ends. One mark: Williams rebuilds from that silence, so the dynamic drop itself signals the change from title music to underscore."},
  {"text": "Discuss how orchestration is used to distinguish between the fanfare and theme material and the action underscore in Main Title.", "marks": 4, "kind": "Explanation",
   "mark_scheme": "One mark: brass dominate the fanfare and main theme. One mark: the underscore is driven by tremolo strings and rapid figuration. One mark: syncopated brass stabs and timpani punctuate the action. One mark: a clear link between each scoring choice and its dramatic function, heroism against tension and chase."},
]

kcs = [
  {"q": "What melodic feature best describes the main heroic theme?",
   "options": ["Stepwise and chromatic", "Triadic with wide leaps", "Entirely syncopated with no clear pitch centre", "Based on a twelve-note scale"], "correct": 1},
  {"q": "Which instrumental family primarily carries the lyrical B section?",
   "options": ["Brass", "Woodwind", "Strings", "Percussion"], "correct": 2},
  {"q": "What is meant by 'quartal harmony' in this cue?",
   "options": ["Harmony built from stacked thirds", "Harmony built from stacked fourths", "Harmony with no chords at all", "A four-bar repeating bass pattern"], "correct": 1},
  {"q": "What launches the phrases of the main theme, giving it forward energy?",
   "options": ["A drum roll", "Triplet upbeats", "A held pause", "A cymbal crash"], "correct": 1},
  {"q": "Which devices create tension in the action underscore?",
   "options": ["Tremolo strings and syncopated brass stabs", "A solo unaccompanied flute", "A repeated ground bass in the cellos", "Multitracked backing vocals"], "correct": 0},
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
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", "starwars_l5.html"), "w",
        encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
