"# StudyVault Homepage — "Your revision, taking shape"
## Aesthetic angle: EDITORIAL / Ink constellation on paper

A single self-contained `home.html`. Inline CSS + JS, no external JS libs. One `<canvas>` carries the particle field; all controls are real DOM layered over/beside it.

---

## 0. DESIGN TOKENS (paste verbatim into `:root` — these ARE the reader skin)

```css
:root{
  --bg-body:#f7f6f4; --bg-card:#ffffff;
  --text-primary:#1d1c1a; --text-secondary:#54524d; --text-muted:#7f7c75;
  --border-light:#e6e4e0; --border-lighter:#f0eeea;
  --anchor:#566a72;                 /* neutral page accent (the period, focus rings, the one CTA) */
  --radius:8px; --radius-sm:6px;
  --shadow-sm:0 1px 3px rgba(45,42,38,.06);
  --shadow-md:0 4px 12px rgba(45,42,38,.08);
  --shadow-lg:0 8px 24px rgba(45,42,38,.10);
  --ease:cubic-bezier(.22,1,.36,1);
  --font-head:'Schibsted Grotesk',system-ui,sans-serif;  /* headings + ALL UI */
  --font-read:'Literata',Georgia,serif;                  /* body / lede / italic subtitles */
}
html,body{background:var(--bg-body);color:var(--text-primary);font-family:var(--font-read);}
h1,h2,h3,.ui,button,input,.kicker,nav{font-family:var(--font-head);}
.kicker{ text-transform:uppercase; letter-spacing:.13em; font-size:.72rem; font-weight:700; color:var(--text-muted); }
```
Fonts (one link in `<head>`):
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400..800&family=Literata:ital,opsz,wght@0,7..72,400..600;1,7..72,400..500&display=swap" rel="stylesheet">
```

**Colour-through-structure compliance.** Across the whole *chrome* there are exactly THREE places colour appears, all structural:
1. The period in `StudyVault.` is `--anchor` (colour lives in a glyph).
2. The ONE primary CTA is a solid `--anchor` fill (a button that earns its colour).
3. The chosen-subject shelf rows each carry a **3px left rule** in that subject's accent + an 8%-accent tint on the row — the exact `.key-fact` idiom from the reader (`border-left:3px solid accent; background:color-mix(accent 8%, card)`).
Everything else is `#fff`/`#f7f6f4` surfaces, ink type, 1px `--border-light` hairlines. **The canvas particles are coloured by subject — that is data encoding, not decoration, and is allowed.** No pills, no edge-strips on cards, no tinted icon chips, no gradients-as-decoration, no drop caps, radius capped at 8px.

---

## 1. PAGE COMPOSITION

Single non-scrolling viewport on desktop (the page IS the hero — there is nothing to scroll to; this is a doorway, not a brochure). Vertical stack, `100dvh`, `display:grid; grid-template-rows:auto 1fr auto;` → masthead / hero-stage / footer.

```
┌───────────────────────────────────────────────────────────┐
│ MASTHEAD  StudyVault.        For schools · school code · Sign in   [Get started] │  (auto)
├───────────────────────────────────────────────────────────┤
│                                                             │
│              <canvas>  full-bleed ink field                 │  (1fr — fills)
│                                                             │
│        ┌─ centred glass-free console (max-width 560px) ─┐   │
│        │  kicker: YOUR REVISION, TAKING SHAPE            │   │
│        │  H1: Everything you're sitting. Nothing you're not. │
│        │  lede (Literata)                                │   │
│        │  [ search input · "Add a subject…" ]            │   │
│        │  suggestion row / chosen shelf appears here     │   │
│        │  resolution CTAs (appear once ≥1 chosen)        │   │
│        └────────────────────────────────────────────────┘   │
│                                                             │
├───────────────────────────────────────────────────────────┤
│ FOOTER  © StudyVault · Built by a teacher · Privacy · Free, always │  (auto)
└───────────────────────────────────────────────────────────┘
```

The console is NOT a card with a border by default — it sits directly on the paper/field so the dots read as ink *behind and around* the type (editorial: type on paper, specks in the margins). Only the input has a hairline. As subjects are added the shelf grows downward; the canvas converges its dots toward a point just behind/above the console so the cluster and the type cohabit.

### 1a. Masthead (height ~68px, `padding:0 clamp(1.25rem,4vw,2.75rem)`)
- Left: `StudyVault` in `--font-head` 700, `1.18rem`, `letter-spacing:-.01em`, ink — followed by a `.` span coloured `--anchor`.
- Right (desktop): plain-text nav, `--font-head` 500, `.92rem`, `--text-secondary`, separated by hairline dividers (a `<span>` `1px×14px` `background:--border-light`, `vertical-align:middle`, `margin:0 .9rem`): **For schools** · **I have a school code** · **Sign in**. Hover → ink, 1px underline `text-underline-offset:3px`, decoration-colour `--anchor` at 45%.
- Far right: ONE solid button **Get started** — `background:--anchor; color:#fff; border:none; border-radius:--radius-sm; padding:.55rem 1rem; font-weight:600; box-shadow:var(--shadow-sm)`. Hover `filter:brightness(.94); box-shadow:var(--shadow-md)`. This is the only filled colour in the chrome.
- Mobile (<720px): nav collapses to just `Sign in` + `Get started`; the rest moves to footer.
- Bottom hairline: `border-bottom:1px solid var(--border-light)`.

### 1b. Footer (height ~52px)
- One quiet line, `.82rem`, `--text-muted`, centred or left: `© 2026 StudyVault` · `Built by a teacher` · `Privacy` · `Free, always`. Hairline top. Links underline on hover only. No social, no columns — a doorway has a small sill.

---

## 2. THE HERO CONSOLE (DOM, layered over canvas via `position:relative; z-index:2`)

Centred, `max-width:560px`, `text-align:center`, vertically centred in the stage with a slight upward bias (`align-self:center; margin-top:-4vh`) so the cluster has room to gather above it.

- **Kicker** (`.kicker`): `YOUR REVISION, TAKING SHAPE` — `--text-muted`, `margin-bottom:1rem`.
- **H1**: `Everything you're sitting.<br>Nothing you're not.` — `--font-head` 700, `clamp(2rem,4.4vw,3.2rem)`, `line-height:1.04`, `letter-spacing:-.02em`, `text-wrap:balance`, ink. The second line `Nothing you're not.` is `--text-secondary` so the promise reads as a beat. (No accent on type here — restraint; the field carries the colour.)
- **Lede** (Literata, `1.05rem`, `--text-secondary`, `max-width:42ch`, `margin:1rem auto 1.75rem`): `Name the subjects you're revising and the whole GCSE library — every board, 4,400 lessons — settles into just yours.`
- **Picker** (see §5).
- **Resolution CTAs** (see §6) — hidden until first pick.

On `prefers-reduced-motion`, the H1 still loads instantly (no stagger); only the dot-breathing is replaced by a static arrangement.

---

## 3. THE LOAD ANIMATION (exact timeline, ms)

A calligraphic settling — ink finding the page. `t=0` is `DOMContentLoaded` + fonts ready (`document.fonts.ready.then(start)`; if fonts hang >400ms, start anyway).

| t (ms) | what | from → to | easing | dur |
|---|---|---|---|---|
| 0 | Canvas already painted black-paper field at **rest target, opacity 0**. Particles pre-seeded at their drift home positions. | — | — | — |
| 0–900 | **Ink-in.** Per-particle alpha ramps 0→base over a staggered window: each particle's start delay = `i / N * 600ms`, ramp 300ms. Reads as ink blooming across the sheet from top-left to bottom-right (seed particles sorted by `x+y`). | α 0→base | `easeOutCubic` | 900 |
| 200 | Kicker fades+rises. | opacity 0→1, `translateY(8px→0)` | `--ease` | 600 |
| 320 | H1 line 1 fades+rises. | same | `--ease` | 700 |
| 420 | H1 line 2. | same | `--ease` | 700 |
| 560 | Lede. | opacity 0→1, `translateY(6px→0)` | `--ease` | 650 |
| 720 | Input fades+rises, then a one-time **focus pulse**: a 1px `--anchor` ring expands `box-shadow:0 0 0 0 → 0 0 0 4px (anchor@0%)` and fades, 600ms, drawing the eye to where to type. Input is NOT auto-focused (would pop mobile keyboard). | opacity 0→1 | `--ease` | 650 |
| ~900 | **Breathing begins.** Once ink-in completes the global drift/breathe loop (which has been running but masked by the ink-in alpha ramp) is now fully visible. | — | — | continuous |

The page never shows a blank flash: canvas paints frame 1 with alpha 0 immediately, type is `opacity:0` in CSS and animated up. Total choreography settles by ~1.4s; nothing blocks interaction (input is live from t=720).

---

## 4. CANVAS PARTICLE SYSTEM

### 4a. Setup & DPR
```js
const cvs = document.getElementById('field');
const ctx = cvs.getContext('2d', { alpha:true });
let DPR = Math.min(window.devicePixelRatio || 1, 2);   // CAP at 2 — 3x retina kills fill-rate
function resize(){
  const w = cvs.clientWidth, h = cvs.clientHeight;
  cvs.width  = Math.round(w * DPR);
  cvs.height = Math.round(h * DPR);
  ctx.setTransform(DPR,0,0,DPR,0,0);   // draw in CSS px
  W = w; H = h;
}
```
Canvas is `aria-hidden="true"`, `position:absolute; inset:0; z-index:1; pointer-events:none` (cursor interaction read from a window listener, not the canvas, so DOM controls stay clickable).

### 4b. Particle count & colour distribution
- **N = 3600** on desktop (≥1024px), **2200** on tablet, **1200** on phone (<640px) — read `innerWidth` once at init. Caps keep the rAF loop ≤4ms/frame even on integrated GPUs.
- Each particle is permanently assigned a **subject** (and thus colour). Distribution is **weighted by lesson count across the FULL 72-subject catalogue**, not just the 25 named. Implementation: build a cumulative-weight table from the 25 named subjects (their real lesson counts) PLUS a synthetic `"other"` bucket weighted `~1800` (the long tail of the 72) coloured in low-saturation neutral-greys drawn from `--text-muted`/`--border` family so the tail reads as "the rest of the library" without competing. Roll `Math.random()` against the cumulative table to pick each particle's subject.
- Colours stored as `{r,g,b}` parsed once from the subject hex. Particles are drawn at **base alpha 0.34** when "in the field" (un-chosen), nudged per-particle ±0.06 by a static random so the field has tonal grain (ink density varies — looks hand-laid, not printed).

### 4c. Particle struct (home position = drift anchor on a loose grid)
```js
// jittered grid so the field fills evenly but never looks gridded
function makeParticles(){
  const ar = W/H, cols = Math.round(Math.sqrt(N*ar)), rows = Math.ceil(N/cols);
  let i=0; const P=[];
  for(let r=0;r<rows;r++) for(let c=0;c<cols && i<N;c++,i++){
    const hx = (c+0.5)/cols * W + (Math.random()-.5)*(W/cols)*0.9;
    const hy = (r+0.5)/rows * H + (Math.random()-.5)*(H/rows)*0.9;
    const subj = pickSubjectByWeight();
    P.push({
      hx, hy,                      // home (drift centre)
      x:hx, y:hy,                  // live position
      px:hx, py:hy,                // (for converge lerp source)
      ph: Math.random()*Math.PI*2, // breathe phase
      sp: 0.5 + Math.random()*0.7, // breathe speed mult
      amp: 2.2 + Math.random()*2.6,// breathe amplitude px
      r: 0.8 + Math.random()*0.9,  // dot radius (ink speck)
      col: subj.rgb, subj: subj.slug,
      a: subj.baseA + (Math.random()-.5)*0.12,
      // converge fields, set when chosen:
      tx:null, ty:null, chosen:false, dim:0   // dim 0→1 = receding
    });
  }
  return P;
}
```

### 4d. Per-frame update (the drift/breathe + cursor + state lerps)
Time-based, not frame-based, so motion is identical at 60/120Hz. `dt` clamped.
```js
let t=0;
function frame(now){
  const dt = Math.min((now - last)/1000, 0.033); last = now; t += dt;
  ctx.clearRect(0,0,W,H);
  for(let k=0;k<P.length;k++){
    const p=P[k];
    if(p.chosen){
      // ---- CONVERGE: ease toward cluster target ----
      p.x += (p.tx - p.x) * (1 - Math.pow(0.0016, dt));  // ~ critically-eased follow
      p.y += (p.ty - p.y) * (1 - Math.pow(0.0016, dt));
      // tiny living jitter once arrived so the cluster breathes, not freezes:
      p.x += Math.sin(t*0.8 + p.ph) * 0.18;
      p.y += Math.cos(t*0.7 + p.ph) * 0.18;
    } else {
      // ---- DRIFT/BREATHE: gentle Lissajous around home ----
      const bx = Math.sin(t*0.18*p.sp + p.ph) * p.amp;
      const by = Math.cos(t*0.15*p.sp + p.ph*1.3) * p.amp;
      let tx = p.hx + bx, ty = p.hy + by;
      // ---- CURSOR: faint repulse within 90px, max 14px push ----
      if(mouseOn){
        const dx = tx-mx, dy = ty-my, d2 = dx*dx+dy*dy;
        if(d2 < 8100){ const d=Math.sqrt(d2)||1, f=(90-d)/90*14; tx+=dx/d*f; ty+=dy/d*f; }
      }
      p.x += (tx - p.x) * (1 - Math.pow(0.02, dt));   // smooth, not snappy
      p.y += (ty - p.y) * (1 - Math.pow(0.02, dt));
      // recede if a different subject was chosen (dim ramps toward 1):
      if(anyChosen) p.dim += (1 - p.dim) * (1 - Math.pow(0.25, dt));
      else          p.dim += (0 - p.dim) * (1 - Math.pow(0.25, dt));
    }
    // ---- DRAW ----
    const baseA = p.chosen ? Math.min(p.a*2.1, 0.92)        // chosen specks BRIGHTEN
                           : p.a * (1 - p.dim*0.78);        // others fade toward 22% of base
    if(baseA < 0.012) continue;
    ctx.globalAlpha = baseA;
    ctx.fillStyle = p.chosen
      ? `rgb(${p.col[0]},${p.col[1]},${p.col[2]})`
      : `rgb(${p.col[0]},${p.col[1]},${p.col[2]})`;
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.chosen ? p.r*1.25 : p.r, 0, 6.283);
    ctx.fill();
  }
  ctx.globalAlpha = 1;
  raf = requestAnimationFrame(frame);
}
```
- **Drift model:** each speck orbits its home on a slow Lissajous, amplitude 2.2–4.8px, period ~35–60s (`t*0.15–0.18`) — a *breath*, not a flutter. Lerp factor `1-0.02^dt` ≈ 0.99/frame → silky.
- **Cursor:** soft radial repulse, radius 90px, max displacement 14px, falls off linearly. Faint by design — "the ink notices you." Disabled on touch (`pointercoarse`).
- **Render order:** chosen specks are drawn LAST (push chosen indices to a second pass, or sort once on pick) so they sit visually on top of the dimmed field. Cheapest: maintain a `chosen[]` index array, draw field first then chosen.
- No blending/shadow/glow on the speck itself (fill-rate + the "no glossy" rule). The "glow" of a cluster is *emergent* from density + brightened alpha, not a shadow.

---

## 5. THE PICKER (DOM, keyboard-first)

### 5a. Input
A single text input, `--font-head`, `1rem`, `padding:.85rem 1rem`, `background:#fff`, `border:1px solid var(--border-light)`, `border-radius:--radius-sm`, `box-shadow:var(--shadow-sm)`, `max-width:480px; margin:0 auto`. Placeholder: `Add a subject — e.g. Biology, History…`. Focus → `border-color:var(--anchor); box-shadow:0 0 0 3px color-mix(in srgb,var(--anchor) 18%,transparent)` (the focus-visible ring, AA-visible). A small unicode `+` (`＋` U+FF0B, or an inline 1-path `<svg>`) sits left of the placeholder at `--text-muted` — drawn as inline SVG, **never a CSS data-URI** (per the gotcha).

### 5b. Suggestion list (combobox pattern, ARIA-correct)
- Input is `role="combobox" aria-expanded aria-controls="sg-list" aria-autocomplete="list"`.
- As the student types, filter the 25 named subjects by case-insensitive substring; render up to 6 in a `role="listbox" id="sg-list"` directly below the input: `#fff`, 1px border, radius 6, `--shadow-md`. Each row `role="option"`: subject name (`--font-head` 600) + a quiet right-aligned `--text-muted` `{n} lessons`. NO colour chip on the row (banned idiom) — the colour appears only once chosen, as the left-rule on the shelf.
- Keyboard: `↓/↑` move `aria-activedescendant` through options (highlighted row = `background:var(--border-lighter)`); `Enter` selects the active (or first) option; `Esc` closes the list. Fully operable without a mouse.
- On select: clear the input, collapse the list, fire `addSubject(slug)`.

### 5c. Per-subject board (chosen on the shelf, not in search)
Board is **per subject**. When a subject is added it lands on the shelf (§5d) with a board still unset, showing a compact inline `<select>` (native, styled minimally: `--font-head .82rem`, hairline border, radius 6, `--text-secondary`) seeded with that subject's real boards (e.g. History → AQA / Edexcel / OCR / Eduqas; Maths → AQA / Edexcel / OCR / Eduqas; single-board subjects show the lone board as static text, no select). Default to the most-common board but leave it changeable. The board choice does NOT change the converge (it's catalogue metadata for the eventual shelf); it just records what the student sits. Keyboard: `<select>` is natively operable; `aria-label="Exam board for {subject}"`.

### 5d. The shelf (chosen subjects)
Replaces nothing — it grows in a list below the input, `margin-top:1.25rem`, `max-width:480px; margin-inline:auto; text-align:left`. Each chosen subject is a **row** (the `.key-fact` idiom — the ONE place structure carries subject colour):
```
[3px accent left-rule] [8%-accent tint bg] [radius 0 6 6 0]
  Biology                         Edexcel ▾        ✕
  54 lessons · brightening into your shelf
```
- Row: `display:flex; align-items:center; gap:.75rem; padding:.7rem .9rem; border-left:3px solid {accent}; background:color-mix(in srgb,{accent} 8%,#fff); border-radius:0 var(--radius-sm) var(--radius-sm) 0; margin-bottom:.5rem;`
- Subject name `--font-head` 600 ink; sub-line `--font-read` italic `.85rem` `--text-muted`.
- Right side: the board `<select>` (or static board text) + a remove `✕` button (`--text-muted`, `background:none; border:none`, hover ink, `aria-label="Remove {subject}"`, `border-radius:--radius-sm`, focus ring). Removing fires `removeSubject` → its specks release back to the field (chosen=false, dim eases back to 0).
- Rows animate in: `opacity 0→1, translateY(6px→0)`, 400ms `--ease`. This is the *only* accent colour in the resting UI, and it's load-bearing structure (the left-rule names which constellation just formed), so it's compliant.

---

## 6. PICK → CONVERGE (the gravitational moment)

When `addSubject(slug)` fires:

1. **Select that subject's specks.** Iterate `P`, mark `p.chosen=true` for every `p.subj===slug`. (~weighted count; Biology ≈ N × 54/totalWeight ≈ 70–110 specks — enough to read as a cluster.)
2. **Assign cluster targets.** All chosen subjects share ONE settling region: a soft disc centred at `(cx, cy)` where `cx=W/2`, `cy = consoleTop - 90` (just above the H1, in the upper margin). When multiple subjects are chosen, partition the disc into **angular wedges** — subject *j* of *m* chosen gets the wedge `[j/m, (j+1)/m]·2π` — so each constellation occupies its own arc and the colours don't muddle. Within a wedge, scatter targets by golden-angle for even, organic packing:
```js
function assignTargets(){
  const chosenSubs = order;                 // array of chosen slugs, in pick order
  const m = chosenSubs.length;
  const R = Math.min(W,H) * 0.20;           // cluster radius
  const cx = W/2, cy = consoleTopY - 90;
  // per-subject running index
  const idx = {}; chosenSubs.forEach(s=>idx[s]=0);
  for(const p of P){
    if(!p.chosen){ p.tx=p.ty=null; continue; }
    const j = chosenSubs.indexOf(p.subj);
    const n = idx[p.subj]++;
    const wedge0 = (j/m)*Math.PI*2, wedgeW = (1/m)*Math.PI*2;
    // golden-angle radial fill inside the wedge
    const gr = Math.sqrt((n+0.5)/ subjectCounts[p.subj]) * R;  // 0..R, denser centre
    const ga = wedge0 + (n*2.39996 % wedgeW);                  // golden angle, wrapped to wedge
    p.tx = cx + Math.cos(ga)*gr + (Math.random()-.5)*4;
    p.ty = cy + Math.sin(ga)*gr*0.82 + (Math.random()-.5)*4;   // 0.82 = gentle vertical squash
  }
}
```
3. **The transition.** Per §4d, chosen specks lerp toward `(tx,ty)` with factor `1-0.0016^dt` (a firm but eased pull — effective ~92% closed/sec, visually arriving in ~700–900ms). Simultaneously their alpha ramps to `min(base*2.1,.92)` and radius ×1.25 — they **brighten and thicken** as they gather (ink pooling). Easing reads as calligraphic: fast initial draw-in, long soft settle (the `pow(k,dt)` follow is inherently ease-out).
4. **Unchosen specks recede.** `anyChosen` flips true → every un-chosen speck's `dim` eases 0→1 (factor `1-0.25^dt`, ~0.6s), dropping its alpha to `base × 0.22` and slowing/loosening its drift slightly (multiply amp by `1-0.4*dim` if desired). They do NOT leave the canvas — the rest of the library stays faintly present (the promise is "just yours," not "we deleted everything"), a quiet grey-ish ghost field behind the bright cluster.
5. **The constellation names itself.** 250ms after the cluster begins gathering, a DOM label fades in beside the cluster (`position:absolute` over canvas, anchored to the wedge's outer edge): the subject name in `--font-head` 600 `.9rem` ink + a hairline 14px tick mark in the subject accent pointing at the cluster. Fade `opacity 0→1, translateX(-4px→0)`, 500ms `--ease`. With multiple subjects, each label sits at its wedge's outer angle; on crowding (>4) labels stack to a compact legend below the cluster instead (name + 6px accent dot). *This dot/tick is accent-coloured but it is a data label pointing at data — compliant, like the canvas colour.*
6. **De-select** (✕ or board removal): `p.chosen=false` for that subject; `tx/ty` nulled; specks ease home (the same drift lerp recaptures them — `x` lerps back toward `hx+breathe`). Targets for the remaining subjects are re-assigned (`assignTargets()` re-runs so wedges re-partition for the new `m`). Label fades out 300ms.

**Multi-pick feel:** each new subject is its own small gravitational event — its wedge appears, existing wedges narrow to make room (their targets re-lerp over ~500ms), so the constellation visibly *reorganises* to admit the newcomer. Satisfying, legible, never chaotic.

---

## 7. CHOSEN-STATE RESOLUTION (the CTAs + shelf payoff)

Once `chosen.length >= 1`, a resolution block fades up below the shelf (`opacity 0→1, translateY(8px→0)`, 500ms `--ease`, 200ms after the first pick settles):

- **Headline beat** (`--font-head` 600, `1.05rem`, ink, centred): `That's your shelf — {n} subjects, {totalLessons} lessons, just yours.` (numbers live-counted from the chosen subjects' real lesson counts.)
- **Primary CTA** (the one solid-anchor button, reused styling from masthead but larger): **Create your free account** — `--anchor` fill, `#fff`, radius 6, `padding:.7rem 1.4rem`, `font-weight:600`, `box-shadow:var(--shadow-sm)`; sub-label beneath in `--font-read` italic `.85rem` `--text-muted`: `Keep your shelf on every device.`
- **Quiet secondaries** (text buttons, hairline-underline-on-hover, `--text-secondary`, `--font-head` 500, separated by hairline dividers, centred under the primary): **Sign in** · **I have a school code**.
  - `Sign in` → real login route.
  - `I have a school code` → reveals a small inline input (slides down, 300ms) `Enter your school code` + a quiet **Continue** (anchor-text, not filled). This is the school-student path; no marketing.
- Copy is plain, warm, second-person; never salesy. No stats wall, no "how it works."

**No-account framing:** the account is sold as *earning a benefit you just built* ("keep your shelf on every device"), positioned AFTER the shelf exists, never as a gate. A student could ignore it and still proceed (the shelf + a quiet **Start revising →** ghost link could route to `/browse` with the chosen subjects in localStorage even unauthenticated — preserving today's no-login behaviour).

---

## 8. REDUCED MOTION (`@media (prefers-reduced-motion: reduce)`)

Detected at init via `matchMedia('(prefers-reduced-motion: reduce)').matches` AND respected live (listen for changes):
- **No drift, no breathe, no ink-in stagger.** Particles are placed at their home positions and drawn ONCE (single `frame()` call, no rAF loop). The field is a calm, static arrangement of specks.
- **Type appears instantly** (no fade/rise) — all `opacity:1` immediately.
- **Converge is an instant state change:** on pick, chosen specks are *teleported* to their targets (set `p.x=p.tx; p.y=p.ty`) and the canvas redrawn once; unchosen specks redrawn at dimmed alpha. No animated lerp, no rAF. The cluster simply *is* there. Labels appear with no fade.
- Cursor interaction disabled (would require a loop).
This keeps the wow's *meaning* (overwhelming whole → just yours) while removing all vestibular motion.

---

## 9. NO-JS FALLBACK

Inside `<noscript>` (and as the default DOM that JS enhances): the canvas is `display:none` (it's useless without JS), and the console shows a **plain, fully-usable picker**:
- The H1 + lede (static).
- A real `<form method="get" action="/browse">` with a `<select multiple>` (or a list of labelled `<input type="checkbox">` rows) listing the 25 subjects, each with its own board `<select>`. Submit → `/browse?subjects=…`.
- All three resolution CTAs render as plain `<a>` links to `/signup`, `/login`, `/school-code`.
No animation, no canvas — but a student on a JS-blocked browser can still pick subjects + boards and proceed. Progressive enhancement: JS, on load, hides the static form and shows the canvas-driven console.

---

## 10. KEY JS SNIPPETS (the hard parts)

**(a) Weighted subject pick** — builds the catalogue-true distribution:
```js
const SUBJECTS = [
  {slug:'maths', name:'Mathematics', hex:'#3f5e78', lessons:48, boards:['AQA','Edexcel','OCR']},
  {slug:'combined-science', name:'Combined Science', hex:'#4f7a6a', lessons:78, boards:['AQA','Edexcel','OCR']},
  {slug:'biology', name:'Biology', hex:'#5b8a63', lessons:54, boards:['AQA','Edexcel','OCR']},
  /* …all 25 named subjects… */
];
const OTHER = {slug:'other', name:'', hex:'#9a968e', lessons:1800, boards:[]}; // the 47-subject long tail, neutral grey
const POOL = [...SUBJECTS, OTHER].map(s=>({...s, rgb:hexToRgb(s.hex), baseA: s.slug==='other'?0.22:0.34}));
let acc=0; const cum = POOL.map(s=>({s, hi: acc+=s.lessons})); const TOTAL=acc;
function pickSubjectByWeight(){ const r=Math.random()*TOTAL; for(const c of cum) if(r<c.hi) return c.s; return POOL[0]; }
function hexToRgb(h){ const n=parseInt(h.slice(1),16); return [n>>16&255, n>>8&255, n&255]; }
```

**(b) Add / remove a subject** (drives both DOM shelf + canvas state):
```js
const order = [];                          // chosen slugs in pick order
function addSubject(slug){
  if(order.includes(slug)) return;
  order.push(slug);
  for(const p of P) if(p.subj===slug) p.chosen=true;   // claim its specks
  anyChosen = order.length>0;
  assignTargets();                          // re-partition wedges for new m
  if(reduceMotion){ snapChosenToTargets(); drawOnce(); }
  renderShelf(); renderResolution(); spawnLabel(slug);
}
function removeSubject(slug){
  order.splice(order.indexOf(slug),1);
  for(const p of P) if(p.subj===slug){ p.chosen=false; p.tx=p.ty=null; }
  anyChosen = order.length>0;
  assignTargets();
  if(reduceMotion){ snapChosenToTargets(); drawOnce(); }
  renderShelf(); renderResolution(); removeLabel(slug);
}
```

**(c) Converge target assignment** — see §6 `assignTargets()` (golden-angle wedge fill). The two load-bearing numbers: cluster radius `R = min(W,H)*0.20`; vertical squash `0.82`; golden angle `2.39996 rad`.

**(d) The follow-lerp identity** used everywhere for frame-rate-independent easing — `value += (target - value) * (1 - Math.pow(retain, dt))`, where `retain` is the fraction *remaining* per second: `0.0016` ≈ a firm converge (~900ms settle), `0.02` ≈ silky drift, `0.25` ≈ a soft ~0.6s dim. This single primitive gives consistent eased motion at any refresh rate.

---

## 11. PERFORMANCE NOTES
- N capped (3600/2200/1200) + DPR capped at 2 → fill ~3600 `arc()`s/frame; on a mid laptop ~2–3ms. If a device reports `hardwareConcurrency<=4` AND mobile, drop to N=900.
- Single clear+redraw per frame; no per-particle shadow/blur; chosen drawn in a second cheap pass.
- Pause the rAF loop when the tab is hidden (`document.visibilitychange` → `cancelAnimationFrame`), resume on focus, re-seeding `last=performance.now()` so `dt` doesn't spike.
- `resize` debounced 150ms → `resize()` + `makeParticles()` re-seed (re-grid for new aspect) + `assignTargets()`.

---

## 12. WHY THIS WOWS IN ONE FIRST IMPRESSION
A 15-year-old lands and, before reading a word, watches ink bloom across warm paper into a living field of thousands of specks — instantly, wordlessly legible as *"this is a lot."* That is the felt experience of GCSE overwhelm, rendered. Then they type one subject and a hundred of those specks brighten, gather, and quietly label themselves into a single constellation while the rest dim to a ghost — the overwhelming whole becoming *just theirs*, in one eased, calligraphic beat. The product's entire thesis — narrowing — is not *described*, it is *performed*, and the student is the one who performs it. It feels premium and teacher-made because the colour only ever lives in data (the specks) and in one structural left-rule on the shelf, never wrapped decoratively around UI; the restraint is the credibility.

## RISKS
- **Cluster legibility with many subjects:** beyond ~5 picks the wedges crowd and colours can muddle into a brown smear. Mitigation: cap visible distinct clusters at ~6, switch labels to the stacked legend, and consider slightly increasing `R` per added subject (`R = min(W,H)*(0.18+0.012*m)`).
- **Mobile fill-rate:** 1200 specks on a budget Android can dip below 60fps; the `hardwareConcurrency` fallback to 900 + DPR cap is the guard. Test on a real low-end device.
- **Console-over-field contrast:** dense bright dots directly behind the H1 could hurt AA legibility during converge (cluster sits *above* the H1 by design, in the upper margin, specifically to avoid this — keep `cy = consoleTop-90`, never behind the text). If the field is ever too busy behind type, add a very subtle 0→`--bg-body` radial *masking* of the type's bounding box in canvas (a paper-coloured wash, not a decorative gradient) — but verify it doesn't read as a box.
- **`text-wrap:balance` + Schibsted at clamp sizes** can reflow oddly mid-load before fonts settle; gate the type-reveal on `document.fonts.ready` to avoid a FOUT jump under the dots.
"