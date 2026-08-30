var W = {
  meta: {
    id: 'elizabeths-crossroads',
    title: "Elizabeth's Crossroads: Marry or Wait?",
    teaches: "Every marriage and succession option available to Elizabeth carried a specific political risk, so refusing to choose was the strategy that minimised total danger."
  },

  initialState: function () {
    return { marriage: 2, succession: 1 };
  },

  apply: function (state, action) {
    var s = { marriage: state.marriage, succession: state.succession };
    if (action.t === 'set') {
      if (action.key === 'marriage') {
        var m = Math.round(action.v);
        if (m < 0) m = 0; if (m > 2) m = 2;
        s.marriage = m;
      } else if (action.key === 'succession') {
        var c = Math.round(action.v);
        if (c < 0) c = 0; if (c > 1) c = 1;
        s.succession = c;
      }
      return s;
    }
    if (action.t === 'reset') {
      return { marriage: 2, succession: 1 };
    }
    return s;
  },

  derive: function (state) {
    var m = state.marriage;
    var religiousRisk = (m === 0) ? 1 : 0;
    var warRisk = (m === 0) ? 1 : 0;
    var civilWarRiskFaction = (m === 1) ? 1 : 0;
    var diplomaticLeverage = (m === 2) ? 1 : 0;

    var s = state.succession;
    var plotRisk = (s === 0) ? 1 : 0;
    var civilWarRiskSuccession = (s === 1) ? 1 : 0;

    var totalRiskFlags = religiousRisk + warRisk + civilWarRiskFaction + plotRisk + civilWarRiskSuccession;

    return {
      religiousRisk: religiousRisk,
      warRisk: warRisk,
      civilWarRiskFaction: civilWarRiskFaction,
      diplomaticLeverage: diplomaticLeverage,
      plotRisk: plotRisk,
      civilWarRiskSuccession: civilWarRiskSuccession,
      totalRiskFlags: totalRiskFlags
    };
  },

  regions: function (state, w, h) {
    var regs = [];
    // Marriage signposts (top band)
    var topY = h * 0.22;
    var xSign = w * 0.85;
    var ys = [h * 0.06, h * 0.22, h * 0.38];
    for (var i = 0; i < 3; i++) {
      regs.push({
        x: xSign - 40, y: ys[i] - 22, w: 80, h: 44,
        action: { t: 'set', key: 'marriage', v: i }
      });
    }
    // Succession signposts (bottom band)
    var ys2 = [h * 0.62, h * 0.82];
    for (var j = 0; j < 2; j++) {
      regs.push({
        x: xSign - 40, y: ys2[j] - 22, w: 80, h: 44,
        action: { t: 'set', key: 'succession', v: j }
      });
    }
    return regs;
  },

  controls: [
    { key: 'marriage', label: 'Marriage choice (0=Catholic prince, 1=domestic noble, 2=stay unmarried)', min: 0, max: 2, step: 1, value: 2, unit: 'path' },
    { key: 'succession', label: 'Succession choice (0=name James now, 1=stay silent)', min: 0, max: 1, step: 1, value: 1, unit: 'path' }
  ],

  render: function (ctx, state, derived, w, h, acc) {
    var ink = '#2d2a26', muted = '#8d8880', grid = '#e8e2d9';
    ctx.fillStyle = '#f7f3ec';
    ctx.fillRect(0, 0, w, h);

    // faint map texture lines
    ctx.strokeStyle = grid;
    ctx.lineWidth = 1;
    for (var gx = 0; gx < w; gx += 40) {
      ctx.beginPath(); ctx.moveTo(gx, 0); ctx.lineTo(gx, h); ctx.stroke();
    }
    for (var gy = 0; gy < h; gy += 40) {
      ctx.beginPath(); ctx.moveTo(0, gy); ctx.lineTo(w, gy); ctx.stroke();
    }

    ctx.font = '13px Georgia, serif';
    ctx.fillStyle = ink;
    ctx.textAlign = 'left';
    ctx.fillText('Elizabeth\u2019s Crossroads', 14, 20);

    // Start marker (Elizabeth)
    var startX = w * 0.08;
    var marriageY = h * 0.22;
    var successionY = h * 0.72;

    function drawStart(y, label) {
      ctx.beginPath();
      ctx.arc(startX, y, 10, 0, Math.PI * 2);
      ctx.fillStyle = acc;
      ctx.fill();
      ctx.strokeStyle = ink;
      ctx.stroke();
      ctx.fillStyle = ink;
      ctx.textAlign = 'center';
      ctx.font = '11px Georgia, serif';
      ctx.fillText(label, startX, y + 26);
    }
    drawStart(marriageY, 'Elizabeth');
    drawStart(successionY, 'Elizabeth');

    var xSign = w * 0.85;

    // ---- Marriage crossroad ----
    var mYs = [h * 0.06, h * 0.22, h * 0.38];
    var mLabels = ['Catholic Prince', 'Home-grown Noble', 'Stay Single'];
    var mSelected = state.marriage;

    for (var i = 0; i < 3; i++) {
      var isSel = (i === mSelected);
      ctx.beginPath();
      ctx.moveTo(startX + 12, marriageY);
      ctx.lineTo(xSign - 45, mYs[i]);
      ctx.strokeStyle = isSel ? '#c9a227' : muted;
      ctx.lineWidth = isSel ? 5 : 2;
      ctx.stroke();

      // signpost
      ctx.fillStyle = isSel ? '#c9a227' : '#d8d2c6';
      ctx.strokeStyle = ink;
      ctx.lineWidth = 1;
      ctx.fillRect(xSign - 40, mYs[i] - 14, 80, 28);
      ctx.strokeRect(xSign - 40, mYs[i] - 14, 80, 28);
      ctx.fillStyle = ink;
      ctx.font = '11px Georgia, serif';
      ctx.textAlign = 'center';
      ctx.fillText(mLabels[i], xSign, mYs[i] + 4);

      // badges for this path: religious(cross), war(swords), civilWar(crown), leverage(star)
      var rr = (i === 0) ? 1 : 0;
      var wr = (i === 0) ? 1 : 0;
      var cf = (i === 1) ? 1 : 0;
      var dl = (i === 2) ? 1 : 0;

      var bx = xSign + 55;
      var by = mYs[i];
      drawBadge(ctx, bx, by - 10, '\u271D', rr, acc, muted, 'Faith');
      drawBadge(ctx, bx + 34, by - 10, '\u2694', wr, acc, muted, 'War');
      drawBadge(ctx, bx + 68, by - 10, '\u2654', cf, acc, muted, 'Civil');
      drawBadge(ctx, bx + 102, by - 10, '\u2726', dl, '#4a7a4a', muted, 'Leverage');
    }

    // ---- Succession crossroad ----
    var sYs = [h * 0.62, h * 0.82];
    var sLabels = ['Name James Now', 'Say Nothing'];
    var sSelected = state.succession;

    for (var j = 0; j < 2; j++) {
      var isSel2 = (j === sSelected);
      ctx.beginPath();
      ctx.moveTo(startX + 12, successionY);
      ctx.lineTo(xSign - 45, sYs[j]);
      ctx.strokeStyle = isSel2 ? '#c9a227' : muted;
      ctx.lineWidth = isSel2 ? 5 : 2;
      ctx.stroke();

      ctx.fillStyle = isSel2 ? '#c9a227' : '#d8d2c6';
      ctx.strokeStyle = ink;
      ctx.lineWidth = 1;
      ctx.fillRect(xSign - 40, sYs[j] - 14, 80, 28);
      ctx.strokeRect(xSign - 40, sYs[j] - 14, 80, 28);
      ctx.fillStyle = ink;
      ctx.font = '11px Georgia, serif';
      ctx.textAlign = 'center';
      ctx.fillText(sLabels[j], xSign, sYs[j] + 4);

      var pr = (j === 0) ? 1 : 0;
      var cs = (j === 1) ? 1 : 0;

      var bx2 = xSign + 55;
      var by2 = sYs[j];
      drawBadge(ctx, bx2, by2 - 10, '\u2020', pr, acc, muted, 'Plot');
      drawBadge(ctx, bx2 + 34, by2 - 10, '\u2654', cs, acc, muted, 'Civil');
    }

    // Scoreboard
    var sbX = w - 130, sbY = 12, sbW = 118, sbH = 60;
    ctx.fillStyle = '#fffdf8';
    ctx.strokeStyle = ink;
    ctx.lineWidth = 1;
    ctx.fillRect(sbX, sbY, sbW, sbH);
    ctx.strokeRect(sbX, sbY, sbW, sbH);
    ctx.fillStyle = ink;
    ctx.font = '11px Georgia, serif';
    ctx.textAlign = 'left';
    ctx.fillText('Total risk flags', sbX + 8, sbY + 16);
    ctx.font = 'bold 22px Georgia, serif';
    ctx.fillStyle = derived.totalRiskFlags >= 2 ? '#a13a2f' : acc;
    ctx.fillText(String(derived.totalRiskFlags) + ' / 5', sbX + 8, sbY + 42);

    function drawBadge(ctx, x, y, symbol, active, activeColor, inactiveColor, caption) {
      ctx.beginPath();
      ctx.arc(x, y, 14, 0, Math.PI * 2);
      ctx.fillStyle = active ? activeColor : '#eee9e0';
      ctx.fill();
      ctx.strokeStyle = active ? '#7a2e24' : inactiveColor;
      ctx.lineWidth = active ? 2 : 1;
      ctx.stroke();
      ctx.fillStyle = active ? '#fff' : inactiveColor;
      ctx.font = '12px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(symbol, x, y + 1);
      ctx.textBaseline = 'alphabetic';
      ctx.font = '9px Georgia, serif';
      ctx.fillStyle = active ? ink : inactiveColor;
      ctx.fillText(caption, x, y + 24);
    }
  },

  caption: function (state, derived) {
    var mLabels = ['a Catholic foreign prince', 'a home-grown noble', 'staying unmarried'];
    var sLabels = ['naming James VI now', 'staying silent on the succession'];
    var mText = mLabels[state.marriage];
    var sText = sLabels[state.succession];
    if (derived.totalRiskFlags <= 1) {
      return 'Choosing ' + mText + ' and ' + sText + ' minimises risk to ' + derived.totalRiskFlags + ' flag(s) \u2014 this is close to Elizabeth\u2019s real strategy of "permanent ambiguity".';
    }
    return 'Choosing ' + mText + ' and ' + sText + ' lights up ' + derived.totalRiskFlags + ' risk flags \u2014 every combination carries some danger, but some carry far more than others.';
  }
};

if (typeof module !== 'undefined') module.exports = W;