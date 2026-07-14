# Maths Practice Audit — Edexcel (overnight run, 15 July 2026)

Tom's brief: "the maths practice is probably the weakest part of the site — audit it,
flag problems, think about best-practice maths teaching, implement solutions."
Scope agreed: Edexcel only (48 lessons, 960 problems), live edits allowed,
multi-agent workflows approved. His concrete complaint: **the feedback often
described a mistake he hadn't made.**

## What ran

1. **Audit workflow** — 48 agents (one per lesson), each independently solving all
   ~20 of its problems before comparing with stored answers, judging tier
   progression, flagging quality issues, and computing the exact wrong answer each
   listed misconception would produce (`expect`). Every disputed solution then went
   to **two independent solver agents**; only unanimous disputes counted.
   136 agents, ~5.4M tokens.
2. **Repair workflow** — 15 problems whose *questions* were mis-posed (stored
   answer doesn't solve them) each got a minimal-edit repair agent + a fresh-solve
   checker. 31 agents.

## Findings

| | |
|---|---|
| Problems audited | 960 (bronze 384 / silver 336 / gold 240) |
| **Solutions confirmed wrong** | **35 (3.6%)** — every one silently marked students wrong for being right |
| Auditor disputes rejected by verification | 9 (the two-solver layer earned its keep) |
| Quality issues filed | 243 — bad misconception message 89 · ambiguous wording 52 · degenerate 44 · duplicate 36 · display error 15 · off-topic 7 |
| Tier progression | 36 good · 12 "mixed" (some genuine step-up, some relabelled difficulty) |
| Misconceptions enriched with `expect` | 1,085 live |

Error archetypes: premature-rounding chains (cosine rule answers off by degrees),
arithmetic slips (hemisphere volume off by exactly 1.0), and a systematic authoring
failure in algebra-L09/L10 where **simultaneous-equation problems were generated with
solutions that don't solve them** (checked one equation only). One problem was
geometrically impossible (hypotenuse 2x with legs x and x+7 forces the "hypotenuse"
shorter than a leg's requirement — repaired to x√5, keeping x=7).

## What was fixed (all LIVE in Supabase)

- **20 wrong solutions corrected** in place (unanimously verified values).
- **15 mis-posed problems repaired** with minimal edits that make the intended clean
  answer correct (e.g. `5(2x−3)=3(x+4)` → `3(x+2)` so x=3 works; every repair
  re-solved from scratch by an independent checker). Each repaired problem got
  fresh misconceptions with computed expects.
- **1,085 misconceptions now carry `expect`** — the exact wrong answer that error
  produces for that problem.

## Player changes (commit de478f02)

- **Honest diagnosis:** feedback names a misconception ONLY when the student's
  actual answer matches its expected wrong answer (`expect`, or the legacy
  `equals_X` check names the content always carried but the player ignored).
  No match → "compare your working with the method steps, line by line" — guidance,
  never a guessed diagnosis. This is the direct fix for Tom's complaint.
- **Worked-example nudge:** two wrong in a row offers one-click entry to the
  Learn view's worked examples (worked-example-first is the evidence-backed ladder;
  this is the lightest way to route strugglers to it mid-session).
- **Per-day seeded shuffle** within each tier: returning students no longer meet
  the identical questions in the identical order every session.

## Rollback

Pre-change state of all 48 lessons: `scratchpad/_maths_edexcel_practice.json`.
Full provenance: `scratchpad/_maths_audit/` (audit result, enrich files, repair
files, apply logs).

## Not done yet (next batches, in order of value)

1. **Triage the 243 quality issues** — the 44 degenerate + 36 duplicate are
   mechanical rewrites (workflow-shaped); the 52 ambiguous need wording surgery;
   89 bad-message issues partly superseded by enrichment.
2. **Port the whole pattern to AQA / OCR / Eduqas maths** (same pipeline, ~3× the
   volume) once Tom is happy with the Edexcel shape.
3. **Session pedagogy, phase 2:** current session = whole bank, linear. Consider
   capped sessions (~10 problems) mixing new tier + retrieval of previous misses,
   and surfacing the method card on first wrong rather than only via nudge.
4. **Sync practice attempt history to accounts** (localStorage per-lesson history
   already exists) so the teacher dashboard sees practice-first subjects.
5. English/language practice audits (Tom flagged those too).
