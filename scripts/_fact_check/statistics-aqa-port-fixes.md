# Statistics AQA — inherited practice-bank fixes ported from the Edexcel review (15 Sep 2026)

Source: Opus review of the Edexcel port (scratchpad stats_review/findings_*.json). 14 of 19 AQA practice lessons changed; backup of the pre-fix rows in the session scratchpad (_backup_aqa_practice.json).

# representing-data — AQA correction report

Unit: `representing-data`, lessons L01–L06 (AQA GCSE Statistics practice banks).
Source: `AQA_FINDINGS.md`. Output: `representing-data-LNN.aqa.fixed.json` (indent 1, `ensure_ascii=False`).
Scripts used: `_fix_representing_data.py` (apply), `_verify.py` (check), `_render.py` (draw).

22 findings are listed for this unit. **20 APPLIED, 2 n/a.**
7 additional edits are marked **EXTRA** — see "Extras" at the end.

---

## L01 — Tally Charts, Tabulation and Pictograms

| Finding | AQA index | Status | Evidence |
|---|---|---|---|
| gold[3]: stem asks "why" but every option answers yes/no | `gold[3]` (same) | **APPLIED** | Stem read "Which statement best describes why this is a misleading representation?" while options start "No — as long as the key…", "Yes — varying symbol sizes…". Stem now reads "Is this a misleading representation? Choose the statement that best explains your answer." |
| bronze[4].misconceptions[0]: feedback asserts a quarter symbol and 65, then contradicts itself with 70 | `bronze[4]` (same) | **APPLIED** | Old message: "…one quarter symbol (5). Total = 60 + 5 = 65. Re-check the picture: the partial symbol is a half, giving 3 × 20 + 0.5 × 20 = 70." Replaced with the single consistent HALF explanation. |
| gold[2]: the miscounted class cannot be determined | `gold[2]` (same) | **APPLIED** | Stem ended "A bundle of 5 was likely miscounted as 3. In which class is the error most likely?" The clause "Assuming the error is most likely in the class with the most tally bundles," is now inserted before the question. |
| silver[2]: chart y-min 50 / title "starts at 50" vs drawn axis starting at 60 | `silver[2]` (same) | **APPLIED** | Lowest SVG y-label is `>60</text>` at y=226 (the axis baseline); chart said `"min": 50`. Now `min: 60` and title "Reporter's bar chart (y-axis starts at 60)". |
| topic_links: prerequisite points at this same lesson | `topic_links` | **APPLIED** | `prerequisites` held `{"slug": "representing-data/1", "title": "Tally Charts, Tabulation and Pictograms"}` — L01 itself. Now `[]`. |

## L02 — Bar Charts, Pie Charts and Stem-and-Leaf Diagrams

| Finding | AQA index | Status | Evidence |
|---|---|---|---|
| bronze[3]: drawn January bars 45 / 30, walk reads 40 / 55 and subtracts the wrong way | `bronze[3]` (same) | **APPLIED** | SVG scale 3.333 px/unit from baseline y=226: Shop A rect height 150.0 → 45, Shop B 100.0 → 30 (Feb 166.7 → 50, 140.0 → 42). Walk step 0 now "Shop A = 45 and Shop B = 30"; step 2 `pre` "45 − 30 = ", hint "Subtract Shop B's January bar from Shop A's."; chart Shop A `[45, 50]`, Shop B `[30, 42]`. |
| silver[2]: drawn composite bar labels B 30 online / 10 in-store, walk quotes 45 and 15 | `silver[2]` (same) | **APPLIED** | The SVG prints the values itself: Product B blue `>30</text>`, red `>10</text>` (rect heights 157.5 → 30, 52.5 → 10 at 5.25 px/unit). Walk now "online 30 stacked on in-store 10", "Product B total = 30 + 10 = " → 40, "10 ÷ 40 = " → 0.25; chart Online `[20, 30]`, In-store `[20, 10]`. Answer 25 % unchanged. |
| silver[1].misconceptions[0]: eight ordered values listed (19 missing), yet 23 called the 5th | `silver[1]` (same) | **APPLIED** | Old list "15, 18, 20, 23, 27, 31, 34, 39" is 8 values; the stem-and-leaf gives nine (stem 1 → 5 8 9). Message now lists "15, 18, 19, 20, 23, 27, 31, 34, 39". |
| gold[5].misconceptions[0]: differences 5, 45, 2, 5 quoted from the chart object; drawn chart gives 10, 30, 10, 8 | `gold[5]` (same) | **APPLIED** | Drawn rect heights → North 40, 55, 45, 50 and South 30, 25, 35, 42. Message now "Jan = 10, Feb = 30, Mar = 10, Apr = 8 … (55 − 25 = 30)"; chart North `[40, 55, 45, 50]`, South `[30, 25, 35, 42]`. |
| gold[6]: stem asks "to 1 decimal place" but the answer 4.5 is exact | — | **n/a** | The AQA L02 gold tier has six items (indices 0–5) and no such stem. A whole-unit search found zero occurrences of "decimal place", "d.p." or "1dp" in L01–L03, L05 and L06; the single L04 hit is an unrelated item. The problem is absent from the AQA bank. |
| GENERIC: board named in student text | `gold[2].misconceptions[0]` and `[2]` | **APPLIED** | "For the AQA n=9 rule:" → "For the exam board's n=9 rule:"; "AQA Statistics uses (n+1)/4 interpolation:" → "The exam board uses (n+1)/4 interpolation:". These were the only two board names anywhere in the unit (case-insensitive sweep for AQA / Edexcel / Pearson / OCR / WJEC / Eduqas). |

## L03 — Frequency Polygons, Time Series and Line Charts

| Finding | AQA index | Status | Evidence |
|---|---|---|---|
| gold[5]: stem says A is always above B, but the drawn polygons cross at midpoint 30 | `gold[5]` (same) | **APPLIED** | Drawn A was 12, 14, 8, 4, 2 and B was 2, 4, 8, 14, 12 at x = 10…50 — equal at 30, then B above. The SVG is redrawn to six points: A = 4, 10, 18, 16, 8, 4 and B = 2, 6, 10, 8, 4, 2 at midpoints 5, 15, 25, 35, 45, 55. The y-axis labels became 0/5/10/15/20 on the same pixel rows so that 18 fits. The chart object already held exactly these values and is unchanged. |
| bronze[5]: walk asks for "Highest frequency = 11"; the drawn polygon peaks at 14 | `bronze[5]` (same) | **APPLIED** | Drawn heights 4, 10, 14, 8, 4 at midpoints 5…45 (13.125 px/unit, axis max 16). Walk step 0 now lists "4, 10, 14, 8 and 4"; step 1 `answer` 11 → 14, `done` "14 is the tallest."; chart data `[4, 10, 14, 8, 4]`. Solution 25 (the midpoint) unchanged. |
| bronze[2]: walk says 4, 9, 12, 8, 5 and a peak at midpoint 25; drawn 3, 8, 12, 7, 2 at 10, 30, 50, 70, 90 | `bronze[2]` (same) | **APPLIED** | Confirmed from the polyline: `94.6,181.0 179.8,106.0 265.0,46.0 350.2,121.0 435.4,196.0` → heights 3, 8, 12, 7, 2 at x = 10, 30, 50, 70, 90. Walk step 0, step 2 `done` and the misconception now say "midpoint 50"; chart labels `["10","30","50","70","90"]`, data `[3, 8, 12, 7, 2]`. Solution 12 unchanged. |
| gold[2]: drawn x-axis in seconds (0.1–0.7 s) while the chart object and feedback are in milliseconds | `gold[2]` (same) | **APPLIED** | SVG axis title "Reaction time (s, midpoint)" with ticks 0.1…0.7; points sit at 0.2, 0.3, 0.4, 0.5, 0.6. Misconception now "Untrained peaks at 0.3 s (more symmetric). Trained peaks at 0.5 s with more weight in higher times."; chart labels `["0.2"…"0.6"]` and x-title "Reaction time (s, midpoints)". Stem (an open command on an MC item) now reads "…Which statement correctly compares the two distributions, including skewness?" |

## L04 — Histograms and Frequency Density

| Finding | AQA index | Status | Evidence |
|---|---|---|---|
| silver[0] (HIGH): frequency density asked for with no frequency given; the walk invents 30 and the chart shows the answer | `silver[0]` (same) | **APPLIED** | Stem was "The histogram shows four bars with unequal class widths. Calculate the frequency density for the class 20–40." and the chart plotted `[2.5, 4.0, 1.5, 0.5]` — the third value is the answer. Stem now states the frequency; the `chart` key is deleted; misconception is "Class width = 40 − 20 = 20. Frequency density = 30 ÷ 20 = 1.5." (the author's "(You need to recover freq from a different bar first…)" note is gone). |
| gold[4].misconceptions[0]: feedback works from frequencies 30 and 30, the stem gives 16 and 8 | `gold[4]` (same) | **APPLIED** | Old: "Class 10–20 density = 30/10 = 3; class 20–40 density = 30/20 = 1.5. The wider bar must be shorter…". Now "16 / 10 = 1.6; … 8 / 20 = 0.4. The wider bar must be drawn a quarter of the height, not half." This also agrees with the keyed option ("density 0.4 vs 1.6"). |
| gold[6].guided_steps[1]: garbled step, tallest bar 18, heights 12/18/6 | — | **n/a** | The AQA L04 gold tier has six items (0–5) and no modal-class item. Whole-file search: "tallest" 0 hits, "modal" 0 hits. The problem is absent from the AQA bank. |
| gold[3]: chart plots the unknown bar at 14, the value the student must find | `gold[3]` (same) | **APPLIED** | Chart data was `[3.5, 14]` and the solution is 14. Data now `[3.5, 0]` and the second label is "20–30 (h = ?)". The chart object is kept rather than deleted because this stem still says "The histogram below has a bar for class 20–30 with height h", so the diagram must remain; the class interval is kept in the label because the student needs the width. |

## L05 — Cumulative Frequency and Box Plots

| Finding | AQA index | Status | Evidence |
|---|---|---|---|
| gold[0]: keyed option quotes School B median 165 and max 183; the drawn box plot shows median 168, min 152, max 180 | `gold[0]` (same) | **APPLIED** | Axis 140 at x=55, 185 at x=495 (9.778 px/unit). Drawn B was min 152, Q1 160, median 168, Q3 172, max 180; drawn A max was 182 while the chart object said 185. Seven SVG coordinates were changed (whiskers, caps, median line). Re-read from the corrected geometry: **School A min 145, Q1 155, median 162, Q3 170, max 185; School B min 148, Q1 160, median 165, Q3 172, max 183** — matching the chart object and the keyed option exactly. |
| bronze[2]: drawn min 5 / max 50 while the chart object says 10 / 55 | `bronze[2]` (same) | **APPLIED** | Axis 0 at x=55, 60 at x=495 (7.333 px/unit): min cap x=91.7 → 5, max cap x=421.7 → 50. Chart `min` 10 → 5, `max` 55 → 50. |
| bronze[4]: drawn Q1 45, median 58, Q3 72 while the chart object says 48, 62, 74 | `bronze[4]` (same) | **APPLIED** | Axis 20 at x=55, 100 at x=495 (5.5 px/unit): box rect x=192.5 → Q1 45, median line x=264.0 → 58, right edge 341.0 → Q3 72. Chart `q1` 45, `median` 58, `q3` 72. |
| bronze[4]: delete any empty `"hint": ""` key in guided_steps[0] | `bronze[4].guided_steps[0]` | **n/a (sub-item)** | That step carries only a `say` key — no `hint` at all. A whole-unit sweep found zero empty-string values in any of the six files. Nothing to delete. |

## L06 — Scatter Diagrams, Population Pyramids and Choropleth

| Finding | AQA index | Status | Evidence |
|---|---|---|---|
| bronze[1]: keyed "Moderate positive correlation" fits the drawn scatter, but the chart object data is nearly perfectly linear | `bronze[1]` (same) | **APPLIED** | Chart held (1,3), (2,5), (3,6) … (10,20) — effectively y = 2x, which would key as "Perfect positive". The SVG draws 11 scattered circles; at 21.5 px/unit in x and 4.4 px/unit in y they decode to the brief's list. Chart data replaced with (0,9), (2,1), (3,9), (6,24), (8,24), (10,29), (11,27), (13,42), (15,43), (17,44), (20,42). |

---

## Generic rules across the unit

- **Board names in student-facing text:** two occurrences found, both in `L02 gold[2]` misconception messages; both replaced with "the exam board". A case-insensitive sweep of all six fixed files now returns **0**.
- **Named HTML entities in plain-text fields:** **none to convert.** Every named entity in this unit (`&mdash; &ndash; &le; &lt; &ldquo; &rdquo; &rarr; &minus;`) sits inside an HTML-markup field — `method_card.content` in all six lessons, plus `tier_guides.silver.example.steps[*].content` and `worked_examples[1].steps[*].content` in L02. The generic rule explicitly excludes those. No entity was found in any `display`, `options`, `message`, `pre`, `hint`, `done`, `say`, `post`, `question`, `steps` or `exam_context` string outside an SVG or HTML block. Nothing inside an SVG was touched.

## Extras (beyond the wording of the brief)

Each of these is a residue of a finding the brief does name: after the named fix the same item still carried numbers that contradicted its own diagram or its corrected walk. They are listed separately so they are easy to review or revert.

| Where | Change |
|---|---|
| L02 `bronze[3].misconceptions[0].message` | "Shop A = 40, Shop B = 55. Difference = 55 − 40" → "Shop A = 45, Shop B = 30. Difference = 45 − 30". Left alone it contradicted the corrected walk and the drawn bars. |
| L02 `silver[2].misconceptions[0].message` | "45 + 15 = 60 … (15/60) × 100" → "30 + 10 = 40 … (10/40) × 100". Same reason. |
| L03 `bronze[5].misconceptions[0].message` | "highest frequency (11)" → "(14)", to match the corrected peak. |
| L03 `gold[2].chart` datasets | Untrained `[2,8,18,9,3]` → `[6,16,12,4,2]`, Trained `[1,5,10,14,10]` → `[2,4,10,14,10]`. The brief re-labelled this chart's axis in seconds but left the frequencies disagreeing with the drawn polygons; they now match, and they support the corrected "peaks at 0.3 s / 0.5 s" feedback. |
| L04 `silver[0].guided_steps[0].say` | "This bar's frequency is 30." → "This class has frequency 30." The brief deletes this item's chart, so "this bar" pointed at a diagram that no longer exists. |

## Departures from the brief's literal text

- Where the brief writes ASCII operators (`-`, `/`, `x`) the bank uses unicode (`−`, `÷`, `×`) in sibling strings of the same item, so the bank's characters were used (for example `45 − 30 = ` rather than `45 - 30 = `). Class intervals keep the file's en-dash (`20–40`, not `20-40`). The one exception is L04 `gold[4]`, whose original message already used a slash for division, so `16 / 10` and `8 / 20` are kept as written.
- L03 `bronze[2]` and `bronze[5]` guided step 0: the brief quotes only the sentence carrying the numbers. The AQA steps open with an extra teaching sentence ("The frequency is the height (the y-value) of each point." / "The modal class is the one with the highest frequency."), which is kept; only the numbers changed.
- L04 `gold[3]`: the brief offers "label the second bar `h = ?` **or** delete the chart object". The label route was taken (see the table above) and written as `20–30 (h = ?)` so the class width the student needs stays on the axis.
- L03 `gold[5]`: redrawing six points where five were drawn required adding one `<circle>` marker per series and moving the two series labels from x=412.0 to x=447.5. Y-axis tick labels changed from 0/4/8/12/16 to 0/5/10/15/20 on the identical pixel rows, because the target peak of 18 does not fit under an axis that stops at 16. No other structure changed.

---

## Validity and count check

All six fixed files parse as JSON, keep the top-level row shape
`['id', 'title', 'unit_id', 'lesson_number', 'status', 'tier', 'practice_data']`,
keep `practice_data` key order
`['guided', 'method_card', 'tier_guides', 'topic_links', 'exam_context', 'problem_bank', 'worked_examples']`,
and keep every problem count.

| File | JSON | bronze | silver | gold | total | changed leaves | board names | entities left in plain text |
|---|---|---|---|---|---|---|---|---|
| representing-data-L01.aqa.fixed.json | valid | 8 → 8 | 6 → 6 | 6 → 6 | 20 → 20 | 6 | 0 | 0 |
| representing-data-L02.aqa.fixed.json | valid | 8 → 8 | 6 → 6 | 6 → 6 | 20 → 20 | 29 | 0 | 0 |
| representing-data-L03.aqa.fixed.json | valid | 8 → 8 | 6 → 6 | 6 → 6 | 20 → 20 | 35 | 0 | 0 |
| representing-data-L04.aqa.fixed.json | valid | 8 → 8 | 6 → 6 | 6 → 6 | 20 → 20 | 7 | 0 | 0 |
| representing-data-L05.aqa.fixed.json | valid | 8 → 8 | 6 → 6 | 6 → 6 | 20 → 20 | 6 | 0 | 0 |
| representing-data-L06.aqa.fixed.json | valid | 8 → 8 | 6 → 6 | 6 → 6 | 20 → 20 | 19 | 0 | 0 |

Total: 120 problems in, 120 problems out; 102 changed leaves.
The only key added or removed anywhere is the deletion of `silver[0].chart` in L04, which the brief instructs.

### Diagram check

Both edited SVGs parse as XML (`xml.etree.ElementTree.fromstring`) and were rendered in headless Chromium
(`_render.png`, via `_render.py`). Values recovered from the corrected geometry:

- **L03 gold[5]** — Group A (5, 4), (15, 10), (25, 18), (35, 16), (45, 8), (55, 4); Group B (5, 2), (15, 6), (25, 10), (35, 8), (45, 4), (55, 2). A is above B at every midpoint, the peak of 18 sits inside the new 0–20 axis, and both series labels fit inside the viewBox.
- **L05 gold[0]** — School A 145 / 155 / 162 / 170 / 185; School B 148 / 160 / 165 / 172 / 183.

No Supabase writes were made. The original `.aqa.json` files are untouched.

# numerical-measures (Statistics AQA) — port of the Edexcel review findings

Source rows: `numerical-measures-L01..L07.aqa.json`
Output rows: `numerical-measures-L01..L07.aqa.fixed.json` (indent 1, `ensure_ascii=False`)

No board name appears anywhere in the seven files. A grep for
`aqa|edexcel|pearson|ocr|wjec|eduqas|exam board|examiner` returns nothing, so every
"board named in the method card" finding is **n/a**.

---

## L01 — Mode, Median and Mean for Ungrouped Data

| Finding | Result | Evidence |
|---|---|---|
| topic_links lists Lesson 2 (a later lesson) as the only prerequisite → remove it | **APPLIED** | `topic_links.prerequisites` held one entry, `numerical-measures/2` "Averages from Frequency Tables and Grouped Data". Now `[]`. |
| Entities → unicode | **APPLIED** | 13 plain-text fields converted (`&mdash;` in guided say/done, `&ndash;` in `exam_context.marks`). |

## L02 — Averages from Frequency Tables and Grouped Data

| Finding | Result | Evidence |
|---|---|---|
| gold[1].misconceptions: last sentence names 10–20 as the modal class | **APPLIED** at AQA **gold[1]** | The table in the same item gives f = 2, 6, 7, 3, 2 (Σf = 20), so 20–30 (f = 7) is modal, not 10–20 (f = 6). Old tail: "The modal class (10–20) has the highest frequency but is not the median class here." Replaced with the brief's sentence. |
| Entities → unicode | **APPLIED** | 21 fields. |

Note: the brief's replacement sentence is used verbatim, except that its two ASCII
hyphens take the file's own typography — en dash for the class range "20–30", em dash
for the aside — so the message does not mix dash styles mid-sentence.

## L03 — Weighted Mean and Geometric Mean

| Finding | Result | Evidence |
|---|---|---|
| tier_guides.silver.example rounds √2.94 to 1.715 then answers 1.72 (HIGH) | **APPLIED** at `tier_guides.silver.example` | Recomputed: √2.94 = 1.714642…, so 3 s.f. = **1.71**. The file said "≈ 1.715" then "≈ 1.72". Step 1 → `= 1.7146`, Answer → `≈ 1.71 … factor of 1.71 per year`. (`worked_examples[1]`, the same question, already carried 1.7146 / 1.71 and was left alone.) |
| gold item: mean seasonal variation "for each quarter" from one year | **n/a** | The word "seasonal" does not occur in any numerical-measures file. Edexcel-only added item. |
| topic_links: drop numerical-measures/4, keep /2 | **APPLIED** | Prerequisites were `[numerical-measures/2, numerical-measures/4]`; /4 is the following lesson. Now `[numerical-measures/2]`. |
| Entities → unicode | **APPLIED** | 87 fields (this lesson is entity-heavy: `&times; &divide; &radic; &asymp; &rarr; &minus; &pound;`). |

## L04 — Range, Quartiles and Interquartile Range

| Finding | Result | Evidence |
|---|---|---|
| silver "position 2.75 in 5, 8, 11, …" keyed 13.25 → 10.25 (HIGH) | **n/a** | No such item. The AQA method card states the spec "ensures exam datasets have n values where n is one less than a multiple of 4 … so quartile positions are always whole numbers and no interpolation is needed". No "2.75", "10.25" or "13.25" anywhere in the file. Its misconception/guided scratch commentary is therefore also n/a. |
| gold[1]: key option says 44 is "more than double Q3" | **APPLIED** at AQA **gold[1]** | Stem: "A dataset of 7 values has Q1 = 10, Q3 = 22. A new value of 44 is added…". 2 × 22 = 44 exactly, so "more than double" is false. `options[0]` → "Yes, because it sits far above Q3 = 22 and well clear of the rest of the data". |
| Board named in the method card | **n/a** | No board name. The only board-ish sentence is "The 1.5 × IQR rule is given in the Higher formula sheet", which the brief's EXCLUDED list rules out of scope. |
| Entities → unicode | **APPLIED** | 20 fields. |

## L05 — Standard Deviation and Interpercentile Range

| Finding | Result | Evidence |
|---|---|---|
| gold item (mean 30, Σx² = 47500, n = 50) keyed 10 → σ = 7.07 (HIGH) | **n/a** | "47500" does not occur. The AQA gold Σx²-style item is gold[3]: n = 6, Σx = 60, Σx² = 700, keyed 4.08 — recomputed √(700/6 − 10²) = √16.667 = 4.0825 → 4.08, correct. |
| Its final guided step leaves "wait – check … re-verify arithmetic" | **n/a** | No scratch commentary in the file (grep for "wait" / "re-verify" returns nothing). |
| silver item (mean 20, 17200/40) keyed 6.32 → 5.48 (HIGH) | **n/a** | "17200" does not occur. The AQA silver equivalent is silver[2]: Σx² = 580, n = 6, mean 9, keyed 3.96 — recomputed √(96.667 − 81) = √15.667 = 3.9581 → 3.96, correct. |
| Method card names the board | **n/a** | No board name. |
| Method card defines IPR with the 10th–90th example, then defines IDR as the same thing | **APPLIED** at `method_card.content` | Old: "…(IPR) is the difference between two percentile values, e.g. the 90th minus the 10th percentile. The interdecile range (IDR) is the 90th minus the 10th percentile specifically." Replaced with the brief's wording; the trailing sentence about cumulative frequency graphs is kept. |
| Entities → unicode | **APPLIED** | 22 fields (`&sigma; &radic; &approx; &minus; &rsquo;`). Note `&approx;` is not a real HTML entity and was rendering literally; it is now ≈. |

For completeness the two HIGH σ values in the brief were recomputed anyway:
√(47500/50 − 30²) = √50 = 7.0711 → **7.07**, and √(17200/40 − 20²) = √30 = 5.4772 → **5.48**.
Neither dataset exists in the AQA bank.

## L06 — Scatter Diagrams, Line of Best Fit and Regression

In this lesson the brief's phrase "the chart" always describes the **inline SVG** in
`display`, not the Chart.js `chart` object: every quoted defect (0→43.6, 11 points,
"(3,8),(5,11)…", 10 points) decodes exactly from the SVG pixel coordinates, while the
chart objects are mostly tidy. Fixes were therefore applied to the SVG geometry. Every
edited SVG was re-decoded back to data units, checked for XML well-formedness and
rendered in Chrome.

| Finding | Result | Evidence |
|---|---|---|
| gold[0]: stem says x range 5 to 30 but the drawn points run x = 0 to ≈43.6 | **APPLIED** at AQA **gold[0]** | Decoded old points: x = 0, 5.6, 8.1, 12.3, 16.9, 24.0, 26.6, 32.1, 34.7, 40.9, **43.60**. Replaced with 11 points at x = 5, 7, 9, 12, 14, 17, 19, 22, 25, 28, 30 scattered about the given line y = 10 + 2.4x (y = 24, 27, 35, 37, 48, 47, 58, 60, 73, 75, 83). Same count, same rising trend. Re-decode confirms x ∈ [5.0, 30.0]. The `chart` object was already 5→30 on the line, so it was left untouched. |
| silver[0]: guided steps list x = 2,4,…,12 and y = 3,7,…,23 but the plot shows (3,8),(5,11),(7,13),(7,14),(9,15),(11,17) | **APPLIED** at AQA **silver[0]** | The SVG decodes to exactly those six points plus the red double-mean marker at (7, 13). Both `pre` fields rewritten to "(3 + 5 + 7 + 7 + 9 + 11) ÷ 6 =" and "(8 + 11 + 13 + 14 + 15 + 17) ÷ 6 =", and the misconception to match. Totals still 42 and 78, so the keyed answers 7 and 13 and the existing hints stay correct. |
| bronze[2]: text says 7 students but 11 points are plotted | **APPLIED** at AQA **bronze[2]** | The SVG held 11 data circles (plus the red mean crosshair). Redrawn with exactly 7 points — (1,3), (2,5), (4,10), (5,12), (6,15), (8,18), (9,21) — whose means are x̄ = 35/7 = **5** and ȳ = 84/7 = **12**, matching the stem and the mean marker. These are the `chart` object's own 7 points, so picture and chart now agree. |
| gold[4]: text says 6 students but 10 points are plotted | **APPLIED** at AQA **gold[4]** | 10 data circles decoded. Stem → "…test score (y) for 10 students". |
| bronze[7]: text says x = 10 to 50 but points run 0 to 60 | **APPLIED** at AQA **bronze[7]** | Decoded points run x = 0.0 … 60.0. Stem → "data from x = 0 to x = 60"; the prediction stays at x = 30 and the keyed answer (interpolation) still holds. |
| Entities → unicode | **APPLIED** | 12 fields. |

### Two consistency changes beyond the literal wording of the brief (flagged for review)

1. **bronze[7] misconception.** The stem fix would have left the feedback saying
   "x = 30 lies within the data range (10 to 50)", contradicting the corrected stem.
   Changed to "(0 to 60)".
2. **silver[0] `chart` object data.** The brief rewrites the guided walk to the drawn
   points; the `chart` object still held the old (2,3)…(12,23). Because a `chart`
   object renders as a second, side-by-side figure (`renderChartPanel` in
   `practice.html`), leaving it would have put a third set of numbers in front of the
   student. Set to the drawn points — same 6 points, same keys, same rising trend.

**Residual mismatch, not fixed:** gold[4] now says 10 students and its SVG draws 10
points, but its `chart` object still holds 6 points. Correcting that would mean adding
points, which the instruction "for L06 keep the number of points" forbids, so it is
left for a decision. (The same SVG-vs-chart-object divergence exists across this bank
generally; only the items the brief names were touched.)

## L07 — Spearman's Rank Correlation Coefficient

| Finding | Result | Evidence |
|---|---|---|
| Board name if any | **n/a** | No board name. `method_card.steps[5]` says "using the spec bands", which is board-neutral. |
| Entities → unicode | **APPLIED** | 20 fields (`&rsquo; &ndash; &sup2; &minus; &mdash;`). |

---

## Generic-rule application

Entities were converted in every string field **except**:

* any field named `content` — those hold HTML markup (`method_card.content`,
  `tier_guides.*.example.steps[].content`, `worked_examples[].steps[].content`);
* anything inside an `<svg>…</svg>` block (none of the SVGs in this unit contains an
  entity, but the guard is in place);
* the markup-critical entities `&lt; &gt; &amp; &quot; &apos; &nbsp;`.

`&lt;` is deliberately left encoded. It survives in five places — L07
`method_card.steps[5]`, the three `tier_guides.*.steps[5]`, and L07
`problem_bank.bronze[2].display` — all of which read "…weak, &lt;0.2 none". Those
fields reach the page through `innerHTML` (`practice.html` lines 5004, 5781; 
`practice-loader.js` line 284), so `&lt;` is the correct encoding and renders as "<";
converting it to a bare `<` would open a stray tag and swallow the rest of the string.

Entity names found and mapped: `mdash ndash times divide minus asymp approx radic rarr
pound sigma rsquo ldquo rdquo middot sup2 Rightarrow`. No unmapped entity remained.

---

## JSON validity and problem counts

All seven fixed files parse. Top-level keys are unchanged
(`id, title, unit_id, lesson_number, status, tier, practice_data`), and no problem was
added, removed or reordered.

| file | JSON | bronze | silver | gold | key shape vs source |
|---|---|---|---|---|---|
| numerical-measures-L01.aqa.fixed.json | valid | 8 → 8 | 6 → 6 | 5 → 5 | identical except `topic_links.prerequisites` 1 → 0 entries (the fix) |
| numerical-measures-L02.aqa.fixed.json | valid | 8 → 8 | 6 → 6 | 6 → 6 | identical |
| numerical-measures-L03.aqa.fixed.json | valid | 8 → 8 | 6 → 6 | 5 → 5 | identical except `topic_links.prerequisites` 2 → 1 entries (the fix) |
| numerical-measures-L04.aqa.fixed.json | valid | 8 → 8 | 6 → 6 | 5 → 5 | identical |
| numerical-measures-L05.aqa.fixed.json | valid | 8 → 8 | 6 → 6 | 5 → 5 | identical |
| numerical-measures-L06.aqa.fixed.json | valid | 8 → 8 | 6 → 6 | 6 → 6 | identical |
| numerical-measures-L07.aqa.fixed.json | valid | 8 → 8 | 6 → 6 | 6 → 6 | identical |

Every changed leaf was classified. Content changes are exactly the ones listed above;
all other differences (13 + 21 + 87 + 20 + 22 + 12 + 20 = 195 fields) are pure
entity-to-unicode substitutions.

## Visual check

The five edited or renamed L06 figures were parsed as XML (all well-formed) and
rendered in Chrome from `_l06_figures.html`. gold[0] now shows 11 points between
x = 5 and x = 30 on a clear positive trend; bronze[2] shows 7 points with the red
double-mean marker sitting on (5, 12); bronze[7] and gold[4] show the corrected stems
("x = 0 to x = 60", "for 10 students") over their unchanged plots.

## Scripts

`_nm_fix.py` (fixer, with an assertion per finding), `_nm_verify.py` /
`_nm_verify2.py` (validity, counts, change classification), `_nm_render.py`
(well-formedness + preview page). Supabase was not touched.

# probability-comparing-distributions — AQA port report

Source files: `probability-comparing-distributions-L01.aqa.json` … `L06.aqa.json`.
Output: `probability-comparing-distributions-L04.aqa.fixed.json` (the only lesson that changed).

Unit-wide scan first: no exam-board name (AQA / Edexcel / Pearson / OCR / WJEC / Eduqas,
any case) appears in any string of any of the six rows. Named and numeric HTML entities
appear in only these places, and all but two sit inside HTML-markup fields
(`method_card.content`, `tier_guides.*.example.steps[].content`,
`worked_examples[].steps[].content`, problem `display` values that are `<table>` markup),
so the generic entity rule does not touch them.

---

## L01 — Probability Scale, Expected Frequency and Estimating from Data
Brief: generic rules only.

- Board name in student text — **n/a**. Zero matches in the row.
- Entities → unicode — **n/a**. Only `&mdash;` in `practice_data.method_card.content`,
  which is HTML markup (`<p>…`), so it is excluded by the rule.

**No file written.**

## L02 — Relative Risk, Absolute Risk and Risk Communication
Brief: generic rules only.

- Board name — **n/a**. Zero matches.
- Entities → unicode — **n/a**. `&divide; &ldquo; &mdash; &rdquo;` in `method_card.content`;
  `&lsquo; &mdash; &rsquo;` in `tier_guides.gold.example.steps[3].content` and
  `worked_examples[2].steps[3].content`. All three are HTML markup fields.

**No file written.**

## L03 — Two-Way Tables, Tree Diagrams and Venn Diagrams
Brief: generic rules only.

- Board name — **n/a**. Zero matches.
- Entities → unicode — **n/a**. `&ldquo; &mdash; &rdquo;` in `method_card.content` only (HTML).

**No file written.**

## L04 — Comparing Data Sets in Context  → `probability-comparing-distributions-L04.aqa.fixed.json`

1. **`guided.teach.gold` compares two brands by standard deviation (Higher only) in a
   both-tier lesson — APPLIED.** Found at `practice_data.guided.teach.gold` (row `tier`
   is `both`). Evidence, before: display read "Brand A: mean 20 h, standard deviation 2.
   Brand B: mean 18 h, standard deviation 6." and step 1 was labelled `SD ratio = 6 ÷ 2 = `.
   - `display` replaced with the brief's median/IQR wording, verbatim.
   - `steps[1].pre` `SD ratio = 6 ÷ 2 = ` → `IQR ratio = 6 ÷ 2 = `; `steps[1].say`
     "Brand B's SD (6)" → "Brand B's IQR (6)"; `steps[1].hint` "larger SD by the smaller"
     → "larger IQR by the smaller". Answer 3 unchanged.
   - `steps[2].say` "its standard deviation is 3 times smaller" → "its IQR is 3 times smaller".
   - **Consequential edit beyond the brief's literal list** (flagged for review): the new
     display gives *medians*, so `steps[0]` was re-worded from means to medians —
     `pre` "Difference in means = 20 − 18 = " → "Difference in medians = 20 − 18 = ",
     `say` "Compare the means" → "Compare the medians", `hint` "smaller mean from the larger"
     → "smaller median from the larger", and `steps[2].say` "(mean 20 h vs 18 h)" →
     "(median 20 h vs 18 h)". Without this the walk would have quoted means that the fixed
     display no longer states. Answer 2 unchanged.
2. **`tier_guides.gold.example.question` carries "(This standard-deviation comparison is
   Higher tier content.)" — n/a.** The AQA question reads in full: "The table below compares
   weekly wages at two companies. Both means are identical. What does the standard deviation
   tell us, and which company offers more consistent wages?" No Higher-tier note to remove.
3. **`bronze[3]` `&pound;` in `options[0]` and the misconception — APPLIED.** AQA index
   `bronze[3]` (the salary-table "which average is most appropriate" item — same index as
   Edexcel). Before: `options[0]` "…the extreme high value (&pound;95 000) would distort the
   mean"; `misconceptions[0].message` "When there is an outlier (&pound;95 000)…". Both now
   carry `£`.
4. **Generic entity sweep — no further change.** The other `&pound;` / `&mdash;` / `&minus;` /
   `&ldquo;` / `&rdquo;` instances are all inside HTML markup: `method_card.content`,
   `tier_guides.bronze|gold.example.steps[].content`, `worked_examples[0|2].steps[].content`,
   and the two `<table class="data-table">` displays (`bronze[3].display`,
   `silver[5].display`) — the brief names only `options[0]` and the misconception for
   `bronze[3]`, which matches.
5. **Board name — n/a.** Zero matches in the row.

## L05 — Normal Distribution and Standardising Data
Brief: board named in the method card → generic wording; entities.

- **Board named in the method card — n/a.** `practice_data.method_card` contains no board
  name. The AQA text is already generic: "The formula will always be given in the question:
  \(z = \frac{x - \mu}{\sigma}\)" and "No calculations beyond these three results are expected
  on the specification."
- **Entities → unicode — n/a.** `&ldquo; &mdash; &rdquo; &rsquo;` appear only in
  `method_card.content` (HTML markup). The `method_card.steps` plain strings are already
  unicode.

**No file written.**

## L06 — Quality Control Charts, Population Estimates and Capture-Recapture
Brief: method card opening sentence names the board; entities.

- **Method card opening sentence names the board — n/a.** The AQA opening sentence is
  "<p>This lesson covers three Higher-tier applications of the Normal distribution and
  sampling.</p>" — no board name, so nothing to strip. Left unchanged (the brief's
  replacement text exists only to drop the board's name).
- **Entities → unicode — n/a.** `&ndash; &plusmn;` in `method_card.content`, `&mdash;` in
  `tier_guides.gold.example.steps[1].content` and `worked_examples[2].steps[1].content` —
  all HTML markup. The `method_card.steps` plain strings already use unicode `±` and `–`.

**No file written.**

---

## Validity and count check

Only one fixed file exists, so only one row is checked.

| File | JSON parses | Top-level keys | bronze | silver | gold | Problem keys / solutions / option counts |
|---|---|---|---|---|---|---|
| `probability-comparing-distributions-L04.aqa.fixed.json` | OK | identical, same order (`id, title, unit_id, lesson_number, status, tier, practice_data`) | 8 → 8 | 6 → 6 | 5 → 5 | unchanged for every item |

Further checks on the fixed file:

- `practice_data` key order unchanged (`guided, method_card, tier_guides, topic_links,
  exam_context, problem_bank, worked_examples`).
- `id`, `title`, `unit_id`, `lesson_number`, `status`, `tier` unchanged.
- Leaf-path set identical to the source — nothing added, removed or re-ordered.
- Exactly 10 leaf strings differ, all listed in the L04 section above.
- Board names in the fixed row: none. Entities left in plain-text (non-markup) fields: none.
- Written with `indent=1`, `ensure_ascii=False`; byte-level line endings and trailing bytes
  match the source file's style.

Scripts used: `_pcd_explore.py`, `_pcd_ent2.py`, `_pcd_l04.py`, `_pcd_fix.py`, `_pcd_verify.py`
(all in the same directory). Supabase was not touched.

## Addendum 15 Sep 2026 — double-rendered graphs

Tom's spot-check (Edexcel numerical-measures L6, bronze): a scatter item drew its inline SVG inside the question AND the practice page drew the item's leftover `chart` object in the DATA panel, with different points. 58 problems in each Statistics bank carried both (the Aug guided rebuild added the SVGs and kept the chart objects). Fix applied to Supabase: the `chart` object is deleted wherever `display` already contains an `<svg` (116 objects across 14 lessons, both boards). Items with a chart object and no SVG (13 AQA, 16 Edexcel) keep the panel. Backup: session scratchpad `_backup_both_banks_prechartdrop_2026-09-15.json`. Rule for the practice factory: a problem carries ONE picture — an inline SVG in `display` OR a `chart` object, never both.
