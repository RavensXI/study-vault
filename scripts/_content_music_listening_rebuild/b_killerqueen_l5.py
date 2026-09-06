# -*- coding: utf-8 -*-
"""music-edexcel / aos2-vocal-music / L5 -- Killer Queen, the ELEMENTS walk.
Same recording as L4 (2ZBtPf7FOoM, 193 s). Pins reuse verified probe times:
0:05 first sound (3/3), 0:33 chorus 1 (3/3), 1:22 chorus 2 (3/3), 1:31 guitar
solo (2/3), 2:08 the voice returns (3/3), 2:24 final chorus (3/3). One card per
element: rhythm and metre, texture, harmony and tonality, timbre and technology,
melody, dynamics."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck import Deck, dfn, patch, build_questions, check_plain

BACKUP = "music-edexcel__aos2-vocal-music__L05"
d = Deck(lesson_id="7af3603a-1650-442e-a633-b8d5a2d3af7b",
         subject="music-edexcel", unit="aos2-vocal-music", lesson_no=5,
         yt="2ZBtPf7FOoM", dur=193, track_label="Killer Queen",
         credit="Top of the Pops, 1974, from the official Queen channel on YouTube &mdash; not hosted by "
                "StudyVault. Queen: Killer Queen.")
TITLE = "Queen: Killer Queen — The Elements in Close-Up"

d.pins = [
    ("t1c1", 5,   "Rhythm",      "Finger snaps and piano set the lilt. Four beats, but each one splits into three."),
    ("t1c2", 33,  "Texture",     "Two layers become a wall. Count what arrives at the chorus."),
    ("t1c3", 82,  "Harmony",     "Chorus two. Chords that step outside the key and slide back."),
    ("t1c4", 91,  "Timbre",      "Brian May&rsquo;s guitar sound: home-made instrument, layered lines, bell-like tones."),
    ("t1c5", 128, "Melody",      "The third verse. Listen to the leaps and the way words are pushed and pulled."),
    ("t1c6", 144, "Dynamics",    "The last chorus. Louder because there is more of it, not because anyone plays harder."),
]

d.add_cover(
  "The same song, element by element",
  [
    "Killer Queen, from Queen&rsquo;s 1974 album <em>Sheer Heart Attack</em>, written by Freddie Mercury: lead vocal, "
    "stacked backing vocals, piano, electric guitars, bass and drums, in a bright major key and a rolling %s, shaped "
    "as verse-chorus form with a guitar solo."
    % dfn("12/8", "A compound time signature: four beats in a bar, each divided into three"),
    "The previous lesson followed the song section by section. This one stops six times, once for each %s an examiner "
    "can set a question on: rhythm and metre, texture, harmony, timbre and studio technology, melody and dynamics."
    % dfn("element of music", "The building blocks of music: melody, harmony, tonality, texture, timbre, dynamics, rhythm, metre, tempo and structure"),
    "Press play and the cards follow the music. Tap any number to jump to that moment.",
  ])

d.add_statement(1, "Rhythm", "1 &middot; Four beats, each split in three",
  "Snap along and you will find four beats in the bar. %s Then listen to what fills each beat: three notes, not two. "
  "That is %s time, and it is why the song rolls rather than marches. The piano adds %s, pushing notes off the beat, "
  "which gives the accompaniment its music-hall strut."
  % (d.ref(1), dfn("compound", "Time in which each beat divides into three, as in 6/8, 9/8 and 12/8"),
     dfn("syncopation", "Placing accents on weak beats or between beats, against the expected pulse")),
  "the triple subdivision inside each beat. If it swings but you can still count four, the answer is 12/8, not 4/4.")

d.add_statement(2, "Texture", "2 &middot; From two layers to many",
  "In the verse there were two layers: a voice and a piano, which is %s. %s At the chorus that becomes a block of "
  "sound, because separate recordings of Mercury, May and Taylor singing harmony are stacked together. The harmony "
  "has not changed. Only the number of layers has."
  % (dfn("melody-dominated homophony", "A texture with one clear melody supported by accompanying chords"), d.ref(2)),
  "how many distinct vocal parts you can pick out. Say how many layers and what each is doing, not just "
  "&lsquo;the texture gets thicker&rsquo;.")

d.add_statement(3, "Harmony", "3 &middot; Chords with a twist",
  "The song sits securely in a major key. %s Mercury colours it with %s that step outside the key and resolve "
  "straight back, and with runs of chords whose roots fall by fifths, the %s, which pulls the ear towards the %s at "
  "the end of a phrase. Pop function, classical furniture."
  % (d.ref(3), dfn("chromatic chords", "Chords using notes from outside the home key, added for colour"),
     dfn("circle of fifths", "A chord pattern whose roots fall by a fifth each time, creating strong forward motion"),
     dfn("cadence", "The chord progression that closes a musical phrase")),
  "a chord that sounds momentarily wrong and then right again. Name it as chromatic, and say it resolves back to the key.")

d.add_statement(4, "Timbre", "4 &middot; The sound of the guitar",
  "May plays a guitar he built himself, the Red Special, through a %s, which drives the amplifier into a singing, "
  "sustained tone. %s He layers several such lines by %s, and adds ringing %s to imitate bells. Panning spreads them "
  "left and right; %s and wah-wah pedal shape the tone further."
  % (dfn("treble booster", "A device that boosts an electric guitar&rsquo;s high frequencies to drive the amplifier harder"),
     d.ref(4), dfn("overdubbing", "Recording a further part on top of parts already recorded"),
     dfn("harmonics", "Bell-like ringing notes made by touching a string lightly at certain points"),
     dfn("flanger", "An effect that mixes a signal with a very slightly delayed copy of itself, giving a swirling sound")),
  "several guitars moving in parallel, not one. Name the effect and describe what it does to the sound.")

d.add_statement(5, "Melody", "5 &middot; The line and the delivery",
  "The lead vocal is deliberately theatrical. %s It leaps widely rather than moving by step, stretches and clips the "
  "rhythm against the beat, and exaggerates consonants. That delivery is a kind of %s: the manner of singing acts out "
  "the glamour the words describe: how a phrase is sung carries meaning."
  % (d.ref(5), dfn("word painting", "Shaping the music so that it reflects the meaning of the words")),
  "the size of the leaps and the freedom of the rhythm. Describe the effect, not the lyric.")

d.add_statement(6, "Dynamics", "6 &middot; Loudness built from layers",
  "The last chorus is the loudest point in the song, and nobody is playing harder. %s The increase comes from %s: "
  "backing vocals, guitar parts and the fuller mix are all kept in at once. Studio pop builds a %s by addition, where "
  "an orchestra would build one by playing louder."
  % (d.ref(6), dfn("layering", "Combining separately recorded parts so that more sounds play at once"),
     dfn("climax", "The point of greatest intensity in a piece")),
  "the difference between the first verse and this. Same tune, four times the sound, no crescendo marked anywhere.")

d.add_checklist(
  "Melody: wide leaps and flexible rhythm, delivered theatrically. Harmony: major, with chromatic passing chords and "
  "circle-of-fifths movement into cadences. Texture: melody-dominated homophony in the verses, thickening to dense "
  "layered vocal and guitar harmony in the choruses. Rhythm and metre: 12/8 compound time with a rolling, syncopated "
  "lilt. Timbre and technology: Red Special guitar with treble booster, multitracked and harmonised guitar lines, "
  "harmonics, panning, flanger and wah-wah, produced with Roy Thomas Baker. Dynamics: built by layering rather than "
  "by playing louder.",
  "Every one of those words needs a moment attached to it. &ldquo;Multitracking&rdquo; earns little; &ldquo;the "
  "backing vocals at the first chorus are several recorded takes stacked together, which is why the texture thickens "
  "instantly&rdquo; earns the mark.")

content = d.content()
exam_tip = ("<p>Production is examinable content, not background. If you can name multitracking, overdubbing, panning, "
            "flanger and wah-wah and say what each one does to the sound you hear, you are answering a texture or "
            "timbre question properly. Write the technique, then the audible result, then why it suits the song: "
            "&lsquo;the stacked backing vocals give a choir-like block of sound that matches the theatrical subject&rsquo;.</p>")
conclusion = ("<p>You can now take Killer Queen apart element by element: a 12/8 lilt with a syncopated piano, a "
              "texture that grows from two layers to many, chromatic and circle-of-fifths harmony inside a secure "
              "major key, a guitar sound built from a home-made instrument and studio overdubs, a leaping theatrical "
              "vocal line, and dynamics made by addition. That completes the Vocal Music area of study, so revisit "
              "Purcell alongside it and practise comparing the two.</p>")
description = ("Six numbered stops in Killer Queen, one for each element: rhythm, texture, harmony, timbre and studio "
               "technology, melody and dynamics.")

flashcards = [
  {"q": "What instruments form the core texture in Killer Queen's verses?",
   "a": "Lead vocal supported by piano, a melody-dominated homophonic texture of only two layers."},
  {"q": "What is a circle of fifths?",
   "a": "A chord pattern in which the roots fall by a fifth each time, creating strong forward motion towards a cadence."},
  {"q": "What production technique is central to Killer Queen's layered vocal harmonies?",
   "a": "Multitracking, or overdubbing: separate vocal takes by Mercury, May and Taylor are recorded one at a time and combined into a single dense texture."},
  {"q": "How does the texture of Killer Queen change by the final chorus compared with verse 1?",
   "a": "It thickens from a two-layer piano-and-voice texture into a dense multi-layered texture with stacked backing vocals and added guitar parts."},
  {"q": "What is the time signature of Killer Queen, and what does it do to the feel?",
   "a": "12/8, a compound time with four beats in a bar each divided into three. It gives the rolling, swung, music-hall lilt rather than a straight rock backbeat."},
  {"q": "How does Brian May get his guitar sound on this track?",
   "a": "His home-made Red Special guitar through a treble booster for a sustained singing tone, with several harmonised lines overdubbed, bell-like harmonics, and panning, flanger and wah-wah in the mix."},
]

practice = [
  {"text": "State the recording technique used by Queen to create dense vocal harmony in the choruses of Killer Queen.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for multitracking or overdubbing of vocal parts."},
  {"text": "Describe two ways the texture of Killer Queen changes between the first verse and the final chorus.", "marks": 2, "kind": "Description",
   "mark_scheme": "One mark each, up to two, from: stacked multitracked backing vocals are added; layered guitar parts are added; the two-layer voice-and-piano texture becomes dense and multi-layered."},
  {"text": "Explain how chromatic chords and circle-of-fifths harmony contribute to the sophisticated character of Killer Queen.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: chromatic chords use notes from outside the key. One mark: they add colour and then resolve back, so the key is never lost. One mark: circle-of-fifths movement drives the harmony forward into cadences, a device borrowed from classical and jazz writing."},
  {"text": "Name one studio production technique used on Killer Queen and describe its audible effect.", "marks": 2, "kind": "Description",
   "mark_scheme": "One mark for naming panning, flanger, wah-wah, overdubbing or multitracking. One mark for an accurate description of the sound it creates, such as flanger giving a swirling phased tone or panning spreading parts across the stereo field."},
  {"text": "Identify the time signature of Killer Queen and describe the rhythmic feel it creates.", "marks": 2, "kind": "Description",
   "mark_scheme": "One mark for 12/8 or compound quadruple time. One mark for the rolling, swung, lilting feel produced by dividing each beat into three, reinforced by syncopation in the piano."},
  {"text": "Compare the use of accompaniment in Killer Queen and Music for a While.", "marks": 4, "kind": "Explanation",
   "mark_scheme": "One mark: Purcell uses a continuously repeating ground bass with continuo. One mark: Queen use a piano-led band with layered studio overdubs. One mark: Purcell's accompaniment is fixed while the voice varies above it. One mark: Queen's accompaniment grows across the song, so the variation is in the accompaniment rather than the voice."},
]

kcs = [
  {"q": "Which harmonic feature helps create forward momentum toward cadences in Killer Queen?",
   "options": ["Ground bass", "Circle-of-fifths chord movement", "Pentatonic scale", "Ostinato bass riff"], "correct": 1},
  {"q": "What production technique allowed Queen to create dense, stacked vocal harmonies?",
   "options": ["Live choir recording", "Multitracking and overdubbing", "Reverb only", "Single-take recording"], "correct": 1},
  {"q": "In what time signature is Killer Queen written?",
   "options": ["4/4", "3/4", "12/8", "7/8"], "correct": 2},
  {"q": "Which production effect creates a swirling, phased sound by combining a signal with a slightly delayed copy of itself?",
   "options": ["Wah-wah", "Flanger", "Reverb only", "Compression"], "correct": 1},
  {"q": "Which best describes the texture change across Killer Queen's structure?",
   "options": ["It stays constant throughout", "It thins out toward the end", "It builds gradually from sparse to densely layered", "It alternates randomly with no pattern"], "correct": 2},
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
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", "killerqueen_l5.html"), "w",
        encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
