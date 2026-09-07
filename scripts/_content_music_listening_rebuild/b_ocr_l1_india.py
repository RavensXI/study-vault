# -*- coding: utf-8 -*-
"""music-ocr / aos3-rhythms-listening / L1 -- India and Punjab.

Rebuilt from a PRACTICE row (synthesised-click problem bank) into a guided
listening lesson on two real recordings, per Tom's decision 7 Sep 2026.

Recordings, both verified: oEmbed 200, yt-dlp playable_in_embed True, age 0,
and loaded without error in a real YouTube IFrame player on the studyvault.co.uk
origin (durations below are that player's own getDuration).

  t1  JzdkIrQ73iY  246 s  darbarfestival: "Teen Taal | Ustad Tari Khan | Music
                          of India". Punjab-gharana tabla solo in teentaal with
                          harmonium lehra; the player recites the bols first.
  t2  pPZFlxmfqrM  312 s  Balwinder Safri (Topic, label release): "Aaja Billo".
                          UK bhangra: dhol chaal with tumbi, harmonium,
                          synthesisers and a drum machine.

Pin times: 3-vote Gemini consensus, timings.json keys ocr_l1_t1 / ocr_l1_t1b /
ocr_l1_t2 / ocr_l1_t2b; every pin carries at least 2 of 3 agreeing votes.
Dropped: t1 "harmonium_lehra_enters" at 55 s (3 s from the 52 s pin, folded
into that card); t1 "speech_ends" (56 / 103 / 103 -- corroborated but it
contradicts the 3/3 music_starts at 52, so the recitation and the playing
interleave and no single pin is honest); t1 "first_sound" at 5 s (a logo
sting, not music); t2 "first_vocal_entry" at 12 s (2.8% from the 3 s pin,
folded into the 23 s card); t2 "groove_starts" from the first probe
(4 / 12 / 27 -- re-probed as "percussion_groove_in" and settled at 3 s).
"""
import io, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck_multi import MultiDeck, dfn, patch, check_plain

BACKUP = "music-ocr__aos3-rhythms-listening__L01"
HERE = os.path.dirname(os.path.abspath(__file__))
old = json.load(io.open(os.path.join(HERE, "backups", BACKUP + ".json"), encoding="utf-8"))

d = MultiDeck(
    lesson_id=old["id"], subject="music-ocr", unit="aos3-rhythms-listening", lesson_no=1,
    tracks=[("t1", "JzdkIrQ73iY", 246, "Tabla in teentaal"),
            ("t2", "pPZFlxmfqrM", 312, "Bhangra: Aaja Billo")],
    credit=("Streamed from YouTube &mdash; not hosted by StudyVault. Ustad Tari Khan, tabla solo in teentaal "
            "(Darbar Festival); Balwinder Safri, &lsquo;Aaja Billo&rsquo;."))
TITLE = "India and Punjab — Guided Listening"

d.pins = [
    ("t1", "t1c1", 26,  "He says it first", "Before he plays the composition, Tari Khan speaks it: the bols, the spoken syllables that name each stroke."),
    ("t1", "t1c2", 52,  "Tabla and lehra",  "The solo proper begins and the harmonium starts its repeating melody, which keeps the 16-beat cycle audible."),
    ("t1", "t1c3", 83,  "Variations begin", "The opening theme starts to be varied systematically &mdash; a kaida and its paltas."),
    ("t1", "t1c4", 208, "Fastest point",    "The tempo and the density are at their highest here."),
    ("t1", "t1c5", 228, "The last stroke",  "The closing phrase lands and the audience applauds."),
    ("t2", "t2c1", 3,   "The groove drops", "The spoken sample ends and the whole modern rhythm section arrives at once."),
    ("t2", "t2c2", 23,  "The hook",         "The voice enters at about twelve seconds; by here the chorus hook has come round for the first time."),
    ("t2", "t2c3", 43,  "Tumbi exposed",    "An instrumental break where the one-stringed tumbi is clearly on top."),
    ("t2", "t2c4", 231, "Dhol break",       "Late in the track the singing stops and the drums take over."),
    ("t2", "t2c5", 278, "Final chorus",     "The last full statement of the hook before the ending."),
]

d.add_cover(
  "One region, two rhythmic systems",
  [
   "Track one is North Indian classical music: a solo on the %s, the pair of hand drums, in %s, the 16-beat cycle. "
   "Ustad Tari Khan is a Pakistani master of the %s, the Punjab school of tabla playing. Behind him a harmonium "
   "repeats a short melody so the cycle can always be counted. Everything you hear is measured against that cycle."
   % (dfn("tabla", "A pair of North Indian hand drums: the wooden dayan and the metal bayan"),
      dfn("teentaal", "The most common North Indian rhythmic cycle: 16 beats in four groups of four; also spelt tintal"),
      dfn("gharana", "A school or lineage of Indian musicians, each with its own repertoire and style")),
   "Track two is %s, the Punjabi folk music that became a British pop genre. &lsquo;Aaja Billo&rsquo; was released "
   "in 2000 by Balwinder Safri, founder of the Safri Boyz and one of the biggest names in UK bhangra. The double-"
   "headed %s drives it, and around the dhol sit a %s, a harmonium, synthesisers and a drum machine."
   % (dfn("bhangra", "A Punjabi harvest dance music, revived and modernised by British Asian bands from the 1980s"),
      dfn("dhol", "A large double-headed Punjabi barrel drum, played with two sticks of different weights"),
      dfn("tumbi", "A one-stringed Punjabi plucked instrument with a high, twanging sound")),
   "Press play and the cards follow the music. Use the track buttons to swap recordings, and tap any number to jump.",
  ], title="The tradition")

d.add_statement(1, "1 · He says it first", "1 &middot; Said before it is played",
  "Tari Khan talks to the audience and recites the composition out loud before he plays it. %s Those syllables are "
  "%s: each one names a particular stroke, so a tabla player can speak a piece as accurately as play it. It is how "
  "the repertoire is taught, and why the tradition needs no notation."
  % (d.ref(1), dfn("bols", "The spoken syllables that name tabla strokes, such as dha, dhin, na and tin")),
  "the same pattern spoken and then played. If you can hear the match, you have heard how the music is passed on.")

d.add_statement(2, "2 · Tabla and lehra", "2 &middot; The cycle starts turning",
  "The solo begins and the harmonium comes in with a short repeating melody, the %s. %s Its job is to mark the "
  "cycle so the tabla can leave it and come back. Find the steady pulse first, then find the strongest stroke: "
  "that is %s, beat one, where every cycle restarts. Count on and the heavy stroke returns after sixteen."
  % (dfn("lehra", "A short melody repeated over and over to mark the rhythmic cycle behind a solo; also called nagma"),
     d.ref(2), dfn("sam", "The first beat of a rhythmic cycle, the strongest point in it")),
  "the pulse first, then the strongest stroke. Count the beats between strong strokes to get the cycle length.")

d.add_statement(3, "3 · Variations begin", "3 &middot; A theme, then its variations",
  "The opening pattern is now being reworked. %s A %s is a short theme developed through a strict series of "
  "variations, or %s, which reorder and expand the bols while keeping the cycle exactly sixteen beats long. Beat "
  "nine is %s, the empty group: the low drum lifts off and the sound thins."
  % (d.ref(3), dfn("kaida", "A tabla theme and the systematic variations built from its syllables"),
     dfn("paltas", "The individual variations within a kaida"),
     dfn("khali", "The &lsquo;empty&rsquo; part of a cycle, marked by a wave rather than a clap and by a lighter stroke")),
  "the moment in each cycle where the bass drops out. That is khali, and it tells you where you are in sixteen.")

d.add_statement(4, "4 · Fastest point", "4 &middot; The tempo climbs",
  "This is the densest, fastest playing in the solo. %s Indian musicians call tempo %s, and a solo of this kind "
  "climbs steadily rather than jumping. The cycle has not changed length: the beats are simply closer together, "
  "and more strokes are being fitted between them."
  % (d.ref(4), dfn("laya", "Tempo, or the speed of the pulse, in Indian classical music")),
  "the cycle staying sixteen beats long while the pulse quickens. Speed is not the same as a change of metre.")

d.add_statement(5, "5 · The last stroke", "5 &middot; Landing on sam",
  "The solo closes with a %s: a phrase played three times so that its final stroke arrives exactly on sam. %s That "
  "is why the ending feels so decisive, and why the audience applauds on the beat. It is the standard way to "
  "finish a passage in this music, and naming it is worth a mark."
  % (dfn("tihai", "A phrase repeated three times so that its last stroke lands on beat one of the cycle"), d.ref(5)),
  "three repetitions of the same phrase, then a stroke that lands with the harmonium. Count them.")

d.add_statement(6, "1 · The groove drops", "1 &middot; Everything at once",
  "A spoken sample, then the whole rhythm section lands together. %s That is the first thing to say about modern "
  "bhangra: the dhol is played alongside a %s and synthesisers, so a folk drum from Punjab is sitting inside a "
  "studio-built dance track. The %s of technology on traditional music is examinable, and it is audible here."
  % (d.ref(6), dfn("drum machine", "An electronic instrument that plays programmed drum sounds"),
     dfn("impact", "How something changes as a result of another thing acting on it")),
  "two drum sounds at once: one struck by hand, one programmed. Name both.")

d.add_statement(7, "2 · The hook", "2 &middot; The chaal, and the swing",
  "The vocal comes in and the chorus hook comes round. %s Under it the dhol plays the %s, the eight-beat bhangra "
  "groove. Listen to the pairs of quick notes between the beats: they are not even. Each pair is long then short, "
  "a %s feel, and that lopsided lilt is what makes bhangra sound like bhangra."
  % (d.ref(7), dfn("chaal", "The characteristic eight-beat bhangra rhythm played on the dhol"),
     dfn("swung", "Pairs of quick notes played long-then-short rather than evenly")),
  "swing. Are the pairs of quick notes even, or is each pair long-short?")

d.add_statement(8, "3 · Tumbi exposed", "3 &middot; One string, high above",
  "An instrumental break, and the tumbi is clearly on top. %s It has a single string, plucked with one finger, and "
  "it plays repeating high figures rather than chords. Alongside it the dhol&rsquo;s two heads are doing different "
  "jobs: a thin stick on the treble head, a heavier one on the bass head. That is why one drum sounds like two."
  % d.ref(8),
  "the two sides of the dhol. High and dry on one head, deep and booming on the other.")

d.add_statement(9, "4 · Dhol break", "4 &middot; The drum takes over",
  "The singing stops and the percussion drives the track alone. %s In a live bhangra performance this is where the "
  "dancing takes over, and the modern recording keeps the shape even though nobody is dancing in a studio. The "
  "chaal is unchanged: what has been removed is the melody, not the groove."
  % d.ref(9),
  "the groove continuing untouched with the voice gone. The rhythm was never accompaniment.")

d.add_statement(10, "5 · Final chorus", "5 &middot; Round again",
  "The hook returns for the last time. %s Bhangra structure is built from repeats: verse, chorus, break, chorus, "
  "with %s sung couplets in the older folk style feeding the verses. The song does not develop in the way a "
  "Western pop song does; it circles, exactly as the tala circles in track one."
  % (d.ref(10), dfn("boliyan", "Short traditional Punjabi couplets sung over a bhangra groove")),
  "how little changes between one chorus and the next. Repetition is the structure, not a shortage of ideas.")

d.add_checklist(
  "Indian classical: tabla and harmonium; teentaal, 16 beats in four groups of four; sam on beat one, khali at "
  "beat nine; bols, kaida and paltas, tihai; lehra or nagma; laya rising through the solo; the Punjab gharana. "
  "Bhangra: dhol playing the eight-beat chaal with swung quavers; tumbi, harmonium, synthesisers, drum machine "
  "and studio production; boliyan; harvest-dance origins in Punjab and a British Asian revival from the 1980s. "
  "OCR asks for performers by name: Ustad Tari Khan and Balwinder Safri will both do.",
  "Do not mix up the two systems. Raga is melody, tala is rhythm, and chaal belongs to bhangra, not to classical "
  "music. And never stop at naming a feature: &ldquo;it uses a tala&rdquo; earns nothing, while &ldquo;the tabla "
  "plays a 16-beat teentaal cycle, with the bass lifting off at khali on beat nine&rdquo; earns the mark.")

content = d.content()

exam_tip = ("<p>Every question in this topic is answered by counting or by listening to how beats divide. Find the "
            "steady pulse first, then the strongest stroke, because cycles restart there; count the beats between "
            "strong strokes and you have the cycle length. Then ask whether pairs of quick notes are even or "
            "swung. Write description plus effect: &lsquo;the dhol plays a repeated chaal with swung quavers, "
            "which gives the dance its lolloping, off-beat drive&rsquo; scores where &lsquo;it has a chaal "
            "rhythm&rsquo; does not.</p>")
conclusion = ("<p>You can now count a 16-beat teentaal cycle from sam to sam, hear khali thin the sound at beat "
              "nine, follow a kaida into its variations and recognise a tihai landing on the beat; and you can "
              "hear the bhangra chaal underneath a modern production, name the dhol, tumbi and drum machine, and "
              "explain what studio technology has done to a Punjabi folk music.</p>")
description = ("Follow a teentaal tabla solo and a bhangra track landmark by landmark: sam, khali, kaida, tihai, "
               "and the swung chaal under a modern production.")

flashcards = [
 {"q": "What is a tala, and how many beats are there in teentaal?",
  "a": "A tala is the repeating rhythmic cycle of North Indian classical music. Teentaal has 16 beats, grouped as four fours."},
 {"q": "What do sam and khali mean?",
  "a": "Sam is beat one, the strongest point of the cycle, where every cycle restarts. Khali is the 'empty' section, at beat nine in teentaal, where the bass drum lifts off and the sound thins."},
 {"q": "What are bols?",
  "a": "The spoken syllables that name tabla strokes, such as dha, dhin, na and tin. Players recite a composition before playing it, which is how the repertoire is taught and memorised."},
 {"q": "What is a tihai?",
  "a": "A phrase repeated three times so that its final stroke lands exactly on sam, beat one. It is the standard way of closing a passage or a whole solo."},
 {"q": "Describe the chaal.",
  "a": "The characteristic eight-beat bhangra rhythm played on the dhol, with the quick notes between the beats swung long-short rather than played evenly."},
 {"q": "Name three ways modern technology has changed bhangra.",
  "a": "Drum machines and programmed percussion alongside the dhol; synthesisers replacing or doubling traditional melody instruments; multitrack studio recording, sampling and mixing, which allow a folk drum to sit inside a dance production."},
]

practice = [
 {"text": "State how many beats there are in teentaal and how they are grouped.", "marks": 2, "kind": "Identification",
  "mark_scheme": "1 mark: 16 beats. 1 mark: grouped as four groups of four."},
 {"text": "Explain what sam and khali are, and describe what you can hear at each.", "marks": 4, "kind": "Explanation",
  "mark_scheme": "Sam: beat one of the cycle (1), heard as the strongest stroke, where the cycle restarts and phrases land (1). Khali: the empty section, beat nine in teentaal (1), heard as a thinning of the sound because the bass drum lifts off (1)."},
 {"text": "What is a lehra, and why does a tabla soloist need one?", "marks": 3, "kind": "Explanation",
  "mark_scheme": "A short melody repeated over and over, usually on harmonium or sarangi (1). It marks out the cycle continuously (1) so that the soloist can depart from the basic pattern and still be heard to return to sam (1)."},
 {"text": "Describe the chaal, and explain how you would recognise it by ear.", "marks": 3, "kind": "Description",
  "mark_scheme": "An eight-beat bhangra rhythm played on the dhol (1). The pairs of quick notes between the beats are swung, long then short, rather than even (1). Recognised by the lopsided lilt and by the dhol's two contrasting drum sounds, high stick and deep stick (1)."},
 {"text": "Explain how modern technology has changed traditional Punjabi bhangra, referring to what you can hear.", "marks": 4, "kind": "Explanation",
  "mark_scheme": "Award up to 4 for: drum machine or programmed percussion layered with the acoustic dhol; synthesisers and keyboards added to or replacing traditional melody instruments; studio multitracking, sampling and mixing; the spoken or sampled introduction; the result heard as a folk drum inside a dance-pop production."},
 {"text": "Compare how the two recordings are structured.", "marks": 4, "kind": "Comparison",
  "mark_scheme": "Tabla solo: a single unbroken cycle of 16 beats repeating throughout, with theme and variations (kaida and paltas), rising tempo and a tihai to close (2). Bhangra: verse and chorus repeating, with instrumental and drum breaks, over an unchanging eight-beat chaal (2). Credit the point that both are cyclic rather than developmental."},
]

kcs = [
 {"q": "How many beats are there in teentaal?", "options": ["Seven", "Twelve", "Sixteen", "Eight"], "correct": 2},
 {"q": "What is sam?", "options": ["The empty section of the cycle", "The first beat of the cycle", "A three-fold cadence", "A drum syllable"], "correct": 1},
 {"q": "Which instrument plays the repeating lehra behind the tabla solo?", "options": ["Sitar", "Tumbi", "Harmonium", "Tanpura"], "correct": 2},
 {"q": "The chaal is the characteristic rhythm of which music?", "options": ["Hindustani classical", "Bhangra", "Carnatic classical", "Qawwali"], "correct": 1},
 {"q": "How are the pairs of quick notes treated in the chaal?", "options": ["Evenly", "Swung, long then short", "Swung, short then long", "Played as triplets"], "correct": 1},
]

related_media = [
 {"category": "Videos & Channels", "items": [
   {"url": "https://www.youtube.com/watch?v=6YWnqKbTSxY",
    "title": "darbarfestival — Tabla Solo in Drut Tintal, Pandit Sanju Sahai",
    "description": "The same 16-beat cycle at speed, in a different gharana. Good for comparing styles."},
   {"url": "https://www.youtube.com/watch?v=tw_IH7NIPzw",
    "title": "darbarfestival — Dhir Dhir, tintal tabla solo, Gurdain Rayatt",
    "description": "A longer solo that explains its own bols as it goes, then develops them."},
   {"url": "https://www.youtube.com/@DarbarFestival",
    "title": "Darbar Festival",
    "description": "Indian classical performances filmed in concert: sitar, sarod, bansuri, tabla and voice."},
   {"url": "https://www.youtube.com/watch?v=eUsK2I8dLyI",
    "title": "Kuljit Bhamra — The Dhol Express",
    "description": "Dhol alone, with no production around it: the clearest chaal you will find."}]},
 {"category": "Reference", "items": [
   {"url": "https://www.britannica.com/art/tala",
    "title": "Britannica — Tala",
    "description": "How rhythmic cycles work in Indian music, including sam, vibhag and khali."},
   {"url": "https://www.britannica.com/art/bhangra",
    "title": "Britannica — Bhangra",
    "description": "Harvest-dance origins in Punjab and the British Asian revival."}]},
]

# ---- build, verify, patch ---------------------------------------------------
pq = [{"text": q["text"], "type": "%d mark%s — %s" % (q["marks"], "" if q["marks"] == 1 else "s", q["kind"]),
       "marks": q["mark_scheme"]} for q in practice]
kc = [{"q": q["q"], "type": "mcq", "correct": q["correct"], "options": q["options"]} for q in kcs]
fc = [{"q": f["q"], "a": f["a"]} for f in flashcards]

errs, warns = d.verify(content, (exam_tip or "") + (conclusion or ""))
allids = [int(x) for x in re.findall(r'data-narration-id="n(\d+)"', content + exam_tip + conclusion)]
if allids != list(range(1, len(allids) + 1)):
    errs.append("narration ids across content+tip+conclusion not contiguous")
for o, lbl in ((pq, "practice"), (kc, "kc"), (fc, "flashcards")):
    check_plain(o, lbl, errs)
if len(description) > 160:
    errs.append("description %d chars" % len(description))
print("cards", len(d.cards), "| pins", len(d.pins), "| narration ids", d._n, "| chars", len(content),
      "| desc", len(description))
print("card words", d.card_words)
for w in warns:
    print("WARN", w)
if errs:
    print("ERRORS:")
    for e in errs:
        print("  -", e)
    raise SystemExit(1)
print("verify OK")

payload = {"title": TITLE, "content_html": content, "exam_tip_html": exam_tip,
           "conclusion_html": conclusion, "description": description,
           "flashcard_questions": fc, "practice_questions": pq, "knowledge_checks": kc,
           "related_media": related_media, "youtube_video_id": None,
           "practice_data": None, "narration_manifest": None}
io.open(os.path.join(HERE, "html", "ocr_l1_india.html"), "w", encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
