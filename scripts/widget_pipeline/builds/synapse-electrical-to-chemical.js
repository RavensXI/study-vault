/* StudyVault lesson widget: synapse-electrical-to-chemical
   Self-contained. No imports, no network, no globals beyond window.SVWidget. */
(function () {
  'use strict';

  var STEPS = [
    { n: 1, label: 'Impulse arrives at the gap',     form: 'electrical' },
    { n: 2, label: 'Neurotransmitter released',      form: 'chemical'   },
    { n: 3, label: 'Diffuses across the gap',        form: 'chemical'   },
    { n: 4, label: 'Binds to receptor molecules',    form: 'chemical'   },
    { n: 5, label: 'A new impulse starts',           form: 'electrical' }
  ];

  /* stop = the last step in the chain that still happens.
     art  = how the scenario is drawn on the diagram. */
  var ITEMS = [
    {
      id: 'normal',
      text: 'A normal impulse travels down the first neurone and reaches the gap.',
      stop: 5, art: {},
      why: 'Electrical, chemical, then electrical again. The impulse stops at the membrane; a chemical crosses; binding starts a brand-new impulse.'
    },
    {
      id: 'empty',
      text: 'The vesicles at the end of the first neurone are empty — no neurotransmitter is stored.',
      stop: 1, art: { vesicles: 'empty' },
      why: 'With no chemical to release, nothing crosses. An impulse cannot jump the gap by itself — only neurotransmitter closes it.'
    },
    {
      id: 'backwards',
      text: 'An impulse travels the wrong way and arrives at the gap from the receptor side.',
      stop: 1, art: { dir: -1 },
      why: 'Traffic is one-way: vesicles sit only in the first neurone and receptors only on the other membrane, so nothing can be released from this side.'
    },
    {
      id: 'blocker',
      text: 'A drug has settled into the receptor molecules, so the neurotransmitter cannot fit them.',
      stop: 3, art: { receptors: 'plug' },
      why: 'Still released, and it still diffuses across — diffusion needs no receptors. But crossing is not the signal: no new impulse until it binds.'
    },
    {
      id: 'shape',
      text: 'The receptor molecules on the next neurone are the wrong shape for this neurotransmitter.',
      stop: 3, art: { receptors: 'wrong' },
      why: 'Receptors are shape-specific. The molecules reach the membrane but cannot fit it, so the message dies in the gap it has just crossed.'
    },
    {
      id: 'enzyme',
      text: 'An enzyme in the gap breaks the neurotransmitter down as soon as it is released.',
      stop: 2, art: { gap: 'enzyme' },
      why: 'Released, then destroyed before it could cross. Nothing reaches the receptors. Breaking it down is also how a synapse switches itself off.'
    },
    {
      id: 'wider',
      text: 'This gap is wider than normal. Everything else about the synapse works.',
      stop: 5, art: { gap: 'wide' },
      why: 'Diffusion still carries the molecules across, only more slowly. Delayed, not stopped — and that delay at every synapse is why signals are not instant.'
    },
    {
      id: 'burst',
      text: 'A burst of impulses arrives and many vesicles empty into the gap at once.',
      stop: 5, art: { vesicles: 'many' },
      why: 'More neurotransmitter fills more receptors, so the threshold is passed easily. Extra chemical makes firing more certain, not bigger.'
    },
    {
      id: 'few',
      text: 'Very little neurotransmitter is released, so only a few receptors are filled.',
      stop: 4, art: { vesicles: 'few' },
      why: 'Binding happened, but not enough of it. A new impulse starts only when enough receptors are filled to reach the threshold.'
    }
  ];

  var INK = '#2d2a26', MUTED = '#8d8880', HAIR = '#e8e2d9', PAPER = '#faf8f5', DONE = '#4f7d63';

  var CSS = [
    '.svw-syn{--a:#a6603c;box-sizing:border-box;background:#fff;border:1px solid #e8e3db;border-radius:16px;',
    'padding:1rem 1rem 1.05rem;color:' + INK + ';font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;',
    'display:grid;gap:.5rem;line-height:1.4}',
    '.svw-syn *,.svw-syn *::before,.svw-syn *::after{box-sizing:border-box}',
    '.svw-syn p,.svw-syn h3{margin:0}',
    '.svw-syn .kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--a)}',
    '.svw-syn .ttl{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.22rem;line-height:1.2;margin-top:.12rem}',
    '.svw-syn .mid{display:grid;gap:.55rem}',
    '.svw-syn.is-wide .mid{grid-template-columns:1.02fr .98fr;gap:.9rem;align-items:start}',
    '.svw-syn .stage{background:' + PAPER + ';border:1px solid ' + HAIR + ';border-radius:12px;padding:.45rem .55rem .5rem}',
    '.svw-syn .dia{display:block;width:100%;max-width:360px;max-height:118px;height:auto;margin:0 auto}',
    '.svw-syn.is-wide .dia{max-width:100%;max-height:180px}',
    '.svw-syn .scen{font-size:.82rem;line-height:1.45;color:#4a453e;margin-top:.35rem;min-height:2.6em}',
    '.svw-syn .rows{display:grid;gap:.25rem}',
    '.svw-syn .row{display:flex;align-items:center;gap:.5rem;width:100%;text-align:left;',
    'background:' + PAPER + ';border:1px solid #ddd7cd;border-radius:10px;padding:.32rem .5rem;',
    'font:600 .82rem/1.3 Inter,system-ui,sans-serif;color:' + INK + ';cursor:pointer;-webkit-appearance:none;appearance:none}',
    '.svw-syn .row:focus-visible{outline:2px solid var(--a);outline-offset:2px}',
    '.svw-syn .row .bdg{flex:0 0 auto;width:19px;height:19px;border-radius:50%;display:flex;align-items:center;',
    'justify-content:center;background:#fff;border:1px solid #ddd7cd;font-size:.68rem;font-weight:700;color:#5b564e;',
    'font-variant-numeric:tabular-nums}',
    '.svw-syn .row .lab{flex:1 1 auto}',
    '.svw-syn .row .frm{flex:0 0 auto;font-size:.66rem;font-weight:600;color:' + MUTED + '}',
    '.svw-syn .row[aria-pressed="true"]{background:' + INK + ';border-color:' + INK + ';color:#fff}',
    '.svw-syn .row[aria-pressed="true"] .bdg{background:#fff;border-color:#fff;color:' + INK + '}',
    '.svw-syn .row[aria-pressed="true"] .frm{color:rgba(255,255,255,.72)}',
    '.svw-syn .row[data-happened="yes"]{background:#fff;border-color:' + HAIR + '}',
    '.svw-syn .row[data-happened="yes"] .bdg{background:' + DONE + ';border-color:' + DONE + ';color:#fff}',
    '.svw-syn .row[data-happened="no"]{background:#fff;border-color:' + HAIR + ';color:#9a948b}',
    '.svw-syn .row[data-happened="no"] .frm{color:#b5afa5}',
    '.svw-syn .row[data-picked="yes"]{box-shadow:inset 0 0 0 2px var(--a)}',
    '.svw-syn .row[disabled]{cursor:default}',
    '.svw-syn .act{display:flex;align-items:center;gap:.6rem;justify-content:space-between;margin-top:.38rem}',
    '.svw-syn .run{font-size:.74rem;color:' + MUTED + ';font-variant-numeric:tabular-nums}',
    '.svw-syn .go{flex:0 0 auto;background:' + INK + ';color:#fff;border:1px solid ' + INK + ';border-radius:10px;',
    'padding:.5rem .95rem;font:600 .82rem/1 Inter,system-ui,sans-serif;cursor:pointer;-webkit-appearance:none;appearance:none}',
    '.svw-syn .go:focus-visible{outline:2px solid var(--a);outline-offset:2px}',
    '.svw-syn .go[disabled]{background:#fff;color:#a9a39a;border-color:#e0d9cd;cursor:default}',
    '.svw-syn .cap{font-size:.84rem;line-height:1.5;color:#4a453e;min-height:3.6em}',
    '.svw-syn .cap b{font-weight:700;color:' + INK + '}',
    '.svw-syn .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}'
  ].join('');

  var SVG = [
    '<svg class="dia" viewBox="0 0 340 116" preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false">',
    '<g class="g-post">',
    '<path d="M344,46 H240 V38 a10,10 0 0 0 -10,-10 H202 a12,12 0 0 0 -12,12 V74 a12,12 0 0 0 12,12 H230 a10,10 0 0 0 10,-10 V70 H344 Z" fill="#fff" stroke="#d8d1c4" stroke-width="1.6"/>',
    '<path class="pk" fill="' + PAPER + '" stroke="#cdc5b7" stroke-width="1.5"/>',
    '<path class="pk" fill="' + PAPER + '" stroke="#cdc5b7" stroke-width="1.5"/>',
    '<path class="pk" fill="' + PAPER + '" stroke="#cdc5b7" stroke-width="1.5"/>',
    '<circle class="plug" cx="194" cy="42" r="4.4" fill="#cfc8bb" opacity="0"/>',
    '<circle class="plug" cx="194" cy="57" r="4.4" fill="#cfc8bb" opacity="0"/>',
    '<circle class="plug" cx="194" cy="72" r="4.4" fill="#cfc8bb" opacity="0"/>',
    '<rect class="imp2" x="202" y="47" width="15" height="22" rx="6" opacity="0"/>',
    '</g>',
    '<path d="M-4,46 H112 V38 a10,10 0 0 1 10,-10 H150 a12,12 0 0 1 12,12 V74 a12,12 0 0 1 -12,12 H122 a10,10 0 0 1 -10,-10 V70 H-4 Z" fill="#fff" stroke="#d8d1c4" stroke-width="1.6"/>',
    '<circle class="ves" cx="128" cy="42" r="6.5" fill="' + PAPER + '" stroke="#c2bbad" stroke-width="1.4"/>',
    '<circle class="ves" cx="143" cy="57" r="6.5" fill="' + PAPER + '" stroke="#c2bbad" stroke-width="1.4"/>',
    '<circle class="ves" cx="127" cy="72" r="6.5" fill="' + PAPER + '" stroke="#c2bbad" stroke-width="1.4"/>',
    '<circle class="ves vx" cx="146" cy="39" r="6.5" fill="' + PAPER + '" stroke="#c2bbad" stroke-width="1.4" opacity="0"/>',
    '<circle class="ves vx" cx="145" cy="74" r="6.5" fill="' + PAPER + '" stroke="#c2bbad" stroke-width="1.4" opacity="0"/>',
    '<g class="enz" stroke="#b0a99b" stroke-width="1.6" stroke-linecap="round" opacity="0">',
    '<path d="M167,34 l6,6 M173,34 l-6,6"/><path d="M172,58 l6,6 M178,58 l-6,6"/><path d="M166,76 l6,6 M172,76 l-6,6"/>',
    '</g>',
    '<rect class="imp" x="-30" y="47" width="15" height="22" rx="6" opacity="0"/>',
    '<circle class="mol" r="3.7" fill="#6f6a61" opacity="0"/>',
    '<circle class="mol" r="3.7" fill="#6f6a61" opacity="0"/>',
    '<circle class="mol" r="3.7" fill="#6f6a61" opacity="0"/>',
    '<circle class="mol" r="3.7" fill="#6f6a61" opacity="0"/>',
    '<circle class="mol" r="3.7" fill="#6f6a61" opacity="0"/>',
    '<line class="pline" y1="20" y2="94" stroke-width="1.2" stroke-dasharray="3 3" opacity="0"/>',
    '<g class="pflag" opacity="0"><rect x="-10" y="0" width="20" height="17" rx="5"/>',
    '<text x="0" y="12.6" text-anchor="middle" font-size="11.5" font-weight="700" fill="#fff" font-family="Inter,sans-serif">1</text></g>',
    '<line class="tline" y1="20" y2="94" stroke="' + DONE + '" stroke-width="1.8" opacity="0"/>',
    '<g class="tflag" opacity="0"><rect x="-10" y="0" width="20" height="17" rx="5" fill="' + DONE + '"/>',
    '<text x="0" y="12.6" text-anchor="middle" font-size="11.5" font-weight="700" fill="#fff" font-family="Inter,sans-serif">1</text></g>',
    '<text x="62" y="107" text-anchor="middle" font-size="11.5" fill="' + MUTED + '" font-family="Inter,sans-serif">first neurone</text>',
    '<text class="lgap" x="176" y="107" text-anchor="middle" font-size="11.5" fill="' + MUTED + '" font-family="Inter,sans-serif">gap</text>',
    '<text class="lnext" x="290" y="107" text-anchor="middle" font-size="11.5" fill="' + MUTED + '" font-family="Inter,sans-serif">next neurone</text>',
    '</svg>'
  ].join('');

  function clamp01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function ease(t) { return t * t * (3 - 2 * t); }
  function lower(s) { return s.charAt(0).toLowerCase() + s.slice(1); }

  window.SVWidget = {
    meta: {
      id: 'synapse-electrical-to-chemical',
      title: 'How far does the signal get?',
      teaches: 'At a synapse the electrical impulse stops at the gap; neurotransmitter is released, diffuses across and binds to receptor molecules, and only then does a new electrical impulse start.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ((ctx.accent || '') + '').trim();
      if (!accent) {
        try { accent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim(); } catch (e) { accent = ''; }
      }
      if (!/^#[0-9a-f]{3,8}$/i.test(accent)) accent = '#a6603c';
      var reduced = !!ctx.reducedMotion;
      if (!reduced && window.matchMedia) {
        try { reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e2) {}
      }

      var style = document.createElement('style');
      style.textContent = CSS;
      root.appendChild(style);

      var wrap = document.createElement('div');
      wrap.className = 'svw-syn';
      wrap.style.setProperty('--a', accent);
      wrap.innerHTML =
        '<div><p class="kick">Synapse</p><h3 class="ttl">How far does the signal get?</h3></div>' +
        '<div class="mid">' +
          '<div class="stage">' + SVG + '<p class="scen"></p></div>' +
          '<div class="ctl"><div class="rows"></div>' +
            '<div class="act"><p class="run"></p><button type="button" class="go">Check</button></div>' +
          '</div>' +
        '</div>' +
        '<p class="cap"></p><div class="sr" aria-live="polite"></div>';
      root.appendChild(wrap);

      var q = function (s) { return wrap.querySelector(s); };
      var qa = function (s) { return Array.prototype.slice.call(wrap.querySelectorAll(s)); };

      var scenEl = q('.scen'), capEl = q('.cap'), runEl = q('.run'),
          goEl = q('.go'), srEl = q('.sr'), rowsEl = q('.rows');
      var postG = q('.g-post'), imp = q('.imp'), imp2 = q('.imp2'),
          pline = q('.pline'), pflag = q('.pflag'), pnum = q('.pflag text'),
          tline = q('.tline'), tflag = q('.tflag'), tnum = q('.tflag text'),
          enzG = q('.enz'), lgap = q('.lgap'), lnext = q('.lnext');
      var pockets = qa('.pk'), plugs = qa('.plug'), ves = qa('.ves'),
          vesExtra = qa('.vx'), mols = qa('.mol');

      imp.setAttribute('fill', accent);
      imp2.setAttribute('fill', accent);
      pline.setAttribute('stroke', accent);
      q('.pflag rect').setAttribute('fill', accent);

      /* ---------- the chain, as buttons ---------- */
      var rowEls = STEPS.map(function (s) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'row';
        b.setAttribute('aria-pressed', 'false');
        b.innerHTML = '<span class="bdg"></span><span class="lab"></span><span class="frm"></span>';
        b.querySelector('.bdg').textContent = s.n;
        b.querySelector('.lab').textContent = s.label;
        b.querySelector('.frm').textContent = s.form;
        b.addEventListener('click', function () { pick(s.n); });
        rowsEl.appendChild(b);
        return b;
      });

      /* ---------- state ---------- */
      var st = { picked: 0, checked: false, correct: false, streak: 0, mastered: false, attempted: 0, first: true };
      var item = null, queue = [], raf = 0, guard = 0, molCount = 3;
      var POCKET_Y = [42, 57, 72];

      function geom(it) {
        var wide = it.art.gap === 'wide';
        return { postX: wide ? 208 : 190, wide: wide, dir: it.art.dir === -1 ? -1 : 1 };
      }
      function stepX(n, it) {
        var g = geom(it);
        if (g.dir === -1) return [0, 196, 178, 168, 150, 62][n];
        return Math.min([0, 150, 170, g.postX - 4, g.postX + 9, g.postX + 92][n], 320);
      }
      function pocketPath(y, kind) {
        if (kind === 'wrong') return 'M190,' + (y - 6) + ' h7 v12 h-7 z';
        return 'M190,' + (y - 6) + ' a6,6 0 0 1 0,12 z';
      }

      function applyArt(it) {
        var g = geom(it);
        postG.setAttribute('transform', 'translate(' + (g.postX - 190) + ',0)');
        lgap.setAttribute('x', g.wide ? 185 : 176);
        lnext.setAttribute('x', g.wide ? 300 : 290);

        var vmode = it.art.vesicles;
        ves.forEach(function (c) {
          c.setAttribute('fill', vmode === 'empty' ? 'none' : PAPER);
          c.setAttribute('stroke-dasharray', vmode === 'empty' ? '3 2.4' : 'none');
        });
        vesExtra.forEach(function (c) { c.setAttribute('opacity', vmode === 'many' ? '1' : '0'); });

        pockets.forEach(function (p, i) { p.setAttribute('d', pocketPath(POCKET_Y[i], it.art.receptors)); });
        plugs.forEach(function (p) { p.setAttribute('opacity', it.art.receptors === 'plug' ? '1' : '0'); });
        enzG.setAttribute('opacity', it.art.gap === 'enzyme' ? '1' : '0');

        molCount = vmode === 'many' ? 5 : vmode === 'few' ? 1 : 3;
      }

      function durs(it) {
        return { travel: 460, rel: 240, dif: it.art.gap === 'wide' ? 720 : 520, bind: 200, fire: 440, mark: 260 };
      }
      function total(it) {
        var d = durs(it), S = it.stop;
        return d.travel + (S >= 2 ? d.rel : 0) + (S >= 3 ? d.dif : 0) +
               (S >= 4 ? d.bind : 0) + (S >= 5 ? d.fire : 0) + d.mark;
      }
      function frac(it, ms) {
        var d = durs(it), S = it.stop, t = ms;
        var f = { travel: 0, rel: 0, dif: 0, bind: 0, fire: 0, mark: 0 };
        f.travel = clamp01(t / d.travel); t -= d.travel; if (t < 0) return f;
        if (S >= 2) { f.rel = clamp01(t / d.rel); t -= d.rel; if (t < 0) return f; }
        if (S >= 3) { f.dif = clamp01(t / d.dif); t -= d.dif; if (t < 0) return f; }
        if (S >= 4) { f.bind = clamp01(t / d.bind); t -= d.bind; if (t < 0) return f; }
        if (S >= 5) { f.fire = clamp01(t / d.fire); t -= d.fire; if (t < 0) return f; }
        f.mark = clamp01(t / d.mark);
        return f;
      }

      function paint(f) {
        var g = geom(item), i;
        var startX = g.dir === -1 ? 348 : -30;
        var endX = g.dir === -1 ? 197 : 139;
        imp.setAttribute('x', startX + (endX - startX) * ease(f.travel));
        imp.setAttribute('opacity', f.travel > 0 ? 0.95 : 0);

        var gapStart = 166, target = g.postX - 11;
        for (i = 0; i < mols.length; i++) {
          var m = mols[i];
          if (i >= molCount) { m.setAttribute('opacity', '0'); continue; }
          var sy = 40 + (i % 3) * 15 + (i > 2 ? 7 : 0);
          var cx = gapStart + (target - gapStart) * ease(f.dif);
          cx += ((g.postX + 4) - target) * f.bind;
          var ty = POCKET_Y[i % 3];
          var cy = sy + (ty - sy) * f.bind + Math.sin(f.dif * 7 + i * 2) * 2.4 * (1 - f.dif);
          var op = f.rel;
          if (item.art.gap === 'enzyme') { op = f.rel * (1 - 0.85 * f.mark); }
          m.setAttribute('cx', cx);
          m.setAttribute('cy', cy);
          m.setAttribute('opacity', op);
        }

        imp2.setAttribute('x', 202 + 128 * ease(f.fire));
        imp2.setAttribute('opacity', f.fire > 0 ? 0.95 : 0);

        tline.setAttribute('opacity', f.mark);
        tflag.setAttribute('opacity', f.mark);
        placeFlags(f.mark > 0);
      }

      function placeFlags(revealed) {
        var px = st.picked ? stepX(st.picked, item) : 0;
        var tx = stepX(item.stop, item);
        if (revealed && st.picked && st.picked !== item.stop && Math.abs(px - tx) < 24) {
          if (px < tx) { px -= 11; tx += 11; } else { px += 11; tx -= 11; }
        }
        px = Math.max(12, Math.min(328, px));
        tx = Math.max(12, Math.min(328, tx));
        pflag.setAttribute('transform', 'translate(' + px + ',0)');
        pline.setAttribute('x1', px); pline.setAttribute('x2', px);
        tflag.setAttribute('transform', 'translate(' + tx + ',0)');
        tline.setAttribute('x1', tx); tline.setAttribute('x2', tx);
        var show = (st.picked && !(revealed && st.picked === item.stop)) ? 1 : 0;
        pflag.setAttribute('opacity', show);
        pline.setAttribute('opacity', show ? 0.55 : 0);
        if (st.picked) pnum.textContent = st.picked;
        tnum.textContent = item.stop;
      }

      function stopAnim() {
        if (raf) { cancelAnimationFrame(raf); raf = 0; }
        if (guard) { clearTimeout(guard); guard = 0; }
      }

      function run() {
        stopAnim();
        if (reduced) { paint(frac(item, total(item) + 10)); return; }
        var t0 = null, dur = total(item), it = item;
        raf = requestAnimationFrame(function loop(now) {
          if (t0 === null) { t0 = now; }
          var e = now - t0;
          paint(frac(it, e));
          if (e < dur) { raf = requestAnimationFrame(loop); } else { raf = 0; }
        });
        /* one-shot guard: if frames are throttled (background tab), still land
           on the finished picture rather than a frozen half-reveal. */
        guard = setTimeout(function () {
          guard = 0;
          if (raf) { cancelAnimationFrame(raf); raf = 0; }
          if (item === it) { paint(frac(it, dur + 10)); }
        }, dur + 500);
      }

      /* ---------- flow ---------- */
      function shuffled() {
        var rest = ITEMS.filter(function (x) { return x.id !== 'normal'; });
        for (var i = rest.length - 1; i > 0; i--) {
          var j = Math.floor(Math.random() * (i + 1)), t = rest[i]; rest[i] = rest[j]; rest[j] = t;
        }
        return rest;
      }
      function nextItem() {
        if (!queue.length) queue = shuffled();
        setItem(queue.shift());
      }

      function setItem(it) {
        stopAnim();
        item = it;
        st.picked = 0; st.checked = false; st.correct = false;
        applyArt(it);
        scenEl.textContent = it.text;
        rowEls.forEach(function (b) {
          b.disabled = false;
          b.setAttribute('aria-pressed', 'false');
          b.removeAttribute('data-happened');
          b.removeAttribute('data-picked');
        });
        goEl.textContent = 'Check';
        goEl.disabled = true;
        paint(frac(it, -1));
        pflag.setAttribute('opacity', 0); pline.setAttribute('opacity', 0);
        tflag.setAttribute('opacity', 0); tline.setAttribute('opacity', 0);
        imp.setAttribute('opacity', 0); imp2.setAttribute('opacity', 0);
        mols.forEach(function (m) { m.setAttribute('opacity', 0); });
        capEl.innerHTML = st.first
          ? 'Tap the last step that still happens, then press <b>Check</b>.'
          : (st.mastered ? 'Another one — same chain, a different fault.' : 'A new synapse. Where does this one stop?');
        publish();
      }

      function pick(n) {
        if (st.checked) return;
        st.picked = n;
        rowEls.forEach(function (b, i) { b.setAttribute('aria-pressed', i + 1 === n ? 'true' : 'false'); });
        goEl.disabled = false;
        placeFlags(false);
        srEl.textContent = 'Chosen: step ' + n + ', ' + STEPS[n - 1].label + '.';
        publish();
      }

      function check() {
        st.checked = true;
        st.attempted++;
        st.first = false;
        st.correct = st.picked === item.stop;
        if (st.correct) { st.streak++; if (st.streak >= 3) st.mastered = true; }
        else { st.streak = 0; }

        rowEls.forEach(function (b, i) {
          if (document.activeElement === b) goEl.focus();
          b.disabled = true;
          b.setAttribute('aria-pressed', 'false');
          b.setAttribute('data-happened', i + 1 <= item.stop ? 'yes' : 'no');
          if (i + 1 === st.picked) b.setAttribute('data-picked', 'yes');
        });

        var verdict;
        if (st.correct) {
          verdict = item.stop === 5
            ? '<b>Right</b> — it goes the whole way and a new impulse starts.'
            : '<b>Right</b> — it gets to step ' + item.stop + ' and no further.';
        } else if (st.picked > item.stop) {
          verdict = '<b>Not quite</b> — step ' + (item.stop + 1) + ' (' + lower(STEPS[item.stop].label) + ') does not happen here.';
        } else {
          verdict = '<b>Not quite</b> — step ' + (st.picked + 1) + ' (' + lower(STEPS[st.picked].label) + ') still happens here.';
        }

        var extra = '';
        if (st.mastered && st.streak === 3) {
          extra = ' <b>Three in a row — you have it:</b> no electricity crosses the gap; a chemical does, and binding starts the new impulse.';
        }
        capEl.innerHTML = verdict + ' ' + item.why + extra;
        srEl.textContent = capEl.textContent;

        runEl.textContent = (st.mastered || st.streak === 0) ? ''
          : st.streak + ' right in a row — ' + (3 - st.streak) + ' to go';
        goEl.textContent = st.mastered ? 'Another anyway' : 'Next';
        goEl.disabled = false;
        run();
        publish();
      }

      function publish() {
        root.dataset.svState = JSON.stringify({
          item: item ? item.id : null,
          picked: st.picked || null,
          answer: item ? item.stop : null,
          checked: st.checked,
          correct: st.checked ? st.correct : null,
          streak: st.streak,
          mastered: st.mastered,
          attempted: st.attempted
        });
      }

      goEl.addEventListener('click', function () {
        if (st.checked) { nextItem(); } else if (st.picked) { check(); }
      });

      /* wide layout decided by measured width, not viewport */
      function fit() {
        var w = root.clientWidth || wrap.clientWidth;
        if (w >= 620) { wrap.classList.add('is-wide'); } else { wrap.classList.remove('is-wide'); }
      }
      if (window.ResizeObserver) { new ResizeObserver(fit).observe(root); }
      else { window.addEventListener('resize', fit); }
      fit();

      setItem(ITEMS[0]);
    }
  };
})();
