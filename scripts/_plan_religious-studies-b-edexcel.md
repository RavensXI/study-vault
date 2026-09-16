# Build plan — Pearson Edexcel GCSE Religious Studies B (1RB0), "Beliefs in Action"

Written 16 Sep 2026 by Claude (Fable) for execution by Opus agents through the Batch API.
Spec on disk: `specs/edexcel/religious-studies-b-1RB0.md` (Issue on file; 351k chars). Sister build to port
from: `religious-studies-edexcel` (Spec A, 1RA0, 71 lessons, 15 units, live). Register: 23,481 entries in
June 2025 (Pearson's own count), more than 1RA0's 17,143. Value rank #1 on the remaining-builds page.

## 0. Guardrails that apply to this build (read before anything runs)

1. **Plan check against the sister subject (docs/PIPELINE.md, Phase 1).** Spec A's shape is
   Paper 1 religion / Paper 2 second religion / Paper 3 philosophy & ethics / Paper 4 textual.
   Spec B's shape is Area of Study 1 / Area 2 OR Area 3, each = one religion × four sections.
   No NEA exists. **No exam-technique unit or guide pages** (retired). Exam technique goes into each
   lesson's `exam_tip_html` only.
2. **Spec is the source.** RS has no set products; the spec's numbered content points per section
   (e.g. "2.1 Marriage…", "4.3 Euthanasia…") are the authority. Every lesson prompt carries the
   verbatim spec text of the section(s) it teaches as `section_markers`; the fact-check runs with
   `factcheck_search_max: 0` and **`assessment_rules_doc` set to the spec's assessment section**
   (the Media rebuild's fact-check ran without it and called true exam facts "fabricated" — the
   runner must refuse to fact-check without it).
3. **Never name the board** in student text ("the exam board"). Use the site's "Mastering / Secure /
   Developing / Emerging" band ladder, never Pearson level descriptors, never the paper codes.
4. **Budget: $16.45 on the API console.** The ledger reads ~2× high, so stop launching new stages when
   `costs.jsonl` passes **$26 at batch list price**, and never start a stage whose estimate would cross
   it. Canary two lessons first (content → validate → fact-check) before the fleet.
5. **Nothing is "done" until it passes the standing checklist** in memory
   `feedback_verify_whole_student_experience`: rendered on desktop and phone, narration plays, KC/
   flashcards open, no `[object Object]`/`undefined`/`NaN`/raw entities/board names, media links live.

## 1. Exam structure (from the spec — put this text in `assessment_rules_doc`)

- Students sit **two papers**: Paper 1 = Area of Study 1 (Religion and Ethics) on one religion;
  Paper 2 = Area of Study 2 (Religion, Peace and Conflict) **or** Paper 3 = Area of Study 3
  (Religion, Philosophy and Social Justice) on a **different** religion (Catholic Christianity and
  Christianity count as the same religion for this rule).
- Each paper: written, 1 hour 45 minutes, 102 marks, 50%. Four questions (one per section), each in
  parts (a)–(d): (a) 3 marks Outline three; (b) 4 marks Explain two; (c) 5 marks Explain two with
  reference to a source of wisdom and authority; (d) 12 marks Evaluate a statement, with 3 SPaG marks
  on one (d) per paper. `question_type_names` = the same five as 1RA0:
  `['3 marks — Outline Three', '3 marks — Describe', '4 marks — Explain Two', '5 marks — Explain Two with Sources', '12 marks — Discuss a Statement']`.
- Sections per area (every religion option has the same four):
  - Area 1 Religion and Ethics: 1 Beliefs · 2 Marriage and the Family · 3 Living the … Life · 4 Matters of Life and Death.
  - Area 2 Religion, Peace and Conflict: 1 Beliefs · 2 Crime and Punishment · 3 Living the … Life · 4 Peace and Conflict.
  - Area 3 Religion, Philosophy and Social Justice: 1 Beliefs · 2 Philosophy of Religion · 3 Living the … Life · 4 Equality.
- Religion options: Area 1 and Area 2: Catholic Christianity, Christianity, Islam, Buddhism, Hinduism,
  Judaism, Sikhism. Area 3: Catholic Christianity, Christianity, Islam only.

## 2. Scope and phasing

**Phase 1 (this batch, ~22 lessons, ≈ $22 list / ≈ $11 real):** the two pairings almost every centre
takes.
- Route "state school": Area 1 **Christianity** + Area 2 **Islam**.
- Route "Catholic school": Area 1 **Catholic Christianity** + Area 2 **Judaism**.

**Phase 2 (later, on a top-up):** Area 1 Islam; Area 2 Christianity / Catholic; Area 3 (Christianity,
Catholic, Islam); Area 1/2 Buddhism, Hinduism, Sikhism. Unit slugs below are designed so Phase 2 adds
units without renaming anything.

## 3. Units and lessons (Phase 1)

Unit slug pattern: `area1-<religion>`, `area2-<religion>`, `area3-<religion>`. One lesson per spec
section, with the two heaviest sections split in two so every numbered content point gets real
coverage (Area 1 sections 1 and 4; Area 2 sections 1 and 4). Article format throughout (no practice
units). Lesson `section_markers` = the spec's numbered points for that section, quoted verbatim.

### area1-christianity — "Area of Study 1: Religion and Ethics (Christianity)" — 6 lessons
1. Christian Beliefs: the Trinity, Creation and the Incarnation (§1.1–1.4) ← transfer HIGH from `paper-1-christianity` L1
2. Christian Beliefs: the Last Days, Salvation, Eschatology and the Problem of Evil (§1.5–1.8) ← HIGH from `paper-1-christianity` L2–L3
3. Marriage and the Family (§2.1–2.8: marriage, sexual relationships, family, support for the family, family planning, divorce, equality of men and women, gender prejudice) ← MEDIUM from `paper-3-philosophy-ethics-christianity` L4–L5
4. Living the Christian Life (§3.1–3.8: worship, sacraments, prayer, pilgrimage, celebrations, the future of the Church, the local church, the worldwide Church) ← HIGH from `paper-1-christianity` L4–L5
5. Matters of Life and Death: Origins of the Universe, the Value of Life and Life After Death (§4.1–4.4) ← MEDIUM from `paper-1-christianity` L3 + fresh
6. Matters of Life and Death: Abortion, Euthanasia and Non-religious Arguments (§4.5–4.8) ← fresh

### area1-catholic-christianity — "Area of Study 1: Religion and Ethics (Catholic Christianity)" — 6 lessons
Same six shapes as above, ported from `paper-1-catholic-christianity` (L1–L6) and
`paper-3-philosophy-ethics-catholic` (L4–L5); Catholic specifics (Magisterium, natural law, the
sacraments as seven, Catholic teaching on contraception and euthanasia) come from the spec's Section
text for the Catholic option, not from the Christianity lesson.

### area2-islam — "Area of Study 2: Religion, Peace and Conflict (Islam)" — 5 lessons
1. Muslim Beliefs: the Six Beliefs, the Five Roots, the Nature of Allah, Risalah (§1.1–1.4) ← HIGH from `paper-2-islam` L1–L2
2. Muslim Beliefs: Holy Books, Angels, Akhirah and Predestination (§1.5–1.8) ← HIGH from `paper-2-islam` L2
3. Crime and Punishment (§2.1–2.8: justice, crime, good and evil actions, punishment, aims of punishment, forgiveness, treatment of criminals, the death penalty) ← fresh (spec text)
4. Living the Muslim Life (§3.1–3.8: Ten Obligatory Acts, Shahadah, Salah, Sawm, Zakah/Khums, Hajj, jihad, celebrations) ← HIGH from `paper-2-islam` L3–L4
5. Peace and Conflict (§4.1–4.8: peace, peacemaking, conflict, pacifism, Just War theory, holy war, weapons of mass destruction, issues surrounding conflict) ← fresh (spec text)

### area2-judaism — "Area of Study 2: Religion, Peace and Conflict (Judaism)" — 5 lessons
Same five shapes, Beliefs and Living ported from `paper-2-judaism` L1–L4; Crime and Punishment and
Peace and Conflict fresh from the spec's Judaism Section 2 and 4 text.

Total Phase 1: 22 lessons. Accents: reuse the 1RA0 unit accent family (#7c2d12 subject accent).

## 4. Subject row, options and gating

- New subject row `religious-studies-b-edexcel`, name "Religious Studies B", exam_board "Pearson Edexcel",
  spec_code "1RB0", school_id NULL, status live; lessons inserted at `pending_review`
  (feedback_freetier_inserts_at_live).
- `settings.options` in the same shape as 1RA0's (`paper1`/`paper2` with `choices`, `required`), renamed for
  this spec: `area1` (label "Paper 1 religion", choices = Phase 1: Christianity → `area1-christianity`,
  Catholic Christianity → `area1-catholic-christianity`) and `area2` (label "Paper 2 religion", choices:
  Islam → `area2-islam`, Judaism → `area2-judaism`), with the rule text "must be a different religion from
  Paper 1; Catholic and Christianity count as the same". No `paper3_map`/`paper4_map`.
- `question_type_names` as in §1. `has_exam_guides` false. Revision-technique guides: adapt the 9 from
  `religious-studies-edexcel` (the Media guide builder pattern, revision-technique only).

## 5. Wiring (the five wizard maps, in lockstep — feedback_wizard_three_maps_in_lockstep)

- `index.html`: `freeSubjectMeta` row; `boardConfig` for religious-studies gains an "Edexcel B (Beliefs in
  Action)" entry alongside Edexcel A, with the two pickers from §4 (model on the existing `'edexcel'`
  block at ~line 2293); `slugMap` `'edexcel b'` → `religious-studies-b-edexcel`; not tiered.
- `js/browse-loader.js` `BASE_SLUG_BOARDS` entry; `welcome.html` cover + `BOARD_OFFERS` + `WSUB.rs.edexcelb`;
  `dash-data.js` `SUBSLUG.rs` + `FIRSTUNIT`.
- `data/exam-dates-2027.json`: 1RB0 papers (Pearson 2027 final timetable; the RS entry may already carry
  the same dates as 1RA0 — check and add a `religious-studies-b` key if the dates differ).
- Register: add a line to `docs/PRESCRIBED_WORKS_REGISTER.md` (no rotating works; nothing to gate).

## 6. Pipeline sequence (mirror `scripts/api_build/run_media_eduqas.py`, new `run_rs_b_edexcel.py`)

plan (from this file + the 1RA0 catalog, `source_subject_slug` = `religious-studies-edexcel`) →
plancheck → activate → prep → CANARY (submit 2 lessons: area1-christianity L3 and area2-islam L5, the
two fresh shapes) → poll/validate → factcheck (rules doc, no web) → review the canary by hand → submit
the rest → poll → fix/pollfix → factcheck → applyfixes → insert → media (curated related media, then
`prune_media_lessons.py --ids … --apply`, every lesson ≥ 8 live items) → heroes (photographs, vision-gated;
`finder.used` seeded with every RS hero on all boards so no duplicates) → narrate → guides → gate/options
→ **verification pass** (§0.5) → report. Podcasts and explainers follow automatically after Tom flips.

## 7. Deliverables back to Tom

`scripts/_fact_check/religious-studies-b-edexcel.md` (findings + what was applied), the cost tally from
`costs.jsonl` (list and halved), the 22 lesson URLs on the local server, screenshots of two lessons on
phone, and a list of anything not built or not verified. Commit locally after each stage; never push.
