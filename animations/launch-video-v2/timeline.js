/* StudyVault launch videos v2 — the beat grid and the two edits (students, teachers), shared by the
   picture (comp.js) and the score (score.cjs).

   30 fps, 16 frames a beat -> 112.5 BPM; a bar is 64 frames (2.133 s).
   Each scene: id, bars, the kind of each bar (drives the arrangement), the transition that brings it
   in, and its key moments in BEATS from the scene's start. Cues name a key (or a beat) and a sound, so
   the picture and the music read the same numbers.

   Bar kinds: intro | drop | groove | build | break | stop | end
   Transitions: line (the opening wipe) | circle (a colour field grows out of the outgoing scene's exit
   point and collapses into the incoming scene's anchor) | bars (staggered colour bars sweep up) |
   field (the colour field stays: the scene is drawn on it) | zoom (the outgoing scene zooms through its
   exit point itself, then the circle collapse) */
(function (root) {
  const FPS = 30, BEAT = 16, BAR = 64;
  const BPM = FPS * 60 / BEAT;
  const C = { rust: '#c06325', green: '#2f7d4f', ink: '#2d2a26', navy: '#27466b' };

  const OPEN = { id: 'open', bars: 1, kinds: ['intro'],
    keys: { dot: 0, lock: 1, unlock: 2, swing: 2.5, collapse: 3.25, line: 3.5 },
    cues: [['dot', 'dot'], ['lock', 'thud'], ['unlock', 'unlock'], ['swing', 'swish'], ['collapse', 'suck'], [3, 'riser1']] };
  const HEAD = { id: 'head', bars: 2, kinds: ['drop', 'groove'], enter: { type: 'line' },
    keys: { w0: 1, w1: 1.5, w2: 2, w3: 2.5, stop: 3, boards: 4 },
    cues: [['w0', 'word'], ['w1', 'word'], ['w2', 'word'], ['w3', 'word'], ['stop', 'dot'], ['boards', 'board4']] };
  const END = (tag) => ({ id: 'end', bars: 2, kinds: ['stop', 'end'], enter: { type: 'circle', color: C.rust }, tag,
    keys: { hit: 1, letters: 1, lock: 1.75, close: 2.25, tag: 2.75, url: 3.5 },
    cues: [['hit', 'hit'], ['lock', 'swish'], ['close', 'lockclick'], ['tag', 'word'], ['url', 'word']] });

  const students = [
    OPEN, HEAD,
    { id: 'lesson', bars: 3, kinds: ['groove', 'break', 'groove'], enter: { type: 'circle', color: C.rust },
      keys: { read: 0.5, hear: 2, narr: 2.5, watch: 5.5, press: 6.5, play: 6.75 },
      cues: [['read', 'pop'], ['hear', 'pop'], ['watch', 'pop'], ['press', 'click'], ['play', 'swish']] },
    { id: 'flash', bars: 3, kinds: ['groove', 'groove', 'build'], enter: { type: 'bars', color: C.ink },
      keys: { cardIn: 0.25, typeFrom: 1, check: 4, tick: 5, flip: 6.5, zoom: 11 },
      cues: [['typeFrom', 'typing'], ['check', 'click'], ['tick', 'chime'], ['flip', 'flip'], ['zoom', 'riser1']] },
    { id: 'practice', bars: 4, kinds: ['drop', 'groove', 'groove', 'groove'], enter: { type: 'zoom', color: C.green },
      keys: { cardIn: 0.25, blocks: 1, off: 3, typeA: 3.5, tick: 5, fb: 5.5, streak: 6, swap: 8, tiles: 9, check2: 12, tick2: 13 },
      cues: [['blocks', 'blocks4'], ['off', 'pop'], ['typeA', 'typing3'], ['tick', 'chime'], ['streak', 'streak3'], ['swap', 'swish'], ['tiles', 'tiles5'], ['check2', 'click'], ['tick2', 'chime']] },
    { id: 'exam', bars: 3, kinds: ['groove', 'build', 'drop'], enter: { type: 'circle', color: C.green },
      keys: { cardIn: 0.25, lines: 1, submit: 4, marking: 4.5, mark: 8, fb1: 9, fb2: 10 },
      cues: [['lines', 'typing'], ['submit', 'click'], ['mark', 'impact'], ['fb1', 'pop'], ['fb2', 'pop']] },
    { id: 'widget', bars: 3, kinds: ['break', 'groove', 'groove'], enter: { type: 'bars', color: C.rust },
      keys: { cardIn: 0.25, pickWrong: 2, why: 3, next: 5.5, pickRight: 7, streak: 8 },
      cues: [['pickWrong', 'click'], ['why', 'buzz'], ['next', 'swish'], ['pickRight', 'click'], [7.25, 'chime'], ['streak', 'streak3']] },
    { id: 'free', bars: 1, kinds: ['drop'], enter: { type: 'field', color: C.rust },
      keys: { free: 0.25, ads: 1.5 },
      cues: [['free', 'word'], ['ads', 'word']] },
    END('Free GCSE revision. Every major exam board. No ads.'),
  ];

  const teachers = [
    OPEN, HEAD,
    { id: 'montage', bars: 3, kinds: ['drop', 'groove', 'groove'], enter: { type: 'circle', color: C.rust },
      keys: { f1: 0.25, f1tick: 2.5, f2: 4, f2tick: 6.5, f3: 8, f3mark: 10.5 },
      cues: [['f1tick', 'chime'], ['f2', 'swish'], ['f2tick', 'chime'], ['f3', 'swish'], ['f3mark', 'impact_s']] },
    { id: 'classes', bars: 3, kinds: ['groove', 'groove', 'groove'], enter: { type: 'bars', color: C.ink },
      keys: { cardIn: 0.25, brief: 1, figs: 3, p1: 6, p2: 7, p3: 8 },
      cues: [['brief', 'pop'], ['figs', 'count'], ['p1', 'pop'], ['p2', 'pop'], ['p3', 'pop']] },
    { id: 'markbook', bars: 2, kinds: ['break', 'groove'], enter: { type: 'circle', color: C.green },
      keys: { cardIn: 0.25, cells: 1, legend: 5 },
      cues: [['cells', 'cells'], ['legend', 'pop']] },
    { id: 'wrong', bars: 4, kinds: ['groove', 'build', 'drop', 'break'], enter: { type: 'bars', color: C.rust },
      keys: { cardIn: 0.25, rows: 1, light: 8, board: 10, open: 10.5, reveal: 13 },
      cues: [['rows', 'rows4'], ['light', 'impact'], ['board', 'click'], ['open', 'swish'], ['reveal', 'click'], [13.25, 'pop'], [13.625, 'chime']] },
    { id: 'summary', bars: 3, kinds: ['break', 'groove', 'groove'], enter: { type: 'circle', color: C.ink },
      keys: { cardIn: 0.25, h1: 1.5, h2: 4, h3: 6.5 },
      cues: [['cardIn', 'mail'], ['h1', 'pop'], ['h2', 'pop'], ['h3', 'pop']] },
    { id: 'pack', bars: 3, kinds: ['groove', 'groove', 'groove'], enter: { type: 'bars', color: C.green },
      keys: { cardIn: 0.25, bars: 2, wrongs: 5, para: 7 },
      cues: [['bars', 'blocks4'], ['wrongs', 'pop'], ['para', 'typing']] },
    { id: 'safe', bars: 3, kinds: ['break', 'break', 'groove'], enter: { type: 'circle', color: C.navy },
      keys: { cardIn: 0.25, body: 1.5, note: 3.5, review: 7 },
      cues: [['cardIn', 'mail'], ['note', 'pop'], ['review', 'click']] },
    { id: 'private', bars: 2, kinds: ['groove', 'build'], enter: { type: 'bars', color: C.ink },
      keys: { cardIn: 0.25, rows: 1, lock: 3.5, close: 4.5 },
      cues: [['rows', 'rows4'], ['lock', 'swish'], ['close', 'lockclick']] },
    Object.assign(END('For schools.'), { enter: { type: 'circle', color: C.ink } }),
  ];

  /* the opening headline's word beats: 'Every major GCSE subject' (4 words) keeps 1, 1.5, 2, 2.5; a
     department's 'GCSE History' (2) lands on 1.5 and 2.5, 'GCSE Combined Science' (3) on 1.5, 2, 2.5 */
  const headWordBeats = n => n >= 4 ? [1, 1.5, 2, 2.5] : n === 3 ? [1.5, 2, 2.5] : [1.5, 2.5];
  function build(scenes) {
    let bar = 0;
    const out = scenes.map(s => { const o = Object.assign({}, s, { bar0: bar, f0: bar * BAR, f1: (bar + s.bars) * BAR }); bar += s.bars; return o; });
    return { scenes: out, bars: bar, frames: bar * BAR };
  }
  const VIDEOS = { students: build(students), teachers: build(teachers) };
  const api = { FPS, BEAT, BAR, BPM, C, VIDEOS, headWordBeats, SEC: f => f / FPS };
  if (typeof module !== 'undefined') module.exports = api; else root.TL = api;
})(this);
