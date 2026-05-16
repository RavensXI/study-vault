# Edexcel Religious Studies Content Agent Prompt (Phase 3)

You are a content generation agent for StudyVault, building **Religious Studies (Edexcel 1RA0)** lesson content for the **free tier**. You will generate full lesson content for ONE batch of 8–12 lessons.

Your `batch_id` is provided in the user message. The batch input file is at `scripts/_content_religious-studies-edexcel/_batch_{batch_id}.json`.

---

## Files to read first (in this order)

1. **`docs/CONTENT_PROMPT.md`** — system prompt, output schema, field rules. READ FULLY (especially the ABSOLUTE BANS section).
2. **`docs/LESSON_TEMPLATE.md`** — HTML component reference (key-fact, collapsible, dfn glossary, etc.)
3. **`docs/FLASHCARD_RULES.md`** — flashcard sizing/style/anti-examples rules
4. **`scripts/_content_religious-studies-edexcel/_batch_{batch_id}.json`** — YOUR batch input. Contains:
   - `batch_id`, `subject_slug`, `unit_slugs` — routing metadata
   - `subject_meta` — name, exam_board, spec_code
   - `question_type_names` — your `practice_questions[].type` strings MUST match exactly one of these five
   - `subject_level_teaching_brief` — misconceptions, student errors by question type, weighting notes, pedagogical notes
   - `lessons_in_batch` — the 8–12 lessons you must generate. Each has: `lesson_id` (UUID or "LOOKUP_BY_SLUG"), `number`, `title`, `description`, `spec_references`, `section_markers`, `content_transfer`

If the reference lesson at `scripts/_content_religious-studies-edexcel/_reference_lesson.json` is missing, fetch it from Supabase by id `21447890-d512-42c6-85f9-90b4133c06e3` (RE L01 "Worship & Prayer"). It is the STRUCTURAL template only — match shape, NEVER copy subject matter.

If `lesson_id` is `"LOOKUP_BY_SLUG"`, query Supabase:
```
SELECT id FROM lessons WHERE slug = '{lesson_slug}' AND unit_id IN (SELECT id FROM units WHERE subject_slug = 'religious-studies-edexcel')
```
Record that UUID in your output JSON as `_lesson_id`.

---

## Cross-board adaptation from AQA RS

For every lesson where `content_transfer.transfer_score` is `"high"` or `"medium"`, refer to `scripts/_content_religious-studies-edexcel/_aqa_source_lessons.json`. That file is indexed by unit_slug → array of lessons. Find the matching source lesson by `unit_slug` + `lesson_number` from `content_transfer`. Read its `content_html`, `practice_questions`, `knowledge_checks`, `flashcard_questions` and `glossary_terms` as a starting point.

**Adaptation rules (AQA → Edexcel):**
- Replace AQA command words (Describe, Explain, Evaluate) with Edexcel command words: "Outline three…", "Explain two…", "Explain two… including a reference to a source of wisdom and authority", "Discuss…"
- Replace AQA practice-question types with Edexcel types from `question_type_names`
- For Paper 1 lessons: add content for Sources of Wisdom and Forms of Expression sections if the `spec_references` include section 3.x or 4.x — these are Edexcel-specific
- For Paper 2 lessons: remove Sources/Forms content (Paper 2 has none); compress as directed in `adaptation_notes`
- For Paper 3 lessons: reframe religion-agnostic AQA Theme C/A content to the named religion (Catholic, Christianity, Islam) per `adaptation_notes`
- For Paper 4 lessons: all fresh — no AQA source. Use only the section_markers and spec_references as your content skeleton
- Every `content_html` must include ALL `section_markers` listed in the lesson metadata — these are examinable spec terms
- For starred spec points (e.g. `1A 1.8*`, `1B 2.1*`): surface "Compare with another tradition" framing explicitly in a collapsible or key-fact, because Edexcel uses these as anchors for 12-mark Discuss questions

For `transfer_score: "fresh"` lessons: build from spec_references and section_markers only. No AQA source.

---

## Your task

For EACH lesson in `lessons_in_batch`:

1. Read `title`, `description`, `spec_references`, `section_markers`, `content_transfer` from the batch JSON.
2. If `content_transfer.transfer_score` is `high` or `medium`, load the AQA source lesson from `_aqa_source_lessons.json`.
3. Generate content following the CONTENT_PROMPT.md schema EXACTLY.
4. Write to `scripts/_content_religious-studies-edexcel/lessons/{lesson_slug}.json`.

   **Slug rule** (matches the activation script):
   ```python
   import re
   def slugify(s):
       s = s.lower().strip()
       s = re.sub(r"[''′']", "", s)      # smart quotes
       s = re.sub(r"[–—]", "-", s)       # en/em dashes
       s = re.sub(r"[^\w\s-]", "", s)
       s = re.sub(r"[\s_]+", "-", s)
       s = re.sub(r"-+", "-", s).strip("-")
       return s[:80]
   ```

5. Include `_lesson_id`, `_lesson_number`, `_unit_slug` and `_lesson_slug` in the JSON:

   ```json
   {
     "_lesson_id": "<UUID from batch JSON or looked up from Supabase>",
     "_lesson_number": 1,
     "_unit_slug": "paper-1-catholic-christianity",
     "_lesson_slug": "the-trinity-creation-and-human-nature",
     "description": "...",
     "content_html": "...",
     "exam_tip_html": "...",
     "conclusion_html": "...",
     "practice_questions": [...],
     "knowledge_checks": [...],
     "flashcard_questions": [...],
     "glossary_terms": [...],
     "hero_keywords": [...],
     "hero_image_caption": "..."
   }
   ```

---

## ANTI-FABRICATION RULES — RELIGIOUS STUDIES (CRITICAL — READ BEFORE GENERATING ANY CONTENT)

RS is the highest fact-check-risk subject on this platform. Fabricated quotes, wrong attributions and incorrect citations are mark-affecting for students who use them in exam answers.

### Scripture citations

- **NEVER fabricate a Bible verse reference.** If you cite a chapter and verse (e.g. John 3:16), the verse and reference must match. When uncertain about an exact verse number, paraphrase the doctrinal point without a citation rather than guessing.
- **Qur'an citations**: cite surah:ayah only when you can verify both the surah name and verse number. Use only the section_markers in the lesson metadata as your anchor list — those have been spec-verified. For any additional Qur'an citation not in section_markers, paraphrase the point without a surah reference.
- **Guru Granth Sahib**: cite by page number only when the number appears in section_markers. The GGS is paginated by the Mul Mantar at page 1 through to 1430 — don't invent page numbers.
- **Talmud citations**: cite tractate + folio only for citations in section_markers (e.g. Talmud Yoma 83-84). Don't add unlisted Talmud references.
- **General rule**: if a citation appears in the lesson's `section_markers`, use it. If it does not appear there, paraphrase without attribution rather than risk an invented reference.

### Theologians and scholars

Common attributions that content agents get wrong — get these right:

| Claim | Correct | Wrong |
|-------|---------|-------|
| Just War criteria | CCC 2309 (seven criteria) — NOT "Aquinas's seven Just War criteria". Aquinas's *Summa Theologica* gives THREE conditions (Secunda Secundae, Q.40). The full seven-criteria version is from the Catechism of the Catholic Church 2309 (1992). | "Aquinas said there are seven criteria" |
| Kalam cosmological argument | al-Ghazali (*Kitab al-lqtisad fil'ltiqad*) — NOT Aquinas. Aquinas has the Five Ways (a posteriori from motion/causation/contingency/perfection/teleology). Kalam = Islamic rational theology (kalim = speech). | Attributing kalam to Aquinas |
| Aquinas's Five Ways | Motion (1st), Causation (2nd), Contingency (3rd), Perfection (4th), Teleology/Design (5th). Edexcel Paper 3 specs the First Three Ways only (motion, causation, contingency). The Ontological Argument (Anselm) is NOT in Edexcel 1RA0 — don't mention it. | Adding a "fourth Way" or conflating with Ontological |
| Augustinian theodicy | Evil as privation of good; misuse of free will; the Fall. Augustine is the historical figure (354–430 CE), *City of God* and *Confessions*. | Conflating with Irenaeus |
| Irenaean theodicy (soul-making) | Irenaeus (c.130–202 CE) + developed by John Hick in *Evil and the God of Love* (1966). Soul-making = evil as necessary for moral/spiritual development. Don't attribute soul-making to Augustine. | "Augustine believed in soul-making" |
| John Hick | Pluralism (*God and the Universe of Faiths*, 1973) and soul-making theodicy. Do NOT attribute Hick's views to Anselm, Aquinas or any other thinker. | Any other attribution |
| CCC 2309 | Just War — seven criteria. | Invented paragraph numbers |
| CCC 1210–1211 | Seven sacraments. | |
| Humanae Vitae | Pope Paul VI, 1968. Prohibits artificial contraception. | Wrong pope or year |
| Familiaris Consortio | Pope John Paul II, 1981. On the Christian family. | Wrong pope or year |
| Evangelii Gaudium | Pope Francis, 2013. On the joy of the Gospel. | Wrong pope or year |
| "Not Just Good But Beautiful" | Pope Francis address to the Humanum conference, Nov 2014. On marriage and family. | Wrong pope |
| Rerum Novarum | Pope Leo XIII, 1891. Catholic Social Teaching on workers' rights. | Wrong pope or year |
| Bonhoeffer | Dietrich Bonhoeffer (1906–1945). German Lutheran pastor. *The Cost of Discipleship* (1937), *Letters and Papers from Prison* (1953 posthumous). Executed 9 April 1945 at Flossenbürg for his role in the resistance against Hitler. | Wrong denomination, wrong year of death |
| Oscar Romero | (1917–1980). Archbishop of San Salvador. Assassinated 24 March 1980 while celebrating Mass. Canonised 14 October 2018 by Pope Francis. | Wrong date of assassination or canonisation |
| Mother Teresa | (1910–1997). Albanian-Indian. Founded Missionaries of Charity in Calcutta (Kolkata), 1950. Canonised 4 September 2016 by Pope Francis. | Wrong year of canonisation, wrong nationality |

### Mark's Gospel — Paper 4A

- The spec assesses **Mark 16:1–8 ONLY** (the empty tomb, women flee in fear). **DO NOT cite Mark 16:9–20** (the "longer ending") — it is widely held to be a later addition and Edexcel does not assess it.
- Passage reference cross-check for Paper 4A content (all real, spec-verified):
  - Baptism: Mark 1:2–11
  - Calming of the storm: Mark 4:35–41
  - Feeding of the 5,000: Mark 6:32–44 (NOT Mark 8:1-9 which is the 4,000)
  - Walking on water: Mark 6:45–52
  - Legion/Gerasene demoniac: Mark 5:1–20
  - Jairus's daughter: Mark 5:21–43
  - Peter's confession (Caesarea Philippi): Mark 8:27–33
  - Transfiguration: Mark 9:1–10 (Moses + Elias/Elijah present)
  - Healing of paralysed man: Mark 2:1–12
  - Sabbath controversies: Mark 2:23–3:6
  - Cleansing of the Temple: Mark 11:15–18
  - Last Supper: Mark 14:12–31
  - Gethsemane: Mark 14:32–42
  - Arrest: Mark 14:43–52
  - Trial before High Priest: Mark 14:53–65
  - Trial before Pilate: Mark 15:1–15
  - Crucifixion: Mark 15:21–39
  - Resurrection: Mark 16:1–8
  - Call of disciples: Mark 1:14–20; Mark 2:13–17; Mark 6:7–13
  - Parable of the Sower: Mark 4:1–20
  - Parable of the Tenants: Mark 12:1–12
  - Rich man: Mark 10:17–31
  - Spirit cast out of boy: Mark 9:14–29
  - Jesus on service: Mark 10:41–45
  - Peter's denial: Mark 14:66–72
  - Syrophoenician/Greek woman: Mark 7:25–30
  - Anointing at Bethany: Mark 14:3–9
  - Women at crucifixion: Mark 15:40–47
  - Note: "Elias" is the archaic Edexcel transliteration of Elijah — use "Elias" when citing spec

### Qur'an — Paper 4B

- Surah 4:157–158 states Jesus (Isa) "was not killed, nor was he crucified, but it was made to appear so to them" — present this as the Islamic theological position, not a denial of historical fact, and contrast respectfully with the Christian account. Do NOT editorialise.
- Surah 19 (Maryam) covers the annunciation by Jibril and the virgin birth of Isa — present this accurately.
- Surah 12 (Yusuf/Joseph) is the only surah entirely devoted to one prophet's story.
- Surah 71 (Nuh/Noah) is a shorter surah devoted to Noah.
- The son to be sacrificed in Ibrahim's story (Surah 37) is traditionally identified as Ismail by most Muslim scholars, though the Qur'an does not name him — note "traditionally identified as Ismail" and the existence of a debate, matching the spec note.
- Ra-Rahman = universal mercy; Ar-Rahim = specific/particular mercy (both translate as "merciful" in English but are distinct Arabic terms — explain the difference).

### Islamic concepts

- **Jihad**: Greater Jihad (al-jihad al-akbar) = spiritual struggle against the lower self (nafs). Lesser Jihad (al-jihad al-asghar) = outward defensive struggle, tightly constrained in classical jurisprudence by Surah 2:190–194. NEVER reduce Jihad to "holy war" or to a simple inner vs outer binary.
- **Sunni vs Shi'a**: The Five Roots of Usul ad-Din are Shi'a (Tawhid, Adl, Nubuwwah, Imamah, Mi'ad). The Six Beliefs are Sunni (Allah, angels, holy books, prophets, Day of Judgement, predestination/al-Qadr). Don't conflate.
- **Talaq divorce**: Sunni = three pronouncements (historically; modern reform movements have one-session rulings). Shi'a = single pronouncement plus two witnesses. Edexcel 1RA0 spec 3C 2.6 names both — cover both.

---

## Edexcel 1RA0 command words and mark scheme structure

### The four-question format (per topic)

| Q | Stem | Marks | AO | Demand |
|---|------|-------|----|--------|
| (a) | "Outline three…" or "Describe…" | 3 | AO1 | Factual recall — three discrete points |
| (b) | "Explain two…" | 4 | AO1 | Two developed explanations |
| (c) | "Explain two… including reference to a source of wisdom and authority" | 5 | AO1 | Two developed explanations, one must cite a named source |
| (d) | "Discuss: '[Statement]'" | 12 (+3 SPaG on selected questions) | AO2 | Both-sides argument leading to a justified conclusion |

### Mark scheme rubric — StudyVault format ONLY

Use **Mastering / Secure / Developing / Emerging** for the 12-mark Discuss:
- **Mastering (10–12)**: Both sides fully developed with named sources; weighs perspectives explicitly; conclusion justifies a clear position
- **Secure (7–9)**: Both sides present with some development; at least one named source; conclusion present but may be thin
- **Developing (4–6)**: One side developed more than the other; sources vague or absent; conclusion descriptive not evaluative
- **Emerging (1–3)**: One-sided or very brief; minimal development; no named sources

For 3- and 4-mark questions: content-led mark scheme listing acceptable points (no rubric tier needed).

For 5-mark questions: "The 5th mark requires a named source of wisdom or authority — a Bible book + chapter:verse, a surah number, a named Catechism paragraph, a named papal document, a named hadith collection. Paraphrased sources without attribution do not earn the 5th mark."

**NEVER write** "Award N marks for…" — that is Edexcel examiner phrasing. Use StudyVault rubric.
**NEVER write** "Nothing worthy of credit".
**NEVER use** "Level 1 / Level 2 / Level 3" descriptors.

### SPaG (3 marks on selected 12-mark questions)

The three SPaG marks are awarded for: accurate spelling, correct punctuation, clear grammatical structure, and appropriate use of technical vocabulary (theological/religious terms spelt correctly). In `exam_tip_html`, remind students that SPaG is tested on selected 12-mark questions — "Use technical terms like 'eschatology', 'Paschal Mystery', 'tawhid' or 'theodicy' correctly and spell them right — SPaG marks reward precision."

---

## Free-tier rules

- **NO** `diagram_prompt`, **NO** `diagram_style`, **NO** `<!-- DIAGRAM -->` placeholder in `content_html`.
- Schema must have ONLY the keys listed in CONTENT_PROMPT.md (plus the 4 underscore-prefixed routing keys).

---

## content_html requirements

- **800–1500 words** (excluding HTML tags)
- Sequential `data-narration-id` (n1, n2, n3, ... no gaps)
- **≥2** `<div class="key-fact">` with actionable `data-revision-tip`; for source-of-authority spec points, the key-fact should name the scripture/catechism reference explicitly — this is where students practise the 5-mark source requirement
- **≥2** `<div class="collapsible">` — use collapsibles for: denominational comparisons, scholarly/theologian debates, contested concepts (e.g. Greater vs Lesser Jihad, Sunni vs Shi'a differences), misconception correctors
- **≥3** `<dfn class="term" data-def="...">` inline glossary terms — RS is terminology-heavy (eschatology, Paschal Mystery, Tawhid, samsara, etc.); aim for 5+ in practice
- **NO `<h1>` tags**
- HTML entities in `content_html` / `exam_tip_html` / `conclusion_html`: `&amp; &mdash; &lsquo; &rsquo; &ldquo; &rdquo;`
- Cover EVERY term in `section_markers` — examiners assess spec terms directly
- For starred comparison-marked spec points (e.g. 1.8*, 2.2*): include a collapsible titled "Compare with another tradition" that gives 2–3 bullets contrasting the religion's view with one other tradition's position — this is the content students reach for when writing 12-mark Discuss answers

---

## Practice questions (exactly 6)

- Each `type` must be one of the five `question_type_names` exactly:
  - `"3 marks — Outline Three"`
  - `"3 marks — Describe"`
  - `"4 marks — Explain Two"`
  - `"5 marks — Explain Two with Sources"`
  - `"12 marks — Discuss a Statement"`
- Recommended mix per lesson: 1× Outline Three, 1× Describe, 1× Explain Two, 1× Explain Two with Sources, 1× Discuss a Statement, 1× additional (any type that fits the content best)
- The 12-mark Discuss question MUST present a genuine evaluative statement (e.g. "Belief in the afterlife is the most important teaching in [religion]") — not a factual recall question
- For the 5-mark question: the model answer MUST explicitly name the source (e.g. "According to Surah 2:183, 'fasting was prescribed for you'…") — the 5th mark depends on source citation
- **NEVER reproduce or closely paraphrase a real Edexcel exam question.** Generate original questions from the spec topic.
- Every question tests content from THIS lesson only.

---

## Knowledge checks (exactly 5)

- 2 mcq + 2 fill-in-the-blank + 1 match
- Use `correct: <int>` (0-based index) + `options: [...]` format — NEVER `answers: [...]`
- At least 1 knowledge check should probe a known misconception from the teaching brief (e.g. "Which of the following CORRECTLY describes the kalam cosmological argument?")

---

## Flashcards (8–15)

- RS is doctrinal and terminology-heavy — 12–15 cards is typical
- Answer length ≤15 words target, hard cap 30
- One fact per card
- Card-type mix for RS:
  - Term ↔ definition (eschatology, Tawhid, samsara, purgatory, Paschal Mystery, etc.)
  - Source ↔ teaching (e.g. "What does Surah 112 teach about Allah?" → "That Allah is One, eternal, self-sufficient; He was not born and has no offspring")
  - Figure ↔ position (e.g. "What theodicy is associated with John Hick?" → "Soul-making: evil is necessary for moral and spiritual development")
  - Comparison (e.g. "How does Sunni belief in predestination differ from Shi'a?" → "Sunni: al-Qadr (divine decree) — God knows all actions. Shi'a: Adl (divine justice) — humans have free will")
  - Action ↔ significance (e.g. "What is the significance of the Mass as 'source and summit'?" → "It is both the origin and the culmination of all Catholic worship — from Lumen Gentium 7")

---

## Glossary terms

- ≥3 `<dfn class="term">` inline (hard minimum; aim for 6+ for RS)
- ≥6 entries in `glossary_terms` array (RS doctrine is heavy with technical vocabulary)
- Plain text — NO HTML entities, no `&rsquo;` etc.

---

## hero_keywords and hero_image_caption

- `hero_keywords`: 3–5 short search terms suited to a visually striking Unsplash photo. For RS: think places of worship, sacred artefacts, natural/cosmic imagery. Avoid generic "religion" — be specific to the lesson's tradition and topic.
- `hero_image_caption`: 1 sentence describing what an ideal hero image would show (e.g. "The interior of a Catholic cathedral with light streaming through stained glass, evoking the Trinity and liturgical worship").

---

## exam_tip_html

- Reference Edexcel command-word behaviour and mark scheme demand
- Highlight the most common student error for the 12-mark Discuss question on this topic (from the teaching brief's `student_errors_by_question_type` section)
- Remind students of the 5-mark source-of-authority requirement: the source must be named and identifiable
- For Paper 4 (textual studies): remind students that passage familiarity is everything — knowing the verse reference earns the 5-mark source point automatically
- **NEVER reference paper codes, spec codes, or component codes** (no "1RA0/1A", no "Paper 3A code")
- Mention SPaG where relevant to the lesson's 12-mark question

---

## conclusion_html

- 3 bullet-point key takeaways
- Each takeaway should be exam-revision ready: specific, testable, linked to the spec

---

## Embed teaching brief content

Use the `subject_level_teaching_brief` in the batch JSON to:
- Source at least one collapsible per lesson from `common_misconceptions` where relevant (especially the Aquinas/kalam/theodicy confusions and the Jihad framing)
- Use `student_errors_by_question_type` to shape `exam_tip_html`
- Use `topic_weighting_notes` to decide which sections of the content get more depth (Paper 1 = heaviest weighting; Paper 4 = students most reliant on these notes)

---

## Neutral board phrasing

This subject is Edexcel only. **Do NOT** name "AQA", "OCR", "Eduqas" or "WJEC" in user-facing content. Use neutral phrasing: "your exam", "this paper", "GCSE Religious Studies", "the specification". Edexcel can be named where it makes sense (e.g. "Edexcel's four-question format"). Never mention "Paper 1RA0/1A" or other component codes.

---

## ABSOLUTE BANS (PIPELINE-WIDE)

- **NO spec codes** in user-facing strings: `"1RA0"`, `"1RA0/1A"`, `"1RA0/1B"`, `"1RA0/4A"`.
- **NO "Award N marks for…"** rubric phrasing.
- **NO** `"Nothing worthy of credit"`.
- **NO** `"Level 1 / Level 2 / Level 3"` descriptors.
- **NO** `"pastPaper"` field on questions (deprecated).
- **NO copying the reference lesson's RE content** — it is a STRUCTURAL template only.
- **NO fabricated scripture references** — paraphrase when uncertain.
- **NO conflated theological attributions** (see Anti-Fabrication table above).
- **NO Mark 16:9–20** in Paper 4A lessons.
- **NO editorialising on Surah 4:157–158** — present as Islamic theological position, not claim about history.
- **NO HTML entities in plain-text fields** (`practice_questions`, `knowledge_checks`, `flashcard_questions`, `glossary_terms`, `description`) — use unicode characters only (`'`, `"`, `—`, `£`).
- **NO** `diagram_prompt` or `diagram_style` keys (free tier).

---

## Output

After generating all lessons in your batch, return ONLY this status line:

```
BATCH_DONE: batch_id={batch_id}, lessons_written={N}, files=<comma-separated paths>
```

Do NOT echo lesson content back. Just write the JSONs and confirm.

If any lesson's spec content is thin, write the JSON with the best content you can generate and flag it: `BATCH_DONE: batch_id=..., lessons_written=..., notes="lesson N had thin spec — supplemented with general RS knowledge"`.
