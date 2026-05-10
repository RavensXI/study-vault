# HT coverage gaps — science-ocr-b (Combined OCR 21C B)

HT spec points the lesson prose does NOT develop. These need new content commissioned before the existing tier filter will reveal them on Higher tier.

Approx. 9 flagged items across 6 paper-level reports.

---

## biology-paper-1

### HT Tagging Report — OCR 21st Century B Combined Science, Biology Paper 1

**Date:** 2026-05-10  
**HT source:** `scripts/_pilot_higher_only/ocr-combined-science-b-21c-J260_ht.md`  
**Lessons processed:** L01–L08 (8 lessons)

---

#### Wraps applied

### L07_out.html — 1 wrap

| narration-id | Spec point | Rationale |
|---|---|---|
| n11 | B3.1 item 6 — explain interaction of temperature, light intensity and CO₂ in limiting the rate, and use graphs depicting the effects | Paragraph explains that all three factors interact and that a plateau on a rate-vs-one-factor graph reveals a *different* factor has become limiting. This multi-factor interaction and graphical interpretation is the HT-specific skill; Foundation covers the existence of limiting factors but not the interaction logic. |

---

#### Lessons copied unchanged (no HT content added)

| File | Reason |
|---|---|
| L01_out.html | Already contains `<div class="higher-only">` at n22 (non-coding DNA). Pre-existing block untouched. |
| L02_out.html | Already contains `<div class="higher-only">` at n21–n22 (polydactyly). Pre-existing block untouched. |
| L03_out.html | B1.3 HT spec point present but content absent — see gap below. |
| L04_out.html | Topics B2.x — no HT spec points in any B2 topic (spec confirms zero bold items). |
| L05_out.html | Topics B2.x — no HT spec points. |
| L06_out.html | Topics B2.x — no HT spec points. |
| L08_out.html | Topics B3.2–B3.4 — no HT spec points. |

---

#### Coverage gaps

### Gap 1 — B1.3 item 3: Genetic engineering steps (L03)

**Spec point:** "describe the main steps in the process of genetic engineering including: isolating and replicating the required gene(s); putting the gene(s) into a vector (e.g. a plasmid); using the vector to insert the gene(s) into cells; selecting modified cells."

**Status:** L03 covers GM crops, gene therapy and PGD but does **not** include the mechanistic steps of genetic engineering (isolating a gene, using a plasmid vector, inserting into host cells, selecting transformed cells). There is no paragraph in L03 that could be wrapped for this HT point.

**Action needed:** Add a new paragraph (or collapsible section) to L03 covering the four genetic engineering steps. Mark it `<div class="higher-only">`. This content is absent from the lesson entirely, not merely untagged.

---

### Gap 2 — B3.1 item 5: Inverse square law (L07)

**Spec point:** "use the inverse square law to explain why the rate of photosynthesis changes with distance from a light source."

**Status:** L07 n12 mentions that moving a plant further from a light source decreases the light it receives, but does not state or apply the inverse square law (intensity ∝ 1/d²). No paragraph can be wrapped for this HT point.

**Action needed:** Add a sentence or short paragraph to L07 (inside or near the collapsible "How Each Factor Limits the Rate") explaining the inverse square law and its application to photosynthesis experiments. Mark it `<div class="higher-only">`.

---

### Gap 3 — B3.1 item 6: Multi-factor graph interaction — key-fact block (L07)

**Spec point covered by n11 wrap above.** However, the key-fact block at `data-narration-id="n15"` (on the div, not a `<p>`) also articulates the interaction concept ("The three limiting factors interact. A graph plateau means a different factor is now limiting."). This block is not a `<p data-narration-id>` element and therefore was not wrapped per task rules. If the narration player reads the div-level narration-id, this content will still be spoken to Foundation students. Consider whether the key-fact div should also receive a `higher-only` wrapper in a future pass.

---

#### Summary

| Metric | Count |
|---|---|
| Lessons processed | 8 |
| Wraps added | 1 (L07 n11) |
| Pre-existing higher-only blocks left untouched | 2 (L01 n22, L02 n21–n22) |
| Coverage gaps requiring new content | 2 (L03 genetic engineering steps, L07 inverse square law) |
| Coverage gaps requiring div-level tagging decision | 1 (L07 key-fact n15) |

## biology-paper-2

### HT Tagging Report — OCR 21st Century B Combined Science Biology Paper 2

**Date:** 2026-05-10
**Source spec:** `scripts/_pilot_higher_only/ocr-combined-science-b-21c-J260_ht.md`
**Input lessons:** L01–L08 (`*_in.html`) → Output: `*_out.html`

---

#### Bio Paper 2 HT spec points identified

From the extract, Biology HT points covering Paper 2 content are:

| Chapter | Spec ref | Description |
|---------|----------|-------------|
| B5.6 | point 2 | Explain how glucagon and insulin work **together** to control blood sugar (negative feedback) |
| B5.5 | point 2 | Explain interactions of FSH, LH, oestrogen and progesterone in the menstrual cycle |
| B5.5 | point 4 | Explain use of hormones in modern reproductive technologies to treat infertility |

**B3.1 HT points** (inverse square law for photosynthesis; limiting factors with graphs) do not appear in any of the 8 lessons — photosynthesis is not covered in this unit's lesson set (Bio Paper 2 as laid out here covers B5.x topics).

**B5.3 HT point 2** (roles of thyroxine and adrenaline + negative feedback) — L05 mentions these glands in a listing paragraph (n14) but does not explain their mechanisms or negative feedback in detail. No HT wrapping applied: the prose does not go beyond Foundation-level naming.

---

#### Changes made per lesson

### L01 — Respiration
**No HT content.** Copied unchanged.

### L02 — Cell Structure and Microscopy
**No HT content.** Copied unchanged.

### L03 — Mitosis, Differentiation, Stem Cells
**No HT content.** Copied unchanged.

### L04 — Exchange Surfaces and Transport
**No HT content.** Copied unchanged.

### L05 — Nervous System and Endocrine System
**No HT content wrapped.** L05 n14 names the thyroid gland and adrenal glands but does not explain thyroxine/adrenaline roles or negative feedback mechanisms (those are absent from the lesson prose). Copied unchanged.

### L06 — Homeostasis
**1 paragraph wrapped.** Spec ref: B5.6 point 2.

- `n7` wrapped: glucagon mechanism + "insulin and glucagon work in opposite directions — this opposing action is how negative feedback achieves precise control."
- `n6` (insulin) left unwrapped: Foundation spec covers insulin's basic role in lowering blood glucose.

```html
<div class="higher-only">
<p data-narration-id="n7">When blood glucose falls, the pancreas secretes glucagon...</p>
</div>
```

### L07 — Menstrual Cycle, Fertility Treatment, Kidney Failure
**3 paragraphs wrapped across 2 locations.** Spec refs: B5.5 points 2 and 4.

**Location 1** — immediately after n2 (intro sentence), before key-fact n4:
- `n3` wrapped: full 4-hormone interaction sequence (FSH→oestrogen→LH surge→ovulation→corpus luteum→progesterone→menstruation). This is the complete B5.5 point 2 mechanism.

**Location 2** — inside the "Fertility Treatment and IVF" collapsible:
- `n7` and `n8` wrapped together (single `<div class="higher-only">` block): FSH injections for ovulation induction + full IVF description. This is B5.5 point 4.

### L08 — Evolution, Classification, Biodiversity
**No HT content.** Copied unchanged.

---

#### Structural decisions

- `<div class="higher-only">` placed **outside** the `<p data-narration-id>` elements, wrapping whole paragraphs. Attributes on `<p>` tags preserved verbatim.
- Where two consecutive HT paragraphs appear (n7+n8 in L07), they share one wrapper div rather than two separate wrappers, to avoid doubled CSS boundaries.
- The `<div class="higher-only">` inside the collapsible (L07 fertility section) is placed inside `<div class="collapsible-inner">` so the entire collapsible remains visible but its content is hidden at Foundation tier. This is intentional: Foundation students still see the collapsible header ("Fertility Treatment and IVF") but the inner content is suppressed.
- Key-fact boxes, headings, and non-HT collapsibles are untouched in all lessons.

---

#### Summary

| Lesson | HT wraps | Paragraphs wrapped |
|--------|----------|--------------------|
| L01 | 0 | — |
| L02 | 0 | — |
| L03 | 0 | — |
| L04 | 0 | — |
| L05 | 0 | — |
| L06 | 1 | n7 |
| L07 | 2 | n3; n7+n8 |
| L08 | 0 | — |
| **Total** | **3** | **4 paragraphs** |

## chemistry-paper-1

### OCR 21st Century B Combined Science J260 — Chem P1 HT-only tagging report

HT source: `scripts/_pilot_higher_only/ocr-combined-science-b-21c-J260_ht.md`
Scope: Chemistry chapters C1–C6 (Chemistry Paper 1)

---

#### L01: The Atmosphere
- Wrapped: 0 new blocks
- Notes: No HT material present. HT for C1.1 is "explain the limitations of the particle model in relation to changes of state when particles are represented by inelastic spheres". This lesson covers atmospheric composition and how it changed over time — particle model content is absent.

#### L02: Energy and Chemical Reactions
- Wrapped: 0 new blocks (1 pre-existing block preserved)
- Notes: Pre-existing `higher-only` block correctly wraps the "Bond Energies (Higher)" section: h2 n17, paragraph n18, and the "How to Calculate Energy Changes Using Bond Energies" collapsible (n19–n21). This covers spec C1.2 point 5 ("calculate energy changes in a chemical reaction by considering bond breaking and bond making energies"). Copied unchanged.

#### L03: Climate Change and the Greenhouse Effect
- Wrapped: 0 new blocks
- Notes: No HT material present. C1.1 and C1.2 HT content does not appear in this lesson.

#### L04: Water Treatment and Potable Water
- Wrapped: 0 new blocks
- Notes: No HT material present. No HT spec points in C1.3 or C1.4 (topics with zero HT items per source file).

#### L05: Atomic Structure
- Wrapped: 0 new blocks
- Notes: No HT material present. C2.x topics carry no bold-marked HT items in the OCR 21C B spec.

#### L06: The Periodic Table
- Wrapped: 0 new blocks
- Notes: No HT material present. Group 1, Group 7, Group 0 trends and electronic configuration are all Foundation + Higher content. C3.2 HT (bioleaching/phytoextraction) is not taught in this lesson.

#### L07: Chemical Bonding
- Wrapped: 0 new blocks
- Notes: No HT material present. Ionic, covalent, and metallic bonding — and the structure/properties relationships — are Foundation-accessible at this level of detail.

#### L08: Chemical Equations
- Wrapped: 1 new block
- Notes:
  - "Half-Equations for Electrolysis" collapsible (paragraph n23): wrapped in `higher-only`. Covers spec C3.3 point 4 ("use the names and symbols of common elements and compounds and the principle of conservation of mass to write half equations"). The collapsible teaches writing and balancing half-equations at each electrode — explicitly HT-only in OCR 21C B.
  - Closing paragraph n24 (general equation-writing summary) left untagged — it covers balanced equations and state symbols, which are Foundation + Higher content.

---

#### Summary

| Lesson | HT blocks added | Pre-existing | Output |
|--------|----------------|--------------|--------|
| L01 | 0 | 0 | Copied unchanged |
| L02 | 0 | 1 (bond energies) | Copied unchanged |
| L03 | 0 | 0 | Copied unchanged |
| L04 | 0 | 0 | Copied unchanged |
| L05 | 0 | 0 | Copied unchanged |
| L06 | 0 | 0 | Copied unchanged |
| L07 | 0 | 0 | Copied unchanged |
| L08 | 1 | 0 | Modified |

**Lessons modified: 1 of 8 (L08)**
**Lessons with pre-existing correct tags: 1 of 8 (L02)**
**Lessons copied unchanged: 6 of 8 (L01, L03, L04, L05, L06, L07)**
**Total new `higher-only` wraps added: 1**

---

#### HT spec points covered

| Spec ref | Content | Lesson | Status |
|----------|---------|--------|--------|
| C1.2 pt 5 | Bond energy calculations | L02 | Pre-existing |
| C3.3 pt 4 | Write half-equations | L08 | New wrap |

#### HT spec points not found in any lesson

| Spec ref | Content | Reason |
|----------|---------|--------|
| C1.1 pt 2 | Limitations of particle model (inelastic spheres) | No lesson in the 8 develops states of matter / particle model in depth |
| C3.2 pt 6 | Evaluate bioleaching / phytoextraction | Not taught in these 8 lessons |
| C3.3 pt 5 | Redox in terms of electron gain/loss (C3.3) | No lesson covers OIL RIG / electron-transfer redox explicitly |
| C4.4 pt 2 | Redox in terms of electron gain/loss (C4.4) | Not taught in these 8 lessons |
| C5.2 pts 4–7, 9 | Avogadro constant, moles, stoichiometry, mass calcs | Not taught in these 8 lessons |
| C5.3 pts 1–2 | Concentration in g/dm³ and mol/dm³ | Not taught in these 8 lessons |
| C6.1 pts 5–7 | Dilute/concentrated vs weak/strong acids; pH and H⁺ | Not taught in these 8 lessons |
| C6.3 pt 3 | Equilibrium position predictions | Not taught in these 8 lessons |

## chemistry-paper-2

### HT Tagging Report — OCR 21st Century B Combined Science Chemistry Paper 2

**Date:** 2026-05-10  
**Source spec:** `scripts/_pilot_higher_only/ocr-combined-science-b-21c-J260_ht.md`  
**Lessons processed:** L01–L08

---

#### Summary

| File | Changes | Spec point(s) |
|------|---------|---------------|
| L01_out.html | None — copied unchanged | No Chem P2 HT content |
| L02_out.html | 1 `higher-only` block added | C3.2 item 6 |
| L03_out.html | 2 `higher-only` blocks added | C3.3 items 4 and 5 |
| L04_out.html | None — copied unchanged | No Chem P2 HT content |
| L05_out.html | None — copied unchanged | No Chem P2 HT content |
| L06_out.html | None — copied unchanged | No Chem P2 HT content |
| L07_out.html | None — copied unchanged | No Chem P2 HT content |
| L08_out.html | None — copied unchanged | No Chem P2 HT content |

---

#### Detailed changes

### L02_out.html — Reactivity series and metal extraction
**Spec point: C3.2 item 6** — "evaluate alternative biological methods of metal extraction (bacterial and phytoextraction)"

- Wrapped `<p data-narration-id="n18">` inside the collapsible "Biological Methods of Metal Extraction (Higher)" with `<div class="higher-only">`.
- The collapsible container and its toggle remain unwrapped (the heading is informational for all tiers; the body is HT).

### L03_out.html — Electrolysis
**Spec points: C3.3 item 4** (half equations) and **C3.3 item 5** (oxidation/reduction in terms of electron gain/loss)

**Block 1** — wrapped n6, n7, n8, n9:
- `n6`: OIL/RIG definition — cathode = cations gain electrons (reduction); anode = anions lose electrons (oxidation). This is the HT electron-transfer definition of redox (C3.3 item 5).
- `n7`: Introduction to half equations (C3.3 item 4).
- `n8`: Cathode half equation for NaCl electrolysis.
- `n9`: Anode half equation for NaCl electrolysis.
- `n10` (conclusion paragraph) left unwrapped — it summarises the products of molten NaCl electrolysis and the binary compound rule, which is Foundation-level product prediction.

**Block 2** — wrapped n15 inside the "Worked Example: Predicting Electrolysis Products" collapsible:
- n15 contains the step-by-step worked example including "Half equation at cathode" and "Half equation at anode" — entirely HT (C3.3 item 4).
- Steps 1–3 (identifying ions, predicting products from reactivity) also sit within n15 and are part of the HT worked example; the whole paragraph is wrapped as a single unit per the wrapping convention.

---

#### Chem P2 HT spec points not found in lessons L01–L08

The following HT topics from Chem P2 (C4.4, C5.2, C5.3, C6.1, C6.3) had no corresponding content in the eight lessons reviewed. They are either covered in other units or not yet present:

- **C4.4 item 2**: redox in terms of electron gain/loss (in a materials/recycling context)
- **C5.2 items 4–7, 9**: Avogadro constant, mole calculations, stoichiometry, limiting reagent, standard form
- **C5.3 items 1–2**: concentration calculations (g/dm³ and mol/dm³)
- **C6.1 items 5–7**: dilute/concentrated/weak/strong acids; pH and hydrogen ion concentration
- **C6.3 item 3**: equilibrium position and effect of changing conditions

---

#### Methodology notes

- Only `<p data-narration-id="...">` elements were wrapped (whole paragraphs, never partial sentences).
- No prose was altered; all attributes preserved.
- No existing `higher-only` blocks were present in the input files — none were touched.
- Wraps were placed inside collapsible `<div class="collapsible-content">` containers where applicable, leaving the collapsible toggle buttons and headings visible to all tiers.
- Conservative approach: where a paragraph mixed Foundation and HT content (e.g. n10 in L03), it was left unwrapped.

## physics-paper-1

### HT Tagging Report — OCR 21st Century B Combined Science Physics Paper 1

**Date:** 2026-05-10  
**Source spec:** `scripts/_pilot_higher_only/ocr-combined-science-b-21c-J260_ht.md`  
**Input files:** `L01_in.html` – `L08_in.html`  
**Output files:** `L01_out.html` – `L08_out.html`

---

#### HT Spec Points in Physics Paper 1

| Chapter | Spec point | Covered in |
|---------|-----------|-----------|
| P1.1 | Radio waves produced by / induce oscillations in electrical circuits | Not present in any lesson prose |
| P1.2 | Temperature of a body related to the balance between incoming, absorbed and emitted radiation; factors determining Earth's temperature | L02 |
| P1.3 | Waves travel at different speeds in different substances, speeds may vary with wavelength | L03 |
| P1.3 | Refraction explained by differences in wave speed in different substances | L03 |
| P3.5 | Interaction forces between magnet and current-carrying conductor | L08 |
| P3.5 | Fleming's left-hand rule | L08 |
| P3.5 | F = BIl equation | L08 |
| P3.5 | Force causes rotation in the coil of a DC motor | L08 |
| P4.3 | Vector diagrams, momentum, Newton's 2nd law (Δp = Ft), circular orbit, inertial mass | No P4 lessons in this set |
| P5.1 | Calculate net decline as ratio after integral number of half-lives | Not present in L01 prose (half-life mentioned qualitatively only) |

---

#### Per-Lesson Decisions

### L01 — Radiation All Around Us
- **HT spec:** P5.1 (calculate ratio after N half-lives).
- **Decision:** No HT content present. Half-life is mentioned qualitatively (technetium-99m, ~6 hours) but no ratio calculation appears in the prose.
- **Action:** Copied unchanged.

### L02 — Earth's Radiation Balance / Climate Change
- **HT spec:** P1.2 — explain how temperature of a body relates to the balance between incoming, absorbed and emitted radiation; illustrate with everyday examples including factors determining Earth's temperature.
- **Tagged:** n4 (energy balance definition), n5 (albedo — factors affecting Earth's temperature), n8 (greenhouse gas absorption and re-emission → warmer surface), n9 (disrupted energy balance → new equilibrium at higher temperature).
- **Not tagged:** n13, n14 (EM spectrum/climate description), n15, n16 (models and evidence collapsible), n18, n19 (consequences) — these extend rather than constitute the core P1.2 HT explanation.
- **`<div class="higher-only">` blocks added:** 4

### L03 — Waves
- **HT spec:** P1.3 items 9+10 — waves travel at different speeds in different substances; refraction explained by speed differences. Also P1.1 item 10 (radio waves/oscillations).
- **P1.1 note:** The specific detail that radio waves can be produced by or induce oscillations in electrical circuits does not appear anywhere in L03's prose. No tag added.
- **P1.3:** n18 covers all three wave behaviours (reflection, refraction, diffraction) in a single `<p>`. The refraction bullet explicitly states a wave changes speed when passing between media and explains direction change — this matches both items 9 and 10. Because reflection and diffraction are Foundation-level content in the same paragraph, the whole `<p data-narration-id="n18">` was wrapped rather than attempting to split a single paragraph element. **Conservative decision: wrap the whole paragraph** since it is the only way to tag the HT refraction explanation without altering prose structure.
- **`<div class="higher-only">` blocks added:** 1

### L04 — Energy Sources and Demand
- **HT spec:** None in P1 scope.
- **Action:** Copied unchanged.

### L05 — Generators and the National Grid
- **HT spec:** None in P1 scope.
- **Action:** Copied unchanged.

### L06 — Electric Circuits
- **HT spec:** None in P1 scope.
- **Action:** Copied unchanged.

### L07 — Electrical Power, AC/DC and Efficiency
- **HT spec:** None in P1 scope.
- **Action:** Copied unchanged.

### L08 — Magnets and the Motor Effect
- **HT spec:** P3.5 items 1–4 (all four are HT-only).
  - Item 1: interaction forces between magnet and current-carrying conductor.
  - Item 2: Fleming's left-hand rule represents relative orientations of force, conductor and field.
  - Item 3: F = BIl equation and calculation.
  - Item 4: force causes rotation in a rectangular coil (simple DC motor).
- **Tagged paragraphs:**
  - Motor Effect section: n12 (motor effect definition), n13 (intro to factors), n14 (bullet list of factors), n15 (intro to equation), n16 (F = BIl display equation), n17 (variable definitions).
  - Fleming's section: n20 (Fleming's rule intro), n21 (thumb/first/second finger mnemonic), n22 (reversal explanation).
  - Electric Motors collapsible: n23 (coil between magnets, opposite forces), n24 (split-ring commutator, continuous rotation).
- **Not tagged:** n25–n27 (real-world applications: loudspeakers and MRI) — these are contextual applications; the spec note says "detailed knowledge of motor construction not required" and loudspeaker/MRI are Foundation-accessible examples.
- **`<div class="higher-only">` blocks added:** 11 (6 in motor-effect section + 3 in Fleming's section + 2 inside the collapsible)

---

#### Summary

| Lesson | HT blocks added | Action |
|--------|----------------|--------|
| L01 | 0 | Copied unchanged |
| L02 | 4 | HT tagged (P1.2 radiation balance) |
| L03 | 1 | HT tagged (P1.3 refraction/speed) |
| L04 | 0 | Copied unchanged |
| L05 | 0 | Copied unchanged |
| L06 | 0 | Copied unchanged |
| L07 | 0 | Copied unchanged |
| L08 | 11 | HT tagged (P3.5 motor effect + Fleming's + F=BIl + motors) |

**Total `<div class="higher-only">` blocks inserted: 16**  
No prose was altered. All `data-narration-id` and other attributes preserved. No existing `higher-only` blocks were present in any input file.

---

#### Notes and Edge Cases

- **L03 n18:** Reflection (Foundation) and refraction (HT) and diffraction (Foundation) all appear in one `<p>` element. Wrapping the whole paragraph is the only structure-preserving option. Foundation students will see this paragraph hidden — this is a known limitation of paragraph-level granularity. If sub-paragraph tagging is ever implemented (e.g. `<span class="higher-only">`), the refraction bullet only could be isolated.
- **P1.1 radio wave oscillations:** Not taught in any of the 8 lesson files. This HT point may belong to a different lesson or may need to be added to L03 in a future content pass.
- **P4.3 / P5.1 calc:** No Physics Paper 1 lessons covering P4 motion topics or half-life ratio calculations are present in this lesson set. If such lessons exist elsewhere, they will need a separate tagging pass.

## physics-paper-2

### HT Tagging Report — OCR 21st Century B Combined Science Physics Paper 2

**Date:** 2026-05-10  
**Source spec:** `scripts/_pilot_higher_only/ocr-combined-science-b-21c-J260_ht.md`  
**Lessons processed:** L01–L08

---

#### HT spec points relevant to Physics Paper 2

From the HT extract, Physics Paper 2 topics cover:

| Chapter | Spec ref | HT items |
|---------|----------|----------|
| P3.5 | How do electric motors work? | 1–4 (force on conductor, Fleming LHR, F=BIl, motor rotation) |
| P4.3 | What is the connection between forces and motion? | 3 (vector diagram resolution), 4 (momentum equation + conservation), 5 (F=Δp/t), 7 (circular orbit), 8 (inertial mass) |
| P5.1 | What is radioactivity? | 11 (net decline as ratio after n half-lives) |

---

#### Lesson decisions

| File | Topic | HT present? | Action | Paragraphs wrapped |
|------|-------|-------------|--------|--------------------|
| L01 | Forces, mass/weight, free-body diagrams, resultant forces | Marginal — n20 mentions "resolving forces is a HT skill" within a mixed F/HT sentence; cannot wrap without hiding Foundation content | Copied unchanged | — |
| L02 | Speed, velocity, acceleration, d-t graphs, v-t graphs, stopping distance | Already has `higher-only` block around n22 (area under v-t graph) | Copied unchanged (block untouched) | Pre-existing: n22 |
| L03 | Newton's Laws, momentum | Yes — P4.3 items 4+5: momentum definition, p=mv equation, conservation of momentum | **Wrapped** | n18, n19, n20 |
| L04 | Energy stores, work done, KE, GPE, efficiency | No — all content is F+H | Copied unchanged | — |
| L05 | Atomic structure, radiation types, half-life | Yes — P5.1 item 11: net decline as ratio after integral number of half-lives | **Wrapped** | n20 |
| L06 | Contamination/irradiation, medical uses, safety | No — all content is F+H | Copied unchanged | — |
| L07 | Particle model, internal energy, SHC, latent heat | No — all content is F+H | Copied unchanged | — |
| L08 | Hooke's Law, deformation, density | No — all content is F+H | Copied unchanged | — |

---

#### Detail on wraps applied

### L03 — Momentum section (P4.3 items 4 & 5)

Wrapped `<p data-narration-id="n18">`, `<p data-narration-id="n19">`, and `<p data-narration-id="n20">` together in a single `<div class="higher-only">` block immediately below the `<h2 data-narration-id="n17">Momentum</h2>` heading.

- n18: momentum definition and "product of mass × velocity" intro
- n19: the `p = m × v` equation display
- n20: explanation including conservation of momentum with worked collision example

The `<h2>` heading itself was left outside the block (headings are not `<p data-narration-id>` elements and the heading text alone is not assessable content). The collapsible that follows (n21–n24, stopping distance) is Foundation content and was left unwrapped.

P4.3 item 5 (F = Δp/t) does not appear in any lesson in this set — not tagged.

### L05 — Half-life ratio calculation (P5.1 item 11)

Wrapped `<p data-narration-id="n20">` in a single `<div class="higher-only">` block.

- n20: "After one half-life, half the original unstable nuclei remain. After two half-lives, a quarter remain. After three, an eighth..." — this is the net-decline-as-ratio calculation required by HT item 11.

n19 (half-life definition, randomness) is Foundation and left unwrapped. The half-life graph collapsible (n21–n22) and key-fact (n23) are Foundation/both-tier and left unwrapped.

---

#### HT spec points not found in any lesson

| Spec ref | Item | Note |
|----------|------|------|
| P3.5 | 1–4 (electric motors, Fleming LHR, F=BIl) | No lesson in this set covers electric motors |
| P4.3 item 3 | Vector diagram resolution | Mentioned in L01 n20 prose but not as a standalone teachable paragraph — cannot be cleanly wrapped |
| P4.3 item 5 | F = Δp/t (change in momentum = force × time) | Not present in any lesson |
| P4.3 item 7 | Circular orbit — constant speed, changing velocity | Touched briefly in L02 n5 within a Foundation paragraph; cannot be cleanly separated |
| P4.3 item 8 | Inertial mass | Not present in any lesson |

These gaps should be flagged if the lessons are ever regenerated or extended.

---

#### Files produced

```
physics-paper-2/
  L01_out.html  — unchanged copy
  L02_out.html  — unchanged copy (pre-existing higher-only block preserved)
  L03_out.html  — n18/n19/n20 wrapped in higher-only
  L04_out.html  — unchanged copy
  L05_out.html  — n20 wrapped in higher-only
  L06_out.html  — unchanged copy
  L07_out.html  — unchanged copy
  L08_out.html  — unchanged copy
```
