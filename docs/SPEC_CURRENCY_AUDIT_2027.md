# Spec-Currency Audit — 2027 Cohort

**Run:** 2026-06-19 · **Scope:** 88 live free-tier subjects (school_id NULL). Unity bespoke out of scope (owner-controlled, low spec-volatility).

**Result:** 81 GREEN · 6 AMBER · 1 RED

Method: one research agent per subject checked the Ofqual Register of Regulated Qualifications (operational/certification end dates = authoritative withdrawal signal) plus the board's own specification/updates pages. Every RED/withdrawal verdict was adversarially re-verified before it was allowed to stand (a refuted withdrawal downgrades to AMBER for human confirm, never silently to GREEN). Calibration: GCSEs cannot be reformed mid-course, so RED = withdrawal affecting the 2027 series, not a future reform.

Re-run annually: `python scripts/_gen_spec_audit_worklist.py` then run the `spec-currency-audit-2027` workflow, then `python scripts/_gen_spec_audit_ledger.py <date>`.

## RED — withdrawn / not offered for 2027 (decision needed) (1)

These qualifications do not have a normal summer-2027 exam series. Decide per subject: pull from the picker, mark legacy, or rebuild against the replacement spec.

### GCSE Food Preparation and Nutrition — Eduqas (WJEC) `C560QS (C560P1 written / C560P2 on-screen)`
- **slug:** `food-preparation-and-nutrition-eduqas` · **offered 2027:** False · **confidence:** high · **end date:** Final full assessment: Summer 2026. Resit-only: January 2027 (subject to demand). Ofqual operational end date: 31/07/2027. No Summer 2027 exam series.
- **What changed:** No material content amendment since our 2026-05-05 build. The qualification is being withdrawn, not updated.
- **Adversarial verify:** confirmed_withdrawn=True, still_offered_2027=False — Adversarial attempt to refute the withdrawal FAILED — every authoritative board source confirms the legacy spec is being withdrawn, not updated.

LEGACY SPEC (our build target): Eduqas GCSE Food Preparation and Nutrition, code C560 / C560QS (England, first taught 2016).
- Eduqas/WJEC's own guidance,
- **Action:** WITHDRAW from our free-tier offer for the 2027 cohort. Eduqas/WJEC GCSE Food Preparation and Nutrition (C560, QN 601/8093/6) is being replaced by the reformed GCSE Food and Nutrition (QWADN, QN 601/8085/7; first teaching Sept 2025, first assessment Summer 2026). From Sept 2025 learners must NOT be entered onto C560; its final full assessment was Summer 2026 with only a conditional January 2027 resit — there is NO Summer 2027 examination. A 2027-cohort student (started Sept 2025) cannot sit C560. Replace our content with the new GCSE Food and Nutrition (teaching from 2025) spec, or retire the Eduqas food slug. Confidence high: Ofqual operational end date 31/07/2027 and the repeated official Eduqas/WJEC withdrawal notice both confirm this. Note: distinct from the also-withdrawn legacy GCSE Food and Nutrition QWADN/601/8085/7 — verdict is for C560 specifically.
- **Evidence:** https://www.qualifications.education.gov.uk/Qualification/60180936 · https://www.eduqas.co.uk/qualifications/food-preparation-and-nutrition-gcse/ · https://www.wjec.co.uk/qualifications/food-and-nutrition-gcse/ · https://www.eduqas.co.uk/media/1wabxvpn/eduqas-food-prep-and-nutr-newsletter-sept-2025-1-1.pdf

## AMBER — offered for 2027 but a change needs a content review (6)

Offered for 2027, but a material spec/assessment change lands on the 2027 cohort or a withdrawal is coming for a later cohort. Targeted content pass, not a rebuild. Priority-order by exam-entry size.

### Cambridge National in Information Technology (Level 1/Level 2) — OCR `J836`
- **slug:** `it-ocr` · **offered 2027:** True · **confidence:** high
- **What changed:** Spec moved to Version 7 (June 2026), issued after our 2026-05-09 build. Material teaching-content changes to Unit R070 (Augmented Reality, the NEA unit): Topic Area 3.2 Triggers — "Object recognition" and "Location based" REMOVED from teaching content; Topic Area 4.1 Testing — "User testing" REMOVED from teaching content; Topic Area 3.4 Information report — "Animation" ADDED to teaching content; R070 Aims/Assessment guidance clarified that alternative software can be used to create a simulated AR experience (with expectations defined); Section 6.2.2 Plagiarism expanded with AI-misuse and source-referencing teaching requirements. Remaining V7 changes are admin/clarification (marks calculator on results day, feedback section, post-results services, refreshed hyperlinks, Cambridge OCR rebrand). Note: V6 (Sept 2025) was a pre-build rebrand/clarification update; only V7 is post-build and material.
- **Action:** Review R070 (Augmented Reality) content built 2026-05-09 against Version 7 (June 2026). Specifically: remove any teaching of "object recognition" and "location-based" triggers (Topic Area 3.2) and "user testing" (Topic Area 4.1) as these were dropped from the teaching content; add coverage of "animation" in the information report (3.4); reflect that a simulated AR experience using alternative software is now explicitly permitted; and align any plagiarism/integrity material with the expanded AI-misuse and referencing requirements. Confirmed still offered for summer 2027 (OCR lists set assignments for the Jan and June 2027 series; no withdrawal notice). NB: J836 is a vocational Level 1/2 Cambridge National (technical award), not a true GCSE — assessment is one exam unit (R050) plus two NEA coursework units (R060, R070); content drift here is in the NEA unit.
- **Evidence:** https://www.ocr.org.uk/qualifications/cambridge-nationals/it-level-1-2-j836/ · https://www.ocr.org.uk/qualifications/cambridge-nationals/it-level-1-2-j836/assessment/ · https://www.ocr.org.uk/Images/610951-specification-cambridge-nationals-it-j836.pdf · https://www.ocr.org.uk/administration/support-and-tools/subject-updates/cambridge-national-it-update-654212/

### GCSE Computer Science — AQA `8525`
- **slug:** `computer-science-aqa` · **offered 2027:** True · **confidence:** medium
- **What changed:** AQA issued an UPDATED 8525 spec (v1.3, June 2025) for the 2027 cohort that REMOVES content (DfE-driven): elements with "varying views on continued relevancy" and "some stated examples of networking protocols". Paper 2 no longer covers the removed content from summer 2027. Crucially, spec code 8525 is REUSED for both the legacy spec (first teach 2020, exams 2022-2026, v1.1/1.2) and the new 2027 spec (first teach Sept 2025, v1.3). The v1.3 amendment was published June 2025, BEFORE our 2026-05-09 build, so it is not an amendment issued after our build (amended_since_build=false). However, AMBER is warranted because our build fell during the transitional year when both spec variants coexist under the identical code: there is a material risk our content tracked legacy 2022-2026 content rather than the trimmed 2027 (v1.3) content. No NEW material amendment was found dated after 2026-05-09.
- **Action:** REVIEW: Confirm our 2026-05-09 build reflects the v1.3 (2027-cohort) trimmed spec, not the legacy 2022-2026 content. Specifically verify removed content is absent: the dropped networking-protocol examples and the lower-relevance items AQA cut from Paper 2 for summer 2027. Cross-check our Computer Systems / Computational Thinking units against the v1.3 spec PDF (16 Jun 2025) at aqa.org.uk/8525. Qualification IS offered for summer 2027 (June 2027 series confirmed: Papers 1A/1B/1C 10 May 2027, Paper 2 19 May 2027) and is NOT withdrawn. Confidence is medium because the Ofqual register detail page (QN 601/8301/9) could not be loaded directly (it now redirects to find-a-regulated-qualification with a JS search form); status was confirmed via AQA's own Key Dates and news pages instead. No operational/certification end date before summer 2027 found.
- **Evidence:** https://www.aqa.org.uk/gcse-computer-science-specification-changes-for-summer-2027 · https://www.aqa.org.uk/subjects/computer-science/gcse/computer-science-8525/key-dates · https://www.aqa.org.uk/subjects/computer-science/gcse/computer-science-8525/specification/general-administration · https://www.aqa.org.uk/subjects/computer-science/gcse/computer-science-8525/specification

### GCSE English Language — AQA `8700`
- **slug:** `english-language-aqa` · **offered 2027:** True · **confidence:** high
- **What changed:** AQA introduced changes to GCSE English Language exam papers that are live from summer 2026 onwards and therefore apply to the summer 2027 cohort. Changes are concentrated in Paper 1: Q1 is now a multiple-choice format (circle-shading, replacing true/false ticks); Q3 narrowed to a single structural effect; Q4 reworded (removed "student", clarified agree/disagree, added a foreground statement); Q5 narrative option now asks for the OPENING of a story rather than a full narrative, plus an imagination reminder. Paper 2 Q2/Q4 minor rewording. Mark schemes enhanced (new "typical features" column for Q5 on both papers). Mark allocations and assessed skills are unchanged; AQA frames these as wording/mark-scheme clarifications. Announced Jan/Mar 2025; updated SAMs (sets 2 & 3) published Nov 2025; spec PDF re-versioned 20 Mar 2026 — 5 days AFTER our 2026-03-15 build. The Q1 multiple-choice and Q5 "story opening" shifts are material to how a practice-first English Language build should drill question formats, so our practice content should be reviewed to confirm it reflects the 2026 AQA Paper 1 format.
- **Action:** REVIEW our practice-first English Language (AQA) content against AQA's 2026 Paper 1 changes — specifically Q1 (now multiple-choice), Q3 (single structural effect), Q5 (story OPENING not full narrative), and the Q4 rewording. These are live for summer 2026 and apply to the 2027 cohort. Our build (2026-03-15) predates the re-versioned spec PDF (20 Mar 2026) by 5 days, so verify the new formats are reflected. Not a withdrawal risk: Ofqual Register shows status "Available to learners" with no end date, and AQA confirms June 2027 exams (8700/1 24 May 2027, 8700/2 8 June 2027). Confidence high.
- **Evidence:** https://find-a-qualification.services.ofqual.gov.uk/qualifications/60142923 · https://www.aqa.org.uk/subjects/english/gcse/english-8700/key-dates · https://www.aqa.org.uk/subjects/english/gcse/english-8700/specification · https://www.aqa.org.uk/english-language-changes

### GCSE English Literature — Eduqas (WJEC) `C720QS`
- **slug:** `english-literature-eduqas` · **offered 2027:** True · **confidence:** high
- **What changed:** MATERIAL content change for the 2027 cohort: the GCSE English Literature Poetry Anthology (Component 1, Section B) has been replaced. The current anthology (18 poems) was examined for the FINAL time in Summer 2026; a NEW 15-poem anthology is examined for the FIRST time in Summer 2027 (first teaching Sept 2025). New anthology adds poems such as "Origin Story" by Eve L. Ewing and drops 3 poems. The spec code (C720QS) and Ofqual QN (601/5246/1) are unchanged — this is an amendment to the existing qualification, not a new one, and the qualification is NOT withdrawn. NOTE: the amendment was PUBLISHED before our build date (Sept 2025 newsletter / 2025 download), so it was not issued after 2026-03-24 (hence amended_since_build=false). The risk is the inverse: our 2026-03-24 build could have been keyed to the still-live 2026 (old 18-poem) anthology. Our anthology coverage must be checked against the new 2027 set.
- **Action:** REVIEW our anthology content. The qualification is fully offered for Summer 2027 (no withdrawal; same C720QS / QN 601/5246/1). AMBER because a material content change is in effect for the 2027 cohort: the Poetry Anthology was swapped — old 18-poem anthology last examined Summer 2026, new 15-poem anthology first examined Summer 2027. Verify that our Eduqas English Lit poetry-anthology lessons cover the NEW 15-poem 2027 anthology (incl. "Origin Story" by Eve L. Ewing; The Schoolboy, I Wandered Lonely as a Cloud, Sonnet 29, Cousin Kate, Drummer Hodge, I Shall Return, Disabled, Decomposition, Catrin, Blackberry Picking, Kamikaze, War Photographer, Dusting the Phone, Remains) and do NOT teach the retired 18-poem set. If our 2026-03-24 build used the old anthology, that content is wrong for the 2027 cohort and needs replacing. Confidence high on the facts; not amended_since_build because the change pre-dates our build.
- **Evidence:** https://www.eduqas.co.uk/qualifications/english-literature-gcse/ · https://www.eduqas.co.uk/home/english-with-eduqas/eduqas-gcse-english-literature-poetry-anthology-2025/ · https://www.eduqas.co.uk/media/zd1b4ii5/new-poetry-anthology-for-first-examination.pdf · https://www.eduqas.co.uk/media/szolurrz/new-poetry-anthology-for-first-examination-in-2027-mlp-18pt.pdf

### Pearson Edexcel Level 1/Level 2 GCSE (9-1) in Geography A — Edexcel (Pearson) `1GA0`
- **slug:** `geography-edexcel-a` · **offered 2027:** True · **confidence:** medium
- **What changed:** No NEW material content amendment was published after our 2026-04-25 build. However, an assessment change that was already published earlier (Issue 4, 4 Sept 2024; current spec Issue 5, Sept 2025) first took EFFECT at the May/June 2026 exam series, immediately after our build: Paper 1 (1GA0/01 The Physical Environment) duration increased from 1h30 to 1h45. Issue 4 also made DEI terminology updates ('small number of geographical terms' changed for inclusivity). The May 2026 subject update only reiterated the Paper 1 duration change; it introduced nothing new. No Issue 6 has been published in 2026.
- **Action:** Quick review recommended (AMBER), not a rebuild. The qualification is firmly offered for summer 2027 (Ofqual Register: QN 601/8134/5, status 'Available to learners', no operational end date; no withdrawal notice). The 2027 cohort sits the same now-locked updated spec (Issue 5). The one thing to verify: our 2026-04-25 content was built right before the May/June 2026 series when Paper 1's new 1h45 duration first applied — confirm our exam-technique/timing guidance and any Paper 1 references reflect 1h45 (not 1h30) and that we adopted the Issue 4 DEI terminology. Note: the DfE funding-approval end date of 31/07/2027 is a routine funding window (periodically renewed), NOT a qualification withdrawal/last-assessment date — Ofqual shows no operational end date. Medium confidence: the Issue 5 PDF could not be parsed directly to confirm the printed summary-of-changes, but multiple Pearson sources corroborate the issue history and the single assessment change.
- **Evidence:** https://find-a-qualification.services.ofqual.gov.uk/qualifications/60181345 · https://www.qualifications.education.gov.uk/Qualification/60181345 · https://qualifications.pearson.com/en/qualifications/edexcel-gcses/geography-a-2016.html · https://qualifications.pearson.com/en/news-policy/subject-updates/geography/GCSE-Geography-A-B-Specification-Updates.html

### Separate Sciences B (Twenty First Century) — Biology B / Chemistry B / Physics B — OCR `J257 / J258 / J259`
- **slug:** `separate-sciences-ocr-b` · **offered 2027:** True · **confidence:** high · **end date:** 31/07/2027 (operational end date on DfE/Ofqual register — summer 2027 is the FINAL assessment series; no exams or resits available thereafter)
- **What changed:** No material content amendment issued after the 2026-05-09 build date. The live specification remains the 2016 accredited version; the most recent documented spec touch was Feb 2024 (Physics B), well before our build. Content is current.
- **Action:** FLAG FOR WITHDRAWAL PLANNING. The entire OCR Twenty First Century Science B suite (Biology B J257, Chemistry B J258, Physics B J259, Combined Science B J260) carries an operational end date of 31/07/2027 on the DfE/Ofqual register — confirmed directly for Combined Science B (QN 60186902) and Chemistry B (QN 60186057), and the suite shares dates. Summer 2027 exams ARE available (hence still_offered_2027=true, not RED), but it is the LAST assessment series; the suite is being discontinued in favour of OCR's Gateway Science suite (A) thereafter. Content stays usable for the 2027 cohort with no spec changes needed, but schedule this subject for retirement/relabel after summer 2027 and do not target it for the 2028 cohort. Confidence high on the withdrawal date (two independent DfE register entries, consistent suite-wide).
- **Evidence:** https://www.qualifications.education.gov.uk/Qualification/60186902 · https://www.qualifications.education.gov.uk/Qualification/60186057 · https://www.ocr.org.uk/qualifications/gcse/twenty-first-century-science-suite-biology-b-j257-from-2016/ · https://www.ocr.org.uk/qualifications/gcse/twenty-first-century-science-suite-biology-b-j257-from-2016/assessment/

## GREEN — current & offered for 2027 (81)

<details><summary>Full GREEN list</summary>

- BTEC Level 1/Level 2 Tech Award in Health and Social Care — Pearson Edexcel `BTEC Tech Award (2022)` (health-social-care-edexcel)
- Cambridge National (Level 1/Level 2) in Child Development — OCR `J809` (cambridge-nationals-child-development)
- Cambridge National Level 1/2 in Engineering Programmable Systems — OCR `J824` (cambridge-nationals-engineering-programmable-systems)
- Cambridge National Level 1/2 in Enterprise and Marketing — OCR `J837` (cambridge-nationals-enterprise-and-marketing)
- Cambridge National Level 1/Level 2 in Engineering Design — OCR `J822` (cambridge-nationals-engineering-design)
- Cambridge National Level 1/Level 2 in Engineering Manufacture — OCR `J823` (cambridge-nationals-engineering-manufacture)
- Cambridge National Level 1/Level 2 in Health and Social Care — OCR `J835` (health-social-care-ocr)
- Cambridge National in Sport Studies (Level 1/2) — OCR `J829` (cambridge-nationals-sport-studies)
- Cambridge Nationals - Creative iMedia (Level 1/Level 2) — OCR `J834` (cambridge-nationals-creative-imedia)
- Cambridge Nationals Sport Science (Level 1/Level 2) — OCR `J828` (cambridge-nationals-sport-science)
- Classical Civilisation — OCR `J199` (classical-civilisation-ocr)
- GCSE (9-1) Astronomy — Edexcel (Pearson) `1AS0` (astronomy-edexcel)
- GCSE (9-1) Business — OCR `J204` (business-ocr)
- GCSE (9-1) Combined Science — Edexcel (Pearson) `1SC0` (science-edexcel)
- GCSE (9-1) Combined Science A (Gateway Science) — OCR `J250` (science-ocr)
- GCSE (9-1) Computer Science — OCR `J277` (computer-science)
- GCSE (9-1) Electronics — Eduqas / WJEC `C490QS` (electronics-eduqas)
- GCSE (9-1) English Language — Edexcel (Pearson) `1EN0` (english-language-edexcel)
- GCSE (9-1) English Literature — OCR `J352` (english-literature-ocr)
- GCSE (9-1) Gateway Science Suite — Separate Sciences A (Biology A, Chemistry A, Physics A) — OCR `J247 / J248 / J249` (separate-sciences-ocr)
- GCSE (9-1) Geography A — Eduqas (WJEC) `C111QS` (geography-eduqas)
- GCSE (9-1) Geography A (Geographical Themes) — OCR `J383` (geography-ocr)
- GCSE (9-1) Geography B — Edexcel B (Pearson) `1GB0` (geography-edexcel-b)
- GCSE (9-1) Geology — Eduqas / WJEC `C480QS (Welsh-medium 4250SA); our records' "C180QS / 3180QS" appears incorrect` (geology-eduqas)
- GCSE (9-1) Mathematics — OCR `J560` (maths-ocr)
- GCSE (9-1) Physical Education — OCR `J587` (physical-education-ocr)
- GCSE (9-1) Religious Studies — OCR `J625` (religious-studies-ocr)
- GCSE (9-1) Religious Studies A — Edexcel (Pearson) `1RA0` (religious-studies-edexcel)
- GCSE (9-1) Separate Sciences — Biology / Chemistry / Physics — Edexcel (Pearson) `1BI0 / 1CH0 / 1PH0` (separate-sciences-edexcel)
- GCSE (9-1) Sociology — Eduqas / WJEC `C200QS / 3200QS` (sociology-eduqas)
- GCSE (9-1) Spanish — Edexcel (Pearson) `1SP1` (spanish-edexcel)
- GCSE Business — Pearson Edexcel `1BS0` (business-edexcel)
- GCSE Business — AQA `8132` (business-aqa)
- GCSE Citizenship Studies — AQA `8100` (citizenship-aqa)
- GCSE Combined Science B (Twenty First Century Science) — OCR `J260` (science-ocr-b)
- GCSE Combined Science: Trilogy — AQA `8464` (science-aqa)
- GCSE Computer Science — Eduqas / WJEC `C500QS` (computer-science-eduqas)
- GCSE Computer Science — Edexcel (Pearson) `1CP2` (computer-science-edexcel)
- GCSE Design and Technology — AQA `8552` (design-technology)
- GCSE Design and Technology — Eduqas / WJEC `C600QS / 3600QS` (design-technology-eduqas)
- GCSE Drama — AQA `8261` (drama-aqa)
- GCSE Economics — AQA `8136` (economics-aqa)
- GCSE Engineering — AQA `8852` (engineering-aqa)
- GCSE English Language — OCR `J351` (english-language-ocr)
- GCSE English Language — Eduqas (WJEC-CBAC) `C700QS` (english-language-eduqas)
- GCSE English Literature — AQA `8702` (english-literature-aqa)
- GCSE English Literature — Edexcel (Pearson) `1ET0` (english-literature-edexcel)
- GCSE Film Studies — Eduqas / WJEC `C670QS / 3670QS` (film-studies-eduqas)
- GCSE Food Preparation and Nutrition — AQA `8585` (food-preparation-and-nutrition-aqa)
- GCSE French — Eduqas (WJEC) `C800QS` (french-eduqas)
- GCSE French — AQA `8652` (french-aqa)
- GCSE French — Edexcel (Pearson) `1FR1` (french-edexcel)
- GCSE Geography — AQA `8035` (geography-aqa)
- GCSE German — AQA `8662` (german-aqa)
- GCSE German — Edexcel (Pearson) `1GN1` (german-edexcel)
- GCSE History — Edexcel `1HI0` (history-edexcel)
- GCSE History — AQA `8145` (history-aqa)
- GCSE History A (Explaining the Modern World) — OCR `J410` (history-ocr)
- GCSE Mathematics — Eduqas (WJEC) `C300QS` (maths-eduqas)
- GCSE Mathematics — Edexcel (Pearson) `1MA1` (maths-edexcel)
- GCSE Mathematics — AQA `8300` (maths-aqa)
- GCSE Media Studies — AQA `8572` (media-studies-aqa)
- GCSE Physical Education — Edexcel (Pearson) `1PE0` (physical-education-edexcel)
- GCSE Physical Education — AQA `8582` (physical-education-aqa)
- GCSE Psychology — AQA `8182` (psychology-aqa)
- GCSE Religious Studies — Eduqas / WJEC `C120QS / 3120QS` (religious-studies-eduqas)
- GCSE Religious Studies A (8062) + Short Course (8061) — AQA `8062 / 8061` (religious-studies-aqa)
- GCSE Separate Sciences (Biology / Chemistry / Physics) — AQA `8461/8462/8463` (separate-sciences)
- GCSE Sociology — AQA `8192` (sociology-aqa)
- GCSE Spanish — Eduqas (WJEC) `C820QS` (spanish-eduqas)
- GCSE Spanish — AQA `8692` (spanish-aqa)
- GCSE Statistics — AQA `8382` (statistics-aqa)
- Level 1/2 Vocational Award in Construction and the Built Environment (Technical Award) — Eduqas / WJEC `5229QA` (l12-construction-built-environment)
- Level 1/2 Vocational Award in Engineering (Technical Award) — Eduqas (WJEC) `5239QA` (engineering-eduqas)
- Level 1/2 Vocational Award in Health and Social Care (Technical Award) — Eduqas (WJEC) `5249QA` (health-social-care-eduqas)
- Level 1/2 Vocational Award in Hospitality and Catering (Technical Award) — Eduqas / WJEC `5409QA` (hospitality-catering)
- Level 1/2 Vocational Award in ICT (Technical Award) — Eduqas / WJEC `5539QA` (l12-ict)
- Level 1/2 Vocational Award in Retail Business (Technical Award) — Eduqas / WJEC `5789QA (live board code; audit brief said 5299QA — see action)` (l12-retail-business)
- Level 1/2 Vocational Award in Sport and Coaching Principles (Technical Award) — Eduqas / WJEC `5259QA` (l12-sport-and-coaching-principles)
- NCFE Level 1/2 Technical Award in Music Technology — NCFE `603/7008/7` (music-technology)
- WJEC Eduqas Level 1/Level 2 GCSE (9-1) in History — Eduqas (WJEC) `C100QS` (history-eduqas)

</details>
