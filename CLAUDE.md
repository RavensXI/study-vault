# StudyVault — Project Reference

Multi-subject GCSE revision site rebuilt from WordPress to static HTML. Opens directly in browser via `file://` protocol — no server, no build tools. Repo: https://github.com/RavensXI/study-vault.

### Deployments
- **GitHub Pages** (`main` branch): https://ravensxi.github.io/study-vault/ — History only, no login
- **Vercel** (`platform` branch): https://study-vault-alpha.vercel.app/ — full multi-subject platform with login

## Owner
Teacher: Tom Shaun, email: `t.shaun@unity.lancs.sch.uk`
Git config: user "Tom Shaun", email "tomshaun90@gmail.com"

## Current Status

### Branches
- **`main`** — live student-facing site. History content at root level. Single-subject, no login.
- **`platform`** (current) — multi-subject platform. History content under `history/` subfolder. Login system, subject picker, dashboard. Will eventually replace `main`.
- When merging `main` into `platform`, be aware of the path difference (root vs `history/`).

### What's done

**History (complete — 60 lessons across 4 units):**
- All lessons cross-referenced against teacher PPTs, readability-passed for GCSE students
- Hero images (Wikimedia Commons), infographic diagrams (Gemini API, ~71 total), practice questions (6/lesson, 360 total with AQA past paper tags), knowledge checks (5/lesson, 300 total)
- TTS narration: All 60 lessons fully narrated with Azure Speech (Ollie/Bella alternating). MP3s hosted on Cloudflare R2. Manifests populated with R2 URLs and durations. Player UI in place on all 60 lessons.
- Accessibility toolbar (dark mode, dyslexia font, font sizing, Irlen overlays)
- Glossary tooltips, collapsible sections, timelines, key fact boxes, lightbox
- Embedded YouTube videos in sidebar (45 lessons — Conflict, Health, Elizabethan)
- Related Media sidebar (Lesson Podcast, curated Podcasts/Movies/TV/Docs, Study Tools)
- Exam Technique section (7 guide pages for every AQA question type + hub)
- Revision Techniques section (7 guide pages + hub, green theme)
- Page transitions, scroll progress bar, floating narration mini-player

**Platform features:**
- Root `index.html` — single-page app with login, subject picker, and dashboard views
- **Microsoft SSO** via Supabase Auth (Azure AD / Entra) — "Sign in with Microsoft" button for Unity College accounts. Supabase JS client loaded via CDN. SSO users get UUID-based localStorage keys; demo users keep username-based keys. `onAuthStateChange` listener handles session lifecycle. **Code is complete but SSO is blocked pending Entra admin consent** — Unity College's tenant restricts user consent. Network manager (Global Admin) needs to grant tenant-wide admin consent for the "StudyVault" Enterprise Application (Entra ID → Enterprise Applications → StudyVault → Permissions → Grant admin consent). App only requests `User.Read` (name + email). Deputy head approval being sought first (meeting Tuesday), then network manager does the one-click consent.
- 3 demo accounts (emma/jake/guest) kept alongside SSO for non-Unity demos. Demo account buttons auto-submit (no manual form).
- Subject picker: 25 GCSE subjects in 6 groups. History, Business, Geography, Sport Science, and Drama are `active: true` with URLs; others show "Coming Soon"
- Dashboard: greeting + exam countdown, today's revision cards, progress stats, subject grid
- Auth state: Supabase session checked first (async), then localStorage demo fallback. Subject/progress data in localStorage keyed by user ID.

**Business Studies (Edexcel 1BS0) — presentation-ready:**
- Landing page (`business/index.html`) with distinct images: `subject-business-1.jpg` (market stall) for Theme 1, `subject-business.jpg` (high street) for Theme 2
- Theme 1 and Theme 2 index pages (15 lesson cards each)
- All 30 lessons built with full content, diagrams (matplotlib reference + Gemini concept images), practice questions, knowledge checks, Related Media, video placeholders
- TTS narration: All 30 lessons fully narrated with Azure Speech. MP3s hosted on Cloudflare R2.
- Theme 1 Lesson 1 fully featured: YouTube video embedded, Spotify podcast linked
- Exam Technique guides: hub + 6 guide pages (`business/exam-technique/`) for all Edexcel question types
- Revision Technique guides: hub + 8 guide pages (`business/revision-technique/`) including business-specific `practising-calculations.html`
- Hybrid diagram system: matplotlib for structured reference graphics, Gemini for photorealistic concept images

**Geography (AQA 8035) — complete (40 lessons across 2 papers):**
- Paper 1 (Physical Geography, indigo theme) and Paper 2 (Human Geography, red theme), 20 lessons each
- All lessons built with full content, practice questions (6/lesson, AQA format), knowledge checks (5/lesson)
- TTS narration: All 40 lessons fully narrated with Azure Speech. MP3s hosted on Cloudflare R2.
- Exam Technique guides: hub + guide pages for AQA Geography question types
- Revision Technique guides: hub + guide pages adapted for Geography context

**Sport Science (OCR Cambridge National R180) — presentation-ready:**
- Landing page (`sport-science/index.html`) with single centred R180 unit card, orange theme (#ea580c)
- Unit index page (`sport-science/r180/index.html`) with 10 lesson cards
- All 10 lessons built with full content sourced from teacher PPTs, practice questions (6/lesson, OCR format: 1/2/3/4/6/8 marks), knowledge checks (5/lesson)
- Hero images (Wikimedia Commons, user-selected), Gemini pictorial isotype diagrams (all 10 QC'd)
- Related Media sidebar curated for all 10 lessons (podcasts, videos, movies, TV, documentaries, study tools)
- Exam Technique guides: hub + 5 guide pages (`sport-science/exam-technique/`) for OCR question types (Identify/State, Describe, Explain, Extended response, Discuss)
- Revision Technique guides: hub + 7 guide pages (`sport-science/revision-technique/`) with sport-science-specific examples
- TTS narration complete: all 10 lessons narrated with Azure Speech (350 clips, manifests with durations). Odd lessons = Ollie (male), even = Bella (female). MP3s hosted on Cloudflare R2.

**Drama (OCR J316) — complete (12 lessons across 2 units):**
- Blood Brothers Section A (6 lessons, purple theme) and Rise Up Section B (6 lessons, purple theme)
- All 12 lessons built via content generation pipeline, practice questions (6/lesson, OCR format), knowledge checks (5/lesson)
- 24 past paper questions tagged from OCR specimen/sample papers
- TTS narration: All 12 lessons fully narrated with Azure Speech (400 clips). MP3s hosted on Cloudflare R2.
- Gemini pictorial isotype diagrams (12 total, all QC'd)
- Exam Technique guides: hub + 9 guide pages (`drama/exam-technique/`) for OCR question types
- Revision Technique guides: hub + 8 guide pages (`drama/revision-technique/`)
- First subject built entirely through the automated content generation pipeline

### Dynamic Architecture (LIVE on Vercel)
All content now served from Supabase on the `platform` branch (Vercel deployment). Static HTML files remain in repo as backup but are no longer linked from the dynamic site.

**What's running:**
- 152 lessons in Supabase `lessons` table with content_html, questions, narration manifests, related media
- 79 guide pages in `guide_pages` table
- Images on Cloudflare R2 (`studyvault-images` bucket)
- ~5,000 narration MP3s on Cloudflare R2 (`studyvault-audio` bucket)
- Dynamic templates: `lesson.html`, `browse.html`, `guide.html` with JS loaders
- URL scheme: `/lesson/{subject}/{unit}/{number}`, `/browse/{subject}/{unit?}`, `/guide/{subject}/{type}/{slug?}`
- Dashboard links to dynamic routes (not static HTML)
- Auth guards on all dynamic pages (Supabase session or demo localStorage)
- Public RLS policies for live content (anon users can read `status='live'` rows)
- Admin tools: `/admin/pipeline` (upload/generate), `/admin/review` (QC review), `/admin/images` (hero image QA + diagram QA with Gemini regen)
- Admin login on homepage with Pipeline, Review, Images nav
- Pipeline adapter: `scripts/supabase_writer.py` for writing new content to DB

**Supabase tables:** schools, profiles, subjects, units, lessons, guide_pages, user_selected_subjects, lesson_visits, knowledge_check_scores, content_pipeline_logs, upload_jobs, pipeline_steps, classes, class_members

**R2 buckets:**
- `studyvault-audio` — narration MP3s, public URL: `https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev`
- `studyvault-images` — hero images + diagrams, public URL: `https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev`

### Still TODO
- **Drama hero images**: Need QA positioning via `/admin/images`
- **Drama L1**: NotebookLM video still needed
- **Dashboard progress bars**: Currently use hardcoded demo data — need real Supabase queries
- **Platform admin setup**: SSO must be active first, then: `UPDATE profiles SET role = 'platform_admin' WHERE email = 't.shaun@unity.lancs.sch.uk'`
- **Direct Postgres connection**: Tom's home network is IPv6-only to Supabase — need to troubleshoot or use a different network. Env var `SUPABASE_DB_URL` has the password.
- **2 parsing fixes**: Business Theme 1 Lesson 9 (0 practice questions) and Theme 2 Lesson 14 (0 knowledge checks) — JS syntax the parser couldn't handle
- **Sport Science**: YouTube videos for lessons 2–10
- **Business Studies**: Videos and podcasts for lessons 2–30 (deferred until green-lit by management)
- PWA (service worker + manifest.json)
- **Microsoft SSO activation**: network manager grants Entra admin consent (one click) → then test on Vercel
- Role detection (teacher vs student) — profiles table exists, needs testing
- Remove demo accounts once SSO is battle-tested
- Retire static HTML files once dynamic system is fully verified


### Future features (not started)
- Retrieval Practice / Flashcards — port spaced repetition flashcard system from `../vaultcards/` (React/Supabase app with Leitner-box algorithm, decks, streak tracking, XP, achievements, head-to-head challenges, teacher deck creation, PowerPoint→AI card generation). Requires Supabase backend first. Algorithms and data model are portable; React/Tailwind UI is not — will need vanilla JS/CSS reimplementation to fit Study Vault's static architecture.
- Content for remaining subjects beyond History, Business, Geography, Sport Science, and Drama

---

## File Structure
```
Study Vault/
├── CLAUDE.md
├── index.html                ← Subject selection / login / dashboard (SPA)
├── lesson.html               ← Dynamic lesson template (Supabase-driven)
├── browse.html               ← Dynamic browse template (subject/unit index)
├── guide.html                ← Dynamic guide template (exam/revision technique)
├── vercel.json               ← Vercel rewrites for dynamic routes
├── css/style.css             ← All styling
├── js/
│   ├── main.js               ← All JS (Phase 1/2 split for dynamic pages)
│   ├── lesson-loader.js      ← Fetches lesson from Supabase, populates template
│   ├── browse-loader.js      ← Fetches subject/unit data, renders cards
│   └── guide-loader.js       ← Fetches guide pages (exam/revision technique)
├── package.json              ← npm deps (jszip, xml2js, pdf-parse, @supabase/supabase-js, @aws-sdk/client-s3)
├── admin/
│   ├── pipeline.html         ← Content generation pipeline UI
│   ├── review.html           ← QC review page (platform_admin only)
│   └── images.html           ← Image QA tool (hero images + diagrams with Gemini regen)
├── api/pipeline/             ← Vercel serverless routes (upload, parse, approve-plan, status)
│   └── _lib/                 ← Shared auth.js, supabase.js
├── supabase/
│   └── migrations/001_schema.sql  ← Full DB schema (tables, RLS, triggers)
├── images/                   ← padlock.svg, subject-{id}.jpg
├── fonts/opendyslexic-*/     ← OpenDyslexic woff2/woff
├── history/
│   ├── index.html            ← History landing page (4 unit cards)
│   ├── conflict-tension/     ← 15 lessons + hero images + diagrams
│   ├── health-people/        ← 15 lessons + hero images + diagrams
│   ├── elizabethan/          ← 15 lessons + hero images + diagrams
│   ├── america/              ← 15 lessons + hero images + diagrams
│   ├── exam-technique/       ← Hub + 7 guide pages (purple theme)
│   └── revision-technique/   ← Hub + 7 guide pages (green theme)
├── business/
│   ├── index.html            ← Business landing page (2 theme cards)
│   ├── theme-1/              ← 15 lessons + diagrams (all built)
│   ├── theme-2/              ← 15 lessons + diagrams (all built)
│   ├── exam-technique/       ← Hub + 6 guide pages (Edexcel question types)
│   └── revision-technique/   ← Hub + 8 guide pages (incl. practising-calculations)
├── geography/
│   ├── index.html            ← Geography landing page (2 paper cards)
│   ├── paper-1/              ← 20 lessons (Physical Geography, indigo)
│   ├── paper-2/              ← 20 lessons (Human Geography, red)
│   ├── exam-technique/       ← Hub + guide pages (AQA Geography)
│   └── revision-technique/   ← Hub + guide pages
├── sport-science/
│   ├── index.html            ← Sport Science landing page (1 unit card)
│   ├── r180/                 ← 10 lessons (orange theme)
│   ├── exam-technique/       ← Hub + 5 guide pages (OCR question types)
│   └── revision-technique/   ← Hub + 7 guide pages
├── drama/                    ← Drama (OCR J316), built via pipeline
│   └── (static backups — content served dynamically from Supabase)
├── specs/                    ← Exam board specifications (OCR J316 Drama spec)
├── docs/                     ← Pipeline & reference docs
│   ├── DIAGRAM_PIPELINE.md
│   ├── NARRATION_PIPELINE.md
│   ├── LESSON_TEMPLATE.md
│   ├── QUESTIONS_PIPELINE.md
│   ├── RELATED_MEDIA_PIPELINE.md
│   ├── SUBJECT_PLAYBOOK.md
│   ├── SUBJECT_PROMPT.md
│   ├── GENERATION_PROMPT.md  ← Inject-at-call-time prompt for content generation
│   └── PIPELINE_ARCHITECTURE.md ← Full pipeline architecture docs
├── scripts/                  ← Build scripts & voice references
│   ├── migrate_to_supabase.py       ← Migrate 140 lessons from HTML to Supabase
│   ├── supabase_writer.py           ← Pipeline adapter (DB writes instead of HTML)
│   ├── upload_images_to_r2.py       ← Upload hero images + diagrams to R2
│   ├── gemini_regen.py
│   ├── generate_azure_narration.py  ← Azure Speech TTS batch generator (MP3 output)
│   ├── convert_wav_to_mp3.py        ← Batch WAV→MP3 converter (ffmpeg)
│   ├── upload_to_r2.py              ← Upload narration MP3s to Cloudflare R2
│   ├── generate_narration.py        ← Legacy Qwen3-TTS (Conflict lessons)
│   ├── pipeline_generate.py         ← CLI helper for pipeline (info, text, write, status, review)
│   ├── generate_drama_diagrams.py   ← Drama Gemini diagram generation
│   ├── generate_drama_narration.py  ← Drama Azure Speech TTS generation
│   ├── download_drama_heroes.py     ← Drama hero image downloader
│   ├── tag_drama_past_papers.py     ← Drama past paper question tagger
│   ├── generate_sport_*.py
│   ├── download_sport_heroes.py
│   ├── insert_sport_images.py
│   ├── compress_images.py    ← Resize & compress all project images (Pillow)
│   ├── voice-reference/      ← Voice cloning samples
│   └── runpod/               ← RunPod deployment scripts
├── tts-research-log.md       ← TTS research (external agents)
├── tech-research-log.md      ← EdTech research (external agents)
└── Spec and Materials/       ← Teacher PPTs (untracked)
    └── Lessons/{Health,America,Conflict,Elizabeth}/
```

### Path conventions
- **Dynamic pages** (`lesson.html`, `browse.html`, `guide.html`): absolute paths (`/css/style.css`, `/js/main.js`)
- **Static pages** (legacy HTML files still in repo): relative paths (`../../css/style.css`)
- **URL scheme**: `/lesson/{subject}/{unit}/{number}`, `/browse/{subject}/{unit?}`, `/guide/{subject}/{type}/{slug?}`

---

## API Keys

All stored in environment variables — never commit them.

| Service | Env Var | Used For |
|---------|---------|----------|
| Gemini | `GEMINI_API_KEY` | Diagram generation (see `docs/DIAGRAM_PIPELINE.md`) |
| ElevenLabs | `ELEVENLABS_API_KEY` | TTS paid fallback (see `docs/NARRATION_PIPELINE.md`) |
| Supabase | `SUPABASE_URL` | Project URL (`https://baipckgywpnwapobwtsy.supabase.co`) — hardcoded in `index.html` |
| Supabase | `SUPABASE_ANON_KEY` | Publishable anon key — hardcoded in `index.html` (safe for client-side). Microsoft SSO (Azure AD) configured. |
| Supabase | `SUPABASE_SERVICE_KEY` | Service role key — **server-side only** (bypasses RLS). Used by migration and pipeline scripts. Never commit. |
| Azure Speech | `AZURE_SPEECH_KEY` | TTS narration generation (region: `uksouth`, S0 tier). See `docs/NARRATION_PIPELINE.md` |
| Cloudflare R2 | `R2_ACCESS_KEY_ID` | S3-compatible access key for narration audio bucket |
| Cloudflare R2 | `R2_SECRET_ACCESS_KEY` | Secret key for R2 bucket access |
| Cloudflare R2 | `R2_ACCOUNT_ID` | Cloudflare account ID for R2 endpoint URL |
| Supabase | `SUPABASE_DB_URL` | Direct Postgres password (IPv6 connection blocked from Tom's network — troubleshoot later) |

---

## Unit Colour Themes

| Unit | Body class | Accent |
|------|-----------|--------|
| Conflict & Tension | `unit-conflict` | `#c44536` (terracotta) |
| Health & People | `unit-health` | `#0d9488` (teal) |
| Elizabethan | `unit-elizabethan` | `#b45309` (amber) |
| America | `unit-america` | `#2563eb` (blue) |
| Exam Technique | `unit-exam-technique` | `#7c3aed` (purple) |
| Revision Techniques | `unit-revision-technique` | `#16a34a` (green) |
| Business Theme 1 | `unit-business-1` | `#0891b2` (cyan) |
| Business Theme 2 | `unit-business-2` | `#059669` (emerald) |
| Geography Paper 1 | `unit-geography-1` | `#4f46e5` (indigo) |
| Geography Paper 2 | `unit-geography-2` | `#dc2626` (red) |
| Sport Science R180 | `unit-sport-science` | `#ea580c` (orange) |
| Drama Section A | `unit-drama-section-a` | `#7c3aed` (purple) |
| Drama Section B | `unit-drama-section-b` | `#7c3aed` (purple) |

---

## Lesson Page Template

Full template, content components (key facts, collapsibles, timelines, glossary terms, diagrams, hero images), and content editing conventions documented in **`docs/LESSON_TEMPLATE.md`** — read that file before building or editing lessons.

Canonical template: `history/conflict-tension/lesson-01.html`.

---

## Practice Questions & Knowledge Checks

Full details documented in **`docs/QUESTIONS_PIPELINE.md`** — read that file before writing questions for any subject. Covers question formats, mark allocations per subject/exam board, `getGuideUrl()` mapping, knowledge check types, and sourcing guidance.

**Summary:** 6 practice questions + 5 knowledge checks per lesson. Past paper questions tagged with `pastPaper` property. Knowledge checks: 2 MCQ + 2 fill-in-the-blank + 1 match-up. Best score in localStorage.

---

## Sidebar Structure

Three sections in order: **Knowledge Check** (button → modal quiz), **Related Media** (collapsible categories), **Video** (YouTube embed, 45 lessons only).

Full Related Media curation process, HTML patterns, category emojis, and link conventions documented in **`docs/RELATED_MEDIA_PIPELINE.md`** — read that file before adding or updating Related Media.

**Summary:** Spin up research agents (one per lesson) to find engaging external content. Category order: Lesson Podcast → Podcasts → Videos & Channels → Movies → TV Shows → Documentaries → Study Tools. Empty categories omitted. Max 3 items per category. Movies/TV/docs use JustWatch UK URLs; podcasts use specific episode URLs.

Do NOT add a "Key Facts" section to the sidebar. Sidebar scrolls independently within `max-height: calc(100vh - 6rem)` — a subtle accent-coloured scrollbar appears on hover.

---

## Subject Build Plans

Lesson breakdowns, spec references, exam/revision technique guides, and subject-specific notes:

- **Business Studies (Edexcel 1BS0):** `business/BUILD_PLAN.md` — 2 themes, 30 lessons, cyan/emerald
- **Geography (AQA 8035):** `geography/BUILD_PLAN.md` — 2 papers, 40 lessons, indigo/red
- **Sport Science (OCR R180):** `sport-science/BUILD_PLAN.md` — 1 unit, 10 lessons, orange
- **Drama (OCR J316):** Built via pipeline — 2 units, 12 lessons, purple

---

## Diagram Generation

Full pipeline documented in **`docs/DIAGRAM_PIPELINE.md`** — read that file before creating or updating diagrams.

**Summary:** 4-step process — (1) research agents find real citable data, (2) matplotlib generates data-accurate baseline, (3) Gemini pictorial isotype redesign using thematic icons, (4) QC agent review with up to 3 regeneration iterations.

**Key details:**
- Model: `gemini-3.1-flash-image-preview`, API key in `$GEMINI_API_KEY`
- Filenames: `diagram_descriptive_name.jpg`, matplotlib backups as `*_matplotlib.jpg`
- HTML: `<figure class="diagram">`, full width, 720px max
- Placement: at **content-relevant locations**, not always at the top. 15+ lines from other images.
- Helper scripts: `scripts/gemini_regen.py`, `scripts/generate_{subject}_diagrams.py`, `scripts/generate_{subject}_gemini_infographics.py`

**Legacy:** Business uses hybrid matplotlib + Gemini concept images. History uses Gemini-only infographics (~71 total).

---

## JS Features (main.js)

Split into two phases for dynamic page support:

**Phase 1 — runs on DOMContentLoaded (static elements always present):**
- `initScrollProgress()` — accent-coloured bar at page top
- `initMobileNav()` — hamburger menu
- `initAccessibility()` — dark mode, dyslexia font, font size, Irlen overlays (persisted in `studyvault-a11y`)
- `initPageTransitions()` — fade-out/in on internal links

**Phase 2 — `window.initLessonFeatures()` (called after content injection, or immediately on static pages):**
- `initCollapsibles()` — expand/collapse with animation
- `initVisitedTracking()` — localStorage `studyvault-visited`
- `initPracticeQuestions()` — random question selection, mark scheme display, past paper badges, guide links via `getGuideUrl()` (supports both static `../exam-technique/` and dynamic `/subject/exam-technique/` paths)
- `initNarration()` — play/pause, speed toggle, paragraph highlighting, mini-player, auto-scroll suppression
- `initGlossary()` — popup tooltips from `data-def`, hover/tap
- `initKnowledgeCheck()` — modal quiz overlay, best score in localStorage
- `initLightbox()` — click-to-expand on hero images and diagrams
- `initHeroEdit()` — `?hero-edit` URL param for position adjustment
- `initRevisionTips()` — green lightbulb tips on `.key-fact`, `.timeline`, `.collapsible` (supports dynamic paths)
- `initNavIcons()` — pen (purple) / lightbulb (green) icons on nav links, pill-styled prev/next
- `initLessonNavBackSlot()` — back-link positioning on first/last lessons
- `initLessonPill()` — lesson number pill in sticky header (supports both `lesson-NN.html` and `/lesson/.../N` URLs)
- `initLogoLink()` — logo links to root (skips rewrite on dynamic routes)

**Dynamic page loaders (separate files):**
- `lesson-loader.js` — auth check → parse `/lesson/{subject}/{unit}/{number}` → fetch from Supabase → populate template → call `initLessonFeatures()`
- `browse-loader.js` — auth check → render subject landing or unit index from Supabase → calls `initNavIcons()` for header icons
- `guide-loader.js` — auth check → render guide hub index or individual guide page from Supabase → rewrites relative links to dynamic `/guide/` routes

---

## Design Rules
- Background: warm cream `#faf8f5`, not bright white
- Text: warm dark brown `#2d2a26`, not pure black
- Font: Inter (body) + Source Serif 4 (headings) via Google Fonts `<link>` tags in HTML `<head>` (not CSS `@import` — avoids render-blocking waterfall)
- Cards: `border-radius: 16px`, soft warm shadows
- Static pages: data inlined in HTML. Dynamic pages: data fetched from Supabase at runtime.
- Logo: inline SVG padlock replaces period in "StudyVault." — `currentColor`, scales with text
- Narration highlight: gold `#fef9e7` with `#e6b800` border
- Key takeaways: 2-3 bullets, not exhaustive lists
- Images: hero images max 1200px wide, diagrams max 1000px wide, JPEG quality 82. Run `python scripts/compress_images.py` after adding new images.

---

## Content Editing Conventions

See **`docs/LESSON_TEMPLATE.md`** for full conventions. Key rules:

- **Scope:** Only edit within `<article class="study-notes">`, `<div class="exam-tip">`, `<div class="conclusion">`
- **Preserve:** All `data-narration-id` attributes, glossary `<dfn>` terms, HTML entities
- **Readability:** Short sentences, active voice, concrete over abstract (GCSE age 15-16)
- **PPTs:** Read with `python -m markitdown "filepath"` (.pptx only)

---

## TTS Narration

Full details documented in **`docs/NARRATION_PIPELINE.md`** — read that file before doing any narration work. Covers models tried, voice cloning config, generation process, infrastructure, and progress tracking.

**Summary:** Azure Speech (cloud API) — near-instant, deterministic, British English voices alternating by lesson (Ollie male odd, Bella female even). **All 152 lessons fully narrated** across all 5 subjects (~5,000 MP3 clips). Audio hosted on **Cloudflare R2** (`studyvault-audio` bucket, public r2.dev URL). Manifests in each lesson HTML point to R2 URLs with durations. Generation script outputs MP3 directly (96kbps, 24kHz, mono). Also check `tts-research-log.md` for latest model developments.

---

## YouTube Videos

Channel: `@UnityCollegeHistory`. Three playlists mapped 1:1 to lessons (Elizabethan, Health, Conflict — 15 each). America has no videos. Video IDs are already embedded in each lesson's sidebar HTML.

## Conflict & Tension Hero Images
Conflict hero images use older naming (e.g. `Versailles_1919.jpg`, `lesson 2 hero.jpg` with spaces). Other units use `lesson-NN-hero.jpg`.

---

## Research Logs

Two automated research agents write daily findings to log files in this directory:
- **`tts-research-log.md`** — TTS/voice cloning developments (new models, benchmarks, AMD compatibility)
- **`tech-research-log.md`** — EdTech/dev tools developments (hosting, PWA, AI in education)

When TTS, narration, hosting, or platform architecture topics come up, **read the relevant log file(s) first** before making recommendations.
