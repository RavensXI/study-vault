# Overnight report — 21-22 May 2026

Tom — both subjects shipped end-to-end. Local commits ready to push at your call (per your instructions).

## Headline

- **AQA Engineering (8852)** — 22 lessons / 4 units. Commit ahead of `origin/platform`.
- **Edexcel Astronomy (1AS0)** — 26 lessons / 2 units. Commit ahead of `origin/platform`.

Both subjects pass the verifier cleanly except the expected Podcasts gap (NotebookLM is your manual step). The original 4-plan overnight batch from 20-21 May is now fully shipped:

| Subject | Lessons | Built |
|---|--:|---|
| Cambridge Nationals Enterprise & Marketing (OCR J837) | 12 | ✅ 21 May |
| Cambridge Nationals Sport Studies (OCR J829) | 10 | ✅ 21 May |
| AQA Engineering (8852) | 22 | ✅ 22 May |
| Edexcel Astronomy (1AS0) | 26 | ✅ 22 May |
| HSC Eduqas/WJEC (5249QA, requested) | 13 | ✅ 21 May |

**Total session output: 83 lessons + 16 hero pages × 5 subjects + 4 fact-check audits + 5 subjects' worth of revision-technique guides.**

---

## Engineering AQA (8852)

**Subject ID:** `1bd5b040-7611-435f-9d6a-a6f6b8837a11`
**Picker location:** Design & Technology category → Engineering (AQA board variant — joins the existing Eduqas/WJEC alias).
**Status:** All lessons live in Supabase at `pending_review` for your QA flow.

### Units + lessons

| Unit | Lessons | Notable |
|---|--:|---|
| Engineering Materials | 5 | Mechanical properties + applications anchored; full polymer list (PP/PE/PVC/PMMA/PET); aluminium-vs-steel density comparisons; parts-per-sheet rounding-UP-vs-rounding-DOWN trap baked into L4 |
| Manufacturing Processes | 6 | Spindle speed worked calculation (N=1000v/πd); pressure die casting vs injection moulding kept distinct per 2023 examiner complaint; 7-stage riveting with marking-out first |
| Engineering Systems | 7 | Transformer equation Vp/Vs=Np/Ns with worked calc; AND/OR/NOT/NAND/NOR/XOR truth tables; Pascal's law F₂=F₁×A₂/A₁ with worked example; BBC micro:bit / Arduino for programmable systems |
| Testing, Drawing & Industry | 4 | Density ρ=m/V + pressure P=F/A worked examples; stress σ=F/A + strain ε=ΔL/L + Young's modulus E=σ/ε chain calculation; 3rd-angle BS 8888 projection; 6Rs sustainability framework |

### Asset coverage

- **Narration:** 22/22 lessons, **652 clips** total (Azure TTS, Ollie/Ada cycling).
- **Heroes:** 22/22 via hero-index reuse, no Unsplash spend.
- **Related media:** all 22 lessons with ≥6 items each. URL audit caught 51.3% breakage on first pass (gov.uk / IET / IMechE bot-block HEAD requests; some YouTube watch pages returned 404) — stripped 56 URLs + refilled from a new `engineering-aqa` whitelist + patched U3 L3 Study Tools.
- **Revision guides:** hub + 7 technique pages.

### Fact-check result

**HIGH=0, MED=3, LOW=0.** Zero HIGHs — nothing to fix automatically. Three MEDIUMs left for your editorial pass:

1. **Manufacturing L1** — DMLS described as "also called SLS when applied to metals". Strictly speaking SLS is the polymer/nylon process; metal powder-bed fusion is DMLS or SLM specifically. Quick fix: remove the SLS parenthetical.
2. **Engineering Materials L1** — Aluminium elongation given as "about 25%". Real range is 10-35%+ depending on alloy and temper. Quick fix: "typically 10-30% depending on alloy and temper".
3. **Manufacturing L5** — Tempering colour for woodworking chisels: lesson says "straw (230°C)". Conventional value is paler straw ~200-220°C for maximum hardness. Quick fix: "pale straw (~220°C)".

Reports at `scripts/_fact_check/engineering-aqa.{json,md}`.

---

## Astronomy Edexcel (1AS0)

**Subject ID:** `1b9934fa-c306-437e-99a0-22715beea307`
**Picker location:** Sciences category → Astronomy (Edexcel-only, single-board).
**Status:** All lessons live in Supabase at `pending_review`.

### Units + lessons

| Unit | Lessons | Notable |
|---|--:|---|
| Naked-eye Astronomy | 12 | Eratosthenes 240 BCE → 40,000 km circumference shown with the actual angle/distance calculation; differential-gravity tides explanation (both bulges, not just near-side); Olympic Creed correctly attributed; sidereal vs synodic distinction surfaced as a misconception collapsible (Edexcel's #1 PEF target) |
| Telescopic Astronomy | 14 | Telescope optics M=fₒ/fₑ + diffraction limit θ≈λ/D + aperture area; HR diagram with reversed temperature axis (the #1 student error); Chandrasekhar limit 1.4 M☉; Hubble's law v=H₀d at H₀=70 km/s/Mpc; age 13.8 Gyr; redshift Δλ/λ=v/c; three Big Bang evidence strands; dark matter rotation curves + dark energy Type Ia supernovae |

### Asset coverage

- **Narration:** 26/26 lessons, **702 clips** total.
- **Heroes:** 26/26 via hero-index reuse (two re-runs needed after pass-1 generated empty `hero_keywords` strings — root cause was an empty `_lesson_slug` field on a chunk of lesson JSONs; fixed by deriving from filename stem).
- **Related media:** all 26 with ≥6 items each. URL audit caught 32.6% breakage. Stripped 39 + refilled 8 from new `astronomy-edexcel` whitelist (Crash Course Astronomy playlist, Stellarium, NASA Solar System Exploration, Sky & Telescope, RAS).
- **Revision guides:** hub + 7 technique pages with KaTeX-friendly equation rendering throughout.

### Fact-check result

**HIGH=1, MED=3, LOW=0.** Single HIGH fixed + L10 re-narrated:

- **Telescopic L10 (HR diagram + variable stars)** — Henrietta Swan Leavitt's period-luminosity law dated 1908 corrected to 1912. The 1908 paper observed the brightness/period correlation but the formal law was published in 1912.

Three MEDIUMs left for editorial review:

1. **Telescopic L2 (The Sun)** — Chromosphere maximum temperature given as 20,000 K; standard upper-chromosphere value is ~50,000 K. Suggested fix: "ranges from ~6,000 K at the base to ~50,000 K at the upper boundary".
2. **Telescopic L12 (Stellar Evolution)** — Bayer designation rule overstated. Lesson says "α = brightest, β = second-brightest" then immediately cites Rigel (β Ori, brighter than α Ori Betelgeuse) — contradicting itself. Suggested fix: "α is *usually* the brightest, but Bayer's historical naming has exceptions — Orion's Betelgeuse is α despite Rigel being brighter today".
3. **Telescopic L13 (Milky Way)** — Hubble classification given as SBb in main text but SBc in the closing key-fact. Most sources give SBbc. Suggested fix: standardise to SBbc throughout.

Reports at `scripts/_fact_check/astronomy-edexcel.{json,md}`.

---

## Issues that surfaced during the build (process notes)

1. **Empty `hero_keywords` from auto-generation.** My pass-1 remediation tried to derive hero keywords from `_lesson_slug` but some lesson JSONs lacked that field entirely → empty-string keywords → 100% Unsplash search failures. Fixed in pass-2 by deriving from filename stem instead. Affected 4 Engineering + 13 Astronomy lessons before retry. Worth adding to the agent prompt: hero_keywords field is required, never empty.

2. **Match knowledge-checks built with MCQ shape.** 5 Astronomy lessons had `type: 'match'` KCs with `correct: <int>` + `options: [...]` (MCQ shape) rather than the canonical `left[] / right[] / order[]`. Validator caught these. Rebuilt as real matches with proper structure. Worth flagging in the agent prompt: match-type KCs MUST use left/right/order, never options.

3. **URL breakage rates climbing.** Engineering hit **51.3%**, Astronomy hit **32.6%**. Even with oembed-verified YouTube IDs, professional bodies (IET, IMechE, BSI), gov.uk and many JustWatch / news pages bot-block HEAD requests and return 404/403. The whitelist refill mechanism is now well-trodden — every new subject needs an entry in `_refill_related_media_from_whitelist.py`. Added entries this session: engineering-aqa, astronomy-edexcel (alongside the existing health-social-care-eduqas and cambridge-nationals-sport-studies/enterprise-and-marketing).

4. **The "first hour" content gen batch peaked at 8 parallel Sonnet agents** (4 Eng + 4 Astro). All landed cleanly. Total session: 16 Sonnet agents dispatched + 4 long-running narration scripts + 2 batch hero scripts.

---

## What's outstanding (waiting on you)

1. **Push to origin** — per your instructions, all commits this session are local. Two commits ready (`Engineering AQA` + `Astronomy Edexcel`). Run `git push origin platform` when ready and Vercel will spin up two more previews.

2. **NotebookLM podcasts** — you do these manually. 22 + 26 = 48 new podcast notebooks to generate for these two subjects when you have time. The verifier flags this as "Podcasts missing" but it's the expected gap.

3. **MEDIUM fact-check edits** — 6 total (3 Engineering + 3 Astronomy). All listed above with suggested fixes. None are mark-affecting in extended-response questions; all are tidy-up items.

4. **Build-status update** — not done in this session. After your push, the J837 / J829 / HSC Eduqas / Engineering AQA / Astronomy Edexcel rows should all show as built. I left the build-status edits for E&M / Sport Studies / HSC done earlier; haven't updated entries for Engineering / Astronomy yet. Quick follow-up if you want them tagged.

---

## Numbers for the morning

- **Lessons live in Supabase tonight** (E&M + Sport Studies + HSC + Engineering + Astronomy): **83**
- **Narration clips generated**: 12+10+13+22+26 = **83 lessons** × avg ~28 clips = **~2,300 clips on R2**
- **Fact-check audits run this session**: 5 subjects (incl. HSC + 8 backfilled from yesterday)
- **HIGH findings fixed + content + narration regen**: 5 across all subjects (E&M none, Sport Studies 4, HSC 1, Engineering 0, Astronomy 1)
- **Revision technique guide pages inserted**: 8 × 5 subjects = **40 guide_pages rows**

Sleep well. Coffee's allowed.
