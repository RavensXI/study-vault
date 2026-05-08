# Prose/Drama Audit Triage Summary

**Input:** `_prose_audit_consolidated.json` — 486 findings across 40 texts  
**Output:** `_prose_audit_fixlist.json` — same 486 records with `triage` + `triage_reason` fields

---

## Overall Counts

| Tier | Count | % |
|------|-------|---|
| `fix` | 214 | 44% |
| `borderline` | 112 | 23% |
| `noise` | 160 | 33% |
| **Total** | **486** | 100% |

---

## Per-Text Breakdown

| Text | fix | borderline | noise | Total |
|------|-----|-----------|-------|-------|
| A Christmas Carol | 2 | 3 | 2 | 7 |
| A Taste of Honey | 9 | 3 | 2 | 14 |
| An Inspector Calls | 8 | 0 | 2 | 10 |
| Animal Farm | 3 | 0 | 19 | 22 |
| Anita and Me | 13 | 16 | 8 | 37 |
| Blood Brothers | 6 | 4 | 10 | 20 |
| Boys Don't Cry | 10 | 0 | 2 | 12 |
| Coram Boy | 8 | 6 | 3 | 17 |
| DNA | 4 | 3 | 5 | 12 |
| Frankenstein | 4 | 3 | 0 | 7 |
| Great Expectations | 3 | 3 | 5 | 11 |
| Henry V | 2 | 3 | 2 | 7 |
| Hobson's Choice | 22 | 0 | 3 | 25 |
| Jane Eyre | 5 | 1 | 9 | 15 |
| Jekyll and Hyde | 5 | 3 | 1 | 9 |
| Journey's End | 8 | 3 | 1 | 12 |
| Julius Caesar | 1 | 1 | 6 | 8 |
| Leave Taking | 18 | 9 | 2 | 29 |
| Lord of the Flies | 2 | 2 | 5 | 9 |
| Macbeth | 2 | 2 | 1 | 5 |
| Much Ado About Nothing | 0 | 0 | 14 | 14 |
| My Name is Leon | 3 | 4 | 5 | 12 |
| Never Let Me Go | 4 | 3 | 2 | 9 |
| Oranges Are Not the Only Fruit | 4 | 2 | 3 | 9 |
| Othello | 3 | 1 | 1 | 5 |
| Pigeon English | 7 | 6 | 8 | 21 |
| Pride and Prejudice | 5 | 0 | 3 | 8 |
| Princess & The Hustler | 8 | 3 | 2 | 13 |
| Refugee Boy | 4 | 5 | 3 | 12 |
| Romeo and Juliet | 1 | 0 | 0 | 1 |
| Silas Marner | 3 | 1 | 1 | 5 |
| The Curious Incident (Eduqas) | 14 | 0 | 1 | 15 |
| The Empress | 5 | 4 | 2 | 11 |
| The History Boys | 6 | 0 | 2 | 8 |
| The Merchant of Venice | 4 | 4 | 4 | 12 |
| The Sign of Four | 2 | 2 | 1 | 5 |
| The Tempest | 2 | 0 | 1 | 3 |
| The War of the Worlds | 1 | 5 | 15 | 21 |
| The Woman in Black | 3 | 3 | 0 | 6 |
| Twelfth Night | 4 | 1 | 3 | 8 |

**Highest fix-density texts:** Hobson's Choice (22 fixes), Leave Taking (18), The Curious Incident/Eduqas (14), Anita and Me (13), Boys Don't Cry (10), A Taste of Honey (9), Journey's End (8), Princess & The Hustler (8), Coram Boy (8), An Inspector Calls (8).

**Texts that are mostly noise:** Animal Farm (19 noise / 3 fix — audit found mostly pre-verified accurate content), Much Ado About Nothing (14 noise / 0 fix — most entries lacked issue or canonical truth fields), The War of the Worlds (15 noise / 1 fix), Blood Brothers (10 noise), Jane Eyre (9 noise).

---

## Lesson-Level Breakdown

| Metric | Count |
|--------|-------|
| Lessons with ≥1 `fix` issue | **154** |
| Lessons with ≥3 `fix` issues (section rewrite / regen candidates) | **13** |
| Lessons with only `noise` / `borderline` | ~70 |

---

## Top 10 Most-Fix-Affected Lessons

| Fixes | Text | Lesson Title | Lesson ID |
|-------|------|-------------|-----------|
| 4 | Hobson's Choice | Context: Victorian Salford & Social Change | `98a51576` |
| 4 | Hobson's Choice | Acts 3-4: The Power Shift | `cc28ebbd` |
| 4 | Hobson's Choice | Character Analysis | `6ffaf9a9` |
| 4 | Leave Taking | Character Analysis | `dfc930cd` |
| 3 | Boys Don't Cry | Adam's Story: Coming Out | `b7a10772` |
| 3 | Boys Don't Cry | Character Analysis | `c81cefe5` |
| 3 | Coram Boy | Part 3: Discovery & Resolution | `26985264` |
| 3 | Hobson's Choice | Act 1: Hobson's World & Maggie's Plan | `9c4e5f72` |
| 3 | Jane Eyre | Gateshead & Lowood | `2fe05d71` |
| 3 | Journey's End | Act 1: Arrival in the Trenches | `c25f6db3` |

(Also ≥3 fixes: Pigeon English – The Ending `aad20898`, Princess & The Hustler – Act 1 `263021cb`, Curious Incident – Context `dc133c88`)

---

## Recommended Repair Scope

### Regen candidates (systemic fabrication / wrong primary text — all lessons in the unit need rebuilding)

These units have errors so deeply embedded across all lessons that surgical fixes would not be sufficient:

| Text | Problem | Lessons affected |
|------|---------|-----------------|
| **Hobson's Choice** (Edexcel) | 5+ fabricated direct quotations used throughout as key exam quotes. No canonical Maggie/Hobson/Willie lines verified against primary text. | All 7 lessons |
| **Leave Taking** (AQA + OCR) | Fabricated plot point (Enid's abandoned Jamaican child) pervades every lesson. Wrong character assigned pregnancy (Viv not Del). Wrong sister ages. | All lessons on both boards |
| **Boys Don't Cry** (Edexcel) | Josh's role as attacker inverted to supportive boyfriend throughout. Mother's death described as abandonment. Adam described as closeted when he is openly gay. | All 6 lessons |
| **The Curious Incident** (Eduqas) | All 8 lessons teach Haddon's novel when students study the Stephens play-text. Chapter structure, quotations, ending, narrator all from wrong text. | All 8 lessons |

### Section rewrite candidates (3+ fixes but regen may be disproportionate)

Lessons with 3-4 fixes where targeted section rewrites would be cheaper:

- Hobson's Choice L1 Context (`98a51576`) — premiere venue, date, character profession, unverified quote
- Hobson's Choice Acts 3-4 (`cc28ebbd`) — 4 fabricated quotes across narrative and flashcards
- Leave Taking Character Analysis — both boards (`dfc930cd`, `f0818d0e`) — abandoned child x3, wrong ages
- Jane Eyre Gateshead & Lowood (`2fe05d71`) — typhus/consumption dfn, Helen's death cause, internal contradiction
- Journey's End Act 1 (`c25f6db3`) — 3 quote errors (fabricated, misattributed, wrong act)
- Coram Boy Part 3 (`26985264`) — Meshak death inversion, Otis punishment, non-existent Part Three
- Pigeon English The Ending (`aad20898`) — killer identity (x3 instances)
- Princess & The Hustler Act 1 (`263021cb`) — Wendell absent at start, Lorna entirely missing, Wendell's criminal past

### Surgical fixes (1-2 fixes per lesson — most of the 156 lessons)

The remaining 143 lessons (156 - 13) have 1-2 fixes each. These are:

- Individual fabricated or misattributed quotes (An Inspector Calls, Frankenstein, Othello, Jekyll & Hyde)
- Specific plot errors (Animal Farm anthem, Great Expectations Miss Havisham, DNA cigarette placement)
- Biographical contextual facts (Golding/concentration camps, A Taste of Honey Delaney's age, Naoroji vote margin)
- dfn/glossary definition errors (Jane Eyre typhus/consumption)
- Wrong primary text signals (Curious Incident's 'I can do anything' declarative vs play's question form)

---

## Notes on Triage Decisions

**`borderline` is used sparingly (~22%)** for:
- Date ±2yr where both values are defensible (Coral Island 1857/1858, Delaney writing time 10 days vs 2 weeks)
- Salerio/Salarino where editions genuinely vary
- Character omissions that are relevant but not exam-critical (Osborne 'for England', Startop unnamed)
- Minor scene conflations that are unlikely to come up as exam extract triggers

**Much Ado About Nothing (14 noise / 0 fix)** — All 14 entries lack either an `issue` or `canonical_truth` field. There may be genuine findings here but the audit data does not contain enough context to classify them. Recommend a separate targeted audit of these lessons.

**Animal Farm (19 noise / 3 fix)** — The audit was thorough but found mostly pre-verified accurate content. The 3 fixes are real (anthem/commandments confusion, 'three days' vs 'three nights', Napoleon's poem placement).

**The War of the Worlds (15 noise / 1 fix)** — Most findings were low-severity paraphrase-level observations. The 1 fix (artilleryman's tunnel satire) is genuine. The rest are acceptable simplifications.
