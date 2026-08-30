# Free-Tier AI Allowance & Server-Side Budget — Spec

Status: DRAFT for Tom's review (31 Aug 2026). Launch feature, not a retrofit.
Owner file: `api/_lib/budget.js` (new). Companion: per-route telemetry.

## Principles

1. **No ads. Families don't pay.** The allowance keeps both: free users pay
   nothing — AI is generous-but-finite per day instead of unlimited.
2. **Invisible to honest use.** Allowances sit ~3× above heavy real usage.
   No meters, no countdown chips, no gamification. The limit is only ever
   seen by the student who hits it.
3. **Enforced server-side.** Every AI route checks the budget in Supabase
   BEFORE calling Bedrock. Client-side caps (e.g. the exit-ticket cleanup
   counter) become UX conveniences, not controls.
4. **Degrade, never dead-end.** Exhausted marking falls back to
   self-assessment against the model answer; exhausted tutor says when it
   resets. Content, quizzes, flashcards, narration, podcasts, widgets are
   never gated — they cost nothing.
5. **School tier = unlimited** (within a high abuse ceiling). "Unlimited AI
   marking and tutoring" becomes a printed line on the licence sheet.

## Daily allowances (reset midnight Europe/London)

| Route | Signed-in free | Anonymous (no account) | School tier |
|---|---|---|---|
| Quick marks (≤8 marks) | 30 | 10 | unlimited* |
| Exam-tier marks (>8 marks) | 5 | 2 | unlimited* |
| Tutor messages | 15 | 5 | unlimited* |
| Simplify/explain cache misses | 60 | 20 | unlimited* |
| Exit-ticket triage + cleanup | n/a (school feature) | n/a | 1/lesson + 30 cleanups |

\* abuse ceiling 300 AI calls/day/user across all routes; hitting it is a
flag in the telemetry digest, not a student-facing event.

- 30 quick marks = five full lessons' practice in one day. 15 tutor messages
  is a long tutoring session. Nobody honest notices.
- Anonymous users get a working taste, then: "Create a free account for your
  full daily allowance" — the conversion nudge doubles as the abuse guard,
  since IP-keyed budgets are spoofable but account-keyed ones are not.
- Worst-case spend per signed-in free user per day ≈ 36p; realistic
  behaviour unchanged (£1–3/year). The cap's job is the top-1% tail and
  runaway-script scenarios, which it converts into a hard ceiling.

## Enforcement mechanics

- **Table** `ai_usage_daily`: `(subject_key, day, route, count)` with a
  unique composite key. `subject_key` = auth user id when signed in, else
  `anon:` + SHA-256(IP + coarse UA). Raw IPs never stored.
- **Atomic check-and-increment** via one Postgres RPC
  (`consume_ai_budget(subject_key, route, limit)`) so concurrent requests
  can't race past the limit. Returns remaining count.
- **Shared helper** `api/_lib/budget.js` imported by all AI routes; one
  line at the top of each handler:
  `const ok = await consumeBudget(req, 'quick_mark'); if (!ok) return res.status(429).json({budget:'exhausted', resetAt});`
- **Response contract**: HTTP 429 with `{budget:'exhausted', resetAt}`.
  Clients render the graceful fallback (below), never a raw error.
- **Config, not code**: limits live in one `LIMITS` map; a
  `AI_BUDGET_MULTIPLIER` env var scales every limit globally (0.5 halves
  them; 0 disables free-tier AI entirely) — the emergency dial turns
  without a deploy.
- **Fail open on infrastructure error**: if the budget check itself errors,
  the request proceeds and the failure is logged. Students are never
  blocked by our bug; the multiplier exists for genuine emergencies.

## Student-facing copy (only shown on exhaustion)

- Marking: "You've used today's AI marking — it resets at midnight. Compare
  your answer with the model answer yourself: examiners say self-marking is
  one of the best revision habits there is." → reveal mark scheme +
  self-assessment ticks (already exist in the practice UI).
- Tutor: "The tutor's done for today — back at midnight. The Simplify and
  Explain buttons still work on every paragraph."
- Anonymous: same messages, plus one quiet line: "Free accounts get triple
  the daily allowance."

## Telemetry (ships with the feature, not after)

- `ai_usage_daily` doubles as the usage log — no second write path.
- Weekly Resend digest (reuse the audit-email infra): per-route call counts,
  estimated spend by tier (free/anon/school), cache hit rate on simplify,
  count of users hitting any limit, top-10 heaviest subject_keys (hashed).
- The digest is the replacement for this spec's softest assumption (the
  behaviour mix): after two weeks of real data, allowances get re-tuned.

## Rollout

1. Build behind `AI_BUDGET_MULTIPLIER` (unset = enforcement off, telemetry
   still recording). Deploy; watch a fortnight of pure telemetry.
2. Turn enforcement on with the table above. Watch the exhaustion counts —
   target: <0.5% of daily actives ever see a limit message.
3. Fold the exit-ticket cleanup cap into this system when tickets ship;
   delete the localStorage counter.

## Non-goals

- No ads, ever, on any tier (settled; this spec exists to keep it settled).
- No content gating: nothing pre-generated is ever behind the budget.
- No visible meters, streaks, or "upgrade" upsells on the free tier.
- No per-feature pricing. One budget, one dial.
