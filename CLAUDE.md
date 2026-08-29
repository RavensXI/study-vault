# StudyVault — Project Reference

Multi-subject GCSE revision site. Repo: https://github.com/RavensXI/study-vault

### Deployments
- **GitHub Pages** (`main`): https://ravensxi.github.io/study-vault/ — History only, no login
- **Vercel** (`platform`): https://www.studyvault.co.uk/ (custom domain, also study-vault-alpha.vercel.app) — full platform, public content, admin/teacher login

### Owner
Tom Shaun — `t.shaun@unity.lancs.sch.uk` / git: `tomshaun90@gmail.com`

---

## Branches
- **`main`** — History at root level. Single-subject, no login.
- **`platform`** (current) — multi-subject. History under `history/`. Public content, school login, password-gated admin/teacher areas.
- **`lesson-widgets`** — the interactive widget fleet (see below). Local only, merge-ready (clean test-merge vs platform, QA evidence 29 Aug), awaiting Tom's merge decision.
- **`sandbox` / `landing-wizard`** — summer redesign work. Never merge to platform/main until launch.

## Counts snapshot — 29 Aug 2026

> **Rule: every count in this file carries a date.** Counts go stale the day
> after they are written. Regenerate with `python scripts/audit_subject_status.py`
> (add `--subjects` for per-subject live lesson counts) and re-stamp this
> section rather than trusting or hand-editing the numbers.

| | Subjects | Lessons (live) | Lessons (all) |
|---|---|---|---|
| Free tier (school_id NULL) | 93 live | 4,318 | 4,412 |
| Unity College | 18 | 554 | 554 |
| Severn Vale School | 1 (`science-severnvale`) | 32 | 48 |
| **Total** | | **4,904** | **5,014** |

Also in the census (29 Aug): 92 lessons `pending_review` — mostly the three
new Music boards (Eduqas / OCR / Edexcel) awaiting Tom's review flips; 16
`ready_for_teacher`; 693 units.

**Unity's 18 subjects** (bespoke, school code `unitypassionrespect`):
business, computer-science, creative-imedia, design-technology, drama,
english-language, english-literature, food-preparation-and-nutrition, french,
gcse-music, geography, german, history, religious-studies, science,
separate-sciences, spanish, sport-science. (Maths and Music Technology no
longer appear as live Unity subject rows — Music Tech was last taught
2025-26.)

**Free tier** covers every major GCSE subject across AQA / Edexcel / OCR /
Eduqas where the spec allows (100%-coursework specs excluded), plus niche
single-board subjects (Astronomy, Geology, Electronics, Film Studies,
Psychology ×3 boards, Economics, Sociology, Statistics, Classical
Civilisation, L1/2 vocational ports, and more). Per-board lesson counts:
run the census with `--subjects` — do not maintain a table here.

**Architecture:** `school_id = NULL` rows are generic/public content for free
users. `school_id` set = school-specific bespoke content. Both tiers share
the same templates and loaders. **Never mix generic and school content; Unity
content never ports to free tier (same spec = fresh build).**

## What every subject has

Content, practice questions (6/lesson), knowledge checks (5/lesson),
flashcards (5/lesson), TTS narration (Azure, MP3s on R2), hero images
(photographs — vision-gated pipeline), exam/revision technique guides,
curated related media (URL-audited — see YouTube audit below).

**Format exceptions — practice-first** (`practice.html` + `practice-loader.js`,
no narration/podcasts/flashcards/KCs): Maths ×4 boards, English Language ×4,
Spanish/French/German (AQA + Edexcel), Science/Separate-Science calculation
units, Geography Skills. Mixed-format subjects list practice units in
`subjects.settings.practice_units`.

**Tier gaps (accurate 29 Aug 2026):**
- **Diagrams**: Unity-only (Gemini diagrams stripped from free tier Apr 2026;
  GPT-image-2 replacement parked).
- **Cinematic explainer videos**: Unity complete (552). Free tier now has
  substantial video coverage too — census 29 Aug: 3,999 lessons carry an R2
  video, 357 a YouTube embed, 0 Google Drive. (Do not claim "free tier has
  no videos"; it is no longer true. All self-hosted video is R2.)
- **Podcasts**: Unity complete; free-tier backlog cleared Aug 2026; new units
  generate automatically the morning after their last lesson flips live.

## Interactive widgets (branch `lesson-widgets`, unmerged)

91 bespoke misconception-driven interactives wired into 279 lessons
(280 strips; one lesson carries two), built Aug 2026, all field-reviewed by
Tom. Commit-before-feedback, phone-first, mastery exit (3-in-a-row), embed
strip → modal. Verified 29 Aug: clean test-merge vs platform, 91/91 harness
passes, 279/279 lessons render.

- Wiring: `js/widget-embed.js` (MAP of lesson-key → widget file, anchor,
  optional per-lesson `variant`). Builds in `scripts/widget_pipeline/builds/`.
- Pipeline + design rules: `scripts/widget_pipeline/BUILD_GUIDE.md` (the
  design authority), `CONTRACT.md`, `STYLE_DIGEST.md`, harness at
  `scripts/widget_pipeline/harness/check.mjs`.
- Completion credit: widget mastery earns a 10-weight "interactive" activity
  (commit 23635106; in-denominator vs bonus-credit decision open with Tom).
- Remaining queues: 3-lesson band (48 clusters), merge decision.

## Specification Database

193 GCSE specs from all 4 boards as markdown + YAML frontmatter, the
authoritative source for content generation.

- **Location:** `specs/{board}/{slug}-{code}.md` — indexed by `specs/index.json`
- **Script:** `python scripts/download_specs.py`
- **Two build modes:** Bespoke (teacher uploads) or Generic (spec-only).
  See `docs/PIPELINE.md` (master playbook) and `docs/PLANNING_PROMPT.md`.
- Annual spec-currency audit before each new cohort (skill:
  `spec-currency-audit-2027`).

## Dynamic Architecture (LIVE on Vercel)

All content served from Supabase. Static HTML remains as backup. Images on
R2 (`studyvault-images`), audio on R2 (`studyvault-audio`), video on R2
(`studyvault-video`).

- **Templates:** `lesson.html`, `browse.html`, `guide.html`, `practice.html` + JS loaders
- **URL scheme:** `/lesson/{subject}/{unit}/{number}`, `/practice/...`,
  `/browse/{subject}/{unit?}`, `/guide/{subject}/{type}/{slug?}`, `/exams`
- **Auth (4 tiers):**
  - **Free users:** no login required; email+password accounts exist for sync
    (`user_state` table, merge-on-sign-in — js/account-sync.js). **NO ADS on
    the free tier** — settled decision. ⚠ STANDING RULE: no student state may
    be device-only; every new localStorage key joins the account-sync
    whitelist.
  - **School students:** ⚠ **SCHOOL CODES ARE RETIRED — not the model.**
    School sign-in is **SSO (Microsoft / Google)**, school email fallback.
    The code path (`schools.settings.student_code`, `api/auth/login.js`)
    still functions but is legacy — do not build against it. Microsoft SSO
    awaits Entra admin consent; that consent gates student identity and
    therefore everything teacher-facing per-pupil.
  - **Teachers:** individual Supabase Auth accounts, invited by admin,
    scoped via `teacher_subjects`. One consolidated screen at
    `/teacher/classes`. Boundary rules: teachers SEE attainment +
    misconceptions; behaviour aggregate-only; never study habits; NO
    work-setting/assignments/due dates (vision boundary).
  - **Admin:** `ADMIN_PASSWORD` via `js/auth-gate.js`.
- **AI routes:** all 5 run on Bedrock **eu-west-2 (London)** — verify with
  `servedBy` on `/api/ai-mark`. Marking is marks-routed (Haiku ≤8, Sonnet >8;
  essays 2000 tokens). ⚠ open: US fallback must fail closed before any DPA
  claim.
- **Admin pages:** `/admin/pipeline`, `/admin/review`, `/admin/images`,
  `/admin/editor`, `/admin/editor-guide` (Tom-only, never redesigned — leave).
- **Teacher pages:** `/teacher/login`, `/teacher/signup`, `/teacher/classes`
  (customer-facing; redesign before Sept).
- **Supabase tables:** schools, profiles, subjects, units, lessons,
  guide_pages, school_subscriptions, user_selected_subjects, lesson_visits,
  knowledge_check_scores, user_state, content_pipeline_logs, upload_jobs,
  pipeline_steps, classes, class_members, teacher_invitations,
  teacher_subjects, notifications
- **R2 buckets:** `studyvault-audio` (pub-f7b76d81365b4b2f954567763694a24e.r2.dev),
  `studyvault-images` (pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev),
  `studyvault-video` (pub-157a3979382e4f98b51f7f868078e5a3.r2.dev)
- **Cookie consent:** `js/cookie-consent.js`; privacy at `/privacy.html`.
- **Business email:** studyvault.info@gmail.com

## Automation (scheduled tasks, all hourly-heartbeat wrappers with cooldowns)

| Task | Wrapper | What it does |
|---|---|---|
| StudyVault - Daily Podcast Build | `scripts/daily_podcast_build.ps1` | NLM podcasts for units whose last lesson flipped live; unit-complete gated; logs `scripts/_podcast_daily_logs/` |
| StudyVault - Daily Explainer Build | `scripts/daily_explainer_build.ps1` | NLM explainer videos; logs `scripts/_explainer_daily_logs/` |
| StudyVaultShorts | sandbox worktree `scripts/daily_shorts_build.ps1` | shorts feed, cap 100/day; yields ≤35 video slots to explainer demand |
| StudyVault - Weekly YouTube Audit | `scripts/weekly_yt_audit.ps1` (Sun 04:00) | full link audit; Resend email on dead links; accepted-list + placeholder denylist + wrong-channel check (`scripts/_yt_audit_accepted.json`) |
| StudyVaultBackup | (Sun 03:00) | OneDrive backup; R2→B2 mirror (30-day lock) |

⚠ **2 Sep 2026: Gemini Notebook (ex-NotebookLM) switches to compute-based
limits, 5-hour refresh, deferred generations.** Every calibrated quota
(60/day podcasts, ~200/day audio, 20/day video pool, shorts contention) is
void that day — treat 2–3 Sep as a re-calibration day from the batch logs.

## Active TODO (pruned 29 Aug 2026 — split by who can move it)

### Tom's tasks (decisions, reviews, external actions)
- **Review flips**: 92 `pending_review` lessons — the three Music boards
  (Eduqas 32 / OCR 37 / Edexcel 31, built 16 Aug) + music listening feature.
- **Widget fleet decisions**: merge `lesson-widgets`? completion-credit
  in-denominator vs bonus? go/no-go on the 3-lesson band (48 clusters)?
- **Teacher pages redesign direction** (3 customer-facing pages, before
  Sept) — pick the direction; Claude builds it.
- **Microsoft SSO**: chase Entra admin consent — the blocker for all
  per-pupil data.
- **Vercel env check**: confirm `ALLOW_US_FALLBACK` is NOT set (the AI
  routes fail closed as of 4307ac6d, deployed 29 Aug — that env var is the
  only override).
- **Per-school term dates** for planner holiday awareness (needs school
  calendars only Tom can obtain).
- **GPT-image-2 diagrams**: budget call (~£0.12/image, ~£400–700 full
  build-out) — parked until decided.
- **Geography Skills L13/L14**: review pass with Claude (L11/12 done).

### Claude's tasks (delegable — runnable any time)
- **NLM re-calibration** on 2–3 Sep after the compute-limit change (plan
  saved in memory; read real throughput from batch logs, re-size caps).
- **English Literature debt**: audit + worklist for AQA regex-generated
  flashcards and placeholder `content_html`; then fixes on approval.
- **Parents' evening print view**; **dashboard progress widgets** (replace
  demo data with real Supabase queries).
- **Exam dates 2027 edition** of `data/exam-dates-2026.json` once boards
  publish timetables.
- **Mobile app (Capacitor)** — execution ready when Tom green-lights.
- **Prescribed-works register**: fill Music AQA + Media AQA once the 2027
  CSP list is published (blocked on external publication, then Claude's).

### Recently shipped (Aug 2026)
- Widget fleet built + field-reviewed (equity band: every qualifying subject
  family; depth band stages 14–18); fleet-wide strip-anchor fix ($end mode).
- Account sync (19 Aug): all student state account-linked; `user_state`.
- Podcasts/explainers/shorts fully automated with health probes.
- Misconception tagging live: 2,384 AI-marking prompts + per-distractor MC
  enrichment feed the teacher misconception table.
- YouTube link hygiene (28–29 Aug): 38 wrong videos + 64 wrong credits fixed
  (218 items; the generic pipeline had invented ids — incl. a 22× rickroll
  placeholder); audit hardened (accepted-list, denylist, channel check).
- Fact-check content fixes on live rows (e.g. geology rule-of-Vs inversion,
  28 Aug — re-narrated).
- Parents' evening packs, teacher area consolidation, AI marking in London,
  essay-tier routing fix, cohort gate, D&T Edexcel, EngLit Eduqas anthology
  (all earlier Aug — details in memory).

## API Keys

All in environment variables — never commit.

| Service | Env Var | Notes |
|---------|---------|-------|
| Gemini | `GEMINI_API_KEY` | image generation (`gemini-3.1-flash-image-preview`) |
| Supabase | `SUPABASE_URL`, `SUPABASE_ANON_KEY` | public, hardcoded in `index.html` |
| Supabase | `SUPABASE_SERVICE_KEY` | server-side only |
| Supabase (DDL) | `SUPABASE_DB_URL` | psycopg2 → aws-1-eu-west-2 pooler |
| Azure Speech | `AZURE_SPEECH_KEY` | region `uksouth`, pay-as-you-go |
| R2 | `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_ACCOUNT_ID` | Cloudflare |
| Unsplash | `UNSPLASH_ACCESS_KEY` | hero search |
| ElevenLabs | `ELEVENLABS_API_KEY` | unused fallback |
| Admin auth | `ADMIN_PASSWORD` | gates /admin/* |
| Teacher auth | `TEACHER_PASSWORD` | legacy shared fallback |
| Resend | `RESEND_API_KEY` + `NOTIFY_TO`, `NOTIFY_FROM` | bug reports, subject requests, audit alerts |
| AWS | (Vercel env) | Bedrock eu-west-2 for AI routes |

## Key Conventions

- **Design:** background `#faf8f5`, text `#2d2a26`, Inter + Source Serif 4,
  `border-radius: 16px`, soft shadows. No coloured left-border stripes.
- **Images:** heroes max 1200px (photographs, vision-gated), diagrams max
  1000px, JPEG q82.
- **Content:** 6 practice + 5 KCs + 5 flashcards per lesson; GCSE age 15–16
  readability. `*_html` fields use entities; plain-text fields use unicode
  (validator enforces). Fact-check BEFORE narration.
- **Narration:** Azure, Ollie (odd) / Ada (even lessons), MP3 96kbps 24kHz
  mono; languages use multilingual voices + SSML `<lang>` (foreign text in
  `<em>`/`<strong>`). See `docs/NARRATION_PIPELINE.md`.
- **PPTs:** `python -m markitdown "file.pptx"`.
- **Equations:** KaTeX auto-render — inline `\(...\)`, display `$$...$$`.
- **Animations:** soft-close damping `cubic-bezier(0.16, 1, 0.3, 1)`,
  `.sv-reveal`/`.sv-stagger`, `prefers-reduced-motion` respected; browse unit
  cards never scroll-revealed.
- **Lesson completion:** WEIGHTED model — spec at
  `design-lab/LESSON_COMPLETION_SPEC.md`, implemented in `js/main.js`
  `weighted()`. Never invent an ad-hoc completion rule.

## Reference Docs (read on demand)

**Start here for any new subject build:** `docs/PIPELINE.md`.

| Doc | When |
|-----|------|
| `docs/PIPELINE.md` | entry point for builds |
| `docs/PLANNING_PROMPT.md` | phase 1 planning agent |
| `docs/CONTENT_PROMPT.md` | article content agent |
| `docs/PRACTICE_PIPELINE.md` | practice-format factory |
| `docs/REFERENCE_LESSONS.md` | pinned structural examples |
| `docs/REVISION_TECHNIQUES/` | 7 canonical templates |
| `docs/LESSON_TEMPLATE.md` | article HTML components |
| `docs/QUESTIONS_PIPELINE.md` | question formats, marks |
| `docs/DIAGRAM_PIPELINE.md` | Unity-only diagrams |
| `docs/NARRATION_PIPELINE.md` | TTS |
| `docs/VIDEO_PIPELINE.md` | videos + podcasts |
| `docs/RELATED_MEDIA_PIPELINE.md` | media curation (URLs MUST be audited) |
| `docs/UNIT_THEMES.md` | unit accents |
| `docs/PRACTICE_BUILD_MASTER_PLAN.md` | practice corpus plan + QA gates |
| `docs/TIER_DIFFERENTIATION_PLAN.md` | Foundation/Higher runbook |
| `docs/FUTURE_FEATURES.md`, `docs/SUBJECT_ROADMAP.md`, `docs/FILE_STRUCTURE.md` | planning |
| `docs/archive/` | superseded — never generate from these |
| `scripts/widget_pipeline/BUILD_GUIDE.md` | widget design authority |
| `scripts/science-practice/SCIENCE_PRACTICE_SCHEMA.md` | science practice data |
| `scripts/language-practice/PRACTICE_DATA_SCHEMA.md` | language practice data |
| `scripts/factory/FACTORY_RULES.md` | EngLang factory |
| `data/exam-dates-2026.json` | exam dates (needs annual refresh) |
| `{subject}/BUILD_PLAN.md` | per-subject breakdown |

Commercial/privacy docs live OUTSIDE this repo in
`Documents\StudyVault Business\` (`docs/` deploys verbatim to Vercel).

## JS Architecture (main.js)

**Phase 1** (DOMContentLoaded): scroll progress, mobile nav, a11y toolbar,
page transitions, `initRevealAnimations()`.
**Phase 2** (`window.initLessonFeatures()`, after content injection):
collapsibles, visited tracking, practice questions, narration, glossary,
knowledge check, lightbox, revision tips, nav icons, lesson pill, weighted
completion.

**Dynamic loaders:** `lesson-loader.js`, `browse-loader.js`,
`guide-loader.js` — auth check → Supabase fetch → populate → init.
Lesson content injects into `#study-notes`. `js/widget-embed.js` places
widget strips post-render (on `lesson-widgets` branch).

## Sidebar Structure

Three sections: **Knowledge Check** (button → modal), **Related Media**
(collapsible categories), **Video**. Do NOT add a "Key Facts" section.

## Video Embeds

- **YouTube:** video ID in `lessons.youtube_video_id` → inline iframe.
- **Google Drive:** full `/preview` URL in the same field → thumbnail +
  modal (`sidebar-video--gdrive`). Files must be "Anyone with the link".
- **R2:** URL containing `r2.dev/` or ending `.mp4` → native `<video>` modal.
- Related-media YouTube links render as `<a target="_blank">` (not iframes),
  so embed-disabled (403) videos still work there.

## Schools

- **Unity College** — code `unitypassionrespect` (legacy), 18 bespoke
  subjects (snapshot above).
- **Severn Vale School** — code `vale2026` (legacy), `science-severnvale`.
  Teacher: Alex Cameron (individual Supabase Auth).
