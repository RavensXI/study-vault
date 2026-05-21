# Fact-Check Report: AQA Statistics (statistics-aqa)

**Date:** 2026-05-21
**Lessons checked:** 9
**Fact-checkable claims found:** 14
**Issues found:** HIGH 0 / MEDIUM 2 / LOW 0

---

## Summary

Statistics is a methods-heavy subject with low factual-claim density. Most lessons contain no named-person attributions, no fabricated statistics, and no named-dataset references with specific figures. The two issues found relate to an outdated organisation name and an oversimplification of the ONS Census coverage — both in L3.

---

## Issues Requiring Fixes

### MEDIUM — L3: NHS Digital is a defunct organisation (merged Feb 2023)

**Lesson:** Primary and Secondary Data Sources (L3)
**Claim:** _"organisations such as the Office for National Statistics (ONS), NHS Digital, the Met Office, and the Department for Education all publish large, high-quality datasets"_

NHS Digital merged into NHS England on 1 February 2023. The brand no longer exists. Data previously published under the NHS Digital banner is now published by NHS England (accessible at digital.nhs.uk). Referring to it as "NHS Digital" is out of date.

**Fix:** Replace `NHS Digital` with `NHS England (formerly NHS Digital)` or simply `NHS England`.

---

### MEDIUM — L3: "ONS Census covers the entire UK population" — technically inaccurate

**Lesson:** Primary and Secondary Data Sources (L3)
**Claim:** _"The ONS Census, for example, covers the entire UK population at ten-year intervals"_

The ONS administers the census only for England and Wales. Scotland's census is administered by National Records of Scotland (NRS), and Northern Ireland's by the Northern Ireland Statistics and Research Agency (NISRA). Calling it "the ONS Census" and saying it covers "the entire UK population" conflates three legally separate exercises. At GCSE level this is a minor issue — the spirit of the example is valid — but it could cause a well-informed student to query the lesson.

**Fix:** _"The UK Census covers the entire UK population at ten-year intervals — administered by the ONS for England and Wales, and by equivalent agencies for Scotland and Northern Ireland."_ Or simply remove "ONS" and say "The UK Census".

---

## Lessons With No Issues

| Lesson | Title | Notes |
|--------|-------|-------|
| L1 | Hypotheses, Questions and Investigation Constraints | No named-person or named-dataset claims. All definitional/methodological. |
| L2 | Types of Data and Variables | Standard data-type classifications. No named statisticians or real-world datasets. |
| L4 | Sampling Methods and Stratification | Hypothetical school worked examples only. No real-world statistics cited. |
| L5 | Questionnaires, Pilot Studies and Cleaning Data | Methodological only. No attributions. |
| L9 | The Statistical Enquiry Cycle | PPDAC cycle review. No named statisticians or real data. |

---

## Lessons With Verified Claims (all passed)

### L3 — "Unemployment definition changed multiple times between 1970s and 1990s" — PASS
Well documented. The UK government changed claimant count criteria approximately 30 times since 1979. ILO/Labour Force Survey adopted as headline measure in 2003.

### L6 — Correlation thresholds (strong ≥ 0.6, weak 0.2–0.6, none < 0.2) — PASS
Exact match to AQA GCSE Statistics 8382 specification (Section E8b). "Moderate" correctly excluded.

### L6 — Spearman's rank correlation description — PASS
Accurate. Charles Spearman introduced the coefficient in 1904. It is non-parametric, rank-based, suitable for ordinal data. Description matches AQA spec E9c.

### L6 — Pearson PMCC description ("measures the linear relationship between two quantitative variables") — PASS
Standard GCSE-level language; matches AQA spec framing. Technically Pearson requires continuous/interval-scale data, but "quantitative" is the accepted GCSE terminology.

### L6 — Spearman vs Pearson distinction ("Spearman measures rank orders; Pearson measures linear relationship") — PASS
Direct match to AQA spec notes E9c.

### L7 — Normal distribution 68/95 rule — PASS
Accurate. The empirical rule states ~68% within 1 SD and ~95% within 2 SD. AQA spec E11b confirms this wording.

### L7 — Warning lines (±2 SD) and action lines (±3 SD) in quality control — PASS
Standard Shewhart control chart convention. Confirmed by AQA teaching resources.

### L7 — Positive skew: household income example — PASS
Accurate; consistent with ONS income data showing high-earner distortion of mean.

### L7 — Binomial distribution symmetry claim (p=0.5 symmetric, p≠0.5 skewed) — PASS
Correct mathematical property of the binomial distribution.

### L8 — RPI published monthly by ONS, used for rail fares and benefits — PASS
Accurate. RPI link to rail fares restored in 2025 (temporary cap in 2024 was a government override, not a structural change). Student loan interest also RPI-linked.

### L8 — CPI as Bank of England's target measure for inflation — PASS
Confirmed. Government sets the Bank a 2% CPI target.

### L8 — Birth rate (live births per 1,000 per year) and death rate (deaths per 1,000 per year) — PASS
Standard ONS and WHO definitions. Correct.

---

## Verdict

Two medium-severity issues, both in L3, both involving organisational/coverage accuracy rather than statistical content. Zero fabricated statisticians, zero fabricated formulas, zero invented statistics. The lesson set is reliable for teaching purposes with the two fixes applied.
