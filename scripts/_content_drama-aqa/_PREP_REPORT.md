# Drama AQA — Phase 3 Content Generation Prep Report

**Subject:** Drama (AQA 8261), free tier
**Scope:** 85 lessons across 12 units (3 universal + 9 set plays)
**Build status:** scaffolded; ready to dispatch content agents

---

## Deliverables under `scripts/_content_drama-aqa/`

| File | Purpose | Size |
|------|---------|------|
| `_AGENT_PROMPT.md` | Drama-specific content agent prompt (Phase 3) | 24.7 KB |
| `_spec_universal.txt` | Spec slice for Units 1–3 (theatre roles, practitioners, live theatre review) | 13.0 KB |
| `_spec_set-play.txt` | Spec slice for Units 4–12 (the 9 set plays share Section B framework) | 10.4 KB |
| `_reference_lesson.json` | Structural reference (RE Worship & Prayer, RE L01) | 21.3 KB |
| `_batch_universal_b1.json` | Theatre Roles & Stagecraft L1–5 (5 lessons) | — |
| `_batch_universal_b2.json` | Practitioners & Styles L1–4 (4 lessons) | — |
| `_batch_universal_b3.json` | Live Theatre Review L1–4 (4 lessons) | — |
| `_batch_{play}_b1.json` ×9 | Set play L1–4 (Plot/Characters/Themes/Context) | — |
| `_batch_{play}_b2.json` ×9 | Set play L5–8 (Methods/Staging/Performance/Practitioner) | — |
| `_build_batches.py` | Build script — assembles all 21 batches deterministically from the Phase 1 plan + per-play briefs | — |
| `lessons/` | Empty; populated by content agents | — |

**Total: 21 batch JSONs covering all 85 lessons.**

---

## Validation results

- 21 batch JSONs all valid JSON, all have the 12 required top-level keys.
- 85 unique lesson slugs match the 85 Supabase rows for `subjects.slug = 'drama-aqa'` exactly (no mismatches across all 12 units, all 85 lessons).
- No banned terms (`Award N marks for`, `Level 1`, `Section A/B/C`, `Component 1/2/3`, `Paper 1`, `8261`, `Nothing worthy of credit`) in user-facing strings (lesson titles, descriptions, slugs, unit subtitles).
- Question-type allow-list correctly enforced:
  - **Unit 3 (`live-theatre-review`)**: includes the `32 marks — Live Theatre Review` type; uses it in 4 of 4 lessons' suggested types.
  - **All 11 other units**: omit the 32-mark type. Allowed list is the 8 remaining names.
- Every lesson's `suggested_question_types` is a subset of its unit's `allowed_question_types_for_this_unit`.

---

## Per-play unit-level teaching briefs

The bulk of the Phase 3 prep work was the per-play `unit_level_teaching_brief` blocks. Each of the 9 set play units carries a brief with:

1. **synopsis** (3–4 sentences, no plot detail beyond what is needed for context)
2. **major_characters** (5–10 with one-line role descriptions, no copyrighted dialogue)
3. **major_themes** (5–7 themes with brief expansions)
4. **historical_context** (when written, when set, social/political backdrop)
5. **playwright_context** (key biographical points)
6. **dramatic_methods** (notable stylistic features — episodic, narrator-as-chorus, multi-roling, in-yer-face, naturalism, Frantic-Assembly hybrid, verse-vs-prose, documentary verbatim, etc.)
7. **key_scenes_for_staging** (5–7 named scenes/moments students often write about, with one-line descriptions — no dialogue reproduced)
8. **most_relevant_practitioners** (which practitioners apply best to this play, with justification)
9. **copyright_status** ("public domain" for Romeo & Juliet, "in copyright — 15-word cap, paraphrase preferred" for the other 8)
10. **stage_history_highlights** (1–2 notable productions for orientation; never used as worked examples for Live Theatre Review)
11. **common_misconceptions** (5 student errors specific to this play, anchored in published examiner / National Theatre Learn / ACT teacher guidance)

These briefs are the play-specific content agents need; the spec is generic across plays and doesn't list per-play content.

The two universal-content units (Theatre Roles & Stagecraft, Practitioners & Styles) carry shorter briefs focused on what students should remember + the unit's most common misconceptions.

The Live Theatre Review unit's brief codifies the **fictional-productions-only** rule: every worked example must reference a clearly imagined hypothetical production, never a real one, because each student writes about a different real production they have seen.

---

## Drama-specific content rules baked in

Every batch carries the full `drama_content_rules` block from the Phase 1 plan in its `subject_level_teaching_brief`. The headline rules:

1. **Performer-AND-Designer lens** on every set-play lesson (vocal/physical + at least one design discipline per worked example and mark scheme).
2. **Mandatory stagecraft terminology** (proxemics, gestus, gobo, soundscape, blocking, multi-roling, naturalism, fourth wall, tableau, etc.).
3. **No plot reproduction** — moments referenced by name only.
4. **15-word quotation cap** for in-copyright plays; max once per lesson; Romeo and Juliet exempt (public domain).
5. **Practice-question stems about staging**, not about quoted dialogue.
6. **Live Theatre Review = fictional productions only.**
7. **Practitioner application per play** — overrides specified per play in the unit brief.
8. **Glossary density** ≥6 entries (Drama is term-heavy — easy floor).
9. **British English** (theatre, behaviour, programme).

---

## Dispatch command pattern

```bash
# Per-batch agent dispatch (run via Claude Code Task tool, model: sonnet)
# Working directory: repo root.

# Wave 1 (5 agents in parallel — recommended):
#  - universal_b1, universal_b2, universal_b3, crucible_b1, blood-brothers_b1

# Wave 2 (5 agents):
#  - crucible_b2, blood-brothers_b2, noughts-and-crosses_b1, around-the-world_b1, things-i-know_b1

# Wave 3 (5 agents):
#  - noughts-and-crosses_b2, around-the-world_b2, things-i-know_b2, romeo-and-juliet_b1, taste-of-honey_b1

# Wave 4 (6 agents):
#  - romeo-and-juliet_b2, taste-of-honey_b2, great-wave_b1, great-wave_b2, empress_b1, empress_b2
```

Per-agent prompt (substitute `{batch_id}`):

```
You are a Drama (AQA) content generation agent. Read scripts/_content_drama-aqa/_AGENT_PROMPT.md in full, then generate content for batch_id={batch_id}. Read your batch input at scripts/_content_drama-aqa/_batch_{batch_id}.json. Write each lesson JSON to scripts/_content_drama-aqa/lessons/{lesson_slug}.json. Return only the BATCH_DONE status line.
```

---

## Wave-size recommendation

**5–6 agents per wave, 4 waves.** Reasoning:
- Each set-play batch loads roughly 30 KB of subject brief + 8 KB of unit brief + 13 KB of spec + 21 KB of reference lesson + 25 KB of agent prompt = ~100 KB of context per agent.
- Sonnet handles this comfortably; throttling is the constraint, not context.
- 5 agents × 4 lessons each = 20 lessons per wave. Total 4 waves cleanly partitions the 85 lessons.
- Wave 4 has 6 agents to fit the remainder; this is still well within parallel-dispatch comfort.
- Sequential set-play batch pairs (e.g. crucible_b1 then crucible_b2) help the second agent reuse cache implicitly when it loads the same play brief.

After each wave, validate the new lesson JSONs against `scripts/_validate_content_json.py` before dispatching the next wave; this catches HTML-entity-in-plain-text issues, banned-rubric-phrase issues and slug mismatches early.

---

## Post-Phase-3 next steps (not in this scaffold)

After all 85 lessons are generated and validated:
1. Insert via the standard activation script.
2. Hero images via Unsplash agent.
3. Narration via Azure Speech (Ollie odd / Ada even).
4. Related media (Phase 4) via the `related_media` agent prompt — same pattern as Citizenship, with podcast-into-related-media contract.
5. Revision technique guides (Phase 5) using the 7 templates in `docs/REVISION_TECHNIQUES/`, populated with Drama-specific examples.
6. Commit + tom_brief on the platform branch.
