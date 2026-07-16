# Board Fan-Out — Maths AQA / OCR / Eduqas (full guided conversion)

You are converting ONE maths practice lesson on a non-Edexcel board to the
complete guided-learning + diagrams format that Tom approved on maths-edexcel.
This is the FULL stack in one pass. Read these two specs first; they are the
law and this file only adds board-specific deltas:

1. `C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\SPEC.md`
   (pedagogy model, per-lesson procedure 1-9, style law, ship gate, checker brief)
2. `C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\SPEC_DIAGRAMS.md`
   (exam-realism figures: when to draw, SVG rules, chart configs, figure law)

## Deltas for this run

- **No prior audit exists for these boards. Trust NOTHING.** On Edexcel,
  3.6% of stored solutions were flat wrong, simultaneous-equations lessons
  (L09/L10) had solutions that satisfied only one equation, several problems
  were degenerate on non-calculator settings, and duplicate answers appeared
  within tiers. These boards were built by the same original pipeline:
  expect the same diseases. Fresh-solve EVERY problem from its display
  before anything else; fix with minimal clean-answer edits.
- **Do diagrams in the same pass** (SPEC_DIAGRAMS rules) for visual lessons:
  geometry and graphs units, probability-statistics, and any other problem
  that describes a printable figure. Textual units (most of number, algebra,
  ratio) usually need none: apply the exam-realism test.
- **Simultaneous equations lessons**: algebra-L09 uses `input_type:
  "xy_pair"` (ordered x-then-y boxes) on every problem; algebra-L10 asks for
  the two x-values via `input_type: "two_solutions"` with the display ending
  "Give the two x-values." Copy the Edexcel exemplar's approach exactly:
  `C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_audit\_l09_rebuilt_practice_data.json`
- **Method cards / tier guides are sidebar content.** The player fixed the
  layout, but respect the medium: guide steps within budget (validator
  enforces 115 words/card), example content lines SHORT (break chained
  equalities across steps rather than one long line), nothing wider than a
  ~250px column when rendered.
- **Misconception expects**: these boards never got the enrichment pass.
  Derive every expect by committing the error (SPEC.md section 2); rewrite
  any message containing an em dash.
- **Openers must be fresh for your lesson's topic** (you may take the same
  concrete ANGLE as the Edexcel sibling lesson, but write it yourself and
  verify your own numbers). Never copy numbers blindly: your board's bank
  differs.

## Files for YOUR board (substitute {board} = maths-aqa | maths-ocr | maths-eduqas)

- Work-list (lesson ids): `C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_worklist_{board}.json`
- Pre-run rollback dump: `_pre_dump_{board}.json` (same directory)
- Ship gate paths: shard `lesson_{board}_<KEY>.json` and changes
  `changes_{board}_<KEY>.json` in the `_maths_boards` directory.
- Validator (must PASS before PATCH):
  `python "C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\_validate_guided.py" <shard>`

Everything else (data access, PATCH-only-practice_data, no git, no bash
heredocs for backslash content, write .py files) is as SPEC.md says.

## CHECKER BRIEF

Run BOTH checker briefs against the LIVE row: the maths/walk checks from
SPEC.md (fresh-solve every problem, recompute every box, reproduce every
expect, completion boundaries, opener quality, preservation vs the board's
pre-dump) AND the figure checks from SPEC_DIAGRAMS.md (every label vs the
numbers, plotted points satisfy equations, theme safety, missed-figure
sweep on visual lessons). Report defects with exact paths. FAIL on any maths
error, non-computing box, non-reproducing expect, label mismatch, or lost
preserved fields.
