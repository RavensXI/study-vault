# PE OCR (J587) Phase 3 — Prep Report

## What was set up

Scaffolding for cross-board adaptation Phase 3. Twenty-seven OCR lesson shells already exist in Supabase (subject id `3569b57d-4d3b-4e4d-a3f7-c4b5d3fcbecb`); this directory now contains everything an Opus/Sonnet content-agent fan-out needs to write the 27 lesson JSONs.

## Files produced (in `scripts/_content_physical-education-ocr/`)

### Prompts and reference
- `_AGENT_PROMPT.md` — content-agent system prompt. Built from PE AQA prompt + an explicit cross-board adaptation section (transfer-score behaviour, OCR terminology delta table, AO weightings, OCR spec-ref format `1.1.a` etc., 8-mark cap on extended response).
- `_RELATED_MEDIA_PROMPT.md` — related-media curator prompt. Mirrors PE AQA, retargeted for OCR (categories: Podcasts / Videos & Channels / one of {Documentaries, Movies, TV Shows} / Study Tools).
- `_reference_lesson.json` — full Supabase row for RE L01 "Worship & Prayer" (id `21447890-d512-42c6-85f9-90b4133c06e3`) — structural template only.

### Spec slices
- `_spec_physical-factors-affecting-performance.txt` — Component 01 (sections 1.1.a-e + 1.2.a-c). 944 body lines + OCR-specific framing header.
- `_spec_socio-cultural-issues-and-sports-psychology.txt` — Component 02 (sections 2.1.a-c + 2.2 + 2.3). 543 body lines + OCR-specific framing header.

### Source-content files (`_source/`)
- 25 AQA lesson JSONs at `_source/aqa_<aqa-slug>.json`. Each contains the source row's `id, slug, title, lesson_number, description, content_html, exam_tip_html, conclusion_html, practice_questions, knowledge_checks, flashcard_questions, glossary_terms`. (No `narration_script` column on `lessons` — narration is in a separate manifest table; agents work from `content_html` only.)
- The 2 fresh OCR lessons (Unit 1 L14 Preventing Injury, Unit 2 L5 Violence in Sport) have NO source — agents build from spec slice.

### Batch JSONs (6 batches, 4-5 lessons each)
- `_batch_u1_b1.json` — Unit 1 (Physical Factors) lessons 1, 2, 3, 4, 5  (Skeleton, Synovial Joints, Muscles+Fixator, Levers, Planes/Axes)
- `_batch_u1_b2.json` — Unit 1 lessons 6, 7, 8, 9, 10  (Cardiovascular, Respiratory, Aerobic/Anaerobic, Effects of Exercise, Components of Fitness + Tests)
- `_batch_u1_b3.json` — Unit 1 lessons 11, 12, 13, 14  (SPOR/FITT, Methods of Training, Warm Up/Cool Down, Preventing Injury [FRESH])
- `_batch_u2_b1.json` — Unit 2 (Socio-Cultural + Sports Psych) lessons 1, 2, 3, 4, 5  (Engagement, Commercialisation, Ethics, Drugs, Violence [FRESH])
- `_batch_u2_b2.json` — Unit 2 lessons 6, 7, 8, 9  (Skill Characteristics + Continua, SMART Goals, Mental Prep, Guidance)
- `_batch_u2_b3.json` — Unit 2 lessons 10, 11, 12, 13  (Feedback, Health/Fitness/Wellbeing, Sedentary Lifestyle, Diet/Nutrition)

Each batch entry carries: `lesson_id` (Supabase UUID), `lesson_number`, `slug`, `title`, `description`, `spec_references` (OCR codes), `section_markers`, `suggested_question_types`, `content_transfer` block (transfer_score, source unit/lesson, adaptation_notes), and `source_aqa_file` pointer (or `null` for fresh).

### Helper scripts (run once each, kept for reproducibility)
- `_fetch_setup.py` — pulls reference lesson, AQA source rows, and OCR lesson IDs from Supabase. Re-runnable.
- `_make_spec_slices.py` — slices the OCR J587 spec into per-unit files.
- `_make_batches.py` — builds the 6 batch JSONs from the plan + fetched IDs.
- `_fetch_setup_result.json` — intermediate output from the fetcher (OCR id map + fetch summary).

## Source-content fetcher results
- **AQA source files pulled**: 25 of 25 expected (100% match rate).
- **Fresh lessons (no source)**: 2  (`preventing-injury-in-physical-activity`, `violence-in-sport`).
- **Failures**: 0.

## Calls / decisions made
- **Batch sizes** — 4-5 lessons each (six batches). Slightly larger than the AQA build's 3-4 because every transferable lesson has a saved AQA source file, so per-lesson agent work is lighter.
- **8-mark vs 6-mark capstone** — assigned per-lesson. Lessons that the OCR spec flags as evaluation-rich (cardiovascular, effects of exercise, components of fitness, short-and-long-term effects, principles of training, methods of training, preventing injury, ethics, drugs, mental preparation, health/fitness/wellbeing, sedentary lifestyle, diet/nutrition, lever systems) get an 8-mark Evaluate as the sixth question; pure-recall lessons get a 6-mark Analyse instead. Agents can override if the lesson topic doesn't sustain an 8-mark.
- **Data-amenable lessons** — keyword-matched (cardiovascular, effects of exercise, components of fitness, engagement patterns, wellbeing, diet/nutrition, sedentary lifestyle, drugs, commercialisation). These get a `3 marks — Calculate from Data` and `4 marks — Interpret Data` slot in `suggested_question_types` instead of `2 marks — State Two` and a generic `4 marks — Explain`.
- **AQA L1 disambiguation** — both AQA units start at L1 (skeleton in Unit 1, skill+ability in Unit 2). Resolved by maintaining an explicit Unit-1 slug allow-list in `_make_batches.py`.
- **Spec line ranges** — Unit 1 = lines 656-1599 of `specs/ocr/physical-education-J587.md` (Component 01, sections 1.1-1.2). Unit 2 = lines 1601-2143 (Component 02, sections 2.1-2.3). Confirmed against grep of `2c.1`/`2c.2` headings.
- **Mental Preparation Techniques (Unit 2 L8)** mapped to AQA L6 (`arousal-and-the-inverted-u-theory`) per the plan. Agent must STRIP the inverted-U content entirely and rebuild around four named techniques (imagery, mental rehearsal, selective attention, positive thinking). Adaptation notes already flag this in the batch JSON; the AGENT_PROMPT terminology delta also calls it out.
- **Reference lesson missing column** — `lessons` table has no `narration_script` column (narration lives in `narration_manifest` JSON). Adjusted the fetcher to skip it; content agents don't need narration audio anyway.

## Anything missing or needing watch
- **No issues blocking content fan-out.** All 27 lesson IDs resolved, all 25 source rows fetched, all 6 batches written and verified.
- **OCR's longitudinal vs sagittal axis** — confirmed against the spec slice (line 920ish in unit 1 spec) before locking the terminology delta. Spec says longitudinal; agents have explicit instruction.
- **Calculator** — OCR allows calculators on Paper 1; flagged in the AGENT_PROMPT so agents include numeric calculation questions where appropriate.
- **Validator alignment** — agents must hit `_verify_subject_build.py` rules: exact category names "Videos & Channels" + one of {"Movies","TV Shows","Documentaries"} + "Articles & Reading" or "Study Tools". The AGENT_PROMPT and RELATED_MEDIA_PROMPT both spell these out verbatim.

## Confirm: scope of changes
**Only the new directory `scripts/_content_physical-education-ocr/` was modified.** No edits to other directories, no Supabase writes (Phase 2 already activated lessons; this phase is read-only against the DB). The fetcher and slicer scripts read from `specs/ocr/physical-education-J587.md` and `scripts/_plan_physical-education-ocr.json` and `scripts/_content_physical-education-aqa/` but did not modify them.
