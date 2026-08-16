# Music OCR J536 build plan (free tier) — task #58

Second board off `docs/MUSIC_BOARDS_REUSE_PLAN.md` (Eduqas shipped 16 Aug).
Five AoS; **no set works — every exam extract is unfamiliar**, so there are
no study-piece player lessons on this board. AoS1 is the learner's own
performing/composing (NEA) — the appraising build covers AoS2–5.
Tom's go: 16 Aug ("crack on with OCR").

## Units (8 — 30 lessons)

| # | slug | content | source |
|---|------|---------|--------|
| 1 | listening-skills | 3 drills | copy music-aqa, neutralise |
| 2 | aos2-the-concerto-through-time | 4 articles | new (Baroque solo + grosso; Classical; Romantic; elements-and-method) |
| 3 | aos2-concerto-listening | 4 drills | copy: Mozart K.622 (a real concerto), Beethoven Sym 1, Mozart 40, Haydn 94 — period-and-elements listening for the 1650–1910 span |
| 4 | aos3-rhythms-of-the-world | 4 articles | new (India & Punjab; Eastern Mediterranean & Middle East; Africa; Central & South America) |
| 5 | aos4-film-music | 4 articles | 3 adapted from music-eduqas film + 1 NEW video-game-music lesson (OCR-specific) |
| 6 | aos5-conventions-of-pop | 4 articles | new against OCR's four strands (Rock 'n' Roll 50s–60s; Rock Anthems 70s–80s; Pop Ballads 70s–90s; Solo Artists 1990–now), reusing AQA/Eduqas pop material |
| 7 | aos45-unfamiliar-listening | 3 drills | copy: pop, orchestral colour (film-adjacent), ensemble textures |
| 8 | score-reading | 4 drills | copy music-aqa, neutralise |

practice_units: listening-skills, score-reading, aos2-concerto-listening,
aos45-unfamiliar-listening.

## Gates

- **Rhythms of the World drill audio waits for Tom** (synthesised rhythm
  patterns vs official embeds vs sourced recordings). Articles are prose
  about real traditions — they build now, fact-check gated, with official
  YouTube embeds for the works discussed. NO drills in aos3 until Tom rules.
- Everything lands pending_review. Fact-check before narration.

## Process improvements carried from the Eduqas retro

- **No dead listen boxes.** The article builder must not emit sv-listen
  figures. Every listening example is an `<!-- EMBED: {key} -->` marker;
  all markers are wired post-build through the search+verify pipeline
  (yt search → oEmbed → title keyword → channel gate), or cut.
- Board-name ban includes AQA/Edexcel/Eduqas/WJEC/OCR; "Section A of the
  exam" phrasing banned; spec slices sanitised of OCR page furniture.
- Copies carry slug; copier resume-safe; `.order('id')` on any paginated
  read; Edit tool for file edits, never heredoc patchers.

## Order of work

1. Activation (subject + 8 units). 2. Skills + drills copies with the
neutralise pass + QA gate. 3. Articles (~16, canary L1 first). 4. Embed
wiring sweep. 5. Fact-check agents → surgical fixes. 6. Heroes, related
media, narration (post-fact-check). 7. QA gates, verification sweep, log,
commit. Podcasts/explainers post-flip as usual.
