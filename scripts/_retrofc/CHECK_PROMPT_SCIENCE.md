# Retro fact-check: checker brief (GCSE Sciences)

You are fact-checking ONE unit of GCSE science lessons (Combined Science or a
separate science) that were built before the mandatory fact-check gate. Your
job is to find claims that would cost a student marks or mislead them, and to
write surgical fixes. Expected yield is 10-15% of lessons carrying at least
one real error. Do not pad; do not rewrite style; do not "improve" correct
text.

## Inputs (all paths relative to the repo root)

- `<unit-dir>/_brief.json` - subject, unit, board, the spec file(s), the
  qualification (combined or separate), lesson list with each lesson's `tier`
  (`F`, `H`, `both`, or null = untiered).
- `<unit-dir>/raw/L01.txt ...` - one file per lesson: description, content
  HTML, conclusion, exam tip, practice questions, knowledge checks,
  flashcards, glossary. READ THESE one at a time. Do not read `_raw.json`.
- The spec markdown named in the brief: the authority for what is in scope,
  which statements are Higher-tier only, which content is separate-science
  only, the required practicals, the equations students must recall versus
  those given on the equation sheet, and the paper structure (number of
  papers, duration, marks, tiers, which topics sit in which paper). GREP the
  spec (`grep -n -i "phrase"`); read whole sections only when needed.
- No primary text. Physical constants, SI units, standard values and
  definitions come from the spec first; where the spec is silent use your own
  knowledge only for settled facts (e.g. the charge on an electron, the
  order of the reactivity series, the products of complete combustion). If
  you are not certain, do not "correct" it - record a NOTE.

## What to check, in priority order

1. **Spec scope and tier.** Content that is not in this board's spec for this
   qualification is a finding (separate-science content taught in a Combined
   unit as if examined, e.g. AQA Space physics in Trilogy; Edexcel
   separate-only statements in 1SC0). Higher-tier-only content taught to a
   Foundation-tier lesson without a Higher flag is MEDIUM. Wrong paper
   allocation (a topic said to be on Paper 1 when the spec puts it on Paper
   2) is MEDIUM. Required practicals: the practical named must exist in the
   spec for this qualification, with the right method outline (independent /
   dependent / control variables, the safety point the spec highlights).
2. **Numbers, units, equations.** Every value (g = 9.8 N/kg, c = 3.0 x 10^8
   m/s, specific heat capacity of water 4200 J/kg degC, speed of sound, Avogadro
   constant, molar volume 24 dm3 at RTP, relative masses, pH values, blood
   glucose figures, normal body temperature, heart rate), every unit and
   prefix, every physics equation (symbol form and word form), every chemical
   equation (balanced, correct formulae, state symbols if given), every
   numeric worked example (recompute it). A wrong equation, a wrong constant
   or an unbalanced equation presented as balanced is HIGH. Say which
   equations the spec says students must RECALL and which are GIVEN when a
   lesson claims either.
3. **Facts and definitions.** Spec definitions (e.g. "specific latent heat",
   "osmosis", "mole", "isotope") should match the spec's wording in
   substance. Organelle / organ / hormone / enzyme facts, process order
   (stages of mitosis, the cardiac cycle, fractional distillation order,
   electrolysis products at each electrode), classifications (metal /
   non-metal, exothermic / endothermic, vector / scalar) and historical
   attributions (Rutherford, Chadwick, Mendeleev, Darwin, Wallace) must be
   right. Invented scientist names, dates or "studies" are HIGH.
4. **Answer keys.** Knowledge checks (`correct` index vs `options`), practice
   mark schemes and model answers (recompute every calculation, check sig
   figs and units), flashcard answers. A knowledge check that marks the true
   answer wrong is HIGH. Watch for questions whose "correct" option and
   explanation disagree.
5. **Exam claims.** Number of papers, duration, marks, tiers, and which
   paper covers which topics, all against the spec's assessment section.
   Never assert a paper structure from memory: read it in the spec. Mark
   allocations on practice questions must be plausible for the question type
   (1-2 marks for recall, 4-6 for explain/describe, 6 for extended response).
6. **Misconceptions the lesson teaches as fact.** E.g. "heavier objects fall
   faster", "current is used up", "plants respire only at night", "the
   atomic mass is the number of protons", "a catalyst takes part in the
   reaction and is used up", "all metals react with water". Correcting these
   is HIGH when the sentence is stated as true.

Ignore: style, length, tone, missing detail that is not wrong, structure,
narration ids, images, diagrams.

## Writing the fixes

Two output files in `<unit-dir>`:

### `_report.json`
```json
{"unit": "...", "checked_at": "...", "spec_used": "specs/aqa/....md",
 "findings": [
  {"id": "F1", "lesson": 3, "field": "content_html", "severity": "HIGH",
   "claim": "the exact wrong text or claim", "truth": "what is actually the case",
   "evidence": "spec 4.5.1.2 / recomputation: 12 x 9.8 = 117.6 N / settled fact",
   "verdict": "FIX" | "ADJUDICATE" | "NOTE"}
 ],
 "lessons_clean": [1, 2, 5], "summary": "one or two sentences"}
```
- FIX: you are certain and the fix is surgical; it appears in `_edits.json`.
- ADJUDICATE: a real concern where the right correction needs a judgement
  (a spec ambiguity, a tier question the lesson metadata cannot settle, an
  edit that would ripple through narration heavily). Describe the options in
  `truth`. Not edited.
- NOTE: worth recording, not worth an edit (LOW severity only).

### `_edits.json` (array; only FIX findings)
- Text fields (`description`, `content_html`, `exam_tip_html`,
  `conclusion_html`): `{"lesson": 3, "field": "content_html", "find": "...",
  "replace": "...", "severity": "HIGH", "note": "F1: why"}`.
  `find` is copied EXACTLY from the raw file (same entities, same tags, same
  `<sub>`/`<sup>`, same KaTeX `\(...\)` delimiters, same dash characters) and
  must occur exactly once in that field. Keep the edit as short as the
  correction allows; keep every `<dfn>`, `data-def`, `data-narration-id`,
  `data-revision-tip` attribute intact; keep the same number of
  `data-narration-id` blocks (edit text inside a block, never add or remove
  blocks). `*_html` fields use HTML entities (`&deg;`, `&times;`, `&rarr;`);
  plain-text fields (questions, flashcards, glossary) use unicode.
- JSON fields (`practice_questions`, `knowledge_checks`,
  `flashcard_questions`, `glossary_terms`): `{"lesson": 3, "field":
  "knowledge_checks", "path": "[2].correct", "expect": 1, "value": 2,
  "severity": "HIGH", "note": "F4: ..."}`. Always give `expect` (the current
  value) so a stale edit cannot land on the wrong item.
- Plain-language rule: any sentence you rewrite must read for a 15-year-old.
  Short sentences, no hedging, British spelling.
- Validator limits that have bitten: flashcard answers 30 words or fewer,
  and a short flashcard answer must not be a comma list (say one thing); two
  flashcards in one lesson must not share the same answer text; lesson
  `description` under 100 characters; never write an AO code immediately
  followed by a full stop.
- Copyright distancing (house rule): never paste a board's mark-scheme
  descriptors, level wording, indicative content, past-paper questions or
  specimen answers into any field. Correct FACTS (marks, timing, paper and
  section, objectives, extract / closed-book rules) and describe formats in
  the house vocabulary. The banned-string list below is the validator's
  floor, not the whole rule.
- Banned strings anywhere in lesson fields (the house validator rejects the
  whole unit): "Level 1".."Level 9" band names (use the house ladder: Top
  band / Upper-mid band / Mid band / Lower-mid band / Low band); "Paper 1
  Section B"-style codes (say "Paper 1" or "this paper"); "Component 1";
  spec codes like "AQA 8464", "Edexcel 1SC0", "OCR J250"; the rubric phrases
  "Nothing worthy of credit" and "Award N marks for".

## How to report back

Your final message is read by the orchestrator, whose context is precious.
Keep it under 250 words: counts (lessons, findings by severity, edits), the
ADJUDICATE items one line each with your recommendation, and anything that
blocked you (spec section missing, tier unresolvable). No prose summary of
what was fine.
