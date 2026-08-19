# Bespoke-widget pipeline — canary findings (19 Aug)

Two units through four tiers on the real API: science-aqa physics-paper-1
(11 lessons) and history-aqa elizabethan-england (14).

**Spend: $7.81 of the $25.08 budget.** Every figure below is measured
token usage, not an estimate.

## Does the verification idea work? Yes — with caveats.

The adversarial gate caught a genuine, subtle pedagogical fault on the
first widget it examined. `energy-store-scaler` exposed height and speed
as independent sliders while summing KE + GPE into one "total" readout —
coherent-looking, and wrong in the way that teaches a misconception. No
syntax check or fact lookup would have found that; it needed a model
reasoning about what the interaction implies. That is the strongest
evidence for Tom's proposal.

The second widget (`match-the-minister`) passed 409 property assertions
and the fact-check, with two low-severity code-tidiness notes.

**But the gate has its own error rate.** 150 of 1,560 assertions on
widget 1 "failed" because the GENERATED TEST called `caption(params)`
when the contract is `caption(p, d)` — a broken test, not a broken
widget. A gate that cries wolf is nearly as expensive as no gate. Fix:
put exact function signatures in the test-generator prompt, and treat
"test threw" differently from "invariant violated".

Also checked by hand: the widget uses g = 10 N/kg, which matches this
lesson's own wording. (Whether the lesson should say 9.8 to match AQA's
data sheet is a separate content question — flagged, not touched.)

## Real economics, per delivered widget

| Tier | Model | Cost each | Note |
|---|---|---|---|
| 1 triage | Haiku 4.5 | $0.003 | per lesson scanned |
| 2 spec + invariants | Sonnet 5 | $0.082 | per candidate |
| 3 build | Opus 5 | $0.68 | per successful build |
| 4 gate | Sonnet 5 | $0.23 | testgen + fact-check |

With one fix-cycle on roughly half of them: **~$1.45 per finished
widget.** Full corpus at the observed 92% hit rate ≈ **$5,400**; at a
sensible ~45% hit rate ≈ **$2,600**. My earlier "~$700" estimate was low
by 4-7x: I under-counted Opus output (thinking tokens are billed), and
ignored both the gate and rebuild cycles.

## Three things to fix before any fleet run

1. **The contract is strangling the variety — this is the big one.**
   Haiku chose genuinely varied verbs (match-pairs, sort-into-groups,
   choose-a-path, annotate-the-picture, build-to-a-spec). Sonnet then
   returned `kind: "explore"` for EVERY one, because the contract only
   offers sliders+canvas or a stepper. Bespoke generation cannot deliver
   freshness while the host only knows one shape. Needs first-class
   drag-to-order, drag-to-group, pair-matching, click-to-annotate and
   hit-the-target hosts before scaling.
2. **Triage says yes to 92%** (23/25). That is a rubber stamp, not a
   filter. Make Haiku name the specific idea and reject decoration;
   target 40-50%.
3. **Token budgets.** At max_tokens 8000 every Opus build hit the cap:
   three returned empty text, three returned code truncated mid-
   statement, $4 burned for nothing. Thinking is billed and eats the
   budget silently. Builds need ~24k and streaming (the API refuses
   long non-streaming calls); Sonnet specs need 8k+. A syntax gate now
   rejects truncated builds so they can never reach a lesson.

## Verdict

Viable, and the verification story holds up better than I argued. But
not ready to fleet: fix the host shapes first, or you will pay ~$2,600
to generate 1,800 variations of the same slider.
