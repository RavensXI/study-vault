# Edexcel Physical Education (1PE0) Content Agent Prompt (Phase 3)

You are a content generation agent for StudyVault, building **Physical Education (Edexcel 1PE0)** lesson content for the **free tier**. You will generate full lesson content for ONE batch of 2-4 lessons.

Your `batch_id` is provided in the user message. The batch input file is at `scripts/_content_physical-education-edexcel/_batch_{batch_id}.json`.

---

## Files to read first (in this order)

1. **`docs/CONTENT_PROMPT.md`** — system prompt, output schema, field rules. READ FULLY (especially the ABSOLUTE BANS section).
2. **`docs/LESSON_TEMPLATE.md`** — HTML component reference (key-fact, collapsible, dfn glossary, etc.)
3. **`docs/FLASHCARD_RULES.md`** — flashcard sizing/style/anti-examples rules
4. **`scripts/_content_physical-education-edexcel/_batch_{batch_id}.json`** — YOUR batch input. Contains:
   - `subject` + `unit` metadata (slug, accent, body_class, subtitle)
   - `spec_slice_path` — read this for the spec extract for the relevant paper
   - `reference_lesson_path` — read this for STRUCTURAL pattern (RE Worship & Prayer; do NOT copy its subject matter, just its shape)
   - `subject_level_teaching_brief` — subject-wide examiner signals + misconceptions, derived from Pearson Edexcel teacher support, Edexcel examiner reports and EEF cognitive-science evidence
   - `unit_level_teaching_brief` — currently empty `{}` (no unit-level breakdown in Phase 1; rely on the subject brief)
   - `registered_question_type_names` — your `practice_questions[].type` strings MUST match exactly one of these
   - `allowed_question_types_for_this_unit` — for PE, BOTH papers allow the FULL 11-entry list (calculations and data interpretation appear on both papers)
   - `lessons_in_batch` — the 2-4 lessons you must generate. Each has: `number`, `title`, `description`, `slug`, `spec_references`, `suggested_question_types`

If the reference lesson at `reference_lesson_path` is missing, fetch it from Supabase by id `21447890-d512-42c6-85f9-90b4133c06e3` (RE L01 "Worship & Prayer"). It is the STRUCTURAL template only — match shape, NEVER copy subject matter.

---

## Your task

For EACH lesson in `lessons_in_batch`:

1. Read the lesson's `title`, `description`, `spec_references`, `suggested_question_types` from the batch JSON.
2. Read the corresponding section of the spec slice at `spec_slice_path`.
3. Generate content following the CONTENT_PROMPT.md schema EXACTLY.
4. Write to `scripts/_content_physical-education-edexcel/lessons/{lesson_slug}.json` where `{lesson_slug}` is the lesson's slug. **Use this exact slugify rule** (matches the activation script):

   ```python
   import re
   def slugify(s):
       s = s.lower().strip()
       s = re.sub(r"[‘’′]", "", s)              # smart quotes
       s = re.sub(r"[–—]", "-", s)               # en/em dashes
       s = re.sub(r"[^\w\s-]", "", s)
       s = re.sub(r"[\s_]+", "-", s)
       s = re.sub(r"-+", "-", s).strip("-")
       return s[:80]
   ```

   So *"The Cardiovascular System and Exercise"* → `the-cardiovascular-system-and-exercise`. The slug is already provided in the batch JSON — use that string verbatim, do not re-slugify.

5. Include the `_lesson_number`, `_unit_slug` and `_lesson_slug` in the JSON for downstream insertion (in addition to the standard schema keys):

   ```json
   {
     "_lesson_number": 1,
     "_unit_slug": "human-body-and-movement",
     "_lesson_slug": "the-skeleton-structure-and-functions",
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

   Underscore-prefixed keys are stripped at insert time but help the insertion script find the right lesson row.

---

## Critical rules — Physical Education specific

### Free-tier
- **NO** `diagram_prompt`, **NO** `diagram_style`, **NO** `<!-- DIAGRAM -->` placeholder in `content_html`.
- **NO referencing diagrams that don't exist.** Free-tier lessons have no embedded images. Do NOT write "as shown in the diagram below" or "look at the heart diagram opposite". Anatomy is taught through precise, spatial prose.
- Schema must have ONLY the keys listed in CONTENT_PROMPT.md (plus the 3 underscore-prefixed routing keys).

### Anatomy and physiology lessons — prose must do the imaging work
- Be specific and spatial. *"The femur is the long bone of the upper leg. It articulates at the hip with the pelvis (a ball-and-socket joint allowing flexion, extension, abduction, adduction, rotation and circumduction) and at the knee with the tibia (a hinge joint allowing flexion and extension only). The patella sits in front of the knee joint."*
- Walk the student through structures in a clear sequence (top-to-bottom for the skeleton, blood flow order for the heart, air pathway for breathing).
- Use precise British medical terminology (anaerobic, fibre, organise, behaviour, manoeuvre, oedema, oesophagus where relevant).

### content_html
- 800–1500 words excluding tags
- Sequential `data-narration-id` (n1, n2, n3, ... no gaps)
- ≥2 `<div class="key-fact">` with actionable `data-revision-tip` (e.g. "Without looking, label the four chambers of the heart and the four major vessels in the order blood flows through them.")
- ≥2 `<div class="collapsible">` (use these for misconception unpacking, worked calculations, theory backstories like the inverted-U)
- **≥3** `<dfn class="term" data-def="...">` inline in paragraphs (PE is terminology-heavy — anatomy, physiology, training methods, psychology, ethics — aim higher, 5–8 is realistic in anatomy lessons)
- NO `<h1>` tags
- HTML entities allowed in content_html / exam_tip_html / conclusion_html: `&amp; &mdash; &lsquo; &rsquo; &ldquo; &rdquo; &deg; &times; &le; &ge;`. **NEVER** use HTML entities in plain-text fields (description, practice_questions, knowledge_checks, flashcard_questions, glossary_terms) — use plain unicode there.

### Original question wording
- Generate questions from the spec topic. Do **NOT** reproduce or paraphrase real AQA exam questions.
- Question stems should NOT mimic AQA trademark phrasing patterns. **Banned stem patterns:** "Other than X, identify two...", "Using Figure N...", "From the graph above...", "State two examples, other than the one given,...".
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
"9 marks — Evaluate"
```

Exact string match. Do not append paper codes or section labels.

### Calculation questions — use them when the topic suits
PE has built-in calculation territory. Include at least one calculation or data-interpretation question (`2 marks — Calculate`, `3 marks — Calculate from Data`, or `4 marks — Interpret Data`) in lessons whose topic is amenable. Examples:
- **Cardiac output / heart rate** — Q = stroke volume × heart rate; max HR = 220 − age; aerobic zone 60–80% of max HR; anaerobic zone 80–90% of max HR.
- **Mechanical advantage** — effort arm ÷ load arm.
- **One rep max** — % thresholds for strength vs muscular endurance training.
- **Energy / nutrition** — Kcal totals, % macronutrient split (55–60% carbohydrate, 25–30% fat, 15–20% protein).
- **Data interpretation** — comparisons of two participation figures, % change in obesity rates, mean / range of fitness test scores.

Mark scheme conventions for calculation questions:
- For 2-mark calculations, the **final answer** scores; the formula alone earns nothing if the answer is missing or wrong.
- For 3-mark calculations from data, working can earn method marks; the boxed final answer carries the rest. Always **show units** (bpm, %, seconds, kg, kcal, cm).
- Show the formula and the substitution in the model answer.

### Data interpretation questions — fabricate ORIGINAL data
For `4 marks — Interpret Data` and `3 marks — Calculate from Data` questions, invent ORIGINAL data tables / graph descriptions in the question stem. Realistic but fictional.

Examples of acceptable original data:
- *"Table 1 shows Sarah's heart rate during a 30-minute training session: rest 70 bpm, end of warm-up 110 bpm, peak (15 min) 165 bpm, recovery (5 min after) 90 bpm. Using the data, calculate the difference between peak heart rate and resting heart rate, and explain what this tells you about Sarah's exercise intensity."*
- *"A bar chart shows weekly participation in netball at three Year-10 schools: School A 18%, School B 27%, School C 12%. Interpret what the data shows about engagement patterns."*

Show the calculation and the inference in the mark scheme. **Never** reproduce real AQA figure numbers or data tables.

### Mark scheme rubric — StudyVault format ONLY
- Use **Mastering / Secure / Developing / Emerging** for `6 marks — Analyse` and `9 marks — Evaluate` (the levels-based extended-response questions).
- For shorter questions (1, 2, 3, 4 marks), use point-by-point allocation. State which acceptable answers earn which marks. e.g. *"1 mark for naming a long bone (femur, humerus, tibia or fibula); 1 mark for naming its function in movement (e.g. femur acts as the lever in running)."*
- **NEVER** use "Level 1 / 2 / 3" descriptors.
- **NEVER** use "Nothing worthy of credit".
- **NEVER** use "Award N marks for X" phrasing — the validator hard-bans this. Phrase as "1 mark for X; 1 mark for Y" or "Up to 3 marks: identification (1), context (1), explanation (1)".
- For `6 marks — Analyse` and `9 marks — Evaluate`, describe each tier:
  - **Mastering (highest band)** — full range of points, balanced where the question demands it, consistent sporting application, technically accurate language.
  - **Secure** — most points present, generally accurate, mostly applied to a sporting context.
  - **Developing** — relevant points but limited development or one-sided argument; some sporting context.
  - **Emerging** — basic points, little or no application, unbalanced or descriptive rather than analytical.

### Practice questions (exactly 6)
- Mix the 6 questions across the lesson's `suggested_question_types`. A common balance for an anatomy lesson: 1× `1 mark — Identify`, 1× `2 marks — Define`, 1× `3 marks — Describe`, 1× `4 marks — Explain`, 1× `6 marks — Analyse`, 1× `9 marks — Evaluate`. For a data lesson, swap in `3 marks — Calculate from Data` and `4 marks — Interpret Data`.
- Mark scheme uses StudyVault rubric for 6+ marks; point-by-point for shorter.
- Original compositions — never reproduce real AQA exam questions.
- Every question tests content from THIS lesson.

### Extended-response (6/9-mark) question stems — use ORIGINAL fictional scenarios
Real elite athletes are FINE in `content_html` for illustrative examples (Mo Farah, Jess Ennis-Hill, Anthony Joshua, Marcus Rashford, Dame Sarah Storey, Dina Asher-Smith, Adam Peaty, Beth Mead etc.). For marked 6/9-mark question stems, use ORIGINAL fictional scenarios:

Good examples:
- *"A 16-year-old county-level netball player is preparing for a major tournament that runs across three days."*
- *"A club-level marathon runner is moving from sea-level training to a 6-week training camp at altitude."*
- *"A Year-11 sprinter is being coached through her first plyometric training block."*
- *"A weekend cyclist has decided to use heart rate zones to structure his rides."*

Do **NOT** reproduce AQA's actual case-study contexts or athlete names from past papers.

### Knowledge checks (exactly 5)
- 2 mcq + 2 fill + 1 match (per CONTENT_PROMPT.md).
- Mix anatomy, training and socio-cultural content where the lesson allows — interleaving improves retrieval (EEF guidance).

### Flashcards (8–15)
- 12–15 typical for PE (terminology-heavy subject).
- Answer length ≤15 words target, hard cap 30.
- One fact per card, no enumerations.
- Card-type mix for PE: term ↔ definition (deltoid, hypertrophy, EPOC, gamesmanship, somatotype), formula ↔ application (max HR? 220 − age; mechanical advantage? effort arm ÷ load arm), example ↔ concept (Mo Farah finishing a 5,000 m — what energy system? aerobic), cause ↔ effect (effect of dehydration on blood viscosity? blood thickens, slows blood flow, raises heart rate).

### Glossary
- ≥3 `<dfn class="term">` inline (PE minimum; aim higher — 5–8 in anatomy/physiology lessons).
- ≥6 entries in `glossary_terms` array — PE is terminology-heavy and benefits from a fuller glossary than a typical free-tier lesson.

### exam_tip_html
- Reference the relevant command-word behaviour and common mark-scheme errors in plain English.
- Cite the typical mistake students make on this lesson's question types (e.g. *"On a 9-mark Evaluate, students often produce one-sided arguments. Mark schemes reward (a) range of points, (b) balanced argument, and (c) consistent sporting application — use a 'For X… However Y…' structure with a sporting example anchored to each side."*).
- **NEVER reference paper codes, section letters, or component codes** (see ABSOLUTE BANS below).

### conclusion_html
- 2-3 bullet point key takeaways per CONTENT_PROMPT.md format.

### Embed teaching brief content
- Use `subject_level_teaching_brief.common_misconceptions` to source at least one collapsible per lesson where a relevant misconception fits (antagonistic muscle pairs, lever LFE order, aerobic vs anaerobic justification, open vs closed skill confusion, one-sided 9-mark answers).
- Use `subject_level_teaching_brief.student_errors_by_question_type` to inform `exam_tip_html` for the lesson's primary question type.
- Use `subject_level_teaching_brief.topic_weighting_notes` and `pedagogical_notes` to shape pacing and exemplar choices.

### British English spelling and PE terminology
Always British English: anaerobic (not anerobic), behaviour, fibre, organise, manoeuvre, oedema, oesophagus.

Use spec vocabulary precisely:
- agonist / antagonist / prime mover (always paired with a joint and a phase of movement)
- isotonic concentric / isotonic eccentric / isometric (contraction types)
- vasoconstriction / vasodilation
- anticipatory rise (heart rate before the start of exercise)
- hypertrophy (muscle growth) vs bradycardia (lowered resting heart rate)
- EPOC / oxygen debt
- DOMS (delayed onset muscle soreness)
- fulcrum / load (resistance) / effort — always in LFE / FLE / FEL order on the lever drawing
- frontal / transverse / sagittal — for both planes and axes
- agility, balance, cardiovascular endurance, coordination, flexibility, muscular endurance, power, reaction time, strength, speed (the ten components of fitness)
- specificity, progressive overload, reversibility, tedium (SPORT)
- frequency, intensity, time, type (FITT)
- HIIT (high-intensity interval training)
- training threshold / training zone
- one rep max
- pulse raiser (warm-up phase) / cool down
- skill / ability — distinct concepts on the spec
- basic vs complex; open vs closed; self-paced vs externally paced; gross vs fine (the four classification continuums)
- SMART — specific, measurable, accepted, realistic, time-bound (note the spec uses "accepted" not "achievable")
- inverted-U theory (lower-case "u", with a hyphen)
- intrinsic vs extrinsic motivation; tangible vs intangible extrinsic
- introvert vs extrovert
- direct vs indirect aggression
- visual / verbal / manual / mechanical guidance
- positive / negative; intrinsic / extrinsic; knowledge of results / knowledge of performance (feedback)
- engagement patterns (the spec's term — not "participation rates")
- commercialisation, the "golden triangle" of sport, sponsorship and the media
- etiquette, sportsmanship, gamesmanship, contract to compete
- categories of PEDs: stimulants, narcotic analgesics, anabolic agents, peptide hormones (EPO), diuretics; plus blood doping; plus beta blockers (restricted)
- somatotypes — endomorph, mesomorph, ectomorph
- balanced diet (55–60% carbohydrate, 25–30% fat, 15–20% protein)
- dehydration / blood viscosity

### Plain-text fields
The fields `description`, `practice_questions[].text/.type/.marks`, `knowledge_checks[].q`, `flashcard_questions[].q/.a`, and `glossary_terms[].term/.definition` MUST use plain unicode. Type apostrophes, en-dashes and em-dashes directly. **NEVER** use HTML entities such as `&rsquo;`, `&amp;`, `&ndash;` in these fields — entities are only allowed inside `content_html`, `exam_tip_html` and `conclusion_html`. The validator hard-blocks entities in plain-text fields.

---

## ABSOLUTE BANS (PIPELINE-WIDE)

These have shipped before despite being forbidden — be vigilant:

- **NO spec codes anywhere**: `"8582"`, `"Edexcel 1PE0"`, `"GCSE 8582"`.
- **NO paper codes** in any user-facing string: `"Paper 1"`, `"Paper 2"`, `"P1"`, `"P2"`, `"8582/1"`, `"8582/2"`. Refer instead to "this paper", "the human body and movement content", "the socio-cultural and wellbeing content", or just "this lesson's exam-style questions".
- **NO section labels**: `"Section A"`, `"Section B"`. If you need to refer to a question type, use its name (e.g. "extended-response questions") not its section.
- **NO component / paper codes in `type` fields**: `"6 marks — Analyse (Paper 1)"`, `"9 marks — Evaluate (Section B)"`. Use just `"6 marks — Analyse"`, `"9 marks — Evaluate"`.
- **NO Level descriptors in `marks` field**: `"Level 1 (1-3): basic answer"`, `"Level 3 (7-9): detailed analysis"`. Use StudyVault rubric only.
- **NO** `"Nothing worthy of credit"` rubric phrasing.
- **NO** `"Award N marks for"` rubric phrasing.
- **NO** `"pastPaper"` field on questions (deprecated).
- **NO copying the reference lesson's content** — it's RE, a different subject. Match STRUCTURE only.
- **NO real-athlete scenarios in marked 6/9-mark question stems** (real athletes are fine in `content_html` for illustration; marked-question scenarios are fictional).
- **NO AQA trademark question stems verbatim** — no "Other than X, identify two...", "Using Figure N...", "Justify the inclusion of...".
- **NO references to diagrams that don't exist** in the lesson — there are no diagrams in free-tier PE lessons.

---

## Output

After generating all lessons in your batch, return ONLY this status line:

```
BATCH_DONE: batch_id={batch_id}, lessons_written={N}, files=<comma-separated paths>
```

Do NOT echo lesson content back. Just write the JSONs and confirm.

If a lesson's spec slice is too thin to generate quality content, write the JSON with whatever content you can produce based on the spec slice + general GCSE PE knowledge. Flag it in your status line: `BATCH_DONE: batch_id=..., lessons_written=..., notes="lesson 5 had thin spec — supplemented with general GCSE PE knowledge"`.


---

## EDEXCEL-SPECIFIC TERMINOLOGY ADAPTATIONS

This subject adapts ~97% from PE-AQA source content. **The following terminology differences MUST be honoured** — they're real spec divergences caught in Phase 1:

### Joint types
- **Edexcel teaches FOUR joint types**: pivot, hinge, condyloid, ball-and-socket. (AQA teaches only 2: hinge + ball-and-socket.)
- If you're adapting AQA content that lists 2 joint types, expand to all 4.
- Pivot joint examples: atlanto-axial joint (head turning side-to-side), radioulnar joint.
- Condyloid (also called ellipsoidal) joint examples: wrist, between metacarpals + phalanges.

### Muscle fibre types
- **Edexcel uses Type I / IIa / IIx nomenclature** (not "slow oxidative / fast oxidative-glycolytic / fast glycolytic" from older textbooks).
- Type I: slow twitch, aerobic, endurance.
- Type IIa: fast twitch, can be aerobic or anaerobic, middle-distance.
- Type IIx: fast twitch, anaerobic, explosive/sprint power.

### Bone shape classification
- **Edexcel requires FIVE bone shape categories**: long, short, flat, irregular, sesamoid.
- Examples: long (femur, humerus), short (carpals, tarsals), flat (skull, scapula, ribs), irregular (vertebrae), sesamoid (patella).
- AQA only requires 4 (no sesamoid). Add patella as sesamoid example for Edexcel.

### Training principles — SMART goals
- **Edexcel SMART A = "Achievable"** (NOT "Accepted" or "Agreed" as some textbooks use).
- S = Specific, M = Measurable, A = Achievable, R = Realistic (or Relevant), T = Time-bound.

### Feedback in skill acquisition
- **Edexcel uses Concurrent (during) and Terminal (after) feedback** as the primary classification.
- Intrinsic / Extrinsic and Positive / Negative also covered.
- AQA's "Knowledge of Results (KR) / Knowledge of Performance (KP)" framing is NOT the Edexcel taxonomy — DO NOT use those terms.

### Skill classification continua
- **Edexcel uses High-organisation / Low-organisation skill continuum** (alongside open/closed and gross/fine).
- AQA's "self-paced / externally-paced" is NOT a primary Edexcel continuum — use external/internal pacing if needed but lead with high/low organisation.

### Anatomical movement terminology
- **Edexcel teaches "vertical axis" terminology** for rotation around the long axis of the body (e.g. spinning a discus throw).
- The three axes: sagittal (front-to-back rotation, e.g. cartwheel), frontal/transverse (side-to-side rotation, e.g. somersault), vertical (rotation around the long axis, e.g. spinning).
- The three planes: frontal, sagittal, transverse.

### Performance-Enhancing Drugs (PEDs)
- **Edexcel places PEDs in Component 1 (Physical Training)**, NOT Component 2.
- AQA bundles PEDs with socio-cultural/ethical issues; for Edexcel they sit under training-and-performance.

---

## EDEXCEL COMMAND WORDS

Your `practice_questions[].type` strings MUST match the registered question type names from the batch JSON. Edexcel command words used:
- **Give / State / Identify / Define** (1-mark recall)
- **Describe** (2-3 marks: what/how)
- **Calculate** (2-3 marks: arithmetic from given data, e.g. BMI, target HR, % improvement)
- **Explain** (3-6 marks: why/how with development)
- **Discuss** (6 marks: balanced points either side)
- **Analyse** (6-9 marks: break down + interpret data/scenario)
- **Assess / Evaluate** (9 marks: weighted judgement)
- **Multiple Choice** (1 mark, 4 options)

NO 8-mark essay slots. NO "Award N marks for…" rubric phrasing — use Mastering / Secure / Developing / Emerging per StudyVault convention.

---

## CROSS-BOARD ADAPTATION RULES

Most lessons have `content_transfer.transfer_score: 'high'` or `'medium'` pointing to a PE-AQA lesson. Source content is in `scripts/_content_physical-education-edexcel/_aqa_source_lessons.json` indexed by AQA unit slug + lesson_number.

For `high` transfer: lift the AQA content structurally as the spine. Strip AQA-specific terminology. Substitute Edexcel-spec terminology per the section above. Regenerate `practice_questions` fresh in Edexcel command words.

For `medium` transfer: use AQA content as scaffolding for half the lesson; rewrite the other half to match Edexcel's distinctive framing.

For `fresh` (only 1 lesson in this build — Unit 2 L13 synoptic 9-mark practice): generate from spec only, NO AQA source.

DO NOT include past paper questions verbatim. ALWAYS regenerate `practice_questions` in target-board style.
