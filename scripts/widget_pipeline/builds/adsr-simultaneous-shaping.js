/* StudyVault lesson widget — adsr-simultaneous-shaping
   One note, one envelope. Attack, decay and release are TIMES; sustain is a
   LEVEL held while the key is down. Every envelope drawn here comes from the
   same parametric model {a, d, s, r, hold}, so the pictures and the marking
   cannot drift apart. No audio: characters are described in words. */
(function () {
  'use strict';

  var CLS = 'svw-adsr';
  var STAGE_NAME = { a: 'Attack', d: 'Decay', s: 'Sustain', r: 'Release' };
  var LETTER = ['A', 'B', 'C'];

  /* ---------- the model ---------- */

  function fmt(ms) {
    if (ms < 1000) return Math.round(ms) + ' ms';
    return (ms / 1000).toFixed(2) + ' s';
  }
  function valFmt(key, v) {
    return key === 's' ? v + '%' : fmt(v);
  }
  function describe(p) {
    return 'attack ' + fmt(p.a) + ', decay ' + fmt(p.d) +
           ', sustain ' + p.s + '%, release ' + fmt(p.r);
  }
  function apply(p, change) {
    var q = { a: p.a, d: p.d, s: p.s, r: p.r, hold: p.hold };
    q[change.key] = change.to;
    return q;
  }
  /* level breakpoints, in ms and 0-100 */
  function breakpoints(p, tmax) {
    var tPeak = p.a;
    var tSet = p.a + p.d;
    var hold = Math.max(p.hold, tSet + 30);
    return [[0, 0], [tPeak, 100], [tSet, p.s], [hold, p.s],
            [hold + p.r, 0], [tmax, 0]];
  }

  /* ---------- drawing ---------- */

  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }

  function envSVG(p, o) {
    var W = o.w, H = o.h, tmax = o.tmax, full = o.detail === 'full';
    var padL = full ? 28 : 7, padR = 7, padT = full ? 14 : 9, padB = full ? 18 : 9;
    var x0 = padL, x1 = W - padR, y0 = padT, y1 = H - padB;
    var ink = '#2d2a26', muted = '#5b564e', line = '#ddd7cd';
    function X(t) { return (x0 + (Math.min(t, tmax) / tmax) * (x1 - x0)).toFixed(1); }
    function Y(v) { return (y1 - (v / 100) * (y1 - y0)).toFixed(1); }
    function poly(q, stroke, dash, wid) {
      var pts = breakpoints(q, tmax).map(function (b) { return X(b[0]) + ',' + Y(b[1]); }).join(' ');
      return '<polyline points="' + pts + '" fill="none" stroke="' + stroke +
             '" stroke-width="' + (wid || 2) + '" stroke-linejoin="round" stroke-linecap="round"' +
             (dash ? ' stroke-dasharray="5 3"' : '') + ' vector-effect="non-scaling-stroke"/>';
    }
    function keyBand(q, fill) {
      var hold = Math.max(q.hold, q.a + q.d + 30);
      return '<rect x="' + X(0) + '" y="' + y0 + '" width="' + (X(hold) - X(0)) +
             '" height="' + (y1 - y0) + '" fill="' + fill + '"/>' +
             '<line x1="' + X(hold) + '" y1="' + y0 + '" x2="' + X(hold) + '" y2="' + y1 +
             '" stroke="' + line + '" stroke-width="1" stroke-dasharray="3 3"/>';
    }

    var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' +
            esc(o.alt || 'Envelope shape') + '">';
    s += keyBand(p, o.accent + '20');
    if (o.overlay) s += keyBand(o.overlay, o.accent + '12');
    /* axes */
    s += '<line x1="' + x0 + '" y1="' + y1 + '" x2="' + x1 + '" y2="' + y1 +
         '" stroke="' + line + '" stroke-width="1"/>';
    s += '<line x1="' + x0 + '" y1="' + y0 + '" x2="' + x0 + '" y2="' + y1 +
         '" stroke="' + line + '" stroke-width="1"/>';
    if (full && p.s > 0) {
      var holdF = Math.max(p.hold, p.a + p.d + 30);
      s += '<line x1="' + X(p.a + p.d) + '" y1="' + Y(p.s) + '" x2="' + X(holdF) +
           '" y2="' + Y(p.s) + '" stroke="' + muted + '" stroke-width="1" stroke-dasharray="2 3"/>';
      var lx = (parseFloat(X(p.a + p.d)) + parseFloat(X(holdF))) / 2;
      var ly = p.s > 75 ? parseFloat(Y(p.s)) + 11 : parseFloat(Y(p.s)) - 4;
      s += '<text x="' + lx.toFixed(1) + '" y="' + ly.toFixed(1) + '" text-anchor="middle" font-size="8.5" fill="' +
           muted + '" font-family="Inter, sans-serif">sustain level</text>';
    }
    if (o.overlay) s += poly(o.overlay, o.accent, false, 2.6);
    s += poly(p, ink, false);
    if (full) {
      var mid = ((y0 + y1) / 2).toFixed(1);
      s += '<text x="9" y="' + mid + '" transform="rotate(-90 9 ' + mid +
           ')" text-anchor="middle" font-size="8.5" fill="' + muted +
           '" font-family="Inter, sans-serif">loudness</text>';
      var band = o.overlay || p;
      var bh = Math.max(band.hold, band.a + band.d + 30);
      s += '<text x="' + ((parseFloat(X(0)) + parseFloat(X(bh))) / 2).toFixed(1) + '" y="' + (H - 5) +
           '" text-anchor="middle" font-size="8.5" fill="' + muted +
           '" font-family="Inter, sans-serif">key held down</text>';
      s += '<text x="' + x1 + '" y="' + (H - 5) + '" text-anchor="end" font-size="8.5" fill="' +
           muted + '" font-family="Inter, sans-serif">time</text>';
    }
    return s + '</svg>';
  }

  /* ---------- derived feedback ---------- */

  function sameShort(key, p) {
    if (key === 'a') return 'the same ' + fmt(p.a) + ' attack';
    if (key === 'd') return 'the same ' + fmt(p.d) + ' decay';
    if (key === 's') return 'the same ' + p.s + '% sustain level';
    return 'the same ' + fmt(p.r) + ' release';
  }
  function diffFact(key, b, c) {
    if (key === 'a') return 'the attack, the time from silence to full loudness: ' + fmt(b.a) + ' in one, ' + fmt(c.a) + ' in the other';
    if (key === 'd') return 'the decay, the fall from the peak to the held level: ' + fmt(b.d) + ' in one, ' + fmt(c.d) + ' in the other';
    if (key === 's') return 'the sustain, the LEVEL held while the key is down: ' + b.s + '% in one, ' + c.s + '% in the other';
    return 'the release, the fade after the key lifts: ' + fmt(b.r) + ' in one, ' + fmt(c.r) + ' in the other';
  }
  function joinList(a) {
    if (a.length < 2) return a[0] || '';
    return a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1];
  }
  /* names the single most salient mismatch between two envelopes */
  function diffPhrase(chosen, correct) {
    var d = [
      ['a', Math.abs(chosen.a - correct.a) / 500],
      ['d', Math.abs(chosen.d - correct.d) / 500],
      ['s', Math.abs(chosen.s - correct.s) / 100],
      ['r', Math.abs(chosen.r - correct.r) / 800]
    ].sort(function (x, y) { return y[1] - x[1]; });
    var k = d[0][0];
    if (k === 'a') {
      return chosen.a > correct.a
        ? 'That one swells in over ' + fmt(chosen.a) + '; this sound is at full loudness in ' + fmt(correct.a) + '.'
        : 'That one is at full loudness in ' + fmt(chosen.a) + '; this sound swells in over ' + fmt(correct.a) + '.';
    }
    if (k === 's') {
      if (correct.s === 0) return 'That one holds at ' + chosen.s + '% for as long as the key is down; this sound holds nothing at all.';
      return chosen.s > correct.s
        ? 'That one holds at ' + chosen.s + '% while the key is down; this sound settles at ' + correct.s + '%.'
        : 'That one settles at ' + chosen.s + '%; this sound holds at ' + correct.s + '% while the key is down.';
    }
    if (k === 'd') {
      return chosen.d > correct.d
        ? 'That one takes ' + fmt(chosen.d) + ' to fall from the peak; this sound drops in ' + fmt(correct.d) + '.'
        : 'That one drops from the peak in ' + fmt(chosen.d) + '; this sound takes ' + fmt(correct.d) + '.';
    }
    return chosen.r > correct.r
      ? 'That one rings on for ' + fmt(chosen.r) + ' after the key lifts; this sound stops in ' + fmt(correct.r) + '.'
      : 'That one stops ' + fmt(chosen.r) + ' after the key lifts; this sound rings on for ' + fmt(correct.r) + '.';
  }
  function charLine(p) {
    if (p.s === 0) return 'Sustain is 0, so it has faded to nothing while the key is still down.';
    if (p.s >= 95) return 'Sustain is 100%, so it holds full loudness for as long as the key is down.';
    if (p.a >= 400) return 'The long attack is what makes it swell in rather than start.';
    return 'The four values together give it its character.';
  }

  /* ---------- the bank ---------- */

  var PLUCK = { a: 5, d: 340, s: 0, r: 200 };
  var PAD = { a: 820, d: 380, s: 70, r: 900 };
  var ORGAN = { a: 12, d: 0, s: 100, r: 40 };
  var BRASS = { a: 110, d: 170, s: 85, r: 240 };
  var MARIMBA = { a: 3, d: 480, s: 0, r: 90 };

  var ROUNDS = [
    {
      id: 'pick-pluck', kind: 'pick', tmax: 2800, hold: 1700,
      prompt: 'A plucked string: loudest the instant it is touched, gone quickly, holding nothing while the key stays down. Same pitch in all three — which envelope is it?',
      opts: [PLUCK, PAD, ORGAN], answer: 0
    },
    {
      id: 'hold-longer', kind: 'single', tmax: 2900,
      base: { a: 60, d: 380, s: 45, r: 300, hold: 1000 },
      change: { key: 'hold', to: 2200 },
      scene: 'The same patch is played twice.',
      opts: [
        { t: 'The held level is the same — the flat part just lasts longer.', ok: true },
        { t: 'The sustain setting has effectively been turned up.' },
        { t: 'The note grows louder the longer it is held.' }
      ],
      why: function (r, i) {
        var b = r.base;
        if (i === 0) return 'Right — you said the held level is the same. Sustain is a LEVEL, not a length: the note sits at ' + b.s + '% for as long as the key is down, and the three times are untouched.';
        if (i === 1) return 'Not quite — you said the sustain setting has been turned up. Nothing on the synth changed: sustain is the level it settles at, still ' + b.s + '%. Key-down time is the player’s choice, not a control.';
        return 'Not quite — you said it grows louder as it is held. After the ' + fmt(b.d) + ' decay the envelope is flat at ' + b.s + '% until the key lifts, then the release fades it out.';
      }
    },
    {
      id: 'which-release', kind: 'pair', tmax: 2800,
      base: { a: 60, d: 300, s: 60, r: 150, hold: 1300 },
      change: { key: 'r', to: 1100 }
    },
    {
      id: 'attack-to-instant', kind: 'single', tmax: 3000,
      base: { a: 700, d: 300, s: 70, r: 800, hold: 1500 },
      change: { key: 'a', to: 5 },
      scene: 'This envelope swells in slowly.',
      opts: [
        { t: 'It now starts at full loudness instead of swelling in.', ok: true },
        { t: 'It is now louder overall than before.' },
        { t: 'It now rings on for longer after the key lifts.' }
      ],
      why: function (r, i) {
        var b = r.base;
        if (i === 0) return 'Right — you said it starts at full loudness. Attack is a TIME: ' + fmt(b.a) + ' of swelling becomes ' + fmt(r.change.to) + '. The peak it reaches is unchanged.';
        if (i === 1) return 'Not quite — you said it is louder overall. Attack sets how LONG the rise takes, not how high: both reach the same peak, one in ' + fmt(r.change.to) + ' not ' + fmt(b.a) + '.';
        return 'Not quite — you said it rings on for longer. The fade after the key lifts is release, still ' + fmt(b.r) + '. Attack only changes the start.';
      }
    },
    {
      id: 'which-sustain', kind: 'pair', tmax: 2200,
      base: { a: 40, d: 300, s: 80, r: 250, hold: 1400 },
      change: { key: 's', to: 20 }
    },
    {
      id: 'pick-organ', kind: 'pick', tmax: 2800, hold: 1700,
      prompt: 'An organ: full loudness the instant the key goes down, exactly as loud however long it is held, and stopping almost as the key lifts. Which envelope is it?',
      opts: [BRASS, ORGAN, PLUCK], answer: 1
    },
    {
      id: 'sustain-to-zero', kind: 'single', tmax: 2200,
      base: { a: 20, d: 400, s: 60, r: 250, hold: 1400 },
      change: { key: 's', to: 0 },
      scene: 'This envelope settles and holds while the key is down.',
      opts: [
        { t: 'It fades to silence while the key is still down.', ok: true },
        { t: 'It stops the moment the key is released.' },
        { t: 'It lasts as long as before, but quieter all through.' }
      ],
      why: function (r, i) {
        var b = r.base;
        if (i === 0) return 'Right — you said it fades to silence with the key still down. With sustain at 0 the decay has nowhere to stop: peak to nothing in ' + fmt(b.d) + ', well before the key lifts.';
        if (i === 1) return 'Not quite — you said it stops when the key is released. It has already gone: the ' + fmt(b.d) + ' decay now runs to nothing, and the key holds until ' + fmt(b.hold) + '.';
        return 'Not quite — you said it lasts as long but quieter throughout. Sustain is not a volume control: the attack still reaches the same peak, and only the level after the decay drops.';
      }
    },
    {
      id: 'hold-pluck', kind: 'single', tmax: 2600,
      base: { a: PLUCK.a, d: PLUCK.d, s: PLUCK.s, r: PLUCK.r, hold: 900 },
      change: { key: 'hold', to: 2000 },
      scene: 'The same plucked patch is played twice.',
      opts: [
        { t: 'Almost no difference — it has already faded to silence.', ok: true },
        { t: 'The note lasts about twice as long.' },
        { t: 'It is held at a steady level for twice as long.' }
      ],
      why: function (r, i) {
        var b = r.base;
        if (i === 0) return 'Right — you said almost no difference. Sustain is 0%, so it is gone ' + fmt(b.a + b.d) + ' in. What keeps a note going is the sustain level, not the finger.';
        if (i === 1) return 'Not quite — you said it lasts about twice as long. With sustain at 0% the sound has already died ' + fmt(b.a + b.d) + ' in, so holding the key changes nothing you can hear.';
        return 'Not quite — you said it is held at a steady level. There is no level to hold: sustain is 0%, so the ' + fmt(b.d) + ' decay carries it to silence.';
      }
    },
    {
      id: 'pick-pad', kind: 'pick', tmax: 2800, hold: 1700,
      prompt: 'A string pad: it swells in over most of a second, holds well below its peak while the key is down, then fades slowly away. Which envelope is it?',
      opts: [MARIMBA, BRASS, PAD], answer: 2
    }
  ];

  /* ---------- mount ---------- */

  function mount(root, ctx) {
    ctx = ctx || {};
    var accent = String(ctx.accent || '').trim();
    if (!/^#[0-9a-f]{6}$/i.test(accent)) {
      accent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim();
    }
    if (!/^#[0-9a-f]{6}$/i.test(accent)) accent = '#8a6f4e';
    var reduced = !!ctx.reducedMotion;

    root.classList.add(CLS);

    var css = document.createElement('style');
    css.textContent = [
      '.' + CLS + '{background:#fff;border:1px solid #e8e3db;border-radius:16px;padding:1rem 1.15rem 1.05rem;',
      'font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.45;}',
      '.' + CLS + ' *{box-sizing:border-box;}',
      '.' + CLS + ' .k{margin:0;font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:' + accent + ';}',
      '.' + CLS + ' .t{margin:.12rem 0 .3rem;font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.2rem;line-height:1.2;}',
      '.' + CLS + ' .frame{margin:0;font-size:.78rem;line-height:1.45;color:#5b564e;}',
      '.' + CLS + ' .prompt{margin:.5rem 0 .45rem;font-size:.86rem;line-height:1.45;}',
      '.' + CLS + ' .stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.4rem .45rem .3rem;}',
      '.' + CLS + ' .one{max-width:352px;margin:0 auto;}',
      '.' + CLS + ' .pair{max-width:420px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:.5rem;}',
      '.' + CLS + ' .fig span{display:block;text-align:center;font-size:.72rem;color:#5b564e;font-weight:600;}',
      '.' + CLS + ' svg{width:100%;height:auto;display:block;}',
      '.' + CLS + ' .legend{margin:.1rem 0 .1rem;text-align:center;font-size:.72rem;color:#5b564e;}',
      '.' + CLS + ' .legend i{display:inline-block;width:14px;height:2px;vertical-align:middle;margin:0 .25rem;}',
      '.' + CLS + ' .pickrow{max-width:480px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr 1fr;gap:.4rem;}',
      '.' + CLS + ' .pick{padding:.25rem .25rem .3rem;background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;cursor:pointer;font-family:inherit;}',
      '.' + CLS + ' .pick b{display:block;font-size:.78rem;font-weight:700;color:#5b564e;}',
      '.' + CLS + ' .pick[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;}',
      '.' + CLS + ' .pick[aria-pressed="true"] b{color:#fff;}',
      '.' + CLS + ' .opts{margin-top:.45rem;display:grid;gap:.35rem;}',
      '.' + CLS + ' .opts.grid2{grid-template-columns:1fr 1fr;}',
      '.' + CLS + ' .opt{text-align:left;font-family:inherit;font-size:.82rem;font-weight:600;line-height:1.35;',
      'padding:.38rem .6rem;border:1px solid #ddd7cd;border-radius:10px;background:#faf8f5;color:#2d2a26;cursor:pointer;}',
      '.' + CLS + ' .opts.grid2 .opt{text-align:center;}',
      '.' + CLS + ' .opt.right,.' + CLS + ' .pick.right{border-color:' + accent + ';background:' + accent + '1f;}',
      '.' + CLS + ' .opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff;}',
      '.' + CLS + ' .act{margin-top:.45rem;display:flex;align-items:center;justify-content:space-between;gap:.6rem;}',
      '.' + CLS + ' .run{font-size:.75rem;color:#5b564e;font-variant-numeric:tabular-nums;}',
      '.' + CLS + ' .go{font-family:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;border-radius:10px;',
      'border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer;flex:none;}',
      '.' + CLS + ' .go[disabled]{opacity:.4;cursor:default;}',
      '.' + CLS + ' .cap{margin:.55rem 0 0;font-size:.84rem;line-height:1.5;min-height:2.6em;}',
      '.' + CLS + ' .cap b{color:' + accent + ';}',
      '.' + CLS + ' .cap.done b{color:#4f7d63;}',
      '.' + CLS + ' .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;}',
      reduced ? '' : '.' + CLS + ' .opt,.' + CLS + ' .pick,.' + CLS + ' .go{transition:background-color .12s ease,color .12s ease,border-color .12s ease;}',
      '.' + CLS + ' :focus-visible{outline:2px solid ' + accent + ';outline-offset:2px;}'
    ].join('');
    root.appendChild(css);

    function el(tag, cls, txt) {
      var n = document.createElement(tag);
      if (cls) n.className = cls;
      if (txt != null) n.textContent = txt;
      return n;
    }

    root.appendChild(el('p', 'k', 'Sound creation'));
    root.appendChild(el('h3', 't', 'The shape of one note'));
    root.appendChild(el('p', 'frame',
      'A synth shapes every note it plays with one envelope, set by four controls: attack, decay, sustain and release.'));

    var promptEl = el('p', 'prompt', '');
    root.appendChild(promptEl);

    /* pick row (three candidate envelopes) */
    var pickRow = el('div', 'pickrow');
    var pickBtns = [];
    for (var i = 0; i < 3; i++) {
      var b = el('button', 'pick');
      b.type = 'button';
      b.setAttribute('aria-pressed', 'false');
      var holder = el('span', 'mini');
      var lab = el('b', null, LETTER[i]);
      b.appendChild(holder);
      b.appendChild(lab);
      b.dataset.i = String(i);
      pickRow.appendChild(b);
      pickBtns.push({ btn: b, holder: holder });
    }
    root.appendChild(pickRow);
    var pickNote = el('p', 'legend', 'Shaded band = the key held down.');
    root.appendChild(pickNote);

    /* stage */
    var stage = el('div', 'stage');
    var pairWrap = el('div', 'pair');
    var figs = [];
    for (var j = 0; j < 2; j++) {
      var f = el('div', 'fig');
      var h = el('div');
      var cap = el('span', null, 'Envelope ' + (j + 1));
      f.appendChild(h);
      f.appendChild(cap);
      pairWrap.appendChild(f);
      figs.push(h);
    }
    var oneWrap = el('div', 'one');
    var oneHolder = el('div');
    var legend = el('p', 'legend');
    oneWrap.appendChild(oneHolder);
    oneWrap.appendChild(legend);
    stage.appendChild(pairWrap);
    stage.appendChild(oneWrap);
    root.appendChild(stage);

    /* text options */
    var opts = el('div', 'opts');
    var optBtns = [];
    for (var m = 0; m < 4; m++) {
      var ob = el('button', 'opt');
      ob.type = 'button';
      ob.setAttribute('aria-pressed', 'false');
      ob.dataset.i = String(m);
      opts.appendChild(ob);
      optBtns.push(ob);
    }
    root.appendChild(opts);

    var act = el('div', 'act');
    var run = el('span', 'run', '');
    var go = el('button', 'go', 'Check');
    go.type = 'button';
    go.disabled = true;
    act.appendChild(run);
    act.appendChild(go);
    root.appendChild(act);

    var capEl = el('p', 'cap', '');
    root.appendChild(capEl);
    var sr = el('p', 'sr');
    sr.setAttribute('aria-live', 'polite');
    root.appendChild(sr);

    /* ---------- state ---------- */
    var idx = 0, sel = -1, committed = false;
    var streak = 0, attempted = 0, mastered = false, lastCorrect = null;

    function pushState(picked, correct) {
      root.dataset.svState = JSON.stringify({
        round: ROUNDS[idx].id,
        selected: sel < 0 ? null : sel,
        picked: picked === undefined ? null : picked,
        correct: correct === undefined ? null : correct,
        streak: streak,
        mastered: mastered,
        attempted: attempted
      });
    }
    pushState();

    function show(node, on) { node.style.display = on ? '' : 'none'; }

    function drawStage(reveal) {
      var r = ROUNDS[idx];
      if (r.kind === 'pick') return;
      if (r.kind === 'pair') {
        var changed = apply(r.base, r.change);
        figs[0].innerHTML = envSVG(r.base, { w: 200, h: 120, tmax: r.tmax, detail: 'compact', accent: accent, alt: 'Envelope 1' });
        figs[1].innerHTML = envSVG(changed, { w: 200, h: 120, tmax: r.tmax, detail: 'compact', accent: accent, alt: 'Envelope 2' });
        return;
      }
      var after = reveal ? apply(r.base, r.change) : null;
      oneHolder.innerHTML = envSVG(r.base, {
        w: 320, h: 116, tmax: r.tmax, detail: 'full', accent: accent,
        overlay: after, alt: 'Envelope: ' + describe(r.base)
      });
      if (after) {
        legend.innerHTML = '<i style="background:#2d2a26"></i>before' +
          '<i style="background:' + accent + ';margin-left:.8rem"></i>after';
      } else {
        legend.textContent = '';
      }
    }

    function loadRound() {
      var r = ROUNDS[idx];
      sel = -1;
      committed = false;
      capEl.textContent = '';
      capEl.classList.remove('done');
      go.textContent = mastered ? 'Another anyway' : 'Check';
      go.disabled = true;

      show(pickRow, r.kind === 'pick');
      show(pickNote, r.kind === 'pick');
      optBtns.forEach(function (n) { n.classList.remove('right'); });
      pickBtns.forEach(function (n) { n.btn.classList.remove('right'); });
      show(stage, r.kind !== 'pick');
      show(pairWrap, r.kind === 'pair');
      show(oneWrap, r.kind === 'single');
      show(opts, r.kind !== 'pick');
      opts.classList.toggle('grid2', r.kind === 'pair');

      if (r.kind === 'pick') {
        promptEl.textContent = r.prompt;
        for (var i = 0; i < 3; i++) {
          var p = r.opts[i];
          var q = { a: p.a, d: p.d, s: p.s, r: p.r, hold: r.hold };
          pickBtns[i].holder.innerHTML = envSVG(q, {
            w: 120, h: 78, tmax: r.tmax, detail: 'mini', accent: accent,
            alt: 'Envelope ' + LETTER[i]
          });
          pickBtns[i].btn.setAttribute('aria-pressed', 'false');
          pickBtns[i].btn.setAttribute('aria-label', 'Envelope ' + LETTER[i]);
        }
      } else if (r.kind === 'pair') {
        promptEl.textContent = 'These two envelopes shape the same note at the same pitch. Exactly one of the four controls has been changed. Which one?';
        var keys = ['a', 'd', 's', 'r'];
        for (var k = 0; k < 4; k++) {
          optBtns[k].textContent = STAGE_NAME[keys[k]];
          optBtns[k].dataset.key = keys[k];
          optBtns[k].setAttribute('aria-pressed', 'false');
          show(optBtns[k], true);
        }
      } else {
        var ch = r.change;
        promptEl.textContent = ch.key === 'hold'
          ? r.scene + ' It is held for ' + fmt(ch.to) + ' instead of ' + fmt(r.base.hold) + '. Nothing on the synth is changed — what does the note do?'
          : r.scene + ' The ' + STAGE_NAME[ch.key].toLowerCase() + ' control is changed from ' +
            valFmt(ch.key, r.base[ch.key]) + ' to ' + valFmt(ch.key, ch.to) + '. Nothing else is touched — what does the note now do?';
        for (var n = 0; n < 4; n++) {
          if (n < r.opts.length) {
            optBtns[n].textContent = r.opts[n].t;
            optBtns[n].setAttribute('aria-pressed', 'false');
            show(optBtns[n], true);
          } else {
            show(optBtns[n], false);
          }
        }
      }
      drawStage(false);
      pushState();
    }

    function activeList() {
      var r = ROUNDS[idx];
      if (r.kind === 'pick') return pickBtns.map(function (x) { return x.btn; });
      if (r.kind === 'pair') return optBtns;
      return optBtns.slice(0, r.opts.length);
    }

    function selectIdx(i, group) {
      var r = ROUNDS[idx];
      var list = activeList();
      var wanted = r.kind === 'pick' ? 'pick' : 'opt';
      if (committed || group !== wanted) return;
      if (!(i >= 0 && i < list.length)) return;
      sel = i;
      for (var n = 0; n < optBtns.length; n++) optBtns[n].setAttribute('aria-pressed', 'false');
      for (var m = 0; m < pickBtns.length; m++) pickBtns[m].btn.setAttribute('aria-pressed', 'false');
      list[i].setAttribute('aria-pressed', 'true');
      go.disabled = false;
      capEl.textContent = r.kind === 'pick'
        ? 'Envelope ' + LETTER[i] + ' is chosen.'
        : '“' + optBtns[i].textContent + '” is chosen.';
      sr.textContent = capEl.textContent;
      pushState();
    }

    function commit() {
      var r = ROUNDS[idx], ok, msg, picked;

      if (r.kind === 'pick') {
        var correctP = r.opts[r.answer];
        var chosenP = r.opts[sel];
        ok = sel === r.answer;
        picked = 'Envelope ' + LETTER[sel];
        var cQ = { a: correctP.a, d: correctP.d, s: correctP.s, r: correctP.r, hold: r.hold };
        if (ok) {
          msg = 'Right — envelope ' + LETTER[sel] + ': ' + describe(correctP) + '. ' + charLine(correctP);
        } else {
          msg = 'Not quite — you chose envelope ' + LETTER[sel] + '. ' + diffPhrase(chosenP, correctP) +
                ' It is envelope ' + LETTER[r.answer] + ': ' + describe(correctP) + '.';
        }
        void cQ;
      } else if (r.kind === 'pair') {
        var changed = apply(r.base, r.change);
        var key = optBtns[sel].dataset.key;
        ok = key === r.change.key;
        picked = STAGE_NAME[key];
        var others = ['a', 'd', 's', 'r'].filter(function (x) { return x !== r.change.key; });
        var sames = others.map(function (x) { return sameShort(x, r.base); });
        if (ok) {
          msg = 'Right — you said ' + picked + '. Both have ' + joinList(sames) + '. What differs is ' +
                diffFact(r.change.key, r.base, changed) + '.';
        } else {
          msg = 'Not quite — you said ' + picked + ', but both have ' + sameShort(key, r.base) +
                '. What differs is ' + diffFact(r.change.key, r.base, changed) + '.';
        }
      } else {
        ok = !!r.opts[sel].ok;
        picked = r.opts[sel].t;
        msg = r.why(r, sel);
      }

      committed = true;
      attempted += 1;
      if (r.kind === 'pick') {
        pickBtns[r.answer].btn.classList.add('right');
      } else if (r.kind === 'pair') {
        optBtns[['a', 'd', 's', 'r'].indexOf(r.change.key)].classList.add('right');
      } else {
        for (var w = 0; w < r.opts.length; w++) {
          if (r.opts[w].ok) optBtns[w].classList.add('right');
        }
      }
      if (ok) { streak += 1; } else { streak = 0; }
      lastCorrect = ok;
      if (ok && streak >= 3 && !mastered) mastered = true;

      if (ok && streak >= 3) {
        msg += ' Three in a row — you have it: attack, decay and release are times; sustain is a level.';
        capEl.classList.add('done');
      } else {
        capEl.classList.remove('done');
      }
      capEl.textContent = msg;
      run.textContent = ok
        ? (streak >= 3 ? 'Three in a row.' : streak + ' right in a row — ' + (3 - streak) + ' more.')
        : 'Run reset — three in a row finishes it.';
      sr.textContent = msg;

      drawStage(true);
      go.textContent = mastered ? 'Another anyway' : 'Next';
      go.disabled = false;
      pushState(picked, ok);
    }

    pickRow.addEventListener('click', function (e) {
      var b = e.target.closest ? e.target.closest('.pick') : null;
      if (b) selectIdx(parseInt(b.dataset.i, 10), 'pick');
    });
    opts.addEventListener('click', function (e) {
      var b = e.target.closest ? e.target.closest('.opt') : null;
      if (b) selectIdx(parseInt(b.dataset.i, 10), 'opt');
    });
    go.addEventListener('click', function () {
      if (committed) {
        idx = (idx + 1) % ROUNDS.length;
        loadRound();
      } else if (sel >= 0) {
        commit();
      }
    });
    root.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !committed && sel >= 0) {
        sel = -1;
        optBtns.forEach(function (n) { n.setAttribute('aria-pressed', 'false'); });
        pickBtns.forEach(function (n) { n.btn.setAttribute('aria-pressed', 'false'); });
        go.disabled = true;
        capEl.textContent = '';
        pushState();
      }
    });

    void lastCorrect;
    loadRound();
  }

  window.SVWidget = {
    meta: {
      id: 'adsr-simultaneous-shaping',
      title: 'ADSR — the shape of one note',
      teaches: 'Attack, decay and release are times; sustain is the level held while the key is down. The four act together on one note.'
    },
    mount: mount
  };
})();
