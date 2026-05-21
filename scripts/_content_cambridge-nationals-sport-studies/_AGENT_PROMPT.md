# Sport Studies Content Agent Prompt (Phase 3)

You are generating content for **Cambridge National Sport Studies (OCR J829)** — a vocational Level 1/Level 2 qualification. The exam unit is R184 *Contemporary Issues in Sport*. NEA units R185–R187 are out of scope.

This subject is LOW transfer — most lessons are generated **fresh from spec**. There is no `port_source_path` because the related GCSE PE content doesn't share lesson-level structure with R184. You work from `adaptation_notes` + `spec_references` + `section_markers` in your batch input.

---

## Files to read first (in this order)

1. **`docs/CONTENT_PROMPT.md`** — system prompt, output schema, field rules. READ FULLY (especially ABSOLUTE BANS).
2. **`docs/LESSON_TEMPLATE.md`** — HTML component reference.
3. **`docs/FLASHCARD_RULES.md`** — flashcard sizing/style rules.
4. **`scripts/_content_cambridge-nationals-sport-studies/_batch_{batch_id}.json`** — YOUR batch input.
5. **`scripts/_content_business-edexcel/_reference_lesson.json`** — structural shape only. Match the shape, NEVER copy subject matter.

---

## Your task

For EACH lesson in `lessons_in_batch`:

1. Read the lesson's `title`, `description`, `spec_references`, `section_markers`, `adaptation_notes`.
2. Generate full content following `docs/CONTENT_PROMPT.md` schema EXACTLY.
3. Apply the per-lesson `adaptation_notes` literally — they tell you what R184 wants explicitly and what to exclude.
4. Write to `scripts/_content_cambridge-nationals-sport-studies/lessons/{lesson_slug}.json`. Slugify rule:

   ```python
   import re
   def slugify(s):
       s = s.lower().strip()
       s = re.sub(r"[^\w\s-]", "", s)
       s = re.sub(r"[\s_]+", "-", s)
       s = re.sub(r"-+", "-", s).strip("-")
       return s[:80]
   ```

5. Include routing keys:

   ```json
   {
     "_lesson_number": 1,
     "_unit_slug": "contemporary-issues-in-sport",
     "_lesson_slug": "...",
     "description": "...",
     "content_html": "...",
     ...
   }
   ```

---

## Subject framing — Sport Studies (R184) specific

### Audience
- **Vocational L1/L2** — accessible at L1 (clear, concrete, less abstract clause stacking than a GCSE PE textbook), with L2 stretch in extended responses.
- Content is **socio-cultural and contemporary**, NOT physiology. Sport Studies overlaps thematically with PE socio-cultural units but R184 is broader and more current. Don't slip into anatomy / training principles / energy systems — those are PE, not R184.

### R184 topic structure
Your 10 lessons cover R184's five Topic Areas:
- **TA1 User groups + barriers** (L1 user groups, L2 barriers)
- **TA2 Popularity, emerging sports, values** (L3 popularity + emerging, L4 values, L5 Olympic movement)
- **TA3 Etiquette + sportsmanship** (L6 etiquette, sportsmanship, spectator behaviour)
- **TA4 PEDs + WADA** (L7 drugs, sanctions, banned substance categories)
- **TA5 Hosting major events + NGBs + technology** (L8 hosting pre-event, L9 hosting during/legacy, L10 NGBs + technology)

### R184 question structure
- Section A: 30 marks — short-answer recall (1, 2, 3 marks)
- Section B: 28 marks — applied / explain / analyse (3–6 marks) tied to source materials
- Section C: 12 marks — extended response, evaluation or discussion (8 marks banded)
- **OCR examiner concern #1**: "answers not applied" — extended responses must contextualise specific scenarios.

### Vocabulary precision (R184 uses these specific terms)
- **User groups**: ethnic minorities; retired/over 50s; families with children; teenagers; people with disabilities; single parents; carers; full-time workers; unemployed.
- **Barriers**: time, family commitments, cost, lack of facilities, lack of role models, lack of disposable income, fashion, low self-esteem, perceived risk, stereotyping, religion/culture, restricted access.
- **Solutions to barriers** ARE assessable.
- **Values**: team spirit, fair play, citizenship, tolerance, respect, etiquette, national pride, excellence — name these as discrete spec values, not vague.
- **PEDs categories**: anabolic agents, peptide hormones, beta blockers, stimulants, diuretics, narcotics, cannabinoids, glucocorticoids, alcohol. UKAD enforces the WADA Prohibited List in the UK.
- **WADA "Whereabouts" rule**: elite athletes must declare their location for 1 hour every day for unannounced testing. Three missed tests in 12 months = ban.
- **Sanctions**: warnings → fines → bans (length depends on substance) → criminal prosecution for trafficking.
- **NGB examples**: The FA (football), RFU (rugby union), ECB (cricket), LTA (tennis), England Athletics, British Cycling.

### Currency — bake in a refresh-cycle warning
R184 content goes stale fast (Olympics every 4 years, doping cases, technology). Use **examples from the last 5 years** where possible:
- Paris 2024 Summer Olympics (most recent)
- Beijing 2022 Winter Olympics
- Russian doping scandals (Sotchi 2014, ban from Tokyo 2020 as "ROC", Paris 2024 as "AIN")
- Padel + pickleball as emerging sports
- VAR in Premier League (introduced 2019-20)
- Hawk-Eye, GoalLine technology

---

## Free-tier (mandatory)

- **NO** `diagram_prompt`, **NO** `diagram_style`, **NO** `<!-- DIAGRAM -->` placeholder.
- Schema must have ONLY keys listed in CONTENT_PROMPT.md plus the 3 underscore-prefixed routing keys.

## content_html

- 800–1500 words excluding tags.
- Sequential `data-narration-id` (n1, n2, n3 — no gaps).
- ≥2 `<div class="key-fact">` with actionable `data-revision-tip`.
- ≥2 `<div class="collapsible">`.
- **≥3** `<dfn class="term" data-def="...">` inline.
- NO `<h1>` tags.
- HTML entities in content_html / exam_tip_html / conclusion_html: `&amp; &mdash; &lsquo; &rsquo; &ldquo; &rdquo; &pound;`
- **Plain text in `description`, `practice_questions`, `knowledge_checks`, `flashcard_questions`, `glossary_terms`** — unicode quotes/dashes, NOT HTML entities (validator blocks entities in these fields).

## Question types

Use only types listed in `registered_question_type_names`. The 13 OCR-style types:
- `1 mark — Multiple Choice`, `1 mark — Identify`, `1 mark — State`
- `2 marks — Describe`, `2 marks — Outline`
- `3 marks — Explain`, `3 marks — Calculate` (rare — only if a lesson has a quantitative element)
- `4 marks — Explain`
- `6 marks — Analyse`, `6 marks — Justify`, `6 marks — Discuss`
- `8 marks — Evaluate` (R184's extended-response format)

Per-lesson balance (exactly 6 questions): mix recall (1–3 marks) + applied (3–4 marks) + at least one 6-mark or 8-mark extended. Bring the 8-mark Evaluate in for L4 (Values), L7 (PEDs), L9 (Legacy), L10 (NGBs/Tech) — those map to the spec's evaluative pivots.

## Extended-response case-study scenarios

- **6+ mark questions MUST include a short ORIGINAL case-study scenario** — 2–4 sentences setting up a fictional UK sports context: named small/regional sports club, an athlete, a town, one or two relevant figures. **NEVER use real national governing bodies, athletes, or clubs in marked-question stems** — they go in `content_html` for illustration only.
- Original fictional names: e.g. *Kingsmere Athletics Club* (small club in Norwich), *Aoife O'Donnell* (junior swimmer in Belfast), *Hilltop Rugby Union* (community club in Stockport), *Crescent FC* (women's grassroots football, Bristol).
- Vary names across lessons.

## Mark scheme rubric

- StudyVault format ONLY: **Mastering / Secure / Developing / Emerging** for 6+ mark questions.
- **NEVER** "Level 1/2/3" descriptors. NEVER "Nothing worthy of credit". NEVER "Award N marks for identification".
- Short-answer (1, 2, 3 marks): content-led list, no rubric tier.

## Knowledge checks (exactly 5)

- 2 MCQ + 2 fill + 1 match per `docs/CONTENT_PROMPT.md`.
- **CRITICAL:** Use `correct: <int>` + `options[]` schema (NOT `answers: [...]`).

## Flashcards (8–15 per FLASHCARD_RULES.md)

- 10–14 typical. Answer ≤15 words target, hard cap 30. **One fact per card, no enumerations.**
- Card-type mix: term ↔ definition, cause ↔ effect, example ↔ concept, fact ↔ application.

## Glossary

- ≥3 `<dfn class="term">` inline.
- ≥6 entries in `glossary_terms` array.

## exam_tip_html

- Reference the relevant command word + common errors.
- For L1/L2 audience, tips should be concrete.
- **NEVER reference spec codes (R184, R185, etc.) or section letters or "OCR" by name** (see ABSOLUTE BANS).
- Cite "answers not applied" for any lesson whose primary question type is extended-response.

## conclusion_html

- 2–3 bullet point key takeaways.

## Embed teaching brief content

- Use `subject_level_teaching_brief.common_misconceptions` to source at least one collapsible per lesson where a relevant misconception fits.
- Use `subject_level_teaching_brief.student_errors_by_question_type` for exam_tip_html on lessons with extended-response questions.

---

## ABSOLUTE BANS (PIPELINE-WIDE)

- **NO spec codes**: `J829`, `R184`, `R185`, `R186`, `R187`.
- **NO topic-area codes**: `TA1`, `TA2`, `Topic Area 1.1`. Refer to topics by name.
- **NO board names**: `OCR`, `Pearson`, `Cambridge Nationals` in content_html / exam_tip_html / conclusion_html / question stems / mark schemes / glossary / flashcards.
- **NO paper codes**: `Paper 1`, `P1`, `Section A`, `Section B`, `Section C`.
- **NO component codes in `type` fields**: just `"6 marks — Analyse"`, not `"6 marks — Analyse (R184)"`.
- **NO Level descriptors in `marks`**: use StudyVault rubric.
- **NO** "Nothing worthy of credit" / "Award N marks for identification".
- **NO real-business/real-athlete/real-NGB case-study scenarios** in marked-question stems.
- **NO recycled fictional names** within your batch.
- **NO HTML entities in plain-text fields** (`description`, `practice_questions`, `knowledge_checks`, `flashcard_questions`, `glossary_terms`).

---

## Output checklist (run before writing each file)

- [ ] All required schema fields present.
- [ ] All 3 underscore-prefixed routing keys present.
- [ ] No `<h1>` in content_html.
- [ ] Sequential `data-narration-id` (no gaps).
- [ ] ≥2 key-fact, ≥2 collapsible, ≥3 `<dfn class="term">`.
- [ ] Exactly 6 practice_questions, exactly 5 knowledge_checks, 8–15 flashcards.
- [ ] `practice_questions[].type` strings in `allowed_question_types_for_this_unit`.
- [ ] knowledge_checks use `correct: <int>` + `options[]` (not `answers`).
- [ ] No spec codes / paper codes / board names.
- [ ] No HTML entities in plain-text fields.
- [ ] Fresh fictional case-study names per lesson.

## When done

Per lesson:
```
LESSON_DONE: number=N slug={slug} words={count} questions=6 kcs=5 flashcards={n}
```

Final:
```
BATCH_DONE: batch_id={batch_id} lessons={count}
```
