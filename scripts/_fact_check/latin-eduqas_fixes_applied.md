# Fixes applied — latin-eduqas (10 Sep 2026)

Every HIGH and MEDIUM finding was applied before narration, per the
fact-check-before-narration rule.

## Article lessons (21)
- Findings: 119 total — HIGH 23, MEDIUM 66, LOW 30.
- Applied: 89 HIGH+MEDIUM corrections across 21 lessons, in one batch.
- Re-validated after the corrections: 21 PASS, 0 FAIL (schema, narration-ID
  sequence, flashcard rules, knowledge-check mix, drift grep).
- Deterministic Latin quotation gate (`latin_quote_gate.py`) before the fixes:
  223 emphasised spans checked, 6 misses. After: 227 spans, 3 misses, all of
  them Latin technical terms in the Roman civilisation unit, which has no
  prescribed Latin text — `libertus` (on the defined vocabulary list),
  `manumissio iusta` and `victimarii`. Both fabricated set-text quotations are
  gone.

## Practice banks (12 lessons, 240 problems)
- Findings: 96 — HIGH 11, MEDIUM 58, LOW 27.
- Applied: 69 HIGH+MEDIUM corrections.
- Re-validated after the corrections: 12/12 pass the shape, tier-count and
  drift checks, and `_qa_practice_data.py --family latin` reports 0 errors and
  0 warnings across 240 problems.

## What the check was worth
Errors a student would otherwise have revised as fact, and lost marks on:
- Propertius Elegy 4.6: the lesson inverted the line, saying Apollo tells
  Octavian the sea is already his. The land is already his; he is told to win
  the sea.
- Sallust, Sempronia: `psallere` and `saltare` were called historic infinitives
  in three separate fields. They complete `poterat`; the historic infinitives in
  that passage are `posse`, `movere` and `uti`.
- Aeneid 8: Evander was called Etruscan. He is the Arcadian king of Pallanteum;
  Mezentius is the Etruscan.
- Aeneid 8: the Ara Maxima was said to be founded in honour of Cacus. It honours
  Hercules.
- Livy at New Carthage: the lesson said Scipio freed the artisans. He declared
  them public slaves of the Roman people.
- Cicero's letter about Tiro is a letter written TO Tiro.
- Three invented rules about the optional final section of the language paper
  (which cases are tested, which degrees of adjective may appear, and a word
  count for the English-into-Latin list) — none of them stated anywhere in the
  specification.
- In the practice banks: `per` given the ablative; an accusative time expression
  labelled ablative; `cum` clauses given the indicative across a whole lesson
  where the course requires the subjunctive; `dies` treated as feminine against
  the defined vocabulary list; a nominative plural used as a direct object.
