# Flashcard Rules

Authoritative source for what makes a good StudyVault flashcard. Agents read this before generating cards; the validator enforces the hard rules; Tom's review checks against these when approving new subjects.

Flashcards consolidate knowledge students already have a grip on — they don't teach new concepts from scratch. The lesson content teaches; the flashcards lock it in. Apply these rules strictly; the cost of a bad card compounds (spaced-repetition systems will keep showing it).

---

## The 7 rules

### 1. Minimum information per card

One fact, one relationship, one term per card. A student should be able to mark their own attempt right or wrong in a single glance. If the answer is more than one sentence, split into multiple cards.

**Bad (one card cramming four facts):**
- Q: What is meant by 'Hippocrates'?
- A: An ancient Greek physician (c460-370 BC) who developed the Theory of the Four Humours, arguing that illness resulted from an imbalance in the body's four key fluids.

**Good (same knowledge, three cards):**
- Q: Who was Hippocrates? / A: An ancient Greek physician.
- Q: What theory is Hippocrates known for? / A: The Theory of the Four Humours.
- Q: What did the Theory of the Four Humours claim about illness? / A: That illness resulted from an imbalance in the body's four key fluids.

### 2. No enumerations in answers

If the answer is a list ("name two X", "give three Y"), the student can't self-grade reliably. They get one of the items and don't know whether to pass or fail themselves. Each item in the list becomes its own card, with context that makes each specific.

**Bad:**
- Q: Name two ways to increase cash inflow.
- A: Chase unpaid invoices and offer discounts for early payment.

**Good (two cards):**
- Q: A business wants to speed up customer payments. What's the fastest lever? / A: Chase unpaid invoices.
- Q: How can a business incentivise customers to pay early? / A: Offer discounts for early payment.

### 3. Context in the question, not in the answer

The question must uniquely identify what you're testing. "Who wrote this?" is useless. "Who wrote *Jekyll and Hyde*?" is a flashcard. Context in the question also unlocks **cloze deletion** — powerful because surrounding words anchor memory while the test stays sharp.

**Bad:**
- Q: When was it fought?
- A: 1066.

**Good (question form):**
- Q: When was the Battle of Hastings? / A: 1066.

**Better (cloze form):**
- Q: The Battle of Hastings was fought in ____, between William of ____ and King ____.
- A: 1066 / Normandy / Harold.

Cloze cards are especially good for dated statements, formulae with components, and quotations.

### 4. Avoid interference

Within one deck, no two card fronts should plausibly have the same answer. If "A church service that follows a set structure" could describe both liturgical worship AND another type of worship in the same deck, the cards interfere — the student can't reliably retrieve the right term. Either tighten the definition to be uniquely identifying or drop one card.

**Bad (interferes within one lesson):**
- Q: A church service that follows a set pattern. / A: Liturgical worship.
- Q: A church service with planned order but some flexibility. / A: Semi-liturgical worship.

**Good:**
- Q: A church service with the *same* structure every week, led by a priest, with set responses. / A: Liturgical worship.
- (The alternative term gets its own card only if it's in the spec and uniquely distinguishable.)

### 5. Understanding precedes memorisation

Don't create cards for concepts the student hasn't yet grasped through the lesson. Cards reinforce; they don't introduce. This means: every flashcard answer should be something the lesson body has already taught. No flashcards on material that only appears in the card itself.

### 6. Evidence-based inclusion

Every card earns its place by being something the student actually needs for the exam. Flavour terms ("Finches of the Grove" in Dickens, "Obeah woman" in Leave Taking, individual minor quote's exact phrasing) don't belong. Core exam content does.

Test: would this card's answer plausibly appear on the target board's exam or in a typical mark scheme? If yes, keep. If no, drop — the student has finite revision time.

### 7. Answer length

**Target: ≤ 15 words. Hard cap: 30 words.** Longer than 30 → split.

Questions can be longer (cloze cards, especially) but should read as a single continuous thought, not a paragraph.

---

## Per-subject card recipes

Different subjects need different card types. One-size-fits-all is why current cards feel uneven. The retrofit agent picks from the allowed types for the target subject.

### History (article format)

Allowed card types:
- **Event → Date**: "When did the Black Death arrive in England?" / "1348."
- **Person → one-line significance**: "Who was Edward Jenner?" / "The doctor who developed the smallpox vaccine in 1796."
- **Cause → Effect**: "What effect did the Great Plague of 1665 have on London's population?" / "It killed roughly 100,000 people, about a quarter of the city."
- **Cloze on dated statements**: "The ____ of ____ in 1381 was triggered by the Poll Tax." / "Peasants' Revolt."
- **Source → attribution**: "Which ancient physician wrote *On the Natural Faculties*?" / "Galen."

Avoid: essay-style prompts ("How far do you agree..."), multi-step enumerations of causes.

Target 10-15 cards per lesson.

### Religious Education (article format)

Allowed types:
- **Belief / concept → short definition**: "What is *tawhid* in Islam?" / "The belief in the absolute oneness of God."
- **Practice → purpose**: "Why do Muslims perform *salah*?" / "To submit to God's will five times daily, structuring the day around remembrance of Allah."
- **Source of authority → attribution**: "Which source teaches *'Love your neighbour as yourself'*?" / "The Bible (Mark 12:31), spoken by Jesus."
- **Concept → distinguishing feature**: "What makes Quaker worship different from Anglican?" / "Quakers worship in silence, waiting for the Spirit; Anglicans follow a set liturgy."
- **Scholar / divergence → position**: "What view does Richard Dawkins take on religious upbringing?" / "He argues labelling children with their parents' religion is a form of harm."

Avoid: inverted "definition → term" as default (interferes easily with similar concepts). Use term → definition forward.

Target 10-15 cards per lesson.

### Science (all three, article format)

Allowed types:
- **Term → short definition**: "What is osmosis?" / "The movement of water across a partially permeable membrane, from high to low water concentration."
- **Equation → application**: "What equation links force, mass and acceleration?" / "F = ma."
- **Cloze on equations**: "Wave speed = ____ × ____." / "frequency / wavelength."
- **Quantity → SI unit**: "What is the SI unit of work done?" / "Joules (J)."
- **Process → next step**: "In aerobic respiration, what does glucose + oxygen produce?" / "Carbon dioxide + water + energy (ATP)."
- **Cloze on numbered steps**: "Stages of mitosis: prophase → ____ → ____ → telophase." / "metaphase / anaphase."

Avoid: cards that require understanding a diagram the student can't see (unless we add image support).

Target 12-18 cards per lesson (more because science has more atomic facts).

### English Literature (article format)

Allowed types:
- **Character → defining quote**: "Which short phrase captures Lady Macbeth's ambition?" / '*Unsex me here.*'
- **Quote → speaker**: "Who says '*O, I am fortune's fool*'?" / "Romeo (Romeo and Juliet, Act 3)."
- **Quote → one-line analysis**: "What does '*Out, damned spot*' reveal about Lady Macbeth?" / "Her guilt manifests as hallucinated blood — she cannot wash away what she has done."
- **Theme → evidence**: "Where in *An Inspector Calls* does Priestley attack capitalist self-interest?" / "Birling's 'every man has to look after himself' speech in Act 1."
- **Technique → example in text**: "Give an example of pathetic fallacy in *Macbeth*." / "The stormy night of Duncan's murder."

Avoid: essay-style questions ("How does Dickens present..."), vague analytical prompts.

Target 10-15 cards per lesson.

### Geography (article format)

Allowed types:
- **Place → distinguishing feature**: "What feature makes the Nile Delta an agricultural centre?" / "Fertile silt deposits from annual flooding before the Aswan Dam."
- **Process → stage**: "What's the second stage of the water cycle after evaporation?" / "Condensation."
- **Term → short definition**: "What is a pyroclastic flow?" / "A fast-moving current of hot gas and volcanic ash that flows along the ground."
- **Cloze on statistics**: "The 2010 Haiti earthquake killed approximately ____ people." / "230,000."
- **Case study → key fact**: "What was the magnitude of the 2011 Tōhoku earthquake?" / "9.0–9.1 on the moment magnitude scale."

Target 10-15 cards per lesson.

### Business / Economics (article format)

Allowed types:
- **Term → definition**: "What does limited liability mean?" / "Owners only lose what they invested; personal assets are protected from business debts."
- **Formula → component**: "In break-even = Fixed Costs / Contribution per Unit, what is contribution per unit?" / "Selling price per unit minus variable cost per unit."
- **Concept → one real-world example**: "Give an example of penetration pricing by a UK company." / "Aldi's low-price entry into the UK grocery market."
- **Cloze on formulae**: "Gross profit = Revenue − ____." / "Cost of sales."
- **Misconception → correction**: "Why are fringe benefits classed as *financial* motivation, not non-financial?" / "They have monetary value to the employee and cost the business money — they're pay in a different form."

Avoid: enumerations of strategies ("name three pricing methods"), vague application prompts.

Target 10-15 cards per lesson.

### Sociology / Psychology / similar conceptual (article format)

Allowed types:
- **Theorist → claim**: "What did Durkheim argue was the function of religion in society?" / "Social cohesion — binding communities through shared belief and ritual."
- **Study → finding**: "What did Milgram's 1963 obedience study find?" / "65% of participants administered what they believed were fatal electric shocks when instructed by an authority figure."
- **Term → definition**: "What is *anomie* in Durkheim's theory?" / "A breakdown of social norms that leaves individuals without moral guidance."
- **Cloze on dated studies**: "____'s (____) study on conformity found that ____% of participants gave a wrong answer at least once." / "Asch / 1951 / 75."

Target 10-15 cards per lesson.

---

## Subjects that get NO flashcards

- **Mathematics (practice format)** — all tiers use `practice_data`, not article content. No flashcards.
- **Modern Foreign Languages (practice format)** — vocab drilling happens through practice problems with audio.
- **English Language practice units** — passage-based skills, not flashcardable.
- **Science calculation units** (Physics Calc, Chem Calc, Bio Data, Higher Calculations) — equation recall happens through practice problems.
- **Geography Skills unit** — mixed-format mostly practice, no flashcards.

Planning agent's classification of a unit as `practice` automatically skips flashcard generation.

---

## Volume target per lesson

| Subject type | Cards per lesson |
|---|---|
| History narrative | 12-15 |
| Science (content-dense) | 12-18 |
| RE beliefs/practices | 10-14 |
| English Literature | 10-15 |
| Geography | 10-15 |
| Business / Economics | 10-15 |
| Sociology / Psychology | 10-15 |
| Any subject (lean lesson) | 8 minimum |

If a lesson genuinely can't support 8 cards without violating the rules, it can go below — but the agent must note why in its summary (e.g. "Lesson is a brief introduction with little factual content; 6 cards is the honest ceiling").

---

## Anti-examples from the current platform

These are from shipped content. Agents should recognise and never produce:

**The stuffing violation (Rule 1):**
- Q: "What is meant by 'Hippocrates'?"
- A: "An ancient Greek physician (c460-370 BC) who developed the Theory of the Four Humours, arguing that illness resulted from an imbalance in the body's four key fluids."
- Problem: three facts jammed into one card. Split into Hippocrates-is-Greek-physician, Hippocrates-wrote-Four-Humours, Four-Humours-is-about-imbalance.

**The broken fragment (Rule 6 + Rule 1):**
- Q: "_____ About the Cause of Disease In medieval England (c1250–1500), people had very limited understanding of what actually caused disease"
- A: "Ideas"
- Problem: the Q is an orphaned fill-in-blank from content; the A is a single word that teaches nothing. Scrapped.

**The interference trap (Rule 4):**
- Q: "A church service that follows a set pattern" → A: "Liturgical worship"
- Q: "Formal worship with structured responses" → A: "Common worship"
- Problem: both definitions could describe either term. The cards collide.

**The enumeration (Rule 2):**
- Q: "Name two ways to increase cash inflow"
- A: "Chase unpaid invoices and offer discounts for early payment"
- Problem: student can get one, miss one, and not know if they've passed.

**The inverted glossary interference (Rule 3 + Rule 4):**
- Q: "Acts of praise, honour or devotion directed towards God"
- A: "worship"
- Problem: the definition could describe many terms (praise, prayer, worship, devotion, adoration). Front should be the term.

---

## What is NOT a flashcard

If a prompt falls into these categories, it does not belong in a flashcard deck. Send it elsewhere:

- **Essay / extended response prompts** — "How does Dickens present Pip's moral decline?" is a practice question, not a flashcard.
- **Multi-step evaluations** — "How far do you agree that...?" Belongs in practice_questions.
- **Ambiguous comparisons without specifics** — "What's the difference between similar things?" fails Rule 3.
- **"Why does X matter?" without context** — fails Rule 3.
- **Open discussion questions** — no right/wrong answer to self-grade.
- **Revision strategy tips** — "How would you revise this topic?" isn't content.

---

## Agent instructions (summary)

When generating flashcards for a lesson:

1. Read the lesson content, glossary, key facts, title, and teaching brief
2. Identify the subject category and pull the matching recipe
3. Draft cards using the allowed card types for that subject
4. Validate each card against the 7 rules (especially answer length and enumeration patterns)
5. Check for interference within the deck
6. Target the volume for the subject type; go lower only with justification
7. Return the array — answer cap ≤30 words, target ≤15
8. If a glossary term is included as a flashcard, choose one direction (term→def is the default for most subjects; cloze for dated/formula-heavy content) and use only that direction per card

Do NOT produce cards that re-ask a knowledge_check question verbatim, or that restate lesson headings as questions.

---

## Validator hard rules (enforced before Supabase write)

- Every card has a `q` and `a` field, both strings
- `a` is ≤ 30 words (hard cap). Warn at > 15.
- `q` is ≥ 5 words (anti-fragment: filters out "Ideas" broken cards)
- No comma+and enumeration in `a` unless total word count ≤ 6
- `a` is not a single word unless `q` matches pattern `"What is the [term for / name for]..."` OR `"Who is..."` OR `"When..."` OR the `a` is a date/number
- `a` is not a substring of `q` (rejects card-restating-itself cases)
- Deck has 8-18 cards (soft range), validator warns outside this band
- At least 2 distinct card types per lesson (e.g. not all term→def)
- No two cards in the same deck have the same `a` value (direct duplicate check)

Failed cards are logged; the agent gets one retry opportunity to fix and resubmit.

---

## Rollback + provenance

The retrofit archives every pre-retrofit `flashcard_questions` array to `scripts/_flashcard_backup/{date}/{lesson_id}.json` before overwriting Supabase. If quality regresses for any lesson, the backup restores it.

After retrofit:
- The client-side glossary auto-import (in `js/main.js` `openFlashcardModal`) is disabled
- `flashcard_questions` becomes the single authoritative source for what the modal shows
- New lessons must follow this doc from generation time
