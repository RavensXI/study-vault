# StudyVault — Commercialisation Strategy

## Product Vision

Schools upload their teaching resources (PPTs, worksheets) → AI generates polished, narrated revision sites → QA'd before going live → students get a branded revision platform. School keeps IP ownership; StudyVault handles tech + quality layer.

**Data separation principle:** Tom never sees uploaded source materials (school IP). Source files processed by AI then deleted. Generated revision content is visible to Tom for QA — that's the product.

---

## Pricing Models

### 1. Per-Subject Licensing (recommended starting model)
- **£250–400/subject/year**
- Maps directly to department budgets — Head of History can approve £300 without SLT
- Typical school starts with 3–5 subjects → £750–2,000/year
- Full adoption (15 subjects) → £3,750–6,000/year

### 2. Tiered School Licence (upsell once multiple departments want in)

| Tier | Subjects | Price/year | Effective per-subject |
|------|----------|------------|----------------------|
| Starter | Up to 3 | £500 | ~£167 |
| Standard | Up to 10 | £1,200 | ~£120 |
| Unlimited | All subjects | £2,500 | Depends on uptake |

### 3. Per-Pupil Pricing
- £2–5 per pupil per year (whole school or KS4 only)
- 1,200 students → £2,400–6,000/year
- Common in EdTech (Seneca ~£3–5/pupil) but schools wary of scaling costs in MATs

### 4. MAT/Trust-Level Deals (the real money)
- 10-school MAT: £15,000–30,000/year
- One procurement conversation covers 10 schools
- MATs love consistency across their trust

---

## Penetration Pricing Strategy

Start low to build market share and word of mouth, then raise prices for new schools once established. **Never raise prices on existing schools** — they took the risk early and they become your advocates.

### Why this works in education
- **Teachers talk to each other** — subject networks, TeachMeet events, edu Twitter/X. One enthusiastic Head of History is worth more than any marketing spend. Give them a price they'll rave about.
- **Early adopters take the most risk** — trying an unproven product from a new company. Reward that with a locked-in price that builds fierce loyalty.
- **Schools hate price surprises** — grandfathering is expected in education SaaS. "Your price never goes up" is a genuine selling point.
- **Margins can absorb it** — at ~48p/lesson generation cost, even £100/subject/year is 85% margin year 1 and 99%+ from year 2 onwards.

### Pricing Phases

| | Launch (first ~20 schools) | Standard (once established) |
|---|---|---|
| Per subject | **£100/yr** | £200–250/yr |
| Starter (3 subjects) | **£250/yr** | £500/yr |
| Unlimited | **£1,000/yr** | £2,000–2,500/yr |

**Launch price is locked in forever** for early schools. At £100/subject, a Head of Department can pay from their stationery budget without asking SLT. When they tell colleagues at other schools, they're saying "it's only £100 a year" — even though new schools pay double.

### Phased Rollout

**Phase 1 — Launch pricing, per-subject (first ~20 schools)**
- Lowest friction: single department can trial without whole-school buy-in
- Proves value quickly: one subject, one term, measurable impact
- Natural expansion: other departments ask for it
- Revenue: 20 schools × 3 subjects × £100 = **£6,000/yr** (cost: ~£360)

**Phase 2 — Standard pricing, introduce tiered licences**
- When 3+ departments in same school want in
- Unlimited tier is the upsell (margin lives here)
- Launch schools still pay launch prices — they're your case studies
- Revenue: 50 schools × mix of tiers = **£50,000–80,000/yr**

**Phase 3 — MAT-level deals at standard pricing**
- Case studies from Phase 1/2 schools
- Trust Director of Education as single buyer
- 10-school MAT at £1,500/school = £15,000/deal

---

## Free Tier Strategy

### Option A: Free Generic Content
Expand existing free History content to cover 5–6 heavy-hitter GCSE subjects (Maths, English, Science, History, Geography). Generic AI-generated content — not school-specific.

**Pros:** SEO/discovery, brand credibility, network effects (students share it)
**Cons:** Scale of work (200+ lessons), not as tightly aligned as bespoke product
**Revenue:** Ad-supported (see below)

### Option B: One Free Bespoke Subject Per School
School uploads resources for one subject, gets full revision site for free.

**Pros:** Eliminates purchase risk, creates internal champions, proves pipeline
**Cons:** QA cost with no revenue, freeloader risk

### Recommended: Both, Sequenced
1. **Now:** Existing content (History, Business, Geography, Sport Science) serves as generic free tier. Already built, zero extra work.
2. **When pipeline is ready:** Offer one free bespoke subject as onboarding hook. Scoped tightly (one component/paper, supported formats, QA on Tom's timeline).
3. **At scale:** "StudyVault Free" (generic, ad-supported, no login) vs "StudyVault for Schools" (bespoke, ad-free, login, analytics).

---

## Ad Revenue (Free Tier)

### Expected CPMs (UK education)
| Ad Type | CPM | Notes |
|---------|-----|-------|
| Display banner (AdSense) | £1–4 | Sidebar, footer |
| In-content native | £3–8 | Between sections |
| Programmatic (Mediavine/Raptive) | £4–10 | Requires scale |

### Revenue Projections
- **Year 1** (10k monthly students): £300–500/month = **£4,000–6,000/year** (covers infra)
- **At scale** (50k monthly students, 750k monthly pageviews): ~£2,250/month = **~£27,000/year**
- **Peak revision season** (March–May): traffic 3–4x, ad revenue £6,000–8,000/month

### Ad Placement Rules
- **Never:** during narration, in knowledge checks, in practice questions, pop-ups/interstitials
- **OK:** top leaderboard (above hero), sidebar (below KC section), between Key Takeaways and footer
- Filter out gambling, dating, weight loss categories (serving 15-year-olds)

### Strategic Value
Ads are simultaneously revenue AND a sales tool. Every ad impression is a micro-reminder that an ad-free premium version exists. The Spotify model: free is useful but slightly annoying, paid removes friction + adds bespoke features.

---

## Margin Analysis

### Infrastructure Costs (Monthly)
| Service | Current | At 500 schools |
|---------|---------|----------------|
| Supabase | Free/~£20 | ~£50–80 |
| Cloudflare R2 | Pennies | ~£30–50 |
| Vercel | Free/~£16 | ~£16–40 |
| Domain | ~£1 | ~£1 |
| **Total** | **~£5–20** | **~£100–170** |

### AI Generation Cost Per Subject (verified Mar 2026, 26-lesson Music subject)

| Component | Cost per lesson | 26 lessons |
|-----------|----------------|------------|
| Claude API (content + guides + media) | £0.39 | £10.14 |
| Gemini diagram | £0.05 | £1.30 |
| Azure narration | £0.04 | £1.04 |
| Hero images (Unsplash/Wikimedia) | Free | Free |
| **Total** | **~£0.48** | **~£12.48** |

Notes:
- Claude API cost includes prompt caching (~60% saving vs list price)
- Actual API balance drop: $12.63 (£9.97) for Claude, ~$1.74 (£1.37) Gemini, ~$1.28 (£1.01) Azure
- Smaller subjects (10 lessons) cost ~£5–6 total; larger subjects (40 lessons) cost ~£20–25
- Guides and media are per-subject (not per-lesson), so per-lesson cost drops slightly with more lessons

### Margins by Phase

**Phase 1 (20 schools, launch pricing, manual QA):**
- Revenue: 20 × 3 subjects × £100 = £6,000/year
- AI generation: 60 subjects × £12 = ~£720
- Infra: ~£300/year
- Your QA time: ~150 hours
- **Margin excl. time: ~83%**
- **Effective hourly rate: ~£33/hr** (but building the foundation)

**Phase 2 (50 schools, mix of launch + standard pricing):**
- Revenue: ~£60,000/year
- AI generation: ~£1,500 (one-off, year 1 only)
- Infra: ~£600/year
- Your time: ~300 hours/year
- **Margin excl. time: ~96%**
- **Margin incl. time at £40/hr: ~76%**

**Phase 3 (200+ schools, standard pricing, largely automated):**
- Revenue: £400,000–600,000/year
- Infra + AI: ~£6,000/year
- 1 QA hire: ~£30,000/year
- **Margin: ~94%+**

### Why Margins Are Exceptional
No engineering team (Claude Code + Python scripts), no content team (Gemini + Azure Speech), no infrastructure team (R2 + Vercel free tier). Generation cost is one-off per school — year 2+ is pure recurring revenue minus hosting. The only real cost is QA labour, which drops with automation.

---

## Revenue Projections

| Phase | Timeline | Revenue | Key Driver |
|-------|----------|---------|------------|
| Launch | Year 1 | £6,000/yr | 20 schools at launch pricing, word of mouth from Unity |
| Proving | Year 2 | £30,000–60,000/yr | 50 schools, mix of launch + standard pricing |
| Growth | Year 3–4 | £100,000–200,000/yr | 100 schools + 2 MATs, case studies |
| Scale | Year 5+ | £500,000–750,000/yr | 200 schools + 10 MATs |
| Ceiling | — | £2–3M/yr | 500 schools + 30 MATs (<15% market penetration) |

England alone has ~3,500 secondary schools.

---

## Conversion Funnel

```
Free generic content (SEO) → students discover StudyVault
         ↓
Students share with classmates → teachers notice
         ↓
Teacher explores → sees quality → "can we get this for Biology?"
         ↓
One free bespoke subject → school uploads resources → full experience
         ↓
Department loves it → other departments ask → school buys tiered licence
         ↓
School shows results → MAT rolls out trust-wide
```

---

## Key Risks

1. **Teacher friction** — upload process must be dead simple or adoption stalls
2. **Competing with free** — Seneca/BBC Bitesize are free. Differentiator is personalisation from school's own resources.
3. **QA bottleneck** — Tom is sole reviewer. Need automated QC or team, or teacher self-review with automated guardrails.
4. **Exam board changes** — specs change ~every 5 years. Actually a feature: recurring revenue because content stays current.

## Long-Term Play

Data flywheel: every school that uploads resources teaches the AI what good teaching looks like. Eventually offer "select AQA Biology and get a full revision site" without any upload — the accumulated data becomes the product. Flips from "we process your resources" to "we ARE the resource."

---

## Features That Drive Upgrades (Free → Premium)

| Free Tier | Premium (Schools) |
|-----------|-------------------|
| Generic AI content | Built from school's own resources |
| Ads present | Ad-free |
| No analytics | Teacher dashboard with student data |
| No school branding | School-branded |
| Major specs only | Exact spec match guaranteed |
| No login required | Login + progress tracking |
| Copy-to-clipboard AI marking | In-app AI marking (examiner-calibrated) |
| Community support | Direct support |

---

## Planned Feature: In-App AI Marking

### Current state
Practice questions have "AI Mark My Answer" button → copies question + mark scheme + student answer to clipboard → student pastes into ChatGPT/Claude. Works but zero friction, zero data capture.

### Planned upgrade
Direct in-app AI marking via Vercel Serverless Function (`/api/mark`). One click → examiner-quality feedback appears inline.

### Cost per marking request
~500–800 tokens in, ~300–500 out.

| Model | Cost/request | 28 students × 10/month × 10 months |
|---|---|---|
| Claude Haiku | ~£0.0002 | ~£0.56/year per class |
| GPT-4o-mini | ~£0.0003 | ~£0.84/year per class |
| Claude Sonnet | ~£0.002 | ~£5.60/year per class |

At 500 schools: ~£300–400/year total AI spend. Essentially free.

### Architecture
```
Student clicks "AI Mark" → POST /api/mark
  → Vercel function validates auth
  → Checks monthly usage limit (Supabase query)
  → Calls LLM with examiner-calibrated prompt
  → Saves request + response to Supabase
  → Returns structured feedback to browser
```

### Feedback structure
- **Marks awarded:** e.g. 3/4
- **Strengths:** What the student got right, with specifics
- **Gaps:** What's missing for full marks
- **Examiner tip:** Links to relevant exam technique guide

### Usage limits
10–20 markings/month per student (free with Premium subscription). Encourages quality over spam. Unlimited marking as a paid add-on (£50/year).

### Data value for teacher dashboard
Every marking attempt is logged — teachers can see:
- Which questions students are attempting
- Average scores on extended writing
- Weak areas in exam technique
- Improvement over time

This data is uncapturable in the current clipboard model.

### Supabase table needed
```sql
CREATE TABLE ai_marking_requests (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id text NOT NULL,
  lesson_slug text,
  subject text NOT NULL,
  question_text text NOT NULL,
  mark_scheme text NOT NULL,
  student_answer text NOT NULL,
  ai_feedback jsonb NOT NULL,
  model_used text,
  tokens_used int,
  created_at timestamptz DEFAULT now()
);
CREATE INDEX idx_marking_user_month ON ai_marking_requests (user_id, created_at);
```

### Build effort
1. One Vercel serverless function (`/api/mark.js`, ~80 lines)
2. One Supabase table (above)
3. System prompts per exam board (AQA, Edexcel, OCR)
4. Frontend: replace clipboard button with AI mark button + inline feedback display
5. Usage counter component ("7 of 10 markings remaining")

---

## Planned Feature: Submit to Teacher (Marking Queue)

### Concept
Students submit practice answers directly to their teacher via the platform. Replaces the current "copy to clipboard" flow with an in-platform submission that lands in the teacher dashboard.

Two buttons side by side on each practice question:
- **"AI Mark"** — instant AI feedback (for independent revision, evenings/weekends)
- **"Submit to Teacher"** — goes to teacher's marking queue (for homework, timed practice, answers that matter)

### Teacher Marking Queue (dashboard section)
- Submissions arrive sorted by date, filterable by class/student/question
- Each shows: student name, question text, mark allocation, student's answer
- Teacher writes feedback + marks awarded → "Return to Student"
- Student sees feedback next login (notification badge on practice section)

### Key workflows

**1. Set assignments:** Teacher selects a question from any lesson → sets a due date → students see it flagged on their lesson page → submit via the platform. Teacher gets all 28 answers in one view.

**2. Bulk marking:** When 25 students answer the same question, show all answers side by side. Much faster to mark than isolated submissions.

**3. AI-assisted marking:** AI pre-marks each submission (marks + feedback draft). Teacher reviews, adjusts marks, adds personalised comments. Cuts marking time by ~70% while keeping human quality. Students see "Marked by Mr Shaun" not "Marked by AI."

### Data generated
- Which students are doing practice (not just visiting lessons)
- Extended writing quality over time (teacher-validated scores)
- Which questions teachers are setting (popular = worth improving)
- Teacher marking turnaround times
- Comparison: AI marks vs teacher marks (calibration data)

### Supabase tables needed
```sql
CREATE TABLE student_submissions (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  student_id text NOT NULL,
  teacher_id text,               -- NULL if unassigned
  class_id uuid REFERENCES classes(id),
  lesson_slug text,
  subject text NOT NULL,
  question_text text NOT NULL,
  mark_scheme text NOT NULL,
  max_marks int NOT NULL,
  student_answer text NOT NULL,
  -- AI pre-marking (optional)
  ai_marks int,
  ai_feedback jsonb,
  -- Teacher marking
  teacher_marks int,
  teacher_feedback text,
  marked_at timestamptz,
  -- Assignment context (NULL if voluntary submission)
  assignment_id uuid,
  status text DEFAULT 'pending', -- pending | marked | returned
  created_at timestamptz DEFAULT now()
);

CREATE TABLE assignments (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  teacher_id text NOT NULL,
  class_id uuid REFERENCES classes(id),
  lesson_slug text,
  subject text NOT NULL,
  question_text text NOT NULL,
  mark_scheme text NOT NULL,
  max_marks int NOT NULL,
  due_date timestamptz,
  created_at timestamptz DEFAULT now()
);

CREATE INDEX idx_submissions_teacher ON student_submissions (teacher_id, status);
CREATE INDEX idx_submissions_student ON student_submissions (student_id, created_at);
```

### Commercial value
This is the feature that makes StudyVault indispensable for teachers, not just students. It replaces exercise books for extended writing practice. Once a teacher is setting homework through the platform and marking in the dashboard, switching away means losing their entire marking history and workflow. Strong retention driver.

---

## Content Revisions & School Customisation

### Types of change (by frequency)

| Frequency | Examples |
|---|---|
| **Rare** (every 5–8 years) | Exam board switch, complete spec change |
| **Occasional** (1–2/year) | Swapping optional topics within a spec, restructuring unit order |
| **Frequent** (ongoing) | Rewording a paragraph, adding a mnemonic, updating a teaching method for a question type |

### Why generation credits are the wrong model
- Creates anxiety about spending them — teachers hesitate to request changes
- "What counts as one generation?" is impossible to define fairly (a paragraph fix vs a full subject rebuild)
- Punishes the most engaged schools — the teachers who care most about quality hit the limit first

### Three-tier approach instead

#### Tier 1: Self-Service Edits (unlimited, free with Premium)

A lightweight CMS layer on top of generated content. Teachers click "Edit" on any lesson and make changes directly:

- Edit/reword text within a lesson
- Add mnemonics, teacher notes, school-specific context
- Reorder content sections
- Toggle sections on/off ("hide this collapsible for my students")
- Update exam technique guides with their preferred method/approach

Changes are saved **per-school** — the base content stays the same, the school's customisations overlay on top. Other schools using the same subject still see the original.

**Handles ~80% of change requests. Costs nothing. Zero involvement from us.**

#### Tier 2: Topic Swaps & Partial Rebuilds (included in Premium, queued)

When a school drops a topic and picks a different one, or needs new content for a different optional unit:

1. Teacher submits request via dashboard ("Switching from America to Cold War")
2. Uploads their resources for the new topic
3. AI generates new content → automated QC runs
4. Teacher reviews and approves (or flags issues)
5. Goes live

Included in Premium — no extra charge. Processed within ~2 weeks during term, faster during holidays. Most schools need 2–3 of these per year at most.

#### Tier 3: Full Subject Rebuild (one-off fee or included in higher tiers)

Complete exam board switch or new spec rollout — essentially re-onboarding that subject:

- Full regeneration from new resources
- New diagrams, narration, questions
- Full QA cycle

Pricing options:
- **Included once/year in Unlimited tier** — incentivises top-tier adoption
- **£150–200 one-off on lower tiers** — cheaper than initial subject cost (infrastructure exists)
- **Free when triggered by an actual spec change** — if AQA issues a new History spec, we regenerate for all schools on that spec simultaneously. Part of the service.

The spec-change guarantee is a major selling point: *"When the spec changes, we handle it. Your revision site updates automatically."* No other revision resource does this.

### Per-school customisation architecture

Data model supports a layered override system:

```
Base content (shared, maintained by StudyVault)
       ↓
School-level overrides (per-school customisations)
       ↓
What the student sees (merged at render time)
```

```sql
CREATE TABLE school_content_overrides (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  school_id uuid REFERENCES schools(id) NOT NULL,
  lesson_id uuid REFERENCES lessons(id),
  guide_page_id uuid REFERENCES guide_pages(id),
  -- What's being overridden
  override_type text NOT NULL,    -- 'replace_section' | 'hide_section' | 'append' | 'teacher_note'
  target_selector text,           -- CSS-style selector or section ID within content
  original_content text,          -- snapshot of what was replaced (for diffing)
  custom_content text,            -- the school's replacement/addition
  edited_by text NOT NULL,        -- teacher profile ID
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

CREATE INDEX idx_overrides_school_lesson ON school_content_overrides (school_id, lesson_id);
```

**Benefits of this approach:**
- One canonical version of each lesson maintained centrally
- Schools customise without affecting anyone else
- When base content updates (spec change), school overrides are preserved where they don't conflict
- Analytics: which parts of lessons are schools commonly changing? Signal that base content may need improving.
- School feels ownership over "their" version while we maintain the foundation

### Summary table

| Change type | How handled | Cost to school | Our effort |
|---|---|---|---|
| Text tweaks, mnemonics, rewordings | Self-service editor | Free (unlimited) | None |
| Toggle/reorder sections | Self-service editor | Free (unlimited) | None |
| Teacher notes / school-specific additions | Self-service editor | Free (unlimited) | None |
| New optional topic (upload resources) | Queued generation | Free with Premium | Low (automated) |
| New exam technique method | Self-service or queued | Free with Premium | Low |
| Full exam board switch | Queued generation | Included in Unlimited / £150 one-off | Medium |
| Spec change (exam board issues new spec) | We regenerate for all schools | Free — part of the service | Medium (batch) |
