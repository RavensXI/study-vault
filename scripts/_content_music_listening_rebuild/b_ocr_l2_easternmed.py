# -*- coding: utf-8 -*-
"""music-ocr / aos3-rhythms-listening / L2 -- Eastern Mediterranean and Middle East.

Rebuilt from a PRACTICE row (synthesised-click problem bank) into a guided
listening lesson on two real recordings, per Tom's decision 7 Sep 2026.

Recordings, both verified: oEmbed 200, yt-dlp playable_in_embed True, age 0,
and loaded without error in a real YouTube IFrame player on the studyvault.co.uk
origin (durations below are that player's own getDuration).

  t1  WvFh7PmMmXk  513 s  Classical Arabic Orchestra of Aleppo: "Samai Bayati
                          (Taksim Oud, Samai Thaqil 10/8, Samai Darij 6/8)".
                          Takht ensemble: oud, qanun, ney, violin, riq,
                          darabuka. Opens with a free-rhythm oud taqsim.
  t2  _3Ksv4Z1q4o  186 s  Orchestra Mesogios (Topic, label release):
                          "Kalamatianos". Greek circle dance in 7/8 (3+2+2) for
                          clarinet, violin, santouri, laouto and tambourine.

Pin times: 3-vote Gemini consensus, timings.json keys ocr_l2_t1 / ocr_l2_t1b /
ocr_l2_t2 / ocr_l2_t2b; every pin carries at least 2 of 3 agreeing votes.
Dropped: t1 "final_chord" at 511 s (99.6% along the bar -- the pin and its
tooltip would sit off the end of the scrub track); t1 "mid_contrast_section"
(209) is the same moment as "solo_instrument_passage" (209), so one pin
carries both; t2 "clarinet_lead" and "violin_lead" from the first probe, which
collided with each other at 28-29 s and were replaced by the cleaner strain
questions in the re-probe.
"""
import io, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck_multi import MultiDeck, dfn, patch, check_plain

BACKUP = "music-ocr__aos3-rhythms-listening__L02"
HERE = os.path.dirname(os.path.abspath(__file__))
old = json.load(io.open(os.path.join(HERE, "backups", BACKUP + ".json"), encoding="utf-8"))

d = MultiDeck(
    lesson_id=old["id"], subject="music-ocr", unit="aos3-rhythms-listening", lesson_no=2,
    tracks=[("t1", "WvFh7PmMmXk", 513, "Arabic samai"),
            ("t2", "_3Ksv4Z1q4o", 186, "Greek kalamatianos")],
    credit=("Streamed from YouTube &mdash; not hosted by StudyVault. Classical Arabic Orchestra of Aleppo, "
            "&lsquo;Samai Bayati&rsquo;; Orchestra Mesogios, &lsquo;Kalamatianos&rsquo;."))
TITLE = "Eastern Mediterranean and Middle East — Guided Listening"

d.pins = [
    ("t1", "t1c1", 0,   "Oud alone",        "A solo improvisation with no pulse at all: the oud explores the mode before the piece begins."),
    ("t1", "t1c2", 93,  "The ensemble in",  "The whole ensemble and the percussion enter together and a ten-beat cycle starts turning."),
    ("t1", "t1c3", 209, "One voice leads",  "A solo instrument takes the melody forward inside the cycle while the others fall back."),
    ("t1", "t1c4", 371, "The refrain again", "The opening ensemble refrain returns after a contrasting section &mdash; the shape of the whole piece."),
    ("t1", "t1c5", 426, "The metre changes", "The closing section moves into a faster, lilting six, and the hand percussion is at its most exposed."),
    ("t2", "t2c1", 0,   "Seven, not eight", "The dance starts at once. Count the fast pulses in a bar: seven, grouped long-short-short."),
    ("t2", "t2c2", 28,  "A second strain",  "A new melody, same metre. Greek dance tunes are built from strains that are repeated and swapped."),
    ("t2", "t2c3", 46,  "A third strain",   "A third melody, and the lead passes between the instruments."),
    ("t2", "t2c4", 74,  "Back to the first", "The opening strain returns: the tunes alternate rather than develop."),
    ("t2", "t2c5", 180, "The last phrase",  "The final phrase of the dance, ending on the beat rather than fading."),
]

d.add_cover(
  "Irregular beats, decorated melodies",
  [
   "Track one is Arabic art music from Aleppo in Syria. A %s &mdash; the small classical ensemble of %s, %s, %s, "
   "violin and %s &mdash; plays a samai. It opens with a solo %s: pure improvisation with no pulse at all. The "
   "melody follows a %s, and some of its notes fall between the notes a piano can play."
   % (dfn("takht", "The small classical ensemble of Arabic art music"),
      dfn("oud", "A short-necked, fretless Arabic lute, the ancestor of the European lute"),
      dfn("qanun", "A large Arabic zither plucked with plectra worn on the fingers"),
      dfn("ney", "An end-blown reed flute used across the Arab world, Turkey and Iran"),
      dfn("riq", "A small Arabic tambourine with heavy jingles, played with great precision"),
      dfn("taqsim", "A free-rhythm improvisation that explores a maqam before or between metred sections"),
      dfn("maqam", "The Arabic modal system: a scale plus rules about how its melodies move, including microtonal steps")),
   "Track two is a %s, a Greek circle dance, played by clarinet, violin, %s, %s and tambourine. This Area of Study "
   "also asks for Palestinian and Israeli folk music, and all of it shares the same two signatures: %s built from "
   "unequal groups of equal fast pulses, and melodies decorated far more heavily than a Western tune would be."
   % (dfn("kalamatianos", "A Greek line or circle dance in 7/8, named after the town of Kalamata"),
      dfn("santouri", "A Greek hammered dulcimer, struck with light beaters"),
      dfn("laouto", "A long-necked Greek lute used to accompany dance music"),
      dfn("irregular metres", "Metres with an odd number of fast pulses per bar, grouped unequally; also called additive")),
   "Press play and the cards follow the music. Use the track buttons to swap recordings, and tap any number to jump.",
  ], title="The tradition")

d.add_statement(1, "1 · Oud alone", "1 &middot; No pulse at all",
  "The oud plays alone, and there is no beat to count. %s A taqsim is improvised: the player works through the "
  "notes of the maqam, testing each one, pausing where the phrase wants to pause. Listen to the pitches. Several "
  "of them sit between the keys of a piano, and those %s are what makes the mode sound like this one and no other."
  % (d.ref(1), dfn("microtones", "Intervals smaller than a semitone; in Arabic music, notes roughly a quarter-tone apart")),
  "pitches between the piano&rsquo;s notes, and the absence of any pulse. Free rhythm is itself the answer.")

d.add_statement(2, "2 · The ensemble in", "2 &middot; Ten beats, and everyone at once",
  "The whole takht arrives with the percussion and a cycle starts turning. %s The rhythmic pattern, or %s, has ten "
  "beats, unequally grouped, so it never settles into a march or a waltz. Notice the texture: every instrument is "
  "playing the same melody, but each one decorates it differently. That is %s."
  % (d.ref(2), dfn("iqa", "The rhythmic cycle or mode of Arabic music, played on riq and darabuka"),
     dfn("heterophony", "One melody played simultaneously by several performers, each decorating it their own way")),
  "count the fastest steady pulse per bar. Ten, in unequal groups, means an irregular cycle.")

d.add_statement(3, "3 · One voice leads", "3 &middot; A section for one player",
  "A single instrument steps forward and the rest fall back to accompany. %s A samai is built from separate "
  "sections, and each one gives different material to the ensemble; some are shared, some belong to one player. "
  "The cycle underneath does not change, so the soloist is measured against a beat you can still count."
  % d.ref(3),
  "which instrument has the melody, and how the others change what they play to make room for it.")

d.add_statement(4, "4 · The refrain again", "4 &middot; The refrain comes back",
  "The opening ensemble music returns after the contrasting section. %s That alternation is the whole structure of "
  "a samai: a new section, then the refrain, then another new section, then the refrain again. The effect is "
  "closer to a %s than to anything that develops, and it makes the form easy to describe in an answer."
  % (d.ref(4), dfn("rondo", "A form in which a recurring section alternates with contrasting ones")),
  "music you have already heard, returning unchanged. Name it as a returning refrain, not as a repeat.")

d.add_statement(5, "5 · The metre changes", "5 &middot; Into a faster six",
  "The closing section shifts into a quicker, lilting metre in groups of three, and the %s and %s are at their "
  "most exposed. %s A metre change at the end is standard in this form. Say which way it moves: from an unequal "
  "ten to an even, rolling six, and from stately to dancing."
  % (dfn("riq", "A small Arabic tambourine with heavy jingles"),
     dfn("darabuka", "A goblet-shaped hand drum, the main Arabic dance drum"), d.ref(5)),
  "the change of grouping, then the change of character. Both are worth marks; only one is obvious.")

d.add_statement(6, "1 · Seven, not eight", "1 &middot; Count to seven",
  "The dance begins immediately, with the %s leading. %s Count the fastest steady pulses in a bar and you get "
  "seven, not eight, grouped 3+2+2. That long group at the front is why the dance limps forward: the first step is "
  "longer than the two that follow it. Try marching in two or waltzing in three and neither will fit."
  % (dfn("clarinet", "In Greek folk music the klarino, the lead melody instrument of a dance band"), d.ref(6)),
  "the accent pattern. Where is the LONG group? At the front, and that is what makes it a kalamatianos.")

d.add_statement(7, "2 · A second strain", "2 &middot; A new tune, same seven",
  "A different melody, over exactly the same rhythm. %s Greek dance tunes are built from short %s that are "
  "repeated, decorated and handed round the band. The metre never changes: it is the ground the dancers hold on "
  "to, and changing it would stop the circle."
  % (d.ref(7), dfn("strains", "Short self-contained melodies that make up a folk dance tune")),
  "the metre continuing underneath a completely new tune. Melody changes; the seven does not.")

d.add_statement(8, "3 · A third strain", "3 &middot; Passing it round",
  "A third melody, and the lead moves between the instruments. %s Behind them the %s and the tambourine hold the "
  "rhythm, while the santouri fills the gaps. This division &mdash; melody instruments in front, plucked and "
  "struck instruments behind &mdash; is how a Greek dance band works, and it is worth naming as texture."
  % (d.ref(8), dfn("laouto", "A long-necked Greek lute, played with a plectrum to drive the rhythm")),
  "which instrument has the tune at any moment. The answer changes more than once.")

d.add_statement(9, "4 · Back to the first", "4 &middot; Round it comes",
  "The opening strain returns. %s The structure here is alternation, not development: tunes come back rather than "
  "growing. That is true of the Arabic samai on the other track as well, and of the tala and chaal cycles in the "
  "India and Punjab lesson. Traditional music across this whole Area of Study is built on return."
  % d.ref(9),
  "a melody you recognise from the beginning. Say which one and where it came from.")

d.add_statement(10, "5 · The last phrase", "5 &middot; It stops on the beat",
  "The final phrase arrives and the dance ends. %s There is no fade and no Western cadence: the tune finishes its "
  "phrase, and because the dancers need to know when to stop, the ending is exact. Compare it with the Arabic "
  "track, which also stops rather than resolving."
  % d.ref(10),
  "the last accent. Everything in this music, including the ending, is measured in fast pulses.")

d.add_checklist(
  "Arabic: takht of oud, qanun, ney, violin, riq and darabuka; taqsim, free rhythm and improvised; maqam with "
  "microtonal notes; heavy ornamentation; heterophonic texture; the iqa, a ten-beat cycle, changing to a faster "
  "six at the end; sections alternating with a returning refrain. Greek: kalamatianos in 7/8 grouped 3+2+2, an "
  "irregular or additive metre; clarinet and violin leading, laouto and tambourine driving, santouri filling; "
  "strains alternating. Both are dance and social music, learnt by ear and spread by recording and broadcast.",
  "Never write &ldquo;it sounds Middle Eastern&rdquo;. Count first and name the number: seven fast pulses grouped "
  "3+2+2, or a ten-beat cycle. Then name what the melody does: microtonal steps, heavy ornamentation, "
  "heterophony. Number plus grouping plus one melodic feature is a complete answer in two lines.")

content = d.content()

exam_tip = ("<p>Count the fastest steady pulse per bar before you write anything: seven or nine means an irregular "
            "metre, and saying so is the first mark. Then find the accent pattern and say where the long group "
            "falls &mdash; 3+2+2 for a kalamatianos, 2+2+2+3 for a karsilamas in nine. In Arabic music, listen "
            "for pitches between the notes of a piano and describe them as microtonal, and describe the "
            "improvised free-rhythm opening as a taqsim rather than as an introduction.</p>")
conclusion = ("<p>You can now count a seven-pulse Greek dance and hear where its long group falls, follow an "
              "Arabic samai from its free-rhythm taqsim through a ten-beat cycle to a faster closing metre, and "
              "name the instruments of both ensembles. You can also describe what these melodies do that Western "
              "ones do not: microtonal steps, dense ornamentation and a heterophonic texture.</p>")
description = ("Follow an Arabic samai and a Greek kalamatianos landmark by landmark: taqsim, maqam and "
               "microtones, a ten-beat cycle, and seven pulses grouped 3+2+2.")

flashcards = [
 {"q": "What is a maqam?",
  "a": "The Arabic modal system: a scale together with rules about how melodies move within it. Many maqamat include microtonal steps, notes roughly a quarter-tone apart, which no piano can play."},
 {"q": "What is a taqsim?",
  "a": "A free-rhythm improvisation on one instrument that explores a maqam. It has no pulse, no fixed length and no accompaniment, and it usually comes before or between the metred sections."},
 {"q": "Name the instruments of a takht ensemble.",
  "a": "Oud (fretless lute), qanun (plucked zither), ney (end-blown reed flute), violin, and percussion: riq (tambourine) and darabuka (goblet drum)."},
 {"q": "What is heterophony?",
  "a": "One melody played at the same time by several performers, each decorating it in their own way. It is the standard texture of Arabic and much Eastern Mediterranean traditional music."},
 {"q": "How is a kalamatianos counted?",
  "a": "Seven fast pulses in a bar, grouped 3+2+2. The long group comes first, which is why the dance leans forward on its first step."},
 {"q": "What is an additive or irregular metre?",
  "a": "A metre built from unequal groups of equal fast pulses, such as 7/8 as 3+2+2 or 9/8 as 2+2+2+3. It cannot be marched in two or waltzed in three."},
]

practice = [
 {"text": "State the metre of the Greek dance and how its beats are grouped.", "marks": 2, "kind": "Identification",
  "mark_scheme": "1 mark: 7/8, or seven fast pulses in a bar. 1 mark: grouped 3+2+2, with the long group first."},
 {"text": "Define taqsim and describe two things you can hear in the one that opens the Arabic track.", "marks": 3, "kind": "Explanation",
  "mark_scheme": "Definition: a free-rhythm improvisation exploring a maqam (1). Two from: no pulse or beat; a single instrument alone; pauses at the ends of phrases; ornamented, decorated lines; microtonal pitches (1 mark each, up to 2)."},
 {"text": "Explain what microtones are and why they matter in this music.", "marks": 3, "kind": "Explanation",
  "mark_scheme": "Intervals smaller than a semitone, roughly quarter-tones (1). They fall between the notes available on a piano or Western fixed-pitch instrument (1). They are part of the identity of a maqam, so the mode cannot be reproduced accurately without them (1)."},
 {"text": "Describe the texture of the Arabic ensemble and name it.", "marks": 3, "kind": "Description",
  "mark_scheme": "Several instruments playing the same melody at once (1), each adding its own ornaments so the lines differ slightly (1). The term is heterophony or heterophonic (1)."},
 {"text": "A student says the Greek dance is in 7/8 grouped 2+2+3. Explain what listening evidence proves them wrong.", "marks": 3, "kind": "Explanation",
  "mark_scheme": "The accent falls at the start of the bar on a group of three, not at the end (1). The first step or beat is audibly longer than the two that follow (1). Tapping 2+2+3 places the long group late and does not fit the dance step or the accompaniment (1)."},
 {"text": "Compare how the Arabic samai and the Greek dance are structured.", "marks": 4, "kind": "Comparison",
  "mark_scheme": "Samai: separate sections alternating with a returning refrain, over a ten-beat cycle, with a change to a faster metre at the end (2). Greek dance: short strains repeated and alternated, with the lead passing between instruments, over an unchanging 7/8 (2). Credit the point that both alternate and return rather than develop."},
]

kcs = [
 {"q": "How many fast pulses are there in a bar of kalamatianos, and how are they grouped?", "options": ["Seven, as 3+2+2", "Seven, as 2+2+3", "Nine, as 2+2+2+3", "Eight, as 3+3+2"], "correct": 0},
 {"q": "What is the oud?", "options": ["An end-blown reed flute", "A short-necked fretless lute", "A plucked zither", "A goblet-shaped hand drum"], "correct": 1},
 {"q": "A free-rhythm improvisation exploring a maqam is called a:", "options": ["Iqa", "Samai", "Taqsim", "Teslim"], "correct": 2},
 {"q": "Notes that fall between the notes of a piano are described as:", "options": ["Chromatic", "Microtonal", "Modal", "Diatonic"], "correct": 1},
 {"q": "Several performers playing the same melody at once, each decorating it differently, is called:", "options": ["Polyphony", "Homophony", "Heterophony", "Monophony"], "correct": 2},
]

related_media = [
 {"category": "Videos & Channels", "items": [
   {"url": "https://www.youtube.com/watch?v=lqFxlaXYXBM",
    "title": "Classical Arabic Orchestra of Aleppo — Samai Husseini",
    "description": "The same form and the same ensemble, shorter and with no taqsim: good for hearing the ten-beat cycle on its own."},
   {"url": "https://www.youtube.com/watch?v=RKNv7F819ww",
    "title": "Oxford Maqam — Semai Bayati",
    "description": "The same maqam played by a British ensemble, so you can compare two readings of one mode."},
   {"url": "https://www.youtube.com/watch?v=mAz91lvI-JQ",
    "title": "Katevas — Greek folk dances of Macedonia",
    "description": "A run of dances in different metres, useful for telling seven from nine by ear."},
   {"url": "https://www.youtube.com/watch?v=GJL9KAue0ic",
    "title": "Nikos Sgouros — Kalamatianos Dance (Moreas)",
    "description": "Another kalamatianos, clarinet-led, for a second example of 3+2+2."}]},
 {"category": "Reference", "items": [
   {"url": "https://www.britannica.com/art/Greek-music",
    "title": "Britannica — Greek music",
    "description": "Background on Greek folk instruments, dance forms and their regional traditions."},
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
io.open(os.path.join(HERE, "html", "ocr_l2_easternmed.html"), "w", encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
