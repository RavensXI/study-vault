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

### Step 1: Upload & Parse
Teacher uploads PPTs via `/admin/pipeline`. The web UI:
- Uploads files to Supabase Storage (`pipeline-uploads` bucket)
- Extracts text from PPTs (serverless parser)
- Creates an `upload_job` with extracted text and subject config

### Step 2: Plan & Generate Content
In Claude Code:
```bash
python scripts/pipeline_generate.py info <job_id>
python scripts/pipeline_generate.py text <job_id>
```

Claude Code reads the spec + extracted PPT text, then generates each lesson's JSON (content, questions, knowledge checks, glossary, plus `diagram_prompt` and `hero_keywords` for asset scripts).

```bash
# Write each lesson to Supabase
python scripts/pipeline_generate.py write <job_id> <unit_slug> <lesson_number> _temp_lesson.json
```

### Step 3: Asset Generation
Run all assets autonomously:
```bash
python scripts/pipeline_generate.py run-all-assets <job_id>
```

This orchestrates:
1. **Diagrams + Heroes in parallel** — `generate_diagrams.py` reads `diagram_prompt` from pipeline_steps, calls Gemini; `download_heroes.py` reads `hero_keywords`, searches Wikimedia
2. **Narration (sequential, after diagrams)** — `generate_narration.py` extracts text from lesson HTML, generates Azure Speech TTS, uploads MP3s to R2

Or run individually:
```bash
python scripts/generate_diagrams.py --job-id <uuid> [--lessons 1,2,3] [--dry-run]
python scripts/download_heroes.py --job-id <uuid> [--lessons 1,2,3] [--dry-run]
python scripts/generate_narration.py --job-id <uuid> [--lessons 1,2,3] [--dry-run]
```

### Step 4: Related Media
Claude Code curates related media via web search (scripts can't do this). For each lesson:
- Research podcasts, videos, movies, TV, documentaries, study tools
- Write via `SupabaseWriter.update_related_media()`, then mark `media_done=true` on the pipeline step

See `RELATED_MEDIA_PIPELINE.md` for category rules and link conventions.

### Step 5: Exam & Revision Technique Guides
Claude Code generates guide pages via `SupabaseWriter.upsert_guide()`:
- Exam technique hub + one guide per question type
- Revision technique hub + 7-8 standard guides adapted for the subject

### Step 6: Subject Activation
- Add CSS colour classes to `css/style.css` (light + dark mode)
- Update `subjects` table: `is_active: true`, set `settings` jsonb (quote ticker, unit images)
- Update root `index.html` subject picker
- Register question type names in `getGuideUrl()` mapping in `js/main.js`

### Step 7: QA Review
```bash
python scripts/pipeline_generate.py review <job_id>
```

Then use `/admin/review` to QC each lesson and `/admin/images` to adjust hero image positions.

### Step 8: Check Progress
```bash
python scripts/pipeline_generate.py status <job_id>   # Summary with asset flags
python scripts/pipeline_generate.py assets <job_id>    # Detailed per-lesson table
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
