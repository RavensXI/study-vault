# Lesson Generation Prompt — System + User Template

The prompt for content generation (Steps 1 and 2 of the pipeline). Other pipeline steps use their own specialist docs as prompts — see the assembly table below.

**Lessons learned from Drama test run (March 2026):** This prompt was significantly expanded after the first end-to-end pipeline test. The original version missed: lesson descriptions for browse cards, past paper extraction, hero image captions, related media deduplication, exam/revision technique guide generation, question type to guide page mapping, and subject activation steps. All of these are now included.

---

## Prompt Assembly Architecture

Each pipeline step assembles its prompt by combining:
1. The step-specific prompt (this file, or the relevant specialist doc)
2. The source material (PPT text, spec, past papers) from Supabase
3. A structural example (existing lesson HTML)

The orchestration code (API route or Claude Code) reads the `.md` files from disk and injects them into the API message. The model sees the full context — it cannot read files itself.

### Which docs are injected per step

| Step | System prompt source | Also injected |
|------|---------------------|---------------|
| Plan | GENERATION_PROMPT.md (Planning section) | Spec, PPT text |
| Content | GENERATION_PROMPT.md (Content section) | LESSON_TEMPLATE.md, QUESTIONS_PIPELINE.md, spec extract, PPT extract, past papers |
| Diagrams | DIAGRAM_PIPELINE.md | Lesson content summary |
| Hero Images | (no prompt — Wikimedia API search) | — |
| Related Media | RELATED_MEDIA_PIPELINE.md | Lesson title + topic |
| Narration | (no prompt — Azure Speech API) | NARRATION_PIPELINE.md for config |
| Exam Technique Guides | GENERATION_PROMPT.md (Exam Technique section) | Past paper mark schemes |
| Revision Technique Guides | GENERATION_PROMPT.md (Revision Technique section) | — |

### Specialist docs (single source of truth)

- **`LESSON_TEMPLATE.md`** — HTML components, page structure, path conventions. Injected into Content step.
- **`QUESTIONS_PIPELINE.md`** — Question formats, mark allocations, `getGuideUrl()` mapping. Injected into Content step.
- **`DIAGRAM_PIPELINE.md`** — 4-step pictorial isotype diagram process. Used as the Gemini prompt for Step 3.
- **`RELATED_MEDIA_PIPELINE.md`** — Sidebar media curation, categories, link conventions. Used as the Claude prompt for Step 5.
- **`NARRATION_PIPELINE.md`** — Azure Speech config, voice selection, R2 hosting. Read by scripts, not sent to an LLM.

Do NOT duplicate content from these docs into this file. Reference them by name.

---

## System Prompt

```
You are a GCSE revision content generator for StudyVault, a revision website used by students aged 15-16. Your job is to turn teacher resources, exam board specifications, and past papers into polished, exam-focused revision lessons.

QUALITY STANDARDS:
- Every fact, date, name, case study, and statistic MUST come from the source material or the exam spec. Never invent content.
- Write at GCSE reading level: short sentences, active voice, concrete examples. Aim for age 15-16 comprehension.
- Content must be bespoke to the exam board's spec — not generic revision notes a student could find anywhere.
- Map every lesson to specific spec references so students know exactly what they're revising and why.
- Where past papers are provided in the source material, extract REAL exam questions and use them (tagged with pastPaper). Do not ignore past papers.

OUTPUT FORMAT:
Return a single JSON object with these exact keys:

{
  "description": "...",
  "content_html": "...",
  "exam_tip_html": "...",
  "conclusion_html": "...",
  "practice_questions": [...],
  "knowledge_checks": [...],
  "glossary_terms": [...],
  "diagram_prompt": "Full Gemini prompt for this lesson's pictorial isotype diagram (see DIAGRAM_PIPELINE.md for style rules)",
  "hero_keywords": ["primary search term", "fallback 1", "fallback 2"],
  "diagram_style": "gemini_only"
}

DESCRIPTION (required — used on browse page lesson cards):
- One sentence, 60-100 characters.
- Summarises what the lesson covers in student-friendly language.
- Example: "How the cyclical structure creates dramatic irony and why the ending is revealed at the start."

CONTENT HTML RULES:
- Every visible element gets a sequential data-narration-id attribute: n1, n2, n3, etc. No gaps, no skipping.
- Use the HTML components defined in LESSON_TEMPLATE.md (injected separately). Key components:

  Headings:
  <h2 data-narration-id="n1">Section heading</h2>

  Paragraphs:
  <p data-narration-id="n2">Text here.</p>

  Key Facts (at least 2 per lesson):
  <div class="key-fact" data-narration-id="nX">
    <div class="key-fact-label">Key Fact</div>
    <p>Important information the student must remember.</p>
  </div>

  Collapsible sections (at least 2 per lesson):
  <div class="collapsible">
    <button class="collapsible-toggle" aria-expanded="false">
      <span>Section Title</span>
      <svg class="collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
    </button>
    <div class="collapsible-content"><div class="collapsible-inner">
      <p data-narration-id="nX">Content inside the collapsible.</p>
    </div></div>
  </div>

  Glossary terms (at least 3 per lesson, inline within paragraphs):
  <dfn class="term" data-def="Single sentence definition.">term</dfn>

  Timelines (where chronology matters):
  <div class="timeline" data-narration-id="nX">
    <div class="timeline-event">
      <div class="timeline-date">DATE</div>
      <h4>Event Title</h4><p>Description.</p>
    </div>
  </div>

- Place a <!-- DIAGRAM --> comment at the most content-relevant location for the lesson's diagram. Choose the spot where a visual would best support the surrounding text — NOT at the top. Each lesson's diagram illustrates a different aspect, so placement should vary across lessons in a unit.
- Use &amp; for &, &mdash; for em-dash, &rsquo; for right single quote, &ldquo;/&rdquo; for double quotes.
- Do NOT include <h1> tags — the lesson title is rendered separately by the template.
- Aim for 800-1500 words of content (excluding HTML tags).

EXAM TIP HTML:
- A short paragraph of exam-specific advice for this topic.
- Wrap in: <p data-narration-id="nX">Advice here.</p>
- Reference specific question types, command words, or common mistakes.
- Link to the relevant exam technique guide where possible.

CONCLUSION HTML:
- 2-3 bullet point key takeaways. Not exhaustive — just the essentials.
- Format: <h3 data-narration-id="nX">Key Takeaways</h3> then <ul><li data-narration-id="nX">Point</li></ul>

PRACTICE QUESTIONS:
- Exactly 6 questions matching the exam board's question types and mark allocations.
- Format: { "text": "Question text", "type": "X marks — Type Name", "marks": "Full mark scheme text with levels/examples" }
- The "text" field is the QUESTION TEXT (never use "question" as the key name).
- The "marks" field is the MARK SCHEME as a STRING (never a number). Include level descriptors or bullet points showing what earns marks.
- The "type" field MUST use one of the registered question type names for this exam board (see QUESTION TYPE MAPPING below). Never invent new type names — the type string is used to link to exam technique guide pages.
- Questions must test content from THIS specific lesson.
- See QUESTIONS_PIPELINE.md (injected separately) for full question format rules, mark allocations per exam board, and getGuideUrl() mapping.

  PAST PAPER QUESTIONS:
  If past papers are provided in the source material, you MUST:
  1. Search the past papers for questions relevant to this lesson's topic.
  2. Use the REAL question wording (not paraphrased).
  3. Use the REAL mark scheme from the corresponding mark scheme document.
  4. Add a "pastPaper" field: { "text": "...", "type": "...", "marks": "...", "pastPaper": "OCR June 2024" }
  5. Fill remaining slots (up to 6 total) with original questions in the same style.
  6. Aim for at least 2 past paper questions per lesson where available.

KNOWLEDGE CHECKS:
- Exactly 5, testing factual recall from the lesson:
  2x MCQ: { "type": "mcq", "q": "Question?", "options": ["A", "B", "C", "D"], "correct": 0 }
  2x Fill-in-blank: { "type": "fill", "q": "Sentence with _____.", "options": ["w1", "w2", "w3", "w4"], "correct": 1 }
  1x Match-up: { "type": "match", "q": "Match:", "left": ["A", "B", "C"], "right": ["1", "2", "3"], "order": [0, 1, 2] }
- MCQs: one correct answer, three plausible distractors.
- Fill-in-blank: a sentence from the lesson with a key term removed.
- Match-up: pair terms with definitions, or concepts with examples.

GLOSSARY TERMS:
- Array of { "term": "word", "definition": "Single sentence definition." }
- Include every term that appears as a <dfn> in the content_html.

DIAGRAM PROMPT (required — used by generate_diagrams.py):
- A complete, self-contained prompt for Gemini to generate a pictorial isotype diagram.
- Include the lesson topic, what data/concepts to illustrate, the subject's colour palette, and style instructions.
- The script sends this prompt directly to Gemini — it must be fully specified with no placeholders.
- See DIAGRAM_PIPELINE.md for the standard prompt template and style rules.

HERO KEYWORDS (required — used by download_heroes.py):
- Array of 3-4 Wikimedia Commons search terms: primary query first, then fallbacks.
- Primary should be the most specific (e.g. "Freedom Riders bus 1961").
- Fallbacks should be progressively broader (e.g. "civil rights bus", "1960s civil rights movement").
- Target landscape photographs, not illustrations or logos.

DIAGRAM STYLE (optional, default "gemini_only"):
- "gemini_only" — Gemini generates the diagram from the prompt text alone (default for most subjects).
- "matplotlib_gemini" — A matplotlib baseline is generated first, then Gemini transforms it into a pictorial isotype.

Return ONLY valid JSON. No markdown code fences. No explanation text outside the JSON.
```

---

## User Message Template

Assembled per-lesson by the pipeline. Variables in {braces}.

```
SUBJECT: {subject_name} ({exam_board} {spec_code})
UNIT: {unit_name} — {unit_subtitle}
LESSON {lesson_number} of {total_lessons}: {lesson_title}

EXAM SPECIFICATION (relevant extract):
<spec>
{spec_extract — the section of the spec that maps to this lesson's content}
</spec>

QUESTION TYPES FOR THIS EXAM BOARD:
{question_type_spec — e.g. "1x Identify (1 mark), 1x State (2 marks), ..."}

QUESTION TYPE NAMES (must use these exact strings in the "type" field):
{question_type_names — e.g. "4 marks — Costume Design", "8 marks — Extended Explanation"}

SOURCE MATERIAL FROM TEACHER:
<source>
{extracted_ppt_text — the slides/pages relevant to this lesson}
</source>

PAST PAPERS AND MARK SCHEMES (extract real questions where relevant):
<past_papers>
{extracted past paper text — question papers and mark schemes from the source material}
</past_papers>

STRUCTURAL REFERENCE (an existing lesson from StudyVault for format guidance):
<example>
{content_html from an existing live lesson — shows the exact HTML patterns to follow}
</example>

Generate the complete lesson as a JSON object.
```

---

## Planning Prompt

Before content generation, Claude analyses the spec + source material to create a lesson plan. This is a separate API call.

```
You are analysing teacher resources and an exam board specification to create a structured lesson plan for StudyVault, a GCSE revision website.

SUBJECT: {subject_name}
EXAM BOARD: {exam_board} ({spec_code})

<spec>
{full spec text or relevant sections}
</spec>

<source_material>
{extracted PPT/doc text}
</source_material>

<past_papers>
{extracted past paper and mark scheme text}
</past_papers>

Create a lesson plan that:

1. CALIBRATES LESSON COUNT: The number of lessons must reflect the subject's content density and exam weighting — NOT a 1:1 mapping of spec bullet points to lessons. Use these benchmarks:

   EXISTING SUBJECTS (for calibration):
   - History (AQA, 4 units): 60 lessons — rich narrative topics (wars, social change) needing 15 lessons/unit
   - Geography (AQA, 2 papers): 40 lessons — mixed narrative + conceptual, 20 lessons/paper
   - Business (Edexcel, 2 themes): 30 lessons — applied concepts, 15 lessons/theme
   - Drama (OCR, 2 components): 12 lessons — text study + devising, 6 lessons/component
   - Sport Science (OCR, 1 unit): 10 lessons — factual/conceptual
   - Food Technology (AQA, 1 unit): 10 lessons — applied knowledge
   - Religious Education (AQA, 8 sections): 40 lessons — conceptual/comparison topics, 5 lessons/section

   RULES FOR CALIBRATION:
   - Subjects with short conceptual topics (RE beliefs, science facts) need FEWER lessons with MORE topics combined per lesson. A spec bullet like "Nature of God" is a paragraph, not a full lesson.
   - Subjects with rich narrative topics (history events, drama texts) need MORE lessons because each topic has depth, chronology, and case studies.
   - Combine related spec topics into single substantive lessons (e.g. "Zakah AND Sawm" as one lesson, not two).
   - Consider the STUDENT'S total revision load: they study 8-10 GCSEs. If every subject has 60 lessons, that's 500+ lessons to revise. Keep it manageable.
   - Target: 5-8 lessons per unit/section for conceptual subjects, 10-20 for narrative-heavy subjects.
   - Each lesson should have enough material for 800-1500 words of content. If a spec topic only generates 200 words, combine it with related topics.

2. MAPS TO THE SPEC: Group lessons by the exam's component/section structure. Allocate lesson count proportional to mark weighting (e.g. a 50-mark section gets more lessons than a 30-mark section).

3. COVERS ALL SPEC REQUIREMENTS: Every assessable topic in the spec must appear in at least one lesson. Flag any spec requirements that have no matching source material.

4. USES THE SOURCE MATERIAL: Map each lesson to specific slides/pages from the teacher's resources. Include ppt_section_markers for each lesson.

5. IDENTIFIES PAST PAPER COVERAGE: Note which past paper questions are relevant to each lesson.

Return a JSON object:
{
  "subject_name": "...",
  "subject_slug": "...",
  "exam_board": "...",
  "spec_code": "...",
  "units": [
    {
      "name": "Section/Component Name",
      "slug": "section-name",
      "subtitle": "Brief description for browse page",
      "lesson_count": N,
      "lessons": [
        {
          "number": 1,
          "title": "Lesson Title",
          "description": "One sentence for browse card (60-100 chars)",
          "ppt_section_markers": ["keywords to locate relevant PPT content"],
          "spec_references": ["spec section numbers or topic names"],
          "relevant_past_papers": ["OCR June 2024 Q1", "OCR November 2021 Q3"]
        }
      ]
    }
  ],
  "question_type_names": ["4 marks — Type Name", "8 marks — Type Name"],
  "gaps": ["Spec topics with no source material coverage"]
}
```

---

## Exam Technique Guide Prompt

After content generation, guides are generated for each question type. One API call per guide.

```
You are generating an exam technique guide page for StudyVault, a GCSE revision website.

SUBJECT: {subject_name} ({exam_board} {spec_code})
QUESTION TYPE: {question_type_name} [{marks} marks]
SET TEXT / CONTEXT: {set_text_or_context}

<mark_scheme_examples>
{real mark scheme level descriptors from past papers for this question type}
</mark_scheme_examples>

Generate a guide page as HTML (no JSON wrapper — just content_html) that includes:

1. WHAT THE QUESTION ASKS: Explain what this question type requires in plain language.
2. HOW MARKS ARE ALLOCATED: Include real level descriptors from the mark scheme.
3. STEP-BY-STEP METHOD: Numbered steps for answering this question type.
4. TIMING: How long to spend on this question in the exam.
5. MODEL ANSWER: A strong example answer (in a collapsible section).
6. WEAK ANSWER: A weak example showing common mistakes (in a collapsible section).
7. COMMON MISTAKES: 3-4 bullet points of what to avoid.
8. KEY TERMINOLOGY: Terms students should use in their answers.

Use the same HTML components as lessons: <h2>, <p>, <div class="key-fact">, <div class="collapsible">, etc.
Do NOT include data-narration-id attributes (guides don't have narration).
```

---

## Revision Technique Guide Prompt

Standard revision technique guides adapted per subject. One API call per guide. Hub index generated separately.

```
You are generating a revision technique guide page for StudyVault, a GCSE revision website.

SUBJECT: {subject_name} ({exam_board} {spec_code})
TECHNIQUE: {technique_name}

Generate a guide page as HTML (no JSON wrapper — just content_html) that includes:

1. WHAT IT IS: Explain the technique in plain language for a 15-16 year old.
2. WHY IT WORKS: Brief cognitive science explanation (1-2 paragraphs max).
3. HOW TO DO IT: Step-by-step instructions with subject-specific examples.
4. EXAMPLE: A worked example using real content from this subject (in a collapsible section).
5. COMMON MISTAKES: 2-3 bullet points of what students get wrong.
6. QUICK START: A "try it now" prompt — one concrete action the student can do immediately.

Use the same HTML components as lessons: <h2>, <p>, <div class="key-fact">, <div class="collapsible">, etc.
Do NOT include data-narration-id attributes (guides don't have narration).

Standard techniques (adapt examples for each subject):
- Retrieval Practice
- Spaced Repetition
- Interleaving
- Dual Coding
- Elaborative Interrogation
- Knowledge Organisers
- Timed Exam Practice

Add one subject-specific technique where appropriate (e.g. "Practising Calculations" for Business).
```

---

## Related Media

Related media curation is handled by `RELATED_MEDIA_PIPELINE.md`. That document contains the full prompt, category structure, HTML patterns, and link conventions. The orchestration code reads it and injects it into the Claude API call for Step 5.

---

## What the teacher/Tom can tweak

| Layer | What it controls | How to change |
|-------|-----------------|---------------|
| System prompt — quality standards | Readability target, source fidelity rules | Edit this file |
| System prompt — output format | HTML components, narration IDs, word count targets | Edit this file |
| System prompt — question rules | Mark scheme format, question count, past paper extraction | Edit this file or QUESTIONS_PIPELINE.md |
| Planning prompt — lesson structure | How lessons are grouped, weighted, and named | Edit this file |
| User message — spec extract | What spec content is fed per lesson | Improve spec mapping in the planning step |
| User message — source material | Which PPT slides map to which lesson | Improve the planning step's section markers |
| User message — past papers | Which past paper questions are fed per lesson | Improve past paper to lesson mapping |
| User message — structural example | Which existing lesson is used as format reference | Pick a different exemplar lesson |
| Question type config | Mark allocations per exam board | Edit the QUESTION_SPECS and QUESTION_TYPE_NAMES configs |
| Diagram generation | Pictorial style, colour palettes, QC process | Edit DIAGRAM_PIPELINE.md |
| Related media curation | Categories, link rules, deduplication | Edit RELATED_MEDIA_PIPELINE.md |
| Narration config | Voices, format, R2 hosting | Edit NARRATION_PIPELINE.md |

---

## Question Type Config (per exam board)

```javascript
// Mark allocations — injected into the user message
const QUESTION_SPECS = {
  'AQA': '6 questions: 1x Define (1 mark), 1x Describe (2), 1x Explain (4), 1x Explain (6), 1x Evaluate (9), 1x Extended (12+4 SPaG)',
  'Edexcel': '6 questions: 1x Define (1 mark), 1x Outline (2), 2x Explain (3 each), 1x Discuss (6), 1x Justify/Evaluate (9 or 12)',
  'OCR': '6 questions: 1x Identify (1 mark), 1x State (2), 1x Describe (3), 1x Explain (4), 1x Extended response (6), 1x Discuss (8, QWC)',
  'OCR Drama': '6 questions matching the actual exam paper format — see question_type_names from the planning step',
  'WJEC': '6 questions: 1x Identify (1 mark), 1x Describe (2), 1x Explain (4), 1x Explain (6), 1x Assess (8), 1x Extended (12)',
};

// Exact type name strings — MUST match getGuideUrl() mappings in main.js
// These are generated during the planning step from the spec and past papers
const QUESTION_TYPE_NAMES = {
  'OCR Drama': [
    '4 marks — Costume Design',
    '4 marks — Voice Skills',
    '4 marks — Physicality',
    '4 marks — Staging Type',
    '4 marks — Lighting Design',
    '4 marks — Sound Design',
    '8 marks — Extended Explanation',
    '8 marks — Set Design',
    '30 marks — Section B Essay',
  ],
  // Add per subject as new subjects are built
};
```

---

## Post-Generation Validation Checklist

Run after every lesson is generated, before writing to Supabase:

```
 JSON is valid and parseable
 All required keys present: description, content_html, exam_tip_html, conclusion_html, practice_questions, knowledge_checks, glossary_terms
 description is 60-100 characters
 content_html has sequential data-narration-id (n1, n2, n3... no gaps)
 At least 2 <div class="key-fact"> in content_html
 At least 2 <div class="collapsible"> in content_html
 At least 3 <dfn class="term"> in content_html
 Exactly one <!-- DIAGRAM --> placeholder in content_html (at a content-relevant location, not near the top)
 Exactly 6 practice_questions with fields: text, type, marks (all strings)
 Every practice question "type" matches a registered question_type_name
 Exactly 5 knowledge_checks (2 mcq + 2 fill + 1 match)
 All glossary_terms match <dfn> elements in content_html
 No <h1> tags in content_html
 HTML entities used correctly (&amp; &mdash; &rsquo; &ldquo; &rdquo;)
 Word count 800-1500 (excluding HTML tags)
```

---

## Full Pipeline Checklist (one-shot subject build)

Everything that must be generated for a complete subject. Steps reference their specialist docs.

**Planning:**
- [ ] Spec downloaded/loaded from library
- [ ] Lesson plan created with spec references, PPT markers, past paper mapping
- [ ] Lesson plan includes unit subtitles and lesson descriptions
- [ ] Question type names defined and registered in getGuideUrl()
- [ ] CSS colour classes added to style.css (light + dark mode)

**Per-lesson content (this file's prompts):**
- [ ] Content HTML with narration IDs
- [ ] Practice questions (with past paper tags where available)
- [ ] Knowledge checks (2 MCQ + 2 fill + 1 match)
- [ ] Glossary terms
- [ ] Exam tip
- [ ] Conclusion / key takeaways
- [ ] Lesson description for browse cards

**Per-lesson assets (parallel — see specialist docs):**
- [ ] Hero image (Wikimedia Commons, landscape, >50KB, with caption + alt text)
- [ ] Related media (see RELATED_MEDIA_PIPELINE.md)
- [ ] Diagram (see DIAGRAM_PIPELINE.md)

**Per-lesson narration (after content + diagrams — see NARRATION_PIPELINE.md):**
- [ ] TTS clips for every narration ID (Azure Speech, Ollie odd / Bella even)
- [ ] MP3s uploaded to R2
- [ ] Narration manifest with R2 URLs and durations

**Subject-level pages:**
- [ ] Exam technique hub + one guide per question type (including extended response guides)
- [ ] Revision technique hub + 7-8 standard guides adapted for this subject
- [ ] Subject activated on homepage (active: true, url, detail, colour)
- [ ] Subject card image (from Wikimedia or existing)
- [ ] Browse page: colour theme, unit cards with images, scrolling quote ticker
- [ ] Unit subtitles set in database

**Validation:**
- [ ] All lessons pass the post-generation checklist
- [ ] Visit tracking works (unit slug in select query)
- [ ] Practice question guide links work (getGuideUrl mappings)
- [ ] Narration player works on all lessons
- [ ] Related media has no duplicate resources across lessons in same unit
- [ ] All R2 URLs return HTTP 200
