# Edexcel Spanish (1SP1) — Phase 3 Scaffolding Prep Report

**Date:** 2026-05-04
**Phase:** 3 (practice content generation — scaffolding only, no content generated yet)
**Subject:** Spanish, Pearson Edexcel 1SP1, free tier
**Supabase subject_id:** `512c030a-4f65-45a7-a542-aa3661d29a26`

## Files created

All under `scripts/_content_spanish-edexcel/`:

| File | Purpose |
|---|---|
| `_AGENT_PROMPT.md` | Phase 3 content agent system prompt — Spanish-adapted from French Edexcel; embeds ser/estar, por/para, preterite/imperfect, personal a, demonstratives, lowercase nationalities, desde hace + present, indefinite-article-omission with profession, gustar agreement, double negation, subject pronoun omission, inverted punctuation. Voices for dictation references: `es-ES-AlvaroNeural` / `es-ES-ElviraNeural`. |
| `_RELATED_MEDIA_PROMPT.md` | Spanish related-media curation prompt. HEAD-validated ROOT URLs only — sources biased to BBC Bitesize / BBC Sounds / RTVE / iPlayer / Languages Online / Notes in Spanish / Dreaming Spanish / News in Slow Spanish / Coffee Break Spanish. No fabricated deep links (per recent retraction). |
| `_reference_lesson.json` | Canonical structural reference — pulled `spanish-aqa` `people-and-lifestyle` L01 "Family and Describing People" (`practice_data` only). |
| `_spec_spanish-edexcel.txt` | Spec slice extracted from `specs/edexcel/spanish-2024-1SP1.md`. 8 sections: qualification overview, AOs, themes, role-play settings, vocab Appendix 1 overview + per-theme pointers, grammar Appendix 2 overview, Appendix 3 names, spec changes. **Auto-gitignored** via `.gitignore:25` (`scripts/_content_*/_spec_*.txt`). |
| `_source/` (19 files) | AQA Spanish source `practice_data` for every plan lesson with `transfer_score` ∈ {high, medium}. |
| `_batch_t1_personal_world.json` | Theme 1 batch — 5 lessons. |
| `_batch_t2_lifestyle_wellbeing.json` | Theme 2 batch — 5 lessons. |
| `_batch_t3_neighbourhood.json` | Theme 3 batch — 4 lessons. |
| `_batch_t4_media_tech.json` | Theme 4 batch — 4 lessons. |
| `_batch_t5_studying_future.json` | Theme 5 batch — 4 lessons. |
| `_batch_t6_travel_tourism.json` | Theme 6 batch — 5 lessons. |
| `_prep_fetch.py` | One-shot prep script that pulled source lessons, the reference lesson, and built the 6 batch JSONs. Idempotent — read-only against Supabase. |
| `lessons/` | Empty output directory; agents write generated lesson JSONs here. |

## Source files pulled

19 unique files in `_source/`. Plan totals: **15 high + 6 medium + 3 low + 3 fresh = 27 lessons.** Source files cover the 21 high+medium lessons; some AQA source lessons are referenced by multiple Edexcel lessons (e.g. `aqa_communication-and-world_lesson_4.json` is shared by Travel L02 and L05; `aqa_popular-culture_lesson_2.json` is shared by Media L01 and L02), so 21 references resolve to 19 distinct files.

| Source unit | Files | Lesson numbers |
|---|---|---|
| `people-and-lifestyle` | 9 | 1, 2, 3, 4, 5, 6, 8, 9, 10 |
| `popular-culture` | 4 | 2, 3, 4, 8 |
| `communication-and-world` | 6 | 1, 2, 3, 4, 7, 8 |

## Batch breakdown

| Batch | Unit slug | Lessons | Tier mix | Transfer scores |
|---|---|---|---|---|
| `t1_personal_world` | `my-personal-world` | 5 | 4 both, 1 higher | 3 high, 0 medium, 1 low, 1 fresh |
| `t2_lifestyle_wellbeing` | `lifestyle-and-wellbeing` | 5 | 4 both, 1 higher | 4 high, 0 medium, 0 low, 1 fresh |
| `t3_neighbourhood` | `my-neighbourhood` | 4 | 4 both | 3 high, 0 medium, 1 low, 0 fresh |
| `t4_media_tech` | `media-and-technology` | 4 | 4 both | 1 high, 2 medium, 1 low, 0 fresh |
| `t5_studying_future` | `studying-and-my-future` | 4 | 4 both | 2 high, 1 medium, 0 low, 1 fresh |
| `t6_travel_tourism` | `travel-and-tourism` | 5 | 5 both | 2 high, 3 medium, 0 low, 0 fresh |
| **Totals** | | **27** | 25 both, 2 higher | **15 high, 6 medium, 3 low, 3 fresh** |

## Spanish-specific gotchas baked into the agent prompt

The agent prompt explicitly drills these Spanish-only rules (no French parallel):

1. **ser vs estar** — identity/origin/profession/permanent vs location/state/mood/temporary; bans `soy cansado`, `estoy profesor`.
2. **por vs para** — cause/exchange/duration vs purpose/destination/recipient.
3. **preterite vs imperfect** — completed vs descriptive/habitual past; French collapses both into the perfect, so habits don't transfer.
4. **personal a** — mandatory before definite human direct objects; `veo a mi hermano` not `veo mi hermano`.
5. **Three-way demonstratives** — este / ese / aquel (no aquel-equivalent in French).
6. **Lowercase nationalities and languages** — `español`, `inglés`, `francés` (capitalised in English, NOT in Spanish).
7. **desde hace + present** — Spanish uses present tense for ongoing duration; English uses perfect, French uses present too.
8. **No indefinite article before profession after ser** — `soy profesor`, not `soy un profesor`.
9. **Subject pronoun omission** — `hablo español`, not `yo hablo español` (unless emphatic).
10. **Double negative required** — `no veo nada`, never `veo nada`.
11. **Gustar agreement with thing-liked** — `me gusta el chocolate` (sg), `me gustan las manzanas` (pl); always sg with infinitives.
12. **Inverted punctuation** — `¿…?` and `¡…!` at the START of questions and exclamations.
13. **b/v indistinguishable in dictation** — the Spanish dictation pitfall.
14. **Written accents on stress-rule deviations and ALL question words** — qué, dónde, cómo, cuándo, por qué, cuál, cuánto.

## Three "fresh" lessons (no AQA source)

| Theme | Lesson | Tier | Notes |
|---|---|---|---|
| T1 L04 Equality and Inclusion | higher | Build from Edexcel Higher-tier social-issues lexis. Drill present subjunctive after `es importante que`. |
| T2 L04 Mental Wellbeing | higher | Build from Edexcel emotion/wellbeing vocab. Drill `estar` with emotions (estoy estresado, NOT soy estresado) and `sentirse + adjective`. |
| T5 L03 Jobs and Work Experience | both | Spanish AQA has NO dedicated jobs lesson (unlike French AQA). Build from Edexcel Appendix 1 vocab. Drill ser + profession with no article (soy profesor). |

## Unmatched / gaps

None. All 21 high/medium plan lessons resolved to source files. All 27 target lesson IDs resolved in Supabase.

## Verification

- Spec slice path matches `_AGENT_PROMPT.md` and the batch JSON `spec_slice_path` field.
- Reference lesson path matches batch JSON `reference_lesson_path` field.
- Agent prompt path matches batch JSON `agent_prompt_path` field.
- `output_dir` = `scripts/_content_spanish-edexcel/lessons` (the empty dir created above).
- `subject_id` in every batch matches Supabase: `512c030a-4f65-45a7-a542-aa3661d29a26`.

## Touched files

All work confined to `scripts/_content_spanish-edexcel/`. No files outside this directory were created or modified.

## Next step

Phase 3 content generation: dispatch each `_batch_t{1-6}_*.json` to a Sonnet 4.6 content agent with `_AGENT_PROMPT.md` as the system prompt. Agents write to `lessons/{slug}.json`. Validate via `scripts/_validate_content_json.py` before insertion.
