(function () {
  'use strict';

  var TEMPLATE = [
    '<style>',
    '.svspr{font-family:Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:#2d2a26;background:#faf8f5;padding:16px;border-radius:16px;box-sizing:border-box;max-width:900px;margin:0 auto;}',
    '.svspr *{box-sizing:border-box}',
    '.svspr h2{font-family:"Source Serif 4",Georgia,serif;font-size:19px;margin:0 0 4px;font-weight:600}',
    '.svspr h3{font-family:"Source Serif 4",Georgia,serif;font-size:15px;margin:0 0 8px;font-weight:600}',
    '.svspr .sub{margin:0 0 14px;color:#8d8880;font-size:13px;line-height:1.45}',
    '.svspr .modebar{display:flex;gap:8px;margin-bottom:12px}',
    '.svspr .mb{flex:1;padding:10px;border:1px solid #e8e2d9;background:#fff;border-radius:12px;font:inherit;font-size:14px;color:#2d2a26;cursor:pointer}',
    '.svspr .mb.on{border-color:var(--acc);color:var(--acc);font-weight:600}',
    '.svspr .mb:focus-visible,.svspr .opt:focus-visible,.svspr .again:focus-visible{outline:2px solid var(--acc);outline-offset:2px}',
    '.svspr .card{background:#fff;border:1px solid #e8e2d9;border-radius:14px;padding:10px 10px 6px;margin-bottom:12px}',
    '.svspr canvas{display:block;width:100%;height:250px;touch-action:pan-y}',
    '.svspr .hint{font-size:12px;color:#8d8880;margin:4px 2px 6px;line-height:1.4}',
    '.svspr .sliders{display:grid;gap:10px;grid-template-columns:1fr;margin-bottom:12px}',
    '@media(min-width:560px){.svspr .sliders{grid-template-columns:1fr 1fr}}',
    '.svspr .ctl{display:block;background:#fff;border:1px solid #e8e2d9;border-radius:12px;padding:8px 12px 10px}',
    '.svspr .ctl-top{display:flex;justify-content:space-between;align-items:baseline;font-size:13px;margin-bottom:2px}',
    '.svspr .ctl-v{font-variant-numeric:tabular-nums;color:var(--acc);font-weight:600}',
    '.svspr input[type=range]{width:100%;accent-color:var(--acc);margin:4px 0 0}',
    '.svspr .readout{display:grid;gap:8px;grid-template-columns:1fr 1fr}',
    '@media(min-width:600px){.svspr .readout{grid-template-columns:repeat(4,1fr)}}',
    '.svspr .rcard{background:#fff;border:1px solid #e8e2d9;border-radius:12px;padding:8px 10px}',
    '.svspr .rk{display:block;font-size:10px;color:#8d8880;text-transform:uppercase;letter-spacing:.05em}',
    '.svspr .rv{display:block;font-size:17px;font-variant-numeric:tabular-nums;margin:3px 0 2px}',
    '.svspr .rf{display:block;font-size:11px;color:#8d8880;font-variant-numeric:tabular-nums}',
    '.svspr .idea{font-size:13px;line-height:1.55;border-left:3px solid var(--acc);padding:2px 0 2px 10px;margin:12px 2px}',
    '.svspr .quiz{background:#fff;border:1px solid #e8e2d9;border-radius:14px;padding:12px}',
    '.svspr .q{font-size:13.5px;line-height:1.5;margin:0 0 10px}',
    '.svspr .opts{display:flex;flex-wrap:wrap;gap:8px}',
    '.svspr .opt{padding:8px 14px;border:1px solid #e8e2d9;background:#faf8f5;border-radius:10px;font:inherit;font-size:14px;font-variant-numeric:tabular-nums;color:#2d2a26;cursor:pointer}',
    '.svspr .opt[disabled]{cursor:default}',
    '.svspr .opt.right{border-color:var(--acc);color:var(--acc);font-weight:600;background:#fff}',
    '.svspr .opt.wrong{border-color:#b8433a;color:#b8433a;background:#fff}',
    '.svspr .fb{font-size:13px;line-height:1.5;margin:10px 0 0;min-height:1px}',
    '.svspr .qfoot{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:10px}',
    '.svspr .again{padding:7px 12px;border:1px solid #e8e2d9;background:#faf8f5;border-radius:10px;font:inherit;font-size:13px;color:#2d2a26;cursor:pointer}',
    '.svspr .score{font-size:12px;color:#8d8880;font-variant-numeric:tabular-nums;margin:0}',
    '</style>',
    '<h2>Series vs parallel: same resistors, different circuit</h2>',
    '<p class="sub">Two resistors and one battery. Rewire them and watch the total resistance, the current in each part, and the p.d. across each resistor change.</p>',
    '<div class="modebar" role="group" aria-label="Circuit type">',
    '<button type="button" class="mb on" data-mode="0" data-key="mode">Series</button>',
    '<button type="button" class="mb" data-mode="1" data-key="mode">Parallel</button>',
    '</div>',
    '<div class="card"><canvas role="img"></canvas>',
    '<p class="hint">Arrow thickness (and the speed of the flow) shows how much current passes through that part of the circuit.</p></div>',
    '<div class="sliders">',
    '<label class="ctl"><span class="ctl-top"><span>Resistor R\u2081</span><span class="ctl-v" data-out="r1">4 \u03a9</span></span>',
    '<input type="range" min="1" max="20" step="1" value="4" data-key="r1" aria-label="Resistor R1 in ohms"></label>',
    '<label class="ctl"><span class="ctl-top"><span>Resistor R\u2082</span><span class="ctl-v" data-out="r2">8 \u03a9</span></span>',
    '<input type="range" min="1" max="20" step="1" value="8" data-key="r2" aria-label="Resistor R2 in ohms"></label>',
    '<label class="ctl"><span class="ctl-top"><span>Supply voltage</span><span class="ctl-v" data-out="voltage">12 V</span></span>',
    '<input type="range" min="1" max="20" step="1" value="12" data-key="voltage" aria-label="Supply voltage in volts"></label>',
    '</div>',
    '<div class="readout"></div>',
    '<p class="idea"></p>',
    '<div class="quiz"><h3>Quick check</h3><p class="q"></p><div class="opts"></div><p class="fb"></p>',
    '<div class="qfoot"><button type="button" class="again">New question</button><p class="score">Score: 0 / 0</p></div></div>'
  ].join('');

  window.SVWidget = {
    meta: {
      id: 'series-vs-parallel-resistors',
      title: 'Series vs Parallel: Same Resistors, Different Circuit',
      teaches: 'How total resistance, current distribution and voltage distribution differ between series and parallel arrangements of the same two resistors'
    },

    mount: function (root, ctx) {
      var acc = (ctx && ctx.accent) || '#b4552d';
      var reduced = !!(ctx && ctx.reducedMotion);
      var INK = '#2d2a26', MUTED = '#8d8880', GRID = '#e8e2d9', PAPER = '#faf8f5';

      root.classList.add('svspr');
      root.style.setProperty('--acc', acc);
      root.innerHTML = TEMPLATE;

      var canvas = root.querySelector('canvas');
      var readout = root.querySelector('.readout');
      var ideaEl = root.querySelector('.idea');
      var qEl = root.querySelector('.q');
      var optsEl = root.querySelector('.opts');
      var fbEl = root.querySelector('.fb');
      var scoreEl = root.querySelector('.score');
      var againBtn = root.querySelector('.again');
      var modeBtns = Array.prototype.slice.call(root.querySelectorAll('.mb'));

      var state = { r1: 4, r2: 8, voltage: 12, mode: 0 };
      var quiz = { asked: 0, score: 0, last: null, current: null };

      /* ---------- physics ---------- */
      function derive(s) {
        var r1 = s.r1, r2 = s.r2, V = s.voltage, Rt, It, i1, i2, v1, v2;
        if (s.mode === 0) {
          Rt = r1 + r2;
          It = V / Rt;
          i1 = It; i2 = It;
          v1 = It * r1; v2 = It * r2;
        } else {
          Rt = (r1 * r2) / (r1 + r2);
          v1 = V; v2 = V;
          i1 = V / r1; i2 = V / r2;
          It = V / Rt;
        }
        return {
          totalResistance: Rt, totalCurrent: It,
          current1: i1, current2: i2,
          voltage1: v1, voltage2: v2
        };
      }

      function fmt(x) {
        if (!isFinite(x)) return '—';
        var s = x.toFixed(2);
        s = s.replace(/\.00$/, '').replace(/(\.\d)0$/, '$1');
        return s;
      }

      /* ---------- canvas ---------- */
      function arrowHead(g, x, y, ang, size) {
        g.save();
        g.translate(x, y);
        g.rotate(ang);
        g.beginPath();
        g.moveTo(size, 0);
        g.lineTo(-size * 0.85, size * 0.7);
        g.lineTo(-size * 0.85, -size * 0.7);
        g.closePath();
        g.fill();
        g.restore();
      }

      function polyline(g, pts) {
        g.beginPath();
        g.moveTo(pts[0][0], pts[0][1]);
        for (var i = 1; i < pts.length; i++) g.lineTo(pts[i][0], pts[i][1]);
        g.stroke();
      }

      var phase = 0;

      function draw() {
        var cssW = Math.max(280, canvas.clientWidth || root.clientWidth || 320);
        var cssH = cssW < 420 ? 250 : 275;
        var dpr = window.devicePixelRatio || 1;
        if (canvas.width !== Math.round(cssW * dpr) || canvas.height !== Math.round(cssH * dpr)) {
          canvas.width = Math.round(cssW * dpr);
          canvas.height = Math.round(cssH * dpr);
          canvas.style.height = cssH + 'px';
        }
        var g = canvas.getContext('2d');
        g.setTransform(dpr, 0, 0, dpr, 0, 0);
        g.clearRect(0, 0, cssW, cssH);

        var d = derive(state);
        var fs = cssW < 400 ? 10 : 12;
        var xL = 42, xR = cssW - 26;
        var span = xR - xL;
        var yBot = cssH - 40;
        var cx = (xL + xR) / 2;
        var Imax = Math.max(d.totalCurrent, 1e-12);

        function wOf(I) { return 2 + 6 * Math.min(1, I / Imax); }

        var segs = [], boxes = [];

        if (state.mode === 0) {
          var yTop = 70;
          segs.push({ pts: [[cx - 7, yBot], [xL, yBot], [xL, yTop], [xR, yTop], [xR, yBot], [cx + 7, yBot]], I: d.totalCurrent });
          var bw = Math.min(94, span * 0.30), bh = 26;
          boxes.push({ x: xL + span * 0.32, y: yTop, w: bw, h: bh, lab: 'R\u2081 = ' + state.r1 + ' \u03a9', v: 'V\u2081 = ' + fmt(d.voltage1) + ' V', i: 'I\u2081 = ' + fmt(d.current1) + ' A', below: true });
          boxes.push({ x: xL + span * 0.72, y: yTop, w: bw, h: bh, lab: 'R\u2082 = ' + state.r2 + ' \u03a9', v: 'V\u2082 = ' + fmt(d.voltage2) + ' V', i: 'I\u2082 = ' + fmt(d.current2) + ' A', below: true });
        } else {
          var yB1 = 74, yB2 = yBot - 62;
          segs.push({ pts: [[cx - 7, yBot], [xL, yBot], [xL, yB2]], I: d.totalCurrent });
          segs.push({ pts: [[xL, yB2], [xR, yB2]], I: d.current2 });
          segs.push({ pts: [[xL, yB2], [xL, yB1], [xR, yB1], [xR, yB2]], I: d.current1 });
          segs.push({ pts: [[xR, yB2], [xR, yBot], [cx + 7, yBot]], I: d.totalCurrent });
          var pbw = Math.min(120, span * 0.36), pbh = 26;
          boxes.push({ x: cx, y: yB1, w: pbw, h: pbh, lab: 'R\u2081 = ' + state.r1 + ' \u03a9', v: 'V\u2081 = ' + fmt(d.voltage1) + ' V', i: 'I\u2081 = ' + fmt(d.current1) + ' A', below: true });
          boxes.push({ x: cx, y: yB2, w: pbw, h: pbh, lab: 'R\u2082 = ' + state.r2 + ' \u03a9', v: 'V\u2082 = ' + fmt(d.voltage2) + ' V', i: 'I\u2082 = ' + fmt(d.current2) + ' A', below: true });
        }

        /* base wires */
        g.lineCap = 'round';
        g.lineJoin = 'round';
        g.strokeStyle = INK;
        g.lineWidth = 2;
        g.setLineDash([]);
        segs.forEach(function (s) { polyline(g, s.pts); });

        /* current flow */
        segs.forEach(function (s) {
          var w = wOf(s.I);
          g.strokeStyle = acc;
          g.globalAlpha = 0.85;
          g.lineWidth = w;
          if (reduced) {
            g.setLineDash([]);
          } else {
            var speed = 22 + 70 * Math.min(1, s.I / Imax);
            g.setLineDash([10, 10]);
            g.lineDashOffset = -phase * speed;
          }
          polyline(g, s.pts);
          g.setLineDash([]);
          g.globalAlpha = 1;
          /* heads at midpoint of each straight piece */
          g.fillStyle = acc;
          for (var k = 1; k < s.pts.length; k++) {
            var a = s.pts[k - 1], b = s.pts[k];
            var dx = b[0] - a[0], dy = b[1] - a[1];
            var len = Math.sqrt(dx * dx + dy * dy);
            if (len < 34) continue;
            arrowHead(g, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2, Math.atan2(dy, dx), 4 + w * 0.55);
          }
        });

        /* battery */
        (function () {
          g.strokeStyle = INK;
          g.lineWidth = 2.5;
          g.beginPath(); g.moveTo(cx - 7, yBot - 15); g.lineTo(cx - 7, yBot + 15); g.stroke();
          g.lineWidth = 2;
          g.beginPath(); g.moveTo(cx + 7, yBot - 8); g.lineTo(cx + 7, yBot + 8); g.stroke();
          g.font = fs + 'px Inter, system-ui, sans-serif';
          g.textAlign = 'center';
          g.textBaseline = 'middle';
          g.fillStyle = MUTED;
          g.fillText('+', cx - 17, yBot - 12);
          g.fillText('\u2212', cx + 17, yBot - 12);
          g.fillStyle = INK;
          g.font = '600 ' + (fs + 1) + 'px Inter, system-ui, sans-serif';
          g.fillText(state.voltage + ' V supply', cx, yBot + 26);
        })();

        /* resistor boxes and labels */
        g.textAlign = 'center';
        g.textBaseline = 'middle';
        boxes.forEach(function (b) {
          g.fillStyle = '#ffffff';
          g.strokeStyle = INK;
          g.lineWidth = 1.6;
          g.beginPath();
          var r = 4, x = b.x - b.w / 2, y = b.y - b.h / 2;
          g.moveTo(x + r, y);
          g.arcTo(x + b.w, y, x + b.w, y + b.h, r);
          g.arcTo(x + b.w, y + b.h, x, y + b.h, r);
          g.arcTo(x, y + b.h, x, y, r);
          g.arcTo(x, y, x + b.w, y, r);
          g.closePath();
          g.fill();
          g.stroke();
          g.fillStyle = INK;
          g.font = '600 ' + fs + 'px Inter, system-ui, sans-serif';
          g.fillText(b.lab, b.x, b.y + 0.5);
          g.font = fs + 'px Inter, system-ui, sans-serif';
          g.fillStyle = INK;
          g.fillText(b.v, b.x, b.y - b.h / 2 - 11);
          g.fillStyle = acc;
          g.fillText(b.i, b.x, b.y + b.h / 2 + 11);
        });

        /* caption + total current tag */
        g.textAlign = 'left';
        g.fillStyle = MUTED;
        g.font = fs + 'px Inter, system-ui, sans-serif';
        g.fillText(state.mode === 0 ? 'Series \u2014 one path' : 'Parallel \u2014 two paths', 6, 14);
        g.textAlign = 'right';
        g.fillStyle = acc;
        g.font = '600 ' + fs + 'px Inter, system-ui, sans-serif';
        g.fillText('I total = ' + fmt(d.totalCurrent) + ' A', cssW - 6, 14);
      }

      /* ---------- readout / text ---------- */
      function render() {
        var d = derive(state);
        var r1 = state.r1, r2 = state.r2, V = state.voltage;

        root.querySelector('[data-out="r1"]').textContent = r1 + ' \u03a9';
        root.querySelector('[data-out="r2"]').textContent = r2 + ' \u03a9';
        root.querySelector('[data-out="voltage"]').textContent = V + ' V';
        modeBtns.forEach(function (b) {
          var on = (+b.dataset.mode) === state.mode;
          b.classList.toggle('on', on);
          b.setAttribute('aria-pressed', on ? 'true' : 'false');
        });

        var rFormula = state.mode === 0
          ? 'R\u2081 + R\u2082 = ' + r1 + ' + ' + r2
          : '1/R = 1/' + r1 + ' + 1/' + r2;

        readout.innerHTML =
          '<div class="rcard"><span class="rk">Total resistance</span><span class="rv">' + fmt(d.totalResistance) + ' \u03a9</span><span class="rf">' + rFormula + '</span></div>' +
          '<div class="rcard"><span class="rk">Total current</span><span class="rv">' + fmt(d.totalCurrent) + ' A</span><span class="rf">I = V \u00f7 R = ' + V + ' \u00f7 ' + fmt(d.totalResistance) + '</span></div>' +
          '<div class="rcard"><span class="rk">Through R\u2081</