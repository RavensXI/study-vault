# Overnight log — 16 Aug 2026: Music Eduqas + OCR + Edexcel builds (#57, #58, #60)

## Music Edexcel 1MU0 (task #60) — BUILT same evening, Tom's go 16 Aug

Plan: `EDEXCEL_BUILD_PLAN.md`. 31 lessons / 7 units, pending_review,
subject live. The set-work board: 8 prescribed works, each with two
study lessons carrying the sv-annotated-player (official videos: DG
Pathétique + Star Wars/Vienna Phil, Chamber Orchestra of Europe
Brandenburg mvt 3, Queen Official TOTP Killer Queen, WickedVEVO,
Helen Watts Purcell, official-audio Release + Samba Em Preludio).
11 practice copies (era spans corrected; exam_context rebuilt for this
spec's Component 3 comparison essay). 20 articles ~$2.20 (one network
death mid-run — the orphan-draft sweep pattern now inserts paid drafts
before regenerating). 39 embeds wired MAP-FIRST (retro applied: curate
once, apply from the saved map; two weak picks hand-patched).
Fact-check: **41 findings, 31 HIGH** — the heaviest of the three
boards, as predicted for set works (Brandenburg entry order
violin-first ×4 fields; Purcell ground 3 bars not 8×34; Killer Queen
first-Top-10 + missing third verse + 12/8 backwards; Spalding's
"double bass" is Pearson's acoustic bass guitar, string ensemble
fabricated, my own player pins/credit corrected incl. 2008 not 2010;
Release vocalist credits untangled; AoS3 CLEAN). All fixed, remnant
sweep clean (three survivors verified legitimate). Narration 462+22
clips ~$2.54 post-fact-check. Heroes 31/31 MD5-distinct (two dupe
rounds fixed — finder dedupes by URL only, note for the pipeline).
Related media 20/20 (strict-JSON retries for six). QA gate 0 errors.

## Site-wide catches from Tom's Eduqas review pass (same evening)

- **41 dangling "what to listen for" captions** across music-eduqas +
  music-ocr's film copies — every one completed with a work-specific
  pointer and its narration clip regenerated in place (shared R2 keys
  healed both subjects). `fix_dangling_captions.py`.
- **Music-family revision-tip gap**: the music article pipeline never
  emitted data-revision-tip, so every lightbulb fell back to generic
  copy — music-aqa included. Every other subject family checked: fully
  tipped. 163 boxes across the four music boards now carry specific,
  box-grounded retrieval tasks. `music_revision_tips.py`. TODO
  (pipeline): the article builders should emit data-revision-tip at
  build time.

---

## Music OCR J536 (task #58) — BUILT same day, Tom's go 16 Aug afternoon

Plan: `OCR_BUILD_PLAN.md`. 33 lessons / 8 units, all pending_review,
subject live. No set works on this spec — no study-piece players; AoS1
(My Music) is NEA, so the appraising build covers AoS2–5.

- **Phases 1–2**: activation + 17 practice copies (concerto listening
  renumbered chronologically Baroque→Romantic; AQA's Broadway problem
  DROPPED — not an OCR strand; AoS renumbering transformed and asserted).
- **Phase 3**: 13 fresh articles ~$1.13, ALL first-pass valid; 3 film
  articles copied wholesale from music-eduqas (content, embeds,
  narration manifests, heroes, related media — zero cost). Retro
  applied: NO listen boxes — 34 embed markers wired at build time via
  search+verify (NBS Brandenburg 4, Berliner Phil, Nintendo's own Zelda
  concert, O'Donnell's Halo, VEVO pop originals, Mangueira bateria,
  Mamady Keita live). Retro note: yt search ordering is UNSTABLE between
  dry-run and apply — two picks drifted (one amateur video, one wrong
  song version); both caught and replaced. Next board: wire from the
  dry-run map, don't re-search on apply.
- **Phase 5 fact-check** (4 agents; `scripts/_fact_check/music-ocr.md`):
  16 findings, 11 HIGH — Livin' On A Prayer's key change is a minor
  third not a semitone (content+mark scheme+flashcard), hora is duple
  not triple (4 places — one found only by the remnant sweep), dunun
  sizes reversed, K.314 is Flute Concerto No. 2, Halo chant metre +
  Mjolnir Mix honestly relabelled + Salvatori co-credited, Zarathustra's
  C major/minor ambiguity restored, Dylan's harmonica removed, a lyric
  quotation removed. All fixed surgically, zero remnants.
- **Phase 5 assets**: heroes 30 fresh + 3 carried, all 33 MD5-distinct;
  related media 13/13 URL-audited (two world-music lessons needed the
  strict-JSON retry); narration 300 clips ~$1.72 post-fact-check, film
  manifests reused cross-subject.
- **Phase 6**: QA gate 0 errors, zero music-ocr warnings. Final sweep
  across all 33 lessons: ZERO issues (statuses, slugs, heroes+captions,
  question counts/shapes, embeds, no ghost clips, board-name ban).

**Gate for Tom:** Rhythms of the World has ARTICLES only — its drills
wait on the synthesised-rhythms vs embeds decision. Plus the usual
review flip; podcasts after.

---

# Music Eduqas build (task #57) — earlier the same night

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
