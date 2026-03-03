# Content Generation Pipeline — Full Architecture

How teacher resources become complete revision lessons. Documents the dependency graph, parallelisation strategy, and prompt structure for each step.

---

## Dependency Graph

```
1. PLAN (spec + PPTs → lesson structure)
   │   Sequential — everything depends on this
   ▼
2. CONTENT (per-lesson: HTML + questions + KC + glossary)
   │   Sequential per lesson — but L2 content can start while L1 assets run
   ▼
   ┌─── 3. DIAGRAMS ───────┐
   ├─── 4. HERO IMAGES ────┤  These 3 run IN PARALLEL per lesson
   └─── 5. RELATED MEDIA ──┘  None depend on each other
   │
   ▼   Must wait for content + diagrams (diagram placement affects narration IDs)
6. NARRATION (reads final HTML → TTS per element → upload to R2)
```

---

## Execution Flow (12-lesson subject)

```
Plan ──────────────────────────────────────────────────────────►
  │
  ├─ Content L1 ─► [Diagrams L1 | Heroes L1 | Media L1] ─► Narration L1
  ├─ Content L2 ─► [Diagrams L2 | Heroes L2 | Media L2] ─► Narration L2
  ├─ Content L3 ─► [Diagrams L3 | Heroes L3 | Media L3] ─► Narration L3
  │  ...
  └─ Content L12 ► [Diagrams L12 | Heroes L12 | Media L12] ► Narration L12
```

Content generation is sequential (each lesson is one API call, ~30-60s).
Asset generation (diagrams/heroes/media) starts per-lesson as soon as that lesson's content is done.
Narration runs last per-lesson, after all assets are placed in the HTML.

**Rolling pipeline:** L1 assets generate while L2 content generates. No step waits for all lessons to finish before the next step begins.

---

## Steps in Detail

### Step 1: Plan

**Input:** Spec document + extracted PPT text + exam board config
**Output:** Lesson plan JSON (units, lessons, titles, spec references, PPT section markers)
**Model:** Claude (single call)
**Duration:** ~30-60s

The plan maps teacher content against the spec:
- Groups content into units matching the exam structure
- Decides lesson count based on spec weighting (e.g. 50-mark section gets more lessons than 30-mark section)
- Maps each lesson to specific spec references and PPT slide ranges
- Identifies gaps (spec requirements with no PPT coverage — flagged for the teacher)

### Step 2: Content

**Input:** Spec extract for this lesson + PPT sections + example lesson HTML + question type config
**Output:** JSON with content_html, exam_tip_html, conclusion_html, practice_questions, knowledge_checks, glossary_terms
**Model:** Claude (one call per lesson)
**Duration:** ~30-60s per lesson
**Prompt:** See `docs/GENERATION_PROMPT.md`

This is the core generation step. The system prompt encodes all quality standards, HTML formatting rules, and pedagogical approach. The user message provides the spec, source material, and structural example.

### Step 3: Diagrams

**Input:** Lesson title, content summary, unit colour palette
**Output:** One diagram per lesson (JPEG on R2)
**Model:** Gemini `gemini-3.1-flash-image-preview` for pictorial isotype; matplotlib for data-driven charts
**Duration:** ~30-60s per lesson
**Runs in parallel with:** Hero images, related media

Two sub-approaches depending on subject:
- **Data-driven subjects** (History, Geography, Business): Research real statistics → matplotlib baseline → Gemini pictorial transform
- **Non-data subjects** (Drama, English): Gemini concept illustrations (character maps, stage layouts, timeline graphics)

Diagram is placed at a content-relevant location in the HTML (not always at the top). Placement updates the content_html and may shift narration IDs — this is why narration must run after diagrams.

### Step 4: Hero Images

**Input:** Lesson title, topic keywords
**Output:** One hero image per lesson (JPEG on R2)
**Source:** Wikimedia Commons API (real photographs only, never AI-generated)
**Duration:** ~10-20s per lesson (download + compress)
**Runs in parallel with:** Diagrams, related media

Search Wikimedia for landscape photographs relevant to the lesson topic. Download with User-Agent header, 3-5s delays between requests. Verify >50KB. Save attribution. Default position: `object-position: center 50%`. ~30% will need manual position tweaks by Tom during QA.

### Step 5: Related Media

**Input:** Lesson title, subject, topic
**Output:** Curated sidebar links (JSON array of categories with items)
**Model:** Claude with web search
**Duration:** ~30-60s per lesson
**Runs in parallel with:** Diagrams, hero images

Research real external resources per lesson:
- **Podcasts** — specific episode links (not channel homepages)
- **Videos & Channels** — YouTube videos on the topic
- **Movies / TV / Documentaries** — JustWatch UK links
- **Study Tools** — BBC Bitesize, Seneca, subject-specific sites

Every link must be verified. Empty categories are omitted. Max 3 items per category. See `docs/RELATED_MEDIA_PIPELINE.md` for full conventions.

### Step 6: Narration

**Input:** Final content_html (with diagrams placed), lesson number (odd/even for voice selection)
**Output:** MP3 clips on R2 + narration manifest JSON
**Service:** Azure Speech REST API (region: uksouth)
**Duration:** ~2-5s per clip, ~60-120s per lesson
**Must run after:** Content + diagrams (narration IDs must be final)

Extracts text from each `data-narration-id` element in the HTML. Generates one MP3 per element using Azure Speech:
- Odd lessons → `en-GB-OllieMultilingualNeural` (male)
- Even lessons → `en-GB-BellaNeural` (female)
- Format: 24kHz, 96kbps, mono MP3

Uploads clips to R2 (`studyvault-audio` bucket). Builds manifest with R2 URLs and durations. Updates lesson record in Supabase.

---

## Prompt Assembly

Each pipeline step assembles its prompt from docs on disk plus per-lesson data from Supabase. The orchestration code (API route or Claude Code) reads the `.md` files and injects them into the API call. The model cannot read files itself — everything it needs must be in the message.

### Assembly per step

**Step 1 — Plan:**
```javascript
const planningPrompt = readFile('docs/GENERATION_PROMPT.md'); // Planning Prompt section
const specText = readFile(specPath);
const pptText = extractPptText(pptPaths);
const pastPaperText = extractPastPapers(pastPaperPaths);

const message = assemblePrompt(planningPrompt, {
  specText,
  pptText,
  pastPaperText
});

const plan = await claude.messages.create({ messages: [message] });
```

**Step 2 — Content (per lesson):**
```javascript
const systemPrompt = readFile('docs/GENERATION_PROMPT.md');   // System Prompt section
const lessonTemplate = readFile('docs/LESSON_TEMPLATE.md');
const questionRules = readFile('docs/QUESTIONS_PIPELINE.md');
const specExtract = getSpecForLesson(plan, lessonNumber);
const pptExtract = getPptForLesson(plan, lessonNumber);
const pastPapers = getPastPapersForLesson(plan, lessonNumber);
const exampleLesson = getExampleLessonHtml();

const message = assemblePrompt(systemPrompt, {
  lessonTemplate,
  questionRules,
  specExtract,
  pptExtract,
  pastPapers,
  exampleLesson
});

const lesson = await claude.messages.create({ messages: [message] });
```

**Step 3 — Diagrams (per lesson):**
```javascript
const diagramPrompt = readFile('docs/DIAGRAM_PIPELINE.md');   // prompt template + style rules
const lessonSummary = summariseLesson(lesson.content_html);
const colourPalette = getSubjectPalette(subjectSlug);

// Step 3a: matplotlib baseline (no LLM — Python script)
await runScript('scripts/generate_{subject}_diagrams.py', lessonNumber);

// Step 3b: Gemini pictorial transform
const matplotlibImage = readImage(matplotlibPath);
const geminiPrompt = buildDiagramPrompt(diagramPrompt, lessonSummary, colourPalette);
const diagram = await gemini.generateContent({ prompt: geminiPrompt, image: matplotlibImage });

// Step 3c: QC agent review (up to 3 iterations)
await qcReview(diagram, matplotlibImage, geminiPrompt);
```

**Step 4 — Hero Images (per lesson):**
```javascript
// No LLM prompt — direct Wikimedia API search
const keywords = extractKeywords(lesson.title, lesson.content_html);
const image = await wikimediaSearch(keywords);
await downloadAndCompress(image, outputPath);
```

**Step 5 — Related Media (per lesson):**
```javascript
const mediaPrompt = readFile('docs/RELATED_MEDIA_PIPELINE.md');  // agent prompt template
const lessonTitle = lesson.title;
const topicSummary = lesson.description;
const previousMedia = getPreviousLessonMedia(subjectSlug);  // for deduplication

const message = assemblePrompt(mediaPrompt, {
  lessonTitle,
  topicSummary,
  previousMedia
});

const media = await claude.messages.create({ messages: [message], tools: ['web_search'] });
```

**Step 6 — Narration (per lesson):**
```javascript
// No LLM — deterministic TTS via Azure Speech REST API
// Config comes from NARRATION_PIPELINE.md (read by the script, not sent to a model)
const voice = (lessonNumber % 2 === 1) ? 'en-GB-OllieMultilingualNeural' : 'en-GB-BellaNeural';
const elements = extractNarrationElements(finalContentHtml);

for (const element of elements) {
  const mp3 = await azureSpeech.synthesize(element.text, { voice, format: 'mp3-96kbps-24khz' });
  await uploadToR2(mp3, `${subject}/${unit}/narration_lesson-${nn}_${element.id}.mp3`);
}
```

**Exam Technique Guides:**
```javascript
const guidePrompt = readFile('docs/GENERATION_PROMPT.md');  // Exam Technique section
const markSchemes = getMarkSchemesForType(questionType);

const message = assemblePrompt(guidePrompt, { markSchemes });
const guide = await claude.messages.create({ messages: [message] });
```

**Revision Technique Guides:**
```javascript
const guidePrompt = readFile('docs/GENERATION_PROMPT.md');  // Revision Technique section
const techniqueName = 'Retrieval Practice';  // or whichever technique

const message = assemblePrompt(guidePrompt, { techniqueName, subjectName });
const guide = await claude.messages.create({ messages: [message] });
```

### Key principles

- **Single source of truth:** each doc owns its domain. Content rules live in GENERATION_PROMPT.md, diagram rules in DIAGRAM_PIPELINE.md, etc. Never duplicate between files.
- **Inject, don't reference:** the model cannot follow file references. The orchestration code must read the full doc and paste it into the message.
- **Spec + source material from Supabase:** the planning step stores `spec_extract` and `ppt_section_markers` per lesson. The content step retrieves these and injects them.
- **Example lesson from DB:** fetch `content_html` from an existing live lesson in the same subject (or History as fallback) for structural reference.

---

## Commercial API Routes (future)

When moved to Vercel serverless with Claude API:

```
POST /api/pipeline/plan           → Claude API call
POST /api/pipeline/generate       → Claude API call (per lesson)
POST /api/pipeline/diagrams       → Gemini API call (per lesson)
POST /api/pipeline/heroes         → Wikimedia API (per lesson)
POST /api/pipeline/media          → Claude API + web search (per lesson)
POST /api/pipeline/narration      → Azure Speech API (per lesson)
GET  /api/pipeline/status         → Returns progress for all steps
```

The browser orchestrates the rolling pipeline:
1. Call `/plan`, wait for response
2. For each lesson: call `/generate`, wait, then fire `/diagrams` + `/heroes` + `/media` in parallel
3. When all three asset calls return for a lesson, call `/narration`
4. Update progress UI after each call completes

Each route uses the service key for Supabase writes. Auth verified via JWT or demo header.

**Script-to-API mapping:**

| Script | Future API Route |
|--------|-----------------|
| `generate_narration.py` | `POST /api/pipeline/narrate` |
| `generate_diagrams.py` | `POST /api/pipeline/diagrams` |
| `download_heroes.py` | `POST /api/pipeline/heroes` |
| Claude Code media curation | `POST /api/pipeline/media` |

---

## Claude Code Mode (current, Max plan)

Same pipeline, but Claude Code executes all steps autonomously. **Never pause to ask for permission between steps — run the full pipeline end-to-end once the user says "go".**

### Execution order (maximise parallelism)

**Phase 1 — Setup (~1 min):**
1. Find job: `pipeline_generate.py info {job_id}` + `text {job_id}`
2. Read spec from `Spec and Materials/` via `python -m markitdown`
3. Create lesson plan + pipeline steps in Supabase

**Phase 2 — Maximum parallel launch (~5 min):**
Launch ALL of these as background agents in a **single message**:
- N lesson content agents (one per lesson, using Write tool for JSON + `pipeline_generate.py write`)
- 1 exam technique guides agent (only needs question types from plan)
- 1 revision technique guides agent (only needs subject name)
- 1 CSS + subject activation + homepage picker agent (only needs slug + colour)
- 1 getGuideUrl mapping agent (only needs question type strings)

**Phase 3 — Assets + media in parallel (~10-15 min):**
When content agents complete, launch simultaneously:
- `pipeline_generate.py run-all-assets {job_id}` (background) — diagrams + heroes parallel, then narration
- N media curation agents (one per lesson, all at once) — web search doesn't depend on assets

**Phase 4 — Commit + deploy:**
When all flags are green: commit CSS/JS changes, push to Vercel.

### Key rules
- **Never ask, just execute** — stopping for permission adds minutes of wasted round-trips
- **Launch all agents in single batches** — never stagger (3 now, 7 later)
- **Use Write tool for JSON files** — not bash heredocs (shell escaping breaks on HTML content)
- **Media runs alongside assets** — media only needs lesson titles, not diagrams/heroes/narration
- **Guides and CSS run alongside content** — they don't depend on lesson HTML

### Target: 10-lesson subject in under 20 minutes

**Asset scripts (subject-agnostic, all accept `--job-id`):**
- `scripts/generate_diagrams.py` — reads `diagram_prompt` from pipeline_steps, calls Gemini, uploads to R2
- `scripts/download_heroes.py` — reads `hero_keywords` from pipeline_steps, searches Wikimedia, uploads to R2
- `scripts/generate_narration.py` — extracts text from lesson HTML, Azure Speech TTS, uploads to R2
- `scripts/pipeline_generate.py assets {job_id}` — shows per-lesson asset completion table

See `docs/SUBJECT_PLAYBOOK.md` for the full execution playbook with timing targets.

---

## Estimated Timelines

**Claude Code mode (with full parallelism):**

| Subject size | Phase 2 (content + guides + CSS) | Phase 3 (assets + media parallel) | Total |
|-------------|----------------------------------|-----------------------------------|-------|
| 10 lessons | ~5 min | ~13 min | ~18 min |
| 15 lessons | ~7 min | ~18 min | ~25 min |
| 30 lessons | ~12 min | ~25 min | ~37 min |

**Benchmark:** Food Technology (10 lessons) first build took 36 minutes with suboptimal ordering. With full parallelism (guides/CSS alongside content, media alongside assets), target is under 20 minutes.

Narration is always the bottleneck — it runs sequentially per lesson (~8-12 min for 10 lessons). Everything else parallelises well.

---

## Quality Gates

After generation, before going live:

1. **Automated checks** (run by pipeline):
   - Every lesson has 6 practice questions, 5 knowledge checks
   - Sequential narration IDs with no gaps
   - At least 2 key facts, 2 collapsibles, 3 glossary terms per lesson
   - All referenced image/audio files exist on R2
   - No API keys in generated content

2. **Tom's QA review** (via admin/review.html):
   - Hero image positions (~30% need tweaking)
   - Diagram quality and relevance
   - Content accuracy against source material
   - Exam tip usefulness
   - Related media link verification

3. **Teacher review** (future, via self-service editor):
   - Content matches their teaching approach
   - Correct emphasis on topics they prioritise
   - School-specific context added where needed
