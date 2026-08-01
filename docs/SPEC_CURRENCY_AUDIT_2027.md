# Spec-Currency Audit — 2027 Cohort (all subjects, all boards)

**Run:** 2026-08-01 · **Scope:** 194 qualifications = every catalogued spec (specs/index.json, all boards) unioned with everything we ship. Build status: {'not-built': 73, 'both': 17, 'free': 83, '?': 20, 'school': 1}.

**Result:** 148 GREEN · 29 AMBER · 17 RED.

Method: per-qualification research agent (Ofqual register operational/cert end dates + board amendment pages), every RED/withdrawal adversarially re-verified. For built specs RED/AMBER = act now; for not-built specs the verdict is a BUILD-READINESS signal (RED = do not build / superseded). Re-run: `_gen_spec_audit_worklist.py --scope full` → workflow `spec-currency-audit-2027` → this script.

> **Systemic note — Wales reform (Wales IS a planned build market).** WJEC `3xxxQS`/`3xxxCS` legacy GCSEs (Curriculum for Wales) are being withdrawn — final full assessment Summer 2026, Jan-2027 resit only, no Summer 2027 series — and REPLACED by new "Made-for-Wales" GCSEs (first teaching 2025/2026). So a WJEC legacy RED below means **build the Made-for-Wales replacement** (a future build target we have not yet catalogued), NOT ignore. Our existing "Eduqas / WJEC" aliased content stays fine for **England (Eduqas, Cxxx)**; for reformed subjects the **Wales arm diverges** and becomes a SEPARATE Made-for-Wales build/row (the aliasing no longer holds). See memory project_wales_build_plan.

## 1. Built content needing action (10)

Subjects we ship that are RED or AMBER — real 2027-cohort exposure.

- `RED/free` **French** — Eduqas `C800QS` (conf high)
  - **End date:** Operational end date 28 February 2025; final certification date 31 August 2025 (last exam series summer 2025)
  - **What changed:** No post-build amendment. The defect is pre-existing withdrawal, not drift. Ofqual lists WJEC Eduqas Level 1/Level 2 GCSE (9-1) in French, QN 601/8900/9, as "No longer awarded", operational end 28 Feb 2025, final certification 31 Aug 2025. Eduqas's own qualifications list carries no GCSE French — only AS/A Level French (A800QS). Eduqas trailed a reformed GCSE French for first teaching Sept 2024, but the draft never completed accreditation; the Ofqual register shows only two available GCSE French 
  - **Action:** Retire the subject. Remove Eduqas from the French board picker and de-list the 26 free-tier French Eduqas lessons — no 2027 student can sit this qualification, and the content is built from a spec whose last exams were summer 2025. Point students to AQA or Pearson Edexcel French, the only boards with live reformed GCSE French specs. Apply the same check and the same fix to Eduqas Spanish C820QS (QN 601/8901/0), also "No longer awarded" and built the same day, 2026-06-07.
  - Evidence: https://find-a-qualification.services.ofqual.gov.uk/qualifications/60189009 · https://find-a-qualification.services.ofqual.gov.uk/qualifications?title=French&qualificationTypes=GCSE%20(9%20to%201) · https://www.eduqas.co.uk/qualifications/

- `RED/free` **GCSE Computer Science (Wales, teaching from 2017)** — WJEC `3500QS` (conf high)
  - **End date:** Summer 2026 = final full assessment. January 2027 = resit-only opportunity, subject to demand. No summer 2027 series.
  - **What changed:** No material content amendment after 2026-05-19. The spec text stays at Version 3 (January 2019). The change is a WITHDRAWAL, not an amendment. WJEC's own qualification page carries the notice: "Summer 2026 will be the final full assessment opportunity for this qualification. A resit opportunity for examinations will be available in January 2027, subject to demand." It also states that from September 2025 learners must not be entered onto 3500QS in Year 10 and must instead take GCSE Computer Scie
  - **Action:** RED — retire this content for the 2027 cohort. Do not serve WJEC 3500QS material to students who sit exams in summer 2027, because no summer 2027 series exists. Our free-tier build of 2026-05-19 is aligned to the retired 3500QS spec. Two options: (1) rebuild against WJEC 3460QS ("Made for Wales", teaching from September 2025, first award 2027) if we want Wales Computer Science coverage; or (2) unpublish the WJEC Computer Science option and leave AQA, Edexcel, OCR and Eduqas s
  - Evidence: https://www.wjec.co.uk/qualifications/computer-science-gcse/ · https://www.wjec.co.uk/qualifications/gcse-computer-science-teaching-from-2025/ · https://www.wjec.co.uk/qualifications/

- `RED/free` **GCSE Spanish (WJEC Eduqas)** — Eduqas `C820QS` (conf high)
  - **End date:** Operational end date 28 February 2025; final certification date 31 August 2025 (Ofqual). Ofqual status: "No longer awarded". Last exam series: summer 2025. No summer 2026 series and no summer 2027 series.
  - **What changed:** No amendment issue. The problem is withdrawal, not version drift. Eduqas withdrew GCSE Spanish before our 2026-06-07 build. Eduqas trailed a reformed GCSE Spanish (first teaching September 2024, first assessment summer 2026) in its article "Bringing languages to life", but that qualification was never brought to market: there is no Eduqas GCSE Spanish page in the Eduqas sitemap, no Eduqas GCSE Spanish record on the Ofqual register, and no C820 entry code in the Eduqas exam timetables. Eduqas has
  - **Action:** RED — DO NOT serve this for the 2027 cohort. Eduqas GCSE Spanish C820QS is withdrawn and was already dead when we built it on 2026-06-07. Ofqual (QN 601/8901/0) gives status "No longer awarded", operational end date 28 February 2025 and final certification date 31 August 2025. The joint Wales-and-Eduqas GCSE timetables confirm this from the entry-code side: 22 other Eduqas C-code GCSE families appear in both the summer 2026 and summer 2027 timetables, but C820 (Spanish), C800
  - Evidence: https://find-a-qualification.services.ofqual.gov.uk/qualifications/60189010 · https://www.qualifications.education.gov.uk/Qualification/60189010 · https://www.eduqas.co.uk/media/1awnxucv/summer-2027-wales-and-eduqas-gcse-final-version-080726.pdf

- `RED/free` **Religious Studies** — WJEC `3120QS` (conf high)
  - **End date:** Summer 2026 = final full assessment. January 2027 = resit examinations only, subject to demand. No summer 2027 assessment.
  - **What changed:** No material content amendment to 3120QS was found after 2026-05-08. The decisive issue is not drift, it is withdrawal. WJEC states on its own qualification page: "Summer 2026 will be the final full assessment opportunity for this qualification. A resit opportunity for examinations will be available in January 2027, subject to demand." The same page also states: "From September 2025, learners must not be entered onto this qualification in Year 10, they should be entered for GCSE Religious Studies
  - **Action:** Do not serve this specification to the 2027 cohort, and do not build further content against it. A student sitting Religious Studies in Wales in summer 2027 is on the new Made-for-Wales specification 3150QS, not 3120QS. Our content dated 2026-05-08 is built to a specification whose last full exam is summer 2026. Take three steps. First, confirm whether WJEC 3120QS content is actually live on the free tier — the Religious Studies row in CLAUDE.md lists AQA, Edexcel and Eduqas 
  - Evidence: https://www.wjec.co.uk/qualifications/religious-studies-gcse/ · https://www.wjec.co.uk/qualifications/religious-studies-gcse/#tab_keydocuments · https://www.wjec.co.uk/qualifications/gcse-religious-studies-teaching-from-2025/

- `AMBER/free` **Cambridge Nationals Level 1/Level 2 in Enterprise and Marketing** — OCR (Cambridge OCR) `J837` (conf high)
  - **What changed:** Spec moved from Version 5 (September 2025) to Version 6 (June 2026), issued after our 2026-05-21 build. Verified directly from the live spec PDF "Specification updates" table. Version 6 changes: hyperlinks refreshed throughout; unit recording sheets (URS) and set-assignment feedback form now only on Teach Cambridge; Section 4.3 — the AIM of unit R068 updated to reflect a change to the set-assignment tasks; Section 4.3/4.4 — marking-criteria grids for R068 and R069 updated; Section 5.4 — marks ca
  - **Action:** AMBER — light-touch review only; do NOT rebuild. Exam-facing exposure is nil. Our 12 free-tier lessons sit in one unit mapped to R067, the written-paper unit, whose teaching content is unchanged in Version 6. The post-build amendment touches only R068/R069 (NEA), which we deliberately excluded at build time. Two small jobs: (1) if we surface any coursework/NEA guidance, refresh it to the June 2026 R068 aim, the updated R068/R069 marking grids, and the tightened AI-misuse/refe
  - Evidence: https://www.ocr.org.uk/qualifications/cambridge-nationals/enterprise-and-marketing-level-1-2-j837/ · https://www.ocr.org.uk/Images/610949-specification-cambridge-nationals-enterprise-and-marketing-j837.pdf · https://www.ocr.org.uk/qualifications/cambridge-nationals/enterprise-and-marketing-level-1-2-j837/specification-at-a-glance/

- `AMBER/free` **Cambridge OCR Level 1/Level 2 Cambridge National in IT** — OCR `J836` (conf high)
  - **What changed:** OCR issued Version 7 in June 2026. We built on 9 May 2026 against Version 6 (September 2025). Version 7 makes MATERIAL teaching-content changes, but ALL of them are in Unit R070 (Using Augmented Reality to Present Information, an NEA unit): Topic Area 3.2 Triggers - "Object recognition and Location based removed from the teaching content"; Topic Area 3.4 Information report - "Animation added to the teaching content"; Topic Area 4.1 Testing - "User testing removed from the teaching content". Vers
  - **Action:** No urgent content fix. Keep the 12 R050 lessons live for the 2027 cohort. The qualification is safe: the Ofqual Register shows "Available to learners", operational start 01/09/2022, and NO operational end date or certification end date. OCR publishes set assignments for the January 2027 and June 2027 series. AMBER is for one narrow reason only: the live spec moved to Version 7 (June 2026) after our 9 May 2026 build. Do two things. (1) Update our stored spec copy specs/ocr/cam
  - Evidence: https://find-a-qualification.services.ofqual.gov.uk/qualifications/60371158 · https://www.ocr.org.uk/qualifications/cambridge-nationals/it-level-1-2-j836/ · https://www.ocr.org.uk/Images/610951-specification-cambridge-nationals-it-j836.pdf

- `AMBER/school` **Drama** — OCR `J316` (conf high)
  - **End date:** 31 August 2028 (Ofqual operational end and certification end). Final first teach September 2026. Final assessment opportunity June/Summer 2028. No resit after that series.
  - **What changed:** Summer 2027 is SAFE. Ofqual shows the qualification as "Available to learners", operational 01 September 2016 to 31 August 2028. OCR withdraws J316 after the June 2028 series, so the 2027 cohort is fully served. Two spec versions came out near or after our 2026-03-02 build. Version 3.1 (March 2026) added withdrawal information to the front cover and section 2a — administrative only. Version 3.2 (April 2026) is AFTER our build and carries MATERIAL content changes: section 2c "Performance texts up
  - **Action:** KEEP and REVIEW — do not retire. Exams run in summer 2027 and again in summer 2028, so the content has two more live cohorts. Do three things. First, diff our Component 04 coverage against the Version 3.2 text list; Blood Brothers is still listed, so our main unit stands, but confirm we cite the Methuen 2001 edition. Second, add the new section 4e guidance on AI use in the non-exam assessment to any NEA or coursework guide pages — this is new spec content we do not yet cover.
  - Evidence: https://find-a-qualification.services.ofqual.gov.uk/qualifications/60189757 · https://www.ocr.org.uk/qualifications/gcse/drama-j316-from-2016/ · https://www.ocr.org.uk/administration/support-and-tools/subject-updates/qual-withdrawals-757190/

- `AMBER/free` **GCSE English Literature** — Eduqas `C720QS` (conf high)
  - **What changed:** MATERIAL change that hits the 2027 cohort, but it was issued BEFORE our build, so we never picked it up. Eduqas replaced the whole Poetry Anthology (Component 1 Section B) for first assessment summer 2027. The new anthology has 15 poems. The old anthology had 18 poems. NO poem appears on both lists. New 15: The Schoolboy (Blake), I Wandered Lonely as a Cloud (Wordsworth), Cousin Kate (Rossetti), Sonnet 29 (E B Browning), Drummer Hodge (Hardy), Disabled (Owen), I Shall Return (McKay), Decompositi
  - **Action:** URGENT rebuild of one unit. The qualification is healthy: no withdrawal, spec structure unchanged, exams run in summer 2027. The risk is our content, not the spec. Our 8 poetry-anthology lessons teach the outgoing 18-poem anthology. They are CORRECT for the summer 2026 exams and WRONG for the summer 2027 cohort. Rebuild those 8 lessons against the new 15 poems before September 2026, when the 2027 cohort starts Year 11. Do this first: (1) download the new anthology PDF at http
  - Evidence: https://www.eduqas.co.uk/qualifications/english-literature-gcse/ · https://www.eduqas.co.uk/media/zd1b4ii5/new-poetry-anthology-for-first-examination.pdf · https://resources.eduqas.co.uk/Pages/ResourceSingle.aspx?rIid=2197

- `AMBER/both` **GCSE History** — AQA `8145` (conf high)
  - **What changed:** No spec amendment. The AQA specification is still Version 1.3 (24 Sep 2019) — the same version that was live when we built on 2026-03-01. AQA's news feed shows no GCSE History items in 2026 (it does carry a GCSE Italian specification-change notice, confirming AQA publishes such notices when they occur). The AMBER is NOT a spec change. It is the scheduled annual rotation of the Paper 2 Section B "historic environment" specified site, which is built into the spec and announced three years ahead (n
  - **Action:** Do NOT treat this as a spec-currency problem — the qualification is safe and the spec is unchanged. Exams are confirmed for summer 2027 (AQA key dates lists 8145 Paper 1 on 20 May 2027 and Paper 2 on 28 May 2027). The required action is a content refresh of the historic environment lessons before the 2027 intake. In each British depth study the site lesson is L13, with the site threaded through earlier lessons, so this is not a one-lesson swap. Rebuild for the 2027 sites: Nor
  - Evidence: https://find-a-qualification.services.ofqual.gov.uk/qualifications/60182179 · https://www.aqa.org.uk/subjects/history/gcse/history-8145/key-dates · https://www.aqa.org.uk/subjects/history/gcse/history-8145/specification

- `AMBER/free` **GCSE Sociology** — WJEC `C200QS` (conf high)
  - **End date:** 31/03/2028 (Wales only — QiW certification end date and regulation end date; last permitted learner start 30/09/2025). No operational or certification end date in England or Northern Ireland.
  - **What changed:** No material content amendment after 2026-05-07. The board document library lists no 2026 specification update, addendum or errata. The subject content taught in 2026-27 is identical to what we built against.
  - **Action:** KEEP SERVING for the 2027 cohort — the content is correct and the exams run. Two things need attention.

1. FIX THE CATALOGUE RECORD. Spec code "3200QS" does not exist. There is no separate WJEC-Wales Sociology GCSE. Both registers show ONE qualification, "WJEC Eduqas Level 1/Level 2 GCSE (9-1) in Sociology", board code C200QS, Ofqual QN 603/1045/5, Wales approval C00/1176/4. Relabel our row to Eduqas/WJEC C200QS. Our free-tier Sociology Eduqas build (33 lessons) already targ
  - Evidence: https://find-a-qualification.services.ofqual.gov.uk/qualifications/60310455 · https://www.qiw.wales/qualifications/C0011764 · https://www.wjec.co.uk/qualifications/sociology-gcse/

## 2. Sunsetting watch — built, fine for 2027 but withdrawing soon (1)

- `GREEN/free` **Level 1/2 Vocational Award in ICT (Technical Award)** — Eduqas (WJEC-CBAC) `5539QA` (conf high)
  - **End date:** Wales only: Summer 2028 is the final full assessment opportunity (Unit 1 resit January 2029). England: no end date. Ofqual register shows no operational end date and no certification end date.
  - **What changed:** No material content amendment after the build date of 2026-06-15. The newest amendment on either board page is the May 2023 re-publication of the Unit 2 SAMs and guidance for teaching, carried into the 12 September 2023 specification. The Eduqas and WJEC qualification pages show no 2026 update or notice. The spec PDF link on the WJEC site is still the 12/09/23 file, so the accredited version has not moved.
  - **Action:** GREEN — keep the built content as is. The Ofqual register lists QN 603/7018/X (WJEC-CBAC) as "Available to learners", operational start 01 September 2022, with no operational end date and no certification end date. Neither the Eduqas nor the WJEC qualification page carries a withdrawal, final-award or last-assessment notice for England. Summer 2027 exams are therefore safe. The specification is unchanged since 12 September 2023, which is before our build date of 2026-06-15, s
  - Evidence: https://www.eduqas.co.uk/qualifications/level-12-vocational-award-in-ict/ · https://www.wjec.co.uk/qualifications/level-12-vocational-award-in-ict/ · https://find-a-qualification.services.ofqual.gov.uk/qualifications/6037018X

## 3. Do NOT build — not-built specs that are withdrawn/superseded (9)

- `WJEC` **GCSE Business (Wales)** `3510QS` — DO NOT BUILD 3510QS. It is withdrawn and has no summer 2027 exam series. Retarget the build to WJEC GCSE Business - Teaching from 2025, entry code 3160QS (Made for Wales), which is first taught from S
- `WJEC` **GCSE Drama (Wales)** `3690QS` — DO NOT BUILD 3690QS. It is withdrawn for the 2027 cohort — no summer 2027 exam series exists for it, only a legacy January 2027 resit window subject to demand. Building it would produce content no 202
- `WJEC` **GCSE English Language (Wales)** `3700QS` — DO NOT BUILD 3700QS. This qualification is withdrawn for the 2027 cohort. A student sitting exams in summer 2027 in Wales cannot be on 3700QS - WJEC banned Year 10 entry from September 2025, so the 20
- `WJEC` **GCSE English Literature (WJEC, Wales)** `3720QS` — DO NOT BUILD 3720QS. It is withdrawn for the 2027 cohort — last full exams are summer 2026, with only a January 2027 resit. A student sitting in summer 2027 cannot take this specification. Building it
- `WJEC` **GCSE Food and Nutrition (Wales)** `3560QS` — DO NOT BUILD 3560QS. The qualification is withdrawn for the 2027 cohort. WJEC states: "Summer 2026 will be the final full assessment opportunity for this qualification. A resit opportunity for examina
- `WJEC` **GCSE French (Wales)** `3800QS` — DO NOT BUILD 3800QS. It is withdrawn for the 2027 cohort: the last full assessment is summer 2026, with only a January 2027 resit series subject to demand. Learners starting Year 10 in September 2025 
- `WJEC` **GCSE Music (Wales)** `3660QS` — DO NOT BUILD 3660QS. The spec is dead for our target cohort. Students who sit exams in summer 2027 are on 3630QS, not 3660QS. A build against 3660QS would be wrong content on day one. Replace the cata
- `WJEC` **GCSE Welsh Language (Cymraeg Iaith Gyntaf)** `3000CS` — DO NOT BUILD 3000CS. It is withdrawn for the 2027 cohort — students starting Year 10 in September 2025 must not be entered for it, and summer 2026 is the last full assessment. Any content built agains
- `WJEC` **GCSE Welsh Literature (Llenyddiaeth Gymraeg)** `3010CS` — DO NOT BUILD 3010CS. This qualification is withdrawn before the 2027 cohort. A student sitting exams in summer 2027 cannot take it — summer 2026 is the last full assessment, and only a January 2027 re

## 4. Build with care — not-built AMBER (build to the current version) (18)

- `AQA` **GCSE Art and Design (Art, craft and design)** `8201` — DO NOT BUILD — but not for spec-currency reasons. The qualification itself is healthy: Ofqual lists QN 601/8088/2 as "Available to learners" with NO operational end date and NO certification end date,
- `AQA` **Art and Design (Fine art)** `8202` — [HARMONISED post-verify: family spec 8201-8206 shares the 2027 Component 1 change; sibling 8201 verify proved it material. Not-built + coursework-excluded, so no action.] BUILD-READINESS: GREEN on spe
- `AQA` **Art and Design (Graphic communication)** `8203` — Not built - this is a build-readiness verdict. The qualification is HEALTHY and locked for summer 2027: Ofqual lists QN 601/8088/2 "AQA Level 1/Level 2 GCSE (9-1) in Art and Design" as "Available to l
- `AQA` **GCSE Art and Design (Textile design)** `8204` — [HARMONISED post-verify: family spec 8201-8206 shares the 2027 Component 1 change; sibling 8201 verify proved it material. Not-built + coursework-excluded, so no action.] BUILD-READINESS: spec is curr
- `AQA` **Art and Design (Three-dimensional design)** `8205` — [HARMONISED post-verify: family spec 8201-8206 shares the 2027 Component 1 change; sibling 8201 verify proved it material. Not-built + coursework-excluded, so no action.] SAFE TO BUILD from a spec-cur
- `AQA` **Art and Design (Photography)** `8206` — DO NOT BUILD - but for product-fit reasons, not spec decay. Two separate findings. (1) Currency: the qualification is healthy and continuing. AQA's key-dates page lists a 31 May 2027 non-exam-assessme
- `Edexcel (Pearson)` **GCSE Computer Science** `1CP1` — Research flagged withdrawal; adversarial verify REFUTED it. Human confirm. DO NOT BUILD against 1CP1 — it is a dead/superseded entry code, not a live 2027 target. Decisive evidence: Pearson's official
- `Eduqas` **Level 1/2 Vocational Award in Global Business Communication (French)** `5879QA` — Research flagged withdrawal; adversarial verify REFUTED it. Human confirm. DO NOT BUILD. The qualification is formally withdrawn. Exams do still run in summer 2027 — it is the final award series — so 
- `Eduqas` **Level 1/2 Vocational Award in Global Business Communication (German)** `5889QA` — Research flagged withdrawal; adversarial verify REFUTED it. Human confirm. DO NOT BUILD. The qualification is withdrawn. The Eduqas page shows this banner verbatim: "This qualification has been withdr
- `Eduqas` **Level 1/2 Vocational Award in Global Business Communication (Spanish)** `5899QA` — Research flagged withdrawal; adversarial verify REFUTED it. Human confirm. DO NOT BUILD. The Eduqas qualification page carries an explicit notice: "This qualification has been withdrawn and will award
- `OCR` **GCSE Classical Greek** `J292` — Classical Greek J292 is safe for the 2027 cohort — exams do run in summer 2027 — but do NOT build the 2016 content version. It reaches its final assessment in summer 2027, so it would serve one exam s
- `WJEC` **GCSE Biology (Wales)** `3400QS` — BUILD-READY, but pick the correct Unit 3 version first. No withdrawal risk: WJEC confirms the separate sciences continue to summer 2031, and the new Double Award does not replace them. The qualificati
- `WJEC` **GCSE History (Wales)** `3100QS` — BUILD-READINESS: do not build 3100QS. Build the replacement 3130QS instead. WJEC states on its own qualification page: "Summer 2027 will be the final full assessment opportunity for this qualification
- `WJEC` **Level 1/2 Vocational Award in Global Business Communication (French)** `5879QA` — Research flagged withdrawal; adversarial verify REFUTED it. Human confirm. DO NOT BUILD. Summer 2027 is the terminal exam series for this qualification, so any content we build would have a single-coh
- `WJEC` **Level 1/2 Vocational Award in Global Business Communication (Spanish)** `5899QA` — BUILD-READINESS: build only if you accept a two-cohort life. Summer 2027 exams are safe. The Ofqual register shows the qualification "Available to learners" with an operational end date of 31 August 2
- `WJEC` **GCSE Media Studies (Wales)** `3680QS` — Research flagged withdrawal; adversarial verify REFUTED it. Human confirm. DO NOT BUILD. Exams do run in summer 2027, but this qualification is already being superseded. Qualifications Wales states pl
- `WJEC` **WJEC GCSE Physical Education (Full Course) — Wales only** `3550QS` — Research flagged withdrawal; adversarial verify REFUTED it. Human confirm. DO NOT BUILD. Build-readiness = RED — the qualification is actively being superseded, and a named replacement already exists.
- `WJEC` **GCSE Physics (Wales)** `3420QS` — SAFE TO BUILD, but build against the UPDATED 3420QS (new Unit 3, teaching from September 2026) — not the 2016 Unit 3. Reason: September 2026 is now, so every new Year 10 in Wales is on the updated ver

## 5. GREEN — current & offered for 2027 (148)

91 built (no action) · 46 not-built (build-ready).

<details><summary>Full GREEN list</summary>

- `None` BTEC Level 1/Level 2 Tech Award in Health and Social Care (2022) — Pearson Edexcel (BTEC) `BTEC Tech Award (2022 suite); publication code VQ000054`
- `None` Cambridge OCR Level 1/Level 2 Cambridge National in Sport Science (J828) — OCR `J828 (R180 = externally assessed exam unit)`
- `None` GCSE Latin — Eduqas `C990QS (our catalogue records C580QS — see action)`
- `None` GCSE Physical Education — Eduqas `C550QS (full course); C555QT (short course)`
- `None` Latin — WJEC `C990QS`
- `None` Level 1/2 Vocational Award in Construction and the Built Environment (Technical Award) — Eduqas (WJEC-CBAC) `E819QA (accredited Eduqas qual code; 5229QA held in our catalogue is the Eduqas ENTRY code for the same qualification)`
- `None` Level 1/2 Vocational Award in Performing Arts (Technical Award) — Eduqas (WJEC) `5639QA`
- `None` Level 1/2 Vocational Award in Retail Business (Technical Award) — Eduqas `5789QA`
- `None` Music — Eduqas `C660QS (component prefix C660U — C660U10-1 Performing, C660U20-1 Composing, C660U30-1 Appraising)`
- `None` WJEC Eduqas Level 1/Level 2 GCSE (9-1) in Art and Design — Eduqas `C650QS (family C650QS-C656QS: Art Craft and Design, Fine Art, Critical and Contextual Studies, Textile Design, Graphic Communication, Three-Dimensional Design, Photography)`
- `None` WJEC Eduqas Level 1/Level 2 GCSE (9-1) in Film Studies — WJEC `C670QS (our catalogue label "WJEC 3670QS" is wrong — see action)`
- `both` Cambridge Nationals: Creative iMedia — OCR `J834`
- `both` Food Preparation and Nutrition — AQA `8585`
- `both` GCSE (9-1) Business — Edexcel `1BS0`
- `both` GCSE (9-1) Computer Science — OCR `J277`
- `both` GCSE Biology — AQA `8461`
- `both` GCSE Chemistry — AQA `8462`
- `both` GCSE Combined Science: Trilogy — AQA `8464`
- `both` GCSE Design and Technology — AQA `8552`
- `both` GCSE English Language — AQA `8700`
- `both` GCSE English Literature — AQA `8702`
- `both` GCSE French — AQA `8652`
- `both` GCSE Geography — AQA `8035`
- `both` GCSE Physics — AQA `8463`
- `both` GCSE Religious Studies A — AQA `8062`
- `both` GCSE Spanish (AQA Level 1/Level 2 GCSE (9-1) in Spanish) — AQA `8692`
- `both` German — AQA `8662`
- `free` Cambridge National Level 1/Level 2 in Health and Social Care — OCR `J835`
- `free` Cambridge National Level 1/Level 2 in Sport Science — OCR (Cambridge OCR) `J828`
- `free` Cambridge Nationals Level 1/Level 2 in Engineering Design — OCR (Cambridge OCR) `J822`
- `free` Cambridge Nationals: Child Development (Level 1/Level 2) — OCR `J809`
- `free` Cambridge Nationals: Engineering Manufacture (Level 1/Level 2) — OCR `J823`
- `free` Cambridge OCR Level 1/Level 2 Cambridge National in Engineering Programmable Systems — OCR `J824`
- `free` Cambridge OCR Level 1/Level 2 Cambridge National in Sport Studies — OCR `J829`
- `free` Cambridge OCR Level 1/Level 2 GCSE (9-1) in Business — OCR `J204`
- `free` Cambridge OCR Level 1/Level 2 GCSE (9-1) in Mathematics — OCR `J560`
- `free` Cambridge OCR Level 1/Level 2 GCSE (9-1) in Religious Studies (Full Course) — OCR `J625`
- `free` Classical Civilisation — OCR `J199`
- `free` Combined Science — Edexcel `1SC0`
- `free` Design and Technology — Eduqas `C600QS`
- `free` English Literature — OCR `J352`
- `free` GCSE (9-1) Astronomy — Edexcel (Pearson) `1AS0`
- `free` GCSE (9-1) Biology — Edexcel `1BI0`
- `free` GCSE (9-1) Biology B (Twenty First Century Science) — OCR `J257`
- `free` GCSE (9-1) Chemistry — Edexcel (Pearson) `1CH0`
- `free` GCSE (9-1) Chemistry A (Gateway Science) — OCR `J248`
- `free` GCSE (9-1) Chemistry B (Twenty First Century Science) — OCR `J258`
- `free` GCSE (9-1) Combined Science A (Gateway Science) — OCR (now branded Cambridge OCR) `J250`
- `free` GCSE (9-1) Combined Science B (Twenty First Century Science) — OCR `J260`
- `free` GCSE (9-1) English Language — OCR `J351`
- `free` GCSE (9-1) English Literature — Edexcel `1ET0`
- `free` GCSE (9-1) Geography A — Edexcel `1GA0`
- `free` GCSE (9-1) Geography A (Geographical Themes) — OCR `J383`
- `free` GCSE (9-1) Geography B — Edexcel (Pearson) `1GB0`
- `free` GCSE (9-1) History A (Explaining the Modern World) — OCR `J410`
- `free` GCSE (9-1) Physical Education — Edexcel `1PE0`
- `free` GCSE (9-1) Physical Education — OCR `J587`
- `free` GCSE (9-1) Physics — Edexcel `1PH0`
- `free` GCSE (9-1) Physics B (Twenty First Century Science) — OCR `J259`
- `free` GCSE (9-1) Psychology — Edexcel `1PS0`
- `free` GCSE (9-1) Psychology — OCR `J203`
- `free` GCSE (9-1) Religious Studies A — Edexcel `1RA0`
- `free` GCSE Biology A (Gateway Science) — OCR `J247`
- `free` GCSE Business — AQA `8132`
- `free` GCSE Citizenship Studies — AQA `8100`
- `free` GCSE Computer Science — AQA `8525`
- `free` GCSE Computer Science — Edexcel (Pearson) `1CP2`
- `free` GCSE Drama — AQA `8261`
- `free` GCSE Economics — AQA `8136`
- `free` GCSE Engineering — AQA `8852`
- `free` GCSE English Language — Edexcel (Pearson) `1EN0`
- `free` GCSE English Language — Eduqas `C700QS`
- `free` GCSE Food Preparation and Nutrition — Eduqas `C560QS`
- `free` GCSE French (2024) — Edexcel (Pearson) `1FR1`
- `free` GCSE History — Eduqas `C100QS`
- `free` GCSE Mathematics — AQA `8300`
- `free` GCSE Media Studies — AQA `8572`
- `free` GCSE Physical Education — AQA `8582`
- `free` GCSE Religious Studies (Route A / Route B) — Eduqas `C120QS`
- `free` GCSE Religious Studies (Short Course) — AQA `8061`
- `free` GCSE Sociology — AQA `8192`
- `free` GCSE Sociology — Eduqas `C200QS`
- `free` GCSE Statistics — AQA `8382`
- `free` German — Edexcel `1GN1`
- `free` Level 1/2 Vocational Award in Engineering (Technical Award) — Eduqas `5239QA`
- `free` Level 1/2 Vocational Award in Health and Social Care (Technical Award) — Eduqas `5249QA`
- `free` Level 1/2 Vocational Award in Hospitality and Catering (Technical Award) — Eduqas `5409QA`
- `free` Level 1/2 Vocational Award in ICT (Technical Award) — Eduqas (WJEC-CBAC) `5539QA`
- `free` Level 1/2 Vocational Award in Sport and Coaching Principles (Technical Award) — Eduqas `5259QA`
- `free` Mathematics — Edexcel `1MA1`
- `free` Music Technology — NCFE `603/7008/7`
- `free` Pearson Edexcel Level 1/Level 2 GCSE (9-1) in History — Edexcel `1HI0`
- `free` Physics A (Gateway Science) — OCR `J249`
- `free` Psychology — AQA `8182`
- `free` Spanish — Edexcel `1SP1`
- `free` WJEC Eduqas Level 1/Level 2 GCSE (9-1) in Computer Science — Eduqas `C500QS`
- `free` WJEC Eduqas Level 1/Level 2 GCSE (9-1) in Electronics — Eduqas `C490QS`
- `free` WJEC Eduqas Level 1/Level 2 GCSE (9-1) in Electronics — WJEC (WJEC CBAC Ltd — published as "WJEC Eduqas") `C490QS`
- `free` WJEC Eduqas Level 1/Level 2 GCSE (9-1) in Film Studies — Eduqas `C670QS`
- `free` WJEC Eduqas Level 1/Level 2 GCSE (9-1) in Geography A — Eduqas `C111QS`
- `free` WJEC Eduqas Level 1/Level 2 GCSE (9-1) in Mathematics — Eduqas `C300QS`
- `free` WJEC Level 1/2 Vocational Award in Hospitality and Catering (Technical Award) — WJEC `5409QA`
- `not-built` Ancient History — OCR `J198`
- `not-built` Art and Design (Art, Craft and Design) — Edexcel `1AD0`
- `not-built` Bengali — AQA `8638`
- `not-built` Cambridge OCR Level 1/Level 2 GCSE (9-1) in Citizenship Studies — OCR `J270`
- `not-built` Cambridge OCR Level 1/Level 2 GCSE (9-1) in Economics — OCR `J205`
- `not-built` Cambridge OCR Level 1/Level 2 GCSE (9-1) in Food Preparation and Nutrition — OCR `J309`
- `not-built` Cambridge OCR Level 1/Level 2 GCSE (9-1) in Religious Studies (Short Course) — OCR `J125`
- `not-built` Chinese (spoken Mandarin/spoken Cantonese) — Edexcel `1CN0`
- `not-built` Combined Science: Synergy — AQA `8465`
- `not-built` Dance — AQA `8236`
- `not-built` Design and Technology — OCR `J310`
- `not-built` GCSE (9-1) Biblical Hebrew — Edexcel `1BH0`
- `not-built` GCSE (9-1) Design and Technology — Edexcel `1DT0`
- `not-built` GCSE (9-1) Greek — Edexcel `1GK0`
- `not-built` GCSE (9-1) Gujarati — Edexcel `1GU0`
- `not-built` GCSE (9-1) History B (Schools History Project) — OCR `J411`
- `not-built` GCSE (9-1) Italian — Edexcel (Pearson) `1IN0`
- `not-built` GCSE (9-1) Japanese — Edexcel (Pearson) `1JA0`
- `not-built` GCSE (9-1) Media Studies — Eduqas `C680QS`
- `not-built` GCSE (9-1) Media Studies — OCR `J200`
- `not-built` GCSE (9-1) Portuguese — Edexcel (Pearson) `1PG0`
- `not-built` GCSE Arabic — Edexcel (Pearson) `1AA0`
- `not-built` GCSE Chemistry (Wales) — WJEC `3410QS`
- `not-built` GCSE Chinese (Spoken Mandarin) — AQA `8673`
- `not-built` GCSE Drama — Edexcel `1DR0`
- `not-built` GCSE Drama — Eduqas `C690QS`
- `not-built` GCSE Geography B — Eduqas `C112QS`
- `not-built` GCSE Geography B (Geography for Enquiring Minds) — OCR `J384`
- `not-built` GCSE Hebrew (Modern) — AQA `8678`
- `not-built` GCSE Italian — AQA `8633`
- `not-built` GCSE Music — AQA `8271`
- `not-built` GCSE Music — Edexcel `1MU0`
- `not-built` GCSE Music — Eduqas `C660QS`
- `not-built` GCSE Religious Studies B — AQA `8063`
- `not-built` GCSE Russian — Edexcel `1RU0`
- `not-built` GCSE Turkish — Edexcel `1TU0`
- `not-built` GCSE Urdu — AQA `8648`
- `not-built` GCSE Urdu — Edexcel `1UR0`
- `not-built` Latin — OCR `J282`
- `not-built` Music — OCR `J536`
- `not-built` Panjabi — AQA `8683`
- `not-built` Pearson Edexcel Level 1/Level 2 GCSE (9-1) in Citizenship Studies — Edexcel `1CS0`
- `not-built` Pearson Edexcel Level 1/Level 2 GCSE (9-1) in Statistics — Edexcel (Pearson) `1ST0`
- `not-built` Persian — Edexcel `1PN0`
- `not-built` Polish — AQA `8688`
- `not-built` WJEC Eduqas Level 1/Level 2 GCSE (9-1) in Business — Eduqas `C510QS`

</details>
