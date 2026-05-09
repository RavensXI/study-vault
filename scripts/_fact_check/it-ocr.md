# Fact-Check Report — it-ocr (OCR Cambridge National IT J836)

**Checked:** 2026-05-09  
**Lessons checked:** 14  
**Findings:** HIGH 0 · MEDIUM 0 · LOW 2  
**Ship status:** CLEAR — no HIGH findings

---

## Summary

All 14 lessons were checked against authoritative sources:

- **UK legislation** (legislation.gov.uk): Computer Misuse Act 1990, Copyright Designs & Patents Act 1988, Data Protection Act 2018, Freedom of Information Act 2000, Health & Safety at Work Act 1974
- **Cyber-security** (ncsc.gov.uk): malware types (virus, worm, trojan, ransomware, spyware, adware, botnet), social engineering methods (phishing, pretexting, baiting, quid pro quo, scareware, shoulder surfing), hacker hat colours
- **IoE / Cisco** (Cisco Blogs): four pillars — People, Process, Data, Things ✓ verified correct
- **Spreadsheet functions** (support.microsoft.com): VLOOKUP four arguments, SUMIF syntax, COUNTIF syntax, IF/AND/OR nesting ✓ all correct
- **Flowchart symbols**: oval (start/end), rectangle (process), diamond (decision), parallelogram (input/output) ✓ verified correct against ANSI/ISO standards
- **AR types**: marker-based, markerless, superimposed ✓ definitions consistent with industry standard sources
- **FOI Act response time**: 20 working days ✓ verified correct (legislation.gov.uk / ICO)
- **Bluetooth**: one LOW finding (range understated — see below)

---

## Findings

### LOW-1 — Lesson 6 (Prevention Measures & IT Legislation)

**Lesson ID:** `0d6e448b-2d22-4536-a281-5d5fc2dcaea2`

**Claim:** "(3) modifying computer data without authorisation (e.g. installing malware)"

**Issue:** The lesson describes CMA offence 3 using the original 1990 Act wording ("unauthorised modification of computer material"). The Police and Justice Act 2006 replaced section 3 with a broader formulation: "Unauthorised acts with intent to impair, or with recklessness as to impairing, operation of computer, etc." The lesson's wording is the conventional GCSE-level simplification used across OCR revision resources and is not materially misleading at this level. The example given (installing malware) is correct.

**Recommended wording (optional improvement):** Retain current wording but note in parentheses: "also covers DoS attacks and any act with intent to impair a computer system."

**Source:** https://www.legislation.gov.uk/ukpga/1990/18/section/3

---

### LOW-2 — Lesson 7 (Digital Communications & Distribution)

**Lesson ID:** `155fc37f-da29-4609-a314-9ecc723cbd0f`

**Claim:** "Bluetooth connects devices at short range (typically up to 10 metres)"

**Issue:** Bluetooth range depends on device power class. Class 2 consumer devices (headphones, keyboards) reach 10–30 m. Class 1 devices reach up to ~100 m. Bluetooth 5.0+ extends range further still. Stating "up to 10 metres" understates the typical modern consumer Bluetooth range. This is unlikely to cause an exam problem (the spec treats Bluetooth as short-range), but it could create a misconception.

**Recommended correction:** Change to "typically 10–30 metres for consumer devices, though range varies by device class."

**Source:** https://www.bluetooth.com/learn-about-bluetooth/key-attributes/range/

---

## Clean lessons (0 findings)

| # | Lesson |
|---|--------|
| L1 | Design Tools for IT Solutions |
| L2 | Human Computer Interface (HCI) in Everyday Life |
| L3 | Information, Data Types & Validation |
| L4 | Data Collection, Storage & Testing |
| L5 | Cyber-security: Threats & Impacts |
| L8 | The Internet of Everything (IoE) |
| Spreadsheets L1 | Planning & Designing a Spreadsheet Solution |
| Spreadsheets L2 | Building the Spreadsheet — Formulas, Functions & Validation |
| Spreadsheets L3 | Testing & Evaluating the Spreadsheet Solution |
| AR L1 | Augmented Reality — Purpose, Types & Devices |
| AR L2 | Designing & Creating an AR Model Prototype |
| AR L3 | Testing & Reviewing the AR Prototype |

*(Lessons 9–14 above use the unit numbering Spreadsheets L1–L3 and AR L1–L3)*

---

## Notes on high-risk claim categories

| Category | Verdict |
|---|---|
| CMA 1990 offences (dates, scope) | PASS — dates correct, offences accurately described at GCSE level |
| CDPA 1988 (software, images, music) | PASS — scope correctly described |
| DPA 2018 / UK GDPR (principles, rights) | PASS — lawful basis, accuracy, retention, subject access rights all correct |
| FOI Act — 20 working days | PASS — confirmed against legislation.gov.uk s.10 and ICO guidance |
| H&S at Work Act (ergonomics, breaks) | PASS — correctly describes employer duty; DSE Regulations 1992 are the implementing instrument but the lesson does not cite section numbers |
| IoE four pillars (Cisco) | PASS — People, Process, Data, Things match Cisco's canonical definition |
| Malware types (7 named) | PASS — virus, worm, trojan, ransomware, spyware, adware, botnet all correctly defined |
| Social engineering (6 methods) | PASS — phishing, pretexting, baiting, quid pro quo, scareware, shoulder surfing all correctly described |
| VLOOKUP syntax | PASS — four arguments in correct order; 0 = exact match correctly stated |
| SUMIF syntax | PASS — SUMIF(range, criteria, sum_range) argument order correct |
| COUNTIF syntax | PASS — COUNTIF(range, criteria) correct |
| Flowchart symbols | PASS — oval/start-end, rectangle/process, diamond/decision, parallelogram/input-output confirmed against ISO 5807 / ANSI |
| AR types (marker-based, markerless, superimposed) | PASS — definitions consistent with industry standard AR taxonomy |
| Bluetooth range | LOW finding (see above) |
