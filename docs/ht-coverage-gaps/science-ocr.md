# HT coverage gaps — science-ocr (Combined OCR Gateway A)

HT spec points the lesson prose does NOT develop. These need new content commissioned before the existing tier filter will reveal them on Higher tier.

Approx. 0 flagged items across 6 paper-level reports.

---

## biology-paper-1

### HT Tagging Report — OCR Gateway A Combined Science Biology Paper 1

Date: 2026-05-10  
Source: `ocr-combined-science-a-gateway-J250_ht.md`  
Lessons processed: L01–L08 (8 lessons, B1–B3 topics)

---

#### HT spec points in scope (Biology Paper 1: B1–B3)

| Spec point | Description | Status |
|------------|-------------|--------|
| B1.1c | Electron microscopy increasing understanding of sub-cellular structures | Tagged in L01 |
| B1.4f | Interaction of temperature, light intensity and CO2 concentration using graphs | Pre-tagged in L04 |
| B3.2b | Roles of thyroxine and adrenaline; negative feedback | Pre-tagged in L07 |
| B3.2d | Interactions of FSH, LH, oestrogen and progesterone in menstrual cycle | Tagged in L07 |
| B3.2e | Hormonal and non-hormonal contraception (use and evaluation) | Tagged in L07 |
| B3.2f | Hormones in fertility treatments (IVF, ovulation induction) | Pre-tagged in L07 |
| B3.3c | Glucagon interacting with insulin to control blood sugar | Pre-tagged in L08 |

Mathematical HT points (BM1.1iii standard form; BM1.4v inverse square law) — not tagged. The magnification formula (n25, L01) is Foundation-level; the inverse square law is introduced in context but not as a standalone mathematical skill. No prose isolated to these mathematical requirements was found that was separable from Foundation content.

---

#### Wraps applied per file

### L01_out.html — 1 new higher-only block
**B1.1c** — electron microscopy increasing understanding of sub-cellular structures  
Wrapped: `n23` + `n24` (two consecutive `<p>` elements)  
Boundary: opens after the PAG B1 collapsible; closes before key-fact n25 (magnification formula, which is Foundation).

Rationale: n23 names the TEM and explicitly notes it "greatly increasing our understanding of how cells work (B1.1c)". n24 develops the explanation of what electron microscopy revealed (cristae, surface area). Both directly map to B1.1c. The key-fact n25 covers the magnification formula — required at all tiers — so is left outside the block.

### L02_out.html — unchanged (no HT content)
Topics: DNA structure, protein synthesis, enzyme activity. No HT spec points in B1.2 for this unit.

### L03_out.html — unchanged (no HT content)
Topics: aerobic/anaerobic respiration, biological molecules, exercise. No HT spec points in B1.3.

### L04_out.html — pre-existing higher-only block preserved
**B1.4f** — factor interaction on graphs already wrapped (n16 + key-fact n17). No new wraps needed.

### L05_out.html — unchanged (no HT content)
Topics: diffusion/osmosis/active transport, cell cycle, SA:V ratio, circulatory system, xylem/phloem. No HT spec points in B2.1 or B2.2.

### L06_out.html — unchanged (no HT content)
Topics: nervous system structure, neurones, synapses, reflex arcs. No HT spec points in B3.1.

### L07_out.html — 2 new higher-only blocks (plus 2 pre-existing preserved)
**B3.2d** — FSH/LH/oestrogen/progesterone interaction in menstrual cycle  
Wrapped: `n10` (single `<p>` element — the four-hormone detailed interaction)  
Boundary: n8 (intro to menstrual cycle, mentions testosterone — Foundation) and n9 (stem sentence "The four hormones are:") are left outside; the key-fact n11 is Foundation-level recall (names + basic roles) and left outside.

**B3.2e** — hormonal and non-hormonal contraception evaluation  
Wrapped: the entire "Contraception: Hormonal and Non-hormonal Methods" collapsible (n12, n13, n14)  
Boundary: block opens before the collapsible button; closes after n14.

Pre-existing blocks preserved as-is:  
- Thyroxine/Adrenaline collapsible (n5, n6) — B3.2b  
- Fertility Treatments collapsible (n15, n16) — B3.2f

### L08_out.html — pre-existing higher-only block preserved
**B3.3c** — glucagon/insulin interaction already wrapped (n7). No new wraps needed.

---

#### Coverage gaps (HT points not found in lesson prose)

| Spec point | Issue |
|------------|-------|
| BM1.1iii | Standard form calculations — no prose in L01 specifically requiring standard form. The magnification numbers appear but the *skill* of calculating in standard form is not taught as a standalone block. Gap exists; would require new content, not just tagging. |
| BM1.4v | Inverse square law as a mathematical skill — L04 n13 introduces the law conceptually (with the formula) but does not drill the calculation. The skill is present as context but not as an isolated HT block that could be wrapped without also wrapping Foundation content. Conservative call: not tagged. Gap noted. |
| B3.2d (partial) | The key-fact n11 in L07 names FSH/LH/oestrogen/progesterone and their basic roles. This is borderline — OCR specifies that *explaining the interactions* is HT. The key-fact summarises interactions briefly and is arguably reinforcement for both tiers. Left untagged to avoid hiding a useful summary from Foundation students. |

---

#### Decisions log

- **Conservative on collapsible wrapping**: when an entire collapsible panel is HT, the `<div class="higher-only">` wraps the whole `<div class="collapsible">` block (not just the inner `<p>` elements). This hides the toggle button too, which is the correct behaviour.
- **n9 in L07 not wrapped**: "The four hormones controlling the menstrual cycle are:" is a stem sentence that creates context. Wrapping it would orphan a dangling sentence visible to Foundation students. Left outside; the detailed interaction (n10) is wrapped.
- **Key-fact n11 in L07 not wrapped**: A brief one-line summary ("FSH matures egg… LH triggers ovulation…") is useful revision reinforcement at Foundation level and does not teach the HT interaction in depth. Left outside.
- **Magnification key-fact n25 in L01 not wrapped**: The magnification formula is explicitly assessed at Foundation. The key-fact covers it alongside a mention of electron microscope resolution — leaving it outside the higher-only block is correct.
- **Pre-tagged blocks in L04, L07, L08**: preserved exactly; no edits applied inside existing higher-only divs.

## biology-paper-2

### HT Tagging Report — OCR Gateway A Combined Science Bio Paper 2

**Date:** 2026-05-10  
**HT source:** `scripts/_pilot_higher_only/ocr-combined-science-a-gateway-J250_ht.md`  
**Lessons processed:** L01–L08

---

#### Spec mapping

Bio Paper 2 covers topics B4–B6 in OCR Gateway A (J250).

| Topic | HT-only spec points (from extract) |
|-------|-------------------------------------|
| B4: Community level systems | None |
| B5: Genes, inheritance and selection | None |
| B6.2: Feeding the human race | **B6.2c** — describe the main steps in genetic engineering (restriction enzymes, sticky ends, ligase, host bacteria, antibiotic resistance markers, vectors/plasmids) |
| B6.1, B6.3 | None |

---

#### Lesson-by-lesson findings

| File | Topic | HT content present? | Action |
|------|-------|---------------------|--------|
| L01 | B4.1 — Ecosystems, interdependence, biodiversity | No | Copied unchanged |
| L02 | B4.1 — Carbon, water and nitrogen cycles; decomposition | No | Copied unchanged |
| L03 | B5.1 — Genes, chromosomes, alleles, inheritance, Punnett squares | No | Copied unchanged |
| L04 | B5.2 — Variation, natural selection, evolution, antibiotic resistance, selective breeding | No | Copied unchanged |
| L05 | B6.1 — Monitoring ecosystems; human interactions; pollution indicators; conservation | No | Copied unchanged |
| L06 | B6.2 — Food security, farming techniques, GM crops, sustainable farming | **See note below** | Copied unchanged |
| L07 | B6.3 — Health and disease; body defences; immune response; vaccination | No | Copied unchanged |
| L08 | B6.3 — Non-communicable diseases; CVD; cancer; correlation vs causation | No | Copied unchanged |

### L06 — B6.2c note

The HT spec point B6.2c requires students to "describe the main steps in the process of genetic engineering — restriction enzymes, sticky ends, ligase, host bacteria and selection using antibiotic resistance markers, vectors e.g. plasmids."

L06 (n12–n13) does discuss genetic modification at a conceptual level (pest-resistant crops, golden rice, concerns about cross-pollination) — this corresponds to **B6.2d** (Foundation-level understanding of GM crops). The mechanistic detail that is HT-only (restriction enzymes, sticky ends, ligase, host bacteria, antibiotic resistance selection markers, plasmid vectors) is **not present** in the lesson. There is nothing to wrap.

If the lesson is later extended to include the step-by-step genetic engineering mechanism, those paragraphs should be wrapped as:

```html
<div class="higher-only">
  <p data-narration-id="nXX">...</p>
  <!-- all paragraphs covering restriction enzymes, sticky ends, ligase,
       host bacteria, antibiotic resistance markers and vectors -->
</div>
```

---

#### Output files

All 8 output files are verbatim copies of their inputs. No `<div class="higher-only">` wrappers were added.

```
L01_out.html  — unchanged copy
L02_out.html  — unchanged copy
L03_out.html  — unchanged copy
L04_out.html  — unchanged copy
L05_out.html  — unchanged copy
L06_out.html  — unchanged copy  (B6.2c HT mechanism absent from lesson)
L07_out.html  — unchanged copy
L08_out.html  — unchanged copy
```

## chemistry-paper-1

### HT Tagging Report — OCR Gateway A Combined Science Chemistry Paper 1

Date: 2026-05-10
Source spec: `scripts/_pilot_higher_only/ocr-combined-science-a-gateway-J250_ht.md`
Lessons: L01–L08 (Topics C1–C3, plus C2 bonding/structure)

---

#### Lessons copied unchanged (no new HT blocks added)

| File | Reason |
|------|--------|
| L01_out.html | Already has `<div class="higher-only">` around n15–n16 (Limitations of the particle model / C1.1c). No new additions needed. |
| L02_out.html | Topic C2 (atomic structure). No HT-only spec points in C2 per the extract. |
| L03_out.html | Topic C2 (pure substances, mixtures, separation). No HT-only spec points in C2. |
| L04_out.html | Topic C2 (bonding). No HT-only spec points in C2. |
| L05_out.html | Topic C2 (structure and properties). No HT-only spec points in C2. |
| L06_out.html | Already has `<div class="higher-only">` around n19 (reacting masses / moles calculation, C3.1h/i/n). No new additions needed. |
| L07_out.html | Already has `<div class="higher-only">` around n11–n17 (bond energy calculations). No new additions needed. |

---

#### Lessons with new HT blocks added

### L08_out.html — Oxidation/Reduction, Acids, Electrolysis

**1 new block added.**

**n21 (key-fact)** — Half equations at electrodes

- Spec reference: C3.1b (partial) — "write formulae and balanced chemical equations **and half equations**"
- The key fact shows `Na⁺ + e⁻ → Na` and `2Cl⁻ → Cl₂ + 2e⁻` with the label "Half equations show what happens at each electrode separately."
- Wrapped the entire `<div class="key-fact" data-narration-id="n21">` in `<div class="higher-only">`.

---

#### Conservative calls (not wrapped)

**L08 n3** — Redox in terms of electrons (C3.3b)

The paragraph begins with a Foundation-level copper oxide / oxygen-based redox example, then adds: "At Higher Tier, you also need to explain redox in terms of electrons…" Both tiers' content is interleaved in a single `<p>` element. Wrapping the whole paragraph would hide a Foundation example from Foundation students. Left unchanged. The inline "(Higher)" signal in the prose is sufficient for students reading the full lesson; the CSS hide only applies when Foundation tier is active via body class.

**L08 n4** — Key fact with electron definitions

Contains both oxygen-based (Foundation) and electron-based (Higher) definitions in one paragraph with an inline "(Higher)" label. Same reasoning as above — mixed content within a single element; wrapping would hide Foundation content. Left unchanged.

**L06 n24** — Reaction types collapsible

Mentions "Oxidation: gaining oxygen (or losing electrons)" and "Reduction: losing oxygen (or gaining electrons)" in a list covering multiple reaction types. The electron phrasing is a brief embedded gloss, not the full C3.3b Higher skill (which requires identifying which species is oxidised/reduced and writing electron half equations). Foundation students need the oxygen-based oxidation/reduction definition, which is in the same sentence. Left unchanged.

---

#### Summary

| Lesson | Action | HT blocks (total in output) |
|--------|--------|----------------------------|
| L01 | Copied unchanged | 1 (pre-existing: Limitations of particle model) |
| L02 | Copied unchanged | 0 |
| L03 | Copied unchanged | 0 |
| L04 | Copied unchanged | 0 |
| L05 | Copied unchanged | 0 |
| L06 | Copied unchanged | 1 (pre-existing: reacting masses) |
| L07 | Copied unchanged | 1 (pre-existing: bond energy calculations) |
| L08 | 1 new block added | 2 (pre-existing: strong/weak acids; new: half equations key fact) |

**Total new `<div class="higher-only">` blocks added: 1**
**Total pre-existing blocks preserved: 4**

## chemistry-paper-2

### HT Tagging Report — OCR Gateway A Combined Science Chemistry Paper 2

**Date:** 2026-05-10
**Lessons processed:** L01–L08 (8 files)

---

#### HT spec points in Chem P2 scope (C4–C6)

From `ocr-combined-science-a-gateway-J250_ht.md`:

| Spec ref | Description | HT |
|----------|-------------|-----|
| C4.1 | Predicting and identifying reactions and products | No HT points |
| C5.2c | Le Chatelier's principle (concentration, temperature, pressure) | **HT** |
| C6.1c | Biological metal extraction (phytoextraction, bioleaching) | **HT** |

All other Chem P2 content (C4.1, C5.1, C6.2 etc.) is Foundation + Higher.

---

#### Lesson-by-lesson results

| File | Topic coverage | HT content found | Action |
|------|---------------|-----------------|--------|
| L01 | Reactivity series, displacement, metal extraction | C6.1c: phytoextraction + bioleaching collapsible | **Already wrapped** — `<div class="higher-only">` present at lines 29–39 |
| L02 | Periodic table, Group 1/7/0 trends | None | Copied unchanged |
| L03 | Flame tests, gas tests, ion tests, instrumental analysis | None | Copied unchanged |
| L04 | Rate of reaction, collision theory, catalysts | None | Copied unchanged |
| L05 | Reversible reactions, dynamic equilibrium, Le Chatelier, Haber | C5.2c: Le Chatelier principle + Haber process analysis | **Already wrapped** — `<div class="higher-only">` present from line 23 to end of file |
| L06 | Atom economy, % yield, LCA, crude oil, cracking | None | Copied unchanged |
| L07 | Atmosphere evolution, greenhouse effect, climate change | None | Copied unchanged |
| L08 | Resources, potable water, waste water, pollutants | None | Copied unchanged |

---

#### Key decisions

**Le Chatelier + Haber (L05):** The entire `higher-only` block in the input correctly wraps both the Le Chatelier section and the Haber Process section. The Haber Process analysis is inseparable from Le Chatelier application (C5.2c), so leaving both wrapped is correct.

**No new wrapping required.** Both HT passages (C5.2c, C6.1c) were already correctly tagged in the input files. No prose was changed.

**No partial-HT cases in Chem P2:** Unlike C3.1b ("and half equations" HT suffix), there are no analogous partial-HT statements in C4–C6 content. All Foundation paragraphs are clean.

---

#### Output files

All 8 `_out.html` files written. L01 and L05 retain existing `higher-only` blocks. L02, L03, L04, L06, L07, L08 are byte-for-byte copies of their inputs.

## physics-paper-1

### HT Tagging Report — OCR Gateway A Combined Science Physics Paper 1

**Date:** 2026-05-10  
**Source spec:** `scripts/_pilot_higher_only/ocr-combined-science-a-gateway-J250_ht.md`  
**Lessons processed:** L01–L08 (8 lessons)

---

#### Summary

| File | HT blocks added | Status |
|------|----------------|--------|
| L01 | 0 | Copied unchanged — no HT content |
| L02 | 1 (new) | Gas pressure/temperature section wrapped |
| L03 | 1 (new) | v²=u²+2as equation wrapped; existing v-t area blocks preserved |
| L04 | 0 | Copied unchanged — terminal velocity, momentum, inertia already tagged |
| L05 | 1 (new) | Energy stored in spring (½ke²) collapsible wrapped |
| L06 | 0 | Copied unchanged — no HT content |
| L07 | 0 | Copied unchanged — no HT content |
| L08 | 0 | Copied unchanged — motor effect/Fleming's LHR already tagged |

**Total new `higher-only` wrappers added: 3**  
**Pre-existing `higher-only` blocks preserved: 5** (L03 ×2, L04 ×2, L08 ×1)

---

#### Spec-point to lesson mapping

### P1 — Matter

| Spec point | Content | Lesson | Action |
|-----------|---------|--------|--------|
| P1.2g | Explain molecular motion in gas relates to temperature and pressure | L02 n29–n30 | **WRAPPED** (h2 + n29 + n30 + n31) |
| P1.2h | Explain temperature/pressure relationship at constant volume (qualitative) | L02 n30 | Same block as above |

### P2 — Forces

| Spec point | Content | Lesson | Action |
|-----------|---------|--------|--------|
| PM2.1iii | Apply v² = u² + 2as | L03 n12–n14 | **WRAPPED** |
| P2.1f | Interpret enclosed areas in v-t graphs | L03 n23h + n24h | Already tagged (preserved) |
| PM2.2ii | Recall and apply p = mv | L04 n27–n30 | Already tagged in momentum collapsible (preserved) |
| P2.2f | Terminal velocity examples (skydivers, vehicles) | L04 n24–n26 | Already tagged (preserved) |
| P2.2j | Inertia definition; inertial mass = F/a | L04 n30 | Inside pre-existing momentum block (preserved) |
| P2.2k | Define momentum; conservation in collisions | L04 n27–n29 | Inside pre-existing momentum block (preserved) |
| PM2.3ii | Apply E_e = ½ke² | L05 n12–n14 | **WRAPPED** (whole collapsible) |

### P3 — Electricity and magnetism

| Spec point | Content | Lesson | Action |
|-----------|---------|--------|--------|
| PM3.3i | F = BIl equation | L08 n16 | Already tagged in motor effect block (preserved) |
| P3.3h | Force between magnet and conductor | L08 n14 | Already tagged (preserved) |
| P3.3i | Fleming's left-hand rule | L08 n19–n21 | Already tagged (preserved) |
| P3.3j | Apply F = BIl to calculate forces | L08 n17 | Already tagged (preserved) |
| P3.3k | How motor effect causes rotation | L08 n23–n24 | Already tagged (preserved) |

### Spec points not found in these lessons

| Spec point | Content | Note |
|-----------|---------|------|
| P2.2e | Vector diagrams, resolution of forces, scale drawings | No content for this in L01–L08; would fall in a dedicated vectors/forces lesson if it exists |
| P2.2g | Free body diagrams — two or more forces, resultant force | Same — no dedicated content found |
| P2.2h | Free body diagrams — balanced forces, zero resultant (qualitative) | Same |
| P2.2p | Object in circle, constant speed but changing velocity | L03 n5 mentions this concept but it is a brief introductory statement about vectors, not an extended HT treatment; conservatively left untagged |

---

#### Wrapping decisions

### Conservative approach taken

- Only `<p data-narration-id>` elements and their enclosing section headings (`<h2>`) were wrapped where the h2 exists solely to introduce HT content.
- Collapsibles were wrapped as a unit (outer `div.collapsible`) when the entire collapsible body is HT (L05 "Energy Stored in a Spring").
- No prose was altered. No attributes were changed.
- Existing `higher-only` blocks were not re-wrapped or restructured.

### L02 — Gas pressure/temperature (P1.2g/h)

The spec makes clear both g and h are HT-only. The lesson's "Gas Pressure and Temperature" section (h2 + three paragraphs) is entirely HT content. Wrapped all four elements together in one `<div class="higher-only">` at the end of the lesson.

### L03 — v²=u²+2as (PM2.1iii)

Spec point PM2.1iii requires applying `v² = u² + 2as`. The basic `a = (v−u)/t` equation (n9–n11) is Foundation-level and was left untouched. The transition sentence "For uniform (constant) acceleration, you also need the equation:" (n12) is part of the HT block and was included in the wrapper alongside n13 and n14.

### L05 — Elastic PE equation (PM2.3ii)

The `½ke²` equation is explicitly HT-only (PM2.3ii). The entire "Energy Stored in a Spring" collapsible covers only this equation and its application. The wrapper was placed around the outer `div.collapsible` so the collapsed button is also hidden for Foundation students.

### P2.2p borderline call (L03 n5)

L03 n5 contains one sentence: "An object travelling in a circle at constant speed has a changing velocity because its direction constantly changes — meaning it is always accelerating, even though its speed stays the same." Spec P2.2p is listed as HT-only. However, this sentence is embedded mid-paragraph within the foundational Speed/Velocity section and is phrased as an illustrative example of the vector/scalar distinction (which is Foundation content). Wrapping it would require splitting the paragraph, which the task instructs against. The HT-specific aspect (circular motion as the main topic) is not the primary purpose of this paragraph. Left untagged; flagged here for human review.

## physics-paper-2

### HT-tagging report — OCR Gateway A Combined Science Physics Paper 2

Generated: 2026-05-10

#### Lessons processed

| File | HT spec points matched | Action |
|------|------------------------|--------|
| L01 — Types of Wave, Wave Properties, Wave Speed, Reflection/Refraction/Diffraction | None in P4.1 area | Copied unchanged |
| L02 — EM Spectrum, Hazards, Absorption/Transmission/Reflection | P4.2i (already wrapped), P4.2j (newly wrapped) | 1 new `higher-only` block added |
| L03 — Atomic Structure, Radioactivity, Half-Life | None new — existing blocks untouched | Copied unchanged |
| L04 — Uses of Radioactive Materials | None in P7.2 area | Copied unchanged |
| L05 — Conservation of Energy, Work Done, Efficiency | P5.2e (already wrapped) | Copied unchanged |
| L06 — Energy Resources, National Grid | PM6.2i transformer equation not present in prose | Copied unchanged |
| L07 — Motion, Velocity-Time Graphs, Stopping Distance | No P8 HT points in extract | Copied unchanged |
| L08 — Solar System, Satellites, Stars | No P8.3 HT points in extract | Copied unchanged |

#### New `higher-only` blocks added: 1

### L02 — `data-narration-id="n24"` (P4.2j)

**Spec point:** P4.2j — "recall that different substances may absorb, transmit, refract, or reflect electromagnetic waves in ways that vary with wavelength"

**Content wrapped:**
> A given material may absorb some wavelengths, transmit others, and reflect the rest. For example, glass transmits visible light but absorbs UV. The atmosphere transmits visible light and radio waves but absorbs most UV, X-rays and gamma rays…

**Rationale:** This paragraph specifically describes wavelength-dependent behaviour, which is the HT aspect of P4.2j. The preceding paragraph (n23) describes the four interaction types (absorption, transmission, reflection, refraction) in general terms — this is Foundation-accessible and left unwrapped. The n24 paragraph adds the wavelength-selective dimension that the HT spec point requires.

**P4.2k note:** The refraction explanation in n23 ("changes speed (and may change direction) when entering a different material") covers basic refraction at Foundation level. The HT spec point P4.2k asks students to "explain how some effects are related to differences in the velocity of EM waves in different substances" — this deeper mechanistic explanation is not developed separately from the Foundation refraction description in this lesson, so no additional wrapping was applied for P4.2k. A future content author may wish to add a higher-only collapsible developing the velocity-difference explanation for refraction effects.

#### Pre-existing `higher-only` blocks (untouched)

| File | Narration IDs | Content |
|------|---------------|---------|
| L02 | wraps `n25` collapsible | Radio waves / oscillations in electrical circuits (P4.2i) |
| L03 | wraps `n22h` | Fraction remaining formula (1/2)^n |
| L03 | wraps `n23h` key-fact | Key Fact for (1/2)^n formula |
| L05 | wraps collapsible containing n26–n32 | Reducing Wasted Energy / ways to increase efficiency (P5.2e) |

#### HT spec points with no content to wrap

| Spec point | Reason |
|------------|--------|
| PM6.2i — transformer equation `Vp × Ip = Vs × Is` | The equation is absent from L06 prose. The lesson describes step-up/step-down transformers conceptually (n20) but does not include the formula. Foundation lesson; HT formula would need to be added, not wrapped. |
| P4.2k — effects related to velocity differences | No standalone HT paragraph to wrap; basic refraction described at Foundation level in n23. See P4.2k note above. |
