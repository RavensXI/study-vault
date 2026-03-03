# StudyVault — New Subject Build Playbook

Runbook for adding a new GCSE subject to StudyVault. Content is generated via the pipeline and stored in Supabase. All lessons are served dynamically from the database.

For the pipeline architecture, see `PIPELINE_ARCHITECTURE.md`. For prompt details, see `GENERATION_PROMPT.md`.

---

## Prerequisites

Before starting a build, the teacher MUST provide:

1. **Subject name, exam board & spec code** (e.g. "Religious Studies, AQA 8062")
2. **Source material** — teacher PPTs, textbook extracts, or spec documents. Upload via `/admin/pipeline`.
3. **Colour theme** — one accent colour per unit/paper

---

## One-Shot Build Flow

**CRITICAL: Execute autonomously. Never stop to ask the user for permission between steps. The entire flow runs without pausing.**

### Phase 1: Setup (T=0)

Teacher uploads PPTs via `/admin/pipeline`. Claude Code finds the job:
```bash
python scripts/pipeline_generate.py info <job_id>
python scripts/pipeline_generate.py text <job_id>
```

Read the spec from `Spec and Materials/` (use `python -m markitdown`). Create the lesson plan and pipeline steps in Supabase.

### Phase 2: Maximum Parallel Launch (T=1 min)

**Launch ALL of the following as parallel background agents in a SINGLE message:**

| Agent | Depends on | Count |
|-------|-----------|-------|
| Lesson content agents (one per lesson) | Plan | 10-30 |
| Exam technique guides agent | Question types from plan | 1 |
| Revision technique guides agent | Subject name only | 1 |
| CSS + subject activation agent | Subject slug + colour | 1 |
| getGuideUrl mapping agent | Question type strings | 1 |

**Why this works:** Guides, CSS, and mappings do NOT depend on lesson content. They only need the plan (question types, subject slug, colour). Launch them at the same time as content generation.

Each lesson content agent uses the **Write tool** (not bash heredocs) to create its temp JSON, then runs `pipeline_generate.py write`. The Write tool handles all escaping natively.

### Phase 3: Assets + Media in Parallel (T=5 min, when content lands)

**As soon as all content agents complete, launch TWO things simultaneously:**

```
Background: python scripts/pipeline_generate.py run-all-assets <job_id>
Parallel:   10 media curation agents (one per lesson, all at once)
```

**Why this works:** Media curation (web search for podcasts, videos, study tools) does NOT depend on diagrams, heroes, or narration. It only needs lesson titles/topics. Run it alongside asset generation, not after.

### Phase 4: Commit + Push (T=15-18 min)

When media agents and assets both finish:
```bash
python scripts/pipeline_generate.py status <job_id>   # Verify all flags green
git add / commit / push                                # Deploy to Vercel
```

### Target Timeline

```
T=0    Plan + pipeline steps
T=1    PARALLEL: content agents + guides + CSS + getGuideUrl
T=5    Content done → PARALLEL: run-all-assets + media agents
T=12   Media done
T=18   Narration finishes (slowest asset). All flags green.
T=18   Commit, push, live.
```

**For a 10-lesson subject, target is under 20 minutes.** The first Food Tech build took 36 minutes due to sequential execution and unnecessary pauses. The optimised flow above eliminates both.

### Execution Rules

1. **Never ask permission** — execute the full pipeline autonomously once the user says "go"
2. **Launch all agents in single batches** — never launch 3 then wait then launch 7 more
3. **Use the Write tool for JSON files** — not bash heredocs (shell escaping issues)
4. **Maximise parallelism** — if task B doesn't depend on task A's output, run them together
5. **Media runs alongside assets, not after** — this saves ~10 minutes

### Model Selection

Use the `model` parameter on Agent tool calls. **Opus for anything that touches code or lesson quality. Cheaper models for everything else.**

| Task | Model | Why |
|------|-------|-----|
| Lesson content agents | **opus** | Quality-critical — content accuracy, HTML structure, exam alignment |
| Exam technique guides | **sonnet** | Templated writing, no code changes |
| Revision technique guides | **sonnet** | Templated writing, no code changes |
| Media curation agents | **haiku** | Web search + write JSON to Supabase. No creative writing, no code. |
| CSS + subject activation | **opus** | Touches code — must get it right first time |
| getGuideUrl mappings | **opus** | Touches code |

### Agent Prompt Requirements (lessons learned from QA)

**Revision technique guides MUST include these three slugs** (hardcoded in main.js lightbulb tips):
- `retrieval-practice` — linked from `.key-fact` elements
- `dual-coding` — linked from `.timeline` elements
- `elaborative-interrogation` — linked from `.collapsible` elements
Plus any additional techniques. If these three are missing, lightbulb links will 404.

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

**CSS/activation agent MUST set `subjects.settings`** jsonb with:
- `quote_ticker_html` — scrolling quotes for the browse page header
- `unit_image_positions` — hero image positions for unit cards on browse page
Also set the unit's `description` field for the browse card subtitle.

**Media curation agents MUST search beyond study tools.** Include:
- Movies and documentaries (search JustWatch UK). Examples: Super Size Me, Fed Up, What the Health for nutrition topics.
- Podcasts (search Spotify for specific episodes, not just channels).
- Don't settle for only BBC Bitesize + Seneca + YouTube — push for varied, engaging content.

**Hero images:** Alt text should be descriptive (not just the lesson title). `download_heroes.py` now cleans the Wikimedia filename into a readable caption.

**Diagrams:** No figcaption needed — alt text is sufficient. `generate_diagrams.py` no longer adds captions.

**Lessons are created with `status: 'live'`** — no manual approval step needed during generation.

### Manual Scripts (for individual reruns)
```bash
python scripts/generate_diagrams.py --job-id <uuid> [--lessons 1,2,3] [--dry-run]
python scripts/download_heroes.py --job-id <uuid> [--lessons 1,2,3] [--dry-run]
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
| Empty hero_keywords | Derive from lesson title as fallback — script handles this |
