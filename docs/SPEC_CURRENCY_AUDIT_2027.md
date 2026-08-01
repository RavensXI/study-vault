# Spec-Currency Audit — 2027 Cohort (all subjects, all boards)

**Run:** 2026-08-01 · **Scope:** 194 qualifications = every catalogued spec (specs/index.json, all boards) unioned with everything we ship. Build status: {'?': 194}.

**Result:** 148 GREEN · 29 AMBER · 17 RED.

Method: per-qualification research agent (Ofqual register operational/cert end dates + board amendment pages), every RED/withdrawal adversarially re-verified. For built specs RED/AMBER = act now; for not-built specs the verdict is a BUILD-READINESS signal (RED = do not build / superseded). Re-run: `_gen_spec_audit_worklist.py --scope full` → workflow `spec-currency-audit-2027` → this script.

> **Systemic note — Wales reform (Wales IS a planned build market).** WJEC `3xxxQS`/`3xxxCS` legacy GCSEs (Curriculum for Wales) are being withdrawn — final full assessment Summer 2026, Jan-2027 resit only, no Summer 2027 series — and REPLACED by new "Made-for-Wales" GCSEs (first teaching 2025/2026). So a WJEC legacy RED below means **build the Made-for-Wales replacement** (a future build target we have not yet catalogued), NOT ignore. Our existing "Eduqas / WJEC" aliased content stays fine for **England (Eduqas, Cxxx)**; for reformed subjects the **Wales arm diverges** and becomes a SEPARATE Made-for-Wales build/row (the aliasing no longer holds). See memory project_wales_build_plan.

## 1. Built content needing action (0)

Subjects we ship that are RED or AMBER — real 2027-cohort exposure.

## 2. Sunsetting watch — built, fine for 2027 but withdrawing soon (0)

## 3. Do NOT build — not-built specs that are withdrawn/superseded (0)


## 4. Build with care — not-built AMBER (build to the current version) (0)


## 5. GREEN — current & offered for 2027 (148)

0 built (no action) · 0 not-built (build-ready).

<details><summary>Full GREEN list</summary>

- `None` Ancient History — OCR `J198`
- `None` Art and Design (Art, Craft and Design) — Edexcel `1AD0`
- `None` BTEC Level 1/Level 2 Tech Award in Health and Social Care (2022) — Pearson Edexcel (BTEC) `BTEC Tech Award (2022 suite); publication code VQ000054`
- `None` Bengali — AQA `8638`
- `None` Cambridge National Level 1/Level 2 in Health and Social Care — OCR `J835`
- `None` Cambridge National Level 1/Level 2 in Sport Science — OCR (Cambridge OCR) `J828`
- `None` Cambridge Nationals Level 1/Level 2 in Engineering Design — OCR (Cambridge OCR) `J822`
- `None` Cambridge Nationals: Child Development (Level 1/Level 2) — OCR `J809`
- `None` Cambridge Nationals: Creative iMedia — OCR `J834`
- `None` Cambridge Nationals: Engineering Manufacture (Level 1/Level 2) — OCR `J823`
- `None` Cambridge OCR Level 1/Level 2 Cambridge National in Engineering Programmable Systems — OCR `J824`
- `None` Cambridge OCR Level 1/Level 2 Cambridge National in Sport Science (J828) — OCR `J828 (R180 = externally assessed exam unit)`
- `None` Cambridge OCR Level 1/Level 2 Cambridge National in Sport Studies — OCR `J829`
- `None` Cambridge OCR Level 1/Level 2 GCSE (9-1) in Business — OCR `J204`
- `None` Cambridge OCR Level 1/Level 2 GCSE (9-1) in Citizenship Studies — OCR `J270`
- `None` Cambridge OCR Level 1/Level 2 GCSE (9-1) in Economics — OCR `J205`
- `None` Cambridge OCR Level 1/Level 2 GCSE (9-1) in Food Preparation and Nutrition — OCR `J309`
- `None` Cambridge OCR Level 1/Level 2 GCSE (9-1) in Mathematics — OCR `J560`
- `None` Cambridge OCR Level 1/Level 2 GCSE (9-1) in Religious Studies (Full Course) — OCR `J625`
- `None` Cambridge OCR Level 1/Level 2 GCSE (9-1) in Religious Studies (Short Course) — OCR `J125`
- `None` Chinese (spoken Mandarin/spoken Cantonese) — Edexcel `1CN0`
- `None` Classical Civilisation — OCR `J199`
- `None` Combined Science — Edexcel `1SC0`
- `None` Combined Science: Synergy — AQA `8465`
- `None` Dance — AQA `8236`
- `None` Design and Technology — Eduqas `C600QS`
- `None` Design and Technology — OCR `J310`
- `None` English Literature — OCR `J352`
- `None` Food Preparation and Nutrition — AQA `8585`
- `None` GCSE (9-1) Astronomy — Edexcel (Pearson) `1AS0`
- `None` GCSE (9-1) Biblical Hebrew — Edexcel `1BH0`
- `None` GCSE (9-1) Biology — Edexcel `1BI0`
- `None` GCSE (9-1) Biology B (Twenty First Century Science) — OCR `J257`
- `None` GCSE (9-1) Business — Edexcel `1BS0`
- `None` GCSE (9-1) Chemistry — Edexcel (Pearson) `1CH0`
- `None` GCSE (9-1) Chemistry A (Gateway Science) — OCR `J248`
- `None` GCSE (9-1) Chemistry B (Twenty First Century Science) — OCR `J258`
- `None` GCSE (9-1) Combined Science A (Gateway Science) — OCR (now branded Cambridge OCR) `J250`
- `None` GCSE (9-1) Combined Science B (Twenty First Century Science) — OCR `J260`
- `None` GCSE (9-1) Computer Science — OCR `J277`
- `None` GCSE (9-1) Design and Technology — Edexcel `1DT0`
- `None` GCSE (9-1) English Language — OCR `J351`
- `None` GCSE (9-1) English Literature — Edexcel `1ET0`
- `None` GCSE (9-1) Geography A — Edexcel `1GA0`
- `None` GCSE (9-1) Geography A (Geographical Themes) — OCR `J383`
- `None` GCSE (9-1) Geography B — Edexcel (Pearson) `1GB0`
- `None` GCSE (9-1) Greek — Edexcel `1GK0`
- `None` GCSE (9-1) Gujarati — Edexcel `1GU0`
- `None` GCSE (9-1) History A (Explaining the Modern World) — OCR `J410`
- `None` GCSE (9-1) History B (Schools History Project) — OCR `J411`
- `None` GCSE (9-1) Italian — Edexcel (Pearson) `1IN0`
- `None` GCSE (9-1) Japanese — Edexcel (Pearson) `1JA0`
- `None` GCSE (9-1) Media Studies — Eduqas `C680QS`
- `None` GCSE (9-1) Media Studies — OCR `J200`
- `None` GCSE (9-1) Physical Education — Edexcel `1PE0`
- `None` GCSE (9-1) Physical Education — OCR `J587`
- `None` GCSE (9-1) Physics — Edexcel `1PH0`
- `None` GCSE (9-1) Physics B (Twenty First Century Science) — OCR `J259`
- `None` GCSE (9-1) Portuguese — Edexcel (Pearson) `1PG0`
- `None` GCSE (9-1) Psychology — Edexcel `1PS0`
- `None` GCSE (9-1) Psychology — OCR `J203`
- `None` GCSE (9-1) Religious Studies A — Edexcel `1RA0`
- `None` GCSE Arabic — Edexcel (Pearson) `1AA0`
- `None` GCSE Biology — AQA `8461`
- `None` GCSE Biology A (Gateway Science) — OCR `J247`
- `None` GCSE Business — AQA `8132`
- `None` GCSE Chemistry — AQA `8462`
- `None` GCSE Chemistry (Wales) — WJEC `3410QS`
- `None` GCSE Chinese (Spoken Mandarin) — AQA `8673`
- `None` GCSE Citizenship Studies — AQA `8100`
- `None` GCSE Combined Science: Trilogy — AQA `8464`
- `None` GCSE Computer Science — AQA `8525`
- `None` GCSE Computer Science — Edexcel (Pearson) `1CP2`
- `None` GCSE Design and Technology — AQA `8552`
- `None` GCSE Drama — AQA `8261`
- `None` GCSE Drama — Edexcel `1DR0`
- `None` GCSE Drama — Eduqas `C690QS`
- `None` GCSE Economics — AQA `8136`
- `None` GCSE Engineering — AQA `8852`
- `None` GCSE English Language — AQA `8700`
- `None` GCSE English Language — Edexcel (Pearson) `1EN0`
- `None` GCSE English Language — Eduqas `C700QS`
- `None` GCSE English Literature — AQA `8702`
- `None` GCSE Food Preparation and Nutrition — Eduqas `C560QS`
- `None` GCSE French — AQA `8652`
- `None` GCSE French (2024) — Edexcel (Pearson) `1FR1`
- `None` GCSE Geography — AQA `8035`
- `None` GCSE Geography B — Eduqas `C112QS`
- `None` GCSE Geography B (Geography for Enquiring Minds) — OCR `J384`
- `None` GCSE Hebrew (Modern) — AQA `8678`
- `None` GCSE History — Eduqas `C100QS`
- `None` GCSE Italian — AQA `8633`
- `None` GCSE Latin — Eduqas `C990QS (our catalogue records C580QS — see action)`
- `None` GCSE Mathematics — AQA `8300`
- `None` GCSE Media Studies — AQA `8572`
- `None` GCSE Music — AQA `8271`
- `None` GCSE Music — Edexcel `1MU0`
- `None` GCSE Music — Eduqas `C660QS`
- `None` GCSE Physical Education — AQA `8582`
- `None` GCSE Physical Education — Eduqas `C550QS (full course); C555QT (short course)`
- `None` GCSE Physics — AQA `8463`
- `None` GCSE Religious Studies (Route A / Route B) — Eduqas `C120QS`
- `None` GCSE Religious Studies (Short Course) — AQA `8061`
- `None` GCSE Religious Studies A — AQA `8062`
- `None` GCSE Religious Studies B — AQA `8063`
- `None` GCSE Russian — Edexcel `1RU0`
- `None` GCSE Sociology — AQA `8192`
- `None` GCSE Sociology — Eduqas `C200QS`
- `None` GCSE Spanish (AQA Level 1/Level 2 GCSE (9-1) in Spanish) — AQA `8692`
- `None` GCSE Statistics — AQA `8382`
- `None` GCSE Turkish — Edexcel `1TU0`
- `None` GCSE Urdu — AQA `8648`
- `None` GCSE Urdu — Edexcel `1UR0`
- `None` German — AQA `8662`
- `None` German — Edexcel `1GN1`
- `None` Latin — OCR `J282`
- `None` Latin — WJEC `C990QS`
- `None` Level 1/2 Vocational Award in Construction and the Built Environment (Technical Award) — Eduqas (WJEC-CBAC) `E819QA (accredited Eduqas qual code; 5229QA held in our catalogue is the Eduqas ENTRY code for the same qualification)`
- `None` Level 1/2 Vocational Award in Engineering (Technical Award) — Eduqas `5239QA`
- `None` Level 1/2 Vocational Award in Health and Social Care (Technical Award) — Eduqas `5249QA`
- `None` Level 1/2 Vocational Award in Hospitality and Catering (Technical Award) — Eduqas `5409QA`
- `None` Level 1/2 Vocational Award in ICT (Technical Award) — Eduqas (WJEC-CBAC) `5539QA`
- `None` Level 1/2 Vocational Award in Performing Arts (Technical Award) — Eduqas (WJEC) `5639QA`
- `None` Level 1/2 Vocational Award in Retail Business (Technical Award) — Eduqas `5789QA`
- `None` Level 1/2 Vocational Award in Sport and Coaching Principles (Technical Award) — Eduqas `5259QA`
- `None` Mathematics — Edexcel `1MA1`
- `None` Music — OCR `J536`
- `None` Music — Eduqas `C660QS (component prefix C660U — C660U10-1 Performing, C660U20-1 Composing, C660U30-1 Appraising)`
- `None` Music Technology — NCFE `603/7008/7`
- `None` Panjabi — AQA `8683`
- `None` Pearson Edexcel Level 1/Level 2 GCSE (9-1) in Citizenship Studies — Edexcel `1CS0`
- `None` Pearson Edexcel Level 1/Level 2 GCSE (9-1) in History — Edexcel `1HI0`
- `None` Pearson Edexcel Level 1/Level 2 GCSE (9-1) in Statistics — Edexcel (Pearson) `1ST0`
- `None` Persian — Edexcel `1PN0`
- `None` Physics A (Gateway Science) — OCR `J249`
- `None` Polish — AQA `8688`
- `None` Psychology — AQA `8182`
- `None` Spanish — Edexcel `1SP1`
- `None` WJEC Eduqas Level 1/Level 2 GCSE (9-1) in Art and Design — Eduqas `C650QS (family C650QS-C656QS: Art Craft and Design, Fine Art, Critical and Contextual Studies, Textile Design, Graphic Communication, Three-Dimensional Design, Photography)`
- `None` WJEC Eduqas Level 1/Level 2 GCSE (9-1) in Business — Eduqas `C510QS`
- `None` WJEC Eduqas Level 1/Level 2 GCSE (9-1) in Computer Science — Eduqas `C500QS`
- `None` WJEC Eduqas Level 1/Level 2 GCSE (9-1) in Electronics — Eduqas `C490QS`
- `None` WJEC Eduqas Level 1/Level 2 GCSE (9-1) in Electronics — WJEC (WJEC CBAC Ltd — published as "WJEC Eduqas") `C490QS`
- `None` WJEC Eduqas Level 1/Level 2 GCSE (9-1) in Film Studies — Eduqas `C670QS`
- `None` WJEC Eduqas Level 1/Level 2 GCSE (9-1) in Film Studies — WJEC `C670QS (our catalogue label "WJEC 3670QS" is wrong — see action)`
- `None` WJEC Eduqas Level 1/Level 2 GCSE (9-1) in Geography A — Eduqas `C111QS`
- `None` WJEC Eduqas Level 1/Level 2 GCSE (9-1) in Mathematics — Eduqas `C300QS`
- `None` WJEC Level 1/2 Vocational Award in Hospitality and Catering (Technical Award) — WJEC `5409QA`

</details>
