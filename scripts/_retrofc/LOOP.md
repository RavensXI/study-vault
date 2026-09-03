# EngLit retro fact-check: autonomous loop procedure

One tick = one unit. State lives on disk; this file is the whole procedure.
Tom's standing rules: all four EngLit boards before any other subject; never
push; commit per unit; fact-check before narration; backups before writes.

Files (scripts/_retrofc/): `_queue.json` (units, status queued/done),
`_state.json` (tracker ledger), `_loop.json` (loop state: `resume_after`
ISO time or null, `in_progress` {subject, unit, stage} or null, `ticks`,
`units_done`), `LOOP.md` (this), `CHECK_PROMPT.md` (checker brief),
`_unit.py` (prep / finish), `_tracker.html` (built by finish).

## Tick

1. `python scripts/_retrofc/_unit.py next` and read `_loop.json`.
2. If `resume_after` is in the future: do nothing, ScheduleWakeup for
   min(3600, seconds until resume_after + 120) with `noop: true`.
3. If `in_progress.stage == "checking"` and the unit dir has `_report.json`:
   go to step 6 (finish). If it has no report: a checker is probably still
   running - only relaunch it (step 5) when `checker_launched_at` is more
   than 45 minutes old. A second wake source (an hourly cron heartbeat)
   exists purely so a dead wakeup chain recovers; this guard is what stops
   it double-running a unit.
4. Otherwise take the next queued unit: `python scripts/_retrofc/_unit.py
   prep <subject> <unit>`; set `in_progress = {subject, unit, stage:
   "checking"}` in `_loop.json`.
5. Launch the checker (Agent, subagent_type general-purpose, model opus)
   with the prompt template below, then ScheduleWakeup 1500s (`noop: false`)
   as the fallback heartbeat; the checker's task-notification is the real
   wake signal. End the turn.
6. On the checker's notification (or a heartbeat that finds `_report.json`):
   read the checker's short report. Rule on each ADJUDICATE item: fix it
   only when the correction is certain and surgical (append an edit to
   `_edits.json` with a small python one-liner); otherwise leave it as a
   NOTE in the report. Then `python scripts/_retrofc/_unit.py finish
   <subject> <unit>`. If finish rolls back (new validator violations),
   remove or repair the offending edit and run finish again once; if it
   fails twice, mark the unit `status: "blocked"` in `_queue.json` with a
   note and move on.
7. Publish the tracker: Artifact tool, file `scripts/_retrofc/_tracker.html`,
   url https://claude.ai/code/artifact/10dfeef7-23eb-45ec-a525-d4b6a0ec5242
   (omit favicon). Set `in_progress = null`, `units_done += 1`.
8. Go straight to step 4 for the next unit in the SAME turn if capacity
   allows; otherwise ScheduleWakeup 60s.

## Second-reader audit (Tom, 2 Sep)

Every tenth unit (`units_done % 10 == 0`), the orchestrator itself re-reads
ONE lesson of the unit just finished, cold: export the live post-fix text
(the `audit_*.md` export used on 2 Sep: description, content, conclusion,
exam tip, questions, checks, flashcards, glossary, plus the checker's
findings for that lesson), grep every quotation against the cached text or
verify facts against the spec, and record the result in `_loop.json.audits`
as `{unit, lesson, missed: [...], wrong_fixes: [...], verdict}`. A missed
mark-affecting error or a wrong fix means: fix it directly (edit + finish
path), and tighten CHECK_PROMPT*.md before the next launch. First two
audits (OCR Macbeth L2, Edexcel Animal Farm L3, 2 Sep): clean.

## Codex pool (Tom's ruling, 3 Sep 2026 evening)

A second checker pool runs on Tom's ChatGPT Plus Codex CLI. It starts at the
FAR END of the queue and the two pools meet in the middle: `_unit.py next`
hands Claude the first free queued unit and `next --pool codex` the last;
`prep --pool codex` stamps the queue item so neither pool can take the
other's unit. The whole queue (priorities 1-9) is built up front for this
reason (science via `_build_science_queue.py`, 3-9 via `_build_queue.py`);
the family-boundary roll-over section below is therefore already done.
Codex state lives in `_loop.json.codex`: `{in_progress: {subject, unit,
model, effort, launched_at, attempts} | null, units_done, resume_after,
audits}`.

Every tick, AFTER the Claude steps and in the same turn:

C1. If `codex.resume_after` is in the future: skip the Codex steps.
C2. If `codex.in_progress` is set, read `<dir>/_codex_done.json`. If it is
    missing, the run is still going (the wrapper kills at 40 min) - skip.
    If present with `report_ok` true: read `<dir>/_codex_last_message.md`
    (under 250 words), rule on ADJUDICATE items exactly as in step 6, run
    `python scripts/_retrofc/_unit.py finish <subject> <unit>` (same
    validator / rollback / re-narration / commit path; runs sequentially
    with the Claude finish so git never sees two writers), publish the
    tracker, `codex.units_done += 1`, `codex.in_progress = null`. If
    `report_ok` is false or `exit_code` is not 0: tail `_codex_run.log`;
    a usage-limit / rate-limit message -> set `codex.resume_after` from it
    (or now + 5h05m) and leave `in_progress` for a relaunch; a network
    error -> relaunch once (`attempts` 2); a second failure -> mark the
    queue item `blocked` with a note and clear `in_progress`.
C3. If nothing is in progress: `python scripts/_retrofc/_unit.py next
    --pool codex`; if it returns a unit, `prep <subject> <unit> --pool codex`,
    set `codex.in_progress`, and launch the wrapper DETACHED (PowerShell
    `Start-Process -FilePath python -ArgumentList @(...) -WindowStyle Hidden
    -PassThru -RedirectStandardOutput <dir>\_launcher_stdout.txt
    -RedirectStandardError <dir>\_launcher_stderr.txt`) with
    `scripts/_retrofc/_run_codex_checker.py <dir> --model gpt-5.6-terra
    --effort xhigh --family <family> --facts "<facts>" --timeout-min 40`.
    Default model Terra xhigh; Sol high is the alternate when Terra is
    rate-limited. `--family` is the brief's family (`generic` for
    priorities 4-9). `--facts`: the board-facts line from the lists below
    for EngLit; the science anchors for science; otherwise "read the spec's
    assessment section before asserting any exam claim". Delete a stale
    `_codex_done.json` before launching.
C4. Second-reader audit for Codex units: every FIFTH Codex unit for the
    first twenty, then every tenth, same method as the Claude audit; record
    in `codex.audits`. A missed mark-affecting error tightens the wrapper's
    prompt in `_run_codex_checker.py` before the next launch.
C5. Codex never receives service keys (`shell_environment_policy.inherit=
    "core"`) and writes only inside its unit dir; the finish step is what
    touches Supabase, R2 and git, and it runs with the orchestrator's env.

## Rate limit

If an Agent launch or any model call fails with a usage-limit message,
read the reset time from the message, write it to `_loop.json.resume_after`
(add 3 minutes), and ScheduleWakeup for min(3600, that delay) with
`noop: true`. Chained hourly wakeups until the reset are expected. If no
reset time is given, use now + 5h05m.

## When the EngLit queue empties: roll into the sciences (Tom, 2 Sep)

Do NOT stop. Run `python scripts/_retrofc/_build_science_queue.py` once (it
appends the 8 science subjects' article units with `family: "science"`,
`spec`, `qualification`; practice units excluded; idempotent), publish the
tracker, send a PushNotification with the EngLit totals, then go straight
to step 4. Science items use `CHECK_PROMPT_SCIENCE.md` (the brief's
`check_prompt` field says which) and the science prompt template below.
After the sciences, every later family is queued the same way, in tracker
priority order, each time `next` returns done:
`python scripts/_retrofc/_build_queue.py --priority N --confirm` for N = 3
(history, brief CHECK_PROMPT_HISTORY.md), 4 (geography), 5 (RS / geology /
astronomy), 6 (business / CS / PE / sociology / D&T), 7 (niche), 8, 9
(music). Priorities 4-9 use CHECK_PROMPT_GENERIC.md (the brief's
`check_prompt` field says which; the checker prompt template is the science
one with the brief path swapped and the "board anchors" line replaced by
"read the spec's assessment section before asserting any exam claim"). The
builder prints its spec mapping; if it reports UNRESOLVED specs it refuses
to save - fix the mapping by hand (`--subjects a,b --family X`) and rerun.
Publish the tracker and send a PushNotification at each family boundary.

## Stop

Queue empty after priority 9 (`next` returns done and every family has
been queued): build the tracker once more, publish it, send a
PushNotification with the totals, ScheduleWakeup `stop: true`. Also stop,
with a PushNotification saying why, if three consecutive units block.

## Science checker prompt template

```
Repo root: C:\Users\tshau\Documents\Study Vault (run everything from there).
First read scripts/_retrofc/CHECK_PROMPT_SCIENCE.md in full; it is your brief and its rules bind.
Unit to check: <subject> / <unit> (<n> lessons; qualification: <combined|separate>; board <board>). Unit dir: <dir>.
Brief: <dir>/_brief.json (each lesson's tier is listed). Spec: <spec> - grep it for
scope, tier flags (HT only), required practicals, the equations list, and read its
assessment section for paper structure before asserting any exam claim.
Read raw/L01.txt ... one at a time. Check every value, unit, equation and worked
example (recompute), every spec-scope and tier claim, every required practical,
every answer key. Write <dir>/_report.json and <dir>/_edits.json exactly in the
shapes CHECK_PROMPT_SCIENCE.md specifies; `find` strings copied exactly and unique
in their field. Do NOT write to Supabase or run any script that writes. This
session's WebSearch budget is exhausted; the spec is the authority, WebFetch
(BBC Bitesize is blocked; use Wikipedia / physics.nist.gov) only for settled
constants. Finish with a report under 250 words as the brief describes.
```

Science board anchors (verify in the spec before asserting):
- AQA Trilogy 8464: 6 papers (Bio 1-2, Chem 1-2, Phys 1-2), 1h15 each, 70
  marks, F/H tiers; separate 8461/8462/8463: 2 papers each, 1h45, 100 marks.
- Edexcel 1SC0: 6 papers, 1h10, 60 marks; separate 1BI0/1CH0/1PH0: 2 papers
  each, 1h45, 100 marks.
- OCR Gateway A J250: 6 papers, 1h10, 60 marks; separate J247/J248/J249: 2
  papers each, 1h45, 90 marks.
- OCR 21st Century B J260 and J257/J258/J259: read the spec (different
  structure - do not assert from memory).

## Checker prompt template

```
Repo root: C:\Users\tshau\Documents\Study Vault (run everything from there).
First read scripts/_retrofc/CHECK_PROMPT.md in full; it is your brief and its rules bind.
Unit to check: <subject> / <unit> (<n> lessons). Unit dir: <dir>.
Brief: <dir>/_brief.json. Spec: <spec>. Board facts: <one line of the board's
paper/marks/AO facts for this text type>.
Primary text: <path or "in copyright: verify quotations by web search">.
Read raw/L01.txt ... one at a time. Check every quotation (wording, speaker,
scene/chapter), every exam claim against the spec, every answer key against
the corrected facts. Write <dir>/_report.json and <dir>/_edits.json exactly
in the shapes CHECK_PROMPT.md specifies; `find` strings copied exactly and
unique in their field. Do NOT write to Supabase or run any script that
writes. Finish with a report under 250 words as CHECK_PROMPT.md describes.
```

Board facts to paste (keep current with the spec files):
- AQA 8702: Paper 1 Shakespeare 30 + 4 SPaG (AO1 12 / AO2 12 / AO3 6), extract
  printed, closed book; Paper 1 19th-century novel 30 (AO1 12 / AO2 12 / AO3 6),
  extract printed; Paper 2 modern text 30 + 4 SPaG (AO1 12 / AO2 12 / AO3 6),
  no extract; poetry cluster 30 (AO1 12 / AO2 12 / AO3 6), one poem printed;
  unseen 24 (AO1 12 / AO2 12) + 8 (AO2). Paper 1 1h45, Paper 2 2h15.
- Edexcel 1ET0: Paper 1 (Shakespeare 40 = extract 20 + whole play 20, incl.
  SPaG on part b; post-1914 40 incl. SPaG); Paper 2 (19th-century novel 40 =
  extract 20 + essay 20; anthology poetry 20; unseen 20 comparison). Read
  the spec for AO splits per question before asserting any.
- OCR J352: Component 01 modern prose/drama (extract-based comparison 20 +
  essay 20) and 19th-century prose (extract 20 + essay 20 incl. SPaG); Component
  02 poetry across time (anthology comparison 20 + unseen 20) and Shakespeare
  (extract-based 20 + essay 20 incl. SPaG). Read the spec for AO weights.
- Eduqas C720QS: Component 1 Shakespeare (extract 15 + essay 25 incl. SPaG 5)
  and poetry anthology (15 + 25); Component 2 post-1914 prose/drama (extract
  15 + essay 25... read the spec), 19th-century prose, unseen poetry (15 + 25).
  Read the spec for exact marks before asserting any.
