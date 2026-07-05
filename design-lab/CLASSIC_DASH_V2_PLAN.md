# Classic Dashboard v2 — plan from Tom's brief (5 Jul 2026)

Thesis unchanged: classic = the desk's contents, filed neatly. This round makes
every card REAL — driven by the same engines the product already ships.

## 0. What already exists (changes the cost of everything below)
- **Leitner is built.** The lesson flashcard modal (main.js) does right/wrong
  self-assessment into `sv-flashcard-progress` (5 boxes, intervals 0/1/2/4/7/14,
  per-card next-review dates, streak). `/revise` is a cross-lesson review page
  sharing that store, with a box-distribution bar viz (red→green segments).
- **A deterministic revision planner is live at /exams** (no AI, exam-date-driven,
  plan in localStorage). Re-planning is a cheap pure function.

## 1. Revision timetable: prompted at signup, dynamic after
- First-visit dashboard state = "build your timetable" prompt → reuse the /exams
  planner flow (subjects + exam dates already there), embedded as an onboarding
  step rather than a separate page students must find.
- **Dynamic adjustment rule (deterministic, no AI):** each login, compare
  planned-days-past vs evidence of study (lesson visits, flashcard sessions,
  warm-ups — all already tracked locally). Missed items roll forward and the
  remaining schedule re-spreads from today to the exam dates. Kept-to plan =
  byte-identical output. One pure function, unit-testable.
- **Calendar becomes the planner's face:** dashboard mini-calendar days are
  clickable → popover listing that day's scheduled items (subject-coloured,
  each deep-linking to its lesson/practice/review session). Red ✕ = missed
  (rolled forward), tick = done, ring = today.
- Note: ties into the existing "holiday awareness" open item — term dates can
  slot into the same re-spread function later.

## 2. This Week panel
- Drop Radio and Next Mock (no decision value).
- Keep: Best subject, Needs a look, Warm-up accuracy, Shorts watched.
- Candidate 5th line: "Cards due today: N" from the Leitner store — it earns
  its place because it's actionable (click → review session).

## 3. Flashcards door → real interleaved Leitner session
- Door opens the /revise experience (same store the lesson modals feed):
  due-cards-first, interleaved across subjects, right/wrong per card.
- Alongside the session: the box-distribution viz (already styled in
  revise.html) + "due today" count.
- **How explicit about Leitner:** don't name it. Show the five boxes as a
  journey ("new → learning → nearly there → solid → mastered") with the
  interval consequence stated plainly ("got it right — see it again in 7
  days"). The mechanism teaches itself; the jargon goes in a revision-technique
  guide link for the curious.
- Storage note: `sv-flashcard-progress` is localStorage — fine for demo;
  account-level sync is a platform-v2 item.

## 4. Start button starts the warm-up
- Build the warm-up player: a 10-question quick-fire overlay pulling from
  (a) KCs the student got wrong (knowledge_check_scores/local), (b) Leitner
  box-1/2 cards, (c) failing that, KCs from recently-visited lessons.
- Start = warm-up overlay → on completion, auto-advance to plan item 2 (the
  continue lesson). The plan card's items become genuinely sequential.
- Warm-up accuracy line in This Week then reads from real attempts.

## 5. Subject cards
- Faded ladder sketches at 86px don't read — replace with the subject's cloth
  tab treatment doing more work: a wider accent tab + the painted vignette
  RESERVED for hover/expanded state where it has room to breathe.
- **Click behaviour:** card face splits into two honest targets —
  "Continue: <next lesson title> →" (primary) and a compact "Units ▾" expander
  listing the subject's units with per-unit progress, each row linking to
  /browse/{subject}/{unit} (topic picker). No more forced next-lesson.
- Card keeps: name, progress bar (subject colour), n of m + %.

## 6. "64 of 273 topics" — answer
- The number counts LESSONS (sum of unit lesson counts). Lesson↔topic is 1:1
  in our structure, so "topics" isn't false, but practice-first subjects make
  it wobbly (a maths "lesson" is a topic drill set). Recommendation: say
  "lessons" everywhere (truthful, matches the browse pages' own language);
  keep "topics" only in marketing copy.

## Build order (each shippable alone)
1. Quick wins: This Week trim, topics→lessons, subject-card split targets +
   units expander, de-emphasise sketches (small CSS/JS, one pass).
2. Flashcards door → /revise session + box viz + due-today line.
3. Warm-up player + Start rewiring.
4. Timetable onboarding + dynamic re-spread + clickable calendar (biggest;
   builds on /exams engine).

Demo caveat: all evidence signals are localStorage on the demo, so "dynamic"
behaviours demo per-browser. Real accounts inherit the same logic later.
