/* Timbre: same notes, different music.
   Self-contained lesson widget. No network, no audio, no storage.
   Nothing here plays or imitates a sound: the device works from where a
   fixed set of pitches sits inside each instrument's playing range. */
(function () {
  'use strict';

  var ID = 'timbre-integral-to-composition';

  /* ---------------- pitch + range model ----------------
     MIDI numbers, C4 = 60. Ranges are standard sounding ranges for the
     orchestral instruments named, kept conservative at both ends. Every
     register description in the widget is computed from this table; none
     of it is typed by hand. */

  var NAMES = ['C', 'C♯', 'D', 'E♭', 'E', 'F', 'F♯', 'G', 'A♭', 'A', 'B♭', 'B'];
  function pname(m) { return NAMES[((m % 12) + 12) % 12] + (Math.floor(m / 12) - 1); }

  var AXIS_LO = 24, AXIS_HI = 108;          /* C1 to C8, the drawn axis */
  function pct(m) { return ((m - AXIS_LO) / (AXIS_HI - AXIS_LO)) * 100; }

  var INST = {
    flute: { lo: 60, hi: 96 },
    corAnglais: { lo: 52, hi: 81 },
    clarinet: { lo: 50, hi: 91 },
    bassoon: { lo: 34, hi: 75 },
    horn: { lo: 35, hi: 77 },
    trumpet: { lo: 52, hi: 82 },
    trombone: { lo: 40, hi: 72 },
    violin: { lo: 55, hi: 100 },
    viola: { lo: 48, hi: 88 },
    cello: { lo: 36, hi: 81 },
    celesta: { lo: 60, hi: 108 }
  };

  /* Where the phrase sits inside an instrument's range, 0 = bottom, 1 = top. */
  function seat(key, phrase) {
    var i = INST[key];
    return (((phrase.lo + phrase.hi) / 2) - i.lo) / (i.hi - i.lo);
  }
  function regShort(key, phrase) {
    var p = seat(key, phrase);
    if (p < 0.26) { return 'low in its range'; }
    if (p < 0.60) { return 'mid-range'; }
    if (p < 0.84) { return 'high in its range'; }
    return 'the very top of its range';
  }
  function rangeText(key) {
    var i = INST[key];
    return pname(i.lo) + '–' + pname(i.hi);
  }
  function phraseText(p) { return pname(p.lo) + '–' + pname(p.hi); }

  /* ---------------- rounds ----------------
     Two kinds. 'score' = commit to the scoring that serves a stated
     effect. 'read' = the composer's re-scoring is given; commit to what
     the listener now hears. In both, one option is the misconception:
     that the notes are the music and the scoring is a wrapper. */

  var ROUNDS = [
    {
      id: 'strain', kind: 'score', phrase: { lo: 60, hi: 69 },
      frame: 'A closing phrase must sound strained and pleading. Choose the scoring.',
      options: [
        { name: 'bassoon', inst: 'bassoon', text: 'One bassoon, exposed, no doubling', right: true,
          fb: 'These notes sit high in the bassoon’s range, so the player must push, and the line sounds tight and strained.' },
        { name: 'flute', inst: 'flute', text: 'One flute, over held strings',
          fb: 'These notes are at the bottom of the flute’s range, where it sounds breathy and weak. Strain comes from playing near the top.' },
        { name: 'viola section', inst: 'viola', text: 'Viola section, all together',
          fb: 'Mid-range violas blend into one warm sound, and a section hides one player’s effort. The bassoon strains; violas do not.' },
        { mis: true, name: 'any of them would do', text: 'Any of them — the notes plead anyway',
          fb: 'The pitches are the same, but the three do not sound alike: the bassoon strains, the flute weakens, the violas sound calm.' }
      ]
    },
    {
      id: 'oneReed', kind: 'read', phrase: { lo: 62, hi: 71 },
      frame: 'Violas had this theme. One cor anglais now takes the same notes. What changes?',
      rows: [
        { prefix: 'Was: ', name: 'Viola section', inst: 'viola' },
        { prefix: 'Now: ', name: 'Solo cor anglais', inst: 'corAnglais', on: true }
      ],
      options: [
        { name: 'thinner and sadder', text: 'Thinner and sadder — one reed where a section had been', right: true,
          fb: 'One reed has a narrow, nasal tone where a dozen bowed strings were, so the line stops sounding like a group.' },
        { name: 'grander and more triumphant', text: 'Grander and more triumphant than before',
          fb: 'One reed takes weight away instead of adding it. The same notes now sound smaller and more alone.' },
        { name: 'quieter but otherwise the same', text: 'Quieter, but otherwise the same music',
          fb: 'Loudness is only part of it. The reedy tone changes the mood of the phrase, not just how loud it is.' },
        { mis: true, name: 'the same notes mean the same music', text: 'No real change — the pitches are the same, so the music is the same',
          fb: 'The pitches have not changed, so every difference you hear is timbre: violas sound like a group, one reed sounds alone.' }
      ]
    },
    {
      id: 'distance', kind: 'score', phrase: { lo: 53, hi: 60 },
      frame: 'The melody must sound distant, as if from another room. Choose the scoring.',
      options: [
        { name: 'muted horn', inst: 'horn', text: 'Muted horn, under quiet tremolo strings', right: true,
          fb: 'The mute makes the tone softer and duller, and the tremolo blurs it, so the same notes seem to come through a wall.' },
        { name: 'trombone section', inst: 'trombone', text: 'Trombone section, unison, loud and open',
          fb: 'That is a hard, close, brassy sound. Distance comes from softening the tone, not from choosing low notes.' },
        { name: 'cello section', inst: 'cello', text: 'Cello section, warm, doubled by violas',
          fb: 'A warm block of strings sounds close and solid. The muted horn under tremolo is the one that sounds far away.' },
        { mis: true, name: 'quiet playing sounds far away', text: 'Any of them, marked pianissimo — quiet playing sounds far away',
          fb: 'A quiet trombone section still sounds hard and close. Distance comes from the mute and the blurred tremolo.' }
      ]
    },
    {
      id: 'topOfRange', kind: 'read', phrase: { lo: 67, hi: 74 },
      frame: 'Violas had this phrase. One bassoon now takes the same pitches. What changes?',
      rows: [
        { prefix: 'Was: ', name: 'Viola section', inst: 'viola' },
        { prefix: 'Now: ', name: 'One bassoon', inst: 'bassoon', on: true }
      ],
      options: [
        { name: 'tighter and more exposed', text: 'Tighter, more strained, more exposed', right: true,
          fb: 'The pitches have not moved, but they sit at the very top of the bassoon’s range, and one reed replaces a section.' },
        { name: 'lower and heavier', text: 'Lower and heavier — the bassoon is a bass instrument',
          fb: 'The pitches have not changed. On the bassoon they sit at the very top of its range, so the sound is tight, not heavy.' },
        { name: 'warmer and rounder', text: 'Warmer and rounder than the violas were',
          fb: 'A section of violas is the warm option. One bassoon at the top of its range sounds thinner, and you hear the effort.' },
        { mis: true, name: 'nothing important changes', text: 'Nothing important changes — the pitches are the same',
          fb: 'That is the point: the pitches are fixed, so the strain, the thinness and the colour all come from the scoring.' }
      ]
    },
    {
      id: 'brilliance', kind: 'score', phrase: { lo: 72, hi: 79 },
      frame: 'The last phrase must cut through, hard and bright. Choose the scoring.',
      options: [
        { name: 'trumpets', inst: 'trumpet', text: 'Two trumpets, unmuted, no doubling', right: true,
          fb: 'High in its range the trumpet is hard and bright. Brass cuts through a loud orchestra; mid-range woodwind is covered.' },
        { name: 'flutes', inst: 'flute', text: 'Flutes, doubled by clarinets',
          fb: 'Mid-range woodwind blends in and gets buried under a loud orchestra. A cutting sound needs an edge; trumpets have it.' },
        { name: 'celesta', inst: 'celesta', text: 'Celesta alone',
          fb: 'It sparkles, but the sound is small and dies at once, so a full orchestra covers it. Trumpets ring out.' },
        { mis: true, name: 'any of them would do', text: 'Any of them — it is the top line, so it will cut through',
          fb: 'Being the top line does not make it heard. Flutes vanish under a loud orchestra; the same notes on trumpets ring out.' }
      ]
    },
    {
      id: 'massed', kind: 'read', phrase: { lo: 69, hi: 77 },
      frame: 'A solo flute had this line. The violins now play it, forte. What changes?',
      rows: [
        { prefix: 'Was: ', name: 'Solo flute', inst: 'flute' },
        { prefix: 'Now: ', name: 'Violin section', inst: 'violin', on: true }
      ],
      options: [
        { name: 'a whole section, not one voice', text: 'A whole section now, not one voice', right: true,
          fb: 'The pitches have not changed, but many players in unison give the line weight. It stops sounding like one person.' },
        { name: 'higher and brighter', text: 'Higher and brighter than the flute',
          fb: 'Nothing has been transposed: still A4 to F5, mid-range for violins. The weight and the colour change, not the pitch.' },
        { name: 'louder but still one player', text: 'Louder, but the line still sounds like one player',
          fb: 'Sixteen players in unison do not sound like one loud flute. The line sounds like a crowd, not one person.' },
        { mis: true, name: 'it is still the same tune', text: 'Not much — it is still the same tune',
          fb: 'The notes are fixed, so the scoring makes every difference: a solo flute sounds fragile, a section sounds strong.' }
      ]
    }
  ];
  var MASTERY = 'Three in a row — you have it. Change the instrument, the part of its range, or the number of players, and the same notes mean something new.';

  function rowsFor(r) {
    if (r.rows) { return r.rows; }
    var out = [], i;
    for (i = 0; i < r.options.length; i++) {
      if (r.options[i].inst) { out.push({ prefix: '', name: r.options[i].name, inst: r.options[i].inst, opt: i }); }
    }
    return out;
  }

  /* ---------------- mount ---------------- */

  function mount(root, ctx) {
    ctx = ctx || {};
    var cs = window.getComputedStyle(root);
    var accent = (cs.getPropertyValue('--accent') || '').trim() || ctx.accent || '#8a6a4f';
    var still = !!ctx.reducedMotion;

    root.className = (root.className ? root.className + ' ' : '') + 'svw-timbre';

    var css = [
      '.svw-timbre{position:relative;background:#fff;border:1px solid #e8e3db;border-radius:16px;padding:1rem;',
      'font-family:Inter,system-ui,-apple-system,sans-serif;color:#2d2a26;-webkit-text-size-adjust:100%;}',
      '.svw-timbre *{box-sizing:border-box;}',
      '.svw-timbre .kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:' + accent + ';margin:0 0 .2rem;}',
      '.svw-timbre h3{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.22rem;line-height:1.2;margin:0 0 .3rem;}',
      '.svw-timbre .frame{font-size:.86rem;line-height:1.4;margin:0 0 .5rem;color:#3a352e;}',
      '.svw-timbre .stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.45rem .55rem .3rem;margin:0 0 .5rem;}',
      '.svw-timbre .fixed{font-size:.72rem;line-height:1.3;color:#8d8880;margin:0 0 .28rem;}',
      '.svw-timbre .fixed b{color:#2d2a26;font-weight:600;font-variant-numeric:tabular-nums;}',
      '.svw-timbre .bars{position:relative;padding-top:2px;}',
      '.svw-timbre .row{position:relative;margin:0 0 .36rem;}',
      '.svw-timbre .rlab{font-size:.7rem;line-height:1.25;color:#77716a;margin:0 0 2px;}',
      '.svw-timbre .rlab b{color:#2d2a26;font-weight:600;}',
      '.svw-timbre .trk{position:relative;height:12px;border-radius:6px;background:#efe8dd;overflow:hidden;}',
      '.svw-timbre .seg{position:absolute;top:0;bottom:0;background:#d9d0bf;}',
      '.svw-timbre .row.on .seg{background:' + accent + '7a;}',
      '.svw-timbre .hit{position:absolute;top:0;bottom:0;background:#6f675c;}',
      '.svw-timbre .row.on .hit{background:#2d2a26;}',
      '.svw-timbre .row.on .trk{background:' + accent + '1f;}',
      '.svw-timbre .opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:.34rem;margin:0 0 .5rem;max-width:660px;}',
      '.svw-timbre .opt{font:600 .82rem Inter,system-ui,sans-serif;color:#2d2a26;padding:.4rem .55rem;border-radius:10px;',
      'border:1px solid #ddd7cd;background:#faf8f5;cursor:pointer;text-align:left;width:100%;line-height:1.3;}',
      '.svw-timbre .opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff;}',
      '.svw-timbre .opt[disabled]{cursor:default;opacity:.92;}',
      '.svw-timbre .bar{display:flex;align-items:center;gap:.55rem;flex-wrap:wrap;margin:0 0 .45rem;}',
      '.svw-timbre .go{font:600 .82rem Inter,system-ui,sans-serif;color:#fff;background:#2d2a26;border:1px solid #2d2a26;',
      'padding:.5rem .95rem;border-radius:10px;cursor:pointer;}',
      '.svw-timbre .go[disabled]{background:#faf8f5;border-color:#ddd7cd;color:#a9a298;cursor:default;}',
      '.svw-timbre .run{font-size:.74rem;color:#8d8880;}',
      '.svw-timbre .run.done{color:#4f7d63;font-weight:600;}',
      '.svw-timbre .cap{font-size:.86rem;line-height:1.42;margin:0;color:#3a352e;min-height:3.6em;}',
      '.svw-timbre .cap b{color:#2d2a26;}',
      '.svw-timbre .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;}'
    ].join('');
    if (!still) {
      css += '.svw-timbre .opt,.svw-timbre .seg,.svw-timbre .hit{transition:background-color .16s ease,border-color .16s ease,color .16s ease;}';
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

    root.appendChild(el('p', 'kick', 'Orchestration'));
    root.appendChild(el('h3', null, 'Same notes, different music'));
    var frameEl = el('p', 'frame', '');
    root.appendChild(frameEl);

    var stage = el('div', 'stage');
    var fixedEl = el('p', 'fixed', '');
    stage.appendChild(fixedEl);
    var barsEl = el('div', 'bars');
    var rowNodes = [], i;
    for (i = 0; i < 3; i++) {
      var rw = el('div', 'row');
      rw.appendChild(el('p', 'rlab', ''));
      var trk = el('div', 'trk');
      trk.appendChild(el('span', 'seg'));
      trk.appendChild(el('span', 'hit'));
      rw.appendChild(trk);
      barsEl.appendChild(rw);
      rowNodes.push(rw);
    }
    stage.appendChild(barsEl);
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

    var bar = el('div', 'bar');
    var go = el('button', 'go', 'Check');
    go.type = 'button';
    go.disabled = true;
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
    var offset = Math.floor(Math.random() * ROUNDS.length);
    var n = 0, streak = 0, attempted = 0, mastered = false;
    var round = null, shown = null, rows = null, picked = -1, checked = false;

    function answerIndex() {
      for (var j = 0; j < shown.length; j++) { if (shown[j].right) { return j; } }
      return -1;
    }

    function pushState(extra) {
      var st = {
        streak: streak, mastered: mastered, attempted: attempted,
        round: round ? round.id : null,
        kind: round ? round.kind : null,
        notes: round ? phraseText(round.phrase) : null,
        expected: (round && shown) ? shown[answerIndex()].text : null
      };
      if (extra) {
        for (var k in extra) {
          if (Object.prototype.hasOwnProperty.call(extra, k)) { st[k] = extra[k]; }
        }
      }
      root.dataset.svState = JSON.stringify(st);
    }

    function paintBars() {
      var p = round.phrase;
      for (var j = 0; j < rowNodes.length; j++) {
        var node = rowNodes[j];
        if (j >= rows.length) { node.style.display = 'none'; continue; }
        node.style.display = '';
        var r = rows[j], inst = INST[r.inst];
        var lab = node.childNodes[0];
        lab.textContent = '';
        if (r.prefix) { lab.appendChild(document.createTextNode(r.prefix)); }
        var b = document.createElement('b');
        b.textContent = r.name.charAt(0).toUpperCase() + r.name.slice(1);
        lab.appendChild(b);
        lab.appendChild(document.createTextNode(
          ' · ' + rangeText(r.inst) + ' · ' + regShort(r.inst, p)
        ));
        var trk = node.childNodes[1];
        trk.childNodes[0].style.left = pct(inst.lo) + '%';
        trk.childNodes[0].style.width = (pct(inst.hi) - pct(inst.lo)) + '%';
        trk.childNodes[1].style.left = pct(p.lo) + '%';
        trk.childNodes[1].style.width = (pct(p.hi) - pct(p.lo)) + '%';
      }
      paintRowState();
    }

    function paintRowState() {
      for (var j = 0; j < rows.length; j++) {
        var on = !!rows[j].on;
        if (picked >= 0 && round.kind === 'score') {
          on = shown[picked].mis ? true : (shown[picked].row === j);
        }
        rowNodes[j].className = 'row' + (on ? ' on' : '');
      }
    }

    function paintOptions() {
      for (var j = 0; j < optNodes.length; j++) {
        optNodes[j].textContent = shown[j].text;
        optNodes[j].setAttribute('aria-pressed', picked === j ? 'true' : 'false');
      }
    }

    function paintRun() {
      if (mastered) {
        run.className = 'run done';
        run.textContent = 'Mastered — carry on';
      } else if (streak === 0) {
        run.className = 'run';
        run.textContent = attempted ? 'Back to zero — 3 in a row to go' : '';
      } else {
        run.className = 'run';
        run.textContent = streak + ' in a row — ' + (3 - streak) + ' to go';
      }
    }

    function newRound() {
      round = ROUNDS[(n + offset) % ROUNDS.length];
      var rot = n % round.options.length;
      shown = round.options.slice(rot).concat(round.options.slice(0, rot));
      rows = rowsFor(round);
      /* link each score-round option to the bar it describes */
      for (var j = 0; j < shown.length; j++) {
        shown[j].row = -1;
        for (var k = 0; k < rows.length; k++) {
          if (rows[k].inst && shown[j].inst === rows[k].inst) { shown[j].row = k; }
        }
      }
      picked = -1;
      checked = false;
      frameEl.textContent = round.frame;
      fixedEl.innerHTML = '';
      fixedEl.appendChild(document.createTextNode('Same notes in every version: '));
      var strong = document.createElement('b');
      strong.textContent = phraseText(round.phrase);
      fixedEl.appendChild(strong);
      fixedEl.appendChild(document.createTextNode('.'));
      paintBars();
      paintOptions();
      for (var q = 0; q < optNodes.length; q++) { optNodes[q].disabled = false; }
      go.textContent = 'Check';
      go.disabled = true;
      cap.textContent = round.kind === 'score'
        ? 'Each row shows one instrument’s range. The dark block is where these notes fall.'
        : 'Both rows show the same notes. What has changed is the instrument, and how many play it.';
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

      /* reveal: the scoring the composer actually chose is lit on the stage */
      var ai = answerIndex();
      for (var j = 0; j < rows.length; j++) {
        var on = (round.kind === 'score') ? (shown[ai].row === j) : !!rows[j].on;
        rowNodes[j].className = 'row' + (on ? ' on' : '');
      }
      for (var q = 0; q < optNodes.length; q++) { optNodes[q].disabled = true; }

      var msg;
      if (ok && mastered && streak === 3) {
        msg = 'Right — you said ' + shortOf(choice) + '. ' + MASTERY;
      } else {
        msg = (ok ? 'Right — ' : 'Not quite — ') + 'you said ' + shortOf(choice) + '. ' + choice.fb;
      }
      cap.textContent = msg;
      sr.textContent = msg;
      go.textContent = mastered ? 'Another anyway' : 'Next scoring';
      go.disabled = false;
      paintRun();
      pushState({ chosen: choice.text, correct: ok, misconception: !!choice.mis });
      go.focus();
    }

    function shortOf(choice) { return choice.name; }

    optsEl.addEventListener('click', function (e) {
      var t = e.target;
      while (t && t !== optsEl && !(t.classList && t.classList.contains('opt'))) { t = t.parentNode; }
      if (!t || t === optsEl || t.disabled) { return; }
      picked = parseInt(t.getAttribute('data-i'), 10);
      paintOptions();
      paintRowState();
      go.disabled = false;
      var c = shown[picked];
      cap.textContent = 'You have chosen: ' + c.text + '.';
      sr.textContent = c.text + ' selected.';
      pushState({ chosen: c.text, correct: null, misconception: !!c.mis });
    });

    go.addEventListener('click', commit);

    newRound();
  }

  window.SVWidget = {
    meta: {
      id: ID,
      title: 'Timbre: same notes, different music',
      teaches: 'Timbre is chosen alongside the notes, not added afterwards: the same pitches change meaning depending on which instrument plays them, where they sit in its range, and how many players carry them.'
    },
    mount: mount
  };
})();
