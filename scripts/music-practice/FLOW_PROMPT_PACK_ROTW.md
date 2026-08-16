# Flow prompt pack — Rhythms of the World gold gaps (music-ocr aos3-rhythms-listening)

Four clips, **two takes each** (`a`/`b`). WAV, 60–90 seconds for a clean
20–24 second trim. **No lyrics anywhere** — wordless vocals only where
stated. Idiom, instrumentation and technique only — no artist names, no
song imitation.

## What is missing and what is not

Real PD recordings already cover TWO regions' gold: Manyalawi (Cairo
1909) for the Eastern Mediterranean and Dengozo (1923 maxixe) for the
samba side of the Americas. The gaps are:

- **L1 India & Punjab** — no licence-clean early recordings circulate
  with provenance; needs (1) a bhangra groove and (2) an Indian
  classical texture.
- **L3 Africa** — no pre-1926 drum-ensemble recordings exist at all;
  needs a West African percussion ensemble.
- **L4 calypso half** — the 1920s Trinidad discs are composition-
  encumbered (Belasco, d. 1967); needs a steel pan band.

Generated clips ship with honest captions ("generated demonstration in
the style of…") and their gold questions rest ONLY on features the
verification stack confirms: tempo and metre by onset analysis,
groupings (3+3+2, swing ratio, layer-entry density) by the same
machinery that gates gen_rotw_rhythms.py, instrument presence by 2/3
blind Gemini votes.

---

## 1. `rotw_bhangra_a` / `_b` — modern bhangra groove (L1 gold)

> Instrumental Punjabi bhangra dance track. A big double-headed dhol
> drum leads throughout: deep bass strokes on the beats, sharp high
> cracks between them, in a swung eight-quaver groove at 102 beats per
> minute in steady 4/4. A short, twangy one-string tumbi riff repeats
> over the top, joined by hand claps and a shimmering tambourine.
> Modern club production underneath: a programmed kick reinforcing the
> dhol's bass strokes and a bright synth stab answering the riff.
> High energy, festival feel, built for dancing. No singing, no rapping,
> no film-orchestra strings, no tempo changes, no lyrics.

**Tests:** swung chaal subdivision (machine: swing ratio ≈2:1) · dhol
low-high alternation · steady duple metre at ~102 bpm · traditional
drum plus modern production (the spec's technology bullet).

## 2. `rotw_indian_classical_a` / `_b` — sitar, tabla and tanpura (L1 gold)

> North Indian classical trio texture. A tanpura drone hums constantly
> beneath everything. A sitar plays a flowing, heavily ornamented
> melodic line — slides between notes, quivering shakes around held
> tones — over a tabla pair keeping a clear repeating sixteen-beat
> cycle at a relaxed 72 beats per minute, with a firm stroke opening
> each cycle. The sitar phrases float across the cycle and land
> together with the tabla's strongest stroke. Intimate, focused,
> acoustic. No orchestra, no synthesisers, no Western drum kit, no
> singing, no lyrics.

**Tests:** constant drone (machine: sustained low-band energy) ·
melody-plus-drone-plus-percussion texture · slow steady pulse ·
ornamented/sliding melodic style (Gemini votes) · cycle-opening accent.

## 3. `rotw_african_ensemble_a` / `_b` — West African drum ensemble (L3 gold)

> A West African percussion ensemble recorded acoustically in an open
> space. It BUILDS IN STAGES: an iron bell pattern starts alone for the
> first ten seconds; a shaker joins; then a deep bass drum played with
> sticks; finally a hand-played lead drum on top, high and cracking.
> Underneath, the bell keeps a lilting three-feel while the bass drum
> pulls in two against it. In the final third, the lead drum breaks
> into short solo phrases answered each time by the full ensemble
> together. Around 96 beats per minute, rolling compound feel. Drums
> and bell only — no melody instruments, no synthesisers, no singing,
> no lyrics.

**Tests:** staged texture build (machine: onset density steps up at
each entry) · 3-against-2 cross-rhythm · call-and-response alternation
(machine: solo/tutti energy alternation) · hand-drum ensemble timbre
(Gemini votes).

## 4. `rotw_steelpan_a` / `_b` — steel pan calypso band (L4 gold)

> A Trinidad steel pan band playing an instrumental calypso. Bright
> lead tenor pans carry a cheerful singable melody, middle pans strum
> offbeat chords, a bass pan walks underneath. The groove sits in
> bright 4/4 at 116 beats per minute with the accents grouped
> three-three-two, pushed along by shaker, cowbell and a light drum
> kit. Sunny, carnival street-party feel, acoustically recorded.
> No synthesisers, no orchestra, no singing, no lyrics.

**Tests:** steel pan timbre (Gemini votes — pans are unmistakable) ·
3+3+2 accent grouping (machine) · duple metre ~116 bpm · lead / strum /
bass pan roles.

---

## Workflow after generation

Drop the WAVs in `scripts/music-practice/_rotw_flow/`. The validation
pass runs audio_features + onset checks + 3-vote Gemini probes per
take, A/B picks the winner, trims 20–24 s, loudnorms to I=-17, uploads
to `music-ocr/aos3-rhythms-listening/` and swaps the hard-synthetic
gold questions for real-feature questions wired to the new clips.
Nothing ships on a failed screen — the AoS2 pack's revision loop
applies unchanged.
