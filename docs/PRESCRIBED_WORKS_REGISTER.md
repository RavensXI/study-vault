# Prescribed-Works Register

**First run:** 2026-08-06 · **Re-run:** every June, after boards publish next-year lists (AQA CSPs land 1 June on the secure portal; AQA History sites are announced 3 years ahead).

## Why this exists

The spec-currency audit (`docs/SPEC_CURRENCY_AUDIT_2027.md`) answers "is the qualification alive, and did the board amend the spec after we built?". It never compares lesson content against works the spec pins by name. Set works, study pieces, CSPs, set films, set plays, anthologies and historic-environment sites can rotate inside a healthy, unchanged qualification — or our build plan can simply omit one. Both happened (Music AQA study pieces; Media AQA CSPs). This register closes that gap.

**Method:** for each built subject whose spec names works, list what the board currently prescribes, diff against our live units/lessons, record the verdict. Matching is presence-level (do we teach this named work?), not a content fact-check — that is the fact-check pipeline's job.

## Subjects with NO named works (out of scope)

Maths, all sciences (required practicals are stable in-spec), Geography (case studies are centre-chosen), RS, MFL, Business, Economics, Computer Science, PE, Statistics, Astronomy, Citizenship, D&T, Engineering, Electronics, Geology, Food, Hospitality & Catering, H&SC, Sociology/Psychology (named studies live inside the spec, so spec-currency covers them), Cambridge Nationals exam units, Music Tech NCFE.

RS checked again 16 Sep 2026 when **Religious Studies B (Edexcel 1RB0)** was built: the specification names scripture passages inside its own content points (Matthew 3:13&ndash;17, Surah 112, Talmud Yoma 83&ndash;84 and so on), and those travel with the spec text, so spec-currency covers them. Nothing rotates by year and there is no set text, set work or anthology to gate. The same is true of every other RS specification we hold.

## Register — checked 2026-08-06

| Subject | Prescribed works | Our coverage | Verdict |
|---|---|---|---|
| **Music AQA** (free) | Study pieces first assessed 2026: AoS1 Beethoven Sym. 1 mvt 1; AoS2 Queen (Bohemian Rhapsody, Seven Seas of Rhye, Love of my Life); AoS3 Esperanza Spalding (I Know You Know, Little Fly, I Adore You); AoS4 Bartók Hungarian Pictures mvts 1/2/4/5. 2020-set pieces (Mozart K.622, Little Shop, Graceland, Kodály) had FINAL assessment 2025. | AoS1 ✅ AoS4 ✅ (right movements). **AoS2 ✗ AoS3 ✗ — no study-piece lesson at all.** Verified by full-field search: zero mentions of Queen/Spalding in any of 27 lessons. | 🔴 **HOLE — build Queen + Spalding articles** |
| **Media Studies AQA** (free) | Close Study Products. List published on the AQA secure portal each 1 June before the COURSE starts (two years before exams — the June-2027 list has existed since 1 June 2025); newspapers rotate EVERY year, others periodically. Exam questions name the CSPs. | 20 lessons, all framework theory (semiotics, narrative, industries, audiences). **Zero CSP lessons.** | 🔴 **HOLE — same class as Music. Need the 2027 CSP booklet (secure portal, teacher login) before building. Annual maintenance thereafter.** |
| **History AQA** (free + Unity) | Historic environment site rotates annually per British depth study. 2027 sites (AQA news, fetched 6 Aug 2026): Norman = Battle of Hastings; Medieval = Battle of Stirling Bridge; Elizabethan = Spanish Armada; Restoration = Dutch Raid on the Medway 1667. 2028: White Tower / Acton Burnell / Kenilworth / St Paul's. | **No unit has ever had a site lesson** (deliberate earlier decision, reversed 6 Aug 2026). Adjacent content exists in every unit (Hastings L2, Stirling Bridge in L11, Armada L8/Unity L9, Dutch Wars L11). | ✅ **2027 set built + fact-checked + narrated 6 Aug 2026**; **2028 set built same day** (White Tower, Acton Burnell, Kenilworth ×2, St Paul's — appended after the 2027 lessons). Cohort-year scoping LIVE on sandbox loaders: `subjects.settings.exam_year_lessons` + `studyvault-exam-year` filter in browse + prev/next nav (staff and no-year users see all; titles carry the year). Next June: 2029 sites + swap the maps. |
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
2. AQA Media: download new CSP booklet (secure portal), refresh CSP lessons. Search 15 Sep 2026: the 2027 GCSE booklet is NOT online anywhere public (school-hosted copies stop at 2025; the A-level 2027 booklet is public but not the GCSE one). AQA news 14 Sep 2026: for summer 2028 the video game CSP Blackpink The Game (service ended 31 Aug 2026) is replaced by LEGO Fortnite; the Blackpink music video stays. Both the 2027 and 2028 GCSE booklets sit on AQA Centre Services (teacher login).
3. AQA History: check announced sites for cohort+1.
4. Spec-currency audit (`_gen_spec_audit_worklist.py` → workflow).
5. Exam dates JSON for the new year.

## Known audit-tooling defect (fix pending)

`_gen_spec_audit_worklist.py` joins live subjects to the catalogue by spec-code token intersection. `C660U` (Unity Music) vs `C660QS` and `R180` (Sport Science) vs `J828` fail the join, so those qualifications appear TWICE in audit output — once researched via the live-subject fallthrough (correct) and once as "not-built" from the catalogue side (wrong). Latent risk: a withdrawal verdict on the catalogue row would be actioned as "do not build" instead of "retire live lessons". Fix: alias map or normalised code join.

## Cohort-rotation audit — 13 Sep 2026

**Question:** across every live subject's specification, what content depends on the exam year the student sits, and is each such thing gated on the site? Method: eight agents read all 113 live subjects' specs (95 matched spec files plus the unmatched ones by filename) for year-bound prescriptions, rotating sites, pre-release material, withdrawn options and spec end dates, with a web check of the board page where the spec said "published separately". Then each finding was checked against the live corpus and the site's gates (`subjects.settings.exam_year_lessons`, the wizard option pickers, `SUNSET_YEARS`).

### Rotates by exam year (revision content) — and how it is gated

| Subject | What rotates | Our corpus | Gate |
|---|---|---|---|
| History AQA (free + Unity) | Historic environment site, every year, per British depth study. 2027 = Hastings / Stirling Bridge / Armada / Medway; 2028 = White Tower / Acton Burnell / Kenilworth / St Paul's; **2029 not yet published**. | 2027 and 2028 site lessons built. | ✅ `exam_year_lessons` per lesson. Build 2029 when AQA publishes (June cycle). |
| History Eduqas (free) | Nominated historic site, every two years, per thematic study. 2026–27 = Policing in Liverpool / Letchworth / Chatham dockyards / Glastonbury. **New sites for 2028+ not yet nominated.** | Site lessons for the 2026–27 set (L10 / L9 / L9 / L9). | ✅ **Gated 13 Sep 2026** to 2027 (was unguarded: a 2028 student would have revised the wrong site). Build the 2028 sites when nominated. |
| Latin Eduqas (free, pending review) | Narratives every two years (2026–27 Livy + Virgil Hercules; **2028–29 Apuleius Cupid & Psyche + Virgil Aeneas and Anchises**, announced April 2026); themes and Roman Civilisation topics every three years (2027–29 Heroes and Villains / Come Dine with Me; Slavery / Festivals). DVL fixed. | Narratives unit = 2026–27 pair; themes and civilisation units = 2027–29 set. | ✅ Narratives unit gated to 2027 (13 Sep). **Build the 2028–29 narratives** for the Year 10 cohort; re-key. |
| Geography Eduqas (free) | Component 3 fieldwork: WJEC names one methodology + one conceptual framework per year. 2027 = Change over time + Sphere of influence; 2028 = Transects + Place; 2029 = Flows + Inequality; 2030 = Qualitative surveys + Mitigating risk. | Fieldwork Enquiry unit is generic (3 lessons); teaches no year's pair. | ✅ **Built 13 Sep 2026**: L4 (2027: change over time + sphere of influence) and L5 (2028: transects + place) appended, keyed by year, at pending review. Add L6 for 2029 (geographical flows + inequality) in the June 2027 cycle. |
| Music AQA (free) | Study pieces replaced in one rotation, 2026 onwards (Beethoven Sym 1 / Queen / Esperanza Spalding / Bartók Hungarian Pictures mvts 1,2,4,5). No next rotation announced. | On the 2026 set. (Lesson title says "Hungarian Sketches"; AQA's name is Hungarian Pictures.) | ✅ Nothing to gate. Watch AQA. |
| Media Studies AQA (free) | Close Study Products: booklet each 1 June, newspapers yearly, secure portal. | Zero CSP lessons (known hole, register above). | n/a until CSPs are built. |
| Film Studies Eduqas (free) | Set-film list versioned by first-assessment year (current list from 2024; review window "every three to five years" opens 2027 — nothing announced). Timeline appendix extended to 2018 from 2024. NEA brief from 2027 lives on the WJEC Portal, no longer in the spec. | All 30 current films; timeline lesson covers 1995–2018. | ✅ Watch the monthly Eduqas circulars. |
| English Literature Eduqas (free) | Poetry anthology: 18-poem set last examined 2026; 15-poem set first examined 2027. Text lists on a three-year review, no change announced. | Anthology unit = the 15 new poems. | ✅ (2026 cohort has sat.) |
| English Literature AQA / Edexcel / OCR | Additions and withdrawals all pre-2025 and in force (AQA: History Boys, Curious Incident, Never Let Me Go last exam 2024; OCR: Leave Taking from 2024, anthology v2). | No withdrawn texts in any corpus. | ✅ |
| History OCR A (free) | Site study is OCR-set but **fixed**: Spitalfields (from 2020) and Kenilworth Castle; three-year review with two years' notice, so no change possible before 2029. | Units match. | ✅ |
| Drama OCR J316 (Unity) | Spec withdrawn: final first teach Sept 2026, final exams summer 2028. The 2028 set-text swap (Blue Remembered Hills, Noughts & Crosses) was **cancelled** 13 Apr 2026; seven texts stand to the end. | Blood Brothers (on the list). | ✅ Repo spec refreshed to v3.2 (13 Sep). Unity needs a new board after 2028. |
| Cambridge National Sport Studies (free) | R184 asks for "current" examples (emerging sports, initiatives, rule changes). | Examples run to Paris 2024 / 2026. | ✅ Refresh at the June cycle. |
| Computer Science Edexcel (free) | Paper 2 Programming Language Subset reissued per series (v5 2024, v6 2025; 2026 not yet seen). | Programming with Python unit (6 lessons). | Checked 13 Sep 2026 against PLS v6: five lessons corrected in place (records as lists, open/close, no negative indexes/global/end=/sum()/membership in) and re-narrated; L7 string formatting and L8 library modules + turtle added at pending review. Re-check for a PLS v7 after 31 Jan 2027. Worklist: `scripts/_fact_check/computer-science-edexcel_pls_check_2026-09-13.md`. |

### Fixed per option (centre-chosen) — no year gate needed
History Edexcel (historic environment fixed per thematic study: Whitechapel / Western Front / London WW2; Issue 6 content from 2026, our spec is Issue 6), Drama AQA (nine plays, no year ties), Music Edexcel (eight set works, no end date), Music Eduqas (Badinerie + Africa, "no plan to change"), Music OCR (no set works at all), Classical Civilisation OCR, all RS, all MFL, Geography AQA/Edexcel/OCR case studies and fieldwork, D&T designers list, PE activity lists.

### Pre-release and NEA material (changes yearly, not revision content)
Geography AQA Paper 3 booklet (12 weeks before the exam — the one pre-release students revise; not buildable in advance), Media AQA NEA briefs, D&T AQA/Edexcel/Eduqas contextual challenges, Engineering AQA brief, Food AQA/Eduqas tasks, Music Edexcel/Eduqas/OCR composition briefs, Drama OCR stimulus paper, Film Eduqas production brief, every Cambridge National and WJEC Level 1/2 set assignment, BTEC HSC set assignments, NCFE Music Tech brief, CS Eduqas prep task. Geography Edexcel B's Paper 3 booklet is handed out in the exam.

### Spec end dates found
- OCR Drama J316: last exams summer 2028 (Unity).
- Eduqas **Food Prep C560QS: not ending** — Ofqual 601/8093/6 "Available to learners", no end date; Eduqas has a summer 2027 exam scheduled. The June audit's "2027" was the Wales-only 601/8085/7. Sunset entry removed from `index.html` (13 Sep).
- Eduqas Computer Science C500QS and D&T C600QS: an agent flagged retirements, but those are the Wales (WJEC 3xxx) qualifications; the England pages and the Ofqual register show no end date. No action.
- L1/2 ICT 5539QA: Wales ends 2028; England has no confirmed end date (DfE funding window to 31 Jul 2027 is not a teach-out).
- OCR Twenty First Century Science J257–J260: **not ending** — Ofqual null end dates (review 2034), 2027 fees and timetable published, equations-sheet rule applies from 2028. The "2027" was the DfE funding-approval end date, which Gateway A carries too. Sunsets removed (13 Sep). Rule: a DfE funding end date is never a withdrawal; only a board notice or an Ofqual end date sets a final series.
- Two other timing changes already correct on our guides: Edexcel Geography A Paper 1 and B Paper 2 are 1h45 from 2026.
