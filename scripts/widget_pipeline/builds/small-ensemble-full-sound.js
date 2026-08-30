/* Filling the texture: how few players can sound full.
   Self-contained lesson widget. No network, no audio, no storage.
   NOTHING here plays or imitates sound. The device is a register map:
   every part is drawn as the span of pitch it actually occupies, tagged
   with the job it does. Fullness is computed from that model alone -
   four register bands sounding, three or more separate jobs - so the
   drawing and the marking can never disagree. */
(function () {
  'use strict';

  var ID = 'small-ensemble-full-sound';

  /* ---------------- register model ----------------
     MIDI numbers, C4 = 60. The drawn axis is C2 (36) to C7 (96), which
     covers every part used below. Band edges are the ordinary choral /
     quartet divisions, and every span given to a part is inside the
     normal playing or singing range of that instrument or voice. */

  var NAMES = ['C', 'C♯', 'D', 'E♭', 'E', 'F', 'F♯', 'G', 'A♭', 'A', 'B♭', 'B'];
  function pname(m) { return NAMES[((m % 12) + 12) % 12] + (Math.floor(m / 12) - 1); }

  var AXIS_LO = 36, AXIS_HI = 96;
  function pct(m) { return ((m - AXIS_LO) / (AXIS_HI - AXIS_LO)) * 100; }

  var BANDS = [
    { name: 'Bass', lo: 36, hi: 53 },
    { name: 'Tenor', lo: 53, hi: 65 },
    { name: 'Alto', lo: 65, hi: 77 },
    { name: 'Treble', lo: 77, hi: 96 }
  ];
  var MIN_OVERLAP = 3;          /* semitones - integer test, no float edges */

  function sounding(p) { return !p.resting && p.hi > p.lo; }

  function bandCovered(parts, b) {
    for (var i = 0; i < parts.length; i++) {
      var p = parts[i];
      if (!sounding(p)) { continue; }
      if (Math.min(p.hi, b.hi) - Math.max(p.lo, b.lo) >= MIN_OVERLAP) { return true; }
    }
    return false;
  }
  function coverage(parts) {
    var out = [], i;
    for (i = 0; i < BANDS.length; i++) { out.push(bandCovered(parts, BANDS[i])); }
    return out;
  }
  function bandsCovered(parts) {
    var c = coverage(parts), k = 0, i;
    for (i = 0; i < c.length; i++) { if (c[i]) { k++; } }
    return k;
  }
  function roleList(parts) {
    var seen = [], i;
    for (i = 0; i < parts.length; i++) {
      var p = parts[i];
      if (!sounding(p) || !p.role) { continue; }
      if (seen.indexOf(p.role) < 0) { seen.push(p.role); }
    }
    return seen;
  }
  function playerCount(parts) {
    var n = 0, i;
    for (i = 0; i < parts.length; i++) { n += (parts[i].n || 1); }
    return n;
  }
  /* The whole verdict, in one line: the range is covered AND the parts
     are doing different jobs. Headcount is not in it anywhere. */
  function isFull(parts) {
    return bandsCovered(parts) === 4 && roleList(parts).length >= 3;
  }

  function applyOpt(base, o) {
    var out = [], i, k;
    for (i = 0; i < base.length; i++) {
      var p = base[i];
      var q = { name: p.name, role: p.role, lo: p.lo, hi: p.hi, n: p.n || 1, resting: !!p.resting };
      var s = o.set && o.set[p.name];
      if (s) {
        for (k in s) { if (Object.prototype.hasOwnProperty.call(s, k)) { q[k] = s[k]; } }
      }
      out.push(q);
    }
    if (o.add) {
      for (i = 0; i < o.add.length; i++) {
        var a = o.add[i];
        out.push({ name: a.name, role: a.role, lo: a.lo, hi: a.hi, n: a.n || 1, resting: false });
      }
    }
    return out;
  }

  /* Two kinds of change, kept apart on purpose. A bar that MOVED is the
     thing the student altered about the sound; a part that merely gained
     doublers changed its headcount and nothing else, and the drawing has
     to say so - that is the whole misconception. */
  function baseOf(base, part) {
    for (var i = 0; i < base.length; i++) {
      if (base[i].name === part.name) { return base[i]; }
    }
    return null;
  }
  function barMoved(base, part) {
    var b = baseOf(base, part);
    if (!b) { return true; }    /* a part that was not there before */
    return b.lo !== part.lo || b.hi !== part.hi || b.role !== part.role ||
           !!b.resting !== !!part.resting;
  }
  function countChanged(base, part) {
    var b = baseOf(base, part);
    if (!b) { return false; }
    return (b.n || 1) !== (part.n || 1);
  }

  /* ---------------- rounds ----------------
     Every round offers the misconception as a real, committable answer:
     that a full sound needs more players. Every round's verdict is
     computed by isFull() on the applied ensemble, never authored. */

  var ROUNDS = [
    {
      id: 'quartet-crowded', ensemble: 'String quartet',
      frame: 'A string quartet must sound full here, but all four players crowd the top of the range. Choose the one change that fills the texture.',
      parts: [
        { name: 'Violin I', role: 'melody', lo: 72, hi: 84 },
        { name: 'Violin II', role: 'melody', lo: 72, hi: 84 },
        { name: 'Viola', role: 'inner harmony', lo: 67, hi: 76 },
        { name: 'Cello', role: 'inner harmony', lo: 65, hi: 74 }
      ],
      options: [
        {
          label: 'Cello to the bass, viola to the middle',
          short: 'the cello and viola down',
          set: { Cello: { role: 'bass line', lo: 40, hi: 55 }, Viola: { lo: 55, hi: 67 } },
          fb: 'Same four players — but the cello now holds the floor and the viola the middle.'
        },
        {
          mis: true,
          label: 'Four is too few — hire eight more players',
          short: 'eight more players',
          set: {
            'Violin I': { n: 3 }, 'Violin II': { n: 3 }, Viola: { n: 3 }, Cello: { n: 3 }
          },
          fb: 'Twelve players, and not one bar moved. They are all crowded into the same two bands.'
        },
        {
          label: 'Play the whole passage fortissimo',
          short: 'fortissimo',
          set: {},
          fb: 'Loud is not full. Fortissimo pushes the same two bands harder and leaves the bottom silent.'
        },
        {
          label: 'Double-stops on both violins',
          short: 'double-stops on the violins',
          set: { 'Violin I': { lo: 69 }, 'Violin II': { lo: 69 } },
          fb: 'Double-stops add notes, but both notes are up top. The bars widen; the bass stays empty.'
        }
      ]
    },
    {
      id: 'wind-quintet-floor', ensemble: 'Wind quintet',
      frame: 'Three of this wind quintet crowd the tune up top while horn and bassoon rest. Choose the one change that fills the texture.',
      parts: [
        { name: 'Flute', role: 'melody', lo: 74, hi: 86 },
        { name: 'Oboe', role: 'melody', lo: 74, hi: 84 },
        { name: 'Clarinet', role: 'melody', lo: 72, hi: 84 },
        { name: 'Horn', role: null, lo: 0, hi: 0, resting: true },
        { name: 'Bassoon', role: null, lo: 0, hi: 0, resting: true }
      ],
      options: [
        {
          label: 'Bassoon on the bass, horn in the middle',
          short: 'bassoon on the bass, horn in the middle',
          set: {
            Bassoon: { role: 'bass line', lo: 36, hi: 53, resting: false },
            Horn: { role: 'inner harmony', lo: 53, hi: 67, resting: false }
          },
          fb: 'Five players still: the bassoon gives a floor, the horn fills the middle.'
        },
        {
          mis: true,
          label: 'Five is too few — add three more players',
          short: 'three more players',
          set: { Flute: { n: 2 }, Oboe: { n: 2 }, Clarinet: { n: 2 } },
          fb: 'Eight players now, on three lines that already existed. Not one bar moved downwards.'
        },
        {
          label: 'Clarinet down an octave, same tune',
          short: 'the clarinet down an octave',
          set: { Clarinet: { lo: 60, hi: 72 } },
          fb: 'That fills the middle, but the bass is still silent and all three are still on the tune.'
        },
        {
          label: 'All three higher and louder',
          short: 'higher and louder',
          set: {
            Flute: { lo: 79, hi: 91 }, Oboe: { lo: 79, hi: 88 }, Clarinet: { lo: 77, hi: 86 }
          },
          fb: 'Higher and louder empties the middle instead of filling it — everything is now up top.'
        }
      ]
    },
    {
      id: 'duet-to-trio', ensemble: 'Vocal ensemble',
      frame: 'Two characters sing a duet in thirds, high and close together. Choose the one change that fills the texture for the climax.',
      parts: [
        { name: 'Soprano', role: 'melody', lo: 69, hi: 81 },
        { name: 'Mezzo', role: 'inner harmony', lo: 65, hi: 77 }
      ],
      options: [
        {
          label: 'Add a bass voice two octaves below',
          short: 'a bass voice below',
          add: [{ name: 'Bass', role: 'bass line', lo: 41, hi: 57 }],
          fb: 'Three voices. The bass reaches two octaves below the duet and anchors the harmony.'
        },
        {
          mis: true,
          label: 'Two can never sound full — add twenty',
          short: 'twenty singers on the tune',
          set: { Soprano: { n: 20 } },
          fb: 'Twenty on one line is louder, not fuller. One line is one line, however many sing it.'
        },
        {
          label: 'Add a descant above the two voices',
          short: 'a descant above',
          add: [{ name: 'Descant', role: 'countermelody', lo: 79, hi: 86 }],
          fb: 'A descant adds sparkle over the top. The bottom two thirds of the range is still silent.'
        },
        {
          label: 'Second mezzo on the same harmony line',
          short: 'a second mezzo on the harmony',
          set: { Mezzo: { n: 2 } },
          fb: 'Two singers on one harmony line is still one harmony line. Nothing new sounds.'
        }
      ]
    },
    {
      id: 'octave-unison', ensemble: 'String quartet',
      frame: 'All four players have the same tune, doubled in octaves. Choose the one change that turns this into a texture.',
      parts: [
        { name: 'Violin I', role: 'melody', lo: 72, hi: 84 },
        { name: 'Violin II', role: 'melody', lo: 72, hi: 84 },
        { name: 'Viola', role: 'melody', lo: 60, hi: 72 },
        { name: 'Cello', role: 'melody', lo: 48, hi: 60 }
      ],
      options: [
        {
          label: 'Give the lower three separate jobs',
          short: 'separate jobs for the lower three',
          set: {
            Cello: { role: 'bass line', lo: 40, hi: 55 },
            Viola: { role: 'inner harmony', lo: 55, hi: 67 },
            'Violin II': { role: 'countermelody', lo: 65, hi: 77 }
          },
          fb: 'Now a bass, an inner part and a countermelody answer the tune.'
        },
        {
          mis: true,
          label: 'Add eight more players to the tune',
          short: 'eight more players',
          set: {
            'Violin I': { n: 3 }, 'Violin II': { n: 3 }, Viola: { n: 3 }, Cello: { n: 3 }
          },
          fb: 'Twelve players on one tune is a loud unison, not a texture. Nothing answers anything.'
        },
        {
          label: 'Violin II a third above, same tune',
          short: 'Violin II a third above',
          set: { 'Violin II': { lo: 76, hi: 88 } },
          fb: 'A third above is the same tune in parallel — nobody holds a bass or an inner part.'
        },
        {
          label: 'Double-stops for all four players',
          short: 'double-stops for all four',
          set: {
            'Violin I': { lo: 67 }, 'Violin II': { lo: 67 }, Viola: { lo: 55 }, Cello: { lo: 43 }
          },
          fb: 'Double-stops thicken each line, yet everyone is still following the same tune.'
        }
      ]
    },
    {
      id: 'hollow-middle', ensemble: 'String quartet',
      frame: 'The tune sits high, the bass line low, and two of the four are resting. Choose the one change that fills the texture.',
      parts: [
        { name: 'Violin I', role: 'melody', lo: 79, hi: 91 },
        { name: 'Violin II', role: null, lo: 0, hi: 0, resting: true },
        { name: 'Viola', role: null, lo: 0, hi: 0, resting: true },
        { name: 'Cello', role: 'bass line', lo: 40, hi: 52 }
      ],
      options: [
        {
          label: 'Wake the viola and Violin II',
          short: 'the viola and Violin II back in',
          set: {
            Viola: { role: 'inner harmony', lo: 55, hi: 67, resting: false },
            'Violin II': { role: 'countermelody', lo: 67, hi: 79, resting: false }
          },
          fb: 'The same four players. Two of them were silent; now they carry the middle of the range.'
        },
        {
          mis: true,
          label: 'Too few players — add a cello and a violin',
          short: 'two more players',
          set: { Cello: { n: 2 }, 'Violin I': { n: 2 } },
          fb: 'You hired two more while the viola and Violin II sat silent. The middle is still empty.'
        },
        {
          label: 'Cello up an octave, nearer the tune',
          short: 'the cello up an octave',
          set: { Cello: { lo: 52, hi: 64 } },
          fb: 'You moved the hole instead of filling it — the middle gains a line, the bass loses one.'
        },
        {
          label: 'Decorated runs above the tune',
          short: 'runs above the tune',
          set: { 'Violin I': { hi: 93 } },
          fb: 'Decoration sits on top of sound that is already there. The gap is in the middle.'
        }
      ]
    }
  ];

  var MASTERY = 'Three in a row — you have it. Fullness comes from covering the range and giving each part its own job, not from numbers.';
  var WORDS = ['no', 'one', 'two', 'three', 'four', 'five'];

  function listWords(a) {
    if (a.length === 1) { return a[0]; }
    return a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1];
  }

  /* The sentence that reports the model, computed from the parts alone. */
  function mapNote(parts) {
    var c = coverage(parts), gaps = [], i;
    for (i = 0; i < BANDS.length; i++) { if (!c[i]) { gaps.push(BANDS[i].name.toLowerCase()); } }
    if (gaps.length) { return 'Still empty: ' + listWords(gaps) + '.'; }
    var r = roleList(parts).length;
    if (r < 3) { return 'Every band sounds, but the parts share only ' + WORDS[r] + (r === 1 ? ' job.' : ' jobs.'); }
    return 'All four bands sounding, ' + WORDS[r] + ' different jobs.';
  }

  /* ---------------- mount ---------------- */

  function mount(root, ctx) {
    ctx = ctx || {};
    var cs = window.getComputedStyle(root);
    var accent = (cs.getPropertyValue('--accent') || '').trim() || ctx.accent || '#8a6a4f';
    var still = !!ctx.reducedMotion;

    root.className = (root.className ? root.className + ' ' : '') + 'svw-ensfull';

    var css = [
      '.svw-ensfull{position:relative;background:#fff;border:1px solid #e8e3db;border-radius:16px;padding:.9rem;',
      'font-family:Inter,system-ui,-apple-system,sans-serif;color:#2d2a26;-webkit-text-size-adjust:100%;}',
      '.svw-ensfull *{box-sizing:border-box;}',
      '.svw-ensfull .kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:' + accent + ';margin:0 0 .15rem;}',
      '.svw-ensfull h3{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.18rem;line-height:1.2;margin:0 0 .2rem;}',
      '.svw-ensfull .frame{font-size:.82rem;line-height:1.38;margin:0 0 .35rem;color:#3a352e;}',
      '.svw-ensfull .stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.35rem .5rem .35rem;margin:0 0 .4rem;}',
      '.svw-ensfull .ens{font-size:.72rem;line-height:1.3;color:#8d8880;margin:0 0 .25rem;}',
      '.svw-ensfull .ens b{color:#2d2a26;font-weight:600;}',
      '.svw-ensfull .ens .cnt{color:#2d2a26;font-weight:600;font-variant-numeric:tabular-nums;}',
      '.svw-ensfull .map{position:relative;}',
      '.svw-ensfull .lanes{position:absolute;left:0;right:0;top:0;bottom:0;display:flex;pointer-events:none;}',
      '.svw-ensfull .lane{height:100%;}',
      '.svw-ensfull .lane+.lane{box-shadow:inset 1px 0 0 #e6dfd2;}',
      '.svw-ensfull .lane.gap{background:#ebe1cf;}',
      '.svw-ensfull .heads{position:relative;display:flex;margin:0 0 3px;}',
      '.svw-ensfull .bh{font-size:.66rem;font-weight:600;letter-spacing:.03em;color:#a09a90;',
      'white-space:nowrap;overflow:hidden;}',
      '.svw-ensfull .rows{position:relative;}',
      '.svw-ensfull .row{margin:0 0 5px;}',
      '.svw-ensfull .row:last-child{margin-bottom:0;}',
      '.svw-ensfull .rlab{font-size:.7rem;line-height:1.2;color:#7d766d;margin:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}',
      '.svw-ensfull .rlab b{color:#2d2a26;font-weight:600;}',
      '.svw-ensfull .row.chg .rlab b,.svw-ensfull .row.more .rlab b{color:' + accent + ';}',
      '.svw-ensfull .trk{position:relative;height:8px;}',
      '.svw-ensfull .trk:before{content:"";position:absolute;left:0;right:0;top:4px;height:1px;background:#ded6c8;}',
      '.svw-ensfull .row.rest .trk:before{background:#eae3d6;}',
      '.svw-ensfull .bar{position:absolute;top:0;bottom:0;border-radius:2px;background:#4a443c;}',
      '.svw-ensfull .row.chg .bar{background:' + accent + ';}',
      '.svw-ensfull .opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:.28rem;margin:0 0 .4rem;max-width:640px;}',
      '.svw-ensfull .opt{font:600 .82rem Inter,system-ui,sans-serif;color:#2d2a26;padding:.4rem .6rem;border-radius:10px;',
      'border:1px solid #ddd7cd;background:#faf8f5;cursor:pointer;text-align:left;width:100%;line-height:1.3;}',
      '.svw-ensfull .opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff;}',
      '.svw-ensfull .opt[disabled]{cursor:default;opacity:.92;}',
      '.svw-ensfull .bar-row{display:flex;align-items:center;gap:.55rem;flex-wrap:wrap;margin:0 0 .35rem;}',
      '.svw-ensfull .go{font:600 .82rem Inter,system-ui,sans-serif;color:#fff;background:#2d2a26;border:1px solid #2d2a26;',
      'padding:.45rem .9rem;border-radius:10px;cursor:pointer;}',
      '.svw-ensfull .go[disabled]{background:#faf8f5;border-color:#ddd7cd;color:#a9a298;cursor:default;}',
      '.svw-ensfull .run{font-size:.74rem;color:#8d8880;}',
      '.svw-ensfull .run.done{color:#4f7d63;font-weight:600;}',
      '.svw-ensfull .cap{font-size:.82rem;line-height:1.4;margin:0;color:#3a352e;min-height:3.1em;}',
      '.svw-ensfull .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;}'
    ].join('');
    if (!still) {
      css += '.svw-ensfull .opt,.svw-ensfull .bar,.svw-ensfull .lane{transition:background-color .16s ease,border-color .16s ease,color .16s ease,left .2s ease,width .2s ease;}';
    }

    var style = document.createElement('style');
    style.textContent = css;
    root.appendChild(style);

    function el(tag, cls, text) {
      var n = document.createElement(tag);
      if (cls) { n.className = cls; }
      if (text != null) { n.textContent = text; }
      return n;
    }

    root.appendChild(el('p', 'kick', 'Ensemble texture'));
    root.appendChild(el('h3', null, 'Filling the texture'));
    var frameEl = el('p', 'frame', '');
    root.appendChild(frameEl);

    var stage = el('div', 'stage');
    var ensEl = el('p', 'ens', '');
    stage.appendChild(ensEl);

    var map = el('div', 'map');
    var lanesEl = el('div', 'lanes');
    var laneNodes = [], headNodes = [], i;
    var headsEl = el('div', 'heads');
    for (i = 0; i < BANDS.length; i++) {
      var w = (pct(BANDS[i].hi) - pct(BANDS[i].lo)) + '%';
      var ln = el('div', 'lane');
      ln.style.width = w;
      lanesEl.appendChild(ln);
      laneNodes.push(ln);
      var hd = el('div', 'bh', BANDS[i].name);
      hd.style.width = w;
      headsEl.appendChild(hd);
      headNodes.push(hd);
    }
    map.appendChild(lanesEl);
    map.appendChild(headsEl);

    var rowsEl = el('div', 'rows');
    var rowNodes = [];
    for (i = 0; i < 5; i++) {
      var rw = el('div', 'row');
      rw.appendChild(el('p', 'rlab', ''));
      var trk = el('div', 'trk');
      trk.appendChild(el('span', 'bar'));
      rw.appendChild(trk);
      rowsEl.appendChild(rw);
      rowNodes.push(rw);
    }
    map.appendChild(rowsEl);
    stage.appendChild(map);
    root.appendChild(stage);

    var optsEl = el('div', 'opts');
    var optNodes = [];
    for (i = 0; i < 4; i++) {
      var o = el('button', 'opt', '');
      o.type = 'button';
      o.setAttribute('aria-pressed', 'false');
      o.setAttribute('data-i', String(i));
      optsEl.appendChild(o);
      optNodes.push(o);
    }
    root.appendChild(optsEl);

    var barRow = el('div', 'bar-row');
    var go = el('button', 'go', 'Check');
    go.type = 'button';
    go.disabled = true;
    var run = el('span', 'run', '');
    barRow.appendChild(go);
    barRow.appendChild(run);
    root.appendChild(barRow);

    var cap = el('p', 'cap', '');
    root.appendChild(cap);
    var sr = el('p', 'sr');
    sr.setAttribute('aria-live', 'polite');
    root.appendChild(sr);

    /* ---------------- state ---------------- */
    var offset = Math.floor(Math.random() * ROUNDS.length);
    var n = 0, streak = 0, attempted = 0, mastered = false;
    var round = null, shown = null, current = null, picked = -1, checked = false;

    function pushState(extra) {
      var st = {
        streak: streak, mastered: mastered, attempted: attempted,
        round: round ? round.id : null,
        ensemble: round ? round.ensemble : null,
        players: current ? playerCount(current) : null,
        bands: current ? bandsCovered(current) : null,
        roles: current ? roleList(current).length : null,
        full: current ? isFull(current) : null
      };
      if (extra) {
        for (var k in extra) {
          if (Object.prototype.hasOwnProperty.call(extra, k)) { st[k] = extra[k]; }
        }
      }
      root.dataset.svState = JSON.stringify(st);
    }

    function paintMap(parts, committed) {
      var cov = coverage(parts), j;
      ensEl.textContent = '';
      var b = document.createElement('b');
      b.textContent = round.ensemble;
      ensEl.appendChild(b);
      ensEl.appendChild(document.createTextNode(' · '));
      var c = document.createElement('span');
      c.className = 'cnt';
      c.textContent = String(playerCount(parts));
      ensEl.appendChild(c);
      ensEl.appendChild(document.createTextNode(' players'));

      for (j = 0; j < BANDS.length; j++) {
        var empty = committed && !cov[j];
        laneNodes[j].className = 'lane' + (empty ? ' gap' : '');
        headNodes[j].textContent = BANDS[j].name + (empty ? ' gap' : '');
        headNodes[j].style.color = empty ? '#5b564e' : '#a09a90';
      }

      for (j = 0; j < rowNodes.length; j++) {
        var node = rowNodes[j];
        if (j >= parts.length) { node.style.display = 'none'; continue; }
        node.style.display = '';
        var p = parts[j];
        var moved = committed && barMoved(round.parts, p);
        var recount = committed && countChanged(round.parts, p);
        node.className = 'row' + (p.resting ? ' rest' : '') +
                         (moved ? ' chg' : '') + (recount ? ' more' : '');
        var lab = node.childNodes[0];
        lab.textContent = '';
        var nm = document.createElement('b');
        nm.textContent = p.name + ((p.n || 1) > 1 ? ' ×' + p.n : '');
        lab.appendChild(nm);
        lab.appendChild(document.createTextNode(
          p.resting ? ' · resting' : ' · ' + p.role + ' · ' + pname(p.lo) + '–' + pname(p.hi)
        ));
        var bar = node.childNodes[1].childNodes[0];
        if (p.resting) {
          bar.style.display = 'none';
        } else {
          bar.style.display = '';
          bar.style.left = pct(p.lo) + '%';
          bar.style.width = (pct(p.hi) - pct(p.lo)) + '%';
        }
      }
    }

    function paintOptions() {
      for (var j = 0; j < optNodes.length; j++) {
        optNodes[j].textContent = shown[j].label;
        optNodes[j].setAttribute('aria-pressed', picked === j ? 'true' : 'false');
      }
    }

    function paintRun() {
      if (mastered) {
        run.className = 'run done';
        run.textContent = 'Mastered — carry on';
      } else if (streak === 0) {
        run.className = 'run';
        run.textContent = attempted ? 'Run reset — 3 in a row' : '';
      } else {
        run.className = 'run';
        run.textContent = streak + ' in a row — ' + (3 - streak) + ' to go';
      }
    }

    function newRound() {
      round = ROUNDS[(n + offset) % ROUNDS.length];
      /* rotate by the offset too, so the answer is not always first on
         the opening screen */
      var rot = (n + offset) % round.options.length;
      shown = round.options.slice(rot).concat(round.options.slice(0, rot));
      for (var j = 0; j < shown.length; j++) {
        shown[j].result = applyOpt(round.parts, shown[j]);
        shown[j].right = isFull(shown[j].result);
      }
      current = applyOpt(round.parts, {});
      picked = -1;
      checked = false;
      frameEl.textContent = round.frame;
      paintMap(current, false);
      paintOptions();
      for (var q = 0; q < optNodes.length; q++) { optNodes[q].disabled = false; }
      go.textContent = 'Check';
      go.disabled = true;
      cap.textContent = 'Each bar shows where one part actually sounds, across the four bands of the range.';
      paintRun();
      pushState({ chosen: null, correct: null, misconception: null });
      n++;
    }

    function commit() {
      if (checked) { newRound(); optNodes[0].focus(); return; }
      if (picked < 0) { return; }
      var choice = shown[picked];
      var ok = !!choice.right;
      checked = true;
      attempted++;
      if (ok) { streak++; if (streak >= 3) { mastered = true; } } else { streak = 0; }

      current = choice.result;
      paintMap(current, true);
      for (var q = 0; q < optNodes.length; q++) { optNodes[q].disabled = true; }

      var body = (ok && mastered && streak === 3) ? MASTERY : choice.fb + ' ' + mapNote(current);
      var msg = (ok ? 'Right — ' : 'Not quite — ') + 'you chose ' + choice.short + '. ' + body;
      cap.textContent = msg;
      sr.textContent = msg;
      go.textContent = mastered ? 'Another anyway' : 'Next ensemble';
      go.disabled = false;
      paintRun();
      pushState({ chosen: choice.label, correct: ok, misconception: !!choice.mis });
      go.focus();
    }

    optsEl.addEventListener('click', function (e) {
      var t = e.target;
      while (t && t !== optsEl && !(t.classList && t.classList.contains('opt'))) { t = t.parentNode; }
      if (!t || t === optsEl || t.disabled) { return; }
      picked = parseInt(t.getAttribute('data-i'), 10);
      paintOptions();
      go.disabled = false;
      cap.textContent = 'You have chosen: ' + shown[picked].label + '.';
      sr.textContent = shown[picked].label + ' selected.';
      pushState({ chosen: shown[picked].label, correct: null, misconception: !!shown[picked].mis });
    });

    go.addEventListener('click', commit);

    newRound();
  }

  window.SVWidget = {
    meta: {
      id: ID,
      title: 'Filling the texture',
      teaches: 'A small ensemble sounds full when its parts cover the range from bass to treble and each part does a different job — melody, countermelody, inner harmony, bass line. Adding players who double what is already there adds loudness, not fullness.'
    },
    mount: mount
  };
})();
