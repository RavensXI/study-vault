# Geography Build Plan — AQA 8035

Reference file for the Geography section build. Survives context compaction.
Read this file at the start of each session to know where things stand.

## Overview
- **Subject:** AQA GCSE Geography 8035
- **Structure:** 2 papers, 20 lessons each, 40 total
- **No Paper 3** (fieldwork/pre-release — too school-specific)
- **Colour themes:** Paper 1 = `#4f46e5` (indigo) `unit-geography-1`, Paper 2 = `#dc2626` (red) `unit-geography-2`
- **Source material:** Extracted PPT/doc text in `Spec and Materials/Geography/_extracted_text/`
- **Template:** Follow `business/theme-1/lesson-01.html` as canonical pattern

## Folder Structure
```
geography/
├── index.html              ← Landing page (DONE)
├── BUILD_PLAN.md           ← This file
├── paper-1/
│   ├── index.html          ← Unit index (DONE)
│   └── lesson-01..20.html  ← 20 lessons
├── paper-2/
│   ├── index.html          ← Unit index (DONE)
│   └── lesson-01..20.html  ← 20 lessons
├── exam-technique/
│   ├── index.html          ← Hub page
│   └── [guide pages]       ← One per question type
└── revision-technique/
    ├── index.html          ← Hub page
    └── [guide pages]       ← ~7-8 guides
```

## Build Progress

### Infrastructure
- [x] CSS themes (unit-geography-1, unit-geography-2, dark mode variants)
- [x] Folder structure created
- [x] geography/index.html (landing page)
- [x] geography/paper-1/index.html (unit index)
- [x] geography/paper-2/index.html (unit index)
- [x] Update platform SPA (root index.html) — make Geography active with URL
- [ ] Hero images for landing page cards (subject-geography-1.jpg, subject-geography-2.jpg)

### Paper 1: Living with the Physical Environment (20 lessons)

**Section A: The Challenge of Natural Hazards (8 lessons)**

| # | Title | Source Folders | Status |
|---|---|---|---|
| 01 | Natural Hazards, Plate Tectonics & Distribution | Tectonics L1–L3 | DONE |
| 02 | Plate Boundaries & Living Near Hazards | Tectonics L4–L5 | DONE |
| 03 | Earthquake Case Studies: Haiti & Christchurch | Tectonics L6–L9 | DONE |
| 04 | Managing Tectonic Hazards: The Three Ps | Tectonics L10 | DONE |
| 05 | Global Atmospheric Circulation & Tropical Storms | Weather L1–L4 | DONE |
| 06 | Typhoon Haiyan & Managing Tropical Storms | Weather L5–L7 | DONE |
| 07 | UK Weather Hazards: Cumbria Floods | Weather L8–L10 | DONE |
| 08 | Climate Change: Causes, Effects & Responses | Weather L11–L15 | DONE |

**Section B: The Living World (5 lessons)**

| # | Title | Source Folders | Status |
|---|---|---|---|
| 09 | Ecosystems & UK Small-Scale Ecosystems | TRF L1–L2 | DONE |
| 10 | Tropical Rainforests: Characteristics & Adaptations | TRF L3–L5 | DONE |
| 11 | Amazon Deforestation & Sustainable Management | TRF L6–L10 | DONE |
| 12 | Hot Deserts: Characteristics & Adaptations | Hot Deserts L1–L4 | DONE |
| 13 | The Sahara, Desertification & Management | Hot Deserts L5–L9 | DONE |

**Section C: Physical Landscapes in the UK (7 lessons)**

| # | Title | Source Folders | Status |
|---|---|---|---|
| 14 | Coastal Processes: Weathering, Waves & Transport | Coasts L1–L3 | DONE |
| 15 | Coastal Landforms: Erosion & Deposition | Coasts L4–L8 | DONE |
| 16 | Coastal Management & Lyme Regis Case Study | Coasts L9–L10 | DONE |
| 17 | River Processes & Profiles | Rivers L1–L3 | DONE |
| 18 | River Landforms: Waterfalls to Estuaries | Rivers L4–L8 | DONE |
| 19 | Flooding: Causes & Hydrographs | Rivers L9–L10 | DONE |
| 20 | Flood Management & the River Tees | Rivers L11–L12 | DONE |

### Paper 2: Challenges in the Human Environment (20 lessons)

**Section A: Urban Issues & Challenges (8 lessons)**

| # | Title | Source Folders | Status |
|---|---|---|---|
| 01 | Global Urbanisation & Megacities | Rio L1–L2 | DONE |
| 02 | Rio de Janeiro: Importance & Opportunities | Rio L3–L4 | DONE |
| 03 | Rio: Social, Economic & Environmental Challenges | Rio L5–L7 | DONE |
| 04 | Rio: Improvements & Sustainable Urban Living | Rio L8–L10 | DONE |
| 05 | UK Urbanisation & Liverpool's Importance | Liverpool L1–L2 | DONE |
| 06 | Liverpool: Migration, Decline & Deprivation | Liverpool L3–L5 | DONE |
| 07 | Liverpool: Opportunities & Urban Greening | Liverpool L6–L7 | DONE |
| 08 | Liverpool: Regeneration, Transport & Sustainability | Liverpool L8–L12 | DONE |

**Section B: The Changing Economic World (9 lessons)**

| # | Title | Source Folders | Status |
|---|---|---|---|
| 09 | Measuring Development: Indicators & the DTM | CEW L1–L4 | DONE |
| 10 | Causes of Uneven Development | CEW L5–L7 | DONE |
| 11 | Reducing the Development Gap & Tourism in Kenya | CEW L8–L11 | DONE |
| 12 | India: Location, Importance & Population | India L1–L2 | DONE |
| 13 | India: Employment, TNCs & Trade | India L3–L5 | DONE |
| 14 | India: Aid, Environment & Economic Growth | India L6–L8 | DONE |
| 15 | Globalisation & the Changing UK Economy | UK Economy L1–L2 | DONE |
| 16 | Post-Industrial UK: Business Parks, Environment & Rural Change | UK Economy L3–L5 | DONE |
| 17 | The North-South Divide, Transport & the UK in the Wider World | UK Economy L6–L8 | DONE |

**Section C: The Challenge of Resource Management (3 lessons)**

| # | Title | Source Folders | Status |
|---|---|---|---|
| 18 | Resource Management & Energy Supply | Energy L1–L2 | DONE |
| 19 | Energy Impacts & Extraction: Fracking | Energy L3–L4 | DONE |
| 20 | Sustainable Energy & the Nepal Micro-Hydro Case Study | Energy L5–L7 | DONE |

### Exam Technique (DONE)
- Hub page (index.html) + 6 guide pages
- define-state.html (1 mark), state-outline.html (2 marks), explain-describe.html (4 marks)
- explain-examples.html (6 marks), discuss-evaluate.html (9+3 SPaG), data-skills.html (1-4 marks)

### Revision Technique (DONE)
- Hub page (index.html) + 8 guide pages
- retrieval-practice.html, spaced-repetition.html, dual-coding.html, knowledge-organisers.html
- case-study-cards.html, sketch-maps.html (geography-specific)
- elaborative-interrogation.html, timed-exam-practice.html

## Source Material Locations

Extracted text files (one .txt per source PPT/doc):
```
Spec and Materials/Geography/_extracted_text/
├── Paper 1 Question 1 Tectonics/          ← L1-L10 + assessment + revision
├── Paper 1 Question 1 Weather and Climate/ ← L1-L15 + assessment + revision
├── Paper 1 Question 2 TRF/                ← L1-L10 + assessment + revision
├── Paper 1 Question 2 Hot deserts/         ← L1-L9 + assessment + revision
├── Paper 1 Question 3 Coasts/             ← L1-L10 + recap sheets
├── Paper 1 Question 4 Rivers/             ← L1-L12 + recap sheets
├── Paper 2 Question 1 Liverpool/          ← L1-L12 + revision
├── Paper 2 Question 1 Rio/               ← L1-L10 + revision
├── Paper 2 Question 2 Changing economic world/ ← L1-L11 + assessment
├── Paper 2 Question 2 India/              ← L1-L8 + revision
├── Paper 2 Question 2 UK economy/         ← L1-L8 + assessment + revision
└── Paper 2 Question 6 Energy/             ← L1-L7 + revision
```

## AQA Geography Question Types (for practice questions)

Each lesson gets 6 practice questions. AQA Geography uses:
- **1-mark**: Multiple choice or define/state
- **2-mark**: State two... / Outline one...
- **4-mark**: Explain two... / Describe...
- **6-mark**: Explain... (with examples/case study detail)
- **9-mark** (+3 SPaG): Discuss... / To what extent... / Evaluate... / Assess...
- Some 3-mark questions on graphs/maps/data interpretation

Standard mix per lesson: 1x 1-mark, 1x 2-mark, 1x 4-mark, 1x 6-mark, 1x 9-mark, 1x skills/data (varies)

## Knowledge Check Format
5 per lesson: 2 MCQ + 2 fill-in-the-blank + 1 match-up (same as History/Business)

## Lesson HTML Structure
Follow canonical template from business/theme-1/lesson-01.html:
- body class: `unit-geography-1` or `unit-geography-2`
- data-unit: `geography-paper-1` or `geography-paper-2`
- data-lesson: `lesson-NN`
- Paths: `../../css/style.css`, `../../js/main.js`
- Header brand links to `../index.html`
- Nav: Home, Unit Overview, Exam Technique, Revision Techniques, Next/Prev Lesson
- All content elements get `data-narration-id="n1"`, `n2`, etc.
- Glossary terms: `<dfn class="term" data-def="...">term</dfn>`
- Empty narration manifest: `window.narrationManifest = [];`
- Practice questions in `window.practiceQuestions`
- Knowledge check in `window.knowledgeCheck`

## Key Decisions
- No hero images initially (would need Wikimedia/stock sourcing)
- No diagrams initially (would need matplotlib scripts or Gemini API)
- No video embeds initially (no known Geography YouTube channel mapped)
- Related Media sidebar: link to InternetGeography, Seneca, BBC Bitesize, relevant docs/podcasts
- Practice questions use AQA Geography mark schemes and command words
