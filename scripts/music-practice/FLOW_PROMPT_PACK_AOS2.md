# Flow prompt pack — AoS2 popular music (aos-listening L1)

Four clips, **two takes each** (`a` / `b` — A/B picking has earned its keep on
both previous batches). WAV, 60–90 seconds so there is room to trim a clean
15–20 second window. **No lyrics anywhere** — wordless vocals only where stated.

## Why these four

`aos-listening` L1 needs four more questions (bronze +1, silver +1, gold +2).
AQA's AoS2 strands are defined by ERA: Broadway 1950s–1990s, rock of the 1960s
and 1970s, film and computer gaming music 1990s–present, and pop 1990s–present.
So the four clips are chosen to give the **era-dating contrast** that
aos2-popular-music L4 teaches — a live band that breathes against a programmed
grid. The drill then tests exactly what the article taught.

Two earlier routes failed and are not worth retrying:

- **Constructed clips** (`gen_excerpts.py`). Tom: *"those are garbage and don't
  sound like pop at all... they both just basically sound like somebody playing
  a flute."* A sampled flute cannot stand in for a bass guitar.
- **CC BY library music** (Kevin MacLeod, seven tracks auditioned). Licence was
  fine and the audio was real, but Tom: *"none of them sound like pop music in
  the way I think of it."* Library instrumentals are not the idiom.

Every prompt below describes **idiom, instrumentation and technique only** — no
artist names, no song titles, nothing asking Flow to imitate a particular
record.

---

## 1. `aos2_rock_60s70s_a` / `_b` — live rock band, 1960s–70s

> Energetic four-piece rock band playing live together in one room, late 1960s
> style. Overdriven electric guitar with a warm valve-amp grit, electric bass
> guitar playing a moving line, acoustic drum kit with an audible room sound,
> and Hammond organ underneath. Medium tempo around 120 beats per minute, with
> the feel pushing and pulling slightly rather than sitting exactly on the beat.
> Verse-chorus feel with space for a short guitar solo. Analogue tape warmth.
> No programmed drums, no drum machine, no synthesiser, no auto-tuned or layered
> vocals, no modern sub-bass, no click-track tightness, no lyrics.

**Tests:** live-band feel (tempo breathes) · overdriven guitar · Hammond organ ·
acoustic kit with room · dates to the 1960s–70s.

## 2. `aos2_pop_90s_now_a` / `_b` — programmed pop, 1990s onwards

> Modern pop production, instrumental. Programmed drum machine beat locked
> exactly to the grid with a crisp snare on beats two and four, deep synthesised
> sub-bass, bright synthesiser pads and a short repeating synth hook that loops
> through the whole track. Everything heavily compressed so the mix sits loud
> and level. Tempo exactly 104 beats per minute with no drift whatsoever.
> Clean, clinical, studio-built. No acoustic drum kit, no electric guitar solo,
> no Hammond organ, no orchestral instruments, no tempo variation, no lyrics.

**Tests:** programmed/quantised beat · synth bass and pads · loop-based
construction · heavy compression · dates to the 1990s or later.
**Pairs directly with clip 1** — same question, opposite answer.

## 3. `aos2_broadway_a` / `_b` — Broadway pit orchestra

> Show-tune instrumental for a Broadway pit orchestra in a 1950s–60s style.
> Lush strings, bright brass section, woodwind, piano and upright bass, with a
> light swung drum kit. Confident, optimistic character with a clear singable
> melody carried by the strings, a key change lifting the final section, and a
> big held final chord. Theatre acoustic. No electric guitar, no synthesiser, no
> drum machine, no rock backbeat, no lyrics.

**Tests:** pit-orchestra scoring · show-tune idiom · key change for lift ·
Broadway strand.

## 4. `aos2_gaming_loop_a` / `_b` — film and computer gaming music

> Driving instrumental cue for a modern action video game. Full orchestral
> strings and brass layered with electronic percussion and synthesised bass,
> over a relentless repeating string ostinato. Builds by ADDING layers —
> instruments enter one at a time and drop away again — rather than by changing
> the tune, and ends where it began so it could loop seamlessly. Tempo steady at
> about 140 beats per minute. Cinematic, wide stereo. No lyrics, no solo vocal,
> no acoustic drum kit backbeat, no guitar solo, no fade out.

**Tests:** orchestral-plus-electronic hybrid · ostinato · layering in and out ·
seamless loop (the feature that distinguishes game music from film) · dates to
the 1990s or later.

---

## After generation

1. Trim to a 15–20 second window where the full texture is running — not the
   intro.
2. `python scripts/music-practice/validate_flow_batch.py <folder>` — the three
   passes: unprimed description, 3-vote shuffled MCQ ensemble, then a distractor
   audit so no distractor is *also* true.
3. Tom's ear is final. Generated audio is claim-class, not construction-class:
   nothing ships without both the validator and a listen.
4. Measure tempo and beat-spread (see `prep_ccpop.py`) — clips 1 and 2 should
   differ sharply, and that measured difference is what the era question rests on.
5. Upload, add to `AUDIO_PROVENANCE.md`, wire the four questions, then re-run
   `python scripts/_audit_practice_tiers.py`.
