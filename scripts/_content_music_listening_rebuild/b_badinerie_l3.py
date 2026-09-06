# -*- coding: utf-8 -*-
"""music-eduqas / aos1-forms-and-devices / L3 -- Badinerie, STRUCTURAL walk.
Video BsiqjGgwuU8 (Netherlands Bach Society), 1:41 = 101 s, with a title card
before the music.
Pin times: 0:07 the music starts (3/3), 0:22 the A section is repeated (3/3),
0:37 the B section begins (3/3), 1:01 the B section is repeated (2/3), 1:24 the
last chord (3/3). The arithmetic corroborates them: A runs 15 s and its repeat
15 s, B runs 24 s and its repeat 23 s, matching a 16-bar A against a longer B.
FACT FIXES carried into this deck (the pair contradicted itself before):
  * the A section ends in F sharp minor, the DOMINANT minor, not the relative
    major; F sharp minor does not share a key signature with B minor.
  * the B section begins from that F sharp minor and passes through related
    keys including D major, the relative major, on its way home to B minor.
The board is never named."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from deck import Deck, dfn, patch, build_questions, check_plain

BACKUP = "music-eduqas__aos1-forms-and-devices__L03"
d = Deck(lesson_id="bf2df88f-9c27-481e-b3c6-7fe4fc834b7d",
         subject="music-eduqas", unit="aos1-forms-and-devices", lesson_no=3,
         yt="BsiqjGgwuU8", dur=101, track_label="Badinerie", board="eduqas",
         credit="Performance by the Netherlands Bach Society, streamed from YouTube &mdash; not hosted by "
                "StudyVault. Bach: Badinerie, Orchestral Suite No. 2 in B minor, BWV 1067. A title card runs "
                "before the music.")
TITLE = "Bach: Badinerie from Orchestral Suite No. 2 — Guided Listening"

d.pins = [
    ("t1c1", 7,  "A section",   "The flute launches straight into semiquavers over strings and continuo, in B minor."),
    ("t1c2", 22, "A repeated",  "Back to the beginning. The same music, and your second chance to hear the key change."),
    ("t1c3", 37, "B section",   "The second half begins from the key A ended in, and starts working its way home."),
    ("t1c4", 61, "B repeated",  "The longer half, heard again. Listen for any extra decoration the players add."),
    ("t1c5", 84, "Last chord",  "A firm perfect cadence in B minor. Under a minute and a half of music, all told."),
]

d.add_cover(
  "Bach: Badinerie",
  [
    "The last movement of Bach&rsquo;s Orchestral Suite No. 2 in B minor, BWV 1067, for solo flute with strings and "
    "%s. B minor, 2/4, fast, and cast in %s: two halves, each played twice. The French title means playful jesting."
    % (dfn("continuo", "The continuous bass line and chords of Baroque music, usually cello with harpsichord"),
       dfn("binary form", "A two-part structure, A and B, each usually repeated, giving A A B B")),
    "A Baroque %s collected stylised dances. Around its four standard movements composers slipped in lighter "
    "%s &mdash; minuets, gavottes, a badinerie &mdash; and this one has outgrown the suite it belongs to."
    % (dfn("suite", "A collection of contrasting dance-based movements, usually sharing one key"),
       dfn("galanteries", "Optional lighter dance movements inserted into a Baroque suite")),
    "Press play and the cards follow the music. Tap any number to jump to that moment.",
  ])

d.add_statement(1, "A section", "1 &middot; Straight in",
  "No introduction: the flute is already running. %s The movement opens in the %s, B minor, with the solo line in "
  "continuous semiquavers over strings and continuo. Before this half is over the harmony will have moved to F sharp "
  "minor, the %s, and closed there with a perfect cadence."
  % (d.ref(1), dfn("tonic", "The home key of a piece, to which the harmony finally returns"),
     dfn("dominant minor", "The minor key built on the fifth degree of the scale: F sharp minor in B minor")),
  "the flute never stopping. Fix the opening shape now &mdash; you will hear it again in about fifteen seconds.")

d.add_statement(2, "A repeated", "2 &middot; The same half again",
  "The music jumps back and plays the first half again. %s That repeat is written into the form, not a "
  "performer&rsquo;s choice: %s means A A B B. Use the second hearing to follow the journey from B minor to the "
  "cadence in F sharp minor, which is the point of this half."
  % (d.ref(2), dfn("binary form", "A two-part structure, A and B, each usually repeated")),
  "the arrival on a new key at the end of the half. Naming that key is what turns a form label into a mark.")

d.add_statement(3, "B section", "3 &middot; The second half",
  "The B section begins from the F sharp minor that A reached. %s It does not stay: Bach steers it through related "
  "keys, touching D major, the %s of B minor, before turning firmly for home. Nothing from the opening is restated "
  "wholesale, which is exactly what separates binary form from %s."
  % (d.ref(3), dfn("relative major", "The major key sharing a key signature with a minor key: D major for B minor"),
     dfn("ternary form", "A three-part structure, A B A, in which the opening section returns")),
  "the harmony travelling. This half is longer than the first, and it is longer because it is doing more work.")

d.add_statement(4, "B repeated", "4 &middot; And again",
  "The second half is played through a second time. %s In Baroque performance a repeat is an invitation: players "
  "often add %s the second time round, so listen for anything decorative that was not there before. The written "
  "notes are identical; the performance need not be."
  % (d.ref(4), dfn("ornaments", "Small decorative notes added to a melody, such as trills and mordents")),
  "small differences between the two hearings. If you hear none, that is an observation too.")

d.add_statement(5, "Last chord", "5 &middot; Home",
  "The music lands on a perfect %s in B minor, the key it started in. %s The whole movement has lasted under a "
  "minute and a half, and in that time it has left the tonic, cadenced in a related key, wandered further and "
  "returned. That departure and return is what binary form is for."
  % (dfn("cadence", "The chord progression that closes a musical phrase or piece"), d.ref(5)),
  "how decisively it stops. Then say the shape out loud: A, A, B, B, B minor to F sharp minor and back.")

d.add_checklist(
  "Genre: the closing galanterie of a Baroque orchestral suite. Forces: solo transverse flute, first and second "
  "violins, violas, and continuo of cello with harpsichord. Key: B minor, moving to F sharp minor, the dominant "
  "minor, at the end of A, and back through related keys including D major during B. Metre and tempo: 2/4, fast. "
  "Structure: binary form, A A B B, with no restatement of the opening inside B. Texture: melody-dominated "
  "homophony with occasional imitation. Dynamics: terraced. Context: Bach, BWV 1067, the only one of his four "
  "orchestral suites led by a solo flute.",
  "Name the keys, not just the form. &ldquo;It is in binary form&rdquo; earns little; &ldquo;section A modulates "
  "from B minor to F sharp minor and section B works back to B minor&rdquo; earns the mark.")

content = d.content()
exam_tip = ("<p>The commonest error on this movement is calling it ternary form, because both binary and ternary "
            "have repeated sections. The test is simple: does the opening material return in full at the end? Here "
            "it does not, so the answer is binary. Then add the keys &mdash; B minor to F sharp minor across A, and "
            "back to B minor across B &mdash; because form questions are marked on the harmonic detail.</p>")
conclusion = ("<p>You can now follow the movement through its four playings: A, A, B, B, with the first half ending "
              "in F sharp minor and the second half working back to B minor for the final cadence. The next lesson "
              "takes the same recording element by element &mdash; the flute writing, the texture, the key scheme, "
              "the dynamics, and the metre and tone colour.</p>")
description = ("Follow Bach's Badinerie through its binary form, A A B B, from the flute's first semiquaver to the "
               "final cadence in B minor.")

flashcards = [
  {"q": "What is a Baroque suite?",
   "a": "A collection of contrasting stylised dance movements, usually sharing a key, written for entertainment at court or in concert."},
  {"q": "What does 'Badinerie' mean and where does it appear in Bach's suite?",
   "a": "It means playful jesting or banter. It is the final movement of Bach's Orchestral Suite No. 2 in B minor, BWV 1067."},
  {"q": "How is the Badinerie scored?",
   "a": "For solo transverse flute with strings, first and second violins and violas, and continuo of cello with harpsichord."},
  {"q": "Describe the binary form key scheme of the Badinerie.",
   "a": "Section A moves from the tonic B minor to F sharp minor, the dominant minor. Section B begins there and returns through related keys, including D major, to B minor. Both sections are repeated, giving A A B B."},
  {"q": "How do you tell binary form from ternary form by ear?",
   "a": "In ternary form the opening material returns in full at the end. In binary form it does not; the music simply moves between two key areas and closes in the tonic."},
  {"q": "What is a galanterie in a Baroque suite?",
   "a": "An optional lighter dance movement, such as a minuet, gavotte or badinerie, inserted alongside the four standard dances."},
]

practice = [
  {"text": "State the meaning of the title 'Badinerie'.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for playful jesting, banter, or an equivalent translation."},
  {"text": "Name the solo instrument featured throughout Bach's Badinerie.", "marks": 1, "kind": "Identification",
   "mark_scheme": "One mark for flute. Accept traverso or transverse flute."},
  {"text": "Identify the form used in the Badinerie and explain how you can tell it apart from ternary form.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: binary form, or A A B B. One mark: each of the two sections is repeated. One mark: the opening material is not restated in full at the end, which is what would make it ternary."},
  {"text": "Describe the key scheme of the Badinerie's two sections.", "marks": 2, "kind": "Description",
   "mark_scheme": "One mark: section A moves from B minor to F sharp minor, the dominant minor. One mark: section B begins in F sharp minor and returns through related keys, including D major, to B minor."},
  {"text": "Explain how the scoring of the suite supports the character of the Badinerie.", "marks": 3, "kind": "Explanation",
   "mark_scheme": "One mark: the solo flute carries rapid, virtuosic melodic lines. One mark: strings and continuo supply harmonic support and occasional imitation. One mark: the combination gives the light, playful, energetic effect the title promises."},
  {"text": "Explain how rhythm and texture combine to create the playful character of the Badinerie.", "marks": 4, "kind": "Explanation",
   "mark_scheme": "One mark: continuous semiquaver movement at a fast tempo. One mark: scalic and arpeggio figures extended by sequence. One mark: a mostly homophonic texture with brief imitation between flute and violins. One mark: terraced dynamics adding sudden contrast, all linked to the light, teasing character."},
]

kcs = [
  {"q": "What does the French word 'Badinerie' mean?",
   "options": ["Playful jesting or banter", "Solemn procession", "Mournful lament", "Grand celebration"], "correct": 0},
  {"q": "Which instrument is the principal melodic voice in the Badinerie?",
   "options": ["Oboe", "Solo flute", "Violin", "Harpsichord"], "correct": 1},
  {"q": "What form is the Badinerie written in?",
   "options": ["Ternary form", "Rondo form", "Binary form", "Theme and variations"], "correct": 2},
  {"q": "In which key does the Badinerie begin?",
   "options": ["D major", "B minor", "G major", "F sharp minor"], "correct": 1},
  {"q": "Which group provides the bass line and harmonic filling in the Badinerie?",
   "options": ["Continuo", "Woodwind section", "Brass section", "Percussion"], "correct": 0},
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
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", "badinerie_l3.html"), "w",
        encoding="utf-8").write(content)
patch(d, payload, apply="--apply" in sys.argv)
