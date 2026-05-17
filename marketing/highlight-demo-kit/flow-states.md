# Highlight Mode — flow states

One section per visual state of the feature. Useful for Designer when generating frame-by-frame illustrations, carousel slides, or step-by-step screenshots.

---

## State 1 — Out of mode (resting)

What the student sees on a fresh lesson page.

* Lesson page is rendered normally (no shadow lift, plain `#faf8f5` background).
* Bottom-left: **single FAB** in subject-accent colour.
  * Icon: marker pen (SVG, currentColor white).
  * Label (desktop only): "Highlight mode".
* No popover, no modal, no cursor change.
* Bug-reporter FAB lives bottom-right at the same vertical position.

---

## State 2 — Entering mode

Student clicks the Highlight Mode FAB. Single transition frame.

* Article body (`#study-notes`) gains:
  * Solid white background (`#ffffff`)
  * Soft drop shadow lift `0 12px 40px -8px rgba(45,42,38,.25)`
  * Slight outward horizontal padding (the card extends ~20px past the original text margins, text doesn't move)
* FAB stack swaps: the single "Highlight mode" button is replaced by **two pill buttons** side-by-side:
  * `[ Lesson Highlights · 0 ]` (white count chip on dark pill, dimmed because there are zero highlights yet)
  * `[ × Exit Highlight Mode ]` (black pill, X icon + label)
* Cursor anywhere inside the article changes to a **marker-pen SVG cursor**, body coloured to match the currently-selected highlight (default yellow on first use).
* `::selection` colour inside the article matches the current highlight tone.

---

## State 3 — Dragging

Student is dragging a text selection across a sentence.

* Native text selection draws in the *light* tone of the current highlight colour (e.g. `#fef9c3` for yellow), not the browser default blue.
* Marker-pen cursor still visible.
* No popover yet.

---

## State 4 — Highlight commits (sweep animation)

Student releases the mouse / lifts finger. ~420ms beauty moment.

* The selected text gets wrapped in `<mark>` elements styled in the current colour.
* Each `<mark>` is initialised with `background-size: 0% 100%` and animates to `100% 100%` over 420ms with `cubic-bezier(0.4, 0, 0.2, 1)` — visually a **left-to-right colour wash**.
* Multi-line / multi-mark highlights stagger 45ms per mark (line 1 starts, line 2 joins 45ms later) so the reveal cascades down the paragraph.
* Cursor stays as marker pen.
* Native text selection is cleared as the sweep completes.

---

## State 5 — Popover open

Immediately after the sweep, the popover appears, anchored above the highlighted text.

* Card: white, `14px` radius, soft drop shadow, ~260px wide.
* Top row: **four circular swatches** (Yellow / Green / Pink / Blue), 28×28, with a 2px border ring around the currently-active colour.
* Middle: empty multi-line note textarea ("Add a note (optional)…").
* Bottom row, left to right: tiny bin icon (delete this highlight) → "Done" primary button.
* Note textarea autofocuses.
* Tapping any swatch live-updates the highlight tone *behind the popover* immediately.

---

## State 6 — Saved highlight (idle, in mode)

After Done is pressed, popover closes, highlight is saved.

* The text in the article stays marked in its chosen colour.
* If a note was added, a small dot appears at the end of the highlighted text (subtle indicator that "this highlight has a note").
* Lesson Highlights FAB count chip animates from `0` → `1` (or whatever the new total is).
* Article stays in the lifted/white state.
* Student is still in Highlight Mode and can keep highlighting.

---

## State 7 — Tapping an existing highlight

Student clicks/taps an existing highlight to edit it.

* Popover reappears anchored above that highlight, pre-filled with its existing colour and note.
* Bin icon is now visible (delete is available).
* Same edit affordances as State 5.

---

## State 8 — Mobile tap-to-start (no selection)

Mobile-only flow. Student is in Highlight Mode and taps a single word.

* That word gets a **dashed outline** (translucent border, 2px dashed in accent colour) — implemented as an absolutely-positioned overlay div, not a DOM mutation, so the text underneath is untouched.
* A pill banner appears at the top of the viewport: **"Now tap the last word to highlight"**.
* On second tap: the dashed outline + banner disappear, the highlight commits (sweep animation), popover opens. Same flow as desktop from here on.
* Tapping the same word twice cancels.

---

## State 9 — Lesson Highlights modal

Student clicks the bottom-left "Lesson Highlights" FAB.

* Bottom-sheet modal (mobile) or centred modal (desktop) slides up.
* Header: "My highlights" + a yellow "Print these notes" pill button + close ×.
* Body: a vertical list of every highlight on this lesson, each showing:
  * The highlighted text in its colour tone, with a saturated colour bar on the left edge.
  * The note below it (if any).
  * "Jump to" and "Delete" buttons.
* Print button takes the student to `/knowledge-organiser.html` with this lesson's highlights pre-loaded for printing.

---

## State 10 — Exit

Student clicks the X "Exit Highlight Mode" pill.

* Article body loses the lift / white background, returns to resting state.
* Cursor returns to default.
* FAB stack collapses back to the single "Highlight mode" button.
* Highlights stay on the page (greyed-out treatment removed, they look exactly as before — still tappable to re-edit).
