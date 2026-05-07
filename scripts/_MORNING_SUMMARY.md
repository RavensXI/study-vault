# Poem Audit — Morning Summary (2026-05-08)

## TL;DR

- **168 canonical poems** sourced into `data/canonical_poems/` covering all 4 boards.
- **All 90 English Lit poetry lessons audited** — 1066 quotes extracted, 42 confirmed misquotes flagged across 26 lessons (~4% misquote rate per quote, ~29% of lessons affected).
- **No automatic fixes applied** — fabrications need editorial replacement, not single-word patching.
- **3 lessons need whole-lesson regeneration** (3+ fabrications each).

## Reports for you to read

- **`scripts/_poem_audit_report.md`** (602 lines) — Markdown, grouped by lesson, every confirmed misquote with side-by-side comparison + triage reasoning. Read this first.
- **`scripts/_poem_audit_triaged.json`** — full structured data (178 raw flags categorised).
- **`data/canonical_poems/`** — the new ground-truth store, one .txt per poem. Reusable for future audits, content-gen, etc.

## Confirmed misquotes — top concerns

### Lessons that need whole regeneration (3+ fabrications)

1. **`337d64f7`** — OCR Youth & Age L2 "Growing Up & Change" — **5 fabrications** across Midnight on the Great Western, The Bluebell, Farther (×2), My First Weeks. None of these lines exist in the canonical poems.

2. **`23564a46`** — OCR Love & Relationships L3 "Complicated Love" — **3 fabrications**, including "I shall be your comrade, friend and mate" and "I am no doll to dress and sit for feeble worship" — neither line is in any OCR L&R poem.

3. **`52f7c2a5`** — OCR Youth & Age L8 "Exam Technique & Quotation Bank" — **3 fabrications** carried through from L2 + L6.

### Notable individual fabrications

- **Singh Song! (AQA L&R L4)** — already fixed earlier, but the canonical confirmed: "Toronto plane-Loss" line was fully fabricated; the bride in Nagra's actual poem has "a red crew cut and... a Tartan sari".
- **Winter Swans (AQA L&R L5 + L8)** — "our hands, like swans, / settled after flight" is paraphrased; canonical has "like a pair of wings settling after flight".
- **Remains (AQA P&C)** — "blood-shadow wanders the streets" should be "His blood-shadow stays on the street" (Armitage).
- **War Photographer (Edexcel Conflict L2)** — "reassurance of the viewfinder" should be "reassurance of the frame". (Note: this is Carole Satyamurti's *War Photographer*, NOT Carol Ann Duffy's — different poems, both called *War Photographer*. Edexcel uses Satyamurti's.)
- **The Manhunt (Eduqas, 2 lessons)** — "I'm still / as a cicada shell" — not in Armitage's actual poem.
- **Stewart Island (Edexcel T&P, 2 lessons)** — "a raft of resting shags" and "But for the birds I might have been / the only living creature" — both fabricated; not in Fleur Adcock's poem.
- **Letters from Yorkshire** — "Is it enough to say that what he sees / I see?" — fabricated rhetorical question.

### Earlier fixes confirmed correct

The 4 fixes I applied yesterday have all been verified against the new canonical store:
- Shelley's "moonbeams kiss the **sea**" ✓
- Armitage's "**zero-end**" / "**one-hundredth**" of an inch ✓
- Hardy's "**stick-ends**, charred" ✓

## Why the audit found 113 false-positive attributions

The matcher checked quotes against the lesson's **own cluster only**. ~113 flagged quotes turned out to be canonical quotes from *comparison poems* (poems from OTHER clusters — e.g. an OCR Love & Relationships lesson comparing to Shakespeare's Sonnet 116, or Carol Ann Duffy's Valentine, or Tennyson's Light Brigade). These are correctly used in the lessons; the audit just couldn't see them because they live in a different anthology folder.

A future improvement would be a "global" canonical store covering common comparison poems across boards.

## Why the audit shows 23 false-positive prose

Some quotes my extractor pulled out of `content_html` are actually analytical prose with curly quotes around poem titles (e.g. *Both Sheers in 'Winter Swans' and Hardy in 'Neutral Tones' use pathetic fallacy...*). The triage agent caught these — no action needed.

## Recommended next steps (your call)

1. **Approve the Markdown report** — read it through, agree which fixes are real.
2. **Fix the obvious paraphrases** — Winter Swans, Remains, War Photographer (Satyamurti), Letters from Yorkshire — I can patch + regen narration in ~10 mins per lesson.
3. **Decide on the 3 deep-fabrication lessons** — regen from scratch with canonical text supplied to the agent (per the new pipeline rule we agreed).
4. **Add canonical-text supplied generation as a hard pipeline rule in `docs/CONTENT_PROMPT.md`** — for any English Lit lesson, the agent prompt MUST include the canonical poem text. Without it, agent paraphrases/hallucinates copyrighted modern poems.
5. **Phase 2 (later) — extend audit to drama + prose** — Macbeth, AIC, Jekyll, ACC, novels. Same pipeline, different sources.

## Stats

| Metric | Value |
|---|---|
| Canonical poems sourced | 168 |
| English Lit poetry lessons audited | 90 |
| Quotes extracted | 1066 |
| Raw audit flags (after filters) | 178 |
| Confirmed misquotes (post-triage) | 42 |
| False-positive attributions | 113 |
| False-positive prose | 23 |
| Lessons with ≥1 confirmed misquote | 26 |
| Lessons with ≥3 misquotes (regen recommended) | 3 |
| Auto-applied fixes | 0 (all need your call) |

## Pushed commits

- `7a4e0f2` — earlier session: Shelley/Armitage/Hardy fixes (commit message documents the 4 corrections, plus 2 still flagged for your verification — Singh Song & Alvi)
- `be1fcdb` — this session: full canonical-text store + audit pipeline + triage
