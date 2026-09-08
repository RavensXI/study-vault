# Homepage v2 — responsive pass TODO (8 Sep 2026)

The landing page is a fixed 1835px painted canvas scaled by `fitScale()` (body zoom). Round 3 kept that model; everything below is what a proper reflow pass has to solve before launch. Verified on the 430px captures `_hp_430_p{0..2}.png` and the Playwright phone run (`_pw_r3.py`).

## Landing page (`welcome.html`)
- **Whole canvas scales down on phones** — at 430px the zoom is ~0.23, so the picker tiles, the tablet and the bookshelf are readable only with pinch-zoom. Needs a `max-width` reflow: one column of picker tiles, tablet full-bleed, bookshelf as 3–4 short shelves.
- **Snap is desktop-only** (fine pointer + ≥700px tall). On touch the page free-scrolls; the settle easing is also off there. Decide whether phones get sections at all or a plain stacked page.
- **Wings and props** (`@prop` tokens at both ends of every lower shelf) have no room below ~1100px canvas width; hide them under a breakpoint rather than letting them overlap the slot.
- **Tablet** is `flex:0 0 790px` with the caption list beside it; below ~1200px it should stack (tablet, then the five controls under it) and the iframe height clamp needs a phone floor (~420px).
- **Bookshelf catalogue** is two rows of 23 at `--bkh:190px` on a 1500px slot; on narrow canvases re-chunk into 3–4 rows (the renderer already takes `half`; make the row size a function of slot width) and drop the bookends below ~900px.
- **Boards panel** (`.catboards`) is absolutely centred with `min-width:520px`; on phones it should be a full-width sheet under the shelves.
- **Merged questions + schools shelf**: drawers (600px) + answer paper (380px) + notice (440px) only fit side by side; stack in that order under ~1300px.
- **Floor**: "Still scrolling?" call-to-action and the boards line are fine, but the footer skirting `background-size` should switch to `cover` on narrow widths.

## Embedded lesson (`lesson.html?embed=1`) — mostly done, two leftovers
- **Header title overlaps the wordmark at 390px** on the plain (non-embed) lesson page: `.header-lesson-title` sits on top of "StudyVault" (see `_pw_phone_dock.png`). Pre-existing on `platform`; fix in `css/style.css` header rules, not here.
- The a11y band now scrolls sideways as one row below ~720px (and always in embed). Check the scroll affordance on a real phone; add a fade at the right edge if it reads as clipped.

## Embedded workbook (`practice.html?embed=1`)
- The practice layout is `height:100vh` — inside the tablet that is the iframe height, which works, but on a phone reflow the tablet iframe should be at least 560px tall so the score bar and the answer box both fit.
- The first-visit method modal is suppressed in embed only; on the real phone page it still opens full-screen (by design).

## Verification hooks to keep
- `?snap&at=N` (pins page heights to the viewport for captures), `?pick=slug,slug` (pre-ticks), `_shots.py` (all shelves at 1440×900 / 1280×720 / 430), `_pw_r3.py` (the five controls, workbook swap, bookshelf, FAQ drawer, phone dock).
