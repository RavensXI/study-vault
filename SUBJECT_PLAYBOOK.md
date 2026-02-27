# StudyVault — New Subject Build Playbook

Automated runbook for adding a new GCSE subject to StudyVault. Designed to be executed via a Ralph Wiggum loop with minimal teacher intervention.

For HTML patterns, component structure, and sidebar layout — read existing lessons in `business/theme-1/lesson-01.html` or `geography/paper-1/lesson-01.html` as live reference. Copy from what's already built.

---

## Prerequisites

Before starting a build, the teacher MUST provide:

1. **Subject name, exam board & spec code** (e.g. "Religious Studies, AQA 8062")
2. **Source material** in `Spec and Materials/{Subject}/` — teacher PPTs, textbook extracts, or spec documents. These are the primary content source. **No source material = no build.**
3. **Colour theme** — two accent colours (one per unit/paper)

Extract text from PPTs before starting: `python -m markitdown "file.pptx"`. Store extracted text in `Spec and Materials/{Subject}/_extracted_text/`.

---

## Running the Build

### Quick start

1. Ensure source material is in `Spec and Materials/{Subject}/`
2. Copy `SUBJECT_PROMPT.md` and fill in the blanks (subject name, exam board, colours)
3. Run:
```bash
/ralph-loop "$(cat SUBJECT_PROMPT.md)" --max-iterations 80 --completion-promise "BUILD_COMPLETE"
```
4. When the loop finishes, review images in browser and provide hero position/replacement feedback
5. Apply image fixes (manually or with a short follow-up session)
6. Commit and push

### What the loop does

The Ralph loop executes 9 phases sequentially. Each phase has a QA check that must pass before moving on. If QA fails, the loop self-corrects and retries. Progress is tracked in `{subject}/BUILD_PROGRESS.md` so the loop survives restarts.

### What the teacher does after

One pass through every lesson in the browser to check:
- Hero image positions (expect ~30% need `object-position` tweaks)
- Hero image replacements (expect ~15% need different photos)
- Gemini diagram quality (arrows, clarity, relevance)
- Any content issues that jump out

Everything else — lesson content, practice questions, knowledge checks, MPL diagrams, related media, exam/revision technique pages — should be done by the loop.

---

## Phase Reference

### Phase 1: Research & Plan
- Read ALL source material in `Spec and Materials/{Subject}/`
- Read the exam board spec to determine unit structure, lesson count, question types
- Draft `{subject}/BUILD_PLAN.md` with: lesson list, spec references, colour palettes, question types
- Decide naming: body classes, data attributes, folder structure

**QA:** `BUILD_PLAN.md` exists with all lessons mapped to spec references.

### Phase 2: CSS & Scaffolding
- Add unit colour classes to `css/style.css` (follow existing patterns)
- Create folder structure
- Update root `index.html` subject picker

**QA:** Folders exist. CSS classes defined. Subject appears in picker.

### Phase 3: Lesson HTML
Generate every lesson from the source material. This is the most critical phase.

**Content rules:**
- Every lesson MUST be built from the teacher's source material and spec — not from general knowledge
- Cross-reference PPTs for specific facts, dates, names, case studies, statistics
- Content must be bespoke to this exam board's spec, not generic revision notes
- GCSE readability: short sentences, active voice, concrete examples, age 15-16
- Each lesson needs: article content with narration IDs, 2-3 key facts, collapsibles, glossary terms, exam tip, conclusion, 6 practice questions (exam board format), 5 knowledge checks (2 MCQ + 2 fill + 1 match)

**QA (run validation script):**
```
✓ Every lesson file exists
✓ Every lesson has exactly 6 practiceQuestions
✓ Every lesson has exactly 5 knowledgeCheck (2 MCQ + 2 fill + 1 match)
✓ Every lesson has sequential data-narration-id (n1, n2, n3... no gaps)
✓ Every lesson has exam-tip, conclusion, lesson-nav
✓ Every lesson has correct CSS/JS paths (../../css/style.css, ../../js/main.js)
✓ Every lesson has window.narrationManifest = []
✓ Prev/next nav links point to files that exist
✓ At least 2 glossary <dfn> terms per lesson
✓ At least 2 key-fact divs per lesson
```

### Phase 3b: Supporting Pages
- Subject landing page (`{subject}/index.html`)
- Unit index pages with lesson cards
- Exam technique: hub + one guide per question type (purple theme)
- Revision techniques: hub + 7-8 guides (green theme), add subject-specific one if relevant

**QA:**
```
✓ Unit index pages list every lesson
✓ Subject landing links to every unit index
✓ Exam technique guides exist for every question type in practiceQuestions
✓ All internal links resolve to existing files
```

### Phase 4: Hero Images
- Write batch download script using Wikimedia Commons API
- User-Agent: `StudyVault/1.0 (educational)`, 3-5s delays, verify >50KB
- Prefer landscape orientation (wider than tall)
- Save attributions to `{subject}/hero_attributions.json`
- Insert into HTML between lesson-header and a11y-toolbar
- Default position: `object-position: center 50%`

**DO NOT use AI-generated heroes — real photographs only.**

**QA:**
```
✓ Every lesson has <figure class="lesson-hero-image">
✓ Every referenced hero file exists on disk and is >50KB
✓ Every hero has alt text and figcaption with attribution
```

### Phase 5: Matplotlib Diagrams
- Plan chart type variety BEFORE generating — assign types across all lessons
- Maximum 25% tile/card layouts. Prefer: bar, line, grouped bar, stacked bar, matrix, pyramid, donut
- One diagram per lesson, placed after first key-fact
- Data must be factual — never invent statistics. Use tiles/flows when no real numbers exist
- Unit colour palette: 6 shades dark→light, shadow, title colour

**QA:**
```
✓ Every lesson has at least one <figure class="diagram">
✓ Every referenced diagram file exists on disk
✓ No more than 25% tile/card layouts
✓ Chart type distribution is varied (log types used per lesson)
```

### Phase 6: Gemini Concept Diagrams (Selective)
- Only where a textbook illustration adds genuine value (cross-sections, processes, maps, spatial diagrams)
- Model: `gemini-3.1-flash-image-preview` — API key from `$GEMINI_API_KEY` env var
- Prompt must include: "MINIMAL arrows", "no overlapping text", explicit spatial positions
- Place before exam-tip, 15+ lines from other images
- Audit for redundancy with MPL — each must show different content

**QA:**
```
✓ All referenced Gemini diagram files exist on disk
✓ No lesson has MPL and Gemini showing the same concept
```

### Phase 7: Related Media
- Research lesson-specific media for every lesson (use WebSearch + WebFetch to verify)
- Categories: Podcasts (episode links), Movies (JustWatch UK), TV Shows (JustWatch UK), Documentaries (JustWatch UK), Study Tools (BBC Bitesize, Seneca, subject-specific sites)
- Every link must go to specific content — NEVER a channel or homepage
- Verify every link with WebFetch before inserting
- Omit empty categories

**QA:**
```
✓ Every lesson has <div class="sidebar-section sidebar-media">
✓ No link points to a channel homepage or generic page
✓ Study Tools includes at least one subject-specific link per lesson
```

### Phase 8: Subject Card Images
- Download 1-2 landscape photos from Wikimedia for `images/subject-{subject}-{n}.jpg`
- Same download rules as heroes (User-Agent, delays, >50KB)

**QA:**
```
✓ Subject card images exist in images/ folder
✓ Root index.html references them correctly
```

### Phase 9: Final QA & Signal
- Run FULL validation script across all checks
- Grep all files for API key patterns (`AIzaSy`, `sk-ant-`, `sk-`) — must find zero
- Verify no Python generation scripts are staged in git
- If all pass, output the completion promise

---

## Validation Script

The loop must write and run an actual Python validation script at `{subject}/validate.py`. This is not pseudocode — it must execute and report pass/fail for every check listed in the phases above.

The script should:
1. Parse every lesson HTML file with regex or html.parser
2. Check for required elements, correct counts, file existence
3. Print a clear PASS/FAIL report per lesson
4. Exit with code 0 (all pass) or 1 (any failures)
5. On failure, print exactly what's wrong and in which file

The loop should run this script after each phase and fix any failures before moving on.

---

## Content Quality: The Most Important Thing

The single most important requirement is that **lesson content is bespoke to the subject and exam board, built from the teacher's source material**.

This means:
- Read every PPT and extracted text file in `Spec and Materials/{Subject}/`
- Map each lesson directly to spec references
- Include the specific case studies, examples, dates, names, and statistics from the source material
- Use the exam board's terminology and question phrasing
- Practice questions must match the exam board's actual question types and mark allocations
- Do NOT write generic revision content from general knowledge — students can get that anywhere

If a lesson's source material is thin, flag it in `BUILD_PROGRESS.md` rather than padding with generic content.

---

## Common Pitfalls

| Pitfall | Prevention |
|---------|-----------|
| Generic content not from source material | Read PPTs first, map every fact to spec reference |
| All MPL diagrams are tile cards | Assign chart types upfront — max 25% tiles |
| Gemini arrows everywhere | "MINIMAL arrows", specify exact count/direction |
| Made-up chart data | Factual data only; tiles/flows when no real numbers |
| MPL + Gemini show same thing | Audit every dual-diagram lesson |
| Wikimedia 429 rate limiting | 3-5 second delays between requests |
| Wikimedia returns HTML not JPEG | Always set User-Agent header |
| Portrait hero images | Filter for landscape during download |
| API key in committed files | Read from env var, grep before completion |
| Generic media links | Episode/page-specific only, verified with WebFetch |
| Wrong Gemini model | `gemini-3.1-flash-image-preview` (Nano Banana 2) |
| Windows encoding crashes | `sys.stdout.reconfigure(encoding='utf-8')` in all scripts |
