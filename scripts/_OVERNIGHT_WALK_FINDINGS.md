# Overnight site walk — findings (12 Aug 2026)

Method: real browser, desktop 1400×950, as a **student** (no admin session),
walking whole journeys rather than checking pages. Screenshots at every step,
reviewed by eye. Assertions kept minimal and treated as hints about which
picture to open, never as verdicts — every false pass on 11 Aug came from a
green proxy check sitting over a visibly broken page.

Scope agreed with Tom: desktop only (mobile is separate work), Music excluded
(he is reviewing it himself; audio cannot be judged from here).

**Nothing here has been fixed.** Catalogue only. Screenshots in
`.claude/jobs/4059242c/tmp/walk/`.

---

## Findings

### F0 — The cohort gate is live in code but unreachable: nothing writes the year any more
`welcome.html` vs `index.html` · Severity: **HIGH, does not self-heal**

Tom noticed he was never asked what year he is in during sign-up. He was right,
and it is the root cause of F1 below.

`studyvault-exam-year` is:

- **written by exactly one page — `index.html`**, the OLD front door ("Which
  year are you in?", Year 10 / Year 11, ten references)
- **read by four live surfaces** — `js/browse-loader.js`, `js/exam-countdown.js`,
  `js/lesson-loader.js`, `exams.html`

`welcome.html`, the new front door that went live on 11 Aug, contains **zero**
references to it. So since the redesign shipped, nothing sets the value and all
four consumers read an empty string.

What each loses while it is unset:

| Surface | Behaviour with no cohort year |
|---|---|
| `exams.html` | `_yearsAhead` stays 0, so the plan paces to the 2026 season — which is over. Hence F1. |
| `js/exam-countdown.js` | cohort guard inert |
| `js/lesson-loader.js` | nav cohort guard inert |
| `js/browse-loader.js` | year-specific lesson filtering skipped, so students are shown lessons for exam years they will not sit |

The work itself is fine and fully merged — `cohort-gate` and `exam-dates-2027`
are both 0 commits ahead of platform. It was not lost in a branch; it was left
behind on a page that is no longer the homepage. The planner's own comment
states the intent plainly: *"so the countdowns and revision plan pace to THEIR
exams, not a series they will never sit."*

The fix is to ask the year in the new picker and write the same key. Not
attempted tonight — it is a question in a flow Tom is actively reviewing, and it
needs deciding where in the journey it belongs.

### F0/F1 — FIXED 12 Aug (see below for what remains)

The year question is back on the boards step of the new picker and is required.
The planner's slug-mismatch is fixed too. What is NOT fixed: the planner still
reports "No live lessons found" even with subjects, units and lessons all
returning rows — a third cause, not yet found. See F5.

### F1 — Revision planner is on the 2026 cohort while the dashboard is on 2027
`/exams` · Severity: **HIGH until 21 Aug** — but see F0: it does **not**
fully self-heal, because the cohort value it needs is never written

On the same day, for the same student:

- The **dashboard** says "272 days to your first exam · **May 2027**".
- The **planner** says "GCSE revision plan, April–June **2026**" and renders
  "No live lessons found for your selected subjects." — an empty page.

Two different rollover rules:

| Surface | Rule | Today gives |
|---|---|---|
| `exams.html` (planner) | `new Date() < '2026-08-21' ? 2026 : 2027` | 2026 |
| `js/exam-countdown.js` | same cutoff | 2026 |
| `dash-data.js` | dates hardcoded to 2027 | 2027 |

The planner's window (April–June 2026) ended two months ago, so it has nothing
to schedule and shows an empty state. It fixes itself on **21 August 2026**, the
day after results day. But for the next nine days the single feature that tells
a new student what to do between now and their exams is blank — and it is blank
during exactly the window when Year 11s are picking up their results and
younger siblings are starting to revise.

Worth deciding whether the cutoff should move earlier, or whether the planner
should follow the dashboard's lead rather than its own calendar.

### F2 — Dashboard exam dates are a provisional demo timetable, shown as fact
`dash-data.js` · Severity: **MEDIUM**

The "272 days to your first exam · May 2027" figure comes from a table whose own
comment reads *"per-subject exam papers (summer 2027, PROVISIONAL demo
timetable…)"*. A student is being given a countdown to a date we made up.

Nobody will be harmed by a few days' drift, but the number is presented with the
confidence of a real timetable, and `data/exam-dates-2027.json` exists. Worth
pointing the dashboard at the real file, or labelling it provisional until the
boards publish.

### F3 — Two 404s on every lesson, browse and guide page
`_lw_manifest.json`, `_lw_captions_demo.json` · Severity: **LOW, cosmetic**

Painted-hero lookups left over from the desk-world skin, reaching into
`design-lab/`, which is excluded from the deploy. They fail silently and nothing
visible breaks, but they fire on every content page load. Already known; now
confirmed site-wide rather than lesson-only.

### F4 — Reading extract is about twice the size of the same extract beside it
`/practice/english-language-aqa/paper-1-reading/1` · Severity: **question**

The source extract in the left passage panel renders at display size — ten lines
of large serif italic filling a tall column. The *same* extract inside the
worked example on the right renders at normal body size.

For it: the panel carries read-aloud, a dyslexia font and colour overlays, so it
is plainly built as a reading-comfort surface. Against it: this is the text a
student re-reads constantly while answering, and at this size even a short
extract runs past a screenful, so the question scrolls out of view. Needs a
judgement, not a fix.

---

## Checked and clean

- **New-student journey**: `/` → picker → 8 subjects → boards → 11 topic
  questions → dashboard. No console errors, no failed loads. Board step
  correctly blocks until every subject has one; multi-pick questions (Geography
  "UK physical landscapes", pick 2) enforce the full count; the dashboard
  reports **0% complete**, so the 11 Aug percentage fix holds in the real flow.
- **Twenty content pages** across ten subjects — History, Business, Psychology,
  Geography, Science, RS, Computer Science (article); Maths, English Language,
  Spanish (practice). Correct titles, no redirects, no raw LaTeX in body text,
  no failed requests, no console errors.
- **Every internal link offered on eight lesson pages** — 64 links followed,
  **zero dead**. Note: `/guide/history-aqa/exam-technique/index` 404s, but the
  site never links to it (history-aqa has revision-technique guides only). I
  invented that URL; it is not a defect.
- **Browse** pages for History, Maths, Science and a unit-level browse.
- **Guides**: revision-technique index and an English Literature exam-technique
  page both render.
- **Shorts feed**, **flashcard revision**, **both dashboards** all render.
- **Spanish method card** is particularly well built — vocabulary table, grammar
  focus, worked model with translation.

---

## Harness faults worth recording

Four things looked like site bugs for a few minutes and were mine:

1. Clicking board chips **detached by the re-render** each click triggers, so
   only the first registered.
2. Answering a **pick-2** question once and reading the disabled Next as a bug.
3. Reading the **guided warm-up step** as a broken question card, because its
   input has a different id from the bare-question input.
4. Inventing a guide URL and treating its 404 as a dead link.

All four produced a plausible-looking failure. The pattern: when a check goes
red, suspect the check first; when it goes green, go and look anyway.


---

## F5 — Planner still empty after both fixes (open)

`/exams` · Severity: **HIGH** · found 12 Aug, **not fixed**

With a cohort year set and the slug mismatch corrected, the planner now:

- says "GCSE revision plan, April–June **2027**" (was 2026)
- shows the honest banner "Official 2027 timetables are not published yet, so
  these dates are estimates based on the 2026 papers"
- successfully queries **subjects → units → lessons**, all returning rows

…and still renders "No live lessons found for your selected subjects."

So `fetchTopicPools()` receives lessons and returns an empty pool. The filtering
between "lessons came back" and "pool is empty" is where the remaining fault
lives. Candidates not yet tested: a `status` filter, or the pool builder
requiring topic selections (`WIZ.topics`) that a student who has not answered
option questions does not have.

Deliberately not guessed at. Two fixes tonight were verified by watching the
behaviour change; this one would have been a guess, and the planner is the
feature a revising student leans on hardest.
