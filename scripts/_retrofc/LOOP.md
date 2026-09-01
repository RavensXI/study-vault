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
   go to step 6 (finish). If it has no report and no checker is running
   (no pending task notification), relaunch the checker (step 5).
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

## Rate limit

If an Agent launch or any model call fails with a usage-limit message,
read the reset time from the message, write it to `_loop.json.resume_after`
(add 3 minutes), and ScheduleWakeup for min(3600, that delay) with
`noop: true`. Chained hourly wakeups until the reset are expected. If no
reset time is given, use now + 5h05m.

## Stop

Queue empty (`next` returns done): build the tracker once more, publish
it, send a PushNotification with the totals, ScheduleWakeup `stop: true`.
Also stop, with a PushNotification saying why, if three consecutive units
block.

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
