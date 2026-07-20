# Geography Skills practice: guided rebuild (20 Jul 2026)

All 12 Geography Skills lessons converted to the guided-learning format already
shipped across maths (192) and the science calculations (60), plus the
map-first player layout. **72 rows live** (12 lessons × 6 subjects: AQA,
Edexcel A, Edexcel B, OCR, Eduqas, and Unity's `geography`).

## What was actually wrong

Four things, all verified rather than assumed:

1. **292 catch-all misconceptions.** Every one used `check: "wrong"`, so it
   fired on *any* wrong answer. This is the same bug Tom hit in maths in July:
   students get told they made a mistake they did not make. Worse, several
   stated the answer outright. L11 bronze[0]'s message read *"They are both in
   grid square 8332"* — which is the answer.
2. **No guided format at all.** No opener, no teach walks, no completion
   problem, no rescue walks, no tier guides. The section still had the
   up-front method card Tom rejected for maths ("no student will read that").
3. **The map was marooned.** Geography Skills is the one subject where the
   stimulus *is* the question, but the player gave it half the split and
   centred it in a taller panel, so a wide OS map rendered 508×431 with ~220px
   of dead space above it. It also carried `cursor: zoom-in` with no click
   handler, advertising a zoom that never happened.
4. **The section stops at L12.** Contours and map interpretation, the two
   hardest OS-map skills, have never existed.

A fifth suspicion turned out to be **wrong** and is worth recording: I expected
many problems to reference a figure they did not carry. Only 3 of 240 do, and
those describe their data in words. No work was needed there.

## What was done

**Content** — 12 authoring agents, each with an independent adversarial
checker, against a spec written for this subject
(`scratchpad/_geo_guided/SPEC_GEOGRAPHY.md`). Its geography-specific rules:
the stimulus is sacred (never dropped, never an invented URL), **every walk
opens by LOCATING the student on the map or chart before reading any value**,
multiple choice gets walks too (41% of the bank), and no message may state the
answer.

- **75+ problems repaired**, **516 misconceptions** now all `expect`-matched,
  so a diagnosis only ever fires on the answer that error actually produces.
  Zero catch-alls survive.
- Every lesson gained an opener, three teach walks, three tier guides, tier
  descriptions (geography had none), and walks on 228 of 240 problems. The 12
  without are purely evaluative multiple choice carrying `guided_skip_reason`.
- Openers are concrete and drawn: a pizza cut into quarters, a queue of eight
  people split four ways, five friends' pocket money where one gets £100, a
  multi-storey car park for grid references, two towns as circles for
  proportional symbols. All as inline SVG, so nothing is claimed that is not
  shown.

**Player** (`practice.html`):
- Map-first layout: the stimulus column widens to 62% when a map is showing,
  map and zoom affordance centre as one group, `object-fit: contain` so a map
  is never cropped. Measured in headless Chrome: **508×431 → 623×528**, 1.5×
  the visible area, grid squares legible.
- Wired the existing lightbox to the map and added "Tap the map to enlarge".
- The completion problem now fires on the tier's **first walk-capable**
  question instead of strictly index 0. When the shuffle dealt an evaluative MC
  first, the completion step was skipped for that tier entirely. This also
  fixes `maths-edexcel/algebra/13`, already known to skip it.

**L08 needed a human-equivalent judgement.** Two walks made contradictory
claims about the same point on `isotherm-uk.png`, which neither the author nor
the checker could see. I fetched and read it: it carries **only 4/6/8 degree
isotherms**, Q sits between 4 and 6 (=5), and P sits *south* of the 8 line with
nothing beyond it. So `bronze[2]` had invented a 10° line, estimated P as 9
from it, then "checked" that estimate against the same assumption; and
`silver[5]` had placed P between 6 and 8 to make its stored difference of 2
come out. P has no upper bound, so that difference is not determinate:
`silver[5]` is reposed to ask the *smallest possible* difference (3), which the
map does answer and which teaches that isolines give bounds, not exact values.

## Verification

- Validator PASS on all 12 (`_validate_geo.py` — adds answer-leakage
  detection, catch-all rejection, stimulus preservation, required tier
  descriptions). Run against the *old* L11 it reports 101 real defects.
- **228 walks machine-checked: every one lands on its stored solution.**
- Zero surviving `check:"wrong"` across all 12 lessons.
- Stimulus preservation audit: every image and chart present before is present
  now, no invented URLs. The only other field changes are em-dash removals my
  own style rule mandated.
- All 72 rows propagated and **re-read as byte-identical** to canonical. All 72
  were already identical before this work, Unity included, so no
  generic/school mixing was introduced.
- Full-journey headless driver **complete and green on L01, L04, L08, L11 and
  on `geography-ocr` and `geography-eduqas`**: opener with two doors and a hint
  on a wrong try, teach walk, pre-worked completion, lifeline correctly hidden
  on non-walkable MC and shown on walkable, wrong answer offering rescue, and
  the pre-answer walk opening without failing first.
- The remaining 8 (L02, L03, L05, L06, L07, L09, L10, L12) were driven as far
  as the completion card, all reached it, and **none logged a failure** — they
  ran out of the driver's virtual-time budget mid-journey rather than breaking.
  So all 12 are confirmed to boot, run the opener, run the teach walk and deal
  a pre-worked completion problem; 4 are confirmed end to end.

## All 12 adversarially checked

The first fan-out hit the session limit before L03, L09 and L12 could be
checked. They were checked and repaired in a second pass once usage reset, and
**all three now pass**. Those checkers did the thing the first round could not:
they **fetched and pixel-measured the actual images**.

- **L09** measured every circle diameter on `proportional-symbol-uk.png`
  (London 91px, Birmingham 31px, key circles 87/43/21…) and the perpendicular
  shaft widths on `flow-line-uk.png` against its key (3px=15k, 5px=30k,
  10px=60k), then zoomed the London node to count which arrowheads terminate
  there. Every stored answer confirmed against measurement, no invented feature.
- **L12** downloaded all 9 OS map extracts, measured the grid spacing on each,
  located every named feature in pixels, and re-derived every compass bearing
  and ruler distance through the actual readout formula in `practice.html`.
- **L03** decoded the four inline SVGs pixel by pixel rather than trusting
  their prose, and found one stored answer (silver[1]) that was reachable by no
  method: 40 corrected to 39 (least squares gives 38.15, neighbour midpoint
  38.5).

Final state across all 12: **240 problems, 228 walks, 516 misconceptions, zero
surviving `check:"wrong"`, zero walk-landing failures.** The 12 problems without
walks are purely evaluative multiple choice carrying `guided_skip_reason`.

## L13 and L14 built (21 Jul, overnight)

The section stopped at L12 and had never covered contours or whole-map
interpretation. Both now exist, built to this same guided spec:

- **L13 Contours & Relief** — contour interval, spacing as gradient, spot
  heights, landform shape, height at a point, gradient in m per km at gold.
- **L14 Map Interpretation** — land use from symbols, settlement site and
  shape, relief and drainage, evidence-based judgement at gold.

20 problems each (8/7/5) and **every problem is walkable (20/20)**, better
coverage than the original twelve. Zero catch-all misconceptions, zero
walk-landing failures, units on measured quantities and on no multiple choice.

Built from the 14 OS sheets no lesson was using. The checkers verified map
facts from pixels: the 10 m contour interval confirmed on every sheet by
scanning for four thin lines between index contours, Worsaw Hill's 200 m ring
confirmed to contain two closed rings, square 9073 measured at zero contour
pixels against a neighbour's 1189.

One confirmed defect, repaired: an L13 walk note claimed a contour gap spanned
"most of a square"; measured, the grid is 713 px per km and the gap is 19-39 px,
about a eighteenth. The stored answer and box values were right, only the
description overstated.

**Status: `pending_review` on all six variants.** Admins see them with a preview
banner, students cannot. `scratchpad/_geo_guided/_publish_l13_l14.py --publish`
flips status and `units.lesson_count` together (browse lists live lessons but
labels from lesson_count, so the two must move as one); `--unpublish` reverses.

Preview (logged in as admin):
- https://study-vault-git-landing-wizard-tom-shauns-projects.vercel.app/practice/geography-aqa/geographical-skills/13
- https://study-vault-git-landing-wizard-tom-shauns-projects.vercel.app/practice/geography-aqa/geographical-skills/14

## Outstanding

1. **L04 teach pyramids** are captioned "% of total population" but their bars
   sum to 53% and 55%. Flagged by the checker, not fixed.
2. **Pre-existing chart defects, inherited not introduced**: L04 bank pyramids
   total 125.8%, 109.3% and 118.5%; `flow-line-uk.png`'s key reads
   "thousands/yr" but its reference labels read 15,000/30,000/60,000.
3. **L11 wording**: two problems shared the answer 4016; `silver[1]` ("the
   water close to Chaigley Hall") and `gold[4]` ("nearest education facility")
   depend on judging by eye.
4. **L13 Contours / L14 Map Interpretation still do not exist.** Note the
   memory claim that "contour assets are on R2 ready" is **wrong** — R2 holds
   31 objects under `geography/os-maps/`, all plain OS tiles, no contour
   overlays. They are still buildable: 9 upland maps (Snowdonia, Dartmoor,
   Lake District, Greenhead Gill, Pendle Hill…) show contours natively and
   **8 of them are currently unused by any lesson**.
5. **None of this reaches a student until `landing-wizard` merges to
   `platform`.** Production still lacks the guided engine entirely.

## Files

- `scratchpad/_geo_guided/SPEC_GEOGRAPHY.md` — the brief
- `scratchpad/_geo_guided/_validate_geo.py` — deterministic gate
- `scratchpad/_geo_guided/_apply_checker_repairs.py` — the 10 hand repairs, each documented
- `scratchpad/_geo_guided/_propagate.py` — canonical → 5 variants, verified by re-read
- `scratchpad/_geo_guided/_geo_journey.html` — full-journey driver
- `scratchpad/_geo_guided/_maplayout_harness.html` — before/after map layout
- `scratchpad/_geo_audit/_pre_dump_all.json` — rollback for all 72 rows
