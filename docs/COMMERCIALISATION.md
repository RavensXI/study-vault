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

## Recommended Phasing

**Phase 1 — Start with per-subject pricing (£250–350/subject/year)**
- Lowest friction: single department can trial without whole-school buy-in
- Proves value quickly: one subject, one term, measurable impact
- Natural expansion: other departments ask for it

**Phase 2 — Introduce tiered licences**
- When 3+ departments in same school want in
- Unlimited tier is the upsell (margin lives here)

**Phase 3 — MAT-level deals**
- Case studies from Phase 1/2 schools
- Trust Director of Education as single buyer

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

### AI Generation Cost Per Subject: ~£2–5
(Azure Speech ~£1–3 + Gemini API ~£0.50–2 + R2 storage pennies)

### Margins by Phase

**Phase 1 (10 schools, manual QA):**
- Revenue: 10 × £1,500 = £15,000/year
- Infra + AI costs: ~£500/year
- Your QA time: ~200–300 hours
- **Margin excl. time: ~97%**
- **Effective hourly rate: £50–75/hr**

**Phase 2 (50 schools, semi-automated QC):**
- Revenue: £100,000/year
- Infra + AI: ~£2,500/year
- Your time: ~500 hours/year (automated QC catches 80%)
- **Margin excl. time: ~97%**
- **Margin incl. time at £40/hr: ~77%**

**Phase 3 (200+ schools, largely automated):**
- Revenue: £400,000–750,000/year
- Infra + AI: ~£6,000/year
- 1 QA hire: ~£30,000/year
- **Margin: ~90%+**

### Why Margins Are Exceptional
No engineering team (Claude + Python scripts), no content team (Gemini + Azure Speech), no infrastructure team (R2 + Vercel free tier). The only real cost is QA labour, which drops with automation.

---

## Revenue Projections

| Phase | Timeline | Revenue | Key Driver |
|-------|----------|---------|------------|
| Proving | Year 1–2 | £15,000/yr | 10 schools, word of mouth from Unity |
| Growth | Year 3–4 | £140,000/yr | 50 schools + 2 MATs, case studies |
| Scale | Year 5+ | £750,000/yr | 200 schools + 10 MATs |
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
| Community support | Direct support |
