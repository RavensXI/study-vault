# How to build a lesson widget

Read this immediately before you write the code. `CONTRACT.md` says what the
host requires. This says what makes the thing good.

Every rule below came from looking at rendered output. The failures quoted are
real, from `builds/`. The things called good are in `js/lesson-widgets.js` and
`css/lesson-widgets.css` — three hand-built widgets that the owner accepted.
That file is the bar. Open it before you start.

---

## 0. What deserves a widget at all

These exist for two reasons, and only two: to **break up the reading**, and to
make a **hard, abstract idea concrete**. They are not assessment, they are not
data collection, and they are not decoration for its own sake. They ship on the
free tier, to every student.

The test for whether a lesson deserves one:

> **Can a student read this passage correctly and still picture it wrongly?**

If yes, build. That catches:

- **invisible mechanisms** — electron flow, osmosis, how a synapse fires, what
  is actually moving in a sound wave;
- **counterintuitive relationships** — frequency up, wavelength down; a steeper
  basin giving a *shorter* lag time;
- **interacting variables**, where changing one shifts another and the student
  cannot hold both in their head at once;
- **things prose has to flatten** — a trench cross-section, a castle's
  approach, plate movement, anything spatial or simultaneous.

If no, do not build. Narrative history, definitions, quotation analysis and
anything already concrete in text get nothing. A widget that merely restates
the prose is worse than no widget: it costs the student time and teaches them
that these are skippable.

**Roughly one lesson in three or four should qualify.** That is the rhythm that
keeps them feeling fresh. Saturation is the failure mode — if every lesson has
one, they become furniture and get scrolled past.

---

## 0b. Commit before feedback

**But commit only where a real prediction exists.** Tom's field ruling on
the greenhouse widget (20 Aug): its "how many stay trapped?" answer was 0
in every round, and its "how many return?" answer was "about half" with a
tolerance - so after round one the student was re-typing a constant, and
mastery measured arithmetic, not understanding. A question whose answer
never changes is not a question. When the target idea has no fair,
variable, checkable question, build a STEP-THROUGH DEMONSTRATION instead:
the student advances the mechanism stage by stage (and flips any real
variable, like the CO2 level) rather than answering. Demonstration
widgets have no verdict and no mastery streak; svState carries
{step, completed} so achievement is still creditable. The commit-check
doctrine below applies to every widget that DOES pose a question.

**This is the most important pedagogical rule here, and the current widgets all
break it.**

A student who drags a slider and watches numbers move learns much less than one
who first commits to an answer, is wrong, and sees why. Continuous live feedback
lets them fiddle until it goes green — optimising the widget instead of thinking
about the physics.

So: **let the student assemble a whole answer, then have them commit it.**

> The insulation widget should let you choose loft, walls and glazing, then
> press **Check** — and only then find out whether the build reaches 85%, what
> it cost, and which measure was carrying its weight. Not a number that ticks
> up live as you drag.

- The commit control is a real button, labelled with the action: **Check**,
  **Run it**, **Test the design**, **See what happened**. Never "Submit".
- Before commit, show the consequences the student can *reason* about — the
  price of each option, what it physically does — but not the verdict.
- After commit, the reveal is the teaching moment: what happened, **why**, and
  what to change. Then let them adjust and go again.
- Where an interaction is genuinely exploratory and has no answer — a wave you
  are getting a feel for — live feedback is right. Know which kind you are
  building. If there is a correct answer anywhere in it, make them commit.

For a matching or sorting task, the equivalent is: place everything, then
**Check**, rather than lighting each tile green or red as it lands.

---

## 0c. Know when to stop

A widget with a bank of questions must have an **end**, and the end must be
mastery, not exhaustion.

**Exit on a run of correct answers — three is a good default.** A student who
has understood it should be released after three; a student who is guessing
keeps going. Never make anyone grind through a fixed ten to prove a point they
made at question three.

- A wrong answer **resets the run to zero**. That is the cost of guessing:
  you have to show it twice more.
- Show the run *while they are working*, quietly: "2 right in a row — one more
  and you have it." It gives the pile a bottom and it is the only counter worth
  displaying (see rule 6 on not scoring).
- When they get there, say what they now KNOW, not what they scored. "Three in
  a row — you have it. The current is the same everywhere, and V = I x R gives
  the bigger resistor the bigger share." Not "3/3, 100%".
- Let them carry on if they want: the button becomes **Another anyway**, never
  a dead end.
- Report it in `root.dataset.svState` as `{streak, mastered, attempted}` so a
  lesson can credit completion on *achieving* the thing rather than on opening
  the widget.

This does not apply to one-shot interactions — a single chain to order, one
diagram to label, a wave to get a feel for. Those end when they are done. It
applies wherever you have built a pool the student could otherwise loop
through forever.

---

## 1. The size budget

A widget opens in a **modal**, reached from a compact button inline in the
lesson. **Design it for the phone first** — most revision happens on one, and a
layout that works at 360px nearly always works on a laptop, while the reverse is
almost never true. Start narrow, then let it breathe.

It gets about **560px of usable height** on a laptop and a **360px minimum
width** on a phone.

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

**Header carries the title AND the task frame.** See rule 2 for what a task
frame is and what it is not.

---

## 2. State the task, then let the controls teach themselves

**Open with a task frame: the scenario and the command, in exam register,
one or two sentences, at the top under the title.** Tom's field test of
stage 1 (20 Aug) found every widget guilty of the same thing: the opening
screen assumed the student already knew the premise. The greenhouse widget's
first question was "How many of the 12 come back down?" - twelve WHAT? The
scenario (the warm ground sends 12 packets of infrared up towards space)
existed only in a caption BELOW the commit button. An exam question never
does this: it states the situation before it asks anything. So must a widget.

A task frame is the situation plus the ask - "A heater delivers 50 J to
this ice every second. Predict what the thermometer does over the next two
minutes, and where the energy goes." It is NOT a how-to paragraph: "click a
button to choose, then press Check" is still banned, because -

**- the controls themselves must still teach themselves.** After the task
frame, the opening state must show the student what to DO without any UI
instructions.

**Sequence the control groups.** When there is more than one group of
controls (a setting, a prediction, a commit), the eye must be told the
order - numbered step chips, or progressive disclosure (the next group
wakes when the previous is set). Three equal-weight groups side by side
read as a control panel, not a task.

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

**Never borrow a text's own words without marking them as quotation.**
Tom's field review (27 Aug): the witches widget wove Macbeth's line
"keep the word of promise to our ear, and break it to our hope" into its
own prose, unquoted - and Tom read it as overly flowery AI
editorialising. He was right in effect: a reader cannot tell borrowed
brilliance from generated purple. If the set text's words appear, put
them in quotation marks with a beat of attribution and keep each
quotation under 15 words; otherwise write plain English. The same field
review produced the plain-language rule: feedback must parse FIRST TIME
for a 15-year-old who got the answer wrong - poetic compression ("the
wish is heard with the letter") fails that test even when it is precise.

**But the first words still answer "was I right?"** Tom's field test (20
Aug): he committed a wrong answer to the greenhouse widget and got a
correct paragraph about re-emission - and could not tell whether he had
been right or wrong. Teaching-not-scoring is about what follows the
verdict, not a licence to omit it. Every feedback message opens with an
explicit marker - "Right -" or "Not quite -" - and every wrong branch
echoes the student's own committed answer before the mechanism: "Not
quite - you said 3 came back down and 3 stayed trapped. What happened: 4
came back down, none stayed trapped." A student who cannot find their own
answer in the feedback cannot connect the teaching to their mistake.

**The misconception answer must be expressible.** If the wrong picture the
widget exists to falsify cannot even be committed - the greenhouse chip
rows stopped at 6 while 8 packets were absorbed, so "all 8 stay trapped"
was un-enterable - the widget tests nothing. Scale answer ranges to the
round's data, and check the misconception answer fits at every round.

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

1. Could a student read this lesson correctly and still picture the idea
   wrongly? (If not, this widget should not exist.)
4. If there is a right answer anywhere in it, does the student **commit** — a
   Check button — before any verdict appears, rather than getting live feedback
   they can fiddle towards?
5. If there is a pool of questions, does it **end on a run of correct answers**
   (three is the default), reset that run on a wrong one, show the run while
   working, and still allow "Another anyway"?
6. Designed at 360px first, and measured height ≤ 560px at 900px wide and
   ≤ 640px at 360px wide, with no internal scrollbar?
7. Four zones or fewer, one stage, no placeholder boxes for unearned answers?
8. Does the widget open with a task frame — scenario + ask, exam register,
   1-2 sentences? And with every OTHER piece of text deleted, would a
   student still know what to do? (Delete any text that only survives the
   test by explaining the UI.)
9. Does the most likely first click do something useful rather than scold?
10. Do the title and framing avoid giving away any answer?
11. Is every discrete choice a button whose label carries its trade-off, and every
   slider a genuinely continuous quantity with worded ends?
12. Does every control change something visible immediately?
13. Does every box of prose get 32+ characters per line at 360px?
14. Have you enumerated the state space, and is there a real decision in it — more
   than one route to success, and a way to be wrong that costs something?
15. Is every claim in the text true of the reachable range? (State the actual
    ceiling; do not say "approaches 100%".)
16. Is success decided on integers or an explicit epsilon, with the intended
    solution clear of the boundary by at least one step?
17. Does the caption name a mechanism and its consequence, in the lesson's own
    vocabulary — rather than report a score?
18. Does a wrong answer explain what distinguishes it from the right one?
19. White card on warm ground, house colours and type, accent used sparingly,
    every selector scoped, no invented alert palette?
20. No timer running for decoration; DOM built once and mutated; keyboard focus
    stays where the student left it?
