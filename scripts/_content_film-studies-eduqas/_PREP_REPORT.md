# Phase 3 Prep Report — Film Studies (Eduqas C670QS / WJEC 3670QS), free tier

## Scope

28 lessons across 5 units, free tier, dual-board universal (Eduqas C670QS for English centres + WJEC 3670QS for Welsh centres — identical specification, single content body).

| Unit | Lessons | Batches |
|------|---------|---------|
| 1. Film Form and Language | 7 | 2 (3+4) |
| 2. US Mainstream Comparative | 7 | 2 (3+4) |
| 3. US Independent | 6 | 2 (3+3) |
| 4. Global Film | 5 | 1 (5) |
| 5. Developments in Film Technology | 3 | 1 (3) |
| **Total** | **28** | **8** |

## Files written

```
scripts/_content_film-studies-eduqas/
  _AGENT_PROMPT.md                       <- full agent prompt, film-specific
  _PREP_REPORT.md                        <- this file
  _build_batches.py                      <- programmatic batch generator
  _reference_lesson.json                 <- copied from drama-aqa (RE L01 structure)
  _spec_universal.txt                    <- Unit 1 + Unit 5 spec slice
  _spec_set-films.txt                    <- Units 2, 3, 4 spec slice (set-film framework)
  _batch_film-form_b1.json               <- Unit 1 lessons 1-3
  _batch_film-form_b2.json               <- Unit 1 lessons 4-7
  _batch_us-mainstream_b1.json           <- Unit 2 lessons 1-3 (institutional + Dracula/Lost Boys + Singin/Grease)
  _batch_us-mainstream_b2.json           <- Unit 2 lessons 4-7 (Pillow/Harry + Rebel/Ferris + Body Snatchers/E.T. + comparative method)
  _batch_us-indie_b1.json                <- Unit 3 lessons 1-3 (overview + Juno + Whiplash)
  _batch_us-indie_b2.json                <- Unit 3 lessons 4-6 (Lady Bird + Hurt Locker/Hate U Give + specialist writing)
  _batch_global-film_b1.json             <- Unit 4 all 5 lessons
  _batch_developments_b1.json            <- Unit 5 all 3 lessons
  lessons/                               <- empty; agents write here
```

## Slug verification

All 28 lesson slugs pre-confirmed against Supabase:
```
SELECT lessons.slug FROM lessons
JOIN units ON units.id = lessons.unit_id
JOIN subjects ON subjects.id = units.subject_id
WHERE subjects.slug = 'film-studies-eduqas';
```
No drift between plan slugs and Supabase rows. The activation step (Phase 2) seeded the rows with these exact slugs.

## Question types

7 registered question types — all 7 are valid in every unit.

```
1 mark — Identify
2 marks — Define
5 marks — Explain Effect
8 marks — Analyse Filmic Element
10 marks — Micro-Analysis
15 marks — Compare and Contrast
25 marks — Extended Essay
```

Per-unit weighting (see `_AGENT_PROMPT.md`):
- Unit 1 — short forms (recall + define + explain effect + analyse filmic element)
- Unit 2 — comparative-and-contrast is the unit signature; one 25-mark per set-film lesson
- Unit 3 — extended essay is the unit signature; one 25-mark per set-film lesson
- Unit 4 — balanced; 10-mark micro-analysis + 25-mark extended essay
- Unit 5 — short factual forms only; no 25-mark

## Set-film briefs

Substantive briefs in `unit_level_teaching_brief.set_films_covered` for every set-film lesson:

| Unit 2 lesson | Set films | Brief covers |
|---------------|-----------|--------------|
| L2 | Dracula (1931), The Lost Boys (1987) | synopsis, director/year/country, characters, themes, production context, critical reception, filmic methods, 5 named scenes, theory, copyright |
| L3 | Singin' in the Rain (1952), Grease (1978) | as above |
| L4 | Pillow Talk (1959), When Harry Met Sally (1989) | as above |
| L5 | Rebel Without a Cause (1955), Ferris Bueller's Day Off (1986) | as above |
| L6 | Invasion of the Body Snatchers (1956), E.T. (1982) | as above |

| Unit 3 lesson | Set films | Brief covers |
|---------------|-----------|--------------|
| L2 | Juno (2007) | full brief |
| L3 | Whiplash (2014) | full brief |
| L4 | Lady Bird (2017) | full brief |
| L5 | The Hurt Locker (2008), The Hate U Give (2018) | full brief for each |
| L6 | Specialist writing — generic | skill brief, no rotating sources named |

| Unit 4 lesson | Set films | Brief covers |
|---------------|-----------|--------------|
| L1 | All 5 global English-language as overview | per-film capsule |
| L2 | Slumdog Millionaire (2008) | full brief |
| L3 | All 5 global non-English overview | per-film capsule |
| L4 | Wadjda (2012), Girlhood (2014) | full brief for each |
| L5 | All 5 contemporary UK as overview | per-film capsule |

Research source discipline: factual-only (BFI, Britannica, Wikipedia, IMDb-level facts). NO copyrighted dialogue. NO plot reproduction beyond 1-3 sentence concept-only synopsis. NO ingestion of Eduqas/WJEC mark schemes, examiner reports beyond general findings, or third-party study guides.

Total web-search budget used: 0 (sufficient public knowledge from production-fact-level training data without needing additional retrieval; if agent finds a fact ambiguous it should mark it with TODO rather than fabricate).

## Copyright discipline (baked in)

All 18 distinct set films treated as IN COPYRIGHT in the UK (the earliest, Dracula 1931, has UK copyright until 2033 under the 70-years-after-author's-death rule for Tod Browning). Hard rules:

- Max 15 words quoted from any film, max once per lesson, in quotation marks
- NO plot reproduction beyond named-sequence labels
- NO reproduction of critical interpretations from Eduqas/WJEC material, secure-website sources, or third-party study guides
- NO board codes (C670QS, 3670QS), component codes (Component 1/2/3), or section letters (Section A/B/C) in user-facing strings
- NO real-production references for the Unit 3 specialist-writing lesson — generic skill teaching only
- Mark scheme rubric: StudyVault Mastering / Secure / Developing / Emerging — no Level 1-4, no "Award N marks for", no "Nothing worthy of credit"

The validator at `scripts/_validate_content_json.py` already enforces several of these. The agent prompt restates them explicitly.

## Dispatch command pattern

Eight batches, six-agent waves to stay inside throttling. Suggested dispatch:

**Wave 1** (run six in parallel):
```
batch_id=film-form_b1
batch_id=film-form_b2
batch_id=us-mainstream_b1
batch_id=us-mainstream_b2
batch_id=us-indie_b1
batch_id=us-indie_b2
```

**Wave 2** (run remaining two in parallel after Wave 1 completes):
```
batch_id=global-film_b1
batch_id=developments_b1
```

Each agent invocation runs the prompt at `scripts/_content_film-studies-eduqas/_AGENT_PROMPT.md` against `scripts/_content_film-studies-eduqas/_batch_{batch_id}.json` and writes to `scripts/_content_film-studies-eduqas/lessons/{lesson_slug}.json`. Agent returns the standard `BATCH_DONE: ...` status line.

After all 8 batches complete, run the existing pipeline validator + insertion script (parallel to drama-aqa's flow):
```
python scripts/_validate_content_json.py scripts/_content_film-studies-eduqas/lessons
python scripts/_insert_content_to_supabase.py film-studies-eduqas
```

## Validation summary

- 8 batch JSONs written, all valid JSON, all parse cleanly
- 2 spec slices, both non-empty (~140 + ~150 lines)
- 1 reference lesson copied (RE L01 from drama-aqa)
- 1 agent prompt written, film-specific
- 28 lesson slugs across batches match Supabase exactly (no missing, no extra)
- Slug counts: 3+4+3+4+3+3+5+3 = 28
- film_content_rules block carried in every batch's subject_level_teaching_brief
- No copyrighted dialogue in any batch JSON
- No paper codes / section letters in user-facing strings (the do_not_use list inside studyvault_mark_scheme_rules is metadata, not user-facing — agents read it as a ban list)
