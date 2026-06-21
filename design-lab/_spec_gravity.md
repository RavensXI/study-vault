# StudyVault Homepage — "Your revision, taking shape"
## FINAL BUILDABLE SPEC (synthesis: Direction 1 backbone + grafts from 0/2/3)

Single self-contained file at `/design-lab/home.html`. Inline `<style>` + inline vanilla `<script>`. **No external JS libs.** One decorative `<canvas>` carries the particle field; every interactive control is real, keyboard-operable DOM layered over/beside it. Hero images already exist at `/images/subject-{slug}.jpg` (verified). Reuse the existing `SUBJECTS` array shape from the current `design-lab/home.html` (keys `k,n,a,img,boards,def,L`).

---

## 0. Design tokens — VERBATIM from the live reader skin (`css/reskin.css [data-skin="reader"]`, lines 233–248, verified against source)

The reader skin's neutral anchor **is** `#566a72` (`--accent:var(--subject-accent,#566a72)`), radii **8px / 6px** (NOT 6/4 — that's the paper skin), and the `.key-fact` idiom is real (reskin line 146–148). Paste into `:root`:

```css
:root{
  --bg-body:#f7f6f4; --bg-card:#ffffff;
  --text-primary:#1d1c1a; --text-secondary:#54524d; --text-muted:#7f7c75;
  --border-light:#e6e4e0; --border-lighter:#f0eeea;
  --anchor:#566a72;                 /* neutral page accent (period, focus ring, default CTA) */
  --accent:var(--anchor);           /* JS re-points to dominant chosen subject once picks exist */
  --radius:8px; --radius-sm:6px;
  --shadow-sm:0 1px 3px rgba(45,42,38,.06);
  --shadow-md:0 4px 12px rgba(45,42,38,.08);
  --shadow-lg:0 8px 24px rgba(45,42,38,.10);
  --ease:cubic-bezier(.22,1,.36,1);
  --font-head:'Schibsted Grotesk',system-ui,sans-serif;  /* headings + ALL UI */
  --font-read:'Literata',Georgia,serif;                  /* body / lede */
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg-body);color:var(--text-primary);font-family:var(--font-read);line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden}
h1,h2,h3,.ui,nav,button,input,select,.kicker{font-family:var(--font-head)}
a{color:inherit;text-decoration:none}
:focus-visible{outline:2.5px solid var(--accent);outline-offset:2px;border-radius:4px}
.kicker{text-transform:uppercase;letter-spacing:.13em;font-size:.72rem;font-weight:700;color:var(--text-muted)}
```

Fonts — one `<link>`, exactly as the brief and existing file specify:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400..800&family=Literata:opsz,wght@7..72,400..600&display=swap" rel="stylesheet">
```
First thing in `<head>`: `<script>document.documentElement.classList.add('js')</script>` (already present in the file) so the rich canvas UI shows only with JS; the no-JS picker is the default DOM (§8).

### 0.1 Colour-through-structure budget (the whole page — audit against this; any 6th coloured thing is a regression)
Accent colour appears in EXACTLY these structural/data places:
1. The **period** in `StudyVault.` → `--anchor` (colour in a glyph).
2. The **canvas particles** → colour ENCODES which subject a lesson belongs to (data, allowed).
3. The **cluster glow** → a soft radial tinted to the *dominant* chosen subject (data: which subject dominates; on the decorative aria-hidden canvas).
4. The **constellation tick** + **shelf-row colour dot/left-rule** → data labels (which constellation), accent in glyphs/a 3px structural rule = the `.key-fact` idiom (reskin 146–148).
5. **ONE solid `--anchor`→subject-accent primary button** (the resolved signup CTA / masthead Get started — same identity).
6. The **focus-visible ring** (`--anchor`).
Everything else: `#f7f6f4`/`#fff` surfaces, ink/soft/muted type, 1px `--border-light` hairlines. **BANNED:** 999px pills/chips (use square `--radius-sm` tags), coloured edge-strips/top-bars on cards, tinted icon-in-rounded-square chips, decorative gradients on UI, glossy/heavy shadows (only `--shadow-sm/md/lg`), drop caps, Inter/Roboto/system defaults, purple-on-white. Buttons keep button affordances.

---

## 1. Page composition (one viewport-tall stage + hairline footer — a doorway, not a brochure)

```
┌──────────────────────────────────────────────────────────────┐
│ MASTHEAD (sticky, ~64px, transparent→hairline on scroll)       │
│ StudyVault.     For schools · I have a school code · Sign in   │
│                                          [ Get started ]       │
├──────────────────────────────────────────────────────────────┤
│  ░░░░  full-bleed <canvas id="field"> particle sky (aria-hidden)│
│  ░░░░  ~3,600 drifting subject-coloured motes, gently breathing │
│                                                                │
│            ┌──── centred control column (max 600px) ────┐      │
│            │  kicker:  YOUR REVISION, TAKING SHAPE        │     │
│            │  H1:  Everything you're sitting.             │     │
│            │       Nothing you're not.   (marker on L2)   │     │
│            │  lede (Literata, swaps on first pick)        │     │
│            │  ┌─ ⌕ command input ──────────────┐ [＋]      │     │
│            │  suggestion row (type-only) / SHELF rows      │     │
│            │  ── resolution: ONE accent CTA + quiet links ─│     │
│            └──────────────────────────────────────────────┘     │
│   (chosen clusters glow in the field BELOW/AROUND this column)  │
├──────────────────────────────────────────────────────────────┤
│ FOOTER (hairline top): © StudyVault 2026 · Privacy · For schools│
└──────────────────────────────────────────────────────────────┘
```

- `.stage{position:relative;min-height:100svh;display:grid;place-items:center;overflow:hidden}` — `100svh` so mobile browser chrome never crops the field.
- `#field` (canvas): `position:absolute;inset:0;width:100%;height:100%;z-index:0;pointer-events:none;filter:blur(.35px)` (the one cheap bloom pass — graft from Dir 0). `aria-hidden="true"`.
- `.control{position:relative;z-index:2;max-width:600px;margin-inline:auto;text-align:center;padding-top:16vh}` — sits OVER the field. The cluster forms in the field's lower-centre (Cy below the input), so live bright dots never sit behind the H1.
- **Legibility plate** behind ONLY the type block (graft + de-risk from Dir 0/2): a feathered fog of the page bg under the control column, NOT a coloured gradient. `.control::before{content:"";position:absolute;inset:-8% -6% -4% -6%;z-index:-1;background:radial-gradient(120% 100% at 50% 38%, rgba(247,246,244,.94) 0%, rgba(247,246,244,.86) 52%, rgba(247,246,244,0) 100%)}`. This is a legibility device (only the page colour, no border/chrome), so it does not break the colour rule. **Mandatory QA:** verify H1 `#1d1c1a` clears 7:1 over the densest possible field behind the plate.

### Masthead
- `.mast{position:sticky;top:0;z-index:50;background:color-mix(in srgb,var(--bg-body) 86%,transparent);backdrop-filter:saturate(1.1) blur(8px);border-bottom:1px solid transparent;transition:border-color .2s}` → add `.scrolled` (border `--border-light`) when `scrollY>8`.
- Wordmark `StudyVault` + `<i>.</i>` in `--anchor` (`font-style:normal`): `font-weight:800;font-size:1.3rem;letter-spacing:-.02em`.
- Nav: plain text links `For schools` · `I have a school code` · `Sign in`, `font-head;.92rem;color:var(--text-secondary);padding:.4rem .95rem;position:relative`. Hairline dividers: `a:not(:first-child)::before{content:"";position:absolute;left:0;top:50%;transform:translateY(-50%);height:1.05em;border-left:1px solid var(--border-light)}`. Hover → `--text-primary`; school-code + Sign in get a 1px underline (`text-underline-offset:3px`, `decoration-color:var(--anchor)`).
- **ONE solid button** total: `Get started` — `background:var(--anchor);color:#fff;font-head;font-weight:600;padding:.6rem 1.15rem;border-radius:var(--radius-sm);border:1px solid transparent`; hover `box-shadow:var(--shadow-md);transform:translateY(-1px)`. Anchors to the same signup flow as the resolved CTA.
- Mobile (<640px): nav collapses to just `[ Get started ]`; secondary links live in the resolved hero block anyway.

### Type ramp (control column)
- Kicker (always): `YOUR REVISION, TAKING SHAPE`, `--text-muted`, `margin-bottom:.9rem`.
- H1 (always): **"Everything you're sitting."** (line 1) / **"Nothing you're not."** (line 2, `<br>` ≥768px). `font-weight:800;font-size:clamp(2.1rem,4.6vw,3.2rem);line-height:1.04;letter-spacing:-.02em;text-wrap:balance`. Line 2 carries the **marker-highlight** — accent woven into glyphs, NOT a box: a thin underline `box-shadow:inset 0 -.28em 0 color-mix(in srgb,var(--accent) 22%,transparent)` on a `<span>`, animated `transform:scaleX(0→1)` (transform-origin left) over 700ms on load. (Glyph-level accent is explicitly allowed.)
- Lede (pre-pick): *"The whole GCSE library is up there — every subject, every board, 4,400 lessons. Tell it what you're sitting, and the rest fades away."* `font-read;clamp(1.02rem,1.5vw,1.16rem);color:var(--text-secondary);max-width:46ch;margin:1rem auto 1.5rem`.
- Lede (≥1 pick), swapped via `aria-live="polite"`: *"That's yours — {n} subjects, {ΣL} lessons, glowing. Add more, or make it permanent."*

### Footer
One hairline-topped row, `border-top:1px solid var(--border-light);padding:1.4rem 0;font-head;.85rem;color:var(--text-muted)`: `© StudyVault 2026` · `Privacy` · `For schools` · `Cookies`. No columns, no link farm.

---

## 2. Catalogue model — encode data, make the field read as the WHOLE 4,400 (graft: Dir 0 neutral bucket)

Reuse the existing 25-subject `SUBJECTS` array (`{k,n,a,img,boards,def,L}`). The field must look like the **whole catalogue (72 subjects / ~4,400 lessons)**, not just the 25, so:

```js
const TOTAL = 3600;                 // reads identically to "thousands"; perf-safe to 60fps mid-phone
const NAMED_SHARE = 0.62;           // named 25 own 62% of motes…
const REST_HEX = '#8a857d';         // …38% is a muted-slate "everything else" bucket (subj = -1)
const sumL = SUBJECTS.reduce((s,x)=>s+x.L,0);              // ≈ 921
SUBJECTS.forEach((s,i)=>{ s.idx=i; s.count = Math.max(34, Math.round(TOTAL*NAMED_SHARE*(s.L/sumL))); });
let named = SUBJECTS.reduce((s,x)=>s+x.count,0);
const REST_COUNT = TOTAL - named;   // neutral remainder ≈ 38%
```
- `Math.max(34,…)` floors small subjects: Drama (14 lessons) → ≥34 motes (visibly brightens on pick); Combined Science (78) → ~190 motes.
- The neutral bucket (`subj=-1`, colour `#8a857d`, baseAlpha slightly lower) is **never selectable** and **always recedes** on any pick — it's the visual proof that "the rest of the library" exists and is being narrowed away.
- Parse every subject hex to `[r,g,b]` ONCE. Precompute `indicesBySubject[i] = Int32Array of particle indices` (graft Dir 3 — never an O(N·subjects) per-frame scan).

---

## 3. Canvas particle system

### 3.1 Storage — typed arrays (graft Dir 1, perf floor)
Flat `Float32Array`s for cache-friendliness at 3,600. Fields per particle: `x,y` (live), `hx,hy` (ambient home), `vx,vy`, `tx,ty` (converge target), `ph` (breathe phase), `r0` (base radius 0.7–1.8 css px), `a` (live alpha), `aT` (target alpha), `z` (0=far..1=near depth → size+parallax), plus `sub Int16Array` (subject idx or -1) and `st Uint8Array` (0 ambient · 1 chosen · 2 receding).

### 3.2 Spawn
- Home: polar **centre-biased ellipse** filling the stage, oversample edges via sqrt so it reads as a soft cloud not a rectangle: `a=rand*2π; rad=sqrt(rand); hx=cx+cos(a)*rad*W*0.50; hy=cy+sin(a)*rad*H*0.46`.
- `z=rand`; `r0 = 0.7 + z*1.1`; ambient `aT = (sub===-1 ? 0.09 : 0.12) + z*0.16` (named 0.12–0.28, rest dimmer); `a` starts 0 (bloom-in). `ph=rand*2π`.

### 3.3 The canonical easing primitive (graft Dir 2 — use everywhere)
Frame-rate-independent, identical at 60/120Hz. `dt` in **seconds**, clamped `≤0.033`:
```
v += (target - v) * (1 - Math.pow(retain, dt))
//   retain ≈ 0.0016 → firm converge, ~700ms settle
//   retain ≈ 0.02   → silky ambient drift
//   retain ≈ 0.25   → soft ~0.6s alpha dim/brighten
```

### 3.4 Per-frame ambient (state 0) — drift + breathing + cursor parallax
Three slow layered motions (dust motes, never snow):
1. **Brownian tether:** weak random nudge + weak spring to the breathing home so the field wanders ~10–18px peak-to-peak over 6–9s but never disperses. `home` is scaled about centre by `breath = 1 + Math.sin(t*0.0007)*0.009` (≈9s, ±0.9% inhale).
2. **Breathing alpha shimmer:** `aT_live = baseA + Math.sin(t*0.0008 + ph)*0.03`; ease `a` toward it with retain 0.02.
3. **Cursor parallax (desktop only):** within 140px, near (high-z) dots lean ~6px away from the pointer, falloff linear. `mx,my` init `-99999`; reset on `mouseleave`. Disabled on touch and under reduced-motion.

### 3.5 Render loop + DPR
```js
const dpr = Math.min(window.devicePixelRatio||1, 2);   // CAP at 2 — retina phones gain nothing from 3×
// size backing store W*dpr×H*dpr, CSS size W×H, ctx.setTransform(dpr,0,0,dpr,0,0) → draw in CSS px
function frame(now){
  const dt = Math.min((now-last)/1000, 0.033); last=now; const t=now;
  ctx.clearRect(0,0,W,H);
  if(picks.length) drawClusterGlow(t);                 // §4.3 — radial, BEFORE dots
  for(const g of indicesBySubject){                    // batch fillStyle by subject (~26 swaps/frame)
    ctx.fillStyle = g.css;
    for(const i of g.list){
      if(reduced){ /* static: positions already final */ }
      else if(st[i]===0) updateAmbient(i,t);
      else updateConverge(i,dt,t);                      // §4.2
      if(a[i] < 0.012) continue;
      ctx.globalAlpha = a[i];
      const r = r0[i] * (st[i]===1 ? 1.7 : 1);          // chosen motes bigger
      ctx.beginPath(); ctx.arc(x[i],y[i], r, 0, 6.283); ctx.fill();
    }
  }
  ctx.globalAlpha = 1;
  raf = requestAnimationFrame(frame);
}
```
- **Bloom:** the CSS `filter:blur(.35px)` on the canvas gives every round mote a soft halo for one cheap GPU pass — NOT per-dot `shadowBlur` (fatal at 3,600). Round `arc()` motes (not Dir 3's fillRect squares) are retained because the soft mote texture is what sells the premium "living sky".
- Pause `cancelAnimationFrame` on `document.hidden`; resume on `visibilitychange`, reseeding `last=performance.now()` so `dt` never spikes.
- **FPS guard (graft Dir 0):** sample avg frame time over the first 30 frames; if avg <50fps, drop `TOTAL` to 2,200 (skip every Nth particle by setting `a=0`) and remove the CSS blur.

---

## 4. Pick → converge (the gravitational moment)

### 4.1 Targets — per-subject phyllotaxis discs (Dir 1 backbone + Dir 3 density-encodes-count)
Chosen subjects do NOT merge into one blob — each gets its own tidy glowing disc so the student sees distinct constellations (avoids the navy-family colour-muddle that hurt Dir 0/2's single shared wedge-disc). Layout:
- Cluster band sits in the field's **lower-centre**, below the input: `Cy = H*0.5 + controlHeight*0.20` (never behind the H1).
- For `m` chosen subjects, place `m` wells: m=1 centred at `(W/2, Cy)`; m≥2 evenly spaced across the middle 70% of width on a gentle smile arc `wy_j = Cy - sin(j/(m-1)*π)*H*0.03`.
- Each subject's disc **radius scales by sqrt(count)** (graft Dir 3): `discR = clamp(3.0*Math.sqrt(count), 26, min(W,H)*0.16)` — a 78-lesson subject is a visibly denser/larger glow than a 14-lesson one (the secondary "lots of Maths, a little Drama" read).
- Within a disc, golden-angle (sunflower) packing for even, organic, seam-free fill:
```js
const GOLD = Math.PI*(3 - Math.sqrt(5));   // 2.39996…
// for the k-th of `count` dots: r = discR*Math.sqrt((k+0.5)/count); ang = k*GOLD;
// tx = wx + r*Math.cos(ang) + jitter(±0.6);  ty = wy + r*Math.sin(ang)*0.82 + jitter(±0.6)  // 0.82 = perspective squash
```
- **Gather order (graft Dir 3):** sort a subject's dots by distance to its well centre, fill innermost slots first → minimal travel, tidy outside-in fill.

### 4.2 The transition (Dir 1 critically-damped spring with one whisper of overshoot)
```js
function updateConverge(i, dt, t){
  if(st[i]===1){            // chosen: brighten + magnetise home, single soft overshoot
    const k = boostUntil>t ? 0.028 : 0.022, damp = boostUntil>t ? 0.90 : 0.80;
    vx[i] = (vx[i]*damp) + (tx[i]-x[i])*k;  vy[i] = (vy[i]*damp) + (ty[i]-y[i])*k;
    x[i]+=vx[i]; y[i]+=vy[i];
    if(Math.hypot(tx[i]-x[i],ty[i]-y[i])<2){               // settled → faint orbital life, never frozen
      x[i]+=Math.cos(t*0.0006+ph[i])*0.12; y[i]+=Math.sin(t*0.0006+ph[i])*0.12;
    }
    aT[i] = 0.55 + z[i]*0.40;                              // BRIGHTEN to 0.55–0.95
  } else {                  // receding: dim + drift gently outward, never destroyed
    aT[i] = sub[i]===-1 ? 0.03 : 0.05;
    x[i] += (hx[i]+(hx[i]-cx)*0.25 - x[i]) * (1-Math.pow(0.0016,dt));
    y[i] += (hy[i]+(hy[i]-cy)*0.25 - y[i]) * (1-Math.pow(0.0016,dt));
  }
  a[i] += (aT[i]-a[i]) * (1-Math.pow(0.25,dt));            // ~0.6s brighten/dim
}
```
- `boostUntil = performance.now() + 450`: for 450ms after a pick, chosen dots use slightly under-damped constants (`k=0.028, damp=0.90`) → ONE ~5px settle wobble, then revert to critically-damped (no second bounce — that reads cartoonish). **Felt timing:** ~70% of distance covered in the first ~380ms, fully settled by ~700ms — a single satisfying gravitational pull.
- Stagger each dot's start by `dist/maxDist * 120ms` so the disc visibly *gathers* rather than snapping.
- **Re-flow on every add/remove:** recompute all well centres + retarget every chosen dot (existing constellations slide to make room over ~600ms — the "rearranges to admit the newcomer" beat). Springs compose, so rapid picks just retarget mid-glide.
- **Remove:** that subject's dots flip `st=0`, `aT` back to ambient, `tx,ty=hx,hy` → they spring back out and resume breathing (~900ms); remaining wells re-flow.

### 4.3 Cluster glow (graft Dir 0 — the luminous payoff)
When `picks.length>0`, draw ONE soft radial per well BEFORE the dots, tinted to that well's subject colour (data-encoded, on the decorative layer), alpha eased 0→0.16 over 500ms:
```js
const grad = ctx.createRadialGradient(wx,wy,0, wx,wy,discR*1.7);
grad.addColorStop(0, `rgba(${r},${g},${b},${0.16*glow})`); grad.addColorStop(1, `rgba(${r},${g},${b},0)`);
ctx.fillStyle=grad; ctx.beginPath(); ctx.arc(wx,wy,discR*1.7,0,6.283); ctx.fill();
```
`glow` lerps 0→1 on first pick, back to 0 when cleared.

---

## 5. The picker UI (real DOM, WAI-ARIA combobox, keyboard-first)

### 5.1 Command input + add
- Single row: `<input type="text" role="combobox" aria-expanded="false" aria-controls="ac-list" aria-autocomplete="list" placeholder="Name a subject you're sitting…">` + trailing `<button aria-label="Add subject">`. Card field: `background:var(--bg-card);border:1px solid var(--border-light);border-radius:var(--radius-sm);box-shadow:var(--shadow-sm);padding:.85rem 1rem;font-head;1.05rem`. Focus-within: `border-color:var(--accent);box-shadow:0 0 0 3px color-mix(in srgb,var(--accent) 16%,transparent)`.
- The `⌕` is an **inline `<svg>`** stroke icon (1.6px, `currentColor`, `--text-muted`) — NEVER a CSS `background:url(data:…)` (the data-URI footgun that truncates the stylesheet).
- **Do NOT autofocus** (would pop the mobile keyboard over the wow). On load (≥1400ms), a single quiet one-time focus pulse on the input border draws the eye.

### 5.2 Autocomplete listbox
- Filter `SUBJECTS` by `name.toLowerCase().includes(q)` + alias map (`maths→Mathematics`, `lit→English Literature`, `compsci/comp sci→Computer Science`). Render ≤6 in `<ul id="ac-list" role="listbox">`: white card, 1px border, `--shadow-lg`, `--radius`. Each `<li role="option">`: subject name (ink, `font-head 600`) + 8px subject-colour dot (colour = data) + right-aligned `--text-muted` lesson count.
- Keyboard: ↑/↓ move `aria-activedescendant`; Enter selects active (or first); Esc closes; Tab leaves. Hover mirrors active. On select → clear input, collapse, `addSubject(k)`.

### 5.3 Suggestion row (pre-pick, NOT pills)
Under the input, 6 popular starters as **plain text buttons** separated by `·`: `Maths · Combined Science · English Language · History · Geography · Biology`. `font-head;.92rem;color:var(--text-secondary)`; hover → ink + 1px underline + leading colour-dot. Plus `See all 25 →` text link. Clicking adds with that subject's `def` board.

### 5.4 Per-subject board (board is PER subject)
A subject is fully "added" once it has a board, but the converge fires IMMEDIATELY on add (commit feels instant) — the board only gates the "looks complete" state:
1. Add subject → dots converge now; an inline board step appears on its shelf row.
2. Board step = inline `<fieldset role="radiogroup" aria-label="Exam board for {subject}">` with that subject's boards only, as small **text radios** `AQA · Edexcel · OCR · Eduqas` (`aria-checked`). Default-focus the first board the instant the subject is added (keyboard flow: type → Enter → arrow → Enter). Single-board subjects (e.g. Psychology) auto-set + show board as static text — no radiogroup.
3. Until set, the row shows `Pick your board` in `--text-muted`; copy reflects it: `3 subjects · 1 needs a board`.

### 5.5 The shelf (chosen-state result — the `.key-fact` idiom)
Each chosen subject = a slim **row** (NOT a uniform button), built exactly like the reader `.key-fact` (reskin 146–148):
```css
.shelf-row{
  display:flex;align-items:center;gap:.75rem;padding:.7rem .9rem;
  background:color-mix(in srgb, var(--row-accent) 8%, var(--bg-card));
  border:none;border-left:3px solid var(--row-accent);
  border-radius:0 var(--radius-sm) var(--radius-sm) 0;box-shadow:none;
}
.shelf-row:hover{box-shadow:var(--shadow-sm)}
```
- `--row-accent` is set inline on THAT row only (`style="--row-accent:#3f5e78"`); the page's `--accent` is separate. This is accent woven as a *structural left-rule* (the lesson key-fact), the page's compliant subject-colour-in-UI place.
- Left: the subject's 8px colour dot OR (richer, once a board is set) a `28×28` rounded real hero thumbnail `<img src="/images/subject-{slug}.jpg" loading="lazy" style="object-fit:cover;border-radius:6px">` — same colour the student watches brighten in the cluster (eye-to-cluster mapping).
- Subject name (ink, `font-head 600`); sub-line `font-read;.85rem;--text-muted`: `{L} lessons · {board}`.
- Right: the board radiogroup (§5.4) + remove `×` (1.2px stroke inline-SVG, `--text-muted`→`--text-primary` hover, `aria-label="Remove {subject}"`).
- Rows enter `opacity 0→1 / translateY(6px→0)`, 220ms `--ease`, staggered 40ms.

### 5.6 Self-labelling constellation (graft Dir 2/3)
250ms after a cluster gathers, a real **DOM label** (not canvas text — crisp, selectable, translatable, SR-readable; `aria-hidden="false"`) fades in beside its well: subject name `font-head 600 .85rem` ink + a 14px hairline **tick** in the subject accent pointing at the disc + `{L} lessons · {board}` in `--text-muted`. Fade `opacity 0→1 / translateX(-4px→0)`, 500ms `--ease`. Past ~5 picks, switch labels to a compact stacked legend under the band (name + 6px accent dot) to avoid crowding.

---

## 6. EXACT load animation (timings + easing; "wow on load", no click)

`t=0` = `document.fonts.ready` resolved (or 400ms timeout). Easing: **soft** = `cubic-bezier(.22,1,.36,1)`.

| t (ms) | Event | How |
|--------|-------|-----|
| 0 | Page bg painted. Canvas rAF starts; all 3,600 motes at `home`, `a=0`. Control column type `opacity:0` (only if `.js`). | — |
| 0–900 | **Field blooms centre-out.** Each mote fades to ambient `baseA`; per-mote start delay `= (dist_from_centre/R)*350ms`, ramp 550ms, `easeOutCubic` → a single point becomes a galaxy in <1s. Breathing already runs underneath (imperceptible until motes are visible). | per-mote `a` lerp |
| 200 | Kicker fades+rises (8px→0), 420ms soft. | CSS `.rv.in` |
| 320 | H1 line 1 fades+rises (12px→0), 520ms soft. | CSS |
| 420 | H1 line 2, same. | CSS |
| 560 | Marker highlight on "Nothing you're not." sweeps `scaleX(0→1)` from left, 700ms soft. | CSS transition |
| 600 | Lede + input fade in (10px→0), 480ms soft, 60ms stagger. | CSS |
| 900 | Field at full ambient brightness; idle breathing holds indefinitely. | — |
| ~1400 | One-time input focus-pulse (border `--border-light→--accent→--border-light`, 900ms). NOT autofocus. | CSS |

**On first pick:** cluster glow eases 0→full 500ms; chosen dots converge ~700ms; shelf row enters 220ms; label fades 250ms after gather. Each later pick = a fresh ~600–700ms re-flow.

---

## 7. Resolution → account CTA (appears once ≥1 subject HAS a board)

A quiet block fades in under the shelf (240ms):
```
[ Create your free account — keep your shelf on every device ]   ← the ONE solid button, --accent
Already have one? Sign in   ·   I have a school code             ← plain text, hairline divider
Just start revising →                                            ← tertiary no-gate escape link
Free · no payment · your shelf saves to this device until you sign in.   ← --text-muted .85rem
```
- The primary button is the **only** solid-accent button in the hero; its colour = the **dominant chosen subject's** colour (most dots). JS re-points `:root{--accent}` once picks exist, with a 400ms colour transition on the button — the page anchor "warms into their colour" (earned, meaningful).
- A short count beat above it (Literata): *"That's your shelf — **{n} subjects · {ΣL} lessons**, just the ones you're sitting."* — their number, not 4,400 (narrowing achieved). The thesis line **"Everything you're sitting. Nothing you're not."** is the H1, so it isn't repeated here.
- `Just start revising →` (graft Dir 0/3) hands the picks (localStorage `{slug,board}[]`) to the real browse/wizard — proving the account is a benefit, never a gate.
- `I have a school code` reveals an inline `Enter your school code` input + quiet `Continue` (text link, not filled), sliding down 300ms.

---

## 8. Reduced-motion + No-JS

### `prefers-reduced-motion: reduce` (detect via `matchMedia` at init AND listen for live changes)
- **No drift/breathing/bloom/cursor; no rAF loop after first paint.** Run `frame()` exactly ONCE: motes at `home`, ambient alpha, full radius — a calm fixed star-field.
- **Converge = instant state change:** on pick, set `x=tx,y=ty,a=aT` immediately and redraw once; glow drawn at full alpha in one step; labels appear with no fade.
- All CSS entrance transitions → `transition:none` (gate `.rv` opacity behind `@media (prefers-reduced-motion:no-preference)` so reduced users see final state).

### No-JS (`html:not(.js)`)
- Canvas never initialises (it's decorative `aria-hidden` — zero information lost).
- The control column renders a **plain, usable picker**: `<form method="get" action="/browse">` containing a `<fieldset>` of all 25 subjects as labelled checkboxes, each with an inline native `<select>` for board, and a submit `Build my shelf`. The three CTAs (`Create free account` / `Sign in` / `I have a school code`) are plain `<a href>`. Styled with the same tokens (white cards, hairlines, ink) so it looks intentional, not broken.
- `.js .picker-plain{display:none}` / `.picker-plain{display:block}` and inverse for the rich UI — progressive enhancement.

---

## 9. Accessibility + performance checklist

- Particles in canvas only (3,600); **zero** per-dot DOM. DPR capped at 2. `fillStyle` batched by subject (~26 swaps/frame) via precomputed `indicesBySubject`. One CSS `filter:blur(.35px)` for bloom (no `shadowBlur`).
- `requestAnimationFrame` paused on `document.hidden` and after the single static reduced-motion frame. FPS probe drops `TOTAL`→2,200 + removes blur if <50fps in first 500ms.
- Canvas `aria-hidden="true"`; all interaction real DOM. Combobox follows WAI-ARIA APG (input + listbox + `aria-activedescendant`). Board radiogroups labelled per subject (`aria-checked`). Remove buttons labelled. Constellation labels are real text (`aria-hidden="false"`).
- `:focus-visible` ring everywhere (2.5px accent, offset 2px).
- WCAG AA: ink `#1d1c1a` on `#f7f6f4` ≈ 15:1; `--text-secondary #54524d` ≈ 7.4:1; `--text-muted #7f7c75` ≈ 4.6:1 (only ≥.85rem). **Mandatory:** verify H1 ≥7:1 over the densest field region behind the legibility plate (worst case = peak ambient; the cluster band sits below the H1 by design).
- Resize: `ResizeObserver` on `.stage` (debounced via rAF) → recompute `W,H,cx,cy`; scale homes proportionally (`hx *= newW/oldW`) so the field never teleports; re-run cluster re-flow if picks exist.

---

## 10. Hard-parts JS index
- `buildField()` — typed-array spawn + weighted subject assignment + neutral bucket (§2, §3.2).
- `updateAmbient(i,t)` — drift + breathing + cursor parallax (§3.4), uses the easing primitive (§3.3).
- `assignTargets()` — per-subject phyllotaxis discs, sqrt-count radius, nearest-first gather, well re-flow (§4.1).
- `updateConverge(i,dt,t)` — critically-damped spring + 450ms overshoot boost + recede (§4.2).
- `drawClusterGlow(t)` — per-well radial tint, eased glow (§4.3).
- `addSubject(k)/removeSubject(k)` — drive shelf DOM + canvas state + label + `--accent` re-point; instant-snap branch under `reduced`.
- Helpers: `hexToRgb(hex)`, `indicesBySubject`, alias map.

## 11. Why this wows in one first impression
A 15-year-old lands and the screen is already alive — thousands of faint subject-coloured motes breathing as one calm GCSE sky, no spinner, no banner, no ask. They type "History," hit Enter, and a swarm of dots brightens and is pulled, springing, into a small glowing constellation that names itself, while the rest of the universe dims and drifts to the edges. By the third subject they've built a private, luminous, labelled shelf in *their* colours, the page anchor has warmed into their dominant subject's hue, and the only button quietly offers to keep it forever — with a no-gate "just start revising" beside it. The product's whole thesis (everything you're sitting, nothing you're not) is *performed* on their own subjects, in real time, never described. It looks made-by-a-teacher, not generated: round soft motes on warm paper, colour only where it encodes data, ink type, hairline rules, one honest accent button.

## 12. Risks / watch-outs
- **Contrast under the H1:** the legibility plate (page-bg fog, not a coloured gradient) must keep H1 ≥7:1; cluster band Cy sits below the headline by design. Test worst case.
- **Colour muddle:** four navy-family accents (Maths/History/Physics/Computer Science) blur in the scatter (fine pre-pick — meant to read as one whole) but per-subject SEPARATED discs + labels carry differentiation post-converge (this is why we reject the single shared-disc wedge of Dir 0/2).
- **Low-end Chromebook/Android (real student device):** 3,600 arcs + blur — the FPS probe (→2,200 + no blur) and reduced-motion floor are the guards; test on a real budget device.
- **The CSS data-URI trap:** every icon is inline `<svg>` or a unicode glyph (⌕, ×, ＋). Never let anyone "optimise" them into `background:url(data:…)`.
- **Wizard hand-off:** serialise picks as `{slug, board}[]` so the production five-maps-lockstep wizard can hydrate directly; keep that exact shape.
- **Colour-discipline drift:** the single biggest way this becomes "AI slop" later is someone adding a tinted card or gradient CTA. The rule for this page: accent only in the wordmark period, particle glyphs, cluster glow, constellation tick + shelf left-rule, and the one filled button. Anything else coloured is a regression.