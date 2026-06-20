# Spec-Currency Audit — 2027 Cohort (all subjects, all boards)

**Run:** 2026-06-20 · **Scope:** 194 qualifications = every catalogued spec (specs/index.json, all boards) unioned with everything we ship. Build status: {'not-built': 87, 'both': 17, 'free': 87, 'school': 3}.

**Result:** 161 GREEN · 18 AMBER · 15 RED.

Method: per-qualification research agent (Ofqual register operational/cert end dates + board amendment pages), every RED/withdrawal adversarially re-verified. For built specs RED/AMBER = act now; for not-built specs the verdict is a BUILD-READINESS signal (RED = do not build / superseded). Re-run: `_gen_spec_audit_worklist.py --scope full` → workflow `spec-currency-audit-2027` → this script.

> **Systemic note — Wales reform.** WJEC `3xxxQS`/`3xxxCS` legacy GCSEs (Curriculum for Wales / "Made-for-Wales") are being withdrawn: final full assessment Summer 2026, Jan-2027 resit only, no Summer 2027 series. Our "Eduqas / WJEC" aliased subjects are fine for **England (Eduqas, Cxxx)** but the **Wales (WJEC, 3xxx)** arm is dead for 2027 — relevant only if we serve Welsh students.

## 1. Built content needing action (9)

Subjects we ship that are RED or AMBER — real 2027-cohort exposure.

- `RED/free` **GCSE Computer Science (WJEC, Wales)** — WJEC `3500QS` (conf high)
  - **End date:** Summer 2026 = final full assessment; January 2027 = final resit only (subject to demand). No full summer 2027 exam series.
  - **What changed:** Legacy WJEC GCSE Computer Science 3500QS (Wales) is being withdrawn. WJEC's qualification page states summer 2026 is the final full assessment opportunity, with a January 2027 resit only (subject to demand). From Sept 2025, learners must not be entered in Year 10 and must instead take the replacement GCSE Computer Science 3460QS (teaching from 2025, for award from 2027), part of the Qualifications Wales National 14-16 reform.
  - **Action:** RED — DO NOT serve/maintain this for a 2027 cohort. The WJEC 3500QS legacy spec has no full summer 2027 exam series (final full assessment summer 2026; Jan 2027 resit only). A 2027 teaching/exam cohort must be on the replacement spec WJEC GCSE Computer Science 3460QS ("Made for Wales", teaching from 2025, first award 2027). Recommendation: retire/redirect our 3500QS-aligned content and rebuild against 3460QS if WJEC-Wales Computer Science coverage is wanted. Note our live cat
  - Evidence: https://www.wjec.co.uk/qualifications/computer-science-gcse/ · https://www.wjec.co.uk/qualifications/gcse-computer-science-teaching-from-2025/ · https://www.wjec.co.uk/media/13im5was/wjec-gcse-computer-science-specification-e.pdf

- `RED/free` **GCSE Religious Studies (WJEC, full course, teaching from 2017)** — WJEC `3120QS` (conf high)
  - **End date:** Final full assessment: Summer 2026. Resit-only opportunity: January 2027 (subject to demand). No summer 2027 series.
  - **What changed:** 3120QS is being withdrawn and replaced by WJEC's new "Made for Wales" GCSE Religious Studies (3150QS, teaching from September 2025). Final full assessment of 3120QS is Summer 2026, with a January 2027 resit only (subject to demand). From September 2025, learners cannot be entered onto 3120QS in Year 10 and must take 3150QS instead.
  - **Action:** RED — DO NOT continue relying on this content for the 2027 cohort. WJEC GCSE Religious Studies 3120QS (teaching from 2017) is being withdrawn: Summer 2026 is the final full assessment and there is NO summer 2027 series, only a conditional January 2027 resit for legacy candidates. Any student starting now sits the new "Made for Wales" spec 3150QS (teaching from September 2025). Our 2026-05-08 content is built to the retired 3120QS spec and must be REBUILT to the new 3150QS spe
  - Evidence: https://www.wjec.co.uk/qualifications/religious-studies-gcse/ · https://www.wjec.co.uk/qualifications/gcse-religious-studies-teaching-from-2025/ · https://www.wjec.co.uk/media/iiobkkix/wjec-gcse-religious-studies-specification-e.pdf

- `AMBER/free` **Cambridge Nationals: Enterprise and Marketing** — OCR `J837` (conf high)
  - **What changed:** Spec moved to Version 6 (June 2026), issued after our 2026-05-21 build. Material content change is confined to the two NEA/coursework units: the aim of unit R068 was updated to reflect a change to the set-assignment tasks, and the R068/R069 marking-criteria grids were amended to make grading more explicit. Also a non-content rebrand (OCR -> "Cambridge OCR", with an "About our new name" statement, effective Sept 2025) and admin changes (Appendix A file-formats table; URS + set-assignment feedback
  - **Action:** Light-touch review only; do not rebuild. Our 12 lessons map to the unchanged R067 exam unit, so exam-facing content is unaffected. Recommended: (1) refresh any coursework/NEA (R068/R069) guidance/wording to match the June 2026 marking-criteria and set-assignment-task changes if we surface any; (2) swap "OCR" -> "Cambridge OCR" naming where shown. Availability is solid: OCR confirms Jan/June 2027 assessment series; DfE funding approved to 31/07/2027; QN 603/7093/2 shows no ope
  - Evidence: https://www.ocr.org.uk/qualifications/cambridge-nationals/enterprise-and-marketing-level-1-2-j837/ · https://www.ocr.org.uk/Images/610949-specification-cambridge-nationals-enterprise-and-marketing-j837.pdf · https://www.qualifications.education.gov.uk/Qualification/60370932

- `AMBER/free` **GCSE (9-1) Sociology** — WJEC / Eduqas `3200QS (WJEC, Wales) / C200QS (Eduqas, England)` (conf high)
  - **End date:** Summer 2027 (last exams in Wales under WJEC 3200QS); Year 10 starters Sept 2025 are the final Wales cohort. England/Eduqas C200QS continues beyond 2027 with no withdrawal notice.
  - **What changed:** No material content amendment since the 2026-05-07 build. The accredited spec is locked: Version 2 (January 2019), teaching from 2017. The only documented amendment is admin-only (clarification of resit rules in the 'Making entries' section), which predates our build. Spec content is unchanged.
  - **Action:** SAFE FOR 2027 COHORT, but flag as final year under the WJEC (Wales) 3200QS code. Summer 2027 IS offered: Eduqas/WJEC have published a Summer 2027 examination timetable that includes Sociology (C200, two 1h45 components), and Qualifications Wales confirms Year 10 starters in Sept 2025 (who sit exams summer 2027) are the LAST cohort able to take GCSE Sociology in Wales. It is being withdrawn in Wales under the 'Qualified for the Future' reform and replaced by the new GCSE Socia
  - Evidence: https://www.wjec.co.uk/qualifications/sociology-gcse/ · https://www.eduqas.co.uk/qualifications/sociology-gcse/ · https://qualifications.wales/regulation-reform/reforming/qualified-for-the-future/made-for-wales-gcses/

- `AMBER/free` **GCSE Computer Science** — AQA `8525` (conf high)
  - **What changed:** AQA reformed 8525 in line with DfE subject-content changes: same spec code, updated v1.3 (16 Jun 2025) reduces content for the 2027 cohort. Per the official "Summary of changes" (v1.0, June 2025): 3.4.5 Systems architecture — REMOVED Von Neumann architecture references and optical secondary storage. 3.5 Networks — REMOVED LAN topologies (star/bus), removed the requirement to know the use of common network protocols, removed Ethernet, Wi-Fi, UDP and FTP, removed alternative link-layer names; rewo
  - **Action:** Review which 8525 edition our content (built 2026-05-09, 23 lessons) targets. Verify the Computer Systems and Computational Thinking units against v1.3: if they still teach Von Neumann architecture, optical secondary storage, LAN star/bus topologies, or the protocols Ethernet/Wi-Fi/UDP/FTP as required exam content, demote that to optional/context (it is removed from the 2027 Paper 2) and reframe TCP/UDP transport-layer wording (UDP dropped). No withdrawal risk — qualification
  - Evidence: https://www.aqa.org.uk/gcse-computer-science-specification-changes-for-summer-2027 · https://www.aqa.org.uk/files/e5e3609b-98ee-4a88-b4ff-da9dc40904cd/faf3ab172b76f13781ac8dbe12783c16915663e0.pdf · https://www.aqa.org.uk/subjects/computer-science/gcse/computer-science-8525/specification/scheme-of-assessment

- `AMBER/both` **GCSE English Language** — AQA `8700` (conf high)
  - **What changed:** AQA issued a material assessment amendment to GCSE English Language 8700, first assessed summer 2026 (so it applies to the 2027 cohort). The spec PDF was republished 20 Mar 2026, AFTER our 12 Mar 2026 build. Paper 1: Q1 now multiple-choice (circle-shading), Q3 now targets a single structural effect (not broad structural analysis), Q4 reworded (drops the "student" framing, students may agree and/or disagree, specifies which extract portion applies), Q5 narrative option now asks for a story "openi
  - **Action:** Review our AQA English Language practice content against the summer-2026 assessment changes (spec republished 20 Mar 2026, after our 12 Mar build). Priority: Paper 1 Q1 (now multiple-choice), Q3 (single structural effect), and Q5 narrative-"opening" task; plus minor Paper 2 Q2/Q4 rewording. Marks, structure and AOs are unchanged, so the bulk of content holds, but question-type authenticity in practice items needs updating for the 2027 cohort. Qualification is confirmed still 
  - Evidence: https://www.aqa.org.uk/english-language-changes · https://www.aqa.org.uk/subjects/english/gcse/english-8700/specification · https://www.aqa.org.uk/subjects/english/gcse/english-8700/key-dates

- `AMBER/free` **GCSE English Literature** — Eduqas (WJEC) `C720QS (C720)` (conf high)
  - **What changed:** Eduqas has replaced the GCSE English Literature Poetry Anthology for the 2027 cohort. The OLD anthology (18 poems) was examined for the last time in Summer 2026; the NEW anthology (15 poems — 3 fewer, with more poems by women and broader global voices) is taught from September 2025 and FIRST examined in Summer 2027. Same spec code (C720) and QN (601/5246/1) — the qualification is NOT withdrawn, only the Component 1 poetry-from-1789 anthology content has changed. Our content was built 2026-03-24,
  - **Action:** Review and rebuild the Component 1 poetry anthology lessons against the NEW Eduqas 15-poem anthology (first examination Summer 2027). Download the new anthology PDF (eduqas.co.uk/media/zd1b4ii5/new-poetry-anthology-for-first-examination.pdf) and Eduqas free Digital Resources (Blended Learning + Knowledge Organiser for all 15 poems). Re-plan the anthology unit: replace dropped poems, add the new ones, and re-narrate affected lessons. Non-poetry components (Shakespeare, A Chris
  - Evidence: https://www.eduqas.co.uk/qualifications/english-literature-gcse/ · https://www.eduqas.co.uk/home/english-with-eduqas/eduqas-gcse-english-literature-poetry-anthology-2025/ · https://www.eduqas.co.uk/media/zd1b4ii5/new-poetry-anthology-for-first-examination.pdf

- `AMBER/free` **GCSE Food Preparation and Nutrition** — Eduqas `C560QS` (conf high)
  - **End date:** 2027-07-31 (funding/review end on DfE-Ofqual register; final exam series Summer 2027, provisional exam 24 May 2027)
  - **What changed:** No material content amendment to the specification since our 2026-05-05 build. The only post-build communication is the April 2026 Eduqas newsletter, which carries administrative/clarification changes only: NEA initial sample-size increase from summer 2026, AI-declaration coversheet reminders, new 2025 exemplars, and exam-timetable dates. No teaching-content change, so the live C560 spec content matches what we built.
  - **Action:** KEEP for summer 2027, but FLAG as terminal. This is a withdrawing qualification in active teach-out: it is being replaced by the new WJEC/Eduqas GCSE Food and Nutrition (first teaching Sept 2025, first exams 2027). From Sept 2025 learners must NOT be entered onto C560 in Year 10. Exams ARE still available for summer 2027 (DfE register funds it to 31/07/2027; April 2026 Eduqas newsletter timetables a provisional 24 May 2027 exam), so it is NOT RED — students already on-course 
  - Evidence: https://www.eduqas.co.uk/media/nmvi002b/eduqas-gcse-food-preparation-nutrition-newsletter-april-2026.pdf · https://www.qualifications.education.gov.uk/Qualification/60180936 · https://www.eduqas.co.uk/qualifications/food-preparation-and-nutrition-gcse/

- `AMBER/free` **GCSE Spanish** — Eduqas `C820QS` (conf medium)
  - **What changed:** No post-build amendment is the issue. The issue is a pre-build spec mismatch: the reformed Eduqas GCSE MFL specs (French/German/Spanish) have first teaching Sept 2024 and first exams Summer 2026, and are the live qualification for the 2027 cohort. Our repo file specs/eduqas/spanish-C820QS.md, although tagged spec_code C820QS, contains the OLD 'Teaching from 2016 / award from 2018 / Version 3b August 2023' specification text — i.e. the legacy spec whose final Eduqas assessment was Summer 2026. Ou
  - **Action:** REVIEW/REBUILD against the reformed Eduqas GCSE Spanish spec. Still offered for summer 2027 (not RED), so do not withdraw. But verify our content was built from the reformed Eduqas spec, not the legacy 2016 one — current evidence (specs/eduqas/spanish-C820QS.md holding 'Teaching from 2016, Version 3b Aug 2023' text) indicates it was built from the legacy spec. Action: (1) obtain the reformed Eduqas C820QS spec PDF + sample assessment materials and replace the legacy file; (2)
  - Evidence: https://www.eduqas.co.uk/articles/bringing-languages-to-life-reformed-gcses-in-french-german-and-spanish/ · https://www.eduqas.co.uk/home/modern-foreign-language-gcses-for-2024/ · https://www.qualifications.education.gov.uk/Qualification/60189010

## 2. Sunsetting watch — built, fine for 2027 but withdrawing soon (4)

- `GREEN/free` **Level 1/2 Vocational Award in ICT (Technical Award)** — Eduqas (WJEC) `5539QA` (conf high)
  - **End date:** Wales: Summer 2028 final full assessment (Unit 1 resit Jan 2029). England: no confirmed end date.
  - **What changed:** No material content amendment found after the build date (2026-06-15). Current accredited spec is Version 3 (12 Sep 2023); Unit 2 SAMs and guidance for teaching re-published May 2023. All amendment activity predates the build.
  - **Action:** BUILD-READINESS: GREEN — current, accredited, funded and examined for the 2027 cohort in both England and Wales, so worth building. Caveat for planning (not a blocker): a withdrawal horizon exists beyond 2027 — Wales has a confirmed final full assessment in Summer 2028 (Unit 1 resit Jan 2029) and England has no confirmed end date amid the wider DfE Level 2 / V-Level reform; the England DfE funding approval end date is 31/07/2027 (a funding window subject to routine extension,
  - Evidence: https://www.eduqas.co.uk/qualifications/level-12-vocational-award-in-ict/ · https://www.wjec.co.uk/qualifications/level-12-vocational-award-in-ict/ · https://www.wjec.co.uk/media/pvbotmta/wjec_l1-2-vocaward-ict_spec-e-120923.pdf

- `GREEN/free` **OCR GCSE Chemistry B (Twenty First Century Science)** — OCR `J258` (conf high)
  - **End date:** 2027-07-31 (operational end date; summer 2027 is the FINAL exam series — suite withdrawn thereafter)
  - **What changed:** No material content amendment found issued after the 2026-05-09 build date. GCSE specs are locked mid-course; the accredited J258 spec (601/8605/7) is unchanged. OCR's J258 specification and SaveMyExams spec pages show no 2026 amendment or withdrawal notice in their content.
  - **Action:** GREEN for the 2027 cohort: J258 is still Available on the Ofqual register and the summer 2027 (May/June 2027) exam series falls inside the operational window, so students sitting in 2027 are covered and our content (built 2026-05-09) remains fit. IMPORTANT caveat: the operational end date is 31/07/2027 across the entire Twenty First Century Science B suite (J257/J258/J259/J260), meaning summer 2027 is the LAST assessment series and the suite is being retired — do NOT carry th
  - Evidence: https://www.qualifications.education.gov.uk/Qualification/60186057 · https://www.qualifications.education.gov.uk/Qualification/60186902 · https://www.ocr.org.uk/qualifications/gcse/twenty-first-century-science-suite-chemistry-b-j258-from-2016/

- `GREEN/school` **GCSE (9-1) Drama** — OCR `J316` (conf high)
  - **End date:** 2028-08-31
  - **What changed:** Two set-text notices were issued after our 2026-03-02 build, but neither affects the summer 2027 cohort. (1) "Two new set texts" (Blue Remembered Hills, Noughts & Crosses) applied ONLY to first-teach Sept 2026 / first-assessment June 2028 — explicitly not students assessed in 2027. (2) "Set texts to remain unchanged" (13 Apr 2026) then reversed that plan for the final cohort, keeping Misterman and Gizmo until withdrawal. The Component 04 set-text list for the 2027 cohort (incl. Misterman + Gizmo
  - **Action:** No action needed for the 2027 cohort — content is current and fit. FORWARD FLAG ONLY: OCR (Cambridge OCR) is withdrawing GCSE Drama J316. Final first teach Sept 2026; final assessment opportunity June 2028 (no resits after); Ofqual operational + certification end date 31 Aug 2028. Plan a content sunset for J316 after the June 2028 series; Eduqas Drama is the likely migration board for future cohorts. Do NOT treat the withdrawal as a 2027 risk.
  - Evidence: https://www.ocr.org.uk/qualifications/gcse/drama-j316-from-2016/ · https://www.ocr.org.uk/administration/support-and-tools/subject-updates/qual-withdrawals-757190/ · https://www.ocr.org.uk/administration/support-and-tools/subject-updates/gcse-drama-texts-update-757683/

- `GREEN/free` **GCSE Design and Technology** — WJEC `3600QS` (conf high)
  - **End date:** Summer 2027 = final full assessment; January 2028 = final resit (subject to demand). No new Year 10 entries from Sept 2026.
  - **What changed:** No amendment since our 2026-05-19 build. The current accredited spec is Version 2 (January 2019); its only ever amendment (v2) clarified resit rules and predates the build by years. The spec is locked for the 2027 cohort.
  - **Action:** KEEP — GREEN for the 2027 cohort. WJEC confirms verbatim: "Summer 2027 will be the final full assessment opportunity for this qualification. A resit opportunity for examinations will be available in January 2028, subject to demand." The 2027 cohort is the LAST to sit this spec but the exam IS available, and the spec is unchanged since build (v2, Jan 2019). Per audit rules a reform for a later cohort is not a RED. IMPORTANT SUNSET CAVEAT (not a status trigger): this is being w
  - Evidence: https://www.wjec.co.uk/qualifications/design-and-technology-gcse/ · https://www.wjec.co.uk/qualifications/gcse-design-and-technology-teaching-from-2026/ · https://www.wjec.co.uk/media/qhamvsua/wjec-gcse-d-t-spec-from-2017-e.pdf

## 3. Do NOT build — not-built specs that are withdrawn/superseded (13)

- `Edexcel (Pearson)` **GCSE Computer Science (2016)** `1CP1` — DO NOT BUILD against 1CP1 — it is a dead/superseded code (last exams 2021). The correct current target for the Edexcel GCSE Computer Science 2027 cohort is the 2020 spec, code 1CP2 (GREEN, current, on
- `WJEC` **GCSE Art and Design (Art, Craft & Design)** `3650QS` — DO NOT BUILD against 3650QS. This is the LEGACY WJEC GCSE Art and Design "Art, Craft & Design" spec (teaching from 2016, Wales-only, Qualifications Wales-regulated). Its final full assessment was Summ
- `WJEC` **GCSE Business (WJEC, approved by Qualifications Wales)** `3510QS` — DO NOT BUILD against 3510QS. This is the withdrawn 2017 WJEC GCSE Business spec (Qualifications Wales). Per the official WJEC qualification page: summer 2026 is the final full assessment, with only a 
- `WJEC` **GCSE Drama** `3690QS` — DO NOT BUILD 3690QS. This is a Wales-specific reform: the WJEC GCSE Drama 3690QS (teaching from 2016) is being withdrawn — last full assessment summer 2026, with only a demand-dependent January 2027 r
- `WJEC` **GCSE English Language (Wales)** `3700QS` — DO NOT BUILD 3700QS. This Wales-only GCSE English Language spec is being superseded by the new WJEC GCSE English Language and Literature (Double and Single Award), teaching from Sept 2025. From Sept 2
- `WJEC` **GCSE English Literature (Wales)** `3720QS` — DO NOT BUILD. WJEC GCSE English Literature 3720QS is a Wales-only qualification being withdrawn under the Curriculum for Wales / 'Made for Wales' reform. WJEC's official page states summer 2026 is the
- `WJEC` **GCSE Food and Nutrition** `3560QS` — DO NOT BUILD against 3560QS. This legacy WJEC GCSE Food and Nutrition (QN 601/8085/7, Qualifications Wales-regulated) is being withdrawn: last full assessment was summer 2026, with only a demand-depen
- `WJEC` **GCSE French (legacy, teaching from 2016)** `3800QS` — DO NOT BUILD against 3800QS. This legacy spec is withdrawn for the 2027 cohort: WJEC's official qualification page states "Summer 2026 will be the final full assessment opportunity for this qualificat
- `WJEC` **GCSE Mathematics / Mathematics – Numeracy (WJEC, Wales)** `3300QS / 3310QS` — DO NOT BUILD the legacy 3300QS/3310QS. These Welsh GCSEs (regulated by Qualifications Wales, not Ofqual) have their final full assessment in Summer 2026 and are being superseded from Sept 2025 by the 
- `WJEC` **GCSE Music (WJEC, legacy spec from 2016)** `3660QS` — DO NOT BUILD against 3660QS. This entry code is the LEGACY WJEC GCSE Music spec (from 2016, QN 601/8290/8): final full assessment Summer 2026, January 2027 resit only (subject to demand), and learners
- `WJEC` **GCSE Welsh Language** `3000CS` — DO NOT BUILD. This qualification is being withdrawn under the Curriculum for Wales / Made-for-Wales reform. From Sept 2025 learners must not be entered in Year 10; they sit the new GCSE Iaith a Llenyd
- `WJEC` **GCSE Welsh Literature** `3010CS` — DO NOT BUILD. WJEC GCSE Welsh Literature (3010CS) is being withdrawn under Curriculum for Wales reform. Summer 2026 was the final full assessment; the only 2027 availability is a January 2027 RESIT ON
- `WJEC` **GCSE Welsh Second Language** `3020CS` — DO NOT BUILD. WJEC GCSE Welsh Second Language (3020 family; Qualifications Wales / Ofqual ref C00/1166/2) is being withdrawn. WJEC's official page states "Summer 2026 will be the final full assessment

## 4. Build with care — not-built AMBER (build to the current version) (11)

- `AQA` **GCSE Art and Design (Art, craft and design)** `8201` — BUILD-READINESS: Cleared to build — qualification is current and offered for summer 2027 (June 2027 NEA deadlines and 2027 exam timetable both confirm it; QN 601/8088/2; not withdrawn). AMBER flag is 
- `Eduqas` **Level 1/2 Vocational Award in Global Business Communication (French)** `5879QA` — BUILD-READINESS NOTE: This qualification is WITHDRAWN with its final-ever exam sitting in Summer 2027 (Eduqas notice verbatim: "This qualification has been withdrawn and will award for the final time 
- `Eduqas` **Level 1/2 Vocational Award in Global Business Communication (German)** `5889QA` — Research flagged withdrawal; adversarial verify REFUTED it. Human confirm. DO NOT BUILD. This qualification is WITHDRAWN and awards for the final time in Summer 2027 (confirmed on the official Eduqas 
- `Eduqas (WJEC-CBAC)` **Level 1/2 Vocational Award in Global Business Communication (Spanish)** `5899QA` — Research flagged withdrawal; adversarial verify REFUTED it. Human confirm. DO NOT BUILD. The qualification has been formally WITHDRAWN by Eduqas: the Eduqas page states it "has been withdrawn and will
- `Eduqas` **GCSE Physical Education** `C550QS` — BUILD-READINESS: AMBER — do NOT build a fresh full content suite. Although C550QS IS still offered for summer 2027 (the 2027 cohort started Year 10 in Sept 2025 and is unaffected by the Sept-2026 Year
- `WJEC` **German** `3850QS (new, teaching from 2025) / 3820QS (legacy 2016, resit-only Jan 2027). NOTE: the supplied code 3810QS is WJEC GCSE SPANISH, not German.` — BUILD-READINESS (AMBER, build with care). German IS offered for summer 2027, so worth building — BUT two hazards must be handled before building. (1) CODE MISMATCH: the supplied code 3810QS is WJEC GC
- `WJEC` **WJEC GCSE History (Wales-only)** `3100QS` — BUILD-READINESS (not-built): Spec is current and validly assessed for summer 2027, but the qualification is in active withdrawal — summer 2027 is the FINAL full assessment (resit only Jan 2028), and a
- `WJEC` **Level 1/2 Vocational Award in Global Business Communication (French)** `5879QA` — Research flagged withdrawal; adversarial verify REFUTED it. Human confirm. DO NOT BUILD. Build-readiness signal is RED. This qualification (2022 spec, QN 603/7488/3) is being withdrawn: Ofqual operati
- `WJEC` **GCSE Media Studies** `3680QS` — BUILD-READINESS: AMBER — build with caution / consider deprioritising the WJEC 3680QS variant. This Wales-regulated qualification is being WITHDRAWN under Curriculum for Wales reform and replaced by t
- `WJEC` **GCSE Physical Education (Full Course)** `3550QS` — Research flagged withdrawal; adversarial verify REFUTED it. Human confirm. DO NOT BUILD. Build-readiness = RED. WJEC's official qualification page states summer 2027 is the FINAL full assessment oppor
- `WJEC` **GCSE Spanish (WJEC, Made for Wales)** `3840QS` — BUILD-READINESS: Worth building, BUT fix the spec code first. The catalogued code 3820QS does NOT belong to WJEC Spanish — 3820QS is WJEC GCSE German. The correct codes are: legacy WJEC GCSE Spanish =

## 5. GREEN — current & offered for 2027 (161)

98 built (no action) · 63 not-built (build-ready).

<details><summary>Full GREEN list</summary>

- `both` Cambridge Nationals: Creative iMedia — OCR `J834`
- `both` GCSE (9-1) Business — Edexcel `1BS0`
- `both` GCSE (9-1) Computer Science — OCR `J277`
- `both` GCSE Biology — AQA `8461`
- `both` GCSE Chemistry — AQA `8462`
- `both` GCSE Combined Science: Trilogy — AQA `8464`
- `both` GCSE Design and Technology — AQA `8552`
- `both` GCSE English Literature — AQA `8702`
- `both` GCSE Food Preparation and Nutrition — AQA `8585`
- `both` GCSE French — AQA `8652`
- `both` GCSE Geography — AQA `8035`
- `both` GCSE German — AQA `8662`
- `both` GCSE History — AQA `8145`
- `both` GCSE Physics — AQA `8463`
- `both` GCSE Religious Studies A — AQA `8062`
- `both` GCSE Spanish — AQA `8692`
- `free` BTEC Tech Award Level 1/2 in Health and Social Care — Pearson Edexcel `603/7047/6 (BTEC Tech Award 2022)`
- `free` Cambridge National Level 1/2 in Health and Social Care — OCR `J835`
- `free` Cambridge National Level 1/Level 2 in Sport Studies — OCR `J829`
- `free` Cambridge National in Engineering Programmable Systems (Level 1/Level 2) — OCR `J824`
- `free` Cambridge Nationals Level 1/Level 2 in Child Development — OCR `J809`
- `free` Cambridge Nationals Level 1/Level 2 in Sport Science — OCR `J828`
- `free` Cambridge Nationals: Engineering Design — OCR `J822`
- `free` Cambridge Nationals: Engineering Manufacture (Level 1/Level 2) — OCR `J823`
- `free` Cambridge Nationals: IT — OCR `J836`
- `free` Computer Science — Eduqas `C500QS`
- `free` GCSE (9-1) Biology A (Gateway Science) — OCR `J247`
- `free` GCSE (9-1) Biology B (Twenty First Century Science) — OCR `J257`
- `free` GCSE (9-1) Business — OCR `J204`
- `free` GCSE (9-1) Chemistry — Edexcel (Pearson) `1CH0`
- `free` GCSE (9-1) Classical Civilisation — OCR `J199`
- `free` GCSE (9-1) Combined Science B (Twenty First Century Science) — OCR `J260`
- `free` GCSE (9-1) English Language — Eduqas (WJEC) `C700QS`
- `free` GCSE (9-1) Geography A — Edexcel (Pearson) `1GA0`
- `free` GCSE (9-1) Geography A (Geographical Themes) — OCR `J383`
- `free` GCSE (9-1) Geography B — Edexcel (Pearson) `1GB0`
- `free` GCSE (9-1) Geology — Eduqas (WJEC) `C180QS / C480QS`
- `free` GCSE (9-1) Mathematics — OCR `J560`
- `free` GCSE (9-1) Physics A (Gateway Science) — OCR `J249`
- `free` GCSE (9-1) Physics B (Twenty First Century Science) — OCR `J259`
- `free` GCSE Astronomy — Edexcel `1AS0`
- `free` GCSE Biology — Edexcel `1BI0`
- `free` GCSE Business — AQA `8132`
- `free` GCSE Chemistry A (Gateway Science) — OCR `J248`
- `free` GCSE Citizenship Studies — AQA `8100`
- `free` GCSE Combined Science — Edexcel `1SC0`
- `free` GCSE Combined Science A (Gateway Science) — OCR `J250`
- `free` GCSE Computer Science — Edexcel (Pearson) `1CP2`
- `free` GCSE Design and Technology — Eduqas `C600QS`
- `free` GCSE Design and Technology — WJEC `3600QS`
- `free` GCSE Drama — AQA `8261`
- `free` GCSE Economics — AQA `8136`
- `free` GCSE Electronics — Eduqas `C490QS`
- `free` GCSE Engineering — AQA `8852`
- `free` GCSE English Language — Edexcel `1EN0`
- `free` GCSE English Language (9-1) — OCR `J351`
- `free` GCSE English Literature — Edexcel `1ET0`
- `free` GCSE English Literature — OCR `J352`
- `free` GCSE Film Studies — WJEC `3670QS`
- `free` GCSE French — Edexcel `1FR1`
- `free` GCSE French (Eduqas, reformed) — Eduqas (WJEC) `C800QS`
- `free` GCSE Geography A — Eduqas `C111QS`
- `free` GCSE German (2024) — Edexcel `1GN1`
- `free` GCSE History — Edexcel (Pearson) `1HI0`
- `free` GCSE Mathematics — AQA `8300`
- `free` GCSE Mathematics — Edexcel (Pearson) `1MA1`
- `free` GCSE Mathematics — Eduqas `C300QS`
- `free` GCSE Media Studies — AQA `8572`
- `free` GCSE Physical Education — AQA `8582`
- `free` GCSE Physical Education — Edexcel `1PE0`
- `free` GCSE Physical Education — OCR `J587`
- `free` GCSE Physics — Edexcel (Pearson) `1PH0`
- `free` GCSE Psychology — AQA `8182`
- `free` GCSE Religious Studies (Eduqas, Route A / Route B) — Eduqas `C120QS`
- `free` GCSE Religious Studies (Short Course) — AQA `8061`
- `free` GCSE Religious Studies A — Edexcel `1RA0`
- `free` GCSE Sociology — AQA `8192`
- `free` GCSE Sociology — Eduqas `C200QS`
- `free` GCSE Spanish — Edexcel `1SP1`
- `free` GCSE Statistics — AQA `8382`
- `free` History A (Explaining the Modern World) — OCR `J410`
- `free` Level 1/2 Technical Award in Music Technology (V Cert) — NCFE `603/7008/7`
- `free` Level 1/2 Vocational Award in Construction and the Built Environment (Technical Award) — Eduqas (WJEC-CBAC) `E819QA (task-supplied 5229QA is a legacy/entry designation; current accredited code is E819QA)`
- `free` Level 1/2 Vocational Award in Engineering (Technical Award) — Eduqas `5239QA`
- `free` Level 1/2 Vocational Award in Health and Social Care — Eduqas `5249QA`
- `free` Level 1/2 Vocational Award in Hospitality and Catering — WJEC `5409QA`
- `free` Level 1/2 Vocational Award in Hospitality and Catering (Technical Award) — Eduqas `5409QA`
- `free` Level 1/2 Vocational Award in ICT (Technical Award) — Eduqas (WJEC) `5539QA`
- `free` Level 1/2 Vocational Award in Retail Business (Technical Award) — Eduqas `5299QA`
- `free` Level 1/2 Vocational Award in Sport and Coaching Principles — Eduqas `5259QA`
- `free` OCR GCSE (9-1) Religious Studies (Full Course) — OCR `J625`
- `free` OCR GCSE Chemistry B (Twenty First Century Science) — OCR `J258`
- `free` WJEC Eduqas Level 1/Level 2 GCSE (9-1) in Film Studies — Eduqas `C670QS`
- `free` WJEC Eduqas Level 1/Level 2 GCSE (9-1) in Geology — WJEC (Eduqas) `3180QS`
- `free` WJEC Eduqas Level 1/Level 2 GCSE (9-1) in History — Eduqas (WJEC) `C100QS`
- `not-built` Cambridge OCR Level 1/Level 2 GCSE (9-1) in Media Studies — OCR `J200`
- `not-built` GCSE (9-1) Ancient History — OCR `J198`
- `not-built` GCSE (9-1) Art and Design (Art, Craft and Design) — Edexcel (Pearson) `1AD0`
- `not-built` GCSE (9-1) Biblical Hebrew — Edexcel `1BH0`
- `not-built` GCSE (9-1) Citizenship Studies — Edexcel `1CS0`
- `not-built` GCSE (9-1) Citizenship Studies — OCR `J270`
- `not-built` GCSE (9-1) Classical Greek — OCR `J292`
- `not-built` GCSE (9-1) Design and Technology — Edexcel (Pearson) `1DT0`
- `not-built` GCSE (9-1) Design and Technology — OCR `J310`
- `not-built` GCSE (9-1) Economics — OCR `J205`
- `not-built` GCSE (9-1) Food Preparation and Nutrition — OCR `J309`
- `not-built` GCSE (9-1) Latin — OCR `J282`
- `not-built` GCSE (9-1) Religious Studies (Short Course) — OCR `J125`
- `not-built` GCSE (9-1) Statistics — Edexcel (Pearson) `1ST0`
- `not-built` GCSE Arabic — Edexcel `1AA0`
- `not-built` GCSE Art and Design — Eduqas `C650QS`
- `not-built` GCSE Art and Design (Fine art) — AQA `8202`
- `not-built` GCSE Art and Design (Graphic communication) — AQA `8203`
- `not-built` GCSE Art and Design (Photography) — AQA `8206`
- `not-built` GCSE Art and Design (Textile design) — AQA `8204`
- `not-built` GCSE Art and Design (Three-dimensional design) — AQA `8205`
- `not-built` GCSE Bengali — AQA `8638`
- `not-built` GCSE Biology (WJEC, Wales / Qualifications Wales) — WJEC `3400QS`
- `not-built` GCSE Business — Eduqas `C510QS`
- `not-built` GCSE Chemistry (Wales) — WJEC `3410QS`
- `not-built` GCSE Chinese (Spoken Mandarin) — AQA `8673`
- `not-built` GCSE Chinese (spoken Mandarin / spoken Cantonese) — Edexcel `1CN0`
- `not-built` GCSE Combined Science: Synergy — AQA `8465`
- `not-built` GCSE Dance — AQA `8236`
- `not-built` GCSE Drama — Edexcel `1DR0`
- `not-built` GCSE Drama — Eduqas `C690QS`
- `not-built` GCSE Electronics — WJEC/Eduqas `C490 (catalogued by us as 3490QS)`
- `not-built` GCSE Geography (WJEC, Made for Wales) — WJEC `3140QS`
- `not-built` GCSE Geography B — Eduqas `C112QS`
- `not-built` GCSE Geography B (Geography for Enquiring Minds) — OCR `J384`
- `not-built` GCSE Greek — Edexcel `1GK0`
- `not-built` GCSE Gujarati — Edexcel `1GU0`
- `not-built` GCSE Hebrew (Modern) — AQA `8678`
- `not-built` GCSE History B (Schools History Project) — OCR `J411`
- `not-built` GCSE Italian — AQA `8633`
- `not-built` GCSE Italian — Edexcel `1IN0`
- `not-built` GCSE Japanese — Edexcel `1JA0`
- `not-built` GCSE Latin — Eduqas (WJEC) `C990QS`
- `not-built` GCSE Latin — WJEC `C990QS`
- `not-built` GCSE Media Studies — Eduqas (WJEC) `C680QS`
- `not-built` GCSE Music — AQA `8271`
- `not-built` GCSE Music — Edexcel `1MU0`
- `not-built` GCSE Music — Eduqas `C660QS`
- `not-built` GCSE Music — OCR `J536`
- `not-built` GCSE Panjabi — AQA `8683`
- `not-built` GCSE Persian — Edexcel `1PN0`
- `not-built` GCSE Physics — WJEC `3420QS`
- `not-built` GCSE Polish — AQA `8688`
- `not-built` GCSE Portuguese — Edexcel (Pearson) `1PG0`
- `not-built` GCSE Psychology — Edexcel (Pearson) `1PS0`
- `not-built` GCSE Religious Studies B — AQA `8063`
- `not-built` GCSE Russian — Edexcel `1RU0`
- `not-built` GCSE Turkish — Edexcel `1TU0`
- `not-built` GCSE Urdu — AQA `8648`
- `not-built` GCSE Urdu — Edexcel `1UR0`
- `not-built` Level 1/2 Vocational Award in Global Business Communication (Spanish) — WJEC `5899QA`
- `not-built` Level 1/2 Vocational Award in Performing Arts (Technical Award) — Eduqas (WJEC) `5639QA`
- `not-built` Psychology — OCR `J203`
- `school` Cambridge National Level 1/Level 2 in Sport Science — OCR `R180 (unit of J828)`
- `school` GCSE (9-1) Drama — OCR `J316`
- `school` GCSE Music — Eduqas `C660U`

</details>
