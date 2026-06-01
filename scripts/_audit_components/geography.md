# Geography Optional Topics Audit

**Date:** 2026-06-01
**Scope:** All free-tier geography slugs (school_id NULL). Unity school geography (`slug=geography`) is bespoke and excluded.

---

## Summary table

| Slug | Optional groups | Built? | Picker? | Verdict |
|------|----------------|--------|---------|---------|
| geography-aqa | 3 groups (Living World 1-of-2, Physical Landscapes 2-of-3, Resource Management 1-of-3) | All options covered inside flat units — no separate-option structure | None | MISSING-PICKER |
| geography-edexcel-a | 3 groups (Landscapes 2-of-3, Resource Mgmt 1-of-2, Fieldwork 1-of-2 physical + 1-of-2 human) | All options covered inside flat units | None | MISSING-PICKER |
| geography-edexcel-b | 2 groups in Paper 2 exam (fieldwork 1-of-2 physical + 1-of-2 human) — all content compulsory to TEACH | No per-student option required at content-delivery level | None | COMPULSORY (exam-day choice only) |
| geography-ocr | No optional topics — all content compulsory | All content present | None | COMPULSORY |
| geography-eduqas | 2 groups: Component 1 option (Theme 3 OR 4) + Component 2 option (Theme 7 OR 8) | Both options in each pair appear to be built in same unit — no separation | None | MISSING-PICKER |

---

## Detailed findings

### geography-aqa (8035)

**Optional groups in spec:**

1. **Section B: The Living World** — students study Ecosystems + Tropical Rainforests (compulsory) AND **one from Hot Deserts OR Cold Environments** (pick 1 of 2).
2. **Section C: Physical Landscapes in the UK** — students study UK Physical Landscapes overview (compulsory) AND **two from Coastal, River, Glacial landscapes** (pick 2 of 3).
3. **Section C: Resource Management** (Paper 2) — students study the Resource Management overview (compulsory) AND **one from Food, Water OR Energy** (pick 1 of 3).

**Built units:**
- Paper 1: Physical Geography (20 lessons) — flat unit
- Paper 2: Human Geography (20 lessons) — flat unit
- Geographical Skills (12 lessons)

**Coverage of options in Paper 1 (20 lessons):**

| Topic | Lessons | Notes |
|-------|---------|-------|
| Tectonic Hazards | L1–L4 | Compulsory |
| Weather Hazards | L5–L8 | Compulsory |
| Ecosystems + Tropical Rainforests | L9–L11 | Compulsory |
| Hot Deserts | L12–L13 | **Optional A** — included |
| Cold Environments | **MISSING** | **Optional B — NOT BUILT** |
| Coastal Landscapes | L14–L16 | Optional — included |
| River Landscapes | L17–L18 | Optional — included |
| Flood Management (Rivers) | L19–L20 | Optional rivers extension — included |
| Glacial Landscapes | **MISSING** | **Optional — NOT BUILT** |

**Coverage of options in Paper 2 (20 lessons):**

| Topic | Lessons | Notes |
|-------|---------|-------|
| Urban Issues | L1–L8 | Compulsory |
| Changing Economic World | L9–L17 | Compulsory |
| Resource Management Overview | L18 | Compulsory |
| Energy Resource Management | L19–L20 | **Optional A** — included |
| Food Resource Management | **MISSING** | **Optional B — NOT BUILT** |
| Water Resource Management | **MISSING** | **Optional C — NOT BUILT** |

**Picker:** No picker exists in `js/free-user-filters.js` or `index.html`.

**Verdict:** PARTIAL-BUILD + MISSING-PICKER.
- Cold Environments lessons absent (students picking that option have no content).
- Glacial Landscapes lessons absent (one of the Paper 1 Section C options).
- Food and Water resource management lessons absent (two of three Paper 2 options).
- Even for built options, no picker exists so all students see everything in a single 20-lesson block regardless of their actual option choices.

---

### geography-edexcel-a (1GA0)

**Optional groups in spec:**

1. **Component 1 (Paper 1), Topic 1: Changing Landscapes** — UK Landscapes overview compulsory + **two from three**: 1A Coastal, 1B River, 1C Glaciated. Students answer questions on their two chosen landscapes in the exam.
2. **Component 2 (Paper 2), Topic 6: Resource Management** — Resource Management overview compulsory + **one from two**: 6A Energy OR 6B Water.
3. **Component 3 (Paper 3), Section A: Physical Fieldwork** — students choose **one from two** exam questions: Rivers OR Coasts (teacher selects which fieldwork environment to teach).
4. **Component 3 (Paper 3), Section B: Human Fieldwork** — students choose **one from two** exam questions: Central/Inner Urban Area OR Rural Settlements (teacher selects).

**Built units:**
- Paper 1: The Physical Environment (12 lessons) — flat unit
- Paper 2: The Human Environment (10 lessons) — flat unit
- Paper 3: Fieldwork & UK Challenges (6 lessons) — flat unit
- Geographical Skills (12 lessons)

**Coverage of options in Paper 1 (12 lessons):**

| Topic | Lessons | Notes |
|-------|---------|-------|
| UK Geology overview | L1 | Compulsory |
| Coastal Landscapes | L2–L3 | Optional 1A — included |
| River Landscapes | L4–L5 | Optional 1B — included |
| Glaciated Landscapes | L6 | Optional 1C — included (1 lesson only, others get 2 each) |
| Weather Hazards | L7–L10 | Compulsory |
| Ecosystems | L11–L12 | Compulsory |

All three landscape options appear to be built (though Glacial gets only 1 lesson vs 2 for Coastal and River). No picker exists.

**Coverage of options in Paper 2 (10 lessons):**

| Topic | Lessons | Notes |
|-------|---------|-------|
| Urban / Cities | L1–L4 | Compulsory |
| Development | L5–L7 | Compulsory |
| Resource Management Overview | L8 | Compulsory |
| Energy Resource Management | L9 | Optional 6A — included |
| Water Resource Management | L10 | Optional 6B — included |

Both resource options present. No picker.

**Coverage of Paper 3 fieldwork options (6 lessons):**

| Topic | Lessons | Notes |
|-------|---------|-------|
| Physical Fieldwork (Rivers & Coasts combined) | L1 | Both environments covered in one lesson — no separation |
| Human Fieldwork (Urban & Rural combined) | L2 | Both environments covered in one lesson — no separation |
| Data presentation/analysis | L3 | Generic |
| UK Challenges | L4–L6 | Compulsory |

Physical and human fieldwork lessons each cover both exam options in a single lesson, so there is no content gap but also no filtering possible.

**Picker:** None.

**Verdict:** MISSING-PICKER. All options are nominally built (Glacial slightly thin at 1 lesson). No picker means students cannot select their two landscape choices or their resource management option — they see all content with no guidance on what applies to them.

---

### geography-edexcel-b (1GB0)

**Optional groups in spec:**

Component 2 (Paper 2), Section C exam structure offers **one from two** for physical fieldwork (Coastal change OR River processes) and **one from two** for human fieldwork (Dynamic urban areas OR Changing rural areas). However, the CONTENT students must study is specified without optionality: Topics 4A (Coastal change and conflict) AND 4B (River processes and pressures) are BOTH listed as sub-topics of Topic 4. The fieldwork question choice on exam day is based on which fieldwork they actually did, not a pre-declared topic election. Teachers select one physical and one human fieldwork environment but students study the corresponding content depth — the spec does not say "study one of these."

Component 3 (Paper 3) Section D offers a choice of one from three decisions for a 12-mark essay — this is an unseen, in-exam choice based on pre-release material, not a teachable content option.

**Built units:**
- Global Geographical Issues (10 lessons) — all compulsory
- UK Geographical Issues (10 lessons) — covers both coastal AND river landscapes plus both urban/rural fieldwork contexts
- People and Environment Issues (8 lessons) — all compulsory
- Geographical Skills (12 lessons)

All content built. No student-selectable optional topics exist at the content level.

**Picker:** None needed at content level.

**Verdict:** COMPULSORY. Edexcel B's exam-day question choices are school/teacher decisions about which fieldwork to conduct, not student content elections. No picker required.

---

### geography-ocr (J383)

**Optional groups in spec:** None. OCR Geography A (J383) has three fully compulsory components:
- J383/01: Living in the UK Today — Landscapes of the UK, People of the UK, UK Environmental Challenges (all studied)
- J383/02: The World Around Us — Ecosystems, People of the Planet, Environmental threats (all studied)
- J383/03: Geographical Skills (all studied)

No "choose one from" groups appear anywhere in the content specification.

**Built units:**
- Living in the UK Today (10 lessons)
- The World Around Us (10 lessons)
- Geographical Skills (12 lessons)

**Picker:** Not applicable.

**Verdict:** COMPULSORY. No optional topics in this spec.

---

### geography-eduqas (C111QS)

**Optional groups in spec:**

1. **Component 1, Section B** — students study **one from two**: Theme 3 (Tectonic Landscapes and Hazards) OR Theme 4 (Coastal Hazards and their Management). Exam question choice matches studied theme.
2. **Component 2, Section B** — students study **one from two**: Theme 7 (Social Development Issues) OR Theme 8 (Environmental Challenges). Exam question choice matches studied theme.

**Built units and lesson coverage:**

| Unit | Slug | Lessons | Options covered |
|------|------|---------|----------------|
| Tectonic & Coastal Hazards | tectonic-coastal-hazards | 4 | L1–L2 = Theme 3 (Tectonic); L3–L4 = Theme 4 (Coastal) — both packed into one unit |
| Weather, Climate & Ecosystems | weather-climate-ecosystems | 5 | Core Theme 5 — compulsory |
| Development & Resources | development-resources | 5 | Core Theme 6 — compulsory |
| Rural-Urban Links | rural-urban-links | 5 | Core Theme 2 — compulsory |
| Landscapes & Physical Processes | landscapes-physical-processes | 6 | Core Theme 1 — compulsory |
| Social & Environmental Challenges | social-environmental-challenges | 4 | L1–L2 = Theme 7 (Social Development); L3–L4 = Theme 8 (Environmental Challenges) — both packed into one unit |
| Fieldwork Enquiry | fieldwork-enquiry | 3 | Component 3 — compulsory |
| Geographical Skills | geographical-skills | 12 | Skills — compulsory |

**Both options in each pair are built** within a single combined unit (4 lessons each split 2+2 or 2+2). There is no structural separation between the options at the unit level — both are delivered together.

**Picker:** None.

**Verdict:** MISSING-PICKER. Both options per choice group are built but co-mingled within the same unit. Without a picker, students studying Theme 3 (Tectonic) see Theme 4 (Coastal) lessons too and vice versa. Same problem for Themes 7 and 8. A picker or a lesson-level filter is needed to surface only the relevant option.

---

## Picker design notes (for future implementation)

If a picker is added, it should record choices in localStorage (consistent with the tier/subject preference pattern) and filter lesson lists on the browse page. The minimum viable picker for each slug:

**geography-aqa:**
- Living World: Hot Deserts OR Cold Environments (choose 1)
- Physical Landscapes: Coastal + River / Coastal + Glacial / River + Glacial (choose 2 of 3)
- Resource Management: Food / Water / Energy (choose 1)

**geography-edexcel-a:**
- Landscapes: select two from Coastal / River / Glaciated (choose 2 of 3; default show all 3)
- Resource Management: Energy OR Water (choose 1)

**geography-eduqas:**
- Component 1 option: Tectonic Landscapes and Hazards OR Coastal Hazards and their Management (choose 1)
- Component 2 option: Social Development Issues OR Environmental Challenges (choose 1)

**geography-edexcel-b / geography-ocr:** No picker needed.

The biggest content gap is geography-aqa, which is missing Cold Environments, Glacial Landscapes, Food security, and Water resource lessons entirely.
