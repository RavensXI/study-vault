# -*- coding: utf-8 -*-
"""music-ocr / aos3-rhythms-listening / L3 -- African Drumming.

Rebuilt from a PRACTICE row (synthesised-click problem bank) into a guided
listening lesson on two real recordings, per Tom's decision 7 Sep 2026.

Recordings, both verified: oEmbed 200, yt-dlp playable_in_embed True, age 0,
and loaded without error in a real YouTube IFrame player on the studyvault.co.uk
origin (durations below are that player's own getDuration).

  t1  7-CEt1XQ2A4  292 s  Famoudou Konate with Ensemble Hamana Dan Ba, "Matadi"
                          (Famoudou Konate - Topic, label release). Malinke
                          ensemble from Guinea: lead djembe, dundun family with
                          bells, call-and-response singing.
  t2  oToZfPGMMBY  337 s  Sona Jobarteh, "Jarabi" (BBC News Africa). Kora with
                          guitar and calabash percussion, sung.

Pin times: 3-vote Gemini consensus, timings.json keys ocr_l3_t1 / ocr_l3_t1b /
ocr_l3_t1c / ocr_l3_t2 / ocr_l3_t2b. Every pin below carries at least 2 of 3
agreeing votes. Dropped for want of corroboration: t2 "groove_established"
(votes 78 / 5 / 30) and the t1 5 s "ensemble locks in" pin, which sat 1.7% from
the 0 s pin and would have overlapped it on the scrub bar.
"""
import io, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck_multi import MultiDeck, dfn, patch, check_plain

BACKUP = "music-ocr__aos3-rhythms-listening__L03"
HERE = os.path.dirname(os.path.abspath(__file__))
old = json.load(io.open(os.path.join(HERE, "backups", BACKUP + ".json"), encoding="utf-8"))

d = MultiDeck(
    lesson_id=old["id"], subject="music-ocr", unit="aos3-rhythms-listening", lesson_no=3,
    tracks=[("t1", "7-CEt1XQ2A4", 292, "Malinke ensemble"),
            ("t2", "oToZfPGMMBY", 337, "Kora: Jarabi")],
    credit=("Streamed from YouTube &mdash; not hosted by StudyVault. Famoudou Konat&eacute; with Ensemble "
            "Hamana Dan Ba, &lsquo;Matadi&rsquo;; Sona Jobarteh, &lsquo;Jarabi&rsquo; (BBC News Africa)."))
TITLE = "African Drumming — Guided Listening"

d.pins = [
    ("t1", "t1c1", 0,   "The call",          "The lead djembe calls alone; within five seconds the bells and the three dundun drums have all entered."),
    ("t1", "t1c2", 65,  "Lead voice",        "A solo singer calls a phrase and the group answers &mdash; call and response, over an unbroken drum groove."),
    ("t1", "t1c3", 127, "Djembe solo",       "The lead drummer improvises across the top while every accompanying pattern stays exactly as it was."),
    ("t1", "t1c4", 177, "The song returns",  "Back to the sung section. The piece alternates song and solo; nothing here is written down."),
    ("t1", "t1c5", 239, "The texture thins", "Parts drop away and the lead drum is left with a much lighter accompaniment."),
    ("t1", "t1c6", 285, "All stop together", "The ensemble ends on a signal from the lead drummer, not on a counted bar."),
    ("t2", "t2c1", 0,   "Kora alone",        "Twenty-one strings over a calabash gourd. The repeating accompaniment pattern is the kumbengo."),
    ("t2", "t2c2", 22,  "The band joins",    "Guitar and calabash percussion layer in on top of the kora &mdash; the same building principle as the drum ensemble."),
    ("t2", "t2c3", 101, "The jeli sings",    "The voice enters. In Mande tradition the kora player is a jeli: musician, praise singer and keeper of history."),
    ("t2", "t2c4", 249, "Improvised flight", "An instrumental passage where the kora breaks into fast decorative runs above the pattern: birimintingo."),
    ("t2", "t2c5", 329, "The close",         "The song ends by winding the pattern down rather than with a Western cadence."),
]

d.add_cover(
  "Layers that lock together",
  [
   "Two West African traditions sit side by side here. Track one is %s drumming from Guinea: a lead %s, the three "
   "%s drums with bells fixed to them, and singers. Track two is the %s, the 21-string harp of the Mande %s "
   "families, played by Sona Jobarteh of the Gambia. Both are learnt by ear and handed on by %s."
   % (dfn("Malinke", "A West African people of Guinea, Mali and neighbouring countries; also spelled Malinke or Maninka"),
      dfn("djembe", "A goblet-shaped West African drum played with bare hands, giving bass, tone and slap sounds"),
      dfn("dundun", "A family of cylindrical West African bass drums played with sticks, usually with a bell attached"),
      dfn("kora", "A 21-string West African harp with a large calabash gourd resonator"),
      dfn("jeli", "A hereditary Mande musician, praise singer and oral historian; also called a griot"),
      dfn("oral tradition", "Music passed on by ear and by imitation rather than through written notation")),
   "The method is the same in both. Short repeating patterns, %s, are stacked one on another. Because the layers "
   "group the same bar in different ways they pull against each other &mdash; that is %s, and where two groupings "
   "collide head on it is %s. A lead player calls the music in, signals the changes and improvises above it."
   % (dfn("ostinati", "Short patterns repeated over and over; the plural of ostinato"),
      dfn("polyrhythm", "Two or more different rhythms sounding at the same time"),
      dfn("cross rhythm", "Two conflicting groupings of the same bar, such as three against two")),
   "Press play and the cards follow the music. Use the track buttons to swap recordings, and tap any number to jump.",
  ], title="The tradition")

d.add_statement(1, "1 · The call", "1 &middot; The call, then the layers",
  "The lead djembe opens alone with a short call. %s That phrase is the signal to start, and within five seconds "
  "the bells and the three dunduns &mdash; %s, %s and %s &mdash; have entered and the groove is running. The pulse "
  "is %s: every beat splits into three, so the music rolls rather than marches."
  % (d.ref(1), dfn("dundunba", "The largest and lowest dundun drum"),
     dfn("sangban", "The middle-sized dundun drum, which usually carries the key pattern"),
     dfn("kenkeni", "The smallest and highest dundun drum, holding the steadiest pattern"),
     dfn("compound", "A metre in which each beat divides into three rather than two")),
  "the ORDER in which the layers enter. Follow one layer at a time before you judge the whole texture.")

d.add_statement(2, "2 · Lead voice", "2 &middot; Call and response",
  "A single voice sings a phrase and the group answers with a fixed reply. %s That alternation is %s, and it is "
  "not only a vocal device: the lead drummer calls and the ensemble answers in exactly the same way. Underneath, "
  "the accompanying drum patterns carry on unchanged, so the answer always lands in the same place."
  % (d.ref(2), dfn("call and response", "One performer sings or plays a phrase and another performer or group answers it")),
  "alternation, not accumulation. One voice, then the group, over a drum pattern that never breaks.")

d.add_statement(3, "3 · Djembe solo", "3 &middot; The master drummer takes over",
  "The lead djembe pulls clear of the ensemble and improvises. %s Listen to how the accompaniment behaves: the "
  "bell, the dunduns and the second djembe repeat their ostinati exactly as before. That is the point of an "
  "ostinato-based texture. Because the ground stays fixed, the solo can cut across it and the %s stays audible."
  % (d.ref(3), dfn("cross rhythm", "Two conflicting groupings of the same bar, such as three against two")),
  "conflicting groupings of the same bar. The solo is measured against the layers, not against a conductor.")

d.add_statement(4, "4 · The song returns", "4 &middot; Song, solo, song",
  "The singing comes back and the drums drop into their supporting role. %s The structure of the whole piece is "
  "this alternation of sung sections and drum solos, and there is no score deciding when each one arrives. The "
  "lead drummer signals the changes, the ensemble hears them and follows. That is oral tradition working live."
  % d.ref(4),
  "the join between solo and song. Somebody cued it, and the cue is audible in the lead drum.")

d.add_statement(5, "5 · The texture thins", "5 &middot; The texture thins",
  "Parts fall away and the lead drum is left with far less around it. %s %s is the exam word here, and it is the "
  "easiest mark in the topic to score badly: say which layers stopped and which carried on. A thinned texture in "
  "this music is a deliberate structural event, not a mistake or a fade."
  % (d.ref(5), dfn("Texture", "How many layers of sound there are and how they relate to each other")),
  "which parts drop out. Name them, and name what is left.")

d.add_statement(6, "6 · All stop together", "6 &middot; Everyone stops together",
  "The piece ends with the whole ensemble stopping on the same stroke. %s Nobody counted a final bar: the lead "
  "drummer played a break that the players recognise, and they finished on it. In an answer about how these "
  "musicians work together, that ending is your strongest single piece of evidence."
  % d.ref(6),
  "the break that warns the ending is coming, and the exactness of the stop that follows it.")

d.add_statement(7, "1 · Kora alone", "1 &middot; Twenty-one strings",
  "The kora plays alone. %s It has 21 strings running over a bridge above a %s resonator, and the player plucks "
  "with both thumbs and both index fingers, so one pair of hands can hold a bass line, a repeating pattern and a "
  "melody at once. The pattern you can hear looping is the %s."
  % (d.ref(7), dfn("calabash", "A large dried gourd, cut and covered with skin to make a resonating body"),
     dfn("kumbengo", "The repeating accompaniment pattern that a kora player holds under a song")),
  "one player producing several layers. The kumbengo is an ostinato, exactly like the drum patterns opposite.")

d.add_statement(8, "2 · The band joins", "2 &middot; Adding parts",
  "Guitar and %s percussion come in over the kora. %s The principle is the one you met in track one: the music "
  "grows by adding layers to an ostinato that is already running, not by changing key or theme. Notice that the "
  "kora keeps its kumbengo going underneath the moment the others arrive."
  % (dfn("calabash", "A large dried gourd, here struck as a percussion instrument"), d.ref(8)),
  "how texture builds with added parts. Say which instrument enters, and over what.")

d.add_statement(9, "3 · The jeli sings", "3 &middot; The jeli sings",
  "The voice enters. %s Sona Jobarteh comes from one of the Gambia&rsquo;s principal %s families, and she is among "
  "the first women to perform professionally on an instrument traditionally handed from father to son. A jeli is a "
  "musician, a praise singer and an oral historian, which is why this repertoire carries so much history in it."
  % (d.ref(9), dfn("griot", "A hereditary West African musician, praise singer and keeper of oral history")),
  "the voice riding over a pattern that never stops. The kora does not pause to accompany it.")

d.add_statement(10, "4 · Improvised flight", "4 &middot; Birimintingo",
  "The singing stops and the kora breaks into fast decorative runs above the accompaniment. %s That improvised "
  "flourishing is called %s, and it is the counterpart of the master drummer&rsquo;s solo: a fixed ground beneath, "
  "invention on top. Both traditions build their solos the same way."
  % (d.ref(10), dfn("birimintingo", "The improvised, decorative solo runs a kora player plays above the kumbengo")),
  "the kumbengo continuing underneath the runs. If it stopped, this would not be birimintingo.")

d.add_statement(11, "5 · The close", "5 &middot; Winding down",
  "The performance ends by letting the pattern run out rather than by a Western %s. %s Structure in this music is "
  "cyclic: sections are as long as the players decide, and the end is agreed in performance. Saying so, and giving "
  "the evidence, is worth more than naming a form that was never used here."
  % (dfn("cadence", "A chord progression that closes a phrase or piece in Western music"), d.ref(11)),
  "the absence of a final chord. The music stops; it does not resolve.")

d.add_checklist(
  "Instruments: lead djembe (bass, tone and slap), dundunba, sangban and kenkeni with attached bells, and the "
  "21-string kora over a calabash. Rhythm and metre: compound pulse, ostinato layers, polyrhythm and cross rhythm. "
  "Texture: layered, built by adding parts, thinned deliberately. Structure: cyclic, alternating song and solo, "
  "with no notation. Devices: call and response, improvised djembe solos, kumbengo and birimintingo. Context: "
  "Malinke ensemble music from Guinea, and the hereditary jeli or griot tradition of the Mande world.",
  "Marks come from mechanism, not atmosphere. &ldquo;It sounds tribal&rdquo; earns nothing. &ldquo;The bell plays "
  "an unchanging timeline while the lead djembe improvises across it, so the two groupings cross&rdquo; earns the "
  "mark, because it names the parts, says what each is doing and says how they relate.")

content = d.content()

exam_tip = ("<p>When a question asks how this music is put together, answer in the order the sound arrives: which "
            "instrument starts, which layers are added and in what order, what each layer repeats, and who changes "
            "it. Examiners reward the mechanism &mdash; ostinato, polyrhythm, cross rhythm, call and response, "
            "layered build &mdash; tied to a moment you can point to. Avoid the words &lsquo;tribal&rsquo; and "
            "&lsquo;primitive&rsquo;: they describe nothing and cost you the register marks.</p>")
conclusion = ("<p>You can now follow a Malinke drum ensemble from the lead djembe&rsquo;s call through its layered "
              "entries, call-and-response singing, master-drummer solos and cued ending, and you can hear the same "
              "ostinato-plus-improvisation principle at work in a kora performance, where kumbengo carries "
              "birimintingo. Name the instruments, the order of entries and the devices, and this becomes one of "
              "the most answerable topics on the listening paper.</p>")
description = ("Follow a Malinke drum ensemble and a kora performance landmark by landmark: layered entries, call "
               "and response, cross rhythm and improvised solos.")

flashcards = [
 {"q": "Name the three drums of the dundun family, from lowest to highest.",
  "a": "Dundunba (largest and lowest), sangban (middle) and kenkeni (smallest and highest). Each usually has a bell attached, played by the same performer."},
 {"q": "What are the three main sounds of a djembe?",
  "a": "Bass, played in the centre with the flat hand; tone, played at the edge with the fingers together; and slap, a sharper, higher crack at the edge."},
 {"q": "What is the difference between polyrhythm and cross rhythm?",
  "a": "Polyrhythm means several different rhythms sounding at once. Cross rhythm is the sharper case where two parts group the same bar in conflicting ways, such as three against two."},
 {"q": "What does the master drummer do in a West African drum ensemble?",
  "a": "Calls the ensemble in, signals changes of section, improvises solos over the unchanging ostinati, and cues the ending. The other parts repeat their patterns underneath."},
 {"q": "What is a kora, and how is it played?",
  "a": "A 21-string West African harp with a large calabash resonator. The player plucks with both thumbs and both index fingers, holding a bass line, a repeating pattern and a melody at once."},
 {"q": "Define kumbengo and birimintingo.",
  "a": "Kumbengo is the repeating accompaniment pattern a kora player holds under a song. Birimintingo is the improvised decorative runs played above it."},
]

practice = [
 {"text": "Name the instrument that opens the Malinke recording and state what its opening phrase does.", "marks": 2, "kind": "Identification",
  "mark_scheme": "1 mark: the lead djembe. 1 mark: it plays a call or signal that starts the piece and brings the other parts in."},
 {"text": "Describe how the texture of the Malinke ensemble is built in the first ten seconds.", "marks": 3, "kind": "Description",
  "mark_scheme": "Credit: lead djembe alone first; bells and dundun drums added; layers accumulate over a repeating ostinato until the full groove is running. Award up to 3 for naming parts and the order of entry."},
 {"text": "Explain the difference between polyrhythm and cross rhythm, using this music as your example.", "marks": 4, "kind": "Explanation",
  "mark_scheme": "Polyrhythm: several different rhythms sounding at once (1). Cross rhythm: two parts grouping the same bar in conflicting ways, e.g. three against two (1). Applied example: the bell or dundun ostinato against the improvising djembe (1). Reference to the ostinati staying fixed so the conflict is audible (1)."},
 {"text": "Describe two ways in which call and response is used in the Malinke recording.", "marks": 2, "kind": "Description",
  "mark_scheme": "1 mark each, up to 2: a solo singer answered by the group chorus; the lead drummer calling and the ensemble answering; a drum phrase answered by a fixed response pattern."},
 {"text": "Explain how a kora player produces several musical layers at once.", "marks": 3, "kind": "Explanation",
  "mark_scheme": "Credit: 21 strings arranged over a bridge on both sides (1); plucked with both thumbs and both index fingers (1); the thumbs hold bass and the repeating kumbengo while the fingers take melody or improvised birimintingo (1)."},
 {"text": "This music is passed on by oral tradition. Give two features of the performances that show this.", "marks": 2, "kind": "Explanation",
  "mark_scheme": "1 mark each, up to 2: sections are of no fixed length and are cued in performance; the ending is signalled by the lead player rather than counted; solos are improvised; players respond to signals rather than reading notation."},
]

kcs = [
 {"q": "Which drum leads a Malinke ensemble and plays the improvised solos?", "options": ["Kenkeni", "Djembe", "Sangban", "Kora"], "correct": 1},
 {"q": "What is an ostinato?", "options": ["A sudden change of key", "A short pattern repeated over and over", "A free improvisation", "A three-against-two rhythm"], "correct": 1},
 {"q": "How many strings does a kora have?", "options": ["Six", "Twelve", "Twenty-one", "Forty-seven"], "correct": 2},
 {"q": "What is the correct term for the repeating accompaniment pattern in kora playing?", "options": ["Birimintingo", "Kumbengo", "Kenkeni", "Tala"], "correct": 1},
 {"q": "In Mande tradition, what is a jeli or griot?", "options": ["A type of drum", "A hereditary musician, praise singer and oral historian", "A festival held after harvest", "A repeating bell pattern"], "correct": 1},
]

related_media = [
 {"category": "Videos & Channels", "items": [
   {"url": "https://www.youtube.com/watch?v=TD3PXm9B8H8",
    "title": "Christian Vogler — Famoudou Konaté: 'Soli' (Rhythms of the Malinké, 1990)",
    "description": "Archive film of the same master drummer with his ensemble: bell, dunduns and djembe solos in close-up."},
   {"url": "https://www.youtube.com/watch?v=xHDvwWBJ0NQ",
    "title": "andymcgraw — Agbekor (slow)",
    "description": "An Ewe ensemble from Ghana: the gankogui bell timeline underneath the whole performance."},
   {"url": "https://www.youtube.com/watch?v=J4RniuafFiI",
    "title": "Toumani Diabaté — Djelika",
    "description": "Kora with balafon and ngoni. Compare its kumbengo and birimintingo with the Jarabi track."},
   {"url": "https://www.youtube.com/watch?v=Ig91Z0-rBfo",
    "title": "University of Music FRANZ LISZT Weimar — Sona Jobarteh and Band",
    "description": "A full concert if you want more of the kora in an ensemble setting."}]},
 {"category": "Reference", "items": [
   {"url": "https://www.britannica.com/art/African-music",
    "title": "Britannica — African music",
    "description": "Background on ensemble drumming, oral transmission and the social role of musicians."},
   {"url": "https://www.bbc.co.uk/bitesize/subjects/zpsvr82",
    "title": "BBC Bitesize — GCSE Music",
    "description": "Revision notes on world music features for the listening paper."}]},
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
io.open(os.path.join(HERE, "html", "ocr_l3_africa.html"), "w", encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
