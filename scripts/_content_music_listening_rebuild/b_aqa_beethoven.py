# -*- coding: utf-8 -*-
"""music-aqa / aos1-western-classical / L3 -- Beethoven Symphony No. 1, i.
Rebuilt as a guided-listening deck. This lesson is LIVE and Tom has QA'd it by
ear, so every existing pin time is carried over unchanged and the musical
claims are restructured, not re-argued.

The R2 wave dock is reused verbatim: data-audio, data-peaks, the canvas and the
inline peaks JSON (duration 581.5) all survive; only the pin buttons change.

PROBE RESULT -- FLAGGED, NOT APPLIED. A whole-file Gemini probe of the real R2
recording plus a targeted 60-140 s window probe both put the Allegro con brio
earlier than pin 2:
    pin 2 Allegro con brio    107 s   probe 82 s (2/3) and 89 s (2/3, windowed)
    pin 3 second subject      143 s   probe 132 s (2/3)
    pin 4 exposition repeat   232.5   probe split (206 / 195 / 162)
    pin 5 development         378     probe split (331 / 308)
    pin 6 recapitulation      406     probe 404 (2/3)   <- agrees
    pin 7 coda                520     probe 515-524     <- agrees
The machine agrees with Tom on the two late landmarks and disagrees on the
early ones, but disagrees with ITSELF on the repeat and the development, so the
evidence is not strong enough to move a QA'd live pin. Left as-is for Tom's ear
to settle; see the report.
"""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck_raw import RawDeck, dfn, patch, build_questions_keep, check_plain

BACKUP = "music-aqa__aos1-western-classical__L03"
HERE = os.path.dirname(os.path.abspath(__file__))
old = json.load(io.open(os.path.join(HERE, "backups", BACKUP + ".json"), encoding="utf-8"))

d = RawDeck(lesson_id=old["id"], subject="music-aqa", unit="aos1-western-classical", lesson_no=3,
            original_html=old["content_html"])
TITLE = "Beethoven: Symphony No. 1, First Movement — Guided Listening"

d.pins = [   # (track, cid, seconds, title, tip) -- times unchanged from the live lesson
    ("t1", "c1", 0,     "Adagio molto introduction", "Dominant seventh &mdash; an opening chord that pulls towards F major: the wrong key, on purpose."),
    ("t1", "c2", 107,   "Allegro con brio",          "Sforzando &mdash; sudden forced accents &mdash; and a fast crescendo as C major finally lands."),
    ("t1", "c3", 143,   "Second subject",            "Second subject &mdash; the contrasting melody in a related key, carried by the wind."),
    ("t1", "c4", 232.5, "Exposition repeat",         "Exposition &mdash; the section presenting both subjects; Classical convention repeats it in full."),
    ("t1", "c5", 378,   "Development",               "Development &mdash; fragments of the themes pushed through unstable, shifting keys."),
    ("t1", "c6", 406,   "Recapitulation",            "Recapitulation &mdash; the themes return, now settled in the home key of C major."),
    ("t1", "c7", 520,   "Coda",                      "Coda &mdash; the closing passage: emphatic cadences hammering the ending home."),
]

PORTRAIT = ('<figure class="sv-card-img"><img src="https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev/'
            'music-aqa/cards/beethoven-1803-horneman.jpg" alt="Portrait miniature of Ludwig van Beethoven by '
            'Christian Horneman"><figcaption>Beethoven around the time of this symphony. Christian Horneman. '
            'Public domain.</figcaption></figure>')

d.add_cover(
  "A symphony that starts in the wrong key",
  [
    "Beethoven&rsquo;s Symphony No. 1 in C major, completed and first performed in 1800, is the compulsory set "
    "study piece. A late-Classical orchestra, C major, and a first movement built as a slow %s introduction "
    "followed by an Allegro con brio in %s."
    % (dfn("Adagio molto", "An Italian tempo marking meaning very slow"),
       dfn("sonata form", "A structure in three main stages, exposition, development and recapitulation, often followed by a coda")),
    "Beethoven wrote it as a former pupil of Haydn and an admirer of Mozart, using the four-movement plan and "
    "standard orchestra they had established. What he does inside that inheritance is the point: the piece is "
    "often described as standing on the boundary between the Classical era and the Romantic one he helped create."
    + PORTRAIT,
    "Press play and the cards follow the music. Tap any number to jump to that moment.",
  ])

d.add_statement(1, "1 · Adagio molto introduction", "1 &middot; The wrong chord",
  "The movement opens slowly, bars 1 to 12. %s The very first chord is a %s &mdash; but it belongs in F major, not "
  "in the symphony&rsquo;s home key of C major. For 1800 that was a striking way to begin, and the introduction "
  "goes on touching harmonic areas without settling in any of them."
  % (d.ref(1), dfn("dominant seventh", "A four-note chord built on the fifth degree of a scale, which normally pulls strongly towards the tonic")),
  "a chord that pulls somewhere, then does not go there. Most symphonies before 1800 state the home key at once.")

d.add_statement(2, "2 · Allegro con brio", "2 &middot; C major, at last",
  "The wait ends and C major finally lands, with far more force for having been delayed. %s The music is in %s, "
  "written 2/2, so there are two strong beats a bar rather than four. Short repeated motifs drive it, sudden %s "
  "accents jolt the texture, and a rapid crescendo pushes it forward."
  % (d.ref(2), dfn("alla breve", "A time signature, also written 2/2, with two minim beats in a bar, giving a fast, strong pulse"),
     dfn("sforzando", "A sudden strong accent placed on a single note or chord")),
  "the release of tension. Name the arrival of the %s, not just &lsquo;it gets faster&rsquo;."
  % dfn("tonic", "The home key of a piece, the point of harmonic rest"))

d.add_statement(3, "3 · Second subject", "3 &middot; The wind answers",
  "A contrasting theme arrives in a related key: the %s. %s Listen to who plays it. The orchestra is a standard "
  "late-Classical one &mdash; pairs of flutes, oboes, clarinets and bassoons, pairs of horns and trumpets, timpani "
  "and strings &mdash; and Beethoven gives the wind its own melodic material rather than doubling the strings."
  % (dfn("second subject", "A contrasting theme introduced later in the exposition, usually in a different key from the first subject"), d.ref(3)),
  "wind tone carrying the tune. Clarinets were still a new addition to the symphony orchestra in 1800.")

d.add_statement(4, "4 · Exposition repeat", "4 &middot; Both subjects again",
  "The whole %s is played a second time, as Classical convention expects. %s Use it: you now know what the first "
  "subject and the second subject sound like, so listen through the repeat and check you can hear the join between "
  "them and the change of key that comes with it."
  % (dfn("exposition", "The opening section of a sonata-form movement, where the first and second subjects are introduced"), d.ref(4)),
  "the same two ideas in the same order. This repeat is the free practice run the movement gives you.")

d.add_statement(5, "5 · Development", "5 &middot; Taken apart",
  "No new theme appears here. %s The %s takes fragments of what you have already heard and pushes them through "
  "unstable, shifting keys, so a tune you know keeps surfacing in unfamiliar surroundings. Recognising material in "
  "pieces rather than whole is the skill this section tests."
  % (d.ref(5), dfn("development", "The middle section of sonata form, where ideas from the exposition are fragmented, altered and moved through different keys")),
  "scraps of the first subject rather than the whole theme, and harmony that will not settle.")

d.add_statement(6, "6 · Recapitulation", "6 &middot; Home",
  "The themes return, and this time they stay in C major. %s That is what a %s does: it restates the exposition&rsquo;s "
  "material with the tonal argument resolved, so the second subject no longer moves away to a related key. After all "
  "the delay at the start, the home key now sounds settled rather than withheld."
  % (d.ref(6), dfn("recapitulation", "The section of sonata form that restates the exposition&rsquo;s themes, now usually staying in the home key")),
  "the same themes, but with the key fixed. Say which section you are in and what the key is doing.")

d.add_statement(7, "7 · Coda", "7 &middot; Hammering it home",
  "A closing passage rounds the movement off. %s The %s drives emphatic %s that leave no doubt about C major &mdash; "
  "the key the opening chord deliberately avoided. Across nine minutes Beethoven has turned the home key from "
  "something withheld into something insisted upon."
  % (d.ref(7), dfn("coda", "A concluding passage added after the recapitulation to round off a movement"),
     dfn("cadences", "Chord patterns that end a phrase, like musical punctuation")),
  "how firmly it stops. Compare that certainty with the ambiguous chord you heard at the very beginning.")

d.add_checklist(
  "Genre: Classical symphony, first movement. Forces: pairs of flutes, oboes, clarinets and bassoons, pairs of "
  "horns and trumpets, timpani and strings. Key: C major, approached through an introduction that avoids it. Metre "
  "and tempo: Adagio molto, then Allegro con brio in alla breve. Structure: slow introduction, then sonata form "
  "with the exposition repeated, a development, a recapitulation and a coda. Dynamics: sforzando accents and rapid "
  "crescendos. Context: 1800, written by a pupil of Haydn on the edge of the Romantic era.",
  "Support each point by naming the element, using its technical term and locating it in the music. Weak: "
  "&ldquo;the music sounds exciting and grand&rdquo; &mdash; no element, no term, no location. Strong: &ldquo;the "
  "first subject, from around 1:50, creates energy through short repeated motifs and sudden sforzando accents, "
  "before a rapid crescendo drives the music out of the ambiguous Adagio molto introduction.&rdquo;")

content = d.content()
exam_tip = old["exam_tip_html"]
conclusion = old["conclusion_html"]
description = ("Follow Beethoven's First Symphony through seven landmarks, from the wrong-key opening chord to the "
               "coda that hammers C major home.")

pq, kc, fc = build_questions_keep(BACKUP)
errs, warns = d.verify(content, (exam_tip or "") + (conclusion or ""), allow_img=True)
for o, lbl in ((pq, "practice"), (kc, "kc"), (fc, "flashcards")):
    check_plain(o, lbl, errs)
if len(description) > 160:
    errs.append("description %d chars" % len(description))
print("cards", len(d.cards), "| narration ids", d._n, "| chars", len(content), "| desc", len(description),
      "| card words", d.card_words)
for w in warns:
    print("WARN", w)
if errs:
    print("ERRORS:")
    for e in errs:
        print("  -", e)
    raise SystemExit(1)
print("verify OK")
payload = {"title": TITLE, "content_html": content, "description": description,
           "flashcard_questions": fc, "practice_questions": pq, "knowledge_checks": kc,
           "narration_manifest": None}
io.open(os.path.join(HERE, "html", "aqa_beethoven.html"), "w", encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
