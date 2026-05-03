# Phase 3 Prep Report — Physical Education (AQA) Free-Tier Build

**Date:** 2026-05-03
**Subject:** Physical Education, AQA, free tier (school_id NULL)
**Status:** Scaffolding complete — ready for content-agent dispatch.

---

## What was generated

All under `scripts/_content_physical-education-aqa/`:

| File | Purpose |
|---|---|
| `_AGENT_PROMPT.md` | Per-batch agent prompt template. PE-specific: 11 question types incl. Calculate / Calculate from Data / Interpret Data; StudyVault Mastering/Secure/Developing/Emerging rubric for 6+ marks; original-question-wording bans (no AQA trademark stems); fictional scenarios in 6/9-mark stems (real athletes only in `content_html`); ORIGINAL fabricated data tables for data-interpretation questions; British English spellings; no-diagram rule (free tier); ≥3 inline `<dfn>` and ≥6 glossary entries; PE terminology checklist (anatomy, physiology, training, psychology, ethics). |
| `_spec_human-body-and-movement.txt` | Paper 1 spec extract — full 3.1.1 (Applied anatomy & physiology), 3.1.2 (Movement analysis), 3.1.3 (Physical training), 3.1.4 (Use of data). Page-number footers, copyright lines and "Visit aqa.org.uk" preambles stripped. Quantitative formulae footer added. |
| `_spec_socio-cultural-influences-and-wellbeing.txt` | Paper 2 spec extract — full 3.2.1 (Sports psychology), 3.2.2 (Socio-cultural), 3.2.3 (Health/fitness/wellbeing), plus a 3.2.4 Use-of-data appendix mirroring 3.1.4 with Paper-2-flavoured data scenarios. |
| `_reference_lesson.json` | Copy of RE L01 "Worship & Prayer" (Supabase id `21447890-d512-42c6-85f9-90b4133c06e3`) — duplicated from `scripts/_content_business-edexcel/_reference_lesson.json`. Used as STRUCTURAL template only. |
| `_batch_p1_b1.json` … `_batch_p2_b5.json` | 9 batch JSON inputs (4 Paper 1 batches, 5 Paper 2 batches). |
| `lessons/` | Empty output directory; agents will write per-lesson JSONs here. |

A one-shot helper `scripts/_gen_pe_batches.py` was used to build the 9 batches consistently from the plan. Discardable; left in place for re-runs if the plan changes.

## Batch grouping (33 lessons total)

**Paper 1 — Human Body & Movement** (16 lessons → 4+4+4+4):
- `p1_b1` — L1–4: Skeleton; Muscles & antagonistic pairs; Synovial joints; Cardiovascular system. *(Anatomy block.)*
- `p1_b2` — L5–8: Respiratory system; Aerobic vs anaerobic; Short/long-term effects; Lever systems. *(Physiology + first calculation lesson.)*
- `p1_b3` — L9–12: Planes & axes; Health/fitness components; Fitness testing; SPORT and FITT. *(Movement analysis + foundation training.)*
- `p1_b4` — L13–16: Methods of training; Optimising training; Warm-up/cool-down; Using data in PE. *(Training application + data lesson — heaviest calculation lesson.)*

**Paper 2 — Socio-cultural Influences & Wellbeing** (17 lessons → 4+4+4+3+2):
- `p2_b1` — L1–4: Skill/ability/classification; Goal setting & SMART; Information processing; Guidance.
- `p2_b2` — L5–8: Feedback; Arousal & inverted-U; Personality/aggression/motivation; Engagement patterns. *(Sports-psych theory block.)*
- `p2_b3` — L9–12: Commercialisation; Technology; Conduct; PEDs & blood doping. *(Ethics-and-society block — heavy 9-mark Evaluate territory.)*
- `p2_b4` — L13–15: Spectator behaviour & hooliganism; Physical/emotional/social wellbeing; Sedentary lifestyle/obesity/somatotypes.
- `p2_b5` — L16–17: Energy/diet/nutrition/hydration; Interpreting data on participation. *(Final pair — second data-interpretation lesson.)*

I kept Paper 1 as 4×4 (clean topic boundaries) and Paper 2 as 4+4+4+3+2 (rather than rebalancing to 4×4+1) because the topic boundaries align better with the AQA spec section breaks — sports psychology, socio-cultural, then wellbeing, then data — and agents work faster on coherent topic batches.

## Verification

- All 9 batch JSONs parse as valid JSON.
- All 33 declared slugs match the existing Supabase `lessons.slug` rows under subject `physical-education-aqa` (verified programmatically against live Supabase). Counts: 16 lessons in `human-body-and-movement`, 17 lessons in `socio-cultural-influences-and-wellbeing`. Zero missing, zero extra.
- `allowed_question_types_for_this_unit` is the full 11-entry list for both units (PE has no paper-vs-paper question-type restriction — calculations and data-interpretation appear on both papers per the spec; the difference is what the data is *about*, not which formats are allowed).
- Subject-level teaching brief (5 misconceptions, 5 question-type error patterns, 4 weighting notes, 2 spec-change notes, 8 pedagogical notes) embedded in every batch with citations preserved.
- Unit-level teaching brief is `{}` per the prompt instruction (Phase 1 didn't break it down by unit).
- Banned-string scan: occurrences of `8582`, `Paper 1`, `Paper 2`, `Award N marks for`, `Nothing worthy of credit` in batch JSONs are confined to (a) source URLs inside citations within the teaching brief (e.g. `AQA-8582-VOCAB.PDF`), and (b) instructional text in `pedagogical_notes` / `student_errors_by_question_type` that tells the agent to AVOID those patterns. None ships in user-facing strings; this is the same posture as the Business Edexcel scaffold. Spec slice files contain "Paper 1" / "Paper 2" in their own headers as scaffolding signposts for the agent — those files are agent input, never copied into lesson output.

## Decisions made

1. **5 batches in Paper 2 not 4** — tagging on a 2-lesson `p2_b5` for the final data-interpretation lesson + nutrition lesson. Keeps each batch ≤ 4 lessons.
2. **`allowed_question_types_for_this_unit` = full 11** — no paper-bound restriction. Calculations and data interpretation appear on both papers; the registered set has no paper-coded variants.
3. **Reference lesson copied locally** — saved `_reference_lesson.json` next to the batches so agents do not need Supabase access just for the structural template. Source is still RE L01.
4. **Spec slice mirrors plan structure** — Paper 1 file holds 3.1.1–3.1.4 inclusive; Paper 2 file holds 3.2.1–3.2.3 plus a 3.2.4 use-of-data appendix that mirrors 3.1.4 (the spec puts use-of-data only in section 3.1.4, but it's assessed on both papers, so I duplicated the rules into the Paper 2 file with Paper-2 example contexts so the agent doesn't need to cross-read).
5. **Calculation guidance front-loaded in agent prompt** — PE has built-in calculation territory (cardiac output, max HR, training zones, mechanical advantage, one rep max, energy macros). The prompt explicitly calls out which lessons should include a calculation question.
6. **Data-interpretation question rule** — agent must FABRICATE original data tables / graph descriptions in the question stem. Plan already says this; prompt enforces with concrete examples.
7. **Real-athlete rule** — real elite athletes are FINE in `content_html` for illustrative examples (Mo Farah, Jess Ennis-Hill, Anthony Joshua, Marcus Rashford, Dame Sarah Storey, Adam Peaty). Marked 6/9-mark question stems must use ORIGINAL fictional scenarios (no athlete names; descriptive only — "16-year-old county-level netball player", etc.).
8. **No-diagram rule explicit** — free-tier PE has no diagrams. Prompt forbids "as shown in the diagram below" type prose. Anatomy is taught through precise spatial description.
9. **Glossary minimum bumped** — PE is terminology-dense, so `_AGENT_PROMPT.md` requires ≥6 `glossary_terms` entries (and ≥3 inline `<dfn>` per CONTENT_PROMPT.md).
10. **British English spelling enforced** — anaerobic, behaviour, fibre, organise, manoeuvre. PE-specific vocab checklist in the prompt.
11. **Suggested question types per lesson** — 5–7 per lesson, drawn from the registered 11. Calculation lessons (L4 cardiovascular, L8 levers, L14 optimising training, L16 data, P2 L16 nutrition, P2 L17 data) get `2 marks — Calculate` or `3 marks — Calculate from Data`. Data lessons additionally get `4 marks — Interpret Data`. Engagement/socio-cultural lessons get `9 marks — Evaluate` (ethical territory). Anatomy lessons get `1 mark — Identify` and `2 marks — Define` plus higher tariffs.

## Dispatch pattern for the main session

```
For each batch_id in [p1_b1, p1_b2, p1_b3, p1_b4, p2_b1, p2_b2, p2_b3, p2_b4, p2_b5]:

  Spawn an Agent (model: "sonnet") with the system prompt = contents of
    scripts/_content_physical-education-aqa/_AGENT_PROMPT.md

  User message = "Your batch_id is {batch_id}. Read scripts/_content_physical-education-aqa/_batch_{batch_id}.json
                  and proceed."

  Each agent writes 2-4 JSONs into scripts/_content_physical-education-aqa/lessons/
  and returns: BATCH_DONE: batch_id={batch_id}, lessons_written={N}, files=...

Run all 9 in parallel — they share inputs read-only and write to disjoint output filenames.
```

Total expected: 33 lesson JSONs at `scripts/_content_physical-education-aqa/lessons/{slug}.json`. Once written, validate with `scripts/_validate_content_json.py`, then run the standard insertion script to upsert into Supabase against the existing rows (matched by `_unit_slug` + `_lesson_number` or `_lesson_slug`).

## Anything else

- No script-level QA was done on individual lesson outputs — that's Tom's visual review in `/admin/review`.
- Phase 1 plan, Phase 2 activation, and Supabase rows (33) are all confirmed in place; this scaffold writes Phase 3 content directly into the existing lesson rows.
- After Phase 3 content is in, Phase 4 (heroes / narration / podcasts / related media) can run without touching this scaffolding.
- `scripts/_gen_pe_batches.py` is left alongside other one-shots in `scripts/`. Re-runnable if the plan changes.
