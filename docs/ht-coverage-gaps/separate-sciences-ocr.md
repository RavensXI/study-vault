# HT coverage gaps — separate-sciences-ocr (Triple OCR Gateway A)

HT spec points the lesson prose does NOT develop. These need new content commissioned before the existing tier filter will reveal them on Higher tier.

Approx. 9 flagged items across 6 paper-level reports.

---

## biology-paper-1

### HT Tagging Report — OCR Gateway A Triple Biology Paper 1

**Spec source:** `scripts/_pilot_higher_only/ocr-biology-a-gateway-J247_ht.md`  
**Scope:** B1–B3 HT spec points (9 of 18 total — B5/B6 are Paper 2, not tagged here)  
**Date:** 2026-05-10

---

#### Wraps applied

### L02 — DNA, Protein Synthesis, Enzymes, Mitosis

| narration-id | Content | Spec code | Rationale |
|---|---|---|---|
| n3 | Triplet code paragraph ("Each group of three bases codes for a particular amino acid…") | B1.2e | HT: explain how DNA structure affects proteins via triplet code |
| n6 | Transcription/translation paragraph ("The journey from gene to protein involves two key stages…") | B1.2d | HT: describe protein synthesis — unzipping, mRNA, translation, amino acid assembly |

**Notes:** n7 (proteins as enzymes/hormones/antibodies) was left untagged — it is general foundational content not confined to B1.2d/e. The h2 heading n5 ("From DNA to Protein") was left visible so Foundation students see the section exists; only the mechanistic detail paragraph n6 is hidden.

---

### L04 — Photosynthesis

| narration-id | Content | Spec code | Rationale |
|---|---|---|---|
| n16 (inside existing `higher-only`) | Interaction of limiting factors paragraph | B1.4f | Already tagged in source — copied unchanged |

No new wraps added.

---

### L07 — Nervous System and the Brain

| narration-id | Content | Spec code | Rationale |
|---|---|---|---|
| n21 | Brain function methods and complexity paragraph ("Our understanding of brain function comes from several sources…") | B3.1g + B3.1h | Covers difficulties of investigating brain function (EEG, MRI, case studies, complexity) and the challenge of treating brain disorders |

**Coverage note:** n21 is a single paragraph that partially covers both B3.1g (difficulties of investigating) and B3.1h (limitations of treatment). The lesson does not have dedicated paragraphs for each point — no deeper text existed to wrap. The HT content here is thinner than the spec demands (the spec asks for: limited ability to repair nervous tissue, irreversible damage, difficulty accessing brain; the lesson only says "treating brain disorders challenging"). This is a coverage gap (see below).

---

### L08 — Endocrine System

| narration-id / block | Content | Spec code | Rationale |
|---|---|---|---|
| n5–n6 (inside existing `higher-only`) | Thyroxine negative feedback + adrenaline | B3.2b | Already tagged in source — copied unchanged |
| n9 | FSH/LH/oestrogen/progesterone interactions paragraph | B3.2d | HT: explain interactions of all four hormones in menstrual cycle control |
| n13 (inside existing `higher-only`) | IVF and fertility treatments | B3.2f | Already tagged in source — copied unchanged |
| Collapsible: "Uses of Plant Hormones in Agriculture" (n17–n19) | Selective herbicides, root cuttings, seedless fruit (gibberellins), ethene/dormancy | B3.2i | HT: describe different ways people use plant hormones |

**Notes on n9:** The key-fact box (n10) summarising the menstrual cycle was left untagged — it provides a brief F&H-appropriate summary of the cycle names without the detailed interaction mechanism. The introductory sentence n8 was also left untagged as it only names the cycle. The detailed interaction is confined to n9.

**Notes on plant hormones collapsible:** The entire `<div class="collapsible">` block wrapping n17/n18/n19 was placed inside `<div class="higher-only">` rather than wrapping individual `<p>` elements, because the collapsible button and wrapper are inseparable from the content paragraphs. This is consistent with the approach already used for the thyroxine/adrenaline and fertility treatment blocks in the source file.

---

#### Unchanged lessons (copied verbatim)

| Lesson | Topic | Reason no wraps |
|---|---|---|
| L01 | Eukaryotic/prokaryotic cells, microscopy | No B1.2d/e content in this lesson (protein synthesis is covered in L02) |
| L03 | Respiration, biological molecules | No HT spec points in B1.2 respiration topics; all respiration outcomes are F&H |
| L05 | Transport, osmosis, SA:V | No HT spec points in B1.3 or B2 topics |
| L06 | Plant and human transport, circulatory system | No HT spec points in B2 or B3 vascular topics |

---

#### Coverage gaps — honest assessment

### B3.1h — Limitations of treating brain/nervous damage
The spec requires: "limited ability to repair nervous tissue, irreversible damage to surrounding tissues, difficulties with accessing parts of the brain." L07 n21 only gives a general statement ("This makes treating brain disorders challenging"). The specific mechanisms listed in B3.1h are not present in the lesson text. **Wrap applied conservatively to the closest paragraph, but the underlying content is insufficient for a full HT answer on this point.**

### B3.1g — Difficulties of investigating brain function
The spec requires: "difficulty in obtaining and interpreting case studies and the consideration of ethical issues." L07 n21 mentions EEG and MRI but does not explicitly discuss case study interpretation difficulties or ethical issues. **Partial coverage only — same paragraph wrapped, same gap as B3.1h.**

### B1.2d — tRNA as carrier of amino acids
The spec explicitly lists "tRNA as the carrier of amino acids" as a required detail in B1.2d. L02 n6 covers unzipping, mRNA, transcription and translation but does not mention tRNA. **The wrapped content is a close match but misses one required detail.**

### B3.2d — Menstrual cycle graph reading
The spec mentions understanding graphs of hormone levels across the cycle. L08 does not include a graph or explicit graph-reading guidance. The hormone interaction text (n9) covers the mechanism, but graph interpretation is not present. **Content-level gap, not a tagging issue.**

---

#### Summary table

| Lesson | New wraps | Pre-existing higher-only | Action |
|---|---|---|---|
| L01 | 0 | 0 | Copied unchanged |
| L02 | 2 (n3, n6) | 0 | Tagged |
| L03 | 0 | 0 | Copied unchanged |
| L04 | 0 | 1 (n16) | Copied unchanged |
| L05 | 0 | 0 | Copied unchanged |
| L06 | 0 | 0 | Copied unchanged |
| L07 | 1 (n21) | 0 | Tagged |
| L08 | 2 (n9, collapsible n17–n19) | 2 (thyroxine block, fertility block) | Tagged |
| **Total** | **5 new wraps** | **3 pre-existing** | |

## biology-paper-2

### HT-Tagging Report — OCR Gateway A Triple Biology Paper 2

**Date:** 2026-05-10  
**Source spec:** `scripts/_pilot_higher_only/ocr-biology-a-gateway-J247_ht.md`  
**Scope:** B4–B6 HT points only (Bio Paper 2). B1/B3 HT points in Paper 2 lessons noted separately.

---

#### Lesson outcomes

| File | Topic | HT points present | Action | New `higher-only` blocks |
|------|-------|-------------------|--------|--------------------------|
| L01 | Homeostasis, Blood Glucose, Temp | B3.3d (glucagon) — already wrapped | Copy unchanged | 0 (pre-existing: 1) |
| L02 | Kidneys, ADH, Kidney Failure | B3.3i + B3.3j (ADH negative feedback + osmotic challenges) | HT added | 1 |
| L03 | Ecosystems, Energy Transfer | B4.1c (10% energy efficiency) — already wrapped | Copy unchanged | 0 (pre-existing: 1) |
| L04 | DNA, Protein Synthesis | B1.2d/e (protein synthesis, triplet code) — Paper 1 HT, out of scope | Copy unchanged | 0 |
| L05 | Genetics, Inheritance | B5.1e (coding/non-coding DNA variants) — content not present in lesson | Copy unchanged | 0 |
| L06 | Evolution, Evidence | B5.2 has no HT-only points per spec | Copy unchanged | 0 |
| L07 | Monitoring Ecosystems | B6.1d (evaluate evidence for environmental changes) — no isolatable HT prose | Copy unchanged | 0 |
| L08 | Food Security, GM, Tissue Culture | B6.2e (genetic engineering process) | HT added | 1 |
| L09 | Disease, Immunity, Monoclonal Ab | B6.3m/n (monoclonal antibodies) — already wrapped; B6.3i (plant disease) not in lesson | Copy unchanged | 0 (pre-existing: 1) |

**Total new `higher-only` blocks added: 2**  
**Pre-existing `higher-only` blocks untouched: 3**

---

#### Detail on new blocks

### L02 — B3.3i / B3.3j (ADH negative feedback + osmotic challenges)

**Spec points:**
- **B3.3i**: Describe the effect of ADH on the permeability of the kidney tubules (amount of water reabsorbed and negative feedback)
- **B3.3j**: Explain the response of the body to different temperature and osmotic challenges (dehydration, excess water, high salt; mechanism of kidney function, thirst)

**Wrapped:** The "Negative Feedback: How ADH Controls Water Levels" collapsible (n12–n13) and the ADH key-fact (n14).

**Left unwrapped:** n11 (introduces ADH role and basic permeability — F&H level coverage of B3.3f).

**Rationale:** n12–n13 provide the full negative feedback loop with osmoreceptor response to dehydration and excess water intake (directly addressing B3.3i and B3.3j). n14 key-fact summarises HT content. The introductory paragraph n11 covers the basic F&H concept that ADH controls water reabsorption and increases tubule permeability.

---

### L08 — B6.2e (Genetic Engineering — main steps)

**Spec point:**
- **B6.2e**: Describe the main steps in the process of genetic engineering (restriction enzymes, sticky ends, ligase, host bacteria, selection using antibiotic resistance markers, vectors e.g. plasmids)

**Wrapped:** The entire "Genetic Modification" collapsible (n8–n10), covering the GM process (restriction enzymes, vectors), GM crop examples (golden rice), and concerns/ethics.

**Left unwrapped:** n11 key-fact (summarises both selective breeding and GM at a high level — retained as F&H context). Selective breeding prose (n5–n7), tissue culture (n13) and biological control (n14–n16) are all F&H.

**Rationale:** The GM collapsible is the only content in L08 corresponding to B6.2e. The key-fact at n11 is summary-level and mentions GM only briefly alongside selective breeding, so it remains visible to Foundation students as contextual orientation. The collapsible contains all the HT process detail.

---

#### Out-of-scope notes

### L04 — Protein Synthesis (B1.2d/B1.2e)
Protein synthesis content (n17–n19 collapsible) maps to B1.2d/e, which are Paper 1 HT points. These are outside the Paper 2 B4–B6 filter and have not been tagged.

### L05 — B5.1e (Coding/non-coding DNA variants)
B5.1e ("genetic variants influencing phenotype in coding and non-coding DNA") is a Paper 2 HT point but no corresponding prose exists in L05. The lesson covers genotype/phenotype and inheritance patterns at a level consistent with F&H spec points (B5.1a–d). Flag for content review if a B5.1e section is to be added.

### L07 — B6.1d (Evaluate evidence for environmental changes)
B6.1d is an HT evaluation demand. The lesson covers indicator species, sampling, eutrophication and conservation strategies — all at F&H depth. No prose block is isolatable as purely HT content; B6.1d is an analytical skill applied to the F&H body of knowledge. No tagging applied. This is the expected pattern for evaluation-command HT points.

### L09 — B6.3i (Plant disease detection)
B6.3i (laboratory and field detection of plant diseases) does not appear in L09, which focuses entirely on human communicable/non-communicable diseases and the immune response. B6.3m/n (monoclonal antibodies) were already correctly tagged in the source file.

---

#### Verification checklist

- [x] No existing `higher-only` blocks altered
- [x] No prose content changed
- [x] All `data-narration-id` attributes preserved
- [x] All `dfn`, `strong`, `em`, `collapsible` structures intact
- [x] `<div class="higher-only">` wraps at block level (outside `<p>` tags, wrapping whole collapsibles/key-facts)
- [x] Unchanged lessons copied verbatim

## chemistry-paper-1

### HT Tagging Report — OCR Gateway A Triple Chemistry Paper 1

**Spec source:** `scripts/_pilot_higher_only/ocr-chemistry-a-gateway-J248_ht.md`  
**Lessons processed:** L01–L08 (8 lessons)  
**HT spec points in scope (C1–C3):** C1.1c, C2.3g–j, C3.1e/g/h/k/l, C3.2d, C3.3b/g/i/j

---

#### Lesson-by-lesson decisions

| Lesson | Topic | HT content found | Action |
|--------|-------|-----------------|--------|
| L01 | The Particle Model | C1.1c — limitations of particle model (n15–n17) | **Already tagged** — existing `higher-only` block present. Copied unchanged. |
| L02 | The Structure of the Atom | None (atomic number, isotopes, electronic config are all-tier) | Copied unchanged. |
| L03 | The Periodic Table | None (Group 1/7/0 trends are all-tier at this level) | Copied unchanged. |
| L04 | Separation Techniques | None | Copied unchanged. |
| L05 | Chemical Bonding | Dative covalent bond (n11) — **Already tagged** — existing `higher-only` block. Note: dative bonds are not listed in C1–C3 HT spec extract but the block was pre-existing; left untouched. | Copied unchanged. |
| L06 | Structure, Properties and Nanoparticles | **C2.3g–j** — nano dimensions, surface area to volume ratio, properties related to uses, risks (n14 heading + n15, n16, collapsible n17) | **WRAPPED** — new `higher-only` div around entire nanoparticles section. See below. |
| L07 | Chemical Equations and Moles | C3.1g/h — mole concept, Avogadro's constant, reacting masses (n20–n29) | **Already tagged** — existing `higher-only` block present. Copied unchanged. |
| L08 | Energy Changes | C3.2d — bond energy calculations (n13–n18) | **Already tagged** — existing `higher-only` block present. Copied unchanged. |

---

#### L06 — Change detail

**Spec points covered:** C2.3g (nano dimensions vs atom/molecule scale), C2.3h (surface area to volume ratio), C2.3i (properties related to uses), C2.3j (risks of nanoparticulate materials).

**Wrapped:** `<h2 data-narration-id="n14">` through the end of the Risks collapsible `</div>` (lines 35–47 in `_in`).

```html
<div class="higher-only">
<h2 data-narration-id="n14">Nanoparticles</h2>
<p data-narration-id="n15">...</p>   <!-- C2.3g/h: nano scale, SA:V ratio -->
<p data-narration-id="n16">...</p>   <!-- C2.3i: properties related to uses -->
<div class="collapsible">            <!-- C2.3j: risks -->
  ...
  <p data-narration-id="n17">...</p>
</div>
</div>
```

The following section (`<h2 data-narration-id="n18">Polymers and Metals</h2>` + n19) is all-tier and was left outside the wrapper.

---

#### HT spec points NOT found in lessons (C1–C3)

The following C3 HT points were not directly represented as standalone sections in any lesson, likely because they are assessed via calculation practice rather than article content, or because they fall in later lessons not included in this batch:

- **C3.1e** — balanced ionic equations
- **C3.1k** — stoichiometry / limiting reagent
- **C3.1l** — reacting mass calculations from balanced equations (partial — n29 in L07 touches this inside the already-tagged mole block)
- **C3.3b** — redox in terms of electron transfer
- **C3.3g** — dilute/concentrated vs weak/strong acids
- **C3.3i/j** — pH and hydrogen ion concentration

These were not found as unwrapped content in L01–L08 and require no action here.

---

#### Output files

| File | Status |
|------|--------|
| L01_out.html | Copied — pre-existing `higher-only` block (C1.1c) |
| L02_out.html | Copied — no HT content |
| L03_out.html | Copied — no HT content |
| L04_out.html | Copied — no HT content |
| L05_out.html | Copied — pre-existing `higher-only` block (dative bonds) |
| L06_out.html | **EDITED** — nanoparticles section (n14–n17) wrapped in `higher-only` |
| L07_out.html | Copied — pre-existing `higher-only` block (C3.1g/h moles) |
| L08_out.html | Copied — pre-existing `higher-only` block (C3.2d bond energies) |

## chemistry-paper-2

### HT Tagging Report — OCR Gateway A Triple Chemistry Paper 2

**Source spec:** `scripts/_pilot_higher_only/ocr-chemistry-a-gateway-J248_ht.md`
**Lessons processed:** L01–L09 (9 lessons)
**Output files:** `LNN_out.html` written for all 9 lessons

---

#### Per-lesson summary

### L01 — Oxidation, Reduction, Acids, Salts
**Spec refs:** C3.3b (electron-transfer redox), C3.3g (strong/weak/dilute/concentrated), C5.1b (titration)
**Changes:** 3 new/adjusted blocks
- n5 — already wrapped (C3.3b: redox in terms of electron transfer)
- n11 + n12 — wrapped together: strong/weak/dilute/concentrated distinction and key fact (C3.3g HT). Note: n11 opens with Foundation-level pH scale description but the paragraph is dominated by HT strong/weak content; wrapped as a unit.
- Titration collapsible (n19) — wrapped: describing the titration technique is C5.1b HT.
- Neutralisation and acid reactions (n13–n18) left unwrapped — Foundation content.

### L02 — Electrolysis
**Changes:** None. Two existing `higher-only` blocks retained:
- Half-equations for molten lead bromide (n8–n11)
- Half-equations for aluminium extraction (n27–n29)
**Output:** copied unchanged.

### L03 — Qualitative Analysis
**Changes:** None. One existing `higher-only` block retained:
- Instrumental methods and flame emission spectroscopy (n20–n22) (C4.2f/g HT)
**Output:** copied unchanged.

### L04 — Rate of Reaction
**Spec check:** C6.1e ("interpret graphs of reaction conditions versus rate") applies to industrial process condition graphs (Haber, etc.), not to the volume-vs-time rate measurement graphs in this lesson. All content in L04 maps to Foundation-level collision theory and rate measurement.
**Changes:** None.
**Output:** copied unchanged.

### L05 — Reversible Reactions and Equilibria
**Changes:** None. One existing `higher-only` block retained:
- Le Chatelier's Principle + Haber Process analysis (n13–n23) (C5.3c HT)
**Output:** copied unchanged.

### L06 — Atom Economy, Yield, LCA, Recycling, Metal Extraction
**Spec refs:** C5.1g (theoretical mass), C5.1h (% yield), C5.1i (define atom economy), C5.1j (calculate atom economy), C6.1c (evaluate alternative biological methods)
**Changes:** 2 new blocks
- n2–n8 (entire atom economy and % yield section including key fact) — wrapped. All four C5.1 calculation/definition items are HT.
- "Comparing Extraction Methods" collapsible (n21) — wrapped (C6.1c: evaluate alternative biological methods). The description of phytomining/bioleaching (n17–n20) is Foundation and left unwrapped.
- LCA (n10–n11), Recycling (n13–n15), Sustainability (n23) — Foundation-level, not wrapped.

### L07 — Organic Chemistry (Alkanes, Alkenes, Alcohols, Carboxylic Acids, Polymers)
**Spec refs:** C6.2a–j (ALL HT): functional groups, homologous series, first-four members, addition reactions, addition polymerisation, condensation polymerisation, polymer structure deduction.
**Changes:** Entire lesson wrapped in a single `<div class="higher-only">`.
Foundation students have no organic chemistry in OCR Gateway A — every paragraph is HT-only.

### L08 — Atmosphere, Climate Change, Pollutants
**Spec check:** No HT spec items from the extract map to atmospheric composition, greenhouse effect, climate change evidence, or combustion pollutants. These are shared Foundation/Higher content in C6.
**Changes:** None.
**Output:** copied unchanged.

### L09 — Resources, Water, Haber Process, NPK Fertilisers
**Spec refs:** C6.1g (Haber process importance in agriculture), C6.1i (N, P, K role), C6.1j (industrial production of fertilisers as integrated processes)
**Changes:** 1 new block
- n18 (heading) + n19–n20 (Haber process → NPK fertilisers section and key fact) — wrapped (C6.1g, i, j HT).
- Finite/renewable resources, sustainable development, potable water, desalination, sewage treatment — Foundation-level, not wrapped.

---

#### Wrapping decisions — methodology notes

1. **Unit rule:** wrap the whole `<p data-narration-id>` element even if the opening sentence touches Foundation content, provided the paragraph's substance is dominated by HT material (applied to L01 n11).
2. **Collapsibles:** a collapsible whose entire content is HT is wrapped at the `<div class="higher-only">` level outside the `<div class="collapsible">`. The collapsible markup is preserved inside.
3. **Existing blocks untouched:** pre-existing `higher-only` divs in L01, L02, L03, L05 were not modified.
4. **Conservative approach:** when a topic could be argued either way (e.g. LCA evaluation, sewage treatment), it was left unwrapped unless it appears explicitly in the HT extract.
5. **C6.1e interpretation:** "interpret graphs of reaction conditions versus rate" (C6.1e) was not applied to L04's basic volume-vs-time graphs. C6.1e refers to industrial condition graphs (e.g. temperature/pressure vs yield/rate for the Haber process), which appear only in the L05 context and are already under the Le Chatelier block.

---

#### HT blocks per lesson (final state)

| Lesson | Topic | Existing HT blocks | New HT blocks | Total |
|--------|-------|--------------------|---------------|-------|
| L01 | Redox, Acids, Salts | 1 (n5) | 2 (n11–12; titration collapsible) | 3 |
| L02 | Electrolysis | 2 | 0 | 2 |
| L03 | Qualitative Analysis | 1 | 0 | 1 |
| L04 | Rate of Reaction | 0 | 0 | 0 |
| L05 | Equilibria | 1 | 0 | 1 |
| L06 | Atom Economy / Metal Extraction | 0 | 2 | 2 |
| L07 | Organic Chemistry | 0 | 1 (whole lesson) | 1 |
| L08 | Atmosphere / Climate | 0 | 0 | 0 |
| L09 | Resources / NPK | 0 | 1 (Haber/NPK section) | 1 |

## physics-paper-1

### HT Tagging Report — OCR Gateway A Triple Physics Paper 1

**Date:** 2026-05-10  
**Input dir:** `scripts/_pilot_higher_only/ocr/separate-sciences-ocr/physics-paper-1/`  
**HT spec source:** `scripts/_pilot_higher_only/ocr-physics-a-gateway-J249_ht.md`

---

#### Summary

8 lessons processed. 1 lesson modified; 7 copied unchanged (existing wraps already correct or no HT content present).

---

#### Lesson-by-lesson decisions

### L01 — Particle Model, Density, Pressure (P1 Matter)
**Status: copied unchanged — existing `higher-only` block already correct**

- `<div class="higher-only">` already wraps the "Calculating Pressure in a Fluid Column" collapsible (n21–n24). Covers spec points P1.3i and P1.3j (explain/calculate pressure at depth: p = hρg).
- The "Gas Pressure and Temperature" collapsible (n26) was reviewed against P1.3e ("doing work on a gas can increase its temperature, e.g. bicycle pump"). The collapsible describes *heating* a gas at constant volume raising pressure via kinetic theory — that is Foundation-level particle model content, not specifically P1.3e (which concerns compression doing work). Not wrapped.
- The introductory qualitative pressure paragraph (n20) describes pressure increasing with depth qualitatively — Foundation-accessible content present in both tiers. Not wrapped.

### L02 — Changes of State, SHC, SLH (P1 Matter)
**Status: copied unchanged — no P1–P4 HT content present**

No HT spec points apply to this lesson's content (changes of state, internal energy, specific heat capacity, specific latent heat are all Foundation-accessible topics at the level taught here).

### L03 — Speed, Velocity, Graphs, Terminal Velocity (P2 Forces)
**Status: MODIFIED — 1 new `higher-only` block added**

**Existing wrap (preserved):**
- `<div class="higher-only">` around n24 (area under v-t graph). Covers P2.1f.

**New wrap added:**
- Wrapped `<h2 data-narration-id="n26">Terminal Velocity</h2>` plus paragraphs n27, n28, n29 in a single `<div class="higher-only">` block.
- Spec point: **P2.2f** — "describe examples of the forces acting on an isolated solid object or system (To include: examples of objects that reach terminal velocity for example skydivers and applying similar ideas to vehicles)". This is explicitly listed as Higher Tier only in J249.

**Not wrapped (rationale):**
- n5 (circular motion sentence within the "Velocity" paragraph): P2.2q is HT, but the sentence sits inside a Foundation paragraph covering velocity/displacement as vectors. The paragraph cannot be split without altering prose. Conservative decision: leave as mixed paragraph, flag for future review if a full paragraph rewrite is ever done.

### L04 — Newton's Laws, Stopping Distance (P2 Forces)
**Status: copied unchanged — existing `higher-only` block already correct**

- `<div class="higher-only">` already wraps the "Inertial Mass" section (n18–n21). Covers P2.2j.
- Newton's Third Law (n22–n25) and stopping distance (n27–n29) are Foundation content. Not wrapped.
- Momentum (P2.2k) and free body diagrams (P2.2e/g/h) are not present in this lesson.

### L05 — Springs, Moments, Levers (P2 Forces)
**Status: copied unchanged — no HT content present**

Hooke's Law, elastic potential energy, moments, levers and gears are Foundation-accessible at the level covered. No applicable P1–P4 HT points.

### L06 — Electricity: Charge, Resistance, I-V Characteristics (P3 Electricity)
**Status: copied unchanged — no P1–P4 HT content present**

P3 is not part of the HT extract used (which covers P1, P2, P4 topics only). No changes required.

### L07 — Circuits, Mains, Power, National Grid (P3 Electricity)
**Status: copied unchanged — no P1–P4 HT content present**

P3 electricity content. The transformer/National Grid paragraph (n25–n26) touches on transformer principles but P4.2g–i (transformer equations/ratio calculations) are HT for Topic P4 Magnetism — this content appears in L07 at a qualitative Foundation level as context for the National Grid. It does not constitute the P4.2 assessable learning outcomes. Not wrapped.

### L08 — Magnetism, Motor Effect, Electromagnetic Induction (P4 Magnetism)
**Status: copied unchanged — existing `higher-only` block already correct**

- `<div class="higher-only">` already wraps the full Motor Effect / Fleming's Left-Hand Rule / Electric Motors / Electromagnetic Induction section (n11–n24). Covers P4.2a, P4.2b, P4.2c, P4.2d, P4.2e.
- Foundation content (permanent/induced magnets, field lines, electromagnets/solenoids) correctly left unwrapped.

---

#### HT spec points: coverage map

| Spec point | Topic | Lesson | Status |
|------------|-------|--------|--------|
| P1.3e | Doing work on gas raises temp (bicycle pump) | L01 | Not present as distinct HT content — general kinetic theory at Foundation level only |
| P1.3h | Factors influencing floating/sinking | L01 | Not explicitly present as a dedicated section |
| P1.3i | Pressure varies with depth/density, upthrust | L01 | Covered inside existing `higher-only` block (n21–n24) |
| P1.3j | Calculate pressure differences at depth (p=hρg) | L01 | Covered inside existing `higher-only` block (n22–n23) |
| P2.1f | Enclosed area in v-t graphs = distance | L03 | Already wrapped (n24) |
| P2.2f | Terminal velocity (skydivers/vehicles) | L03 | **Newly wrapped (n26–n29)** |
| P2.2j | Inertial mass (F/a ratio) | L04 | Already wrapped (n18–n21) |
| P2.2q | Circular motion / changing velocity | L03 | Mixed into Foundation paragraph (n5) — not wrapped; conservative decision |
| P4.2a–e | Motor effect, Fleming's, F=BIl, motors, induction | L08 | Already wrapped (n11–n24) |

---

#### Files produced

| File | Change |
|------|--------|
| `L01_out.html` | Unchanged copy |
| `L02_out.html` | Unchanged copy |
| `L03_out.html` | **Modified** — terminal velocity section (n26–n29) wrapped in `<div class="higher-only">` |
| `L04_out.html` | Unchanged copy |
| `L05_out.html` | Unchanged copy |
| `L06_out.html` | Unchanged copy |
| `L07_out.html` | Unchanged copy |
| `L08_out.html` | Unchanged copy |

## physics-paper-2

### HT Tagging Report — OCR Gateway A Triple Physics Paper 2

Generated: 2026-05-10  
Spec source: `scripts/_pilot_higher_only/ocr-physics-a-gateway-J249_ht.md`  
Topic scope: P5 (Waves), P6 (Radioactivity), P7 (Energy), P8 (Global challenges)

---

#### Summary

9 lessons processed. 3 lessons modified (new `<div class="higher-only">` blocks added). 6 lessons copied unchanged (existing HT blocks already present, or no HT content identified).

---

#### Lesson-by-lesson decisions

### L01 — Types of Wave / Wave Properties / Reflection, Refraction, Diffraction
**Action: copied unchanged**  
Existing HT block: n29 (sound speed in solids/liquids — P5.1h adjacent context).  
P5.1h (ear structure) and P5.1i (hearing frequency range, ageing) have no corresponding prose in this lesson — content was not written at that level of detail; no tagging opportunity.

### L02 — Electromagnetic Spectrum
**Action: copied unchanged**  
Existing HT block: n25 (radio waves and electrical oscillations — P5.2j).  
P5.3a/P5.3b content (absorption/transmission/reflection varying by wavelength; effects related to velocity differences) appears in n22–n24 but is mixed with foundation-level material (basic absorption/transmission/reflection). Tagging individual paragraphs would cut shared foundation content; left untagged per conservative brief.

### L03 — Reflection, Refraction, Lenses
**Action: copied unchanged**  
Existing HT block: n24 (lens power in dioptres).  
No additional HT spec points identified.

### L04 — Radioactivity
**Action: copied unchanged**  
Existing HT block: n22 (fraction remaining = (½)ⁿ — P6.1k).  
The half-life graph context and ratio calculation are fully covered by the existing block.

### L05 — Uses of Radiation / Fission / Fusion
**Action: copied unchanged**  
No HT spec points from the P5–P8 extract apply to this lesson's content. P6.1k is handled in L04.

### L06 — Energy Stores, Work Done, GPE, KE, Power
**Action: MODIFIED — 1 new block**

| narration ID | content | spec point | change |
|---|---|---|---|
| n31 | Ways to increase efficiency (lubrication, streamlining, insulation, LED) | P7.2e | wrapped |

n31 sits inside the `Efficiency` collapsible (after the formula and worked values). Wrapped as a standalone `<div class="higher-only">` around just that `<p>`. n28–n30 (efficiency definition and formula) retained as shared content — the equation itself is on both tiers; only the "how to increase" requirement is HT.

### L07 — Energy Sources, Efficiency, National Grid
**Action: MODIFIED — 2 new blocks**

| narration IDs | content | spec point | change |
|---|---|---|---|
| n27 | Lubrication, insulation, streamlining, better materials (reducing wasted energy) | P7.2e | wrapped |
| n29–n30 | National Grid — P_lost = I²R; step-up/step-down transformers for efficient high-voltage transmission | P8.2f | wrapped |

n26 (intro: "common techniques include") left outside the HT block — it is a bridging sentence that flows naturally for foundation readers even if the detail below is hidden.  
The National Grid collapsible (n29–n30) is entirely HT per P8.2f ("link PD and turns of transformer to power transfer; relate to advantages of high-voltage transmission"). Both paragraphs wrapped together inside a single `<div class="higher-only">` within the collapsible inner div.

### L08 — Stopping Distance, Momentum, Safety Features
**Action: copied unchanged**  
Existing HT block: n27 (F = Δp/Δt — force–momentum equation).  
P8.1h (estimate forces in typical road situations) — no dedicated paragraph in this lesson targets that specific skill beyond what is already gated by the momentum equation block.

### L09 — Solar System, Satellites, Stars, Red-Shift
**Action: MODIFIED — 1 new block**

| narration IDs | content | spec point | change |
|---|---|---|---|
| n9–n10 | Circular orbit: centripetal force → changing direction, unchanged speed; closer orbit → faster speed, smaller radius | P8.3f, P8.3g | wrapped |

n9–n10 are inside the `Natural Satellites and Gravity in Orbit` collapsible. Both paragraphs wrapped together — they form a single conceptual unit (P8.3f: gravity → changing velocity but unchanged speed; P8.3g: radius must change if speed changes).  
P8.3h (temperature ↔ radiation balance, Earth's atmosphere) and P8.3i (P/S waves, sonar) have no corresponding prose in this lesson; not present to tag.

---

#### HT spec points — coverage summary

| Spec point | Description | Lesson | Tagged? |
|---|---|---|---|
| P5.1h | Sound waves ↔ vibrations in solids; ear structure | L01 | No prose present |
| P5.1i | Limited frequency range; hearing and ageing | L01 | No prose present |
| P5.2i | Velocity/absorption/reflection differences for imaging | L02 | Mixed with foundation; left untagged |
| P5.2j | Radio waves and electrical oscillations | L02 | Pre-existing block (n25) |
| P5.3a | Substances absorb/transmit/refract/reflect EM waves by wavelength | L02 | Mixed with foundation; left untagged |
| P5.3b | Effects related to velocity differences in EM waves | L02 | Mixed with foundation; left untagged |
| P6.1k | Calculate net decline as ratio after n half-lives | L04 | Pre-existing block (n22) |
| P7.2e | Describe ways to increase efficiency | L06 n31, L07 n27 | NEW blocks added |
| P8.1h | Estimate forces in typical road situations | L08 | No dedicated prose beyond F=Δp/Δt block |
| P8.2f | Transformer PD/turns ratio; advantages of high-voltage transmission | L07 n29–n30 | NEW block added |
| P8.3f | Circular orbit: gravity → changing velocity, unchanged speed | L09 n9 | NEW block added |
| P8.3g | Stable orbit: radius must change if speed changes | L09 n10 | NEW block added |
| P8.3h | Body temperature ↔ radiation balance; Earth atmosphere | L09 | No prose present |
| P8.3i | P and S waves; sonar for hidden structure exploration | L09 | No prose present |

---

#### Files written

| File | Status |
|---|---|
| L01_out.html | Copied unchanged |
| L02_out.html | Copied unchanged |
| L03_out.html | Copied unchanged |
| L04_out.html | Copied unchanged |
| L05_out.html | Copied unchanged |
| L06_out.html | Modified — n31 wrapped |
| L07_out.html | Modified — n27 wrapped; n29–n30 wrapped |
| L08_out.html | Copied unchanged |
| L09_out.html | Modified — n9–n10 wrapped |
