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
