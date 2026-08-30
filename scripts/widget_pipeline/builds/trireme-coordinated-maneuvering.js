/* trireme-coordinated-maneuvering
   Ramming was a manoeuvre, not a charge. The student reads a top-down
   tactical picture (sea room, the gap, the water past the enemy's flank)
   and commits to one order. One geometry model decides the outcome and
   draws the track, so the reveal can never drift from the picture. */
(function () {
  'use strict';

  var TURN = 2;     /* ship-widths of clear water needed to come about */
  var MIN_GAP = 2;  /* ship-widths needed to row through, oars out     */

  /* Each situation: sea room across the strait, how many of their ships
     are drawn up abreast, where the gap sits, how much clear water lies
     behind their line, how many of their ships are in the strait.
     Their line is anchored on the near shore, so the open flank (if any)
     is at the bottom of the picture. */
  var SCENES = [
    { key: 'open',   name: 'Open water off the Attic coast',    sea: 10, abreast: 6, gapAt: -1, gapW: 0, depth: 8, fleet: 200 },
    { key: 'gap',    name: 'A gap opens in their line', sea: 10, abreast: 7, gapAt: 3, gapW: 3, depth: 7, fleet: 200 },
    { key: 'narrow', name: 'The strait at its narrowest',        sea: 5,  abreast: 5, gapAt: -1, gapW: 0, depth: 8, fleet: 200 },
    { key: 'crowd',  name: 'More ships crowd in behind',    sea: 6,  abreast: 6, gapAt: -1, gapW: 0, depth: 7, fleet: 300 },
    { key: 'shoal',  name: 'Their shore lies close behind', sea: 9, abreast: 6, gapAt: 2, gapW: 3, depth: 1, fleet: 240 },
    { key: 'thin',   name: 'A thin break in their line',         sea: 10, abreast: 6, gapAt: 4, gapW: 1, depth: 7, fleet: 200 },
    { key: 'ragged', name: 'Dawn: their line rows out', sea: 9, abreast: 6, gapAt: 2, gapW: 2, depth: 6, fleet: 180 }
  ];

  var ORDERS = [
    { id: 'charge',    label: 'Charge straight in — ram prow to prow' },
    { id: 'diekplous', label: 'Diekplous — through the gap, at the sterns' },
    { id: 'periplous', label: 'Periplous — round the end, into the flank' },
    { id: 'hold',      label: 'Hold the line closed, shore to shore' }
  ];

  var SAID = {
    charge:    'you charged straight in, prow to prow',
    diekplous: 'you ordered the diekplous, through the gap',
    periplous: 'you ordered the periplous, round the end',
    hold:      'you held the line closed'
  };

  /* ---- the model ------------------------------------------------- */
  function solve(s) {
    var span = s.abreast + s.gapW;              /* berths their line covers */
    var flank = s.sea - span;                   /* open water past its end  */
    var canDiek = s.gapW >= MIN_GAP && s.depth >= TURN;
    var canPeri = flank >= TURN;
    return {
      key: s.key, name: s.name, sea: s.sea, abreast: s.abreast,
      gapAt: s.gapAt, gapW: s.gapW, depth: s.depth, fleet: s.fleet,
      span: span, flank: flank,
      correct: canDiek ? 'diekplous' : (canPeri ? 'periplous' : 'hold')
    };
  }
  var MODEL = SCENES.map(solve);

  function w(n) { return n + ' ship-width' + (n === 1 ? '' : 's'); }

  function rightShort(s) {
    if (s.correct === 'diekplous') {
      return 'the diekplous — a break ' + w(s.gapW) + ' wide, ' + s.depth + ' behind to turn in';
    }
    if (s.correct === 'periplous') {
      return 'the periplous — ' + w(s.flank) + ' of water past their end';
    }
    return 'hold the line closed — no gap, no water past their end';
  }

  function verdictText(choice, s) {
    var head;
    if (choice === s.correct) {
      if (choice === 'diekplous') {
        return 'Right — ' + SAID[choice] + '. A break ' + w(s.gapW) +
          ' wide lets you row through with the oars out, and ' + s.depth +
          ' behind gives room to come about — 170 rowers pulling as one. You take the stern, where there is no ram.';
      }
      if (choice === 'periplous') {
        return 'Right — ' + SAID[choice] + '. There are ' + w(s.flank) +
          ' of open water past their last ship and coming about takes ' + TURN +
          '. You round the flank and ram the side at the waterline, where the hull is thin and three banks of oars are exposed.';
      }
      return 'Right — ' + SAID[choice] + '. No gap and no water past their end, so nothing can be rowed through or round. Only ' +
        s.abreast + ' of their ' + s.fleet +
        ' ships can reach you at once; Herodotus says the Greeks kept their order while the Persian fleet lost its own.';
    }
    if (choice === 'charge') {
      head = 'Not quite — ' + SAID[choice] +
        '. Both rams meet the strongest timbers, your way stops dead and both hulls are wrecked. A ram opens a hull from the side or quarter.';
    } else if (choice === 'diekplous') {
      head = (s.gapW < MIN_GAP)
        ? 'Not quite — ' + SAID[choice] + '. ' +
          (s.gapW ? 'The break is only ' + w(s.gapW) + ' wide' : 'Their line is closed — there is no break') +
          ', and you need ' + MIN_GAP + ' to row through without your oars being sheared off.'
        : 'Not quite — ' + SAID[choice] + '. The break is wide enough, but only ' + w(s.depth) +
          ' lies behind it — coming about takes ' + TURN +
          ', so you go through and are pinned, stern to them.';
    } else if (choice === 'periplous') {
      head = 'Not quite — ' + SAID[choice] + '. ' +
        (s.flank ? 'Only ' + w(s.flank) + ' of water lies past their last ship'
                 : 'Their line touches both shores, so there is no end to get round') +
        ', and coming about takes ' + TURN + '.';
    } else {
      head = 'Not quite — ' + SAID[choice] + '. Holding is the order when there is no room to manoeuvre, but here ' +
        (s.correct === 'periplous'
          ? 'there are ' + w(s.flank) + ' past the end of their line'
          : 'their line is broken and there is water behind it to turn in') + '.';
    }
    return head + ' Here: ' + rightShort(s) + '.';
  }

  function briefText(s) {
    return s.fleet + ' of their ships are in the strait, but the water only lets ' +
      s.abreast + ' of them reach your line at once. The rest lie astern.';
  }

  var MASTERY = 'Three in a row — you have it. A trireme rams the side or the quarter, never prow to prow, and both manoeuvres need sea room: the diekplous a gap to row through, the periplous an open flank. The narrows at Salamis gave the larger Persian fleet neither.';

  /* ---- widget ---------------------------------------------------- */
  window.SVWidget = {
    meta: {
      id: 'trireme-coordinated-maneuvering',
      title: 'Give the order',
      teaches: 'Ramming at Salamis was a coordinated manoeuvre needing sea room, not a head-on charge; the narrow strait denied the larger Persian fleet the room its numbers needed.'
    },
    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent || (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';
      var still = !!ctx.reducedMotion;
      var SVGNS = 'http://www.w3.org/2000/svg';

      var order = MODEL.slice();
      for (var i = order.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1)), t = order[i]; order[i] = order[j]; order[j] = t;
      }
      var pos = 0, scene = order[0];
      var sel = null, committed = false, streak = 0, mastered = false, attempted = 0;

      /* ---- shell ---- */
      var box = document.createElement('div');
      box.className = 'svw-tri';
      var style = document.createElement('style');
      style.textContent = css(accent, still);
      box.appendChild(style);

      var head = el('div', 'svw-tri__head');
      head.appendChild(txt(el('div', 'svw-tri__kicker'), 'Greek naval tactics'));
      head.appendChild(txt(el('h3', 'svw-tri__title'), 'Give the order'));
      head.appendChild(txt(el('p', 'svw-tri__frame'),
        'Salamis, 480 BC. You command a Greek trireme. Read the water and give the order that puts your bronze ram onto an enemy hull.'));
      box.appendChild(head);

      var row = el('div', 'svw-tri__row');
      var stagewrap = el('div', 'svw-tri__stagewrap');
      var svg = document.createElementNS(SVGNS, 'svg');
      svg.setAttribute('viewBox', '0 0 340 120');
      svg.setAttribute('role', 'img');
      svg.setAttribute('aria-hidden', 'true');
      svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
      stagewrap.appendChild(svg);
      row.appendChild(stagewrap);

      var side = el('div', 'svw-tri__side');
      var stats = el('div', 'svw-tri__stats');
      var sceneEl = el('b', 'svw-tri__scene');
      var numsEl = el('span', 'svw-tri__nums');
      stats.appendChild(sceneEl); stats.appendChild(numsEl);
      side.appendChild(stats);

      var orders = el('div', 'svw-tri__orders');
      orders.setAttribute('role', 'group');
      orders.setAttribute('aria-label', 'Orders');
      var btns = ORDERS.map(function (o) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'svw-tri__order';
        b.setAttribute('aria-pressed', 'false');
        var sp = el('span', 'svw-tri__oname');
        sp.textContent = o.label;
        b.appendChild(sp);
        b.addEventListener('click', function () { pick(o.id); });
        orders.appendChild(b);
        return b;
      });
      side.appendChild(orders);

      var foot = el('div', 'svw-tri__foot');
      var go = document.createElement('button');
      go.type = 'button';
      go.className = 'svw-tri__go';
      go.textContent = 'See what happens';
      go.disabled = true;
      go.addEventListener('click', onGo);
      var streakEl = el('span', 'svw-tri__streak');
      foot.appendChild(go); foot.appendChild(streakEl);
      side.appendChild(foot);
      row.appendChild(side);
      box.appendChild(row);

      var cap = el('p', 'svw-tri__cap');
      box.appendChild(cap);

      var sr = el('p', 'svw-tri__sr');
      sr.setAttribute('aria-live', 'polite');
      box.appendChild(sr);

      root.appendChild(box);

      /* width classes: the modal is resized, not the viewport, so media
         queries would never fire. Read the real width instead. */
      function fit() {
        var wpx = box.getBoundingClientRect().width || 360;
        box.classList.toggle('svw-tri--wide', wpx >= 500);
      }
      fit();
      if (window.ResizeObserver) { new ResizeObserver(fit).observe(box); }

      /* ---- behaviour ---- */
      function pick(id) {
        if (committed) return;
        sel = id;
        btns.forEach(function (b, k) {
          var on = ORDERS[k].id === id;
          b.classList.toggle('is-sel', on);
          b.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
        go.disabled = false;
        publish();
      }

      function onGo() {
        if (!committed) {
          if (!sel) return;
          committed = true;
          attempted++;
          var ok = sel === scene.correct;
          if (ok) { streak++; if (streak >= 3) mastered = true; } else { streak = 0; }
          btns.forEach(function (b, k) {
            b.disabled = true;
            b.classList.toggle('is-right', ORDERS[k].id === scene.correct);
            b.classList.toggle('is-wrong', ORDERS[k].id === sel && !ok);
          });
          drawOutcome(sel);
          cap.textContent = (mastered && ok) ? MASTERY : verdictText(sel, scene);
          cap.classList.add('is-verdict');
          sr.textContent = cap.textContent;
          go.textContent = mastered ? 'Another anyway' : 'Next situation';
          paintStreak();
          publish();
        } else {
          pos = (pos + 1) % order.length;
          scene = order[pos];
          loadScene();
        }
      }

      function loadScene() {
        sel = null; committed = false;
        btns.forEach(function (b) {
          b.disabled = false;
          b.className = 'svw-tri__order';
          b.setAttribute('aria-pressed', 'false');
        });
        go.textContent = 'See what happens';
        go.disabled = true;
        sceneEl.textContent = scene.name;
        numsEl.textContent = 'sea room ' + scene.sea + ' · their line ' + scene.abreast +
          ' abreast · water past its end ' + scene.flank + ' · gap ' +
          (scene.gapW ? scene.gapW + ' wide' : 'none') + ' · coming about needs ' + TURN;
        cap.textContent = briefText(scene);
        cap.classList.remove('is-verdict');
        sr.textContent = scene.name + '. ' + numsEl.textContent + '. ' + cap.textContent;
        paintStreak();
        drawScene();
        publish();
      }

      function paintStreak() {
        streakEl.textContent = mastered
          ? 'you have it'
          : (streak === 0 ? '' : streak + ' right in a row — ' + (3 - streak) + ' more');
      }

      function publish() {
        root.dataset.svState = JSON.stringify({
          scene: scene.key, choice: sel, committed: committed,
          correct: committed ? (sel === scene.correct) : null,
          streak: streak, mastered: mastered, attempted: attempted
        });
      }

      /* ---- drawing --------------------------------------------- */
      var B = 9, VW = 340, VH = 120, EX = 230, OX = 72, LEN = 18, BEAM = 5;
      var fleetLayer, trackLayer, chanTop, chanBot;

      function n(tag, attrs, parent) {
        var e = document.createElementNS(SVGNS, tag);
        for (var k in attrs) { if (attrs.hasOwnProperty(k)) e.setAttribute(k, attrs[k]); }
        (parent || svg).appendChild(e);
        return e;
      }
      function by(b) { return chanTop + (b + 0.5) * B; }
      function ship(g, x, y, dir, fill, op) {
        var tip = x + dir * (LEN / 2), st = x - dir * (LEN / 2), sh = tip - dir * 5, h = BEAM / 2;
        n('path', {
          d: 'M' + tip + ',' + y + ' L' + sh + ',' + (y - h) + ' L' + st + ',' + (y - h) +
             ' L' + st + ',' + (y + h) + ' L' + sh + ',' + (y + h) + ' Z',
          fill: fill, opacity: op == null ? 1 : op
        }, g);
      }
      function occupied(b) {
        if (b < 0 || b >= scene.span) return false;
        if (scene.gapAt >= 0 && b >= scene.gapAt && b < scene.gapAt + scene.gapW) return false;
        return true;
      }

      function drawScene() {
        while (svg.firstChild) { svg.removeChild(svg.firstChild); }
        var chanH = scene.sea * B;
        chanTop = (VH - chanH) / 2; chanBot = chanTop + chanH;
        var farX = Math.min(VW, EX + scene.depth * B + 12);

        n('rect', { x: 0, y: 0, width: VW, height: VH, fill: '#f2f5f4' });
        n('rect', { x: 0, y: 0, width: VW, height: chanTop, fill: '#e7dfd1' });
        n('rect', { x: 0, y: chanBot, width: VW, height: VH - chanBot, fill: '#e7dfd1' });
        if (farX < VW - 2) {
          n('rect', { x: farX, y: chanTop, width: VW - farX, height: chanH, fill: '#e7dfd1' });
          n('line', { x1: farX, y1: chanTop, x2: farX, y2: chanBot, stroke: '#cfc5b3', 'stroke-width': 1 });
        }
        n('line', { x1: 0, y1: chanTop, x2: VW, y2: chanTop, stroke: '#cfc5b3', 'stroke-width': 1 });
        n('line', { x1: 0, y1: chanBot, x2: VW, y2: chanBot, stroke: '#cfc5b3', 'stroke-width': 1 });
        n('text', { x: EX, y: chanTop - 4, fill: '#6f6960', 'font-size': 10, 'text-anchor': 'middle' }).textContent = 'their line';
        n('text', { x: OX, y: chanBot + 11, fill: '#6f6960', 'font-size': 10, 'text-anchor': 'middle' }).textContent = 'your line';

        fleetLayer = n('g', {});
        trackLayer = n('g', {});
        for (var b = 0; b < scene.span; b++) {
          if (occupied(b)) ship(fleetLayer, EX, by(b), -1, '#6b655c');
        }
        ourBerths().forEach(function (ob) { ship(fleetLayer, OX, by(ob), 1, accent); });
      }

      function ourBerths() {
        var c = scene.sea / 2 - 0.5, out = [c - 2, c, c + 2], lo = 0, hi = scene.sea - 1;
        return out.map(function (v) { return Math.max(lo, Math.min(hi, v)); });
      }

      var trackDash = '6 4', trackW = 2;
      function path(d, colour, op) {
        return n('path', {
          d: d, fill: 'none', stroke: colour, 'stroke-width': trackW,
          'stroke-dasharray': trackDash, 'stroke-linecap': 'round', opacity: op
        }, trackLayer);
      }
      function arrowHead(x, y, ang, colour, op) {
        n('path', {
          d: 'M0,0 L-7,-3.2 L-7,3.2 Z', fill: colour, opacity: op,
          transform: 'translate(' + x + ',' + y + ') rotate(' + ang + ')'
        }, trackLayer);
      }
      function hit(x, y, colour) {
        n('circle', { cx: x, cy: y, r: 3.2, fill: colour }, trackLayer);
      }
      function burst(x, y, colour) {
        n('path', {
          d: 'M-5,-5 L5,5 M5,-5 L-5,5', stroke: colour, 'stroke-width': 2,
          'stroke-linecap': 'round', fill: 'none',
          transform: 'translate(' + x + ',' + y + ')'
        }, trackLayer);
      }

      function yc() { return by(ourBerths()[1]); }
      function gapY() { return chanTop + (scene.gapAt + scene.gapW / 2) * B; }
      function nearestTarget() {
        var want = ourBerths()[1], best = null, bd = 99;
        for (var b = 0; b < scene.span; b++) {
          if (!occupied(b)) continue;
          var d = Math.abs(b - want);
          if (d < bd) { bd = d; best = b; }
        }
        return best == null ? 0 : best;
      }

      function drawCharge(colour, op) {
        var y = by(nearestTarget());
        path('M' + (OX + 12) + ',' + yc() + ' L' + (EX - 20) + ',' + y, colour, op);
        arrowHead(EX - 14, y, 0, colour, op);
        burst(EX - 11, y, colour);
      }
      function drawDiek(colour, op, ok) {
        var yg = gapY(), tb = scene.gapAt > 0 ? scene.gapAt - 1 : scene.gapAt + scene.gapW,
            yt = by(tb), out = EX + Math.max(14, Math.min(scene.depth * B - 6, 34));
        path('M' + (OX + 12) + ',' + yc() + ' L' + (EX - 26) + ',' + yg + ' L' + out + ',' + yg +
             ' Q' + (out + 16) + ',' + yg + ' ' + (out + 8) + ',' + yt +
             ' L' + (EX + 15) + ',' + yt, colour, op);
        arrowHead(EX + 13, yt, 180, colour, op);
        if (ok) { hit(EX + 10, yt, colour); }
        else if (scene.gapW < MIN_GAP) { burst(EX - 4, yg, colour); }
        else { burst(Math.min(VW - 8, EX + scene.depth * B + 6), yg, colour); }
      }
      function drawPeri(colour, op, ok) {
        var yEnd = by(scene.span - 1), lane = chanBot - 4, turn = EX + 24;
        path('M' + (OX + 12) + ',' + yc() + ' L' + (EX - 46) + ',' + lane + ' L' + turn + ',' + lane +
             ' Q' + (turn + 14) + ',' + lane + ' ' + (turn + 4) + ',' + (yEnd + 12) +
             ' L' + (EX + 4) + ',' + (yEnd + 8), colour, op);
        arrowHead(EX + 3, yEnd + 7, -120, colour, op);
        if (ok) hit(EX + 2, yEnd + 5, colour);
        else burst(turn, lane, colour);
      }
      function drawHold(colour, op, ok) {
        var bs = ourBerths();
        path('M' + OX + ',' + by(bs[0]) + ' L' + OX + ',' + by(bs[2]), colour, op);
        n('text', { x: OX, y: chanTop - 4, fill: colour, 'font-size': 10, 'text-anchor': 'middle', opacity: op },
          trackLayer).textContent = 'line held';
        if (!ok) return;
        for (var r = 1; r <= 2; r++) {
          for (var b = 0; b < scene.span; b++) {
            if (!occupied(b)) continue;
            ship(trackLayer, EX + r * 23, by(b) + (r % 2 ? 2 : -2), -1, '#a8a196', 0.85);
          }
        }
      }

      function drawOutcome(choice) {
        while (trackLayer.firstChild) { trackLayer.removeChild(trackLayer.firstChild); }
        var c = scene.correct;
        trackDash = '6 4'; trackW = 2;
        if (c === 'hold') drawHold(accent, 1, true);
        else if (c === 'diekplous') drawDiek(accent, 1, true);
        else drawPeri(accent, 1, true);
        if (choice !== c) {
          trackDash = '1.5 3'; trackW = 1.6;
          if (choice === 'charge') drawCharge('#8d8880', 0.9);
          else if (choice === 'diekplous') drawDiek('#8d8880', 0.9, false);
          else if (choice === 'periplous') drawPeri('#8d8880', 0.9, false);
          else drawHold('#8d8880', 0.9, false);
        }
      }

      /* ---- helpers ---- */
      function el(tag, cls) { var e = document.createElement(tag); e.className = cls; return e; }
      function txt(e, s) { e.textContent = s; return e; }

      /* first paint last: the drawing constants above are plain vars, so
         nothing may draw before their assignments have run */
      loadScene();
    }
  };

  function css(accent, still) {
    return [
      '.svw-tri{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.45}',
      '.svw-tri *{box-sizing:border-box}',
      '.svw-tri__kicker{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:' + accent + '}',
      '.svw-tri__title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.2rem;margin:.12rem 0 .18rem;line-height:1.2}',
      '.svw-tri__frame{margin:0 0 .5rem;font-size:.82rem;line-height:1.4;color:#4a453e}',
      '.svw-tri__row{display:block}',
      '.svw-tri--wide .svw-tri__row{display:grid;grid-template-columns:minmax(170px,1fr) minmax(230px,1.1fr);gap:.85rem;align-items:start}',
      '.svw-tri__stagewrap{max-width:340px;margin:0 auto .45rem;background:#faf8f5;border:1px solid #e8e2d9;border-radius:12px;overflow:hidden}',
      '.svw-tri--wide .svw-tri__stagewrap{margin:0;max-width:420px}',
      '.svw-tri__stagewrap svg{display:block;width:100%;height:auto}',
      '.svw-tri__stats{margin:0 0 .4rem;font-size:.74rem;line-height:1.35;color:#6f6960}',
      '.svw-tri__scene{display:block;font-size:.78rem;font-weight:700;color:#2d2a26}',
      '.svw-tri__nums{display:block;font-variant-numeric:tabular-nums}',
      '.svw-tri__orders{display:grid;gap:5px}',
      '.svw-tri__order{display:block;width:100%;text-align:left;font:600 .82rem/1.3 inherit;color:#2d2a26;' +
        'background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;padding:.42rem .6rem;cursor:pointer' +
        (still ? '' : ';transition:background .12s ease,border-color .12s ease') + '}',
      '.svw-tri__order:hover:not(:disabled){border-color:#c6bdaf}',
      '.svw-tri__order.is-sel{background:#2d2a26;border-color:#2d2a26;color:#fff}',
      '.svw-tri__order:disabled{cursor:default;opacity:.7}',
      '.svw-tri__order.is-right{border-color:#4f7d63;box-shadow:inset 0 0 0 1px #4f7d63;opacity:1}',
      '.svw-tri__order.is-wrong{background:#2d2a26;border-color:#2d2a26;color:#fff;opacity:1}',
      '.svw-tri__oname{display:block}',
      '.svw-tri__foot{display:flex;align-items:center;gap:.6rem;margin-top:.45rem}',
      '.svw-tri__go{font:600 .82rem/1.2 inherit;color:#fff;background:#2d2a26;border:1px solid #2d2a26;' +
        'border-radius:10px;padding:.5rem .9rem;cursor:pointer}',
      '.svw-tri__go:disabled{background:#faf8f5;color:#a09a90;border-color:#e0d9cd;cursor:default}',
      '.svw-tri__streak{font-size:.74rem;color:#6f6960;font-variant-numeric:tabular-nums}',
      '.svw-tri__cap{margin:.5rem 0 0;font-size:.84rem;line-height:1.45;color:#4a453e;min-height:3.1em}',
      '.svw-tri__cap.is-verdict{color:#2d2a26}',
      '.svw-tri__sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}'
    ].join('');
  }
})();
