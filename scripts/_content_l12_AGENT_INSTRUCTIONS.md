# L1/2 Vocational Award — Article Lesson Agent Instructions

You write ONE complete article-format revision lesson for a WJEC Eduqas/WJEC Level 1/2 Vocational Award
(the externally-assessed unit). Your specific lesson (subject, unit, lesson number, title, description,
SUB-TOPICS TO COVER, SPEC FILE, REF FILE, OUTFILE) is given in the calling message.

## STEP 1 — Read these first
1. The SPEC FILE (given in the call) — the official teaching content. This is the **source of truth for
   coverage**: cover every relevant point for your SUB-TOPICS using the spec's terminology.
2. `_ref_lesson.json` (in the same content dir) — a REAL finished lesson. Match its JSON structure and every
   field's shape EXACTLY (content_html components, knowledge_checks shapes, flashcard/glossary shapes).

## STEP 2 — Write a single JSON OBJECT to your OUTFILE
Keys, exactly as in the ref: `title`, `description`, `content_html`, `exam_tip_html`, `conclusion_html`,
`practice_questions`, `knowledge_checks`, `flashcard_questions`, `glossary_terms`.

## Hard rules
- **NEVER put any spec code or spec scaffolding in student-facing text.** Forbidden anywhere in any field:
  topic codes like `1.1.1` / `1.2`, the unit code (`5299QA` / `5259QA`), `Topic Area`, `externally assessed`,
  `the specification`, `Unit 1`, `Component`, or the exam-board name. Write it as a normal revision lesson.
  (This was the #1 defect in the last vocational build — do not repeat it.)
- **content_html**: ~900–1400 words. Use the ref's components: section `<h2>`/`<h3>` headings,
  `<p data-narration-id="nN">` paragraphs (number them n1, n2, … in order), **at least 2** key-fact divs and
  **at least 2** collapsibles, exactly as the ref builds them. For every glossary term, wrap its first mention
  in the content with the same `<dfn class="term" data-def="…">term</dfn>` markup the ref uses (so ≥4 dfns).
- **exam_tip_html** and **conclusion_html**: same shape as the ref (conclusion = "Key Takeaways" list).
- **practice_questions**: exactly 6 (match the ref's object shape and mark style — never write "Award N marks").
- **knowledge_checks**: exactly 5 — two `mcq`, two `fill`, one `match` — each with the EXACT field shape the
  ref uses (`mcq`/`fill`: `q`,`type`,`correct`,`options`; `match`: the ref's left/right/order shape).
- **flashcard_questions**: exactly 12. Each ≤30 words; answers ≤12 words, no enumerated lists; single-word
  answers must be phrased as a W-question.
- **glossary_terms**: 4–6, each `{term, definition}`; ≥4 of them must appear as `<dfn>` in content_html.
- **Plain-text fields** (description, practice_questions, knowledge_checks, flashcard_questions, glossary_terms):
  literal Unicode only — NO HTML entities (`&rsquo;`, `&amp;` etc.). description ≤120 chars.
- Reading age 15–16. Accurate, exam-relevant content. These are "ports": you already know the overlapping
  GCSE Business / PE material well — use that knowledge, but cover exactly what the spec lists for this lesson.

## STEP 3 — Self-check
Re-open the file: confirm it parses; 6 practice / 5 KC (2 mcq+2 fill+1 match) / 12 flashcards / 4–6 glossary;
≥2 key-fact divs, ≥2 collapsibles, ≥4 `<dfn>`; and grep your own text for any of the forbidden spec strings.

Return ONE line: `{subject} {unit} L{NN}: written` (or describe any problem).
