# Music Eduqas C660QS — build plan (free tier, slug `music-eduqas`)

Started 16 Aug 2026, late. Off `docs/MUSIC_BOARDS_REUSE_PLAN.md` with Tom's
decisions locked (Eduqas first; no Unity porting; Unity later subscribes to
THIS build and overrides its old music). Spec bullets source:
`_eduqas_aos_spec_extract.md` (verbatim from specs/eduqas/music-C660QS.md).
House rule: neutral phrasing — never name the board in prose.

## Audio sourcing hierarchy (Tom, 16 Aug)

1. Existing verified library (PD recordings + synth drill bank) — free reuse.
2. Honest synthesis (music21/FluidSynth, score-player) — facts true by
   construction. **Badinerie is a PD composition: its excerpts are
   SYNTHESISED from the score**, which unblocks the study lessons from the
   recording gate; a real recording embed can join later.
3. Flow-generated music — only where the established machine-ear validation
   flow can verify the question from the audio itself (the AoS2-4 pattern).
4. Official YouTube embeds — real works, oEmbed-verified (Africa, ensemble
   and film examples).

## Units (~31 lessons; subject `live`, lessons `pending_review`)

### Article units
| Unit | Lessons | Source |
|---|---|---|
| aos1-forms-and-devices | L1 forms (binary/ternary/minuet–trio/rondo/variations/strophic); L2 devices (ostinato, sequence, imitation, pedal, canon, drone…); L3–L4 **Badinerie study** (structure+context; devices+scoring) | AQA aos1 ~70%; Badinerie NEW with synthesised score excerpts |
| aos2-music-for-ensemble | L1 texture+sonority; L2 jazz & blues ensembles; L3 musical theatre & chamber | texture material ~40%; rest new |
| aos3-film-music | L1 scoring devices+leitmotif; L2 mood, time & place; L3 building a cue | AQA aos2 film segment ~50% |
| aos4-popular-music | L1 pop forms & hooks; L2 bhangra & fusion; L3–L4 **Africa study** (embed-plus-features, NO audio excerpts) | AQA aos2 ~50%; Africa NEW |

### Practice units
| Unit | Lessons | Source |
|---|---|---|
| listening-skills | 3 | COPY from music-aqa + terminology/neutral-phrasing pass |
| score-reading | 4 | COPY from music-aqa (same pass) |
| forms-devices-listening | 8 | ADAPT music-aqa western-classical drills — same PD works, same 1650–1910 span; forms questions added |
| ensemble-film-pop-listening | 3 | ADAPT music-aqa aos-listening (blues/latin map to ensemble; film maps; pop maps) |

## Assets (per house convention)
Heroes (vision-gated), narration (Ollie/Ada), KCs + flashcards + practice
questions through the QA gates, related media (URL-audited), misconception
diagnoses. Podcasts + explainers AFTER Tom's review flip, as with AQA.

## Gates that wait for Tom
- The review pass over all lessons (everything lands pending_review).
- Any REAL Badinerie recording embed (synthesised excerpts carry the drills
  meanwhile). No other ear-gates by design.

## Execution order (overnight)
1. Subject activation: subject row, 8 units, accents, quote ticker.
2. Skills copies (listening-skills, score-reading) + terminology pass.
3. Drills adaptation (forms-devices-listening; ensemble-film-pop-listening).
4. Article content (fact-check gated), then assets.
5. QA gates: _qa_practice_data, _qa_practice_answers, validators, link audit.
Log: OVERNIGHT_LOG_2026-08-16.md. Scheduled check-ins throughout.
