# English Literature — Coverage Audit
**Date:** 2026-06-01  
**Auditor:** Claude Code (read-only, no content modified)

---

## Method

For each slug: spec set-text lists extracted from official spec PDFs → picker config read from `index.html` `litTexts` object → built units queried live from Supabase (school_id IS NULL). Cross-referenced all three layers.

---

## 1. english-literature-aqa (AQA 8702)

### 1a. Spec choice groups

| Group | Count | Texts |
|-------|-------|-------|
| Shakespeare [pick 1 of 6] | 6 | Macbeth, Romeo & Juliet, The Tempest, The Merchant of Venice, Much Ado About Nothing, Julius Caesar |
| 19th-Century Novel [pick 1 of 7] | 7 | A Christmas Carol, Jekyll & Hyde, Great Expectations, Jane Eyre, Frankenstein, Pride & Prejudice, The Sign of Four |
| Modern Text [pick 1 of 12 active] | 12 active | **Drama:** An Inspector Calls, Blood Brothers, DNA, A Taste of Honey, Princess & The Hustler, Leave Taking; **Prose:** Lord of the Flies, **Telling Tales** (AQA Anthology), Animal Farm, Anita & Me, Pigeon English, My Name is Leon. _(Expired: Never Let Me Go last 2024; The History Boys last 2024; The Curious Incident last 2024)_ |
| Poetry cluster [pick 1 of 3 active] | 3 active | Power & Conflict, Love & Relationships, Worlds and Lives _(first exam 2025)_ |

### 1b. Picker offers

- Shakespeare (6): Macbeth, Romeo & Juliet, The Tempest, The Merchant of Venice, Much Ado About Nothing, Julius Caesar
- 19th Century Novel (7): A Christmas Carol, Jekyll & Hyde, Frankenstein, Pride & Prejudice, Jane Eyre, Great Expectations, The Sign of Four
- Modern Text (11): An Inspector Calls, Animal Farm, Lord of the Flies, Blood Brothers, Pigeon English, DNA, Anita and Me, A Taste of Honey, Princess & The Hustler, Leave Taking, My Name is Leon
- Poetry (3): Power & Conflict, Love & Relationships, Worlds and Lives

### 1c. Built units in Supabase (28 units total)

All 6 Shakespeare texts built (7–10 lessons each) ✓  
All 7 19th-C Novel texts built ✓  
11 Modern texts built — matching exactly what picker offers ✓  
3 Poetry clusters built ✓  
Plus: Unseen Poetry (4 lessons) — compulsory, correctly excluded from picker ✓

### 1d. Gaps identified

**MISSING FROM PICKER AND UNBUILT: "Telling Tales" (AQA Anthology)**  
The AQA spec lists "Telling Tales" (AQA Anthology, ed. Frank Cottrell Boyce) as an active prose Modern Text (no "Last exam" annotation). It does not appear in the picker and no unit has been built for it.

No other gaps found. Expired texts (Never Let Me Go, The History Boys, Curious Incident) correctly omitted.

### 1e. Verdict

**PARTIAL-BUILD** — 1 active spec text not offered or built: *Telling Tales*. All other 27 texts fully covered.

---

## 2. english-literature-edexcel (Edexcel 1ET0)

### 2a. Spec choice groups

| Group | Count | Texts |
|-------|-------|-------|
| Shakespeare [pick 1 of 6] | 6 | Macbeth, The Tempest, Romeo & Juliet, Much Ado About Nothing, Twelfth Night, The Merchant of Venice |
| 19th-Century Novel [pick 1 of 7] | 7 | Jane Eyre, Great Expectations, Jekyll & Hyde, A Christmas Carol, Pride & Prejudice, Silas Marner, Frankenstein |
| Post-1914 British [pick 1 of 12] | 12 | An Inspector Calls, Hobson's Choice, Blood Brothers, Journey's End, Animal Farm, Lord of the Flies, Anita & Me, The Woman in Black, The Empress, Refugee Boy, Coram Boy, Boys Don't Cry |
| Poetry anthology [pick 1 of 4] | 4 | Relationships, Conflict, Time and Place, Belonging |

### 2b. Picker offers

- Shakespeare (6): Macbeth, Romeo & Juliet, The Tempest, The Merchant of Venice, Much Ado About Nothing, Twelfth Night
- 19th Century Novel (7): A Christmas Carol, Jekyll & Hyde, Frankenstein, Pride & Prejudice, Jane Eyre, Great Expectations, Silas Marner
- Modern Text (12): An Inspector Calls, Animal Farm, Lord of the Flies, Blood Brothers, Hobson's Choice, Journey's End, Anita and Me, The Woman in Black, The Empress, Refugee Boy, Coram Boy, Boys Don't Cry
- Poetry (4): Relationships, Conflict, Time and Place, Belonging

### 2c. Built units in Supabase (29 units total)

All 6 Shakespeare texts built ✓  
All 7 19th-C Novel texts built ✓  
All 12 Post-1914 texts built ✓  
All 4 Poetry collections built ✓

### 2d. Gaps identified

None. All 29 texts built, all 29 texts offered in picker.

### 2e. Verdict

**OK** — 0 gaps. Full coverage of all 29 picker-offered texts. All match the spec.

---

## 3. english-literature-ocr (OCR J352)

### 3a. Spec choice groups

| Group | Count | Texts |
|-------|-------|-------|
| Shakespeare [pick 1 of 4] | 4 | Romeo and Juliet, The Merchant of Venice, Macbeth, Much Ado About Nothing |
| 19th-Century Novel [pick 1 of 6] | 6 | Great Expectations, Pride & Prejudice, War of the Worlds, Jekyll & Hyde, Jane Eyre, A Christmas Carol |
| Modern prose/drama [pick 1 of 6 active] | 6 active | Anita and Me, Never Let Me Go, Animal Farm, An Inspector Calls, DNA, Leave Taking _(expired: My Mother Said I Never Should, last exam 2023)_ |
| Poetry cluster [pick 1 of 3] | 3 | Love and Relationships, Conflict, Youth and Age |

### 3b. Picker offers

- Shakespeare (4): Macbeth, Romeo & Juliet, The Merchant of Venice, Much Ado About Nothing
- 19th Century Novel (6): A Christmas Carol, Jekyll & Hyde, Great Expectations, Pride & Prejudice, Jane Eyre, The War of the Worlds
- Modern Text (6): An Inspector Calls, Animal Farm, Never Let Me Go, Anita and Me, DNA, Leave Taking
- Poetry (3): Love and Relationships, Conflict, Youth and Age

### 3c. Built units in Supabase (20 units total)

All 4 Shakespeare texts built ✓  
All 6 19th-C Novel texts built ✓  
All 6 Modern texts built ✓  
All 3 Poetry clusters built ✓  
Plus: Unseen Poetry (6 lessons) — compulsory, excluded from picker ✓

### 3d. Gaps identified

None. All 19 text-based units built and offered.

### 3e. Verdict

**OK** — 0 gaps. Full coverage across all 19 picker texts. Expired text (My Mother Said I Never Should) correctly omitted.

---

## 4. english-literature-eduqas (Eduqas C720QS)

### 4a. Spec choice groups

| Group | Count | Texts |
|-------|-------|-------|
| Shakespeare [pick 1 of 6] | 6 | Romeo and Juliet, Macbeth, Othello, Much Ado About Nothing, Henry V, The Merchant of Venice |
| 19th-Century Prose [pick 1 of 6] | 6 | A Christmas Carol, Silas Marner, Pride & Prejudice, War of the Worlds, Jane Eyre, Jekyll & Hyde |
| Post-1914 Prose/Drama [pick 1 of 10] | 10 | Lord of the Flies, Anita and Me, Never Let Me Go, The Woman in Black, Oranges Are Not the Only Fruit, The Curious Incident (play script), A Taste of Honey, An Inspector Calls, The History Boys, Blood Brothers |
| Poetry anthology [single compulsory] | 1 | WJEC Eduqas Poetry Anthology (all 18 poems, no cluster choice) |

### 4b. Picker offers

- Shakespeare (6): Macbeth, Romeo & Juliet, The Merchant of Venice, Much Ado About Nothing, Othello, Henry V
- 19th Century Novel (6): A Christmas Carol, Jekyll & Hyde, Pride & Prejudice, Jane Eyre, Silas Marner, The War of the Worlds
- Modern Text (10): An Inspector Calls, Lord of the Flies, Blood Brothers, Anita and Me, Never Let Me Go, The Woman in Black, The History Boys, The Curious Incident..., A Taste of Honey, Oranges Are Not the Only Fruit
- Poetry (1): Poetry Anthology

### 4c. Built units in Supabase (24 units total)

All 6 Shakespeare texts built ✓  
All 6 19th-C Prose texts built ✓  
All 10 Post-1914 texts built ✓  
Poetry Anthology built ✓  
Plus: Unseen Poetry (7 lessons) — Eduqas has Unseen Poetry in exam; this unit is present and correct ✓

### 4d. Gaps identified

None. All 23 text-based units built and offered. Note: Eduqas Unseen Poetry is a separate exam section (Component 2 Section C) and is handled as its own unit — correctly present.

### 4e. Verdict

**OK** — 0 gaps. Full coverage across all 23 picker texts.

---

## Summary

| Slug | Verdict | Picker-offered-but-unbuilt | Spec-active-but-not-in-picker |
|------|---------|---------------------------|-------------------------------|
| english-literature-aqa | PARTIAL-BUILD | 0 | 1 (Telling Tales) |
| english-literature-edexcel | OK | 0 | 0 |
| english-literature-ocr | OK | 0 | 0 |
| english-literature-eduqas | OK | 0 | 0 |

**Total picker-offered-but-unbuilt: 0** (no picker offers a text without a built unit)  
**Total spec-active-but-missing: 1** ("Telling Tales" — AQA only, no picker entry and no unit built)

---

## Notes on memory-flagged placeholder content

Memory warns of "Eng Lit lessons with placeholder content_html" across boards. This audit did not directly inspect content_html values, but all units show lesson counts of 7–10 with `status=live` and 0 `pending_review`. The placeholder concern flagged in memory (`project_englit_placeholder_content.md`) relates to multi-board Eng Lit content where an agent templated sections (e.g. "Brontë's treatment of exam technique"). This needs a separate content-QA pass querying content_html for boilerplate phrases. The lesson-count/status layer is clean.

---

## Recommendations

1. **Build "Telling Tales" unit for english-literature-aqa** — AQA Anthology (ed. Cottrell Boyce), active set text, no "last exam" note in spec. Add picker entry with slug `telling-tales`. Estimated ~7 lessons.
2. **Run placeholder content audit** — search `content_html` across all four subjects for boilerplate phrases (e.g. "treatment of exam technique", "Brontë's treatment") to identify any unfinished lessons. See `memory/project_englit_placeholder_content.md`.
3. **AQA flashcard quality** — memory flags 74 of 214 AQA Eng Lit lessons have <8 flashcards (regex-generated, not AI). These are live but low quality. See `memory/project_englit_aqa_regex_regen.md`.
