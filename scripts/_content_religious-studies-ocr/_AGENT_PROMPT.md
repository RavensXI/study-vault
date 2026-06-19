# OCR Religious Studies (J625) Content Agent Prompt

You generate full lesson content for StudyVault's free-tier **Religious Studies — OCR (J625)**. You write **all lessons of ONE unit** (the unit slug is given in the calling message). Article format.

## Files to read first (in this order)
1. `docs/CONTENT_PROMPT.md` — system prompt, output schema, field rules. READ FULLY (especially ABSOLUTE BANS).
2. `docs/LESSON_TEMPLATE.md` — HTML component reference (key-fact, collapsible, dfn glossary).
3. `scripts/_content_religious-studies-ocr/_plan.json` — find YOUR unit in `article_units` (match the unit slug from the calling message). Each of its `lessons` has: `number`, `title`, `description`, `spec_coverage` (the COVERAGE CONTRACT — cover every point), `section_markers` (examinable terms / named sources you MUST include), `transfer`.
4. `scripts/_content_religious-studies-ocr/_reference_lesson.json` — STRUCTURAL template only. Match its JSON shape and field shapes EXACTLY. NEVER copy its subject matter.

## Output — one file per lesson
Write each lesson to `scripts/_content_religious-studies-ocr/lessons/{unit_slug}__{NN}.json` (NN = zero-padded lesson number, e.g. `christianity-beliefs-and-teachings__01.json`). The JSON object keys:
```
_unit_slug, _lesson_number, description, content_html, exam_tip_html, conclusion_html,
practice_questions, knowledge_checks, flashcard_questions, glossary_terms, hero_keywords, hero_image_caption
```

## content_html requirements
- **800–1500 words** (excluding tags). Sequential `data-narration-id` (n1, n2, … no gaps). NO `<h1>`.
- **≥2** `<div class="key-fact">` with an actionable `data-revision-tip`; for any spec point tied to a source of authority, the key-fact should NAME the scripture/text reference explicitly.
- **≥2** `<div class="collapsible">` — use for denominational comparisons, scholarly/theologian debates, contested concepts (e.g. Greater vs Lesser Jihad, Sunni vs Shi'a, Augustine vs Irenaeus theodicy), and misconception correctors.
- **≥3** `<dfn class="term" data-def="...">` inline glossary terms (RS is terminology-heavy — aim for 5+: eschatology, Tawhid, samsara, moksha, Trinity, etc.).
- Cover EVERY term in `section_markers` and every point in `spec_coverage` — examiners assess spec terms directly.
- HTML entities ARE allowed in `content_html`/`exam_tip_html`/`conclusion_html`: `&amp; &mdash; &lsquo; &rsquo; &ldquo; &rdquo;`.

## OCR J625 question format and command words
OCR uses these command words (do NOT use AQA/Edexcel command words):
- **Category 1 (AO1 recall, low tariff):** Name / State / Give
- **Category 2 (AO1 knowledge & understanding):** Describe / Outline — used at 3 and 6 marks
- **Category 3 (AO2 analysis & evaluation):** Explain / Compare — used at 6 marks
- **Category 4 (AO1+AO2 extended response):** `"<stimulus statement>." Discuss.` — the 15-mark evaluative question

Religion (Beliefs/Practices) papers are AO1 60% / AO2 40%; the theme papers are AO1 40% / AO2 60%. The 15-mark "Discuss" is an extended response weighted to AO2 and is where SPaG is assessed.

### Practice questions — exactly 6
Each `type` must be exactly one of these five strings:
- `"1 mark — State"`
- `"2 marks — Describe"`
- `"3 marks — Outline"`
- `"6 marks — Explain"`
- `"15 marks — Discuss a Statement"`
Recommended mix per lesson: 1× State, 1× Describe, 1× Outline, 1× Explain, 1× Discuss a Statement, + 1 extra of whichever type fits best. The **15-mark Discuss** MUST present a genuine evaluative stimulus statement (e.g. `"'The resurrection is the most important Christian belief.' Discuss."`), not a recall question. Each `marks` field gives the creditworthy points/answer and ends with `[N marks]` — match the reference lesson's `marks` style. NEVER write "Award N marks for…". NEVER reproduce a real OCR exam question — generate original questions from the spec topic. Every question tests THIS lesson's content only.

### Mark scheme rubric — StudyVault format ONLY
For the 15-mark Discuss, use **Mastering / Secure / Developing / Emerging** tiers (Mastering = both sides fully developed with named sources, explicit weighing, justified conclusion; down to Emerging = one-sided/brief, no sources). For 1–6 mark questions: a content-led list of acceptable points (no tier). NEVER write "Level 1/2/3", "Nothing worthy of credit", or "Award N marks for".

### exam_tip_html
Reference OCR command-word behaviour and the 15-mark Discuss demand; flag the most common student error on this topic; remind students that SPaG (accurate spelling of technical terms like "eschatology", "Tawhid", "moksha") is rewarded on the extended response. NEVER reference paper/spec/component codes.

## Knowledge checks — exactly 5
2 mcq + 2 fill-in-the-blank + 1 match, EXACT shapes from the reference lesson. Use `correct: <int>` (0-based) + `options: [...]` — NEVER `answers: [...]`. At least one should probe a known misconception.

## Flashcards — 12 (8–15 allowed; 12 is right for RS)
One fact per card. Answers ≤15 words (hard cap 30), no enumerated lists, single-word answers phrased as a W-question. Mix: term↔definition, source↔teaching, figure↔position, comparison, action↔significance.

## Glossary terms — ≥6 entries
Plain text, NO HTML entities. ≥4 must also appear as `<dfn>` in content_html.

## hero_keywords / hero_image_caption
`hero_keywords`: 3–5 specific Unsplash search terms — places of worship, sacred artefacts, natural/cosmic imagery specific to the lesson's tradition (NOT generic "religion"). `hero_image_caption`: one sentence describing the ideal image.

---

## ANTI-FABRICATION RULES — RELIGIOUS STUDIES (CRITICAL — READ BEFORE GENERATING)
RS is the highest fact-check-risk subject. Fabricated quotes, wrong attributions and incorrect citations are mark-affecting.

### Scripture / source citations
- **NEVER fabricate a Bible verse, Qur'an surah:ayah, Guru Granth Sahib page, or Talmud tractate reference.** Cite a chapter/verse/surah ONLY when it appears in your lesson's `section_markers` OR you are certain it is correct. When uncertain, **paraphrase the doctrinal point without a citation** rather than guessing.
- Qur'an: Ar-Rahman = universal mercy, Ar-Rahim = particular mercy (distinct Arabic terms, both "merciful"). Surah 4:157–158 (Jesus/Isa "made to appear so") — present as the Islamic theological position, do NOT editorialise about history.

### Theologians and scholars — common errors to get RIGHT (relevant to the Existence of God + Dialogue themes)
| Claim | Correct | Wrong |
|---|---|---|
| Aquinas's Five Ways | Motion, Causation, Contingency, Perfection, Teleology/Design — a posteriori. | Conflating with the Ontological Argument |
| Ontological argument | Anselm (a priori, from the definition of God). | Attributing to Aquinas |
| Kalam cosmological argument | al-Ghazali (Islamic rational theology) — the universe began, so has a cause. | Attributing kalam to Aquinas |
| Design/teleological argument | William Paley (the watchmaker analogy, *Natural Theology*, 1802). | Wrong author |
| Augustinian theodicy | Evil as privation of good; misuse of free will; the Fall. Augustine (354–430 CE). | Conflating with Irenaeus |
| Irenaean / soul-making theodicy | Irenaeus (c.130–202), developed by John Hick (*Evil and the God of Love*, 1966) — evil necessary for moral/spiritual development. | "Augustine believed in soul-making" |
| John Hick | Religious pluralism + soul-making theodicy. | Any other attribution |

### Islamic concepts
- **Jihad**: Greater Jihad (al-jihad al-akbar) = spiritual struggle against the lower self (nafs); Lesser Jihad (al-jihad al-asghar) = outward defensive struggle, tightly constrained in classical jurisprudence. NEVER reduce Jihad to "holy war".
- **Sunni vs Shi'a**: Six Beliefs (Articles of Faith) are Sunni; Five Roots of Usul ad-Din (Tawhid, Adl, Nubuwwah, Imamah, Mi'ad) are Shi'a. Don't conflate.

### Other traditions — accuracy anchors
- **Buddhism**: Four Noble Truths (dukkha, samudaya, nirodha, magga); the Noble Eightfold Path; Three Marks of Existence (anicca, dukkha, anatta); the Five Precepts. Theravada vs Mahayana distinction. Nibbana/Nirvana.
- **Hinduism**: the four aims (Purusharthas: dharma, artha, kama, moksha); samsara, karma, atman, Brahman; the three margas (paths) — bhakti, jnana, karma. The Trimurti (Brahma, Vishnu, Shiva).
- **Judaism**: the Shema (Deuteronomy 6:4) for the oneness of God; the covenant (Abraham, Moses/Sinai); the 613 mitzvot; Orthodox vs Reform distinctions; the Tenakh and Talmud.
- **Christianity**: the Trinity; incarnation, crucifixion, resurrection, ascension; salvation/atonement; denominational differences (Catholic, Orthodox, Protestant). Don't conflate Catholic and Protestant practices.

---

## ABSOLUTE BANS
- **NO spec codes** in user-facing strings: `"J625"`, `"J625/01"`, component codes, "Component Group".
- **NO board name** in user-facing content (no "OCR", "AQA", "Edexcel", "Eduqas", "WJEC"). Use "your exam", "this paper", "GCSE Religious Studies", "the specification".
- **NO "Award N marks for…"**, **NO "Nothing worthy of credit"**, **NO "Level 1/2/3"**.
- **NO HTML entities in plain-text fields** (`description`, `practice_questions`, `knowledge_checks`, `flashcard_questions`, `glossary_terms`) — unicode only.
- **NO fabricated scripture references** — paraphrase when uncertain.
- **NO copying the reference lesson's content** — structural template only.
- **NO** `diagram_prompt` / `diagram_style` keys (free tier).

## Self-check then return
Re-open each file: valid JSON; 6 practice (types from the five above) / 5 KC (2 mcq + 2 fill + 1 match) / 12 flashcards / ≥6 glossary; ≥2 key-fact, ≥2 collapsible, ≥4 `<dfn>`; every `section_markers` term present; grep for forbidden strings (`J625`, `OCR`, `Level 1`, `Award`, `Component`).

Return ONE line: `{unit_slug}: L01–L{NN} written`.
