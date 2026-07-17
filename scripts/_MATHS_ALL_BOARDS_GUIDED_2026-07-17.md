# Maths Practice: All Four Boards in Guided-Learning Format — 17 July 2026

Tom's overnight brief: audit/fix the method cards, then roll the full Edexcel
treatment (guided learning + exam-realism diagrams) across maths AQA, OCR and
Eduqas. Fable 5 wrote the specs and did QA; Opus 4.8 agents did the work with
independent adversarial checkers per lesson.

## Result

**All 192 maths lessons across all four boards are live in the guided
format**: concrete opener puzzle, two doors, per-tier teach walks, completion
problems, "do this one with me" rescue on every non-MC question, tier guides,
per-problem hints, honest misconception expects, exam-realism figures on
visual units, zero em dashes, xy_pair inputs on both simultaneous-equations
lessons per board.

| Board | Clean | Fixed on revision | Hand-fixed by Fable |
|---|---|---|---|
| Edexcel (15-16 Jul) | 44 | 3 | encoding repair + 1 label |
| AQA | 45 | 2 | 1 (opener taught a falsehood) |
| OCR | 46 | 2 | 0 |
| Eduqas | 41 | 7 | 0 |

Final QA per board: live validator sweep 48/48 PASS, preservation intact,
mojibake scan clean. Eduqas/AQA/OCR openers are fresh takes, not copies
(cinema trip for simultaneous equations, balance scales for linear equations,
algebra tiles for completing the square).

## Method-card fix (before the fan-out, per Tom)

The left-panel step list used a flex `li` where mixed text + KaTeX + bold
shattered into interleaved columns and overflowed the container. Fixed in the
player (single `.step-body` flex item + wrapping insurance + tightened
example block); applies to every practice lesson on the platform. Verified by
screenshot before/after.

## Best checker catches this run

- AQA geometry-L06: opener asked which of 30°/60° "the longest side" faces
  (accepting 60) — false; the longest side faces the 90°. Maths everywhere
  else in the lesson verified perfect to 4 d.p. Fable reworded it truthfully.
- OCR/Eduqas revisions: figure-label mismatches and expect derivation slips
  caught before students ever saw them.

## Scale

Three boards ≈ 310 live Opus agents, ~46M subagent tokens, run across three
session-limit windows with clean cache resumes each time.

## Standing dependencies / next

1. **Merge landing-wizard → platform before September** (production player
   lacks the guided engine; new data degrades gracefully except xy_pair
   lessons render a single input box).
2. English/language practice adaptation (non-numeric boxes) when Tom calls it.
3. Player polish backlog: completion should use the first walk-capable
   question when Q1 is multiple-choice.
4. Rollbacks: `scratchpad/_maths_boards/_pre_dump_maths-{aqa,ocr,eduqas}.json`
   and `scratchpad/_maths_guided/_pre_fanout_dump.json` (Edexcel).
