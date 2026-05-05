# Eduqas Food Preparation and Nutrition (C560QS) Phase 3 — Prep Report

## What was set up

Scaffolding for a fresh-build Phase 3. Sixteen lesson shells already exist in Supabase (subject id `088cd43e-5cf4-4af2-a0a3-7b5171ef83c8`, 9 in unit `food-science-and-nutrition` and 7 in unit `food-safety-provenance-and-choice`). This directory now contains everything a fan-out of Sonnet 4.6 content agents needs to write the 16 lesson JSONs from spec only. No cross-board source content was pulled — fresh build from spec, per Tom's directive (Unity bespoke Food Tech is school-specific, not a cross-board reuse source; AQA 8585 covers the same named subject but with different coverage and a different paper structure, so no transfer pipeline either).

## Files produced (in `scripts/_content_food-preparation-and-nutrition-eduqas/`)

### Prompts and reference
- `_AGENT_PROMPT.md` — content-agent system prompt. Fresh-build flavour, **Path A neutral phrasing** (never "Eduqas" or "WJEC" in user-facing prose — use "your exam", "this paper", "GCSE Food Preparation and Nutrition"), practical-applied tone bias (real cooking processes, real foods, real eaters), 12-mark cap on extended response (Eduqas does have 6 / 8 / 12 levels-based questions), 8 registered question types, AOs as plain `AO1` / `AO2` / `AO4` (AO3 is NEA-only — never used on this build), plain-text-fields enforcement, validator-aligned glossary >=6 / flashcards >=8 / 6 practice / 5 KCs / 2+ key-fact / 2+ collapsible rules, ABSOLUTE BANS section.
- `_RELATED_MEDIA_PROMPT.md` — related-media curator prompt. Required categories: Podcasts / Videos & Channels / one of {Movies, TV Shows, Documentaries} / Study Tools (per `_verify_subject_build.py`). Articles & Reading recommended as a 5th. UK-first sources biased to NHS Eatwell, FSA, BNF (Food a Fact of Life), Coeliac UK, Diabetes UK, BBC Good Food, BBC Food Programme, Sortedfood, Jamie Oliver, Adam Ragusea / Ethan Chlebowski for cooking science. Placeholder podcast pattern flagged for Tom's NotebookLM manual pass.
- `_reference_lesson.json` — full Supabase row for RE L01 "Worship & Prayer" (id `21447890-d512-42c6-85f9-90b4133c06e3`) — structural template only.

### Spec slice
- `_spec_food-preparation-and-nutrition.txt` — Eduqas C560QS Component 1 spec extract covering all 6 areas of content (Food commodities; Principles of nutrition; Diet and good health; The science of food; Where food comes from; Cooking and food preparation), plus AO weightings (AO1 20%, AO2 20%, AO4 10%) and a self-authored command-verb reference (Identify, State, Describe, Explain, Discuss, Analyse, Evaluate, Compare, Calculate). Component 2 (NEA) is excluded — those are practical project components delivered in school kitchens, not revision lessons. **Not committed to git** (matches `.gitignore` rule `scripts/_content_*/_spec_*.txt`).

### Batch JSONs (4 batches, 16 lessons total)

| Batch | Unit | Lessons | Lesson numbers |
|-------|------|---------|----------------|
| `_batch_u1_b1.json` | food-science-and-nutrition | 4 | 1, 2, 3, 4 |
| `_batch_u1_b2.json` | food-science-and-nutrition | 5 | 5, 6, 7, 8, 9 |
| `_batch_u2_b1.json` | food-safety-provenance-and-choice | 4 | 1, 2, 3, 4 |
| `_batch_u2_b2.json` | food-safety-provenance-and-choice | 3 | 5, 6, 7 |

Each batch entry carries: `lesson_id` (Supabase UUID), `lesson_number`, `slug`, `title`, `description`, `spec_references` (Eduqas area numbers `1`-`6`), `section_markers`, `suggested_question_types` (6 types per lesson — agent picks the best 6).

### Capstone distribution

12-mark Evaluate capstones assigned to lessons whose content sustains a reasoned qualitative judgement:
- U1 L6 — Diet, Health Conditions & Lifestyle Choices (evaluating diet adaptations for a named medical / lifestyle need)
- U2 L3 — Food Provenance & Sustainability (evaluating sustainability trade-offs of local vs imported food)
- U2 L7 — Developing Recipes & Meals for Specific Needs (evaluating recipe adaptations against a brief)

8-mark Discuss / Analyse capstones for lessons that sustain weighing perspectives:
- U1 L3 — Macronutrients (analysing complementary actions and consequences of malnutrition)
- U1 L5 — Energy Requirements & Life-Stage Diets (analysing energy balance / BMR / PAL)
- U1 L9 — Functional & Chemical Properties of Ingredients (analysing why a result was not achieved + remedy)
- U2 L2 — Food Poisoning, Bacteria & Cross-Contamination (analysing the chain from inadequate hygiene to outbreak)
- U2 L5 — Food Manufacturing, Processing & Modified Foods (analysing positive and negative effects of modification)

The remaining 8 lessons take a 6-mark Explain capstone (recall + reasoning).

## Decisions / calls made

- **Batch sizes** — 4 / 5 / 4 / 3, exactly as briefed. Boundaries follow Eduqas's 6 areas of content (Areas 1-3 in Unit 1, Areas 4-6 in Unit 2 with the food-science / food-spoilage split crossing the unit boundary on purpose so Unit 1 is "science / nutrition / planning" and Unit 2 is "safety / where food comes from / choice").
- **Question type registry** — 8 types, 12-mark cap. Eduqas Component 1 has 6 / 8 / 12-mark levels-based extended responses, so the cap is 12 (not 8 like OCR R032). No separate "Calculate" type — calculation work (Area 3 "Calculate energy and nutritional values") is folded into `2 marks — State / Give` and `4 marks — Explain` with explicit calculation steps in the mark scheme.
- **Path A neutral phrasing** — explicitly enforced in `_AGENT_PROMPT.md`. The Supabase row could later be reused for the WJEC equivalent (3550QS, Welsh maintained schools) without rewrites — that's the moat for board names.
- **Reference lesson** — RE L01 "Worship & Prayer" (`21447890-d512-42c6-85f9-90b4133c06e3`) used as the structural pattern, per `docs/REFERENCE_LESSONS.md`.
- **Fresh build** — no `_source/` directory and no AQA / OCR cross-board adaptation. Per Tom's brief.
- **Practical / applied tone bias** — explicit instruction in `_AGENT_PROMPT.md` to anchor every concept in a named real cooking situation + named eater + dish / context. Examples biased to plausible GCSE student cooking (Victoria sandwich, stir-fry, shortcrust pastry, sponge cake, Sunday roast) rather than restaurant-only or molecular-gastronomy framings.
- **Subject-level teaching brief** — copied verbatim from the plan JSON's `teaching_brief` block (9 misconceptions, 8 student errors by question type covering all 8 question types, 6 weighting notes, 3 spec-change notes, 7 pedagogical notes). Sourced from the C560QS spec text plus standard EEF cognitive-science evidence.

## Anything missing or needing watch

- **No issues blocking content fan-out.** All 16 lesson IDs resolved against Supabase, all 4 batches written and verified, spec slice and reference lesson on disk.
- **Validator alignment** — required `_verify_subject_build.py` category groups (Podcasts / Videos & Channels / one of Movies-TV Shows-Documentaries / Study Tools, ≥6 items per lesson) are explicitly spelled out in `_RELATED_MEDIA_PROMPT.md`. The default in the prompt is `TV Shows` (cooking TV is rich) but the curator can swap for `Documentaries` on sustainability / food-poverty / provenance lessons.
- **Calculation work caveat** — Area 3 includes calculating energy and nutrient values for recipes / meals / diets. The prompt notes this is folded into the existing `2 marks — State / Give` and `4 marks — Explain` types (with calculation steps in mark schemes); there is no separate `Calculate` type. Watch for content agents incorrectly inventing one.
- **Spec slice not committed** — by design (`.gitignore` rule `scripts/_content_*/_spec_*.txt`). Local-only, written for the content agents to read at fan-out time.

## Confirm: scope of changes

**Only the new directory `scripts/_content_food-preparation-and-nutrition-eduqas/` was modified / created.** No edits to other directories, no Supabase writes (Phase 2 already activated lessons; this phase reads from Supabase only). Two temporary helper scripts written during prep (`scripts/_tmp_fetch_food_prep_eduqas.py` and `scripts/_tmp_make_food_prep_batches.py`) — these can be deleted; they were one-shot generators for the batch JSONs and the reference lesson fetch.
