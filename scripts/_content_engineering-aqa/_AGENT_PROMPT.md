# Engineering AQA Content Agent Prompt (Phase 3)

You are generating content for **AQA GCSE Engineering (8852)** — written exam paper only (60% of the qualification). NEA design-process work (3.6) is out of scope.

Baseline transfer MEDIUM: most lessons have a sibling subject (Design & Technology AQA, Separate Sciences AQA Physics, Electronics Eduqas) as voice/structural reference but **no specific port_source_path** — generate from spec + adaptation_notes + section_markers. Use the sibling subject's tone as inspiration only.

---

## Files to read first

1. `docs/CONTENT_PROMPT.md` — system prompt, output schema, field rules.
2. `docs/LESSON_TEMPLATE.md` — HTML component reference.
3. `docs/FLASHCARD_RULES.md` — flashcard rules.
4. `scripts/_content_engineering-aqa/_batch_{batch_id}.json` — YOUR batch input.
5. `scripts/_content_business-edexcel/_reference_lesson.json` — structural shape only.

---

## Subject framing — AQA Engineering 8852

### Audience
- **GCSE Engineering (8852)** — proper GCSE (not L1/L2 vocational), but mechanically-minded students. Use technical-school / workshop tone. Concrete examples from automotive, aerospace, civil, manufacturing.
- Lessons cover materials, manufacturing, systems (mechanical/electrical/electronic/structural/pneumatic/hydraulic + programmable), testing, drawing standards.

### Spec quirks
- **Calculations**: density, area, volume, pressure (P=F/A), mechanical advantage (load/effort), gear ratio (driven/driver), pulley calculations, stress (σ=F/A), strain (ε=ΔL/L), Young's modulus (E=σ/ε). Include calculation questions in the relevant lessons (U4 L1, L2 especially).
- **CAD/CAM**: 2D + 3D CAD packages; CAM = computer-aided manufacture (CNC machining, 3D printing as CAM output).
- **Engineering drawing standards**: 3rd angle projection (BS 8888), isometric, oblique, exploded views, hidden detail lines, centre lines, section views, tolerances (±0.1mm typical).
- **Programmable systems**: microcontrollers (Arduino, PIC, BBC micro:bit), input/process/output model, sensors → microcontroller → actuators. Flowchart programming.
- **Smart materials**: shape-memory alloys (nitinol), thermochromic, photochromic, piezoelectric. These appear briefly.
- **Sustainability framework**: 6Rs (Rethink, Refuse, Reduce, Reuse, Repair, Recycle).

### Real-world examples acceptable in content_html
- Boeing 787 (CFRP fuselage)
- F1 cars (carbon fibre monocoque)
- Tesla Gigafactory (additive manufacturing for prototypes)
- HS2 (steel grade), Crossrail (tunnel boring)
- Dyson (cyclonic vacuum design iteration)
- BBC micro:bit / Arduino in school workshops
- BAE Systems, Rolls-Royce (UK engineering employers)

### Marked-question scenarios — fictional only
- 6+ mark questions need ORIGINAL fictional scenarios: e.g. *Fenwick Manufacturing Ltd* (small Sheffield CNC shop), *Aethon Robotics* (Cambridge start-up building agricultural robots), *Marrowbone Engineering* (West Midlands automotive parts supplier), *Daleside Pumps* (Yorkshire hydraulics specialist), *Crane & Hatch* (Birmingham fabrication workshop). Vary across lessons.

---

## Free-tier (mandatory)

- NO `diagram_prompt`, NO `<!-- DIAGRAM -->` placeholder.
- Schema must have ONLY keys listed in CONTENT_PROMPT.md + 3 underscore-prefixed routing keys.

## content_html

- 800-1500 words excluding tags.
- Sequential `data-narration-id` (no gaps).
- ≥2 `<div class="key-fact">` with actionable `data-revision-tip`.
- ≥2 `<div class="collapsible">`.
- ≥3 `<dfn class="term" data-def="...">` inline.
- NO `<h1>` tags.
- HTML entities ALLOWED in content_html / exam_tip_html / conclusion_html.
- **Plain text in `description`, `practice_questions`, `knowledge_checks`, `flashcard_questions`, `glossary_terms`** — unicode quotes/dashes/symbols (×, ÷, μ, σ, ε, Δ, °), NOT HTML entities.

## Question types

Use only types listed in `registered_question_type_names`. AQA Engineering uses GCSE-style mark allocations (1-12 marks typical).

## Mark scheme rubric

- StudyVault format ONLY: Mastering / Secure / Developing / Emerging for 6+ mark questions.
- NEVER use "Level 1/2/3" descriptors.
- For Kohlberg-style "Level" content — N/A in Engineering, you won't hit this.

## Knowledge checks (exactly 5)

- 2 MCQ + 2 fill + 1 match.
- Use `correct: <int>` + `options[]` schema (NOT `answers: [...]`).

## Flashcards (8-15)

- 10-14 typical. ≤15 words target, hard cap 30. One fact per card, no enumerations.
- Watch the single-word-answer trap: questions must start "What is/Who was/When/Name" for one-word answers.

## Glossary

- ≥3 `<dfn class="term">` inline.
- ≥6 entries in `glossary_terms` array.

---

## ABSOLUTE BANS

- **NO spec codes** (8852, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6) in user-facing strings.
- **NO board names** (AQA, Pearson, OCR) in content_html / exam tips / questions / flashcards / glossary.
- **NO paper labels** (Paper 1, P1, Section A).
- **NO Level descriptors in `marks`**.
- **NO** "Nothing worthy of credit" / "Award N marks for identification".
- **NO real-company names** in marked-question case-study stems (real companies OK in content_html for illustration).
- **NO recycled fictional names** within your batch.
- **NO HTML entities in plain-text fields**.

## Output checklist

- [ ] All required schema fields present.
- [ ] All 3 underscore-prefixed routing keys present.
- [ ] No `<h1>`. Sequential `data-narration-id`.
- [ ] ≥2 key-fact, ≥2 collapsible, ≥3 `<dfn>`.
- [ ] Exactly 6 practice_questions, 5 knowledge_checks, 8-15 flashcards.
- [ ] KC uses `correct`+`options[]`.
- [ ] No board names / spec codes anywhere.
- [ ] No HTML entities in plain-text fields.
- [ ] Fresh fictional case-study names per lesson.

## When done

```
LESSON_DONE: number=N slug={slug} words={count} questions=6 kcs=5 flashcards={n}
```

Final:
```
BATCH_DONE: batch_id={batch_id} lessons={count}
```
