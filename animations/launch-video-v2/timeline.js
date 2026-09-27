/* StudyVault launch video v2 — the beat grid, shared by the score (score.cjs) and the picture (comp.js).
   30 fps, 16 frames a beat -> 112.5 BPM; an eighth is 8 frames, a sixteenth 4, a bar 64 (2.133 s).
   Stage 1 test clip: 6 bars and one beat = 400 frames = 13.33 s.
   Every key moment is written as F(bar, beat, sixteenth) so the cut, the pop and the drum hit that
   belong together share a frame. */
(function (root) {
  const FPS = 30, BEAT = 16, SIX = 4, BAR = 64;
  const F = (bar, beat = 0, six = 0) => bar * BAR + beat * BEAT + six * SIX;
  const FRAMES = F(6, 1);
  const BPM = FPS * 60 / BEAT;

  /* The test beat map. Names are used by comp.js (picture) and score.cjs (sound). */
  const K = {
    dotIn: F(0, 0),        // rust dot springs in on ink
    lockIn: F(0, 1),       // the dot grows into the padlock
    unlock: F(0, 2),       // the shackle lifts: click
    lockOut: F(0, 3),      // the padlock collapses back to a dot, the dot stretches into a line
    wipe: F(1, 0),         // the line opens into a full paper screen: IMPACT, groove starts
    w1: F(1, 1), w2: F(1, 1, 2), w3: F(1, 2),   // "Every" "GCSE" "subject." (the full stop is the dot)
    boards: F(1, 3),       // AQA, Edexcel, OCR, Eduqas on sixteenths
    textOut: F(2, 2),      // words mask out upwards; the full stop stays
    dotMove: F(2, 3),      // the full stop travels to the card's centre
    cardIn: F(3, 0),       // the flashcard springs out of the dot
    typeFrom: F(3, 1), typeTo: F(3, 3, 3),     // the pupil types (a key every other frame)
    check: F(4, 0),        // Check pressed: click
    tick: F(4, 1),         // green tick springs in: CHIME, "Checked instantly." reveals
    flip: F(4, 3),         // the card flips to the model answer: whoosh
    zoom: F(5, 2),         // zoom-through into the tick: riser
    collapse: F(5, 3),     // the green screen collapses into a dot on paper
    next: F(6, 0),         // the next scene's first frame: HIT
  };
  const api = { FPS, BEAT, SIX, BAR, F, FRAMES, BPM, K, SEC: f => f / FPS };
  if (typeof module !== 'undefined') module.exports = api; else root.TL = api;
})(this);
