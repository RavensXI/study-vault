# StudyVault — New Subject Build Playbook

Runbook for adding a new GCSE subject to StudyVault. Content is generated via the pipeline and stored in Supabase. All lessons are served dynamically from the database.

For the pipeline architecture, see `PIPELINE_ARCHITECTURE.md`. For prompt details, see `GENERATION_PROMPT.md`.

---

## MANDATORY CHECKLIST — every new subject must have ALL of these

Before marking a subject as complete, verify every item:

- [ ] **Subject created** in Supabase with correct slug, exam_board, spec_code, school_id, settings
- [ ] **Units created** with slug, name, subtitle, body_class, accent colours, lesson_count, sort_order
- [ ] **All lessons generated** with content_html, practice_questions (6), knowledge_checks (5), flashcard_questions (5), glossary_terms
- [ ] **Hero images** on every lesson (Unsplash → R2 → `lessons.hero_image_url`)
- [ ] **Unit images** on every unit (`units.image_url` — use Unsplash or copy from first lesson hero)
- [ ] **Quote ticker** in `subjects.settings.quote_ticker_html` (5-6 subject-relevant quotes, full HTML structure)
- [ ] **Narration** on every lesson (Azure TTS → R2 → `lessons.narration_manifest`). Exception: Maths practice format has no narration.
- [ ] **Podcasts** on every lesson (NotebookLM → R2 → `lessons.podcast_url` or related_media)
- [ ] **Related media** on every lesson (2-3 verified YouTube URLs in `lessons.related_media`)
- [ ] **Guide pages** — exam technique + revision technique (in `guide_pages` table)
- [ ] **Homepage card** in `index.html` with subject image, accent colour, lesson count
- [ ] **Picker item** in `index.html` (for school subjects shown in the subject picker)
- [ ] **Foundation/Higher wrapping** if tiered subject (Science, Languages, Maths) — `<div class="higher-only">` on HT sections

This checklist exists because agents consistently forget unit images, quote tickers, and homepage cards. Do NOT skip these steps.

---

## Two Build Modes

### Mode 1: Bespoke (teacher uploads resources)
Teacher provides PPTs/resources → pipeline generates content tailored to their teaching materials + the spec. Result: school-specific content with `school_id` set.

### Mode 2: Generic (spec-only, no teacher resources)
Pipeline generates content directly from the exam specification. No teacher input needed. Result: free-tier content with `school_id = NULL`. This is how we build content at scale for every GCSE subject.

---

## Automated Lesson Planning (Generic Mode)

When building from a spec with no teacher resources, the pipeline must determine lesson count and unit structure automatically.

### Step 1: Identify exam vs coursework components
Read the spec and determine which components are externally examined. **Only generate revision content for examined components.** Coursework/NEA/controlled assessment components are excluded — students don't revise for those in the same way.

### Step 2: Scale lesson count by exam weight and subject type

| Subject type | Exam weight | Lesson range | Examples |
|-------------|------------|--------------|---------|
| Core subjects | 100% | 40-55 lessons | Maths, English Lang, English Lit, Combined Science |
| Full GCSE options (100% exam) | 100% | 25-35 lessons | History, Geography, RE, Languages, Business |
| GCSE with coursework | 50-60% exam | 15-25 lessons | Art & Design, D&T, Food, Drama, Music, PE |
| Vocational (BTEC/Cambridge Nat) | 40% exam | 10-15 lessons | H&SC, Sport Science, Creative iMedia, H&C |

Core subjects get more content because:
- They carry more weight in Progress 8 and school accountability
- Students have more teaching time allocated (typically 7-8 hours/fortnight vs 4-5 for options)
- The exams are longer and cover more content

### Step 3: Structure units from the spec
- Each exam paper or major spec section becomes a unit
- Topics within each paper become lessons
- Aim for 5-10 lessons per unit (too few = sparse, too many = overwhelming)
- If a paper has 15+ topics, group related topics into combined lessons

### Step 4: Propose the plan
Present the unit/lesson breakdown to Tom for review before generating. Format:
```
Subject: {name} ({board} {code})
Exam weight: {X}%
Proposed: {N} lessons across {M} units

Unit 1: {name} ({X} lessons)
  L1: {title}
  L2: {title}
  ...
```

Tom reviews and adjusts if needed ("too many", "combine these", "split this"). Then generate.

---

## Prerequisites

### Bespoke builds (Mode 1):
1. **Subject name, exam board & spec code** (e.g. "Religious Studies, AQA 8062")
2. **Source material** — teacher PPTs, textbook extracts, or spec documents. Upload via `/admin/pipeline`.
3. **Colour theme** — one accent colour per unit/paper

### Generic builds (Mode 2):
1. **Subject name, exam board & spec code** only
2. Spec loaded from `specs/{board}/{slug}-{code}.md` (193 specs pre-indexed)
3. Colour theme chosen by the activation agent

---

## Specification Database

193 GCSE specifications from all 4 exam boards, pre-converted to markdown with YAML frontmatter.

- **Location:** `specs/{board}/{slug}-{code}.md`
- **Index:** `specs/index.json` — maps board + subject + spec_code to file path
- **Boards:** AQA (48), Edexcel (37), OCR (42), WJEC (32), Eduqas (34)
- **Script:** `python scripts/download_specs.py` — re-downloads and converts all specs
- **Usage:** Look up by exam board + subject slug or spec code. The full spec markdown is fed to content generation agents as context.

---

## One-Shot Build Flow

**CRITICAL: Execute autonomously. Never stop to ask the user for permission between steps. The entire flow runs without pausing.**

### Phase 1: Setup (T=0)

**Bespoke:** Teacher uploads PPTs via `/admin/pipeline`. Claude Code finds the job:
```bash
python scripts/pipeline_generate.py info <job_id>
python scripts/pipeline_generate.py text <job_id>
```

**Generic:** No upload needed. Read the spec directly from the database.

Look up the spec from `specs/index.json`. Match by exam board + subject/spec code. The markdown spec files are in `specs/{board}/{slug}-{code}.md` with YAML frontmatter. If the spec isn't in the database, download it with `python scripts/download_specs.py --board {board}`.

**The spec is the authority, not the teacher resources.** The lesson plan MUST cover every topic and theme in the exam spec, even if the teacher's uploaded resources don't include material for all of them. Teacher resources are the primary source for content and emphasis, but if the spec lists a topic and there are no PPTs for it, the lesson must still be generated using the spec as the source. Students need full coverage of the spec to revise effectively — gaps in teacher uploads cannot become gaps in the revision content.

### Phase 1b: Activation BEFORE Content (T=30s)

**CRITICAL — run the CSS + subject activation agent FIRST**, before launching content agents. This agent creates the units in Supabase with their accent colours. The content generation script (`pipeline_api_generate.py generate`) reads unit accents from the DB to include in diagram prompts. If units don't exist yet, diagrams default to grey.

| Agent | Depends on | Count |
|-------|-----------|-------|
| CSS + subject activation agent | Subject slug + colour | 1 |

**The activation agent MUST do ALL of the following:**
1. Create subject + units + empty lesson shells in Supabase
2. Add CSS body class variables (`.unit-{subject}-N`) for light + dark mode in `css/style.css`
3. **Add the subject card to `index.html`** — both the `.home-card` in the subject grid AND the `.picker-item` in the subject picker modal. Download a subject image from Unsplash to `images/subject-{slug}.jpg`.
4. Set `subjects.settings` (quote ticker HTML, unit_image_positions)
5. **Add the subject slug to `SUBJECT_ORDER`** in `scripts/generate_cinematic_videos.py` — without this, the podcast/video script can't find the subject.

**Quote ticker notes for MFL subjects:** Quotes should be in the target language WITH an English translation after a slash (e.g. "El que lee mucho, sabe mucho" / "He who reads a lot, knows a lot" — Cervantes). Mix proverbs with quotes from famous figures from that language's culture (authors, artists, scientists, athletes). Students need to understand the quotes, and famous figures add cultural knowledge.

If any of these are missed, the subject won't appear on the homepage even though lessons exist in Supabase.

Wait for this to complete (~30 seconds), then proceed to Phase 2.

### Phase 2: Maximum Parallel Launch (T=1 min)

**Launch ALL of the following as parallel background agents in a SINGLE message:**

| Agent | Depends on | Count |
|-------|-----------|-------|
| Lesson content agents (**max 10 lessons per agent**) | Plan + unit accents in DB | varies |
| Exam technique guides agent | Question types from plan | 1 |
| Revision technique guides agent | Subject name only | 1 |
| getGuideUrl mapping agent | Question type strings | 1 |

**CRITICAL guide rules:**
- **USE THE TEMPLATES:** Guide agents MUST use `docs/EXAM_TECHNIQUE_TEMPLATE.md` and `docs/REVISION_TECHNIQUE_TEMPLATE.md` as their HTML structure. Agents fill in `{{PLACEHOLDER}}` values with subject-specific content. They do NOT invent their own HTML structure, class names, or layouts. This prevents the formatting drift that occurs when agents generate HTML from scratch.
- Guides MUST be split into separate agents. Max ~5 guide pages per agent (including hub). Split as: (1) exam hub + first 4 guides, (2) remaining 4 exam guides, (3) revision hub + 3 foundation guides, (4) 5 remaining revision guides (subject-specific + exam prep). That's 4 guide agents total for MFL subjects.
- Each guide agent MUST create a hub/index page (slug `index`, sort_order 0) that links to all individual guide pages. Without the hub page, guide-loader shows "No hub page found".
- The subject-specific section should contain techniques unique to that subject (e.g. for MFL: vocab building, grammar drilling, listening/speaking practice; for Science: equation practice, required practicals).
- **Guide hub colours are FIXED across all subjects:** Revision technique hubs always use green (`--paper-accent: #16a34a; --paper-light: #f0fdf4;`) for ALL sections. Exam technique hubs always use purple (`--paper-accent: #7c3aed; --paper-light: #f5f3ff;`) for ALL sections. These do NOT vary by subject.
- **All guide page links MUST use full absolute paths** — e.g. `/guide/spanish/exam-technique/dictation`, NOT bare slugs like `dictation.html` or `dictation`. Bare slugs resolve incorrectly with the guide-loader URL scheme. Never use `{subject}` or `{slug}` placeholders — use the actual subject slug.
- Always use `<main>` + `<aside class="lesson-sidebar">` structure. Look at an existing History exam guide for the exact HTML.

**Why this works:** Guides and mappings do NOT depend on lesson content. They only need the plan (question types, subject slug). Launch them at the same time as content generation.

Each lesson content agent uses the **Write tool** (not bash heredocs) to create its temp JSON, then runs `pipeline_generate.py write`. The Write tool handles all escaping natively.

### Phase 3: Per-Lesson Streaming (T=1+ min, as each content agent completes)

**Assets can be launched early** — `run-all-assets` now auto-detects new lessons that arrive while it's running and re-runs heroes + diagrams for them. No need to wait for all content agents to finish before starting assets.

**After diagrams complete, ALWAYS run diagram QA** — download all diagrams and visually review them using the Read tool. Check for: correct accent colour, accurate text/labels, readable layout, relevant to lesson topic. Flag any that need regeneration. Do NOT skip this step. The API-based QA (`claude_qa.py`) is disabled — QA must be done by Claude Code reviewing the images directly.

For each completed lesson, launch in parallel:
- `generate_diagrams.py --job-id <id> --lessons <N>` (background)
- `download_heroes.py --job-id <id> --lessons <N>` (background)
- `generate_narration.py --job-id <id> --lessons <N>` (background, after diagrams — or accept slight narration ID risk)
- 1 media curation agent for lesson N (background, sonnet)

**This means:** By the time L10's content finishes, L1-L9's assets may already be done. A stuck lesson only blocks itself, not the other 9.

### Supervisor Responsibilities

While agents run, actively monitor:
1. **Check for stuck agents** — if a content agent has produced zero output after 3 minutes, kill and relaunch it
2. **Launch downstream immediately** — don't accumulate completions. As each notification arrives, fire that lesson's assets + media in the same response
3. **Track progress** — periodically run `pipeline_generate.py status <job_id>` to see overall state
4. **Handle failures** — if an asset script fails for one lesson, note it and move on. Don't block other lessons.

### Phase 4: Commit + Push

When all flags are green (or all automated ones — media may still be running):
```bash
python scripts/pipeline_generate.py status <job_id>   # Verify flags
```

**Set unit images** — each unit needs an `image_url` for the browse page cards. Use lesson 1's hero image:
```python
for unit in units:
    l1 = sb.table('lessons').select('hero_image_url').eq('unit_id', unit['id']).eq('lesson_number', 1).single().execute()
    sb.table('units').update({'image_url': l1.data['hero_image_url']}).eq('id', unit['id']).execute()
```

**Content-specific revision tips** — every `<div class="key-fact">` must have a `data-revision-tip` attribute with a specific recall task tailored to that key fact's content. This should be generated during content creation (in the lesson JSON). If not generated at creation time, run the batch tip script afterwards. Generic tips like "Cover this and recall" are NOT acceptable — each tip must reference the actual content.

Then commit and deploy:
```bash
git add / commit / push                                # Deploy to Vercel
```

### Target Timeline (streaming)

```
T=0    Plan + pipeline steps
T=0    PARALLEL: 10 content agents + guides + CSS + getGuideUrl
T=1    First content lands → immediately launch its assets + media
T=2    More content landing → each triggers its own assets + media
T=3    Supervisor detects stuck agent → kill + relaunch
T=5    All content done. Most assets already running or finished.
T=12   Last narration finishes. All flags green.
T=12   Commit, push, live.
```

**Target: 10-lesson subject in ~12 minutes** with streaming. Benchmarks: 36 min (run 1, sequential), 21:49 (run 3, streaming with one stuck agent). Streaming eliminates the wait-for-all-content bottleneck.

### Execution Rules

1. **Never ask permission** — execute the full pipeline autonomously once the user says "go"
2. **Launch all agents in single batches** — never launch 3 then wait then launch 7 more
3. **Use the Write tool for JSON files** — not bash heredocs (shell escaping issues)
4. **Maximise parallelism** — if task B doesn't depend on task A's output, run them together
5. **Media runs alongside assets, not after** — this saves ~10 minutes
6. **STRICT: Maximum 10 lessons per content agent.** Agents generating more than ~15 lessons in a single batch produce thin/templated content for later lessons. Split into batches of 8-10 and run in parallel instead. Quality > speed.

### Model Selection

Use the `model` parameter on Agent tool calls. **Opus for anything that touches code or lesson quality. Cheaper models for everything else.**

| Task | Model | Why |
|------|-------|-----|
| Lesson content agents | **opus** | Quality-critical — content accuracy, HTML structure, exam alignment |
| Exam technique guides | **sonnet** | Templated writing, no code changes |
| Revision technique guides | **sonnet** | Templated writing, no code changes |
| Media curation agents | **sonnet** | Haiku produces inconsistent JSON structures that crash lesson-loader. Sonnet is reliable. |
| CSS + subject activation | **opus** | Touches code — must get it right first time |
| getGuideUrl mappings | **opus** | Touches code |

### Agent Prompt Requirements (lessons learned from QA)

**Revision techniques should be chosen per subject during planning.** Consider what content types the subject has (memorisation-heavy? analysis-heavy? practical skills?) and pick techniques that genuinely suit it. Not every subject needs the same set.

**Current limitation (TODO: refactor):** `initRevisionTips()` in main.js hardcodes three lightbulb tip links for ALL subjects: `retrieval-practice` (on `.key-fact`), `dual-coding` (on `.timeline`), `elaborative-interrogation` (on `.collapsible`). Until refactored to read from `subjects.settings.revision_tip_mappings`, these three slugs MUST exist to avoid 404s. Additional subject-specific techniques beyond these three are encouraged.

**Planned fix:** Store `revision_tip_mappings` in `subjects.settings` mapping CSS selectors to technique slug/label/tip text. `initRevisionTips()` reads from settings (passed via lesson-loader) instead of hardcoded array. Each subject gets bespoke lightbulb tips.

**All guide pages MUST use this HTML structure** (required by `guide-loader.js`):
```html
<main class="lesson-content">
  <!-- guide content here -->
</main>
<aside class="lesson-sidebar">
  <div class="guide-quick-ref">...</div>
  <div class="guide-other">...</div>
</aside>
```
Hub index pages use a different structure (`guide-hub` div, no `<main>`/`<aside>`).

**CSS/activation agent MUST set these Supabase fields** (pipeline_generate.py write does NOT set them):
- `subjects.settings.quote_ticker_html` — scrolling quotes. MUST use the full HTML structure (not bare spans):
  ```html
  <div class="quote-ticker"><div class="quote-ticker-track">
  <span class="quote-item" style="--q-color: #ACCENT;">"Quote" <em>— Author</em></span>
  ...duplicate first 2 quotes at end for seamless loop...
  </div></div>
  ```
- `units.accent` / `accent_light` / `accent_badge` — the correct colour (pipeline_generate.py only sets colour on first create, not updates)
- `units.image_url` — a hero image URL to show on the unit card on the browse page
- `units.subtitle` — description text for the browse card
- `units.body_class` — CSS class name (e.g. `unit-food-technology-1`)

**CRITICAL — two pitfalls found in Music pipeline (Mar 2026):**
1. **Settings must be a dict, NOT a JSON string.** Supabase-py auto-serialises dicts to jsonb. If you do `{"settings": json.dumps({...})}` it double-serialises and the frontend gets a string instead of an object. The quote ticker silently fails. Always write: `{"settings": {"quote_ticker_html": "..."}}`
2. **Unit `image_url` must be set explicitly.** It's not set by the generation step or the assets step. After heroes are generated, run `pipeline_api_generate.py activate <job_id>` to copy each unit's first lesson hero image to `units.image_url` and verify settings format.

**Post-generation safety net:** `python scripts/pipeline_api_generate.py activate <job_id>` — fixes settings format, sets unit images from hero images, verifies all required fields.

**Media curation agents MUST write this exact JSON structure** to `lessons.related_media` (lesson-loader.js crashes on any other format):
```json
[
  {
    "category": "Videos & Channels",
    "emoji": "&#127909;",
    "items": [
      {"title": "Video Title", "url": "https://...", "description": "Why this is useful"}
    ]
  },
  {
    "category": "Documentaries",
    "emoji": "&#127916;",
    "items": [
      {"title": "Film Title (Year)", "url": "https://www.justwatch.com/uk/movie/...", "description": "..."}
    ]
  },
  {
    "category": "Study Tools",
    "emoji": "&#128218;",
    "items": [
      {"title": "Site Name — Topic", "url": "https://...", "description": "..."}
    ]
  }
]
```
Each object MUST have `category` (string), `emoji` (HTML entity), and `items` (array of objects with `title`, `url`, `description`). Empty categories should be omitted, not included with empty items arrays. Max 3 items per category.

**Media curation agents MUST search beyond study tools.** Include:
- Movies and documentaries (search JustWatch UK). Examples: Super Size Me, Fed Up, What the Health for nutrition topics.
- Podcasts (search Spotify for specific episodes, not just channels).
- Don't settle for only BBC Bitesize + Seneca + YouTube — push for varied, engaging content.

**Hero images:** `download_heroes.py` checks the hero image index (`data/hero-image-index.json`) first for reusable images before searching Unsplash/Wikimedia. Matches scoring ≥4 are reused directly (no download). New images are automatically added to the index after upload. Use `--no-reuse` to force fresh searches. Alt text should be descriptive (not just the lesson title).

**Diagrams:** No figcaption needed — alt text is sufficient. `generate_diagrams.py` no longer adds captions.

**Lessons are created with `status: 'live'`** — no manual approval step needed during generation.

### Manual Scripts (for individual reruns)
```bash
python scripts/generate_diagrams.py --job-id <uuid> [--lessons 1,2,3] [--dry-run]
python scripts/download_heroes.py --job-id <uuid> [--lessons 1,2,3] [--dry-run] [--no-reuse]
python scripts/generate_narration.py --job-id <uuid> [--lessons 1,2,3] [--dry-run]
```

---

## Content Quality: The Most Important Thing

The single most important requirement is that **lesson content is bespoke to the subject and exam board, built from the teacher's source material**.

This means:
- All content must come from the teacher's PPTs and the exam spec — not general knowledge
- Map each lesson directly to spec references
- Include specific case studies, examples, dates, names, and statistics from the source material
- Use the exam board's terminology and question phrasing
- Practice questions must match the exam board's actual question types and mark allocations
- Do NOT write generic revision content — students can get that anywhere

If a lesson's source material is thin, flag it rather than padding with generic content.

### Language Subjects (French, German, Spanish)

Language subject content has an additional requirement: **all foreign-language text MUST be wrapped in `<em>` or `<strong>` HTML tags**. This is how the narration pipeline auto-detects phrases that need SSML `<lang>` wrapping for correct pronunciation.

- Use `<em>` for foreign sentences and phrases (e.g. `<em>Je m'appelle Claude</em>`)
- Use `<strong>` for individual vocabulary words (e.g. `<strong>le chien</strong>`)
- The `generate_narration.py` script checks the subject slug against `SUBJECT_LANG_CODES` in `scripts/lib/narration.py` and automatically applies the correct language code (`fr-FR`, `de-DE`, `es-ES`)
- No manual SSML editing is needed — the pipeline handles everything if the HTML tags are correct
- Content agents generating language lessons must be explicitly told to use `<em>` and `<strong>` for foreign text

---

## Post-Generation Validation

Run after every lesson is generated, before writing to Supabase:

```
✓ JSON is valid and parseable
✓ All required keys present: description, content_html, exam_tip_html, conclusion_html,
  practice_questions, knowledge_checks, glossary_terms, diagram_prompt, hero_keywords
✓ description is 60-100 characters
✓ content_html has sequential data-narration-id (n1, n2, n3... no gaps)
✓ At least 2 <div class="key-fact"> in content_html
✓ At least 2 <div class="collapsible"> in content_html
✓ At least 3 <dfn class="term"> in content_html
✓ Exactly 6 practice_questions with fields: text, type, marks
✓ Every practice question "type" matches a registered question_type_name
✓ Exactly 5 knowledge_checks (2 mcq + 2 fill + 1 match)
✓ All glossary_terms match <dfn> elements in content_html
✓ Exactly one <!-- DIAGRAM --> placeholder in content_html (at a content-relevant location, not near the top)
✓ No <h1> tags in content_html
✓ Word count 800-1500 (excluding HTML tags)
✓ diagram_prompt is a complete Gemini prompt (not a placeholder)
✓ hero_keywords has 3-4 search terms (primary + fallbacks)
```

---

## What the Teacher Does After

One pass through every lesson on the live site to check:
- Hero image positions (~30% need `object-position` tweaks via `/admin/images`)
- Gemini diagram quality (arrows, clarity, relevance — can regenerate via `/admin/images`)
- Any content issues that jump out (edit via `/admin/review`)

---

## Pipeline Progress Tracking

The `pipeline_steps` table tracks 7 flags per lesson:

| Flag | Set by |
|------|--------|
| `content_done` | `pipeline_generate.py write` |
| `questions_done` | `pipeline_generate.py write` |
| `glossary_done` | `pipeline_generate.py write` |
| `diagrams_done` | `generate_diagrams.py` |
| `hero_done` | `download_heroes.py` |
| `narration_done` | `generate_narration.py` |
| `media_done` | Claude Code (manual) |

Asset metadata stored per-step:
- `diagram_prompt` — full Gemini prompt (written during content generation)
- `hero_keywords` — Wikimedia search terms array
- `subject_slug` — cached for quick lookups
- `diagram_style` — `'gemini_only'` (default) or `'matplotlib_gemini'`

View progress: `pipeline_generate.py status <job_id>` or `/admin/pipeline` UI.

---

## Common Pitfalls

| Pitfall | Prevention |
|---------|-----------|
| Generic content not from source material | Read PPTs first, map every fact to spec reference |
| Gemini arrows everywhere | "MINIMAL arrows" in diagram prompt, specify exact count |
| Made-up chart data | Factual data only; use concept illustrations when no real numbers |
| Wikimedia 429 rate limiting | 3-5 second delays between requests (built into script) |
| Portrait hero images | Wikimedia search filters for landscape during download |
| API key in committed files | Read from env var, grep before committing |
| Generic media links | Episode/page-specific only, verified with WebFetch |
| Wrong Gemini model | `gemini-3.1-flash-image-preview` (Nano Banana 2) |
| Windows encoding crashes | `sys.stdout.reconfigure(encoding='utf-8')` in all scripts |
| Missing diagram_prompt | Validate JSON output includes diagram_prompt before writing |
| Grey/wrong diagram colours | Run activation agent BEFORE content generation so unit accents are in DB. `pipeline_api_generate.py` reads accents from `units` table. If not found, falls back to grey `#6b7280` |
| Empty hero_keywords | Derive from lesson title as fallback — script handles this |
| Diagrams clustered at top | Content HTML must include `<!-- DIAGRAM -->` at content-relevant spot |
| Diagram inside collapsible | Placeholder must be between sections, not inside collapsibles |
