# Subject Build — Ralph Loop Prompt

<!--
  INSTRUCTIONS: Copy this file, fill in the 4 variables below, then run:
  /ralph-loop "$(cat SUBJECT_PROMPT.md)" --max-iterations 80 --completion-promise "BUILD_COMPLETE"
-->

<!-- ━━━ FILL THESE IN ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ -->
**Subject:** [e.g. Religious Studies]
**Exam board & spec code:** [e.g. AQA 8062]
**Colour 1 (Unit/Paper 1):** [e.g. #7c3aed purple]
**Colour 2 (Unit/Paper 2):** [e.g. #0891b2 cyan]
<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ -->

## Your task

Build a complete GCSE revision subject for StudyVault. Read `SUBJECT_PLAYBOOK.md` for the full reference, then execute the phases below in order.

## Critical rules

1. **Source material is king.** All lesson content MUST come from the teacher's PPTs and spec documents in `Spec and Materials/{Subject}/`. Extract text first with `python -m markitdown`. Do NOT write generic revision content from general knowledge — every fact, case study, date, name and statistic must trace back to the source material or the exam board spec.
2. **Read existing lessons as your template.** Look at `business/theme-1/lesson-01.html` and `geography/paper-1/lesson-01.html` for exact HTML structure, component patterns, sidebar layout. Copy the patterns precisely.
3. **Track progress.** Write and update `{subject}/BUILD_PROGRESS.md` after each phase so you can resume if interrupted. Record: which phase you're on, what's done, what's left.
4. **Run QA after every phase.** Write `{subject}/validate.py` in Phase 3 and run it after every subsequent phase. Fix all failures before moving on.
5. **Never hardcode API keys.** Use `os.environ['GEMINI_API_KEY']` for Gemini calls. Grep all files for key patterns before signalling completion.

## Phases

### Phase 1: Research & Plan
1. Extract all PPTs in `Spec and Materials/{Subject}/` to `_extracted_text/`
2. Read every extracted file to understand the full content
3. Research the exam board's spec structure and question types (use WebSearch if needed)
4. Write `{subject}/BUILD_PLAN.md`: lesson list with titles, spec refs, unit mapping
5. Derive 6-shade colour palettes per unit from the provided accent colours
6. Decide naming conventions (body classes, data attributes, folder names)

**Done when:** `BUILD_PLAN.md` exists with complete lesson plan.

### Phase 2: CSS & Scaffolding
1. Add unit colour classes to `css/style.css`
2. Create all folders: `{subject}/`, units, exam-technique, revision-technique
3. Add subject to root `index.html` picker with `active: true`

**Done when:** Folders exist, CSS defined, subject in picker.

### Phase 3: Lesson HTML
For every lesson in the plan:
1. Read the relevant source material (PPTs/extracted text) for this lesson
2. Generate a complete lesson HTML file using the existing template structure
3. Include: article content with sequential `data-narration-id`, 2-3 key facts, collapsibles, glossary terms (`<dfn>`), exam tip, conclusion
4. Include: 6 practice questions matching the exam board's question types, 5 knowledge checks (2 MCQ + 2 fill + 1 match), empty narration manifest
5. Ensure correct prev/next nav and CSS/JS paths

Then write `{subject}/validate.py` — a real, runnable validation script that checks:
- Every lesson has 6 practiceQuestions, 5 knowledgeCheck (correct type mix)
- Sequential narration IDs with no gaps
- Required elements: exam-tip, conclusion, lesson-nav, hero placeholder, sidebar
- Correct CSS/JS paths
- Prev/next links point to existing files
- At least 2 glossary terms and 2 key-fact divs per lesson

Run it. Fix all failures. Re-run until clean.

**Done when:** `validate.py` exits with code 0.

### Phase 3b: Supporting Pages
1. Subject landing page with unit cards
2. Unit index pages listing every lesson
3. Exam technique hub + one guide per question type (purple theme)
4. Revision technique hub + 7-8 guides (green theme) + subject-specific guide if relevant

Add link validation checks to `validate.py`. Run it.

**Done when:** `validate.py` exits with code 0 including link checks.

### Phase 4: Hero Images
1. Write a Wikimedia download script (User-Agent, 3-5s delays, >50KB check, landscape preference)
2. Download heroes for every lesson, save attributions to JSON
3. Insert into HTML (between lesson-header and a11y-toolbar, `object-position: center 50%`)
4. Add hero checks to `validate.py` (file exists, >50KB, has alt+figcaption)

Run validation.

**Done when:** `validate.py` exits with code 0 including hero checks.

### Phase 5: MPL Diagrams
1. Plan chart type variety — assign a type to each lesson (max 25% tiles)
2. Write generation script with unit colour palette
3. Generate all diagrams, insert into HTML (after first key-fact)
4. Add diagram checks to `validate.py` (file exists, variety logged)

Run validation.

**Done when:** `validate.py` exits with code 0 including diagram checks.

### Phase 6: Gemini Concept Diagrams
1. Decide which lessons benefit from a textbook illustration (not all will)
2. Write generation script using `gemini-3.1-flash-image-preview` and `$GEMINI_API_KEY`
3. Prompts must include "MINIMAL arrows", "no overlapping text", explicit spatial directions
4. Insert before exam-tip, 15+ lines from other images
5. Audit for redundancy with MPL diagrams — change one if they show the same concept

**Done when:** All referenced diagram files exist. No MPL/Gemini redundancy.

### Phase 7: Related Media
1. For every lesson, research specific podcasts, movies, TV, documentaries, study tools
2. Use WebSearch to find real links, WebFetch to verify they work
3. Every link must go to specific content (episode, movie page, topic page) — never a channel
4. Insert into sidebar, omitting empty categories
5. Add media checks to `validate.py`

**Done when:** `validate.py` exits with code 0 including media checks.

### Phase 8: Subject Card Images
1. Download 1-2 Wikimedia landscape photos for `images/subject-{subject}-{n}.jpg`
2. Verify root index.html references them correctly

**Done when:** Card images exist and display in subject picker.

### Phase 9: Final Validation
1. Run `validate.py` — all checks must pass
2. Grep every file in `{subject}/` for API key patterns: `AIzaSy`, `sk-ant-`, `sk-`
3. Verify no `.py` scripts inside `{subject}/` except `validate.py`
4. Verify `BUILD_PROGRESS.md` shows all phases complete

If ALL checks pass, output:

<promise>BUILD_COMPLETE</promise>

If any check fails, fix the issue and retry. Do NOT output the completion promise until every check passes.
