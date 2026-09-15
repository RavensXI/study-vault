# Widget reuse check - subjects built or extended since 1 September 2026

Run on 15 September 2026 with `scripts/widget_pipeline/match_existing_widgets.py`.
Nothing is wired. Tom approves each pairing. Then a human edits the `MAP` in
`js/widget-embed.js`.

## What the fleet holds

91 interactives are built. 279 lessons carry one (280 strips; one lesson carries
two). `widget_catalogue.json` classes each one:

| Class | Count | What it means |
|---|---|---|
| `portable` | 81 | The model computes its own content. Drop it into any lesson that teaches the idea. |
| `variant_needed` | 3 | The mechanism carries, but the deck names one context. A second deck behind `ctx.variant` is necessary. |
| `content_bound` | 7 | The widget IS one named case (Macbeth, Othello, Kenilworth, the Armada, Salamis, the tholos, Germany 1918-33). |

The high `portable` count is the finding. Most of the fleet is reusable.

## The eight subjects

| Subject | Lessons read | Skipped | Candidates found | Proposed | Bands |
|---|---|---|---|---|---|
| statistics-edexcel | 9 | 19 practice | 5 | **3** | 3 high |
| media-studies-eduqas | 22 | 0 | 26 | **4** | 4 high |
| latin-eduqas | 21 | 12 practice | 0 | **0** | - |
| geography-eduqas (`fieldwork-enquiry`) | 5 | 0 | 2 | **2** | 1 high, 1 medium |
| computer-science-edexcel (`programming-python`) | 8 | 0 | 0 | **0** | - |
| music-eduqas | 10 | 18 practice, 4 listening | 13 | **3** | 3 high |
| music-ocr | 16 | 17 practice, 4 listening | 30 | **6** | 3 high, 1 medium, 2 low |
| music-edexcel | 4 | 11 practice, 16 listening | 6 | **3** | 2 high, 1 low |

21 pairings in total. Listening lessons and practice lessons are excluded by
design: they have no article body to anchor a strip to.

"Candidates found" is every pairing above the threshold. "Proposed" is what
survives the two caps. `BUILD_GUIDE.md` section 0 allows about one lesson in
three to carry an interactive, and the live MAP never puts one widget in more
than two lessons of a subject. Each report lists the rest under "Held back".

## The strongest 10 pairings

Each anchor below is quoted from that lesson's `content_html`. The strip goes in
immediately **before** the named heading.

| # | Score | Widget | Lesson key | Anchor heading |
|---|---|---|---|---|
| 1 | 1.00 | `stratification-not-a-sampling-method` | `statistics-edexcel/planning-designing-enquiry/4` | "Stratifying by More Than One Category (Higher)" |
| 2 | 0.99 | `vertical-vs-horizontal-integration` | `media-studies-eduqas/theoretical-framework/4` | "Convergence Across Platforms and Borders" |
| 3 | 0.96 | `time-series-trend-vs-noise` | `statistics-edexcel/interpreting-results-sec/3` | "Calculating a Moving Average" |
| 4 | 0.96 | `media-construction-of-reality` | `media-studies-eduqas/theoretical-framework/3` | "Selection, Construction and Mediation" |
| 5 | 0.94 | `sonata-form-key-relationships` | `music-edexcel/aos1-instrumental-music/1` | "Set Work Spotlight: Beethoven’s Pathétique Sonata, First Movement" |
| 6 | 0.93 | `media-construction-of-reality` | `media-studies-eduqas/set-products-language-representation/3` | `$end` (append after the last section) |
| 7 | 0.93 | `timbre-integral-to-composition` | `music-eduqas/aos3-film-music/2` | "Releasing Tension: The Journey to Resolution" |
| 8 | 0.93 | `timbre-integral-to-composition` | `music-ocr/aos4-film-music/2` | "Releasing Tension: The Journey to Resolution" |
| 9 | 0.93 | `sonata-form-key-relationships` | `music-eduqas/aos1-forms-and-devices/1` | "Rondo Form: A Recurring Refrain" |
| 10 | 0.92 | `vertical-vs-horizontal-integration` | `media-studies-eduqas/set-products-industries-audiences/3` | "Convergence and Cross-Media Promotion" |

All ten widgets are `portable`. No data variant is necessary. Not one of the 21
proposals needs a variant.

## Per subject, with my honest confidence

### statistics-edexcel - 3 proposed, all strong

Both statistics widgets were built for `statistics-aqa`. The Edexcel spec
teaches the same two ideas.

- **`stratification-not-a-sampling-method` -> `planning-designing-enquiry/4`**
  ("Sampling Methods and Stratification"). Score 1.00. The lesson title holds
  three of the widget's keywords. The AQA twin is wired at the same lesson
  number. I am confident.
- **`time-series-trend-vs-noise` -> `interpreting-results-sec/3`** ("Time
  Series, Index Numbers and Rates of Change"). Score 0.96. The lesson has a
  "Calculating a Moving Average" heading, and the widget teaches the 4-point
  moving average. I am confident.
- **`stratification-not-a-sampling-method` -> `planning-designing-enquiry/3`**
  ("Primary and Secondary Data Sources"). Score 0.89. This is the weakest of the
  three. The lesson covers census against sample and data sources, not
  stratification. The keyword hits are real but general: bias, census,
  population. **My recommendation: reject this one.** Keep the widget for lesson
  4 only.

19 of the 28 Statistics lessons are practice format. They hold no article body,
so no strip can go in them.

### media-studies-eduqas - 4 proposed, all strong

Two widgets built for `media-studies-aqa` transfer cleanly. Neither names a
brand or a set product.

- **`vertical-vs-horizontal-integration` -> `theoretical-framework/4`** ("Media
  Industries: Ownership, Funding and Regulation"). Score 0.99. The lesson has a
  "Vertical and Horizontal Integration" section. The widget's own chain is
  production, distribution, exhibition. I am confident.
- **`media-construction-of-reality` -> `theoretical-framework/3`**
  ("Representation, Stereotypes and Gender Theory"). Score 0.96. The anchor
  heading is "Selection, Construction and Mediation". I am confident.
- **`media-construction-of-reality` -> `set-products-language-representation/3`**
  (Newspaper front pages: The Guardian and The Sun). Score 0.93. Two accurate
  front pages that build different versions of one event is this widget's task
  frame exactly. I am confident. The anchor computes as `$end`, so the strip goes
  after the last section.
- **`vertical-vs-horizontal-integration` -> `set-products-industries-audiences/3`**
  (Film Industry: No Time to Die). Score 0.92. Sound, but it puts the widget in
  the subject a second time. Wire it only if Tom wants both.

22 more pairings were found and held back. They are mostly the same two widgets
landing on further industry and representation lessons.

### latin-eduqas - 0 proposed, and that is correct

Latin maps to the `classics` family. Only two classics widgets exist:
`tholos-engineered-structure` (a Mycenaean tomb) and
`trireme-coordinated-maneuvering` (the strait at Salamis). Both are Greek. Both
are `content_bound`. Eduqas Latin teaches Roman civilisation, accidence, syntax
and two set narratives. Nothing matched, even at a threshold of 0.10.

This is a real gap, not a tool failure. If Latin is to get an interactive,
someone must build it. The likely subject is word order and case endings: a
student can read a Latin sentence correctly and still picture the grammar
wrongly, which is the `BUILD_GUIDE.md` section 0 test.

### geography-eduqas, `fieldwork-enquiry` - 2 proposed, 1 strong

This is the best cross-subject reuse in the run. The statistics sampling widget
serves geography fieldwork.

- **`stratification-not-a-sampling-method` -> `fieldwork-enquiry/1`** ("The
  Geographical Enquiry Process"). Score 0.68, band high. The lesson has a
  "Sampling: You Cannot Measure Everything" section and a "Justifying Sample
  Size and Method" heading. I am confident about the idea.
- **`stratification-not-a-sampling-method` -> `fieldwork-enquiry/3`**
  ("Conclusions, Evaluation & UK Decisions"). Score 0.54, band medium. Sampling
  is evaluated here, not taught. **My recommendation: reject.**

One qualification, and it is mine, not the score's. The widget's populations are
a school, a gym, a hospital, a college and a rowing club. A geography student
meets sampling at a transect, a quadrat or a pedestrian count. The widget is
correct as it stands and I would wire it. A fieldwork deck behind `ctx.variant`
would read better, and it is a small build.

`geography-eduqas` already carries two interactives in
`landscapes-physical-processes`, so the subject is not short of them.

### computer-science-edexcel, `programming-python` - 0 proposed, and that is correct

The unit teaches Python syntax: data types, selection and iteration, string
handling, lists, files, subprograms, `.format`, library modules. The three
computing widgets teach binary search, the fetch-execute cycle and audio
sampling. None of them belongs in a syntax lesson.
`binary-search-requires-sorted-data` is already wired to
`computer-science-edexcel/computational-thinking/4`, which is where it belongs.

### music-eduqas, music-ocr, music-edexcel - 12 proposed, 8 strong

This is the largest win. Three music widgets were built for one board each, and
all three are model-driven. `sonata-form-key-relationships` does semitone
arithmetic from any home key. `timbre-integral-to-composition` works from
standard instrument ranges. `small-ensemble-full-sound` works from a register
map. None of them names a set work.

Strongest:

- **`sonata-form-key-relationships` -> `music-edexcel/aos1-instrumental-music/1`**,
  anchor "Set Work Spotlight: Beethoven’s Pathétique Sonata, First Movement".
  Score 0.94. The lesson has a "Sonata Form and the Fortepiano" section.
- **`sonata-form-key-relationships` -> `music-eduqas/aos1-forms-and-devices/1`**,
  anchor "Rondo Form: A Recurring Refrain". Score 0.93. The widget covers binary,
  ternary and rondo beside sonata form, which is this lesson exactly.
- **`timbre-integral-to-composition` -> `music-eduqas/aos3-film-music/2`** and
  **-> `music-ocr/aos4-film-music/2`**, both anchored at "Releasing Tension: The
  Journey to Resolution". Score 0.93 each. They are the same film-music lesson on
  two boards.
- **`small-ensemble-full-sound` -> `music-edexcel/aos4-fusions/1`** (0.88) and
  **-> `music-ocr/aos5-conventions-of-pop/3`** (0.81). Both teach how few players
  fill a texture.

Weaker, with my recommendations:

- `small-ensemble-full-sound` -> `music-eduqas/aos4-popular-music/1` (0.82). The
  keywords sit in the title but they are general: melody, accompaniment,
  texture. Accept if Tom wants a pop-texture interactive. It is defensible.
- `timbre-integral-to-composition` -> `music-ocr/aos2-the-concerto-through-time/3`
  (0.75, the Romantic concerto). Reasonable. Timbre and orchestration are taught
  there.
- `small-ensemble-full-sound` -> `music-ocr/aos5-conventions-of-pop/1` (0.57,
  medium). Borderline. **Reject.** It repeats the widget in the same unit.
- `sonata-form-key-relationships` -> `music-ocr/aos2-the-concerto-through-time/4`
  (0.45, low). Every keyword hit is in the body, none in a heading. The lesson
  teaches unfamiliar-extract skills. **Reject.**
- `adsr-simultaneous-shaping` -> `music-ocr/aos3-rhythms-of-the-world/1` (0.32,
  low). **Reject. This is a false positive.** The lesson covers raga, tala and
  bhangra. The words "attack", "sustain" and "synthesiser" occur in the prose,
  but the widget teaches a synthesiser envelope.
- `small-ensemble-full-sound` -> `music-edexcel/aos2-vocal-music/1` (0.32, low).
  **Reject.** Body hits only.

Most music lessons are listening lessons or practice lessons, so the article
pool is small: 4 lessons on Edexcel, 10 on Eduqas, 16 on OCR.

## What blocks reuse

1. **Seven widgets are locked to one named case.** `witches-...` (Macbeth),
   `iago-...` (Othello), `kenilworth-...`, `armada-...`, `trireme-...`
   (Salamis), `tholos-...` (Mycenae) and `nazi-rise-...` (Germany 1918-33). They
   travel to boards that teach the same case, and nowhere else.
2. **Three widgets need a second data deck to travel.**
   `tactical-vs-strategic-victory` is the only one that already reads
   `ctx.variant` (decks `ww1` and `vietnam`). `holderness-hard-defences` models
   one named coastline. `film-colour-as-narrative-device` writes every round
   around Skyfall, so Eduqas Media, with different set products, cannot take it
   as built.
3. **Whole families own no widget.** Latin and the rest of `classics` hold only
   two Greek case studies. English Language, Maths and Sport Science hold none.
   Matching cannot fix that.
4. **Listening and practice lessons cannot take a strip.** They have no article
   body. That removes most of the music corpus and two thirds of Statistics.

## Two hygiene findings, for Tom

These came out of validating the matcher. Neither is mine to fix.

1. **A probable mis-wiring in the live MAP.** `js/widget-embed.js:1128` puts
   `conservation-of-energy-dispersal` - a kettle, a hoist and a braking bike -
   on `science-ocr/biology-paper-2/1`, which is an Ecosystems lesson. It is the
   only one of the 280 placements that scores zero against its own lesson.
2. **One build is wired to nothing.** `demand-curve-movement-vs-shift` is
   superseded by `curve-movement-vs-shift`, which covers supply as well and
   holds the three `economics-aqa` placements. The old file can go.

## How far the matcher can be trusted

I checked it against the 280 placements Tom has already approved. For each one I
asked whether the tool would have found that widget for that lesson.

| Check | Result |
|---|---|
| Pairs scored at all | 279 of 280 |
| Scored "high" | 266 |
| Correct widget ranked first | 255 |
| Correct widget in the top three | 279 |
| Computed anchor identical to the approved one | 226 (81%) |

The single miss is the suspected mis-wiring above. The anchor agrees with Tom's
own choice four times in five. The other fifth is a different real heading in the
same lesson, which is a judgement call, not an error. Every anchor in this run
was checked back against its lesson's own headings, including a check for an
earlier heading that would shadow it by prefix. None failed.

## Files

- `scripts/widget_pipeline/widget_catalogue.json` - 91 rows, one per widget.
- `scripts/widget_pipeline/match_existing_widgets.py` - the matcher.
- `scripts/widget_pipeline/matches/<slug>.md` and `.json` - this run.
- `docs/PIPELINE.md` - Phase 5b says when the check runs in a build.
