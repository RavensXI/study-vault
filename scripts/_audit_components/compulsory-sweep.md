# Compulsory Sweep — Free-Tier Subjects

Audit date: 2026-06-01. Checked spec files in `specs/` for student/school exam-content choices (e.g. "choose one topic", optional exam unit, set-text picker). NEA/coursework choices are not flagged — only written-exam content choices matter for the revision platform.

---

## Business

- **Business AQA 8132** — COMPULSORY (no exam content choice)
- **Business Edexcel 1BS0** — COMPULSORY (franchise/sole-trader mention is spec content, not a student option; multiple-choice format note is exam mechanics, not content choice)
- **Business OCR J204** — COMPULSORY (no exam content choice)

## Computer Science

- **Computer Science OCR J277** — COMPULSORY (no exam content choice)
- **Computer Science AQA 8525** — COMPULSORY. Options A/B/C (C#/Python/VB.NET) are entry-code variants for the programming task; the written exam content is identical for all.

## Combined Science / Separate Sciences

- **Combined Science AQA 8464 (Trilogy)** — COMPULSORY (Biology/Chemistry/Physics all compulsory; no optional content)
- **AQA Biology 8461 / Chemistry 8462 / Physics 8463** — COMPULSORY (all content compulsory)

## Mathematics

- **Mathematics AQA 8300** — COMPULSORY (Foundation/Higher tier split is a tier choice, not a content choice within the same tier)

## Languages (AQA)

- **Spanish AQA 8692** — COMPULSORY. In-exam writing task: students pick Q5.1 or 5.2 (Foundation) / Q2.1 or 2.2 and Q3.1 or 3.2 (Higher). These are alternative prompts for the same writing task answered at exam time — NOT different topics to learn. All themes/vocabulary are identical for all students.
- **French AQA 8652** — COMPULSORY. Same in-exam writing task variant choice as Spanish — not a content-coverage difference.
- **German AQA 8662** — COMPULSORY. Same in-exam writing task variant choice as Spanish/French — not a content-coverage difference.

## Citizenship

- **Citizenship AQA 8100** — COMPULSORY (no exam content choice)

## Health & Social Care

- **Health & Social Care Pearson Edexcel** — No spec file in repo; not swept. (Free-tier has 12 lessons built — flagged for manual check if optional exam units exist in the Pearson GCSE HSC spec.)
- **Health & Social Care Eduqas L1/2 5249QA** — COMPULSORY (resit mechanic noted but no content choice)
- **Cambridge Nationals Health & Social Care OCR J835** — COMPULSORY for exam unit; "chosen from" reference is a cross-reference in spec changelog, not a student choice.

## Hospitality & Catering

- **Hospitality & Catering Eduqas L1/2 5409QA** — COMPULSORY (no exam content choice)

## Food Preparation & Nutrition

- **Food Preparation & Nutrition AQA 8585** — COMPULSORY (no exam content choice)

## Psychology

- **Psychology AQA 8182** — COMPULSORY (no exam content choice)

## Economics

- **Economics AQA 8136** — COMPULSORY (no exam content choice)

## Statistics

- **Statistics AQA 8382** — COMPULSORY (no exam content choice)

## Astronomy

- **Astronomy Edexcel 1AS0** — COMPULSORY (the "select one from four answer choices" reference is multiple-choice question format, not content choice)

## Engineering

- **Engineering AQA 8852** — COMPULSORY for written exam. NEA brief has optional examples, but NEA is not the written exam and the spec content is the same for all students.

## Electronics

- **Electronics Eduqas C490QS** — COMPULSORY (no exam content choice)

## Geology

- **Geology Eduqas C180QS** — COMPULSORY (no exam content choice)

## Cambridge Nationals (vocational)

- **Enterprise & Marketing OCR J837** — COMPULSORY (3 mandatory units, no optional units; "choose one pricing strategy" is NEA task guidance, not exam content)
- **Sport Studies OCR J829** — COMPULSORY for written exam. Structure: R184 (mandatory written exam) + R185 (mandatory NEA) + 1 of {R186, R187} optional NEA. The optional units are NEA only — no written exam content choice.
- **IT OCR J836** — COMPULSORY (3 mandatory units, no optional units)
- **Sport Science OCR J828** — COMPULSORY for written exam. Structure: R180 (mandatory written exam) + R181 (mandatory NEA) + 1 of {R182, R183} optional NEA. Optional units are NEA only.

## **FLAG: Creative iMedia OCR J834**

> **FLAG: optional NEA unit (1 of 5) — R095 Characters & Comics / R096 Animation & Audio / R097 Interactive Digital Media / R098 Visual Imaging / R099 Digital Games**
>
> Mandatory units: R093 (written exam — Creative iMedia in the Media Industry) + R094 (NEA — Visual Identity & Digital Graphics). Then students/schools choose 1 of 5 optional NEA units.
>
> **Impact on platform:** Unity iMedia (23 lessons / 4 units) is school-bespoke and covers the units Unity chose. There is no free-tier iMedia build, so no generic coverage problem today. If a free-tier iMedia is ever built, it can only claim to cover R093 + R094 (the compulsory portion); the optional unit would need to be labelled per-choice.

## Music Technology

- **Music Technology NCFE 603/7008/7** — No spec file in repo. Cannot sweep. Unity-only subject, marked for removal Sept 2026. Treat as out of scope for this audit.

## **FLAG: Film Studies Eduqas C670QS**

> **FLAG: multiple school-chosen film texts per component**
>
> Component 1 (US Film): schools choose 1 pair from 5 pairs of mainstream films + 1 of 5 independent films.
> Component 2 (Global Film): schools choose 1 of 5 English-language films, 1 of 5 non-English films, 1 of 5 UK films.
> Component 3 (Documentary/Short/Silent + British film): further prescribed-list choices.
>
> **Impact on platform:** Free-tier Film Studies has 44 lessons built (Eduqas). This subject is inherently film-choice-dependent — like English Literature with set texts. Any lessons covering specific film analysis are only valid for students whose school chose those films. This is a known design trade-off (same as Eng Lit), not a pipeline error — but it is a genuine exam-content choice that users should be aware of.

## **FLAG: Drama AQA 8261**

> **FLAG: set-play choice from a list of 9 plays for Section B written exam**
>
> AQA Drama Section B (written exam): students answer questions on one set play chosen from: The Crucible, Blood Brothers, Noughts and Crosses, Around the World in 80 Days, Things I Know to be True, Romeo and Juliet, A Taste of Honey, The Great Wave, The Empress.
>
> **Impact on platform:** Unity Drama (bespoke) covers Blood Brothers + Rise Up — school-specific choice, fine. Free-tier AQA Drama has 85 lessons. If those lessons cover all 9 set plays, coverage is appropriate but broad. If they cover only specific plays, lessons are only relevant to students whose school chose those plays. Same structural issue as Eng Lit / Film Studies.

---

## Summary

| Subject | Verdict |
|---------|---------|
| Business (AQA/Edexcel/OCR) | COMPULSORY |
| Computer Science (OCR/AQA) | COMPULSORY |
| Combined Science AQA 8464 | COMPULSORY |
| Separate Sciences AQA 8461/8462/8463 | COMPULSORY |
| Mathematics AQA 8300 | COMPULSORY |
| Spanish / French / German AQA | COMPULSORY (in-exam prompt variants are not content choices) |
| Citizenship AQA 8100 | COMPULSORY |
| Health & Social Care Eduqas/OCR | COMPULSORY |
| Health & Social Care Pearson Edexcel | NOT SWEPT (no spec in repo) |
| Hospitality & Catering Eduqas | COMPULSORY |
| Food Preparation & Nutrition AQA | COMPULSORY |
| Psychology AQA 8182 | COMPULSORY |
| Economics AQA 8136 | COMPULSORY |
| Statistics AQA 8382 | COMPULSORY |
| Astronomy Edexcel 1AS0 | COMPULSORY |
| Engineering AQA 8852 | COMPULSORY (written exam content) |
| Electronics Eduqas | COMPULSORY |
| Geology Eduqas | COMPULSORY |
| Enterprise & Marketing OCR J837 | COMPULSORY |
| Sport Studies OCR J829 | COMPULSORY (written exam R184 only) |
| IT OCR J836 | COMPULSORY |
| Sport Science OCR J828 | COMPULSORY (written exam R180 only) |
| **Creative iMedia OCR J834** | **FLAG: 1 of 5 optional NEA units (Unity-only, no free-tier impact today)** |
| **Film Studies Eduqas** | **FLAG: school-chosen film texts per component (like Eng Lit set texts)** |
| **Drama AQA 8261** | **FLAG: 1 of 9 set plays for written exam Section B** |
| Music Technology NCFE | NOT SWEPT (no spec in repo; Unity-only, removing Sept 2026) |
