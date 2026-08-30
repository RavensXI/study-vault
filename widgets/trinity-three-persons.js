/* trinity-three-persons - one God in three persons, and the two errors.

   Format (BUILD_GUIDE 0b): a CLASSIFICATION task with a live shield of the
   Trinity as its stage. The shield is not decoration: it carries exactly two
   kinds of claim - three "is" spokes (each person IS the one God) and three
   "is not" edges (no person IS another). Tritheism denies the spokes;
   modalism denies the edges. So each committed verdict is drawn on the
   shield as which half of the doctrine the claim broke.

   Content note: the doctrine is presented as what Christians teach, not
   asserted as fact. Tritheism and modalism are historical technical terms
   and are glossed wherever they appear. */
(function () {
  'use strict';

  var CAT = {
    doctrine: {
      label: 'Keeps the doctrine',
      said: 'it keeps the doctrine',
      name: 'the doctrine',
      gloss: 'both halves hold, each person fully God and no person another'
    },
    tritheism: {
      label: 'Three separate gods · tritheism',
      said: 'three separate gods',
      name: 'tritheism',
      gloss: 'it makes three gods out of the one God'
    },
    modalism: {
      label: 'One God in three modes · modalism',
      said: 'one God in three modes',
      name: 'modalism',
      gloss: 'it makes one God appear as three, one after another'
    }
  };

  /* true category > what the student picked instead. These must read true of
     EVERY claim in the bin, so none of them names a detail of one claim. */
  var DIAG = {
    'doctrine>tritheism': 'Distinct persons are not separate gods. The claim asserts both halves; tritheism drops the one.',
    'doctrine>modalism': 'The persons here stay distinct, and stay so permanently. Modalism makes them one person under three names.',
    'tritheism>doctrine': 'The claim keeps the three but drops the one, and the one is the harder half to hold.',
    'tritheism>modalism': 'Modalism collapses three into one; tritheism splits one into three. Opposite errors.',
    'modalism>doctrine': 'The claim keeps the one but drops the three: the persons become stages, not persons.',
    'modalism>tritheism': 'Tritheism multiplies God; modalism collapses the persons. Opposite errors.'
  };

  var POOL = [
    { c: 'doctrine', t: 'The Father, the Son and the Holy Spirit are all fully God, yet there is one God.',
      w: 'Christians hold both halves at once: three who are each fully God, and one God. No dividing the being, no merging the persons.' },
    { c: 'doctrine', t: 'At the baptism of Jesus the Father speaks, the Son is baptised and the Spirit descends.',
      w: 'All three are there in the same moment, so this cannot be one God taking turns. Christians read Matthew 3:16-17 as a Trinitarian scene.' },
    { c: 'doctrine', t: 'The Father sent the Son into the world.',
      w: 'Sending needs two: one who sends and one who is sent. Yet the one sent is fully God, so "the Son is God" holds alongside "the Son is not the Father".' },
    { c: 'doctrine', t: 'There was never a time when the Son did not exist.',
      w: 'Co-eternal. The Son is not a later creation nor a stage God passed through: the Nicene Creed says "begotten, not made".' },
    { c: 'doctrine', t: 'No one person of the Trinity is greater or lesser than the others.',
      w: 'Co-equal. The three are one in being, so rank between them is ruled out. It is a difference of person, not of status.' },
    { c: 'doctrine', t: 'The Father is not the Son, and the Son is not the Spirit, yet each is the one God.',
      w: 'That is the whole shield in one sentence. The persons are distinct, and the God that each of them is is the same God.' },

    { c: 'tritheism', t: 'There are three gods who work closely together.',
      w: 'Three gods means three beings, however well they cooperate. Christians confess one God, not a committee.' },
    { c: 'tritheism', t: 'The Father, the Son and the Spirit are three separate gods who never disagree.',
      w: 'Agreement is not unity of being. Making them separate gods breaks the claim that each person is the one God.' },
    { c: 'tritheism', t: 'Christians believe in three divine beings, each a god in his own right.',
      w: 'This counts three Gods. Christian teaching counts three persons and one God: number the beings, not the persons.' },
    { c: 'tritheism', t: 'God is a team of three gods sharing one plan.',
      w: 'A shared plan is agreement between beings. The doctrine claims something stronger: one being, not a partnership.' },

    { c: 'modalism', t: 'God switches between three modes, depending on the job in hand.',
      w: 'Switching means only one is in play at a time, so the persons are not permanently distinct. Christians reject that.' },
    { c: 'modalism', t: 'One God wears the mask of the Father, then of the Son, then of the Spirit.',
      w: 'A mask hides one wearer. That makes "the Father is not the Son" false: same person, different face.' },
    { c: 'modalism', t: 'Father, Son and Spirit are three names for one person, used at different times.',
      w: 'Three names for one person is still one person. The doctrine says three persons, distinct from one another and never merged.' },
    { c: 'modalism', t: 'God was the Father in the Old Testament, became the Son, and is now the Spirit.',
      w: 'That puts the persons in a sequence. Christians hold that all three exist at once, and always have.' },
    { c: 'modalism', t: 'The three persons are three roles one God plays, one after another.',
      w: 'Roles belong to one actor. The persons are not parts that a single person plays: each is distinct from the others.' }
  ];

  var NODES = [
    { x: 150, y: 16, w: 60, t: 'Father' },
    { x: 150, y: 76, w: 48, t: 'God', centre: true },
    { x: 44, y: 136, w: 46, t: 'Son' },
    { x: 252, y: 136, w: 82, t: 'Holy Spirit' }
  ];

  var LINKS = [
    { k: 'is', x1: 150, y1: 16, x2: 150, y2: 76, lx: 150, ly: 46, t: 'is', w: 18 },
    { k: 'is', x1: 150, y1: 76, x2: 44, y2: 136, lx: 97, ly: 106, t: 'is', w: 18 },
    { k: 'is', x1: 150, y1: 76, x2: 252, y2: 136, lx: 201, ly: 106, t: 'is', w: 18 },
    { k: 'isnot', x1: 150, y1: 16, x2: 44, y2: 136, lx: 97, ly: 76, t: 'is not', w: 40 },
    { k: 'isnot', x1: 150, y1: 16, x2: 252, y2: 136, lx: 201, ly: 76, t: 'is not', w: 40 },
    { k: 'isnot', x1: 44, y1: 136, x2: 252, y2: 136, lx: 148, ly: 136, t: 'is not', w: 40 }
  ];

  var NS = 'http://www.w3.org/2000/svg';

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt != null) n.textContent = txt;
    return n;
  }

  function sv(tag, attrs) {
    var n = document.createElementNS(NS, tag);
    for (var k in attrs) {
      if (Object.prototype.hasOwnProperty.call(attrs, k)) n.setAttribute(k, attrs[k]);
    }
    return n;
  }

  function firstSentence(s) {
    var i = s.indexOf('. ');
    return i < 0 ? s : s.slice(0, i + 1);
  }

  function css(accent) {
    return [
      '.svw-tri{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26}',
      '.svw-tri *{box-sizing:border-box}',
      '.svw-tri .svw-tri-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:' + accent + '}',
      '.svw-tri .svw-tri-h{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.2rem;line-height:1.25;margin:.15rem 0 .3rem}',
      '.svw-tri .svw-tri-frame{font-size:.84rem;line-height:1.45;color:#5b564e;margin:0 0 .55rem}',
      '.svw-tri .svw-tri-grid{display:block}',
      '.svw-tri.is-wide .svw-tri-grid{display:grid;grid-template-columns:300px 1fr;gap:1.1rem;align-items:start}',
      '.svw-tri .svw-tri-shield{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.35rem .3rem;max-width:318px;margin:0 auto .55rem}',
      '.svw-tri.is-wide .svw-tri-shield{margin:0}',
      '.svw-tri .svw-tri-shield svg{display:block;width:100%;height:auto}',
      '.svw-tri .svw-tri-claim{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.6rem .7rem;margin:0 0 .55rem}',
      '.svw-tri .svw-tri-claim p{margin:0;font-size:.92rem;line-height:1.4;font-weight:600}',
      '.svw-tri .svw-tri-choices{display:flex;flex-direction:column;gap:.4rem;margin:0 0 .55rem}',
      '.svw-tri .svw-tri-opt{font:600 .82rem/1.2 inherit;text-align:left;padding:.5rem .8rem;border:1px solid #ddd7cd;border-radius:10px;background:#faf8f5;color:#2d2a26;cursor:pointer}',
      '.svw-tri .svw-tri-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
      '.svw-tri .svw-tri-echo{display:none;font-size:.82rem;line-height:1.45;margin:0 0 .45rem;color:#5b564e}',
      '.svw-tri .svw-tri-echo b{color:#2d2a26;font-weight:600}',
      '.svw-tri .svw-tri-cap{display:none;font-size:.84rem;line-height:1.5;margin:0 0 .55rem;color:#2d2a26}',
      '.svw-tri .svw-tri-won{display:block;margin-top:.3rem;color:#4f7d63;font-weight:600}',
      '.svw-tri .svw-tri-row{display:flex;align-items:center;gap:.6rem;flex-wrap:wrap}',
      '.svw-tri .svw-tri-go{font:600 .82rem/1.2 inherit;padding:.5rem .95rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}',
      '.svw-tri .svw-tri-go[disabled]{background:#faf8f5;border-color:#ddd7cd;color:#a49d93;cursor:default}',
      '.svw-tri .svw-tri-next{font:600 .82rem/1.2 inherit;padding:.5rem .95rem;border-radius:10px;border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;cursor:pointer;display:none}',
      '.svw-tri .svw-tri-run{font-size:.78rem;color:#8d8880;font-variant-numeric:tabular-nums}',
      '.svw-tri .svw-tri-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}'
    ].join('');
  }

  function mount(root, ctx) {
    ctx = ctx || {};
    var accent = ctx.accent || (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';

    root.className = 'svw-tri';
    root.innerHTML = '';
    var style = document.createElement('style');
    style.textContent = css(accent);
    root.appendChild(style);

    root.appendChild(el('div', 'svw-tri-kick', 'Christian belief · the Trinity'));
    root.appendChild(el('h3', 'svw-tri-h', 'One God, three persons'));
    var frame = el('p', 'svw-tri-frame',
      'Christians teach that each person of the Trinity is fully God, and that no person is another. What does each claim do to that teaching?');
    root.appendChild(frame);

    var grid = el('div', 'svw-tri-grid');
    root.appendChild(grid);

    /* ---- stage: the shield ------------------------------------------ */
    var shieldBox = el('div', 'svw-tri-shield');
    var svg = sv('svg', {
      viewBox: '0 0 300 152',
      role: 'img',
      'aria-label': 'Shield of the Trinity. The Father is God, the Son is God, the Holy Spirit is God. The Father is not the Son, the Son is not the Holy Spirit, the Holy Spirit is not the Father.'
    });
    var linkNodes = [];
    var i, L, N;
    for (i = 0; i < LINKS.length; i++) {
      L = LINKS[i];
      var line = sv('line', { x1: L.x1, y1: L.y1, x2: L.x2, y2: L.y2, 'stroke-linecap': 'round' });
      svg.appendChild(line);
      linkNodes.push({ def: L, line: line });
    }
    for (i = 0; i < LINKS.length; i++) {
      L = LINKS[i];
      svg.appendChild(sv('rect', { x: L.lx - L.w / 2, y: L.ly - 7.5, width: L.w, height: 15, rx: 4, fill: '#faf8f5' }));
      var lt = sv('text', {
        x: L.lx, y: L.ly, 'text-anchor': 'middle', 'dominant-baseline': 'central',
        'font-size': 11, 'font-family': 'Inter, system-ui, sans-serif', 'font-weight': 500
      });
      lt.textContent = L.t;
      svg.appendChild(lt);
      var strike = sv('line', {
        x1: L.lx - L.w / 2 + 2, y1: L.ly, x2: L.lx + L.w / 2 - 2, y2: L.ly,
        'stroke-width': 1.4, stroke: '#9a938a', visibility: 'hidden'
      });
      svg.appendChild(strike);
      linkNodes[i].text = lt;
      linkNodes[i].strike = strike;
    }
    for (i = 0; i < NODES.length; i++) {
      N = NODES[i];
      svg.appendChild(sv('rect', {
        x: N.x - N.w / 2, y: N.y - 11, width: N.w, height: 22, rx: 11,
        fill: N.centre ? accent + '1f' : '#fff',
        stroke: N.centre ? accent : '#d8d1c6', 'stroke-width': 1
      }));
      var nt = sv('text', {
        x: N.x, y: N.y, 'text-anchor': 'middle', 'dominant-baseline': 'central',
        'font-size': 11.5, 'font-family': 'Inter, system-ui, sans-serif', 'font-weight': 600, fill: '#2d2a26'
      });
      nt.textContent = N.t;
      svg.appendChild(nt);
    }
    shieldBox.appendChild(svg);
    grid.appendChild(shieldBox);

    /* ---- working column --------------------------------------------- */
    var col = el('div', 'svw-tri-col');
    grid.appendChild(col);

    var claimBox = el('div', 'svw-tri-claim');
    var claimP = el('p', null, '');
    claimBox.appendChild(claimP);
    col.appendChild(claimBox);

    var order = ['doctrine', 'tritheism', 'modalism'];
    var choices = el('div', 'svw-tri-choices');
    var optBtns = {};
    order.forEach(function (key) {
      var b = el('button', 'svw-tri-opt', CAT[key].label);
      b.type = 'button';
      b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', function () { pick(key); });
      choices.appendChild(b);
      optBtns[key] = b;
    });
    col.appendChild(choices);

    var echo = el('div', 'svw-tri-echo');
    col.appendChild(echo);

    var cap = el('div', 'svw-tri-cap');
    col.appendChild(cap);

    var row = el('div', 'svw-tri-row');
    var go = el('button', 'svw-tri-go', 'Check');
    go.type = 'button';
    go.disabled = true;
    var next = el('button', 'svw-tri-next', 'Next claim');
    next.type = 'button';
    var run = el('span', 'svw-tri-run', '');
    row.appendChild(go);
    row.appendChild(next);
    row.appendChild(run);
    col.appendChild(row);

    var sr = el('p', 'svw-tri-sr', '');
    sr.setAttribute('aria-live', 'polite');
    root.appendChild(sr);

    /* ---- state ------------------------------------------------------- */
    var queue = [];
    var current = null;
    var picked = null;
    var committed = false;
    var streak = 0;
    var attempted = 0;
    var mastered = false;

    function refill() {
      var bag = POOL.slice();
      var a, b, tmp;
      for (a = bag.length - 1; a > 0; a--) {
        b = Math.floor(Math.random() * (a + 1));
        tmp = bag[a]; bag[a] = bag[b]; bag[b] = tmp;
      }
      /* keep neighbours in different bins so all three stay in play */
      for (var m = 1; m < bag.length; m++) {
        if (bag[m].c === bag[m - 1].c) {
          for (var n = m + 1; n < bag.length; n++) {
            if (bag[n].c !== bag[m - 1].c) {
              tmp = bag[m]; bag[m] = bag[n]; bag[n] = tmp;
              break;
            }
          }
        }
      }
      queue = bag;
    }

    function paintShield(verdict) {
      for (var q = 0; q < linkNodes.length; q++) {
        var ln = linkNodes[q];
        var broken = verdict === 'tritheism' ? ln.def.k === 'is'
          : verdict === 'modalism' ? ln.def.k === 'isnot'
            : false;
        var lit = !!verdict && !broken;
        ln.line.setAttribute('stroke', broken ? '#c9c2b6' : (lit ? accent : '#cdc6ba'));
        ln.line.setAttribute('stroke-width', lit ? 2 : 1.5);
        ln.line.setAttribute('stroke-dasharray', broken ? '5 4' : 'none');
        ln.text.setAttribute('fill', broken ? '#9a938a' : (lit ? accent : '#8d8880'));
        ln.text.setAttribute('font-weight', lit ? 600 : 500);
        ln.strike.setAttribute('visibility', broken ? 'visible' : 'hidden');
      }
    }

    function state(extra) {
      var s = { attempted: attempted, streak: streak, mastered: mastered };
      if (current) { s.claim = current.t.slice(0, 44); s.answer = current.c; }
      s.picked = picked;
      for (var k in extra) {
        if (Object.prototype.hasOwnProperty.call(extra, k)) s[k] = extra[k];
      }
      root.dataset.svState = JSON.stringify(s);
    }

    function runLine() {
      if (mastered) { run.textContent = 'You have it — carry on if you want.'; return; }
      if (streak === 0) { run.textContent = attempted ? 'Run reset. Three in a row to finish.' : ''; return; }
      run.textContent = streak === 1 ? '1 right in a row.' : '2 right in a row — one more and you have it.';
    }

    function serve() {
      if (!queue.length) refill();
      current = queue.shift();
      picked = null;
      committed = false;
      claimP.textContent = '“' + current.t + '”';
      order.forEach(function (k) { optBtns[k].setAttribute('aria-pressed', 'false'); });
      frame.style.display = '';
      choices.style.display = '';
      echo.style.display = 'none';
      cap.style.display = 'none';
      go.style.display = '';
      go.disabled = true;
      next.style.display = 'none';
      paintShield(null);
      runLine();
      state({ phase: 'asked' });
    }

    function pick(key) {
      if (committed) return;
      picked = key;
      order.forEach(function (k) { optBtns[k].setAttribute('aria-pressed', k === key ? 'true' : 'false'); });
      go.disabled = false;
      sr.textContent = 'Chosen: ' + CAT[key].label + '.';
      state({ phase: 'picked' });
    }

    function commit() {
      if (committed || !picked) return;
      committed = true;
      attempted++;
      var right = picked === current.c;
      var justMastered = false;
      if (right) {
        streak++;
        if (streak >= 3 && !mastered) { mastered = true; justMastered = true; }
      } else {
        streak = 0;
      }

      paintShield(current.c);

      echo.innerHTML = '';
      var said = el('div', null, 'You said: ');
      said.appendChild(el('b', null, CAT[picked].label));
      echo.appendChild(said);
      if (!right) {
        var truth = el('div', null, 'The answer: ');
        truth.appendChild(el('b', null, CAT[current.c].label));
        echo.appendChild(truth);
      }
      echo.style.display = 'block';

      var msg;
      if (right) {
        msg = 'Right — ' +
          (current.c === 'doctrine' ? 'it keeps the doctrine.' : 'that is ' + CAT[current.c].name + '.') +
          ' ' + (justMastered ? firstSentence(current.w) : current.w);
      } else {
        msg = 'Not quite — you said ' + CAT[picked].said + '. It is ' + CAT[current.c].name + ': ' +
          CAT[current.c].gloss + '. ' + DIAG[current.c + '>' + picked];
      }
      cap.textContent = msg;
      if (justMastered) {
        var wonLine = 'Three in a row — you have it. Both halves hold at once, so the doctrine is neither three gods nor one God in three modes.';
        cap.appendChild(el('span', 'svw-tri-won', wonLine));
        msg = msg + ' ' + wonLine;
      }
      cap.style.display = 'block';

      /* the frame asked the question; the caption is now answering it, so the
         two never stack and the widget does not grow on commit */
      frame.style.display = 'none';
      choices.style.display = 'none';
      go.style.display = 'none';
      next.textContent = mastered ? 'Another anyway' : 'Next claim';
      /* the stylesheet hides this button, so it must be given a real display
         value here - clearing the inline style would fall back to none */
      next.style.display = 'inline-block';
      runLine();
      sr.textContent = msg;
      state({ phase: 'checked', correct: right });
      try { next.focus({ preventScroll: true }); } catch (e1) { /* focus is a nicety */ }
    }

    go.addEventListener('click', commit);
    next.addEventListener('click', function () {
      serve();
      try { optBtns.doctrine.focus({ preventScroll: true }); } catch (e2) { /* nicety */ }
    });
    root.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape' && !committed && picked) {
        picked = null;
        order.forEach(function (k) { optBtns[k].setAttribute('aria-pressed', 'false'); });
        go.disabled = true;
        sr.textContent = 'Choice cleared.';
        state({ phase: 'asked' });
      }
    });

    /* two columns only where both still get a readable measure of prose */
    function fit() {
      var w = root.getBoundingClientRect().width;
      if (w >= 620) { root.classList.add('is-wide'); } else { root.classList.remove('is-wide'); }
    }
    if (typeof ResizeObserver === 'function') {
      new ResizeObserver(fit).observe(root);
    }
    fit();

    refill();
    serve();
  }

  window.SVWidget = {
    meta: {
      id: 'trinity-three-persons',
      title: 'One God, three persons',
      teaches: 'The Trinity as Christians state it: one God in three co-equal, co-eternal persons - not three gods (tritheism) and not one God in three modes (modalism).'
    },
    mount: mount
  };
})();
