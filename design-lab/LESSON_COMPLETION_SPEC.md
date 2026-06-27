# Lesson completion model — spec

Replaces the all-or-nothing "do everything" gate with a **weighted model** that nudges students toward at least one high-value activity per lesson, while leaving an escape hatch. Agreed with Tom, 27 Jun 2026.

## Activities & weights (standard article lesson)

| Activity | Weight | Rationale |
|---|---|---|
| **Practice exam question** | **40** | The grade-mover (AI-marked, exam-authentic). High value. |
| Flashcards | 15 | Spaced retrieval |
| Revision task | 15 | Active processing |
| Quick quiz (5 KCs) | 10 | Light retrieval |
| Video | 10 | Passive — low value |
| Podcast | 10 | Passive — low value |
| **Total** | **100** | |

**Pass threshold = 50%.** Below 50 = in progress; ≥50 = "done" (counts in the dashboard's done totals). The bar keeps filling to 100% to show *depth* ("fully explored").

## The needle (why these numbers)

Three requirements and how the weights satisfy them:
1. **Exam question alone shouldn't pass** → `E (40) < T (50)`. ✓ Forces "exam + something else."
2. **Exam + any one other passes** → `E (40) + smallest other (10) = 50 ≥ T`. ✓ (so every non-exam activity is ≥10.)
3. **The exam-averse can still finish via the others** → `sum(non-exam) = 60 ≥ T`. ✓

Net effect: doing the **exam question + one quick thing (2 activities)** is the *shortest* path to done, so the architecture makes the high-value choice the path of least resistance — no nagging. A student who does everything *except* the exam question caps at 50% (just scrapes done), honestly signalling they skipped the thing that matters most.

General rule for tuning: keep total = 100, `E < 50`, every other ≥ `(T − E)`, and `sum(non-exam) ≥ T`.

## Normalisation (lessons that don't have every activity)

Completion% = **(sum of completed weights) ÷ (sum of *available* weights) × 100**, with the threshold at 50% of available. So:
- **Practice-first lessons** (Maths, MFL, Eng-Lang, science calc units): the practice question *is* the lesson → 100% on completion, no escape hatch needed.
- A lesson genuinely missing one activity rescales cleanly; the same relative shape holds.

## Architecture / what's needed to build it

- Per-student, per-lesson, **per-activity** completion records (right now only visits + `knowledge_check_scores` are captured; "did the exam question / task / watched video / heard podcast" is not). New schema + lesson-page wiring.
- This is the **same tracking** that makes the dashboard's Guided plan and "what's fading" genuinely smart (last-seen + which activities done), so it pays off twice.
- The lesson template's progress bar reads the weighted %; the dashboard's per-subject/per-unit progress and the "Your progress" constellation read aggregate done-counts off the threshold.

## Not building (decided)
- No knowledge graph / prerequisite sequencing (that's for teaching-from-scratch; this is revision). See `project_dashboard_two_door`.
- Spaced repetition stays simple (last-seen, oldest-first), not a full SRS engine.
