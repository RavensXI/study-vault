# Component-Choice Audit: Media Studies, Music, PE, Sociology

Audit date: 2026-06-01
Auditor: Claude Code (read-only, no content modifications)

---

## (A) Media Studies — slug `media-studies-aqa` (8572)

### Are CSPs student/school chosen?

No. CSPs are **fully prescribed by AQA**. Each year AQA publishes a mandatory CSP booklet (downloaded from the secure AQA website on 1 June preceding the course start) that lists the exact products all students must study. Schools have zero choice over which CSPs to teach — every student in every school studies the same products. The exam questions in both Paper 1 and Paper 2 are written to those specific prescribed products.

The only "choice" in the spec is in the NEA (non-exam assessment): students pick one of five annually changing briefs set by AQA. NEA is not examinable article content.

### Built units

| Unit | Slug |
|------|------|
| Media Audiences | `media-audiences` |
| Media Industries | `media-industries` |
| Media Language | `media-language` |
| Media Representations | `media-representations` |

These four units map directly to the four components of the theoretical framework (spec sections 3.4–3.7). All examinable content is covered. No component choice exists in the written papers.

### Verdict

**COMPULSORY** — CSPs are AQA-prescribed annually; no student/school choice in the written papers. No picker needed. The four theory-framework units cover 100% of written exam content. NEA (brief choice) is non-examinable and not relevant to content lessons.

---

## (B) Music — slug `music-aqa` (8271) and `gcse-music` (Eduqas C660U/C660QS)

### AQA Music 8271 — slug `music-aqa`

**Component 1 (40% — written exam) has student choice in Section B.**

The written exam has two sections:
- **Section A (Listening):** Eight questions covering ALL four Areas of Study with unfamiliar music. No choice — students must answer all.
- **Section B (Contextual/Study Pieces):** Four question sets, one per Area of Study 1–4. Students must answer **two sets — one of which must be Area of Study 1 (Western Classical 1650–1910, compulsory), and one freely chosen from AoS 2, 3, or 4.**

The three choosable options are:
- Area of Study 2: Popular Music (study piece: Queen — Bohemian Rhapsody / Seven Seas of Rhye / Love of my Life, from 2026)
- Area of Study 3: Traditional Music (study piece: Esperanza Spalding — I Know You Know / Little Fly / I Adore You, from 2026)
- Area of Study 4: Western Classical Tradition since 1910 (study piece: Bartók — Hungarian Pictures movements 1,2,4,5, from 2026)

Components 2 (Performing) and 3 (Composing) are NEA. Performing repertoire is freely chosen by student/teacher; Composition 1 brief is externally set with four options. Neither creates examinable content units.

**Built units:**
- Score Reading (4 lessons)
- Area of Study 1: Western Classical Tradition 1650–1910 (8 lessons)

**Missing:** AoS 2 (Popular Music), AoS 3 (Traditional Music), AoS 4 (Western Classical since 1910). Students must study AoS 1 plus exactly one of AoS 2–4 for Section B. Since there are three valid options and schools/students choose one, all three need to be built so the platform covers each possible option.

### Eduqas Music C660U/C660QS — slug `gcse-music`

`gcse-music` exists only as a **school-specific row** (Unity College, school_id set). There is no free-tier generic `gcse-music` or `music-eduqas` slug in Supabase.

The Eduqas spec (C660QS) written exam (Component 3: Appraising, 40%) has **eight compulsory questions, two on each of the four Areas of Study.** All four areas are compulsory — there is no student choice in the written exam. The two "prepared extracts" (Badinerie Bach for AoS 1, Africa by Toto for AoS 4) are fixed for all students.

The NEA (Components 1 and 2 — Performing and Composing) involves choice of repertoire and choice of one composition brief from four, but these are not examinable article content.

The Unity-bespoke `gcse-music` appears to have 26 lessons / 6 units already built (per CLAUDE.md). No free-tier Eduqas Music subject exists to audit.

### Verdicts

- **`music-aqa` — MISSING-PICKER / PARTIAL-BUILD:** Section B requires AoS 1 (compulsory) plus one of AoS 2/3/4 (student-chosen). Only AoS 1 + Score Reading are built. AoS 2, 3, and 4 are missing entirely. A subject-level option picker for Areas of Study 2–4 is needed, or all three should be built as units and a picker added so students select which AoS they are studying.
- **`gcse-music` (Unity school-specific) — COMPULSORY:** Written exam has no student choice — all four AoS compulsory. No picker needed. (Free-tier Eduqas Music does not exist in Supabase.)

---

## (C) Physical Education — slugs `physical-education-aqa`, `physical-education-edexcel`, `physical-education-ocr`

### AQA PE 8582

Written papers (60% total):
- **Paper 1 (30%):** Applied anatomy and physiology, Movement analysis, Physical training, Use of data — all compulsory, answer all questions.
- **Paper 2 (30%):** Sports psychology, Socio-cultural influences, Health/fitness/wellbeing, Use of data — all compulsory, answer all questions.

No student choice in either written paper. The spec lists two theory units in the content table of contents: "The human body and movement" and "Socio-cultural influences and wellbeing."

NEA (40%): Practical performance in three physical activities. Students choose which sports/activities to perform. This is non-examinable practical assessment — not article content.

**Built units:**
- The Human Body and Movement (`human-body-and-movement`)
- Socio-Cultural Influences and Wellbeing (`socio-cultural-influences-and-wellbeing`)

Both written paper topics are covered. No picker needed.

### Edexcel PE 1PE0

Written papers (60% total):
- **Component 1 (30%):** Fitness and Body Systems — all compulsory.
- **Component 2 (30%):** Health and Performance — all compulsory.

No student choice in written papers. NEA (40%): Practical Performance (Component 3) and Personal Exercise Programme (Component 4) — student chooses activities, non-examinable.

**Built units:**
- Fitness and Body Systems (`fitness-and-body-systems`)
- Health and Performance (`health-and-performance`)

Both written paper topics covered. No picker needed.

### OCR PE J587

Written papers (60% total):
- **J587/01 (30%):** Physical Factors Affecting Performance — compulsory.
- **J587/02 (30%):** Socio-Cultural Issues and Sports Psychology — compulsory.

No student choice in written papers. NEA (40%): Practical Performances (J587/04) and Analysing & Evaluating Performance (J587/05) — student/school chooses sport activities, non-examinable.

**Built units:**
- Physical Factors Affecting Performance (`physical-factors-affecting-performance`)
- Socio-Cultural Issues and Sports Psychology (`socio-cultural-issues-and-sports-psychology`)

Both written paper topics covered. No picker needed.

### Verdicts

- **`physical-education-aqa` — COMPULSORY:** Written papers have no student choice. Only optionality is NEA practical activities (non-examinable). Both theory units built. No picker needed.
- **`physical-education-edexcel` — COMPULSORY:** Same as AQA. Both theory units built. No picker needed.
- **`physical-education-ocr` — COMPULSORY:** Same pattern. Both theory units built. No picker needed.

---

## (D) Sociology — slugs `sociology-aqa` (8192) and `sociology-eduqas` (C200QS)

### AQA Sociology 8192

Two written papers (50% each), both fully compulsory:
- **Paper 1:** Sociology of Families and Education (+ relevant research methods and theory)
- **Paper 2:** Sociology of Crime and Deviance and Social Stratification (+ relevant research methods and theory)

Each paper has Section A and Section B but both require answers to all questions (multiple choice + short/extended responses) — no optional topic choice within or between papers.

**Built units:**
- Studying Society & Research Methods (`studying-society-research-methods`)
- The Sociology of Families (`families`)
- The Sociology of Education (`education`)
- The Sociology of Crime and Deviance (`crime-deviance`)
- The Sociology of Social Stratification (`social-stratification`)

All five units cover the complete spec. No picker needed.

### Eduqas Sociology C200QS

Two written components (50% each), both fully compulsory:
- **Component 1:** Key concepts & cultural transmission, Families, Education, Research Methods
- **Component 2:** Social differentiation & stratification, Crime and deviance, Applied research methods

All questions in both components are compulsory (mix of short answer, structured and extended-response). No optional topic choice in either component.

**Built units:**
- Cultural Transmission & Research Methods (`cultural-transmission-research-methods`)
- The Sociology of Families (`families`)
- The Sociology of Education (`education`)
- Social Differentiation and Stratification (`social-differentiation-stratification`)
- Crime, Deviance and Applied Research (`crime-deviance`)

All five units cover the complete spec. No picker needed.

### Verdicts

- **`sociology-aqa` — COMPULSORY:** No student choice in written exams. All five content areas built. No picker needed.
- **`sociology-eduqas` — COMPULSORY:** No student choice in written exams. All five content areas built. No picker needed.

---

## Summary Table

| Slug | Verdict | Notes |
|------|---------|-------|
| `media-studies-aqa` | **COMPULSORY** | CSPs prescribed by AQA annually, no school/student choice. All 4 theory-framework units built. |
| `music-aqa` | **MISSING-PICKER / PARTIAL-BUILD** | Section B requires AoS 1 (compulsory) + 1 of AoS 2/3/4 (student choice). Only AoS 1 + Score Reading built. AoS 2, 3, 4 are missing. Needs picker + 3 missing AoS units. |
| `gcse-music` (Unity) | **COMPULSORY** | Eduqas written exam has no choice — all 4 AoS compulsory. Unity bespoke build complete. No picker needed. |
| `physical-education-aqa` | **COMPULSORY** | Written papers fully compulsory. Only optionality is NEA practical activities (non-examinable). Both theory units built. |
| `physical-education-edexcel` | **COMPULSORY** | Same pattern. Both theory units built. |
| `physical-education-ocr` | **COMPULSORY** | Same pattern. Both theory units built. |
| `sociology-aqa` | **COMPULSORY** | No choice in either paper. All 5 units built. |
| `sociology-eduqas` | **COMPULSORY** | No choice in either component. All 5 units built. |

---

## Action Required

**`music-aqa` only.** Three units need to be built and a picker wired:

1. Area of Study 2: Popular Music (study piece: Queen from 2026)
2. Area of Study 3: Traditional Music (study piece: Esperanza Spalding from 2026)
3. Area of Study 4: Western Classical Tradition since 1910 (study piece: Bartók from 2026)

Implementation options:
- **Option A (preferred):** Build all three AoS units. Add a school/subject-level picker (similar to tier picker) so students select which AoS 2–4 they are studying, hiding the other two. Or simply build all three and let teachers/students navigate to the relevant one.
- **Option B:** Build all three units without a picker — students see all three and use the relevant one. Simpler but risks confusion.

Note: Study pieces changed in 2024 (first assessed 2026). Content currently covering only AoS 1 uses the 2024+ cohort's study piece (Beethoven Symphony No.1 mvt 1).
