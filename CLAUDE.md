# StudyVault — Project Reference

Multi-subject GCSE revision site. Repo: https://github.com/RavensXI/study-vault

### Deployments
- **GitHub Pages** (`main`): https://ravensxi.github.io/study-vault/ — History only, no login
- **Vercel** (`platform`): https://study-vault-alpha.vercel.app/ — full platform, public content, admin/teacher login

### Owner
Tom Shaun — `t.shaun@unity.lancs.sch.uk` / git: `tomshaun90@gmail.com`

---

## Branches
- **`main`** — History at root level. Single-subject, no login.
- **`platform`** (current) — multi-subject. History under `history/`. Public content, school login for students, password-gated admin/teacher areas, 20 subjects (15 school-specific + 5 generic free-tier).

## Subjects — Unity College (school_id set, all on Vercel)

| Subject | Exam Board | Lessons | Units | Cinematic Videos | Podcasts |
|---------|-----------|---------|-------|-----------------|----------|
| History | AQA | 60 | 4 (Conflict, Health, Elizabethan, America) | 0/60 | 60/60 |
| Business Studies | Edexcel 1BS0 | 30 | 2 themes | 0/30 | 30/30 |
| Geography | AQA 8035 | 40 | 2 papers | 0/40 | 40/40 |
| Sport Science | OCR R180 | 10 | 1 (R180) | 9/10 | 10/10 |
| Drama | OCR J316 | 12 | 2 (Blood Brothers, Rise Up) | 0/12 | 12/12 |
| Food Technology | AQA 8585 | 10 | 1 (Nutrition & Health) | 7/10 | 10/10 |
| Religious Education | AQA 8062 | 40 | 8 | 0/40 | 40/40 |
| Music | Eduqas C660U | 26 | 6 (Elements, Forms, Ensemble, Popular, Film, Toto Africa) | 0/26 | 26/26 |
| English Literature | AQA 8702 | 42 | 5 (Macbeth, A Christmas Carol, Animal Farm, Power & Conflict, Unseen Poetry) | 0/42 | 42/42 |
| English Language | AQA 8700 | 30 | 4 (P1 Reading, P1 Writing, P2 Reading, P2 Writing) | 0/30 | 30/30 |
| Science | AQA 8464 | 48 | 6 (Bio P1, Bio P2, Chem P1, Chem P2, Phys P1, Phys P2) | 20/48 | 0/48 |
| Separate Sciences | AQA 8461/8462/8463 | 22 | 3 (Biology, Chemistry, Physics) | 0/22 | 0/22 |
| Spanish | AQA 8692 | 26 | 3 (People & Lifestyle, Popular Culture, Communication & World) | 0/26 | 0/26 |
| German | AQA 8662 | 26 | 3 (People & Lifestyle, Popular Culture, Communication & World) | 0/26 | 0/26 |
| French | AQA 8652 | 26 | 3 (People & Lifestyle, Popular Culture, Communication & World) | 0/26 | 0/26 |
| **Subtotal** | | **448** | **53** | **36/448** | **300/448** |

## Subjects — Free Tier (school_id NULL, generic content)

| Subject | Exam Board | Lessons | Units | Cinematic Videos | Podcasts |
|---------|-----------|---------|-------|-----------------|----------|
| Maths | Edexcel 1MA1 | 37 | TBC | 0/37 | 0/37 |
| Science (generic) | AQA 8464 | 48 | 6 | 24/48 | 47/48 |
| Separate Sciences (generic) | AQA 8461/8462/8463 | 22 | 3 | 0/22 | 22/22 |
| English Language (generic) | AQA 8700 | 30 | 4 | 0/30 | 30/30 |
| English Literature (generic) | AQA 8702 | 70 | TBC | 0/70 | 0/70 |
| **Subtotal** | | **207** | | **24/207** | **99/207** |

**Architecture:** `school_id = NULL` rows are generic/public content visible to free users. `school_id` set = school-specific bespoke content. Both tiers share the same templates and loaders.

Every subject has: content, practice questions (6/lesson), knowledge checks (5/lesson), TTS narration (Azure Speech, ~11,700 MP3s on R2), Gemini diagrams (automated QA via Claude Sonnet), hero images, exam technique guides, revision technique guides, related media.

## Dynamic Architecture (LIVE on Vercel)

All content served from Supabase. Static HTML files remain as backup.

- **577 lessons** (370 school + 207 generic) + **226 guide pages** (194 school + 32 generic) in Supabase. Images on R2 (`studyvault-images`), audio on R2 (`studyvault-audio`), cinematic videos on R2 (`studyvault-video`).
- **Templates:** `lesson.html`, `browse.html`, `guide.html` with JS loaders
- **URL scheme:** `/lesson/{subject}/{unit}/{number}`, `/browse/{subject}/{unit?}`, `/guide/{subject}/{type}/{slug?}`
- **Auth (3 tiers):**
  - **Free users:** No login. Generic content (school_id NULL) + ads. Prefs stored in localStorage via `js/free-user.js`.
  - **School students:** Enter school code (stored in `schools.settings.student_code`). Validated via `api/auth/login.js`, stored in sessionStorage. Sees only subscribed subjects (restricted mode via `school_subscriptions` table), no ads.
  - **Teachers/Admin:** `ADMIN_PASSWORD` / `TEACHER_PASSWORD` via `js/auth-gate.js`. Teacher setup flow in `js/teacher-setup.js`.
  - **Microsoft SSO:** Still pending Entra admin consent.
- **Admin pages:** `/admin/pipeline` (upload/generate), `/admin/review` (QC), `/admin/images` (image QA), `/admin/editor` (lesson editor), `/admin/editor-guide` (guide editor)
- **Supabase tables:** schools, profiles, subjects, units, lessons, guide_pages, school_subscriptions, user_selected_subjects, lesson_visits, knowledge_check_scores, content_pipeline_logs, upload_jobs, pipeline_steps, classes, class_members
- **R2 buckets:** `studyvault-audio` (`pub-f7b76d81365b4b2f954567763694a24e.r2.dev`), `studyvault-images` (`pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev`), `studyvault-video` (`pub-157a3979382e4f98b51f7f868078e5a3.r2.dev`)
- **Cookie consent:** Banner on all pages via `js/cookie-consent.js`. Privacy policy at `/privacy.html`.
- **Business email:** studyvault.info@gmail.com

## Active TODO
- **Severn Vale demo LIVE** — school code `vale2026`, subscribes to Science + Separate Sciences. Generic content (school_id NULL).
- **Editor school scoping (BLOCKER):** Lesson/guide editors have NO school_id scoping — dangerous with duplicate subject slugs across schools. Must fix before teacher onboarding.
- **Dashboard progress**: Hardcoded demo data — need real Supabase queries
- **Microsoft SSO activation**: network manager grants Entra admin consent → test on Vercel
- **Cinematic videos**: 60/577 done (Sport Science 9 + Food Tech 7 + Generic Science 24 + History 20 YouTube). Daily limit 20/day. See `docs/VIDEO_PIPELINE.md`.
- **Podcasts (Unity)**: 300/370 done. Science 0/48 + Sep Sci 0/22 remaining (deliberately paused — must NOT copy from generic). See `docs/VIDEO_PIPELINE.md`.
- **Podcasts (Generic)**: 99/207 done. Science 47/48, Sep Sci 22/22, Eng Lang 30/30. Eng Lit 0/70 + Maths 0/37 remaining.
- **Collapsible UX**: Tinted background + "Tap to expand" hint (dismissed after first click via localStorage). Lightbulb no longer overlaps chevron.
- **Card design refresh**: Explored editorial overlay + stacked deck designs. Reverted — readability issues with varied hero images. Noted in FUTURE_FEATURES.md for later iteration.
- **Notification sound**: Beep plays after every Claude response via `Stop` hook in `~/.claude/settings.json`.
- **Remotion promo video**: Prototype at `studyvault-promo/`. Slot machine opener, 8 scenes, school-targeted pitch. Needs music + iteration.
- **Niche exam board targeting**: Initial school list at `scripts/niche-board-schools.csv`. See `memory/exam-board-market-share.md` + FUTURE_FEATURES.md.
- **Parents' evening print view**: Dashboard section with quick-print option per class — key stats and data summary for parents' evening conversations
- **Mobile app (Capacitor)**: Wrap existing PWA with Capacitor for App Store + Google Play listing. Adds push notifications. Requires Apple Developer account (£79/yr) + Google Play ($25 one-off). Tom handles account signup + store submissions; Claude does code/config.
- Role detection (teacher vs student), remove demo accounts once SSO works, retire static HTML

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
| Teacher auth | `TEACHER_PASSWORD` | Gates `/admin/editor`, `/admin/editor-guide` |

## Key Conventions

- **Design:** Background `#faf8f5`, text `#2d2a26`, Inter + Source Serif 4, `border-radius: 16px`, soft shadows
- **Images:** Heroes max 1200px, diagrams max 1000px, JPEG quality 82
- **Content:** 6 practice questions + 5 knowledge checks per lesson. Readability for GCSE age 15-16.
- **Narration:** Azure Speech, Ollie (odd lessons) / Bella (even), MP3 96kbps 24kHz mono
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
