/* Sonata form: follow the keys.
   Self-contained lesson widget. No network, no audio, no storage. */
(function () {
  'use strict';

  var ID = 'sonata-form-key-relationships';

  /* ---------------- key arithmetic model ---------------- */
  /* Every answer below is computed from semitone arithmetic on the home key.
     Nothing is hand-authored. Dominant = +7. Relative major = +3 from minor.
     Subdominant = +5. Relative minor = +9. Submediant (from minor) = +8. */

  var SHARP = ['C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B'];
  var FLAT = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B'];

  /* Home keys chosen so every derived key spells cleanly, no double accidentals. */
  var HOMES = [
    { pc: 0, mode: 'major', spell: 'sharp' },   /* C major  */
    { pc: 9, mode: 'minor', spell: 'sharp' },   /* A minor  */
    { pc: 7, mode: 'major', spell: 'sharp' },   /* G major  */
    { pc: 2, mode: 'minor', spell: 'flat' },    /* D minor  */
    { pc: 2, mode: 'major', spell: 'sharp' },   /* D major  */
    { pc: 7, mode: 'minor', spell: 'flat' },    /* G minor  */
    { pc: 5, mode: 'major', spell: 'flat' },    /* F major  */
    { pc: 4, mode: 'minor', spell: 'sharp' },   /* E minor  */
    { pc: 10, mode: 'major', spell: 'flat' },   /* B flat major */
    { pc: 11, mode: 'minor', spell: 'sharp' },  /* B minor  */
    { pc: 9, mode: 'major', spell: 'sharp' },   /* A major  */
    { pc: 0, mode: 'minor', spell: 'flat' },    /* C minor  */
    { pc: 3, mode: 'major', spell: 'flat' },    /* E flat major */
    { pc: 6, mode: 'minor', spell: 'sharp' }    /* F sharp minor */
  ];

  function keyName(pc, mode, home) {
    var t = (home.spell === 'flat') ? FLAT : SHARP;
    return t[((pc % 12) + 12) % 12] + (mode === 'major' ? ' major' : ' minor');
  }
  function tonic(h) { return keyName(h.pc, h.mode, h); }
  function dominant(h) { return keyName(h.pc + 7, 'major', h); }
  function dominantMinor(h) { return keyName(h.pc + 7, 'minor', h); }
  function relativeMajor(h) { return keyName(h.pc + 3, 'major', h); }
  function relativeMinor(h) { return keyName(h.pc + 9, 'minor', h); }
  function subdominant(h) { return keyName(h.pc + 5, h.mode, h); }
  function submediant(h) { return keyName(h.pc + 8, 'major', h); }

  /* The key the second subject arrives in during the exposition. */
  function expoAway(h) { return h.mode === 'major' ? dominant(h) : relativeMajor(h); }
  function awayWord(h) { return h.mode === 'major' ? 'the dominant' : 'the relative major'; }

  /* ---------------- rounds ---------------- */

  function roundExposition(h) {
    var right = expoAway(h);
    return {
      type: 'exposition',
      frame: 'A classical movement in ' + tonic(h) + '. The first subject is stated in the tonic, then the second subject enters. Predict the key the second subject arrives in.',
      options: [right, tonic(h), subdominant(h), h.mode === 'major' ? relativeMinor(h) : submediant(h)],
      answer: right,
      bands: [{ label: 'Exposition', span: '1 / 3' }],
      stations: [
        { chip: tonic(h), tone: 'tonic', role: 'Subject 1' },
        { chip: '?', tone: 'ask', role: 'Subject 2' }
      ],
      resolve: { index: 1, chip: right, tone: 'away' }
    };
  }

  function roundRecap(h) {
    var away = expoAway(h);
    return {
      type: 'recapitulation',
      frame: 'The same movement, now at the recapitulation. The exposition had taken the second subject to ' + away + '. Predict the key the second subject returns in.',
      options: [tonic(h), away, subdominant(h), h.mode === 'major' ? relativeMinor(h) : dominantMinor(h)],
      answer: tonic(h),
      bands: [
        { label: 'Exposition', span: '1 / 3' },
        { label: 'Development', span: '3 / 4' },
        { label: 'Recapitulation', span: '4 / 6' }
      ],
      stations: [
        { chip: tonic(h), tone: 'tonic', role: 'Subject 1' },
        { chip: away, tone: 'away', role: 'Subject 2' },
        { chip: 'many keys', tone: 'unstable', role: 'unsettled' },
        { chip: tonic(h), tone: 'tonic', role: 'Subject 1' },
        { chip: '?', tone: 'ask', role: 'Subject 2' }
      ],
      resolve: { index: 4, chip: tonic(h), tone: 'tonic' }
    };
  }

  function roundSection(h, variant) {
    var r = {
      type: 'section',
      frame: 'One section of a sonata-form movement in ' + tonic(h) + '. These are the keys it passes through, in order. Name the section.',
      options: ['Exposition', 'Development', 'Recapitulation'],
      bands: [{ label: '?', span: '1 / -1' }]
    };
    if (variant === 0) {
      r.answer = 'Exposition';
      r.stations = [
        { chip: tonic(h), tone: 'tonic', role: 'opens here' },
        { chip: expoAway(h), tone: 'away', role: 'cadence confirms it' }
      ];
    } else if (variant === 1) {
      r.answer = 'Development';
      r.stations = [
        { chip: expoAway(h), tone: 'unstable', role: 'passes through' },
        { chip: subdominant(h), tone: 'unstable', role: 'then' },
        { chip: h.mode === 'major' ? relativeMinor(h) : dominantMinor(h), tone: 'unstable', role: 'then, no cadence' }
      ];
    } else {
      r.answer = 'Recapitulation';
      r.stations = [
        { chip: tonic(h), tone: 'tonic', role: 'Subject 1' },
        { chip: tonic(h), tone: 'tonic', role: 'Subject 2' }
      ];
    }
    r.resolveBand = r.answer;
    return r;
  }

  function buildRound(n, offset) {
    var h = HOMES[(n + offset) % HOMES.length];
    var t = n % 3;
    if (t === 0) return roundExposition(h);
    if (t === 1) return roundRecap(h);
    return roundSection(h, Math.floor(n / 3) % 3);
  }

  /* ---------------- feedback ---------------- */

  function feedback(r, h, chosen, ok) {
    var head = ok ? 'Right — you said ' + chosen + '. ' : 'Not quite — you said ' + chosen + '. ';
    if (r.type === 'exposition') {
      if (ok) {
        return head + 'The second subject leaves home for ' + awayWord(h) + ', and a cadence confirms the new key. That modulation is what makes this sonata form rather than a tune stated twice: the exposition deliberately ends in the wrong key, and the argument has to be settled later.';
      }
      if (chosen === tonic(h)) {
        return head + 'That is the tonic — the key it started in. The second subject moves to ' + r.answer + ', ' + awayWord(h) + '. If both subjects stayed at home there would be no tonal tension to resolve, and the movement would be a theme repeated, not sonata form.';
      }
      return head + 'The second subject arrives in ' + r.answer + ', ' + awayWord(h) + ' of ' + tonic(h) + '. Other related keys get visited later, in the development — but the exposition makes one firm move away and confirms it with a cadence.';
    }
    if (r.type === 'recapitulation') {
      if (ok) {
        return head + 'The second subject comes home. The recapitulation transposes it into the tonic, so the key the exposition ran away to is finally resolved.';
      }
      if (chosen === expoAway(h)) {
        return 'Not quite — you said ' + chosen + ', the key it had in the exposition. That is the "just a repeat" trap: it returns in ' + r.answer + ', the tonic. Transposing the second subject home is the whole reason the form exists.';
      }
      return head + 'The recapitulation resolves rather than travels: both subjects are heard in ' + r.answer + ', the tonic. Wandering to other keys belongs to the development, which has already finished by this point.';
    }
    if (ok) {
      if (r.answer === 'Exposition') return head + 'Two settled keys, tonic then ' + awayWord(h) + ', each confirmed by a cadence — that is the exposition stating its argument.';
      if (r.answer === 'Development') return head + 'Several related keys in quick succession with no cadence to settle any of them is the signature of the development: it destabilises the material before the tonic is restored.';
      return head + 'Both subjects in ' + tonic(h) + ', with no move away, only happens in the recapitulation — the second subject has been transposed home.';
    }
    var why = {
      Exposition: 'the exposition states two subjects in two settled keys, tonic then ' + awayWord(h) + ', each confirmed by a cadence',
      Development: 'the development slips through several keys quickly and confirms none of them',
      Recapitulation: 'the recapitulation keeps both subjects in the tonic, with no move away'
    };
    return head + 'But ' + why[chosen] + '. Here, ' + why[r.answer] + ' — so this is the ' + r.answer.toLowerCase() + '.';
  }

  function shortVerdict(r, h, chosen) {
    if (r.type === 'exposition') return 'Right — you said ' + chosen + ', ' + awayWord(h) + '.';
    if (r.type === 'recapitulation') return 'Right — you said ' + chosen + ' — home again.';
    return 'Right — you said ' + chosen + '.';
  }

  var MASTERY = 'Three in a row — you have it. Sonata form is a drama of keys: the second subject leaves the tonic, the development settles nowhere, and the recapitulation brings it home.';

  /* ---------------- mount ---------------- */

  function mount(root, ctx) {
    ctx = ctx || {};
    var cs = window.getComputedStyle(root);
    var accent = (cs.getPropertyValue('--accent') || '').trim() || ctx.accent || '#7b5e46';
    var still = !!ctx.reducedMotion;

    root.className = (root.className ? root.className + ' ' : '') + 'svw-sonata';

    var css = [
      '.svw-sonata{position:relative;background:#fff;border:1px solid #e8e3db;border-radius:16px;padding:1.15rem;',
      'font-family:Inter,system-ui,-apple-system,sans-serif;color:#2d2a26;-webkit-text-size-adjust:100%;}',
      '.svw-sonata *{box-sizing:border-box;}',
      '.svw-sonata .kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:' + accent + ';margin:0 0 .2rem;}',
      '.svw-sonata h3{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.22rem;line-height:1.2;margin:0 0 .35rem;}',
      '.svw-sonata .frame{font-size:.86rem;line-height:1.45;margin:0 0 .7rem;color:#3a352e;}',
      '.svw-sonata .stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.55rem .5rem .5rem;margin:0 0 .6rem;}',
      '.svw-sonata .bands,.svw-sonata .sts{display:grid;gap:.3rem;}',
      '.svw-sonata .bands{margin-bottom:.45rem;}',
      '.svw-sonata .band{font-size:.68rem;font-weight:600;letter-spacing:.02em;text-align:center;color:#5b564e;',
      'background:#f2ece3;border-radius:7px;padding:.2rem .1rem;}',
      '.svw-sonata .band.on{background:' + accent + '22;color:#2d2a26;}',
      '.svw-sonata .sts{position:relative;}',
      '.svw-sonata .sts:before{content:"";position:absolute;left:12%;right:12%;top:5px;height:2px;background:#e0d9cd;}',
      '.svw-sonata .st{position:relative;text-align:center;min-width:0;}',
      '.svw-sonata .dot{display:block;width:10px;height:10px;border-radius:50%;margin:0 auto .3rem;background:#faf8f5;border:2px solid #cdc5b8;}',
      '.svw-sonata .st.tonic .dot{background:' + accent + ';border-color:' + accent + ';}',
      '.svw-sonata .st.ask .dot{border-color:#2d2a26;}',
      '.svw-sonata .chip{font-size:.74rem;font-weight:600;font-variant-numeric:tabular-nums;line-height:1.25;',
      'padding:.22rem .12rem;border-radius:8px;border:1px solid #ddd7cd;background:#fff;color:#2d2a26;}',
      '.svw-sonata .st.tonic .chip{background:' + accent + '1f;border-color:' + accent + ';}',
      '.svw-sonata .st.away .chip{border-style:dashed;color:#5b564e;}',
      '.svw-sonata .st.unstable .chip{border-style:dashed;color:#8d8880;background:#f6f2ec;}',
      '.svw-sonata .st.ask .chip{border:1.5px solid #2d2a26;font-size:.9rem;}',
      '.svw-sonata .role{font-size:.66rem;line-height:1.25;color:#8d8880;margin-top:.22rem;}',
      '.svw-sonata .home{font-size:.66rem;color:#8d8880;text-align:center;margin:.35rem 0 0;}',
      '.svw-sonata .home b{color:#2d2a26;font-weight:600;}',
      '.svw-sonata .opts{display:grid;grid-template-columns:1fr 1fr;gap:.4rem;margin:0 0 .55rem;}',
      '.svw-sonata .opt{font:600 .82rem Inter,system-ui,sans-serif;color:#2d2a26;padding:.5rem .4rem;border-radius:10px;',
      'border:1px solid #ddd7cd;background:#faf8f5;cursor:pointer;text-align:center;width:100%;}',
      '.svw-sonata .opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff;}',
      '.svw-sonata .opt[disabled]{cursor:default;opacity:.9;}',
      '.svw-sonata .bar{display:flex;align-items:center;gap:.6rem;flex-wrap:wrap;margin:0 0 .55rem;}',
      '.svw-sonata .go{font:600 .82rem Inter,system-ui,sans-serif;color:#fff;background:#2d2a26;border:1px solid #2d2a26;',
      'padding:.5rem .95rem;border-radius:10px;cursor:pointer;}',
      '.svw-sonata .run{font-size:.74rem;color:#8d8880;}',
      '.svw-sonata .run.done{color:#4f7d63;font-weight:600;}',
      '.svw-sonata .cap{font-size:.86rem;line-height:1.5;margin:0;color:#3a352e;min-height:4.2em;}',
      '.svw-sonata .cap b{color:#2d2a26;}',
      '.svw-sonata .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;}',
      '@media (min-width:620px){.svw-sonata{padding:1.35rem;}.svw-sonata .opts{grid-template-columns:repeat(4,1fr);}',
      '.svw-sonata .cap{min-height:4.5em;}}'
    ].join('');
    if (!still) {
      css += '.svw-sonata .opt,.svw-sonata .chip,.svw-sonata .band{transition:background-color .16s ease,border-color .16s ease,color .16s ease;}';
    }

    var style = document.createElement('style');
    style.textContent = css;
    root.appendChild(style);

    function el(tag, cls, text) {
      var n = document.createElement(tag);
      if (cls) n.className = cls;
      if (text != null) n.textContent = text;
      return n;
    }

    root.appendChild(el('p', 'kick', 'Sonata form'));
    root.appendChild(el('h3', null, 'Follow the keys'));
    var frameEl = el('p', 'frame', '');
    root.appendChild(frameEl);

    var stage = el('div', 'stage');
    var bandsEl = el('div', 'bands');
    var stsEl = el('div', 'sts');
    var bandNodes = [], stNodes = [];
    var i;
    for (i = 0; i < 3; i++) { var b = el('div', 'band', ''); bandsEl.appendChild(b); bandNodes.push(b); }
    for (i = 0; i < 5; i++) {
      var s = el('div', 'st');
      s.appendChild(el('span', 'dot'));
      s.appendChild(el('div', 'chip', ''));
      s.appendChild(el('div', 'role', ''));
      stsEl.appendChild(s);
      stNodes.push(s);
    }
    stage.appendChild(bandsEl);
    stage.appendChild(stsEl);
    var homeEl = el('p', 'home', '');
    stage.appendChild(homeEl);
    root.appendChild(stage);

    var optsEl = el('div', 'opts');
    var optNodes = [];
    for (i = 0; i < 4; i++) {
      var o = el('button', 'opt', '');
      o.type = 'button';
      o.setAttribute('aria-pressed', 'false');
      optsEl.appendChild(o);
      optNodes.push(o);
    }
    root.appendChild(optsEl);

    var bar = el('div', 'bar');
    var go = el('button', 'go', 'Check');
    go.type = 'button';
    var run = el('span', 'run', '');
    bar.appendChild(go);
    bar.appendChild(run);
    root.appendChild(bar);

    var cap = el('p', 'cap', '');
    root.appendChild(cap);
    var sr = el('p', 'sr');
    sr.setAttribute('aria-live', 'polite');
    root.appendChild(sr);

    /* ---------------- state ---------------- */
    var offset = Math.floor(Math.random() * HOMES.length);
    var n = 0, streak = 0, attempted = 0, mastered = false;
    var round = null, home = null, picked = null, checked = false;

    function pushState(extra) {
      var st = { streak: streak, mastered: mastered, attempted: attempted, round: round ? round.type : null, home: home ? tonic(home) : null, expected: round ? round.answer : null };
      if (extra) { for (var k in extra) { if (Object.prototype.hasOwnProperty.call(extra, k)) st[k] = extra[k]; } }
      root.dataset.svState = JSON.stringify(st);
    }

    function paintStations(list) {
      var cols = 'repeat(' + list.length + ',1fr)';
      stsEl.style.gridTemplateColumns = cols;
      bandsEl.style.gridTemplateColumns = cols;
      for (var j = 0; j < stNodes.length; j++) {
        var node = stNodes[j];
        if (j < list.length) {
          node.style.display = '';
          node.className = 'st ' + list[j].tone;
          node.childNodes[1].textContent = list[j].chip;
          node.childNodes[2].textContent = list[j].role;
        } else {
          node.style.display = 'none';
        }
      }
    }

    function paintBands(list) {
      for (var j = 0; j < bandNodes.length; j++) {
        var node = bandNodes[j];
        if (j < list.length) {
          node.style.display = '';
          node.style.gridColumn = list[j].span;
          node.className = 'band' + (list[j].on ? ' on' : '');
          node.textContent = list[j].label;
        } else {
          node.style.display = 'none';
        }
      }
    }

    function paintOptions() {
      for (var j = 0; j < optNodes.length; j++) {
        var node = optNodes[j];
        if (j < round.shown.length) {
          node.style.display = '';
          node.textContent = round.shown[j];
          node.disabled = false;
          node.setAttribute('aria-pressed', picked === round.shown[j] ? 'true' : 'false');
        } else {
          node.style.display = 'none';
        }
      }
    }

    function paintRun() {
      if (mastered) {
        run.className = 'run done';
        run.textContent = 'Mastered — keep going if you like';
      } else if (streak === 0) {
        run.className = 'run';
        run.textContent = attempted ? 'Run reset — three in a row ends it' : '';
      } else {
        run.className = 'run';
        run.textContent = streak + ' right in a row — ' + (3 - streak) + ' more and you have it';
      }
    }

    function newRound() {
      round = buildRound(n, offset);
      home = HOMES[(n + offset) % HOMES.length];
      var rot = n % round.options.length;
      round.shown = round.options.slice(rot).concat(round.options.slice(0, rot));
      picked = null;
      checked = false;
      frameEl.textContent = round.frame;
      paintBands(round.bands);
      paintStations(round.stations);
      homeEl.innerHTML = '';
      homeEl.appendChild(document.createTextNode('Home key '));
      var strong = document.createElement('b');
      strong.textContent = tonic(home);
      homeEl.appendChild(strong);
      paintOptions();
      go.textContent = 'Check';
      cap.textContent = round.type === 'section'
        ? 'Read the keys, then commit to a section.'
        : 'Choose the key you expect, then commit.';
      paintRun();
      pushState({ chosen: null, correct: null });
      n++;
    }

    function commit() {
      if (checked) { newRound(); optNodes[0].focus(); return; }
      if (!picked) {
        cap.textContent = 'Choose one of the keys first, then press Check.';
        sr.textContent = 'Choose an answer first.';
        optNodes[0].focus();
        return;
      }
      var ok = picked === round.answer;
      checked = true;
      attempted++;
      if (ok) { streak++; if (streak >= 3) { mastered = true; } } else { streak = 0; }

      if (round.type === 'section') {
        paintBands([{ label: round.resolveBand, span: round.bands[0].span, on: true }]);
      } else {
        var st = round.stations.slice();
        st[round.resolve.index] = { chip: round.resolve.chip, tone: round.resolve.tone, role: st[round.resolve.index].role };
        paintStations(st);
      }
      for (var j = 0; j < optNodes.length; j++) { optNodes[j].disabled = true; }

      var msg = (ok && mastered && streak === 3)
        ? shortVerdict(round, home, picked) + ' ' + MASTERY
        : feedback(round, home, picked, ok);
      cap.textContent = msg;
      sr.textContent = msg;
      go.textContent = mastered ? 'Another anyway' : 'Next movement';
      paintRun();
      pushState({ chosen: picked, correct: ok });
      go.focus();
    }

    optsEl.addEventListener('click', function (e) {
      var t = e.target;
      while (t && t !== optsEl && t.className !== 'opt') { t = t.parentNode; }
      if (!t || t === optsEl || t.disabled) { return; }
      picked = t.textContent;
      paintOptions();
      cap.textContent = round.type === 'section'
        ? 'You have chosen ' + picked + '. Press Check to see the section.'
        : 'You have chosen ' + picked + '. Press Check to see what the composer does.';
      sr.textContent = picked + ' selected.';
      pushState({ chosen: picked, correct: null });
    });

    go.addEventListener('click', commit);

    newRound();
  }

  window.SVWidget = {
    meta: {
      id: ID,
      title: 'Sonata form: follow the keys',
      teaches: 'Sonata form is defined by its key scheme: the second subject modulates away in the exposition and returns in the tonic at the recapitulation.'
    },
    mount: mount
  };
})();
