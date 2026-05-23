# Eduqas History Content Agent Prompt (Phase 3)

You are generating content for **Eduqas GCSE History (C100QS)** — England-market spec (NOT WJEC 3100QS, which is Wales-only). One Sonnet agent per batch (one pathway = one unit).

## Files to read first

1. `docs/CONTENT_PROMPT.md` — schema, ABSOLUTE BANS.
2. `docs/LESSON_TEMPLATE.md` — HTML components.
3. `docs/FLASHCARD_RULES.md` — flashcard rules.
4. `scripts/_content_history-eduqas/_batch_{batch_id}.json` — YOUR batch (one full pathway / unit).
5. **Critical fact-check anchor:** `docs/REFERENCE_LESSONS.md` — pinned RE L01 ID `21447890-d512-42c6-85f9-90b4133c06e3` (RE "Worship & Prayer") — structural reference.
6. If your batch has high/medium transfer source lessons (look at `lessons_in_batch[].source_subject_slug` + `source_unit_slug` + `source_lesson_number`), the relevant AQA / Edexcel lesson may already have been fetched at one of these patterns:
   - `scripts/_content_history-{board}-{unit_slug}.json` (single-pathway plans)
   - Otherwise, work from `adaptation_notes` + `section_markers` (no source export step for this build given the volume).

## Subject framing — Eduqas History

### Audience
- Proper GCSE (years 10-11, ages 14-16). Use precise historical terminology with explanations. Cite years and named figures accurately.

### Structure of YOUR pathway
Check `unit.pathway_category`:
- **`british-depth`** (1A-1D) — narrow time window, deep coverage of a British era
- **`non-british-depth`** (1E-1H) — narrow time window, deep coverage of a non-British era
- **`period-study`** (2A-2D) — wider time-span period (~50-100 years) covering one country/region
- **`thematic-study`** (2E-2H) — long-sweep change-and-continuity thematic c500-present. These have a **historic environment site** (capture in content_html for the relevant lesson — see `unit.historic_environment_site_2026_2027` if present in your batch)

### Eduqas question types (mark allocations in your batch)
- 2-mark "Describe one feature" — short factual recall
- 4-mark "Describe two features" — paired short recall
- 5-mark "How useful are sources..." (source utility)
- 6-mark "Causation: explain the consequences/causes..." (cause/consequence)
- 8-mark "Cause/Significance/Consequence" (deeper analytical) — STUDYVAULT RUBRIC tiers
- 10-mark "Why do interpretations differ..." (historiography)
- 12-mark "How far do you agree..." extended essay — Mastering/Secure/Developing/Emerging
- 16-mark "Account for..." extended essay — Mastering/Secure/Developing/Emerging
- Other registered types: check your batch's `registered_question_type_names`

### Historic facts must be accurate
Eduqas History will run through the mandatory fact-check pass. Common sense rule: every named date, person, place, treaty, battle, act of parliament, or statistic must be verifiable. When in doubt, prefer the most widely-cited consensus figure rather than a specific contested number. Use:
- Years/dates: accurate ±0 years for named events
- Named people: correct attribution + role
- Treaties / Acts: correct year + key terms
- Statistics: prefer ranges or cite "approximately" if disputed
- Quotes: only use widely-documented quotes; if uncertain, summarise without quoting

### Sensitive content guidance
- Slavery, Holocaust, racism, colonial violence, war crimes — handle with historical precision. Avoid sensationalism. Cite primary-source evidence where naming atrocities.
- Religious belief — describe doctrines without endorsing/denigrating.

## Free-tier (mandatory)

- NO `diagram_prompt`, NO `<!-- DIAGRAM -->` placeholder.
- Schema must have ONLY keys listed in CONTENT_PROMPT.md + 3 underscore-prefixed routing keys.

## content_html

- 800-1500 words excluding tags.
- Sequential `data-narration-id` (no gaps).
- ≥2 `<div class="key-fact">` with actionable `data-revision-tip`.
- ≥2 `<div class="collapsible">`.
- ≥3 `<dfn class="term" data-def="...">` inline.
- NO `<h1>` tags.
- HTML entities ALLOWED in content_html / exam_tip_html / conclusion_html.
- **Plain text in `description`, `practice_questions`, `knowledge_checks`, `flashcard_questions`, `glossary_terms`** — unicode quotes/dashes, NOT HTML entities.

## Knowledge checks (exactly 5)

- 2 MCQ + 2 fill + 1 match.
- MCQ + fill use `correct: <int>` + `options[]`.
- Match uses `left[]` + `right[]` + `order[]` (NOT `correct[]` — Sport Studies + Astronomy both shipped broken with `correct` on match-type until remediation caught them).

## Flashcards (8-15)

- 10-14 typical. ≤15 words target, hard cap 30. One fact per card, no enumerations.
- Watch the single-word-answer trap: questions must start with "What is/Who was/When/Name" for one-word answers.

## Glossary

- ≥3 `<dfn class="term">` inline.
- ≥6 entries in `glossary_terms` array.

## hero_keywords

**REQUIRED** — array of 3 search strings, each ≥2 words. Engineering + Astronomy both shipped with empty `hero_keywords` until I caught it in remediation. Examples:
- For a Crusades lesson: `["medieval Crusades knights", "Jerusalem stone walls", "medieval warfare manuscript"]`
- For a Cold War lesson: `["Cold War Berlin Wall", "Cuban missile crisis archive", "1960s Soviet propaganda poster"]`

## Output checklist

- [ ] All required schema fields present
- [ ] 3 underscore-prefixed routing keys (`_lesson_number`, `_unit_slug`, `_lesson_slug`)
- [ ] hero_keywords is a 3-element array, no empty strings
- [ ] No `<h1>` in content_html, sequential `data-narration-id`
- [ ] ≥2 key-fact, ≥2 collapsible, ≥3 `<dfn class="term">`
- [ ] Exactly 6 practice_questions, exactly 5 knowledge_checks, 8-15 flashcards
- [ ] KC match uses `left/right/order`, KC MCQ+fill use `correct/options`
- [ ] No board names ("Eduqas", "WJEC", "Pearson"), no spec codes (C100QS), no component codes ("Component 1", "Option 1A")
- [ ] No HTML entities in description/practice/KC/flashcard/glossary
- [ ] Historical accuracy on every named year/person/place

## ABSOLUTE BANS

- **NO spec codes** (C100QS, C100UA-H, C100U1-8) in user-facing strings
- **NO board names** (Eduqas, WJEC, Pearson) in content/exam-tips/questions
- **NO component/option codes** ("Component 1", "Option 1A", "Studies in Depth") — refer to topics by name
- **NO Level descriptors in `marks`** — use StudyVault Mastering/Secure/Developing/Emerging
- **NO** "Nothing worthy of credit" / "Award N marks for identification"
- **NO HTML entities in plain-text fields**

## When done

```
LESSON_DONE: number=N slug={slug} words={count} questions=6 kcs=5 flashcards={n}
```

Final per batch:
```
BATCH_DONE: batch_id={batch_id} lessons={count}
```
