# Phase 3 Prep Report — Citizenship Studies (AQA) Free-Tier Build

**Date:** 2026-05-03
**Subject:** Citizenship Studies, AQA, free tier (school_id NULL)
**Status:** Scaffolding complete — ready for content-agent dispatch.

---

## What was generated

All under `scripts/_content_citizenship-aqa/`:

| File | Purpose |
|---|---|
| `_AGENT_PROMPT.md` | Per-batch agent prompt template. Citizenship-specific: 9 generic question types (no Section A/B, no Source A/B/C); StudyVault Mastering/Secure/Developing/Emerging rubric for 8+ marks; original-question-wording bans; ORIGINAL fictional sources required for every Source Interpretation question; political impartiality rules block (DfE 2022 statutory guidance + Education Act s.406-407) front-and-centre as a non-negotiable; real-figure rules (historical OK, recent partisan only in neutral factual context, never in marked stems); ≥3 inline `<dfn>` and ≥6 glossary entries; British English spellings; no-diagram rule (free tier); citizenship terminology checklist (parliamentary, electoral, legal, international). |
| `_spec_politics-participation-active-citizenship.txt` | Unit 1 spec extract — full 3.1 (skills), 3.4 (Politics & Participation) and 3.5 (Active Citizenship). Page-number footers and "Visit aqa.org.uk" preambles stripped. Command-word taxonomy footer included. |
| `_spec_life-modern-britain-rights-responsibilities.txt` | Unit 2 spec extract — full 3.2 (Life in Modern Britain) and 3.3 (Rights and Responsibilities). 3.2.5 included with a note that it overlaps Active Citizenship taught in Unit 1. Command-word taxonomy footer included. |
| `_reference_lesson.json` | Copy of RE L01 "Worship & Prayer" (Supabase id `21447890-d512-42c6-85f9-90b4133c06e3`) — duplicated from `scripts/_content_physical-education-aqa/_reference_lesson.json`. STRUCTURAL template only. |
| `_batch_u1_b1.json` … `_batch_u2_b4.json` | 8 batch JSON inputs (4 Unit 1 batches, 4 Unit 2 batches). |
| `lessons/` | Empty output directory; agents will write per-lesson JSONs here. |

A one-shot helper `scripts/_gen_citizenship_batches.py` was used to build the 8 batches consistently from the plan. Discardable; left in place for re-runs if the plan changes.

## Batch grouping (29 lessons total)

**Unit 1 — Politics, Participation and Active Citizenship** (16 lessons → 4+4+4+4):
- `u1_b1` — L1-4: Democracy; British Constitution; Parliament; Bill becomes law. *(Foundations.)*
- `u1_b2` — L5-8: Government/PM/Cabinet; Political parties; Voting systems; Local & devolved. *(Power and elections.)*
- `u1_b3` — L9-12: Elections & turnout; Tax & spending; Other countries; Bringing change. *(Participation.)*
- `u1_b4` — L13-16: Digital democracy; Pressure groups & civil society; Two case studies; Planning a citizenship action. *(Active citizenship block.)*

**Unit 2 — Life in Modern Britain & Rights and Responsibilities** (13 lessons → 4+3+3+3):
- `u2_b1` — L1-4: British values; Identity & diversity; Migration; Media & free press. *(Life in Modern Britain.)*
- `u2_b2` — L5-7: UK in the world; Why society needs laws; Criminal vs civil. *(Bridge into Rights.)*
- `u2_b3` — L8-10: Police, courts & legal reps; Legal ages & three legal systems; History of rights. *(Legal system.)*
- `u2_b4` — L11-13: Crime & sentencing; Human rights & international law; Citizens in the legal system. *(Crime, rights, civic legal action.)*

I kept Unit 1 as 4×4 (clean topic boundaries: foundations / power / participation / active citizenship) and Unit 2 as 4+3+3+3 because the topic boundaries align with the spec section breaks — Life in Modern Britain runs L1-5, then Rights and Responsibilities runs L6-13. The 4+3+3+3 split keeps "Life in Modern Britain" together in batch 1, with batch 2 acting as a bridge (UK in the world finishes Life in Modern Britain; "why society needs laws" + "criminal vs civil" open Rights and Responsibilities).

## Verification

- All 8 batch JSONs parse as valid JSON.
- All 29 declared slugs match the existing Supabase `lessons.slug` rows under subject `citizenship-aqa` (verified programmatically against live Supabase). Counts: 16 lessons in `politics-participation-active-citizenship`, 13 lessons in `life-modern-britain-rights-responsibilities`. Zero missing, zero extra.
- `allowed_question_types_for_this_unit` is the full 9-entry list for both units (Citizenship has no unit-bound question-type restriction; the 9 generic command words are agnostic to which paper they appear on).
- Subject-level teaching brief (10 misconceptions, 9 question-type error patterns, 5 weighting notes, 2 spec-change notes, 7 pedagogical notes, plus the **`political_impartiality_rules`**, **`studyvault_mark_scheme_rules`** and **`source_authoring_rules`** blocks) embedded in every batch with citations preserved.
- Unit-level teaching brief is `{}` per the prompt instruction (Phase 1 didn't break it down by unit).
- Banned-string scan: zero occurrences of `Paper 1`, `Paper 2`, `Section A`, `Section B`, `Source A`, `Source B`, `Source C`, `8100/1`, `8100/2`, `Award N marks for`, or `Nothing worthy of credit` in the **user-facing fields** of any batch JSON (unit metadata + lessons_in_batch). The `subject_level_teaching_brief` legitimately contains some of these tokens as anti-examples (the agent is being told to avoid them), which mirrors the same posture as PE / Business Edexcel scaffolds. Spec slice files are agent input, never copied verbatim into lesson output.

## Decisions made

1. **8 batches, balanced 4 + 4** — Unit 1 splits cleanly into 4×4 by topic block; Unit 2 splits 4+3+3+3 to keep Life in Modern Britain in batch 1 and align the rest with spec section breaks.
2. **Both units allow the full 9 question types** — the qualification's command-word taxonomy is paper-agnostic. Source Interpretation appears on both papers.
3. **Reference lesson copied locally** — saved `_reference_lesson.json` next to the batches so agents do not need Supabase access just for the structural template. Source is still RE L01 (`21447890-d512-42c6-85f9-90b4133c06e3`).
4. **Spec slice grouping** — Unit 1 file holds 3.1 + 3.4 + 3.5 (skills + politics + active citizenship); Unit 2 file holds 3.2 + 3.3 (Life in Modern Britain + Rights and Responsibilities). 3.2.5 is included in the Unit 2 file with a cross-reference note flagging that civic-society / citizens-bringing-change is also taught in Unit 1 case-study lessons.
5. **Political impartiality embedded twice** — once in `pedagogical_notes` (high-level rule), once in the dedicated `political_impartiality_rules` block (full DfE 2022 framework). The agent prompt also pulls it forward as a non-negotiable above the schema rules.
6. **Source-authoring rules pulled into every batch** — fictional source authorship rule is critical because Source Interpretation is the most copyright-sensitive question type. Examples of acceptable and forbidden source types are in the brief and the prompt.
7. **Real political figures rules narrowed** — historical figures (Wollstonecraft, Pankhurst, Mandela, MLK Jr., Equiano) are fine in `content_html`. Recent partisan figures (Starmer, Sunak, Farage, Johnson) only in neutral factual context (e.g. naming the 2024 election outcome). NEVER in marked 8/12-mark question stems.
8. **Source Interpretation present in every lesson** — every lesson's `suggested_question_types` includes `4 marks — Source Interpretation` because source-handling is a recurring assessment skill on both papers.
9. **Glossary minimum bumped** — Citizenship is terminology-dense (parliamentary, electoral, legal, international), so `_AGENT_PROMPT.md` requires ≥6 `glossary_terms` entries (and ≥3 inline `<dfn>` per CONTENT_PROMPT.md).
10. **British English spelling enforced** — organise, behaviour, programme, recognise, defence, neighbour, judgement, manoeuvre. Citizenship-specific vocab checklist in the prompt covers parliamentary, electoral, legal, international and active-citizenship terminology.
11. **Suggested question types per lesson** — 6 per lesson, drawn from the registered 9. Each includes the 1-mark MCQ, a short-answer (Identify Two or State), a 4-mark mid-tariff (Describe or Explain), the 4-mark Source Interpretation, an 8-mark extended (Analyse or Discuss), and the 12-mark Evaluate. The Analyse / Discuss choice mirrors which is more natural for the topic — Discuss for contested-issue lessons (voting age, immigration, monarchy debate, sentencing) and Analyse for systems-and-process lessons (Parliament, courts, treaties).

## Dispatch pattern for the main session

```
For each batch_id in [u1_b1, u1_b2, u1_b3, u1_b4, u2_b1, u2_b2, u2_b3, u2_b4]:

  Spawn an Agent (model: "sonnet") with the system prompt = contents of
    scripts/_content_citizenship-aqa/_AGENT_PROMPT.md

  User message = "Your batch_id is {batch_id}. Read scripts/_content_citizenship-aqa/_batch_{batch_id}.json
                  and proceed."

  Each agent writes 3-4 JSONs into scripts/_content_citizenship-aqa/lessons/
  and returns: BATCH_DONE: batch_id={batch_id}, lessons_written={N}, files=...

Run all 8 in parallel — they share inputs read-only and write to disjoint output filenames.
```

Total expected: 29 lesson JSONs at `scripts/_content_citizenship-aqa/lessons/{slug}.json`. Once written, validate with `scripts/_validate_content_json.py`, then run the standard insertion script to upsert into Supabase against the existing rows (matched by `_unit_slug` + `_lesson_number` or `_lesson_slug`).

## Anything else

- No script-level QA was done on individual lesson outputs — that's Tom's visual review in `/admin/review`. Reviewer must check the political impartiality rules separately on every lesson before lifting `pending_review`.
- Phase 1 plan, Phase 2 activation, and Supabase rows (29) are all confirmed in place; this scaffold writes Phase 3 content directly into the existing lesson rows.
- After Phase 3 content is in, Phase 4 (heroes / narration / podcasts / related media) can run without touching this scaffolding.
- `scripts/_gen_citizenship_batches.py` is left alongside other one-shots in `scripts/`. Re-runnable if the plan changes.
