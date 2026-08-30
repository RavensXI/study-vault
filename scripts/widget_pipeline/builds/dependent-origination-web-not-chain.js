/* StudyVault lesson widget — dependent-origination-web-not-chain
 * Self-contained. No imports, no network, no storage outside root.
 */
(function () {
  'use strict';

  var ROUNDS = [
    {
      id: 'lamp',
      frame: 'An oil lamp burns inside a jar. The lid is sealed and the air runs out. Each arrow runs from a condition to what depends on it — select everything that ceases.',
      removed: 'air',
      nodes: [
        { id: 'oil',    x: 16, y: 16, label: 'Oil',       sub: 'the fuel',    name: 'the oil' },
        { id: 'air',    x: 16, y: 50, label: 'Air',       sub: '',            name: 'the air' },
        { id: 'wick',   x: 16, y: 84, label: 'Wick',      sub: '',            name: 'the wick' },
        { id: 'flame',  x: 50, y: 50, label: 'Flame',     sub: '',            name: 'the flame' },
        { id: 'light',  x: 84, y: 26, label: 'Lamplight', sub: 'in the room', name: 'the lamplight' },
        { id: 'shadow', x: 84, y: 76, label: 'Shadow',    sub: 'on the wall', name: 'the shadow' }
      ],
      edges: [['oil', 'flame'], ['air', 'flame'], ['wick', 'flame'], ['flame', 'light'], ['light', 'shadow']],
      right: 'Right — the flame, the lamplight and the shadow all cease, and the shadow stood two steps from the air. Oil and wick are untouched: the arrows run towards the flame, not back from it.',
      linear: 'The lamplight rested on the flame, and the shadow on the lamplight, so both go as well. Conditions do not stop at the next link along.',
      empty: 'Nothing here holds itself up. The flame needs air, so it goes — and the lamplight and the shadow that rested on it go with it.',
      extra: 'Neither depends on the flame — both were in the lamp before it was lit. Everything is conditioned, but not by everything.',
      mixed: 'The arrows run into the flame from oil and wick, and out of it to lamplight and shadow. Follow them forward, never back.'
    },
    {
      id: 'craving',
      frame: 'Buddhists teach that craving (tanha) for things to be other than they are can fall away completely. Suppose it does — select everything that ceases with it.',
      removed: 'craving',
      nodes: [
        { id: 'contact',  x: 16, y: 18, label: 'Contact',       sub: 'eyes, ears, body', name: 'contact' },
        { id: 'feeling',  x: 16, y: 62, label: 'Feeling',       sub: 'vedana',           name: 'feeling' },
        { id: 'craving',  x: 50, y: 34, label: 'Craving',       sub: 'tanha',            name: 'craving' },
        { id: 'change',   x: 50, y: 88, label: 'Things change', sub: 'anicca',           name: 'impermanence' },
        { id: 'clinging', x: 84, y: 30, label: 'Clinging',      sub: 'holding on',       name: 'clinging' },
        { id: 'dukkha',   x: 84, y: 80, label: 'Suffering',     sub: 'dukkha',           name: 'suffering' }
      ],
      edges: [['contact', 'feeling'], ['feeling', 'craving'], ['craving', 'clinging'], ['clinging', 'dukkha'], ['change', 'dukkha']],
      right: 'Right — clinging and suffering cease, and that is all. Contact, feeling and impermanence carry on untouched, so nothing had to be destroyed: one condition was removed.',
      linear: 'Clinging does go — and suffering rested on clinging, so it goes too. Following the web one step further is the whole point.',
      empty: 'That is the fatalist reading, that the web is fixed in advance. Buddhists teach the opposite: remove craving and clinging goes, and suffering with it.',
      extra: 'None of them depends on craving; they were its conditions, and they stay. Ending suffering does not mean ending experience.',
      mixed: 'Craving fed clinging, and clinging fed suffering. What craving rested on is untouched.'
    },
    {
      id: 'self',
      frame: 'Buddhists teach that there is no fixed, unchanging self (anatta). Suppose someone sees this clearly and the sense of a fixed ‘me’ drops away — select everything that ceases.',
      removed: 'me',
      nodes: [
        { id: 'body',     x: 16, y: 16, label: 'Body',          sub: 'rupa',                name: 'the body' },
        { id: 'feel',     x: 16, y: 50, label: 'Feeling',       sub: 'vedana',              name: 'feeling' },
        { id: 'mind',     x: 16, y: 84, label: 'Consciousness', sub: 'vinnana',             name: 'consciousness' },
        { id: 'me',       x: 50, y: 50, label: 'A fixed ‘me’', sub: '',            name: 'the sense of a ‘me’' },
        { id: 'clinging', x: 84, y: 26, label: 'Clinging',      sub: 'to ‘my’ things', name: 'clinging' },
        { id: 'fear',     x: 84, y: 76, label: 'Fear',          sub: 'of losing yourself',  name: 'fear' }
      ],
      edges: [['body', 'me'], ['feel', 'me'], ['mind', 'me'], ['me', 'clinging'], ['clinging', 'fear']],
      right: 'Right — clinging and fear cease, while body, feeling and consciousness carry straight on. Buddhists teach that no self was holding them together: the sense of a ‘me’ rested on them, not they on it.',
      linear: 'Clinging goes, and the fear of losing yourself rested on that clinging, so it goes too. Follow the arrow one step further.',
      empty: 'A great deal rests on the sense of a fixed ‘me’ in Buddhist teaching: clinging to ‘my’ things and the fear of losing yourself both depend on it.',
      extra: 'Those are conditions of the sense of a ‘me’, not results of it. They do not vanish when it does — that is exactly what anatta claims.',
      mixed: 'The khandas feed the sense of a ‘me’, not the other way round. Only what lies downstream of it ceases.'
    },
    {
      id: 'wave',
      frame: 'A wave is rolling in towards the beach. The wind that raised it drops to nothing — select everything that ceases.',
      removed: 'wind',
      nodes: [
        { id: 'wind',  x: 16, y: 16, label: 'Wind',      sub: '',               name: 'the wind' },
        { id: 'water', x: 16, y: 50, label: 'Water',     sub: '',               name: 'the water' },
        { id: 'floor', x: 16, y: 84, label: 'Sea bed',   sub: 'its shape',      name: 'the sea bed' },
        { id: 'wave',  x: 50, y: 50, label: 'The wave',  sub: '',               name: 'the wave' },
        { id: 'ride',  x: 84, y: 26, label: 'The ride',  sub: 'a surfer takes', name: 'the ride' },
        { id: 'sound', x: 84, y: 76, label: 'The sound', sub: 'of it breaking', name: 'the sound' }
      ],
      edges: [['wind', 'wave'], ['water', 'wave'], ['floor', 'wave'], ['wave', 'ride'], ['wave', 'sound']],
      right: 'Right — the wave, the ride and the sound all cease. Water and sea bed stay exactly as they were: they were conditions of the wave, and a wave is something happening, not a thing that owns itself.',
      linear: 'The wave goes — and the ride and the sound rested on the wave, so they go with it. The cascade does not stop after one step.',
      empty: 'The wave is not a thing in its own right. It is water behaving in a certain way because of wind and sea bed, and without the wind that behaviour stops.',
      extra: 'Neither depends on the wave; both are among its conditions. Everything is conditioned, but not by everything.',
      mixed: 'The arrows run into the wave from water and sea bed, and out of it to the ride and the sound.'
    }
  ];

  var MASTERY = 'Right — three in a row, and you have it. Conditions make a web, not a chain: pull one out and everything resting on it goes, while whatever it rested on carries on. That is why Buddhists teach that suffering can end.';

  var CSS = [
    '.svw-doweb{',
    'font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;box-sizing:border-box;max-width:100%;}',
    '.svw-doweb *,.svw-doweb *::before,.svw-doweb *::after{box-sizing:border-box;}',
    '.svw-doweb .svw-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--svw-a,#7a6a55);line-height:1.3;}',
    '.svw-doweb .svw-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.2rem;line-height:1.25;margin:.14rem 0 .4rem;}',
    '.svw-doweb .svw-frame{font-size:.84rem;line-height:1.5;color:#4b463f;margin:0 0 .55rem;}',
    '.svw-doweb .svw-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;height:242px;padding:6px;overflow:hidden;}',
    '.svw-doweb .svw-web{position:relative;height:100%;max-width:560px;margin:0 auto;}',
    '.svw-doweb .svw-lines{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible;}',
    '.svw-doweb .svw-node{position:absolute;transform:translate(-50%,-50%);width:31%;max-width:158px;min-width:78px;',
    'display:flex;flex-direction:column;align-items:center;gap:1px;padding:.34rem .3rem;text-align:center;',
    'background:#fff;border:1px solid #ddd7cd;border-radius:10px;color:#2d2a26;font:inherit;cursor:pointer;',
    'overflow-wrap:break-word;word-break:break-word;}',
    '.svw-doweb .svw-node:focus-visible{outline:2px solid var(--svw-a,#7a6a55);outline-offset:2px;}',
    '.svw-doweb .svw-nlabel{font-size:.76rem;font-weight:600;line-height:1.2;}',
    '.svw-doweb .svw-nsub{font-size:.68rem;line-height:1.2;color:#8d8880;}',
    '.svw-doweb .svw-ntag{font-size:.66rem;font-weight:700;letter-spacing:.03em;line-height:1.2;margin-top:1px;}',
    '.svw-doweb .svw-ntag:empty{display:none;}',
    '.svw-doweb .svw-node[data-marked="1"]{background:#2d2a26;border-color:#2d2a26;color:#fff;}',
    '.svw-doweb .svw-node[data-marked="1"] .svw-nsub{color:#cfc9c0;}',
    '.svw-doweb .svw-node[data-fate="gone"]{background:#fff;border-style:dashed;border-color:#ddd7cd;color:#8d8880;}',
    '.svw-doweb .svw-node[data-fate="gone"] .svw-nlabel{text-decoration:line-through;}',
    '.svw-doweb .svw-node[data-fate="gone"] .svw-ntag{color:#4f7d63;}',
    '.svw-doweb .svw-node[data-fate="stays"]{background:#fff;border-color:#ddd7cd;color:#2d2a26;}',
    '.svw-doweb .svw-node[data-fate="stays"] .svw-ntag{color:#8d8880;}',
    '.svw-doweb .svw-node[data-fate] .svw-nsub{color:#8d8880;}',
    '.svw-doweb .svw-node[data-youmarked="1"]{box-shadow:0 0 0 2px var(--svw-a,#7a6a55);}',
    '.svw-doweb .svw-removed{position:absolute;transform:translate(-50%,-50%);width:31%;max-width:158px;min-width:78px;',
    'display:flex;flex-direction:column;align-items:center;gap:1px;padding:.34rem .3rem;text-align:center;',
    'background:#f3efe8;border:1px dashed #c9c2b6;border-radius:10px;color:#8d8880;overflow-wrap:break-word;word-break:break-word;}',
    '.svw-doweb .svw-removed .svw-nlabel{font-size:.76rem;font-weight:600;line-height:1.2;text-decoration:line-through;}',
    '.svw-doweb .svw-removed .svw-nsub{font-size:.68rem;line-height:1.2;color:#8d8880;}',
    '.svw-doweb .svw-bar{display:flex;align-items:center;gap:.6rem;flex-wrap:wrap;margin:.6rem 0 .5rem;}',
    '.svw-doweb .svw-btn{font-family:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;border-radius:10px;',
    'border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer;}',
    '.svw-doweb .svw-btn:focus-visible{outline:2px solid var(--svw-a,#7a6a55);outline-offset:2px;}',
    '.svw-doweb .svw-quiet{font-family:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;border-radius:10px;',
    'border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;cursor:pointer;}',
    '.svw-doweb .svw-run{font-size:.75rem;color:#8d8880;margin-left:auto;font-variant-numeric:tabular-nums;}',
    '.svw-doweb .svw-run:empty{display:none;}',
    '.svw-doweb .svw-cap{font-size:.84rem;line-height:1.5;color:#2d2a26;min-height:44px;margin:0;}',
    '.svw-doweb .svw-sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0;}',
    '.svw-doweb:not(.svw-nomotion) .svw-node{transition:background .16s ease,color .16s ease,border-color .16s ease;}',
    '@media (max-width:430px){.svw-doweb .svw-node,.svw-doweb .svw-removed{width:32%;}}'
  ].join('');

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function svg(tag) {
    return document.createElementNS('http://www.w3.org/2000/svg', tag);
  }

  /* Transitive closure: every node reachable forward from the removed node. */
  function computeFallout(round) {
    var out = {};
    round.edges.forEach(function (e) {
      (out[e[0]] = out[e[0]] || []).push(e[1]);
    });
    var gone = {}, queue = (out[round.removed] || []).slice();
    while (queue.length) {
      var id = queue.shift();
      if (gone[id]) continue;
      gone[id] = true;
      (out[id] || []).forEach(function (n) { if (!gone[n]) queue.push(n); });
    }
    return { gone: gone, direct: (out[round.removed] || []).slice() };
  }

  function joinList(items) {
    if (!items.length) return 'nothing';
    if (items.length === 1) return items[0];
    return items.slice(0, -1).join(', ') + ' and ' + items[items.length - 1];
  }

  window.SVWidget = {
    meta: {
      id: 'dependent-origination-web-not-chain',
      title: 'Remove one condition',
      teaches: 'Dependent origination is a web of mutually conditioning factors, not a one-way chain: remove a condition and everything resting on it ceases, while its own conditions carry on.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var uid = 'svwdo' + Math.random().toString(36).slice(2, 8);

      root.className = (root.className ? root.className + ' ' : '') + 'svw-doweb';
      if (ctx.reducedMotion) root.classList.add('svw-nomotion');

      var style = el('style');
      style.textContent = CSS;
      root.appendChild(style);

      var accent = ctx.accent;
      if (!accent) {
        accent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim();
      }
      if (!accent) accent = '#7a6a55';
      root.style.setProperty('--svw-a', accent);

      root.appendChild(el('div', 'svw-kick', 'Dependent origination · paticcasamuppada'));
      root.appendChild(el('div', 'svw-title', 'Remove one condition'));

      var frameEl = el('p', 'svw-frame', '');
      root.appendChild(frameEl);

      var stage = el('div', 'svw-stage');
      var web = el('div', 'svw-web');
      stage.appendChild(web);
      root.appendChild(stage);

      var lines = svg('svg');
      lines.setAttribute('class', 'svw-lines');
      lines.setAttribute('aria-hidden', 'true');
      var defs = svg('defs');
      [['on', '#a8a096'], ['off', '#ded8ce']].forEach(function (m) {
        var mk = svg('marker');
        mk.setAttribute('id', uid + '-' + m[0]);
        mk.setAttribute('markerWidth', '7');
        mk.setAttribute('markerHeight', '7');
        mk.setAttribute('refX', '6');
        mk.setAttribute('refY', '3');
        mk.setAttribute('orient', 'auto');
        mk.setAttribute('markerUnits', 'userSpaceOnUse');
        var p = svg('path');
        p.setAttribute('d', 'M0,0 L6.5,3 L0,6 z');
        p.setAttribute('fill', m[1]);
        mk.appendChild(p);
        defs.appendChild(mk);
      });
      lines.appendChild(defs);
      web.appendChild(lines);

      var bar = el('div', 'svw-bar');
      var goBtn = el('button', 'svw-btn', 'Check');
      goBtn.type = 'button';
      var runEl = el('span', 'svw-run', '');
      bar.appendChild(goBtn);
      bar.appendChild(runEl);
      root.appendChild(bar);

      var cap = el('p', 'svw-cap', '');
      root.appendChild(cap);

      var sr = el('p', 'svw-sr', '');
      sr.setAttribute('aria-live', 'polite');
      root.appendChild(sr);

      /* ---- state ---- */
      var attempted = 0, streak = 0, mastered = false;
      var round, fallout, marked, committed, wasCorrect;
      var nodeEls = {}, lineEls = [];

      function setState() {
        var payload = {
          round: round.id,
          removed: round.removed,
          marked: Object.keys(marked).filter(function (k) { return marked[k]; }).sort(),
          committed: committed,
          correct: wasCorrect,
          streak: streak,
          mastered: mastered,
          attempted: attempted
        };
        root.dataset.svState = JSON.stringify(payload);
      }

      function nodeById(id) {
        for (var i = 0; i < round.nodes.length; i++) {
          if (round.nodes[i].id === id) return round.nodes[i];
        }
        return null;
      }

      function edgePoint(cx, cy, hw, hh, dx, dy) {
        var len = Math.sqrt(dx * dx + dy * dy) || 1;
        var ux = dx / len, uy = dy / len;
        var tx = Math.abs(ux) > 1e-6 ? hw / Math.abs(ux) : Infinity;
        var ty = Math.abs(uy) > 1e-6 ? hh / Math.abs(uy) : Infinity;
        var t = Math.min(tx, ty);
        return { x: cx + ux * t, y: cy + uy * t };
      }

      function drawEdges() {
        var wr = web.getBoundingClientRect();
        if (!wr.width) return;
        round.edges.forEach(function (e, i) {
          var ln = lineEls[i];
          if (!ln) return;
          var ae = nodeEls[e[0]], be = nodeEls[e[1]];
          if (!ae || !be) return;
          var a = ae.getBoundingClientRect(), b = be.getBoundingClientRect();
          var ax = a.left - wr.left + a.width / 2, ay = a.top - wr.top + a.height / 2;
          var bx = b.left - wr.left + b.width / 2, by = b.top - wr.top + b.height / 2;
          var dx = bx - ax, dy = by - ay;
          var p1 = edgePoint(ax, ay, a.width / 2 + 3, a.height / 2 + 3, dx, dy);
          var p2 = edgePoint(bx, by, b.width / 2 + 8, b.height / 2 + 8, -dx, -dy);
          ln.setAttribute('x1', p1.x.toFixed(1));
          ln.setAttribute('y1', p1.y.toFixed(1));
          ln.setAttribute('x2', p2.x.toFixed(1));
          ln.setAttribute('y2', p2.y.toFixed(1));
        });
      }

      function paintEdges() {
        round.edges.forEach(function (e, i) {
          var ln = lineEls[i];
          if (!ln) return;
          var dead = committed && (fallout.gone[e[1]] || e[0] === round.removed);
          ln.setAttribute('stroke', dead ? '#ded8ce' : '#a8a096');
          ln.setAttribute('stroke-dasharray', dead ? '3 3' : 'none');
          ln.setAttribute('marker-end', 'url(#' + uid + '-' + (dead ? 'off' : 'on') + ')');
        });
      }

      function renderRound() {
        Object.keys(nodeEls).forEach(function (k) { nodeEls[k] = null; });
        nodeEls = {};
        lineEls = [];
        var kill = web.querySelectorAll('.svw-node,.svw-removed');
        for (var i = 0; i < kill.length; i++) kill[i].parentNode.removeChild(kill[i]);
        while (lines.childNodes.length > 1) lines.removeChild(lines.lastChild);

        frameEl.textContent = round.frame;

        round.edges.forEach(function () {
          var ln = svg('line');
          ln.setAttribute('stroke-width', '1.4');
          ln.setAttribute('stroke-linecap', 'round');
          lines.appendChild(ln);
          lineEls.push(ln);
        });

        round.nodes.forEach(function (n) {
          var isRemoved = n.id === round.removed;
          var node = el(isRemoved ? 'div' : 'button', isRemoved ? 'svw-removed' : 'svw-node');
          node.style.left = n.x + '%';
          node.style.top = n.y + '%';
          node.appendChild(el('span', 'svw-nlabel', n.label));
          if (n.sub) node.appendChild(el('span', 'svw-nsub', n.sub));
          if (isRemoved) {
            node.appendChild(el('span', 'svw-nsub', 'removed'));
          } else {
            node.type = 'button';
            node.dataset.id = n.id;
            node.dataset.marked = '0';
            node.appendChild(el('span', 'svw-ntag', ''));
            node.setAttribute('aria-pressed', 'false');
            node.addEventListener('click', function () { toggle(n.id); });
          }
          nodeEls[n.id] = node;
          web.appendChild(node);
        });

        paintEdges();
        drawEdges();
        requestAnimationFrame(drawEdges);
      }

      function toggle(id) {
        if (committed) return;
        marked[id] = !marked[id];
        var node = nodeEls[id];
        node.dataset.marked = marked[id] ? '1' : '0';
        node.setAttribute('aria-pressed', marked[id] ? 'true' : 'false');
        var count = Object.keys(marked).filter(function (k) { return marked[k]; }).length;
        sr.textContent = nodeById(id).name + (marked[id] ? ' marked as ceasing. ' : ' unmarked. ') + count + ' marked.';
        setState();
      }

      function clearMarks() {
        if (committed) return;
        round.nodes.forEach(function (n) {
          if (marked[n.id]) {
            marked[n.id] = false;
            nodeEls[n.id].dataset.marked = '0';
            nodeEls[n.id].setAttribute('aria-pressed', 'false');
          }
        });
        sr.textContent = 'All marks cleared.';
        setState();
      }

      function commit() {
        committed = true;
        attempted += 1;

        var chosen = [], missed = [], extras = [], allGone = [];
        round.nodes.forEach(function (n) {
          if (n.id === round.removed) return;
          var truth = !!fallout.gone[n.id];
          if (truth) allGone.push(n.name);
          if (marked[n.id]) chosen.push(n.name);
          if (truth && !marked[n.id]) missed.push(n.name);
          if (!truth && marked[n.id]) extras.push(n.name);
        });
        wasCorrect = missed.length === 0 && extras.length === 0;

        if (wasCorrect) { streak += 1; if (streak >= 3) mastered = true; }
        else { streak = 0; }

        round.nodes.forEach(function (n) {
          if (n.id === round.removed) return;
          var node = nodeEls[n.id];
          var truth = !!fallout.gone[n.id];
          node.dataset.fate = truth ? 'gone' : 'stays';
          node.dataset.youmarked = marked[n.id] ? '1' : '0';
          node.dataset.marked = '0';
          node.querySelector('.svw-ntag').textContent = truth ? 'ceases' : 'still here';
          node.disabled = true;
        });
        paintEdges();
        drawEdges();

        var text;
        if (wasCorrect && mastered && streak === 3) {
          text = MASTERY;
        } else if (wasCorrect) {
          text = round.right;
        } else if (chosen.length === 0) {
          text = 'Not quite — you said nothing ceases. ' + round.empty;
        } else if (extras.length === 0 && chosen.length === fallout.direct.length &&
                   fallout.direct.every(function (d) { return marked[d]; })) {
          text = 'Not quite — you said only ' + joinList(chosen) + ' ceases. ' + round.linear;
        } else if (missed.length === 0) {
          text = 'Not quite — you also marked ' + joinList(extras) + '. ' + round.extra;
        } else {
          text = 'Not quite — you marked ' + joinList(chosen) + '; what ceases is ' + joinList(allGone) + '. ' + round.mixed;
        }
        cap.textContent = text;
        sr.textContent = text;

        goBtn.textContent = mastered ? 'Another anyway' : 'Next scenario';
        updateRun();
        setState();
      }

      function updateRun() {
        if (mastered) { runEl.textContent = 'You have it'; return; }
        if (attempted === 0) { runEl.textContent = ''; return; }
        if (streak === 0) { runEl.textContent = 'Run back to zero'; return; }
        if (streak === 1) { runEl.textContent = '1 right in a row'; return; }
        runEl.textContent = '2 right in a row — one more';
      }

      function startRound() {
        round = ROUNDS[attempted % ROUNDS.length];
        fallout = computeFallout(round);
        marked = {};
        committed = false;
        wasCorrect = null;
        cap.textContent = '';
        goBtn.textContent = 'Check';
        renderRound();
        updateRun();
        setState();
      }

      goBtn.addEventListener('click', function () {
        if (committed) { startRound(); goBtn.focus(); }
        else commit();
      });

      root.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') clearMarks();
      });

      startRound();

      if (typeof ResizeObserver === 'function') {
        var ro = new ResizeObserver(function () { drawEdges(); });
        ro.observe(web);
      } else {
        window.addEventListener('resize', drawEdges);
      }
    }
  };
})();
