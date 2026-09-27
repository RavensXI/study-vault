/* StudyVault launch video — the beat grid and every cue, shared by the score (score.cjs)
   and the picture (comp.js). Nothing here is in seconds except SEC(): everything is a frame
   on the grid, so a cut, a word and a drum hit that share a grid point share a frame.

   30 fps, 14 frames a beat  ->  128.571 BPM, a beat is exactly 0.4667 s, an eighth is 7 frames.
   21 bars of 4 beats = 1176 frames = 39.2 s. */
(function (root) {
  const FPS = 30, BEAT = 14, EIGHTH = 7, BAR = 56, BARS = 21, FRAMES = BAR * BARS;
  const BPM = FPS * 60 / BEAT;
  const F = (bar, beat = 0, eighth = 0) => bar * BAR + beat * BEAT + eighth * EIGHTH;
  const SEC = f => f / FPS;

  /* Sections: [id, first bar, bars]. Every cut is a downbeat. */
  const SECTIONS = [
    ['intro', 0, 1],      // the front door
    ['boards', 1, 1],     // 98 courses, four boards  (riser)
    ['drop', 2, 2],       // subject montage on eighths: 4,490 lessons / Free / No ads
    ['lesson', 4, 2],     // Read it / Hear it / Watch it
    ['cards', 6, 2],      // typed flashcards, tick on bar 7 beat 1
    ['maths', 8, 1],      // guided maths, ticks on beats
    ['spanish', 9, 1],    // vocab pairs snap on eighths
    ['english', 10, 1],   // traffic-light rows on eighths, Correct on the last eighth
    ['ai', 11, 2],        // exam answer typed, 4/4 lands on bar 12 beat 1
    ['widget', 13, 2],    // interactive: choices on beats, RIGHT on bar 14
    ['teacher', 15, 2],   // what the class gets wrong, rows on beats
    ['recap', 17, 1],     // four ticks on four beats  (riser)
    ['stop', 18, 1],      // two beats of silence, then the HIT on beat 2
    ['end', 19, 2],       // end card
  ].map(([id, bar, bars]) => ({ id, bar, bars, f0: F(bar), f1: F(bar + bars) }));

  /* Sound-and-picture cues. type: impact | whoosh | tick | pop | click | key | riser | stop | hit */
  const CUES = [];
  const cue = (f, type, extra) => CUES.push(Object.assign({ f, type }, extra || {}));

  // transitions: a whoosh that PEAKS on each cut (starts 5 frames early)
  SECTIONS.slice(1).forEach(s => { if (!['drop', 'stop', 'end', 'recap'].includes(s.id)) cue(s.f0 - 5, 'whoosh'); });
  // boards: four board names on eighths, riser into the drop
  [F(1, 1, 0), F(1, 1, 1), F(1, 2, 0), F(1, 2, 1)].forEach(f => cue(f, 'pop'));
  cue(F(1), 'riser', { len: BAR });
  cue(F(2), 'impact');
  // drop montage swaps on every eighth
  for (let i = 1; i < 16; i++) cue(F(2) + i * EIGHTH, 'click');
  cue(F(3), 'pop'); cue(F(3, 1), 'pop');
  // lesson: three camera jumps on beats
  cue(F(4, 2), 'click'); cue(F(5, 0), 'click');
  // flashcards: 8 key strokes on the eighths of bar 6, checking on bar 7 beat 0, tick on beat 1
  for (let i = 0; i < 8; i++) cue(F(6) + i * EIGHTH, 'key');
  cue(F(7, 0), 'click'); cue(F(7, 1), 'tick');
  // maths: type on eighths, ticks on beats 1 and 3
  cue(F(8, 0, 0), 'key'); cue(F(8, 0, 1), 'key'); cue(F(8, 1), 'tick');
  cue(F(8, 2, 0), 'key'); cue(F(8, 2, 1), 'key'); cue(F(8, 3), 'tick');
  // spanish: seven pairs on eighths 1..7
  for (let i = 1; i <= 7; i++) cue(F(9) + i * EIGHTH, 'pop', { n: i });
  // english: six rows on eighths 1..6, Correct on eighth 7
  for (let i = 1; i <= 6; i++) cue(F(10) + i * EIGHTH, 'pop', { n: i });
  cue(F(10, 3, 1), 'tick');
  // ai: typing through bar 11, click on bar 12 beat 0, the mark lands on beat 1
  for (let i = 0; i < 8; i++) cue(F(11) + i * EIGHTH, 'key');
  cue(F(12, 0), 'click'); cue(F(12, 1), 'impact', { small: true });
  // widget: two choices on beats 2 and 3, check on bar 14 beat 0 lands RIGHT
  cue(F(13, 2), 'click'); cue(F(13, 3), 'click'); cue(F(14, 0), 'tick');
  // teacher: five rows on beats, zoom on bar 16 beat 2
  for (let i = 0; i < 5; i++) cue(F(15, i < 4 ? i : 3, i < 4 ? 0 : 1), 'pop');
  cue(F(16, 2), 'click');
  // recap: four ticks on four beats, riser under
  for (let i = 0; i < 4; i++) cue(F(17, i), 'tick');
  cue(F(17), 'riser', { len: BAR });
  // stop-down and the hit
  cue(F(18, 0), 'stop'); cue(F(18, 2), 'hit');
  cue(F(19, 0), 'pop'); cue(F(19, 2), 'pop');

  const API = { FPS, BEAT, EIGHTH, BAR, BARS, FRAMES, BPM, F, SEC, SECTIONS, CUES };
  if (typeof module !== 'undefined') module.exports = API; else root.TL = API;
})(this);
