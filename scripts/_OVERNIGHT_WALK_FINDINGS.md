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

### F1 — Revision planner is on the 2026 cohort while the dashboard is on 2027
`/exams` · Severity: **HIGH until 21 Aug, then self-healing**

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
