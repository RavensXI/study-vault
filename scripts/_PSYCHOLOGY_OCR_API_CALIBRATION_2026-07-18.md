# Psychology OCR (J203) — First API-Built Subject: Cost Calibration

**Built 18 July 2026** entirely through the Anthropic **API** (not the Claude Code
subscription) via a new deterministic Batch-API driver
(`scripts/api_build/driver.py`). This is the calibration datapoint for costing the
remaining pipeline on Commercial-Terms API access.

Subject is **live**, 31 lessons across 7 units at `pending_review`. Full assets:
heroes (31/31, all index-reused — £0), 8 revision guides, related media
(URL-audited), narration (Azure), wizard wired as a 2-board subject. Verifier: **PASS**.

---

## What it cost (Anthropic API, this run)

Total **$35.63 (~£28)**. Per-stage:

| Stage | Calls | Cost | Notes |
|---|---|---|---|
| Plan (Opus + web search) | 2 | $7.53 | One call was wasted — a parse bug lost the reply before I saved it. Fixed. A clean plan is ~$3.8. |
| Content (Sonnet 5, batch) | 31 | $2.97 | First pass; truncated on 23/31 (adaptive thinking eats the output cap). |
| Content-fix | 41 | $3.31 | Churn from that truncation — **eliminated** by raising the cap to 32k. |
| Guides (adapt from AQA) | 28 | $0.84 | 7 technique pages rewritten to OCR topics + index passthrough. |
| Fact-check (Opus + web search) | 31 | $6.37 | Legitimate and load-bearing — see below. |
| Apply fixes | 10 | $0.47 | Surgical corrections to 10 flagged lessons. |
| Media (curation) | 48 | $13.94 | **$11.94 of this was one bad idea** — see below. |
| **Total** | | **$35.63** | |

Prompt caching worked: 28/31 content requests read the shared 50k-token prefix at
0.1× price; the fact-check and media stages read 3M and 35M cached tokens
respectively. Batch API gave the flat 50% discount throughout.

## The two expensive mistakes (both now fixed in the driver)

1. **Media over-verification — $11.94.** I first gave the media agent `web_fetch`
   to verify every URL itself. It ran enormous loops (dozens of fetch +
   code-execution rounds per lesson), burned ~15k output tokens each, and *still*
   only produced usable output for 14/31 (the rest hit the token cap mid-JSON).
   Replaced with **web_search-only** curation ($1.99 for the re-run) feeding the
   **zero-cost** Python URL auditor (`_audit_related_media_urls.py`), which is the
   mandatory Phase-5 step anyway. The auditor found 58 dead links (25% — bang on
   the historical rate), I pruned them and backfilled 4 short lessons from a
   hand-verified canonical pool. **Net lesson: never pay a model to verify URLs.**

2. **Content truncation — $3.31 of avoidable churn.** Sonnet 5's adaptive thinking
   bills ~10-14k tokens against `max_tokens` *before* the lesson JSON, so a 16k cap
   truncated most lessons. Raised to 32k; a clean run writes every lesson first try.

## What a clean *second* board (Edexcel 1PS0) will cost

Removing the wasted plan call, the truncation churn, and the media-heavy loop:

| Stage | Projected |
|---|---|
| Plan | ~$3.8 |
| Content (32k cap, one pass + light fix) | ~$4.5 |
| Guides | ~$0.8 |
| Fact-check | ~$6.4 |
| Apply fixes | ~$0.5 |
| Media (search-only) | ~$2.0 |
| Warmup | ~$0.2 |
| **Anthropic API total** | **~$18–22 (£14–17)** |

Plus **~$4 Azure** narration (separate account, pay-as-you-go) and **£0 heroes**
(index reuse). Podcasts are Tom/NLM, later, free.

**So: the first board cost £28 including all the learning; the second should cost
~£15–17 all-in.** Both are inside a single $100 top-up. One board ≈ one school
licence's worth of a whole year's generation.

## Why the fact-check spend is worth it (21 HIGH findings)

The Opus fact-check caught real, mark-affecting fabrications a student would have
revised and lost marks on:

- **Eysenck's psychoticism** wrongly attributed to "an overactive dopamine system"
  (correct: high testosterone / low serotonin) — appeared in content, a key-fact,
  a glossary term, a flashcard, a knowledge-check *and* a mark scheme. Six spots,
  one wrong idea.
- **Blackwell et al. (2007)** fixed-mindset result stated as a *decline* (correct:
  a flat trajectory).
- **Kessler/WHO mental-health statistic** given as 50%-by-15 / 75%-by-18 (correct:
  50%-by-14 / 75%-by-24).
- **NatCen 2011 riots study** narrowed to "Tottenham" (correct: multi-area England).
- **OCR's fourth sampling method** (snowball) dropped entirely.

I rejected 2 of the checker's HIGH findings as false positives — it judged the
OCR 13-mark essay against AQA's 9-mark tariff. The driver now feeds the checker
the target board's tariffs so that can't recur.

## Driver design notes (for reuse)

- Deterministic stage pipeline; the **driver holds all Supabase keys** — agents are
  single-shot and never touch the DB (the safety upgrade after the mojibake incident).
- Every response's usage is ledgered to `costs.jsonl`; `driver.py costs` prints the
  table above. Batch collection is idempotent (no double-ledgering on re-poll).
- Resumable per stage via the run dir; state in `state.json`.
- Config-driven (`config_psychology-ocr.json`) — a second board is a new config
  pointing at the same AQA source plan + catalogue + reference lesson.
