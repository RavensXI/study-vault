# How to build a lesson widget

Read this immediately before you write the code. `CONTRACT.md` says what the
host requires. This says what makes the thing good.

Every rule below came from looking at rendered output. The failures quoted are
real, from `builds/`. The things called good are in `js/lesson-widgets.js` and
`css/lesson-widgets.css` — three hand-built widgets that the owner accepted.
That file is the bar. Open it before you start.

---

## 1. The size budget

A widget opens in a **modal**. It gets about **560px of usable height** on a
laptop and a **360px minimum width** on a phone.

- At 900px wide: the whole widget is **560px tall or less**.
- At 360px wide: **640px tall or less**.
- **No internal scrolling. Ever.** Not on a pane, not on a list, not on a column.
- Check it: `root.getBoundingClientRect().height` at both widths.

This is the budget that is missed most often, so treat it as the first
constraint, not the last.

> The three hand-built widgets measure **456px, 486px and 506px**. That is the
> shape to copy.
>
> `_opus-insulate-to-target` computes to **~919px** at 800px wide: 73px header,
> 360px stage, 262px controls, 160px feedback. `_opus-match-the-minister`
> computes to **~861px**. Both are half again over budget, so a student meets
> them through a letterbox — the screenshot of the insulate widget shows the
> title, three lines of prose, and *not one control*.

Four things buy back the height:

**Four zones, maximum.** Title, stage, controls, caption. The house widgets use
exactly these (`widgetShell()`). The insulate widget uses seven across four
nested cards, and pays 4 × 24px in card padding alone for the privilege.

**One stage.** One diagram, one graph, one board. Not a house *and* a meter side
by side, each in its own card.

**No empty scaffolding.** Never render a placeholder for an answer not yet
given. `match-the-minister` draws eight dashed boxes reading the literal words
"empty slot" — **368px, 43% of the whole widget**, before the student has done
anything. Reveal a slot when it is filled, or lay the answers into the tile
they came from.

**Title only in the header.** No instruction paragraph. See rule 2.

---

## 2. The opening state must teach itself

**If you need a sentence of instructions, the design has already failed.** The
opening state must show the student what to do without them reading anything.

Before you write the markup, answer this: *what is the single most likely first
action of a bored 15-year-old?* Make that action work.

> In `match-the-minister` the most likely first action is clicking one of the
> descriptions — they are the interesting content. Doing so gets you
> `'Choose a name on the left first, then this tile.'` The most probable first
> gesture is a dead end that returns a telling-off. Either accept both orders,
> or make only one thing clickable at the start.

**Never state the answer in the framing.** The same widget opens with
*"Watch the traps: Cecil's patient paperwork is not Walsingham's secrecy, and
the Council only advised."* Descriptor d2 is "patient written memoranda"
(Cecil). Descriptor d8 is "it advised while the queen decided" (the Council).
The instructions hand over two of the eight pairs verbatim and signpost two
more.

**No scoreboard before the first move.** "Matched 0/8", "Mistakes 0" and an
empty progress bar are three pieces of furniture that say nothing yet.

---

## 3. DOM, SVG or canvas

Choose per element, not per widget. Mixing is normal.

**DOM with CSS grid/flex** — anything containing a sentence, any set of
choices, any tiles/cards/slots, any table of figures. Text must reflow and be
selectable. **Never paint a sentence into a canvas.**

**SVG** — a labelled diagram under roughly 50 elements that you update by
setting attributes: a house cross-section, a circuit, a map, a set of arrows.
It scales crisply, takes real `<text>`, and each part can be addressed.

**Canvas** — continuous or spatial things redrawn wholesale: a travelling wave,
a hydrograph, a graph, dozens of moving items. When you use canvas, mirror the
state into a visually hidden live region — see `.svw-sr` and the sorting
widget's `sr` paragraph, which keeps the bars followable without sight.

**Give sentences room to be sentences.** Any box holding prose gets **at least
32 characters per line**; aim for 45–75.

> `match-the-minister` lays its descriptions out with
> `repeat(auto-fill,minmax(155px,1fr))`. In the right-hand column that yields
> two tiles of about 145px, so a 93-character sentence —
> *"Weighed every option in patient written memoranda; John Guy called him 'the
> indispensable man'"* — wraps to six lines of roughly fifteen characters. That
> is the "text crushed into tiny boxes" complaint, exactly.

---

## 4. Controls

**A discrete choice is buttons. Never a slider.** If you can enumerate the
states, enumerate them on screen, and **put the trade-off in the label**.

> `_opus-insulate-to-target` uses `min="0" max="300" step="50"` for loft
> insulation — seven stops, each with a real price of £200 per 50mm. That is a
> menu wearing a slider's clothes. The student cannot see the options or the
> prices, only a handle. The wall and glazing choices in the same widget *are*
> buttons carrying cost and mechanism ("Cavity — trapped air · £600"), which is
> right; the loft should match them.

**A slider is only for a genuinely continuous quantity** where the intermediate
values mean something and you want the student to feel a trend: frequency,
amplitude, relief, land use. Label both ends in words (`'flat'` / `'steep'`,
`'permeable (chalk)'` / `'impermeable (clay)'`), as `slider()` does.

**Every control must visibly change something within 100ms.** A control that
moves no pixels is decoration — delete it or give it consequences.

**Every control needs a visible current value.** Sliders show the live number
next to the label; buttons show a selected state that is unmistakable at a
glance.

---

## 5. Getting it wrong has to be possible, and has to cost something

An interaction with no wrong answer teaches nothing. But a wrong answer that
costs nothing is worse: it turns into guess-until-green.

- **Check the endgame.** In `match-the-minister` each person locks at 2/2, so
  once three are full the remaining tiles have exactly one legal home. The last
  two "answers" are forced. Design so the final move still requires knowing
  something.
- **Check the search space.** In `_opus-insulate-to-target` only **6 of 42**
  combinations reach the target, and **every one of them requires double
  glazing**. The advertised trade-off is thinner than it looks. Enumerate your
  own state space and confirm there is a real decision in it.
- **A wrong attempt must leave something behind** — a narrowed field, a visible
  cost, a diagnosis. Not just an incremented counter.

---

## 6. Feedback teaches; it does not score

The caption is the teaching. It is always present, updates on every change, and
has a `min-height` so nothing jumps.

**Name the pattern, the mechanism, and what it means.** One to three sentences.

> Good — the hydrograph:
> *"Short lag time, steep rising limb, high peak — a **flashy hydrograph**.
> Water is racing over steep, impermeable, built-up ground straight into the
> river. **High flood risk.**"*
> It names the exam term, explains the mechanism, states the consequence.
>
> Good — the waves widget:
> *"Turn **frequency** up and the **wavelength shrinks** — the wave speed is set
> by the rope, so **v = f×λ** stays at 6 m/s (2.0 Hz × 3.0 m). Amplitude changes
> the **energy** the wave carries — not its speed."*
> It states the invariant, plugs in the live numbers, and pre-empts the
> misconception in the last clause.
>
> Bad — insulate: *"Not there yet: 493 W is still escaping. Cut about 193 W more
> to reach 85%."* Arithmetic. It never says why the roof leaks most, nor which
> measure buys the most watts per pound.
>
> Bad — match-the-minister: *"Correct — William Cecil. He served from the day
> Elizabeth became queen until his death in 1598."* The tile the student just
> clicked says "in office almost the entire reign". The reward for being right
> is a paraphrase.

**Wrong-answer feedback is diagnostic.** Say why that choice was tempting and
what separates it from the right one. "Not Walsingham" is a verdict; "Walsingham
bought secrets — this one is about surviving in office for forty years" teaches.

**No accuracy percentages.** Delete *"8 attempts, 0 mistakes — 100% accuracy."*
Nothing is being marked. Say what the student now knows.

**Label quantities like a teacher**, with symbol and unit: `Wavelength λ`,
`Period T`, `Wave speed v` → `6 m/s (fixed)`. That last parenthesis teaches the
invariant for free.

---

## 7. Never promise what the interaction cannot deliver

**Compute the reachable range before you write a word of prose.** Every claim in
the caption must be true of the states the controls can actually produce.

> `_opus-insulate-to-target` prints *"efficiency can get close to 100% but never
> reach it."* Its own best case — 300mm loft, insulated solid walls, double
> glazing — is **88.0%**. The text promises a ceiling the widget cannot approach.

**Derive the answer from the model; never hand-author it.** The sorting stepper
runs the real algorithm and records each comparison as it goes, so the animation
cannot drift from the algorithm. Do that. Hardcoded verdict thresholds rot:
`insulate-to-target.js` says *"close to the cheapest way"* when `cost <= 1150`,
a magic number that does not match its own optimum of £1125.

**Never decide success with a bare float comparison.**

> `hitTarget: efficiency >= TARGET` where `TARGET = 0.85`. The intended cheapest
> solution lands on **exactly** 300 W of loss, i.e. exactly 0.85 — it passes only
> because `(2000-300)/2000` happens to be exact in binary. Two lines later the
> same file computes the same threshold as `INPUT * (1 - TARGET)`, which
> evaluates to **300.00000000000006**. Two expressions for one number,
> disagreeing by 6e-14, and a student who does everything right sitting on the
> knife edge between them.

Compare in integers where you can (watts, marks, counts), otherwise use an
explicit epsilon — and **place the intended solution at least one control step
clear of the boundary** so the pass is unambiguous.

**Every figure defensible for GCSE**, and in the lesson's own vocabulary and
units. If the lesson says `g = 10 N/kg`, use 10.

---

## 8. House style

Read `css/lesson-widgets.css`. Match it.

**The widget is a white card on the warm page** — `background:#fff`,
`border:1px solid #e8e3db`, `border-radius:16px`, `padding:1.35rem`. The working
area inside it is the warm paper (`#faf8f5`, as `.svw-canvaswrap`).

> Both generated widgets invert this: the outer wrapper is `#faf8f5` with white
> cards inside, so the widget dissolves into the page and the only visible
> structure is a scatter of boxes. It reads as unfinished.

**Colour.** Ink `#2d2a26`, muted `#8d8880`, hairline `#e8e2d9`, paper `#faf8f5`.
The accent is `ctx.accent` — use it for the live data mark, the selected state
and one highlight, not for filling whole buttons. For "done", the house uses a
single muted green `#4f7d63`. **Do not invent a per-widget red/green alert
palette**; `#fdf1ef` panels with `#8e2f27` text are not this site. No coloured
left-border stripes, no gradients, no drop shadows on small elements, no emoji.

**Type.** Source Serif 4 for the title only, at 1.22rem. Inter for everything
else. Labels .78rem/600. Stats .8rem. Caption .88rem/1.5. All changing numbers
get `font-variant-numeric: tabular-nums` so they do not jitter.

**Buttons** follow `.svw-btn`: .82rem, weight 600, `padding:.5rem .95rem`,
`border-radius:10px`, 1px `#ddd7cd`, background `#faf8f5`. Selected is an ink
fill (`#2d2a26`, white text).

**Scope every selector under your own root class.**

> `insulate-to-target.js` ships `input[type=range] { ... }` unscoped. That
> restyles every range input on the lesson page, including the accessibility
> toolbar.

**Read the accent from your own node** (`getComputedStyle(root)`), not from
`documentElement` — two layers set `--accent` and they disagree.

---

## 9. Motion and lifecycle

- Respect `ctx.reducedMotion`: no autoplay, no transitions, no shake.
- **Never run a timer for decoration.** `_opus-insulate-to-target` runs
  `setInterval(..., 90)` forever to wobble three arrows — about 11 redraws a
  second, for the life of the page, whether or not anyone is looking. Animate
  only while something is genuinely playing, and stop when it stops. The waves
  widget's loop returns immediately when paused: *a paused widget costs nothing*.
- **Build the DOM once, then mutate it.** Do not `innerHTML = ''` and rebuild on
  every click. `match-the-minister` rebuilds four cards and eight buttons per
  interaction, which is why it needs a manual `focusKey` system to put keyboard
  focus back — and it still lands focus on the wrong tile, jumping to the first
  in the pool rather than staying where the student was.
- **One source of truth per piece of state.** The same widget stores its "wrong
  answer" flash in both a `shakeId` variable and DOM classes removed by a 620ms
  timer, so a re-render in that window re-reddens a tile that has moved on.

---

## 10. Self-check before you emit code

Answer all of these. Any "no" means edit before you output.

1. Measured height ≤ 560px at 900px wide and ≤ 640px at 360px wide, with no
   internal scrollbar?
2. Four zones or fewer, one stage, no placeholder boxes for unearned answers?
3. Would a student know what to do with the instructions deleted? (Now delete
   them.)
4. Does the most likely first click do something useful rather than scold?
5. Do the title and framing avoid giving away any answer?
6. Is every discrete choice a button whose label carries its trade-off, and every
   slider a genuinely continuous quantity with worded ends?
7. Does every control change something visible immediately?
8. Does every box of prose get 32+ characters per line at 360px?
9. Have you enumerated the state space, and is there a real decision in it — more
   than one route to success, and a way to be wrong that costs something?
10. Is every claim in the text true of the reachable range? (State the actual
    ceiling; do not say "approaches 100%".)
11. Is success decided on integers or an explicit epsilon, with the intended
    solution clear of the boundary by at least one step?
12. Does the caption name a mechanism and its consequence, in the lesson's own
    vocabulary — rather than report a score?
13. Does a wrong answer explain what distinguishes it from the right one?
14. White card on warm ground, house colours and type, accent used sparingly,
    every selector scoped, no invented alert palette?
15. No timer running for decoration; DOM built once and mutated; keyboard focus
    stays where the student left it?
