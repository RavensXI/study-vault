# Practice Renderer Audit — `practice.html` + `practice-loader.js`

Audited against the live `practice.html` (lines 1–5400+) and `js/practice-loader.js`.
Date: 2026-05-14. Branch: `subject/statistics-aqa`.

---

## 1. `chart` field (Chart.js)

**Supported — yes.** Every problem may carry a `chart` object. The renderer (lines 4177–4204 of `practice.html`) does:

```js
window._currentChart = new Chart(ctx, {
  type: p.chart.type,
  data: p.chart.data,
  options: Object.assign({ responsive: true, maintainAspectRatio: true,
    plugins: { legend: { display: p.chart.showLegend || false } }
  }, p.chart.options || {})
});
```

The canvas is capped at `max-height: 180px` inline. The container element is `#problem-chart-container`.

**Chart types confirmed wired:**
- `bar` — standard vertical/horizontal bar charts
- `line` — line charts, time series, frequency polygons, cumulative frequency curves
- `scatter` — scatter diagrams (x/y pairs, no connecting line by default)
- `pie` — pie/sector charts
- `doughnut` — doughnut charts
- `boxplot` — box-and-whisker (via `@sgratzl/chartjs-chart-boxplot` plugin, see §4)

Chart.js 4 natively supports all of the above. "histogram" is not a named type — use `bar` with `barPercentage: 1.0, categoryPercentage: 1.0` and pre-calculated frequency density values on the y-axis.

**What the loader does NOT do:**
- It does not deep-merge `options` intelligently beyond `Object.assign` — put all axis config inside `p.chart.options`.
- It does not auto-label axes; agents must set `options.scales.x.title` and `options.scales.y.title` explicitly.

---

## 2. `display` field — HTML support

**Full HTML injection — yes.** Line 4171:

```js
eqEl.innerHTML = formatDisplay(p.display || '');
```

`formatDisplay` (lines 4078–4094) does light formatting (auto line-breaks after colons, paragraph breaks before instruction verbs, non-breaking spaces around `=` signs). It does **not** sanitise HTML — tags pass through verbatim.

This means the `display` field accepts:
- `<table>` — renders fully (essential for two-way tables, frequency tables, stem-and-leaf)
- `<svg>` — renders inline (Venn diagrams, tree diagrams, pictograms)
- `<pre>`, `<code>` — renders as-is (back-to-back stem-and-leaf)
- `<strong>`, `<em>`, `<br>`, `<span>` — standard inline formatting

**Caveat:** `formatDisplay`'s auto–line-break rule replaces `: ` followed by a digit with `:<br>` — this can break data tables if used in the same string as a raw colon. Wrap table content in a `<table>` tag inside `display` instead of relying on the colon heuristic.

---

## 3. `image` field

**Not confirmed in `practice-loader.js` or `practice.html`.** The Geography Skills panel uses `problem.image` to display OS map images in a separate panel (see `renderChartPanel` region), but that is panel-specific. There is no `<img>` injection from `problem.image` in the main problem card renderer. **Do not rely on an `image` field for Statistics problems.** Use inline `<svg>` in `display` instead.

---

## 4. `chartjs-chart-boxplot` plugin

**Loaded on `practice.html` — yes.** Line 12:

```html
<script src="https://cdn.jsdelivr.net/npm/@sgratzl/chartjs-chart-boxplot@4/build/index.umd.min.js"></script>
```

Box plots (`type: "boxplot"`) are available on `practice.html`. The plugin expects data as arrays of raw values per dataset (it computes Q1/median/Q3/whiskers internally) **or** pre-computed summary objects `{ min, q1, median, q3, max }`. Use pre-computed form for Statistics since exam questions specify exact quartile values.

Box plots are NOT available on `lesson.html` (article format). Box plot charts in `display` should use inline SVG instead if the lesson is article format.

---

## 5. Inline SVG in `display`

**Supported.** Since `display` is injected via `innerHTML` without sanitisation, inline `<svg>` tags render. This is the correct mechanism for:
- Venn diagrams (2 or 3 overlapping circles with counts)
- Tree diagrams (branching probability trees)
- Pictograms (symbol grids with a key)

Keep SVG `viewBox` defined and `width="100%"` so it scales inside the problem card.

---

## Summary table — what to use for each chart type

| Chart type | Mechanism | Notes |
|---|---|---|
| Bar chart | `chart` field, `type:"bar"` | Set axis titles in options |
| Histogram | `chart` field, `type:"bar"` with `barPercentage:1,categoryPercentage:1` | y-axis = frequency density; label each bar with class boundary |
| Pie / sector | `chart` field, `type:"pie"` | Set `showLegend:true` for label display |
| Line chart / time series | `chart` field, `type:"line"` | |
| Frequency polygon | `chart` field, `type:"line"` with `fill:false`, midpoints as x labels | |
| Cumulative frequency | `chart` field, `type:"line"` | x = upper class boundary, y = CF |
| Scatter diagram | `chart` field, `type:"scatter"` | Data as `{x,y}` pairs; add `tension:0` |
| Box plot | `chart` field, `type:"boxplot"` | Plugin loaded; use pre-computed `{min,q1,median,q3,max}` |
| Two-way / frequency table | `<table>` HTML in `display` field | Use `.data-table` class |
| Stem-and-leaf (single) | `<table class="stem-leaf">` in `display` | See template in `PRACTICE_PIPELINE.md` |
| Stem-and-leaf (back-to-back) | `<table class="stem-leaf stem-leaf--btb">` in `display` | See template |
| Venn diagram | Inline `<svg class="venn-diagram">` in `display` | 2 or 3 circles; label counts |
| Tree diagram | Inline `<svg class="tree-diagram">` in `display` | Branch lines + probability labels |
| Pictogram | Inline `<svg class="pictogram">` in `display` | Symbol grid + key row |
| Population pyramid / choropleth | Inline `<svg>` or a descriptive `<table>` — case-by-case | Complex; prefer MCQ proxy where possible |
