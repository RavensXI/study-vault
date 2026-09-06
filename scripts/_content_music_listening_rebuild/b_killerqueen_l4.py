# -*- coding: utf-8 -*-
"""music-edexcel / aos2-vocal-music / L4 -- Killer Queen, the STRUCTURAL walk.
Video 2ZBtPf7FOoM (Top of the Pops, 1974, Queen Official), 3:13 = 193 s.
Pin times, all from the Gemini probe: verse 1 0:08 (3/3), chorus 1 0:33 (3/3),
verse 2 0:58 (3/3), guitar solo 1:31 (2/3), the voice returns 2:08 (3/3), final
chorus 2:24 (3/3). The televised introduction runs to 0:05 (3/3) and the track
ends at 3:06 (3/3); neither is pinned. Chorus 2 (1:22, 3/3) is described inside
the guitar-solo card rather than pinned, because 1:22 and 1:31 would collide.
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck import Deck, dfn, patch, build_questions, check_plain

BACKUP = "music-edexcel__aos2-vocal-music__L04"
d = Deck(lesson_id="574b8a80-cbf4-421d-9731-4e7c8eb2a83d",
         subject="music-edexcel", unit="aos2-vocal-music", lesson_no=4,
         yt="2ZBtPf7FOoM", dur=193, track_label="Killer Queen",
         credit="Top of the Pops, 1974, from the official Queen channel on YouTube &mdash; not hosted by "
                "StudyVault. Queen: Killer Queen.")
TITLE = "Queen: Killer Queen — Guided Listening"

d.pins = [
    ("t1c1", 8,   "Verse 1",      "Lead vocal over a strutting piano. Two layers, and you can hear every word."),
    ("t1c2", 33,  "Chorus 1",     "The stacked backing vocals arrive and the texture thickens in an instant."),
    ("t1c3", 58,  "Verse 2",      "The same tune, but not the same sound: guitar layers are added underneath."),
    ("t1c4", 91,  "Guitar solo",  "The second chorus is cut short and Brian May takes over with a composed, layered solo."),
    ("t1c5", 128, "Verse 3",      "The voice returns after the solo, fuller than it was the first time."),
    ("t1c6", 144, "Final chorus", "Everything the song has gathered, sounding at once, into the wry close."),
]

d.add_cover(
  "Queen: Killer Queen",
  [
    "A 1974 single from the album %s, written by Freddie Mercury. Lead vocal, stacked backing vocals, piano, "
    "electric guitar, bass and drums, in a bright major key and a rolling %s, and shaped as %s with a guitar solo."
    % ("<em>Sheer Heart Attack</em>",
       dfn("12/8", "A compound time signature: four beats in a bar, each divided into three"),
       dfn("verse-chorus form", "A song built from alternating verses, which change their words, and a chorus, which returns unchanged")),
    "It reached number two, Queen&rsquo;s biggest hit to that point and a year before <em>Bohemian Rhapsody</em>. "
    "It is piano-led and closer to music hall and cabaret than to hard rock, and it was built in the studio with "
    "producer Roy Thomas Baker out of layers no four musicians could play at once.",
    "Press play and the cards follow the music. The first five seconds are the television introduction. Tap any "
    "number to jump to that moment.",
  ])

d.add_statement(1, "Verse 1", "1 &middot; Voice and piano",
  "The song opens with finger snaps and piano before Mercury enters. %s What you hear now is the plainest texture in "
  "the whole song: one lead vocal carried on a syncopated, music-hall piano part, which is %s. Nothing is competing "
  "with the voice, so the wit in the words lands. Remember this thinness &mdash; the song is measured against it."
  % (d.ref(1), dfn("melody-dominated homophony", "A texture with one clear melody supported by accompanying chords")),
  "just two layers. Count them now, so you can hear how many are added later.")

d.add_statement(2, "Chorus 1", "2 &middot; The chorus arrives",
  "The chorus does not simply get louder; it gets thicker. %s Mercury, May and Roger Taylor recorded take after take "
  "of %s which were stacked into a choir-like block of sound behind the lead. The band called this the studio doing "
  "what the stage could not, and it became the sound people recognise as Queen."
  % (d.ref(2), dfn("backing vocals", "Sung parts supporting the lead vocal, here recorded many times over and layered")),
  "the moment the single voice becomes a crowd. That switch is the clearest structural signpost in the song.")

d.add_statement(3, "Verse 2", "3 &middot; The same, but not the same",
  "Verse two returns to the tune of verse one. %s Listen to what has changed underneath it: guitar lines have been "
  "added, and parts are spread left and right across the mix by %s. Each returning verse is a varied %s, so the song "
  "grows without altering its harmony or its shape."
  % (d.ref(3), dfn("panning", "Placing a recorded sound at a chosen point between the left and right speakers"),
     dfn("strophe", "A verse that repeats the same music with new words")),
  "new layers arriving rather than a new tune. That is how Queen keep a repeat from sounding mechanical.")

d.add_statement(4, "Guitar solo", "4 &middot; The solo takes over",
  "The second chorus is cut short and the guitar takes the song. %s This is not an improvised rock solo: May "
  "harmonises the line with himself, %s several guitar parts into a written-out instrumental chorus, complete with "
  "bell-like %s. It carries thematic weight, in the way a composer would use it."
  % (d.ref(4), dfn("overdubbing", "Recording a further part on top of parts already recorded"),
     dfn("harmonics", "Bell-like ringing notes made by touching a guitar string lightly at certain points")),
  "several guitars moving in parallel rather than one. That layering is the point of the passage.")

d.add_statement(5, "Verse 3", "5 &middot; The voice comes back",
  "The solo ends and a third verse begins. %s The song has now been through every section it owns: introduction, "
  "verse, chorus, verse, chorus, solo, verse. Nothing new is coming, so from here Queen build only by adding, and the "
  "%s that follows is the fullest sound in the record."
  % (d.ref(5), dfn("outro", "The closing section of a song, after the last verse or chorus")),
  "the accompaniment already heavier than it was in verse one, before the last chorus has even started.")

d.add_statement(6, "Final chorus", "6 &middot; The varied close",
  "The last chorus is not a copy of the first. %s Mercury changes his delivery, the backing vocals are denser and the "
  "guitar layers stay in. That is why the closing section is called a varied chorus: the sense of %s comes from "
  "texture and dynamics, not from any new melody or chord."
  % (d.ref(6), dfn("climax", "The point of greatest intensity in a piece")),
  "how far this is from the piano and single voice you heard at the start. Same tune, four times the sound.")

d.add_checklist(
  "Genre: glam-era pop rock with music-hall and cabaret leanings. Forces: lead vocal, multitracked backing vocals, "
  "piano, electric guitars, bass, drums. Key: a bright major key. Metre and tempo: 12/8, a rolling compound lilt at a "
  "moderate pace. Structure: introduction, three verses and three choruses with a guitar solo after the second chorus "
  "and a varied final chorus. Texture: melody-dominated homophony that thickens by layering. Harmony: functional, "
  "coloured by chromatic chords. Context: 1974, from Sheer Heart Attack, a year before Bohemian Rhapsody.",
  "Structure marks come from labels tied to what you can hear. &ldquo;Verse-chorus form&rdquo; earns little; "
  "&ldquo;the second chorus is cut short after nine seconds so the guitar solo can begin&rdquo; earns the mark.")

content = d.content()
exam_tip = ("<p>If a question asks you to describe the structure, give the sections in order and say what tells you "
            "each one has started. The verses are recognised by the thinner piano-and-voice texture, the choruses by "
            "the stacked backing vocals, and the solo by the harmonised guitar lines. A list of labels with no audible "
            "evidence stays in the lower bands, however correct the labels are.</p>")
conclusion = ("<p>You can now follow Killer Queen section by section and say why each entry sounds the way it does: "
              "the bare piano verse, the sudden choir of backing vocals, the varied second verse, the composed solo, "
              "the returning voice and the built-up final chorus. The next lesson takes the same recording apart "
              "element by element &mdash; melody, harmony, texture, rhythm, timbre and dynamics.</p>")
description = ("Follow Killer Queen section by section, from the piano-led first verse through the guitar solo to the "
               "varied final chorus.")

flashcards = [
  {"q": "What album features Killer Queen and in what year was it released?",
   "a": "Sheer Heart Attack, released in 1974."},
  {"q": "What instrument leads the verse accompaniment in Killer Queen?", "a": "Piano."},
  {"q": "List the sections of Killer Queen in the order you hear them.",
   "a": "Introduction, verse 1, chorus 1, verse 2, chorus 2, guitar solo, verse 3, varied final chorus and outro."},
  {"q": "How is Brian May's guitar solo structurally different from a typical rock solo?",
   "a": "It is composed rather than improvised, and built from layered, harmonised, multitracked guitar lines, so it works like a written-out instrumental chorus."},
  {"q": "Why is the final section of Killer Queen described as a varied chorus?",
   "a": "The melody and chords are the same, but the vocal delivery is altered and the backing vocals and guitar layers are denser, so the song builds to a climax instead of simply repeating."},
  {"q": "Where does Killer Queen sit in Queen's career?",
   "a": "It came in 1974 on Sheer Heart Attack, reached number two and was their biggest hit at that point, a year before Bohemian Rhapsody."},
]

practice = [
  {"text": "Identify the album on which Killer Queen was released.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for Sheer Heart Attack."},
  {"text": "Name the sections of Killer Queen in the order you hear them.", "marks": 3, "kind": "Identification",
   "mark_scheme": "One mark for introduction and verse first. One mark for the chorus following each verse. One mark for the guitar solo falling after the second chorus, followed by a third verse and a varied final chorus."},
  {"text": "Explain how Brian May's guitar solo differs from a typical improvised rock solo.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: it is composed, not improvised. One mark: it is built from harmonised, multitracked guitar lines. One mark: it functions as a written-out instrumental chorus contributing thematic material."},
  {"text": "Identify the instrument that leads the accompaniment texture in the verses.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for piano."},
  {"text": "Explain how Queen stop the returning verses from sounding like a mechanical repeat.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: the melody returns but the accompaniment changes. One mark: guitar layers and backing vocals are added on later verses. One mark: panning spreads the added parts across the stereo field, so each strophe sounds fuller than the last."},
  {"text": "Explain why the final section of Killer Queen is described as varied rather than a simple repeat of the chorus.", "marks": 4, "kind": "Explanation",
   "mark_scheme": "One mark: the melody and harmony are unchanged. One mark: the vocal delivery is altered. One mark: the texture is denser, with more backing vocals and guitar layers retained. One mark: the effect is a built climax rather than a mechanical repeat or a plain fade."},
]

kcs = [
  {"q": "On which Queen album does Killer Queen appear?",
   "options": ["A Night at the Opera", "Sheer Heart Attack", "Jazz", "News of the World"], "correct": 1},
  {"q": "What instrument primarily leads the accompaniment texture in the verses of Killer Queen?",
   "options": ["Electric guitar", "Piano", "Bass guitar", "Drums"], "correct": 1},
  {"q": "How is Brian May's guitar solo best described?",
   "options": ["A loosely improvised blues solo", "A composed, layered melodic statement", "A drum solo transcribed for guitar", "An unaccompanied cadenza"], "correct": 1},
  {"q": "Which section comes immediately after the guitar solo?",
   "options": ["The introduction returns", "A third verse", "An instrumental fade", "A key change"], "correct": 1},
  {"q": "What overall structure does Killer Queen follow?",
   "options": ["Ternary form", "Verse-chorus form with a guitar solo", "Ground bass", "Sonata form"], "correct": 1},
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
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", "killerqueen_l4.html"), "w",
        encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
