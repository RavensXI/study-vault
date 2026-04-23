# StudyVault Content Pipeline

Master playbook for adding any new GCSE subject. This is the entry point — specialist docs are linked from the relevant phases below.

Replaces the older `SUBJECT_PLAYBOOK.md` and `PIPELINE_ARCHITECTURE.md`. Written for a world where we build every GCSE subject across every board, not just Unity-bespoke.

---

## Two questions every subject build starts with

1. **Free-tier or Unity bespoke?** Determines `school_id` and feature matrix below.
2. **Which units are article-format, which are practice-format?** Planning agent decides per unit using the heuristic in `PLANNING_PROMPT.md`. Mixed subjects (article + practice in the same subject) are fine — Geography already does this.

| Feature | Free-tier | Unity bespoke |
|---|---|---|
| `school_id` | `NULL` | set |
| Initial `status` | `pending_review` | `live` |
| Hero images | ✓ | ✓ |
| Narration (Azure TTS) | ✓ | ✓ |
| Podcast (NotebookLM audio) | ✓ | ✓ |
| Related media agent | ✓ | ✓ |
| Gemini diagrams | ✗ — do not produce | ✓ |
| `<!-- DIAGRAM -->` in content_html | ✗ — do not emit | ✓ |
| Cinematic video overview | ✗ — leave `youtube_video_id` NULL | ✓ |
| Revision technique guides | ✓ (templated, see below) | ✓ (templated, see below) |
| Exam technique guides | ✗ — removed entirely | ✗ — removed entirely |

Copyright policy: all content is original. No spec codes, paper codes, component codes, or exam board Level descriptors in any student-facing field. All mark schemes use StudyVault's rubric (Mastering / Secure / Developing / Emerging). See `CONTENT_PROMPT.md` for the full ban list and the concrete anti-examples drawn from past drift.

---

## Phase 1 — Plan

Single Claude call, once per subject+board. Prompt in `PLANNING_PROMPT.md`.

**Inputs:**
- Spec from `specs/{board}/{slug}-{code}.md` (193 specs already indexed in `specs/index.json`)
- Grounded web research pass (whitelisted sources — see `PLANNING_PROMPT.md` for exact list). Research informs *style, structure, emphasis, common misconceptions, 2026 spec changes* — never content or mark schemes.

**Outputs (plan JSON):**
- Subject metadata (slug, board, spec_code, colour palette, target audience)
- Unit structure with `article_units: [...]` and `practice_units: [...]` lists
- Per-lesson: number, title, description (60–100ch), spec references, spec-section markers
- Question type names for registration in `getGuideUrl()` (article units only)
- Teaching brief (structured: common misconceptions, examiner-report signals, topic weighting, spec changes, pedagogical notes). This brief is injected into every content agent call for this subject.

Unit structure rules and calibration heuristics live in `PLANNING_PROMPT.md`. The plan is the contract — everything downstream reads from it.

---

## Phase 2 — Subject activation

One activation agent, runs immediately after Phase 1 completes. Must run before any content agents because unit accent colours need to exist in Supabase for downstream steps.

**The agent creates:**
1. `subjects` row (slug, name, exam_board, spec_code, school_id, settings)
2. `units` rows (slug, name, subtitle, body_class, accent/accent_light/accent_badge, lesson_count, sort_order)
3. Empty `lessons` shells (one per planned lesson)
4. `subjects.settings`:
   - `quote_ticker_html` — 5–6 subject-relevant quotes (see `MANDATORY_CHECKLIST.md`); must be a dict, never `json.dumps(...)`
   - `practice_units` — array of unit slugs that use practice format (empty array for article-only subjects)
   - `unit_image_positions` — map of unit slug → object-position for unit card image
5. Homepage additions:
   - `.home-card` entry and `.picker-item` entry in `index.html`
   - Subject image at `images/subject-{slug}.jpg` (Unsplash)
6. CSS in `css/style.css`: one `.unit-{slug}-{N}` rule per unit, light + dark mode accent vars. Body class is only needed for the dark-mode variant; accent CSS is set per-lesson via `lesson-loader.js` from DB values.
7. Append subject slug to `SUBJECT_ORDER` in `scripts/generate_cinematic_videos.py` (for Unity only, but harmless for free tier).

Practice-format subjects (`practice_units` populated) skip the `<!-- DIAGRAM -->` placeholder in content and skip cinematic video generation per the feature matrix above.

---

## Phase 3 — Per-lesson content (parallel, bounded)

Branch by unit format:

### Article units → single content agent per lesson

Prompt: `CONTENT_PROMPT.md`. Reference lesson: pinned article example in `REFERENCE_LESSONS.md` (fetched by lesson ID, not by "most recent").

Agent output (JSON, written via Write tool — never bash heredocs):
- `description` — 60–100ch, browse-card copy
- `content_html` — sequential `data-narration-id="nN"`, ≥2 key-facts with actionable `data-revision-tip`, ≥2 collapsibles, ≥3 `<dfn class="term">` inline glossary; higher-only wrapping for tiered subjects; KaTeX for equations; no `<h1>`; no `<!-- DIAGRAM -->` unless Unity bespoke
- `exam_tip_html`, `conclusion_html` — both with narration IDs
- `practice_questions` — exactly 6, type strings matching registered names, marks as StudyVault rubric string
- `knowledge_checks` — exactly 5 (2 MCQ + 2 fill + 1 match)
- `flashcard_questions` — exactly 5, distinct from KCs
- `glossary_terms` — one per `<dfn>` in content_html
- `hero_keywords` — 3–4 Unsplash/Wikimedia search terms

Validation runs before each lesson writes to Supabase. See `CONTENT_PROMPT.md` for the full post-generation checklist and the ban-list grep.

**Agent limits:** max 10 lessons per agent. Beyond that, content thins and templates kick in. Split into parallel batches instead.

### Practice units → factory stage pipeline

See `PRACTICE_PIPELINE.md`. English Language Paper 1 Reading is the schema-defining unit; other practice subjects follow the same eight-stage shape with subject-specific input types.

Stages: passages → method cards + bronze (parallel) → silver + worked examples (parallel) → gold → AI prompts → topic links → assembly → insert.

Output: `practice_data` JSONB on each lesson row (not `content_html`). Practice lessons have no narration on content, no podcasts, no flashcards, no knowledge checks — but do have passage narration (6 Azure voices cycled) and related media.

---

## Phase 4 — Per-lesson assets (parallel after content)

Runs per lesson as its content lands, not batched. A stuck content agent blocks only itself.

| Asset | Produced by | Destination | Feature matrix |
|---|---|---|---|
| Hero image | `scripts/batch_heroes_*.py` or `download_heroes.py` (Unsplash → R2, index-first reuse) | `lessons.hero_image_url`, `hero_image_alt`, `hero_image_caption`, `hero_image_position` | Both tiers |
| Narration | `scripts/batch_narration.py` (Azure: Ollie odd / Ada even; multilingual SSML for language subjects) | `lessons.narration_manifest` array of `{id, src, duration}` | Both tiers |
| Podcast | `scripts/batch_podcasts.py` (NotebookLM audio overview, unit-context prompt) | Inserted into `lessons.related_media` under category `Podcasts` with title `Lesson Podcast`. The tabbed player reads it from there — do not store separately. | Both tiers |
| Related media | Dedicated Sonnet agent, one per lesson (see `RELATED_MEDIA_PIPELINE.md`) | `lessons.related_media` (array of category dicts — flat list, not nested) | Both tiers |
| Cinematic video | `scripts/generate_cinematic_videos.py` | `lessons.youtube_video_id` = R2 URL | **Unity only** |
| Diagram | `scripts/generate_diagrams.py` (Gemini) — see `DIAGRAM_PIPELINE.md`. GPT-image-2 replacement under evaluation (see `memory/gpt_image_2_evaluation.md`) | Inline `<figure>` in content_html; R2 URL | **Unity only** |

**Podcast-into-related-media is a hard contract.** `lesson-loader.js:306–317` greps `related_media` for category `Podcasts` → item title `Lesson Podcast`. Any other placement breaks the tabbed player.

**Dedicated related media agent, always.** Do not bolt it onto the content agent. Quality drops substantially when combined — related media needs its own web search budget.

---

## Phase 5 — Revision technique guides (templated)

Single agent per subject. Reads the 7 canonical technique files in `docs/REVISION_TECHNIQUES/` and fills in `{{SUBJECT_EXAMPLE_1}}` / `{{SUBJECT_EXAMPLE_2}}` with two subject-appropriate worked examples per technique. Pedagogy stays canonical; only the examples are bespoke.

The 7 techniques are fixed across all subjects: retrieval-practice, spaced-repetition, interleaving, dual-coding, elaborative-interrogation, knowledge-organisers, timed-practice. A subject may optionally add one discipline-specific technique (e.g. "Practising Calculations" for Science).

Hub page colour is fixed: green (`#16a34a` / `#f0fdf4`) for revision technique hubs, regardless of subject.

Guide HTML structure is `<main class="lesson-content">` + `<aside class="lesson-sidebar">` as required by `guide-loader.js`. Links use full absolute paths (`/guide/{subject}/revision-technique/{slug}`).

**Exam technique guides are not generated.** Removed entirely — the per-lesson `exam_tip_html` and the practice question mark schemes carry the same pedagogical load without the copyright adjacency.

---

## Phase 6 — Ship

1. Run `scripts/_audit_reference_candidates.py` (or equivalent) to sanity-check every shipped lesson against the drift grep (spec codes, Level descriptors, component codes). Zero hits required.
2. Set unit `image_url` from lesson 1's hero image for each unit.
3. Confirm `subjects.settings` is a dict, not a JSON string (breaks quote ticker silently).
4. Confirm every practice question `type` string is registered in `getGuideUrl()` mappings — no 404s.
5. Confirm `youtube_video_id` convention: Unity lessons have R2 URLs, free-tier article lessons are NULL, free-tier practice lessons are the sentinel `'practice-only'`.
6. Rerun `python scripts/_gen_tracker.py` — the subject tracker spreadsheet rebuilds from Supabase and now includes the new subject.
7. Commit + push. Tom reviews `status: pending_review` lessons via `/admin/review` and flips them to `live` once satisfied.

---

## Execution rules for Claude Code

- **Never pause to ask permission between phases.** Once Tom says "go", run the full pipeline end to end.
- **Phases 1 and 2 are sequential.** Everything in Phase 3 and beyond parallelises aggressively.
- **Agent parallelism:** max 10 lessons per content agent. Launch multiple in a single message, not staggered.
- **Use the Write tool for JSON files.** Bash heredocs mangle HTML content in escaping.
- **Use Claude Code subscription for all AI work, not the Anthropic API.** See `memory/feedback_no_api_credits.md`. This means disabling `claude_qa.py` on diagram generation.
- **Content agents have no DB read access.** Keep them isolated — they receive everything they need in the prompt. See `memory/pipeline-rules.md`.
- **The reference lesson is always the one pinned in `REFERENCE_LESSONS.md`.** Never "pick a recent one" — that's how past drift propagated.

---

## Timing target

10-lesson free-tier subject: ~20 minutes end-to-end with full parallelism.
30-lesson free-tier subject: ~40 minutes.
Multi-board same subject (4 boards × 30 lessons): launched as 4 parallel pipelines.

Narration is the usual bottleneck — runs sequentially per lesson. Everything else parallelises well.

---

## Related docs

| Doc | Purpose |
|---|---|
| `PLANNING_PROMPT.md` | Phase 1 agent prompt — research, mode decision, plan JSON schema |
| `CONTENT_PROMPT.md` | Phase 3 article agent prompt — full output schema, ban list, validation checklist |
| `PRACTICE_PIPELINE.md` | Phase 3 practice factory stages |
| `REFERENCE_LESSONS.md` | Pinned Supabase IDs for structural examples |
| `RELATED_MEDIA_PIPELINE.md` | Phase 4 related media agent prompt |
| `NARRATION_PIPELINE.md` | Azure TTS config (Ollie/Ada, multilingual SSML) |
| `VIDEO_PIPELINE.md` | Cinematic video + podcast generation (NotebookLM) |
| `DIAGRAM_PIPELINE.md` | Gemini diagrams (Unity only). GPT-image-2 replacement under evaluation |
| `REVISION_TECHNIQUES/` | 7 canonical technique templates |
| `QUESTIONS_PIPELINE.md` | Practice question formats, mark allocations, `getGuideUrl()` |
| `LESSON_TEMPLATE.md` | HTML components reference |
| `MANDATORY_CHECKLIST.md` | Pre-ship verification (shares bullets with Phase 6) |
