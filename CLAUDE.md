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
- **`platform`** (current) — multi-subject. History under `history/`. Public content, password-gated admin/teacher areas, 9 subjects.

## Subjects (all complete, all on Vercel)

| Subject | Exam Board | Lessons | Units | Videos |
|---------|-----------|---------|-------|--------|
| History | AQA | 60 | 4 (Conflict, Health, Elizabethan, America) | 60/60 |
| Business Studies | Edexcel 1BS0 | 30 | 2 themes | 0/30 |
| Geography | AQA 8035 | 40 | 2 papers | 0/40 |
| Sport Science | OCR R180 | 10 | 1 (R180) | 1/10 |
| Drama | OCR J316 | 12 | 2 (Blood Brothers, Rise Up) | 1/12 |
| Food Technology | AQA 8585 | 10 | 1 (Nutrition & Health) | 1/10 |
| Religious Education | AQA 8062 | 40 | 8 | 1/40 |
| Music | Eduqas C660U | 26 | 6 (Elements, Forms, Ensemble, Popular, Film, Toto Africa) | 0/26 |
| English Literature | AQA 8702 | 42 | 5 (Macbeth, A Christmas Carol, Animal Farm, Power & Conflict, Unseen Poetry) | 0/42 |
| **Total** | | **270** | **31** | **64/270** |

Every subject has: content, practice questions (6/lesson), knowledge checks (5/lesson), TTS narration (Azure Speech, ~8,500 MP3s on R2), Gemini diagrams, hero images, exam technique guides, revision technique guides, related media.

## Dynamic Architecture (LIVE on Vercel)

All content served from Supabase. Static HTML files remain as backup.

- **270 lessons** + **144 guide pages** in Supabase. Images on R2 (`studyvault-images`), audio on R2 (`studyvault-audio`).
- **Templates:** `lesson.html`, `browse.html`, `guide.html` with JS loaders
- **URL scheme:** `/lesson/{subject}/{unit}/{number}`, `/browse/{subject}/{unit?}`, `/guide/{subject}/{type}/{slug?}`
- **Auth:** Public content (no login for students). Admin pages gated by `ADMIN_PASSWORD` env var, teacher pages by `TEACHER_PASSWORD` — via `js/auth-gate.js` + `api/auth/login.js`. Teacher setup flow in `js/teacher-setup.js` (name + subject + unit picker). Microsoft SSO still pending Entra admin consent.
- **Admin pages:** `/admin/pipeline` (upload/generate), `/admin/review` (QC), `/admin/images` (image QA), `/admin/editor` (lesson editor), `/admin/editor-guide` (guide editor)
- **Supabase tables:** schools, profiles, subjects, units, lessons, guide_pages, user_selected_subjects, lesson_visits, knowledge_check_scores, content_pipeline_logs, upload_jobs, pipeline_steps, classes, class_members
- **R2 buckets:** `studyvault-audio` (`pub-f7b76d81365b4b2f954567763694a24e.r2.dev`), `studyvault-images` (`pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev`)

## Active TODO
- **Dashboard progress**: Hardcoded demo data — need real Supabase queries
- **Microsoft SSO activation**: network manager grants Entra admin consent → test on Vercel
- **NotebookLM videos**: 194 lessons remaining (task list: `NOTEBOOKLM_VIDEO_TASKLIST.md`)
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
- **Animations:** Soft-close damping `cubic-bezier(0.16, 1, 0.3, 1)` on all entrance animations. `.sv-reveal` / `.sv-stagger` CSS classes + IntersectionObserver. Split timing: fast opacity (~0.5s), slow transform glide (~1-1.3s). `prefers-reduced-motion` respected. Browse page unit cards have no scroll reveal (all visible immediately so students don't miss units below the fold).

## Reference Docs (read on demand)

| Doc | When to read |
|-----|-------------|
| `docs/LESSON_TEMPLATE.md` | Building or editing lesson content |
| `docs/QUESTIONS_PIPELINE.md` | Writing questions for any subject |
| `docs/DIAGRAM_PIPELINE.md` | Creating or updating diagrams |
| `docs/NARRATION_PIPELINE.md` | TTS narration work |
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

**Dynamic loaders:** `lesson-loader.js`, `browse-loader.js`, `guide-loader.js` — auth check → Supabase fetch → populate template → init features

## Sidebar Structure

Three sections: **Knowledge Check** (button → modal), **Related Media** (collapsible categories), **Video** (YouTube embed). Do NOT add a "Key Facts" section. See `docs/RELATED_MEDIA_PIPELINE.md` for media curation.
