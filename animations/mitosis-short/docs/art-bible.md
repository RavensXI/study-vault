# Art bible: The cell cycle and mitosis

The visual rules every scene follows.
The look comes from `docs/reference-analysis.md`: warm ink illustration cut against navy blueprint.
Where this file and a scene brief disagree on a colour, weight or rule, this file wins.
Where this file and `docs/storyboard.md` disagree on a position or a time, the storyboard wins.

## 1. Frame

The canvas is 1080 px wide and 1920 px tall at 24 fps.
Every pixel value in this file assumes that size.
The origin is the top-left corner and y grows downward.

### 1.1 Shorts safe area

YouTube Shorts draws its own interface over the video.
The title and channel row covers roughly the bottom 380 px, the button column covers roughly x 950 to 1080 from y 1000 down, and the top bar covers roughly the top 180 px.
Anything the viewer must read (the subject, a match-cut shape, a glyph that carries meaning, the wordmark) sits inside x 60 to 940 and y 220 to 1540.
Backgrounds, stripes, grain, guide geometry, construction lines and decorative scenery run full bleed.

### 1.2 Composition for a tall frame

Compose for the height, never crop a square.
Hanging and climbing subjects use the vertical axis: the egg under the leaf, the J, the chrysalis, the emerging adult, the fir trunk.
The frame centre line x = 540 is the default axis for the subject.
Large subjects fill 60 to 90 percent of the frame width so they read on a phone.

## 2. Palettes

Names below are the keys of `FILM.lib.pal`.
Where a key already exists in `src/lib.js`, the value here is the published final value.
Colour is flat.
Tone in illustrated mode comes from hatching, never from gradients.
Radial glow halos are allowed only in schematic mode.

### 2.1 Warm illustrated palette (paper plate)

| Name | Hex | Use |
|---|---|---|
| paper | #EFE3C9 | Paper base |
| paperShade | #E2D1B0 | Paper shadow, tucked scale edges on white |
| paperDeep | #CDB58C | Paper vignette, deep paper tone |
| stripeCream | #F2E7CF | Stripe band A, default |
| stripeYellow | #EFDCA3 | Stripe band B, cold open and summer |
| stripeApricot | #F0D9B5 | Stripe band B, chrysalis and eclosion, dawn sky |
| stripeSage | #DCE3CC | Stripe band B, leaf and larva shots |
| stripeSpring | #E4EDD0 | Stripe band B, spring egg |
| stripeSky | #C9D3D2 | Stripe band B, migration sky |
| ink | #2A1C13 | Main outlines |
| inkSoft | #5B4331 | Secondary outlines, detail lines, egg ridges |
| inkFaint | #8A735C | Construction lines, graticule |
| tan | #C8A47A | Shed skin, dry grass |
| ochre | #C38F2E | Grass bands, autumn leaf patches |
| rose | #C88C86 | Dusty rose accents |
| duskRose | #E3B1A1 | Dusk sky band |
| sage | #94A47F | Generic foliage |
| teal | #3C8783 | Water hatching, teal accents |
| tealDeep | #285F5D | Deep water hatching |
| sun | #F1BF4A | Sun disc |
| nightSky | #4E3F6E | Night sky band |
| night | #2F2748 | Deepest night, star-field base |
| white | #FBF6EA | Highlights, latex beads, silk, floss, moon |

`orange #D8742B`, `leaf #6E8F4F`, `wood #A8784C`, `sunset #E79D8F`, `dusk #5A4878` and `red #BF3F2C` stay available in `lib.pal` for incidental scenery.

### 2.2 Cell extension, warm

| Name | Hex | Use |
|---|---|---|
| cytoplasm | #F1E3B8 | Cytoplasm fill inside the membrane |
| cytoHatch | #C9B382 | Directional hatching in the cytoplasm near the membrane |
| membrane | #2A1C13 | Cell membrane (ink), doubled stroke |
| nucleus | #C9A9C4 | Nucleus fill, mauve |
| nucleusDeep | #9A7A99 | Nucleus cross-hatch shadow, nucleolus |
| nucleusRim | #5B4331 | Nuclear membrane stroke (inkSoft) |
| chromoA | #4F6C9A | Chromosome pair A (long), blue |
| chromoADeep | #34496C | Hatching and outline on pair A |
| chromoALight | #7F9AC4 | Pair A glow when compared or arriving |
| chromoB | #B6603F | Chromosome pair B (short), rust |
| chromoBDeep | #7E3F28 | Hatching and outline on pair B |
| chromoBLight | #D48F6E | Pair B glow |
| centromere | #5B4331 | Centromere disc (inkSoft) |
| mito | #9DB08A | Mitochondria, sage |
| mitoDeep | #6F8A5E | Mitochondria inner ridges and hatching |
| ribosome | #8A735C | Ribosome stipple (inkFaint) |
| fibre | #6B7F8A | Spindle fibres on paper, slate blue-grey |
| pole | #7E9A63 | Centrosome discs on paper |
| neighbour | #E8DDBE | Neighbour cell cytoplasm at 70 to 80 percent |
| neighbourNucleus | #D3B9CF | Neighbour cell nuclei |
| membraneDash | #5B4331 | Fragments of the dissolving nuclear membrane |

### 2.3 Cool schematic palette (blueprint plate)

| Name | Hex | Use |
|---|---|---|
| navy | #0B1230 | Blueprint base |
| navyDeep | #060A1C | Near-black navy for the opening spark frame |
| navyLight | #18234D | Inset circle fills, panel tint |
| grid | #3A4A86 | 60 px grid lines |
| lavender | #C8C1EF | Main linework |
| lineWhite | #EEF0FF | Emphasis lines, veins, ticks |
| paleBlue | #9CC2EA | Secondary accent, frost |
| glow | #FFF3DC | Nucleus cores, sun glyph, glows |
| magenta | #FF3D98 | Moments of change only |
| hemolymph | #BFEFF5 | Fluid dots moving through veins |
| schemBlue | #9CC2EA | Chromosome pair A identity tint in blueprint (paleBlue) |
| schemRust | #F2A66A | Chromosome pair B identity tint in blueprint |

Subject tints are line or dot colours, never fills, and a schematic shot uses at most one of them besides magenta.

### 2.4 Overlay colours on illustrations

| Name | Hex | Use |
|---|---|---|
| annMagenta | #E43D8C | Change rings, trajectory of the migration, target rings |
| annBlue | #3B8EE0 | Trajectory and motion lines, fluid paths, rulers |
| annYellow | #EAB530 | Attention rings, brackets, tally rings, sun paths |
| teal | #3C8783 | Secondary guide lines when blue is already in use |

Overlays sit above the illustration at full opacity and never get hatched or grained.

## 3. Line

All widths are at 1080 px wide.
Illustrated lines come from `lib.inkPath` with pressure variation of plus or minus 25 percent.

### 3.1 Illustrated weights

| Element | Width | Colour and opacity |
|---|---|---|
| Hero subject outline | 5 px | ink 100% |
| Doubled hero outline, occasional | 1.5 px, offset 3 px | ink 40% |
| Secondary form outline | 3 px | ink 100% |
| Detail lines: segment rings, leaf veins, egg ridges | 1.8 px | inkSoft 90% |
| Hatch strokes | 1.2 to 1.8 px | ink or the form's deep colour, 70 to 90% |
| Construction lines | 1.5 px | inkFaint 30% |
| Wing veins on the adult | filled bands 10 to 18 px at a 1000 px wingspan, tapering toward the margin | veinBlack |

Scale wing-vein bands with the wingspan.
Female veins are about 1.3 times the male width.

### 3.2 Schematic weights

| Element | Width | Colour and opacity |
|---|---|---|
| Primary outline, double | outer 2.5 px and inner 1.5 px, 9 px apart | lavender 85% outer, 50% inner |
| Secondary outline | 1.5 px | lavender 60% |
| Lattice and cell lines | 1 px | lavender 30 to 40% |
| Grid | 1 px, 60 px pitch | grid 35% |
| Guide circles | 1.5 px | lavender 12 to 18% |
| Long diagonals | 1 px | lavender 12% |
| Ticks | 1.5 px, 10 to 20 px long | lineWhite 60% |
| Brackets | 1.5 px, end ticks 16 px | lavender 60% |
| Magenta flashes and rings | 3 px | magenta 100%, fading |

### 3.3 Overlay weights

| Element | Width |
|---|---|
| Attention and change rings | 3 px |
| Trajectory lines | 2.5 px |
| Dashed trajectories | 2.5 px, 14 px on and 10 px off |
| Motion rings | 2 px |
| Arc annotations | 2 px with 8 px end ticks |
| Rulers | 2 px, short ticks 12 px, long ticks 28 px |

## 4. Tone

### 4.1 Hatching

Light comes from the upper left, so shadow falls on the lower right of each form.
Only shadow sides and recesses get hatched, and lit sides stay flat colour.
The primary hatch runs at 45 degrees, rising from lower left to upper right.
Cross-hatch adds a second layer at 105 degrees for deep shadow.
Spacing sets the tone: 12 px for light shade, 8 px for mid shade, 5 px for dark shade, with the cross layer at 7 px.
Cylinders (stems, caterpillar bodies, the abdomen, the fir trunk) take contour hatching perpendicular to the long axis, slightly curved, 6 to 8 px apart, on the shadow half only.
Leaves take hatching parallel to the side veins, between the veins.
Bark takes lengthwise hatching.
Water takes horizontal hatching, and coastlines take engraved hatching parallel to the coast that fades with distance offshore.
Every stroke jitters: angle plus or minus 3 degrees, spacing plus or minus 15 percent, each end plus or minus 6 px.

### 4.2 Stipple

Stipple dots have a radius of 1.0 to 2.2 px.
Use stipple for leaf hairs, frost, stars, floss texture, yolk and tissue in blueprint, and the body texture of a butterfly seen very small.
Density runs from 0.002 dots per px² (sparse) to 0.02 dots per px² (dense).

### 4.3 Grain and boil

`core` lays paper grain over illustrated shots and fine noise over schematic shots, re-seeded on the 12 fps boil clock.
Scenes do not add their own full-frame grain.
Every ink and schematic line wobbles on the same 12 fps boil through `lib.boil(T)`, so still frames shimmer like drawn animation.

### 4.4 Stripes

The stripe background uses `lib.stripes` with a band width of 140 px at 30 degrees, rising left to right (`width: 140, angle: -0.52`).
Band A is stripeCream and band B changes by act, as listed in 2.1.
Stripes drift 6 px along their normal per beat unless a shot says otherwise.

## 5. Schematic language

The schematic shots explain what happens inside, and they never show the outside life.
Every schematic frame starts from `lib.blueprint`: navy base, 60 px grid, at least one large faint guide circle, and two long diagonals.
The subject is a double lavender outline with fine internal structure.
Cell structure is a lattice: hexagons (14 to 18 px cells) for tissue and eyes, rectangular cells for the egg shell and leaf section.
Nuclei and points of activity are glow dots: core radius 8 to 10 px in glow, halo radius 40 px, and 8 to 16 radial ticks 14 to 22 px long at 70 percent.
Measurement is shown with brackets, tick scales and arc annotations, never with numbers.
No text appears in any schematic shot except the final wordmark.
Relationships are shown as a network: thin curved lavender lines from a source region to small circular node glyphs 90 to 120 px across.
Magenta marks a moment of change (fertilisation, division, a breakdown, a lock-on, the heading) and each magenta event lasts at most 12 frames before fading.
A cycle glyph sits at (900, 300): a ring of radius 44 split into four arcs (egg, larva, pupa, adult, clockwise from the top), the current stage arc in lineWhite and the others in lavender 25 percent.

## 6. Overlays on illustrations

Overlays show what the drawing cannot: paths, attention, sound, time and scale.
They are thin rings, arcs, straight guide lines, rulers and brackets in the four overlay colours.
Rings expand with `outExpo` and fade over 5 to 12 frames.
Trajectory lines draw on behind a moving subject at 24 fps.
Every illustrated shot carries at least one overlay and at most four overlay colours at once.

## 7. Motion

### 7.1 The on-twos rule

Anything that is drawn as a character or object moves on twos: butterflies, caterpillars, wings, the chrysalis, falling capsules, seeds, particles.
Compute its pose from `lib.onTwos(t)`, so it changes 12 times a second and holds each drawing for 2 frames.
Camera moves, zooms, overlay draw-on progress and ring expansion run at a full 24 fps so they stay smooth.
Line wobble follows the 12 fps boil clock.

### 7.2 Timing

The beat is 0.5 s, which is 12 frames at 24 fps.
An 8th note is 6 frames and a 16th note is 3 frames.
Every pop, molt, division, cut and hit lands on a beat, an 8th or a 16th, exactly on the frame.
Pops use `outBack` over 3 frames with a 6 to 10 percent overshoot.
Draw-ons use `outExpo` over 6 frames.
Character motion never eases for longer than one beat, and only camera moves may run slower.
Motion should feel snappy, never floaty.

### 7.3 Determinism

Seed every random choice from `lib.hash(shotId, ...)` through `lib.rng`.
A scene draws from `t` alone and never depends on a previous frame.
A scene may be asked for `t` slightly beyond its duration during a transition, so clamp to the final pose.

## 8. Match cuts

A match cut keeps a shape on the same pixels across a mode change.
The shared geometry tables live in `docs/storyboard.md`, section "Shared geometry", and scenes copy those numbers exactly.
Line weights may change across the cut, positions may not.

## 9. Wordmark

The wordmark is the word `studyvault` in lowercase.
Draw it with `lib.text` in a thin system sans-serif (light weight), 44 px, letter-spacing 0.12 em, inkSoft at 85 percent on paper.
It is centred on x = 540 with its baseline at y = 1470, inside the Shorts safe area, and appears only in shot 11.

## 10. Subject reference

Draw from these facts.
Source: the GCSE Biology specification's cell-cycle content (a body cell's chromosomes in pairs; growth with more sub-cellular structures; DNA copied so each chromosome is two identical copies; mitosis where one set of chromosomes is pulled to each end and the nucleus divides; then the cytoplasm and membrane divide to give two identical cells) and the site's fact-checked mitosis lesson narration (animations/mitosis/audio/manifest.json).
Lines marked "general" come from standard cell biology.

### 10.1 The cell

A generic animal body cell: an irregular near-circle (never a perfect circle), a membrane as a single continuous line, cytoplasm filling it, one nucleus a little off centre.
No cell wall, no chloroplasts, no vacuole (those are plant features).
Inside the cytoplasm: mitochondria drawn as beans with folded inner ridges, and ribosomes drawn as fine stipple.
The nucleus is bounded by its own membrane and holds the chromosomes; a nucleolus is a denser disc inside it (general).

### 10.2 Chromosomes

Body cells hold 46 chromosomes in 23 pairs. We draw two pairs so the viewer can follow them: pair A long (chromoA), pair B short (chromoB). Both members of a pair are the same length; the two pairs differ.
Between divisions the chromosomes are long and thin and drawn as loose worm shapes in the nucleus; they are drawn, never hidden, so the count can be followed.
After the DNA is copied each chromosome is two identical copies joined at the centromere, drawn as an X: two arms of equal length meeting at a disc.
Just before and during mitosis the chromosomes condense: shorter, thicker, darker.
After the copies are pulled apart each copy is a single-arm chromosome (half an X); each daughter nucleus receives one copy of every chromosome, so each daughter has the same four we started with.

### 10.3 The cell cycle

Three stages in the order the film shows them: the cell grows and makes more ribosomes and mitochondria; the DNA is copied; mitosis.
Growth does not change the chromosome number.
The copy must be exact or the new cell gets the wrong instructions.

### 10.4 DNA copy

DNA is a double helix: two strands with base-pair rungs between them.
Copying: the strands separate (unzip) and a new strand is built along each old strand, giving two identical double helices (general).
The film shows this at 6x zoom on one chromosome; both new helices sit side by side and become the two arms of the X.

### 10.5 Mitosis

The nuclear membrane breaks down.
Fine fibres (the spindle) stretch out from each end of the cell; the two ends are the poles, each with a centrosome (general).
The fibres take hold of the chromosomes at the centromere and line them up across the middle of the cell.
The fibres shorten and pull the copies apart, one set to each end; the cell elongates as they do.
A new membrane forms around each set: the nucleus has divided.
Then the cytoplasm and the cell membrane divide by pinching in at the middle, making two cells.
Both new cells are genetically identical to the parent, and each can divide again.

### 10.6 Tissue

Body cells sit among many others; new skin, blood and gut lining, and the closing of a cut, are made by cell division.
In the wide tissue shots several neighbours are mid-division at different stages, so the field reads as living tissue.

### 10.7 Mistakes to avoid

- Drawing the cell as a perfect circle: draw an irregular near-circle with seeded wobble.
- A plant cell: no cell wall, chloroplasts or vacuole.
- More or fewer chromosomes than four, or pairs of unequal length: two pairs, four chromosomes, both members of a pair identical in length and colour.
- Copies of different sizes: the two arms of an X are identical.
- Chromosomes vanishing between shots: they are drawn in every shot, loose or condensed.
- The membrane breaking before the copy: the copy (04, 05) comes before the nuclear membrane breaks (06).
- Fibres attached anywhere but the centromere: they take hold at the centromere.
- Copies going to the same pole: one copy of each chromosome to each pole, so each daughter has four.
- The cell dividing before the two nuclei exist: two nuclei form (09) before the cytoplasm divides (10).
- Daughters drawn different from each other: they are the same size, with the same four chromosomes.
- Naming the exam board anywhere on screen.
