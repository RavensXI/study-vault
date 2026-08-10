# Score Reading unit — student-experience audit (10 Aug 2026)

Tom, who cannot read music, reported the four `score-reading` lessons "in no way help me".
I sat all four in a headless browser as a student and examined the three score images at native
resolution. He is right, and the reasons split into three kinds. **No fixes applied yet** — the
remedy for several of these depends on a decision only Tom can make (see the last section).

Unit: `music-aqa` / `score-reading`, 4 lessons, 33 questions, 3 distinct score images.

---

## A. Wrong answer keys — a correct student is marked wrong

### A1. HIGH — Mozart time signature is marked 4/4; the score shows cut common (2/2)
`L1 bronze Q1`: "Look at Excerpt A (Mozart Symphony No.40). What is the time signature?"
Marked correct: **4/4**. Options offered: 3/4, 2/4, 4/4, 6/8.

The image (`lesson-02-score.jpg`, verified at 3x native) shows **¢** — cut common, alla breve, 2/2 —
in both the treble and bass staves, with two flats (G minor). Mozart 40 mvt 1 *is* alla breve.
So the marked answer is wrong AND the correct answer is not among the options. A student who reads
the symbol correctly cannot answer.

Worse, it contradicts the next question in the same lesson: `L1 bronze Q2` asks what "C with a line
through it" means and correctly answers **"2/2 alla breve"**. One lesson teaches ¢ = 2/2 and then
marks ¢ = 4/4.

Propagates to: the passage caption ("simple 4/4 time"), and `L1 gold Q2` whose stem reads
"Compare Excerpt A (Mozart, 4/4) and Excerpt C (Chopin, 12/8)".

### A2. HIGH — three questions ask about markings that are not in the image
`lesson-01-score.jpg` (Beethoven Allegro) contains, verified at 3x zoom across the whole image:
a treble clef, ¢, dotted minims, slurs and staccato dots. It contains **no `sf` and no hairpin**,
and in fact no dynamic markings at all.

Yet:
- `L3 bronze Q2` — "What does the marking 'sf' mean?"
- `L3 silver Q2` — "What symbol indicates a gradual increase in volume?" (answer: hairpin crescendo)
- `L3 gold Q1` — "sf marks appear frequently" (they appear zero times)
- passage caption — "Look for: **sf** (sforzando) accent markings; hairpin crescendo symbol"
- and the same false claim in the AoS1 drill L1 caption: "Note the 2/2 time signature, sf accents,
  and crescendo hairpin"

A student told to find the sf accents searches a picture that has none, and reasonably concludes
the fault is theirs.

### A3. HIGH — Chopin "dynamic marking at the start" is not a dynamic
`L3 bronze Q1`: "Look at Excerpt A (Chopin Nocturne). What dynamic marking appears at the start of
the piece?" Marked correct: **p (piano)**.
The image shows **"espress. dolce"** at the start — expression directions, not dynamics. The first
real dynamics (`cresc.`, `f`, `p`) appear in the second system, not at the start.

### A4. MEDIUM — the anacrusis claim does not match the excerpt
`L1 silver Q1`: "The piece begins with two quavers before the first full bar."
The excerpt begins with rests over accompaniment; the quaver upbeat leads into bar 2. It is an
anacrusis to the **melody**, not to the piece. As written, a student comparing the sentence with
the image sees a contradiction.

---

## B. The notation is not legible, and cannot be enlarged

Measured in the browser at a 1440x900 viewport:

| Lesson | Image | Natural | Rendered | Scale |
|--------|-------|---------|----------|-------|
| L1 | lesson-06-score.jpg | 878x493 | 377x213 | 0.43 |
| L2 | lesson-02-score.jpg | 1200x610 | 475x243 | 0.40 |
| L3 | lesson-01-score.jpg | 1200x216 | **475x87** | 0.40 |
| L4 | lesson-02-score.jpg | 1200x610 | 475x268 | 0.45 |

**Nothing is clickable and there is no lightbox.** `practice.html` does not load `main.js`, which is
where the lightbox lives, so the zoom that article lessons have simply does not exist on practice
pages. Asking a student to identify an articulation mark from an 87-pixel-tall strip, with no way to
enlarge it, is not a fair test at any level of musical literacy.

The images are also raw 19th-century engravings — fingering numbers, pedal marks and editorial
marks all compete for attention with the thing being asked about.

## C. Nothing on any score is annotated

No arrow, circle, highlight or label anywhere. Every question of the form "Look at Excerpt X and
find Y" expects the student to already know where Y lives on a stave. That is precisely the skill
the lesson claims to teach, so the lesson assumes its own outcome.

---

## D. The deeper problem: the unit does not actually teach score reading

Of the 33 questions, 20 are framed "Look at Excerpt X" — but most of those are **definition
questions answerable from the method card without looking at the score at all**: what `sf` means,
what ¢ means, how sforzando differs from forte, how many quavers are in a compound beat. The
remaining 13 never mention a score.

So the unit is largely a **terminology quiz wearing score-reading clothes**. That explains Tom's
experience exactly: a non-reader is never given a way in, because the lesson never actually requires
the notation to be read — and therefore never teaches how to read it. The score sits alongside as
decoration.

---

## Recommendation

The spec requires this: Section A can show up to 12 bars of staff notation. So the unit must stay.
But it needs a different approach, and there are three levels of ambition.

**1. Minimum, non-negotiable regardless of approach.** Fix A1-A4 (four wrong or unanswerable keys),
and correct the two captions that promise markings the images do not contain. These are wrong under
any design.

**2. Make the existing format usable.** Add a lightbox/zoom to practice pages (the component exists
in `main.js`; practice.html would need it or a small standalone equivalent), and render the score at
its natural width rather than 40%. Cheap, and it removes the "I literally cannot see it" barrier.

**3. The real fix — annotate the notation.** Replace raw scans with clean, purpose-made excerpts
where the element under discussion is visibly marked: a coloured ring round the time signature, a
labelled arrow to the anacrusis, the sf accents highlighted. Then teach the symbol *on the image*
before testing it. This is what Tom's instinct asked for, and it is the only version that helps a
student who cannot yet read music.

For (3) the images should be generated rather than scanned, so the annotation is authored, correct
and legible. Options worth costing: LilyPond or Verovio/MusicXML rendering to SVG (free, exact,
scriptable, and SVG stays sharp at any zoom — and inline SVG already works in practice display, see
[[reference_practice_display_inline_svg]]). That also fixes B and C at the same time, because a
generated SVG can be rendered at any size with labels baked in.

Recommendation: do (1) now, and treat (2)+(3) as one small build — the unit is only 4 lessons and
3 images, so this is a contained piece of work, not a rebuild of the subject.
