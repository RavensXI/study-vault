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

## Next (in order)
- Phase 3: drills adaptation — forms-devices-listening (8 lessons from
  western-classical-1650-1910: same PD works, forms questions added) and
  ensemble-film-pop-listening (3 from aos-listening).
- Phase 4: article content through fact-check gates (Badinerie study with
  synthesised score excerpts; Africa embed-plus-features).
- Phase 5: assets (heroes vision-gated, narration, KCs/flashcards/
  questions, related media URL-audited, misconception diagnoses).
- Phase 6: QA gates (_qa_practice_data, _qa_practice_answers, link audit).

## For Tom's morning
- Review pass over the whole subject when the build completes.
- Badinerie REAL recording choice (synthesised excerpts carry the drills
  meanwhile).
