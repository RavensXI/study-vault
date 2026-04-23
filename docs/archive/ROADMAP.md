# StudyVault — Product Roadmap

*Last updated: 5 Apr 2026*

This is the single source of truth for what gets built and in what order. The principle: **solidify → broaden → deepen → monetise.** Each phase has a "done when" definition so we know when to move on.

---

## Phase 1 — Lock Down What Exists

**Goal:** Every Unity lesson is QA'd, polished, and confidently usable with students. This is the reference-quality showcase for selling to other schools.

**Done when:** All 598 Unity lessons are `live` status with no known issues.

### Checklist

- [ ] Full QA pass on all 20 Unity subjects (598 lessons)
  - [ ] Content accuracy spot-check (sample 2-3 lessons per subject)
  - [ ] Hero images — no broken/missing/irrelevant images
  - [ ] Diagrams — no rendering issues, labels correct
  - [ ] Narration — plays correctly, no mispronunciations that break meaning
  - [ ] Practice questions — answers are correct, mark schemes make sense
  - [ ] Knowledge checks — all 5 per lesson, answers correct
  - [ ] Flashcard questions — all 5 per lesson, sensible Q&A pairs
  - [ ] Guide pages — exam technique + revision technique per subject, no broken formatting
  - [ ] Related media — YouTube links still live, relevant to lesson
- [ ] Fix any issues found during QA
- [ ] Move all Unity lessons from `pending_review` → `live`
- [ ] Verify Severn Vale (Biology) is in good shape for Alex Cameron
- [ ] Update `docs/SUBJECT_ROADMAP.md` to reflect current state (it's out of date — CS, D&T, Music Tech all show as "to build")

### Not in scope for Phase 1
- No new features
- No new subjects
- No new schools

---

## Phase 2 — Content Coverage (Every GCSE, Every Board)

**Goal:** When any GCSE student in England searches for revision help, their subject and exam board exists on StudyVault. This is what drives organic adoption and makes the free tier compelling enough to pull teachers in.

**Done when:** Every mainstream GCSE subject across AQA, Edexcel, OCR, and Eduqas has baseline content (lessons + heroes + narration + practice Qs + knowledge checks + flashcards + guide pages).

### 2a — QA existing multi-board content

~1,266 generic lessons already generated across 4 core subjects (Eng Lang, Eng Lit, Maths, Combined Science). All currently `pending_review`.

- [ ] QA pass on English Language (4 boards, 180 lessons)
- [ ] QA pass on English Literature (4 boards, 750 lessons)
- [ ] QA pass on Mathematics (4 boards, 192 lessons) — practice format, check problem accuracy
- [ ] QA pass on Combined Science (3 boards, 144 lessons)
- [ ] Move to `live` as each board/subject passes QA

### 2b — Generate remaining subjects

Use the spec database (193 specs) + `docs/SUBJECT_PLAYBOOK.md` pipeline to generate every GCSE subject we don't already cover. Generic content (school_id NULL), spec-only mode (no teacher resources needed).

**Priority order** (by student volume and commercial value):

| Priority | Subjects | Why |
|----------|----------|-----|
| **High** | Geography (Edexcel, OCR, Eduqas), History (AQA, OCR, Eduqas), RE (Edexcel, OCR, Eduqas) | Large take-up, essay-heavy = high revision need |
| **High** | Separate Sciences (Edexcel, OCR), Business (AQA, OCR, Eduqas) | Popular options, multiple boards underserved |
| **Medium** | Languages — French, German, Spanish (Edexcel, OCR, Eduqas) | Smaller cohorts but no good free revision tools for languages |
| **Medium** | D&T, Computer Science, Drama, Music, Food Tech, Sport Science (other boards) | Fill out the long tail |
| **Lower** | Niche subjects — Sociology, Psychology, Media Studies, PE, Citizenship | Only generate when a school requests or for SEO coverage |

Each subject follows the standard playbook: lessons → heroes → narration → practice Qs → KCs → flashcards → guide pages → related media.

### 2c — Complete remaining Unity assets

- [ ] Cinematic videos — 339 remaining at 20/day (~17 days). Continue daily batches.
- [ ] Podcasts — ~955 remaining (mostly Eng Lit). Continue daily batches at 200/day.
- [ ] Diagrams for multi-board content (pending — flagged in CLAUDE.md)

### Not in scope for Phase 2
- No new interactive features
- No new practice input types
- No commercial infrastructure (Stripe, etc.)

---

## Phase 3 — Deepen the Learning Experience

**Goal:** Transform StudyVault from "revision notes with quizzes" into "an interactive study platform." This is the retention play — students who are already here use it more and more effectively.

**Done when:** Universal practice mode is live with 3+ input types, and the cross-subject interleaved practice page works.

### 3a — Universal practice input types

Build reusable interactive components that work across subjects. Each one is a new input type in `practice.html` / `practice-loader.js`.

| Input Type | Description | Primary Subjects | Also Works In |
|------------|-------------|-----------------|---------------|
| **Text highlighting** | Select text spans to identify techniques/features | English Language | Eng Lit, History (source utility), RE, Science |
| **Image hotspot** | Click zones on an image to identify features | History (source analysis) | Geography (photos), Science (diagrams), D&T |
| **Drag-and-drop ordering** | Arrange items in correct sequence | History (timelines) | Science (processes), Music (notation) |
| **Labelling** | Place labels on a diagram/image | Science (diagrams) | Geography (maps), D&T, Music |
| **Categorisation** | Sort items into groups | Any subject | Causes/consequences, advantages/disadvantages |
| **Mark scheme reveal** | Student writes answer, then self-marks against model answer | Any essay subject | History, Eng Lit, RE, Business, Geography |
| **AI-marked writing** | Write a response, get instant AI feedback | English Language | Any subject with extended writing |

**Build order:** Mark scheme reveal (cheapest, works everywhere) → text highlighting → image hotspot → ordering → labelling → categorisation → AI marking (needs API route).

### 3b — Per-lesson practice mode

Any lesson can optionally have practice exercises. Student reads the lesson, then switches to practice mode for that topic.

- [ ] Practice mode toggle on lesson pages (article ↔ practice)
- [ ] `practice_data` JSONB column already exists — extend schema for new input types
- [ ] Lesson progress tracker gets "Complete practice" step
- [ ] Generate practice exercises for existing subjects (start with essay subjects + source-based subjects)

### 3c — Cross-subject interleaved practice

Standalone `/practice` page that pulls questions from across the student's selected subjects.

- [ ] Session UI — 15-20 mixed questions per session
- [ ] Interleaving algorithm — mix subjects AND input types
- [ ] Adaptive question selection:
  - Weighted by spaced repetition data (Leitner box state)
  - Prioritise topics with low KC scores or not revisited recently
  - Minimum threshold before unlocking (need enough visited lessons)
- [ ] Session summary — accuracy by subject, weak topics, "revise next" suggestions
- [ ] Connect to existing flashcard Leitner system — extend beyond flashcards to drive all question types

### 3d — Other learning features

These can be built in parallel with practice modes or slotted in as quick wins:

- [ ] Smart revision recommendations — "Today's Revision" on dashboard driven by spaced repetition algorithm instead of hardcoded demo data
- [ ] Rank-up / prestige system — gamification layer on subject progress bars
- [ ] Card & browse page design refresh — stronger visual identity
- [ ] Diagram & hero image bank — reuse QA'd assets across schools, reduce Gemini costs

---

## Phase 4 — Commercial Readiness

**Goal:** Schools can find StudyVault, sign up, pay, and onboard without Tom doing manual work for each one.

**Done when:** A teacher can discover StudyVault, sign up, choose their subject/board, get content generated, and pay — all self-serve. Tom's only involvement is QA.

### 4a — Ads on free tier

- [ ] Ad integration (AdSense or similar) on generic content pages
- [ ] Ad placement: top leaderboard, sidebar below KC, between Key Takeaways and footer
- [ ] Category filtering (no gambling, dating, weight loss — serving 15-year-olds)
- [ ] "Ad-free with school account" messaging

### 4b — Teacher dashboard (real data)

- [ ] Replace hardcoded demo data with real Supabase queries
- [ ] Student progress tracking (lesson visits, KC scores, revision tasks)
- [ ] Class-level insights and engagement metrics
- [ ] Parents' evening print view

### 4c — In-app AI marking

- [ ] `/api/mark` serverless function (Haiku, ~£0.0002/request)
- [ ] `ai_marking_requests` Supabase table
- [ ] Replace clipboard button with inline AI feedback
- [ ] Usage limits (10-20/month per student)
- [ ] Teacher visibility of marking data in dashboard

### 4d — Payment infrastructure

- [ ] Stripe integration — per-subject checkout + school-wide checkout
- [ ] Self-serve teacher sign-up flow (no Tom invitation needed)
- [ ] School code auto-generated on purchase
- [ ] Upgrade path: per-subject → school-wide (credit existing payments)

### 4e — Student accounts (premium tier)

- [ ] Individual student accounts (email + password, linked to school via code)
- [ ] Progress data moves from localStorage to Supabase
- [ ] Existing localStorage progress migrated on first login

### 4f — Submit to Teacher (marking queue)

- [ ] Students submit practice answers to teacher dashboard
- [ ] Teacher marking queue with AI pre-marking
- [ ] Assignment setting (teacher selects question → students see it)
- [ ] Bulk marking view

### 4g — Pipeline & QA improvements

- [ ] Teacher QA flow — content → `pending_review` → Tom QA → `ready_for_teacher` → teacher publishes → `live`
- [ ] Per-school content customisation overlay (teacher edits without affecting base content)
- [ ] Legacy file format support (.ppt/.doc → server-side conversion)
- [ ] Direct-to-storage uploads (bypass Vercel body limit)

---

## Phase 5 — Scale

**Goal:** Sell to MATs and large school groups. Handle 200+ schools without proportional increase in Tom's time.

**Done when:** Two MAT deals closed, automated QA catches 95%+ of issues, Tom's QA time is <1 hour per new subject.

- [ ] Microsoft SSO (Entra) + Google Workspace SSO
- [ ] MAT-level admin — single procurement, multi-school rollout
- [ ] Automated content QA (reduce Tom's review burden)
- [ ] Email service (Resend/SendGrid) for transactional notifications
- [ ] Niche exam board school targeting — database of which schools use which boards
- [ ] Spotify podcast distribution for school subjects
- [ ] Mobile app (Capacitor PWA wrapper) for App Store + Google Play

---

## What's NOT on the roadmap (and why)

| Idea | Why not now |
|------|-----------|
| VaultCards full port (head-to-head, achievements, XP) | The cross-subject practice mode (3c) supersedes this — build the new version, don't port the old one |
| School branding / white-label | Nice-to-have, not a purchase driver. Add when a school specifically asks |
| Curriculum mapping / SOW alignment | Teachers care about this but it's a rabbit hole. Revisit after Phase 4 |
| AI tutor / chatbot | High cost, hard to QA, liability risk. The mark scheme reveal + AI marking covers the same need more safely |
| Remotion promo video | Finish when needed for sales outreach, not before product is ready to sell |

---

## Guiding Principles

1. **Finish before you start.** QA what exists before generating more. Generate content before building features. Build features before adding payment.
2. **Coverage before depth.** A student whose subject doesn't exist won't wait for your practice mode. A student whose subject does exist will come back when you add features later.
3. **Every phase earns the next.** Phase 1 gives you a showcase. Phase 2 drives organic traffic. Phase 3 retains users. Phase 4 monetises them. Phase 5 scales.
4. **Don't build for hypothetical schools.** Build for Unity first (your live users), then for the next 20 schools, then for 200. Each phase's scope matches its audience.
5. **One-way doors need thought. Two-way doors need speed.** Content generation is two-way (regenerate if wrong). Payment infrastructure is one-way (hard to change pricing model). Move fast on the first, deliberate on the second.
