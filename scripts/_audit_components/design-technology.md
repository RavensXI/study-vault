# D&T Audit — Specialist Technical Principles / Material Areas

**Date:** 2026-06-01
**Slugs audited:** `design-technology` (AQA 8552), `design-technology-eduqas` (Eduqas C600QS / WJEC 3600QS)

---

## Slug 1: `design-technology` (AQA 8552)

### 1. Optionality — Written Exam

**The AQA written exam does NOT require students to choose one material area.** All material categories are examined together.

Spec section 3.2 (p.19) states:

> "In addition to the core technical principles, **all students** should develop an in-depth knowledge and understanding of the following specialist technical principles: [...] Each specialist technical principle should be **delivered through at least one material category or system**. Not all of the principles outlined above relate to every material category or system, but **all must be taught**."

Section 2.2 (exam structure) shows Section B is simply "Specialist technical principles (30 marks) — Several short answer questions (2–5 marks) and one extended response." There is no separate option section or candidate choice. Questions are set across material categories but all students sit the same paper.

**Conclusion: No student choice is required in the written exam.** The spec wording "through at least one material category" is a teaching/delivery instruction — it means each *principle* (e.g. forces and stresses) must be taught using at least one material as the example vehicle. It does not mean different students specialise in different materials for exam purposes.

The 6 material categories the principles can be delivered through are:
- papers and boards
- timber based materials
- metal based materials
- polymers
- textile based materials
- electronic and mechanical systems

### 2. Coverage

**Units built:**

| Unit | Slug | Lessons |
|------|------|---------|
| Core Technical Principles | `core-technical` | 6 |
| Specialist Technical Principles | `specialist-technical` | 7 |
| Designing & Making Principles | `designing-making` | 7 |

**Core Technical (6 lessons):** L1 New & Emerging Technologies, L2 Energy Generation & Storage, L3 Modern & Smart Materials, L4 Systems Approach to Designing, L5 Mechanical Devices, L6 Materials & Their Working Properties. Matches spec 3.1.1–3.1.6 exactly.

**Specialist Technical (7 lessons):** L1 Selecting Materials & Components, L2 Forces & Stresses, L3 Ecological & Social Footprint, L4 Sources, Origins & LCA, L5 Stock Forms Types & Sizes, L6 Scales of Production, L7 Surface Treatments & Finishes.

**Gap identified:** Spec 3.2.8 lists **Specialist Techniques and Processes** as one of the 9 required specialist technical principles. The build has 7 lessons and omits it. The 9 spec principles are:
1. Selection of materials or components (L1 covered)
2. Forces and stresses (L2 covered)
3. Ecological and social footprint (L3 covered)
4. Sources and origins (L4 covered)
5. Using and working with materials — **MISSING** (no dedicated lesson; spec 3.2.5 covers properties, modification of properties, and shaping/forming per material category — partially addressed inside other lessons but not explicitly)
6. Stock forms, types and sizes (L5 covered)
7. Scales of production (L6 covered)
8. Specialist techniques and processes — **MISSING as a standalone lesson** (spec 3.2.8 covers production aids, tools/equipment/processes by wastage/addition/deforming categories, tolerances, commercial processes, quality control)
9. Surface treatments and finishes (L7 covered)

So principle 5 ("Using and working with materials", spec 3.2.5) and principle 8 ("Specialist techniques and processes", spec 3.2.8) are not built as standalone lessons. These are the most process-heavy parts of the spec: how to cut, shape, drill, cast, weld, vacuum form, injection mould, sew, solder etc. across all material categories, plus commercial processes (offset litho, routing, milling, weaving, pick-and-place assembly) and quality control.

Note: Some of this content may be partially embedded in other lessons (e.g. L7 finishes touches forming methods lightly), but spec 3.2.5 and 3.2.8 are substantive sections each warranting a dedicated lesson. Currently at 7 lessons; spec coverage would suggest 9 are needed.

**Designing & Making (7 lessons):** L1–L7 cover investigation/research, environmental challenges, work of others, design strategies/communication, prototype development, tolerances/material management, specialist tools/techniques. This maps cleanly to spec 3.3.1–3.3.11.

### 3. Picker

No board-level picker / material-area picker exists for D&T in `free-user-filters.js`. The `index.html` `slugMap` at line 3598 shows the standard board→slug routing (`'aqa': 'design-technology'`), which is correct since there is no material choice for AQA. No fw-step for material specialisation exists, which is correct for AQA — no action needed there.

### 4. Verdict

**PARTIAL-BUILD** — Two of the nine AQA Specialist Technical Principles are not built as lessons: (5) "Using and Working with Materials" (spec 3.2.5 — properties in use, modification of properties, shaping/forming per material category) and (8) "Specialist Techniques and Processes" (spec 3.2.8 — tools/equipment/wastage/addition/deforming/reforming, commercial processes, quality control). The build needs 2 additional lessons in the `specialist-technical` unit to achieve full coverage of Section B exam content.

---

## Slug 2: `design-technology-eduqas` (Eduqas C600QS / WJEC 3600QS)

### 1. Optionality — Written Exam

**The Eduqas written exam (Component 1) requires every student to answer on in-depth knowledge of at least one material area, but all students sit the SAME paper with common questions — there is no separate option section in the exam.**

Spec section 2.1 (p.6) states:

> "In-depth knowledge and understanding is presented in six clear and distinct topic areas: a. electronic systems, programmable components & mechanical devices; b. papers & boards; c. natural & manufactured timber; d. ferrous & non-ferrous metals; e. thermoforming & thermosetting polymers; f. fibres & textiles. **Learners are required to study at least one of these six areas**..."

The assessment summary (p.3–4) states Component 1 is "A mix of short answer, structured and extended writing questions assessing candidates' knowledge and understanding of: technical principles; designing and making principles..." There is no mention of candidate choice in the exam itself (no "Answer ONE from the following" option sections in the written paper). The single-material specialisation determines what content students have studied in depth, but the exam paper itself covers all areas with questions written to be accessible regardless of which area was studied — or, typically, the extended question allows material-specific answers.

**The six in-depth material options are:**
- a. Electronic systems, programmable components & mechanical devices
- b. Papers & boards
- c. Natural & manufactured timber
- d. Ferrous & non-ferrous metals
- e. Thermoforming & thermosetting polymers
- f. Natural, synthetic, blended and mixed fibres; woven, non-woven and knitted textiles

### 2. Coverage

**Units built:**

| Unit | Slug | Lessons |
|------|------|---------|
| Design and Technology in Our World | `design-technology-our-world` | 6 |
| Electronic and Mechanical Systems | `electronic-mechanical-systems` | 5 |
| Materials and Their Properties | `materials-and-properties` | 6 |
| Designing and Making Principles | `designing-and-making-principles` | 5 |

**Design and Technology in Our World (6 lessons):** L1 New and Emerging Technologies, L2 Sustainability and the 6 Rs, L3 Energy Generation and Storage, L4 Smart Materials and Modern Materials, L5 Composites and Technical Textiles, L6 CAD, CAM and Production Techniques. Maps to spec core knowledge areas 1–7 adequately.

**Electronic and Mechanical Systems (5 lessons):** L1–L4 cover electronic systems I/P/O, programmable components, mechanical devices, mechanical calculations. L5 Forces, Stresses and Reinforcement. This unit covers the core (spec 5–7) and the in-depth area (a) as one combined unit. Adequate.

**Materials and Their Properties (6 lessons):** L1 Papers and Boards, L2 Timbers, L3 Metals, L4 Polymers, L5 Natural/Synthetic Textiles, L6 Woven/Non-Woven/Knitted Textiles. This covers the core materials section (spec 8–12) at breadth-level.

**MISSING — In-depth treatment of material areas b through f:** The spec requires in-depth knowledge for the chosen material area (spec p.15–31 details 7 topics for each of the 6 areas: sources/origins/footprint, selection factors, forces/stresses, stock forms, scales of production, specialist techniques, surface finishes). The `materials-and-properties` unit has 6 lessons covering ALL 5 material categories at overview level (core knowledge), but **none of the 6 lessons provides the in-depth treatment** (the 7-topic deep-dive per material area). Students need in-depth coverage of their chosen material to answer Component 1 at depth.

The build is structured as: 1 overview lesson per material category (core breadth). But the spec mandates at least one material area gets the full 7-topic in-depth treatment that covers: physical/working properties in detail, ecological footprint, selection influencers, forces/reinforcement, stock forms with costing, scales of production, specialist techniques (wastage, addition, deforming/reforming), surface treatments.

The `electronic-mechanical-systems` unit functions as both the core introduction AND the in-depth treatment for area (a). That pattern is correct. But areas (b)–(f) have only overview lessons, not in-depth ones.

**Designing and Making Principles (5 lessons):** L1–L5 cover context/user needs, work of designers, design strategies, communicating ideas, prototyping. Covers spec 2.2 core adequately. The in-depth designing/making section (selecting/marking out/tools/techniques/finishes) is not separately built, though it maps to NEA practice rather than exam content.

### 3. Picker

No material-area picker (fw-step) exists in `free-user-filters.js`. The `index.html` shows `'design-technology': { 'AQA': true, 'Eduqas': true, 'WJEC': true }` at line 1816 and the slugMap at line 3598 routes correctly to `design-technology-eduqas`. No material-area selection step was ever wired. Given that the spec says students study *at least one* material area and the build currently covers all areas at overview level (not as separate selectable tracks), no picker mechanism is triggered. However, if in-depth units were built per material area, a picker would be needed to direct students to their relevant unit.

### 4. Verdict

**PARTIAL-BUILD** — The `electronic-mechanical-systems` unit correctly doubles as in-depth treatment for material area (a). However, the other five material areas (papers & boards; timber; metals; polymers; textiles/fibres) each receive only a single overview lesson in `materials-and-properties` at core-knowledge breadth. The spec requires each material area to also be covered at in-depth level (7 topics per area: sources/ecological footprint, selection, forces, stock forms, scales of production, specialist techniques, surface finishes). A student specialising in, say, metals would have no in-depth materials content to study. The build needs either (i) 5 additional in-depth units (one per remaining material area, each ~5–7 lessons) or (ii) a single expanded `materials-in-depth` unit with sub-sections per material, plus a picker to guide students to their chosen area.

---

## Summary

| Slug | Board | Optionality | Verdict |
|------|-------|-------------|---------|
| `design-technology` | AQA 8552 | No student choice — all principles examined for all students, taught through any material vehicle | **PARTIAL-BUILD** — 2 of 9 specialist technical principles not built (3.2.5 "Using and Working with Materials", 3.2.8 "Specialist Techniques and Processes") |
| `design-technology-eduqas` | Eduqas C600QS / WJEC 3600QS | Students study ≥1 in-depth material area; exam paper is common but in-depth questions expected from chosen area | **PARTIAL-BUILD** — In-depth treatment (7-topic deep-dive) built only for area (a) Electronic/Mechanical Systems; areas (b)–(f) [papers, timber, metals, polymers, textiles] have overview-only lessons. No in-depth units or picker for remaining 5 material areas. |
