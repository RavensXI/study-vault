window.SVWidget = {
  meta: {
    id: 'insulate-to-target',
    title: 'Insulate the House to Hit 85% Efficiency',
    teaches: 'Thicker insulation and better materials cut wasted thermal energy, raising efficiency towards (but never reaching) 100% — at a cost.'
  },

  mount: function (root, ctx) {
    var accent = (ctx && ctx.accent) || '#b4653a';
    var reduced = !!(ctx && ctx.reducedMotion);

    /* ---------------- physics model ---------------- */
    var INPUT = 2000;            // W delivered by the heater
    var TARGET = 0.85;           // target efficiency
    var BASE = 20;               // W always lost through floor and draughts

    var WALLS = [
      { label: 'None',        sub: 'bare cavity',      loss: 360, cost: 0 },
      { label: 'Cavity',      sub: 'trapped air',      loss: 130, cost: 600 },
      { label: 'Solid + board', sub: 'insulated solid', loss: 70,  cost: 2400 }
    ];
    var GLAZE = [
      { label: 'Single', sub: 'one pane',    loss: 220, cost: 0 },
      { label: 'Double', sub: 'gas between', loss: 80,  cost: 1800 }
    ];
    var LOFT_COST_PER_50 = 200;
    var CHEAPEST = 3600;         // loft 300 mm + cavity walls + double glazing

    function loftLoss(t) { return 30 + 280 * (50 / (50 + t)); }

    function derive(p) {
      var lo = loftLoss(p.loftThickness);
      var wa = WALLS[p.wallChoice].loss;
      var gl = GLAZE[p.glazingChoice].loss;
      var heatLossRate = lo + wa + gl + BASE;
      var efficiency = (INPUT - heatLossRate) / INPUT;
      var cost = (p.loftThickness / 50) * LOFT_COST_PER_50 +
                 WALLS[p.wallChoice].cost + GLAZE[p.glazingChoice].cost;
      return {
        loft: lo, wall: wa, glass: gl,
        heatLossRate: heatLossRate,
        efficiency: efficiency,
        cost: cost,
        hitTarget: efficiency >= TARGET
      };
    }

    /* ---------------- helpers ---------------- */
    function rgba(hex, a) {
      var h = hex.replace('#', '');
      if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
      var n = parseInt(h, 16);
      return 'rgba(' + ((n >> 16) & 255) + ',' + ((n >> 8) & 255) + ',' + (n & 255) + ',' + a + ')';
    }
    function money(v) { return '£' + v.toLocaleString('en-GB'); }

    var uid = 'itw' + Math.random().toString(36).slice(2, 7);
    var LOSS_COL = '#c2562f';

    /* ---------------- styles ---------------- */
    var css = '' +
'.itw-w{--ac:' + accent + ';--acs:' + rgba(accent, 0.14) + ';--acm:' + rgba(accent, 0.35) + ';' +
'font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:#2d2a26;' +
'background:#faf8f5;padding:14px;border-radius:16px;box-sizing:border-box;line-height:1.45;}' +
'.itw-w *,.itw-w *::before{box-sizing:border-box;}' +
'.itw-w h2{font-family:"Source Serif 4",Georgia,serif;font-size:20px;margin:0 0 6px;font-weight:600;}' +
'.itw-w p{margin:0;}' +
'.itw-hd p{font-size:14px;color:#5b554d;max-width:62ch;}' +
'.itw-card{background:#fff;border:1px solid #e8e2d9;border-radius:14px;padding:12px;}' +
'.itw-stage{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:12px;margin-top:12px;}' +
'@media (max-width:640px){.itw-stage{grid-template-columns:1fr;}}' +
'.itw-house{display:block;width:100%;height:auto;}' +
'.itw-side{display:grid;grid-template-columns:auto minmax(0,1fr);gap:10px;align-items:start;}' +
'.itw-meter{display:block;width:104px;height:auto;}' +
'@media (max-width:360px){.itw-meter{width:86px;}}' +
'.itw-stats{display:grid;gap:8px;align-content:start;}' +
'.itw-stat .k{display:block;font-size:11px;letter-spacing:.03em;text-transform:uppercase;color:#8d8880;}' +
'.itw-stat .v{display:block;font-size:15px;font-weight:600;font-variant-numeric:tabular-nums;}' +
'.itw-stat .v.big{font-size:26px;font-family:"Source Serif 4",Georgia,serif;}' +
'.itw-coins{display:block;width:100%;max-width:150px;height:auto;margin-top:2px;}' +
'.itw-badge{display:inline-block;margin-top:6px;font-size:12px;font-weight:600;padding:3px 8px;border-radius:999px;' +
'border:1px solid #e8e2d9;color:#8d8880;}' +
'.itw-badge.on{border-color:var(--ac);background:var(--acs);color:var(--ac);}' +
'.itw-ctl{margin-top:12px;display:grid;gap:14px;}' +
'.itw-row .lab{display:flex;justify-content:space-between;align-items:baseline;gap:8px;font-size:13px;font-weight:600;margin-bottom:6px;}' +
'.itw-row .lab .now{font-weight:600;color:var(--ac);font-variant-numeric:tabular-nums;}' +
'.itw-row .hint{font-weight:400;font-size:12px;color:#8d8880;}' +
'.itw-w input[type=range]{width:100%;accent-color:var(--ac);margin:0;height:26px;}' +
'.itw-ticks{display:flex;justify-content:space-between;font-size:11px;color:#8d8880;margin-top:-2px;}' +
'.itw-seg{display:flex;gap:8px;flex-wrap:wrap;}' +
'.itw-seg button{flex:1 1 96px;min-width:92px;text-align:left;font:inherit;font-size:13px;font-weight:600;' +
'padding:8px 10px;border:1px solid #e8e2d9;background:#fff;border-radius:11px;color:#2d2a26;cursor:pointer;}' +
'.itw-seg button .s{display:block;font-size:11px;font-weight:400;color:#8d8880;}' +
'.itw-seg button:hover{border-color:var(--acm);}' +
'.itw-seg button[aria-pressed="true"]{border-color:var(--ac);background:var(--acs);}' +
'.itw-seg button[aria-pressed="true"] .s{color:#5b554d;}' +
'.itw-seg button:focus-visible,.itw-w input:focus-visible,.itw-acts button:focus-visible{outline:2px solid var(--ac);outline-offset:2px;}' +
'.itw-fb{margin-top:12px;}' +
'.itw-calc{font-size:14px;font-variant-numeric:tabular-nums;padding-bottom:8px;border-bottom:1px solid #e8e2d9;}' +
'.itw-msg{font-size:14px;margin-top:8px !important;color:#5b554d;}' +
'.itw-msg b{color:#2d2a26;}' +
'.itw-msg.good b{color:var(--ac);}' +
'.itw-note{font-size:12px;color:#8d8880;margin-top:8px !important;}' +
'.itw-acts{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px;}' +
'.itw-acts button{font:inherit;font-size:13px;padding:7px 12px;border-radius:10px;border:1px solid #e8e2d9;' +
'background:#fff;color:#2d2a26;cursor:pointer;}' +
'.itw-acts button:hover{border-color:var(--acm);}';

    /* ---------------- markup ---------------- */
    var houseSVG =
'<svg class="itw-house" viewBox="0 0 360 280" role="img" aria-labelledby="' + uid + 't">' +
  '<title id="' + uid + 't">House cross-section with heat-loss arrows</title>' +
  '<defs>' +
    '<pattern id="' + uid + 'h" width="7" height="7" patternUnits="userSpaceOnUse">' +
      '<path d="M0,7 L7,0" stroke="' + rgba(accent, 0.55) + '" stroke-width="1.1"/></pattern>' +
  '</defs>' +
  '<line x1="8" y1="240.5" x2="352" y2="240.5" stroke="#e8e2d9" stroke-width="2"/>' +
  '<polygon points="76,140 180,76 284,140" fill="#f3efe8" stroke="#2d2a26" stroke-width="1.6" stroke-linejoin="round"/>' +
  '<rect x="90" y="140" width="180" height="100" fill="#ffffff" stroke="#2d2a26" stroke-width="1.6"/>' +
  /* loft insulation */
  '<rect data-ref="loftIns" x="96" y="137" width="168" height="3" fill="#f3efe8" stroke="#c9bfae" stroke-width="1"/>' +
  '<rect data-ref="loftInsP" x="96" y="137" width="168" height="3" fill="url(#' + uid + 'h)" stroke="none"/>' +
  /* wall insulation */
  '<rect data-ref="wallL" x="90" y="140" width="3" height="100" fill="#f3efe8" stroke="none"/>' +
  '<rect data-ref="wallLP" x="90" y="140" width="3" height="100" fill="url(#' + uid + 'h)" stroke="none"/>' +
  '<rect data-ref="wallR" x="267" y="140" width="3" height="100" fill="#f3efe8" stroke="none"/>' +
  '<rect data-ref="wallRP" x="267" y="140" width="3" height="100" fill="url(#' + uid + 'h)" stroke="none"/>' +
  /* door */
  '<rect x="112" y="192" width="32" height="48" fill="#f3efe8" stroke="#2d2a26" stroke-width="1.2"/>' +
  '<circle cx="138" cy="216" r="1.8" fill="#2d2a26"/>' +
  /* window */
  '<rect x="196" y="160" width="52" height="40" fill="#e4edf1" stroke="#2d2a26" stroke-width="1.6"/>' +
  '<rect data-ref="pane2" x="202" y="166" width="40" height="28" fill="none" stroke="#2d2a26" stroke-width="1.2" opacity="0"/>' +
  '<line x1="222" y1="160" x2="222" y2="200" stroke="#2d2a26" stroke-width="0.8" opacity="0.5"/>' +
  /* arrows */
  '<g data-ref="aLoft" transform="translate(180,70) rotate(-90)" fill="none" stroke="' + LOSS_COL + '" stroke-width="2.2" stroke-linecap="round">' +
    '<path data-ref="pLoft" d=""/><path data-ref="hLoft" d="M-9,-5 L0,0 L-9,5" stroke-linejoin="round"/></g>' +
  '<g data-ref="aWall" transform="translate(88,206) rotate(180)" fill="none" stroke="' + LOSS_COL + '" stroke-width="2.2" stroke-linecap="round">' +
    '<path data-ref="pWall" d=""/><path data-ref="hWall" d="M-9,-5 L0,0 L-9,5" stroke-linejoin="round"/></g>' +
  '<g data-ref="aGlass" transform="translate(250,180)" fill="none" stroke="' + LOSS_COL + '" stroke-width="2.2" stroke-linecap="round">' +
    '<path data-ref="pGlass" d=""/><path data-ref="hGlass" d="M-9,-5 L0,0 L-9,5" stroke-linejoin="round"/></g>' +
  /* labels */
  '<text data-ref="tLoft" x="180" y="18" text-anchor="middle" font-size="12" font-weight="600" fill="' + LOSS_COL + '">roof 310 W</text>' +
  '<text data-ref="tWall" x="8" y="196" text-anchor="start" font-size="12" font-weight="600" fill="' + LOSS_COL + '">walls 360 W</text>' +
  '<text data-ref="tGlass" x="352" y="168" text-anchor="end" font-size="12" font-weight="600" fill="' + LOSS_COL + '">window 220 W</text>' +
  '<text x="180" y="262" text-anchor="middle" font-size="11.5" fill="#8d8880">heater input 2000 W &#183; floor &amp; draughts 20 W always lost</text>' +
'</svg>';

    var meterSVG =
'<svg class="itw-meter" viewBox="0 0 112 250" role="img" aria-labelledby="' + uid + 'm">' +
  '<title id="' + uid + 'm">Efficiency meter</title>' +
  '<rect x="34" y="20" width="34" height="200" fill="#f3efe8" stroke="#e8e2d9" stroke-width="1"/>' +
  '<rect data-ref="fill" x="34" y="120" width="34" height="100" fill="' + LOSS_COL + '"/>' +
  '<line x1="34" y1="20" x2="68" y2="20" stroke="#e8e2d9"/>' +
  '<line x1="34" y1="120" x2="68" y2="120" stroke="#e8e2d9"/>' +
  '<text x="30" y="24" text-anchor="end" font-size="10" fill="#8d8880">100</text>' +
  '<text x="30" y="124" text-anchor="end" font-size="10" fill="#8d8880">50</text>' +
  '<text x="30" y="224" text-anchor="end" font-size="10" fill="#8d8880">0</text>' +
  '<line x1="28" y1="50" x2="74" y2="50" stroke="' + accent + '" stroke-width="1.6" stroke-dasharray="4 3"/>' +
  '<text x="78" y="47" font-size="10.5" font-weight="600" fill="' + accent + '">85%</text>' +
  '<text x="78" y="59" font-size="9.5" fill="#8d8880">target</text>' +
  '<text x="51" y="242" text-anchor="middle" font-size="10" fill="#8d8880">efficiency</text>' +
'</svg>';

    var segWall = WALLS.map(function (w, i) {
      return '<button type="button" data-wall="' + i + '" aria-pressed="false">' + w.label +
             '<span class="s">' + w.sub + ' &#183; ' + (w.cost ? money(w.cost) : 'free') + '</span></button>';
    }).join('');
    var segGlaze = GLAZE.map(function (g, i) {
      return '<button type="button" data-glaze="' + i + '" aria-pressed="false">' + g.label +
             '<span class="s">' + g.sub + ' &#183; ' + (g.cost ? money(g.cost) : 'free') + '</span></button>';
    }).join('');

    root.innerHTML =
'<style>' + css + '</style>' +
'<div class="itw-w">' +
  '<div class="itw-hd">' +
    '<h2>Insulate the house to hit 85%</h2>' +
    '<p>The heater puts <strong>2000 W</strong> into the house. Everything that leaks out through the roof, walls and windows is wasted energy. Reach <strong>85% efficiency</strong> &mdash; then see how cheaply you can do it.</p>' +
  '</div>' +
  '<div class="itw-stage">' +
    '<div class="itw-card">' + houseSVG + '</div>' +
    '<div class="itw-card itw-side">' + meterSVG +
      '<div class="itw-stats">' +
        '<div class="itw-stat"><span class="k">Efficiency</span><span class="v big" data-ref="eff">&mdash;</span>' +
          '<span class="itw-badge" data-ref="badge">below target</span></div>' +
        '<div class="itw-stat"><span class="k">Wasted (heat loss)</span><span class="v" data-ref="loss"></span></div>' +
        '<div class="itw-stat"><span class="k">Useful heat kept</span><span class="v" data-ref="useful"></span></div>' +
        '<div class="itw-stat"><span class="k">Total spent</span><span class="v" data-ref="cost"></span>' +
          '<svg class="itw-coins" viewBox="0 0 150 78" role="img" aria-hidden="true"><g data-ref="coins"></g></svg></div>' +
      '</div>' +
    '</div>' +
  '</div>' +
  '<div class="itw-card itw-ctl">' +
    '<div class="itw-row">' +
      '<div class="lab"><label for="' + uid + 'loft">Loft insulation thickness <span class="hint">&pound;200 per 50&nbsp;mm</span></label>' +
        '<span class="now" data-ref="loftVal">100 mm</span></div>' +
      '<input id="' + uid + 'loft" type="range" min="0" max="300" step="50" value="100">' +
      '<div class="itw-ticks"><span>0</span><span>150 mm</span><span>300</span></div>' +
    '</div>' +
    '<div class="itw-row"><div class="lab"><span>Wall type</span><span class="hint">thicker &amp; trapped air = slower conduction</span></div>' +
      '<div class="itw-seg" role="group" aria-label="Wall type">' + segWall + '</div></div>' +
    '<div class="itw-row"><div class="lab"><span>Glazing</span><span class="hint">a gas layer cuts conduction and convection</span></div>' +
      '<div class="itw-seg" role="group" aria-label="Glazing">' + segGlaze + '</div></div>' +
  '</div>' +
  '<div class="itw-card itw-fb" aria-live="polite">' +
    '<div class="itw-calc" data-ref="calc"></div>' +
    '<p class="itw-msg" data-ref="msg"></p>' +
    '<p class="itw-note">Some energy always escapes, so efficiency can get close to 100% but never reach it.</p>' +
    '<div class="itw-acts">' +
      '<button type="button" data-ref="reset">Strip it all out</button>' +
      '<button type="button" data-ref="reveal">Show the cheapest way</button>' +
    '</div>' +
  '</div>' +
'</div>';

    var R = {};
    Array.prototype.forEach.call(root.querySelectorAll('[data-ref]'), function (el) {
      R[el.getAttribute('data-ref')] = el;
    });
    var slider = root.querySelector('#' + uid + 'loft');
    var wallBtns = Array.prototype.slice.call(root.querySelectorAll('[data-wall]'));
    var glazeBtns = Array.prototype.slice.call(root.querySelectorAll('[data-glaze]'));

    /* ---------------- state ---------------- */
    var state = { loftThickness: 100, wallChoice: 0, glazingChoice: 0 };
    var bestCost = null, foundCheapest = false, revealed = false;
    var phase = 0;
    var last = null;

    function wavy(len, amp, ph) {
      var n = Math.max(3, Math.round(len / 3)), d = '', i, x, y;
      for (i = 0; i <= n; i++) {
        x = len * i / n;
        y = amp * Math.sin(x / 7 + ph) * Math.sin(Math.PI * i / n);
        d += (i ? 'L' : 'M') + x.toFixed(1) + ',' + y.toFixed(1) + ' ';
      }
      return d;
    }

    function drawArrows(d) {
      var scale = function (w) { return 10 + 62 * (w / 360); };
      var set = function (pk, hk, w) {
        var L = scale(w);
        R[pk].setAttribute('d', wavy(L, 3.4, phase));
        R[hk].setAttribute('transform', 'translate(' + L.toFixed(1) + ',0)');
      };
      set('pLoft', 'hLoft', d.loft);
      set('pWall', 'hWall', d.wall);
      set('pGlass', 'hGlass', d.glass);
    }

    function drawCoins(cost) {
      var n = Math.round(cost / 200), i, s = '', perCol = 7;
      for (i = 0; i < n; i++) {
        var col = Math.floor(i / perCol), row = i % perCol;
        var cx = 16 + col * 32, cy = 70 - row * 5;
        s += '<ellipse cx="' + cx + '" cy="' + cy + '" rx="12" ry="4.6" fill="' + rgba(accent, 0.18) +
             '" stroke="' + accent + '" stroke-width="1"/>';
      }
      if (!n) s = '<text x="16" y="72" font-size="11" fill="#8d8880">nothing spent yet</text>';
      R.coins.innerHTML = s;
    }

    function update() {
      var d = derive(state);
      last = d;

      /* house */
      var h = 3 + (state.loftThickness / 300) * 24;
      R.loftIns.setAttribute('y', (140 - h).toFixed(1)); R.loftIns.setAttribute('height', h.toFixed(1));
      R.loftInsP.setAttribute('y', (140 - h).toFixed(1)); R.loftInsP.setAttribute('height', h.toFixed(1));
      R.loftInsP.setAttribute('opacity', state.loftThickness ? 1 : 0);

      var ww = [3, 10, 16][state.wallChoice];
      R.wallL.setAttribute('width', ww); R.wallLP.setAttribute('width', ww);
      R.wallR.setAttribute('width', ww); R.wallR.setAttribute('x', 270 - ww);
      R.wallRP.setAttribute('width', ww); R.wallRP.setAttribute('x', 270 - ww);
      R.wallLP.setAttribute('opacity', state.wallChoice ? 1 : 0);
      R.wallRP.setAttribute('opacity', state.wallChoice ? 1 : 0);

      R.pane2.setAttribute('opacity', state.glazingChoice ? 1 : 0);

      drawArrows(d);
      R.tLoft.textContent = 'roof ' + Math.round(d.loft) + ' W';
      R.tWall.textContent = 'walls ' + Math.round(d.wall) + ' W';
      R.tGlass.textContent = 'window ' + Math.round(d.glass) + ' W';

      /* meter */
      var hgt = d.efficiency * 200;
      R.fill.setAttribute('y', (220 - hgt).toFixed(1));
      R.fill.setAttribute('height', hgt.toFixed(1));
      R.fill.setAttribute('fill', d.hitTarget ? accent : LOSS_COL);

      /* stats */
      var pct = d.efficiency * 100;
      R.eff.textContent = pct.toFixed(1) + '%';
      R.loss.textContent = Math.round(d.heatLossRate) + ' W';
      R.useful.textContent = Math.round(INPUT - d.heatLossRate) + ' W';
      R.cost.textContent = money(d.cost);
      R.badge.textContent = d.hitTarget ? 'target reached' : 'below target';
      R.badge.className = 'itw-badge' + (d.hitTarget ? ' on' : '');
      drawCoins(d.cost);

      /* controls */
      R.loftVal.textContent = state.loftThickness === 0 ? 'none' : state.loftThickness + ' mm';
      wallBtns.forEach(function (b) {
        b.setAttribute('aria-pressed', String(+b.dataset.wall === state.wallChoice));
      });
      glazeBtns.forEach(function (b) {
        b.setAttribute('aria-pressed', String(+b.dataset.glaze === state.glazingChoice));
      });

      /* feedback */
      R.calc.innerHTML = 'efficiency = (2000 W &minus; <b>' + Math.round(d.heatLossRate) +
        ' W</b>) &divide; 2000 W = <b>' + d.efficiency.toFixed(3) + '</b> = <b>' + pct.toFixed(1) + '%</b>';

      if (d.hitTarget) {
        if (bestCost === null || d.cost < bestCost) bestCost = d.cost;
        if (d.cost <= CHEAPEST) foundCheapest = true;
      }

      var msg;
      if (!d.hitTarget) {
        var need = d.heatLossRate - INPUT * (1 - TARGET);
        msg = 'Not there yet: <b>' + Math.round(d.heatLossRate) + ' W</b> is still escaping. Cut about <b>' +
              Math.ceil(need) + ' W</b> more to reach 85%.';
      } else if (d.cost <= CHEAPEST) {
        msg = '<b>Cheapest solution found</b> &mdash; 85% for ' + money(d.cost) +
              '. Deep loft insulation plus cavity walls beats paying ' + money(WALLS[2].cost) +
              ' for insulated solid walls.';
      } else {
        msg = '<b>Target reached</b> at ' + pct.toFixed(1) + '% for ' + money(d.cost) +
              '. There is a cheaper combination that still hits 85% &mdash; which measure gives you the most watts per pound?';
      }
      if (revealed && !foundCheapest) {
        msg += ' The cheapest possible is ' + money(CHEAPEST) + ': 300 mm loft, cavity walls, double glazing.';
      }
      R.msg.innerHTML = msg;
      R.msg.className = 'itw-msg' + (d.hitTarget ? ' good' : '');

      root.dataset.svState = JSON.stringify({
        loftThickness: state.loftThickness,
        wallChoice: state.wallChoice,
        glazingChoice: state.glazingChoice,
        heatLossRate: d.heatLossRate,
        efficiency: d.efficiency,
        efficiencyPercent: +pct.toFixed(2),
        cost: d.cost,
        hitTarget: d.hitTarget,
        bestCost: bestCost,
        foundCheapest: foundCheapest
      });
    }

    /* ---------------- events ---------------- */
    slider.addEventListener('input', function () {
      state.loftThickness = +slider.value;
      update();
    });
    wallBtns.forEach(function (b) {
      b.addEventListener('click', function () { state.wallChoice = +b.dataset.wall; update(); });
    });
    glazeBtns.forEach(function (b) {
      b.addEventListener('click', function () { state.glazingChoice = +b.dataset.glaze; update(); });
    });
    R.reset.addEventListener('click', function () {
      state.loftThickness = 0; state.wallChoice = 0; state.glazingChoice = 0;
      slider.value = '0'; revealed = false; update();
    });
    R.reveal.addEventListener('click', function () {
      revealed = true;
      state.loftThickness = 300; state.wallChoice = 1; state.glazingChoice = 1;
      slider.value = '300'; update();
    });

    /* ---------------- animation ---------------- */
    if (!reduced) {
      var timer = setInterval(function () {
        if (!root.isConnected) { clearInterval(timer); return; }
        phase += 0.35;
        if (last) drawArrows(last);
      }, 90);
    }

    update();
  }
};