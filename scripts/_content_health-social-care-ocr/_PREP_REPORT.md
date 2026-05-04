# HSC OCR (J835 R032) Phase 3 — Prep Report

## What was set up

Scaffolding for a fresh-build Phase 3. Thirteen OCR R032 lesson shells already exist in Supabase (subject id `21ece010-ec90-4320-8368-37a2526d070e`, unit id `76633e36-0d65-4a90-baed-60e73d63976a`). This directory now contains everything a fan-out of Sonnet 4.6 content agents needs to write the 13 lesson JSONs from spec only. No cross-board source content was pulled — Tom's brief explicitly directs fresh build.

## Files produced (in `scripts/_content_health-social-care-ocr/`)

### Prompts and reference
- `_AGENT_PROMPT.md` — content-agent system prompt. Fresh-build flavour (no AQA-source rules), neutral board phrasing, vocational L1/L2 tone bias, 8-mark cap on extended response, 8 registered question types (no Calculate types), AOs as plain PO1/PO2/PO3, plain-text-fields enforcement, validator-aligned glossary ≥6 / flashcards ≥8 / 6 practice / 5 KCs / 2+ key-fact / 2+ collapsible rules, ABSOLUTE BANS section.
- `_RELATED_MEDIA_PROMPT.md` — related-media curator prompt. Required categories: Podcasts / Videos & Channels / one of {Documentaries, Movies, TV Shows} / Study Tools (per `_verify_subject_build.py`). Articles & Reading recommended as a 5th. UK-first sources biased to NHS, Skills for Care, CQC, NSPCC, Mencap, Age UK, RNIB / RNID, Alzheimer's Society. Sensitive-content note for safeguarding-related lessons.
- `_reference_lesson.json` — full Supabase row for RE L01 "Worship & Prayer" (id `21447890-d512-42c6-85f9-90b4133c06e3`) — structural template only.

### Spec slice
- `_spec_principles-of-care.txt` — OCR J835 spec extract for R032 only (lines 1544-2346 of `specs/ocr/cambridge-nationals-health-and-social-care-J835.md`) plus Appendix B (command and descriptor words). R033, R034 and R035 (NEA units) are excluded. Header summarises R032's 70-mark structure, PO weightings, scenario-based question expectation, and 8-mark extended-response cap. **Not committed to git** (matches `.gitignore` rule `scripts/_content_*/_spec_*.txt`).

### Batch JSONs (3 batches, 13 lessons total)
- `_batch_b1.json` — lessons 1, 2, 3, 4, 5 (Topic Area 1: rights of service users + Topic Area 2 partial: person-centred values, 6Cs, benefits)
- `_batch_b2.json` — lessons 6, 7, 8, 9 (Topic Area 2 finish: effects when values not applied + Topic Area 3 partial: verbal, non-verbal/active listening, special methods)
- `_batch_b3.json` — lessons 10, 11, 12, 13 (Topic Area 3 finish: importance/impact of communication + Topic Area 4: safeguarding, infection prevention, safety procedures and security)

Each batch entry carries: `lesson_id` (Supabase UUID), `lesson_number`, `slug`, `title`, `description`, `spec_references` (OCR codes 1.1-4.4), `section_markers`, `suggested_question_types` (7 types — agent picks the best 6).

8-mark Discuss / Evaluate capstones assigned to lessons whose content sustains discussion or evaluation:
- L2 (benefits when rights maintained — discuss),
- L5 (benefits of values — discuss for SU vs SP perspectives),
- L6 (effects when values NOT applied — evaluate PIES connections),
- L10 (importance and impact of communication — discuss good vs poor),
- L11 (safeguarding — discuss / evaluate impacts of failure),
- L13 (safety procedures vs measures + security — evaluate).

The other seven lessons take a 6-mark Explain capstone — recall + reasoning rather than evaluation.

## Decisions / calls made

- **Batch sizes** — 5 / 4 / 4. Boundaries follow OCR's Topic Area structure: b1 covers Topic Areas 1+ start of 2, b2 covers rest of 2 + most of 3, b3 covers tail of 3 + all of 4. Slightly tighter than PE OCR's 4-5 per batch because R032 is shorter (13 lessons) than J587 (27).
- **Question type registry** — 8 types (no Calculate). R032 has zero quantitative content, so calculation types are out. Capped at 8-mark extended response (PO3-only) per spec assessment guidance ("one 8-mark extended response question which will assess Performance Objective 3"). Up to two 6-mark extended responses per real exam, but only one per lesson in our pipeline.
- **Reference lesson** — RE L01 "Worship & Prayer" (`21447890-d512-42c6-85f9-90b4133c06e3`) used as the structural pattern, per `docs/REFERENCE_LESSONS.md`.
- **Fresh build** — no `_source/` directory and no AQA / Edexcel cross-board adaptation. The existing free-tier Edexcel BTEC HSC build covers a structurally different unit (Component 3: factors affecting health/wellbeing, lifestyle indicators, health-plan design) — only ~20-25% topical overlap, none of which justifies a transfer pipeline. Per Tom's brief.
- **Neutral board phrasing** — OCR is named where it clarifies (command-word definitions, R032 assessment structure). Default to neutral phrasing ("your exam", "this paper", "the externally assessed unit") elsewhere. Eduqas / WJEC / AQA / Pearson BTEC explicitly banned in user-facing prose.
- **Vocational tone** — explicit instruction in `_AGENT_PROMPT.md` to anchor every concept in a named real-care setting + named service user + practitioner, biasing examples to L1/L2 vocational learner experience (GP surgery, residential home, community centre, after-school club, foodbank etc.).
- **Subject-level teaching brief** — copied verbatim from the plan JSON's `teaching_brief` block (8 misconceptions, 8 student errors by question type, 6 weighting notes, 4 spec-change notes, 7 pedagogical notes). Sourced from the J835 spec text plus standard EEF cognitive-science evidence.

## Anything missing or needing watch

- **No issues blocking content fan-out.** All 13 lesson IDs resolved against Supabase, all 3 batches written and verified, spec slice and reference lesson on disk.
- **Validator alignment** — required `_verify_subject_build.py` category groups (Podcasts / Videos & Channels / one of Documentaries-Movies-TV Shows / Study Tools, ≥6 items per lesson) are explicitly spelled out in `_RELATED_MEDIA_PROMPT.md`.
- **Sensitive-content awareness** — flagged in `_RELATED_MEDIA_PROMPT.md` for safeguarding (L11), abuse / harm (L11), end-of-life (L6 PIES), dementia (recurring across L6, L8, L10) lessons. Curators steered toward analytical sources (BBC, Guardian, HSJ, Skills for Care, NSPCC Learning) and away from tabloid abuse coverage or graphic footage.
- **Spec slice not committed** — by design (`.gitignore` rule `scripts/_content_*/_spec_*.txt`). Local-only, written for the content agents to read at fan-out time.

## Confirm: scope of changes

**Only the new directory `scripts/_content_health-social-care-ocr/` was modified.** No edits to other directories, no Supabase writes (Phase 2 already activated lessons; this phase reads from Supabase only). The fetcher reads from `specs/ocr/cambridge-nationals-health-and-social-care-J835.md`, the plan at `scripts/_plan_health-social-care-ocr.json`, and live Supabase rows — none of those were modified.
