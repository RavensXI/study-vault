# Subject Roadmap

*Last updated: 28 May 2026*

Live counts in this doc are point-in-time snapshots. For an authoritative current view, query Supabase or run `python scripts/_audit_subject_status.py`.

## Unity College — Bespoke (~19 subjects, ~535 lessons)

| Subject | Exam Board | Lessons | Units | Notes |
|---------|-----------|---------|-------|-------|
| History | AQA | 60 | 4 | QA'd, fact-check pass May 2026 |
| Business Studies | Edexcel 1BS0 | 30 | 2 themes | |
| Geography | AQA 8035 | 54 | 3 (incl. Skills practice unit) | |
| Sport Science | OCR R180 | 10 | 1 | |
| Drama | OCR J316 | 12 | 2 (Blood Brothers, Rise Up) | |
| Food Prep & Nutrition | AQA 8585 | 10 | 1 | |
| Religious Studies | AQA 8062 | 40 | 8 | |
| Music | Eduqas C660U | 26 | 6 | |
| English Literature | AQA 8702 | 42 | 5 | |
| English Language | AQA 8700 | 30 | 4 | Practice-first |
| Combined Science | AQA 8464 | 48 + 15 practice | 6 + 3 practice | |
| Separate Sciences | AQA 8461/2/3 | 22 + 6 practice | 3 + 1 | |
| Spanish / German / French | AQA | 26 each | 3 each | Practice-first |
| Creative iMedia | OCR J834 | 23 | 4 | |
| Computer Science | OCR J277 | 23 | 2 | |
| Design & Technology | AQA 8552 | 20 | 3 | |
| Mathematics | Edexcel 1MA1 | 48 | 6 | Practice-first. Subscribed from generic. |
| Music Technology | NCFE | 15 | 5 | **Remove Sept 2026** — last year taught. |

## Severn Vale School — Bespoke + Subscribed (~48 lessons)

| Subject | Exam Board | Lessons | Notes |
|---------|-----------|---------|-------|
| Combined Science — Biology (bespoke) | AQA 8464 | 16 | Built from teacher PPTs |
| + Chemistry & Physics (subscribed) | AQA 8464 | 32 | Re-slugged `science-severnvale` 27 May to clear cross-school slug clash with Unity |

## Free Tier (school_id NULL, generic content)

**72 live free-tier subjects, ~3,823 lessons** across all major boards. Detail table below; for a current snapshot use Supabase.

### Core multi-board subjects

| Subject | AQA | Edexcel | OCR | Eduqas | Total |
|---------|-----|---------|-----|--------|-------|
| English Language | 30 | 50 | 50 | 50 | 180 |
| English Literature | 214 | 215 | 156 | 190 | 775 |
| Mathematics | 48 | 48 | 48 | 48 | 192 |
| Combined Science | 85 | 63 | 63 (+63 J260 OCR-B) | — | 274 |
| Separate Sciences | 69 | 71 | 72 (+74 J260 OCR-B) | — | 286 |
| History | 210 | 202 | 117 | 167 | 696 |
| Geography | 52 | 40 (A) + 40 (B) | 32 | 44 | 208 |
| Religious Studies | 74 | 71 | — | 53 | 198 |
| Business | 30 | 30 | 30 | — | 90 |
| Computer Science | 26 | 26 | 23 | 29 | 104 |
| Physical Education | 33 | 30 | 27 | — | 90 |
| Health & Social Care | — | 12 | 13 | 13 | 38 |
| Sociology | 33 | — | — | 33 | 66 |
| French / German / Spanish | 26 each | 27 each | — | — | 159 |

### Single-board / niche generic subjects

| Subject | Board | Lessons | Built |
|---------|-------|---------|-------|
| Astronomy | Edexcel | 26 | ✓ |
| Cambridge Nationals — Enterprise & Marketing | OCR | 12 | ✓ |
| Cambridge Nationals — Sport Studies | OCR | 10 | ✓ |
| Citizenship | AQA | 29 | ✓ |
| Design & Technology | AQA / Eduqas | 20 / 22 | ✓ |
| Drama | AQA | 85 | ✓ |
| Electronics | Eduqas | 20 | ✓ |
| Engineering | AQA / Eduqas | 22 / 14 | ✓ |
| Film Studies | Eduqas | 44 | ✓ |
| Food Prep & Nutrition | Eduqas | 16 | ✓ |
| Geology | Eduqas | 30 | ✓ |
| Hospitality & Catering | Eduqas / WJEC | 10 | ✓ |
| IT | OCR (J836) | 12 | ✓ |
| Media Studies | AQA | 20 | ✓ |
| Music Technology | NCFE | 15 | ✓ |
| **Psychology** | AQA | 32 | ✓ *(28 May 2026)* |
| Statistics | AQA | 28 | ✓ |

## Coverage gaps still worth filling

These are spec codes where we have one board but could add others, ranked by exam-entry volume. Run `admin/build-status.html` for the current authoritative ranking.

### High value
- Psychology — Edexcel (2nd-largest entries after AQA)
- Sociology — Edexcel, OCR
- Media Studies — Eduqas, OCR
- Geography — additional board variants where market share justifies (currently all 4 boards covered, but Edexcel B is split A/B)

### Medium value
- Music — OCR (rare entries), Edexcel (rare). Music is small-entry overall.
- Drama — Edexcel, Eduqas, OCR (currently AQA only)
- Engineering — OCR (entry volumes lower than AQA / Eduqas)
- D&T — Edexcel, OCR (small entry counts)

### Lower priority / market saturation
- Latin, Classical Greek, Ancient History — very low UK entries (under 10k each)
- Hebrew, Yiddish, etc. — sub-1k entries

## Coursework-only specs — explicitly NOT built

Excluded from the picker and from `admin/build-status.html` via the `EXCLUDED_FAMILIES` map (not just SKIP-tagged). See [[feedback_coursework_only_specs_excluded]] in memory.

- Art & Design (any spec)
- Photography
- Dance
- L1/2 Performing Arts (Pearson 5289QA — 100% coursework)

Specs with high NEA but at least one written exam (Drama, Music, D&T, Food Prep) **stay** in the build list and are built.

## Notes on staleness

This doc was last seriously rewritten 28 May 2026 (the previous version dated 5 April 2026 had drifted by ~3 months of builds — Drama, Media Studies, Sociology, PE, Engineering, Geology, Film Studies, Statistics, Citizenship, Cambridge Nationals, Health & Social Care variants, Psychology, History OCR/Eduqas, and many others all built in the intervening period). When this drifts again, the source of truth is Supabase + `admin/build-status.html`.
