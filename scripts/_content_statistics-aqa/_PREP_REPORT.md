# Statistics AQA — Content Workspace Prep Report

Date: 2026-05-14

## Files created

| File | Purpose |
|---|---|
| `_AGENT_PROMPT_ARTICLE.md` | System prompt for article-format content agents (Units 1 + 5) |
| `_AGENT_PROMPT_PRACTICE.md` | System prompt for practice-format content agents (Units 2 + 3 + 4) |
| `_practice_reference_maths.json` | Supabase-fetched practice_data from Maths AQA Quadratic Graphs (id: c8bc060f) |
| `_reference_lesson_article.json` | Supabase-fetched RE L01 Worship & Prayer (id: 21447890) — structural template |
| `_batch_a01.json` | Article batch: Unit 1 planning-designing-enquiry (5 lessons) |
| `_batch_a02.json` | Article batch: Unit 5 interpreting-results-sec (4 lessons) |
| `_batch_p01.json` | Practice batch: Unit 2 representing-data (6 lessons) |
| `_batch_p02.json` | Practice batch: Unit 3 numerical-measures (7 lessons) |
| `_batch_p03.json` | Practice batch: Unit 4 probability-comparing-distributions (6 lessons) |

## Lesson counts

| Batch | Unit | Format | Lessons |
|---|---|---|---|
| a01 | planning-designing-enquiry | article | 5 |
| a02 | interpreting-results-sec | article | 4 |
| p01 | representing-data | practice | 6 |
| p02 | numerical-measures | practice | 7 |
| p03 | probability-comparing-distributions | practice | 6 |
| **Total** | | | **28** |

## Tier distribution

| Tier | Count | Unit distribution |
|---|---|---|
| foundation | 1 | representing-data L1 (tally charts) |
| both | 21 | all article lessons; most practice lessons |
| higher | 6 | representing-data L4; numerical-measures L3, L5, L7; probability L5, L6 |

## Pending draw-input decks (6)

These lessons have `pending_draw_input: true` — diagram-drawing problems are substituted with numeric/MCQ proxies:

- **representing-data L2** — bar/pie/stem-and-leaf (pie sector angles, MCQ chart selection)
- **representing-data L3** — frequency polygons (midpoint coordinate questions)
- **representing-data L4** — histograms with unequal class widths (forward + reverse density calculations)
- **representing-data L5** — cumulative frequency + box plots (read median/Q3; MCQ box plot selection)
- **representing-data L6** — scatter/population pyramids/choropleth (read values off labelled diagrams)
- **numerical-measures L6** — line of best fit + regression (double mean point coordinates; regression y-value)

## Notable divergences from Maths-shape practice

1. **Fraction input type added.** Statistics probability questions use `input_type: "fraction"` (with `solutions: [{numerator, denominator}]`) — this exists in the Maths platform but was not needed for the Maths reference lesson (Quadratic Graphs). The practice prompt documents this with a worked example.

2. **two_solutions used differently.** Maths uses `two_solutions` for quadratic roots (two numbers with same sign context). Stats uses it for Q1 + Q3 pairs and outlier pairs — the same schema, different mathematical context.

3. **No `ai_marking_prompts` field.** All Stats problems are deterministic (exact numeric answers, MCQ, fractions). The Maths reference has no AI marking either, so this is consistent. The practice prompt explicitly bans the field.

4. **`isAnswer` (not `is_answer`).** The Maths reference uses `isAnswer: true` (camelCase). The Science practice schema uses `is_answer: true` (snake_case). Stats follows the Maths convention per `_practice_reference_maths.json`.

5. **complete_table input type.** Stats needs to test cumulative frequency table completion and grouped frequency Σfx tables — the `complete_table` type is documented in the practice prompt with a CF example. The renderer should already support this (it exists in the representing-data plan's `practice_input_types`).

6. **Context-mandatory gold problems.** The teaching brief stresses that 45%+ of marks come from interpretation and methodology (AO2 + AO3). Gold problems in every practice deck must include at least one context-based comparison or explanation problem (not just additional numeric drills). The practice prompt bakes this into the Bronze/Silver/Gold calibration table.

7. **Higher-only whole-lesson decks.** Four practice lessons are tier=higher (representing-data L4, numerical-measures L3+L5+L7, probability L5+L6). The practice prompt instructs agents to set `higher_only: true` on all 20 problems in these lessons.

8. **Spec-formula-sheet awareness.** Unlike Maths (where most formulae are recalled), Stats has a two-tier formula status: some formulae are on the AQA Higher formula sheet (Spearman's, regression, standard deviation), others are in the question (all rate-of-change formulae), others must be recalled by all students (frequency density). Method cards must call this out explicitly.

## Subject-specific anti-hallucination flags baked into prompts

- No H₀/H₁ notation (explicitly excluded by AQA 8382 spec A1)
- No X~B(n,p) notation (spec uses "binomial" word only, n ≤ 5)
- No formal X-bar distribution notation (E13b: intuitive only)
- Correlation thresholds hardcoded: |r| ≥ 0.6 strong, 0.2–0.6 weak, < 0.2 no correlation
- No 3D representation drawing (spec C1b: interpretation only)

## Next steps for content agents

1. Run article agents on a01 and a02 in parallel (5 + 4 = 9 lessons; each under the 10-lesson agent limit)
2. Run practice agents on p01, p02, p03 in parallel (6 + 7 + 6 = 19 lessons total across 3 agents)
3. After content lands: run hero agent, narration agent, related media agent per lesson
4. Podcasts: article lessons (9) get NotebookLM podcasts; practice lessons (19) do not
5. Revision technique guides: one agent, reads docs/REVISION_TECHNIQUES/ and fills in Stats examples
6. Pre-ship: `python scripts/_verify_subject_build.py statistics-aqa`
7. Pre-ship: `python scripts/_fact_check_subject.py statistics-aqa` (article lessons only; skip practice — deterministic)
