# Prescribed-Works Register

**First run:** 2026-08-06 · **Re-run:** every June, after boards publish next-year lists (AQA CSPs land 1 June on the secure portal; AQA History sites are announced 3 years ahead).

## Why this exists

The spec-currency audit (`docs/SPEC_CURRENCY_AUDIT_2027.md`) answers "is the qualification alive, and did the board amend the spec after we built?". It never compares lesson content against works the spec pins by name. Set works, study pieces, CSPs, set films, set plays, anthologies and historic-environment sites can rotate inside a healthy, unchanged qualification — or our build plan can simply omit one. Both happened (Music AQA study pieces; Media AQA CSPs). This register closes that gap.

**Method:** for each built subject whose spec names works, list what the board currently prescribes, diff against our live units/lessons, record the verdict. Matching is presence-level (do we teach this named work?), not a content fact-check — that is the fact-check pipeline's job.

## Subjects with NO named works (out of scope)

Maths, all sciences (required practicals are stable in-spec), Geography (case studies are centre-chosen), RS, MFL, Business, Economics, Computer Science, PE, Statistics, Astronomy, Citizenship, D&T, Engineering, Electronics, Geology, Food, Hospitality & Catering, H&SC, Sociology/Psychology (named studies live inside the spec, so spec-currency covers them), Cambridge Nationals exam units, Music Tech NCFE.

## Register — checked 2026-08-06

| Subject | Prescribed works | Our coverage | Verdict |
|---|---|---|---|
| **Music AQA** (free) | Study pieces first assessed 2026: AoS1 Beethoven Sym. 1 mvt 1; AoS2 Queen (Bohemian Rhapsody, Seven Seas of Rhye, Love of my Life); AoS3 Esperanza Spalding (I Know You Know, Little Fly, I Adore You); AoS4 Bartók Hungarian Pictures mvts 1/2/4/5. 2020-set pieces (Mozart K.622, Little Shop, Graceland, Kodály) had FINAL assessment 2025. | AoS1 ✅ AoS4 ✅ (right movements). **AoS2 ✗ AoS3 ✗ — no study-piece lesson at all.** Verified by full-field search: zero mentions of Queen/Spalding in any of 27 lessons. | 🔴 **HOLE — build Queen + Spalding articles** |
| **Media Studies AQA** (free) | Close Study Products. List published on the AQA secure portal each 1 June before the COURSE starts (two years before exams — the June-2027 list has existed since 1 June 2025); newspapers rotate EVERY year, others periodically. Exam questions name the CSPs. | 20 lessons, all framework theory (semiotics, narrative, industries, audiences). **Zero CSP lessons.** | 🔴 **HOLE — same class as Music. Need the 2027 CSP booklet (secure portal, teacher login) before building. Annual maintenance thereafter.** |
| **History AQA** (free + Unity) | Historic environment site rotates annually per British depth study. 2027 sites (AQA news, fetched 6 Aug 2026): Norman = Battle of Hastings; Medieval = Battle of Stirling Bridge; Elizabethan = Spanish Armada; Restoration = Dutch Raid on the Medway 1667. 2028: White Tower / Acton Burnell / Kenilworth / St Paul's. | **No unit has ever had a site lesson** (deliberate earlier decision, reversed 6 Aug 2026). Adjacent content exists in every unit (Hastings L2, Stirling Bridge in L11, Armada L8/Unity L9, Dutch Wars L11). | ✅ **Built 6 Aug 2026** — 5 site lessons at pending_review (scripts/history-sites/), PD-art heroes vision-gated. Fact-check + narration pending. Re-do for 2028 sites next June. |
| **Music Eduqas** (Unity) | Bach Badinerie; Toto Africa — both "from summer 2022 onwards", no end date. | Both taught (unit each). | ✅ |
| **Drama AQA** (free) | 9 set plays (live AQA page, fetched 6 Aug 2026): Crucible, Blood Brothers, Noughts & Crosses, 80 Days, Things I Know to Be True, R&J, Taste of Honey, Great Wave, Empress. | All 9 = our 9 set-text units, one for one. | ✅ |
| **Drama OCR** (Unity) | Performance text list v3.2 (Apr 2026). | Blood Brothers still listed (spec audit verified). Rise Up = devising stimulus, not set text. | ✅ |
| **English Lit AQA** (free + Unity) | 6 Shakespeare, 7 19th-c novels, modern texts incl 2023 additions (Leave Taking, Princess & the Hustler, My Name is Leon), Telling Tales, clusters: L&R, P&C, Worlds and Lives. | Free tier: complete — every option built. Unity: Macbeth/ACC/Animal Farm/P&C, all current. | ✅ |
| **English Lit Edexcel** (free) | Shakespeare ×6, modern ×12, 19th-c ×7, collections: Relationships, Conflict, Time and Place, Belonging. | All 29 units in spec (Journey's End curly-quote grep artefact — present). | ✅ |
| **English Lit OCR** (free) | J352 text list + Towards a World Unknown clusters (L&R, Conflict, Youth and Age). | All 20 units in spec. | ✅ |
| **English Lit Eduqas** (free) | Prose/drama list + NEW 15-poem anthology (first assessed 2027). | All 22 prose/drama units in spec; anthology rebuilt 2 Aug 2026 to the 2027 list. | ✅ |
| **Film Studies Eduqas** (free) | 5 comparative pairs, 5 US indie, 5 global English, 5 global non-English, 5 UK. | All 30 films match `specs/eduqas/film-studies-C670QS.md` (audit-verified current 1 Aug 2026). | ✅ |

## Annual June cycle (do together)

1. Re-run this register (diff board lists vs live units).
2. AQA Media: download new CSP booklet (secure portal), refresh CSP lessons.
3. AQA History: check announced sites for cohort+1.
4. Spec-currency audit (`_gen_spec_audit_worklist.py` → workflow).
5. Exam dates JSON for the new year.

## Known audit-tooling defect (fix pending)

`_gen_spec_audit_worklist.py` joins live subjects to the catalogue by spec-code token intersection. `C660U` (Unity Music) vs `C660QS` and `R180` (Sport Science) vs `J828` fail the join, so those qualifications appear TWICE in audit output — once researched via the live-subject fallthrough (correct) and once as "not-built" from the catalogue side (wrong). Latent risk: a withdrawal verdict on the catalogue row would be actioned as "do not build" instead of "retire live lessons". Fix: alias map or normalised code join.
