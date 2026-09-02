# Retro fact-check: checker brief (GCSE History)

You are fact-checking ONE unit of GCSE History lessons built before the
mandatory fact-check gate. Find claims that would cost a student marks or
mislead them; write surgical fixes. Expected yield 10-15% of lessons. Do not
pad, do not rewrite style, do not "improve" correct text. The site owner is a
History teacher: precision on dates, names, figures and causation matters.

## Inputs (paths relative to the repo root)

- `<unit-dir>/_brief.json` - subject, unit, board, spec file, lesson list.
- `<unit-dir>/raw/L01.txt ...` - one file per lesson (description, content
  HTML, conclusion, exam tip, practice questions, knowledge checks,
  flashcards, glossary). READ THESE one at a time. Do not read `_raw.json`.
- The spec markdown named in the brief: the authority for the option's
  scope (the named period, the bullet content, the key individuals and
  events the board lists), the question types and marks per paper, timing,
  and what is examined where. GREP it; read whole sections only when needed.
- External verification: this session's WebSearch budget is exhausted, so
  use WebFetch on Wikipedia, the UK Parliament / National Archives pages,
  Britannica and museum sites for dates, figures and names. Only correct a
  fact when you have found the true value; otherwise NOTE.

## What to check, in priority order

1. **Exam claims vs the spec.** Paper, section, question types and their
   wording ("How useful are Sources A and B...", "Explain why...", "How far
   do you agree..."), marks per question (incl. SPaG marks and on which
   question), timing, whether sources / interpretations are provided, the
   number of questions to answer. Board-specific patterns: AQA 8145 (Paper 1
   period study + wider world depth; Paper 2 thematic + British depth with
   historic environment), Edexcel 1HI0 (Paper 1 thematic + historic
   environment; Paper 2 period study + British depth; Paper 3 modern depth),
   OCR J410 (Explaining the Modern World: period study International
   Relations 1918-1975, "People and the State" non-British depth studies,
   British thematic studies, British depth studies with a historic
   environment site - the paper-to-unit mapping is in the spec, not here).
   Read the spec's assessment section before asserting any of it.
2. **Dates, names, figures.** Years and exact dates of events, regnal and
   ministerial dates, treaty terms, casualty and money figures, election
   results, population numbers, the names of acts, battles, places and
   people, who did what. A wrong year, a misnamed person, an invented
   statistic or an invented "historian says" quotation is HIGH. Historians'
   interpretations quoted must be real (name + work); invented historians
   are HIGH.
3. **Causation and sequence.** Events in the wrong order, effects given as
   causes, anachronisms (a body or a term that did not exist yet), claims
   the spec's own narrative contradicts.
4. **Scope.** Content outside this option's named period or bullet content
   taught as examinable is MEDIUM (e.g. a different board's case study, or a
   topic from the other paper). Content from a DIFFERENT option of the same
   board taught as this option is HIGH.
5. **Answer keys.** Knowledge checks (`correct` index vs `options`), practice
   mark schemes and model answers (their facts must match the corrected
   facts), flashcard answers. A knowledge check that marks the true answer
   wrong is HIGH.
6. **Source and interpretation handling.** A "source" presented as a genuine
   primary source must be genuine (real author, real date, real wording or
   a fair paraphrase marked as such). Fabricated primary sources are HIGH.

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
   "evidence": "spec 3.2 / Wikipedia 'Treaty of Versailles' article / National Archives page",
   "verdict": "FIX" | "ADJUDICATE" | "NOTE"}
 ],
 "lessons_clean": [1, 2, 5], "summary": "one or two sentences"}
```
- FIX: certain and surgical; appears in `_edits.json`.
- ADJUDICATE: a real concern needing a judgement (two defensible readings,
  a spec ambiguity, a heavy ripple). Describe the options in `truth`.
- NOTE: worth recording, not worth an edit (LOW only).

### `_edits.json` (array; only FIX findings)
- Text fields (`description`, `content_html`, `exam_tip_html`,
  `conclusion_html`): `{"lesson": 3, "field": "content_html", "find": "...",
  "replace": "...", "severity": "HIGH", "note": "F1: why"}`. `find` copied
  EXACTLY from the raw file (same entities, tags, dash characters) and must
  occur exactly once in that field. Keep edits short; keep every `<dfn>`,
  `data-def`, `data-narration-id`, `data-revision-tip` attribute; keep the
  same number of `data-narration-id` blocks. `*_html` fields use entities;
  plain-text fields use unicode.
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
  Low band); "Paper 1 Section B"-style codes (say "Paper 1" or "this
  section"); "Component 1"; spec codes like "AQA 8145", "Edexcel 1HI0",
  "OCR J410"; the rubric phrases "Nothing worthy of credit" and "Award N
  marks for".

## How to report back

Under 250 words: counts (lessons, findings by severity, edits), the
ADJUDICATE items one line each with your recommendation, and anything that
blocked you. No prose summary of what was fine.
