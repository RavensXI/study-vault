# Sociology AQA (8192) Phase 3 — Prep Report

## What was set up

Scaffolding for a fresh-build Phase 3. Thirty-three AQA Sociology 8192 lesson shells already exist in Supabase (subject id `6c46be2d-9c7c-47bf-840c-c6afd8a058b2`). This directory now contains everything a fan-out of Sonnet 4.6 content agents needs to write the 33 lesson JSONs from spec only. No cross-board source content was pulled — Tom's brief is explicit: fresh build (no other UK board offers GCSE Sociology — AQA is sole-supplier).

## Files produced (in `scripts/_content_sociology-aqa/`)

### Prompts and reference
- `_AGENT_PROMPT.md` — content-agent system prompt. Fresh-build flavour, neutral board phrasing (AQA only), academic-discursive tone bias, **multiple-perspectives-framing as the headline rule** (every contested topic gets functionalist / Marxist / feminist / interactionist / New Right / postmodernist treatment with no authorial line), 12-mark cap on extended response, 5 registered question types (no Calculate, no 6/8-mark — AQA's highest is 12), validator-aligned glossary >=6 / flashcards >=8 / 6 practice / 5 KCs / 2+ key-fact / 2+ collapsible rules, AQA Appendix B as the authoritative theorist pairing list, **named theorists with year + key concept guidance** (Durkheim, Marx, Weber, Parsons, Oakley, Willmott and Young, Rapoports, Zaretsky, Delphy and Leonard, Bowles and Gintis, Willis, Halsey, Ball, Becker, Merton, Heidensohn, Albert Cohen, Carlen, Davis and Moore, Townsend, Murray, Walby, Devine), sociological-vocabulary precision (sex vs gender, deviance vs crime, status vs role, etc.), original-fictional-scenario rule for case studies, plain-text-fields enforcement, ABSOLUTE BANS section.
- `_RELATED_MEDIA_PROMPT.md` — related-media curator prompt. Required categories: Podcasts / Videos & Channels / one of {Documentaries, Movies, TV Shows} / Study Tools (per `_verify_subject_build.py`). Articles & Reading recommended as a 5th. **CRITICAL: ROOT URLs ONLY for Study Tools** — explicit callout to the recent 731-broken-URL audit, with 6 approved root URLs (tutor2u.net/sociology, BBC Bitesize, Seneca, ONS, Ipsos UK, JRF). UK-first sources biased to BBC Sounds (Thinking Allowed, Analysis, More or Less, In Our Time), Tutor2u Sociology, The Sociology Show, JRF, Resolution Foundation, King's Fund. Sensitive-content note for crime, family breakdown, abuse, gender violence, racial inequality. Political-impartiality reminder for contested social policy.
- `_reference_lesson.json` — full Supabase row for RE L01 "Worship & Prayer" (id `21447890-d512-42c6-85f9-90b4133c06e3`) — structural template only.

### Spec slice
- `_spec_sociology.txt` — AQA 8192 spec extract: Section 3 (subject content, all 7 topic areas 3.1-3.7), plus Appendix A (key terms — authoritative vocabulary list), plus Appendix B (texts and summaries — authoritative theorist pairings). 86,267 chars / 2,667 lines. **Not committed to git** (matches `.gitignore` rule `scripts/_content_*/_spec_*.txt`).

### Batch JSONs (6 batches, 33 lessons total)
- `_batch_u1_methods.json` — Unit 1 lessons 1-6 (Studying Society and Research Methods). Sociological approach, classical thinkers, four perspectives, research design and sampling, methods (questionnaires/interviews/observation), practical and ethical issues.
- `_batch_u2_families.json` — Unit 2 lessons 1-7 (Families). Functions, family forms and Rapoports' diversity, conjugal roles and Oakley, changing relationships and Willmott and Young, criticisms (Zaretsky / Delphy and Leonard), divorce since 1945, researching families.
- `_batch_u3_education.json` — Unit 3 lessons 1-6 (Education). Roles and functions (Durkheim/Parsons), types of school, Bowles and Gintis correspondence principle, factors affecting achievement (Halsey / Ball), processes within schools (labelling / Willis), researching education.
- `_batch_u4a_crime_part1.json` — Unit 4 lessons 1-4 (Crime and Deviance, first half). Social construction, Merton functionalist/strain, Becker labelling, formal and informal social control with Heidensohn.
- `_batch_u4b_crime_part2.json` — Unit 4 lessons 5-7 (Crime and Deviance, second half). Factors affecting offending (Albert Cohen / Carlen), public debates, crime data and the dark figure.
- `_batch_u5_stratification.json` — Unit 5 lessons 1-7 (Social Stratification). Davis and Moore, Marx vs Weber on class, life chances and Devine, Townsend / Murray on poverty, Weber on power and authority, Walby on patriarchy, researching stratification and crime.

Each batch entry carries: `lesson_id` (Supabase UUID, all 33 verified live), `lesson_number`, `slug`, `title`, `description`, `spec_references` (AQA codes 3.1, 3.3.1, 3.4.3, 3.5.1, 3.6.5, 3.7 etc.), `section_markers` (verbatim from Phase 1 plan), `suggested_question_types` (all 5 registered types — agents pick the best 6 questions per lesson).

### Question type registry — 5 types

```
1 mark — Multiple Choice
2 marks — Define
3 marks — Identify and Describe
4 marks — Describe
12 marks — Discuss How Far Sociologists Would Agree
```

The 12-mark Discuss is the **cap** for AQA Sociology — every lesson gets one as the capstone. The other four are the recall + apply types that drill the named-list content (5 family forms, Rapoports' 5 diversity types, Merton's 5 responses, Weber's 3 authority types, Walby's 6 structures, the 4 perspectives, Appendix A's ~250 terms).

## Decisions / calls made

- **Batch sizes** — 6 / 7 / 6 / 4 / 3 / 7. Boundaries follow AQA's topic structure: each unit becomes its own batch except Crime which is split (4+3) per the user's brief because it's the longest single-perspective-heavy block. 33 lessons in 6 batches sits in the 4-7 lessons-per-batch sweet spot.
- **Question type registry** — 5 types (Multiple Choice / Define / Identify and Describe / Describe / Discuss). Pulled verbatim from the Phase 1 plan's `question_type_names`. AQA Sociology has no calculation content and no 6/8-mark questions — the 12-mark Discuss is where AO3 (analysis and evaluation) is awarded, and it is the highest-mark question on each paper.
- **Reference lesson** — RE L01 "Worship & Prayer" (`21447890-d512-42c6-85f9-90b4133c06e3`) used as the structural pattern, per `docs/REFERENCE_LESSONS.md`.
- **Fresh build** — no `_source/` directory. AQA is the sole UK board offering GCSE Sociology (OCR no longer offers it; Eduqas is A-level only). Per Tom's brief, no cross-board adaptation is appropriate.
- **Neutral board phrasing** — AQA is named where it clarifies (command-word definitions, paper structure). Default to neutral phrasing ("your exam", "this paper", "GCSE Sociology") elsewhere. No other boards mentioned.
- **Multiple perspectives framing** — the most distinctive Sociology rule. Every topic that admits perspectival disagreement must present competing perspectives factually. Authorial line: NONE. Explicit examples in the agent prompt for family diversity, gender roles, ethnic inequality, class inequality, crime, poverty.
- **Named theorists** — Appendix B is the authoritative pairing list. The agent prompt names every theorist on the spec with their key concept and (where known) the year of the work. Agents are explicitly told NOT to introduce theorists outside Appendix B.
- **Fictional scenarios** — for any lesson needing illustrative case studies (especially research methods lessons). UK context throughout (ONS, Crime Survey for England and Wales, Divorce Reform Act 1969, UK educational policy).
- **Subject-level teaching brief** — copied verbatim from the Phase 1 plan's `teaching_brief` (10 misconceptions, 5 student errors by question type, 6 weighting notes, 3 spec-change notes, 7 pedagogical notes). Sourced from the AQA 8192 spec text, AQA examiner reports referenced via published examiner commentary, and standard EEF cognitive-science evidence.
- **Quote ticker** — built from the plan's `quote_ticker_quotes` (Mills, Marx, Boosler, Twain, Machiavelli, Marx) into the unit's quote-ticker HTML for downstream lesson-page rendering.

## Anything missing or needing watch

- **No issues blocking content fan-out.** All 33 lesson IDs resolved against Supabase, all 6 batches written and verified, spec slice and reference lesson on disk, agent prompts cover all the AQA-specific gotchas.
- **Validator alignment** — required `_verify_subject_build.py` category groups (Podcasts / Videos & Channels / one of Documentaries-Movies-TV Shows / Study Tools, ≥6 items per lesson) are explicitly spelled out in `_RELATED_MEDIA_PROMPT.md`.
- **Broken-URL prevention** — the related-media prompt has the strongest "ROOT URLs ONLY" warning of any subject build to date, with the exact 6 approved root URLs listed for Study Tools. Direct response to the 731-broken-URL audit.
- **Sensitive-content awareness** — flagged in `_RELATED_MEDIA_PROMPT.md` for crime, family breakdown, abuse, gender violence (Walby), racial inequality, poverty. Curators steered toward analytical sources (BBC Reality Check, Guardian Long Read, BBC Ideas, FT Weekend, The Conversation UK) and away from tabloid coverage. Explicit note on political impartiality for contested social policy topics.
- **Spec slice not committed** — by design (`.gitignore` rule `scripts/_content_*/_spec_*.txt`). Local-only, written for the content agents to read at fan-out time.
- **Murray (New Right) handling** — flagged in the agent prompt for careful neutral framing. The underclass thesis is contentious; the prompt directs agents to describe it as "Murray's New Right argument that..." and balance with Townsend's structural counter.

## Confirm: scope of changes

**Only the new directory `scripts/_content_sociology-aqa/` was modified.** No edits to other directories, no Supabase writes (Phase 2 already activated lessons; this phase reads from Supabase only for the reference lesson row and for ID verification). The fetcher reads from `specs/aqa/sociology-8192-8192.md` (existing), the plan at `scripts/_plan_sociology-aqa.json` (existing), and live Supabase rows — none of those were modified.

## Files in directory

```
scripts/_content_sociology-aqa/
├── _AGENT_PROMPT.md                  (content agent system prompt)
├── _RELATED_MEDIA_PROMPT.md          (related media curator prompt)
├── _PREP_REPORT.md                   (this file)
├── _reference_lesson.json            (RE L01 — structural template)
├── _spec_sociology.txt               (AQA 8192 spec slice — gitignored)
├── _batch_u1_methods.json            (6 lessons)
├── _batch_u2_families.json           (7 lessons)
├── _batch_u3_education.json          (6 lessons)
├── _batch_u4a_crime_part1.json       (4 lessons)
├── _batch_u4b_crime_part2.json       (3 lessons)
├── _batch_u5_stratification.json     (7 lessons)
└── lessons/                          (empty — content agents write here)
```
