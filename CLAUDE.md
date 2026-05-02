# StudyVault — Project Reference

Multi-subject GCSE revision site. Repo: https://github.com/RavensXI/study-vault

### Deployments
- **GitHub Pages** (`main`): https://ravensxi.github.io/study-vault/ — History only, no login
- **Vercel** (`platform`): https://www.studyvault.co.uk/ (custom domain, also accessible at study-vault-alpha.vercel.app) — full platform, public content, admin/teacher login

### Owner
Tom Shaun — `t.shaun@unity.lancs.sch.uk` / git: `tomshaun90@gmail.com`

---

## Branches
- **`main`** — History at root level. Single-subject, no login.
- **`platform`** (current) — multi-subject. History under `history/`. Public content, school login for students, password-gated admin/teacher areas.

## Subjects — Unity College (school_id set, all on Vercel)

| Subject | Exam Board | Lessons | Units | Podcasts |
|---------|-----------|---------|-------|----------|
| History | AQA | 60 | 4 (Conflict, Health, Elizabethan, America) | 60/60 |
| Business Studies | Edexcel 1BS0 | 30 | 2 themes | 30/30 |
| Geography | AQA 8035 | 54 | 3 (Paper 1, Paper 2, Geographical Skills) | 40/40 |
| Sport Science | OCR R180 | 10 | 1 (R180) | 10/10 |
| Drama | OCR J316 | 12 | 2 (Blood Brothers, Rise Up) | 12/12 |
| Food Technology | AQA 8585 | 10 | 1 (Nutrition & Health) | 10/10 |
| Religious Education | AQA 8062 | 40 | 8 | 40/40 |
| Music | Eduqas C660U | 26 | 6 | 26/26 |
| English Literature | AQA 8702 | 42 | 5 | 42/42 |
| English Language | AQA 8700 | 30 (practice-first) | 4 | No narration — practice format |
| Science | AQA 8464 | 48 + 15 practice | 6 + 3 practice (Physics Calc, Chem Calc, Bio Data) | 48/48 |
| Separate Sciences | AQA 8461/8462/8463 | 22 + 6 practice | 3 + 1 practice (Higher Calculations) | 22/22 |
| Spanish | AQA 8692 | 26 | 3 | 26/26 |
| German | AQA 8662 | 26 | 3 | 26/26 |
| French | AQA 8652 | 26 | 3 | 26/26 |
| Creative iMedia | OCR J834 | 23 | 4 | 23/23 |
| Mathematics | Edexcel 1MA1 | 48 (practice-first) | 6 | No narration — practice format |
| Computer Science | OCR J277 | 23 | 2 (Computer Systems, Computational Thinking) | 23/23 |
| Design & Technology | AQA 8552 | 20 | 3 (Core Technical, Specialist Technical, Designing & Making) | 20/20 |
| Music Technology | NCFE 603/7008/7 | 15 | 5 (subscribed from generic, last year — remove Sept 2026) | 15/15 |
| **Subtotal** | | **598 + 21 practice** | | **584/584** |

## Subjects — Severn Vale School (school_id set)

| Subject | Exam Board | Lessons | Units | Podcasts |
|---------|-----------|---------|-------|----------|
| Combined Science (Biology) | AQA 8464 | 16 | 2 (Bio P1, Bio P2) — bespoke from teacher PPTs | 1/16 |
| + Chemistry & Physics | AQA 8464 | 32 | 4 (copied from generic) | 0/32 |

Teacher account: Alex Cameron (acameron@severnvaleschool.com), school code `vale2026`.

## Subjects — Free Tier (school_id NULL, generic content)

### Core subjects across all exam boards (NEW — Mar 2026)

| Subject | AQA | Edexcel | OCR | Eduqas | Total |
|---------|-----|---------|-----|--------|-------|
| English Language | 30 | 50 | 50 | 50 | 180 |
| English Literature | 214 | 215 | 156 | 190 | 775 |
| Mathematics | 48 | 48 | 48 | 48 | 192 |
| Combined Science | 48 | 48 | 48 | — | 144 |
| **Core total** | | | | | **1,291** |

### Other generic subjects

| Subject | Exam Board | Lessons |
|---------|-----------|---------|
| Separate Sciences | AQA 8461/8462/8463 | 22 |
| Health & Social Care | Pearson Edexcel | 12 |
| History | Edexcel 1HI0 | 36 |
| Religious Education | AQA 8062 | 28 |
| Hospitality & Catering | WJEC 5409 | 10 |
| Music Technology | NCFE 603/7008/7 | 15 |
| **Other total** | | **123** |

**Grand total: ~1,990 lessons across all subjects and boards.**

**Architecture:** `school_id = NULL` rows are generic/public content visible to free users. `school_id` set = school-specific bespoke content. Both tiers share the same templates and loaders.

Every subject has: content, practice questions (6/lesson), knowledge checks (5/lesson), flashcard questions (5/lesson), TTS narration (Azure Speech, MP3s on R2), hero images, exam technique guides, revision technique guides, related media (curated YouTube, study tools, documentaries, podcasts). **Diagrams are Unity-only** — Gemini diagrams were stripped from all free tier lessons on 22 Apr 2026 due to quality concerns; GPT-image-2 being evaluated as replacement (see Active TODO). **Cinematic videos are Unity-only** — free tier has none because NotebookLM's 20/day generation limit doesn't scale. **Exceptions using practice-first format** (`practice.html` + `practice-loader.js`): Maths (misconception detection, 5 maths input types), English Language (10 English input types including AI marking), Languages — Spanish/French/German (7 language input types including AI translation marking), and Science/Separate Sciences calculation units (equation recall drilling with hint toggle). No article narration/podcasts/flashcards/KCs for practice-first subjects. Science calculation units sit alongside article units (mixed format via `practice_units` in subject settings).

## Specification Database

193 GCSE specifications from all 4 exam boards, converted to markdown with YAML frontmatter. Used by the content generation pipeline as the authoritative source for each subject.

- **Location:** `specs/{board}/{slug}-{code}.md` — indexed by `specs/index.json`
- **Boards:** AQA (48), Edexcel (37), OCR (42), WJEC (32), Eduqas (34)
- **Script:** `python scripts/download_specs.py` — downloads PDFs from exam board websites, converts via `markitdown`, adds frontmatter
- **Usage:** Pipeline matches teacher's exam board + subject to the right spec file. Content agents receive the spec markdown as context.
- **Frontmatter:** `board`, `subject`, `spec_code`, `slug`
- **Two build modes:** Bespoke (teacher uploads resources + spec) or Generic (spec-only, no teacher input). Generic mode enables building every GCSE subject at scale. See `docs/PIPELINE.md` for the rebuilt master playbook and `docs/PLANNING_PROMPT.md` for lesson planning rules (exam weight scaling, unit structure, lesson count ranges, article-vs-practice mode decision).

## Dynamic Architecture (LIVE on Vercel)

All content served from Supabase. Static HTML files remain as backup.

- **~1,986 lessons** (535 Unity incl 21 practice + 48 Severn Vale + 1,389 generic) + **557 guide pages** in Supabase. Images on R2 (`studyvault-images`), audio on R2 (`studyvault-audio`), cinematic videos on R2 (`studyvault-video`).
- **Templates:** `lesson.html`, `browse.html`, `guide.html`, `practice.html` with JS loaders
- **URL scheme:** `/lesson/{subject}/{unit}/{number}`, `/practice/{subject}/{unit}/{number}` (maths, geography skills, english-language, spanish, french, german, science calculations), `/browse/{subject}/{unit?}`, `/guide/{subject}/{type}/{slug?}`, `/exams` (personal exam timetable + revision planner)
- **Mixed-format subjects:** `subjects.settings.practice_units` array lists which units use `/practice/` URLs. `browse-loader.js` checks this per unit. Example: Geography has article units (Paper 1, Paper 2) + practice unit (Geographical Skills). English Language has all 4 units as practice-first.
- **Auth (4 tiers):**
  - **Free users:** No login. Generic content (school_id NULL) + ads. Prefs stored in localStorage via `js/free-user.js`.
  - **School students:** Enter school code (stored in `schools.settings.student_code`). Validated via `api/auth/login.js`, stored in sessionStorage. Sees only subscribed subjects (restricted mode via `school_subscriptions` table), no ads.
  - **Teachers:** Individual Supabase Auth accounts (email + password). Invited by admin, sign up at `/teacher/signup?token=...`. Login at `/teacher/login`. Scoped to their school + assigned subjects via `teacher_subjects` table. Session stored in both sessionStorage and localStorage (cross-tab). Auth-gate supports `data-auth="teacher"` mode.
  - **Admin:** `ADMIN_PASSWORD` via `js/auth-gate.js`. Sees all schools/subjects. Shared password still works alongside Supabase Auth.
  - **Microsoft SSO:** Still pending Entra admin consent.
- **Admin pages:** `/admin/pipeline` (upload/generate), `/admin/review` (QC), `/admin/images` (image QA with school filter), `/admin/editor` (lesson editor), `/admin/editor-guide` (guide editor)
- **Teacher pages:** `/teacher/login`, `/teacher/signup`, `/teacher/dashboard` (demo data), `/teacher/review` → review.html, `/teacher/editor` → editor.html, `/teacher/upload` → pipeline.html
- **Supabase tables:** schools, profiles, subjects, units, lessons, guide_pages, school_subscriptions, user_selected_subjects, lesson_visits, knowledge_check_scores, content_pipeline_logs, upload_jobs, pipeline_steps, classes, class_members, teacher_invitations, teacher_subjects, notifications
- **R2 buckets:** `studyvault-audio` (`pub-f7b76d81365b4b2f954567763694a24e.r2.dev`), `studyvault-images` (`pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev`), `studyvault-video` (`pub-157a3979382e4f98b51f7f868078e5a3.r2.dev`)
- **Cookie consent:** Banner on all pages via `js/cookie-consent.js`. Privacy policy at `/privacy.html`.
- **Business email:** studyvault.info@gmail.com

## Active TODO

### Open work (still pending)
- **GPT-image-2 diagram evaluation** (parked) — quality much better than Gemini, ~£0.12/image, ~£400-700 full build-out cost. Two-step pipeline (Claude prompt → gpt-image-2). See `memory/gpt_image_2_evaluation.md`.
- **Revision planner: school holiday awareness** — needs per-school term dates before Sep 2026 cohort. Open design question on intensity (more / less / hybrid). See `memory/project_holiday_awareness.md`.
- **Revision planner: update exam dates annually** — `data/exam-dates-2026.json` needs new version each year from board timetables.
- **Practice question format review (English Literature)** — currently 30+4-mark full essays. Consider varied mix vs exam authenticity. Needs legal advice on copyright risk. See `GCSE Platform Copyright Risk Analysis.txt`.
- **Geography Skills L13 (Contours) and L14 (Map Interpretation) QA pass** — L11/L12 done with Tom; L13/L14 still need review.
- **Parents' evening print view** — dashboard section with quick-print per class.
- **Mobile app (Capacitor)** — wrap PWA for App Store + Google Play.
- **Dashboard progress widgets** — currently hardcoded demo data; need real Supabase queries.
- **Music Technology** — remove Unity subscription Sept 2026 (last year taught).

### Recent (last 6 weeks)
- **Pipeline rebuild v2 LIVE** (22 Apr) — entry point `docs/PIPELINE.md`. Old `SUBJECT_PLAYBOOK.md` / `PIPELINE_ARCHITECTURE.md` / `GENERATION_PROMPT.md` archived. Exam guides killed (per-question mark schemes carry the load). Revision guides templated in `docs/REVISION_TECHNIQUES/`. Reference lesson pinned: RE L01 "Worship & Prayer" (`21447890-d512-42c6-85f9-90b4133c06e3`). Free-tier ships as `pending_review`, no Gemini diagrams, no cinematic videos. See `memory/pipeline_rebuild_v2.md`.
- **Free tier picker v2 LIVE** (22 Apr) — 8-category accordion, search filter, "Soon" tags, core subjects auto-included. Welcome modal rework (1 May): two-column choice with subject-request callout, returns until decision made.
- **Launch polish LIVE** (26 Apr) — first-time lesson tutorial (coachmark steps, replay button), bug reporter (FAB → R2 + bug_reports → `/admin/bugs`), subject request feature (homepage `<details>` + wizard step 1, `/admin/requests`), About + FAQ pages, deck-reveal animation, lesson-notice modal (school-specific alerts), subject build verifier (`scripts/_verify_subject_build.py`). Code in `js/lesson-loader.js`, `js/bug-reporter.js`, `js/deck-reveal.js`. See `memory/project_launch_polish_session_2026-04-26.md`.
- **Email alerts on bug reports + subject requests LIVE** (1 May) — `/api/bug-report` and `/api/subject-request` send Resend email after DB insert. Env vars: `RESEND_API_KEY`, `NOTIFY_TO`, `NOTIFY_FROM`. Tom's Resend account is registered to a different inbox; Gmail filter forwards to `studyvault.info@gmail.com`. Awaiting `studyvault.co.uk` domain verification (registrar is auntie's account) before switching to branded sender.
- **Auto-sync unit.image_url from L1 hero LIVE** (2 May) — Postgres trigger `sync_unit_image_from_lesson_1_trg` on `lessons` table. Edit any lesson 1's `hero_image_url` and the parent unit's `image_url` updates automatically. Schema: `scripts/_create_unit_image_sync_trigger.sql`.
- **Validator catches HTML entities in plain-text fields** (2 May) — `scripts/_validate_content_json.py` fails files where `&rsquo;`, `&amp;`, etc. appear in `description` / `practice_questions` / `knowledge_checks` / `flashcard_questions` / `glossary_terms`. Rule: if field name ends in `_html` use entities, otherwise plain unicode. Documented at top of `docs/CONTENT_PROMPT.md`.

### Major builds completed
- **All 4 boards covered** for English Lang (180 lessons), English Lit (775), Maths (192 practice-format), Combined Science (Eduqas doesn't offer Combined — confirmed not a gap).
- **History Edexcel 1HI0 free-tier** (2 May) — 13 new units, 166 lessons. All assets (heroes, narration, podcasts, related media, revision guides). Joined the 4 existing Edexcel options for a 17-option picker.
- **Practice-first builds**: Maths (4 boards × 48), English Language (30 / 600 problems / 151 passages), Languages (Spanish/French/German × 26 / 1,560 problems / 234 dictation clips), Geography Skills (14 / 280 problems), Science Practice (21 / 420 problems).
- **Foundation/Higher tiering** (3 Apr) — 562 lessons across Maths, Sciences, Languages.
- **Exam Countdown LIVE** (`js/exam-countdown.js`) + **Exam Timetable & Revision Planner LIVE** at `/exams` (no AI, deterministic scheduling).
- **AI Marking API LIVE** at `/api/ai-mark` — Haiku ≤8 marks, Sonnet >8 marks, formative.
- **Cinematic videos COMPLETE** for Unity (552/552). Free-tier no videos (NotebookLM 20/day doesn't scale).
- **Podcasts**: 200/day via NotebookLM. Unity 526/526 done. New multi-board ~200 done, ~955 remaining.
- **Diagrams**: Unity-only — CS (19), D&T (14), 7 data-viz Chart.js, 57 Geography chart problems. Free-tier diagrams stripped 22 Apr; GPT-image-2 replacement under evaluation.
- **OS Map Skills** (4 Apr) — 28 OS OpenData maps + contour overlays at R2 `geography/os-maps/`.

### Schools
- **Severn Vale** — code `vale2026`. Bespoke Biology (16 from teacher PPTs), generic Chem/Physics. Teacher: Alex Cameron (individual Supabase Auth).
- **Unity College** — code `unitypassionrespect`. 17 bespoke subjects (16 + Maths copied from generic).

## API Keys

All in environment variables — never commit.

| Service | Env Var | Notes |
|---------|---------|-------|
| Gemini | `GEMINI_API_KEY` | Diagram generation |
| Supabase | `SUPABASE_URL` | Hardcoded in `index.html` (public) |
| Supabase | `SUPABASE_ANON_KEY` | Hardcoded in `index.html` (public) |
| Supabase | `SUPABASE_SERVICE_KEY` | Server-side only, never commit |
| Azure Speech | `AZURE_SPEECH_KEY` | Region: `uksouth` |
| R2 | `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_ACCOUNT_ID` | Cloudflare R2 |
| Unsplash | `UNSPLASH_ACCESS_KEY` | Hero image search |
| ElevenLabs | `ELEVENLABS_API_KEY` | TTS fallback (unused) |
| Admin auth | `ADMIN_PASSWORD` | Gates `/admin/pipeline`, `/admin/review`, `/admin/images` |
| Teacher auth | `TEACHER_PASSWORD` | Shared password fallback (Unity-scoped). Individual teacher accounts preferred. |
| Azure Speech | `AZURE_SPEECH_KEY` | Region: `uksouth`. Pay-as-you-go (upgraded from free tier 27 Mar 2026). |

## Key Conventions

- **Design:** Background `#faf8f5`, text `#2d2a26`, Inter + Source Serif 4, `border-radius: 16px`, soft shadows
- **Images:** Heroes max 1200px, diagrams max 1000px, JPEG quality 82
- **Content:** 6 practice questions + 5 knowledge checks per lesson. Readability for GCSE age 15-16.
- **Narration:** Azure Speech, Ollie (odd lessons) / Ada (even — replaced Bella 21 Mar 2026), MP3 96kbps 24kHz mono. Language subjects (French/German/Spanish) use multilingual voices (`OllieMultilingualNeural` + `AdaMultilingualNeural`) with SSML `<lang>` tags for foreign phrases. Foreign text must be in `<em>` or `<strong>` tags for auto-detection. See `docs/NARRATION_PIPELINE.md`.
- **PPTs:** Read with `python -m markitdown "filepath"` (.pptx only)
- **Equations (KaTeX):** Maths/science equations use KaTeX auto-render. Inline: `\(...\)`, display: `$$...$$`. CDN loaded on `lesson.html` and `guide.html`. `docs/CONTENT_PROMPT.md` instructs future content to output LaTeX (not HTML entities). Conversion script: `scripts/convert_equations_to_katex.py`.
- **Animations:** Soft-close damping `cubic-bezier(0.16, 1, 0.3, 1)` on all entrance animations. `.sv-reveal` / `.sv-stagger` CSS classes + IntersectionObserver. Split timing: fast opacity (~0.5s), slow transform glide (~1-1.3s). `prefers-reduced-motion` respected. Browse page unit cards have no scroll reveal (all visible immediately so students don't miss units below the fold).

## Reference Docs (read on demand)

**Start here for any new subject build:** `docs/PIPELINE.md` — master playbook covering both free-tier and Unity modes, both article and practice formats.

| Doc | When to read |
|-----|-------------|
| `docs/PIPELINE.md` | **Entry point** — building a new subject. Replaces old `SUBJECT_PLAYBOOK.md` |
| `docs/PLANNING_PROMPT.md` | Phase 1 — planning agent prompt (research + mode decision + plan JSON) |
| `docs/CONTENT_PROMPT.md` | Phase 3 article — content agent system prompt + output schema |
| `docs/PRACTICE_PIPELINE.md` | Phase 3 practice — factory stages for practice-format lessons |
| `docs/REFERENCE_LESSONS.md` | Pinned Supabase IDs of structural example lessons |
| `docs/REVISION_TECHNIQUES/` | 7 canonical technique templates (fill in subject examples only) |
| `docs/LESSON_TEMPLATE.md` | HTML components reference for article lessons |
| `docs/QUESTIONS_PIPELINE.md` | Practice question formats, mark allocations, `getGuideUrl()` mappings |
| `docs/DIAGRAM_PIPELINE.md` | Unity-only: Gemini diagrams. GPT-image-2 replacement under evaluation |
| `docs/NARRATION_PIPELINE.md` | TTS narration (Ollie/Ada, multilingual SSML) |
| `docs/VIDEO_PIPELINE.md` | Unity-only: cinematic videos. Both tiers: podcasts (NotebookLM) |
| `docs/RELATED_MEDIA_PIPELINE.md` | Related media agent prompt. Podcast-into-related-media contract |
| `docs/UNIT_THEMES.md` | Unit body classes and accent colours |
| `docs/FUTURE_FEATURES.md` | Planned features and wishlist |
| `docs/SUBJECT_ROADMAP.md` | Subjects built and still to build |
| `docs/FILE_STRUCTURE.md` | Repo file/folder layout |
| `docs/COMMERCIALISATION.md` | Pricing, cost model, commercial strategy |
| `docs/archive/` | Superseded docs (pre-rebuild). Do not generate from these |
| `scripts/science-practice/SCIENCE_PRACTICE_SCHEMA.md` | Science practice data format, equation reference |
| `scripts/language-practice/PRACTICE_DATA_SCHEMA.md` | Language practice data format, 12 input types |
| `scripts/factory/FACTORY_RULES.md` | English Language factory stage rules |
| `data/exam-dates-2026.json` | All GCSE exam dates by board, plus Unity board mapping |
| `{subject}/BUILD_PLAN.md` | Subject-specific lesson breakdown |
| `tts-research-log.md` | TTS/voice cloning developments |
| `tech-research-log.md` | EdTech/platform developments |

## JS Architecture (main.js)

**Phase 1** (DOMContentLoaded): scroll progress, mobile nav, accessibility toolbar, page transitions, `initRevealAnimations()` (scroll-triggered entrance animations)
**Phase 2** (`window.initLessonFeatures()`, called after content injection): collapsibles, visited tracking, practice questions, narration, glossary tooltips, knowledge check, lightbox, revision tips, nav icons, lesson pill

**Dynamic loaders:** `lesson-loader.js`, `browse-loader.js`, `guide-loader.js` — auth check → Supabase fetch → populate template → init features. `guide-loader.js` has school_id scoping (fetches school-specific guides when logged in as school student).

## Sidebar Structure

Three sections: **Knowledge Check** (button → modal), **Related Media** (collapsible categories), **Video** (YouTube embed or Google Drive modal). Do NOT add a "Key Facts" section. See `docs/RELATED_MEDIA_PIPELINE.md` for media curation.

## Video Embeds

- **YouTube:** Store YouTube video ID in `lessons.youtube_video_id`. Renders inline iframe in sidebar.
- **Google Drive:** Store full Google Drive `/preview` URL in `lessons.youtube_video_id` (e.g. `https://drive.google.com/file/d/{FILE_ID}/preview`). `lesson-loader.js` detects `drive.google.com`, shows thumbnail + play button in sidebar, opens video in a large modal overlay on click. CSS class `sidebar-video--gdrive`.
- **R2 Video:** Store R2 URL (containing `r2.dev/` or ending `.mp4`) in `lessons.youtube_video_id`. Renders dark thumbnail card with play button in sidebar, opens native `<video>` element in modal overlay (`preload="metadata"`, no autoplay). Bucket: `studyvault-video` (`pub-157a3979382e4f98b51f7f868078e5a3.r2.dev`).
- **Sharing:** Google Drive files must be set to "Anyone with the link can view" for embed to work.
