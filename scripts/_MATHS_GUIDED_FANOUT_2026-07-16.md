# Maths Edexcel Guided-Learning Fan-Out — 16 July 2026

Tom's brief (overnight): expand the approved L09 guided-learning pilot across
all maths Edexcel lessons. Fable 5 writes the spec and QAs; Opus 4.8 agents do
the work. Two-for-one confirmed before starting: there is exactly ONE
`maths-edexcel` subject (school_id NULL); Unity College subscribes to the same
rows the free tier serves.

## Result

**All 48 maths-edexcel lessons are now live in the guided-learning format.**
Every lesson has: a concrete opener puzzle, two doors, per-tier teach walks,
machine-checkable guided steps on every non-MC problem (completion problems +
"do this one with me"), tier guides, per-problem hints, slim method card,
honest misconception expects, and zero em dashes.

## How it ran

- **Spec** (`scratchpad/_maths_guided/SPEC.md`): pedagogy model, per-lesson
  procedure, opener quality bar, completion-boundary rule, style law, checker
  brief. **Validator** (`_validate_guided.py`): deterministic gate agents had
  to pass before PATCHing.
- **Pipeline per lesson**: Opus author (follows spec, fresh-solves the bank,
  patches live) → independent adversarial Opus checker (re-solves every
  problem, recomputes every guided box, reproduces every misconception
  expect) → revision + re-check on failure.
- **Scale**: 100 agents, ~22M tokens, ~2h05 wall clock (interrupted once by
  the Opus session limit at 01:50, resumed cleanly on cache; one transient
  connection drop retried the same way).

## What the safety net caught

- **3 lessons failed their first independent check** and were fixed on
  revision: ratio-proportion-L01, ratio-proportion-L04, geometry-L06.
- **ratio-proportion-L01's revision agent corrupted text encoding**
  (double-encoded UTF-8: £ → Â£, and × mangled into literal em dashes). The
  re-checker caught it with a forensic byte-level report, confirmed the maths
  itself was perfect (every box and expect reproduced), and Fable repaired the
  encoding deterministically (cp1252 round-trip, 141 strings), re-validated,
  re-patched. Lesson for the pipeline: the no-heredoc rule needs to be
  screamed even louder at agents; the validator + independent check caught it
  regardless.

## Fable QA (after the fan-out)

- Live validator sweep: **48/48 PASS**; preserved fields
  (related_videos/topic_links/passages) byte-identical everywhere; mojibake
  scan clean everywhere.
- Opener taste review of all 48: concrete hooks throughout (skaters' 360s for
  angles, paper folding for exponential growth, big-wheel ride for trig
  graphs, pocket money for averages, pizza quarters for fractions).
- Headless full-journey click-throughs (opener → doors → teach walk →
  completion → wrong answer → rescue → pre-answer walk): geometry-L05,
  probability-statistics-L04, ratio-proportion-L02, number-L02, plus the L09
  pilot. All phases passed.
- Hand-verified the surds/bounds gold walks (number-L07) by independent
  computation.

## Caveats / next

1. **Merge dependency**: production (`platform` branch) still runs the old
   player. New data degrades gracefully there, EXCEPT algebra L09's xy_pair
   input renders as a single box. Merge landing-wizard before September.
2. **MC-heavy lessons** (e.g. algebra-L13 Sequences): multiple-choice
   questions carry no walk by design; if the day's first question is MC the
   completion problem is skipped. Future polish: use the first walk-capable
   question for the completion instead of strictly question 1.
3. **Other boards**: maths AQA / OCR / Eduqas (3 × 48 lessons) can reuse this
   exact pipeline + spec whenever approved. English and languages practice
   need an adapted spec (non-numeric boxes).
4. Rollback: `scratchpad/_maths_guided/_pre_fanout_dump.json` (all 48 rows,
   pre-run). Per-lesson shards + changelogs in the same directory.
