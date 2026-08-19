# Generated widget contract

Every generated widget is ONE JavaScript file with **no DOM in its
thinking layer**. The model logic is pure, the drawing is separate. That
split is not stylistic — it is what makes a generated widget verifiable:
property tests exercise `derive()` / `steps()` in Node with no browser,
so thousands of widgets can be checked in seconds.

```js
/* SV Widget */
var W = {
  meta: {
    id: 'physics-p1-l5-power',          // unique slug
    title: 'Balance the household ring main',
    teaches: 'P = VI rearranged, and why the ring main trips',
    kind: 'explore'                      // 'explore' | 'steps'
  },

  // 'explore': named controls become sliders/toggles in the host
  controls: [
    { key: 'voltage', label: 'Mains voltage', min: 200, max: 250,
      step: 1, value: 230, unit: 'V' },
    { key: 'kettle', label: 'Kettle on', type: 'toggle', value: true }
  ],

  // PURE. params in, derived values out. No DOM, no randomness, no Date.
  derive: function (p) {
    var current = (p.kettle ? 3000 : 0) / p.voltage;
    return { current: current, tripped: current > 13 };
  },

  // canvas drawing. ctx is 2d, w/h are CSS pixels, acc is the lesson's
  // accent colour. May read p and d, must not mutate them.
  render: function (ctx, p, d, w, h, acc) { /* ... */ },

  // one sentence of teaching, reacting to the current state
  caption: function (p, d) {
    return d.tripped ? 'Over <b>13 A</b> — the fuse blows.' : '...';
  }
};
```

For `kind: 'steps'` (walk-through interactions — an algorithm, a process,
a chronology) replace `controls`/`derive` with:

```js
  steps: function (p) {          // PURE, returns the whole script at once
    return [{ caption: '...', state: { /* JSON-serialisable */ } }, ...];
  },
  render: function (ctx, step, w, h, acc) { ... }
```

## Rules the generator must obey

1. **Purity.** `derive`/`steps` must be deterministic: no `Math.random`,
   no `Date`, no DOM, no network. Same params in, same values out.
2. **Total.** Must not throw anywhere in the declared control ranges,
   and must not return `NaN`, `Infinity` or `undefined` fields.
3. **Honest numbers.** Every quantity must be defensible for GCSE and
   consistent with the lesson's own figures and vocabulary.
4. **The interaction must teach.** A control the student can move that
   does not change the meaning of the picture is a failure.
5. **No lyrics, no long quotations**, and no claims not supported by the
   lesson text.
6. Plain ES5-compatible JS, no imports, no libraries, ends with
   `if (typeof module !== 'undefined') module.exports = W;`
