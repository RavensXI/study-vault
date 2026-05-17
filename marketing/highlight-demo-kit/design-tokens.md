# StudyVault design tokens

The visual language Designer should match when producing marketing assets for the highlight feature.

## Colours

### Page chrome

| Token | Hex | Use |
|---|---|---|
| `--bg-page` | `#faf8f5` | Whole-page background (warm cream) |
| `--bg-card` | `#ffffff` | Cards, popovers, the article surface in Highlight Mode |
| `--text-primary` | `#2d2a26` | Body text, headings |
| `--text-secondary` | `#5d564b` | Supporting text |
| `--text-muted` | `#8a8276` | Labels, hints |
| `--border-lighter` | `rgba(45,42,38,0.08)` | Card borders |

### Subject accents (sample — there are ~25 total in `css/style.css`)

| Subject | Accent |
|---|---|
| History | `#c44536` |
| Geography | `#059669` |
| Business | `#b45309` |
| Computer Science | `#2563eb` |
| Statistics | `#0369a1` |
| Religious Studies | `#1e40af` |
| Drama | `#6b21a8` |
| Sport Science | `#ea580c` |

Use one strong subject accent per marketing asset rather than mixing several — it reads as "this is the History page" not "this is a generic edtech tool".

### Highlight colours (the four marker pens)

| Name | Mark BG (light mode) | Swatch (saturated) | Dark-mode mark BG |
|---|---|---|---|
| Yellow | `#fef9c3` | `#fef08a` | `rgba(234,179,8,.55)` |
| Green  | `#dcfce7` | `#86efac` | `rgba(34,197,94,.45)` |
| Pink   | `#fce7f3` | `#f9a8d4` | `rgba(236,72,153,.45)` |
| Blue   | `#dbeafe` | `#93c5fd` | `rgba(59,130,246,.5)` |

The swatches in the popover are saturated; the actual highlight that appears on the text is the lighter "mark BG" tone — so highlighted text stays readable.

## Typography

| Family | Used for |
|---|---|
| **Inter** (400/500/600/700) | All UI: buttons, body, labels, navigation |
| **Source Serif 4** (400/500/600/700) | Lesson titles, section headings, marketing headlines |

Load from Google Fonts:
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:wght@400;500;600;700&display=swap" rel="stylesheet">
```

## Geometry

| Token | Value |
|---|---|
| Card border-radius | `16px` (`--radius`) |
| Pill border-radius | `999px` |
| FAB border-radius | `999px` |
| Popover border-radius | `14px` |
| Mark border-radius | `3px` |
| Container max-width | `1160px` (`--page-max`); article body ~760px |

## Shadows

| Token | Value |
|---|---|
| Soft (cards) | `0 1px 3px rgba(45,42,38,.06)` |
| Medium | `0 4px 12px rgba(45,42,38,.08)` |
| FAB | `0 10px 24px rgba(20,18,15,.18)` |
| Modal | `0 -20px 48px rgba(20,18,15,.18)` (mobile bottom sheet) |
| Highlight Mode article lift | `0 12px 40px -8px rgba(45,42,38,.25), 0 2px 8px rgba(45,42,38,.08)` |

## Animation

All entrance / state-change animations use a **soft-close** ease:

```css
cubic-bezier(0.16, 1, 0.3, 1)
```

| Animation | Duration | Easing |
|---|---|---|
| Highlight sweep (left → right colour reveal) | `420ms` | `cubic-bezier(0.4, 0, 0.2, 1)` |
| Sweep stagger between marks of the same highlight | `45ms` per mark | linear |
| Popover slide in | `200ms` | `cubic-bezier(0.16, 1, 0.3, 1)` |
| FAB hover lift | `150ms` | linear-ish (`transform 150ms ease, filter 150ms ease`) |
| Mark flash on "jump to" | `1.4s` | `ease` |
| Reduced-motion users | All animations disabled — colour appears instantly |

## FAB (bottom-left highlight button)

* Pill shape, `999px` radius
* Background: subject accent (`--accent`), text white
* Padding `10px 14px`, icon + label inline
* Mobile (≤768px): label hidden, icon-only at `10px` padding
* Stacked layout on desktop (one button out of mode → two side-by-side in mode)
* Side-by-side on mobile to avoid overlapping the narration mini-player

## Popover (after a highlight is created)

* White card, `14px` radius, `1px` subtle border, soft shadow
* Top row: 4 saturated swatch buttons (Yellow / Green / Pink / Blue), 28×28, circular
* Middle: multi-line note textarea, `10px` radius, light fill `#faf8f5`
* Bottom row: bin icon (delete) + "Done" pill button (dark, primary)

## Cursor (in Highlight Mode)

Custom marker-pen SVG cursor. The pen body recolours to match the currently-selected highlight colour. Inline data-URI SVG; not referenced as a file.
