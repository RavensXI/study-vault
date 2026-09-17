# Storyboard: The cell cycle and mitosis

The plan every agent works from. Where this file and the art bible disagree on a position or a time, this file wins.

## Logline

One body cell grows, copies its chromosomes, and divides by mitosis into two genetically identical cells, one of which starts the cycle again.
Hand-inked paper shots of the cell and its tissue cut against navy blueprint shots of what is happening inside, every event on a beat grid, every pixel drawn in JavaScript.

## Numbers

- 120 bpm: beat 0.5 s (12 frames), bar 2 s (48 frames)
- 30 s = 15 bars = 720 frames at 24 fps, 1080×1920
- 11 shots, 2 to 4.5 s each, boundaries on the beat grid

## Summary

| Order | Id | Start | End | Mode | Title |
|---|---|---|---|---|---|
| 01 | hero-cell | 0.0 | 2.0 | illustrated | Cold open: one cell among many |
| 02 | cell-blueprint | 2.0 | 4.5 | schematic | Inside: nucleus, 23 pairs, the cycle |
| 03 | growth | 4.5 | 7.0 | illustrated | The cell grows |
| 04 | dna-copy-blueprint | 7.0 | 9.5 | schematic | The DNA is copied |
| 05 | copies-joined | 9.5 | 11.5 | illustrated | Two identical copies, joined |
| 06 | membrane-breaks | 11.5 | 13.5 | illustrated | Mitosis begins: the nuclear membrane goes |
| 07 | spindle-blueprint | 13.5 | 16.0 | schematic | Fibres line the chromosomes up |
| 08 | pull-apart | 16.0 | 19.0 | illustrated | The copies are pulled apart |
| 09 | two-nuclei-blueprint | 19.0 | 21.5 | schematic | Two new nuclei, the cell pinches |
| 10 | two-cells | 21.5 | 25.5 | illustrated | Two cells, pull back to the tissue |
| 11 | loop | 25.5 | 30.0 | illustrated | One daughter becomes the hero: the cycle loops |

## Structure

- Act 1, bars 1 to 4 (0 to 8 s): the cell and what it holds. Cold open, the blueprint of the nucleus and the 23 pairs, growth, and the DNA copy begins.
- Act 2, bars 5 to 6 (8 to 12 s): the copies. The copy completes and the chromosomes become joined pairs of identical copies. The hinge is the midpoint downbeat, T 12.0: the nuclear membrane breaks down and mitosis begins, with a cream flash.
- Act 3, bars 7 to 11 (12 to 22 s): mitosis. Spindle, line-up, pull apart, two nuclei.
- Act 4, bars 12 to 15 (22 to 30 s): two cells, the tissue, the loop.
- Match cuts: 01 to 02 (the cell outline, G1); 04 to 05 (the four X chromosomes, G2); 06 to 07 (chromosomes into the spindle, G2 to G3); 08 to 09 (the two chromosome sets at the poles, G3); 09 to 10 (the pinched cell into two cells, G4); 11 to 01 (the daughter cell lands on G1 for the loop).
- Push-ins and pull-backs: 04 pushes 6x into one chromosome then pulls back to the nucleus; 10 pulls back 0.45x to the tissue; 11 pushes back into one daughter to zoom 1 on G1.
- Time device: the cycle glyph, a ring at (900, 300) of radius 60 with three sectors, lit as the film advances: grow (T 4.5), copy (T 7.0), mitosis (T 12.0), complete (T 21.5). Shot 02 owns the canonical helper; every other shot copies it verbatim.
- The ending lands on the opening composition, so the film loops.

## Conventions

- `T` is global seconds, `t` is shot-local seconds (t = T − start). Every timestamp in a shot entry is global T.
- Camera moves use `lib.camera(ctx, { x, y, zoom, rot }, fn)`: the world point (x, y) maps to the frame centre (540, 960).
- Palette names come from the art bible. The two chromosome pairs are always chromoA (long, blue) and chromoB (short, rust), so a viewer can follow them across every cut.
- Hard cuts are the default. 06 declares `transitionIn: { kind: 'flash', dur: 0.125 }` for the hinge; 10 declares `{ kind: 'flash', dur: 0.125 }` for the division.
- Scenes clamp `t` past their duration during transitions.
- Text: none in schematic shots. On paper shots only `bracket({ label })` and `arcAnnotation({ label })` carry the five GCSE terms, one per shot at most: chromosome (05), nucleus (06), spindle (08), membrane (09), identical (10). The wordmark appears once, in 11.

## Shared geometry

Scenes copy these numbers exactly, or the match cuts jump.

### G1: the hero cell (01, 02, 03, 11 end)

Cell: an irregular near-circle, centre (540, 900), mean radius 380, drawn as a 40-point polyline with radius 380 + 14·noise; the nucleus a near-circle centre (540, 900), mean radius 170.
Membrane 6 px ink; nuclear membrane 4 px inkSoft.
Four chromosomes rest inside the nucleus as loose worm shapes (uncondensed but drawn, so they can be followed): chromoA1 centred (470, 850), chromoA2 centred (610, 850), each 130 px long; chromoB1 centred (480, 955), chromoB2 centred (600, 955), each 85 px long. All lie at 20 degrees off horizontal, alternately left and right.
Mitochondria: 6 beans, 60 by 28 px, at (300, 700), (760, 720), (280, 1060), (790, 1080), (420, 1190), (660, 640).
Ribosome stipple fills the cytoplasm at density 0.35 in inkFaint.
Neighbour cells: partial circles cut by the frame edge, centres (60, 380), (1020, 420), (40, 1420), (1040, 1400), (540, 1690), radius 300 to 360, drawn in the same style at 70 percent opacity.

### G2: the four X chromosomes after the copy (04 end, 05, 06 start)

Each chromosome is two identical copies joined at the centromere, drawn as an X: chromoA is 150 px tall with arms 40 px wide; chromoB is 100 px tall.
Centres as in G1: A1 (470, 850), A2 (610, 850), B1 (480, 955), B2 (600, 955), tilted 20 degrees alternately.
The centromere is a 14 px inkSoft disc at the crossing.

### G3: the spindle (07, 08, 09 start)

Poles (centrosomes) at (540, 430) and (540, 1370), each a 22 px disc with 12 radial ticks.
The metaphase plate is the line y = 900; at T 16.0 the four X chromosomes sit on it with centres at x 400 (A1), 495 (B1), 585 (B2), 680 (A2), upright (arms vertical).
Fibres: from each pole, one line to each centromere, plus 10 free fibres fanning to the far side.
At T 19.0 the copies have arrived: the upper set centred on y 560 (A at x 470 and 610, B at x 480 and 600), the lower set on y 1240, mirrored, each copy now a single-arm chromosome (half of its X), 5 px wide.
The cell outline during 07 and 08 elongates from the G1 circle to an ellipse of half-width 380 and half-height 520, centre (540, 900).

### G4: two daughter cells (09 end, 10 start)

The pinched cell at T 21.5: two near-circles, centres (540, 560) and (540, 1240), radius 300, joined by a neck 60 px wide at y 900 that closes on the cut.
Each daughter's nucleus: centre as the cell, radius 135, with its four single-copy chromosomes in the G1 arrangement scaled 0.8.

### G5: the cycle glyph (all shots; 02 owns the helper)

Ring centre (900, 300), radius 60, stroke 3 px; three sectors: grow from 12 o'clock clockwise 180 degrees, copy the next 90, mitosis the last 90.
Unlit sectors: inkFaint on paper, lavender 30 percent on blueprint. Lit: annYellow on paper, lineWhite on blueprint. A 6 px marker dot travels the ring with the film: at 12 o'clock at T 0, and reaching the end of each sector at T 7.0, T 12.0, T 21.5, then completing at T 30.
Sits inside the safe area (x 60 to 940, y 220 to 1540).

---

## 01 hero-cell: Cold open, one cell among many

T 0.0 to 2.0, illustrated, enters on the film start and the loop replay.

### Composition

Stripes in stripeCream and stripeYellow full bleed. The hero cell on G1 fills the middle of the frame; neighbours cut by the edges. Frame 0 is fully drawn.

### Forms

Membrane in ink with a doubled stroke; cytoplasm in cytoplasm with directional hatching in cytoHatch near the membrane; nucleus in nucleus with cross-hatch shadow along its lower left; nucleolus a 40 px disc in nucleusDeep at (500, 870); chromosomes as worm shapes in chromoA and chromoB with an ink outline; mitochondria in mito with inner ridge lines in mitoDeep; ribosome stipple in inkFaint.
Construction lines in inkFaint extend past the cell: the circle's diameters at 45 degrees and a faint square around it.

### Overlays

annBlue ring, radius 400 to 440, and a 90-degree annYellow arc with ticks over the top of the cell, the reference's cold-open geometry.

### Motion

T 0.000: full pose.
T 0.500 (beat): the cell "breathes" — membrane radius 380 to 392 and back over 3 drawings with outBack — and yellow and magenta rings burst from the nucleus (radius 170 to 520 over 6 frames, fading).
T 1.000, T 1.500: smaller breaths; the chromosomes wobble on twos.
Throughout: stripes drift 1 px per frame, ribosome stipple boils.

### Camera

Locked push-in, zoom 1.00 to 1.04 over the shot with inOutSine.

### Enter and exit

Enters from the loop (11's final frame is this frame). Exits on a hard cut to 02, a match cut on the G1 outline.

### Subject

Every second the body replaces millions of worn-out cells: skin, blood, gut lining, all made by cell division. A body cell holds its chromosomes in a nucleus; in body cells they come in pairs, 46 in 23 pairs. We draw two pairs so the viewer can follow them.

### Sound

T 0.0: the hook — a felt kick and a low pad swell in D minor; the four-note kalimba motif D5, F5, A5, E5 on 8ths.
T 0.5: a ring burst — an upward glass gliss over 200 ms and a soft crash.

---

## 02 cell-blueprint: Inside — nucleus, 23 pairs, the cycle

T 2.0 to 4.5, schematic, hard cut in.

### Composition

Blueprint base: navy, 60 px grid, guide circles of radius 470 and 640 centred (540, 900), corner diagonals. The cell on G1 as a double lavender outline; the nucleus as a lavender lattice disc; the four chromosomes as lattice worm shapes with glow dots at their centres. The cycle glyph G5 at (900, 300), unlit, its marker at 12 o'clock. A tally of 23 pairs: 46 short lineWhite ticks grouped in 23 pairs along an arc of radius 300 around the nucleus, from 8 o'clock to 4 o'clock clockwise. Height bracket at x = 900 from y 520 to 1280 (the cell's diameter).

### Forms

Lavender lattice weight for the outlines; hexLattice inside the nucleus at 18 px; glow dots (radius 10, 12 radial ticks) at the four chromosome centres; ticks and brackets in lineWhite at 60 percent.

### Motion

T 2.000: near-black navy with one white spark at (540, 900).
T 2.250: grid, circles and diagonals fade in over 6 frames; the outline draws round from 12 o'clock over 8 frames with outExpo.
T 2.500 (beat): the nucleus lattice sweeps in; the four glow dots pop with outBack on 16ths (2.5, 2.625, 2.75, 2.875).
T 3.000 (beat): the 46 ticks draw in pairs on 32nds along the arc, a magenta ring pulsing once per pair, finishing at T 3.75.
T 4.000 (beat): the cycle glyph draws (ring, then the three sector boundaries), and the marker dot appears at 12 o'clock with a magenta flash of radius 20 to 80 over 4 frames.
Throughout: the guide circles rotate 6 degrees across the shot; the lattice boils.

### Camera

Locked at zoom 1: the outline lies exactly on G1 at the cut.

### Enter and exit

Enters on a hard cut from the warm hero to near-black: the reference's spark beat. Exits on a hard cut to 03, back on the paper cell.

### Subject

The nucleus holds the chromosomes. In body cells they come in pairs, 46 in 23 pairs. Cells divide in a series of stages called the cell cycle: the cell grows, the DNA is copied, then mitosis.

### Sound

T 2.0: everything drops except a glassy sine ping on D6 with long reverb.
T 2.5: four rising bell pings on 16ths (D5, F5, A5, D6).
T 3.0 to 3.75: 23 paired plips climbing a D minor scale in 32nds, quiet, panned along the arc.
T 4.0: a soft gong on D3 and the kalimba motif returns on 8ths.

---

## 03 growth: The cell grows

T 4.5 to 7.0, illustrated, hard cut in.

### Composition

Stripes in stripeCream and stripeSage. The cell on G1, drawn as in 01, with more going on inside. The cycle glyph G5 with the grow sector lighting up across the shot. An annBlue ruler down the right side at x = 960 from y 520 to 1280 with a bracket that stretches as the cell grows.

### Forms

As 01. Mitochondria in mito; new ones drawn in over the shot. Ribosome stipple density rises from 0.35 to 0.6.

### Overlays

The ruler and growth bracket in annBlue; a tally ring at (180, 300) in annYellow that adds a tick per new mitochondrion.

### Motion

T 4.500: frame fully drawn, the glyph marker starts moving through the grow sector, reaching its end at T 7.0.
T 5.000 (beat): membrane mean radius 380 to 398 over 3 drawings with outBack; two mitochondria draw in at (360, 560) and (720, 1240) over 4 frames each.
T 5.500 (beat): radius to 414; two more mitochondria at (240, 900) and (840, 900); stipple density rises.
T 6.000 (beat): radius to 428; two more at (500, 1240) and (620, 560); the nucleus grows 170 to 185.
T 6.500 (beat): radius to 440 and holds; a yellow ring pulses from the nucleus.
Chromosomes wobble on twos throughout, unchanged in number.

### Camera

Locked, slow push zoom 1.00 to 1.03 with inOutSine.

### Enter and exit

Enters on a hard cut from the blueprint. Exits on a hard cut to 04, which opens on the nucleus.

### Subject

First the cell grows, and makes more ribosomes and mitochondria (sub-cellular structures). The chromosome number does not change during growth.

### Sound

T 4.5: brush pattern on 8ths and the pad rises a third.
T 5.0, 5.5, 6.0: a woody tock and a soft "chew" grain as each pair of mitochondria draws in; a plip per tally tick.
T 6.5: a warm glass ring on A5 for the pulse.

---

## 04 dna-copy-blueprint: The DNA is copied

T 7.0 to 9.5, schematic, hard cut in.

### Composition

Blueprint. Opens on the nucleus from G1 (centre (540, 900), radius 185 after growth) with the four chromosomes as lattice worms, then pushes 6x into chromoA1 so it fills the frame as a double helix, then pulls back to the nucleus where all four have become X shapes on G2. Cycle glyph: the copy sector lights across the shot, marker at its end at T 9.5. Bracket at x = 900 measuring the helix; a "1 → 2" is NOT written; the count is shown by ticks: one tick becomes two on each copy beat.

### Forms

Double helix: two lavender strands, 12 px apart at zoom, with lineWhite base-pair rungs every 14 px, seeded wobble. The new strands draw in in magenta then settle to lavender. X chromosomes on G2 in lattice weight with glow-dot centromeres.

### Motion

T 7.000: nucleus and four worms, marker starts.
T 7.250: push-in to chromoA1 over 12 frames with inOutCubic to zoom 6, centred on (470, 850).
T 7.750 (16th): the helix unzips from the top: the rungs split and the two strands separate over 8 frames.
T 8.000 (beat): new strands draw along each old strand from the top over 12 frames in magenta, rungs re-pairing, so two double helices lie side by side by T 8.5; a magenta flash at the fork on the beat.
T 8.500 (beat): pull back to zoom 1 over 12 frames with inOutCubic.
T 9.000 (beat): each worm becomes an X on G2 with outBack over 3 drawings, on 16ths: A1 at 9.0, A2 at 9.125, B1 at 9.25, B2 at 9.375; a tick under each splits into two ticks as it does.
T 9.375 to 9.5: hold on G2.

### Camera

The push-in and pull-back above; the G2 pose at T 9.5 is drawn screen-fixed so 05 matches exactly.

### Enter and exit

Enters on a hard cut from 03's cell. Exits on a hard cut to 05, a match cut on the four X shapes.

### Subject

Then the DNA is copied, so each chromosome becomes two identical copies. The two copies stay joined together until they are pulled apart. The copy must be exact, or the new cell gets the wrong instructions.

### Sound

T 7.0: cut to the blueprint drop, sine ping on D6.
T 7.25: a rising reverse swell under the push-in.
T 7.75: a zip — a fast downward noise sweep, high-passed.
T 8.0: a bell arpeggio in D minor pentatonic in 16ths tracks the new strands.
T 9.0, 9.125, 9.25, 9.375: four pings (D5, F5, A5, D6), one per X.

---

## 05 copies-joined: Two identical copies, joined

T 9.5 to 11.5, illustrated, hard cut in.

### Composition

Stripes in stripeCream and stripeApricot. The cell on G1 at radius 440 (after growth), the nucleus radius 185, and inside it the four X chromosomes on G2 in ink: chromoA and chromoB with an ink outline and cross-hatched arms. A bracket in annYellow under chromoA1 with the label "chromosome". An annBlue annotation arc joining the two arms of A1 with the label "identical".

### Forms

X chromosomes: each arm a rounded rod with hatching at 30 degrees; the centromere an inkSoft disc; a faint inkFaint centre line down each arm.

### Overlays

The bracket and arc above; a magenta ring on each centromere that pulses once on the beat.

### Motion

T 9.500: G2 pose, screen-fixed to match 04.
T 10.000 (beat): the four centromere rings pulse (radius 14 to 60 over 4 frames); the bracket draws in over 4 frames.
T 10.500 (beat): the "identical" arc draws from the left arm to the right arm of A1 over 6 frames; the two arms glow chromoA lighter for 3 drawings.
T 11.000 (beat): all four chromosomes tighten (condense): each X shrinks 6 percent with outBack and its hatching darkens.
Throughout: chromosomes wobble on twos; stripes drift.

### Camera

Locked at zoom 1.

### Enter and exit

Enters on a hard cut from the blueprint (match on G2). Exits on the hinge flash into 06.

### Subject

Each chromosome is now two identical copies joined at the centromere. They stay joined until they are pulled apart.

### Sound

T 9.5: kick and pad return; kalimba motif.
T 10.0: four soft tocks on 32nds as the rings pulse.
T 10.5: a glass gliss up a fifth for the arc.
T 11.0: a low thud and a tightening "creak" grain.

---

## 06 membrane-breaks: Mitosis begins — the nuclear membrane goes

T 11.5 to 13.5, illustrated, `transitionIn: { kind: 'flash', dur: 0.125 }`.

### Composition

Stripes in stripeCream and stripeApricot. Same cell as 05. The nuclear membrane breaks into dashes that drift outward and fade; the chromosomes condense fully and begin to drift toward the equator. Cycle glyph: the mitosis sector starts lighting at T 12.0. A bracket in annYellow around the fading nucleus labelled "nucleus".

### Forms

Membrane fragments: 24 inkSoft dashes of 30 to 60 px on the nucleus circle. Chromosomes on G2, darkened.

### Overlays

The bracket; an annBlue dotted circle where the nucleus was, fading with it.

### Motion

T 11.500: hold on the 05 pose through the flash.
T 12.000 (beat, the hinge): a cream flash (core), the nuclear membrane bursts into the 24 dashes which move outward 40 px over 6 frames with outExpo and fade over 12; the nucleolus dissolves as stipple.
T 12.500 (beat): the chromosomes shrink to 90 percent (condensed) with outBack; the two poles begin to show as faint inkFaint discs at (540, 430) and (540, 1370) drawing in over 8 frames.
T 13.000 (beat): the chromosomes drift toward y = 900, reaching the G3 metaphase positions at T 13.5 with inOutCubic; the cell outline begins to elongate toward the G3 ellipse (half-height 520 by T 13.5).

### Camera

Locked at zoom 1.

### Enter and exit

Enters on the flash from 05 (same pose). Exits on a hard cut to 07, a match cut on the chromosome positions (G3 at T 13.5, x 400, 495, 585, 680 on y 900) and the poles.

### Subject

Now mitosis begins, and the membrane around the nucleus breaks down.

### Sound

T 12.0: the hinge hit — a whump with a sub drop, a crash, everything else ducked; the pad modulates to D major.
T 12.5: a dry tock; T 13.0: a slow rising glide as the chromosomes gather.

---

## 07 spindle-blueprint: Fibres line the chromosomes up

T 13.5 to 16.0, schematic, hard cut in.

### Composition

Blueprint. The elongating cell as a lavender ellipse on G3, the two poles as glow dots with radial ticks, the four X chromosomes on the equator in lattice weight with glow-dot centromeres. Fibres draw from each pole to each centromere and 10 free fibres fan to the far side. A width bracket along y = 900 from x 340 to 740; ticks on the plate. Cycle glyph marker a quarter through the mitosis sector.

### Forms

Poles: 22 px discs with 12 ticks. Fibres: lineWhite at 45 percent, 2 px, seeded wobble, drawn with tracePath. Chromosomes: X lattice, 6 px.

### Motion

T 13.500: chromosomes already on the plate but loosely scattered ±40 px in y; poles bright.
T 14.000 (beat): fibres shoot from the top pole to each centromere over 6 frames with outExpo, one per 32nd; a magenta tick at each touch.
T 14.500 (beat): fibres from the bottom pole, likewise.
T 15.000 (beat): the chromosomes snap onto y = 900 exactly with outBack over 3 drawings and stand upright; the free fibres draw in.
T 15.500 (beat): the bracket draws along the plate; the fibres tremble (2 px wobble at 12 fps).

### Camera

Locked at zoom 1.

### Enter and exit

Enters on a hard cut from 06 (match on chromosomes and poles). Exits on a hard cut to 08 on the same geometry.

### Subject

Fine fibres stretch out from each end of the cell. They take hold of the chromosomes and line them up across the middle.

### Sound

T 13.5: blueprint drop, sine ping.
T 14.0 and 14.5: fibre draws as short pizzicato plucks on 32nds, rising for the top pole and falling for the bottom.
T 15.0: a bright ting on A5 as they snap to the plate; T 15.5: a tremolo shimmer.

---

## 08 pull-apart: The copies are pulled apart

T 16.0 to 19.0, illustrated, hard cut in.

### Composition

Stripes in stripeCream and stripeSky. The elongated cell as an ink ellipse on G3, poles as small hatched discs, fibres as thin inkSoft lines, the four X chromosomes on the plate in ink. A bracket in annYellow beside the fibres labelled "spindle". As the copies split, annBlue arrows follow them to the poles.

### Forms

As 05 for the chromosomes; fibres 2 px inkSoft, slightly wavy; poles hatched.

### Overlays

The bracket; annBlue motion arcs; two annYellow rings at the poles that pulse when the sets arrive.

### Motion

T 16.000: G3 metaphase pose, screen-fixed.
T 16.500 (beat): the fibres tighten (straighten) over 3 drawings; each centromere splits into two inkSoft discs 10 px apart.
T 17.000 (beat): the copies separate: each X becomes two single-arm chromosomes moving to opposite poles on twos, arriving by T 18.5 with inOutCubic; the trailing arms lag like a V.
T 18.000 (beat): the cell elongates further (half-height 560) and the poles move to (540, 400) and (540, 1400).
T 18.500 (beat): the sets arrive on G3's end positions (upper set on y 560, lower on y 1240); the pole rings pulse.
T 19.000: hold.

### Camera

Locked, slow pull zoom 1.00 to 0.97.

### Enter and exit

Enters on a hard cut from the blueprint (match on G3). Exits on a hard cut to 09, a match cut on the two sets at the poles.

### Subject

Then the fibres pull the copies apart, one set to each end. Each end receives one full set of chromosomes.

### Sound

T 16.0: kick and pad; kalimba motif in D major.
T 16.5: a creak as the fibres tighten.
T 17.0: a downward whoosh and a split "crack"; then a ratchet of plips on 16ths as the copies travel.
T 18.5: two glass rings, A5 then D6, one per pole.

---

## 09 two-nuclei-blueprint: Two new nuclei, the cell pinches

T 19.0 to 21.5, schematic, hard cut in.

### Composition

Blueprint. The elongated cell outline on G3, the two chromosome sets at the poles as lattice single-arm chromosomes. A new lattice membrane draws around each set (radius 135 around (540, 560) and (540, 1240)); the cell outline pinches at y = 900 into the G4 shape. Brackets measure each new nucleus. Cycle glyph marker three quarters through mitosis.

### Forms

Lattice membranes in lavender with a lineWhite rim; the pinch drawn as the outline pulled in by two opposing arcs; measurement brackets and ticks.

### Motion

T 19.000: the poles' rings fade; sets held.
T 19.500 (beat): the upper membrane draws round from 12 o'clock over 8 frames with outExpo; T 19.750: the lower one.
T 20.000 (beat): the fibres dissolve as stipple over 6 frames; the chromosomes relax into worm shapes (uncondense) with inOutSine over 12 frames.
T 20.500 (beat): the outline starts to pinch at y 900, the neck narrowing from 760 px to 60 px by T 21.5 with inOutCubic; a magenta ring marks the furrow on each beat (20.5, 21.0).
T 21.375: the G4 pose is reached and held to the cut.

### Camera

Locked at zoom 1.

### Enter and exit

Enters on a hard cut from 08 (match on the sets). Exits on the division flash into 10 (match on G4).

### Subject

A new membrane forms around each set, so the nucleus has divided. Then the cytoplasm and the cell membrane begin to divide.

### Sound

T 19.0: blueprint drop, sine ping.
T 19.5 and 19.75: two soft bell arpeggios, one per membrane.
T 20.0: a cave-reverb wash as the fibres dissolve.
T 20.5, 21.0: two low pulses with a tightening creak, a tock on each.

---

## 10 two-cells: Two cells, pull back to the tissue

T 21.5 to 25.5, illustrated, `transitionIn: { kind: 'flash', dur: 0.125 }`.

### Composition

Stripes in stripeCream and stripeYellow. The two daughter cells on G4 in ink, each with a nucleus and four single-copy chromosomes, mitochondria shared out. An annBlue arc joins the two nuclei with the label "identical". Cycle glyph completes its mitosis sector at T 21.5. Then the camera pulls back to 0.45 and the tissue appears: two dozen neighbour cells around the pair, several of them mid-division at different stages.

### Forms

As 01 for cell drawing. Neighbour cells in the same style at 80 percent; three of them show a pinch, one shows a spindle in miniature.

### Overlays

The arc; a yellow ring around each daughter on the beat; a tally ring at (180, 300) showing 1 then 2.

### Motion

T 21.500: flash in on the G4 pose; the neck closes on the beat over 3 drawings with outBack; both membranes seal with a small yellow ring each.
T 22.000 (beat): the "identical" arc draws over 6 frames; the tally ring flips 1 to 2.
T 22.500 (beat): pull back begins, zoom 1.00 to 0.45 over 36 frames with inOutCubic, centred (540, 900).
T 23.000 to 25.000: the tissue draws in around the pair as the camera pulls back, cells popping in on 16ths outward from the centre.
T 25.000 (beat): the field is full; the two daughters glow chromoA lighter for 3 drawings; hold.

### Camera

Locked to T 22.5, then the pull-back above.

### Enter and exit

Enters on the flash from 09 (match on G4). Exits on a hard cut to 11, which starts on the same wide tissue.

### Subject

Finally the cytoplasm and the cell membrane divide, making two cells. Both new cells are genetically identical to the parent, and each can divide again. New skin, blood and gut lining, and the closing of a cut, are all made this way.

### Sound

T 21.5: the division hit — a whump, a crash, and a two-note answer (D5, A5) with the kalimba.
T 22.0: a glass gliss for the arc; a plip for the tally.
T 22.5 to 25.0: a rising pad and marimba pattern in 16ths as the tissue fills, one plip per cell popping in, panned by position.
T 25.0: a warm gong on D3.

---

## 11 loop: One daughter becomes the hero — the cycle loops

T 25.5 to 30.0, illustrated, hard cut in.

### Composition

Opens on 10's final wide tissue. The camera pushes into the lower daughter so that by T 29.5 it sits exactly on G1 at zoom 1 with the 01 composition: stripes stripeCream and stripeYellow, neighbours at 01's positions, mitochondria and chromosomes in the G1 arrangement (the four single copies have grown back to the G1 worm shapes). The cycle glyph marker completes the ring at T 30.0. The wordmark, 24 px inkSoft in the house serif via `lib.text`, sits at (880, 1500) from T 28.5.

### Forms

As 01.

### Overlays

A yellow ring pulses from the nucleus at T 29.5, the same as 01's T 0.5 burst about to come.

### Motion

T 25.500: hold the wide tissue for one beat.
T 26.000 (beat): push-in begins, zoom 0.45 to 1.00 over 72 frames with inOutSine, the camera centre easing from (540, 900) to the point that lands the lower daughter on G1.
T 27.000, 28.000 (beats): as the daughter grows in frame its chromosomes relax from single copies into the G1 worm shapes, two neighbours redraw into 01's neighbour positions.
T 28.500: the wordmark fades in over 8 frames.
T 29.500 (beat): the frame equals 01's frame 0, screen-fixed; a yellow ring pulses.
T 30.000: cut to 01 (the loop).

### Camera

The push-in above; the last 12 frames are screen-fixed on G1.

### Enter and exit

Enters on a hard cut from 10 on the same wide frame. Exits into 01 on the loop.

### Subject

Each new cell can divide again: the cycle repeats. Body cells are replaced continuously by this cycle.

### Sound

T 25.5: the pad thins; the kalimba motif slows to quarter notes.
T 26.0 to 29.0: a long rising reverse swell under the push-in; a heartbeat kick on each beat, growing.
T 29.5: a glass ring on D6 that carries across the loop seam into 01's T 0.0 hit; the level matches bar 1 so the loop restarts cleanly.
