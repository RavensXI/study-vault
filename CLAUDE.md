# StudyVault — Project Reference

Multi-subject GCSE revision site rebuilt from WordPress to static HTML. Opens directly in browser via `file://` protocol — no server, no build tools. Hosted on GitHub Pages via https://github.com/RavensXI/study-vault.

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
- TTS narration: Conflict & Tension all 15 manifests populated. Lessons 01–14 fully narrated, lesson 15 partial (1 clip). WAV files stored locally only — gitignored, need hosting solution. Other 3 units not started. Player UI in place on all 60 lessons.
- Accessibility toolbar (dark mode, dyslexia font, font sizing, Irlen overlays)
- Glossary tooltips, collapsible sections, timelines, key fact boxes, lightbox
- Embedded YouTube videos in sidebar (45 lessons — Conflict, Health, Elizabethan)
- Related Media sidebar (Lesson Podcast, curated Podcasts/Movies/TV/Docs, Study Tools)
- Exam Technique section (7 guide pages for every AQA question type + hub)
- Revision Techniques section (7 guide pages + hub, green theme)
- Page transitions, scroll progress bar, floating narration mini-player

**Platform features:**
- Root `index.html` — single-page app with login, subject picker, and dashboard views
- 3 demo accounts (emma/jake/guest, all password "revision" except guest/"guest")
- Subject picker: 25 GCSE subjects in 6 groups. History, Business, Geography, and Sport Science are `active: true` with URLs; others show "Coming Soon"
- Dashboard: greeting + exam countdown, today's revision cards, progress stats, subject grid
- All state in localStorage — no backend

**Business Studies (Edexcel 1BS0) — presentation-ready:**
- Landing page (`business/index.html`) with distinct images: `subject-business-1.jpg` (market stall) for Theme 1, `subject-business.jpg` (high street) for Theme 2
- Theme 1 and Theme 2 index pages (15 lesson cards each)
- All 30 lessons built with full content, diagrams (matplotlib reference + Gemini concept images), practice questions, knowledge checks, Related Media, video placeholders
- Theme 1 Lesson 1 fully featured: YouTube video embedded, Spotify podcast linked, TTS narration (33 clips, 7 min audio — WAV files local only)
- Exam Technique guides: hub + 6 guide pages (`business/exam-technique/`) for all Edexcel question types
- Revision Technique guides: hub + 8 guide pages (`business/revision-technique/`) including business-specific `practising-calculations.html`
- Hybrid diagram system: matplotlib for structured reference graphics, Gemini for photorealistic concept images

**Geography (AQA 8035) — complete (40 lessons across 2 papers):**
- Paper 1 (Physical Geography, indigo theme) and Paper 2 (Human Geography, red theme), 20 lessons each
- All lessons built with full content, practice questions (6/lesson, AQA format), knowledge checks (5/lesson)
- Exam Technique guides: hub + guide pages for AQA Geography question types
- Revision Technique guides: hub + guide pages adapted for Geography context

**Sport Science (OCR Cambridge National R180) — content-ready:**
- Landing page (`sport-science/index.html`) with single R180 unit card, orange theme (#ea580c)
- Unit index page (`sport-science/r180/index.html`) with 10 lesson cards
- All 10 lessons built with full content sourced from teacher PPTs, practice questions (6/lesson, OCR format: 1/2/3/4/6/8 marks), knowledge checks (5/lesson)
- Exam Technique guides: hub + 5 guide pages (`sport-science/exam-technique/`) for OCR question types (Identify/State, Describe, Explain, Extended response, Discuss)
- Revision Technique guides: hub + 7 guide pages (`sport-science/revision-technique/`) with sport-science-specific examples
- Narration player UI in place on all 10 lessons (empty manifests, ready for audio)
- Still needs: hero images (Wikimedia Commons), matplotlib diagrams, Gemini concept images

### Still TODO
- **Sport Science**: Hero images, matplotlib reference diagrams (orange palette), Gemini concept images (selective). No narration yet.
- **Business Studies**: audio hosting solution needed before narration WAVs can go live (Cloudflare R2 recommended — free 10GB tier, zero egress). Videos and podcasts for lessons 2–30 (deferred until green-lit by management).
- TTS narration — remaining History units (Health, Elizabethan, America — 45 lessons). KaniTTS-2 flagged as worth testing (RTF ~0.2, zero-shot voice cloning, PyTorch so potentially AMD-compatible).
- PWA (service worker + manifest.json)
- Real auth backend (Supabase) + teacher analytics dashboard — deferred until institutional green light


### Future features (not started)
- Retrieval Practice — cross-lesson spaced repetition quiz (requires backend)
- Content for remaining subjects beyond History, Business, Geography, and Sport Science

---

## File Structure
```
Study Vault/
├── CLAUDE.md
├── index.html                ← Subject selection / login / dashboard (SPA)
├── css/style.css             ← All styling
├── js/main.js                ← All JS
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
├── docs/                     ← Pipeline & reference docs
│   ├── DIAGRAM_PIPELINE.md
│   ├── NARRATION_PIPELINE.md
│   ├── LESSON_TEMPLATE.md
│   ├── QUESTIONS_PIPELINE.md
│   ├── RELATED_MEDIA_PIPELINE.md
│   ├── SUBJECT_PLAYBOOK.md
│   └── SUBJECT_PROMPT.md
├── scripts/                  ← Build scripts & voice references
│   ├── gemini_regen.py
│   ├── generate_narration.py
│   ├── generate_sport_*.py
│   ├── download_sport_heroes.py
│   ├── insert_sport_images.py
│   ├── voice-reference/      ← Voice cloning samples
│   └── runpod/               ← RunPod deployment scripts
├── tts-research-log.md       ← TTS research (external agents)
├── tech-research-log.md      ← EdTech research (external agents)
└── Spec and Materials/       ← Teacher PPTs (untracked)
    └── Lessons/{Health,America,Conflict,Elizabeth}/
```

### Path conventions
- Root `index.html` → `css/style.css`, `js/main.js`
- Subject landing pages (e.g. `history/index.html`) → `../css/style.css`, `../js/main.js`
- Lesson/unit pages (e.g. `history/conflict-tension/lesson-01.html`) → `../../css/style.css`, `../../js/main.js`

---

## API Keys

All stored in environment variables — never commit them.

| Service | Env Var | Used For |
|---------|---------|----------|
| Gemini | `GEMINI_API_KEY` | Diagram generation (see `docs/DIAGRAM_PIPELINE.md`) |
| ElevenLabs | `ELEVENLABS_API_KEY` | TTS paid fallback (see `docs/NARRATION_PIPELINE.md`) |

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

All initialised in `DOMContentLoaded`:
- `initScrollProgress()` — accent-coloured bar at page top
- `initCollapsibles()` — expand/collapse with animation
- `initVisitedTracking()` — localStorage `studyvault-visited`
- `initMobileNav()` — hamburger menu
- `initPracticeQuestions()` — random question selection, mark scheme display, past paper badges, guide links via `getGuideUrl()`
- `initNarration()` — play/pause, speed toggle, paragraph highlighting, mini-player, auto-scroll suppression
- `initAccessibility()` — dark mode, dyslexia font, font size, Irlen overlays (persisted in `studyvault-a11y`)
- `initGlossary()` — popup tooltips from `data-def`, hover/tap
- `initKnowledgeCheck()` — modal quiz overlay, best score in localStorage
- `initLightbox()` — click-to-expand on hero images and diagrams
- `initHeroEdit()` — `?hero-edit` URL param for position adjustment
- `initPageTransitions()` — fade-out/in on internal links
- `initRevisionTips()` — green lightbulb tips on `.key-fact`, `.timeline`, `.collapsible`
- `initNavIcons()` — pen (purple) / lightbulb (green) icons on nav links, pill-styled prev/next
- `initLessonNavBackSlot()` — back-link positioning on first/last lessons

---

## Design Rules
- Background: warm cream `#faf8f5`, not bright white
- Text: warm dark brown `#2d2a26`, not pure black
- Font: Inter (body) + Source Serif 4 (headings) via Google Fonts
- Cards: `border-radius: 16px`, soft warm shadows
- All data inlined in HTML (no fetch — `file://` CORS restrictions)
- Logo: inline SVG padlock replaces period in "StudyVault." — `currentColor`, scales with text
- Narration highlight: gold `#fef9e7` with `#e6b800` border
- Key takeaways: 2-3 bullets, not exhaustive lists

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

**Summary:** Qwen3-TTS running locally on AMD RX 6800 (CPU mode, slow but working). Conflict & Tension lessons 01–14 narrated, everything else pending. WAV files gitignored — need Cloudflare R2 hosting before going live. Also check `tts-research-log.md` for latest model developments.

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
