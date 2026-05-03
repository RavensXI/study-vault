# Phase 3 Prep Report — Business (Edexcel) Free-Tier Build

**Date:** 2026-05-03
**Subject:** Business Studies, Edexcel, free tier (school_id NULL)
**Status:** Scaffolding complete — ready for content-agent dispatch.

---

## What was generated

All under `scripts/_content_business-edexcel/`:

| File | Purpose |
|---|---|
| `_AGENT_PROMPT.md` | Per-batch agent prompt template (Business-specific bans, calculation guidance, original-case-study rule, StudyVault rubric, ≥6 glossary entries, command-word fidelity, Edexcel terminology). |
| `_spec_investigating-small-business.txt` | Theme 1 spec extract (Topics 1.1–1.5, full subject content) + Appendix 1 (command words) + Appendix 3 (formulae) footer. Page numbers / copyright lines / paper code preamble stripped. |
| `_spec_building-a-business.txt` | Theme 2 spec extract (Topics 2.1–2.5) + same Appendix 1 / 3 footer. |
| `_reference_lesson.json` | Copy of RE L01 "Worship & Prayer" (Supabase id `21447890-d512-42c6-85f9-90b4133c06e3`) — duplicated from `scripts/_content_history-edexcel/_reference_lesson.json`. Used as STRUCTURAL template only. |
| `_batch_t1_b1.json` … `_batch_t2_b4.json` | 8 batch JSON inputs (4 per theme). |
| `lessons/` | Empty output directory; agents will write per-lesson JSONs here. |

## Batch grouping (30 lessons total)

**Theme 1 — Investigating Small Business** (15 lessons → 4 + 4 + 4 + 3):
- `t1_b1` — L1–4: Enterprise & dynamic environment; Entrepreneur; Customer needs / market research; Segmentation & mapping.
- `t1_b2` — L5–8: Competitive environment; Aims & calculations; Break-even & margin of safety; Cash & cash-flow forecasting. *(Calculation-heavy.)*
- `t1_b3` — L9–12: Sources of finance; Ownership & limited liability; Location & marketing mix; Business plan.
- `t1_b4` — L13–15: Stakeholders; Technology & legislation; Economic climate.

**Theme 2 — Building a Business** (15 lessons → 4 + 4 + 4 + 3):
- `t2_b1` — L1–4: Growth methods; Aims & objectives change; Globalisation; Ethics, environment, pressure groups.
- `t2_b2` — L5–8: Product life cycle; Pricing & promotion; Place & integrated marketing mix; Production processes.
- `t2_b3` — L9–12: Stock & suppliers; Quality & sales process; Profit calculations & ARR; Interpreting business data. *(Calculation-heavy.)*
- `t2_b4` — L13–15: Org structures & ways of working; Recruitment, training & development; Motivation.

I rebalanced the suggested grouping (which would have left T2 b4 with 5 lessons) to a 4+4+4+3 split for better agent cognitive load.

## Verification

- All 8 batch JSONs parse as valid JSON.
- All 30 declared slugs match the slugify rule used by the activation script (verified programmatically).
- All 30 declared slugs match the existing Supabase `lessons.slug` rows under subject `business-edexcel` (verified programmatically against live Supabase). Counts: 15 lessons in `investigating-small-business`, 15 lessons in `building-a-business`.
- Banned-string grep scan clean — only occurrences are inside the explicit BANS section of `_AGENT_PROMPT.md` telling the agent NOT to use them.
- `allowed_question_types_for_this_unit` is the full 14-entry list for both units (Business has no paper-vs-paper question-type split — calculations + extended writing appear on both themes per the spec).
- Subject-level teaching brief (8 misconceptions, 6 question-type error patterns, 6 weighting notes, 2 spec-change notes, 4 pedagogical notes) embedded in every batch with citations preserved.
- Unit-level teaching brief is `{}` per the prompt instruction (Phase 1 didn't break it down by unit).

## Decisions made

1. **Batch split rebalanced** — chose 4+4+4+3 / 4+4+4+3 over the suggested 4+4+4+3 / 4+3+3+5 to keep all batches ≤ 4 lessons.
2. **`allowed_question_types_for_this_unit` = full list** — Business has no paper-bound question-type restriction (unlike History where Paper 2 British Depth has only 4 allowed types).
3. **Reference lesson copied locally** — saved `_reference_lesson.json` next to the batches so agents do not need Supabase access just for the structural template. Source is still RE L01 (`21447890-d512-42c6-85f9-90b4133c06e3`).
4. **Spec extracts include Appendices 1 + 3 in BOTH theme files** — both themes use the command words (Appendix 1) and formulae (Appendix 3), so duplicating saves agents a cross-file lookup.
5. **`unit_level_teaching_brief = {}`** — Phase 1 plan put everything at subject level. Agents fall back to the subject brief, which is rich enough.
6. **Calculation guidance front-loaded in agent prompt** — Business has more numeric questions than History; the prompt explicitly calls out break-even / cash flow / profit margins / ARR with formula-and-substitution mark-scheme expectations.
7. **Original case-study rule** — agent prompt mandates fictional business names in 6/9/12-mark question stems (with a list of exemplar names), real businesses allowed only in `content_html` for illustration.
8. **Glossary minimum bumped** — Business is terminology-heavy, so `_AGENT_PROMPT.md` requires ≥6 `glossary_terms` entries (vs. CONTENT_PROMPT.md's general lower bound).

## Dispatch pattern for the main session

```
For each batch_id in [t1_b1, t1_b2, t1_b3, t1_b4, t2_b1, t2_b2, t2_b3, t2_b4]:

  Spawn an Agent (model:"sonnet") with the system prompt = contents of
    scripts/_content_business-edexcel/_AGENT_PROMPT.md

  User message = "Your batch_id is {batch_id}. Read scripts/_content_business-edexcel/_batch_{batch_id}.json
                  and proceed."

  Each agent writes 3–4 JSONs into scripts/_content_business-edexcel/lessons/
  and returns: BATCH_DONE: batch_id={batch_id}, lessons_written={N}, files=...

Run all 8 in parallel — they share inputs read-only and write to disjoint output filenames.
```

Total expected: 30 lesson JSONs at `scripts/_content_business-edexcel/lessons/{slug}.json`. Once written, validate with `scripts/_validate_content_json.py`, then run the standard insertion script to upsert into Supabase against the existing rows (matched by `_unit_slug` + `_lesson_number`).

## Anything else

- No script-level QA was done on individual lesson outputs — that's Tom's visual review in `/admin/review`.
- Phase 1 plan, Phase 2 activation, and Supabase rows are all confirmed in place; this scaffold writes Phase 3 content directly into the existing lesson rows.
- After Phase 3 content is in, Phase 4 (heroes / narration / podcasts / related media) can run without touching this scaffolding.
