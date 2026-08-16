# Overnight log — 16 Aug 2026: Music Eduqas build (task #57)

Plan: `EDUQAS_BUILD_PLAN.md`. Decisions locked with Tom before bed:
Eduqas first; no Unity porting (Unity later subscribes to THIS build and
overrides its old music); audio hierarchy = verified library → honest
synthesis (Badinerie excerpts synthesised from the PD score) → Flow only
where machine-ear-verifiable → official YouTube embeds. Everything lands
pending_review; podcasts/explainers after Tom's flip.

## Done

- **Phase 1 — activation** (eduqas_activate.py): subject `music-eduqas`
  (school_id NULL, live, C660QS) + 8 units with accents/subtitles/body
  classes + AQA's music quote ticker + practice_units set. Verified: 8
  units created.
- **Phase 2 — skills copies** (eduqas_copy_skills.py): listening-skills
  (3) + score-reading (4) copied from music-aqa with the neutral-phrasing
  pass — 12 "Section A" references neutralised to listening-exam wording,
  prose verified board-name-free (URL slugs excluded from the check: they
  legitimately contain 'aqa'). Cross-subject R2 audio confirmed serving
  (HTTP 200 with a browser UA; R2 403s bare urllib — known). Lessons
  pending_review.
- Tooling note: two rounds lost to heredoc/inline-patch quoting again —
  switched to the Edit tool mid-phase. The standing rule stands.

- **Phase 3 — drills copied** (eduqas_copy_drills.py, 55eeca40):
  forms-devices-listening (8) + ensemble-film-pop-listening (3). The
  board-name check caught a REAL leak in the music-aqa SOURCE ("directly
  tested in AQA listening questions") — three source lessons cleaned
  (western-classical L5, aos-listening L2+L3). Copier made resume-safe
  after a partial first run. Cross-board AoS numbering in the three
  listening titles retitled to this spec's structure. QA gate 0 errors;
  remnant sweep across all 18 practice lessons: zero Section A, zero
  board names. TODO (suite): add a board-name check to
  _qa_practice_data.py — it missed the source leak.
- **Forms-question additions DONE** (eduqas_forms_questions.py, on Tom's
  morning go-ahead): 12 questions across the 8 forms-devices-listening
  drills. The copied AQA banks already named the obvious forms (rondo L3,
  variations L4, ternary L7), so the additions cover what the Eduqas spec
  needs on top: minuet and trio (L1), strophic rejection (L5), through-
  composed (L8), ornamented repetition + coda (L6), rondo-vs-ternary and
  variations-vs-rondo proof questions (L3/L4), ternary principle +
  sequence devices (L2/L7), refrain recurrence (L8). Every question
  carries per-distractor misconception diagnoses. QA gate re-run: 0
  errors, no new warnings. Backup
  `_backup_forms_questions_2026-08-16.json`.

- **Phase 4 — 14 article lessons BUILT** (eduqas_build_articles.py,
  ~$2.80 total incl. retries): validated per lesson (counts, KC shape,
  plain-text purity, sequential narration ids, board-name ban) and
  inserted pending_review; drafts in _eduqas_drafts/. Two validator
  lessons learned en route: the spec slices carried WJEC page furniture
  the model echoed (slices now sanitised), and "Section A" is legitimate
  MUSICAL terminology in forms lessons — the ban is now scoped to paper-
  structure phrasing only. Study-piece embeds woven (Netherlands Bach
  Society Badinerie; TotoVEVO Africa — both oEmbed-verified). Full
  verification: 14 articles, all pending_review, zero markers, zero
  board names, zero paper-structure phrases. Spot-reads (Africa L3,
  Badinerie L3): factually sound, no lyrics.

- **Phase 5 — fact-check APPLIED** (4 parallel agent passes; findings in
  `scripts/_fact_check/music-eduqas.json` + `.md`): 20 findings — 12 HIGH /
  7 MEDIUM / 1 LOW; aos3-film-music clean. Headlines: the Badinerie key
  scheme was REVERSED (Section A ends in F sharp minor, the dominant minor
  — not D major) across aos1 L3+L4 all fields; Africa is a half-time FEEL
  with straight sixteenths, not a half-time shuffle (that is Rosanna);
  kalimba intro = layered Yamaha GS-1 + real marimba; solo synth CS-80 not
  GX-1; dagga/tilli name the dhol STICKS; Eine kleine 2nd mvt is a rondo —
  ternary example swapped to Chopin's Raindrop Prelude; So What call,
  Sweeney Todd menace, A Little Priest corrected. All applied via
  `eduqas_factcheck_fixes.py` (backup `_backup_factcheck_fixes_2026-08-16
  .json`); one generic replace briefly produced "groove groove" in the
  woven caption — repaired, and the weave-script source caption corrected
  so re-weaves stay clean. Remnant sweep across every content + question
  field: ZERO.
- **Phase 5 — heroes DONE** (eduqas_heroes.py): 32/32 set, 0 failed, 145
  vision calls. Verified: alt + caption on all 32, all 32 MD5-distinct,
  all download at full size.
- **Phase 5 — related media DONE** (build_related_media.py, now
  parameterised --subject/--units): 14/14 article lessons, every URL
  audited live (oEmbed for YouTube). One stubborn lesson (aos4 L2 Bhangra)
  needed a strict-JSON retry; its board-safe fallback set is generic
  (Bitesize/BBC Sounds/Classic FM) — fine, honest, alive.
- **Phase 5 — narration DONE** (narrate_eduqas_articles.py, post-fact-
  check per the house rule): 14/14 manifests, 369 clips, 97,946 chars,
  ~$1.57 Azure. Ollie odd / Ada even. R2 `music-eduqas/{unit}/`. Spot-
  checked 4 random clips serving from R2 at full size.
- **Phase 6 — QA gate**: `_qa_practice_data.py` — 0 errors corpus-wide,
  zero warnings touch music-eduqas.
- **Final sweep: ZERO issues** — 32 lessons / 8 units: every lesson
  pending_review with slug + hero; articles all have 6 PQ / 5 KC (correct+
  options shape) / 5 FC / 8+ glossary / exam tip / conclusion / related
  media / narration; both study-piece embeds woven; practice lessons all
  carry practice_data; practice_units setting correct.

## Build totals
- 32 lessons: 18 practice (copied + neutralised from music-aqa) + 14 new
  articles. All pending_review awaiting Tom.
- Cost: articles ~$2.80 + related media ~$0.40 + fact-check agents +
  narration ~$1.57 + heroes (vision) — well under a tenner all-in.

## For Tom's morning
- Review pass over the whole subject when the build completes.
- Badinerie REAL recording choice (synthesised excerpts carry the drills
  meanwhile).
