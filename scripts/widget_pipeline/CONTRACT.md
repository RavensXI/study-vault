# Generated widget contract

**This contract constrains the SHAPE OF THE CODE, never the kind of
interaction.** Invent whatever interaction teaches the lesson best —
dragging cards into groups, ordering events, matching pairs, clicking
hotspots on a picture, dealing a hand, routing a path, tuning two
competing dials, dropping items on a scale. There is no menu. If the
lesson wants something nobody has built before, build that.

The only rule is that the widget's *thinking* must be pure and
separate from its *drawing*, so it can be tested without a browser.
That is what makes generated interactives trustworthy at scale — not
sameness.

## The shape

```js
var W = {
  meta: { id: 'kebab-slug', title: '...', teaches: '...' },

  // PURE. The whole interaction lives in state.
  initialState: function () { return { /* JSON-serialisable */ }; },

  // PURE. Every user gesture becomes an action; this is the only way
  // state ever changes. Must never mutate its input.
  //   action examples you might invent:
  //   {t:'set', key:'voltage', v:230}   {t:'pick', card:3}
  //   {t:'drop', card:3, bin:'catholic'}   {t:'swap', a:2, b:5}
  //   {t:'hotspot', id:'gatehouse'}    {t:'reset'}
  apply: function (state, action) { return newState; },

  // PURE. Anything worth asserting on or showing: scores, whether the
  // student is right, computed physics, what is left to do.
  derive: function (state) { return { /* ... */ }; },

  // PURE. Where the clickable things ARE, so tests can drive the widget
  // without a browser and the host can route clicks. Return [] if the
  // widget is driven only by declared controls.
  regions: function (state, w, h) {
    return [{ x: 0, y: 0, w: 40, h: 40, action: { t: 'pick', card: 0 } }];
  },

  // Optional: sliders/toggles the host should render as real inputs.
  // Their changes arrive as {t:'set', key, v}.
  controls: [{ key: 'voltage', label: 'Mains', min: 200, max: 250,
               step: 1, value: 230, unit: 'V' }],

  // Drawing only. May read state/derived; must not change them.
  render: function (ctx, state, derived, w, h, acc) { /* ... */ },

  // One sentence of teaching that reacts to where the student is.
  caption: function (state, derived) { return '...'; }
};
if (typeof module !== 'undefined') module.exports = W;
```

A slider widget is just one where `regions()` is empty and `controls`
is populated. A drag-to-group widget has no controls and rich regions.
Both are the same code shape, so both are testable the same way.

## Rules

1. **Purity.** `initialState`, `apply`, `derive`, `regions` must be
   deterministic — no `Math.random`, no `Date`, no DOM, no network.
   `apply` must not mutate the state it is given.
2. **Total.** No throwing, and no `NaN`/`Infinity`/`undefined` fields,
   for any reachable state or any action `regions()` can emit.
3. **Reachable.** Every action a student can perform must be emitted by
   `regions()` or by a declared control, so tests can reach the whole
   interaction.
4. **Honest.** Every number, date and name must be defensible for GCSE
   and consistent with the lesson's own figures and vocabulary.
5. **It must teach.** An interaction that cannot be got wrong, or whose
   controls do not change the meaning of the picture, is a failure.
6. No lyrics, no long quotations, no claims the lesson does not support.
7. Plain ES5, no imports, no libraries.
