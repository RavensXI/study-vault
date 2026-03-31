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
| Geography | AQA 8035 | 40 | 2 papers | 40/40 |
| Sport Science | OCR R180 | 10 | 1 (R180) | 10/10 |
| Drama | OCR J316 | 12 | 2 (Blood Brothers, Rise Up) | 12/12 |
| Food Technology | AQA 8585 | 10 | 1 (Nutrition & Health) | 10/10 |
| Religious Education | AQA 8062 | 40 | 8 | 40/40 |
| Music | Eduqas C660U | 26 | 6 | 26/26 |
| English Literature | AQA 8702 | 42 | 5 | 42/42 |
| English Language | AQA 8700 | 30 | 4 | 30/30 |
| Science | AQA 8464 | 48 | 6 | 48/48 |
| Separate Sciences | AQA 8461/8462/8463 | 22 | 3 | 22/22 |
| Spanish | AQA 8692 | 26 | 3 | 26/26 |
| German | AQA 8662 | 26 | 3 | 26/26 |
| French | AQA 8652 | 26 | 3 | 26/26 |
| Creative iMedia | OCR J834 | 23 | 4 | 23/23 |
| Mathematics | Edexcel 1MA1 | 48 (practice-first) | 6 | No narration — practice format |
| Music Technology | NCFE 603/7008/7 | 15 | 5 (subscribed from generic, last year — remove Sept 2026) | 15/15 |
| **Subtotal** | | **541** | | **541/541** |

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
| Mathematics | — | 48 (Edexcel only, practice-first rebuild) | — | — | 48 |
| Combined Science | 48 | 48 | 48 | — | 144 |
| **Core total** | | | | | **1,337** |

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

**Grand total: ~1,986 lessons across all subjects and boards.**

**Architecture:** `school_id = NULL` rows are generic/public content visible to free users. `school_id` set = school-specific bespoke content. Both tiers share the same templates and loaders.

Every subject has: content, practice questions (6/lesson), knowledge checks (5/lesson), flashcard questions (5/lesson), TTS narration (Azure Speech, MP3s on R2), hero images, exam technique guides, revision technique guides, related media (curated YouTube, study tools, documentaries, podcasts). Gemini diagrams only on older subjects — new multi-board content pending. **Exception: Maths** uses practice-first format (`practice.html` + `practice-loader.js`) with method cards, worked examples, graded problem banks with misconception detection. No narration, podcasts, flashcards, or knowledge checks.

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

- **~1,986 lessons** (541 Unity + 48 Severn Vale + ~1,460 generic) + **~535 guide pages** in Supabase. Images on R2 (`studyvault-images`), audio on R2 (`studyvault-audio`), cinematic videos on R2 (`studyvault-video`).
- **Templates:** `lesson.html`, `browse.html`, `guide.html`, `practice.html` with JS loaders
- **URL scheme:** `/lesson/{subject}/{unit}/{number}`, `/practice/{subject}/{unit}/{number}` (maths), `/browse/{subject}/{unit?}`, `/guide/{subject}/{type}/{slug?}`
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
- **Maths REBUILT as practice-first format** (31 Mar 2026) — Old multi-board content deleted (296 lessons). Rebuilding Edexcel 1MA1 only: 48 lessons (30 Foundation, 18 Higher) across 6 units. Practice format: method card modal, worked examples with step reveals, 20 graded problems (Bronze/Silver/Gold) with misconception detection. Tier pass: 4-in-a-row or 75%. No narration/podcasts/flashcards/KCs. Template: `practice.html` + `practice-loader.js`. Data: `practice_data` JSONB column. Test lesson live: `/practice/maths/algebra/7`. Other boards (OCR, AQA, Eduqas) to follow after Edexcel validated.
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
- **Cinematic video overviews** — 20/day via NotebookLM. `scripts/generate_cinematic_videos.py` (rewritten 27 Mar 2026): Supabase is the source of truth (no state file). Queries for lessons with no `youtube_video_id`, creates notebook, generates video, downloads to R2, updates Supabase. Sessions file (`_cinematic_sessions.json`) is ephemeral scratch for active renders only. Unity progress: 187/526 (6 subjects complete: Drama, English Language, English Literature, Food Tech, Science, Sport Science. History 35/60 in progress). ~17 days remaining at 20/day.
- **Podcasts in progress** — 200/day via NotebookLM. `scripts/batch_podcasts.py` handles create → poll → download → R2 upload → Supabase update. ~200 done for Science + Eng Lang, ~955 remaining (mostly Eng Lit). Prompt includes unit context (covered/upcoming lessons) and varied opening instructions (no more "imagine").
- **Diagrams not yet generated** for new multi-board content (Gemini generation pending).
- **Dashboard progress**: Hardcoded demo data — need real Supabase queries.
- **Homepage subject filtering LIVE** (28 Mar 2026) — School students only see bespoke + subscribed subjects. Maths added as locked core subject alongside English and Science.
- **Mobile editor LIVE** (26 Mar 2026) — Floating action button (bottom-right) opens slide-up sidebar with Save/Discard/Preview. Body `transform: none` override fixes `position: fixed`.
- **Remaining subjects to build**: Computer Science (OCR), Design & Technology (AQA).
- **Parents' evening print view**: Dashboard section with quick-print option per class.
- **Mobile app (Capacitor)**: Wrap existing PWA for App Store + Google Play.

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
