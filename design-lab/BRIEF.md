# StudyVault Homepage — Design Brief
*Summer 2026 redesign · design-lab · build from this, clean*

## The one line
StudyVault is the **one-stop shop for GCSE revision**: tell it what you're sitting, and it strips away the noise — leaving just *your* subjects, on *your* exam boards, in one calm place.

## Audience
- **Primary: the student.** Year 10–11, 14–16, often stressed, usually on a phone.
- **Not the homepage's job:** schools, teachers, parents. They get a separate "For schools" page. Here they get a *quiet door*, never a pitch.

## The job of the page
Get a student from landing → "revising in just my stuff" in under a minute. **Launchpad, not sales pitch.** Friction is already near-zero (free, no login). The page's real job is to remove the *cognitive* friction — the tab-hopping, the "is this even my board?", the overload — not to add marketing.

## The one thing they remember
> "I don't have to hunt across five sites and guess what's relevant. I tell it my subjects and boards once, and it's all here — filtered to exactly mine."

- The product's hero is the **wizard picker** — the act of narrowing down.
- Breadth (72 subjects · 4 boards · 4,400 lessons) is the **proof**, never the headline. Leading with breadth would echo the very overload we remove.

## Message hierarchy
1. Stop tab-hopping. One place for everything you're revising.
2. Tell us what you're sitting → you only ever see yours.
3. And it's genuinely all here: lessons, practice that marks itself, podcasts, a plan.
4. Built by a teacher, written to your exact spec. Free.

## Tone & personality
Calm · warm · inviting · clearly teacher-designed — but **professional, not childish**. The page must *embody* the promise: decluttered, generous whitespace, clear hierarchy. **The medium is the message** — a noisy, busy page would contradict a product whose whole point is removing overload.

## Visual language (carried from redesign v2)
- Neutral warm base `#f7f6f4`, ink `#1d1c1a`, navy anchor `#3f5e78`, **muted per-subject accents**.
- Sans headlines (Schibsted Grotesk) + serif body (Literata). Sizes up. **No drop caps.**
- **Tile hierarchy, not uniform buttons.** Soft radii, soft shadows, soft-close easing `cubic-bezier(.16,1,.3,1)`.
- Warmth / teacher-made carried by hand-drawn **accents** (marker highlight, sketched line icons) used *sparingly*.
- Rejected: paper texture, "crisp" sterile, purple-gradient AI-slop.

## Page structure (narrative arc)
*Juggling everything → tell us what you're sitting → here's just your stuff → it's genuinely all here → teacher-made & free → go.*

1. **Masthead** — minimal: logo · How it works · For schools (quiet) · I have a school code.
2. **Hero** — the narrowing promise + a working **"build your shelf" picker**. Primary CTA launches the wizard.
3. **Your shelf** — the calm payoff: just *your* chosen subjects, as tiles.
4. **All in one place** — lessons / practice that marks itself / podcasts / planner. Framed as "no more tab-hopping."
5. **Why trust it** — teacher-built, written to your spec, free. Light.
6. **Reassurance stats** — breadth as proof, not boast.
7. **Closing CTA** — back to the picker.
8. **Footer.**

## Success looks like
A 15-year-old lands, instantly gets *"oh — this is all my revision, in one place,"* picks their subjects + boards, and is in a lesson. No marketing read, no account.

## Constraints
- Must fold back into the real platform (`index.html`), existing tokens/fonts, real wizard + slug machinery.
- **Mobile-first** — most students arrive on a phone.
- Accessible: WCAG AA, `prefers-reduced-motion`, full keyboard.
- Light and fast — a calm page should *feel* instant.

## Consistency with the rebuilt reader — NON-NEGOTIABLE
The homepage must feel like the same product as the rebuilt lesson pages. Source of truth: **`css/reskin.css`, `body[data-skin="reader"]`.** Match these exactly:

| | Value |
|---|---|
| Base / card | `--bg-body:#f7f6f4` · `--bg-card:#fff` |
| Text | primary `#1d1c1a` · secondary `#54524d` · muted `#7f7c75` |
| Borders | `--border-light:#e6e4e0` · `--border-lighter:#f0eeea` |
| Accent | **one muted accent per subject** (`--subject-accent`); neutral page anchor `#566a72`; `--accent-light` = accent 8% → white; badge = translucent accent (`accent 14% → transparent`) |
| Radius | `--radius:8px` · `--radius-sm:6px` (NOT the old 14–20px) |
| Shadows | flat by default (`box-shadow:none`); subtle only — `--shadow-sm 0 1px 3px /.06` · `--shadow-md 0 4px 12px /.08` · `--shadow-lg 0 8px 24px /.10` |
| Fonts | head/UI `Schibsted Grotesk` · read `Literata`. UI labels uppercase, `.12–.14em` |
| Easing | **`cubic-bezier(.22,1,.36,1)`** for transform/reveal |
| Card idiom | `bg-card + 1px border-light + radius 8 + shadow:none`; hover → `translateY(-3px) + shadow-lg + border-color accent-35%` |
| Links | accent colour, 1px underline, 2px offset, decoration-colour accent-45% → full accent on hover |

No drop caps. No paper texture. No heavy/glossy shadows. The current production `index.html` (Inter, bright blues) is the OLD look — do **not** match it.

## Open decisions — RESOLVED
1. **Hero picker fidelity** → **(a) faux-live "build your shelf" picker** in the hero. Demonstrates the narrowing, then CTA hands to the real wizard.
2. **Sketches' fate** → **(b) accents only.** Warmth via the marker highlight + sketched line icons (and at most one or two whisper-faint doodles), so the page stays visibly decluttered — the medium matches the "removes overload" message. Full desk background retired. *(Easy to reintroduce more sketch presence if Tom wants it back.)*

## Build artifact
`design-lab/home.html` — built fresh from this brief. (Prior breadth-led concept `home-sketch.html` kept for reference.)
