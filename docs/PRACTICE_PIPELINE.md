# Practice Pipeline — Practice-Format Lessons

For subjects or units where the plan marks them as practice-format. Replaces the bespoke per-subject approach with a unified eight-stage factory.

Article-format lessons use `CONTENT_PROMPT.md` instead.

---

## When a unit is practice-format

Decided by the planning agent per unit — see `PLANNING_PROMPT.md`. Triggers when:
- >50% of the unit's exam marks come from 1–6 mark deterministic questions (calculations, grammar, short answer, technique application)
- The unit is skills-based (procedural) rather than content-based (knowledge)

Subjects already using practice format:
- **Mathematics** (all 4 boards, practice-only) — see `memory/project_maths_practice_rebuild.md`
- **English Language** (practice-first, 4 units) — factory stages documented in `scripts/factory/FACTORY_RULES.md`
- **Modern Foreign Languages** (Spanish/French/German, practice-only) — see `scripts/language-practice/PRACTICE_DATA_SCHEMA.md`
- **Science calculation units** (Physics Calc, Chem Calc, Bio Data, Higher Calculations) — see `scripts/science-practice/SCIENCE_PRACTICE_SCHEMA.md`
- **Geography Skills** (one unit within a mixed subject)

---

## Output shape

Practice lessons store their content in `lessons.practice_data` (JSONB), not `content_html`. The loader renders from `practice.html` + `practice-loader.js` rather than `lesson.html` + `lesson-loader.js`.

```json
{
  "method_card": {
    "title": "Lesson Title",
    "content": "<p>HTML — 200-400 words. Strategy-focused; equations/rules only.</p>",
    "steps": ["Imperative step 1", "Step 2", "Step 3"]
  },
  "exam_context": {
    "paper": "Paper reference",
    "marks": "Typical mark range",
    "frequency": "How often this appears in exams"
  },
  "worked_examples": [
    { "difficulty": "Bronze", "question": "...", "steps": [...] },
    { "difficulty": "Silver", "question": "...", "steps": [...] },
    { "difficulty": "Gold", "question": "...", "steps": [...] }
  ],
  "problem_bank": {
    "bronze": [ /* 7-8 problems */ ],
    "silver": [ /* 6 problems */ ],
    "gold": [ /* 5-6 problems */ ]
  },
  "ai_marking_prompts": { /* system prompts for AI-marked question types */ },
  "topic_links": { "prerequisites": [...] }
}
```

Totals: **20 problems per lesson** (7-8 Bronze, 6 Silver, 5-6 Gold). Worked examples: one per tier (3 per lesson), 2-4 steps each.

No `content_html`, no narration, no podcasts, no flashcards, no knowledge checks. Passage narration (6 Azure voices cycled) exists for passage-based subjects like English Language — see Phase 4 in `PIPELINE.md`.

---

## The eight factory stages

Each stage is one agent call per lesson (or parallelised across lessons where the inputs are lesson-independent). This structure was proven on English Language Paper 1 Reading and generalises to all practice subjects with subject-specific input types swapped in at stage 3+.

| Stage | Name | Depends on | Parallelisable |
|---|---|---|---|
| s1 | Passages (passage-based subjects only) or lesson specs | Plan | Across lessons |
| s2 | Method cards | s1 | Across lessons |
| s3 | Bronze problems | s1, s2 | Across lessons |
| s4 | Silver problems + worked examples | s1, s2, s3 | Across lessons |
| s5 | Gold problems | s1, s2, s4 | Across lessons |
| s6 | Worked examples (if not covered in s4) | s3, s4, s5 | Across lessons |
| s7 | AI marking system prompts | subject-level, once | — |
| s8 | Topic links | s1-s6 | Across lessons |

Each stage outputs a JSON file (one per lesson or one per subject). Final assembly merges them into the `practice_data` object and inserts into Supabase.

**Why stages, not a single mega-prompt:** one agent producing a whole lesson's 20 problems thins toward the end (silver and gold are worse than bronze). Specialised stage agents keep quality consistent. Proven in English Language — don't deviate.

---

## Input types registry

Practice format uses input-type tags to determine how `practice-loader.js` renders the problem. Not every subject uses every type — each subject area has its own appropriate set.

### Universal (all subjects)
- `single_value` — numeric answer with optional unit and tolerance
- `multiple_choice` — 4 options, `solutions: [correctIndex]`

### Maths
See `memory/project_maths_practice_rebuild.md`. Types: `single_value`, `two_solutions`, `fraction`, `standard_form`, `multiple_choice`. Chart.js data visualisations in the `chart` field on the problem.

### English Language
See `scripts/factory/FACTORY_RULES.md`. Types: `traffic_light`, `highlight_evidence`, `connotation_picker`, `multiple_choice`, `evidence_match`, `ai_mark`, `misleading_summary`, `ai_write`, `improve_sentence`, `spot_error`, `reorder`.

### Modern Foreign Languages
See `scripts/language-practice/PRACTICE_DATA_SCHEMA.md`. Types: `vocab_match`, `gap_fill` (word bank and free-input), `translate` (bidirectional, AI-marked), `dictation` (Azure TTS audio), `sentence_builder`, `spot_correct`, `role_play`, `multiple_choice`, `reorder`, `ai_mark`, `ai_write`.

### Science (calculation units)
See `scripts/science-practice/SCIENCE_PRACTICE_SCHEMA.md`. Types: `single_value`, `standard_form`, `multiple_choice`. Chart.js for data-skill lessons. Equation hint toggle: Bronze/Silver show per-problem "Show equation" button, Gold = pure recall.

### Geography Skills
One unit within an otherwise-article subject. Uses passages with custom panels: `chart` (Chart.js in centre panel), `image` (OS maps, generated Cartopy maps), `ruler` (digital ruler for distance calculations), stats tools auto-detected from question keywords. See the Geography Skills sections of the main CLAUDE.md and `memory/` for the live enhancements.

---

## Universal quality rules

Applied at validation across every practice subject:

1. **Original content only.** No past paper questions, no exam board mark scheme language, no spec codes, no component codes.
2. **Method cards = strategy, not content.** 2-3 sentences of HTML plus 3-6 imperative steps. Not mini-articles.
3. **Worked examples use illustrative framing.** "Consider this phrase…", "Look at the quote above…", "In this example…". Never live-reading framing ("Read this extract…").
4. **Final worked example step has `isAnswer: true`** (Languages/English use `isAnswer`; Science uses `is_answer` — honour each subject's schema convention).
5. **Every problem has `misconceptions`** (Maths/Science) or equivalent `wrong` explanations (Languages) — 1-3 entries per problem, specific and educational.
6. **AI marking prompts reward insight over format.** Referencing specific words without quotation marks IS valid evidence. Don't require embedded quotation. Don't require formal PEE structure. Use StudyVault language — never "AQA examiner", always "GCSE tutor".
7. **Marks routing.** `marks <= 8` → Haiku. `marks > 8` → Sonnet. Matches `/api/ai-mark` behaviour.
8. **Higher-only flagging.** Problems testing Higher-tier content get `higher_only: true` (filtered out of Foundation view by `practice-loader.js`).
9. **Topic links** use the format `{ "title": "Lesson Title", "slug": "unit-slug/N" }`. Sequential within unit: each lesson links to its predecessor and successor.
10. **No `related_videos` in `practice_data`.** Related media is on the lesson row, not in practice_data — the template reads it from there automatically.

---

## Passage narration (passage-based subjects only)

Applies to English Language, other reading-based practice subjects. Not needed for Maths, Science calcs, or Geography Skills.

- Six Azure voices cycled across passages to maintain variety (Ada, Ollie, Olivia, Nova Turbo, Shimmer Turbo, Andrew)
- Script: `scripts/generate_passage_narration.py`
- Each passage gets one MP3 on R2. URL stored on the passage record.

---

## Dictation audio (MFL only)

- `input_type: "dictation"` problems need TTS audio generated
- Target-language voice selection based on `target_lang` field (es/fr/de)
- Script: `scripts/language-practice/generate_dictation_audio.py` (or equivalent)
- `max_plays` controls how many times a student can replay (typically 2 at Bronze/Silver, 2-3 at Gold)
- `strict_accents` toggle: Bronze/Silver lenient, Gold strict

---

## Validation before ship

QA script: `scripts/_qa_practice_data.py` — reads every practice lesson's `practice_data` from Supabase and validates:
- 20 problems per lesson (tier distribution 7-8 / 6 / 5-6)
- Every problem has required fields per its `input_type`
- Solutions are the correct type (numeric for calculations, array of indices for multiple_choice)
- No exam board Level descriptors in any string field
- No spec codes or component codes
- All AI marking prompts reference `/api/ai-mark` tier routing correctly

Runs before shipping, same as the article drift grep in `CONTENT_PROMPT.md`.

---

## Reference lessons (pinned)

Three practice references are pinned, covering the structurally distinct shapes:

- **Passage-based English practice** → English Language AQA Paper 1 Reading L1 "Explicit and Implicit Information" (`83ab6156-e0e5-4011-bb79-2c7a70bbdc41`). Use for: English Language (all boards), Geography Skills, Science calculation units. Seven input types, prose-analysis focus, AI-marked extended responses.
- **Language/MFL practice** → Spanish AQA Popular Culture L1 "Free-Time Activities and Hobbies" (`934d507a-841c-48ed-8608-836ea49cc7f4`). Use for: French, German, Spanish, and any new GCSE language (Italian, Mandarin, Latin language paper, etc.). Ten input types including language-unique `vocab_match`, `dictation`, `translate`, `role_play`, `sentence_builder`, `spot_correct`. AI marking for translation and role play.
- **Calculation-based (Maths shape)** → Maths AQA Graphs L3 "Quadratic Graphs" (`c8bc060f-c094-4b04-abec-5577523f8667`). Use for: Mathematics, Statistics, Further Maths, Astronomy calculations. Five input types including Maths-unique `two_solutions`. No AI marking (deterministic). Chart.js inline pattern cross-referenced.

Planning agent decides which reference to fetch based on the subject's dominant question style:
- MFL subject? → Language reference
- Maths/Stats/calc subject? → Maths reference
- Everything else practice-shaped? → English Lang reference (widest coverage, AI marking for prose responses)

Full practice reference details with Supabase IDs, fetch snippets, and subject mapping lists are in `REFERENCE_LESSONS.md`.

Agent prompt template for each stage, and the full stage orchestration script, live in `scripts/factory/`. This doc is the entry point, not the runbook.
