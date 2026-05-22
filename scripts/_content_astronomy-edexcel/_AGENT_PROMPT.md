# Astronomy Edexcel Content Agent Prompt (Phase 3)

You are generating content for **Edexcel GCSE Astronomy (1AS0)**. All-article format, two units (Naked-eye Astronomy + Telescopic Astronomy).

This subject is **essentially all fresh content from spec**. The planner nominally flagged some lessons as having Separate Sciences Physics overlap, but Astronomy goes into far more depth on stellar evolution / cosmology / observational techniques than the single Physics lesson on each topic — so port_source paths are NOT provided and you generate everything from spec + adaptation_notes + section_markers.

---

## Files to read first

1. `docs/CONTENT_PROMPT.md` — system prompt, output schema, field rules.
2. `docs/LESSON_TEMPLATE.md` — HTML component reference.
3. `docs/FLASHCARD_RULES.md` — flashcard rules.
4. `scripts/_content_astronomy-edexcel/_batch_{batch_id}.json` — YOUR batch input.
5. `scripts/_content_business-edexcel/_reference_lesson.json` — structural shape only.

---

## Subject framing — Edexcel Astronomy 1AS0

### Audience
- Proper GCSE (not vocational). Science-curious students who chose this as an option subject. Use precise scientific terminology with explanations. Awe + rigour balance.
- Real Edexcel Astronomy students will use observational logs as part of the qualification, so reference back-garden astronomy practicalities (light pollution, Bortle scale, smartphone star-trackers, naked-eye limiting magnitude).

### Topic structure
- **Unit 1 Naked-eye Astronomy** (12 lessons): celestial sphere, equatorial vs altazimuth coordinates, diurnal motion, sidereal vs synodic, seasons + ecliptic, lunar phases + eclipses, planets + zodiac, observing equipment basics, fieldwork enquiry skills
- **Unit 2 Telescopic Astronomy** (14 lessons): telescope optics (refractors, reflectors, magnification M = fo/fe), CCDs/imaging, stellar parallax (d = 1/p), magnitude (m - M = 5log(d) - 5), HR diagram + stellar evolution, exoplanets + habitable zones, cosmology (Hubble v = H0d, redshift Δλ/λ = v/c, CMB, Big Bang)

### Equations you'll reference (KaTeX-friendly)
- Distance from parallax: `\(d = \frac{1}{p}\)` (p in arcseconds, d in parsecs)
- Distance modulus: `\(m - M = 5\log_{10}(d) - 5\)`
- Hubble's law: `\(v = H_0 d\)`
- Kepler's third law: `\(T^2 / r^3 = \text{constant}\)`
- Telescope magnification: `\(M = f_o / f_e\)`
- Redshift: `\(\Delta\lambda / \lambda = v / c\)`

Use KaTeX inline (`\(...\)`) or display (`$$...$$`) as appropriate. KaTeX is loaded on lesson.html.

### Spec-specific framing
- **Naked-eye limiting magnitude**: mag 6 in dark sky; mag 4 in suburban; mag 2 in city
- **Hubble constant**: ~70 km/s/Mpc (Edexcel uses this value; flag the ongoing Planck vs Cepheid tension only if it serves the lesson)
- **Age of universe**: 13.8 Gyr
- **Stellar lifecycle**: nebula → protostar → main sequence (H fusion) → red giant/supergiant → white dwarf / neutron star / black hole (mass-dependent)
- **HR diagram axes**: luminosity (y) vs temperature/spectral class (x). Temperature reversed (high temp left, low temp right per convention).
- **Edexcel 2023 + 2024 PEFs**: students confuse sidereal vs synodic; misattribute the diurnal/annual motion; eclipse geometry mistakes; chromatic aberration vs spherical aberration confusion; tides wrongly attributed to a single Moon pull (it's the differential gravitational gradient).

### Marked-question scenarios — fictional only
- 6+ mark questions need original fictional astronomy contexts: e.g. *Brackenfell Observing Society* (Cumbria amateur club), *Dr Halima Yousef* (planetarium educator in Birmingham), *Holt Astronomy Group* (Norfolk dark-sky enthusiasts), *Caerwyn Observatory* (Welsh teaching observatory), *Marina Vassilakis* (sixth-form astronomy enthusiast in Glasgow). Vary across lessons.

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
- KaTeX-friendly equations (inline `\(...\)` or display `$$...$$`).
- **Plain text in `description`, `practice_questions`, `knowledge_checks`, `flashcard_questions`, `glossary_terms`** — unicode quotes/dashes/symbols (×, ÷, °, λ, Δ), NOT HTML entities.

## Question types

Use only types listed in `registered_question_type_names`.

## Knowledge checks (exactly 5)

- 2 MCQ + 2 fill + 1 match.
- Use `correct: <int>` + `options[]` schema (NOT `answers: [...]`).

## Flashcards (8-15)

- 10-14 typical. ≤15 words target, hard cap 30. One fact per card, no enumerations.

## Glossary

- ≥3 `<dfn class="term">` inline.
- ≥6 entries in `glossary_terms` array.

---

## ABSOLUTE BANS

- **NO spec codes** (1AS0) in user-facing strings.
- **NO board names** (Edexcel, Pearson) in content_html / exam tips / questions / flashcards.
- **NO paper codes** (1AS0/01, 1AS0/02).
- **NO Level descriptors in `marks`**.
- **NO** "Nothing worthy of credit" / "Award N marks for identification".
- **NO recycled fictional names** within your batch.
- **NO HTML entities in plain-text fields**.

## Output checklist

- [ ] All required schema fields present.
- [ ] All 3 underscore-prefixed routing keys.
- [ ] No `<h1>`. Sequential `data-narration-id`.
- [ ] ≥2 key-fact, ≥2 collapsible, ≥3 `<dfn>`.
- [ ] Exactly 6 practice_questions, 5 knowledge_checks, 8-15 flashcards.
- [ ] KC uses `correct`+`options[]`.
- [ ] No board names / spec codes.
- [ ] No HTML entities in plain-text fields.
- [ ] Fresh fictional names per lesson.

## When done

```
LESSON_DONE: number=N slug={slug} words={count} questions=6 kcs=5 flashcards={n}
```

Final:
```
BATCH_DONE: batch_id={batch_id} lessons={count}
```
