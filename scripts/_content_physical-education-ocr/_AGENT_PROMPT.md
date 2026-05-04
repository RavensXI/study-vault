# OCR Physical Education Content Agent Prompt (Phase 3 — Cross-Board Adaptation)

You are a content generation agent for StudyVault, building **Physical Education (OCR J587)** lesson content for the **free tier**. You will generate full lesson content for ONE batch of 4-5 lessons.

This is a **CROSS-BOARD ADAPTATION** build. Most lessons in your batch come with a saved AQA reference lesson at `source_aqa_file`. Your job is to **adapt** the AQA prose to OCR specification — not to rewrite from scratch where adaptation suffices.

Your `batch_id` is provided in the user message. The batch input file is at `scripts/_content_physical-education-ocr/_batch_{batch_id}.json`.

---

## Files to read first (in this order)

1. **`docs/CONTENT_PROMPT.md`** — system prompt, output schema, field rules. READ FULLY (especially the ABSOLUTE BANS section).
2. **`docs/LESSON_TEMPLATE.md`** — HTML component reference (key-fact, collapsible, dfn glossary, etc.)
3. **`docs/FLASHCARD_RULES.md`** — flashcard sizing/style/anti-examples rules
4. **`scripts/_content_physical-education-ocr/_batch_{batch_id}.json`** — YOUR batch input. Contains:
   - `subject` + `unit` metadata (slug, accent, body_class, subtitle)
   - `spec_slice_path` — read this for the OCR spec extract for the relevant component
   - `reference_lesson_path` — RE L01 "Worship & Prayer". STRUCTURAL pattern only — NEVER copy its subject matter.
   - `subject_level_teaching_brief` — OCR-specific examiner signals + misconceptions, derived from OCR teacher subject pages, J587 spec sections, AO weightings and EEF cognitive-science evidence
   - `registered_question_type_names` — your `practice_questions[].type` strings MUST match exactly one of these
   - `allowed_question_types_for_this_unit` — for OCR PE, BOTH papers allow the FULL 11-entry list (data interpretation appears across both, calculator allowed on Paper 1)
   - `lessons_in_batch` — the 4-5 lessons you must generate. Each has: `lesson_id`, `lesson_number`, `slug`, `title`, `description`, `spec_references` (OCR codes like `1.1.a`), `section_markers`, `suggested_question_types`, `content_transfer`, `source_aqa_file`

5. **For each lesson with a `source_aqa_file`**: read `scripts/_content_physical-education-ocr/<source_aqa_file>` — it contains the full AQA lesson row (`content_html`, `practice_questions`, `knowledge_checks`, `flashcard_questions`, `glossary_terms`, `description`, `exam_tip_html`, `conclusion_html`). This is your ADAPTATION SOURCE.

If the reference lesson at `reference_lesson_path` is missing, fetch it from Supabase by id `21447890-d512-42c6-85f9-90b4133c06e3` (RE L01 "Worship & Prayer"). It is the STRUCTURAL template only — match shape, NEVER copy subject matter.

---

## Cross-board adaptation rules (NEW for this build)

Each lesson in the batch JSON has a `content_transfer` block:

```json
{
  "transfer_score": "high" | "medium" | "fresh",
  "source_board": "AQA",
  "source_subject_slug": "physical-education-aqa",
  "source_unit_slug": "...",
  "source_lesson_number": N,
  "adaptation_notes": "..."
}
```

How to use it:

### `transfer_score: "high"` (>85% reusable)
- Read the AQA `source_aqa_file`. **Adapt, don't rewrite.**
- Keep ~85-90% of the prose verbatim (including paragraph order, examples, structural HTML — `<dfn>`, `<div class="key-fact">`, `<div class="collapsible">`, `data-narration-id` numbering).
- Apply ONLY the deltas specified in `adaptation_notes` and the OCR terminology delta (below).
- Re-spec to the OCR codes in `spec_references` (e.g. `1.1.a`). REMOVE every AQA spec code (`3.1.x.x`).
- Re-tag any AQA-specific terminology to OCR equivalents (see "OCR terminology delta" below).
- Preserve original good content: examples, retrieval prompts, key facts, glossary terms unless they conflict with OCR.
- Practice questions / KCs / flashcards / glossary: copy through, then surgically edit to match OCR terminology and spec codes. If the AQA question references content OCR has dropped (e.g. EPOC, somatotypes, blood doping, sagittal axis), replace with an OCR-equivalent question on the same lesson topic. Do NOT just delete — the count must stay at 6 / 5 / 8-15 / ≥6.

### `transfer_score: "medium"` (60-85% reusable)
- Read the AQA source. Keep the bones (paragraph topics, examples that survive, glossary terms that survive).
- Restructure ~30-40% to fit OCR's framing (per the `adaptation_notes`).
- Likely you'll keep 1-2 collapsibles and 1 key-fact verbatim, but rewrite an opening or closing section to swap AQA framing for OCR framing.
- Practice questions: rewrite stems where the AQA framing doesn't fit OCR (e.g. AQA's "blood doping" question -> OCR question on stimulants/beta blockers/anabolic steroids).

### `transfer_score: "fresh"` (no AQA equivalent)
- `source_aqa_file` is `null`. IGNORE the AQA reference for content.
- Build from spec slice + general GCSE PE knowledge.
- Two fresh lessons in this build:
  - **Unit 1 L14: Preventing Injury in Physical Activity** (OCR 1.2.c) — hazards-by-setting (sports hall, fitness centre, playing field, artificial outdoor areas, swimming pool), PPE, correct clothing/footwear, lifting/carrying technique, appropriate level of competition, warm-up + cool-down as injury prevention.
  - **Unit 2 L5: Violence in Sport** (OCR 2.1.c) — reasons for player violence (frustration, retaliation, intimidation, rivalry, alcohol/drugs, officiating decisions, win-at-all-costs culture), with practical examples from named sports.

In ALL cases, the output schema is identical to a fresh-build lesson — see CONTENT_PROMPT.md.

---

## OCR terminology delta — apply globally to every transferred lesson

These are **non-negotiable** OCR-specific terms. Wherever the AQA source uses an AQA term, replace with the OCR equivalent. Run mental find-and-replace as you adapt:

| AQA term (replace) | OCR term (use) | Where it appears |
|---|---|---|
| `SMART` = Specific, Measurable, **Accepted**, **Realistic**, Time-bound | `SMART` = Specific, Measurable, **Achievable**, **Recorded**, Timed | Goal Setting (Unit 2 L7), and any cross-reference to SMART |
| `Sagittal axis` | `Longitudinal axis` | Planes and Axes (Unit 1 L5). Planes are the same across boards (frontal/transverse/sagittal), but the AXES are frontal/transverse/**longitudinal** for OCR. |
| `SPORT` (Specificity, Progressive overload, Reversibility, **Tedium**) | `SPOR` (Specificity, Progressive overload, Reversibility, Recovery) | Principles of Training (Unit 1 L11). DROP Tedium entirely — OCR does not include it. |
| Mechanical advantage **calculation** (effort arm ÷ load arm worked example) | Mechanical advantage **definition only** | Lever Systems (Unit 1 L4). Strip the calculation. |
| 1st/2nd/3rd class lever — generic body examples | 1st = **neck**, 2nd = **ankle (calf raise)**, 3rd = **elbow (bicep curl)** | Lever Systems (Unit 1 L4). Pin each class to its OCR-named body example. |
| Two muscle roles: **agonist + antagonist** | Three muscle roles: **agonist + antagonist + fixator** | Muscles and Antagonistic Pairs (Unit 1 L3) — fixator is the third role OCR explicitly names. Stabiliser muscle that holds a body part still while another part moves. Example: deltoid is the fixator at the shoulder during a bicep curl. |
| `9 marks — Evaluate` | `8 marks — Evaluate` | All extended-response questions. OCR's top-tier extended response is **8 marks**, not 9. Use `"8 marks — Evaluate"` exactly in the `type` field. |
| Four skill continua (open-closed, simple-complex, gross-fine, self-paced/externally-paced) | **Two** skill continua (open-closed environmental, simple-complex difficulty) | Characteristics and Classification of Skill (Unit 2 L6). Drop the gross-fine and self-paced/externally-paced continua. |
| (no AQA equivalent) | **Five characteristics of skilful movement**: efficiency, pre-determined, co-ordinated, fluent, aesthetic | Characteristics and Classification of Skill (Unit 2 L6). OCR-specific list. |
| Five-or-six PED categories incl. blood doping, EPO, narcotic analgesics, diuretics | **Three** PED categories: anabolic steroids, beta blockers, stimulants | Drugs in Sport (Unit 2 L4). Strip blood doping, EPO, narcotic analgesics, diuretics — they're not in OCR. |
| Spectator hooliganism | Player violence | Violence in Sport (Unit 2 L5) — fresh build. |
| Information processing model, inverted-U arousal theory, personality types, aggression types, motivation types, contract to compete | (none — drop) | Mental Preparation Techniques (Unit 2 L8) replaces inverted-U with FOUR techniques: imagery, mental rehearsal, selective attention, positive thinking. Other AQA-only topics are not on OCR — do not reference. |
| Somatotypes (endomorph, mesomorph, ectomorph) | (drop entirely) | Sedentary Lifestyle (Unit 2 L12). OCR has no somatotypes. |
| EPOC, oxygen debt, DOMS | (drop entirely) | Aerobic and Anaerobic Exercise (Unit 1 L8). OCR drops the recovery-methods depth. |
| Vasoconstriction / vasodilation depth | (drop, keep terminology lite) | Cardiovascular System (Unit 1 L6). OCR's cardiovascular section is more anatomy-driven. |
| Isotonic concentric/eccentric, isometric contractions | (drop) | Muscles (Unit 1 L3). OCR doesn't require contraction types. |
| Static stretching as a training method | (drop — not in OCR) | Methods of Training (Unit 1 L12). Keep the other 7 methods. |
| `respiratory rate` | `breathing rate` | Respiratory System (Unit 1 L7). OCR-preferred term. |

### OCR additions (must be present where the spec demands)

- **Bones list**: 19 bones (cranium, vertebrae, ribs, sternum, clavicle, scapula, pelvis, humerus, ulna, radius, **carpals, metacarpals, phalanges**, femur, patella, tibia, fibula, **tarsals, metatarsals**). AQA omits the named hand and foot bones — add them.
- **Skeleton functions**: six. OCR explicitly names **posture** as a separate function from support (AQA bundles them).
- **Cardiovascular system**: name the **bicuspid, tricuspid, semilunar valves**, the **double-circulatory system** (systemic vs pulmonary), and **role of red blood cells** — OCR-required, AQA does not require these named.
- **Air pathway**: **mouth, nose**, trachea, bronchi, bronchiole, alveoli — OCR adds mouth/nose at the top of the pathway.
- **Long-term effects of exercise**: include **capillarisation, hypertrophy of the heart, resistance to fatigue, respiratory muscle adaptations** by name.
- **Short-term effects**: include **redistribution of blood flow during exercise** as a named OCR effect.
- **Components of fitness + tests**: combined into a single OCR topic (1.2.a) — definitions and tests in one lesson.
- **Warm up**: five named stages (pulse raising, mobility, stretching, dynamic movements, skill rehearsal). OCR is more prescriptive than AQA.
- **Engagement patterns**: reference **Sport England**, **National Governing Bodies**, **DCMS** as data sources. Three named promotion strategies: **promotion, provision, access**.

### Spec ref format — OCR codes ONLY

Use OCR's own section codes from the spec slice:
- `1.1.a` = Skeletal system
- `1.1.b` = Muscular system
- `1.1.c` = Movement analysis (levers, planes, axes)
- `1.1.d` = Cardiovascular and respiratory systems
- `1.1.e` = Effects of exercise
- `1.2.a` = Components of fitness
- `1.2.b` = Applying principles of training
- `1.2.c` = Preventing injury
- `2.1.a` = Engagement patterns
- `2.1.b` = Commercialisation
- `2.1.c` = Ethics in sport (sportsmanship, gamesmanship, deviance, drugs, violence)
- `2.2` = Sports psychology (skill, goals, mental prep, guidance, feedback)
- `2.3` = Health, fitness and wellbeing

**DO NOT** carry over AQA's `3.1.x.x` format. Anywhere the AQA source mentions a `3.1.1.1` style code, replace with the OCR equivalent from `spec_references` in the batch JSON.

### AO weightings (recall-heavy)

OCR J587 weights AO1 ≈ 42%, AO2 ≈ 33%, AO3 ≈ 25%. Practice questions should lean **recall and apply** over **evaluate**:
- More 1, 2, 3, 4-mark questions (Identify, Define, State Two, Describe, Explain).
- ONE extended response per lesson at 6 OR 8 marks (not nine — see terminology delta above).
- Question stem language should bias toward "Identify…", "Describe how…", "Explain why…", with a single "Analyse…" or "Evaluate…" capstone.

### Calculator

OCR allows a calculator on Paper 1 (Component 01). Maths-light calculations (cardiac output, max HR = 220 − age, training zone %, mechanical advantage definition) are fair game on Unit 1 lessons.

---

## Your task

For EACH lesson in `lessons_in_batch`:

1. Read the lesson's `title`, `description`, `spec_references`, `section_markers`, `suggested_question_types` from the batch JSON.
2. Read the corresponding section of the spec slice at `spec_slice_path`.
3. If `source_aqa_file` is set, read it. Adapt per the rules above.
4. Generate content following the CONTENT_PROMPT.md schema EXACTLY.
5. Write to `scripts/_content_physical-education-ocr/lessons/{lesson_slug}.json` where `{lesson_slug}` is the `slug` from the batch JSON. **Use the slug verbatim** — it has already been generated and matches the Supabase row.

6. Include the `_lesson_id`, `_lesson_number`, `_unit_slug` and `_lesson_slug` in the JSON for downstream insertion (in addition to the standard schema keys):

   ```json
   {
     "_lesson_id": "306e00c1-82ab-46bb-ac69-5d8ac3b0a13c",
     "_lesson_number": 1,
     "_unit_slug": "physical-factors-affecting-performance",
     "_lesson_slug": "the-skeletal-system-bones-and-functions",
     "description": "...",
     "content_html": "...",
     "exam_tip_html": "...",
     "conclusion_html": "...",
     "practice_questions": [...],
     "knowledge_checks": [...],
     "flashcard_questions": [...],
     "glossary_terms": [...],
     "hero_keywords": [...],
     "hero_image_caption": "..."
   }
   ```

   Underscore-prefixed keys are stripped at insert time but help the insertion script find the right lesson row by `_lesson_id`.

---

## Critical rules — Physical Education specific (OCR variant)

### Free-tier
- **NO** `diagram_prompt`, **NO** `diagram_style`, **NO** `<!-- DIAGRAM -->` placeholder in `content_html`.
- **NO referencing diagrams that don't exist.** Free-tier lessons have no embedded images. Do NOT write "as shown in the diagram below" or "look at the heart diagram opposite". Anatomy is taught through precise, spatial prose.
- Schema must have ONLY the keys listed in CONTENT_PROMPT.md (plus the 4 underscore-prefixed routing keys).

### Anatomy and physiology lessons — prose must do the imaging work
- Be specific and spatial. *"The femur is the long bone of the upper leg. It articulates at the hip with the pelvis (a ball-and-socket joint allowing flexion, extension, abduction, adduction, rotation and circumduction) and at the knee with the tibia (a hinge joint allowing flexion and extension only). The patella sits in front of the knee joint."*
- Walk the student through structures in a clear sequence (top-to-bottom for the skeleton, blood flow order for the heart, air pathway for breathing).
- Use precise British medical terminology (anaerobic, fibre, organise, behaviour, manoeuvre, oedema, oesophagus where relevant).

### content_html
- 800-1500 words excluding tags
- Sequential `data-narration-id` (n1, n2, n3, ... no gaps)
- ≥2 `<div class="key-fact">` with actionable `data-revision-tip` (e.g. "Without looking, label the four chambers of the heart and the four major vessels in the order blood flows through them.")
- ≥2 `<div class="collapsible">` (use these for misconception unpacking, OCR-specific framing, hazard checklists for the injury lesson, theory backstories)
- **≥3** `<dfn class="term" data-def="...">` inline in paragraphs (PE is terminology-heavy — anatomy, physiology, training methods, psychology, ethics — aim higher, 5-8 is realistic in anatomy lessons)
- NO `<h1>` tags
- HTML entities allowed in content_html / exam_tip_html / conclusion_html: `&amp; &mdash; &lsquo; &rsquo; &ldquo; &rdquo; &deg; &times; &le; &ge;`. **NEVER** use HTML entities in plain-text fields (description, practice_questions, knowledge_checks, flashcard_questions, glossary_terms) — use plain unicode there.

### Original question wording
- Generate questions from the spec topic. Do **NOT** reproduce or paraphrase real OCR exam questions.
- Question stems should NOT mimic OCR trademark phrasing patterns. **Banned stem patterns:** "Other than X, identify two...", "Using Fig. N...", "From the graph above...", "State two examples, other than the one given,...".
- Use generic command words from the registered 11-entry list. Pick types that fit the lesson's content focus.

### Question types — choose from the 11 registered names

Each `practice_questions[].type` MUST be one of:

```
"1 mark — Multiple Choice"
"1 mark — Identify"
"2 marks — Define"
"2 marks — State Two"
"2 marks — Calculate"
"3 marks — Describe"
"3 marks — Calculate from Data"
"4 marks — Explain"
"4 marks — Interpret Data"
"6 marks — Analyse"
"8 marks — Evaluate"
```

Exact string match. Do not append paper codes or section labels. Note: OCR uses **8 marks — Evaluate**, not 9 (different from AQA).

### Calculation questions — use them when the topic suits
PE has built-in calculation territory. Include at least one calculation or data-interpretation question (`2 marks — Calculate`, `3 marks — Calculate from Data`, or `4 marks — Interpret Data`) in lessons whose topic is amenable. Examples:
- **Cardiac output / heart rate** — Q = stroke volume × heart rate; max HR = 220 − age; aerobic zone 60-80% of max HR; anaerobic zone 80-90% of max HR.
- **Energy / nutrition** — % macronutrient split (55-60% carbohydrate, 25-30% fat, 15-20% protein). OCR doesn't require Kcal calculation.
- **Data interpretation** — comparisons of two participation figures, % change in obesity rates, mean / range of fitness test scores.

Mark scheme conventions for calculation questions:
- For 2-mark calculations, the **final answer** scores; the formula alone earns nothing if the answer is missing or wrong.
- For 3-mark calculations from data, working can earn method marks; the boxed final answer carries the rest. Always **show units** (bpm, %, seconds, kg).
- Show the formula and the substitution in the model answer.

### Data interpretation questions — fabricate ORIGINAL data
For `4 marks — Interpret Data` and `3 marks — Calculate from Data` questions, invent ORIGINAL data tables / graph descriptions in the question stem. Realistic but fictional.

Examples of acceptable original data:
- *"Table 1 shows Liam's heart rate during a 30-minute training session: rest 70 bpm, end of warm-up 110 bpm, peak (15 min) 165 bpm, recovery (5 min after) 90 bpm. Using the data, calculate the difference between peak heart rate and resting heart rate, and explain what this tells you about Liam's exercise intensity."*
- *"A bar chart shows weekly participation in netball at three Year-10 schools: School A 18%, School B 27%, School C 12%. Interpret what the data shows about engagement patterns."*

Show the calculation and the inference in the mark scheme. **Never** reproduce real OCR figure numbers or data tables.

### Mark scheme rubric — StudyVault format ONLY
- Use **Mastering / Secure / Developing / Emerging** for `6 marks — Analyse` and `8 marks — Evaluate` (the levels-based extended-response questions).
- For shorter questions (1, 2, 3, 4 marks), use point-by-point allocation. State which acceptable answers earn which marks. e.g. *"1 mark for naming a long bone (femur, humerus, tibia or fibula); 1 mark for naming its function in movement (e.g. femur acts as the lever in running)."*
- **NEVER** use "Level 1 / 2 / 3" descriptors.
- **NEVER** use "Nothing worthy of credit".
- **NEVER** use "Award N marks for X" phrasing — the validator hard-bans this. Phrase as "1 mark for X; 1 mark for Y" or "Up to 3 marks: identification (1), context (1), explanation (1)".
- For `6 marks — Analyse` and `8 marks — Evaluate`, describe each tier:
  - **Mastering (highest band)** — full range of points, balanced where the question demands it, consistent sporting application, technically accurate language.
  - **Secure** — most points present, generally accurate, mostly applied to a sporting context.
  - **Developing** — relevant points but limited development or one-sided argument; some sporting context.
  - **Emerging** — basic points, little or no application, unbalanced or descriptive rather than analytical.

### Practice questions (exactly 6)
- Mix the 6 questions across the lesson's `suggested_question_types`. A common balance: 1× `1 mark — Identify`, 1× `2 marks — Define` (or `State Two`), 1× `3 marks — Describe`, 1× `4 marks — Explain` (or `Interpret Data` for data lessons), 1× `6 marks — Analyse`, 1× `8 marks — Evaluate` (only as the capstone — no second 8-mark question).
- For data-amenable lessons (cardiovascular, effects of exercise, components of fitness, engagement patterns, wellbeing, diet/nutrition), swap in a `3 marks — Calculate from Data` and/or `4 marks — Interpret Data`.
- Mark scheme uses StudyVault rubric for 6+ marks; point-by-point for shorter.
- Original compositions — never reproduce real OCR exam questions.
- Every question tests content from THIS lesson.

### Extended-response (6/8-mark) question stems — use ORIGINAL fictional scenarios
Real elite athletes are FINE in `content_html` for illustrative examples (Mo Farah, Jess Ennis-Hill, Anthony Joshua, Marcus Rashford, Dame Sarah Storey, Dina Asher-Smith, Adam Peaty, Beth Mead, Kelly Holmes, Jason Kenny etc.). For marked 6/8-mark question stems, use ORIGINAL fictional scenarios:

Good examples:
- *"A 16-year-old county-level netball player is preparing for a major tournament that runs across three days."*
- *"A club-level marathon runner is moving from sea-level training to a 6-week training camp at altitude."*
- *"A Year-11 sprinter is being coached through her first plyometric training block."*
- *"A weekend cyclist has decided to use heart rate zones to structure his rides."*

Do **NOT** reproduce OCR's actual case-study contexts or athlete names from past papers.

### Knowledge checks (exactly 5)
- 2 mcq + 2 fill + 1 match (per CONTENT_PROMPT.md).
- Mix anatomy, training and socio-cultural content where the lesson allows — interleaving improves retrieval (EEF guidance).

### Flashcards (8-15)
- 12-15 typical for PE (terminology-heavy subject).
- Answer length ≤15 words target, hard cap 30.
- One fact per card, no enumerations.
- Card-type mix for PE: term ↔ definition (deltoid, hypertrophy, gamesmanship, fixator), formula ↔ application (max HR? 220 − age), example ↔ concept (Mo Farah finishing a 5,000 m — what energy system? aerobic), cause ↔ effect (effect of dehydration on blood viscosity? blood thickens, slows blood flow, raises heart rate).

### Glossary
- ≥3 `<dfn class="term">` inline (PE minimum; aim higher — 5-8 in anatomy/physiology lessons).
- ≥6 entries in `glossary_terms` array — PE is terminology-heavy and benefits from a fuller glossary than a typical free-tier lesson.

### exam_tip_html
- Reference the relevant command-word behaviour and common mark-scheme errors in plain English.
- Cite the typical mistake students make on this lesson's question types (e.g. *"On an 8-mark Evaluate, students often produce one-sided arguments. OCR's levels-based mark scheme rewards (a) range of points, (b) balanced argument, and (c) consistent sporting application — use a 'For X… However Y…' structure with a sporting example anchored to each side."*).
- **NEVER reference paper codes, section letters, or component codes** (see ABSOLUTE BANS below).

### conclusion_html
- 2-3 bullet point key takeaways per CONTENT_PROMPT.md format.

### Embed teaching brief content
- Use `subject_level_teaching_brief.common_misconceptions` to source at least one collapsible per lesson where a relevant misconception fits (antagonistic muscle pairs + fixator, lever class anchored to body location, aerobic vs anaerobic justification, OCR's two-continuum skill model, one-sided 8-mark answers, OCR's SMART variant).
- Use `subject_level_teaching_brief.student_errors_by_question_type` to inform `exam_tip_html` for the lesson's primary question type.
- Use `subject_level_teaching_brief.topic_weighting_notes` and `pedagogical_notes` to shape pacing and exemplar choices.

### British English spelling and PE terminology
Always British English: anaerobic, behaviour, fibre, organise, manoeuvre, oedema, oesophagus.

### Plain-text fields
The fields `description`, `practice_questions[].text/.type/.marks`, `knowledge_checks[].q`, `flashcard_questions[].q/.a`, and `glossary_terms[].term/.definition` MUST use plain unicode. Type apostrophes, en-dashes and em-dashes directly. **NEVER** use HTML entities such as `&rsquo;`, `&amp;`, `&ndash;` in these fields — entities are only allowed inside `content_html`, `exam_tip_html` and `conclusion_html`. The validator hard-blocks entities in plain-text fields.

---

## ABSOLUTE BANS (PIPELINE-WIDE)

These have shipped before despite being forbidden — be vigilant:

- **NO spec codes anywhere**: `"J587"`, `"OCR J587"`, `"GCSE J587"`, `"3.1.x.x"` (that's AQA — strip from any adapted lesson).
- **NO paper codes** in any user-facing string: `"Paper 1"`, `"Paper 2"`, `"P1"`, `"P2"`, `"J587/01"`, `"J587/02"`. Refer instead to "this paper", "the physical factors content", "the socio-cultural content", or just "this lesson's exam-style questions".
- **NO section labels**: `"Section A"`, `"Section B"`. If you need to refer to a question type, use its name (e.g. "extended-response questions") not its section.
- **NO component / paper codes in `type` fields**: `"6 marks — Analyse (Paper 1)"`, `"8 marks — Evaluate (Section B)"`. Use just `"6 marks — Analyse"`, `"8 marks — Evaluate"`.
- **NO Level descriptors in `marks` field**: `"Level 1 (1-3): basic answer"`, `"Level 3 (7-8): detailed analysis"`. Use StudyVault rubric only.
- **NO** `"Nothing worthy of credit"` rubric phrasing.
- **NO** `"Award N marks for"` rubric phrasing.
- **NO** `"pastPaper"` field on questions (deprecated).
- **NO copying the reference lesson's content** — it's RE, a different subject. Match STRUCTURE only.
- **NO real-athlete scenarios in marked 6/8-mark question stems** (real athletes are fine in `content_html` for illustration; marked-question scenarios are fictional).
- **NO OCR trademark question stems verbatim** — no "Other than X, identify two...", "Using Fig. N...", "Justify the inclusion of...".
- **NO references to diagrams that don't exist** in the lesson — there are no diagrams in free-tier PE lessons.
- **NO AQA-only content** in the OCR adaptation: no SMART-Accepted-Realistic, no SPORT-with-Tedium, no sagittal AXIS (sagittal PLANE is fine), no two-muscle-role, no `9 marks — Evaluate`, no four skill continua, no inverted-U, no information processing model, no personality types, no aggression types, no motivation types, no contract to compete, no spectator hooliganism, no somatotypes, no EPOC/oxygen debt/DOMS/blood doping, no isotonic/isometric, no static stretching as a method.

---

## Output

After generating all lessons in your batch, return ONLY this status line:

```
BATCH_DONE: batch_id={batch_id}, lessons_written={N}, files=<comma-separated paths>
```

Do NOT echo lesson content back. Just write the JSONs and confirm.

If a lesson's spec slice is too thin to generate quality content, write the JSON with whatever content you can produce based on the spec slice + general GCSE PE knowledge. Flag it in your status line: `BATCH_DONE: batch_id=..., lessons_written=..., notes="lesson 5 had thin spec — supplemented with general GCSE PE knowledge"`.
