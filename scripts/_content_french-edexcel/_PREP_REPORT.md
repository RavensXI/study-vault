# Edexcel French (1FR1) Phase 3 — Prep Report

## What was set up

Scaffolding for a cross-board adapted Phase 3, practice-first format. Twenty-seven lesson shells already exist in Supabase (subject id `1ce0c7a2-b375-448e-b12d-c4626c31bd11`, 6 units across 6 Edexcel themes). This directory now contains everything a fan-out of Sonnet 4.6 content agents needs to write the 27 lesson `practice_data` JSONs by adapting from the existing `french-aqa` source. No content was generated.

## Files produced (in `scripts/_content_french-edexcel/`)

### Prompts and reference
- **`_AGENT_PROMPT.md`** — content-agent system prompt. Covers practice-first cross-board adaptation, French-language correctness rules (gender / agreement / conjugation / accents / negation / articles / prepositions / past-participle agreement / pronoun position), Edexcel Appendix 1 prescribed vocabulary discipline, transfer-score adaptation logic (high/medium/low/fresh), 8+6+6=20 problem-count enforcement, three AI marking prompts (translate_to_target / role_play / writing), Edexcel's nine prescribed role-play settings, method-card / worked-example / plain-text-fields rules, ABSOLUTE BANS (board names, paper codes, French errors).
- **`_reference_lesson.json`** — full `practice_data` from AQA French L01 "Family Members and Descriptions" (id `0f3...`, fetched from Supabase). Canonical structural template only.
- **`_spec_french-edexcel.txt`** — Edexcel 1FR1 spec slice. Sections: Qualification overview (4 papers, 25% each); Assessment Objectives (AO1/AO2/AO3 with component breakdown); 6 thematic contexts; 9 prescribed role-play settings + Foundation/Higher rules; Appendix 1 vocabulary overview + key vocab pointers organised by theme; Appendix 2 grammar overview (nouns/pronouns/determiners, negation, interrogatives, reflexives, all 6 tenses + conditional + subjunctive + pluperfect + passive, adjectives, adverbs, prepositions, derivational morphology, sound-symbol correspondences); Appendix 3 names guidance; spec changes vs legacy. **Not committed to git** (matches `.gitignore` rule `scripts/_content_*/_spec_*.txt`).

### Source files (AQA French practice_data dumps)
- **`_source/`** — 19 dumps from `french-aqa` Supabase rows. **Not committed to git** (`.gitignore` rule `scripts/_content_*/_source/`).

  | Source unit | Lesson | Title |
  |-------------|--------|-------|
  | people-and-lifestyle | L01 | Family Members and Descriptions |
  | people-and-lifestyle | L02 | Friendships and Qualities |
  | people-and-lifestyle | L03 | Relationships, Marriage and Future Plans |
  | people-and-lifestyle | L04 | Healthy Living and Lifestyle |
  | people-and-lifestyle | L05 | Food, Drink and Mealtimes |
  | people-and-lifestyle | L06 | Body Parts, Illness and Wellbeing |
  | people-and-lifestyle | L07 | Sport and Staying Active |
  | people-and-lifestyle | L08 | School Subjects and Opinions |
  | people-and-lifestyle | L09 | School Life, Rules and Uniform |
  | people-and-lifestyle | L10 | Jobs, Work Experience and Future Plans |
  | communication-and-world | L01 | Holidays and Travel Plans |
  | communication-and-world | L02 | Past Holidays and Experiences |
  | communication-and-world | L03 | Accommodation and Hotels |
  | communication-and-world | L04 | Countries, Weather and Transport |
  | communication-and-world | L06 | My House and Home |
  | communication-and-world | L07 | My Town and Local Area |
  | communication-and-world | L08 | The Environment and Global Issues |
  | popular-culture | L02 | Music, Film and Television |
  | popular-culture | L06 | Celebrity Culture and Role Models |

### Batch JSONs (6 batches, 27 lessons total)

| Batch | Theme | Unit slug | Lessons | Lesson numbers | Tier mix |
|-------|-------|-----------|---------|----------------|----------|
| `_batch_t1_personal_world.json` | Theme 1 | my-personal-world | 5 | 1, 2, 3, 4, 5 | 4 both, 1 higher |
| `_batch_t2_lifestyle_wellbeing.json` | Theme 2 | lifestyle-and-wellbeing | 5 | 1, 2, 3, 4, 5 | 4 both, 1 higher |
| `_batch_t3_neighbourhood.json` | Theme 3 | my-neighbourhood | 4 | 1, 2, 3, 4 | 4 both |
| `_batch_t4_media_tech.json` | Theme 4 | media-and-technology | 4 | 1, 2, 3, 4 | 4 both |
| `_batch_t5_studying_future.json` | Theme 5 | studying-and-my-future | 4 | 1, 2, 3, 4 | 4 both |
| `_batch_t6_travel_tourism.json` | Theme 6 | travel-and-tourism | 5 | 1, 2, 3, 4, 5 | 5 both |

Each batch entry carries: `lesson_id` (Supabase UUID), `lesson_number`, `slug`, `title`, `description`, `tier`, `spec_references`, `section_markers`, `content_transfer` block, `source_aqa_file` (path or null).

## Transfer-score breakdown

Plan-stated transferability for the 27 lessons:
- **high (16)** — direct lift, problem structures reused with vocab refresh
- **medium (6)** — partial reuse, 50%+ of surface text rewritten
- **low (3)** — tone reference only, fresh build from spec slice
- **fresh (2)** — Edexcel-specific subjects (Equality and Inclusion T1L4; Mental Wellbeing and Healthy Living T2L4), no AQA source. Both pitched at Higher tier.

19 source files written (some AQA lessons referenced by multiple Edexcel lessons → deduplicated on disk: `popular-culture/L2`, `people-and-lifestyle/L10`, `communication-and-world/L4` were each referenced twice).

## Decisions / calls made

- **Practice-first format** — schema is `scripts/language-practice/PRACTICE_DATA_SCHEMA.md`. 8 bronze + 6 silver + 6 gold = 20 problems per lesson, twelve allowed input types, three shared `ai_marking_prompts`. Agent prompt enforces this hard.
- **AQA source as primary structural reference** — `french-aqa` already has fully-built `practice_data` for all 26 of its lessons. The Edexcel build inherits problem shapes wherever the topic aligns; agents adapt only what the prescribed Edexcel vocabulary/grammar requires.
- **French-correctness as the paramount rule** — agent prompt opens with non-negotiable language correctness. Gender, agreement, conjugation, accents, articles, prepositions all spelled out with examples and pitfalls. "If unsure, simplify" failsafe.
- **Edexcel Appendix 1 vocabulary discipline** — agent prompt instructs swapping non-Edexcel AQA vocab for Edexcel-prescribed equivalents, with worked examples (e.g. AQA `copain/copine` → Foundation `ami/amie`; AQA `sympa` → kept as informal acceptable).
- **Nine prescribed role-play settings embedded** — agent prompt maps lessons to natural settings (Theme 2 L03 → doctor's surgery; Theme 3 L02 → shop/market; Theme 3 L03 → train station; Theme 6 L03 → hotel + campsite branch; Theme 6 L05 → tourist info office).
- **Higher-only lessons** — T1L4 (Equality) and T2L4 (Mental Wellbeing) carry `tier: higher`. Agent prompt tells fresh-build agents to use abstract opinion language, Higher-only Appendix 1 vocab, and to drill Higher grammar harder (passive, subjunctive after `il faut que / pour que / bien que / avant que`, ne…que, complex relatives `auquel`/`dont`).
- **Reference lesson** — AQA French L01 "Family Members and Descriptions" used as canonical practice_data shape. Already structurally clean.
- **Routing keys** — agent must wrap output with `_lesson_id`, `_lesson_number`, `_unit_slug`, `_lesson_slug` (stripped at insert time but used by the insertion script to find the right Supabase row).

## Source-mapping mismatches in the plan (flagged, not fixed)

Two `content_transfer` blocks in `_plan_french-edexcel.json` point at AQA source lessons that don't match the description in `adaptation_notes`. The agent prompt instructs agents to read both the source file AND the adaptation_notes — these mismatches will surface during content generation.

1. **Theme 4 L03 "Social Media and Online Life"** — plan claims `source: communication-and-world/L6` but the actual L6 is "My House and Home". The adaptation_notes describe a "Direct lift from AQA L6 'Social Media: Pros and Cons'", which doesn't exist. The likely intended source is **`popular-culture/L7 "Social Media and Online Life"`** (exact title match) or **`communication-and-world/L5 "Technology and Social Media"`**.
   The current `_source/aqa_communication-and-world_lesson_6.json` (My House and Home) is irrelevant to this lesson. Agents will need to pull the correct source manually OR build fresh from the spec slice. **Action for content fan-out:** swap source to `popular-culture/L7` (closer topical match) before this batch runs.

2. **Theme 6 L04 "Tourist Attractions and Eating Out"** — plan claims `source: popular-culture/L6` but the actual L6 is "Celebrity Culture and Role Models". The adaptation_notes describe reusing "the restaurant role-play from AQA Popular Culture L6", which is in **`popular-culture/L8 "Eating Out and Restaurant Conversations"`** instead.
   The current `_source/aqa_popular-culture_lesson_6.json` (Celebrity Culture) is partly irrelevant. Tourist-attraction content will need fresh build; restaurant role-play should be pulled from L8. **Action for content fan-out:** also pull `popular-culture/L8` before this batch runs.

Both mismatches are logged here and not silently auto-corrected — Tom should decide whether to update the plan JSON before content gen or have agents handle the swap at fan-out time.

## Anything missing or needing watch

- **Two source-mapping mismatches** (above) — single most important thing to resolve before content fan-out. Recommend pulling the two corrected source files (`popular-culture/L7` and `popular-culture/L8`) and updating the relevant batches' `source_aqa_file` paths before running Theme 4 / Theme 6.
- **Dictation audio (Phase 4)** — TTS for dictation problems will run separately via `scripts/language-practice/generate_dictation_audio.py` after content is generated. Not part of this scaffolding.
- **Validator alignment** — the language-practice schema is enforced by `insert_practice_data.py` / `merge_and_insert.py` (in `scripts/language-practice/`). The agent prompt's "EXACTLY 20 problems" rule mirrors what the inserter expects.
- **No Eduqas / WJEC reuse** — French is offered by Edexcel + AQA + OCR + Eduqas, but only `french-aqa` is built on the platform. Cross-board adaptation is therefore single-source.
- **Spec slice not committed** — by design (`.gitignore` rule `scripts/_content_*/_spec_*.txt`). Local-only.
- **Source dumps not committed** — by design (`.gitignore` rule `scripts/_content_*/_source/`). Local-only.

## Confirm: scope of changes

**Only `scripts/_content_french-edexcel/` was modified / created.** No edits to other directories, no Supabase writes (Phase 2 already activated lessons; this phase reads from Supabase only). One temporary helper script written during prep (`scripts/_tmp_fetch_french_edexcel.py`) — this can be deleted; it was a one-shot generator for the source dumps, reference lesson, and batch JSONs.
