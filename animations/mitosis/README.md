# The cell cycle and mitosis — a drawn animation

A self-contained page that plays a 71-second animation of one cell dividing
by mitosis, with narration, the narrated sentence on screen, and a scene
scrub. Every frame is drawn in JavaScript on a `<canvas>`: no images, no
video, no libraries. The only external request is the Google Fonts
stylesheet; the page still works without it (system fallbacks).

Open it at **http://127.0.0.1:8904/animations/mitosis/index.html**
(start the server with `python _dev_server.py` from the repo root).

    animations/mitosis/
      index.html            the whole thing - markup, style, drawing, timing
      audio/scene-01..12.mp3 narration, one clip per scene (Azure, Ada)
      audio/manifest.json   the script, clip lengths, voice and format
      build_audio.py        regenerates the clips from the script
      verify.py             Playwright checks + the proof frames
      proof/                12 moments, a poster, a phone width, reduced motion

## Narration script

Written first, checked against AQA 4.1.2.2 before anything was drawn. Plain
GCSE English, British spelling, no exam board named.

1. Your body makes new cells all the time, to grow, to repair damage and to replace cells that wear out.
2. It does this in a series of stages called the cell cycle.
3. Inside this cell the nucleus holds the chromosomes, and in body cells they come in pairs.
4. First the cell grows and makes more of the structures inside it, such as ribosomes and mitochondria.
5. Then the DNA is copied, so each chromosome becomes two identical copies, joined together.
6. Now mitosis begins, and the membrane around the nucleus breaks down.
7. Fine fibres stretch out from each end of the cell and take hold of the chromosomes.
8. The chromosomes line up in a row across the middle of the cell.
9. The fibres pull the copies apart, so one set of chromosomes is pulled to each end of the cell.
10. A new membrane forms around each set, so the nucleus has divided.
11. Finally the cytoplasm and the cell membrane divide, making two cells.
12. Each new cell has the same chromosomes as the cell it came from, which is how the body grows and repairs itself.

## Scenes

The clip length drives everything. The drawing for a scene runs for exactly
the length of its clip; then a 0.55 s beat of quiet before the next clip
starts. Durations are read from the `Audio` elements at load, so replacing a
clip re-times the animation with no code change.

| # | key | what is drawn | clip (s) | scene (s) |
|---|-----|---------------|---------:|----------:|
| 1 | appear | one cell among its neighbours, membrane, cytoplasm, nucleus, 3 mitochondria | 6.17 | 6.72 |
| 2 | cycle | the three-stage ring is drawn in the corner; the neighbours fade | 3.79 | 4.34 |
| 3 | nucleus | four chromosomes fade in: two pairs, one long, one short | 5.74 | 6.29 |
| 4 | growth | the cell enlarges; mitochondria 3 → 6, ribosomes 13 → 28 | 6.55 | 7.10 |
| 5 | replicate | each chromosome grows its copy; the X shape closes at the centromere | 6.43 | 6.98 |
| 6 | envelope | the nuclear envelope breaks into fragments and drifts out (*prophase*) | 4.75 | 5.30 |
| 7 | spindle | poles appear, fibres reach out and take hold at each centromere | 4.80 | 5.35 |
| 8 | align | the four chromosomes line up on the equator (*metaphase*) | 3.82 | 4.37 |
| 9 | separate | copies separate, centromere first, arms trailing (*anaphase*) | 5.86 | 6.41 |
| 10 | reform | an envelope forms round each set; the spindle goes (*telophase*) | 4.80 | 5.35 |
| 11 | furrow | the membrane pinches; cytoplasm and organelles split | 5.11 | 5.66 |
| 12 | settle | two round daughter cells, four chromosomes each | 6.79 | 7.34 |

Total 71.2 s. Measured end to end in Chrome: 72.0 s from the first click to
the "Play again" state.

## The science

Straight from AQA 4.1.2.2 (`specs/aqa/science-8464-8464.md`, and the same
text in `specs/aqa/biology-8461-8461.md`), and phrased to match lesson 2 of
`science-aqa / biology-paper-1`.

- The three overall stages the spec asks for: **grow and copy** (scenes 4–5),
  **mitosis** (6–10), **divide** (11–12). The corner ring has one arc for
  each and fills as the cycle runs.
- Diploid parent with **4 chromosomes = 2 pairs**. Length says which pair;
  colour says which member of the pair. Both daughters finish with one of
  each — long brown, long teal, short brown, short teal — so the count and
  the set are checkable on screen.
- The two chromatids of a chromosome are drawn from the same seed, mirrored,
  so they are identical by construction.
- Each chromatid is held by a fibre from the pole it travels to, attached at
  its centromere. In anaphase the centromere leads and the arms trail.
- The nuclear envelope is a double line, it breaks down, and it reforms
  round each set before the cytoplasm divides.
- Mitochondria and ribosomes double before division, and both daughters get
  a share.
- No meiosis, no crossing over, no chromosome numbers that do not add up.

Known simplifications, all standard for GCSE diagrams:

- Chromosomes are shown inside the nucleus before replication. In a real
  interphase nucleus the chromatin is not condensed enough to see as
  separate chromosomes.
- Four chromosomes, not 46, for clarity. The narration never states a number.
- The phase names (prophase, metaphase, anaphase, telophase) appear as light
  handwritten notes only. The spec says students do not need them, so they
  never carry the explanation — the narration stays on the three stages.
- Centrioles, kinetochores and the ER are not drawn.

## House style

Paper `#f6f1e7`, card `#fffdf8`, ink `#26231e`, line `#e4dfd2`, anchor brown
`#5b4632` for the chromosomes and the membrane line, one accent (`#46706b`)
for the other member of each pair. Schibsted Grotesk for the title, Literata
for the narrated sentence, Caveat for the phase notes. Square 4px controls,
no pills, no coloured stripes, easing `cubic-bezier(.16, 1, .3, 1)`.

The painterly look is procedural: every shape is a wobbled outline painted
as three offset washes with a rim of gathered pigment and a hand line drawn
twice, over a generated paper grain. The wobble comes from a hash, so shapes
are stable frame to frame apart from a deliberate 7 fps boil of under a
pixel. `prefers-reduced-motion` turns the boil and the tweens off: each
scene shows its finished state and the scrub steps through them.

## Rebuilding the audio

    python animations/mitosis/build_audio.py          # keeps existing clips
    python animations/mitosis/build_audio.py --force  # re-synthesises all 12

Azure Speech, `en-GB-AdaMultilingualNeural` (the site's even-lesson voice;
the cell cycle is lesson 2), 24 kHz 96 kbps mono MP3 — the house format from
`scripts/lib/narration.py`. Needs `AZURE_SPEECH_KEY`.

## What was verified

`python animations/mitosis/verify.py` in installed Chrome, with the repo
served from `_dev_server.py`:

- all 12 clips load (`readyState` ≥ 1) and every scene length equals its
  clip length plus the 0.55 s beat, to the millisecond;
- playback advances on the audio clock (2.47 s of scene 1 after 2.5 s);
- a full run reaches scene 12 and stops at "Play again" after 72.0 s;
- the scrub jumps to a scene and swaps the sentence;
- reduced motion renders and steps with no errors;
- console clean, no failed requests, at 1300px and at 400px.

Proof frames are in `proof/`, one per stage, plus the poster, the phone
width and a reduced-motion frame.
