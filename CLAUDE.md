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
- **`lesson-widgets`** — the interactive widget fleet (see below). MERGED into platform 30 Aug 2026 (e2931afe) and live; the branch is history now.
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
typed flashcards (a deck of ≤14 judged by Jev — live 19 Sep 2026; `api/flashcards/judge.js`, curation `scripts/flashcards/curate_recall_cards.py`), TTS narration (Azure, MP3s on R2), hero images
(photographs — vision-gated pipeline), exam/revision technique guides,
curated related media (URL-audited — see YouTube audit below).

**Format exceptions — practice-first** (`practice.html` + `practice-loader.js`,
no narration/podcasts/flashcards/KCs): Maths ×4 boards, English Language ×4,
Spanish/French/German (AQA + Edexcel), Science/Separate-Science calculation
units, Geography Skills. Mixed-format subjects list practice units in
`subjects.settings.practice_units`.

**Third format — listening (6 Sep 2026):** Music set-work lessons are article
rows whose `content_html` carries the `sv-listening` stage. The page docks a
card carousel over a listening player and hides the sidebar, audio player,
practice section and reader tour, so they need NO podcast, explainer video
or narration. The marker is the classification, exposed as the stored
generated column `lessons.is_listening` (indexed; migration 20260906130000).
`batch_podcasts.py`, `batch_explainer_videos.py` and `/admin/build-status`
skip or separately count them. Any new consumer of "article lessons" must
exclude `is_listening`.
Deck standard (7 Sep 2026): all 24 listening lessons follow the approved
guided-listening deck — docked player with verified numbered pins, a cover card,
one ~75-word statement card per pin, an exam checklist (builders + timing audit
in `scripts/_content_music_listening_rebuild/`). Single-work lessons cap at 9
cards; the four multi-work music-aqa study pieces run to pins+2 cards and reuse
their existing dock verbatim (R2 wave dock for Beethoven, multi-track YouTube
for the rest).

**Tier gaps (accurate 29 Aug 2026):**
- **Diagrams**: Unity-only (Gemini diagrams stripped from free tier Apr 2026;
  GPT-image-2 replacement parked).
- **Cinematic explainer videos**: Unity complete (552). Free tier now has
  substantial video coverage too — census 29 Aug: 3,999 lessons carry an R2
  video, 357 a YouTube embed, 0 Google Drive. (Do not claim "free tier has
  no videos"; it is no longer true. All self-hosted video is R2.)
- **Podcasts**: Unity complete; free-tier backlog cleared Aug 2026; new units
  generate automatically the morning after their last lesson flips live.

## Interactive widgets (LIVE since 30 Aug 2026)

91 bespoke misconception-driven interactives wired into 279 lessons
(280 strips; one lesson carries two), built Aug 2026, all field-reviewed by
Tom. Commit-before-feedback, phone-first, mastery exit (3-in-a-row), embed
strip → modal. Merged 30 Aug (e2931afe), builds deployed under `/widgets/`
(c6a5fa39); verified live 11 Sep: `.sv-embed-strip` renders and the modal
mounts the widget.

- Wiring: `js/widget-embed.js` (MAP of lesson-key → widget file, anchor,
  optional per-lesson `variant`). Builds in `scripts/widget_pipeline/builds/`.
- Pipeline + design rules: `scripts/widget_pipeline/BUILD_GUIDE.md` (the
  design authority), `CONTRACT.md`, `STYLE_DIGEST.md`, harness at
  `scripts/widget_pipeline/harness/check.mjs`.
- Completion credit: widget mastery earns a 10-weight "interactive" activity
  (commit 23635106; in-denominator vs bonus-credit decision open with Tom).
- Remaining queue: 3-lesson band (48 clusters).

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
    The code path is CLOSED (1 Sep 2026): `api/auth/login.js` answers 410
    to any code and the three "Enter school code" buttons on `index.html`
    are hidden. `schools.settings.student_code` is dead data. Microsoft SSO
    awaits Entra admin consent; that consent gates student identity and
    therefore everything teacher-facing per-pupil.
  - **Teachers:** individual Supabase Auth accounts, invited by admin,
    scoped via `teacher_subjects`. Two kinds of row: subjects on the
    invitation carry can_edit/can_publish (review + editor links appear);
    subjects a teacher ticks on sign-up are a teaching declaration only
    (both false). One consolidated screen at
    `/teacher/classes`. Boundary rules: teachers SEE attainment +
    misconceptions; behaviour aggregate-only; never study habits; NO
    work-setting/assignments/due dates (vision boundary).
  - **Admin:** Tom's own Supabase account + a Microsoft Authenticator code (session aal2), from the admin-mfa branch (29 Sep 2026). `ADMIN_PASSWORD` is retired (`/api/auth/login` answers 410). Server check `api/_lib/admin-auth.js`; sign-in and code step at `/teacher/login` (`js/staff-mfa.js`); `/admin/security`; lock-out recovery `scripts/admin_mfa_reset.py`. A platform_admin without the code step counts as a teacher.
- **AI routes:** all 5 run on Bedrock **eu-west-2 (London) through the `eu.` cross-region profile, so a request may be served from any AWS EU region** — public wording is "UK and EU", never "London only" (Tom, 29 Sep 2026) — verify with
  `servedBy` on `/api/ai-mark`. Marking is marks-routed (Haiku ≤8, Sonnet >8;
  essays 2000 tokens). ⚠ open: US fallback must fail closed before any DPA
  claim.
- **School content is private (24 Sep 2026):** RLS lets visitors read live free-tier
  content only; a school's subjects/units/lessons/guides are readable only by its users
  (profile school OR class membership, `user_school_ids()`), its teachers, and admins.
  Unpublished lessons are staff-only. The password-gated admin pages read content through
  `/api/staff/rest`; `js/content-reads.js` (loaded before supabase-js) routes admin reads there
  and signs plain content fetches for signed-in users. Never offer `?sid=` links to pupils.
  Tests: `scripts/security/` (dry run, browser, live). Rollback in `supabase/migrations/`.
- **Answer pool (26 Sep 2026):** anonymous counts of the answers pupils give, to find faulty
  questions and improve feedback. Table `answer_pool` (service key only, RLS on, no policies):
  question key + tidied answer or chosen option (≤60 chars) + verdict + count + ISO week first
  seen; for AI-marked writing the MARK only. No identity, school, IP or time. Client
  `js/answer-pool.js` (practice, lesson, dashboard pages; key formats in its header), server
  `api/pool.js` (drops personal-looking answers). Off for staff, demo pupils, Demo High School
  and the test schools, and for safeguarding-flagged answers. Widgets are not counted. Stated in
  privacy.html. The old prototype table `events` and `/teach` were retired the same day.
- **Safeguarding route (23 Sep 2026):** exam answers, tutor messages, flashcard
  answers and searches get a London-hosted check beside the marking; a flag shows
  the pupil a support panel and, for a signed-in pupil in a class at a school with
  `schools.settings.safeguarding` set, stores the concern and emails the lead (no
  names or words in the email). Lead reviews at `/teacher/safeguarding`. Unity's
  lead: Bev Worthington. Details: `docs/SAFEGUARDING_ROUTE.md`.
- **Admin pages:** `/admin/pipeline`, `/admin/review`, `/admin/images`,
  `/admin/editor`, `/admin/editor-guide` (Tom-only, never redesigned — leave).
- **Teacher pages:** `/teacher/login`, `/teacher/signup`, `/teacher/classes`
  (customer-facing; redesign before Sept). `/teacher/dashboard` is a rewrite
  onto `/teacher/classes` — the demo prototype it used to serve was deleted
  29 Aug. Every figure on the class screen comes from
  `/api/teacher/class-progress`; nothing on it is seeded or illustrative.
- **Supabase tables:** schools, profiles, subjects, units, lessons,
  guide_pages, school_subscriptions, user_selected_subjects, lesson_visits,
  knowledge_check_scores, user_state, content_pipeline_logs, upload_jobs,
  pipeline_steps, classes, class_members, teacher_invitations,
  teacher_subjects, notifications
- **R2 buckets:** `studyvault-audio` (audio.studyvault-media.co.uk),
  `studyvault-images` (images.studyvault-media.co.uk),
  `studyvault-video` (video.studyvault-media.co.uk)
- **Cookie consent:** `js/cookie-consent.js`; privacy at `/privacy.html`.
- **Business email:** studyvault.info@gmail.com

## Automation (scheduled tasks, all hourly-heartbeat wrappers with cooldowns)

| Task | Wrapper | What it does |
|---|---|---|
| StudyVault - Daily Podcast Build | `scripts/daily_podcast_build.ps1` | NLM podcasts for units whose last lesson flipped live; unit-complete gated; logs `scripts/_podcast_daily_logs/` |
| StudyVault - Daily Explainer Build | `scripts/daily_explainer_build.ps1` | NLM explainer videos; logs `scripts/_explainer_daily_logs/` |
| StudyVaultShorts | sandbox worktree `scripts/daily_shorts_build.ps1` | shorts feed, cap 100/day; yields ≤35 video slots to explainer demand |
| StudyVault - Weekly YouTube Audit | `scripts/weekly_yt_audit.ps1` (Sun 04:00) | full link audit; **auto-prunes** a related-media link dead on two consecutive Sundays with a hard reason (private/removed; watch-page playabilityStatus), backup in `scripts/_yt_audit_prunes/`, never below 8 items, video slot + in-body embeds only flagged; Resend email says what was pruned and what is Held; accepted-list + placeholder denylist + wrong-channel check (`scripts/_yt_audit_accepted.json`); history in `_yt_audit_dead_history.json` (Tom, 7 Sep 2026) |
| StudyVaultBackup | (Sun 03:00) | OneDrive backup; R2→B2 mirror (30-day lock) |

⚠ **2 Sep 2026: Gemini Notebook (ex-NotebookLM) switches to compute-based
limits, 5-hour refresh, deferred generations.** Every calibrated quota
(60/day podcasts, ~200/day audio, 20/day video pool, shorts contention) is
void that day — but as of 3 Sep the change has NOT reached us (Google:
~10% rollout; no usage bar in Tom's UI). Trigger for re-calibration = the
usage bar appearing, or a mid-batch cap in the logs; then re-size from the
batch logs.

## Active TODO (checked against git + memory 25 Sep 2026 — split by who can move it)

### Tom's tasks (decisions, reviews, external actions)
- **Microsoft SSO**: chase Entra admin consent — the blocker for all
  per-pupil data.
- **Vercel env check**: confirm `ALLOW_US_FALLBACK` is NOT set (the AI
  routes fail closed as of 4307ac6d — that env var is the only override).
- **Per-school term dates** for planner holiday awareness (needs school
  calendars only Tom can obtain).
- **Geography Skills L13/L14**: review pass with Claude (built 21 Jul; L11/12 done).
- *(long-term)* **GPT-image-2 diagrams** (~£400–700) — revisit when school
  revenue lands (Tom, 30 Aug). **Mobile app (Capacitor)** — after launch
  settles (Tom, 30 Aug).

### Claude's tasks (delegable — runnable any time)
- **Retro fact-check follow-ups** (checking phase COMPLETE 6 Sep): question-type
  relabel partly applied (ec56802d; review lists from 15874811); science Key
  Takeaways de-dup (8 lessons); Eduqas self-naming sweep (47 lessons,
  `scripts/_englit_debt_worklist.md`); PD extract authoring (scope unclear);
  platform duration re-measure (nice-to-have).
- **3-lesson widget band** (48 clusters) — APPROVED and now unblocked (its
  retro fact-check gate was met 6 Sep).
- **NLM shared budget**: sandbox shorts job runs on the shared allowance
  (`scripts/lib/nlm_pool.py`, 24 Sep); the explainer wrapper on platform still
  uses its own `--daily-cap 100` — bring it onto the same ledger.
- **English Literature debt**: 3 duplicate-content clusters left (flashcards
  regenerated and placeholders closed 30 Aug).
- **Prescribed-works register**: Media AQA CSPs — blocked on the 2027 booklet
  (AQA teacher-login portal). Music AQA is filled (f2b2d505).

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
| Admin auth | ~~`ADMIN_PASSWORD`~~ | RETIRED with the admin-mfa branch (29 Sep 2026): admin is Tom's account + a TOTP code; delete the Vercel var once that is live |
| Teacher auth | ~~`TEACHER_PASSWORD`~~ | RETIRED 6 Sep 2026 — teachers use their own accounts; delete the Vercel var |
| Resend | `RESEND_API_KEY` + `NOTIFY_TO`, `NOTIFY_FROM` | bug reports, subject requests, audit alerts |
| AWS | (Vercel env) | Bedrock eu-west-2 for AI routes |

## Key Conventions

- **Design:** background `#faf8f5`, text `#2d2a26`, Inter + Source Serif 4,
  `border-radius: 16px`, soft shadows. No coloured left-border stripes.
- **Images:** heroes max 1200px (photographs, vision-gated), diagrams max
  1000px, JPEG q82.
- **Content:** 6 practice + 5 KCs + a flashcard deck of ≤14 (12–15 curated cards plus typed-recall cards, judged down to 14) per lesson; GCSE age 15–16
  readability. `*_html` fields use entities; plain-text fields use unicode
  (validator enforces). Fact-check BEFORE narration.
- **Narration:** MAI voices since 2 Oct 2026 — Harry (odd) / Emily (even), `en-GB-…:MAI-Voice-2.1-Flash` via the Foundry resource (FOUNDRY_ENDPOINT/KEY); language lessons keep Ollie/Ada multilingual; older audio stays Ollie/Ada until re-narrated (Unity in one batch before its launch). MP3 96kbps 24kHz
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
| `data/exam-dates-2027.json` | exam dates (2027 edition; refresh each year) |
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
widget strips post-render.

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
