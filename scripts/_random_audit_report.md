# Random Fact-Check Audit — Platform-Wide Sanity Check

60 lessons sampled at random across non-English-Lit subjects, audited via web-search-verified Sonnet agents (~9 in parallel, one per subject group).

## Headline numbers

| Subject group | Lessons sampled | HIGH | MED | LOW | Total |
|---|---|---|---|---|---|
| History (AQA + Edexcel) | 12 | 0 | 3 | 3 | 6 |
| Science (combined + separate) | 10 | 0 | 3 | 2 | 5 |
| Business (3 boards) | 6 | **3** | 2 | 6 | 11 |
| Geography (5 boards) | 8 | **2** | 3 | 3 | 8 |
| RE/RS | 6 | 1 | 1 | 3 | 5 |
| Drama / Film | 4 | 1 | 0 | 5 | 6 |
| PE (AQA + OCR) | 4 | 1 | 2 | 3 | 6 |
| CS / D&T | 4 | 0 | 2 | 2 | 4 |
| Other (Music/Food/HSC/Citizenship/Hospitality) | 6 | 1 | 0 | 3 | 4 |
| **Total** | **60** | **9** | **16** | **30** | **55** |

**HIGH-severity rate: 9/60 = 15%** (vs prose audit's ~20% high rate).

Extrapolating to the ~1,800 non-English-Lit lessons → **~270 estimated platform-wide HIGH-severity issues**. Significant but **far less concentrated than English Lit**, where some texts had 50%+ of lessons flagged.

## What kind of HIGH-severity issues these are

Most "high" findings fall into one of three categories:

### 1. Stale facts (4 of 9 highs)

- **Citizenship — Parliament**: 92 hereditary peers presented as live fact. Removed by the **House of Lords (Hereditary Peers) Act 2026** (29 April 2026 — last week).
- **Business — JLP bonus**: described as paid annually "when in profit". Actually discretionary; declined in 2021, 2023, 2024 (incl. after returning to £56m profit).
- **Business — Burberry margins**: 15-20% net margin cited as luxury benchmark. Was true 2019-21; FY23/24 was ~0% with operating losses.
- **Business — UK minimum wage**: £11.44 stated as 2024-25; from April 2025 it's £12.21.

These are **drift from when written**, not fabrications. Pattern: any lesson citing current statistics, named legislation, or specific corporate facts will go stale within 1-3 years. Worth a separate "stale-fact sweep" annually.

### 2. Stat fabrications (3 of 9)

- **Business — Nissan Sunderland**: "a car every 67 seconds" — actual rate is one every ~120 seconds (~45% too fast). No source.
- **Geography — Manchester 2021 census**: "33% born outside UK" attributed to census — actual figure is **31.4%**. Misattributed-to-source error.
- **PE — Mo Farah resting HR**: "low 40s" — multiple sources put it at **~33 bpm**. 8-10 bpm error on a famous named example.

### 3. Wrong attribution (2 of 9)

- **Drama AQA Romeo and Juliet L7**: cites "Frantic Assembly's 2008 production" of R&J — they staged **Othello** in 2008. Frantic Assembly have no R&J production.
- **RE — Abortion & Euthanasia (Islam)**: Qur'an 6:2 cited for "Allah breathes a soul" — that verse is about clay creation only; the soul-breathing reference is **Qur'an 15:29 / 32:9 / 38:72**.

## Subject quality ranking (best → worst)

1. **History** — 0 highs across 12 lessons; 7/12 lessons completely clean. Best result. Strong on names, dates, treaties.
2. **Science** — 0 highs across 10; 5/10 clean. Mostly good; minor teaching-simplification flags (K/Na density anomaly, 7-rank Linnaeus).
3. **CS / D&T** — 0 highs across 4. Programming + data-structure facts solid.
4. **Other (Music/Food/HSC/Citizenship)** — 1 stale-fact high (hereditary peers); 26 specific claims verified clean.
5. **RE/RS** — 1 high (wrong Qur'an verse attribution); 30+ scripture/scholar attributions clean.
6. **Drama/Film** — 1 high (Frantic Assembly misattribution); set-text content otherwise solid.
7. **PE** — 1 high (Mo Farah HR); spec-aligned simplifications elsewhere.
8. **Geography** — 2 highs (tar-sands production rate + Manchester census stat); plus stale UK population, BBC MediaCityUK year.
9. **Business** — **3 highs** (Nissan rate, JLP bonus rule, Burberry margins). Worst subject. Pattern: business case studies decay fast.

## Recommendations

1. **Don't panic about non-Eng-Lit content quality**. The 15% high-severity rate is meaningful but most issues are stale data or peripheral attributions, not the deep "wrong text being taught" or "fabricated quote" issues that dominated English Lit.

2. **Annual stale-fact sweep**. Statistics, named legislation, current case studies, and corporate facts decay within 1-3 years. A simple agent that re-checks numerical claims and "current" framings annually would catch most of these.

3. **Apply the 9 specific high-severity fixes immediately** (Citizenship hereditary peers + Business × 3 + Geography × 2 + Drama R&J + RE Qur'an + PE Mo Farah). These are cheap one-line edits.

4. **Business case studies are the riskiest subject going forward** — both for fabrications and for stale data. Worth tighter curation when generating future business content.

5. **Pipeline rule for new content**: any lesson citing a specific named statistic should include a date stamp ("as of 2024") so future students know to check currency.

## Audit data

- Per-subject findings: `scripts/_random_audit/{group}.json`
- Sample list: `scripts/_random_audit_sample.json`
