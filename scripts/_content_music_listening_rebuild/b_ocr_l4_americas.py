# -*- coding: utf-8 -*-
"""music-ocr / aos3-rhythms-listening / L4 -- Samba, Calypso and the Americas.

Rebuilt from a PRACTICE row into a guided listening lesson on two real
recordings, per Tom's decision 7 Sep 2026.

Recordings, both verified: oEmbed 200, yt-dlp playable_in_embed True, age 0,
and loaded without error in a real YouTube IFrame player on the studyvault.co.uk
origin (durations below are that player's own getDuration).

  t1  2dGbBoQNeCU  274 s  Monobloco Oficial: "Peguei Um Ita No Norte (Explode
                          Coracao)" live, DVD 2010. Salgueiro's 1993
                          samba-enredo played by a full Rio bateria.
  t2  BWcwonrBw0w  498 s  TrinidadAllStars (official channel): "Curry Tabanca",
                          their International Panorama winning arrangement by
                          Leon "Smooth" Edwards of Winsford Devine's calypso.

Pin times: 3-vote Gemini consensus, timings.json keys ocr_l4_t1 / ocr_l4_t1b /
ocr_l4_t2 / ocr_l4_t2b; every pin carries at least 2 of 3 agreeing votes.
Dropped for want of corroboration: t1 "percussion_only_section" (0 / 13 / 225)
and t1 "big_break" (225 / 232); t2 "quiet_or_thinned_passage" (199 / 374).
Merged: t1 "full_bateria_entry" at 2 s into the 0 s pin, and t2
"full_band_and_engine_room" at 20 s into the 19 s pin -- both would have
overlapped their neighbour on the scrub bar.
"""
import io, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck_multi import MultiDeck, dfn, patch, check_plain

BACKUP = "music-ocr__aos3-rhythms-listening__L04"
HERE = os.path.dirname(os.path.abspath(__file__))
old = json.load(io.open(os.path.join(HERE, "backups", BACKUP + ".json"), encoding="utf-8"))

d = MultiDeck(
    lesson_id=old["id"], subject="music-ocr", unit="aos3-rhythms-listening", lesson_no=4,
    tracks=[("t1", "2dGbBoQNeCU", 274, "Samba bateria"),
            ("t2", "BWcwonrBw0w", 498, "Steelband calypso")],
    credit=("Streamed from YouTube &mdash; not hosted by StudyVault. Monobloco, &lsquo;Peguei Um Ita No "
            "Norte&rsquo; (live, 2010); Trinidad All Stars Steel Orchestra, &lsquo;Curry Tabanca&rsquo;."))
TITLE = "Samba, Calypso and the Americas — Guided Listening"

d.pins = [
    ("t1", "t1c1", 0,   "The bateria starts", "A whistle and a calling drum bring the whole percussion band in together within two seconds."),
    ("t1", "t1c2", 23,  "Voices join",        "The sung samba-enredo enters over the groove; the crowd takes the refrain with the singer."),
    ("t1", "t1c3", 51,  "The band breaks",    "A break: the whole bateria plays a figure together instead of the groove, then drops straight back in."),
    ("t1", "t1c4", 100, "Next verse",         "A later verse. The percussion pattern is unchanged &mdash; the song moves on, the groove does not."),
    ("t1", "t1c5", 234, "Final refrain",      "The last full statement of the refrain, with the whole crowd singing it."),
    ("t2", "t2c1", 19,  "Pans enter",         "After the stage announcement the orchestra begins, engine room included, from the first bar."),
    ("t2", "t2c2", 68,  "The calypso tune",   "The first clear statement of the calypso melody itself, high in the tenor pans."),
    ("t2", "t2c3", 152, "New section",        "A fresh section of the arrangement: same tune, reworked material around it."),
    ("t2", "t2c4", 374, "Key change",         "The arrangement lifts into a new key &mdash; a Panorama trademark."),
    ("t2", "t2c5", 426, "Strumming",          "The middle pans take over with repeated strummed chords rather than the melody."),
    ("t2", "t2c6", 477, "The finish",         "The closing chords, and the crowd."),
]

d.add_cover(
  "Two carnivals, one rhythmic idea",
  [
   "Both recordings are carnival music, and both are built on %s inside a duple frame. Track one is a Rio de "
   "Janeiro %s: the percussion band of a samba parade. The song is Salgueiro&rsquo;s 1993 %s, &lsquo;Peguei Um Ita "
   "No Norte&rsquo;, played here live by the Rio group Monobloco. Track two is a %s from Trinidad."
   % (dfn("syncopation", "Accents placed off the main beats, against the pulse"),
      dfn("bateria", "The percussion section of a Brazilian samba school, from a dozen to several hundred players"),
      dfn("samba-enredo", "The theme song written for a samba school&rsquo;s carnival parade each year"),
      dfn("steelband", "A Trinidadian orchestra of tuned steel pans, made originally from oil drums")),
   "The Trinidad All Stars are playing their %s arrangement of &lsquo;Curry Tabanca&rsquo;, a %s by Winsford "
   "Devine, arranged for the band by Leon &lsquo;Smooth&rsquo; Edwards. Calypso carries news, gossip and political "
   "comment in its words; the steelband takes the tune and rebuilds it for a competition stage."
   % (dfn("Panorama", "Trinidad and Tobago&rsquo;s national steelband competition, held at carnival"),
      dfn("calypso", "A Trinidadian song style with strong syncopation and topical, often satirical, words")),
   "Press play and the cards follow the music. Use the track buttons to swap recordings, and tap any number to jump.",
  ], title="The tradition")

d.add_statement(1, "1 · The bateria starts", "1 &middot; The whole band, at once",
  "A whistle and the %s, the leader&rsquo;s calling drum, bring the band in. %s Within two seconds everything is "
  "playing: %s on the beat and the deepest one answering, %s cutting semiquavers across the top, %s bells, %s and "
  "shakers. Confirm the metre first. This is duple, two beats in a bar."
  % (dfn("repinique", "A small, high-pitched Brazilian drum used by the leader to call and cue the band"), d.ref(1),
     dfn("surdos", "The large bass drums of a bateria, played in two or three tuned sizes"),
     dfn("tamborins", "Small, shallow Brazilian frame drums struck with a flexible beater"),
     dfn("agogo", "A pair of tuned metal bells struck with a stick"),
     dfn("caixa", "The Brazilian snare drum of a bateria")),
  "which beat the deepest drum owns. In samba the low surdo answers on the second beat, not the first.")

d.add_statement(2, "2 · Voices join", "2 &middot; The song arrives",
  "The singing enters over a groove that does not change to accommodate it. %s A samba-enredo is written to be "
  "sung by thousands of people while they walk, so the tune is simple, the range is narrow and the refrain comes "
  "round quickly. Listen to how fast the crowd joins in: that is %s in a stadium."
  % (d.ref(2), dfn("call and response", "One performer sings a phrase and a group answers it")),
  "the percussion carrying on underneath, unaltered. The song sits on the groove; it does not lead it.")

d.add_statement(3, "3 · The band breaks", "3 &middot; The break",
  "The groove stops and the whole bateria plays one figure together, then drops back in as if nothing happened. "
  "%s Brazilians call this a %s or %s. It is rehearsed, cued by the leader, and it is the clearest evidence you "
  "can give that a bateria is one instrument played by many people."
  % (d.ref(3), dfn("break", "A short passage where the whole band plays a written figure instead of the groove"),
     dfn("paradinha", "Literally &lsquo;little stop&rsquo;: a rehearsed pause or unison figure in a samba groove")),
  "everybody stopping on the same semiquaver. Nobody drifts, because the leader called it.")

d.add_statement(4, "4 · Next verse", "4 &middot; The groove does not move",
  "A later verse of the song. %s Compare it with the first: the words and the melody have moved on, the "
  "percussion has not. Samba structure is a repeating %s under a song in verses and refrains, and the interest "
  "comes from the breaks, the singers and the sheer weight of the band, not from the pattern changing."
  % (d.ref(4), dfn("ostinato", "A short pattern repeated over and over")),
  "3+3+2 accents pulling against the steady pulse while everything else stays put.")

d.add_statement(5, "5 · Final refrain", "5 &middot; The refrain, everybody",
  "The last full statement of the refrain, sung by the whole crowd. %s In a parade this is what the judges and the "
  "public hear most, so a samba-enredo is judged partly on how singable its refrain is. Structure worth naming: "
  "introduction, verse, refrain, break, verse, refrain &mdash; strophic, with the bateria constant throughout."
  % d.ref(5),
  "the density at the end. More voices, the same groove, and a surdo still answering on beat two.")

d.add_statement(6, "1 · Pans enter", "1 &middot; A hundred oil drums",
  "The announcement finishes and the orchestra starts. %s Steel pans are tuned from oil drums, sunk and hammered "
  "into note patterns; a large band has tenor pans on the melody, double seconds and %s in the middle, and %s "
  "underneath. Behind them the %s &mdash; irons, scratcher and drum kit &mdash; keeps the rhythm."
  % (d.ref(6), dfn("cellos", "Middle-range steel pans, usually playing chords and counter-melody"),
     dfn("bass pans", "The lowest steel pans, several drums to a player, playing the bass line"),
     dfn("engine room", "The rhythm section of a steelband: brake-drum irons, scratcher and drum kit")),
  "the irons cutting through the pans. That metallic pulse is the engine room, and it never stops.")

d.add_statement(7, "2 · The calypso tune", "2 &middot; The tune itself",
  "The calypso melody arrives, high in the tenor pans. %s Calypso came out of Trinidad&rsquo;s carnival and out of "
  "West African %s song; the words carry news, teasing and political comment, and a %s can make a national "
  "argument in a chorus. Here the words are gone and the tune alone has to carry it."
  % (d.ref(7), dfn("call and response", "One singer leads a phrase and a group answers it"),
     dfn("calypsonian", "A calypso singer-songwriter, usually performing under a stage name")),
  "syncopation in the tune: the melody notes land between the beats the irons are marking.")

d.add_statement(8, "3 · New section", "3 &middot; Variation, not repetition",
  "A new section of the arrangement. %s A Panorama piece takes a calypso lasting three minutes and rebuilds it "
  "into eight: new counter-melodies, new %s, changes of key and changes of texture. The tune stays recognisable "
  "and everything around it is rewritten."
  % (d.ref(8), dfn("countermelody", "A second melody played at the same time as the main tune")),
  "the tune underneath the new material. Say what has changed around it, and what has not.")

d.add_statement(9, "4 · Key change", "4 &middot; The lift",
  "The whole band lifts into a new key. %s A %s late in a Panorama arrangement is a standard device: it raises the "
  "excitement without changing the tune, and on a stage with no amplification it is the loudest thing an arranger "
  "can do. Name the effect and the reason, not just the fact."
  % (d.ref(9), dfn("modulation", "A change of key")),
  "the same melody suddenly sitting higher and brighter. Everything moves up together.")

d.add_statement(10, "5 · Strumming", "5 &middot; Strumming",
  "The middle pans take the foreground with repeated strummed chords rather than the melody. %s This is where a "
  "steelband sounds least like an orchestra and most like a giant guitar section: the %s is chordal and rhythmic "
  "at once, with the melody instruments answering around it."
  % (d.ref(10), dfn("texture", "How many layers of sound there are and how they relate to each other")),
  "chords on the off-beats. The strumming is a rhythm part as much as a harmony part.")

d.add_statement(11, "6 · The finish", "6 &middot; The finish",
  "The arrangement drives to its closing chords and the crowd takes over. %s Both recordings end the same way: "
  "not with a fade, but with a full ensemble stop that everybody has rehearsed. In carnival music the ending is "
  "part of the performance, because a competition is being won or lost on it."
  % d.ref(11),
  "the last chord and how tightly it is placed. Then compare it with how the samba track ends.")

d.add_checklist(
  "Samba: 2/4, semiquaver subdivision, surdo answering on beat two, tamborim, agogo, caixa, repinique and ganza; "
  "a bateria of a samba school playing a strophic samba-enredo with rehearsed breaks. Calypso and steelband: "
  "duple metre with heavy syncopation and 3+3+2 accents; tenor pans, double seconds, cellos and bass pans, with "
  "an engine room of irons, scratcher and kit; Panorama arrangements add countermelodies, strumming sections and "
  "a late key change. Context: both are carnival music, both African-descended, both competitive.",
  "The marks are in the detail. &ldquo;It is lively and syncopated&rdquo; earns nothing. &ldquo;The low surdo "
  "answers on the second beat while the tamborims cut semiquavers across it&rdquo; earns the mark, because it "
  "names the instrument, the beat and the relationship between the two.")

content = d.content()

exam_tip = ("<p>Confirm the metre before you write anything else: both of these dances are duple, and half of the "
            "wrong answers in this topic start by calling samba a triple-time dance. Then find the deepest drum "
            "and say which beat it owns, and listen for 3+3+2 accents pulling against the pulse. If you are asked "
            "to compare the two traditions, compare mechanisms &mdash; who keeps the pulse, who syncopates against "
            "it, how the ensemble is cued &mdash; rather than listing instruments.</p>")
conclusion = ("<p>You can now hear a Rio bateria from its opening call through its breaks and refrains, and follow "
              "a Panorama steelband arrangement through its statement of the calypso, its new sections, its key "
              "change and its strumming. Name the instruments, the duple metre, the syncopation and the 3+3+2 "
              "grouping, and say who in the ensemble is doing what.</p>")
description = ("Follow a Rio samba bateria and a Trinidad steelband landmark by landmark: surdo on beat two, "
               "breaks, syncopation and a Panorama key change.")

flashcards = [
 {"q": "What is a bateria, and what is the surdo's job in it?",
  "a": "The percussion band of a Brazilian samba school. The surdos are its bass drums, played in two or three tuned sizes; the lowest marks the second beat of the bar, which is what gives samba its forward lean."},
 {"q": "Name four instruments of a samba bateria besides the surdo.",
  "a": "Tamborim, agogo bells, caixa (snare drum), repinique (the leader's calling drum), ganza or chocalho shakers, and cuica."},
 {"q": "What is a samba-enredo?",
  "a": "The theme song written for a samba school's carnival parade each year. It is strophic, with a short singable refrain, and thousands of people sing it while they walk."},
 {"q": "What is the tresillo, or 3+3+2, grouping?",
  "a": "Eight fast pulses in a bar accented as three plus three plus two, so the accents pull against the steady duple beat. It runs through much Latin American and Caribbean dance music."},
 {"q": "Name the main families of pans in a steelband and what they play.",
  "a": "Tenor or lead pans take the melody; double seconds and cellos or guitars play chords and countermelody in the middle; bass pans, several drums to a player, play the bass line."},
 {"q": "What is the engine room of a steelband?",
  "a": "Its rhythm section: irons (car brake drums struck with metal beaters), a scratcher and a drum kit. It keeps the pulse cutting through the pans and never stops."},
]

practice = [
 {"text": "State the metre of both recordings in this lesson.", "marks": 1, "kind": "Identification",
  "mark_scheme": "1 mark: duple. Accept 2/4 for the samba and 4/4 or duple for the calypso arrangement."},
 {"text": "Describe the role of the surdo in a samba bateria.", "marks": 2, "kind": "Description",
  "mark_scheme": "1 mark: it is the bass drum of the band, played in two or three tuned sizes. 1 mark: the lowest surdo marks or answers on the second beat of the bar, giving samba its forward lean."},
 {"text": "Explain what a break, or paradinha, is and what it shows about how a bateria works together.", "marks": 3, "kind": "Explanation",
  "mark_scheme": "Break: the groove stops and the whole band plays one rehearsed figure together (1). It is cued or called by the leader, usually on the repinique or whistle (1). It shows the band operating as a single rehearsed instrument, responding to signals rather than notation (1)."},
 {"text": "Name three families of pan in a steel orchestra and describe what each plays.", "marks": 3, "kind": "Identification",
  "mark_scheme": "1 mark each, up to 3: tenor or lead pans, melody; double seconds or cellos or guitars, chords and countermelody; bass pans, the bass line."},
 {"text": "Explain what the engine room contributes to a steelband, and why it matters at Panorama.", "marks": 3, "kind": "Explanation",
  "mark_scheme": "Credit: irons, scratcher and drum kit (1); they keep an unbroken metallic pulse that cuts through the massed pans (1); on an unamplified outdoor stage with a very large band it is what holds the ensemble and the audience together (1)."},
 {"text": "Compare how the samba track and the steelband track are structured.", "marks": 4, "kind": "Comparison",
  "mark_scheme": "Samba: strophic song, verses and refrain over an unchanging percussion ostinato, punctuated by rehearsed breaks (2). Steelband: a competition arrangement that expands a short calypso with new sections, countermelodies, a strumming passage and a late key change (2). Credit any accurate comparison of what changes and what stays fixed."},
]

kcs = [
 {"q": "Which beat does the lowest surdo mark in samba?", "options": ["Beat one", "Beat two", "Beat three", "Every off-beat"], "correct": 1},
 {"q": "What is the repinique used for in a bateria?", "options": ["Playing the melody", "Calling and cueing the band", "Marking the bass line", "Shaking a steady pulse"], "correct": 1},
 {"q": "What is Panorama?", "options": ["A samba school in Rio", "Trinidad and Tobago's national steelband competition", "A type of steel pan", "The Brazilian word for a rhythmic break"], "correct": 1},
 {"q": "Which pans usually carry the melody in a steel orchestra?", "options": ["Bass pans", "Cellos", "Tenor or lead pans", "Double seconds"], "correct": 2},
 {"q": "The accent pattern 3+3+2 across eight fast pulses is known as:", "options": ["Tresillo", "Chaal", "Tala", "Timeline"], "correct": 0},
]

related_media = [
 {"category": "Videos & Channels", "items": [
   {"url": "https://www.youtube.com/@MonoblocoOficial",
    "title": "Monobloco Oficial",
    "description": "The Rio group from track one: more live bateria performances with the full percussion line-up."},
   {"url": "https://www.youtube.com/@TrinidadAllStars",
    "title": "Trinidad All Stars",
    "description": "The steel orchestra's own channel, including Panorama performances from several years."},
   {"url": "https://www.youtube.com/watch?v=krlQB56actI",
    "title": "Rio Carnaval — Mangueira, sambas de enredo (live, 2025)",
    "description": "A full samba school on parade: hear how much bigger a school's bateria is than a bloco."},
   {"url": "https://www.youtube.com/watch?v=hIlUS2UVYk4",
    "title": "Lord Kitchener — Old Time Calypso",
    "description": "A sung calypso by one of Trinidad's great calypsonians, so you can hear the words a steelband leaves out."}]},
 {"category": "Reference", "items": [
   {"url": "https://www.bbc.co.uk/bitesize/guides/zrk9dxs/revision/5",
    "title": "BBC Bitesize — Samba music",
    "description": "Instrument-by-instrument notes on the bateria and the samba groove."},
   {"url": "https://www.britannica.com/art/calypso-music",
    "title": "Britannica — Calypso",
    "description": "Origins of calypso in Trinidad, its carnival setting and its role as social commentary."}]},
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
io.open(os.path.join(HERE, "html", "ocr_l4_americas.html"), "w", encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
