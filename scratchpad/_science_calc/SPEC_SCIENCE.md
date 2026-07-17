# Science Calculations Fan-Out — Guided Conversion (60 distinct versions → 165 rows)

You are converting ONE science calculation practice lesson to the guided
format Tom approved across all four maths boards. Read both maths specs first;
they are the law and this file only adds the science deltas:

1. `C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\SPEC.md`
2. `C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\SPEC_DIAGRAMS.md`

Also read the science schema (equation reference, field meanings):
`C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scripts\science-practice\SCIENCE_PRACTICE_SCHEMA.md`

## Science deltas

### One conversion, many rows (fingerprint propagation)
Your work-list entry has `canonical_id` (the row you fetch and convert) and
`all_row_ids` (every row sharing this exact practice_data, across boards and
Unity College). After the validator passes, PATCH the SAME final practice_data
to EVERY id in `all_row_ids`. They are byte-identical today; keep them
byte-identical.

### Board-neutral phrasing (hard rule)
Shared rows serve AQA + Edexcel + OCR simultaneously. NEVER write "this is on
your equation sheet" / "you must memorise this" as a board fact, and never
name a board. Say "check whether your board gives you this equation" or just
teach the equation. (Same principle as the platform's Eduqas/WJEC rule.)

### The walk ritual is the science method
Every guided walk follows the exam ritual, one box at a time:
1. Equation (say-step stating it; for bank problems the student ALSO has the
   existing "Show equation" recall toggle — keep every `equation_hint` field
   exactly as is, it is good retrieval practice).
2. **Unit conversion as its own box wherever the given units are not the base
   units** ("mass in kg = ⬚", "time in seconds = ⬚"). Unit slips are the top
   mark-killer; make the conversion explicit and catchable.
3. Substitute (box per value where it teaches; keep walks lean).
4. Compute (the `phase: "substitute"` completion boundary goes where the
   set-up ends and the calculation begins; student always computes).
5. Answer WITH UNIT: final say/done states the unit explicitly ("2 cm³/s").
   Box answers stay numeric only; never ask the student to type a unit.

### Box-value exactness
The guided engine checks boxes at ±0.005. Choose step values that are exact
at every step, or state the rounding in the pre text ("to 2 d.p."). With
g = 9.8 prefer masses/heights that give clean products. Do not change a
problem's published answer to make a walk cleaner; adapt the walk.

### Misconception expects
Derive every expect by committing the error: forgot_square, forgot_half,
unit_error (×1000 or ÷1000 slips), inverse_error, wrong_rearrange. Respect
the `accept` tolerance: an expect must sit OUTSIDE the accept window of the
correct answer or it can never fire (drop it if unavoidable). Keep `unit`,
`accept`, `higher_only` fields intact on every problem.

### Verification (trust nothing)
No prior audit exists. Fresh-solve every problem from its display: check the
arithmetic, the unit consistency, the `accept` sanity, `higher_only` flags
(momentum, v²=u²+2as, transformer, moles-concentration are HT/Separate),
g = 9.8 unless the display says otherwise, and chart problems' data actually
yielding the stored answer.

### Figures
- Electricity lessons: draw simple circuit diagrams (SVG, standard symbols:
  cell as long/short line pair, resistor as rectangle, ammeter A in circle,
  voltmeter V in circle) where the problem describes a circuit.
- Bio-data / rates lessons: keep and verify existing `chart` configs; add a
  chart where the problem says "the graph shows" without one.
- No decoration on pure-formula problems.

### Openers: physical intuition first
The concrete hook is a physical surprise the student can feel, then the
reveal names the equation. Examples of the calibre expected: kinetic energy
(why 30 mph does FOUR times the damage of 15 mph, not twice: the v² insight);
density (why a pebble sinks but a supertanker floats); power (two kettles,
same water, one twice as fast); moles (counting atoms by weighing, like
counting coins by weighing the bag). Openers are per-version: write your own,
verify your own numbers.

### Tier guides (science ladder)
Bronze: one equation, values given in the right units, straight in.
Silver: convert units first, or rearrange the equation before substituting.
Gold: multi-step (two equations chained, efficiency, or interpret data first).
Check the lesson's actual bank matches this ladder; note mismatches in your
changes file rather than reordering aggressively.

## Ship gate

1. Shard: `C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_science_calc\lesson_<WORKKEY>.json`
   (WORKKEY is your work-list key, e.g. physics-calculations-L01@32fbb0cae2)
2. Validator MUST pass:
   `python "C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\_validate_guided.py" <shard>`
3. PATCH every id in `all_row_ids` with the identical practice_data.
4. Changes file: `changes_<WORKKEY>.json` with problems_fixed, figures_added,
   rows_patched, opener_concept, notes.

Work-list: `C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_science_calc\_worklist_versions.json`
Rollback: `_pre_dump_all.json` (same directory). Data access, PATCH-only-
practice_data, no git, no bash heredocs: as SPEC.md.

## CHECKER BRIEF

Run the SPEC.md checker brief plus:
1. Fresh-solve every problem INCLUDING unit conversions; verify `unit` and
   `accept` fields; verify expects sit outside the accept window.
2. Recompute every walk box; confirm the completion boundary leaves the
   computation to the student; confirm final answer + unit stated.
3. Board-neutrality: no board names, no equation-sheet claims, on shared rows.
4. Circuit/chart figures: labels match the numbers; chart data yields the
   stored answer.
5. Propagation: fetch at least TWO ids from `all_row_ids` and confirm their
   practice_data is byte-identical to the canonical row.
6. Run the validator on the live canonical row.
FAIL on any maths error, dead expect (inside accept window), box that does
not compute, board-specific claim on a shared row, or propagation mismatch.
