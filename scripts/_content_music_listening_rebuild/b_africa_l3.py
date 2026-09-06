# -*- coding: utf-8 -*-
"""music-eduqas / aos4-popular-music / L3 -- Africa, STRUCTURAL walk.
Video FTQbiNvZqaY (official video), 4:32 = 272 s.
Pin times, all 3/3 unless noted: 0:00 first sound, 0:24 verse 1, 1:09
pre-chorus, 1:20 chorus 1, 2:50 the instrumental section, 4:03 the fade begins
(2/3, 4:00 and 4:03). Verse 2 (1:43) and chorus 2 (2:27) were also 3/3 and are
described in the cards rather than pinned. All three votes answered "none" to a
key change for the final choruses, so the deck does not claim one.
The board is never named."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck import Deck, dfn, patch, build_questions, check_plain

BACKUP = "music-eduqas__aos4-popular-music__L03"
d = Deck(lesson_id="1fa8008e-3bd6-44be-a821-a60e7f274eb4",
         subject="music-eduqas", unit="aos4-popular-music", lesson_no=3,
         yt="FTQbiNvZqaY", dur=272, track_label="Africa", board="eduqas",
         credit="Official video, streamed from YouTube &mdash; not hosted by StudyVault. Toto: Africa (1982).")
TITLE = "Toto: Africa — Guided Listening"

d.pins = [
    ("t1c1", 0,   "Intro",       "The layered ostinato: a synth programmed to sound like a kalimba, doubled by a real marimba."),
    ("t1c2", 24,  "Verse 1",     "The half-time groove arrives. Count where the snare falls."),
    ("t1c3", 69,  "Pre-chorus",  "The lift starts here, before the hook has even arrived."),
    ("t1c4", 80,  "Chorus 1",    "The hook, with backing vocals stacked in harmony. The fullest texture so far."),
    ("t1c5", 170, "Solo",        "The voices stop and a synthesiser takes the tune over the same ostinato."),
    ("t1c6", 243, "The fade",    "Layers strip away and the track fades on the pattern it opened with."),
]

d.add_cover(
  "Toto: Africa",
  [
    "A 1982 single from the album <em>Toto IV</em>, written by David Paich and Jeff Porcaro, and a US number one the "
    "following year. Lead and backing vocals, layered keyboards and synthesisers, marimba, guitar, bass and drums, "
    "in %s with a chorus that lifts."
    % dfn("verse-chorus form", "A song shape alternating verses, which carry changing words, with a returning chorus"),
    "Toto were formed in Los Angeles in 1977 out of experienced %s. That matters here: the track was assembled in "
    "the studio, layer by layer, using the newest synthesiser technology of the day rather than played live in one take."
    % dfn("session musicians", "Professional players hired to perform on other artists&rsquo; recordings"),
    "Press play and the cards follow the music. Tap any number to jump to that moment.",
  ])

d.add_statement(1, "Intro", "1 &middot; The pattern that never leaves",
  "The first sound is a bright, repeating figure high in the register. %s It is two instruments at once: a digital "
  "synthesiser programmed to imitate a %s, doubled by a real marimba, with a fast decay so each note is plucked "
  "rather than held. This %s runs almost continuously for the rest of the song."
  % (d.ref(1), dfn("kalimba", "An African thumb piano, plucked with the thumbs, with a bright bell-like tone"),
     dfn("ostinato", "A short pattern repeated persistently throughout a section or whole piece")),
  "the bell-like, plucked quality. Everything else in the track is added around this one figure.")

d.add_statement(2, "Verse 1", "2 &middot; The groove underneath",
  "The band enters and the drum pattern is the thing to listen to. %s Jeff Porcaro plays a %s: the snare lands on "
  "beat three rather than on two and four, over steady sixteenth notes on the hi-hat. The snare arrives less often "
  "than you expect, which is why the track feels spacious rather than driven."
  % (d.ref(2), dfn("half-time groove", "A drum pattern whose snare backbeat falls on beat three over a busier subdivision, giving a relaxed feel")),
  "the gap between snare hits. Count to four and notice how little is landing where a rock beat would put it.")

d.add_statement(3, "Pre-chorus", "3 &middot; The lift begins early",
  "Before the hook arrives, the song has already started to grow. %s Extra keyboard lines come in, backing voices "
  "gather and the register rises, so the chorus is prepared rather than sprung. That preparation is what a "
  "%s is for: it makes the arrival feel earned."
  % (d.ref(3), dfn("pre-chorus", "A short section between verse and chorus that builds towards it")),
  "layers arriving before the words of the hook do. Structure marks come from spotting the build, not just the chorus.")

d.add_statement(4, "Chorus 1", "4 &middot; The hook",
  "The chorus arrives and the texture is the fullest yet. %s The lead vocal is doubled and supported by backing "
  "vocals a third or a sixth away, the drums fill out and more keyboard layers join. Because the energy rises as "
  "well as the material changing, this is called a %s."
  % (d.ref(4), dfn("lifted chorus", "A chorus in which texture, register and energy rise compared with the verse")),
  "how many more parts are sounding than in the verse. Say &lsquo;more layers&rsquo;, not &lsquo;it gets bigger&rsquo;.")

d.add_statement(5, "Solo", "5 &middot; The instrumental",
  "Verse two and a second chorus have been and gone, and now the voices stop altogether. %s A synthesiser takes the "
  "melodic lead over the same ostinato and rhythm section, so the texture thins back to melody plus accompaniment "
  "and the solo timbre stands out. It is short: the singing returns within about fifteen seconds."
  % d.ref(5),
  "the ostinato continuing underneath. The solo is laid over the song, not a break from it.")

d.add_statement(6, "The fade", "6 &middot; Taking it apart",
  "The song ends the way many studio pop records of the period do, by %s rather than by stopping. %s Layers are "
  "removed one at a time until little is left but the pattern the track opened with, which closes the arch. There "
  "is no final chord and no key change anywhere in the song."
  % (dfn("fading out", "Gradually reducing the volume of the whole mix to end a recording"), d.ref(6)),
  "which layers survive longest. Ending on the opening ostinato is a deliberate shape, not just a fade.")

d.add_checklist(
  "Genre: early 1980s soft rock and pop. Forces: lead and backing vocals, layered synthesisers and keyboards, "
  "marimba, electric guitar, bass and drum kit. Structure: intro, verse, pre-chorus, lifted chorus, verse, chorus, "
  "short instrumental solo, final choruses and fade, over a near-continuous ostinato. Texture: homophonic and thin "
  "in the verse, thick and layered in the chorus. Rhythm: half-time groove, snare on beat three over steady "
  "sixteenths. Context: 1982, from Toto IV, built in the studio by session musicians.",
  "Name the section and the evidence together. &ldquo;The chorus sounds bigger&rdquo; earns little; &ldquo;the "
  "chorus adds stacked backing vocals in thirds and further keyboard layers over the same ostinato&rdquo; earns the mark.")

content = d.content()
exam_tip = ("<p>Always name the technique rather than the impression. Do not write that the drums sound relaxed; "
            "identify the half-time groove and say the snare falls on beat three over steady sixteenths. Do not "
            "write that the chorus sounds bigger; refer to layering, added vocal harmony and rising register. The "
            "technical word plus the evidence is what the mark scheme is looking for.</p>")
conclusion = ("<p>You can now follow the whole track: the ostinato that never leaves, the half-time groove, the "
              "pre-chorus lift, the layered chorus, the short synthesiser solo and the fade back to the opening "
              "pattern. The next lesson takes the same recording element by element &mdash; timbre and technology, "
              "rhythm, texture, harmony, melody and production.</p>")
description = ("Follow Toto's Africa through six landmarks, from the kalimba-like ostinato to the fade that strips "
               "the track back to where it began.")

flashcards = [
  {"q": "What creates the kalimba-like timbre in the intro of 'Africa'?",
   "a": "A digital synthesizer programmed with a fast decay to sound plucked and metallic, doubled by a real marimba."},
  {"q": "What is a half-time groove?",
   "a": "A drum pattern placing the snare backbeat on beat three over a steady sixteenth-note subdivision, so the snare falls less often and the groove feels laid-back."},
  {"q": "What form does 'Africa' follow?",
   "a": "Verse-chorus form, with a pre-chorus and a lifted chorus in which texture, register and energy all rise."},
  {"q": "Who wrote 'Africa', and on which album was it released?",
   "a": "David Paich and Jeff Porcaro, on Toto IV in 1982. It reached number one in the US the following year."},
  {"q": "Why can Toto be called a studio band?",
   "a": "Its members were experienced Los Angeles session musicians who built the sound through studio technology and layering rather than by recording live in one take."},
  {"q": "How does 'Africa' end?",
   "a": "With a fade-out. Layers are removed one at a time until little remains but the opening ostinato, so the track closes on the pattern it started with."},
]

practice = [
  {"text": "Name the decade in which Toto recorded and released 'Africa'.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for the 1980s, or for 1982."},
  {"text": "Identify the term used to describe Jeff Porcaro's distinctive drum pattern in 'Africa'.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for half-time groove, or half-time drum groove."},
  {"text": "Describe how the opening synth pattern in 'Africa' creates a kalimba-like timbre.", "marks": 2, "kind": "Description",
   "mark_scheme": "One mark: a synthesizer programmed with a fast decay or percussive envelope, so notes sound plucked rather than sustained. One mark: it sits high in the register and is doubled by a real marimba, imitating a plucked metallic instrument."},
  {"text": "Explain how texture changes between the verse and the chorus in 'Africa'.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: the verse is relatively sparse, with bass, drums and keyboard chords over the ostinato. One mark: the chorus adds backing vocal harmony and further keyboard layers. One mark: the drums fill out and the register rises, so the chorus is lifted rather than simply different."},
  {"text": "Explain why Toto can be described as a studio band, referring to the roles of its members.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: the members were experienced session musicians before forming the band. One mark: each brought a specialist studio role, for example Paich and Steve Porcaro on keyboards and Jeff Porcaro on drums. One mark: the track was built by layering separately recorded parts using new synthesizer technology rather than played live."},
  {"text": "Discuss how the drum groove, keyboard layering and verse-chorus form work together to create the overall feel of 'Africa'.", "marks": 4, "kind": "Explanation",
   "mark_scheme": "One mark: the half-time groove keeps the pulse spacious and relaxed. One mark: layered keyboards and the continuous ostinato give a polished, full sound. One mark: verse-chorus form with a pre-chorus prepares each arrival. One mark: a developed link showing how the lifted chorus depends on all three working together."},
]

kcs = [
  {"q": "In what year was Toto's 'Africa' released?",
   "options": ["1975", "1982", "1990", "2001"], "correct": 1},
  {"q": "What creates the kalimba-like sound at the start of 'Africa'?",
   "options": ["An acoustic kalimba recorded live", "A programmed synthesizer doubled by a marimba", "A sampled recording of rainfall", "An electric guitar with a capo"], "correct": 1},
  {"q": "What term describes Jeff Porcaro's drum groove in 'Africa'?",
   "options": ["Straight rock beat", "Half-time groove", "Four-on-the-floor", "Drum and bass break"], "correct": 1},
  {"q": "What is meant by a 'lifted chorus'?",
   "options": ["A chorus performed a cappella", "A chorus with reduced texture and quieter dynamics", "A chorus where texture, layering and energy rise compared to the verse", "A chorus that repeats the verse melody exactly"], "correct": 2},
  {"q": "How does the track end?",
   "options": ["On a loud final chord", "With a fade-out back to the opening ostinato", "With an unaccompanied vocal", "With a key change into a last chorus"], "correct": 1},
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
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", "africa_l3.html"), "w",
        encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
