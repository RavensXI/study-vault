# Diagram Pass — Maths Edexcel (exam-realism figures)

You are adding figures to ONE already-converted guided-learning lesson.
Tom's rule: **draw wherever the exam paper would print a figure.** A GCSE
student should see what they'd see in the exam: labelled triangles, shapes,
circle-theorem figures, actual graphs, tree/Venn diagrams, box plots. Read
`SPEC.md` in this directory first for house style (no em dashes, unicode,
GCSE voice) and data access (Supabase REST, PATCH practice_data only).

## The two mechanisms (both already supported by the player)

1. **Chart.js config in `problem.chart`** for anything with x-y axes: linear /
   quadratic / cubic / reciprocal / trig graphs, real-life graphs,
   scatter/cumulative-frequency curves. Some problems already have one (see
   graphs-L01, probability-statistics-L05 for live examples). Schema example:

   {"type": "scatter", "data": {"datasets": [{"type": "line", "data":
   [{"x":0,"y":1},...], "tension": 0, "fill": false, "borderColor":
   "#3b82f6", "pointRadius": 5, "pointBackgroundColor": "#3b82f6"}]},
   "options": {"scales": {"x": {"min":-1,"max":5,"ticks":{"stepSize":1},
   "grid":{"color":"rgba(0,0,0,0.05)"},"title":{"text":"x","display":true}},
   "y": {...}}}}

   Use `tension: 0.35`-ish for smooth curves, 0 for straight lines. Plot
   enough points that the curve is faithful (quadratics: 9+ points).

2. **Inline SVG at the START of `problem.display`** (before the question
   text) for geometric figures: triangles, rectangles/compound shapes,
   solids (isometric-ish cuboids/cylinders are fine drawn simply), circle
   theorems, transformation grids, vectors on grids, angle diagrams, Venn
   diagrams, probability trees, box plots, pie charts.

## SVG rules (validator-enforced where possible)

- Root tag: `viewBox`, `role="img"`, `aria-label="..."` (say what it shows).
- Self-contained: no external refs, no scripts. Keep each figure lean
  (typically < 3KB).
- **Theme-safe**: all `<text>` uses `fill="currentColor"`; outline strokes
  use `currentColor`; region fills use soft colours with `fill-opacity="0.3"`
  (e.g. #60a5fa, #f59e0b, #34d399) so they read on light AND dark themes.
  Never hard-code near-black text fills.
- Labels in Inter, font-size 10-12 within a ~240-260 viewBox width. The
  player sizes figures to max-width 280px; design for legibility at that.
- Angle arcs for angle questions; small square for right angles; tick marks
  for equal sides; arrows for parallel lines and vectors. Exam conventions.
- Where a figure is deliberately not to scale (most triangles), add the exam
  caption inside the display after the svg:
  `<span class="figure-caption">Diagram not drawn accurately</span>`

## The one law: THE FIGURE MUST MATCH THE NUMBERS

A mislabelled diagram is worse than none. Every number shown in the figure
must appear in (or follow from) the problem text; the unknown the student
finds is marked `?` or with its letter. Generate figures PROGRAMMATICALLY
from the problem's own values (write a Python script that emits the SVG per
problem from its numbers), then re-read each figure against its problem
text. Angles drawn should be roughly plausible (a 30° angle should look
acute) even when not to scale.

## Where to add (and where not)

- Add: any problem whose text describes a shape, angle set, graph, tree,
  Venn, chart, or grid. Also opener/teach-walk displays that describe a
  scene a figure would make concrete (see geometry-L05's opener as the
  reference implementation; note its text fills predate the currentColor
  rule, yours must use currentColor).
- Do NOT add decoration to problems that are genuinely textual (pure
  calculation, "find the gradient between two given points" is fine without
  a figure if coordinates are given, but a line ON a grid is better when the
  question says "the graph shows").
- Do not change any question text, solutions, guided steps, hints, or
  misconceptions in this pass unless the figure exposes an inconsistency;
  if it does, fix minimally and note it in your changes file.
- If the lesson already has `chart` on a problem, keep it (improve only if
  wrong).

## Ship gate

1. Write updated practice_data to `lesson_<KEY>_diagrams.json` in this
   directory; run `_validate_guided.py` on it until PASS.
2. PATCH live. Write `changes_<KEY>_diagrams.json`:
   {"key", "figures_added": [{tier, index, kind: "svg"|"chart", what}],
    "opener_touched": bool, "notes"}

## CHECKER BRIEF (diagram pass)

Fetch the LIVE row. For every figure (svg or chart):
1. Cross-check every visible number/label against the problem text and
   solutions. Any mismatch = FAIL.
2. Geometry sanity: right angles marked where claimed, the `?` marks the
   thing actually asked for, angle sizes plausibly shaped, graph points
   satisfy the stated equation (recompute several points per curve).
3. Theme safety: no hard-coded dark text fills in <text>; region fills use
   opacity. External refs = FAIL.
4. Coverage judgement: list problems that describe a printable figure but
   still lack one (missed opportunities) in findings; 2+ clear misses = FAIL.
5. Run the validator on the live data.
Return: key, pass, maths_errors (label mismatches count), findings with
exact paths.
