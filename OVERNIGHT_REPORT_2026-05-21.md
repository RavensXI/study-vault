# Overnight report — 19-20 May 2026

Tom — both jobs delivered. Branch `platform`, two commits, pushed.

## 1. AQA Religious Studies Short Course (8061) — WIRED

Treated as a pure repackaging of AQA Spec A (8062) as you suggested. Same
Supabase row, no new lessons, no new units.

**What it gives the student.** A new board option "AQA Short Course" on the
RE picker, with:
- Pick **2 of 4 religions** — Buddhism, Christianity, Islam, Judaism (Beliefs
  only, no Practices, per the 8061 spec).
- Both themes tap-selected (the helper text says so) — **Theme A:
  Relationships & Families** and **Theme B: Religion, Peace & Conflict**. The
  second one maps to Spec A's Theme D, just relettered to "B" in 8061 wording.

**How it works under the hood.**
- New entry `'AQA Short Course': true` in `boardConfig['religious-studies']`.
- New variant `'aqa short course'` in `religiousEducationOptions` — 4 religions,
  2 themes, caps both at 2.
- `slugMap['religious-studies']['aqa short course']` → `religious-studies-aqa`
  (same row as full Spec A).
- Wizard save logic writes `entry.course_type = 'short'` when this board is
  selected.
- `reAqaFilter` in `js/free-user-filters.js` honours `pref.course_type === 'short'`
  and skips `*-practices` units, so the student only sees Beliefs lessons +
  the two themes.
- Subject row `spec_code` bumped to `"8062 / 8061"` so the build-status page
  counts both specs as built. Idempotent script left at
  `scripts/_set_re_aqa_spec_code_dual.py`.
- BUILD_NOTES updated in `admin/build-status.html` (both religious-studies and
  religious-education entries) to show WIRED state.

**Commit:** `a74d513` "RS AQA Short Course (8061): wire as alias of Spec A (8062)"

**Worth testing in the morning:**
- Open the picker → pick Religious Studies → board "AQA Short Course".
- Confirm you can pick exactly 2 of 4 religions and 2 of 2 themes, then Continue.
- Hit the homepage RE card → it should count only ~10 lessons (2 religions ×
  one Beliefs unit each + 2 themes), not the full Spec A count.
- Visit `/browse/religious-studies-aqa` → no Practices units should be visible
  for that user.

## 2. Phase-1 plans — 4 single-board subjects

Planning JSON only — no Supabase activation, no content gen. Built so the
build-status page would drop a row each once they're queued for full builds.
All four passed the planner's own validation gates (no spec codes in
user-facing strings, accent_badge translucent, citations on misconceptions,
etc.).

Files all in `scripts/_plan_<slug>.json`. **Commit:** `ea6af52`.

### Cambridge Nationals Enterprise & Marketing (OCR J837)
- **Slug:** `cambridge-nationals-enterprise-and-marketing`
- **Scope:** R067 only (40% written exam). R068/R069 NEA portfolio units
  excluded per coursework-only policy.
- **Structure:** 1 unit ("Enterprise and Marketing Concepts"), 12 lessons.
  TA1=2, TA2=2, TA3=2 (calculations), TA4=4 (largest — extended evaluation
  always targets here), TA5=2.
- **Transfer baseline: HIGH** — 7 lessons port from `business-edexcel`,
  4 medium, 1 fresh.
- **Key gotcha from OCR Jan 2025 examiner report:** the #1 discriminator for
  lower-performing candidates was "writing answers which were not applied" —
  baked into the teaching brief. Prescriptive spec quirks also flagged
  (salaries/utilities = FIXED, not variable; loan repayments aren't a cost
  but interest is; no break-even formula recall; no plc; no 7Ps).
- **Sept 2025 spec change:** TV advert added to 4.3 — content should
  emphasise this on first build.
- **Hero colour:** `#b45309` (matches existing `business-edexcel`).

### Cambridge Nationals Sport Studies (OCR J829)
- **Slug:** `cambridge-nationals-sport-studies`
- **Scope:** R184 only (Contemporary Issues in Sport). R185-R187 NEA excluded.
- **Structure:** 1 unit, 10 lessons covering all 5 R184 topic areas.
- **Transfer baseline: LOW** — most lessons `fresh`. Three rated `medium`
  against AQA PE socio-cultural (values, etiquette, PEDs, tech) where the
  analytical pattern can borrow but content needs rewriting.
- **9 cited misconceptions** drawn from OCR spec, SAM, UKAD Whereabouts.
- **Currency warning baked in:** Paris 2024, padel/pickleball, UKAD sanctions,
  VAR policy — needs a 2-3 year refresh cycle.
- **Hero colour:** `#dc2626` (vibrant red).

### AQA Engineering (8852)
- **Slug:** `engineering-aqa`
- **Scope:** Written paper only (60%). 3.6 NEA design-process work excluded.
- **Structure:** 4 article units / 22 lessons / 0 practice units (calculations
  integrated into article lessons, mirroring the 120-mark paper's integrated
  maths design).
  - U1 Engineering Materials (5 lessons, steel-grey)
  - U2 Manufacturing Processes (6 lessons, industrial-amber)
  - U3 Engineering Systems (7 lessons, industrial-blue — biggest unit)
  - U4 Testing, Drawing & Industry (4 lessons, industrial-teal)
- **Transfer baseline: MEDIUM** — 3 high / 15 medium / 2 low / 2 fresh.
  ~70% materials/manufacturing/CAD ports from `design-and-technology-aqa`;
  electrical + stress/strain calcs from Separate Sciences Physics.
  Microcontrollers + structural/pneumatic/hydraulic systems are genuinely
  fresh ground.
- **18 cited misconceptions** from AQA 8852/W examiner reports 2022 + 2023,
  plus 8852/C NEA report 2023.
- **Hero colour:** `#475569` (steel grey).

### Edexcel Astronomy (1AS0)
- **Slug:** `astronomy-edexcel`
- **Structure:** 2 article units / 26 lessons (Naked-eye Astronomy: 12;
  Telescopic Astronomy: 14). All 16 spec topics covered, 215 spec-reference
  points mapped, zero gaps.
- **Transfer baseline: MEDIUM** — 2 high (stellar evolution L12, cosmology
  L14 from `separate-sciences-aqa`), 4 medium, 4 low, 16 fresh. Observational
  astronomy + telescope optics are largely fresh.
- **All-article (no practice unit)** — AO3 only 20% and calculations are
  1-2 marks embedded across topics, so fragmenting would break conceptual
  flow. Planner followed the prompt's "default to article" rule.
- **12 cited misconceptions** from Edexcel 2023+2024 Principal Examiner
  Feedback (tides/eclipse/occultation/Mercury/magnetosphere/diagrams),
  FutureLearn, Sheffield phy217, NAAP.
- **KaTeX-friendly formulas:** d=1/p, m-M=5log(d)-5, v=H₀d, T²/r³=const,
  M=fₒ/fₑ, Δλ/λ=v/c — referenced in the teaching brief for content writers.
- **Hero colour:** `#312e81` (deep indigo, midnight blue).

## Scratch files left behind

The Engineering planning agent dumped 3 examiner-report conversions to repo
root as scratch — `scripts_eng_examiner_2022W.txt`,
`scripts_eng_examiner_2023C.txt`, `scripts_eng_examiner_2023W.txt`. They're
not part of the plan output and they're not tracked. Safe to delete, or
keep as evidence-base reference. I left them untracked.

Also untracked but you may want to keep: `scripts/_batch_podcast_state.json`
(podcast batch state — was already in your working tree before tonight,
unrelated to this work).

## What's next

Recommend hitting "Push" on full builds for the two Cambridge Nationals
subjects first — they're both small (10 and 12 lessons), Enterprise has the
highest transfer baseline (~7/12 ports from existing business content), and
knocking off two single-board OCR rows in one push makes the build-status
page look noticeably tidier. Engineering and Astronomy are bigger
(22 and 26 lessons) and have more fresh-content lift; happy to queue
those next if you want.

Hope you slept well.
