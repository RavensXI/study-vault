# The cell cycle and mitosis — a drawn animation

A self-contained page that plays an 86-second animation of one cell dividing
by mitosis, with narration, the narrated sentence on screen, hand-lettered
labels, and a scene scrub. Every frame is drawn in JavaScript on a
`<canvas>`: no images, no video, no libraries. The only external request is
the Google Fonts stylesheet; the page still works without it.

Open it at **http://127.0.0.1:8904/animations/mitosis/index.html**
(start the server with `python _dev_server.py` from the repo root).

    animations/mitosis/
      index.html             the whole thing - markup, style, drawing, timing
      audio/scene-01..18.mp3 narration, one clip per scene (Azure, Ada)
      audio/manifest.json    the script, clip lengths, voice and format
      build_audio.py         regenerates the clips from the script
      verify.py              Playwright checks + the proof frames
      proof/                 19 moments, a poster, a phone width, reduced motion

## Two worlds

The animation cuts between them, the way the reference film does.

- **Paper.** A warm illustrated tissue: hatched ground, stippled matrix,
  fifty-odd drawn neighbour cells, our cell in the middle. House palette,
  boiling hand-drawn line, paper grain, vignette.
- **Slate.** The same subject "under the microscope" on `#2b2925`: chalk and
  teal wireframes, a faint dotted grid, ripples, measurement rules, tally
  marks and annotations in Caveat. It carries the technical beats — the
  cycle diagram, the chromosome count, the DNA copy, the spindle.

Cuts are hard, on the scene boundary, with a brief flash and a 2% scale pop
(and expanding rings when we land on slate). The camera opens wide on the
tissue, rushes into one cell at scene 5, and pulls back at the end to show
the two new cells among the many.

## Narration script

Written first, checked against AQA 4.1.2.2 before anything was drawn. Plain
GCSE English, British spelling, no exam board named.

1. Every second, your body replaces millions of worn-out cells.
2. New skin, new blood, new gut lining: all made by cells dividing.
3. When you cut your finger, cell division closes the wound.
4. Cells do this in a series of stages called the cell cycle.
5. Inside this cell, the nucleus holds the chromosomes.
6. In body cells they come in pairs: forty-six in all, in twenty-three pairs.
7. We draw two pairs here, so you can follow them.
8. First the cell grows, and makes more ribosomes and mitochondria.
9. Then the DNA is copied, so each chromosome becomes two identical copies.
10. The two copies stay joined together until they are pulled apart.
11. The copy must be exact, or the new cell gets the wrong instructions.
12. Now mitosis begins, and the membrane around the nucleus breaks down.
13. Fine fibres stretch out from each end of the cell.
14. They take hold of the chromosomes and line them up across the middle.
15. Then the fibres pull the copies apart, one set to each end.
16. A new membrane forms around each set, so the nucleus has divided.
17. Finally the cytoplasm and the cell membrane divide, making two cells.
18. Both new cells are genetically identical to the parent, and each can divide again.

## Scenes

The clip length drives everything. A scene's drawing runs for exactly the
length of its clip; then a 0.35 s beat of quiet before the next clip starts.
Durations are read from the `Audio` elements at load, so replacing a clip
re-times the animation with no code change.

| # | key | world | what is drawn | clip (s) | scene (s) |
|---|-----|-------|---------------|---------:|----------:|
| 1 | field | paper | a whole field of tissue, our cell in the middle | 4.42 | 4.77 |
| 2 | dividing | paper | four neighbours pinch and become eight cells | 5.14 | 5.49 |
| 3 | wound | paper | a tear opens in the tissue and new cells fill it | 3.84 | 4.19 |
| 4 | cycle | slate | the three-stage cycle dial draws itself, then shrinks into the corner | 4.01 | 4.36 |
| 5 | inside | paper | quick zoom to one cell; cell membrane, cytoplasm, nucleus labelled | 3.82 | 4.17 |
| 6 | count | slate | 23 pairs of chromosomes tally up to 46; two pairs lassoed | 5.28 | 5.63 |
| 7 | pairs | paper | our four chromosomes, bracketed as two pairs | 3.22 | 3.57 |
| 8 | growth | paper | the cell enlarges; ribosomes 14→30, mitochondria 3→6 | 4.68 | 5.03 |
| 9 | copy | slate | the copy draws itself on beside the original, then joins | 5.33 | 5.68 |
| 10 | joined | slate | the X, with the centromere ringed: two copies, joined here | 3.86 | 4.21 |
| 11 | exact | slate | matching bands down both copies: identical | 4.49 | 4.84 |
| 12 | envelope | paper | the nuclear envelope breaks into drifting fragments (*prophase*) | 4.75 | 5.10 |
| 13 | spindle | slate | poles glow, fibres draw on one at a time and take hold | 3.26 | 3.61 |
| 14 | align | paper | the four chromosomes on the equator (*metaphase*) | 3.79 | 4.14 |
| 15 | separate | paper | copies dart to the poles with motion trails (*anaphase*) | 4.34 | 4.69 |
| 16 | reform | paper | an envelope round each set; two nuclei labelled (*telophase*) | 4.80 | 5.15 |
| 17 | furrow | paper | the membrane pinches; cytoplasm and organelles split | 5.11 | 5.46 |
| 18 | settle | paper | pull back: two cells among many, genetically identical | 5.45 | 5.80 |

Total 85.9 s. Measured end to end in Chrome: 87.5 s from the first click to
the "Play again" state.

## Labels

Hand-lettered in Caveat on a leader line that draws itself out from the
thing, at 45 degrees and then flat, in screen space so the text keeps its
size whatever the camera does. Each one arrives as the narration names it
and fades as the scene ends: **cell membrane, cytoplasm, nucleus**
(scene 5), **chromosome** and a bracket reading **a pair** (7),
**ribosome, mitochondrion** (8), **two copies / joined here** (10),
**identical** (11), **nuclear membrane** (12), **spindle fibres** (13),
**nucleus** twice (16), **genetically identical** (18). The four phase names
stay as small handwritten notes, top left.

## The science

Straight from AQA 4.1.2.2 (`specs/aqa/science-8464-8464.md`, and the same
text in `specs/aqa/biology-8461-8461.md`), phrased to match lesson 2 of
`science-aqa / biology-paper-1`.

- The three overall stages the spec asks for: **grow and copy** (scenes
  8–11), **mitosis** (12–16), **divide** (17–18). The corner dial has one
  arc for each and fills as the cycle runs.
- 46 chromosomes in 23 pairs is stated once, counted on the slate, and then
  the drawing honestly says it is following two pairs.
- Diploid parent with **4 chromosomes = 2 pairs**. Length says which pair;
  colour says which member. Both daughters finish with one of each — long
  brown, long teal, short brown, short teal.
- The two chromatids of a chromosome are drawn from the same seed, mirrored,
  so they are identical by construction; the slate scene proves it with
  matching bands.
- Each chromatid is held by a fibre from the pole it travels to, attached at
  its centromere. In anaphase the centromere leads and the arms trail.
- The nuclear envelope is a double line, breaks down, and reforms round each
  set before the cytoplasm divides.
- Mitochondria and ribosomes double before division; both daughters get a
  share. No meiosis, no crossing over.

Known simplifications, all standard for GCSE diagrams:

- Chromosomes are shown inside the nucleus before replication. In a real
  interphase nucleus the chromatin is not condensed enough to see as
  separate chromosomes.
- Four chromosomes are drawn, not 46 — and the narration says so.
- The phase names appear only as light handwritten notes. The spec says
  students do not need them, so they never carry the explanation.
- Centrioles, kinetochores and the ER are not drawn.

## House style

Paper `#f6f1e7`, card `#fffdf8`, ink `#26231e`, line `#e4dfd2`, anchor brown
`#5b4632` for the chromosomes and the membrane line, one accent `#46706b`
for the other member of each pair. Slate `#2b2925`, chalk `#f0e8d8`, chalk
teal `#7fb9b0`. Schibsted Grotesk for the title, Literata for the narrated
sentence, Caveat for every label. Square 4px controls, no pills, no coloured
stripes, easing `cubic-bezier(.16, 1, .3, 1)`.

The painterly look is procedural: every shape is a wobbled outline painted
as three offset washes with a rim of gathered pigment and a hand line drawn
twice, cross-hatched for shading, over a generated paper grain and a
vignette. The wobble comes from a hash, so shapes are stable frame to frame
apart from a deliberate 7 fps boil of under a pixel. The tissue field is
rendered once to an offscreen canvas and moved with the camera.

`prefers-reduced-motion` turns off the boil, the drift, the pop and every
tween: each scene shows its finished state and the scrub steps through them.

## Rebuilding the audio

    python animations/mitosis/build_audio.py          # keeps existing clips
    python animations/mitosis/build_audio.py --force  # re-synthesises all 18

Azure Speech, `en-GB-AdaMultilingualNeural` (the site's even-lesson voice;
the cell cycle is lesson 2), 24 kHz 96 kbps mono MP3 — the house format from
`scripts/lib/narration.py`. Needs `AZURE_SPEECH_KEY`.

## What was verified

`python animations/mitosis/verify.py` in installed Chrome, with the repo
served from `_dev_server.py`:

- all 18 clips load (`readyState` ≥ 1) and every scene length equals its
  clip length plus the 0.35 s beat, to the millisecond;
- playback advances on the audio clock (2.48 s of scene 1 after 2.5 s);
- a full run passes through all 18 scenes and stops at "Play again" at
  87.5 s;
- the scrub jumps to a scene and swaps the sentence;
- reduced motion renders and steps with no errors;
- console clean, no failed requests, at 1300px and at 400px.

Proof frames are in `proof/`, one per stage, plus the poster, the phone
width and a reduced-motion frame.
