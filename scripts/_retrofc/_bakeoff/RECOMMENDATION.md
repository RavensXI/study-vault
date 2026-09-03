# Codex checker pool: recommendation (3 Sep 2026)

## The test

One unit, OCR Dr Jekyll and Mr Hyde (7 lessons), checked cold by four Codex
models with the same brief, board facts and text as the Opus checker. Scored
against the Opus run (31 findings, 11 HIGH, 127 edits, about 12 minutes).
The matcher counts a hit only when claim wording overlaps; the "cold read"
column corrects it by hand where a model merged several Opus findings into one.

| Model / effort | Findings | Opus HIGH caught (matcher / cold read) | Edits that apply | Minutes | Caught the L7 AO4 error |
|---|---|---|---|---|---|
| Sol medium | 31 | 6 / 6 of 11 | 140 / 140 | 17 | no |
| Luna high | 36 | 8 / 8 of 11 | 138 / 159 (21 broken by a cp1252 read; prompt rule added) | 22 | no |
| Terra xhigh | 34 | 8 / 9 of 11 | 111 / 111 | 17 | yes |
| Sol high | 28 | 5 / 9 of 11 | 118 / 118 | 17 (rerun 3 Sep evening; the first run was lost to the internet outage) | yes |

The AO4 error is the mark-affecting one: the lesson taught AO1, AO2 and AO3
for a section that credits spelling, punctuation and grammar instead. Only
Terra xhigh and Sol high caught it.

Real errors the Codex models found that Opus missed (verified against the
Gutenberg text): Jekyll's daytime transformation is on a bench in Regent's
Park, not on waking (Sol medium and Sol high); the location is a "by-street",
not "Bye Street"; the "forgery" quotation in an L3 practice question is
invented; the Utterson description "lean, cold, scanty" is not the text's
"lean, long, dusty, dreary and yet somehow lovable"; Lanyon is a "hide-bound
pedant". Both Sol runs and Terra also flagged every "40 marks - Shakespeare
Essay" practice label, which Opus logged once as a unit-level finding.

Weak spots seen in every Codex run: no NOTE or ADJUDICATE verdicts at all
(everything is a FIX, including quotations they could not fully verify);
Sol high relabels discursive practice prompts as "untimed whole-text
practice", a policy the Claude checkers do not apply; Terra is mildly
pedantic about figurative language ("ape-like fury is not a simile").

## Recommendation

Add Codex as a second pool on SEPARATE units, not as a second opinion on the
same unit and not as a replacement. Default model Terra xhigh; Sol high as
the alternate when Terra's 5-hour window is hot. Do not use Sol medium or
Luna in the loop.

Why a separate pool: each model missed something another caught, and the
binding limit on the Claude loop is its 5-hour window, so a second window on
a different account adds throughput rather than accuracy. The Fable cold-read
audit stays the accuracy control: every fifth Codex unit for the first twenty,
then every tenth like the Claude units.

## Allowance and cost (Tom's readings, 2 Sep)

| | Codex (ChatGPT Plus, 20 pounds) | Claude (Max, 90 pounds) |
|---|---|---|
| 5-hour window per unit | about 16% (3 units per window) | binding today |
| Weekly cap per unit | about 2.5% (about 40 units a week) | not the binding limit |
| Cost per unit at that pace | about 0.12 pounds | about 0.19 pounds |

At 40 units a week Codex adds roughly a third to the loop's throughput. The
weekly cap, not the window, is what stops it.

## Integration design (about half a day, after your ruling)

1. Dispatcher in `_unit.py`: `next --pool codex` hands out the next queued
   unit to a Codex worker; the Claude tick skips units marked
   `checker: codex`. Two units in flight at once, never the same unit twice.
2. Codex units use the existing `_run_codex_checker.py` wrapper (unit dir
   only, no service keys, 40-minute kill) and the SAME finish path:
   validator, rollback on violation, re-narration, per-unit commit, tracker.
3. Brief additions for Codex: state the practice-label policy explicitly;
   require NOTE for any quotation not verified against a fetched source.
4. Rate-limit handling: parse the Codex usage-limit message, write
   `resume_after` for the Codex pool only, keep the Claude pool running.
5. Tracker: a "checker" column (opus / terra / sol) so the audit sample can
   be drawn per pool.

## What I need from you

- Yes or no to the integration, and Terra xhigh as the default.
- A glance at the ChatGPT usage bar after the first day, so the 16% per unit
  reading is confirmed with a real Terra run rather than the bake-off pair.
