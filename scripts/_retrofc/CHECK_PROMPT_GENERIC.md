# Retro fact-check: checker brief (Geography, RS, Business, Computer Science, PE, Sociology, D&T, Geology, Astronomy and other subjects)

You are fact-checking ONE unit of GCSE lessons built before the mandatory
fact-check gate. Find claims that would cost a student marks or mislead them;
write surgical fixes. Expected yield 10-15% of lessons. Do not pad, do not
rewrite style, do not "improve" correct text.

## Inputs (paths relative to the repo root)

- `<unit-dir>/_brief.json` - subject, unit, board, spec file, lesson list
  (with `tier` where the subject is tiered).
- `<unit-dir>/raw/L01.txt ...` - one file per lesson (description, content
  HTML, conclusion, exam tip, practice questions, knowledge checks,
  flashcards, glossary). READ THESE one at a time. Do not read `_raw.json`.
- The spec markdown named in the brief: the authority for scope (what is
  examinable, named case studies / set texts / prescribed content), key
  terms and their definitions, the paper structure, question types, marks
  and timing. GREP it; read whole sections only when needed.
- External verification: this session's WebSearch budget is exhausted, so
  use WebFetch on Wikipedia, official statistics (ONS, UN, World Bank), the
  relevant professional or religious bodies' own sites, and manufacturers'
  or standards pages for technical values. Only correct a fact when you have
  found the true value; otherwise NOTE.

## What to check, in priority order

1. **Exam claims vs the spec.** Papers, sections, question types, marks
   (incl. SPaG and where it sits), timing, tiers, what is examined where,
   which case studies / texts / options this subject-board combination
   actually sets. Read the spec's assessment section before asserting.
2. **Facts, figures, definitions.** Statistics (dates, percentages,
   populations, GDP, casualty counts, magnitudes), named case studies (the
   right place, event, year and figures), scripture or doctrine quoted
   (verbatim and correctly attributed: book, chapter and verse; the right
   tradition), legal and technical facts (acts, standards, units, formulae,
   material properties, algorithms and their complexity, hardware facts),
   sporting rules and physiology values. An invented statistic, a misquoted
   scripture, a wrong formula or a wrong case-study figure is HIGH.
3. **Scope.** Content taught as examinable that belongs to a different board
   or option is MEDIUM; content from a different option of the SAME board
   taught as this option is HIGH. Higher-tier-only content taught to a
   Foundation lesson without a flag is MEDIUM (tiered subjects only).
4. **Answer keys.** Knowledge checks (`correct` index vs `options`), practice
   mark schemes and model answers (recompute every calculation; facts must
   match the corrected facts), flashcard answers. A knowledge check that
   marks the true answer wrong is HIGH.
5. **Misconceptions stated as fact.** Correct them only when the true
   statement is settled and the fix is surgical.

Ignore: style, length, tone, missing detail that is not wrong, structure,
narration ids, images.

## Writing the fixes

Two output files in `<unit-dir>`: `_report.json` and `_edits.json`, in
exactly the shapes below.

### `_report.json`
```json
{"unit": "...", "checked_at": "...", "spec_used": "specs/....md",
 "findings": [
  {"id": "F1", "lesson": 3, "field": "content_html", "severity": "HIGH",
   "claim": "the exact wrong text or claim", "truth": "what is actually the case",
   "evidence": "spec 3.1.2 / ONS page / Wikipedia article / recomputation",
   "verdict": "FIX" | "ADJUDICATE" | "NOTE"}
 ],
 "lessons_clean": [1, 2, 5], "summary": "one or two sentences"}
```
- FIX: certain and surgical; appears in `_edits.json`.
- ADJUDICATE: a real concern needing a judgement. Describe the options in
  `truth`. Not edited.
- NOTE: worth recording, not worth an edit (LOW only).

### `_edits.json` (array; only FIX findings)
- Text fields (`description`, `content_html`, `exam_tip_html`,
  `conclusion_html`): `{"lesson": 3, "field": "content_html", "find": "...",
  "replace": "...", "severity": "HIGH", "note": "F1: why"}`. `find` copied
  EXACTLY from the raw file (same entities, tags, `<sub>`/`<sup>`, KaTeX
  `\(...\)`, dash characters) and must occur exactly once in that field.
  Keep edits short; keep every `<dfn>`, `data-def`, `data-narration-id`,
  `data-revision-tip` attribute; keep the same number of
  `data-narration-id` blocks. `*_html` fields use entities; plain-text
  fields use unicode.
- JSON fields (`practice_questions`, `knowledge_checks`,
  `flashcard_questions`, `glossary_terms`): `{"lesson": 3, "field":
  "knowledge_checks", "path": "[2].correct", "expect": 1, "value": 2,
  "severity": "HIGH", "note": "F4: ..."}`. Always give `expect`.
- Plain-language rule: rewritten sentences must read for a 15-year-old.
  Short sentences, no hedging, British spelling.
- Validator limits: flashcard answers 30 words or fewer and not a comma
  list; two flashcards in one lesson must not share the same answer text;
  lesson `description` under 100 characters; never write an AO code
  immediately followed by a full stop.
- Copyright distancing (house rule): never paste a board's mark-scheme
  descriptors, level wording, indicative content, past-paper questions or
  specimen answers into any field. Correct FACTS (marks, timing, paper and
  section, objectives, extract / closed-book rules) and describe formats in
  the house vocabulary. The banned-string list below is the validator's
  floor, not the whole rule.
- Banned strings (the validator rejects the whole unit): "Level 1".."Level
  9" band names (use Top band / Upper-mid band / Mid band / Lower-mid band /
  Low band); "Paper 1 Section B"-style codes; "Component 1"; spec codes like
  "AQA 8035", "Edexcel 1GA0", "OCR J384", "Eduqas C111"; the rubric phrases
  "Nothing worthy of credit" and "Award N marks for". Eduqas / WJEC lessons
  never name the board in prose.

## How to report back

Under 250 words: counts (lessons, findings by severity, edits), the
ADJUDICATE items one line each with your recommendation, and anything that
blocked you. No prose summary of what was fine.
