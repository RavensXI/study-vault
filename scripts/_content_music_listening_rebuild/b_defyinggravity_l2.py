# -*- coding: utf-8 -*-
"""music-edexcel / aos3-stage-and-screen / L2 -- Defying Gravity, STRUCTURAL walk.
Video l0Bs_eaXaCo (Original Broadway Cast Recording lyric video), 5:52 = 352 s.
Pin times: 0:05 first sung line (3/3), 1:16 'Something has changed within me'
(3/3), 1:53 'defying gravity' first sung (3/3), 3:27 two voices heard together
(2/3), 4:32 the lift into a higher key (2/3), 5:28 the sustained high note near
the end (2/3). The track ends at 5:50 (3/3), which is not pinned.
The old lesson's embedded Over the Rainbow video is dropped."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck import Deck, dfn, patch, build_questions, check_plain

BACKUP = "music-edexcel__aos3-stage-and-screen__L02"
d = Deck(lesson_id="388a0415-c6c7-4792-ad25-5eab65e66f45",
         subject="music-edexcel", unit="aos3-stage-and-screen", lesson_no=2,
         yt="l0Bs_eaXaCo", dur=352, track_label="Defying Gravity",
         credit="Original Broadway cast recording, streamed from YouTube &mdash; not hosted by StudyVault. "
                "Schwartz: Defying Gravity (Wicked).")
TITLE = "Schwartz: Defying Gravity — Guided Listening"

d.pins = [
    ("t1c1", 5,   "Dialogue",       "Speech-rhythm lines over sparse chords. Theatre first, song second."),
    ("t1c2", 76,  "The song proper", "The vocal line settles into a real tune and the accompaniment starts to drive."),
    ("t1c3", 113, "The title idea",  "The hook arrives, and with it the leap on the key word."),
    ("t1c4", 207, "Two voices",      "Elphaba and Glinda together. The argument becomes music."),
    ("t1c5", 272, "The lift",        "The key steps up for the last stretch, and the texture thickens behind it."),
    ("t1c6", 328, "The climax",      "The highest, longest note in the number, over the fullest scoring."),
]

d.add_cover(
  "Schwartz: Defying Gravity",
  [
    "The %s of <em>Wicked</em>, the 2003 musical with music and lyrics by Stephen Schwartz, based on Gregory "
    "Maguire&rsquo;s novel. Voices of Elphaba and Glinda over a %s of strings, woodwind and brass combined with a "
    "rock rhythm section of electric guitar, bass, drum kit and keyboards."
    % (dfn("act one finale", "The big closing number before the interval, resolving a major plot decision on a high point"),
       dfn("pit orchestra", "The instrumental ensemble that plays below or beside the stage in a musical")),
    "Its dramatic job is fixed by its position: Elphaba decides to reject the Wizard&rsquo;s regime and accept being "
    "called wicked, and the music has to carry her from uncertainty to defiance in about five minutes, then send the "
    "audience into the interval.",
    "Press play and the cards follow the music. Tap any number to jump to that moment.",
  ])

d.add_statement(1, "Dialogue", "1 &middot; Not a song yet",
  "This does not begin like a song at all. %s The vocal lines follow the rhythm and rise and fall of speech over "
  "sparse, sustained chords, a style close to %s. There is no strong pulse and no repeating pattern, so your ear has "
  "nothing to hold on to. That is deliberate."
  % (d.ref(1), dfn("recitative", "A vocal style that follows the natural rhythm and inflection of speech rather than a formal tune")),
  "words winning over melody. Say &lsquo;recitative-like&rsquo; or &lsquo;speech-rhythm&rsquo;, not &lsquo;the singing is quiet&rsquo;.")

d.add_statement(2, "The song proper", "2 &middot; Melody takes over",
  "The lines lengthen, the phrases start to shape themselves, and underneath them the accompaniment settles into "
  "continuous quavers. %s After the free opening, that regular pulse arrives as a release. From here the number runs "
  "on a %s core, and each time round it is bigger than the last."
  % (d.ref(2), dfn("verse-chorus", "A song shape alternating verses, which change their words, with a returning chorus")),
  "the moment a pulse appears. The change from free to measured is one of the clearest structural signposts in the set work.")

d.add_statement(3, "The title idea", "3 &middot; The hook",
  "The title phrase is sung for the first time, and Schwartz sets it to a rising figure with an upward leap on the "
  "key word. %s In a stage number nothing is decorative: the tune climbs because the character is talking about "
  "flight. This is the material the whole rest of the song will keep transforming."
  % d.ref(3),
  "the shape of the phrase, not just the words. A wide upward leap here is a picture of what is being sung about.")

d.add_statement(4, "Two voices", "4 &middot; Two characters at once",
  "Until now the singers have taken turns. %s Here the two voices sound together, so the disagreement between them "
  "becomes audible as music rather than as dialogue. The %s writing is a reminder that this is a scene: the song is "
  "carrying a plot, not just a mood."
  % (d.ref(4), dfn("ensemble", "Writing for two or more voices singing at the same time")),
  "two independent lines at once. Say who is singing what, and what the combination tells you about the drama.")

d.add_statement(5, "The lift", "5 &middot; The key steps up",
  "The whole texture moves up a level. %s Schwartz raises the key more than once across the number, each rise "
  "arriving at a higher emotional stake, and the final statement lands in D flat major. The %s makes the listener "
  "feel a physical ascent, which is exactly what the words describe."
  % (d.ref(5), dfn("step-up modulation", "Moving the music into a higher key to lift the intensity of a repeated section")),
  "everything sitting higher than before. Name the device as a rising key change, and say why it fits the lyric.")

d.add_statement(6, "The climax", "6 &middot; The last note",
  "The final section abandons verses and choruses. %s Chorus material comes back transformed &mdash; higher, louder, "
  "doubled by the full pit orchestra and rock section, with a driving %s bass beneath &mdash; and the singer holds "
  "one sustained, belted note above it. The pitch never falls back before the end."
  % (d.ref(6), dfn("ostinato", "A short pattern repeated persistently, often in the bass, to drive a section forward")),
  "the texture at its thickest under the highest note. That combination is what makes this the most quoted extract in the song.")

d.add_checklist(
  "Genre: musical theatre act one finale, a power ballad. Forces: two solo voices with a pit orchestra of strings, "
  "woodwind and brass plus a rock rhythm section. Structure: recitative-like dialogue, then a verse-chorus core that "
  "intensifies each time, then a transformed final section and a sustained coda. Tonality: rising step-up "
  "modulations, ending in D flat major. Texture: sparse chords at the start, thickening to full orchestra and voices. "
  "Rhythm: free at first, then continuous driving quavers. Context: Wicked, 2003, music and lyrics by Stephen Schwartz.",
  "Every device here has a dramatic job. &ldquo;The key changes&rdquo; earns little; &ldquo;the key steps up before "
  "the final section so the whole texture rises with Elphaba&rsquo;s decision&rdquo; earns the mark.")

content = d.content()
exam_tip = ("<p>Because this is a stage number, link every feature to what it does for the drama. A wide upward leap "
            "is not just a wide interval, it is flight; a step-up modulation is not just a key change, it is growing "
            "resolve; the thickening orchestration is the scene filling up. Naming the device and then naming its "
            "dramatic effect is what separates the top band from the middle.</p>")
conclusion = ("<p>You can now follow the number from speech-like dialogue, through the arrival of a real tune and the "
              "title hook, to the two voices together, the key lift and the final sustained note over the fullest "
              "scoring. The next lesson takes the same recording element by element &mdash; melody, tonality, "
              "texture, rhythm, orchestration and dynamics.</p>")
description = ("Follow Defying Gravity through six landmarks, from speech-like dialogue to the belted final note in "
               "D flat major.")

flashcards = [
  {"q": "What is the dramatic function of Defying Gravity within Wicked?",
   "a": "It is the act one finale, resolving Elphaba's decision to embrace her power and closing the first half on a dramatic high point."},
  {"q": "Who wrote Defying Gravity, and when did Wicked open?",
   "a": "Stephen Schwartz wrote the music and lyrics. Wicked opened in 2003, based on Gregory Maguire's novel."},
  {"q": "What vocal style opens the song before the melody develops?",
   "a": "A dialogue-like, recitative-style exchange between Elphaba and Glinda with sparse sustained chords and no strong pulse."},
  {"q": "Describe the sections of Defying Gravity in order.",
   "a": "A free recitative-like opening, a verse-chorus core that intensifies with each repeat, a transformed final section, and a sustained climactic coda."},
  {"q": "How does the key scheme develop across the song?",
   "a": "It rises through step-up modulations, each at a higher emotional stake, before settling in D flat major for the final climactic statement."},
  {"q": "What two instrumental traditions are blended in the orchestration?",
   "a": "A traditional pit orchestra of strings, woodwind and brass, combined with a rock rhythm section of electric guitar, bass, drum kit and keyboard or synthesiser."},
]

practice = [
  {"text": "Identify the vocal style used at the very opening of Defying Gravity.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for recitative-like, speech-rhythm or dialogue-like writing."},
  {"text": "Explain the dramatic function of Defying Gravity within Wicked.", "marks": 2, "kind": "Explanation",
   "mark_scheme": "One mark: it is the act one finale. One mark: it resolves Elphaba's decision to reject the Wizard and sends the audience into the interval on a high point."},
  {"text": "Describe how the song moves from its dialogue-like opening into full song.", "marks": 3, "kind": "Description",
   "mark_scheme": "One mark: the opening has free speech-rhythm lines over sparse sustained chords with no strong pulse. One mark: the vocal lines become longer and more shaped. One mark: a continuous quaver accompaniment establishes a pulse, and the number settles into a verse-chorus core."},
  {"text": "Describe the key scheme used across Defying Gravity and explain its dramatic effect.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: the key rises more than once across the song. One mark: the final statement is in D flat major. One mark: each lift raises the intensity and gives a physical sense of ascent matching the lyric."},
  {"text": "Explain how the orchestration of Defying Gravity combines two different musical traditions.", "marks": 4, "kind": "Explanation",
   "mark_scheme": "One mark: a pit orchestra of strings, woodwind and brass. One mark: a rock rhythm section of guitar, bass, drum kit and keyboards. One mark: the two play together, the orchestra giving lush harmonic support and the rhythm section giving drive. One mark: the blend gives a contemporary sound while keeping the scale expected of a Broadway finale."},
  {"text": "Discuss how the vocal writing in the final section reflects the song's dramatic climax.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: the melody leaps to extreme high pitches. One mark: the singer holds a sustained, belted note. One mark: the register never falls back before the end, so the vocal line itself acts out the defiance in the words."},
]

kcs = [
  {"q": "Which musical does Defying Gravity come from?",
   "options": ["Wicked", "The Wizard of Oz", "Rent", "Hamilton"], "correct": 0},
  {"q": "What dramatic role does Defying Gravity play within the show?",
   "options": ["The opening number", "The act one finale", "The curtain call", "An instrumental overture"], "correct": 1},
  {"q": "In which key does the song reach its final climactic statement?",
   "options": ["C minor", "D flat major", "A major", "F sharp minor"], "correct": 1},
  {"q": "Which combination of forces provides the orchestration for Defying Gravity?",
   "options": ["String quartet only", "Solo piano and voice", "Pit orchestra combined with a rock rhythm section", "Full symphony orchestra with organ"], "correct": 2},
  {"q": "What happens to the texture across the course of the song?",
   "options": ["It stays the same throughout", "It thins out towards the end", "It thickens from sparse chords to full orchestra and voices", "It alternates between solo and silence"], "correct": 2},
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
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", "defyinggravity_l2.html"), "w",
        encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
