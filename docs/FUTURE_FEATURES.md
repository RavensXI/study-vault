# Future Features

## Teacher Content Editors — v1 built, needs iteration

### Lesson Editor (`/admin/editor`)
Block-based editor for lesson content. Teachers browse by subject/unit/lesson, edit content blocks (paragraph, key fact, collapsible, timeline, heading, list, blockquote), add/delete/reorder blocks, edit exam tip and conclusion sections, preview as student sees it, save back to Supabase via `api/pipeline/update-lesson.js`. Formatting toolbar (B/I/U/Glossary), Ctrl+S save, paste stripping, unsaved changes warning, sticky sidebar with save/discard/preview. Deep-linkable via query params (`?subject=...&unit=...&lesson=...`). Edit buttons on review page.

### Guide Editor (`/admin/editor-guide`)
Block-based editor for exam technique and revision technique guide pages. Teachers pick guide type and specific guide via the teacher setup modal flow (or direct URL params). Editable block types: page header (badge, title, subtitle), sections (h2/h3/p/tables), steps (numbered lists with add/remove), mistakes (add/remove), mark band tables (editable cells, add rows), collapsibles (model answers, templates). Sidebar sections editable (quick reference steps/timing). Save via `api/pipeline/update-guide.js`. Hub/index pages are not editable here (pipeline-generated). Deep-linkable: `?subject=...&type=exam-technique&slug=...`.

**Still needs (both editors):**
- **Cross-lesson templates** — "push this block to all lessons in unit"
- **Image picker** — search Wikimedia/Unsplash, upload custom, reposition. Currently diagrams are read-only.
- **No AI regeneration** — deliberate product decision. Only AI assist: optional "format my rough note into a key-fact box" and "check readability level" on pasted text.

## Auto-fetch Exam Specs & Papers
When a teacher uploads lessons, automatically find the exam board spec, past papers, and mark schemes. Either scrape/search at generation time or build a bank of specs beforehand. Need to determine the most reliable approach (exam board websites, curated library, or hybrid).

## Diagram & Hero Image Bank
Build a reusable, tagged bank of generated diagrams and hero images. When a new lesson is generated, search the bank for an appropriate existing image before calling Gemini or Unsplash. Same exam board + same topic = same diagram — a school teaching AQA Health & the People doesn't need a fresh "four humours" diagram when we already have one.

**Diagrams:** New Supabase table (`diagram_bank`) or columns on `lessons` — stores topic keywords, subject, unit, visual style (timeline, process flow, comparison, isotype). Before `generate_diagrams.py` calls Gemini, it queries the bank for semantic matches (cheap LLM call to score relevance vs full image generation). Matches reuse the existing R2 URL. Misses generate as normal, and the new diagram auto-enters the bank after QA.

**Heroes:** Same approach for Unsplash/Wikimedia hero images — tag by topic ("medieval castle", "laboratory equipment", "parliament"). Reuse across schools studying the same spec topics. Unsplash API integration already done (`scripts/lib/unsplash.py`, `download_heroes.py`, `/admin/images` search).

**Key benefit at scale:** Gemini diagram generation is the most expensive and error-prone pipeline step. Reusing QA'd diagrams across schools on the same exam board eliminates repeated generation costs and the regenerate-until-right QA cycle. Bank grows organically — every new subject/school enriches it for future runs.

## Teacher Data Dashboard
Major upgrade from current demo/hardcoded state. Needs real Supabase queries for progress tracking, engagement metrics, class-level insights. Key for selling to SLT — should be visually compelling and data-rich. Dedicated session to design and build.

## Direct-to-Storage Uploads (Commercial)
Current upload flow parses PPTs in the browser and sends extracted text via a JSON POST to a Vercel serverless function. This hits Vercel's 4.5 MB body limit for very large uploads (e.g. 2000+ science PPTs). Chunked upload added as a workaround (splits text into 2 MB chunks sent sequentially). For the commercial product, implement direct-to-storage uploads: browser uploads files straight to Supabase storage via presigned URLs, then a background worker parses them. No serverless function body limits involved. Standard pattern for large file handling at scale.

## Pipeline UX & Permissions Rework
Clarify who sees what — admin vs teacher screens. Currently can't QA images before publishing (have to set lessons live first, which doesn't make sense). Need a proper preview/staging state, clearer QA flow, and role-appropriate views for the pipeline.

**Teacher QA flow (for scale):** When onboarding a MAT or whole school, pipeline generates lessons as `review` instead of `live`. Teachers get a subject-scoped review page — preview lesson, check hero/diagram, approve (→ `live`) or reject with notes (→ `draft`). Infrastructure already exists: `content_status` enum, `/admin/review` page, `api/pipeline/review.js` approve/reject endpoints, audit logging. Main changes needed: (1) flip pipeline to write `review` not `live`, (2) teacher-accessible review page scoped to their subject, (3) inline hero/diagram previews on review cards. Not needed yet while it's one department — build when first external school onboards.

## Smart Revision Recommendations
Dashboard "Today's Revision" cards and subject browse pages driven by a retrieval practice algorithm instead of hardcoded demo data. Two paths into revision: (1) algorithmic "Up Next" — spaced repetition prioritising unvisited lessons, low knowledge check scores, and time-since-last-visit; (2) student choice — browse units freely, but each subject's browse page shows a "Recommended Next" card at the top. Needs real Supabase tracking (lesson_visits + knowledge_check_scores tables exist), a recommendation algorithm (portable from VaultCards Leitner-box), and UI changes to browse-loader + dashboard.

## Rank-up / Prestige System
Students can fill subject progress bars multiple times and "rank up" — gamification layer on top of lesson completion. Needs design decisions: rank names/tiers, visual treatment (badge, colour change, animation on rank-up), XP-based vs pure completion-based, whether ranks are per-subject or global.

## Retrieval Practice / Flashcards
Port spaced repetition flashcard system from `../vaultcards/` (React/Supabase app with Leitner-box algorithm, decks, streak tracking, XP, achievements, head-to-head challenges, teacher deck creation, PowerPoint→AI card generation). Algorithms and data model are portable; React/Tailwind UI is not — will need vanilla JS/CSS reimplementation.

## NotebookLM Video Overviews
Creating NotebookLM podcast-style video overviews for each lesson. History (60/60 complete). Food Tech L1 and RE Christianity Beliefs L1 also done. 137 lessons remaining across 6 subjects. Task list for Claude Code browser-control agent: `NOTEBOOKLM_VIDEO_TASKLIST.md`. `youtube_video_id` column on lessons table stores the video ID; lesson-loader.js renders the embed in sidebar.

## LaTeX Maths/Science Rendering (KaTeX)
Add KaTeX (CDN) for rendering equations, formulae, and chemical notation in Maths, Science, and other quantitative subjects. Faster and lighter than MathJax. Load CSS + JS via `<link>`/`<script>` tags, call `renderMathInElement()` in `lesson-loader.js` after content injection. Content generation prompt would include LaTeX notation inline (`\(...\)`) and display-mode (`\[...\]`).

## More Subjects
14 subjects remaining. Full list with exam boards: `docs/SUBJECT_ROADMAP.md`.
