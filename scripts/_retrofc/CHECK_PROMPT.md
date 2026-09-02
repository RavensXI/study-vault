# Retro fact-check: checker brief (English Literature)

You are fact-checking ONE unit of GCSE English Literature lessons that were
built before the mandatory fact-check gate. Your job is to find claims that
would cost a student marks or mislead them, and to write surgical fixes.
Expected yield is 10-15% of lessons carrying at least one real error; the
proven failure modes are listed below. Do not pad; do not rewrite style.

## Inputs (all paths relative to the repo root)

- `<unit-dir>/_brief.json` - subject, unit, spec path, primary-text path (or
  a note that the text is in copyright), lesson list.
- `<unit-dir>/raw/L01.txt ...` - one file per lesson: description, content
  HTML, conclusion, exam tip, practice questions, knowledge checks,
  flashcards, glossary. READ THESE, one at a time. Do not read `_raw.json`.
- The spec markdown named in the brief: the authority for paper/section
  structure, marks, assessment objectives, timing, question types,
  extract vs whole-text, closed-book rules, SPaG marks.
- The primary text, if present, under `scripts/_retrofc/_texts/`. GREP it
  (`grep -n -i "phrase"`); never read it whole. Quotation marks and dashes
  in the lessons are curly/typographic; search with a short distinctive
  word run, not the whole sentence.
- For in-copyright texts and anthology poems: WebSearch / WebFetch a
  reliable source (publisher extracts, poetry foundation, examiner reports).
  Only flag a quotation as wrong when you have found the real wording.

## What to check, in priority order

1. **Exam claims vs the spec.** Paper and section, marks per question,
   AO weightings (e.g. AQA 8702 Paper 1 Shakespeare: AO1 12 / AO2 12 / AO3 6 +
   4 SPaG; Paper 2 modern text: 30 + 4 SPaG; poetry cluster 30, unseen 24 + 8),
   timing, whether an extract is printed, closed-book vs open-book, whether
   context (AO3) is assessed on that question at all. Board-specific:
   Edexcel 1ET0 Paper 1/2 splits and its 20-mark essays; OCR J352 two-part
   questions and the 20+20 pattern; Eduqas C720 Component 1/2 and the
   Eduqas "AO2 not assessed on unseen comparison" style rules. Also the
   FALSE claim pattern "AO2 is not assessed on this question" when the spec
   says it is (this "AO2 denial" appeared in several AQA modern-text units).
2. **Quotations.** Verbatim wording, speaker, addressee, act/scene or
   chapter, and the moment in the plot. Fabricated quotations and
   misattributed lines were the single largest source of findings so far.
   A memorisation list or flashcard containing a line from a DIFFERENT text
   (a Macbeth line in a Blood Brothers list) is a HIGH finding.
3. **Facts.** Character names, relationships, deaths, dates of composition
   and publication, author biography, historical context claims, plot
   order. Invented poet or critic names are HIGH.
4. **Answer keys.** Knowledge checks (`correct` index vs `options`),
   practice-question mark schemes and model answers, flashcard answers must
   agree with the corrected facts. A knowledge check that marks the true
   answer wrong is HIGH.
5. **Labelling.** Question-type labels and mark counts on practice
   questions that do not match the board's real question (e.g. "Shakespeare
   essay" labels on a modern-text unit).

Ignore: style, length, tone, missing detail that is not wrong, structure,
narration ids, images. Do NOT "improve" correct text.

## Writing the fixes

Two output files in `<unit-dir>`:

### `_report.json`
```json
{"unit": "...", "checked_at": "...", "primary_text_used": true,
 "findings": [
  {"id": "F1", "lesson": 3, "field": "content_html", "severity": "HIGH",
   "claim": "the exact wrong text or claim", "truth": "what is actually the case",
   "evidence": "Gutenberg ch. 12 line: '...' / spec section 3.1 / URL",
   "verdict": "FIX" | "ADJUDICATE" | "NOTE"}
 ],
 "lessons_clean": [1, 2, 5], "summary": "one or two sentences"}
```
- FIX: you are certain and the fix is surgical; it appears in `_edits.json`.
- ADJUDICATE: a real concern where the right correction needs a judgement
  (two defensible readings, a spec ambiguity, an edit that would ripple
  through narration heavily). Describe the options in `truth`. Not edited.
- NOTE: worth recording, not worth an edit (LOW severity only).

### `_edits.json` (array; only FIX findings)
- Text fields (`description`, `content_html`, `exam_tip_html`,
  `conclusion_html`): `{"lesson": 3, "field": "content_html", "find": "...",
  "replace": "...", "severity": "HIGH", "note": "F1: why"}`.
  `find` is copied EXACTLY from the raw file (same curly quotes, same
  entities, same tags) and must occur exactly once in that field. Keep the
  edit as short as the correction allows; keep every `<dfn>`, `data-def`,
  `data-narration-id`, `data-revision-tip` attribute intact; keep the same
  number of `data-narration-id` blocks (edit text inside a block, never
  add or remove blocks).
- JSON fields (`practice_questions`, `knowledge_checks`,
  `flashcard_questions`, `glossary_terms`): `{"lesson": 3, "field":
  "knowledge_checks", "path": "[2].correct", "expect": 1, "value": 2,
  "severity": "HIGH", "note": "F4: ..."}`. Always give `expect` (the current
  value) so a stale edit cannot land on the wrong item.
- Plain-language rule: any sentence you rewrite must read for a 15-year-old.
  Short sentences, no hedging, British spelling.
- Validator limits that have bitten: flashcard answers 30 words or fewer,
  and a short flashcard answer must not be a comma list ("spelling,
  punctuation and grammar" is rejected as an enumeration; say one thing);
  lesson `description` under 100 characters; never write an AO code
  immediately followed by a full stop ("...AO1 and AO3." is rejected as a
  spec-code pattern; write "...AO1 and AO3 (context)." or reorder).
- Banned strings anywhere in lesson fields (the house validator rejects the
  whole unit): "Level 1".."Level 9" band names (use the house ladder: Top
  band / Upper-mid band / Mid band / Lower-mid band / Low band / Basic
  band); "Paper 1 Section B"-style codes (say "the 19th-century novel
  question" or "this section"); "Component 1"; spec codes like "AQA 8702"
  or "OCR J352"; the rubric phrases "Nothing worthy of credit" and "Award N
  marks for".

## How to report back

Your final message is read by the orchestrator, whose context is precious.
Keep it under 250 words: counts (lessons, findings by severity, edits),
the ADJUDICATE items one line each with your recommendation, and anything
that blocked you (text not found, spec section missing). No prose summary
of what was fine.
