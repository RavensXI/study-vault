# English Literature — content debt audit

Read-only audit of Supabase, 29 Aug 2026. No row was modified.
Scope: the four free-tier boards. The Unity bespoke subject `english-literature` is
included only where it duplicates free-tier content.

## 1. Denominators

| Board | Slug | Lessons | Units | Flashcards | Cards | Cards/lesson | KCs | KC/lesson | Practice Qs | Median content words |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| AQA | `english-literature-aqa` | 222 | 29 | 222/222 (100%) | 2,914 | 13 | 222/222 (100%) | 5 | 222/222 | 858 |
| Edexcel | `english-literature-edexcel` | 215 | 29 | 215/215 (100%) | 2,960 | 14 | 215/215 (100%) | 5 | 215/215 | 987 |
| Eduqas | `english-literature-eduqas` | 197 | 24 | 197/197 (100%) | 2,408 | 12 | 197/197 (100%) | 5 | 197/197 | 847 |
| OCR | `english-literature-ocr` | 156 | 20 | 156/156 (100%) | 2,125 | 14 | 156/156 (100%) | 5 | 156/156 | 730 |
| **Free-tier total** | | **790** | **102** | **790/790 (100%)** | **10,407** | 13 | **790/790 (100%)** | 5 | **790/790** | **861** |
| _Unity AQA (reference)_ | `english-literature` | 42 | 5 | 42/42 (100%) | 209 | 5 | 42/42 (100%) | 5 | 42/42 | 1012 |

Coverage is complete. Every one of the 790 free-tier lessons carries flashcards,
exactly 5 knowledge checks and exactly 6 practice questions. There is no coverage
gap anywhere in English Literature — the debt is entirely a **quality** debt.

## 2. Flashcard verdicts

| Board | Lessons | Clean | Suspect | Bad | Bad + suspect |
|---|---:|---:|---:|---:|---:|
| AQA | 222 | 188 | 12 | 22 | 34 (15%) |
| Edexcel | 215 | 206 | 9 | 0 | 9 (4%) |
| Eduqas | 197 | 189 | 8 | 0 | 8 (4%) |
| OCR | 156 | 145 | 11 | 0 | 11 (7%) |
| **Total** | **790** | **728** | **40** | **22** | **62** |

**The regex debt is real, and it is smaller and more localised than the note in
memory says.** The memory note estimated ~140 remaining regex-generated AQA lessons.
The actual figure is **22 lessons**, all in `english-literature-aqa`, and the other
three boards are clean of it. Templated cards make up 7.6% of AQA's card pool
and 0.0-0.3% of every other board's.

Detection was by templated question stems — the generator emitted a small fixed set:

| Template | AQA cards | Edexcel | Eduqas | OCR |
|---|---:|---:|---:|---:|
| `in_TITLE_what` | 96 | 0 | 2 | 4 |
| `in_TITLE_what_is_said_about` | 52 | 0 | 0 | 0 |
| `term_mean_in_this_lesson` | 36 | 0 | 0 | 0 |
| `what_does_QUOTE_reveal` | 20 | 0 | 0 | 0 |
| `state_a_key_point_from` | 14 | 0 | 0 | 0 |
| `give_an_example_of` | 4 | 0 | 4 | 2 |

The stems split into two grades. **Broken** stems — `in_TITLE_what_is_said_about`,
`state_a_key_point_from`, `what_does_QUOTE_reveal`, `term_mean_in_this_lesson`,
`name_a_key_concept` — produce cards that are wrong or unusable, because the rule
guessed a subject from the first capitalised word of a sentence or truncated a
quotation. **Monotone** stems — `in_TITLE_what`, `give_an_example_of` — produce
individually correct cards, but when 7 of 11 cards share one stem the deck becomes a
glossary drill with no coverage of plot, character or method. Both were checked by
reading full decks; the monotone grade alone never condemns a card.

Scoring rule used: **bad** = 25%+ of the lesson's cards use a *broken* stem, or 60%+
use any stem. **suspect** = at least one broken-stem card, or 40%+ monotone, or fewer
than 10 cards, or 45%+ of answers lifted verbatim from the lesson body, or 30%+ of
cards ask about "the lesson" instead of the text, or 2+ cards duplicated in another
lesson.

### The 22 bad lessons (all AQA)

| Key | Title | Broken | Templated | Patterns |
|---|---|---:|---:|---|
| `english-literature-aqa/a-christmas-carol/1` | Victorian Context & Dickens' Purpose | 2 | 9/12 | in_TITLE_what x7, in_TITLE_what_is_said_about x1, state_a_key_point_from x1 |
| `english-literature-aqa/an-inspector-calls/10` | Language, Structure and Dramatic Devices | 0 | 8/11 | in_TITLE_what x8 |
| `english-literature-aqa/animal-farm/6` | The Windmill & Boxer's Exploitation | 4 | 8/10 | in_TITLE_what x4, in_TITLE_what_is_said_about x4 |
| `english-literature-aqa/blood-brothers/4` | Adolescence & Growing Apart | 10 | 10/10 | in_TITLE_what_is_said_about x3, term_mean_in_this_lesson x5, what_does_QUOTE_reveal x2 |
| `english-literature-aqa/dna/3` | Acts 3-4: Escalation & the Ending | 9 | 9/9 | in_TITLE_what_is_said_about x3, state_a_key_point_from x1, term_mean_in_this_lesson x5 |
| `english-literature-aqa/dna/4` | Character Analysis | 9 | 9/9 | in_TITLE_what_is_said_about x3, state_a_key_point_from x1, term_mean_in_this_lesson x5 |
| `english-literature-aqa/frankenstein/6` | The Pursuit & the Ending | 5 | 11/12 | in_TITLE_what x6, in_TITLE_what_is_said_about x4, state_a_key_point_from x1 |
| `english-literature-aqa/great-expectations/1` | Context: Victorian Class & Social Mobility | 3 | 9/11 | in_TITLE_what x6, in_TITLE_what_is_said_about x3 |
| `english-literature-aqa/lord-of-the-flies/4` | Chapters 7-9: Savagery & Simon's Death | 4 | 9/11 | in_TITLE_what x5, in_TITLE_what_is_said_about x3, state_a_key_point_from x1 |
| `english-literature-aqa/lord-of-the-flies/5` | Chapters 10-12: The Final Descent | 6 | 10/13 | in_TITLE_what x4, in_TITLE_what_is_said_about x5, state_a_key_point_from x1 |
| `english-literature-aqa/love-and-relationships/2` | Family Love | 7 | 8/8 | give_an_example_of x1, what_does_QUOTE_reveal x7 |
| `english-literature-aqa/macbeth/10` | The Ending & Key Themes | 4 | 9/13 | in_TITLE_what x5, in_TITLE_what_is_said_about x3, state_a_key_point_from x1 |
| `english-literature-aqa/my-name-is-leon/3` | Part 2: Foster Care & Maureen | 0 | 7/8 | in_TITLE_what x7 |
| `english-literature-aqa/power-and-conflict/6` | Remains & War Photographer | 7 | 9/9 | give_an_example_of x2, what_does_QUOTE_reveal x7 |
| `english-literature-aqa/power-and-conflict/9` | The Prelude — Power of Nature | 9 | 9/10 | in_TITLE_what_is_said_about x1, state_a_key_point_from x1, term_mean_in_this_lesson x4, what_does_QUOTE_reveal x3 |
| `english-literature-aqa/pride-and-prejudice/1` | Context: Regency Society & Austen's World | 1 | 7/10 | in_TITLE_what x6, state_a_key_point_from x1 |
| `english-literature-aqa/pride-and-prejudice/3` | Wickham, Collins & Darcy's Letter | 3 | 9/11 | in_TITLE_what x6, in_TITLE_what_is_said_about x2, state_a_key_point_from x1 |
| `english-literature-aqa/the-merchant-of-venice/6` | Character Analysis | 4 | 10/11 | in_TITLE_what x6, in_TITLE_what_is_said_about x4 |
| `english-literature-aqa/the-merchant-of-venice/7` | Key Themes & Exam Technique | 12 | 12/12 | in_TITLE_what_is_said_about x5, state_a_key_point_from x1, term_mean_in_this_lesson x6 |
| `english-literature-aqa/the-tempest/4` | Acts 4-5: Resolution & Forgiveness | 4 | 9/11 | in_TITLE_what x5, in_TITLE_what_is_said_about x3, state_a_key_point_from x1 |
| `english-literature-aqa/unseen-poetry/1` | Reading & Analysing an Unseen Poem | 8 | 8/8 | in_TITLE_what_is_said_about x3, state_a_key_point_from x1, term_mean_in_this_lesson x4 |
| `english-literature-aqa/worlds-and-lives/2` | Identity & Heritage | 10 | 10/10 | in_TITLE_what_is_said_about x2, state_a_key_point_from x1, term_mean_in_this_lesson x7 |

### Three representative bad cards

**1 — the generator matched a conjunction and turned it into a subject.**
`english-literature-aqa/the-merchant-of-venice/7`, card 9 of 12:

> **Q:** In Key Themes & Exam Technique, what is said about But?
> **A:** The Christians, who preach mercy, show none — exposing the gap between their words and actions

The source sentence begins "But the Christians, who preach mercy…". The rule took the
first capitalised word of the sentence as the topic. All 12 cards in this lesson are
templated; six of them are glossary definitions re-labelled "What does the term 'X'
mean in this lesson?".

**2 — a playwright presented to the student as a character.**
`english-literature-aqa/dna/4` ("Character Analysis"), card 8 of 9:

> **Q:** In Character Analysis, what is said about Kelly?
> **A:** Leaves Phil's inner life deliberately opaque, making him both fascinating and deeply disturbing

Source prose: "Kelly leaves Phil's inner life deliberately opaque…" — that is Dennis
Kelly, the author of *DNA*. The card sits between cards on Phil and on Adam, so a
student revising characters learns that "Kelly" is a character in the play. This is
mark-affecting.

**3 — a corrupted quotation, plus the wrong speaker.**
`english-literature-aqa/love-and-relationships/2` ("Family Love"), card 4 of 8:

> **Q:** What does 'fingertips still pinch / the last one-Loss of your tape' reveal?
> **A:** She holds on as long as possible, reluctant to let go

Armitage's line is "the last one-hundredth of an inch". The extractor truncated at the
hyphen and spliced in text from the next section. A student who quotes this in an exam
gets no AO2 credit. All 8 cards in this lesson are templated, seven of them
"What does '<quote>' reveal?".

## 3. Placeholder / thin content_html

**There is no literal placeholder text anywhere in English Literature.** A scan of all
832 lessons for "content coming soon", "placeholder", "TODO", "[TBC]", "TBD",
"lorem ipsum" and "under construction" returned **zero hits**. The templated-title
signature recorded in memory ("Brontë's treatment of exam technique") no longer exists
either — the named example lessons now hold real prose. That specific debt is closed.

What remains is measurable **thinness** and **cross-board duplication**.

| Board | Rebuild (<45% of median) | Extend (45-62%) | Rewrite duplicate | Total flagged |
|---|---:|---:|---:|---:|
| AQA | 0 | 3 | 22 | 25 |
| Edexcel | 0 | 0 | 0 | 0 |
| Eduqas | 0 | 2 | 8 | 10 |
| OCR | 12 | 17 | 8 | 37 |
| **Total** | **12** | **22** | **38** | **72** |

Free-tier median lesson = **861 words** of plain text. OCR sits well below the
other three boards (median 730 words vs Edexcel 987), and every rebuild-grade lesson
is OCR.

### Rebuild — 12 lessons, all OCR

| Key | Title | Words | % of median | Markers |
|---|---|---:|---:|---|
| `english-literature-ocr/unseen-poetry/4` | Responding to Themes | 181 | 21% | very_thin, heading_heavy |
| `english-literature-ocr/unseen-poetry/5` | Comparing Two Unseen Poems | 186 | 22% | very_thin, heading_heavy |
| `english-literature-ocr/unseen-poetry/3` | Analysing Form & Structure | 204 | 24% | very_thin, heading_heavy |
| `english-literature-ocr/unseen-poetry/2` | Analysing Language & Imagery | 213 | 25% | very_thin, heading_heavy |
| `english-literature-ocr/poetry-youth-and-age/7` | Comparison Skills | 262 | 30% | very_thin, heading_heavy |
| `english-literature-ocr/unseen-poetry/1` | What is Unseen Poetry? | 267 | 31% | very_thin |
| `english-literature-ocr/unseen-poetry/6` | Exam Technique & Timed Practice | 319 | 37% | very_thin |
| `english-literature-ocr/pride-and-prejudice/8` | Key Themes & Exam Technique | 361 | 42% | very_thin |
| `english-literature-ocr/pride-and-prejudice/1` | Context: Regency Society | 362 | 42% | very_thin |
| `english-literature-ocr/poetry-youth-and-age/6` | Comparing Across Time | 366 | 43% | very_thin |
| `english-literature-ocr/pride-and-prejudice/7` | Irony & Narrative Voice | 377 | 44% | very_thin |
| `english-literature-ocr/pride-and-prejudice/6` | Character Analysis | 379 | 44% | very_thin |

`english-literature-ocr/unseen-poetry` is the worst unit on the platform: six lessons,
median 208 words, roughly a quarter of the corpus norm. The prose that is there is
correct and well written — three `<h2>` sections and two Key Facts each — it is simply
a third of a lesson. This unit should be treated as an unfinished build, not a repair.

### Extend — 22 lessons

| Key | Title | Words | % of median | Markers |
|---|---|---:|---:|---|
| `english-literature-ocr/war-of-the-worlds/8` | Key Themes & Exam Technique | 398 | 46% | thin |
| `english-literature-ocr/war-of-the-worlds/7` | Symbolism & Setting | 400 | 46% | thin |
| `english-literature-ocr/war-of-the-worlds/2` | Book 1: The Arrival | 405 | 47% | thin |
| `english-literature-ocr/war-of-the-worlds/5` | Character & Narration | 406 | 47% | thin |
| `english-literature-ocr/war-of-the-worlds/6` | Science Fiction Genre & Structure | 414 | 48% | thin |
| `english-literature-ocr/poetry-conflict/7` | Comparison Skills | 430 | 50% | thin |
| `english-literature-ocr/war-of-the-worlds/3` | Book 1: The Fall of Civilisation | 436 | 51% | thin |
| `english-literature-ocr/a-christmas-carol/1` | Context: Victorian Poverty | 436 | 51% | thin |
| `english-literature-ocr/war-of-the-worlds/1` | Context: Victorian Science & Empire | 462 | 54% | thin |
| `english-literature-ocr/war-of-the-worlds/4` | Book 2: Survival & Resolution | 465 | 54% | thin |
| `english-literature-ocr/poetry-conflict/8` | Exam Technique & Quotation Bank | 472 | 55% | thin |
| `english-literature-ocr/poetry-conflict/5` | Form, Structure & Language | 498 | 58% | thin |
| `english-literature-ocr/poetry-youth-and-age/5` | Form, Structure & Language | 509 | 59% | thin |
| `english-literature-ocr/pride-and-prejudice/4` | Pemberley & Changed Perceptions | 509 | 59% | thin |
| `english-literature-eduqas/unseen-poetry/5` | Comparing Two Unseen Poems | 510 | 59% | thin |
| `english-literature-aqa/an-inspector-calls/2` | Act 1: The Engagement and the Inspector Arrives | 511 | 59% | thin |
| `english-literature-ocr/poetry-youth-and-age/4` | Memory & Nostalgia | 517 | 60% | thin |
| `english-literature-eduqas/unseen-poetry/6` | Exam Timing & Strategy | 517 | 60% | thin |
| `english-literature-ocr/pride-and-prejudice/3` | Wickham, Collins & Darcy's Letter | 528 | 61% | thin |
| `english-literature-aqa/an-inspector-calls/7` | Characters: The Inspector and Mr Birling | 529 | 61% | thin |
| `english-literature-ocr/anita-and-me/8` | Key Themes & Exam Technique | 730 | 85% | heading_heavy |
| `english-literature-aqa/princess-and-the-hustler/1` | Context: 1960s Bristol & the Bus Boycott | 892 | 104% | heading_heavy |

### Duplicate content — 38 lessons in 3 clusters

An 8-gram shingle comparison of all 832 lessons found three clusters where whole units
are the same prose under two subject slugs. The board name was find-and-replaced
correctly in each copy, so nothing names the wrong board — but the lessons are
otherwise identical.

| Cluster | Lessons | Overlap | Note |
|---|---|---|---|
| `a-taste-of-honey` L1-L8 | AQA <-> Eduqas | 96.8-100% | Free tier <-> free tier. Two boards, one text. |
| `leave-taking` L1-L8 | AQA <-> OCR | 73.6-97.0% | Free tier <-> free tier. Flashcards are duplicated too. |
| `a-christmas-carol` L1, 2, 4, 5, 6, 7 | **Unity** `english-literature` <-> free-tier AQA | 99.2-100% | **Crosses the Unity/free-tier line.** |

The third cluster needs a decision before any content work. The standing rule is that
Unity bespoke content does not port to the free tier — same spec code means a fresh
build. Six A Christmas Carol lessons currently exist on both sides at 99-100%
identity. The audit cannot tell which way the copy went; either direction breaks the
rule, and the free-tier AQA side is the one that should be rewritten.

## 4. Other findings

- **Eduqas names its own board in prose in 47 lessons** (88 mentions). The locked
  directive is that Eduqas and WJEC content uses neutral phrasing and never names the
  board. This is a find-and-replace pass, not a content job — no agent needed.
- **`<!-- DIAGRAM -->` comments remain in 660 lessons** (AQA 157, Edexcel 202, Eduqas 174, OCR 127) — residue from the April 2026
  free-tier diagram strip. They are invisible to students. One SQL update clears them.
- **Knowledge checks are uniform and complete**: 5 per lesson on all 832 lessons, all
  in the canonical `correct` + `options` shape. No KC debt.
- **Practice questions**: 6 per lesson on all 832 lessons. No debt.
- **82 flashcard (question, answer) pairs are shared by more than one lesson** (166 card
  instances). Most are legitimate cross-board facts about the same set text
  ("When was A Christmas Carol first published?"). Only the `leave-taking` cluster is a
  genuine copy.

## 5. Sized recommendation

Cost anchor: the settled Anthropic Console figure from the Psychology API build is
**$0.48 per lesson** for a full lesson generation (content, questions, KCs, flashcards),
with prompt caching on. A batch content agent handles ~5 lessons per run. A
flashcards-only regeneration re-uses the existing `content_html` as cached context and
emits ~15 short cards, so budget it at roughly a quarter of a full lesson (~$0.12).

| # | Job | Lessons | Runs (~5/run) | API cost | Priority |
|---|---|---:|---:|---:|---|
| 1 | Regenerate flashcards — 22 AQA `bad` lessons | 22 | 5 | ~$3 | **Do first** |
| 2 | Rebuild OCR `unseen-poetry` (6) + the 6 other rebuild-grade OCR lessons | 12 | 3 | ~$6 | **Do first** |
| 3 | Rewrite one side of each free-tier duplicate pair (Eduqas A Taste of Honey 8, OCR Leave Taking 8), flashcards included | 16 | 4 | ~$8 | Should |
| 4 | Decide the Unity/free-tier A Christmas Carol overlap, then rewrite the free-tier AQA side | 6 | 2 | ~$3 | Should — needs Tom's decision first |
| 5 | Regenerate flashcards — the remaining 24 `suspect` lessons not covered by job 3 | 24 | 5 | ~$3 | Optional |
| 6 | Extend the 22 thin lessons to corpus length | 22 | 5 | ~$11 | Optional |
| | **Total** | **102 lesson-jobs** | **24** | **~$32 (£26)** | |

Add-ons that ride on the content jobs:

- **Re-narration.** Jobs 2, 3, 4 and 6 change `content_html`, so those 56 lessons need
  a fresh Azure pass at ~£0.10/lesson — about **£6**. Fact-check runs before narration,
  per the standing pipeline rule.
- **Podcasts.** `english-literature-ocr/unseen-poetry` would be rebuilt wholesale, so
  that unit's podcasts should be regenerated once the lessons are live. The other jobs
  touch too few lessons per unit to justify it.
- **Free.** The Eduqas board-naming fix and the `<!-- DIAGRAM -->` comment strip are
  both single SQL passes with no model cost.

**Minimum credible fix is jobs 1 and 2: 34 lessons, 8 runs, ~$8 plus ~£1.20 narration.**
That clears every card a teacher would call broken and the one unit that is visibly
unfinished. Jobs 3 and 4 close the duplication, which matters more for originality and
for the Unity boundary rule than for what a student sees. Job 6 is polish.

Machine-readable worklist: `scripts/_englit_debt_worklist.json`
