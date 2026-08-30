/* post-production-parallel-workflow
   A post schedule drawn as a week strip. The student predicts what can run
   alongside an unlocked edit, and what has to be redone when the cut changes
   after picture lock. Every schedule consequence is computed from one
   dependency model, so the reveal redraws the strip from the same numbers. */
(function () {
  'use strict';

  /* ---------- the dependency model -------------------------------------- */

  var ROWS = [
    { key: 'editor',   label: 'Editor' },
    { key: 'sound',    label: 'Sound designer' },
    { key: 'colour',   label: 'Colourist' },
    { key: 'vfx',      label: 'VFX & graphics' },
    { key: 'composer', label: 'Composer' }
  ];

  function rowIndex(k) {
    for (var i = 0; i < ROWS.length; i++) if (ROWS[i].key === k) return i;
    return 0;
  }

  /* Four small productions. Weeks only; every derived date comes from here. */
  var PROJECTS = [
    {
      id: 'harbour', name: 'Harbour Rescue', kind: 'charity film',
      assemble: 2, fine: 3,
      soundStart: 3, vfxStart: 3, scoreStart: 4, vfxLabel: 'Titles',
      mix: 2, grade: 2, renders: 1, record: 1,
      recut: { scene: 'the lifeboat launch', longer: true, graphics: false }
    },
    {
      id: 'market', name: 'Night Market', kind: '90-second promo',
      assemble: 1, fine: 2,
      soundStart: 2, vfxStart: 2, scoreStart: 2, vfxLabel: 'Graphics',
      mix: 1, grade: 1, renders: 1, record: 1,
      recut: { scene: 'the closing logo shot', longer: false, graphics: true }
    },
    {
      id: 'ridge', name: 'Ridge Runner', kind: 'game trailer',
      assemble: 2, fine: 2,
      soundStart: 3, vfxStart: 2, scoreStart: 3, vfxLabel: 'VFX shots',
      mix: 2, grade: 1, renders: 1, record: 1,
      recut: { scene: 'the ridge chase', longer: true, graphics: true }
    },
    {
      id: 'serve', name: 'Second Serve', kind: 'sports short',
      assemble: 2, fine: 3,
      soundStart: 4, vfxStart: 3, scoreStart: 3, vfxLabel: 'Stats',
      mix: 2, grade: 1, renders: 1, record: 1,
      recut: { scene: 'the final rally', longer: false, graphics: false }
    }
  ];

  function plan(p) {
    var lock = p.assemble + p.fine;
    var postMax = Math.max(p.mix, p.grade, p.renders, p.record);
    var master = lock + postMax + 1;
    return { lock: lock, master: master, recutWeek: master,
             redoWeek: master + 1, newMaster: master + 2 };
  }

  /* Which strands must redo work after a post-lock re-cut. Sound and colour
     always re-conform to a changed picture; music only if the timings move;
     graphics only if that scene carries any. */
  function rippleSet(p) {
    var s = ['fm', 'cg'];
    if (p.recut.longer) s.push('rs');
    if (p.recut.graphics) s.push('fx');
    return s;
  }

  /* Jobs a small post team might have on its list. lock:true means the job
     conforms to the final picture and cannot start until picture lock. */
  var POOL = [
    { id: 'sd', row: 'sound',    label: 'Sound design',      ref: 'sound design',        lock: false, len: 2, bl: 'Sound design' },
    { id: 'vo', row: 'sound',    label: 'Record voice-over', ref: 'the voice-over',      lock: false, len: 1, bl: 'Voice-over' },
    { id: 'tm', row: 'sound',    label: 'Temp mix',          ref: 'the temp mix',        lock: false, len: 1, bl: 'Temp mix' },
    { id: 'fm', row: 'sound',    label: 'Final mix',         ref: 'the final mix',       lock: true,  len: 2, bl: 'Mix' },
    { id: 'gt', row: 'colour',   label: 'Grade tests',       ref: 'the grade tests',     lock: false, len: 1, bl: 'Grade tests' },
    { id: 'cg', row: 'colour',   label: 'Colour grade',      ref: 'the colour grade',    lock: true,  len: 2, bl: 'Grade' },
    { id: 'bt', row: 'vfx',      label: 'Build titles',      ref: 'the titles build',    lock: false, len: 2, bl: 'Titles' },
    { id: 'fx', row: 'vfx',      label: 'VFX renders',       ref: 'the VFX renders',     lock: true,  len: 1, bl: 'Renders' },
    { id: 'cs', row: 'composer', label: 'Compose to cut',    ref: 'composing',           lock: false, len: 2, bl: 'Compose' },
    { id: 'rs', row: 'composer', label: 'Record the score',  ref: 'the score record',    lock: true,  len: 1, bl: 'Score',
      label2: 'Music score', ref2: 'the music score' },
    { id: 'st', row: 'editor',   label: 'Subtitle timings',  ref: 'subtitle timing',     lock: true,  len: 1, bl: 'Subtitles' },
    { id: 'dx', row: 'editor',   label: 'Client exports',    ref: 'the client exports',  lock: true,  len: 1, bl: 'Exports' }
  ];

  function poolById(id) {
    for (var i = 0; i < POOL.length; i++) if (POOL[i].id === id) return POOL[i];
    return null;
  }

  /* ---------- small helpers --------------------------------------------- */

  function shuffle(a) {
    var r = a.slice();
    for (var i = r.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), t = r[i]; r[i] = r[j]; r[j] = t;
    }
    return r;
  }
  function pickDistinctRows(list, n) {
    var used = {}, out = [];
    var s = shuffle(list);
    for (var i = 0; i < s.length && out.length < n; i++) {
      if (used[s[i].row]) continue;
      used[s[i].row] = 1; out.push(s[i]);
    }
    return out;
  }
  function and(list) {
    if (!list.length) return 'nothing';
    if (list.length === 1) return list[0];
    return list.slice(0, -1).join(', ') + ' and ' + list[list.length - 1];
  }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  function sameSet(a, b) {
    if (a.length !== b.length) return false;
    var m = {}; a.forEach(function (x) { m[x] = 1; });
    for (var i = 0; i < b.length; i++) if (!m[b[i]]) return false;
    return true;
  }
  function hexRgba(hex, alpha) {
    var h = String(hex || '').trim().replace('#', '');
    if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
    if (!/^[0-9a-f]{6}$/i.test(h)) h = '8a6a4f';
    return 'rgba(' + parseInt(h.slice(0, 2), 16) + ',' + parseInt(h.slice(2, 4), 16) +
           ',' + parseInt(h.slice(4, 6), 16) + ',' + alpha + ')';
  }

  /* ---------- styles (every selector scoped to .svw-ppw) ---------------- */

  var CSS = [
    '.svw-ppw{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.45;}',
    '.svw-ppw *{box-sizing:border-box;}',
    '.svw-ppw .kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--ppw-a);}',
    '.svw-ppw .ttl{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.2rem;margin:.05rem 0 .25rem;line-height:1.2;}',
    '.svw-ppw .frame{font-size:.84rem;color:#4a453e;margin:0 0 .45rem;min-height:2.5em;}',
    '.svw-ppw .strip{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.4rem .45rem .45rem;}',
    '.svw-ppw .g{display:grid;column-gap:0;row-gap:2px;align-items:center;}',
    '.svw-ppw .lockcap{font-size:.66rem;color:#8d8880;white-space:nowrap;text-align:right;padding-right:3px;overflow:hidden;}',
    '.svw-ppw .wk{font-size:.66rem;color:#8d8880;text-align:center;font-variant-numeric:tabular-nums;}',
    '.svw-ppw .wk--del{background:#2d2a26;color:#fff;border-radius:4px;font-weight:600;}',
    '.svw-ppw .delcap{font-size:.66rem;color:#2d2a26;font-weight:600;white-space:nowrap;text-align:right;padding-right:3px;overflow:hidden;}',
    '.svw-ppw .rl{font-size:.67rem;font-weight:600;color:#5b564e;padding-right:6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}',
    '.svw-ppw .lane{align-self:stretch;background:#f3eee6;border-radius:5px;}',
    '.svw-ppw .lockline{align-self:stretch;border-right:1px dashed #a89f90;pointer-events:none;}',
    '.svw-ppw .bar{height:20px;border-radius:5px;display:flex;align-items:center;justify-content:center;',
    'font-size:.66rem;font-weight:600;overflow:hidden;white-space:nowrap;min-width:0;padding:0 3px;}',
    '.svw-ppw .bar--edit{background:#2d2a26;border:1px solid #2d2a26;color:#fff;}',
    '.svw-ppw .bar--pre{background:var(--ppw-tint);border:1px solid var(--ppw-line);color:#3c372f;}',
    '.svw-ppw .bar--post{background:#f1ece4;border:1px solid #d8d0c4;color:#5b564e;}',
    '.svw-ppw .bar--redo{background:repeating-linear-gradient(135deg,#e8ded1 0 4px,#f7f2ea 4px 9px);border:1px solid #c8bcaa;color:#4a453e;}',
    '.svw-ppw .chips{display:grid;grid-template-columns:repeat(auto-fill,minmax(142px,1fr));gap:5px;margin:.45rem 0 .42rem;}',
    '.svw-ppw .chip{font:600 .76rem/1.3 Inter,system-ui,sans-serif;text-align:left;color:#2d2a26;background:#faf8f5;',
    'border:1px solid #ddd7cd;border-radius:10px;padding:.42rem .55rem;cursor:pointer;}',
    '.svw-ppw.motion .chip{transition:background-color .12s ease,border-color .12s ease;}',
    '.svw-ppw .chip.none{grid-column:1/-1;}',
    '.svw-ppw .chip[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff;}',
    '.svw-ppw .chip:focus-visible{outline:2px solid var(--ppw-a);outline-offset:2px;}',
    '.svw-ppw .chip.hit{background:#eef3ef;border-color:#4f7d63;color:#33543f;}',
    '.svw-ppw .chip.bad{background:#f4f1ec;border-color:#e4ded4;color:#8d8880;text-decoration:line-through;}',
    '.svw-ppw .chip.miss{background:var(--ppw-tint);border-color:var(--ppw-line);border-style:dashed;color:#4a453e;}',
    '.svw-ppw .chip[disabled]{cursor:default;}',
    '.svw-ppw .go{display:flex;align-items:center;gap:.65rem;flex-wrap:wrap;}',
    '.svw-ppw .btn{font:600 .82rem/1.2 Inter,system-ui,sans-serif;background:#2d2a26;color:#fff;border:1px solid #2d2a26;',
    'border-radius:10px;padding:.5rem .95rem;cursor:pointer;}',
    '.svw-ppw .btn[disabled]{background:#faf8f5;color:#a9a29a;border-color:#ddd7cd;cursor:default;}',
    '.svw-ppw .btn:focus-visible{outline:2px solid var(--ppw-a);outline-offset:2px;}',
    '.svw-ppw .run{font-size:.74rem;color:#8d8880;}',
    '.svw-ppw .cap{font-size:.82rem;line-height:1.48;color:#3c372f;margin:.45rem 0 0;min-height:2em;}',
    '.svw-ppw .cap b{font-weight:600;}',
    '.svw-ppw .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;}'
  ].join('');

  /* ---------- widget ----------------------------------------------------- */

  window.SVWidget = {
    meta: {
      id: 'post-production-parallel-workflow',
      title: 'The post-production schedule',
      teaches: 'Post-production runs several specialists in parallel off shared versions; picture lock is the point the picture stops moving, and a re-cut after it forces sound, colour, graphics and music to re-conform.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent ||
        (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';
      var reduced = !!ctx.reducedMotion;

      var LABEL_W = 86, ROW_H = 23;

      var wrap = document.createElement('div');
      wrap.className = 'svw-ppw' + (reduced ? '' : ' motion');
      wrap.style.setProperty('--ppw-a', accent);
      wrap.style.setProperty('--ppw-tint', hexRgba(accent, 0.22));
      wrap.style.setProperty('--ppw-line', hexRgba(accent, 0.68));

      var style = document.createElement('style');
      style.textContent = CSS;
      wrap.appendChild(style);

      var kick = mk('div', 'kick');
      var ttl = mk('div', 'ttl'); ttl.textContent = 'The post-production schedule';
      var frame = mk('p', 'frame');
      var strip = mk('div', 'strip');
      var grid = mk('div', 'g'); strip.appendChild(grid);
      var chipBox = mk('div', 'chips');
      var goRow = mk('div', 'go');
      var btn = document.createElement('button');
      btn.type = 'button'; btn.className = 'btn'; btn.textContent = 'Check the schedule';
      var runLine = mk('span', 'run');
      goRow.appendChild(btn); goRow.appendChild(runLine);
      var capBox = mk('p', 'cap');
      var sr = mk('p', 'sr'); sr.setAttribute('aria-live', 'polite');

      [kick, ttl, frame, strip, chipBox, goRow, capBox, sr].forEach(function (n) { wrap.appendChild(n); });
      root.appendChild(wrap);

      /* six reusable chip buttons: five options plus the whole-chain option */
      var CHIPS = [];
      for (var c = 0; c < 6; c++) {
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'chip'; b.setAttribute('aria-pressed', 'false');
        b.addEventListener('click', onChip);
        chipBox.appendChild(b); CHIPS.push(b);
      }
      btn.addEventListener('click', onGo);

      var st = { round: 0, streak: 0, mastered: false, attempted: 0, committed: false };
      var R = null;

      newRound();

      /* ---------- round construction -------------------------------------- */

      function newRound() {
        var p = PROJECTS[Math.floor(st.round / 2) % PROJECTS.length];
        var type = (st.round % 2 === 0) ? 'parallel' : 'ripple';
        var d = plan(p);
        R = { p: p, d: d, type: type, picked: {}, committed: false };

        if (type === 'parallel') {
          var free = POOL.filter(function (t) { return !t.lock; });
          var held = POOL.filter(function (t) { return t.lock; });
          var nFree = 2 + Math.floor(Math.random() * 2);          /* 2 or 3 */
          R.options = shuffle(pickDistinctRows(free, nFree)
                        .concat(pickDistinctRows(held, 5 - nFree)));
          R.correct = R.options.filter(function (t) { return !t.lock; })
                               .map(function (t) { return t.id; });
          R.noneLabel = 'None — they all wait for the locked edit';
          R.weeks = d.master;
          frame.textContent = 'Picture lock is the end of week ' + d.lock +
            '. Select every job that can already be under way before then.';
        } else {
          R.options = ['fm', 'cg', 'fx', 'rs'].map(poolById);
          R.correct = rippleSet(p);
          R.noneLabel = 'Nothing else — only the edit changes';
          R.weeks = d.newMaster;
          frame.textContent = 'In week ' + d.master + ' the client asks for ' + p.recut.scene +
            ' to be re-cut. ' + (p.recut.longer ? 'The scene gets longer.'
                                                : 'The new shot is the same length.') +
            (p.recut.graphics ? ' It carries graphics.' : ' It has no graphics in it.') +
            ' Select every strand that must redo work.';
        }

        kick.textContent = p.name + ' · ' + p.kind;
        drawChips();
        renderStrip(baseBars(), R.d.master);
        capBox.textContent = '';
        runLine.textContent = st.streak ? runText() : '';
        btn.textContent = st.mastered ? 'Another anyway' : 'Check the schedule';
        btn.disabled = true;
        publish(null);
      }

      function drawChips() {
        for (var i = 0; i < CHIPS.length; i++) {
          var b = CHIPS[i];
          b.className = 'chip'; b.setAttribute('aria-pressed', 'false');
          if (i < R.options.length) {
            b.hidden = false; b.disabled = false;
            b.textContent = (R.type === 'ripple' && R.options[i].label2) ?
              R.options[i].label2 : R.options[i].label;
            b.dataset.id = R.options[i].id;
          } else if (i === R.options.length) {
            b.hidden = false; b.disabled = false; b.className = 'chip none';
            b.textContent = R.noneLabel; b.dataset.id = 'none';
          } else {
            b.hidden = true; b.disabled = true; b.textContent = ''; b.dataset.id = '';
          }
        }
      }

      /* ---------- the strip ------------------------------------------------ */

      function bar(row, from, to, label, tone) {
        return { row: row, from: from, to: to, label: label, tone: tone };
      }

      /* The schedule as it stands before the student commits. */
      function baseBars() {
        var p = R.p, d = R.d, b = [];
        b.push(bar('editor', 1, p.assemble, 'Assemble', 'edit'));
        b.push(bar('editor', p.assemble + 1, d.lock, 'Fine cut', 'edit'));
        if (R.type === 'ripple') {
          b.push(bar('sound', p.soundStart, d.lock, 'Sound design', 'pre'));
          b.push(bar('sound', d.lock + 1, d.lock + p.mix, 'Mix', 'post'));
          b.push(bar('colour', d.lock + 1, d.lock + p.grade, 'Grade', 'post'));
          b.push(bar('vfx', p.vfxStart, d.lock, p.vfxLabel, 'pre'));
          b.push(bar('vfx', d.lock + 1, d.lock + p.renders, 'Renders', 'post'));
          b.push(bar('composer', p.scoreStart, d.lock, 'Compose', 'pre'));
          b.push(bar('composer', d.lock + 1, d.lock + p.record, 'Score', 'post'));
        }
        return b;
      }

      /* The same model, recomputed for the reveal. */
      function revealBars() {
        var p = R.p, d = R.d;
        if (R.type === 'parallel') {
          var b = baseBars(), post = {};
          R.options.forEach(function (t) {
            if (!t.lock) {
              var span = Math.min(Math.max(t.len, 2), d.lock - 1);
              b.push(bar(t.row, d.lock - span + 1, d.lock, t.bl, 'pre'));
            } else {
              var start = d.lock + 1 + (post[t.row] || 0);
              var room = Math.max(1, d.master - 1 - start + 1);
              var len = Math.min(Math.max(t.len, 2), room);
              post[t.row] = (post[t.row] || 0) + len;
              b.push(bar(t.row, start, start + len - 1, t.bl, 'post'));
            }
          });
          return b;
        }
        var r = baseBars();
        /* strip the old master week, then rebuild the tail from the re-cut */
        r.push(bar('editor', d.recutWeek, d.recutWeek, 'Re-cut', 'edit'));
        R.correct.forEach(function (id) {
          var t = poolById(id);
          r.push(bar(t.row, d.redoWeek, d.redoWeek, 'Redo', 'redo'));
        });
        return r;
      }

      function renderStrip(bars, deliver) {
        var n = R.weeks, i, w;
        R.deliver = deliver;
        while (grid.firstChild) grid.removeChild(grid.firstChild);
        grid.style.gridTemplateColumns = LABEL_W + 'px repeat(' + n + ',1fr)';
        grid.style.gridTemplateRows = '13px 15px repeat(' + ROWS.length + ',' + ROW_H + 'px)';

        var lc = mk('div', 'lockcap'); lc.textContent = 'picture lock';
        lc.style.gridColumn = '2 / span ' + R.d.lock; lc.style.gridRow = '1';
        grid.appendChild(lc);

        var dc = mk('div', 'delcap'); dc.textContent = 'master';
        dc.style.gridColumn = (R.d.lock + 2) + ' / span ' + (deliver - R.d.lock);
        dc.style.gridRow = '1';
        grid.appendChild(dc);

        for (w = 1; w <= n; w++) {
          var cell = mk('div', 'wk' + (w === deliver ? ' wk--del' : ''));
          cell.textContent = String(w);
          if (w === deliver) cell.setAttribute('aria-label', 'week ' + w + ', master delivered');
          cell.style.gridColumn = String(w + 1); cell.style.gridRow = '2';
          grid.appendChild(cell);
        }
        for (i = 0; i < ROWS.length; i++) {
          var lab = mk('div', 'rl'); lab.textContent = ROWS[i].label;
          lab.style.gridColumn = '1'; lab.style.gridRow = String(3 + i);
          grid.appendChild(lab);
          var lane = mk('div', 'lane');
          lane.style.gridColumn = '2 / -1'; lane.style.gridRow = String(3 + i);
          grid.appendChild(lane);
        }
        var ll = mk('div', 'lockline');
        ll.style.gridColumn = String(R.d.lock + 1); ll.style.gridRow = '1 / -1';
        grid.appendChild(ll);

        bars.forEach(function (b) {
          var el = mk('div', 'bar bar--' + b.tone);
          el.style.gridColumn = (b.from + 1) + ' / span ' + (b.to - b.from + 1);
          el.style.gridRow = String(3 + rowIndex(b.row));
          el.setAttribute('role', 'img');
          el.setAttribute('aria-label', ROWS[rowIndex(b.row)].label + ': ' + b.label +
            ', week ' + b.from + (b.to > b.from ? ' to ' + b.to : ''));
          var t = document.createElement('span');
          t.textContent = b.label;
          el.appendChild(t);
          grid.appendChild(el);
        });
        fitBars();
      }

      /* Bar captions only survive where the bar is wide enough to hold them. */
      function fitBars() {
        var bs = grid.querySelectorAll('.bar');
        for (var i = 0; i < bs.length; i++) {
          var span = bs[i].firstChild;
          if (!span) continue;
          span.style.display = '';
          if (bs[i].scrollWidth > bs[i].clientWidth) span.style.display = 'none';
        }
      }

      /* ---------- interaction --------------------------------------------- */

      function onChip(e) {
        var b = e.currentTarget;
        if (R.committed || b.disabled) return;
        var id = b.dataset.id;
        var on = b.getAttribute('aria-pressed') === 'true';
        if (!on && id === 'none') {
          CHIPS.forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
          R.picked = {};
        } else if (!on) {
          var noneBtn = CHIPS[R.options.length];
          noneBtn.setAttribute('aria-pressed', 'false');
          delete R.picked.none;
        }
        if (on) { delete R.picked[id]; } else { R.picked[id] = 1; }
        b.setAttribute('aria-pressed', on ? 'false' : 'true');
        btn.disabled = !picks().length;
        publish(null);
      }

      function picks() { return Object.keys(R.picked); }

      function onGo() {
        if (R.committed) { st.round++; newRound(); return; }
        var chosen = picks();
        if (!chosen.length) return;

        var ok = sameSet(chosen, R.correct);
        R.committed = true;
        st.attempted++;
        st.streak = ok ? st.streak + 1 : 0;
        if (ok && st.streak >= 3) st.mastered = true;

        markChips(chosen);
        renderStrip(revealBars(), R.type === 'ripple' ? R.d.newMaster : R.d.master);
        var msg = ok ? rightText(chosen) : wrongText(chosen);
        capBox.innerHTML = msg;
        sr.textContent = capBox.textContent;
        runLine.textContent = runText();
        btn.textContent = st.mastered ? 'Another anyway' : 'Next project';
        btn.disabled = false;
        publish(ok);
      }

      function markChips(chosen) {
        var want = {}; R.correct.forEach(function (i) { want[i] = 1; });
        var got = {}; chosen.forEach(function (i) { got[i] = 1; });
        for (var i = 0; i < CHIPS.length; i++) {
          var b = CHIPS[i]; if (b.hidden) continue;
          var id = b.dataset.id;
          b.disabled = true;
          b.className = 'chip' + (id === 'none' ? ' none' : '') +
            (got[id] && want[id] ? ' hit' : got[id] ? ' bad' : want[id] ? ' miss' : '');
        }
      }

      function runText() {
        if (st.mastered) return 'you have it';
        if (!st.streak) return '';
        return st.streak === 1 ? '1 right in a row — two more'
                               : st.streak + ' right in a row — one more and you have it';
      }

      /* ---------- what the feedback says ---------------------------------- */

      function refsOf(ids) {
        return ids.map(function (i) {
          var t = poolById(i);
          return (R.type === 'ripple' && t.ref2) ? t.ref2 : t.ref;
        });
      }
      function safeWhy(id) {
        if (id === 'fx') return 'that scene carries no graphics';
        if (id === 'rs') return 'the shot lengths do not move';
        return 'it is not tied to the picture';
      }

      function rightText(chosen) {
        if (st.mastered) return masterText();
        var d = R.d, p = R.p;
        if (R.type === 'parallel') {
          var waits = R.options.filter(function (t) { return t.lock; })
                               .map(function (t) { return t.ref; });
          var many = chosen.length > 2 ? 'all ' : chosen.length === 2 ? 'both ' : '';
          return 'Right — ' + and(refsOf(chosen)) + ' ' + many +
            (chosen.length === 1 ? 'works' : 'work') + ' to a rough cut, so ' +
            (chosen.length === 1 ? 'it overlaps' : 'they overlap') + ' the edit. ' +
            cap(and(waits)) + ' conform to the final picture and wait for <b>picture lock</b> in week ' +
            d.lock + '.';
        }
        var safe = [];
        if (!p.recut.longer) safe.push('the score holds');
        if (!p.recut.graphics) safe.push('the graphics hold');
        return 'Right — ' + and(refsOf(chosen)) + ' must re-conform to the new cut, so the master slips from week ' +
          d.master + ' to week ' + d.newMaster + '.' +
          (safe.length ? ' ' + cap(and(safe)) + ': that part of the picture has not moved.' : '');
      }

      function masterText() {
        return 'Right — three in a row. You have it: post runs several specialists at once from shared ' +
          'versions, and <b>picture lock</b> is the moment the picture stops moving so the mix and the ' +
          'grade can conform to it.';
      }

      function wrongText(chosen) {
        var d = R.d;
        var want = {}; R.correct.forEach(function (i) { want[i] = 1; });
        var extra = chosen.filter(function (i) { return i !== 'none' && !want[i]; });
        var missed = R.correct.filter(function (i) { return chosen.indexOf(i) < 0; });
        var saidNone = chosen.indexOf('none') >= 0;
        var bits = [];

        if (R.type === 'parallel') {
          if (saidNone) bits.push('you said they all wait for the locked edit');
          else {
            if (extra.length) bits.push('you picked ' + and(refsOf(extra)) + ', which conform' +
              (extra.length === 1 ? 's' : '') + ' to the final picture');
            if (missed.length) bits.push((bits.length ? 'and left out ' : 'you left out ') + and(refsOf(missed)));
          }
          return 'Not quite — ' + bits.join(' ') + '. ' + cap(and(refsOf(R.correct))) +
            ' work to a rough cut and overlap the edit; the rest wait for <b>picture lock</b> in week ' +
            d.lock + '.';
        }
        if (saidNone) bits.push('you said only the edit changes');
        else {
          if (extra.length) bits.push('you picked ' + and(refsOf(extra)) + ', but ' + and(extra.map(safeWhy)));
          if (missed.length) bits.push((bits.length ? 'and left out ' : 'you left out ') + and(refsOf(missed)));
        }
        return 'Not quite — ' + bits.join(' ') + '. ' + cap(and(refsOf(R.correct))) +
          ' must re-conform to the new cut, so the master slips from week ' + d.master +
          ' to week ' + d.newMaster + '.';
      }

      /* ---------- state for the gate --------------------------------------- */

      function publish(correct) {
        root.dataset.svState = JSON.stringify({
          project: R.p.id, type: R.type, week: R.d.lock,
          selected: picks().sort(), correct: correct,
          streak: st.streak, mastered: st.mastered, attempted: st.attempted
        });
      }

      function mk(tag, cls) {
        var n = document.createElement(tag);
        n.className = cls;
        return n;
      }

      if (typeof ResizeObserver === 'function') {
        var ro = new ResizeObserver(function () { fitBars(); });
        ro.observe(wrap);
      }
    }
  };
})();
