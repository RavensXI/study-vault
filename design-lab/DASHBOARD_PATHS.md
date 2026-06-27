# Sketch learning-path dashboard

`dashboard-paths.html` — the path-driven student dashboard (replaces the canvas
constellation in `dashboard.html`). Built 27 Jun 2026.

Serve: `python design-lab/serve.py` → http://127.0.0.1:8901/design-lab/dashboard-paths.html
(constellation original still at `…/dashboard.html` for comparison).

## What it does
- **Drill-down:** Subjects overview → Topics (units) grid → winding **lesson path**.
  Subject → topic → lesson, exactly as briefed.
- **Left-rail navigator:** subjects accordion → unit rows; click a unit to jump
  straight to its path. The "select from the list" variant.
- **Continue card** drops you onto English Literature's path at the "up next" node.
- Breadcrumbs everywhere; brand / "All subjects" reset to the overview.
- Real lessons/units pulled live from Supabase for **SAM** (the 9-subject demo
  student defined in `STUDENT[]`), same data + `keep` filters as `dashboard.html`.

## Backdrops
Each unit's path sits on a bespoke **gpt-image-2 SKETCH** backdrop (Sketch = the
locked style). Files: `assets/path-bg-u-<subject>-<unit>.png`, indexed by
`_path_backdrops.json` (key `"<subjectSlug>/<unitSlug>"`). The path overlays the
empty central lane the prompts reserve; titles lift off the art with a paper halo.

Generate / regenerate:
- `python scripts/_designlab_sam_discover.py` → `scratch_sam_units.json` (SAM's units)
- `python scripts/_designlab_unit_backdrops.py [subject]` → 45-unit sketch set + manifest

### ⚠ Generation status (27 Jun) — 16 / 45 sketches done
The overnight batch hit the **OpenAI account billing hard limit** after 16 sketches.
Art-backed so far: **Maths (6), English Language (4), English Literature (5),
Combined Science · Biology Paper 1**. Still TODO (29): the rest of Combined
Science (Chem/Physics + Bio P2 base sketch), **History, Geography, Spanish,
Computer Science, Religious Studies**. Those units render cleanly with no backdrop
(graceful blank) until generated. To finish once the OpenAI limit is raised — the
generator skips existing files, so just re-run:
`python scripts/_designlab_unit_backdrops.py`

## Progressive fidelity (Tom's idea — see memory `project_progressive_fidelity_backdrops`)
The art is meant to **sharpen as you master a unit**: sketch (0–33%) → blueprint
(33–66%) → refined (66–99%) → photoreal (100%). The dashboard already picks a
unit's stage from its mastery (`autoStage`), falls back to sketch when a stage
isn't generated, shows the chosen stage as a pip, and offers a dev **fidelity
toggle** on the path (stages with no art are disabled).
- Proof: full 4-stage ladder on **Combined Science · Biology Paper 2**
  (`_designlab_fidelity_ladder.py`), plus Biology P1 photo + Chemistry P1 blueprint
  (`_designlab_stage_backdrop.py`) so Combined Science's topics grid shows the
  ladder for real (photo / blueprint / sketch by mastery).
- Full rollout (4 stages × every unit) is deferred — Tom said "doesn't need doing now".
