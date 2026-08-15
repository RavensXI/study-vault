# Test Suite — Plan

**Status:** proposal, written 14 Aug 2026 during the Supabase outage. Nothing
built beyond the rescue described in §2.
**The one-sentence case:** we already write tests constantly — we just throw
them away. The suite is the decision to keep them.

---

## 1. What already exists (the surprising part)

### 1.1 Permanent, already in the repo
| Asset | What it proves | State |
|---|---|---|
| `scripts/_qa_practice_data.py` | every practice problem structurally sound (18k problems) | run on demand; exit-code gated |
| `scripts/_qa_practice_answers.py` | every deterministic answer key correct (7k problems, 3 checks) | run on demand |
| `scripts/_validate_content_json.py` | article lesson shape, entity rules | wired into the API build driver |
| `scripts/model-eval/` | AI marking quality bake-off (cases, runner, report) | the closest thing to a real suite we own |
| `scripts/_audit_related_media_urls.py` | dead-link pruning | mandatory build phase |

### 1.2 Written this fortnight, alive only by luck
The two temp directories hold **200+ one-shot scripts, ~40 of them tests in
all but name** (`test_*`, `verify_*`, `walk_*`, `shot_*`). They proved, at
various moments: join-endpoint auth (including the smuggled student_id), class
scoping, review-queue scoping on both roles, password-reset recovery, the fork
banner, year scoping, the full student journeys (picker → content → drill →
surfaces → links), score-reading walks, and eight teacher-platform screens by
render. Every one ran once, passed, and was abandoned — in folders the OS will
eventually clear. **The classes-page regression happened precisely because the
page's proof had no guardian three days later.**

### 1.3 Rescued today
30 of the highest-value harnesses now live in `scripts/tests/_incoming/` —
raw, unrefined, but in git. That is the vanished-factory lesson applied:
never-committed means gone.

---

## 2. The shape of the suite

```
scripts/tests/
  run_tests.py            one command; --fast | --full | --live
  _incoming/              rescued raw material (temporary, drains to rings)
  unit/                   pure functions, no network        (~seconds)
  api/                    endpoint handlers, stubbed auth    (~30s)
  e2e/                    Playwright, APIs route-mocked      (~1-2 min)
  live/                   read-only smoke against production (~1 min, opt-in)
  fixtures/               captured REAL responses (real_progress.json pattern)
```

**Ring 1 — unit.** Pure logic with zero dependencies: `close()` tolerances,
`baseSubject()` slug reduction, join-code validation, `collectUnits()` plan
shapes, the misconception-tag vocabulary check. Milliseconds each; run always.

**Ring 2 — api.** The pattern this fortnight proved: stub `requireTeacher`
via `require.cache`, call the handler as a function, assert on status + body.
Auth refusals, scoping boundaries, membership checks, the smuggled-id case.
Needs a database for some cases — see §4 for the interim rule.

**Ring 3 — e2e (mocked).** Playwright against local pages with
`page.route()` serving captured fixtures — the teacher screens, the join round
trip, the reset flow, pack rendering. Fast, deterministic, no network, and the
only ring that catches "the page renders but is wrong" (identical bars, 7,000px
panels — both real catches this fortnight).

**Ring 4 — live smoke (opt-in).** Read-only walks of production: the five
money journeys (lesson loads, practice answers, join page serves, teacher
classes loads, sign-in door works) plus `servedBy` on one AI mark proving
London. Run before pushes that touch those paths, and after deploys.

**The runner** is a plain Python orchestrator — no framework adoption. It runs
node for `.js`, python for `.py`, prints one PASS/FAIL table, exits non-zero
on any failure. `--fast` = rings 1+2-mocked (~30s). `--full` adds ring 3.
`--live` adds ring 4.

---

## 3. The bug museum (the seeding principle)

Every bug fixed becomes a test that would have caught it, so no bug returns
quietly. The founding exhibits, all from the last two weeks:

1. Join accepts only token identity; smuggled `student_id` ignored *(rescued, working)*
2. Review queue: lessons scoped, not just the dropdown; `lessons_only` fast path scoped; foreign `subject_id` → 403 *(rescued)*
3. Class progress: subject-scoped; zeroes on a practice-format class are legitimate; teacher of another class → 403 *(rescued)*
4. Password reset: recovery session must not bounce to the dashboard; stale errors clear on input *(rescued)*
5. `close(76, 76.392)` passes when the ask says nearest degree *(unit, to write — the repr('76.0') bug)*
6. `baseSubject('geography-edexcel-a')` → 'geography' *(unit, to write)*
7. MC options never prefixed "A." ; `expect` never the correct index *(already enforced in enrich_mc's validator — port to unit ring)*
8. The buildbar guard: an optional element's absence must not kill `load()` *(e2e-mocked)*
9. Warm-up bars: heights must differ when scores differ *(e2e-mocked, the flex bug)*
10. AI feedback: markdown from the marker never renders raw *(e2e-mocked — currently an OPEN bug, WC-5; test lands with the fix)*
11. `servedBy` contains "bedrock" on marking routes *(live ring)*
12. Editor: non-staff see live lessons only *(api ring — the guard that was dead for months)*

---

## 4. The database question (honest bit)

Ring 2's real cases currently run against the **production** database —
read-only or self-cleaning (`__E2E_TEST__` rows). That has worked, but it is
the same "no staging" exposure the review pack already flags, and tonight it
has a new corollary: **when Supabase is down, we cannot even verify.**

Interim rule (now): live-DB tests are read-only or create-then-delete, named
loudly, and skipped automatically when the probe fails — a down database must
read as SKIPPED, not FAILED.

Proper fix (when staging exists): ring 2 points at the staging project via env
var, and the interim rule becomes the exception again. The staging plan is a
separate decision; this suite is designed so pointing it elsewhere is one
variable.

---

## 5. Costs

Rings 1-3: zero — local compute, mocked APIs, no AI calls (fixtures are
captured real responses). Ring 4: fractions of a penny when it touches one AI
mark. CI later: GitHub Actions free tier covers us hundreds of pushes a month.
Net effect on the Claude bill: negative — the suite replaces the re-derivation
I currently do by hand each time.

---

## 6. Phases

| Phase | Work | Effort |
|---|---|---|
| **P0 — rescue** | done today: 30 harnesses + 2 fixtures into `_incoming/` | done |
| **P1 — wire** | DONE 16 Aug: runner + 6 unit tests + 7 promoted API tests, 13/13 green, skip-on-down-DB proven | done |
| **P2 — journeys** | promote the `shot_*`/journey scripts into ring 3 with fixtures; write the five-journey live smoke | an afternoon |
| **P3 — habit** | suite runs before every push that touches api/, js/, or the big pages; failures block the push (my discipline, not tooling) | immediate, free |
| **P4 — CI** | GitHub Action runs `--fast` on every push; graduates to gate once trusted | an hour, later |

**What this deliberately does not do:** adopt a test framework, chase coverage
percentages, or test content (the validators own that). The suite guards
*behaviour* — auth, scoping, money, rendering — the things that broke this
fortnight and the things that would end a school contract if they broke next
term.
