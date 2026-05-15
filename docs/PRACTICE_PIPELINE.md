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
  - **Do not** prefix option strings with "A.", "B." etc. The renderer adds A/B/C/D letter badges automatically based on shuffled display position. Prefixing in the data would render as "A. A. London".

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

## Chart embedding rules — never describe what you can show

**The rule:** if a problem references a data visualisation — bar chart, histogram, pictogram, scatter diagram, stem-and-leaf, frequency table, Venn diagram, tree diagram, box plot, pie chart, frequency polygon, cumulative frequency curve, population pyramid, choropleth, time series, or any other chart or table — it MUST embed the visualisation, not describe it in prose.

A question stem that tells the student what a chart contains is not the same as showing the chart. GCSE Statistics exam papers always print the actual chart. The practice renderer must do the same.

### Anti-examples

**Bar chart** (wrong):
> ❌ "The following bar chart shows the heights of students in a class. The bar for 150–160 cm reaches 8, the bar for 160–170 cm reaches 12..."

**Right:** include the `chart` field with a Chart.js config. The student reads from the rendered chart.

**Pictogram** (wrong):
> ❌ "A pictogram uses one football to represent six goals. Liverpool: 4 footballs. Arsenal: 3 footballs. Chelsea: 2.5 footballs. What is Arsenal's total goal tally?"

**Right:** embed the pictogram as inline SVG in the `display` field with a key. The student reads from the picture.

**Stem-and-leaf** (wrong):
> ❌ "The stem 3 has leaves 2, 5, 7. The stem 4 has leaves 0, 4, 8, 9..."

**Right:** embed a `<table class="stem-leaf">` inside the `display` field.

---

### Per-chart-type rendering table

| Chart type | Mechanism | Notes |
|---|---|---|
| Bar chart | `chart` field, `type:"bar"` | Set `options.scales.x.title` and `y.title` |
| Histogram | `chart` field, `type:"bar"` with `barPercentage:1, categoryPercentage:1` | y-axis label = "Frequency density"; x labels = class boundaries |
| Pie / sector | `chart` field, `type:"pie"`, `showLegend:true` | |
| Line chart / time series | `chart` field, `type:"line"` | |
| Frequency polygon | `chart` field, `type:"line"`, `fill:false`, midpoints as x labels | |
| Cumulative frequency curve | `chart` field, `type:"line"` | x = upper class boundary, y = CF |
| Scatter diagram | `chart` field, `type:"scatter"` | Data as `{x,y}` pairs |
| Box plot | `chart` field, `type:"boxplot"` | Plugin loaded on `practice.html`; use pre-computed `{min,q1,median,q3,max}` objects |
| Two-way table / frequency table | `<table class="data-table">` HTML inside `display` field | Full HTML is rendered via `innerHTML` — no sanitisation |
| Stem-and-leaf (single) | `<table class="stem-leaf">` inside `display` field | See HTML template below |
| Stem-and-leaf (back-to-back) | `<table class="stem-leaf stem-leaf--btb">` inside `display` field | See HTML template below |
| Venn diagram | Inline `<svg class="venn-diagram" viewBox="0 0 300 180" width="100%">` inside `display` | 2 or 3 overlapping circles; label each region with its count |
| Tree diagram | Inline `<svg class="tree-diagram" viewBox="0 0 400 260" width="100%">` inside `display` | Branch lines with probability labels at each branch |
| Pictogram | Inline `<svg class="pictogram" viewBox="0 0 360 200" width="100%">` inside `display` | Symbol grid with a key row at the bottom |
| Tally chart | `<table class="tally-chart">` inside `display` | Three columns: Category, Tally, Frequency |
| Population pyramid / choropleth | Inline `<svg>` or descriptive `<table>` — case-by-case | Complex; prefer MCQ proxy when chart would be very large |

**Note on `display` field HTML:** the renderer calls `eqEl.innerHTML = formatDisplay(p.display)` with no sanitisation. Full HTML — `<table>`, `<svg>`, `<pre>` — renders correctly. Inline KaTeX `\(...\)` is also supported alongside HTML.

**Note on box plots:** `@sgratzl/chartjs-chart-boxplot@4` is loaded on `practice.html` (confirmed line 12). It is NOT loaded on `lesson.html` — article-format lessons must use inline SVG for box plots instead.

**Note on `image` field:** there is no `image` field handler in the main problem-card renderer. Do not use it. Use `display`-embedded SVG for all static visual content.

---

### Stem-and-leaf HTML template

Single dataset:

```html
<table class="stem-leaf">
  <tr><th>Stem</th><th>Leaves</th></tr>
  <tr><td>2</td><td>3 5 7</td></tr>
  <tr><td>3</td><td>0 1 4 8</td></tr>
  <tr><td>4</td><td>2 6 9</td></tr>
</table>
<p class="stem-leaf-key">Key: 2 | 3 means 23</p>
```

Back-to-back (comparison of two datasets — Group A leaves read right-to-left, Group B left-to-right):

```html
<table class="stem-leaf stem-leaf--btb">
  <tr><th>Group A</th><th>Stem</th><th>Group B</th></tr>
  <tr><td>9 7 3</td><td>2</td><td>1 4 6</td></tr>
  <tr><td>8 5 1</td><td>3</td><td>0 2 7</td></tr>
  <tr><td>6 4</td><td>4</td><td>3 5 8 9</td></tr>
</table>
<p class="stem-leaf-key">Key: 3 | 2 | 1 means Group A = 23, Group B = 21</p>
```

---

### Tally chart HTML template

```html
<table class="tally-chart">
  <tr><th>Colour</th><th>Tally</th><th>Frequency</th></tr>
  <tr><td>Red</td><td>|||| |</td><td>6</td></tr>
  <tr><td>Blue</td><td>||||</td><td>4</td></tr>
  <tr><td>Green</td><td>|||</td><td>3</td></tr>
</table>
```

Use `||||` (four vertical strokes) for groups of four and `||||` + space + `|` for five. Do not use Unicode tally characters — they render inconsistently across browsers. Plain ASCII `|` characters in a monospace-styled cell are fine.

---

### Pictogram SVG template

Pictograms must include a key. AQA spec requires the key to appear with the diagram. Example (footballs representing goals, 1 symbol = 6 goals, half-symbol = 3):

```html
<svg class="pictogram" viewBox="0 0 360 180" width="100%" xmlns="http://www.w3.org/2000/svg">
  <!-- Row labels -->
  <text x="70" y="35" text-anchor="end" font-family="Inter,sans-serif" font-size="13">Liverpool</text>
  <text x="70" y="75" text-anchor="end" font-family="Inter,sans-serif" font-size="13">Arsenal</text>
  <text x="70" y="115" text-anchor="end" font-family="Inter,sans-serif" font-size="13">Chelsea</text>
  <!-- Symbols (circles as stand-in for footballs — replace with <use> if icon available) -->
  <!-- Liverpool: 4 full symbols -->
  <circle cx="90"  cy="28" r="10" fill="#1a1a1a"/>
  <circle cx="115" cy="28" r="10" fill="#1a1a1a"/>
  <circle cx="140" cy="28" r="10" fill="#1a1a1a"/>
  <circle cx="165" cy="28" r="10" fill="#1a1a1a"/>
  <!-- Arsenal: 3 full symbols -->
  <circle cx="90"  cy="68" r="10" fill="#1a1a1a"/>
  <circle cx="115" cy="68" r="10" fill="#1a1a1a"/>
  <circle cx="140" cy="68" r="10" fill="#1a1a1a"/>
  <!-- Chelsea: 2 full + 1 half (right semicircle) -->
  <circle cx="90"  cy="108" r="10" fill="#1a1a1a"/>
  <circle cx="115" cy="108" r="10" fill="#1a1a1a"/>
  <path d="M125,108 a10,10 0 0,1 -10,-10 a10,10 0 0,1 10,10 Z" fill="#1a1a1a"/>
  <!-- Key -->
  <line x1="75" y1="150" x2="345" y2="150" stroke="#ccc" stroke-width="1"/>
  <circle cx="90" cy="163" r="8" fill="#1a1a1a"/>
  <text x="105" y="168" font-family="Inter,sans-serif" font-size="12" fill="#555">= 6 goals</text>
</svg>
```

Adapt symbol shape and counts to the specific question. Always include the key line.

---

### Venn diagram SVG template (two sets)

```html
<svg class="venn-diagram" viewBox="0 0 300 160" width="100%" xmlns="http://www.w3.org/2000/svg">
  <circle cx="110" cy="80" r="60" fill="#3b82f6" fill-opacity="0.25" stroke="#3b82f6" stroke-width="1.5"/>
  <circle cx="190" cy="80" r="60" fill="#ef4444" fill-opacity="0.25" stroke="#ef4444" stroke-width="1.5"/>
  <!-- Region counts -->
  <text x="75"  y="85" text-anchor="middle" font-family="Inter,sans-serif" font-size="18" font-weight="600">8</text>
  <text x="150" y="85" text-anchor="middle" font-family="Inter,sans-serif" font-size="18" font-weight="600">5</text>
  <text x="225" y="85" text-anchor="middle" font-family="Inter,sans-serif" font-size="18" font-weight="600">12</text>
  <!-- Labels -->
  <text x="80"  y="20" text-anchor="middle" font-family="Inter,sans-serif" font-size="12" fill="#1e40af">Set A</text>
  <text x="220" y="20" text-anchor="middle" font-family="Inter,sans-serif" font-size="12" fill="#b91c1c">Set B</text>
</svg>
```

For three-set Venn diagrams, use three overlapping circles and label all seven regions (A only, B only, C only, A∩B, A∩C, B∩C, A∩B∩C).

---

### Tree diagram SVG template

```html
<svg class="tree-diagram" viewBox="0 0 400 220" width="100%" xmlns="http://www.w3.org/2000/svg">
  <!-- Root point -->
  <circle cx="40" cy="110" r="4" fill="#555"/>
  <!-- First branches -->
  <line x1="44" y1="110" x2="156" y2="55"  stroke="#555" stroke-width="1.5"/>
  <line x1="44" y1="110" x2="156" y2="165" stroke="#555" stroke-width="1.5"/>
  <!-- Branch probability labels -->
  <text x="85"  y="72"  font-family="Inter,sans-serif" font-size="12" text-anchor="middle">0.4</text>
  <text x="85"  y="148" font-family="Inter,sans-serif" font-size="12" text-anchor="middle">0.6</text>
  <!-- First-level nodes -->
  <circle cx="160" cy="55"  r="4" fill="#555"/>
  <circle cx="160" cy="165" r="4" fill="#555"/>
  <!-- Labels -->
  <text x="168" y="59"  font-family="Inter,sans-serif" font-size="13" fill="#1e40af">Red</text>
  <text x="168" y="169" font-family="Inter,sans-serif" font-size="13" fill="#b91c1c">Blue</text>
  <!-- Second branches from Red -->
  <line x1="164" y1="55"  x2="276" y2="30"  stroke="#555" stroke-width="1.5"/>
  <line x1="164" y1="55"  x2="276" y2="80"  stroke="#555" stroke-width="1.5"/>
  <text x="215" y="33"  font-family="Inter,sans-serif" font-size="12" text-anchor="middle">0.3</text>
  <text x="215" y="77"  font-family="Inter,sans-serif" font-size="12" text-anchor="middle">0.7</text>
  <text x="284" y="34"  font-family="Inter,sans-serif" font-size="13" fill="#1e40af">Red</text>
  <text x="284" y="84"  font-family="Inter,sans-serif" font-size="13" fill="#b91c1c">Blue</text>
  <!-- Second branches from Blue -->
  <line x1="164" y1="165" x2="276" y2="140" stroke="#555" stroke-width="1.5"/>
  <line x1="164" y1="165" x2="276" y2="190" stroke="#555" stroke-width="1.5"/>
  <text x="215" y="143" font-family="Inter,sans-serif" font-size="12" text-anchor="middle">0.5</text>
  <text x="215" y="187" font-family="Inter,sans-serif" font-size="12" text-anchor="middle">0.5</text>
  <text x="284" y="144" font-family="Inter,sans-serif" font-size="13" fill="#1e40af">Red</text>
  <text x="284" y="194" font-family="Inter,sans-serif" font-size="13" fill="#b91c1c">Blue</text>
</svg>
```

Scale `viewBox` height to match the number of branches. Without-replacement problems must update branch probabilities at second stage accordingly (e.g. if 3 red + 5 blue and first draw was red: second-stage P(red) = 2/7).

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
