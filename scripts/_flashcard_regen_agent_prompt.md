# Flashcard Regeneration Agent Prompt

Given a batch of lessons, produce new `flashcard_questions` arrays for each
following `docs/FLASHCARD_RULES.md`. This prompt is filled in per batch by
the orchestrator (`scripts/_regen_flashcards.py`).

---

## Agent brief

You are regenerating flashcards for a batch of StudyVault lessons. The
current flashcards across the platform were generated before we had
research-backed pedagogy rules, and most don't meet the quality bar. Your
job is to replace them with short, atomic, exam-relevant cards that
actually help a GCSE student consolidate knowledge.

## READ FIRST — in this order

1. `docs/FLASHCARD_RULES.md` — the authoritative pedagogy doc. 7 rules,
   per-subject card recipes with Q/A examples, anti-examples, validator
   rules. DO NOT SKIP. This is the single source of truth.

2. `scripts/_validate_content_json.py` — the `validate_flashcards` function
   shows the hard rules the orchestrator will enforce before writing to
   Supabase. Make sure your output passes it.

---

## Your inputs (per lesson in the batch)

You'll receive a JSON file per lesson at `scripts/_regen_flashcards_input/{lesson_id}.json`:

```json
{
  "lesson_id": "uuid",
  "title": "...",
  "description": "...",
  "subject_slug": "business-aqa",
  "subject_name": "Business Studies",
  "exam_board": "AQA",
  "subject_category": "business",   // for picking the right recipe from FLASHCARD_RULES.md
  "content_html": "<h2>...</h2><p>...</p>",
  "glossary_terms": [{"term": "...", "definition": "..."}],
  "key_facts": ["extracted text of each key-fact block"],
  "existing_flashcards": [{"q": "...", "a": "..."}]   // for reference only — don't copy
}
```

`subject_category` maps to a recipe in `FLASHCARD_RULES.md`. Possible values:
- `history` — use History recipe (event↔date, person↔significance, cause↔effect, cloze)
- `re` — Religious Education recipe
- `science` — Combined / Separate Sciences recipe
- `english-literature` — Eng Lit recipe (character↔quote, quote↔analysis, theme↔evidence)
- `geography` — Geography recipe
- `business` — Business / Economics recipe
- `sociology` / `psychology` — conceptual recipe
- `other` — fall back to mixed term/fact/cloze card types, applying the 7 rules
- `practice` — **SKIP, do not generate cards**. Return `{"skip": true, "reason": "practice-format subject"}`.

## Your output (per lesson)

Write to `scripts/_regen_flashcards_output/{lesson_id}.json`:

```json
{
  "lesson_id": "uuid",
  "flashcard_questions": [
    {"q": "...", "a": "..."},
    ...
    // 8-15 cards, matching the recipe for subject_category
  ],
  "notes": "One-line summary of approach — e.g. 'Went with 12 cards: 4 term→def, 3 event→date, 3 cause→effect, 2 cloze. Dropped 3 glossary terms (Finches of Grove, confidence trickster, peripeteia) as flavour.'"
}
```

If you can't produce at least 8 cards without violating rules, go lower
with justification in `notes`. Target: 8-15. Hard lower bound: 6.

## Rules summary (full detail in FLASHCARD_RULES.md)

Every card must:
1. Cover ONE fact (no stuffing multiple facts into one answer)
2. Have no enumerations in the answer (no "X and Y" lists → split)
3. Have enough context in the question to be answered without guessing
4. Not interfere with other cards in the deck (no duplicate plausible answers)
5. Be for exam-relevant content, not flavour/minor detail
6. Have answer ≤ 30 words (target ≤ 15)

Plus:
- Mix at least 2 card types per lesson (not all term→def)
- Don't restate knowledge_checks as flashcards
- For glossary terms you include, pick ONE direction (term→def is the default
  for most subjects; never both directions for the same term)
- Questions ≥ 5 words (no broken fragments)

## Subject-specific reminders

- **History**: include cloze cards for dated statements ("In ____ the ____ Revolt was triggered by the Poll Tax"). Use the event↔date pattern liberally — dates are exam-gold.
- **Science**: equation rearrangement cards AND cloze on formulae. `F = m × ____` is a great card.
- **English Lit**: quotes are essential. Character → defining quote is powerful; quote → speaker identifies authorship; quote → one-line analysis (not paragraph analysis).
- **Business / Economics**: formula components as cards (not whole formula). `Gross profit = Revenue − ____` beats "What is gross profit?"
- **RE**: source of authority cards — match teaching to scripture passage. Keep definitions tight; religious concepts interfere easily.
- **Geography**: case study stats as cloze. Named places and distinguishing features.
- **Sociology / Psychology**: theorist → claim, study → finding (with year). Cloze on dated studies.

## What's in / out

IN:
- Subject-specific facts the student MUST know for the exam
- Definitions (tight, unique)
- Dates and numerical facts
- Causes and effects
- Formulae and their components
- Quotes and their speakers / one-line significance
- Key case study facts

OUT:
- Essay prompts ("How does Dickens present...?")
- Multi-step analytical questions
- Flavour terminology that won't appear in a mark scheme
- Cards that restate lesson headings as questions
- Cards that duplicate knowledge_check content verbatim
- Open-ended discussion questions
- Process "tips" or revision advice

## Anti-examples to avoid producing

These are from the current platform and must not be repeated:

```
BAD: Q: "What is meant by 'Hippocrates'?"
     A: "An ancient Greek physician (c460-370 BC) who developed the Theory of the Four Humours, arguing that illness resulted from an imbalance in the body's four key fluids."
WHY: Four facts in one card. Split into three separate cards.
```

```
BAD: Q: "_____ About the Cause of Disease In medieval England..."
     A: "Ideas"
WHY: Broken fragment from content, single-word answer gives no testable understanding.
```

```
BAD: Q: "Name two ways to increase cash inflow"
     A: "Chase unpaid invoices and offer discounts for early payment"
WHY: Enumeration — student can't self-grade.
```

```
BAD: Q: "Acts of praise, honour or devotion directed towards God."
     A: "worship"
WHY: Definition front + term back = interference risk (many concepts match the definition). Flip direction.
```

## Validation

After generating cards for a lesson, self-check:

1. Are all answers ≤ 30 words? (If any are over, split them.)
2. Are there any enumeration patterns in answers?
3. Do any two cards have the same answer? (Interference — rewrite one or drop.)
4. Are the question fronts specific enough that there's only one right answer?
5. Is the deck using at least 2 card types?
6. Would these cards match the Q/A style in `FLASHCARD_RULES.md` for this subject?

If any fail, fix before writing output.

## Return

For each lesson in the batch:
- One JSON file written to the output directory
- Notes field should briefly explain card type mix and any judgement calls
  (glossary terms dropped, card count below target, etc.)

At the end of the batch, return a summary: total lessons processed, any
failures or skips, any patterns you noticed across lessons.
