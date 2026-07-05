# QUEUED: Computer Science OCR (free-tier) content rebuild

**Trigger:** Tom, 5 Jul 2026 — "queue the CS rebuild when the strip is done."
Runs AFTER the spec-reference strip (workflow wf_349cb260, 105 lessons) is
applied + verified.

## Why
- All 23 lessons are early-generation: body text ~450–550 words vs the
  platform article standard (~3× that). Tom hit it on computer-systems L3.
- The build's content prompt habitually cited "OCR J277 spec section X.Y"
  (46 hits) — banned. Strip removes them from the LIVE rows; the rebuild
  fixes the depth problem at source.

## Scope
- Subject: `computer-science` (school_id NULL), OCR J277.
- Units (KEEP rows, ids, slugs, accents): computer-systems (12 lessons),
  computational-thinking (11 lessons). Lesson rows: KEEP ids/slugs/numbers/
  titles — regenerate content_html, description, practice_questions,
  knowledge_checks, flashcard_questions, glossary_terms IN PLACE (PATCH).
  Preserving lesson ids keeps shorts manifest/questions + podcast URLs valid.
- Do NOT touch Unity's `computer-science[school]` copy (same slugs, school_id
  set) — mirror decision is Tom's, flag after free-tier lands.

## Method (per memory/pipeline-rules.md + docs/PIPELINE.md)
1. No permission-asking between steps once started.
2. Content agents: OPUS, one per lesson, full batch in one launch (workflow).
   Inputs each agent Reads itself:
   - docs/CONTENT_PROMPT.md (system prompt + output schema)
   - spec: C:\Users\tshau\Documents\Study Vault\specs\ocr\computer-science-J277.md
     (feed relevant spec bullets VERBATIM per [[feedback_spec_is_source_of_truth]]
     — but NEVER cite spec numbers in output; policy banner in prompt)
   - existing lesson row JSON (title, number, unit) for continuity.
   Output: JSON per docs/CONTENT_PROMPT.md schema to scratchpad file.
3. Central: scripts/_validate_content_json.py per lesson (entities rule,
   "Award N marks" drift-grep per [[food_prep_aqa_build]]), backup old rows,
   PATCH.
4. Phase 6 fact-check (scripts/_fact_check_subject.py computer-science)
   BEFORE any narration ([[feedback_factcheck_before_narration]]).
5. Narration: 23 lessons stale after rebuild (plus ~90 strip-affected lessons
   platform-wide have minor audio drift). Present cost to Tom before running.
6. Shorts/podcast mappings survive (lesson ids unchanged); KC-based shorts
   questions must be re-checked after new KCs land — re-run the shorts qbank
   fetch + remap for this subject's lessons.

## Decisions (Tom, 5 Jul): BOTH YES
- Re-narration: YES — (a) 23 rebuilt CS free-tier lessons, (b) Unity CS copies
  after mirror, (c) strip-touched lessons whose content_html changed
  (from scratchpad/specfix_backup.jsonl, exclude CS which is rebuilt anyway;
  exclude practice-first subjects — no narration). Ollie odd / Ada even,
  docs/NARRATION_PIPELINE.md. Note in report: Unity podcasts/cinematic videos
  for CS become stale (NLM/manual — Tom's call separately).
- Unity mirror: YES — copy the six rebuilt content fields onto
  computer-science[school] rows matched by (unit_slug, lesson_number).
  Unity CS was originally a copy of generic, so this preserves provenance.

## Status
- [x] Strip: 105/105 applied (2 scanner leftovers = benign D&T design-spec
      language), platform scanner clean. Backups: scratchpad/specfix_backup.jsonl
- [~] Rebuild content fan-out RUNNING (wf_9ed6aeda-cd3, 23 Opus agents,
      outputs scratchpad/csrebuild_out/<id>.json)
- [x] Validated + applied 23/23 free-tier (avg 1,033 words; 2 flashcards
      hand-fixed; 1 lesson single-agent regen after two phantom successes).
      Backups: scratchpad/csrebuild_backup.jsonl
- [x] Fact-check gate PASSED: 0 findings, 4 web-verify slices
      (scripts/_fact_check/computer-science.{json,md})
- [x] Unity mirror 23/23 by (unit_slug, lesson_number).
      Backups: scratchpad/unity_cs_backup.jsonl
- [~] Re-narration RUNNING (task b1tptfbtn): 98 lessons sequential via
      _narrate_single_lesson.py — 23 free CS + 23 Unity CS + 52 strip-drift
      (list: scratchpad/renarrate_strip_list.json; log: scratchpad/renarrate_run.log)
- [x] Shorts remap: N/A — no shorts exist for slug computer-science
- [ ] Final report (incl. stale Unity CS podcasts/videos note)
