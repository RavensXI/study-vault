# Health & Social Care Content Agent Prompt (Phase 3)

You are generating content for **Health and Social Care** — a Level 1/Level 2 vocational award covering growth/development across the lifespan, self-concept, measuring health, and promoting well-being. This is a dual-board build (Eduqas/WJEC 5249QA share the same spec); a single Supabase row serves both boards via slugMap aliasing.

**Critical per memory rule (feedback_eduqas_wjec_neutral_phrasing):** NEVER use "Eduqas" or "WJEC" by name in any user-facing prose. Refer neutrally to "this Level 1/2 qualification", "the exam unit", "the spec", or "Health & Social Care."

Mixed transfer pattern: most lessons port partially from `health-social-care-ocr` or `health-social-care-edexcel` (free-tier sibling rows). Where a `port_source_path` is set, read the source lesson and adapt the prose, scenarios, and structure — never replicate verbatim. Where no port source, generate fresh from spec.

---

## Files to read first (in this order)

1. **`docs/CONTENT_PROMPT.md`** — system prompt, output schema, field rules.
2. **`docs/LESSON_TEMPLATE.md`** — HTML component reference.
3. **`docs/FLASHCARD_RULES.md`** — flashcard rules.
4. **`scripts/_content_health-social-care-eduqas/_batch_{batch_id}.json`** — YOUR batch input.
5. **For each lesson with a `port_source_path`:** read it. Contains `_export_meta` (target/source mapping + adaptation_notes) and `source_lesson` (full Supabase row to adapt from).
6. **`scripts/_content_business-edexcel/_reference_lesson.json`** — structural shape only.

---

## Subject framing — HSC L1/L2 specific

### Audience
- **Vocational L1/L2** — accessible at L1, stretch at L2. Care-sector language, concrete settings: residential care home, GP surgery, after-school club, mental health support service, hospital ward, foster placement, day centre, hospice, GP practice. Not academic theorising.
- The exam paper is Unit 1 (40% of the qualification). Unit 2 is NEA portfolio (out of scope here).

### Topic structure
Your 13 lessons span 2 units:
- **Unit 1: Growth, Development & Influences Across the Lifespan** (L1-L7) — 5 life stages, PIES (Physical/Intellectual/Emotional/Social) development, life factors (genetic / biological / environmental / social / economic / lifestyle), lifestyle choices, life events (expected vs unexpected), and formal/informal support when developmental milestones aren't reached.
- **Unit 2: Self-Concept, Measuring Health & Promoting Well-being** (L1-L6) — active participation, inclusion, resilience, self-concept formation, defining health/illness/disease/well-being, physical indicators of health (pulse rate, blood pressure, BMI, peak flow, temperature), promoting health and well-being, named campaigns (Change4Life, This Girl Can, Stoptober, NHS Couch to 5K, etc.).

### Named theorists / frameworks to use precisely
- **Piaget** — 4 cognitive development stages: sensorimotor, pre-operational, concrete operational, formal operational. Don't oversimplify.
- **Kohlberg** — moral development stages (pre-conventional, conventional, post-conventional). Note the spec may not require depth here — check `adaptation_notes`.
- **Bowlby** — attachment theory: monotropy + critical period (0-3 years). The 44 Thieves study is the classic citation.
- **Ainsworth** — Strange Situation, attachment types: secure, insecure-avoidant, insecure-resistant.
- **Erikson** — psychosocial stages (8 stages across the lifespan). Identity vs role confusion in adolescence is the most exam-relevant one.
- **Bandura** — social learning theory (modelling, observation, vicarious reinforcement).
- **Marmot Review (2010)** — health inequalities, social determinants of health. UK-specific, high exam value.

### UK care-sector terminology (use these exact terms)
- **PIES** development (Physical / Intellectual / Emotional / Social)
- **Life stages**: infancy (0-2), early childhood (3-8), adolescence (9-18), early adulthood (19-45), middle adulthood (46-65), later adulthood (65+) — check the spec for exact age bands; some boards differ
- **Person-centred care**, dignity, respect, choice, independence, privacy, confidentiality, safeguarding
- **Life factors**: genetic, biological, environmental, social, economic, cultural, lifestyle
- **Health indicators**: pulse rate (60-100 bpm resting), blood pressure (120/80 mmHg ideal), BMI (categories: underweight <18.5, healthy 18.5-24.9, overweight 25-29.9, obese ≥30), peak flow (varies by age/height/sex), temperature (36.1-37.2°C)
- **NHS Constitution** (2009, refreshed) values: respect, compassion, working together for patients
- **Care Quality Commission (CQC)** — England's care regulator. Note that in Wales the equivalent is **Care Inspectorate Wales (CIW)** and in Scotland it's the **Care Inspectorate**. Use "the care regulator" when speaking generally; name specific regulators only when geographically grounded.

### Named UK health campaigns (post-2015 still-current)
- Change4Life (now Better Health) — childhood obesity / family activity
- This Girl Can (Sport England) — women's physical activity
- Stoptober — smoking cessation, annual October
- NHS Couch to 5K — walking-to-running app
- Dry January (Alcohol Change UK)
- 5 A Day (fruit/veg)
- Catch It, Bin It, Kill It (respiratory hygiene)

---

## Free-tier (mandatory)

- **NO** `diagram_prompt`, **NO** `diagram_style`, **NO** `<!-- DIAGRAM -->` placeholder.
- Schema must have ONLY keys listed in CONTENT_PROMPT.md plus the 3 underscore-prefixed routing keys.

## content_html

- 800-1500 words excluding tags.
- Sequential `data-narration-id` (n1, n2, n3 — no gaps).
- ≥2 `<div class="key-fact">` with actionable `data-revision-tip`.
- ≥2 `<div class="collapsible">`.
- **≥3** `<dfn class="term" data-def="...">` inline.
- NO `<h1>` tags.
- HTML entities in content_html / exam_tip_html / conclusion_html: `&amp; &mdash; &lsquo; &rsquo; &ldquo; &rdquo; &pound;`
- **Plain text in `description`, `practice_questions`, `knowledge_checks`, `flashcard_questions`, `glossary_terms`** — unicode quotes/dashes, NOT HTML entities.

## Adapt from source (NOT replicate)

For lessons with a `port_source_path`:
- **Rephrase the prose** — never leave whole paragraphs verbatim from the source.
- **Replace scenarios** — invent fresh service-user case studies with new names.
- **Replace numerical examples** — change figures, ages, lengths of stay so worked content is distinct.
- **Restructure** to match this spec's LO ordering — don't copy the source's section order.

For fresh-generation lessons (no `port_source_path`): generate from spec only via `adaptation_notes` + `section_markers`.

## Question types

Use only types listed in `registered_question_type_names`. Typical mix per lesson (6 questions): 1-2 recall (1-3 marks), 2-3 applied (3-4 marks), 1-2 extended (6-10 marks). Calculation questions only where natural (e.g. BMI calculation in the indicators-of-health lesson).

## Extended-response case-study scenarios

- **6+ mark questions MUST include a short ORIGINAL service-user case-study scenario** — 2-4 sentences setting up a fictional service user in a fictional care setting. Name + age + setting + one relevant detail.
- **Original fictional names**: e.g. *Aaliyah Idris (76, hospice patient with motor neurone disease)*, *Bryn Roberts (4, attending nursery)*, *Mr Caleb Owen (52, recently diagnosed Type 2 diabetes)*, *Iona Stewart (16, residential care leaver entering independent living)*, *Pat Quirke (66, Stage 1 dementia diagnosis)*. Vary names across lessons.
- **Real services** (NHS, CQC, Marie Curie, Samaritans, MIND, Macmillan) MAY appear inside `content_html` as illustrative examples — but NEVER inside a marked-question case-study stem. Marked-question scenarios are always fictional people.

## Mark scheme rubric

- StudyVault format ONLY: **Mastering / Secure / Developing / Emerging** for 6+ mark questions.
- **NEVER** "Level 1/2/3" descriptors. NEVER "Nothing worthy of credit". NEVER "Award N marks for identification".
- Short-answer (1, 2, 3 marks): content-led list, no rubric tier.

## Knowledge checks (exactly 5)

- 2 MCQ + 2 fill + 1 match per `docs/CONTENT_PROMPT.md`.
- **CRITICAL:** Use `correct: <int>` + `options[]` schema (NOT `answers: [...]`).

## Flashcards (8-15 per FLASHCARD_RULES.md)

- 10-14 typical. Answer ≤15 words target, hard cap 30. **One fact per card, no enumerations.**
- Watch out for the single-word-answer trap: questions starting with "What is/Who was/When/Name" can have one-word answers; statements ("X requires Y" → just one word) fail validation.

## Glossary

- ≥3 `<dfn class="term">` inline.
- ≥6 entries in `glossary_terms` array.

## exam_tip_html

- Reference the relevant command word + common errors.
- L1/L2 audience: concrete tips, not abstract.
- **NEVER reference spec codes (5249QA), unit numbers (Unit 1/Unit 2), or board names ("Eduqas", "WJEC").**

## conclusion_html

- 2-3 bullet point key takeaways.

---

## ABSOLUTE BANS (PIPELINE-WIDE)

- **NO board names**: "Eduqas", "WJEC", "Pearson", "OCR" in user-facing prose anywhere (content, exam tips, questions, flashcards, glossary).
- **NO spec codes**: `5249QA`, `5099QA`, any other spec code in user-facing strings.
- **NO unit codes**: `Unit 1`, `Unit 2`, `U1`, `U2` in user-facing strings. Refer to "this exam unit" or "the externally-assessed unit" if needed.
- **NO paper labels**: `Section A`, `Section B`.
- **NO Level descriptors in `marks`**.
- **NO** "Nothing worthy of credit" / "Award N marks for identification".
- **NO real service-user names** in marked-question case-study stems.
- **NO recycled fictional names** within your batch.
- **NO HTML entities in plain-text fields**.
- **NO** copying source lesson content verbatim — port = rephrase + restructure + replace examples.

---

## Output checklist (run before writing each file)

- [ ] All required schema fields present.
- [ ] All 3 underscore-prefixed routing keys present (`_lesson_number`, `_unit_slug`, `_lesson_slug`).
- [ ] No `<h1>` in content_html.
- [ ] Sequential `data-narration-id` (no gaps).
- [ ] ≥2 key-fact, ≥2 collapsible, ≥3 `<dfn class="term">`.
- [ ] Exactly 6 practice_questions, exactly 5 knowledge_checks, 8-15 flashcards.
- [ ] knowledge_checks use `correct: <int>` + `options[]` (not `answers`).
- [ ] No board names, spec codes, unit numbers anywhere in user-facing content.
- [ ] No HTML entities in plain-text fields.
- [ ] Fresh fictional case-study names per lesson.
- [ ] Source-adapted lessons rephrased + restructured + new examples (not verbatim).

## When done

```
LESSON_DONE: number=N slug={slug} words={count} questions=6 kcs=5 flashcards={n}
```

Final:

```
BATCH_DONE: batch_id={batch_id} lessons={count}
```
