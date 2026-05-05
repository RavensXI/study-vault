# AQA Religious Studies A 8062 Gap-Fill Phase 3 — Prep Report

## What was set up

Scaffolding for a gap-fill content generation against the existing free-tier `religious-education` subject (`8efd391b-1981-46a2-a22f-0baf45925c2b`). Phase 1 plan and Phase 2 activation are already done — 12 new units (sort_order 9-20) and 46 new lesson shells live in Supabase. This directory contains everything a fan-out of Sonnet 4.6 content agents needs to write the 46 lesson JSONs.

Existing 8 units (Christianity Beliefs/Practices, Islam Beliefs/Practices, Themes A/B/D/E — sort_order 1-8) are OUT OF SCOPE and untouched. No edits anywhere outside `scripts/_content_religious-education-gap-fill/`.

## Files produced (in `scripts/_content_religious-education-gap-fill/`)

### Prompts and reference
- `_AGENT_PROMPT.md` — content-agent system prompt. Adapted from the Food Prep Eduqas v2 prompt with RE-specific overrides:
  - Tone: respectful, neutral, factual; each religion treated as a living tradition; sub-traditions named (Theravada/Mahayana, Catholic/Orthodox/Protestant, Shaivism/Vaishnavism, Orthodox/Reform/Liberal Judaism, sahajdhari/amritdhari).
  - Theme F sensitivity rules: factual coverage of women's rights / LGBTQ+ / racial discrimination / wealth; no authorial judgement; sub-tradition contrast required; DfE political impartiality framework cited.
  - Original case studies: fictional believers + scenarios; real institutions (Lourdes, Vatican, Golden Temple at Amritsar) and real historical figures (Jesus, Buddha, Moses, Guru Nanak, Aquinas, Paley) allowed; no quoting contemporary religious leaders' speeches verbatim.
  - StudyVault rubric (Mastering / Secure / Developing / Emerging) for 6/8/12-mark; AQA RS extended response goes to 12 marks (NOT capped at 8).
  - AO codes plain (AO1 / AO2 only — NO AO3 on AQA RS, ever).
  - Plain-text fields (description ≤120 chars, practice_questions stems, KCs, flashcards, glossary) — unicode only, no HTML entities.
  - HTML fields (content_html, exam_tip_html, conclusion_html) — entities allowed.
  - Validator-aligned: 6 PQ, 5 KC (2 mcq + 2 fill + 1 match), ≥8 flashcards, ≥6 glossary, 2+ key-fact divs, 2+ collapsibles in content_html.
  - Reference lesson: `21447890-d512-42c6-85f9-90b4133c06e3` (RE L01 "Worship & Prayer" — sibling lesson in this exact subject; structural template only).
  - Hard ban on board names ("AQA"), spec codes ("8062"), component / paper labels, level descriptors in `marks` field.

- `_RELATED_MEDIA_PROMPT.md` — related-media curator prompt. Required categories per validator: **Podcasts**, **Videos & Channels**, one of {**Movies**, **TV Shows**, **Documentaries**} (default Documentaries for RE — strong canon), **Study Tools**. Optional **Articles & Reading** recommended. Format made explicit per `feedback_related_media_format.md`: list of category groups with nested `items` arrays — NOT flat per-item entries. Per-religion UK-first source biases supplied (BBC Bitesize, BBC Religion, BBC Sounds, Religion Media Centre, plus religion-specific UK organisations: Buddhist Society, Catholic Education Service, CAFOD, Hindu Council UK, Board of Deputies of British Jews, Sikh Network UK). Theme C and Theme F have specific UK source biases (BBC Philosophy & Ethics, Theos Think Tank, Amnesty UK). Placeholder podcast pattern flagged for Tom's NotebookLM manual pass.

- `_reference_lesson.json` — full Supabase row for RE L01 "Worship & Prayer" (id `21447890-d512-42c6-85f9-90b4133c06e3`). Sibling lesson within this exact subject — perfect structural template (matched HTML scaffolding, narration density, key-fact and collapsible patterns).

### Spec slice
- `_spec_religious-education.txt` — AQA 8062 spec extract. Covers Section 4.1 (religion option list), 3.1.1 Buddhism, 3.1.3 Catholic Christianity, 3.1.4 Hinduism, 3.1.6 Judaism, 3.1.7 Sikhism, 3.2.1.3 Theme C, 3.2.1.6 Theme F. Plus AO weighting (AO1 50% / AO2 50%, NO AO3) and command-verb reference. **Christianity (3.1.2) and Islam (3.1.5) are intentionally excluded** — already built. Themes A, B, D, E also excluded for the same reason. **Not committed to git** (matches `.gitignore` rule `scripts/_content_*/_spec_*.txt`).

### Batch JSONs (7 batches, 46 lessons total)

| Batch | Religion / Theme | Units | Lessons |
|-------|------------------|-------|---------|
| `_batch_buddhism.json` | Buddhism | beliefs + practices | 8 (4+4) |
| `_batch_catholic.json` | Catholic Christianity | beliefs + practices | 8 (4+4) |
| `_batch_hinduism.json` | Hinduism | beliefs + practices | 8 (4+4) |
| `_batch_judaism.json` | Judaism | beliefs + practices | 8 (4+4) |
| `_batch_sikhism.json` | Sikhism | beliefs + practices | 8 (4+4) |
| `_batch_theme_c.json` | Theme C — Existence of God & revelation | 1 unit | 3 |
| `_batch_theme_f.json` | Theme F — Religion, human rights & social justice | 1 unit | 3 |

Each batch entry carries: `lesson_id` (Supabase UUID), `unit_slug`, `lesson_number`, `slug`, `title`, `description`, `spec_references` (AQA 8062 codes such as `3.1.1.1`, `3.2.1.6`), `section_markers`, `suggested_question_types` (the 6 most useful types — agent picks the best 6 per lesson). All 46 lesson IDs were resolved against Supabase — verified counts match the plan exactly (4+4 per religion × 5 religions + 3 + 3 = 46).

### Standardised teaching brief

Each batch carries a `subject_level_teaching_brief` (10 misconceptions covering all 5 religions + Themes C & F; 7 student-error notes by question type covering all 7 registered types; 7 weighting notes; 3 spec-change notes; 7 pedagogical notes from EEF cognitive-science evidence) PLUS a `religion_specific_brief` containing sub-traditions to name, key textual sources, and tone notes specific to that religion / theme.

### Capstone distribution

Each lesson typically takes BOTH a 6-mark Explain (with required source-of-authority reference) AND a 12-mark Evaluate as the practice-question shape — that's the dominant AQA RS pattern (each religion / theme in the actual exam runs 1, 1, 4, 6, 12 marks). The agent prompt instructs picking the 6+12 pairing as the standard combination per lesson, with shorter-tariff applied questions filling out the remaining 4 of the 6 practice questions.

## Decisions / calls made

- **Batch grouping** — by religion (5 batches × 8 lessons) and by theme (2 batches × 3 lessons). 7 batches total. Religion batches share the same religion-specific brief across Beliefs and Practices for tonal consistency (a single batch covering both halves of a religion lets the agent reuse vocabulary, name eaters consistently, and avoid repetition across the 8 lessons). Theme batches stand alone.
- **Question type registry** — 7 types, 12-mark cap. AQA RS uses 1, 1, 4, 6, 12 marks per question stem; the registry exposes "2 marks — State / Give" and "8 marks — Discuss / Analyse" as available types for lessons where they fit, even though the dominant patterns are 1+1+4+6+12.
- **No "3 marks — Describe"** — AQA RS does not use a 3-mark band on the written paper, so it isn't in the registered list. Food Prep Eduqas does have it; RE does not. Agent prompt is explicit on this.
- **NO AO3 anywhere** — AQA RS has only AO1 (knowledge) and AO2 (analyse / evaluate). Half a dozen places in the agent prompt and spec slice flag this hard.
- **Reference lesson** — RE L01 "Worship & Prayer" (`21447890-d512-42c6-85f9-90b4133c06e3`) used as the structural pattern. It is a SIBLING lesson in this exact subject (Christianity Practices L1) — perfect structural reference.
- **Tone bias** — explicit instruction on neutrality: each religion as a living tradition; sub-traditions named where they differ; no comparative ranking; no authorial judgement on truth claims OR on Theme F's contested issues.
- **Theme F scope** — covers human rights, women's rights, LGBTQ+ rights, racial discrimination, wealth. The death penalty (which some boards bundle with Theme F) belongs to Theme E (already built). Agent prompt is explicit on this.
- **Path A neutrality** — not strictly required (AQA-only subject) but consistency rule: don't write "AQA" in user-facing prose. Use "your exam", "GCSE Religious Studies", "the written paper".

## Anything missing or needing watch

- **No issues blocking content fan-out.** All 46 lesson IDs resolved, all 7 batches written, spec slice and reference lesson on disk, prompts complete.
- **Validator alignment** — required `_verify_subject_build.py` category groups (Podcasts / Videos & Channels / one of Movies-TV Shows-Documentaries / Study Tools, ≥6 items per lesson) explicitly spelled out in `_RELATED_MEDIA_PROMPT.md`. Default category for the third slot is `Documentaries` (RE has a strong religion-documentary canon) but the curator can swap to `TV Shows` for Theme F lessons that touch on contemporary social-justice topics.
- **Spec slice not committed** — by design (`.gitignore` rule `scripts/_content_*/_spec_*.txt`). Local-only, written for content agents to read at fan-out time.
- **Plan vs Supabase** — plan lesson `description` was used to populate Supabase shells (verified at fetch). Both plan-derived `spec_references` and `section_markers` flow into the batch JSON to give agents the topic anchors.
- **Catholic Christianity vs Christianity** — the existing `christianity-beliefs` / `christianity-practices` units cover the broader-Christianity spec content (3.1.2). `catholic-christianity-beliefs` / `catholic-christianity-practices` cover the distinctive Catholic content (3.1.3). Both ship as options because schools may teach either (just not both as their assessed pair). Agent prompt's religion-specific brief for Catholic flags Orthodox / Protestant contrast as required by the spec.

## Confirm: scope of changes

**Only the new directory `scripts/_content_religious-education-gap-fill/` was modified / created.** No edits to other directories, no Supabase writes (Phase 2 already activated lessons; this phase reads from Supabase only). Two temporary helper scripts written during prep (`scripts/_tmp_fetch_re_gap_fill.py` and `scripts/_tmp_make_re_gap_fill_batches.py`) — these can be deleted; they were one-shot generators for the batch JSONs and the reference lesson fetch.
