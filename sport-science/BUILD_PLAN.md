# Sport Science (OCR Cambridge National R180) — Build Plan

One unit (R180: Reducing the Risk of Sports Injuries), 10 lessons.

- Body class: `unit-sport-science`
- Data attribute: `data-unit="sport-science-r180"`
- Theme colour: orange `#ea580c`

---

## R180: Reducing the Risk of Sports Injuries (exam unit, 40%)

| # | Title | Spec Ref | Status |
|---|-------|----------|--------|
| 1 | Extrinsic Factors | 1.1 | Built (hero, diagram, video) |
| 2 | Intrinsic Factors | 1.2 | Built (hero, diagram) |
| 3 | Warm Up Routines | 2.1–2.2 | Built (hero, diagram) |
| 4 | Cool Down Routines | 2.3–2.4 | Built (hero, diagram) |
| 5 | Acute Sports Injuries | 3.1 | Built (hero, diagram) |
| 6 | Chronic Sports Injuries | 3.2 | Built (hero, diagram) |
| 7 | Reducing Risk & Emergency Action Plans | 4.1 | Built (hero, diagram) |
| 8 | Treatment & Rehabilitation | 4.2 | Built (hero, diagram) |
| 9 | Medical Conditions: Asthma, Diabetes & Epilepsy | 5.1–5.3 | Built (hero, diagram) |
| 10 | Medical Conditions: SCA, Hypothermia, Heat Exhaustion & Dehydration | 5.4–5.5 | Built (hero, diagram) |

---

## Exam Technique Guides

Hub + 5 guide pages in `sport-science/exam-technique/`:

| Guide | Marks | File |
|-------|-------|------|
| Identify / State | 1–2 | `identify-state.html` |
| Describe | 3 | `describe.html` |
| Explain | 4 | `explain.html` |
| Extended response | 6 | `extended-response.html` |
| Discuss* (QWC assessed) | 8 | `discuss.html` |

## Revision Technique Guides

Hub + 7 guide pages in `sport-science/revision-technique/`:
- `retrieval-practice.html`, `spaced-repetition.html`, `dual-coding.html`, `knowledge-organisers.html`, `flashcard-drills.html`, `scenario-practice.html`, `timed-exam-practice.html`

---

## PPT Source Material

Located in `Spec and Materials/OCR Sport Science/` (untracked). Six topic folders:
- `1 Extrinsic factors/`
- `2 Intrinsic factors/`
- `3 Warm up and cool down/`
- `4 different types.../`
- `5 Reducing Risk.../`
- `6 causes.../`

---

## Diagram Approach

Uses the **pictorial isotype pipeline** (see `DIAGRAM_PIPELINE.md`):
1. Research agents found real citable data (peer-reviewed studies, NHS, Sport England)
2. Matplotlib baselines generated with orange palette (`#9a3412` → `#fb923c`)
3. Gemini pictorial isotype redesign (thematic icons matching each topic)
4. QC agent review — 7 of 10 images needed regeneration

Matplotlib backups stored as `*_matplotlib.jpg` (not committed to git).

---

## Still TODO

- TTS narration (narration player UI in place, empty manifests)
- YouTube videos for lessons 2–10 (L01 has one video)
- Related media curation for all 10 lessons (see `RELATED_MEDIA_PIPELINE.md`)
