# Overnight build report — 2026-05-20

## TL;DR

**4 of 5 Eduqas subjects built through Phase 3 overnight. 101 article lessons in `pending_review`.**

| Subject | Spec | Lessons | Status | Local commit |
|---|---|---|---|---|
| Electronics Eduqas | C490QS | 20 | All inserted, pending_review | yes |
| Geology Eduqas | C180QS | 30 | All inserted, pending_review | yes |
| D&T Eduqas | C600QS | 22 | All inserted, pending_review | yes |
| CS Eduqas | C500QS | 29 (article only) | All inserted, pending_review | yes |
| Latin Eduqas | C580QS | — | Deferred (per your call: set-text rotation needs your input) | n/a |

**Nothing pushed.** All commits local on `platform`. Wizard wiring also deferred — Phase 2 created the Supabase rows (subjects, units, lesson shells) but did not touch `index.html`, `js/browse-loader.js`, or CSS. Subjects are findable via `/admin/review` and `/admin/build-status` but NOT via the student wizard yet.

---

## What you'll see in admin

### `/admin/build-status`
The four built subjects will now appear in the **Built** table. The to-build cards for Electronics / Geology / D&T / CS will still show — each family still has unbuilt boards (Edexcel/OCR/WJEC variants), but they no longer show the Eduqas variant as "to build" because the Supabase row exists. The notes you wrote earlier are still accurate for those remaining boards.

### `/admin/review`
101 new lessons in `pending_review` ready for your QA. Suggested review order if you only have time for a sample:
- Reference lesson per subject (typically L1 of unit 1) to confirm structural fit
- One lesson with heavy maths/equations from Electronics (e.g. "RC Time Delays and the 555 Monostable")
- The fieldwork-notice lesson in Geology (`investigative-geology-maps-fieldwork-and-practical-skills`)
- One material-area lesson in D&T (any of `papers-and-boards`, `natural-and-manufactured-timbers`, etc.)
- One Python code-block lesson in CS (any of `defining-algorithms-pseudocode-and-flowcharts`, `programming-constructs-and-subroutines`, `data-structures-arrays-records-and-file-design`)

---

## What's not done (in priority order for tomorrow)

1. **Latin Eduqas (C580QS)** — Plan exists at `scripts/_plan_latin-eduqas.json`. Plan flagged 3 gaps tied to set-text rotation: Components 2/3A/3B all have themes/texts that rotate every 2–3 years. Pick the right cycle to target before content generation. (E.g. for 2026 exams the set themes are Heroes and Villains / Come Dine with Me for Component 2; check Eduqas current set-text rotation.)

2. **CS Practice unit (Python Practice for the On-Screen Exam, 6 lessons)** — Practice-format generation uses a different factory pipeline (`docs/PRACTICE_PIPELINE.md`). The Supabase shell wasn't created for it during Phase 2 since `_activate_generic.py` only handles article_units. The plan lists this as `practice_units[0]`. Worth a separate session because the schema is heavier (input types, AI marking prompts, tier distribution).

3. **Wizard wiring (5 maps)** for the 4 built subjects — when you want them student-visible:
   - `index.html` `slugMap` (line ~3286)
   - `index.html` `freeSubjectMeta` (line ~1443)
   - `index.html` `boardConfig` (line ~1696)
   - `index.html` `FW_CATEGORIES` (line ~2084)
   - `js/browse-loader.js` `BASE_SLUG_BOARDS` (line ~99)
   Per `feedback_wizard_three_maps_in_lockstep` — all five must update together. Each subject needs an entry; status follows the established pattern (e.g. Electronics → STEM category; Geology → Sciences? probably; D&T → D&T category; CS → Computing & Digital).

4. **Phase 4 assets** — heroes, narration, podcasts, related media for all 4 subjects. Per `docs/PIPELINE.md` these parallelise per-lesson. Run with you watching because:
   - Related media URL audit pass is essential (~20% URL hallucination per memory)
   - Azure TTS narration runs sequentially per lesson and can hit rate limits
   - NotebookLM podcasts are manual (you do these)

5. **Phase 5 — revision technique guides** for the 4 subjects (templated; one agent per subject, fills in the 7 canonical technique files with subject examples).

6. **Phase 6 — verifier + fact-check** before any `live` flip:
   - `python scripts/_verify_subject_build.py electronics-eduqas` (and equivalents)
   - Fact-check probably low-priority for these subjects (Geology has named scholars but mostly settled; Electronics/D&T/CS are deterministic content — fact-check primarily catches RE/Eng Lit/History fabrications)

7. **WJEC aliases** — Electronics 3490QS, Geology 3180QS, D&T 3600QS, CS 3500QS are all true zero-content aliases (same dual-accredited spec for the first three; CS is regulator-boundary-only). Easy wires-only job after the Eduqas builds are wizard-wired.

---

## Remediation patterns applied across the 4 builds

Captured here so we can iterate the content prompts later if these recur on the next batch of subjects.

### HTML entities in plain-text fields (5 + 5 + 3 + 6 = 19 lessons affected)
Agents kept using `&Omega;` / `&deg;` / `&amp;` / `&lt;` in `practice_questions[].marks`. Fix script: `scripts/_fix_entities_in_text_fields.py <slug>` — decodes entities across all plain-text fields per CONTENT_PROMPT field rule. Should be added as a mandatory post-gen pass in the pipeline.

### "Component 1/2" code references (1 + 3 + 0 + 0 = 4 lessons)
Most common in Geology (3 lessons) — agents referenced "Component 2" for fieldwork/practical skills. Reworded to "the practical-skills component" / "the theory component". Worth adding to CONTENT_PROMPT.md ban-list explicit anti-examples.

### Single-word flashcard answers without W-question starters (6 lessons)
Pattern: agents wrote questions starting "The X is which Y?" / "A Z has W which?" — non-W starters that fail the FC validator when answer is single-word. Mechanical rephrase: invert clauses to lead with "Which / What / In which". The validator regex permits starters: `^(what|who|when|where|which|why|how|name|give|define|state|list|in (which|what))`. Worth adding this rule to FLASHCARD_RULES.md as a hard constraint with anti-examples.

### Enumeration in short flashcard answers (5 lessons)
Pattern: "X, Y and Z" in answers ≤12 words. Validator flags this — the rule is split into separate cards. Either rephrased the answer to a synthesis ("each combining…") or to one specific concept.

### Word count under 800 (4 lessons)
Mostly hit ~668–696 words. Pattern was content agents being terser than the lower bound. Extended each by adding a ~150-word section that links the lesson's concepts to broader CS / Geology / Electronics context. Worth tightening the content prompt to emphasise the 800-word floor more explicitly.

### "Level 1/2" descriptors (1 lesson, CS sorting)
The merge sort split-phase trace literally used "Level 1: [5,3] | [8,1]" / "Level 2: [5]|[3]|[8]|[1]". Validator's regex `\bLevel\s+[1-9]\b` is exam-board-level-descriptor focused but also catches this innocent use. Reworded to "Stage 1/2". Probably an edge case rather than a pattern to systematically prevent.

### Narration ID gaps (2 lessons, CS extensions)
Caused by my own extensions — I started new sections at n40 assuming continuity, but underlying max was n28/n19. Renumbered. Future remediation pattern: when extending content, query the highest existing narration ID first.

---

## What I committed locally (5 commits, none pushed)

```
6d26e45  Hospitality Eduqas alias + Unity-port fixes + Performing Arts excluded   (pre-overnight)
979046e  Film Studies: add WJEC as alias of Eduqas                                 (pre-overnight)
c59c4f8  build-status: split ALIAS tag into ALIAS vs PORT + add Business notes     (pre-overnight)
456503d  admin/build-status: expandable build notes on to-build cards              (pre-overnight)
[new]    Electronics Eduqas: Phase 3 build (20 lessons)
[new]    Geology Eduqas: Phase 3 build (30 lessons)
[new]    D&T Eduqas: Phase 3 build (22 lessons)
[new]    CS Eduqas: Phase 3 build (29 article lessons)
```

`git log --oneline platform ^origin/platform` to see the unpushed commits.

---

## Generic pipeline scripts now in place

These were written this session and may be useful for future Phase 3 builds:

- `scripts/_activate_generic.py <slug>` — Phase 2 activation from any `_plan_<slug>.json`
- `scripts/_prep_content_batches.py <slug>` — splits article_units into batch JSONs
- `scripts/_insert_generic.py <slug>` — patches lesson shells from `_content_<slug>/lessons/*.json`
- `scripts/_fix_entities_in_text_fields.py <slug>` — decodes HTML entities across plain-text fields

Each takes the subject slug as a single arg. All work off the plan JSON + activation report — no per-subject hardcoded settings.

---

## Sleep well, see you in the morning.
