# -*- coding: utf-8 -*-
"""music-eduqas / aos4-popular-music / L4 -- Africa, ELEMENTS walk.
Same recording as L3 (FTQbiNvZqaY, 272 s). Pin times all 3/3 except the fade
(2/3): 0:00 first sound, 0:24 verse 1, 1:43 verse 2, 2:27 chorus 2, 2:50 the
instrumental section, 4:03 the fade. One card per element: timbre and
technology, rhythm, texture, harmony, melody, production and dynamics.
The board is never named."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck import Deck, dfn, patch, build_questions, check_plain

BACKUP = "music-eduqas__aos4-popular-music__L04"
d = Deck(lesson_id="ad0c93c9-6eaa-4c7b-86e9-8f34a7550cbc",
         subject="music-eduqas", unit="aos4-popular-music", lesson_no=4,
         yt="FTQbiNvZqaY", dur=272, track_label="Africa", board="eduqas",
         credit="Official video, streamed from YouTube &mdash; not hosted by StudyVault. Toto: Africa (1982).")
TITLE = "Toto: Africa — The Elements in Close-Up"

d.pins = [
    ("t1c1", 0,   "Timbre",     "Two instruments pretending to be one. Listen to how each note stops."),
    ("t1c2", 24,  "Rhythm",     "Count to four and find the snare. It is not where you expect it."),
    ("t1c3", 103, "Texture",    "The verse: melody plus accompaniment over the ostinato. Count the layers."),
    ("t1c4", 147, "Harmony",    "Backing voices a third and a sixth from the tune, moving with it."),
    ("t1c5", 170, "Melody",     "A synthesiser takes the tune. The accompaniment underneath has not changed."),
    ("t1c6", 243, "Production", "The fade. Studio technique deciding how the song ends."),
]

d.add_cover(
  "The same track, element by element",
  [
    "Toto&rsquo;s 1982 single from <em>Toto IV</em>, written by David Paich and Jeff Porcaro: vocals, layered "
    "synthesisers and keyboards, marimba, guitar, bass and drums, over an %s that runs almost from end to end."
    % dfn("ostinato", "A short pattern repeated persistently throughout a section or whole piece"),
    "The previous lesson followed the song section by section. This one stops six times, once for each %s the exam "
    "sets questions on here: timbre and technology, rhythm, texture, harmony, melody, and production with dynamics."
    % dfn("element of music", "The building blocks of music: melody, harmony, tonality, texture, timbre, dynamics, rhythm, metre, tempo and structure"),
    "Press play and the cards follow the music. Tap any number to jump to that moment.",
  ])

d.add_statement(1, "Timbre", "1 &middot; A sound built, not recorded",
  "This bright opening figure is not one instrument. %s A digital %s was programmed to imitate the plucked, metallic "
  "sound of an African thumb piano, and a real marimba was recorded doubling it. The %s is fast, so each note stops "
  "almost at once, which is what makes the pattern sound plucked."
  % (d.ref(1), dfn("synthesizer", "An electronic instrument that generates and shapes sound, able to imitate other instruments"),
     dfn("decay", "How quickly a note dies away after it is played")),
  "the short, bell-like stop on every note. Name the technology, not just the sound it imitates.")

d.add_statement(2, "Rhythm", "2 &middot; Where the snare is not",
  "Count four beats and follow the snare drum. %s In a standard rock beat it lands on two and four. Here it lands "
  "on beat three only, over a busy stream of sixteenth notes on the hi-hat. That is a %s, and the mismatch between "
  "busy hi-hat and sparse snare is a form of %s."
  % (d.ref(2), dfn("half-time groove", "A drum pattern whose snare backbeat falls on beat three over a busier subdivision"),
     dfn("syncopation", "Accenting beats that are not normally emphasised")),
  "how far apart the snare hits are. That spacing is why the track feels relaxed at this tempo.")

d.add_statement(3, "Texture", "3 &middot; Counting the layers",
  "A verse is the thinnest the song gets once the band is in. %s Over the ostinato sit bass, drum kit and keyboard "
  "chords under a single lead vocal: a %s texture, melody plus supporting accompaniment. Fix that number of layers, "
  "because the chorus will roughly double it."
  % (d.ref(3), dfn("homophonic", "A texture in which parts move together, a melody supported by chordal accompaniment")),
  "how few parts are sounding. Use the words thinner and denser rather than smaller and bigger.")

d.add_statement(4, "Harmony", "4 &middot; Voices in parallel",
  "The chorus is where the harmony shows. %s The lead vocal is doubled and backing voices sing a third or a sixth "
  "above or below, all moving in the same rhythm, which makes a homophonic %s. That blended sound reinforces the "
  "%s and is held back from the verses on purpose, to create contrast."
  % (d.ref(4), dfn("vocal harmony", "Two or more vocal lines at different pitches sung at the same time"),
     dfn("hook", "The short, memorable phrase a listener recognises instantly")),
  "the parallel movement. The voices are not independent lines; they move as one thickened melody.")

d.add_statement(5, "Melody", "5 &middot; The tune changes hands",
  "The voices stop and a synthesiser takes the melodic lead. %s Everything under it stays: the ostinato, the bass "
  "and the groove continue unchanged, so the texture thins back to melody plus accompaniment and the solo %s becomes "
  "the featured sound. It lasts about fifteen seconds before the singing returns."
  % (d.ref(5), dfn("timbre", "The characteristic tone colour that distinguishes one instrument or voice from another")),
  "the accompaniment carrying on regardless. That is why the section thins without losing momentum.")

d.add_statement(6, "Production", "6 &middot; Decisions made in the studio",
  "The song does not end; it is faded. %s Every part here was recorded separately and combined, which is %s, and "
  "%s was added to voices and drums to make the mix sound spacious and smooth. Production is not a neutral wrapper "
  "in this track: it decides the texture, the sound and the ending."
  % (d.ref(6), dfn("multitrack layering", "Recording parts separately and combining them in the mix to build texture"),
     dfn("reverb", "An effect simulating sound reflecting in a space, making a recording sound bigger or smoother")),
  "how polished and wide the mix is. Name the technique, then say what it does to what you hear.")

d.add_checklist(
  "Melody: a memorable vocal hook, taken over by a synthesizer in the instrumental section. Harmony: close vocal "
  "harmony in thirds and sixths in the chorus, with no key change anywhere in the song. Texture: homophonic and "
  "thin in the verse, thick and layered in the chorus, thinning again for the solo. Rhythm: half-time groove, snare "
  "on beat three over steady sixteenths, and a continuous ostinato. Timbre: a synthesizer imitating a kalimba, "
  "doubled by marimba. Production: multitrack layering, reverb and a fade-out ending.",
  "Attach the term to the sound. &ldquo;It uses reverb&rdquo; earns little; &ldquo;reverb on the vocals and drums "
  "widens the mix and smooths the sound, which is what makes the chorus feel spacious&rdquo; earns the mark.")

content = d.content()
exam_tip = ("<p>Production counts as musical content in this area of study, not as background information. Learn to "
            "name multitrack layering, reverb and the fade-out, and to say what each does to the sound you can hear. "
            "The same applies to texture: use monophonic, homophonic and layered precisely, and describe the verse "
            "as thinner and the chorus as denser rather than smaller and bigger.</p>")
conclusion = ("<p>You can now name each element of this track and point to where it is audible: a synthesizer "
              "imitating a kalimba over a doubled marimba, a half-time groove with the snare on beat three, a "
              "homophonic verse against a layered chorus, close vocal harmony in thirds and sixths, the tune passing "
              "to a synthesizer, and production choices that decide both the polish and the ending.</p>")
description = ("Six numbered stops in Toto's Africa, one for each element: timbre, rhythm, texture, harmony, melody "
               "and production.")

flashcards = [
  {"q": "What plays the main ostinato in 'Africa'?",
   "a": "A digital synthesizer programmed to imitate a kalimba, doubled by a real marimba, heard from the introduction onwards."},
  {"q": "How does the texture change from verse to chorus in 'Africa'?",
   "a": "It moves from a sparser, homophonic verse texture to a thicker, layered chorus with added vocal harmony and further keyboard layers."},
  {"q": "What kind of vocal texture is used in the chorus?",
   "a": "Homophonic vocal harmony, with backing vocals singing in thirds and sixths above or below the lead and moving in the same rhythm."},
  {"q": "What effect gives 1980s pop recordings a spacious, polished sound?",
   "a": "Reverb, added to vocals and drums to simulate space and smooth the sound."},
  {"q": "What production technique allows a producer to build texture gradually across a song?",
   "a": "Multitrack layering: recording each part separately, then combining and balancing them in the mix."},
  {"q": "What happens to the texture during the synthesizer solo?",
   "a": "It thins back to melody plus accompaniment. The vocals stop while the ostinato, bass and drum groove continue, so the solo timbre is featured."},
]

practice = [
  {"text": "Identify the instruments that play the repeating pattern heard throughout most of 'Africa'.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for a synthesizer imitating a kalimba, doubled by marimba. Accept marimba or kalimba alone."},
  {"text": "Describe the change in texture between the verse and chorus of 'Africa'.", "marks": 2, "kind": "Description",
   "mark_scheme": "One mark: the verse is sparser and homophonic, a lead vocal over ostinato, bass, drums and keyboard chords. One mark: the chorus is thicker and more layered, with backing vocal harmony and added keyboard parts."},
  {"text": "Name the production technique that allows separate instrumental and vocal parts to be recorded and combined afterwards.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for layering, or multitrack recording."},
  {"text": "Explain how reverb affects the sound of the drums or vocals in a track such as 'Africa'.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: reverb simulates sound reflecting in a space. One mark: it makes the part sound bigger, smoother or more distant. One mark: applied to vocals or drums it widens the mix and contributes to the polished early 1980s sound."},
  {"text": "Explain why the texture thins during the synthesizer solo section of the song.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: the vocals and their harmony layers drop out. One mark: the ostinato and rhythm section continue underneath. One mark: this leaves a melody-plus-accompaniment texture so the solo timbre stands out as the featured sound."},
  {"text": "Discuss how vocal harmony contributes to the effectiveness of the chorus in 'Africa'.", "marks": 4, "kind": "Explanation",
   "mark_scheme": "One mark: backing vocals sing in thirds and sixths around the lead. One mark: they move in the same rhythm, giving a homophonic vocal texture. One mark: the blended sound reinforces the hook. One mark: because the harmony is held back from the verses, it creates contrast and helps lift the chorus."},
]

kcs = [
  {"q": "What plays the continuous ostinato pattern in 'Africa'?",
   "options": ["A synthesizer imitating a kalimba, doubled by marimba", "Electric guitar", "Saxophone", "Cello"], "correct": 0},
  {"q": "Which best describes the chorus vocal texture in 'Africa'?",
   "options": ["Monophonic", "Homophonic vocal harmony", "Unaccompanied solo", "Call and response only"], "correct": 1},
  {"q": "What effect is commonly added to vocals and drums to create a spacious, polished sound in 1980s pop production?",
   "options": ["Distortion", "Reverb", "Panning only", "Muting"], "correct": 1},
  {"q": "What happens to the texture during the synthesizer solo?",
   "options": ["It becomes thicker with extra vocal layers", "It thins to melody plus accompaniment", "All instruments stop", "The ostinato disappears entirely"], "correct": 1},
  {"q": "On which beat does the snare fall in the half-time groove?",
   "options": ["Beats two and four", "Beat three only", "Every beat", "Beat one only"], "correct": 1},
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
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", "africa_l4.html"), "w",
        encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
