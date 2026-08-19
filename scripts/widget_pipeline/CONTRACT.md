# What a generated interactive must satisfy

Almost nothing. Build whatever teaches the lesson best.

Earlier versions of this file prescribed a code shape — pure functions,
one canvas, sliders — so that tests could run cheaply in Node. That was
a bad trade: it turned discrete choices into numbered sliders, forced
paragraphs of text to be laid out by hand in pixel coordinates, and made
everything look the same. Verification has moved into a real browser
instead, where it drives the actual thing a student uses. So the design
is yours.

**Use the whole browser.** Real HTML buttons and labels. CSS grid and
flexbox, so text lays itself out instead of being positioned by hand.
SVG for diagrams. Canvas where canvas genuinely wins — graphs,
simulations, anything continuous or animated. Drag and drop. CSS
transitions. If the lesson wants a map, draw a map. If it wants cards
you deal onto a table, deal cards onto a table.

Choose the right tool: **text-heavy interactions should be DOM**, not
text painted into a canvas. Graphs and spatial models should be canvas
or SVG. Mixing them in one widget is normal and encouraged.

## The only rules

1. **One self-contained file.** No imports, no CDN, no network of any
   kind — no `fetch`, no `XMLHttpRequest`, no remote fonts or images.
   Everything inline. (The site runs under a strict CSP and must work
   offline.)
2. **Mount through this entry point**, and nothing else:

   ```js
   window.SVWidget = {
     meta: { id: 'kebab-slug', title: '...', teaches: '...' },
     mount: function (root, ctx) { /* build your UI inside root */ }
   };
   ```

   `root` is an empty `<div>` you own completely. `ctx` gives you
   `{ accent: '#rrggbb', reducedMotion: true|false }` — use the accent
   as the widget's highlight colour so it matches its lesson.
3. **No `eval`, no `new Function`, no writing to `localStorage`** or
   anything else outside `root`.
4. **Responsive.** Must work from 320px to 900px wide without
   horizontal scrolling, and be usable by touch.
5. **Reachable by keyboard.** Anything clickable must be a real
   `<button>`/`<a>`/input, or carry `tabindex` and respond to Enter.
   Respect `ctx.reducedMotion` by not auto-animating.
6. **Expose state for testing**: set `root.dataset.svState` to a small
   JSON summary whenever something meaningful changes (score, whether
   the student is correct, key computed values). The browser-based gate
   reads this to check behaviour. Keep it to the facts a test would
   assert on.
7. **Honest content.** Every number, date, name and unit defensible for
   GCSE and consistent with the lesson's own figures and vocabulary. No
   long quotations, no lyrics.
8. **It must be possible to get it wrong.** An interaction with no wrong
   answer, or a control that doesn't change what the student sees, is a
   failure.

## House look (guidance, not constraint)

Warm and calm: ink `#2d2a26`, muted `#8d8880`, hairlines `#e8e2d9`,
paper `#faf8f5`, cards white with `border-radius: 12–16px`. Inter for UI,
Source Serif 4 for headings. The lesson's accent (`ctx.accent`) for
highlights and correctness. No drop shadows on small elements, no
gradients, no emoji. British English.
