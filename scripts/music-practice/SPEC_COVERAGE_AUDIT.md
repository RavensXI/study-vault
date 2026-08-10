# Music AQA 8271 — full spec coverage audit (9 Aug 2026)

The definitive pass. Every Section A strand and every Section B study piece in the spec,
checked against every lesson in `music-aqa` (school_id NULL). Run this again after any
spec rotation. Source of truth: `specs/aqa/music-8271-8271.md` (contains BOTH rotations —
read past the "final assessment 2025" block to find the current works).

## Section B — study pieces (current rotation, first taught 2024 / first assessed 2026)

| AoS | Study piece | Our lesson | State |
|-----|-------------|-----------|-------|
| 1 | Beethoven Symphony No.1, Mvt 1 | aos1-western-classical/L3 | Guided Listening, hosted PD audio, machine-verified pins |
| 2 | Queen: Bohemian Rhapsody, The Seven Seas of Rhye, Love of my Life | aos2-popular-music/L3 | Guided Listening, 3 embedded set recordings |
| 3 | Esperanza Spalding: Little Fly, I Know You Know, I Adore You | aos3-traditional-music/L2 | Guided Listening, 3 embedded set recordings |
| 4 | Bartók: Hungarian Pictures (movements 1, 2, 4, 5) | aos4-since-1910/L2 | Guided Listening, 4 embedded movements |

All four correct and complete. Movement 3 (Melody) is correctly excluded.

## Section A — unfamiliar-listening strands (68 marks)

| AoS | Strand | Covered by | Verdict |
|-----|--------|-----------|---------|
| 1 | Coronation Anthems and Oratorios of Handel | wc-1650-1910/L5 (Zadok) | OK |
| 1 | Orchestral music of Haydn, Mozart, Beethoven | wc-1650-1910/L1,L2,L3,L4 | OK |
| 1 | Piano music of Chopin and Schumann | wc-1650-1910/L6,L7 | OK |
| 1 | The Requiem of the late Romantic period | wc-1650-1910/L8 (Verdi) | OK |
| 2 | Music of Broadway 1950s–1990s | aos2/L2 (musical theatre) | thin — topic yes, ERA no |
| 2 | Rock music of 1960s and 1970s | — | **GAP** |
| 2 | Film and computer gaming music 1990s–present | aos2/L2 | OK (topic), era untaught |
| 2 | Pop music 1990s–present | — | **GAP** |
| 3 | Blues 1920–1950 | aos3/L1, aos-listening/L2 | OK |
| 3 | Fusion with African and/or Caribbean music | aos3/L1, aos-listening/L2 | OK |
| 3 | Contemporary Latin music | aos3/L1, aos-listening/L2 | OK |
| 3 | Contemporary Folk of the British Isles | aos3/L1, aos-listening/L2 | OK |
| 4 | Orchestral music of Copland | aos-listening/L3 only | thin — drill only |
| 4 | British: Arnold, Britten, Maxwell-Davies, Tavener | aos-listening/L3 only | thin — drill only |
| 4 | Orchestral music of Kodály and Bartók | aos4/L2, aos-listening/L3 | OK |
| 4 | Minimalism: Adams, Reich, Riley | aos4/L3, aos-listening/L3 | OK |

## The one real gap (task #43)

`aos2-popular-music/L1` ("Rock and Pop") teaches FEATURES only — standard line-up,
verse-chorus, riffs and hooks, backbeat, swung vs straight feel, production. It names no
decade at all. But AoS2's strands are defined by ERA, and Section A explicitly asks for
"musical elements, musical **contexts** and musical language". A student can describe the
elements of an extract but cannot place it in its period or tell 60s/70s rock from 90s+ pop.

Also worth noting (lower priority): AoS4's Copland and British-composer strands appear only
in the unfamiliar-listening practice drill, never in a taught article.

## Why this kept getting missed
Every previous check was piecemeal — study pieces one day, one movement another. Nobody had
read all four Areas of Study against all 30 lessons in one pass until now. Do this whole-spec
sweep FIRST on any subject, not last.

## AoS2 era gap CLOSED (9 Aug)
New lesson aos2-popular-music L4 "Placing a Track in Time" (id d601ff11) — appended, never inserted.
Covers all four AoS2 Section A strands by ERA: rock 60s/70s, pop 90s+, Broadway across its decades,
film+gaming 90s+. Full asset set: 5 KCs, 5 flashcards, 6 practice questions WITH mark schemes,
7 glossary terms, exam tip, conclusion. No hero image and no narration yet (see below).

GOTCHA worth remembering: practice_questions REQUIRE a "marks" field. Omit it and
formatMarkScheme() throws inside initLessonFeatures, which silently kills every later feature on
the page — chunk menu, glossary popups, knowledge check. The lesson still LOOKS fine.
Always set text + type + marks.

FACT-CHECK (agent, 9 Aug) — report scripts/_fact_check/music-aqa-aos2-l4.md
1 HIGH found IN MY OWN WRITING and fixed: I dated grid-exact/programmed drums to "the 1990s or
later". Wrong — drum machines (Linn LM-1, TR-808, both 1980) put quantised drums on mainstream pop
from 1980-82. Reworded to "common since the early 1980s, so it rules out 1960s/70s live-band rock",
which is what the test is actually good for. The claim appeared in THREE places (key fact, KC1,
flashcard 5) — all corrected; KC1 reworded to ask what it rules OUT.
2 LOW fixed: overdrive tooltip vs glossary disagreed and over-specified valve amps; sung-through
definition contradicted itself. Also added the 3 tooltipped-but-missing glossary cards (fuzz,
double-tracked, ostinato) — 10 terms now.
Everything else verified sound, including all answer keys.
HERO: via the real sandbox HeroFinder (scripts/lib/hero_pipeline.py) — vision grade A, vinyl records
of different eras, Eric Krull / Unsplash, md5 e47d0843bf58dda0dd24918da5d3ff44, deduped against all
11 existing music-aqa heroes. NOTE: HeroFinder lives ONLY in the sandbox worktree, not main.

## Format map — why this subject has THREE kinds of lesson (10 Aug)

Read this before asking "what are these old-looking lessons for?" again. Music is a mixed-format
subject: `subjects.settings.practice_units` lists four units that serve at `/practice/`, the rest
serve at `/lesson/`. That is deliberate, not drift.

| Unit | Lessons | Route | Format | Job |
|------|---------|-------|--------|-----|
| aos1-western-classical | 3 | /lesson/ | article + 1 Guided Listening | teach AoS1 |
| aos2-popular-music | 4 | /lesson/ | article + 1 Guided Listening | teach AoS2 |
| aos3-traditional-music | 2 | /lesson/ | article + 1 Guided Listening | teach AoS3 |
| aos4-since-1910 | 3 | /lesson/ | article + 1 Guided Listening | teach AoS4 |
| listening-skills | 3 | /practice/ | drill | build the ear from scratch |
| western-classical-1650-1910 | 8 | /practice/ | drill | AoS1 Section A unfamiliar listening |
| aos-listening | 3 | /practice/ | drill | AoS2-4 Section A unfamiliar listening |
| score-reading | 4 | /practice/ | drill | read the printed score in Section A |

**The four Guided Listening lessons are the four Section B set works** — Beethoven, Queen,
Spalding, Bartók. GL exists to walk you THROUGH a piece you are required to know: pinned
annotations tell you what you are hearing as you hear it.

**The 18 drill lessons are Section A** — 68 of the 96 marks. Section A plays music you have never
heard. The whole skill is extracting features with NO scaffolding. Annotating those excerpts with
GL pins would delete the exam skill they exist to build. So: **do not convert the drills to Guided
Listening.** Different job, opposite pedagogy.

165 questions across the 18 drills, bronze/silver/gold, all on 70 distinct licence-clean MP3s
hosted on R2 (`music-aqa/...`). No YouTube anywhere in the drills.

### Player upgrade DONE (10 Aug)
The drills used to render audio as a bare browser `<audio controls>` grey pill next to the study
pieces' bespoke waveform dock. Now they have their own inline player: 90 of them across all 18
lessons, one row — play, waveform, clock.

- `js/practice-audio.js` (sandbox branch) — self-contained, NOT the main.js dock. practice.html
  does not load main.js, and the components want opposite things: the dock is fixed to the
  viewport and carries pins, which would be wrong here. **Never add pins to a drill** — Section A
  is unfamiliar listening, so annotation deletes the skill being tested.
- `scripts/music-practice/gen_drill_peaks.py` — ffmpeg -> 260-value envelope per file.
  Manifest `_drill_peaks.json` is committed, so a re-run costs nothing.
- `scripts/music-practice/apply_inline_player.py` — swaps the markup in Supabase. Idempotent,
  writes a backup first, `--dry-run` and `--restore <backup>` supported. The backup
  (`_drill_practice_data_backup.json`) is gitignored — it is a point-in-time dump, not source.
- Peaks travel INLINE in the passage HTML. R2 sends no `Access-Control-Allow-Origin` header, so
  the browser cannot fetch a `.peaks.json` cross-origin. Do not "improve" this to a fetch.
- Players are wired by a MutationObserver, so passage panel / worked examples / method-card modal
  all work without hooking three separate injection sites.

Pins were deliberately left out: only 8 of the 165 drill questions cite a timestamp, so pin times
are real ear-work. If they are ever added, do it as reveal-AFTER-answering so the excerpt stays
unannotated until the student has committed.

### Two defects found while doing it
1. `listening-skills` L3's only worked example pointed at `ex015_cadence.mp3`, which 404s — the
   demonstration played silence. Re-pointed to `exC_perfect.mp3`, the one existing clip matching
   the worked answer ("perfect"). It is also a silver question's clip; reused deliberately, since
   hearing a perfect cadence in the demo and again in a question is reinforcement.
2. `.learn-card-head` is a capped scroll box with NO affordance, so the last visible line read as
   the end of the question. Real overflow measured: music AoS1 L1 70px, score reading L1 225px,
   geography skills L1 115px. Students were answering truncated sentences. Fixed with a bottom
   fade that appears only when there is more, plus a cap raise 48vh -> 60vh (guided 52 -> 58) —
   verified at 960/800/720 heights that the action buttons stay on screen even at 64vh.

## Reviewing Guided Listening lessons — MUST use the preview deployment
`origin/platform` (and so www.studyvault.co.uk) has ZERO Guided Listening assets: 0 hits for
`sv-listening` in css/style.css, 0 for `initListeningLesson` in js/main.js, service worker still
sv-v5. A GL lesson opened from the PRODUCTION /admin/review screen renders as unstyled markup —
it looks broken because the CSS and JS simply are not there.
Review at the landing-wizard preview instead (Vercel SSO-protected, so curl sees a 302 — that is
the auth wall, not a missing build):
  https://study-vault-git-landing-wizard-tom-shauns-projects.vercel.app/admin/review
Local equivalent: `python design-lab/serve.py` then http://127.0.0.1:8901/ (plain http.server will
NOT work — no rewrites).

## FACT-CHECK COVERAGE — the honest state (10 Aug)

**Correction to an earlier draft of this section:** it claimed only 4 of 14 article lessons had
ever been fact-checked. That was wrong. A Phase 6 pass DID run at build time.

| Pass | When | Scope | Result |
|------|------|-------|--------|
| Build-time Phase 6 | 6 Aug (`f2b2d505`) | all 11 article lessons then existing | 3 HIGH, 4 MEDIUM, 6 LOW — applied by `apply_factcheck_fixes.py`, grounded in AQA teacher guides |
| Bitesize deep pass | 9 Aug | Queen, Spalding, Bartok (the 3 embed decks) | **14 further errors** in lessons the 6 Aug pass had already cleared |
| Agent | 9 Aug | aos2 L4 (new lesson) | 1 HIGH + 2 LOW |
| This pass | 10 Aug | timestamps subject-wide + aos4 L3 | 10 timestamp corrections + 1 contradiction |
| — | — | **all 18 drills, 165 questions** | **NEVER IN SCOPE** |

Two process failures, both worth more than any individual error:

**1. The build-time pass left no artefact.** Every other subject has
`scripts/_fact_check/{slug}.json` + `.md`. Music has neither, so from the filesystem it looked as
though no check had happened. If a pass leaves no report, the next person re-does it or wrongly
assumes it never ran — both waste a day. **Always write the report.**

**2. The fixes were applied to `content_html` only.** `apply_factcheck_fixes.py` correctly found
that Riley's In C is not additive and rewrote the body — but never touched the `<h2>` heading
("The additive process — Terry Riley") or flashcard 2, which both went on asserting exactly the
claim the check had just refuted. It surfaced today as a live contradiction, four days later.
**A fact-check fix must sweep every field: content, headings, KCs, flashcards, glossary and
practice questions.** Same shape as the drum-machine error that hid in three fields on aos2 L4.

And the 9 Aug pass finding 14 more errors in three lessons the 6 Aug pass had signed off says the
build-time check was real but not sufficient — it is a floor, not a guarantee.

The drills were invisible to `_fact_check_subject.py` throughout: it plans only lessons with
`content_html`, and drills keep everything in `practice_data`. So 165 answer keys had never been
looked at. A wrong key marks a correct answer wrong — worse than a wrong sentence.

### Timestamp errors found and fixed (10 Aug)
Measured from the hosted recordings with ffmpeg (amplitude envelope, 1s buckets) — not guessed.

- **Haydn 94 'Surprise', lesson-04.mp3.** Bars 1-8 end ~0:21; the pianissimo repeat sits at
  0.007-0.037 until 0:41; **0:42 jumps to 0.541, a x27 step**. The chord is at **0:42**, not the
  0:27 we claimed. At 0:27 the music is near-silent — a student following the instruction hears
  nothing. Fixed in 4 places: aos1 L1, aos1 L2, and TWO drill L4 questions.
- **Handel Zadok, lesson-05.mp3.** Crescendo 0.066 -> 0.096 through 1:20-1:33, 1:34 = 0.185,
  1:36 = 0.451. **Choir enters ~1:36**, not 1:30. Fixed in 4 places: aos1 L1, drill L5 method card
  and two drill L5 questions.
- **Beethoven Sym 1, lesson-01.mp3.** Our content disagreed with itself: the lessons said the
  Allegro arrives "about 1:50", the drill method card said "Adagio 0:00-1:10 / Allegro from 1:10".
  Loudness alone was ambiguous because **the Allegro con brio begins piano**. Extending the window
  settled it: quiet trough 1:31-1:43 (rms 0.013-0.042), then sustained growth from **1:45** to a
  tutti by 1:53 (rms 0.11). The Guided Listening pin `data-t="107"` (1:47) agrees independently.
  So the LESSONS were right and the DRILL was wrong — the method card is now 1:45. Nearly corrected
  the wrong one; measuring is what caught it.

Note: aos1 L3's apparent "1:502" typo is not a typo. It is 1:50 followed by a GL ref button
`<button class="sv-ap-ref" data-t="107">2</button>`. Tag-stripped extraction makes it look garbled —
same class of illusion as [[reference_practice_display_inline_svg]]. Left alone.

### Content error found and fixed
**aos4 L3 contradicted itself about Terry Riley.** Body: In C "works differently — built not on
note-by-note growth but on staggered repetition". PQ1 mark scheme: "(Terry Riley's In C is NOT
additive)". But the section heading read "The additive process — Terry Riley" and flashcard 2
answered "which composer is linked to it" with "Terry Riley". A student revising from the flashcard
learned the exact association the lesson's own mark scheme refuses to credit. Heading and flashcard
fixed; body and mark scheme were already right.

### Drill answer keys — machine audit (165 questions)
Structurally clean: every solution index in range, no duplicate or near-identical options (the 9
flags were the heuristic misfiring on legitimate distractors like "2 quavers per beat" vs "3"), no
explanation naming a non-key option, no orphan `passage_id`, every question has an explanation.
**This does NOT confirm the answers are musically true** — that needs ears on the audio and stays
on Tom's check list. Script: `scripts/music-practice/audit_drill_keys.py`.

### Deep pass now COMPLETE for every article lesson (10 Aug)
Three agents, batched by Area of Study, read every field — not just content_html — against the spec,
the saved Bitesize text and the audio itself. Every finding was re-verified here before applying;
nothing was taken on the agent's word.

| Lesson | Verdict |
|--------|---------|
| aos1 L1 Orchestra | clean (beyond today's timestamp fixes) |
| aos1 L2 Structures | clean |
| aos1 L3 Beethoven (study piece) | **exposition-repeat pin 9.5s late** + portrait caption |
| aos2 L1 Rock and Pop | clean |
| aos2 L2 Stage, Screen and Games | clean |
| aos3 L1 Four Styles | **mark scheme paid twice for one fact** |
| aos4 L1 Twentieth-Century Colour | clean |
| aos4 L3 Minimalism | **off-spec composer credited as the model answer** |
| aos-listening L1, L3 | clean |

**aos1 L3 — exposition-repeat pin (MEDIUM).** Pin c4 and its in-text ref both pointed at 242s; the
repeat actually begins at ~232.5s, so clicking "the whole exposition repeats" dropped you into the
middle of the restated first subject. Corroborated in two independent feature spaces: the agent's
chroma cross-correlation (peak 232.5s, 0.97) and, here, log-spectrogram band correlation using the
lesson's own first-subject pin (107s) as reference — a sharp isolated peak of 0.9800 at 232.5s
against a surrounding plateau of ~0.945-0.955, with 242s scoring 0.9491. Moved to 232.5s, left%
recomputed against the true duration 581.45s. Pin/ref invariant re-checked after the edit.
The agent also *cleared* the recapitulation pin (c6, 406s) after initially suspecting it — bar-count
maths said the development should be longer, but a ~3x sustained energy jump at 404-406s matches the
recap's fortissimo unison entry. Worth noting: it reported the negative result rather than quietly
dropping it.

**aos3 L1 — a mark payable twice (MEDIUM).** "Describe two features of the rhythm" credited both
"swung/shuffle rhythm" AND "uneven long-short division of the beat", but the lesson's own glossary
defines swung rhythm AS an uneven long-short division. One fact, two names, two marks. Merged.

**aos4 L3 — off-spec composer (MEDIUM).** PQ1's mark scheme named Philip Glass as "most clearly"
the right composer for the additive process. The spec strand is "Minimalist music of John Adams,
Steve Reich and Terry Riley" (spec line 857) — Glass is neither in it nor taught in the lesson.
The agent proposed crediting Reich instead; REJECTED, because the body teaches Reich as phasing and
never as additive, so the swap would only move the contradiction. The underlying defect was that the
question demanded a composer the course never supplies — none of the three named composers cleanly
exemplifies the additive process, and the lesson says so of Riley explicitly. Question rewritten to
test the distinction the lesson does teach: name the technique, then explain how In C differs.

Lesson for next time: when an agent proposes a fix, check whether the fix creates a new
contradiction. Two of the three findings here needed a different remedy from the one suggested.

## Stale-rotation sweep (10 Aug)
Regex swept all 30 lessons for "previous set work / assessed to 202x / until 202x". Two hits, both
on drill L3. Fixed: L1 "The current AQA set work" -> "The set work for this Area of Study";
L3 "Previous AQA set work (assessed to 2025)" -> dropped. Mozart Clarinet Concerto stays — it is
still valid Section A practice for the Haydn/Mozart/Beethoven orchestral strand, it just must not
be framed by which rotation it used to belong to.
