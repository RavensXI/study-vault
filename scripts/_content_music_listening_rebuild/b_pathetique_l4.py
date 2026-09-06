# -*- coding: utf-8 -*-
"""music-edexcel / aos1-instrumental-music / L4 -- Pathetique i, STRUCTURAL walk.
Video hcczxDKkYhU (Fabian Mueller, Deutsche Grammophon), 9:20 = 560 s.
Pin times and how they were corroborated (four probe rounds, timings.json):
  0    Grave begins, 3/3.
  100  Allegro begins, 3/3 in two rounds (1:40).
  143  second subject, 2/3, and the arithmetic fits: the exposition runs
       100-221 s for 122 bars (~0.99 s/bar), so bar 51 falls at ~140 s.
  221  the exposition repeat, 2/3; the repeat then runs 221-329 s (108 s),
       the same music slightly quicker, and all three probes answered "yes"
       to the direct question about whether the exposition is played twice.
  329  the Grave returns, five votes across three rounds.
  375  the fast music is running again, seven votes across three rounds; the
       gap 329-375 is 46 s for the four Grave bars, matching the opening
       Grave's 10 s per bar.
  505  the last Grave, 3/3; 544 the coda resumes, 2/3; 552 the last chord.
DROPPED: a separate pin for the recapitulation. Votes for it collided with the
375 s answer and never agreed independently, so the recapitulation is described
in prose instead of pinned.
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck import Deck, dfn, patch, build_questions, check_plain

BACKUP = "music-edexcel__aos1-instrumental-music__L04"
d = Deck(lesson_id="e20420ef-8560-4f9f-800c-0a388c2bd0fd",
         subject="music-edexcel", unit="aos1-instrumental-music", lesson_no=4,
         yt="hcczxDKkYhU", dur=560, track_label="Path&eacute;tique i",
         credit="Fabian M&uuml;ller, streamed from YouTube (Deutsche Grammophon) &mdash; not hosted by StudyVault. "
                "Beethoven: Piano Sonata No. 8 &lsquo;Path&eacute;tique&rsquo;, 1st movement.")
TITLE = "Beethoven: Pathétique Sonata, First Movement — Guided Listening"

d.pins = [
    ("t1c1", 0,   "Grave",             "Heavy C minor chords and dotted rhythms. An introduction with the weight of an opera scene."),
    ("t1c2", 100, "Allegro",           "The first subject rockets up over a tremolo left hand. Everything changes at once."),
    ("t1c3", 143, "Second subject",    "The contrasting theme arrives &mdash; in the unexpected minor, before it brightens."),
    ("t1c4", 221, "Heard again",       "The whole exposition is played a second time. Same music, so use it to check your landmarks."),
    ("t1c5", 329, "The Grave returns", "The slow introduction erupts back mid-movement. Beethoven&rsquo;s structural shock."),
    ("t1c6", 375, "Development",       "Fragments of the first subject, worked through key after key."),
    ("t1c7", 505, "Grave, then coda",  "One last memory of the introduction, then a fast, abrupt close in C minor."),
]

d.add_cover(
  "Beethoven: Path&eacute;tique Sonata, first movement",
  [
    "Composed in 1798 for solo piano, in C minor and common time: a slow %s introduction, then an Allegro di molto e "
    "con brio in %s. Beethoven titled it himself &mdash; <em>Grande Sonate Path&eacute;tique</em> &mdash; and "
    "dedicated the sonata to his patron Prince Karl von Lichnowsky."
    % (dfn("Grave", "A very slow, solemn tempo marking"),
       dfn("sonata form", "A structure in three sections: exposition, development and recapitulation")),
    "Haydn and Mozart wrote sonatas for the drawing room. Beethoven writes this one as public theatre, and the "
    "radical stroke is that the slow introduction refuses to stay at the beginning: it comes back twice inside the "
    "fast movement.",
    "Press play and the cards follow the music. Tap any number to jump to that moment.",
  ])

d.add_statement(1, "Grave", "1 &middot; The introduction",
  "C minor, very slow, and immediately dramatic. %s A loud %s chord is answered by a hushed one; the harmony is "
  "unsettled by %s that belong to no single key. The texture is %s, so nothing distracts from the gesture itself. "
  "Fix this sound: you will meet it twice more."
  % (d.ref(1), dfn("dotted rhythm", "A long dotted note followed by a short one, giving a jagged, marching feel"),
     dfn("diminished seventh chords", "Chords built from stacked minor thirds, with no strong pull to one key"),
     dfn("homophonic", "One melody supported by chords moving in the same rhythm")),
  "the loud-then-quiet pairs. That contrast, not the tune, is what the introduction is made of.")

d.add_statement(2, "Allegro", "2 &middot; The storm arrives",
  "Tempo, dynamic and texture all change in a single bar. %s The %s climbs restlessly in the right hand over a "
  "hammering %s in the left, in the tonic key of C minor. This is the %s of the sonata form beginning, and the shock "
  "comes purely from placing it against what went before."
  % (d.ref(2), dfn("first subject", "The opening main theme of a sonata-form movement, in the home key"),
     dfn("tremolo", "Very rapid repetition of a note, octave or chord"),
     dfn("exposition", "The first section of sonata form, which presents the first and second subjects")),
  "the left hand shuddering underneath. If you hear fast repeated notes under a rising tune, you are in the first subject.")

d.add_statement(3, "Second subject", "3 &middot; The wrong minor",
  "A bridge passage modulates away and a smoother, more singing theme appears. %s The expected key would be E flat "
  "major, the %s of C minor. Beethoven gives E flat minor instead, so the contrast arrives still in shadow; only "
  "later does it brighten into E flat major, where a closing theme finishes the exposition."
  % (d.ref(3), dfn("relative major", "The major key sharing a key signature with a minor key: E flat major for C minor")),
  "a theme that sings rather than drives, but stays dark. Naming E flat minor rather than E flat major earns the mark.")

d.add_statement(4, "Heard again", "4 &middot; Everything again",
  "If this sounds familiar, it should: the pianist takes the %s and plays the whole exposition a second time. %s Use "
  "it. Listen through the repeat with the three landmarks in mind &mdash; first subject, bridge, second subject &mdash; "
  "and check that you can hear each join without looking at the numbers."
  % (dfn("repeat", "An instruction to play a section a second time before continuing"), d.ref(4)),
  "the same music in the same order. This is the free practice run the movement gives you.")

d.add_statement(5, "The Grave returns", "5 &middot; The introduction breaks in",
  "The fast music stops and the Grave comes back. %s In 1798 an introduction was disposable; Beethoven brings his "
  "back to open the %s, so the slow and fast worlds of the movement turn out to belong to each other. Its diminished "
  "sevenths return with it."
  % (d.ref(5), dfn("development", "The middle section of sonata form, where existing material is fragmented and moved through keys")),
  "the tempo collapsing. A sudden change of tempo mid-extract is almost always the Grave coming back.")

d.add_statement(6, "Development", "6 &middot; Working the material",
  "The fast tempo is running again and the development is under way. %s No new tune appears: Beethoven fragments the "
  "first subject and the bridge, passes motifs between the hands and drives them through unstable keys by %s. The "
  "recapitulation then brings the first subject home to C minor."
  % (d.ref(6), dfn("sequence", "Repeating a short idea immediately at a higher or lower pitch")),
  "short scraps of the first subject rather than the whole theme, and harmony that refuses to settle.")

d.add_statement(7, "Grave, then coda", "7 &middot; The last word",
  "The Grave appears once more, for a few bars only. %s By now the recapitulation has run its course, taking the "
  "second subject through F minor before settling in C. What follows is a short %s built from first-subject material "
  "at the same fierce tempo, ending abruptly in C minor. The dark key wins."
  % (d.ref(7), dfn("coda", "A closing passage that rounds off a movement")),
  "the moment of held-breath stillness before the final rush. Nothing brightens; the movement simply stops.")

d.add_checklist(
  "Genre: Classical solo piano sonata, first movement. Forces: one pianist. Key: C minor, with the second subject in "
  "E flat minor turning to E flat major, and F minor in the recapitulation. Metre and tempo: common time throughout, "
  "Grave against Allegro di molto e con brio. Structure: slow introduction plus sonata form, with the Grave returning "
  "at the start of the development and again before the coda. Texture: homophonic, melody over tremolo. Harmony: "
  "chromatic, with diminished sevenths. Context: 1798, Vienna, dedicated to Prince Karl von Lichnowsky.",
  "Name the section and the key together. &ldquo;It changes key&rdquo; earns little; &ldquo;the second subject "
  "arrives in E flat minor rather than the expected E flat major&rdquo; earns the mark.")

content = d.content()
exam_tip = ("<p>If an extract changes tempo partway through, the return of the Grave is the most likely answer, so "
            "learn its dotted rhythms and thick low chords well enough to name them in a second. Then say where in "
            "the structure that return falls &mdash; at the start of the development, or just before the coda &mdash; "
            "because the mark is for the structural point, not for spotting that the music slowed down.</p>")
conclusion = ("<p>You can now follow the whole movement: the Grave, the first subject over its tremolo, the second "
              "subject in the wrong minor, the exposition repeat, the Grave breaking into the development, and the "
              "last Grave before the coda. The next lesson takes the same recording element by element &mdash; "
              "dynamics, texture, tonality, harmony, melody and tempo.</p>")
description = ("Follow Beethoven's Pathetique first movement through seven landmarks, from the Grave introduction to "
               "the abrupt coda in C minor.")

flashcards = [
  {"q": "What tempo marking is given to the slow introduction of the Pathetique's first movement?", "a": "Grave."},
  {"q": "In which city and year was the Pathetique Sonata composed and published?",
   "a": "Vienna, composed in 1798 and published in 1799, dedicated to Prince Karl von Lichnowsky."},
  {"q": "In which key does the second subject first appear, and where does it go?",
   "a": "It appears in E flat minor rather than the expected relative major, then brightens into E flat major for the closing theme."},
  {"q": "What happens to the key of the second subject group when it returns in the recapitulation?",
   "a": "It appears first in F minor before resolving to C, so the return to the tonic feels hard-won."},
  {"q": "Where does the Grave material return in the movement?",
   "a": "Twice more after the opening: at the start of the development, and very briefly just before the coda."},
  {"q": "List the sections of the first movement in order.",
   "a": "Grave introduction, exposition (first subject, bridge, second subject, closing theme, repeated), Grave, development, recapitulation, Grave, coda."},
]

practice = [
  {"text": "Name the key in which the first subject of the exposition is heard.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for C minor."},
  {"text": "Describe the tonal journey of the second subject group within the exposition.", "marks": 2, "kind": "Description",
   "mark_scheme": "One mark: it begins in E flat minor rather than the expected relative major. One mark: it brightens into E flat major, in which the closing theme ends the exposition."},
  {"text": "Explain how Beethoven creates a dramatic effect at the start of the Allegro section.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: tempo changes abruptly from Grave to Allegro di molto e con brio. One mark: dynamics and texture change with it, the left hand taking up a tremolo. One mark: the shock comes from the contrast with the stillness before it, so structure itself becomes a dramatic device."},
  {"text": "Explain how the exposition repeat can help you in a listening exam.", "marks": 2, "kind": "Explanation",
   "mark_scheme": "One mark: the whole exposition is played twice, so first subject, bridge and second subject can be heard again in the same order. One mark: a second hearing lets a candidate confirm the key and character of each landmark before writing."},
  {"text": "Explain why the recurring Grave material is significant to the structure of the movement.", "marks": 4, "kind": "Explanation",
   "mark_scheme": "One mark: it returns at the start of the development. One mark: it returns again briefly before the coda. One mark: introductions of the period were not normally reused. One mark: the returns frame the movement and tie the slow and fast material into one dramatic argument."},
  {"text": "Compare the character of the first and second subjects in the exposition.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: the first subject is urgent and rising, over a tremolo accompaniment, in C minor. One mark: the second subject is smoother and more lyrical, in E flat minor. One mark: a supported comparison of mode, texture or emotional character between the two."},
]

kcs = [
  {"q": "In which key is the first movement of the Pathetique Sonata written?",
   "options": ["C minor", "E flat major", "G minor", "F minor"], "correct": 0},
  {"q": "What unusual structural feature does Beethoven include regarding the slow introduction?",
   "options": ["It is played by an orchestra", "It returns later in the movement", "It is omitted from the recapitulation", "It is played twice as fast each time"], "correct": 1},
  {"q": "What key does the second subject initially appear in during the exposition?",
   "options": ["E flat major", "E flat minor", "C major", "G minor"], "correct": 1},
  {"q": "Which piano technique creates a shuddering, orchestral effect beneath the first subject?",
   "options": ["Trill", "Tremolo", "Staccato", "Glissando"], "correct": 1},
  {"q": "What is the overall form of the first movement?",
   "options": ["Rondo form", "Theme and variations", "Sonata form with a slow introduction", "Binary form"], "correct": 2},
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
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", "pathetique_l4.html"), "w",
        encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
