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
| English Literature | 197 | 215 | 156 | 182 | 750 |
| Mathematics | 48 | 48 | 48 | 48 | 192 |
| Combined Science | 48 | 48 | 48 | — | 144 |
| **Core total** | | | | | **1,266** |

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

**Grand total: ~1,965 lessons across all subjects and boards.**

**Architecture:** `school_id = NULL` rows are generic/public content visible to free users. `school_id` set = school-specific bespoke content. Both tiers share the same templates and loaders.

Every subject has: content, practice questions (6/lesson), knowledge checks (5/lesson), flashcard questions (5/lesson), TTS narration (Azure Speech, MP3s on R2), hero images, exam technique guides, revision technique guides, related media (curated YouTube, study tools, documentaries, podcasts). Gemini diagrams only on older subjects — new multi-board content pending. **Exceptions using practice-first format** (`practice.html` + `practice-loader.js`): Maths (misconception detection, 5 maths input types), English Language (10 English input types including AI marking), Languages — Spanish/French/German (7 language input types including AI translation marking), and Science/Separate Sciences calculation units (equation recall drilling with hint toggle). No article narration/podcasts/flashcards/KCs for practice-first subjects. Science calculation units sit alongside article units (mixed format via `practice_units` in subject settings).

## Specification Database

193 GCSE specifications from all 4 exam boards, converted to markdown with YAML frontmatter. Used by the content generation pipeline as the authoritative source for each subject.

- **Location:** `specs/{board}/{slug}-{code}.md` — indexed by `specs/index.json`
- **Boards:** AQA (48), Edexcel (37), OCR (42), WJEC (32), Eduqas (34)
- **Script:** `python scripts/download_specs.py` — downloads PDFs from exam board websites, converts via `markitdown`, adds frontmatter
- **Usage:** Pipeline matches teacher's exam board + subject to the right spec file. Content agents receive the spec markdown as context.
- **Frontmatter:** `board`, `subject`, `spec_code`, `slug`
- **Two build modes:** Bespoke (teacher uploads resources + spec) or Generic (spec-only, no teacher input). Generic mode enables building every GCSE subject at scale. See `docs/SUBJECT_PLAYBOOK.md` for automated lesson planning rules (exam weight scaling, unit structure, lesson count ranges).

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
- **Multi-board core subjects COMPLETE** (30 Mar 2026) — English Language (4 boards, 180 lessons), English Literature (4 boards, 750 lessons), Combined Science (3 boards, 144 lessons). All have: content, heroes, narration, related media, guide pages (exam technique + revision technique). All `pending_review` status.
- **Maths COMPLETE — practice-first format, all 4 boards** (2 Apr 2026) — 192 lessons (48 per board × 4: Edexcel, AQA, OCR, Eduqas), 3,833 problems. Practice format: method card modal, worked examples with step reveals, 20 graded problems (Bronze/Silver/Gold) with misconception detection. 5 input types: single_value, two_solutions, fraction, standard_form, multiple_choice. Calculator/non-calculator flags on every problem. Chart.js data visualisation (bar, pie, scatter, line, boxplot, histogram). Tier pass: 4-in-a-row or 75%. No narration/podcasts/flashcards/KCs. Template: `practice.html` + `practice-loader.js`. Data: `practice_data` JSONB column. Foundation/Higher tier filtering.
- **Language Practice COMPLETE** (12 Apr 2026) — Spanish, French, German converted from article to practice-first format. 78 lessons, 1,560 problems, 234 dictation audio clips on R2. 7 new input types: `vocab_match` (tap-to-match pairs), `gap_fill` (word bank or free input with structured grammar feedback), `translate` (bidirectional, AI-marked via Haiku), `dictation` (Azure TTS audio, word-by-word diff scoring), `sentence_builder` (word tiles with grammar distractors), `spot_correct` (find and fix one grammar error), `role_play` (AQA Paper 2 scenario cards, AI-marked). All use `target_lang` field (es/fr/de) for language-specific accent bars. Method cards condensed from original article content. 312 Gold problems flagged `higher_only` for F/H filtering. Pipeline: `scripts/language-practice/` with schema, generation JSONs, insertion script, and audio generation script. Prototypes at `prototypes/` for reference.
- **Foundation/Higher tier filtering COMPLETE** (3 Apr 2026, extended 12 Apr 2026) — 484 article lessons + 78 language practice lessons across all tiered subjects. Article lessons: in-content `<div class="higher-only">` wrapping hides HT sections. Practice lessons: `higher_only: true` flag on problems, `practice-loader.js` filters them out for Foundation students. Wizard tier picker → `studyvault-tiers` localStorage. Subjects: Maths (192 practice-format, F/H per lesson), Combined Science AQA/Edexcel/OCR (192 lessons, 53 wrapped), Separate Sciences AQA (22 lessons, 14 wrapped), French (26, 312 higher_only problems), German (26), Spanish (26).
- **Science Practice Mode COMPLETE** (13 Apr 2026) — 21 lessons, 420 problems across 4 new practice units. Combined Science: Physics Calculations (8 lessons, 160 problems, blue `#2563eb`), Chemistry Calculations (4 lessons, 80 problems, red `#dc2626`), Biology Data Skills (3 lessons, 60 problems, green `#16a34a`). Separate Sciences: Higher Calculations (6 lessons, 120 problems, purple `#7c3aed`). Equation hint toggle: Bronze/Silver show per-problem "Show equation" button, Gold = pure recall (no hints). Method cards show strategy only, not equations. 7 higher_only problems (momentum, v²=u²+2as). Chart.js graphs for rates, d-t, v-t. Standard form input for large/small values. Scripts: `scripts/science-practice/` (schema, JSON source files, insertion script).
- **Exam Countdown LIVE** (14 Apr 2026) — Compact pill showing days until next exam. Practice pages: header left dead space. Lesson pages: above title. Browse pages: inside hero. Amber <30 days, red <7 days. Dismissible via sessionStorage. Detects board per subject via `window._examBoard`. Exam dates in `data/exam-dates-2026.json` (AQA timetable + JCQ common timetable for Edexcel/OCR/Eduqas). Per-subject board mapping for Unity in `unity_boards` key. JS: `js/exam-countdown.js`, included on `browse.html`, `lesson.html`, `practice.html`.
- **Exam Timetable & Revision Planner LIVE** (14 Apr 2026) — Personal revision planner at `/exams` (`exams.html`). Auto-builds on page load from student's homepage subject picks (localStorage `studyvault-subjects` + locked core subjects). Calendar month-view (April/May/June) as main UI. Red exam pills + subject-coloured revision pills. Scheduling algorithm: pulls real lesson titles from Supabase, maps units to exam papers via `UNIT_PAPER_MAP`, distributes topics deterministically. Priority = `remaining_topics / days_until_exam` with starvation safety net (3-day minimum frequency, only within 21 days of exam). Paper-aware: P1 content before P1 exam, P2 before P2. Per-subject board lookup (`unity_boards`). Combined Science included for separate-sciences students. Generic/subscribed subjects (Maths on Edexcel) fetched as fallback. Intensity ramping: >120 days = 1/day, >60 days = 2/day, ≤60 days = 3/day. Topic recycling for spaced repetition over a full academic year. Rest day picker (Sunday/Saturday). ICS calendar export with device-specific instructions. Print: landscape, calendar only. No AI cost. Homepage link: "My Exam Timetable" pill next to "Your subjects". BST timezone fix: uses local date formatting not `toISOString()`.
- **Severn Vale School LIVE** — school code `vale2026`. Bespoke Biology (16 lessons from teacher PPTs) + generic Chem/Physics. Teacher: Alex Cameron (individual Supabase Auth account). Upload page at `/teacher/upload`.
- **Teacher URLs LIVE** (26 Mar 2026) — `/teacher/review`, `/teacher/editor`, `/teacher/upload` rewrite to admin pages. School-scoped via `getAuthContext()`.
- **Sign out button LIVE** (28 Mar 2026) — Red "Sign out" in header nav on all auth-gated pages. Clears sessionStorage, localStorage, and Supabase Auth.
- **Review page optimised** (28 Mar 2026) — First load fetches full summary, subsequent Apply clicks use `lessons_only=1` to skip expensive count queries.
- **Music Technology LIVE** (30 Mar 2026) — NCFE 603/7008/7. 15 lessons, 5 units, generic (school_id NULL) + Unity subscription. First non-standard board (NCFE). All assets complete. **Remove Unity subscription Sept 2026** (last year taught).
- **Podcast RSS feeds LIVE** (30 Mar 2026) — API route at `/api/podcast/feed?subject={slug}&school={id_or_code}`. Generates valid RSS XML with all podcast episodes in curriculum order. School-aware (passes school_id for bespoke subjects). Subscribe modal on lesson pages with copy-to-clipboard. Works with Pocket Casts, Apple Podcasts, Overcast, etc. Image slug mapping handles mismatched filenames.
- **Podcast resume LIVE** (30 Mar 2026) — Saves podcast playback position to localStorage every ~5 seconds + on page unload. Resumes from saved position when student returns. Clears on episode completion.
- **Guide page templates** (30 Mar 2026) — `docs/EXAM_TECHNIQUE_TEMPLATE.md` and `docs/REVISION_TECHNIQUE_TEMPLATE.md` provide fixed HTML structures for guide agents to fill in. Prevents formatting drift from agents generating HTML from scratch. Playbook updated to require template usage.
- **Image QA page** — School filter dropdown added. Subject/unit filters scope by subject_id to handle duplicate slugs across schools. Unit filter persistence fixed (was resetting on reload).
- **KaTeX in modals FIXED** (25 Mar 2026) — Quick Quiz and Flashcard modals now call `renderKaTeX()` after injecting content. Maths equations render properly.
- **Preview banner grid fix** (25 Mar 2026) — `grid-column: 1/-1` on preview banner prevents it breaking the two-column layout.
- **Accent CSS variables from DB** (25 Mar 2026) — `lesson-loader.js` sets `--accent`/`--accent-light`/`--accent-badge` via `style.setProperty` from unit DB values. No CSS body class needed for new units.
- **RLS fix** (25 Mar 2026) — Added `Public read access on lessons` SELECT policy so anon key can read all lessons (content is revision material, not sensitive). JS handles status visibility.
- **Cinematic video overviews COMPLETE** (15 Apr 2026) — All Unity College lessons done. 552/552 (439 R2 videos + 113 practice-only). 17 batches over 16 days (30 Mar – 15 Apr) via NotebookLM (20/day limit). `scripts/generate_cinematic_videos.py`: Supabase is source of truth, queries lessons with no `youtube_video_id`, creates notebook, generates video, downloads to R2, updates Supabase. Sessions file (`_cinematic_sessions.json`) is ephemeral scratch. Practice-only lessons (Geography Skills, Maths, English Language, Languages, Science calculations, Sep Sci calculations) marked with `youtube_video_id = 'practice-only'`. Script filtered to Unity school only (`UNITY_SCHOOL_ID`). See `memory/cinematic_video_log.md` for full batch log and `memory/feedback_cinematic_video_download.md` for download verification rules.
- **Podcasts in progress** — 200/day via NotebookLM. `scripts/batch_podcasts.py` handles create → poll → download → R2 upload → Supabase update. ~200 done for Science + Eng Lang, ~955 remaining (mostly Eng Lit). Prompt includes unit context (covered/upcoming lessons) and varied opening instructions (no more "imagine").
- **Diagrams:** Gemini-generated for CS (19) and D&T (14), plus Chart.js interactive charts for 7 data-visualisation lessons + 57 geography chart problems. Chart.js loaded on `lesson.html` + `practice.html` via CDN; lesson diagrams stored as `data-chart` JSON attribute on `<canvas>` elements, rendered by `lesson-loader.js` (100ms setTimeout for DOM layout). Practice page charts rendered inline. Multi-board content diagrams still pending.
- **OS Map Skills** (4 Apr 2026) — 28 real OS OpenData map images with contour overlays from OS Terrain 50. Maps captured programmatically from os.openstreetmap.org tiles at zoom 15 and 16. Grid lines with numbered eastings/northings overlaid via PIL. Contours at 10m intervals (50m index contours labelled). All free under Open Government Licence with attribution. Images at `images/os-maps/` and R2 `geography/os-maps/`. Map viewer tool at `test-os-viewer.html`.
- **Dashboard progress**: Hardcoded demo data — need real Supabase queries.
- **Homepage subject filtering LIVE** (28 Mar 2026) — School students only see bespoke + subscribed subjects. Maths added as locked core subject alongside English and Science.
- **Mobile editor LIVE** (26 Mar 2026) — Floating action button (bottom-right) opens slide-up sidebar with Save/Discard/Preview. Body `transform: none` override fixes `position: fixed`.
- **Computer Science COMPLETE** (3 Apr 2026) — OCR J277, Unity College. 23 lessons, 2 units (Computer Systems + Computational Thinking). Full pipeline: content, heroes, narration, podcasts, 95 curated videos, 15 guide pages, 33 diagrams (19 Gemini + 7 Chart.js). QA'd.
- **Design & Technology COMPLETE** (3 Apr 2026) — AQA 8552, Unity College. 20 lessons, 3 units (Core Technical + Specialist Technical + Designing & Making). Full pipeline: content, heroes, narration, podcasts, 136 curated media items, 14 guide pages, 17 diagrams (14 Gemini + 3 Chart.js). QA'd. All material categories covered broadly.
- **Geography Skills unit — QA & enhancements** (10-12 Apr 2026) — 14 practice lessons in Unity Geography (AQA 8035). Major practice page improvements:
  - **Chart panel** (10 Apr): Charts now render in the large centre passage panel instead of the small inline container. `handlePassagePanel()` detects `p.chart` and routes to `renderChartPanel()`. Roughly doubles chart size. Mobile tab label switches to "Chart".
  - **Image panel** (10 Apr): Static images (maps, diagrams) render in the centre panel via `p.image` field. Used for L8-L9 generated maps and L11-L14 OS maps. Click-to-fullscreen via lightbox.
  - **Statistics tools** (10 Apr): Four contextual tools in the centre panel for L5-L7: Number Sorter (drag to reorder for median/quartile), Range Finder (select highest/lowest), Tally Counter (count frequency for mode), Calculator (basic arithmetic). Tool auto-detected from question keywords + `calculator` flag.
  - **Ruler tool** (11 Apr): Digital ruler for L12 distance questions. Click two points on OS map → shows distance in cm on map + scale (e.g. "6.2 cm · Scale 1:25,000 (4 cm = 1 km)"). Students calculate real distance themselves. Fullscreen button for closer look. z15 maps = 1:50,000, z16 maps = 1:25,000.
  - **Question formatting** (10 Apr): `formatDisplay()` adds line breaks before instruction keywords (Explain, Calculate, etc.) and after colons before data series. Non-breaking spaces in data pairs (mean = 12).
  - **Six-figure GR tolerance** (11 Apr): Accepts ±1 on easting and northing independently. Input strips spaces/commas (accepts "842324", "842 324", "842,324").
  - **Method cards trimmed** (10 Apr): All 14 Geography Skills method cards shortened — punchy steps, max 5, no full sentences.
  - **Generated maps** (10-11 Apr): Cartopy + Natural Earth for consistent style. L8: choropleth (2021 census data), isotherm, isobar, isohyet over real UK coastlines. L9: proportional symbol (15 UK cities by population), flow line (internal migration). All on R2 at `geography/geographical-skills/maps/`. Script: `scripts/_gen_isoline_maps.py`, `scripts/_gen_l9_maps.py`.
  - **OS map fixes** (11 Apr): L11-L14 questions had inline `<img>` tags — moved to `image` field. Silver/gold questions swapped from z15 (too zoomed out) to z16 maps. All 80 questions audited against actual maps. L11 and L12 fully QA'd with Tom — feature names, grid references, and answers verified. L13-L14 still need QA pass.
  - **Unit hero image** (10 Apr): Lake District OS map uploaded as Geographical Skills unit card image.
- **English Language COMPLETE — practice-first format, all 4 units** (8 Apr 2026) — 30 lessons (8+8+7+7), 600 problems (20/lesson), 151 original passages narrated by 6 Azure voices. Practice format: method card, worked examples with step reveals, 20 graded problems (Bronze/Silver/Gold). 10 input types: traffic_light (dynamic categories, up to 8), highlight_evidence (contiguous word selection), connotation_picker, multiple_choice, evidence_match, ai_mark (Haiku ≤8m, Sonnet >8m), misleading_summary, ai_write, improve_sentence, spot_error, reorder. AI marking via `/api/ai-mark` with tier-based routing. Passage panel with a11y tools (TTS, OpenDyslexic, 6 colour overlays). Mobile: tab toggle between Extract/Question views, long-press highlight. Dark mode. Pre-recorded passage narration (6 voices: Ada, Ollie, Olivia, Nova Turbo, Shimmer Turbo, Andrew). Factory pipeline: `scripts/factory/` with stage-based generation, `FACTORY_RULES.md` for content rules.
- **AI Marking API LIVE** (8 Apr 2026, updated 12 Apr 2026) — `/api/ai-mark` Vercel serverless route. Tier-based routing: ≤8 marks → Haiku 4.5 (fast, cheap), >8 marks → Sonnet 4.6 (exam-level). System prompts per question type: inference_analysis, language_analysis, structure_analysis, evaluation, full_evaluation, comparison, full_comparison, creative_writing, creative_writing_extended, improve_sentence, improve_argument + translate_to_target, role_play, writing (language subjects). `engCheckAI` now passes `source_text`, `model_answers`, `direction` for translations and `scenario`, `bullets` with model answers for role plays — prevents AI marking wrong translations as correct. Formative marking: rewards insight over format, doesn't require embedded quotation.
- **Practice page dark mode LIVE** (8 Apr 2026) — Toggle in score bar, syncs with lesson page via `studyvault-a11y` localStorage. Flash prevention on load. Covers all input types, passage panel, modals, feedback.
- **Practice page mobile UX** (8 Apr 2026) — Tab toggle between Extract and Question views on <900px. Long-press + drag or long-press + tap-endpoint for text highlighting. Auto-scroll to next button and worked example steps.
- **Practice page layout** (8 Apr 2026) — Sidebar extends to top of viewport with split header (sidebar colour left, solid white right). Score bar: a11y tools centred over left column, tier/score centred over right column. Static header (not fixed). Accent-coloured thin scrollbars. Related media from lesson `related_media` field (not duplicated in practice_data).
- **Parents' evening print view**: Dashboard section with quick-print option per class.
- **Mobile app (Capacitor)**: Wrap existing PWA for App Store + Google Play.
- **Revision planner: school holiday awareness (Sep 2026)**: Planner currently schedules every day regardless of holidays. Before the next cohort starts in September, add per-school term dates (in `schools` table or `schools.settings`) so the planner can adjust intensity around half terms, Christmas, Easter. Open design question: should holidays mean MORE revision (students are free all day), LESS (they need a break), or a HYBRID (term time = light, holidays = medium, Easter = intensive)? Could also be a student toggle. See `memory/project_holiday_awareness.md` for full notes.
- **Revision planner: update exam dates annually**: `data/exam-dates-2026.json` needs a new version each year extracted from the AQA/Edexcel/OCR/Eduqas timetable PDFs. The `unity_boards` mapping may also need updating if subjects change board.

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
- **Equations (KaTeX):** Maths/science equations use KaTeX auto-render. Inline: `\(...\)`, display: `$$...$$`. CDN loaded on `lesson.html` and `guide.html`. `docs/GENERATION_PROMPT.md` instructs future content to output LaTeX (not HTML entities). Conversion script: `scripts/convert_equations_to_katex.py`.
- **Animations:** Soft-close damping `cubic-bezier(0.16, 1, 0.3, 1)` on all entrance animations. `.sv-reveal` / `.sv-stagger` CSS classes + IntersectionObserver. Split timing: fast opacity (~0.5s), slow transform glide (~1-1.3s). `prefers-reduced-motion` respected. Browse page unit cards have no scroll reveal (all visible immediately so students don't miss units below the fold).

## Reference Docs (read on demand)

| Doc | When to read |
|-----|-------------|
| `docs/LESSON_TEMPLATE.md` | Building or editing lesson content |
| `docs/QUESTIONS_PIPELINE.md` | Writing questions for any subject |
| `docs/DIAGRAM_PIPELINE.md` | Creating or updating diagrams |
| `docs/NARRATION_PIPELINE.md` | TTS narration work |
| `docs/VIDEO_PIPELINE.md` | NotebookLM cinematic videos & podcasts |
| `docs/RELATED_MEDIA_PIPELINE.md` | Adding sidebar media |
| `docs/GENERATION_PROMPT.md` | Content generation (inject-at-call-time prompt) |
| `docs/PIPELINE_ARCHITECTURE.md` | Full pipeline architecture |
| `docs/SUBJECT_PLAYBOOK.md` | Running the one-shot pipeline for a new subject |
| `docs/EXAM_TECHNIQUE_TEMPLATE.md` | HTML template for exam technique guide pages |
| `docs/REVISION_TECHNIQUE_TEMPLATE.md` | HTML template for revision technique guide pages |
| `docs/UNIT_THEMES.md` | Unit body classes and accent colours |
| `docs/FUTURE_FEATURES.md` | Planned features and wishlist |
| `docs/SUBJECT_ROADMAP.md` | Subjects built and still to build (14 remaining) |
| `docs/FILE_STRUCTURE.md` | Repo file/folder layout |
| `docs/COMMERCIALISATION.md` | Pricing, cost model, commercial strategy |
| `scripts/science-practice/SCIENCE_PRACTICE_SCHEMA.md` | Science practice data format, equation reference (recall vs given) |
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
