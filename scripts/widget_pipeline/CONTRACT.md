# What a generated interactive must satisfy

This file is the **integration contract** only — how the widget plugs into the
site. It says nothing about design.

**For how to design and build the thing, read `BUILD_GUIDE.md`.** That is the
document to have open while you write the code. It carries the size budget,
the control rules, the house style and the self-check list, and it is derived
from looking at real rendered output.

## The rules

1. **One self-contained file.** No imports, no CDN, no network of any kind — no
   `fetch`, no `XMLHttpRequest`, no remote fonts or images. Everything inline.
   (The site runs under a strict CSP and must work offline.)
2. **Mount through this entry point**, and nothing else:

   ```js
   window.SVWidget = {
     meta: { id: 'kebab-slug', title: '...', teaches: '...' },
     mount: function (root, ctx) { /* build your UI inside root */ }
   };
   ```

   `root` is an empty `<div>` you own completely. `ctx` gives you
   `{ accent: '#rrggbb', reducedMotion: true|false }`.
3. **No `eval`, no `new Function`, no writing to `localStorage`** or anything
   else outside `root`. Scope every CSS selector to your own root class — an
   unscoped rule leaks into the lesson page.
4. **Responsive.** Must work from 320px to 900px wide without horizontal
   scrolling, and be usable by touch. The widget opens in a modal: see the
   height budget in `BUILD_GUIDE.md`.
5. **Reachable by keyboard.** Anything clickable must be a real
   `<button>`/`<a>`/input, or carry `tabindex` and respond to Enter. Respect
   `ctx.reducedMotion` by not auto-animating.
6. **Expose state for testing**: set `root.dataset.svState` to a small JSON
   summary whenever something meaningful changes (score, whether the student is
   correct, key computed values). The browser-based gate reads this to check
   behaviour. Keep it to the facts a test would assert on.
7. **Honest content.** Every number, date, name and unit defensible for GCSE and
   consistent with the lesson's own figures and vocabulary. No long quotations,
   no lyrics.
8. **It must be possible to get it wrong.** An interaction with no wrong answer,
   or a control that doesn't change what the student sees, is a failure.
